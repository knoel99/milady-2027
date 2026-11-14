"""Variance-preserving diffusion on the same spaces and networks as the flow matching models.

Model family compared with flow matching in the race (the offer names "diffusion or flow
matching"). The noising path is trigonometric, x_s = cos(φ) x₁ + sin(φ) ε with φ = π s / 2,
s ∈ [0, 1] (s = 0: data, s = 1: noise), so that Var(x_s) is constant for standardized data. The
network ``field(x, s, c)`` predicts the velocity along the path, v = cos(φ) ε − sin(φ) x₁
("v-prediction"), which stays well conditioned at both ends: x̂₁ = cos(φ) x_s − sin(φ) v̂ and
ε̂ = sin(φ) x_s + cos(φ) v̂.

- :func:`diffusion_loss`: mean squared error on v, uniform s;
- :func:`diffusion_sample`: from s = 1 to s = 0 in ``steps`` steps, one network evaluation per step.
  ``stochastic=True`` is ancestral sampling (fresh noise at every step, the reverse-time SDE);
  ``stochastic=False`` is the deterministic sampler (probability-flow ODE, DDIM), a rotation of
  angle Δφ in the (x, v) plane.

Only torch is imported.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

import torch

__all__ = ["diffusion_loss", "diffusion_sample"]


def _angles(s: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    phi = 0.5 * math.pi * s
    return torch.cos(phi), torch.sin(phi)


def diffusion_loss(
    field: Any,
    x1: torch.Tensor,
    c: torch.Tensor,
    *,
    noise_fn: Callable[[torch.Size], torch.Tensor] | None = None,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    """‖field(x_s, s, c) − v‖² (mean over all entries), v = cos(φ) ε − sin(φ) x₁, s uniform on [0, 1]."""
    n = x1.shape[0]
    if generator is not None:
        eps = torch.randn(x1.shape, generator=generator).to(x1.device)
        s = torch.rand(n, generator=generator).to(x1.device)
    else:
        eps = noise_fn(x1.shape) if noise_fn is not None else torch.randn_like(x1)
        s = torch.rand(n, device=x1.device)
    cos, sin = (a.view(-1, *([1] * (x1.dim() - 1))) for a in _angles(s))
    xs = cos * x1 + sin * eps
    target = cos * eps - sin * x1
    return ((field(xs, s, c).float() - target) ** 2).mean()


def diffusion_sample(
    field: Any,
    z: torch.Tensor,
    c: torch.Tensor,
    steps: int = 100,
    stochastic: bool = True,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    """Sample from noise ``z`` (s = 1) to data (s = 0) in ``steps`` network evaluations.

    At each step the network gives x̂₁ and ε̂ at the current s. Deterministic: x ← cos(φ') x̂₁ +
    sin(φ') ε̂. Ancestral: x ← cos(φ') x̂₁ + (sin²(φ') − ς²)^½ ε̂ + ς ξ with ξ fresh Gaussian noise and
    ς² = (sin²φ' / sin²φ)(1 − cos²φ / cos²φ'), the variance of the reverse transition of the
    discretized forward process (DDPM); ς = 0 at the last step.
    """
    n = z.shape[0]
    x = z
    grid = torch.linspace(1.0, 0.0, steps + 1, device=z.device)
    for i in range(steps):
        s, s_next = grid[i], grid[i + 1]
        cos, sin = _angles(s)
        cos_n, sin_n = _angles(s_next)
        v = field(x, s.expand(n), c).float()
        x1_hat = cos * x - sin * v
        eps_hat = sin * x + cos * v
        if stochastic and i < steps - 1:
            var = (sin_n**2 / sin**2) * (1.0 - cos**2 / cos_n**2)
            sigma = torch.sqrt(torch.clamp(var, min=0.0))
            noise = torch.randn(x.shape, generator=generator).to(x.device) if generator is not None else torch.randn_like(x)
            x = cos_n * x1_hat + torch.sqrt(torch.clamp(sin_n**2 - sigma**2, min=0.0)) * eps_hat + sigma * noise
        else:
            x = cos_n * x1_hat + sin_n * eps_hat
    return x
