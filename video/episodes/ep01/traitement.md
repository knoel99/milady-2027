# Épisode 01 : traitement

Titre de travail : « Ce qui sort, ce qui tourne ».
Module rattaché : `site/prep/p1-calcul-vectoriel/index.qmd`, « Calcul vectoriel et analyse de Fourier ».
Durée visée : environ 12 min 15, soit environ 1 840 mots de narration à 150 mots par minute, sous le plafond de 2 000 mots.
Spectateur : fin de L1, premier épisode du film, aucun module ni épisode avant celui-ci.

Fil de l'épisode : lire une carte de flèches avec deux questions locales, « est-ce que ça sort ? » et « est-ce que ça tourne ? », posées à un seul objet, le petit cercle. L'épisode s'arrête au local, dans le plan. Il se termine sur une énigme : sur l'écoulement cellulaire, le compteur de flux reste à zéro partout. La réponse, les théorèmes intégraux, le champ magnétique et la fonction de courant sont dans ep02.

Cette version reprend le fond de l'ancien épisode unique, relu et corrigé trois fois (`avant-decoupage/`). Toutes ses corrections d'exactitude sont gardées. Ce qui change : le découpage, un rythme plus lent, et une voix qui ne dicte plus aucune formule.

## 1. Objectifs de l'épisode

Objectifs du module traités, dans la part indiquée :

- **Objectif 1**, en partie : divergence et rotationnel en coordonnées cartésiennes, en 2D, avec leur sens physique. Le gradient est pour ep02. Pas les coordonnées cylindriques, pas le laplacien.
- **Objectif 3**, seulement sa base locale : flux et circulation à travers un petit cercle. Les théorèmes eux-mêmes et le sens de $\nabla\cdot\mathbf{B} = 0$ sont dans ep02.

Objectifs 2, 4, 5, 6 et 7 : hors de cet épisode (objectif 4 dans ep02, les autres au texte, voir la section 5).

À la fin de la vidéo, l'apprenant saura :

1. dire ce qu'est le flux à travers un cercle : la somme des parts des flèches perpendiculaires au bord, comptées en plus vers l'extérieur et en moins vers l'intérieur ;
2. dire ce que mesure la divergence en un point, le flux sortant d'un petit cercle divisé par son aire, à la limite, et la calculer en 2D par $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, en sachant d'où vient chaque terme grâce au petit carré ;
3. dire ce qu'est un écoulement incompressible et pourquoi il garde les aires ;
4. dire ce que mesure la vorticité 2D $\omega = \partial_x u_y - \partial_y u_x$, la circulation sur un petit cercle parcouru dans le sens trigonométrique, divisée par son aire, à la limite, et prédire si une petite roue à aubes tourne, en sachant qu'elle tourne à $\omega/2$ ;
5. distinguer « les lignes de courant sont courbes » de « le fluide tourne sur lui-même », sur le cisaillement et le tourbillon ponctuel.

## 2. La question de départ

> Devant une carte de flèches, comment savoir ce que fait le fluide près d'un point ?

L'épisode s'ouvre sur une carte de flèches sans titre ni formule : l'écoulement cellulaire $\psi = \sin x\sin y$, que le spectateur ne connaît pas encore. On lui donne deux questions pour la lire, sortir et tourner, et un seul outil, le petit cercle. La même carte revient deux fois : à l'idée 2, pour rendre visible la limite qui se stabilise ; à la clôture, pour l'énigme du flux nul partout. Une phrase situe le but du parcours, sans rien expliquer des machines : plus tard, il faudra juger des cartes dessinées par une machine.

Les deux cartes de l'ancienne ouverture, la charge et le petit aimant, ne sont pas dans ep01. Elles vont dans ep02.

## 3. Les idées qui méritent une image

### Idée 1. Ce qui sort : le flux et la divergence

**Ce qu'elle dit.** Un champ vectoriel associe une flèche à chaque point ; c'est le seul terme défini à l'ouverture de l'idée. « Ligne de courant » n'est défini qu'à l'idée 2, au cisaillement, où il sert ; « ligne de champ » n'est pas dans ep01 et va dans ep02. Chaque flèche a une composante horizontale et une composante verticale. La dérivée partielle se dit en mots : de combien une composante change quand on avance vers la droite sans changer de hauteur, par unité de longueur. On entoure un point d'un petit cercle. En chaque point du bord, la flèche se coupe en deux morceaux : celui qui traverse le bord, qui compte, et celui qui le longe, qui ne fait rien sortir. On compte le premier en plus vers l'extérieur, en moins vers l'intérieur, et on fait la somme : c'est le flux, ce qui sort du cercle chaque seconde moins ce qui y entre. Un grand cercle enferme plus de surface, donc souvent plus de flux : on divise par l'aire, on fait rétrécir le cercle, c'est la divergence. Le robinet et la bonde sont vus de dessus, sur la table ou la carte : l'eau semble naître sous le jet, elle quitte la carte par la bonde.

La formule vient du petit carré : par le côté droit, le flux vaut la composante horizontale fois la longueur du côté ; la composante est prise en deux points, à droite et à gauche, séparés d'une longueur de côté ; le bilan droite moins gauche est l'écart de cette composante fois la longueur ; on divise par l'aire, la longueur au carré ; il reste l'écart divisé par la longueur, un taux de variation, la dérivée partielle. Même geste en bas et en haut. Chaque composante est dérivée dans sa propre direction.

Deux champs : la source $(x, y)$, de divergence 2 partout, et la rotation solide $(-y, x)$, de divergence 0. Une raison dite pour chaque dérivée : dans la source, la composante horizontale grandit d'autant qu'on avance vers la droite, la verticale d'autant qu'on monte ; dans la rotation, la composante horizontale ne change pas quand on va vers la droite, ni la verticale quand on monte. Cercle promené : centré, les flèches de la source traversent toutes vers l'extérieur, celles de la rotation longent le bord ; déplacé, dans les deux champs, des flèches entrent d'un côté et sortent de l'autre ; elles sont de même taille pour la rotation, et les sortantes l'emportent pour la source. Le compteur affiche exactement 2 ou 0, quels que soient la place et le rayon, parce que la divergence de ces champs est la même en tout point.

Incompressible : divergence nulle partout. Raison dite : chaque petit cercle rend tout ce qu'il reçoit, donc une tache de fluide transportée dans le plan garde son aire ; dans l'espace, c'est son volume qu'elle garde. La rivière illustre le cas de l'espace, pas celui du plan : chaque goutte y garde son volume, car l'eau se laisse très mal comprimer. On ne dit pas que l'eau d'une rivière garde son aire en surface.

**L'image.** Une flèche décomposée sur le cercle en tirets. Le petit carré, flèche courte à gauche, longue à droite, puis le même geste en haut et en bas. Le cercle promené sur la source et la rotation, avec le compteur « flux sortant divisé par l'aire ». Une tache transportée par un écoulement sans divergence, qui s'étire sans changer d'aire ; le réalisateur peut prendre le cisaillement de l'idée 2, encore sans nom, mais pas la rotation solide, où la tache ne se déforme pas.

**Contraintes.** Toute formule dont la voix dit le sens est affichée au même moment. La stabilisation du compteur n'est pas montrée sur les champs linéaires, où elle n'a rien à montrer.

### Idée 2. Ce qui tourne : la circulation, la vorticité et la roue à aubes

**Ce qu'elle dit.** Même cercle, parcouru dans le sens trigonométrique ; on garde cette fois le morceau qui longe le bord, en plus dans le sens du parcours, en moins contre ; la somme est la circulation. Divisée par l'aire, à la limite, elle donne la vorticité. Sa formule vient aussi du petit carré, avec les rôles croisés : la composante verticale dérivée vers la droite, moins la composante horizontale dérivée vers le haut. Dans l'espace, la vorticité devient une flèche, le rotationnel de la vitesse ; pour un écoulement plan, cette flèche est perpendiculaire à l'écran, elle en sort si la vorticité est positive et y entre sinon ; la vorticité est sa longueur comptée avec un signe.

La roue à aubes tourne à la moitié de la vorticité, énoncé suivi aussitôt de la rotation solide : le disque tourne à la vitesse de rotation 1, la roue tourne avec lui, et le compteur affiche 2. Deux surprises :

- le cisaillement $(y, 0)$ : à droite en haut, à gauche en bas, immobile sur la ligne du milieu ; « ligne de courant » est défini ici, une courbe qui suit partout les flèches de vitesse ; le fluide avance partout à l'horizontale, donc les lignes de courant sont des droites ; roue posée sur la ligne du milieu, aubes du haut poussées à droite, du bas à gauche ; sens horaire ; vorticité $-1$, roue à $1/2$ ;
- le tourbillon ponctuel : vitesse en un sur la distance au centre, lignes circulaires ; hors du centre, la roue fait le tour en gardant son orientation, comme une cabine de grande roue ; le bord proche du centre est poussé plus vite, ce qui la ferait tourner dans un sens, la courbure du trajet dans l'autre, et pour cette décroissance précise les deux effets s'annulent exactement ; la voix renvoie au calcul de l'exercice 2 (c). La vorticité est nulle partout sauf au centre, où elle n'est pas définie, car la vitesse y devient infinie : c'est là que se cache toute la rotation, et c'est pourquoi un cercle qui entoure le centre a une circulation non nulle, la même pour tout cercle ; un cercle qui ne l'entoure pas donne zéro. « Garde cette image » : ep02 la reprend avec le carrelage et la charge.

Enfin, retour à la carte du début : cercle rétrécissant dans une cellule ; le compteur « circulation divisée par l'aire » varie, puis se fixe sur la vorticité au centre du cercle. La limite devient visible.

**L'image.** La roue dans la rotation solide, collée au fluide. Le cisaillement avec la roue sur la ligne du milieu. Le tourbillon ponctuel : la roue en cabine de grande roue, deux flèches de vitesse sur ses bords, la plus longue côté centre. Plusieurs cercles autour du centre avec un compteur « circulation » sans division par l'aire, plus un cercle à l'écart qui affiche 0. Le cercle rétrécissant dans une cellule.

**Contraintes.** Ne jamais poser la roue sur le centre du tourbillon, ni y faire rétrécir un cercle. Dans le cisaillement, sens horaire. La circulation se calcule toujours dans le sens trigonométrique. Le cercle rétrécissant reste loin des droites qui séparent les cellules. Mot « aubes », jamais « pales ».

### Clôture. L'énigme des cellules

**Ce qu'elle dit.** On pose à la carte des cellules la première question : le compteur de flux reste à zéro, partout, à toute taille. Ce n'est pas un hasard. Pourquoi ? La question reste ouverte ; ep02 y répond. Récapitulatif des deux gestes, et deux rappels : le cisaillement a des lignes droites et fait pourtant tourner la roue ; loin du centre du tourbillon ponctuel, la roue ne tourne pas sur elle-même. Renvoi aux exercices. Une phrase annonce ep02 : passer du petit cercle à toute une région.

**L'image.** Le cercle promené sur les cellules, compteur de flux à 0 ; la formule $\mathbf{u} = (\sin x\cos y, -\cos x\sin y)$ en coin, jamais dite ; le mot « pourquoi ? » reste affiché.

**Contraintes.** Rien sur la fonction de courant, rien sur $\psi$ : la formule de $\psi$ n'apparaît pas dans ep01.

## 4. L'enchaînement et le minutage approximatif

| Bloc | Début | Durée | Contenu |
|---|---|---|---|
| Ouverture | 0:00 | 0 min 35 | La carte des cellules sans titre, les deux questions, le petit cercle, une phrase sur le but du parcours. |
| Idée 1 | 0:35 | 4 min 40 | Vocabulaire, dérivée partielle en mots ; flux ; divergence ; petit carré ; source et rotation ; cercle promené ; incompressibilité. |
| Idée 2 | 5:15 | 4 min 20 | Circulation, vorticité, rotationnel ; roue à aubes et rotation solide ; cisaillement ; tourbillon ponctuel et compensation ; rotation au centre ; limite visible sur les cellules. |
| Clôture | 9:35 | 1 min 10 | L'énigme du flux nul ; les deux gestes ; exercices ; annonce de ep02. |
| **Total** | | **10 min 45** | Minutage d'origine, à recaler au storyboard : la narration corrigée compte environ 1 840 mots, soit 12 min 15. |

Le temps gagné sur l'ancien épisode unique sert à ralentir : une idée par phrase, des exemples concrets (robinet, bonde d'évier, rivière), et des pauses avant les surprises.

## 5. Ce qu'on laisse au texte du module, et pourquoi

- **Gradient, théorèmes intégraux, champ magnétique, fonction de courant** : dans ep02, pas au texte seulement.
- **Coordonnées cylindriques et laplacien vectoriel (section 1.5)** : surtout des calculs, mieux travaillés crayon en main.
- **Le laplacien (proposition 1.8 (iii))** : une notion de plus, qui trouvera sa place avec la diffusion.
- **Notation indicielle, Levi-Civita, identités vectorielles (section 1.4, chapitre 2, objectif 2)** : démonstrations algébriques, qui ne passent pas à l'oral.
- **Le rotationnel 3D en détail** : nommé en une phrase ; son calcul complet est à l'exercice 1 (b).
- **Fourier, Helmholtz–Hodge, projection (chapitres 5 et 6, objectifs 5 à 7)** : un bloc entier, hors de portée d'un premier épisode.
- **Les modèles génératifs** : une phrase de but à l'ouverture, rien d'autre.
- **Les blocs de code et toutes les démonstrations** : la vidéo montre ce qu'ils établissent, le texte garde le reste.

## 6. Renvois vers le module

Sections, avec leurs ancres exactes :

- `#objectifs` : objectifs 1 et 3, dans la part indiquée ;
- `#ch1` : section 1.1 (champs, lignes de champ, dérivées partielles), section 1.3 (définition 1.7, proposition 1.8, exemple 1.9 et figure `fig-champs.png`) ; exemple 1.16 de la section 1.5, à lire sans les formules cylindriques (rotation solide, tourbillon ponctuel) ;
- `#ch3` : sections 3.1 et 3.2 pour le flux et la circulation à travers un petit cercle, et le schéma interactif « flux et circulation à travers un petit cercle » ; les théorèmes sont renvoyés à ep02 ;
- `#exercices` : liste ci-dessous.

Exercices à faire après la vidéo :

- **Exercice 1, « Calculs directs »**, question (b) : divergence et rotationnel d'un champ donné. La question (c) porte sur le gradient, après ep02.
- **Exercice 2, « La roue à aubes »**, questions (b) et (c) : le cisaillement et le tourbillon ponctuel. La question (a) demande la notation indicielle, à garder pour après le chapitre 2.

## 7. Quiz

### Quiz — questions

1. On considère les champs plans $\mathbf{u} = (x, y)$ et $\mathbf{v} = (-y, x)$. Lequel a une divergence non nulle, et lequel a une vorticité non nulle ?
2. On entoure un point d'un cercle de plus en plus petit. Vers quoi tend le flux sortant à travers ce cercle, divisé par l'aire du disque ?
3. Dans l'écoulement $\mathbf{u} = (y, 0)$, toutes les lignes de courant sont droites. Une petite roue à aubes posée dans cet écoulement tourne-t-elle ? Si oui, dans quel sens et à quelle vitesse ?
4. Dans le tourbillon ponctuel, les lignes de courant sont des cercles. Une roue posée loin du centre tourne-t-elle sur elle-même ? Où se trouve la rotation de ce champ ?
5. Un écoulement plan a une divergence nulle partout. Que devient l'aire d'une petite tache de fluide qu'il transporte, et pourquoi ?

### Quiz — réponses (à ne pas montrer à l'apprenant)

1. $\mathbf{u}$ a une divergence égale à 2 et une vorticité nulle ; $\mathbf{v}$ a une divergence nulle et une vorticité égale à 2. Les quatre calculs : $\nabla\cdot\mathbf{u} = \partial_x x + \partial_y y = 2$ ; $\omega_{\mathbf{u}} = \partial_x y - \partial_y x = 0$ ; $\nabla\cdot\mathbf{v} = \partial_x(-y) + \partial_y x = 0$ ; $\omega_{\mathbf{v}} = \partial_x x - \partial_y(-y) = 2$ (définition 1.7, exemple 1.9).
2. Vers la divergence du champ au centre du cercle. C'est la définition de la divergence comme limite d'un flux par unité d'aire (section 3.2).
3. Oui, dans le sens horaire, à la vitesse angulaire $1/2$. $\omega = \partial_x u_y - \partial_y u_x = -1$ ; les flèches vont à droite en haut et à gauche en bas, donc les aubes du haut sont poussées à droite et celles du bas à gauche (exemple 1.9, exercice 2 (b)).
4. Non : hors du centre, la vorticité est nulle et la roue garde son orientation ; l'écart de vitesse entre ses deux bords et la courbure du trajet se compensent exactement. Toute la rotation est concentrée au centre : la vorticité y est nulle partout sauf au centre, où elle n'est pas définie, et tout cercle qui l'entoure donne la même circulation (exemple 1.16 de la section 1.5, à lire sans les formules cylindriques ; exercice 2 (c)).
5. Elle garde son aire, même si elle s'étire et se déforme : chaque petit cercle rend tout ce qu'il reçoit, le flux sortant de la tache est nul (section 1.3, écoulement incompressible). Dans l'espace, c'est le volume qui se conserve, comme pour chaque goutte d'eau d'une rivière.
