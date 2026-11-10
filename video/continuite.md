# Bible de continuité du film

Ce fichier dit ce que le film a déjà défini, noté, montré et expliqué. Un épisode suivant ne le réexplique pas et ne le contredit pas. Il le rappelle au plus d'une phrase.

Le module 1 est traité en deux épisodes : ep01, « Ce qui sort, ce qui tourne », et ep02, « Le bord, l'aimant et la carte des hauteurs ». L'ancienne version en un seul épisode est archivée dans `video/episodes/ep01/avant-decoupage/` ; son fond scientifique, validé, est repris sans changement.

## 1. Vocabulaire imposé

- On dit « renversement » du champ, comme le parcours écrit, jamais « inversion », dans la voix comme à l'écran.
- « Bascule » est réservé au double puits. Jamais pour le champ.
- Par prudence, la voix évite aussi « inverse » et « inversement » : on dit « contraire aux aiguilles d'une montre », « diminue comme un sur la distance ».
- Sens de rotation : « sens trigonométrique », expliqué une fois dans ep01 comme « le sens contraire des aiguilles d'une montre » ; l'autre sens se dit « sens horaire ».
- « Dipôle » : le petit aimant lui-même ; son champ est un « champ dipolaire ». Ses lignes n'ont « ni début ni fin ». On ne dit jamais « les lignes se referment toujours ».
- « Monopôle » : pôle magnétique isolé, qui n'existe pas. Formulation de ep02 : aucun point ne peut être le départ ou l'arrivée d'une gerbe de lignes.
- « Aubes » : seul mot pour la roue et ses parties, jamais « pales ».
- Critère magnétique : en 3D, « flux nul à travers n'importe quelle surface fermée » ; dans le plan, « flux nul à travers n'importe quel contour fermé du plan ». Le critère porte sur le champ dans l'espace, pas sur le dessin.
- Le tourbillon ponctuel : la roue y fait le tour « comme une cabine de grande roue ».

## 2. Ton et langue parlée

- Tutoiement du spectateur, impératifs compris : « prends », « regarde », « pose », « garde la question ». Le « on » sert pour les définitions et les raisonnements.
- Une idée par phrase, 20 mots au plus sauf énumération que l'oreille suit. Pas de tiret cadratin, pas de parenthèses.
- Des mots simples, ni administratifs ni vagues. Des images concrètes : robinet, bonde d'évier, rivière, ballon, boussole, limaille, carte de randonnée, boîte à œufs.
- Aucun segment de plus de six mots repris du module. En particulier, la voix ne dit pas « dans le sens des aiguilles d'une montre », mais « dans le sens horaire ».

### Règle : aucune formule dictée

La voix ne lit jamais une formule symbole par symbole. La formule va dans une ligne « > écran », affichée au moment où la voix en dit le sens. Proscrits dans la voix : « d rond », « nabla », « psi », « oméga », « u x », « u y », « moins y, x », « x, y » comme coordonnées, « R au carré », « sinus x fois sinus y », et toute lettre isolée qui désigne un objet, dont « a », qui s'entend comme le verbe avoir, et « B ». Le linter `tools/lint_narration.py` compte les phrases longues et les symboles dictés ; le relecteur-langue part de son rapport.

| Objet | À l'écran | Dans la voix |
|---|---|---|
| Vitesse | $\mathbf{u} = (u_x, u_y)$ | « la vitesse », « la flèche » |
| Composantes | $u_x$, $u_y$ | « la composante horizontale », « la composante verticale » |
| Dérivée partielle | $\partial_x u_x$, $\partial_y u_y$ | « la dérivée partielle vers la droite », « vers le haut » ; en clair : de combien la composante change quand on avance vers la droite sans changer de hauteur |
| Divergence | $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$ | « la divergence » ; « chaque composante dérivée dans sa propre direction » |
| Vorticité 2D | $\omega = \partial_x u_y - \partial_y u_x$ | « la vorticité » ; « les rôles se croisent : la composante verticale vers la droite, moins la composante horizontale vers le haut » |
| Rotationnel | $\nabla\times\mathbf{u}$ | « le rotationnel », la flèche qui sort de l'écran |
| Vitesse de la roue | $\omega/2$ | « la moitié de la vorticité » |
| Source | $(x, y)$ | « le fluide fuit l'origine dans toutes les directions » |
| Rotation solide | $(-y, x)$ | « le fluide tourne d'un seul bloc, comme un disque rigide » |
| Cisaillement | $(y, 0)$ | « à droite en haut, à gauche en bas, immobile sur la ligne du milieu » |
| Tourbillon ponctuel | $\lvert\mathbf{u}\rvert = 1/r$ | « la vitesse diminue comme un sur la distance au centre » |
| Écoulement cellulaire | $\mathbf{u} = (\sin x\cos y, -\cos x\sin y)$, $\psi = \sin x\sin y$ | « les cellules », « comme des engrenages de fluide » ; la carte : « bosses et creux alternés, comme une boîte à œufs » ; formule jamais dite |
| Champ magnétique | $\mathbf{B}$ | « le champ magnétique » |
| Divergence de B | $\nabla\cdot\mathbf{B} = 0$ | « sa divergence est nulle en tout point » |
| Champ d'une charge sur une sphère | $1/R^2$, $4\pi R^2$ | « quand le rayon double, l'intensité est divisée par quatre, l'aire multipliée par quatre » |
| Flux de la charge | $4\pi$ | « quatre pi », valeur seulement |
| Gradient | $\nabla\psi = (\partial_x\psi, \partial_y\psi)$ | « le gradient », « la flèche de pente », vers la montée la plus raide |
| Fonction de courant | $\psi$ | « la carte des hauteurs », puis « la fonction de courant » |
| Champ tourné | $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$ | « la flèche de pente tournée d'un quart de tour dans le sens horaire » |
| Vorticité des cellules | $\omega = 2\psi$ | « deux fois la fonction de courant » |
| Potentiel magnétique 2D | $a$, $\mathbf{B} = \nabla^\perp a$ | « le potentiel magnétique », jamais la lettre seule |
| Théorèmes | $\int_\Omega \nabla\cdot\mathbf{u}\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}\ell$, $\int_\Omega \omega\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{t}\,\mathrm{d}\ell$ | « la somme des divergences fois les aires égale le flux à travers le bord » ; de même pour les vorticités et la circulation |

Notations écran conformes à `specs/notations.md` : domaine $\Omega$, bord $\partial\Omega$, normale sortante $\mathbf{n}$, $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, $\mathbf{B} = \nabla^\perp a$.

Conventions de sens, à ne jamais contredire à l'écran :

- la circulation se calcule en parcourant le cercle, ou chaque carreau, dans le sens trigonométrique ;
- $\nabla^\perp$ tourne le gradient d'un quart de tour dans le sens horaire ; les grandes valeurs de $\psi$ sont à gauche du courant ;
- dans l'écoulement cellulaire $\psi = \sin x\sin y$, les cellules où $\psi > 0$, les bosses, tournent dans le sens trigonométrique ; les droites $x = k\pi$ et $y = k\pi$ les séparent ;
- dans le cisaillement $(y, 0)$, les flèches vont à droite en haut, à gauche en bas ; la roue tourne dans le sens horaire, à $1/2$.

## 3. Motifs récurrents

- **Le petit cercle en tirets.** L'objet central de ep01. Il pose deux questions, « est-ce que ça sort ? » pour le flux et « est-ce que ça tourne ? » pour la circulation. On le promène et on le fait rétrécir dans ep01 ; dans ep02, on le multiplie en carrelage et on le gonfle en sphère. En 3D, les cercles en tirets des cartes sont des sphères vues en coupe.
- **Le compteur.** Affiché à côté du cercle : « flux sortant divisé par l'aire » ou « circulation divisée par l'aire ». Jamais de compteur 2D sur une carte qui représente une coupe 3D : là, seulement les valeurs $4\pi$ et 0.
- **La roue à aubes.** Détecteur de rotation locale ; elle tourne à la moitié de la vorticité, énoncé suivi aussitôt de la rotation solide. Dans le cisaillement, elle est posée sur la ligne du milieu. Jamais sur le centre du tourbillon ponctuel, où aucun cercle ne rétrécit non plus.
- **Formules à l'écran.** La voix dit le sens, l'écran affiche la formule au même moment.
- **L'écoulement cellulaire, fil des deux épisodes.** Ouverture de ep01, carte sans titre ; idée 2 de ep01, la circulation par unité d'aire se stabilise ; clôture de ep01, l'énigme : flux nul partout, « pourquoi ? », question laissée ouverte ; ouverture de ep02, rappel ; idée 3 de ep02, résolution : le champ est fabriqué par une fonction de courant.
- **Le tourbillon ponctuel, écho.** ep01 : toute la rotation au centre, même circulation pour tout cercle qui l'entoure, « garde cette image ». ep02 : le carrelage de l'anneau l'explique, puis la charge en est l'écho pour ce qui sort.
- **Le carrelage.** Les côtés intérieurs se compensent par paires, il ne reste que le bord : « le bord raconte l'intérieur ».
- **Les deux cartes.** Dans ep02 seulement : charge à gauche, petit aimant étendu à droite, jamais un dipôle ponctuel. Le spectateur est invité à répondre avant le verdict. La carte de l'aimant passe le test, celle de la charge échoue.
- **La carte de randonnée.** La fonction de courant lue comme une altitude ; lignes de niveau ; gradient vers la montée la plus raide. Ce n'est « pas un vrai relief, un outil de calcul ».

## 4. Termes définis et ce qui a été expliqué

### ep01, « Ce qui sort, ce qui tourne », module 1

Défini et expliqué, à ne plus réexpliquer :

- champ vectoriel, ligne de champ, ligne de courant ; composantes horizontale et verticale ;
- dérivée partielle, en mots : de combien une composante change quand on avance vers la droite sans changer de hauteur, par unité de longueur ;
- flux à travers un cercle : somme des parts perpendiculaires au bord, en plus vers l'extérieur, en moins vers l'intérieur ;
- divergence : flux divisé par l'aire, à la limite du petit cercle ; positive, le point fait sortir, image du robinet ; négative, il avale, image de la bonde ; formule 2D obtenue sur un petit carré, droite moins gauche, haut moins bas, chaque composante dérivée dans sa propre direction ;
- source, divergence 2 ; rotation solide, divergence 0 et vorticité 2 ; cercle déplacé : flèches entrantes d'un côté, sortantes de l'autre, de même taille pour la rotation ; compteur exactement 2 ou 0 parce que ces champs sont très simples ;
- incompressible : divergence nulle ; une tache transportée garde son aire, son volume dans l'espace ; l'eau d'une rivière se comporte presque ainsi ;
- circulation, dans le sens trigonométrique ; vorticité ; formule aux rôles croisés ; rotationnel nommé comme la flèche 3D, qui sort de l'écran pour un écoulement plan ;
- roue à aubes à la moitié de la vorticité ; la vorticité vaut deux fois la vitesse de rotation sur place ;
- cisaillement : lignes droites, vorticité moins un, roue dans le sens horaire à un demi ;
- tourbillon ponctuel : vitesse en un sur la distance au centre ; hors du centre, la roue ne tourne pas sur elle-même, compensation exacte pour cette façon précise de ralentir ; toute la rotation au centre, où la vitesse devient infinie ; même circulation pour tout cercle qui entoure le centre, zéro pour un cercle qui ne l'entoure pas ;
- des lignes droites peuvent tourner, des lignes courbes peuvent ne pas tourner ;
- la limite rendue visible : dans une cellule, la circulation par unité d'aire se stabilise sur la vorticité au centre du cercle.

Seulement annoncé dans ep01, expliqué dans ep02 :

- l'énigme des cellules : flux nul partout, « ce n'est pas un hasard », « pourquoi ? » ; ep01 ne dit rien de la fonction de courant et n'affiche pas $\psi$ ;
- « garde cette image » sur le tourbillon ponctuel, repris par le carrelage et par la charge ;
- « on passera du petit cercle à toute une région » ;
- le but du parcours, en une phrase : plus tard, des machines dessineront de telles cartes, et il faudra juger si elles sont physiquement crédibles.

### ep02, « Le bord, l'aimant et la carte des hauteurs », module 1

Défini et expliqué, à ne plus réexpliquer :

- théorème de Green-Ostrogradski et théorème de Stokes dans le plan, par le carrelage, l'égalité valant à la limite de carreaux de plus en plus petits ; énoncés en mots puis complets à l'écran ; « le bord raconte l'intérieur » ;
- le tourbillon ponctuel expliqué : l'anneau entre deux cercles a une vorticité nulle, donc même circulation ;
- passage du plan à l'espace : le cercle devient sphère, l'aire un volume, le carreau un cube, le bord une surface fermée, la peau d'un ballon ;
- champ magnétique, celui d'un aimant, qui oriente une boussole ; divergence nulle en tout point, équivalente à un flux nul à travers n'importe quelle surface fermée ; pas de monopôle ;
- champ d'une charge : sur une sphère centrée, il traverse bien en face avec la même intensité partout ; intensité divisée par quatre et aire multipliée par quatre quand le rayon double ; flux quatre pi ; divergence nulle hors de la charge, source cachée dans le point ; une sphère à côté a un flux nul ;
- petit aimant : dipôle, champ dipolaire, lignes sans début ni fin, flux nul pour toute sphère ; limaille de fer ;
- la question des deux cartes, et sa réponse ;
- gradient : vers la montée la plus raide, perpendiculaire aux lignes de niveau, plus long où la pente est forte ;
- fonction de courant, flèche de pente tournée d'un quart de tour dans le sens horaire ; divergence nulle par construction car l'ordre des dérivations ne compte pas pour une carte assez lisse ; lignes de courant égales aux lignes de niveau ;
- résolution de l'énigme : la boîte à œufs donne les cellules ; bosses dans le sens trigonométrique, creux dans le sens horaire ; vorticité égale à deux fois la fonction de courant, calcul laissé au spectateur ;
- potentiel magnétique, $\mathbf{B} = \nabla^\perp a$ en 2D, même geste, flux nul à travers n'importe quel contour fermé du plan ;
- limite dite : la construction garantit la divergence nulle, pas la ressemblance avec un vrai champ ; une carte au hasard donne un champ sans divergence mais sans réalisme ; juger un champ viendra plus tard.

Seulement nommé, pas expliqué, donc encore à faire :

- la projection : « partir d'un champ quelconque et lui retirer la partie qui diverge », annoncée pour le chapitre 6 du module ;
- les machines qui dessinent la fonction de courant pour la vitesse de fluides en deux dimensions, bien plus agités que les cellules : une phrase, sans nom propre à l'oral ; légende « Wang et al., FunDiff, Nature Communications, 2026 », sur la carte de vitesse seulement, jamais sur la carte du champ magnétique. Rien n'a été dit des modèles génératifs eux-mêmes.

## 5. Non abordé, laissé au texte du module

Laplacien, y compris $\omega = -\Delta\psi$ et $j = -\Delta a$ ; coordonnées cylindriques ; notation indicielle et identités vectorielles ; équation d'induction ; potentiel vecteur 3D et jauge ; décomposition poloïdale-toroïdale ; lemme de Poincaré et topologie ; Fourier ; Helmholtz-Hodge et projection de Leray ; expérience E2. Le film n'a pas affirmé que tout champ sans divergence s'écrit $\nabla^\perp\psi$.

Aucun chiffre d'expérience cité dans ep01 ni dans ep02.
