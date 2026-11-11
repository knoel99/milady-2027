# Épisode 02 : narration

Titre de travail : « Le bord, l'aimant et la carte des hauteurs ».
Module : `prep/p1-calcul-vectoriel/index.qmd`. Traitement : `video/episodes/ep02/traitement.md`.
Ton : tutoiement. Voix : environ 1 780 mots, soit 11 min 50 à 150 mots par minute.
Les lignes « > écran : » et « > légende : » ne sont pas dites. La voix ne dicte aucune formule : la formule est à l'écran, la voix dit ce qu'elle signifie.

## Ouverture

### P1

[e2-rappel] À la fin de l'épisode précédent, une énigme est restée ouverte.
[e2-souviens] Souviens-toi : tu as promené un petit cercle sur des cellules qui tournent.
[e2-cellules] Le compteur de flux restait à zéro, partout.
[e2-question] Pourquoi ce champ ne diverge-t-il nulle part ?
[e2-detour] Pour répondre, on va faire un détour par le champ magnétique.
[e2-promesse] À la fin, tu sauras fabriquer des champs qui ne divergent nulle part.

> écran : l'écoulement cellulaire de ep01, formule en coin ; le cercle se promène, compteur de flux à 0 ; « pourquoi ? ».

### P2

[e2-plan] On avance en trois étapes.
[e2-etape1] D'abord, passer d'un petit cercle à toute une région.
[e2-etape2] Ensuite, passer du plan à l'espace, et rencontrer le champ magnétique.
[e2-etape3] Enfin, construire des champs sans divergence, au lieu de les vérifier.

> écran : le plan en trois lignes, affichées au fil de la voix : « du petit au grand » ; « du plan à l'espace » ; « construire ».

## Idée 1. Le bord raconte l'intérieur

### P3

[e2-but] Le but : relier ce qui se passe dans une région à ce qu'on voit sur son bord.
[e2-region] Prends une région du plan, de forme quelconque.
[e2-carrelage] Découpe-la en petits carreaux, comme un carrelage.
[e2-chaque] Pour chaque carreau, calcule le flux qui sort par ses quatre côtés.
[e2-voisins] Regarde maintenant deux carreaux voisins.
[e2-commun] Ils partagent un côté.
[e2-passe] Ce qui sort de l'un par ce côté entre dans l'autre.
[e2-annule] Compté une fois en plus et une fois en moins, il disparaît du total.

> écran : deux carreaux voisins ; sur leur côté commun, une flèche sortante pour l'un, entrante pour l'autre ; les deux s'effacent.

### P4

[e2-tous] Fais la même chose pour tous les côtés intérieurs.
[e2-paires] Ils s'effacent tous, par paires.
[e2-bord] Il ne reste que les côtés posés sur le bord de la région.
[e2-total] Le flux total des carreaux, c'est donc le flux à travers le bord.

> écran : le carrelage complet ; les flèches des côtés intérieurs s'effacent par paires, il ne reste que le contour.

### P5

[e2-rappeldiv] Or tu sais ce que vaut le flux d'un tout petit carreau.
[e2-produit] C'est à peu près sa divergence, multipliée par son aire.
[e2-definition] C'est ce que dit la définition de la divergence, vue dans l'épisode précédent.
[e2-affine] Plus les carreaux sont petits, plus cette approximation est bonne.
[e2-erreur] Quand les carreaux rapetissent, l'erreur sur chacun devient bien plus petite que son aire.
[e2-erreursomme] Additionnées, ces erreurs finissent par disparaître.
[e2-limite] À la limite, l'égalité devient exacte.
[e2-enonce] La somme des divergences fois les aires égale le flux à travers le bord.
[e2-nom] C'est le théorème de Green-Ostrogradski.

> écran : les carreaux se subdivisent pendant [e2-affine] et [e2-erreur] ; avec [e2-enonce], « Green-Ostrogradski : somme des divergences × aire = flux à travers le bord » ; puis l'énoncé complet ∫Ω ∇·u dx = ∮∂Ω u·n dℓ.

### P6

[e2-stokes0] Remplace maintenant le flux par la circulation.
[e2-stokes1] Chaque carreau est parcouru dans le sens trigonométrique.
[e2-stokes2] Sur un côté commun, les deux carreaux voisins passent donc dans des sens contraires.
[e2-stokes3] Là encore, leurs contributions s'annulent.
[e2-stokesrappel] Tu l'as vu dans l'épisode un : la circulation d'un petit carreau vaut à peu près sa vorticité fois son aire.
[e2-stokes4] La somme des vorticités fois les aires égale la circulation sur le bord.
[e2-stokesnom] C'est le théorème de Stokes, dans le plan.
[e2-raconte] Dans les deux cas, le bord raconte l'intérieur.
[e2-tour] Pour connaître le total à l'intérieur, il suffit de faire le tour.

> écran : deux carreaux voisins parcourus dans le sens trigonométrique, flèches opposées sur le côté commun ; avec [e2-stokesrappel], « circulation d'un petit carreau ≈ ω × aire » ; avec [e2-stokes4], « Stokes : somme des vorticités × aire = circulation sur le bord » ; puis ∫Ω ω dx = ∮∂Ω u·t dℓ, sous-titré « bord parcouru en gardant la région à sa gauche, sens trigonométrique pour une région sans trou ».

### P7

[e2-echo] Tu te souviens du tourbillon ponctuel ?
[e2-echo2] Tout cercle autour du centre donnait la même circulation.
[e2-echo3] Carrelle maintenant l'anneau entre deux de ces cercles.
[e2-anneaubord] Son bord, ce sont les deux cercles.
[e2-anneausens] Les carreaux longent le grand dans le sens trigonométrique, et le petit dans le sens horaire.
[e2-anneaudiff] La circulation sur ce bord vaut celle du grand cercle, moins celle du petit.
[e2-anneaunulle] Or la vorticité est nulle dans tout l'anneau : on l'a vu dans l'épisode un.
[e2-echo4] La différence vaut donc zéro : les deux cercles ont la même circulation.
[e2-echo5] Toute la rotation vient du centre.
[e2-echo6] Chaque cercle autour du centre la compte en entier.

> écran : deux cercles autour du centre du tourbillon, l'anneau entre eux carrelé ; avec [e2-anneausens], flèches de parcours dans le sens trigonométrique sur le grand cercle, dans le sens horaire sur le petit ; avec [e2-anneaunulle], « vorticité nulle dans l'anneau » ; avec [e2-echo4], « circulation(grand) − circulation(petit) = 0 » ; aucun cercle ne rétrécit sur le centre.

## Idée 2. Du plan à l'espace : le champ magnétique

### P8

[e2-planjusque] Jusqu'ici, tout se passait dans le plan.
[e2-sphere] Dans l'espace, le petit cercle devient une petite sphère.
[e2-volume] L'aire devient un volume, et le carreau devient un petit cube.
[e2-peau] Le bord de la région devient une surface fermée, comme la peau d'un ballon.
[e2-pareil] Le raisonnement ne change pas.
[e2-faces] Les faces communes à deux cubes s'annulent, et il ne reste que la peau.

> écran : le cercle se gonfle en sphère, le carreau en petit cube ; un ballon découpé en petits cubes, faces intérieures qui s'effacent.

### P9

[e2-champb] Applique ce raisonnement au champ magnétique, celui que crée un aimant.
[e2-boussole] C'est lui qui oriente l'aiguille d'une boussole.
[e2-loi] Il obéit à une règle : sa divergence est nulle en tout point.
[e2-admet] C'est une loi de la physique : ici, on l'admet, sans la démontrer.
[e2-global] Grâce au carrelage, cette règle a une version globale.
[e2-surface] Le flux magnétique est nul à travers n'importe quelle surface fermée.
[e2-ressort] Ce qui sort par un côté du ballon rentre par un autre côté.
[e2-lignechamp] Une ligne de champ est une courbe qui suit partout les flèches du champ.
[e2-lignecourant] Pour une vitesse, c'est la ligne de courant de l'épisode un.
[e2-traverse] Les lignes de champ d'un aimant, par exemple, le traversent de part en part.

> écran : avec [e2-loi], ∇·B = 0, sous-titré « divergence du champ magnétique » ; avec [e2-admet], « loi admise » ; avec [e2-surface], « flux nul à travers n'importe quelle surface fermée ».
> écran : avec [e2-lignechamp], quelques flèches du champ et une courbe tracée le long d'elles, le mot « ligne de champ » ; avec [e2-traverse], l'esquisse d'un aimant traversé par ses lignes, sans détail.

### P10

[e2-imagine] Imagine un point d'où partiraient des lignes de champ.
[e2-suppose] Et suppose qu'il n'en arrive pas autant.
[e2-ballon] Un petit ballon autour de ce point verrait plus de lignes sortir qu'entrer.
[e2-interdit] Son flux ne serait pas nul, ce qui est interdit.
[e2-aucun] Aucun point ne peut donc être le départ ou l'arrivée d'une gerbe de lignes.
[e2-monopole] Un tel point s'appellerait un monopôle magnétique : il n'en existe pas.

> écran : un point hypothétique d'où partent des lignes, entouré d'une petite sphère ; le tout barré ; le mot « monopôle ».

### P11

[e2-charge] Compare avec le champ d'une charge électrique.
[e2-partent] Ses flèches partent de la charge dans toutes les directions.
[e2-coupe] Sur ces images, les cercles en tirets sont des sphères, vues en coupe.
[e2-transparents] Imagine-les comme des ballons transparents posés autour de la charge.
[e2-centree] Prends une sphère centrée sur la charge.
[e2-enface] Partout sur elle, le champ la traverse bien en face, avec la même intensité.
[e2-faiblit] Plus la sphère est grande, plus cette intensité faiblit.
[e2-diviseequatre] Quand le rayon double, l'intensité est divisée par quatre.
[e2-grandit] L'aire de la sphère, elle, grandit.
[e2-multquatre] Quand le rayon double, l'aire est multipliée par quatre.
[e2-produit2] Le flux est le produit de l'intensité par l'aire.
[e2-memeprod] Divisé par quatre puis multiplié par quatre, ce produit reste le même.
[e2-quatrepi] Il vaut toujours quatre pi, quel que soit le rayon.

> écran : panneau de gauche de fig-monopole-dipole.png ; sphères de rayons croissants autour de la charge ; flèches perpendiculaires à la sphère, de même longueur sur une même sphère, plus courtes sur les sphères plus grandes.
> écran : avec [e2-diviseequatre], « intensité = 1/R² », sous-titré « unités choisies pour que l'intensité vaille 1/R² » ; avec [e2-multquatre], « aire = 4πR² » ; avec [e2-quatrepi], « flux = 4π ». Aucun compteur « flux divisé par l'aire ».

### P12

[e2-pourtant] Pourtant, hors de la charge, la divergence de ce champ est nulle.
[e2-cache] Toute la source se cache dans le point lui-même.
[e2-entoure] Seule une sphère qui entoure ce point la révèle.
[e2-cote] Une sphère placée à côté a un flux nul.
[e2-tourbillon] Souviens-toi du tourbillon ponctuel : toute sa rotation était cachée au centre.
[e2-sortie] Ici, c'est toute la sortie qui se cache dans un point.

> écran : une sphère en coupe à l'écart de la charge, valeur affichée 0 ; une sphère qui l'entoure, 4π.

### P13

[e2-aimant] Regarde maintenant un petit aimant.
[e2-dipole] On l'appelle un dipôle, et son champ est un champ dipolaire.
[e2-limaille] De la limaille de fer posée autour de lui dessine ses lignes.
[e2-sortent] Ses lignes sortent par un bout de l'aimant.
[e2-fonttour] Elles font le tour par l'extérieur, puis rentrent par l'autre bout.
[e2-traversent] Ensuite, elles traversent l'aimant de part en part.
[e2-sansfin] Elles n'ont ni début ni fin.
[e2-nul] Toute sphère, qu'elle entoure l'aimant ou non, a un flux nul.

> écran : un petit aimant étendu, traversé de part en part par ses lignes ; sphères en coupe, valeur 0 pour chacune.

### P14

[e2-deuxcartes] Voici deux cartes sans étiquette : laquelle peut montrer un champ magnétique ?
[e2-reflechis] Pense aux sphères en coupe, et prends quelques secondes avant la réponse.

> écran : deux cartes côte à côte, la charge à gauche, le petit aimant étendu à droite, sans étiquette ; sur chacune, des cercles en tirets ; « laquelle peut être magnétique ? ».

### P15

[e2-critere] Le test porte sur le champ dans l'espace, pas sur le dessin.
[e2-critere2] Il faut un flux nul à travers n'importe quelle surface fermée.
[e2-verdict1] La carte de droite, celle de l'aimant, passe le test.
[e2-verdict2] Celle de gauche échoue, à cause de son point central.

> écran : 4π autour de la charge, 0 autour de l'aimant ; la carte de droite cochée.

## Idée 3. Construire plutôt que vérifier : la fonction de courant

### P16

[e2-verifier] Vérifier un champ, c'est bien.
[e2-mieux] Le construire juste dès le départ, c'est mieux.
[e2-hauteurs] Prends une carte des hauteurs, comme une carte de randonnée.
[e2-altitude] À chaque point du plan, elle donne une altitude.
[e2-outil] Ce n'est pas un vrai relief : c'est un outil de calcul.
[e2-niveau] Les lignes de niveau relient les points de même altitude.

> écran : une carte des hauteurs, notée ψ(x, y), avec ses lignes de niveau.

### P17

[e2-marche] Imagine que tu marches sur cette carte.
[e2-gradient] En chaque point, une flèche indique la montée la plus raide.
[e2-gradnom] On l'appelle le gradient.
[e2-gradcomp] Ses deux composantes disent de combien on monte en allant vers la droite, et vers le haut.
[e2-angle] Le gradient coupe toujours les lignes de niveau à angle droit.
[e2-pente] Plus la pente est forte, plus il est long.
[e2-douce] Sur une pente douce, il est court.
[e2-randonneur] Un randonneur qui suit cette flèche grimpe le plus vite possible.
[e2-plat] Celui qui suit une ligne de niveau ne monte ni ne descend.

> écran : avec [e2-gradcomp], ∇ψ = (∂xψ, ∂yψ) ; une flèche de gradient perpendiculaire à une ligne de niveau, plus longue là où les lignes se serrent.

### P18

[e2-quart] Tourne cette flèche d'un quart de tour, dans le sens horaire.
[e2-suit] Elle ne monte plus : elle suit la ligne de niveau.
[e2-vitesse] Prends cette flèche tournée comme vitesse du fluide.
[e2-courant] Les lignes de niveau deviennent alors des lignes de courant.
[e2-gauche] Les hauteurs les plus grandes restent toujours à gauche du courant.
[e2-fonction] La carte des hauteurs prend un nouveau nom : la fonction de courant.

> écran : une flèche de gradient pivote d'un quart de tour dans le sens horaire et devient tangente à la ligne de niveau ; les grandes valeurs de ψ restent à gauche du courant.
> écran : avec [e2-fonction], u = ∇⊥ψ = (∂yψ, −∂xψ), sous-titré « ψ : fonction de courant ».

### P19

[e2-calcul] Calcule la divergence de cette vitesse.
[e2-deuxtermes] On trouve deux termes.
[e2-terme1] Le premier dérive la carte vers le haut, puis vers la droite.
[e2-terme2] Le second fait la même chose dans l'autre ordre, et on le retranche.
[e2-ordre] Pour une carte assez lisse, l'ordre des deux dérivations ne change rien.
[e2-zero] Les deux termes sont égaux, et leur différence vaut zéro.
[e2-toujours] Ce calcul marche pour n'importe quelle carte des hauteurs.
[e2-livree] La divergence nulle n'est plus à vérifier : elle vient avec la construction.

> écran : avec [e2-deuxtermes], ∇·u = ∂x∂yψ − ∂y∂xψ ; avec [e2-zero], « = 0 ».

### P20

[e2-boite] Choisis une carte faite de bosses et de creux alternés, comme une boîte à œufs.
[e2-formule] Sa formule est à l'écran.
[e2-revoila] Fais tourner ses flèches de pente d'un quart de tour, dans le sens horaire.
[e2-retrouve] Tu retrouves les cellules de l'énigme.
[e2-reponse] Voilà la réponse : ce champ a été fabriqué à partir d'une fonction de courant.
[e2-zero2] Le compteur de flux restait donc à zéro, et partout.

> écran : avec [e2-boite], ψ = sin x sin y, en relief puis en lignes de niveau.
> écran : avec [e2-revoila], les flèches de vitesse apparaissent le long des lignes de niveau ; avec [e2-retrouve], elles forment les cellules alternées ; la formule u = (sin x cos y, −cos x sin y) de ep01 revient en coin ; le petit cercle repasse, compteur de flux à 0.

### P21

[e2-bosse] Autour d'une bosse, le fluide tourne dans le sens trigonométrique.
[e2-creux] Autour d'un creux, il tourne dans le sens horaire.
[e2-frontieres] Les droites où l'altitude vaut zéro séparent les cellules.
[e2-vort2] Un calcul court montre que la vorticité vaut deux fois la fonction de courant.
[e2-toimeme] Tu peux le faire toi-même, crayon en main.

> écran : avec [e2-frontieres], les droites x = kπ et y = kπ, où ψ = 0, séparent les cellules ; avec [e2-vort2], ω = 2ψ.

### P22

[e2-dansplan] Le champ magnétique vivait dans l'espace : on revient maintenant dans le plan.
[e2-recette] Là, la même recette marche aussi pour le champ magnétique.
[e2-potentiel] On part d'une carte des hauteurs qu'on appelle le potentiel magnétique.
[e2-memegeste] C'est le même geste, avec un autre nom.
[e2-tourne] On fait tourner ses flèches de pente d'un quart de tour, dans le sens horaire.
[e2-champ] On obtient un champ sans divergence à coup sûr : il peut être magnétique.
[e2-contour] Son flux est nul à travers n'importe quel contour fermé du plan.
[e2-office] Au lieu de vérifier qu'un champ peut être magnétique, on en fabrique un qui l'est forcément.

> écran : avec [e2-dansplan], « dans le plan » ; la même carte, renommée a, sous-titrée « potentiel magnétique », avec des flèches du champ magnétique ; avec [e2-tourne], B = ∇⊥a ; les lignes de niveau du potentiel sont les lignes du champ.

### P23

[e2-attention] Attention à ce que la recette ne promet pas.
[e2-garantit] Elle garantit une divergence nulle.
[e2-ressemble] Elle ne garantit pas que le champ ressemble à un vrai champ.
[e2-hasard] Une carte prise au hasard donne un champ sans divergence, mais sans rien de réaliste.
[e2-juger] Juger si un champ est réaliste, tu l'apprendras plus tard dans le parcours.

### P24

[e2-chercheurs] Des chercheurs se servent déjà de cette astuce.
[e2-agites] Ils l'appliquent à un écoulement simulé en deux dimensions, bien plus agité que les cellules de l'énigme.
[e2-dessine] Leur machine dessine la fonction de courant, plutôt que la vitesse elle-même.
[e2-jamais] La vitesse qu'on en tire est donc sans divergence, par construction.
[e2-vitesses] Dans ce travail, l'astuce sert pour une vitesse de fluide, pas pour un champ magnétique.

> écran : carte de vitesse d'un fluide plan agité, illustration fabriquée pour le film, ni figure de l'article ni sortie de FunDiff ; avec ses lignes de courant.
> légende : Idée utilisée par Wang et al., FunDiff, Nature Communications, 2026.
> écran : légende sur la carte de vitesse seulement, jamais sur la carte du champ magnétique.

## Clôture

### P25

[e2-retenir] Retiens trois idées.
[e2-r1] Le bord raconte l'intérieur : c'est le carrelage, Green-Ostrogradski et Stokes.
[e2-r2] Le champ magnétique a un flux nul à travers n'importe quelle surface fermée.
[e2-r2b] Ses lignes n'ont ni début ni fin, et il n'y a pas de monopôle.
[e2-r3] Prends les flèches de pente d'une fonction de courant.
[e2-r3b] Tourne-les d'un quart de tour dans le sens horaire : le champ obtenu n'a pas de divergence.

> écran : trois lignes, chacune avec sa formule : « ∫Ω ∇·u dx = ∮∂Ω u·n dℓ » ; « ∇·B = 0 » ; « u = ∇⊥ψ, ∇·u = 0 ».

### P26

[e2-voie] Il existe une autre façon d'obtenir un champ sans divergence.
[e2-retirer] On part d'un champ quelconque et on lui retire la partie qui diverge.
[e2-projection] Cette méthode s'appelle la projection.
[e2-chapitre6] Le module la traite au chapitre six.
[e2-crayon] D'ici là, prends un crayon.
[e2-exos] Les exercices affichés à l'écran changent ces images en calculs.

> écran : exercices 1 c, 6, 7 a, 9 a et 9 c, ancre #exercices du module ; « projection : chapitre 6 ».
