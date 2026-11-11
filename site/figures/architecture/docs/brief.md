# Brief — figure « architecture »

- **Mode** : design. **Format** : journal, pleine largeur 183 mm (page Calcul et données, section « La chaîne de traitement »).
- **Lecteur** : les encadrants (MHD numérique, apprentissage), le candidat, la personne qui déploiera l'infrastructure.
- **Phrase à retenir** : une campagne YAML traverse sept modules qui rangent les fichiers lourds dans un stockage objet et leur trace dans un catalogue relationnel ; la même chaîne tourne sur un portable, une VM GPU ou un cluster Slurm, seuls changent les services qui l'hébergent.

## Idées clés (ordre d'importance)

1. Sept étapes, un module chacune, dans l'ordre causal : campagne, lancement, simulation, stockage, jeu de données, entraînement, évaluation (numérotation de la table de la page Calcul).
2. Deux magasins aux rôles distincts : les fichiers lourds (stockage objet, chemin `{campagne}/{uuid}/fields.h5`) et les métadonnées (tables du catalogue) ; chaque étape écrit au catalogue.
3. Le même UUID relie la simulation au catalogue et son fichier ; la partie simulations du catalogue se reconstruit à partir des fichiers (`milady.catalog ingest`).
4. Trois cibles réalisent la même chaîne avec des services différents : portable (venv, SQLite, dossier local), VM (Docker Compose : PostgreSQL, MinIO, MLflow, worker, Jupyter, ports sur 127.0.0.1 et tunnel SSH), cluster (image Apptainer, tableaux de jobs à 1 GPU par simulation, `torchrun` par nœud, SQLite sur `$WORK`, fichiers sur `$SCRATCH`, puis copie vers S3 et ingestion).
5. Exemple suivi d'un bout à l'autre : la campagne `palier2_tg3d` (Re × Pm = 4 × 3, 12 simulations), entraînée par `train_fm3d` (validation Re = 100, Pm = 1 ; test Re = 50, Pm = 2).

## Ce que la figure ne doit pas laisser croire

- que la chaîne a tourné sur un GPU, un vrai cluster ou une VM louée (non testé) ;
- que tout le catalogue SQLite d'un cluster est transféré (seules les simulations, leurs fichiers et diagnostics sont ingérés) ;
- que les fichiers sont immuables par construction (`--force` les réécrit) ;
- que Docker ou MLflow sont nécessaires sur un portable ;
- qu'un ordre de déploiement entre cibles est imposé.

## Portée

Niveau modules et services. L'intérieur du solveur et la correspondance champ par champ entre fichier MFF et catalogue sont dans la figure « solveur » ; les simulations des expériences E1–E3 dans la figure « simulations ».

## Style

Hérité des figures du site (cadre, plan-these, taxonomie) : Arial, gris neutres pour l'infrastructure, couleur réservée aux données selon la clé du site (vert = paramètres de contrôle, bleu = u, vermillon = B, violet = modèle génératif, ambre = mesures en loi), pastilles numérotées gris foncé, finition illustrée pour les vignettes.
