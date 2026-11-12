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
              "W4s_potentials_sym", "W5_stationarity", "W5_control", "W6_diffusion", "W4c_potentials_smooth"]
POST = ["W7_tilting", "W8_rescaling", "W5_stationarity_half", "W5_control_half"]
KEYS = [("ed_ratio", "ED / floor", False), ("div_rel_b_mean", "rel. div. B", False),
        ("balance_residual_total", "|energy residual|", True), ("spec_err_b_l2", "err. E_B(k)", False),
        ("hel_m_err_rel", "err. H_M", False), ("null_count_err_rel", "err. nulls", False),
        ("restart_drift_eb", "restart drift E_B", False), ("hc_sign_asym", "|P(H_c>0)−½|", False),
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
    extra = root / f"e4_mhd3d{tag}_s{seed}_C.json"
    if all(p.exists() for p in parts):
        data = [json.loads(p.read_text()) for p in parts]
    elif whole.exists():
        data = [json.loads(whole.read_text())]
    else:
        return None
    if extra.exists():
        data.append(json.loads(extra.read_text()))
    out = {"config": {**data[0]["config"], "group": "merged"}, "evaluation": {}, "times": {}, "h14": [], "h12": [],
           "durations_s": [d["total_duration_s"] for d in data]}
    for d in data:
        out["evaluation"].update(d["evaluation"])
        out["times"].update(d["times"])
        out["h14"] += d["h14"]
        out["h12"] += d["h12"]
    path = root / f"e4_mhd3d{tag}_s{seed}.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return path


def load(quick: bool = False, root: Path = R, tag: str = "") -> dict[int, dict]:
    tag = tag + ("_quick" if quick else "")
    out = {}
    for s in SEEDS:
        merge(s, tag, root)
        p = root / f"e4_mhd3d{tag}_s{s}.json"
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


def paired_row(label: str, a: np.ndarray, b: np.ndarray) -> str:
    d, m, se = paired(a, b)
    return (f"| {label} | {', '.join(f(x) for x in d)} | {f(m)} ± {f(se)} | {f(m / se, 2) if se > 0 else '–'} | "
            f"{int((d > 0).sum())} of {len(d)} |")


def select(runs: dict) -> dict:
    """Generator with the lowest validation energy-distance ratio (mean over the seeds)."""
    val = {v: float(np.nanmean(per_seed(runs, v, "ed_ratio", "val"))) for v in GENERATORS
           if not np.all(np.isnan(per_seed(runs, v, "ed_ratio", "val")))}
    best = min(val, key=val.get)
    return {"variant": best, "criterion": "lowest energy-distance ratio on the validation η, mean over the seeds",
            "seeds": sorted(runs), "val_ed_ratio": val}


def section(quick: bool = False, root: Path = R, replication: str | None = None, run_tag: str = "") -> list[str]:
    """E4 section of the digest; with ``replication``, the same tables for an independent replication
    stored under ``root`` or for a run with another protocol (``run_tag``, e.g. "_cs0.5"): no selection
    file is written, the title says what the replication is."""
    tag = "_quick" if quick else ""
    runs = load(quick, root, run_tag)
    out: list[str] = []
    P = out.append
    dp, rp = root / f"e4_data{tag}.json", root / f"e4_reference{tag}.json"
    if not dp.exists():
        return out
    data = json.loads(dp.read_text())
    c = data["config"]
    if replication:
        P(f"## E4 - replication: {replication}\n")
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
    P(f"\n### Selected generator: {sv}\n")
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
        P(paired_row("ED ratio: W7_tilting − W5_stationarity_half (H8)", ed("W7_tilting"), ed("W5_stationarity_half")))
        P(paired_row("ED ratio: W7_tilting − W5_control_half", ed("W7_tilting"), ed("W5_control_half")))
        P(paired_row("polarity asymmetry: W4_potentials − W4s_potentials_sym (H9)",
                     per_seed(runs, "W4_potentials", "hc_sign_asym"), per_seed(runs, "W4s_potentials_sym", "hc_sign_asym")))
        P(paired_row("ED ratio: W4s_potentials_sym − W4_potentials (H9)", ed("W4s_potentials_sym"), ed("W4_potentials")))
        P(paired_row("ED ratio: W6_diffusion − W4_potentials (H10)", ed("W6_diffusion"), ed("W4_potentials")))
        if not np.all(np.isnan(ed("W4c_potentials_smooth"))):
            P(paired_row("ED ratio: W4_potentials − W4c_potentials_smooth (H15)", ed("W4_potentials"), ed("W4c_potentials_smooth")))
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
        P(f"| {s} | " + " | ".join(f"{next(iter(r['times'][v].values())):.0f}" if v in r["times"] else "–" for v in tn)
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
