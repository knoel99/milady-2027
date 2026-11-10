# Épisode 01 : narration

Module : `prep/p1-calcul-vectoriel/index.qmd`. Traitement : `video/episodes/ep01/traitement.md`.
Ton : tutoiement. Voix : environ 2 090 mots, soit 13 min 55 à 150 mots par minute.
Les lignes « > écran : » et « > légende : » ne sont pas dites.

## Ouverture

### P1

[o-cartes] Voici deux cartes de flèches.
[o-fleche] En chaque point, une flèche donne la direction du champ et son intensité.
[o-gauche] À gauche, le champ d'une charge électrique.
[o-droite] À droite, celui d'un petit aimant.
[o-question] Si on cachait les étiquettes, saurais-tu dire laquelle peut être un champ magnétique ?

> écran : deux cartes côte à côte, la charge à gauche, un petit aimant étendu à droite, sans étiquette.

### P2

[o-enjeu] Cette question va nous suivre longtemps.
[o-machine] Plus tard dans le parcours, une machine dessinera des champs, et il faudra juger si la physique les accepte.
[o-plan] Pour y répondre, on avance en trois temps.
[o-local] D'abord, regarder un point de très près avec deux questions simples : est-ce que ça sort, et est-ce que ça tourne ?
[o-global] Ensuite, passer du petit au grand, puis du plan à l'espace.
[o-fabriquer] Enfin, fabriquer des champs qui passent le test à coup sûr.

## Idée 1. La divergence : ce qui sort d'un petit cercle

### P3

[d-vocabulaire] D'abord, un peu de vocabulaire.
[d-vectoriel] Une carte comme celles-ci s'appelle un champ vectoriel : à chaque point du plan, on attache une flèche.
[d-lignes] Une courbe qui suit les flèches partout s'appelle une ligne de champ ; pour une vitesse, on dit ligne de courant.
[d-composantes] La flèche a deux composantes : u x vers la droite, u y vers le haut.
[d-partielle] Pour savoir comment u x change quand on se déplace vers la droite, on dérive en x en gardant y fixe.
[d-drond] C'est une dérivée partielle, et on la lit d rond u x sur d rond x.

### P4

[d-source] Première question : ce point est-il une source ?
[d-cercle] Pour le savoir, entoure-le d'un petit cercle.
[d-decompose] En chaque point du bord, coupe la flèche en deux morceaux.
[d-travers] Le morceau perpendiculaire au bord, celui qui le traverse, est le seul qui compte.
[d-longe] Le morceau qui longe le bord ne fait rien sortir.
[d-signe] On le compte en plus s'il pointe vers l'extérieur, en moins s'il pointe vers l'intérieur.

> écran : une flèche posée sur le cercle en tirets, décomposée en sa part perpendiculaire au bord, qui compte, et sa part le long du bord, qui ne compte pas.

### P5

[d-flux] On additionne ces morceaux tout autour du cercle : c'est le flux.
[d-aire] On divise ensuite par l'aire du disque, pour ne pas avantager les grands cercles.
[d-limite] Enfin, on fait rétrécir le cercle vers le point.
[d-divergence] Le nombre obtenu à la limite s'appelle la divergence du champ en ce point.
[d-positive] Si elle est positive, le point fait sortir plus qu'il ne reçoit.
[d-negative] Si elle est négative, il avale.

### P6

[d-carre] Pour trouver la formule, remplace le cercle par un petit carré.
[d-cotes] Regarde d'abord ses côtés gauche et droit.
[d-ecart] Ce qui sort à droite, moins ce qui entre à gauche, c'est l'écart de u x entre ces deux côtés.
[d-variation] Rapporté à la largeur du carré, cet écart devient d rond u x sur d rond x.
[d-hautbas] Même geste en haut et en bas, et l'on obtient d rond u y sur d rond y.
[d-somme] La divergence est la somme des deux : d rond u x sur d rond x, plus d rond u y sur d rond y.

> écran : petit carré, flèche entrante courte à gauche, flèche sortante longue à droite ; puis le même geste en bas et en haut.

### P7

[d-deux] Essayons sur deux champs.
[d-fuit] Le premier fuit l'origine dans toutes les directions : au point x, y, sa flèche est x, y.
[d-vautdeux] Sa divergence vaut un plus un, donc deux.
[d-rotation] Le second tourne autour de l'origine : au point x, y, sa flèche est moins y, x.
[d-vautzero] Sa divergence vaut zéro plus zéro, donc zéro.

### P8

[d-centre] Pose d'abord le cercle au centre.
[d-sortent] Dans la source, toutes les flèches franchissent le bord vers l'extérieur.
[d-glissent] Dans la rotation, elles glissent le long du bord sans jamais le franchir.
[d-promene] Promène maintenant le cercle loin de l'origine.
[d-entrent] Dans les deux champs, des flèches entrent d'un côté et ressortent de l'autre.
[d-bilan] Le bilan reste nul pour la rotation ; pour la source, il vaut toujours deux fois l'aire du disque.

> écran : le cercle promené sur la source et sur la rotation, avec le compteur « flux sortant divisé par l'aire », qui affiche 2 ou 0.

### P9

[d-compteur] Le compteur affiche exactement deux ou zéro, quelles que soient la place du cercle et sa taille.
[d-simple] Cette régularité tient à la grande simplicité de ces deux champs.
[d-incompressible] Un écoulement de divergence nulle partout ne crée ni ne détruit d'aire, et dans l'espace, ni de volume.
[d-nomme] On le dit incompressible.

### P10

[d-cellules] Dernier essai, sur un champ plus riche : des cellules qui tournent côte à côte, comme des engrenages de fluide.
[d-enigme] Promène le cercle où tu veux : le compteur reste bloqué sur zéro.
[d-pourquoi] Pourquoi ce champ ne diverge-t-il nulle part ?
[d-suspens] Garde la question, la réponse viendra à la fin.

> écran : l'écoulement cellulaire ; le cercle se promène, le compteur de flux reste à 0.

## Idée 2. Le rotationnel : la roue à aubes

### P11

[r-tourne] Même petit cercle, autre question : est-ce que ça tourne ?
[r-sens] Cette fois, on parcourt le cercle dans le sens trigonométrique, contraire aux aiguilles d'une montre.
[r-garde] En chaque point du bord, on garde le morceau de flèche qui longe le cercle, dans le sens du parcours.
[r-circulation] La somme de ces morceaux s'appelle la circulation.
[r-vorticite] Divisée par l'aire, puis à la limite, elle donne la vorticité, qu'on note oméga.
[r-formule] Sa formule croise les rôles : d rond u y sur d rond x, moins d rond u x sur d rond y.

### P12

[r-rotationnel] Dans l'espace, la vorticité devient une flèche, le rotationnel de la vitesse ; dans le plan, oméga est sa composante qui sort de l'écran.
[r-roue] Pour la sentir, pose dans l'écoulement une petite roue à aubes.
[r-moitie] Elle tourne sur elle-même à une vitesse angulaire égale à oméga divisé par deux.

### P13

[r-bloc] Reprends la rotation de tout à l'heure.
[r-disque] Le fluide y tourne d'un seul bloc, comme un disque rigide, à la vitesse angulaire un.
[r-colle] La roue colle au fluide : elle fait un tour quand il en fait un.
[r-affiche] Pourtant, le compteur de vorticité affiche deux.
[r-retiens] Retiens-le : la vorticité vaut deux fois la vitesse de rotation locale.

> écran : la roue dans la rotation solide, qui tourne avec le fluide ; compteur de vorticité à 2.

### P14

[r-surprises] Viennent maintenant deux surprises.
[r-cisaillement] Dans un cisaillement, les flèches vont vers la droite en haut et vers la gauche en bas, d'autant plus vite qu'on s'éloigne de la ligne du milieu.
[r-droites] Toutes les lignes de courant sont droites.
[r-pales] Pourtant, les pales du haut sont poussées vers la droite, et celles du bas vers la gauche.
[r-horaire] La roue tourne dans le sens des aiguilles d'une montre : oméga vaut moins un, et la roue tourne à la vitesse angulaire un demi.

> écran : le cisaillement, la roue dont les pales du haut filent à droite et celles du bas à gauche.

### P15

[r-tourbillon] Seconde surprise : le tourbillon ponctuel.
[r-ponctuel] Le fluide tourne autour d'un centre, et sa vitesse diminue comme un sur la distance à ce centre.
[r-cercles] Ses lignes de courant sont des cercles.
[r-nacelle] Pourtant, hors du centre, la roue en fait le tour en gardant son orientation, comme une nacelle de grande roue.
[r-immobile] Elle ne tourne pas sur elle-même.

> écran : la roue fait le tour du centre sans pivoter ; elle n'est jamais posée sur le centre.

### P16

[r-bords] Regarde ses deux bords.
[r-proche] Le bord proche du centre est poussé plus vite que le bord éloigné, ce qui la ferait tourner dans un sens.
[r-courbe] La courbure du trajet, elle, la ferait tourner dans l'autre.
[r-compense] Les deux effets se compensent exactement.
[r-lecon] Des lignes courbes ne prouvent donc pas que le fluide tourne sur lui-même, et des lignes droites ne l'en empêchent pas.

> écran : sur les deux bords de la roue, deux flèches de vitesse, la plus longue du côté du centre.

### P17

[r-ou] Où est passée la rotation de ce champ ?
[r-concentree] Elle est tout entière au centre, là où la formule perd son sens.
[r-entoure] Seul un cercle qui entoure le centre la révèle.
[r-reviendra] Garde cette image : elle reviendra bientôt.

### P18

[r-retour] Reviens aux cellules, et place le cercle à l'intérieur de l'une d'elles, loin des frontières.
[r-varie] Tant que le cercle est grand, le compteur « circulation divisée par l'aire » change avec le rayon.
[r-stabilise] Quand il rétrécit, le compteur bouge de moins en moins, puis se fixe sur une valeur.
[r-valeur] Cette valeur, c'est la vorticité au centre du cercle.
[r-visible] La limite dont on parlait depuis le début devient enfin visible.

> écran : cercle rétrécissant à l'intérieur d'une cellule, loin des droites qui séparent les cellules ; le compteur de circulation divisée par l'aire se stabilise.

## Idée 3. Du petit au grand, du plan à l'espace

### P19

[g-grand] Passons du petit au grand.
[g-carrelage] Découpe une région du plan en petits carreaux, comme un carrelage.
[g-voisins] Prends deux carreaux voisins : ce qui sort de l'un par leur côté commun entre dans l'autre.
[g-annule] Sur ce côté, les deux contributions s'annulent.
[g-reste] Additionne les flux de tous les carreaux : il ne reste que ce qui franchit le bord extérieur.

> écran : le carrelage ; les flèches des côtés intérieurs s'effacent par paires, il ne reste que le contour.

### P20

[g-produit] Or le flux d'un petit carreau vaut à peu près sa divergence multipliée par son aire.
[g-somme] La somme des divergences multipliées par l'aire de chaque carreau égale donc le flux à travers le bord.
[g-ostrogradski] C'est le théorème de Green-Ostrogradski.
[g-stokes] Avec des circulations à la place des flux, le même carrelage donne le théorème de Stokes : la somme des vorticités multipliées par l'aire de chaque carreau égale la circulation sur le bord.
[g-raconte] Dans les deux cas, le bord raconte l'intérieur.

### P21

[g-plan] Jusqu'ici, tout se passait dans le plan.
[g-sphere] Dans l'espace à trois dimensions, le petit cercle devient une petite sphère, et l'aire devient un volume.
[g-cube] Le carreau devient un petit cube, et le bord de la région devient une surface fermée, comme la peau d'un ballon.
[g-peau] Le raisonnement ne change pas : les faces communes se compensent, il ne reste que la peau.

> écran : le cercle se gonfle en sphère, le carreau en petit cube.

### P22

[g-champb] Appliquons cela au champ magnétique, qu'on note B.
[g-loi] La physique impose que sa divergence soit nulle en tout point : on écrit nabla point B égale zéro.
[g-equivaut] D'après le carrelage, cela revient à dire que le flux de B est nul à travers n'importe quelle surface fermée.
[g-imagine] Imagine une ligne de champ qui partirait d'un point.
[g-sphereautour] Une petite sphère autour de ce point verrait des lignes sortir sans qu'autant y entrent, et son flux ne serait pas nul.
[g-monopole] Une ligne de champ magnétique n'a donc ni départ ni arrivée : il n'existe pas de pôle magnétique isolé, pas de monopôle.

### P23

[g-charge] Compare avec la charge électrique.
[g-coupe] Sur ces cartes, les cercles en tirets sont en fait des sphères, vues en coupe.
[g-faiblit] Sur une sphère de rayon R centrée sur la charge, le champ vaut un sur R au carré.
[g-grandit] L'aire de cette sphère vaut quatre pi R au carré.
[g-quatrepi] Le flux est le produit des deux : les R au carré s'en vont, il reste quatre pi, quelle que soit la taille de la sphère.

> écran : panneau de gauche de fig-monopole-dipole.png ; sphères de rayons croissants autour de la charge, le champ faiblit, l'aire grandit, le produit reste 4π. Aucun compteur « flux divisé par l'aire ».

### P24

[g-pourtant] Pourtant, hors de la charge, la divergence de ce champ est nulle.
[g-concentree] Toute la source est concentrée au point lui-même.
[g-revele] Seule une sphère qui entoure ce point la révèle ; une sphère qui ne l'entoure pas a un flux nul.
[g-echo] C'est le même phénomène qu'au centre du tourbillon, pour la sortie au lieu de la rotation.

### P25

[g-dipole] Le champ d'un petit aimant s'appelle un dipôle.
[g-traversent] Ses lignes sortent par un bout, font le tour par l'extérieur, rentrent par l'autre bout, puis traversent l'aimant.
[g-sansfin] Elles n'ont ni début ni fin.
[g-nul] Toute sphère, qu'elle entoure l'aimant ou non, a un flux nul.

> écran : un petit aimant étendu, traversé de part en part par ses lignes ; valeurs affichées : 4π autour de la charge, 0 autour de l'aimant.

### P26

[g-reponse] On peut maintenant répondre à la question du début.
[g-critere] Pour être magnétique, une carte de flèches doit avoir un flux nul à travers n'importe quelle surface fermée.
[g-verdict] La carte de l'aimant passe le test ; celle de la charge échoue, à cause de son point central.

## Idée 4. Construire plutôt que vérifier : la fonction de courant

### P27

[c-construire] Vérifier un champ, c'est bien ; le construire juste dès le départ, c'est mieux.
[c-randonnee] Prends une fonction psi de x et de y, et lis-la comme une carte de randonnée : psi, c'est l'altitude.
[c-niveau] Les lignes de niveau relient les points de même altitude.
[c-gradient] Le gradient de psi est la flèche faite de d rond psi sur d rond x et de d rond psi sur d rond y.
[c-montee] Il pointe vers la montée la plus raide et coupe les lignes de niveau à angle droit.

### P28

[c-quart] Tourne cette flèche d'un quart de tour dans le sens des aiguilles d'une montre.
[c-longe] Elle ne monte plus : elle longe la ligne de niveau.
[c-vitesse] Prends cette flèche tournée comme vitesse u, et note-la nabla perpendiculaire psi.
[c-compos] Ses composantes sont d rond psi sur d rond y, puis moins d rond psi sur d rond x.
[c-gauche] Les lignes de niveau deviennent des lignes de courant, et les grandes valeurs de psi restent à gauche du courant.

> écran : carte des lignes de niveau de ψ = sin x sin y ; une flèche de gradient, perpendiculaire à une ligne de niveau, pivote d'un quart de tour dans le sens horaire et devient tangente ; les grandes valeurs de ψ restent à gauche du courant.

### P29

[c-calcul] Calculons sa divergence.
[c-croisees] On trouve d rond x de d rond y psi, moins d rond y de d rond x psi.
[c-ordre] Si psi est assez lisse, l'ordre des deux dérivations ne compte pas.
[c-nulle] Les deux termes sont égaux, la différence vaut zéro, et cela quel que soit psi.
[c-livree] La divergence nulle n'est plus à vérifier : elle est livrée avec la construction.

### P30

[c-sinus] Choisis psi égale sinus x fois sinus y.
[c-revoila] Tu retrouves exactement les cellules de tout à l'heure.
[c-resolue] Voilà pourquoi le compteur de flux restait à zéro : ce champ avait été fabriqué pour ne jamais diverger.

> écran : les flèches de vitesse apparaissent le long des lignes de niveau et forment les cellules alternées ; le petit cercle repasse, compteur de flux à 0.

### P31

[c-omega] Sa vorticité vaut deux fois psi.
[c-tournent] Là où psi est positif, la cellule tourne dans le sens trigonométrique ; là où il est négatif, dans le sens des aiguilles d'une montre.
[c-frontieres] Les droites où psi s'annule séparent les cellules.
[c-machines] Des chercheurs utilisent déjà cette astuce : pour la vitesse d'un fluide en deux dimensions, ils font dessiner psi à leur machine, plutôt que la vitesse elle-même.

> écran : les droites x = kπ et y = kπ, où ψ = 0, séparent les cellules.
> légende : FunDiff, Wang et al., 2026, publié ; cité au chapitre 4 du module. Sur la carte de vitesse seulement, jamais sur la carte de B.

### P32

[c-recette] La même recette marche pour le champ magnétique dans le plan.
[c-potentiel] On part d'une fonction a, le potentiel magnétique, et on pose B égale nabla perpendiculaire a.
[c-passe] Le champ obtenu passe le test des surfaces fermées, à coup sûr.
[c-office] Au lieu de vérifier qu'une carte peut être magnétique, on en fabrique une qui l'est d'office.

> écran : la même carte, renommée a, avec des flèches de B.

### P33

[c-promet] Attention à ce que la recette ne promet pas.
[c-ressemble] Elle garantit la divergence nulle, pas que le champ ressemble à un vrai champ, et apprendre à juger cela viendra plus tard dans le parcours.

## Clôture

### P34

[f-gestes] Récapitulons les trois gestes de l'épisode.
[f-sortir] Sortir : le flux d'un petit cercle, divisé par son aire, donne la divergence.
[f-tourner] Tourner : la circulation, divisée par l'aire, donne la vorticité, qui vaut deux fois la rotation de la roue.
[f-construire] Construire : le gradient de psi, tourné d'un quart de tour, donne un champ qui ne diverge jamais.

### P35

[f-voie] Il existe une autre voie.
[f-retirer] On part d'un champ quelconque, et on lui retire la partie qui diverge.
[f-projection] Cela s'appelle la projection, et c'est au chapitre six du module.
[f-crayon] D'ici là, prends un crayon : les exercices un, deux, six, sept et neuf t'attendent.
[f-calculs] Ils changent ces images en calculs.

> écran : exercices 1 b et c, 2 b et c, 6, 7 a, 9 a et c, ancre #exercices du module.
