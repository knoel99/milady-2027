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
    res = r["resume"]
    print("## E1 - Gissinger reversal model (invariant law conditioned on Γ)\n")
    c = r["config"]
    print(f"Configuration: μ = {c['mu']}, ν = {c['nu']}; training Γ {c['G_train']}; test Γ {c['G_test']}; "
          f"{c['trajectoires_par_Gamma']} trajectories per Γ, kept duration {c['duree_gardee']}; iterations {c['iters']}; "
          f"seeds {c['seeds']}; {c['n_gen']} samples generated per Γ; Heun {c['pas_ODE_Heun']} steps; MLP {c['largeur_MLP']}×{c['profondeur_MLP']}; h_Rice = {c['h_Rice']}.\n")
    keys = [("energie", "energy dist."), ("sw1", "SW1"), ("asym", "|P(D>0)−½|"), ("liou_train_moy", "Liouville deg≤2"),
            ("liou_test_moy", "Liouville deg 3"), ("dEdt_std", "σ(dE/dt)"), ("erreur_pont", "err. P(|D|<0.25)"),
            ("erreur_taux_rice", "err. Rice rate")]
    for split in ("test", "train"):
        print(f"\n### Means over the {split} Γ (mean over seeds)\n")
        print("| variant | " + " | ".join(k[1] for k in keys) + " | ESS/N |")
        print("|---|" + "---|" * (len(keys) + 1))
        for v, d in res.items():
            if split in d:
                print(f"| {v} | " + " | ".join(f(d[split].get(k[0])) for k in keys) + f" | {f(d[split].get('ess_frac_b'))} |")
    print(f"\nMonte Carlo noise floors (subsample of the reference): {json.dumps(res['planchers_bruit_MC'])}")
    print(f"Reference: {json.dumps(res['reference'])}\n")
    print("### Data: zero crossings of D (simulation) and asymmetry of the training data\n")
    print("| Γ | simulation rate | Rice rate (ref.) | P(D>0) training |")
    print("|---|---|---|---|")
    for g, s in sorted(r["donnees"].items(), key=lambda t: float(t[0])):
        print(f"| {g} | {f(s['taux_passages_simulation'])} | {f(s['taux_rice_reference'])} | {f(s.get('P(D>0)_train'), 4)} |")
    print("\n### Fine grid (model C seed 0 and F seed 0)\n")
    print("| Γ | sim. rate | Rice ref. | Rice C | Rice F | bridge ref. | bridge C | bridge F |")
    print("|---|---|---|---|---|---|---|---|")
    for x in r["grille_fine"]:
        print(f"| {x['Gamma']} | {f(x['taux_simulation'])} | {f(x['taux_rice_ref'])} | {f(x['taux_rice_modele'])} | "
              f"{f(x.get('taux_rice_modele_F'))} | {f(x['pont_ref'])} | {f(x['pont_modele'])} | {f(x.get('pont_modele_F'))} |")
    e1_detail(r)
    print(f"\nTotal duration: {r['duree_totale_s']:.0f} s.\n")


def e1_detail(r):
    """Per-Γ and per-seed details taken from the E1 JSON.

    For each Γ the JSON keeps the mean and standard deviation (ddof = 0) of the two seeds: the two per-seed values
    are therefore mean ± standard deviation, without knowing which belongs to which seed. We publish the envelope
    ("low" = mean - std, "high" = mean + std); the mean over Γ for each seed lies
    between the mean of the low values and that of the high values.
    """
    ev, res = r["evaluation"], r["resume"]
    ref_sd = res["reference"]["dEdt_std"]
    fine = r["grille_fine"]

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
    for v in ("C_equivariant", "F_stationnarite_C", "F0_temoin_C"):
        print(f"| {v} | " + " | ".join(f(mean([x[k][1] for x in rows(v, 'test')])) for k in ("energie", "liou_train_moy", "liou_test_moy")) + " |")

    print("\n### Per-seed envelope of σ(dE/dt)/σ_ref (mean σ over the test Γ, divided by the reference)\n")
    print("| variant | low seed | high seed |")
    print("|---|---|---|")
    for v in ("F_stationnarite_C", "F0_temoin_C", "C_court", "F_stationnarite_Ccourt", "F0_temoin_Ccourt"):
        lo, hi = env(v, "test", "dEdt_std")
        print(f"| {v} | {f(lo / ref_sd)} | {f(hi / ref_sd)} |")
    print("\nOn short C, seed 1 diverged: at each Γ its value is the high one, which separates the seeds.")

    print("\n### Short C, seed 0 (low value at each Γ) against its control, test Γ\n")
    print("| metric | F on short C, seed 0 | control F0, mean over seeds | control F0, high seed |")
    print("|---|---|---|---|")
    for k, lab in (("energie", "energy dist."), ("liou_train_moy", "Liouville deg≤2"), ("liou_test_moy", "Liouville deg 3")):
        lo, _ = env("F_stationnarite_Ccourt", "test", k)
        _, hi0 = env("F0_temoin_Ccourt", "test", k)
        print(f"| {lab} | {f(lo)} | {f(res['F0_temoin_Ccourt']['test'][k])} | {f(hi0)} |")

    print("\n### A posteriori tilting per test Γ (mean over seeds, half b)\n")
    print("| Γ | ESS/N (A) | Liouville deg≤2: A half → A tilted | ESS/N (C) | Liouville deg≤2: C half → C tilted |")
    print("|---|---|---|---|---|")
    for i, x in enumerate(rows("D_inclinaison_C", "test")):
        a, am = rows("D_inclinaison_A", "test")[i], rows("A_reference_moitie", "test")[i]
        cm = rows("C_equivariant_moitie", "test")[i]
        print(f"| {x['Gamma']} | {f(a['ess_frac_b'])} | {f(am['liou_train_moy'][0])} → {f(a['liou_train_moy'][0])} | "
              f"{f(x['ess_frac_b'])} | {f(cm['liou_train_moy'][0])} → {f(x['liou_train_moy'][0])} |")

    below = [x for x in fine if x["taux_simulation"] == 0]
    g1 = [x for x in fine if abs(x["Gamma"] - 1.0) < 1e-9][0]
    mc = max(below, key=lambda x: x["taux_rice_modele"])
    mf = max(below, key=lambda x: x["taux_rice_modele_F"])
    print(f"\nSpurious crossings below the threshold (fine grid, zero simulated rate): at most {f(mc['taux_rice_modele'])} for C "
          f"(Γ = {mc['Gamma']}) and {f(mf['taux_rice_modele_F'])} for F (Γ = {mf['Gamma']}), i.e. "
          f"{f(100 * mc['taux_rice_modele'] / g1['taux_simulation'], 2)} % and {f(100 * mf['taux_rice_modele_F'] / g1['taux_simulation'], 2)} % "
          f"of the simulated rate at Γ = 1 ({f(g1['taux_simulation'])}).")

    print("\n### Durations per variant and per seed (s)\n")
    print("| variant | seed | training or fine-tuning | generation per 1000 samples |")
    print("|---|---|---|---|")
    for v, seeds in r["entrainement"].items():
        for s, d in seeds.items():
            t = d.get("temps_entrainement_s", d.get("temps_reglage_fin_s"))
            print(f"| {v} | {s} | {t:.0f} | {f(d.get('temps_generation_s_par_1000'), 2)} |")


def e2():
    p = R / "e2_mhd2d.json"
    if not p.is_file():
        print("## E2 - missing\n")
        return
    r = json.loads(p.read_text())
    res, c = r["resume"], r["config"]
    print("## E2 - forced 2D MHD, generation conditioned on η\n")
    print(f"Configuration: N = {c['N']}, ν = {c['nu']}, α = {c['alpha']}, forcing band {c['kf']}; training η "
          f"{[round(e, 5) for e in c['eta_train']]}; test η {[round(e, 5) for e in c['eta_test']]}; {c['modes']} independent "
          f"Fourier modes; dimension {c['dim_potentiels']} (potentials) or {c['dim_composantes']} (components); MLP width {c['largeur']}, "
          f"{c['iters']} iterations; {c['n_gen']} samples per η; {c['n_train_par_eta']} training snapshots per η; "
          f"injection (Itô) ε_u, ε_b, ε_{{a²}} = {[round(x, 5) for x in c['injection']]}.\n")
    keys = [("div_rel_u", "rel. div. u"), ("div_rel_b", "rel. div. B"), ("spectrum_error_log10", "err. spectrum"),
            ("err_Eu_rel", "err. E_u"), ("err_Eb_rel", "err. E_B"), ("balance_residual_energie", "energy residual"),
            ("balance_residual_Hc", "H_c residual"), ("balance_residual_A2", "⟨a²⟩ residual"), ("std_diss_rel", "σ(D)/σ_ref"),
            ("energy_distance_features", "energy dist.")]
    for split in ("test", "train"):
        print(f"\n### Means over the {split} η\n")
        print("| variant | " + " | ".join(k[1] for k in keys) + " |")
        print("|---|" + "---|" * len(keys))
        for v, d in res.items():
            if v == "en_loi":
                continue
            print(f"| {v} | " + " | ".join(f(d[split][k[0]]) for k in keys) + " |")
        for m in ("base", "inclinaison", "recalage"):
            print(f"| in law: {m} (V4, half b) | " + " | ".join(f(res['en_loi'][m][split][k[0]]) for k in keys) + " |")
    print(f"\nMean ESS/N of the tilting: {f(res['en_loi']['ess_frac_b_moy'])}")
    e2_detail(r)
    print("\nTimes: " + json.dumps({k: {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()}
                                     for k, v in r["variantes"].items()}))
    print(f"\nTotal duration: {r['duree_totale_s']:.0f} s.\n")


def e2_detail(r):
    """Detail per value of η (a single seed per variant in E2)."""
    ev, el = r["evaluation"], r["en_loi"]
    vs = ["V0_libre", "V1_penalite", "V4_potentiels", "V5_temoin", "V5_potentiels_stat"]
    rows = sorted([(x["eta"], "training", i) for i, x in enumerate(ev[vs[0]]["train"])]
                  + [(x["eta"], "test", i) for i, x in enumerate(ev[vs[0]]["test"])])
    for k, lab in (("energy_distance_features", "energy distance"), ("balance_residual_energie", "signed residual of the energy balance"),
                   ("err_Eb_rel", "relative error on E_B")):
        print(f"\n### Per η: {lab}\n")
        print("| η | set | " + " | ".join(vs) + " |")
        print("|---|---|" + "---|" * len(vs))
        for eta, split, i in rows:
            sp = "train" if split == "training" else "test"
            print(f"| {eta:.5f} | {split} | " + " | ".join(f(ev[v][sp][i][k]) for v in vs) + " |")
    print("\n### Per η: law constraints on V4 (half b)\n")
    print("| η | Pm = ν/η | set | ESS/N | base dist. | tilting dist. | recalibration dist. | base residual | tilting residual |")
    print("|---|---|---|---|---|---|---|---|---|")
    for key, x in sorted(el.items(), key=lambda t: float(t[0])):
        print(f"| {float(key):.5f} | {f(r['config']['nu'] / float(key))} | {'training' if x['split'] == 'train' else 'test'} | {f(x['ess_frac_b'])} | "
              f"{f(x['base']['energy_distance_features'])} | {f(x['inclinaison']['energy_distance_features'])} | "
              f"{f(x['recalage']['energy_distance_features'])} | {f(x['base']['balance_residual_energie'])} | "
              f"{f(x['inclinaison']['balance_residual_energie'])} |")


def e3():
    p = R / "e3_abc.json"
    if not p.is_file():
        return
    r = json.loads(p.read_text())
    print("## E3 - ABC kinematic dynamo (A = B = C = 1, Rm = 1/η, N = 32)\n")
    print("| Rm | λ | λ (last quarter) | rel. div. |")
    print("|---|---|---|---|")
    for t in r["taux"]:
        print(f"| {t['Rm']} | {f(t['lambda'], 4)} | {f(t['lambda_dernier_quart'], 4)} | {f(t['div_rel'])} |")
    print(f"\nConvergence N = 48: {r['convergence']}")
    print(f"Interpolated thresholds: {[round(s, 2) for s in r['seuils_interpoles']]}")
    print(f"Duration: {r['duree_s']:.0f} s.\n")


if __name__ == "__main__":
    print("# Results digest (generated by experiments/digest.py)\n")
    e1(); e2(); e3()
