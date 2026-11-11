# Épisode 01 : traitement

Module rattaché : `site/prep/p1-calcul-vectoriel/index.qmd`, « Calcul vectoriel et analyse de Fourier ».
Durée visée : 14 min, soit environ 2 100 mots de narration à 150 mots par minute.
Spectateur : fin de L1, premier épisode du film, aucun module ni épisode avant celui-ci.

Fil de l'épisode : lire un champ de flèches avec deux questions locales, « est-ce que ça sort ? » et « est-ce que ça tourne ? », passer du petit cercle au domaine entier, puis du plan à l'espace, en déduire ce qu'interdit l'équation $\nabla\cdot\mathbf{B} = 0$, puis montrer qu'on peut fabriquer des champs, vitesse comme champ magnétique, qui la respectent d'office. L'épisode ne traite que le chapitre 1 en partie, le chapitre 3 en partie et la section 4.1 ; Fourier et la projection restent au texte.

## 1. Objectifs de l'épisode

Objectifs du module traités, dans la part indiquée :

- **Objectif 1**, en partie : gradient, divergence et rotationnel en coordonnées cartésiennes, surtout en 2D, avec leur sens physique. Pas les coordonnées cylindriques, pas le laplacien, que l'épisode nomme au plus.
- **Objectif 3**, en grande partie : le théorème de Green–Ostrogradski et celui de Stokes, compris comme « l'addition des petits cercles », et le sens de $\nabla\cdot\mathbf{B} = 0$ : pas de monopôle magnétique. Le calcul effectif d'un flux ou d'une circulation reste aux exercices.
- **Objectif 4**, en partie : la fonction de courant en 2D, qui donne un champ à divergence nulle par construction, et son analogue magnétique en 2D, $\mathbf{B} = \nabla^\perp a$. Pas le potentiel vecteur en 3D, pas la jauge de Coulomb.

Objectifs 2, 5, 6 et 7 : laissés au texte du module (voir la section 5).

À la fin de la vidéo, l'apprenant saura :

1. dire ce qu'est le flux à travers un cercle, la somme des composantes des flèches perpendiculaires au bord, comptées positivement vers l'extérieur ; dire ce que mesure la divergence en un point, comme le flux sortant d'un petit cercle divisé par son aire, et la calculer en 2D par $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, en sachant d'où vient chaque terme ;
2. dire ce que mesure la vorticité 2D $\omega = \partial_x u_y - \partial_y u_x$, comme la circulation sur un petit cercle parcouru dans le sens trigonométrique, divisée par son aire, et prédire si une petite roue à aubes tourne, en sachant que sa vitesse angulaire vaut $\omega/2$ ;
3. distinguer « les lignes de courant sont courbes » de « le fluide tourne sur lui-même », sur le cisaillement et le tourbillon ponctuel ;
4. expliquer pourquoi la somme des divergences multipliées par l'aire de chaque cellule égale le flux à travers le bord du domaine, transposer ce raisonnement en 3D, où le cercle devient une sphère et l'aire un volume, et en déduire qu'un champ magnétique, à divergence nulle, a un flux nul à travers toute surface fermée et des lignes de champ sans début ni fin ;
5. construire un champ 2D à divergence nulle à partir d'une fonction $\psi$, par $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, expliquer pourquoi les lignes de courant sont les lignes de niveau de $\psi$, et savoir que la même recette, $\mathbf{B} = \nabla^\perp a$, donne un champ magnétique 2D sans divergence.

## 2. La question de départ

> Devant une carte de flèches, comment savoir si elle pourrait représenter un champ magnétique ?

L'épisode s'ouvre sur deux cartes de flèches côte à côte, d'allure voisine : l'une est le champ d'une charge ponctuelle, l'autre celui d'un petit aimant. Le spectateur ne sait pas encore les distinguer. La réponse arrive en trois temps : on apprend à lire localement ce qui sort et ce qui tourne (idées 1 et 2), on passe du local au global, puis du plan à l'espace (idée 3), et on découvre qu'on peut construire des champs, vitesses comme champs magnétiques, qui passent le test à coup sûr (idée 4). Cette question prépare aussi, sans l'annoncer en détail, l'objectif du parcours : juger un champ produit par une machine avec des critères physiques.

## 3. Les idées qui méritent une image

### Idée 1. La divergence : ce qui sort d'un petit cercle

**Ce qu'elle dit.** Un champ vectoriel associe une flèche à chaque point. Pour savoir si un point est une source, on l'entoure d'un petit cercle et on calcule le flux : en chaque point du bord, on ne garde de la flèche que sa composante perpendiculaire au bord, comptée positivement si elle pointe vers l'extérieur, négativement si elle pointe vers l'intérieur, et on additionne le long du cercle. On divise par l'aire du disque et on fait rétrécir le cercle : le nombre obtenu est la divergence. En 2D, elle s'écrit $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, où $\partial_x$ veut dire « dériver en $x$ en gardant $y$ fixe ». Intuition de la formule, sur un petit carré plutôt qu'un cercle : ce qui sort par le côté droit moins ce qui entre par le côté gauche, c'est l'écart de $u_x$ entre les deux côtés, donc la variation de $u_x$ en $x$ ; de même, haut moins bas donne la variation de $u_y$ en $y$ ; la somme des deux est le bilan total. Pour la source $\mathbf{u} = (x, y)$, la divergence vaut 2 partout ; pour la rotation $\mathbf{u} = (-y, x)$, elle est nulle. Un écoulement à divergence nulle ne crée ni ne détruit d'aire en 2D, ni de volume en 3D : il est incompressible.

**L'image.** D'abord une flèche isolée posée sur le cercle en tirets, décomposée en deux : sa part perpendiculaire au bord, qui compte, et sa part le long du bord, qui ne compte pas pour le flux. Puis un petit carré, avec les flèches entrante à gauche et sortante à droite de longueurs différentes, pour faire voir le terme $\partial_x u_x$, puis le même geste en haut et en bas pour $\partial_y u_y$. Ensuite le cercle « promené », avec à côté le compteur « flux sortant divisé par l'aire » :

- centré sur l'origine, dans la source, toutes les flèches traversent le cercle vers l'extérieur ; dans la rotation, elles longent le cercle sans le traverser ;
- déplacé loin de l'origine, le cercle reçoit des flèches d'un côté et en laisse sortir de l'autre, dans les deux champs. Le bilan reste nul pour la rotation ; pour la source, il vaut toujours deux fois l'aire. Sur ces deux champs, le compteur affiche exactement 2 ou 0, quels que soient la position et le rayon : on le montre, et la narration dit que c'est parce que ces champs sont très simples.

La stabilisation du rapport quand le cercle rétrécit n'est pas montrée sur un champ linéaire, où elle n'a rien à montrer. On la montre avec le même geste à l'idée 2, sur l'écoulement cellulaire, pour la circulation (voir le journal, point 1). À la fin de l'idée 1, on promène le cercle une seule fois sur l'écoulement cellulaire : le compteur de flux reste à 0 partout. Le spectateur l'apprend comme une énigme, que l'idée 4 résout : ce champ a été fabriqué pour ne jamais diverger.

### Idée 2. Le rotationnel : la roue à aubes

**Ce qu'elle dit.** Même petit cercle, autre question : on parcourt le cercle dans le sens trigonométrique et on additionne la composante des flèches le long du cercle, c'est la circulation. Divisée par l'aire, à la limite, elle donne la vorticité $\omega = \partial_x u_y - \partial_y u_x$, composante selon $\mathbf{e}_z$ du rotationnel $\nabla\times\mathbf{u}$. Une petite roue à aubes posée dans l'écoulement tourne à la vitesse angulaire $\omega/2$. Dans la rotation solide $\mathbf{u} = (-y, x)$, le fluide tourne d'un bloc à la vitesse angulaire 1, la roue tourne avec lui à la même vitesse, et pourtant $\omega = 2$ : la vorticité vaut deux fois la vitesse de rotation locale. Deux surprises montrent ensuite que la vorticité n'est pas la courbure des lignes :

- dans le cisaillement $\mathbf{u} = (y, 0)$, les flèches vont vers la droite en haut et vers la gauche en bas ; les lignes de courant sont droites, et pourtant la roue tourne dans le sens des aiguilles d'une montre ($\omega = -1$, vitesse angulaire $1/2$) ;
- dans le tourbillon ponctuel, dont la vitesse est $(-y, x)/(x^2 + y^2)$ : elle tourne autour du centre et sa valeur est inversement proportionnelle à la distance au centre. Les lignes sont des cercles, et pourtant, hors du centre, la roue ne tourne pas sur elle-même. Le côté de la roue proche du centre est entraîné plus vite que le côté éloigné, ce qui tendrait à la faire tourner dans un sens ; la courbure de la trajectoire la ferait tourner dans l'autre ; les deux effets se compensent exactement. Toute la rotation de ce champ est concentrée au centre, où la formule n'a pas de sens : seul un cercle qui entoure le centre la révèle. Ce point sera repris à l'idée 3.

**L'image.** Une roue à aubes stylisée, posée successivement dans la rotation solide, le cisaillement et le tourbillon ponctuel. Dans la rotation solide, la roue colle au fluide : elle fait un tour quand le fluide fait un tour, et le compteur de vorticité affiche 2. Dans le cisaillement, les pales du haut, poussées vers la droite, vont plus vite que celles du bas, poussées vers la gauche. Dans le tourbillon ponctuel, la roue fait le tour du centre en gardant son orientation, comme une nacelle de grande roue ; les flèches de vitesse sur ses deux bords ont des longueurs visiblement différentes, la plus longue du côté du centre, pour faire voir la compensation. Contrainte pour le storyboard : ne jamais poser la roue sur le centre du tourbillon ponctuel, ni y faire rétrécir un cercle.

Enfin le cercle rétrécissant de l'idée 1 revient sur l'écoulement cellulaire, à l'intérieur d'une cellule, loin des droites qui séparent les cellules : le compteur « circulation divisée par l'aire » varie avec le rayon, puis se stabilise sur la vorticité au centre du cercle. C'est ici que la définition par la limite devient visible.

### Idée 3. Du petit au grand, du plan à l'espace : le bord raconte l'intérieur, et l'aimant n'a pas de source

**Ce qu'elle dit.** On pave un domaine plan de petites cellules. Sur un côté commun à deux cellules, ce qui sort de l'une entre dans l'autre : les deux contributions s'annulent. Quand on additionne tous les flux, il ne reste que le bord extérieur. Or le flux d'une petite cellule vaut à peu près sa divergence multipliée par son aire. La somme des divergences multipliées par l'aire de chaque cellule égale donc le flux à travers le bord : c'est le théorème de Green–Ostrogradski. Le même pavage, avec des circulations au lieu de flux, donne le théorème de Stokes, en une phrase : la somme des vorticités multipliées par l'aire de chaque cellule égale la circulation sur le bord.

Passage à l'espace, dit à voix haute : tout ce qui précède était dans le plan ; en trois dimensions, le petit cercle devient une petite sphère, l'aire devient un volume, et le bord du domaine devient une surface fermée. Le raisonnement du pavage reste le même. Appliqué au champ magnétique : $\nabla\cdot\mathbf{B} = 0$ en tout point équivaut à un flux nul à travers toute surface fermée. Une ligne de champ magnétique ne peut donc ni commencer ni finir en un point : il n'y a pas de monopôle magnétique.

Le champ d'une charge électrique ponctuelle, lui, vaut $1/R^2$ sur la sphère de rayon $R$ centrée sur la charge. L'aire de cette sphère vaut $4\pi R^2$. Le flux est le produit des deux : $4\pi$, quel que soit $R$. Pourtant, hors de la charge, la divergence de ce champ est nulle : toute la source est concentrée au point, et seule une surface qui entoure ce point la révèle ; une sphère qui ne l'entoure pas a un flux nul. C'est le même phénomène que le centre du tourbillon ponctuel de l'idée 2, pour la sortie au lieu de la rotation.

Le dipôle magnétique se définit en une phrase : c'est le champ d'un petit aimant. Ses lignes sortent par un bout de l'aimant, font le tour par l'extérieur, rentrent par l'autre bout et traversent l'aimant : elles n'ont ni début ni fin. La narration ne dit pas « les lignes se referment toujours ».

**L'image.** Un domaine plan découpé en carreaux, chaque carreau avec ses petites flèches de flux sur ses côtés ; les flèches des côtés intérieurs se neutralisent par paires et s'effacent, il ne reste que le contour. Puis une transition qui gonfle le cercle en sphère et le carreau en petit cube, pour marquer le passage à l'espace. Puis la charge ponctuelle, avec des sphères de rayons croissants : sur chacune, le champ faiblit et l'aire grandit, et le produit reste $4\pi$. Pour la charge, on reprend le panneau de gauche de `fig-monopole-dipole.png`. Pour l'aimant, on ne reprend pas le panneau de droite, dont le dipôle ponctuel donne l'impression que les lignes convergent au centre : on dessine un petit aimant étendu, ou une boucle de courant, que les lignes traversent de part en part. Les cercles en tirets de ces deux cartes sont des sphères vues en coupe, et la narration le dit : on n'y affiche aucun compteur 2D « flux divisé par l'aire », seulement les deux valeurs de la figure, $4\pi$ autour de la charge et 0 pour l'aimant. On peut maintenant répondre à la question de départ.

### Idée 4. Construire plutôt que vérifier : la fonction de courant

**Ce qu'elle dit.** Une fonction $\psi(x, y)$ se lit comme une carte topographique. Son gradient $\nabla\psi = (\partial_x\psi, \partial_y\psi)$ pointe vers la plus forte montée et coupe les lignes de niveau à angle droit. On le tourne d'un quart de tour dans le sens des aiguilles d'une montre : $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$ longe les lignes de niveau, qui deviennent les lignes de courant, avec les grandes valeurs de $\psi$ à gauche du courant. Sa divergence vaut $\partial_x\partial_y\psi - \partial_y\partial_x\psi$, et elle est nulle quel que soit $\psi$, pourvu que $\psi$ soit assez lisse, parce que l'ordre des deux dérivées ne compte pas alors. Exemple : $\psi = \sin x \sin y$ donne l'écoulement cellulaire de l'idée 1, qui ne diverge nulle part. Sa vorticité vaut $2\psi$ : les cellules où $\psi > 0$ tournent dans le sens trigonométrique, les autres dans le sens des aiguilles d'une montre.

La même recette vaut pour le champ magnétique en 2D : on part d'une fonction $a$, le potentiel magnétique, et on pose $\mathbf{B} = \nabla^\perp a$. Le champ obtenu passe le test de l'idée 3 à coup sûr. C'est ce qui referme la question de départ : au lieu de vérifier qu'une carte de flèches peut être un champ magnétique, on peut en fabriquer une qui l'est d'office.

Limite, dite en une phrase : la construction garantit que la divergence est nulle, pas que le champ ressemble à un vrai champ ; savoir juger cela est une question pour plus tard dans le parcours. La narration ne dit pas non plus que tout champ sans divergence s'obtient ainsi, ce que nuance l'exercice 9 (c).

Pour les modèles génératifs, une seule phrase à l'oral, sans nom propre : des chercheurs font dessiner $\psi$ à leur machine plutôt que la vitesse, pour la vitesse d'un fluide en deux dimensions. La référence apparaît en légende à l'écran : FunDiff, Wang et al., 2026, publié, cité au chapitre 4 du module. La voix et la légende parlent de vitesse de fluide, jamais de champ magnétique, pour ne pas laisser croire que FunDiff génère des champs magnétiques. Aucun chiffre d'expérience. L'expérience E2 du dépôt, qui compare ce mécanisme à d'autres, reste dans les renvois et les notes, pas dans la voix.

**L'image.** Une carte de lignes de niveau de $\psi = \sin x \sin y$ ; une flèche de gradient perpendiculaire à une ligne de niveau pivote d'un quart de tour dans le sens des aiguilles d'une montre et devient tangente à la ligne ; les flèches de vitesse apparaissent le long des lignes et forment les cellules alternées, comme le quatrième panneau de `fig-champs.png`. Contraintes pour le storyboard : les grandes valeurs de $\psi$ restent à gauche du sens du courant ; les cellules où $\psi > 0$ tournent dans le sens trigonométrique ; les droites $x = k\pi$ et $y = k\pi$, où $\psi = 0$, séparent les cellules. Le petit cercle de l'idée 1 repasse sur la carte, son compteur de flux reste à 0 : l'énigme est résolue. Puis la même carte, relabellisée $a$, avec des flèches de $\mathbf{B}$ : un champ magnétique 2D fabriqué sans divergence. La légende FunDiff s'affiche seulement sur la carte de vitesse.

## 4. L'enchaînement et le minutage approximatif

| Bloc | Début | Durée | Contenu |
|---|---|---|---|
| Ouverture | 0:00 | 0 min 45 | Deux cartes de flèches, charge et petit aimant, la question de départ, le plan en trois temps. |
| Idée 1 | 0:45 | 3 min | Champ vectoriel, dérivée partielle en une phrase, flux comme somme des composantes perpendiculaires, divergence ; le petit carré pour $\partial_x u_x + \partial_y u_y$ ; source et rotation, cercle promené ; incompressibilité ; l'énigme de l'écoulement cellulaire. |
| Idée 2 | 3:45 | 3 min | Circulation dans le sens trigonométrique, vorticité, roue à aubes ; rotation solide et $\omega/2$ ; cisaillement ; tourbillon ponctuel et compensation ; cercle rétrécissant sur l'écoulement cellulaire. |
| Idée 3 | 6:45 | 3 min 30 | Pavage, compensation des côtés intérieurs, Green–Ostrogradski, Stokes en une phrase ; passage à l'espace ; $\nabla\cdot\mathbf{B} = 0$ ; charge et $4\pi$, source concentrée au point ; petit aimant ; réponse à la question de départ. |
| Idée 4 | 10:15 | 3 min | Carte topographique, gradient, quart de tour, $\nabla^\perp\psi$, divergence nulle par construction ; cellules ; $\mathbf{B} = \nabla^\perp a$ ; limite de la construction ; une phrase sur les modèles génératifs. |
| Clôture | 13:15 | 0 min 45 | Récapitulatif des trois gestes, sortir, tourner, construire ; l'autre voie en une phrase concrète : partir d'un champ quelconque et lui retirer la partie qui diverge, c'est la projection, au chapitre 6 ; renvois aux exercices. Rien sur les mécanismes de génération. |
| **Total** | | **14 min** | Environ 2 100 mots. |

Les idées 1 et 2 utilisent le même objet, le petit cercle, pour deux questions : c'est le motif visuel qui relie tout l'épisode. L'idée 3 reprend ce cercle en le multipliant, puis le gonfle en sphère, et l'idée 4 le retrouve sous la forme d'un test que le champ passe d'office. L'écoulement cellulaire sert de fil : énigme à l'idée 1, limite visible à l'idée 2, solution à l'idée 4.

## 5. Ce qu'on laisse au texte du module, et pourquoi

- **Coordonnées cylindriques et laplacien vectoriel (section 1.5)** : ce sont surtout des calculs, et leur difficulté, les vecteurs de base qui tournent, se travaille mieux crayon en main. Le spectateur de L1 n'en a pas besoin pour l'intuition de l'épisode.
- **Le laplacien (proposition 1.8 (iii))** : son sens, l'écart à la moyenne locale, mérite une image, mais il ajouterait une cinquième notion ; il trouvera mieux sa place quand la diffusion entrera en jeu dans les modules suivants. L'épisode ne dit donc pas que $\omega = -\Delta\psi$, seulement que $\omega = 2\psi$ dans l'exemple.
- **Notation indicielle, Levi-Civita, identités vectorielles et formules de produits (sections 1.4 et chapitre 2, objectif 2)** : ce sont des démonstrations algébriques, qui ne passent pas à l'oral. L'épisode n'utilise qu'une conséquence, en 2D, que la divergence de $\nabla^\perp\psi$ est nulle, montrée directement.
- **Équation d'induction (section 2.3) et bilan d'énergie magnétique (section 3.4)** : elles demandent l'électromagnétisme local, que l'apprenant n'a pas encore.
- **Densité de courant $j = -\Delta a$ en MHD 2D (section 4.1)** : elle demande le laplacien, laissé au texte ; l'épisode ne garde que $\mathbf{B} = \nabla^\perp a$.
- **Potentiel vecteur, jauge de Coulomb, décomposition poloïdale–toroïdale (sections 4.2 et 4.3)** : extension 3D de l'idée 4 ; elle demande le rotationnel 3D et la notion de jauge, trop pour un premier épisode.
- **Topologie, lemme de Poincaré et champ moyen (théorème 4.2, proposition 4.5 (v), remarque 4.3)** : subtilité importante mais secondaire pour l'intuition ; elle est travaillée dans l'exercice 9 (c). L'épisode se garde seulement d'affirmer que tout champ sans divergence s'écrit $\nabla^\perp\psi$.
- **Fourier, TFD, FFT, Parseval, repliement, règle des 2/3 (chapitre 5, objectif 5)** : un bloc entier, qui mériterait sa propre vidéo si le plan du film le permet ; le survoler ici le rendrait confus.
- **Helmholtz–Hodge, projection de Leray, parois (chapitre 6, objectifs 6 et 7)** : ils reposent sur Fourier. L'épisode se contente de dire en une phrase qu'on peut aussi partir d'un champ quelconque et lui retirer la partie qui diverge, et que c'est la projection, au chapitre 6.
- **Les modèles génératifs et l'expérience E2** : l'apprenant ne connaît encore ni les modèles génératifs ni le rapport ; la voix s'en tient à une phrase simple, la référence FunDiff passe en légende, E2 reste aux notes.
- **Les blocs de code (différentiation automatique, quadratures, FFT)** : la vidéo montre ce qu'ils établissent, le texte garde le code à recopier et à exécuter.
- **Toutes les démonstrations** : l'épisode donne l'idée du pavage pour Green–Ostrogradski et Stokes ; les preuves restent au texte.

## 6. Renvois vers le module

Sections, avec leurs ancres exactes :

- `#objectifs` : objectifs 1, 3 et 4 du module ;
- `#ch1` : section 1.1 (champs, lignes de champ, dérivées partielles), section 1.2 (gradient, proposition 1.6), section 1.3 (définition 1.7, proposition 1.8, exemple 1.9 et figure `fig-champs.png`, exemple 1.16 : rotation solide, tourbillon ponctuel, fil électrique) ;
- `#ch3` : sections 3.1 et 3.2 (flux, circulation, théorème 3.4 de Green–Riemann, cas plan de Stokes, théorèmes 3.5 et 3.6, schéma interactif « flux et circulation à travers un petit cercle »), section 3.3 (proposition 3.8 et figure `fig-monopole-dipole.png`, dont seul le panneau de gauche est repris) ;
- `#ch4` : introduction du chapitre (FunDiff, Wang et al., 2026, pour la légende), section 4.1 (définition 4.4, proposition 4.5, exemple 4.6, et le paragraphe qui suit sur $\mathbf{B} = \nabla^\perp a$ en MHD 2D) ; pour les notes seulement, le renvoi de ce paragraphe à l'expérience E2 du rapport, `../../rapport/index.html#e2` ;
- `#ch6` : pour la phrase de clôture sur la projection, sans développement ;
- `#exercices` : liste ci-dessous.

Exercices à faire après la vidéo :

- **Exercice 1, « Calculs directs »**, questions (b) et (c) : divergence, rotationnel, plus grand taux de variation et sa direction.
- **Exercice 2, « La roue à aubes »**, questions (b) et (c) : le cisaillement et le tourbillon ponctuel de l'idée 2. La question (a) demande la notation indicielle, à garder pour après le chapitre 2.
- **Exercice 6, « Le champ coulombien »** : flux de la charge ponctuelle, et pourquoi un champ magnétique ne peut pas se comporter ainsi.
- **Exercice 7, « Green et Ampère »**, question (a) : l'aire d'un domaine par une circulation sur son bord.
- **Exercice 9, « Fonction de courant »**, questions (a) et (c) : débit entre deux points comme différence de $\psi$, et ce qu'une fonction de courant périodique ne peut pas représenter.

## 7. Quiz

### Quiz — questions

1. On considère les champs plans $\mathbf{u} = (x, y)$ et $\mathbf{v} = (-y, x)$. Lequel a une divergence non nulle, et lequel a une vorticité non nulle ?
2. On entoure un point d'un cercle de plus en plus petit. Vers quoi tend le flux sortant à travers ce cercle, divisé par l'aire du disque ?
3. Dans l'écoulement $\mathbf{u} = (y, 0)$, toutes les lignes de courant sont droites. Une petite roue à aubes posée dans cet écoulement tourne-t-elle ? Si oui, dans quel sens ?
4. Pourquoi l'égalité $\nabla\cdot\mathbf{B} = 0$ empêche-t-elle une ligne de champ magnétique de commencer en un point ?
5. On pose $\psi = \sin x \sin y$ et $\mathbf{u} = (\partial_y\psi, -\partial_x\psi)$. Sans développer le calcul, que vaut $\nabla\cdot\mathbf{u}$, et quelles courbes suivent les lignes de courant ?

### Quiz — réponses (à ne pas montrer à l'apprenant)

1. $\mathbf{u}$ a une divergence non nulle, égale à 2, et une vorticité nulle ; $\mathbf{v}$ a une divergence nulle et une vorticité égale à 2. Justification, les quatre calculs : $\nabla\cdot\mathbf{u} = \partial_x x + \partial_y y = 2$ ; $\omega_{\mathbf{u}} = \partial_x y - \partial_y x = 0$ ; $\nabla\cdot\mathbf{v} = \partial_x(-y) + \partial_y x = 0$ ; $\omega_{\mathbf{v}} = \partial_x x - \partial_y(-y) = 2$, d'après la définition 1.7 et l'exemple 1.9.
2. Vers la divergence du champ au centre du cercle. Justification : c'est le théorème de Green–Ostrogradski appliqué à un disque qui rétrécit (section 3.2, formule de la divergence comme limite d'un flux par unité de volume, ici d'aire).
3. Oui, dans le sens des aiguilles d'une montre, à la vitesse angulaire $1/2$. Justification : $\omega = \partial_x u_y - \partial_y u_x = -1$ ; les flèches vont vers la droite en haut et vers la gauche en bas, donc les pales du haut sont poussées vers la droite et celles du bas vers la gauche (exemple 1.9, exercice 2 (b)).
4. Si des lignes partaient d'un point sans qu'autant y arrivent, une petite sphère autour de ce point aurait un flux sortant non nul. Justification : $\nabla\cdot\mathbf{B} = 0$ partout équivaut à un flux nul à travers toute surface fermée, par le théorème de Green–Ostrogradski (proposition 3.8).
5. $\nabla\cdot\mathbf{u} = 0$, et les lignes de courant sont les lignes de niveau $\sin x \sin y = \text{cste}$ : des cellules fermées, hors des droites $x = k\pi$ et $y = k\pi$ où $\psi = 0$, qui les séparent. Justification : la divergence vaut $\partial_x\partial_y\psi - \partial_y\partial_x\psi = 0$ car l'ordre des dérivées ne compte pas, et $\mathbf{u}\cdot\nabla\psi = 0$ (proposition 4.5 (i) et (iii), exemple 4.6).

## 8. Journal des corrections

1. Idée 1, image : cercle promené réécrit. Centré, les flèches de la source traversent vers l'extérieur et celles de la rotation longent le cercle ; déplacé, des flèches entrent d'un côté et sortent de l'autre, bilan nul pour la rotation, deux fois l'aire pour la source ; compteur exactement 2 ou 0 sur ces champs linéaires. Écart à l'arbitrage, à trancher : l'écoulement cellulaire est à divergence nulle, son flux divisé par l'aire vaut 0 à tout rayon, il ne peut donc pas montrer la stabilisation du flux. La stabilisation est montrée à l'idée 2, sur la circulation de l'écoulement cellulaire, qui est non linéaire ; à l'idée 1, l'écoulement cellulaire sert d'énigme, flux nul partout. Si la session veut une stabilisation du flux, il faudrait un champ non linéaire à divergence non nulle, absent des figures du module, par exemple $\nabla(\sin x\sin y)$, à faire valider par les relecteurs.
2. Idée 3 : ajouté que la divergence du champ coulombien est nulle hors de la charge, que toute la source est concentrée au point et que seule une surface qui l'entoure la révèle ; parallèle avec le centre du tourbillon ponctuel, annoncé dès l'idée 2.
3. Idée 3 : passage explicite du plan à l'espace, dit à voix haute, le cercle devient une petite sphère et l'aire un volume ; transition visuelle cercle vers sphère ; les cercles en tirets des cartes sont dits sphères en coupe, sans compteur 2D, seulement $4\pi$ et 0.
4. Idée 3 et question de départ : le dipôle ponctuel de la figure n'est plus repris ; petit aimant étendu ou boucle de courant traversés par les lignes ; « dipôle » défini comme le champ d'un petit aimant ; « ni début ni fin » gardé, « se referment toujours » proscrit. Renvoi #ch3 précisé : seul le panneau de gauche de la figure est repris.
5. Idée 3 et objectif 4 : « la somme des divergences multipliées par l'aire de chaque cellule », de même pour les vorticités dans Stokes.
6. Idée 2 et objectif 2 : la circulation se calcule en parcourant le cercle dans le sens trigonométrique.
7. Idée 2 : tourbillon ponctuel défini par sa vitesse $(-y, x)/(x^2 + y^2)$, inversement proportionnelle à la distance au centre ; image de la compensation, côté proche du centre plus rapide ; interdiction de poser la roue ou un cercle rétrécissant sur le centre ; exemple 1.16 ajouté aux renvois #ch1.
8. Idée 4 : quart de tour dans le sens des aiguilles d'une montre ; cellules où $\psi > 0$ dans le sens trigonométrique, $\omega = 2\psi$ ; contrainte « grandes valeurs de $\psi$ à gauche du courant » conservée ; « pourvu que $\psi$ soit assez lisse » ajouté.
9. Renvois #ch3 : théorème 3.4, Green–Riemann, cas plan de Stokes, ajouté.
10. Idée 1 : un écoulement à divergence nulle conserve les aires en 2D et les volumes en 3D.
11. Idée 4 : ajouté en une phrase que la construction garantit la divergence nulle, pas la ressemblance avec un vrai champ, question renvoyée à plus tard dans le parcours ; pas d'affirmation que tout champ sans divergence s'obtient ainsi, renvoi à l'exercice 9 (c) et à la section 5 ; aucun chiffre d'expérience.
12. Idée 4, objectifs 4 et 5, question de départ : ajouté $\mathbf{B} = \nabla^\perp a$ en 2D, qui referme la question de départ ; renvoi au paragraphe suivant l'exemple 4.6 ; $j = -\Delta a$ laissé au texte.
13. Idée 1 et objectif 1 : flux défini comme la somme des composantes perpendiculaires au bord, comptées positivement vers l'extérieur ; image d'une flèche décomposée.
14. Idée 1 : intuition de $\partial_x u_x + \partial_y u_y$ sur un petit carré, droite moins gauche puis haut moins bas, avec son image.
15. Idée 2 : $\omega/2$ expliqué par la rotation solide, fluide à vitesse angulaire 1, roue collée au fluide, $\omega = 2$ ; image de la roue qui colle au fluide.
16. Idée 2 et réponse 3 du quiz : dans le cisaillement $(y, 0)$, flèches vers la droite en haut et vers la gauche en bas.
17. Idée 3 : $4\pi$ expliqué par $1/R^2$ fois $4\pi R^2$, quel que soit $R$ ; « dans les unités de l'exemple du module » retiré ; image de sphères de rayons croissants.
18. Idée 4 : à l'oral, une phrase simple sans nom propre sur les machines qui dessinent $\psi$ pour la vitesse d'un fluide 2D ; FunDiff, Wang et al., 2026, publié, en légende sur la seule carte de vitesse ; E2 retiré de la voix, gardé aux renvois et aux notes ; rien ne laisse croire que FunDiff génère des champs magnétiques. Ligne ajoutée en section 5.
19. Clôture, section 4 et section 5 : « projeter » remplacé par « partir d'un champ quelconque et lui retirer la partie qui diverge ; c'est la projection, au chapitre 6 » ; rien sur les mécanismes de génération.
20. Section 4 et en-tête : minutage 0:45, 3:00, 3:00, 3:30, 3:00, 0:45, total 14 min et environ 2 100 mots ; Stokes en une phrase.
21. Quiz : R1 donne les quatre calculs ; R4 commence par « si des lignes partaient d'un point sans qu'autant y arrivent » ; R5 dit « cellules fermées, hors des droites $x = k\pi$ et $y = k\pi$ où $\psi = 0$, qui les séparent » ; les deux blocs, questions puis réponses, sont conservés.
