# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Le projet

Site Quarto statique (FR + EN) préparant le stage M2 MilaDy 2027 : 8 modules de préparation (`prep/`), un rapport de stage **prospectif** (`rapport/`), un sujet de thèse (`these/`), des expériences CPU (`experiences/`). Publié par GitHub Pages depuis `main`, à la racine : les `index.html` rendus sont versionnés avec leurs `index.qmd`, sans construction côté GitHub.

Le film est repris sous forme d'épisodes : `video/` contient le moteur, sans contenu (règles dans « Le film » ci-dessous). Le workflow `.github/workflows/drive-upload.yml` envoie un film terminé vers Google Drive ; ses secrets Google sont à configurer et documenter quand un premier épisode sera prêt à livrer.

## Les specs font foi

Lire avant d'écrire une page :

- `specs/page-contract.md` : structure obligatoire des modules (sections et ancres `{#objectifs}` … `{#sources}`), encadrés Quarto (`def`, `thm`, `proof`, `prop`, `ex`, `note`, `key`, `recap`), règles KaTeX (pas de macro, pas de `\label`), code, figures, style.
- `specs/notations.md` : notations communes à toutes les pages.
- `specs/theorie-brief.md` : énoncés et preuves (Propositions 1 à 9) que le rapport et la thèse doivent reprendre **à l'identique**, plan E1–E3, et ce qui est déjà publié (à citer, ne pas revendiquer).
- `specs/sources/*.md` : bases de faits vérifiés (`litterature`, `dynamo`, `encadrants`, `donnees-metriques`). Seule source autorisée pour les faits sur la littérature, les encadrants, l'offre et le projet. Balises `[vérifié]`, `[corrigé : …]`, `[NON CONFIRMÉ]` : ne jamais utiliser une entrée `[NON CONFIRMÉ]` sans nouvelle vérification.
- `specs/infra.md`, `specs/format-donnees.md` : contrat du paquet `milady/` et de `infra/` (guide : `infra/README.md`).

Règles transversales : distinguer ce qui est **mesuré dans ce dépôt**, **publié** (avec référence) ou **conjecturé** ; les chiffres d'expériences cités dans les pages viennent de `experiences/resultats/digest.md` (généré par `experiences/digest.py` à partir des JSON), jamais d'ailleurs.

## Commandes du site

Prérequis : `tools/setup-cloud.sh` installe l'environnement (Quarto 1.7.32, Python 3, Node.js, ffmpeg, Playwright).

```bash
python3 tools/new_page.py prep/<id> "Titre" "Sous-titre"   # squelette (en-tête généré : ne pas le modifier)
python3 tools/render.py rapport prep/p3-mhd-dynamo         # rendre des pages ; --all pour tout le site
python3 tools/check_gates.py [page …]                      # sections, ≥ 10 exercices ★ par module, liens, ancres, fraîcheur du HTML
python3 tools/compare_fr_en.py <page FR> …                 # parité FR/EN (ancres, formules, encadrés, code, images, exercices)
python3 tools/make_en.py <page FR>                         # après traduction : corrige les liens de ressources de en/<page>
NODE_PATH=<node_modules avec katex@0.19.0> node tools/check_katex.mjs $(find . -name index.html)
```

- Ne jamais éditer un `index.html` à la main : toujours `tools/render.py`, qui restaure les balises KaTeX épinglées (SRI) que Quarto retire. Ne pas publier `index_files/` ni `.quarto/`.
- Toute modification d'une page française se reporte dans `en/<même chemin>/index.qmd` (mêmes ancres, mêmes formules), puis `make_en.py`, rendu des deux pages et `compare_fr_en.py`.
- Images : variante anglaise `x-en.png` à côté de `x.png` ; `make_en.py` la choisit automatiquement.
- Les blocs ```` ```python ```` des pages ne sont pas exécutés par Quarto : chacun doit tourner seul en < 30 s sur CPU, sortie recopiée en commentaire.

## Expériences et tests

```bash
cd experiences && python3 e1_gissinger.py --quick   # aussi e2_donnees.py, e2_mhd2d.py, e3_abc.py ; figures.py ; digest.py > resultats/digest.md
make test                                           # pytest sur tests/ (paquet milady)
python -m pytest tests/test_format.py -k <nom>      # un seul test
```

`common.py` regroupe le flow matching, l'échantillonneur de Heun, les métriques entre lois et l'inclinaison exponentielle partagés par E1–E3. Les sorties `--quick` (`resultats/*_quick.*`, `figures/*_quick.*`) sont ignorées par git ; seules les sorties complètes sont citées par les pages.
