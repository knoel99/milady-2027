#!/usr/bin/env python3
"""data_cloud.py: converters for the PENDING scenes, from the cloud / HPC outputs to data/*.json.

Nothing here runs a simulation, a training or a benchmark: each converter READS files that a campaign
produced elsewhere (MFF files, evaluation reports of milady.eval, catalog dumps) and writes the small data
file that the scene's "result" variant draws (Kit.seat: curve | lamps | gauge | map). Until such a file
exists the scene ships as an empty seat (status "pending"). Contract of every output (CONTRACT.md §5):

  meta      {source, sha256, sources: [{path, sha256}], generator, extracted, stamp (<= 44 chars), note}
  verdict   "met" | "not_met" | "inconclusive"   computed HERE from the criterion, never in a scene
  verdict_rule   the rule as applied (text), verdict_text  one line for the screen
  fields    flat {name: spoken-ready string} for the narration placeholders {{name}} of the result variant
  payload   series (curve seat) | lamps (lamp seat) | value (gauge seat) | map (map seat), plus details

Converters (scene, output):
  palier1     10.3  palier1_sweep.json        MFF of palier1_mhd2d: dissipation around the flat injection line
  abc3d       10.4  palier2_abc3d.json        MFF of palier2_abc3d: s(Rm), last-quarter fit, thresholds, D17 bet
  tg3d        10.5  palier2_tg3d.json         MFF of palier2_tg3d: log E_B(t), kinematic rate, saturation flag (A8)
  fm3d-eval   10.7  fm3d_eval.json            evaluation JSON of milady.eval: lamps (a)-(d), spectra, distances
  fm3d-stat   X3.5  fm3d_stationarity.json    two evaluation JSONs (stationarity loss vs control)
  trace       X5.3  x5_campaign_trace.json    catalog dump (python -m milady.catalog sims --campaign C)
  bill        X5.5  x5_compute_bill.json      catalog dumps + the plan's estimates (a JSON you pass)
  xpoints     X5.4  x5_xpoints.json           MFF (reference) + npz of generated B fields: X-point counts
  tier0       X4.5  x4_tier0.json             an E1-style results JSON with 3 seeds (same schema as e1_gissinger.json)
  seat        X4.2, X4.4, X6.4, X6.5, 10.9    a generic "seat JSON" (format below) for VKS, DRESDYN, branch, Rice levels
  selftest          builds tiny synthetic inputs in a temporary folder and runs every converter (no simulation)

Usage (in the repository venv: h5py is needed for MFF):
  python -I tools/data_cloud.py abc3d --mff '/runs/store/palier2_abc3d/*/fields.h5' [--out data/palier2_abc3d.json]
  python -I tools/data_cloud.py fm3d-eval --eval eval_fm3d.json [--tg data/palier2_tg3d.json]
  python -I tools/data_cloud.py selftest
Generic seat JSON (VKS / DRESDYN / branch / Rice levels, until their own converters exist):
  {"stamp": "...", "source": "<what produced it>", "type": "lamps"|"curve"|"gauge",
   "lamps": [{"id", "state": "met|not_met|inconclusive", "value"}] | "series": [...] | "value": x,
   "verdict": "...", "verdict_text": "...", "fields": {...}}
"""
import argparse
import base64
import datetime
import glob
import hashlib
import json
import math
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get("MILADY_REPO", "/home/user/milady-2027")
GEN = "tools/data_cloud.py"
TODAY = datetime.date.today().isoformat()
VERDICTS = ("met", "not_met", "inconclusive")


# ================================================================================================
# helpers
# ================================================================================================
def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def meta(paths, stamp, note=""):
    assert len(stamp) <= 44, f"stamp too long for a lower-third: {stamp}"
    paths = list(paths)
    srcs = [{"path": p, "sha256": sha_file(p)} for p in paths]
    m = {"source": paths[0] if len(paths) == 1 else f"{len(paths)} files ({os.path.dirname(paths[0]) or '.'})",
         "sha256": srcs[0]["sha256"] if len(srcs) == 1 else hashlib.sha256("".join(s["sha256"] for s in srcs).encode()).hexdigest(),
         "sources": srcs, "generator": GEN, "extracted": TODAY, "stamp": stamp, "status": "result"}
    if note:
        m["note"] = note
    return m


def pack(a):
    a = np.ascontiguousarray(np.asarray(a, dtype="<f4"))
    return {"dtype": "f32", "shape": list(a.shape), "b64": base64.b64encode(a.tobytes()).decode("ascii")}


def rnd(x, sig=5):
    if isinstance(x, dict):
        return {k: rnd(v, sig) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rnd(v, sig) for v in x]
    if isinstance(x, (bool, np.bool_)) or x is None:
        return None if x is None else bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        x = float(x)
        return None if not math.isfinite(x) else float(f"{x:.{sig}g}")
    return x


def say(x, sig=2):
    """number written for the ear: 0.0021 -> 'zero point zero zero two one' is the writer's job; here a compact
    on-screen/narration-ready string with 2 significant digits (the writer may respell it)"""
    if x is None or not math.isfinite(float(x)):
        return "not available"
    x = float(x)
    if x == 0:
        return "0"
    e = math.floor(math.log10(abs(x)))
    if -3 <= e <= 4:
        return f"{float(f'{x:.{sig}g}'):g}"
    return f"{x / 10 ** e:.{sig - 1}f} times ten to the {e}"


def expand(patterns):
    out = []
    for p in patterns:
        if os.path.isdir(p):
            out += sorted(glob.glob(os.path.join(p, "**", "*.h5"), recursive=True))
        else:
            out += sorted(glob.glob(p)) or [p]
    if not out:
        raise SystemExit("no input file")
    return out


def need_milady():
    if REPO not in sys.path:
        sys.path.insert(0, REPO)
    try:
        from milady.data import format as mff  # noqa: F401  (h5py, read-only use)
    except ImportError as e:
        raise SystemExit(f"milady.data.format unavailable ({e}): run with the repository venv (h5py)")
    return mff


def slope(t, y):
    """least-squares slope of y(t) (same as milady.sim.mhd3d.growth_rate_fit)"""
    t, y = np.asarray(t, float), np.asarray(y, float)
    ok = np.isfinite(y)
    return float(np.polyfit(t[ok], y[ok], 1)[0]) if ok.sum() >= 2 else float("nan")


def crossings(x, y):
    """linear interpolation of the sign changes of y(x) (sorted x)"""
    out = []
    for i in range(len(x) - 1):
        if not (math.isfinite(y[i]) and math.isfinite(y[i + 1])):
            continue
        if y[i] == 0:
            out.append(float(x[i]))
        elif y[i] * y[i + 1] < 0:
            out.append(float(x[i] - y[i] * (x[i + 1] - x[i]) / (y[i + 1] - y[i])))
    return out


def write(doc, out):
    assert doc.get("verdict") in VERDICTS, "verdict must be met | not_met | inconclusive"
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    new = json.dumps(doc, ensure_ascii=False, indent=1)
    strip = lambda d: {**d, "meta": {k: v for k, v in d.get("meta", {}).items() if k != "extracted"}}
    if os.path.exists(out):
        try:
            if strip(json.load(open(out))) == strip(json.loads(new)):
                print(f"{out}: unchanged")
                return
        except json.JSONDecodeError:
            pass
    tmp = out + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new)
    os.replace(tmp, out)
    print(f"{out}: written ({doc['verdict']})")


def kept_window(rd):
    """times of the stored field snapshots (the kept window, after the burn-in)"""
    t = np.asarray(rd["coords"]["time"], float)
    return float(t.min()), float(t.max())


# ================================================================================================
# 10.3 palier1_mhd2d: dissipation around the flat injection line (Ito rate, A3)
# ================================================================================================
def conv_palier1(files, hist_bins=41, tol=0.05):
    """per eta: the dissipation series of trajectory 0, the constant injection (Ito rate), a histogram of
    injection - dissipation over all trajectories and kept times (centred on 0 when the run is stationary),
    and one current-density tile j = dBy/dx - dBx/dy (trajectory 0, last snapshot).
    Verdict rule (a stationarity check of the data, not a PhD-plan criterion): |E[inj - D]| / inj < tol at every eta."""
    mff = need_milady()
    rows = []
    for p in files:
        rd = mff.read_mff(p, fields=[])
        d, par = rd["diagnostics"], rd["params"]
        t0, _ = kept_window(rd)
        td = np.asarray(d["time"], float)
        keep = td >= t0 - 1e-9
        diss = np.atleast_2d(np.asarray(d["dissipation"], float))[:, keep]
        inj = np.atleast_2d(np.asarray(d["injection"], float))[:, keep]
        res = inj - diss
        nt = int(np.asarray(rd["coords"]["time"]).size)
        bfield = mff.read_mff(p, fields=["magnetic_field"], t=nt - 1, traj=0)["fields"]["magnetic_field"][0, 0]
        n = bfield.shape[0]
        k = np.fft.fftfreq(n, 1.0 / n)
        KX, KY = np.meshgrid(k, k, indexing="ij")
        bx, by = np.fft.fft2(bfield[..., 0]), np.fft.fft2(bfield[..., 1])
        j = np.real(np.fft.ifft2(1j * KX * by - 1j * KY * bx))
        rows.append({"eta": float(par["eta"]), "path": p, "t": td[keep], "diss0": diss[0], "inj": float(np.mean(inj)),
                     "res": res.ravel(), "rel": float(abs(np.mean(res)) / max(abs(np.mean(inj)), 1e-300)), "j": j,
                     "Eb": float(np.mean(np.asarray(d["magnetic_energy"], float)[..., keep])) if "magnetic_energy" in d else None})
    rows.sort(key=lambda r: r["eta"])
    span = max(float(np.max(np.abs(r["res"]))) for r in rows) or 1.0
    edges = np.linspace(-span, span, hist_bins + 1)
    step = lambda a, m=240: a[:: max(1, len(a) // m)]
    per = [{"eta": r["eta"], "injection": r["inj"], "t": rnd(step(r["t"]).tolist()), "dissipation": rnd(step(r["diss0"]).tolist()),
            "residual_hist": np.histogram(r["res"], bins=edges)[0].tolist(), "rel_mean_residual": rnd(r["rel"]),
            "magnetic_energy_mean": rnd(r["Eb"])} for r in rows]
    worst = max(rows, key=lambda r: r["rel"])
    verdict = "met" if worst["rel"] < tol else "not_met"
    mid = rows[len(rows) // 2]
    doc = {"meta": meta([r["path"] for r in rows], "SIMULATED · palier1_mhd2d · 2D MHD",
                        note="injection is the constant Ito rate of the white-in-time forcing (a flat line); only the dissipation fluctuates"),
           "verdict": verdict, "verdict_rule": f"|E[injection − dissipation]| / injection < {tol} at every η (stationarity of the data)",
           "verdict_text": f"worst η = {worst['eta']:.4g}: mean residual {100 * worst['rel']:.2g} % of the injection",
           "x": {"label": "η, magnetic diffusivity", "values": [r["eta"] for r in rows]},
           "y": {"label": "|E[injection − dissipation]| / injection"},
           "series": [{"name": "simulated, mean residual", "kind": "simulated", "field": "metric", "y": [rnd(r["rel"]) for r in rows]}],
           "hist_edges": rnd(edges.tolist()), "per_eta": per,
           "map": {"grid": pack(mid["j"]), "vmax": rnd(float(np.max(np.abs(mid["j"])))), "eta": mid["eta"], "generated": False},
           "fields": {"n_eta": str(len(rows)), "worst_eta": say(worst["eta"], 3), "worst_residual_percent": say(100 * worst["rel"]), "verdict": verdict.replace("_", " ")}}
    return doc


# ================================================================================================
# 10.4 palier2_abc3d: growth rate s(Rm), thresholds, the D17 bet s(17) > 0 > s(18)
# ================================================================================================
def conv_abc3d(files, modes=(8, 12, 16, 20)):
    """s = slope of ln|B| over the kept window (t >= first stored snapshot); s_q = slope over its last quarter;
    one value per trajectory (seed), averaged. Bet (decision D17): s(17) > 0 > s(18) with |s - s_q| < |s| at both.
    Inconclusive when Rm = 17 or 18 is missing or the two fits disagree; extra points (17.25, 17.5, 17.75) are
    drawn when present."""
    mff = need_milady()
    pts, mode_out, paths = {}, {}, []
    for p in files:
        rd = mff.read_mff(p, fields=[])
        Rm = float(rd["params"]["Rm"])
        d = rd["diagnostics"]
        t0, t1 = kept_window(rd)
        td = np.asarray(d["time"], float)
        lb = np.atleast_2d(np.asarray(d["log_b_rms"], float))
        keep = td >= t0 - 1e-9
        q = td >= t1 - 0.25 * (t1 - t0) - 1e-9
        s = [slope(td[keep], row[keep]) for row in lb]
        sq = [slope(td[q], row[q]) for row in lb]
        pts.setdefault(Rm, {"s": [], "sq": []})
        pts[Rm]["s"] += s
        pts[Rm]["sq"] += sq
        paths.append(p)
        if any(abs(Rm - m) < 1e-9 for m in modes):
            nt = int(np.asarray(rd["coords"]["time"]).size)
            b = mff.read_mff(p, fields=["magnetic_field"], t=nt - 1, traj=0)["fields"]["magnetic_field"][0, 0].astype(float)
            b /= max(np.sqrt((b ** 2).sum(-1)).max(), 1e-300)
            st = max(1, b.shape[0] // 16)
            mode_out[f"Rm{Rm:g}"] = {"Rm": Rm, "b16": pack(np.moveaxis(b[::st, ::st, ::st], -1, 0)), "babs_z0": pack(np.sqrt((b[:, :, 0] ** 2).sum(-1)))}
    Rms = sorted(pts)
    s = [float(np.mean(pts[r]["s"])) for r in Rms]
    sq = [float(np.mean(pts[r]["sq"])) for r in Rms]
    spread = [float(np.ptp(pts[r]["s"])) if len(pts[r]["s"]) > 1 else 0.0 for r in Rms]
    get = lambda r: (s[Rms.index(r)], sq[Rms.index(r)]) if r in Rms else (None, None)
    (s17, q17), (s18, q18) = get(17.0), get(18.0)
    if s17 is None or s18 is None:
        verdict, why = "inconclusive", "Rm = 17 or Rm = 18 is missing"
    elif abs(s17 - q17) >= abs(s17) or abs(s18 - q18) >= abs(s18):
        verdict, why = "inconclusive", "the whole-run and last-quarter fits disagree at 17 or 18"
    elif s17 > 0 > s18:
        verdict, why = "met", "s(17) > 0 > s(18): the first window closes between 17 and 18"
    else:
        verdict, why = "not_met", "the sign change is not between Rm = 17 and 18"
    thr = crossings(Rms, s)
    doc = {"meta": meta(paths, "SIMULATED · palier2_abc3d · ABC flow",
                        note="s = growth rate (slope of ln|B|) over the kept window; s_q over its last quarter; mean over seeds"),
           "verdict": verdict, "verdict_rule": "s(17) > 0 > s(18) with |s − s_q| < |s| at both (decision D17; published windows R:1112)",
           "verdict_text": why,
           "x": {"label": "Rm, magnetic Reynolds number", "values": Rms},
           "y": {"label": "s, growth rate"},
           "series": [{"name": "s, whole kept window", "kind": "simulated", "field": "b", "y": rnd(s)},
                      {"name": "s, last quarter", "kind": "simulated", "field": "fg", "y": rnd(sq), "points": False}],
           "seed_spread": rnd(spread), "n_seeds": [len(pts[r]["s"]) for r in Rms], "thresholds": [round(x, 2) for x in thr],
           "modes": mode_out,
           "fields": {"s17": say(s17, 2), "s18": say(s18, 2), "thresholds": ", ".join(f"{x:.3g}" for x in thr) or "none",
                      "n_thresholds": str(len(thr)), "verdict": verdict.replace("_", " ")}}
    return doc


# ================================================================================================
# 10.5 palier2_tg3d: kinematic growth, saturation flag (A8), threshold per Pm
# ================================================================================================
def _shell_spectrum(f):
    """E(k) = 1/2 sum over the shell round(|k|) = k of |f_k|^2 (forward-normalised FFT, as milady.eval)"""
    n = f.shape[-2]
    fh = np.fft.fftn(f, axes=tuple(range(f.ndim - 4, f.ndim - 1))) / n ** 3
    k = np.fft.fftfreq(n, 1.0 / n)
    K = np.sqrt(k[:, None, None] ** 2 + k[None, :, None] ** 2 + k[None, None, :] ** 2)
    sh = np.rint(K).astype(int)
    dens = 0.5 * np.sum(np.abs(fh) ** 2, axis=-1).reshape(-1, n ** 3).mean(0)
    return np.bincount(sh.ravel(), weights=dens, minlength=n // 2 + 1)[: n // 2 + 1]


def conv_tg3d(files, sat_frac=0.1, window=10.0, spectra=True):
    """per (Re, Pm): ln E_B(t), the kinematic rate s_kin = largest slope of ln E_B / 2 over a sliding window of
    `window` time units (the exponential phase), E_B averaged over the kept window, and a flag:
    saturated if |slope of ln E_B over the kept window| / 2 < sat_frac * |s_kin| (A8: only saturated runs are
    draws from a stationary state), growing, or decaying. Threshold per Pm: sign change of s_kin in Rm.
    Verdict (qualitative at this scale, criterion of the scene): met if a threshold is bracketed at two Pm or
    more; not_met if no run grows; inconclusive otherwise."""
    mff = need_milady()
    runs, paths = [], []
    for p in files:
        rd = mff.read_mff(p, fields=[])
        par, d = rd["params"], rd["diagnostics"]
        Re, Pm = float(par["Re"]), float(par["Pm"])
        td = np.asarray(d["time"], float)
        Eb = np.atleast_2d(np.asarray(d["magnetic_energy"], float))[0]
        lE = np.log(np.maximum(Eb, 1e-300))
        dt = float(np.median(np.diff(td))) if td.size > 1 else 1.0
        w = max(2, int(round(window / dt)))
        slopes = [slope(td[i:i + w], lE[i:i + w]) / 2 for i in range(0, max(1, td.size - w), max(1, w // 4))]
        s_kin = float(np.nanmax(slopes)) if np.nanmax(slopes) > 0 else float(np.nanmin(slopes))
        t0, _ = kept_window(rd)
        keep = td >= t0 - 1e-9
        s_end = slope(td[keep], lE[keep]) / 2
        flag = "saturated" if s_kin > 0 and abs(s_end) < sat_frac * abs(s_kin) else ("growing" if s_end > 0 else "decaying")
        run = {"Re": Re, "Pm": Pm, "Rm": Re * Pm, "s_kin": rnd(s_kin), "s_end": rnd(s_end), "flag": flag,
               "Eb_kept_mean": rnd(float(np.mean(Eb[keep]))), "t": rnd(td[:: max(1, td.size // 200)].tolist()),
               "logEb": rnd(lE[:: max(1, td.size // 200)].tolist())}
        if spectra:
            f = mff.read_mff(p, fields=["velocity", "magnetic_field"], traj=0)["fields"]
            run["spectrum_u"] = rnd(_shell_spectrum(f["velocity"][0]).tolist())
            run["spectrum_b"] = rnd(_shell_spectrum(f["magnetic_field"][0]).tolist())
        runs.append(run)
        paths.append(p)
    runs.sort(key=lambda r: (r["Pm"], r["Re"]))
    thr = {}
    for Pm in sorted({r["Pm"] for r in runs}):
        rr = [r for r in runs if r["Pm"] == Pm]
        c = crossings([r["Rm"] for r in rr], [r["s_kin"] for r in rr])
        if c:
            thr[f"{Pm:g}"] = round(c[0], 3)
    if not any(r["s_kin"] > 0 for r in runs):
        verdict, why = "not_met", "no run shows a growing field"
    elif len(thr) >= 2:
        verdict, why = "met", "a threshold is bracketed at " + ", ".join(f"Pm = {k}: Rm_c ≈ {v:.3g}" for k, v in thr.items())
    else:
        verdict, why = "inconclusive", "a threshold is bracketed at fewer than two Pm values"
    sat = [r for r in runs if r["flag"] == "saturated"]
    doc = {"meta": meta(paths, "SIMULATED · palier2_tg3d · Taylor–Green",
                        note=f"s_kin = growth rate of |B| (half the slope of ln E_B) in the exponential phase; saturated if the kept-window slope < {sat_frac} s_kin (A8)"),
           "verdict": verdict, "verdict_rule": "qualitative at this scale: a threshold bracketed at two Pm or more (saturated runs only for budgets)",
           "verdict_text": why, "runs": runs, "thresholds_Rm": thr, "saturated": [[r["Re"], r["Pm"]] for r in sat],
           "x": {"label": "Rm = Re × Pm", "values": [r["Rm"] for r in runs]},
           "y": {"label": "s, kinematic growth rate"},
           "series": [{"name": f"Pm = {Pm:g}", "kind": "simulated", "field": "b", "x": [r["Rm"] for r in runs if r["Pm"] == Pm],
                       "y": [r["s_kin"] for r in runs if r["Pm"] == Pm]} for Pm in sorted({r["Pm"] for r in runs})],
           "fields": {"n_runs": str(len(runs)), "n_saturated": str(len(sat)), "n_growing": str(sum(r["s_kin"] > 0 for r in runs)),
                      "thresholds": "; ".join(f"Pm {k}: about {v:.2g}" for k, v in thr.items()) or "none bracketed", "verdict": verdict.replace("_", " ")}}
    return doc


# ================================================================================================
# 10.7 fm3d evaluation: lamps (a)-(d) of the tier-2 criteria (T:917), indicative only (A7)
# ================================================================================================
def _holdout(config):
    try:
        import yaml
        cfg = yaml.safe_load(open(config))
        sp = cfg.get("data", {}).get("split", cfg.get("data", {}))
        return [dict(x) for x in (sp.get("val") or [])], [dict(x) for x in (sp.get("test") or [])]
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"cannot read the val/test points from {config} ({e}); pass --holdout '{{\"val\": [...], \"test\": [...]}}'")


def _match(point, lst):
    return any(all(abs(float(point.get(k, math.nan)) - float(v)) < 1e-9 for k, v in q.items()) for q in lst)


def conv_fm3d_eval(eval_path, holdout=None, tg=None, div_tol=1e-12, spec_tol=0.1):
    """lamps: (a) relative divergence of u and B < div_tol at every point; (b) log-spectrum error of u and B
    < spec_tol decade per band at the TRAINING points (T:917; diagnostic only at val/test, A7); (c) Rm_c within
    10 % at a Pm without data and (d) threshold error halved by branch conditioning: not testable at this
    scale (inconclusive). Points whose reference run is not saturated (tg flags, A8) are marked."""
    rep = json.load(open(eval_path))
    val, test = holdout or ([], [])
    sat = None
    if tg:
        sat = {(float(a), float(b)) for a, b in json.load(open(tg)).get("saturated", [])}
    pts = []
    for r in rep["results"]:
        P, M, Dd = r["point"], r["metrics"], r.get("details", {})
        role = "val" if _match(P, val) else "test" if _match(P, test) else "train"
        pts.append({"point": P, "role": role, "div_u": M.get("div_rel_u"), "div_b": M.get("div_rel_b"),
                    "spec_u": M.get("err_spectre_u_log10"), "spec_b": M.get("err_spectre_b_log10"),
                    "dist": M.get("dist_energie"), "floor": M.get("plancher_dist_energie"), "budget": M.get("residu_bilan_total"),
                    "saturated_ref": None if sat is None else (float(P.get("Re", -1)), float(P.get("Pm", -1))) in sat,
                    "spectra": {k: Dd[k] for k in ("spectrum_u", "spectrum_b", "spectrum_u_ref", "spectrum_b_ref") if k in Dd}})
    divs = [v for p in pts for v in (p["div_u"], p["div_b"]) if v is not None]
    la = "met" if divs and max(divs) < div_tol else ("not_met" if divs else "inconclusive")
    tr = [p for p in pts if p["role"] == "train" and p["spec_u"] is not None and p["spec_b"] is not None]
    worst_b = max((max(p["spec_u"], p["spec_b"]) for p in tr), default=None)
    lb = "inconclusive" if worst_b is None else ("met" if worst_b < spec_tol else "not_met")
    lamps = [{"id": "a", "state": la, "value": rnd(max(divs)) if divs else None},
             {"id": "b", "state": lb, "value": rnd(worst_b)},
             {"id": "c", "state": "inconclusive", "value": "full tier needed"},
             {"id": "d", "state": "inconclusive", "value": "full tier needed"}]
    # the verdict covers the criteria testable at this scale, (a) and (b); (c) and (d) stay inconclusive lamps
    verdict = "not_met" if "not_met" in (la, lb) else ("met" if la == lb == "met" else "inconclusive")
    doc = {"meta": meta([eval_path] + ([tg] if tg else []), "GENERATED · fm3d · evaluation",
                        note=f"model {rep.get('model_id') or rep.get('model')}; created {rep.get('created')}; indicative at 12 × 40 snapshots (plan: about 20 × 5000, T:912)"),
           "verdict": verdict, "verdict_rule": f"(a) divergence < {div_tol:g} everywhere; (b) log-spectrum error < {spec_tol} decade per band at the training points (T:917); (c), (d) need the full tier",
           "verdict_text": "(a) and (b) only, indicative at 12 runs × 40 snapshots (plan: about 20 × 5000); (c) and (d) need the full tier",
           "lamps": lamps, "points": rnd(pts), "model": rep.get("model_id") or rep.get("model"),
           "fields": {"worst_spectrum_error": say(worst_b), "max_divergence": say(max(divs) if divs else None),
                      "n_points": str(len(pts)), "verdict": verdict.replace("_", " ")}}
    return doc


# ================================================================================================
# X3.5 stationarity loss in 3D: fine-tuned model vs control (weight 0)
# ================================================================================================
def conv_fm3d_stat(eval_path, control_path, budget_tol=0.05, spread=(0.8, 1.2)):
    """per point: |budget residual| with the loss and with the control; the bet (adapted from the tier-1
    criteria, the plan sets none for 3D, A9): residual < budget_tol at points without data, the control gains
    nothing (its residual stays above), and, when the report has it, the dissipation spread ratio within
    `spread` (std_diss_rel is not computed by milady.eval today: C:166 -> inconclusive)."""
    A, C = json.load(open(eval_path)), json.load(open(control_path))
    key = lambda r: json.dumps(r["point"], sort_keys=True)
    ctrl = {key(r): r for r in C["results"]}
    rows = []
    for r in A["results"]:
        c = ctrl.get(key(r))
        rows.append({"point": r["point"], "residual": r["metrics"].get("residu_bilan_total"), "residual_control": c and c["metrics"].get("residu_bilan_total"),
                     "dist": r["metrics"].get("dist_energie"), "dist_control": c and c["metrics"].get("dist_energie"),
                     "spread_ratio": r["metrics"].get("std_diss_rel")})
    ok_res = [abs(x["residual"]) < budget_tol for x in rows if x["residual"] is not None]
    gain = [abs(x["residual"]) < abs(x["residual_control"]) for x in rows if x["residual"] is not None and x["residual_control"] is not None]
    spr = [x["spread_ratio"] for x in rows if x["spread_ratio"] is not None]
    l_res = "met" if ok_res and all(ok_res) else ("not_met" if ok_res else "inconclusive")
    l_ctrl = "met" if gain and all(gain) else ("not_met" if gain else "inconclusive")
    l_spr = "inconclusive" if not spr else ("met" if all(spread[0] <= v <= spread[1] for v in spr) else "not_met")
    lamps = [{"id": "budget", "state": l_res, "value": rnd(max(abs(x["residual"]) for x in rows if x["residual"] is not None)) if ok_res else None},
             {"id": "control", "state": l_ctrl, "value": None},
             {"id": "spread", "state": l_spr, "value": rnd(spr) if spr else "not computed by milady.eval"}]
    states = [l["state"] for l in lamps]
    verdict = "not_met" if "not_met" in states else ("met" if all(s == "met" for s in states) else "inconclusive")
    return {"meta": meta([eval_path, control_path], "GENERATED · fm3d + stationarity loss",
                         note="bet adapted from the tier-1 criteria (T:903); the plan sets no budget target in 3D (T:917)"),
            "verdict": verdict, "verdict_rule": f"|budget residual| < {budget_tol} at every point; control residual larger; σ(dissipation) ratio in {list(spread)}",
            "verdict_text": "the control run must not reach the same budget: otherwise the loss did nothing",
            "lamps": lamps, "points": rnd(rows),
            "fields": {"worst_residual_percent": say(100 * max((abs(x["residual"]) for x in rows if x["residual"] is not None), default=float("nan"))),
                       "verdict": verdict.replace("_", " ")}}


# ================================================================================================
# X5.3 campaign trace, X5.5 compute bill (catalog dumps)
# ================================================================================================
def conv_trace(catalog_path):
    sims = json.load(open(catalog_path))
    rows = []
    for s in sims:
        files = s.get("files") or []
        rows.append({"id": s.get("id"), "parameters": s.get("parameters"), "status": s.get("status"), "wall_time_s": s.get("wall_time_s"),
                     "started_at": s.get("started_at"), "finished_at": s.get("finished_at"), "n_gpus": s.get("n_gpus"),
                     "files": [{"uri": f.get("uri"), "sha256": (f.get("sha256") or "")[:12], "size_bytes": f.get("size_bytes")} for f in files]})
    done = [r for r in rows if r["status"] in ("done", "completed", "finished", "ok")]
    total_s = sum(r["wall_time_s"] or 0 for r in rows)
    size = sum(f["size_bytes"] or 0 for r in rows for f in r["files"])
    camp = (sims[0].get("campaign") if sims else None) or "campaign"
    verdict = "met" if rows and len(done) == len(rows) else ("not_met" if rows else "inconclusive")
    return {"meta": meta([catalog_path], f"CATALOG · {camp}"[:44], note="python -m milady.catalog sims --campaign <name> (JSON dump)"),
            "verdict": verdict, "verdict_rule": "every simulation of the campaign finished, with a checksummed file", "verdict_text": f"{len(done)} of {len(rows)} simulations finished",
            "campaign": camp, "simulations": rnd(rows), "totals": {"n": len(rows), "done": len(done), "wall_time_h": rnd(total_s / 3600), "bytes": size},
            "fields": {"n_sims": str(len(rows)), "n_done": str(len(done)), "hours": say(total_s / 3600), "gigabytes": say(size / 1e9)}}


def conv_bill(catalog_paths, plan_path):
    """measured GPU (or CPU) hours per campaign from wall_time_s × max(n_gpus, 1) against the plan's estimates
    (a JSON {campaign: hours} that YOU pass, transcribed from the thesis T:955-974; no number is typed here).
    Gauge value = measured / planned for the campaigns present; verdict met within the plan's factor-two band."""
    plan = json.load(open(plan_path))
    meas = {}
    for p in catalog_paths:
        for s in json.load(open(p)):
            c = s.get("campaign") or "?"
            meas[c] = meas.get(c, 0.0) + (s.get("wall_time_s") or 0) * max(1, int(s.get("n_gpus") or 0)) / 3600
    common = [c for c in meas if c in plan]
    ratio = (sum(meas[c] for c in common) / sum(plan[c] for c in common)) if common else None
    verdict = "inconclusive" if ratio is None else ("met" if 0.5 <= ratio <= 2 else "not_met")
    return {"meta": meta(list(catalog_paths) + [plan_path], "CATALOG · compute bill", note="hours = wall_time_s × max(n_gpus, 1); plan from T:955-974 as passed"),
            "verdict": verdict, "verdict_rule": "measured / planned hours within [0.5, 2] (the plan's band of at least a factor two, T:974)",
            "verdict_text": "" if ratio is None else f"measured / planned = {ratio:.2g}",
            "value": rnd(ratio), "measured_hours": rnd(meas), "planned_hours": plan,
            "fields": {"ratio": say(ratio), "measured_hours": say(sum(meas.values())), "verdict": verdict.replace("_", " ")}}


# ================================================================================================
# X5.4 X-points (saddles of the magnetic potential a), reference MFF vs generated npz
# ================================================================================================
def xpoint_count(bx, by):
    """number of saddle points of a, with B = (d_y a, -d_x a), on a periodic grid: cells where both
    components of grad a change sign, classified by the sign of det(Hessian) (< 0: X-point)"""
    n = bx.shape[0]
    k = np.fft.fftfreq(n, 1.0 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0
    ah = -(1j * KY * np.fft.fft2(bx) - 1j * KX * np.fft.fft2(by)) / k2
    ah[0, 0] = 0
    d = lambda f: np.real(np.fft.ifft2(f))
    ax, ay = d(1j * KX * ah), d(1j * KY * ah)
    axx, ayy, axy = d(-KX * KX * ah), d(-KY * KY * ah), d(-KX * KY * ah)
    # a grid square (corners i..i+1, j..j+1, periodic) may hold a critical point when both components of
    # grad a take both signs on its corners; adjacent candidate squares are one critical point (flood fill)
    def mixed(f):
        q = [f > 0, np.roll(f, -1, 0) > 0, np.roll(f, -1, 1) > 0, np.roll(np.roll(f, -1, 0), -1, 1) > 0]
        return np.logical_or.reduce(q) & ~np.logical_and.reduce(q)
    cand = mixed(ax) & mixed(ay)
    det = axx * ayy - axy ** 2
    det = (det + np.roll(det, -1, 0) + np.roll(det, -1, 1) + np.roll(np.roll(det, -1, 0), -1, 1)) / 4
    seen, count = np.zeros_like(cand), 0
    for i0, j0 in zip(*np.nonzero(cand)):
        if seen[i0, j0]:
            continue
        stack, cells = [(i0, j0)], []
        seen[i0, j0] = True
        while stack:
            i, j = stack.pop()
            cells.append((i, j))
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a2, b2 = (i + di) % n, (j + dj) % n
                if cand[a2, b2] and not seen[a2, b2]:
                    seen[a2, b2] = True
                    stack.append((a2, b2))
        if np.mean([det[c] for c in cells]) < 0:
            count += 1
    return count


def conv_xpoints(files, generated=None, tol=None):
    mff = need_milady()
    ref, paths = [], []
    for p in files:
        B = mff.read_mff(p, fields=["magnetic_field"])["fields"]["magnetic_field"]
        ref += [xpoint_count(b[..., 0], b[..., 1]) for b in B.reshape(-1, *B.shape[2:])]
        paths.append(p)
    gen = []
    if generated:
        z = np.load(generated)
        G = z["magnetic_field"]
        gen = [xpoint_count(b[..., 0], b[..., 1]) for b in G.reshape(-1, *G.shape[-3:])]
        paths.append(generated)
    mr, mg = float(np.mean(ref)), (float(np.mean(gen)) if gen else None)
    rel = None if mg is None else abs(mg - mr) / max(mr, 1e-12)
    verdict = "inconclusive" if rel is None or tol is None else ("met" if rel < tol else "not_met")
    hi = max(ref + gen) + 1
    return {"meta": meta(paths, "SIMULATED vs GENERATED · X-points", note="saddles of the magnetic potential a; no threshold in the plan (T:872-876): pass --tolerance to judge"),
            "verdict": verdict, "verdict_rule": "relative difference of the mean X-point counts < tolerance" if tol else "no tolerance set: compare the two distributions by eye",
            "verdict_text": "" if rel is None else f"mean counts: reference {mr:.3g}, generated {mg:.3g}",
            "counts_reference": ref, "counts_generated": gen, "bins": list(range(hi + 1)),
            "fields": {"mean_reference": say(mr), "mean_generated": say(mg), "verdict": verdict.replace("_", " ")}}


# ================================================================================================
# X4.5 tier 0 with 3 seeds: an E1-style results JSON
# ================================================================================================
def conv_tier0(e1_path):
    d = json.load(open(e1_path))
    seeds = d["config"].get("seeds", [])
    g = d["grille_fine"]
    res = d.get("resume", {})
    # Rice error far from / near the threshold, as the report reads E1 (cumulative relative error)
    G = np.array([r["Gamma"] for r in g])
    sim = np.array([r["taux_simulation"] for r in g])
    mod = np.array([r["taux_rice_modele"] for r in g])
    on = sim > 0
    err = float(np.sum(np.abs(mod[on] - sim[on])) / max(np.sum(sim[on]), 1e-300)) if on.any() else None
    verdict = "inconclusive"   # the tier-0 criteria (T:878-890) need the 1e6-snapshot campaign; 3 seeds only firm up E1
    return {"meta": meta([e1_path], f"DATA · tier 0 · {len(seeds)} seeds"),
            "verdict": verdict, "verdict_rule": "tier-0 criteria T:878-890 need 1e6 snapshots per Γ; this file firms up E1 with more seeds",
            "verdict_text": f"{len(seeds)} seeds; cumulative Rice error {err:.2g}" if err is not None else f"{len(seeds)} seeds",
            "x": {"label": "Γ, control parameter", "values": G.tolist(), "train": [bool(r["dans_entrainement"]) for r in g]},
            "y": {"label": "crossing rate of D (per unit time)"},
            "series": [{"name": "simulation (counted crossings)", "kind": "simulated", "field": "b", "y": rnd(sim.tolist())},
                       {"name": "Rice, generated", "kind": "generated", "field": "metric", "y": rnd(mod.tolist())}],
            "summary": rnd(res), "seeds": seeds,
            "fields": {"n_seeds": str(len(seeds)), "cumulative_error_percent": say(100 * err if err is not None else None), "verdict": "inconclusive"}}


# ================================================================================================
# generic seat JSON (VKS, DRESDYN, branch conditioning, Rice levels): validate and stamp
# ================================================================================================
def conv_seat(path):
    s = json.load(open(path))
    t = s.get("type")
    if t not in ("lamps", "curve", "gauge", "map"):
        raise SystemExit("seat JSON: type must be lamps | curve | gauge | map")
    if s.get("verdict") not in VERDICTS:
        raise SystemExit("seat JSON: verdict must be met | not_met | inconclusive")
    if t == "lamps" and not all(l.get("state") in VERDICTS for l in s.get("lamps", [])):
        raise SystemExit("seat JSON: every lamp needs state met | not_met | inconclusive")
    if t == "curve" and not s.get("series"):
        raise SystemExit("seat JSON: curve needs series")
    if t == "gauge" and not isinstance(s.get("value"), (int, float)):
        raise SystemExit("seat JSON: gauge needs a numeric value")
    doc = {k: v for k, v in s.items() if k not in ("stamp", "source")}
    doc["meta"] = meta([path], s.get("stamp") or "DATA · consortium results", note=f"generic seat JSON; produced by: {s.get('source', 'unknown')}")
    doc.setdefault("fields", {})["verdict"] = s["verdict"].replace("_", " ")
    return doc


# ================================================================================================
# selftest: tiny synthetic inputs (no simulation: analytic arrays written with milady.data.format)
# ================================================================================================
def selftest():
    mff = need_milady()
    tmp = tempfile.mkdtemp(prefix="data_cloud_selftest_", dir=os.environ.get("TMPDIR"))
    rng = np.random.default_rng(0)
    out = os.path.join(tmp, "out")
    os.makedirs(out)
    ok = []

    def check(name, cond):
        ok.append((name, bool(cond)))
        print(("PASS " if cond else "FAIL ") + name)

    # palier1: 2 trajectories, 4 kept snapshots on 8x8, diagnostics with a flat injection
    p1 = []
    for i, eta in enumerate((0.004, 0.008, 0.016)):
        n, nt = 8, 4
        tt = np.arange(nt, dtype=float) + 30.0
        x = np.linspace(0, 2 * np.pi, n, endpoint=False)
        B = np.zeros((2, nt, n, n, 2), np.float32)
        B[..., 0] = np.sin(x)[None, None, None, :]
        U = np.zeros_like(B)
        td = np.arange(30.0, 34.0, 0.5)
        diss = 0.0895 + 0.01 * rng.standard_normal((2, td.size))
        diss -= diss.mean() - 0.0895 * (1 + 0.01 * i)
        p = os.path.join(tmp, f"p1_{i}.h5")
        mff.write_mff(p, {"velocity": U, "magnetic_field": B}, {"time": tt, "x": x, "y": x}, {"eta": eta, "nu": 0.008},
                      diagnostics={"time": td, "dissipation": diss, "injection": np.full((2, td.size), 0.0895),
                                   "magnetic_energy": np.full((2, td.size), 0.1)}, meta={"git_commit": "selftest"})
        p1.append(p)
    d = conv_palier1(p1)
    write(d, os.path.join(out, "palier1_sweep.json"))
    check("palier1: 3 eta, verdict met (residual 2 % < 5 %)", len(d["per_eta"]) == 3 and d["verdict"] == "met")
    check("palier1: injection is flat (Ito rate)", all(abs(r["injection"] - 0.0895) < 1e-12 for r in d["per_eta"]))

    # abc3d: ln|B| = s t + noise-free, s chosen to place a window 9 < Rm < 17.6
    s_of = lambda Rm: 0.008 * (Rm - 9) * (17.6 - Rm) / 17.2
    p2 = []
    for Rm in (8, 12, 17, 18, 20):
        n = 4
        tt = np.array([150.0, 200.0, 250.0])
        x = np.linspace(0, 2 * np.pi, n, endpoint=False)
        Bf = rng.standard_normal((2, tt.size, n, n, n, 3)).astype(np.float32)
        td = np.arange(150.0, 250.01, 0.5)
        lb = np.stack([s_of(Rm) * td + c for c in (0.0, 0.3)])
        p = os.path.join(tmp, f"abc_{Rm}.h5")
        mff.write_mff(p, {"magnetic_field": Bf}, {"time": tt, "x": x, "y": x, "z": x}, {"Rm": float(Rm)},
                      diagnostics={"time": td, "log_b_rms": lb}, meta={"git_commit": "selftest"})
        p2.append(p)
    d = conv_abc3d(p2, modes=(12,))
    write(d, os.path.join(out, "palier2_abc3d.json"))
    check("abc3d: s(17) > 0 > s(18) -> met", d["verdict"] == "met")
    check("abc3d: two thresholds near 9 and 17.6", len(d["thresholds"]) == 2 and abs(d["thresholds"][0] - 9) < 0.5 and abs(d["thresholds"][1] - 17.6) < 0.5)
    d2 = conv_abc3d([q for q in p2 if not q.endswith("_17.h5")], modes=())
    check("abc3d: Rm = 17 missing -> inconclusive", d2["verdict"] == "inconclusive")

    # tg3d: E_B grows exponentially then saturates (Rm above threshold) or decays (below)
    p3 = []
    for Re in (25, 50, 100):
        for Pm in (0.5, 1.0):
            n = 4
            Rm = Re * Pm
            s = 0.05 * (Rm - 40) / 40
            td = np.arange(0.0, 140.01, 0.5)
            Eb = 1e-6 * np.exp(2 * s * td)
            if s > 0:
                Eb = np.minimum(Eb, 0.05 * (1 + 0.001 * np.sin(td)))
            tt = np.arange(100.0, 140.0, 10.0)
            x = np.linspace(0, 2 * np.pi, n, endpoint=False)
            U = rng.standard_normal((1, tt.size, n, n, n, 3)).astype(np.float32)
            p = os.path.join(tmp, f"tg_{Re}_{Pm}.h5")
            mff.write_mff(p, {"velocity": U, "magnetic_field": 0.1 * U}, {"time": tt, "x": x, "y": x, "z": x}, {"Re": float(Re), "Pm": Pm},
                          diagnostics={"time": td, "magnetic_energy": Eb[None]}, meta={"git_commit": "selftest"})
            p3.append(p)
    d = conv_tg3d(p3)
    tgp = os.path.join(out, "palier2_tg3d.json")
    write(d, tgp)
    check("tg3d: threshold bracketed at two Pm -> met", d["verdict"] == "met" and len(d["thresholds_Rm"]) == 2)
    fl = {r["Rm"]: r["flag"] for r in d["runs"]}
    check("tg3d: Rm 100 saturated, Rm 50 still growing at t = 140 (A8), Rm < 40 decaying",
          fl[100.0] == "saturated" and fl[50.0] == "growing" and all(f == "decaying" for R, f in fl.items() if R < 40))

    # fm3d evaluation report (schema of milady.eval.metrics.main)
    def res(Re, Pm, spec, div=1e-15):
        return {"point": {"Re": Re, "Pm": Pm}, "physical_parameters": {"Rm": Re * Pm},
                "metrics": {"div_rel_u": div, "div_rel_b": div, "err_spectre_u_log10": spec, "err_spectre_b_log10": spec / 2,
                            "dist_energie": 0.3, "plancher_dist_energie": 0.1, "residu_bilan_total": 0.04},
                "details": {"spectrum_u": [1, 0.5], "spectrum_b": [1, 0.4], "spectrum_u_ref": [1, 0.5], "spectrum_b_ref": [1, 0.4]}, "seconds": 1.0}
    ev = {"model": "fm3d", "model_id": "00000000-selftest", "created": "2027-01-01T00:00:00+00:00",
          "results": [res(25, 0.5, 0.05), res(200, 2.0, 0.08), res(100, 1.0, 0.3), res(50, 2.0, 0.4)]}
    ep = os.path.join(tmp, "eval.json")
    json.dump(ev, open(ep, "w"))
    d = conv_fm3d_eval(ep, holdout=([{"Re": 100, "Pm": 1.0}], [{"Re": 50, "Pm": 2.0}]), tg=tgp)
    write(d, os.path.join(out, "fm3d_eval.json"))
    check("fm3d-eval: (b) judged at training points only (val 0.3, test 0.4 ignored) -> met", d["lamps"][1]["state"] == "met" and d["verdict"] == "met")
    check("fm3d-eval: (c), (d) not testable at this scale", [l["state"] for l in d["lamps"][2:]] == ["inconclusive", "inconclusive"])
    ev2 = json.loads(json.dumps(ev))
    for r in ev2["results"]:
        r["metrics"]["residu_bilan_total"] = 0.2
    cp = os.path.join(tmp, "eval_ctrl.json")
    json.dump(ev2, open(cp, "w"))
    d = conv_fm3d_stat(ep, cp)
    write(d, os.path.join(out, "fm3d_stationarity.json"))
    check("fm3d-stat: budget met, control worse, spread missing -> inconclusive", [l["state"] for l in d["lamps"]] == ["met", "met", "inconclusive"] and d["verdict"] == "inconclusive")

    # catalog dumps
    sims = [{"id": f"s{i}", "campaign": "palier1_mhd2d", "parameters": {"eta": 0.004 * i}, "status": "done", "wall_time_s": 1800.0, "n_gpus": 0,
             "files": [{"uri": f"store/{i}/fields.h5", "sha256": "ab" * 32, "size_bytes": 10 ** 7}]} for i in range(1, 4)]
    cat = os.path.join(tmp, "sims.json")
    json.dump(sims, open(cat, "w"))
    d = conv_trace(cat)
    write(d, os.path.join(out, "x5_campaign_trace.json"))
    check("trace: 3 of 3 finished", d["verdict"] == "met" and d["totals"]["n"] == 3)
    plan = os.path.join(tmp, "plan.json")
    json.dump({"palier1_mhd2d": 1.0}, open(plan, "w"))
    d = conv_bill([cat], plan)
    write(d, os.path.join(out, "x5_compute_bill.json"))
    check("bill: 1.5 h measured vs 1 h planned -> within factor two", d["verdict"] == "met" and abs(d["value"] - 1.5) < 1e-9)

    # X-points on an analytic field: a = cos x cos y has 4 saddles on [0, 2pi)^2 (at x, y in {pi/2, 3pi/2})
    n = 32
    x = np.linspace(0, 2 * np.pi, n, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing="ij")
    a = np.cos(X) * np.cos(Y)
    bx, by = -np.cos(X) * np.sin(Y), np.sin(X) * np.cos(Y)   # B = (d_y a, -d_x a)
    check("xpoints: cos x cos y has 4 saddles", xpoint_count(bx, by) == 4)
    xs = x + 0.37 * (x[1] - x[0])   # same field, grid off the critical points
    Xs, Ys = np.meshgrid(xs, xs, indexing="ij")
    check("xpoints: 4 saddles on a shifted grid", xpoint_count(-np.cos(Xs) * np.sin(Ys), np.sin(Xs) * np.cos(Ys)) == 4)
    Bm = np.stack([bx, by], -1)[None, None].astype(np.float32)
    p = os.path.join(tmp, "xp_ref.h5")
    mff.write_mff(p, {"magnetic_field": np.repeat(Bm, 2, 1)}, {"time": np.array([0.0, 1.0]), "x": x, "y": x}, {"eta": 0.008}, meta={"git_commit": "selftest"})
    gp = os.path.join(tmp, "gen.npz")
    np.savez(gp, magnetic_field=np.repeat(Bm[0], 3, 0))
    d = conv_xpoints([p], gp, tol=0.1)
    write(d, os.path.join(out, "x5_xpoints.json"))
    check("xpoints: same field -> met", d["verdict"] == "met")

    # tier0 from an E1-style JSON (tiny)
    e1 = {"config": {"seeds": [0, 1, 2]}, "resume": {}, "grille_fine": [
        {"Gamma": 0.86, "taux_simulation": 0.0, "taux_rice_modele": 0.0001, "dans_entrainement": True},
        {"Gamma": 0.9, "taux_simulation": 0.0044, "taux_rice_modele": 0.0063, "dans_entrainement": True}]}
    e1p = os.path.join(tmp, "e1.json")
    json.dump(e1, open(e1p, "w"))
    d = conv_tier0(e1p)
    write(d, os.path.join(out, "x4_tier0.json"))
    check("tier0: 3 seeds, inconclusive by design", d["fields"]["n_seeds"] == "3" and d["verdict"] == "inconclusive")

    # generic seat
    sp = os.path.join(tmp, "vks.json")
    json.dump({"type": "lamps", "stamp": "SIMULATED · SFEMaNS · VKS", "source": "selftest", "verdict": "inconclusive",
               "lamps": [{"id": "a", "state": "met", "value": 0.07}, {"id": "b", "state": "inconclusive"}]}, open(sp, "w"))
    d = conv_seat(sp)
    write(d, os.path.join(out, "tier3_vks.json"))
    check("seat: generic VKS lamps stamped", d["meta"]["stamp"].startswith("SIMULATED") and d["lamps"][0]["state"] == "met")

    bad = [n for n, c in ok if not c]
    print(f"selftest: {len(ok) - len(bad)}/{len(ok)} passed; outputs in {out}")
    return 1 if bad else 0


# ================================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    def add(name, **kw):
        p = sub.add_parser(name)
        p.add_argument("--out", default=None)
        return p
    p = add("palier1"); p.add_argument("--mff", nargs="+", required=True); p.add_argument("--tol", type=float, default=0.05)
    p = add("abc3d"); p.add_argument("--mff", nargs="+", required=True); p.add_argument("--modes", default="8,12,16,20")
    p = add("tg3d"); p.add_argument("--mff", nargs="+", required=True); p.add_argument("--sat-frac", type=float, default=0.1); p.add_argument("--no-spectra", action="store_true")
    p = add("fm3d-eval"); p.add_argument("--eval", required=True); p.add_argument("--tg"); p.add_argument("--config", default=os.path.join(REPO, "infra/configs/train_fm3d.yaml")); p.add_argument("--holdout")
    p = add("fm3d-stat"); p.add_argument("--eval", required=True); p.add_argument("--control", required=True)
    p = add("trace"); p.add_argument("--catalog", required=True)
    p = add("bill"); p.add_argument("--catalog", nargs="+", required=True); p.add_argument("--plan", required=True)
    p = add("xpoints"); p.add_argument("--mff", nargs="+", required=True); p.add_argument("--generated"); p.add_argument("--tolerance", type=float)
    p = add("tier0"); p.add_argument("--e1", required=True)
    p = add("seat"); p.add_argument("--in", dest="inp", required=True); p.add_argument("--name", required=True)
    sub.add_parser("selftest")
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return selftest()
    D = os.path.join(HERE, "data")
    if a.cmd == "palier1":
        doc, name = conv_palier1(expand(a.mff), tol=a.tol), "palier1_sweep"
    elif a.cmd == "abc3d":
        doc, name = conv_abc3d(expand(a.mff), modes=tuple(float(m) for m in a.modes.split(",") if m)), "palier2_abc3d"
    elif a.cmd == "tg3d":
        doc, name = conv_tg3d(expand(a.mff), sat_frac=a.sat_frac, spectra=not a.no_spectra), "palier2_tg3d"
    elif a.cmd == "fm3d-eval":
        ho = tuple(json.loads(a.holdout)[k] for k in ("val", "test")) if a.holdout else _holdout(a.config)
        doc, name = conv_fm3d_eval(a.eval, ho, a.tg), "fm3d_eval"
    elif a.cmd == "fm3d-stat":
        doc, name = conv_fm3d_stat(a.eval, a.control), "fm3d_stationarity"
    elif a.cmd == "trace":
        doc, name = conv_trace(a.catalog), "x5_campaign_trace"
    elif a.cmd == "bill":
        doc, name = conv_bill(a.catalog, a.plan), "x5_compute_bill"
    elif a.cmd == "xpoints":
        doc, name = conv_xpoints(expand(a.mff), a.generated, a.tolerance), "x5_xpoints"
    elif a.cmd == "tier0":
        doc, name = conv_tier0(a.e1), "x4_tier0"
    else:
        doc, name = conv_seat(a.inp), a.name
    write(doc, a.out or os.path.join(D, name + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
