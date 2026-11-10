# Épisode 02 : storyboard

Narration : `video/episodes/ep02/narration.md`, validée (1 782 mots, 11 min 53 s à 150 mots par minute). Traitement : `video/episodes/ep02/traitement.md`. Bible : `video/continuite.md`. Retours : pas de `retours.md` pour ep02 ; ceux de ep01 s'appliquent (enchaîner, trancher soi-même les points mineurs). Épisode précédent : `video/episodes/ep01/narration.md`, dont les motifs sont repris sans être réexpliqués.

Base : l'ancien storyboard relu et corrigé, `video/episodes/ep01/avant-decoupage/storyboard.md`, scènes 12 à 19. Ses champs, ses géométries et les corrections de son « Journal des corrections » sont repris tels quels pour tout ce qui passe ici ; chaque reprise est indiquée par « ancien n.m ».

20 scènes, de 21 à 56 s. Durée estimée, phrase par phrase à 0,4 s par mot : 11 min 45 s (1 763 mots à mon décompte), plus 4 s de pause conseillée après [e2-reflechis]. Le moteur recale tout sur la voix.

## 0. Conventions communes à toutes les scènes

**Repères.** Chaque plan commence sur le repère entre crochets de `narration.md`, qui sert de nom de cue au moteur. Un plan dure jusqu'au repère du plan suivant. Les durées sont estimées phrase par phrase à 0,4 s par mot.

**Registre.** NIGHT pour tout l'épisode (fond `--bg`). Pas de PAPER : aucune page ni figure du site n'est incrustée ; le panneau de gauche de `fig-monopole-dipole.png` est redessiné dans le thème (section 4, point 9).

**Coordonnées.** Tous les champs se calculent analytiquement dans la page, en coordonnées mathématiques, **y vers le haut**. Chaque scène définit `toPx(x, y)`, qui retourne l'axe vertical pour l'écran. C'est une condition des contraintes de sens : sans elle, les bosses de ψ tourneraient dans le sens horaire et les grandes valeurs de ψ passeraient à droite du courant. Le constructeur le vérifie sur une image fixe de la scène 16 (cellule en bas à gauche, ψ > 0, sens trigonométrique) et de la scène 14 (bosse à gauche du courant). Les déplacements en px sont, eux aussi, comptés y vers le haut.

**Notations.** Conformes à `specs/notations.md` et à la bible : domaine $\Omega$, bord $\partial\Omega$, normale sortante $\mathbf{n}$, tangente $\mathbf{t}$ du parcours, $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, $\mathbf{B} = \nabla^\perp a$. L'ancien storyboard écrivait $D$ parce que Ω servait à la roue à aubes ; ep02 n'a pas de roue, donc $\Omega$ partout, comme la narration. Énoncés exacts, ceux de la narration : $\int_\Omega \nabla\cdot\mathbf{u}\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}\ell$ et $\int_\Omega \omega\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{t}\,\mathrm{d}\ell$ ; en 3D, $\oint_{\partial\Omega}\mathbf{B}\cdot\mathbf{n}\,\mathrm{d}S = 0$. Le champ d'une charge n'a pas de lettre (la bible n'en définit pas) : on ne l'écrit jamais $\mathbf{E}$.

**Couleurs.**

| Rôle | Jeton |
|---|---|
| Vitesse u, flèches et lignes de courant, vorticité ω, carte de ψ | `--u` (cartes : `Kit.cmap('u')`, argent pour le négatif, `--u-hi` pour le positif) |
| Champ magnétique B, lignes de B, carte de a | `--b` (cartes : `Kit.cmap('b')`) |
| Cercles en tirets, carreaux, sphères, ballons, cubes, flèches de parcours, flèche de gradient avant le quart de tour, relief en fil de fer | `--chalk` |
| Annotations, étiquettes, « − » des paires qui s'annulent, points d'entrée des lignes | `--muted` |
| Champ de la charge, et les deux cartes de la question tant que le verdict n'est pas tombé | `--fg-2`, neutre (section 5, point 5) |
| Matière de l'aimant | `--matter` ; bout nord teinté `--b`, bout sud `--matter-dark`, comme l'aiguille M1 (`Kit.needle`) |
| Limaille de fer | `--matter` à 70 % |

**Zones.** Contenu dans le cadre sûr (x de 96 à 1824, y de 56 à 880) ; rien sous y = 880. Calque de formule (`Kit.formulaLayer`) en bas à droite pour les formules non dites et les rappels ; bandeau (`Kit.lowerThird`, kind `reference`) en bas à gauche, une seule fois, pour la légende FunDiff (scène 19). Les formules dont la voix dit le sens s'écrivent en grand avec `Kit.equation`, au moment où la voix le dit.

**Mouvement.** Tout est une fonction pure du temps : trajectoires paramétrées par t, traceurs par `Kit.tracers` (Scene.stepper), aucun hasard hors des graines nommées dans le code. Aucun cercle ne rétrécit sur le centre du tourbillon ; en scène 05, les cercles n'apparaissent que du plus petit au plus grand.

**Compteurs.** Seulement là où la carte est un vrai champ du plan : « FLUX ÷ AIRE » sur les cellules (scènes 01 et 16), « FLUX » sur un contour fermé (scènes 17 et 18). Calcul dans la page, à chaque image, par quadrature sur 256 points du bord : composante normale pondérée par l'élément d'arc $\lvert\gamma'(s)\rvert\,\Delta s$, normale orientée vers l'extérieur, parcours trigonométrique. Exacts à l'arrondi affiché ; jamais « −0 ». **Aucun compteur sur une carte qui représente une coupe 3D** (scènes 07 à 12) : seules les valeurs 4π et 0, symboliques, écrites et non calculées. Les valeurs 2π de la scène 05 sont symboliques aussi, les mêmes que dans ep01.

**Longueur des flèches.** Direction exacte ; longueur par la compression de l'ancien storyboard : L(I) = k·I si I ≤ I_s, L(I) = k·I_s·(2 − I_s/I) au-delà, strictement croissante, sans plafond dur. Un petit disque vide entoure chaque point singulier. Seuils :

- charge (scènes 09, 10, 12) : unité 120 px pour R = 1, I_s = 1,2, pour que les flèches des sphères R = 1, 2, 3 se lisent exactement 1, 1/4, 1/9 (60, 15 et 6,7 px) ;
- tourbillon (scène 05) : unité 100 px, I_s = 0,8, comme dans ep01 ;
- gradient (scène 13) : I_s = 1,2, au-dessus de toutes les pentes comparées, donc rapports exacts ;
- aimant (scènes 07, 11, 12) : seuil au-dessus de l'intensité au centre de l'aimant.

**Texte à l'écran.** Aucune phrase de la voix n'est recopiée. L'écran porte des formules, des valeurs symboliques ou de compteur, des pictogrammes et des étiquettes d'une ou deux unités qui nomment un objet dessiné ou une formule (« ψ », « a », « Ω », « ∂Ω », « LIGNE DE CHAMP », « MONOPÔLE », « GREEN–OSTROGRADSKI », « STOKES »). Les seules phrases écrites sont celles que la voix ne dit pas et que la narration exige : le sous-titre de Stokes, la mention des unités de la charge, la mention « les lignes de niveau du potentiel sont les lignes du champ », la légende FunDiff. Étiquettes mono en capitales par `Kit.upper` (les lettres grecques gardent leur casse). Décimales à la virgule.

**Badge d'honnêteté.** Aucun, sauf SCHEMATIC pour toute la scène 19 (FunDiff), du premier au dernier plan. Pas de CONTEXT : le bandeau porte seul la référence. Si le moteur exige un badge par scène, SCHEMATIC partout.

**Motifs repris de ep01, sans les réexpliquer.**

- Le petit cercle en tirets : même tiret (12 px plein, 9 px vide), même épaisseur (3 px), même `--chalk`. Compteur à sa droite, chiffres tabulaires.
- La sphère : un cercle `--chalk` avec un équateur en ellipse en tirets et un léger dégradé radial (ancien 13.2). « Ballon » = la même sphère, voile `--chalk` à 10 %.
- La flèche de parcours : petite flèche courbe `--chalk`, sens trigonométrique sur chaque carreau et chaque cercle mesuré.
- Le marqueur « région à gauche » (nouveau) : sur un bord, un chevron `--chalk` dans le sens du parcours et, à sa gauche, une demi-pastille voilée `--chalk` à 20 % qui touche la région. Il dit d'un coup d'œil de quel côté est la région.
- Le point d'interrogation de l'énigme : `--chalk`, 120 px, logé dans le coin haut gauche à la fin de ep01.

## 1. Découpage en scènes

| Scène | Fichier (`video/scenes/ep02/`) | Paragraphes | Mots (env.) | Durée | Composants |
|---|---|---|---|---|---|
| ep02.01 | `01_enigme.html` | P1, P2 | 98 | 39 s | `Kit.arrows`, `Kit.streamlines`, `Kit.tracers`, cercle-sonde, compteur, `Kit.formulaLayer`, `Kit.pen`, pictogrammes en code de scène |
| ep02.02 | `02_carrelage.html` | P3, P4 | 117 | 47 s | SVG (région, carreaux découpés, flèches de flux), `Kit.equation` |
| ep02.03 | `03_green.html` | P5 | 89 | 36 s | SVG, deux jauges en code de scène, `Kit.equation`, `Kit.morph`, `Kit.formulaLayer` |
| ep02.04 | `04_stokes.html` | P6 | 93 | 37 s | SVG (flèches de parcours, marqueur « région à gauche »), `Kit.equation` ×2, `Kit.formulaLayer` |
| ep02.05 | `05_anneau.html` | P7 | 99 | 40 s | `Kit.arrows`, `Kit.fieldLines`, SVG (anneau carrelé en secteurs), `Kit.equation` |
| ep02.06 | `06_espace.html` | P8 | 61 | 24 s | SVG/canvas en perspective (plan incliné, sphère, cubes), `Kit.equation` |
| ep02.07 | `07_champ_magnetique.html` | P9 | 113 | 45 s | `Kit.arrows`, `Kit.fieldLines`, `Kit.needle`, SVG (aimant, ballon), `Kit.equation`, `Kit.formulaLayer` |
| ep02.08 | `08_monopole.html` | P10 | 66 | 26 s | SVG (point, lignes, sphère), `Kit.equation`, `Kit.pen` |
| ep02.09 | `09_charge.html` | P11 | 123 | 49 s | `Kit.arrows`, SVG (sphères), tableau en code de scène, `Kit.equation`, `Kit.pen` |
| ep02.10 | `10_source_cachee.html` | P12 | 59 | 24 s | `Kit.arrows`, SVG (sphères, calottes, cône tangent) |
| ep02.11 | `11_aimant.html` | P13 | 69 | 28 s | `Kit.arrows`, lignes de niveau (de r·A_φ), traceur, limaille en canvas, SVG |
| ep02.12 | `12_deux_cartes.html` | P14, P15 | 64 | 26 s + 4 s | `Kit.arrows`, `Kit.predictCard`, SVG (sphères en coupe), `Kit.pen` |
| ep02.13 | `13_randonnee.html` | P16, P17 | 141 | 56 s | relief en fil de fer, `Kit.fieldMap`, lignes de niveau, `Kit.equation`, `Kit.pen` |
| ep02.14 | `14_quart_de_tour.html` | P18 | 62 | 25 s | `Kit.fieldMap`, lignes de niveau, `Kit.tracers`, `Kit.equation` |
| ep02.15 | `15_construction.html` | P19 | 79 | 32 s | `Kit.equation`, `Kit.morph`, `Kit.fieldMap` ×3 (vignettes), `Kit.pen` |
| ep02.16 | `16_boite_a_oeufs.html` | P20, P21 | 113 | 45 s | relief en fil de fer, `Kit.fieldMap`, lignes de niveau, `Kit.arrows`, `Kit.tracers`, cercle-sonde, compteur, `Kit.formulaLayer`, `Kit.equation` |
| ep02.17 | `17_potentiel.html` | P22 | 95 | 38 s | `Kit.fieldMap`, lignes de niveau, `Kit.arrows`, `Kit.equation`, cercle-sonde (contour quelconque), compteur, `Kit.pen` |
| ep02.18 | `18_limite.html` | P23 | 52 | 21 s | `Kit.fieldMap`, lignes de niveau, cercle-sonde, compteur, `Kit.pen` |
| ep02.19 | `19_fundiff.html` | P24 | 62 | 25 s | `Kit.badge` (SCHEMATIC), `Kit.fieldMap`, lignes de niveau, `Kit.tracers`, `Kit.chip` ×2, `Kit.lowerThird`, `Kit.formulaLayer`, `Kit.pen` |
| ep02.20 | `20_cloture.html` | P25, P26 | 108 | 43 s | pictogrammes, `Kit.equation`, `Kit.projector`, `Kit.chip` |
| **Total** | | P1 à P26 | 1 763 | **11 min 45 s** | |

« Cercle-sonde », « compteur » et « lignes de niveau » sont des composants proposés (section 5). Tant qu'ils ne sont pas acceptés, ils s'écrivent en code de scène, avec la même apparence partout.

## 2. Plans

### ep02.01 · `01_enigme.html` · P1, P2 · 39 s

Écoulement cellulaire ψ = sin x sin y sur [0, 2π]² (2 × 2 cellules), **même panneau et même trajectoire de cercle que la scène de l'énigme de ep01** ; si elle n'est pas encore construite, panneau de 760 × 760 px centré (x 580 à 1340, y 90 à 850). Flèches `--u`, lignes de courant `--u` à 45 %, traceurs à 40 %. Calque de formule, étiquette « CHAMP » : $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$, comme dans ep01. Aucune mention de ψ dans cette scène : ep01 ne l'a pas affiché.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 1.1 | [e2-rappel] | Les cellules, flèches et lignes de courant ; le calque de formule ; le point d'interrogation de ep01 dans le coin haut gauche. | Fondu d'entrée de 0,6 s ; traceurs en marche. | 4,4 s |
| 1.2 | [e2-souviens] | Le petit cercle en tirets (90 px) se pose ; compteur « FLUX ÷ AIRE » à sa droite. | Le cercle se promène sur la trajectoire de ep01, qui traverse plusieurs cellules et franchit les droites de séparation. | 4,8 s |
| 1.3 | [e2-cellules] | Le compteur reste sur 0 tout au long du trajet. | Promenade continue ; chiffres immobiles. | 3,2 s |
| 1.4 | [e2-question] | Le cercle s'arrête ; le point d'interrogation quitte le coin et vient se poser à côté du compteur. | Glissement de 0,8 s, pulsation du compteur. | 2,8 s |
| 1.5 | [e2-detour] | Les cellules se réduisent en vignette (40 %) en haut à gauche, avec le point d'interrogation. Au centre droit, un pictogramme d'aimant (rectangle vertical, nord `--b`, sud `--matter-dark`). Une flèche au `Kit.pen` (arrow, `bend` 0,3) part de la vignette, contourne l'aimant et revient vers la vignette : le détour. | Réduction de 0,8 s ; l'aimant apparaît ; la flèche se trace en 1,2 s. | 4,4 s |
| 1.6 | [e2-promesse] | À côté de la vignette, un cadre vide en tirets `--muted`, de même taille ; des lignes fermées `--u` s'y dessinent d'elles-mêmes, comme fabriquées. | Tracé des lignes en 1,5 s. Rien n'est nommé. | 5,2 s |
| 1.7 | [e2-plan] | Tout s'efface sauf la vignette des cellules, qui reste en haut à gauche jusqu'à la fin de la scène. Trois emplacements numérotés 1, 2, 3 (mono `--muted`), en colonne, à gauche du centre. | Apparition des numéros. | 2 s |
| 1.8 | [e2-etape1] | Pictogramme 1 : un petit cercle en tirets, puis à côté un carrelage de 3 × 2 carreaux dont le contour s'épaissit. | Le cercle se dédouble en carreaux (0,8 s), le contour s'allume. | 3,6 s |
| 1.9 | [e2-etape2] | Pictogramme 2 : un cercle en tirets qui se gonfle en sphère ; une ligne `--b` la traverse, entre d'un côté et ressort de l'autre. | Gonflement de 1 s, puis la ligne se trace. | 4,4 s |
| 1.10 | [e2-etape3] | Pictogramme 3 : trois lignes de niveau ; une flèche `--chalk` perpendiculaire pivote d'un quart de tour dans le sens horaire, devient tangente et passe en `--u`. | Rotation de 0,8 s, sens horaire, puis fondu de couleur. | 4,4 s |

Les trois pictogrammes reviennent à la scène 20, chacun avec sa formule. Ils remplacent les trois lignes de texte prévues par la narration (section 4, point 1).

### ep02.02 · `02_carrelage.html` · P3, P4 · 47 s

Région $\Omega$ **de forme quelconque**, étoilée, de bord r(θ) = 1 + 0,25 cos 2θ + 0,15 sin 3θ en unités de la région (250 px par unité), centrée à l'écran en (620, 470) : elle tient dans x 270 à 970, y 120 à 820. Colonne d'équation à droite (x 1100 à 1780). Carrelage : la grille de pas 0,25 (62,5 px), **découpée par le bord** ; les carreaux du bord sont des morceaux de carré limités par la courbe. Le découpage est donc exact : la réunion des carreaux est Ω, et leurs côtés non partagés forment exactement $\partial\Omega$. Champ de l'ancienne scène 12 : u = (x²/2 − 0,5 y, y + 0,5 x), origine au centre de la région ; ∇·u = x + 1 et ω = 1, non nulles, pour que les deux énoncés aient un contenu. Sur chaque côté de chaque carreau, **une seule** petite flèche `--u` perpendiculaire au côté, dans le sens du champ, de longueur proportionnelle au flux par ce côté (ancien 12.3, correction 10).

Carreaux de travail : A = [0 ; 0,25] × [−0,5 ; −0,25] et B = [0,25 ; 0,5] × [−0,5 ; −0,25], entiers et dans Ω (le coin le plus loin du centre est à 0,71 < r = 0,89 dans cette direction). Sur leur côté commun x = 0,25, $u_x$ = 0,031 + 0,5·|y| est compris entre 0,16 et 0,28 : positif, la flèche va vers la droite, sans changement de signe le long du côté.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 2.1 | [e2-but] | La région Ω : intérieur voilé `--chalk` à 12 %, contour `--chalk` 3 px. Étiquettes « Ω » dans la région, « ∂Ω » sur le contour. | Le voile pulse une fois, puis le contour pulse une fois : l'intérieur, puis le bord. | 6,8 s |
| 2.2 | [e2-region] | Le contour se déforme lentement (les coefficients 0,25 et 0,15 varient en douceur) puis se fige dans la forme ci-dessus. | Déformation de 2 s, arrêt sans rebond. | 3,2 s |
| 2.3 | [e2-carrelage] | Les lignes du carrelage, découpées par le contour. | Tracé ligne par ligne en 1,2 s. | 2,8 s |
| 2.4 | [e2-chaque] | Le carreau A s'allume ; sur ses quatre côtés, une flèche de flux chacun, avec un « + » `--chalk` là où elle sort de A, un « − » `--muted` là où elle entre. | Les quatre flèches poussent l'une après l'autre. | 4,8 s |
| 2.5 | [e2-voisins] | Le carreau B, à droite de A, s'allume à son tour. | — | 2 s |
| 2.6 | [e2-commun] | Leur côté commun s'épaissit ; les autres flèches de A baissent à 30 %. | Trait de 0,4 s. | 1,6 s |
| 2.7 | [e2-passe] | Sur le côté commun, une seule flèche, vers la droite. Un « + » `--chalk` du côté de A : pour A, elle sort. Un « − » `--muted` du côté de B : pour B, elle entre. Aucune flèche n'est dédoublée ni retournée. | Le « + » puis le « − » s'allument. | 4,4 s |
| 2.8 | [e2-annule] | Le « + » et le « − » glissent l'un vers l'autre sur la flèche et s'annulent ; la flèche du côté commun s'efface avec eux. | Glissement et fusion en 0,6 s. | 5,6 s |
| 2.9 | [e2-tous] | Toutes les flèches de tous les côtés, une par côté, avec leurs paires « + » / « − » sur les côtés intérieurs. | Apparition en 1 s. | 3,6 s |
| 2.10 | [e2-paires] | Les paires s'annulent et les flèches intérieures s'effacent. | Vague de gauche à droite en 1,5 s. | 2 s |
| 2.11 | [e2-bord] | Il reste les flèches posées sur le contour, chacune perpendiculaire au bord. Le contour s'épaissit. | — | 4,8 s |
| 2.12 | [e2-total] | L'intérieur baisse à 30 %. À droite : $\displaystyle\sum_{\text{carreaux}} \text{flux} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}\ell$. | Écriture terme à terme ; un arc `--chalk` fait le tour du contour pendant l'écriture du membre de droite. | 5,2 s |

### ep02.03 · `03_green.html` · P5 · 36 s

Même région, même champ, même colonne. Pour que l'erreur se voie, la divergence d'un carreau est **prise en son coin en bas à gauche**, marqué d'un point `--chalk` : comme ∇·u = x + 1 est affine, l'erreur sur un carreau carré de côté h vaut alors h³/2, soit h/2 fois son aire ; elle est calculée dans la page, par quadrature, y compris pour les carreaux découpés. (Prise au centre, elle serait exactement nulle pour ce champ, et la jauge ne montrerait rien.) Deux jauges verticales sans graduation ni chiffre, en code de scène, à droite du carrelage : « ERREUR ÷ AIRE » pour le carreau mis en avant, « Σ ERREURS » pour toute la région.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 3.1 | [e2-rappeldiv] | Le carreau A mis en avant, ses quatre flèches de flux ; le reste à 30 %. | Zoom de 1,5× sur A en 0,8 s. | 4,8 s |
| 3.2 | [e2-produit] | À côté : $\text{flux}(A) \approx (\nabla\cdot\mathbf{u}) \times \text{aire}(A)$ ; le point du coin s'allume sous le facteur $\nabla\cdot\mathbf{u}$. | Écriture ; le carreau se remplit d'un voile `--chalk` à 15 % sous le facteur « aire ». | 3,6 s |
| 3.3 | [e2-definition] | Calque de formule, rappel de ep01 : $\nabla\cdot\mathbf{u} = \lim_{r\to0} \dfrac{\text{flux}}{\pi r^2}$. | Fondu du calque. | 5,2 s |
| 3.4 | [e2-affine] | Retour au plan large. Les carreaux se subdivisent une fois (pas 0,125). Les deux jauges apparaissent, pleines au départ. | Subdivision en 0,6 s ; les jauges descendent à mi-hauteur, valeurs calculées. | 4 s |
| 3.5 | [e2-erreur] | Seconde subdivision (pas 0,0625). La jauge « ERREUR ÷ AIRE » descend encore de moitié. | Subdivision en 0,6 s ; jauge en 0,6 s. | 5,6 s |
| 3.6 | [e2-erreursomme] | La jauge « Σ ERREURS » descend avec elle et tend vers le bas de sa course. | Descente continue en 1,5 s (subdivisions suivantes, calculées sans être dessinées). | 2,4 s |
| 3.7 | [e2-limite] | Les jauges touchent le fond et s'effacent ; le carrelage le plus fin reste, à 40 %. | Fondu de 0,4 s. | 2,4 s |
| 3.8 | [e2-enonce] | $\sum (\nabla\cdot\mathbf{u})\,\text{aire} \;\to\; \int_\Omega \nabla\cdot\mathbf{u}\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}\ell$. | Écriture du Σ, puis `Kit.morph` du Σ vers l'intégrale ; le membre de droite vient de l'équation de 2.12. | 5,6 s |
| 3.9 | [e2-nom] | Étiquette mono « GREEN–OSTROGRADSKI » au-dessus de l'énoncé. | — | 2 s |

### ep02.04 · `04_stokes.html` · P6 · 37 s

Même région, même champ (ω = 1), carrelage de pas 0,25, mêmes carreaux A et B. Colonne d'équation à droite ; l'énoncé de Green–Ostrogradski y reste en haut, à 40 %.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 4.1 | [e2-stokes0] | Les carreaux A et B ; leurs flèches de flux s'effacent. | Fondu de 0,4 s. | 2,8 s |
| 4.2 | [e2-stokes1] | Dans A et dans B, une flèche de parcours `--chalk` qui fait le tour du carreau, sens trigonométrique. | Chaque flèche fait un tour en 1,2 s, puis reste posée. | 3,2 s |
| 4.3 | [e2-stokes2] | Sur le côté commun, les deux parcours en sens contraires : vers le haut pour A, vers le bas pour B (deux chevrons `--chalk`). Sur ce côté, une seule flèche `--u` tangente, la part du champ le long du côté. Un « + » du côté du carreau dont le parcours suit cette flèche, un « − » de l'autre. | Les chevrons s'allument, puis la flèche `--u`, puis les signes. | 5,6 s |
| 4.4 | [e2-stokes3] | Les signes fusionnent et s'annulent ; la flèche tangente du côté commun s'efface. | 0,6 s. | 2 s |
| 4.5 | [e2-stokesrappel] | Tout le carrelage : une flèche tangente par côté, les paires des côtés intérieurs s'annulent, il reste les flèches tangentes du contour. Colonne : $\text{circulation}(A) \approx \omega \times \text{aire}(A)$. Calque de formule, rappel de ep01 : $\omega = \lim_{r\to0} \dfrac{\text{circulation}}{\pi r^2}$. | Apparition en 1 s, effacement par paires en vague en 1,5 s ; écriture de la formule. | 8 s |
| 4.6 | [e2-stokes4] | $\sum \omega\,\text{aire} \;\to\; \int_\Omega \omega\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{t}\,\mathrm{d}\ell$, sous l'énoncé de Green–Ostrogradski. Dessous, en `--fg-2`, 32 px : « bord parcouru en gardant la région à sa gauche, sens trigonométrique pour une région sans trou ». Sur le contour, trois marqueurs « région à gauche ». | Écriture, `Kit.morph` du Σ vers l'intégrale ; le sous-titre en fondu ; les marqueurs s'allument un à un. | 5,2 s |
| 4.7 | [e2-stokesnom] | Étiquette mono « STOKES » au-dessus de ce second énoncé. | — | 2,8 s |
| 4.8 | [e2-raconte] | Les deux énoncés à 100 % ; le contour s'épaissit, l'intérieur baisse à 30 %. | — | 3,2 s |
| 4.9 | [e2-tour] | Un point `--chalk` fait une fois le tour du contour, sens trigonométrique, un marqueur « région à gauche » attaché à lui. | Un tour en 3 s, vitesse d'arc constante. | 4,4 s |

### ep02.05 · `05_anneau.html` · P7 · 40 s

Tourbillon ponctuel de ep01, u = (−y, x)/(x² + y²), sens trigonométrique, unité 100 px, centre à l'écran en (620, 480), panneau de 1000 × 760 px à gauche (x 120 à 1120, y 100 à 860) ; colonne à droite (x 1180 à 1780). Flèches `--u` compressées (I_s = 0,8), disque vide de 30 px autour du centre, point `--fg` au centre (ancienne scène 10). **Anneau** entre le petit cercle r₁ = 1,2 (120 px) et le grand r₂ = 3,2 (320 px), les deux cercles centrés de ep01. Carrelage de l'anneau en **secteurs** : 3 couronnes (rayons 1,2 ; 1,87 ; 2,53 ; 3,2) × 12 secteurs de 30°. Le disque intérieur r < 1,2 n'est **pas** carrelé : il reste sombre, le centre n'est dans aucun carreau. Aucun cercle ne rétrécit, à aucun moment.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 5.1 | [e2-echo] | Le tourbillon : flèches et cinq lignes de courant circulaires. | Fondu d'entrée. | 2,4 s |
| 5.2 | [e2-echo2] | L'image de ep01 : trois cercles en tirets qui entourent le centre, apparus du plus petit au plus grand (120 px centré ; 220 px décentré de (70, 40) px ; 320 px centré), chacun avec sa valeur « 2π ». | Chaque cercle se trace, sa valeur s'écrit. | 3,6 s |
| 5.3 | [e2-echo3] | Le cercle décentré et les trois valeurs s'effacent. Entre les cercles de 120 et 320 px, l'anneau se voile `--chalk` à 12 % et se carrelle en secteurs. | Tracé des rayons puis des couronnes en 1,2 s. | 3,2 s |
| 5.4 | [e2-anneaubord] | Les deux cercles s'épaississent ; les lignes intérieures du carrelage baissent à 50 %. | — | 2,4 s |
| 5.5 | [e2-anneausens] | Dans chaque carreau, une flèche de parcours trigonométrique. Sur chaque côté partagé, deux chevrons opposés, qui s'effacent par paires. Il reste : sur le grand cercle, des chevrons dans le **sens trigonométrique** ; sur le petit, dans le **sens horaire**. Un marqueur « région à gauche » sur chaque cercle : sa demi-pastille touche l'anneau dans les deux cas (vers l'intérieur pour le grand cercle, vers l'extérieur pour le petit). | Flèches de parcours en 0,8 s ; effacement des paires en vague, en 1,5 s ; chevrons du bord qui défilent doucement dans leur sens. | 6 s |
| 5.6 | [e2-anneaudiff] | Colonne : $\oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{t}\,\mathrm{d}\ell = \text{circulation}(\text{grand}) - \text{circulation}(\text{petit})$. Le terme « grand » souligné en `--chalk` en même temps que le grand cercle pulse, puis le terme « petit » avec le petit cercle. | Écriture terme à terme ; pulsations synchronisées. | 5,6 s |
| 5.7 | [e2-anneaunulle] | Dans l'anneau, en trois endroits, « ω = 0 » en `--u`. Au-dessus de l'équation : $\int_\Omega \omega\,\mathrm{d}\mathbf{x} = 0$. | Les trois étiquettes s'allument une à une ; écriture. | 5,6 s |
| 5.8 | [e2-echo4] | $\text{circulation}(\text{grand}) - \text{circulation}(\text{petit}) = 0$, en grand, sous le reste. | `Kit.morph` depuis l'équation de 5.6. | 4,8 s |
| 5.9 | [e2-echo5] | Le point du centre passe en `--u-hi` ; l'anneau baisse à 40 %. | Pulsation lente. | 2,4 s |
| 5.10 | [e2-echo6] | « 2π » sur le petit cercle, puis sur le grand ; puis un troisième cercle, décentré, entre les deux, qui entoure le centre, avec « 2π ». | Valeurs écrites l'une après l'autre ; le troisième cercle se trace (il apparaît, il ne rétrécit pas). | 3,6 s |

### ep02.06 · `06_espace.html` · P8 · 24 s

Dessins en SVG ou canvas 2D (ancienne scène 13) : la sphère est un cercle `--chalk` avec un équateur en ellipse en tirets et un dégradé radial ; les cubes sont en perspective isométrique, arêtes `--chalk`, arêtes cachées en tirets, peints du fond vers l'avant.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 6.1 | [e2-planjusque] | Le carrelage de la scène 04, à plat, contour épais. | Il s'incline en perspective (60°) en 1,2 s. | 2,8 s |
| 6.2 | [e2-sphere] | Un petit cercle en tirets posé sur le plan se gonfle en sphère. | L'équateur apparaît, le dégradé se lève, en 1,5 s. | 3,6 s |
| 6.3 | [e2-volume] | Un carreau se soulève en petit cube. À côté : $\pi r^2$ devient $\tfrac43\pi r^3$. | Extrusion de 1 s ; `Kit.morph` de la formule. | 4,4 s |
| 6.4 | [e2-peau] | À droite du plan, un ballon (sphère, voile `--chalk` à 10 %). L'étiquette « ∂Ω » quitte le contour du plan et se pose sur la peau du ballon, qui s'allume. | Glissement de l'étiquette en 0,8 s. | 6 s |
| 6.5 | [e2-pareil] | Le ballon se remplit de cubes : les 32 cubes d'une grille 4 × 4 × 4 dont le centre est dans la boule. | Cubes posés couche par couche en 1,5 s. | 2 s |
| 6.6 | [e2-faces] | Les faces communes s'effacent par paires ; il reste l'extérieur de l'empilement, une surface fermée en escalier, voilée à 15 %. Puis subdivisions (8 × 8 × 8, 16 × 16 × 16, toujours les cubes dont le centre est dans la boule) : l'escalier s'affine et fond vers la peau lisse du ballon. | Effacement en vague en 1,5 s ; deux subdivisions à 1 s d'écart ; fondu de 0,6 s vers la sphère lisse (ancien 13.4, correction 18). | 5,6 s |

### ep02.07 · `07_champ_magnetique.html` · P9 · 45 s

Panneau à gauche (x 120 à 1000, y 100 à 860), colonne à droite (x 1100 à 1780). Aimant étendu de l'ancienne scène 01 : rectangle vertical de 60 × 180 px, centré en (560, 520), nord en haut ; champ d'une pile de 24 spires par Biot–Savart, **noyau régularisé** (ε = 5 px) et points de grille masqués à moins de 10 px d'une spire (correction 15). Flèches `--b` sur une grille 11 × 11, compressées. Jamais de dipôle ponctuel.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 7.1 | [e2-champb] | L'aimant, puis ses flèches `--b`. Le ballon de la scène 06 se réduit et attend dans le coin haut gauche du panneau. | Fondu de l'aimant ; flèches qui poussent depuis leur pied, en 0,8 s. | 4,4 s |
| 7.2 | [e2-boussole] | Une boussole (`Kit.needle`, size 160) posée sur l'axe, au-dessus de l'aimant, en (560, 250) : l'aiguille, nord `--b` en haut, s'aligne sur la flèche du champ à cet endroit. | Entrée de 0,4 s ; l'aiguille part de 40° et rejoint l'axe avec un amorti ≤ 3 %. | 2,8 s |
| 7.3 | [e2-loi] | Colonne : $\nabla\cdot\mathbf{B} = 0$ en grand. | Écriture. | 4,8 s |
| 7.4 | [e2-admet] | Accolade sous $\nabla\cdot\mathbf{B}$, étiquette $\lim \dfrac{\text{flux}}{\text{volume}}$ en `--muted` : la définition rappelée, plutôt qu'un texte qui répète la voix. La boussole s'efface. | Accolade de 0,3 s. | 5,2 s |
| 7.5 | [e2-global] | Le ballon glisse dans le champ, à droite de l'aimant, centré en (800, 420), rayon 90 px : il n'entoure pas l'aimant. | Glissement de 1 s. | 3,6 s |
| 7.6 | [e2-surface] | Sous $\nabla\cdot\mathbf{B} = 0$ : $\Longleftrightarrow\ \oint_{\partial\Omega}\mathbf{B}\cdot\mathbf{n}\,\mathrm{d}S = 0$ pour tout $\Omega$. | Écriture ; la peau du ballon s'allume pendant celle du membre de gauche. | 4 s |
| 7.7 | [e2-ressort] | Quatre lignes de B (`Kit.fieldLines`, `--b`) traversent le ballon ; chaque ligne entre en un point `--muted` et ressort en un point `--b` : quatre entrées, quatre sorties. | Tracé en 1,5 s, points marqués un à un. | 5,2 s |
| 7.8 | [e2-lignechamp] | Les deux formules passent dans le calque de formule. Dans la colonne, un encart de 560 × 360 px : un morceau du champ de l'aimant, quelques flèches `--b`, et une courbe `--b` tracée le long d'elles, chaque flèche tangente à la courbe ; étiquette « LIGNE DE CHAMP ». | La courbe se trace en suivant les flèches, en 1,5 s. | 5,6 s |
| 7.9 | [e2-lignecourant] | Sous l'encart, un encart jumeau : un morceau d'écoulement de ep01 (le cisaillement), flèches `--u` et une ligne de courant `--u` tracée le long d'elles. Un signe « = » `--chalk` entre les deux encarts. Pas d'étiquette. | Même geste, même rythme. | 4,4 s |
| 7.10 | [e2-traverse] | Les encarts s'effacent. Sur l'aimant, une esquisse : trois lignes `--b` qui passent **à travers** le corps de l'aimant, du sud vers le nord, et en sortent. Sans détail, sans boucle complète. | Tracé de 1,2 s, du bas vers le haut. | 5,2 s |

### ep02.08 · `08_monopole.html` · P10 · 26 s

Panneau central de 900 × 700 px, fond `--panel` : une hypothèse, pas un champ existant. Lignes `--b` **en tirets, à 60 %**.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 8.1 | [e2-imagine] | Un point `--fg` au centre ; douze lignes en tirets partent de lui dans toutes les directions, avec une pointe vers l'extérieur. | Lignes tracées vers l'extérieur en 1,2 s. | 3,6 s |
| 8.2 | [e2-suppose] | Trois lignes seulement arrivent vers le point, pointes vers lui. | Tracé vers l'intérieur. | 2,8 s |
| 8.3 | [e2-ballon] | Une petite sphère en tirets autour du point (rayon 110 px). Sur sa peau : douze points de sortie `--b`, trois points d'entrée `--muted`. | Tracé de la sphère, puis marquage des points. | 5,2 s |
| 8.4 | [e2-interdit] | À droite : $\oint_{\partial\Omega}\mathbf{B}\cdot\mathbf{n}\,\mathrm{d}S \neq 0$ ; au-dessus, à 40 %, la règle $= 0$ de la scène 07. | Écriture ; le « ≠ » pulse. | 4 s |
| 8.5 | [e2-aucun] | Le panneau de l'hypothèse est barré au `Kit.pen` (cross, `--chalk`). | Trait de 0,6 s. | 6 s |
| 8.6 | [e2-monopole] | Étiquette mono « MONOPÔLE » sous le panneau barré. | — | 4,8 s |

### ep02.09 · `09_charge.html` · P11 · 49 s

Panneau de gauche de `fig-monopole-dipole.png`, **redessiné dans le thème** : charge ponctuelle au centre d'un panneau de 760 × 760 px (x 136 à 896, y 80 à 840), champ r̂/r² en `--fg-2`, unité 120 px, flèches sur une grille 13 × 13, compressées avec I_s = 1,2, disque vide de 40 px, point `--fg` au centre. Colonne à droite (x 1000 à 1780) pour le tableau et les formules. **Aucun compteur** : seules valeurs, 4π et 0, symboliques.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 9.1 | [e2-charge] | Le panneau, vide ; le point de la charge. | Fondu d'entrée. | 2,8 s |
| 9.2 | [e2-partent] | Les flèches `--fg-2`. | Elles poussent depuis la charge vers l'extérieur, en vague radiale de 1,2 s. | 4 s |
| 9.3 | [e2-coupe] | Deux cercles en tirets `--chalk` : l'un centré sur la charge (R = 1, 120 px), l'autre déplacé, centre à (1,7 ; 1,7), rayon 1, qui n'entoure pas la charge. | Tracé au trait en 0,8 s chacun. | 5,2 s |
| 9.4 | [e2-transparents] | Les deux cercles gagnent un équateur en ellipse et un voile : des ballons transparents. | Gonflement de 1,2 s (ancien 14.2). | 4 s |
| 9.5 | [e2-centree] | Le ballon déplacé s'efface (il revient à la scène 10). La grille de flèches baisse à 25 %. | Fondu. | 2,4 s |
| 9.6 | [e2-enface] | Sur la sphère R = 1, douze flèches perpendiculaires à la sphère, toutes de **même longueur** (60 px). | Elles poussent ensemble. | 5,6 s |
| 9.7 | [e2-faiblit] | Sphères centrées R = 2 et R = 3 (240 et 360 px), chacune avec douze flèches perpendiculaires, de même longueur sur une même sphère, **plus courtes** d'une sphère à la suivante : 15 px puis 6,7 px, rapports exacts 1, 1/4, 1/9. | Une sphère après l'autre. | 3,6 s |
| 9.8 | [e2-diviseequatre] | Colonne : « intensité = 1/R² », dessous en `--muted` « unités choisies pour que l'intensité vaille 1/R² ». Tableau, colonnes « R » et « intensité » : 1 → 1, 2 → 1/4, 3 → 1/9. Les lignes R = 1 et R = 2 surlignées, et en même temps les flèches des sphères R = 1 et 2. | Écriture de la formule, puis des lignes du tableau. | 3,6 s |
| 9.9 | [e2-grandit] | Les voiles des trois sphères s'allument, de plus en plus grands. | Fondu échelonné. | 2,4 s |
| 9.10 | [e2-multquatre] | « aire = 4πR² » ; colonne « aire » : 4π, 16π, 36π, lignes R = 1 et 2 surlignées. | Écriture. | 3,6 s |
| 9.11 | [e2-produit2] | « flux = $\dfrac{1}{R^2} \times 4\pi R^2$ ». | Écriture terme à terme. | 3,6 s |
| 9.12 | [e2-memeprod] | Les deux $R^2$ barrés au `Kit.pen` (cross, petit) ; colonne « flux » : 4π, 4π, 4π. | Barres, puis colonne. | 4,8 s |
| 9.13 | [e2-quatrepi] | « flux = 4π » encadré au `Kit.pen` (box). Valeur 4π posée à côté de chaque sphère. | Trait de 0,6 s. | 3,6 s |

Pas de compteur « flux divisé par l'aire », nulle part.

### ep02.10 · `10_source_cachee.html` · P12 · 24 s

Même panneau ; le tableau et les sphères R = 2 et 3 sont partis. Géométrie de la sphère déplacée (ancien 14.6, correction 3) : rayon ρ = 1, centre à (1,7 ; 1,7), à d ≈ 2,40 de la charge. Le cône tangent issu de la charge la touche le long d'un cercle, à α = arccos(ρ/d) ≈ 65° de la direction de la charge, vu du centre de la sphère. Il sépare une **calotte d'entrée** tournée vers la charge, petite (environ 29 % de l'aire), et une **calotte de sortie**, grande (environ 71 %). Intensité normale au point le plus proche (à 1,4 de la charge) : environ 0,51 ; au plus éloigné (à 3,4) : environ 0,09.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 10.1 | [e2-pourtant] | Cinq tout petits ballons (rayon 18 px) posés çà et là hors de la charge, chacun avec la valeur « 0 ». | Ils apparaissent l'un après l'autre. | 4,4 s |
| 10.2 | [e2-cache] | Les petits ballons s'effacent ; le point de la charge s'allume en `--fg`. | Pulsation. | 3,6 s |
| 10.3 | [e2-entoure] | La sphère centrée R = 1 revient, valeur « 4π ». | Tracé, valeur. | 3,6 s |
| 10.4 | [e2-cote] | La sphère déplacée, dessinée en 3D : contour, équateur en ellipse en tirets, cercle de tangence en ellipse `--chalk` pleine de 2 px, et les deux génératrices du cône tangent en tirets `--muted`, de la charge aux bords de ce cercle. Petite calotte d'entrée teintée `--muted` à 25 %, avec des flèches perpendiculaires **entrantes et fortes** ; grande calotte de sortie teintée `--fg-2` à 12 %, avec des flèches **sortantes et faibles**, plus nombreuses ; part perpendiculaire nulle sur le cercle de tangence. Valeur « 0 ». | Sphère, cône et cercle de tangence, teinte des calottes, flèches (calotte d'entrée d'abord), puis la valeur. | 3,2 s |
| 10.5 | [e2-tourbillon] | À droite, vignette du tourbillon de la scène 05 : centre, cercles qui l'entourent, valeurs 2π. Les deux centres reliés par un trait `--muted` en tirets. | Fondu de la vignette, puis le trait. | 4,4 s |
| 10.6 | [e2-sortie] | Le point de la charge et le centre du tourbillon pulsent ensemble ; « 4π » et « 2π » s'allument ensemble. | Deux pulsations synchronisées. | 4,4 s |

### ep02.11 · `11_aimant.html` · P13 · 28 s

Aimant étendu de la scène 07, en grand (rectangle de 90 × 270 px, mêmes proportions), panneau de 900 × 760 px à gauche. Lignes de champ = **lignes de niveau de r·A_φ** (r : distance à l'axe ; A_φ : potentiel vecteur azimutal des 24 spires, même régularisation), tracées par marching squares. Niveaux : les valeurs de r·A_φ en **douze graines** du plan médian, x = ±0,1 à ±0,6 rayon de l'aimant par pas de 0,1, **aucune sur l'axe** (ancien 15, correction 14). Le traceur est sur la ligne de la graine +0,6, qui boucle entièrement dans le panneau ; le constructeur le vérifie sur image fixe, sinon il prend la graine la plus éloignée de l'axe dont la ligne boucle dans le panneau. La position du traceur est une fonction pure du temps, réglée par abscisse curviligne : il est sur la face nord au début de [e2-sortent], sur la face sud au début de [e2-traversent], de nouveau sur la face nord au début de [e2-sansfin].

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 11.1 | [e2-aimant] | L'aimant seul, au centre du panneau. | Fondu d'entrée. | 2 s |
| 11.2 | [e2-dipole] | Ses flèches `--b`, y compris à l'intérieur de l'aimant, où elles vont du sud vers le nord. | Les flèches poussent. | 4,4 s |
| 11.3 | [e2-limaille] | Les flèches baissent à 30 %. Limaille : 1 500 grains (traits de 10 px, `--matter` à 70 %), à des positions tirées d'une graine nommée, chacun orienté selon le champ en son point, aucun dans l'aimant. Puis les lignes de niveau `--b` se tracent par-dessus. | Les grains tombent en 0,8 s (fondu, petit pivot vers leur direction, amorti ≤ 3 %) ; lignes tracées en 1,5 s. | 4,4 s |
| 11.4 | [e2-sortent] | Un traceur `--fg` quitte la face nord le long de sa ligne. | Avance à vitesse d'arc réglée. | 2,8 s |
| 11.5 | [e2-fonttour] | Le traceur fait le tour par l'extérieur et arrive à la face sud. | — | 4,4 s |
| 11.6 | [e2-traversent] | Le traceur traverse l'aimant du sud au nord ; le tronçon intérieur de sa ligne s'allume en `--b-hi`. | — | 2,8 s |
| 11.7 | [e2-sansfin] | Le traceur continue sur sa ligne, sans arrêt ; deux autres traceurs partent sur deux autres lignes. | Boucle continue. | 2,4 s |
| 11.8 | [e2-nul] | Deux sphères en coupe : une centrée qui entoure tout l'aimant (rayon 200 px), une déplacée en haut à droite. Valeur « 0 » sur chacune. | Tracé des sphères, valeurs. | 4,4 s |

### ep02.12 · `12_deux_cartes.html` · P14, P15 · 26 s + 4 s

Les deux cartes de l'ancienne scène 01, côte à côte : à gauche (x 136 à 896), la charge de la scène 09 ; à droite (x 1024 à 1784), l'aimant étendu de la scène 07, y 120 à 840. **Les deux en `--fg-2`, flèches et corps de l'aimant neutres (`--matter`, sans teinte nord)** jusqu'au verdict : la couleur ne donne pas la réponse. Sur chaque carte, deux cercles en tirets `--chalk`, l'un centré (gauche : rayon 150 px ; droite : 170 px, qui entoure tout l'aimant), l'autre déplacé en haut à droite, qui n'entoure rien (gauche : centre à (204, 204) px de la charge, rayon 120 px). Sans étiquette.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 12.1 | [e2-deuxcartes] | Les deux cartes, leurs cercles. Au-dessus, centrée en x 960, y 60, une `Kit.predictCard` compacte (sans question) : kicker « TA RÉPONSE », deux options « GAUCHE » et « DROITE ». | Les flèches poussent, gauche puis droite ; la carte de réponse descend. | 4,4 s |
| 12.2 | [e2-reflechis] | Les quatre cercles pulsent une fois. Puis rien ne bouge. **Pause conseillée de 4 s** (`hold_after`). | Pulsation de 0,6 s, puis maintien. | 4,8 s + 4 s |
| 12.3 | [e2-critere] | Chaque carte s'incline en perspective (35°) ; sur chacun de ses cercles se lève une sphère dont le cercle est la coupe ; puis les cartes se remettent à plat, les cercles gardent leur équateur. | Inclinaison de 1 s, maintien, retour de 0,8 s. | 4,8 s |
| 12.4 | [e2-critere2] | Les valeurs s'écrivent : à gauche, 4π sur le cercle centré, 0 sur le déplacé ; à droite, 0 et 0. Calque de formule : $\oint_{\partial\Omega}\mathbf{B}\cdot\mathbf{n}\,\mathrm{d}S = 0$ pour tout $\Omega$. | Valeurs une à une. | 4 s |
| 12.5 | [e2-verdict1] | L'option « DROITE » s'allume (`answerAt`). La carte de droite passe en `--b`, le bout nord de l'aimant se teinte. `Kit.pen` check `--chalk` sous la carte de droite. | Fondu de couleur de 0,8 s ; coche de 0,6 s. | 4 s |
| 12.6 | [e2-verdict2] | `Kit.pen` cross sous la carte de gauche, puis un cercle au `Kit.pen` autour de la charge et de sa valeur 4π. | Croix, puis cercle, 0,6 s chacun. La carte de réponse reste allumée au moins 1,2 s, puis sort. | 3,6 s |

### ep02.13 · `13_randonnee.html` · P16, P17 · 56 s

Carte des hauteurs **générique**, pas encore la boîte à œufs (révélée à la scène 16) : ψ(x, y) = exp(−((x + 1,2)² + y²)/0,8) + 0,7 exp(−((x − 1,6)² + (y − 0,3)²)/3), une bosse étroite (pente forte) et une bosse large (pente douce), sur [−3,2 ; 4] × [−2,6 ; 2,6], unité 125 px, panneau de 900 × 650 px à gauche (x 120 à 1020, y 120 à 770). Colonne à droite (x 1120 à 1780). Carte `Kit.fieldMap` kind `u`. Lignes de niveau ψ = 0,1 à 0,9 par pas de 0,1, plus les deux niveaux exacts ψ(Q) et ψ(Q′), en `--fg-2` fin, par marching squares.

Points de travail : **Q = (−1,2 ; −0,6)**, sur le flanc de la bosse étroite, sous son sommet : ∇ψ(Q) ≈ (0,07 ; 0,98), presque vers le haut. **Q′ = (1,6 ; −1,0)**, sur le flanc de la bosse large : ∇ψ(Q′) ≈ (0 ; 0,35). Rapport des longueurs ≈ 2,8, exact à l'écran (sous le seuil). Gradients calculés analytiquement dans la page.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 13.1 | [e2-verifier] | Au centre, à gauche, le pictogramme du test de la scène 12 : une sphère en coupe et une coche. | Coche au `Kit.pen`. | 2 s |
| 13.2 | [e2-mieux] | À droite, le pictogramme 3 de la scène 01 : la flèche qui pivote et devient tangente. La coche baisse à 40 %. | Le pictogramme rejoue son geste. | 3,2 s |
| 13.3 | [e2-hauteurs] | Les pictogrammes s'effacent. Le relief de ψ en fil de fer `--chalk` (grille 40 × 30), en perspective, chaque maille teintée par `Kit.cmap('u')`. | Le relief se lève depuis le plan en 1,2 s. | 4 s |
| 13.4 | [e2-altitude] | Un point `--chalk` se promène sur le relief ; un fil vertical `--muted` le relie à son ombre sur le plan, et sa hauteur suit ψ. | Trajet de 3 s. | 3,6 s |
| 13.5 | [e2-outil] | Le relief s'aplatit dans la carte de couleur vue de dessus ; étiquette « ψ(x, y) ». | Aplatissement et retour de face en 1,2 s. | 4,4 s |
| 13.6 | [e2-niveau] | Les lignes de niveau se tracent. | Du sommet vers l'extérieur, en 1,5 s. | 4 s |
| 13.7 | [e2-marche] | Un petit point `--chalk` posé en Q. | Pose de 0,4 s. | 2,4 s |
| 13.8 | [e2-gradient] | En Q, une flèche `--chalk` vers la montée la plus raide, vers le sommet de la bosse étroite. | Elle pousse depuis son pied. | 4,4 s |
| 13.9 | [e2-gradnom] | Étiquette $\nabla\psi$ au bout de la flèche. | — | 1,6 s |
| 13.10 | [e2-gradcomp] | Colonne : $\nabla\psi = (\partial_x\psi,\ \partial_y\psi)$. Sur la carte, les deux composantes de la flèche en tirets `--chalk`, horizontale puis verticale, chacune reliée à son terme par la couleur du surlignage. | Écriture terme à terme ; projections de 0,5 s chacune, synchronisées. | 6,8 s |
| 13.11 | [e2-angle] | Petit carré d'angle droit `--chalk` entre la flèche et la ligne de niveau ψ = ψ(Q), qui passe par Q et s'allume. | Tracé. | 4,4 s |
| 13.12 | [e2-pente] | Cinq flèches de gradient le long d'une droite qui descend du sommet de la bosse étroite vers l'extérieur : les plus longues là où les lignes se serrent. | Elles poussent l'une après l'autre. | 3,6 s |
| 13.13 | [e2-douce] | En Q′, sur la bosse large, une flèche de gradient courte ; ses lignes de niveau sont écartées. Les deux flèches de Q et Q′ restent côte à côte en vue. | Elle pousse. | 2,8 s |
| 13.14 | [e2-randonneur] | Un point `--chalk` part de (−0,4 ; −1,1) et monte en suivant le gradient jusqu'au sommet de la bosse étroite ; sa trace coupe chaque ligne de niveau à angle droit. | Trajectoire intégrée dans `setup` (ascension de plus grande pente), parcourue en 3 s. | 4,4 s |
| 13.15 | [e2-plat] | Un second point part de Q′ et fait le tour de la bosse large sur sa ligne de niveau ; un fil vertical `--muted` de longueur constante montre que sa hauteur ne change pas. | Un tour en 4 s. | 4,8 s |

### ep02.14 · `14_quart_de_tour.html` · P18 · 25 s

Même carte, même point Q, même colonne. En Q, $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi) \approx (0{,}98 ; -0{,}07)$ : vers la droite, la bosse au-dessus, donc à gauche du courant.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 14.1 | [e2-quart] | La flèche de gradient en Q pivote d'un quart de tour dans le **sens horaire** autour de Q : du haut vers la droite. Un arc `--muted` avec pointe horaire montre le geste. | Rotation de 1,2 s, inOutCubic. | 4,4 s |
| 14.2 | [e2-suit] | La flèche est tangente à la ligne ψ = ψ(Q), qui s'allume. | — | 4 s |
| 14.3 | [e2-vitesse] | La flèche passe de `--chalk` à `--u` ; étiquette $\nabla^\perp\psi$. | Fondu de couleur de 0,6 s. | 3,2 s |
| 14.4 | [e2-courant] | Toutes les lignes de niveau passent en `--u` et reçoivent des pointes dans le sens de $\nabla^\perp\psi$ ; traceurs `--u` à 40 % (300 particules). Autour de chaque bosse, ils tournent dans le sens trigonométrique. | Pointes réparties en 1 s ; traceurs en marche. | 4 s |
| 14.5 | [e2-gauche] | Quatre petits « + » `--chalk`, chacun juste à gauche du courant, du côté des plus grandes valeurs : deux sur des lignes de la bosse étroite, un sur une ligne de la bosse large, un sur une ligne extérieure qui entoure les deux bosses. | Les « + » s'allument un à un. | 4,4 s |
| 14.6 | [e2-fonction] | Colonne : $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi,\ -\partial_x\psi)$ ; sous la carte, l'étiquette devient « ψ : fonction de courant ». | Écriture terme à terme ; fondu de l'étiquette. | 4,8 s |

### ep02.15 · `15_construction.html` · P19 · 32 s

Équation en grand au centre (ancien 17.1 à 17.5). Sous chaque terme, un petit pictogramme d'ordre en `--muted` : deux flèches qui disent la direction de la première puis de la seconde dérivation (↑ puis → pour $\partial_x\partial_y\psi$ ; → puis ↑ pour $\partial_y\partial_x\psi$).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 15.1 | [e2-calcul] | $\nabla\cdot\mathbf{u} =$ au centre. | Écriture. | 2,4 s |
| 15.2 | [e2-deuxtermes] | $\nabla\cdot\mathbf{u} = \partial_x\partial_y\psi - \partial_y\partial_x\psi$, premier terme `--u`, second `--chalk`. | Écriture terme à terme. | 1,6 s |
| 15.3 | [e2-terme1] | Focus sur le premier terme (le reste à 35 %) ; pictogramme ↑ puis →. | Les deux flèches du pictogramme se tracent l'une après l'autre. | 4,8 s |
| 15.4 | [e2-terme2] | Focus sur le second terme et le signe moins ; pictogramme → puis ↑. | Idem. | 5,2 s |
| 15.5 | [e2-ordre] | Dans le second terme, $\partial_y$ et $\partial_x$ échangent leurs places ; son pictogramme devient ↑ puis →. | `Kit.morph` de 0,8 s. | 4,8 s |
| 15.6 | [e2-zero] | Les deux termes, identiques, se superposent ; « = 0 » s'écrit. | Superposition en 0,6 s. | 4 s |
| 15.7 | [e2-toujours] | Sous l'équation, trois vignettes de cartes ψ différentes (`Kit.fieldMap` kind `u`, 240 × 240 px) : la carte des deux bosses, et deux sommes de modes de Fourier tirées de graines nommées. Chacune avec ses lignes de courant et une coche. Aucune n'est la boîte à œufs. | Vignettes en cascade, coches au `Kit.pen`. | 3,6 s |
| 15.8 | [e2-livree] | « = 0 » encadré au `Kit.pen` (box). | Trait de 0,6 s. | 5,2 s |

### ep02.16 · `16_boite_a_oeufs.html` · P20, P21 · 45 s

ψ = sin x sin y sur [0, 2π]², 2 × 2 cellules, panneau de 760 × 760 px à gauche (x 140 à 900, y 100 à 860), colonne à droite. Lignes de niveau ψ = ±0,2, ±0,4, ±0,6, ±0,8. Cellule en bas à gauche (0 < x, y < π) : ψ > 0, une bosse, sens trigonométrique ; image fixe de contrôle (section 0).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 16.1 | [e2-boite] | Le relief de ψ en fil de fer, en perspective, bosses et creux alternés ; puis, dans la colonne, $\psi = \sin x\,\sin y$. | Le relief se lève en 1,2 s ; la formule s'écrit à la fin du plan. | 6 s |
| 16.2 | [e2-formule] | La formule soulignée au `Kit.pen` ; le relief s'aplatit en carte de couleur avec ses lignes de niveau. | Trait de 0,4 s ; aplatissement de 1,2 s. | 2 s |
| 16.3 | [e2-revoila] | Les flèches de vitesse `--u` apparaissent le long des lignes de niveau, chacune tangente. | Vague depuis les sommets et les creux. | 5,6 s |
| 16.4 | [e2-retrouve] | Lignes de niveau en `--u`, traceurs : les cellules alternées de ep01 tournent. Calque de formule, étiquette « CHAMP » : $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$, comme à la scène 01. | Fondu des traceurs en 0,6 s. | 2,4 s |
| 16.5 | [e2-reponse] | La vignette de l'énigme de la scène 01 et son point d'interrogation reviennent en haut à gauche ; le point d'interrogation s'efface. | Fondu, puis effacement de 0,6 s. | 5,6 s |
| 16.6 | [e2-zero2] | Le petit cercle et son compteur « FLUX ÷ AIRE » repassent sur la trajectoire de la scène 01 ; compteur à 0. | Trajectoire de 3 s, puis le cercle, son compteur et la vignette s'effacent en 0,4 s, avant la fin du plan. | 4 s |
| 16.7 | [e2-bosse] | Sur les deux bosses (ψ > 0 : en bas à gauche et en haut à droite), une flèche courbe `--chalk` dans le sens trigonométrique et un petit « + ». | Les flèches courbes se dessinent ; traceurs à 40 %. | 4 s |
| 16.8 | [e2-creux] | Sur les deux creux (ψ < 0), une flèche courbe dans le sens horaire et un petit « − ». | Idem. | 3,6 s |
| 16.9 | [e2-frontieres] | Les droites x = kπ et y = kπ en `--chalk`, étiquette « ψ = 0 ». | Tracé en 0,8 s. | 3,6 s |
| 16.10 | [e2-vort2] | La carte passe de ψ à ω : même motif, échelle deux fois plus étendue (barre de couleur `--muted` graduée ψ : ±1, puis ω : ±2). Colonne : $\omega = 2\psi$. | Fondu de 0,8 s entre les deux graduations ; écriture. | 5,6 s |
| 16.11 | [e2-toimeme] | $\omega = 2\psi$ souligné au `Kit.pen`. | Trait de 0,4 s. | 2,8 s |

### ep02.17 · `17_potentiel.html` · P22 · 38 s

La carte des cellules de la scène 16 (pas une autre carte), renommée a, en `Kit.cmap('b')`. Champ $\mathbf{B} = \nabla^\perp a$ avec a = sin x sin y. Mêmes panneau et colonne.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 17.1 | [e2-dansplan] | Au centre, le ballon de la scène 07, traversé de ses lignes `--b`, en perspective ; il s'aplatit en un cercle posé sur un plan, et le plan revient de face. | Aplatissement de 1,2 s, retour de face de 0,8 s, puis fondu vers la carte. | 4,8 s |
| 17.2 | [e2-recette] | La carte de ψ de la scène 16, lignes de niveau, à gauche. | Fondu d'entrée. | 4 s |
| 17.3 | [e2-potentiel] | L'étiquette ψ devient a ; la carte passe de `--u` à `--b`. Sous la carte : « a : potentiel magnétique ». | Fondu de couleur de 1 s. | 4,4 s |
| 17.4 | [e2-memegeste] | Colonne, deux lignes en regard : $\psi \;\mapsto\; \mathbf{u} = \nabla^\perp\psi$ en `--u`, à 40 % ; en dessous, $a \;\mapsto\; ?$ en `--b`. | Écriture. | 2,8 s |
| 17.5 | [e2-tourne] | Sur la carte, en un point, la flèche de pente `--chalk` pivote d'un quart de tour dans le sens horaire et passe en `--b` ; puis toutes les flèches `--b` apparaissent le long des lignes de niveau, qui passent en `--b`. Dans la colonne, le « ? » devient $\mathbf{B} = \nabla^\perp a$. Sous la carte, en `--fg-2`, 32 px : « les lignes de niveau du potentiel sont les lignes du champ ». | Rotation de 0,8 s ; vague de flèches ; `Kit.morph` du « ? ». | 6 s |
| 17.6 | [e2-champ] | Colonne : $\nabla\cdot\mathbf{B} = 0$ et une coche au `Kit.pen` ; sur la carte, un traceur `--fg` suit une ligne de niveau, les flèches de B tangentes sur son passage. | Écriture, coche ; traceur continu. | 5,2 s |
| 17.7 | [e2-contour] | Un contour fermé irrégulier en tirets `--chalk` (une forme de haricot) posé sur la carte ; compteur « FLUX » à 0. Ce compteur est permis : la carte est un vrai champ du plan, pas une coupe. Quadrature de la section 0 ; 0 sur toutes les images fixes, jamais « −0 ». | Le contour se déforme et se déplace en continu ; le compteur reste à 0. | 4,4 s |
| 17.8 | [e2-office] | Le pictogramme du test (sphère en coupe et coche) et le pictogramme 3 côte à côte, sous la colonne ; une flèche au `Kit.pen` du premier vers le second. | Flèche de 0,6 s. | 6,4 s |

### ep02.18 · `18_limite.html` · P23 · 21 s

Colonne à droite, deux lignes ; carte à gauche.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 18.1 | [e2-attention] | La carte de a de la scène 17, à gauche, à 60 %. Dans la colonne, deux emplacements l'un sous l'autre. | Fondu. | 3,2 s |
| 18.2 | [e2-garantit] | Première ligne : $\nabla\cdot\mathbf{B} = 0$ et une coche. | Coche au `Kit.pen`. | 2 s |
| 18.3 | [e2-ressemble] | Seconde ligne : un emplacement vide, cadre en tirets `--muted`, et un point d'interrogation `--chalk`. Aucune image de champ réel n'y est dessinée. | Le point d'interrogation s'allume. | 4,4 s |
| 18.4 | [e2-hasard] | La carte des cellules est remplacée par une carte de a **prise au hasard** : somme de 16 modes de Fourier à nombres d'onde entiers, 1 ≤ \|k\| ≤ 4, graine nommée « ep02-hasard », figée ; lignes de niveau et flèches `--b`. Le contour haricot y repasse, compteur « FLUX » à 0. La coche reste ; le point d'interrogation reste. | Fondu croisé de 1 s ; contour en mouvement. | 6 s |
| 18.5 | [e2-juger] | Le contour et son compteur s'effacent ; le point d'interrogation pulse une fois ; tout baisse à 40 % à la fin. | — | 5,2 s |

### ep02.19 · `19_fundiff.html` · P24 · 25 s

**Badge SCHEMATIC pour toute la scène**, de 19.1 à 19.5. Carte agitée à gauche (640 × 640 px, x 176 à 816, y 96 à 736). Sa fonction de courant est une somme de 24 modes de Fourier à **nombres d'onde entiers** (k_x, k_y), 2 ≤ \|k\| ≤ 6, sur [0, 2π]², amplitudes et phases fixées par une graine nommée dans le code, différente de celle de la scène 18 ; elle est **figée** pendant toute la scène. C'est une **illustration fabriquée pour le film, ni figure de l'article ni sortie de FunDiff**. La carte de gauche est une **carte de vitesse** : fond `--bg`, lignes de courant `--u` (lignes de niveau de ψ), flèches `--u` clairsemées à 50 %, traceurs `--u`. Encart à droite (480 × 480 px, x 1184 à 1664, y 160 à 640).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 19.1 | [e2-chercheurs] | Dans l'encart de droite, la carte des cellules de la scène 16, réduite, lignes et traceurs. Badge SCHEMATIC en haut à droite. | Fondu ; le badge se découvre. | 2,8 s |
| 19.2 | [e2-agites] | À gauche, la carte de vitesse agitée : lignes de courant, flèches clairsemées, traceurs. Chip `schematic` en haut à gauche de la carte, `maxWidth` 600 : « ILLUSTRATION DU FILM · PAS UNE SORTIE DE FUNDIFF ». Bandeau (`Kit.lowerThird` kind `reference`), **sous la carte de vitesse**, dans la zone x 96 à 996, y ≈ 780 à 880, l2 seul : « Idée utilisée par Wang et al., FunDiff, Nature Communications, 2026 ». | Ouverture de la carte en 1 s ; lignes en 1,5 s ; chip et bandeau en fondu, maintenus jusqu'à la fin de la scène. | 6,8 s |
| 19.3 | [e2-dessine] | Dans l'encart, la carte des cellules est remplacée par la carte de ψ de l'écoulement agité (`Kit.cmap('u')`, étiquette « ψ »), avec un chip `schematic` « ILLUSTRATION ». Une flèche au `Kit.pen` va de l'encart vers la carte de vitesse, étiquetée $\nabla^\perp$. | Fondu croisé de 0,8 s ; flèche de 0,6 s. | 4,8 s |
| 19.4 | [e2-jamais] | Calque de formule : $\mathbf{u} = \nabla^\perp\psi \;\Rightarrow\; \nabla\cdot\mathbf{u} = 0$. | Fondu du calque. | 4,4 s |
| 19.5 | [e2-vitesses] | Le $\mathbf{u}$ du calque souligné au `Kit.pen`, en `--u`. Les traceurs continuent, seuls à bouger. | Trait de 0,4 s ; maintien. | 6 s |

La légende FunDiff ne s'affiche que dans cette scène, sous la carte de vitesse. **Aucune carte de B n'est à l'écran pendant toute la scène.** Sur les cartes : aucun chiffre (ni compteur, ni barre graduée, ni valeur), ni « Kolmogorov », ni « Re », ni violet `--model`, ni chip `generated`, ni cadre violet (`generated: false`).

### ep02.20 · `20_cloture.html` · P25, P26 · 43 s

Les trois pictogrammes de la scène 01 en colonne à gauche ; chacun reçoit sa formule en face.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 20.1 | [e2-retenir] | Les trois pictogrammes, en colonne à gauche. | Apparition échelonnée. | 1,2 s |
| 20.2 | [e2-r1] | En face du pictogramme 1 : $\int_\Omega \nabla\cdot\mathbf{u}\,\mathrm{d}\mathbf{x} = \oint_{\partial\Omega}\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}\ell$. | Écriture ; le contour du pictogramme s'allume. | 4,4 s |
| 20.3 | [e2-r2] | En face du pictogramme 2 : $\nabla\cdot\mathbf{B} = 0$. | Écriture ; la ligne `--b` du pictogramme traverse la sphère. | 4,8 s |
| 20.4 | [e2-r2b] | À côté du pictogramme 2, une petite ligne `--b` fermée qui traverse un aimant miniature, parcourue par un point ; et le pictogramme barré du monopôle (scène 08), en petit. | Point en boucle continue. | 5,6 s |
| 20.5 | [e2-r3] puis [e2-r3b] | En face du pictogramme 3 : $\mathbf{u} = \nabla^\perp\psi,\ \ \nabla\cdot\mathbf{u} = 0$. | Écriture ; la flèche du pictogramme rejoue son quart de tour horaire. | 7,2 s |
| 20.6 | [e2-voie] | Les trois lignes baissent à 40 %. `Kit.projector` à droite, plan étiqueté « CHAMPS SANS DIVERGENCE », champ `--u`. | Entrée de 0,5 s. | 4 s |
| 20.7 | [e2-retirer] | La flèche se projette sur le plan ; la part retirée, en tirets `--muted`, reste un instant. | `drop` au début du plan. | 5,2 s |
| 20.8 | [e2-projection] | Le projecteur reste. | Maintien. | 2 s |
| 20.9 | [e2-chapitre6] | Chip `plain` sous le projecteur : « MODULE 1 · #CH6 ». | — | 2,8 s |
| 20.10 | [e2-crayon] | Carte d'exercices, à droite, à la place du projecteur : « EXERCICES » en mono, puis 1 c · 6 · 7 a · 9 a, c ; dessous, l'ancre « #exercices » en `--muted`. | Lignes en cascade. | 2 s |
| 20.11 | [e2-exos] | Les trois pictogrammes et la carte d'exercices restent seuls. | Maintien, puis fondu au noir de 1 s en fin de scène (3 s de pause conseillée). | 4 s |

## 3. Contraintes physiques : où elles portent

| Contrainte | Plans |
|---|---|
| Une seule flèche par côté, jamais retournée ; « + » du côté où elle sort, « − » du côté où elle entre | 2.4 à 2.12, 4.3 à 4.5 |
| Découpage exact de Ω : carreaux du bord découpés par la courbe, côtés non partagés = $\partial\Omega$ | 2.3 à 2.12, 3.x, 4.x |
| L'erreur par carreau est bien plus petite que son aire, calculée et non dessinée à la main (divergence prise au coin) | 3.4 à 3.7 |
| Carreaux parcourus dans le sens trigonométrique ; bord parcouru en gardant la région à sa gauche | 4.2 à 4.9, 5.5 |
| Anneau : grand cercle dans le sens trigonométrique, petit dans le sens horaire ; centre hors de tout carreau | 5.3 à 5.8 |
| Aucun cercle ne rétrécit sur le centre du tourbillon ; cercles apparus du petit au grand | 5.2, 5.10, 10.5 |
| Vorticité nulle dans l'anneau, valeurs 2π symboliques | 5.7, 5.10, 10.5, 10.6 |
| Aimant étendu, jamais de dipôle ponctuel ; Biot–Savart régularisé ; lignes = lignes de niveau de r·A_φ, aucune graine sur l'axe | 7.x, 11.x, 12.x |
| Les lignes de l'aimant le traversent de part en part, du sud vers le nord à l'intérieur | 7.10, 11.2, 11.6 |
| Cercles en tirets des cartes = sphères en coupe ; aucun compteur 2D, seulement 4π et 0, symboliques | 9.x, 10.x, 11.8, 12.x |
| Flèches de la charge : même longueur sur une même sphère, plus courtes sur les plus grandes, rapports exacts 1, 1/4, 1/9 ; mention des unités | 9.6 à 9.8 |
| Sphère déplacée : petite calotte d'entrée à flèches fortes, grande calotte de sortie à flèches faibles, valeur 0 | 10.4 |
| Couleur neutre des deux cartes jusqu'au verdict | 12.1 à 12.4 |
| Gradient perpendiculaire aux lignes de niveau, plus long où elles se serrent, rapports exacts | 13.8 à 13.14 |
| Quart de tour dans le sens horaire ; grandes valeurs de ψ à gauche du courant ; bosses dans le sens trigonométrique | 1.10, 14.1 à 14.5, 16.7, 16.8, 17.5, 20.5 ; axe y vers le haut (section 0) |
| Les droites x = kπ et y = kπ séparent les cellules | 16.9 |
| La carte de a est celle des cellules ; lignes de niveau de a = lignes de B ; compteur FLUX permis car vrai champ du plan | 17.3 à 17.7, 18.4 |
| La recette ne promet pas la ressemblance : aucune image de « vrai champ » dessinée | 18.3 à 18.5 |
| Légende FunDiff sur la carte de vitesse seulement, aucune carte de B dans la scène ; illustration, aucun chiffre, badge SCHEMATIC | 19.1 à 19.5 ; jamais en 17.x, 18.x |

## 4. Points signalés à la narration (non modifiée)

1. **P2, ligne « écran ».** Les trois lignes « du petit au grand », « du plan à l'espace », « construire » reprennent la voix. Remplacées par trois pictogrammes numérotés (1.7 à 1.10), qui reviennent à la clôture avec leurs formules (20.1 à 20.5).
2. **P25, [e2-r3] puis [e2-r3b].** « tournées d'un quart de tour » sans « dans le sens horaire », contraire à la bible (section 1 : jamais « d'un quart de tour » seul). À corriger par le scénariste ; l'image, elle, rejoue le quart de tour horaire (20.5).
3. **P5 et P6, lignes « écran ».** « Green-Ostrogradski : somme des divergences × aire = flux à travers le bord » et son pendant pour Stokes répètent [e2-enonce] et [e2-stokes4]. Remplacés par la somme Σ qui devient l'intégrale (3.8, 4.6), avec le nom du théorème en étiquette.
4. **P7, ligne « écran ».** « vorticité nulle dans l'anneau » répète [e2-anneaunulle]. Remplacé par « ω = 0 » posé dans l'anneau et $\int_\Omega \omega\,\mathrm{d}\mathbf{x} = 0$ (5.7).
5. **P9, ligne « écran ».** « divergence du champ magnétique » et « loi admise » répètent la voix : remplacés par l'accolade « lim flux ÷ volume » (7.4), comme l'ancien 13.6 ; rien n'est écrit pour « admise ». « flux nul à travers n'importe quelle surface fermée » devient la formule $\oint_{\partial\Omega}\mathbf{B}\cdot\mathbf{n}\,\mathrm{d}S = 0$ pour tout Ω (7.6). Le mot « ligne de champ » reste, comme étiquette de la courbe dessinée (7.8).
6. **P14, ligne « écran ».** « laquelle peut être magnétique ? » répète [e2-deuxcartes]. Remplacé par une carte de réponse compacte sans question, options « GAUCHE » / « DROITE » (12.1), qui s'allume au verdict.
7. **P22, ligne « écran ».** « dans le plan » répète [e2-dansplan]. Remplacé par le ballon qui s'aplatit sur un plan (17.1).
8. **P1, ligne « écran ».** « pourquoi ? » répète [e2-question]. Seul le point d'interrogation de ep01 est repris (1.4).
9. **P11, ligne « écran ».** Le panneau de gauche de `fig-monopole-dipole.png` est redessiné dans le thème, même géométrie, au lieu d'incruster la figure blanche (qui obligerait au registre PAPER).
10. **Continuité avec ep01.** La ligne « écran » de ep01 P6 parle de parts « vertes » et « rouges » ; le thème n'a ni vert ni rouge pour cela. ep02 marque les signes par « + » `--chalk` et « − » `--muted`, comme l'ancien storyboard : à aligner quand le storyboard de ep01 sera écrit.

## 5. Écarts proposés

Rien de ceci n'est appliqué ni validé par l'auteur : à accepter ou refuser. Reprise, en une liste, des écarts de l'ancien storyboard qui servent encore, et de ceux qu'ajoute ep02. L'ancien point 1, la roue à aubes, ne sert pas dans ep02 et n'est pas repris.

1. **Composant « compteur » (`Kit.readout`).** `Kit.chip` affiche un texte fixe ; il faut une valeur recalculée à chaque image, en chiffres tabulaires (`.tnum`), avec un libellé mono, une position qui suit un objet, une **virgule décimale** (`Kit.fmt` écrit un point) et la normalisation du zéro signé (jamais « −0 »). Raison : motif de la bible ; scènes 01, 16, 17, 18.
2. **Composant « cercle-sonde » (`Kit.probe`).** Cercle ou contour fermé quelconque en tirets `--chalk`, donné par une paramétrisation γ(s), avec ses parts de flèches normales ou tangentes, et la quadrature sur 256 points (élément d'arc, normale extérieure, parcours trigonométrique), divisée ou non par l'aire, qui alimente le compteur. Raison : le compteur doit afficher une valeur calculée ; scènes 01, 16, 17, 18.
3. **Composant « lignes de niveau » (`Kit.contours`).** Marching squares sur une grille scalaire, tracé progressif, niveaux donnés en liste ou par des points graines, pointes de flèche facultatives dans le sens de ∇⊥ψ, traceur à vitesse d'arc réglable sur une ligne fermée. Raison : scènes 11 (r·A_φ), 13 à 19 ; ψ et a reviendront dans les épisodes suivants.
4. **Options de `Kit.arrows` : `compress`, `hole`, `points`.** `compress: {k, threshold}` : L(I) = k·I sous le seuil, k·I_s·(2 − I_s/I) au-dessus, strictement croissante, sans plafond dur ; `hole` : disque vide autour d'un point ; `points` : flèches en des points donnés (bords de carreaux, sphères, flancs de colline) au lieu d'une grille. Aujourd'hui la longueur est normalisée par le maximum de la grille, ce qui rend la charge et le tourbillon illisibles. Raison : scènes 02 à 05, 07, 09 à 13.
5. **Couleur `--fg-2` pour le champ de la charge et pour les deux cartes de la question.** Le thème n'a pas de couleur clé pour le champ électrique ; colorer l'aimant en `--b` pendant la question donnerait la réponse. Pas de nouvelle couleur, un rôle nouveau pour un jeton existant. Raison : scènes 09, 10, 12.
6. **Dessins en perspective et relief : sphère, ballon, calottes et cône tangent, cubes, plan incliné, carte inclinée, relief en fil de fer.** Pas de composant ; code de scène en SVG ou canvas 2D (ellipses, dégradé radial, isométrie, cubes peints du fond vers l'avant, transformation affine du dessin 2D, pas de 3D CSS). À factoriser dans `motifs.js` si un épisode suivant les reprend. Raison : scènes 06 à 13, 16, 17.
7. **Marqueurs de parcours : flèche de parcours d'un carreau ou d'un cercle, chevron et marqueur « région à gauche ».** Nouveaux, en code de scène ; même dessin partout, à factoriser avec le point 6. Raison : la convention de sens du bord doit se lire sans texte ; scènes 04 et 05.
8. **Libellés français des composants.** `Kit.projector` : `planeLabel` « champs sans divergence » ; `Kit.predictCard` : kicker « TA RÉPONSE » au lieu de « PREDICT » par défaut, options « GAUCHE » et « DROITE ». Pas un écart si le moteur accepte ces options telles quelles ; à noter pour le constructeur. Raison : scènes 12 et 20.
