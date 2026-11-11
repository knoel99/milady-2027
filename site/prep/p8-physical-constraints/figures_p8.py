"""Static figures of module p8 (physical constraints in generative models).

Usage: python3 figures_p8.py [out_dir]     (default: the folder of this script)
Both figures rerun the code block of the page that precedes them (section 3.5: six ways of obtaining
a divergence-free field, seed 0; section 6: tilting of the double-well law, seed 0) and print the
numbers quoted in the captions. Runs on one CPU thread in about one minute.
"""
import sys
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import minimize
from scipy.stats import gaussian_kde, wasserstein_distance

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

fs.use(10.5)
HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------------------------
def divergence_experiment():
    """Code block of section 3.5, unchanged except for the names; returns {variant: (div_rel, W1/E)} and the floor."""
    torch.set_num_threads(1); torch.manual_seed(0); rng = np.random.default_rng(0)
    ks = np.array([(i, j) for i in range(-2, 3) for j in range(-2, 3) if i > 0 or (i == 0 and j > 0)], float)
    nk, kn = len(ks), np.linalg.norm(ks, axis=1)
    e = np.stack([ks[:, 1], -ks[:, 0]], 1) / kn[:, None]
    D = 4 * nk
    P = np.zeros((D, D)); C = np.zeros((D, 2 * nk))
    for cs in range(2):
        for i in range(nk):
            j = 2 * (cs * nk + i)
            P[j:j + 2, j:j + 2] = np.outer(e[i], e[i])
            C[j:j + 2, (1 - cs) * nk + i] = (1 if cs == 0 else -1) * kn[i] * e[i]
    K4 = np.concatenate([ks, ks])

    def div_rel(x):
        c = x.reshape(len(x), 2 * nk, 2)
        return np.sqrt(((c * K4).sum(-1) ** 2).sum(1) / ((c ** 2).sum(-1) * (K4 ** 2).sum(-1)).sum(1))

    def data(N):
        r = rng.uniform(0.5, 1.5, (N, 1))
        psi = r * np.tile(kn, 2) ** -2.0 * rng.normal(size=(N, 2 * nk))
        return psi @ C.T, psi

    def train(X, penalty=0.0, noise_in_S=False, steps=1000):
        X = torch.tensor(X, dtype=torch.float32); d = X.shape[1]
        Pt = torch.tensor(P, dtype=torch.float32); Q = torch.eye(D) - Pt
        net = torch.nn.Sequential(torch.nn.Linear(d + 1, 128), torch.nn.SiLU(), torch.nn.Linear(128, 128),
                                  torch.nn.SiLU(), torch.nn.Linear(128, d))
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        for _ in range(steps):
            x1 = X[torch.randint(len(X), (256,))]; x0 = torch.randn_like(x1); t = torch.rand(256, 1)
            if noise_in_S:
                x0 = x0 @ Pt.T
            xt = (1 - t) * x0 + t * x1
            v = net(torch.cat([xt, t], 1))
            loss = ((v - (x1 - x0)) ** 2).sum(1).mean()
            if penalty:
                loss = loss + penalty * (((xt + (1 - t) * v) @ Q.T) ** 2).sum(1).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        return net

    @torch.no_grad()
    def generate(net, x0, proj=None, n=50):
        x = torch.tensor(x0, dtype=torch.float32)
        Pt = None if proj is None else torch.tensor(proj, dtype=torch.float32)
        if Pt is not None:
            x = x @ Pt.T
        for i in range(n):
            x = x + net(torch.cat([x, torch.full((len(x), 1), i / n)], 1)) / n
            if Pt is not None:
                x = x @ Pt.T
        return x.double().numpy()

    U, Psi = data(4000); Uref, _ = data(2000)
    su = np.repeat(np.sqrt((U.reshape(-1, 2 * nk, 2) ** 2).sum(2).mean(0)), 2); sp = Psi.std(0)
    E = lambda x: 0.25 * (x ** 2).sum(1)  # noqa: E731
    floor = wasserstein_distance(E(data(2000)[0]), E(Uref)) / E(Uref).mean()
    z = rng.normal(size=(2000, D))
    net_u, net_pen = train(U / su), train(U / su, penalty=1.0)
    net_S, net_psi = train(U / su, noise_in_S=True), train(Psi / sp)
    res = {"free": generate(net_u, z) * su}
    res["final projection"] = res["free"] @ P.T
    res["projected flow"] = generate(net_u, z, proj=P) * su
    res["soft penalty"] = generate(net_pen, z) * su
    res["flow in S"] = generate(net_S, z, proj=P) * su
    res["potential psi"] = (generate(net_psi, z[:, :2 * nk]) * sp) @ C.T
    out = {}
    for name, x in res.items():
        out[name] = (float(np.median(div_rel(x))), wasserstein_distance(E(x), E(Uref)) / E(Uref).mean())
        print(f"divergence: {name:17s} median div_rel = {out[name][0]:.1e}, W1(E)/E = {out[name][1]:.3f}")
    print(f"divergence: floor W1(E)/E = {floor:.3f}")
    return out, floor


def fig_divergence_mechanisms(out):
    res, floor = divergence_experiment()
    rows = [("free", "free"), ("soft penalty", "soft penalty"), ("final projection", "free + final projection"),
            ("projected flow", "projected flow"), ("flow in S", "flow in S (projected noise)"),
            ("potential psi", "potential ψ (stream function)")]
    fig, ax = plt.subplots(figsize=(11, 4.4))
    y = np.arange(len(rows))[::-1]
    for yi, (key, label) in zip(y, rows):
        div, w1 = res[key]
        exact = div < 1e-6
        ax.barh(yi, w1, height=0.5, color=fs.C1 if exact else "#6b7280")
        mant, ex = f"{div:.1e}".split("e")
        sup = str(int(ex)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
        txt = "0 (machine precision)" if exact else f"{mant}·10{sup}"
        ax.text(0.885, yi, txt, va="center", transform=ax.get_yaxis_transform())
    ax.axvline(floor, color=fs.INK, ls="--", lw=1.6)
    ax.text(floor + 0.008, len(rows) - 0.45, "sampling floor", va="bottom")
    ax.text(0.885, len(rows) - 0.45, "relative divergence (median)", va="bottom", fontweight="bold",
            transform=ax.get_yaxis_transform())
    ax.set_yticks(y, [label for _, label in rows]); ax.set_ylim(-0.6, len(rows) - 0.2)
    ax.set_xlim(0, max(r[1] for r in res.values()) * 1.18); ax.grid(axis="y", visible=False)
    ax.set_xlabel("error on the energy law  W₁(E) / ⟨E⟩")
    ax.set_title("Same training budget: an exact constraint is not enough, what the network must learn matters",
                 loc="left", fontsize=11, pad=24)
    ax.set_axisbelow(True)
    fig.subplots_adjust(right=0.78)
    fs.save(fig, out / "fig-divergence-mechanisms.png")


# ---------------------------------------------------------------------------------------------
def fig_tilting(out):
    """Code block of section 6 (double well, sigma = 0.7, model too hot sigma = 0.85), seed 0."""
    rng = np.random.default_rng(0)
    sigma = 0.7
    grid = np.linspace(-3, 3, 6001)

    def law(sig):
        p = np.exp(-2 * (grid ** 4 / 4 - grid ** 2 / 2) / sig ** 2); return p / np.trapezoid(p, grid)

    def draw(p, N):
        F = np.cumsum(p); F /= F[-1]; return np.interp(rng.uniform(size=N), F, grid)

    F = lambda x: x - x ** 3  # noqa: E731
    g1 = lambda x: x * F(x) + sigma ** 2 / 2  # noqa: E731
    g2 = lambda x: x ** 3 * F(x) + 1.5 * sigma ** 2 * x ** 2  # noqa: E731

    def tilt(x, G):
        dual = lambda b: np.log(np.mean(np.exp(G @ b - (G @ b).max()))) + (G @ b).max()  # noqa: E731
        b = minimize(dual, np.zeros(G.shape[1]), method="BFGS").x
        w = np.exp(G @ b - (G @ b).max()); return w / w.sum()

    N = 20000
    draw(law(sigma), N)                                     # the page draws the reference first (same RNG stream)
    xq = draw(law(0.85), N)
    r = np.sqrt((1 + np.sqrt(1 + 2 * sigma ** 2)) / 2)
    w1 = tilt(xq, g1(xq)[:, None])
    w2 = tilt(xq, np.stack([g1(xq), g2(xq)], 1))
    mu = law(sigma)
    print(f"tilting: true law peak {mu.max():.2f}, value at 0 {mu[3000]:.2f}; per-sample projection at ±{r:.2f}; "
          f"ESS/N = {1 / np.sum(w1 ** 2) / N:.2f}, {1 / np.sum(w2 ** 2) / N:.2f}")
    xs = np.linspace(-2.4, 2.4, 600)
    kde = lambda w: gaussian_kde(xq, bw_method=0.08, weights=w)(xs)  # noqa: E731
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(grid, mu, color=fs.INK, lw=2.4, label="true law μ")
    ax.plot(xs, kde(None), "--", color="#6b7280", lw=2, label="model q (biased)")
    ax.plot(xs, kde(w1), ":", color=fs.C2, lw=2.2, label="q tilted, 1 identity (φ = x²/2)")
    ax.plot(xs, kde(w2), color=fs.C2, lw=2.6, label="q tilted, 2 identities (φ = x²/2, x⁴/4)")
    for s in (-r, r):
        ax.annotate("", xy=(s, 0.62), xytext=(s, 0.0), arrowprops=dict(arrowstyle="-|>", color=fs.C1, lw=2.6))
    ax.plot([], [], color=fs.C1, lw=2.6, label="per-sample correction: 2 Diracs (mass ½ each)")
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(0, 0.68); ax.grid(axis="x", visible=False)
    ax.set_xlabel("state x"); ax.set_ylabel("density")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=9.5)
    ax.set_title("Enforcing a stationarity identity: reweight the law, do not move each sample", loc="left", fontsize=11)
    fig.tight_layout()
    fs.save(fig, out / "fig-tilting.png")


if __name__ == "__main__":
    out = fs.out_dir(__file__, sys.argv)
    for fn in (fig_divergence_mechanisms, fig_tilting):
        fn(out)
