"""Static figures of module p4 (dynamical systems, bifurcations, chaos, noise).

Usage: python3 figures_p4.py [out_dir]     (default: the figures/ folder next to this script)
Each figure reuses the code block of the page that precedes it; the numbers quoted in the captions
are printed. Runs on CPU in about one minute.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

fs.use(10)
HERE = Path(__file__).resolve().parent


def rk4(f, x, dt):
    k1 = f(x); k2 = f(x + 0.5 * dt * k1); k3 = f(x + 0.5 * dt * k2); k4 = f(x + dt * k3)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# ---------------------------------------------------------------------------------------------
def fig_bifurcations(out):
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))

    def branch(a, r, x, stable, **kw):
        a.plot(r, x, color=fs.C1 if stable else fs.C2, ls="-" if stable else "--", **kw)

    # (a) saddle-node x' = r + x^2: fixed points ±sqrt(-r), stable for x < 0
    r = np.linspace(-1, 0, 400)
    branch(ax[0, 0], r, -np.sqrt(-r), True, label="stable")
    branch(ax[0, 0], r, np.sqrt(-r), False, label="unstable")
    ax[0, 0].set_xlim(-1, 0.6); ax[0, 0].legend(loc="upper right")
    ax[0, 0].set_title("(a) saddle-node: ẋ = r + x²")
    # (b) supercritical pitchfork x' = rx - x^3
    r1, r2 = np.linspace(-1, 0, 200), np.linspace(0, 1, 400)
    branch(ax[0, 1], r1, 0 * r1, True); branch(ax[0, 1], r2, 0 * r2, False)
    branch(ax[0, 1], r2, np.sqrt(r2), True); branch(ax[0, 1], r2, -np.sqrt(r2), True)
    ax[0, 1].set_title("(b) supercritical pitchfork: ẋ = rx − x³")
    # (c) subcritical pitchfork x' = rx + x^3 - x^5: x^2 = (1 ± sqrt(1 + 4r)) / 2
    r = np.linspace(-0.25, 0.4, 600)
    up = np.sqrt((1 + np.sqrt(1 + 4 * r)) / 2)
    rm = np.linspace(-0.25, 0, 400)
    lo = np.sqrt(np.clip((1 - np.sqrt(1 + 4 * rm)) / 2, 0, None))
    a = ax[1, 0]
    for s in (1, -1):
        branch(a, r, s * up, True); branch(a, rm, s * lo, False)
    branch(a, np.linspace(-0.5, 0, 100), np.zeros(100), True); branch(a, np.linspace(0, 0.4, 100), np.zeros(100), False)
    arrow = dict(arrowstyle="->", color=fs.INK2, lw=1.4)
    a.annotate("", xy=(0, 0.95), xytext=(0, 0.02), arrowprops=arrow)
    a.annotate("", xy=(-0.25, 0.05), xytext=(-0.25, 0.68), arrowprops=arrow)
    a.set_title("(c) subcritical pitchfork: ẋ = rx + x³ − x⁵")
    # (d) imperfect pitchfork x' = h + rx - x^3, h = 0.05: roots and stability from f'(x) = r - 3x^2
    h = 0.05
    rs, xs, st = [], [], []
    for rr in np.linspace(-1, 1, 1601):
        for x in np.roots([-1, 0, rr, h]):
            if abs(x.imag) < 1e-9:
                rs.append(rr); xs.append(x.real); st.append(rr - 3 * x.real ** 2 < 0)
    rs, xs, st = map(np.array, (rs, xs, st))
    ax[1, 1].scatter(rs[st], xs[st], s=1.5, color=fs.C1, lw=0)
    ax[1, 1].scatter(rs[~st], xs[~st], s=1.5, color=fs.C2, lw=0)
    r_sn = 3 * (h / 2) ** (2 / 3)
    print(f"bifurcations: imperfect pitchfork, saddle-node at r = 3 (h/2)^(2/3) = {r_sn:.3f}")
    ax[1, 1].set_title(f"(d) imperfect pitchfork: ẋ = h + rx − x³ (h = {h})")
    for a in ax.flat:
        a.axhline(0, color=fs.INK2, lw=0.7); a.axvline(0, color=fs.INK2, lw=0.7)
        a.set_xlabel("r"); a.set_ylabel("x*")
    fig.tight_layout()
    fs.save(fig, out / "bifurcations.png")


# ---------------------------------------------------------------------------------------------
def fig_lorenz(out):
    s, r, b = 10.0, 28.0, 8.0 / 3.0

    def F(x):
        return np.array([s * (x[1] - x[0]), x[0] * (r - x[2]) - x[1], x[0] * x[1] - b * x[2]])

    dt = 0.01
    x = np.array([1.0, 1.0, 1.0])
    for _ in range(2000):                                   # transient, as in the page
        x = rk4(F, x, dt)
    traj = [x]
    for _ in range(5000):
        traj.append(rk4(F, traj[-1], dt))
    traj = np.array(traj)
    # two trajectories separated by 1e-8 along x, no renormalization
    xa, xb = x.copy(), x + np.array([1e-8, 0.0, 0.0])
    ts, ds = [0.0], [1e-8]
    for k in range(4000):
        xa, xb = rk4(F, xa, dt), rk4(F, xb, dt)
        ts.append((k + 1) * dt); ds.append(np.linalg.norm(xb - xa))
    ts, ds = np.array(ts), np.array(ds)
    lam1 = 0.90                                             # page: lambda_1 ≈ 0.90 (Benettin and QR)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].plot(traj[:, 0], traj[:, 2], color=fs.C1, lw=0.6)
    ax[0].set_xlabel("x"); ax[0].set_ylabel("z"); ax[0].set_title("(a) Lorenz attractor (x–z projection)")
    ax[1].semilogy(ts, ds, color=fs.C1, lw=1.3)
    tt = np.linspace(0, 27, 50)
    ax[1].semilogy(tt, 1e-8 * np.exp(lam1 * tt), "--", color=fs.C2, lw=1.8, label=f"slope λ₁ = {lam1:.2f}")
    ax[1].set_ylim(3e-9, 1e2); ax[1].legend(loc="lower right")
    ax[1].set_xlabel("time t"); ax[1].set_ylabel("|δx(t)| (log scale)")
    ax[1].set_title("(b) distance between two trajectories (initial distance 10⁻⁸)")
    sat = ts[np.argmax(ds > 1.0)]
    print(f"lorenz: separation reaches 1 at t = {sat:.1f}, max {ds.max():.1f}")
    fig.tight_layout()
    fs.save(fig, out / "lorenz.png")


# ---------------------------------------------------------------------------------------------
def fig_kramers(out):
    rng = np.random.default_rng(1)
    U = lambda x: x ** 4 / 4 - x ** 2 / 2  # noqa: E731
    dU = 0.25

    def tau_exact(s):
        inner = lambda y: quad(lambda z: np.exp(-2 * U(z) / s ** 2), -np.inf, y)[0]  # noqa: E731
        return 2 / s ** 2 * quad(lambda y: np.exp(2 * U(y) / s ** 2) * inner(y), -1, 1)[0]

    def tau_kramers(s):
        return 2 * np.pi / np.sqrt(2.0) * np.exp(2 * dU / s ** 2)

    # simulation of the page (Euler–Maruyama, 250 particles per level, T = 800)
    levels = np.array([0.40, 0.45, 0.50, 0.60])
    sig = np.repeat(levels, 250)
    dt, T = 0.01, 800.0
    x = -np.ones(sig.size); well = -np.ones(sig.size); nb = np.zeros(sig.size)
    for _ in range(int(T / dt)):
        x += -(x ** 3 - x) * dt + sig * np.sqrt(dt) * rng.standard_normal(sig.size)
        flip = ((well < 0) & (x > 1)) | ((well > 0) & (x < -1))
        well[flip] *= -1; nb[flip] += 1
    tau_sim = np.array([250 * T / nb[sig == s].sum() for s in levels])
    for s, t in zip(levels, tau_sim):
        print(f"kramers: sigma = {s:.2f}  tau sim = {t:.1f}  exact = {tau_exact(s):.1f}  Kramers = {tau_kramers(s):.1f}")
    # one path at sigma = 0.45
    rng2 = np.random.default_rng(7)
    n = int(600 / dt)
    path = np.empty(n); y = -1.0
    noise = rng2.standard_normal(n)
    for k in range(n):
        y += -(y ** 3 - y) * dt + 0.45 * np.sqrt(dt) * noise[k]
        path[k] = y
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.6), gridspec_kw={"width_ratios": [1, 1.6, 1.1]})
    xx = np.linspace(-1.8, 1.8, 400)
    ax[0].plot(xx, U(xx), color=fs.C1)
    ax[0].annotate("", xy=(0, -0.245), xytext=(0, 0.0), arrowprops=dict(arrowstyle="<->", color=fs.INK2))
    ax[0].text(0.08, -0.14, "barrier ΔU = 1/4", fontsize=9)
    ax[0].set_ylim(-0.33, 0.6); ax[0].set_xlabel("x"); ax[0].set_title("(a) potential U(x) = x⁴/4 − x²/2")
    ax[1].plot(np.arange(n)[::5] * dt, path[::5], color=fs.C1, lw=0.6)
    ax[1].set_xlabel("time t"); ax[1].set_ylabel("x(t)"); ax[1].set_title("(b) sample path, σ = 0.45")
    s_grid = 1 / np.sqrt(np.linspace(2, 11, 30))
    inv = 1 / s_grid ** 2
    ax[2].semilogy(inv, [tau_exact(s) for s in s_grid], color=fs.C1, label="exact formula (integral)")
    ax[2].semilogy(inv, tau_kramers(s_grid), "--", color=fs.C2, label="Kramers asymptotics")
    ax[2].semilogy(1 / levels ** 2, tau_sim, "o", color=fs.C3, ms=7, label="simulation (Euler–Maruyama)")
    ax[2].set_xlabel("1/σ²"); ax[2].set_ylabel("mean switching time τ"); ax[2].legend(fontsize=8.5, loc="upper left")
    ax[2].set_title("(c) Arrhenius–Kramers law")
    fig.tight_layout()
    fs.save(fig, out / "kramers.png")


# ---------------------------------------------------------------------------------------------
MU, NU = 0.119, 0.1


def gissinger_rhs(Y, g):
    q, d, v = Y
    return np.array([MU * q - v * d, -NU * d + v * q, g - v + q * d])


def gissinger_run(g, Y, dt, n, every=None):
    """RK4 with step dt for n steps; returns the final state and, if ``every``, the stored states."""
    f = lambda Z: gissinger_rhs(Z, g)  # noqa: E731
    keep = []
    for k in range(n):
        Y = rk4(f, Y, dt)
        if every and k % every == 0:
            keep.append(Y)
    return Y, (np.array(keep) if every else None)


def fig_gissinger(out):
    dt = 0.02
    # (e): the sweep of the page (30 trajectories per Gamma, transient 600, duration 1500)
    rng = np.random.default_rng(3)
    gammas = np.array([0.84, 0.85, 0.86, 0.865, 0.87, 0.88, 0.90, 0.95])
    g = np.repeat(gammas, 30)
    Y = rng.normal(size=(3, g.size)) * 0.8; Y[2] = np.abs(Y[2])
    Y, _ = gissinger_run(g, Y, dt, int(600 / dt))
    crossings = np.zeros(g.size)
    for _ in range(int(1500 / dt)):
        s0 = np.sign(Y[1])
        Y = rk4(lambda Z: gissinger_rhs(Z, g), Y, dt)
        crossings += np.sign(Y[1]) != s0
    rate = np.array([crossings[g == G].sum() / (30 * 1500) for G in gammas])
    print("gissinger: rate of zero crossings per Gamma:", ", ".join(f"{G}: {r:.5f}" for G, r in zip(gammas, rate)))
    # (a)-(d): single trajectories after a transient of 600
    rng = np.random.default_rng(4)
    starts = {}
    for G in (0.84, 0.86, 0.90):
        y0 = np.abs(rng.normal(size=3)) * 0.8
        y0, _ = gissinger_run(G, y0, dt, int(600 / dt))
        starts[G] = y0
    S = np.array([-1.0, -1.0, 1.0])                         # symmetry (Q, D, V) -> (-Q, -D, V)
    every = 10
    _, a86 = gissinger_run(0.86, starts[0.86], dt, int(1500 / dt), every)
    _, b86 = gissinger_run(0.86, starts[0.86] * S, dt, int(1500 / dt), every)
    _, a90 = gissinger_run(0.90, starts[0.90], dt, int(1500 / dt), every)
    _, c84 = gissinger_run(0.84, starts[0.84], dt, int(1500 / dt), every)
    _, d90 = gissinger_run(0.90, starts[0.90], dt, int(4000 / dt), every)
    t = np.arange(len(a86)) * dt * every
    fig = plt.figure(figsize=(12, 6.6))
    gs = fig.add_gridspec(2, 3)
    ax_a, ax_b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])
    ax_c, ax_d = fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])
    ax_e = fig.add_subplot(gs[1, 1:])
    hi, lo = (a86, b86) if a86[:, 1].mean() > 0 else (b86, a86)
    ax_a.plot(t, hi[:, 1], color=fs.C2, lw=0.8); ax_a.plot(t, lo[:, 1], color=fs.C1, lw=0.8)
    ax_a.set_title("(a) D(t) for Γ = 0.86: no reversal")
    ax_b.plot(t, a90[:, 1], color=fs.C1, lw=0.8); ax_b.set_title("(b) D(t) for Γ = 0.90: chaotic reversals")
    for a in (ax_a, ax_b):
        a.set_ylim(-3.3, 3.3); a.set_xlabel("time t"); a.set_ylabel("D")
    side = c84 if c84[:, 1].mean() < 0 else c84 * S
    ax_c.scatter(side[:, 0], side[:, 1], s=0.6, color=fs.C1, lw=0, label="attractor D < 0")
    ax_c.scatter(-side[:, 0], -side[:, 1], s=0.6, color=fs.C2, lw=0, label="attractor D > 0 (image under S)")
    ax_c.legend(loc="upper right", fontsize=8, markerscale=8)
    ax_c.set_title("(c) Γ = 0.84: two symmetric attractors")
    ax_d.scatter(d90[:, 0], d90[:, 1], s=0.6, color=fs.C1, lw=0)
    ax_d.set_title("(d) Γ = 0.90: merged attractors")
    for a in (ax_c, ax_d):
        a.set_xlim(-3, 3); a.set_ylim(-3.3, 3.3); a.set_xlabel("Q"); a.set_ylabel("D")
    ax_e.axvspan(0.86, 0.865, color=fs.C2, alpha=0.25, lw=0)
    ax_e.plot(gammas, rate, "o-", color=fs.C1, ms=7)
    ax_e.text(0.841, rate.max() * 0.72, "observed threshold\nbetween 0.86 and 0.865", fontsize=9)
    ax_e.set_xlabel("Γ"); ax_e.set_ylabel("crossings per unit time"); ax_e.set_title("(e) rate of zero crossings of D")
    fig.tight_layout()
    fs.save(fig, out / "gissinger.png")


if __name__ == "__main__":
    out = fs.out_dir(str(HERE / "figures" / "x"), sys.argv)
    for fn in (fig_bifurcations, fig_lorenz, fig_kramers, fig_gissinger):
        fn(out)
