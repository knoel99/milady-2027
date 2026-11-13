"""Digest of experiment E4 (Markdown), selection of the measured variant, merge of the group files.

    python3 e4_digest.py            # prints the E4 section; experiments/digest.py includes it in results/digest.md

Reads results/e4_data.json, e4_reference.json and e4_mhd3d_s<k>.json (k = 0 … 4, merged from the group
files e4_mhd3d_s<k>_A.json and _B.json). Writes results/e4_selection.json: the variant measured by the
race objectives C1–C5, T1 and T2, i.e. the generator with the lowest energy-distance ratio on the
**validation** η (mean over the seeds); the held-out test η play no part in the selection.
Standard library and NumPy only.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent / "results"
SEEDS = (0, 1, 2, 3, 4)
GENERATORS = ["W0_free", "W1_penalty", "W2_final_projection", "W3_projected_flow", "W4_potentials",
              "W4s_potentials_sym", "W5_stationarity", "W5_control", "W6_diffusion", "W4c_potentials_smooth",
              "G0_gaussian_modes", "W9_skip_sym", "W10_anchored", "W11_anchored_skip", "W9L_skip_long",
              "W11L_anchored_skip_long", "W10L_anchored_long", "G1_gaussian_full", "G2_gaussianised_W9", "G3_gaussianised_G1", "W9N_skip_sym", "W12_skip_stationarity", "W12_skip_control",
              "W13_skip_tilting", "W12_skip_stationarity_half", "W12_skip_control_half",
              "S_w512", "S_w2048", "S_w5632", "S_w512_long", "S_w2048_long"]
# Later variants (H28, H29): checkpoints of the model anchored on G1, W9 retrained in the job and its samples recoloured,
# controls. None is a candidate for the selected generator: iteration 0 of W14 is G1, the choice among its checkpoints is
# the registered rule of H28, and a correction of the samples (like the tilting and the rescaling) never was one.
LATER = [f"W14_full_anchor_it{k}" for k in (0, 50, 150, 250, 500, 1000, 2000, 4000)] + [
    "G1T_gaussian_full", "W9R_skip_sym", "W9R_steps_check", "W15_recoloured_modes", "W16_recoloured_full", "G4_recoloured_gaussian",
    "W9Zb_skip_sym", "W9Z_skip_sym_gaussdata", "W9Yb_skip_sym", "W9Y_skip_sym_gausstraj"] + [
    f"{law}_tau{t}" for law in ("G0X", "G1X", "W9X", "W16X", "REFX") for t in ("0", "0.5", "1", "2", "4", "8")] + [
    "G1V_gaussian_full", "W16V_recoloured_full", "W17_recoloured_surrogate", "REFV_raw", "REFV_recoloured"] + [
    "W9P_skip_sym"] + [f"W18_anchor_on_W9_it{k}" for k in (0, 150, 250, 1000, 2000, 4000)] + ["W9PP_retrained_on_W9"] + [
    f"COLD_tau{t}" for t in ("2", "8", "16", "32", "64", "128", "200")] + [
    "G5_gaussian_struct", "W9Q_skip_sym"] + [f"{t}_it{k}" for t in ("W19_struct_anchor", "W20_struct_anchor_on_W9") for k in (0, 150, 1000, 4000)]
GENERATORS += LATER
# G0 has no network: it is the baseline to beat, not a candidate for the selected generator (the C1 note of
# race/teams/claude/objectives.toml names the model family: conditional flow matching on the Fourier modes).
CANDIDATES = [v for v in GENERATORS if not v.startswith(("G0_", "G1_", "G2_", "G3_")) and v not in LATER]   # learned generators only
REGISTERED = ["W0_free", "W2_final_projection", "W3_projected_flow", "W4_potentials", "W4s_potentials_sym",
              "W5_stationarity", "W6_diffusion"]
POST = ["W7_tilting", "W8_rescaling", "W5_stationarity_half", "W5_control_half"]
KEYS = [("ed_ratio", "ED / floor", False), ("div_rel_b_mean", "rel. div. B", False),
        ("balance_residual_total", "|energy residual|", True), ("balance_residual_magnetic", "|magnetic balance|", True),
        ("spec_err_b_l2", "err. E_B(k)", False),
        ("hel_m_err_rel", "err. H_M", False), ("null_count_err_rel", "err. nulls", False),
        ("restart_drift_eb", "restart drift E_B", False), ("restart_drift_eu", "restart drift E_u", False),
        ("hc_sign_asym", "|P(H_c>0)−½|", False),
        ("std_residual_rel", "σ(dE/dt)/σ_ref", False), ("ess_frac", "ESS/N", False)]


def f(v, d=3):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "–"
    if abs(v) != 0 and (abs(v) < 1e-3 or abs(v) >= 1e4):
        return f"{v:.2e}"
    return f"{v:.{d}g}"


def merge(seed: int, tag: str | bool = "", root: Path = R) -> Path | None:
    """Merge the group files of a seed into results/e4_mhd3d<tag>_s<seed>.json (groups A and B needed, C optional).

    ``tag``: suffix of the run ("" for E4, "_quick", "_cs0.5" for a run with another condition embedding…).
    """
    tag = ("_quick" if tag else "") if isinstance(tag, bool) else tag
    parts = [root / f"e4_mhd3d{tag}_s{seed}_{g}.json" for g in ("A", "B")]
    whole = root / f"e4_mhd3d{tag}_s{seed}_all.json"
    if not all(p.exists() for p in parts) and not whole.exists():        # a run of the later groups only (D, E, L)
        parts = [p for g in ("A", "B") if (p := root / f"e4_mhd3d{tag}_s{seed}_{g}.json").exists()]
        if not any((root / f"e4_mhd3d{tag}_s{seed}_{g}.json").exists() for g in ("C", "D", "E", "L", "S", "G", "M", "N", "F", "R", "T", "Z", "Y", "X", "V", "O", "P", "K", "Q")):
            return None
    if all(p.exists() for p in parts):
        data = [json.loads(p.read_text()) for p in parts]
    elif whole.exists():
        data = [json.loads(whole.read_text())]
    else:
        return None
    for g in ("C", "D", "E", "L", "S", "G", "M", "N", "F", "R", "T", "Z", "Y", "X", "V", "O", "P", "K", "Q"):                      # optional groups, added after the first runs
        extra = root / f"e4_mhd3d{tag}_s{seed}_{g}.json"
        if extra.exists():
            data.append(json.loads(extra.read_text()))
    out = {"config": {**data[0]["config"], "group": "merged"}, "evaluation": {}, "times": {}, "h14": [], "h12": [], "h27": [],
           "durations_s": sorted({round(d["total_duration_s"], 1) for d in data})}      # parts of one run share a duration
    for d in data:
        out["evaluation"].update(d["evaluation"])
        out["times"].update(d["times"])
        out["h14"] += d["h14"]
        out["h12"] += d["h12"]
        out["h27"] += d.get("h27", [])
    path = root / f"e4_mhd3d{tag}_s{seed}.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return path


def load(quick: bool = False, root: Path = R, tag: str = "") -> dict[int, dict]:
    tag = tag + ("_quick" if quick else "")
    out = {}
    for s in SEEDS:
        p = root / f"e4_mhd3d{tag}_s{s}.json"
        parts = list(root.glob(f"e4_mhd3d{tag}_s{s}_*.json"))
        if parts and (not p.exists() or max(q.stat().st_mtime for q in parts) > p.stat().st_mtime):
            merge(s, tag, root)                 # reading never rewrites a merged file that is up to date
        if p.exists():
            out[s] = json.loads(p.read_text())
    return out


def per_seed(runs: dict, variant: str, key: str, split: str = "test", absolute: bool = False) -> np.ndarray:
    """Mean over the η of ``split`` of ``key`` for each seed (NaN where the key is absent)."""
    vals = []
    for r in runs.values():
        rows = r["evaluation"].get(variant, {}).get(split, [])
        v = [abs(x[key]) if absolute else x[key] for x in rows if key in x]
        vals.append(np.mean(v) if v else np.nan)
    return np.asarray(vals)


def paired(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float, float]:
    d = a - b
    se = d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else float("nan")
    return d, float(d.mean()), float(se)


def paired_row(label: str, a: np.ndarray, b: np.ndarray) -> str | None:
    """Row of the table of paired comparisons; None when one of the two variants is not in the run."""
    if np.all(np.isnan(np.asarray(a, dtype=float))) or np.all(np.isnan(np.asarray(b, dtype=float))):
        return None
    d, m, se = paired(a, b)
    return (f"| {label} | {', '.join(f(x) for x in d)} | {f(m)} ± {f(se)} | {f(m / se, 2) if se > 0 else '–'} | "
            f"{int((d > 0).sum())} of {len(d)} |")


def h28_lines(runs: dict, ref: dict | None) -> list[str]:
    """H28: the model anchored on G1 along its training; selection of the checkpoint and verdict, clause by clause, as
    registered (research/hypotheses.json, amendment of 2026-11-13 written before any full run)."""
    names = sorted({v for r in runs.values() for v in r["evaluation"] if v.startswith("W14_full_anchor_it")}, key=lambda v: int(v.rsplit("it", 1)[1]))
    if not names or ref is None:
        return []
    out: list[str] = []
    it = {v: int(v.rsplit("it", 1)[1]) for v in names}

    def cells(v: str, key: str, split: str) -> dict[float, np.ndarray]:
        """{η: values over the seeds} of ``key`` for the variant ``v``."""
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get(split, []):
                if key in x:
                    acc.setdefault(round(x["eta"], 5), []).append(x[key])
        return {e: np.asarray(a) for e, a in sorted(acc.items(), reverse=True)}

    rv = lambda e, key: ref["values"][f"{e:.5f}"][key]                                    # noqa: E731
    ed = lambda v, split: np.mean(list(cells(v, "ed_ratio", split).values()), axis=0)     # noqa: E731  per seed, mean over the η
    third = lambda v, split: {e: a.mean() / rv(e, "prod_fluct_over_d") for e, a in cells(v, "prod_fluct_over_d", split).items()}   # noqa: E731
    mflow = lambda v: {e: a.mean() - rv(e, "prod_mean_over_d") for e, a in cells(v, "prod_mean_over_d", "test").items()}          # noqa: E731
    eb = lambda v: {e: a.mean() / rv(e, "E_B") - 1 for e, a in cells(v, "E_B", "test").items()}                                  # noqa: E731
    mean_abs = lambda v, key: float(np.mean([np.abs(a).mean() for a in cells(v, key, "test").values()])) if cells(v, key, "test") else float("nan")  # noqa: E731
    val_eta = sorted(cells(names[0], "ed_ratio", "val"), reverse=True)
    test_eta = sorted(cells(names[0], "ed_ratio", "test"), reverse=True)
    train_eta = sorted(cells(names[0], "ed_ratio", "train"), reverse=True)
    e_sel = min(val_eta)                                                                   # the lower validation η (0.0403)
    out.append("\nH28: flow matching anchored on the full-covariance Gaussian law, read along one training (seed means; ED / floor: mean over "
               "the η of the split; third-order part over that of the reference; mean-flow part minus that of the reference; E_B over "
               "that of the reference minus 1, on the generated samples).\n")
    head = ["checkpoint", "ED val", "ED test"] + [f"3rd/ref val η={e:.4f}" for e in val_eta] + [f"3rd/ref η={e:.4f}" for e in test_eta] + \
           [f"3rd/ref train η={train_eta[0]:.4f}"] + ["max |mean-flow − ref|", "max |E_B/ref − 1|", "|magnetic balance|", "|energy residual|",
                                                    "err. E_B(k)", "err. H_M", "err. nulls", "drift E_B τ=4", "overshoot E_B", "FM loss",
                                                    "FM loss − iteration 0 (smallest and largest seed)"]
    out.append("| " + " | ".join(head) + " |")
    out.append("|---|" + "---|" * (len(head) - 1))
    for v in names:
        tv, tt, ttr = third(v, "val"), third(v, "test"), third(v, "train")
        loss = [r["times"].get(v, {}).get("fm_loss_train_sample") for r in runs.values()]
        loss = [x for x in loss if x is not None]
        dl = [r["times"][v]["fm_loss_train_sample"] - r["times"][names[0]]["fm_loss_train_sample"] for r in runs.values()
              if "fm_loss_train_sample" in r["times"].get(v, {}) and "fm_loss_train_sample" in r["times"].get(names[0], {})]
        row = [f"iteration {it[v]}", f(float(ed(v, "val").mean())), f(float(ed(v, "test").mean()))] + [f(tv[e], 2) for e in val_eta] + \
              [f(tt[e], 2) for e in test_eta] + [f(ttr[train_eta[0]], 2), f(max(abs(x) for x in mflow(v).values())),
                                               f(max(abs(x) for x in eb(v).values())), f(mean_abs(v, "balance_residual_magnetic")),
                                               f(mean_abs(v, "balance_residual_total")), f(mean_abs(v, "spec_err_b_l2")),
                                               f(mean_abs(v, "hel_m_err_rel")), f(mean_abs(v, "null_count_err_rel")),
                                               f(mean_abs(v, "restart_drift_eb")), f(mean_abs(v, "restart_overshoot_eb")),
                                               f(float(np.mean(loss)), 5) if loss else "–",
                                               f"{min(dl):+.1e} to {max(dl):+.1e}" if dl and it[v] > 0 else "–"]
        out.append("| " + " | ".join(row) + " |")
    # measurement check: iteration 0 against G1 sampled exactly in the same job
    v0, g1 = names[0], "G1_gaussian_full"
    if it[v0] == 0 and any(g1 in r["evaluation"] for r in runs.values()):
        d_ed = float(ed(v0, "test").mean() - ed(g1, "test").mean())
        t0 = max(abs(a.mean()) for a in cells(v0, "prod_fluct_over_d", "test").values())
        dm = max(abs(cells(v0, "prod_mean_over_d", "test")[e].mean() - cells(g1, "prod_mean_over_d", "test")[e].mean()) for e in test_eta)
        de = max(abs(cells(v0, "E_B", "test")[e].mean() / cells(g1, "E_B", "test")[e].mean() - 1) for e in test_eta)
        ok = abs(d_ed) <= 0.5 and t0 < 0.02 and dm <= 0.02 and de <= 0.03
        out.append(f"H28, check of the measurement (iteration 0 against G1 of the same job, seed means, held-out η): ED / floor differs by "
                   f"{f(d_ed)} (limit 0.5); largest |third-order part| {f(float(t0))} (limit 0.02); largest difference of the mean-flow part "
                   f"{f(float(dm))} (limit 0.02); largest |E_B(it 0)/E_B(G1) − 1| {f(float(de))} (limit 0.03): {'PASS' if ok else 'FAIL'}.")
    else:
        out.append("H28, check of the measurement: iteration 0 or G1 missing from this run: NOT AVAILABLE.")
    # selection on the validation η, then the clauses of the refutation criterion
    cand = [v for v in names if it[v] > 0]
    qual = [v for v in cand if 0.3 <= third(v, "val")[e_sel] <= 1.5]
    out.append(f"H28, selection on the validation η: third-order part over that of the reference at η = {e_sel:.4f}: "
               + "; ".join(f"iteration {it[v]}: {f(third(v, 'val')[e_sel], 2)} (ED val {f(float(ed(v, 'val').mean()))})" for v in cand)
               + f". Qualifying (between 0.3 and 1.5): {', '.join(str(it[v]) for v in qual) or 'none'}.")
    if not qual:
        out.append("H28, verdict on this realisation of the data: REFUTED (clause a: no checkpoint qualifies on the validation η).")
        return out
    ks = min(qual, key=lambda v: float(ed(v, "val").mean()))
    tt = third(ks, "test")
    low = sorted(test_eta)[:2]                                                             # the two lower held-out η
    signs = {e: int((np.sign(cells(ks, "prod_fluct_over_d", "test")[e]) == np.sign(rv(e, "prod_fluct_over_d"))).sum()) for e in low}
    n_seed = len(next(iter(cells(ks, "prod_fluct_over_d", "test").values())))
    need = min(4, n_seed)
    b_bad = [e for e in low if not (0.3 <= tt[e] <= 1.5) or signs[e] < need]
    r_ed = ed(ks, "test") / ed(v0, "test")
    c_bad = float(ed(ks, "test").mean() / ed(v0, "test").mean()) > 1.5 or int((r_ed > 1.5).sum()) > 1
    d_val, e_val = mflow(ks), eb(ks)
    d_bad = [e for e in test_eta if abs(d_val[e]) > 0.05]
    e_bad = [e for e in test_eta if abs(e_val[e]) > 0.05]
    out.append(f"H28, checkpoint k* = iteration {it[ks]} (smallest ED on the validation η among the qualifying ones). Clause b, third-order part "
               f"over that of the reference at the two lower held-out η: " + ", ".join(f"η = {e:.4f}: {f(tt[e], 2)} ({signs[e]} of {n_seed} seeds with the sign of the reference)" for e in sorted(low, reverse=True))
               + f" (between 0.3 and 1.5, at least {need} seeds): {'FAIL' if b_bad else 'pass'}. Clause c, ED / floor of k* over that of iteration 0: "
               f"{f(float(ed(ks, 'test').mean() / ed(v0, 'test').mean()), 2)} on the seed means, per seed {', '.join(f(float(x), 2) for x in r_ed)} "
               f"(limit 1.5, at most one seed above): {'FAIL' if c_bad else 'pass'}. Clause d, mean-flow part minus that of the reference: "
               + ", ".join(f"{f(float(d_val[e]))}" for e in test_eta) + f" (limit 0.05): {'FAIL' if d_bad else 'pass'}. Clause e, E_B over that of "
               f"the reference minus 1: " + ", ".join(f"{f(float(e_val[e]))}" for e in test_eta) + f" (limit 0.05): {'FAIL' if e_bad else 'pass'}.")
    bad = [c for c, x in (("b", b_bad), ("c", c_bad), ("d", d_bad), ("e", e_bad)) if x]
    out.append(f"H28, verdict on this realisation of the data: {'REFUTED (clauses ' + ', '.join(bad) + ')' if bad else 'NOT REFUTED'}; third-order part "
               f"of k* at η = {max(test_eta):.4f}: {f(tt[max(test_eta)], 2)} of the reference, at the training η = {train_eta[0]:.4f}: "
               f"{f(third(ks, 'train')[train_eta[0]], 2)}.")
    return out


def h29_lines(runs: dict, ref: dict | None) -> list[str]:
    """H29, H30, H31: the samples of W9 recoloured onto the moments of the data, the restart at equal moments, the restart
    of G1 at the training η; verdicts clause by clause, as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    if ref is None or not ({"W16_recoloured_full", "G1T_gaussian_full"} & have):
        return []
    out: list[str] = []
    if "W16_recoloured_full" in have:                      # a run still being assembled: only the seeds that have every law
        full = {s: r for s, r in runs.items() if "G4_recoloured_gaussian" in r["evaluation"]}
        if len(full) < len(runs):
            out.append(f"\nH29-H31: {len(full)} of the {len(runs)} seeds have the recoloured laws; the lines below use these seeds only "
                       "(incomplete run: no verdict may be quoted).")
            runs = full
    n_seed = len(runs)
    need = min(4, n_seed)

    def cells(v: str, fn, split: str = "test") -> dict[float, np.ndarray]:
        """{η: values over the seeds} of ``fn(row)`` for the variant ``v`` (rows without the quantity are skipped)."""
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get(split, []):
                try:
                    acc.setdefault(round(x["eta"], 5), []).append(fn(x))
                except KeyError:
                    pass
        return {e: np.asarray(a) for e, a in sorted(acc.items(), reverse=True)}

    key = lambda k: (lambda x: x[k])                                                     # noqa: E731
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    over_eta = lambda d: np.mean(list(d.values()), axis=0)                               # noqa: E731  per seed, mean over the η
    sem = lambda a: float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")   # noqa: E731
    exc = lambda x: max(0.0, max(x["restart_anchor"]["eb"][1:]))                         # noqa: E731
    rise = lambda x: max(x["restart_anchor"]["eb"][1:]) - x["restart_anchor"]["eb"][0]   # noqa: E731
    amax = lambda x: max(abs(y) for y in x["restart_anchor"]["eb"])                      # noqa: E731
    a0 = lambda x: x["restart_anchor"]["eb"][0]                                          # noqa: E731
    g1 = "G1_gaussian_full" if "G1_gaussian_full" in have else "G1T_gaussian_full"
    w16, w15, g4, w9, chk = "W16_recoloured_full", "W15_recoloured_modes", "G4_recoloured_gaussian", "W9R_skip_sym", "W9R_steps_check"

    if w16 in have:
        etas = sorted(cells(w16, key("ed_ratio")), reverse=True)
        low = sorted(etas)[:2]
        n_rs = sorted({r["config"].get("n_restart") for r in runs.values()})
        out.append(f"\nH29, H30: samples of W9 recoloured onto the moments fitted on the data (seed means on the held-out η; restart of "
                   f"{', '.join(str(x) for x in n_rs)} samples; third-order part over that of the reference; mean-flow part minus that of "
                   f"the reference; E_B of the generated samples over that of the reference minus 1).\n")
        head = ["law", "ED / floor"] + [f"3rd/ref η={e:.4f}" for e in etas] + ["max |mean-flow − ref|", "max |E_B/ref − 1|", "|magnetic balance|",
                "|energy residual|", "err. E_B(k)", "err. H_M", "err. nulls", "σ(dE/dt)/σ_ref", "a(0)", "excursion", "rise", "overshoot",
                "largest |a|", "drift E_B τ=4"]
        out.append("| " + " | ".join(head) + " |")
        out.append("|---|" + "---|" * (len(head) - 1))
        m = lambda v, fn: float(over_eta(cells(v, fn)).mean()) if cells(v, fn) else float("nan")     # noqa: E731
        mabs = lambda v, k: float(np.mean([np.abs(a).mean() for a in cells(v, key(k)).values()])) if cells(v, key(k)) else float("nan")   # noqa: E731
        third = lambda v: {e: a.mean() / rv(e, "prod_fluct_over_d") for e, a in cells(v, key("prod_fluct_over_d")).items()}             # noqa: E731
        mflow = lambda v: {e: a.mean() - rv(e, "prod_mean_over_d") for e, a in cells(v, key("prod_mean_over_d")).items()}               # noqa: E731
        eb = lambda v: {e: a.mean() / rv(e, "E_B") - 1 for e, a in cells(v, key("E_B")).items()}                                        # noqa: E731
        for v in (g1, g4, w9, chk, w15, w16):
            if v not in have:
                continue
            t = third(v)
            out.append("| " + " | ".join([v, f(m(v, key("ed_ratio")))] + [f(t[e], 2) for e in etas] + [
                f(max(abs(x) for x in mflow(v).values())), f(max(abs(x) for x in eb(v).values())), f(mabs(v, "balance_residual_magnetic")),
                f(mabs(v, "balance_residual_total")), f(mabs(v, "spec_err_b_l2")), f(mabs(v, "hel_m_err_rel")), f(mabs(v, "null_count_err_rel")),
                f(mabs(v, "std_residual_rel")), f(m(v, a0)), f(m(v, exc)), f(m(v, rise)), f(mabs(v, "restart_overshoot_eb")), f(m(v, amax)),
                f(mabs(v, "restart_drift_eb"))]) + " |")
        # null control shared by H29 and H30: Gaussian draws through the map of W16 against G1 of the same job
        if g4 in have and g1 in have:
            d_ed = m(g4, key("ed_ratio")) - m(g1, key("ed_ratio"))
            t4 = max(abs(a.mean()) for a in cells(g4, key("prod_fluct_over_d")).values())
            dm = max(abs(cells(g4, key("prod_mean_over_d"))[e].mean() - cells(g1, key("prod_mean_over_d"))[e].mean()) for e in etas)
            de = max(abs(cells(g4, key("E_B"))[e].mean() / cells(g1, key("E_B"))[e].mean() - 1) for e in etas)
            dx = m(g4, exc) - m(g1, exc)
            ok29 = abs(d_ed) <= 0.5 and t4 < 0.02 and dm <= 0.03 and de <= 0.03
            out.append(f"H29, null control (G4 against G1 of the same job): ED / floor differs by {f(d_ed)} (limit 0.5); largest |third-order part| "
                       f"{f(float(t4))} (limit 0.02); largest difference of the mean-flow part {f(float(dm))} (limit 0.03); largest "
                       f"|E_B(G4)/E_B(G1) − 1| {f(float(de))} (limit 0.03): {'PASS' if ok29 else 'FAIL'}. H30, null control: excursion of G4 minus "
                       f"that of G1 {f(dx)} (limit 0.02 in absolute value): {'PASS' if abs(dx) < 0.02 else 'FAIL'}.")
        else:
            ok29 = False
            out.append("H29, H30, null controls: G4 or G1 missing from this run: NOT AVAILABLE.")
        # H29, clause by clause
        t, mf, e_b = third(w16), mflow(w16), eb(w16)
        signs = {e: int((np.sign(cells(w16, key("prod_fluct_over_d"))[e]) == np.sign(rv(e, "prod_fluct_over_d"))).sum()) for e in low}
        a_bad = [e for e in etas if abs(mf[e]) > 0.05 or abs(e_b[e]) > 0.05]
        b_bad = [e for e in low if not (0.3 <= t[e] <= 1.5) or signs[e] < need]
        absbal = lambda v: over_eta({e: np.abs(a) for e, a in cells(v, key("balance_residual_magnetic")).items()})       # noqa: E731
        d = absbal(g1) - absbal(w16) if g1 in have else np.full(n_seed, np.nan)
        c_bad = not (d.mean() > 2 * sem(d) and int((d > 0).sum()) >= need)
        d_ed16 = m(w16, key("ed_ratio")) - (m(g1, key("ed_ratio")) if g1 in have else float("nan"))
        d_bad = not d_ed16 <= 0.5
        out.append(f"H29, clause a (second moments): mean-flow part minus that of the reference {', '.join(f(float(mf[e])) for e in etas)}; "
                   f"E_B over that of the reference minus 1 {', '.join(f(float(e_b[e])) for e in etas)} (limit 0.05 each): {'FAIL' if a_bad else 'pass'}. "
                   f"Clause b (third-order part over that of the reference at the two lower η): "
                   + ", ".join(f"η = {e:.4f}: {f(t[e], 2)} ({signs[e]} of {n_seed} seeds with the sign of the reference)" for e in sorted(low, reverse=True))
                   + f" (between 0.3 and 1.5, at least {need} seeds): {'FAIL' if b_bad else 'pass'}. Clause c (|magnetic balance| of G1 minus that of "
                   f"W16, paired): {f(float(d.mean()))} ± {f(sem(d))}, {int((d > 0).sum())} of {n_seed} seeds positive (more than 2 SE, at least {need} "
                   f"seeds): {'FAIL' if c_bad else 'pass'}. Clause d (ED / floor of W16 minus that of G1): {f(d_ed16)} (limit 0.5): "
                   f"{'FAIL' if d_bad else 'pass'}.")
        bad = [c for c, x in (("a", a_bad), ("b", b_bad), ("c", c_bad), ("d", d_bad)) if x]
        out.append(f"H29, verdict on this realisation of the data: " + ("TEST INVALID (null control)" if not ok29 else
                   ("REFUTED (clauses " + ", ".join(bad) + ")" if bad else "NOT REFUTED")) + ".")
        if chk in have and w9 in have:                       # numerical protocol: 4 times the Heun steps, same noise
            de = max(abs(cells(chk, key("E_B"))[e].mean() - cells(w9, key("E_B"))[e].mean()) / rv(e, "E_B") for e in etas)
            dd = max(abs(cells(chk, key("ed_ratio"))[e].mean() - cells(w9, key("ed_ratio"))[e].mean()) for e in etas)
            steps = sorted({r["times"].get(chk, {}).get("steps") for r in runs.values()} - {None})
            out.append(f"H29, check of the numerical protocol (W9R integrated with {', '.join(str(x) for x in steps)} Heun steps against "
                       f"{', '.join(str(x) for x in sorted({r['config'].get('steps') for r in runs.values()}))}, same noise): largest change of "
                       f"E_B over that of the reference {f(float(de))} (tolerance 0.02); largest change of ED / floor {f(float(dd))} "
                       f"(tolerance 0.5): {'within tolerance' if de <= 0.02 and dd <= 0.5 else 'OUT OF TOLERANCE'}.")
        # H30: excursion above the reference at equal moments
        if g4 in have:
            dx = over_eta(cells(g4, exc)) - over_eta(cells(w16, exc))
            bad30 = not (dx.mean() > 2 * sem(dx) and dx.mean() >= 0.02 and int((dx > 0).sum()) >= need)
            ctl = abs(m(g4, exc) - m(g1, exc)) < 0.02 if g1 in have else False
            per = {e: cells(g4, exc)[e] - cells(w16, exc)[e] for e in etas}
            out.append(f"H30, excursion of E_B above the reference, G4 minus W16, paired over the seeds (mean over the held-out η): "
                       f"{', '.join(f(float(x)) for x in dx)}; {f(float(dx.mean()))} ± {f(sem(dx))}, {int((dx > 0).sum())} of {n_seed} seeds positive "
                       f"(more than 2 SE, at least 0.02, at least {need} seeds). Per η, with the third-order part of W16 over the dissipation: "
                       + "; ".join(f"η = {e:.4f}: {f(float(per[e].mean()))} ± {f(sem(per[e]))}, {int((per[e] > 0).sum())} of {n_seed} positive "
                                   f"(third-order part {f(float(cells(w16, key('prod_fluct_over_d'))[e].mean()))})" for e in etas)
                       + f". Verdict on this realisation of the data: {'TEST INVALID (null control)' if not ctl else ('REFUTED' if bad30 else 'NOT REFUTED')}.")
            # asked by the review of the encadrant role (2026-11-13): paired ED differences per η, the kinetic energy at restart
            ed = key("ed_ratio")
            pairs = [("W16 minus G1", w16, g1), ("G4 minus G1", g4, g1), ("W15 minus W16", "W15_recoloured_modes", w16)]
            out.append("H29, H30, paired differences of ED / floor over the seeds (mean ± SE; per η): " + "; ".join(
                f"{label}: {f(float((over_eta(cells(a, ed)) - over_eta(cells(b, ed))).mean()))} ± {f(sem(over_eta(cells(a, ed)) - over_eta(cells(b, ed))))} ("
                + ", ".join(f"{f(float((cells(a, ed)[e] - cells(b, ed)[e]).mean()))} ± {f(sem(cells(a, ed)[e] - cells(b, ed)[e]))}" for e in etas) + ")"
                for label, a, b in pairs if a in have and b in have) + ".")
            eu = lambda fn: (lambda x: fn(x["restart_anchor"]["eu"]))                    # noqa: E731
            out.append("H30, kinetic energy at restart, E_u(τ)/E_u,ref − 1 (mean over the held-out η and the seeds): " + "; ".join(
                f"{v}: at τ = 0 {f(m(v, eu(lambda a: a[0])))}, largest |value| {f(m(v, eu(lambda a: max(abs(y) for y in a))))}, at the last τ "
                f"{f(m(v, eu(lambda a: a[-1])))}" for v in (g1, g4, "W9R_skip_sym", "W15_recoloured_modes", w16) if v in have) + ".")
    # H31: G1 restarted at the training η, where it has the sample moments of the data
    gt = "G1T_gaussian_full"
    if gt in have and cells(gt, key("restart_overshoot_eb"), "train"):
        ov, a_0, rs, am = (cells(gt, fn, "train") for fn in (key("restart_overshoot_eb"), a0, rise, amax))
        bad31 = [e for e in ov if ov[e].mean() < 0.05 or int((ov[e] < 0.05).sum()) > 1]
        out.append("H31, restart of G1 at the training η (sample moments of the data, no interpolation): " + "; ".join(
            f"η = {e:.4f}: a(0) {f(float(a_0[e].mean()))}, overshoot {f(float(ov[e].mean()))} ± {f(sem(ov[e]))} "
            f"({int((ov[e] < 0.05).sum())} of {len(ov[e])} seeds below 0.05), rise {f(float(rs[e].mean()))}, largest |a| {f(float(am[e].mean()))}"
            for e in ov) + "; at the held-out η: " + "; ".join(
            f"η = {e:.4f}: overshoot {f(float(a.mean()))}" for e, a in cells(gt, key("restart_overshoot_eb")).items())
            + f". Verdict on this realisation of the data: {'REFUTED (η = ' + ', '.join(f'{e:.4f}' for e in bad31) + ')' if bad31 else 'NOT REFUTED'}.")
    return out


def _per_seed(runs: dict, v: str, key: str, split: str = "test") -> dict[float, list[float]]:
    """Values of one variant per η, one per seed (mean over the fields of the seed is already in the file)."""
    acc: dict = {}
    for r in runs.values():
        for x in r["evaluation"].get(v, {}).get(split, []):
            if key in x:
                acc.setdefault(round(x["eta"], 5), []).append(x[key])
    return acc


def h32_lines(runs: dict, ref: dict | None) -> list[str]:
    """H32: Kac-Rice factors of the number of null points (density of B at zero, Jacobian where B is weak), reference
    against G1 and the other laws of the run; verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"] if any("kr_density" in x for x in r["evaluation"][v].get("test", []))}
    g1 = next((v for v in ("G1_gaussian_full", "G1T_gaussian_full") if v in have), None)
    if ref is None or g1 is None or "kr_density" not in next(iter(ref["values"].values())):
        return []
    out: list[str] = []

    def law(v: str, key: str, split: str = "test") -> dict[float, float]:
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get(split, []):
                if key in x:
                    acc.setdefault(round(x["eta"], 5), []).append(x[key])
        return {e: float(np.mean(a)) for e, a in sorted(acc.items(), reverse=True)}

    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    etas = sorted(law(g1, "kr_density"), reverse=True)
    out.append("\nH32: Kac-Rice factors of the mean number of magnetic null points per field (threshold 0.1 of the rms of |B|; density of B "
               "at zero in units of rms⁻³, Jacobian where B is weak in rms³ per cell³; predicted = cells × density × Jacobian; seed means).\n")
    out.append("| law | " + " | ".join(f"η = {e:.4f}: density | Jacobian | predicted | counted" for e in etas) + " |")
    out.append("|---|" + "---|---|---|---|" * len(etas))
    out.append("| reference | " + " | ".join(f"{f(rv(e, 'kr_density'))} | {f(rv(e, 'kr_jacobian'))} | {f(rv(e, 'kr_predicted'))} | "
                                             f"{f(rv(e, 'null_count_mean'))}" for e in etas) + " |")
    order = [v for v in GENERATORS if v in have and not v.startswith("W14_")]
    for v in order:
        d, j, pr, cnt = law(v, "kr_density"), law(v, "kr_jacobian"), law(v, "kr_predicted"), law(v, "null_count")
        out.append(f"| {v} | " + " | ".join(f"{f(d[e])} | {f(j[e])} | {f(pr[e])} | {f(cnt[e])}" for e in etas) + " |")
    out.append("H32, ratios to the reference (density at zero, Jacobian): " + "; ".join(
        f"{v}: " + ", ".join(f"η = {e:.4f}: {f(law(v, 'kr_density')[e] / rv(e, 'kr_density'), 2)} and "
                             f"{f(law(v, 'kr_jacobian')[e] / rv(e, 'kr_jacobian'), 2)}" for e in etas) for v in order) + ".")
    # checks of the measurement, for the reference and for G1
    worst_pred, worst_eps = 0.0, 0.0
    for e in etas:
        worst_pred = max(worst_pred, abs(rv(e, "kr_predicted") / rv(e, "null_count_mean") - 1),
                         abs(law(g1, "kr_predicted")[e] / law(g1, "null_count")[e] - 1))
        for tag in ("_eps005", "_eps02"):
            for k in ("kr_density", "kr_jacobian"):
                worst_eps = max(worst_eps, abs(rv(e, k + tag) / rv(e, k) - 1), abs(law(g1, k + tag)[e] / law(g1, k)[e] - 1))
    ok = worst_pred <= 0.2 and worst_eps <= 0.2
    detail = []                                                # per η and per law (review of the encadrant role, 2026-11-13)
    for e in etas:
        for who, get in (("reference", lambda k, e=e: rv(e, k)), (g1, lambda k, e=e: law(g1, k)[e])):
            eps = max(abs(get(k + tag) / get(k) - 1) for tag in ("_eps005", "_eps02") for k in ("kr_density", "kr_jacobian"))
            cnt = get("null_count_mean") if who == "reference" else law(g1, "null_count")[e]
            detail.append(f"η = {e:.4f}, {who}: threshold {f(eps, 2)}, count {f(abs(get('kr_predicted') / cnt - 1), 2)}")
    out.append("H32, the two checks per η and per law (largest relative change of a factor between the thresholds; relative gap of the "
               "predicted to the counted number): " + "; ".join(detail) + ".")
    sems = [float(np.std(a, ddof=1) / np.sqrt(len(a)) / np.mean(a)) for k in ("kr_density", "kr_jacobian", "kr_jacobian_all")
            for a in _per_seed(runs, g1, k).values() if len(a) > 1]
    if sems:
        out.append(f"H32, relative standard error over the seeds of the factors of {g1}, not included in the errors below (as registered): "
                   f"{f(min(sems), 2)} to {f(max(sems), 2)}.")
    out.append(f"H32, checks of the measurement (reference and {g1}, held-out η): largest relative gap between the predicted and the counted "
               f"number of null points {f(worst_pred)} (limit 0.2); largest relative change of a factor between the thresholds 0.05 or 0.2 "
               f"and 0.1: {f(worst_eps)} (limit 0.2): {'PASS' if ok else 'FAIL'}.")
    def ratio(key: str) -> dict[float, tuple[float, float]]:
        """G1 over the reference, with the standard error that the jackknife of the reference gives it."""
        g = law(g1, key)
        return {e: (g[e] / rv(e, key), g[e] / rv(e, key) * ref["values"][f"{e:.5f}"].get(key + "_se", float("nan")) / rv(e, key)) for e in etas}

    full = "kr_jacobian_all" in next(iter(ref["values"].values())) and "kr_jacobian_all" in next(
        x for r in runs.values() for x in r["evaluation"][g1]["test"])
    rj, rd = ratio("kr_jacobian"), ratio("kr_density")
    ra = ratio("kr_jacobian_all") if full else {e: (float("nan"), float("nan")) for e in etas}
    bad = [e for e in etas if rj[e][0] < 1.5 or rd[e][0] > 1.25 or ra[e][0] >= 1.25]
    sure = full and all(rj[e][0] - 2 * rj[e][1] >= 1.5 and rd[e][0] + 2 * rd[e][1] <= 1.25 and ra[e][0] + 2 * ra[e][1] < 1.25 for e in etas)
    pm = lambda t: f"{f(t[0], 3)} ± {f(t[1], 2)}"                                         # noqa: E731
    tr = law(g1, "kr_jacobian", "train")
    out.append(f"H32, {g1} over the reference (± the jackknife error of the reference over its trajectories): Jacobian where B is weak "
               + ", ".join(pm(rj[e]) for e in etas) + " (at least 1.5 each); density at zero " + ", ".join(pm(rd[e]) for e in etas)
               + " (at most 1.25 each); Jacobian over all the cells " + ", ".join(pm(ra[e]) for e in etas) + " (below 1.25 each)"
               + ("; at the training η, density and Jacobian where B is weak: " + ", ".join(
                   f"η = {e:.4f}: {f(law(g1, 'kr_density', 'train')[e] / rv(e, 'kr_density'), 2)} and {f(tr[e] / rv(e, 'kr_jacobian'), 2)}"
                   for e in tr) if tr else "")
               + ". Verdict on this realisation of the data: " + (
                   "MEASUREMENT INVALID (checks)" if not ok else
                   "NOT AVAILABLE (this run was made before the amended criterion: no Jacobian over all the cells, no error of the reference)"
                   if not full else
                   ("REFUTED (η = " + ", ".join(f"{e:.4f}" for e in bad) + ")" if bad else
                    ("SUPPORTED (each ratio beyond its threshold by two standard errors)" if sure else "INCONCLUSIVE (within two standard errors of a threshold)"))) + ".")
    return out


H25_VALUES = {0: (-0.006, -0.082, -0.118), 100: (-0.012, -0.085, -0.113)}      # third-order part of W9 at the held-out η, by data seed offset


def h33_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H33: the model with the affine term trained on Gaussian surrogate data against the same model trained on the data;
    verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    wz, wb = "W9Z_skip_sym_gaussdata", "W9Zb_skip_sym"
    if ref is None or wz not in have or wb not in have:
        return []
    out: list[str] = []

    def cells(v: str, key: str, split: str = "test") -> dict[float, np.ndarray]:
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get(split, []):
                if key in x:
                    acc.setdefault(round(x["eta"], 5), []).append(x[key])
        return {e: np.asarray(a) for e, a in sorted(acc.items(), reverse=True)}

    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    etas = sorted(cells(wz, "prod_fluct_over_d"), reverse=True)
    low = sorted(etas)[:2]
    tr = sorted(cells(wz, "prod_fluct_over_d", "train"), reverse=True)
    out.append("\nH33: the model with the affine term trained on the data (W9Zb) and on Gaussian surrogate data with the first two moments "
               "of the data (W9Z: draws of G1, as many as there are snapshots); seed means ± SE.\n")
    out.append("| quantity | " + " | ".join(f"η = {e:.4f}: on the data | on Gaussian data" for e in etas) + " |")
    out.append("|---|" + "---|---|" * len(etas))
    sem = lambda a: float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")   # noqa: E731
    pm = lambda a: f"{f(float(a.mean()))} ± {f(sem(a))}"                                 # noqa: E731
    rows = [("third-order part of the production / D (reference: " + ", ".join(f(rv(e, "prod_fluct_over_d")) for e in etas) + ")", "prod_fluct_over_d", None),
            ("mean-flow part / D (reference: " + ", ".join(f(rv(e, "prod_mean_over_d")) for e in etas) + ")", "prod_mean_over_d", None),
            ("E_B over that of the reference − 1", "E_B", "E_B"), ("ED / floor", "ed_ratio", None),
            ("|magnetic balance|", "balance_residual_magnetic", "abs"), ("err. nulls", "null_count_err_rel", None),
            ("σ(dE/dt)/σ_ref", "std_residual_rel", None)]
    for label, key, how in rows:
        line = []
        for e in etas:
            for v in (wb, wz):
                a = cells(v, key).get(e)
                if a is None:
                    line.append("–")
                else:
                    a = a / rv(e, "E_B") - 1 if how == "E_B" else (np.abs(a) if how == "abs" else a)
                    line.append(pm(a))
        out.append(f"| {label} | " + " | ".join(line) + " |")
    tz, tb = cells(wz, "prod_fluct_over_d"), cells(wb, "prod_fluct_over_d")
    ratio = {e: float(tz[e].mean() / tb[e].mean()) for e in etas}
    per_seed_ratio = {e: tz[e] / tb[e] for e in etas}
    bad = [e for e in low if abs(ratio[e]) >= 0.3 or int((np.abs(per_seed_ratio[e]) >= 0.3).sum()) > 1]
    # checks of the measurement: the model trained on the data reproduces H25 and has the sign of the reference; the law of the
    # surrogate set (G1 of the job) and the surrogate set itself have no third-order part
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    h25 = H25_VALUES.get(offset)
    dev25 = max(abs(float(tb[e].mean()) - x) for e, x in zip(etas, h25, strict=True)) if h25 and len(etas) == 3 else float("nan")
    need = min(4, len(next(iter(tb.values()))))
    sign_ok = all(int((np.sign(tb[e]) == np.sign(rv(e, "prod_fluct_over_d"))).sum()) >= need for e in low)
    sur = [abs(x) for r in runs.values() for x in r["times"].get(wz, {}).get("surrogate_third_order", {}).values()]
    base_ok = bool(dev25 <= 0.02) and sign_ok and bool(sur) and max(sur) < 0.02
    n_sur = len({k for r in runs.values() for k in r["times"].get(wz, {}).get("surrogate_third_order", {})})
    n_train = len([k for k, x in ref["values"].items() if x.get("split") == "train"])
    out.append("H33, third-order part of the model trained on Gaussian data over that of the model trained on the data: " + "; ".join(
        f"η = {e:.4f}: {f(ratio[e], 2)} on the seed means, per seed {', '.join(f(float(x), 2) for x in per_seed_ratio[e])}" for e in etas)
        + ("; at the training η: " + "; ".join(
            f"η = {e:.4f}: {f(float(cells(wb, 'prod_fluct_over_d', 'train')[e].mean()))} on the data, "
            f"{f(float(cells(wz, 'prod_fluct_over_d', 'train')[e].mean()))} on Gaussian data (reference {f(rv(e, 'prod_fluct_over_d'))})" for e in tr) if tr else "")
        + f". Criterion at the two lower held-out η: ratio below 0.3 in absolute value on the seed means and in all seeds but one at most. "
          f"Third-order part of the model trained on the data at the held-out η (to compare with H25): "
          + ", ".join(f(float(tb[e].mean())) for e in etas)
          + f" (largest gap to the values of H25 for this realisation: {f(float(dev25))}, limit 0.02; sign of the reference at the "
            f"two lower η in at least {need} seeds: {'yes' if sign_ok else 'no'}). Third-order part computed on the surrogate training sets "
            f"themselves, largest absolute value over the seeds and the {n_sur} training η where it is computed (of the {n_train} of the "
            f"training set; the register says each): {f(max(sur)) if sur else 'not recorded'} (limit 0.02).")
    g1 = next((v for v in ("G1_gaussian_full", "G1T_gaussian_full") if v in have), None)
    t1 = max(abs(a.mean()) for a in cells(g1, "prod_fluct_over_d").values()) if g1 else float("nan")
    ok = base_ok and bool(t1 < 0.02)
    if g1:
        ed_z, ed_g, eb_z, eb_g = cells(wz, "ed_ratio"), cells(g1, "ed_ratio"), cells(wz, "E_B"), cells(g1, "E_B")
        if all(len(ed_z[e]) == len(ed_g[e]) for e in etas):
            out.append(f"H33, the model trained on Gaussian data against {g1}, the law of its training set (same seed, paired; both evaluated "
                       "against the reference): ED / floor " + "; ".join(
                           f"η = {e:.4f}: {f(float(ed_z[e].mean()), 3)} against {f(float(ed_g[e].mean()), 3)} (difference {pm(ed_z[e] - ed_g[e])}, "
                           f"positive in {int((ed_z[e] > ed_g[e]).sum())} of {len(ed_z[e])} seeds)" for e in etas)
                       + "; E_B over that of the reference − 1: " + "; ".join(
                           f"η = {e:.4f}: {f(float(eb_z[e].mean() / rv(e, 'E_B') - 1), 2)} against {f(float(eb_g[e].mean() / rv(e, 'E_B') - 1), 2)}"
                           for e in etas) + ".")
    out.append(f"H33, largest |third-order part| of {g1}, the law of the surrogate training set, on the held-out η: {f(float(t1))} (limit 0.02). "
               f"Flow-matching loss on a fixed sample of its own training set (fixed noise): model trained on the data "
               f"{f(float(np.mean([r['times'].get(wb, {}).get('fm_loss_train_sample', np.nan) for r in runs.values()])), 5)}, model trained on "
               f"the Gaussian data {f(float(np.mean([r['times'].get(wz, {}).get('fm_loss_train_sample', np.nan) for r in runs.values()])), 5)}. "
               f"Checks of the measurement: {'PASS' if ok else 'FAIL'}. Verdict on this realisation of the data: "
               + ("MEASUREMENT INVALID (checks)" if not ok else ("REFUTED (η = " + ", ".join(f"{e:.4f}" for e in bad) + ")" if bad else "NOT REFUTED")) + ".")
    return out


def h34_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H34: the model with the affine term trained on Gaussian trajectories (the time correlation of the data, nothing
    non-Gaussian) against the same model trained on the data; verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    wy, wb = "W9Y_skip_sym_gausstraj", "W9Yb_skip_sym"
    if ref is None or wy not in have or wb not in have:
        return []
    out: list[str] = []

    def cells(v: str, key: str, split: str = "test") -> dict[float, np.ndarray]:
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get(split, []):
                if key in x:
                    acc.setdefault(round(x["eta"], 5), []).append(x[key])
        return {e: np.asarray(a) for e, a in sorted(acc.items(), reverse=True)}

    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    sem = lambda a: float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")   # noqa: E731
    pm = lambda a: f"{f(float(a.mean()))} ± {f(sem(a))}"                                 # noqa: E731
    etas = sorted(cells(wy, "prod_fluct_over_d"), reverse=True)
    low = sorted(etas)[:2]
    out.append("\nH34: the model with the affine term trained on the data (W9Yb) and on Gaussian trajectories with the covariance and the "
               "lag-one autocorrelation of the data (W9Y); seed means ± SE.\n")
    out.append("| quantity | " + " | ".join(f"η = {e:.4f}: on the data | on Gaussian trajectories" for e in etas) + " |")
    out.append("|---|" + "---|---|" * len(etas))
    for label, key, how in (("third-order part of the production / D (reference: " + ", ".join(f(rv(e, "prod_fluct_over_d")) for e in etas) + ")", "prod_fluct_over_d", None),
                            ("mean-flow part / D (reference: " + ", ".join(f(rv(e, "prod_mean_over_d")) for e in etas) + ")", "prod_mean_over_d", None),
                            ("E_B over that of the reference − 1", "E_B", "E_B"), ("ED / floor", "ed_ratio", None),
                            ("|magnetic balance|", "balance_residual_magnetic", "abs"), ("err. nulls", "null_count_err_rel", None),
                            ("σ(dE/dt)/σ_ref", "std_residual_rel", None)):
        line = []
        for e in etas:
            for v in (wb, wy):
                a = cells(v, key).get(e)
                line.append("–" if a is None else pm(a / rv(e, "E_B") - 1 if how == "E_B" else (np.abs(a) if how == "abs" else a)))
        out.append(f"| {label} | " + " | ".join(line) + " |")
    ty, tb = cells(wy, "prod_fluct_over_d"), cells(wb, "prod_fluct_over_d")
    ratio = {e: float(ty[e].mean() / tb[e].mean()) for e in etas}
    per_seed_ratio = {e: ty[e] / tb[e] for e in etas}
    a_bad = [e for e in low if abs(ratio[e]) >= 0.3 or int((np.abs(per_seed_ratio[e]) >= 0.3).sum()) > 1]
    eby = {e: abs(float(cells(wy, "E_B")[e].mean()) / rv(e, "E_B") - 1) for e in etas}
    ebb = {e: abs(float(cells(wb, "E_B")[e].mean()) / rv(e, "E_B") - 1) for e in etas}
    b_bad = [e for e in etas if eby[e] > 0.5 * ebb[e]]
    # checks of the measurement
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    h25 = H25_VALUES.get(offset)
    dev25 = max(abs(float(tb[e].mean()) - x) for e, x in zip(etas, h25, strict=True)) if h25 and len(etas) == 3 else float("nan")
    need = min(4, len(next(iter(tb.values()))))
    sign_ok = all(int((np.sign(tb[e]) == np.sign(rv(e, "prod_fluct_over_d"))).sum()) >= need for e in low)
    sur = [abs(x) for r in runs.values() for x in r["times"].get(wy, {}).get("surrogate_third_order", {}).values()]
    rho = [v for r in runs.values() for v in r["times"].get(wy, {}).get("autocorrelation", {}).values()]
    drho = max((abs(v["rho_surrogate_weighted"] - v["rho_data_weighted"]) for v in rho), default=float("nan"))
    g1 = next((v for v in ("G1_gaussian_full", "G1T_gaussian_full") if v in have), None)
    t1 = max(abs(a.mean()) for a in cells(g1, "prod_fluct_over_d").values()) if g1 else float("nan")
    ok = bool(dev25 <= 0.02) and sign_ok and bool(sur) and max(sur) < 0.02 and bool(drho <= 0.03) and bool(t1 < 0.02)
    out.append("H34, clause a, third-order part of the model trained on Gaussian trajectories over that of the model trained on the data: "
               + "; ".join(f"η = {e:.4f}: {f(ratio[e], 2)} on the seed means, per seed {', '.join(f(float(x), 2) for x in per_seed_ratio[e])}" for e in etas)
               + f" (below 0.3 in absolute value at the two lower η, on the seed means and in all seeds but one at most): {'FAIL' if a_bad else 'pass'}. "
               "Clause b, |E_B/E_B,ref − 1| of the model trained on Gaussian trajectories and of the model trained on the data: "
               + "; ".join(f"η = {e:.4f}: {f(eby[e])} and {f(ebb[e])}" for e in etas) + f" (at most half, at each η): {'FAIL' if b_bad else 'pass'}.")
    out.append(f"H34, checks of the measurement: largest gap of the base to the values of H25 {f(float(dev25))} (limit 0.02), sign of the reference at the two "
               f"lower η in at least {need} seeds: {'yes' if sign_ok else 'no'}; largest |third-order part| of {g1} {f(float(t1))} and of the surrogate "
               f"training sets {f(max(sur)) if sur else 'not recorded'} (limit 0.02 each); lag-one autocorrelation weighted by the variance of the "
               f"directions, data and surrogate: " + "; ".join(sorted({f"{v['rho_data_weighted']:.3f} and {v['rho_surrogate_weighted']:.3f}" for v in rho}))[:400]
               + f" (largest gap {f(float(drho))}, limit 0.03): {'PASS' if ok else 'FAIL'}. Flow-matching loss on a fixed sample of its own training "
               f"set: model trained on the data {f(float(np.mean([r['times'].get(wb, {}).get('fm_loss_train_sample', np.nan) for r in runs.values()])), 5)}, "
               f"on Gaussian trajectories {f(float(np.mean([r['times'].get(wy, {}).get('fm_loss_train_sample', np.nan) for r in runs.values()])), 5)}. "
               "Verdict on this realisation of the data: " + ("MEASUREMENT INVALID (checks)" if not ok else (
                   "REFUTED (clause " + " and ".join(c for c, x in (("a", a_bad), ("b", b_bad)) if x) + ")" if a_bad or b_bad else "NOT REFUTED")) + ".")
    return out


H35_KEYS = (("null-count error", "null_count_err_rel", True, 0.2), ("energy residual", "balance_residual_total", True, 0.05),
            ("spectrum + helicity", ("spec_err_b_l2", "hel_m_err_rel"), True, 0.15), ("ED / floor", "ed_ratio", False, 10.0),
            ("restart drift", "restart_drift_eb", True, 0.05))


def refnulls(offset: int | None) -> dict | None:
    """Null count of the reference on all its snapshots (e4_refnulls.py), for the realisation of a seed offset; None if absent."""
    # computed on the pods, on the data of each realisation: the data files of the session's own CPU are another realisation
    places = {0: [R / "replications" / "e4_recsur_a" / "e4_refnulls.json"],
              100: [R / "replications" / "e4_recsur_indep_a" / "e4_refnulls.json"]}.get(offset, [])
    for p in places:
        if p.exists():
            return json.loads(p.read_text())["values"]
    return None


def h35_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H35: G0, G1, W9 and W16 followed by a short relaxation in the solver; verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    if ref is None or "W16X_tau0" not in have:
        return []
    out: list[str] = []
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731

    def taus_of(law: str) -> list[float]:
        return sorted(float(v.rsplit("_tau", 1)[1]) for v in have if v.startswith(law + "_tau"))

    def name(law: str, t: float) -> str:
        return f"{law}_tau{t:g}"

    def seed_mean(v: str, key, absolute: bool) -> float:
        """As the objectives: mean over the held-out η for each seed, then mean over the seeds."""
        keys = key if isinstance(key, tuple) else (key,)
        return float(np.nanmean(sum(per_seed(runs, v, k, absolute=absolute) for k in keys)))

    def eb_dev(v: str) -> dict[float, float]:
        return {e: float(np.mean(a)) / rv(e, "E_B") - 1 for e, a in sorted(_per_seed(runs, v, "E_B").items(), reverse=True)}

    def null_err(v: str) -> dict[float, float]:
        return {e: float(np.mean(np.abs(a))) for e, a in sorted(_per_seed(runs, v, "null_count_err_rel").items(), reverse=True)}

    laws = [law for law in ("G0X", "G1X", "W9X", "W16X") if name(law, 0) in have]
    grid = taus_of("W16X")
    out.append("\nH35: laws followed by a relaxation of duration τ in the solver (seed means; errors as in the objectives, means over the "
               "held-out η; E_B: largest |E_B/E_B,ref − 1| over the held-out η; |det ∇B|: mean over all the cells over that of the reference, "
               "mean over the held-out η).\n")
    out.append("| law | τ | null-count error | mean \\|E_B/ref − 1\\| | largest \\|E_B/ref − 1\\| | energy residual | spectrum + helicity | ED / floor | "
               "\\|det ∇B\\| / ref | restart drift |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    stats: dict = {}
    for law in laws + (["REFX"] if name("REFX", 0) in have else []):
        for t in taus_of(law):
            v = name(law, t)
            eb = eb_dev(v)
            jac = _per_seed(runs, v, "kr_jacobian_all")
            jr = float(np.mean([np.mean(a) / rv(e, "kr_jacobian_all") for e, a in jac.items()])) if jac and "kr_jacobian_all" in next(
                iter(ref["values"].values())) else float("nan")
            st = {"null": seed_mean(v, "null_count_err_rel", True), "eb_mean": float(np.mean([abs(x) for x in eb.values()])),
                  "eb_max": max(abs(x) for x in eb.values()), "res": seed_mean(v, "balance_residual_total", True),
                  "spec": seed_mean(v, ("spec_err_b_l2", "hel_m_err_rel"), True), "ed": seed_mean(v, "ed_ratio", False), "jac": jr,
                  "drift": seed_mean(v, "restart_drift_eb", True)}
            stats[(law, t)] = st
            out.append(f"| {law} | {t:g} | {f(st['null'])} | {f(st['eb_mean'])} | {f(st['eb_max'])} | {f(st['res'])} | {f(st['spec'])} | "
                       f"{f(st['ed'])} | {f(st['jac'])} | {'–' if np.isnan(st['drift']) else f(st['drift'])} |")

    def tau_star(law: str) -> float:
        for t in taus_of(law):
            if stats[(law, t)]["null"] <= 0.2 and stats[(law, t)]["eb_mean"] <= 0.05:
                return t
        return float("inf")

    star = {law: tau_star(law) for law in laws}

    def why(law: str) -> str:
        """Which condition holds a law back at the last τ before its τ* (or at the last τ of the grid)."""
        ts = taus_of(law)
        before = [t for t in ts if t < star[law]]
        if not before:
            return "both conditions met at τ = 0"
        st = stats[(law, before[-1])]
        held = [n for n, bad in (("null count", st["null"] > 0.2), ("E_B", st["eb_mean"] > 0.05)) if bad]
        return f"at τ = {before[-1]:g} held back by " + " and ".join(held)

    def star_per_seed(law: str) -> list[str]:
        res = []
        for r in runs.values():
            got = "none"
            for t in taus_of(law):
                rows = r["evaluation"].get(name(law, t), {}).get("test", [])
                if rows and np.mean([abs(x["null_count_err_rel"]) for x in rows]) <= 0.2 and \
                        np.mean([abs(x["E_B"] / rv(x["eta"], "E_B") - 1) for x in rows]) <= 0.05:
                    got = f"{t:g}"
                    break
            res.append(got)
        return res

    want = [name(law, t) for law in ("G0X", "G1X", "W9X", "W16X") for t in (0, 1, 2, 4, 8)] + [name("REFX", t) for t in (0, 1, 4)]
    complete = set(runs) >= set(range(5)) and all(v in r["evaluation"] for r in runs.values() for v in want)
    fs = lambda t: "none on the grid" if np.isinf(t) else f"{t:g}"                         # noqa: E731
    # clause (a): the null-count error at τ = 1 against τ = 0, at each held-out η
    bad_a, parts = [], []
    for law in ("G1X", "W16X"):
        if name(law, 1) in have:
            n0, n1 = null_err(name(law, 0)), null_err(name(law, 1))
            parts.append(f"{law}: " + ", ".join(f"η = {e:.4f}: {f(n1[e])} against {f(n0[e])} (ratio {f(n1[e] / n0[e], 2)})" for e in n0))
            bad_a += [f"{law} at η = {e:.4f}" for e in n0 if n1[e] > 0.6 * n0[e]]
    full = name("W16X", 4) in have and name("G1X", 1) in have
    # clause (b): the five thresholds for W16X relaxed by 4 time units
    bad_b = []
    if full:
        v = name("W16X", 4)
        for label, key, absolute, limit in H35_KEYS:
            x = seed_mean(v, key, absolute)
            if not x <= limit:
                bad_b.append(f"{label} {f(x)} > {limit:g}")
    bad_c = not star.get("W16X", np.inf) < star.get("G1X", np.inf)
    out.append("H35 (a), null-count error at τ = 1 against τ = 0, at each held-out η (criterion: at most 0.6 of it): " + "; ".join(parts) + ".")
    out.append("H35 (b), W16X relaxed by 4 time units against the thresholds of the objectives (C5 0.2, C3 0.05, C4 0.15, C1 10, T1 0.05): "
               + ("not available in this run" if not full else ", ".join(
                   f"{label} {f(seed_mean(name('W16X', 4), key, absolute))}" for label, key, absolute, _ in H35_KEYS)) + ".")
    out.append("H35 (c), residual relaxation time τ* (first τ of the grid " + ", ".join(f"{t:g}" for t in grid) + " with a null-count error of "
               "at most 0.2 and a mean |E_B/E_B,ref − 1| of at most 0.05): " + ", ".join(
                   f"{law} {fs(star[law])} ({why(law)}; per seed: {', '.join(star_per_seed(law))})" for law in laws)
               + ("; τ* of W16 and of G1 are equal: not resolved by the grid" if star.get("W16X") == star.get("G1X") else "") + ".")
    # checks of the measurement
    chk, ok = [], True
    for t in taus_of("REFX"):
        v = name("REFX", t)
        ne, eb = max(null_err(v).values()), max(abs(x) for x in eb_dev(v).values())
        ok &= ne <= 0.1 and eb <= 0.03
        chk.append(f"reference snapshots relaxed by τ = {t:g}: largest null-count error {f(ne)} (limit 0.1), largest |E_B/ref − 1| {f(eb)} (limit 0.03)")
    if not taus_of("REFX"):
        ok = False
        chk.append("no control on reference snapshots in this run")
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    other_root = R / "replications" / {0: "e4_recolour", 100: "e4_recolour_indep"}.get(offset, "none")
    other = load(False, other_root) if (other_root / "e4_reference.json").exists() and full else {}
    same = other and set(other) >= set(runs) and all("W16_recoloured_full" in other[k]["evaluation"] for k in runs)
    if same:
        other = {k: other[k] for k in runs}                # the same seeds on both sides
        d_ed = seed_mean(name("W16X", 0), "ed_ratio", False) - float(np.nanmean(per_seed(other, "W16_recoloured_full", "ed_ratio")))
        d_nu = seed_mean(name("W16X", 0), "null_count_err_rel", True) - float(np.nanmean(per_seed(other, "W16_recoloured_full", "null_count_err_rel", absolute=True)))
        d_g1 = seed_mean(name("G1X", 0), "null_count_err_rel", True) - float(np.nanmean(per_seed(other, "G1_gaussian_full", "null_count_err_rel", absolute=True)))
        ok &= abs(d_ed) <= 0.5 and abs(d_nu) <= 0.1 and abs(d_g1) <= 0.05
        chk.append(f"against the job of H29 on the same data ({other_root.name}): W16 at τ = 0, ED / floor {f(d_ed)} (limit 0.5) and null-count "
                   f"error {f(d_nu)} (limit 0.1); G1 at τ = 0, null-count error {f(d_g1)} (limit 0.05"
                   + ("; zero by construction: same draws of G1 and same reference statistics" if d_g1 == 0 else "") + ")")
    else:
        ok = False
        chk.append("the job of H29 on the same data is not available with the same seeds: checks (2) and (3) not computed")
    full_ref = refnulls(offset)
    if full_ref and full:                                   # asked by the jury-externe role (2026-11-13): reported, not the criterion
        def err_full(v: str) -> dict[float, float]:
            return {e: abs(float(np.mean(a)) / full_ref[f"{e:.5f}"]["null_count_mean"] - 1)
                    for e, a in sorted(_per_seed(runs, v, "null_count").items(), reverse=True)}
        ratios = {law: {e: err_full(name(law, 1))[e] / err_full(name(law, 0))[e] for e in err_full(name(law, 0))} for law in ("G1X", "W16X")}
        mean_err = {law: {t: float(np.mean(list(err_full(name(law, t)).values()))) for t in taus_of(law)} for law in laws}
        star_full = {law: next((t for t in taus_of(law) if mean_err[law][t] <= 0.2 and stats[(law, t)]["eb_mean"] <= 0.05), float("inf"))
                     for law in laws}
        out.append("H35, the same quantities with the null count of the reference taken on all its snapshots (e4_refnulls.py: "
                   + ", ".join(f"η = {float(e):.4f}: {f(v['null_count_mean'])} ± {f(v['null_count_se_traj'])}" for e, v in full_ref.items()
                               if v["split"] == "test")
                   + "; standard error over the trajectories), reported beside the registered criterion: (a) ratio at τ = 1 over τ = 0: "
                   + "; ".join(f"{law}: " + ", ".join(f(x, 2) for x in ratios[law].values()) for law in ratios)
                   + "; (b) null-count error of the laws relaxed by 4 time units: "
                   + ", ".join(f"{law} {f(mean_err[law][4.0])}" for law in laws if 4.0 in mean_err[law])
                   + "; at τ = 0: " + ", ".join(f"{law} {f(mean_err[law][0.0])}" for law in laws)
                   + "; (c) τ*: " + ", ".join(f"{law} {fs(star_full[law])}" for law in laws) + ".")
    out.append("H35, checks of the measurement: " + "; ".join(chk) + f": {'PASS' if ok else 'FAIL'}. Verdict on this realisation of the data: "
               + ("INCOMPLETE (the seeds 0 to 4 do not all hold every law at every τ: no verdict)" if not complete else
                  "MEASUREMENT INVALID (checks)" if not ok else
                  ("NOT REFUTED" if not (bad_a or bad_b or bad_c) else "REFUTED on " + "; ".join(
                      ([f"(a): {', '.join(bad_a)}"] if bad_a else []) + ([f"(b): {', '.join(bad_b)}"] if bad_b else [])
                      + (["(c): τ* of W16 is not smaller than that of G1"] if bad_c else [])))) + ".")
    return out


def h36_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H36: W9 trained on the same number of snapshots from four times the trajectories; verdict as registered."""
    data_file = root / "e4_data.json"
    cfg = json.loads(data_file.read_text())["config"] if data_file.exists() else {}
    if ref is None or cfg.get("n_traj", 24) == 24 or not any("W9_skip_sym" in r["evaluation"] for r in runs.values()):
        return []
    main_root = R / "replications" / "e4_nongauss"            # G0, W9 and G1 on the data of the main run, with the production split
    main = json.loads((main_root / "e4_reference.json").read_text())["values"]
    main_runs = load(False, main_root)
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    out = [f"\nH36: the same number of snapshots from more trajectories ({cfg.get('n_traj')} trajectories, kept duration {cfg.get('t_keep'):g}, "
           f"{next(iter(ref['values'].values()))['n']} snapshots per η, seed offset {cfg.get('data_seed_offset')}); seed means, "
           "with the values of the run e4_nongauss on the data of the main run (24 trajectories of 100 snapshots) in brackets.\n"]

    def cell(rs: dict, rf, v: str, fn) -> dict[float, np.ndarray]:
        acc: dict = {}
        for r in rs.values():
            for x in r["evaluation"].get(v, {}).get("test", []):
                try:
                    acc.setdefault(round(x["eta"], 5), []).append(fn(x, rf[f"{x['eta']:.5f}"]))
                except KeyError:
                    pass
        return {e: np.asarray(a) for e, a in sorted(acc.items(), reverse=True)}

    sem = lambda a: float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")   # noqa: E731
    rows = (("E_B over that of the reference − 1", lambda x, r: x["E_B"] / r["E_B"] - 1), ("ED / floor", lambda x, r: x["ed_ratio"]),
            ("mean-flow part of the production − reference", lambda x, r: x["prod_mean_over_d"] - r["prod_mean_over_d"]),
            ("third-order part / reference", lambda x, r: x["prod_fluct_over_d"] / r["prod_fluct_over_d"]),
            ("null-count error", lambda x, r: abs(x["null_count_err_rel"])), ("restart drift", lambda x, r: abs(x.get("restart_drift_eb", np.nan))))
    laws = [v for v in ("G0_gaussian_modes", "G1_gaussian_full", "W9_skip_sym") if any(v in r["evaluation"] for r in runs.values())]
    etas = sorted(cell(runs, ref["values"], "W9_skip_sym", rows[0][1]), reverse=True)
    out.append("| law | quantity | " + " | ".join(f"η = {e:.4f}" for e in etas) + " |")
    out.append("|---|---|" + "---|" * len(etas))
    for v in laws:
        for label, fn in rows:
            new, old = cell(runs, ref["values"], v, fn), cell(main_runs, main, v, fn)
            out.append(f"| {v} | {label} | " + " | ".join(
                f"{f(float(new[e].mean()))} ± {f(sem(new[e]))} [{f(float(old[e].mean())) if e in old else '–'}]" for e in etas) + " |")
    dev = cell(runs, ref["values"], "W9_skip_sym", rows[0][1])
    n_seed = min(len(a) for a in dev.values())
    deficit = {e: float(-dev[e].mean()) for e in etas}
    # checks: same stationary law as the main run; G1 of the new data has the energy of its reference
    d_eb = max(abs(rv(e, "E_B") / main[f"{e:.5f}"]["E_B"] - 1) for e in (float(k) for k in ref["values"]))
    d_eb_test = max(abs(rv(e, "E_B") / main[f"{e:.5f}"]["E_B"] - 1) for e in etas)
    d_3 = max(abs(rv(e, "prod_fluct_over_d") - main[f"{e:.5f}"]["prod_fluct_over_d"]) for e in (float(k) for k in ref["values"]))
    g1 = cell(runs, ref["values"], "G1_gaussian_full", rows[0][1])
    d_g1 = max(abs(float(a.mean())) for a in g1.values()) if g1 else float("nan")
    # check (1) as registered for the first cycle (seed offset 200): the eleven η; as amended on 2026-11-13 for the second cycle
    # (other seed offsets): the held-out η, where the criterion is read (see the amendments of H36 in the register)
    first_cycle = cfg.get("data_seed_offset") == 200
    ok = (d_eb if first_cycle else d_eb_test) <= 0.05 and d_3 <= 0.05 and d_g1 <= 0.05
    verdict = ("INCOMPLETE (fewer than five seeds)" if n_seed < 5 else "MEASUREMENT INVALID (checks)" if not ok else
               "REFUTED (the deficit is at most 0.06 at each held-out η)" if all(abs(x) <= 0.06 for x in deficit.values()) else
               "SUPPORTED (the deficit is at least 0.09 at each held-out η)" if all(x >= 0.09 for x in deficit.values()) else "INCONCLUSIVE")
    out.append("H36, deficit of magnetic energy of W9_skip_sym trained on this data set, at the held-out η: "
               + ", ".join(f"η = {e:.4f}: {f(deficit[e])} ± {f(sem(dev[e]))}" for e in etas)
               + f" ({n_seed} seeds, ± the standard error over the training seeds only; refuted if at most 0.06 at each η, supported if at "
                 f"least 0.09 at each η). Checks of the measurement: "
                 f"reference of this data set against that of the main run, largest relative gap of E_B over the eleven η {f(d_eb)} "
                 f"({'limit 0.05' if first_cycle else 'reported'}) and over the held-out η {f(d_eb_test)} "
                 f"({'reported' if first_cycle else 'limit 0.05, check as amended for the second cycle'}), "
                 f"largest gap of the third-order part {f(d_3)} (limit 0.05); largest |E_B/E_B,ref − 1| of G1 at the held-out η {f(d_g1)} "
                 f"(limit 0.05): {'PASS' if ok else 'FAIL'}. Verdict: {verdict}.")
    return out


def h37_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H37: the model trained on Gaussian surrogates and recoloured like W16; oracle on reference snapshots; as registered."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    w16, w17, g1 = "W16V_recoloured_full", "W17_recoloured_surrogate", "G1V_gaussian_full"
    if ref is None or w17 not in have or w16 not in have:
        return []
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    sem = lambda a: float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")   # noqa: E731

    def seedwise(rs: dict, v: str, fn) -> np.ndarray:
        """Mean over the held-out η of ``fn(row)`` for each seed."""
        return np.array([np.mean([fn(x) for x in r["evaluation"][v]["test"]]) for r in rs.values() if v in r["evaluation"]])

    def per_eta(v: str, fn) -> dict[float, float]:
        acc: dict = {}
        for r in runs.values():
            for x in r["evaluation"].get(v, {}).get("test", []):
                acc.setdefault(round(x["eta"], 5), []).append(fn(x))
        return {e: float(np.mean(a)) for e, a in sorted(acc.items(), reverse=True)}

    exc = lambda x: max(0.0, max(x["restart_anchor"]["eb"][1:]))                         # noqa: E731
    quantities = (("ED / floor", lambda x: x["ed_ratio"]), ("excursion of E_B", exc), ("restart drift", lambda x: abs(x["restart_drift_eb"])),
                  ("null-count error", lambda x: abs(x["null_count_err_rel"])), ("|magnetic balance|", lambda x: abs(x["balance_residual_magnetic"])),
                  ("largest |E_B/ref − 1|", None), ("third-order part / reference at the two lower η", None))
    out = ["\nH37: the model with the affine term trained on the data (W16V) and on Gaussian surrogate data (W17), each recoloured onto the "
           "moments of G1 through its own map; G1 sampled exactly; reference snapshots without and with the map from the moments of all the "
           "snapshots of the η (REFV: its energy distance is not a distance to quote, its states are in the reference). Seed means ± SE "
           "over the held-out η; 512 restarted states.\n",
           "| law | " + " | ".join(q[0] for q in quantities) + " |", "|---|" + "---|" * len(quantities)]
    for v in (g1, w16, w17, "REFV_raw", "REFV_recoloured"):
        if v not in have:
            continue
        cells = []
        for label, fn in quantities:
            if fn is not None:
                a = seedwise(runs, v, fn)
                cells.append(f"{f(float(a.mean()))} ± {f(sem(a))}")
            elif label.startswith("largest"):
                cells.append(f(max(abs(x) for x in per_eta(v, lambda x: x["E_B"] / rv(x["eta"], "E_B") - 1).values())))
            else:
                t = per_eta(v, lambda x: x["prod_fluct_over_d"] / rv(x["eta"], "prod_fluct_over_d"))
                cells.append(", ".join(f(t[e], 2) for e in sorted(t)[:2][::-1]))
        out.append(f"| {v} | " + " | ".join(cells) + " |")
    n_seed = len(runs)
    complete = set(runs) >= set(range(5)) and all(v in r["evaluation"] for r in runs.values() for v in (w16, w17))
    data_cfg = root / "e4_data.json"
    full_ref = refnulls(json.loads(data_cfg.read_text())["config"].get("data_seed_offset", 0)) if data_cfg.exists() else None
    if full_ref:                                            # asked by the review of the encadrant role (2026-11-13)
        out.append("H37, null-count error against the count of the reference on all its snapshots (mean over the held-out η and the seeds; "
                   "the table above is against the 400 snapshots of the reference stage): " + ", ".join(
                       f"{v} {f(float(np.mean([abs(np.mean(a) / full_ref[f'{e:.5f}']['null_count_mean'] - 1) for e, a in _per_seed(runs, v, 'null_count').items()])))}"
                       for v in (g1, w16, w17, "REFV_raw", "REFV_recoloured") if v in have) + ".")
    d = seedwise(runs, w17, exc) - seedwise(runs, w16, exc)
    bad = not (d.mean() >= 0.02 and d.mean() > 2 * sem(d) and int((d > 0).sum()) >= min(4, n_seed))
    # checks of the measurement
    third = max(abs(x) for x in per_eta(w17, lambda x: x["prod_fluct_over_d"]).values())
    eb17 = max(abs(x) for x in per_eta(w17, lambda x: x["E_B"] / rv(x["eta"], "E_B") - 1).values())
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    other_root = R / "replications" / {0: "e4_recolour", 100: "e4_recolour_indep"}.get(offset, "none")
    other = load(False, other_root) if (other_root / "e4_reference.json").exists() else {}
    same = bool(other) and set(other) >= set(runs) and all("W16_recoloured_full" in other[k]["evaluation"] for k in runs)
    if same:
        other = {k: other[k] for k in runs}
        d_exc = float(seedwise(runs, w16, exc).mean() - seedwise(other, "W16_recoloured_full", exc).mean())
        d_ed = float(seedwise(runs, w16, lambda x: x["ed_ratio"]).mean() - seedwise(other, "W16_recoloured_full", lambda x: x["ed_ratio"]).mean())
    else:
        d_exc = d_ed = float("nan")
    ok = third < 0.02 and eb17 <= 0.05 and same and abs(d_exc) <= 0.02 and abs(d_ed) <= 0.5
    g = seedwise(runs, w17, exc) - seedwise(runs, g1, exc) if g1 in have else np.array([np.nan])
    out.append(f"H37, excursion of E_B above the reference, W17 minus W16, paired over the seeds (mean over the held-out η): "
               f"{', '.join(f(float(x)) for x in d)}; {f(float(d.mean()))} ± {f(sem(d))}, {int((d > 0).sum())} of {n_seed} seeds positive "
               f"(criterion: at least 0.02, more than 2 SE, at least {min(4, n_seed)} seeds). Reported: W17 minus G1 of the same job "
               f"{f(float(g.mean()))} ± {f(sem(g))}. Checks of the measurement: largest |third-order part| of W17 over the dissipation "
               f"{f(third)} (limit 0.02); largest |E_B/E_B,ref − 1| of W17 {f(eb17)} (limit 0.05); W16 of this job against W16 of the job of "
               f"H29 on the same data ({other_root.name}, same seeds): excursion {f(d_exc)} (limit 0.02), ED / floor {f(d_ed)} (limit 0.5): "
               f"{'PASS' if ok else 'FAIL'}. Verdict on this realisation of the data: "
               + ("INCOMPLETE (the seeds 0 to 4 do not all hold both laws: no verdict)" if not complete else
                  "MEASUREMENT INVALID (checks)" if not ok else ("REFUTED" if bad else "NOT REFUTED")) + ".")
    return out


def h38_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H38: positive control of the anchored model, trained on samples of W9; verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    base = "W9P_skip_sym"
    its = sorted(int(v.rsplit("_it", 1)[1]) for v in have if v.startswith("W18_anchor_on_W9_it"))
    if ref is None or base not in have or not its:
        return []
    last = its[-1]
    name = lambda k: f"W18_anchor_on_W9_it{k}"                                           # noqa: E731
    third = lambda v: _per_seed(runs, v, "prod_fluct_over_d")                             # noqa: E731
    etas = sorted(third(base), reverse=True)
    etas = [e for e in etas if e in third(name(last))]
    low = sorted(e for e in etas if ref["values"][f"{e:.5f}"]["split"] == "test")[:2]
    tb = third(base)
    out = ["\nH38: positive control of the anchored model (the construction of H28) trained on samples of W9: third-order part of the "
           "production over the dissipation, seed means; ratio to that of W9 of the same job (whose samples are the training set); "
           "flow-matching loss on a fixed sample of the training set.\n",
           "| model | " + " | ".join(f"η = {e:.4f}: third-order part | ratio to W9" for e in low) + " | loss |", "|---|" + "---|---|" * len(low) + "---|"]
    loss = lambda v: float(np.mean([r["times"].get(v, {}).get("fm_loss_train_sample", np.nan) for r in runs.values()]))   # noqa: E731
    for v in [base] + [name(k) for k in its] + (["W9PP_retrained_on_W9"] if "W9PP_retrained_on_W9" in have else []):
        t = third(v)
        out.append(f"| {v} | " + " | ".join(f"{f(float(np.mean(t[e])))} | {f(float(np.mean(t[e]) / np.mean(tb[e])), 2)}" for e in low)
                   + f" | {'–' if np.isnan(loss(v)) else f(loss(v), 5)} |")
    tl = third(name(last))
    ratio = {e: float(np.mean(tl[e]) / np.mean(tb[e])) for e in low}
    per_seed_ratio = {e: np.asarray(tl[e]) / np.asarray(tb[e]) for e in low}
    n_seed = min(len(tl[e]) for e in low)
    bad = [e for e in low if ratio[e] < 0.3 or int((per_seed_ratio[e] < 0.3).sum()) > 1]
    # checks of the measurement
    t0 = max(abs(float(np.mean(a))) for e, a in third(name(0)).items() if ref["values"][f"{e:.5f}"]["split"] == "test") if 0 in its else float("nan")
    sets = [r["times"].get(name(0), {}).get("training_set_third_order", {}) for r in runs.values()]
    tr = _per_seed(runs, base, "prod_fluct_over_d", "train")
    d_set = max(abs(float(np.mean([s[f"{e:.5f}"] for s in sets if f"{e:.5f}" in s])) - float(np.mean(tr[e]))) for e in tr) if tr and all(sets) else float("nan")
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    h25 = H25_VALUES.get(offset)
    test_etas = sorted((e for e in third(base) if ref["values"][f"{e:.5f}"]["split"] == "test"), reverse=True)
    d25 = max(abs(float(np.mean(tb[e])) - x) for e, x in zip(test_etas, h25, strict=True)) if h25 and len(test_etas) == 3 else float("nan")
    ok = t0 < 0.02 and d_set <= 0.02 and d25 <= 0.02
    out.append(f"H38, third-order part of the anchored model at iteration {last} over that of W9: "
               + "; ".join(f"η = {e:.4f}: {f(ratio[e], 2)} on the seed means, per seed {', '.join(f(float(x), 2) for x in per_seed_ratio[e])}" for e in low)
               + f" (criterion: at least 0.3 on the seed means and in all seeds but one at most, at each of the two lower held-out η). Checks of the "
                 f"measurement: largest |third-order part| at iteration 0 over the held-out η {f(t0)} (limit 0.02); largest gap between the "
                 f"third-order part of the training set and that of W9 generated at the same training η {f(d_set)} (limit 0.02); largest gap of "
                 f"W9 of this job to the values of H25 {f(d25)} (limit 0.02): {'PASS' if ok else 'FAIL'}. Verdict: "
               + ("INCOMPLETE (fewer than five seeds)" if n_seed < 5 else "MEASUREMENT INVALID (checks)" if not ok else
                  ("REFUTED (η = " + ", ".join(f"{e:.4f}" for e in bad) + ")" if bad else "NOT REFUTED"))
               + (" Inconclusive zone of the register (a ratio between 0.2 and 0.4): a second realisation is to be run." if any(0.2 <= ratio[e] <= 0.4 for e in low) else "") + ".")
    return out


def h39_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H39: ensembles of the solver from the initial condition of the data, read along the transient; as registered."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    taus = sorted(float(v.rsplit("_tau", 1)[1]) for v in have if v.startswith("COLD_tau"))
    if ref is None or not taus:
        return []
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    name = lambda t: f"COLD_tau{t:g}"                                                      # noqa: E731
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    full_ref = refnulls(offset)

    def seedwise(v: str, fn) -> np.ndarray:
        return np.array([np.mean([fn(x) for x in r["evaluation"][v]["test"]]) for r in runs.values() if v in r["evaluation"]])

    def eb_mean(v: str) -> float:                           # as in H35: |E_B/ref − 1| of the seed mean, mean over the held-out η
        return float(np.mean([abs(float(np.mean(a)) / rv(e, "E_B") - 1) for e, a in _per_seed(runs, v, "E_B").items()]))

    def null_full(v: str) -> float:
        return float(np.mean([abs(float(np.mean(a)) / full_ref[f"{e:.5f}"]["null_count_mean"] - 1) for e, a in _per_seed(runs, v, "null_count").items()]))

    out = ["\nH39: ensembles of the solver started from the initial condition of the data and read at τ (512 trajectories per η and per seed; "
           "seed means over the held-out η; errors as in H35).\n",
           "| τ | null-count error | the same against the count on all the snapshots | mean \\|E_B/ref − 1\\| | energy residual | spectrum + helicity | "
           "ED / floor | \\|det ∇B\\| / ref |", "|---|---|---|---|---|---|---|---|"]
    stats = {}
    for t in taus:
        v = name(t)
        jac = _per_seed(runs, v, "kr_jacobian_all")
        st = {"null": float(seedwise(v, lambda x: abs(x["null_count_err_rel"])).mean()), "eb": eb_mean(v),
              "res": float(seedwise(v, lambda x: abs(x["balance_residual_total"])).mean()),
              "spec": float(seedwise(v, lambda x: abs(x["spec_err_b_l2"]) + abs(x["hel_m_err_rel"])).mean()),
              "ed": float(seedwise(v, lambda x: x["ed_ratio"]).mean()),
              "jac": float(np.mean([np.mean(a) / rv(e, "kr_jacobian_all") for e, a in jac.items()])) if jac else float("nan"),
              "null_full": null_full(v) if full_ref else float("nan")}
        stats[t] = st
        out.append(f"| {t:g} | {f(st['null'])} | {f(st['null_full'])} | {f(st['eb'])} | {f(st['res'])} | {f(st['spec'])} | {f(st['ed'])} | {f(st['jac'])} |")
    star = next((t for t in taus if stats[t]["null"] <= 0.2 and stats[t]["eb"] <= 0.05), float("inf"))
    star_full = next((t for t in taus if stats[t]["null_full"] <= 0.2 and stats[t]["eb"] <= 0.05), float("inf")) if full_ref else float("nan")
    star_ed = next((t for t in taus if stats[t]["ed"] <= 10), float("inf"))
    per_seed = []
    for r in runs.values():
        got = "none"
        for t in taus:
            rows = r["evaluation"].get(name(t), {}).get("test", [])
            if rows and np.mean([abs(x["null_count_err_rel"]) for x in rows]) <= 0.2 and np.mean([abs(x["E_B"] / rv(x["eta"], "E_B") - 1) for x in rows]) <= 0.05:
                got = f"{t:g}"
                break
        per_seed.append(got)
    fs = lambda t: "none on the grid" if np.isinf(t) else f"{t:g}"                         # noqa: E731
    complete = set(runs) >= set(range(5)) and all(name(t) in r["evaluation"] for r in runs.values() for t in taus)
    last = taus[-1]
    ok = stats[last]["null"] <= 0.2 and stats[last]["eb"] <= 0.05
    out.append(f"H39, τ*_cold (first τ of the grid " + ", ".join(f"{t:g}" for t in taus) + " with a null-count error of at most 0.2 and a mean "
               f"|E_B/E_B,ref − 1| of at most 0.05): {fs(star)} (per seed: {', '.join(per_seed)}; against the reference count on all the "
               f"snapshots: {'not available' if not full_ref else fs(star_full)}); first τ with an energy distance below 10 floors: {fs(star_ed)}. "
               f"Criterion: refuted if τ*_cold is 16 or less. Check of the measurement: at τ = {last:g} the ensemble meets the two conditions "
               f"(null-count error {f(stats[last]['null'])}, mean |E_B/ref − 1| {f(stats[last]['eb'])}): {'PASS' if ok else 'FAIL'}. Verdict on this "
               "realisation of the data: " + ("INCOMPLETE (the seeds 0 to 4 do not all hold every τ: no verdict)" if not complete else
                                             "MEASUREMENT INVALID (check)" if not ok else ("REFUTED" if star <= 16 else "NOT REFUTED")) + ".")
    return out


def h40_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H40: the model anchored on a Gaussian law with a structured covariance; verdict as registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    its = sorted(int(v.rsplit("_it", 1)[1]) for v in have if v.startswith("W19_struct_anchor_it"))
    if ref is None or not its or "W9Q_skip_sym" not in have:
        return []
    last = its[-1]
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    third = lambda v: {e: np.asarray(a) for e, a in _per_seed(runs, v, "prod_fluct_over_d").items()}   # noqa: E731
    test = sorted((e for e in third(f"W19_struct_anchor_it{last}") if ref["values"][f"{e:.5f}"]["split"] == "test"), reverse=True)
    low = sorted(test)[:2]
    mean = lambda v, fn: float(np.mean([np.mean([fn(x) for x in r["evaluation"][v]["test"]]) for r in runs.values() if v in r["evaluation"]]))   # noqa: E731
    worst = lambda v, fn: max((float(np.mean([fn(x) for r in runs.values() for x in r["evaluation"].get(v, {}).get("test", []) if round(x["eta"], 5) == e]))   # noqa: E731
                               for e in test), key=abs)
    exc = lambda x: max(0.0, max(x["restart_anchor"]["eb"][1:])) if "restart_anchor" in x else float("nan")                       # noqa: E731
    loss = lambda v: float(np.mean([r["times"].get(v, {}).get("fm_loss_train_sample", np.nan) for r in runs.values()]))            # noqa: E731
    out = ["\nH40: flow matching anchored on a Gaussian law with a structured covariance (leading eigen-directions plus one block per "
           "mode), trained on the data (W19) and, as a positive control, on samples of W9 (W20); G5: the structured law sampled exactly. "
           "Seed means over the held-out η unless a column says otherwise.\n",
           "| model | third-order part / reference, two lower η | third-order part / that of W9, two lower η | mean-flow part − reference "
           "(largest) | E_B/ref − 1 (largest) | ED / floor | \\|magnetic balance\\| | null-count error | excursion | restart drift | loss |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    t9 = third("W9Q_skip_sym")
    names = ["G5_gaussian_struct", "W9Q_skip_sym"] + [f"W19_struct_anchor_it{k}" for k in its] + sorted(
        (v for v in have if v.startswith("W20_struct_anchor_on_W9_it")), key=lambda v: int(v.rsplit("_it", 1)[1]))
    for v in [n for n in names if n in have]:
        t = third(v)
        out.append(f"| {v} | " + ", ".join(f(float(t[e].mean() / rv(e, "prod_fluct_over_d")), 2) for e in low[::-1]) + " | "
                   + ", ".join(f(float(t[e].mean() / t9[e].mean()), 2) for e in low[::-1]) + " | "
                   + f"{f(worst(v, lambda x: x['prod_mean_over_d'] - rv(x['eta'], 'prod_mean_over_d')))} | "
                   + f"{f(worst(v, lambda x: x['E_B'] / rv(x['eta'], 'E_B') - 1))} | {f(mean(v, lambda x: x['ed_ratio']))} | "
                   + f"{f(mean(v, lambda x: abs(x['balance_residual_magnetic'])))} | {f(mean(v, lambda x: abs(x['null_count_err_rel'])))} | "
                   + f"{'–' if np.isnan(mean(v, exc)) else f(mean(v, exc))} | "
                   + f"{'–' if np.isnan(mean(v, lambda x: abs(x.get('restart_drift_eb', np.nan)))) else f(mean(v, lambda x: abs(x['restart_drift_eb'])))} | "
                   + f"{'–' if np.isnan(loss(v)) else f(loss(v), 5)} |")
    n_seed = len(runs)
    need = min(4, n_seed)
    # clause (a): the control against W9
    ctl = f"W20_struct_anchor_on_W9_it{last}"
    if ctl in have:
        tc = third(ctl)
        ra = {e: float(tc[e].mean() / t9[e].mean()) for e in low}
        ps = {e: tc[e] / t9[e] for e in low}
        bad_a = [e for e in low if ra[e] < 0.3 or int((ps[e] < 0.3).sum()) > 1]
        txt_a = ("(a) control, third-order part over that of W9: " + "; ".join(
            f"η = {e:.4f}: {f(ra[e], 2)} on the seed means, per seed {', '.join(f(float(x), 2) for x in ps[e])}" for e in low[::-1])
                 + (": pass" if not bad_a else ": FAIL"))
    else:
        bad_a, txt_a = ["absent"], "(a) control: not in this run"
    # clause (b): the model trained on the data against the reference
    tb = third(f"W19_struct_anchor_it{last}")
    rb = {e: float(tb[e].mean() / rv(e, "prod_fluct_over_d")) for e in low}
    sg = {e: int((np.sign(tb[e]) == np.sign(rv(e, "prod_fluct_over_d"))).sum()) for e in low}
    bad_b = [e for e in low if rb[e] < 0.3 or sg[e] < need]
    eb = {e: float(np.mean(_per_seed(runs, f"W19_struct_anchor_it{last}", "E_B")[e])) / rv(e, "E_B") - 1 for e in test}
    bad_c = [e for e in test if abs(eb[e]) > 0.05]
    # checks
    t0 = max(max(abs(float(a.mean())) for e, a in third(f"{tag}_it0").items() if e in test)
             for tag in ("W19_struct_anchor", "W20_struct_anchor_on_W9") if f"{tag}_it0" in have)
    g5 = max(abs(float(np.mean(a)) / rv(e, "E_B") - 1) for e, a in _per_seed(runs, "G5_gaussian_struct", "E_B").items() if e in test) \
        if "G5_gaussian_struct" in have else float("nan")
    data_file = root / "e4_data.json"
    offset = json.loads(data_file.read_text())["config"].get("data_seed_offset", 0) if data_file.exists() else None
    h25 = H25_VALUES.get(offset)
    d25 = max(abs(float(t9[e].mean()) - x) for e, x in zip(test, h25, strict=True)) if h25 and len(test) == 3 else float("nan")
    ok = t0 < 0.02 and g5 <= 0.05 and d25 <= 0.02
    complete = set(runs) >= set(range(5)) and all(f"W19_struct_anchor_it{last}" in r["evaluation"] for r in runs.values()) and last == 4000
    out.append(f"H40, iteration {last}: " + txt_a + ". (b) trained on the data, third-order part over that of the reference: " + "; ".join(
        f"η = {e:.4f}: {f(rb[e], 2)} ({sg[e]} of {n_seed} seeds with the sign of the reference)" for e in low[::-1])
        + (": pass" if not bad_b else ": FAIL") + ". (c) E_B over that of the reference − 1 at the held-out η: "
        + ", ".join(f(eb[e]) for e in test) + (" (limit 0.05 each): pass" if not bad_c else " (limit 0.05 each): FAIL")
        + f". Checks of the measurement: largest |third-order part| at iteration 0 {f(t0)} (limit 0.02); largest |E_B/E_B,ref − 1| of the "
          f"structured Gaussian law {f(g5)} (limit 0.05); largest gap of W9 of this job to the values of H25 {f(d25)} (limit 0.02): "
          f"{'PASS' if ok else 'FAIL'}. Verdict on this realisation of the data: "
        + ("INCOMPLETE (five seeds at iteration 4000 are needed: no verdict)" if not complete else "MEASUREMENT INVALID (checks)" if not ok else
           ("NOT REFUTED" if not (bad_a or bad_b or bad_c) else "REFUTED on " + ", ".join(
               c for c, bad in (("(a)", bad_a), ("(b)", bad_b), ("(c)", bad_c)) if bad))) + ".")
    return out


H41_W10 = (-0.012, -0.043, -0.064)        # third-order part of W10 at the held-out η in the run e4_nongauss (data of the main run)


def h41_lines(runs: dict, ref: dict | None, root: Path = R) -> list[str]:
    """H41: the anchored code path of H28/H38/H40 with an anchor of rank 0 against W10 (GaussianAnchoredField); a run with
    another rank and no W10 is reported without a verdict. As registered (research/hypotheses.json)."""
    have = {v for r in runs.values() for v in r["evaluation"]}
    its = sorted(int(v.rsplit("_it", 1)[1]) for v in have if v.startswith("W19_struct_anchor_it"))
    ranks = {r["times"].get(f"W19_struct_anchor_it{its[-1]}", {}).get("rank") for r in runs.values()} if its else set()
    if ref is None or not its or ranks == {300}:
        return []
    rank = next(iter(ranks)) if len(ranks) == 1 else None
    last = f"W19_struct_anchor_it{its[-1]}"
    third = lambda v: {e: np.asarray(a) for e, a in _per_seed(runs, v, "prod_fluct_over_d").items()}   # noqa: E731
    test = sorted((e for e in third(last) if ref["values"][f"{e:.5f}"]["split"] == "test"), reverse=True)
    low = sorted(test)[:2][::-1]
    rv = lambda e, k: ref["values"][f"{e:.5f}"][k]                                       # noqa: E731
    mean = lambda v, fn: float(np.mean([np.mean([fn(x) for x in r["evaluation"][v]["test"]]) for r in runs.values() if v in r["evaluation"]]))   # noqa: E731
    loss = lambda v: float(np.mean([r["times"].get(v, {}).get("fm_loss_train_sample", np.nan) for r in runs.values()]))            # noqa: E731
    t19 = third(last)
    out = [f"\nH41: the anchored code path of H28, H38 and H40 (FullGaussianAnchoredField) with an anchor of rank {rank}, iteration "
           f"{its[-1]}: third-order part over the dissipation at the held-out η " + ", ".join(f(float(t19[e].mean())) for e in test)
           + " (reference " + ", ".join(f(rv(e, "prod_fluct_over_d")) for e in test) + "); over that of the reference at the two lower η: "
           + ", ".join(f(float(t19[e].mean() / rv(e, "prod_fluct_over_d")), 2) for e in low)
           + f"; largest E_B/E_B,ref − 1 {f(max((float(np.mean(a)) / rv(e, 'E_B') - 1 for e, a in _per_seed(runs, last, 'E_B').items() if e in test), key=abs))}; "
             f"ED / floor {f(mean(last, lambda x: x['ed_ratio']))}; loss on a fixed training sample at iteration 0 and at the end: "
             f"{f(loss('W19_struct_anchor_it0'), 5)}, {f(loss(last), 5)}."]
    if "W10_anchored" not in have:
        out.append(f"H41, rank {rank}: reported measurement (no W10 in this job: no verdict).")
        return out
    t10 = third("W10_anchored")
    diff = {e: float(t19[e].mean() - t10[e].mean()) for e in test}
    bad = [e for e in low if abs(diff[e]) > 0.02]
    d10 = max(abs(float(t10[e].mean()) - x) for e, x in zip(test, H41_W10, strict=True)) if len(test) == 3 else float("nan")
    complete = set(runs) >= set(range(5)) and all(last in r["evaluation"] and "W10_anchored" in r["evaluation"] for r in runs.values()) \
        and its[-1] == 4000 and rank == 0
    out.append("H41, the same against W10 of this job (anchored on the mode-wise law through GaussianAnchoredField; same seeds): third-order "
               "part of W10 " + ", ".join(f(float(t10[e].mean())) for e in test) + "; difference " + ", ".join(f(diff[e]) for e in test)
               + f" (criterion: at most 0.02 in absolute value at the two lower η); E_B/E_B,ref − 1 of W10 "
               + f"{f(max((float(np.mean(a)) / rv(e, 'E_B') - 1 for e, a in _per_seed(runs, 'W10_anchored', 'E_B').items() if e in test), key=abs))}, "
               + f"ED / floor {f(mean('W10_anchored', lambda x: x['ed_ratio']))}. Check of the measurement: largest gap of W10 of this job to "
               + f"its values in the run e4_nongauss {f(d10)} (limit 0.02): {'PASS' if d10 <= 0.02 else 'FAIL'}. Verdict: "
               + ("INCOMPLETE (five seeds at iteration 4000 with rank 0 are needed: no verdict)" if not complete else
                  "MEASUREMENT INVALID (check)" if not d10 <= 0.02 else ("REFUTED (η = " + ", ".join(f"{e:.4f}" for e in bad) + ")" if bad else "NOT REFUTED")) + ".")
    return out


def select(runs: dict) -> dict:
    """Generator with the lowest validation energy-distance ratio (mean over the seeds)."""
    val = {v: float(np.nanmean(per_seed(runs, v, "ed_ratio", "val"))) for v in GENERATORS
           if not np.all(np.isnan(per_seed(runs, v, "ed_ratio", "val")))}
    best = min((v for v in val if v in CANDIDATES), key=val.get, default=None)     # None: a run without any candidate
    return {"variant": best, "criterion": "flow-matching or diffusion generator with the lowest energy-distance ratio on the "
            "validation η, mean over the seeds (the Gaussian laws G0, G1 and G2 are not candidates)",
            "seeds": sorted(runs), "val_ed_ratio": val}


def same_data_line(root: Path, c: dict) -> str | None:
    """Is the reference data of a job the realisation that its seed offset names? The solver is chaotic: a pod with another
    CPU type regenerates another realisation from the same seeds (found by the review of H34, 2026-11-13)."""
    base = {0: R / "e4_reference.json", 100: R / "replications" / "e4_indep" / "e4_reference.json"}.get(c.get("data_seed_offset", 0))
    mine = root / "e4_reference.json"
    if c.get("n_traj", 24) != 24 or base is None or not base.exists() or not mine.exists() or base == mine:
        return None
    a, b = json.loads(mine.read_text())["values"], json.loads(base.read_text())["values"]
    gap = max(abs(a[e]["E_B"] / b[e]["E_B"] - 1) for e in a if e in b)
    which = "main run" if c.get("data_seed_offset", 0) == 0 else "independent replication (e4_indep)"
    if gap < 1e-6:
        return f"Reference data: the realisation of the {which} (largest relative gap of E_B over the η: {f(gap)}).\n"
    return (f"Reference data: ANOTHER REALISATION than that of the {which}, although the seeds are the same (largest relative gap of E_B over "
            f"the η: {f(gap)}): the pod of this job has another CPU type and the chaotic solver diverged. Comparisons with jobs on the data of "
            f"the {which} are comparisons across realisations.\n")


def section(quick: bool = False, root: Path = R, replication: str | None = None, run_tag: str = "") -> list[str]:
    """E4 section of the digest; with ``replication``, the same tables for an independent replication
    stored under ``root`` or for a run with another protocol (``run_tag``, e.g. "_cs0.5"): no selection
    file is written, the title says what the replication is."""
    tag = "_quick" if quick else ""
    runs = load(quick, root, run_tag)
    out: list[str] = []
    P = lambda line: out.append(line) if line is not None else None            # noqa: E731
    dp, rp = root / f"e4_data{tag}.json", root / f"e4_reference{tag}.json"
    if not dp.exists():
        return out
    data = json.loads(dp.read_text())
    c = data["config"]
    if replication:
        P(f"## E4 - additional run: {replication}\n")
        P(same_data_line(root, c))
    else:
        P("## E4 - forced 3D MHD dynamo (ABC forcing at kf = 2), generation conditioned on η\n")
    P(f"Data (experiments/e4_data.py): N = {c['N']}, every mode |m_i| ≤ {c['kcut']} ({c['modes']} complex modes per field component pair), "
      f"ν = {c['nu']} (Re = {f(c['Re'])}), kf = {c['kf']}; training η {c['eta_train']}; validation η {c['eta_val']}; test η {c['eta_test']}; "
      f"{c['n_traj']} trajectories per η, transient {c['t_burn']}, kept {c['t_keep']}, one snapshot every {c['every']}; {c['dtype']}; "
      f"generation time {data['duration_s']:.0f} s on 4 cores.\n")
    ref = json.loads(rp.read_text()) if rp.exists() else None
    P("### Reference data per η\n")
    P("| η | Rm | set | E_u | E_B | H_M | energy residual (time mean) | H_M drift (SE) | nulls per snapshot | k_λ | ED floor |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for v in data["values"]:
        r = ref["values"].get(f"{v['eta']:.5f}", {}) if ref else {}
        P(f"| {v['eta']:.5f} | {f(v['Rm'])} | {v['split']} | {f(v['kinetic_energy']['mean'])} | {f(v['magnetic_energy']['mean'])} | "
          f"{f(v['magnetic_helicity']['mean'])} | {f(v['balance_residual_total'])} | {f(v['magnetic_helicity']['half_drift_se'], 2)} | "
          f"{f(r.get('null_count_mean'))} ± {f(r.get('null_count_se'), 2)} | {f(r.get('k_lambda'))} | {f(r.get('ed_floor_512'))} |")
    P("\nEnergy residual: (⟨injection⟩ − ⟨Dν + Dη⟩)/⟨Dν + Dη⟩ over the kept window and the trajectories (solver diagnostics). "
      "H_M drift: difference of the trajectory means between the two halves of the kept window, in units of its standard error. "
      "ED floor: energy distance between two reference subsamples of 512 snapshots from disjoint halves of the trajectories.\n")
    if ref:
        P("### Reference: magnetic helicity spectrum and stationarity identities (H11)\n")
        P("| η | H(k = 1) ± SE | Σ_{k ≥ 2} H(k) ± SE | E_B(1)/E_B | z of ⟨j·B⟩ | r_b | energy residual ± SE | magnetic-energy residual | restart drift E_B |")
        P("|---|---|---|---|---|---|---|---|---|")
        for key, r in sorted(ref["values"].items(), key=lambda t: -float(t[0])):
            P(f"| {key} | {f(r['H_k1'])} ± {f(r['H_k1_se'], 2)} | {f(r['H_k_ge_2'])} ± {f(r['H_k_ge_2_se'], 2)} | {f(r['EB_k1_fraction'])} | "
              f"{f(r['current_helicity_z'], 2)} | {f(r['r_b'])} | {f(r['balance_residual_total'])} ± {f(r['balance_residual_total_se'], 2)} | "
              f"{f(r['balance_residual_magnetic'])} | {f(r.get('restart_drift_eb'))} |")
        vals = list(ref["values"].values())
        bad1 = [k for k, r in ref["values"].items() if not r["H_k1"] < -2 * r["H_k1_se"]]
        bad2 = [k for k, r in ref["values"].items() if not r["H_k_ge_2"] > 2 * r["H_k_ge_2_se"]]
        frac = [r["EB_k1_fraction"] for r in vals]
        P(f"\nH11: H(1) negative by 2 SE at {len(vals) - len(bad1)} of {len(vals)} η; Σ_{{k ≥ 2}} H positive by 2 SE at "
          f"{len(vals) - len(bad2)} of {len(vals)} η (fails at η = {', '.join(bad2) if bad2 else 'none'}); E_B(1)/E_B in "
          f"[{f(min(frac))}, {f(max(frac))}]; |z| of ⟨j·B⟩ above 2 at {sum(abs(r['current_helicity_z']) > 2 for r in vals)} of {len(vals)} η. "
          "SE over the trajectory means; r_b = |Σ_k E J(k)| / Σ_k |E J(k)| with J(k) the shell spectrum of ⟨j·B⟩.")
        test = [(k, r) for k, r in ref["values"].items() if r["split"] == "test"]
        P("\nNull count of the reference against the evaluation grid (test η, same 100 snapshots): "
          + "; ".join(f"η = {k}: " + ", ".join(f"{g}³: {f(r.get(f'null_count_mean_grid{g}_n100'))}" for g in (32, 48, 64))
                      for k, r in test) + ".\n")
    fp = root / "e4_floor.json"
    floors = json.loads(fp.read_text())["values"] if fp.exists() and not quick else None
    if floors and ref:
        P("### Noise floors of the energy distance (experiments/e4_floor.py)\n")
        P("| η | set | trajectory-split floor, n = 512: mean ± sd [min, max] over 20 splits | random-split floor, n = 512 | ratio | E\\|Y − Y'\\| |")
        P("|---|---|---|---|---|---|")
        for key, r in sorted(floors.items(), key=lambda t: -float(t[0])):
            a, b = r["traj_split_512"], r["random_split_512"]
            P(f"| {key} | {ref['values'][key]['split']} | {f(a['mean'])} ± {f(a['sd'])} [{f(a['min'])}, {f(a['max'])}] | {f(b['mean'])} | "
              f"{f(a['mean'] / b['mean'])} | {f(r['mean_pairwise_distance'])} |")
        P("\nThe C1 ratio uses the trajectory-split floor (two reference subsamples from disjoint halves of the 24 trajectories, mean "
          "of the first 10 splits). It contains the variability between trajectories, it is uncertain (the splits reuse the same 24 "
          "trajectories) and it favours the generator: a perfect generator would score below 1 (about 0.6 by the encadrant's "
          "extrapolation, an estimate). The random-split floor is the sampling noise of 512 snapshots that ignore the trajectories.\n")
    if not runs:
        P("No model run yet.\n")
        return out
    seeds = sorted(runs)
    cfg = runs[seeds[0]]["config"]
    P(f"Models (experiments/e4_mhd3d.py): ResMLP {cfg['width']}×{cfg['depth']}, {cfg['iters']} iterations, batch {cfg['batch']}, "
      f"lr {cfg['lr']}; latent dimension {cfg['dim_potentials']} (potentials) or {cfg['dim_components']} (components); "
      f"{cfg['n_train']} training snapshots; {cfg['n_gen']} samples per validation and test η, Heun {cfg['steps']} steps "
      f"(diffusion: {2 * cfg['steps']} ancestral steps); fine-tuning {cfg['ft_iters']} iterations, β = {cfg['beta']}; "
      f"nulls on {cfg['n_null']} samples, restart of {cfg['n_restart']} samples over τ = {cfg['tau']}; seeds {seeds}.\n")
    names = [v for v in GENERATORS + POST if any(v in r["evaluation"] for r in runs.values())]
    for split in ("test", "val", "train"):
        P(f"### Means over the {split} η (mean over the seeds)\n")
        P("| variant | " + " | ".join(k[1] for k in KEYS) + " |")
        P("|---|" + "---|" * len(KEYS))
        for v in names:
            P(f"| {v} | " + " | ".join(f(float(np.nanmean(per_seed(runs, v, k, split, a)))) for k, _, a in KEYS) + " |")
        if ref and split == "test":
            t = [r for r in ref["values"].values() if r["split"] == "test"]
            P(f"| reference | 1 (floor) | – | {f(np.mean([abs(r['balance_residual_total']) for r in t]))} | – | – | – | "
              f"{f(np.mean([r['restart_drift_eb'] for r in t]))} | {f(np.mean([r['hc_sign_asym'] for r in t]))} | 1 | – |")
        P("")
    P(f"### Across seeds: means over the test η, mean ± sd [min, max] over {len(seeds)} seeds\n")
    sk = [k for k in KEYS if k[0] in ("ed_ratio", "balance_residual_total", "spec_err_b_l2", "hel_m_err_rel", "null_count_err_rel")]
    P("| variant | " + " | ".join(k[1] for k in sk) + " |")
    P("|---|" + "---|" * len(sk))
    for v in names:
        cells = []
        for k, _, a in sk:
            x = per_seed(runs, v, k, "test", a)
            cells.append(f"{f(np.nanmean(x))} ± {f(np.nanstd(x, ddof=1) if len(x) > 1 else None)} [{f(np.nanmin(x))}, {f(np.nanmax(x))}]")
        P(f"| {v} | " + " | ".join(cells) + " |")
    sel = select(runs)
    if not quick and not replication:
        (R / "e4_selection.json").write_text(json.dumps(sel, indent=1), encoding="utf-8")
    sv = sel["variant"]
    P(f"\n### Selected generator: {sv if sv else 'none'}\n")
    if sv is None:
        P("This run holds no candidate for the selected generator (the Gaussian laws, the checkpoints of H28 and the corrections of "
          "the samples are not candidates): the objectives are those of the main run.\n")
    else:
        P("Validation energy-distance ratio (mean over the seeds): " + ", ".join(f"{k} {f(v)}" for k, v in sel["val_ed_ratio"].items()) + ".\n")
        P("| objective | value on the held-out test η (mean over the seeds) |")
        P("|---|---|")
        c4 = per_seed(runs, sv, "spec_err_b_l2") + per_seed(runs, sv, "hel_m_err_rel")
        div_max = max(x["div_rel_b_max"] for r in runs.values() for x in r["evaluation"][sv]["test"])
        for label, val in (("C1 energy distance / floor", np.mean(per_seed(runs, sv, "ed_ratio"))),
                           ("C2 max relative divergence of B", div_max),
                           ("C3 |energy balance residual|", np.mean(per_seed(runs, sv, "balance_residual_total", absolute=True))),
                           ("C4 spectrum error + helicity error", np.mean(c4)),
                           ("C5 relative error on the null count", np.mean(per_seed(runs, sv, "null_count_err_rel"))),
                           ("T1 restart drift of E_B", np.mean(per_seed(runs, sv, "restart_drift_eb"))),
                           ("T2 polarity asymmetry", np.mean(per_seed(runs, sv, "hc_sign_asym")))):
            P(f"| {label} | {f(float(val))} |")
        if floors:
            x20 = np.asarray([np.mean([row["ed"] / floors[f"{row['eta']:.5f}"]["traj_split_512"]["mean"]
                                       for row in r["evaluation"][sv]["test"]]) for r in runs.values()])
            x10 = per_seed(runs, sv, "ed_ratio")
            P(f"\nEnergy-distance ratio of {sv} per seed with the floor of the protocol (10 splits): {', '.join(f(x) for x in x10)} "
              f"(mean {f(float(x10.mean()))}); with the floor averaged over 20 splits: {', '.join(f(float(x)) for x in x20)} (mean {f(float(x20.mean()))}).")
    if len(seeds) >= 2:
        P(f"\n### Paired comparisons over the seeds {seeds} (means over the test η; SE = sd(ddof = 1)/√n)\n")
        P("| comparison | per-seed differences | mean ± SE | mean/SE | seeds with a positive difference |")
        P("|---|---|---|---|---|")
        ed = lambda v: per_seed(runs, v, "ed_ratio")                                   # noqa: E731
        res = lambda v: per_seed(runs, v, "balance_residual_total", absolute=True)     # noqa: E731
        P(paired_row("ED ratio: W0_free − W4_potentials (H4)", ed("W0_free"), ed("W4_potentials")))
        P(paired_row("ED ratio: W0_free − W1_penalty (H5)", ed("W0_free"), ed("W1_penalty")))
        P(paired_row("ED ratio: W2_final_projection − W3_projected_flow (H6)", ed("W2_final_projection"), ed("W3_projected_flow")))
        P(paired_row("|energy residual|: W5_control − W5_stationarity (H7)", res("W5_control"), res("W5_stationarity")))
        P(paired_row("ED ratio: W5_stationarity − W5_control (H7)", ed("W5_stationarity"), ed("W5_control")))
        for key, label, ab in (("balance_residual_magnetic", "|magnetic balance|", True), ("r_b", "r_b (helicity identity)", False),
                               ("null_count_err_rel", "err. nulls", False), ("spec_err_b_l2", "err. E_B(k)", False)):   # side effects of the loss
            P(paired_row(f"{label}: W5_stationarity − W5_control (side effect, H7)", per_seed(runs, "W5_stationarity", key, absolute=ab),
                         per_seed(runs, "W5_control", key, absolute=ab)))
        P(paired_row("ED ratio: W7_tilting − W5_stationarity_half (H8)", ed("W7_tilting"), ed("W5_stationarity_half")))
        P(paired_row("ED ratio: W7_tilting − W5_control_half", ed("W7_tilting"), ed("W5_control_half")))
        P(paired_row("polarity asymmetry: W4_potentials − W4s_potentials_sym (H9)",
                     per_seed(runs, "W4_potentials", "hc_sign_asym"), per_seed(runs, "W4s_potentials_sym", "hc_sign_asym")))
        P(paired_row("ED ratio: W4s_potentials_sym − W4_potentials (H9)", ed("W4s_potentials_sym"), ed("W4_potentials")))
        P(paired_row("ED ratio: W6_diffusion − W4_potentials (H10)", ed("W6_diffusion"), ed("W4_potentials")))
        if not np.all(np.isnan(ed("W4c_potentials_smooth"))):
            P(paired_row("ED ratio: W4_potentials − W4c_potentials_smooth (H15)", ed("W4_potentials"), ed("W4c_potentials_smooth")))
        has = lambda v: not np.all(np.isnan(ed(v)))                                  # noqa: E731
        if has("G0_gaussian_modes") and any(has(v) for v in REGISTERED):
            best = min((v for v in REGISTERED if has(v)), key=lambda v: float(np.nanmean(ed(v))))
            P(paired_row(f"ED ratio: best registered generator ({best}) − G0_gaussian_modes (H16)", ed(best), ed("G0_gaussian_modes")))
        if has("W9_skip_sym"):
            P(paired_row("ED ratio: W4s_potentials_sym − W9_skip_sym (H17)", ed("W4s_potentials_sym"), ed("W9_skip_sym")))
        if has("W9L_skip_long") and has("G0_gaussian_modes"):
            for key, label in (("restart_drift_eb", "restart drift E_B"), ("null_count_err_rel", "err. nulls"), ("ed_ratio", "ED ratio")):
                P(paired_row(f"{label}: G0_gaussian_modes − W9L_skip_long (H18)", per_seed(runs, "G0_gaussian_modes", key),
                             per_seed(runs, "W9L_skip_long", key)))
        h12 = {s: r["h12"] for s, r in runs.items() if r["h12"]}
        if h12:
            m = lambda k: np.asarray([np.mean([x[k] for x in rows]) for rows in h12.values()])   # noqa: E731
            P(paired_row("|err H_M|: tilting on the energy identity − tilting on the helicity identity (H12)",
                         m("hel_m_err_rel_tilt_a"), m("hel_m_err_rel_tilt_b")))
            P(paired_row("normalized residuals of W4s: r_b − r_a (H12)", m("r_b"), m("r_a")))
        div0, div1 = per_seed(runs, "W0_free", "div_rel_b_mean"), per_seed(runs, "W1_penalty", "div_rel_b_mean")
        if not np.all(np.isnan(ed("W4c_potentials_smooth"))):
            P(f"\nH15: seed-mean ED ratio on the held-out η: W4_potentials {f(float(np.nanmean(ed('W4_potentials'))))}, "
              f"W4c_potentials_smooth {f(float(np.nanmean(ed('W4c_potentials_smooth'))))}; on the training η: "
              f"{f(float(np.nanmean(per_seed(runs, 'W4_potentials', 'ed_ratio', 'train'))))} and "
              f"{f(float(np.nanmean(per_seed(runs, 'W4c_potentials_smooth', 'ed_ratio', 'train'))))}.")
        if has("W10_anchored") and has("G0_gaussian_modes"):
            for v, h in (("W10_anchored", "H19"), ("W11_anchored_skip", "H20"), ("W11L_anchored_skip_long", "H20, long")):
                if not has(v):
                    continue
                for key, label in (("ed_ratio", "ED ratio"), ("restart_drift_eb", "restart drift E_B"), ("null_count_err_rel", "err. nulls")):
                    P(paired_row(f"{label}: G0_gaussian_modes − {v} ({h})", per_seed(runs, "G0_gaussian_modes", key), per_seed(runs, v, key)))
        if has("G0_gaussian_modes"):                 # what a Gaussian law cannot hold, and what it holds better (review of 2026-11-13)
            for v in ("W9_skip_sym", "W11_anchored_skip", "W9L_skip_long", "W11L_anchored_skip_long"):
                if not has(v):
                    continue
                for key, label, ab in (("balance_residual_magnetic", "|magnetic balance|", True), ("restart_drift_eu", "restart drift E_u", False),
                                       ("balance_residual_total", "|energy residual|", True), ("spec_err_b_l2", "err. E_B(k)", False)):
                    P(paired_row(f"{label}: G0_gaussian_modes − {v}", per_seed(runs, "G0_gaussian_modes", key, absolute=ab),
                                 per_seed(runs, v, key, absolute=ab)))
            if has("W9_skip_sym") and has("W11_anchored_skip"):
                for key, label in (("ed_ratio", "ED ratio"), ("restart_drift_eb", "restart drift E_B"), ("null_count_err_rel", "err. nulls")):
                    P(paired_row(f"{label}: W9_skip_sym − W11_anchored_skip", per_seed(runs, "W9_skip_sym", key), per_seed(runs, "W11_anchored_skip", key)))
        if has("G1_gaussian_full"):                     # H22: what the inter-mode covariance holds
            mb = per_seed(runs, "G1_gaussian_full", "balance_residual_magnetic", absolute=True)
            P(f"| H22: |magnetic balance| of G1_gaussian_full, per seed | {', '.join(f(x) for x in mb)} | {f(float(np.nanmean(mb)))} ± "
              f"{f(float(np.nanstd(mb, ddof=1) / np.sqrt(len(mb))))} | – | – |")
            for key, label in (("restart_drift_eb", "restart drift E_B"), ("null_count_err_rel", "err. nulls"), ("ed_ratio", "ED ratio"),
                               ("restart_drift_eu", "restart drift E_u"), ("restart_drift_eb_max", "largest |drift of E_B| over τ"),
                               ("restart_drift_eu_max", "largest |drift of E_u| over τ")):
                for other in ("W9_skip_sym", "G0_gaussian_modes"):
                    if has(other):
                        P(paired_row(f"{label}: {other} − G1_gaussian_full (H22)", per_seed(runs, other, key), per_seed(runs, "G1_gaussian_full", key)))
        if has("W12_skip_stationarity"):                # H23, H24: loss and sampling mechanisms on the model with the affine term
            for key, label, ab in (("balance_residual_total", "|energy residual|", True), ("balance_residual_magnetic", "|magnetic balance|", True),
                                   ("r_b", "r_b (helicity identity)", False), ("null_count_err_rel", "err. nulls", False),
                                   ("spec_err_b_l2", "err. E_B(k)", False)):
                P(paired_row(f"{label}: W12_skip_control − W12_skip_stationarity (H23)", per_seed(runs, "W12_skip_control", key, absolute=ab),
                             per_seed(runs, "W12_skip_stationarity", key, absolute=ab)))
            P(paired_row("ED ratio: W12_skip_stationarity − W12_skip_control (H23)", ed("W12_skip_stationarity"), ed("W12_skip_control")))
            P(paired_row("|energy residual|: W12_skip_control_half − W13_skip_tilting (H24)", res("W12_skip_control_half"), res("W13_skip_tilting")))
            P(paired_row("ED ratio: W13_skip_tilting − W12_skip_control_half (H24)", ed("W13_skip_tilting"), ed("W12_skip_control_half")))
        if has("S_w512"):
            def loss_of(v: str) -> str:
                x = [r["times"].get(v, {}).get("fm_loss_train_sample") for r in runs.values()]
                x = [y for y in x if y is not None]
                return f(float(np.mean(x))) if x else "–"
            P("\nH21 (width scan, no affine term): " + "; ".join(
                f"{v}: ED ratio {f(float(np.nanmean(ed(v))))}, loss {loss_of(v)}" for v in
                ("S_w512", "S_w2048", "S_w5632", "S_w512_long", "S_w2048_long") if has(v)) + " (π/2 = 1.571).")
        if has("W13_skip_tilting"):
            P(f"\nH24: ESS/N of W13_skip_tilting, seed mean over the test η: {f(float(np.nanmean(per_seed(runs, 'W13_skip_tilting', 'ess_frac'))))}; "
              f"H23: ratio of the seed-mean ED ratios W12_skip_stationarity / W12_skip_control: "
              f"{f(float(np.nanmean(ed('W12_skip_stationarity')) / np.nanmean(ed('W12_skip_control'))))}.")
        if has("W13_skip_tilting") and floors:
            corr13 = np.asarray([np.mean([(x["ed"] - (1 / (x["ess_frac"] * x["n"]) - 1 / x["n"])
                                           * floors[f"{x['eta']:.5f}"]["mean_pairwise_distance"]) / x["ed_floor"]
                                          for x in r["evaluation"]["W13_skip_tilting"]["test"]]) for r in runs.values()])
            dd = ed("W12_skip_control_half") - corr13
            P(f"H24, W13 corrected for the extra bias of a weighted sample (estimate): ED ratio per seed {', '.join(f(float(x)) for x in corr13)} "
              f"(mean {f(float(corr13.mean()))}); W12_skip_control_half − corrected W13: {f(float(dd.mean()))} ± "
              f"{f(float(dd.std(ddof=1) / np.sqrt(len(dd))))}, positive in {int((dd > 0).sum())} of {len(dd)} seeds.")
            for key, label, ab in (("r_b", "r_b (helicity identity)", False), ("spec_err_u_l2", "err. E_u(k)", False),
                                   ("balance_residual_magnetic", "|magnetic balance|", True), ("null_count_err_rel", "err. nulls", False),
                                   ("spec_err_b_l2", "err. E_B(k)", False), ("hel_m_err_rel", "err. H_M", True), ("hc_sign_asym", "polarity", False)):
                a_, b_ = per_seed(runs, "W12_skip_control_half", key, absolute=ab), per_seed(runs, "W13_skip_tilting", key, absolute=ab)
                dk = a_ - b_
                P(f"H24, {label}: untilted half {f(float(np.nanmean(a_)))}, tilted {f(float(np.nanmean(b_)))}; difference {f(float(np.nanmean(dk)))} ± "
                  f"{f(float(np.nanstd(dk, ddof=1) / np.sqrt(len(dk))))}, tilted better in {int((dk > 0).sum())} of {len(dk)} seeds.")
        for v in ("G0_gaussian_modes", "G1_gaussian_full", "W9_skip_sym", "W11_anchored_skip", "W13_skip_tilting", "S_w2048", "S_w5632"):
            if has(v):                              # production over Ohmic dissipation, from the signed residual r = (P − D)/(|P| + D)
                per = {}
                for r in runs.values():
                    for x in r["evaluation"].get(v, {}).get("test", []):
                        per.setdefault(x["eta"], []).append(x["balance_residual_magnetic"])
                parts = []
                for e in sorted(per, reverse=True):
                    rm = float(np.mean(per[e]))
                    parts.append(f"η = {e:.4f}: residual {f(rm)}, P/D {f((1 + rm) / (1 - rm)) if rm > -0.999 else 'not recoverable (P ≤ 0 in some rows)'}")
                P(f"Magnetic energy balance of {v} (seed mean per held-out η): " + "; ".join(parts) + ".")
        for v in ("S_w512", "S_w2048", "S_w5632", "W12_skip_stationarity", "W12_skip_control"):
            if has(v) and not np.all(np.isnan(per_seed(runs, v, "restart_drift_eb_max"))):
                P(f"Largest restart drift over τ of {v} (seed mean over the test η): E_B {f(float(np.nanmean(per_seed(runs, v, 'restart_drift_eb_max'))))}, "
                  f"E_u {f(float(np.nanmean(per_seed(runs, v, 'restart_drift_eu_max'))))}.")
        split = [v for v in ("G0_gaussian_modes", "G1_gaussian_full", "G3_gaussianised_G1", "G2_gaussianised_W9", "W9_skip_sym", "W9N_skip_sym", "W11_anchored_skip")
                 if has(v) and any("prod_fluct_over_d" in x for r in runs.values() for x in r["evaluation"].get(v, {}).get("test", []))]
        if split:                                   # H25: second-order and third-order parts of the magnetic production
            P("\nMagnetic production over the Ohmic dissipation, split into the part carried by the mean flow (second-order statistics) "
              "and the rest (third-order moment), per held-out η; reference: mean ± SE over the trajectories; variants: mean ± SE over the seeds.\n")
            etas = sorted({x["eta"] for r in runs.values() for x in r["evaluation"][split[0]]["test"]}, reverse=True)
            P("| law | " + " | ".join(f"η = {e:.4f}: mean-flow part | third-order part" for e in etas) + " |")
            P("|---|" + "---|---|" * len(etas))
            if ref and "prod_fluct_over_d" in next(iter(ref["values"].values())):
                P("| reference | " + " | ".join(
                    f"{f(ref['values'][f'{e:.5f}']['prod_mean_over_d'])} ± {f(ref['values'][f'{e:.5f}']['prod_mean_over_d_se'])} | "
                    f"{f(ref['values'][f'{e:.5f}']['prod_fluct_over_d'])} ± {f(ref['values'][f'{e:.5f}']['prod_fluct_over_d_se'])}" for e in etas) + " |")
            per_v = {}
            for v in split:
                cells = []
                for e in etas:
                    a = np.asarray([[x["prod_mean_over_d"], x["prod_fluct_over_d"]] for r in runs.values()
                                    for x in r["evaluation"][v]["test"] if x["eta"] == e])
                    per_v[(v, e)] = a[:, 1]
                    sem = a.std(0, ddof=1) / np.sqrt(len(a)) if len(a) > 1 else np.zeros(2)
                    cells.append(f"{f(float(a[:, 0].mean()))} ± {f(float(sem[0]))} | {f(float(a[:, 1].mean()))} ± {f(float(sem[1]))}")
                P(f"| {v} | " + " | ".join(cells) + " |")
            if ref and "prod_fluct_over_d" in next(iter(ref["values"].values())) and "W9_skip_sym" in split:
                for e in etas:
                    rv = ref["values"][f"{e:.5f}"]
                    w9 = per_v[("W9_skip_sym", e)]
                    P(f"H25, η = {e:.4f}: third-order part of the reference {f(rv['prod_fluct_over_d'])} ± {f(rv['prod_fluct_over_d_se'])} "
                      f"({f(rv['prod_fluct_over_d'] / rv['prod_fluct_over_d_se'], 2)} SE over the trajectory means; delete-one-trajectory "
                      f"jackknife with the mean flow recomputed: ± {f(rv.get('prod_fluct_over_d_se_jack', float('nan')))}, "
                      f"{f(rv['prod_fluct_over_d'] / rv.get('prod_fluct_over_d_se_jack', float('nan')), 2)} SE); W9 per seed {', '.join(f(float(x)) for x in w9)}; "
                      f"ratio of the seed mean to the reference {f(float(w9.mean() / rv['prod_fluct_over_d']), 2)}; "
                      f"seeds with the sign of the reference and at least half its magnitude: "
                      f"{int(((np.sign(w9) == np.sign(rv['prod_fluct_over_d'])) & (np.abs(w9) >= 0.5 * abs(rv['prod_fluct_over_d']))).sum())} of {len(w9)}.")
        if split and ref and has("G1_gaussian_full") and "prod_mean_over_d_se_jack" in next(iter(ref["values"].values())):
            vals = sorted(ref["values"].items(), key=lambda kv: -float(kv[0]))
            P("Third-order part of the magnetic production of the reference over the Ohmic dissipation, at the eleven η (± jackknife SE): "
              + "; ".join(f"η = {float(e):.4f}: {f(v['prod_fluct_over_d'])} ± {f(v['prod_fluct_over_d_se_jack'])}" for e, v in vals) + ".")
            for v in ("W9_skip_sym", "G1_gaussian_full"):          # asked by the review of the report v4
                if not has(v):
                    continue
                acc: dict = {}
                for r in runs.values():
                    for sp in ("train", "test"):
                        for x in r["evaluation"][v].get(sp, []):
                            acc.setdefault((sp, f"{x['eta']:.5f}"), []).append((x.get("prod_fluct_over_d", float("nan")), x["null_count"]))
                keys = sorted(acc, key=lambda kv: (kv[0], -float(kv[1])))
                if v == "W9_skip_sym":
                    P("Third-order part of W9_skip_sym at the training η evaluated (seed mean; ratio to the reference): " + "; ".join(
                        f"η = {float(e):.4f}: {f(float(np.mean([a_[0] for a_ in acc[(sp, e)]])))} "
                        f"({f(float(np.mean([a_[0] for a_ in acc[(sp, e)]])) / ref['values'][e]['prod_fluct_over_d'], 2)})"
                        for sp, e in keys if sp == "train") + ".")
                else:
                    P("Null points of G1_gaussian_full over those of the reference (seed mean): " + "; ".join(
                        f"{'training' if sp == 'train' else 'held-out'} η = {float(e):.4f}: "
                        f"{f(float(np.mean([a_[1] for a_ in acc[(sp, e)]])) / ref['values'][e]['null_count_mean'], 3)}" for sp, e in keys) + ".")
            rows = {}                              # H25, check 2: at the training η, mean-flow part of the reference against P/D of G1
            for sp in ("train", "val"):            # the validation η are outside the registered check: G1 is interpolated there
                for r in runs.values():
                    for x in r["evaluation"]["G1_gaussian_full"].get(sp, []):
                        if "prod_over_d" in x:
                            rows.setdefault((sp, f"{x['eta']:.5f}"), []).append(x["prod_over_d"])
            for (sp, e), g1 in sorted(rows.items(), key=lambda kv: (kv[0][0], -float(kv[0][1]))):
                g1 = np.asarray(g1)
                rv = ref["values"][e]
                se_g, se_r = float(g1.std(ddof=1) / np.sqrt(len(g1))) if len(g1) > 1 else float("nan"), rv["prod_mean_over_d_se_jack"]
                d = float(g1.mean() - rv["prod_mean_over_d"])
                where = "training η" if sp == "train" else "validation η (G1 interpolated, outside the registered check)"
                P(f"H25, check at the {where} = {float(e):.4f}: P/D of G1 {f(float(g1.mean()))} ± {f(se_g)} (SE over the seeds), mean-flow part of the "
                  f"reference {f(rv['prod_mean_over_d'])} ± {f(se_r)} (jackknife); difference {f(d)}: {f(d / se_g, 2)} SE of G1, "
                  f"{f(d / se_r, 2)} SE of the reference, {f(d / float(np.hypot(se_g, se_r)), 2)} combined SE.")
        # ---- restart anchored on the stationary energy of the reference (reviews of 2026-11-13): a(τ) = E_B(τ)/E_B,ref − 1
        def anchored(row: dict) -> list[float] | None:
            if "restart_anchor" in row:
                return list(row["restart_anchor"]["eb"])
            if "restart_curve" in row and ref:                       # older runs: initial energy of the whole ensemble (approximation)
                e0 = row["E_B"] / ref["values"][f"{row['eta']:.5f}"]["E_B"]
                return [e0 - 1] + [e0 * (1 + x) - 1 for x in row["restart_curve"]["eb"]]
            return None

        def anchor_stats(v: str) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
            """Per seed (mean over the test η): the anchored curve, the overshoot max_τ |a| − |a(0)| and |a| at the last time."""
            curves, over, end = [], [], []
            for r in runs.values():
                rows = [anchored(x) for x in r["evaluation"].get(v, {}).get("test", [])]
                rows = [x for x in rows if x is not None]
                if rows:
                    curves.append(np.mean(rows, axis=0))
                    over.append(np.mean([max(abs(y) for y in x[1:]) - abs(x[0]) for x in rows]))
                    end.append(np.mean([abs(x[-1]) for x in rows]))
            return (np.asarray(curves), np.asarray(over), np.asarray(end)) if curves else None

        anch = {v: anchor_stats(v) for v in ("G0_gaussian_modes", "G1_gaussian_full", "G3_gaussianised_G1", "G2_gaussianised_W9", "W9_skip_sym",
                                           "W9N_skip_sym", "W11_anchored_skip", "W12_skip_stationarity", "W12_skip_control", "S_w2048",
                                           "S_w5632", "W9L_skip_long") if has(v)}
        anch = {v: a_ for v, a_ in anch.items() if a_ is not None}
        if anch:
            taus = next((x["restart_anchor"]["tau"] for r in runs.values() for v in anch for x in r["evaluation"][v].get("test", [])
                         if "restart_anchor" in x), None)
            if taus is None:
                taus = [0.0] + next(x["restart_curve"]["tau"] for r in runs.values() for v in anch for x in r["evaluation"][v].get("test", [])
                                    if "restart_curve" in x)
            exact = any("restart_anchor" in x for r in runs.values() for v in anch for x in r["evaluation"][v].get("test", []))
            P("\nRestart anchored on the stationary magnetic energy of the reference, a(τ) = E_B(τ)/E_B,ref − 1 (mean over the held-out η and "
              "the seeds); overshoot = max_τ |a(τ)| − |a(0)|" + ("" if exact else "; initial value from the energy of the whole ensemble (approximation)") + ".\n")
            P("| law | " + " | ".join(f"τ = {t:g}" for t in taus) + " | overshoot ± SE | |a| at the last time ± SE |")
            P("|---|" + "---|" * (len(taus) + 2))
            sem = lambda x: f(float(x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 1 else "–"          # noqa: E731
            if ref and "restart_anchor_eb_mean" in next((x for x in ref["values"].values() if x["split"] == "test"), {}):
                rr = [x for x in ref["values"].values() if x["split"] == "test"]
                P("| reference (4 draws; SE over the draws, mean over η) | " + " | ".join(
                    f"{f(float(np.mean([x['restart_anchor_eb_mean'][i] for x in rr])))} ± {f(float(np.mean([x['restart_anchor_eb_se'][i] for x in rr])))}"
                    for i in range(len(taus))) + " | – | – |")
            for v, (cv, ov, en) in anch.items():
                P(f"| {v} | " + " | ".join(f(float(x)) for x in cv.mean(0)) + f" | {f(float(ov.mean()))} ± {sem(ov)} | {f(float(en.mean()))} ± {sem(en)} |")
            for v in ("W9_skip_sym", "G1_gaussian_full", "G0_gaussian_modes"):                          # H26
                if v in anch:
                    cv, ov, en = anch[v]
                    P(f"H26, {v}: initial deviation a(0) per seed {', '.join(f(float(x)) for x in cv[:, 0])}; overshoot per seed "
                      f"{', '.join(f(float(x)) for x in ov)} (mean {f(float(ov.mean()))}); |a| at the last time per seed {', '.join(f(float(x)) for x in en)} "
                      f"(mean {f(float(en.mean()))}).")
            for a_, b_, label in (("G2_gaussianised_W9", "W9N_skip_sym", "H27"), ("G3_gaussianised_G1", "G1_gaussian_full", "H27, null control")):
                if a_ in anch and b_ in anch:
                    P(paired_row(f"overshoot of E_B: {a_} − {b_} ({label})", anch[a_][1], anch[b_][1]))
            if exact:                      # measures asked by the review of H25-H27, post hoc: not registered criteria
                def course(v: str, fn) -> np.ndarray:
                    return np.asarray([np.mean([fn(anchored(x)) for x in r["evaluation"][v]["test"]]) for r in runs.values()
                                       if r["evaluation"].get(v, {}).get("test")])
                post = [v for v in ("W9_skip_sym", "G2_gaussianised_W9", "G1_gaussian_full", "G3_gaussianised_G1", "G0_gaussian_modes") if v in anch]
                P("Post hoc (review of H25-H27, not registered), seed means over the held-out η: rise of E_B after the restart, max_τ a(τ) − a(0): "
                  + "; ".join(f"{v} {f(float(course(v, lambda x: max(x[1:]) - x[0]).mean()))}" for v in post)
                  + ". Largest |a(τ)| over the course, τ = 0 included: "
                  + "; ".join(f"{v} {f(float(course(v, lambda x: max(abs(y) for y in x)).mean()))}" for v in post)
                  + ". Excursion above the reference, max(0, max_τ a(τ)): "
                  + "; ".join(f"{v} {f(float(course(v, lambda x: max(0.0, max(x))).mean()))}" for v in post) + ".")
                if "G2_gaussianised_W9" in anch and "W9N_skip_sym" in anch:
                    P(paired_row("excursion of E_B above the reference, max(0, max_τ a): G2_gaussianised_W9 − W9N_skip_sym (post hoc, not registered)",
                                 course("G2_gaussianised_W9", lambda x: max(0.0, max(x))), course("W9N_skip_sym", lambda x: max(0.0, max(x)))))
            if exact and "G2_gaussianised_W9" in anch and "W9N_skip_sym" in anch:      # asked by the review of the report v4
                def per_eta(v: str, fn) -> dict:
                    out: dict = {}
                    for r in runs.values():
                        for x in r["evaluation"][v]["test"]:
                            out.setdefault(round(x["eta"], 4), []).append(fn(anchored(x)))
                    return {e: np.asarray(a_) for e, a_ in out.items()}
                exc = lambda x: max(0.0, max(x))                                         # noqa: E731
                g2e, w9e = per_eta("G2_gaussianised_W9", exc), per_eta("W9N_skip_sym", exc)
                P("Post hoc (not registered), per held-out η: excursion above the reference of G2 minus that of W9N, paired over the seeds, "
                  "with the production over dissipation of the two laws: " + "; ".join(
                      f"η = {e:.4f}: {f(float((g2e[e] - w9e[e]).mean()))} ± {f(float((g2e[e] - w9e[e]).std(ddof=1) / np.sqrt(len(w9e[e]))))}, "
                      f"{int((g2e[e] - w9e[e] > 0).sum())} of {len(w9e[e])} seeds positive"
                      f" (P/D {f(float(np.mean([x['prod_over_d'] for r in runs.values() for x in r['evaluation']['G2_gaussianised_W9']['test'] if round(x['eta'], 4) == e])))}"
                      f" and {f(float(np.mean([x['prod_over_d'] for r in runs.values() for x in r['evaluation']['W9N_skip_sym']['test'] if round(x['eta'], 4) == e])))})"
                      for e in sorted(g2e, reverse=True)) + ".")
            # the drift of the objective T1 against the bias of the law on E_B
            pts = [(float(np.nanmean(per_seed(runs, v, "restart_eb_signed"))), float(-cv[:, 0].mean() / (1 + cv[:, 0].mean())))
                   for v, (cv, _, _) in anch.items() if not np.all(np.isnan(per_seed(runs, v, "restart_eb_signed")))]
            if len(pts) >= 4:
                xs, ys = np.asarray(pts).T
                P(f"Signed drift of E_B at τ = 4 against the bias E_B,ref/E_B(0) − 1 of the law, over the {len(pts)} laws above: "
                  f"correlation {f(float(np.corrcoef(xs, ys)[0, 1]), 2)}.")
        for line in h28_lines(runs, ref) + h29_lines(runs, ref) + h32_lines(runs, ref) + h33_lines(runs, ref, root) + h34_lines(runs, ref, root) + h35_lines(runs, ref, root) + h36_lines(runs, ref, root) + h37_lines(runs, ref, root) + h38_lines(runs, ref, root) + h39_lines(runs, ref, root) + h40_lines(runs, ref, root) + h41_lines(runs, ref, root):
            P(line)
        h27 = [x for r in runs.values() for x in r.get("h27", [])]
        if h27:
            P(f"H27, energy distance between the samples of G2 and of W9N over the reference floor, mean over the held-out η and the seeds: "
              f"{f(float(np.mean([x['ed_g2_w9'] / x['ed_floor'] for x in h27])))}; between two halves of the W9N samples (256 each, over the floor at 512): "
              f"{f(float(np.mean([x['ed_w9_halves'] / x['ed_floor'] for x in h27])))}. The energy distance is a V statistic whose value "
              f"under equal laws scales as 1/n + 1/m: the two-halves value at 256 corresponds to "
              f"{f(float(np.mean([0.5 * x['ed_w9_halves'] / x['ed_floor'] for x in h27])))} at 512 against 512; G2 against W9N is "
              f"{f(float(np.mean([x['ed_g2_w9'] / x['ed_floor'] for x in h27]) / np.mean([0.5 * x['ed_w9_halves'] / x['ed_floor'] for x in h27])), 2)} "
              f"times that (review of H25-H27).")
        w9b = "W9N_skip_sym" if has("W9N_skip_sym") else "W9_skip_sym"       # the base of G2, evaluated in the same group
        if has("G2_gaussianised_W9") and has(w9b):                     # H27: what of W9 is not in its first two moments
            def at(v: str, i: int, key: str = "eb") -> np.ndarray:
                return np.asarray([np.mean([abs(x["restart_curve"][key][i]) for x in r["evaluation"][v]["test"] if "restart_curve" in x])
                                   for r in runs.values()])
            taus = next(x["restart_curve"]["tau"] for r in runs.values() for x in r["evaluation"][w9b]["test"] if "restart_curve" in x)
            P("\n| comparison (H27) | per-seed differences | mean ± SE | mean/SE | seeds with a positive difference |")
            P("|---|---|---|---|---|")
            for i, t in enumerate(taus):
                P(paired_row(f"|drift of E_B| at τ = {t:g}: G2_gaussianised_W9 − its base W9 (H27)", at("G2_gaussianised_W9", i), at(w9b, i)))
            for key, label, ab in (("ed_ratio", "ED ratio", False), ("null_count_err_rel", "err. nulls", False),
                                   ("balance_residual_magnetic", "|magnetic balance|", True), ("restart_drift_eu_max", "largest |drift of E_u|, τ ≤ 4", False),
                                   ("std_residual_rel", "σ(dE/dt)/σ_ref", False)):
                P(paired_row(f"{label}: G2_gaussianised_W9 − its base W9 (H27, reported)", per_seed(runs, "G2_gaussianised_W9", key, absolute=ab),
                             per_seed(runs, w9b, key, absolute=ab)))
        if has("G1_gaussian_full"):
            rows = [x for r in runs.values() for x in r["evaluation"]["G1_gaussian_full"].get("test", []) if "restart_curve" in x]
            for v in ("G0_gaussian_modes", "G1_gaussian_full", "G3_gaussianised_G1", "G2_gaussianised_W9", "W9_skip_sym", "W9N_skip_sym", "W11_anchored_skip"):
                rows = [x for r in runs.values() for x in r["evaluation"].get(v, {}).get("test", []) if "restart_curve" in x]
                if rows:
                    taus = rows[0]["restart_curve"]["tau"]
                    eb = np.mean([x["restart_curve"]["eb"] for x in rows], axis=0)
                    eu = np.mean([x["restart_curve"]["eu"] for x in rows], axis=0)
                    P(f"Restart curve of {v} (signed relative change, mean over the test η and the seeds), τ = {', '.join(f(t) for t in taus)}: "
                      f"E_B {', '.join(f(float(x)) for x in eb)}; E_u {', '.join(f(float(x)) for x in eu)}.")
        if has("W9_skip_sym") and has("W4s_potentials_sym"):
            fl = [r["times"].get("W9_skip_sym", {}).get("fm_loss_train_sample") for r in runs.values()]
            fl = [x for x in fl if x is not None]
            P(f"\nH17: ratio of the seed-mean ED ratios W9_skip_sym / W4s_potentials_sym: "
              f"{f(float(np.nanmean(ed('W9_skip_sym')) / np.nanmean(ed('W4s_potentials_sym'))))}; flow-matching loss of W9_skip_sym on "
              f"a training sample, seed mean: {f(float(np.mean(fl))) if fl else '–'} (π/2 = 1.571 for independent unit Gaussian coordinates).")
        if has("W0_free") and has("W4s_potentials_sym"):          # notes of the registered groups A and B
            P(f"\nH5: relative divergence of B, seed mean: W0_free {f(div0.mean())}, W1_penalty {f(div1.mean())}, ratio {f(div1.mean() / div0.mean())}.")
            P(f"H7: ratio of the seed-mean ED ratios W5_stationarity / W5_control: {f(ed('W5_stationarity').mean() / ed('W5_control').mean())}.")
            P(f"H8: ESS/N of W7_tilting, seed mean over the test η: {f(float(np.nanmean(per_seed(runs, 'W7_tilting', 'ess_frac'))))}.")
            if floors:
                # extra V-statistic bias of a weighted sample: (Σw² − 1/n) E|X − X'| ≈ (1/ESS − 1/n) E|Y − Y'|
                corr = []
                for r in runs.values():
                    rows = r["evaluation"].get("W7_tilting", {}).get("test", [])
                    corr.append(np.mean([(x["ed"] - (1 / (x["ess_frac"] * x["n"]) - 1 / x["n"])
                                          * floors[f"{x['eta']:.5f}"]["mean_pairwise_distance"]) / x["ed_floor"] for x in rows]))
                corr = np.asarray(corr)
                P(paired_row("H8 with W7 corrected for the extra bias of a weighted sample (estimate): ED ratio W7 − W5_stationarity_half",
                             corr, ed("W5_stationarity_half")).replace("| H8", "H8", 1).rstrip(" |").replace(" | ", "; "))
            P(f"H9: ratio of the seed-mean ED ratios W4s_potentials_sym / W4_potentials: {f(ed('W4s_potentials_sym').mean() / ed('W4_potentials').mean())}; "
              f"binomial floor of the asymmetry for n = {cfg['n_gen']}: {f((2 * np.pi * cfg['n_gen']) ** -0.5)}.")
        if h12:
            ra, rb = m("r_a"), m("r_b")
            P(f"H12: seed mean of r_b / r_a: {f(float(np.mean(rb / ra)))}; r_b > r_a for {int((rb > ra).sum())} of {len(ra)} seeds; "
              f"ESS/N of the tilt on the helicity identity {f(float(m('ess_frac_tilt_b').mean()))}, on the energy identity "
              f"{f(float(m('ess_frac_tilt_a').mean()))}; |err H_M| without tilting {f(float(m('hel_m_err_rel_base').mean()))}.")
        h14 = [r["h14"] for r in runs.values() if r["h14"]]
        if h14:
            s0, s1 = cfg["steps"], 4 * cfg["steps"]
            a = np.asarray([np.mean([x[f"div_rel_b_mean_steps{s0}"] for x in rows]) for rows in h14])
            b = np.asarray([np.mean([x[f"div_rel_b_mean_steps{s1}"] for x in rows]) for rows in h14])
            P(f"H14: relative divergence of B of W0_free, seed mean: {f(a.mean())} with {s0} Heun steps, {f(b.mean())} with {s1} steps; "
              f"ratio per seed {', '.join(f(x) for x in b / a)}.")
        # H13: null count against the magnetic Taylor wavenumber
        if ref:
            xs, ys = [], []
            for r in runs.values():
                for v in GENERATORS:
                    for row in r["evaluation"].get(v, {}).get("test", []):
                        rr = ref["values"][f"{row['eta']:.5f}"]
                        if "null_count" in row and row["null_count"] > 0:
                            xs.append(np.log(row["k_lambda"] / rr["k_lambda"]))
                            ys.append(np.log(row["null_count"] / rr["null_count_mean"]))
            if len(xs) > 2:
                xs, ys = np.asarray(xs), np.asarray(ys)
                slope, icpt = np.polyfit(xs, ys, 1)
                r2 = 1 - np.sum((ys - slope * xs - icpt) ** 2) / np.sum((ys - ys.mean()) ** 2)
                P(f"H13: least-squares fit of ln(N_gen/N_ref) on ln(k_λ,gen/k_λ,ref) over {len(xs)} points (generators × test η × seeds): "
                  f"slope {f(float(slope))}, intercept {f(float(icpt))}, R² {f(float(r2))}; range of ln(k_λ ratio) [{f(float(xs.min()))}, {f(float(xs.max()))}].")
    P("\n### Durations (s), per seed\n")
    tn = [v for v in GENERATORS if any(v in r["times"] for r in runs.values())]
    P("| seed | " + " | ".join(tn) + " | total |")
    P("|---|" + "---|" * (len(tn) + 1))
    for s, r in runs.items():
        P(f"| {s} | " + " | ".join(f"{next(iter(r['times'][v].values())):.0f}" if v in r["times"] and isinstance(next(iter(r['times'][v].values())), (int, float)) else "–" for v in tn)
          + f" | {sum(r['durations_s']):.0f} |")
    P("")
    return out


def convergence(root: Path = R / "replications" / "e4_convergence") -> list[str]:
    """Convergence check of the E4 data: other grids and half the CFL number, same η (solver summaries)."""
    files = [("16³, CFL 1.5 (same hardware)", "e4_data_n16_same_hardware.json"), ("16³, CFL 0.75", "e4_data_cfl0.75.json"),
             ("24³, CFL 1.5", "e4_data_n24.json"), ("32³, CFL 1.5", "e4_data_n32.json")]
    base_p = R / "e4_data.json"
    if not base_p.exists() or not any((root / f).exists() for _, f in files):
        return []
    base = {v["eta"]: v for v in json.loads(base_p.read_text())["values"]}
    out = ["## E4 - convergence of the data with the grid and the time step (experiments/e4_convergence_job.sh)\n",
           "| η | run | E_u ± SE | E_B ± SE | H_M ± SE | E_B(1)/E_B | H(k = 1) | H(k = 2) | Σ_{k ≥ 3} H | energy residual |",
           "|---|---|---|---|---|---|---|---|---|---|"]

    def row(eta: float, label: str, v: dict) -> str:
        se = lambda k: v[k]["sd_between_traj"] / np.sqrt(v["n_traj"])                 # noqa: E731
        s = v.get("shells")
        sh = (f"{f(s['E_B'][0] / sum(s['E_B']))} | {f(s['H'][0])} | {f(s['H'][1])} | {f(sum(s['H'][2:]))}" if s else "– | – | – | –")
        return (f"| {eta:.5f} | {label} | {f(v['kinetic_energy']['mean'])} ± {f(se('kinetic_energy'), 2)} | "
                f"{f(v['magnetic_energy']['mean'])} ± {f(se('magnetic_energy'), 2)} | {f(v['magnetic_helicity']['mean'])} ± "
                f"{f(se('magnetic_helicity'), 2)} | {sh} | {f(v['balance_residual_total'])} |")

    etas = sorted({v["eta"] for _, fn in files if (root / fn).exists()
                   for v in json.loads((root / fn).read_text())["values"] if v["split"] == "test"}, reverse=True)
    for eta in etas:
        out.append(row(eta, "16³, CFL 1.5 (E4 data, CPU)", base[eta]))
        for label, fn in files:
            if (root / fn).exists():
                d = json.loads((root / fn).read_text())
                if d["config"].get("device", "cpu") == "cpu" and "same hardware" in label:
                    continue
                for v in d["values"]:
                    if v["eta"] == eta and (fn != "e4_data_n16_same_hardware.json" or v.get("shells")):
                        out.append(row(eta, label, v))
    out.append("\nSE: standard deviation of the trajectory means over √(number of trajectories) (24). The shell columns exist only for the "
               "runs made after the shell statistics were added to the data summary. Every run has its own random initial conditions.\n")
    return out


if __name__ == "__main__":
    import sys

    print("\n".join(section("--quick" in sys.argv)))


def polarity() -> list[str]:
    """Descriptive diagnostic of the polarity of the modes k = 1 along the reference trajectories (e4_polarity_diag.py)."""
    path = R / "e4_polarity_diag.json"
    if not path.exists():
        return []
    d = json.loads(path.read_text())
    out = ["## E4 - diagnostic: polarity of the large-scale magnetic field along the reference trajectories\n",
           "Descriptive diagnostic (experiments/e4_polarity_diag.py): no hypothesis, no threshold; data of the session container "
           "(another draw of the same law than the data of the GPU pods). For each of the three magnetic modes of wavenumber 1, "
           "whose law is symmetric under a change of sign: autocorrelation ρ(τ) of the complex amplitude over the trajectories "
           "(24 per η, 198 time units, one snapshot every 2), the lag where it falls under 1/e, and the fraction of "
           "(trajectory, mode) pairs whose projection on its initial value is negative.\n",
           "| η | set | share of E_B at k = 1 | ρ(10) | ρ(50) | ρ(100) | ρ(198) | lag of ρ = 1/e | opposite sign at the end | at some time | pairs |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e, v in d["values"].items():
        r = v["rho"]
        out.append(f"| {e} | {v['split']} | {v['share_of_E_B_at_k1']:.3f} | {r['10']:.2f} | {r['50']:.2f} | {r['100']:.2f} | {r['198']:.2f} | "
                   f"{v['tau_1_over_e']:.0f} | {v['fraction_opposite_at_end']:.2f} | {v['fraction_opposite_at_some_time']:.2f} | {v['pairs']} |")
    vals = list(d["values"].values())
    taus = [v["tau_1_over_e"] for v in vals]
    out.append(f"\nOver the 11 values of η: the lag of ρ = 1/e goes from {min(taus):.0f} to {max(taus):.0f} time units; the fraction of pairs "
               f"of opposite sign at the end of the window from {min(v['fraction_opposite_at_end'] for v in vals):.2f} to "
               f"{max(v['fraction_opposite_at_end'] for v in vals):.2f}; the modes k = 1 hold {min(v['share_of_E_B_at_k1'] for v in vals):.2f} to "
               f"{max(v['share_of_E_B_at_k1'] for v in vals):.2f} of the magnetic energy.\n")
    return out
