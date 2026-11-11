"""Data for the "simulations" figure (E1–E3 side by side).

1. Thumbnails: taken as is from the "thesis-plan" figure (plan_data.json): D(t) series of the Gissinger model
   (Γ = 0.9), 2D MHD snapshot of E2 (current density j and contour lines of a), ABC dynamo mode of E3
   (|B| on three faces, Rm = 12).
2. E1: frequency of zero crossings of D in the fine-grid simulations (results/e1_gissinger.json,
   "fine_grid", simulation_rate) and training and test values of Γ (config).
3. E3: growth rate λ(Rm) and interpolated thresholds (results/e3_abc.json).
4. E2: mean magnetic energy E_B = ½⟨|B|²⟩ in the stationary regime for the 11 values of η of E2, **recomputed**
   with the E2 solver (experiments/mhd2d.py) and its settings (N = 32, ν = 8e-3, α = 0.02, white forcing in
   the annulus 2 ≤ |k| ≤ 3, ε = 0.05 for u and B, 16 members, Δt = 0.01, burn-in 30): mean and standard deviation
   over 30 snapshots spaced 1 apart per member (seeds 300 + i, independent of those of E2). The raw data of
   E2 are not versioned, hence this recomputation.

Usage: python3 make_data.py  (≈ 3 min on 4 cores). Output: sim_data.json.
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # repo root
RES = ROOT / "experiments" / "results"
sys.path.insert(0, str(ROOT / "experiments"))

ETA_TRAIN = [4e-3 * 2 ** (k / 2) for k in range(6)]
ETA_TEST = [4e-3 * 2 ** (k / 2 + 0.25) for k in range(5)]


def e2_point(args):
    i, eta = args
    from mhd2d import MHD2D
    m = MHD2D(n=32, nu=8e-3, eta=eta, alpha=0.02, kf=(2.0, 3.0), eps_u=0.05, eps_b=0.05, batch=16, seed=300 + i)
    dt = 1e-2
    for _ in range(int(30.0 / dt)):
        m.step(dt)
    eb = []
    for _ in range(30):
        for _ in range(int(1.0 / dt)):
            m.step(dt)
        eb.append(m.diagnostics()["Eb"])
    eb = np.concatenate(eb)
    return {"eta": eta, "Eb_mean": float(eb.mean()), "Eb_std": float(eb.std()), "n": int(eb.size)}


def main():
    plan = json.loads((ROOT / "site" / "figures" / "thesis-plan" / "figure" / "data" / "plan_data.json").read_text())
    out = {"vignettes": plan}
    e1 = json.loads((RES / "e1_gissinger.json").read_text())
    out["e1"] = {
        "G_train": e1["config"]["G_train"], "G_test": e1["config"]["G_test"],
        "fine": [[g["Gamma"], g["simulation_rate"]] for g in e1["fine_grid"]],
        "n_traj": e1["config"]["trajectories_per_Gamma"], "t_keep": e1["config"]["kept_duration"],
    }
    e3 = json.loads((RES / "e3_abc.json").read_text())
    out["e3"] = {"rates": [[r["Rm"], r["lambda"]] for r in e3["rates"]], "thresholds": e3["interpolated_thresholds"],
                 "N": e3["config"]["N"], "dt": e3["config"]["dt"], "t_total": e3["config"]["t_total"]}
    etas = sorted(ETA_TRAIN + ETA_TEST)
    with Pool(4) as pool:
        pts = pool.map(e2_point, list(enumerate(etas)))
    out["e2"] = {"points": pts, "eta_train": ETA_TRAIN, "eta_test": ETA_TEST}
    (HERE / "sim_data.json").write_text(json.dumps(out, separators=(",", ":")))
    for p in pts:
        print(f"η = {p['eta']:.5f}  E_B = {p['Eb_mean']:.4f} ± {p['Eb_std']:.4f}")


if __name__ == "__main__":
    main()
