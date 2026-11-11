"""Static figures of module p2 (fluid mechanics, reference flows, turbulence).

Usage: python3 figures_p2.py [out_dir]     (default: the folder of this script)
lagrange and kolmogorov64 rerun the code blocks of the page (sections 1 and 7); the model spectrum is
that of Pope (2000) used by the interactive diagram of section 6 (C = 1.5, p0 = 2, c_L = 6.78,
beta = 5.2, c_eta = 0.40); the VKS panel uses a model stream function and the dimensions of
docs/specs/sources/dynamo.md §1.3. Prints the numbers quoted in the captions. Runs in about a minute.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patches  # noqa: E402

fs.use(10)
HERE = Path(__file__).resolve().parent
PI_TICKS = ([0, np.pi, 2 * np.pi], ["0", "π", "2π"])


def rk4(f, x, h):
    k1 = f(x); k2 = f(x + h / 2 * k1); k3 = f(x + h / 2 * k2); k4 = f(x + h * k3)
    return x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# ---------------------------------------------------------------------------------------------
def fig_lagrange(out):
    """Square blob [0.3, 0.8] x [1.1, 1.6] advected by the cellular flow, without and with a divergent part."""
    def u_sol(p):
        x, y = p[..., 0], p[..., 1]
        return np.stack([np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)], -1)

    def u_div(p):
        return u_sol(p) + 0.35 * np.stack([np.sin(p[..., 0]), np.sin(p[..., 1])], -1)

    s = np.linspace(0, 1, 401)[:-1]
    side = [np.stack([0.3 + 0.5 * s, 1.1 + 0 * s], 1), np.stack([0.8 + 0 * s, 1.1 + 0.5 * s], 1),
            np.stack([0.8 - 0.5 * s, 1.6 + 0 * s], 1), np.stack([0.3 + 0 * s, 1.6 - 0.5 * s], 1)]
    blob = np.concatenate(side)

    def area(c):
        x, y = c[:, 0], c[:, 1]
        return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

    xg = np.linspace(0, np.pi, 200)
    X, Y = np.meshgrid(xg, xg)
    blues = ["#a5c8f0", "#5b9ae6", fs.C1, "#1b4f93"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.6))
    for a, field, title in ((ax[0], u_sol, "(a) ∇·u = 0: material area is conserved"),
                            (ax[1], u_div, "(b) ∇·u ≠ 0: area changes")):
        a.contour(X, Y, np.sin(X) * np.sin(Y), levels=np.linspace(0.1, 0.9, 9), colors=fs.LIGHT, linewidths=0.8)
        c, areas = blob.copy(), []
        for t in range(4):
            if t:
                for _ in range(400):
                    c = rk4(field, c, 1 / 400)
            areas.append(area(c))
            a.fill(c[:, 0], c[:, 1], color=blues[t], alpha=0.35 + 0.1 * t, lw=0)
            a.plot(np.r_[c[:, 0], c[0, 0]], np.r_[c[:, 1], c[0, 1]], color=blues[t], lw=2,
                   label=f"t = {t}: area = {areas[-1]:.4f}")
        print(f"lagrange: {title[:3]} areas {', '.join(f'{v:.4f}' for v in areas)}")
        a.set_xlim(0, np.pi + 0.1); a.set_ylim(0, np.pi + 0.1); a.set_aspect("equal")
        a.set_xlabel("x"); a.set_ylabel("y"); a.set_title(title); a.legend(loc="upper right", fontsize=8.5, frameon=True)
        a.grid(False)
    fig.tight_layout()
    fs.save(fig, out / "lagrange.png")


# ---------------------------------------------------------------------------------------------
def abc(p, A=1.0, B=np.sqrt(2 / 3), C=np.sqrt(1 / 3)):
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    return np.stack([A * np.sin(z) + C * np.cos(y), B * np.sin(x) + A * np.cos(z), C * np.sin(y) + B * np.cos(x)], -1)


def poincare(n_traj=90, T=2000.0, dt=0.05, seed=0):
    """Intersections with the planes z = 0 mod 2 pi (linear interpolation within the step)."""
    rng = np.random.default_rng(seed)
    p = np.column_stack([rng.uniform(0, 2 * np.pi, (n_traj, 2)), np.zeros(n_traj)])
    pts = []
    for _ in range(int(T / dt)):
        q = rk4(abc, p, dt)
        k0, k1 = np.floor(p[:, 2] / (2 * np.pi)), np.floor(q[:, 2] / (2 * np.pi))
        hit = k0 != k1
        if hit.any():
            zc = 2 * np.pi * np.maximum(k0, k1)[hit]
            lam = (zc - p[hit, 2]) / (q[hit, 2] - p[hit, 2])
            pts.append(p[hit, :2] + lam[:, None] * (q[hit, :2] - p[hit, :2]))
        p = q
    return np.mod(np.concatenate(pts), 2 * np.pi)


def fig_flows(out):
    fig, ax = plt.subplots(2, 3, figsize=(12.5, 8.6))
    # (a) plane Poiseuille
    a = ax[0, 0]
    y = np.linspace(-1, 1, 200)
    a.plot(1 - y ** 2, y, color=fs.C1)
    for yy in np.linspace(-0.8, 0.8, 9):
        a.annotate("", xy=(1 - yy ** 2, yy), xytext=(0.05, yy), arrowprops=dict(arrowstyle="-|>", color=fs.INK2, lw=1))
    for yy in (-1, 1):
        a.axhline(yy, color=fs.INK, lw=3)
        a.text(1.75, yy + (0.08 if yy > 0 else -0.08), "wall (no slip)", ha="right", va="center", fontsize=8.5)
    a.text(1.05, 0.55, "U(y) = G(h² − y²)/(2ν)", fontsize=9)
    a.set_xlim(-0.05, 1.8); a.set_ylim(-1.25, 1.25); a.set_xlabel("U / U_max"); a.set_ylabel("y / h")
    a.set_title("(a) Plane Poiseuille")
    xg = np.linspace(0, 2 * np.pi, 96)
    X, Y = np.meshgrid(xg, xg)
    # (b) Taylor–Green
    a = ax[0, 1]
    psi = np.sin(X) * np.sin(Y)
    a.imshow(2 * psi, extent=(0, 2 * np.pi, 0, 2 * np.pi), origin="lower", cmap=fs.DIVERGING, vmin=-2.2, vmax=2.2)
    a.streamplot(X, Y, np.sin(X) * np.cos(Y), -np.cos(X) * np.sin(Y), color=fs.INK, density=0.9, linewidth=0.8)
    a.set_title("(b) 2D Taylor–Green: ψ and ω")
    # (c) laminar Kolmogorov
    a = ax[0, 2]
    a.imshow(np.sin(4 * Y), extent=(0, 2 * np.pi, 0, 2 * np.pi), origin="lower", cmap=fs.DIVERGING, vmin=-1.3, vmax=1.3)
    yq = np.linspace(0.1, 2 * np.pi - 0.1, 24)
    for x0 in (np.pi / 3, 4 * np.pi / 3):
        a.quiver(np.full_like(yq, x0), yq, np.sin(4 * yq), 0 * yq, scale=6, width=0.006, color=fs.INK)
        a.plot(x0 + 0.9 * np.sin(4 * xg), xg, color=fs.INK, lw=0.8)
    a.set_title("(c) Laminar Kolmogorov: uₓ = sin(4y)")
    # (d) ABC slice z = 0
    a = ax[1, 0]
    P = np.stack([X, Y, np.zeros_like(X)], -1)
    U = abc(P)
    a.imshow(U[..., 2], extent=(0, 2 * np.pi, 0, 2 * np.pi), origin="lower", cmap=fs.DIVERGING, vmin=-1.6, vmax=1.6)
    s = slice(3, None, 8)
    a.quiver(X[s, s], Y[s, s], U[s, s, 0], U[s, s, 1], color=fs.INK, scale=22, width=0.005)
    a.set_title("(d) ABC, slice z = 0: u_z (colour), (uₓ, u_y)")
    # (e) Poincaré section
    a = ax[1, 1]
    pts = poincare()
    print(f"flows: Poincaré section, {len(pts)} points from 90 trajectories")
    a.scatter(pts[:, 0], pts[:, 1], s=0.15, color=fs.C1, lw=0)
    a.set_title("(e) ABC, Poincaré section z ≡ 0")
    for a in (ax[0, 1], ax[0, 2], ax[1, 0], ax[1, 1]):
        a.set_xlim(0, 2 * np.pi); a.set_ylim(0, 2 * np.pi); a.set_aspect("equal"); a.grid(False)
        a.set_xticks(*PI_TICKS); a.set_yticks(*PI_TICKS); a.set_xlabel("x"); a.set_ylabel("y")
    # (f) VKS meridional plane: model stream function, 4 poloidal cells, dimensions in mm
    a = ax[1, 2]
    R, H = 206.0, 185.5                                    # cylinder radius, half distance between the disks
    r = np.linspace(-R, R, 160); z = np.linspace(-H, H, 160)
    Rg, Zg = np.meshgrid(r, z)
    psi = np.sin(np.pi * Rg / R) * np.sin(np.pi * Zg / H)  # vanishes on the axis, the wall, the disks and z = 0
    ur, uz = -np.pi / H * np.sin(np.pi * Rg / R) * np.cos(np.pi * Zg / H), np.pi / R * np.cos(np.pi * Rg / R) * np.sin(np.pi * Zg / H)
    # with this sign the fluid is drawn along the axis towards each impeller, ejected radially along the
    # disk and returns along the wall to the mid-plane (u_z > 0 on the axis for z > 0)
    a.streamplot(Rg, Zg, ur, uz, color=fs.C1, density=1.0, linewidth=1.1)
    for zz in (H, -H):
        a.add_patch(patches.Rectangle((-R, zz if zz > 0 else -H - 50), 2 * R, 50, color="#e4e3df", lw=0))
        a.plot([-154.5, 154.5], [zz, zz], color=fs.INK, lw=4)
        for rb in np.linspace(-130, 130, 6):
            a.plot([rb, rb], [zz, zz - np.sign(zz) * 41.2], color=fs.INK, lw=1.2)
        a.text(0, zz + np.sign(zz) * 30, f"impeller ({'+' if zz > 0 else '−'}F)", ha="center", va="center", fontsize=8.5)
    a.add_patch(patches.Rectangle((-R, -H - 50), 2 * R, 2 * H + 100, fill=False, ec=fs.INK, lw=1.5))
    a.axhline(0, color=fs.C2, ls="--", lw=1.6); a.text(R - 5, 12, "shear layer", ha="right", fontsize=8.5)
    a.axvline(0, color=fs.INK2, ls=":", lw=1)
    for (rx, zx, sym) in [(-110, 95, "⊗"), (110, 95, "⊙"), (-110, -95, "⊙"), (110, -95, "⊗")]:
        a.text(rx, zx, sym, ha="center", va="center", fontsize=20, family="DejaVu Sans")
    a.set_xlim(-R - 10, R + 10); a.set_ylim(-H - 60, H + 60); a.set_aspect("equal"); a.grid(False)
    a.set_xlabel("r (mm)"); a.set_ylabel("z (mm)"); a.set_title("(f) von Kármán (VKS), meridional plane")
    fig.tight_layout()
    fs.save(fig, out / "flows.png")


# ---------------------------------------------------------------------------------------------
def pope_spectrum(k, eta, C=1.5, p0=2.0, cL=6.78, beta=5.2, ceta=0.40):
    """Model spectrum of Pope (2000) with epsilon = L = 1."""
    fL = (k / np.sqrt(k ** 2 + cL)) ** (5 / 3 + p0)
    feta = np.exp(-beta * ((((k * eta) ** 4) + ceta ** 4) ** 0.25 - ceta))
    return C * k ** (-5 / 3) * fL * feta


def fig_cascade(out):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    a = ax[0]
    k = np.logspace(-1.5, 5, 600)
    a.axvspan(10 ** -1.5, 2 * np.pi, color=fs.C1, alpha=0.1, lw=0)
    a.axvspan(1e3, 1e5, color=fs.C2, alpha=0.1, lw=0)
    for LE, col in ((1e2, "#5b9ae6"), (1e4, "#1b4f93")):
        a.loglog(k, pope_spectrum(k, 1 / LE), color=col, label=f"L/η = 10{'²' if LE == 1e2 else '⁴'}")
    kk = np.logspace(0.3, 3.4, 10)
    a.loglog(kk, 1.5 * kk ** (-5 / 3) * 3, "--", color=fs.INK2, lw=1.2)
    a.text(80, 1.5 * 80 ** (-5 / 3) * 9, r"$k^{-5/3}$", color=fs.INK2)
    a.annotate("", xy=(800, 1e-5 * 1.2), xytext=(90, 1e-5 * 1.2), arrowprops=dict(arrowstyle="-|>", color=fs.C2, lw=2))
    a.text(80, 1.2e-5, "energy flux ε ", ha="right", va="center", fontsize=9)
    for x, txt in ((0.4, "large scales\n(injection)"), (60, "inertial range\n(L/η = 10⁴)"), (3e4, "dissipation\n(L/η = 10⁴)")):
        a.text(x, 3e-9, txt, ha="center", fontsize=9, bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    a.set_ylim(1e-10, 30); a.set_xlim(10 ** -1.5, 1e5); a.legend(loc="upper right", fontsize=9)
    a.set_xlabel("k L"); a.set_ylabel("E(k)  (ε = L = 1)"); a.set_title("(a) 3D turbulence: model spectrum (Pope, 2000)")
    # (b) sketch of the dual cascade: theoretical slopes only
    b = ax[1]
    kf = 30.0
    k1, k2 = np.logspace(0, np.log10(kf), 50), np.logspace(np.log10(kf), 3, 50)
    b.loglog(k1, (k1 / kf) ** (-5 / 3), color=fs.C1); b.loglog(k2, (k2 / kf) ** -3.0, color=fs.C3)
    b.axvline(kf, color=fs.INK2, ls=":", lw=1); b.text(kf * 1.05, 40, "forcing k_f", color=fs.INK2, fontsize=9)
    b.text(3, 10, r"$k^{-5/3}$"); b.text(200, 1e-2, r"$k^{-3}$")
    b.annotate("", xy=(1.6, 3e-3), xytext=(6, 3e-3), arrowprops=dict(arrowstyle="-|>", color=fs.C1, lw=2))
    b.text(7, 3e-3, "inverse\nenergy cascade", va="center", fontsize=9)
    b.annotate("", xy=(900, 10), xytext=(150, 10), arrowprops=dict(arrowstyle="-|>", color=fs.C3, lw=2))
    b.text(140, 10, "direct enstrophy\ncascade", ha="right", va="center", fontsize=9)
    b.set_xlim(1, 1e3); b.set_ylim(1e-5, 200)
    b.set_xlabel("k"); b.set_ylabel("E(k) / E(k_f)"); b.set_title("(b) 2D turbulence: dual cascade (Kraichnan, 1967)")
    fig.tight_layout()
    fs.save(fig, out / "cascade.png")


# ---------------------------------------------------------------------------------------------
def kolmogorov():
    """Solver of the page (section 7): Re = 40, n_f = 4, 64², spin-up 50, average over 200 time units."""
    N, n_f, Re = 64, 4, 40.0
    nu = 1.0 / Re
    L = 2 * np.pi
    x = np.arange(N) * L / N
    X, Y = np.meshgrid(x, x, indexing="xy")
    KX, KY = np.meshgrid(np.fft.rfftfreq(N, 1.0 / N), np.fft.fftfreq(N, 1.0 / N))
    K2 = KX ** 2 + KY ** 2
    K2inv = np.where(K2 > 0, 1.0 / np.where(K2 > 0, K2, 1.0), 0.0)
    dealias = (np.abs(KX) < N / 3) & (np.abs(KY) < N / 3)
    fx = np.sin(n_f * Y)
    f_w = np.fft.rfft2(-n_f * np.cos(n_f * Y))

    def velocity(wh):
        ph = wh * K2inv
        return np.fft.irfft2(1j * KY * ph, s=(N, N)), np.fft.irfft2(-1j * KX * ph, s=(N, N))

    def rhs_nl(wh):
        ux, uy = velocity(wh)
        wx = np.fft.irfft2(1j * KX * wh, s=(N, N)); wy = np.fft.irfft2(1j * KY * wh, s=(N, N))
        return -np.fft.rfft2(ux * wx + uy * wy) * dealias + f_w

    def budget(wh):
        ux, uy = velocity(wh)
        w = np.fft.irfft2(wh, s=(N, N))
        return 0.5 * np.mean(ux ** 2 + uy ** 2), np.mean(fx * ux), nu * np.mean(w ** 2)

    rng = np.random.default_rng(0)
    w0 = -(Re / n_f) * np.cos(n_f * Y) + 0.1 * rng.standard_normal((N, N))
    wh = np.fft.rfft2(w0) * dealias
    wh[0, 0] = 0.0
    dt, T_spin, T_avg = 0.02, 50.0, 200.0
    E_lin, E_half = np.exp(-nu * K2 * dt), np.exp(-nu * K2 * dt / 2)

    def step(wh):
        k1 = rhs_nl(wh)
        k2 = rhs_nl(E_half * (wh + 0.5 * dt * k1))
        k3 = rhs_nl(E_half * wh + 0.5 * dt * k2)
        k4 = rhs_nl(E_lin * wh + dt * E_half * k3)
        return E_lin * wh + dt / 6 * (E_lin * k1 + 2 * E_half * (k2 + k3) + k4)

    n_spin, n_avg = int(T_spin / dt), int(T_avg / dt)
    for _ in range(n_spin):
        wh = step(wh)
    hist = []
    spec = np.zeros(N // 2 + 1)
    shell = np.rint(np.sqrt(K2)).astype(int)
    wgt = np.where(KX == 0, 1.0, 2.0)
    for it in range(n_avg + 1):
        hist.append(budget(wh))
        if it % 50 == 0:
            uh2 = wgt * np.abs(wh) ** 2 * K2inv / N ** 4
            spec += 0.5 * np.bincount(shell.ravel(), uh2.ravel(), minlength=N)[: N // 2 + 1]
        if it < n_avg:
            wh = step(wh)
    E, P, D = np.array(hist).T
    return X, Y, np.fft.irfft2(wh, s=(N, N)), spec / (n_avg // 50 + 1), T_spin + dt * np.arange(n_avg + 1), P, D


def fig_kolmogorov(out):
    X, Y, w, Ek, t, P, D = kolmogorov()
    print(f"kolmogorov64: <P>_t = {P.mean():.4f}, <D>_t = {D.mean():.4f}, relative difference "
          f"{abs(P.mean() - D.mean()) / D.mean():.2%}; E(1) = {Ek[1]:.2e}, E(4) = {Ek[4]:.2e}, E(20) = {Ek[20]:.2e}; "
          f"P, D range {min(P.min(), D.min()):.2f}–{max(P.max(), D.max()):.2f}")
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.9), gridspec_kw={"width_ratios": [1.05, 1, 1.3]})
    m = np.abs(w).max()
    im = ax[0].imshow(w, extent=(0, 2 * np.pi, 0, 2 * np.pi), origin="lower", cmap=fs.DIVERGING, vmin=-m, vmax=m)
    fig.colorbar(im, ax=ax[0], fraction=0.046, pad=0.04)
    ax[0].set_xticks(*PI_TICKS); ax[0].set_yticks(*PI_TICKS); ax[0].grid(False)
    ax[0].set_xlabel("x"); ax[0].set_ylabel("y"); ax[0].set_title(f"(a) vorticity ω at t = {t[-1]:.0f}")
    k = np.arange(1, 22)
    ax[1].loglog(k, Ek[k], "o-", color=fs.C1, ms=4)
    ax[1].axvline(4, color=fs.INK2, ls=":", lw=1); ax[1].text(4.2, Ek[1] * 0.4, "k = n_f = 4", color=fs.INK2, fontsize=9)
    ax[1].set_xlabel("k"); ax[1].set_ylabel("E(k)"); ax[1].set_title("(b) mean spectrum (64², Re = 40)")
    ax[2].plot(t, P, color=fs.C1, lw=1.1, label="injection P(t) = ⟨f·u⟩")
    ax[2].plot(t, D, color=fs.C2, lw=1.1, label="dissipation ε(t) = ν⟨ω²⟩")
    ax[2].axhline(P.mean(), color=fs.C1, ls="--", lw=1); ax[2].axhline(D.mean(), color=fs.C2, ls="--", lw=1)
    ax[2].set_xlabel("t"); ax[2].legend(loc="upper left", fontsize=9)
    ax[2].set_title(f"(c) budget: P̄ = {P.mean():.4f}, ε̄ = {D.mean():.4f}")
    fig.tight_layout()
    fs.save(fig, out / "kolmogorov64.png")


if __name__ == "__main__":
    out = fs.out_dir(__file__, sys.argv)
    for fn in (fig_lagrange, fig_flows, fig_cascade, fig_kolmogorov):
        fn(out)
