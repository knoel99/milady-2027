# Revue science

Le verdict global est BLOQUANT.

Huit points mettraient à l’écran un chiffre faux, une précision trop forte, ou un énoncé plus fort que ses hypothèses. Le reste des contrôles obligatoires tient. Aucun correctif n’est appliqué ici.

Périmètre lu : `INVENTAIRE.md`, `INCERTITUDES.md`, `MANQUES.md`, les cellules Sources et les pastilles de `PLAN.md`, la colonne "À lire" et les défauts de `QUESTIONS.md`, `STYLE.md` §6. Les durées, le style graphique et Fish ne sont pas relus. `video/` n’est pas ouvert.

## Commit gelé

La référence `4e42429716c093df34ba05b47ada542a13d39c50` est un commit. Elle est ancêtre de `b3517f588f39795b92a4e5e0309e6fb5c9e1328a`. Le sujet commence par "Vidéo : état de l'art", daté du 2026-11-08. `git diff --name-only 4e42429716c093df34ba05b47ada542a13d39c50 HEAD -- en experiences rapport specs` est vide. Les sources scientifiques gelées sont donc celles du travail.

| Point | Plan | Affirmation | Source gelée | Verdict |
|---|---|---|---|---|
| C0 | `INVENTAIRE.md:3` | Le commit source existe et porte les fichiers cités. | commit `4e42429716c093df34ba05b47ada542a13d39c50` | OK |

Correction proposée. Aucune. Critère de levée. Rien à lever.

## Tableau des points

| Id | Plan | Affirmation | Source | Verdict |
|---|---|---|---|---|
| S1 | `INVENTAIRE.md:183-209`, `PLAN.md:164` | La table E1 de test suit `digest.md:11-26`. Le digest donne σ absolu. Le rapport, table 1, donne σ/σ_ref. | `experiences/resultats/digest.md:11-26`, `en/rapport/index.qmd:834-853`, `experiences/resultats/e1_gissinger.json` résumé C et E | OK |
| S2 | `PLAN.md:175`, `INVENTAIRE.md:210` | 4 % et 6 % sur la référence. 14 % cumulé pour Γ ≥ 0,89. 65 % en un point, à Γ = 0,905 et 0,91. 42 % près du seuil. Les deux phrases restent séparées. | `en/rapport/index.qmd:883`, `experiences/resultats/digest.md:94-103` | OK |
| S3 | `PLAN.md:201`, `INVENTAIRE.md:209` et `:249` | ×9 vaut 0,0231 / 0,00257. ×3,6 vaut 2,52 / 0,699 contre le témoin. | `digest.md:14`, `:19`, `:139-140`, `en/index.qmd:85` | OK |
| S4 | `INVENTAIRE.md:262`, `PLAN.md:214` | Seuils JSON 8,87069372523019, 17,602540347824316, 26,796269592804332. Affichage 8,87, 17,6, 26,8. | `experiences/resultats/e3_abc.json:167-171`, `digest.md:198`, `en/rapport/index.qmd:1099` | OK |
| S5 | `INVENTAIRE.md:268`, `PLAN.md:214` | À Rm = 17,5 le signe change selon la fenêtre. λ = +2,34×10⁻⁴ sur la seconde moitié, −2,17×10⁻⁴ sur le dernier quart, −5,20×10⁻⁴ à N = 48. | `e3_abc.json:103-106` et `:164`, `experiences/e3_abc.py:85-87` | OK |
| S6 | `PLAN.md:205`, `MANQUES.md:4` et `:115` | E2 n’est pas une dynamo. E3 n’a pas de générateur. Aucune scène waiting ne dessine un champ 3D. Aucune issue ne dit "renversements 3D générés". Les `result-unmet` restent dicibles. | `en/rapport/index.qmd:925`, `en/these/index.qmd:97`, `MANQUES.md:36-111` | OK |
| S7 | `PLAN.md:121` | 31, 44 et 52 à 71 ne partagent pas un axe. | `specs/sources/dynamo.md:616-618`, `en/rapport/index.qmd:141` | OK |
| S8 | `PLAN.md:299`, `PLAN.md:214` | Le piège √3/η est écrit dans x02. Le cœur compare 8,87, 17,6, 26,8 aux fenêtres d’Archontis sans écrire Rm = 1/η dans l’idée. | `e3_abc.json:9`, `dynamo.md:390` et `:412`, `en/rapport/index.qmd:1112` | RÉSERVE |
| S9 | `PLAN.md:120` | `vks-en.png` reste schematic. | `en/rapport/index.qmd:163` | OK |
| S10 | `PLAN.md:229` | "Aucun modèle génératif de dynamo" est daté du 2026-11-06, confiance moyenne. Le plan écrit medium. La confiance haute vise un autre fait. E1, E2 et E3 ne ferment pas ces lacunes en 3D borné. | `en/rapport/index.qmd:228` et `:238-245`, `en/these/index.qmd:163` | OK |
| S11 | `INVENTAIRE.md:36` | 4,10 et 3,90 restent un jugement de l’auteur. Le plan ne les affiche pas. | `en/encadrants/index.qmd:431` et `:437` | OK |
| S12 | `PLAN.md:147` et `:228` | Quatre noms, titres et rôles, sans opinion ajoutée. | `en/index.qmd:72`, `en/encadrants/index.qmd:130-212` | OK |
| S13 | `PLAN.md:90`, `:107`, `:133` | Bandes océaniques, dernier renversement, disque, Larmor, Glatzmaier et Roberts. Aucun âge, aucun seuil, aucune année dans `PLAN.md`. Le 170 kyr est cité pour être refusé comme fait géologique. | `INCERTITUDES.md:82-92`, `dynamo.md:285` | OK |
| S14 | `PLAN.md:241` | Budget ≈ 1,1×10⁴ h GPU, facteur deux, zéro mesure GPU. | `en/these/index.qmd:959-973` | OK |
| S15 | `PLAN.md:145` et `:264` | Le rapport est prospectif et non endossé. | `en/index.qmd:43-45` | OK |
| S16 | `INVENTAIRE.md:218-256` | Les moyennes E1 et E2 citées à l’écran sont dans le JSON, et le digest en est l’arrondi. | `e1_gissinger.json` résumé, `e2_mhd2d.json` résumé | OK |
| S17 | `PLAN.md:188` | "E2, 50 pas de Heun" est vrai dans le rapport et le script. `digest.md:127` ne le dit pas. L’inventaire ne le range que sous E1. | `en/rapport/index.qmd:595`, `experiences/e2_mhd2d.py:198`, `digest.md:5` et `:127` | RÉSERVE |
| S18 | `PLAN.md:174-176` | La fréquence de Rice est montrée comme loi plus F, avec 4 %, 6 %, 14 %, 65 %, 42 %. Le cœur ne dit pas que la densité jointe n’est pas garantie sur E1. | `en/rapport/index.qmd:509-528`, `:883`, `:901` | BLOQUANT |
| S19 | `PLAN.md:201` et `:287` | Les mesures de projection et de recalage collent au corollaire 6. x01 énonce "KL infini, borne W1" sans les hypothèses. | `en/rapport/index.qmd:447-455`, `digest.md:19` et `:144` | BLOQUANT |
| S20 | `PLAN.md:214` | 8,87, 17,6 et 26,8 sont les bons arrondis. Le cœur ne porte pas ±0,1 sur le second seuil ni ±1 sur le troisième. | `en/rapport/index.qmd:1114`, `INCERTITUDES.md:37` | BLOQUANT |
| S21 | `PLAN.md:225` | "3 variables latentes, Re = 100" est vrai à la ligne citée et absent de `INVENTAIRE.md`. | `en/rapport/index.qmd:169` | BLOQUANT |
| S22 | `PLAN.md:303` | "24 symétries" est vrai à la ligne citée et absent de `INVENTAIRE.md`. | `en/rapport/index.qmd:1120`, `dynamo.md:400` | BLOQUANT |
| S23 | `PLAN.md:275` | "Masse du pont \|D\| < 0,25" n’est pas dans l’inventaire. La ligne citée 883 ne contient pas 0,25. | `en/rapport/index.qmd:729`, `:807`, `:883`, `:1269` | BLOQUANT |
| S24 | `PLAN.md:313` | "μr d’ordre 50 à 100 selon l’article" ne sort pas des lignes citées. | `dynamo.md:160`, `:193-194`, `:220` | BLOQUANT |
| S25 | `PLAN.md:325` | "8 février 2027, 9 h" est dans la recommandation et absent de l’inventaire. | `infra/cloud/RECOMMANDATION-CLOUD.md:873` | BLOQUANT |
| S26 | `PLAN.md:302` | "λ ≥ −1/Rm tenu à Rm = 2". Le JSON vaut −0,500053, soit 5,3×10⁻⁵ sous −0,5. | `e3_abc.json:14`, `en/rapport/index.qmd:1116`, `digest.md:172` | RÉSERVE |
| S27 | `PLAN.md:133` | 90 ± 5 et 130 ± 10 sont justes. L’idée ne rappelle pas Re = 1,5×10³ ni μr = 50. | `dynamo.md:223-225`, `en/rapport/index.qmd:143` | RÉSERVE |
| S28 | `INVENTAIRE.md:209` | SW1 "par 3" pour 0,107 / 0,0333. Le quotient vaut 3,21. | `digest.md:14` et `:19`, `en/rapport/index.qmd:881` | RÉSERVE |
| S29 | `STYLE.md:80-92` | u, B, t, Γ, λ, η, Rm, Q, D, V gardent le sens du film. g10 écrit σ/σ_ref. Le dipôle D et la dissipation restent deux symboles. | `STYLE.md:82-92`, `PLAN.md:201` | OK |

## Bloquants

### S18. Hypothèses de Rice dans le cœur

`PLAN.md:174-176`. La proposition 8 demande un processus stationnaire, des trajectoires C¹, un observable linéaire, et une densité continue du couple D et Ḋ. L’estimateur de fenêtre a un biais d’ordre h² et une variance d’ordre 1 sur Nh. Quatre limites suivent. F doit être connu. Tous les passages comptent, excursions et brouhaha compris. La loi des temps d’attente n’est pas dans la loi stationnaire. Pour une dynamique déterministe, la densité continue n’est pas garantie.

Le cœur dit bien la dépendance à la loi et à F, le refus des temps d’attente, et le comptage des excursions. Il donne h sans la valeur 0,2. Il ne dit pas que E1 est déterministe et que l’hypothèse de densité n’est pas garantie. Le rapport le dit à la ligne 883, puis dans les réserves de la ligne 901. Les 4 % et 6 % y sont un contrôle numérique de l’estimateur de fenêtre, pas une application du théorème sous ses hypothèses.

Les cellules tiennent. À Γ = 0,91, Rice C vaut 0,00937 et le comptage 0,00567, `digest.md:103`. L’écart relatif vaut 65 %. À Γ = 0,905, 0,00807 contre 0,0049, `digest.md:102`, encore 65 %. Le plan place ce 65 % "en un point", et le 42 % "près du seuil". Cette séparation est juste. Les sommes cumulées 4 %, 6 %, 14 % et 42 % n’ont pas été recalculées. Elles sont celles de `en/rapport/index.qmd:883`.

Correction proposée. Dans `g08.not` ou `g08.numbers`, écrire que la densité jointe n’est pas garantie, que h = 0,2, et que 4 % et 6 % sont le contrôle numérique de la fenêtre. Garder PROVED sur l’énoncé, MEASURED sur les pourcentages.

Critère de levée. L’idée du cœur contient ces trois précisions, et la pastille PROVED ne couvre pas les pourcentages.

### S19. Stationnarité en loi et corollaire 6

`PLAN.md:201` et `PLAN.md:287`. Le bon niveau est la loi. Remarque 3.4. dE/dt = P − ε est une identité sur un instantané, et la contrainte est l’espérance nulle. Proposition 5. L’invariance donne E[Lφ] = 0. Corollaire 6, lignes 447 à 455. Si la loi de Lφ ne charge pas 0, ce qui est le cas dès que la variance est strictement positive et qu’il y a une densité, l’ensemble où Lφ vaut 0 est négligeable. Toute loi portée par cet ensemble est singulière, et la KL vers μ est infinie. Si de plus Lφ est lipschitzienne, W1 est minoré par E|Lφ| / L, donc strictement positif.

E1, variante E. La projection par échantillon annule dE/dt. σ tombe à 4,17×10⁻¹⁷, `digest.md:19` et le JSON. La distance d’énergie passe de 0,00257 à 0,0231, facteur 8,99, affiché ×9. Le témoin de variance avant projection est σ_ref = 0,37772, donc l’hypothèse de non-concentration est satisfaite sur ce banc.

E2, recalage. Le script multiplie les échelles |k| > 3 pour imposer la dissipation égale à l’injection sur chaque échantillon, `experiences/e2_mhd2d.py:328`. Le résidu moyen tombe à 8,27×10⁻⁶ et σ/σ_ref à 8,64×10⁻⁴, `digest.md:144`. Ce sont des quasi-zéros numériques. La KL infinie reste la conclusion du corollaire, sous concentration exacte. La distance peut quand même baisser, 1,1 contre 2,62 sur la base. Le plan montre les deux chiffres ensemble. C’est le bon couple.

x01.c6 résume "KL infini, borne W1". Les deux conclusions sont vraies sous les hypothèses. Sans elles, la phrase est plus forte que le corollaire.

Correction proposée. L’idée de x01.c6 et le calque portent la non-concentration et, pour W1, le lipschitz. Pour E1 et E2, dire que la variance mesurée avant contrainte n’est pas nulle. Ne pas écrire que la KL mesurée est infinie. Les chiffres d’écran restent 4,17×10⁻¹⁷ et 8,64×10⁻⁴.

Critère de levée. x01.c6 énonce les deux hypothèses, et aucun calque n’attribue une KL infinie au chiffre mesuré.

### S20. Précision des seuils E3 dans le cœur

`PLAN.md:214`. Les trois affichages 8,87, 17,6, 26,8 sont l’arrondi du rapport. Le JSON a les trois flottants cités plus haut. L’interpolation des seuils lit le signe de λ sur la seconde moitié, t > t_total/2, `experiences/e3_abc.py:85-86` et `:111-112`. λ du dernier quart ne rentre pas dans cette interpolation. À Rm = 17,5, la seconde moitié est positive et le dernier quart est déjà négatif. 17,6 dépend donc de la fenêtre.

Le rapport, ligne 1114, borne le second seuil à environ 0,1 près de 17,5, et le troisième à environ une unité. `INCERTITUDES.md:37` demande d’afficher ces deux limites avec l’arrondi. L’idée du cœur dit que le signe change à Rm = 17,5. Elle ne dit pas ±0,1 ni ±1. x02 le dit pour le troisième seuil, et x02 sort du cœur. Montrer 26,8 en face de "au-dessus de 27" sans l’unité d’incertitude fait lire un écart de 0,2 là où la mesure ne tranche pas à mieux qu’une unité.

Correction proposée. Ajouter à `g11.e3` que le second seuil est connu à environ 0,1 près, que le troisième l’est à environ une unité, et que 17,6 est l’interpolation de la seconde moitié.

Critère de levée. Ces trois précisions sont dans l’idée de `g11.e3`. x02 peut les répéter. Il ne suffit pas.

### S21. Trois variables latentes et Re = 100

`PLAN.md:225`. Fukami et Taira compressent un profil à Re = 100 en trois variables latentes. C’est la ligne `en/rapport/index.qmd:169`. `INVENTAIRE.md` cite l’article sans ces deux nombres. La règle du plan fait de tout nombre d’écran absent de l’inventaire un bloquant.

Correction proposée. Ajouter la phrase à `INVENTAIRE.md`, avec `en/rapport/index.qmd:169`. Garder le chiffre.

Critère de levée. L’inventaire contient les deux nombres et la cellule Sources de `g12.learn` pointe vers cette ligne.

### S22. Groupe à 24 éléments

`PLAN.md:303`. Le mode de la première fenêtre a les symétries paires du groupe de l’ABC, 24 éléments. `en/rapport/index.qmd:1120` et `dynamo.md:400` le disent. L’inventaire ne le dit pas. La même page de `dynamo.md` porte d’autres nombres, Rm1 dans [24,05, 24,10], Rm2 dans [215,0, 215,4], ω ≈ 0,53, σ ≈ 0,1 à Rm = 25 000. Le plan ne les affiche pas. Il ne faut pas les faire entrer avec le 24.

Correction proposée. Une ligne d’inventaire, limitée au groupe de 24 éléments et au mode pair, avec `dynamo.md:400`.

Critère de levée. L’inventaire a cette ligne, et ni le plan ni l’inventaire n’ajoutent les autres nombres du paragraphe.

### S23. Seuil du pont |D| < 0,25

`PLAN.md:275`. La masse du pont est la probabilité que la valeur absolue de D soit inférieure à 0,25. Cette définition est à `en/rapport/index.qmd:729`, rappelée aux lignes 807 et 1269. La cellule cite la ligne 883. Cette ligne porte le plafond 2×10⁻⁴. Elle ne porte pas 0,25. Dans l’inventaire, le 0,25 de la ligne 58 est le diamètre D1 de Riga. Le seuil du pont est un autre nombre.

Correction proposée. Citer `en/rapport/index.qmd:729` pour 0,25, et garder `en/rapport/index.qmd:883` pour 2×10⁻⁴. Ajouter le seuil du pont à l’inventaire, sous un nom qui ne se confond pas avec D1.

Critère de levée. L’inventaire a le seuil 0,25 du pont avec la ligne 729, et la cellule de `x03.bridge` ne cite plus 883 pour ce seuil.

### S24. Intervalle de μr

`PLAN.md:313`. L’idée dit "μr des turbines, ordre 50 à 100 selon l’article", et cite `dynamo.md:189-196` plus `:220`.

Les lignes 193 et 194 donnent un μr maximal de 60, et des mesures vers 65 à 70, pour Giesecke et al. 2010. La ligne 220 donne un μr d’ordre 50 pour les turbines de Nore et al. 2018. Le μr ≈ 100 est Monchaux et al. 2009, à `dynamo.md:160`. La cellule ne cite pas cette ligne. L’intervalle 50 à 100 est absent des lignes citées.

Correction proposée. Trois faits, trois lignes. Le fer sélectionne le mode axisymétrique, `dynamo.md:193`. μr d’ordre 50, `dynamo.md:220`. μr ≈ 100, `dynamo.md:160`. Pas d’intervalle fusionné.

Critère de levée. La scène n’affiche plus "50 à 100", et chaque nombre affiché est celui de sa ligne.

### S25. Date du 8 février 2027

`PLAN.md:325`. `RECOMMANDATION-CLOUD.md:873` écrit que la prochaine clôture de l’accès régulier est le 08/02/2027 à 9 h, source EDARI, dans une recommandation du 2026-11-08. Le plan dit déjà que la date reste à confirmer. Elle n’est pas dans `INVENTAIRE.md`. Un nombre d’écran absent de l’inventaire est bloquant, même quand la source gelée le contient.

Correction proposée. Soit retirer l’heure de l’idée tant que les encadrants ne l’ont pas confirmée. Soit ajouter dans l’inventaire une ligne CONTEXT, "clôture EDARI lue dans la recommandation, à reconfirmer", avec `RECOMMANDATION-CLOUD.md:873`. Cette date reste une citation externe.

Critère de levée. La date est absente de la scène, ou elle est dans l’inventaire avec le statut à reconfirmer.

## Réserves

### S8. Rm = 1/η dans le cœur

x02 écrit le piège R_M = √3/η d’Alexakis. Le cœur compare les seuils mesurés aux fenêtres 8,9, 17,5 et au-dessus de 27. Archontis utilise Rm = 1/η. Le JSON le dit à `e3_abc.json:9`, clé "Rm" égale à "1/eta". La comparaison ne mélange donc pas les deux conventions. L’idée de `g11.e3` ne nomme pas Rm = 1/η. `INCERTITUDES.md:32` demande de le dire avant toute comparaison.

Correction proposée. Écrire Rm = 1/η dans l’idée de `g11.e3`.

Critère de levée. L’idée de `g11.e3` contient Rm = 1/η.

### S17. Cinquante pas de Heun pour E2

Le rapport, ligne 595, intègre E1 et E2 par Heun en 50 pas. Le script E2 appelle `steps=50` à `experiences/e2_mhd2d.py:198`. Le JSON E2 n’a pas de clé Heun. `digest.md:127` ne le dit pas. `digest.md:5` le dit pour E1. L’inventaire range Heun 50 dans la ligne E1 seulement. Le nombre d’écran est juste. La ligne citée pour la moitié E2 ne le porte pas.

Correction proposée. Citer `en/rapport/index.qmd:595` dans la cellule, et ajouter Heun 50 à la ligne E2 de l’inventaire.

Critère de levée. La cellule et l’inventaire citent une ligne qui dit Heun 50 pour E2.

### S26. Test de Beltrami à Rm = 2

La théorie dit λ ≥ −1/Rm. À Rm = 2, le mode exact vaut −0,5. Le JSON donne λ = −0,5000532022510549 et λ du dernier quart = −0,5000070612796725, `e3_abc.json:14-15`. L’écart au mode exact est 5,3×10⁻⁵. Le digest affiche −0,5001 et −0,5. Le rapport dit "au niveau de la valeur exacte". Le plan dit "tenu".

Correction proposée. Écrire "au niveau de −0,5, à quelques 10⁻⁵ près", comme le rapport.

Critère de levée. L’idée ne dit plus que l’inégalité est satisfaite exactement par le flottant du JSON.

### S27. 90 ± 5 et 130 ± 10

Ces deux seuils sont ceux de Nore et al. 2018, table 3, à Re = 1,5×10³ et μr = 50, en changeant la condition aux limites. Le plan dit "simulations du consortium" et cite les bonnes lignes. L’idée ne répète pas Re ni μr. À côté des Rm expérimentaux de g03, le spectateur peut lire 90 et 130 comme un quatrième Rm de salle.

Correction proposée. Mettre Re = 1,5×10³ et μr = 50 dans l’idée de `g04.sim`.

Critère de levée. Les deux paramètres sont dans l’idée, avec la pastille CONTEXT.

### S28. Facteur 3 sur SW1

0,107 / 0,0333 = 3,21. Le rapport écrit "par 3" et donne les deux nombres, qui sont justes. L’inventaire reprend "par 3". Avec deux graines, seul un facteur deux ou plus est retenu. 3,21 reste dans cet ordre. Le plan, lui, n’affiche pas ce facteur. Il affiche le ×9, qui tient.

Correction proposée. Dans l’inventaire, écrire 3,2, ou garder les deux nombres sans le facteur.

Critère de levée. L’inventaire ne dit plus "par 3" pour un quotient de 3,21, ou la scène n’utilise pas ce facteur.

## Statut de chaque résultat

PROVED veut dire démontré dans le rapport prospectif. Cela ne veut pas dire publié, ni endossé. CONJECTURE porte la confiance écrite dans `INCERTITUDES.md`. MEASURED est un chiffre de JSON ou de digest. PLANNED n’a pas été exécuté.

| Résultat | Statut | Limite à tenir à l’écran |
|---|---|---|
| Définitions 3.1, 3.2, 3.3, 3.9. Remarques 3.4, 3.7, 3.11. Propositions 1, 2, 4, 5, 7, 8, 9. Corollaire 6. | PROVED dans le rapport | Hypothèses du texte. Voir S18 et S19. |
| E1, table de test, seuil 0,86 à 0,865, plancher 0,0040, ×9 | MEASURED, numérique | Deux graines. CPU. Dimension 3. Interpolation seulement. h = 0,2. Densité non garantie. |
| E2, V0 à V5, témoin, recalage, inclinaison | MEASURED, numérique | Une graine. Zel’dovich. Forçage f_a. Pm de 0,35 à 2. Plancher de test optimiste. |
| E3, λ de Rm, seuils, divergence du solveur | MEASURED, numérique, solveur seul | Cinématique, sans force de Lorentz. Rm = 1/η. Signe non résolu à 17,5. Pas de générateur. |
| Courbes `vks-en.png` | Schéma | Durées et amplitudes différentes de VKS. CONTEXT seulement pour la géométrie sourcée. |
| 74 renversements du script RK4 | Vérification interne | Le plan ne l’affiche pas. Ne pas la présenter comme E1. |
| Absence d’un modèle génératif de dynamo au 2026-11-06 | CONJECTURE, confiance moyenne | Une absence ne se prouve pas. À relire avant chaque article. |
| Perte de stationnarité utile en 3D, Rice à 20 % sur un champ turbulent, 64³ suffisant à Re ≥ 100 | CONJECTURE, confiance faible | Critères de palier, non mesurés. |
| Équivariance hors des Γ vus, sur E1 | CONJECTURE, confiance haute sur ce banc | Deux graines, plancher explicite. Pas un résultat VKS. |
| Budget 1,1×10⁴ h, réserve 20 %, H1 à H5 | PLANNED | Facteur au moins deux. H4 ne compte pas les simulations de référence en GPU. H1 est un chiffre publié par d’autres, environ 1 150 h. Aucune mesure GPU MilaDy. |
| Paris P-div, P-field, P-stat, P-blur, P-tg, P-bill, P-vks, P-dresdyn | PLANNED, scènes waiting | Créneau `bet` tant que le JSON n’a pas de statut. `result-unmet` dit l’échec. Aucun champ 3D dessiné. |
| Bandes océaniques, date du dernier renversement, dynamo à disque, Larmor, Glatzmaier et Roberts | blocked-source | Aucun nombre dans `PLAN.md`. |
| Scores 4,10, 3,90 et 4,45 | Jugement de l’auteur du site | Hors écran. Non validé par les encadrants. Le 4,45 est favorable par construction. |
| Prix de location du 2026-11-08 | Méthode datée | Hors décision. Le cœur ne les montre pas. |

## Ce qui a été rouvert et qui tient

Les moyennes E1 de `digest.md:12-22` coïncident avec la table 1 du rapport une fois σ divisé par σ_ref = 0,37772. Exemple tenu. Variante C, σ = 0,384, rapport 1,02. Projection E, σ = 4,17×10⁻¹⁷, rapport 1,1×10⁻¹⁶. Le JSON E1 donne les mêmes moyennes avant arrondi, dont 0,00257347 et 0,02311665 pour les distances C et E au test.

Le JSON E2 donne la distance V5 au test 0,699177 et le témoin dans le digest à 2,52. 2,52 / 0,699 = 3,605. V0 est à 4,31. Le plan compare V5 au témoin.

Les graines E1 sont 0 et 1. E2 n’a pas de liste de graines dans son JSON. Le plan le dit dans le caveat de g10.

Les défauts de `QUESTIONS.md` relus contre leur colonne "À lire" suivent les lignes ouvertes. Rm = Re × Pm = 400 à Re = 200 et Pm = 2 est dans `infra/configs/palier2_tg3d.yaml:12` et dans l’inventaire. L’ancrage et la montée de β sont désactivés par défaut à `en/calcul/index.qmd:166`. Le caractère poissonien des temps longs est dans le modèle, `dynamo.md:363` et `en/rapport/index.qmd:159`, et le plan refuse le taux terrestre.
