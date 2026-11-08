"""data_ch11.py: scene data for unit ch11 (decision D4: no run; bookkeeping over recorded results only).

Sources -> outputs:
  data/e1_eval.json, data/e2_eval.json, data/e3_growth.json, data/digest.json, data/ch09_rice.json (themselves extracted
  from experiences/resultats/e1_gissinger.json, e2_mhd2d.json, e3_abc.json, digest.md)
      -> data/ch11_measured.json  (11.1 left column, 11.2 chips): the headline numbers of E1-E3.
  the cloud result files of the six bets (data/palier1_sweep.json, palier2_abc3d.json, palier2_tg3d.json,
  fm3d_eval.json, tier3_vks.json, tier4_dresdyn.json), when present
      -> data/ch11_ledger.json  (11.1 right column): one row per bet, the file's own verdict copied (never computed);
         'pending: true' at the root while none of the three tier-2 files is present (unit notes of script/ch11.json).
A file is rewritten only when its content changes (the extraction date is ignored).
Usage: python3 -I tools/data_ch11.py [--check]
"""
import datetime, hashlib, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
CHECK = "--check" in sys.argv[1:]
GEN = "tools/data_ch11.py"
TODAY = datetime.date.today().isoformat()


def load(name):
    return json.load(open(os.path.join(DATA, name)))


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def measured():
    e1, e2, e3, dg, rc = load("e1_eval.json"), load("e2_eval.json"), load("e3_growth.json"), load("digest.json"), load("ch09_rice.json")
    v1 = e1["variants"]
    asym = [a for sp in ("train", "test") for a in v1["C_equivariant"]["per_gamma"][sp]["asym"]]
    A, C, E = (v1[k]["mean"]["test"]["energie"] for k in ("A_reference", "C_equivariant", "E_projection_C"))
    v2 = e2["variants"]
    tab = dg["tables"][4]
    hdr = tab.get("header") or tab.get("columns")
    row = next(r for r in tab["rows"] if "recalage" in str(r[0]))
    sig = row[hdr.index("σ(D)/σ_ref")]
    assert abs(sig - 8.64e-4) < 1e-6, sig
    doc = {
        "meta": {"source": "data/e1_eval.json", "sha256": sha(os.path.join(DATA, "e1_eval.json")), "generator": GEN, "extracted": TODAY,
                 "stamp": "DATA · E1–E3 · headline results",
                 "sources": [{"path": "data/" + n, "sha256": sha(os.path.join(DATA, n))} for n in ("e2_eval.json", "e3_growth.json", "digest.json", "ch09_rice.json")],
                 "note": "test-value means; E1 2 seeds, E2 1 seed; ratios are bookkeeping (R:873, R:1027, R:1112, R:883)"},
        "e1": {"seeds": len(e1["training"]["C_equivariant"]), "mirror": {"asym_C_min": min(asym), "asym_C_max": max(asym)},
               "distance": {"A": A, "C": C, "ratio": round(A / C, 1)}, "per_snapshot": {"E": E, "C": C, "ratio": round(E / C)},
               "rice": {"model": "C", "seed": 0, "n_per_gamma": rc["n_generated_per_gamma"], "far": {"gamma_min": rc["check"]["C"]["far"]["gamma_min"], "percent": rc["check"]["C"]["far"]["percent"]},
                        "near": {"gamma_min": rc["check"]["C"]["near"]["gamma_min"], "gamma_max": rc["check"]["C"]["near"]["gamma_max"], "percent": rc["check"]["C"]["near"]["percent"]},
                        "pointwise_max_percent": rc["check"]["C"]["pointwise_far"]["max_percent"]}},
        "e2": {"seeds": 1, "grid": "32²", "dynamo": False,
               "divergence": {"free": round(v2["V0_libre"]["mean"]["test"]["div_rel_u"], 3), "potentials": float("%.2g" % ((v2["V4_potentiels"]["mean"]["test"]["div_rel_u"] + v2["V4_potentiels"]["mean"]["test"]["div_rel_b"]) / 2))},
               "crowd": {"V4": round(v2["V4_potentiels"]["mean"]["test"]["dist_energie_features"], 2), "control": round(v2["V5_temoin"]["mean"]["test"]["dist_energie_features"], 2), "V5": round(v2["V5_potentiels_stat"]["mean"]["test"]["dist_energie_features"], 3)},
               "per_snapshot": {"sigma_ratio": sig}},
        "e3": {"grid": "32³", "thresholds": e3["thresholds"], "published": e3["published_windows"]["bounds"], "published_third_approx": True,
               "unresolved_at": 17.5, "divergence_max": float("%.3g" % max(e3["div_rel"]))},
        "caveats": ["toy problems", "interpolation only", "CPU, 4 cores, no GPU", "prospective report"],
    }
    assert doc["e1"]["distance"]["ratio"] == 4.6 and doc["e1"]["per_snapshot"]["ratio"] == 9, doc["e1"]
    return doc


BETS = [("tier1_check", "10.3", "palier1_sweep.json"), ("abc64", "10.4", "palier2_abc3d.json"), ("tg", "10.5", "palier2_tg3d.json"),
        ("fm3d", "10.7", "fm3d_eval.json"), ("vks", "10.9", "tier3_vks.json"), ("dresdyn", "10.9", "tier4_dresdyn.json")]


def ledger():
    rows, srcs = [], []
    for bid, scene, name in BETS:
        p = os.path.join(DATA, name)
        r = {"id": bid, "scene": scene, "file": "data/" + name, "state": "awaiting", "verdict_text": None, "stamp": None, "sha8": None}
        if os.path.exists(p):
            d = json.load(open(p)); m = d.get("meta", {})
            if not (d.get("pending") or m.get("pending")):
                r.update(state=d.get("verdict", "inconclusive"), verdict_text=d.get("verdict_text"), stamp=m.get("stamp"), sha8=(m.get("sha256") or "")[:8])
            srcs.append({"path": "data/" + name, "sha256": sha(p)})
        rows.append(r)
    st = [r["state"] for r in rows]
    n_in = sum(s != "awaiting" for s in st)
    tier2 = any(os.path.exists(os.path.join(DATA, n)) for n in ("palier2_abc3d.json", "palier2_tg3d.json", "fm3d_eval.json"))
    return {"meta": {"source": "the six bet files (none present yet)" if not srcs else srcs[0]["path"], "sha256": srcs[0]["sha256"] if srcs else None, "generator": GEN, "extracted": TODAY,
                     "stamp": "LEDGER · bets of the PhD plan", "sources": srcs, "note": "verdicts copied from the converters' files, never computed here"},
            "pending": not tier2, "rows": rows,
            "fields": {"n_bets": len(rows), "n_in": n_in, "n_met": st.count("met"), "n_not_met": st.count("not_met"), "n_inconclusive": st.count("inconclusive"),
                       "n_awaiting": st.count("awaiting"), "any_met": "met" in st, "any_not_met": "not_met" in st, "any_inconclusive": "inconclusive" in st,
                       "top_awaiting": rows[4]["state"] == "awaiting" and rows[5]["state"] == "awaiting"}}


def write(name, doc):
    p = os.path.join(DATA, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    strip = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if strip(old) == strip(doc):
        print(f"[data_ch11] {name}: unchanged"); return
    if CHECK:
        print(f"[data_ch11] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_ch11] {name}: written")


if __name__ == "__main__":
    write("ch11_measured.json", measured())
    write("ch11_ledger.json", ledger())
