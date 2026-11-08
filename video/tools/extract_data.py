#!/usr/bin/env python3
"""extract_data.py: turn repository results into the small, scene-ready JSON files under data/.
Scenes never read the repository directly: this script is the only bridge, and each output keeps
the source path and its SHA-256 so a changed result is detected by the build (hash of data/*.json).
New campaigns (palier1/2, fm3d, VKS, DRESDYN) get one function each here when their files exist.
Usage: python3 -I tools/extract_data.py [--repo /home/user/milady-2027]
"""
import datetime, hashlib, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = sys.argv[sys.argv.index("--repo") + 1] if "--repo" in sys.argv else "/home/user/milady-2027"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def e1_rate():
    src = os.path.join(REPO, "experiences/resultats/e1_gissinger.json")
    d = json.load(open(src))
    g = d["grille_fine"]
    return {
        "meta": {"source": "experiences/resultats/e1_gissinger.json", "sha256": sha(src),
                 "extracted": datetime.date.today().isoformat(),
                 "stamp": "DATA · E1 · Gissinger three-mode model · 16 trajectories per Γ"},
        "x": {"label": "Γ, control parameter", "values": [r["Gamma"] for r in g],
              "train": [bool(r["dans_entrainement"]) for r in g]},
        "y": {"label": "reversal rate (per unit time)", "unit": ""},
        "series": [
            {"name": "simulation", "kind": "simulated", "field": "b", "y": [r["taux_simulation"] for r in g]},
            {"name": "generative model (Rice estimate)", "kind": "generated", "field": "b", "y": [r["taux_rice_modele"] for r in g]},
        ],
    }


def palier1_eta_sweep():
    """Pending: the palier1_mhd2d campaign has not run yet. When its catalogue exists, read it here
    (python -m milady.catalog sims --campaign palier1_mhd2d). With --provisional-e2, write a PROVISIONAL
    stand-in from E2, which used the same 11 eta values, grid and solver: the relative error of the
    generated magnetic energy per eta (base model and Rice-weighted 'recalage' variant)."""
    if "--provisional-e2" not in sys.argv:
        return None
    src = os.path.join(REPO, "experiences/resultats/e2_mhd2d.json")
    d = json.load(open(src))
    etas = sorted(d["en_loi"], key=float)
    return {
        "meta": {"source": "experiences/resultats/e2_mhd2d.json", "sha256": sha(src),
                 "extracted": datetime.date.today().isoformat(), "provisional": True,
                 "stamp": "PROVISIONAL · E2 stand-in (same η grid) · awaiting palier1_mhd2d"},
        "x": {"label": "η, magnetic diffusivity", "values": [float(e) for e in etas],
              "train": [d["en_loi"][e]["split"] == "train" for e in etas]},
        "y": {"label": "relative error, magnetic energy"},
        "series": [
            {"name": "generated, base", "kind": "generated", "field": "metric", "y": [d["en_loi"][e]["base"]["err_Eb_rel"] for e in etas]},
            {"name": "generated, recalibrated", "kind": "generated", "field": "model", "y": [d["en_loi"][e]["recalage"]["err_Eb_rel"] for e in etas]},
        ],
    }


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    for name, fn in [("e1_rate", e1_rate), ("palier1_eta_sweep", palier1_eta_sweep)]:
        out = fn()
        p = os.path.join(HERE, "data", name + ".json")
        if out is None:
            print(f"{name}: pending (no source data yet)")
            continue
        new = json.dumps(out, indent=1, ensure_ascii=False)
        # rewrite only when the content changes, ignoring the extraction date (otherwise every day would
        # look like a new result and trigger a re-render)
        strip = lambda d: {**d, "meta": {k: v for k, v in d.get("meta", {}).items() if k != "extracted"}}
        if not os.path.exists(p) or strip(json.load(open(p))) != strip(json.loads(new)):
            open(p, "w").write(new)
            print(f"{name}: written")
        else:
            print(f"{name}: unchanged")
