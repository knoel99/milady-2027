"""Static figures of module p7 (generative models: DDPM, flow matching).

Usage: python3 figures_p7.py [out_dir]     (default: the folder of this script)
fig-paths uses the exact marginal field of section 4; fig-fm-conditional trains the network of the
hands-on session 5.6 (same code, seed 0, about 15 s on one CPU thread). Runs in under a minute.
"""
import math
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

fs.use(10)
HERE = Path(__file__).resolve().parent


def _box(a, lim):
    a.set_xlim(-lim, lim); a.set_ylim(-lim, lim); a.set_aspect("equal")
    a.set_xticks([]); a.set_yticks([]); a.grid(False)
    for sp in a.spines.values():
        sp.set_visible(True); sp.set_color("#cccccc")


# ---------------------------------------------------------------------------------------------
def fig_noising(out):
    """Linear schedule of Ho et al. (2020): beta from 1e-4 to 0.02, K = 1000 (example 2.3)."""
    rng = np.random.default_rng(0)
    K = 1000
    abar = np.cumprod(1 - np.linspace(1e-4, 0.02, K))
    n = 2000
    centres = np.array([[np.cos(a), np.sin(a)] for a in np.pi / 8 + np.arange(4) * np.pi / 2])
    y0 = 1.5 * centres[rng.integers(0, 4, n)] + 0.12 * rng.standard_normal((n, 2))
    eps = rng.standard_normal((n, 2))
    fig, ax = plt.subplots(1, 5, figsize=(12, 2.9))
    for a, k in zip(ax, (0, 50, 150, 300, 1000)):
        ab = 1.0 if k == 0 else abar[k - 1]
        yk = np.sqrt(ab) * y0 + np.sqrt(1 - ab) * eps
        a.scatter(yk[:, 0], yk[:, 1], s=1.2, color=fs.C1, alpha=0.6, lw=0)
        a.set_title(f"k = {k}\n" + ("data" if k == 0 else rf"$\bar\alpha_k$ = {ab:.3f}"))
        _box(a, 3.4)
    print("noising: alpha_bar at k = 50, 150, 300, 1000:", ", ".join(f"{abar[k - 1]:.3f}" for k in (50, 150, 300, 1000)))
    fig.tight_layout()
    fs.save(fig, out / "fig-noising.png")


# ---------------------------------------------------------------------------------------------
PI, M, S = np.array([0.3, 0.7]), np.array([-2.0, 2.0]), 0.5


def _p_t(x, t):
    var = (1 - t) ** 2 + t ** 2 * S ** 2
    return sum(p * np.exp(-0.5 * (x - t * m) ** 2 / var) / np.sqrt(2 * np.pi * var) for p, m in zip(PI, M))


def _v_marginal(x, t):
    """Exact marginal field of the linear path (proposition 4.8, same formula as the page)."""
    var = (1 - t) ** 2 + t ** 2 * S ** 2
    g = PI * np.exp(-0.5 * (x[:, None] - t * M) ** 2 / var) / np.sqrt(var)
    w = g / g.sum(1, keepdims=True)
    vk = M + ((t * S ** 2 - (1 - t)) / var) * (x[:, None] - t * M)
    return (w * vk).sum(1)


def fig_paths(out):
    rng = np.random.default_rng(1)
    t = np.linspace(0, 1, 201); x = np.linspace(-4, 4, 401)
    T, X = np.meshgrid(t, x)
    dens = _p_t(X, T)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
    for a in ax:
        a.imshow(dens, extent=(0, 1, -4, 4), origin="lower", aspect="auto", cmap=fs.BLUES, vmax=0.9 * dens.max())
        a.grid(False); a.set_xlabel("flow time t  (t = 0: noise,  t = 1: data)")
    n = 16
    x0 = rng.standard_normal(n)
    x1 = np.where(rng.random(n) < PI[0], M[0], M[1]) + S * rng.standard_normal(n)
    for a0, a1 in zip(x0, x1):
        ax[0].plot([0, 1], [a0, a1], color=fs.C2, lw=1.4)
    ax[0].set_ylabel("x"); ax[0].set_title("Conditional segments  $x_t = (1-t)\\,x_0 + t\\,x_1$  (they cross)")
    z = np.sort(np.concatenate([np.linspace(-1.9, 1.9, 14)]))
    steps, path = 400, [z]
    h = 1.0 / steps
    for k in range(steps):                                    # Heun with the exact field
        v0 = _v_marginal(path[-1], k * h)
        v1 = _v_marginal(path[-1] + h * v0, (k + 1) * h)
        path.append(path[-1] + 0.5 * h * (v0 + v1))
    path = np.array(path)
    ax[1].plot(np.linspace(0, 1, steps + 1), path, color=fs.INK, lw=1.4)
    order = bool(np.all(np.diff(path, axis=1) > 0))
    print(f"paths: marginal trajectories keep their order: {order}")
    ax[1].set_title("Marginal flow trajectories  $\\dot x = v_t(x)$  (no crossing)")
    ax[0].set_ylim(-4, 4)
    fig.tight_layout()
    fs.save(fig, out / "fig-paths.png")


# ---------------------------------------------------------------------------------------------
def fig_fm_conditional(out):
    """Code of the hands-on session 5.6 (seed 0), then 1000 samples per lambda."""
    torch.manual_seed(0)
    torch.set_num_threads(1)

    def samples(lam, n):
        lam = torch.as_tensor(lam, dtype=torch.float32).expand(n)
        k = torch.randint(0, 4, (n,))
        ang = k * math.pi / 2 + lam * math.pi / 4
        centre = (1.0 + lam)[:, None] * torch.stack([torch.cos(ang), torch.sin(ang)], 1)
        return centre + 0.15 * torch.randn(n, 2)

    LAM_TRAIN = torch.tensor([0.0, 0.25, 0.5, 0.75, 1.0])

    class Field(nn.Module):
        def __init__(self, width=128):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(4, width), nn.SiLU(), nn.Linear(width, width), nn.SiLU(),
                                     nn.Linear(width, width), nn.SiLU(), nn.Linear(width, 2))

        def forward(self, x, t, lam):
            return self.net(torch.cat([x, t[:, None], lam[:, None]], 1))

    v = Field()
    opt = torch.optim.Adam(v.parameters(), lr=2e-3)
    n_iter, B = 3000, 256
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_iter)
    for _ in range(n_iter):
        lam = LAM_TRAIN[torch.randint(0, 5, (B,))]
        x1 = samples(lam, B); x0 = torch.randn(B, 2); t = torch.rand(B)
        xt = (1 - t[:, None]) * x0 + t[:, None] * x1
        loss = ((v(xt, t, lam) - (x1 - x0)) ** 2).sum(1).mean()
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
    print(f"fm-conditional: final loss {loss.item():.3f}")

    @torch.no_grad()
    def sample(lam, n, steps=50):
        x = torch.randn(n, 2)
        L = torch.full((n,), float(lam))
        h = 1.0 / steps
        for i in range(steps):
            t = torch.full((n,), i * h)
            d0 = v(x, t, L)
            d1 = v(x + h * d0, t + h, L)
            x = x + 0.5 * h * (d0 + d1)
        return x

    fig, ax = plt.subplots(2, 4, figsize=(11, 5.8))
    for j, lam in enumerate((0.0, 0.375, 0.625, 1.0)):
        tag = f"λ = {lam}" + ("  (unseen λ)" if lam not in (0.0, 1.0) else "")
        d, g = samples(lam, 1000).numpy(), sample(lam, 1000).numpy()
        ax[0, j].scatter(d[:, 0], d[:, 1], s=1.5, color=fs.INK2, lw=0)
        ax[1, j].scatter(g[:, 0], g[:, 1], s=1.5, color=fs.C1, lw=0)
        ax[0, j].set_title(f"data\n{tag}"); ax[1, j].set_title(f"generated (Heun, 50 steps)\n{tag}")
        _box(ax[0, j], 2.6); _box(ax[1, j], 2.6)
    fig.tight_layout()
    fs.save(fig, out / "fig-fm-conditional.png")


if __name__ == "__main__":
    out = fs.out_dir(__file__, sys.argv)
    for fn in (fig_noising, fig_paths, fig_fm_conditional):
        fn(out)
