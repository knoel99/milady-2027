"""Data for the thumbnails of the "thesis-plan" figure.

1. Step 0: D(t) series of the Gissinger model (2012), same equations and parameters as E1
   (experiments/e1_gissinger.py) : dQ/dt = mu Q - V D, dD/dt = -nu D + V Q, dV/dt = Gamma - V + Q D,
   mu = 0.119, nu = 0.1, Gamma = 0.9 (above the reversal crisis, 0.86-0.87 in E1).
2. Step 1: a reference snapshot of E2 (forced 2D MHD, results/e2_samples.npz, versioned,
   Fourier coefficients of u and B): current density j on the grid, and contour lines of the potential a
   (field lines of B).
3. Step 2: kinematic ABC dynamo mode of E3 (results/e3_modes.npz, Rm = 12, in the first
   window 8.9 < Rm < 17.5): |B| on the three visible faces of the periodic box.

Output: plan_data.json (values normalized to [0, 1], rounded).
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[4] / "experiments" / "results"  # repo root: site/figures/thesis-plan/figure/data -> 5 levels up
out = {}

# ---------- 1. Gissinger ----------
MU, NU, GAM = 0.119, 0.1, 0.9


def rhs(x):
    q, d, v = x
    return np.array([MU * q - v * d, -NU * d + v * q, GAM - v + q * d])


x = np.array([0.1, 0.2, 0.9])
dt = 0.01
ts, ds = [], []
t = 0.0
for i in range(int(2400 / dt)):
    k1 = rhs(x); k2 = rhs(x + dt / 2 * k1); k3 = rhs(x + dt / 2 * k2); k4 = rhs(x + dt * k3)
    x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t += dt
    if t > 400 and i % 20 == 0:
        ts.append(t); ds.append(x[1])
ts = np.array(ts) - ts[0]; ds = np.array(ds)
# choose a window with 3 or 4 clear reversals
sgn = np.sign(ds)
flips = np.where(np.diff(sgn) != 0)[0]
print("zero crossings:", len(flips), "sur", ts[-1])
from scipy.ndimage import uniform_filter1d
sm_all = np.sign(uniform_filter1d(ds, 75))
flip_t = ts[np.where(np.diff(sm_all) != 0)[0]]
print("clear reversals:", np.round(flip_t, 1))
W = 560.0
best, score = 0.0, -1
for t0 in np.arange(0, ts[-1] - W, 5):
    f = (flip_t - t0) / W
    inside = f[(f > 0) & (f < 1)]
    if len(inside) != 3:
        continue
    # reversals well inside the window and well spaced
    sc = min(inside.min(), 1 - inside.max(), np.diff(inside).min())
    if sc > score:
        best, score = t0, sc
print("window", best, "score", score)
m = (ts >= best) & (ts < best + W)
tt = (ts[m] - best) / W
dd = ds[m] / np.abs(ds).max()
# subsample for a light plot
step = max(1, len(tt) // 700)
out["gissinger"] = {"t": np.round(tt[::step], 4).tolist(), "D": np.round(dd[::step], 4).tolist(),
                    "Gamma": GAM, "window": [float(best), W]}
print("Gissinger window", best, "points", len(tt[::step]))

# ---------- 2. MHD 2D (E2) ----------
d = np.load(EXP / "e2_samples.npz")
ref = d["ref"]; kx = d["kx"]; ky = d["ky"]
c = ref[0]  # (4, M): ux, uy, bx, by (complex coefficients, half-plane kx >= 0)
bx, by = c[2], c[3]
jk = 1j * kx * by - 1j * ky * bx
k2 = kx ** 2 + ky ** 2
ak = np.where(k2 > 0, jk / np.maximum(k2, 1e-12), 0)  # j = -lap a  => a_k = j_k / k^2
N = 96
xs = np.linspace(0, 2 * np.pi, N, endpoint=False)
X, Y = np.meshgrid(xs, xs, indexing="xy")


def synth(ck):
    f = np.zeros_like(X)
    for cc, a_, b_ in zip(ck, kx, ky):
        w = 1.0 if a_ > 0 else 0.5  # column kx = 0: half weight (Hermitian approximation)
        f += 2 * w * np.real(cc * np.exp(1j * (a_ * X + b_ * Y)))
    return f


J = synth(jk); A = synth(ak)
jn = (J - J.min()) / (J.max() - J.min())
# 48 x 48 map for the thumbnail
Ns = 48
jn_s = jn[::2, ::2]
out["mhd2d"] = {"j": np.round(jn_s, 3).tolist()}
# contour lines of a (field lines of B), in unit coordinates [0, 1]
fig, ax = plt.subplots()
levels = np.linspace(A.min(), A.max(), 12)[1:-1]
cs = ax.contour(xs / (2 * np.pi), xs / (2 * np.pi), A, levels=levels)
lines = []
for seg_list in cs.allsegs:
    for seg in seg_list:
        if len(seg) < 6:
            continue
        lines.append(np.round(seg[:: max(1, len(seg) // 60)], 4).tolist())
plt.close(fig)
out["mhd2d"]["a_lines"] = lines
print("contour lines of a:", len(lines))

# ---------- 3. ABC (E3) ----------
e = np.load(EXP / "e3_modes.npz")
B = e["Rm12"]  # (3, 32, 32, 32), indices (x, y, z) ?
mag = np.sqrt((B ** 2).sum(0))
mag = mag / mag.max()
# faces: x = max, y = 0 (front), z = max (top); index order assumed (0, 1, 2) = (x, y, z)
faces = {
    "x1": mag[-1, :, :],   # (y, z)
    "y0": mag[:, 0, :],    # (x, z)
    "z1": mag[:, :, -1],   # (x, y)
}
out["abc"] = {k: np.round(v, 3).tolist() for k, v in faces.items()}
out["abc"]["Rm"] = 12

(HERE / "plan_data.json").write_text(json.dumps(out))
print("written", HERE / "plan_data.json")

# preview
fig, axs = plt.subplots(1, 5, figsize=(15, 3))
axs[0].plot(tt, dd, lw=0.7); axs[0].axhline(0, color="k", lw=0.5)
axs[1].imshow(jn, cmap="gray", origin="lower"); axs[1].set_title("j")
for ln in lines:
    ln = np.array(ln); axs[2].plot(ln[:, 0], ln[:, 1], "k", lw=0.5)
axs[2].set_aspect(1)
axs[3].imshow(faces["z1"].T, cmap="gray", origin="lower"); axs[3].set_title("|B| z1")
axs[4].imshow(faces["y0"].T, cmap="gray", origin="lower"); axs[4].set_title("|B| y0")
fig.savefig(HERE / "preview.png", dpi=90)
