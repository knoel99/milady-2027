# Questions

Brouillon de cartes, pas la fiche finale et pas un script. Chaque carte : une ligne anglaise à l’écran, au plus 18 mots, dite plus tard en une phrase. La fiche française vouvoie les encadrants ; elle sera rédigée après les relectures, avec ces cartes comme registre. Minutage : fin du chapitre, horloge du **cœur**, sauf les modules x.

Classe : A avant de louer ; B cadre scientifique ; C données et logistique.

Le défaut est ce que l’auteur du stage ferait **sans réponse**, pas ce que les encadrants pensent.

## Cartes de chapitre

### q.g01 — horloge 2:35–3:00 — B

- Écran : `Which Earth rate, if any, should we judge against?` (9)
- Pourquoi : le titre promet une fréquence. Un âge géologique non sourcé la falsifierait.
- Débloque : soit une source primaire acceptée pour le dernier renversement et le taux moyen, soit l’interdiction durable d’un nombre terrestre.
- Défaut : aucun nombre terrestre à l’écran (`INCERTITUDES.md` §E).
- À lire : `en/rapport/index.qmd:86`, `specs/sources/dynamo.md:285`.

### q.g02 — 6:00–6:20 — B

- Écran : `Which length and speed define Rm for each flow?` (9)
- Pourquoi : UL/η change de sens avec U et L.
- Débloque : la légende obligatoire de chaque axe Rm.
- Défaut : redonner la définition dans le plan, jamais un Rm nu.
- À lire : `en/rapport/index.qmd:137`.

### q.g03 — 9:10–9:30 — A si des données VKS sont visées, sinon B

- Écran : `Which VKS definition of Rm will we condition on?` (9)
- Pourquoi : 31, 44 et 52–71 ne se comparent pas.
- Débloque : l’axe du futur conditionnement, et l’interdiction de les superposer.
- Défaut : ne pas entraîner sur « Rm » VKS tant que la convention n’est pas écrite.
- À lire : `specs/sources/dynamo.md:616-618`, `en/rapport/index.qmd:141`.

### q.g04 — 11:40–12:00 — A

- Écran : `Which ancestor should the first 3D runs copy?` (8)
- Pourquoi : Taylor–Green, ABC, VKS et DRESDYN ne posent pas la même question.
- Débloque : l’ordre réel des campagnes contre l’ordre du plan de thèse.
- Défaut : paliers 0 à 2 sur des données que le dépôt sait produire ; VKS seulement après accès.
- À lire : `en/these/index.qmd:906-918`, `infra/cloud/RECOMMANDATION-CLOUD.md:28-29`.

### q.g05 — 14:00–14:20 — B

- Écran : `Should the generator draw fields, or trajectories?` (8)
- Pourquoi : l’offre demande des champs ; la piste B seule demande des séries.
- Débloque : flow matching d’instantanés contre un modèle autorégressif.
- Défaut : instantanés, Rice pour le taux moyen, pas les temps d’attente.
- À lire : `en/index.qmd:66`, `en/encadrants/index.qmd:449-453`.

### q.g06 — 14:35–14:55 — B

- Écran : `Which of these pictures is still only a drawing?` (9)
- Pourquoi : le récapitulatif mélange CONTEXT, schéma et promesse.
- Débloque : la liste de ce qui est déjà mesuré (rien en 3D généré).
- Défaut : pastille sur chaque plan, schémas marqués schematic.
- À lire : `en/rapport/index.qmd:163`, `en/rapport/index.qmd:300`.

### q.g07 — 18:00–18:25 — B

- Écran : `Vary Gamma as in E1, or mu as in the paper?` (11)
- Pourquoi : ce n’est pas le même chemin vers la crise.
- Débloque : le protocole du palier 0.
- Défaut : garder le balayage E1 comme banc mesuré, et étiqueter la crise en μ comme un autre plan de coupe.
- À lire : `en/rapport/index.qmd:784`, `specs/sources/dynamo.md:341-351`.

### q.g08 — 20:55–21:15 — B

- Écran : `Do we count reversals, or every zero crossing?` (9)
- Pourquoi : Rice compte les excursions et le brouhaha.
- Débloque : le critère (c) du palier 0 (20 %).
- Défaut : publier des passages par zéro, et le dire.
- À lire : `en/rapport/index.qmd:528`, `en/these/index.qmd:889`.

### q.g09 — 23:35–23:55 — B

- Écran : `Flow matching or diffusion, once the fields are 3D?` (9)
- Pourquoi : l’offre laisse les deux. E1–E2 ont choisi le chemin linéaire pour pouvoir dériver.
- Débloque : `train_fm3d` contre un autre sampler.
- Défaut : flow matching, comme le code du dépôt.
- À lire : `en/rapport/index.qmd:601`, `infra/configs/train_fm3d.yaml:22-26`.

### q.g10 — 27:30–27:55 — A

- Écran : `Must stationarity fine-tuning be anchored first?` (7)
- Pourquoi : en E1, la même perte échoue sur un modèle biaisé.
- Débloque : `stationarity.anchor` et la montée de β, aujourd’hui désactivés.
- Défaut : pas de réglage fin 3D sans ancrage, sans témoin à β = 0, et sans partir d’un modèle déjà bon.
- À lire : `en/rapport/index.qmd:877`, `en/calcul/index.qmd:166`.

### q.g11 — 31:15–31:35 — B

- Écran : `Which gap counts, once the noise floor is drawn?` (10)
- Pourquoi : deux graines et une graine ne portent pas les mêmes écarts.
- Débloque : la phrase « succès » dans le futur tableau 3D.
- Défaut : E1, facteur ≥ 2 ; E2, facteur ≥ 3 ; toujours le plancher. Une seule graine 3D ne suffira pas au critère de trois graines du palier 0.
- À lire : `en/rapport/index.qmd:901`, `en/rapport/index.qmd:1175`, `en/these/index.qmd:861`.

### q.g12 — 35:15–35:35 — B

- Écran : `Which nearby paper would make this redundant?` (7)
- Pourquoi : l’absence datée du 6 novembre 2026 expire.
- Débloque : la veille avant le premier article (mois 10 du plan).
- Défaut : relire Cai 2026, Tauberschmidt 2026, Mun 2026, FunDiff, PCDM, Genuist, Kacmaz, avant toute phrase « à notre connaissance ».
- À lire : `en/rapport/index.qmd:228`, `en/these/index.qmd:998`.

### q.g13 — 37:20–37:45 — A

- Écran : `Drop Re = 200 at 64 cubed, or refine it?` (11)
- Pourquoi : Rm = 400 à Re = 200, Pm = 2, et 64³ n’est pas vérifié.
- Débloque : la grille `palier2_tg3d` et l’étiquette « provisoire ».
- Défaut : un seul pilote spectral avant la grille ; Re ≥ 100 à 64³ reste provisoire ; pas de 256³ sans accord.
- À lire : `infra/configs/palier2_tg3d.yaml:12-14`, `infra/cloud/RECOMMANDATION-CLOUD.md:253-254`.

### q.g14 — 39:40–40:05 — C

- Écran : `Is a lab GPU or Jean Zay already open?` (10)
- Pourquoi : si oui, la location ne sert qu’à un essai.
- Débloque : louer ou ne pas louer.
- Défaut : ne pas louer tant que cette réponse manque. Le film ne montre pas un achat.
- À lire : `infra/cloud/RECOMMANDATION-CLOUD.md:19-27`, `en/rapport/index.qmd:1214`.

### q.g15 — 40:35–41:00 — C

- Écran : `What do we ask before any paid hour?` (8)
- Pourquoi : referme sur la fiche, pas sur une nouvelle physique.
- Débloque : l’ordre du jour de 45 min.
- Défaut : l’ordre A puis B puis C ci-dessous.
- À lire : `QUESTIONS.md` § registre.

## Cartes des modules (étendu)

| Id | Horloge étendue | Écran (≤ 18 mots) | Classe |
|---|---|---|---|
| q.x03 | 23:55–24:15 | `Do we need waiting times, or only the mean rate?` (10) | B |
| q.x01 | 35:25–35:55 | `Which of these proofs must the paper carry?` (8) | B |
| q.x02 | 42:45–43:05 | `Is 32 cubed enough to trust the second threshold?` (10) | B |
| q.x04 | 52:55–53:15 | `Vacuum or pseudo-vacuum for the first SFEMaNS loss?` (9) | A |
| q.x05 | 58:35–59:05 | `Who files the Jean Zay request, and when?` (9) | C |

Défauts : taux moyen seulement ; les preuves du rapport restent la référence, le film ne les remplace pas ; ne pas sur-interpréter 17,6 ; ne pas choisir la condition aux limites à la place de C. Nore ; ne pas déposer l’accès GENCI soi-même.

## Registre pour la réunion de 45 min

Ordre proposé, à transformer en fiche vouvoyée après G0. Chaque ligne existe déjà comme carte ou comme question du rapport.

### A — à trancher avant de louer (15 min)

1. GPU déjà ouvert au CEREA, au LISN, ou projet GENCI existant. Défaut : pas de location. `q.g14`. `RECOMMANDATION-CLOUD.md:25-27`.
2. Résolution Taylor–Green : retirer Re = 200, ou prévoir 128³ / 256³. Défaut : pilote puis étiquette provisoire. `q.g13`. `RECOMMANDATION-CLOUD.md:253-254`.
3. `n_traj` de `palier2_tg3d` est 1 dans le YAML. Faut-il 4. Défaut : ne pas entraîner sur 40 instantanés en les appelant un jeu. `palier2_tg3d.yaml:45`. `RECOMMANDATION-CLOUD.md:255-258`.
4. Ancrage du réglage fin. Défaut : ancrage obligatoire, témoin à β = 0. `q.g10`.
5. Convention de forçage Taylor–Green avant toute comparaison à Rm_c = 30. Défaut : pas de chiffre de seuil TG dans le film tant que la convention n’est pas alignée. `palier2_tg3d.yaml:3-8`. `dynamo.md:581`.
6. Droit de publier campagnes et extraits sur le site et dans le film. Défaut : les paris restent des paris. `RECOMMANDATION-CLOUD.md:34`, `:261`.

### B — cadre (15 min)

1. Définition de Rm pour VKS. `q.g03`.
2. Priorité des paramètres : Rm, μr, asymétrie, ou rapport de précession. Défaut : (Re, Pm) périodique d’abord. `en/rapport/index.qmd:1210`.
3. Champs complets, champs moyens, ou coefficients réduits. Défaut : instantanés complets sur les paliers périodiques, coefficients seulement si les partenaires le demandent. `en/rapport/index.qmd:1211`.
4. Opérateur discret de divergence et de budget pour SFEMaNS. Défaut : ne pas poser la perte sur ces données avant vérification. `en/rapport/index.qmd:1212`.
5. Métriques de topologie jugées utiles. Défaut : ne pas en inventer ; E1–E3 n’en ont pas. `en/rapport/index.qmd:1213`.
6. Passages par zéro ou renversements. `q.g08`.
7. Chemin μ ou Γ. `q.g07`.
8. Ce qu’un écart au-dessus du plancher autorise à dire. `q.g11`.

### C — données et logistique (15 min)

1. Quelles simulations pendant le stage : LATU, SFEMaNS, les deux, sous quelle forme. Défaut : aucune promesse de courbe VKS. `en/rapport/index.qmd:1209`.
2. Demande d’accès au premier trimestre de thèse, décision au mois 18. `en/these/index.qmd:990`.
3. Qui dépose l’accès dynamique GENCI, et depuis quelle IP en France. `RECOMMANDATION-CLOUD.md:884-889`.
4. GPU de laboratoire. `en/rapport/index.qmd:1214`.
5. Financement après la fin nominale de MilaDy (janvier 2026 + 48 mois) si la thèse va jusqu’en 2030. Défaut : le dire comme question, pas comme un trou caché. `en/these/index.qmd:982`, `:1000`.

La fiche finale ajoutera, pour chaque ligne, le minutage du film (cette table), le choix par défaut (cette table) et le vouvoiement. Elle n’ajoutera pas de question absente de ce registre sans repasser par la relecture science.
