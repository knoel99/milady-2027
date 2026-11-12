"""Tests of the constraint mechanisms and model families of ``milady.train.constraints``.

One test ``test_<name>`` per entry of ``REGISTRY`` (counted by the race objective C7), each checking
the property that defines the mechanism, on the E4 system (16³ solver, cube truncation) where a
solver is needed.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
import torch

from milady.eval import metrics as M
from milady.sim.mhd3d import MHD3D, MHD3DConfig
from milady.train import constraints as C
from milady.train import diffusion
from milady.train.data import FourierPotentialSpace, half_cube_modes
from milady.train.flow import fm_loss

N, KCUT, NU, ETA, KF = 16, 5, 0.05, 0.05, 2


@pytest.fixture(autouse=True)
def _threads() -> None:
    torch.set_num_threads(2)


def _solver(n_traj: int = 2, dtype: str = "float64", t: float = 3.0) -> MHD3D:
    cfg = MHD3DConfig(n=N, mode="dynamic", nu=NU, eta=ETA, forcing="abc", kf=KF, u0="laminar", u_noise=0.3,
                      b0_amp=0.5, n_traj=n_traj, seed=3, dtype=dtype)
    sim = MHD3D(cfg)
    sim.advance_to(t, dt=0.02)
    return sim


def _forcing_hat(space, sim: MHD3D) -> torch.Tensor:
    """Coefficients of the forcing of amplitude 1 at the modes of ``space``."""
    f = (sim.f_phys / sim.forcing_amp).permute(1, 2, 3, 0).cpu().numpy()
    return space.vector_modes(f) if hasattr(space, "vector_modes") else space.base.vector_modes(f)


def _hat(space, sim: MHD3D) -> torch.Tensor:
    return space.field_hat(space.encode(sim.fields(np.float64)).double())


def test_registry_names_have_a_test() -> None:
    for name, (where, what) in C.REGISTRY.items():
        assert where in ("design", "loss", "sampling", "model") and what
        assert f"test_{name}" in globals(), name


def test_galerkin_potentials() -> None:
    """Cube truncation = the solver's modes: zero divergence and the solver's own budgets."""
    assert len(half_cube_modes(KCUT)) == ((2 * KCUT + 1) ** 3 - 1) // 2
    space = FourierPotentialSpace(KCUT, truncation="cube")
    assert space.config()["truncation"] == "cube" and "truncation" not in FourierPotentialSpace(3).config()
    sim = _solver()
    fields = sim.fields(np.float64)
    x = space.encode(fields)
    dec = space.decode(x.double(), N)
    for name in ("velocity", "magnetic_field"):  # every mode kept: the snapshot is reproduced
        assert np.abs(dec[name].numpy() - fields[name]).max() < 1e-6
        assert M.divergence_relative(dec[name]) < 1e-12
    d = sim.diagnostics()
    terms = C.budget_terms_hat(space, space.field_hat(x.double()), NU, ETA, forcing_hat=_forcing_hat(space, sim),
                               amp=sim.forcing_amp, production=True, grid=N)
    for key in ("kinetic_energy", "magnetic_energy", "kinetic_dissipation", "magnetic_dissipation", "injection",
                "magnetic_helicity", "cross_helicity", "magnetic_production"):
        assert np.allclose(terms[key].numpy(), d[key], rtol=2e-5, atol=1e-8), key
    # the potentials' own budget (pre-race code) agrees with the generic one
    ref = space.budget_terms(x.double(), torch.tensor(NU), torch.tensor(ETA))
    assert torch.allclose(ref["kinetic_dissipation"], terms["kinetic_dissipation"], rtol=1e-9)
    assert torch.allclose(ref["magnetic_energy"], terms["magnetic_energy"], rtol=1e-9)


def test_components() -> None:
    """Free components: exact round trip on solenoidal data, and nothing forces k·f̂ = 0."""
    space = C.FourierComponentSpace(KCUT, truncation="cube")
    assert space.n_channels == 12 and space.n_modes == 665
    sim = _solver()
    fields = sim.fields(np.float64)
    x = space.encode(fields)
    dec = space.decode(x.double(), N)
    assert np.abs(dec["magnetic_field"].numpy() - fields["magnetic_field"]).max() < 1e-6
    assert float(space.divergence_fraction(x.double()).max()) < 1e-12
    z = torch.randn(4, space.n_modes, space.n_channels, generator=torch.Generator().manual_seed(0))
    frac = space.divergence_fraction(z)
    assert 0.2 < float(frac.mean()) < 0.5        # isotropic noise: one third of the gradient energy
    b = space.decode(z.double(), N)["magnetic_field"]
    assert abs(M.divergence_relative(b) ** 2 - float(frac[:, 1].mean())) < 0.05
    assert torch.allclose(space.from_hat(space.field_hat(z)), z)
    space.fit(x)
    assert torch.allclose(space.denormalize(space.normalize(x)), x, atol=1e-6)


def test_leray_projection() -> None:
    """Final projection: solenoidal output, idempotent, and it commutes with the normalization."""
    space = C.FourierComponentSpace(KCUT, truncation="cube")
    g = torch.Generator().manual_seed(1)
    z = torch.randn(3, space.n_modes, space.n_channels, generator=g).double()
    p = space.project(z)
    assert float(space.divergence_fraction(p).max()) < 1e-24
    assert torch.allclose(space.project(p), p, atol=1e-12)
    space.fit(space.encode(_solver(n_traj=4).fields(np.float64)))
    left = space.normalize(space.project(space.denormalize(z.float())))
    assert torch.allclose(left, space.project(z.float()), atol=2e-4)


def test_projected_flow() -> None:
    """Projected noise and projected stages: the samples are solenoidal whatever the field."""
    space = C.FourierComponentSpace(3)

    def field(x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return torch.tanh(x.roll(1, dims=2)) + 0.3      # mixes the components: not solenoidal

    z0 = torch.randn(5, space.n_modes, space.n_channels, generator=torch.Generator().manual_seed(2))
    free = C.heun_sample(field, z0, torch.zeros(5, 1), steps=8)
    proj = C.projected_flow_sample(field, space, z0, torch.zeros(5, 1), steps=8)
    assert float(space.divergence_fraction(free).mean()) > 0.05
    assert float(space.divergence_fraction(proj).max()) < 1e-10


def test_divergence_penalty() -> None:
    """Zero on solenoidal predictions, positive otherwise, differentiable through fm_loss."""
    space = C.FourierComponentSpace(3)
    extra = C.divergence_penalty(space, weight=10.0)
    g = torch.Generator().manual_seed(3)
    x1 = space.project(torch.randn(6, space.n_modes, space.n_channels, generator=g))
    t = torch.rand(6, generator=g)
    xt = x1.clone()
    zero_v = torch.zeros_like(x1)                       # x̂1 = x_t = solenoidal x1
    assert float(extra(None, xt, t, None, zero_v, x1)) < 1e-10
    bad_v = torch.randn(x1.shape, generator=g)
    assert float(extra(None, xt, t, None, bad_v, x1)) > 0.1
    net = torch.nn.Linear(space.n_channels, space.n_channels)
    loss = fm_loss(lambda x, tt, c: net(x), x1, torch.zeros(6, 1), extra=extra)
    loss.backward()
    assert net.weight.grad is not None and float(net.weight.grad.abs().sum()) > 0


def test_stationarity_identities() -> None:
    """Each residual is the time derivative of its invariant along the solver's trajectories."""
    space = FourierPotentialSpace(KCUT, truncation="cube")
    sim = _solver(n_traj=2, t=3.0)
    fh_f = _forcing_hat(space, sim)

    def state() -> dict[str, torch.Tensor]:
        return C.budget_terms_hat(space, _hat(space, sim), NU, ETA, forcing_hat=fh_f, amp=sim.forcing_amp)

    h = 1e-3
    before = state()
    sim.advance_to(3.0 + h, dt=h)
    mid = state()
    sim.advance_to(3.0 + 2 * h, dt=h)
    after = state()
    res = C.stationarity_residuals(mid, NU, ETA)

    def ddt(key: str) -> torch.Tensor:
        return (after[key] - before[key]) / (2 * h)

    energy = ddt("kinetic_energy") + ddt("magnetic_energy")
    assert torch.allclose(res["energy"][0], energy, rtol=1e-3, atol=1e-7)
    assert torch.allclose(-2 * ETA * res["magnetic_helicity"][0], ddt("magnetic_helicity"), rtol=1e-3, atol=1e-7)
    assert torch.allclose(res["cross_helicity"][0], ddt("cross_helicity"), rtol=1e-3, atol=1e-7)
    for r, s in res.values():
        assert bool((s > 0).all()) and r.shape == s.shape == (2,)
    # unbiased estimator of the squared mean: E[half-batch product] = μ², whereas mean² adds σ²/n
    g = torch.Generator().manual_seed(4)
    r = 0.3 + torch.randn(4000, 8, generator=g)
    est = torch.stack([C.half_batch_product(row, torch.ones(8), 1) for row in r]).mean()
    naive = (r.mean(1) ** 2).mean()
    assert abs(float(est) - 0.09) < 0.02 and float(naive) > 0.09 + 0.08
    with pytest.raises(ValueError):
        C.half_batch_product(torch.zeros(9), torch.ones(9), 3)


def test_balance_rescaling() -> None:
    """After the rescaling each sample satisfies the energy balance; the forced modes are untouched."""
    space = FourierPotentialSpace(KCUT, truncation="cube")
    sim = _solver(n_traj=3)
    fh, fh_f = _hat(space, sim), _forcing_hat(space, sim)
    before = C.budget_terms_hat(space, fh, NU, ETA, forcing_hat=fh_f, amp=sim.forcing_amp)
    out, s = C.balance_rescaling(space, fh, NU, ETA, fh_f, amp=sim.forcing_amp)
    after = C.budget_terms_hat(space, out, NU, ETA, forcing_hat=fh_f, amp=sim.forcing_amp)
    res = after["injection"] - after["kinetic_dissipation"] - after["magnetic_dissipation"]
    assert bool((s > 0).all())
    assert float((res / after["injection"]).abs().max()) < 1e-10
    assert torch.allclose(after["injection"], before["injection"], rtol=1e-12)
    assert float((before["injection"] - before["kinetic_dissipation"] - before["magnetic_dissipation"]).abs().min()) > 1e-6


def test_balance_tilting() -> None:
    """The weights bring the weighted means of the residuals to zero; λ reweights a second sample."""
    rng = np.random.default_rng(5)
    g = rng.normal(size=(4000, 2)) + np.array([0.3, -0.2])
    w, lam, info = C.balance_tilting(g, reg=0.0)
    assert np.abs(w @ g).max() < 1e-6 and abs(w.sum() - 1) < 1e-12
    assert 0.5 < info["ess_frac"] < 1.0
    g2 = rng.normal(size=(4000, 2)) + np.array([0.3, -0.2])
    z = g2 @ lam
    w2 = np.exp(z - z.max())
    w2 /= w2.sum()
    assert np.abs(w2 @ g2).max() < 0.08


def test_diffusion() -> None:
    """With the exact field of a Gaussian law, both samplers return that law; the loss trains."""
    m, s = 1.5, 0.5

    def oracle(x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        cos, sin = torch.cos(0.5 * math.pi * t)[:, None], torch.sin(0.5 * math.pi * t)[:, None]
        gain = cos * sin * (1 - s * s) / (cos**2 * s * s + sin**2)
        return -sin * m + gain * (x - cos * m)           # E[v | x_s] for x1 ~ N(m, s²)

    g = torch.Generator().manual_seed(6)
    z = torch.randn(20000, 1, generator=g)
    for stochastic in (False, True):
        x = diffusion.diffusion_sample(oracle, z, torch.zeros(len(z), 1), steps=200, stochastic=stochastic,
                                       generator=g)
        assert abs(float(x.mean()) - m) < 0.02 and abs(float(x.std()) - s) < 0.02, stochastic
    net = torch.nn.Linear(4, 4)
    x1 = torch.randn(32, 4, generator=g)
    loss = diffusion.diffusion_loss(lambda x, t, c: net(x), x1, torch.zeros(32, 1), generator=g)
    loss.backward()
    assert math.isfinite(loss.item()) and net.weight.grad is not None
