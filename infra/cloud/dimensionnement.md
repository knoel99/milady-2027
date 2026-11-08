# Dimensionnement des calculs à louer (M1, M3–M8), d'après le dépôt

Lu le 2026-11-07 dans le dépôt (code et documentation seulement : rien n'a été lancé).
Ce document ne contient **aucun prix** ; les heures ci-dessous sont à multiplier par les tarifs relevés
ailleurs (sources datées). Les affirmations sur des plateformes tierces non vérifiées sont marquées
« non vérifié ».

## 0. En une phrase

Aux tailles configurées (64³, 37 + 12 simulations, 480 instantanés d'entraînement), tout le travail
louable maintenant tient en **≈ 1 à 5 heures-GPU de calcul** (incertitude ×3, aucune mesure GPU
n'existe) ou **≈ 45 à 190 heures-vCPU** sur processeur ; le vrai coût sera le temps de mise en route
et de débogage du chemin GPU, jamais exécuté. Si la vérification de résolution impose 128³ ou 256³
pour Re ≥ 100 (probable d'après l'estimation de Kolmogorov, §3.3), il faut ajouter **≈ 7 à 55
heures-GPU** et un processeur ne suffit plus pour 256³.

## 1. Hypothèses de coût

### 1.1 Processeur (mesuré, `milady/sim/mhd3d.py` l. 75–107, BENCHMARK_NOTES)

| Cas (float32, 1 trajectoire, RK4) | 1 fil | 2 fils |
|---|---|---|
| dynamique 32³ | 0,014 s | 0,011–0,015 s |
| dynamique 64³ | 0,15 s | **0,073–0,083 s** |
| cinématique 64³ | 0,052 s | **0,031 s** |

Machine de mesure : 4 cœurs partagés (charge ≈ 4,5). Un cœur dédié récent peut aller 1,5 à 2 fois
plus vite ; à l'inverse, 16 simulations simultanées se disputent la bande passante mémoire. J'applique
un facteur **0,5 à 1,2** aux chiffres mesurés pour les fourchettes. 32³ → 64³ : ×7 à 10 ; j'utilise
le même facteur pour 64³ → 128³ → 256³ (extrapolation, non mesurée). Sur-souscription : ×10 à 100
plus lent (même bloc, l. 89–91) : jamais plus de fils que de cœurs libres.

Mémoire (infra/README.md §6.2, l. 257–265) : état (u, B) = 6 N³ × 4 octets (6,3 Mo à 64³, 50 Mo à 128³,
403 Mo à 256³) ; pic ≈ 15 états (100 Mo mesurés à 64³, 717 Mo à 128³ ; ≈ 6 Go extrapolés à 256³).

### 1.2 GPU (aucune mesure dans le dépôt : raisonnement, incertitude ≥ ×3)

Compté dans le code (`MHD3D._rhs`, l. 491–510, `step`, l. 525–561) : un second membre dynamique =
6 appels FFT (18 FFT scalaires) + ≈ 90 noyaux élémentaires (rotationnels, produits vectoriels,
projection de Leray, masques) ; un pas RK4 ≈ **430 lancements de noyaux** (cinématique : ≈ 140).

- **64³** : chaque noyau touche 3 à 6 Mo, soit quelques µs sur un GPU moderne ; le pas est limité par
  la latence de lancement de PyTorch en mode eager (≈ 5–20 µs par opération côté Python), pas par les
  FLOP. Estimation : **3–10 ms/pas en dynamique, 1–4 ms en cinématique**, quasi indépendante du modèle
  de GPU (un GPU d'entrée de gamme ≈ un H100 à cette taille). Gain ≈ 8–25× sur 2 fils CPU.
  Conséquence utile : `n_traj` (trajectoires groupées dans un même tenseur) est presque gratuit sur
  GPU jusqu'à ≈ 4–8, alors qu'il coûte linéairement sur CPU.
- **128³** : limité par la bande passante mémoire ; ≈ **15–40 ms/pas** pour un GPU de 1–2 To/s.
- **256³** : ≈ **120–300 ms/pas** pour 1–2 To/s ; proportionnellement plus lent sur une carte à
  plus faible bande passante (ordre de grandeur, caractéristiques constructeur non relues ici).
- Plusieurs processus sur un même GPU (ce que fait `make sweep` en local : tous les créneaux sur le
  GPU 0, `milady/sweep.py` l. 497–505, 544–561) remplissent les temps morts de lancement ; gain
  attendu ×2–4 en débit à 64³ (non vérifié). Chaque processus a besoin d'un vCPU pour lancer ses noyaux.

Première action sur la machine louée, qui remplace toutes ces hypothèses (et produit les chiffres de
la scène vidéo M15) : `python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --dtype float32 --steps 50`
puis `--mode kinematic --n-traj 4`.

### 1.3 Pas de temps (CFL, `cfl_dt` l. 588–591 ; boucle d'événements `milady/sim/run.py` l. 630–647)

dt = min(dt_config, cfl / ((max|u| + max|B|) |k|max)), |k|max = √3 × (N−1)//3 = 36,4 (64³), 72,7 (128³),
147 (256³). Le pas est recalculé à chaque événement (diagnostic ou instantané) et rendu constant sur
l'intervalle.

- **ABC cinématique** : vitesse imposée, max|u| = √6 exactement (atteint sur la grille 64³) ;
  dt_CFL = 0,01122 → 45 sous-pas par intervalle de diagnostic de 0,5 → **22 500 pas** pour 250 unités
  de temps (déterministe, pas de B dans le CFL en cinématique).
- **TG dynamique** : vitesse S = max|u| + max|B| inconnue avant la première simulation (forçage
  « turbulent » visant u_rms ~ 1, ordre de grandeur seulement). dt = 0,005 tant que S ≤ 5,5 ; sinon
  plus petit. Pour S = 3 à 10 : **28 000 à 52 000 pas** à 64³ (77 000 si S ≈ 15) ; 31 000–102 000
  à 128³ ; 63 000–207 000 à 256³.

## 2. Tableaux par calcul

Tailles de fichiers : float32 brut = forme × 4 octets ; `write_mff` compresse en gzip niveau 4
(`milady/data/format.py` l. 372–373), gain sur des champs float32 turbulents non mesuré (probablement
faible) : les volumes ci-dessous sont des **majorants**. Les instantanés restent en mémoire pendant la
simulation (`_RunState.add_snap`, `run.py` l. 484) et chaque point de contrôle `.npz` les réécrit tous.

### M1 — `palier1_mhd2d` (MHD 2D, NumPy, CPU seulement)

| Grandeur | Valeur | Source |
|---|---|---|
| Simulations | 11 (η de 4e-3 à 2,26e-2), 16 trajectoires chacune | `infra/configs/palier1_mhd2d.yaml` |
| Grille, pas | 32², dt = 0,01 fixe | idem |
| Temps | t_burn 30 + t_keep 150 = 180 → **18 000 pas** par simulation | idem |
| Instantanés | 150 par trajectoire (2 400 par simulation) | idem, `sweep.output_times` |
| Champs | velocity + magnetic_field, (16, 150, 32, 32, 2) chacun | inventaire M1 |
| Taille | 39,3 Mo par fichier ; **0,43 Go** au total | calcul |
| Mémoire | < 0,5 Go par processus | estimation |
| Temps CPU | E2 (≈ 223 000 pas à 16 trajectoires) a pris ≈ 30 min (`experiences/index.qmd` l. 69) → M1 (198 000 pas) ≈ **25–30 min en série, ≈ 0,5–1 h-vCPU** ; 11 en parallèle : quelques minutes | calcul |
| GPU | aucun (NumPy) | config `gpus: 0` |

Ne justifie pas une location : peut tourner sur le portable, ou sur des cœurs libres de la VM pour
avoir tout dans le même catalogue.

### M3 — `palier2_abc3d` (dynamo cinématique ABC, 64³)

| Grandeur | Valeur | Source |
|---|---|---|
| Simulations | 37 (Rm = 4…40), `n_traj` = 2 graines | `palier2_abc3d.yaml` |
| Pas | 250 unités / 0,0111 = **22 500 pas** (×2 trajectoires groupées) | §1.3 |
| Instantanés | 20 par trajectoire (t = 155…250, tous les 5) | config |
| Champs | velocity + magnetic_field (2, 20, 64, 64, 64, 3) chacun ; u est constant | config l. 58 |
| Taille | 252 Mo par fichier ; **9,3 Go** (4,7 Go sans `velocity`) | calcul |
| Mémoire | solveur ≈ 0,1–0,2 Go + instantanés 0,25 Go + torch ≈ 1–2 Go RSS par processus ; VRAM < 1 Go par processus (contexte CUDA compris) | §1.1 |
| CPU | 22 500 × 2 × 0,031 s ≈ 23 min par simulation (2 fils) → 14,3 h de tâches à 2 fils ≈ **29 h-vCPU** (fourchette **15–35**) | BENCHMARK_NOTES |
| GPU | 22 500 × 1–4 ms ≈ 0,4–1,5 min de calcul par simulation (+ démarrage CUDA, écriture) → **0,25–1 h-GPU** ; temps réel 0,3–1,5 h avec 4–8 processus sur un GPU | §1.2 |
| Résolution | 64³ (k_max = 21) suffisant jusqu'à Rm = 40 (échelle résistive ~ Rm^-1/2 ≈ 0,16, soit k ≈ 6 ; E3 tenait à 32³ jusqu'à Rm = 30) | estimation |

### M4 — `palier2_tg3d` (MHD dynamique Taylor–Green, 64³)

| Grandeur | Valeur | Source |
|---|---|---|
| Simulations | 12 : Re ∈ {25, 50, 100, 200} × Pm ∈ {0,5 ; 1 ; 2}, `n_traj` = 1 | `palier2_tg3d.yaml` |
| Pas | 140 unités : **28 000–52 000 pas** (S = 3–10 ; 77 000 si S ≈ 15) | §1.3 |
| Instantanés | 40 (t = 101…140) ; diagnostics tous les 0,1 | config |
| Champs | velocity + magnetic_field (1, 40, 64, 64, 64, 3) | config |
| Taille | 252 Mo par fichier ; **3,0 Go** | calcul |
| Mémoire | ≈ 1–2 Go RSS par processus ; VRAM < 1 Go par processus | §1.1 |
| CPU | 28 000–52 000 × 0,078 s (+ ≈ 10 % diagnostics et CFL) ≈ 40–80 min par simulation (2 fils) → 8–16 h de tâches à 2 fils ≈ **16–32 h-vCPU** (fourchette 8–38) | BENCHMARK_NOTES ; l'inventaire donnait ≈ 40 min et ≈ 8 h |
| GPU | 28 000–52 000 × 3–10 ms ≈ 1,5–9 min par simulation → **0,3–2 h-GPU** | §1.2 |
| Risque | résolution insuffisante probable pour Re ≥ 100 (§3.3) | config l. 12–14 |

### M5 — `train_fm3d` (flow matching conditionnel, MLP)

| Grandeur | Valeur | Source |
|---|---|---|
| Données | campagne M4 : 12 points × 1 trajectoire × 40 instantanés = 480 échantillons ; validation {Re 100, Pm 1} et test {Re 50, Pm 2} → **400 en entraînement** | `train_fm3d.yaml`, `data.py` l. 590–621 |
| Latent | kmax = 8 : 1 054 modes × 8 canaux = 8 432 dimensions ; ≈ 34 Ko par instantané, 16 Mo pour tout le jeu (sur le GPU) | config |
| Modèle | ResMLP largeur 1024, 6 blocs, expansion 2 : **47,8 M paramètres** d'après le code (`fm3d.py` l. 276–349), et non « ≈ 30 M » comme l'écrit le commentaire de la config (l. 18) | calcul |
| Itérations | ⌈400/64⌉ = 7 lots par époque × 200 époques = **1 400 itérations** (échauffement ramené à 140) | `fm3d.py` l. 1197–1206, `data.py` l. 711–713 |
| Coût par itération | ≈ 18 GFLOP (avant + arrière, lot 64) | calcul |
| Mémoire | poids 0,19 Go + gradients 0,19 + AdamW 0,38 + EMA 0,19 ≈ **1 Go** + contexte CUDA : **2–3 Go de VRAM** | calcul |
| Points de contrôle | ≈ 0,77 Go chacun (poids + EMA + état AdamW, `fm3d.py` l. 1295–1311) ; `last.pt` + `final.pt` ≈ 1,5 Go par run | calcul |
| GPU | limité par les lancements de noyaux : ≈ 5–15 ms/itération → 10–30 s de calcul ; avec lecture des 12 fichiers MFF (3 Go), validation, points de contrôle et évaluation rapide finale : **5–20 min, ≈ 0,1–0,3 h-GPU** | estimation |
| CPU (16–32 vCPU) | ≈ 0,05–0,3 s/itération → 1–7 min, ≈ **1–4 h-vCPU** avec les entrées-sorties | estimation |
| Multi-GPU | inutile (1 400 itérations) ; `NGPUS=1` | — |

### M6 — évaluation 3D (`make eval … --out eval.json`)

| Grandeur | Valeur |
|---|---|
| Travail | ≤ 12 points × 64 échantillons, Heun 50 pas (≈ 100 évaluations du réseau par lot de 16) ≈ 4 800 passes avant ; décodage sur grille 26³ ; métriques ; lecture des instantanés de référence (≤ 3 Go) |
| Référence | `n_ref` = 128 demandé mais **40 instantanés seulement par point** (n_traj = 1) : plancher de distance d'énergie estimé sur 20 contre 20 |
| GPU | < 5 min de calcul, ≈ **0,05–0,1 h-GPU** par évaluation ; 3 évaluations (M5, M7, témoin) |
| CPU | ≈ 1–2 min de réseau + entrées-sorties, ≈ **0,5–1 h-vCPU** par évaluation |
| Lacune | σ(dissipation)/σ_ref par échantillon non calculé (§6, point 1) |

### M7 — réglage fin par la perte de stationnarité (+ run témoin)

| Grandeur | Valeur |
|---|---|
| Commande | `--init-from …/final.pt --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0` (`train_fm3d.yaml` l. 13–15) |
| Coût par itération | perte usuelle + `n_cond` × `n_per` = 64 échantillons tirés par 8 pas de Heun différentiables (16 évaluations du réseau, rétropropagation à travers tout) ≈ **17× une itération normale** |
| Mémoire | activations de 16 évaluations × 64 échantillons ≈ 0,1 Go + copie d'ancrage 0,19 Go : **3–4 Go de VRAM** |
| GPU | 2 000 × 17 × 5–15 ms ≈ 3–9 min (jusqu'à 20 min avec les surcoûts) ≈ **0,1–0,4 h-GPU** |
| CPU (32 vCPU) | 2 000 × 17 × 0,05–0,3 s ≈ 0,5–2,8 h de temps réel ≈ **15–90 h-vCPU** (le poste le plus lourd en CPU) |
| Témoin | même départ, `stationarity.enabled=false`, 2 000 itérations : < 1 min GPU, 2–10 min CPU |
| Points de contrôle | 2 runs × 1,5 Go |

### M8 — générateur de modes propres ABC conditionné par Rm (aucune config ; esquisse dérivée)

Variante de `train_fm3d.yaml` à écrire **avant** la location (fichier non créé, dépôt non modifié) :
`data.dataset: milady_palier2_abc3d`, `data.campaign: palier2_abc3d`, `data.fields: [magnetic_field]`,
`conditioning: [{name: Rm, transform: log}]` (Rm est un paramètre balayé, lu directement par
`param_value`, `data.py` l. 80–99), `auto_dataset.val/test` = quelques Rm de part et d'autre des seuils
8,87 / 17,6 / 26,8, `model.symmetry_b_sign: true`. Le mode cinématique est prévu par le code
(écoulement imposé recalculé par `metrics.imposed_flow`, `fm3d.py` l. 584–588).

| Grandeur | Valeur |
|---|---|
| Données | 37 Rm × 2 trajectoires × 20 instantanés = 1 480 échantillons (≈ 1 240 en entraînement si 6 Rm sont réservés) |
| Latent | B seul : 4 canaux ; kmax 8 → 4 216 dimensions (39 M paramètres) ; kmax 12 → 3 576 modes, 14 304 dimensions (≈ 60 M paramètres) — choisir kmax d'après E_B(k) des modes de E3 |
| Itérations | ⌈1 240/64⌉ = 20 × 200 époques = **4 000** |
| GPU | ≈ 0,5–1,5 min de calcul + entrées-sorties (4,7–9,3 Go à relire) → **0,1–0,3 h-GPU** ; VRAM 2–3 Go |
| CPU | 4 000 × 0,04–0,25 s ≈ 3–17 min → **2–10 h-vCPU** |
| Mises en garde | après t_burn = 150 les 20 instantanés d'une même trajectoire sont presque identiques (mode propre renormalisé ; seuls les modes oscillants varient) : la diversité réelle est ≈ 2 graines × symétries par Rm, et les distances d'énergie par point seront peu informatives. La perte de stationnarité « magnetic » attend λ comme nombre ou nom de **paramètre** (`fm3d.py` l. 655–656) ; or λ est un diagnostic du catalogue (`growth_rate_fit`), pas un paramètre : non utilisable tel quel. |

## 3. Totaux

### 3.1 Scénario A : configurations telles quelles (64³)

| Calcul | h-vCPU (CPU seul) | h-GPU de calcul | Données produites |
|---|---|---|---|
| M1 | 0,5–1 | 0 | 0,43 Go |
| M3 | 15–35 | 0,25–1 | 9,3 Go (4,7 sans u) |
| M4 | 8–38 | 0,3–2 | 3,0 Go |
| M5 | 1–4 | 0,1–0,3 | 1,5 Go (points de contrôle) |
| M6 (×3) | 1,5–3 | 0,15–0,3 | < 10 Mo (JSON) |
| M7 + témoin | 16–95 | 0,1–0,4 | 3 Go |
| M8 | 2–10 | 0,1–0,3 | ≈ 1,3 Go |
| **Total** | **≈ 45–190** | **≈ 1–4,5** | **≈ 19 Go** (≈ 14 Go sans u en ABC) |

Mise en route à ajouter, indépendante de la taille : bootstrap 5–20 min sur VM neuve (README l. 71–73),
construction de l'image GPU, banc d'essai, simulation pilote, débogage du chemin GPU jamais exécuté
(prévoir 2–4 h), copies de données. **Prévoir une session de 8 à 12 heures facturées sur un GPU**, ou
6 à 10 heures de temps réel sur un CPU de 32 vCPU. En comparaison, le plan de thèse prévoit ≈ 700 h
A100 pour le palier 1 complet (M2) et ≈ 3 900 h pour le palier 2 complet (M12) : ces calculs sont des
démonstrations de chaîne, ≈ 0,1 % du palier 2.

### 3.2 Scénario B : résolution corrigée pour M4 (si le pilote la confirme insuffisante)

| Variante | Simulations | Pas | GPU | CPU | Données |
|---|---|---|---|---|---|
| Re = 100 à 128³ | 3 | 31 000–102 000 | 15–40 ms/pas → 0,4–3,4 h-GPU | 0,6–0,8 s/pas (2 fils) → 30–140 h-vCPU | 3 × 2,0 Go |
| Re = 200 à 256³ | 3 | 63 000–207 000 | 0,12–0,3 s/pas → **6–50 h-GPU** (≈ 25 h au centre) | 5–8 s/pas (2 fils) : des semaines, **impraticable** | 3 × 16,1 Go |

Le scénario B ajoute ≈ 7–55 h-GPU et ≈ 50 Go. Il impose aussi, pour 256³, ≈ 16 Go d'instantanés en
mémoire vive par simulation et des points de contrôle `.npz` de taille croissante jusqu'à 16 Go toutes
les 15 min (§6, point 10). Alternative bon marché : abandonner Re = 200 et ne passer que Re = 100 à
128³ (+0,4–3,4 h-GPU).

### 3.3 Pourquoi la résolution est douteuse à Re ≥ 100

Estimation a priori (à confirmer par les spectres de la simulation pilote, comme le demande la config
l. 12–14) : ν = U_ref L_ref / Re = 0,5/Re ; taux de dissipation ε ≈ 0,5–2 (forçage « turbulent »,
ordre de grandeur) ; échelle de Kolmogorov η_K = (ν³/ε)^1/4 ; critère usuel des codes spectraux
k_max η_K ≳ 1.

| Re | 64³ (k_max 21) | 128³ (42) | 256³ (85) |
|---|---|---|---|
| 25 | 0,94–1,33 | 1,9–2,7 | — |
| 50 | 0,56–0,79 | 1,1–1,6 | — |
| 100 | **0,33–0,47** | 0,66–0,94 | 1,3–1,9 |
| 200 | **0,20–0,28** | **0,39–0,56** | 0,8–1,1 |

À Pm = 2, l'échelle résistive est encore ≈ 1,4 fois plus petite. À 64³, seuls Re = 25 (et à la limite
50) sont résolus ; les résultats Re ≥ 100 à 64³ ne doivent être montrés que comme « sous-résolus,
provisoires ».

## 4. VRAM, RAM, disque, stockage objet

| Ressource | Scénario A | Scénario B |
|---|---|---|
| VRAM | ≤ 1 Go par simulation 64³ ; 8 en parallèle ≈ 4–8 Go ; entraînement 2–4 Go → **16 Go suffisent, 24 Go confortables** | 128³ ≈ 1,5 Go ; 256³ ≈ 8–10 Go par simulation (6 Go extrapolés + cuFFT + cache) → 24 Go pour 2 en parallèle |
| RAM | pile Docker ≈ 2–3 Go + 8 processus × 1,5–2 Go → **32 Go minimum, 64 Go confortables** | + ≈ 20–35 Go par simulation 256³ (16 Go d'instantanés + copie par np.stack au point de contrôle et à l'écriture) → 64 Go si une à la fois, 96–128 Go pour deux |
| Disque VM | images ≈ 15 Go + données ≈ 19 Go + copie MinIO + travail → **100–150 Go** | **200 Go** |
| Stockage objet (bucket S3) | ≈ 20–25 Go | ≈ 75–100 Go |
| Sortie réseau | quelques centaines de Mo si l'on ne rapatrie que les JSON dérivés et quelques champs ; ≈ 20 Go pour tout | ≈ 70 Go pour tout |
| vCPU | ≥ nombre de simulations simultanées + 2 (services) : **8–16** sur une VM GPU ; **32** pour le profil CPU seul | idem |

Précision : float32 partout (`dtype: float32`) ; aucun besoin de FP64 matériel ni de cœurs tenseurs
pour les simulations ; bf16 automatique à l'entraînement si le GPU le permet.

## 5. Ce que suppose le chemin de déploiement

**`infra/deploy/bootstrap_vm.sh`** (lu en entier) :

- lancé en **root** (`sudo`), sur **Ubuntu 22.04 ou 24.04** (autre système : avertissement, on
  continue ; Ubuntu 22.04 jamais testé) ; `apt`, et **systemd** (sinon Docker doit déjà tourner) ;
- installe **Docker CE** depuis download.docker.com (retire `docker.io`, `podman-docker`…) ; jamais
  exécuté sur une Ubuntu sans Docker ;
- GPU : exige un **pilote NVIDIA déjà installé** (`nvidia-smi` doit répondre ; sinon il passe en CPU et
  conseille `ubuntu-drivers install --gpgpu` + redémarrage, ou une image « GPU » du fournisseur) ;
  installe le **NVIDIA Container Toolkit** depuis nvidia.github.io et déclare le runtime à Docker ;
- image `milady:gpu` : base `pytorch/pytorch:2.14.1-cuda12.6-cudnn9-runtime`, **pilote ≥ 525** ;
  GPU Blackwell (B200, RTX 50xx) : base CUDA 13, pilote ≥ 580 **et** torch à changer dans
  `requirements-gpu.txt` (`Dockerfile.gpu` l. 1–19) → préférer Ampere, Ada ou Hopper ;
- sortie Internet vers Docker Hub, PyPI, download.docker.com, nvidia.github.io (image GPU de
  plusieurs Go) ;
- disque **100–200 Go** ; pare-feu : **SSH (22) seul** ; services liés à 127.0.0.1 (5432 PostgreSQL,
  9000/9001 MinIO, 5000 MLflow, 8888 Jupyter), accès par tunnel SSH ; `worker-gpu` a `shm_size: 16gb`.

**Plateformes « conteneur » (pods RunPod, instances conteneur Vast.ai…)** : on y est déjà *dans* un
conteneur, en général sans démon Docker ni systemd ni accès root au noyau (**non vérifié** ici, à
confirmer dans leur documentation, certaines offrent aussi de vraies VM). Conséquences tirées du code :

- `bootstrap_vm.sh` et la pile `docker compose` (PostgreSQL, MinIO, MLflow) **ne peuvent pas** tourner
  telles quelles ;
- reste le **chemin venv** : `make setup GPU=1` (torch 2.14.1+cu126, Python ≥ 3.11 exigé, Makefile
  l. 85–93 ; vérifié seulement en CPU), `RUN=local`, catalogue **SQLite** `data/catalog.sqlite`, fichiers
  dans `data/store/` ou dans un bucket S3 du fournisseur (`MILADY_STORAGE_URI` + `MILADY_S3_*`), MLflow
  absent (le journal tombe dans `metrics.jsonl` si `MLFLOW_TRACKING_URI` n'est pas défini) ;
- il faut alors rapatrier `data/catalog.sqlite`, `data/store/` et `data/runs/` **avant** de détruire le
  pod ; seules les simulations se réinjectent ensuite dans un PostgreSQL central
  (`python -m milady.catalog ingest`), pas les modèles ni les évaluations (README §3).

Une **VM complète** (Ubuntu, root, image GPU du fournisseur) est donc le seul cas qui exerce le chemin
documenté de bout en bout.

## 6. Jamais testé (README §12, l. 429–453 ; page calcul l. 190)

- l'image `milady:gpu` complète (construite seulement jusqu'à l'étape pip, puis corrigée), le NVIDIA
  Container Toolkit, l'étape 3 de `bootstrap_vm.sh`, le service `worker-gpu` ;
- le solveur et l'entraînement sur CUDA (bf16, plusieurs GPU, NCCL, `make train NGPUS>1`), et
  `make setup GPU=1` ;
- plusieurs simulations partageant un même GPU (comportement par défaut de `make sweep` en local) ;
- l'installation de Docker sur une Ubuntu neuve, Ubuntu 22.04, `cloud-init.yaml`, `deploy_remote.sh` ;
- les buckets S3 des fournisseurs et `make backup` vers `s3://…` (seul MinIO a servi) ;
- Slurm réel, Apptainer (sans objet pour une VM louée) ;
- les campagnes à leur taille réelle (37 et 12 simulations 64³), l'entraînement de 200 époques, le
  réglage fin M7 à taille réelle ; M8 n'a pas de configuration.

## 7. À corriger ou décider AVANT de louer (sur le portable, sans frais)

1. **σ(dissipation)/σ_ref absent de l'évaluation 3D** : `budget_summary` (`metrics.py` l. 451–470) ne
   renvoie que des moyennes ; `_ensemble_stats` (l. 570–584) garde l'écart-type des hélicités mais pas
   celui des dissipations. Ajouter l'écart-type par échantillon de Dν + Dη (et de chaque terme), son
   rapport à la référence, et un test. Indispensable pour M6/M7 (scène « Corollaire 6 ») ; sinon il
   faudrait relancer les évaluations.
2. **Convertisseurs vidéo** : `video_plan/proto/tools/extract_data.py` n'a que `e1_rate` et une
   fonction `palier1_eta_sweep` qui renvoie `None`. Écrire un convertisseur par scène (MFF → JSON pour
   M1/M3/M4, JSON d'évaluation → JSON pour M5–M8, requête catalogue pour les durées M15) et les tester
   sur des sorties réduites produites sur CPU (mêmes formats). Sur la VM, on ne fait que les exécuter.
3. **Écrire et tester la config M8** (`train_fm3d_abc.yaml`, §2 M8) sur une campagne ABC réduite
   (16³, 2 Rm) ; choisir kmax ; laisser la stationnarité « magnetic » de côté tant que λ n'est pas un
   paramètre lisible.
4. **Décider la résolution de M4** (§3.3) : préparer dès maintenant une campagne séparée à 128³
   (Re = 100) et éventuellement 256³ (Re = 200), ou retirer Re = 200. Le jeu de données automatique ne
   lit **qu'une** campagne (`_create_dataset`, `data.py` l. 799–817) : avec deux campagnes, passer par
   `data.files` ou un jeu enregistré à la main (à vérifier). Le latent tronqué à |m| ≤ 8 rend
   l'entraînement indépendant de N.
5. **Taille du jeu d'entraînement** : 400 échantillons pour 47,8 M paramètres, et 40 instantanés de
   référence par point au lieu des 128 demandés. Option à trancher avec les encadrants : `n_traj: 4`
   dans `palier2_tg3d` (×4 données et références ; quasi gratuit sur GPU, ×4 sur CPU, ×4 en volume :
   12 Go). Corriger aussi le commentaire « ≈ 30 M paramètres » de `train_fm3d.yaml`.
6. **ABC** : retirer `velocity` de `output.fields` (u constant, déjà recalculé analytiquement) : 9,3 → 4,7 Go.
7. **Ordre et gel des données** : le jeu `milady_palier2_tg3d` est créé une fois pour toutes à partir
   des simulations `done` au moment du premier `make train` ; lancer l'entraînement avant la fin de M4
   fige un jeu incomplet. Ne pas réutiliser les noms de campagne réels pour des essais réduits sur le
   catalogue de la VM.
8. **Parallélisme sur un GPU** : `max_parallel` vaut 16 (ABC) et 12 (TG) ; sur une VM à 8 vCPU, cela
   met 16 processus sur 8 cœurs (1 fil chacun). Passer `SWEEP_ARGS="--max-parallel 4"` à 8 (≤ vCPU − 2).
9. **Instance interruptible** : mettre `runtime.checkpoint_to_storage: true` (point de contrôle aussi
   dans S3, toutes les 15 min).
10. **256³ seulement** : les instantanés s'accumulent en mémoire (`run.py` l. 484) et chaque point de
    contrôle les réécrit tous (jusqu'à 16 Go par simulation) : allonger `checkpoint_every_s` ou écrire
    les instantanés au fil de l'eau avant toute campagne 256³.
11. Préparer le bucket S3 du fournisseur (`.env`, README §2.5), une clé limitée à ce bucket, et une
    alerte de budget.

## 8. Profils de machine recommandés

**Profil 1 — une VM avec un GPU (recommandé)** : seule option qui produit les temps GPU (M15), valide
le chemin GPU pour la thèse et ouvre le scénario B.

| | Minimum | Confortable |
|---|---|---|
| GPU | 1 × 16 Go, Ampere/Ada/Hopper (CUDA 12.x) | 1 × 24–48 Go ; inutile de prendre 80 Go ou un H100 pour 64³ (limité par les lancements) ; une carte à forte bande passante ne sert qu'au scénario B |
| vCPU | 8 | 16 |
| RAM | 32 Go | 64 Go (96–128 Go pour deux simulations 256³ en parallèle) |
| Disque | 100 Go SSD | 150–200 Go |
| Système | VM complète Ubuntu 22.04/24.04, root, image GPU du fournisseur (pilote ≥ 525) | idem |
| Réseau | SSH seul entrant | idem |
| Stockage objet | 25 Go, même région | 100 Go (scénario B) |
| Durée | scénario A : une session de 8–12 h facturées | scénario B : + 1 à 3 jours |

Pas de multi-GPU : l'entraînement (1 400 itérations) n'en tire rien, et les simulations 64³ tiennent
toutes sur une seule carte.

**Profil 2 — CPU seul (alternative la moins risquée pour le scénario A)** : 32 vCPU dédiés (instance
« calcul »), 64 Go de RAM, 100 Go de disque, même stockage objet. Il emprunte le chemin **déjà testé**
(`bootstrap_vm.sh --cpu`, image `milady:cpu`) et termine le scénario A en ≈ 6–10 h de temps réel
(16 simulations à 2 fils en parallèle). Il ne donne aucun temps GPU, rend M7 lent (jusqu'à ≈ 3 h) et
exclut 256³.

**Non recommandé pour ce dépôt** : plateformes conteneur sans démon Docker (chemin venv non testé sur
GPU, pas de PostgreSQL/MinIO/MLflow, rapatriement manuel) ; GPU Blackwell (image à reconstruire).

## 9. Ordre d'exécution

0. **Portable, avant location** : §7 (points 1 à 11), `make test`, campagnes réduites et convertisseurs
   testés de bout en bout ; M1 peut aussi tourner ici (≈ 30 min).
1. **VM** : `sudo infra/deploy/bootstrap_vm.sh` (test de fumée GPU inclus) ; en cas d'échec du chemin
   GPU, relancer avec `--cpu` pour ne pas perdre la session.
2. **Banc d'essai M15** : `python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --dtype float32 --steps 50`,
   puis `--mode kinematic --n-traj 4` ; relever `nvidia-smi` (VRAM). Recalculer ce document avec ces chiffres.
3. **Pilote** : la simulation TG la plus exigeante (Re = 200, Pm = 2) seule ; lire `wall_time_s`, le pas
   effectif et les spectres E_u(k), E_B(k) → trancher 64³ / 128³ / 256³ (scénario A ou B).
4. **M3 (ABC, 37) puis M4 (TG, 12)**, `--max-parallel 4` à 8 ; M1 en parallèle sur les cœurs libres
   s'il n'a pas tourné sur le portable. M3 et M4 sont indépendants et peuvent se chevaucher.
5. Vérifier au catalogue que les 12 simulations TG (et les 37 ABC) sont `done`
   (`python -m milady.catalog sims --campaign palier2_tg3d`) ; sauvegarde intermédiaire `make backup`.
6. **M5** `make train CONFIG=infra/configs/train_fm3d.yaml` (évaluation rapide incluse), puis **M6**
   `make eval … EVAL_ARGS="--out s3://…/eval_base.json"`.
7. **M7** réglage fin depuis `final.pt` + run témoin (même départ, β = 0, 2 000 itérations), puis
   évaluation des deux.
8. **M8** entraînement et évaluation sur `palier2_abc3d` (après M3).
9. **Collecte** : requête SQL des heures par campagne (README §6.2), `python -m milady.catalog summary`,
   JSON d'évaluation, `make backup BACKUP_TARGET=s3://…`, exécution des convertisseurs → JSON des
   scènes ; ne télécharger que les JSON dérivés et quelques champs à rendre ; puis supprimer la VM et
   vérifier qu'il ne reste ni disque, ni instantané, ni IP réservée (README §8).

## 10. Hors périmètre de cette location

M2 (palier 1 complet, ≈ 700 h A100, non configuré), M12 (palier 2 complet, ≈ 3 900 h A100), M9–M11
(CPU, code absent pour une partie), M13–M14 (données VKS et DRESDYN non publiques).
