# MilaDy G0 — Revue pédagogique indépendante

## Référence et verdict

- Dépôt : `knoel99/milady-2027`, branche de référence `grok/video-plan`, PR #1.
- **Commit exclusivement relu : `b3517f588f39795b92a4e5e0309e6fb5c9e1328a`.** Tous les repères `fichier:ligne` ci-dessous renvoient à ce commit, non à la tête courante de la branche. Les chemins abrégés sont sous `video-grok/`.
- Lecture indépendante : aucune consultation de l’autre revue ni du chantier `video/` ; aucun changement du dépôt.
- **Bloquants pédagogiques démontrés : 0. Réserves : 6.**
- **Verdict : G0 pédagogie favorable avec réserves.** L’architecture ne démontre pas de falaise inévitable ; elle n’est pas une validation du futur film. Le minutage détaillé de l’étendu et les créneaux de cartes doivent être harmonisés avant le gel des scripts. La fermeture globale de G0 reste au pilotage, après la revue scientifique indépendante et les éventuels correctifs bloquants.

Un bloquant désigne ici une erreur ou une falaise que le plan impose, et non l’absence normale d’un script, d’une animation ou d’une preuve d’écoute futurs. Les incohérences de minutage sont avérées, mais ne prouvent pas à elles seules qu’une explication exige deux fois le temps disponible. Elles sont donc des réserves, pas des bloquants artificiels.

## Chapitre par chapitre

« Tient » signifie compatible au stade plan ; les réserves et contrôles ultérieurs restent applicables. Les cues indiqués comme génériques utilisent la convention de `PLAN.md:71`, sans prétendre que leur implémentation existe.

| Chapitre | Verdict | Repère concerné et justification |
|---|---|---|
| g00 | tient | `cue.g00.needle.show` : bascule vers 7 s du film, puisque g00 commence à 0:00 ; légende hors échelle explicite (`PLAN.md:23,75-82`). |
| g01 | tient | `cue.g01.rate.predict` : distingue fréquence et date ; la coupe éventuelle des bandes conserve sa durée dans rate (`PLAN.md:90-95`). |
| g02 | tient | `cue.g02.ratio.formula` : étirement/effacement puis rapport, prédiction puis formule et éclairage U/L/η (`PLAN.md:103-110`). Définition orale de Pm à contrôler, sans exiger un cours supplémentaire. |
| g03 | tient | `cue.g03.vks.show` : expériences puis conventions de Rm ; trois étiquettes sans axe abusivement commun (`PLAN.md:118-123`). Densité à surveiller, R3. |
| g04 | tient | `cue.g04.reduced.show` : histoire située après les laboratoires ; 2:30, dans le cœur (`PLAN.md:125-138`). Ce n’est pas une histoire exhaustive promise. |
| g05 | tient | `cue.g05.snapshot.predict` : besoin de champs avant différence instantané/loi ; stage annoncé prospectif (`PLAN.md:144-148`). |
| g06 | tient | `cue.g06.recap.show` : récapitulatif L0–L2 sans idée neuve (`PLAN.md:150-152`). Très sensible à la réserve R2 sur le temps de carte. |
| g07 | tient | `cue.g07.inherit.predict` : polarités et récapitulatif préparent le modèle réduit ; lecture de symétrie contre plancher (`PLAN.md:156-167`). Traduction des trois modes en mots/images à vérifier au script, R3. |
| g08 | tient | `cue.g08.numbers.predict` : question de fréquence déjà posée ; loi sans ordre temporel avant Rice ; limites explicites dans le cœur (`PLAN.md:173-179`). |
| g09 | tient | `cue.g09.path.show` : bruit, segments, directions avant justification du solveur ; conditionnement ensuite (`PLAN.md:185-189`). Le flot artificiel ne doit pas devenir une trajectoire physique, R3. |
| g10 | tient | `cue.g10.sample.formula`, `cue.g10.law.caveat` : classes, tentation de contrainte locale, mesure puis corollaire ; prépare L4 (`PLAN.md:197-205`). La présentation comparative doit rester séquentielle, R3. |
| g11 | tient | `cue.g11.e3.caveat` : bilan après les contraintes ; E3 annoncé sans générateur (`PLAN.md:211-215`). L’entrée ABC doit être intelligible sans x02, R3. |
| g12 | tient | `cue.g12.gaps.caveat` : littérature après bilan, limites datées ; 4:00 dans le cœur (`PLAN.md:219-231`). Une carte de familles, non un catalogue à mémoriser, R3. |
| g13 | tient | `cue.g13.bets.show` : paris explicitement waiting, sans champ 3D fabriqué (`PLAN.md:235-242`). Quatre paris à révéler successivement plutôt qu’à lire en concurrence, R3. |
| g14 | tient | `cue.g14.card` : reclasse les questions ; 2:20 satisfait 2–3 min (`PLAN.md:244-255`). Séparer présentation des questions et consultation du registre complet. |
| g15 | tient | `cue.g15.needle.show` : même aiguille et même échelle ; aucun symbole nouveau, non-résultat 3D explicite (`PLAN.md:257-264`). Générique sans opinion prêtée ; temps à régler dans l’enveloppe existante. |

## Accroche, paliers et autonomie

### Motivation → image → mots → formule

L’accroche survient bien dans les trente premières secondes, pas trente secondes après un préambule. Le titre vient après l’aiguille. Rm est motivé par la compétition étirement/effacement avant son écriture. Rice répond à la question de fréquence après la distinction loi/ordre temporel. Le corollaire 6 intervient après la tentation de « réparer » chaque champ (`PLAN.md:75-80,103-110,173-176,197-205`).

Le passage L2→L3 possède un récapitulatif g06 ; le passage L3→L4 utilise g10 comme charnière avant bilan et littérature. Il n’y a pas de dépendance explicitement imposée à une démonstration retirée. En revanche, un numéro de niveau et une équation allumée ne suffiront pas seuls à enseigner : R3 décrit les preuves d’intelligibilité à obtenir au script/pilote. Je ne transforme pas leur absence actuelle en défaut démontré.

### Test mental : supprimer tous les x

| Module retiré | Couture du cœur | Résultat |
|---|---|---|
| x03 | g08→g09 | g08 dit déjà moyenne ≠ temps d’attente et compte les excursions ; g09 peut commencer le générateur sans le détail (`PLAN.md:173-185,272-276`). |
| x01 | g10→g11 | les effets des propositions sont donnés dans g10 ; g11 ne présuppose pas leur preuve (`PLAN.md:197-215,293`). |
| x02 | g11→g12 | seuils, ambiguïté de signe et absence de générateur restent dans g11 ; la littérature ne nécessite pas les 24 symétries (`PLAN.md:214,225-231,299-305`). Introduction minimale d’ABC à contrôler, R3. |
| x04 | g13→g14 | parois restent un problème annoncé, non une technique nécessaire pour comprendre les questions (`PLAN.md:239-252,311-316`). |
| x05 | g14→g15 | question d’accès avant location déjà dans g14 ; retour public à l’aiguille ne nécessite aucun tableau budgétaire (`PLAN.md:250-264,322-329`). |

Le cœur est donc autonome au niveau des dépendances annoncées. L’étendu approfondit des limites, preuves, validations et conditions de réalisation, sans déplacer un prérequis essentiel hors du cœur. x03 monte à L4 puis revient à L3 : ce détour doit être signalé comme approfondissement facultatif, non comme nouvelle condition de compréhension.

## Réserves référencées et critères de levée

### R1 — Horloge détaillée de l’étendu incohérente — défaut démontré, non bloquant

- **Sources :** `PLAN.md:43-61,278-291,295-305,307-316`.
- **Constat :** x01 annonce 5:00 mais ses huit lignes totalisent **5:40** ; x02 annonce 3:30 mais totalise **3:50** ; x04 annonce 4:00 mais totalise **3:40**. x03 et x05 totalisent correctement 3:00 et 3:30. Les modules détaillés donnent **19:40**, donc **60:40** avec le cœur, contre 60:00 dans l’horloge supérieure. Le cœur détaillé reste bien à 41:00.
- **Conséquence apprenant :** risque de couper des respirations ou des liens de preuve pour tenir l’horloge, particulièrement dans x01 ; les cartes étendues seraient aussi décalées.
- **Correction minimale :** choisir une allocation cohérente des sous-scènes dans les enveloppes 5:00/3:30/4:00, en récupérant d’abord le temps excédentaire des cartes (R2), plutôt qu’en accélérant les explications. Recalculer les horloges des cartes après cette décision.
- **Levée :** somme des scènes = durée de chaque module ; somme des modules = 19:00 ; étendu = 60:00, cartes et pauses comprises. Aucune démonstration n’est déclarée complète par simple compression de débit.

### R2 — Cartes annoncées 6–10 s mais créneaux de 20–30 s — défaut démontré, interprétation à lever

- **Sources :** `PLAN.md:71,93,108,152,165,203,291,327` ; `STYLE.md:107,122` ; `QUESTIONS.md:11,59,136-139`.
- **Constat :** les règles imposent 6–10 s ; les lignes nommées card et les horloges des questions réservent fréquemment 20–30 s. Le plan n’explicite pas si le reste est transition, synthèse parlée ou maintien silencieux de la carte. Ce ne sont pas nécessairement 20–30 s de carte réellement voulues.
- **Conséquence apprenant :** soit carte courte étirée artificiellement, soit budget oral comprimé. Cas sensible : g06 a 35 s et 73–76 mots ; si sa carte occupait réellement les 20 s de `QUESTIONS.md`, il ne resterait que 15 s pour le reste.
- **Correction minimale :** distinguer dans les créneaux existants synthèse/transition et carte réellement visible ; ne laisser que 6–10 s à cette dernière. Conserver les budgets de chapitre et réattribuer explicitement le solde.
- **Levée :** une seule durée par carte dans plan, registre et cues ; aucune carte >10 s ; lecture minutée EN et FR compatible avec le budget effectif et les pauses. Pas d’exigence de voix produite à G0.

### R3 — Densité et lexique : risques de falaise à vérifier au script, pas falaises établies

- **Sources :** `PLAN.md:118-120,160-164,174,185-188,197-202,214,225-229,240`.
- **Constat :** Riga/VKS empilent plusieurs nombres ; g07 ouvre sur trois équations ; F et la fenêtre h arrivent avec Rice ; g09 introduit Heun ; g10.sample rapproche E2 et E1 ; g11 cite les seuils avant le module ABC ; g12.gen aligne cinq familles/noms. Une même idée comparative peut tenir en plusieurs révélations, mais pas en lectures simultanées concurrentes.
- **Conséquence apprenant :** perdre le sens des variables, confondre temps de génération et temps physique, ou traiter tous les chiffres/noms comme des prérequis.
- **Correction minimale :** au script, réserver un repère préalable de motivation/image/mots pour Q,D,V, F et ABC ; désigner Heun par sa fonction avant son nom ; ordonner séparément les comparaisons E1/E2 de g10.sample. Distinguer nombres à comprendre et contexte simplement visible. Faire de g12 une carte de familles, sans expliquer chaque méthode en profondeur.
- **Levée :** relecture G1/G2 sur montage cœur seul : un lecteur peut reformuler l’idée de chaque scène sans x01/x02/x03 ni lecture de l’équation ; un seul objet demande une nouvelle lecture à la fois. Si le script exige effectivement un prérequis absent ou deux fois le budget, requalifier alors en bloquant.

### R4 — Limites présentes, audibilité encore non contractualisée partout

- **Sources :** `PLAN.md:145,160-161,175-176,205,214,229-230,235-241`.
- **Constat :** E1 est bien un modèle réduit, g08 borne l’interprétation de Rice ; E2 a « une graine, interpolation, pas une dynamo » sur un cue caveat ; E3 a « pas de générateur ». Ces contenus sont au bon endroit, mais le plan ne dit pas partout expressément lesquels doivent être prononcés, plutôt que laissés à la pastille ou à une légende.
- **Conséquence apprenant :** en écoute seule, croire à des renversements 3D générés ou à une estimation géologique.
- **Correction minimale :** marquer comme obligations orales des deux langues : domaine réduit d’E1 et passages par zéro ; nature 2D/non-dynamo et portée limitée d’E2 ; validation de seuils sans générateur pour E3. Préserver le statut prospectif/non endossé et les paris non exécutés.
- **Levée :** contrôle des scripts puis écoute seule au pilote/film : ces limites sont dicibles et entendues, sans dépendre du texte anglais à l’écran. L’absence actuelle d’audio n’est pas un bloquant G0.

### R5 — Pilote représentatif techniquement, carte question insuffisamment affectée

- **Sources :** `LOTS.md:49-57,59-66` ; `PLAN.md:193,197,201-205`.
- **Constat :** classes et sample testent bien PROVED/MEASURED, contrainte locale/loi, mesure, formule, prédiction et piège « E2 n’est pas une dynamo ». Toutefois les deux fichiers HTML prescrits n’incluent pas g10.card, alors que le pilote promet une carte question. Le caveat du plan est attaché à g10.law, hors des deux scènes retenues ; le critère « not a dynamo » du pilote compense visuellement cette absence.
- **Conséquence apprenant :** le pilote pourrait être accepté sans tester la question de fin ni l’audibilité du piège.
- **Correction minimale :** affecter explicitement un extrait de carte et le caveat oral à la séquence d’essai, sans imposer de réaliser tout g10.
- **Levée :** la capture pilote comprend une carte 6–10 s, la pause 2–3 s avant la barre, le calque et une limite E2 audible EN/FR. Il reste un test représentatif de composants, non une preuve que le passage g06→g08 fonctionne ; ce dernier relève de G1/G2.

### R6 — Suppression éventuelle du disque : 15 s sans destination

- **Sources :** `PLAN.md:91,107,23-24`.
- **Constat :** la suppression des bandes océaniques a un réemploi explicite de 25 s dans g01.rate ; la coupe autorisée du disque n’a pas d’équivalent explicite pour ses 15 s.
- **Conséquence apprenant :** montage cœur raccourci ou remplissage tardif, sans bénéfice pédagogique identifié.
- **Correction minimale :** réallouer ces 15 s à la comparaison mouvement/diffusion ou à sa synthèse, sans nouvelle notion.
- **Levée :** variante avec disque et variante sans disque ont une enveloppe g02 identique de 3:20, cœur 41:00 et budget oral ajusté.

## Budgets et questions : bilan de contrôle

- **Cœur :** 41:00 confirmé par les durées de chapitre et leurs sous-scènes ; **étendu :** 60:00 cible, mais 60:40 dans le détail actuel (R1).
- **Narration :** 5 125–5 330 et 7 500–7 800 mots correspondent bien à 125–130 mots effectifs/min pour 41/60 min (`PLAN.md:15`). Cette mesure inclut les pauses : elle ne signifie pas un débit articulé constant de 125–130 pendant toute la parole. Aucun texte n’existe encore pour certifier la réalisation. Les listes ne nécessitent pas manifestement le double du budget si noms et détails restent contextuels ; R2/R3 protègent cette hypothèse.
- **Pauses prédictives :** 2–3 s explicitement dans les durées (`PLAN.md:71`). Prédiction avant Rm (`104`), avant les pourcentages Rice (`179`) et avant la barre écrasée (`201`) : présentes. À vérifier sur cues, non à ajouter au total après coup.
- **Cartes :** toutes les formulations anglaises sont sous 18 mots. `q.g07` a bien **11 mots** : Vary / Gamma / as / in / E1 / or / mu / as / in / the / paper (`QUESTIONS.md:59-61`). Chaque carte ouvre une décision dominante et le registre fournit un défaut. Les parenthèses de comptage ne sont pas toutes exactes au mot séparé par espace (par exemple q.g08 : 8 plutôt que 9), sans incidence sur le plafond. Ne pas afficher ces compteurs dans le film.
- **Before we compute :** 2:20, conforme ; histoire : 2:30 ; état de l’art contemporain : 4:00, conforme à 4–5 min. Les deux dernières unités restent dans le cœur (`PLAN.md:27,35,37,125-138,219-231,244-255`).
- **Visuels et langues :** anglais dans les deux montages, voix EN/FR et identifiants de cues communs prévus (`PLAN.md:7-13,351-353`). La compréhension des légendes anglaises en voix FR sera à tester, pas présumée acquise.

## Liste des bloquants

**Vide — 0 bloquant pédagogique démontré au commit relu.** Aucune rédaction de script ou scène n’a été entreprise.

## Sources lues et limites

1. `video-grok/REVUES.md`, lu en premier : périmètre, définition du bloquant, contrôles et format.
2. `video-grok/PLAN.md`, intégralement, horloges et modules compris.
3. `video-grok/STYLE.md`, sections 4, 8 et 11 évaluées : motifs, cartes, rythme.
4. `video-grok/QUESTIONS.md`, cartes et défauts, registre compris.
5. `video-grok/LOTS.md`, section pilote évaluée uniquement pour sa représentativité.

Les outils GitHub renvoient les fichiers entiers : STYLE et LOTS ont été reçus intégralement, mais les conclusions sur ces documents restent limitées aux sections ci-dessus. Aucune source scientifique sous-jacente n’a été rouverte ; leurs nombres et démonstrations ne sont pas certifiés ici. Aucune nouvelle recherche web, simulation, exécution scientifique, entraînement, benchmark, génération sonore, dépense, lecture de `video/`, ni publication. Les vérifications d’écoute, débit réel, lisibilité des équations, compréhension indépendante et synchronisation attendent normalement scripts et pilote.

Document local prêt pour intégration ultérieure à `video-grok/revues/PEDAGOGIE.md` par le pilotage ; aucun fichier du dépôt n’a été écrit.
