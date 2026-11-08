#!/usr/bin/env python3
"""data_ch04.py: scene data for unit ch04 that tools/data_existing.py does not provide (READY scenes, decision D4).

No computation of physics: the value below is the RECORDED output of an existing code block of the site
(prep module P4, exercise 14: Lyapunov exponents of the Gissinger model by the QR method), read from the page
text where the site prints it. Only cheap bookkeeping is derived (1 / exponent).

Sources -> outputs:
  en/prep/p4-systemes-dynamiques/index.qmd  (exercise 14: "mu, nu, G = 0.119, 0.1, 0.9" and the printed
      "# T = 2000 : exponents ≈ …", "# T = 4000 : exponents ≈ …")  ->  data/ch04_lyapunov.json  (04.4)
Every output carries meta = {source, sha256, generator, extracted, stamp, note, anchor}; a file is rewritten only
when its content changes (the extraction date is ignored), as in data_existing.py.

Usage: python3 -I tools/data_ch04.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import datetime, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else "/home/user/milady-2027"
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_ch04.py"


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def lyapunov():
    rel = "en/prep/p4-systemes-dynamiques/index.qmd"
    lines = open(os.path.join(REPO, rel), encoding="utf-8").read().split("\n")
    out = {}
    head = next(i for i, l in enumerate(lines) if re.match(r"^\d+\.\s+\*\*.*Lyapunov exponents of the Gissinger model", l))
    par = next(i for i in range(head, head + 40) if re.match(r"^\s*mu, nu, G = ", lines[i]))
    mu, nu, G = (float(x) for x in re.findall(r"[\d.]+", lines[par].split("=")[1]))
    for i in range(par, par + 60):
        m = re.match(r"^# T = (\d+) : exponents ≈ ([+\-−][\d.]+), ([+\-−][\d.]+), ([+\-−][\d.]+)", lines[i])
        if m:
            out[m.group(1)] = {"exponents": [float(x.replace("−", "-")) for x in m.group(2, 3, 4)], "line": i + 1}
    if "4000" not in out:
        raise SystemExit("data_ch04: exercise 14 output for T = 4000 not found in " + rel)
    lam = out["4000"]["exponents"][0]
    return {
        "meta": {"source": rel, "sha256": sha(rel), "generator": GEN, "extracted": datetime.date.today().isoformat(),
                 "stamp": "P4 · exercise 14 · Lyapunov exponents",
                 "anchor": f"{rel}:{out['4000']['line']}",
                 "note": ("recorded output of the site's own code (P4 exercise 14: Gissinger model, QR method, RK4 dt 0.02, "
                          "renormalised every 25 steps); read from the page text, nothing recomputed; Gissinger 2012 "
                          "reports about 0.1. The letter lambda is not used on screen (symbol sheet): 'Lyapunov exponent'.")},
        "model": {"mu": mu, "nu": nu, "Gamma": G},
        "runs": {T: v for T, v in sorted(out.items(), key=lambda kv: int(kv[0]))},
        "largest": lam,
        "lyapunov_time": round(1.0 / lam, 4),
    }


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    strip = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if strip(old) == strip(doc):
        print(f"[data_ch04] {name}: unchanged")
        return
    if CHECK:
        print(f"[data_ch04] {name}: WOULD CHANGE")
        return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"[data_ch04] {name}: written")


if __name__ == "__main__":
    write("ch04_lyapunov.json", lyapunov())
