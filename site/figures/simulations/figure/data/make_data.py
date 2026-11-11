"""Données de la figure « simulations » (E1–E3 côte à côte).

1. Vignettes : reprises telles quelles de la figure « plan-these » (plan_data.json) : série D(t) du modèle de
   Gissinger (Γ = 0,9), instantané de MHD 2D de E2 (densité de courant j et isolignes de a), mode dynamo ABC de E3
   (|B| sur trois faces, Rm = 12).
2. E1 : fréquence des passages de D par zéro dans les simulations de la grille fine (resultats/e1_gissinger.json,
   « grille_fine », taux_simulation) et valeurs de Γ d'entraînement et de test (config).
3. E3 : taux de croissance λ(Rm) et seuils interpolés (resultats/e3_abc.json).
4. E2 : énergie magnétique moyenne E_B = ½⟨|B|²⟩ en régime stationnaire pour les 11 valeurs de η de E2, **recalculée**
   avec le solveur de E2 (experiences/mhd2d.py) et ses réglages (N = 32, ν = 8e-3, α = 0,02, forçage blanc dans
   la couronne 2 ≤ |k| ≤ 3, ε = 0,05 pour u et B, 16 membres, Δt = 0,01, mise en régime 30) : moyenne et écart-type
   sur 30 instantanés espacés de 1 par membre (graines 300 + i, indépendantes de celles de E2). Les données brutes de
   E2 ne sont pas versionnées, d'où ce recalcul.

Usage : python3 make_data.py  (≈ 3 min sur 4 cœurs). Sortie : sim_data.json.
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RES = ROOT / "experiences" / "resultats"
sys.path.insert(0, str(ROOT / "experiences"))

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
    plan = json.loads((ROOT / "figures" / "plan-these" / "figure" / "data" / "plan_data.json").read_text())
    out = {"vignettes": plan}
    e1 = json.loads((RES / "e1_gissinger.json").read_text())
    out["e1"] = {
        "G_train": e1["config"]["G_train"], "G_test": e1["config"]["G_test"],
        "fine": [[g["Gamma"], g["taux_simulation"]] for g in e1["grille_fine"]],
        "n_traj": e1["config"]["trajectoires_par_Gamma"], "t_keep": e1["config"]["duree_gardee"],
    }
    e3 = json.loads((RES / "e3_abc.json").read_text())
    out["e3"] = {"rates": [[r["Rm"], r["lambda"]] for r in e3["taux"]], "thresholds": e3["seuils_interpoles"],
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
