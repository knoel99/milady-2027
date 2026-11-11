"""E3 - Kinematic dynamo of the ABC flow (A = B = C = 1): growth rate as a function of Rm.

Induction equation with prescribed flow, periodic domain [0, 2π)³:
    ∂B/∂t = ∇×(u×B) + η ΔB,   u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x),   Rm = 1/η.
Pseudo-spectral scheme (rfftn), 2/3 dealiasing, integrating-factor RK4 for the diffusion
(solver: ``milady.sim.induction3d``).
The curl form preserves ∇·B = 0 at the discrete level (k·(k×v) = 0).
We measure the growth rate λ = d ln‖B‖/dt after the transient, and keep the eigenmode.

Usage: python3 e3_abc.py [--quick]
Outputs: results/e3_abc[_quick].json, results/e3_modes[_quick].npz
"""
from __future__ import annotations

import argparse
import time

import numpy as np

from common import RESULTS, save_json
from milady.sim.induction3d import growth_rate


def main(quick=False):
    t0 = time.time()
    rms = [4, 8, 12, 16, 20] if quick else [2, 4, 6, 8, 8.5, 9, 9.5, 10, 11, 12, 13, 14, 15, 16, 17, 17.5, 18, 19, 20, 22, 24, 26, 28, 30]
    t_total = 60.0 if quick else 150.0
    rows, modes = [], {}
    for rm in rms:
        lam, lam_q, m = growth_rate(rm, t_total=t_total)
        rows.append({"Rm": rm, "lambda": lam, "lambda_dernier_quart": lam_q, "div_rel": m.divergence_rel()})
        print(f"Rm={rm:5.1f}  λ={lam:+.4f} (last quarter {lam_q:+.4f})  div={m.divergence_rel():.1e}  {time.time() - t0:.0f} s", flush=True)
        if rm in (8, 12, 16, 20):
            modes[f"Rm{rm}"] = np.stack([np.fft.irfftn(c, s=(32,) * 3, axes=(0, 1, 2)) for c in m.bh]).astype(np.float32)
    # Resolution convergence at two points
    conv = []
    for rm in ([12] if quick else [12, 17.5]):
        lam48, _, _ = growth_rate(rm, n=48, t_total=t_total)
        conv.append({"Rm": rm, "lambda_N48": lam48})
        print(f"N=48 Rm={rm}  λ={lam48:+.4f}", flush=True)
    # Thresholds by linear interpolation of the sign changes
    seuils = []
    for a, b in zip(rows[:-1], rows[1:]):
        if np.sign(a["lambda"]) != np.sign(b["lambda"]):
            seuils.append(a["Rm"] + (b["Rm"] - a["Rm"]) * (-a["lambda"]) / (b["lambda"] - a["lambda"]))
    out = {"config": {"N": 32, "A": 1, "B": 1, "C": 1, "dt": 0.05, "t_total": t_total, "Rm": "1/eta"},
           "taux": rows, "convergence": conv, "seuils_interpoles": seuils, "duree_s": time.time() - t0}
    suffix = "_quick" if quick else ""
    save_json(out, f"e3_abc{suffix}.json")
    np.savez_compressed(RESULTS / f"e3_modes{suffix}.npz", **modes)
    print("thresholds:", seuils)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    main(ap.parse_args().quick)
