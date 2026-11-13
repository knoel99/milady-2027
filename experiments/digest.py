"""Numerical digest of the results (Markdown) built from the JSON files: python3 digest.py > results/digest.md

The site pages cite these values; do not copy numbers from anywhere else.
"""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent / "results"


def f(v, d=3):
    if v is None:
        return "–"
    if isinstance(v, (int,)) and not isinstance(v, bool):
        return str(v)
    if abs(v) != 0 and (abs(v) < 1e-3 or abs(v) >= 1e4):
        return f"{v:.2e}"
    return f"{v:.{d}g}"


def e1():
    p = R / "e1_gissinger.json"
    if not p.is_file():
        print("## E1 - full results missing (computation in progress)\n")
        return
    r = json.loads(p.read_text())
    res = r["summary"]
    print("## E1 - Gissinger reversal model (invariant law conditioned on Γ)\n")
    c = r["config"]
    print(f"Configuration: μ = {c['mu']}, ν = {c['nu']}; training Γ {c['G_train']}; test Γ {c['G_test']}; "
          f"{c['trajectories_per_Gamma']} trajectories per Γ, kept duration {c['kept_duration']}; iterations {c['iters']}; "
          f"seeds {c['seeds']}; {c['n_gen']} samples generated per Γ; Heun {c['heun_ode_steps']} steps; MLP {c['mlp_width']}×{c['mlp_depth']}; h_Rice = {c['h_Rice']}.\n")
    keys = [("energy", "energy dist."), ("sw1", "SW1"), ("asym", "|P(D>0)−½|"), ("liou_train_mean", "Liouville deg≤2"),
            ("liou_test_mean", "Liouville deg 3"), ("dEdt_std", "σ(dE/dt)"), ("bridge_error", "err. P(|D|<0.25)"),
            ("rice_rate_error", "err. Rice rate")]
    for split in ("test", "train"):
        print(f"\n### Means over the {split} Γ (mean over seeds)\n")
        print("| variant | " + " | ".join(k[1] for k in keys) + " | ESS/N |")
        print("|---|" + "---|" * (len(keys) + 1))
        for v, d in res.items():
            if split in d:
                print(f"| {v} | " + " | ".join(f(d[split].get(k[0])) for k in keys) + f" | {f(d[split].get('ess_frac_b'))} |")
    wt = {v: d["test"]["energy_weighted"] for v, d in res.items() if isinstance(d, dict) and "energy_weighted" in d.get("test", {})}
    if wt:
        print("\nTilted variants evaluated with their weights (no resampling), energy dist. over the test Γ: "
              + ", ".join(f"{v} {f(x)}" for v, x in wt.items()))
    print(f"\nMonte Carlo noise floors (subsample of the reference): {json.dumps(res['mc_noise_floors'])}")
    print(f"Reference: {json.dumps(res['reference'])}\n")
    print("### Data: zero crossings of D (simulation) and asymmetry of the training data\n")
    print("| Γ | simulation rate | Rice rate (ref.) | P(D>0) training |")
    print("|---|---|---|---|")
    for g, s in sorted(r["data"].items(), key=lambda t: float(t[0])):
        print(f"| {g} | {f(s['simulation_crossing_rate'])} | {f(s['rice_rate_reference'])} | {f(s.get('P(D>0)_train'), 4)} |")
    print("\n### Fine grid (model C seed 0 and F seed 0)\n")
    print("| Γ | sim. rate | Rice ref. | Rice C | Rice F | bridge ref. | bridge C | bridge F | ref. SW1 to next Γ | ref. SW1 floor |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for x in r["fine_grid"]:
        print(f"| {x['Gamma']} | {f(x['simulation_rate'])} | {f(x['rice_rate_ref'])} | {f(x['rice_rate_model'])} | "
              f"{f(x.get('rice_rate_model_F'))} | {f(x['bridge_ref'])} | {f(x['bridge_model'])} | {f(x.get('bridge_model_F'))} | "
              f"{f(x.get('ref_sw1_to_next'))} | {f(x.get('ref_sw1_floor'))} |")
    print("\nref. SW1 to next Γ: sliced W1 between the symmetrized reference laws of consecutive Γ (jump J_δ of "
          "Proposition 9, δ = half the step); floor: same Γ, two halves of the sample.")
    e1_rice(r)
    e1_detail(r)
    e1_seeds(r)
    print(f"\nTotal duration: {r['total_duration_s']:.0f} s.\n")


def e1_detail(r):
    """Per-Γ and per-seed details taken from the E1 JSON.

    For each Γ the JSON keeps [mean, sd, min, max] over the seeds and the per-seed values ("seed_values").
    """
    ev, res = r["evaluation"], r["summary"]
    ref_sd = res["reference"]["dEdt_std"]
    fine = r["fine_grid"]

    def rows(v, split):
        return ev[v][split]

    def mean(xs):
        return sum(xs) / len(xs)

    print("\n### Asymmetry |P(D>0)−½| per Γ (mean over seeds)\n")
    vs = ["A_reference", "B_augmentation", "C_equivariant"]
    print("| Γ | set | " + " | ".join(vs) + " |")
    print("|---|---|" + "---|" * len(vs))
    allg = sorted([(x["Gamma"], "training", i) for i, x in enumerate(rows(vs[0], "train"))]
                  + [(x["Gamma"], "test", i) for i, x in enumerate(rows(vs[0], "test"))])
    for g, split, i in allg:
        sp = "train" if split == "training" else "test"
        print(f"| {g} | {split} | " + " | ".join(f(rows(v, sp)[i]["asym"][0]) for v in vs) + " |")

    print("\n### Spread between seeds (mean standard deviation over the test Γ)\n")
    print("| variant | energy dist. | Liouville deg≤2 | Liouville deg 3 |")
    print("|---|---|---|---|")
    for v in ("C_equivariant", "F_stationarity_C", "F0_control_C"):
        print(f"| {v} | " + " | ".join(f(mean([x[k][1] for x in rows(v, 'test')])) for k in ("energy", "liou_train_mean", "liou_test_mean")) + " |")

    seeds = r["config"]["seeds"]

    def per_seed(v, split, k):
        """Mean over the Γ of one split, for each seed (needs the per-seed values of the JSON)."""
        rs = rows(v, split)
        return [mean([x["seed_values"][k][i] for x in rs]) for i in range(len(seeds))]

    print("\n### Per-seed σ(dE/dt)/σ_ref (mean σ over the test Γ, divided by the reference)\n")
    print("| variant | " + " | ".join(f"seed {s}" for s in seeds) + " |")
    print("|---|" + "---|" * len(seeds))
    diverged = {}
    for v in ("F_stationarity_C", "F0_control_C", "C_short", "F_stationarity_Cshort", "F0_control_Cshort"):
        vals = per_seed(v, "test", "dEdt_std")
        print(f"| {v} | " + " | ".join(f(x / ref_sd) for x in vals) + " |")
        diverged[v] = [s for s, x in zip(seeds, vals, strict=True) if not abs(x / ref_sd) < 10]
    for v, ss in diverged.items():
        if ss:
            print(f"\n{v}: seeds {ss} diverged (σ(dE/dt) more than ten times the reference).")

    print("\n### Stationarity fine-tuning on short C, seeds that did not diverge, against its control, test Γ\n")
    ok = [i for i, s in enumerate(seeds) if s not in diverged["F_stationarity_Cshort"]]
    print(f"Seeds kept: {[seeds[i] for i in ok]}.\n")
    print("| metric | F on short C, mean [min, max] | control F0, mean [min, max] over all seeds |")
    print("|---|---|---|")
    for k, lab in (("energy", "energy dist."), ("liou_train_mean", "Liouville deg≤2"), ("liou_test_mean", "Liouville deg 3")):
        a = [per_seed("F_stationarity_Cshort", "test", k)[i] for i in ok]
        b = per_seed("F0_control_Cshort", "test", k)
        cell = lambda xs: f"{f(mean(xs))} [{f(min(xs))}, {f(max(xs))}]" if xs else "–"
        print(f"| {lab} | {cell(a)} | {cell(b)} |")

    print("\n### A posteriori tilting per test Γ (mean over seeds, half b)\n")
    print("| Γ | ESS/N (A) | Liouville deg≤2: A half → A tilted | ESS/N (C) | Liouville deg≤2: C half → C tilted |")
    print("|---|---|---|---|---|")
    for i, x in enumerate(rows("D_tilting_C", "test")):
        a, am = rows("D_tilting_A", "test")[i], rows("A_reference_half", "test")[i]
        cm = rows("C_equivariant_half", "test")[i]
        print(f"| {x['Gamma']} | {f(a['ess_frac_b'])} | {f(am['liou_train_mean'][0])} → {f(a['liou_train_mean'][0])} | "
              f"{f(x['ess_frac_b'])} | {f(cm['liou_train_mean'][0])} → {f(x['liou_train_mean'][0])} |")

    below = [x for x in fine if x["simulation_rate"] == 0]
    g1 = [x for x in fine if abs(x["Gamma"] - 1.0) < 1e-9][0]
    mc = max(below, key=lambda x: x["rice_rate_model"])
    mf = max(below, key=lambda x: x["rice_rate_model_F"])
    print(f"\nSpurious crossings below the threshold (fine grid, zero simulated rate): at most {f(mc['rice_rate_model'])} for C "
          f"(Γ = {mc['Gamma']}) and {f(mf['rice_rate_model_F'])} for F (Γ = {mf['Gamma']}), i.e. "
          f"{f(100 * mc['rice_rate_model'] / g1['simulation_rate'], 2)} % and {f(100 * mf['rice_rate_model_F'] / g1['simulation_rate'], 2)} % "
          f"of the simulated rate at Γ = 1 ({f(g1['simulation_rate'])}).")

    print("\n### Durations per variant and per seed (s)\n")
    print("| variant | seed | training or fine-tuning | generation per 1000 samples |")
    print("|---|---|---|---|")
    for v, seeds in r["training"].items():
        for s, d in seeds.items():
            t = d.get("training_time_s", d.get("finetuning_time_s"))
            print(f"| {v} | {s} | {t:.0f} | {f(d.get('generation_time_s_per_1000'), 2)} |")


def e1_rice(r):
    """Errors of Rice's formula on the fine grid (the percentages quoted in the report), and floors."""
    fg = r["fine_grid"]
    near = [x for x in fg if 0.865 - 1e-9 <= x["Gamma"] <= 0.885 + 1e-9]
    above = [x for x in fg if x["Gamma"] >= 0.89 - 1e-9]
    below = [x for x in fg if x["Gamma"] <= 0.86 + 1e-9]

    def cum(rows, key):
        den = sum(x["simulation_rate"] for x in rows)
        return sum(abs(x[key] - x["simulation_rate"]) for x in rows) / den if den else None

    print("\n### Rice's formula on the fine grid: relative errors\n")
    print("Cumulative error = Σ|Rice − count| / Σ count over the range; near threshold 0.865 ≤ Γ ≤ 0.885, above Γ ≥ 0.89. "
          f"Models C and F: seed {r['config']['seeds'][0]} only, {r['config'].get('n_big', 'n_big')} samples per Γ.\n")
    print("| distribution | cumulative error near threshold | cumulative error above | mean pointwise error above | max pointwise error above (Γ) |")
    print("|---|---|---|---|---|")
    for key, lab in (("rice_rate_ref", "reference"), ("rice_rate_model", "model C"), ("rice_rate_model_F", "model F")):
        if key not in fg[0]:
            continue
        pts = [(abs(x[key] - x["simulation_rate"]) / x["simulation_rate"], x["Gamma"]) for x in above if x["simulation_rate"] > 0]
        worst = max(pts) if pts else (None, None)
        mean_pt = sum(p for p, _ in pts) / len(pts) if pts else None
        print(f"| {lab} | {f(cum(near, key))} | {f(cum(above, key))} | {f(mean_pt)} | {f(worst[0])} ({worst[1]}) |")
    top = max(fg, key=lambda x: x["Gamma"])
    spur = max(x["rice_rate_model"] for x in below) if below else None
    print(f"\nSpurious crossings of model C below the threshold (Γ ≤ 0.86): max Rice rate {f(spur)}; "
          f"ratio to its value at Γ = {top['Gamma']}: {f(spur / top['rice_rate_model']) if spur is not None and top['rice_rate_model'] else '–'}.")
    n = r["config"]["n_gen"]
    print(f"Binomial floor of the asymmetry |P(D>0) − ½| for N = {n} samples: E|p̂ − ½| ≈ 1/√(2πN) = {f((2 * 3.141592653589793 * n) ** -0.5)}.")


def spread(values):
    """mean ± standard deviation (ddof = 1) [min, max] of a list of per-seed values."""
    n = len(values)
    m = sum(values) / n
    sd = (sum((v - m) ** 2 for v in values) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return f"{f(m)} ± {f(sd)} [{f(min(values))}, {f(max(values))}]"


def paired(a, b):
    """Paired differences a − b over the seeds: (values, mean, standard error with ddof = 1, count of a > b)."""
    d = [x - y for x, y in zip(a, b, strict=True)]
    n = len(d)
    m = sum(d) / n
    se = ((sum((x - m) ** 2 for x in d) / (n - 1)) ** 0.5 / n ** 0.5) if n > 1 else 0.0
    return d, m, se, sum(x > 0 for x in d)


def paired_row(label, a, b):
    d, m, se, k = paired(a, b)
    z = f"{m / se:.1f}" if se > 0 else "–"
    return f"| {label} | " + ", ".join(f(x) for x in d) + f" | {f(m)} ± {f(se)} | {z} | {k} of {len(d)} |"


def e1_seeds(r):
    """Dispersion across seeds of the means over the test Γ (runs that store per-seed values)."""
    seeds = r["config"]["seeds"]
    ev = r["evaluation"]
    if len(seeds) < 2 or "seed_values" not in ev["A_reference"]["test"][0]:
        return
    keys = [("energy", "energy dist."), ("sw1", "SW1"), ("liou_test_mean", "Liouville deg 3"), ("asym", "|P(D>0)−½|")]
    print(f"\n### Across seeds: mean over the test Γ, then mean ± sd [min, max] over {len(seeds)} seeds {seeds}\n")
    print("| variant | " + " | ".join(k[1] for k in keys) + " |")
    print("|---|" + "---|" * len(keys))
    for v, d in ev.items():
        rows = d["test"]
        cells = [spread([sum(row["seed_values"][k][i] for row in rows) / len(rows) for i in range(len(seeds))]) for k, _ in keys]
        print(f"| {v} | " + " | ".join(cells) + " |")

    def ps(v, k):
        rows = ev[v]["test"]
        return [sum(row["seed_values"][k][i] for row in rows) / len(rows) for i in range(len(seeds))]

    print(f"\n### Paired comparisons over the seeds {seeds} (means over the test Γ; SE = sd(ddof = 1)/√n)\n")
    print("| comparison | per-seed differences | mean ± SE | mean/SE | seeds with a positive difference |")
    print("|---|---|---|---|---|")
    print(paired_row("energy dist.: A_reference − C_equivariant (H1)", ps("A_reference", "energy"), ps("C_equivariant", "energy")))
    print(paired_row("Liouville deg 3: F0_control_C − F_stationarity_C (H2)", ps("F0_control_C", "liou_test_mean"), ps("F_stationarity_C", "liou_test_mean")))
    print(paired_row("Liouville deg≤2: F0_control_C − F_stationarity_C", ps("F0_control_C", "liou_train_mean"), ps("F_stationarity_C", "liou_train_mean")))
    print(paired_row("energy dist.: F_stationarity_C − F0_control_C", ps("F_stationarity_C", "energy"), ps("F0_control_C", "energy")))
    ratio = (sum(ps("F_stationarity_C", "energy")) / sum(ps("F0_control_C", "energy")))
    print(f"\nRatio of the mean energy distances F_stationarity_C / F0_control_C: {f(ratio)}.")

    print("\n### Per seed, test Γ: stationarity fine-tuning of C against its control, and per-sample projection\n")
    print("| quantity | " + " | ".join(f"seed {s}" for s in seeds) + " |")
    print("|---|" + "---|" * len(seeds))
    for lab, k in (("energy dist.", "energy"), ("Liouville deg≤2", "liou_train_mean"), ("Liouville deg 3", "liou_test_mean")):
        for v in ("F_stationarity_C", "F0_control_C"):
            print(f"| {lab}, {v} | " + " | ".join(f(x) for x in ps(v, k)) + " |")
    for lab, a, b in (("A_reference / C_equivariant, energy dist.", "A_reference", "C_equivariant"),
                      ("E_projection_C / C_equivariant, energy dist.", "E_projection_C", "C_equivariant")):
        print(f"| {lab} | " + " | ".join(f(x / y) for x, y in zip(ps(a, "energy"), ps(b, "energy"), strict=True)) + " |")
    print("\nRice error column of the tables: |Rice rate averaged over the seeds − simulated rate|, then mean over the Γ.")


def e2_seeds():
    """E2 runs with several seeds: e2_mhd2d.json (seed 0) and e2_mhd2d_s<k>.json."""
    runs = [R / "e2_mhd2d.json"] + sorted(R.glob("e2_mhd2d_s*.json"), key=lambda p: int(p.stem.split("_s")[-1]))
    runs = [json.loads(p.read_text()) for p in runs if p.is_file()]
    if len(runs) < 2:
        return
    seeds = [x["config"].get("seed", 0) for x in runs]
    keys = [("energy_distance_features", "energy dist."), ("div_rel_u", "rel. div. u"), ("balance_residual_energy", "energy residual"),
            ("std_diss_rel", "σ(D)/σ_ref")]
    print(f"\n### Across seeds: means over the test η, mean ± sd [min, max] over {len(runs)} seeds {seeds}\n")
    print("| variant | " + " | ".join(k[1] for k in keys) + " |")
    print("|---|" + "---|" * len(keys))
    for v in runs[0]["summary"]:
        if v == "in_law":
            continue
        print(f"| {v} | " + " | ".join(spread([x["summary"][v]["test"][k] for x in runs]) for k, _ in keys) + " |")
    for m in ("base", "tilting", "rescaling"):
        print(f"| in law: {m} | " + " | ".join(spread([x["summary"]["in_law"][m]["test"][k] for x in runs]) for k, _ in keys) + " |")

    keys2 = [("err_Eu_rel", "err. E_u"), ("err_Eb_rel", "err. E_B"), ("spectrum_error_log10", "err. spectrum"), ("balance_residual_A2", "⟨a²⟩ residual")]
    print(f"\n### Across seeds, other metrics: means over the test η, mean ± sd [min, max] over {len(runs)} seeds\n")
    print("| variant | " + " | ".join(k[1] for k in keys2) + " |")
    print("|---|" + "---|" * len(keys2))
    for v in ("V1_penalty", "V4_potentials", "V5_potentials_stat", "V5_control"):
        print(f"| {v} | " + " | ".join(spread([x["summary"][v]["test"][k] for x in runs]) for k, _ in keys2) + " |")
    for m in ("base", "tilting", "rescaling"):
        print(f"| in law: {m} | " + " | ".join(spread([x["summary"]["in_law"][m]["test"][k] for x in runs]) for k, _ in keys2) + " |")
    print("\nMean ESS/N of the tilting over the eleven η, per seed: " + ", ".join(f(x["summary"]["in_law"]["ess_frac_b_mean"]) for x in runs))

    print(f"\n### Paired comparisons over the seeds {seeds} (means over the test η; SE = sd(ddof = 1)/√n)\n")
    print("| comparison | per-seed differences | mean ± SE | mean/SE | seeds with a positive difference |")
    print("|---|---|---|---|---|")
    ed = lambda v: [x["summary"][v]["test"]["energy_distance_features"] for x in runs]
    print(paired_row("energy dist.: V5_control − V5_potentials_stat (H3)", ed("V5_control"), ed("V5_potentials_stat")))
    print(paired_row("energy dist.: V2_final_projection − V3_projected_flow", ed("V2_final_projection"), ed("V3_projected_flow")))
    print(paired_row("energy dist.: V4_potentials − V3_projected_flow", ed("V4_potentials"), ed("V3_projected_flow")))

    print("\n### Per test η, over the seeds: V5 against its control, and ESS/N of the tilting\n")
    print("| η | control, seed mean | V5, seed mean | control − V5: mean ± SE | mean/SE | seeds where V5 is lower | ESS/N per seed |")
    print("|---|---|---|---|---|---|---|")
    test = runs[0]["evaluation"]["V5_control"]["test"]
    for i, row in enumerate(test):
        a = [x["evaluation"]["V5_control"]["test"][i]["energy_distance_features"] for x in runs]
        b = [x["evaluation"]["V5_potentials_stat"]["test"][i]["energy_distance_features"] for x in runs]
        d, m, se, k = paired(a, b)
        key = min(runs[0]["in_law"], key=lambda e: abs(float(e) - row["eta"]))
        ess = [x["in_law"][key]["ess_frac_b"] for x in runs]
        print(f"| {row['eta']:.5f} | {f(sum(a) / len(a))} | {f(sum(b) / len(b))} | {f(m)} ± {f(se)} | {m / se:.1f} | {k} of {len(d)} | "
              + ", ".join(f(e) for e in ess) + " |")


def e2():
    p = R / "e2_mhd2d.json"
    if not p.is_file():
        print("## E2 - missing\n")
        return
    r = json.loads(p.read_text())
    res, c = r["summary"], r["config"]
    print("## E2 - forced 2D MHD, generation conditioned on η\n")
    print(f"Configuration: N = {c['N']}, ν = {c['nu']}, α = {c['alpha']}, forcing band {c['kf']}; training η "
          f"{[round(e, 5) for e in c['eta_train']]}; test η {[round(e, 5) for e in c['eta_test']]}; {c['modes']} independent "
          f"Fourier modes; dimension {c['dim_potentials']} (potentials) or {c['dim_components']} (components); MLP width {c['width']}, "
          f"{c['iters']} iterations; {c['n_gen']} samples per η; {c['n_train_per_eta']} training snapshots per η; "
          f"injection (Itô) ε_u, ε_b, ε_{{a²}} = {[round(x, 5) for x in c['injection']]}.\n")
    keys = [("div_rel_u", "rel. div. u"), ("div_rel_b", "rel. div. B"), ("spectrum_error_log10", "err. spectrum"),
            ("err_Eu_rel", "err. E_u"), ("err_Eb_rel", "err. E_B"), ("balance_residual_energy", "energy residual"),
            ("balance_residual_Hc", "H_c residual"), ("balance_residual_A2", "⟨a²⟩ residual"), ("std_diss_rel", "σ(D)/σ_ref"),
            ("energy_distance_features", "energy dist.")]
    for split in ("test", "train"):
        print(f"\n### Means over the {split} η (seed 0)\n")
        print("| variant | " + " | ".join(k[1] for k in keys) + " |")
        print("|---|" + "---|" * len(keys))
        for v, d in res.items():
            if v == "in_law":
                continue
            print(f"| {v} | " + " | ".join(f(d[split][k[0]]) for k in keys) + " |")
        for m in ("base", "tilting", "rescaling"):
            print(f"| in law: {m} (V4, half b) | " + " | ".join(f(res['in_law'][m][split][k[0]]) for k in keys) + " |")
    print(f"\nMean ESS/N of the tilting (seed 0): {f(res['in_law']['ess_frac_b_mean'])}")
    if "tilting_weighted_energy_distance" in res["in_law"]:
        w = res["in_law"]["tilting_weighted_energy_distance"]
        print(f"Tilting evaluated with its weights (no resampling), energy dist.: test {f(w['test'])}, train {f(w['train'])}")
    e2_detail(r)
    e2_seeds()
    print("\nTimes: " + json.dumps({k: {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()}
                                     for k, v in r["variants"].items()}))
    print(f"\nTotal duration: {r['total_duration_s']:.0f} s.\n")


def e2_detail(r):
    """Detail per value of η (a single seed per variant in E2)."""
    ev, el = r["evaluation"], r["in_law"]
    vs = ["V0_free", "V1_penalty", "V4_potentials", "V5_control", "V5_potentials_stat"]
    rows = sorted([(x["eta"], "training", i) for i, x in enumerate(ev[vs[0]]["train"])]
                  + [(x["eta"], "test", i) for i, x in enumerate(ev[vs[0]]["test"])])
    for k, lab in (("energy_distance_features", "energy distance"), ("balance_residual_energy", "signed residual of the energy balance"),
                   ("err_Eb_rel", "relative error on E_B")):
        print(f"\n### Per η: {lab}\n")
        print("| η | set | " + " | ".join(vs) + " |")
        print("|---|---|" + "---|" * len(vs))
        for eta, split, i in rows:
            sp = "train" if split == "training" else "test"
            print(f"| {eta:.5f} | {split} | " + " | ".join(f(ev[v][sp][i][k]) for v in vs) + " |")
    print("\n### Per η: law constraints on V4 (half b)\n")
    print("| η | Pm = ν/η | set | ESS/N | base dist. | tilting dist. | rescaling dist. | base residual | tilting residual |")
    print("|---|---|---|---|---|---|---|---|---|")
    for key, x in sorted(el.items(), key=lambda t: float(t[0])):
        print(f"| {float(key):.5f} | {f(r['config']['nu'] / float(key))} | {'training' if x['split'] == 'train' else 'test'} | {f(x['ess_frac_b'])} | "
              f"{f(x['base']['energy_distance_features'])} | {f(x['tilting']['energy_distance_features'])} | "
              f"{f(x['rescaling']['energy_distance_features'])} | {f(x['base']['balance_residual_energy'])} | "
              f"{f(x['tilting']['balance_residual_energy'])} |")


def e3():
    p = R / "e3_abc.json"
    if not p.is_file():
        return
    r = json.loads(p.read_text())
    print("## E3 - ABC kinematic dynamo (A = B = C = 1, Rm = 1/η, N = 32)\n")
    print("| Rm | γ | γ (last quarter) | rel. div. |")
    print("|---|---|---|---|")
    for t in r["rates"]:
        print(f"| {t['Rm']} | {f(t['lambda'], 4)} | {f(t['lambda_last_quarter'], 4)} | {f(t['div_rel'])} |")
    print(f"\nConvergence N = 48: {r['convergence']}")
    print(f"Interpolated thresholds: {[round(s, 2) for s in r['interpolated_thresholds']]}")
    print(f"Duration: {r['duration_s']:.0f} s.\n")


def e4():
    from e4_digest import section

    from e4_digest import R as R4
    from e4_digest import convergence

    lines = section()
    reps = [("e4_nongauss", "tests H25-H27 of the structure beyond a Gaussian law (production split with a jackknife, restart anchored on the "
                            "reference energy up to 16 tau, Gaussianised W9 with a null control): groups D, E, G and N on a RunPod GPU pod, "
                            "own regenerated data"),
            ("e4_nongauss_indep", "the same tests H25-H27 on the data of the independent replication (E4_DATA_SEED=100)"),
            ("e4_final_long", "long trainings: groups D, E and L (W9L, W11L: 8 times the iterations) on a RunPod GPU pod, own regenerated data"),
            ("e4_mech", "Gaussian law with the inter-mode covariance (G1) and loss and tilting on the model with the affine term: groups D, E, G "
                        "and M on a RunPod GPU pod, own regenerated data; restart drift recorded at four times"),
            ("e4_g1indep", "the two Gaussian laws and the model with the affine term (groups D and G) on the data of the independent "
                           "replication (E4_DATA_SEED=100)"),
            ("e4_scan2", "second width scan of H21: groups D and S, 5 seeds on three GPU pods (split by seed)"),
            ("e4_final_scan", "first width scan of H21 (A100, cut by its time limit: S_w5632 and S_w512_long on 2 seeds only)"),
            ("e4_indep", "independent replication: reference data regenerated with other seeds of the initial conditions (E4_DATA_SEED=100), "
                         "groups A to E"),
            ("e4_gpu", "first GPU run of the registered groups A and B (the run reviewed for H4-H14; same data and model seeds as the main run)"),
            ("e4_cpu", "seeds 0 and 1 on the CPU of the session's container (first computation of the groups C, D and E; two seeds only)")]
    for name, what in reps:
        root = R4 / "replications" / name
        if (root / "e4_reference.json").exists():
            lines += section(root=root, replication=what)
    lines += convergence()
    if lines:
        print("\n".join(lines))


if __name__ == "__main__":
    print("# Results digest (generated by experiments/digest.py)\n")
    e1(); e2(); e3(); e4()
