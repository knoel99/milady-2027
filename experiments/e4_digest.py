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
# G0 has no network: it is the baseline to beat, not a candidate for the selected generator (the C1 note of
# race/teams/claude/objectives.toml names the model family: conditional flow matching on the Fourier modes).
CANDIDATES = [v for v in GENERATORS if not v.startswith(("G0_", "G1_", "G2_", "G3_"))]          # learned generators only
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
        if not any((root / f"e4_mhd3d{tag}_s{seed}_{g}.json").exists() for g in ("C", "D", "E", "L", "S", "G", "M", "N")):
            return None
    if all(p.exists() for p in parts):
        data = [json.loads(p.read_text()) for p in parts]
    elif whole.exists():
        data = [json.loads(whole.read_text())]
    else:
        return None
    for g in ("C", "D", "E", "L", "S", "G", "M", "N"):                      # optional groups, added after the first runs
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


def select(runs: dict) -> dict:
    """Generator with the lowest validation energy-distance ratio (mean over the seeds)."""
    val = {v: float(np.nanmean(per_seed(runs, v, "ed_ratio", "val"))) for v in GENERATORS
           if not np.all(np.isnan(per_seed(runs, v, "ed_ratio", "val")))}
    best = min((v for v in val if v in CANDIDATES), key=val.get)
    return {"variant": best, "criterion": "flow-matching or diffusion generator with the lowest energy-distance ratio on the "
            "validation η, mean over the seeds (the Gaussian laws G0, G1 and G2 are not candidates)",
            "seeds": sorted(runs), "val_ed_ratio": val}


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
                      f"η = {e:.4f}: {f(float((g2e[e] - w9e[e]).mean()))} ± {f(float((g2e[e] - w9e[e]).std(ddof=1) / np.sqrt(len(w9e[e]))))}"
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
