# Spec — figure « architecture »

## Structure

Un pipeline (panneau a : sept étapes dans l'ordre causal, de gauche à droite) au-dessus de sa réalisation (panneau b : une grille rôles × cibles). Le panneau a est l'abstraction, le panneau b ses trois réalisations ; la correspondance passe par les rôles (Exécution, Fichiers, Catalogue, Suivi) dessinés avec les mêmes glyphes et les mêmes gris dans les deux panneaux (P2, P13). Pourquoi ce squelette : la phrase à retenir a deux moitiés (« une chaîne » / « trois cibles »), et la seconde n'a de sens que rapportée à la première.

## Concepts envisagés

| Concept | Panneaux | Esquisse | Lecture en 5 s | Fidèle | État de la donnée dessiné (P1) | Correspondance (P2) / comparaison (P3) | Explique ? (P4) |
|---|---|---|---|---|---|---|---|
| **A. Chaîne, deux rails, trois cibles** | a : sept étapes + rails « catalogue » et « fichiers » ; b : grille rôles × cibles | étapes numérotées avec une vignette de la donnée (grille de paramètres, tâches, champ 3D, fichier, découpage, réseau, spectre) ; prises verticales vers deux rails nommés ; en dessous, trois colonnes encadrées alignées sur quatre rangées de rôles | oui : la chaîne se lit en ligne, les rails disent « deux magasins », les colonnes « trois cibles » | oui, aucun enchaînement entre cibles imposé | oui (vignettes de la campagne suivie, palier2_tg3d) | oui : mêmes rôles, mêmes glyphes ; trois cibles sur un même gabarit | explique |
| **B. Couloirs** | un panneau : trois couloirs horizontaux (portable, VM, cluster), étapes placées dans le couloir où elles tournent pour une campagne simulée sur cluster et entraînée sur la VM | flèches qui changent de couloir (copie vers S3, ingestion) | moyenne : il faut suivre les changements de couloir | risque : laisse croire à un ordre de déploiement imposé (contrainte négative) | partiel | non : pas de gabarit commun aux cibles | explique, mais un cas particulier |
| C. Catalogue au centre | catalogue en moyeu, étapes en couronne, cibles en légende | | faible : l'ordre causal se perd | oui | non | non | inventaire |

Retenus pour les deux brouillons (profondeur full) : **A** et **B**. C est écarté (pas d'ordre de lecture).

## Carte (concept A)

**Takeaway (one sentence):** une campagne YAML traverse sept modules qui rangent les fichiers lourds dans un stockage objet et leur trace dans un catalogue relationnel ; la même chaîne tourne sur un portable, une VM GPU ou un cluster Slurm.
**Size:** width 183 mm × height 128 mm
**Hero:** none, figure d'architecture logicielle (P1 « when not », P30 « when not ») ; trois petites icônes de machines dessinées en vector 3D (`L.obliqueBox`), finition illustrée ; vignette du champ calculée (écoulement de Taylor–Green initial, analytique).

### Panneaux
| Panel | Job (one line) | Position / share of the figure |
|---|---|---|
| a | les sept étapes d'une campagne et ce que chacune écrit dans les deux magasins | haut, 183 × 66 mm |
| b | les services qui réalisent chaque rôle sur les trois cibles | bas, 183 × 58 mm |

### Composants
| Panel | Component | Label (exact text) | Look | Source |
|---|---|---|---|---|
| a | en-tête d'étape ×7 | « 1 Campagne », « 2 Lancement », « 3 Simulation », « 4 Stockage », « 5 Jeu de données », « 6 Entraînement », « 7 Évaluation » | pastille gris foncé + nom gras 6,5 pt | draw (pastille du site, `badge` de plan-these) |
| a | vignette 1 : grille de paramètres | « Re », « Pm », « 12 points » | 4 × 3 points verts sur une feuille YAML pâle | draw (`L.circle`), valeurs de palier2_tg3d.yaml |
| a | vignette 2 : tâches | « ×12 », « UUID v5 » | trois cartes empilées, un point vert chacune, points de suspension | draw (`L.rect`, `L.dots`) |
| a | vignette 3 : champ 3D | « u », « B », « 64³ » | cube périodique, |u| du Taylor–Green initial sur trois faces (gris), flèches u bleue et B vermillon | compute (TG analytique) + draw (`L.obliqueBox`, `L.pixelImage` sur faces) |
| a | vignette 4 : fichier | « fields.h5 » | feuille avec arbre HDF5 (trois lignes) | draw |
| a | vignette 5 : découpage | « val », « test » | grille 4 × 3 : 10 points pleins, un point cerclé (val), un anneau vide (test) | draw ; train_fm3d.yaml |
| a | vignette 6 : modèle | « A_u, A_B », « ∇× » | boîte violette avec petit réseau | draw (`L.network`) |
| a | vignette 7 : évaluation | « généré », « référence » | mini spectre log-log, référence gris plein, généré ambre tireté (forme illustrative) | draw (forme indicative, dite telle dans la légende) |
| a | modules ×7 | `infra/configs/`, `milady.sweep`, `milady.sim`, `milady.storage`, `milady.train.data`, `milady.train.fm3d`, `milady.eval` | monospace 5,5 pt gris foncé | draw |
| a | rail catalogue | « Catalogue · PostgreSQL ou SQLite » | bande gris clair arrondie | draw |
| a | prises catalogue ×7 | `campaign`, `simulation · job`, `diagnostic`, `file`, `dataset`, `model`, `evaluation` | trait vertical + point + nom de table monospace | draw (`L.line`, `L.text`) |
| a | rail fichiers | « Fichiers · stockage objet S3, MinIO ou disque » | bande gris moyen arrondie | draw |
| a | prises fichiers | `fields.h5` (étape 4), `last.pt` (étape 6) | trait vertical + point | draw |
| a | lien UUID | « même UUID » | tireté gris entre `file` et `fields.h5` | draw |
| a | ingestion | « ingest » | flèche courbe tiretée du rail fichiers vers le rail catalogue, à droite | draw |
| b | en-têtes de colonnes | « Portable », « VM cloud GPU », « Cluster Slurm » + sous-titres « sans GPU », « Docker Compose », « Apptainer » | icône 3D + nom gras | draw (`L.obliqueBox`) |
| b | rangées | « Exécution », « Fichiers », « Catalogue », « Suivi » | titres gras à gauche ; Fichiers et Catalogue sur les mêmes gris que les rails | draw |
| b | cellules ×12 | voir facts.md | 1–2 lignes, monospace pour les chemins et commandes | draw |
| b | pieds de colonne | `make setup`, `bootstrap_vm.sh`, `make sif` + `sbatch` | monospace | draw |
| b | flèches entre cibles | « copie vers S3 », « ingest » | tiretés du cluster vers la VM | draw |
| b | accès | « tunnel SSH » | tireté du portable vers la VM | draw |

### Relations
| From | To | Kind | Drawn as |
|---|---|---|---|
| étape k | étape k+1 (k = 1…6) | flux | chevrons gris entre vignettes |
| chaque étape | rail catalogue | écrit | prise verticale + point |
| étapes 4 et 6 | rail fichiers | écrit | prise verticale + point |
| rail fichiers | rail catalogue | ingestion (partie simulations) | flèche courbe tiretée |
| fichier (4) | ligne `file` (4) | même UUID | tireté court |
| cluster Fichiers | VM Fichiers | copie | flèche tiretée vers la gauche |
| cluster Catalogue | VM Catalogue | ingestion | flèche tiretée vers la gauche |
| portable | VM | accès | flèche tiretée, « tunnel SSH » |

### Conventions
- Le temps et l'ordre causal vont de gauche à droite (P8).
- Couleur réservée aux données (clé du site) : vert = paramètres de contrôle (Re, Pm), bleu = u, vermillon = B, violet = modèle génératif, ambre = mesures en loi ; tout le reste en gris (P15, P16).
- Le même objet est dessiné de la même façon partout : la grille 4 × 3 en vignettes 1, 2 et 5 ; les rails et les rangées Fichiers / Catalogue (P27).
- Noms de modules, tables, chemins et commandes en monospace.

### Contraintes négatives
- Aucun chiffre de performance (aucun temps GPU mesuré).
- Pas de flèche qui ordonne les cibles entre elles (seulement les synchronisations documentées).
- Pas de « immuable », pas de « transfert complet » du catalogue SQLite.
- Pas de logo de fournisseur ou de produit.
