#!/usr/bin/env python3
"""data_ch07.py: scene data for unit ch07 that tools/data_existing.py does not provide (READY scenes, decision D4).

No simulation, no training: recorded results and stored snapshots only.
  data/ch07_mirror.json  (07.1-07.4)
    ref_sym_085: a seeded subsample of 2,000 stored reference snapshots at Gamma = 0.85 (data/e1_samples_0.85.json, the
                 first rows of the reference array) followed by their images under S = diag(-1, -1, 1): symmetric by
                 construction, as the report's reference is (R:786); dEdt = mu Q^2 - nu D^2 + Gamma V - V^2 + Q D V
                 evaluated on each row (bookkeeping, no integration); p_positive = 1/2.
    runs:        training runs per Gamma and the share pointing up, from e1_gissinger.json donnees P(D>0)_train and
                 config.trajectoires_par_Gamma (R:871).
    asym:        the floor sqrt(2/pi) 1/2 / sqrt(n_gen) (R:832) and the summary values the scenes print (from
                 data/e1_eval.json per-Gamma two-seed means, rounded as the report prints them).
    check3:      control residual of degree 3 at the test values (resume.test.liou_test_moy) and its n_gen floor.
  data/ch07_spike.json   (07.5-07.6)
    distance (test energy distance of C and of E = C projected per sample, ratio, floor), spread (sigma dE/dt of E),
    also_worse (SW1 and Rice-error ratios), juries (config.reglage_fin).
Every output carries meta = {source, sha256, generator, extracted, stamp, note, sources}; a file is rewritten only when
its content changes (the extraction date is ignored).

Usage: python3 -I tools/data_ch07.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import base64, datetime, hashlib, json, math, os, random, struct, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_ch07.py"
E1 = "experiences/resultats/e1_gissinger.json"
S85 = "video/data/e1_samples_0.85.json"
EV = "video/data/e1_eval.json"


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def f32(p):
    raw = base64.b64decode(p["b64"]); return list(struct.unpack("<%df" % (len(raw) // 4), raw))


def pack(vals, shape):
    return {"dtype": "f32", "shape": shape, "b64": base64.b64encode(struct.pack("<%df" % len(vals), *vals)).decode()}


def meta(stamp, note, srcs):
    return {"source": srcs[0], "sha256": sha(srcs[0]), "generator": GEN, "extracted": datetime.date.today().isoformat(),
            "stamp": stamp, "note": note, "sources": [{"path": s, "sha256": sha(s)} for s in srcs]}


def mirror(e1, ev):
    cfg = e1["config"]; mu, nu = cfg["mu"], cfg["nu"]
    sm = json.load(open(os.path.join(REPO, S85))); G = sm["gamma"]
    x = f32(sm["variants"]["ref"]["x"]); n = sm["variants"]["ref"]["n"]
    rows = random.Random(85).sample(range(n), 2000); rows.sort()
    pts = [(x[3 * i], x[3 * i + 1], x[3 * i + 2]) for i in rows]
    pts = pts + [(-q, -d, v) for (q, d, v) in pts]
    flat = [c for p in pts for c in p]
    dedt = [mu * q * q - nu * d * d + G * v - v * v + q * d * v for (q, d, v) in pts]
    ppos = sum(1 for p in pts if p[1] > 0) / len(pts)
    ntr = cfg["trajectoires_par_Gamma"]
    runs = []
    for g in ("0.8", "0.86"):
        p = e1["donnees"][g]["P(D>0)_train"]; up = round(p * ntr)
        assert abs(up - p * ntr) < 1e-9
        runs.append({"gamma": float(g), "n_runs": ntr, "n_up": up, "p_up": p})
    pg = lambda v: ev["variants"][v]["per_gamma"]
    def at(v, G):
        for part in ("train", "test"):
            for g, a in zip(pg(v)[part]["Gamma"], pg(v)[part]["asym"]):
                if abs(g - G) < 1e-9: return a
    Btr, Bte, Call = pg("B_augmentation")["train"]["asym"], pg("B_augmentation")["test"]["asym"], pg("C_equivariant")["train"]["asym"] + pg("C_equivariant")["test"]["asym"]
    ngen = cfg["n_gen"]
    asym = {"floor": round(math.sqrt(2 / math.pi) * 0.5 / math.sqrt(ngen), 4), "n": ngen,
            "formula": "sqrt(2/pi) * 1/2 / sqrt(n) (R:832)",
            "summary": {"A": {"at_0_86": round(at("A_reference", 0.86), 3), "at_0_87": round(at("A_reference", 0.87), 4), "at_0_85": round(at("A_reference", 0.85), 4)},
                        "B": {"train_range": [round(min(Btr), 3), round(max(Btr), 3)], "test_range": [round(min(Bte), 3), round(max(Bte), 3)], "test_mean": round(sum(Bte) / len(Bte), 3)},
                        "C": {"range": [round(min(Call), 4), round(max(Call), 4)]}}}
    r = e1["resume"]; fl = ev["noise_floor"]["n_gen"]["liou_test_moy"]
    check3 = {"A": round(r["A_reference"]["test"]["liou_test_moy"], 4), "B": round(r["B_augmentation"]["test"]["liou_test_moy"], 4),
              "C": round(r["C_equivariant"]["test"]["liou_test_moy"], 4), "floor": round(fl, 4), "n_laws": 10, "label": "ten crowd laws never imposed"}
    return {"meta": meta("DATA · E1 · mirror, runs, asymmetry", "ref_sym_085: stored snapshots + their mirror images (symmetric by construction); runs, asym summary and check3 from recorded results", [E1, S85, EV]),
            "ref_sym_085": {"gamma": G, "n": len(pts), "x": pack(flat, [len(pts), 3]), "dEdt": pack(dedt, [len(pts)]), "p_positive": ppos},
            "runs": runs, "asym": asym, "check3": check3}


def spike(e1, ev):
    r = e1["resume"]; C, E = r["C_equivariant"]["test"], r["E_projection_C"]["test"]
    ratio = E["energie"] / C["energie"]
    assert round(ratio) == 9, ratio
    rf = e1["config"]["reglage_fin"]
    return {"meta": meta("DATA · E1 · per-sample projection (E)", "test Gamma, mean of 2 seeds; float64 evaluation", [E1, EV]),
            "distance": {"C": round(C["energie"], 5), "E": round(E["energie"], 4), "ratio": round(ratio), "floor": round(ev["noise_floor"]["n_gen"]["energie"], 5), "scope": "test Γ, mean of 2 seeds"},
            "spread": {"E": float("%.3g" % E["dEdt_std"]), "C": round(C["dEdt_std"], 3)},
            "also_worse": {"sw1_ratio": round(E["sw1"] / C["sw1"]), "rice_error_ratio": round(E["erreur_taux_rice"] / C["erreur_taux_rice"], 1)},
            "juries": {"gammas_per_step": rf["gammas_par_pas"], "samples_per_gamma": rf["echantillons_par_gamma"], "half": rf["echantillons_par_gamma"] // 2, "beta": rf["beta"], "n_laws": 9}}


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    st = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if st(old) == st(doc): print(f"[data_ch07] {name}: unchanged"); return
    if CHECK: print(f"[data_ch07] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f: json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_ch07] {name}: written")


if __name__ == "__main__":
    e1 = json.load(open(os.path.join(REPO, E1))); ev = json.load(open(os.path.join(REPO, EV)))
    write("ch07_mirror.json", mirror(e1, ev)); write("ch07_spike.json", spike(e1, ev))
