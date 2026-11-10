# Épisode 01 : narration

Titre de travail : « Ce qui sort, ce qui tourne ».
Module : `prep/p1-calcul-vectoriel/index.qmd`. Traitement : `video/episodes/ep01/traitement.md`.
Ton : tutoiement. Voix : environ 1 840 mots, soit 12 min 15 à 150 mots par minute.
Les lignes « > écran : » et « > légende : » ne sont pas dites. La voix ne dicte aucune formule : la formule est à l'écran, la voix dit ce qu'elle signifie.

## Ouverture

### P1

[e1-carte] Voici une carte couverte de flèches.
[e1-fleche] En chaque point, une flèche dit où va le fluide.
[e1-longueur] Plus elle est longue, plus le fluide va vite.
[e1-question] Que fait ce fluide près d'un point donné ?
[e1-deux] Pour le savoir, on va poser deux questions simples.
[e1-sort] Est-ce que ça sort ?
[e1-tourne] Est-ce que ça tourne ?

> écran : une carte de flèches, l'écoulement cellulaire, sans titre ni formule ; puis les deux questions, « est-ce que ça sort ? » et « est-ce que ça tourne ? ».

### P2

[e1-outil] Pour les deux questions, on aura le même outil : un petit cercle.
[e1-machine] Plus tard dans le film, des machines dessineront de telles cartes.
[e1-juger] Il faudra alors juger si ces cartes sont physiquement crédibles.
[e1-lire] Mais d'abord, il faut savoir les lire.

> écran : un petit cercle en tirets se pose sur la carte.

## Idée 1. Ce qui sort : la divergence

### P3

[e1-mots] On commence par trois mots.
[e1-champ] Une carte qui met une flèche en chaque point s'appelle un champ vectoriel.
[e1-composantes] Chaque flèche se décompose en deux parts.
[e1-horizontale] La composante horizontale dit de combien la flèche pousse vers la droite.
[e1-verticale] La composante verticale dit de combien elle pousse vers le haut.

> écran : avec [e1-champ], le mot « champ vectoriel » ; puis une flèche décomposée en deux parts, notées ux vers la droite et uy vers le haut ; u = (ux, uy).

### P4

[e1-change] Il faudra savoir comment une composante change quand on se déplace.
[e1-avance] Pour le mesurer, on avance vers la droite, sans changer de hauteur.
[e1-taux] On regarde de combien la composante change, par unité de longueur.
[e1-derivee] Ce taux s'appelle une dérivée partielle.
[e1-monte] On peut faire de même en montant, sans bouger vers la droite.

> écran : avec [e1-derivee], ∂x ux, sous-titré « dériver en x en gardant y fixe » ; avec [e1-monte], ∂y ux.

### P5

[e1-source] Première question : un point donné est-il une source ?
[e1-robinet] Pense à un robinet qui verse de l'eau sur une table.
[e1-ecarte] Autour de lui, l'eau s'écarte dans toutes les directions.
[e1-dessus] Sur la table, vue de dessus, l'eau semble naître sous le jet.
[e1-cercle] Pour reconnaître une source, entoure le point d'un petit cercle.
[e1-bord] Puis regarde les flèches posées sur le bord du cercle.
[e1-coupe] Chacune se coupe en deux morceaux.
[e1-traverse] Le premier morceau traverse le bord, vers l'extérieur ou vers l'intérieur.
[e1-glisse] Le second glisse le long du bord, sans le traverser.
[e1-seul] Seul le premier fait sortir ou entrer du fluide.

> écran : une flèche posée sur le cercle en tirets, décomposée en sa part perpendiculaire au bord, qui compte, et sa part le long du bord, qui ne compte pas.

### P6

[e1-plus] Si ce morceau pointe vers l'extérieur, on le compte en plus.
[e1-moins] S'il pointe vers l'intérieur, on le compte en moins.
[e1-flux] On fait la somme tout autour du cercle : c'est le flux.
[e1-sens] Le flux mesure ce qui sort du cercle chaque seconde, moins ce qui y entre.

> écran : les parts perpendiculaires au bord, marquées « + » vers l'extérieur, « − » vers l'intérieur ; le mot « flux ».

### P7

[e1-grand] Un grand cercle enferme plus de surface, donc souvent plus de flux.
[e1-aire] Alors on divise le flux par l'aire du disque.
[e1-retrecir] Puis on fait rétrécir le cercle vers le point.
[e1-divergence] Le nombre qu'on trouve à la fin s'appelle la divergence en ce point.
[e1-positive] Une divergence positive veut dire que le point fait sortir du fluide.
[e1-negative] Une divergence négative veut dire qu'il en avale.
[e1-evier] Pense cette fois à la bonde d'un évier.
[e1-quitte] Vue de dessus, l'eau y quitte la carte.
[e1-nulle] Une divergence nulle veut dire que tout ce qui entre ressort.

> écran : avec [e1-divergence], « divergence = flux sortant ÷ aire, quand le cercle rétrécit ».

### P8

[e1-formule] Pour trouver une formule, on remplace le cercle par un petit carré.
[e1-cotes] Regarde d'abord le côté gauche et le côté droit.
[e1-horiz] Par ces deux côtés, seule la composante horizontale traverse.
[e1-droit] Ce qui sort par la droite vaut cette composante, fois la longueur du côté.
[e1-gauchepareil] Ce qui entre par la gauche se calcule de la même façon.
[e1-deuxpoints] La composante est donc prise en deux points, l'un à droite, l'autre à gauche.
[e1-separes] Ces deux points sont séparés d'une longueur de côté.
[e1-ecart] Le bilan des deux côtés, c'est donc l'écart de la composante horizontale, fois la longueur.
[e1-divise] On divise par l'aire du carré, soit la longueur du côté multipliée par elle-même.
[e1-reste] Il reste l'écart divisé par la longueur : c'est un taux de variation.
[e1-dpdroite] Ce taux, c'est la dérivée partielle vers la droite.

> écran : petit carré, flèche entrante courte à gauche, flèche sortante longue à droite ; avec [e1-separes], les deux points de mesure marqués, la longueur du côté entre eux ; « flux = ux × longueur du côté », puis « ÷ aire du carré », puis ∂x ux.

### P9

[e1-hautbas] On refait le même geste en bas et en haut, avec la composante verticale.
[e1-montee] On obtient sa dérivée partielle vers le haut.
[e1-somme] La divergence est la somme de ces deux dérivées.
[e1-propre] Chaque composante est dérivée dans sa propre direction.

> écran : le même geste en bas et en haut ; avec [e1-somme], la formule ∇·u = ∂x ux + ∂y uy.

### P10

[e1-essai] Essaie cette formule sur deux champs simples.
[e1-fuit] Le premier est une source : le fluide fuit l'origine dans toutes les directions.
[e1-allonge] Ses flèches pointent vers l'extérieur et s'allongent avec la distance.
[e1-srcdroite] Avance vers la droite : la composante horizontale grandit d'autant que tu avances.
[e1-srchaut] Monte : la composante verticale grandit d'autant que tu montes.
[e1-un] Chacune des deux dérivées vaut un.
[e1-vautdeux] Sa divergence vaut donc un plus un, soit deux, partout.

> écran : avec [e1-fuit], u = (x, y), flèches qui fuient l'origine ; avec [e1-srcdroite], ∂x ux = 1 ; avec [e1-srchaut], ∂y uy = 1 ; avec [e1-vautdeux], ∇·u = 1 + 1 = 2.

### P11

[e1-bloc] Le second est une rotation : le fluide tourne autour de l'origine, d'un seul bloc.
[e1-perp] Ses flèches sont perpendiculaires au rayon, et s'allongent aussi avec la distance.
[e1-rotdroite] Va vers la droite : la composante horizontale ne change pas.
[e1-rothaut] Monte : la composante verticale ne change pas non plus.
[e1-vautzero] Ici, les deux dérivées valent donc zéro : la divergence est nulle.

> écran : avec [e1-bloc], u = (−y, x), flèches qui tournent ; avec [e1-rotdroite], ∂x ux = 0 ; avec [e1-rothaut], ∂y uy = 0 ; avec [e1-vautzero], ∇·u = 0 + 0 = 0.

### P12

[e1-centre] Centre maintenant le cercle sur l'origine.
[e1-sortent] Dans la source, toutes les flèches traversent le bord vers l'extérieur.
[e1-glissent] Dans la rotation, elles glissent le long du bord, sans le traverser.
[e1-deplace] Déplace ensuite le cercle, loin de l'origine.
[e1-entrent] Cette fois, dans les deux champs, des flèches entrent d'un côté.
[e1-ressortent] D'autres ressortent du côté opposé.

> écran : le cercle promené sur la source et sur la rotation, avec le compteur « flux sortant divisé par l'aire », qui affiche 2 ou 0.

### P13

[e1-rotbilan] Pour la rotation, les flèches qui entrent ont la même taille que celles qui sortent.
[e1-rotnul] Le bilan est nul.
[e1-srcbilan] Pour la source, les flèches qui sortent sont plus longues.
[e1-srcdeux] Le bilan vaut deux fois l'aire du disque.
[e1-compteur] Le compteur affiche donc deux pour la source, zéro pour la rotation, où que soit le cercle.
[e1-taille] Il ne dépend pas non plus de la taille du cercle.
[e1-simple] La raison : dans ces deux champs, la divergence est la même en tout point.

> écran : cercle arrêté loin de l'origine, parts perpendiculaires au bord seules : d'un côté des flèches entrantes, de l'autre des flèches sortantes ; pour la rotation, entrantes et sortantes de même taille ; pour la source, les sortantes l'emportent.

### P14

[e1-incomp] Un écoulement dont la divergence est nulle partout porte un nom.
[e1-nom] On le dit incompressible.
[e1-tache] Suis une petite tache de fluide qui se déplace avec lui.
[e1-deforme] Elle peut s'étirer et se tordre.
[e1-garde] Mais comme chaque petit cercle rend tout ce qu'il reçoit, elle garde son aire.
[e1-volume] Dans l'espace, c'est son volume qu'elle garde.
[e1-riviere] Dans une rivière, chaque goutte d'eau garde presque son volume.
[e1-comprimer] Car l'eau se laisse très mal comprimer.

> écran : une tache colorée transportée par un écoulement plan sans divergence, qui s'étire sans changer d'aire ; « divergence nulle : l'aire se conserve » ; avec [e1-volume], « dans l'espace : le volume se conserve ».

## Idée 2. Ce qui tourne : la vorticité

### P15

[e1-transition] On sait maintenant voir ce qui sort d'un point.
[e1-tourneq] Même petit cercle, seconde question : est-ce que ça tourne ?
[e1-parcours] Cette fois, on fait le tour du cercle dans le sens trigonométrique.
[e1-trigo] C'est le sens contraire des aiguilles d'une montre.
[e1-autre] On garde maintenant l'autre morceau de chaque flèche, celui qui longe le bord.
[e1-avec] Il compte en plus s'il va dans le sens du parcours.
[e1-contre] Il compte en moins s'il va contre.
[e1-circulation] La somme tout autour du cercle s'appelle la circulation.

> écran : le cercle en tirets parcouru dans le sens trigonométrique ; sur chaque flèche du bord, seule la part le long du bord est gardée ; le mot « circulation ».

### P16

[e1-recette] Ensuite, on suit la même recette que pour la divergence.
[e1-divaire] On divise par l'aire, puis on fait rétrécir le cercle.
[e1-vorticite] Le nombre qu'on trouve s'appelle la vorticité.
[e1-vortsens] Elle mesure combien le fluide tourne sur lui-même, en ce point.
[e1-carre] Le petit carré donne aussi sa formule.
[e1-croise] Cette fois, les rôles se croisent.
[e1-vertdroite] On prend la dérivée de la composante verticale vers la droite.
[e1-horizhaut] On lui retire la dérivée de la composante horizontale vers le haut.

> écran : avec [e1-croise], ω = ∂x uy − ∂y ux, les indices croisés mis en évidence.

### P17

[e1-fleche3d] Dans l'espace, la vorticité devient une flèche : le rotationnel de la vitesse.
[e1-plan] Pour un écoulement plan, cette flèche est perpendiculaire à l'écran.
[e1-signe] Elle en sort si la vorticité est positive, elle y entre sinon.
[e1-longueur3d] La vorticité est sa longueur, comptée avec un signe.

> écran : avec [e1-fleche3d], ∇×u ; une flèche perpendiculaire au plan de la carte ; avec [e1-signe], elle sort de l'écran pour ω > 0, elle y entre pour ω < 0.

### P18

[e1-roue] Pour sentir la vorticité, pose une petite roue à aubes dans l'écoulement.
[e1-pousse] Le fluide pousse ses aubes, et elle se met à tourner sur elle-même.
[e1-moitie] Sa vitesse de rotation vaut la moitié de la vorticité.
[e1-exemple] Un exemple aide à le retenir.
[e1-reprends] Reprends la rotation de tout à l'heure.
[e1-disque] Le fluide y tourne d'un seul bloc, comme un disque rigide.
[e1-vitesseun] Le disque tourne à la vitesse de rotation un.
[e1-colle] La roue tourne avec lui, exactement à la même vitesse.
[e1-affiche] Pourtant, le compteur de vorticité affiche deux.
[e1-retiens] Retiens-le : la vorticité vaut deux fois la vitesse de rotation sur place.

> écran : avec [e1-moitie], « vitesse de rotation de la roue = ω ÷ 2 ».
> écran : dès [e1-reprends], la roue dans la rotation solide, qui tourne avec le fluide ; « vitesse de rotation du disque : 1 » ; compteur de vorticité à 2.

### P19

[e1-surprises] Viennent maintenant deux surprises.
[e1-cisail] La première s'appelle un cisaillement.
[e1-haut] En haut, le fluide file vers la droite.
[e1-bas] En bas, il file vers la gauche.
[e1-milieu] Sur la ligne du milieu, il est immobile.
[e1-loin] Plus on s'éloigne de cette ligne, plus il va vite.
[e1-courant] Une ligne de courant est une courbe qui suit partout les flèches de vitesse.
[e1-droites] Partout, il avance à l'horizontale : les lignes de courant sont des droites.

> écran : le cisaillement u = (y, 0) ; flèches vers la droite en haut, vers la gauche en bas, nulles sur la ligne du milieu ; avec [e1-courant], le mot « ligne de courant » et quelques lignes horizontales tracées le long des flèches.

### P20

[e1-pose] Pose la roue sur la ligne du milieu.
[e1-aubeshaut] Ses aubes du haut sont poussées vers la droite.
[e1-aubesbas] Ses aubes du bas sont poussées vers la gauche.
[e1-horaire] La roue tourne donc, dans le sens horaire.
[e1-moinsun] Ici, la vorticité vaut moins un.
[e1-undemi] La roue tourne à la vitesse un demi.
[e1-lecon1] Des lignes droites n'empêchent donc pas le fluide de tourner sur lui-même.

> écran : la roue posée sur la ligne du milieu, aubes du haut vers la droite, du bas vers la gauche ; avec [e1-moinsun], ω = −1 ; avec [e1-undemi], « vitesse de rotation de la roue = 1/2, sens horaire ».

### P21

[e1-tourbillon] Seconde surprise : le tourbillon ponctuel.
[e1-autour] Le fluide tourne autour d'un centre, en cercles.
[e1-diminue] Sa vitesse diminue comme un sur la distance au centre.
[e1-double] Deux fois plus loin, il va deux fois moins vite.
[e1-loincentre] Pose la roue loin du centre, et laisse-la faire le tour.
[e1-cabine] Elle garde toujours la même orientation, comme une cabine de grande roue.
[e1-surplace] Elle ne tourne pas sur elle-même.

> écran : avec [e1-diminue], |u| = 1/r, où r est la distance au centre ; lignes de courant circulaires.
> écran : la roue fait le tour du centre sans pivoter ; elle n'est jamais posée sur le centre.

### P22

[e1-bords] Regarde les deux bords de la roue.
[e1-proche] Le bord proche du centre est poussé plus vite que le bord éloigné.
[e1-unsens] À lui seul, cet écart la ferait tourner dans un sens.
[e1-courbure] Mais son trajet est courbe.
[e1-virage] Ce virage, lui, la ferait tourner dans l'autre sens.
[e1-annulent] Pour cette façon précise de ralentir, les deux effets s'annulent exactement.
[e1-exo2] Le calcul est dans l'exercice deux, et tu peux le faire crayon en main.
[e1-lecon2] Des lignes courbes ne prouvent donc pas que le fluide tourne sur lui-même.

> écran : sur les deux bords de la roue, deux flèches de vitesse, la plus longue du côté du centre ; rappel |u| = 1/r ; avec [e1-exo2], « exercice 2 (c) ».

### P23

[e1-ou] Alors, où est passée la rotation de ce tourbillon ?
[e1-nullepartout] Sa vorticité est nulle partout, sauf au centre.
[e1-nondef] Au centre, elle n'est pas définie, car la vitesse y devient infinie.
[e1-entiere] C'est là, au centre, que se cache toute la rotation.
[e1-revele] Voilà pourquoi un cercle qui entoure le centre a une circulation non nulle.
[e1-memecirc] Petit ou grand, il donne toujours la même circulation.
[e1-zerocirc] Un cercle qui n'entoure pas le centre donne zéro.
[e1-image] Garde cette image en tête : elle reviendra.

> écran : avec [e1-nullepartout], « vorticité nulle hors du centre » ; avec [e1-nondef], le centre marqué « non définie ».
> écran : plusieurs cercles de tailles différentes entourent le centre ; un compteur « circulation », sans division par l'aire, affiche la même valeur pour chacun ; un cercle à l'écart du centre affiche 0.

### P24

[e1-retour] Reviens maintenant à la carte du début.
[e1-engrenages] Elle montre des cellules qui tournent côte à côte, comme des engrenages de fluide.
[e1-coin] Sa formule est dans le coin de l'écran.
[e1-paslire] Tu n'as pas besoin de la lire.
[e1-dedans] Place le cercle à l'intérieur d'une cellule.
[e1-varie] Tant que le cercle est grand, le compteur de circulation par unité d'aire varie d'une taille à l'autre.
[e1-rapetisse] Quand le cercle rapetisse, le compteur bouge de moins en moins.
[e1-fixe] Puis il se fixe sur une valeur.
[e1-valeur] Cette valeur, c'est la vorticité au centre du cercle.
[e1-visible] Voilà la limite dont on parle depuis le début, enfin visible.

> écran : l'écoulement cellulaire, formule en coin, non dite : u = (sin x cos y, −cos x sin y).
> écran : cercle rétrécissant à l'intérieur d'une cellule, loin des droites qui séparent les cellules ; le compteur « circulation divisée par l'aire » se stabilise.

## Clôture. L'énigme des cellules

### P25

[e1-autreq] Pose maintenant l'autre question à ces cellules : est-ce que ça sort ?
[e1-promene] Promène le cercle où tu veux, petit ou grand.
[e1-zero] Le compteur de flux reste bloqué sur zéro, partout.
[e1-nullepart] Nulle part ce fluide ne jaillit, nulle part il ne disparaît.
[e1-hasard] Ce n'est pas un hasard.
[e1-pourquoi] Pourquoi ce champ ne diverge-t-il nulle part ?
[e1-ouverte] Garde la question : l'épisode suivant y répondra.

> écran : le cercle se promène sur les cellules, le compteur « flux sortant divisé par l'aire » reste à 0 ; la formule reste en coin ; le mot « pourquoi ? » reste affiché.

### P26

[e1-retenir] Retiens deux gestes.
[e1-sortir] Sortir : le flux par unité d'aire, sur un cercle qui rétrécit, donne la divergence.
[e1-tourner] Tourner : la circulation par unité d'aire donne la vorticité.
[e1-rouemoitie] La roue à aubes tourne à la moitié de cette vorticité.
[e1-rappelcis] Le cisaillement a des lignes droites, et pourtant il fait tourner la roue.
[e1-rappeltour] Loin du centre du tourbillon ponctuel, la roue ne tourne pas sur elle-même.

> écran : les deux gestes en deux lignes, chacun avec sa formule : ∇·u = ∂x ux + ∂y uy ; ω = ∂x uy − ∂y ux.

### P27

[e1-crayon] Avant l'épisode suivant, prends un crayon.
[e1-exos] Les exercices affichés à l'écran changent ces images en calculs.
[e1-suivant] Ensuite, on passera du petit cercle à toute une région.

> écran : exercices 1 b, 2 b et 2 c, ancre #exercices du module.
