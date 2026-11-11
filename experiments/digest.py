"""Condensé chiffré des résultats (Markdown) à partir des JSON : python3 digest.py > results/digest.md

Les pages du site citent ces valeurs ; ne pas recopier de chiffres d'ailleurs.
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
        print("## E1 — résultats complets absents (calcul en cours)\n")
        return
    r = json.loads(p.read_text())
    res = r["resume"]
    print("## E1 — modèle de renversements de Gissinger (loi invariante conditionnée par Γ)\n")
    c = r["config"]
    print(f"Configuration : μ = {c['mu']}, ν = {c['nu']} ; Γ d'entraînement {c['G_train']} ; Γ de test {c['G_test']} ; "
          f"{c['trajectoires_par_Gamma']} trajectoires par Γ, durée gardée {c['duree_gardee']} ; itérations {c['iters']} ; "
          f"graines {c['seeds']} ; {c['n_gen']} échantillons générés par Γ ; Heun {c['pas_ODE_Heun']} pas ; MLP {c['largeur_MLP']}×{c['profondeur_MLP']} ; h_Rice = {c['h_Rice']}.\n")
    keys = [("energie", "dist. énergie"), ("sw1", "SW1"), ("asym", "|P(D>0)−½|"), ("liou_train_moy", "Liouville deg≤2"),
            ("liou_test_moy", "Liouville deg 3"), ("dEdt_std", "σ(dE/dt)"), ("erreur_pont", "err. P(|D|<0,25)"),
            ("erreur_taux_rice", "err. taux Rice")]
    for split in ("test", "train"):
        print(f"\n### Moyennes sur les Γ de {split} (moyenne des graines)\n")
        print("| variante | " + " | ".join(k[1] for k in keys) + " | ESS/N |")
        print("|---|" + "---|" * (len(keys) + 1))
        for v, d in res.items():
            if split in d:
                print(f"| {v} | " + " | ".join(f(d[split].get(k[0])) for k in keys) + f" | {f(d[split].get('ess_frac_b'))} |")
    print(f"\nPlanchers de bruit Monte-Carlo (sous-échantillon de la référence) : {json.dumps(res['planchers_bruit_MC'])}")
    print(f"Référence : {json.dumps(res['reference'])}\n")
    print("### Données : passages de D par 0 (simulation) et asymétrie des données d'entraînement\n")
    print("| Γ | taux simulation | taux Rice (réf.) | P(D>0) entraînement |")
    print("|---|---|---|---|")
    for g, s in sorted(r["donnees"].items(), key=lambda t: float(t[0])):
        print(f"| {g} | {f(s['taux_passages_simulation'])} | {f(s['taux_rice_reference'])} | {f(s.get('P(D>0)_train'), 4)} |")
    print("\n### Grille fine (modèle C graine 0 et F graine 0)\n")
    print("| Γ | taux sim. | Rice réf. | Rice C | Rice F | pont réf. | pont C | pont F |")
    print("|---|---|---|---|---|---|---|---|")
    for x in r["grille_fine"]:
        print(f"| {x['Gamma']} | {f(x['taux_simulation'])} | {f(x['taux_rice_ref'])} | {f(x['taux_rice_modele'])} | "
              f"{f(x.get('taux_rice_modele_F'))} | {f(x['pont_ref'])} | {f(x['pont_modele'])} | {f(x.get('pont_modele_F'))} |")
    e1_detail(r)
    print(f"\nDurée totale : {r['duree_totale_s']:.0f} s.\n")


def e1_detail(r):
    """Détails par Γ et par graine tirés du JSON de E1.

    Le JSON garde, pour chaque Γ, la moyenne et l'écart-type (ddof = 0) des deux graines : les deux valeurs par graine
    sont donc moyenne ± écart-type, sans savoir laquelle appartient à quelle graine. On publie l'enveloppe
    (« basse » = moyenne − écart-type, « haute » = moyenne + écart-type) ; la moyenne sur les Γ de chaque graine est
    comprise entre la moyenne des valeurs basses et celle des valeurs hautes.
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

    print("\n### Asymétrie |P(D>0)−½| par Γ (moyenne des graines)\n")
    vs = ["A_reference", "B_augmentation", "C_equivariant"]
    print("| Γ | jeu | " + " | ".join(vs) + " |")
    print("|---|---|" + "---|" * len(vs))
    allg = sorted([(x["Gamma"], "entraînement", i) for i, x in enumerate(rows(vs[0], "train"))]
                  + [(x["Gamma"], "test", i) for i, x in enumerate(rows(vs[0], "test"))])
    for g, split, i in allg:
        sp = "train" if split == "entraînement" else "test"
        print(f"| {g} | {split} | " + " | ".join(f(rows(v, sp)[i]["asym"][0]) for v in vs) + " |")

    print("\n### Dispersion entre graines (écart-type moyen sur les Γ de test)\n")
    print("| variante | dist. énergie | Liouville deg≤2 | Liouville deg 3 |")
    print("|---|---|---|---|")
    for v in ("C_equivariant", "F_stationnarite_C", "F0_temoin_C"):
        print(f"| {v} | " + " | ".join(f(mean([x[k][1] for x in rows(v, 'test')])) for k in ("energie", "liou_train_moy", "liou_test_moy")) + " |")

    print("\n### Enveloppe par graine de σ(dE/dt)/σ_ref (σ moyen sur les Γ de test, divisé par la référence)\n")
    print("| variante | graine basse | graine haute |")
    print("|---|---|---|")
    for v in ("F_stationnarite_C", "F0_temoin_C", "C_court", "F_stationnarite_Ccourt", "F0_temoin_Ccourt"):
        lo, hi = env(v, "test", "dEdt_std")
        print(f"| {v} | {f(lo / ref_sd)} | {f(hi / ref_sd)} |")
    print("\nSur C court, la graine 1 a divergé : à chaque Γ, sa valeur est la haute, ce qui sépare les graines.")

    print("\n### C court, graine 0 (valeur basse à chaque Γ) contre son témoin, Γ de test\n")
    print("| métrique | F sur C court, graine 0 | témoin F0, moyenne des graines | témoin F0, graine haute |")
    print("|---|---|---|---|")
    for k, lab in (("energie", "dist. énergie"), ("liou_train_moy", "Liouville deg≤2"), ("liou_test_moy", "Liouville deg 3")):
        lo, _ = env("F_stationnarite_Ccourt", "test", k)
        _, hi0 = env("F0_temoin_Ccourt", "test", k)
        print(f"| {lab} | {f(lo)} | {f(res['F0_temoin_Ccourt']['test'][k])} | {f(hi0)} |")

    print("\n### Inclinaison a posteriori par Γ de test (moyenne des graines, moitié b)\n")
    print("| Γ | ESS/N (A) | Liouville deg≤2 : A moitié → A incliné | ESS/N (C) | Liouville deg≤2 : C moitié → C incliné |")
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
    print(f"\nPassages fictifs sous le seuil (grille fine, taux simulé nul) : au plus {f(mc['taux_rice_modele'])} pour C "
          f"(Γ = {mc['Gamma']}) et {f(mf['taux_rice_modele_F'])} pour F (Γ = {mf['Gamma']}), soit "
          f"{f(100 * mc['taux_rice_modele'] / g1['taux_simulation'], 2)} % et {f(100 * mf['taux_rice_modele_F'] / g1['taux_simulation'], 2)} % "
          f"du taux simulé à Γ = 1 ({f(g1['taux_simulation'])}).")

    print("\n### Durées par variante et par graine (s)\n")
    print("| variante | graine | entraînement ou réglage fin | génération par 1000 échantillons |")
    print("|---|---|---|---|")
    for v, seeds in r["entrainement"].items():
        for s, d in seeds.items():
            t = d.get("temps_entrainement_s", d.get("temps_reglage_fin_s"))
            print(f"| {v} | {s} | {t:.0f} | {f(d.get('temps_generation_s_par_1000'), 2)} |")


def e2():
    p = R / "e2_mhd2d.json"
    if not p.is_file():
        print("## E2 — absent\n")
        return
    r = json.loads(p.read_text())
    res, c = r["resume"], r["config"]
    print("## E2 — MHD 2D forcée, génération conditionnée par η\n")
    print(f"Configuration : N = {c['N']}, ν = {c['nu']}, α = {c['alpha']}, bande de forçage {c['kf']} ; η d'entraînement "
          f"{[round(e, 5) for e in c['eta_train']]} ; η de test {[round(e, 5) for e in c['eta_test']]} ; {c['modes']} modes de Fourier "
          f"indépendants ; dimension {c['dim_potentiels']} (potentiels) ou {c['dim_composantes']} (composantes) ; MLP largeur {c['largeur']}, "
          f"{c['iters']} itérations ; {c['n_gen']} échantillons par η ; {c['n_train_par_eta']} instantanés d'entraînement par η ; "
          f"injection (Itô) ε_u, ε_b, ε_{{a²}} = {[round(x, 5) for x in c['injection']]}.\n")
    keys = [("div_rel_u", "div. rel. u"), ("div_rel_b", "div. rel. B"), ("err_spectre_log10", "err. spectre"),
            ("err_Eu_rel", "err. E_u"), ("err_Eb_rel", "err. E_B"), ("residu_bilan_energie", "résidu énergie"),
            ("residu_bilan_Hc", "résidu H_c"), ("residu_bilan_A2", "résidu ⟨a²⟩"), ("std_diss_rel", "σ(D)/σ_ref"),
            ("dist_energie_features", "dist. énergie")]
    for split in ("test", "train"):
        print(f"\n### Moyennes sur les η de {split}\n")
        print("| variante | " + " | ".join(k[1] for k in keys) + " |")
        print("|---|" + "---|" * len(keys))
        for v, d in res.items():
            if v == "en_loi":
                continue
            print(f"| {v} | " + " | ".join(f(d[split][k[0]]) for k in keys) + " |")
        for m in ("base", "inclinaison", "recalage"):
            print(f"| en loi : {m} (V4, moitié b) | " + " | ".join(f(res['en_loi'][m][split][k[0]]) for k in keys) + " |")
    print(f"\nESS/N moyen de l'inclinaison : {f(res['en_loi']['ess_frac_b_moy'])}")
    e2_detail(r)
    print("\nTemps : " + json.dumps({k: {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()}
                                     for k, v in r["variantes"].items()}))
    print(f"\nDurée totale : {r['duree_totale_s']:.0f} s.\n")


def e2_detail(r):
    """Détail par valeur de η (une seule graine par variante en E2)."""
    ev, el = r["evaluation"], r["en_loi"]
    vs = ["V0_libre", "V1_penalite", "V4_potentiels", "V5_temoin", "V5_potentiels_stat"]
    rows = sorted([(x["eta"], "entraînement", i) for i, x in enumerate(ev[vs[0]]["train"])]
                  + [(x["eta"], "test", i) for i, x in enumerate(ev[vs[0]]["test"])])
    for k, lab in (("dist_energie_features", "distance d'énergie"), ("residu_bilan_energie", "résidu signé du bilan d'énergie"),
                   ("err_Eb_rel", "erreur relative sur E_B")):
        print(f"\n### Par η : {lab}\n")
        print("| η | jeu | " + " | ".join(vs) + " |")
        print("|---|---|" + "---|" * len(vs))
        for eta, split, i in rows:
            sp = "train" if split == "entraînement" else "test"
            print(f"| {eta:.5f} | {split} | " + " | ".join(f(ev[v][sp][i][k]) for v in vs) + " |")
    print("\n### Par η : contraintes en loi sur V4 (moitié b)\n")
    print("| η | Pm = ν/η | jeu | ESS/N | dist. base | dist. inclinaison | dist. recalage | résidu base | résidu inclinaison |")
    print("|---|---|---|---|---|---|---|---|---|")
    for key, x in sorted(el.items(), key=lambda t: float(t[0])):
        print(f"| {float(key):.5f} | {f(r['config']['nu'] / float(key))} | {'entraînement' if x['split'] == 'train' else 'test'} | {f(x['ess_frac_b'])} | "
              f"{f(x['base']['dist_energie_features'])} | {f(x['inclinaison']['dist_energie_features'])} | "
              f"{f(x['recalage']['dist_energie_features'])} | {f(x['base']['residu_bilan_energie'])} | "
              f"{f(x['inclinaison']['residu_bilan_energie'])} |")


def e3():
    p = R / "e3_abc.json"
    if not p.is_file():
        return
    r = json.loads(p.read_text())
    print("## E3 — dynamo cinématique ABC (A = B = C = 1, Rm = 1/η, N = 32)\n")
    print("| Rm | λ | λ (dernier quart) | div. rel. |")
    print("|---|---|---|---|")
    for t in r["taux"]:
        print(f"| {t['Rm']} | {f(t['lambda'], 4)} | {f(t['lambda_dernier_quart'], 4)} | {f(t['div_rel'])} |")
    print(f"\nConvergence N = 48 : {r['convergence']}")
    print(f"Seuils interpolés : {[round(s, 2) for s in r['seuils_interpoles']]}")
    print(f"Durée : {r['duree_s']:.0f} s.\n")


if __name__ == "__main__":
    print("# Condensé des résultats (généré par experiments/digest.py)\n")
    e1(); e2(); e3()
