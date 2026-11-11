# milady-2027

Ressources préparatoires, rapport de stage prospectif et proposition de sujet de thèse pour le stage M2 **« Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems »** (projet ANR MilaDy, ANR-25-CE51-0077 ; CEREA/ENPC et LISN, 2027).

**Site** : <https://knoel99.github.io/milady-2027/>

> Ce site est un projet indépendant. Il n'est ni produit ni validé par l'École nationale des ponts et chaussées, le LISN, l'Observatoire de la Côte d'Azur, l'ANR ou les encadrants du stage. L'offre de référence est le PDF publié par les encadrants : <https://scheng2024.github.io/stage_milady_2027.pdf>. Le rapport de stage est **prospectif** : il est écrit comme s'il concluait le stage, mais ses résultats numériques proviennent uniquement des expériences à petite échelle (CPU) de ce dépôt, décrites et reproductibles dans `experiences/`.

## Ce que contient le site

- **Accueil** (`site/index.qmd`) : l'offre (faits officiels), le projet MilaDy, le parcours en trois étapes.
- **Préparation** (`prep/`) : 8 modules gradués du niveau licence 1 au niveau M2 recherche (calcul vectoriel et Fourier, mécanique des fluides et turbulence, MHD et effet dynamo, systèmes dynamiques, bifurcations et mesures invariantes, probabilités et transport optimal, apprentissage profond, diffusion et flow matching, contraintes physiques). Chaque module : objectifs, plan de travail, cours avec démonstrations, code Python exécuté, exercices corrigés ★/★★/★★★, sources.
- **Encadrants** (`encadrants/`) : travaux de S. Cheng, D. Lucor, C. Nore et Y. Ponty, pistes de thèse et choix argumenté.
- **Rapport de stage** (`rapport/`) : état de l'art, formulation (taxonomie des contraintes, propositions démontrées), méthodes, expériences E1–E3 et résultats, discussion, ouverture vers la thèse.
- **Sujet de thèse** (`these/`) : piste retenue, partie théorique, plan expérimental planifié et évalué (paliers, métriques, risques, calendrier).
- **Expériences** (`experiences/`) : code, résultats JSON et graphiques, et un schéma des trois simulations sur un même gabarit.
- **Schémas interactifs** (`interactifs/`) : six widgets dans le navigateur (flow matching, projection de Leray, contrainte en loi, modèle de Gissinger, dynamo ABC, chaîne de simulation).
- **Calcul et données** (`calcul/`) : l'infrastructure de calcul (format MFF, catalogue, déploiement cloud et Slurm), résumée pour le lecteur, avec deux schémas d'architecture (chaîne de simulation, solveur) et un schéma interactif.
- **Version anglaise** (`en/`) : toutes les pages, aux mêmes chemins sous `en/`.
- **Schémas** (`figures/`) : figures conceptuelles dessinées avec la skill [schematic-figure](https://lgwrightlab.github.io/schematic-figure/) (sources `figure.js`, brief, spec, légende ; sorties SVG/PDF/PNG).

## Reproduire les expériences

Python 3.11+ avec NumPy, SciPy, Matplotlib et PyTorch (CPU suffit).

```bash
cd experiences
python3 e1_gissinger.py            # E1 : loi invariante du modèle de renversements de Gissinger (≈ 2 à 3 h CPU, reprenable)
python3 e2_donnees.py              # E2 : instantanés MHD 2D forcée (≈ 30 min)
python3 e2_mhd2d.py                # E2 : 5 mécanismes de contrainte + volet « en loi » (≈ 1 h)
python3 e3_abc.py                  # E3 : dynamo cinématique ABC, taux de croissance en fonction de Rm (≈ 23 min)
python3 figures.py                 # graphiques
```

Chaque script accepte `--quick` (version réduite, de quelques minutes à une vingtaine de minutes pour E1).

## Calcul HPC et cloud (paquet `milady`, dossier `infra/`)

Le paquet Python `milady` et le dossier `infra/` industrialisent les expériences pour la thèse :
format de données MFF (HDF5 compatible The Well), catalogue PostgreSQL/SQLite des simulations,
modèles et évaluations, stockage S3, suivi MLflow, solveur MHD 3D (PyTorch), entraînement
contraint et évaluation. Guide complet : [`infra/README.md`](infra/README.md) ; contrat :
[`docs/specs/infra.md`](docs/specs/infra.md) ; location dans le cloud :
[`infra/cloud/RECOMMANDATION-CLOUD.md`](infra/cloud/RECOMMANDATION-CLOUD.md).

```bash
git clone https://github.com/knoel99/milady-2027.git && cd milady-2027
sudo infra/deploy/bootstrap_vm.sh            # VM cloud (GPU détecté) : Docker, PostgreSQL, MinIO, MLflow, test de bout en bout
make setup && make smoke RUN=local           # portable, sans Docker (catalogue SQLite, fichiers dans data/)
python -m milady.sweep infra/configs/palier2_abc3d.yaml --scheduler slurm   # cluster Slurm, depuis la frontale
                                             # (image .sif + petit venv : infra/slurm/README-slurm.md)
```

## Construire le site

Prérequis : [Quarto](https://quarto.org) 1.7.32, Python 3, Node.js (vérification KaTeX).

```bash
python3 tools/new_page.py prep/<id> "Titre" "Sous-titre"   # squelette d'une page
python3 tools/render.py --all                              # rendu Quarto + KaTeX épinglé (SRI)
NODE_PATH=<node_modules avec katex@0.19.0> node tools/check_katex.mjs $(find site -name index.html)
python3 tools/check_gates.py                               # sections, exercices, liens, ancres
```

Contrats : `docs/specs/page-contract.md` (structure des pages), `docs/specs/notations.md`, `docs/specs/theorie-brief.md` (énoncés communs au rapport et à la thèse).

## Structure

```
site/                         sources du site, publiées par le workflow pages.yml (racine des URL)
  index.qmd                   accueil
  prep/<id>/index.qmd         modules de préparation
  encadrants/ rapport/ these/ calcul/ interactifs/ experiences/
  en/                         version anglaise, mêmes chemins
  assets/                     paper.css, theme.js, schémas interactifs
  figures/<nom>/              schémas (figure/figure.js, docs/, figure/out/ publié)
  experiences/figures/        graphiques des expériences (écrits par experiences/figures.py)
src/milady/                   paquet Python (format MFF, catalogue, stockage, solveur 3D, entraînement, évaluation)
tests/                        pytest (make test)
experiences/                  scripts E1–E3, common.py, resultats/*.json, digest.md
infra/                        déploiement : Docker, VM cloud, Slurm/Apptainer, configurations, schéma SQL
video/                        moteur du film (projet Node autonome)
docs/                         documentation des développeurs : specs/ (contrats, bases de faits), ARCHITECTURE.md
tools/                        rendu et contrôles du site
.github/workflows/            pages.yml (rendu et déploiement), drive-upload.yml
```

## Dépôt et publication

Ce dépôt (`knoel99/milady-2027`) est publié sur <https://knoel99.github.io/milady-2027/> par le workflow `.github/workflows/pages.yml` : à chaque poussée sur `main`, il rend toutes les pages de `site/` (Quarto 1.7.32, `tools/render.py`), lance les contrôles (`check_gates.py`, `compare_fr_en.py --all`, KaTeX) et publie `site/` sans les sources. Réglage requis une fois : Settings → Pages → Source « GitHub Actions ». Les URL publiques sont les chemins de `site/`. La page d'accueil du site personnel (`knoel99/knoel99.github.io`) y renvoie par une carte.

Le projet a d'abord été développé dans le dossier `milady-2027/` du dépôt du site personnel, puis extrait ici avec tout son historique (`tools/export_repo.sh`, qui repose sur `git subtree split`). Le développement se poursuit désormais directement dans ce dépôt : modifier les sources, rendre les pages touchées, lancer les contrôles ci-dessus (dont `python3 tools/compare_fr_en.py <page>` pour la parité entre le français et l'anglais), puis pousser.

## Licence

Code et textes : Apache 2.0 (`LICENSE`). Les textes officiels cités (offre, résumé ANR) restent la propriété de leurs auteurs. KaTeX (MIT) est chargé depuis jsDelivr.
