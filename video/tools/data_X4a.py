#!/usr/bin/env python3
"""data_X4a.py: first-round (E1) anchor values for scene X4.5 (tier 0, the next round), read from the recorded results.

No simulation, no training (decision D4). Reads experiences/resultats/e1_gissinger.json and writes
data/X4a_tier0_anchor.json with meta = {source, sha256, generator, extracted, stamp, note}:
  first_round.asym_C_min / asym_C_max   model C, |P(D>0) - 1/2| per Gamma (seed mean), min and max over the 21 Gamma
  first_round.asym_floor                Monte Carlo floor E|p_hat - 1/2| = sqrt(2/pi) / (2 sqrt(n_gen)) (R:832)
  first_round.resid_loss / resid_control / resid_ratio   degree-3 crowd-law residual at test Gamma, F vs F0 (R:875)
  first_round.rice_far_cumulative / rice_near_cumulative / rice_far_pointwise_max   Rice on model C (seed 0) vs the
        counted rate, cumulative sum|Rice - count| / sum count for Gamma >= 0.89 and 0.865-0.885, and the largest pointwise
        relative error for Gamma >= 0.89 (R:883)
The extractor asserts the rounded values the report prints (0.0037, 0.0048, 0.0040, x1.98, 14 %, 42 %, 65 %).
Rewrites the file only when its content changes (the extraction date is ignored).
Usage: python3 -I tools/data_X4a.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import datetime, hashlib, json, math, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_X4a.py"
E1 = "experiences/resultats/e1_gissinger.json"


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def build():
    e1 = json.load(open(os.path.join(REPO, E1)))
    ev, res, cfg = e1["evaluation"], e1["resume"], e1["config"]
    asym = [r["asym"][0] for sp in ("train", "test") for r in ev["C_equivariant"][sp]]
    a_min, a_max = min(asym), max(asym)
    floor = math.sqrt(2 / math.pi) / (2 * math.sqrt(cfg["n_gen"]))
    r_loss, r_ctrl = res["F_stationnarite_C"]["test"]["liou_test_moy"], res["F0_temoin_C"]["test"]["liou_test_moy"]
    fine = e1["grille_fine"]
    def cum(lo, hi):
        sel = [r for r in fine if lo - 1e-9 <= r["Gamma"] <= hi + 1e-9]
        return sum(abs(r["taux_rice_modele"] - r["taux_simulation"]) for r in sel) / sum(r["taux_simulation"] for r in sel)
    far, near = cum(0.89, 1.0), cum(0.865, 0.885)
    pw = max(abs(r["taux_rice_modele"] - r["taux_simulation"]) / r["taux_simulation"] for r in fine if r["Gamma"] >= 0.89 - 1e-9 and r["taux_simulation"] > 0)
    checks = [(round(a_min, 4), 0.0037), (round(a_max, 4), 0.0048), (round(floor, 4), 0.004), (round(r_loss / r_ctrl, 2), 0.5), (round(r_ctrl / r_loss, 2), 1.98),
              (round(100 * far), 14), (round(100 * near), 42), (round(100 * pw), 65)]
    for got, want in checks:
        if abs(got - want) > 1e-9:
            raise SystemExit(f"data_X4a: {got} differs from the report's {want}")
    fr = {"asym_C_min": round(a_min, 5), "asym_C_max": round(a_max, 5), "asym_floor": round(floor, 5), "n_gen": cfg["n_gen"], "seeds": len(cfg["seeds"]),
          "resid_loss": round(r_loss, 5), "resid_control": round(r_ctrl, 5), "resid_ratio": round(r_ctrl / r_loss, 3),
          "rice_far_cumulative": round(far, 4), "rice_near_cumulative": round(near, 4), "rice_far_pointwise_max": round(pw, 4),
          "rice_ranges": {"far": [0.89, 1.0], "near": [0.865, 0.885]}}
    return {"meta": {"source": E1, "sha256": sha(E1), "generator": GEN, "extracted": datetime.date.today().isoformat(),
                     "stamp": "DATA · E1 · first round of tier 0",
                     "note": "recorded E1 results (2 seeds); asym per Gamma = seed mean; Rice on model C seed 0 (grille_fine); R:832, R:875, R:883"},
            "first_round": fr}


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    strip = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if strip(old) == strip(doc):
        print(f"[data_X4a] {name}: unchanged"); return
    if CHECK:
        print(f"[data_X4a] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_X4a] {name}: written")


if __name__ == "__main__":
    write("X4a_tier0_anchor.json", build())
