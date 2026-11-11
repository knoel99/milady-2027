# Bible de continuité du film

Ce fichier dit ce que le film a déjà défini, noté, montré et expliqué. Un épisode suivant ne le réexplique pas et ne le contredit pas. Il le rappelle au plus d'une phrase.

## 1. Vocabulaire imposé

- On dit « renversement » du champ, comme le parcours écrit, jamais « inversion », dans la voix comme à l'écran.
- « Bascule » est réservé au double puits. Jamais pour le champ.
- Par prudence, la voix évite aussi « inverse » et « inversement » : on dit « contraire aux aiguilles d'une montre », « diminue comme un sur la distance ».
- « Dipôle » : le petit aimant lui-même ; son champ est un « champ dipolaire ». On ne dit plus « le champ s'appelle un dipôle ». Ses lignes n'ont « ni début ni fin ». On ne dit jamais « les lignes se referment toujours ».
- « Monopôle » : pôle magnétique isolé, qui n'existe pas. Formulation de ep01 : aucun point ne peut être le départ ou l'arrivée d'une gerbe de lignes.
- « Aubes » : seul mot pour la roue et ses parties, jamais « pales ».
- Critère magnétique : en 3D, « flux nul à travers n'importe quelle surface fermée » ; dans le plan, « flux nul à travers n'importe quel contour fermé du plan ». Le critère porte sur le champ que montre la carte, dans l'espace, pas sur la carte elle-même.

## 2. Ton

- Tutoiement du spectateur : « prends », « regarde », « garde la question ». Le « on » sert pour les définitions et les raisonnements.
- Phrases courtes, une idée par phrase. Pas de tiret cadratin, pas de parenthèses.
- Les formules se disent en mots, jamais en LaTeX dans la voix.

## 3. Notations et lectures à voix haute

Conformes à `docs/specs/notations.md`.

| Objet | Écran | Voix |
|---|---|---|
| Vitesse, composantes | $\mathbf{u} = (u_x, u_y)$ | « u », « u x », « u y » |
| Champ magnétique | $\mathbf{B}$ | « B » |
| Dérivée partielle | $\partial_x u_x$ | « d rond u x sur d rond x » |
| Divergence | $\nabla\cdot\mathbf{u}$ | « la divergence », ou « nabla point B » |
| Vorticité 2D | $\omega = \partial_x u_y - \partial_y u_x$ | « oméga » ; « d rond u y sur d rond x, moins d rond u x sur d rond y » |
| Rotationnel | $\nabla\times\mathbf{u}$ | « le rotationnel de la vitesse » |
| Gradient | $\nabla\psi = (\partial_x\psi, \partial_y\psi)$ | « le gradient de psi » |
| Fonction de courant | $\psi$ | « psi » |
| Champ tourné | $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$ | « nabla perpendiculaire psi » |
| Potentiel magnétique 2D | $a$, $\mathbf{B} = \nabla^\perp a$ | « a », « B égale nabla perpendiculaire a » |
| Flux de la charge | $4\pi$ | « quatre pi » |
| Tourbillon ponctuel | $\lvert\mathbf{u}\rvert = 1/r$, $r$ distance au centre | « un sur la distance au centre » |
| Écoulement cellulaire | $\mathbf{u} = (\sin x\cos y, -\cos x\sin y)$ | non dite ; à l'écran seulement |
| Rotation solide | $(-y, x)$ | « la flèche moins y, x », toujours montrée à l'écran |

Conventions de sens, à ne jamais contredire à l'écran :

- la circulation se calcule en parcourant le cercle dans le sens trigonométrique ;
- $\nabla^\perp$ tourne le gradient d'un quart de tour dans le sens des aiguilles d'une montre ; les grandes valeurs de $\psi$ sont à gauche du courant ;
- dans l'écoulement cellulaire $\psi = \sin x \sin y$, les cellules où $\psi > 0$ tournent dans le sens trigonométrique ; les droites $x = k\pi$ et $y = k\pi$ les séparent ;
- dans le cisaillement $(y, 0)$, les flèches vont à droite en haut, à gauche en bas ; la roue tourne dans le sens horaire.

## 4. Motifs récurrents

- **Le petit cercle en tirets.** L'objet central de ep01. Il pose deux questions, « est-ce que ça sort ? » pour le flux et « est-ce que ça tourne ? » pour la circulation. On le promène, on le fait rétrécir, on le multiplie en carrelage, on le gonfle en sphère. En 3D, les cercles en tirets des cartes sont des sphères vues en coupe.
- **Le compteur.** Affiché à côté du cercle : « flux sortant divisé par l'aire » ou « circulation divisée par l'aire ». Jamais de compteur 2D sur une carte qui représente une coupe 3D : là, seulement les valeurs 4π et 0.
- **La roue à aubes.** Détecteur de rotation locale ; elle tourne à oméga divisé par deux, énoncé suivi aussitôt de l'exemple de la rotation solide. Dans le cisaillement, elle est posée sur la ligne du milieu. Ne jamais la poser sur le centre du tourbillon ponctuel. Dans ce tourbillon, elle se déplace comme une nacelle de grande roue.
- **Formules à l'écran.** Quand la voix dit une formule ou des composantes, l'écran l'affiche au même moment.
- **L'écoulement cellulaire** $\psi = \sin x \sin y$. Fil de ep01 : énigme à l'idée 1, flux nul partout ; limite visible à l'idée 2, la circulation divisée par l'aire se stabilise ; solution à l'idée 4, il est fabriqué par une fonction de courant.
- **Le carrelage.** Les côtés intérieurs se compensent par paires, il ne reste que le bord : « le bord raconte l'intérieur ».
- **Les deux cartes d'ouverture.** Charge à gauche, petit aimant étendu à droite, jamais un dipôle ponctuel. Elles portent dès le début des cercles en tirets, révélés à l'idée 3 comme des sphères vues en coupe. La carte de l'aimant passe le test, celle de la charge échoue.
- **La carte de randonnée.** $\psi$ lue comme une altitude, lignes de niveau, gradient vers la montée la plus raide.

## 5. Termes définis et ce qui a été expliqué

### ep01, module 1 « Calcul vectoriel et analyse de Fourier »

Défini et expliqué, à ne plus réexpliquer :

- champ vectoriel, ligne de champ, ligne de courant ;
- dérivée partielle : dériver en x en gardant y fixe ;
- flux à travers un cercle : somme des parts perpendiculaires au bord, comptées en plus vers l'extérieur ;
- divergence : flux divisé par l'aire, à la limite du petit cercle ; formule 2D obtenue sur un petit carré : le flux par un côté vaut la flèche fois la longueur du côté, on divise par l'aire du carré, il reste l'écart par unité de longueur, la dérivée ; droite moins gauche, haut moins bas ;
- source $(x, y)$ de divergence 2, rotation solide $(-y, x)$ de divergence 0 et de vorticité 2 ; cercle déplacé : flèches entrantes d'un côté, sortantes de l'autre, de même taille pour la rotation ;
- incompressible : divergence nulle, ni aire ni volume créé ou détruit ; raison donnée : si rien ne sort d'aucun petit cercle, une tache de fluide transportée garde son aire ;
- circulation, vorticité oméga, rotationnel nommé comme sa version 3D ; la roue tourne à oméga divisé par deux ; la vorticité vaut deux fois la vitesse de rotation locale ;
- cisaillement $(y, 0)$ : lignes droites, oméga égale moins un, la roue tourne ;
- tourbillon ponctuel : vitesse un sur la distance au centre ; lignes circulaires, la roue ne tourne pas sur elle-même hors du centre, la compensation entre vitesse et courbure étant exacte pour cette décroissance précise ; toute la rotation est au centre, où la vitesse devient infinie ; tout cercle qui entoure le centre donne la même circulation ; des lignes courbes ne veulent pas dire que le fluide tourne sur lui-même ;
- théorème de Green-Ostrogradski et théorème de Stokes, par le carrelage, l'égalité valant à la limite de carreaux de plus en plus petits ; énoncés complets à l'écran ; passage du plan à l'espace, le cercle devient sphère, l'aire devient volume, le bord devient surface fermée ;
- nabla point B nommé comme la divergence de B ; divergence de B nulle équivaut à un flux nul à travers toute surface fermée ; pas de monopôle ; un petit aimant est un dipôle, son champ est un champ dipolaire ;
- champ d'une charge : sur une sphère centrée, il traverse bien en face avec la même intensité partout, un sur R au carré, ce qui permet le produit par quatre pi R au carré ; flux quatre pi ; divergence nulle hors de la charge, source concentrée au point ;
- gradient : vers la montée la plus raide, perpendiculaire aux lignes de niveau ;
- fonction de courant psi, $\nabla^\perp\psi$, divergence nulle par construction car l'ordre des dérivations ne compte pas pour psi assez lisse ; lignes de courant égales aux lignes de niveau ;
- $\psi = \sin x \sin y$ : cellules, formule de la vitesse montrée à l'écran dès l'idée 1, vorticité égale à deux fois psi, dite comme un calcul court laissé au spectateur ;
- potentiel magnétique a, $\mathbf{B} = \nabla^\perp a$ en 2D ;
- limite dite : la construction garantit la divergence nulle, pas la ressemblance avec un vrai champ ; juger un champ viendra plus tard.

Seulement nommé, pas expliqué, donc encore à faire :

- la projection : « partir d'un champ quelconque et lui retirer la partie qui diverge », annoncée pour le chapitre 6 du module ;
- les machines qui dessinent psi pour la vitesse d'un fluide 2D, sur des écoulements bien plus agités que les cellules : une phrase, sans nom propre à l'oral ; légende « Wang et al., FunDiff, Nature Communications, 2026 », sur la carte de vitesse seulement, jamais sur la carte de B. Rien n'a été dit des modèles génératifs eux-mêmes ; l'ouverture annonce seulement qu'il faudra juger si les champs qu'ils dessinent sont physiquement crédibles.

Non abordé dans ep01, laissé au texte du module : laplacien, y compris $\omega = -\Delta\psi$ et $j = -\Delta a$ ; coordonnées cylindriques ; notation indicielle et identités vectorielles ; équation d'induction ; potentiel vecteur 3D et jauge ; décomposition poloïdale-toroïdale ; lemme de Poincaré et topologie ; Fourier ; Helmholtz-Hodge et projection de Leray ; expérience E2. Le film n'a pas affirmé que tout champ sans divergence s'écrit $\nabla^\perp\psi$.

Aucun chiffre d'expérience cité dans ep01.
