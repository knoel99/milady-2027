# Épisode 02 : traitement

Titre de travail : « Le bord, l'aimant et la carte des hauteurs ».
Module rattaché : `prep/p1-calcul-vectoriel/index.qmd`, « Calcul vectoriel et analyse de Fourier ».
Durée visée : environ 11 min 50, soit environ 1 780 mots de narration à 150 mots par minute, sous le plafond de 2 000 mots.
Spectateur : fin de L1, qui a vu ep01 (flux, divergence, circulation, vorticité, roue à aubes, tourbillon ponctuel, énigme des cellules) et rien d'autre.

Fil de l'épisode : on rappelle l'énigme de ep01, le flux nul partout sur les cellules. On passe du petit cercle à toute une région par le carrelage, puis du plan à l'espace ; on en déduit ce qu'interdit $\nabla\cdot\mathbf{B} = 0$ ; on compare la charge et le petit aimant, et le spectateur répond à la question « laquelle de ces deux cartes peut être magnétique ? ». Enfin, on construit des champs sans divergence à partir d'une carte des hauteurs, la fonction de courant, ce qui résout l'énigme, et on fabrique de même un champ magnétique plan.

Cette version reprend le fond de l'ancien épisode unique, relu et corrigé trois fois (`../ep01/avant-decoupage/`). Toutes ses corrections d'exactitude sont gardées. Ce qui change : le découpage, un rythme plus lent, et une voix qui ne dicte plus aucune formule.

## 1. Objectifs de l'épisode

Objectifs du module traités, dans la part indiquée :

- **Objectif 1**, la part restante : le gradient, son sens et son lien avec les lignes de niveau.
- **Objectif 3**, en grande partie : le théorème de Green–Ostrogradski et celui de Stokes, compris comme l'addition des petits carreaux, et le sens de $\nabla\cdot\mathbf{B} = 0$ : pas de monopôle magnétique. Le calcul effectif d'un flux ou d'une circulation reste aux exercices.
- **Objectif 4**, en partie : la fonction de courant en 2D, qui donne un champ à divergence nulle par construction, et son analogue magnétique, $\mathbf{B} = \nabla^\perp a$. Pas le potentiel vecteur en 3D, pas la jauge.

Objectifs 2, 5, 6 et 7 : laissés au texte du module (voir la section 5).

À la fin de la vidéo, l'apprenant saura :

1. expliquer pourquoi la somme des divergences multipliées par l'aire de chaque carreau égale le flux à travers le bord du domaine, et de même pour les vorticités et la circulation ;
2. transposer ce raisonnement en 3D, où le cercle devient une sphère, l'aire un volume et le bord une surface fermée, et en déduire qu'un champ magnétique, à divergence nulle, a un flux nul à travers n'importe quelle surface fermée et des lignes de champ sans début ni fin ;
3. expliquer pourquoi le champ d'une charge a un flux $4\pi$ à travers toute sphère qui l'entoure, alors que sa divergence est nulle hors de la charge, et dire laquelle des deux cartes, charge ou aimant, peut être magnétique ;
4. dire ce qu'est le gradient d'une fonction de deux variables, vers la montée la plus raide, perpendiculaire aux lignes de niveau ;
5. construire un champ 2D à divergence nulle à partir d'une fonction $\psi$, par $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, expliquer pourquoi les lignes de courant sont les lignes de niveau de $\psi$, et savoir que la même recette, $\mathbf{B} = \nabla^\perp a$, donne un champ magnétique 2D sans divergence.

## 2. La question de départ

> Pourquoi le compteur de flux restait-il à zéro partout sur les cellules ?

L'épisode s'ouvre sur l'énigme laissée par ep01 : la carte des cellules, le cercle promené, le compteur de flux à zéro. Pour y répondre, on fait un détour : du petit au grand, du plan à l'espace, et par le champ magnétique, qui obéit partout à la même règle que ces cellules. Une seconde question naît en chemin, au milieu de l'épisode : devant deux cartes de flèches sans étiquette, laquelle peut être magnétique ? Le spectateur y répond lui-même, après une pause. La fonction de courant répond ensuite aux deux : on peut fabriquer des champs, vitesses comme champs magnétiques, qui ne divergent nulle part.

## 3. Les idées qui méritent une image

### Idée 1. Le bord raconte l'intérieur : Green–Ostrogradski et Stokes

**Ce qu'elle dit.** On découpe une région du plan en petits carreaux. Sur un côté commun à deux carreaux, ce qui sort de l'un entre dans l'autre : compté une fois en plus, une fois en moins, il disparaît du total. Il ne reste que les côtés posés sur le bord. Le flux d'un petit carreau vaut à peu près sa divergence fois son aire, c'est la définition vue dans ep01 ; l'approximation s'améliore avec des carreaux plus petits ; une phrase dit pourquoi la limite est exacte : quand les carreaux rapetissent, l'erreur sur chacun devient bien plus petite que son aire, et leur somme disparaît. La somme des divergences multipliées par l'aire de chaque carreau égale alors le flux à travers le bord. C'est le théorème de Green–Ostrogradski. Avec les circulations, deux carreaux voisins parcourent leur côté commun dans des sens contraires : même compensation. Une phrase rappelle que la circulation d'un petit carreau vaut à peu près sa vorticité fois son aire, vu dans ep01. C'est le théorème de Stokes dans le plan. Dans les deux cas, « le bord raconte l'intérieur ».

Retour au tourbillon ponctuel de ep01, par l'anneau carrelé entre deux cercles qui entourent le centre. Le bord de l'anneau, ce sont les deux cercles ; les carreaux longent le grand dans le sens trigonométrique et le petit dans le sens horaire. La circulation sur ce bord vaut donc celle du grand cercle moins celle du petit. Or la vorticité est nulle dans tout l'anneau, vu dans ep01 : la différence vaut zéro, les deux cercles ont la même circulation. Toute la rotation vient du centre, que chaque cercle compte en entier. C'est la raison de ce que ep01 avait seulement montré.

**L'image.** Deux carreaux voisins, flèches opposées sur le côté commun qui s'effacent. Le carrelage complet, les côtés intérieurs s'effacent par paires, il ne reste que le contour. Les carreaux se subdivisent. Les deux énoncés en mots, puis en formule ; sous l'énoncé de Stokes : « bord parcouru en gardant la région à sa gauche, sens trigonométrique pour une région sans trou ». L'anneau carrelé entre deux cercles du tourbillon, sens trigonométrique sur le grand cercle, sens horaire sur le petit, et « circulation(grand) − circulation(petit) = 0 ».

**Contraintes.** Aucun cercle ne rétrécit sur le centre du tourbillon. Les carreaux sont parcourus dans le sens trigonométrique. Le bord d'une région est parcouru en la gardant à sa gauche : pour l'anneau, le petit cercle est donc parcouru dans le sens horaire. Énoncés à l'écran, conformes à `specs/notations.md` (domaine $\Omega$, bord $\partial\Omega$, normale sortante $\mathbf{n}$).

### Idée 2. Du plan à l'espace : le champ magnétique n'a pas de source

**Ce qu'elle dit.** Passage à l'espace, dit à voix haute : le petit cercle devient une petite sphère, l'aire un volume, le carreau un petit cube, le bord une surface fermée, la peau d'un ballon. Le raisonnement ne change pas. Le champ magnétique, celui qui oriente l'aiguille d'une boussole, a une divergence nulle en tout point ; la voix dit que c'est une loi de la physique, admise ici. Par le carrelage, cela équivaut à un flux nul à travers n'importe quelle surface fermée. « Ligne de champ » est défini ici, à sa première utilité : une courbe qui suit partout les flèches du champ, la ligne de courant de ep01 quand le champ est une vitesse. Une phrase annonce dès ce moment que les lignes d'un aimant le traversent de part en part, pour que « sortent par un bout » ne sonne pas plus loin comme une source. Un point d'où partiraient plus de lignes qu'il n'en arrive aurait un petit ballon de flux non nul : aucun point ne peut être le départ ou l'arrivée d'une gerbe de lignes ; un tel point serait un monopôle, et il n'en existe pas.

Le champ d'une charge : sur une sphère centrée, il traverse bien en face, avec la même intensité partout, qui diminue comme un sur le carré du rayon ; l'aire de la sphère grandit comme le carré du rayon ; le produit ne dépend pas du rayon et vaut $4\pi$, dans des unités choisies pour que l'intensité vaille $1/R^2$. Dit en mots, lentement, une notion par phrase : l'intensité faiblit, divisée par quatre quand le rayon double ; l'aire grandit, multipliée par quatre ; le produit reste le même, quatre pi. Aussitôt après : hors de la charge, la divergence est nulle : toute la source est concentrée au point, seule une sphère qui l'entoure la révèle, une sphère à côté a un flux nul. C'est le tourbillon ponctuel de ep01, pour ce qui sort au lieu de ce qui tourne.

Le petit aimant est un dipôle ; son champ est un champ dipolaire. Ses lignes sortent par un bout, font le tour par l'extérieur, rentrent par l'autre bout et traversent l'aimant : elles n'ont ni début ni fin. Toute sphère, qu'elle entoure l'aimant ou non, a un flux nul.

Puis la question, en deux phrases : les deux cartes côte à côte, sans étiquette ; laquelle peut montrer un champ magnétique ? Indice des sphères en coupe, pause. Le test porte sur le champ dans l'espace, pas sur le dessin : la carte de l'aimant passe, celle de la charge échoue, à cause de son point central.

**L'image.** Le cercle qui se gonfle en sphère, le carreau en cube, un ballon découpé en cubes. Un point hypothétique d'où partent des lignes, entouré d'une sphère, barré. Le panneau de gauche de `fig-monopole-dipole.png` pour la charge, avec des sphères de rayons croissants : flèches perpendiculaires à la sphère, de même longueur sur une même sphère, plus courtes sur les sphères plus grandes ; mention « unités choisies pour que l'intensité vaille 1/R² ». Une sphère à l'écart de la charge, à 0. Un petit aimant étendu, ou une boucle de courant, traversé de part en part par ses lignes. Les deux cartes côte à côte, puis les valeurs $4\pi$ et 0.

**Contraintes.** On ne reprend pas le panneau de droite de `fig-monopole-dipole.png` : le dipôle ponctuel donne l'impression que les lignes convergent au centre. Les cercles en tirets de ces cartes sont des sphères vues en coupe, et la voix le dit : aucun compteur 2D « flux divisé par l'aire », seulement $4\pi$ et 0. On ne dit jamais « les lignes se referment toujours ».

### Idée 3. Construire plutôt que vérifier : la fonction de courant

**Ce qu'elle dit.** Une carte des hauteurs, lue comme une carte de randonnée ; ce n'est pas un vrai relief, c'est un outil de calcul. Les lignes de niveau relient les points de même altitude. Le gradient pointe vers la montée la plus raide, coupe les lignes de niveau à angle droit, et s'allonge avec la pente ; ses deux composantes disent de combien on monte en allant vers la droite et vers le haut. On le tourne d'un quart de tour dans le sens horaire : il suit la ligne de niveau. Pris comme vitesse, il fait des lignes de niveau des lignes de courant, avec les grandes hauteurs à gauche du courant. La carte prend le nom de fonction de courant. La divergence de cette vitesse est la différence de deux dérivées croisées, prises dans les deux ordres ; pour une carte assez lisse, l'ordre ne compte pas, et la différence est nulle, quelle que soit la carte.

Résolution de l'énigme : une carte en boîte à œufs, $\psi = \sin x\sin y$, donne exactement les cellules de ep01. Autour d'une bosse, le fluide tourne dans le sens trigonométrique, autour d'un creux dans le sens horaire ; les droites où l'altitude vaut zéro séparent les cellules ; la vorticité vaut deux fois la fonction de courant, calcul court laissé au spectateur.

La même recette pour le champ magnétique dans le plan, après une phrase qui dit qu'on revient de l'espace au plan : une carte des hauteurs appelée le potentiel magnétique, $\mathbf{B} = \nabla^\perp a$ ; le champ obtenu est sans divergence à coup sûr, donc il peut être magnétique ; il a un flux nul à travers n'importe quel contour fermé du plan ; les lignes de niveau du potentiel sont les lignes du champ, affiché à l'écran. Au lieu de vérifier, on fabrique un champ qui est forcément sans divergence.

Limite, dite en deux phrases : la recette garantit la divergence nulle, pas la ressemblance avec un vrai champ ; une carte au hasard donne un champ sans divergence mais sans rien de réaliste ; juger cela viendra plus tard. La voix ne dit pas que tout champ sans divergence s'obtient ainsi (exercice 9 (c)).

Modèles génératifs, sans nom propre à l'oral : des chercheurs appliquent l'astuce à un écoulement simulé en deux dimensions, bien plus agité que les cellules de l'énigme ; leur machine dessine la fonction de courant ; la vitesse qu'on en tire est sans divergence par construction. Une phrase précise que, dans ce travail, l'astuce sert pour une vitesse de fluide, pas pour un champ magnétique. À l'écran, une carte de vitesse d'un fluide plan agité, illustration fabriquée pour le film, ni figure de l'article ni sortie de FunDiff. Légende : « Idée utilisée par Wang et al., FunDiff, Nature Communications, 2026 », publié, cité au chapitre 4 du module, sur la carte de vitesse seulement.

Clôture : on dit « une autre façon d'obtenir un champ sans divergence », la projection, que le module traite au chapitre 6.

**L'image.** La carte des hauteurs avec ses lignes de niveau. Une flèche de gradient, perpendiculaire à une ligne de niveau, qui pivote d'un quart de tour dans le sens horaire et devient tangente. La boîte à œufs en relief puis en lignes de niveau ; les flèches de vitesse forment les cellules alternées, comme le quatrième panneau de `fig-champs.png` ; la formule des cellules de ep01 revient en coin ; le petit cercle repasse, compteur de flux à 0. Puis la même carte renommée $a$, avec des flèches de $\mathbf{B}$, et la mention « les lignes de niveau du potentiel sont les lignes du champ ».

**Contraintes.** Les grandes valeurs de $\psi$ restent à gauche du courant ; les cellules où $\psi > 0$ tournent dans le sens trigonométrique ; les droites $x = k\pi$ et $y = k\pi$ séparent les cellules. La légende FunDiff n'apparaît que sur la carte de vitesse, jamais sur la carte de $\mathbf{B}$. Aucun chiffre d'expérience. L'expérience E2 reste aux renvois.

### Clôture

Trois idées à retenir : le bord raconte l'intérieur ; le champ magnétique a un flux nul à travers n'importe quelle surface fermée, ses lignes n'ont ni début ni fin ; une fonction de courant tournée d'un quart de tour donne un champ sans divergence. L'autre voie en une phrase concrète : partir d'un champ quelconque et lui retirer la partie qui diverge, c'est la projection, au chapitre 6. Renvoi aux exercices.

## 4. L'enchaînement et le minutage approximatif

| Bloc | Début | Durée | Contenu |
|---|---|---|---|
| Ouverture | 0:00 | 0 min 45 | Rappel de l'énigme ; le plan en trois étapes. |
| Idée 1 | 0:45 | 2 min 10 | Carrelage, compensation des côtés intérieurs, Green–Ostrogradski ; Stokes ; retour au tourbillon. |
| Idée 2 | 2:55 | 3 min 30 | Passage à l'espace ; $\nabla\cdot\mathbf{B} = 0$ ; pas de monopôle ; charge et $4\pi$, source concentrée au point ; petit aimant ; la question des deux cartes et sa réponse. |
| Idée 3 | 6:25 | 3 min 35 | Carte des hauteurs, gradient, quart de tour, fonction de courant, divergence nulle par construction ; résolution de l'énigme ; potentiel magnétique ; limite ; FunDiff en légende. |
| Clôture | 10:00 | 0 min 40 | Trois idées ; la projection en une phrase ; exercices. |
| **Total** | | **10 min 40** | Minutage d'origine, à recaler au storyboard : la narration corrigée compte environ 1 780 mots, soit 11 min 50. |

L'énigme des cellules relie les deux épisodes : posée à la fin de ep01, rappelée à l'ouverture, résolue à l'idée 3. Le tourbillon ponctuel de ep01 revient deux fois : avec le carrelage de l'anneau, puis comme écho de la charge.

## 5. Ce qu'on laisse au texte du module, et pourquoi

- **Coordonnées cylindriques et laplacien vectoriel (section 1.5)** : surtout des calculs, mieux travaillés crayon en main.
- **Le laplacien (proposition 1.8 (iii))** : une cinquième notion ; il trouvera sa place avec la diffusion. L'épisode ne dit pas que $\omega = -\Delta\psi$, seulement que $\omega = 2\psi$ dans l'exemple.
- **Notation indicielle, Levi-Civita, identités vectorielles (section 1.4, chapitre 2, objectif 2)** : démonstrations algébriques, qui ne passent pas à l'oral. L'épisode montre directement que la divergence de $\nabla^\perp\psi$ est nulle.
- **Équation d'induction (section 2.3) et bilan d'énergie magnétique (section 3.4)** : elles demandent l'électromagnétisme local.
- **Densité de courant $j = -\Delta a$ (section 4.1)** : elle demande le laplacien ; l'épisode ne garde que $\mathbf{B} = \nabla^\perp a$.
- **Potentiel vecteur 3D, jauge de Coulomb, décomposition poloïdale–toroïdale (sections 4.2 et 4.3)** : extension 3D de l'idée 3, trop pour ce niveau.
- **Topologie, lemme de Poincaré et champ moyen (théorème 4.2, proposition 4.5 (v), remarque 4.3)** : travaillés dans l'exercice 9 (c). L'épisode se garde d'affirmer que tout champ sans divergence s'écrit $\nabla^\perp\psi$.
- **Fourier, FFT, repliement (chapitre 5, objectif 5)** : un bloc entier, qui mériterait son propre épisode.
- **Helmholtz–Hodge, projection de Leray, parois (chapitre 6, objectifs 6 et 7)** : ils reposent sur Fourier ; une phrase en clôture.
- **Les modèles génératifs et l'expérience E2** : l'apprenant ne les connaît pas encore ; une phrase simple à l'oral, FunDiff en légende, E2 aux notes.
- **Les blocs de code et toutes les démonstrations** : l'épisode donne l'idée du carrelage ; les preuves restent au texte.

## 6. Renvois vers le module

Sections, avec leurs ancres exactes :

- `#objectifs` : objectifs 1 (gradient), 3 et 4 ;
- `#ch1` : section 1.1 pour les lignes de champ ; section 1.2 (gradient, proposition 1.6) ; exemple 1.16 de la section 1.5, à lire sans les formules cylindriques, pour le rappel du tourbillon ponctuel ;
- `#ch3` : sections 3.1 et 3.2 (flux, circulation, théorème 3.4 de Green–Riemann, cas plan de Stokes, théorèmes 3.5 et 3.6), section 3.3 (proposition 3.8 et figure `fig-monopole-dipole.png`, dont seul le panneau de gauche est repris) ;
- `#ch4` : introduction du chapitre (FunDiff, Wang et al., 2026, pour la légende), section 4.1 (définition 4.4, proposition 4.5, exemple 4.6, et le paragraphe qui suit sur $\mathbf{B} = \nabla^\perp a$ en MHD 2D) ; pour les notes seulement, le renvoi de ce paragraphe à l'expérience E2 du rapport, `../../rapport/index.html#e2` ;
- `#ch6` : pour la phrase de clôture sur la projection, sans développement ;
- `#exercices` : liste ci-dessous.

Exercices à faire après la vidéo :

- **Exercice 1, « Calculs directs »**, question (c) : plus grand taux de variation et sa direction, c'est-à-dire le gradient.
- **Exercice 6, « Le champ coulombien »** : flux de la charge ponctuelle, et pourquoi un champ magnétique ne peut pas se comporter ainsi.
- **Exercice 7, « Green et Ampère »**, question (a) : l'aire d'un domaine par une circulation sur son bord.
- **Exercice 9, « Fonction de courant »**, questions (a) et (c) : débit entre deux points comme différence de $\psi$, et ce qu'une fonction de courant périodique ne peut pas représenter.

## 7. Quiz

### Quiz — questions

1. On découpe une région du plan en petits carreaux et on additionne les flux sortants de tous les carreaux. Pourquoi ne reste-t-il que le flux à travers le bord de la région ?
2. Pourquoi l'égalité $\nabla\cdot\mathbf{B} = 0$ interdit-elle un point d'où partiraient plus de lignes de champ qu'il n'en arrive ?
3. Le champ d'une charge ponctuelle a une divergence nulle hors de la charge. Pourquoi son flux à travers une sphère centrée sur la charge vaut-il pourtant $4\pi$, quel que soit le rayon ?
4. On pose $\psi = \sin x \sin y$ et $\mathbf{u} = (\partial_y\psi, -\partial_x\psi)$. Sans développer le calcul, que vaut $\nabla\cdot\mathbf{u}$, et quelles courbes suivent les lignes de courant ?
5. On choisit une fonction $a$ quelconque, assez lisse, et on pose $\mathbf{B} = \nabla^\perp a$. Que garantit cette construction, et que ne garantit-elle pas ?

### Quiz — réponses (à ne pas montrer à l'apprenant)

1. Sur un côté commun à deux carreaux, ce qui sort de l'un entre dans l'autre : les deux contributions sont opposées et s'annulent. Seuls les côtés posés sur le bord n'ont pas de voisin (théorème de Green–Ostrogradski, section 3.2).
2. Si des lignes partaient d'un point sans qu'autant y arrivent, une petite sphère autour de ce point aurait un flux sortant non nul. Or $\nabla\cdot\mathbf{B} = 0$ partout équivaut à un flux nul à travers n'importe quelle surface fermée, par le théorème de Green–Ostrogradski (proposition 3.8).
3. Sur la sphère de rayon $R$, le champ est perpendiculaire à la surface et d'intensité $1/R^2$ partout ; l'aire vaut $4\pi R^2$ ; le flux est le produit, $4\pi$. La divergence nulle hors de la charge n'empêche rien : toute la source est concentrée au point, que la sphère entoure ; une sphère qui ne l'entoure pas a un flux nul (section 3.3, exercice 6).
4. $\nabla\cdot\mathbf{u} = 0$, et les lignes de courant sont les lignes de niveau $\sin x \sin y = \text{cste}$ : des cellules fermées, hors des droites $x = k\pi$ et $y = k\pi$ où $\psi = 0$, qui les séparent. La divergence vaut $\partial_x\partial_y\psi - \partial_y\partial_x\psi = 0$ car l'ordre des dérivées ne compte pas, et $\mathbf{u}\cdot\nabla\psi = 0$ (proposition 4.5 (i) et (iii), exemple 4.6).
5. Elle garantit $\nabla\cdot\mathbf{B} = 0$, donc un flux nul à travers tout contour fermé du plan. Elle ne garantit pas que $\mathbf{B}$ ressemble à un champ magnétique réel : une fonction $a$ prise au hasard donne un champ sans divergence mais sans réalisme physique (section 4.1).
