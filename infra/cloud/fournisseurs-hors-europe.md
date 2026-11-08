# Hyperscalers et places de marché GPU : offres et prix (relevé du 8 novembre 2026)

Périmètre : louer, en tant que **particulier**, de quoi exécuter les calculs manquants de
`milady-2027` (M1, M3 à M8) avec le chemin de déploiement du dépôt (`infra/deploy/bootstrap_vm.sh` :
VM Ubuntu 22.04/24.04, root, systemd, Docker + `docker compose` avec PostgreSQL, MinIO, MLflow). Ce
fichier couvre AWS, Google Cloud, Azure, RunPod, Vast.ai, Lambda, TensorDock, DigitalOcean et
Paperspace. Les fournisseurs européens (Scaleway, OVHcloud, Hetzner, Nebius, Verda) sont dans
`fournisseurs-europe.md`, le dimensionnement dans `dimensionnement.md`.

**Dates.** Toutes les données ont été lues le **2026-11-08 entre 00 h 02 et 00 h 14 UTC** (horodatage
des fichiers bruts `raw/gp_*` et `raw/vast/*`). Chaque prix renvoie à une source `[code]` listée au
§8 avec son URL. **Prix en USD hors taxes**, sauf Azure (aussi en EUR, donné par l'API). Aucune
conversion USD → EUR n'a été faite. Pour un particulier en France, la TVA de 20 % s'ajoute en principe
(règle UE B2C) ; le montant réellement facturé par chaque fournisseur n'a pas été vérifié. Lambda
l'écrit explicitement (« Plus applicable sales tax/VAT/GST », [LA-PRICE]).

## 0. En bref

- Le besoin est petit (`dimensionnement.md` §3 et §8) : **1 GPU de 16 à 24 Go**, Ampere, Ada ou Hopper
  (les GPU Blackwell imposent de reconstruire l'image, `Dockerfile.gpu` l. 1–19), **8 à 16 vCPU,
  32 à 64 Go de RAM, 100 à 200 Go de disque**, une **VM complète** où Docker tourne. Durée :
  **8 à 12 h facturées** (scénario A), plus **≈ 7 à 55 h-GPU** si 128³/256³ s'imposent (scénario B).
- À ce volume, **le prix n'est pas discriminant** : une session de 8 à 12 h coûte entre ≈ 4 $ et
  ≈ 20 $ HT chez tous les candidats sérieux (§3). Ce qui départage, c'est (1) **le quota GPU à 0 des
  nouveaux comptes** chez AWS, Google Cloud et Azure, avec un délai d'obtention non garanti, et (2) le
  fait que **RunPod et les instances ordinaires de Vast.ai sont des conteneurs** sans démon Docker.
- Hyperscaler le moins cher pour ce profil : **Google Cloud g2-standard-8 / g2-standard-16 (L4) à
  europe-west4 : 0,897 / 1,206 $/h** (Spot 0,538 / 0,723 $/h) [GCP-GCC]. AWS g6.2xlarge / g6.4xlarge
  (L4) à Paris : 1,241 / 1,680 $/h [AWS-OD]. Azure NC8as_T4_v3 (T4) à France Central : 0,878 $/h
  (0,7882 €/h) [AZ-API].
- Sans quota ni attente : **Lambda** (VM, Docker, A10 1,29 $/h ou A6000 1,09 $/h à partir du
  16/11/2026, facturé à la minute, sans frais de sortie) [LA-PRICE] ; **Vast.ai en mode VM** (RTX 4090
  dans l'UE dès 0,486 $/h, médiane 0,670 $/h) [VA-API] ; **TensorDock** (VM KVM, Docker inclus, prix
  publics datés de 2024 : non vérifiés) [TD-PRICE].
- **RunPod** est le moins cher (RTX A5000 0,27 $/h, L4 0,59 $/h) mais **interdit `docker compose`**
  sur les pods [RP-OV] : il ne convient qu'au chemin « venv sans services », jamais testé sur GPU.

## 1. Tableau comparatif (instances à 1 GPU adaptées, prix à la demande et Spot)

Légende « VM + compose » : **oui** = VM complète (root, systemd), Docker et `docker compose`
installables ; **non** = conteneur fourni par la plateforme. Quota : situation d'un **compte neuf**.

| Fournisseur | Instance | GPU (Go) | vCPU / RAM | Région UE (prix) | À la demande HT | Spot / interruptible | Facturation | VM + compose | Quota compte neuf | Src |
|---|---|---|---|---|---|---|---|---|---|---|
| **AWS** | g6.2xlarge | L4 (24) | 8 / 32 Gio | Paris eu-west-3 | **1,241 $/h** (Stockholm 1,037 ; Francfort 1,222) | ≈ 0,37 $/h estimé (−70 %), interruptions 10–15 %/mois (Paris) | à la seconde, 60 s min. | oui | **0** vCPU « G and VT » (à la demande et Spot) | [AWS-OD] [AWS-ADV] [AWS-BILL] [AWS-Q] |
| AWS | g6.4xlarge | L4 (24) | 16 / 64 Gio | Paris | **1,680 $/h** (Stockholm 1,403 ; Francfort 1,655) | ≈ 0,39 $/h estimé (−77 %), interruptions > 20 % (Paris) ; Francfort ≈ 0,55 $/h, 5–10 % | idem | oui | 0 | idem |
| AWS | g5.2xlarge | A10G (24) | 8 / 32 Gio | Paris | 1,538 $/h (Stockholm 1,285 ; Irlande 1,353) | Francfort ≈ 0,71 $/h estimé (−53 %), > 20 % | idem | oui | 0 | idem |
| AWS | g4dn.2xlarge | T4 (16) | 8 / 32 Gio | Paris | 0,879 $/h | ≈ 0,25 $/h estimé (−72 %), > 20 % | idem | oui | 0 | idem |
| AWS | g6e.xlarge | L40S (48) | 4 / 32 Gio | Francfort, Stockholm (**pas Paris**) | 2,327 / 1,974 $/h | Stockholm ≈ 0,83 $/h estimé, > 20 % | idem | oui | 0 | idem |
| AWS | p5.4xlarge | H100 (80) | 16 / 256 Gio | Francfort, Stockholm | 8,600 / 7,362 $/h | non relevé | idem | oui | **0** vCPU « P » | [AWS-OD] [AWS-Q] |
| **Google Cloud** | g2-standard-8 | L4 (24) | 8 / 32 Go | europe-west4 (Pays-Bas) | **0,897 $/h** (europe-west1 0,940) | **0,538 $/h** | à la seconde après 1 min | oui | GPU interdits en essai gratuit ; quota GPU global + régional à demander | [GCP-GCC] [GCP-BILL] [GCP-FREE] [GCP-QUOTA] |
| Google Cloud | g2-standard-16 | L4 (24) | 16 / 64 Go | europe-west4 | **1,206 $/h** (europe-west1 1,263) | **0,723 $/h** | idem | oui | idem | idem |
| Google Cloud | a2-highgpu-1g | A100 40 Go | 12 / 85 Go | europe-west4 | 3,748 $/h | 1,831 $/h | idem | oui | idem | [GCP-GCC] [GCP-ACC] |
| **Azure** | NC8as_T4_v3 | T4 (16) | 8 / 56 Gio | France Central | **0,878 $/h = 0,7882 €/h** (Suède 0,796 $ ; Europe Nord 0,838 $) | **0,261 $/h = 0,2347 €/h** | « full minutes » | oui | **0** vCPU série N (réponse Q&A, pas la doc) | [AZ-API] [AZ-T4] [AZ-BILL] [AZ-Q0] |
| Azure | NC16as_T4_v3 | T4 (16) | 16 / 110 Gio | France Central | 1,407 $/h | 0,419 $/h | idem | oui | idem | [AZ-API] [AZ-T4] |
| Azure | NV36ads_A10_v5 | A10 (24) entier | 36 / 440 Gio | France Central | 4,000 $/h = 3,5908 €/h | 0,739 $/h | idem | oui | idem | [AZ-API] |
| Azure | NC24ads_A100_v4 | A100 80 Go | 24 / 220 Gio | France Central | 4,591 $/h = 4,1214 €/h | 0,933 $/h | idem | oui | idem | [AZ-API] |
| **RunPod** (Secure Cloud) | pod L4 / RTX A5000 / RTX 4090 | 24 / 24 / 24 | 12/50 Go ; 9/25 Go ; 6/41 Go | EU-CZ-1, EU-FR-1, EU-NL-1, EU-RO-1, EU-SE-1, EUR-IS-1…5, EUR-NO-1…2 (GPU par centre non vérifié) | **0,59 / 0,27 / 0,89 $/h** (Community Cloud 0,44 ? / 0,16 / 0,34) | aucun prix Spot exposé par l'API (`null`) | à la seconde | **non** (compose interdit) | aucun quota ; crédit prépayé | [RP-API] [RP-PRICE] [RP-BILL] [RP-OV] |
| RunPod | pod A100 PCIe 80 Go | A100 (80) | 8 / 117 Go | idem | 1,79 $/h (Community 1,19) | – | idem | non | idem | idem |
| **Vast.ai** (mode VM) | RTX 4090, `vms_enabled=true` | 4090 (24) | variable (12–32 vCPU, 31–126 Go vus) | 9 offres UE (CH, FI, DK, RO, IT, HU, GB…) | **min. 0,486, médiane 0,670 $/h** | (tous modes) enchère RTX 4090 UE : médiane 0,388 $/h | à la seconde | **oui en mode VM** ; non en mode conteneur | aucun quota ; crédit prépayé | [VA-API] [VA-VM] [VA-BILL] |
| Vast.ai (conteneur) | RTX 4090 / RTX 3090 / RTX A5000 | 24 | variable | 17 / 17 / 3 offres UE | médiane UE 0,598 / 0,336 / 0,230 $/h | RTX 3090 UE : médiane 0,158 $/h | idem | non | idem | [VA-API] |
| **Lambda** | 1x A10 / 1x A6000 / 1x Quadro RTX 6000 | 24 / 48 / 24 | 30/226 Gio ; 14/100 Gio ; 14/46 Gio | europe-central-1 (Allemagne) existe ; types disponibles **non vérifié** | **1,29 / 1,09 / 0,69 $/h** (en vigueur le 16/11/2026 ; avant : visible seulement connecté) | non (aucune offre trouvée) | « by the minute » | **oui** (Lambda Stack : pilote, NVIDIA Container Toolkit ; Docker) | aucun quota annoncé (« self-serve ») | [LA-PRICE] [LA-DOC] |
| **TensorDock** | VM KVM RTX 4090 / RTX 3090 / RTX A6000 | 24 / 24 / 48 | à la carte (0,003 $/vCPU·h, 0,002 $/Go RAM·h) | **non vérifié** (API des emplacements vide sans connexion) | GPU seul ≈ 0,35 / 0,20 / 0,45 $/h « prix typique », **page datée du 24/07/2024 : non vérifié** | non relevé | à la seconde, sans minimum | **oui** (« Docker included on all VM templates ») | aucun quota (« No quotas ») ; dépôt dès 5 $ | [TD-HOME] [TD-PRICE] [TD-DASH] |
| **DigitalOcean** | GPU Droplet RTX 4000 Ada / L40S | 20 / 48 | 8 / 32 Gio ; 8 / 64 Gio | **pas dans l'UE** : TOR1 (Toronto) seulement ; AMS3 n'a que des H100 (4,41 $/h) | 0,76 / 1,57 $/h | Spot seulement B300, MI350X, MI355X | à la seconde, **5 min minimum** ; éteint = facturé | oui (Droplet) | non vérifié | [DO-PRICE] [DO-AVAIL] |
| **Paperspace** (DigitalOcean) | Machine A4000 / A5000 / RTX4000 | 16 / 24 / 8 | 8 / 45 Go ; 8 / 45 Go ; 8 / 30 Go | non vérifié | 0,76 / 1,38 / 0,56 $/h | – | non vérifié | oui (VM) | non vérifié | [PS-PRICE] |

Notes sur le tableau :
- **AWS Spot** : le flux public des prix Spot (`spot.js`, [AWS-SPOTJS]) ne contient aucune g6 dans
  les régions UE (g4dn.xlarge Paris : 0,1767 $/h) ; il est incomplet. Les valeurs « estimé » ci-dessus
  = prix à la demande × (1 − économie moyenne donnée par le Spot Instance Advisor [AWS-ADV]). Le prix
  Spot réel varie. Le quota Spot « All G and VT Spot Instance Requests » vaut aussi **0** [AWS-Q].
- **Google Cloud** : la page officielle n'affiche que us-central1 ; elle donne pour g2-standard-4
  0,706832276 $/h et Spot 0,423016 $/h [GCP-ACC]. Les prix européens viennent d'un agrégateur tiers
  ([GCP-GCC], mis à jour le 1/11/2026) qui reproduit **exactement** ces deux valeurs us-central1 et la
  valeur g2-standard-16 us-central1 (1,1472 $/h). Les machines G2 (L4) ne sont **pas proposées à Paris**
  (europe-west9) : seulement europe-west1, -2, -3, -4, -6.
- **Azure** : NV36ads_A10_v5 est cher (4 $/h) parce qu'il impose 36 vCPU et 440 Gio. Les tailles
  NVadsA10 inférieures découpent la carte (NV18ads = ½ A10, 12 Go). La nouvelle série
  **NC_RTXPRO6000BSE_v6** (NC24lds : ¼ de RTX PRO 6000 Blackwell, 24 Go, 24 vCPU, 72 Gio, 1,414 $/h,
  Spot 0,261 $/h à France Central) [AZ-API] [AZ-NCV6] est une **carte Blackwell fractionnée (vGPU)** :
  exclue sans reconstruction de l'image, et compatibilité CUDA du mode fractionné non vérifiée.
- **RunPod** : pour plusieurs modèles, l'API renvoie un prix « Community » supérieur au prix « Secure »
  (L4 Community 0,44 $ alors que le modèle n'existe pas en Community, `communityCloud: false`) : ces
  valeurs sont des valeurs par défaut, non des offres. Le pod L4 Secure à 0,59 $/h est confirmé par la
  page de prix (« Updated November 4, 2026 ») [RP-PRICE].
- **Vast.ai** : `dph_total` = prix horaire total affiché par l'API pour l'offre (GPU, CPU, RAM ; part du
  disque comprise selon la taille demandée : **non vérifié**). Filtres : hôtes vérifiés, disponibles,
  non loués, 1 GPU. Prix fixés par chaque hôte et fiabilité variable (0,979 à 0,998 sur les 5 VM 4090
  UE les moins chères). Aucune offre VM trouvée pour L4, RTX A5000, RTX A6000 ou A100 SXM4.
- **Blackwell exclu** (`dimensionnement.md` §5) : AWS g7e, Google Cloud G4 (RTX PRO 6000), Azure NCv6,
  RTX 5090 et RTX PRO 6000 chez RunPod et Vast.ai, B200/B300. Ils ne sont pas listés.
- **T4 (Turing)** : 16 Go suffisent (`dimensionnement.md` §8, minimum), mais la carte est hors de la liste
  Ampere/Ada/Hopper du dimensionnement, sans bf16 ; compatibilité de l'image `pytorch 2.14.1-cuda12.6`
  avec sm_75 **non vérifiée**.

## 2. Pour le scénario B (128³ / 256³) : la bande passante mémoire compte

`dimensionnement.md` §1.2 : à 256³, le pas est limité par la bande passante mémoire (≈ 0,12–0,3 s/pas pour
1–2 To/s). Ordres de grandeur constructeur, **cités de mémoire et non revérifiés aujourd'hui** : L4 et
T4 ≈ 0,3 To/s, A10/A10G ≈ 0,6 To/s, RTX A6000 ≈ 0,77 To/s, L40S ≈ 0,86 To/s, RTX 4090 ≈ 1 To/s
(TensorDock écrit « 1,006 GB/s » [TD-PRICE]), A100 80 Go ≈ 2 To/s. Une L4 serait donc plusieurs fois
plus lente qu'une A100 à 256³.

| Option A100 / grosse bande passante | Prix HT relevé | VM + compose | Src |
|---|---|---|---|
| Vast.ai A100 SXM4 (conteneur ; aucune offre VM trouvée) | médiane UE 0,942 $/h (8 offres) | non | [VA-API] |
| RunPod A100 PCIe / SXM 80 Go | 1,79 $/h Secure | non | [RP-API] |
| Lambda 1x A100 40 Go (SXM ou PCIe) | 1,99 $/h (au 16/11) | oui | [LA-PRICE] |
| Google Cloud a2-highgpu-1g, europe-west4 | 3,748 $/h ; Spot 1,831 $/h | oui | [GCP-GCC] |
| Azure NC24ads_A100_v4, France Central | 4,591 $/h ; Spot 0,933 $/h | oui | [AZ-API] |
| AWS : pas d'A100 à 1 GPU (p4d = 8 GPU, 27,43 $/h à Francfort) ; H100 seul : p5.4xlarge | 7,362 $/h (Stockholm) | oui | [AWS-OD] |
| Vast.ai RTX 4090 en mode VM (≈ 1 To/s) | min. 0,486 $/h UE | oui | [VA-API] |

## 3. Coût d'une session (calcul ici, prix HT du §1, hors disque et TVA)

| Configuration | $/h | 8 h | 12 h (scénario A) | 72 h (ordre de grandeur scénario B) |
|---|---|---|---|---|
| GCP g2-standard-8, europe-west4 | 0,897 | 7,2 $ | 10,8 $ | 65 $ |
| GCP g2-standard-16, europe-west4 (Spot 0,723) | 1,206 | 9,6 $ (5,8 en Spot) | 14,5 $ (8,7) | 87 $ (52) |
| AWS g6.2xlarge, Paris | 1,241 | 9,9 $ | 14,9 $ | 89 $ |
| AWS g6.4xlarge, Paris (Stockholm 1,403) | 1,680 | 13,4 $ | 20,2 $ | 121 $ (101) |
| Azure NC8as_T4_v3, France Central | 0,878 | 7,0 $ | 10,5 $ | 63 $ |
| Lambda 1x A10 (30 vCPU, 226 Gio) | 1,29 | 10,3 $ | 15,5 $ | 93 $ |
| Lambda 1x A6000 | 1,09 | 8,7 $ | 13,1 $ | 78 $ |
| Vast.ai VM RTX 4090 UE (min. / médiane) | 0,486 / 0,670 | 3,9 / 5,4 $ | 5,8 / 8,0 $ | 35 / 48 $ |
| DigitalOcean RTX 4000 Ada (Toronto) | 0,76 | 6,1 $ | 9,1 $ | 55 $ |
| RunPod L4 / RTX A5000 (sans compose) | 0,59 / 0,27 | 4,7 / 2,2 $ | 7,1 / 3,2 $ | 42 / 19 $ |

Disque en plus : 150 Go gp3 à Paris = 150 × 0,0928 $ = **13,9 $/mois** [AWS-EBS] (≈ 0,46 $/jour) ;
disque « balanced » Google ≈ 0,000137 $/Gio·h ≈ **0,10 $/Gio·mois** (tarif us-central1 affiché)
[GCP-PD] ; Azure E10 (128 Gio SSD standard) 10,56 $/mois à France Central [AZ-API].

## 4. Stockage objet et trafic sortant

Besoin (`dimensionnement.md` §4) : 20–25 Go de stockage objet, et en sortie quelques centaines de Mo (JSON,
quelques champs) à ≈ 20 Go (tout) ; ≈ 70 Go en scénario B. **Ces volumes passent tous sous les
franchises ou coûtent moins de 3 $.**

| Fournisseur | Stockage objet | Trafic sortant vers Internet | Src |
|---|---|---|---|
| AWS | S3 Standard Paris 0,024 $/Go·mois ; EBS gp3 Paris 0,0928 $/Go·mois | **100 Go/mois gratuits** (tous services, agrégés), puis 0,09 $/Go (Paris, 10 premiers To) | [AWS-S3] [AWS-EBS] [AWS-DT] |
| Google Cloud | Cloud Storage Standard 0,000027397 $/Gio·h ≈ 0,020 $/Gio·mois (us-central1 affiché ; UE non relevé) | Premium : 1 Gio gratuit puis 0,12 $/Gio jusqu'à 1 To (tableau affiché pour la région par défaut) ; Standard : **200 Gio/mois gratuits** puis 0,085 $/Gio ; entrée gratuite | [GCP-GCS] [GCP-NET] |
| Azure | Blob Hot LRS France Central 0,0192 $/Go·mois | **100 Go gratuits** puis 0,087 $/Go (routage Microsoft) ou 0,08 $/Go (routage Internet) | [AZ-API] |
| RunPod | disque conteneur 0,10 $/Go·mois (en marche) ; volume 0,10 (en marche) / **0,20 (arrêté)** ; volume réseau 0,07 $/Go·mois (< 1 To) | **gratuit** (« no fees for data ingress or egress ») | [RP-BILL] |
| Vast.ai | disque facturé **tant que l'instance existe, même arrêtée** ; médiane 0,20–0,27 $/Go·mois (offres 3090/4090) | **par hôte** : médiane 8 $/To en envoi (max 40 $/To) pour les offres RTX 4090 | [VA-BILL] [VA-API] |
| Lambda | système de fichiers persistant facturé au Go·mois (prix non relevé) | **gratuit** (« no egress fees ») | [LA-PRICE] [LA-DOC] |
| TensorDock | NVMe 0,00005 $/Go·h ≈ 0,04 $/Go·mois (page 2024) ; serveur arrêté ≈ 0,005 $/h (exemple du tableau de bord) | « no ingress/egress fees » | [TD-PRICE] [TD-DASH] [TD-HOME] |
| DigitalOcean | disque de démarrage 500 Gio inclus (RTX 4000 Ada) | 10 000 Gio de transfert inclus par Droplet | [DO-PRICE] |
| Paperspace | non relevé | « free unlimited bandwidth » | [PS-DOC] |

Point d'attention, plateformes prépayées : **solde à zéro = arrêt, voire suppression**. RunPod : pods
arrêtés, données perdues sans volume réseau [RP-BILL] ; Vast.ai : instances arrêtées, puis données
supprimées sans moyen de paiement enregistré [VA-BILL] ; TensorDock : « servers are automatically
deleted » [TD-HOME]. Il faut donc rapatrier les résultats (MinIO → bucket externe ou portable) avant
la fin du crédit.

## 5. Quotas GPU des comptes neufs

| Fournisseur | Situation | Démarche | Délai | Src |
|---|---|---|---|---|
| **AWS** | « Running On-Demand G and VT instances » : **0** par défaut ; « All G and VT Spot Instance Requests » : **0** ; « P » : 0. Quota en **vCPU** par région (g6.4xlarge = 16). | Console Service Quotas, code L-DB2E81BA (à la demande) / L-3819A6DF (Spot), dans la région visée | **non documenté** ; témoignages : de quelques jours à plus d'une semaine, examen plus strict pour un compte neuf (anecdotes, non vérifié) | [AWS-Q] [AWS-QDELAY] |
| **Google Cloud** | Essai gratuit (300 $, 90 jours) : **impossible d'ajouter des GPU** et de demander un quota ; il faut activer le compte payant. Quota global « GPUs (all regions) » + quota régional par modèle (L4 : `GPU_FAMILY:NVIDIA_L4`, Spot : `PREEMPTIBLE_NVIDIA_L4_GPUS`). Valeur par défaut **non indiquée** par la doc (0 selon l'usage courant : non vérifié). | Page Quotas de la console, demande examinée, réponse par courriel | non indiqué par la doc | [GCP-FREE] [GCP-QUOTA] [GCP-QREQ] |
| **Azure** | Quota vCPU série N **0** par défaut (réponse acceptée Microsoft Q&A, 2022 ; pas la doc officielle). Essai gratuit non éligible aux GPU (fils communautaires : **non vérifié**). | « My quotas » → New Quota Request ; sinon ticket de support | doc officielle : « usually happens within a few minutes » si accordé automatiquement ; sinon ticket | [AZ-Q] [AZ-Q0] |
| RunPod, Vast.ai, TensorDock | pas de quota ; crédit prépayé (TensorDock dès 5 $) | – | immédiat (selon stock) | [RP-BILL] [VA-BILL] [TD-HOME] |
| Lambda | « self-serve, first-come access » ; stock souvent limité (non vérifié aujourd'hui) | – | immédiat si stock | [LA-PRICE] |
| DigitalOcean | non vérifié (la page des limites ne parle que des Droplets multi-nœuds) | – | – | [DO-LIM] |

## 6. Notes par fournisseur

**AWS.** VM complète. Image conseillée : AMI « Deep Learning Base OSS Nvidia Driver GPU (Ubuntu 24.04) »,
qui contient le pilote NVIDIA (595.91.07 dans la version du 5/10/2026), Docker CE et le NVIDIA
Container Toolkit, et vise G4dn, G5, G6, Gr6, G6e… (notes de version lues via un miroir
docs.amazonaws.cn dans les résultats de recherche : **non vérifié** sur docs.aws.amazon.com)
[AWS-DLAMI]. g6 existe à Paris, Francfort, Stockholm ; g6e seulement à Francfort et Stockholm ; aucune
g6 dans la liste de prix de l'Irlande [AWS-OD]. Variantes : gr6.4xlarge (L4, 16 vCPU, **128 Gio**) à
1,954 $/h à Paris ; g6f = fractions de L4 (1/8 à 1/2, 3 à 12 Go) [AWS-G6], trop justes. Facturation à la
seconde (60 s minimum) [AWS-BILL]. Le seul vrai obstacle est le **quota à 0** et son délai.

**Google Cloud.** VM complète ; L4 dans europe-west1/2/3/4/6, pas à Paris ; europe-west4 est la moins
chère de l'UE [GCP-GCC]. Facturation : minimum 1 minute puis à la seconde [GCP-BILL]. Les 300 $
d'essai ne servent pas aux GPU tant que le compte n'est pas passé en payant [GCP-FREE]. Sortie Premium
0,12 $/Gio au-delà du premier Gio, ou Standard avec 200 Gio gratuits [GCP-NET].

**Azure.** VM complète ; sur NCasT4_v3, l'extension « NVIDIA GPU driver » installe les pilotes CUDA
[AZ-T4]. Facturation **à la minute pleine** ; une VM « Stopped (Deallocated) » n'est plus facturée,
« Stopped Allocated » l'est encore [AZ-BILL]. Spot très bon marché sur T4 et A100 (≈ −70 à −80 %),
mais évictable [AZ-API] [AZ-BILL]. Quota série N à 0 ; la demande est souvent traitée en minutes
d'après la doc, sans garantie pour les GPU [AZ-Q].

**RunPod.** Pods = conteneurs : « Docker Compose is not supported: Runpod runs Docker for you, so you
cannot spin up your own Docker instance or use Docker Compose on Pods » [RP-OV]. Le tutoriel
Docker-in-Docker de RunPod ne vise que les pods CPU (résultat de recherche, non lu en entier). Les
« savings plans » sont abandonnés ; l'API n'expose plus de prix Spot. Facturation à la seconde,
sortie gratuite [RP-BILL]. Utilisable seulement en lançant les scripts Python directement (sans
PostgreSQL/MinIO/MLflow), chemin non testé sur GPU (`dimensionnement.md` §8).

**Vast.ai.** Place de marché d'hôtes indépendants. Mode **VM** : « Init manager support (e.g.
`systemd`), required for running Docker », gabarit Ubuntu 22.04 VM avec CUDA et Docker ; filtre
`vms_enabled=true` ; limites : démarrage plus lent, moins de machines, accès SSH seulement [VA-VM].
Facturation à la seconde ; disque facturé même arrêté ; bande passante facturée à l'octet selon
l'hôte ; modes à la demande, interruptible, réservé (jusqu'à −50 %) [VA-BILL]. 15 offres VM RTX 4090
dans le monde, dont 9 dans l'UE, au moment du relevé [VA-API].

**Lambda.** VM Linux avec GPU ; image par défaut Lambda Stack (pilote, CUDA, NVIDIA Container
Toolkit ; Docker cité pour l'image alternative) [LA-DOC]. Prix à 1 GPU **en vigueur le 16/11/2026**
(A10 1,29 $, A6000 1,09 $, Quadro RTX 6000 0,69 $, A100 40 Go 1,99 $, H100 PCIe 3,79 $, GH200
2,59 $) ; avant cette date, prix visibles seulement une fois connecté [LA-PRICE]. « Pay by the minute »,
« no egress fees » [LA-PRICE]. Une région europe-central-1 (Allemagne) existe ; disponibilité des
petites instances dans cette région **non vérifiée** [LA-DOC]. Les instances 1x A10 / A6000 dépassent
largement le besoin en vCPU et RAM, ce qui ne coûte rien de plus ici.

**TensorDock.** Place de marché de **VM KVM** : « Root access and dedicated GPUs », « Docker included
on all VM templates », « No quotas », « no ingress/egress fees » ; solde à 0 → serveurs supprimés
[TD-HOME]. Tarifs publics : GPU « typical hourly price, varies by host » (RTX 4090 0,35 $, RTX 3090
0,20 $, RTX A6000 0,45 $, A100 SXM4 80 Go 1,80 $), plus CPU, RAM et disque à la carte, mais la page
porte « Last Updated: July 24, 2024 » → **prix actuels non vérifiés** ; les prix réels et les
emplacements ne sont visibles qu'après connexion [TD-PRICE] [TD-DASH].

**DigitalOcean / Paperspace.** GPU Droplets (VM) : RTX 4000 Ada 0,76 $/h (8 vCPU, 32 Gio, 500 Gio),
RTX 6000 Ada et L40S 1,57 $/h ; à la seconde avec **5 minutes minimum** ; une Droplet éteinte reste
facturée [DO-PRICE]. Ces petits GPU ne sont qu'à **Toronto** ; Amsterdam n'a que des H100 [DO-AVAIL].
Paperspace Machines : A4000 0,76 $/h, A5000 1,38 $/h, RTX4000 0,56 $/h [PS-PRICE], « free unlimited
bandwidth » [PS-DOC] ; régions et granularité de facturation **non vérifiées**.

## 7. Ce que cela implique pour le choix (synthèse de ce fichier seulement)

1. **Si l'on veut démarrer cette semaine sans quota** et garder le chemin `bootstrap_vm.sh` tel quel :
   Lambda (A10 ou A6000, ≈ 10–16 $ la session), ou une VM Vast.ai RTX 4090 dans l'UE (≈ 4–8 $ la
   session, hôte à choisir sur sa fiabilité). TensorDock serait équivalent si ses prix actuels se
   confirment une fois connecté.
2. **Si l'on accepte d'attendre un quota** (et qu'on veut une facture d'un grand fournisseur, des
   régions UE et la reprise possible plus tard pour la thèse) : Google Cloud g2-standard-16 à
   europe-west4 (1,21 $/h, Spot 0,72 $/h) est l'hyperscaler le moins cher pour ce profil ; AWS g6.4xlarge
   à Paris (1,68 $/h) ou Stockholm (1,40 $/h) ensuite. Demander le quota **dès l'ouverture du compte**,
   pour 16 vCPU G (AWS) ou 1 GPU L4 + 1 GPU global (Google Cloud).
3. **Azure** n'a, en petits GPU non-Blackwell, que la T4 (0,88 $/h) ou l'A10 en VM surdimensionnée
   (4 $/h) : moins intéressant, sauf en Spot (T4 0,26 $/h, A100 80 Go 0,93 $/h) si l'on écrit des
   points de contrôle fréquents.
4. **Scénario B (256³)** : viser une A100 80 Go ou une RTX 4090 ; la L4 et la T4 y seront lentes.
5. **RunPod** : à garder pour un calcul isolé en Python pur ; pas pour l'infrastructure du dépôt.

## 8. Sources (toutes lues le 2026-11-08, heure UTC)

| Code | URL | Lu à | Remarque |
|---|---|---|---|
| AWS-OD | https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/EU%20(Paris)/Linux/index.json (idem `EU%20(Frankfurt)`, `EU%20(Ireland)`, `EU%20(Stockholm)`, `US%20East%20(N.%20Virginia)`) | 00:04 | données de https://aws.amazon.com/ec2/pricing/on-demand/ ; publication 2026-11-07T00:28:52Z |
| AWS-ADV | https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json | 00:05 | données de https://aws.amazon.com/ec2/spot/instance-advisor/ (économie %, classe d'interruption) |
| AWS-SPOTJS | https://website.spot.ec2.aws.a2z.com/spot.js | 00:05 | flux de https://aws.amazon.com/ec2/spot/pricing/ ; incomplet (pas de g6 UE) |
| AWS-Q | https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html | ≈ 00:06 | tableau des quotas par défaut |
| AWS-BILL | https://aws.amazon.com/ec2/pricing/on-demand/ | ≈ 00:06 | « by the hour or second (minimum of 60 seconds) » ; 100 Go sortants gratuits/mois |
| AWS-G6 | https://aws.amazon.com/ec2/instance-types/g6/ | ≈ 00:06 | tailles g6, gr6, g6f |
| AWS-DT | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/eu-west-3/index.json | ≈ 00:12 | publication 2026-11-03 |
| AWS-S3 | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/eu-west-3/index.json | ≈ 00:12 | publication 2026-11-04 |
| AWS-EBS | https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json | ≈ 00:12 | publication 2026-11-07 |
| AWS-DLAMI | https://docs.amazonaws.cn/en_us/dlami/latest/devguide/aws-deep-learning-ami-gpubaseoss-ul2404-2026-10-05.md | ≈ 00:13 | **vu dans des résultats de recherche seulement** (miroir) : non vérifié |
| AWS-QDELAY | https://repost.aws/questions/QUxBIRsixkTneUqAemd6QVjw/ (et autres fils re:Post) | ≈ 00:12 | vu dans des résultats de recherche ; témoignages, non vérifié |
| GCP-ACC | https://cloud.google.com/products/compute/pricing/accelerator-optimized | 00:07 | tableaux pour us-central1 seulement |
| GCP-GCC | https://gcloud-compute.com/g2-standard-8.html (idem `g2-standard-4`, `-12`, `-16`, `a2-highgpu-1g`, `a3-highgpu-1g`, `g4-standard-48`, `n1-standard-4`) | 00:08–00:13 | **tiers** (N. Knieling), « Last Update: Sun Nov 1 02:50:43 2026 (GMT) », recoupé avec GCP-ACC |
| GCP-BILL | https://cloud.google.com/compute/gpus-pricing (redirige vers /products/compute/pricing) | 00:06 | « minimum of 1 minute… then 1 second increments » |
| GCP-QUOTA | https://docs.cloud.google.com/compute/resource-usage | ≈ 00:08 | quotas GPU global/régional/préemptible ; essai gratuit |
| GCP-FREE | https://docs.cloud.google.com/free/docs/free-cloud-features | ≈ 00:08 | 300 $ sur 90 jours ; GPU bloqués en essai |
| GCP-QREQ | https://docs.cloud.google.com/docs/quotas/help/request_increase | ≈ 00:12 | délai non indiqué |
| GCP-NET | https://cloud.google.com/vpc/network-pricing | ≈ 00:09 | tableau Premium/Standard |
| GCP-GCS | https://cloud.google.com/storage/pricing | ≈ 00:13 | région par défaut us-central1 |
| GCP-PD | https://cloud.google.com/compute/disks-image-pricing | ≈ 00:13 | région par défaut |
| AZ-API | https://prices.azure.com/api/retail/prices (filtres `serviceName`, `armRegionName`, `armSkuName`, `priceType eq 'Consumption'`, `currencyCode` USD/EUR ; aussi Bandwidth et Storage) | 00:02–00:10 | prix de détail Linux |
| AZ-NCV6 | https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nc-rtxpro6000-bse-v6-series | ≈ 00:08 | màj 2026-07-28 |
| AZ-T4 | https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ncast4v3-series | ≈ 00:08 | màj 2026-07-28 |
| AZ-Q | https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests | ≈ 00:07 | màj 2026-01-23 |
| AZ-Q0 | https://learn.microsoft.com/en-us/answers/questions/972197/gpus-not-available-on-subscription-for-pay-as-you | ≈ 00:09 | Q&A du 2022-08-18, réponse d'un MVP |
| AZ-BILL | https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/ | ≈ 00:09 | FAQ facturation |
| RP-API | https://api.runpod.io/graphql (`gpuTypes`, `dataCenters`) | 00:09–00:10 | public, sans clé |
| RP-PRICE | https://www.runpod.io/pricing | 00:09 | « Updated November 4, 2026 » |
| RP-BILL | https://docs.runpod.io/pods/pricing | ≈ 00:10 | |
| RP-OV | https://docs.runpod.io/pods/overview | ≈ 00:12 | |
| VA-API | https://console.vast.ai/api/v0/bundles/ (paramètre `q` JSON) | 00:10–00:11 | état instantané du marché |
| VA-VM | https://docs.vast.ai/instances/virtual-machines | ≈ 00:10 | |
| VA-BILL | https://docs.vast.ai/instances/pricing | ≈ 00:10 | |
| LA-PRICE | https://lambda.ai/service/gpu-cloud | 00:09 | prix « take effect November 16, 2026 » |
| LA-DOC | https://docs.lambda.com/public-cloud/on-demand/ | ≈ 00:11 | régions, Lambda Stack |
| TD-HOME | https://tensordock.com/ | 00:09 | |
| TD-PRICE | https://tensordock.com/cloud-gpus.html | ≈ 00:12 | « Last Updated: July 24, 2024 » |
| TD-DASH | https://dashboard.tensordock.com/deploy | ≈ 00:12 | « Billed per second, no minimum » |
| DO-PRICE | https://www.digitalocean.com/pricing/gpu-droplets | 00:09 | « New pricing is effective as of August 1, 2026 » |
| DO-AVAIL | https://docs.digitalocean.com/products/droplets/details/availability/ | ≈ 00:11 | |
| DO-LIM | https://docs.digitalocean.com/products/droplets/details/limits/ | ≈ 00:12 | |
| PS-PRICE | https://www.paperspace.com/pricing | 00:09 | |
| PS-DOC | https://docs.digitalocean.com/products/paperspace/machines/details/pricing/ | ≈ 00:12 | page presque vide : seule la phrase sur la bande passante |

Fichiers bruts : `raw/gp_*` (JSON et pages converties en texte) et `raw/vast/*.json`, dans
(copies de travail non versionnées).

### Non vérifié (récapitulatif)

Prix TensorDock actuels et emplacements ; disponibilité des petites instances Lambda en Europe et
prix Lambda avant le 16/11 ; régions et granularité Paperspace ; quota des nouveaux comptes
DigitalOcean ; valeur par défaut du quota GPU Google Cloud ; inéligibilité GPU de l'essai Azure ;
délais d'obtention des quotas AWS et Google Cloud ; contenu exact de l'AMI AWS (miroir) ; composition
de `dph_total` chez Vast.ai ; compatibilité CUDA des vGPU fractionnés Azure ; compatibilité T4 de
l'image PyTorch ; bandes passantes mémoire (§2) ; TVA facturée par chaque fournisseur.
