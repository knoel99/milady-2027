"""Exponential tilting (Csiszár I-projection) of a sample cloud under moment constraints.

- :func:`exp_tilt`: weights w_i ∝ exp(λ·g_i) of minimal KL(w ‖ uniform) such that Σ w_i g_i = target
  (damped Newton on the convex dual, optional regularization);
- :func:`systematic_resample`: systematic resampling of a weighted cloud.

Used by experiments E1–E2 (``experiments/``) to impose stationarity identities on generated samples.
NumPy only.
"""

from __future__ import annotations

import numpy as np

__all__ = ["exp_tilt", "systematic_resample"]


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
    return w, lam / scale, {"ess": float(ess), "ess_frac": float(ess / n), "residual": float(np.linalg.norm(w @ gs))}


def systematic_resample(w: np.ndarray, n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pos = (rng.random() + np.arange(n)) / n
    return np.minimum(np.searchsorted(np.cumsum(w), pos), len(w) - 1)
