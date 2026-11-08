# Rapport de phase 1

Les films ne sont pas faits. Cette exécution s’arrête au plan, sur la branche `grok/video-plan`. La branche d’intégration `grok/video` n’existait pas. `main` n’a pas été poussée et n’a pas été fusionnée.

## Livrables de cette phase

Tous sous `video-grok/`, commit source des citations : `4e42429716c093df34ba05b47ada542a13d39c50`.

| Document | Rôle |
|---|---|
| `README.md` | index |
| `00-PERIMETRE.md` | ce qui a été lu, ce qui n’a pas été ouvert |
| `INVENTAIRE.md` | concepts L0–L5, chiffres `fichier:ligne`, actifs autorisés |
| `INCERTITUDES.md` | collisions, limites, faits externes bloqués |
| `MANQUES.md` | paris, critères, créneaux de narration pour les deux issues |
| `STYLE.md` | guide visuel indépendant, visuels anglais |
| `PLAN.md` | cœur 41:00 (`g00`–`g15`), étendu 60:00 avec cinq modules |
| `QUESTIONS.md` | cartes ≤ 18 mots, registre A/B/C, ordre du jour 45 min |
| `LOTS.md` | lots disjoints, portes, pilote `g10` |
| `REVUES.md` | périmètre exact des deux relectures, non exécutées |
| `FISH.md` | inventaire d’API, zéro requête |
| `STATS.md` | durées et compteurs réels, tokens et coût `unavailable` |

Les quatre MP4, les sous-titres, les pistes, le kit de voix, les convertisseurs, la fiche vouvoyée finale et le mémoire d’état de l’art destiné aux encadrants restent à écrire. Le plan ne les remplace pas.

## Ce que le plan décide

Le cœur monte de L0 à L5 et se regarde sans les modules. Il contient les deux unités demandées : « A century of dynamo hunting » (g04, 2:30, après les salles de sodium) et « The map of the field » (g12, 4:00, après le tableau des résultats). « Before we compute » (g14, 2:20) classe les questions en simulations, cadre, et logistique. L’aiguille bascule dans les premières secondes, hors échelle, et revient à la fin.

Les campagnes `palier1_mhd2d`, `palier2_abc3d`, `palier2_tg3d`, `train_fm3d` et les données VKS / DRESDYN sont des paris. Aucune courbe future n’est dessinée. Chaque scène en attente a trois issues : critère atteint, non atteint, non concluant.

## Blocages

1. Porte G0 ouverte. Deux relecteurs qui n’ont pas écrit ce plan doivent rendre `video-grok/revues/SCIENCE.md` et `video-grok/revues/PEDAGOGIE.md` selon `REVUES.md` avant toute phrase dite.
2. `grok/video` absente. Les fusions futures n’ont pas de base. Une pull request de cette planification ne peut viser que `main`, et elle ne doit pas être fusionnée. Quand `grok/video` sera créée au commit source, la base sera changée.
3. Faits externes demandés par le brief et absents du dépôt : bandes océaniques, date du dernier renversement, dynamo à disque, Larmor, Glatzmaier–Roberts. Aucun nombre n’a été inventé. Les scènes sont `blocked-source` ou coupables.
4. Tokens et coût : non exposés. Fish : non appelé. La clé n’a pas été cherchée.
5. Les JSON E1 et E2 n’ont pas été relus clé par clé. La revue science doit le faire pour tout chiffre d’écran qui dit « issu du JSON » au-delà du digest et des tables du rapport.

## Périmètre recommandé des revues

Science : tout chiffre de `INVENTAIRE.md`, `INCERTITUDES.md`, `MANQUES.md`, les pastilles et les sources de `PLAN.md`, les renvois de `QUESTIONS.md`. Verdict ligne à ligne `ok` / `bloquant` / `réserve`. Hors sujet : le style et les durées, sauf affirmation fausse forcée par l’ordre.

Pédagogie : horloges de `PLAN.md`, motifs et rythme de `STYLE.md`, cartes de `QUESTIONS.md`, représentativité du pilote. Obligatoire : bascule dans les 30 premières secondes, une idée par scène, pas de formule avant sa motivation, cœur autonome sans les modules x, g04 et g12 dans le cœur aux durées prévues, g14 entre 2 et 3 minutes, budgets de mots tenables. Pas de script dans le rapport de revue.

## Limites

Le rapport de stage est prospectif et non validé par les encadrants. E1 a deux graines, E2 une seule, les tests sont des interpolations, E2 n’est pas une dynamo, E3 n’a pas de modèle génératif. Les définitions de Rm du VKS sont incompatibles entre elles. Le budget d’environ 1,1×10⁴ heures GPU est une hypothèse, au moins à un facteur deux, sans mesure GPU.

`infra/cloud/RECOMMANDATION-CLOUD.md` §7.2 pointe vers `video/`. Ce dossier n’a pas été ouvert. Les identifiants de scènes d’ici ne reprennent pas ceux de cette section.

## Avec plus de temps, après les revues

Fermer les bloquants, épingler les sources du §E si elles tiennent, puis seulement : moteur déterministe, pilote g10, scripts par lots disjoints, traduction française sur les mêmes repères, rectangle « not yet run » pour les paris. Pas de location, pas de nouvelle simulation, pas de crédit Fish avant un cache et des textes gelés.

La comparaison avec l’autre production n’est pas faite : elle supposerait d’ouvrir `video/`, ce qui est exclu.
