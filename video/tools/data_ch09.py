"""data_ch09.py: scene data for unit ch09 that data/ does not provide (READY scenes, decision D4: no run).

Bookkeeping only (sums, ratios) over RECORDED results of experiences/resultats/e1_gissinger.json (grille_fine, config),
data/e1_eval.json and data/e2_eval.json. Nothing is simulated or re-trained.

Sources -> output:
  experiences/resultats/e1_gissinger.json (grille_fine: taux_simulation, taux_rice_ref, taux_rice_modele (C, seed 0),
      taux_rice_modele_F, pont_*; config)  ->  data/ch09_rice.json  (09.1, 09.2, 09.4, 09.5, ch09.Q)
  The cumulative error is sum |rice - count| / sum count over a range of Γ (en/rapport/index.qmd:883); the extractor
  asserts the report's rounded numbers (42 / 14 % for C, 32 / 23 % for F, pointwise mean 17 %, max 65 %).
  'factors' (09.5): best test distribution distance / noise floor (E1) and best spectrum error / honest floor (E2),
  read from data/e1_eval.json and data/e2_eval.json (en/rapport/index.qmd:873, :1039: "about twice", "six times").
Usage: python3 -I tools/data_ch09.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import datetime, hashlib, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_ch09.py"
SRC = "experiences/resultats/e1_gissinger.json"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def cum(rows, key, lo, hi):
    sel = [r for r in rows if lo - 1e-9 <= r["Gamma"] <= hi + 1e-9]
    num = sum(abs(r[key] - r["taux_simulation"]) for r in sel)
    den = sum(r["taux_simulation"] for r in sel)
    return {"gamma_min": lo, "gamma_max": hi, "n": len(sel), "cumulative_error": round(num / den, 4), "percent": round(100 * num / den)}


def rice():
    d = json.load(open(os.path.join(REPO, SRC)))
    rows = sorted(d["grille_fine"], key=lambda r: r["Gamma"])
    cfg = d["config"]
    G = [round(r["Gamma"], 4) for r in rows]
    last_zero = max(g for g, r in zip(G, rows) if r["taux_simulation"] == 0 and g < 0.9)
    first = min(g for g, r in zip(G, rows) if r["taux_simulation"] > 0)
    near, far = (first, 0.885), (0.89, 1.0)
    check = {}
    for name, key in (("C", "taux_rice_modele"), ("F", "taux_rice_modele_F"), ("ref", "taux_rice_ref")):
        check[name] = {"near": cum(rows, key, *near), "far": cum(rows, key, *far)}
    pf = [(g, abs(r["taux_rice_modele"] - r["taux_simulation"]) / r["taux_simulation"]) for g, r in zip(G, rows) if g >= 0.89 - 1e-9]
    vals = [round(v, 4) for _, v in pf]
    top2 = sorted(pf, key=lambda p: -p[1])[:2]
    check["C"]["pointwise_far"] = {"gamma": [g for g, _ in pf], "values": vals, "mean": round(sum(vals) / len(vals), 4),
                                   "mean_percent": round(100 * sum(vals) / len(vals)), "max": round(top2[0][1], 4),
                                   "max_percent": round(100 * top2[0][1]), "argmax": sorted(g for g, _ in top2)}
    assert (check["C"]["near"]["percent"], check["C"]["far"]["percent"], check["F"]["near"]["percent"], check["F"]["far"]["percent"]) == (42, 14, 32, 23), check
    assert check["C"]["pointwise_far"]["mean_percent"] == 17 and check["C"]["pointwise_far"]["max_percent"] == 65
    below = [(g, r) for g, r in zip(G, rows) if g <= last_zero + 1e-9]
    bmax = max(below, key=lambda p: p[1]["taux_rice_modele"])
    on = rows[G.index(first)]
    ntraj, keep = cfg.get("trajectoires_par_Gamma", 16), cfg.get("duree_gardee", 3000)
    counted = [round(r["taux_simulation"] * ntraj * keep) for r in rows]
    e1 = json.load(open(os.path.join(HERE, "data/e1_eval.json")))
    e2 = json.load(open(os.path.join(HERE, "data/e2_eval.json")))
    best_e1 = min(e1["variants"][k]["mean"]["test"]["energie"] for k in ("A_reference", "B_augmentation", "C_equivariant"))
    fl_e1 = e1["noise_floor"]["n_gen"]["energie"]
    e2v = {k: v["mean"]["test"]["err_spectre_log10"] for k, v in e2["variants"].items() if k != "reference_sous_echantillon"}
    fl_e2 = e2["variants"]["reference_sous_echantillon"]["mean"]["train"]["err_spectre_log10"]
    ref_sd = e1["reference"]["dEdt_std"]
    sd = lambda v: e1["variants"][v]["mean"]["test"]["dEdt_std"] / ref_sd
    return {
        "meta": {"source": SRC, "sha256": sha(os.path.join(REPO, SRC)), "generator": GEN, "extracted": datetime.date.today().isoformat(),
                 "stamp": "DATA · E1 · fine grid · Rice on C and F, seed 0",
                 "sources": ["data/e1_eval.json", "data/e2_eval.json"],
                 "note": ("cumulative error = sum|Rice - count| / sum count over the range (R:883); model C and F seed 0, "
                          "20,000 generated snapshots per Γ (R:801); rates per unit time; counted crossings = rate x "
                          "trajectories x kept duration; factors = best / floor (R:873, R:1039)")},
        "n_settings": len(rows), "n_unseen": sum(1 for r in rows if not r["dans_entrainement"]), "n_generated_per_gamma": 20000,
        "threshold": {"last_zero": last_zero, "first_nonzero": first},
        "check": check,
        "below": {"gamma_max": last_zero, "C_rate_max": round(bmax[1]["taux_rice_modele"], 7), "C_rate_max_gamma": bmax[0],
                  "C_bridge_max": max(r["pont_modele"] for _, r in below), "truth": 0},
        "onset": {"gamma": first, "count": on["taux_simulation"], "C": round(on["taux_rice_modele"], 7),
                  "ratio": round(on["taux_simulation"] / on["taux_rice_modele"], 1)},
        "overshoot": [{"gamma": g, "count": round(r["taux_simulation"], 6), "C": round(r["taux_rice_modele"], 6)}
                      for g, r in zip(G, rows) if g in (0.875, 0.88)],
        "counted_crossings": {"gamma": G, "n": counted, "trajectories": ntraj, "kept_duration": keep,
                              "min_nonzero": min(c for c in counted if c > 0), "max": max(counted)},
        "factors": {"e1_best_over_floor": round(best_e1 / fl_e1, 2), "e2_best_over_honest_floor": round(min(e2v.values()) / fl_e2, 2)},
        "spread_ratio": {"control_C": round(sd("F0_temoin_C"), 2), "loss_C": round(sd("F_stationnarite_C"), 2),
                         "loss_Cshort": round(sd("F_stationnarite_Ccourt"), 1), "control_Cshort": round(sd("F0_temoin_Ccourt"), 2)},
    }


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    strip = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if strip(old) == strip(doc):
        print(f"[data_ch09] {name}: unchanged"); return
    if CHECK:
        print(f"[data_ch09] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_ch09] {name}: written")


if __name__ == "__main__":
    write("ch09_rice.json", rice())
