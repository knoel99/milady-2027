# Louer du calcul pour MilaDy 2027 : quel fournisseur, quelle machine, et comment exploiter les résultats

Rédigé le 2026-11-08, révisé le même jour, pour préparer le stage MilaDy 2027 (CEREA/ENPC, S. Cheng
et D. Lucor). Périmètre : les calculs manquants M1 et M3 à M8 de l'inventaire vidéo, puis la collecte
des résultats et leur exploitation (pages du site, scènes en attente de la vidéo).

Rien n'a été lancé pour écrire ce document : ni simulation, ni banc, ni entraînement. Le dimensionnement
vient du code et de la documentation du dépôt (annexe `dimensionnement.md`). Les prix ont été relus à la source le 2026-11-08 ; la
liste des sources, avec leur date de lecture, est au §9, et ce qui n'a pas pu être vérifié au §10.
Les défauts de code signalés ici ont été établis **par lecture du code**, sans exécution.

**Révision du 2026-11-08**, après deux contre-vérifications (prix, puis code) : prix Scaleway
confirmés HT ; témoin de M7, requête SQL, région S3, `git clone`, essai M8, taux de Taylor–Green,
portée de `make backup`, repli OVHcloud et budgets corrigés ; passage L4 → L40S et prix du profil
CPU ajoutés.

---

## 0. D'abord, en parler aux encadrants

L'objectif est de comprendre le sujet, puis de poser les bonnes questions aux encadrants **avant** de
lancer le moindre calcul. La vidéo explicative et sa fiche « Questions pour les encadrants » servent
à cela. Plusieurs réponses peuvent rendre la location inutile, ou changer ce qu'il faut calculer :

- **Moyens de calcul.** Le CEREA (ENPC) ou le LISN ont-ils des GPU accessibles à un stagiaire ?
  Existe-t-il déjà un projet GENCI (Jean Zay) où vous ajouter ? Si oui, le dépôt est prêt pour Slurm
  et Apptainer (`infra/slurm/README-slurm.md`), et la location ne sert plus qu'à un essai.
- **Priorités.** Les campagnes périodiques prévues (Taylor–Green et ABC à 64³, générateur 3D) les
  intéressent-elles, ou préfèrent-ils commencer par leurs propres données (LATU, SFEMaNS) ?
- **Paramètres.** Convention de forçage Taylor–Green pour comparer aux seuils publiés, plage de Re et
  de Pm, résolution (64³ suffit-il à Re ≥ 100 ?), nombre de trajectoires par point (`n_traj`).
- **Mesures.** Quelles mesures veulent-ils voir sur les champs générés (hélicités, topologie,
  dispersion des bilans) ? Elles se programment avant de louer (§4.1).
- **Diffusion.** Peut-on publier ces résultats sur le site et dans la vidéo ?

Le reste du document suppose que la location reste utile après cet échange.

---

## 1. En bref

**Recommandation : Scaleway, instance `L4-1-24G`, zone Paris `fr-par-2`.**

- **Machine.** GPU NVIDIA L4 de 24 Go, 8 vCPU, 48 Gio de RAM, à **0,7875 €/h HT** (0,013125 €/min),
  soit 0,945 €/h TTC [SCW-API]. Les prix affichés par Scaleway sont HT [SCW-BILL].
- **Image et disque.** Image « Ubuntu Noble GPU OS 13 (NVIDIA) », avec pilote et environnement
  Docker NVIDIA [SCW-IMG], et un volume bloc de 150 Go (« Low Latency 5K »).
- **Stockage.** Un bucket S3 de 25 Go en région `fr-par`.
- **Durée.** Une session de **≈ 6 à 12,5 heures facturées** pour tout le scénario A : les
  configurations telles quelles, à 64³.

**Budget du scénario A** (EUR TTC ; calcul, disque, IP, stockage et sortie compris ; hypothèses au §8) :

| Bas | Probable | Haut |
|---|---|---|
| **≈ 6 €** | **≈ 16 €** | **≈ 38 €** |

**Si le pilote montre que 64³ ne résout pas Re ≥ 100 (scénario B)**, payer d'abord la seule
variante B1 : les 3 simulations à Re = 100 en 128³, sur la même L4, pour ≈ 1 à 23 € de plus
(≈ 7 € probable). Pour Re = 200 en 256³, deux voies :

- passer sur la `L40S-1-48G` du même compte (1,47 €/h HT) [SCW-API], avec la procédure du §5.14.
  B1 + B2 coûteraient alors **≈ 15 / 85 / 235 € TTC** (bas / probable / haut). L'écart vient de ce
  qu'aucun temps GPU n'a été mesuré ;
- de préférence, garder le 256³ pour Jean Zay (GENCI, gratuit, §8.4).

**Solution de repli : OVHcloud, instance `l4-90`, région Gravelines (GRA11).**

- **Machine.** Même GPU L4, mais 22 vCPU, 90 Go de RAM et 400 Go de NVMe, à **0,75 €/h HT**
  (0,90 € TTC) [OVH-CAT].
- **Avantages.**
  - 200 € HT de crédit d'essai, valables un mois. Ce crédit s'active **automatiquement à la création
    du projet Public Cloud** [OVH-QUOTA] : ne créer ce projet que la semaine de la location.
  - Stockage S3 à 0,007 €/Go·mois, sans frais de sortie [OVH-CAT].
- **Inconvénients.**
  - Le pilote NVIDIA est à installer soi-même [OVH-DOC].
  - Une instance **arrêtée reste facturée** au tarif plein [OVH-BILL] : il faut la supprimer, ou la
    mettre en « shelve », entre deux sessions.
  - Le quota GPU d'un compte en essai n'est pas publié [OVH-QUOTA] (**non vérifié**).
  - Deux pages de la documentation se contredisent sur la granularité de facturation : à la seconde,
    ou par heure entamée [OVH-BILL].

### Pourquoi ce choix

1. **Le besoin est petit.** Le scénario A représente ≈ 1 à 4,5 heures-GPU de calcul réel
   (`dimensionnement.md` §3.1) :
   - les simulations 64³ sont limitées par le lancement des noyaux, pas par la puissance du GPU ;
   - l'entraînement (47,8 M de paramètres d'après le code) demande 2 à 4 Go de VRAM.

   Une L4 de 24 Go suffit. Un H100 coûterait 3,6 fois plus cher (2,8665 €/h HT [SCW-API]) sans
   aller plus vite à 64³ (estimation de `dimensionnement.md` §1.2, non mesurée). Le vrai coût est la mise
   en route et le débogage du chemin GPU, qui n'a jamais été exécuté.
2. **Il faut une VM complète où Docker tourne.** `bootstrap_vm.sh` vise Ubuntu 22.04 ou 24.04, en
   root, puis lance `docker compose` (PostgreSQL, MinIO, MLflow). L'image `milady:gpu` exige un
   pilote NVIDIA ≥ 525 (`Dockerfile.gpu`, l. 11), ce que le script ne vérifie pas. L'image GPU de
   Scaleway fournit le pilote et Docker [SCW-IMG] : c'est le chemin le plus court.
3. **France et Europe.** Paris pour Scaleway, Gravelines pour OVHcloud : les données restent en
   France, et la facture est en euros. Bonus : l'IDRIS accepte comme point de connexion à Jean Zay
   une « instance Cloud d'un fournisseur dont le siège social et les infrastructures sont situés en
   France » [EDARI-DOC]. Une machine précise reste toutefois à faire accepter (**non vérifié**).
4. **Facturation.** À la minute pour les GPU, avec un minimum de 60 min par période de marche
   [SCW-BILL]. Il ne faut donc pas multiplier les arrêts et redémarrages courts.
5. **Quota.** Une vérification d'identité en ligne, à boucler en 15 minutes, débloque une L4 et une
   L40S sans ticket [SCW-QUOTA][SCW-ID].
   - Chez AWS, le quota GPU d'un compte neuf vaut 0 [AWS-Q].
   - Chez Google Cloud, les GPU sont interdits pendant l'essai gratuit [GCP-FREE].
   - Chez Google Cloud et Azure, la valeur par défaut du quota n'est pas confirmée par la
     documentation (**non vérifié**).
6. **Prix.** Parmi les VM GPU de 24 Go relevées en Europe, louées à l'heure sans frais
   d'installation, la `l4-90` d'OVHcloud (0,75 €/h HT) est la moins chère. La L4 de Scaleway vient
   juste derrière (+5 %). Scaleway l'emporte par la mise en route : pilote et Docker préinstallés,
   quota sans ticket. Les places de marché (Vast.ai, RunPod) sont moins chères, mais ce sont des
   conteneurs, ou des hôtes à la fiabilité variable.

**À ne pas louer :**

- H100, A100 80 Go ou plusieurs GPU, sauf si le banc GPU mesuré dit le contraire.
- Les GPU Blackwell (RTX PRO 6000, RTX 50xx, B200, GEX45 de Hetzner) : l'image `milady:gpu` serait
  à reconstruire en CUDA 13 (`Dockerfile.gpu`, l. 11–14).
- Les pods RunPod : `docker compose` y est interdit [RP-OV].
- Un compte AWS, Google Cloud ou Azure pour démarrer vite, à cause du quota GPU.

---

## 2. Comparatif des options retenues ou écartées

Les prix sont HT, à la demande, pour une instance à 1 GPU, relus le 2026-11-08. Les prix en USD ne
sont pas convertis : le taux de change n'a pas été vérifié.

**Fournisseurs européens :**

| Fournisseur, instance | GPU, VRAM | vCPU / RAM | Prix / h HT | VM ou conteneur | Obstacle d'accès | Verdict |
|---|---|---|---|---|---|---|
| **Scaleway `L4-1-24G`** (Paris) | L4, 24 Go | 8 / 48 Gio | **0,7875 €** (0,945 TTC) [SCW-API] | VM, pilote + Docker préinstallés [SCW-IMG] | vérif. d'identité en ligne (15 min) → 1 L4 + 1 L40S [SCW-QUOTA] ; cartes prépayées et virtuelles refusées [SCW-BILL] | **Recommandé** (scénario A) |
| Scaleway `L40S-1-48G` (`fr-par-2`, Varsovie) | L40S, 48 Go | 8 / 96 Gio | 1,470 € (1,764 TTC) [SCW-API] | VM | même quota | **Scénario B** (128³/256³) |
| **OVHcloud `l4-90`** (GRA11) | L4, 24 Go | 22 / 90 Go + 400 Go NVMe | **0,75 €** (0,90 TTC) [OVH-CAT] | VM, pilote à installer [OVH-DOC] | quota d'un compte en essai non publié (**non vérifié**) ; 200 € de crédit d'essai, 1 mois après création du projet [OVH-QUOTA] | **Repli n° 1** |
| OVHcloud `l40s-90` (GRA11) | L40S, 48 Go | 15 / 90 Go | 1,40 € (1,68 TTC) [OVH-CAT] | VM | idem | repli pour le scénario B |
| Verda (ex-DataCrunch) `1x RTX A6000` (Helsinki) | A6000, 48 Go | 10 / 60 Go | 0,7591 € ; spot 0,3795 € [VERDA] (HT ou TTC : **non vérifié**) | VM ; Docker **non vérifié** | prépayé ; solde à zéro → instances arrêtées et volumes supprimés, restaurables 96 h [VERDA-BILL] | option économique, plus risquée |
| Nebius L40S (Finlande, eu-north1) | L40S, 48 Go | 8+ / 32+ Go | dès 1,55 $ ; préemptible dès 0,74 $ [NEB] | VM, images CUDA [NEB-IMG] | quota de 8 L40S par défaut [NEB-Q] ; paiement en USD, 25 $ minimum | alternative, hors France |
| Hetzner GEX45 (Helsinki, dédié) | RTX PRO 4000 **Blackwell**, 24 Go | 14 cœurs / 64 Go | 0,3429 € **+ 209 € d'installation** [HETZ] | serveur dédié | — | écarté (installation, Blackwell) |

**Grands clouds et places de marché :**

| Fournisseur, instance | GPU, VRAM | vCPU / RAM | Prix / h HT | VM ou conteneur | Obstacle d'accès | Verdict |
|---|---|---|---|---|---|---|
| Google Cloud `g2-standard-16` (europe-west4) | L4, 24 Go | 16 / 64 Go | 1,206 $ ; Spot 0,723 $ [GCP-GCC] (site tiers) | VM | GPU interdits pendant l'essai gratuit [GCP-FREE] ; quota à demander, valeur par défaut non publiée [GCP-QUOTA] | pas pour démarrer vite |
| AWS `g6.4xlarge` (Paris) | L4, 24 Go | 16 / 64 Gio | 1,680 $ [AWS-OD] | VM | quota « G and VT » de **0** [AWS-Q] ; délai d'obtention **non vérifié** (témoignages seulement) | non |
| Azure `NC8as_T4_v3` (France Central) | T4, 16 Go | 8 / 56 Gio | 0,7882 € (0,878 $) [AZ-API] | VM | quota par défaut de 0 selon une réponse Q&A de 2022, pas la doc [AZ-Q0] (**non vérifié**) | non (T4 : prise en charge par l'image **non vérifiée**) |
| Lambda `1x A6000` / `1x A10` | 48 / 24 Go | 14 / 100 ; 30 / 226 Gio | 1,09 $ / 1,29 $ à partir du 16/11/2026, hors taxes [LA-PRICE] ; avant cette date, prix visibles seulement une fois connecté (**non vérifié**) | VM, Lambda Stack [LA-DOC] | pas de quota annoncé ; région UE **non vérifiée** | repli hors UE |
| Vast.ai, mode VM, RTX 4090 (Europe) | 24 Go | 12–32 vCPU | min. 0,486 $ (Suisse), médiane 0,670 $ (instantané du marché, 9 offres en Europe dont le Royaume-Uni) [VA-API] | VM en mode VM [VA-VM] | pas de quota ; hôtes indépendants | repli économique |
| RunPod, pod L4 / RTX A5000 | 24 Go | 12 / 50 Go ; 9 / 25 Go | 0,59 $ / 0,27 $ [RP-PRICE] | **conteneur, `docker compose` interdit** [RP-OV] | aucun | écarté pour ce dépôt |

---

## 3. Ce qu'il faut louer exactement

| Élément | Choix | Pourquoi |
|---|---|---|
| Instance | Scaleway `L4-1-24G`, zone **`fr-par-2`** | la L40S n'existe qu'en `fr-par-2` et à Varsovie [SCW-API] : rester dans la même zone et la même région de bucket facilite le scénario B (§5.14) |
| Image | « Ubuntu Noble GPU OS 13 (NVIDIA) » (Ubuntu 24.04) [SCW-IMG] | `bootstrap_vm.sh` n'a été testé qu'en `--cpu`, hors cloud, Docker déjà présent. La doc Scaleway ne garantit pas le plugin `docker compose` (§5.1) |
| Disque | volume bloc **Low Latency 5K** de **150 Go** (200 Go pour le scénario B) | images Docker ≈ 15 Go ; données ≈ 19 Go ; marge (`dimensionnement.md` §4). 0,00013 €/Go·h, soit ≈ 0,47 € HT par jour. Le type « Volume SSD », au même prix, est en fin de commercialisation [SCW-API][SCW-BLK] |
| IP publique | une IPv4 | ≈ 0,005 €/h HT, soit ≈ 0,12 € par jour. L'API ne donne pas l'unité de temps : l'heure est supposée [SCW-API] |
| Réseau | groupe de sécurité : **SSH (22) seul** en entrée | les services n'écoutent que sur 127.0.0.1 ; accès par tunnel SSH (`infra/README.md` §2.4, §10) |
| Stockage objet | 1 bucket en `fr-par`, classe Standard Multi-AZ, **≈ 25 Go** (100 Go pour le scénario B) | les fichiers MFF et les points de contrôle survivent à la suppression de la VM. ≈ 0,016 €/Go·mois [SCW-API] (unité horaire supposée ; ≈ 0,015 selon la page officielle vue par un moteur de recherche). **750 Go gratuits pendant 90 jours** pour un nouveau compte, à activer à la main dans la console, sans pause possible : l'activer le jour de la location [SCW-S3FAQ] |
| Clé d'accès S3 | une clé API dédiée, limitée au stockage objet du projet | `infra/README.md` §2.5 et §10. La restriction au seul bucket est **non vérifiée** |
| Durée | **une session de ≈ 6 à 12,5 h**, puis suppression de la VM | §5 |
| Alerte | alerte de budget à ≈ 50 €, si la console le permet (**non vérifié**) | `infra/README.md` §8 |

**À ne pas louer :**

- **Pas de H100 ni d'A100 80 Go.** À 64³, le pas de temps dure ≈ 3–10 ms, limité par le lancement
  des ≈ 430 noyaux d'un pas RK4, et dépend peu du GPU (`dimensionnement.md` §1.2, estimation non mesurée).
  L'entraînement tient dans 2–4 Go. Seul un banc qui contredirait ces estimations justifierait plus
  gros.
- **Pas de multi-GPU** : 1 400 itérations d'entraînement n'en tirent rien, et chaque simulation 64³
  tient sur une carte.
- **Pas de GPU Blackwell**, et pas de T4 tant que la compatibilité de l'image n'est pas vérifiée.
- **Pas d'instance spot** chez Scaleway : le catalogue n'en contient aucune [SCW-API]. Le spot ne
  vaut la peine que pour le scénario B chez un autre fournisseur, avec les précautions du §5.13.
- **Pas de forfait mensuel** (Hetzner, mensuel OVHcloud) pour quelques heures de calcul.

---

## 4. Avant de louer : sur le portable, sans frais

Tant qu'un GPU tourne, chaque heure compte. Il faut donc arriver avec un code qui produit déjà des
résultats exploitables. La liste reprend `dimensionnement.md` §7, complétée par la contre-vérification
technique.

### 4.1 Corrections qui rendent les résultats exploitables

1. **σ(dissipation)/σ_ref dans l'évaluation 3D.**
   - Constat : `budget_summary` (`src/milady/eval/metrics.py`, l. 451–470) ne renvoie que des
     moyennes ; `_ensemble_stats` (l. 570–584) garde l'écart-type des hélicités, pas celui des
     dissipations.
   - À faire : ajouter l'écart-type par échantillon de Dν + Dη (et de chaque terme) et son rapport à
     la référence, avec un test.
   - Pourquoi : sans cette métrique, la scène « Corollaire 6 » et le verdict sur M7 sont
     impossibles, et il faudrait relancer les évaluations.
2. **Convertisseurs vidéo.** Ils sont livrés avec les sources de la vidéo, dans le dossier `video/`
   du dépôt : un convertisseur par scène à régénérer (fichiers MFF → JSON pour M1, M3 et M4 ; JSON
   d'évaluation → JSON pour M5 à M8 ; requête au catalogue pour la facture de calcul). Ils sont dans
   le dépôt, donc visibles dans les conteneurs (`docker-compose.yml`, l. 65–66) et préservés par
   `deploy_remote.sh` (`rsync --delete`).
   - **Convertisseur de M4.** Ne pas utiliser le `growth_rate` du catalogue. Il est ajusté sur
     t ≥ `t_burn` = 100 (`run.py`, l. 734–751 ; `palier2_tg3d.yaml`, l. 41), donc probablement
     sur la saturation pour une dynamo TG. Réajuster λ sur la phase exponentielle de
     `milady_diagnostics/log_b_rms`, enregistré tous les 0,1 depuis t = 0. Pour l'ABC (M3), le
     `growth_rate` du catalogue convient. Le champ `notes` est une chaîne JSON : le décoder avec
     `json.loads`.
3. **Configuration de M8, à créer.** Écrire `infra/configs/train_fm3d_abc.yaml` d'après
   l'esquisse de `dimensionnement.md` §2 (M8) :
   - données : `data.dataset: milady_palier2_abc3d`, `data.campaign: palier2_abc3d`,
     `data.fields: [magnetic_field]` ;
   - conditionnement : `conditioning: [{name: Rm, transform: log}]` ;
   - un `name:` distinct, par exemple `fm3d_abc3d`, pour que `make eval` retrouve le modèle ;
   - en validation et en test, quelques Rm de part et d'autre des seuils 8,87, 17,6 et 26,8 ;
   - choisir `kmax` ;
   - laisser de côté la perte de stationnarité « magnetic » : λ n'y est pas lisible comme
     paramètre (`fm3d.py`, l. 655–656).

   **Essai réduit**, sous un **autre nom de campagne**, sur 2 valeurs de Rm. Une grille 16³ est
   impossible avec `kmax = 8` : `to_grid` exige 2·kmax < N (`src/milady/train/data.py`, l. 389–391).
   Ajouter `--set train.iters=10 data.kmax=3 data.campaign=<essai> data.dataset=<essai> name=<essai>`,
   ou prendre une grille 24³.
4. **Résolution de M4.** Préparer une campagne séparée (par exemple `palier2_tg3d_hr.yaml`) :
   Re = 100 en 128³, et éventuellement Re = 200 en 256³.
   - L'estimation de Kolmogorov donne k_max·η_K = 0,33–0,47 à Re = 100 et 0,20–0,28 à Re = 200 en
     64³ (`dimensionnement.md` §3.3).
   - Le jeu de données automatique ne lit **qu'une** campagne (`data.py`, l. 799–817). Avec deux
     campagnes, passer par `data.files` (à vérifier).
5. **ABC.** Retirer `velocity` de `output.fields` dans `palier2_abc3d.yaml` : u est constant. Le
   volume passe de 9,3 à 4,7 Go.
6. **Interruptions.** Sur instance interruptible seulement, mettre
   `runtime.checkpoint_to_storage: true` dans les YAML. `milady.sweep` n'a pas d'option `--set` :
   il faut modifier le fichier.
7. **256³ seulement.** Les instantanés s'accumulent en mémoire, et chaque point de contrôle les
   réécrit tous, jusqu'à 16 Go par simulation (`run.py`, l. 484). Avant toute campagne 256³,
   allonger `checkpoint_every_s` ou écrire les instantanés au fil de l'eau.
8. **Petits défauts du dépôt, corrigés le 2026-11-08.**
   - `train_fm3d.yaml`, l. 18 : le modèle compte ≈ 48 M paramètres (47,8 M comptés sur le modèle
     construit), et non ≈ 30 M.
   - La requête SQL des heures par campagne (`infra/README.md` § 6.2, page Calcul) échouait sous
     PostgreSQL (`round(double precision, integer)`) comme sous SQLite (`greatest` absent). Elle
     utilise maintenant `CASE WHEN` et `CAST(… AS NUMERIC)`, valables dans les deux.
   - `dimensionnement.md` §2 (témoin de M7) contient le même oubli que celui corrigé au §5.10.
9. **Vérifier.** `make test RUN=local` doit passer. Faire tourner la chaîne réduite de bout en bout
   en mode portable (`infra/README.md` §4.1) : campagne → `make train` court →
   `make eval CONFIG=… MODEL=<uuid> EVAL_ARGS="--out data/exports/essai.json"` → convertisseurs.

### 4.2 Décisions à prendre avec les encadrants (à leur écrire avant de louer)

- **Résolution de M4.** Faut-il 128³ à Re = 100 et 256³ à Re = 200, ou retirer Re = 200 ? Le
  pilote du §5.5 donnera des spectres pour en décider.
- **`n_traj: 4` dans `palier2_tg3d`.** Avec `n_traj: 1`, il n'y a que 400 échantillons
  d'entraînement et 40 instantanés de référence par point, au lieu des 128 demandés.
  - Sur GPU, `n_traj: 4` est presque gratuit en temps (estimation `dimensionnement.md` §1.2).
  - Il multiplie par 4 les données (≈ 12 Go).
- **Jean Zay.** Ont-ils déjà un projet GENCI où vous ajouter ? Sinon, qui dépose un accès dynamique,
  et quand (§8.4) ?
- Peut-on publier ces résultats sur le site et dans la vidéo (§0) ?

### 4.3 Comptes, clés et `.env`

- **Clé SSH.** `ssh-keygen -t ed25519 -f ~/.ssh/milady_cloud`, puis déclarer la clé publique dans
  la console Scaleway.
- **Compte Scaleway**, de type « Personal Project » [SCW-ACC] :
  - une carte bancaire classique : les cartes prépayées et virtuelles sont refusées [SCW-BILL] ;
  - la vérification d'identité, la veille (pièce d'identité et photo, en 15 min) [SCW-ID].
- **Repli.** Ouvrir le compte OVHcloud à l'avance, sans frais. Ne créer le **projet Public Cloud**
  qu'au moment d'en avoir besoin : les 200 € de crédit démarrent à sa création, pour un mois
  [OVH-QUOTA].
- **Bucket et clé.** Créer le bucket en `fr-par` et une clé API pour le stockage objet. Activer
  l'essai gratuit du stockage objet **le jour de la location**, pas avant [SCW-S3FAQ]. Garder les
  clés hors du dépôt : elles iront dans `infra/docker/.env` **sur la VM** (§5.3). Ce fichier n'est
  jamais versionné, et `deploy_remote.sh` ne copie aucun fichier `.env`.
- **Code.** Deux voies :
  - déployer l'arbre local avec `infra/deploy/deploy_remote.sh`, qui copie aussi les modifications
    non poussées ;
  - pousser les corrections sur une branche, puis la cloner **en nommant la branche** (§5.2) : un
    `git clone` simple prend `main`.

---

## 5. Déroulé pas à pas, le jour de la location

Toutes les commandes se lancent **depuis la racine du dépôt sur la VM**, sauf mention « portable ».
Les durées sont des estimations : aucune n'a été mesurée sur GPU. Le chemin GPU n'a jamais tourné,
d'où la marge de débogage.

| Étape | Durée estimée |
|---|---|
| 5.1–5.3 Création, installation, bucket, test de fumée | 30–60 min |
| 5.4 Banc GPU (M15) | ≈ 5–15 min |
| 5.5 Pilote de résolution | 10–30 min |
| 5.6 M1, M4, M3 | 1–3,5 h |
| 5.7 Contrôle et sauvegarde | 15 min |
| 5.8–5.11 M5, M6, M7 + témoin, M8 | 1–2 h |
| §6 Collecte, convertisseurs, suppression | 0,5–1 h |
| Marge de débogage du chemin GPU | 2–4 h |
| **Total facturé** | **≈ 6–12,5 h** |

### 5.1 Créer la VM

Dans la console Scaleway :

1. Créer une instance `L4-1-24G` en zone `fr-par-2`, avec l'image GPU Ubuntu Noble [SCW-IMG].
2. Lui donner un volume Low Latency 5K de 150 Go, votre clé SSH, et un groupe de sécurité n'ouvrant
   que le port 22.
3. Noter l'IP et l'utilisateur SSH. C'est probablement `root` : les exemples de la doc montrent
   `root@scw-…`, mais pour l'ancienne image OS 12 (**non vérifié** pour OS 13). `bootstrap_vm.sh`
   gère le cas `root`.
4. Une fois connecté, lancer `docker compose version && nvidia-smi`.
   - Si `docker compose version` échoue, le script retirera les paquets Docker de l'image et
     installera Docker CE (`bootstrap_vm.sh`, l. 74–101). Ce chemin n'a jamais été exécuté.
   - La version du pilote doit être ≥ 525.

### 5.2 Installer : `bootstrap_vm.sh`

Depuis le **portable**, pour copier l'arbre local avec les corrections du §4, puis lancer
l'installation (jamais testé sur une vraie VM) :

```bash
infra/deploy/deploy_remote.sh UTILISATEUR@IP -i ~/.ssh/milady_cloud
```

Ou, sur la VM, à partir de la branche poussée :

```bash
git clone --branch <branche> https://github.com/knoel99/milady-2027.git && cd milady-2027
sudo infra/deploy/bootstrap_vm.sh
```

(Équivalent depuis le portable : `deploy_remote.sh UTILISATEUR@IP -i ~/.ssh/milady_cloud --git https://github.com/knoel99/milady-2027.git --branch <branche>`.)

Le script installe le NVIDIA Container Toolkit si besoin et génère `.env`. Il construit ensuite
l'image **`milady:gpu`** (`make image-gpu`), démarre `db`, `s3` et `mlflow`, puis lance
`make smoke` dans le conteneur `worker-gpu`. Seul le mode `--cpu` a été testé, hors cloud.
L'étape GPU (étape 3) n'a jamais tourné (`infra/README.md` §12).

À vérifier dans la sortie :

- l'étape « 3/7 GPU NVIDIA » affiche la L4 et la version du pilote ;
- la ligne « Vérification de l'accès GPU depuis un conteneur » liste la L4 ;
- le test de fumée réussit. Il fait tourner le **solveur sur CPU**, et seul l'entraînement d'une
  itération y utilise CUDA (`smoke.py`, l. 200 et 238). Le premier vrai test du solveur sur GPU est
  le banc du §5.4.

En cas d'échec :

- `infra/README.md` §9 (dépannage) : `sudo nvidia-ctk runtime configure --runtime=docker`, puis
  `docker run --rm --gpus all milady:gpu nvidia-smi` ;
- `make image-gpu` pour reconstruire l'image ;
- si le chemin GPU reste bloqué, `sudo infra/deploy/bootstrap_vm.sh --cpu` sauve une partie de la
  session. Mais avec 8 vCPU, le scénario A complet sur CPU prendrait ≈ 6 à 24 h : mieux vaut alors
  basculer sur l'OVHcloud `l4-90` (22 vCPU).

Se **reconnecter en SSH** ensuite, pour que l'appartenance au groupe `docker` prenne effet.

### 5.3 Brancher le bucket du fournisseur, puis refaire le test de fumée

Ajouter à la fin de `infra/docker/.env`, sur la VM (`infra/README.md` §2.5) :

```bash
MILADY_STORAGE_URI=s3://NOM-DU-BUCKET/data
MILADY_MODELS_URI=s3://NOM-DU-BUCKET/models
MILADY_S3_ENDPOINT=https://s3.fr-par.scw.cloud
MILADY_S3_ACCESS_KEY=<clé Scaleway>
MILADY_S3_SECRET_KEY=<secret Scaleway>
AWS_DEFAULT_REGION=fr-par
```

- **Région.** Le `.env` généré garde `AWS_DEFAULT_REGION=us-east-1`, utilisé pour signer les
  requêtes S3 (`src/milady/storage.py`, l. 139–140). La doc Scaleway demande la région du bucket
  (`fr-par`) avec ce point d'accès [SCW-CLI]. D'où la dernière ligne.
- **Effet de bord.** Cette variable est aussi passée au conteneur MLflow, qui parle à MinIO
  (`docker-compose.yml`, l. 175). Que MinIO accepte `fr-par` est **non vérifié**. Le `make smoke`
  le montrera, car il journalise dans MLflow. En cas d'erreur côté MLflow, revenir à `us-east-1`
  et tester le bucket seul.
- Ne pas toucher à `S3_ACCESS_KEY` ni à `S3_SECRET_KEY` : c'est le compte MinIO de MLflow.

```bash
make down && make up
make smoke          # premier essai réel d'un bucket de fournisseur (jamais testé)
```

### 5.4 D'abord le banc GPU (M15) : il recalibre tout le budget

```bash
make shell          # shell dans le conteneur worker-gpu ; le dépôt y est monté sur /opt/milady
mkdir -p data/exports
python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --dtype float32 --steps 50 | tee data/exports/bench_dynamic.jsonl
python -m milady.sim.mhd3d bench --n 64 128 --device cuda --mode kinematic --n-traj 4 | tee data/exports/bench_kinematic.jsonl
exit
nvidia-smi          # VRAM et pilote
```

Chaque ligne JSON donne `seconds_per_step`, `max_memory_gb` et le nom du GPU. Durée d'une
simulation ≈ `seconds_per_step` × nombre de pas :

| Campagne | Nombre de pas par simulation (`dimensionnement.md` §1.3) |
|---|---|
| ABC 64³ | 22 500 |
| TG 64³ | 28 000–52 000 |
| TG 128³ | 31 000–102 000 |
| TG 256³ | 63 000–207 000 |

**Règle de décision.** Si `seconds_per_step` à 256³ dépasse ≈ 0,3 s sur la L4, 3 simulations 256³
demanderaient au moins ≈ 16 h de GPU (63 000 pas × 0,3 s × 3). Ne pas les faire sur cette machine
(§8.2).

### 5.5 Pilote de résolution : la simulation TG la plus exigeante (Re = 200, Pm = 2)

Les points suivent le produit Re × Pm, le dernier paramètre variant le plus vite : Re = 200,
Pm = 2 est donc l'indice 11. Le vérifier avec `--dry-run`, qui ne lance rien.

```bash
make sweep CONFIG=infra/configs/palier2_tg3d.yaml SWEEP_ARGS="--dry-run"
make sweep CONFIG=infra/configs/palier2_tg3d.yaml SWEEP_ARGS="--indices 11"
```

Contrôle du spectre, dans `make shell`. Ce script n'utilise que des fonctions existantes ;
l'essayer d'abord sur le portable avec une simulation réduite.

```python
import numpy as np
from milady.catalog.api import Catalog
from milady.data.format import read_mff
from milady.eval.metrics import energy_spectrum
sim = Catalog().query_simulations("palier2_tg3d", "done", Re=200, Pm=2.0)[0]
uri = [f["uri"] for f in sim["files"] if f["kind"] == "fields"][0]
d = read_mff(uri, fields=["velocity", "magnetic_field"], t=slice(30, None))
for name, f in d["fields"].items():
    E = energy_spectrum(f).mean(axis=(0, 1))         # moyenne sur les 10 derniers instantanés
    print(name, "wall_time_s =", sim["wall_time_s"], "log10 E(k)/max, k = 1..21 :",
          np.round(np.log10(E[1:22] / E.max() + 1e-300), 1))
```

**Décision.** Le YAML demande des spectres qui « décroissent de plusieurs décades avant k_max »
(`palier2_tg3d.yaml`, l. 12–14), sans seuil chiffré : 3 à 4 décades est une règle d'usage, à
valider avec les encadrants.

- Si le critère est tenu : rester en 64³ (scénario A).
- Sinon :
  - montrer Re ≥ 100 à 64³ seulement comme « sous-résolu, provisoire » ;
  - lancer B1 (Re = 100 en 128³) ;
  - décider de Re = 200 en 256³ (§8.2).

### 5.6 Campagnes, dans l'ordre M1 → M4 → M3, sous `tmux`

```bash
tmux new -s milady                       # Ctrl-b d pour se détacher, tmux attach -t milady pour revenir
make sweep CONFIG=infra/configs/palier1_mhd2d.yaml SWEEP_ARGS="--max-parallel 3"   # M1, CPU (NumPy), quelques minutes
make sweep CONFIG=infra/configs/palier2_tg3d.yaml  SWEEP_ARGS="--max-parallel 6"   # M4 : saute l'indice 11 déjà terminé
make sweep CONFIG=infra/configs/palier2_abc3d.yaml SWEEP_ARGS="--max-parallel 6"   # M3 : 37 simulations, 2 trajectoires chacune
```

- `--max-parallel` doit rester ≤ vCPU − 2 : chaque processus GPU occupe un vCPU. Le nombre de fils
  par simulation vaut min(`resources.cpus`, vCPU // max-parallel) (`src/milady/sweep.py`, l. 548–549).
  Sur la `l4-90` d'OVHcloud (22 vCPU), on peut monter à 16.
- Plusieurs simulations sur un même GPU n'ont **jamais été testées**. Pendant M4, `nvidia-smi` doit
  montrer 6 processus.
- `--max-parallel` est fixé au lancement et **ne se change pas en cours de campagne**. Par défaut,
  garder l'ordre strict : M3 terminée, puis M5. Pour gagner ≈ 1 h : une fois les 12 TG `done`,
  lancer l'ABC avec `--max-parallel 4` dans une deuxième fenêtre `tmux`, et M5 (§5.8) dans une
  troisième.

### 5.7 Vérifier que tout est terminé, puis faire une sauvegarde intermédiaire

```bash
make shell
python -m milady.catalog campaigns       # nombre de simulations par statut, pour chaque campagne
exit
```

- **Attendu** : 11, 12 et 37 simulations `done`, et aucune `running` ni `failed`.
- **Sinon**, relancer la campagne : les simulations terminées sont sautées, et
  `SWEEP_ARGS="--retry-running --max-parallel 6"` relance celles restées `running`.
- **Journaux** : `data/sweeps/<campagne>/<horodatage>/logs/sim-00011.log` (indice sur 5 chiffres).

```bash
export BACKUP_S3_ENDPOINT=https://s3.fr-par.scw.cloud BACKUP_ACCESS_KEY=<clé> BACKUP_SECRET_KEY=<secret>
make backup BACKUP_TARGET=s3://NOM-DU-BUCKET/sauvegardes      # jamais testé vers s3://
```

Cette commande copie les dumps `pg_dump` du catalogue et de MLflow, plus le miroir des buckets
**MinIO** (`infra/deploy/backup.sh`, l. 2–3, 101). Après la première sauvegarde, vérifier dans la
console que `sauvegardes/db/milady-*.dump` existe.

### 5.8 M5 : entraînement, seulement après les 12 simulations TG

Le jeu `milady_palier2_tg3d` est créé **une fois pour toutes** au premier `make train`, à partir
des simulations `done` à ce moment-là (`dimensionnement.md` §7, point 7).

```bash
make train CONFIG=infra/configs/train_fm3d.yaml TRAIN_ARGS="--run-name m5_base"
```

- Points de contrôle : `s3://NOM-DU-BUCKET/models/fm3d_tg3d/m5_base/` (`last.pt`, `final.pt`).
- Une évaluation rapide est faite en fin d'entraînement (`eval.after_train: true`).
- L'UUID du modèle s'affiche à la fin ; sinon, `python -m milady.catalog summary`.
- Coût estimé : 5 à 20 min.

### 5.9 M6 : évaluation complète, avec un rapport JSON

```bash
make eval CONFIG=infra/configs/train_fm3d.yaml MODEL=<uuid m5_base> EVAL_ARGS="--out data/exports/eval_m5_base.json"
```

`--out` accepte aussi une URI `s3://…` (`infra/README.md` §11).

### 5.10 M7 : réglage fin par la perte de stationnarité, avec son run témoin

Les deux runs partent du même modèle, font le même nombre d'itérations et ont le **même ancrage**
aux poids de départ. Seule la perte de stationnarité change.

Attention : `stationarity.anchor` s'applique **même quand `stationarity.enabled=false`**
(`src/milady/train/fm3d.py`, l. 1164 et 1351–1353). Le témoin doit donc recevoir aussi
`stationarity.anchor=1.0`. Sans cela, deux choses changeraient entre les runs. La commande du run
principal vient de `train_fm3d.yaml`, l. 13–15.

```bash
make train CONFIG=infra/configs/train_fm3d.yaml TRAIN_ARGS="--run-name m7_stationnarite --init-from s3://NOM-DU-BUCKET/models/fm3d_tg3d/m5_base/final.pt --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0"
make train CONFIG=infra/configs/train_fm3d.yaml TRAIN_ARGS="--run-name m7_temoin --init-from s3://NOM-DU-BUCKET/models/fm3d_tg3d/m5_base/final.pt --set stationarity.enabled=false stationarity.anchor=1.0 train.iters=2000 train.lr=1e-4 train.warmup=0"
make eval CONFIG=infra/configs/train_fm3d.yaml MODEL=<uuid m7_stationnarite> EVAL_ARGS="--out data/exports/eval_m7_stationnarite.json"
make eval CONFIG=infra/configs/train_fm3d.yaml MODEL=<uuid m7_temoin> EVAL_ARGS="--out data/exports/eval_m7_temoin.json"
```

- `--set` prend toutes les valeurs qui le suivent : il doit rester en dernier dans `TRAIN_ARGS`.
- L'expérience E1 a montré que cette perte peut diverger depuis un modèle biaisé. Ne la lancer que
  si M6 montre un modèle de base correct, et surveiller la perte dans MLflow.

### 5.11 M8 : générateur des modes ABC conditionné par Rm (après M3)

Le fichier `infra/configs/train_fm3d_abc.yaml` est **à créer avant la location** (§4.1, point 3).

```bash
make train CONFIG=infra/configs/train_fm3d_abc.yaml TRAIN_ARGS="--run-name m8_abc"
make eval  CONFIG=infra/configs/train_fm3d_abc.yaml MODEL=<uuid m8_abc> EVAL_ARGS="--out data/exports/eval_m8_abc.json"
```

### 5.12 Surveiller

**Interfaces web.** Depuis le portable, ouvrir un tunnel :

```bash
ssh -N -L 5000:localhost:5000 -L 9001:localhost:9001 -i ~/.ssh/milady_cloud UTILISATEUR@IP
```

Puis <http://localhost:5000> pour MLflow (courbes de perte, hyperparamètres). La console MinIO
(<http://localhost:9001>) ne montre plus que les artefacts MLflow une fois le bucket Scaleway
branché.

**Sur la VM :**

- `watch -n 10 nvidia-smi` : utilisation du GPU et VRAM ;
- `htop` (installé par le bootstrap) : vCPU et RAM ;
- `make ps` : état des services.

**Catalogue**, dans `make shell` (`infra/README.md` §2.4) :

```bash
python -m milady.catalog campaigns
python -m milady.catalog sims --campaign palier2_tg3d --status done
python -m milady.catalog summary
```

**Heures consommées par campagne.** La requête du README échoue sous PostgreSQL (§4.1, point 8) ;
version corrigée par conversion en `numeric` :

```bash
C="docker compose -f infra/docker/docker-compose.yml --env-file infra/docker/.env"
$C exec -T db psql -U milady -d milady --csv -c "SELECT c.name, round((sum(s.wall_time_s * greatest(s.n_gpus, 1)) / 3600.0)::numeric, 2) AS heures, count(*) AS n FROM simulation s JOIN campaign c ON c.id = s.campaign_id WHERE s.status = 'done' GROUP BY c.name;" > data/exports/heures_par_campagne.csv
```

Quand plusieurs simulations partagent le GPU, ce sont des heures de processus, pas des heures
facturées. Les heures facturées correspondent au temps de vie de la VM.

### 5.13 Interruptions et reprises (seulement en spot ou préemptible, hors Scaleway)

**Une simulation interrompue** est marquée `failed` si elle a reçu SIGTERM ; sinon elle reste
`running`. Relancer la campagne avec `SWEEP_ARGS="--retry-running …"`. Avec
`runtime.checkpoint_to_storage: true`, elle reprend au dernier point de contrôle, écrit dans le
bucket toutes les 15 min (`checkpoint_every_s: 900`) (`infra/README.md` §6.3).

**Un entraînement** se relance avec la **même** commande et le même `--run-name` : il reprend depuis
le `last.pt` du bucket. Un point de contrôle est écrit toutes les 1 000 itérations.

**Si la VM est perdue,** le catalogue PostgreSQL, qui est sur son disque, disparaît avec elle.

- Planifier `make backup BACKUP_TARGET=s3://…` toutes les heures. Le `cron` de l'en-tête de
  `backup.sh` doit alors recevoir `BACKUP_S3_ENDPOINT`, `BACKUP_ACCESS_KEY` et `BACKUP_SECRET_KEY`.
- Sur une nouvelle VM, restaurer comme au §5.14.
- À défaut, reconstruire la partie « simulations » à partir des fichiers :
  `python -m milady.catalog ingest s3://NOM-DU-BUCKET/data/palier2_tg3d/<uuid>/fields.h5 --campaign palier2_tg3d`.
  Les modèles et évaluations, eux, ne se reconstruisent pas.

### 5.14 Passer de la L4 à la L40S (scénario B2 seulement)

Le catalogue et la base MLflow vivent dans des volumes Docker, sur le disque de la VM L4
(`docker-compose.yml`, l. 89–90 et 268–270). Une nouvelle instance L40S démarre avec un catalogue
vide. Changer le type de l'instance à l'arrêt, ou réattacher le volume, est **non vérifié** chez
Scaleway. Procédure sûre (jamais testée) :

1. Sur la L4 : `make backup BACKUP_TARGET=s3://NOM-DU-BUCKET/sauvegardes`, puis copier
   `infra/docker/.env` sur le portable (il contient déjà les lignes du §5.3).
2. Créer la L40S en `fr-par-2`. Y copier le code **sans lancer l'installation** :
   `infra/deploy/deploy_remote.sh UTILISATEUR@IP_L40S -i ~/.ssh/milady_cloud --sync-only`
   (ou `git clone --branch`).
3. Déposer l'ancien `.env` dans `milady-2027/infra/docker/.env` (par `scp`), **puis** lancer
   `sudo infra/deploy/bootstrap_vm.sh`. Un `.env` existant n'est jamais écrasé (`gen_env.sh`, l. 9).
4. Récupérer les dumps, dans `make shell` :

   ```bash
   python -c "from milady import storage; [storage.get(u, 'data/restore/' + u.rsplit('/', 1)[1]) for u in storage.ls('s3://NOM-DU-BUCKET/sauvegardes/db')]"
   ```

5. Sur l'hôte, restaurer les deux bases (`infra/README.md` §7), avec les dumps les plus récents :

   ```bash
   C="docker compose -f infra/docker/docker-compose.yml --env-file infra/docker/.env"
   $C exec -T db pg_restore -U milady -d milady --clean --if-exists < data/restore/milady-AAAAMMJJTHHMMSSZ.dump
   $C exec -T db pg_restore -U milady -d mlflow --clean --if-exists < data/restore/mlflow-AAAAMMJJTHHMMSSZ.dump
   ```

6. Contrôler avec `python -m milady.catalog campaigns`, puis supprimer la L4.

Les courbes de perte suivent, car elles sont dans la base `mlflow`. Les artefacts MLflow rangés dans
MinIO, eux, ne suivent pas. À défaut de dumps, réingérer les fichiers MFF avec
`python -m milady.catalog ingest` : les modèles et évaluations ne suivent pas cette voie.

---

## 6. Collecter les résultats, puis détruire la VM

### 6.1 Sauvegardes : ce qui est réellement copié

```bash
make backup BACKUP_TARGET=s3://NOM-DU-BUCKET/sauvegardes    # avec les BACKUP_* exportés (§5.7)
make backup                                                 # copie locale dans ./backups
```

Puis, depuis le **portable** :

```bash
rsync -avz -e "ssh -i ~/.ssh/milady_cloud" UTILISATEUR@IP:milady-2027/backups/ ./sauvegardes-vm/
```

**Limite.** `make backup` copie les dumps PostgreSQL et les buckets **MinIO** seulement. Une fois
le bucket Scaleway branché (§5.3), les fichiers MFF et les `final.pt` ne sont plus dans MinIO : ils
n'existent **qu'en un exemplaire**, dans le bucket Scaleway (Multi-AZ). Pour une seconde copie des
≈ 14–20 Go, la faire depuis le portable vers un disque externe, par exemple avec l'AWS CLI
configurée en région `fr-par` [SCW-CLI] (non testé) :

```bash
aws s3 sync s3://NOM-DU-BUCKET/ /chemin/disque-externe/milady-bucket/ --endpoint-url https://s3.fr-par.scw.cloud
```

Coût : probablement nul, si les 75 Go de sortie gratuits par mois se confirment (**douteux**, §6.2) ;
au pire ≈ 0,20 € HT. Sinon, accepter en connaissance de cause une copie unique.

### 6.2 Exports légers, dans `make shell`, puis sur le portable

```bash
for c in palier1_mhd2d palier2_tg3d palier2_abc3d; do python -m milady.catalog sims --campaign $c > data/exports/sims_$c.json; done
python -m milady.catalog campaigns > data/exports/campaigns.json
python -m milady.catalog summary   > data/exports/eval_summary.json
```

Le rapatriement, depuis le portable :

```bash
rsync -avz -e "ssh -i ~/.ssh/milady_cloud" UTILISATEUR@IP:milady-2027/data/exports/ ./exports-cloud/
```

| À rapatrier | Taille | Usage |
|---|---|---|
| `eval_*.json` (M5, M7 stationnarité, M7 témoin, M8) | < 10 Mo | tableaux du site, scènes M5–M8 |
| `sims_*.json`, `campaigns.json`, `eval_summary.json`, `heures_par_campagne.csv` | quelques Mo | paramètres, `wall_time_s`, `growth_rate` de l'ABC (dans `notes`, chaîne JSON), coût réel |
| `bench_*.jsonl` | < 1 Mo | scène M15 et page Calcul |
| dumps `pg_dump` du catalogue et de MLflow (`backups/db/`) | quelques Mo (non mesuré) | trace complète ; courbes de perte (base MLflow) |
| JSON des scènes produits par les convertisseurs | quelques Mo | vidéo |

**Convertisseurs.** Les lancer sur la VM, dans `make shell`, depuis le dépôt (§4.1, point 2).
`milady.data.format.read_mff` lit directement les URI `s3://` : seuls les diagnostics et quelques
instantanés sous-échantillonnés sortent, sans télécharger de champ complet.

**Champs complets.** Inutiles au site et à la vidéo, mais à garder pour la thèse : nouvelle
évaluation, ingestion au catalogue de Jean Zay (`milady.catalog ingest`). Ils pèsent ≈ 14–19 Go
(scénario A), plus ≈ 50 Go pour le scénario B.

**Coût de sortie.**

- Stockage objet Scaleway : l'API donne 0,01 €/Go vers Internet [SCW-API]. La page officielle
  (403 aux robots), vue par un moteur de recherche, et un site tiers annoncent **75 Go gratuits par
  mois**, puis 0,01 €/Go [SCW-S3PRICE] (**douteux**). Les volumes du scénario A seraient alors
  gratuits ; au pire, tout télécharger (≈ 20 Go) coûte ≈ 0,20 € HT.
- Trafic sortant de l'instance (rsync) : non relevé (**non vérifié**), mais les volumes sont
  faibles.

### 6.3 Où garder

**Dans le bucket Scaleway** (≈ 0,40 € HT/mois pour 25 Go en Multi-AZ, ≈ 0,20 € en One Zone ;
gratuit pendant les 90 jours de l'essai [SCW-S3FAQ]) :

- les fichiers MFF ;
- les `final.pt` : ≈ 0,77 Go chacun pour m5_base, m7_stationnarite et m7_temoin ; ≈ 0,6 Go
  (kmax 8) à ≈ 1 Go (kmax 12) pour m8_abc (calcul d'après `fm3d.py`, l. 300–349) ;
- les sauvegardes.

Les `last.pt` intermédiaires peuvent être supprimés.

**Sur le portable**, plus un disque externe : les sauvegardes, les exports et, si voulu, la seconde
copie du bucket (§6.1).

**Dans le dépôt (git)** : seulement les petits JSON dérivés, à côté des résultats existants (§7.1).
Jamais les champs ni les clés.

### 6.4 Arrêter de payer (`infra/README.md` §8)

1. Vérifier que les sauvegardes existent dans le bucket **et** sur le portable.
2. `make down`.
3. Dans la console, **supprimer l'instance**, pas seulement l'éteindre. Chez Scaleway, une instance
   éteinte ne paie plus le calcul, mais paie encore son IP et ses volumes ; en « standby », elle est
   facturée comme en marche [SCW-INST].
4. Vérifier qu'il ne reste ni volume détaché, ni instantané, ni IP réservée.
5. Garder le bucket ; vider ce qui ne sert plus.

---

## 7. Exploiter les résultats

### 7.1 Mettre à jour le site, en français et en anglais

- **`calcul/index.qmd` et `en/calcul/index.qmd`.**
  - Dans « Coûts » et « Solveur », remplacer « aucun temps GPU n'est donné » par les mesures du banc
    (s/pas à 64³, 128³ et 256³, VRAM maximale), les heures réelles par campagne et le coût payé.
  - Corriger la requête SQL (l. 144) comme au §5.12.
  - Dans « Ce qui est testé », déplacer vers « vérifié » ce qui a tourné : image GPU, Container
    Toolkit, solveur et entraînement CUDA, Docker sur une image de fournisseur, bucket S3 du
    fournisseur, `make backup` vers `s3://`, campagnes à taille réelle.
  - Garder dans « reste à vérifier » ce qui n'a pas tourné : multi-GPU, Slurm, Apptainer.
- **`infra/README.md` §6.2, §11 et §12.** Mêmes déplacements, avec les durées mesurées, et même
  correction SQL. Le README ne donne volontairement aucun prix : garder cette règle.
- **`experiences/index.qmd` et `en/experiences/index.qmd`.** Ajouter une section « Campagnes 3D
  (palier 2) », avec :
  - λ(Rm) à 64³ contre E3 à 32³ ;
  - la carte dynamo / pas de dynamo de TG en (Re, Pm) ;
  - le tableau des métriques de M5, M7 et du témoin ;
  - M8 ;
  - un renvoi aux fichiers de résultats.
- **`experiences/digest.py`.** Il ne lit aujourd'hui que E1, E2 et E3. Lui ajouter une section qui
  lit les nouveaux JSON (par exemple dans `experiences/resultats/`), puis régénérer
  `resultats/digest.md`. Les pages ne citent que des chiffres du digest : c'est la règle de
  `digest.py`.
- **Cadre d'honnêteté.**
  - `these/index.qmd`, l. 57, dit que les « résultats du stage » viennent d'expériences sur CPU.
    Le préciser si des résultats GPU y sont cités.
  - Étiqueter Re ≥ 100 à 64³ « sous-résolu, provisoire » si le pilote le montre.
  - Indiquer une seule graine par configuration TG, et 40 instantanés de référence par point.

### 7.2 Régénérer les scènes vidéo en attente

Le dispositif est décrit dans `video/README.md` du dépôt :

- chaque scène « à régénérer » lit un petit JSON (`video/data/<scène>.json`), produit par un
  convertisseur qui inscrit la source et sa somme SHA-256 ;
- quand les données arrivent, on ne régénère que la narration « résultat » (écrite pour l'échec
  comme pour le succès), les sous-titres et le graphique de cette scène.

| Scène (inventaire) | Source sur la VM | Ce que le convertisseur extrait |
|---|---|---|
| M1 « l'usine à données » | `sims_palier1_mhd2d.json` + `milady_diagnostics` des 11 MFF | séries énergie, dissipation, injection ; vignettes par η (remplace le substitut provisoire de E2 dans `palier1_eta_sweep`) |
| M3 / R1 ABC 64³ | `growth_rate` du catalogue + `t1_fields/magnetic_field` de 4 à 6 valeurs de Rm | table (Rm, λ) ; modes sous-échantillonnés de part et d'autre des seuils |
| M4 / R2 Taylor–Green | `milady_diagnostics/log_b_rms` et `magnetic_energy` des 12 MFF, spectres | E_B(t) par (Re, Pm) ; λ réajusté sur la phase exponentielle (pas le `growth_rate` du catalogue) ; carte des dynamos ; spectres moyens |
| M5–M6 / R3 générateur 3D | `eval_m5_base.json` (+ courbes de perte MLflow) | divergences, erreurs de spectre, distance d'énergie contre plancher, au point de test (Re = 50, Pm = 2) |
| M7 stationnarité 3D | `eval_m7_stationnarite.json`, `eval_m7_temoin.json` | résidu de bilan avant/après contre témoin ; σ(dissipation)/σ_ref (après la correction du §4.1) |
| M8 seuil ABC | `eval_m8_abc.json` | erreurs par Rm, en particulier près de 8,87, 17,6 et 26,8 |
| M15 / R7 facture de calcul | `bench_*.jsonl`, `heures_par_campagne.csv` | s/pas, VRAM, heures et coût réel |

### 7.3 Ce que chaque résultat tranche (paris annoncés avant les données)

Les critères sont ceux du plan de thèse (`these/index.qmd`, palier 2, §3.4, l. 917). Les énoncés
sont ceux du rapport (`rapport/index.qmd`), et les « paris » ceux de `pedagogy.md` §1.8. Chaque
verdict doit pouvoir être « atteint », « non atteint » ou « non concluant ».

| Pari | Calcul | Énoncé visé | Critère affiché | Mesure | Réserve |
|---|---|---|---|---|---|
| **Divergence exacte en 3D** | M5–M6 | Proposition 1 : décodage par potentiels vecteurs, ∇·u = ∇·B = 0 par construction | divergence relative < 10⁻¹² (critère (a) du palier 2) | `div_rel_u`, `div_rel_b` | doit tenir quels que soient les autres résultats ; sinon c'est un défaut de code |
| **Qualité des champs** | M5–M6 | conditionnement paramétrique (P1) au point de test sans données (Re = 50, Pm = 2) | erreur de log-spectre < 0,1 décade par bande jusqu'à k_c/2 aux paramètres d'entraînement (critère (b)) ; distance d'énergie comparée à son plancher | `err_spectre_u_log10`, `err_spectre_b_log10`, `dist_energie`, `plancher_dist_energie` | 400 échantillons pour 47,8 M de paramètres, 40 références par point : distances peu précises |
| **Perte de stationnarité en 3D** | M7 + témoin (même ancrage) | Propositions 5 et 7, Corollaire 6 : la contrainte de bilan se pose en loi | résidu de bilan réduit par rapport au **témoin**, sans dégrader la distance d'énergie ; σ(dissipation)/σ_ref dans [0,8 ; 1,2] (critère du palier 1, repris à titre indicatif) | `residu_bilan_total`, `dist_energie`, nouvelle métrique σ | sans la correction du §4.1, la moitié de la question reste sans réponse ; risque de divergence (E1) |
| **Flou au seuil** | M3 + M8 | Proposition 9 : un générateur régulier en λ ne peut pas suivre un saut de loi | erreur du générateur plus grande près de 8,87, 17,6 et 26,8 que loin des seuils ; λ(Rm) à 64³ comparé aux fenêtres publiées (8,9 < Rm < 17,5 ; Rm ≳ 27) | métriques de `eval_m8_abc.json` par Rm ; `growth_rate` de M3 | les 20 instantanés d'une trajectoire ABC sont presque identiques : diversité réelle ≈ 2 graines par Rm |
| Seuil de dynamo TG (R2) | M4 | un seuil apparaît et bouge avec Pm | qualitatif à cette échelle ; repère publié Rm_c = 30 à Pm = 1 (cité dans `these` §3.4) | E_B(t) ; λ réajusté sur `log_b_rms` (phase exponentielle) | Re ≥ 100 probablement sous-résolu à 64³ ; conventions de forçage à comparer avant tout chiffre |
| Facture de calcul (R7) | M15 | budget de thèse ≈ 1,1 × 10⁴ h GPU (facteur 2 d'incertitude) | heures mesurées extrapolées | banc + SQL corrigée | 64³ n'est pas représentatif de 128³ ou 256³ |

---

## 8. Coûts, voie gratuite et risques

### 8.1 Hypothèses

- **Prix Scaleway**, catalogue d'API relu le 2026-11-08 [SCW-API]. Ils sont **HT** : « Prices
  announced on our website exclude all taxes » [SCW-BILL]. La TVA est ajoutée à 20 %.
  - L4 : 0,945 €/h TTC ; L40S : 1,764 €/h TTC.
  - Volume bloc : 0,00013 €/Go·h HT.
  - IPv4 : ≈ 0,005 €/h HT (unité de temps supposée).
  - Stockage objet : ≈ 0,016 €/Go·mois HT (unité supposée, écart < 10 % avec la page officielle).
  - Sortie : 0,01 €/Go HT, avec probablement 75 Go gratuits par mois (**douteux**).
- **Temps de calcul.** Il vient de `dimensionnement.md`, sans aucune mesure GPU, avec une incertitude d'au
  moins ×3. Dans le scénario A, la mise en route domine la facture, pas le calcul.
- **Bande passante mémoire**, qui compte à 128³ et 256³ (constructeur [NV-L4][NV-L40S][NV-A100]) :
  L4 300 Go/s, L40S 864 Go/s, A100 80 Go 1 935 Go/s (PCIe) à 2 039 Go/s (SXM). Elle sert à
  transposer les estimations de `dimensionnement.md`, établies pour 1 à 2 To/s.

### 8.2 Scénarios (EUR TTC)

| Scénario | Hypothèses | Bas | Probable | Haut |
|---|---|---|---|---|
| **A** : 64³, M1 + M3–M8, L4 Scaleway | **Bas** : 6 h facturées, VM supprimée le jour même, bucket dans l'essai gratuit. **Probable** : 14 h (une session de 12 h + une courte reprise), VM éteinte 2 jours (disque + IP), bucket gardé 6 mois dont 3 gratuits, 5 Go sortants. **Haut** : 30 h (2 à 3 sessions de débogage), disque + IP 5 jours, essai non activé et bucket 12 mois, 25 Go sortants payants | **≈ 6 €** | **≈ 16 €** | **≈ 38 €** |
| **B1** : Re = 100 en 128³ (3 simulations), même L4 | 0,4–3,4 h-GPU à 1–2 To/s, ×3 à ×7 sur une L4 (1,2–24 h ; centre ≈ 7,5 h) | ≈ 1 € | ≈ 7 € | ≈ 23 € |
| **B1 + B2** : 128³ et 256³ (Re = 200), L40S Scaleway | 0,4–3,4 + 6–50 h-GPU à 1–2 To/s, ×1,2 à ×2,3 sur une L40S ; disque de 200 Go ; +50 Go de bucket. Bas : 8 h ; probable : 45 h, bucket 6 mois ; haut : 125 h, bucket 12 mois | ≈ 15 € | ≈ 85 € | ≈ 235 € |
| **Repli A** : OVHcloud `l4-90` | mêmes durées à 0,90 €/h TTC ; S3 à 0,007 €/Go·mois, sortie gratuite ; **instance supprimée (après `make backup`) ou mise en « shelve » entre deux sessions** (instantané facturé, prix non relevé) | ≈ 6 € | ≈ 14 € | ≈ 30 € |

- **OVHcloud.** Une `l4-90` laissée **arrêtée** reste facturée ≈ 21,60 € TTC par jour [OVH-BILL].
  Le crédit d'essai de 200 € HT couvrirait tout le repli, si le quota d'un compte en essai permet
  un GPU (**non vérifié**) et si la location tombe dans le mois qui suit la création du projet.
- **Recalcul après le banc (§5.4)**, pour la partie B2 :
  coût ≈ 3 simulations × nombre de pas (63 000 à 207 000) × `seconds_per_step(256³)` / 3 600 × 1,764 €.
  Par exemple, à 0,15 s/pas et 135 000 pas : ≈ 17 h, soit ≈ 30 € TTC.

**Recommandation :**

- payer A, et B1 si le pilote l'exige ;
- **ne pas payer B2 par défaut** : le faire sur Jean Zay (§8.4), ou ne le lancer qu'avec un banc
  256³ mesuré et l'accord des encadrants.

**Ordre de grandeur pour la thèse.** Les paliers 1 et 2 complets (M2 et M12) représentent ≈ 700 et
≈ 3 900 h GPU de classe A100 selon le plan de thèse (`these/index.qmd`, tableau du budget), soit
≈ 4 600 h. Sur une L40S Scaleway à 1,47 €/h HT, cela fait **au moins ≈ 6 800 € HT**, en comptant une
heure de L40S pour une heure d'A100. La L40S a 2,2 à 2,4 fois moins de bande passante qu'une A100 ;
si elle est 1,2 à 2,3 fois plus lente, le total monte jusqu'à ≈ 15 500 € HT. Ce n'est pas un usage
pour un compte personnel.

### 8.3 Pourquoi pas le CPU seul ?

Le profil CPU de Scaleway le plus proche (`POP2-HC-32C-64G` : 32 vCPU, 64 Go) coûte **0,8512 €/h HT**
en `fr-par-1` et `fr-par-2`, plus cher à l'heure que la L4 [SCW-API]. Son quota est de 1 après
vérification d'identité [SCW-QUOTA]. Il suit le chemin `bootstrap_vm.sh --cpu`, image `milady:cpu`,
testé hors cloud seulement. Il termine le scénario A en ≈ 6–10 h (`dimensionnement.md` §8), soit ≈ 6 à
10 € TTC. Mais :

- il ne mesure aucun temps GPU : la scène M15 resterait vide ;
- il ne valide pas le chemin GPU de la thèse ;
- il exclut 256³.

C'est le plan C, si le GPU échoue.

### 8.4 La voie gratuite pour plus tard : accès dynamique GENCI sur Jean Zay

D'après `voies-academiques.md`, aucune voie académique ne vous est ouverte aujourd'hui, faute d'affiliation
[EDARI-DOC]. La bonne voie est un **accès dynamique (AD) GENCI sur Jean Zay**, à faire déposer par
S. Cheng ou D. Lucor.

- **Conditions.** L'AD est gratuit, ouvert toute l'année, et répond « de quelques jours à
  2 semaines environ » (ailleurs sur la même page : « quelques semaines »). L'allocation dure 1 an,
  avec un plafond de 50 000 h GPU normalisées, soit 12 500 h H100 [EDARI-DOC][IDRIS-NU][EDARI].
- **Demande suggérée** (`voies-academiques.md` §2.5) :
  - ≈ 500 à 1 500 h H100, pour l'entraînement, le 128³/256³ et la mise au point ;
  - ≈ 150 h V100 pour les campagnes 64³ : 1 H100 compte comme 4 V100 [EDARI], et ces campagnes
    iraient sans doute aussi vite sur V100 (non mesuré) ;
  - 5 000 à 10 000 h CPU.
- **Calendrier.** Déposer en janvier ou février 2027. La prochaine clôture de l'accès régulier est
  le **08/02/2027 à 9 h** [EDARI].
- **Côté dépôt.** Il est prêt pour Jean Zay (`infra/slurm/`). Il manque :
  - le projet et votre compte : validations du responsable de recherche et du responsable sécurité,
    IP de connexion en France, enquête administrative possible [EDARI-DOC] ;
  - l'image `.sif` : `make image-gpu && make sif` ;
  - un premier essai en QoS `-dev`.
- **Lien avec la location.** La session de location valide l'image GPU que Jean Zay utilisera, et
  ses fichiers MFF s'ingèrent tels quels (`milady.catalog ingest`).
- **Gratuit mais limité.** Les GPU Kaggle (≈ 30 h/semaine selon des sources tierces,
  **non vérifié**) permettent un essai à sec du solveur sur GPU, sans la pile Docker.

**Questions pour les encadrants :**

- ont-ils déjà un projet Jean Zay ? Sinon, qui dépose l'AD, et quand ?
- le CEREA ou l'ENPC ont-ils des GPU ?
- Lab-IA ou Ruche sont-ils accessibles par le LISN ?
- depuis quelle IP vous connecterez-vous ?

### 8.5 Risques et parades

| Risque | Effet | Parade |
|---|---|---|
| Vérification d'identité Scaleway refusée ou manuelle (délai **non vérifié**), carte refusée | pas de GPU le jour J | la faire la veille ; carte bancaire classique ; compte OVHcloud ouvert à l'avance ; Lambda ou VM Vast.ai en dernier recours |
| Crédit d'essai OVHcloud expiré | repli payant dès la première heure | ne créer le projet Public Cloud qu'au moment de s'en servir [OVH-QUOTA] |
| Quota GPU OVHcloud bloqué pendant l'essai | repli inutilisable | acheter un crédit prépayé, présenté par OVHcloud comme le moyen d'une hausse rapide, « instances GPU » comprises [OVH-QUOTA] ; ou rester sur Scaleway |
| Image `milady:gpu` jamais construite en entier ; Container Toolkit, CUDA ou réinstallation de Docker jamais exécutés | session bloquée | `docker compose version` et `nvidia-smi` avant le bootstrap (§5.1) ; 2–4 h de débogage budgétées ; §9 du README ; en dernier recours `bootstrap_vm.sh --cpu`, ou `l4-90` (22 vCPU) |
| Bucket refusé (région de signature) ou jamais testé | fichiers non écrits | `AWS_DEFAULT_REGION=fr-par`, puis `make smoke` avant toute campagne (§5.3) |
| Temps GPU hors des fourchettes (×3 ou plus) | budget dépassé | banc en premier (§5.4) ; règle de décision ; alerte de budget |
| Résolution insuffisante à Re ≥ 100 | résultats faux, présentés comme vrais | pilote (§5.5) ; étiquette « provisoire » ; B1 ; B2 sur Jean Zay |
| `make train` lancé avant la fin de M4 | jeu de données figé incomplet | contrôle du §5.7 avant le §5.8 ; aucun essai réduit sous les vrais noms de campagne |
| Témoin de M7 sans ancrage | verdict sur la perte de stationnarité faussé | `stationarity.anchor=1.0` dans les deux runs (§5.10) |
| Taux TG lu dans le catalogue | taux de saturation pris pour un taux de dynamo | réajustement sur `log_b_rms` dans le convertisseur (§4.1, point 2) |
| Sur-souscription des vCPU | simulations 10 à 100 fois plus lentes | `--max-parallel` ≤ vCPU − 2 |
| Préemption (spot ou préemptible : Verda, Nebius, Vast.ai) | travail et catalogue perdus | `checkpoint_to_storage: true`, `--retry-running`, `--run-name` identique, `make backup` horaire, `milady.catalog ingest` (§5.13) ; pas de 256³ en spot avant le point 7 du §4.1 |
| Solde prépayé à zéro (Verda, Vast.ai, RunPod) | volumes supprimés [VERDA-BILL] | recharge automatique, ou fournisseur facturé à terme échu (Scaleway prélève début du mois suivant [SCW-BILL]) |
| VM oubliée, ou seulement éteinte | facturation continue : IP et volumes chez Scaleway, **instance entière** chez OVHcloud | checklist du §6.4 ; alerte de budget |
| Copie unique des MFF et des modèles dans le bucket | perte en cas d'erreur de manipulation | seconde copie depuis le portable (§6.1) |
| Clés S3 exposées | accès au bucket | clé limitée au stockage objet, `.env` en droits 600, jamais dans git ; ports liés à 127.0.0.1 |
| Convertisseurs vidéo absents de la VM | scènes impossibles à régénérer | convertisseurs versionnés dans `video/` du dépôt (§4.1, point 2) |

---

## 9. Sources

Toutes lues le **2026-11-08** (00 h 30–00 h 50 UTC), sauf mention contraire.

- [SCW-API] https://api.scaleway.com/product-catalog/v2alpha1/public-catalog/products?page_size=500&product_types=instance (aussi `block_storage`, `object_storage` ; IPv4 dans le catalogue complet)
- [SCW-BILL] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/billing/faq.mdx
- [SCW-INST] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/instances/faq.mdx
- [SCW-IMG] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/gpu/how-to/use-preinstalled-env.mdx
- [SCW-QUOTA] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/organizations-and-projects/organization/organization-quotas.mdx
- [SCW-ID] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/account/setup-lifecycle/verify-identity.mdx
- [SCW-ACC] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/account/concepts/understanding-account.mdx
- [SCW-S3FAQ] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/object-storage/faq.mdx
- [SCW-BLK] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/block-storage/faq.mdx
- [SCW-CLI] https://raw.githubusercontent.com/scaleway/docs-content/main/pages/object-storage/api-cli/object-storage-aws-cli.mdx
- [SCW-S3PRICE] https://www.scaleway.com/en/pricing/storage/ (403 ; vu par extrait de moteur de recherche) et https://sliplane.io/blog/scaleway-object-storage-alternatives (tiers)
- [OVH-CAT] https://eu.api.ovh.com/1.0/order/catalog/public/cloud?ovhSubsidiary=FR
- [OVH-GPU] https://www.ovhcloud.com/fr/public-cloud/gpu/
- [OVH-DOC] https://docs.ovhcloud.com/en/guides/public-cloud/compute/deploy-a-gpu-instance.md
- [OVH-BILL] https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/analyze-billing.md et https://docs.ovhcloud.com/en/guides/account-and-service-management/managing-billing-payments-and-services/changing-hourly-monthly-billing.md
- [OVH-QUOTA] https://docs.ovhcloud.com/fr/guides/public-cloud/cross-functional/increasing-public-cloud-quota.md
- [VERDA] https://verda.com/pricing?currency=eur ; [VERDA-BILL] https://docs.verda.com/welcome-to-verda/pricing-and-billing/
- [NEB] https://nebius.com/prices ; [NEB-Q] https://docs.nebius.com/compute/resources/quotas-limits ; [NEB-IMG] https://docs.nebius.com/compute/storage/boot-disk-images (lu le 2026-11-07, non relu)
- [HETZ] https://www.hetzner.com/dedicated-rootserver/gex45/
- [AWS-OD] https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/EU%20(Paris)/Linux/index.json (liste du 2026-11-07)
- [AWS-Q] https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html
- [GCP-GCC] https://gcloud-compute.com/g2-standard-16.html (tiers, mis à jour le 2026-11-01)
- [GCP-FREE] https://docs.cloud.google.com/free/docs/free-cloud-features ; [GCP-QUOTA] https://docs.cloud.google.com/compute/resource-usage
- [AZ-API] https://prices.azure.com/api/retail/prices ; [AZ-Q0] https://learn.microsoft.com/en-us/answers/questions/972197/gpus-not-available-on-subscription-for-pay-as-you (Q&A de 2022)
- [LA-PRICE] https://lambda.com/service/gpu-cloud (lambda.ai y redirige ; finit sur https://lambda.com/instances) ; [LA-DOC] https://docs.lambda.com/public-cloud/on-demand/ (non relu)
- [VA-API] https://console.vast.ai/api/v0/bundles/ (instantané de 00 h 35 UTC) ; [VA-VM] https://docs.vast.ai/instances/virtual-machines (non relu)
- [RP-PRICE] https://www.runpod.io/pricing ; [RP-OV] https://docs.runpod.io/pods/overview
- [NV-L4] https://www.nvidia.com/en-us/data-center/l4/ ; [NV-L40S] https://www.nvidia.com/en-us/data-center/l40s/ ; [NV-A100] https://www.nvidia.com/en-us/data-center/a100/
- [EDARI] https://www.edari.fr/ ; [EDARI-DOC] https://www.edari.fr/documentation/index.php/Documentation_compl%C3%A8te
- [IDRIS-NU] http://www.idris.fr/docs/jean-zay/nouvel-utilisateur
- Dépôt le dépôt (lu, non modifié) : `infra/README.md`, `Makefile`, `infra/deploy/`, `infra/docker/`, `infra/db/schema.sql`, `infra/configs/`, `src/milady/`, `calcul/index.qmd`, `these/index.qmd` ; plan vidéo : `video_plan/inventory.md` §4, `pedagogy.md` §1.8.

---

## 10. Ce qui n'a pas pu être vérifié

**Prix et conditions**

- Scaleway, sortie du stockage objet : les 75 Go gratuits par mois viennent d'un extrait de moteur
  de recherche et d'un site tiers ; la page officielle renvoie 403.
- Scaleway, unité de temps du stockage objet et de l'IPv4 : l'heure est supposée, l'API ne la donne
  pas.
- Scaleway : prix du trafic sortant de l'instance ; alerte de budget ; restriction d'une clé S3 au
  seul bucket ; délai d'une vérification d'identité manuelle.
- OVHcloud :
  - quota GPU par défaut d'un compte en essai ;
  - granularité réelle de facturation (deux pages se contredisent) ;
  - prix d'un instantané en « shelve ».
- Verda : prix HT ou TTC, Docker, quotas.
- Lambda : prix avant le 16/11/2026 (visibles seulement une fois connecté) ; disponibilité dans
  l'UE.
- Google Cloud et Azure : quota GPU par défaut d'un compte neuf. AWS : délai d'obtention du quota.
- Vast.ai : prix d'un marché qui change en continu ; l'instantané du 2026-11-08 ne vaut que pour
  cet instant.
- TVA réellement appliquée par chaque fournisseur hors Scaleway.

**Technique**

- **Tous les temps GPU** de ce document : aucun banc n'a tourné. Le facteur ×1,2 à ×2,3 de la L40S
  par rapport à l'A100 est déduit de la bande passante.
- Image GPU Scaleway OS 13 :
  - utilisateur SSH par défaut (probablement `root`) ;
  - présence du plugin `docker compose`.
- Changement de type L4 → L40S à l'arrêt, ou réattachement du volume.
- Signature S3 : refus de `us-east-1` par Scaleway (la doc demande `fr-par`) ; acceptation de
  `fr-par` par MinIO pour MLflow.
- Chemins jamais exécutés :
  - `deploy_remote.sh` ;
  - la réinstallation de Docker par `bootstrap_vm.sh` ;
  - l'étape GPU du bootstrap ;
  - `make backup` vers `s3://` ;
  - plusieurs simulations sur un GPU ;
  - la procédure du §5.14 ;
  - la seconde copie par l'AWS CLI.
- Défauts de code signalés ici (SQL, ancrage de M7, kmax de l'essai M8, taux TG, sauvegardes) :
  établis par lecture du code. L'erreur SQL, par exemple, est déduite des types, pas observée.
- Compatibilité de l'image avec V100 et T4.

**Calendrier et accès**

- Délai d'ouverture d'un compte Jean Zay.
- Acceptation par l'IDRIS d'une VM de location précise comme point de connexion.
- Quotas Kaggle.
