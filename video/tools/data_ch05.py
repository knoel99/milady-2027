#!/usr/bin/env python3
"""data_ch05.py: scene data for unit ch05 that tools/data_existing.py does not provide (READY scenes, decision D4).

No simulation, no integration. Two blocks, one file:
  strip  (05.2): membership |D| < h_Rice of the 8,000 stored reference snapshots at Gamma = 0.93, read from
         data/e1_samples_0.93.json (itself extracted by data_existing.py from the E1 sample archive), and
         Ddot = -nu D + V Q evaluated on each stored snapshot (bookkeeping, as the report's #m-rice estimator does).
  check  (05.3): the report's cumulative error sum|Rice(ref) - count| / sum count (R:883) over the two Gamma
         ranges, recomputed from the recorded grille_fine of experiences/resultats/e1_gissinger.json; the
         extractor asserts that the rounded percentages equal the report's 4 and 6.
Output: data/ch05_rice.json, meta = {source, sha256, generator, extracted, stamp, note, sources}; rewritten only
when its content changes (the extraction date is ignored), as in data_existing.py.

Usage: python3 -I tools/data_ch05.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import base64, datetime, hashlib, json, os, struct, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_ch05.py"
E1 = "experiences/resultats/e1_gissinger.json"
SAMP = "video/data/e1_samples_0.93.json"


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def f32(p):
    raw = base64.b64decode(p["b64"])
    return list(struct.unpack("<%df" % (len(raw) // 4), raw))


def build():
    e1 = json.load(open(os.path.join(REPO, E1)))
    cfg = e1["config"]
    h, nu = cfg["h_Rice"], cfg["nu"]
    sm = json.load(open(os.path.join(REPO, SAMP)))
    ref = sm["variants"]["ref"]
    x = f32(ref["x"]); n = ref["n"]
    assert len(x) == 3 * n
    rows = []
    for i in range(n):
        q, d, v = x[3 * i], x[3 * i + 1], x[3 * i + 2]
        if abs(d) < h:
            rows.append((d, i, abs(-nu * d + v * q)))
    rows.sort()
    idx = [r[1] for r in rows]
    med = sorted(rows, key=lambda r: r[2])[len(rows) // 2][1]
    strip = {"gamma": sm["gamma"], "h": h, "coef_D": nu, "n_total": n, "n_in_strip": len(idx),
             "strip_index": idx, "highlight_index": med,
             "note": ("membership and Ddot = -0.1 D + V Q computed on stored snapshots; the Rice estimate of this single "
                      "box is not quoted (the measured comparison is the fine grid of 05.3, R:883)")}
    fine = e1["grille_fine"]
    ranges = []
    for key, label, lo, hi, want in (("near", "near the threshold", 0.865, 0.885, 4), ("above", "above", 0.89, 1.0, 6)):
        sel = [r for r in fine if lo - 1e-9 <= r["Gamma"] <= hi + 1e-9]
        err = sum(abs(r["taux_rice_ref"] - r["taux_simulation"]) for r in sel) / sum(r["taux_simulation"] for r in sel)
        pct = round(100 * err)
        if pct != want:
            raise SystemExit(f"data_ch05: cumulative error {key} = {err:.4f}, report says {want}% (R:883)")
        ranges.append({"key": key, "label": label, "gamma_min": lo, "gamma_max": hi, "n": len(sel),
                       "cumulative_error": round(err, 4), "percent": pct})
    check = {"definition": "sum over the range of |Rice on reference snapshots - counted rate| / sum of counted rate (R:883)",
             "h": h, "ranges": ranges}
    return {
        "meta": {"source": E1, "sha256": sha(E1), "generator": GEN, "extracted": datetime.date.today().isoformat(),
                 "stamp": "DATA · E1 · Rice strip and check",
                 "sources": [{"path": E1, "sha256": sha(E1)}, {"path": SAMP, "sha256": sha(SAMP)}],
                 "note": "strip: stored reference snapshots at Gamma 0.93 (no time order); check: recorded grille_fine, R:883"},
        "strip": strip, "check": check}


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    strip = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if strip(old) == strip(doc):
        print(f"[data_ch05] {name}: unchanged"); return
    if CHECK:
        print(f"[data_ch05] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_ch05] {name}: written")


if __name__ == "__main__":
    write("ch05_rice.json", build())
