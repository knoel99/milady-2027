# Questions pour les encadrants, avant de lancer les simulations

Fiche d'accompagnement du film *How Often Does the Field Flip?*, à apporter à S. Cheng et D. Lucor, avec
C. Nore et Y. Ponty, **avant** toute simulation, tout entraînement et toute location de GPU.

Rédigée le 8 novembre 2026 à partir du registre des questions du film
(`video/script/_shared/question_register.json`, 37 entrées à cette date), du chapitre « Before we compute »
(`video/script/ch10q.json`), de la recommandation cloud (`infra/cloud/RECOMMANDATION-CLOUD.md`, §0 et §4.2),
des six « Questions à discuter avec les encadrants » du rapport et de la matrice des risques du sujet de thèse.

---

## À quoi sert cette fiche

**Le but.** Comprendre le sujet, puis poser les bonnes questions avant de calculer quoi que ce soit.
Plusieurs réponses peuvent rendre la location inutile, ou changer ce qu'il faut calculer (recommandation
cloud, §0). Cette fiche range les 37 questions par ce qu'elles débloquent : **A**, à trancher avant de louer
du calcul ; **B**, le cadre scientifique ; **C**, les données et la logistique. Une proposition d'ordre du
jour pour une première réunion de 45 minutes la termine.

**Le lien avec le film.** Chaque chapitre du film se termine par une carte « ASK · Qn » ; les scènes dont
les résultats n'existent pas encore (les « sièges vides ») portent un encadré de question ; le chapitre
« Before we compute » [vidéo : ch10q, mm:ss] les regroupe et les classe. Les numéros Qn de cette fiche sont
ceux du film et du registre ; si le registre change, il fait foi. Les repères `[vidéo : unité, mm:ss]`
renvoient à la version longue en anglais, la seule qui contienne toutes les scènes ; ils seront remplis
après le rendu final à partir de `video/script/_build/*_cues.json`, grâce à l'identifiant de scène indiqué
à côté de chaque repère.

**Le lien avec la recommandation cloud.** Son §0 demande cet échange avant tout calcul, et son §4.2 liste
les décisions à écrire aux encadrants avant de louer. Tout y est repris : moyens de calcul et Jean Zay
(Q21), priorités (Q22), paramètres (Q18, Q3, Q6), mesures (Q8, Q9, Q16), diffusion (Q26). Le reste de ce
document suppose que la location reste utile après la réunion.

**Ce qu'il faut garder en tête.** Le rapport de stage est **prospectif** ; ses expériences E1 à E3 sont de
petits calculs sur processeur, avec une ou deux graines. Le sujet de thèse est une **proposition
indépendante**, ni demandée ni validée par les encadrants. La chaîne de calcul (`milady`, `infra/`) n'a
jamais tourné sur un GPU, sur un vrai cluster Slurm ni sur une machine louée. Aucun calcul n'a été lancé
pour le film : ses résultats 3D sont des paris écrits avant les données.

**Comment lire chaque question.**

- La question, telle que vous pourriez la poser, avec les personnes à qui la poser.
- **Pourquoi** : la raison, et la section du site à lire. Site en français :
  <https://knoel99.github.io/milady-2027/> (pages `rapport/`, `these/`, `encadrants/`, `calcul/`) ; les
  mêmes pages existent en anglais sous `en/`. Le document `ETAT-DE-L-ART.md` est dans ce dossier.
- **Débloque** : la décision que la réponse permet.
- **Par défaut** : ce que le projet ferait sans réponse (configuration actuelle, décision du film, ou plan
  écrit). Ne pas répondre revient à valider ce défaut.
- Le repère vidéo, puis une ligne **Décision** à remplir pendant la réunion.

**Priorités** (celles du registre ; le classement est une proposition, que les encadrants peuvent changer) :

- **P1** : à trancher avant de louer, car la réponse change ce qui est calculé, comment ou où (13 questions) ;
- **P2** : utile au plan de stage ou à la demande de données, pas aux premières campagnes louées ;
- **P3** : peut attendre (règles de verdict du palier 0, paliers 3 et 4, cadrage des articles).

**Notations** (celles du film) : s, taux de croissance du champ (λ dans le rapport, section E3) ; D, le
dipôle ; ε, la dissipation, et σ(ε)/σ_ref le rapport de sa dispersion à celle de la référence ; r₀, taux des
passages de D par zéro (il compte aussi les excursions) ; r, taux de renversement ; Rm, Re, Pm, nombres de
Reynolds magnétique, de Reynolds et de Prandtl magnétique ; μ_r, perméabilité relative du fer des turbines.

---

## A. À trancher avant de louer du calcul

Neuf questions, toutes P1 : où calculer, quoi d'abord, et les paramètres des deux campagnes 3D périodiques
configurées, `infra/configs/palier2_tg3d.yaml` (Taylor–Green, 12 simulations à 64³) et
`infra/configs/palier2_abc3d.yaml` (dynamo cinématique ABC, Rm de 4 à 40).

### A1. Quels GPU pour le stage ? · Q21 · P1 · S. Cheng, D. Lucor

> « Le CEREA ou le LISN ont-ils des GPU accessibles à un stagiaire ? Existe-t-il déjà un projet GENCI sur
> Jean Zay auquel je pourrais être ajouté ; sinon, qui déposerait un accès dynamique, et quand ? Lab-IA ou
> Ruche sont-ils accessibles par le LISN, et depuis quelle adresse IP faudrait-il se connecter ? »

- **Pourquoi** : aucune heure GPU n'a été mesurée ; le dépôt est prêt pour Slurm et Apptainer (sans avoir
  été essayé sur un vrai cluster), donc avec des GPU de laboratoire ou un projet existant, la location se
  réduit à un essai. À lire : Calcul, « Ce qui est testé, ce qui reste à vérifier » ; recommandation cloud
  §0 et §8.4 ; rapport §7, question 6.
- **Débloque** : où tournent les calculs manquants (M1 et M3 à M8 de la recommandation cloud), qui dépose
  l'accès dynamique GENCI et quand, et s'il faut louer une machine.
- **Par défaut** : une seule session louée (Scaleway L4, scénario A à 64³ : ≈ 6 à 12,5 h facturées,
  ≈ 6 / 16 / 38 € TTC en bas / probable / haut) ; une demande d'accès dynamique sur Jean Zay (≈ 500 à
  1 500 h H100) à faire déposer par S. Cheng ou D. Lucor en janvier ou février 2027, pour le 128³, le 256³
  et la thèse ; pas de 256³ sur un compte personnel.
- [vidéo : ch10, mm:ss] — scène `10.2` (encadré de `X5.3` dans la version longue)
- **Décision** :

### A2. Quelles campagnes d'abord ? · Q22 · P1 · les quatre encadrants

> « Les campagnes périodiques prévues (Taylor–Green et ABC à 64³, puis le générateur 3D) vous
> intéressent-elles, ou préférez-vous que je commence par vos propres données, LATU ou SFEMaNS ? Le
> palier 2D à 128² vaut-il ses heures GPU, ou faut-il passer directement à la 3D ? »

- **Pourquoi** : les campagnes configurées suivent l'escalier de l'étude (paliers 0 à 4) ; le palier 1
  complet à 128² (grille 8 × 8 en (ν, η)) est estimé à ≈ 700 h GPU de classe A100 par le plan. À lire :
  thèse §3.3 et §3.7 ; recommandation cloud §0 (« Priorités ») et §5.6.
- **Débloque** : quels calculs lancer ou louer, dans quel ordre, et si le palier 1 se fait à pleine échelle
  ou cède la place à la 3D.
- **Par défaut** : l'ordre de la recommandation cloud, M1 → M4 → M3, puis M5 à M8 : petite campagne 2D de
  contrôle (`palier1_mhd2d`, 32², 11 valeurs de η), Taylor–Green 64³, ABC 64³, puis entraînement,
  évaluation et réglage fin du générateur 3D ; pas de palier 1 à 128² ; rien sur les données des partenaires
  avant leur accord.
- [vidéo : ch10, mm:ss] — scène `10.3`
- **Décision** :

### A3. Taylor–Green : forçage, définition de Re, résolution · Q18 · P1 · Y. Ponty

> « Pour que le seuil de nos simulations Taylor–Green soit comparable aux seuils publiés (Rm_c = 30 à
> Pm = 1, Ponty et al. 2005), quel forçage et quelle définition du nombre de Reynolds faut-il adopter ? La
> grille 64³ suffit-elle à Re ≥ 100, ou faut-il 128³ à Re = 100 et 256³ à Re = 200, ou retirer Re = 200 ? »

- **Pourquoi** : le pari 2 et les données du générateur 3D viennent de cette campagne ; la configuration
  prend L_ref = 1/k_f = 0,5, U_ref = 1 et une amplitude de forçage « turbulente », d'autres échelles que les
  études publiées, et l'estimation de Kolmogorov donne k_max·η_K ≈ 0,33–0,47 à Re = 100 et 0,20–0,28 à
  Re = 200 en 64³. À lire : thèse §3.4 ; recommandation cloud §4.1 (point 4), §4.2 et §5.5.
- **Débloque** : les réglages de `palier2_tg3d` avant de louer (amplitude du forçage, définition de Re,
  grille), donc la vérification du seuil du pari 2 et les données d'entraînement 3D.
- **Par défaut** : la convention configurée (Re = U_ref L_ref/ν, Reynolds effectif lu ensuite sur u_rms) ;
  d'abord le pilote de résolution à Re = 200, Pm = 2 ; 64³ est gardé si les spectres décroissent de 3 à 4
  décades avant k_max (règle d'usage, à valider), sinon Re ≥ 100 en 64³ est étiqueté « sous-résolu,
  provisoire », Re = 100 passe en 128³ et Re = 200 en 256³ est renvoyé à Jean Zay ; la comparaison à
  Rm_c = 30 reste qualitative.
- [vidéo : ch10, mm:ss] — carte `ch10.Q`
- **Décision** :

### A4. Près du seuil : allonger les simulations, ou les exclure ? · Q24 · P1 · Y. Ponty

> « Près du seuil de Taylor–Green, faut-il allonger les simulations jusqu'à saturation, ou signaler et
> exclure celles qui ne saturent pas ? »

- **Pourquoi** : avec un germe de rms 10⁻³ et des instantanés gardés pour t entre 100 et 140, une
  simulation proche du seuil peut encore croître ; ses instantanés ne suivent alors pas une loi stationnaire
  (⟨dE/dt⟩ ≠ 0) et biaiseraient la perte de stationnarité 3D et le seuil du pari 2. À lire : rapport §3,
  « Cadre » ; thèse §4.2 (risque « variance de la perte de stationnarité trop forte en 3D »).
- **Débloque** : `t_burn` et `t_keep` près du seuil (heures GPU), le drapeau de saturation de l'extracteur,
  et les simulations qui alimentent la perte de stationnarité 3D et le pari 2.
- **Par défaut** : signaler et exclure (décision du film) : une simulation n'est retenue que si la pente de
  ln E_B sur la fenêtre gardée est proche de zéro ; aucune simulation n'est allongée.
- [vidéo : ch10, mm:ss] — scène `10.5` (et `X3.5`, version longue)
- **Décision** :

### A5. Germe minuscule, germe fort, ou les deux ? · Q2 · P1 · Y. Ponty, C. Nore

> « Près du seuil, les simulations de dynamo doivent-elles partir d'un germe minuscule, d'un germe fort, ou
> des deux ? Si les deux : faut-il redescendre depuis des champs saturés, sur quelle plage de Rm, à quel
> Pm ? »

- **Pourquoi** : près du seuil, un germe minuscule croît lentement et peut ne pas saturer pendant la
  simulation ; un germe fort peut atteindre une branche sous-critique (Ponty et al. 2007) qu'un germe
  minuscule manque. À lire : thèse §2.6 et §3.4 (conditionnement par la branche, critère (d)).
- **Débloque** : l'amplitude du germe (aujourd'hui 10⁻³), la durée des simulations Taylor–Green, et un
  éventuel étiquetage des branches dans les données.
- **Par défaut** : germe de rms 10⁻³ seulement, pas de balayage descendant, pas d'étiquette de branche : la
  région sous-critique n'est pas explorée par la première campagne.
- [vidéo : ch01, mm:ss] — carte `ch01.Q` (et `X4.4`, version longue)
- **Décision** :

### A6. Quelles valeurs de Pm ? · Q3 · P1 · Y. Ponty, C. Nore

> « Les simulations n'atteignent pas le Pm du sodium, environ 10⁻⁵ : quelles valeurs de Pm et quelle plage
> de Re les premières simulations 3D doivent-elles couvrir, et faut-il réserver toute une valeur de Pm au
> test ? »

- **Pourquoi** : le seuil Taylor–Green passe de Rm_c = 30 à Pm = 1 à 226 à Pm = 0,3 (Ponty et al. 2005) ;
  le critère (c) du palier 2 demande le seuil déduit du générateur à 10 % près à un Pm sans données, alors
  que la configuration ne réserve que deux points isolés (validation Re = 100, Pm = 1 ; test Re = 50,
  Pm = 2). À lire : thèse §3.4 ; rapport §2, « Dynamos de laboratoire et dynamos numériques ».
- **Débloque** : les valeurs de Pm et de Re de la campagne Taylor–Green, et la valeur de Pm réservée au
  test.
- **Par défaut** : Re ∈ {25, 50, 100, 200} × Pm ∈ {0,5 ; 1 ; 2} et la séparation configurée ; le critère (c)
  n'est alors pas testé, et les spectres au point de test restent un diagnostic sans critère.
- [vidéo : ch02, mm:ss] — carte `ch02.Q` (et `10.7`)
- **Décision** :

### A7. Combien d'instantanés indépendants par réglage ? · Q6 · P1 · Y. Ponty, D. Lucor

> « Combien d'instantanés indépendants faut-il pour chaque réglage, et à quel intervalle les enregistrer ?
> Faut-il passer à `n_traj: 4` dans `palier2_tg3d` ? »

- **Pourquoi** : des instantanés proches sont corrélés ; le plan vise 5 000 instantanés par point 3D
  (≈ 20 points), la campagne configurée en garde 40 par point (12 points), soit 400 échantillons
  d'entraînement et 40 instantanés de référence par point au lieu des 128 que l'évaluation demande. Sur GPU,
  `n_traj: 4` serait presque gratuit en temps (estimation non mesurée) et multiplierait les données par 4
  (≈ 12 Go). À lire : thèse §3.1 et §3.4 ; recommandation cloud §4.2.
- **Débloque** : trajectoires par point, durée gardée et intervalle entre instantanés de la campagne
  Taylor–Green, donc volume de données et heures GPU.
- **Par défaut** : la configuration actuelle (`n_traj: 1`, 40 instantanés espacés d'une unité de temps) ;
  les verdicts 3D sont alors « indicatifs » (12 × 40 instantanés, contre ≈ 20 × 5 000 dans le plan).
- [vidéo : ch04, mm:ss] — carte `ch04.Q` (et `10.7`)
- **Décision** :

### A8. Points répartis, ou resserrés près des seuils ? · Q5 · P1 · Y. Ponty, D. Lucor

> « Avec peu de simulations, faut-il répartir les valeurs des paramètres régulièrement, ou les resserrer
> près de chaque seuil ? En particulier, faut-il ajouter Rm = 17,25 ; 17,5 et 17,75 au balayage ABC ? »

- **Pourquoi** : c'est près d'un seuil que l'erreur d'un générateur régulier en Rm est la plus grande
  (propositions 2.35 et 2.36), et le plan laisse ouverte la densité des points ; à 32³, le signe de s à
  Rm = 17,5 n'est pas résolu, et la campagne 64³ ne balaie que des Rm entiers. À lire : rapport §5, E3,
  « Lecture critique » ; thèse §2.6 et §4.2 (risque « erreur incompressible près des seuils »).
- **Débloque** : les valeurs de Rm du balayage ABC à 64³ et les valeurs de Re à chaque Pm pour
  Taylor–Green.
- **Par défaut** : Rm de 4 à 40 par pas de 1, deux germes par Rm ; le pari 1 est énoncé s(17) > 0 > s(18),
  sans point entre 17 et 18 ; Re ∈ {25, 50, 100, 200} à chaque Pm.
- [vidéo : ch03, mm:ss] — carte `ch03.Q` (et `10.4`)
- **Décision** :

### A9. Terme d'oscillation, ou simulations plus longues ? · Q17 · P1 · Y. Ponty, C. Nore

> « Près des seuils ABC, faut-il ajuster les taux de croissance avec un terme d'oscillation, ou simplement
> garder chaque Rm plus longtemps ? »

- **Pourquoi** : à 32³, l'ajustement long et l'ajustement sur le dernier quart divergent aux deuxième et
  troisième seuils (jusqu'à 2·10⁻³ entre Rm = 20 et 26), sans doute parce que les modes oscillent
  (pulsation ≈ 0,53 dans la première fenêtre selon Bouya et Dormy 2013, non vérifié ici) ; or le pari 1 est
  jugé sur l'accord de ces deux ajustements. À lire : rapport §5, E3, « Lecture critique ».
- **Débloque** : `t_keep` de la campagne ABC (aujourd'hui 100 unités de temps après 150 de transitoire,
  environ huit périodes à ω ≈ 0,53), donc ses heures GPU ; l'estimateur du taux de croissance et la règle
  de verdict du pari 1. ln‖B‖ est déjà enregistré toutes les 0,5 unité de temps, assez pour l'un ou l'autre
  estimateur.
- **Par défaut** : la configuration actuelle et les deux ajustements sans terme d'oscillation ; si leurs
  signes diffèrent à Rm = 17 ou 18, le pari 1 est déclaré « non concluant ».
- [vidéo : X1, mm:ss] — carte `X1.Q`, version longue seulement (rappel dans `10.4`)
- **Décision** :

---

## B. Cadre scientifique : contraintes, mesures, critères de réussite

Les trois premières questions sont P1 : les mesures se programment avant de louer (recommandation cloud,
§4.1), faute de quoi il faudrait relancer les évaluations. Les autres fixent la représentation, les
symétries et les règles de verdict des paliers suivants.

**B.1 · Mesures et critères à programmer avant de louer**

### B1. Quelles statistiques, et à quelle distance du plancher ? · Q8 · P1 · D. Lucor, Y. Ponty, S. Cheng

> « Quelles statistiques les champs générés doivent-ils reproduire (spectres, hélicités, topologie,
> dispersion des bilans, transferts d'énergie locaux), et à quelle distance du plancher de bruit de
> Monte-Carlo parle-t-on de succès ? Faut-il une seconde simulation indépendante à chaque réglage réservé
> au test ? »

- **Pourquoi** : un score ne veut rien dire sans son plancher ; tel que configuré, le plancher 3D compare les
  deux moitiés des 40 instantanés de référence d'un point, pas des échantillons de la taille de ceux du
  score, et l'évaluation 3D n'a aucune métrique de topologie. À lire : thèse §3.1 (protocole commun et
  tableau des métriques) ; rapport §4, « Métriques » ; recommandation cloud §0 (« Mesures »).
- **Débloque** : les métriques à programmer avant de louer, les seuils de succès rapportés au plancher, et
  une éventuelle seconde simulation au point de test. Sous-question (`ETAT-DE-L-ART.md`, Q-11) : l'outil de
  transferts d'énergie locaux sur maillage non structuré de Creff et al. (2024) est-il disponible, et les
  relations kurtosis–asymétrie de Ponty, Politano et Pouquet (2025) peuvent-elles servir de critère ?
- **Par défaut** : les métriques déjà codées (divergence relative, erreur de log-spectre par bande,
  distance d'énergie et son plancher par demi-référence, hélicités, résidus moyens des bilans), plus
  σ(ε)/σ_ref, à ajouter (recommandation cloud §4.1, point 1) ; le critère (b) jugé aux seuls points
  d'entraînement ; pas de topologie en 3D.
- [vidéo : ch06, mm:ss] — carte `ch06.Q`
- **Décision** :

### B2. Quels bilans en moyenne, et leur dispersion ? · Q9 · P1 · Y. Ponty, D. Lucor

> « En 3D, quels bilans les champs générés doivent-ils respecter en moyenne (énergie, hélicité croisée,
> hélicité magnétique), et leur dispersion doit-elle aussi être celle des simulations ? »

- **Pourquoi** : imposé à chaque échantillon, un bilan réduit la loi de la dissipation à un pic qu'un score
  spectral ne voit pas (E2 : σ(ε)/σ_ref = 8,6·10⁻⁴ alors que la distance sur les descripteurs s'améliore) ;
  même imposée en loi, la perte de stationnarité a resserré la loi de dE/dt dans E1 (0,75 contre 1,04 pour
  le témoin). Le plan ne fixe aucun critère de bilan ni de dispersion en 3D, et l'évaluation 3D n'enregistre
  que des résidus moyens. À lire : rapport §3, « Stationnarité : Proposition 5, Corollaire 6 et
  Proposition 7 », et §5, E2, « Résultats » ; thèse §3.3 et §3.4.
- **Débloque** : les bilans qu'impose la perte de stationnarité 3D (l'énergie est codée ; les hélicités
  croisée et magnétique demanderaient du code), la métrique de dispersion à ajouter avant de louer, et la
  règle de verdict du réglage fin M7.
- **Par défaut** : bilan d'énergie seul ; verdict de M7 contre son témoin au même ancrage ; σ(ε)/σ_ref dans
  [0,8 ; 1,2], critère du palier 1 (2D) repris à titre indicatif, puisque le plan n'en fixe pas en 3D.
- [vidéo : ch07, mm:ss] — carte `ch07.Q`
- **Décision** :

### B3. Quelle métrique de topologie ? · Q16 · P1 · C. Nore, Y. Ponty

> « Quelles métriques de topologie jugez-vous les plus pertinentes pour les dynamos du projet : homologie
> persistante, points nuls, hélicité relative ? Sur quel champ, et quel écart du nombre de points X fait
> échouer un modèle ? »

- **Pourquoi** : l'offre de stage demande la topologie, mais le rapport n'en a calculé aucune ; le plan
  liste le nombre de points X au palier 1 sans seuil de réussite, donc tout verdict resterait non
  concluant. À lire : rapport §7, question 5 ; thèse §3.1 (famille « Topologie ») et §3.3.
- **Débloque** : le code de topologie à écrire avant de louer (points X en 2D, diagrammes de persistance et
  points nuls en 3D), le champ sur lequel il porte (|B| ou j·B), et la tolérance qui permet un verdict.
- **Par défaut** : pas de topologie en 3D pour les premières campagnes ; en 2D, le nombre de points X du
  potentiel a, avec la vérification de Poincaré–Hopf (autant de cols que d'extrema sur le tore), rapporté
  comme diagnostic sans verdict.
- [vidéo : X5a, mm:ss] — carte `X5a.Q`, version longue seulement (rappel dans `10q.3`)
- **Décision** :

**B.2 · Ce que le générateur représente et impose**

### B4. Quelles étiquettes sur chaque instantané VKS ? · Q19 · P2 · C. Nore, Y. Ponty

> « Quels paramètres de contrôle sont prioritaires pour le conditionnement : Rm (dans quelle convention),
> μ_r des turbines, asymétrie du forçage, condition de paroi, phase des turbines, ou, pour DRESDYN, le
> rapport des fréquences de précession et de rotation ? »

- **Pourquoi** : un générateur apprend ce que signifient ses étiquettes : le seuil de VKS vaut Rm_c ≈ 31
  avec le facteur d'efficacité K ≈ 0,6 (Monchaux et al. 2007) et 52 ≤ Rm_c ≤ 71 sans ce facteur (Nore et
  al. 2018) ; à Re = 1,5·10³ et μ_r = 50, la seule condition au bord fait passer le seuil simulé de 90 ± 5
  à 130 ± 10, environ 40 % de plus (Nore et al. 2018). À lire : rapport §2, « Dynamos de laboratoire et
  dynamos numériques », et §7, question 2.
- **Débloque** : le vecteur de conditionnement du palier 3 et les métadonnées de chaque instantané
  converti, donc les simulations à demander en μ_r et en condition de paroi.
- **Par défaut** : le vecteur (Re, Rm, μ_r, asymétrie) du plan de thèse, avec la convention de Rm des
  fichiers reçus écrite dans les métadonnées ; condition de paroi et phase des turbines en métadonnées, pas
  en conditionnement.
- [vidéo : X6, mm:ss] — carte `X6.Q`, version longue seulement (la question est motivée dans les deux
  versions par `03.5`)
- **Décision** :

### B5. Parois et milieu extérieur : faut-il les faire varier ? · Q4 · P2 · C. Nore, Y. Ponty

> « En plus des vitesses des turbines et du fer, quelles propriétés des parois et du milieu extérieur
> (conductivité, perméabilité) faut-il faire varier, et faut-il les ajouter au vecteur de conditionnement ? »

- **Pourquoi** : dans la plage explorée, les simulations de VKS ne se sont renversées qu'avec un milieu
  extérieur conducteur (Bousquet et al. 2026) ; les conditions aux parois déplacent le seuil de la dynamo de
  précession (Botez et al. 2026), et vide contre pseudo-vide le déplace d'environ 40 % (Nore et al. 2018).
  À lire : Encadrants, « Premières publications rattachées » ; rapport §2 ; `ETAT-DE-L-ART.md` §4 (Q-3).
- **Débloque** : la liste des paramètres des campagnes de simulation, donc leur nombre, et le vecteur de
  conditionnement.
- **Par défaut** : aucun paramètre ajouté ; parois et milieu extérieur pris tels qu'ils sont dans les
  simulations reçues, et notés en métadonnées.
- [vidéo : chSOA1, mm:ss] — scène `SOA1.4` (pas de carte)
- **Décision** :

### B6. Quelles lois exactes, pour quel opérateur discret ? · Q10 · P2 · C. Nore, Y. Ponty

> « Dans les instantanés de SFEMaNS et de LATU, quelles lois valent exactement, et pour quel opérateur
> discret ? Quelle définition discrète de la divergence et du bilan d'énergie faut-il retenir pour les
> données SFEMaNS, où ∇·B n'est contrôlée que faiblement ? »

- **Pourquoi** : les lois exactes s'intègrent au décodeur, mais « exact » dépend de l'opérateur : un
  générateur exactement solénoïdal serait plus solénoïdal que ses données SFEMaNS. À lire : rapport §7,
  question 4, et §6, « Ce qui manque pour passer aux données MilaDy » ; thèse §2.1 et §3.5.
- **Débloque** : ce que le décodeur intègre par construction (divergence, conditions aux parois et aux
  interfaces), l'opérateur qui mesure la divergence, et ce que chaque instantané stocké doit contenir pour
  la recalculer.
- **Par défaut** : le protocole du plan : divergence mesurée avec l'opérateur du solveur et comparée au
  niveau des données ; bilans recalculés sur les données avec ce même opérateur avant tout entraînement
  (feuille de route du rapport, mois 3).
- [vidéo : ch08, mm:ss] — carte `ch08.Q`
- **Décision** :

### B7. LATU ou SFEMaNS d'abord ? · Q15 · P2 · C. Nore, Y. Ponty, D. Lucor

> « Pour les premières données VKS, le générateur doit-il s'entraîner sur la grille périodique de LATU ou
> sur le maillage cylindrique de SFEMaNS ? Dans LATU, comment la pénalisation représente-t-elle les sauts
> de perméabilité et le milieu extérieur, et quelle condition de divergence est exacte sur sa grille ? »

- **Pourquoi** : LATU donne des champs pseudo-spectraux dans une boîte périodique (3π)³, cylindre et
  turbines imposés par pénalisation, où la voie périodique vers une divergence nulle s'applique ; SFEMaNS
  donne des modes de Fourier azimutaux sur un maillage méridien d'éléments finis, avec fer et raccord au
  vide, un cas qu'aucun générateur publié trouvé ne traite. À lire : rapport §6, « Ce qui manque pour passer
  aux données MilaDy » ; thèse §1.3 (question Q1) ; Encadrants, « Continuité avec le stage » ;
  `ETAT-DE-L-ART.md` §4 (Q-4).
- **Débloque** : le lecteur de données et le décodeur à écrire d'abord ; la possibilité d'ouvrir le palier 3
  au mois 15 avec le décodeur périodique pendant que le décodeur hybride se construit ; le solveur que nomme
  la première demande de données.
- **Par défaut** : LATU d'abord, « dont la grille cartésienne est la plus simple » (page Encadrants), puis
  SFEMaNS.
- [vidéo : chSOA2, mm:ss] — carte `chSOA2.Q`
- **Décision** :

### B8. Champs complets, moyennés, ou coefficients ? · Q25 · P2 · S. Cheng, C. Nore

> « Compte tenu des usages en aval (modèles réduits de type DQVU, assimilation avec TorchDA), le générateur
> doit-il produire des champs complets, des champs moyennés ou des coefficients dans une base réduite ? »

- **Pourquoi** : modèles réduits et assimilation n'utilisent pas les mêmes sorties ; le décodeur, les
  données stockées et les métriques en découlent. À lire : rapport §7, question 3 ; thèse §2.7.
- **Débloque** : l'architecture du décodeur, ce que stocke chaque instantané converti, et les métriques de
  l'évaluation.
- **Par défaut** : le plan de thèse : champs complets décodés depuis un espace latent par des potentiels,
  et énergies des quatre modes POD dominants calculées sur les champs générés (critère (a) du palier 3).
- [vidéo : ch08, mm:ss] — scène `08.7` (pas de carte ; aussi `X6.6`, version longue)
- **Décision** :

### B9. Espace latent : POD, autoencodeur polynomial ou VAE ? · Q36 · P2 · D. Lucor

> « Pour un générateur latent, faut-il partir d'une base POD, d'autoencodeurs polynomiaux initialisés comme
> la POD, ou d'un autoencodeur variationnel ? »

- **Pourquoi** : Bousquet, Nore et Lucor (2025) observent qu'une régularisation plus forte du VAE dégrade la
  reconstruction ; des autoencodeurs polynomiaux équivalents à la POD à l'initialisation s'entraînent
  environ dix fois plus vite en époques sur un écoulement de cylindre oscillant (préprint de 2026, non
  évalué) ; l'hypothèse H2 du plan sur le coût d'un modèle latent n'est pas vérifiée. À lire : thèse §3.7
  (H2) ; `ETAT-DE-L-ART.md` §2.4 et §4 (Q-12).
- **Débloque** : la représentation des paliers 1 à 3.
- **Par défaut** : le plan de thèse : autoencodeur fonctionnel de type FunDiff, avec la POD (tirage
  gaussien des coefficients) et les autoencodeurs de Bousquet, Nore et Lucor (2025) comme méthodes de
  comparaison.
- [vidéo : chSOA2, mm:ss] — scène `SOA2.6` (pas de carte)
- **Décision** :

### B10. Un seul signe de l'asymétrie de forçage ? · Q11 · P3 · C. Nore, Y. Ponty

> « Peut-on ne simuler qu'un seul signe de l'asymétrie de forçage, et laisser l'échange des turbines (la
> symétrie R_π) fournir l'autre ? Turbines, matériaux et maillage méridien sont-ils vraiment symétriques par
> cet échange ? »

- **Pourquoi** : intégrée au réseau, l'action conjointe de R_π fait de la loi à asymétrie négative l'image
  exacte de la loi à asymétrie positive, de quoi diviser par deux les simulations d'asymétrie, si le
  dispositif simulé est réellement symétrique. À lire : thèse §2.4 ; rapport §3, « Symétrie : Proposition 4 ».
- **Débloque** : un seul signe ou les deux dans le balayage d'asymétrie ; les symétries que le générateur
  intègre (deux ou quatre passes du réseau) ; la symétrie exigée du maillage.
- **Par défaut** : demander les deux signes quand ils existent, et se servir de l'image par R_π pour tester
  l'équivariance plutôt que pour économiser des simulations.
- [vidéo : X2, mm:ss] — carte `X2.Q`, version longue seulement
- **Décision** :

### B11. Imposer R_π, ou seulement B → −B ? · Q33 · P3 · C. Nore, D. Lucor

> « Des états publiés de von Kármán et de VKS brisent la symétrie R_π : faut-il imposer l'équivariance R_π,
> avec action conjointe sur l'asymétrie de forçage, ou seulement B → −B ? »

- **Pourquoi** : un état métastable de von Kármán brise R_π pour Re supérieur à 10⁴ (Bousquet et al. 2024),
  et dans la phase saturée de VKS la rétroaction magnétique brise la symétrie de la vitesse même en
  contra-rotation exacte (Botez et al. 2025) ; imposer une symétrie que la loi stationnaire n'a pas
  biaiserait le générateur (lecture de l'auteur). À lire : thèse §2.4 ; `ETAT-DE-L-ART.md` §4 (Q-6).
- **Débloque** : l'architecture du champ de vitesse du flow matching au palier 3.
- **Par défaut** : le plan : équivariance conjointe pour B → −B et R_π, avec l'équivariance simple ou
  conjointe en ablation, comme au palier 0.
- [vidéo : X2, mm:ss] — scène `X2.4`, version longue (aussi `SOA2.5`)
- **Décision** :

**B.3 · Renversements : ce que l'on vise, et comment on le juge**

### B12. La fréquence des renversements, ou leurs signes annonciateurs ? · Q1 · P2 · C. Nore, S. Cheng, D. Lucor

> « Les premières simulations doivent-elles viser la fréquence des renversements, ou les signes annonciateurs
> juste avant un renversement ? L'objectif (i) de MilaDy, phases de précurseur, de renversement et de
> récupération, attend-il de la thèse des précurseurs, ou la fréquence suffit-elle ? »

- **Pourquoi** : une fréquence se déduit d'instantanés et des équations (formule de Rice) ; des précurseurs
  exigent des enregistrements denses autour de chaque renversement, et une simulation en contient peu.
  À lire : thèse §1.3 et §2.5 ; Encadrants, « Résumé officiel et objectifs » ; `ETAT-DE-L-ART.md` §4 (Q-7).
- **Débloque** : la durée des simulations et la cadence de sauvegarde (instantanés espacés, ou séries denses
  autour de chaque renversement), et le périmètre de la question Q3 de la thèse.
- **Par défaut** : la fréquence, par la formule de Rice, à partir d'instantanés ; pas de précurseurs.
- [vidéo : ch00, mm:ss] — carte `ch00.Q`
- **Décision** :

### B13. Quel dipôle, et quel seuil pour un renversement ? · Q7 · P2 · C. Nore, Y. Ponty

> « Pour VKS, quel dipôle la formule de Rice doit-elle suivre, le coefficient du mode POD dipolaire ψ_D de
> Bousquet et al. (2026) ou la composante axiale du moment magnétique, et quel seuil fait d'un passage par
> zéro un renversement ? »

- **Pourquoi** : le plan propose ces deux dipôles ; Rice a besoin de u et B sur chaque instantané pour la
  dérivée du dipôle, et r₀ compte aussi les excursions, alors que le plan laisse ouvert le seuil ±a.
  À lire : thèse §2.5 et §3.5 (critère (d) du palier 3).
- **Débloque** : la série du dipôle et les champs (u et B ensemble) à demander avec les données VKS, et les
  seuils du critère (d) du palier 3.
- **Par défaut** : le coefficient de ψ_D, premier exemple du plan ; r₀ et, séparément, le taux des passages
  de ±a pour quelques seuils choisis sur un plateau, comme au palier 0.
- [vidéo : ch05, mm:ss] — carte `ch05.Q`
- **Décision** :

### B14. Quels réglages reçoivent de longues simulations ? · Q13 · P2 · C. Nore, Y. Ponty

> « Pour quels réglages faut-il des simulations assez longues pour compter les renversements, afin de
> vérifier un taux prédit, et avec quelle barre d'erreur juger ce taux : 5 %, ou un intervalle de Poisson ? »

- **Pourquoi** : un taux prédit ne se vérifie que contre un comptage : E1 a compté de 93 à 572 passages par
  réglage au-dessus du seuil, en 48 000 unités de temps par valeur de Γ ; les simulations de renversements
  en contiennent peu, et les simulations Taylor–Green configurées ne gardent que 40 unités de temps.
  À lire : rapport §5, E1, « Résultats » ; thèse §3.2, §3.5 et §4.2 (risque « trop peu de renversements »).
- **Débloque** : la durée et le nombre de trajectoires par réglage (`t_keep`, `n_traj`), les réglages qui
  reçoivent de longues simulations et ceux qui ne fournissent que des instantanés, et la barre d'erreur.
- **Par défaut** : la parade du plan : validation principale de Rice au palier 0, où la vérité est exacte ;
  pour VKS, un taux jugé par l'intervalle de confiance poissonien à 95 % du comptage simulé (critère (d) du
  palier 3) ; pas de longue simulation Taylor–Green.
- [vidéo : ch09, mm:ss] — carte `ch09.Q`
- **Décision** :

### B15. Viser aussi les temps d'attente ? · Q14 · P3 · C. Nore, Y. Ponty

> « Au-delà de la fréquence : pour VKS, faut-il aussi viser la loi des temps d'attente entre renversements,
> avec de courtes simulations SFEMaNS ou LATU lancées depuis des états générés ? Ces états sont-ils des
> départs valides ? »

- **Pourquoi** : les instantanés et les équations fixent la fréquence des passages par zéro, jamais la loi
  des temps d'attente (proposition 2.32), qui demande la dynamique ; le palier 0 la prévoit à faible coût,
  pour VKS elle coûte du temps de solveur. À lire : thèse §2.5 et §3.2.
- **Débloque** : si le palier VKS budgète de courtes simulations depuis des états générés (combien, quelle
  durée), et si les temps d'attente deviennent un critère ou restent l'affaire d'un modèle temporel.
- **Par défaut** : temps d'attente au palier 0 seulement, en intégrant le modèle depuis des états générés ;
  rien pour VKS.
- [vidéo : X4a, mm:ss] — carte `X4a.Q`, version longue seulement
- **Décision** :

### B16. Quelle largeur pour le plateau de seuils ? · Q28 · P3 · les encadrants

> « Le critère (d) du palier 0 demande que la borne de la proposition 2.30 soit serrée à 30 % près sur un
> plateau de seuils (conjecture 2.33) : quelle largeur doit avoir ce plateau ? »

- **Pourquoi** : sans largeur fixée avant les données, le critère ne permet pas de verdict. À lire : thèse
  §2.5 et §3.2.
- **Débloque** : la règle de verdict du critère (d), et la durée des simulations du palier 0 qui comptent
  les passages à plusieurs seuils.
- **Par défaut** : une largeur fixée par l'auteur et publiée avant les simulations du palier 0.
- [vidéo : X4a, mm:ss] — scène `X4.2`, version longue seulement
- **Décision** :

### B17. Juger la symétrie par un test statistique ? · Q29 · P3 · les encadrants

> « Le critère (a) du palier 0 demande une asymétrie de polarité sous le plancher de Monte-Carlo à chaque Γ ;
> or ce plancher est la moyenne de |p̂ − ½| pour une loi exactement symétrique. Faut-il plutôt un test à un
> niveau annoncé ? »

- **Pourquoi** : un modèle exactement symétrique dépasse ce plancher à environ 42 % des réglages, par graine
  (une variable demi-normale dépasse sa moyenne avec cette probabilité) ; sur dix valeurs de Γ
  indépendantes, il ne passerait le critère partout qu'avec une probabilité d'environ 0,4 %. À lire :
  rapport §5, E1, « Résultats » (plancher de l'asymétrie) ; thèse §3.2.
- **Débloque** : la règle de verdict du critère (a) : un test à un niveau annoncé, ou une marge au-dessus du
  plancher.
- **Par défaut** : un test de |p̂ − ½| sous l'hypothèse de symétrie exacte, à un niveau annoncé avant les
  données et corrigé pour le nombre de valeurs de Γ.
- [vidéo : X4a, mm:ss] — scène `X4.5`, version longue seulement
- **Décision** :

**B.4 · Repli, usages en aval, positionnement**

### B18. Quel repli si la perte de stationnarité échoue ? · Q12 · P2 · S. Cheng, D. Lucor

> « Si la perte de stationnarité échoue, quel est le repli, puisque la repondération par inclinaison
> exponentielle échoue là où le modèle est mauvais ? »

- **Pourquoi** : la règle d'arrêt du palier 0 se replie sur l'inclinaison, mais la matrice des risques du
  même plan dit que l'inclinaison seule n'est pas un repli : elle n'a amélioré aucune loi dans E1 ni dans
  E2, et dans E2 elle ne gardait qu'environ un échantillon effectif sur 500 là où le modèle était le plus
  mauvais. À lire : thèse §3.2 (« Arrêt ») et §4.2 ; rapport §5, E2, « Résultats ».
- **Débloque** : les règles d'arrêt et les ablations des paliers 0 et 1 ; le choix de budgéter plutôt un
  réglage fin ancré (terme de proximité, montée progressive du poids de la perte, trois graines) ; l'ESS/N
  comme diagnostic rapporté.
- **Par défaut** : la parade de la matrice des risques (réglage fin ancré au modèle de départ, lots plus
  grands, montée progressive du poids), l'inclinaison n'étant gardée que comme diagnostic (ESS/N) ; la règle
  d'arrêt du palier 0 serait réécrite en ce sens.
- [vidéo : X3a, mm:ss] — carte `X3a.Q`, version longue seulement
- **Décision** :

### B19. La contrainte de moment d'ordre 3 de DQVU · Q34 · P3 · C. Nore, Y. Ponty

> « Comment la conservation statistique d'un moment d'ordre 3 a-t-elle été choisie pour identifier DQVU, et
> un modèle de type DQVU identifié à partir d'instantanés générés doit-il la conserver ? »

- **Pourquoi** : DQVU a été identifié par régression de Galerkin contrainte (PySINDy), sous une identité
  quadratique de Navier–Stokes et la conservation d'un moment d'ordre 3 (Bousquet et al. 2026) : une
  contrainte sur des moyennes déjà utilisée dans le consortium (lecture de l'auteur, pas des auteurs).
  À lire : Encadrants, « Continuité avec le stage » ; thèse §1.3 (question Q4) et §2.7.
- **Débloque** : le protocole de la question Q4 de la thèse : quels invariants préserver quand on identifie
  un modèle réduit depuis un générateur.
- **Par défaut** : les mêmes contraintes que l'identification publiée, pour comparer à l'identique.
- [vidéo : chSOA1, mm:ss] — scène `SOA1.5`
- **Décision** :

### B20. Assimilation : quelles sondes, quelle méthode ? · Q35 · P3 · S. Cheng, C. Nore

> « Pour l'étude d'assimilation, quelle disposition de sondes magnétiques synthétiques viser (proche de
> celle de VKS ?), et quelle méthode de TorchDA : filtre de Kalman d'ensemble, 4D-Var latent, ou dynamique
> générative ? »

- **Pourquoi** : dans ce que le site a trouvé, aucune assimilation par diffusion n'a été appliquée à la MHD ;
  près d'un renversement, la loi a posteriori est bimodale à cause des deux polarités, ce qui biaise les
  méthodes qui la résument par une moyenne et une covariance. À lire : thèse §2.7 ; Encadrants,
  « Ouvertures : pistes C et D » ; `ETAT-DE-L-ART.md` §4 (Q-9).
- **Débloque** : la conception de l'étude d'assimilation (mois 25 à 27 du plan).
- **Par défaut** : choix reporté au début de cette étude ; aucun travail préparatoire avant.
- [vidéo : chSOA2, mm:ss] — scène `SOA2.5`
- **Décision** :

### B21. Comment situer notre résultat face à PBFM ? · Q31 · P3 · S. Cheng, D. Lucor

> « Baldan et al. (PBFM, ICLR 2026) se disent les premiers à reconnaître le compromis entre exactitude en loi
> et exactitude physique : comment formuler notre résultat sur l'incohérence d'une contrainte par
> échantillon pour un bilan stationnaire, et faut-il ajouter PBFM aux méthodes de comparaison du palier 1 ? »

- **Pourquoi** : le rapport et le plan revendiquent l'énoncé et la mesure de cette incohérence (corollaire
  6), sans citer PBFM. À lire : rapport §1, « Contributions » ; thèse §1.4 ; `ETAT-DE-L-ART.md` §3.3 et §4
  (Q-1).
- **Débloque** : le cadrage du premier article (contraintes en loi, mois 10) et les méthodes de comparaison
  du palier 1.
- **Par défaut** : citer PBFM, restreindre la revendication à l'énoncé et à la mesure pour un bilan
  stationnaire, et ajouter PBFM au palier 1 si son code est disponible.
- [vidéo : chSOA2, mm:ss] — scène `SOA2.8`
- **Décision** :

---

## C. Données et logistique

### C1. Quelles simulations des partenaires, sous quelle forme, quand ? · Q23 · P1 · C. Nore, Y. Ponty

> « Quelles simulations VKS et de précession pourrons-nous obtenir (LATU, SFEMaNS, ou les deux), pour quelles
> valeurs des paramètres, sous quelle forme (champs complets, modes de Fourier azimutaux, coefficients POD),
> avec combien d'instantanés et de renversements par configuration, et quand ? En particulier, quelles séries
> de Bousquet et al. (2026) peuvent nous être transmises ? »

- **Pourquoi** : les deux dernières marches de l'escalier demandent ces simulations, qui ne sont pas
  publiques ; chaque forme demande un lecteur et un stockage différents, aucun lecteur SFEMaNS natif n'existe
  encore, et peu de renversements par simulation donnent de larges barres d'erreur. À lire : rapport §7,
  question 1, et §6, « Ce qui manque pour passer aux données MilaDy » ; thèse §3.5 et §4.2 (risque « accès
  tardif ou partiel »).
- **Débloque** : le lecteur à écrire, le plan de stockage, le calendrier des paliers 3 et 4, et s'il faut
  attendre ces données avant de louer pour les campagnes périodiques.
- **Par défaut** : la parade du plan : demande au premier trimestre par C. Nore et Y. Ponty, paliers 0 à 2
  sur des données produites par la thèse, repli sur des simulations SFEMaNS à basse résolution, décision au
  mois 18 ; les campagnes périodiques n'attendent pas ces données.
- [vidéo : ch10, mm:ss] — scène `10.9` (et `X6.4`, version longue)
- **Décision** :

### C2. Des simulations des grandes échelles comme données d'entraînement ? · Q32 · P2 · C. Nore, Y. Ponty

> « Les simulations des grandes échelles (LES) à grand Re ou à faible Pm peuvent-elles servir à entraîner le
> générateur, et que pourrait-on alors affirmer des petites échelles générées ? »

- **Pourquoi** : un générateur hérite du Pm de ses données, et le faible Pm est un problème ouvert ; Nore
  et al. (2018, VKS, LES à grand Re) et Ponty et al. (2005, Taylor–Green, Pm de 1 à 10⁻², modèle
  lagrangien moyenné et LES) atteignent des régimes hors de portée de la simulation directe. À lire :
  Encadrants, « Caroline Nore » et « Yannick Ponty » ; `ETAT-DE-L-ART.md` §1.5 et §4 (Q-5).
- **Débloque** : les données des paliers 2 et 3 : simulations directes seulement, ou directes et LES.
- **Par défaut** : simulations directes seulement ; le faible Pm reste hors du périmètre revendiqué.
- [vidéo : chSOA2, mm:ss] — scène `SOA2.6`
- **Décision** :

### C3. Les simulations de référence : sur quelles machines ? · Q27 · P2 · C. Nore, Y. Ponty

> « Les simulations de référence, environ 2 × 10⁴ heures CPU ou plus selon les hypothèses du plan, sont hors
> du budget GPU : sur quelles machines et quelles allocations tourneraient-elles ? »

- **Pourquoi** : le budget du plan, ≈ 1,1 × 10⁴ h GPU de classe A100 (incertitude d'au moins un facteur 2),
  ne les compte pas (hypothèse H4 : ressources des laboratoires ou allocation nationale). À lire : thèse
  §3.7 ; recommandation cloud §8.4.
- **Débloque** : si ces simulations utilisent les allocations des partenaires ou doivent être budgétées,
  donc le coût total du plan et la part CPU d'une demande GENCI.
- **Par défaut** : l'hypothèse H4 telle qu'écrite, sans budget propre.
- [vidéo : X5b, mm:ss] — scène `X5.5`, version longue seulement
- **Décision** :

### C4. Qui financerait les derniers mois d'une thèse ? · Q20 · P2 · S. Cheng, D. Lucor, C. Nore

> « Une thèse commencée à l'automne 2027 finirait à l'automne 2030, après la fin nominale de MilaDy
> (48 mois à partir de janvier 2026) : qui financerait ses derniers mois ? »

- **Pourquoi** : la matrice des risques du plan juge l'impact élevé et laisse la probabilité « à
  clarifier » ; l'offre de stage dit seulement qu'une thèse financée « may be offered ». À lire : thèse §4.1
  et §4.2.
- **Débloque** : si le plan de 36 mois tient tel quel ou doit être resserré (le palier 4 tombe en premier),
  et l'engagement dans la thèse.
- **Par défaut** : aucun ; le plan reste une proposition tant que ce point n'est pas clarifié.
- [vidéo : X5b, mm:ss] — carte `X5b.Q`, version longue seulement
- **Décision** :

### C5. Peut-on publier les nouveaux résultats ? · Q26 · P2 · les encadrants

> « Les résultats des calculs à venir peuvent-ils être publiés sur le site du projet et dans une mise à jour
> du film, et avec quels crédits ? »

- **Pourquoi** : le site et le film sont publics, indépendants et non validés par les encadrants ; le film
  annonce un épisode « Results update » et une version 2 quand les résultats arriveront. À lire :
  recommandation cloud §0 (« Diffusion »), §7.1 et §7.2.
- **Débloque** : si l'épisode de mise à jour et les pages du site montrent de nouveaux chiffres, et avec
  quels crédits.
- **Par défaut** : rien de nouveau n'est publié sans votre accord ; les sièges vides du film restent vides.
- [vidéo : ch11, mm:ss] — scène `11.3` (carton de fin)
- **Décision** :

### C6. DRESDYN : combien de rapports de précession ? · Q30 · P3 · C. Nore, Y. Ponty

> « Pour DRESDYN, combien de rapports de précession seront simulés, et avec quel espacement ? Les champs de
> vitesse moyennés de Botez et al. (2026) seront-ils accessibles, et où en est l'expérience ? »

- **Pourquoi** : le critère (a) du palier 4 demande le seuil à 10 % près pour un nombre de Poincaré sans
  données, à l'intérieur d'une branche ; avec peu de valeurs, aucune ne peut être réservée au test. À lire :
  thèse §3.6 et §3.7 ; `ETAT-DE-L-ART.md` §4 (Q-10).
- **Débloque** : si le palier 4 peut être testé, sa séparation entre entraînement et test, et sa part du
  budget (≈ 1 200 h GPU).
- **Par défaut** : la règle d'arrêt du plan : sous environ cinq valeurs de Po, une étude d'interpolation
  sur une branche ; palier 4 abandonné en premier en cas de retard.
- [vidéo : X6, mm:ss] — scène `X6.5`, version longue seulement (rappel dans `10.9`)
- **Décision** :

### C7. Veille bibliographique et premier article · Q37 · P3 · les encadrants

> « Qui assure la veille bibliographique, et faut-il avancer un premier article sur les contraintes en loi
> (paliers 0 et 1) avant le mois 10 ? »

- **Pourquoi** : plusieurs groupes ont publié sur des sujets voisins en 2025 et 2026 ; le plan classe
  « antériorité rattrapée » parmi les risques et y répond par une veille avant chaque soumission et un
  premier article dès le mois 10. À lire : thèse §4.2 et §4.4 ; `ETAT-DE-L-ART.md` §3.4.
- **Débloque** : l'ordre des articles et la première échéance.
- **Par défaut** : le plan tel qu'écrit : veille avant chaque soumission, premier article au mois 10.
- [vidéo : chSOA2, mm:ss] — scène `SOA2.8`
- **Décision** :

---

## Proposition d'ordre du jour : première réunion de 45 minutes

**Objectif.** Sortir avec une décision sur les 13 questions P1, ou, pour chacune, le nom de la personne qui
tranchera et une date. Les questions P2 et P3 partent ensuite par écrit.

**Avant la réunion** (une semaine avant, par courriel) : cette fiche, en signalant les questions P1 ; le
lien du chapitre « Before we compute » [vidéo : ch10q, mm:ss] ; le tableau de budget de la recommandation
cloud (§1).

| Minutes | Sujet | Questions | Surtout pour |
|---|---|---|---|
| 0–5 | Le cadre : ce qui existe (site, rapport prospectif, E1 à E3 sur processeur, proposition de thèse indépendante, chaîne jamais exécutée sur GPU) et ce qui est demandé (des décisions avant tout calcul ; un classement qui n'est qu'une proposition) | — | tous |
| 5–13 | Où calculer, et quoi d'abord | Q21, Q22 | S. Cheng, D. Lucor |
| 13–25 | Paramètres de la campagne Taylor–Green | Q18, Q24, Q2, Q3, Q6 | Y. Ponty, C. Nore |
| 25–30 | Balayage ABC près des seuils | Q5, Q17 | Y. Ponty |
| 30–38 | Mesures et critères à programmer avant de louer | Q8, Q9, Q16 | D. Lucor, S. Cheng, Y. Ponty |
| 38–42 | Données des partenaires : demande et calendrier | Q23 | C. Nore, Y. Ponty |
| 42–45 | Relevé des décisions ; publication des résultats (Q26) ; qui répond aux questions P2 et P3, par écrit ; date de la réunion suivante | Q26 | tous |

**Si le temps manque.** Q5 et Q17 peuvent passer par courriel (elles ne touchent que la campagne ABC, la
moins chère) ; Q16 se traite avec Q8. Ne pas sacrifier Q21 ni Q23 : la première peut rendre la location
inutile, la seconde fixe le calendrier des paliers 3 et 4.

**Après la réunion.**

- Remplir les lignes « Décision » et renvoyer la fiche aux encadrants pour confirmation.
- Reporter les décisions dans une copie des configurations (`palier2_tg3d`, `palier2_abc3d`) et dans le
  courriel prévu au §4.2 de la recommandation cloud ; ne louer qu'ensuite, et seulement si Q21 laisse la
  location utile.
- Envoyer par écrit les questions P2 (Q1, Q4, Q7, Q10, Q12, Q13, Q15, Q19, Q20, Q25, Q27, Q32, Q36) et P3
  (Q11, Q14, Q28, Q29, Q30, Q31, Q33, Q34, Q35, Q37), groupées comme dans cette fiche.
- Après le rendu final du film, remplir les repères `[vidéo : …, mm:ss]` à partir de
  `video/script/_build/*_cues.json`.
