# Périmètre de la phase 1

## Mission de cette exécution

Phase 1 seulement (`BRIEF-GROK.md` §7.1). Produire l’inventaire, le guide de style, le plan chapitré, les portes de relecture, les lots futurs et le journal. Ne pas écrire les scripts. Ne pas animer. Ne pas rendre.

Les films `film_core_en.mp4`, `film_core_fr.mp4`, `film_extended_en.mp4`, `film_extended_fr.mp4` restent **en attente**.

## Commit source

Tous les renvois `fichier:ligne` de l’inventaire et du plan sont valables sur :

`4e42429716c093df34ba05b47ada542a13d39c50`

Message de ce commit : « Vidéo : état de l’art (synthèse et fiche pour les rédacteurs), relectures des derniers modules ». Ce message concerne le dépôt entier. Il n’a pas été utilisé pour lire une production parallèle.

Arbre distant vu au début de l’exécution : `origin/main` seul. Aucune branche `grok/video`. Aucune branche `grok/video-plan` avant celle-ci.

## Ce qui a été lu

Pages désignées par le brief :

- `en/index.qmd`, `en/rapport/index.qmd`, `en/these/index.qmd`, `en/encadrants/index.qmd`
- `en/experiences/index.qmd`, `en/calcul/index.qmd`, `en/interactifs/index.qmd`
- `en/prep/index.qmd` (carte des huit modules ; les 16 556 lignes des modules 1–8 n’ont pas été relues ligne à ligne)
- `experiences/resultats/digest.md`, `experiences/resultats/e3_abc.json`
- `experiences/resultats/e1_gissinger.json` et `e2_mhd2d.json` : non relus octet par octet (324 ko et 80 ko). Les tableaux du rapport qui disent venir du JSON sont cités comme tels. La relecture science doit rouvrir le JSON aux clés utilisées à l’écran.
- `specs/sources/dynamo.md`, `specs/sources/encadrants.md` (titres et zone publications via la page EN), `specs/sources/litterature.md` et `specs/sources/donnees-metriques.md` (structure et titres ; pas une relecture mot à mot des 400+ lignes de chaque note)
- `infra/cloud/RECOMMANDATION-CLOUD.md` §0, §4.2, et, pour les paris et le coût décisionnel, §7.3 et §8
- `infra/configs/palier1_mhd2d.yaml`, `palier2_abc3d.yaml`, `palier2_tg3d.yaml`, `train_fm3d.yaml` (en-têtes et grilles)
- `milady/eval/metrics.py` (clés de `compare_ensembles` et `budget_summary`)
- `assets/paper.css` (jetons de thème), `figures/cadre/figure/parts.js` et `figures/vks/figure/parts.js` (couleurs)
- `figures/*/figure/out/*-en.png` listés, non réinterprétés au-delà des légendes des pages EN

## Ce qui n’a pas été ouvert

- Le dossier `video/` : aucun fichier, aucun `git log`, aucun `git diff`, aucun blame.
- `infra/cloud/RECOMMANDATION-CLOUD.md` §7.2 cite `video/README.md` et un inventaire de scènes d’une autre production. Ce pointeur n’a pas été suivi. Les identifiants de scènes de ce plan (`g00`…, `x01`…) sont les nôtres.
- Aucun fichier d’identifiants (`.env`, clés, `secrets`). Aucune variable d’API lue. Aucun appel Fish. Aucune location cloud. Aucune simulation, aucun entraînement, aucun banc.

## Indépendance

Les chiffres viennent du site, du digest, du JSON E3 et des notes `specs/sources/`. Les métaphores, l’ordre des chapitres, les durées et les noms de repères sont décidés ici. Les figures PNG/SVG du site sont des **actifs autorisés** (planches mesurées ou schémas déjà légendés), pas une narration à recopier.

## Honnêteté de statut du rapport

Le rapport de stage est **prospectif**, écrit avant le stage, non validé par les encadrants (`en/index.qmd:45`, `en/index.qmd:43-45`). Le site n’est ni produit ni endossé par l’ENPC, le LISN, l’OCA, l’ANR ou les encadrants. Toute scène qui citerait une phrase du site comme une conclusion des encadrants est une erreur.

## Langues prévues (pas encore écrites)

- Narration anglaise et narration française, mêmes identifiants de repères.
- Visuels en anglais dans les deux versions.
- Sous-titres incrustés : anglais sur le film EN, français sur le film FR, tirés plus tard du script, jamais d’une transcription.
- Voix prévue : bibliothèque Fish « Ethan », `reference_id` `536d3a5e000945adb7038665781a4aca`, pour les deux langues. Pas de clone. Détail : `FISH.md`. Aucune synthèse dans cette phase.
