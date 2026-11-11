# Fournisseurs cloud GPU européens : offres et prix (relevé du 7 novembre 2026)

Périmètre : louer, en tant que **particulier payant par carte**, une VM GPU (root + Docker) pour
les calculs manquants du dépôt `milady-2027` : campagnes 3D 64³ (M3 : 37 × 2 graines, M4 : 12),
campagne 2D (M1), entraînement d'environ 48 M de paramètres (M5), évaluation et ajustements (M6-M8).
Ces calculs sont petits : en float32, un état 64³ tient en quelques Mo (`infra/README.md` §6.2,
≈ 100 Mo de pic mesuré sur CPU à 64³). N'importe quel GPU de 16 à 24 Go suffit, et plusieurs
simulations peuvent partager un même GPU. Le critère qui compte est donc **le prix horaire d'un
petit GPU et la simplicité d'accès**, pas la puissance de pointe.

Toutes les données ci-dessous ont été lues le **2026-11-07**, entre 23 h 50 et 23 h 58 UTC (horodatage des
fichiers bruts). Les URL figurent dans chaque section et dans la liste finale. « HT » = hors TVA. « TTC » est calculé ici avec la TVA française de 20 % (taux que
donne le catalogue OVHcloud ; pour les fournisseurs étrangers, l'application de la TVA française
à un particulier est la règle UE B2C, mais le montant facturé n'a pas été vérifié). Aucun
prix n'a été converti de USD en EUR (taux de change non vérifié).

## 1. Tableau comparatif (instances à 1 GPU utiles pour ce travail)

| Fournisseur (siège) | Instance | GPU (mémoire) | vCPU / RAM | Prix HT | TTC (20 %) | Facturation | Région(s) UE | Spot / interruptible |
|---|---|---|---|---|---|---|---|---|
| **Scaleway** (FR) | L4-1-24G | L4 (24 Go) | 8 / 48 Gio | 0,013125 €/min = **0,7875 €/h** | 0,945 €/h | à la minute, mais minimum 60 min par période de marche (cf. notes) | fr-par-1, fr-par-2 (Paris), pl-waw-2 (Varsovie) | non (aucune offre trouvée, non vérifié) |
| Scaleway | L40S-1-48G | L40S (48 Go) | 8 / 96 Gio | 0,024498 €/min = **1,470 €/h** | 1,764 €/h | idem | fr-par-2, pl-waw-2 | non |
| Scaleway | RTX6000B-1-96G | RTX PRO 6000 Blackwell (96 Go) | 28 / 240 Gio | 0,048 €/min = 2,88 €/h | 3,456 €/h | idem | fr-par-2 | non |
| Scaleway | H100-1-80G | H100 PCIe (80 Go) | 24 / 240 Gio | 0,047775 €/min = 2,8665 €/h | 3,440 €/h | idem | fr-par-2, pl-waw-2 | non |
| **OVHcloud** (FR) | l4-90 | L4 (24 Go) | 22 / 90 Go, 400 Go NVMe | **0,75 €/h** (540 €/mois au forfait mensuel) | 0,90 €/h | à la seconde après 1 min minimum (doc. du 2026-11-05 ; une autre page dit « toute heure entamée » : contradiction) | GRA11 (Gravelines) seulement pour L4/L40S/A100/H100 | non (non vérifié) |
| OVHcloud | a10-45 | A10 (24 Go) | 30 / 42 Go | 0,76 €/h | 0,912 €/h | idem | étiqueté « coming_soon » dans le catalogue : disponibilité incertaine | non |
| OVHcloud | l40s-90 | L40S (48 Go) | 15 / 90 Go | **1,40 €/h** (1 008 €/mois) | 1,68 €/h | idem | GRA11 | non |
| OVHcloud | t1-45 / t2-45 | V100 16 Go / V100S 32 Go | 8 / 45 Go (t1), 15 / 45 Go (t2) | 0,70 / 0,80 €/h | 0,84 / 0,96 €/h | idem | GRA7, GRA9, GRA11 (+ BHS5 Canada) | non |
| OVHcloud | rtx5000-28 | Quadro RTX 5000 (16 Go) | – | 0,36 €/h | 0,432 €/h | idem | étiqueté « coming_soon » : disponibilité incertaine | non |
| OVHcloud | a100-180 / h100-380 | A100 80 Go / H100 80 Go | 15 / 180 ; 30 / 380 | 2,75 / 2,80 €/h | 3,30 / 3,36 €/h | idem | GRA11 | non |
| **Hetzner** (DE) | GEX45 (serveur **dédié**) | RTX PRO 4000 Blackwell SFF (24 Go) | i5-13500 14 cœurs / 64 Go | 0,3429 €/h ou 214 €/mois, **+ 209 € de frais d'installation** | 0,411 €/h + 250,80 € | à l'heure, plafonné au mois ; sans engagement | HEL1 (Helsinki) | non |
| Hetzner | GEX63 / GEX131 | RTX PRO 6000 Blackwell Max-Q (96 Go) | 20 / 128 Go ; 24 / … | 1,6009 / 2,4022 €/h, + 999 / 1 499 € d'installation | – | idem | HEL1 (GEX131 aussi FSN1, Falkenstein) | non |
| **Nebius** (NL) | L40S Intel | L40S (48 Go) | 8-40 / 32-160 Go | 1,35 $/h GPU + 0,012 $/vCPU·h + 0,0032 $/Gio·h, soit **à partir de 1,55 $/h** | non calculé (USD) | **à la seconde** | eu-north1 (Finlande) seulement | **oui** : préemptible, tarif fixe ≈ 0,65 $/h GPU, soit **à partir de 0,74 $/h** |
| Nebius | H100 NVLink | H100 (80 Go) | 16 / 200 Go | 4,50 $/h | – | à la seconde | eu-north1 seulement | oui, prix spot dynamique « à partir de 0,79 $/h » |
| Nebius | RTX PRO 6000 | 96 Go | 24 / 218 Go | 1,80 $/h | – | à la seconde | eu-south1 (Madrid), uk-south2 ; us-central1 | oui, à partir de 0,79 $/h |
| **Verda** (ex-DataCrunch, FI) | 1x RTX A6000 | A6000 (48 Go) | 10 / 60 Go | **0,7591 €/h** | 0,911 €/h* | prépayé, par tranches de 10 min (non utilisé remboursé) | FIN-01/02/03 (Helsinki) | **oui** : 0,3795 €/h (évictable sans préavis) |
| Verda | 1x Tesla V100 | V100 (16 Go) | 4 / 18 Go | **0,2156 €/h** | 0,259 €/h* | idem | Helsinki | oui : 0,1078 €/h |
| Verda | 1x RTX 6000 Ada | 6000 Ada (48 Go) | 10 / 60 Go | 1,375 €/h | 1,65 €/h* | idem | Helsinki | oui : 0,6874 €/h |
| Verda | 1x L40S | L40S (48 Go) | 20 / 60 Go | 1,735 €/h | 2,082 €/h* | idem | Helsinki | oui : 0,8673 €/h |
| Verda | 1x A100 SXM4 40 Go / 80 Go | A100 | 22 / 120 Go | 1,476 / 2,063 €/h | – | idem | Helsinki | oui : 0,7382 / 1,032 €/h |
| Verda | 1x H100 SXM5 | H100 (80 Go) | 30 / 120 Go | 4,400 €/h | – | idem | Helsinki | oui : 2,200 €/h |
| **Genesis Cloud** (DE) | – | – | – | **non vérifié** | – | – | – | – |

\* Verda : la page de prix ne précise pas si ses montants sont HT. Le TTC est indiqué sous
l'hypothèse « HT », **non vérifiée**.

### Stockage objet (S3) et trafic sortant

| Fournisseur | Stockage objet standard | Trafic sortant (egress) | Particularités |
|---|---|---|---|
| Scaleway | Standard Multi-AZ 0,000022 €/Go·h ≈ **0,016 €/Go·mois** ; One Zone 0,000011 €/Go·h ≈ 0,008 €/Go·mois (l'unité horaire est déduite : l'API ne la précise pas) | **0,01 €/Go** vers Internet (depuis le stockage objet) ; gratuit vers fr-par | 750 Go gratuits pendant 90 jours pour un nouvel utilisateur (condition : n'avoir jamais utilisé la classe Multi-AZ avant le 30/11/2023). Volume bloc SSD 0,00013 €/Go·h ≈ 0,095 €/Go·mois |
| OVHcloud | Standard 0,00001 €/Go·h ≈ **0,007 €/Go·mois** ; Standard 3-AZ ≈ 0,014 ; High Performance 0,018 €/Go·mois | **0 €** (catalogue : trafic sortant du stockage objet et des instances en Europe à 0) | Disque NVMe local de 400 Go inclus dans l4-90 et l40s-90 |
| Hetzner | Forfait 6,49 €/mois (1 To stocké + 1 To de trafic sortant inclus), puis 0,0087 €/To·h (≈ 6,35 €/To·mois) | 1 €/To au-delà du To inclus ; trafic illimité et gratuit sur les serveurs dédiés (sauf option 10G) | Stockage objet à FSN1, HEL1, NBG1 |
| Nebius | 0,0147 $/Gio·mois | 0,015 $/Gio (stockage objet Standard) ; trafic réseau des VM gratuit, IP publique gratuite | Volumes bloc 0,053 à 0,118 $/Gio·mois |
| Verda | Bêta, prix affiché seulement dans la console (**non vérifié**) ; quota bêta de 1 Tio | Téléversements, téléchargements et requêtes non facturés | NVMe bloc 0,179 €/Gio·mois. **Solde prépayé à zéro → instances arrêtées et volumes supprimés** ; accès S3 suspendu |

## 2. Notes par fournisseur

### Scaleway (Iliad, France) : le plus simple pour ce dépôt
- **Prix** : catalogue public officiel, API `https://api.scaleway.com/product-catalog/v2alpha1/public-catalog/products?product_types=instance`
  (lu le 2026-11-07). La page `https://www.scaleway.com/en/pricing/gpu/` renvoie un défi anti-robot (403) : elle n'a
  pas pu être lue. Le catalogue ne dit pas si ses prix sont HT. Ils sont présentés ici comme HT, selon la pratique
  habituelle de Scaleway (**non vérifié** sur la page de prix). Les prix L4, L40S et H100 dépassent d'environ 5 %
  ceux qu'on trouvait en 2024-2025 : le catalogue de novembre 2026 fait foi.
- **Facturation** : les instances GPU sont facturées à la minute de fonctionnement, démarrage et veille compris
  (sauf RENDER-S, à l'heure)
  (`https://raw.githubusercontent.com/scaleway/docs-content/main/pages/instances/faq.mdx`). La FAQ facturation
  ajoute : « Each of these resources is billed separately for a minimum of 60 minutes », chaque période continue
  de marche comptant comme une ressource
  (`https://raw.githubusercontent.com/scaleway/docs-content/main/pages/billing/faq.mdx`). Mieux vaut donc ne pas
  multiplier les arrêts et redémarrages courts. Une instance éteinte mais non supprimée continue de payer son IP et
  ses volumes.
- **VM** : de vraies instances (VM) avec accès root. Image « Ubuntu Noble GPU OS 13 (NVIDIA) » : pilotes NVIDIA
  libres récents et Docker déjà installés
  (`https://raw.githubusercontent.com/scaleway/docs-content/main/pages/gpu/how-to/use-preinstalled-env.mdx`).
  `infra/deploy/bootstrap_vm.sh` doit donc voir le GPU directement.
- **Quotas et vérification d'identité** : avec seulement un moyen de paiement validé, les GPU sont inaccessibles. Il faut
  « valider son identité » pour obtenir **1 instance L4-1-24G, 1 L40S-1-48G et 1 RENDER-S**. Toutes les tailles
  multi-GPU, les H100 et les B300 passent par une demande au support
  (`https://raw.githubusercontent.com/scaleway/docs-content/main/pages/organizations-and-projects/organization/organization-quotas.mdx`).
  RTX6000B ne figure pas dans ce tableau de quotas : il faut probablement passer par le support (**non vérifié**).
  La vérification se fait en ligne (carte d'identité ou passeport + photo) et doit être bouclée **en 15 minutes**.
  En cas d'échec, la vérification passe par le support, avec selfie et pièce d'identité
  (`…/pages/account/setup-lifecycle/verify-identity.mdx`, `…/pages/account/troubleshooting/cannot-verify-identity.mdx`).
  Le délai d'une vérification manuelle n'a pas été trouvé (**non vérifié**).
- **Particulier** : un type de compte « Personal Project » existe
  (`…/pages/account/concepts/understanding-account.mdx`). Cartes acceptées : Visa, MasterCard, CB, UnionPay, Amex,
  plus SEPA. Les **cartes virtuelles et prépayées sont refusées**, et le 3-D Secure est recommandé. Le
  prélèvement a lieu en début de mois suivant (`…/pages/billing/faq.mdx`).
- **Spot** : aucune offre GPU interruptible trouvée (**non vérifié**).
- **Ce qui compte ici** : le stockage S3 est déjà cité par le dépôt (`docs/specs/infra.md`, `MILADY_STORAGE_URI`). Le
  quota d'un seul L4 au départ suffit, car plusieurs simulations 64³ peuvent tourner en parallèle sur ce GPU.

### OVHcloud (France) : le moins cher en euros parmi les L4, avec 200 € de crédit d'essai
- **Prix** : catalogue public officiel `https://eu.api.ovh.com/1.0/order/catalog/public/cloud?ovhSubsidiary=FR`
  (devise EUR, `taxRate` 20). Prix « HT/heure » confirmés sur `https://www.ovhcloud.com/fr/public-cloud/gpu/`
  (L4 0,75 € ; L40S 1,40 € ; A10 0,76 € ; V100S 0,80 € ; H100 2,80 € ; Quadro RTX 5000 0,36 € ; H200 42 €/h pour 8 GPU).
  Le service géré « AI Training » (conteneurs, pas de VM) est facturé à la minute, un peu plus cher : L4 0,83 €/h,
  L40S 1,55 €/h, A10 0,90 €/h, H100 3,10 €/h (même catalogue).
- **Régions** : « The newer models (A100, H100, L4 and L40s) are only available in the GRA11 region for now »
  (`https://docs.ovhcloud.com/en/guides/public-cloud/compute/deploy-a-gpu-instance.md`, mise à jour 2026-11-05).
- **Facturation** : `analyze-billing` (2026-11-05) dit « Every second of use is billed, beyond an initial 1-minute
  minimum — usage is never rounded up to the next hour », et la facturation ne s'arrête qu'à la **suppression**
  de l'instance (« stopped » ou « paused » restent facturées)
  (`https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/analyze-billing.md`). La page
  `changing-hourly-monthly-billing.md` (même date) parle encore de « every commenced hour » : **contradiction
  non tranchée**.
- **VM** : VM avec GPU en passthrough PCI, accès root. **Pilote NVIDIA non préinstallé** : la carte « cannot be used
  yet » tant qu'on n'a pas installé `cuda-drivers` (guide ci-dessus). `bootstrap_vm.sh` repère ce cas et
  affiche la marche à suivre (`ubuntu-drivers install --gpgpu`, puis redémarrage). Compter environ 10 minutes de plus.
- **Quotas** : quotas par projet et par région. Les augmentations dépendent de « l'ancienneté du compte et l'existence
  de factures acquittées », et les comptes en essai « peuvent avoir des options d'augmentation de quota limitées tant
  que leur première facture n'a pas été réglée ». Pour une hausse rapide (« instances GPU »), on peut acheter
  immédiatement un crédit prépayé
  (`https://docs.ovhcloud.com/fr/guides/public-cloud/cross-functional/increasing-public-cloud-quota.md`). Les
  quotas GPU d'un compte neuf ne sont pas publiés (**non vérifié**).
- **Crédit d'essai** : **200 € de crédit HT** pour un premier projet Public Cloud, valable 1 mois, moyen de
  paiement valide exigé (CGV reproduites sur `https://www.ovhcloud.com/fr/public-cloud/gpu/`). Utilisable pour des
  GPU **si le quota du compte en essai le permet** (**non vérifié**).
- **Particulier** : le coupon vise « une personne physique ou morale ». Les vérifications d'identité éventuelles à la
  commande n'ont pas été trouvées (**non vérifié**).
- **Stockage** : S3 Standard ≈ 0,007 €/Go·mois, trafic sortant gratuit (catalogue). C'est le stockage le moins cher et
  le seul sans frais de sortie parmi ces fournisseurs, avec le trafic inclus de Hetzner.

### Hetzner (Allemagne) : serveurs dédiés seulement, mal adapté à un usage ponctuel
- Pas de GPU dans Hetzner Cloud : uniquement des **serveurs dédiés** GEX (bare metal, root complet, Ubuntu proposé).
  `https://www.hetzner.com/dedicated-rootserver/matrix-gpu/` et `https://www.hetzner.com/dedicated-rootserver/gex45/`
  (lus le 2026-11-07) annoncent : GEX45 0,3429 €/h HT ou 214 €/mois, **frais d'installation 209 € HT**, sans durée
  minimale, résiliation immédiate, trafic illimité et gratuit.
- Pour 100 h de calcul : 34 € + 209 € = **243 € HT**, contre 75 à 79 € chez OVHcloud ou Scaleway. L'offre ne devient
  rentable qu'en location au mois pour un travail long (thèse, M2 et M12).
- Pilotes NVIDIA et Docker : à installer soi-même (**non vérifié**). Délai de mise à disposition du serveur,
  éventuelle vérification d'identité d'un nouveau client et restriction de la gamme GEX aux clients existants (signalée
  en 2024 sur un forum) : **non vérifiés**.
- Stockage objet : 6,49 €/mois avec 1 To et 1 To de trafic sortant inclus
  (`https://www.hetzner.com/storage/object-storage/`).

### Nebius (Pays-Bas, centres de données en Finlande, France, etc.) : bon outillage, facturation en USD
- **Prix** : `https://nebius.com/prices` et `https://docs.nebius.com/compute/resources/pricing` (lus le 2026-11-07).
  « All prices are shown without any applicable taxes, including VAT. » Facturation **à la seconde** (« billing unit:
  1 second »).
- **Régions** : régions publiques eu-north1 (Finlande), eu-west1 et eu-west2 (France), eu-south1 (Madrid), uk-south1 et 2,
  etc. (`https://docs.nebius.com/overview/regions`). Mais **L40S et H100 ne sont proposés qu'en eu-north1**. En France,
  seul le H200 (5,40 $/h) est proposé, ce qui est surdimensionné ici.
- **VM** : de vraies VM. Images « Ubuntu 24.04 LTS for NVIDIA GPUs (CUDA 12 / CUDA 13) », avec pilote, CUDA et
  **NVIDIA Container Toolkit** (`https://docs.nebius.com/compute/storage/boot-disk-images`). Que Docker lui-même soit
  installé reste **non vérifié**.
- **Quotas** : palier « default » à l'inscription : **8 L40S** et **8 H100** en eu-north1. Le palier « full » (32) est
  attribué automatiquement selon l'historique (`https://docs.nebius.com/compute/resources/quotas-limits`).
- **Particulier** : inscription possible « as an individual », paiement par carte via Stripe, **en USD uniquement**
  (frais de change de la banque à prévoir). **25 $ prélevés au départ** et crédités sur le solde
  (`https://docs.nebius.com/signup-billing/sign-up`, `https://nebius.com/prices`). Aucune pièce d'identité n'est
  mentionnée dans le guide d'inscription (**non vérifié**).
- **Spot** : L40S préemptible à tarif fixe d'environ 0,65 $/h pour le GPU (« from 0,74 $ » avec CPU et RAM). H100
  et RTX PRO 6000 « from 0,79 $ » au prix spot dynamique, révisable toutes les 15 minutes.

### Verda (ex-DataCrunch, Finlande) : le moins cher à l'heure, prépayé, avec spot
- `https://datacrunch.io/` sert désormais le même site que `https://verda.com/`. Prix en EUR :
  `https://verda.com/pricing?currency=eur` (lu le 2026-11-07). La mention HT ou TTC n'apparaît pas (**non vérifié**).
- **Facturation** : prépayée, par tranches de 10 minutes, la partie non utilisée étant remboursée à la période suivante.
  Recharge automatique par carte possible. **Si le solde tombe à zéro, les instances sont arrêtées et les volumes
  supprimés** (`https://docs.verda.com/welcome-to-verda/pricing-and-billing/`).
- **Spot** : environ −50 %, « evicted by Verda at any point without warning »
  (`https://docs.verda.com/cpu-and-gpu-instances/set-up-a-gpu-instance/`). Convient aux campagnes de simulations
  indépendantes, relançables (README §6.3), à condition d'écrire chaque résultat dans S3 au fil de l'eau.
- **Localisation** : FIN-01, FIN-02, FIN-03, tous à Helsinki
  (`https://docs.verda.com/welcome-to-verda/locations-and-sustainability/`).
- **VM** : instances avec SSH et images Ubuntu 24 et 26 (accès aux compteurs GPU NVIDIA, d'après les notes de version :
  `https://docs.verda.com/welcome-to-verda/release-notes/`). Pilote préinstallé probable, mais Docker
  **non vérifié**. La disponibilité des modèles varie : les tailles indisponibles sont grisées dans la console.
- **V100 16 Go à 0,2156 €/h** : le moins cher pour les simulations 64³. L'image `milady:gpu` est en CUDA 12.6 (qui
  prend encore en charge Volta, sm_70), mais la présence de sm_70 dans la roue torch 2.14.1 + cu126 est **à vérifier**
  (exécuter `torch.cuda.get_arch_list()`). L'image CUDA 13 du Dockerfile ne conviendrait pas : CUDA 13 abandonne Volta.
- Stockage objet en **bêta**, prix visible seulement dans la console, transferts gratuits, quota de 1 Tio.
- Quotas GPU et vérification d'identité d'un nouveau compte particulier : **non vérifiés**.

### Genesis Cloud (Allemagne) : écarté
- Le 2026-11-07, `https://www.genesiscloud.com/` échoue en TLS (« tlsv1 alert internal error ») et
  `https://genesiscloud.com/` renvoie une erreur Cloudflare 522.
- Un article de Bizety daté du 23/09/2025 rapporte que l'entreprise serait en liquidation (« Genesis Cloud GmbH i.L. »),
  sur la foi d'un message Reddit et de la page d'accueil (`https://bizety.com/?p=12386`). Source secondaire unique :
  **non vérifié**. Les prix relevés par des comparateurs tiers (H100 vendu par nœuds de 8) ne sont pas exploitables.
  **À exclure.**

## 3. Ordre de grandeur pour ce travail

Pour **100 heures-GPU** (hypothèse de travail, hors stockage) : Scaleway L4 78,75 € HT (94,50 € TTC) ;
OVHcloud l4-90 75 € HT (90 € TTC), éventuellement couverts par le crédit de 200 € ; Verda A6000 75,91 €
(spot 37,95 €) ; Verda V100 21,56 € (spot 10,78 €) ; Nebius L40S environ 155 $ HT (préemptible environ 74 $) ;
Hetzner GEX45 243 € HT avec l'installation. Pour mémoire, les paliers complets M2 et M12 (environ 700 et 3 900
heures-GPU selon le projet de thèse) coûteraient de 1 000 à 5 700 € HT sur une L40S Scaleway. Ils relèvent de
GENCI ou Jean Zay, pas d'un compte personnel.

## 4. Les trois meilleures options pour ce travail

1. **Scaleway L4-1-24G** (Paris), 0,7875 €/h HT, facturé à la minute (avec un minimum de 60 minutes par période de
   marche) : image GPU avec pilote et Docker, donc `bootstrap_vm.sh` fonctionne sans intervention ; vérification
   d'identité en ligne en 15 minutes pour débloquer 1 L4 et 1 L40S ; S3 déjà prévu par le dépôt ; 750 Go gratuits
   pendant 90 jours. Pour l'entraînement M5, passer à la L40S-1-48G (1,47 €/h). Limites : un seul GPU de chaque
   type sans passer par le support, et trafic sortant facturé 0,01 €/Go.
2. **OVHcloud l4-90** (Gravelines GRA11), 0,75 €/h HT : 22 vCPU et 400 Go de NVMe pour des simulations en
   parallèle ; S3 à 0,007 €/Go·mois sans frais de sortie ; 200 € de crédit d'essai pendant 1 mois. Limites :
   pilote NVIDIA à installer, quota GPU d'un compte en essai incertain avant la première facture (contournable en
   achetant un crédit), contradiction entre deux pages sur la granularité de facturation.
3. **Verda** (Helsinki) : RTX A6000 48 Go à 0,7591 €/h (spot 0,3795 €/h), ou V100 16 Go à 0,2156 €/h si torch
   prend en charge sm_70. C'est le moins cher, en EUR, avec un spot adapté aux campagnes. Limites : solde prépayé
   (à zéro, les volumes sont supprimés), stockage objet en bêta, pas de région en France, mention HT/TTC et quotas
   non vérifiés.

Autre option : Nebius (L40S préemptible à partir de 0,74 $/h, facturation à la seconde, quota de 8 GPU dès
l'inscription, images CUDA avec NVIDIA Container Toolkit), mais facturé en USD et sans L40S ni H100 en France.
À écarter : Hetzner (209 € d'installation pour un usage de quelques jours) et Genesis Cloud (site hors service,
liquidation rapportée).

## 5. Sources (toutes lues le 2026-11-07)

- Scaleway, catalogue de prix (API publique) : https://api.scaleway.com/product-catalog/v2alpha1/public-catalog/products?page_size=500&product_types=instance (pages 1 et 2), `…&product_types=object_storage`, `…&product_types=block_storage`
- Scaleway, page de prix GPU (inaccessible : défi anti-robot, 403) : https://www.scaleway.com/en/pricing/gpu/
- Scaleway, quotas : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/organizations-and-projects/organization/organization-quotas.mdx
- Scaleway, facturation des instances : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/instances/faq.mdx
- Scaleway, FAQ facturation (minimum 60 min, cartes acceptées) : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/billing/faq.mdx
- Scaleway, images GPU : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/gpu/how-to/use-preinstalled-env.mdx
- Scaleway, vérification d'identité : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/account/setup-lifecycle/verify-identity.mdx et `…/pages/account/troubleshooting/cannot-verify-identity.mdx`
- Scaleway, types de compte : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/account/concepts/understanding-account.mdx
- Scaleway, essai gratuit du stockage objet : https://raw.githubusercontent.com/scaleway/docs-content/main/pages/object-storage/faq.mdx
- OVHcloud, catalogue : https://eu.api.ovh.com/1.0/order/catalog/public/cloud?ovhSubsidiary=FR
- OVHcloud, page GPU (prix HT, crédit de 200 €) : https://www.ovhcloud.com/fr/public-cloud/gpu/
- OVHcloud, régions : https://www.ovhcloud.com/fr/public-cloud/regions-availability/
- OVHcloud, déploiement d'une instance GPU (GRA11, pilote) : https://docs.ovhcloud.com/en/guides/public-cloud/compute/deploy-a-gpu-instance.md
- OVHcloud, facturation : https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/analyze-billing.md et https://docs.ovhcloud.com/en/guides/account-and-service-management/managing-billing-payments-and-services/changing-hourly-monthly-billing.md
- OVHcloud, quotas : https://docs.ovhcloud.com/fr/guides/public-cloud/cross-functional/increasing-public-cloud-quota.md
- Hetzner : https://www.hetzner.com/dedicated-rootserver/matrix-gpu/ , https://www.hetzner.com/dedicated-rootserver/gex45/ , https://www.hetzner.com/storage/object-storage/
- Nebius : https://nebius.com/prices , https://docs.nebius.com/compute/resources/pricing , https://docs.nebius.com/overview/regions , https://docs.nebius.com/compute/resources/quotas-limits , https://docs.nebius.com/compute/storage/boot-disk-images , https://docs.nebius.com/signup-billing/sign-up
- Verda : https://verda.com/pricing?currency=eur , https://docs.verda.com/welcome-to-verda/pricing-and-billing/ , https://docs.verda.com/welcome-to-verda/locations-and-sustainability/ , https://docs.verda.com/storage/object-storage/ , https://docs.verda.com/cpu-and-gpu-instances/set-up-a-gpu-instance/ , https://docs.verda.com/welcome-to-verda/release-notes/
- Genesis Cloud : https://www.genesiscloud.com/ (échec TLS), https://genesiscloud.com/ (erreur 522), https://bizety.com/?p=12386 (article du 23/09/2025)
- Dépôt (lecture seule) : `infra/README.md` §2.1, §6.2, §6.3 ; `infra/docker/Dockerfile.gpu` (torch 2.14.1, CUDA 12.6) ; `src/milady/sim/mhd3d.py` (`BENCHMARK_NOTES`)

Les pages et réponses d'API brutes sont conservées dans
(copies de travail non versionnées).
