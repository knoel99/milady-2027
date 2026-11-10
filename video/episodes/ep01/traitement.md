# Épisode 01 : traitement

Module rattaché : `prep/p1-calcul-vectoriel/index.qmd`, « Calcul vectoriel et analyse de Fourier ».
Durée visée : environ 13 min 30, soit près de 2 000 mots de narration à 150 mots par minute.
Spectateur : fin de L1, premier épisode du film, aucun module ni épisode avant celui-ci.

Fil de l'épisode : lire un champ de flèches avec deux questions locales, « est-ce que ça sort ? » et « est-ce que ça tourne ? », passer du petit cercle à la surface entière, en déduire ce qu'interdit l'équation $\nabla\cdot\mathbf{B} = 0$, puis montrer qu'on peut fabriquer des champs qui la respectent d'office. L'épisode ne traite que le chapitre 1 en partie, le chapitre 3 en partie et la section 4.1 ; Fourier et la projection restent au texte.

## 1. Objectifs de l'épisode

Objectifs du module traités, dans la part indiquée :

- **Objectif 1**, en partie : gradient, divergence et rotationnel en coordonnées cartésiennes, surtout en 2D, avec leur sens physique. Pas les coordonnées cylindriques, pas le laplacien, que l'épisode nomme au plus.
- **Objectif 3**, en grande partie : le théorème de Green–Ostrogradski et celui de Stokes, compris comme « l'addition des petits cercles », et le sens de $\nabla\cdot\mathbf{B} = 0$ : pas de monopôle magnétique. Le calcul effectif d'un flux ou d'une circulation reste aux exercices.
- **Objectif 4**, en partie : la fonction de courant en 2D, qui donne un champ à divergence nulle par construction. Pas le potentiel vecteur en 3D, pas la jauge de Coulomb.

Objectifs 2, 5, 6 et 7 : laissés au texte du module (voir la section 5).

À la fin de la vidéo, l'apprenant saura :

1. dire ce que mesure la divergence en un point, comme le flux sortant d'un petit cercle divisé par son aire, et la calculer en 2D par $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$ ;
2. dire ce que mesure la vorticité 2D $\omega = \partial_x u_y - \partial_y u_x$, comme la circulation sur un petit cercle divisée par son aire, et prédire si une petite roue à aubes tourne, en sachant que sa vitesse angulaire vaut $\omega/2$ ;
3. distinguer « les lignes de courant sont courbes » de « le fluide tourne sur lui-même », sur le cisaillement et le tourbillon ponctuel ;
4. expliquer pourquoi la somme des divergences dans un domaine égale le flux à travers son bord, et en déduire qu'un champ magnétique, à divergence nulle, a un flux nul à travers toute surface fermée et des lignes de champ sans début ni fin ;
5. construire un champ 2D à divergence nulle à partir d'une fonction $\psi$, par $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, et expliquer pourquoi les lignes de courant sont les lignes de niveau de $\psi$.

## 2. La question de départ

> Devant une carte de flèches, comment savoir si elle pourrait représenter un champ magnétique ?

L'épisode s'ouvre sur deux cartes de flèches côte à côte, d'allure voisine : l'une est le champ d'une charge ponctuelle, l'autre celui d'un dipôle. Le spectateur ne sait pas encore les distinguer. La réponse arrive en trois temps : on apprend à lire localement ce qui sort et ce qui tourne (idées 1 et 2), on passe du local au global (idée 3), et on découvre qu'on peut construire des champs qui passent le test à coup sûr (idée 4). Cette question prépare aussi, sans l'annoncer en détail, l'objectif du parcours : juger un champ produit par une machine avec des critères physiques.

## 3. Les idées qui méritent une image

### Idée 1. La divergence : ce qui sort d'un petit cercle

**Ce qu'elle dit.** Un champ vectoriel associe une flèche à chaque point. Pour savoir si un point est une source, on entoure ce point d'un petit cercle et on fait le bilan de ce qui sort moins ce qui entre. On divise par l'aire du cercle et on fait rétrécir le cercle : le nombre obtenu est la divergence. En 2D, elle s'écrit $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, où $\partial_x$ veut dire « dériver en $x$ en gardant $y$ fixe ». Pour la source $\mathbf{u} = (x, y)$, elle vaut 2 partout ; pour la rotation $\mathbf{u} = (-y, x)$, elle est nulle. Un écoulement à divergence nulle ne crée ni ne détruit de volume : il est incompressible.

**L'image.** Un champ de flèches, un cercle en tirets que l'on promène puis que l'on rétrécit ; à côté, le rapport « flux sortant divisé par l'aire » s'affiche et se stabilise sur la valeur de la divergence au centre, comme dans le schéma interactif du chapitre 3 du module. On passe de la source, où toutes les flèches traversent le cercle vers l'extérieur, à la rotation, où elles longent le cercle sans le traverser.

### Idée 2. Le rotationnel : la roue à aubes

**Ce qu'elle dit.** Même petit cercle, autre question : on additionne la composante des flèches le long du cercle, c'est la circulation. Divisée par l'aire, à la limite, elle donne la vorticité $\omega = \partial_x u_y - \partial_y u_x$, composante selon $\mathbf{e}_z$ du rotationnel $\nabla\times\mathbf{u}$. Une petite roue à aubes posée dans l'écoulement tourne à la vitesse angulaire $\omega/2$ : pour la rotation solide $\mathbf{u} = (-y, x)$, $\omega = 2$. Deux surprises montrent que la vorticité n'est pas la courbure des lignes : dans le cisaillement $\mathbf{u} = (y, 0)$, les lignes de courant sont droites et pourtant la roue tourne dans le sens des aiguilles d'une montre ($\omega = -1$) ; dans le tourbillon ponctuel, hors du centre, les lignes sont des cercles et pourtant la roue ne tourne pas sur elle-même.

**L'image.** Une roue à aubes stylisée, posée successivement dans la rotation solide, le cisaillement et le tourbillon ponctuel. Dans le cisaillement, les pales du haut sont poussées plus vite que celles du bas. Dans le tourbillon ponctuel, la roue fait le tour du centre en gardant son orientation, comme une nacelle de grande roue.

### Idée 3. Du petit au grand : le bord raconte l'intérieur, et l'aimant n'a pas de source

**Ce qu'elle dit.** On pave un domaine de petites cellules. Sur une face commune à deux cellules, ce qui sort de l'une entre dans l'autre : les deux contributions s'annulent. Quand on additionne tous les flux, il ne reste que le bord extérieur. La somme des divergences à l'intérieur égale donc le flux à travers le bord : c'est le théorème de Green–Ostrogradski. Le même pavage, avec des circulations au lieu de flux, donne le théorème de Stokes : la somme des vorticités égale la circulation sur le bord. Appliqué au champ magnétique : $\nabla\cdot\mathbf{B} = 0$ en tout point équivaut à un flux nul à travers toute surface fermée. Une ligne de champ magnétique ne peut donc ni commencer ni finir en un point : il n'y a pas de monopôle magnétique. Le champ d'une charge électrique, lui, a un flux de $4\pi$ à travers toute sphère qui entoure la charge, dans les unités de l'exemple du module, et nul à travers une sphère qui ne l'entoure pas.

**L'image.** Un domaine découpé en carreaux, chaque carreau avec ses petites flèches de flux sur ses faces ; les flèches des faces intérieures se neutralisent par paires et s'effacent, il ne reste que le contour. Puis retour aux deux cartes de l'ouverture, qui reprennent la figure `fig-monopole-dipole.png` du module : pour la charge, toutes les lignes sortent du cercle en tirets ; pour le dipôle, chaque ligne qui sort rentre plus loin. On peut maintenant répondre à la question de départ.

### Idée 4. Construire plutôt que vérifier : la fonction de courant

**Ce qu'elle dit.** Une fonction $\psi(x, y)$ se lit comme une carte topographique. Son gradient $\nabla\psi = (\partial_x\psi, \partial_y\psi)$ pointe vers la plus forte montée et coupe les lignes de niveau à angle droit. On le tourne d'un quart de tour : $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$ longe les lignes de niveau, qui deviennent les lignes de courant. Sa divergence vaut $\partial_x\partial_y\psi - \partial_y\partial_x\psi$, et elle est nulle quel que soit $\psi$, parce que l'ordre des deux dérivées ne compte pas. Exemple : $\psi = \sin x \sin y$ donne des cellules qui tournent alternativement dans un sens et dans l'autre. Conséquence pour la suite du parcours : une machine qui dessine $\psi$ au lieu de $\mathbf{u}$ produit un champ sans divergence, quoi qu'elle dessine. C'est une voie publiée, celle de FunDiff en 2D (Wang et al., 2026, cité au chapitre 4 du module), et l'un des mécanismes de contrainte comparés dans l'expérience E2 du dépôt.

**L'image.** Une carte de lignes de niveau de $\psi = \sin x \sin y$ ; une flèche de gradient perpendiculaire à une ligne de niveau pivote d'un quart de tour et devient tangente à la ligne ; les flèches de vitesse apparaissent le long des lignes et forment les cellules alternées, comme le quatrième panneau de `fig-champs.png`. Contrainte pour le storyboard : avec la convention du site, les grandes valeurs de $\psi$ restent à gauche du sens du courant.

## 4. L'enchaînement et le minutage approximatif

| Bloc | Début | Durée | Contenu |
|---|---|---|---|
| Ouverture | 0:00 | 1 min | Deux cartes de flèches, la question de départ, le plan en trois temps. |
| Idée 1 | 1:00 | 3 min | Champ vectoriel, dérivée partielle en une phrase, flux à travers un petit cercle, divergence ; source et rotation ; incompressibilité. |
| Idée 2 | 4:00 | 2 min 30 | Circulation, vorticité, roue à aubes ; rotation solide, puis les deux surprises : cisaillement et tourbillon ponctuel. |
| Idée 3 | 6:30 | 3 min | Pavage, compensation des faces intérieures, Green–Ostrogradski, Stokes en une phrase ; $\nabla\cdot\mathbf{B} = 0$, charge contre dipôle ; réponse à la question de départ. |
| Idée 4 | 9:30 | 3 min | Carte topographique, gradient, quart de tour, $\nabla^\perp\psi$, divergence nulle par construction ; cellules ; usage dans les modèles génératifs. |
| Clôture | 12:30 | 1 min | Récapitulatif des trois gestes (sortir, tourner, construire) ; l'autre voie, projeter, annoncée en une phrase et renvoyée au chapitre 6 ; renvois aux exercices. |
| **Total** | | **13 min 30** | Environ 2 000 mots. |

Les idées 1 et 2 utilisent le même objet, le petit cercle, pour deux questions : c'est le motif visuel qui relie tout l'épisode. L'idée 3 reprend ce cercle en le multipliant, et l'idée 4 le retrouve sous la forme d'un test que le champ passe d'office.

## 5. Ce qu'on laisse au texte du module, et pourquoi

- **Coordonnées cylindriques et laplacien vectoriel (section 1.5)** : ce sont surtout des calculs, et leur difficulté, les vecteurs de base qui tournent, se travaille mieux crayon en main. Le spectateur de L1 n'en a pas besoin pour l'intuition de l'épisode.
- **Le laplacien (proposition 1.8 (iii))** : son sens, l'écart à la moyenne locale, mérite une image, mais il ajouterait une cinquième notion ; il trouvera mieux sa place quand la diffusion entrera en jeu dans les modules suivants.
- **Notation indicielle, Levi-Civita, identités vectorielles et formules de produits (sections 1.4 et chapitre 2, objectif 2)** : ce sont des démonstrations algébriques, qui ne passent pas à l'oral. L'épisode n'utilise qu'une conséquence, en 2D, que la divergence de $\nabla^\perp\psi$ est nulle, montrée directement.
- **Équation d'induction (section 2.3) et bilan d'énergie magnétique (section 3.4)** : elles demandent l'électromagnétisme local, que l'apprenant n'a pas encore.
- **Potentiel vecteur, jauge de Coulomb, décomposition poloïdale–toroïdale (sections 4.2 et 4.3)** : extension 3D de l'idée 4 ; elle demande le rotationnel 3D et la notion de jauge, trop pour un premier épisode.
- **Topologie, lemme de Poincaré et champ moyen (théorème 4.2, remarque 4.3)** : subtilité importante mais secondaire pour l'intuition ; elle est travaillée dans l'exercice 9 (c).
- **Fourier, TFD, FFT, Parseval, repliement, règle des 2/3 (chapitre 5, objectif 5)** : un bloc entier, qui mériterait sa propre vidéo si le plan du film le permet ; le survoler ici le rendrait confus.
- **Helmholtz–Hodge, projection de Leray, parois (chapitre 6, objectifs 6 et 7)** : ils reposent sur Fourier. L'épisode se contente d'annoncer en une phrase qu'on peut aussi corriger un champ après coup, en le projetant.
- **Les blocs de code (différentiation automatique, quadratures, FFT)** : la vidéo montre ce qu'ils établissent, le texte garde le code à recopier et à exécuter.
- **Toutes les démonstrations** : l'épisode donne l'idée du pavage pour Green–Ostrogradski et Stokes ; les preuves restent au texte.

## 6. Renvois vers le module

Sections, avec leurs ancres exactes :

- `#objectifs` : objectifs 1, 3 et 4 du module ;
- `#ch1` : section 1.1 (champs, lignes de champ, dérivées partielles), section 1.2 (gradient, proposition 1.6), section 1.3 (définition 1.7, proposition 1.8, exemple 1.9 et figure `fig-champs.png`) ;
- `#ch3` : sections 3.1 et 3.2 (flux, circulation, théorèmes 3.5 et 3.6, schéma interactif « flux et circulation à travers un petit cercle »), section 3.3 (proposition 3.8 et figure `fig-monopole-dipole.png`) ;
- `#ch4` : section 4.1 (définition 4.4, proposition 4.5, exemple 4.6) ;
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

1. $\mathbf{u}$ a une divergence non nulle, égale à 2, et une vorticité nulle ; $\mathbf{v}$ a une divergence nulle et une vorticité égale à 2. Justification : $\partial_x x + \partial_y y = 2$ et $\partial_x x - \partial_y(-y) = 2$, d'après la définition 1.7 et l'exemple 1.9.
2. Vers la divergence du champ au centre du cercle. Justification : c'est le théorème de Green–Ostrogradski appliqué à un disque qui rétrécit (section 3.2, formule de la divergence comme limite d'un flux par unité de volume, ici d'aire).
3. Oui, dans le sens des aiguilles d'une montre, à la vitesse angulaire $1/2$. Justification : $\omega = \partial_x u_y - \partial_y u_x = -1$ ; les pales du haut sont poussées plus vite que celles du bas (exemple 1.9, exercice 2 (b)).
4. Si une ligne commençait en un point, une petite sphère autour de ce point aurait un flux sortant non nul. Justification : $\nabla\cdot\mathbf{B} = 0$ partout équivaut à un flux nul à travers toute surface fermée, par le théorème de Green–Ostrogradski (proposition 3.8).
5. $\nabla\cdot\mathbf{u} = 0$, et les lignes de courant sont les lignes de niveau $\sin x \sin y = \text{cste}$, qui forment des cellules fermées. Justification : la divergence vaut $\partial_x\partial_y\psi - \partial_y\partial_x\psi = 0$ car l'ordre des dérivées ne compte pas, et $\mathbf{u}\cdot\nabla\psi = 0$ (proposition 4.5 (i) et (iii), exemple 4.6).
