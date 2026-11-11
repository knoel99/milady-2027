# Faits — figure « architecture »

Chaque libellé affiché, avec sa source dans le dépôt (chemins relatifs à la racine). Les libellés anglais (figure-en.js) suivent ceux en français.

## Panneau a — chaîne d'une campagne

| Libellé FR | Libellé EN | Source |
|---|---|---|
| « Chaîne d’une campagne » | « Campaign pipeline » | calcul/index.qmd, section « La chaîne de traitement » (tableau des 7 étapes) |
| « Campagne », « Lancement », « Simulation », « Stockage », « Jeu de données », « Entraînement », « Évaluation » | « Campaign », « Launch », « Simulation », « Storage », « Dataset », « Training », « Evaluation » | calcul/index.qmd l. 86-94 ; docs/ARCHITECTURE.md § 1 |
| « 1 » … « 7 » | idem | numérotation du tableau de calcul/index.qmd |
| « Re », « Pm » | idem | infra/configs/palier2_tg3d.yaml : `sweep: Re: [25, 50, 100, 200]`, `Pm: [0.5, 1.0, 2.0]` |
| « 12 simulations » | « 12 simulations » | palier2_tg3d.yaml, description « (12 simulations) » |
| « ×12 » | idem | 12 tâches, une par point (src/milady/sweep.py, en-tête) |
| « UUID v5 » | idem | src/milady/sweep.py, en-tête : « identifiant déterministe (UUID v5 du nom de campagne, de l'indice, des paramètres…) » |
| « u », « B », « u, B · 64³ » | idem | palier2_tg3d.yaml `mode: dynamic` (u et B), `grid: N: 64` ; src/milady/sim/mhd3d.py, en-tête |
| « 64³ » | idem | palier2_tg3d.yaml `grid: N: 64` |
| vignette du cube : |u| de l'écoulement de Taylor–Green initial | — | palier2_tg3d.yaml `u0: laminar` (« écoulement TG d'amplitude U_ref au départ »), `kf: 2` ; champ TG : src/milady/eval/metrics.py `taylor_green_field` (mêmes définitions que mhd3d) |
| « fields.h5 » | idem | src/milady/storage.py, en-tête : `{MILADY_STORAGE_URI}/{campagne}/{uuid_simulation}/{kind}.h5` ; src/milady/sim/run.py étape 4 |
| « dimensions/ », « t1_fields/ », « milady_* », « HDF5 · The Well » | idem | src/milady/data/format.py, en-tête (« La hiérarchie suit exactement le format HDF5 de The Well ») |
| « train », « val », « test », « par point (Re, Pm) » | « train », « val », « test », « by (Re, Pm) point » | infra/configs/train_fm3d.yaml : `auto_dataset: val: {Re: 100, Pm: 1.0}`, `test: {Re: 50, Pm: 2.0}` ; les 10 autres points en entraînement |
| « A_u, A_B » (affiché « Au, AB »), « ∇× », « u, B », « torchrun · DDP » | idem | src/milady/train/fm3d.py, en-tête : potentiels vecteurs A_u, A_B, décodage u = ∇×A_u, B = ∇×A_B |
| « E(k) », « k », « référence », « généré », « spectres, bilans » | « E(k) », « k », « reference », « generated », « spectra, budgets » | src/milady/eval/metrics.py, en-tête : spectres en couronnes, comparaison d'un ensemble généré à une référence ; **forme illustrative** (aucune évaluation 3D n'a encore tourné) |
| `infra/configs/`, `milady.sweep`, `milady.sim`, `milady.storage`, `milady.train.data`, `milady.train.fm3d`, `milady.eval` | idem | calcul/index.qmd l. 86-94 ; étape 5 : le jeu de données est créé par `milady.train.data` au premier entraînement (`data.auto_dataset`, src/milady/train/data.py l. 740-820), `milady.catalog` le stocke |
| « Catalogue · PostgreSQL ou SQLite » | « Catalog · PostgreSQL or SQLite » | docs/ARCHITECTURE.md § 3 « Catalogue » ; src/milady/catalog/api.py |
| `campaign`, `simulation · job`, `diagnostic`, `file`, `dataset`, `model`, `evaluation` | idem | calcul/index.qmd l. 86-94 (colonne « Où c'est enregistré ») ; src/milady/catalog/models.py |
| « Fichiers · S3, MinIO ou disque » | « Files · S3, MinIO or disk » | src/milady/storage.py, en-tête (schémas `s3://`, chemins locaux) |
| `last.pt` | idem | src/milady/train/fm3d.py l. 1103 : `last.pt`, `final.pt` dans le dossier du run |
| « même UUID » | « same UUID » | docs/ARCHITECTURE.md l. 52-53 : « la simulation reçoit le même identifiant au catalogue et dans le fichier (`milady_uuid`) » |
| « ingest » | idem | `python -m milady.catalog ingest` : simulations, fichiers et diagnostics seulement (src/milady/catalog/api.py `ingest_mff` ; calcul/index.qmd l. 96) |

## Panneau b — trois cibles

| Libellé FR | Libellé EN | Source |
|---|---|---|
| « Trois cibles, même chaîne » | « Three targets, one pipeline » | calcul/index.qmd l. 50 |
| « Portable », « sans GPU » | « Laptop », « no GPU » | calcul/index.qmd l. 56 |
| « VM cloud GPU », « Docker Compose » | « Cloud GPU VM », « Docker Compose » | calcul/index.qmd l. 54 ; infra/docker/docker-compose.yml |
| « Cluster Slurm », « Apptainer » | « Slurm cluster », « Apptainer » | calcul/index.qmd l. 55, 78 ; infra/slurm/apptainer.def |
| « Exécution », « Fichiers », « Catalogue », « Suivi » | « Execution », « Files », « Catalog », « Tracking » | docs/ARCHITECTURE.md § 2, tableau (lignes Exécution, Fichiers, Catalogue, Suivi) |
| « venv, processus » | « venv, processes » | Makefile `setup` (.venv) ; src/milady/sweep.py `--scheduler local` (un sous-processus par simulation) |
| « data/store/ » | idem | src/milady/storage.py l. 12 (défaut `file://<racine>/data/store`) |
| « SQLite », « data/catalog.sqlite » | idem | src/milady/catalog/__main__.py l. 8 |
| « metrics.jsonl » | idem | src/milady/train/fm3d.py, en-tête : « journal MLflow si MLFLOW_TRACKING_URI est défini (sinon metrics.jsonl) » |
| « conteneur worker-gpu », « milady:gpu » | « worker-gpu container », « milady:gpu » | docker-compose.yml l. 213-220 (profil gpu, image `milady:gpu`) |
| « MinIO :9000 » | idem | docker-compose.yml l. 117-118 (port 9000, console 9001) |
| « PostgreSQL 16 :5432 » | idem | docker-compose.yml l. 82, 94-95 (`postgres:16.14-bookworm`, port 5432) |
| « MLflow :5000 » | idem | docker-compose.yml l. 191-192 |
| « tableau de jobs », « 1 GPU par simulation » | « job array », « 1 GPU per simulation » | infra/slurm/gen_data.sbatch (`--gres=gpu:1`, « UNE simulation (1 GPU) par élément ») |
| « torchrun par nœud » | « torchrun per node » | infra/slurm/train.sbatch, en-tête |
| « $SCRATCH » | idem | infra/slurm/env.sh l. 63, 73 (fichiers sous `$SCRATCH/milady/store`) |
| « SQLite sur $WORK » | « SQLite on $WORK » | infra/slurm/env.sh l. 68, 72 |
| « MLflow SQLite » | idem | infra/slurm/env.sh l. 74 (`sqlite:///$WORK/milady/mlflow.db`) |
| « nœuds sans Internet » | « nodes without Internet » | calcul/index.qmd l. 78 |
| « copie vers S3 » | « copy to S3 » | docs/ARCHITECTURE.md § 2 (`mc mirror / rclone depuis la frontale`) ; infra/slurm/README-slurm.md § 5 |
| « ingest » (sur la VM, des fichiers copiés vers PostgreSQL) | idem | src/milady/catalog/api.py `ingest_mff` (lit les fichiers MFF) ; infra/slurm/README-slurm.md § 5 ; le catalogue SQLite du cluster n'est pas transféré (calcul/index.qmd l. 78) |

## Retirés de la figure, gardés pour la légende

- ports liés à 127.0.0.1 et accès par tunnel SSH (docker-compose.yml, `${BIND_ADDR:-127.0.0.1}` ; calcul/index.qmd l. 76) ;
- commandes d'installation `make setup`, `sudo infra/deploy/bootstrap_vm.sh`, `make sif` puis `sbatch` (déjà dans le tableau « Démarrer » de la page).
