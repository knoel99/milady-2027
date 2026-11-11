"""Kinematic induction in a prescribed ABC flow: NumPy reference solver of experiment E3.

Induction equation with prescribed flow, periodic domain [0, 2π)³:
    ∂B/∂t = ∇×(u×B) + η ΔB,   u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x),   Rm = 1/η.
Pseudo-spectral scheme (rfftn), 2/3 dealiasing, integrating-factor RK4 for the diffusion.
The curl form preserves ∇·B = 0 at the discrete level (k·(k×v) = 0).

:func:`growth_rate` measures λ = d ln‖B‖/dt after the transient (fit on the second half of the run).
This code produced the published E3 results; ``milady.sim.mhd3d`` (kinematic mode, torch) solves
the same equation with a different random initial field and Leray re-projection, so its λ agrees
only within the fit error (``tests/test_mhd3d.py``). Code name in MFF files: ``induction3d_numpy``.
"""

from __future__ import annotations

import numpy as np

__all__ = ["Induction3D", "growth_rate"]


class Induction3D:
    def __init__(self, n=32, eta=0.1, A=1.0, B=1.0, C=1.0, seed=0):
        self.n, self.eta = n, eta
        k = np.fft.fftfreq(n, 1.0 / n)
        kr = np.fft.rfftfreq(n, 1.0 / n)
        self.kx, self.ky, self.kz = np.meshgrid(k, k, kr, indexing="ij")
        self.k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2
        kmax = n // 3
        self.dealias = (np.abs(self.kx) <= kmax) & (np.abs(self.ky) <= kmax) & (np.abs(self.kz) <= kmax)
        x = np.arange(n) * 2 * np.pi / n
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        self.u = np.stack([A * np.sin(Z) + C * np.cos(Y), B * np.sin(X) + A * np.cos(Z), C * np.sin(Y) + B * np.cos(X)])
        rng = np.random.default_rng(seed)
        b = rng.normal(size=(3, n, n, n))
        bh = np.stack([np.fft.rfftn(c) for c in b]) * self.dealias * np.exp(-self.k2 / 8)
        bh[:, 0, 0, 0] = 0  # no mean field: in the periodic setting it is conserved exactly (neutral mode)
        self.bh = self.solenoidal(bh)
        self.bh /= self.norm(self.bh)

    def solenoidal(self, vh):
        k2 = np.where(self.k2 == 0, 1, self.k2)
        d = self.kx * vh[0] + self.ky * vh[1] + self.kz * vh[2]
        return np.stack([vh[0] - self.kx * d / k2, vh[1] - self.ky * d / k2, vh[2] - self.kz * d / k2])

    def norm(self, vh):
        b = np.stack([np.fft.irfftn(c, s=(self.n,) * 3, axes=(0, 1, 2)) for c in vh])
        return np.sqrt(np.mean(np.sum(b ** 2, 0)))

    def rhs(self, bh):
        b = np.stack([np.fft.irfftn(c, s=(self.n,) * 3, axes=(0, 1, 2)) for c in bh])
        e = np.cross(self.u, b, axis=0)               # u × B
        eh = np.stack([np.fft.rfftn(c) for c in e]) * self.dealias
        # ∇×(u×B) in Fourier space: i k × ê
        return 1j * np.stack([self.ky * eh[2] - self.kz * eh[1], self.kz * eh[0] - self.kx * eh[2], self.kx * eh[1] - self.ky * eh[0]])

    def step(self, dt):
        L = -self.eta * self.k2
        E, E2 = np.exp(L * dt), np.exp(L * dt / 2)
        b = self.bh
        k1 = self.rhs(b)
        k2 = self.rhs(E2 * (b + 0.5 * dt * k1))
        k3 = self.rhs(E2 * b + 0.5 * dt * k2)
        k4 = self.rhs(E * b + dt * E2 * k3)
        self.bh = E * b + dt / 6 * (E * k1 + 2 * E2 * (k2 + k3) + k4)

    def divergence_rel(self):
        d = self.kx * self.bh[0] + self.ky * self.bh[1] + self.kz * self.bh[2]
        return float(np.sqrt(np.sum(np.abs(d) ** 2) / np.sum(self.k2 * np.sum(np.abs(self.bh) ** 2, 0))))


def growth_rate(rm, n=32, t_total=120.0, dt=0.05, seed=0):
    m = Induction3D(n=n, eta=1.0 / rm, seed=seed)
    logn, ts = [], []
    acc = 0.0
    for k in range(int(t_total / dt)):
        m.step(dt)
        if (k + 1) % 20 == 0:
            nb = m.norm(m.bh)
            acc += np.log(nb)
            m.bh /= nb
            logn.append(acc)
            ts.append((k + 1) * dt)
    ts, logn = np.array(ts), np.array(logn)
    late = ts > t_total / 2
    lam = np.polyfit(ts[late], logn[late], 1)[0]
    lam_q = np.polyfit(ts[ts > 3 * t_total / 4], logn[ts > 3 * t_total / 4], 1)[0]
    return float(lam), float(lam_q), m
