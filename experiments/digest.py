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
    print(f"\nMonte Carlo noise floors (subsample of the reference): {json.dumps(res['mc_noise_floors'])}")
    print(f"Reference: {json.dumps(res['reference'])}\n")
    print("### Data: zero crossings of D (simulation) and asymmetry of the training data\n")
    print("| Γ | simulation rate | Rice rate (ref.) | P(D>0) training |")
    print("|---|---|---|---|")
    for g, s in sorted(r["data"].items(), key=lambda t: float(t[0])):
        print(f"| {g} | {f(s['simulation_crossing_rate'])} | {f(s['rice_rate_reference'])} | {f(s.get('P(D>0)_train'), 4)} |")
    print("\n### Fine grid (model C seed 0 and F seed 0)\n")
    print("| Γ | sim. rate | Rice ref. | Rice C | Rice F | bridge ref. | bridge C | bridge F |")
    print("|---|---|---|---|---|---|---|---|")
    for x in r["fine_grid"]:
        print(f"| {x['Gamma']} | {f(x['simulation_rate'])} | {f(x['rice_rate_ref'])} | {f(x['rice_rate_model'])} | "
              f"{f(x.get('rice_rate_model_F'))} | {f(x['bridge_ref'])} | {f(x['bridge_model'])} | {f(x.get('bridge_model_F'))} |")
    e1_detail(r)
    e1_seeds(r)
    print(f"\nTotal duration: {r['total_duration_s']:.0f} s.\n")


def e1_detail(r):
    """Per-Γ and per-seed details taken from the E1 JSON.

    For each Γ the JSON keeps the mean and standard deviation (ddof = 0) of the two seeds: the two per-seed values
    are therefore mean ± standard deviation, without knowing which belongs to which seed. We publish the envelope
    ("low" = mean - std, "high" = mean + std); the mean over Γ for each seed lies
    between the mean of the low values and that of the high values.
    """
    ev, res = r["evaluation"], r["summary"]
    ref_sd = res["reference"]["dEdt_std"]
    fine = r["fine_grid"]

    def rows(v, split):
        return ev[v][split]

    def mean(xs):
        return sum(xs) / len(xs)

    def env(v, split, k):
        lo = mean([x[k][0] - x[k][1] for x in rows(v, split)])
        hi = mean([x[k][0] + x[k][1] for x in rows(v, split)])
        return lo, hi

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

    print("\n### Per-seed envelope of σ(dE/dt)/σ_ref (mean σ over the test Γ, divided by the reference)\n")
    print("| variant | low seed | high seed |")
    print("|---|---|---|")
    for v in ("F_stationarity_C", "F0_control_C", "C_short", "F_stationarity_Cshort", "F0_control_Cshort"):
        lo, hi = env(v, "test", "dEdt_std")
        print(f"| {v} | {f(lo / ref_sd)} | {f(hi / ref_sd)} |")
    print("\nOn short C, seed 1 diverged: at each Γ its value is the high one, which separates the seeds.")

    print("\n### Short C, seed 0 (low value at each Γ) against its control, test Γ\n")
    print("| metric | F on short C, seed 0 | control F0, mean over seeds | control F0, high seed |")
    print("|---|---|---|---|")
    for k, lab in (("energy", "energy dist."), ("liou_train_mean", "Liouville deg≤2"), ("liou_test_mean", "Liouville deg 3")):
        lo, _ = env("F_stationarity_Cshort", "test", k)
        _, hi0 = env("F0_control_Cshort", "test", k)
        print(f"| {lab} | {f(lo)} | {f(res['F0_control_Cshort']['test'][k])} | {f(hi0)} |")

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


def spread(values):
    """mean ± standard deviation (ddof = 1) [min, max] of a list of per-seed values."""
    n = len(values)
    m = sum(values) / n
    sd = (sum((v - m) ** 2 for v in values) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return f"{f(m)} ± {f(sd)} [{f(min(values))}, {f(max(values))}]"


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
        print(f"\n### Means over the {split} η\n")
        print("| variant | " + " | ".join(k[1] for k in keys) + " |")
        print("|---|" + "---|" * len(keys))
        for v, d in res.items():
            if v == "in_law":
                continue
            print(f"| {v} | " + " | ".join(f(d[split][k[0]]) for k in keys) + " |")
        for m in ("base", "tilting", "rescaling"):
            print(f"| in law: {m} (V4, half b) | " + " | ".join(f(res['in_law'][m][split][k[0]]) for k in keys) + " |")
    print(f"\nMean ESS/N of the tilting: {f(res['in_law']['ess_frac_b_mean'])}")
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
    print("| Rm | λ | λ (last quarter) | rel. div. |")
    print("|---|---|---|---|")
    for t in r["rates"]:
        print(f"| {t['Rm']} | {f(t['lambda'], 4)} | {f(t['lambda_last_quarter'], 4)} | {f(t['div_rel'])} |")
    print(f"\nConvergence N = 48: {r['convergence']}")
    print(f"Interpolated thresholds: {[round(s, 2) for s in r['interpolated_thresholds']]}")
    print(f"Duration: {r['duration_s']:.0f} s.\n")


if __name__ == "__main__":
    print("# Results digest (generated by experiments/digest.py)\n")
    e1(); e2(); e3()
