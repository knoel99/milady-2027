"""Shared tools for the MilaDy 2027 experiments.

The generic tools live in the ``milady`` package and are re-exported here with the settings of the
published runs:

- conditional flow matching (linear path, "rectified flow"): ``milady.train.flow``;
- integration of the sampling ODE (Heun): ``milady.train.flow.heun_sample``;
- metrics between distributions: energy distance, sliced Wasserstein-1 (``milady.eval.metrics``);
- exponential tilting (I-projection) of a sample cloud: ``milady.eval.tilt``.

Specific to the experiments: the small MLP field, the sign-symmetrized wrapper and the training loop.
Everything runs on CPU. Python 3.11+, NumPy, PyTorch. The package is used from ``src/`` if it is not
installed (``make setup`` installs it).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

try:
    import milady  # noqa: F401
except ImportError:  # repository checkout without `pip install -e .`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from milady.eval import metrics as _metrics
from milady.eval.tilt import exp_tilt, systematic_resample  # noqa: F401 (re-exported)
from milady.train.flow import FourierEmbedding as Fourier  # noqa: F401 (re-exported)
from milady.train.flow import fm_loss as _fm_loss
from milady.train.flow import heun_sample

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGS = HERE.parent / "site" / "experiments" / "figures"  # published with the page
RESULTS.mkdir(exist_ok=True)
FIGS.mkdir(exist_ok=True)


def seed_all(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


def save_json(obj, name: str) -> Path:
    path = RESULTS / name
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Time and parameter embeddings
# ---------------------------------------------------------------------------
class MLPField(nn.Module):
    """Velocity field v_theta(x, t, c) for low-dimensional states."""

    def __init__(self, dim: int, width: int = 256, depth: int = 4, n_freq: int = 16):
        super().__init__()
        self.temb = Fourier(n_freq)
        self.cemb = Fourier(n_freq, scale=8.0)
        d_in = dim + 2 * (2 * n_freq + 1)
        layers = []
        for i in range(depth):
            layers += [nn.Linear(d_in if i == 0 else width, width), nn.SiLU()]
        layers += [nn.Linear(width, dim)]
        self.net = nn.Sequential(*layers)

    def forward(self, x, t, c):
        return self.net(torch.cat([x, self.temb(t), self.cemb(c)], dim=1))


class SymmetrizedField(nn.Module):
    """v_sym(x) = (v(x) + S v(S x)) / 2 : equivariant for a linear involution S (diagonal)."""

    def __init__(self, base: nn.Module, s_diag):
        super().__init__()
        self.base = base
        self.register_buffer("s", torch.as_tensor(s_diag, dtype=torch.float32))

    def forward(self, x, t, c):
        return 0.5 * (self.base(x, t, c) + self.s * self.base(self.s * x, t, c))


# ---------------------------------------------------------------------------
# Flow matching
# ---------------------------------------------------------------------------
def fm_loss(model, x1, c, noise_fn=None, extra=None):
    """Flow matching loss (linear path x_t = (1-t) x0 + t x1, target x1 - x0); see ``milady.train.flow``.

    noise_fn : function that draws x0 (default: standard Gaussian of the same shape).
    extra    : function (model, xt, t, c, v_pred, x1) -> additional loss (physics penalty).
    """
    return _fm_loss(model, x1, c, noise_fn=noise_fn, extra=extra)


@torch.no_grad()
def sample_ode(model, c, shape, steps: int = 100, noise_fn=None, project=None, x0=None):
    """Integrate dx/dt = v(x, t, c) from t=0 to 1 with Heun's scheme, from Gaussian (or ``noise_fn``) noise.

    project : map (x -> x) applied to the initial noise and after each step (projected flow).
    """
    x = x0 if x0 is not None else (noise_fn(shape) if noise_fn is not None else torch.randn(shape))
    if project is not None:
        x = project(x)
    return heun_sample(model, x, c, steps=steps, project=project)


def train(model, sampler_fn, iters: int, lr: float = 2e-3, log_every: int = 1000, extra=None,
          noise_fn=None, wd: float = 0.0, name: str = ""):
    """Generic training loop. sampler_fn() -> (x1, c)."""
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=iters, pct_start=0.05)
    hist = []
    t0 = time.time()
    run = 0.0
    for it in range(1, iters + 1):
        x1, c = sampler_fn()
        loss = fm_loss(model, x1, c, noise_fn=noise_fn, extra=extra)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        run = 0.98 * run + 0.02 * loss.item() if it > 1 else loss.item()
        if it % log_every == 0 or it == iters:
            hist.append((it, run))
            print(f"[{name}] it {it:6d}  loss {run:.4f}  {time.time() - t0:.0f} s", flush=True)
    return hist, time.time() - t0


# ---------------------------------------------------------------------------
# Distances between distributions (samples): settings of the published E1–E2 runs
# ---------------------------------------------------------------------------
def energy_distance(x: np.ndarray, y: np.ndarray, n: int = 4000, seed: int = 0) -> float:
    """Székely energy distance D² (V statistic, ``torch.cdist`` distances): ``milady.eval.metrics.energy_distance``."""
    return _metrics.energy_distance(x, y, n=n, seed=seed, estimator="V", pdist="torch")


def sliced_w1(x: np.ndarray, y: np.ndarray, n_proj: int = 256, seed: int = 0, n: int = 20000) -> float:
    """Sliced Wasserstein-1, subsampled to ``n`` points then truncated to the smaller set (estimator of E1)."""
    return _metrics.sliced_w1(x, y, n_proj=n_proj, seed=seed, match="truncate", n_sub=n)
