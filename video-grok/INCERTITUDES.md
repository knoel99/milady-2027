# Incertitudes scientifiques

À traiter comme des contraintes de dessin, pas comme des détails à résoudre en voix off. Commit `4e42429716c093df34ba05b47ada542a13d39c50`.

## U1. Le rapport n’est pas une conclusion du stage

Il est écrit **avant** le stage, sur des bancs CPU, et n’est pas validé par les encadrants (`en/index.qmd:45`). Les propositions sont démontrées dans ce texte ; leur intérêt pour MilaDy est une proposition de l’auteur du site. Pastille PROVED pour l’énoncé mathématique, jamais pour « les encadrants retiennent ceci ».

## U2. Petite échelle, peu de graines, interpolation

- CPU 4 cœurs, sans GPU (`en/experiences/index.qmd:43`).
- E1 : deux graines au lieu de trois (`en/rapport/index.qmd:745`). Un écart de quelques dizaines de pour cent est dans la dispersion ; retenir un facteur ≥ 2 (`en/rapport/index.qmd:901`).
- E2 : une graine. Facteur ≥ 3 probablement réel, sans intervalle (`en/rapport/index.qmd:1175`).
- Les η et Γ de test sont **entre** les valeurs d’entraînement (`en/rapport/index.qmd:743`). Aucune extrapolation n’a été mesurée.
- E1 est en dimension 3 : un succès n’informe pas sur un champ VKS (`en/rapport/index.qmd:901`).
- E2 n’est pas une dynamo (`en/rapport/index.qmd:925`). Pm de 0,35 à 2, contre ~10⁻⁵ pour le sodium (`en/rapport/index.qmd:1179`).
- E3 est linéaire, sans rétroaction de la force de Lorentz (`en/these/index.qmd:1008`).
- Les modèles restent faibles : erreur de spectre E2 de 0,07 à 0,23 en log10 au test, contre 0,002 à 0,011 pour les données (`en/rapport/index.qmd:1039`).
- Perte de stationnarité entraînée sur un intégrateur à 8 pas, évaluée à 50 pas (`en/rapport/index.qmd:683`).
- Plancher Monte-Carlo au test E2 optimiste (`en/rapport/index.qmd:747`).
- Topologie demandée par l’offre : non calculée (`en/rapport/index.qmd:739`).

## U3. Collisions de définitions

| Collision | Conséquence à l’écran |
|---|---|
| Rm VKS : K≈0,6 (≈31 ou ≈35), Miralles (≃44), Nore 2018 sans K (52–71) | trois nombres, trois définitions. Jamais un seul axe (`dynamo.md:616-618`) |
| Volume de sodium 150 l ou ~160 L | donner la source de la phrase, ou ne pas donner le litre (`dynamo.md:619`) |
| Moteurs de Riga 2×55 kW, 2×100 kW, ou jusqu’à 200 kW | une phrase, une source (`dynamo.md:81`) |
| Première tentative de Riga 1986 ou 1987 | ne pas choisir (`dynamo.md:79`) |
| Anneau VKS : diamètre ou rayon | ne pas coter (`dynamo.md:136`) |
| ABC : Rm = 1/η (E3, Bouya & Dormy) contre R_M = √3/η (Alexakis) | le dire avant toute comparaison (`dynamo.md:412`) |
| Fenêtres 8,9 / 17,5 / 27 lues dans Archontis 2003, pas dans Galloway & Frisch (PDF 403) | pastille CONTEXT avec la chaîne de citation (`dynamo.md:706`) |
| Taux de croissance maximal de la première fenêtre ABC | valeur inconnue. E3 mesure 0,00765 à Rm = 12 sur sa grille ; ne pas dire « nous retrouvons le maximum publié » (`dynamo.md:706`, `en/rapport/index.qmd:1112`) |
| Gissinger : le papier balaie μ à Γ = 0,9 ; E1 balaie Γ à μ = 0,119 | le seuil 0,86–0,865 est un résultat d’E1, pas la crise μ_c ≈ 0,11928 (`en/rapport/index.qmd:784`) |
| σ(dE/dt) du digest contre σ/σ_ref du rapport | étiqueter (`digest.md:11`, `en/rapport/index.qmd:838`) |
| Seuils E3 : JSON long contre 8,87 / 17,6 / 26,8 | arrondi du rapport. Le second seuil est à environ 0,1 près de 17,5. Le troisième n’est connu qu’à environ une unité près. Ce n’est pas un intervalle de confiance (`e3_abc.json:167-171`, `en/rapport/index.qmd:1114`) |
| « 65 % » et « 42 % » | 65 % ponctuel loin du récit « au seuil » ; 42 % cumulé près du seuil (`en/rapport/index.qmd:883`) |
| 0,70 contre 2,52 (×3,6) | c’est V5 contre le **témoin**, pas contre V0 (`en/index.qmd:85`, `digest.md:139-140`) |
| eps = 0,05 dans le YAML palier 1 contre 0,04479 et 0,04476 mesurés | ne pas mélanger injection nominale et taux d’Itô (`palier1_mhd2d.yaml:25-26`, `digest.md:127`) |
| `n_traj: 1` dans le YAML contre la question « faut-il 4 » | la configuration **écrite** est 1 (`palier2_tg3d.yaml:45`, `RECOMMANDATION-CLOUD.md:255-258`) |
| Zel’dovich | énoncé de Tobias, original non lu (`dynamo.md:627`) |
| ⟨T⟩ ≈ 170 kyr | paramètre du modèle de Pétrélis et al. 2009, pas un taux géologique (`dynamo.md:285`) |
| Courbes de `vks-en.png` | qualitatives, pas des données VKS (`en/rapport/index.qmd:163`) |
| Scores 4,10 et 3,90 | jugement de l’auteur du site (`en/encadrants/index.qmd:435-437`) |
| « Aucun modèle génératif de dynamo » | recherche du 2026-11-06, absence non prouvable (`en/rapport/index.qmd:228`) |
| Budget 1,1×10⁴ h | hypothèses H1–H5, facteur ≥ 2, zéro mesure GPU MilaDy (`en/these/index.qmd:973`) |
| Prix cloud | lus le 2026-11-08, hors décision (`RECOMMANDATION-CLOUD.md:9-15`) |

## U4. Ce que la perte de stationnarité ne permet pas de dire

- Sur un bon modèle E1 elle réduit les résidus, y compris non imposés, et rétrécit dE/dt d’environ un quart (`en/rapport/index.qmd:875`).
- Sur un modèle biaisé elle échoue (une graine diverge) (`en/rapport/index.qmd:877`).
- En E2 elle améliore budget, spectre et distance au test, et le témoin ne gagne rien (`en/rapport/index.qmd:1031`).
- Elle n’a qu’un nombre fini d’identités : nécessaire, non suffisant (`en/rapport/index.qmd:568-571`).
- L’inclinaison ne crée pas de masse et s’effondre là où le modèle est creux (ESS/N → 0,002) (`en/rapport/index.qmd:1033`).
- Le recalage par échantillon annule presque la variance de la dissipation (`digest.md:144`, σ/σ_ref = 8,64×10⁻⁴). Une distance sur les spectres peut quand même « s’améliorer » (1,1 contre 2,62) : il faut montrer σ/σ_ref en même temps (`en/rapport/index.qmd:1035`).
- La variance mesurée de dE/dt sur E1, σ_ref = 0,37772 (`digest.md:49`), ne prouve pas que cette variable n’a pas d’atome en 0. L’absence de masse en 0 reste l’hypothèse du corollaire 6 (`en/rapport/index.qmd:449`).

Confiance dans le mécanisme (où poser la contrainte) : haute sur les bancs mesurés. Confiance dans le transfert 3D, domaine borné, VKS : faible — c’est l’objet de la thèse, pas un résultat (`en/these/index.qmd:1010`).

## U5. Rice

- Hypothèse de densité continue du couple (D, Ḋ), non garantie parce qu’E1 est déterministe (`en/rapport/index.qmd:528`, `:901`). h = 0,2 (`digest.md:5`).
- Les 4 % et 6 % sur la référence sont le contrôle numérique de la fenêtre, pas une application du théorème sous ses hypothèses (`en/rapport/index.qmd:883`).
- Le comptage et Rice ne sont pas la même chose que « un renversement clair ». Les excursions comptent (`en/rapport/index.qmd:528`).
- La loi des temps d’attente n’est pas dans la loi stationnaire (`en/these/index.qmd:850`).
- Près du seuil, le générateur lisse le saut (proposition 9) : retard d’environ 0,005 à 0,01 en Γ, puis dépassement (`en/rapport/index.qmd:883`).
- Sous le seuil, des passages parasites jusqu’à ~2×10⁻⁴ (`en/rapport/index.qmd:883`).

## U6. Géométrie réelle encore non testée

- Parois, vide contre pseudo-vide, sauts de μr : l’écart 90 ± 5 contre 130 ± 10 est une mesure **de simulation publiée**, pas un résultat du générateur (`en/rapport/index.qmd:143`).
- SFEMaNS contrôle ∇·B faiblement (norme de Sobolev négative). Les données ne sont pas solénoïdales pour n’importe quel opérateur discret (`en/rapport/index.qmd:1185`).
- La symétrie utile quand le forçage est asymétrique est jointe sur (état, paramètre). Elle n’a pas été testée (`en/rapport/index.qmd:1187`).
- Données de renversement non publiques (`en/rapport/index.qmd:161`).
- Jauge de Coulomb en domaine borné : deux choix canoniques (Amrouche & Seloula 2011), plus le raccord au potentiel extérieur (`en/rapport/index.qmd:337-339`). Rien de ceci n’est mesuré dans E1–E3.

## U7. DRESDYN

« Narrow range » en nombre de Poincaré, sans borne numérique dans les pages lues (`en/these/index.qmd:943`). Deux familles de modes. Conditions simplifiées qui sous-estiment Rm_c. Succès expérimental décrit comme incertain dans l’offre de postdoc (`en/encadrants/index.qmd:289`). Palier le plus facilement abandonné.

## E. Faits externes bloqués

Le brief autorise des faits externes **seulement sourcés**. Cette phase n’a pas ouvert de nouvelle source primaire hors dépôt. Tant qu’une fiche `video-grok/sources/` n’aura pas une URL ou un DOI daté, relu, ces sujets restent sans nombre :

| Sujet demandé par le brief | État dans le dépôt | Conséquence |
|---|---|---|
| Bandes magnétiques des fonds océaniques | aucune ligne trouvée | scène possible en QUALITATIF seulement après source, ou coupée |
| Dernier renversement géomagnétique (date, nom) | aucune ligne | ne pas écrire d’âge |
| Dynamo à disque | aucune ligne (Herzenberg est cité seulement pour dire que VKS n’en est pas une, `dynamo.md:135`) | ne pas donner de seuil de disque |
| Larmor, champ moyen comme histoire | non épinglés dans `dynamo.md` | le chapitre « century » ne les date pas |
| Glatzmaier–Roberts | non épinglé | ne pas citer d’année ni de « premier renversement simulé » |
| Statistique géologique des temps d’attente | le 170 kyr est un modèle (`dynamo.md:285`) | ne pas le légender « Earth » |

La relecture science a le droit d’ajouter ces sources. Elle n’a pas le droit d’inventer le chiffre en attendant.

## U8. Confiances résumées pour les pastilles CONJECTURE

| Énoncé | Confiance | Pourquoi |
|---|---|---|
| Imposer une contrainte là où elle est vraie (C1–C4) | haute sur E1–E2 | mesuré, avec les limites U2 |
| Équivariance nécessaire pour la symétrie hors des données | haute sur E1 | facteur large, deux graines, plancher explicite |
| Corollaire 6 (projection par échantillon) | haute sur E1 et E2 | effet d’un ordre de grandeur, ou variance annulée |
| Perte de stationnarité utile en 3D sans ancrage | faible | échec E1 sur modèle biaisé ; ancrage encore désactivé par défaut (`en/calcul/index.qmd:166`) |
| Rice à 20 % sur un champ MHD turbulent | faible | critère de palier 0, non testé hors du jouet |
| Générateur régulier en Rm qui résout le seuil ABC | faible, et partiellement contredit par la prop. 9 | le flou est prédit |
| Divergence nulle 3D par potentiels, si le décodeur est bien celui-là | haute comme conséquence de la prop. 1 ; nulle comme résultat, puisqu’aucun champ 3D n’a été généré | |
| Accès aux données VKS à temps | moyenne à faible | non publiques ; plan de repli au mois 18 (`en/these/index.qmd:939`) |
| 64³ suffisant à Re ≥ 100 | faible | le YAML demande une vérification qui n’existe pas |
