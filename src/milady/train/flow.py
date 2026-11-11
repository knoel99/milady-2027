"""Conditional flow matching primitives shared by the 3D training (``milady.train.fm3d``) and the CPU
experiments E1–E2 (``experiments/``).

- :class:`FourierEmbedding`: sinusoidal embedding of a scalar (flow time or normalized parameter);
- :func:`fm_loss`: flow matching loss on the linear path x_t = (1 − t) x₀ + t x₁, target x₁ − x₀;
- :func:`heun_sample`: integration of dz/dt = v(z, t, c) from t = 0 to 1 with Heun's scheme,
  optionally projected after each stage (projected flow).

Only torch is imported: ``import milady.train.flow`` does not load the training pipeline.
"""

from __future__ import annotations

import contextlib
import math
from collections.abc import Callable

import torch
from torch import nn

__all__ = ["FourierEmbedding", "fm_loss", "heun_sample"]

Field = Callable[[torch.Tensor, torch.Tensor, torch.Tensor], torch.Tensor]


class FourierEmbedding(nn.Module):
    """Sinusoidal embedding of a scalar (flow time or normalized parameter)."""

    freqs: torch.Tensor

    def __init__(self, n_freq: int = 16, scale: float = 30.0) -> None:
        super().__init__()
        self.register_buffer("freqs", torch.exp(torch.linspace(0.0, math.log(scale), n_freq)))

    def forward(self, s: torch.Tensor) -> torch.Tensor:
        a = s[:, None] * self.freqs[None, :] * (2 * math.pi)
        return torch.cat([torch.sin(a), torch.cos(a), s[:, None]], dim=1)


def _autocast_ctx(autocast: tuple[str, torch.dtype] | None) -> Callable[[], contextlib.AbstractContextManager]:
    if autocast:
        return lambda: torch.autocast(device_type=autocast[0], dtype=autocast[1])
    return contextlib.nullcontext


def fm_loss(
    field: Field,
    x1: torch.Tensor,
    c: torch.Tensor,
    *,
    noise_fn: Callable[[torch.Size], torch.Tensor] | None = None,
    extra: Callable[..., torch.Tensor] | None = None,
    t_sampling: str = "uniform",
    generator: torch.Generator | None = None,
    autocast: tuple[str, torch.dtype] | None = None,
) -> torch.Tensor:
    """Flow matching loss ‖v(x_t, t, c) − (x₁ − x₀)‖² (mean over all entries).

    ``noise_fn(shape)`` draws x₀ (default: standard Gaussian of the shape of ``x1``); ``t_sampling``:
    ``uniform`` or ``logit_normal``; ``generator``: explicit RNG for x₀ and t (validation losses,
    uniform t). ``extra(field, xt, t, c, v, x1)`` adds a penalty (soft physical constraint).
    Draw order (x₀ first, then t) is part of the contract: at equal seed, results are reproducible.
    """
    n = x1.shape[0]
    if generator is not None:
        x0 = torch.randn(x1.shape, generator=generator).to(x1.device)
        t = torch.rand(n, generator=generator).to(x1.device)
    else:
        x0 = noise_fn(x1.shape) if noise_fn is not None else torch.randn_like(x1)
        if t_sampling == "logit_normal":
            t = torch.sigmoid(torch.randn(n, device=x1.device))
        elif t_sampling == "uniform":
            t = torch.rand(n, device=x1.device)
        else:
            raise ValueError(f"t_sampling: uniform or logit_normal, not {t_sampling!r}")
    tt = t.view(-1, *([1] * (x1.dim() - 1)))
    xt = (1 - tt) * x0 + tt * x1
    with _autocast_ctx(autocast)():
        v = field(xt, t, c)
    loss = ((v.float() - (x1 - x0)) ** 2).mean()
    if extra is not None:
        loss = loss + extra(field, xt, t, c, v, x1)
    return loss


def heun_sample(
    field: Field,
    z: torch.Tensor,
    c: torch.Tensor,
    steps: int = 50,
    autocast: tuple[str, torch.dtype] | None = None,
    project: Callable[[torch.Tensor], torch.Tensor] | None = None,
) -> torch.Tensor:
    """Integrate dz/dt = v(z, t, c) from t = 0 to 1 with the Heun scheme (``steps`` steps, 2 evaluations per step).

    ``project`` (optional) is applied to the predictor and after each step (projected flow); the
    caller projects the initial state if needed. Differentiable if called outside ``torch.no_grad``
    (stationarity losses). The times of a step are ``k h`` and ``(k + 1) h``.
    """
    h = 1.0 / steps
    n = z.shape[0]
    ctx = _autocast_ctx(autocast)
    for k in range(steps):
        t0 = torch.full((n,), k * h, device=z.device)
        t1 = torch.full((n,), (k + 1) * h, device=z.device)
        with ctx():
            v0 = field(z, t0, c).float()
        ze = z + h * v0
        if project is not None:
            ze = project(ze)
        with ctx():
            v1 = field(ze, t1, c).float()
        z = z + 0.5 * h * (v0 + v1)
        if project is not None:
            z = project(z)
    return z
