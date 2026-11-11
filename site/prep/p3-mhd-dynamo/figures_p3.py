"""Static figures of module p3 (MHD and dynamo theory).

Usage: python3 figures_p3.py [out_dir]     (default: the figures/ folder next to this script)
Each data figure reuses the code block of the page that precedes it; the numbers quoted in the
captions are printed. The VKS diagram uses the dimensions of docs/specs/sources/dynamo.md §1.3.
Runs on CPU in about two minutes.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import spherical_jn as jn

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patches  # noqa: E402

fs.use(10)
HERE = Path(__file__).resolve().parent
PI_TICKS = ([0, np.pi, 2 * np.pi], ["0", "π", "2π"])


# ---------------------------------------------------------------------------------------------
def expulsion(Rm, N=128, T=60.0, dt=0.04):
    """Code of the page (section 2): uniform field B0 = (1, 0) in the cellular flow psi = sin x sin y.
    Returns the steady potential a = y + a' on the grid and the final energy <B²>."""
    eta = 1.0 / Rm
    x = np.arange(N) * 2 * np.pi / N
    X, Y = np.meshgrid(x, x, indexing="ij")
    ux, uy = np.sin(X) * np.cos(Y), -np.cos(X) * np.sin(Y)
    KX, KY = np.meshgrid(np.fft.fftfreq(N, 1 / N), np.fft.rfftfreq(N, 1 / N), indexing="ij")
    K2 = KX ** 2 + KY ** 2
    keep = (np.abs(KX) < N / 3) & (KY < N / 3)
    F, iF = np.fft.rfft2, lambda h: np.fft.irfft2(h, s=(N, N))

    def rhs(ah):
        return -F(ux * iF(1j * KX * ah) + uy * iF(1j * KY * ah) + uy) * keep

    E = np.exp(-eta * K2 * dt / 2)
    ah = np.zeros(K2.shape, complex)
    for _ in range(int(round(T / dt))):
        k1 = rhs(ah)
        k2 = rhs(E * (ah + dt / 2 * k1))
        k3 = rhs(E * ah + dt / 2 * k2)
        k4 = rhs(E ** 2 * ah + dt * E * k3)
        ah = E ** 2 * ah + dt / 6 * (E ** 2 * k1 + 2 * E * (k2 + k3) + k4)
    bx, by = 1 + iF(1j * KY * ah), -iF(1j * KX * ah)
    return X, Y, Y + iF(ah), float((bx ** 2 + by ** 2).mean())


def fig_expulsion(out):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.3))
    for a, Rm in zip(ax, (10, 40, 160)):
        X, Y, A, e = expulsion(Rm)
        print(f"expulsion: Rm = {Rm}, <B²>/B0² = {e:.2f} (128² grid)")
        a.contour(X, Y, np.sin(X) * np.sin(Y), levels=np.linspace(-0.9, 0.9, 6), colors=fs.LIGHT, linewidths=0.8, linestyles="solid")
        a.contour(X, Y, A, levels=np.linspace(0, 2 * np.pi, 25)[1:-1], colors=fs.C1, linewidths=1.1, linestyles="solid")
        a.set_aspect("equal"); a.grid(False); a.set_title(f"Rm = {Rm}")
        a.set_xticks(*PI_TICKS); a.set_yticks(*PI_TICKS); a.set_xlabel("x")
    ax[0].set_ylabel("y")
    fig.suptitle("Steady field lines (blue) in the cellular flow ψ = sin x sin y (grey)")
    fig.tight_layout()
    fs.save(fig, out / "expulsion.png")


# ---------------------------------------------------------------------------------------------
def fig_modes_sphere(out):
    conditions = {
        "insulator (vacuum)": lambda x: jn(0, x),
        "pseudo-vacuum: zero tangential B": lambda x: x * jn(0, x) - jn(1, x),
        "perfect conductor: B·n = 0": lambda x: jn(1, x),
    }
    roots = {}
    for name, g in conditions.items():
        xs = np.linspace(0.5, 6, 2000)
        i = np.where(np.sign(g(xs[:-1])) != np.sign(g(xs[1:])))[0][0]
        roots[name] = brentq(g, xs[i], xs[i + 1])
        print(f"modes-sphere: {name}: kR = {roots[name]:.4f}")
    # meridional plane (s = r sin(theta), z); flux function Psi = r f(r) sin²(theta), R = 1
    s, z = np.meshgrid(np.linspace(-2.2, 2.2, 501), np.linspace(-2.2, 2.2, 501))
    r = np.hypot(s, z)
    sin2 = np.where(r > 0, (s / np.where(r > 0, r, 1)) ** 2, 0)
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.6))
    for a, (name, kR) in zip(ax, roots.items()):
        f_in = jn(1, kR * r)
        psi = r * f_in * sin2
        if name.startswith("insulator"):
            psi = np.where(r <= 1, psi, jn(1, kR) / np.where(r > 0, r, 1) * sin2)   # f = f(R) R²/r² outside
        else:
            psi = np.where(r <= 1, psi, np.nan)
            a.add_patch(patches.Rectangle((-2.2, -2.2), 4.4, 4.4, color="#eeedea", zorder=0))
            a.add_patch(patches.Circle((0, 0), 1, color="white", zorder=0))
            a.text(0, -1.7, "wall with μr → ∞" if name.startswith("pseudo") else "perfect conductor",
                   ha="center", color=fs.INK2, fontsize=9)
        lev = np.abs(np.nanmax(np.abs(psi[np.abs(r - 0.5) < 0.6])))
        levels = np.linspace(-lev, lev, 22)
        levels = levels[np.abs(levels) > 1e-9]
        a.contour(s, z, psi, levels=levels, colors=fs.C1, linewidths=1.2, linestyles="solid")
        a.add_patch(patches.Circle((0, 0), 1, fill=False, lw=1.8, color=fs.INK))
        a.annotate("", xy=(0, 2.05), xytext=(0, 1.6), arrowprops=dict(arrowstyle="-|>", color=fs.INK2))
        a.text(0.08, 1.95, "z", color=fs.INK2, fontsize=9)
        a.set_xlim(-2.2, 2.2); a.set_ylim(-2.2, 2.2); a.set_aspect("equal"); a.axis("off")
        a.set_title(f"{name}\nkR = {kR:.3f}")
    fig.suptitle("Slowest dipolar free-decay mode of a conducting sphere (B lines, meridional plane)")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fs.save(fig, out / "modes-sphere.png")


# ---------------------------------------------------------------------------------------------
def fig_alpha2(out):
    def operator(C, N=200):
        h = 1.0 / N
        Id = np.eye(N - 1)
        D1 = (np.eye(N - 1, k=1) - np.eye(N - 1, k=-1)) / (2 * h)
        D2 = (np.eye(N - 1, k=1) - 2 * Id + np.eye(N - 1, k=-1)) / h ** 2
        return np.block([[D2, -C * D1], [C * D1, D2]])

    def rate(C):
        return np.linalg.eigvals(operator(C)).real.max()

    def saturate(C, N=32, T=12.0, dt=1e-3, seed=0):
        k = 2 * np.pi * np.fft.rfftfreq(N, 1.0 / N)
        rng = np.random.default_rng(seed)
        bx, by = 1e-3 * rng.standard_normal(N), 1e-3 * rng.standard_normal(N)
        E = np.exp(-k ** 2 * dt)
        phi = np.where(k > 0, (1 - E) / np.where(k > 0, k ** 2, 1), dt)
        for _ in range(int(T / dt)):
            a = C / (1 + bx ** 2 + by ** 2)
            fx, fy = np.fft.rfft(bx), np.fft.rfft(by)
            nx = -1j * k * np.fft.rfft(a * by)
            ny = 1j * k * np.fft.rfft(a * bx)
            bx = np.fft.irfft(E * fx + phi * nx, N)
            by = np.fft.irfft(E * fy + phi * ny, N)
        return (bx ** 2 + by ** 2).mean()

    Cc = brentq(rate, 4.0, 8.0, xtol=1e-6)
    print(f"alpha2: numerical threshold C_c = {Cc:.4f} (2 pi = {2 * np.pi:.4f})")
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    C = np.linspace(0, 13, 200)
    ax[0].plot(C, C ** 2 / 4 - np.pi ** 2, color=fs.C1, label="theory n = 1: C²/4 − π²")
    ax[0].plot(C, C ** 2 / 4 - 4 * np.pi ** 2, color=fs.C2, label="theory n = 2: C²/4 − 4π²")
    Cn = np.arange(1.0, 13.0)
    ax[0].plot(Cn, [rate(c) for c in Cn], "o", mfc="white", mec=fs.INK, mew=1.5, label="finite differences")
    ax[0].axhline(0, color=fs.INK2, lw=0.8); ax[0].axvline(2 * np.pi, color=fs.INK2, lw=0.8, ls=":")
    ax[0].text(2 * np.pi + 0.15, -39, "2π", color=fs.INK2)
    ax[0].set_ylim(-42, 32); ax[0].legend(loc="upper left", fontsize=9)
    ax[0].set_xlabel(r"$C = \alpha L/\eta_T$"); ax[0].set_ylabel(r"growth rate $\lambda L^2/\eta_T$")
    ax[0].set_title("Slab with B = 0 at walls: threshold C = 2π")
    ax[1].plot(C, np.maximum(C / (2 * np.pi) - 1, 0), color=fs.C1, label="theory C/2π − 1")
    Cs = np.array([5, 6, 6.6, 7, 8, 9, 10, 11, 12])
    sat = [saturate(c, T=40.0 if c < 7.5 else 12.0) for c in Cs]
    for c, m in zip(Cs, sat):
        print(f"alpha2: C = {c:4.1f}  saturated <B²> = {m:.4f}  theory {max(c / (2 * np.pi) - 1, 0):.4f}")
    ax[1].plot(Cs, sat, "o", mfc="white", mec=fs.INK, mew=1.5, label="simulation (α = C/(1 + |B|²))")
    ax[1].axvline(2 * np.pi, color=fs.INK2, lw=0.8, ls=":")
    ax[1].legend(loc="upper left", fontsize=9)
    ax[1].set_xlabel(r"$C = \alpha L/\eta_T$"); ax[1].set_ylabel(r"saturated $\langle|B|^2\rangle\,/\,B^2_\mathrm{eq}$")
    ax[1].set_title("Periodic box: saturation (pitchfork)")
    fig.tight_layout()
    fs.save(fig, out / "alpha2.png")


# ---------------------------------------------------------------------------------------------
def fig_vks(out):
    """Schematic meridional cut, in mm (axis horizontal); proportions approximate."""
    fig, ax = plt.subplots(figsize=(13, 5.6))
    ax.set_xlim(-330, 900); ax.set_ylim(-330, 330); ax.set_aspect("equal"); ax.axis("off")
    copper, sodium = "#b87333", "#e8f0fa"
    ax.add_patch(patches.Rectangle((-302, -289), 604, 578, fc="#f3efe8", ec=copper, lw=4))
    ax.add_patch(patches.Rectangle((-262, -206), 524, 412, fc=sodium, ec=fs.INK2, lw=2))
    ax.plot([-320, 320], [0, 0], ls="--", color=fs.INK2, lw=1)
    ax.text(325, 0, "axis", va="center", color=fs.INK2, fontsize=9)
    for sgn in (-1, 1):
        xd = sgn * 185.5                                     # discs 371 mm apart
        ax.plot([xd, xd], [-154.5, 154.5], color="#333", lw=4)
        ax.plot([sgn * 185.5, sgn * 278], [0, 0], color="#555", lw=5)
        for y in np.linspace(-138, 138, 6):
            ax.plot([xd, xd - sgn * 41.2], [y, y], color="#888", lw=5)
    ax.plot([0, 0], [175, 206], color=fs.INK2, lw=3); ax.plot([0, 0], [-206, -175], color=fs.INK2, lw=3)
    loop_kw = dict(color=fs.C1, lw=1.6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, x1 = sorted((sx * 20, sx * 150)); y0, y1 = sorted((sy * 20, sy * 170))
            ax.add_patch(patches.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, **loop_kw))
            ccw = sx * sy < 0                               # sense of the poloidal cell
            for (xa, ya, dx, dy) in [((x0 + x1) / 2, y1, 1, 0), ((x0 + x1) / 2, y0, -1, 0),
                                     (x0, (y0 + y1) / 2, 0, -1), (x1, (y0 + y1) / 2, 0, 1)]:
                d = -1 if ccw else 1
                ax.annotate("", xy=(xa + 8 * dx * d, ya + 8 * dy * d), xytext=(xa, ya),
                            arrowprops=dict(arrowstyle="-|>", color=fs.C1, lw=1.4))
    for (x, y, sym) in [(-230, 180, "⊙"), (230, 180, "⊗"), (-230, -180, "⊗"), (230, -180, "⊙")]:
        ax.text(x, y, sym, ha="center", va="center", color=fs.C2, fontsize=14, family="DejaVu Sans")
    ax.annotate("", xy=(100, -12), xytext=(-100, -12), arrowprops=dict(arrowstyle="-|>", color="#e34948", lw=3))
    ax.annotate("", xy=(-185.5, -245), xytext=(185.5, -245), arrowprops=dict(arrowstyle="<->", color=fs.INK2))
    ax.text(0, -265, "371 mm", ha="center", va="top", color=fs.INK2, fontsize=9)
    marks = {1: (-280, 265), 2: (-245, -100), 3: (205, 80), 4: (255, 180), 5: (95, 110), 6: (25, -185), 7: (0, -50)}
    for n, (x, y) in marks.items():
        ax.text(x, y, str(n), ha="center", va="center", color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc=fs.INK, ec="white"))
    legend = [
        "copper envelope, inner radius 289 mm: sodium at rest",
        "inner cylinder, R = 206 mm: sodium set in motion",
        "soft-iron impellers (μr of order 50 to 100): disks of radius 154.5 mm,\n8 curved blades of 41.2 mm; 371 mm between the disks",
        "counter-rotation of the two impellers, frequencies F₁ and F₂ (⊙: towards the reader)",
        "poloidal recirculation of the mean flow (4 cells)",
        "thin annulus in the mid-plane",
        "generated mean field: axial dipole, mostly axisymmetric",
    ]
    for i, txt in enumerate(legend):
        y = 250 - i * 78
        ax.text(390, y, str(i + 1), ha="center", va="center", color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc=fs.INK, ec="white"))
        ax.text(420, y, txt, va="center", fontsize=9.5, color=fs.INK)
    ax.set_title("VKS experiment (Cadarache): schematic meridional cut", fontsize=12)
    fs.save(fig, out / "vks.png")


# ---------------------------------------------------------------------------------------------
def fig_gissinger(out):
    """Code of the page (section 7): 4 trajectories per Gamma, reversals counted with the ±0.5 threshold."""
    mu, nu = 0.119, 0.1
    gammas = np.array([0.80, 0.84, 0.86, 0.87, 0.88, 0.90, 0.95, 1.00])

    def F(X, G):
        Q, D, V = X
        return np.array([mu * Q - V * D, -nu * D + V * Q, G - V + Q * D])

    rng = np.random.default_rng(0)
    Gv = np.repeat(gammas, 4)
    X = rng.normal(size=(3, Gv.size)) * 0.8
    X[2] = np.abs(X[2])
    dt, T, T0 = 0.02, 5000.0, 500.0
    last = np.zeros(Gv.size); nrev = np.zeros(Gv.size, int)
    i86, i90 = np.flatnonzero(Gv == 0.86)[0], np.flatnonzero(Gv == 0.90)[0]
    ts, d86, d90 = [], [], []
    for i in range(int(T / dt)):
        k1 = F(X, Gv); k2 = F(X + dt / 2 * k1, Gv); k3 = F(X + dt / 2 * k2, Gv); k4 = F(X + dt * k3, Gv)
        X = X + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if i * dt >= T0:
            p = np.where(X[1] > 0.5, 1.0, np.where(X[1] < -0.5, -1.0, 0.0))
            nrev += (p != 0) & (last != 0) & (p != last)
            last = np.where(p != 0, p, last)
            if i % 5 == 0:
                ts.append((i + 1) * dt); d86.append(X[1, i86]); d90.append(X[1, i90])
    per1000 = nrev.reshape(-1, 4).sum(1) / (4 * (T - T0)) * 1000
    for g, r in zip(gammas, nrev.reshape(-1, 4).sum(1)):
        print(f"gissinger: Gamma = {g:.2f}: {r} reversals over 18000 time units")
    fig = plt.figure(figsize=(12, 4.6))
    gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 0.9])
    a1, a2, a3 = fig.add_subplot(gs[0, :2]), fig.add_subplot(gs[1, :2]), fig.add_subplot(gs[:, 2])
    a1.plot(ts, d86, color=fs.C1, lw=0.7); a1.set_title("Γ = 0.86: chaos without reversals", loc="left")
    a2.plot(ts, d90, color=fs.C2, lw=0.7); a2.set_title("Γ = 0.90: chaotic reversals", loc="left")
    for a in (a1, a2):
        a.axhline(0, color=fs.INK2, lw=0.8); a.set_ylim(-3.3, 3.3); a.set_ylabel("dipole D")
    a1.set_xticklabels([]); a2.set_xlabel("time t")
    a3.axvspan(0.795, 0.865, color="#e4e3df", lw=0)
    a3.plot(gammas, per1000, "o-", color=fs.C1, mfc="white", mew=1.5)
    a3.set_xlabel("Γ"); a3.set_ylabel("reversals per 1000 time units")
    fig.tight_layout()
    fs.save(fig, out / "gissinger.png")


if __name__ == "__main__":
    out = fs.out_dir(str(HERE / "figures" / "x"), sys.argv)
    for fn in (fig_expulsion, fig_modes_sphere, fig_alpha2, fig_vks, fig_gissinger):
        fn(out)
