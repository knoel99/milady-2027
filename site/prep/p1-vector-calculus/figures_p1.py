"""Static figures of module p1 (vector calculus, Fourier analysis, Helmholtz–Hodge decomposition).

Usage: python3 figures_p1.py [out_dir]     (default: the folder of this script)
The Fourier and stream-function figures reuse the code blocks of the page (sections 5 and 6); the
numbers quoted in the captions are printed. Runs on CPU in a few seconds.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patches  # noqa: E402

fs.use(10, **{"axes.titleweight": "bold"})
HERE = Path(__file__).resolve().parent


def _square(a, lim):
    a.set_xlim(-lim, lim); a.set_ylim(-lim, lim); a.set_aspect("equal")
    a.set_xticks([]); a.set_yticks([]); a.grid(False)
    for sp in a.spines.values():
        sp.set_visible(True); sp.set_color("#d4d4d4")


# ---------------------------------------------------------------------------------------------
def fig_fields(out):
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.6))
    x = np.linspace(-1, 1, 41)
    X, Y = np.meshgrid(x, x)
    fields = [("Source", r"$\nabla\cdot\mathbf{u} = 2,\ \ \omega = 0$", X, Y),
              ("Solid-body rotation", r"$\nabla\cdot\mathbf{u} = 0,\ \ \omega = 2$", -Y, X),
              ("Shear", r"$\nabla\cdot\mathbf{u} = 0,\ \ \omega = -1$", Y, 0 * X)]
    for a, (name, sub, U, V) in zip(ax, fields):
        a.streamplot(X, Y, U, V, color=fs.C1, density=1.3, linewidth=1.1, arrowsize=0.9)
        a.set_title(f"{name}\n{sub}"); _square(a, 1)
    # cellular flow on [0, 2 pi]², vorticity background
    x = np.linspace(0, 2 * np.pi, 81)
    X, Y = np.meshgrid(x, x)
    U, V = np.sin(X) * np.cos(Y), -np.cos(X) * np.sin(Y)
    a = ax[3]
    a.imshow(2 * np.sin(X) * np.sin(Y), extent=(0, 2 * np.pi, 0, 2 * np.pi), origin="lower", cmap=fs.DIVERGING,
             vmin=-4.5, vmax=4.5, interpolation="bilinear")
    a.streamplot(X, Y, U, V, color=fs.C1, density=1.2, linewidth=1.1, arrowsize=0.9)
    a.set_title("Cellular flow\n" + r"$\nabla\cdot\mathbf{u} = 0,\ \ \omega = 2\sin x\,\sin y$")
    a.set_xlim(0, 2 * np.pi); a.set_ylim(0, 2 * np.pi); a.set_aspect("equal")
    a.set_xticks([]); a.set_yticks([]); a.grid(False)
    for sp in a.spines.values():
        sp.set_visible(True); sp.set_color("#d4d4d4")
    fig.tight_layout()
    fs.save(fig, out / "fig-fields.png")


# ---------------------------------------------------------------------------------------------
def fig_monopole_dipole(out):
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 4.3))
    a = ax[0]
    for th in np.arange(16) * np.pi / 8:                     # radial lines of x/|x|³
        c, s = np.cos(th), np.sin(th)
        a.plot([0, 3 * c], [0, 3 * s], color=fs.C1, lw=1.2)
        a.annotate("", xy=(1.55 * c, 1.55 * s), xytext=(1.45 * c, 1.45 * s),
                   arrowprops=dict(arrowstyle="-|>", color=fs.C1, lw=1.2))
    a.plot(0, 0, "o", color=fs.INK, ms=7)
    a.set_title("Monopole (point charge)")
    # dipole m along z, cross-section: field lines r = c sin²(theta), theta measured from the z axis
    b = ax[1]
    th = np.linspace(1e-3, np.pi - 1e-3, 400)
    for cst in (0.35, 0.6, 0.9, 1.4, 2.2, 3.5):
        r = cst * np.sin(th) ** 2
        for side in (1, -1):
            xs, zs = side * r * np.sin(th), r * np.cos(th)
            b.plot(xs, zs, color=fs.C1, lw=1.2)
            k = len(th) // 2                                  # equator: field points towards -z
            b.annotate("", xy=(xs[k + 3], zs[k + 3]), xytext=(xs[k], zs[k]),
                       arrowprops=dict(arrowstyle="-|>", color=fs.C1, lw=1.2))
    b.annotate("", xy=(0, 0.2), xytext=(0, -0.15), arrowprops=dict(arrowstyle="-|>", color=fs.INK, lw=2.5))
    b.set_title("Magnetic dipole")
    for a_, label0 in ((a, r"flux $= 4\pi$"), (b, r"flux $= 0$")):
        a_.add_patch(patches.Circle((0, 0), 0.7, fill=False, ls="--", lw=1.8, color=fs.C2))
        a_.add_patch(patches.Circle((1.45, 1.4), 0.45, fill=False, ls="--", lw=1.8, color=fs.C2))
        a_.text(0, -0.85, label0, ha="center", va="top", bbox=dict(fc="white", ec="none", pad=1))
        a_.text(1.45, 0.82, r"flux $= 0$", ha="center", va="top", bbox=dict(fc="white", ec="none", pad=1))
        _square(a_, 2)
    fig.tight_layout()
    fs.save(fig, out / "fig-monopole-dipole.png")


# ---------------------------------------------------------------------------------------------
def fig_fourier(out):
    def wavenumbers(N, L=2 * np.pi):
        return 2 * np.pi * np.fft.fftfreq(N, d=L / N)

    def d_spectral(f):
        k = wavenumbers(f.size)
        if f.size % 2 == 0:
            k[f.size // 2] = 0.0
        return np.real(np.fft.ifft(1j * k * np.fft.fft(f)))

    def d_fd2(f):
        h = 2 * np.pi / f.size
        return (np.roll(f, -1) - np.roll(f, 1)) / (2 * h)

    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    x = np.linspace(0, 2 * np.pi, 1000)
    xg = 2 * np.pi * np.arange(8) / 8
    ax[0].plot(x, np.cos(10 * x), color=fs.C1, lw=1.4, label=r"$\cos(10x)$")
    ax[0].plot(x, np.cos(2 * x), "--", color=fs.C2, label=r"$\cos(2x)$")
    ax[0].plot(xg, np.cos(2 * xg), "o", color=fs.INK, ms=5, label="grid points", zorder=5)
    ax[0].set_xticks([0, np.pi, 2 * np.pi], ["0", "π", "2π"]); ax[0].set_ylim(-1.6, 1.25)
    ax[0].set_ylim(-1.75, 1.25)
    ax[0].legend(loc="lower center", fontsize=8.5, frameon=True, ncol=3, columnspacing=0.8, handlelength=1.5)
    ax[0].set_title(r"Aliasing on $N = 8$ points")
    xx = np.linspace(-0.6, 0.9, 3000)
    for n_max, col in ((11, fs.C2), (101, fs.C1)):
        S = sum(4 / np.pi * np.sin(n * xx) / n for n in range(1, n_max + 1, 2))
        ax[1].plot(xx, S, color=col, lw=1.4, label=rf"$n_\max$ = {n_max}")
    xm = np.linspace(1e-4, np.pi / 2, 200001)
    for n_max in (11, 101):
        smax = (sum(4 / np.pi * np.sin(n * xm) / n for n in range(1, n_max + 1, 2))).max()
        print(f"fourier: max of the partial sum (n_max = {n_max}) = {smax:.4f}")
    ax[1].plot(xx, np.sign(xx), ":", color=fs.INK2, lw=1)
    ax[1].axhline(smax, color=fs.C3, ls="--", lw=1.2); ax[1].text(0.85, smax + 0.03, f"{smax:.3f}", ha="right")
    ax[1].legend(loc="lower right", fontsize=9, frameon=True); ax[1].set_title("Gibbs phenomenon")
    Ns = np.array([4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256])
    es, ed = [], []
    for N in Ns:
        xg = 2 * np.pi * np.arange(N) / N
        f, fp = np.exp(np.sin(xg)), np.cos(xg) * np.exp(np.sin(xg))
        es.append(np.abs(d_spectral(f) - fp).max()); ed.append(np.abs(d_fd2(f) - fp).max())
    for N, a_, b_ in zip(Ns, es, ed):
        if N in (8, 16, 32, 64, 128):
            print(f"fourier: N = {N:3d}  spectral {a_:.1e}  FD2 {b_:.1e}")
    ax[2].loglog(Ns, es, "o-", color=fs.C1, label="spectral")
    ax[2].loglog(Ns, ed, "s-", color=fs.C2, label="finite differences (order 2)")
    ax[2].loglog(Ns, ed[3] * (Ns / Ns[3]) ** -2.0, ":", color=fs.INK2, lw=1)
    ax[2].text(150, ed[3] * (150 / Ns[3]) ** -2.0 * 3, r"$\propto N^{-2}$", color=fs.INK2)
    ax[2].set_xlabel(r"number of points $N$"); ax[2].set_ylabel("max error")
    ax[2].legend(loc="center", bbox_to_anchor=(0.70, 0.45), fontsize=8.5, frameon=True)
    ax[2].set_title(r"Error of the derivative of $e^{\sin x}$")
    fig.tight_layout()
    fs.save(fig, out / "fig-fourier.png")


# ---------------------------------------------------------------------------------------------
def fig_helmholtz(out):
    """Smooth random field (Fourier modes |k| <= 4, seed 2) split with the Leray projection (6.2)."""
    rng = np.random.default_rng(2)
    N = 64
    k1 = np.fft.fftfreq(N, 1.0 / N)
    KX, KY = np.meshgrid(k1, k1, indexing="xy")
    K2 = KX ** 2 + KY ** 2
    filt = (K2 > 0) & (K2 <= 16)
    uh = [np.fft.fft2(rng.normal(size=(N, N))) * filt for _ in range(2)]
    K2s = np.where(K2 > 0, K2, 1)
    div_h = 1j * (KX * uh[0] + KY * uh[1])
    gh = [KX * (KX * uh[0] + KY * uh[1]) / K2s, KY * (KX * uh[0] + KY * uh[1]) / K2s]   # gradient part
    wh = [uh[0] - gh[0], uh[1] - gh[1]]                                                  # P u
    ph = -div_h / K2s                                                                    # grad p = g, i.e. -k² p^ = i k·u^
    om_h = 1j * (KX * wh[1] - KY * wh[0])
    R = lambda h: np.real(np.fft.ifft2(h))  # noqa: E731
    u, g, w = [R(h) for h in uh], [R(h) for h in gh], [R(h) for h in wh]
    print(f"helmholtz: max|div P u| = {np.abs(R(1j * (KX * wh[0] + KY * wh[1]))).max():.1e}, "
          f"max|curl grad p| = {np.abs(R(1j * (KX * gh[1] - KY * gh[0]))).max():.1e}")
    x = np.arange(N) * 2 * np.pi / N
    X, Y = np.meshgrid(x, x, indexing="xy")
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.4))
    panels = [(u, R(div_h), r"field $\mathbf{u}$ (background: $\nabla\cdot\mathbf{u}$)"),
              (g, R(ph), r"gradient part $\nabla p$ (background: $p$)"),
              (w, R(om_h), r"solenoidal part $\mathbb{P}\mathbf{u}$ (background: $\omega$)")]
    for a, (vec, bg, title) in zip(ax, panels):
        m = 1.6 * np.abs(bg).max()
        a.imshow(bg, extent=(0, x[-1], 0, x[-1]), origin="lower", cmap=fs.DIVERGING, vmin=-m, vmax=m,
                 interpolation="bilinear")
        speed = np.hypot(*vec)
        a.streamplot(X, Y, vec[0], vec[1], color=fs.INK, density=1.4, linewidth=2.2 * speed / speed.max(),
                     arrowsize=0.8)
        a.set_title(title); a.set_xlim(0, x[-1]); a.set_ylim(0, x[-1]); a.set_aspect("equal")
        a.set_xticks([]); a.set_yticks([]); a.grid(False)
    fig.tight_layout(w_pad=3)
    for (left, right), sign in zip(zip(ax[:-1], ax[1:]), ("=", "+")):
        p0, p1 = left.get_position(), right.get_position()
        fig.text((p0.x1 + p1.x0) / 2, (p0.y0 + p0.y1) / 2, sign, fontsize=22, ha="center", va="center")
    fs.save(fig, out / "fig-helmholtz.png")


# ---------------------------------------------------------------------------------------------
def fig_current(out):
    """Code of the page (section 6): random stream function with E(k) ~ k^-3, seed 6."""
    rng = np.random.default_rng(6)
    N, L = 256, 2 * np.pi
    kv = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    k1 = kv.copy(); k1[N // 2] = 0.0
    KX, KY = np.meshgrid(k1, k1, indexing="ij")
    kn = np.sqrt(sum(k ** 2 for k in np.meshgrid(kv, kv, indexing="ij")))
    F, Fi = np.fft.fft2, lambda a: np.real(np.fft.ifft2(a))
    amp = np.zeros_like(kn)
    band = (kn >= 4) & (kn <= 64)
    amp[band] = np.sqrt(kn[band] ** -3 / (np.pi * kn[band] ** 3))
    psi = Fi(amp * F(rng.normal(size=(N, N))))
    psi_h = F(psi)
    ux, uy = Fi(1j * KY * psi_h), Fi(-1j * KX * psi_h)
    c = np.sqrt(np.mean(ux ** 2 + uy ** 2))
    ux, uy, psi = ux / c, uy / c, psi / c
    uh2 = (np.abs(F(ux)) ** 2 + np.abs(F(uy)) ** 2) / N ** 4
    E = np.array([0.5 * uh2[(kn >= s - 0.5) & (kn < s + 0.5)].sum() for s in range(N)])
    s = np.arange(8, 49)
    print(f"current: slope of the spectrum between k = 8 and 48: {np.polyfit(np.log(s), np.log(E[s]), 1)[0]:.2f}")
    omega = Fi((KX ** 2 + KY ** 2) * F(psi))
    x = np.arange(N) * L / N
    X, Y = np.meshgrid(x, x, indexing="ij")
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
    m = np.percentile(np.abs(omega), 99)
    ax[0].imshow(omega.T, extent=(0, L, 0, L), origin="lower", cmap=fs.DIVERGING, vmin=-1.5 * m, vmax=1.5 * m,
                 interpolation="bilinear")
    lv = np.linspace(-np.abs(psi).max(), np.abs(psi).max(), 22)
    ax[0].contour(X, Y, psi, levels=lv[lv > 0], colors=fs.INK, linewidths=0.8, linestyles="solid")
    ax[0].contour(X, Y, psi, levels=lv[lv < 0], colors=fs.INK, linewidths=0.8, linestyles="dashed")
    ax[0].set_aspect("equal"); ax[0].set_xticks([]); ax[0].set_yticks([]); ax[0].grid(False)
    ax[0].set_title(r"level lines of $\psi$ (background: $\omega = -\Delta\psi$)")
    k = np.arange(4, 65)
    ax[1].loglog(k, E[k], "o", color=fs.C1, ms=4.5)
    c3 = np.exp(np.mean(np.log(E[s]) + 3 * np.log(s)))          # least-squares amplitude of c k^-3 on k = 8..48
    ax[1].loglog(k[1:-3], c3 * k[1:-3] ** -3.0, "--", color=fs.C2)
    ax[1].text(20, c3 * 20.0 ** -3.0 * 2.5, r"$k^{-3}$", fontsize=12)
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    ax[1].xaxis.set_major_locator(FixedLocator([4, 8, 16, 32, 64])); ax[1].xaxis.set_major_formatter(ScalarFormatter())
    ax[1].xaxis.set_minor_formatter(NullFormatter())
    ax[1].set_xlabel(r"$k$"); ax[1].set_ylabel(r"$E(k)$"); ax[1].set_title(r"energy spectrum $E(k)$")
    fig.tight_layout()
    fs.save(fig, out / "fig-current.png")


if __name__ == "__main__":
    out = fs.out_dir(__file__, sys.argv)
    for fn in (fig_fields, fig_monopole_dipole, fig_fourier, fig_helmholtz, fig_current):
        fn(out)
