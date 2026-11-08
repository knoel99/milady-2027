# Plan chapitré

Phase 1. Pas un script : chaque scène a une idée, des repères nommés, un statut, une pastille, des sources. Les phrases dites seront écrites seulement après les deux relectures de `REVUES.md`.

Titre : **How Often Does the Field Flip?**
Sous-titre à l’écran : *Physics-constrained generative models for turbulent dynamos — a learner’s map of the MilaDy project.*

Deux montages, mêmes scènes, visuels anglais :

| Montage | Contenu | Durée cible |
|---|---|---|
| Cœur `film_core_en`, `film_core_fr` | `g00`–`g15` | 41:00 |
| Étendu `film_extended_en`, `film_extended_fr` | cœur + `x03`, `x01`, `x02`, `x04`, `x05` insérés aux coutures | 60:00 |

Mots effectifs visés, 125 à 130 par minute, pauses incluses dans la durée : cœur 5 125 à 5 330 mots ; étendu 7 500 à 7 800. Ce sont des budgets pour les rédacteurs, pas un texte.

Le cœur se suffit. À chaque couture, la scène suivante du cœur ne dépend pas du module retiré.

## Horloge du cœur

| Id | Titre | Niveau | Durée | Horloge cœur | Mots cibles |
|---|---|---|---|---|---|
| g00 | The needle | L0 | 0:50 | 0:00–0:50 | 104–108 |
| g01 | How often | L0 | 2:10 | 0:50–3:00 | 271–282 |
| g02 | Stretch against smear | L1 | 3:20 | 3:00–6:20 | 417–433 |
| g03 | Three rooms of sodium | L1–L2 | 3:10 | 6:20–9:30 | 396–412 |
| g04 | A century of dynamo hunting | L1–L2 | 2:30 | 9:30–12:00 | 313–325 |
| g05 | The MilaDy question | L2 | 2:20 | 12:00–14:20 | 292–303 |
| g06 | Hold these pictures | L2 | 0:35 | 14:20–14:55 | 73–76 |
| g07 | Three numbers that flip | L2–L3 | 3:30 | 14:55–18:25 | 438–455 |
| g08 | A law without a clock | L3 | 2:50 | 18:25–21:15 | 354–369 |
| g09 | Drawing a field from noise | L3 | 2:40 | 21:15–23:55 | 333–347 |
| g10 | Where the constraint is true | L3–L4 | 4:00 | 23:55–27:55 | 500–520 |
| g11 | The honest table | L3–L4 | 3:40 | 27:55–31:35 | 458–477 |
| g12 | The map of the field | L4–L5 | 4:00 | 31:35–35:35 | 500–520 |
| g13 | The ladder, as bets | L4 | 2:10 | 35:35–37:45 | 271–282 |
| g14 | Before we compute | L4–L5 | 2:20 | 37:45–40:05 | 292–303 |
| g15 | The needle, again | L0 | 0:55 | 40:05–41:00 | 115–119 |
| | | | **41:00** | | |

## Horloge de l’étendu

Les modules ajoutent 19:00. Ils ne déplacent pas le sens du cœur ; ils déplacent l’horloge.

| Ordre | Id | Début étendu | Fin |
|---|---|---|---|
| 1–9 | g00 … g08 | 0:00 | 21:15 |
| 10 | x03 Limits of a snapshot | 21:15 | 24:15 |
| 11–12 | g09, g10 | 24:15 | 30:55 |
| 13 | x01 The proof room | 30:55 | 35:55 |
| 14 | g11 | 35:55 | 39:35 |
| 15 | x02 ABC up close | 39:35 | 43:05 |
| 16 | g12 | 43:05 | 47:05 |
| 17 | g13 | 47:05 | 49:15 |
| 18 | x04 Walls, iron, meshes | 49:15 | 53:15 |
| 19 | g14 | 53:15 | 55:35 |
| 20 | x05 The bill and the plan | 55:35 | 59:05 |
| 21 | g15 | 59:05 | 60:00 |

Coutures : `g08` se ferme sans annoncer x03 ; `g10` énonce les propositions sans les démontrer ; `g11` donne les trois seuils sans la fenêtre oscillante ; `g13` nomme parois et budget en une idée chacun ; `g14` classe les questions sans le tableau d’euros. Retirer x01–x05 laisse un film complet.

## Statuts

| Statut | Sens |
|---|---|
| ready | les entrées sont dans le commit épinglé |
| ready-caveat | ready, mais un piège de `INCERTITUDES.md` est obligatoire à l’écran |
| waiting | pari de `MANQUES.md`, deux issues plus tard, aucune courbe fictive |
| blocked-source | le brief le demande, le dépôt n’a pas la source ; pas de nombre |

Chaque chapitre se termine par la carte de `QUESTIONS.md` (6 à 10 s, dans la durée). Repères : `cue.<scene>.start|predict|show|formula|caveat|card`. Les pauses predict durent 2 à 3 s.

## g00 — The needle (L0, 0:50, ready)

Accroche. À environ 7 s de **cette** scène, l’aiguille bascule vers le sud. Légende fixe : « illustration, not to time scale ». Ce n’est pas un temps géologique et pas un temps VKS.

| Scène | Durée | Pastille | Statut | Idée | Repères |
|---|---|---|---|---|---|
| g00.needle | 0:35 | CONTEXT | ready | Une aiguille peut pointer au sud. On ne dit pas quand, à l’échelle près. | `cue.g00.needle.start`, `cue.g00.needle.show` |
| g00.title | 0:15 | — | ready | Titre et sous-titre. | `cue.g00.title.show` |

Pas de carte question : la question du film est le titre, payée par `g01.card`.

## g01 — How often (L0, 2:10, ready + blocked-source)

But : la question du titre est une fréquence, et nous n’avons pas encore le droit d’afficher un taux terrestre.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g01.earth | 0:40 | CONTEXT | blocked-source | Le champ terrestre change de sens. Sans date tant que `INCERTITUDES.md` §E est ouvert. Boussole reprise, toujours hors échelle. | le rapport dit seulement que la dynamo explique le champ terrestre : `en/rapport/index.qmd:86` |
| g01.stripes | 0:25 | CONTEXT | blocked-source | Les fonds océaniques comme archive, **si** une source est épinglée avant le script ; sinon la scène est coupée et sa durée revient à `g01.rate`. | §E |
| g01.rate | 0:40 | CONTEXT | ready-caveat | « How often » sera, dans ce film, une fréquence tirée d’une loi, pas une date. Le 170 kyr ne s’affiche pas comme fait géologique. | `dynamo.md:285-287` |
| g01.card | 0:25 | PLANNED | ready | Carte question `q.g01`. | `QUESTIONS.md` |

Predict : `cue.g01.rate.predict` avant de montrer que le film refuse un nombre non sourcé.

## g02 — Stretch against smear (L1, 3:20)

But : Rm est un rapport, un seuil existe, une dynamo de disque n’est pas encore chiffrée.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g02.stretch | 0:45 | CONTEXT | ready | Le mouvement étire le champ ; la diffusion l’efface. Image d’abord. | `en/rapport/index.qmd:86` |
| g02.ratio | 0:50 | PROVED | ready | Rm = UL/η. Formule au calque, non lue. Predict avant la formule. | `en/rapport/index.qmd:137` |
| g02.threshold | 0:40 | CONTEXT | ready | Sous le seuil le champ meurt, au-dessus il peut croître. Pas encore de courbe ABC. | `en/rapport/index.qmd:137` |
| g02.sodium | 0:30 | CONTEXT | ready | Le sodium a un Pm très petit : 0,82×10⁻⁵ à 120 °C. Le fluide est turbulent bien avant la dynamo. | `dynamo.md:35`, `en/rapport/index.qmd:137` |
| g02.disk | 0:15 | CONTEXT | blocked-source | Dynamo à disque : couper si §E reste ouvert. Ne pas inventer de Rm critique. | §E |
| g02.card | 0:20 | PLANNED | ready | `q.g02`. | |

`cue.g02.ratio.formula` allume U, L, puis η.

## g03 — Three rooms of sodium (L1–L2, 3:10)

But : Riga, Karlsruhe, VKS, et DRESDYN comme expérience en cours. Une définition de Rm par plan.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g03.riga | 0:40 | CONTEXT | ready-caveat | Novembre 1999, 2150 tr/min, 205 °C, p₂ = 0,0315 ± 0,0009 s⁻¹, f₂ = 1,326 Hz. Moteurs : citer 2×55 kW du PRL, pas les autres chiffres dans le même plan. | `dynamo.md:51-62`, réserve `dynamo.md:81` |
| g03.karlsruhe | 0:30 | CONTEXT | ready | Décembre 1999, 52 générateurs, dipôle stationnaire, deux états. | `dynamo.md:94-98`, `dynamo.md:106` |
| g03.vks | 0:55 | CONTEXT | ready-caveat | Fer doux contre inox. Rm_c ≈ 31 **avec** K ≈ 0,6. Renversements : 16 Hz et 22 Hz, 120 s et 50 s, un renversement ~5 s, diffusion ohmique ~0,4 s. La figure du site reste marquée schematic. | `dynamo.md:124-149`, `en/rapport/index.qmd:149`, `en/rapport/index.qmd:163` |
| g03.defs | 0:25 | CONTEXT | ready-caveat | 31, 44 et 52–71 ne sont pas le même Rm. Trois étiquettes, pas un graphique commun. | `dynamo.md:616-618` |
| g03.dresdyn | 0:20 | CONTEXT | ready | Cylindre en précession, HZDR, objectif (ii). Pas de fenêtre chiffrée. | `en/encadrants/index.qmd:78`, `en/these/index.qmd:943` |
| g03.card | 0:20 | PLANNED | ready | `q.g03`. | |

## g04 — A century of dynamo hunting (L1–L2, 2:30)

Unité d’état de l’art demandée, après les expériences de laboratoire. Elle situe le stage : la question de fréquence a déjà une théorie, des salles de sodium, des simulations, des modèles réduits. Elle ne prétend pas couvrir le siècle entier.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g04.cowling | 0:25 | CONTEXT | ready | Un champ trop symétrique ne se maintient pas (Cowling 1933, via Tobias). | `dynamo.md:435-437` |
| g04.labs | 0:20 | CONTEXT | ready | Rappel en une bande : Riga, Karlsruhe, VKS, puis DRESDYN encore sans dynamo au sens du résumé ANR. | `en/rapport/index.qmd:139`, `en/encadrants/index.qmd:68` |
| g04.sim | 0:35 | CONTEXT | ready-caveat | Simulations du consortium : Nore et al. 2018, seuil qui passe de 90 ± 5 à 130 ± 10 quand on change la condition aux limites ; LATU 384³. Pas Glatzmaier–Roberts tant que §E est ouvert. | `en/rapport/index.qmd:143`, `dynamo.md:223-225`, `dynamo.md:238` |
| g04.reduced | 0:30 | CONTEXT | ready | Forme normale de Pétrélis & Fauve ; trois modes de Gissinger ; DQVU sur 2000 instantanés, données non publiques. | `en/rapport/index.qmd:151-161` |
| g04.stats | 0:20 | CONTEXT | ready-caveat | Les temps d’attente longs sont poissoniens **dans le modèle** de Gissinger 2012. On ne donne pas le taux terrestre. | `dynamo.md:363`, `en/rapport/index.qmd:159` |
| g04.card | 0:20 | PLANNED | ready | `q.g04`. | |

Si la relecture science épingle Larmor, le champ moyen et Glatzmaier–Roberts, ils prennent la place de `g04.cowling` élargi, sans dépasser 2:30 : on raccourcit `g04.labs`, qui répète g03.

## g05 — The MilaDy question (L2, 2:20)

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g05.project | 0:30 | CONTEXT | ready | ANR-25-CE51-0077, janvier 2026, 48 mois, 560 612 €, deux objectifs. | `en/encadrants/index.qmd:56-62`, `:72-78` |
| g05.offer | 0:35 | CONTEXT | ready | L’offre 2027 demande des champs conditionnés, pas d’abord des trajectoires. Stage prospectif, non endossé. | `en/index.qmd:64-68`, `:45` |
| g05.snapshot | 0:40 | PROVED | ready | Un instantané n’a pas de ∂t. Ce qu’on peut imposer dessus n’est pas la même chose que ce qu’on peut imposer à la loi. Predict avant la distinction. | `en/rapport/index.qmd:319-322` |
| g05.names | 0:15 | CONTEXT | ready | Quatre noms, texte seul, rôles sans opinion : Cheng, Lucor, Nore, Ponty. | `en/index.qmd:72` |
| g05.card | 0:20 | PLANNED | ready | `q.g05`. | |

## g06 — Hold these pictures (L2, 0:35)

Récapitulatif de palier. Trois images déjà vues : aiguille, rapport Rm, deux polarités. Bandeau L0–L2. Carte `q.g06`. Aucune idée neuve. `cue.g06.recap.show`.

## g07 — Three numbers that flip (L2–L3, 3:30)

E1 comme histoire, puis les mesures de symétrie. Le détail de Rice est en g08.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g07.odes | 0:40 | CONTEXT | ready-caveat | Trois équations, μ sur Q. Le papier balaie μ ; E1 balaie Γ. | `dynamo.md:311-317`, `en/rapport/index.qmd:784` |
| g07.setup | 0:30 | MEASURED | ready | μ = 0,119, ν = 0,1, Γ de 0,80 à 1,00, CPU, deux graines. | `digest.md:5`, `en/experiences/index.qmd:43` |
| g07.threshold | 0:35 | MEASURED | ready | Aucun passage jusqu’à 0,86 ; 0,00194 à 0,865. Seuil entre deux valeurs d’entraînement. | `en/rapport/index.qmd:871`, `digest.md:94` |
| g07.inherit | 0:40 | MEASURED | ready | À Γ = 0,86 les données sont à 0,3125 en D>0 ; le modèle A affiche 0,183. Predict avant le nuage. | `en/rapport/index.qmd:859-871` |
| g07.equiv | 0:40 | MEASURED | ready | Augmentation symétrique seulement aux Γ vus ; équivariance au plancher 0,004 partout. Distances 0,0118 / 0,00356 / 0,00257 contre plancher 0,00123. | `en/rapport/index.qmd:873`, `digest.md:12-14` |
| g07.card | 0:25 | PLANNED | ready | `q.g07`. | |

`cue.g07.inherit.predict` : le spectateur choisit si le nuage doit être symétrique avant de voir A.

## g08 — A law without a clock (L3, 2:50)

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g08.stationary | 0:30 | PROVED | ready | Une loi stationnaire n’ordonne pas les instantanés. | `en/rapport/index.qmd:264-278` |
| g08.rice | 0:45 | PROVED | ready | La fréquence des zéros dépend de la loi et de F. Formule au calque, fenêtre h. | `en/rapport/index.qmd:509-517` |
| g08.numbers | 0:55 | MEASURED | ready-caveat | Référence : 4 % et 6 %. Générateur C : 14 % cumulé loin du seuil, 65 % en un point, 42 % près du seuil. Le modèle retarde puis dépasse. | `en/rapport/index.qmd:883` |
| g08.not | 0:20 | PROVED | ready | Ce n’est pas la loi des temps d’attente, et les excursions comptent. Le module x03 développera ; cette phrase suffit au cœur. | `en/rapport/index.qmd:528` |
| g08.card | 0:20 | PLANNED | ready | `q.g08`. | |

`cue.g08.numbers.predict` avant les pourcentages.

## g09 — Drawing a field from noise (L3, 2:40)

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g09.path | 0:40 | PROVED | ready | Un bruit gaussien, des segments vers les données, le champ de vitesse est la moyenne des directions. Jouet, pas une mesure. | `en/rapport/index.qmd:281-294`, figure `en/rapport/index.qmd:605` |
| g09.cond | 0:35 | PROVED | ready | Le même réseau reçoit le paramètre. Ticks pleins et ouverts. | `en/rapport/index.qmd:593` |
| g09.why | 0:40 | PROVED | ready | Chemin linéaire, Heun, parce que la perte de stationnarité doit dériver à travers le flot. Diffusion laissée ouverte par l’offre. | `en/rapport/index.qmd:601` |
| g09.sizes | 0:25 | MEASURED | ready | E1 : MLP 256, 12 000 itérations. E2 : largeur 1024, 6 000 itérations, 50 pas de Heun. | `digest.md:5`, `digest.md:127` |
| g09.card | 0:20 | PLANNED | ready | `q.g09`. | |

## g10 — Where the constraint is true (L3–L4, 4:00)

Hinge pédagogique. Pilote recommandé (`LOTS.md`) : `g10.classes` et `g10.sample`.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g10.classes | 0:45 | PROVED | ready | Quatre classes. C1 et C2 sur chaque champ, C3 et C4 sur la loi. | `en/rapport/index.qmd:308-317` |
| g10.hard | 0:40 | MEASURED | ready | V0 : divergence 0,408. Pénalité : 0,34 et 0,162, énergie magnétique trop haute. Potentiels, projection finale : ~10⁻¹⁷. Flot projeté : ~10⁻⁸. | `digest.md:134-138` |
| g10.sym | 0:30 | PROVED | ready | B → −B est une symétrie de la loi. L’équivariance la tient partout. Les identités de budget ne fixent pas les poids. | `en/rapport/index.qmd:399-417` |
| g10.law | 0:35 | MEASURED | ready-caveat | V5 : distance 0,699 contre 2,52 pour le témoin. Le témoin, mêmes itérations, ne gagne pas. Plancher honnête 0,0304 à l’entraînement. | `digest.md:139-140`, `digest.md:160`, `en/index.qmd:85` |
| g10.sample | 0:40 | MEASURED | ready | Recalage : résidu 8,27×10⁻⁶ et σ/σ_ref = 8,64×10⁻⁴. E1 : distance ×9 (0,0231 contre 0,00257). Predict avant la barre écrasée. | `digest.md:144`, `digest.md:19`, `en/rapport/index.qmd:881` |
| g10.bias | 0:25 | PROVED | ready | Le carré d’une moyenne pénalise la variance. Deux demi-lots. | `en/rapport/index.qmd:662-676` |
| g10.card | 0:25 | PLANNED | ready | `q.g10`. | |

`cue.g10.sample.formula` : le corollaire 6 au calque, une ligne, non lue. `cue.g10.law.caveat` : une graine, interpolation, pas une dynamo.

## g11 — The honest table (L3–L4, 3:40)

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g11.works | 0:45 | MEASURED | ready | Ce qui tient : divergence exacte, équivariance, perte utile sur un bon modèle 2D contre son témoin. | `en/rapport/index.qmd:1145-1157` |
| g11.fails | 0:45 | MEASURED | ready | Ce qui ne tient pas : pénalité molle, inclinaison (ESS/N moyen 0,287, et 0,002 là où c’est creux), projection par échantillon, perte sur C court (une graine diverge). | `digest.md:162`, `en/rapport/index.qmd:1008-1012`, `en/rapport/index.qmd:877` |
| g11.floor | 0:30 | MEASURED | ready | Une métrique sans plancher ne dit rien. Le résidu d’hélicité croisée ne classe pas les modèles. | `en/rapport/index.qmd:1037`, `en/rapport/index.qmd:1141` |
| g11.e3 | 0:50 | MEASURED | ready-caveat | Seuils 8,87, 17,6, 26,8 contre fenêtres 8,9 / 17,5 / au-dessus de 27. À Rm = 17,5 le signe change selon la fenêtre. À Rm = 2, λ = −0,5001 contre −0,5. Pas de générateur. | `e3_abc.json:167-171`, `en/rapport/index.qmd:1112-1118` |
| g11.card | 0:20 | PLANNED | ready | `q.g11`. | |

x02 s’insère après `g11.e3` dans l’étendu seulement. `g11.card` reste la fin du chapitre dans les deux montages : dans l’étendu, x02 a sa propre carte, puis on enchaîne vers g12 sans repasser par g11.card une seconde fois. Découpage de montage : cœur = g11 entier ; étendu = g11 sans rallonge, puis x02, et la carte de g11 reste à la fin de g11 (avant x02). x02 ne remplace pas la carte.

## g12 — The map of the field (L4–L5, 4:00)

Deuxième unité d’état de l’art, après le bilan. Contributions publiées, noms en texte, aucune opinion.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g12.learn | 0:40 | CONTEXT | ready | Turbulence et MHD apprises : Fukami & Taira (3 variables latentes, Re = 100), Bousquet, Nore & Lucor 2025 (autoencodeurs et POD). | `en/rapport/index.qmd:169-171` |
| g12.gen | 0:45 | CONTEXT | ready | Flow matching, FunDiff, PIDM, Leray 3D (PCDM), Genuist : aucune stratégie ne gagne partout. | `en/rapport/index.qmd:177-193` |
| g12.lawlit | 0:35 | CONTEXT | ready | Identités d’invariance, Weak Generative Sampler jusqu’à la dimension 100, inclinaison, résidu faible par échantillon. | `en/rapport/index.qmd:214-221` |
| g12.people | 0:40 | CONTEXT | ready | Cheng : TorchDA, diffusion conditionnelle. Lucor : PINN, symétries d’architecture. Nore : SFEMaNS, VKS. Ponty : Taylor–Green à bas Pm, LATU. Titres seulement. | `en/encadrants/index.qmd:130-212` |
| g12.gaps | 0:40 | CONJECTURE | ready-caveat | Six lacunes, recherche du 2026-11-06, confiance medium sur l’absence. Confiance high : E1–E3 ne les ferment pas en 3D borné. | `en/rapport/index.qmd:238-245`, `en/rapport/index.qmd:228` |
| g12.place | 0:20 | PLANNED | ready | Le stage mesure des mécanismes sur des jouets. La thèse vise le générateur conditionnel et la fréquence de Rice, pas un résultat déjà obtenu. | `en/these/index.qmd:1004-1010` |
| g12.card | 0:20 | PLANNED | ready | `q.g12`. | |

## g13 — The ladder, as bets (L4, 2:10)

Tout est PLANNED ou waiting. Aucun rendu de champ 3D.

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| g13.ladder | 0:30 | PLANNED | ready | Cinq paliers. 0–2 prolongent E1–E3. 4 est le premier abandonné. | `en/these/index.qmd:857`, `:999` |
| g13.bets | 0:50 | CONJECTURE | waiting | Quatre paris en une planche architecte : divergence, flou au seuil, Taylor–Green, perte avec ancrage. Confiances de `MANQUES.md`. Emplacements vides. | `MANQUES.md` |
| g13.cost | 0:25 | PLANNED | ready-caveat | ≈ 1,1×10⁴ h GPU, facteur deux, zéro mesure GPU. Assez pour décider de poser la question, pas pour signer un bon de commande. | `en/these/index.qmd:972-973` |
| g13.card | 0:25 | PLANNED | ready | `q.g13`. | |

## g14 — Before we compute (L4–L5, 2:20)

Classe les questions déjà posées. Ne les reformule pas. Détail : `QUESTIONS.md` § registre.

| Scène | Durée | Pastille | Statut | Idée |
|---|---|---|---|---|
| g14.a | 0:40 | PLANNED | ready | (a) simulations et paramètres : résolution, n_traj, ancrage, convention de forçage. |
| g14.b | 0:40 | PLANNED | ready | (b) cadre : définition de Rm, instantanés contre trajectoires, opérateur de divergence, ce qui compte comme succès. |
| g14.c | 0:35 | PLANNED | ready | (c) logistique : données, GPU de laboratoire, Jean Zay, droit de publier, financement au-delà de 48 mois. |
| g14.card | 0:25 | PLANNED | ready | `q.g14`, la question qui résume : louer ou non. |

Durée 2:20, dans la fourchette 2 à 3 min.

## g15 — The needle, again (L0, 0:55)

| Scène | Durée | Pastille | Statut | Idée |
|---|---|---|---|---|
| g15.needle | 0:30 | CONTEXT | ready | Même aiguille, même légende hors échelle. On sait maintenant ce qu’il faudrait mesurer pour répondre, et qu’on ne l’a pas mesuré en 3D. |
| g15.card | 0:25 | PLANNED | ready | `q.g15` renvoie à la fiche, sans nouvelle science. |

Générique : quatre noms, ANR-25-CE51-0077, phrase « prospective report, not endorsed », adresse du dépôt, liste des sources CONTEXT. Dans la durée de g15 ou en queue de 15 s prise sur g15.needle si la relecture pédagogie juge le générique à part. Ne pas ajouter de logos.

## Modules d’approfondissement (étendu seulement)

### x03 — Limits of a snapshot (L4, 3:00, après g08)

| Scène | Durée | Pastille | Statut | Idée | Sources |
|---|---|---|---|---|---|
| x03.wait | 0:50 | PROVED | ready | La loi ne donne pas les temps d’attente. | `en/these/index.qmd:850` |
| x03.chat | 0:40 | PROVED | ready | Rice compte aussi le brouhaha autour de zéro. Seuils ±a. | `en/rapport/index.qmd:528` |
| x03.singular | 0:40 | PROVED | ready | Mesure physique souvent singulière ; forme faible. | `en/rapport/index.qmd:222`, `:568-571` |
| x03.bridge | 0:30 | MEASURED | ready | Masse du pont \|D\|<0,25 et passages parasites ≤ 2×10⁻⁴. | `en/rapport/index.qmd:883`, figure e1_seuil |
| x03.card | 0:20 | PLANNED | ready | `q.x03`. | |

### x01 — The proof room (L4–L5, 5:00, matière papier, après g10)

Une idée par plan, termes de formule allumés un à un. Silence musical.

| Scène | Durée | Pastille | Idée | Source |
|---|---|---|---|---|
| x01.p1 | 0:40 | PROVED | Prop. 1 : l’image dans S. | `en/rapport/index.qmd:326-333` |
| x01.p4 | 0:50 | PROVED | Prop. 4 : équivariance ⇒ invariance pour tout λ. | `en/rapport/index.qmd:399-409` |
| x01.p5 | 0:40 | PROVED | Prop. 5 : E[Lφ] = 0. | `en/rapport/index.qmd:421-429` |
| x01.c6 | 0:50 | PROVED | Corollaire 6 : KL infini, borne W1. | `en/rapport/index.qmd:447-459` |
| x01.est | 0:40 | PROVED | Biais du carré de la moyenne. | `en/rapport/index.qmd:662-676` |
| x01.p8 | 0:40 | PROVED | Prop. 8 : comptage puis espérance. | `en/rapport/index.qmd:509-525` |
| x01.p9 | 0:50 | PROVED | Prop. 9 : Grönwall puis triangle. | `en/rapport/index.qmd:543-561` |
| x01.card | 0:30 | PLANNED | `q.x01`. | |

Le cœur a déjà dit ce que ces énoncés **font**. x01 montre pourquoi. Aucun renvoi du type « comme on vient de le démontrer » dans g11.

### x02 — ABC up close (L4, 3:30, après g11)

| Scène | Durée | Pastille | Idée | Source |
|---|---|---|---|---|
| x02.flow | 0:30 | CONTEXT | Forme ABC, Rm = 1/η, piège √3. | `dynamo.md:388-412` |
| x02.curve | 0:50 | MEASURED | Toute la table des λ, pas seulement les seuils. | `digest.md:170-195` |
| x02.sign | 0:40 | MEASURED | Rm = 17,5, trois signes. Troisième seuil à ±1. | `en/rapport/index.qmd:1114` |
| x02.beltrami | 0:30 | MEASURED | Test exact λ ≥ −1/Rm, tenu à Rm = 2. | `en/rapport/index.qmd:1116` |
| x02.group | 0:30 | CONTEXT | 24 symétries, mode pair de la première fenêtre (Bouya & Dormy 2013). | `en/rapport/index.qmd:1120` |
| x02.next | 0:30 | PLANNED | Générer ces modes par un potentiel est un pari, pas un résultat. | `en/rapport/index.qmd:1120`, `MANQUES.md` P-blur |
| x02.card | 0:20 | PLANNED | `q.x02`. | |

### x04 — Walls, iron, meshes (L5, 4:00, après g13)

| Scène | Durée | Pastille | Idée | Source |
|---|---|---|---|---|
| x04.gap | 0:30 | CONJECTURE | Aucun générateur trouvé avec parois, saut de μr et vide. Confiance medium, datée. | `en/rapport/index.qmd:242` |
| x04.bc | 0:45 | CONTEXT | 90 ± 5 contre 130 ± 10, Re = 1,5×10³, μr = 50. | `dynamo.md:223-225` |
| x04.iron | 0:40 | CONTEXT | Le fer sélectionne le mode axisymétrique. μr des turbines, ordre 50 à 100 selon l’article. | `dynamo.md:189-196`, `dynamo.md:220` |
| x04.mesh | 0:45 | CONTEXT | SFEMaNS : Fourier azimutal × éléments finis. LATU : boîte périodique et pénalisation. | `en/rapport/index.qmd:145`, `:1183` |
| x04.gauge | 0:40 | PROVED | Deux choix de potentiel en domaine borné ; le raccord extérieur reste à faire. | `en/rapport/index.qmd:337-339` |
| x04.card | 0:20 | PLANNED | `q.x04`. | |

### x05 — The bill and the plan (L5, 3:30, matière architecte, après g14)

| Scène | Durée | Pastille | Idée | Source |
|---|---|---|---|---|
| x05.hours | 0:40 | PLANNED | Tableau des heures par palier, réserve 20 %, facteur deux. | `en/these/index.qmd:966-973` |
| x05.h1 | 0:30 | CONTEXT | L’ancre PCDM est un chiffre d’autrui, pas une mesure du dépôt. | `en/these/index.qmd:959` |
| x05.rent | 0:40 | PLANNED | La location n’est utile qu’après la réponse des encadrants. Pas de panier à l’écran dans cette phase : les prix datent du 2026-11-08 et ne sont pas une décision. | `RECOMMANDATION-CLOUD.md:19-37`, `:831-835` |
| x05.genci | 0:40 | CONTEXT | Accès dynamique, dépôt prêt pour Slurm, demande à faire porter. La date de clôture citée dans la recommandation (8 février 2027, 9 h) reste à confirmer avec les encadrants. | `RECOMMANDATION-CLOUD.md:858-873` |
| x05.tested | 0:30 | MEASURED | Ce qui a tourné sans GPU ; ce qui n’a pas tourné. | `en/calcul/index.qmd:180-190` |
| x05.card | 0:30 | PLANNED | `q.x05`. | |

« MEASURED » sur x05.tested porte sur les tests d’installation du dépôt, pas sur un banc de performance GPU. Ne pas en tirer un débit.

## Montée pédagogique (cœur)

| Après | Le spectateur peut | Il ne peut pas encore |
|---|---|---|
| g01 | poser « how often » sans nombre inventé | définir Rm |
| g02 | dire ce que Rm compare | citer une salle d’expérience |
| g03 | distinguer trois expériences et trois définitions de Rm | placer le stage |
| g04 | voir le siècle **sourcé** autour de ces expériences | écrire une équation de modèle |
| g06 | tenir aiguille, rapport, polarités | |
| g07 | lire une asymétrie contre un plancher | prédire une fréquence |
| g08 | accepter une fréquence sans horloge, avec son erreur | construire le générateur |
| g09 | voir un flot conditionnel | choisir la classe de contrainte |
| g10 | poser la contrainte au bon niveau | juger tout le tableau |
| g11 | dire ce qui a marché, ce qui a échoué, ce qui est un jouet | situer la littérature |
| g12 | placer le stage dans les lacunes datées | signer un calcul |
| g14 | poser les questions dans l’ordre A, B, C | |
| g15 | revenir à l’aiguille sans avoir prétendu répondre en 3D | |

Aucun chapitre du cœur n’utilise un symbole avant le plan qui le motive. Γ apparaît en g07, après les polarités. La formule de Rice apparaît en g08, après la question de fréquence. Le corollaire 6 apparaît en g10, après qu’on a vu une contrainte mal placée comme tentation.

## Fichiers de narration futurs (non écrits)

`video-grok/narration/en/<scene>.md` et `video-grok/narration/fr/<scene>.md`, mêmes identifiants de repères, mêmes identifiants de phrase. Cette phase ne crée pas ces fichiers.
