#!/usr/bin/env python3
"""data_existing.py: convert the repository's EXISTING results into scene data (data/*.json).

Scenes never read the repository: this tool is the bridge for the READY scenes (decision D4: no new
simulation, training or benchmark is run; only results already in the repository are used). Every
output carries meta.source (path relative to the repository), meta.sha256 of each source file,
meta.generator and a human stamp for the lower-third. A file is rewritten only when its content changes
(the extraction date is ignored), so an unchanged result never triggers a re-render.

Sources -> outputs (outline.json "data" fields):
  experiences/resultats/e1_gissinger.json   -> e1_finegrid.json   (04.3, 05.3, 09.1-09.3: crossing rate vs Gamma, 41 points)
                                             -> e1_data_rates.json (04.3, 07.1: the 21 data Gammas, P(D>0) of the training data)
                                             -> e1_eval.json       (07.3-07.6, 09.4, X3.2: metrics per variant, noise floors)
  experiences/resultats/e1_echantillons.npz -> e1_samples_<G>.json (04.6, 04.7, 05.2, 07.1, 07.2, 07.5: (Q, D, V) snapshots
     (+ cache_e1/e1_echantillons_complet.npz for 8000 reference points when present; Ddot and dE/dt computed
      algebraically from the model's equations, no integration)
  experiences/resultats/e2_echantillons.npz -> e2_maps.json       (08.1-08.3: vorticity and current maps, 32^2 modes
                                                                    displayed at 128^2 by spectral zero-padding)
  experiences/resultats/e2_mhd2d.json       -> e2_eval.json       (08.2, 08.5, 09.5, X3.2, X3.4)
  experiences/resultats/e3_abc.json         -> e3_growth.json     (03.4, X1.1, X1.3; ghost curve of 10.4)
  experiences/resultats/e3_modes.npz        -> e3_modes.json      (X1.2: dominant modes at Rm 8, 12, 16, 20)
  experiences/resultats/digest.md           -> digest.json        (every table of the digest, parsed)
  figures/*/figure/data/*.json              -> fig_<name>.json    (06.1, 06.3, 08.6, 08.7, 10.1, 02.5: the site's figure data;
                                                                    illustrative ones are stamped SCHEMATIC)
Packed arrays: {"dtype": "f32", "shape": [...], "b64": "..."} (little-endian float32), decoded in scenes
by Scene.f32(). Symbol sheet: the growth rate is s (never lambda); the dipole is D.

Usage: python3 -I tools/data_existing.py [--repo /home/user/milady-2027] [--out data] [--check]
  --check: report what would change, write nothing.
"""
import base64
import datetime
import glob
import hashlib
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)   # the repository root (video/..)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_existing.py"
TODAY = datetime.date.today().isoformat()

# E1 model constants (experiences/e1_gissinger.py:1-8, config of e1_gissinger.json)
MU, NU = 0.119, 0.1


def rp(rel):
    return os.path.join(REPO, rel)


def sha(rel):
    h = hashlib.sha256()
    with open(rp(rel), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def meta(sources, stamp, **extra):
    """meta block: primary source + every source with its SHA-256; the stamp is lower-third line 1 (<= 44 chars)"""
    assert len(stamp) <= 44, f"stamp too long for a lower-third: {stamp}"
    sources = [sources] if isinstance(sources, str) else list(sources)
    m = {"source": sources[0], "sha256": sha(sources[0]), "generator": GEN, "extracted": TODAY, "stamp": stamp}
    if len(sources) > 1:
        m["sources"] = [{"path": s, "sha256": sha(s)} for s in sources]
    m.update(extra)
    return m


def pack(a):
    """float32 array -> {"dtype": "f32", "shape", "b64"} (little-endian)"""
    a = np.ascontiguousarray(np.asarray(a, dtype="<f4"))
    return {"dtype": "f32", "shape": list(a.shape), "b64": base64.b64encode(a.tobytes()).decode("ascii")}


def r(x, sig=6):
    """round floats for stable JSON (None for NaN/inf)"""
    if x is None:
        return None
    if isinstance(x, (list, tuple)):
        return [r(v, sig) for v in x]
    if isinstance(x, dict):
        return {k: r(v, sig) for k, v in x.items()}
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        x = float(x)
        if not np.isfinite(x):
            return None
        return float(f"{x:.{sig}g}")
    return x


# ------------------------------------------------------------------------------------------------
# E1: Gissinger three-mode model
# ------------------------------------------------------------------------------------------------
E1J = "experiences/resultats/e1_gissinger.json"
E1S = "experiences/resultats/e1_echantillons.npz"
E1C = "experiences/resultats/cache_e1/e1_echantillons_complet.npz"


def e1_finegrid():
    d = json.load(open(rp(E1J)))
    g = d["grille_fine"]
    G = [row["Gamma"] for row in g]
    col = lambda k: [r(row[k]) for row in g]
    # threshold: last Gamma with zero simulated crossings, first with crossings
    zero = [row["Gamma"] for row in g if row["taux_simulation"] == 0]
    first = next(row["Gamma"] for row in g if row["taux_simulation"] > 0)
    return {
        "meta": meta(E1J, "DATA · E1 · fine grid, 41 Γ",
                     note="Gissinger three-mode model; generated rates from model C and model F, seed 0; crossing rates of D through 0 (reversals and excursions), per unit time; 'bridge' = mass of |D| < h_Rice"),
        "x": {"label": "Γ, control parameter", "values": G, "train": [bool(row["dans_entrainement"]) for row in g]},
        "y": {"label": "crossing rate of D (per unit time)"},
        "series": [
            {"name": "simulation (counted crossings)", "kind": "simulated", "field": "b", "y": col("taux_simulation")},
            {"name": "Rice, reference snapshots", "kind": "simulated", "field": "metric", "y": col("taux_rice_ref")},
            {"name": "Rice, generated (model C)", "kind": "generated", "field": "metric", "y": col("taux_rice_modele")},
            {"name": "Rice, generated (model F)", "kind": "generated", "field": "model", "y": col("taux_rice_modele_F")},
        ],
        "bridge": {"label": "bridge mass P(|D| < h)", "h_rice": d["config"]["h_Rice"],
                   "reference": col("pont_ref"), "model_C": col("pont_modele"), "model_F": col("pont_modele_F")},
        "quantile99_V": {"reference": col("V_q99_ref"), "model_C": col("V_q99_modele")},
        "threshold": {"last_zero": max(zero), "first_nonzero": first,
                      "text": f"crossings start between Γ = {max(zero)} and {first}"},
        "config": {"mu": d["config"]["mu"], "nu": d["config"]["nu"], "G_train": d["config"]["G_train"],
                   "G_test": d["config"]["G_test"], "trajectories_per_gamma": d["config"]["trajectoires_par_Gamma"],
                   "kept_duration": d["config"]["duree_gardee"], "seeds": d["config"]["seeds"]},
    }


def e1_data_rates():
    d = json.load(open(rp(E1J)))
    don = d["donnees"]
    G = sorted(don, key=float)
    train = set(map(float, d["config"]["G_train"]))
    return {
        "meta": meta(E1J, "DATA · E1 · 21 Γ, 16 trajectories each"),
        "x": {"label": "Γ, control parameter", "values": [float(g) for g in G], "train": [float(g) in train for g in G]},
        "y": {"label": "crossing rate of D (per unit time)"},
        "series": [
            {"name": "simulation (counted crossings)", "kind": "simulated", "field": "b", "y": [r(don[g]["taux_passages_simulation"]) for g in G]},
            {"name": "Rice, reference snapshots", "kind": "simulated", "field": "metric", "y": [r(don[g]["taux_rice_reference"]) for g in G]},
        ],
        "p_bridge_ref": [r(don[g]["P(|D|<0.25)_ref"]) for g in G],
        "p_positive_train": [r(don[g].get("P(D>0)_train")) for g in G],
        "note": "p_positive_train: fraction of training snapshots with D > 0 (training Γ only; null at test Γ)",
    }


E1_VARIANTS = ["A_reference", "B_augmentation", "C_equivariant", "C_court", "D_inclinaison_A", "D_inclinaison_C",
               "D_inclinaison_Ccourt", "E_projection_C", "F_stationnarite_C", "F0_temoin_C", "F_stationnarite_Ccourt",
               "F0_temoin_Ccourt", "A_reference_moitie", "C_equivariant_moitie", "C_court_moitie"]
E1_NAMES = {"A_reference": "A · reference", "B_augmentation": "B · data augmentation", "C_equivariant": "C · equivariant (mirror built in)",
            "C_court": "C short (biased)", "D_inclinaison_A": "D · tilting on A", "D_inclinaison_C": "D · tilting on C",
            "D_inclinaison_Ccourt": "D · tilting on C short", "E_projection_C": "E · per-sample projection on C",
            "F_stationnarite_C": "F · stationarity loss on C", "F0_temoin_C": "F0 · control (no loss) on C",
            "F_stationnarite_Ccourt": "F · stationarity loss on C short", "F0_temoin_Ccourt": "F0 · control on C short",
            "A_reference_moitie": "A · half data", "C_equivariant_moitie": "C · half data", "C_court_moitie": "C short · half data"}
E1_METRICS = {"energie": "distribution distance (energy distance)", "sw1": "sliced Wasserstein", "asym": "|P(D>0) − ½|",
              "liou_train_moy": "Liouville residual, degree ≤ 2", "liou_test_moy": "Liouville residual, degree 3",
              "dEdt_std": "σ(dE/dt)", "erreur_pont": "error on P(|D| < 0.25)", "erreur_taux_rice": "error on the Rice rate"}


def e1_eval():
    d = json.load(open(rp(E1J)))
    ev, res = d["evaluation"], d["resume"]
    per = {}
    for v in E1_VARIANTS:
        rows = {}
        for split in ("train", "test"):
            L = ev[v][split]
            rows[split] = {
                "Gamma": [x["Gamma"] for x in L],
                # [mean, half-spread] over the two seeds as stored (value, spread)
                **{k: [r(x[k][0]) for x in L] for k in ("energie", "sw1", "asym", "pont", "liou_train_moy", "liou_test_moy", "dEdt_std", "taux_rice")},
                **{k + "_spread": [r(x[k][1]) for x in L] for k in ("energie", "asym")},
                "taux_simulation": [r(x["taux_simulation"]) for x in L],
                "taux_rice_ref": [r(x["taux_rice_ref"]) for x in L],
            }
            if "ess_frac_b" in L[0]:
                rows[split]["ess_frac_b"] = [r(x.get("ess_frac_b")) for x in L]
        per[v] = {"name": E1_NAMES[v], "per_gamma": rows, "mean": r(res[v])}
    return {
        "meta": meta(E1J, "DATA · E1 · 2 seeds, means over Γ",
                     note="per_gamma values are [seed mean]; *_spread is the stored seed spread; 'mean' = report tables (digest)"),
        "metrics": E1_METRICS,
        "variants": per,
        "noise_floor": r(res["planchers_bruit_MC"]),
        "reference": r(res["reference"]),
        "training": r(d["entrainement"]),
    }


def e1_samples():
    """one file per Gamma kept in the published archive: (Q, D, V) snapshots per variant + derived columns"""
    z = np.load(rp(E1S))
    full = np.load(rp(E1C)) if os.path.exists(rp(E1C)) else None
    out = {}
    gammas = sorted({k.split("|")[1] for k in z.files}, key=float)
    keep = ["ref", "A_reference", "B_augmentation", "C_equivariant", "C_court", "D_inclinaison_C", "E_projection_C",
            "F_stationnarite_C", "F0_temoin_C"]
    for g in gammas:
        G = float(g)
        srcs = [E1S] + ([E1C] if full is not None else [])
        doc = {"meta": meta(srcs, f"DATA · E1 · snapshots at Γ = {g}",
                            note="columns Q (quadrupole), D (dipole), V (flow mode); Ddot = −νD + VQ and dEdt = μQ² − νD² + ΓV − V² + QDV "
                                 "are computed from the model's equations on each snapshot (no time integration); the archive stores float32, so "
                                 "per-sample projected snapshots (E_projection_C) give |dE/dt| ~ 1e-8 here, not the report's 4e-17 (float64): "
                                 "quote the report's value from e1_eval, use these columns for shapes (histograms) only"),
               "gamma": G, "columns": ["Q", "D", "V"], "variants": {}}
        for v in keep:
            key = f"{v}|{g}"
            if v == "ref" and full is not None and key in full.files:
                x = full[key].astype(np.float64)
                src = E1C
            elif key in z.files:
                x = z[key].astype(np.float64)
                src = E1S
            else:
                continue
            Q, D, V = x[:, 0], x[:, 1], x[:, 2]
            ddot = -NU * D + V * Q
            dedt = MU * Q ** 2 - NU * D ** 2 + G * V - V ** 2 + Q * D * V
            doc["variants"][v] = {
                "name": "reference (simulation snapshots)" if v == "ref" else E1_NAMES.get(v, v), "kind": "simulated" if v == "ref" else "generated",
                "n": int(len(x)), "from": src, "x": pack(x), "Ddot": pack(ddot), "dEdt": pack(dedt),
                "p_positive": r(float(np.mean(D > 0))), "std_dEdt": r(float(np.std(dedt))),
            }
        out[f"e1_samples_{g}"] = doc
    return out


# ------------------------------------------------------------------------------------------------
# E2: forced 2D MHD
# ------------------------------------------------------------------------------------------------
E2J = "experiences/resultats/e2_mhd2d.json"
E2S = "experiences/resultats/e2_echantillons.npz"
E2_NAMES = {"V0_libre": "V0 · unconstrained", "V1_penalite": "V1 · penalty", "V2_proj_finale": "V2 · final projection",
            "V3_flot_projete": "V3 · projected flow", "V4_potentiels": "V4 · potentials (exact by construction)",
            "V5_potentiels_stat": "V5 · potentials + stationarity loss", "V5_temoin": "V5 control (no loss)",
            "reference_sous_echantillon": "reference subsample (noise floor)", "ref": "reference simulation"}


def _grid(c, kx, ky, n):
    """independent rfft coefficients (M,) on modes (kx >= 0 half plane) -> real field on an n x n grid.
    Each retained mode stands for the pair (k, -k); the kx = 0 column gets its conjugate explicitly.
    Scaled so that values equal the field on the native 32^2 grid (spectral interpolation)."""
    F = np.zeros((n, n // 2 + 1), complex)
    ix, iy = kx.astype(int), ky.astype(int) % n
    F[iy, ix] = c
    z = ix == 0
    F[(-ky[z].astype(int)) % n, 0] = np.conj(c[z])
    return np.fft.irfft2(F, s=(n, n)) * (n * n) / (32 * 32)


def e2_maps():
    z = np.load(rp(E2S))
    kx, ky = z["kx"], z["ky"]
    n = 128
    maps = {}
    vmax = {}
    for v in ("ref", "V0_libre", "V1_penalite", "V4_potentiels", "V5_potentiels_stat"):
        c = z[v]   # (8, 4, M): (ux, uy, Bx, By) Fourier coefficients
        ent = {"name": E2_NAMES[v], "kind": "simulated" if v == "ref" else "generated", "samples": []}
        for i in (0, 1):
            ux, uy, bx, by = c[i]
            om = 1j * kx * uy - 1j * ky * ux
            jj = 1j * kx * by - 1j * ky * bx
            s = {"omega": _grid(om, kx, ky, n), "j": _grid(jj, kx, ky, n)}
            if v in ("V0_libre", "V1_penalite") and i == 0:
                s["div_u"] = _grid(1j * kx * ux + 1j * ky * uy, kx, ky, n)
                s["div_b"] = _grid(1j * kx * bx + 1j * ky * by, kx, ky, n)
            if v == "ref":
                for k in ("omega", "j"):
                    vmax[k] = max(vmax.get(k, 0.0), float(np.abs(s[k]).max()))
            ent["samples"].append(s)
        maps[v] = ent
    out = {"meta": meta([E2S, E2J], f"DATA · E2 · 2D MHD, η = {float(z['eta']):.5f}",
                        note="omega = vorticity (flow, blue family), j = current density (magnetic, vermillion family); "
                             "display interpolation (spectral) to 128²: show the chip 'display interpolation (spectral), native grid 32²'; "
                             "vmax = max |value| over the reference samples: use it for every variant (same colour scale)"),
           "eta": r(float(z["eta"])), "grid": [n, n], "native_grid": [32, 32], "vmax": r(vmax), "variants": {}}
    for v, ent in maps.items():
        out["variants"][v] = {"name": ent["name"], "kind": ent["kind"],
                              "samples": [{k: pack(a.astype(np.float32)) for k, a in s.items()} for s in ent["samples"]]}
    return out


E2_KEYS = {"div_rel_u": "relative divergence of u", "div_rel_b": "relative divergence of B", "err_spectre_log10": "spectrum error (log10)",
           "err_Eu_rel": "relative error, kinetic energy", "err_Eb_rel": "relative error, magnetic energy",
           "residu_bilan_energie": "energy budget residual", "residu_bilan_Hc": "cross-helicity budget residual",
           "residu_bilan_A2": "⟨a²⟩ budget residual", "std_diss_rel": "σ(dissipation) / σ_ref", "dist_energie_features": "distribution distance"}


def e2_eval():
    d = json.load(open(rp(E2J)))
    res = d["resume"]
    variants = {k: {"name": E2_NAMES.get(k, k), "mean": r(v)} for k, v in res.items() if k != "en_loi"}
    per = {}
    for k, rows in d["evaluation"].items():
        per[k] = {split: {"eta": [x["eta"] for x in L], **{m: [r(x.get(m)) for x in L] for m in E2_KEYS}} for split, L in rows.items()}
    law = d["en_loi"]
    etas = sorted(law, key=float)
    en_loi = {"eta": [float(e) for e in etas], "split": [law[e]["split"] for e in etas],
              "ess_frac_b": [r(law[e].get("ess_frac_b")) for e in etas],
              **{m: {mm: [r(law[e][m][mm]) for e in etas] for mm in E2_KEYS} for m in ("base", "inclinaison", "recalage")},
              "mean": r({k: v for k, v in res["en_loi"].items()})}
    return {
        "meta": meta(E2J, "DATA · E2 · 1000 samples per η",
                     note="'recalage' = per-sample rescaling onto the energy budget; 'inclinaison' = exponential tilting (on the crowd); "
                          "residuals are signed per η, absolute in the means"),
        "metrics": E2_KEYS, "variants": variants, "per_eta": per, "en_loi": en_loi,
        "config": r(d["config"]), "timing": r(d["variantes"]),
    }


# ------------------------------------------------------------------------------------------------
# E3: kinematic ABC dynamo
# ------------------------------------------------------------------------------------------------
E3J = "experiences/resultats/e3_abc.json"
E3M = "experiences/resultats/e3_modes.npz"
DIG = "experiences/resultats/digest.md"


def e3_growth():
    d = json.load(open(rp(E3J)))
    T = d["taux"]
    Rm = [x["Rm"] for x in T]
    s = [x["lambda"] for x in T]
    # thresholds: linear interpolation of the sign changes of s (as in the digest: 8.87, 17.6, 26.8)
    thr = []
    for i in range(len(T) - 1):
        if s[i] == 0 or s[i] * s[i + 1] < 0:
            thr.append(round(Rm[i] - s[i] * (Rm[i + 1] - Rm[i]) / (s[i + 1] - s[i]), 2))
    conv = d.get("convergence") or d.get("convergence_N48") or []
    return {
        "meta": meta(E3J, f"DATA · E3 · ABC flow, {d['config']['N']}³",
                     note="s = growth rate of the magnetic energy amplitude (real part; the report writes lambda); "
                          "'last quarter' = fit on the last quarter of the run; the published windows are R:1112"),
        "x": {"label": "Rm, magnetic Reynolds number", "values": Rm},
        "y": {"label": "s, growth rate"},
        "series": [
            {"name": f"s, {d['config']['N']}³ (whole run)", "kind": "simulated", "field": "b", "y": [r(v) for v in s]},
            {"name": "s, last quarter of the run", "kind": "simulated", "field": "fg", "y": [r(x["lambda_dernier_quart"]) for x in T]},
        ],
        "div_rel": [r(x["div_rel"]) for x in T],
        "thresholds": thr,
        "published_windows": {"text": "8.9 < Rm < 17.5 and Rm ≳ 27", "bounds": [8.9, 17.5, 27], "source": "R:1112"},
        "convergence_N48": r(conv),
        "exact_check": {"Rm": 2, "bound": -0.5, "s": r(T[0]["lambda"]), "text": "dominant rate can be no lower than −1/Rm = −0.5"},
        "config": d["config"],
    }


def e3_modes():
    z = np.load(rp(E3M))
    out = {"meta": meta(E3M, "DATA · E3 · dominant modes, 32³",
                        note="b: (3, 32, 32, 32) components (x, y, z) normalised to max |B| = 1; "
                             "Rm 8 and 20 decay (s < 0), 12 and 16 grow (first window); no mode of the second window is stored; "
                             "babs: |B| on the full grid; b16: components downsampled to 16³ (every other point); "
                             "slice_z0: |B| on the plane z = 0"),
           "Rm": [], "modes": {}}
    for k in sorted(z.files, key=lambda s: float(s[2:])):
        b = z[k].astype(np.float64)
        b /= np.sqrt((b ** 2).sum(0)).max()
        babs = np.sqrt((b ** 2).sum(0))
        Rm = float(k[2:])
        out["Rm"].append(Rm)
        out["modes"][k] = {"Rm": Rm, "babs": pack(babs), "b16": pack(b[:, ::2, ::2, ::2]), "slice_z0": pack(babs[:, :, 0]),
                           "bz_z0": pack(b[2, :, :, 0])}
    return out


# ------------------------------------------------------------------------------------------------
# digest.md: every markdown table, parsed
# ------------------------------------------------------------------------------------------------
def _num(s):
    s = s.strip()
    t = s.replace("−", "-").replace("×10^", "e").replace(" ", "")
    try:
        return float(t)
    except ValueError:
        return s


def digest():
    lines = open(rp(DIG), encoding="utf-8").read().splitlines()
    tables, section, sub, i = [], None, None, 0
    while i < len(lines):
        L = lines[i]
        if L.startswith("## "):
            section, sub = L[3:].strip(), None
        elif L.startswith("### "):
            sub = L[4:].strip()
        elif L.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in L.strip().strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append([_num(c) for c in cells])
                i += 1
            tables.append({"section": section, "subsection": sub, "header": head, "rows": rows})
            continue
        i += 1
    extras = {}
    for L in lines:
        m = re.match(r"^Seuils interpolés : \[(.*)\]", L)
        if m:
            extras["e3_thresholds"] = [float(x) for x in m.group(1).split(",")]
    return {"meta": meta(DIG, "DATA · results digest",
                         note="tables in the digest's own language (French headers); line references: search the digest by content"),
            "tables": tables, **extras}


# ------------------------------------------------------------------------------------------------
# figure data of the site (pass-through, stamped)
# ------------------------------------------------------------------------------------------------
FIG_SCHEMATIC = {"cadre": "illustrative toy models", "flow-matching": "1D toy laws (exact marginal velocity)",
                 "taxonomie": "illustrative curves, no measurement", "vks": "qualitative curves (normal form), no VKS data"}


def figures():
    out = {}
    for p in sorted(glob.glob(rp("figures/*/figure/data/*.json"))):
        rel = os.path.relpath(p, REPO)
        name = rel.split("/")[1]
        sch = name in FIG_SCHEMATIC
        stamp = (f"SCHEMATIC · site figure '{name}'" if sch else f"DATA · site figure '{name}'")
        doc = {"meta": meta(rel, stamp, schematic=sch, figure=f"figures/{name}",
                           note=(FIG_SCHEMATIC[name] + ": show the SCHEMATIC chip, never numbers from it") if sch else "computed from E1–E3 results"),
               "data": json.load(open(p))}
        out["fig_" + name.replace("-", "_")] = doc
    return out


# ------------------------------------------------------------------------------------------------
def write(name, doc):
    p = os.path.join(OUT, name + ".json")
    new = json.dumps(doc, ensure_ascii=False, separators=(",", ":") if _big(doc) else (", ", ": "), indent=None if _big(doc) else 1)
    strip = lambda d: {**d, "meta": {k: v for k, v in d.get("meta", {}).items() if k != "extracted"}}
    if os.path.exists(p):
        try:
            if strip(json.load(open(p))) == strip(json.loads(new)):
                return "unchanged"
        except json.JSONDecodeError:
            pass
    if CHECK:
        return "would write"
    tmp = p + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new)
    os.replace(tmp, p)
    return "written"


def _big(doc):
    return len(json.dumps(doc)) > 200_000


JOBS = [("e1_finegrid", e1_finegrid), ("e1_data_rates", e1_data_rates), ("e1_eval", e1_eval), (None, e1_samples),
        ("e2_maps", e2_maps), ("e2_eval", e2_eval), ("e3_growth", e3_growth), ("e3_modes", e3_modes),
        ("digest", digest), (None, figures)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    status = 0
    for name, fn in JOBS:
        try:
            res = fn()
        except FileNotFoundError as e:
            print(f"{name or fn.__name__}: source missing ({e.filename}) — skipped")
            status = 1
            continue
        docs = res.items() if name is None else [(name, res)]
        for n, doc in docs:
            st = write(n, doc)
            kb = len(json.dumps(doc)) / 1024
            print(f"{n}: {st} ({kb:.0f} kB) <- {doc['meta']['source']}")
    sys.exit(status)
