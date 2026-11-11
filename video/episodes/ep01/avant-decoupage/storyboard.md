# Épisode 01 : storyboard

Narration : `video/episodes/ep01/narration.md`, validée (environ 2 190 mots). Traitement : `video/episodes/ep01/traitement.md`. Bible : `video/continuite.md`. Retours : `video/episodes/ep01/retours.md` (enchaîner, trancher soi-même les points mineurs).

19 scènes, de 26 à 66 s, durée totale estimée à 14 min 34 s à 150 mots par minute, sans compter les pauses `hold_after` du script.

## 0. Conventions communes à toutes les scènes

**Repères.** Chaque plan commence sur le repère entre crochets de la narration, qui sert de nom de cue au moteur. Les durées sont estimées à 0,4 s par mot ; le moteur les recale sur la voix. Un plan dure jusqu'au repère du plan suivant.

**Registre.** NIGHT pour tout l'épisode (fond `--bg`). Pas de PAPER : aucune page du site n'est citée à l'écran.

**Coordonnées.** Tous les champs se calculent analytiquement dans la page, en coordonnées mathématiques, **y vers le haut**. Chaque scène définit une fonction `toPx(x, y)` qui renverse l'axe vertical pour l'écran. C'est une condition des contraintes de sens : sans ce renversement de l'axe, les cellules où ψ > 0 tourneraient dans le sens horaire à l'écran et les grandes valeurs de ψ passeraient à droite du courant. Le constructeur le vérifie sur une image fixe de la scène 06 (cellule en bas à gauche, ψ > 0, sens trigonométrique). Les déplacements donnés en px sont, eux aussi, comptés y vers le haut.

**Notations.** La région s'écrit $D$ et son bord $\partial D$, partout, jamais $\Omega$ : la lettre Ω est réservée à $\Omega_{\text{roue}}$, la vitesse angulaire de la roue.

**Couleurs.**

| Rôle | Jeton |
|---|---|
| Vitesse u, flèches et lignes de courant, vorticité ω, carte de ψ | `--u` (cartes scalaires : `Kit.cmap('u')`, argent pour le négatif, `--u-hi` pour le positif) |
| Champ magnétique B, lignes de B, carte de a | `--b` (cartes : `Kit.cmap('b')`) |
| Cercles en tirets, carreaux, sphères, cubes, roue à aubes, flèche de gradient avant le quart de tour, flèche de parcours | `--chalk` |
| Annotations, étiquettes d'axes, part de flèche « qui ne compte pas » | `--muted` |
| Champ de la charge électrique, et carte de l'aimant tant qu'elle n'est pas nommée | `--fg-2`, couleur neutre (voir la section 5, point 6) |
| Matière de l'aimant | `--matter` pour le corps ; bout nord teinté `--b`, bout sud `--matter-dark`, comme l'aiguille M1 |

**Zones.** Contenu dans le cadre sûr (x de 96 à 1824, y de 56 à 880) ; rien sous y = 880. Calque de formule (`Kit.formulaLayer`) en bas à droite pour les formules non dites ; bandeau (`Kit.lowerThird`) en bas à gauche pour la référence FunDiff. Les formules que la voix dit s'écrivent en grand avec `Kit.equation`, au moment où la voix les dit.

**Mouvement.** Tout est une fonction pure du temps : trajectoires des cercles paramétrées par t, rotation de la roue intégrée en forme fermée, traceurs par `Kit.tracers` (Scene.stepper).

**Compteurs.** Les flux et circulations affichés par un compteur se calculent dans la page, à chaque image, par quadrature sur 256 points du bord : somme des parts perpendiculaires (ou tangentes) pondérées par l'élément d'arc $\lvert\gamma'(s)\rvert\,\Delta s$, normale orientée vers l'extérieur, parcours dans le sens trigonométrique. Ils sont exacts à l'arrondi affiché, pas au-delà. L'affichage n'écrit jamais « −0 » : une valeur qui s'arrondit à zéro s'écrit « 0 ». Les valeurs 2π, 4π et 0 des scènes 10, 14 et 15 ne sont pas des compteurs : ce sont des valeurs symboliques, écrites et non calculées, posées sans chiffre qui défile.

**Longueur des flèches.** Direction exacte ; longueur donnée par une compression strictement croissante de l'intensité I, linéaire sous un seuil I_s :

- L(I) = k·I si I ≤ I_s ;
- L(I) = k·I_s·(2 − I_s/I) si I > I_s.

La fonction est continue, de pente continue, et tend vers 2·k·I_s sans jamais l'atteindre : il n'y a pas de plafond dur, et « plus longue » veut toujours dire « plus forte ». Sous le seuil, les rapports de longueur sont exacts. Un petit disque vide entoure chaque point singulier. Seuils imposés :

- scène 14 (et carte de la charge des scènes 01 et 15, même unité, 120 px pour R = 1) : I_s = 1,2, au-dessus de l'intensité 1 à R = 1, pour que les flèches des sphères R = 1, 2, 3 se lisent exactement 1, 1/4, 1/9 ;
- scène 10 (unité 100 px, roue de rayon a = 0,5 sur l'orbite R = 2,2) : I_s = 0,8, au-dessus de 1/(R − a) ≈ 0,59, pour que le rapport des deux flèches de 10.7 soit exact ;
- ailleurs, le constructeur prend I_s au-dessus de toutes les intensités des flèches que la voix compare.

Le gain k peut changer d'un jeu de flèches à l'autre (grille, flèches de bord), jamais le seuil d'une même scène.

**Texte à l'écran.** Aucune phrase de la voix n'est recopiée. L'écran porte des formules, des valeurs de compteur, des étiquettes d'une ou deux unités (« ψ », « a », « ω = −1 »), des pictogrammes. Étiquettes mono en capitales par `Kit.upper` (les lettres grecques gardent leur casse). Décimales à la virgule (voir la section 5, point 2).

**Badge d'honnêteté.** Aucun dans l'épisode, qui ne cite aucun résultat mesuré, sauf à la scène 17 : SCHEMATIC pour toute la scène 17, du premier au dernier plan. Pas de badge CONTEXT, nulle part : au plan [c-machines], le bandeau de référence porte seul la référence. Si le moteur exige un badge pour chaque scène, SCHEMATIC partout.

**Motifs.** Le petit cercle en tirets est le même objet d'un bout à l'autre : même tiret (12 px plein, 9 px vide), même épaisseur (3 px), même `--chalk`. Le compteur est toujours à droite du cercle ou sous le panneau, en chiffres tabulaires.

## 1. Découpage en scènes

| Scène | Fichier | Paragraphes | Mots (env.) | Durée | Composants |
|---|---|---|---|---|---|
| ep01.01 | `01_cartes.html` | P1, P2 | 103 | 42 s | `Kit.arrows`, SVG (cercles, aimant), pictogrammes en code de scène |
| ep01.02 | `02_vocabulaire.html` | P3 | 93 | 38 s | `Kit.arrows`, `Kit.fieldLines`, `Kit.equation` |
| ep01.03 | `03_flux.html` | P4, P5 | 127 | 51 s | `Kit.arrows`, cercle-sonde, `Kit.equation` |
| ep01.04 | `04_carre.html` | P6 | 93 | 38 s | SVG, `Kit.equation`, `Kit.morph` |
| ep01.05 | `05_source_rotation.html` | P7, P8 | 122 | 49 s | `Kit.arrows` ×2, `Kit.equation` ×2, cercle-sonde ×2, compteur ×2 |
| ep01.06 | `06_incompressible.html` | P9, P10 | 108 | 44 s | `Kit.arrows`, `Kit.streamlines`, cercle-sonde, compteur, `Kit.formulaLayer` |
| ep01.07 | `07_circulation.html` | P11, P12 | 121 | 49 s | cercle-sonde, `Kit.equation`, SVG en perspective, roue à aubes |
| ep01.08 | `08_rotation_solide.html` | P13 | 65 | 27 s | `Kit.arrows`, `Kit.tracers`, roue à aubes, compteur, `Kit.equation` |
| ep01.09 | `09_cisaillement.html` | P14 | 87 | 35 s | `Kit.arrows`, `Kit.fieldLines`, roue à aubes, compteur, `Kit.equation` |
| ep01.10 | `10_tourbillon.html` | P15, P16, P17 | 155 | 63 s | `Kit.arrows`, `Kit.fieldLines`, roue à aubes, cercles, `Kit.equation` |
| ep01.11 | `11_cellules_limite.html` | P18 | 68 | 28 s | `Kit.streamlines`, cercle-sonde, compteur, `Kit.plot` |
| ep01.12 | `12_carrelage.html` | P19, P20 | 125 | 51 s | SVG (carreaux, flèches de flux), `Kit.equation` ×2 |
| ep01.13 | `13_espace.html` | P21, P22 | 162 | 65 s | SVG/canvas (sphère, cubes), `Kit.fieldLines`, `Kit.equation`, `Kit.pen` |
| ep01.14 | `14_charge.html` | P23, P24 | 135 | 54 s | `Kit.arrows`, SVG (sphères, calottes), tableau en code de scène |
| ep01.15 | `15_aimant_verdict.html` | P25, P26 | 94 | 38 s | lignes de niveau (de r·A_φ), traceur, SVG, `Kit.pen` |
| ep01.16 | `16_randonnee.html` | P27, P28 | 154 | 62 s | `Kit.fieldMap`, lignes de niveau, `Kit.equation` |
| ep01.17 | `17_construction.html` | P29, P30, P31 | 164 | 66 s | `Kit.badge` (SCHEMATIC), `Kit.equation`, `Kit.morph`, `Kit.fieldMap`, `Kit.arrows`, lignes de niveau, cercle-sonde, `Kit.formulaLayer`, `Kit.lowerThird`, `Kit.chip` |
| ep01.18 | `18_potentiel.html` | P32, P33 | 100 | 41 s | `Kit.fieldMap`, lignes de niveau, `Kit.equation`, cercle-sonde (contour quelconque), compteur, `Kit.pen` |
| ep01.19 | `19_cloture.html` | P34, P35 | 92 | 40 s | pictogrammes, `Kit.equation`, `Kit.projector`, `Kit.chip` |
| **Total** | | P1 à P35 | 2 190 | **14 min 34 s** | |

« Cercle-sonde », « compteur », « roue à aubes » et « lignes de niveau » sont des composants proposés (section 5). Tant qu'ils ne sont pas acceptés, ils s'écrivent en code de scène, avec la même apparence partout.

## 2. Plans

### ep01.01 · `01_cartes.html` · P1, P2 · 42 s

Deux panneaux carrés de 760 px, à gauche (x 136 à 896) et à droite (x 1024 à 1784), y 80 à 840. Sans titre ni étiquette.

- Gauche : champ d'une charge ponctuelle au centre du panneau, E = r̂ / r² (unité : 120 px), flèches sur une grille 13 × 13, couleur `--fg-2`, longueur compressée (section 0, I_s = 1,2), disque vide de 40 px autour de la charge, point `--fg` au centre.
- Droite : champ d'un **petit aimant étendu**, vu dans un plan qui contient son axe. Aimant : rectangle vertical de 60 × 180 px, nord en haut. Champ calculé comme celui d'un cylindre uniformément aimanté, c'est-à-dire d'une pile de 24 spires de courant, par Biot–Savart en quadrature sur 64 points par spire, dans `setup`. Le noyau de Biot–Savart est **régularisé** : 1/(|r|² + ε²)^{3/2} au lieu de 1/|r|³, avec ε = 5 px ; en plus, les points de grille à moins de 10 px d'une spire sont masqués. Aucune flèche géante près des bords de l'aimant. Flèches sur la même grille, couleur `--fg-2`, longueur compressée avec un seuil pris au-dessus de l'intensité au centre de l'aimant, y compris à l'intérieur de l'aimant, où elles vont du sud vers le nord. Jamais de dipôle ponctuel.
- Sur chaque carte, deux cercles en tirets `--chalk` : à gauche, l'un centré sur la charge (rayon 150 px), l'autre déplacé en haut à droite, centre à (204, 204) px de la charge, rayon 120 px, qui ne l'entoure pas ; à droite, l'un centré sur l'aimant et qui l'entoure entièrement (rayon 170 px), l'autre déplacé en haut à droite. Aucune valeur ni compteur sur ces cercles.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 1.1 | [o-cartes] | Les deux panneaux, vides, cadre `--matter`. | Les flèches poussent depuis leur pied (`Kit.arrows`, entrée 0,5 s), panneau gauche puis droit à 0,3 s d'écart. | 2 s |
| 1.2 | [o-fleche] | Zoom à 2,5× sur une flèche du panneau gauche, cerclée par `Kit.pen` (circle) ; à côté, deux flèches de même direction et de longueurs différentes, pour « plus long = plus fort ». | Zoom caméra de 0,8 s vers la flèche, maintien, retour au plan large à la fin du plan. | 5 s |
| 1.3 | [o-gauche] | Plan large ; panneau droit à 40 %. | Fondu de 0,3 s. Aucune étiquette « charge » : l'image ne dit pas laquelle est laquelle. | 3 s |
| 1.4 | [o-droite] | Panneau gauche à 40 %, panneau droit à 100 %. | Fondu croisé de 0,3 s. | 2,5 s |
| 1.5 | [o-question] | Les deux panneaux à 100 % ; les quatre cercles en tirets se dessinent. Entre les panneaux, un point d'interrogation `--chalk` de 120 px. | Cercles tracés au trait en 0,8 s (dasharray), l'un après l'autre. | 6 s |
| 1.6 | [o-machine] | Les deux cartes se réduisent à 40 % et glissent en haut à gauche, où elles restent en vignette. Au centre, une troisième carte, vide, cadre en tirets `--muted` : la place d'un champ « à juger ». | Réduction de 0,8 s ; la carte vide s'ouvre par un fondu. Pas de violet `--model` : la machine n'est pas encore présentée. | 7 s |
| 1.7 | [o-plan] | La carte vide s'efface ; trois emplacements numérotés 1, 2, 3 (mono `--muted`), en colonne, à gauche du centre. | Apparition des numéros. | 2,5 s |
| 1.8 | [o-local] | Pictogramme 1 : un petit cercle en tirets avec deux flèches qui le traversent vers l'extérieur, à côté du même cercle avec une flèche de parcours circulaire. | Les flèches poussent ; la flèche de parcours fait un tour, sens trigonométrique. | 6 s |
| 1.9 | [o-global] | Pictogramme 2 : un carrelage de 3 × 2 carreaux dont le contour s'épaissit, puis une sphère en tirets. | Carrelage, puis morphose carré vers sphère en 1 s. | 4,5 s |
| 1.10 | [o-fabriquer] | Pictogramme 3 : quelques lignes de niveau et une flèche qui pivote d'un quart de tour pour devenir tangente. | Rotation de la flèche en 0,8 s, sens horaire. | 3,5 s |

Les trois pictogrammes reviennent à la scène 19, chacun avec sa formule.

### ep01.02 · `02_vocabulaire.html` · P3 · 38 s

Grand panneau central de 1200 × 720 px. Champ de démonstration lisse et sans symétrie, u = (0,6 + 0,4 sin(x + 0,5 y), 0,3 cos x), flèches `--u` sur grille 14 × 9. Sa composante $u_x$ dépend de x : le graphe de 2.5 n'est pas plat.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 2.1 | [d-vocabulaire] | Panneau vide, cadre `--matter`. | Fondu d'entrée. | 3 s |
| 2.2 | [d-vectoriel] | Les flèches apparaissent une à une, en balayage de gauche à droite. | Entrée échelonnée sur 3 s (`Kit.arrows` par colonnes). | 7,5 s |
| 2.3 | [d-lignes] | Trois lignes de champ `--u` (2,5 px) tracées depuis trois graines à gauche ; les flèches baissent à 50 %. | `Kit.fieldLines`, tracé progressif en 2 s ; une flèche sur chaque ligne se pose tangente, pour montrer que la ligne suit les flèches. | 8,5 s |
| 2.4 | [d-composantes] | Une flèche agrandie à droite du panneau, sur deux axes `--muted` ; ses deux composantes en tirets `--u`, horizontale puis verticale, étiquetées $u_x$ et $u_y$. | Projection des deux composantes en 0,5 s chacune. | 5 s |
| 2.5 | [d-partielle] | Une ligne horizontale `--chalk` (y fixé, y = 1) traverse le panneau ; un point glisse le long de cette ligne ; au-dessus, un petit graphe de $u_x(x, 1) = 0{,}6 + 0{,}4\sin(x + 0{,}5)$ en fonction de x, une ondulation, dont la pente au point courant est une tangente `--chalk`. | Le point glisse de gauche à droite en 6 s ; la tangente suit et change d'inclinaison. La ligne ne bouge pas verticalement : y reste fixe. | 8,5 s |
| 2.6 | [d-drond] | La formule $\partial_x u_x$ s'écrit sous le graphe, accolade sous la pente. | `Kit.equation`, révélation en 0,45 s. | 5 s |

### ep01.03 · `03_flux.html` · P4, P5 · 51 s

Champ u = (x − 0,4 y, y + 0,4 x), flèches `--u` : il sort et tourne un peu, donc chaque flèche du bord a une part perpendiculaire et une part le long du bord. Panneau de 900 × 720 px, à gauche (x 120 à 1020, y 100 à 820) ; colonne d'équation à droite, x 1180 à 1780. Le point P est l'origine du champ, où u = 0 ; il n'est pas au centre du panneau mais en haut à droite, à l'écran en (620, 340), pour que le cercle déplacé de 3.6 tienne dans le panneau.

Calcul du plan 3.6. Pour un cercle de centre c et de rayon R, la part perpendiculaire vaut, au point de normale n, n·(A c) + R, où A est la matrice du champ ; elle entre là où n·(A c) < −R. Comme |A c| = 1,077 |c|, il faut |c| > R/1,077 ≈ 167 px pour R = 180 px. Avec c = (−212, −212) px, soit 300 px vers le bas à gauche, l'arc entrant fait environ 112°, du côté qui fait face à P (en haut à droite du cercle), soit 5 des 16 points si le premier point est à 0°. Le cercle déplacé est centré à l'écran en (408, 552) : il occupe x 228 à 588 et y 372 à 732, flèches comprises au plus x 148 et y 812, dans le panneau.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 3.1 | [d-source] | Le champ ; le point P `--chalk` clignote une fois. | Pulsation de 0,4 s. | 3 s |
| 3.2 | [d-cercle] | Cercle en tirets centré sur P, rayon 180 px. | Tracé au trait en 0,8 s. | 3,5 s |
| 3.3 | [d-decompose] | Les flèches de la grille baissent à 25 %. Une flèche posée sur le bord, à 40° au-dessus de l'horizontale. | La flèche pousse depuis son pied. | 4,5 s |
| 3.4 | [d-travers] | Sa part perpendiculaire au bord, en `--u` plein, le long du rayon. | La part se détache de la flèche en 0,5 s. | 6 s |
| 3.5 | [d-longe] | Sa part le long du bord, en tirets `--muted`, tangente au cercle. | Détachement, puis la part tangente baisse à 40 %. | 3,5 s |
| 3.6 | [d-signe] | Seize points répartis sur le bord (premier point à 0°), chacun avec sa part perpendiculaire seule : vers l'extérieur avec un petit « + » `--chalk`, vers l'intérieur avec un « − » `--muted`. | Les seize parts poussent en un tour, sens trigonométrique, en 1,5 s. Centré sur P, toutes sortent. Pour faire voir le « − », le cercle glisse de 300 px vers le bas à gauche (212 px à gauche, 212 px en bas) en 1 s, parts recalculées à chaque image : cinq parts entrent, sur l'arc qui fait face à P. Maintien de 1,5 s, puis retour en 1 s. | 6 s |
| 3.7 | [d-flux] | À droite, l'équation commence : terme « flux » écrit $\text{flux}$, avec une accolade qui rassemble les seize parts (un arc `--chalk` qui fait le tour du cercle). | L'arc fait le tour en 1 s ; le terme s'écrit au bout. | 5 s |
| 3.8 | [d-aire] | Le disque se remplit d'un voile `--chalk` à 12 % ; le terme $\div\ \pi r^2$ s'ajoute. | Remplissage radial en 0,6 s. | 5 s |
| 3.9 | [d-limite] | Le cercle rétrécit vers P jusqu'à 20 px ; le terme $\lim_{r\to 0}$ s'ajoute devant. | Rayon de 180 à 20 px en 2,5 s (inOutCubic). | 3 s |
| 3.10 | [d-divergence] | L'équation complète : $\nabla\cdot\mathbf{u}(P) = \lim_{r\to0} \dfrac{\text{flux}}{\pi r^2}$. | Le membre de gauche s'écrit. | 4,5 s |
| 3.11 | [d-positive] | Sous l'équation, vignette 1 : un point avec quatre flèches qui en partent, étiquette $\nabla\cdot\mathbf{u} > 0$. | Les flèches poussent. | 4,5 s |
| 3.12 | [d-negative] | Vignette 2 à côté : quatre flèches qui arrivent, $\nabla\cdot\mathbf{u} < 0$. | Les flèches poussent vers le point. | 2 s |

### ep01.04 · `04_carre.html` · P6 · 38 s

Grand carré `--chalk` de 360 px, à gauche (centre x 560, y 470), centré sur l'origine du champ. Champ u = (0,5 + 0,6 x, 0,4 + 0,5 y) : $u_x$ croît vers la droite, $u_y$ croît vers le haut. **Échelle : 300 px par unité**, donc le côté vaut h = 1,2 < 1,6 en unités du champ. Ainsi, au milieu de chaque côté, la flèche garde le sens annoncé : $u_x$ = 0,14 à gauche (elle entre) et 0,86 à droite (elle sort) ; $u_y$ = 0,10 en bas (elle entre) et 0,70 en haut (elle sort). Au-delà de h = 1,6, la flèche du bas changerait de sens. Colonne d'équation à droite (x 1000 à 1780).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 4.1 | [d-carre] | Le cercle en tirets se morphose en carré en tirets, même centre. | Morphose de 0,8 s. | 4 s |
| 4.2 | [d-cotes] | Côtés gauche et droit en trait plein `--chalk` ; haut et bas à 30 %. | Les deux côtés s'épaississent. | 3 s |
| 4.3 | [d-cote] | Flèche `--u` longue au milieu du côté droit, qui sort ; une accolade `--muted` sur la longueur du côté, étiquette $h$. Équation : $u_x(\text{droite})\times h$. | La flèche pousse, l'accolade se dessine, puis le terme. | 5 s |
| 4.4 | [d-ecart] | Flèche `--u` courte au milieu du côté gauche, qui entre (0,14 contre 0,86, même échelle). Les deux flèches se superposent au-dessus du carré, base contre base : leur différence est surlignée en `--chalk`. Équation : $\big[u_x(\text{droite}) - u_x(\text{gauche})\big]\times h$. | Les deux flèches glissent hors du carré, se superposent en 0,8 s ; l'écart s'allume. | 7 s |
| 4.5 | [d-variation] | Le carré se remplit d'un voile, étiquette $h^2$ ; l'équation devient $\dfrac{u_x(\text{droite}) - u_x(\text{gauche})}{h}$, puis, en dessous, le carré rétrécit et la fraction se change en $\partial_x u_x$. | `Kit.morph` de la fraction vers $\partial_x u_x$ pendant que le carré passe de 360 à 60 px (h de 1,2 à 0,2). | 9 s |
| 4.6 | [d-hautbas] | Le carré reprend 360 px (h = 1,2) ; côtés haut et bas en plein, flèche courte qui entre en bas, longue qui sort en haut. Le même geste se rejoue en accéléré, terme $\partial_y u_y$. | Rejeu en 3 s. | 6 s |
| 4.7 | [d-somme] | $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, centrée en grand, les deux termes venus de leurs places. | `Kit.morph` ; maintien jusqu'à la fin de la scène (1,5 s de pause conseillée). | 4 s |

### ep01.05 · `05_source_rotation.html` · P7, P8 · 49 s

Deux panneaux de 700 × 560 px côte à côte (x 140 à 840 et 1080 à 1780, y 200 à 760). Gauche : source u = (x, y). Droite : rotation u = (−y, x), sens trigonométrique. Flèches `--u`, grille 11 × 9. L'origine de chaque champ est à 20 px à gauche et 40 px sous le centre du panneau, à l'écran en (470, 520) et (1410, 520), pour que le cercle déplacé et ses flèches tiennent dans le panneau. Formules au-dessus de chaque panneau (y 80 à 180). Un compteur sous chaque panneau, libellé « FLUX ÷ AIRE ».

Géométrie des cercles déplacés. Rayon 130 px, centre final c = (200, 140) px depuis l'origine, à l'écran en (670, 380) et (1610, 380). Parts du bord à une échelle commune aux deux panneaux, la plus longue (gauche, dans la direction de c, |c| + R = 374 px de champ) dessinée à 30 px. Source : la part vaut n·c + R ; comme |c| ≈ 244 px > 130 px, environ 116° du bord, soit 5 des 16 points, ont une part entrante, du côté de l'origine, et les sortantes sont plus longues. Rotation : la part vaut n·(−c_y, c_x), sans terme en R : moitié entrante, moitié sortante, symétriques. Cercle et flèches restent dans le panneau (gauche : x 540 à 826, y 228 à 510 ; droite : x 1480 à 1760).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 5.1 | [d-deux] | Les deux cadres vides. | Fondu. | 1,5 s |
| 5.2 | [d-fuit] | Panneau gauche : flèches de la source ; au-dessus, $\mathbf{u} = (x, y)$. | Flèches poussant depuis l'origine vers l'extérieur ; formule écrite avec la voix. | 7,5 s |
| 5.3 | [d-vautdeux] | Sous la formule : $\nabla\cdot\mathbf{u} = 1 + 1 = 2$. | Écriture terme à terme (`reveal`). | 3 s |
| 5.4 | [d-rotation] | Panneau droit : flèches de la rotation ; $\mathbf{u} = (-y, x)$. | Les flèches poussent. | 6 s |
| 5.5 | [d-vautzero] | $\nabla\cdot\mathbf{u} = 0 + 0 = 0$. | Écriture terme à terme. | 3 s |
| 5.6 | [d-centre] | **Cercle centré** sur l'origine dans chaque panneau, rayon 130 px. Les flèches de la grille baissent à 30 %. | Tracé des deux cercles. | 3 s |
| 5.7 | [d-sortent] | Gauche : seize flèches sur le bord, toutes perpendiculaires et vers l'extérieur. | Elles poussent. | 4,5 s |
| 5.8 | [d-glissent] | Droite : seize flèches sur le bord, toutes tangentes, aucune part perpendiculaire. | Elles poussent ; un léger défilement le long du bord, sens trigonométrique. | 5 s |
| 5.9 | [d-promene] | Les deux cercles se promènent en même temps, sur la même trajectoire fermée et lisse, c(τ) = (20 + 180 cos 2πτ, 110 + 30 cos 4πτ) px, τ de 0 à 1 : elle part de l'origine du panneau vers c = (200, 140), fait sa boucle et **s'arrête en c = (200, 140)**, vitesse nulle à l'arrivée (τ en inOutCubic). Elle reste dans x de −160 à 200 px et y de 80 à 140 px : cercle et flèches dans le panneau. Les compteurs s'allument : 2 à gauche, 0 à droite. | Entrée de 0,4 s de l'origine vers c, puis boucle en 3,1 s ; les seize flèches du bord sont recalculées à chaque image ; les compteurs ne bougent pas. | 3,5 s |
| 5.10 | [d-entrent] | **Cercles déplacés**, arrêtés en c = (200, 140) px, en haut à droite de l'origine. Seules les parts perpendiculaires au bord restent, entrantes d'un côté, sortantes de l'autre. Droite : entrantes et sortantes de même longueur, symétriques. Gauche : cinq parts entrantes, courtes, du côté de l'origine ; les sortantes sont plus longues. | Arrêt doux (déjà acquis à la fin de 5.9) ; les parts tangentes s'effacent. | 4,5 s |
| 5.11 | [d-bilan] | Sous chaque cercle, les parts perpendiculaires se rangent en deux colonnes, entrantes contre sortantes : égales à droite, déséquilibrées à gauche. Compteurs : 2 et 0. | Les parts glissent dans leurs colonnes en 1 s. | 7,5 s |

### ep01.06 · `06_incompressible.html` · P9, P10 · 44 s

Plans 6.1 à 6.5 : les deux panneaux de la scène 05, mêmes origines. Plans 6.6 à 6.9 : écoulement cellulaire ψ = sin x sin y sur [0, 2π] × [0, 2π] (2 × 2 cellules), panneau de 1100 × 720 px centré. Flèches `--u` et lignes de courant `--u` à 45 %. Vérification de sens à faire sur image fixe : la cellule en bas à gauche (0 < x, y < π, ψ > 0) tourne dans le sens trigonométrique.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 6.1 | [d-compteur] | Les deux panneaux de la scène 05, cercles déplacés. | Les cercles changent de place et de rayon (de 60 à 200 px) en continu, sans sortir du panneau ; les compteurs restent sur 2 et 0, chiffres immobiles. | 6,5 s |
| 6.2 | [d-simple] | Les compteurs se figent ; les deux formules $\mathbf{u} = (x, y)$ et $\mathbf{u} = (-y, x)$ restent en haut, le reste baisse à 50 %. | Fondu. | 4 s |
| 6.3 | [d-incompressible] | Dans chaque panneau, une tache de fluide `--chalk` à 20 % (disque de 70 px, contour plein) posée loin de l'origine. À côté de chaque tache, une barre verticale « AIRE » qui suit l'aire de la tache. | Les taches sont transportées par leur champ, en forme fermée : à gauche, la tache s'éloigne et grossit, sa barre monte ; à droite, elle tourne autour de l'origine sans changer de taille, sa barre reste fixe. | 7 s |
| 6.4 | [d-tache] | Panneau droit agrandi ; la tache est couverte de petits cercles en tirets, chacun avec sa mention 0 en `--muted`. | Les petits cercles suivent la tache. | 6,5 s |
| 6.5 | [d-nomme] | La barre d'aire du panneau droit se surligne au `Kit.pen` (underline). | Trait de 0,4 s. | 1,5 s |
| 6.6 | [d-cellules] | Écoulement cellulaire : flèches puis lignes de courant fermées. Calque de formule en bas à droite, étiquette « CHAMP », $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$. | Lignes tracées en 1,5 s ; des traceurs (`Kit.tracers`, 300 particules, 40 %) font voir les cellules tourner côte à côte. | 7 s |
| 6.7 | [d-enigme] | Cercle en tirets de 90 px et compteur « FLUX ÷ AIRE » qui le suit. | Le cercle se promène sur une trajectoire fixée qui traverse plusieurs cellules et franchit les droites de séparation ; le compteur reste sur 0. | 5 s |
| 6.8 | [d-pourquoi] | Le cercle s'arrête ; point d'interrogation `--chalk` à côté du compteur. | Pulsation du compteur. | 3 s |
| 6.9 | [d-suspens] | Le point d'interrogation se réduit et va se loger dans le coin haut gauche, où il reste jusqu'à la fin de la scène. | Glissement de 0,8 s. | 3 s |

### ep01.07 · `07_circulation.html` · P11, P12 · 49 s

Même champ, même panneau, même point P et même cercle que la scène 03, u = (x − 0,4 y, y + 0,4 x), panneau à gauche. Colonne d'équation à droite. Vorticité de ce champ : ω = 0,4 − (−0,4) = 0,8 partout.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 7.1 | [r-tourne] | Le cercle de la scène 03, centré sur P, avec sa flèche décomposée. | Fondu d'entrée. | 4 s |
| 7.2 | [r-sens] | Une flèche de parcours `--chalk` court sur le cercle, sens trigonométrique, contraire aux aiguilles d'une montre. | Un tour en 2,5 s, puis elle reste posée en haut du cercle, pointe vers la gauche. | 5 s |
| 7.3 | [r-garde] | Rôles échangés : la part le long du bord passe en `--u` plein, la part perpendiculaire en tirets `--muted`. Puis seize parts tangentes autour du cercle, toutes dans le sens du parcours (ici elles le sont toutes). | Échange de style en 0,4 s, puis les seize parts poussent en un tour. | 7,5 s |
| 7.4 | [r-circulation] | Un arc `--chalk` rassemble les seize parts ; terme « circulation » à droite. | L'arc fait le tour en 1 s. | 3 s |
| 7.5 | [r-vorticite] | $\omega = \lim_{r\to0} \dfrac{\text{circulation}}{\pi r^2}$, même mise en page que la divergence de la scène 03. | Le cercle rétrécit vers P (de 180 à 20 px), qui n'est pas un point singulier : ce champ est linéaire. | 5,5 s |
| 7.6 | [r-formule] | En haut, rappel à 40 % : $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$. En dessous : $\omega = \partial_x u_y - \partial_y u_x$. Indices croisés mis en évidence : dans ω, les indices $x$ de $\partial_x$ et $y$ de $u_y$ en `--chalk`, reliés par un trait diagonal, de même pour le second terme ; dans la divergence, indices droits. | Écriture terme à terme ; les traits de croisement se dessinent au `Kit.pen` (arrow, sans pointe). | 7 s |
| 7.7 | [r-rotationnel] | Le panneau bascule en perspective (parallélogramme, inclinaison de 55°) ; au centre du cercle, une flèche `--u` qui sort du plan vers le haut, étiquette $\nabla\times\mathbf{u}$ ; à son pied, sa composante notée $\omega$. | Bascule de 1,2 s par transformation affine du dessin 2D (pas de 3D CSS) ; la flèche pousse. | 11,5 s |
| 7.8 | [r-roue] | Retour à plat ; le petit cercle de 20 px s'efface. Une petite roue à aubes `--chalk` (quatre aubes, moyeu, une aube marquée en `--fg`) se pose **sur P**, point de vitesse nulle : elle n'est pas emportée. | Descente de 0,6 s, petit amorti (dépassement ≤ 3 %). Dès qu'elle est posée, elle tourne dans le sens trigonométrique à 0,4 rad par seconde de scène (ω/2 pour ω = 0,8), angle en forme fermée, jusqu'à la fin de la scène. | 5 s |

### ep01.08 · `08_rotation_solide.html` · P13 · 27 s

Rotation solide u = (−y, x), panneau de 1000 × 720 px à gauche, flèches `--u` à 50 %. Un disque de fluide `--chalk` à 8 %, centré sur l'origine, porte un rayon marqué. Roue à aubes posée à 200 px de l'origine, portée par le fluide. Vitesse angulaire du fluide : 1 rad par seconde de scène, un tour en 6,3 s.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 8.1 | [r-moitie] | La roue dans la rotation solide. À droite, $\Omega_{\text{roue}} = \dfrac{\omega}{2}$, en grand. | Le fluide tourne (traceurs, 200 particules, et rayon marqué) ; la roue tourne avec lui. | 5,5 s |
| 8.2 | [r-bloc] | Le rayon marqué du disque s'allume. | — | 2 s |
| 8.3 | [r-disque] | Sous l'équation, un cadran « FLUIDE » : une aiguille `--u` suit l'angle du rayon marqué. | Rotation continue. | 6,5 s |
| 8.4 | [r-colle] | Second cadran « ROUE » à côté : son aiguille `--chalk` suit l'aube marquée. Les deux aiguilles restent alignées. L'aube marquée reste alignée avec le rayon marqué du disque. | Rotation continue ; au bout d'un tour, un trait bref `--chalk` sur les deux cadrans. | 4,5 s |
| 8.5 | [r-affiche] | Compteur « VORTICITÉ » sous la roue : 2. | Le compteur s'allume. | 3 s |
| 8.6 | [r-retiens] | Rapprochement : sous le cadran ROUE, $\Omega_{\text{roue}} = 1$, en face du compteur, $\omega = 2$ ; l'équation $\Omega_{\text{roue}} = \omega/2$ entourée au `Kit.pen`. | Les deux étiquettes glissent côte à côte en 0,6 s ; trait de 0,6 s. | 5 s |

### ep01.09 · `09_cisaillement.html` · P14 · 35 s

Cisaillement u = (y, 0), y = 0 au milieu du panneau (1400 × 640 px, centré). Flèches `--u` : vers la droite en haut, vers la gauche en bas, longueur proportionnelle à |y|, nulles sur la ligne du milieu.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 9.1 | [r-surprises] | Panneau vide ; la ligne du milieu en `--muted` fin. | Fondu. | 2 s |
| 9.2 | [r-cisaillement] | Flèches du cisaillement, ligne par ligne, de la ligne du milieu vers les bords. | Entrée échelonnée en 2 s ; traceurs `--u` à 40 % qui glissent à droite en haut, à gauche en bas. | 11,5 s |
| 9.3 | [r-droites] | Sept lignes de courant horizontales `--u`, droites. | Tracé en 1 s. | 2,5 s |
| 9.4 | [r-aubes] | Roue à aubes posée **sur la ligne du milieu**, au centre du panneau. Sur l'aube du haut, une flèche `--u` vers la droite ; sur l'aube du bas, une flèche `--u` vers la gauche. | La roue descend et se pose ; son centre reste immobile, puisque la vitesse y est nulle. | 9 s |
| 9.5 | [r-horaire] | La roue tourne **dans le sens horaire** à ½ rad par seconde de scène ; flèche courbe `--chalk` horaire à côté, sans chiffre. Compteur « VORTICITÉ » : −1. À droite : $\omega = \partial_x u_y - \partial_y u_x = 0 - 1 = -1$, puis, en dessous, $\Omega_{\text{roue}} = \omega/2 = -\tfrac12$ : le signe moins est le sens horaire. Jamais « ½ » seul. | Rotation continue jusqu'à la fin de la scène. | 10 s |

### ep01.10 · `10_tourbillon.html` · P15, P16, P17 · 63 s

Tourbillon ponctuel u = (−y, x) / (x² + y²), sens trigonométrique, centre au milieu du panneau (1000 × 760 px, à gauche ; colonne à droite x 1180 à 1780). Unité : 100 px. Flèches `--u`, longueur compressée (section 0, I_s = 0,8), disque vide de 30 px autour du centre, point `--fg` au centre. Contrainte : **la roue n'est jamais posée sur le centre** ; aucun cercle ne rétrécit vers le centre. Les valeurs 2π et 0 de 10.13 sont symboliques : écrites, non calculées.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 10.1 | [r-tourbillon] | Panneau vide. | Fondu. | 2,5 s |
| 10.2 | [r-ponctuel] | Flèches du tourbillon ; à droite, $\lvert\mathbf{u}\rvert = \dfrac{1}{r}$, et un petit schéma : r est le segment `--muted` du centre à un point. | Flèches de l'extérieur vers l'intérieur ; formule avec la voix. | 6,5 s |
| 10.3 | [r-cercles] | Cinq lignes de courant circulaires `--u`. | Tracé en 1,2 s. | 2,5 s |
| 10.4 | [r-nacelle] | Roue à aubes de rayon a = 50 px (0,5 unité) posée sur le cercle de rayon 220 px (R = 2,2). Elle fait le tour du centre (vitesse orbitale 1/R² en unités de la scène, un tour en 9 s), **sans pivoter** : l'aube marquée reste pointée vers le haut. Un trait `--muted` fixe à côté sert de référence verticale. | Orbite continue. | 8 s |
| 10.5 | [r-immobile] | Même mouvement ; cadran « ROUE » à droite, aiguille immobile. | — | 2 s |
| 10.6 | [r-bords] | La roue s'arrête à droite du centre (position 3 h). Zoom de 1,8× sur elle. | Ralenti jusqu'à l'arrêt, zoom de 0,8 s. | 2 s |
| 10.7 | [r-proche] | Deux flèches de vitesse `--u` sur ses deux bords, la plus longue du côté du centre, rapport des longueurs exact, 1/(R − a) contre 1/(R + a), soit 0,59 contre 0,37 : les deux intensités sont sous le seuil 0,8, donc dans la partie linéaire. Une petite flèche courbe `--u` horaire : ce que ferait cet écart. Rappel $\lvert\mathbf{u}\rvert = 1/r$ dans le calque de formule. | Les deux flèches poussent, puis la flèche courbe. | 7 s |
| 10.8 | [r-courbe] | L'arc de la trajectoire en `--chalk` ; une seconde flèche courbe `--u` trigonométrique, de même taille : ce que ferait la courbure. | Tracé de l'arc, puis la flèche courbe. | 4 s |
| 10.9 | [r-compense] | Les deux flèches courbes se rapprochent et s'annulent ; l'aiguille du cadran ROUE reste immobile. | Glissement de 0,8 s, puis fondu des deux. | 3,5 s |
| 10.10 | [r-lecon] | Retour au plan large. En vignettes côte à côte, à droite : le cisaillement (lignes droites, roue qui tourne, ω = −1) et le tourbillon (lignes courbes, roue qui ne tourne pas, ω = 0 hors du centre). | Les vignettes jouent leur mouvement en boucle courte. | 9 s |
| 10.11 | [r-ou] | Les vignettes s'effacent ; le point du centre pulse. | — | 3 s |
| 10.12 | [r-concentree] | Le point du centre s'allume en `--u-hi` ; les flèches les plus proches du centre sont les plus longues de la carte, dans la partie compressée. | Pulsation lente. | 4 s |
| 10.13 | [r-entoure] | Trois cercles en tirets qui **entourent** le centre, qui apparaissent du plus petit au plus grand (jamais un rétrécissement) : rayon 120 px centré ; rayon 220 px **décentré**, centre à (70, 40) px du centre du tourbillon, qui l'entoure toujours ; rayon 320 px centré. Pour chacun, la valeur symbolique « CIRCULATION » 2π, sans division par l'aire : 2π, 2π, 2π. Un quatrième cercle, déplacé, qui n'entoure pas le centre (rayon 70 px, centre à (−380, 250) px, hors du grand cercle) : 0. | Chaque cercle se trace, sa valeur s'écrit. | 6 s |
| 10.14 | [r-reviendra] | Tout baisse à 40 % sauf le centre et les trois valeurs 2π. | Fondu. | 2,5 s |

### ep01.11 · `11_cellules_limite.html` · P18 · 28 s

Écoulement cellulaire de la scène 06, panneau à gauche (900 × 720 px). Cercle centré en un point fixe C = (1,4 ; 1,8) de la cellule en bas à gauche, loin des droites x = kπ et y = kπ. Valeur attendue : ω(C) = 2 sin 1,4 sin 1,8 ≈ 1,92. À droite, un graphe `Kit.plot` : axe horizontal « RAYON », axe vertical « CIRCULATION ÷ AIRE ».

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 11.1 | [r-retour] | Cellules et lignes de courant ; cercle en tirets centré sur C, rayon 1,2 en unités du champ, à l'intérieur de la cellule. Compteur « CIRCULATION ÷ AIRE ». | Le cercle se trace. | 6 s |
| 11.2 | [r-varie] | Le graphe s'ouvre ; le point (rayon, valeur) se pose, puis le cercle commence à rétrécir et le point trace la courbe, du grand rayon vers le petit. | Rayon de 1,2 à 0,6 ; la valeur change visiblement. | 6,5 s |
| 11.3 | [r-stabilise] | La courbe s'aplatit. | Rayon de 0,6 à 0,05, plus lentement ; le compteur ralentit puis s'arrête sur 1,92. | 6,5 s |
| 11.4 | [r-valeur] | Ligne horizontale `--muted` en tirets sur le graphe à 1,92, étiquette $\omega(C)$ ; point C `--chalk` au centre du cercle. | `P.hline`. | 4 s |
| 11.5 | [r-visible] | La courbe entière reste ; l'extrémité gauche de la courbe et la ligne se touchent, entourées au `Kit.pen`. | Trait de 0,6 s. | 4,5 s |

### ep01.12 · `12_carrelage.html` · P19, P20 · 51 s

Région rectangulaire D de 960 × 640 px, à gauche (x 140 à 1100, y 140 à 780), soit [0 ; 3] × [0 ; 2] en unités de la région (320 px par unité), découpée en 6 × 4 carreaux `--chalk` de côté 0,5. Champ lisse, u = (x²/2 − 0,5 y, y + 0,5 x) : ∇·u = x + 1, non nulle, et ω = 0,5 − (−0,5) = 1, non nulle aussi, pour que les deux énoncés aient un contenu. Sur chaque côté de chaque carreau, **une seule** petite flèche `--u` perpendiculaire au côté, dans le sens du champ, de longueur proportionnelle au flux par ce côté. Colonne d'équation à droite.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 12.1 | [g-grand] | La région vide, contour `--chalk`. | Fondu. | 2 s |
| 12.2 | [g-carrelage] | Les lignes du carrelage. | Tracé ligne par ligne en 1,2 s. | 4,5 s |
| 12.3 | [g-voisins] | Deux carreaux voisins s'allument : x de 1,5 à 2 et de 2 à 2,5, y de 0,5 à 1. Sur leur côté commun (x = 2, où $u_x$ est entre 1,5 et 1,75, donc positif), une seule flèche, qui va vers la droite. Un petit « + » `--chalk` côté gauche du côté commun : pour le carreau de gauche, elle sort. Un petit « − » `--muted` côté droit : pour le carreau de droite, elle entre. Aucune flèche n'est dédoublée ni retournée. | La flèche pousse, puis le « + » et le « − » s'allument. | 7 s |
| 12.4 | [g-annule] | Le « + » et le « − » glissent l'un vers l'autre sur la flèche et s'annulent ; la flèche du côté commun s'efface avec eux. | Glissement et fusion en 0,6 s. | 3 s |
| 12.5 | [g-reste] | Toutes les flèches de tous les côtés, une par côté ; sur chaque côté intérieur, la même paire « + » / « − » s'allume puis s'annule, et la flèche s'efface ; il reste les flèches du contour. | Apparition en 1 s, effacement par paires en vague de gauche à droite en 2 s. | 6,5 s |
| 12.6 | [g-produit] | Un carreau mis en avant : à côté, $\text{flux} \approx (\nabla\cdot\mathbf{u})\times\text{aire}$. | Écriture. | 6,5 s |
| 12.7 | [g-somme] | Les carreaux se subdivisent : 6 × 4, 12 × 8, 24 × 16. Équation : $\sum (\nabla\cdot\mathbf{u})\,\Delta A \;\to\; \iint_D \nabla\cdot\mathbf{u}\,dA = \text{flux à travers le bord}$. | Deux subdivisions à 2,5 s d'écart ; `Kit.morph` du Σ vers l'intégrale double. Le contour garde ses flèches. | 8,5 s |
| 12.8 | [g-ostrogradski] | Étiquette mono « GREEN–OSTROGRADSKI » au-dessus de l'énoncé. | — | 2,5 s |
| 12.9 | [g-stokes] | Sur le carrelage, les flèches de flux sont remplacées par des flèches de circulation, une par côté, tangentes au côté, dans le sens de la part tangente du champ. Sur chaque côté intérieur, « + » du côté du carreau dont le parcours trigonométrique suit la flèche, « − » de l'autre ; les paires s'annulent encore, sans retourner de flèche. Second énoncé sous le premier : $\iint_D \omega\,dA = \text{circulation sur le bord}$, étiquette « STOKES ». | Échange des flèches en 0,6 s, effacement des paires en 1,5 s. | 7 s |
| 12.10 | [g-raconte] | Le contour s'épaissit ; l'intérieur baisse à 30 %. | — | 3 s |

### ep01.13 · `13_espace.html` · P21, P22 · 65 s

Dessins en SVG ou canvas 2D : la sphère est un cercle `--chalk` avec un équateur en ellipse en tirets et un léger dégradé radial ; les cubes sont en perspective isométrique, arêtes `--chalk`, arêtes cachées en tirets, peints du fond vers l'avant.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 13.1 | [g-plan] | Le carrelage de la scène 12, à plat. | Il bascule en perspective (inclinaison de 60°) en 1,2 s. | 3 s |
| 13.2 | [g-sphere] | Un petit cercle en tirets posé sur le plan se gonfle en sphère ; à côté, $\pi r^2$ devient $\tfrac43\pi r^3$. | L'équateur apparaît, le dégradé se lève, en 1,5 s. | 8 s |
| 13.3 | [g-cube] | Un carreau se soulève en petit cube. Puis un empilement de cubes qui remplit grossièrement une boule : les 32 cubes d'une grille 4 × 4 × 4 dont le centre est dans la boule de rayon 2 côtés. | Extrusion en 1 s, puis les cubes se posent couche par couche en 2 s. | 8,5 s |
| 13.4 | [g-peau] | Les faces communes entre cubes s'effacent par paires ; il reste l'extérieur de l'empilement, une surface fermée en escalier, voilée `--chalk` à 15 %. Puis les cubes se subdivisent (grilles 8 × 8 × 8, puis 16 × 16 × 16, toujours les cubes dont le centre est dans la boule) : l'escalier s'affine et la surface fond vers la sphère, le ballon. | Effacement en vague en 2 s ; deux subdivisions à 1,2 s d'écart, puis fondu de l'escalier fin vers la sphère lisse en 0,6 s. | 5,5 s |
| 13.5 | [g-champb] | Le ballon reste ; quelques lignes de B en `--b` le traversent. | `Kit.fieldLines`, tracé en 1,5 s. | 3,5 s |
| 13.6 | [g-loi] | $\nabla\cdot\mathbf{B} = 0$ en grand, à droite. Accolade sous $\nabla\cdot\mathbf{B}$, étiquette $\lim \dfrac{\text{flux}}{\text{volume}}$ en `--muted`, qui rappelle la définition au lieu de répéter « divergence de B ». | Écriture, puis accolade. | 7 s |
| 13.7 | [g-equivaut] | Sur le ballon, les lignes de B entrent d'un côté et ressortent de l'autre ; les points d'entrée `--muted`, de sortie `--b`, en nombre égal. À côté : flux à travers la peau $= 0$. | Points marqués un à un. | 7,5 s |
| 13.8 | [g-imagine] | Panneau voisin, fond `--panel` : un point d'où partent des lignes `--b` en tirets, à 60 % (une hypothèse, pas un champ existant). | Lignes tracées vers l'extérieur. | 5 s |
| 13.9 | [g-sphereautour] | Une petite sphère en tirets autour de ce point : toutes les lignes sortent, aucune n'entre ; flux $\neq 0$. | Tracé de la sphère, puis marquage des sorties. | 7,5 s |
| 13.10 | [g-monopole] | Le panneau de l'hypothèse est barré au `Kit.pen` (cross, `--chalk`). | Trait de 0,6 s. | 9 s |

### ep01.14 · `14_charge.html` · P23, P24 · 54 s

Reprise de la carte de gauche de la scène 01, qui reprend le panneau de gauche de `fig-monopole-dipole.png` dans le style du thème : charge au centre, champ en `--fg-2`, cercles `--chalk` en tirets. Unité : 120 px ; longueur des flèches compressée avec I_s = 1,2, donc linéaire pour toutes les flèches des sphères. **Aucun compteur « flux ÷ aire » sur cette carte** : la carte est une coupe d'un champ en 3D, et le flux 2D d'un cercle de la carte n'aurait pas de sens. Seules valeurs autorisées : 4π et 0, symboliques, écrites et non calculées.

Géométrie du plan 14.6. Sphère déplacée de rayon ρ = 1 (120 px), centre à (1,7 ; 1,7), soit d ≈ 2,40 de la charge : elle n'entoure pas la charge et ne touche pas la sphère R = 1. Le cône tangent issu de la charge la touche le long d'un cercle, à l'angle α = arccos(ρ/d) ≈ 65° de la direction de la charge, vu depuis le centre de la sphère. Ce cercle sépare une **calotte d'entrée**, tournée vers la charge, petite (environ 29 % de l'aire), et une **calotte de sortie**, grande (environ 71 %). Intensité normale au point le plus proche, à 1,4 de la charge : environ 0,51 ; au point le plus éloigné, à 3,4 : environ 0,09.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 14.1 | [g-charge] | La carte de la charge, en grand, à gauche (760 × 760 px). | Fondu d'entrée. | 2,5 s |
| 14.2 | [g-coupe] | Le cercle centré gagne un équateur en ellipse et un dégradé : c'est une sphère vue en coupe. Même transformation pour le cercle déplacé. | Gonflement de 1,2 s, comme à la scène 13. | 5 s |
| 14.3 | [g-faiblit] | Trois sphères **centrées** sur la charge, rayons R = 1, 2, 3 (120, 240, 360 px). Sur chacune, douze flèches perpendiculaires à la sphère, toutes de même longueur sur une même sphère, et plus courtes d'une sphère à la suivante, dans le rapport exact 1, 1/4, 1/9 (60, 15 et 6,7 px). À droite, un tableau à trois lignes : colonne « R », colonne $1/R^2$ : 1, 1/4, 1/9. | Une sphère après l'autre ; la ligne du tableau s'écrit avec la sphère. | 11,5 s |
| 14.4 | [g-grandit] | Colonne $4\pi R^2$ : 4π, 16π, 36π. | Écriture de la colonne. | 3,5 s |
| 14.5 | [g-quatrepi] | Colonne « produit » : 4π, 4π, 4π. Les R² barrés au `Kit.pen` (cross, petit) dans chaque ligne. Valeur 4π posée à côté de la plus petite sphère. | Écriture, puis barres. | 9 s |
| 14.6 | [g-pourtant] | Le tableau et les sphères R = 2 et 3 s'effacent ; la sphère R = 1 reste avec sa valeur 4π. La sphère **déplacée** (géométrie ci-dessus), dessinée en 3D : contour, équateur en ellipse en tirets, et le cercle de tangence vu depuis la charge, en ellipse `--chalk` pleine de 2 px, avec les deux génératrices du cône tangent en tirets `--muted`, de la charge aux bords de ce cercle. Les deux calottes sont teintées : la petite calotte d'entrée en `--muted` à 25 %, la grande calotte de sortie en `--fg-2` à 12 %. Sur la petite calotte, des flèches perpendiculaires **entrantes et fortes** ; sur la grande, des flèches **sortantes et faibles**, plus nombreuses ; sur le cercle de tangence, la part perpendiculaire est nulle. Pas de coupe plane avec des flèches rangées en colonnes. Valeur 0. | Tracé de la sphère, puis du cône et du cercle de tangence, teinte des calottes, puis les flèches poussent, calotte d'entrée d'abord ; la valeur 0 s'écrit à la fin. | 5 s |
| 14.7 | [g-concentree] | Le point de la charge s'allume en `--fg`. | Pulsation. | 3 s |
| 14.8 | [g-revele] | Les deux valeurs côte à côte : 4π sur la sphère centrée R = 1, 0 sur la sphère déplacée. | — | 7 s |
| 14.9 | [g-echo] | À droite, vignette du tourbillon de la scène 10 : centre, trois cercles qui l'entourent, dont le décentré, valeurs 2π. Les deux centres reliés par un trait `--muted` en tirets. | Fondu de la vignette, puis le trait. | 7 s |

### ep01.15 · `15_aimant_verdict.html` · P25, P26 · 38 s

Reprise de la carte de droite de la scène 01. **Aimant étendu** (rectangle 60 × 180 px, corps `--matter`, bout nord teinté `--b`, bout sud `--matter-dark`). Le panneau de droite de `fig-monopole-dipole.png` n'est pas repris.

Lignes de champ. Le champ est axisymétrique : ses lignes sont exactement les **lignes de niveau de la fonction r·A_φ**, où r est la distance à l'axe et A_φ le potentiel vecteur azimutal des 24 spires de la scène 01, sommé spire par spire (quadrature sur 64 points ou intégrales elliptiques), avec la même régularisation près des spires (ε = 5 px). On calcule r·A_φ sur une grille du panneau et on trace ses lignes de niveau par marching squares (composant « lignes de niveau », section 5, point 4). Les niveaux sont les valeurs de r·A_φ en **douze graines** du plan médian de l'aimant, dans sa partie centrale : x = ±0,1, ±0,2, ±0,3, ±0,4, ±0,5 et ±0,6 rayon de l'aimant (de ±3 à ±18 px), soit six niveaux, chacun donnant deux lignes symétriques. **Aucune graine sur l'axe** : la ligne de l'axe ne se referme pas dans le panneau. Chaque ligne traverse l'aimant du sud au nord, sort par le bout nord, fait le tour par l'extérieur et rentre par le bout sud ; celles des graines proches de l'axe sortent du panneau, ce qui est permis. Même règle de valeurs que la scène 14 : 0, symbolique, aucun compteur.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 15.1 | [g-dipole] | La carte de l'aimant, en grand ; les flèches passent de `--fg-2` à `--b`. | Fondu de couleur en 0,8 s. | 5 s |
| 15.2 | [g-traversent] | Les lignes de champ `--b` se tracent ; un traceur `--fg` parcourt l'une d'elles : sortie par le nord, tour par l'extérieur, entrée par le sud, traversée de l'aimant. Le traceur est sur la ligne de la graine x = +0,6 rayon, qui boucle **entièrement dans le panneau** ; le constructeur le vérifie sur image fixe, et sinon prend la graine la plus éloignée de l'axe dont la ligne boucle dans le panneau. | Tracé des lignes en 1,5 s ; le traceur part du plan médian, de sa graine, et avance le long de la ligne de niveau à vitesse d'arc constante. | 6,5 s |
| 15.3 | [g-sansfin] | Le traceur continue de tourner sur sa ligne. | Boucle continue, un tour en 4 s. | 2 s |
| 15.4 | [g-nul] | Sphères en coupe : une centrée qui entoure l'aimant, une déplacée. Valeur 0 sur chacune. Aucun compteur. | Tracé des sphères, valeurs. | 5 s |
| 15.5 | [g-reponse] | Les deux cartes de la scène 01 côte à côte, à leur place d'ouverture, avec leurs sphères en coupe. Charge en `--fg-2`, aimant en `--b`. | Recadrage de 1 s. | 4 s |
| 15.6 | [g-critere] | Sur chaque sphère, sa valeur : 4π et 0 à gauche, 0 et 0 à droite. | Les valeurs s'écrivent. | 9 s |
| 15.7 | [g-verdict] | `Kit.pen` check `--chalk` sous la carte de l'aimant ; `Kit.pen` cross sous la carte de la charge, puis un cercle au `Kit.pen` autour de la charge et de sa valeur 4π. | Coche, croix, cercle, 0,6 s chacun. | 6 s |

### ep01.16 · `16_randonnee.html` · P27, P28 · 62 s

Carte de ψ = sin x sin y sur [0, 2π]² (`Kit.fieldMap`, kind `u`, 900 × 760 px, à gauche), étiquette « ψ ». Lignes de niveau ψ = ±0,2, ±0,4, ±0,6, ±0,8 en `--fg-2` fin, calculées par marching squares dans la page. Colonne d'équation à droite. Point de travail **Q = (π/2 ; 0,6435)**, dans la cellule en bas à gauche (ψ > 0), sous le sommet : ψ(Q) = sin 0,6435 = 0,6, donc Q est **sur la ligne tracée ψ = 0,6**. En Q, ∇ψ = (0 ; 0,8), vers le haut, et u = ∇⊥ψ = (0,8 ; 0), vers la droite.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 16.1 | [c-construire] | Le pictogramme 3 de la scène 01, seul au centre. | Il grandit et s'efface pour laisser la carte. | 6,5 s |
| 16.2 | [c-randonnee] | La carte de ψ, sans lignes. Quatre sommets et creux marqués « + » et « − » en `--muted` (deux sommets, deux creux). | Fondu de la carte en 1 s. | 8,5 s |
| 16.3 | [c-niveau] | Les lignes de niveau se tracent. | Tracé du sommet vers l'extérieur en 1,5 s. | 4 s |
| 16.4 | [c-gradient] | Flèche de gradient `--chalk` au point Q, vers le sommet (vers le haut). À droite : $\nabla\psi = (\partial_x\psi,\ \partial_y\psi)$. | La flèche pousse ; formule avec la voix. | 8,5 s |
| 16.5 | [c-montee] | Petit carré d'angle droit `--chalk` entre la flèche et la ligne de niveau ψ = 0,6, qui passe par Q. | Tracé. | 5 s |
| 16.6 | [c-quart] | La flèche pivote d'**un quart de tour dans le sens horaire** autour de Q : du haut vers la droite. Un arc `--muted` avec pointe horaire montre le geste. | Rotation de 1,2 s, inOutCubic. | 5,5 s |
| 16.7 | [c-longe] | La flèche est maintenant tangente à la ligne de niveau ψ = 0,6 ; cette ligne s'allume. | — | 3,5 s |
| 16.8 | [c-vitesse] | La flèche passe de `--chalk` à `--u`, étiquette $\nabla^\perp\psi$. | Fondu de couleur de 0,6 s. | 6 s |
| 16.9 | [c-compos] | $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi,\ -\partial_x\psi)$. | Écriture terme à terme. | 5,5 s |
| 16.10 | [c-gauche] | Les lignes de niveau passent en `--u` et reçoivent des pointes de flèche dans le sens du courant. Quatre petits « + » `--chalk`, chacun juste à gauche du courant : deux dans une cellule ψ > 0, du côté du sommet (vers l'intérieur de la cellule) ; deux dans une cellule ψ < 0, du côté du bord de la cellule (vers la droite ψ = 0, loin du creux). Les grandes valeurs sont toujours à gauche. | Pointes réparties en 1 s ; les quatre « + » s'allument un à un, d'abord les deux de la cellule ψ > 0. | 8,5 s |

Vérification : au point Q, sous le sommet d'une cellule ψ > 0, la vitesse va vers la droite et le sommet est au-dessus, c'est-à-dire à gauche du courant. Dans une cellule ψ < 0, par exemple en (3π/2 ; 0,6435), sous le creux, la vitesse va vers la gauche ; à gauche de ce courant, c'est-à-dire vers le bas, vers le bord y = 0, ψ remonte vers 0 : le « + » y est du côté du bord de la cellule, et le creux est à droite du courant.

### ep01.17 · `17_construction.html` · P29, P30, P31 · 66 s

Badge SCHEMATIC pour toute la scène, de 17.1 à 17.12. Plans 17.1 à 17.5 : équation en grand, au centre. Plans 17.6 à 17.11 : la carte de la scène 16, à gauche, colonne à droite. Plan 17.12 : nouvelle mise en page, carte agitée à gauche, au-dessus du bandeau.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 17.1 | [c-calcul] | $\nabla\cdot\mathbf{u} =$ au centre. | Écriture. | 1,5 s |
| 17.2 | [c-croisees] | $\nabla\cdot\mathbf{u} = \partial_x\partial_y\psi - \partial_y\partial_x\psi$, chaque terme dans sa couleur, le premier `--u`, le second `--chalk`. | Écriture terme à terme. | 6 s |
| 17.3 | [c-ordre] | Dans le second terme, $\partial_y$ et $\partial_x$ échangent leurs places. | `Kit.morph` de 0,8 s. | 4 s |
| 17.4 | [c-nulle] | Les deux termes sont identiques ; ils se superposent, puis « = 0 » s'écrit. | Superposition en 0,6 s. | 6 s |
| 17.5 | [c-livree] | « = 0 » encadré au `Kit.pen` (box). | Trait de 0,6 s. | 5 s |
| 17.6 | [c-sinus] | Retour à la carte de ψ, lignes de niveau `--fg-2` ; à droite, $\psi = \sin x\,\sin y$. | Fondu. | 2,5 s |
| 17.7 | [c-revoila] | Les flèches de vitesse `--u` apparaissent le long des lignes de niveau ; les cellules alternées se forment, comme le quatrième panneau de `fig-champs.png`. | Flèches en vague depuis les sommets. | 2,5 s |
| 17.8 | [c-resolue] | Calque de formule : $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$, comme à la scène 06. Le petit cercle et son compteur « FLUX ÷ AIRE » repassent sur la même trajectoire qu'à la scène 06 ; compteur à 0. Le point d'interrogation de la scène 06 revient dans le coin et s'efface. | Trajectoire de 4 s ; puis le cercle et son compteur s'effacent en 0,4 s, avant la fin du plan. Ils ne reviennent plus dans la scène. | 6,5 s |
| 17.9 | [c-omega] | La carte passe de ψ à ω : même motif, échelle de couleur deux fois plus étendue (barre de couleur `--muted` avec graduations ψ : ±1, puis ω : ±2). $\omega = 2\psi$ à droite. | Fondu de 0,8 s entre les deux graduations. | 6 s |
| 17.10 | [c-tournent] | Sur chaque cellule, une flèche courbe : **trigonométrique dans les cellules où ψ > 0**, horaire dans les cellules où ψ < 0. Traceurs à 40 %. | Les flèches courbes se dessinent ; les traceurs tournent. | 9 s |
| 17.11 | [c-frontieres] | Les droites x = kπ et y = kπ en `--chalk`, étiquette ψ = 0. | Tracé en 0,8 s. | 3 s |
| 17.12 | [c-machines] | La carte des cellules se réduit en vignette et glisse à droite (x 1184 à 1664, y 160 à 640). La vignette perd $\omega = 2\psi$, la barre de couleur, les flèches courbes et l'étiquette ψ = 0 : il reste la carte, ses lignes et ses traceurs. À gauche, au-dessus du bandeau, une carte plus agitée (640 × 640 px, x 176 à 816, y 96 à 736) s'ouvre **d'abord sur ψ** : carte de couleur `Kit.cmap('u')`, étiquette « ψ ». ψ est une somme de 24 modes de Fourier à **nombres d'onde entiers** (k_x, k_y), 2 ≤ \|k\| ≤ 6, sur [0, 2π]², amplitudes et phases fixées par une graine nommée dans le code ; ψ est **figé** pendant tout le plan. Puis on en tire les lignes de courant, lignes de niveau de ψ en `--u`, avec des traceurs ; calque de formule en bas à droite : rappel $\mathbf{u} = \nabla^\perp\psi$. Bandeau de référence **sous la carte agitée**, dans la zone du bandeau (x 96 à 996, y 752 à 880) : l1 « RÉFÉRENCE », l2 « Wang et al., FunDiff, Nature Communications, 2026 ». Chip `schematic` sur la carte agitée, en haut à gauche : « illustration · pas une sortie du modèle ». Aucun chiffre sur la carte agitée : ni compteur, ni barre graduée, ni valeur. | Réduction de 1 s ; ouverture de la carte de ψ en 1 s, avec le chip et le bandeau (`Kit.lowerThird` kind `reference`, maintien jusqu'à la fin de la scène) ; 1,5 s plus tard, les lignes de courant se tracent en 1,5 s et le rappel $\mathbf{u} = \nabla^\perp\psi$ s'écrit ; puis les traceurs, seuls à bouger. | 13,5 s |

La légende FunDiff ne s'affiche que sur ce plan, sous la carte agitée, qui est une carte de vitesse tirée de ψ. Aucune carte de B n'est à l'écran pendant ce plan. Sur la carte agitée : ni « Kolmogorov », ni « Re », ni violet `--model`, ni chip `generated`.

### ep01.18 · `18_potentiel.html` · P32, P33 · 41 s

La carte des cellules de la scène 17 (pas la carte agitée), renommée a, en `Kit.cmap('b')`. Champ B = ∇⊥a avec a = sin x sin y.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 18.1 | [c-recette] | La carte de ψ, plein cadre à gauche. | Fondu d'entrée. | 5 s |
| 18.2 | [c-potentiel] | L'étiquette ψ devient a ; la carte passe de `--u` à `--b` ; les flèches passent en `--b`. À droite : $\mathbf{B} = \nabla^\perp a$. | Fondu de couleur de 1 s ; formule avec la voix. | 7 s |
| 18.3 | [c-passe] | Un contour fermé irrégulier `--chalk` en tirets (pas un cercle : une forme de haricot) posé sur la carte ; compteur « FLUX » à 0. Ce compteur est permis ici : la carte est un vrai champ du plan, pas une coupe. Quadrature sur 256 points du contour paramétré γ(s), parcouru dans le sens trigonométrique : somme de B·n pondérée par l'élément d'arc \|γ'(s)\| Δs, normale n = (γ'_y, −γ'_x)/\|γ'\| orientée vers l'extérieur. Le compteur affiche 0 sur toutes les images fixes, jamais « −0 ». | Le contour se déforme et se déplace en continu ; le compteur reste à 0. | 6,5 s |
| 18.4 | [c-office] | Le pictogramme du test de la scène 15 (coche) se pose à côté de la formule. | Coche au `Kit.pen`. | 7 s |
| 18.5 | [c-promet] | La coche reste ; à côté, un second emplacement, vide. | — | 3,5 s |
| 18.6 | [c-ressemble] | Deux lignes à droite : « $\nabla\cdot\mathbf{B} = 0$ » avec la coche ; en dessous, un emplacement vide, cadre en tirets `--muted`, qui attend un vrai champ pour la comparaison, et un point d'interrogation. Aucune image de champ réel n'y est dessinée. | Le point d'interrogation s'allume ; maintien. | 11,5 s |

### ep01.19 · `19_cloture.html` · P34, P35 · 40 s

Les trois pictogrammes de la scène 01 en colonne à gauche ; chacun reçoit sa formule en face. Le pictogramme 1 a deux moitiés (flux, circulation), donc deux formules ; le pictogramme 2 (carrelage, sphère) en a une ; le pictogramme 3 en a une.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 19.1 | [f-gestes] | Les trois pictogrammes de la scène 01, en colonne à gauche. | Apparition échelonnée. | 1,5 s |
| 19.2 | [f-sortir] | En face du pictogramme 1 (gauche) : $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$. Puis, en face du pictogramme 2, plus petite : $\iint_D \nabla\cdot\mathbf{u}\,dA = \text{flux à travers le bord}$, l'énoncé de la scène 12. | Écriture de la première formule, puis de la seconde 2 s plus tard. | 4 s |
| 19.3 | [f-tourner] | En face du pictogramme 1 (droite) : $\omega = \partial_x u_y - \partial_y u_x$, puis $\Omega_{\text{roue}} = \omega/2$ avec une petite roue. | Écriture ; la roue fait un quart de tour **dans le sens trigonométrique**, comme pour ω > 0. | 7 s |
| 19.4 | [f-construire] | En face du pictogramme 3 : $\mathbf{u} = \nabla^\perp\psi \;\Rightarrow\; \nabla\cdot\mathbf{u} = 0$. | Écriture. | 6 s |
| 19.5 | [f-voie] | Les quatre lignes baissent à 40 %. `Kit.projector` à droite, plan étiqueté « CHAMPS SANS DIVERGENCE », champ `--u` : la flèche se projette sur le plan. | `drop` 1 s après l'entrée. | 7 s |
| 19.6 | [f-projection] | Chip `plain` sous le projecteur : « MODULE 1 · #CH6 ». | — | 4 s |
| 19.7 | [f-crayon] | Carte d'exercices, à droite, à la place du projecteur : « EXERCICES » en mono, puis 1 b, c · 2 b, c · 6 · 7 a · 9 a, c ; dessous, l'ancre « #exercices » en `--muted`. | Lignes en cascade. | 5 s |
| 19.8 | [f-calculs] | Les trois pictogrammes et la carte d'exercices restent seuls. | Maintien, puis fondu au noir de 1 s en fin de scène (3 s de pause conseillée). | 2,5 s |

## 3. Contraintes physiques : où elles portent

| Contrainte | Plans |
|---|---|
| Cercle centré ou cercle déplacé, selon le cas | 1.5, 3.6, 5.6 à 5.11, 6.1, 10.13, 14.3, 14.6, 15.4 |
| Un cercle déplacé ne montre des parts entrantes que s'il est assez loin (3.6 : \|c\| > 167 px ; 5.10 : \|c\| ≈ 244 px > 130 px) | 3.6, 5.10 |
| La roue jamais sur le centre du tourbillon ; aucun cercle ne rétrécit vers ce centre | 10.4 à 10.13 (orbite de rayon 220 px ; cercles apparus du petit au grand, l'un décentré mais entourant le centre) |
| La roue posée sur la ligne du milieu dans le cisaillement | 9.4, 9.5, vignette 10.10 |
| La roue posée en un point de vitesse nulle, ou portée par le fluide ; son sens et sa vitesse valent ω/2 | 7.8, 8.x, 9.5, 19.3 |
| Quart de tour horaire, grandes valeurs de ψ à gauche du courant | 1.10, 16.6, 16.10, 19.4 |
| Les cellules où ψ > 0 tournent dans le sens trigonométrique | 6.6, 11.1, 16.10, 17.7, 17.10 ; axe y vers le haut (section 0) |
| Un aimant étendu, pas de dipôle ponctuel ; lignes = lignes de niveau de r·A_φ | 1.x, 15.1 à 15.7 |
| Cercles en tirets des cartes = sphères en coupe, sans compteur 2D, seulement 4π et 0, symboliques | 1.5, 14.x, 15.x |
| Flèches : longueur strictement croissante, linéaire sous le seuil, rapports exacts quand la voix compare | 10.7, 14.3, 14.6 |
| Légende FunDiff sur la carte de vitesse seulement, bandeau sous la carte agitée | 17.12 ; jamais en 18.x |
| La circulation se calcule dans le sens trigonométrique | 7.2, 7.3, 12.9 |
| Le cisaillement : à droite en haut, à gauche en bas, roue horaire, Ω_roue = −½ | 9.2, 9.5 |

## 4. Points signalés à la narration (non modifiée)

1. **P2, ligne « écran ».** Elle prévoit trois lignes de texte, dont « du petit au grand, du plan à l'espace », qui reprend mot pour mot la voix. Le storyboard la remplace par trois pictogrammes numérotés (plans 1.7 à 1.10), qui reviennent à la clôture avec leurs formules (19.1 à 19.4).
2. **P22, ligne « écran ».** Elle prévoit le sous-titre « divergence de B » sous ∇·B = 0, ce que la voix vient de dire. Le storyboard met à la place l'accolade « lim flux ÷ volume » (13.6), qui rappelle la définition.
3. **P23, ligne « écran ».** Elle demande « le panneau de gauche de fig-monopole-dipole.png ». La figure du site est blanche et en bleu et orange. Le storyboard le redessine dans le thème, avec la même géométrie (14.1), au lieu d'incruster l'image, ce qui obligerait à passer en registre PAPER.
4. **P34, ligne « écran ».** Elle prévoit trois lignes de formules. Le storyboard en écrit une de plus, en face du pictogramme 2 (19.2), pour que chaque pictogramme ait sa formule ; la voix n'en parle pas, et c'est l'énoncé déjà vu à la scène 12.

## 5. Écarts proposés

Rien de ceci n'est appliqué : à accepter ou refuser par l'auteur.

1. **Composant « roue à aubes » (`Kit.paddleWheel`).** Il n'existe pas. Il servirait aux scènes 07 à 10 et 19. Options : position (fonction de t), angle propre (fonction de t, en forme fermée), quatre aubes `--chalk`, une aube marquée `--fg`, flèches d'aubes facultatives (couleur `--u`). Raison : le même objet dans cinq scènes doit avoir le même dessin, et son angle doit rester une fonction pure du temps.
2. **Composant « compteur » (`Kit.readout`).** `Kit.chip` affiche un texte fixe ; il faut une valeur qui change à chaque image, en chiffres tabulaires (`.tnum`), avec un libellé mono, une position qui peut suivre un objet, un **séparateur décimal en virgule** (« 1,92 »), alors que `Kit.fmt` écrit un point, et une normalisation du zéro signé : toute valeur qui s'arrondit à zéro s'affiche « 0 », jamais « −0 ». Raison : le compteur est un motif de la bible, présent dans les scènes 05, 06, 08 à 11, 17 et 18.
3. **Composant « cercle-sonde » (`Kit.probe`).** Cercle ou contour fermé quelconque en tirets `--chalk`, donné par une paramétrisation γ(s), avec ses parts de flèches perpendiculaires ou tangentes au bord (style plein ou en tirets selon le mode `flux` ou `circulation`), et le calcul par quadrature du flux ou de la circulation sur 256 points, pondéré par l'élément d'arc \|γ'(s)\| Δs, normale orientée vers l'extérieur, parcours trigonométrique, divisé ou non par l'aire, qui alimente le compteur. Raison : c'est l'objet central de l'épisode (scènes 03, 05 à 07, 11, 17, 18), et le compteur doit afficher une valeur calculée, pas écrite à la main.
4. **Composant « lignes de niveau » (`Kit.contours`).** Marching squares sur une grille scalaire, tracé progressif, niveaux donnés en liste ou par des points graines, pointes de flèche facultatives dans le sens de ∇⊥ψ, traceur à vitesse d'arc constante sur une ligne fermée. Raison : les scènes 15 (r·A_φ), 16 à 18 en ont besoin, et les lignes de niveau reviendront avec ψ et a dans les épisodes suivants.
5. **Compression de longueur dans `Kit.arrows`.** Option `compress: {k, threshold}` : L(I) = k·I sous le seuil, k·I_s·(2 − I_s/I) au-dessus, fonction strictement croissante, continue et de pente continue, sans plafond dur ; et option `hole` (disque vide autour d'un point). Aujourd'hui la longueur est normalisée par le maximum de la grille, ce qui rend la charge et le tourbillon illisibles (une flèche géante, toutes les autres invisibles), et un plafond dur ferait mentir « plus longue = plus forte ». Le seuil se règle par scène : au-dessus de l'intensité 1 à R = 1 en scène 14 (I_s = 1,2), au-dessus de 1/(R − a) en 10.7 (I_s = 0,8). Raison : scènes 01, 10, 14.
6. **Couleur du champ de la charge : `--fg-2`.** Le thème n'a pas de couleur clé pour le champ électrique. Je propose `--fg-2`, neutre, pour la charge pendant tout l'épisode et pour l'aimant jusqu'à [g-dipole], où il passe en `--b`. Colorer l'aimant en `--b` dès l'ouverture donnerait la réponse à la question de départ. Ce n'est pas une nouvelle couleur, mais un rôle nouveau pour un jeton existant.
7. **Dessins en perspective : sphère, calottes, cubes, plan incliné.** Pas de composant ; code de scène en SVG ou canvas 2D (ellipses, dégradé radial, isométrie, empilement de cubes peint du fond vers l'avant). Je propose de les factoriser plus tard dans `motifs.js` si un épisode suivant les reprend. Raison : les scènes 07, 13, 14 et 15 en ont besoin.
8. **Étiquette française du projecteur.** `Kit.projector` accepte `planeLabel` ; j'utilise « champs sans divergence ». Ce n'est pas un écart, sauf si le moteur impose l'anglais par défaut ; à noter pour le constructeur.

## Journal des corrections

1. 3.6 : P placé en (620, 340) à l'écran, origine du champ ; déplacement de 300 px (212 à gauche, 212 en bas), arc entrant d'environ 112°, 5 points sur 16 ; cercle vérifié dans le panneau (calcul en tête de scène 03).
2. 9.5 : $\Omega_{\text{roue}} = \omega/2 = -\tfrac12$ dans la colonne ; plus de « ½ » seul sous la flèche horaire.
3. 14.6 : sphère déplacée en 3D, équateur, cercle de tangence vu depuis la charge, petite calotte d'entrée à flèches fortes, grande calotte de sortie à flèches faibles, valeur 0 ; plus de coupe plane à flèches en colonnes.
4. 2.5–2.6 : champ u = (0,6 + 0,4 sin(x + 0,5 y), 0,3 cos x), dont $u_x$ dépend de x.
5. 12.9 (et toute la scène 12) : champ u = (x²/2 − 0,5 y, y + 0,5 x), ∇·u = x + 1, ω = 1.
6. 8.6 : « Ω_roue = 1 » en face de « ω = 2 ».
7. Section 0 : compression L(I) strictement croissante, linéaire sous un seuil, sans plafond dur ; I_s = 1,2 en scène 14, I_s = 0,8 en 10.7 ; 10.12 et la section 5, point 5, corrigés.
8. Scène 16 : Q = (π/2 ; 0,6435), sur la ligne ψ = 0,6.
9. 16.10 : « les grandes valeurs sont toujours à gauche » ; deux « + » côté sommet dans une cellule ψ > 0, deux côté bord dans une cellule ψ < 0 ; vérification réécrite.
10. 12.3–12.4 (et 12.5, 12.9) : une seule flèche par côté, « + » côté gauche, « − » côté droit, aucune flèche retournée.
11. 5.10 : c = (200, 140) px ; la trajectoire de 5.9 s'arrête en c, vitesse nulle ; origines des panneaux décalées pour que cercle et flèches tiennent.
12. Scène 04 : 300 px par unité, h = 1,2 < 1,6 ; valeurs des quatre flèches données.
13. 7.8 : roue posée sur P, point de vitesse nulle, et tournant dans le sens trigonométrique à 0,4 rad/s dès qu'elle est posée.
14. Scène 15 : douze graines en |x| ≤ 0,6 rayon, aucune sur l'axe, traceur sur la ligne de la graine 0,6 rayon qui boucle dans le panneau, lignes tracées comme lignes de niveau de r·A_φ.
15. Scène 01 : Biot–Savart régularisé (ε = 5 px) et points de grille masqués à moins de 10 px d'une spire.
16. Section 0 « Compteurs » : exacts à l'arrondi affiché, jamais « −0 » ; 2π, 4π et 0 des scènes 10, 14 et 15 dits symboliques ; 18.3 : quadrature pondérée par l'élément d'arc, normale extérieure, compteur à 0 sur les images fixes ; section 5, points 2 et 3, alignés.
17. 10.13 : cercle de 220 px décentré de (70, 40) px, qui entoure toujours le centre ; quatrième cercle positionné hors du grand cercle.
18. 13.3–13.4 : empilement de cubes remplissant une boule, il reste l'extérieur de l'empilement, qui fond vers la sphère par subdivisions successives.
19. Scène 19 : formule du pictogramme 2 ($\iint_D \nabla\cdot\mathbf{u}\,dA = \text{flux à travers le bord}$) en 19.2 ; quart de tour trigonométrique en 19.3, pour ω > 0 ; signalé en section 4, point 4.
20. Section 0 « Notations » : la région s'écrit D partout, jamais Ω.
21. Section 4 : ancien point 1 ([r-aubes]) supprimé, points renumérotés.
22. Section 0 et scène 17 : badge SCHEMATIC pour toute la scène 17 ; plus de badge CONTEXT ; le bandeau porte seul la référence.
23. 17.12 : carte agitée à gauche, bandeau ancré dessous ; la vignette des cellules, à droite, perd ω = 2ψ et la barre de couleur.
24. 17.12 : chip `schematic` « illustration · pas une sortie du modèle » ; ni Kolmogorov, ni Re, ni `--model`, ni chip `generated`.
25. 17.8 : le cercle et son compteur sortent à la fin du plan, avant [c-machines] ; aucun chiffre sur la carte agitée.
26. 17.12 : la carte agitée s'ouvre sur ψ, en `Kit.cmap('u')` avec l'étiquette ψ, puis les lignes de courant, avec le rappel u = ∇⊥ψ.
27. 17.12 : 24 modes à nombres d'onde entiers sur [0, 2π]², ψ figé pendant le plan.
