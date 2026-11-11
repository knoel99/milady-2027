"""Shared tools for the MilaDy 2027 experiments.

- conditional flow matching (linear path, "rectified flow");
- integration of the sampling ODE (Heun);
- metrics between distributions: energy distance, sliced Wasserstein-1;
- exponential tilting (I-projection) of a sample cloud under moment constraints.

Everything runs on CPU. Python 3.11+, NumPy, PyTorch.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

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
class Fourier(nn.Module):
    """Sinusoidal embedding of a scalar in [0, 1] (time or normalised parameter)."""

    def __init__(self, n: int = 16, scale: float = 30.0):
        super().__init__()
        self.register_buffer("freqs", torch.exp(torch.linspace(0.0, math.log(scale), n)))

    def forward(self, s: torch.Tensor) -> torch.Tensor:
        a = s[:, None] * self.freqs[None, :] * 2 * math.pi
        return torch.cat([torch.sin(a), torch.cos(a), s[:, None]], dim=1)


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
    """Flow matching loss (linear path x_t = (1-t) x0 + t x1, target x1 - x0).

    noise_fn : function that draws x0 (default: standard Gaussian of the same shape).
    extra    : function (model, xt, t, c, v_pred, x1) -> additional loss (physics penalty).
    """
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


@torch.no_grad()
def sample_ode(model, c, shape, steps: int = 100, noise_fn=None, project=None, x0=None):
    """Integrate dx/dt = v(x, t, c) from t=0 to 1 with Heun's scheme.

    project : map (x -> x) applied to the initial noise and after each step (projected flow).
    """
    x = x0 if x0 is not None else (noise_fn(shape) if noise_fn is not None else torch.randn(shape))
    if project is not None:
        x = project(x)
    h = 1.0 / steps
    for k in range(steps):
        t0 = torch.full((shape[0],), k * h)
        t1 = torch.full((shape[0],), (k + 1) * h)
        v0 = model(x, t0, c)
        xe = x + h * v0
        if project is not None:
            xe = project(xe)
        v1 = model(xe, t1, c)
        x = x + 0.5 * h * (v0 + v1)
        if project is not None:
            x = project(x)
    return x


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
# Distances between distributions (samples)
# ---------------------------------------------------------------------------
def _mean_pdist(a: torch.Tensor, b: torch.Tensor, chunk: int = 2048) -> float:
    tot = 0.0
    for i in range(0, a.shape[0], chunk):
        tot += torch.cdist(a[i:i + chunk], b).sum().item()
    return tot / (a.shape[0] * b.shape[0])


def energy_distance(x: np.ndarray, y: np.ndarray, n: int = 4000, seed: int = 0, wx=None) -> float:
    """Székely energy distance, D^2 = 2E|X-Y| - E|X-X'| - E|Y-Y'| (>= 0, zero iff same distribution).

    wx : optional weights of the x samples (x is then resampled according to these weights).
    """
    rng = np.random.default_rng(seed)
    if wx is not None:
        idx = rng.choice(len(x), size=min(n, len(x)), p=wx / wx.sum())
    else:
        idx = rng.choice(len(x), size=min(n, len(x)), replace=False)
    a = torch.as_tensor(x[idx], dtype=torch.float64)
    b = torch.as_tensor(y[rng.choice(len(y), size=min(n, len(y)), replace=False)], dtype=torch.float64)
    return 2 * _mean_pdist(a, b) - _mean_pdist(a, a) - _mean_pdist(b, b)


def sliced_w1(x: np.ndarray, y: np.ndarray, n_proj: int = 256, seed: int = 0, n: int = 20000) -> float:
    """Sliced Wasserstein-1: mean over random directions of W1 between 1D projections."""
    rng = np.random.default_rng(seed)
    d = x.shape[1]
    th = rng.normal(size=(n_proj, d))
    th /= np.linalg.norm(th, axis=1, keepdims=True)
    xs = x[rng.choice(len(x), size=min(n, len(x)), replace=False)]
    ys = y[rng.choice(len(y), size=min(n, len(y)), replace=False)]
    m = min(len(xs), len(ys))
    px = np.sort(xs[:m] @ th.T, axis=0)
    py = np.sort(ys[:m] @ th.T, axis=0)
    return float(np.abs(px - py).mean())


# ---------------------------------------------------------------------------
# Exponential tilting (Csiszar I-projection) on a sample cloud
# ---------------------------------------------------------------------------
def exp_tilt(g: np.ndarray, target=None, iters: int = 100, tol: float = 1e-10, reg: float = 0.0):
    """Weights w_i ∝ exp(λ·g_i) with minimal KL(w || uniform) such that Σ w_i g_i = target.

    g : (N, m) values of the constraint functions on the samples.
    Returns (normalised w, λ, info). Damped Newton method on the convex dual
    Φ(λ) = log mean exp(λ·g) - λ·target + (reg / 2N) λᵀ Ĉ λ.
    reg > 0 : regularised I-projection (maximum entropy with relaxed constraints); the tolerated
    residual is of the order of the Monte Carlo error of the empirical mean (Ĉ = correlation of g).
    """
    g = np.asarray(g, dtype=np.float64)
    n, m = g.shape
    target = np.zeros(m) if target is None else np.asarray(target, dtype=np.float64)
    scale = g.std(axis=0) + 1e-12
    gs = (g - target) / scale
    lam = np.zeros(m)
    R = reg * np.corrcoef(gs, rowvar=False).reshape(m, m) / n if reg > 0 else np.zeros((m, m))

    def dual(l):
        z = gs @ l
        zmax = z.max()
        return zmax + np.log(np.mean(np.exp(z - zmax))) + 0.5 * l @ R @ l

    for _ in range(iters):
        z = gs @ lam
        w = np.exp(z - z.max())
        w /= w.sum()
        mean = w @ gs
        grad = mean + R @ lam
        if np.linalg.norm(grad) < tol:
            break
        cov = (gs * w[:, None]).T @ gs - np.outer(mean, mean)
        step = np.linalg.solve(cov + R + 1e-10 * np.eye(m), grad)
        f0, s = dual(lam), 1.0
        while dual(lam - s * step) > f0 - 1e-4 * s * (grad @ step) and s > 1e-8:
            s *= 0.5
        lam = lam - s * step
    z = gs @ lam
    w = np.exp(z - z.max())
    w /= w.sum()
    ess = 1.0 / np.sum(w ** 2)
    return w, lam / scale, {"ess": float(ess), "ess_frac": float(ess / n), "residu": float(np.linalg.norm(w @ gs))}


def systematic_resample(w: np.ndarray, n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pos = (rng.random() + np.arange(n)) / n
    return np.minimum(np.searchsorted(np.cumsum(w), pos), len(w) - 1)
