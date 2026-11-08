# Voies académiques et gratuites (ou presque) pour les calculs MilaDy

Recherche faite le **2026-11-08** (pages lues ce jour-là, sauf mention contraire). Je n'ai rien lancé et
rien modifié dans le dépôt. Les pages web ont servi de données uniquement. Ce que je n'ai
pas pu lire à la source est marqué **non vérifié**. Les numéros [S…] renvoient aux sources du §9 (URL et
date). Les copies brutes des pages n'ont pas été versionnées.

## 0. En bref

1. **Pour vous seul, aujourd'hui** (particulier, pas encore stagiaire), **aucune voie académique n'est
   ouverte** : GENCI, EuroHPC, les mésocentres et les crédits de recherche AWS, Google ou NVIDIA exigent
   tous une affiliation à un laboratoire ou à un établissement [S2][S9][S13][S20][S21][S23]. Ce qui reste
   pour vous : la location payante (`RECOMMANDATION-CLOUD.md` et ses annexes), Azure for Students si vous êtes étudiant
   à temps plein (100 $, GPU non mentionnés [S22]) et les GPU gratuits de Kaggle (non vérifié [S26]).
2. **La bonne voie académique est un « accès dynamique » (AD) GENCI sur Jean Zay**, déposé par un
   encadrant. C'est gratuit et ouvert toute l'année. La réponse arrive en quelques jours à deux semaines
   environ, pour une allocation d'un an. Le volume maximal est de 50 000 heures GPU normalisées
   (= 12 500 h H100) [S2][S6]. Tout ce qui manque pour le stage (M1, M3–M8 : ≈ 1 à 60 h GPU de calcul selon
   la résolution, `dimensionnement.md` §3) en représente **moins de 1 %**. Même le budget
   complet de la thèse (≈ 1,1 × 10⁴ h A100, soit ≈ 2,2 × 10⁴ h normalisées, page `these/index.qmd`
   l. 957–973) reste sous le seuil.
3. **Qui dépose ?** S. Cheng (ENPC) ou D. Lucor (LISN), comme membre permanent : pour un AD, aucun visa du
   directeur de laboratoire n'est alors exigé [S2]. Une fois **stagiaire de M2** dans le laboratoire, vous pouvez
   être utilisateur du projet. Vous pouvez même déposer votre propre AD, mais le visa du directeur est alors
   obligatoire [S2]. Avant la convention de stage, vous ne pouvez pas avoir de compte : seuls les ingénieurs,
   chercheurs, post-doctorants, doctorants et stagiaires de M2 sont autorisés [S2].
4. **Le dépôt est déjà prêt pour Jean Zay** (`infra/slurm/`, vérifié contre la documentation IDRIS le
   2026-11-07). Il manque le compte et le projet, une image `.sif` construite et copiée, et un premier
   essai : rien n'a encore tourné sur GPU (§2.6).
5. **Les mésocentres sont des voies de secours.** Ruche (Paris-Saclay) a des V100 et des A100, et le LISN y
   a un référent, mais la machine est en fin de vie [S13][S14]. Le mésocentre de l'IP Paris (Cholesky) ne
   vise pas le CEREA et était annoncé en panne [S18]. Pour un cluster propre à l'ENPC ou au CEREA, je n'ai
   rien trouvé de public (**non vérifié**).
6. **EuroHPC (accès développement) et les crédits cloud n'apportent rien de plus que GENCI pour ce
   besoin.** EuroHPC demande un porteur sous contrat jusqu'à 3 mois après la fin de l'allocation [S9]. Les
   crédits sont réservés aux enseignants-chercheurs, doctorants et post-doctorants (Google, NVIDIA)
   [S21][S23], ou bien leur instruction prend 90 à 120 jours (AWS) [S20]. OVHcloud et Scaleway ne
   proposent que des programmes pour start-up [S24][S25].

## 1. Rappel : ce qu'il faut calculer, en heures normalisées GENCI

Règle d'équivalence GENCI : « 1 GPU MI300 = 1 GPU H100 = 2 GPU A100 = 2 GPU MI250 = 4 GPU V100 » [S1].
L'IDRIS précise : « 50k heures GPU normalisées = 50k heures V100 ou 25k heures A100 ou 12,5k heures H100 » [S6].

| Besoin | Heures GPU (source) | Heures normalisées (V100) | Part du seuil AD (50 000) |
|---|---|---|---|
| Stage : M1, M3–M8 à 64³ (scénario A) | ≈ 1–4,5 h de calcul (`dimensionnement.md` §3.1) | ≈ 4–18 sur H100 | < 0,1 % |
| Idem, M4 corrigé à 128³/256³ (scénario B) | + ≈ 7–55 h (`dimensionnement.md` §3.2) | + ≈ 28–220 sur H100 | < 0,5 % |
| Marge de mise au point (chemin GPU jamais exécuté, ×5 sur le total) | ≈ 300 h | ≈ 1 200 sur H100 | 2,4 % |
| Paliers 1 + 2 de la thèse (M2, M12) | ≈ 700 + 3 900 h A100 (`these/index.qmd` l. 965–973) | ≈ 9 200 | 18 % |
| Thèse entière, réserve comprise | ≈ 1,1 × 10⁴ h A100 (idem) | ≈ 22 000 | 44 % |

Côté CPU, le seuil AD est de 500 000 heures-cœur [S2]. Le palier 0 (≈ 10³ h) et les simulations CPU du
palier 2 (≈ 2 × 10⁴ h, `these/index.qmd`) restent loin en dessous.

À 64³, `dimensionnement.md` §1.2 estime que le pas de temps dépend de la latence de lancement des noyaux, et non
du modèle de GPU : un V100 y irait presque aussi vite qu'un H100, pour 4 fois moins d'heures normalisées.
**Suggestion :** demander des heures **V100** pour les campagnes de simulation à 64³ et des heures **H100**
pour l'entraînement et les grilles 128³/256³. C'est une estimation : elle n'a pas été mesurée et est à
confirmer par le banc `python -m milady.sim.mhd3d bench` dès le premier accès.

## 2. GENCI : Jean Zay (IDRIS) et autres machines nationales

### 2.1 Types d'allocation

| | Accès dynamique (AD) | Accès régulier (AR) | Allocation stratégique (AS) |
|---|---|---|---|
| Volume | < 500 000 h CPU **et** < 50 000 h GPU normalisées [S2][S6] | au-delà ; projets moyens ≈ 250 kh GPU [S2] | partition H100 de Jean Zay seulement [S2] |
| Calendrier | « ouvertes en permanence » [S2] | 2 sessions par an : allocation en mai (dossier avant février) et en novembre (dossier avant septembre) [S6]. Prochaine clôture : **08/02/2027 à 09h00** (allocation A22) [S1] | ouvertes en permanence [S2] |
| Délai | « de quelques jours à 2 semaines environ » [S2] ; « la validation d'un AD prend quelques jours » [S6] | « de 2 à 6 mois », avec une allocation dynamique de transition (≤ 6 mois) en attendant [S2] | 5 semaines [S2] |
| Expertise | « Pas d'expertise » [S6] : jugé par le directeur du centre, avec avis possible du comité thématique [S2] | expertise scientifique et technique [S6] | comité dédié, puis validation interministérielle [S2] |
| Durée | 1 an, renouvelable à partir de 2 mois avant la fin [S2] | 1 an [S4] | 2 à 6 mois, non renouvelable [S2] |
| Limite | 2 AD actifs par porteur [S2] | — | il faut avoir eu un AD ou un AR avant [S2] |

À savoir pour un AD [S2] :

- **Heures attribuées et heures proposées.** Les heures attribuées sont garanties « dans la mesure de la
  consommation régulière sur l'année » : leur priorité peut baisser selon la pression sur les machines. Si
  la demande est déposée en novembre 2026 et que rien n'est consommé avant le printemps, ce point peut
  jouer. Le déposer en janvier ou février 2027, ou ne demander que le nécessaire, réduit ce risque (mon
  interprétation).
- **Pièces du dossier.** Une description PDF (modèle facultatif pour un AD) ; le visa du directeur de
  laboratoire pour un doctorant ou un stagiaire de M2 ; au renouvellement, un rapport d'activité et les
  publications (DOI ou HAL).
- **Contreparties.** Une recherche « donnant lieu à publication », un rapport d'activité en fin
  d'allocation, une phrase de remerciement imposée, et la publication par GENCI du nom et du laboratoire
  du porteur [S1][S2]. Les ressources de calcul et de stockage sont gratuites [S2].
- **Comité thématique** à choisir parmi 11 [S5]. Ceux qui conviennent à MilaDy : CT6 « Informatique,
  algorithmique, mathématiques… » (mots-clés « machine-learning scientifique », « EDP »), CT10
  « Intelligence artificielle… » ou CT4 « Astrophysique et géophysique » (« géophysique interne »). Le
  choix revient aux encadrants.

### 2.2 Qui peut déposer, qui peut utiliser

Règles lues dans [S2] :

| Statut | Déposer un AD ? | Visa du directeur de laboratoire ? | Être utilisateur d'un projet ? |
|---|---|---|---|
| Membre permanent : enseignant, chercheur, ingénieur (CDD ou CDI), post-doctorant | oui | **non** | oui |
| Doctorant, **stagiaire de M2** dans un laboratoire | oui (AD seulement ; pas d'AR) | **obligatoire** | oui |
| Autres étudiants, personne sans affiliation | non | — | **non** (« Les étudiants hors doctorants et Master 2 ne sont pas autorisés ») |

- Le porteur doit appartenir à une structure du Répertoire national des structures de recherche (RNSR) ou
  à une entreprise ayant une activité de R&D en France [S2]. Le CEREA (ENPC / EDF R&D) et le LISN (Université
  Paris-Saclay / CNRS) relèvent a priori du RNSR (**non vérifié** dans le RNSR lui-même).
- Pour un membre d'un laboratoire CNRS (D. Lucor au LISN, d'après `these/index.qmd`), la validation peut
  se faire entièrement en ligne via la Fédération Éducation-Recherche [S2].

### 2.3 Ouvrir un compte de calcul : ce qui prend du temps

- Aucun compte n'est ouvert automatiquement. Chaque utilisateur se rattache au projet dans eDARI, puis
  demande l'ouverture de son compte. **Cette demande est validée par le responsable de recherche et par le
  responsable réseaux et sécurité de sa structure**, quel que soit son statut [S2][S3][S6].
- L'ouverture peut donner lieu à une enquête administrative (protection du potentiel scientifique et
  technique de la Nation, auprès du haut fonctionnaire de défense et de sécurité) [S2]. **Aucun délai
  d'ouverture de compte n'est publié** (non vérifié). Il faut le lancer dès le premier jour du stage, avec
  la convention signée et une adresse électronique de l'établissement.
- **Filtrage des adresses IP.** Les machines de connexion doivent être déclarées. Leurs IP doivent être
  « localisées en France », gérées et dédiées à l'organisme. À défaut d'IP fixe professionnelle, on peut
  passer par « une instance Cloud d'un fournisseur dont le siège social et les infrastructures sont situés
  en France » [S2][S6]. **Conséquence pour MilaDy** : la VM de l'infrastructure, si elle est louée chez un
  fournisseur français (Scaleway ou OVHcloud, voir les autres fichiers), pourrait servir de rebond SSH vers
  Jean Zay et de catalogue central. Son acceptation reste à faire valider par l'IDRIS (non vérifié).
- Les nœuds de calcul de Jean Zay n'ont **aucun accès à Internet** ; les frontales ont un proxy HTTP(S)
  [S6]. Le dépôt en tient compte (§2.6).

### 2.4 Machines utiles (fiches eDARI [S1], IDRIS [S6])

| Machine | Partition GPU | GPU | Intérêt pour MilaDy |
|---|---|---|---|
| Jean Zay (IDRIS) | H100 (`gpu_p6`, « disponible en septembre 2024 ») | 364 nœuds × 4 H100 SXM5 80 Go, 96 cœurs, 512 Go | entraînement, grilles 128³/256³ ; gabarits du dépôt déjà écrits pour elle |
| Jean Zay | A100 (`gpu_p5`) | 52 nœuds × 8 A100 SXM4 80 Go (416 GPU) | possible ; durée maximale de 20 h (README-slurm) |
| Jean Zay | V100 (`gpu_p13`, `gpu_p2`) | 4 × V100 16/32 Go, ou 8 × V100 32 Go | campagnes à 64³ (4 fois moins d'heures normalisées) |
| Dalia (IDRIS-EXT) | GB200 NVL72 | 72 B200 186 Go, processeurs Arm Grace | inutile ici (Arm, très gros modèles) |
| Adastra (CINES) | MI250X, MI300A | AMD | demanderait une image PyTorch ROCm, absente du dépôt |
| Joliot-Curie / Irene (TGCC) | V100 | 32 nœuds × 4 V100 16 Go | possible, peu de GPU |

**Saturation.** Selon Clubic (21 mai 2026), en 2025, « cinq refusés pour chaque projet accepté faute de
capacité », et environ 1 700 projets d'IA ont été soutenus [S7]. Ce chiffre semble concerner les
allocations en général ; son effet sur les petits AD et sur l'attente en file n'est pas documenté
(**non vérifié**). C'est une raison de plus pour demander peu, bien justifié, et de garder la location
payante en solution de secours.

### 2.5 Combien demander (proposition)

Une première AD bien en dessous du seuil, comme le demande GENCI (« Vous ne devez demander que les
ressources dont vous avez réellement besoin » [S2]) :

- **≈ 500 h H100** (2 000 h normalisées) pour l'entraînement (M5, M7, M8), les grilles 128³/256³
  (scénario B) et la mise au point. Avec ≈ 150 h V100 en plus, cela couvre aussi les 49 simulations à 64³
  (M3, M4).
- **≈ 5 000 à 10 000 h CPU** pour M1, les analyses et les tests CPU (ordre de grandeur, à affiner).
- Si les encadrants veulent démarrer le palier 1 de la thèse (≈ 700 h A100, soit ≈ 350–700 h H100) dans la
  même allocation, la porter à ≈ **1 500 h H100**. On reste à ≈ 12 % du seuil.

Au renouvellement (à partir de 2 mois avant la fin), la thèse pourra rester en AD : 2,2 × 10⁴ h normalisées,
c'est moins que 5 × 10⁴. Elle pourra aussi passer en AR pour avoir des heures expertisées et plus
garanties (session de mai : dossier avant février ; session de novembre : dossier avant septembre [S6]).

### 2.6 Ce que le dépôt prépare déjà pour Jean Zay (`infra/slurm/README-slurm.md`, lu le 2026-11-08)

Déjà prêt :

- **Gabarits.**
  - `gen_data.sbatch` : tableau de jobs, une simulation par GPU, `--signal=TERM@120` pour écrire un point
    de contrôle avant la limite de temps, reprise en resoumettant les mêmes indices.
  - `train.sbatch` : `torchrun` par nœud, plusieurs nœuds possibles.
  - `eval.sbatch`.
  - `env.sh` : charge `module load singularity` si besoin et prend l'image dans `$SINGULARITY_ALLOWED_DIR`.
  - `apptainer.def`.
- **Notes Jean Zay vérifiées le 2026-11-07 dans la documentation IDRIS.**
  - Comptes `--account=<projet>@h100|a100|v100|cpu`.
  - Contraintes `-C h100` et `-C a100`, QoS `-t3` (≤ 20 h), `-t4` (≤ 100 h) et `-dev` (≤ 2 h), durée par
    défaut de 10 min.
  - Espaces `$WORK`, `$SCRATCH` (purgé après 30 jours) et `$STORE`.
  - Singularity seulement : construction impossible sur place, copie par `idrcontmgr cp`, 20 conteneurs au
    plus.
- **Pas d'Internet sur les nœuds de calcul.** Catalogue SQLite et MLflow SQLite sur `$WORK`, enregistrement
  a posteriori par `milady.catalog ingest`, rapatriement vers S3 et PostgreSQL depuis la frontale
  (README-slurm §5).
- **Le README le dit déjà :** « Les heures GPU s'obtiennent par une demande DARI (accès dynamique ou
  régulier) ; un stage passe normalement par le projet de l'équipe d'accueil. »

Ce qui manque :

1. Un projet GENCI et un compte. Les gabarits utilisent `abc@h100` comme exemple, à remplacer par le vrai
   projet (`$IDRPROJ`).
2. L'image : README-slurm §3 dit qu'elle n'est **pas encore publiée** sur `ghcr.io/knoel99/milady:gpu`. Il
   faut la construire ailleurs (`make image-gpu && make sif`, Docker et Apptainer nécessaires), la copier
   avec `scp` puis `idrcontmgr cp`.
3. Un premier essai. Le chemin GPU n'a jamais été exécuté (`dimensionnement.md` §6). Sur Jean Zay, il faut
   commencer par un job en QoS `-dev` (≤ 2 h).
4. Un petit environnement Python ≥ 3.11 sur la frontale pour `milady.sweep --scheduler slurm`, via un
   module du centre (README-slurm §1).
5. Relire la documentation IDRIS avant la campagne. Le site de l'IDRIS a changé : plusieurs anciennes pages
   `idris.fr/info/gestion/…` renvoient 404 le 2026-11-08, alors que `idris.fr/docs/jean-zay/…` répond [S6].

## 3. Mésocentres régionaux

| Mésocentre | Matériel GPU | Qui y a accès | État | Verdict |
|---|---|---|---|---|
| **Ruche, mésocentre Paris-Saclay** [S13] | 10 nœuds × 4 V100 32 Go ; 9 nœuds × 4 A100 40 Go ; 4 nœuds × 2 P100 [S13 hardware] | chercheurs des laboratoires du périmètre Paris-Saclay ayant un référent. **Le LISN a un référent** (F. Popineau) [S13 lab_referent]. Un projet ne peut être créé que par un **membre permanent**. Un compte pour un étudiant de M2 suppose qu'un chercheur se porte garant et qu'une réunion ait lieu avec 2 membres du support [S13 getting_started] | comité de pilotage du 18 nov. 2025 : « Fin de vie de Ruche », nouvelle machine de 2,5 M€ (achat visé avant l'été 2026), arrêt de la facturation aux externes proposé [S14]. État en novembre 2026 **non vérifié** | **plan B** par D. Lucor. Les projets sont facturés (« financing through project invoicing » [S13 lab_referent]) ; un tarif interne de ≈ 1,50 € HT l'heure cœur GPU est cité par un résultat de recherche, mais la délibération source était inaccessible : **non vérifié** [S15] |
| **Lab-IA** (Saclay-IA, géré par le LISN, hébergé à l'IDRIS) [S16][S17] | 12 nœuds, 33 GPU (A6000, V100) [S16] | laboratoires LTCI, LISN, L2S, SAMOVAR, SATIE et MaIAGE [S16]. Procédure d'accès non publiée | chiffres tirés du dossier HCERES 2024, non datés [S16] | **possible via D. Lucor**, à lui demander (non vérifié) |
| **meso@IP-Paris / IDCS (Cholesky)** [S18] | 4 nœuds GPU (V100, A100), d'après une présentation de 2023 citée par un résultat de recherche (non vérifié) | destiné au CMAP, au CMLS, à l'UMA, au CPHT, au LPP et au LMS. **Le CEREA n'est pas cité**, bien que l'ENPC soit membre de l'IP Paris depuis le 16 juillet 2024 [S19] | la page dit que le cluster est « actually down », avec une préproduction visée « by the end of March 2026 », et invite à demander un AD GENCI [S18] | **non pertinent** pour l'instant |
| **ENPC / CEREA** | rien de public trouvé | — | — | **non vérifié** : demander à S. Cheng si le CEREA ou l'ENPC ont des GPU, et si EDF R&D (cotutelle du CEREA) en ouvre aux stagiaires |

## 4. EuroHPC (niveau européen)

- **Development Access** [S8][S9] : pour développer et optimiser du code, y compris des méthodes d'IA.
  - Calendrier : appel ouvert en permanence, clôture le 1ᵉʳ de chaque mois (prochaine : 1ᵉʳ décembre 2026),
    évaluation dans les 2 semaines, accès 2 à 3 semaines après la clôture [S9].
  - Volume : « a small number of node hours », pour un an [S9]. Le volume par machine figure dans une image
    de l'annexe (**non lu**).
  - Machines : JUPITER, LUMI, Leonardo, MareNostrum 5, MeluXina, Vega, Deucalion, Discoverer, Arrhenius
    [S9].
  - Éligibilité : chercheurs d'organismes établis dans l'UE ou un pays associé ; le porteur doit avoir
    **un contrat valable au moins 3 mois après la fin de l'allocation** [S9]. Exclu pour un stagiaire,
    possible pour un encadrant permanent. Attribution au premier arrivé, selon un quota mensuel [S9].
- **AI for Science and Collaborative EU Projects** [S10] : allocation de 6 mois, évaluation par les pairs,
  accès au plus tard un mois après la clôture. Prochaines clôtures : **11 décembre 2026**, puis
  31 décembre 2033 comme date finale. Machines : LUMI, Leonardo, MareNostrum 5 et MeluXina [S10].
- **AI Factories (Playground, Fast Lane, Large Scale)** : gratuites pour les PME et start-up d'IA ; le volet
  science passe par l'appel ci-dessus [S11]. AI Factory France fédère Jean Zay, Adastra, Joliot-Curie et
  la future Alice Recoque [S12].
- **Verdict.** Pour MilaDy, EuroHPC fait double emploi avec un AD GENCI : il est plus lent, demande un
  dossier en anglais, et LUMI ou JUPITER imposent d'autres architectures (AMD, ou Arm avec GH200,
  **non vérifié** dans les pages lues). Utile seulement si GENCI refuse.

## 5. Crédits cloud et offres gratuites

| Programme | Pour qui | Montant | Délai | Pour vous maintenant ? | Pour les encadrants ? |
|---|---|---|---|---|---|
| **AWS Cloud Credit for Research** [S20] | enseignants et personnels de recherche à temps plein ; « graduate, post-graduate, or PhD students » d'un établissement accrédité | étudiants : jusqu'à 5 000 $ ; personnels : sans plafond | instruction au fil de l'eau en **90 à 120 jours**, sans procédure accélérée | non (pas d'affiliation ; un M2 compterait-il comme « graduate student » ? **non vérifié**) | oui, mais trop lent pour un démarrage au printemps 2027 si la demande part après décembre 2026. Crédits valables sur EC2 à la demande et spot |
| **Google Cloud research credits** [S21] | « faculty, PhD students and postdoctoral researchers » ; la France est dans la liste des pays | 5 000 $ annoncés sur la page programme ; le formulaire ne donne pas de montant | non publié ; crédits valables 365 jours après activation | **non** (les étudiants de M2 ne sont pas éligibles) | oui ; il faut un compte de facturation Google Cloud |
| **Azure for Students** [S22] | « full-time university students », sans carte bancaire | 100 $ sur 12 mois | immédiat | seulement si vous êtes étudiant à temps plein. Les GPU ne sont pas mentionnés ; quota GPU **non vérifié** (probablement nul) | — |
| **Crédits de recherche Microsoft Azure** | aucun programme officiel 2026 trouvé | — | — | — | **non vérifié** |
| **NVIDIA Academic Grant Program** [S23] | « full-time faculty member » d'un établissement délivrant des doctorats | jusqu'à 30 000 h H100 80 Go (appel « Simulation and Modeling », qui inclut l'apprentissage automatique informé par la physique) | aucune date ; la page dit « currently not accepting new applications » | non | à surveiller pour la thèse ; utiliser des logiciels ou modèles NVIDIA est exigé |
| **OVHcloud Startup Program** [S24] | start-up et scale-up | 10 000 € (Start), jusqu'à 100 000 € (Scale) | — | non | non (rien pour la recherche publique) |
| **Scaleway Startup Program** [S25] | start-up constituées dans l'UE, selon des agrégateurs (page officielle : erreur 403) | Founders : ≈ 1 000 € (agrégateur) | — | non (**non vérifié**) | non |
| **Kaggle Notebooks** [S26] | tout compte vérifié par téléphone | ≈ 30 h GPU par semaine (T4 ou P100), séances de 9 à 12 h selon les sources | immédiat | **en dépannage seulement** : assez pour les calculs à 64³ (≈ 1–5 h GPU), mais sans la pile Docker (PostgreSQL, MinIO, MLflow) ; mode SQLite et `file://` seulement ; quotas **non vérifiés** à la source officielle | — |

## 6. Ce qui est réaliste, et quand

| Quand | Qui | Quoi | Délai annoncé |
|---|---|---|---|
| **Maintenant (nov.–déc. 2026)** | vous | Aucune voie académique en propre. Location payante (voir les autres fichiers), ou Kaggle pour un pilote à 64³ (non vérifié) | — |
| **Maintenant** | vous → encadrants | Leur demander : (a) ont-ils déjà un projet GENCI sur Jean Zay où vous ajouter (c'est le plus simple) ? (b) sinon, qui dépose un AD, et quand ? (c) le CEREA ou l'ENPC ont-ils des GPU, et le LISN a-t-il accès à Lab-IA ou à Ruche ? (d) d'où vous connecterez-vous (IP du laboratoire ou VM chez un fournisseur français) ? | — |
| **Janv.–févr. 2027** (ou dès maintenant pour que les encadrants testent les gabarits) | S. Cheng ou D. Lucor | Déposer l'AD sur eDARI (§2.5) : V100 et H100 sur Jean Zay plus des heures CPU ; comité CT6 ou CT10 | quelques jours à ≈ 2 semaines [S2][S6] |
| **Avant le stage** | encadrant ou vous | Construire `milady.sif` (`make image-gpu && make sif`) sur une machine avec Docker, ou publier l'image sur GHCR | ≈ 1 journée (estimation) |
| **Premier jour du stage (printemps 2027)** | vous, avec la convention et une adresse de l'établissement | eDARI : rattachement au projet, demande de compte Jean Zay (IP déclarées), validations du responsable de recherche et du responsable sécurité | non publié (**non vérifié**) ; enquête administrative possible [S2] |
| **Pendant le stage** | vous | QoS `-dev`, puis banc d'essai, M3/M4 en tableau de jobs, M5–M8, rapatriement (README-slurm §5). Vous pouvez déposer votre propre AD (2 au plus par porteur) avec le visa du directeur | — |
| **2 mois avant la fin de l'AD** | porteur | Renouveler l'AD pour la thèse, ou déposer un AR (clôture du 08/02/2027 pour l'allocation A22 [S1] ; sessions de mai et de novembre [S6]) | AR : 2 à 6 mois, avec une allocation de transition [S2] |
| **En parallèle (facultatif)** | encadrants | EuroHPC Development (clôture le 1ᵉʳ du mois) ; NVIDIA AGP à sa réouverture | 2 à 5 semaines [S9] |

## 7. Recommandation pour cette partie

- **Pour les calculs du stage :** demander aux encadrants un **AD GENCI sur Jean Zay** (≈ 500–1 500 h H100,
  un peu de V100 et quelques milliers d'heures CPU). C'est gratuit, rapide, et les gabarits sont déjà
  écrits. Le dépôt doit être fait par un encadrant permanent (sans visa) ou par vous une fois stagiaire de
  M2 (avec le visa du directeur).
- **Pour obtenir des résultats avant le stage** (vidéo, pages du site) : aucune voie académique n'est
  possible sans affiliation. Il faut une location courte et payante, où quelques heures de GPU suffisent
  (voir `RECOMMANDATION-CLOUD.md`), ou un pilote gratuit sur Kaggle (non vérifié). Les
  résultats obtenus dans le cloud restent compatibles avec Jean Zay : même image, et le catalogue garde les
  mêmes identifiants grâce à `milady.catalog ingest` (README-slurm §5).
- **Ne pas compter sur :** les crédits AWS (90 à 120 jours), Google ou NVIDIA (réservés aux
  enseignants-chercheurs, doctorants et post-doctorants), les programmes pour start-up d'OVHcloud ou de
  Scaleway, ni sur Ruche ou Cholesky (en fin de vie ou en panne).

## 8. Points non vérifiés

- Délai d'ouverture d'un compte Jean Zay après rattachement (non publié) ; attente en file pour un petit AD
  en 2026–2027.
- Statut exact de S. Cheng (permanent ou non), et existence d'un projet GENCI chez S. Cheng ou D. Lucor.
- GPU propres à l'ENPC, au CEREA ou à EDF R&D accessibles à un stagiaire.
- Ruche : état en novembre 2026, nouvelle machine, tarifs (délibération de CentraleSupélec du 11/12/2024
  inaccessible : erreur 503 / connexion réinitialisée le 2026-11-08). Lab-IA : procédure d'accès.
- EuroHPC : heures-nœuds par machine (annexe en image) ; statut des étudiants comme simples utilisateurs.
- Quotas Kaggle et Colab ; quota GPU d'Azure for Students ; programme Scaleway (page officielle : 403) ;
  programme de crédits de recherche Azure en 2026.
- Équivalence de vitesse V100 / H100 à 64³ (estimation de `dimensionnement.md`, non mesurée).

## 9. Sources (toutes consultées le 2026-11-08 sauf mention contraire)

- [S1] eDARI, page d'accueil (seuil AD/AR, équivalences GPU, clôture AR du 08/02/2027, fiches machines Jean Zay H100/A100, Dalia, Adastra, Irene) : https://www.edari.fr/ (copie : `raw/acad/edari_home.html`)
- [S2] eDARI, « Documentation complète » (éligibilité, statuts, AD/AR/AS, délais, accès aux calculateurs, filtrage IP, enquête administrative) : https://www.edari.fr/documentation/index.php/Documentation_compl%C3%A8te (copie : `raw/acad/edoc_Documentation_compl_C3_A8te_.txt`)
- [S3] eDARI, FAQ (étapes, visa, délai « de quelques jours (dans le meilleur des cas) à quelques semaines ») : https://www.edari.fr/documentation/index.php/F.A.Q.
- [S4] eDARI, « Intelligence artificielle » (AD/AR pour l'IA, AI Factory France) : https://www.edari.fr/documentation/index.php/Intelligence_artificielle
- [S5] eDARI, liste des 11 comités thématiques : https://www.edari.fr/comite/liste
- [S6] IDRIS, « Nouvel utilisateur » (partitions p13/p2/p5/p6, AD/AR, 12,5k h H100 = 50k h normalisées, ouverture de compte, filtrage IP, proxy des frontales) : http://www.idris.fr/docs/jean-zay/nouvel-utilisateur
- [S7] Clubic, « Un an plus tard, Jean Zay est le supercalculateur IA le plus utilisé d'Europe, mais déjà saturé », 21 mai 2026 : https://www.clubic.com/dossier-613582-un-an-plus-tard-jean-zay-est-le-supercalculateur-ia-le-plus-utilise-d-europe-mais-deja-sature.html
- [S8] EuroHPC, appels d'accès : https://eurohpc-ju.europa.eu/access-our-supercomputers/eurohpc-access-calls_en
- [S9] EuroHPC, Development Access (page et PDF « Information for Applicants & Awarded projects ») : https://eurohpc-ju.europa.eu/eurohpc-ju-call-proposals-development-access_en ; https://eurohpc-ju.europa.eu/document/download/8c7d1d34-d6a3-46dd-b552-d81ccbcbfcdb_en?filename=Development%20Call%20-%20Information%20for%20Applicants%20%26%20Awarded%20projects.pdf
- [S10] EuroHPC, AI for Science and Collaborative EU Projects : https://eurohpc-ju.europa.eu/eurohpc-ju-call-proposals-ai-science-and-collaborative-eu-projects_en
- [S11] EuroHPC, AI Factories Access Modes : https://eurohpc-ju.europa.eu/ai-factories/ai-factories-access-modes_en
- [S12] AI Factory France : https://aifactory-france.eu/
- [S13] Mésocentre Paris-Saclay : https://mesocentre.universite-paris-saclay.fr/ ; matériel : https://mesocentre.universite-paris-saclay.fr/ruche/hardware.html ; comptes et projets : https://mesocentre.universite-paris-saclay.fr/ruche/getting_started.html ; référents : https://mesocentre.universite-paris-saclay.fr/ruche/lab_referent.html
- [S14] Comité de pilotage du mésocentre Paris-Saclay, 18 novembre 2025 (diapositives) : https://indico.ijclab.in2p3.fr/event/12394/attachments/26641/39520/slides20251118.pdf
- [S15] Délibération du conseil d'administration de CentraleSupélec, 11/12/2024 (tarifs du mésocentre) : https://research-new.centralesupelec.fr/sites/default/files/deliberation_-ca_11122024.pdf — **inaccessible le 2026-11-08 ; contenu non vérifié**
- [S16] LISN, portfolio HCERES 2024, Lab-IA : https://perso.lisn.upsaclay.fr/mbl/HCERES2024/portfolio/portfolio%20LISN/Element3/LabIA.html
- [S17] Université Paris-Saclay, plateforme Saclay-IA : https://www.universite-paris-saclay.fr/plateforme-saclay-ia
- [S18] IDCS (meso@IP-Paris), documentation de Cholesky : https://docs.idcs.mesocentre.ip-paris.fr/
- [S19] IP Paris, « New statutes… and integration of École nationale des ponts et chaussées », 16 juillet 2024 : https://www.ip-paris.fr/en/news/new-statutes-ip-paris-and-integration-ecole-nationale-des-ponts-et-chaussees
- [S20] AWS Cloud Credit for Research : https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/
- [S21] Google Cloud for Researchers : https://cloud.google.com/edu/researchers ; formulaire et conditions : https://edu.google.com/programs/credits/research/
- [S22] Azure for Students : https://azure.microsoft.com/en-us/free/students
- [S23] NVIDIA Academic Grant Program : https://www.nvidia.com/en-us/industries/higher-education-research/academic-grant-program/
- [S24] OVHcloud Startup Program : https://startup.ovhcloud.com/en/
- [S25] Scaleway Startup Program : https://www.scaleway.com/en/startup-program/ (403 le 2026-11-08) ; agrégateur (non officiel) : https://betterstack.com/community/comparisons/scaleway-vs-ovhcloud-startups/ — **non vérifié**
- [S26] Kaggle (quotas GPU), source tierce : https://gpuperhour.com/blog/free-cloud-gpus-and-credits ; page officielle https://www.kaggle.com/docs/notebooks non lisible sans JavaScript — **non vérifié**
- Dépôt (lu, non modifié) : `infra/slurm/README-slurm.md`, `infra/slurm/env.sh`, `gen_data.sbatch`, `train.sbatch`, `these/index.qmd` (l. 955–973), `index.qmd` (l. 72 : stage de 5 à 6 mois à partir du printemps 2027) ; dimensionnement : `dimensionnement.md`.
