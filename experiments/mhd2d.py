"""Pseudo-spectral solver for forced incompressible 2D MHD, in terms of potentials.

Domain [0, 2π)², periodic, N×N grid, 2/3 dealiasing.
Unknowns: vorticity ω and magnetic potential a, with
    u = (∂y ψ, -∂x ψ),  ω = -Δψ,      B = (∂y a, -∂x a),  j = -Δa.
Equations (random forcing white in time f_ω, f_a; linear friction α at large scales):
    ∂t ω + u·∇ω = B·∇j + ν Δω - α ω + f_ω
    ∂t a + u·∇a = η Δa - α a + f_a
By construction ∇·u = ∇·B = 0 exactly.

Energy balance E = ½⟨|u|² + |B|²⟩ (⟨·⟩ = spatial average):
    dE/dt = -ν⟨ω²⟩ - η⟨j²⟩ - α⟨|u|²⟩ - α⟨|B|²⟩ + (injection by the forcing).
The forcing is white in time: its mean injection rate is a known constant ε_inj
(Itô formula), independent of the state. In a statistically stationary regime:
    E[ν⟨ω²⟩ + η⟨j²⟩ + α⟨|u|²⟩ + α⟨|B|²⟩] = ε_inj,u + ε_inj,b.
This is a constraint on the LAW of the snapshots, not on each snapshot.
"""
from __future__ import annotations

import numpy as np


class MHD2D:
    def __init__(self, n=64, nu=2e-3, eta=2e-3, alpha=0.02, kf=(2.0, 3.0), eps_u=0.05, eps_b=0.05,
                 batch=8, seed=0):
        self.n, self.nu, self.eta, self.alpha = n, nu, eta, alpha
        self.batch = batch
        self.rng = np.random.default_rng(seed)
        k = np.fft.fftfreq(n, 1.0 / n)
        kr = np.fft.rfftfreq(n, 1.0 / n)
        self.kx, self.ky = np.meshgrid(kr, k)          # (n, n//2+1) ; kx = rfft index
        self.k2 = self.kx ** 2 + self.ky ** 2
        self.k2i = np.where(self.k2 > 0, 1.0 / np.maximum(self.k2, 1e-30), 0.0)
        kmax = n // 3
        self.dealias = (np.abs(self.kx) <= kmax) & (np.abs(self.ky) <= kmax)
        kk = np.sqrt(self.k2)
        self.fmask = (kk >= kf[0]) & (kk <= kf[1])
        # Amplitude of the white forcing: mean injection ε = Σ_k |f̂_k|² var / (k² ...) - calibrated below
        self.eps_u, self.eps_b = eps_u, eps_b
        self._calibrate_forcing()
        self.w = np.zeros((batch, n, n // 2 + 1), complex)
        self.a = np.zeros_like(self.w)

    # -- spectral tools ------------------------------------------------------------
    def to_phys(self, fh):
        return np.fft.irfft2(fh, s=(self.n, self.n))

    def to_spec(self, f):
        return np.fft.rfft2(f)

    def _weights(self):
        """Weights of the rfft modes (interior columns count twice)."""
        w = np.full(self.k2.shape, 2.0)
        w[:, 0] = 1.0
        if self.n % 2 == 0:
            w[:, -1] = 1.0
        return w

    def _calibrate_forcing(self):
        # Forcing f̂ = σ ξ / sqrt(dt) on the modes of the band. Mean injection (Itô):
        #   for ω : ε_u = ½ Σ_k w_k σ_u² / k² / N⁴ × N² ... we calibrate numerically on the ⟨·⟩ norm.
        # With ⟨|u|²⟩ = Σ_k w_k |ω̂_k|²/k² / N⁴ and a complex noise ξ of variance 1 per mode,
        # the kinetic energy injection is ½ σ_u² Σ_{k∈band} w_k / k² / N⁴ (and likewise for a with k²→1/k²).
        wk = self._weights() * self.fmask
        n4 = self.n ** 4
        su = np.sum(wk * self.k2i) / n4          # for ω : energy = |ω̂|²/k²
        sb = np.sum(wk * self.k2) / n4           # for a : energy = k² |â|²
        self.sig_u = np.sqrt(2 * self.eps_u / su)
        self.sig_b = np.sqrt(2 * self.eps_b / sb)

    def _noise(self, sig, dt):
        xi = (self.rng.normal(size=self.w.shape) + 1j * self.rng.normal(size=self.w.shape)) / np.sqrt(2)
        f = sig * xi * self.fmask
        f[:, 0, 0] = 0
        # Hermitian symmetry of the kx = 0 column: symmetrise by going through physical space
        return self.to_spec(self.to_phys(f)) / np.sqrt(dt)

    # -- dynamics --------------------------------------------------------------------
    def fields(self, w=None, a=None):
        w = self.w if w is None else w
        a = self.a if a is None else a
        psi = w * self.k2i
        ux = self.to_phys(1j * self.ky * psi)
        uy = self.to_phys(-1j * self.kx * psi)
        bx = self.to_phys(1j * self.ky * a)
        by = self.to_phys(-1j * self.kx * a)
        return ux, uy, bx, by

    def nonlinear(self, w, a):
        psi = w * self.k2i
        j = self.k2 * a
        ux = self.to_phys(1j * self.ky * psi); uy = self.to_phys(-1j * self.kx * psi)
        bx = self.to_phys(1j * self.ky * a); by = self.to_phys(-1j * self.kx * a)
        wx = self.to_phys(1j * self.kx * w); wy = self.to_phys(1j * self.ky * w)
        jx = self.to_phys(1j * self.kx * j); jy = self.to_phys(1j * self.ky * j)
        ax = self.to_phys(1j * self.kx * a); ay = self.to_phys(1j * self.ky * a)
        nw = self.to_spec(-(ux * wx + uy * wy) + (bx * jx + by * jy)) * self.dealias
        na = self.to_spec(-(ux * ax + uy * ay)) * self.dealias
        return nw, na

    def step(self, dt):
        """One step: integrating-factor RK4 (Lawson) for the deterministic part, then forcing (Euler-Maruyama)."""
        Lw = -(self.nu * self.k2 + self.alpha)
        La = -(self.eta * self.k2 + self.alpha)
        Ew, Ew2 = np.exp(Lw * dt), np.exp(Lw * dt / 2)
        Ea, Ea2 = np.exp(La * dt), np.exp(La * dt / 2)
        w, a = self.w, self.a
        k1w, k1a = self.nonlinear(w, a)
        k2w, k2a = self.nonlinear(Ew2 * (w + 0.5 * dt * k1w), Ea2 * (a + 0.5 * dt * k1a))
        k3w, k3a = self.nonlinear(Ew2 * w + 0.5 * dt * k2w, Ea2 * a + 0.5 * dt * k2a)
        k4w, k4a = self.nonlinear(Ew * w + dt * Ew2 * k3w, Ea * a + dt * Ea2 * k3a)
        w = Ew * w + dt / 6 * (Ew * k1w + 2 * Ew2 * (k2w + k3w) + k4w)
        a = Ea * a + dt / 6 * (Ea * k1a + 2 * Ea2 * (k2a + k3a) + k4a)
        self.w = w + dt * self._noise(self.sig_u, dt)
        self.a = a + dt * self._noise(self.sig_b, dt)
        self.w[:, 0, 0] = 0
        self.a[:, 0, 0] = 0

    def injection_rate(self, dt=1e-2, n_draw=200):
        """Exact mean injection rate (Itô) of the two forcings, estimated over noise draws."""
        wt = self._weights()
        n4 = self.n ** 4
        eu, eb = 0.0, 0.0
        for _ in range(n_draw):
            dw = dt * self._noise(self.sig_u, dt)
            da = dt * self._noise(self.sig_b, dt)
            eu += np.mean(0.5 * np.sum(wt * self.k2i * np.abs(dw) ** 2, axis=(-2, -1)) / n4) / dt
            eb += np.mean(0.5 * np.sum(wt * self.k2 * np.abs(da) ** 2, axis=(-2, -1)) / n4) / dt
        return eu / n_draw, eb / n_draw

    def injection_rates_all(self, dt=1e-2, n_draw=400):
        """Injection rate (Itô) of ½⟨|u|²⟩, ½⟨|B|²⟩ and ½⟨a²⟩ by the white forcing."""
        wt = self._weights()
        n4 = self.n ** 4
        eu = eb = ea = 0.0
        for _ in range(n_draw):
            dw = dt * self._noise(self.sig_u, dt)
            da = dt * self._noise(self.sig_b, dt)
            eu += np.mean(0.5 * np.sum(wt * self.k2i * np.abs(dw) ** 2, axis=(-2, -1)) / n4) / dt
            eb += np.mean(0.5 * np.sum(wt * self.k2 * np.abs(da) ** 2, axis=(-2, -1)) / n4) / dt
            ea += np.mean(0.5 * np.sum(wt * np.abs(da) ** 2, axis=(-2, -1)) / n4) / dt
        return eu / n_draw, eb / n_draw, ea / n_draw

    # -- diagnostics ------------------------------------------------------------------
    def diagnostics(self, w=None, a=None):
        w = self.w if w is None else w
        a = self.a if a is None else a
        wt = self._weights()
        n4 = self.n ** 4
        m = lambda f: np.sum(wt * np.abs(f) ** 2, axis=(-2, -1)) / n4   # ⟨f²⟩ (Parseval)
        Eu = 0.5 * m(w * np.sqrt(self.k2i))
        Eb = 0.5 * m(a * np.sqrt(self.k2))
        Zw = m(w)
        Jj = m(self.k2 * a)
        diss = self.nu * Zw + self.eta * Jj + self.alpha * 2 * Eu + self.alpha * 2 * Eb
        return {"Eu": Eu, "Eb": Eb, "enstrophie": Zw, "j2": Jj, "dissipation": diss}


def leray_project(ux, uy):
    """Leray projection of a periodic 2D field onto divergence-free fields (in Fourier space)."""
    n = ux.shape[-1]
    k = np.fft.fftfreq(n, 1.0 / n)
    kx, ky = np.meshgrid(k, k)
    k2 = kx ** 2 + ky ** 2
    k2[0, 0] = 1.0
    fx, fy = np.fft.fft2(ux), np.fft.fft2(uy)
    div = kx * fx + ky * fy
    fx = fx - kx * div / k2
    fy = fy - ky * div / k2
    return np.real(np.fft.ifft2(fx)), np.real(np.fft.ifft2(fy))
