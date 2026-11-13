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


def test_modewise_skip() -> None:
    """Zero at initialization; affine in x; lets a bottlenecked network reach the linear optimum."""
    M, Cc = 12, 4
    g = torch.Generator().manual_seed(7)

    def bottleneck() -> torch.nn.Module:
        class Net(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.f = torch.nn.Sequential(torch.nn.Linear(M * Cc + 1, 3), torch.nn.SiLU(), torch.nn.Linear(3, M * Cc))

            def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
                return self.f(torch.cat([x.flatten(1), t[:, None]], dim=1)).view_as(x)

        return Net()

    torch.manual_seed(0)
    base = bottleneck()
    skip = C.ModewiseAffineSkip(base, M, Cc, n_cond=1)
    x, t, c = torch.randn(5, M, Cc, generator=g), torch.rand(5, generator=g), torch.rand(5, 1, generator=g)
    assert torch.allclose(skip(x, t, c), base(x, t, c))                       # zero-initialized term
    torch.nn.init.normal_(skip.gain.weight, std=0.1)
    a1, a2 = skip.affine(x, t, c), skip.affine(2 * x, t, c)
    off = skip.affine(torch.zeros_like(x), t, c)
    assert torch.allclose(a2 - off, 2 * (a1 - off), atol=1e-5)                # affine in x
    # Gaussian data with mode-dependent variances: the optimum is linear in x, out of reach of width 3
    std = torch.linspace(0.3, 2.0, M)[None, :, None]
    losses = {}
    for name in ("base", "skip"):
        torch.manual_seed(1)
        net = bottleneck() if name == "base" else C.ModewiseAffineSkip(bottleneck(), M, Cc, n_cond=1)
        opt = torch.optim.Adam(net.parameters(), lr=1e-2)
        gen = torch.Generator().manual_seed(2)
        for _ in range(400):
            x1 = std * torch.randn(256, M, Cc, generator=gen)
            loss = fm_loss(net, x1, torch.zeros(256, 1), generator=gen)
            opt.zero_grad()
            loss.backward()
            opt.step()
        losses[name] = loss.item()
    assert losses["skip"] < losses["base"] - 0.1, losses


def test_gaussian_modes() -> None:
    """Moments recovered at the training conditions, interpolated in between, symmetric under the sign."""
    M, Cc, n = 6, 4, 20000
    g = torch.Generator().manual_seed(8)
    a = torch.randn(2, M, Cc, Cc, generator=g) * 0.5
    mean = torch.randn(2, M, Cc, generator=g)
    xs, cs = [], []
    for j, cv in enumerate((0.2, 0.8)):
        xi = torch.randn(n, M, Cc, generator=g)
        xs.append(mean[j] + torch.einsum("mij,nmj->nmi", a[j], xi))
        cs.append(torch.full((n,), cv))
    x, c = torch.cat(xs), torch.cat(cs)
    model = C.ModewiseGaussian().fit(x, c)
    cov_true = torch.einsum("kmij,kmlj->kmil", a, a).double()
    m0, c0 = model.moments(0.2)
    assert torch.allclose(m0, mean[0].double(), atol=0.03) and torch.allclose(c0, cov_true[0], atol=0.05)
    mm, cm = model.moments(0.5)
    assert torch.allclose(mm, 0.5 * (mean[0] + mean[1]).double(), atol=0.03)
    assert torch.allclose(cm, 0.5 * (cov_true[0] + cov_true[1]), atol=0.05)
    assert torch.allclose(model.moments(0.0)[0], m0) and torch.allclose(model.moments(1.5)[0], model.moments(0.8)[0])
    s = model.sample(0.5, 20000, generator=g)
    assert s.dtype == torch.float32 and s.shape == (20000, M, Cc)
    d = s.double() - s.double().mean(0)
    assert torch.allclose(torch.einsum("nmi,nmj->mij", d, d) / len(s), cm, atol=0.08)
    sign = torch.tensor([1.0, 1.0, -1.0, -1.0])
    sym = C.ModewiseGaussian(sign=sign).fit(x, c)
    ms, cvs = sym.moments(0.5)
    assert float(ms[:, 2:].abs().max()) == 0.0 and float(cvs[:, :2, 2:].abs().max()) == 0.0


def test_gaussian_full() -> None:
    """The full-covariance Gaussian keeps the covariance between modes, which the mode-wise law drops."""
    M, Cc, n = 5, 4, 6000
    g = torch.Generator().manual_seed(9)
    a = torch.randn(2, M * Cc, M * Cc, generator=g) * 0.3              # mixes all modes: inter-mode covariance
    mean = torch.randn(2, M * Cc, generator=g)
    xs, cs = [], []
    for j, cv in enumerate((0.2, 0.8)):
        xs.append((mean[j] + torch.randn(n, M * Cc, generator=g) @ a[j].T).reshape(n, M, Cc))
        cs.append(torch.full((n,), cv))
    x, c = torch.cat(xs), torch.cat(cs)
    cov_true = torch.einsum("kij,klj->kil", a, a)
    model = C.FullGaussian().fit(x, c)
    cov = lambda z: torch.cov(z.reshape(len(z), -1).T)
    s0 = model.sample(0.2, 30000, generator=g)
    assert s0.dtype == torch.float32 and s0.shape == (30000, M, Cc)
    mean_data = [z.reshape(len(z), -1).mean(0) for z in xs]
    assert torch.allclose(s0.reshape(len(s0), -1).mean(0), mean_data[0], atol=0.05) and torch.allclose(mean_data[0], mean[0], atol=0.1)
    cov_data = [cov(xs[0]), cov(xs[1])]                                 # the law is the Gaussian of the SAMPLE moments
    assert torch.allclose(cov(s0), cov_data[0], atol=0.1) and torch.allclose(cov_data[0], cov_true[0], atol=0.3)
    sm = model.sample(0.5, 30000, generator=g)                          # interpolated: convex combination of the covariances
    assert torch.allclose(sm.reshape(len(sm), -1).mean(0), 0.5 * (mean_data[0] + mean_data[1]), atol=0.05)
    assert torch.allclose(cov(sm), 0.5 * (cov_data[0] + cov_data[1]), atol=0.1)
    assert torch.equal(model.sample(0.0, 4, generator=torch.Generator().manual_seed(1)),
                       model.sample(0.2, 4, generator=torch.Generator().manual_seed(1)))          # no extrapolation
    # the covariance between two different modes is kept; the mode-wise law has none
    inter = cov_true[0][:Cc, Cc:2 * Cc]
    assert float(inter.abs().max()) > 0.2
    assert torch.allclose(cov(s0)[:Cc, Cc:2 * Cc], inter, atol=0.2)
    sw = C.ModewiseGaussian().fit(x, c).sample(0.2, 30000, generator=g)
    assert float(cov(sw)[:Cc, Cc:2 * Cc].abs().max()) < 0.05
    # symmetric under the sign: odd channels have zero mean and no covariance with the even ones, in every pair of modes
    sign = torch.tensor([1.0, 1.0, -1.0, -1.0])
    sym = C.FullGaussian(sign=sign).fit(x, c)
    ss = sym.sample(0.2, 30000, generator=g)
    odd = sign.repeat(M) < 0
    cs_ = cov(ss)
    assert float(ss.reshape(len(ss), -1).mean(0)[odd].abs().max()) < 0.05
    assert float(cs_[~odd][:, odd].abs().max()) < 0.06
    assert float(cs_[odd][:, odd].abs().max()) > 0.2                    # the odd–odd inter-mode block is kept


def test_gaussian_anchor() -> None:
    """With a zero network, the anchored flow transports N(0, I) onto the fitted Gaussian law."""
    M, Cc, n = 5, 4, 30000
    g = torch.Generator().manual_seed(9)
    a = torch.randn(2, M, Cc, Cc, generator=g) * 0.6
    mean = torch.randn(2, M, Cc, generator=g)
    xs, cs = [], []
    for j, cv in enumerate((0.1, 0.9)):
        xs.append(mean[j] + torch.einsum("mij,nmj->nmi", a[j], torch.randn(n, M, Cc, generator=g)))
        cs.append(torch.full((n,), cv))
    gauss = C.ModewiseGaussian().fit(torch.cat(xs), torch.cat(cs))

    def zero(x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return torch.zeros_like(x)

    field = C.GaussianAnchoredField(zero, gauss)
    for cv in (0.1, 0.5):
        mu, cov = gauss.moments(cv)
        z = torch.randn(n, M, Cc, generator=g)
        with torch.no_grad():
            x = C.heun_sample(field, z, torch.full((n, 1), cv), steps=100)
        d = x.double() - x.double().mean(0)
        got = torch.einsum("nmi,nmj->mij", d, d) / n
        assert torch.allclose(x.double().mean(0), mu, atol=0.05), cv
        assert torch.allclose(got, cov, atol=0.08), cv
    # the closed form is the conditional expectation E[x1 − x0 | x_t]: its loss is below that of a zero field
    x1 = xs[0][:4096]
    base_loss = fm_loss(zero, x1, torch.full((4096, 1), 0.1), generator=torch.Generator().manual_seed(1))
    anch_loss = fm_loss(field, x1, torch.full((4096, 1), 0.1), generator=torch.Generator().manual_seed(1))
    assert float(anch_loss) < float(base_loss) - 0.1
    # mixed conditions in one batch are routed to their own moments
    xb, tb = torch.randn(6, M, Cc, generator=g), torch.rand(6, generator=g)
    cb = torch.tensor([[0.1], [0.9], [0.1], [0.5], [0.9], [0.5]])
    whole = field.gaussian_field(xb, tb, cb)
    for i in range(6):
        assert torch.allclose(whole[i], field.gaussian_field(xb[i:i + 1], tb[i:i + 1], cb[i:i + 1])[0], atol=1e-5)


def test_gaussian_full_anchor() -> None:
    """With a zero network, the flow anchored on the full-covariance Gaussian law transports N(0, I) onto it."""
    M, Cc, n = 5, 4, 20000
    D = M * Cc
    g = torch.Generator().manual_seed(21)
    xs, cs = [], []
    for cv in (0.1, 0.9):                                   # a full D × D mixing: covariance between different modes
        a = torch.randn(D, D, generator=g) * 0.4
        xs.append((torch.randn(D, generator=g) + torch.randn(n, D, generator=g) @ a).reshape(n, M, Cc))
        cs.append(torch.full((n,), cv))
    gauss = C.FullGaussian().fit(torch.cat(xs), torch.cat(cs))

    def zero(x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return torch.zeros_like(x)

    field = C.FullGaussianAnchoredField(zero, gauss)
    for cv, w in ((0.1, 0.0), (0.5, 0.5)):                  # a training condition and an interpolated one
        mu = (1 - w) * gauss.mean[0] + w * gauss.mean[1]
        cov = (1 - w) * gauss.factor[0].T @ gauss.factor[0] + w * gauss.factor[1].T @ gauss.factor[1]
        mu_m, cov_m = gauss.moments(cv)                      # the moments returned by the law itself
        assert torch.allclose(mu_m, mu.double(), atol=1e-6) and torch.allclose(cov_m, cov.double(), atol=1e-5)
        z = torch.randn(n, M, Cc, generator=g)
        with torch.no_grad():
            x = C.heun_sample(field, z, torch.full((n, 1), cv), steps=100).reshape(n, D).double()
        d = x - x.mean(0)
        got = d.T @ d / n
        assert torch.allclose(x.mean(0), mu.double(), atol=0.06), cv
        assert torch.allclose(got, cov.double(), atol=0.12), cv
        off = ~torch.block_diag(*[torch.ones(Cc, Cc)] * M).bool()          # entries between different modes
        assert float(cov[off].abs().mean()) > 0.2 and float((got - cov.double())[off].abs().mean()) < 0.03, cv
    # the closed form is the conditional expectation E[x1 − x0 | x_t]: its loss is below that of a zero field
    x1 = xs[0][:4096]
    base_loss = fm_loss(zero, x1, torch.full((4096, 1), 0.1), generator=torch.Generator().manual_seed(1))
    anch_loss = fm_loss(field, x1, torch.full((4096, 1), 0.1), generator=torch.Generator().manual_seed(1))
    assert float(anch_loss) < float(base_loss) - 0.1
    # mixed conditions in one batch are routed to their own moments
    xb, tb = torch.randn(6, M, Cc, generator=g), torch.rand(6, generator=g)
    cb = torch.tensor([[0.1], [0.9], [0.1], [0.5], [0.9], [0.5]])
    whole = field.gaussian_field(xb, tb, cb)
    for i in range(6):
        assert torch.allclose(whole[i], field.gaussian_field(xb[i:i + 1], tb[i:i + 1], cb[i:i + 1])[0], atol=1e-4)
    # a deep copy (the moving average of a training) has its own network and shares the Gaussian data
    import copy

    lin = torch.nn.Linear(D, D)

    class Net(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.lin = lin

        def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
            return self.lin(x.flatten(1)).view_as(x)

    trained = C.FullGaussianAnchoredField(Net(), gauss)
    twin = copy.deepcopy(trained)
    assert twin.base.lin.weight is not trained.base.lin.weight and torch.equal(twin.base.lin.weight, trained.base.lin.weight)
    assert twin.factor[0] is trained.factor[0] and twin._cache is trained._cache
    assert [n for n, _ in twin.named_parameters()] == [n for n, _ in trained.named_parameters()]
    assert torch.allclose(twin(xb, tb, cb), trained(xb, tb, cb))
    # a sample covariance of fewer snapshots than dimensions is singular: the flow stays finite and puts no
    # variance outside the span of the data
    few = (torch.randn(8, D, generator=g) * 1.5).reshape(8, M, Cc)
    sing = C.FullGaussianAnchoredField(zero, C.FullGaussian().fit(few, torch.zeros(8)))
    with torch.no_grad():
        xs_ = C.heun_sample(sing, torch.randn(4000, M, Cc, generator=g), torch.zeros(4000, 1), steps=100).reshape(4000, D).double()
    assert torch.isfinite(xs_).all()
    a = (few.reshape(8, D) - few.reshape(8, D).mean(0)).double()
    q, _ = torch.linalg.qr(a.T)                             # orthonormal basis of the span (rank 7)
    dd = xs_ - xs_.mean(0)
    inside = (dd @ q[:, :7]).pow(2).sum() / dd.pow(2).sum()
    assert float(inside) > 0.995
    assert torch.allclose(dd.T @ dd / 4000, a.T @ a / 8, atol=0.35)




def test_moment_recolouring() -> None:
    """The linear map gives the samples the target mean and covariance and keeps their non-Gaussian structure."""
    g = torch.Generator().manual_seed(5)
    n, M, d = 40000, 3, 4
    mix = torch.randn(M, d, d, generator=g) * 0.7
    z = torch.randn(n, M, d, generator=g)
    x = torch.einsum("mij,nmj->nmi", mix, z + 0.6 * (z**2 - 1)) + 0.3                       # skewed, correlated
    mu_s = x.double().mean(0)
    dx = x.double() - mu_s
    cov_s = torch.einsum("nmi,nmj->mij", dx, dx) / n
    b = torch.randn(M, d, d, generator=g).double()
    mu_t, cov_t = torch.randn(M, d, generator=g).double(), b @ b.mT + 0.1 * torch.eye(d, dtype=torch.float64)
    y = C.moment_recolouring(x, mu_s, cov_s, mu_t, cov_t).double()                           # one map per mode
    dy = y - y.mean(0)
    assert C.moment_recolouring(x[:8], mu_s, cov_s, mu_t, cov_t).dtype == x.dtype          # returned in the dtype of x
    assert torch.allclose(y.mean(0), mu_t, atol=1e-4)
    assert torch.allclose(torch.einsum("nmi,nmj->mij", dy, dy) / n, cov_t, atol=1e-3)
    # identity when the moments already agree; symmetric positive map
    assert torch.allclose(C.moment_recolouring(x, mu_s, cov_s, mu_s, cov_s).double(), x.double(), atol=1e-4)
    # the same map on the flattened latent (covariance between modes included)
    xf = x.reshape(n, M * d).double()
    mf = xf.mean(0)
    cf = (xf - mf).T @ (xf - mf) / n
    bf = torch.randn(M * d, M * d, generator=g).double()
    tf = bf @ bf.T / (M * d) + 0.05 * torch.eye(M * d, dtype=torch.float64)
    yf = C.moment_recolouring(xf, mf, cf, torch.zeros(M * d, dtype=torch.float64), tf)
    assert torch.allclose(yf.mean(0), torch.zeros(M * d, dtype=torch.float64), atol=1e-4)
    assert torch.allclose((yf - yf.mean(0)).T @ (yf - yf.mean(0)) / n, tf, atol=1e-3)
    # what is not Gaussian is kept: a pure rescaling of the covariance leaves the standardised skewness unchanged,
    # and a Gaussian sample stays Gaussian (zero skewness)
    def skew(v: torch.Tensor) -> torch.Tensor:
        c = v - v.mean(0)
        return (c**3).mean(0) / (c**2).mean(0) ** 1.5

    ys = C.moment_recolouring(x, mu_s, cov_s, mu_s, 4.0 * cov_s).double()
    assert torch.allclose(skew(ys), skew(x.double()), atol=1e-6) and float(skew(x.double()).abs().max()) > 0.5
    gauss = torch.einsum("mij,nmj->nmi", mix, z)
    cg = torch.einsum("nmi,nmj->mij", gauss.double() - gauss.double().mean(0), gauss.double() - gauss.double().mean(0)) / n
    assert float(skew(C.moment_recolouring(gauss, gauss.double().mean(0), cg, mu_t, cov_t).double()).abs().max()) < 0.05
    # a singular source covariance does not blow up
    flat = torch.cat([x[:, :1, :2], torch.zeros(n, 1, 2)], dim=-1)
    cz = torch.einsum("nmi,nmj->mij", flat.double() - flat.double().mean(0), flat.double() - flat.double().mean(0)) / n
    assert torch.isfinite(C.moment_recolouring(flat, flat.double().mean(0), cz, mu_t[:1], cov_t[:1])).all()


def test_gaussian_full_anchor_learns_a_non_gaussian_law() -> None:
    """Positive control of the anchored model: on skewed data the network, zero at the start, lowers the loss and gives
    the samples the skewness of the data (the untrained model is the Gaussian law: no skewness)."""
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(4)
    M, Cc, n = 3, 2, 8192
    D = M * Cc
    z = torch.randn(n, D, generator=g)
    mix = torch.randn(D, D, generator=g) * 0.5 + torch.eye(D)
    x = ((z + 0.7 * (z**2 - 1)) @ mix).reshape(n, M, Cc)
    c = torch.zeros(n)
    gauss = C.FullGaussian().fit(x, c)

    class Net(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.body = torch.nn.Sequential(torch.nn.Linear(D + 1, 128), torch.nn.SiLU(), torch.nn.Linear(128, 128), torch.nn.SiLU())
            self.out = torch.nn.Linear(128, D)
            torch.nn.init.zeros_(self.out.weight)
            torch.nn.init.zeros_(self.out.bias)

        def forward(self, xx: torch.Tensor, t: torch.Tensor, cc: torch.Tensor) -> torch.Tensor:
            return self.out(self.body(torch.cat([xx.flatten(1), t.view(-1, 1)], dim=1))).view_as(xx)

    field = C.FullGaussianAnchoredField(Net(), gauss)
    cond = torch.zeros(2048, 1)

    def fixed_loss() -> float:
        with torch.no_grad():
            return float(fm_loss(field, x[:2048], cond, generator=torch.Generator().manual_seed(7)))

    def skew(v: torch.Tensor) -> torch.Tensor:
        d = v.double() - v.double().mean(0)
        return (d**3).mean(0) / (d**2).mean(0) ** 1.5

    before = fixed_loss()
    with torch.no_grad():
        s0 = skew(C.heun_sample(field, torch.randn(4096, M, Cc, generator=g), torch.zeros(4096, 1), steps=40).reshape(-1, D))
    opt = torch.optim.Adam(field.parameters(), lr=2e-3)
    for _ in range(500):
        idx = torch.randint(0, n, (256,))
        loss = fm_loss(field, x[idx], torch.zeros(256, 1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    after = fixed_loss()
    with torch.no_grad():
        s1 = skew(C.heun_sample(field, torch.randn(4096, M, Cc, generator=g), torch.zeros(4096, 1), steps=40).reshape(-1, D))
    target = skew(x.reshape(n, D))
    big = target.abs() > 0.5                                  # coordinates where the data are clearly skewed
    assert int(big.sum()) >= 2
    assert after < before - 0.02, (before, after)
    assert float(s0[big].abs().max()) < 0.2                   # the untrained model is Gaussian
    assert bool((torch.sign(s1[big]) == torch.sign(target[big])).all()) and float((s1[big] / target[big]).min()) > 0.3, (s1, target)

