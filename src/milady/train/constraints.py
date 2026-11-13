"""Two ways to keep a spectral magnetic field solenoidal.

A Fourier coefficient ``(M, 3)`` splits into a longitudinal part, parallel to
the wavevector, and a transverse part. The longitudinal part is a pure
gradient. ``project_solenoidal`` removes it after every step of the sampler.
``divergence_penalty`` adds its energy to the training loss instead.

Neither function counts magnetic nulls. The Haynes–Parnell count is not
implemented here.
"""

from __future__ import annotations

import torch


def _wavevector(k: torch.Tensor) -> torch.Tensor:
    if k.ndim != 2 or k.shape[-1] != 3:
        raise ValueError("k must have shape (M, 3)")
    return k


def project_solenoidal(coeff: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    """Remove the longitudinal part of ``coeff`` (``(..., M, 3)``, real or complex)."""
    k = _wavevector(k).to(dtype=coeff.real.dtype if coeff.is_complex() else coeff.dtype, device=coeff.device)
    kn2 = (k * k).sum(-1).clamp_min(1e-30)
    dot = (coeff * k).sum(-1)
    return coeff - dot[..., None] * k / kn2[..., None]


def divergence_penalty(coeff: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    """Mean longitudinal energy ``|k · coeff|² / |k|²``. Zero on a solenoidal field."""
    k = _wavevector(k).to(dtype=coeff.real.dtype if coeff.is_complex() else coeff.dtype, device=coeff.device)
    kn2 = (k * k).sum(-1).clamp_min(1e-30)
    dot = (coeff * k).sum(-1)
    return (dot.abs() ** 2 / kn2).mean()
