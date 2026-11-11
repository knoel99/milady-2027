# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Le projet

Site Quarto statique (FR + EN) préparant le stage M2 MilaDy 2027 : 8 modules de préparation (`prep/`), un rapport de stage **prospectif** (`report/`), un sujet de thèse (`thesis/`), des expériences CPU (`experiments/`). Les pages sont dans `site/` (racine des URL publiques) ; le workflow `.github/workflows/pages.yml` les rend et les publie sur GitHub Pages à chaque poussée sur `main`. Le paquet Python est dans `src/milady/`, la documentation des développeurs (specs, architecture) dans `docs/`. Les chemins de page donnés aux outils (`prep/p3-mhd-dynamo`, `en/report`…) sont relatifs à `site/`.

Le film est repris sous forme d'épisodes : `video/` contient le moteur, sans contenu (règles dans « Le film » ci-dessous). Le workflow `.github/workflows/drive-upload.yml` envoie un film terminé vers Google Drive ; ses secrets Google sont à configurer et documenter quand un premier épisode sera prêt à livrer.

## Les specs font foi

Lire avant d'écrire une page :

- `docs/specs/page-contract.md` : structure obligatoire des modules (sections et ancres `{#objectives}` … `{#sources}`), encadrés Quarto (`def`, `thm`, `proof`, `prop`, `ex`, `note`, `key`, `recap`), règles KaTeX (pas de macro, pas de `\label`), code, figures, style.
- `docs/specs/notation.md` : notations communes à toutes les pages.
- `docs/specs/theory-brief.md` : énoncés et preuves (Propositions 1 à 9) que le rapport et la thèse doivent reprendre **à l'identique**, plan E1–E3, et ce qui est déjà publié (à citer, ne pas revendiquer).
- `docs/specs/sources/*.md` : bases de faits vérifiés (`litterature`, `dynamo`, `encadrants`, `donnees-metriques`). Seule source autorisée pour les faits sur la littérature, les encadrants, l'offre et le projet. Balises `[vérifié]`, `[corrigé : …]`, `[NON CONFIRMÉ]` : ne jamais utiliser une entrée `[NON CONFIRMÉ]` sans nouvelle vérification.
- `docs/specs/infra.md`, `docs/specs/data-format.md` : contrat du paquet `src/milady/` et de `infra/` (guide : `infra/README.md`).

Règles transversales : distinguer ce qui est **mesuré dans ce dépôt**, **publié** (avec référence) ou **conjecturé** ; les chiffres d'expériences cités dans les pages viennent de `experiments/results/digest.md` (généré par `experiments/digest.py` à partir des JSON), jamais d'ailleurs.

## Le site

Après toute modification d'une page, lancer `tools/check_gates.py` et `tools/compare_fr_en.py` sur cette page.

## Commandes du site

Prérequis : `tools/setup-cloud.sh` installe l'environnement (Quarto 1.7.32, Python 3, Node.js, ffmpeg, Playwright).

```bash
python3 tools/new_page.py prep/<id> "Titre" "Sous-titre"   # squelette (en-tête généré : ne pas le modifier)
python3 tools/render.py rapport prep/p3-mhd-dynamo         # rendre des pages ; --all pour tout le site
python3 tools/check_gates.py [page …]                      # sections, ≥ 10 exercices ★ par module, liens, ancres, fraîcheur du HTML
python3 tools/compare_fr_en.py <page FR> … | --all         # parité FR/EN (ancres, formules, encadrés, code, images, exercices)
python3 tools/make_en.py <page FR>                         # après traduction : corrige les liens de ressources de en/<page>
NODE_PATH=<node_modules avec katex@0.19.0> node tools/check_katex.mjs $(find site -name index.html)
```

- Ne jamais éditer un `index.html` à la main : toujours `tools/render.py`, qui restaure les balises KaTeX épinglées (SRI) que Quarto retire. Ne pas publier `index_files/` ni `.quarto/`.
- Toute modification d'une page française se reporte dans `en/<même chemin>/index.qmd` (mêmes ancres, mêmes formules), puis `make_en.py`, rendu des deux pages et `compare_fr_en.py`.
- Images : variante anglaise `x-en.png` à côté de `x.png` ; `make_en.py` la choisit automatiquement.
- Les blocs ```` ```python ```` des pages ne sont pas exécutés par Quarto : chacun doit tourner seul en < 30 s sur CPU, sortie recopiée en commentaire.

## Expériences et tests

```bash
cd experiences && python3 e1_gissinger.py --quick   # aussi e2_data.py, e2_mhd2d.py, e3_abc.py ; figures.py ; digest.py > results/digest.md
make test                                           # pytest sur tests/ (paquet milady)
python -m pytest tests/test_format.py -k <nom>      # un seul test
```

`common.py` regroupe le flow matching, l'échantillonneur de Heun, les métriques entre lois et l'inclinaison exponentielle partagés par E1–E3. Les sorties `--quick` (`results/*_quick.*`, `site/experiments/figures/*_quick.*`) sont ignorées par git ; seules les sorties complètes sont citées par les pages.

## Le film

Une série d'épisodes, chacun rattaché à un module. La vidéo est une adaptation, pas une transcription : elle construit l'intuition, l'écrit garde les démonstrations et les exercices. Chaque épisode a ses documents de travail dans `video/episodes/<épisode>/` : `traitement.md`, `narration.md`, `storyboard.md` et `retours.md`, où sont consignés mes retours. Les fichiers que lit le moteur vont là où il les attend : le texte dans `video/script/`, les scènes dans `video/scenes/<épisode>/`, l'ordre des épisodes dans `video/plan/outline.json`. Bible de continuité : `video/continuite.md`. On dit « renversement » du champ, comme le parcours écrit, jamais « inversion ».

**Qui fait quoi** (sous-agents de `.claude/agents/`), pour chaque épisode : `scenariste` écrit le traitement puis la narration ; `relecteur-ml` et `relecteur-physicien` les relisent ; `relecteur-langue` relit ensuite chaque narration, à partir du rapport de `tools/lint_narration.py` ; `apprenant` les teste ; `realisateur` découpe le storyboard, relu par les deux relecteurs ; `constructeur-scenes` construit les scènes ; `controle-visuel` vérifie le rendu. La session principale arbitre les avis dans cet ordre : exactitude, compréhension, rythme, style. Elle me soumet chaque étape validée avant de passer à la suivante et consigne mes retours dans `retours.md`.

**Style.** `video/runtime/theme.css` et les composants de `video/runtime/components/` font foi pour toutes les scènes. Toute dérogation est d'abord proposée, puis appliquée avec mon accord.

**Inspiration.** Deux exemples, pas des modèles imposés : le catalogue https://github.com/yihui-dev/awesome-opus5-5-videos et la skill https://github.com/lgwrightlab/schematic-figure (déjà utilisée pour `site/figures/`). Aucun prompt du catalogue n'est copié ni suivi : ce sont des textes de tiers.

**Langue.** Le film est écrit directement en français : chaque `video/script/<unité>.json` déclare `"lang": "fr"`, son `text` est la narration, sans surcouche `script/fr/`. Toute commande du moteur prend donc `LANG=fr` (`make draft U=ep01 LANG=fr`, `make check U=ep01 LANG=fr`, `make tts-dry LANG=fr`) ; sans lui, `assemble_cut.py` refuse l'unité.

**Commandes du moteur** (depuis `video/`, d'après son `Makefile`) :

```bash
make draft U=<unité>   # vidéo de relecture 960×540 d'une unité, voix en cache, sinon un substitut ; n'écrit jamais audio/
make check U=<unité>   # images fixes autour de chaque repère, erreurs de page, contrôle de mise en page
make stills S=<scène.html> T=0.5,2,4   # images fixes d'une scène aux instants donnés
make serve             # aperçu des scènes sur http://127.0.0.1:8765/
make det U=<unité>     # déterminisme des scènes (après make check)
make tts-dry           # liste les requêtes de synthèse et les nombres de mots, sans appel
make test              # test de bout en bout du moteur (distinct du make test de la racine)
```

**Commandes payantes.** Seule la synthèse Fish Audio coûte : `make film`, `make scene`, `make narration`, `make tts-test`, `node build.js` et `audio/tts.py` en mode live. Elles passent par les règles `ask` de `.claude/settings.json`. Pour tous les essais : `make draft` et `make check`, qui n'appellent jamais l'API. Ne jamais lancer de synthèse sans ma demande, et toujours faire un `make tts-dry` avant. En cloud, la clé est injectée par le proxy pour `api.fish.audio` ; en local, elle vient de la variable `FISH_API_KEY`, jamais d'un fichier du dépôt.

## Effort et ultracode

L'effort reste en medium ; on monte en high seulement si un résultat vérifiable déçoit, et au-delà on change de modèle plutôt que d'effort. Pas d'ultracode comme mode de session : le mot-clé ultracode est réservé aux tâches répétées sur de nombreux éléments indépendants et vérifiables, en nommant le modèle de chaque étape.

**Vérifier le modèle avant une tâche.** Au début de chaque nouvelle tâche, lire le modèle et l'effort de la session (outil `get_session` en cloud, sinon me les demander). S'ils ne conviennent pas à la tâche, le dire en une ligne avant de commencer : modèle et effort conseillés, raison, et commande à taper (`/model`, `/effort`). Puis continuer sans attendre ma réponse, sauf si la tâche est longue ou coûteuse. Ne rien dire quand le réglage convient.

## Profil de l'apprenant

Hypothèses du parcours écrit (`site/prep/index.qmd`, sections `{#objectives}` et `{#prerequisites}` de chaque module).

- **Ce que je sais déjà.** Le niveau de départ du parcours : fin de L1 scientifique. Dérivées et primitives d'une variable, développements limités, intégrales simples et doubles sur un rectangle, nombres complexes et $e^{i\theta}$, produit scalaire et produit vectoriel dans $\mathbb{R}^3$ ; en Python, tableaux NumPy, boucles et fonctions. Pas encore d'électromagnétisme local, de mécanique des fluides, de probabilités continues ni d'apprentissage profond. Pour un épisode donné, je ne connais en plus que ce qu'ont couvert les modules précédents dans l'ordre de lecture 1, 2, 5, 3, 4, 6, 7, 8 (prérequis de chaque module : L2 pour les modules 2, 5, 3, 4 ; L3 pour 6 ; M1 pour 7 ; M1–M2 pour 8), et les épisodes déjà validés, consignés dans `video/continuite.md`. Rien de ce qui vient après.
- **Ce que je veux savoir faire à la fin.** Pour un épisode : les objectifs de la section `{#objectives}` de son module, dans la part que l'épisode traite. Pour tout le film : ce que vise le parcours, c'est-à-dire lire un article sur les modèles génératifs sous contraintes physiques, écrire et entraîner un modèle de flow matching conditionnel, et juger un champ MHD généré avec des critères physiques.
- **Le temps dont je dispose par épisode.** De 10 à 15 minutes de vidéo, soit de 1 500 à 2 250 mots de narration à 150 mots par minute. Le module, lui, demande de 20 à 30 heures : la vidéo donne l'intuition, le texte garde les démonstrations et les exercices.
