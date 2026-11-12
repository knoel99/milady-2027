"""Constraint mechanisms for the conditional generation of 3D MHD fields (u, B) on Fourier modes.

The mechanisms are grouped by where they act, in the words of the internship offer: **model
design**, **training losses** and **sampling procedures**. :data:`REGISTRY` lists them; each entry
has a test ``test_<name>`` in ``tests/test_constraints.py``.

Model design
    - :class:`milady.train.data.FourierPotentialSpace` with ``truncation="cube"``
      (``galerkin_potentials``): vector potentials on every mode of the solver's Galerkin
      truncation; zero divergence by construction and exact quadratic budgets;
    - :class:`FourierComponentSpace` (``components``): the unconstrained baseline, three complex
      components per mode and per field.
Training losses
    - :func:`divergence_penalty`: penalty on the divergence of the end-of-path prediction
      x̂₁ = x_t + (1 − t) v (Proposition 3 of ``docs/specs/theory-brief.md``: unbiased at the optimum);
    - :func:`stationarity_residuals` with :func:`half_batch_product`
      (``stationarity_identities``): law-level identities E[𝓛φ] = 0 of the stationary state, with
      the unbiased estimator of the squared mean: total energy, magnetic helicity
      (E[⟨j·B⟩] = 0, no parameter in it) and cross helicity.
Sampling procedures
    - :func:`leray_hat` / :meth:`FourierComponentSpace.project` (``leray_projection``): Leray
      projection of the final samples;
    - :func:`projected_flow_sample` (``projected_flow``): projected noise and projection of every
      stage of the integrator;
    - :func:`balance_rescaling`: per-sample rescaling of the small scales to the energy balance
      (the per-sample constraint that Corollary 6 shows to be inconsistent with the law);
    - :func:`balance_tilting`: exponential tilting of a sample cloud on the stationarity identities
      (I-projection, Proposition 7).
Model family
    - ``diffusion``: :mod:`milady.train.diffusion` (variance-preserving path, v-prediction,
      ancestral or deterministic sampler), on the same spaces and networks;
    - :class:`ModewiseAffineSkip` (``modewise_skip``): v = G(t, c) x + b(t, c) + network, with one
      C × C matrix per mode. A network narrower than the latent dimension cannot represent the linear
      part of the optimal field (for Gaussian data the field is linear in x); the explicit term can;
    - :class:`GaussianAnchoredField` (``gaussian_anchor``): v = v_Gauss(x, t, c) + network, where
      v_Gauss is the closed-form flow-matching field of the mode-wise Gaussian law; with the network
      at zero the model is the Gaussian baseline, and training only has to learn the departure from it;
    - :class:`ModewiseGaussian` (``gaussian_modes``): no network, the conditional Gaussian law with
      one mean and one covariance per Fourier mode, interpolated between the training conditions. It
      reproduces the mode-wise second-order statistics (spectra, helicities, mean budgets) and nothing
      else: the baseline that a generative model has to beat.

All field coefficients are "forward"-normalized (independent of the resolution) and given on the
half set of modes of the space: ``fh`` has shape ``(b, F, M, 3)`` (complex), ``F`` fields in the order
of ``space.fields``; spatial means follow from Parseval, each mode counting twice.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np
import torch
from torch import nn

from milady.train.data import FIELD_NAMES, TWO_PI, FourierPotentialSpace, _cross
from milady.train.flow import heun_sample

__all__ = [
    "REGISTRY",
    "FourierComponentSpace",
    "GaussianAnchoredField",
    "ModewiseAffineSkip",
    "ModewiseGaussian",
    "balance_rescaling",
    "balance_tilting",
    "budget_terms_hat",
    "divergence_fraction_hat",
    "divergence_penalty",
    "half_batch_product",
    "leray_hat",
    "projected_flow_sample",
    "stationarity_residuals",
]

#: Mechanisms and model families added during the race: name → (where it acts, what it is).
REGISTRY: dict[str, tuple[str, str]] = {
    "galerkin_potentials": ("design", "vector potentials on every mode of the solver's Galerkin truncation"),
    "components": ("design", "free Fourier components: the unconstrained baseline"),
    "divergence_penalty": ("loss", "penalty on the divergence of the end-of-path prediction"),
    "stationarity_identities": ("loss", "law-level energy, magnetic-helicity and cross-helicity identities"),
    "leray_projection": ("sampling", "Leray projection of the final samples"),
    "projected_flow": ("sampling", "projected noise and projection of every integration stage"),
    "balance_rescaling": ("sampling", "per-sample rescaling of the small scales to the energy balance"),
    "balance_tilting": ("sampling", "exponential tilting of the samples on the stationarity identities"),
    "diffusion": ("model", "variance-preserving diffusion, v-prediction, ancestral or deterministic sampler"),
    "modewise_skip": ("design", "explicit mode-wise affine term of the velocity field, around a network with a bottleneck"),
    "gaussian_modes": ("model", "conditional Gaussian law with one mean and covariance per Fourier mode: second-order baseline"),
    "gaussian_anchor": ("design", "velocity field = exact field of the mode-wise Gaussian law + network for the non-Gaussian part"),
}


# =============================================================================================
# Operators on field coefficients
# =============================================================================================
def leray_hat(fh: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    """Leray projection f̂ − k (k·f̂)/|k|² mode by mode; ``fh`` (..., M, 3), ``k`` (M, 3)."""
    kc = k.to(fh.real.dtype)
    k2 = (kc * kc).sum(-1)
    d = (fh * kc).sum(-1) / k2
    return fh - d[..., None] * kc


def divergence_fraction_hat(fh: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    """Σ|k·f̂|² / Σ|k|²|f̂|² per sample and field: the square of ‖∇·f‖ / ‖∇f‖ (differentiable)."""
    kc = k.to(fh.real.dtype)
    k2 = (kc * kc).sum(-1)
    num = ((fh * kc).sum(-1).abs() ** 2).sum(-1)
    den = (k2 * (fh.abs() ** 2).sum(-1)).sum(-1)
    return num / den.clamp_min(1e-30)


def _pair(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """⟨a·b⟩ (spatial mean) from the half-set coefficients (..., M, 3): 2 Re Σ â·b̂*."""
    return 2.0 * (a * b.conj()).real.sum(dim=(-2, -1))


def budget_terms_hat(
    space: Any,
    fh: torch.Tensor,
    nu: torch.Tensor | float,
    eta: torch.Tensor | float,
    *,
    forcing_hat: torch.Tensor | None = None,
    amp: torch.Tensor | float = 1.0,
    production: bool = False,
    grid: int | None = None,
) -> dict[str, torch.Tensor]:
    """Per-sample terms of the budgets from the field coefficients ``fh`` (b, F, M, 3), differentiable.

    ``space``: :class:`FourierPotentialSpace` or :class:`FourierComponentSpace` generating
    ``velocity`` and ``magnetic_field``. ``forcing_hat`` (M, 3): coefficients of the forcing of
    amplitude 1, multiplied by ``amp``. Returns the energies, ``enstrophy`` ⟨|ω|²⟩,
    ``mean_square_current`` ⟨|j|²⟩, the dissipations ν⟨|ω|²⟩ and η⟨|j|²⟩,
    ``injection`` ⟨f·u⟩, the helicities (``magnetic_helicity`` ⟨A·B⟩ in Coulomb gauge,
    ``current_helicity`` ⟨j·B⟩, ``cross_helicity`` ⟨u·B⟩), ``omega_j`` ⟨ω·j⟩ and ``forcing_b`` ⟨f·B⟩
    (cross-helicity budget), and with ``production`` the cubic term ⟨j·(u×B)⟩ on an alias-free grid.
    The curl is used as is: for a field that is not solenoidal, ω and j are still ∇×u and ∇×B.
    """
    k = space.k.to(fh.real.dtype)
    kc = k.to(fh.dtype)
    k2 = (k * k).sum(-1)
    uh = fh[:, space.fields.index("velocity")]
    bh = fh[:, space.fields.index("magnetic_field")]
    wh = 1j * _cross(kc, uh)
    jh = 1j * _cross(kc, bh)
    ah = jh / k2[:, None]
    out = {
        "kinetic_energy": 0.5 * _pair(uh, uh),
        "magnetic_energy": 0.5 * _pair(bh, bh),
        "kinetic_dissipation": nu * _pair(wh, wh),
        "magnetic_dissipation": eta * _pair(jh, jh),
        "enstrophy": _pair(wh, wh),
        "mean_square_current": _pair(jh, jh),
        "magnetic_helicity": _pair(ah, bh),
        "current_helicity": _pair(jh, bh),
        "cross_helicity": _pair(uh, bh),
        "omega_j": _pair(wh, jh),
    }
    if forcing_hat is not None:
        f = forcing_hat.to(fh.dtype)
        out["injection"] = amp * _pair(uh, f.expand_as(uh))
        out["forcing_b"] = amp * _pair(bh, f.expand_as(bh))
    if production:
        n = grid or space.default_grid()
        phys = space.to_grid(torch.stack([uh, bh, jh], dim=1), (n, n, n))
        out["magnetic_production"] = (phys[:, 2] * _cross(phys[:, 0], phys[:, 1])).sum(-1).mean(dim=(-3, -2, -1))
    return out


# =============================================================================================
# Model design: the unconstrained baseline
# =============================================================================================
class FourierComponentSpace(nn.Module):
    """Free representation: the three complex components of û and B̂ at every mode.

    Latent ``(b, M, 6 F)``: for each field, the real parts then the imaginary parts of the three
    components. Nothing forces k·f̂ = 0: this is the baseline against which the constraint mechanisms
    are compared. Same modes, grid conventions and normalization rule as
    :class:`milady.train.data.FourierPotentialSpace` (mean per coordinate, standard deviation per mode
    and per field, pooled over the six channels). Because the scaling is isotropic within a mode, the
    Leray projection commutes with the normalization: :meth:`project` applies to raw and to
    normalized latents alike (the mean of solenoidal data is solenoidal).
    """

    mean: torch.Tensor
    std: torch.Tensor
    sign: torch.Tensor

    def __init__(
        self,
        kmax: float,
        fields: Sequence[str] = FIELD_NAMES,
        lengths: Sequence[float] = (TWO_PI, TWO_PI, TWO_PI),
        symmetric_b: bool = False,
        truncation: str = "ball",
    ) -> None:
        super().__init__()
        self.base = FourierPotentialSpace(kmax, fields, lengths, symmetric_b, truncation)
        self.fields = self.base.fields
        self.lengths = self.base.lengths
        self.symmetric_b = self.base.symmetric_b
        M, C = self.base.n_modes, 6 * len(self.fields)
        self.register_buffer("mean", torch.zeros(M, C))
        self.register_buffer("std", torch.ones(M, C))
        sign = torch.ones(C)
        if self.symmetric_b and "magnetic_field" in self.fields:
            sign[self.field_slice("magnetic_field")] = -1.0
        self.register_buffer("sign", sign)

    # -- description -------------------------------------------------------------------------
    @property
    def k(self) -> torch.Tensor:
        return self.base.k

    @property
    def m(self) -> torch.Tensor:
        return self.base.m

    @property
    def shell(self) -> torch.Tensor:
        return self.base.shell

    @property
    def n_modes(self) -> int:
        return self.base.n_modes

    @property
    def n_channels(self) -> int:
        return 6 * len(self.fields)

    def field_slice(self, name: str) -> slice:
        i = self.fields.index(name)
        return slice(6 * i, 6 * i + 6)

    def default_grid(self) -> int:
        return self.base.default_grid()

    def to_grid(self, hat: torch.Tensor, shape: Sequence[int]) -> torch.Tensor:
        return self.base.to_grid(hat, shape)

    # -- coefficients ↔ latent ---------------------------------------------------------------
    def from_hat(self, fh: torch.Tensor) -> torch.Tensor:
        """Field coefficients ``(b, F, M, 3)`` → raw latent ``(b, M, 6 F)`` (float32)."""
        return self._pack(fh).to(torch.float32)

    def _pack(self, fh: torch.Tensor) -> torch.Tensor:
        x = torch.cat([fh.real, fh.imag], dim=-1)            # (b, F, M, 6)
        return x.movedim(1, 2).reshape(fh.shape[0], self.n_modes, -1)

    def field_hat(self, x: torch.Tensor) -> torch.Tensor:
        """Raw latent ``(b, M, 6 F)`` → field coefficients ``(b, F, M, 3)``."""
        xr = x.reshape(x.shape[0], self.n_modes, len(self.fields), 6).movedim(2, 1)
        return torch.complex(xr[..., :3], xr[..., 3:])

    def encode(self, fields: Mapping[str, Any]) -> torch.Tensor:
        """Fields ``{name: (b, nx, ny, nz, 3)}`` → raw latent ``(b, M, 6 F)``."""
        hats = [self.base.modes_from_grid(torch.as_tensor(fields[name], dtype=torch.float64, device=self.k.device))
                for name in self.fields]
        return self.from_hat(torch.stack(hats, dim=1))

    def decode(self, x: torch.Tensor, shape: Sequence[int] | int | None = None) -> dict[str, torch.Tensor]:
        """Raw latent → physical fields ``{name: (b, nx, ny, nz, 3)}`` (not solenoidal in general)."""
        n = shape if shape is not None else self.default_grid()
        grid = (n, n, n) if isinstance(n, int) else tuple(n)
        f = self.to_grid(self.field_hat(x), grid)
        return {name: f[:, i] for i, name in enumerate(self.fields)}

    # -- normalization -----------------------------------------------------------------------
    @torch.no_grad()
    def fit(self, x: torch.Tensor) -> None:
        """Mean per coordinate, standard deviation per mode and field, from raw latents ``(N, M, 6 F)``."""
        x64 = x.to(torch.float64)
        mean = x64.mean(0)
        if self.symmetric_b and "magnetic_field" in self.fields:
            mean[:, self.field_slice("magnetic_field")] = 0.0
        xc = x64 - mean
        std = torch.empty_like(mean)
        for name in self.fields:
            sl = self.field_slice(name)
            s = xc[:, :, sl].pow(2).mean(dim=(0, 2)).sqrt()
            std[:, sl] = torch.clamp(s, min=1e-6 * float(s.max()) + 1e-30)[:, None]
        self.mean.copy_(mean.to(self.mean.dtype))
        self.std.copy_(std.to(self.std.dtype))

    def normalize(self, x: torch.Tensor) -> torch.Tensor:
        return (x - self.mean) / self.std

    def denormalize(self, z: torch.Tensor) -> torch.Tensor:
        return z * self.std + self.mean

    # -- sampling procedures -----------------------------------------------------------------
    def project(self, x: torch.Tensor) -> torch.Tensor:
        """Leray projection of a latent ``(b, M, 6 F)``, raw or normalized (see the class docstring)."""
        return self._pack(leray_hat(self.field_hat(x), self.k))

    def divergence_fraction(self, x: torch.Tensor) -> torch.Tensor:
        """Σ|k·f̂|²/Σ|k|²|f̂|² of a raw latent, per sample and field ``(b, F)`` (differentiable)."""
        return divergence_fraction_hat(self.field_hat(x), self.k)


# =============================================================================================
# Training losses
# =============================================================================================
def divergence_penalty(space: FourierComponentSpace, weight: float = 10.0) -> Callable[..., torch.Tensor]:
    """Penalty for :func:`milady.train.flow.fm_loss` (argument ``extra``) on the divergence of x̂₁.

    x̂₁ = x_t + (1 − t) v is the end-of-path prediction; the penalty is ``weight`` times the mean
    over the batch and the fields of Σ|k·f̂|²/Σ|k|²|f̂|² of the denormalized x̂₁. The constraint is
    linear, so the penalty vanishes at the optimal field (Proposition 3) and does not bias it.
    """

    def extra(field: Any, xt: torch.Tensor, t: torch.Tensor, c: torch.Tensor, v: torch.Tensor,
              x1: torch.Tensor) -> torch.Tensor:
        x1hat = xt + (1.0 - t).view(-1, *([1] * (xt.dim() - 1))) * v.float()
        return weight * space.divergence_fraction(space.denormalize(x1hat)).mean()

    return extra


def stationarity_residuals(terms: Mapping[str, torch.Tensor], nu: torch.Tensor | float,
                           eta: torch.Tensor | float) -> dict[str, tuple[torch.Tensor, torch.Tensor]]:
    """Residuals of the law-level stationarity identities, with a positive scale for each.

    From the per-sample terms of :func:`budget_terms_hat`, for a statistically stationary forced MHD
    flow in a periodic box (the expectation of each residual is zero under the invariant law):

    - ``energy``: ⟨f·u⟩ − ν⟨|ω|²⟩ − η⟨|j|²⟩, scale ν⟨|ω|²⟩ + η⟨|j|²⟩ (from d(E_u + E_B)/dt);
    - ``magnetic_helicity``: ⟨j·B⟩, scale (⟨|j|²⟩⟨|B|²⟩)^½ (from d⟨A·B⟩/dt = −2η⟨j·B⟩; the identity
      holds whatever η and the forcing);
    - ``cross_helicity``: ⟨f·B⟩ − (ν + η)⟨ω·j⟩, scale (ν + η)(⟨|ω|²⟩⟨|j|²⟩)^½ (from d⟨u·B⟩/dt; odd in
      B, hence trivially satisfied by a law invariant under B → −B).

    Returns ``{name: (residual, scale)}``, both of shape ``(b,)``.
    """
    w2, j2 = terms["enstrophy"], terms["mean_square_current"]
    sinks = terms["kinetic_dissipation"] + terms["magnetic_dissipation"]
    out = {
        "energy": (terms["injection"] - sinks, sinks),
        "magnetic_helicity": (terms["current_helicity"], (j2 * 2.0 * terms["magnetic_energy"]).sqrt()),
    }
    if "forcing_b" in terms:
        out["cross_helicity"] = (terms["forcing_b"] - (nu + eta) * terms["omega_j"], (nu + eta) * (w2 * j2).sqrt())
    return out


def half_batch_product(residual: torch.Tensor, scale: torch.Tensor, n_groups: int) -> torch.Tensor:
    """Unbiased estimate of (E[r]/s)², averaged over ``n_groups`` conditions.

    ``residual`` and ``scale`` hold ``n_groups`` consecutive blocks of an even number of samples (one
    block per condition). Each block is split in two halves; the product of the two half-means has
    expectation (E r)², whereas the square of one mean would add Var(r)/n and penalize the spread of
    the law. The scale (mean over the block) is detached.
    """
    n_per = residual.shape[0] // n_groups
    if n_per < 2 or n_per % 2 or n_per * n_groups != residual.shape[0]:
        raise ValueError("half_batch_product: n_groups blocks of an even number (≥ 2) of samples expected")
    r = residual.view(n_groups, 2, n_per // 2).mean(2)
    s = scale.detach().view(n_groups, n_per).mean(1).clamp_min(1e-30)
    return ((r[:, 0] / s) * (r[:, 1] / s)).mean()


# =============================================================================================
# Sampling procedures
# =============================================================================================
def projected_flow_sample(field: Any, space: FourierComponentSpace, z0: torch.Tensor, c: torch.Tensor,
                          steps: int = 50) -> torch.Tensor:
    """Projected flow: project the noise, then every stage of Heun's scheme, onto k·f̂ = 0.

    ``z0``: Gaussian noise in normalized coordinates ``(b, M, 6 F)``. Train the field with the same
    projected noise (``noise_fn=lambda shape: space.project(torch.randn(shape))``) so that the whole
    path stays in the solenoidal subspace (Proposition 2: only the component in S has to be learnt).
    """
    return heun_sample(field, space.project(z0), c, steps=steps, project=space.project)


def balance_rescaling(space: Any, fh: torch.Tensor, nu: torch.Tensor | float, eta: torch.Tensor | float,
                      forcing_hat: torch.Tensor, amp: torch.Tensor | float = 1.0,
                      k_split: float | None = None) -> tuple[torch.Tensor, torch.Tensor]:
    """Per-sample rescaling of the small scales so that ⟨f·u⟩ = ν⟨|ω|²⟩ + η⟨|j|²⟩ holds for each sample.

    The modes |k| > ``k_split`` (default: just above the largest forced wavenumber) of u and B are
    multiplied by s ≥ 0 with s² = (injection − D_large) / D_small; the forced modes are not touched,
    so the injection is unchanged. This is the per-sample version of a law-level identity: by
    Corollary 6 it cannot give the right law when dE/dt fluctuates (its variance is set to zero).
    Returns the rescaled coefficients and the factors ``s`` (b,).
    """
    k = space.k.to(fh.real.dtype)
    kn = (k * k).sum(-1).sqrt()
    if k_split is None:
        forced = forcing_hat.abs().sum(-1) > 1e-4 * float(forcing_hat.abs().max())   # above float32 round-off
        k_split = float(kn[forced].max()) * (1 + 1e-6)
    small = (kn > k_split).to(fh.real.dtype)[:, None]
    large_t = budget_terms_hat(space, fh * (1 - small), nu, eta, forcing_hat=forcing_hat, amp=amp)
    small_t = budget_terms_hat(space, fh * small, nu, eta)
    d_large = large_t["kinetic_dissipation"] + large_t["magnetic_dissipation"]
    d_small = small_t["kinetic_dissipation"] + small_t["magnetic_dissipation"]
    s = ((large_t["injection"] - d_large) / d_small.clamp_min(1e-30)).clamp_min(0.0).sqrt()
    return fh * (1 - small) + fh * small * s.view(-1, 1, 1, 1).to(fh.dtype), s


def balance_tilting(residuals: np.ndarray, reg: float = 1.0) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    """Exponential tilting of a sample cloud on stationarity identities (I-projection).

    ``residuals`` (N, m): per-sample residuals of m identities (columns of
    :func:`stationarity_residuals`). Returns the weights w_i ∝ exp(λ·g_i) that bring the weighted
    means to zero with minimal KL to the uniform weights, the multipliers λ (to weight another
    sample of the same law: w ∝ exp(g·λ)) and ``{"ess", "ess_frac", "residual"}``. The tilting is
    exact only for the imposed moments and only where the effective sample size holds.
    """
    from milady.eval.tilt import exp_tilt

    return exp_tilt(np.asarray(residuals, dtype=np.float64), reg=reg)


# =============================================================================================
# Model families: explicit linear part, second-order baseline
# =============================================================================================
class ModewiseAffineSkip(nn.Module):
    """v(x, t, c) = G(t, c) x + b(t, c) + base(x, t, c), with one C × C matrix G and one offset b per mode.

    ``x``: latent ``(b, M, C)``. For Gaussian data the optimal flow-matching field is affine in x; with
    uncorrelated Fourier modes it is exactly of this mode-wise form. A base network whose hidden
    width is below M × C cannot carry that term (its Jacobian has rank at most the width): it is given
    explicitly here, as two linear read-outs of an embedding of (t, c), initialized at zero.
    """

    def __init__(self, base: nn.Module, n_modes: int, n_channels: int, n_cond: int, emb_dim: int = 128,
                 n_freq: int = 16, cond_scale: float = 0.5) -> None:
        super().__init__()
        from milady.train.fm3d import ConditionEmbedding

        self.base = base
        self.n_modes, self.n_channels = n_modes, n_channels
        self.embed = ConditionEmbedding(n_cond, emb_dim, n_freq, cond_scale)
        self.gain = nn.Linear(emb_dim, n_modes * n_channels * n_channels)
        self.offset = nn.Linear(emb_dim, n_modes * n_channels)
        for layer in (self.gain, self.offset):
            nn.init.zeros_(layer.weight)
            nn.init.zeros_(layer.bias)

    def affine(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        """The explicit term G(t, c) x + b(t, c)."""
        e = torch.nn.functional.silu(self.embed(t, c))
        g = self.gain(e).view(-1, self.n_modes, self.n_channels, self.n_channels)
        return torch.einsum("bmij,bmj->bmi", g, x) + self.offset(e).view(-1, self.n_modes, self.n_channels)

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return self.affine(x, t, c) + self.base(x, t, c)


class ModewiseGaussian:
    """Conditional Gaussian law with one mean and one C × C covariance per Fourier mode.

    :meth:`fit` estimates the moments of the latents ``x`` (N, M, C) at each distinct value of a
    scalar condition; :meth:`moments` interpolates them linearly between the two neighbouring
    training conditions (a convex combination of covariances is a covariance; no extrapolation);
    :meth:`sample` draws from the interpolated law. ``sign`` (C,), entries ±1: the law is made
    invariant under x → sign · x (e.g. B → −B) by averaging the moments with their images.
    """

    def __init__(self, sign: torch.Tensor | None = None, jitter: float = 1e-6) -> None:
        self.sign = sign
        self.jitter = jitter
        self.c: torch.Tensor | None = None
        self.mean: torch.Tensor | None = None
        self.cov: torch.Tensor | None = None

    @torch.no_grad()
    def fit(self, x: torch.Tensor, c: torch.Tensor) -> ModewiseGaussian:
        x = x.to(torch.float64)
        values = torch.unique(c)
        means, covs = [], []
        for v in values:
            xv = x[c == v]
            m = xv.mean(0)
            d = xv - m
            cov = torch.einsum("nmi,nmj->mij", d, d) / len(xv)
            if self.sign is not None:
                s = self.sign.to(x.dtype).to(x.device)
                m = 0.5 * (m + s * m)
                cov = 0.5 * (cov + s[:, None] * cov * s[None, :])
            means.append(m)
            covs.append(cov)
        self.c, self.mean, self.cov = values.to(torch.float64), torch.stack(means), torch.stack(covs)
        return self

    def moments(self, c: float) -> tuple[torch.Tensor, torch.Tensor]:
        """Mean (M, C) and covariance (M, C, C) at the condition ``c`` (clamped to the training range)."""
        assert self.c is not None and self.mean is not None and self.cov is not None, "fit first"
        grid = self.c
        c = float(min(max(c, float(grid[0])), float(grid[-1])))
        j = int(torch.searchsorted(grid, torch.tensor(c, dtype=grid.dtype, device=grid.device)).clamp(1, len(grid) - 1))
        w = (c - float(grid[j - 1])) / (float(grid[j]) - float(grid[j - 1]))
        return (1 - w) * self.mean[j - 1] + w * self.mean[j], (1 - w) * self.cov[j - 1] + w * self.cov[j]

    @torch.no_grad()
    def sample(self, c: float, n: int, generator: torch.Generator | None = None) -> torch.Tensor:
        """``n`` latents (n, M, C), float32, from the Gaussian law at the condition ``c``."""
        mean, cov = self.moments(c)
        eye = torch.eye(cov.shape[-1], dtype=cov.dtype, device=cov.device)
        scale = cov.diagonal(dim1=-2, dim2=-1).mean(-1).clamp_min(1e-30)
        chol = torch.linalg.cholesky(cov + self.jitter * scale[:, None, None] * eye)
        xi = torch.randn(n, *mean.shape, generator=generator, dtype=cov.dtype).to(cov.device)
        return (mean + torch.einsum("mij,nmj->nmi", chol, xi)).to(torch.float32)


class GaussianAnchoredField(nn.Module):
    """v(x, t, c) = v_Gauss(x, t, c) + base(x, t, c): flow matching anchored on the Gaussian law.

    For x₀ ~ N(0, I) and x₁ ~ N(μ, Σ) on the linear path x_t = (1 − t) x₀ + t x₁, the optimal field is

        v_Gauss(x, t) = μ + (t Σ − (1 − t) I) (t² Σ + (1 − t)² I)⁻¹ (x − t μ),

    applied here mode by mode with the moments of a fitted :class:`ModewiseGaussian`, interpolated
    in the scalar condition ``c`` (first column of the condition tensor). Integrating v_Gauss alone
    from Gaussian noise gives exactly N(μ(c), Σ(c)). ``base`` (any field, typically zero at
    initialization) learns the non-Gaussian part of the law. The eigendecompositions of Σ(c) are
    cached per value of c (few distinct values: the training conditions, then one per sampling call).
    """

    def __init__(self, base: nn.Module, gaussian: ModewiseGaussian, max_cache: int = 64) -> None:
        super().__init__()
        assert gaussian.c is not None and gaussian.mean is not None and gaussian.cov is not None, "fit the Gaussian first"
        self.base = base
        self.jitter = gaussian.jitter
        self.max_cache = max_cache
        self.register_buffer("c_grid", gaussian.c.clone())
        self.register_buffer("mean", gaussian.mean.clone())
        self.register_buffer("cov", gaussian.cov.clone())
        self._cache: dict[tuple[float, str], tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = {}

    def _moments(self, c: float) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Mean (M, C), eigenvalues (M, C) and eigenvectors (M, C, C) of the covariance at ``c`` (float32)."""
        key = (round(c, 7), str(self.mean.device))
        if key not in self._cache:
            grid = self.c_grid
            cc = float(min(max(c, float(grid[0])), float(grid[-1])))
            j = int(torch.searchsorted(grid, torch.tensor(cc, dtype=grid.dtype, device=grid.device)).clamp(1, len(grid) - 1))
            w = (cc - float(grid[j - 1])) / (float(grid[j]) - float(grid[j - 1]))
            mean = (1 - w) * self.mean[j - 1] + w * self.mean[j]
            cov = (1 - w) * self.cov[j - 1] + w * self.cov[j]
            lam, q = torch.linalg.eigh(cov)
            lam = lam.clamp_min(self.jitter * float(lam.mean()))
            if len(self._cache) >= self.max_cache:
                self._cache.clear()
            self._cache[key] = (mean.float(), lam.float(), q.float())
        return self._cache[key]

    def gaussian_field(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        """The closed-form field of the Gaussian law at the conditions ``c`` (b, n_cond) or (b,)."""
        cs = c[:, 0] if c.dim() > 1 else c
        out = torch.empty_like(x)
        for value in torch.unique(cs):
            sel = cs == value
            mean, lam, q = self._moments(float(value))
            tt = t[sel].view(-1, 1, 1).to(x.dtype)
            y = torch.einsum("mji,bmj->bmi", q, x[sel] - tt * mean)                      # Qᵀ (x − t μ)
            gain = (tt * lam - (1 - tt)) / (tt**2 * lam + (1 - tt) ** 2)
            out[sel] = mean + torch.einsum("mij,bmj->bmi", q, gain * y)
        return out

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return self.gaussian_field(x, t, c) + self.base(x, t, c)
