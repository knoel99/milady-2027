"""Tools shared by the package and the CPU experiments E1–E3.

The experiments (``experiments/``) used to carry their own copies of these functions; the published
results in ``experiments/results/`` were computed with them. The frozen copies below are those
versions, verbatim: the package must reproduce them exactly with the settings the experiments use.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from milady.eval import metrics as M
from milady.eval.tilt import exp_tilt, systematic_resample
from milady.train.flow import FourierEmbedding, fm_loss, heun_sample

EXPERIMENTS = Path(__file__).resolve().parent.parent / "experiments"


# ---------------------------------------------------------------------------------------------
# Frozen copies of experiments/common.py (before the move to the package)
# ---------------------------------------------------------------------------------------------
def _old_mean_pdist(a, b, chunk=2048):
    tot = 0.0
    for i in range(0, a.shape[0], chunk):
        tot += torch.cdist(a[i : i + chunk], b).sum().item()
    return tot / (a.shape[0] * b.shape[0])


def _old_energy_distance(x, y, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(x), size=min(n, len(x)), replace=False)
    a = torch.as_tensor(x[idx], dtype=torch.float64)
    b = torch.as_tensor(y[rng.choice(len(y), size=min(n, len(y)), replace=False)], dtype=torch.float64)
    return 2 * _old_mean_pdist(a, b) - _old_mean_pdist(a, a) - _old_mean_pdist(b, b)


def _old_sliced_w1(x, y, n_proj=256, seed=0, n=20000):
    rng = np.random.default_rng(seed)
    th = rng.normal(size=(n_proj, x.shape[1]))
    th /= np.linalg.norm(th, axis=1, keepdims=True)
    xs = x[rng.choice(len(x), size=min(n, len(x)), replace=False)]
    ys = y[rng.choice(len(y), size=min(n, len(y)), replace=False)]
    m = min(len(xs), len(ys))
    px = np.sort(xs[:m] @ th.T, axis=0)
    py = np.sort(ys[:m] @ th.T, axis=0)
    return float(np.abs(px - py).mean())


def _old_fm_loss(model, x1, c, noise_fn=None, extra=None):
    b = x1.shape[0]
    x0 = noise_fn(x1.shape) if noise_fn is not None else torch.randn_like(x1)
    t = torch.rand(b, device=x1.device)
    tt = t.view(-1, *([1] * (x1.dim() - 1)))
    xt = (1 - tt) * x0 + tt * x1
    v = model(xt, t, c)
    loss = ((v - (x1 - x0)) ** 2).mean()
    if extra is not None:
        loss = loss + extra(model, xt, t, c, v, x1)
    return loss


def _old_heun(model, x, c, steps, project=None):
    if project is not None:
        x = project(x)
    h = 1.0 / steps
    n = x.shape[0]
    for k in range(steps):
        t0 = torch.full((n,), k * h)
        t1 = torch.full((n,), (k + 1) * h)
        v0 = model(x, t0, c)
        xe = x + h * v0
        if project is not None:
            xe = project(xe)
        v1 = model(xe, t1, c)
        x = x + 0.5 * h * (v0 + v1)
        if project is not None:
            x = project(x)
    return x


class _Field(torch.nn.Module):
    """Small conditional field (same structure as the MLP field of the experiments)."""

    def __init__(self, dim: int) -> None:
        super().__init__()
        self.t = FourierEmbedding(8)
        self.c = FourierEmbedding(8, scale=8.0)
        self.net = torch.nn.Sequential(torch.nn.Linear(dim + 34, 64), torch.nn.SiLU(), torch.nn.Linear(64, dim))

    def forward(self, x, t, c):
        return self.net(torch.cat([x, self.t(t), self.c(c)], dim=1))


# ---------------------------------------------------------------------------------------------
# Distances
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize(("d", "nx", "ny", "n"), [(3, 5000, 12000, 3000), (21, 1000, 750, 1000)])
def test_energy_distance_reproduces_experiments(d: int, nx: int, ny: int, n: int) -> None:
    """Shapes of E1 (3 variables, n = 3000) and E2 (21 features, n = 1000): identical floats."""
    rng = np.random.default_rng(d)
    x, y = rng.normal(size=(nx, d)), rng.normal(0.1, 1.2, size=(ny, d))
    for seed in (0, 1):
        old = _old_energy_distance(x, y, n=n, seed=seed)
        assert M.energy_distance(x, y, n=n, seed=seed, pdist="torch") == old
        assert M.energy_distance(x, y, n=n, seed=seed) == pytest.approx(old, rel=1e-8)


def test_energy_distance_u_estimator() -> None:
    """U removes the positive O(1/n) bias of V: same law → mean close to 0, V − U > 0."""
    rng = np.random.default_rng(0)
    u, v = [], []
    for seed in range(20):
        x, y = rng.normal(size=(200, 2)), rng.normal(size=(200, 2))
        u.append(M.energy_distance(x, y, seed=seed, estimator="U"))
        v.append(M.energy_distance(x, y, seed=seed, estimator="V"))
    assert all(a > b for a, b in zip(v, u, strict=True))
    assert abs(np.mean(u)) < 3 * np.std(u) / np.sqrt(len(u))
    assert np.mean(v) > 5 * np.std(v) / np.sqrt(len(v))
    with pytest.raises(ValueError):
        M.energy_distance(rng.normal(size=(5, 2)), rng.normal(size=(5, 2)), estimator="W")


def test_sliced_w1_truncate_reproduces_experiments() -> None:
    """E1 compares 10000 generated points with 96000 reference points."""
    rng = np.random.default_rng(1)
    x, y = rng.normal(size=(10000, 3)), rng.normal(0.05, 1.0, size=(96000, 3))
    for seed in (0, 3):
        old = _old_sliced_w1(x, y, seed=seed)
        assert M.sliced_w1(x, y, seed=seed, match="truncate", n_sub=20000) == old
    # the default (quantile) estimator uses every point: different number, same order of magnitude
    q = M.sliced_w1(x, y, seed=0)
    assert q != _old_sliced_w1(x, y, seed=0) and q == pytest.approx(_old_sliced_w1(x, y, seed=0), rel=0.5)


# ---------------------------------------------------------------------------------------------
# Flow matching
# ---------------------------------------------------------------------------------------------
def _proj(z: torch.Tensor) -> torch.Tensor:
    return z - z.mean(1, keepdim=True)


@pytest.mark.parametrize("variant", ["plain", "noise_fn", "extra"])
def test_fm_loss_reproduces_experiments(variant: str) -> None:
    torch.manual_seed(0)
    field = _Field(6)
    x1, c = torch.randn(64, 6), torch.rand(64)
    kw: dict = {}
    if variant == "noise_fn":
        kw["noise_fn"] = lambda shape: _proj(torch.randn(shape))
    if variant == "extra":
        kw["extra"] = lambda m, xt, t, c, v, x1: 0.1 * (xt + (1 - t)[:, None] * v).pow(2).mean()
    torch.manual_seed(5)
    old = _old_fm_loss(field, x1, c, **kw)
    torch.manual_seed(5)
    new = fm_loss(field, x1, c, **kw)
    assert torch.equal(old, new)


@pytest.mark.parametrize(("steps", "project"), [(50, None), (50, _proj), (8, None)])
def test_heun_sample_reproduces_experiments(steps: int, project) -> None:
    """50 steps (sampling of E1–E2, V3 projected) and 8 steps (differentiable loop of the fine-tunings)."""
    torch.manual_seed(0)
    field = _Field(4)
    z, c = torch.randn(32, 4), torch.rand(32)
    with torch.no_grad():
        old = _old_heun(field, z, c, steps, project)
        z0 = project(z) if project is not None else z
        new = heun_sample(field, z0, c, steps=steps, project=project)
    assert torch.equal(old, new)


def test_common_reexports_package_tools() -> None:
    """``experiments/common.py`` uses the package implementations."""
    sys.path.insert(0, str(EXPERIMENTS))
    try:
        import common
        import mhd2d
    finally:
        sys.path.remove(str(EXPERIMENTS))
    from milady.sim.mhd2d import MHD2D

    assert common.Fourier is FourierEmbedding and common.exp_tilt is exp_tilt
    assert common.systematic_resample is systematic_resample and mhd2d.MHD2D is MHD2D
    rng = np.random.default_rng(2)
    x, y = rng.normal(size=(800, 3)), rng.normal(size=(900, 3))
    assert common.energy_distance(x, y, n=500, seed=1) == _old_energy_distance(x, y, n=500, seed=1)
    assert common.sliced_w1(x, y, seed=1) == _old_sliced_w1(x, y, seed=1)


# ---------------------------------------------------------------------------------------------
# Tilting and solvers
# ---------------------------------------------------------------------------------------------
def test_exp_tilt_imposes_the_moments() -> None:
    rng = np.random.default_rng(4)
    g = rng.normal(0.3, 1.0, size=(4000, 2))
    w, _lam, info = exp_tilt(g)
    assert np.allclose(w @ g, 0.0, atol=1e-8) and info["residual"] < 1e-8 and 0 < info["ess_frac"] < 1
    idx = systematic_resample(w, 4000, seed=0)
    assert idx.min() >= 0 and idx.max() < 4000 and abs(g[idx].mean(0)).max() < 0.05


def test_induction3d_agrees_with_mhd3d_kinematic() -> None:
    """The NumPy reference of E3 and the torch solver agree on λ within the fit error (16³, t = 60)."""
    from milady.sim.induction3d import growth_rate

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from test_mhd3d import _abc_growth
    finally:
        sys.path.pop(0)
    for rm in (6.0, 12.0):
        lam, _, sim = growth_rate(rm, n=16, t_total=60.0)
        ref = _abc_growth(rm)
        assert np.sign(lam) == np.sign(ref) and abs(lam - ref) < 0.01, (rm, lam, ref)
        assert sim.divergence_rel() < 1e-12
