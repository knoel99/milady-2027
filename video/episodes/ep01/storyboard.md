# Épisode 01 : storyboard

Narration : `video/episodes/ep01/narration.md`, validée (1 805 mots annoncés, 1 801 comptés ici). Traitement : `video/episodes/ep01/traitement.md`. Bible : `video/continuite.md`. Retours : `video/episodes/ep01/retours.md` (enchaîner, trancher soi-même les points mineurs). Base : l'ancien storyboard relu, `video/episodes/ep01/avant-decoupage/storyboard.md` ; ses plans et ses champs corrigés sont repris, la colonne « Reprend » de la section 1 dit d'où vient chaque scène.

16 scènes, de 24 à 67 s, durée totale estimée à 12 min 00 s à 150 mots par minute, sans compter les pauses `hold_after` du script.

## 0. Conventions communes à toutes les scènes

**Repères.** Chaque plan commence sur le repère entre crochets de la narration, qui sert de nom de cue au moteur. Les durées sont estimées à 0,4 s par mot ; le moteur les recale sur la voix. Un plan dure jusqu'au repère du plan suivant.

**Registre.** NIGHT pour tout l'épisode (fond `--bg`). Pas de PAPER : aucune page du site n'est citée à l'écran.

**Coordonnées.** Tous les champs se calculent analytiquement dans la page, en coordonnées mathématiques, **y vers le haut**. Chaque scène définit une fonction `toPx(x, y)` qui renverse l'axe vertical pour l'écran. C'est une condition des contraintes de sens : sans ce renversement, la cellule en bas à gauche de l'écoulement cellulaire tournerait dans le sens horaire à l'écran, et le cisaillement irait à gauche en haut. Le constructeur le vérifie sur une image fixe de la scène 01 (cellule en bas à gauche, 0 < x, y < π, sens trigonométrique) et de la scène 11 (flèches vers la droite en haut). Les déplacements donnés en px sont, eux aussi, comptés y vers le haut.

**Notations.** La lettre grecque majuscule du domaine n'apparaît nulle part dans ep01 : `docs/specs/notations.md` et ep02 la réservent au domaine. On note α l'angle de l'aube marquée de la roue, ou du rayon marqué du disque, compté positivement dans le sens trigonométrique, et $\dot\alpha$ sa vitesse de rotation : $\dot\alpha_{\text{roue}}$ pour la roue à aubes, $\dot\alpha_{\text{disque}}$ pour le disque de la rotation solide. α se définit sans mot, sur le cadran de 10.11 : un arc entre un trait de référence fixe et l'aiguille. La vorticité s'écrit ω. Aucune fonction de courant, aucun ψ dans ep01 (bible, section 4).

**Couleurs.**

| Rôle | Jeton |
|---|---|
| Vitesse u, flèches, lignes de courant, traceurs, vorticité ω, eau des pictogrammes | `--u` ; point mis en avant (centre du tourbillon) en `--u-hi` ; carte scalaire : `Kit.cmap('u')` |
| Cercles en tirets, carré, roue à aubes, flèche de parcours, taches de fluide, pictogrammes des deux questions | `--chalk` |
| Annotations, étiquettes d'axes, part de flèche « qui ne compte pas », signe « − », cadran d'horloge | `--muted` |
| Robinet, table, évier, seringues, berges de la rivière | `--matter` ; bonde et piston en `--matter-dark` |

Pas de vert ni de rouge pour les parts entrantes et sortantes : `--param` est réservé aux paramètres de contrôle et le thème n'a pas de rouge. Les parts gardent la couleur `--u` ; un petit « + » `--chalk` marque ce qui sort, un « − » `--muted` ce qui entre (voir la section 4, point 3). **Seuil d'affichage des signes** : aucun « + » ni « − » sur une part plus courte que 2 px ; la part reste dessinée, sans signe.

**Zones.** Contenu dans le cadre sûr (x de 96 à 1824, y de 56 à 880) ; rien sous y = 880. Calque de formule (`Kit.formulaLayer`) en bas à droite pour les formules non dites (formule des cellules, rappel $\lvert\mathbf{u}\rvert = 1/r$). Les formules dont la voix dit le sens s'écrivent en grand avec `Kit.equation`, au moment où la voix le dit.

**Mouvement.** Tout est une fonction pure du temps : trajectoires des cercles paramétrées par t, rotation de la roue intégrée en forme fermée, transport des taches en forme fermée, traceurs par `Kit.tracers` (Scene.stepper).

**Compteurs.** Les flux et circulations affichés par un compteur se calculent dans la page, à chaque image, par quadrature sur 256 points du bord : somme des parts perpendiculaires (ou tangentes) pondérées par l'élément d'arc $\lvert\gamma'(s)\rvert\,\Delta s$, normale orientée vers l'extérieur, parcours dans le sens trigonométrique. Ils sont exacts à l'arrondi affiché, pas au-delà. L'affichage n'écrit jamais « −0 » : une valeur qui s'arrondit à zéro s'écrit « 0 ». Décimales à la virgule. Les valeurs 2π et 0 de la scène 13, sur les cercles qui entourent ou non le centre du tourbillon, sont symboliques : écrites, non calculées, posées sans chiffre qui défile. Un compteur est toujours attaché à un cercle visible.

**Longueur des flèches.** Direction exacte. Pour les champs bornés (cellules, source, rotation, cisaillement), la longueur est proportionnelle à l'intensité. Pour le tourbillon ponctuel (scènes 12 et 13), longueur donnée par une compression strictement croissante, linéaire sous un seuil I_s :

- L(I) = k·I si I ≤ I_s ;
- L(I) = k·I_s·(2 − I_s/I) si I > I_s.

La fonction est continue, de pente continue, et tend vers 2·k·I_s sans jamais l'atteindre : pas de plafond dur, « plus longue » veut toujours dire « plus forte ». Seuil I_s = 0,8 (unité 100 px) : au-dessus de 1/(R − a) ≈ 0,59 pour les deux flèches de bord de la roue (12.9), et au-dessus de 1/1,5 ≈ 0,67 pour les deux flèches comparées en 12.4. Un disque vide de 30 px entoure le centre.

**Texte à l'écran.** Aucune phrase de la voix n'est recopiée. L'écran porte des formules, des valeurs de compteur, des pictogrammes et des étiquettes d'une ou deux unités. Seuls quatre termes, demandés par les lignes « écran » de la narration, s'écrivent comme mots : CHAMP VECTORIEL, FLUX, CIRCULATION, LIGNE DE COURANT ; ils s'écrivent en mono capitales par `Kit.upper`, comme des fiches de vocabulaire, au moment où le terme est défini. Libellés des compteurs : FLUX ÷ AIRE, CIRCULATION ÷ AIRE, VORTICITÉ, CIRCULATION. Les lettres grecques gardent leur casse.

**Badge d'honnêteté.** Aucun : l'épisode ne cite aucun résultat mesuré et ne montre aucune sortie de modèle. Si le moteur exige un badge pour chaque scène, SCHEMATIC partout.

**Motifs.** Le petit cercle en tirets est le même objet d'un bout à l'autre : tiret 12 px plein, 9 px vide, épaisseur 3 px, `--chalk`. Le compteur est toujours à droite du cercle ou sous le panneau, en chiffres tabulaires (`.tnum`). Les deux pictogrammes des questions, posés à l'ouverture, reviennent aux scènes 09, 15 et 16 : **pictogramme « sort »**, un cercle en tirets de 90 px traversé par quatre flèches `--u` vers l'extérieur ; **pictogramme « tourne »**, le même cercle avec une flèche de parcours `--chalk` en arc, sens trigonométrique. La roue à aubes : quatre aubes `--chalk`, un moyeu, une aube marquée en `--fg`.

**Écoulement cellulaire.** $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$ sur [0, 2π] × [0, 2π], 2 × 2 cellules, panneau carré de 780 px (124 px par unité). Mêmes réglages aux scènes 01, 14 et 15. La cellule en bas à gauche tourne dans le sens trigonométrique, ses voisines dans le sens horaire ; les droites x = π et y = π les séparent. La formule ne s'affiche qu'au calque de formule, à partir de [e1-coin], jamais dite.

## 1. Découpage en scènes

| Scène | Fichier | Paragraphes | Mots | Durée | Composants | Reprend |
|---|---|---|---|---|---|---|
| ep01.01 | `01_ouverture.html` | P1, P2 | 90 | 36 s | `Kit.arrows`, `Kit.tracers`, `Kit.pen`, pictogrammes, cercle-sonde | 6.6 (cellules) ; 1.6 (carte vide à juger) |
| ep01.02 | `02_vocabulaire.html` | P3, P4 | 100 | 40 s | `Kit.arrows`, `Kit.plot`, `Kit.equation` | 2.1, 2.2, 2.4 à 2.6 |
| ep01.03 | `03_flux.html` | P5, P6 | 142 | 57 s | `Kit.arrows`, `Kit.tracers`, cercle-sonde, `Kit.equation`, pictogrammes robinet | 3.1 à 3.7 |
| ep01.04 | `04_divergence.html` | P7 | 90 | 36 s | `Kit.arrows`, cercle-sonde, `Kit.equation`, pictogrammes évier | 3.8 à 3.12 |
| ep01.05 | `05_carre.html` | P8, P9 | 167 | 67 s | SVG, `Kit.equation`, `Kit.morph` | 4.1 à 4.7 |
| ep01.06 | `06_source_rotation.html` | P10, P11 | 123 | 49 s | `Kit.arrows` ×2, `Kit.plot` ×2, `Kit.equation`, `Kit.tracers` | 5.1 à 5.5 |
| ep01.07 | `07_cercle_promene.html` | P12, P13 | 128 | 51 s | `Kit.arrows` ×2, cercle-sonde ×2, compteur ×2, `Kit.fieldMap` | 5.6 à 5.11, 6.1, 6.2 |
| ep01.08 | `08_incompressible.html` | P14 | 70 | 28 s | `Kit.arrows`, taches transportées, jauge, dessins en perspective, pictogrammes | 6.3 à 6.5 (champ changé) |
| ep01.09 | `09_circulation.html` | P15, P16 | 152 | 61 s | `Kit.arrows`, cercle-sonde, `Kit.equation`, `Kit.morph`, `Kit.pen` | 7.1 à 7.6 |
| ep01.10 | `10_rotationnel_roue.html` | P17, P18 | 141 | 56 s | SVG en perspective, roue à aubes, `Kit.arrows`, `Kit.tracers`, cadrans, compteur, `Kit.equation` | 7.7, 7.8, 8.1 à 8.6 |
| ep01.11 | `11_cisaillement.html` | P19, P20 | 128 | 51 s | `Kit.arrows`, `Kit.tracers`, `Kit.fieldLines`, roue à aubes, cercle-sonde, compteur, `Kit.equation` | 9.1 à 9.5 |
| ep01.12 | `12_tourbillon.html` | P21, P22 | 145 | 58 s | `Kit.arrows` (compression), `Kit.fieldLines`, roue à aubes, cadran, `Kit.formulaLayer`, `Kit.chip` | 10.1 à 10.10 |
| ep01.13 | `13_tourbillon_centre.html` | P23 | 76 | 30 s | `Kit.arrows` (compression), cercles-sondes, compteurs, `Kit.equation` | 10.11 à 10.14 |
| ep01.14 | `14_cellules_limite.html` | P24 | 100 | 40 s | `Kit.arrows`, `Kit.streamlines`, `Kit.tracers`, cercle-sonde, compteur, `Kit.plot`, `Kit.formulaLayer` | 11.1 à 11.5 |
| ep01.15 | `15_enigme.html` | P25 | 60 | 24 s | `Kit.arrows`, `Kit.tracers`, cercles-sondes, compteurs, `Kit.formulaLayer` | 6.7 à 6.9 |
| ep01.16 | `16_cloture.html` | P26, P27 | 89 | 36 s | pictogrammes, vignettes animées, roue à aubes, `Kit.equation`, `Kit.chip` | 19.1 à 19.3, 19.7, 19.8 |
| **Total** | | P1 à P27 | 1 801 | **12 min 00 s** | | |

« Cercle-sonde », « compteur » et « roue à aubes » sont des composants proposés (section 5). Tant qu'ils ne sont pas acceptés, ils s'écrivent en code de scène, avec la même apparence partout.

## 2. Plans

### ep01.01 · `01_ouverture.html` · P1, P2 · 36 s

Écoulement cellulaire (section 0), panneau carré de 780 px centré (x 570 à 1350, y 78 à 858), cadre `--matter`, sans titre ni formule. Flèches `--u` sur une grille 13 × 13, longueur proportionnelle à l'intensité. Point de travail C = (1,4 ; 1,8), dans la cellule en bas à gauche, qui reviendra à la scène 14.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 1.1 | [e1-carte] | Le panneau, puis ses flèches. | Les flèches poussent depuis leur pied (`Kit.arrows`, entrée 0,5 s), en balayage de gauche à droite. | 2,4 s |
| 1.2 | [e1-fleche] | Zoom à 2,5× sur la flèche du nœud (π/2 ; 2π/3) de la grille (pas π/6), cerclée au `Kit.pen` (circle) ; un point `--chalk` à son pied. Elle pointe vers la gauche, longueur 0,5. Le cadrage du zoom contient aussi le nœud (π/2 ; π). | Zoom caméra de 0,8 s vers la flèche, maintien. | 4 s |
| 1.3 | [e1-longueur] | Toujours zoomé : la flèche du nœud (π/2 ; π), sur la même colonne, s'allume. Toutes deux pointent vers la gauche ; longueurs 0,5 et 1 (sur x = π/2, u = (cos y, 0)). Les deux sont cerclées. | Pulsation alternée des deux flèches ; retour au plan large à la fin du plan. | 3,6 s |
| 1.4 | [e1-question] | Plan large. Un point `--chalk` en (2,2 ; 1,0) ; un point d'interrogation `--chalk` de 80 px à côté. Des traceurs `--u` à 40 % (300 particules) se mettent à suivre les flèches. | Le point pulse une fois ; les traceurs démarrent. | 3,2 s |
| 1.5 | [e1-deux] | La carte glisse à gauche et se réduit à 70 % ; à droite, deux emplacements vides, cadres en tirets `--muted`, l'un sous l'autre. | Glissement de 0,8 s. | 3,6 s |
| 1.6 | [e1-sort] | Premier emplacement : pictogramme « sort » (section 0). | Les quatre flèches poussent vers l'extérieur en 0,6 s. | 1,6 s |
| 1.7 | [e1-tourne] | Second emplacement : pictogramme « tourne ». | La flèche de parcours fait un tour, sens trigonométrique, en 1 s. | 1,6 s |
| 1.8 | [e1-outil] | Les deux cercles des pictogrammes se détachent, se fondent en un seul petit cercle en tirets qui vient se poser sur la carte, centré sur C, rayon 0,6 unité (74 px). La carte reprend 100 %. Aucun compteur. | Vol courbe de 1 s, puis le cercle se pose. | 4,8 s |
| 1.9 | [e1-machine] | La carte se réduit à 40 % et glisse en haut à gauche, où elle reste en vignette avec son cercle. Au centre, une deuxième carte, vide, de même taille, cadre en tirets `--muted` : la place d'une carte dessinée plus tard. | Réduction de 0,8 s ; la carte vide s'ouvre par un fondu. Pas de violet `--model` : la machine n'est pas présentée. | 4,4 s |
| 1.10 | [e1-juger] | Sous la carte vide, un seul emplacement de verdict, vide : un filet horizontal plein `--muted` de 160 px, comme une ligne de signature, sans cadre ni tirets, pour ne pas ressembler aux cadres en tirets de 1.5. | Le filet se trace de gauche à droite en 0,5 s ; rien ne s'y inscrit. | 4 s |
| 1.11 | [e1-lire] | La carte vide et l'emplacement de verdict s'effacent ; la vignette revient au centre, à 100 %, avec son cercle. | Retour de 0,8 s, maintien. | 2,8 s |

### ep01.02 · `02_vocabulaire.html` · P3, P4 · 40 s

Grand panneau de 1100 × 720 px à gauche (x 120 à 1220, y 120 à 840). Champ de démonstration lisse et sans symétrie, repris de l'ancien storyboard : $\mathbf{u} = (0{,}6 + 0{,}4\sin(x + 0{,}5y),\ 0{,}3\cos x)$, flèches `--u` sur une grille 13 × 9. Sa composante $u_x$ dépend de x et de y : les deux graphes de 2.8 et 2.10 ne sont pas plats. Colonne de droite (x 1300 à 1800) : trois fiches de vocabulaire, vides au départ, qui se remplissent au fil de la scène.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 2.1 | [e1-mots] | Panneau vide, cadre `--matter`. À droite, trois fiches vides empilées (filets `--muted` en tirets). | Fondu d'entrée ; les fiches apparaissent l'une après l'autre. | 2 s |
| 2.2 | [e1-champ] | Les flèches apparaissent. Fiche 1 : « CHAMP VECTORIEL », et en dessous un petit $\mathbf{u}$. | Entrée échelonnée par colonnes en 3 s (`Kit.arrows`). | 5,2 s |
| 2.3 | [e1-composantes] | Les flèches baissent à 30 %. Une flèche agrandie à droite du panneau, sur deux axes `--muted`. | La flèche grandit depuis sa place sur la grille en 0,6 s. | 2,8 s |
| 2.4 | [e1-horizontale] | Sa part horizontale en tirets `--u`, étiquette $u_x$. | Projection en 0,5 s. | 4,8 s |
| 2.5 | [e1-verticale] | Sa part verticale en tirets `--u`, étiquette $u_y$. Fiche 2 : $\mathbf{u} = (u_x, u_y)$. | Projection en 0,5 s ; la fiche s'écrit. | 4,4 s |
| 2.6 | [e1-change] | La flèche agrandie rejoint la grille. Un point `--chalk` se pose sur le panneau ; à côté de lui, une barre horizontale `--u` montre $u_x$ en ce point. | Le point se déplace un peu ; la barre change de longueur avec lui. | 4,4 s |
| 2.7 | [e1-avance] | Une droite horizontale `--chalk` en y = 1, étiquette $y = 1$ en `--muted` au bout. Le point glisse le long de la droite, sa barre $u_x$ suit. | Glissement de gauche à droite en 4 s ; le point ne quitte pas la droite. | 4,8 s |
| 2.8 | [e1-taux] | Au-dessus du panneau, petit graphe (`Kit.plot`) de $u_x(x, 1) = 0{,}6 + 0{,}4\sin(x + 0{,}5)$ en fonction de x, une ondulation. Au point courant, un petit triangle de pente `--chalk` : un pas horizontal de 1 et la montée correspondante de la tangente. | Le point glisse ; le triangle suit et change d'inclinaison. | 4,4 s |
| 2.9 | [e1-derivee] | Sous le graphe, $\partial_x u_x$, une accolade `--muted` sous le triangle de pente. Fiche 3 : $\partial_x u_x$. | `Kit.equation`, révélation en 0,45 s. | 2,4 s |
| 2.10 | [e1-monte] | La droite horizontale s'efface ; une droite verticale `--chalk` en x = 1, étiquette $x = 1$. Le point monte le long d'elle ; second petit graphe de $u_x(1, y) = 0{,}6 + 0{,}4\sin(1 + 0{,}5y)$ en fonction de y, avec son triangle de pente. Fiche 3 complétée : $\partial_x u_x$, $\partial_y u_x$. | Montée en 3 s ; le terme $\partial_y u_x$ s'écrit à la fin. | 4,8 s |

### ep01.03 · `03_flux.html` · P5, P6 · 57 s

Champ repris de l'ancien storyboard : $\mathbf{u} = (x - 0{,}4y,\ y + 0{,}4x)$, flèches `--u`. Il sort et tourne un peu : chaque flèche du bord a une part perpendiculaire et une part le long du bord. Panneau de 900 × 720 px à gauche (x 120 à 1020, y 100 à 820) ; colonne d'équation à droite, x 1180 à 1780. Le point P est l'origine du champ, où u = 0, à l'écran en (620, 340).

Calcul du plan 3.12, repris tel quel. Pour un cercle de centre c et de rayon R, la part perpendiculaire vaut, au point de normale n, n·(A c) + R, où A est la matrice du champ ; elle entre là où n·(A c) < −R. Comme |A c| = 1,077 |c|, il faut |c| > R/1,077 ≈ 167 px pour R = 180 px. Avec c = (−212, −212) px, soit 300 px vers le bas à gauche, l'arc entrant fait environ 112°, du côté qui fait face à P, soit 5 des 16 points si le premier point est à 0°. Le cercle déplacé est centré à l'écran en (408, 552) : x 228 à 588, y 372 à 732, flèches comprises au plus x 148 et y 812, dans le panneau.

Pictogrammes du robinet (3.2 à 3.4), dans la colonne de droite, x 1180 à 1780, y 140 à 700, en code de scène SVG : table `--matter` vue de côté, robinet `--matter`, jet et nappe d'eau `--u`, petit œil `--muted` au-dessus de la table.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 3.1 | [e1-source] | Le champ ; le point P `--chalk` clignote une fois. | Pulsation de 0,4 s. | 3,2 s |
| 3.2 | [e1-robinet] | Le panneau baisse à 50 %. À droite, vue de côté : la table, le robinet au-dessus, le jet qui tombe. | Le jet descend en 0,6 s. | 4,4 s |
| 3.3 | [e1-ecarte] | La nappe d'eau s'étale sur la table, à gauche et à droite du jet ; petites flèches `--u` horizontales le long de la table, qui partent du pied du jet. | Étalement en 1,2 s ; les flèches poussent vers l'extérieur. | 3,6 s |
| 3.4 | [e1-dessus] | L'œil `--muted` monte au-dessus de la table ; le dessin bascule en vue de dessus : la table devient un rectangle, le jet n'est plus qu'un petit disque en tirets `--muted`, vide, sans point ni croix (le jet tombe vers la table, en s'éloignant de l'œil), et les flèches de la nappe deviennent une gerbe radiale `--u` qui part de ce disque. Les flèches de la gerbe raccourcissent en s'éloignant du disque, en 1/r de la distance à son centre. | Bascule de 1 s par transformation affine (aplatissement vertical), comme un plan qu'on regarde d'en haut. | 4,8 s |
| 3.5 | [e1-cercle] | Le pictogramme se réduit en vignette dans le coin haut droit, où il reste jusqu'à la scène 04. Le panneau reprend 100 % ; cercle en tirets centré sur P, rayon 180 px. | Tracé au trait en 0,8 s. | 4 s |
| 3.6 | [e1-bord] | Les flèches de la grille baissent à 25 %. Une flèche posée sur le bord, à 40° au-dessus de l'horizontale. | La flèche pousse depuis son pied. | 4 s |
| 3.7 | [e1-coupe] | Deux contours en tirets fins `--muted` dessinent les deux morceaux de la flèche, l'un le long du rayon, l'autre tangent au cercle, avec un petit angle droit au pied. | Tracé de 0,5 s. | 2,4 s |
| 3.8 | [e1-traverse] | Le morceau perpendiculaire au bord passe en `--u` plein. | Il se détache de la flèche en 0,5 s ; petit va-et-vient de part et d'autre du bord. | 4,4 s |
| 3.9 | [e1-glisse] | Le morceau le long du bord passe en tirets `--muted`. | Il glisse un peu le long du cercle et revient. | 4 s |
| 3.10 | [e1-seul] | Le morceau tangent baisse à 40 % ; le morceau perpendiculaire pulse. | Pulsation de 0,4 s. | 3,6 s |
| 3.11 | [e1-plus] | Seize points répartis sur le bord (premier point à 0°), chacun avec sa part perpendiculaire seule ; centré sur P, toutes sortent ; un petit « + » `--chalk` au bout de chacune. | Les seize parts poussent en un tour, sens trigonométrique, en 1,5 s. | 4,4 s |
| 3.12 | [e1-moins] | Le cercle glisse de 300 px vers le bas à gauche (212 px à gauche, 212 px en bas) : cinq parts entrent, sur l'arc qui fait face à P, chacune marquée d'un « − » `--muted`. | Glissement de 1 s, parts recalculées à chaque image ; maintien de 1,6 s, puis retour sur P en 1 s. | 3,6 s |
| 3.13 | [e1-flux] | Un arc `--chalk` fait le tour du cercle et rassemble les seize parts ; à droite, fiche « FLUX ». | L'arc fait le tour en 1 s ; la fiche s'écrit au bout. | 4,4 s |
| 3.14 | [e1-sens] | Des traceurs `--u` (200 particules, 50 %) partent de l'intérieur du disque et traversent le bord ; chaque traversée fait un bref éclat `--chalk` sur le bord. | Traceurs continus jusqu'à la fin de la scène. | 6 s |

### ep01.04 · `04_divergence.html` · P7 · 36 s

Même champ, même panneau, même point P que la scène 03. Comme ce champ est linéaire et que sa divergence vaut 2 partout, le flux d'un cercle centré vaut exactement 2πR² : il double quand l'aire double. Colonne de droite : l'équation de la divergence, puis trois vignettes.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 4.1 | [e1-grand] | Deux cercles centrés sur P, rayons 90 et 180 px ; sous le panneau, deux barres horizontales `--u` (« FLUX » en `--muted` à gauche) dont les longueurs sont les flux calculés des deux cercles : la grande est quatre fois la petite. | Les cercles se tracent ; les barres poussent. | 4,8 s |
| 4.2 | [e1-aire] | Les deux disques se remplissent d'un voile `--chalk` à 12 % ; dans la colonne, $\dfrac{\text{flux}}{\pi r^2}$. Les deux barres sont divisées par l'aire de leur disque : elles deviennent égales. | Remplissage radial en 0,6 s ; les barres se recalent en 0,8 s. | 3,6 s |
| 4.3 | [e1-retrecir] | Le petit cercle s'efface ; le grand rétrécit vers P jusqu'à 20 px ; le terme $\lim_{r\to 0}$ s'ajoute devant. | Rayon de 180 à 20 px en 2,5 s (inOutCubic). | 3,6 s |
| 4.4 | [e1-divergence] | L'équation complète : $\nabla\cdot\mathbf{u}(P) = \lim_{r\to0} \dfrac{\text{flux}}{\pi r^2}$. | Le membre de gauche s'écrit. | 5,2 s |
| 4.5 | [e1-positive] | Sous l'équation, vignette 1 : la vignette du robinet vu de dessus (gerbe radiale, flèches en 1/r comme en 3.4), étiquette $\nabla\cdot\mathbf{u} > 0$ accrochée par un filet `--muted` au disque du jet, et à lui seul : hors du disque, une gerbe en 1/r ne diverge pas. | La vignette du coin descend à sa place ; les flèches repoussent. | 4,8 s |
| 4.6 | [e1-negative] | Vignette 2 à côté : quatre flèches qui arrivent sur un point, $\nabla\cdot\mathbf{u} < 0$ accrochée par un filet `--muted` à ce point. | Les flèches poussent vers le point. | 3,2 s |
| 4.7 | [e1-evier] | La vignette 2 s'agrandit au centre de la colonne : vue de côté d'un évier `--matter`, la bonde `--matter-dark` au fond ; l'eau `--u` glisse vers la bonde et descend par elle. | Agrandissement de 0,6 s ; filet d'eau continu. | 3,2 s |
| 4.8 | [e1-quitte] | Le petit œil `--muted` monte ; bascule en vue de dessus : la bonde devient un disque sombre, l'eau une gerbe de flèches qui convergent vers lui et s'arrêtent à son bord ; elles raccourcissent en s'éloignant du disque, en 1/r. L'étiquette $\nabla\cdot\mathbf{u} < 0$ se raccroche, par son filet `--muted`, au disque de la bonde. | Bascule de 1 s, comme en 3.4 ; la vignette reprend sa taille ; le filet glisse du point au disque. | 3,2 s |
| 4.9 | [e1-nulle] | Vignette 3 : un cercle en tirets traversé par des flèches parallèles de même longueur, qui entrent à gauche et ressortent à droite ; $\nabla\cdot\mathbf{u} = 0$. | Les flèches défilent lentement à travers le cercle. | 4,4 s |

### ep01.05 · `05_carre.html` · P8, P9 · 67 s

Repris de l'ancienne scène 04. Grand carré `--chalk` de 360 px, à gauche (centre x 560, y 470), centré sur l'origine du champ. Champ $\mathbf{u} = (0{,}5 + 0{,}6x,\ 0{,}4 + 0{,}5y)$ : $u_x$ croît vers la droite, $u_y$ croît vers le haut. **Échelle : 300 px par unité**, donc le côté vaut h = 1,2 < 1,6. Au milieu de chaque côté, la flèche garde le sens annoncé : $u_x$ = 0,14 à gauche (elle entre) et 0,86 à droite (elle sort) ; $u_y$ = 0,10 en bas (elle entre) et 0,70 en haut (elle sort). Au-delà de h = 1,6, la flèche du bas changerait de sens. Colonne d'équation à droite (x 1000 à 1780).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 5.1 | [e1-formule] | Le cercle en tirets se morphose en carré en tirets, même centre. | Morphose de 0,8 s. | 4,8 s |
| 5.2 | [e1-cotes] | Côtés gauche et droit en trait plein `--chalk` ; haut et bas à 30 %. | Les deux côtés s'épaississent. | 3,6 s |
| 5.3 | [e1-horiz] | Au milieu de chacun des deux côtés, la flèche entière du champ, coupée comme en scène 03 : sa part verticale, le long du côté, en tirets `--muted` ; sa part horizontale, qui traverse, en `--u` plein. | Coupe en 0,5 s ; les parts verticales baissent à 30 %. | 3,6 s |
| 5.4 | [e1-droit] | Flèche horizontale longue au milieu du côté droit, qui sort ; une accolade `--muted` le long du côté, étiquette $h$. Équation : $u_x(\text{droite})\times h$. | L'accolade se dessine, puis le terme. | 5,6 s |
| 5.5 | [e1-gauchepareil] | Flèche courte au milieu du côté gauche, qui entre (0,14 contre 0,86, même échelle). Équation : $u_x(\text{droite})\times h - u_x(\text{gauche})\times h$. | La flèche pousse ; le second terme s'écrit avec son signe moins. | 4,4 s |
| 5.6 | [e1-deuxpoints] | Les deux points de mesure, au milieu des côtés droit et gauche, marqués par deux points `--chalk` ; les arguments « droite » et « gauche » de l'équation s'allument. | Pulsation des deux points et des deux arguments, l'un après l'autre. | 5,6 s |
| 5.7 | [e1-separes] | Une accolade horizontale `--muted` entre les deux points, étiquette $h$, la même lettre que l'accolade du côté. | Tracé de 0,6 s. | 3,6 s |
| 5.8 | [e1-ecart] | Les deux flèches sortent du carré et se superposent au-dessus de lui, base contre base : leur différence est surlignée en `--chalk`. Équation regroupée : $\big[u_x(\text{droite}) - u_x(\text{gauche})\big]\times h$. | Glissement et superposition en 0,8 s ; l'écart s'allume ; `Kit.morph` de l'équation. | 6 s |
| 5.9 | [e1-divise] | Le carré se remplit d'un voile, étiquette $h \times h = h^2$ ; l'équation reçoit $\div\ h^2$. | Remplissage en 0,6 s. | 5,6 s |
| 5.10 | [e1-reste] | Un $h$ du haut et un $h$ du bas se barrent ; il reste $\dfrac{u_x(\text{droite}) - u_x(\text{gauche})}{h}$. À côté, un petit triangle de pente `--chalk`, le même que celui de la scène 02 : pas horizontal h, montée égale à l'écart. | Barres au `Kit.pen` (cross, petites), `Kit.morph` ; le triangle se dessine. | 4,8 s |
| 5.11 | [e1-dpdroite] | Le carré rétrécit et la fraction se change en $\partial_x u_x$. | `Kit.morph` de la fraction vers $\partial_x u_x$ pendant que le carré passe de 360 à 60 px (h de 1,2 à 0,2). | 3,6 s |
| 5.12 | [e1-hautbas] | Le carré reprend 360 px (h = 1,2) ; côtés haut et bas en plein ; flèche courte qui entre en bas, longue qui sort en haut ; les parts horizontales en tirets. Le geste se rejoue en accéléré. | Rejeu en 3 s. | 5,6 s |
| 5.13 | [e1-montee] | Le terme $\partial_y u_y$ s'écrit sous $\partial_x u_x$. | `Kit.morph` de la fraction haut-bas vers $\partial_y u_y$. | 3,2 s |
| 5.14 | [e1-somme] | $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, centrée en grand, les deux termes venus de leurs places. | `Kit.morph`. | 3,6 s |
| 5.15 | [e1-propre] | Dans chaque terme, les deux indices passent en `--chalk` et sont reliés par un petit trait vertical : $x$ avec $x$, $y$ avec $y$. | Les traits se dessinent au `Kit.pen` (arrow, sans pointe) ; maintien jusqu'à la fin de la scène. | 3,2 s |

### ep01.06 · `06_source_rotation.html` · P10, P11 · 49 s

Deux panneaux de 700 × 560 px côte à côte (x 140 à 840 et 1080 à 1780, y 200 à 760). Gauche : source $\mathbf{u} = (x, y)$. Droite : rotation $\mathbf{u} = (-y, x)$, sens trigonométrique. **Unité : 140 px.** Flèches `--u`, grille 11 × 9, longueur proportionnelle. L'origine de chaque champ est à 20 px à gauche et 40 px sous le centre du panneau, à l'écran en (470, 520) et (1410, 520), comme dans l'ancien storyboard. Au-dessus de chaque panneau (y 80 à 190), deux lignes : la formule du champ, puis sa divergence. Sous chaque panneau (y 776 à 870), une bande pour les deux dérivées. Dans chaque panneau, un médaillon de graphe (`Kit.plot`, 260 × 180 px, fond `--panel`) en haut à gauche, à l'écran x 150 à 410, y 210 à 390.

Lignes de marche, choisies pour ne pas croiser le médaillon : droite horizontale y = −1 (à l'écran y = 660), parcourue de x = −1,5 à x = 2 ; droite verticale x = 1,5 (à l'écran x = 680 et 1620), parcourue de y = −1,5 à y = 2. Valeurs : source, $u_x = x$ sur la droite horizontale (graphe de pente 1), $u_y = y$ sur la verticale (pente 1) ; rotation, $u_x = -y = 1$ sur la droite horizontale (graphe plat), $u_y = x = 1{,}5$ sur la verticale (graphe plat).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 6.1 | [e1-essai] | Les deux cadres vides ; au-dessus, rappel à 40 % de $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, centré, qui s'efface à la fin du plan. | Fondu. | 2,8 s |
| 6.2 | [e1-fuit] | Panneau gauche : flèches de la source ; au-dessus, $\mathbf{u} = (x, y)$. | Flèches qui poussent depuis l'origine vers l'extérieur ; traceurs `--u` à 30 % qui fuient l'origine. | 5,2 s |
| 6.3 | [e1-allonge] | Un rayon `--muted` part de l'origine ; les trois flèches posées sur lui, à 1, 2 et 3 unités, s'allument : longueurs 1, 2, 3. | Les trois flèches pulsent l'une après l'autre. | 4 s |
| 6.4 | [e1-srcdroite] | Les flèches baissent à 30 %. Droite horizontale `--chalk` y = −1 ; un point la parcourt avec sa flèche, dont la part horizontale est en `--u` plein, la part verticale en tirets `--muted`. Le médaillon trace $u_x$ en fonction de x : une droite de pente 1, avec un triangle de pente « 1 de côté, 1 de montée ». Dans la bande du bas : $\partial_x u_x = 1$. | Marche de 3 s ; la courbe du médaillon se trace avec le point ; la dérivée s'écrit à la fin. | 4,8 s |
| 6.5 | [e1-srchaut] | Même geste sur la droite verticale x = 1,5 : part verticale en plein ; le médaillon trace $u_y$ en fonction de y, pente 1. Bande du bas : $\partial_y u_y = 1$. | Marche de 2,5 s. | 3,6 s |
| 6.6 | [e1-un] | Les deux « = 1 » de la bande du bas s'allument ensemble. | Soulignés au `Kit.pen` (underline). | 2,4 s |
| 6.7 | [e1-vautdeux] | Sous la formule du champ : $\nabla\cdot\mathbf{u} = 1 + 1 = 2$, les deux « 1 » venus de la bande du bas. Les flèches reprennent 100 %. | `Kit.morph` des deux termes, puis « = 2 ». | 4 s |
| 6.8 | [e1-bloc] | Panneau droit : flèches de la rotation ; au-dessus, $\mathbf{u} = (-y, x)$. Traceurs `--u` à 30 ; un rayon marqué `--chalk` tourne avec eux, sans se courber. | Les flèches poussent ; rotation continue des traceurs et du rayon, 1 rad par seconde de scène. | 5,6 s |
| 6.9 | [e1-perp] | Sur un rayon `--muted`, trois flèches à 1, 2 et 3 unités s'allument, chacune avec un petit angle droit `--muted` à son pied. | Pulsation l'une après l'autre. | 4,8 s |
| 6.10 | [e1-rotdroite] | Même geste qu'en 6.4 sur la droite y = −1 : la part horizontale reste la même tout le long, vers la droite, longueur 1 ; la part verticale, en tirets, change. Médaillon : graphe plat. Bande : $\partial_x u_x = 0$. | Marche de 3 s. | 4 s |
| 6.11 | [e1-rothaut] | Même geste sur la droite x = 1,5 : la part verticale reste la même, vers le haut, longueur 1,5. Médaillon : graphe plat. Bande : $\partial_y u_y = 0$. | Marche de 2,5 s. | 3,6 s |
| 6.12 | [e1-vautzero] | $\nabla\cdot\mathbf{u} = 0 + 0 = 0$ sous la formule de la rotation. Les médaillons et les bandes s'effacent. | `Kit.morph` des deux termes. | 4,4 s |

### ep01.07 · `07_cercle_promene.html` · P12, P13 · 51 s

Les deux panneaux de la scène 06, mêmes origines, formules en haut. Un compteur sous chaque panneau, libellé « FLUX ÷ AIRE », dans la bande y 776 à 870.

Géométrie des cercles déplacés, reprise telle quelle. Rayon 130 px, centre final c = (200, 140) px depuis l'origine, à l'écran en (670, 380) et (1610, 380). Parts du bord à une échelle commune aux deux panneaux, la plus longue (gauche, dans la direction de c) dessinée à 30 px. Source : la part vaut n·c + R ; comme |c| ≈ 244 px > 130 px, environ 116° du bord, de 157° à 273° (angles comptés depuis l'horizontale vers la droite, sens trigonométrique), ont une part entrante, du côté de l'origine, et les sortantes sont plus longues. **Phase des seize points : 11,25°**, soit des points en 11,25° + k × 22,5°, dans les deux panneaux. À gauche, cinq parts entrantes franches, en 168,75°, 191,25°, 213,75°, 236,25° et 258,75° ; les plus courtes, aux deux bouts de l'arc, font environ 3 px, au-dessus du seuil de 2 px (section 0). Avec un premier point à 0°, le point de 157,5° tomberait à 0,3° de la frontière, avec une part quasi nulle. Rotation : la part vaut n·(−c_y, c_x), sans terme en R : moitié entrante, moitié sortante, symétriques. Avec la même phase, les points de 33,75° et 213,75° sont à 1,25° des frontières ; leurs parts, d'environ 0,4 px, restent sans signe : sept « − » et sept « + », symétriques. Cercle et flèches restent dans le panneau.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 7.1 | [e1-centre] | Cercle centré sur l'origine dans chaque panneau, rayon 130 px. Les flèches de la grille baissent à 30 %. | Tracé des deux cercles. | 2,4 s |
| 7.2 | [e1-sortent] | Gauche : seize flèches sur le bord, toutes perpendiculaires et vers l'extérieur, chacune avec son « + ». | Elles poussent en un tour. | 4,4 s |
| 7.3 | [e1-glissent] | Droite : seize flèches sur le bord, toutes tangentes, aucune part perpendiculaire. | Elles poussent ; léger défilement le long du bord, sens trigonométrique. | 4,4 s |
| 7.4 | [e1-deplace] | Les deux cercles se promènent en même temps, sur la trajectoire fermée et lisse c(τ) = (20 + 180 cos 2πτ, 110 + 30 cos 4πτ) px, τ de 0 à 1 : elle part de l'origine vers c = (200, 140), fait sa boucle et **s'arrête en c**, vitesse nulle à l'arrivée. Elle reste dans x de −160 à 200 px et y de 80 à 140 px. Les compteurs s'allument : 2 à gauche, 0 à droite. | Entrée de 0,4 s de l'origine vers c, puis boucle en 2,2 s (τ en inOutCubic) ; les seize flèches du bord sont recalculées à chaque image ; les compteurs ne bougent pas. | 2,8 s |
| 7.5 | [e1-entrent] | Cercles arrêtés en c. Les parts tangentes s'effacent ; seules les parts perpendiculaires restent. Les parts entrantes s'allument avec leur « − » : à droite la moitié du bord (sept « − », la huitième part, presque tangente, sous le seuil de 2 px), à gauche cinq parts courtes, du côté de l'origine. | Fondu des parts tangentes en 0,4 s ; les entrantes pulsent. | 4,4 s |
| 7.6 | [e1-ressortent] | Les parts sortantes s'allument avec leur « + », du côté opposé. | Pulsation. | 2 s |
| 7.7 | [e1-rotbilan] | Droite : sous le cercle, les parts se rangent en deux colonnes, entrantes contre sortantes ; mêmes longueurs, une à une. | Les parts glissent dans leurs colonnes en 1 s. | 6 s |
| 7.8 | [e1-rotnul] | Les deux colonnes droites se superposent et s'annulent ; le compteur 0 pulse. | Superposition en 0,5 s. | 1,6 s |
| 7.9 | [e1-srcbilan] | Gauche : même rangement ; la colonne des sortantes est nettement plus haute. | Glissement en 1 s. | 4 s |
| 7.10 | [e1-srcdeux] | L'excédent de la colonne sortante s'allume en `--chalk` ; le disque du cercle se voile à 12 % ; à côté : $\text{flux} = 2 \times \pi R^2$. | Les colonnes se superposent, l'excédent reste ; la formule s'écrit. | 3,2 s |
| 7.11 | [e1-compteur] | Les colonnes s'effacent, les parts reviennent sur le bord. Les deux cercles se promènent à nouveau, ensemble, sur une trajectoire lisse qui balaie tout le panneau ; compteurs 2 et 0, chiffres immobiles. | Mouvement continu, parts recalculées à chaque image. | 6,4 s |
| 7.12 | [e1-taille] | Les cercles respirent : rayon de 60 à 200 px et retour, sans sortir du panneau ; compteurs toujours 2 et 0. | Rayon en sinusoïde lente, deux cycles. | 4 s |
| 7.13 | [e1-simple] | Les cercles se figent. Sous les flèches, une teinte uniforme : panneau gauche teinté `--u` à 20 % d'un bord à l'autre (`Kit.fieldMap` d'une valeur constante positive), panneau droit sans teinte (valeur nulle). Les deux lignes $\nabla\cdot\mathbf{u} = 2$ et $\nabla\cdot\mathbf{u} = 0$ s'allument. | Fondu de la teinte en 0,8 s ; maintien. | 5,6 s |

### ep01.08 · `08_incompressible.html` · P14 · 28 s

Écoulement plan sans divergence, sans nom à l'écran : une rotation dont la vitesse angulaire diminue avec la distance, $\mathbf{u} = \dfrac{(-y, x)}{1 + x^2 + y^2}$. Sa divergence est nulle partout (toute rotation dont la vitesse angulaire ne dépend que de la distance au centre l'est), et il déforme une tache, contrairement à la rotation solide (traitement, idée 1). Panneau de 1000 × 720 px à gauche (x 120 à 1120, y 120 à 840), unité 120 px, centre au milieu. Flèches `--u` à 60 %. Transport exact en forme fermée : chaque point tourne autour du centre de l'angle t/(1 + r²), ce qui garde les aires exactement. Le temps de scène est réglé pour que l'écart d'angle entre le bord intérieur et le bord extérieur de la tache atteigne environ 2,5 rad à la fin de 8.5.

Tache : disque `--chalk` à 20 %, contour plein, rayon 0,5 unité, centré en (1,3 ; 0). Son contour est suivi sur 512 points. À côté, une jauge verticale « AIRE » `--muted`, dont la hauteur est l'aire calculée du polygone transporté (formule du lacet) ; un trait `--muted` fixe marque la hauteur de départ.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 8.1 | [e1-incomp] | Le panneau et ses flèches ; en haut à droite, $\nabla\cdot\mathbf{u} = 0$. | Fondu ; traceurs `--u` à 30 %. | 4,4 s |
| 8.2 | [e1-nom] | $\nabla\cdot\mathbf{u} = 0$ souligné au `Kit.pen` (underline). | Trait de 0,4 s. | 1,6 s |
| 8.3 | [e1-tache] | La tache se pose ; la jauge AIRE apparaît. | La tache commence à tourner avec le fluide. | 4,4 s |
| 8.4 | [e1-deforme] | La tache s'étire en arc : son bord intérieur prend de l'avance sur son bord extérieur. | Transport continu. | 2,4 s |
| 8.5 | [e1-garde] | La jauge reste au trait de départ. Trois petits cercles en tirets de 30 px, posés dans la tache et transportés avec elle (centres seulement), portent chacun un compteur « FLUX ÷ AIRE » à 0. | Les petits cercles suivent la tache ; compteurs calculés, toujours 0. | 5,6 s |
| 8.6 | [e1-volume] | Le panneau baisse à 30 %. À droite, une boule de fluide `--chalk` en perspective (cercle, équateur en ellipse en tirets, dégradé radial) s'étire en ellipsoïde allongé, demi-axes 1 × 1 × 1 vers $2 \times \tfrac{1}{\sqrt2} \times \tfrac{1}{\sqrt2}$ : à chaque image, demi-axes λ × 1/√λ × 1/√λ, λ de 1 à 2, dont le produit vaut exactement 1 ; jauge verticale « VOLUME », qui reste au trait de départ. | Étirement de 1,5 s. | 2,8 s |
| 8.7 | [e1-riviere] | Nouveau dessin plein cadre : une rivière vue en perspective, berges `--matter`, eau `--u` avec traceurs qui coulent vers la droite. Une goutte `--chalk` (petite sphère) est portée par le courant, s'allonge un peu dans une accélération et reprend sa forme ; la jauge VOLUME la suit, immobile. | Traceurs continus ; trajet de la goutte en 3,5 s. | 4 s |
| 8.8 | [e1-comprimer] | Deux seringues `--matter` côte à côte, fermées au bout : l'une remplie d'air, vide ou parsemée de quelques points `--muted` épars, sans bulles ; l'autre pleine d'eau `--u`. Aucune étiquette, ni « compressible » ni « incompressible ». Un même poids `--matter-dark` pousse les deux pistons : celui de l'air s'enfonce de moitié, celui de l'eau ne bouge presque pas. | Descente des pistons en 1 s ; maintien. | 2,8 s |

### ep01.09 · `09_circulation.html` · P15, P16 · 61 s

Même champ, même panneau, même point P et même cercle que la scène 03 : $\mathbf{u} = (x - 0{,}4y,\ y + 0{,}4x)$, panneau à gauche, colonne d'équation à droite. Vorticité de ce champ : ω = 0,4 − (−0,4) = 0,8 partout.

Calcul du plan 9.7. La part le long du bord, comptée dans le sens trigonométrique, vaut au point de tangente t : t·(A c) + 0,4 R. Pour le cercle déplacé de la scène 03 (c = (−212, −212) px, |A c| ≈ 323 px, R = 180 px), elle est négative là où t·(A c) < −72 px, c'est-à-dire là où l'angle entre t et A c dépasse 102,9°, sur environ 154° du bord, soit 7 des 16 points (premier point à 0°, comme en scène 03 : les points de 270° à 45°). La circulation totale reste positive (0,8 fois l'aire).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 9.1 | [e1-transition] | Le cercle de la scène 03, centré sur P, avec ses seize parts perpendiculaires et la fiche FLUX. | Fondu d'entrée, puis les parts perpendiculaires et la fiche baissent à 30 %. | 3,6 s |
| 9.2 | [e1-tourneq] | Le pictogramme « tourne » de l'ouverture se pose en haut de la colonne. | Sa flèche fait un tour, sens trigonométrique. | 3,6 s |
| 9.3 | [e1-parcours] | Une flèche de parcours `--chalk` court sur le cercle, sens trigonométrique. | Un tour en 2,5 s, puis elle reste posée en haut du cercle, pointe vers la gauche. | 4,8 s |
| 9.4 | [e1-trigo] | À côté du cercle, un petit cadran d'horloge `--muted` dont l'aiguille tourne dans le sens horaire ; la flèche de parcours refait un demi-tour, dans l'autre sens que l'aiguille. | Les deux mouvements ensemble, 1,5 s. | 3,2 s |
| 9.5 | [e1-autre] | Le cadran s'efface. Rôles échangés sur la flèche du bord : la part le long du bord passe en `--u` plein, la part perpendiculaire en tirets `--muted`. Puis seize parts tangentes autour du cercle. | Échange de style en 0,4 s, puis les seize parts poussent en un tour. | 5,2 s |
| 9.6 | [e1-avec] | Ici, toutes les parts vont dans le sens du parcours : chacune reçoit un « + » `--chalk`. | Les « + » s'allument en un tour. | 4,4 s |
| 9.7 | [e1-contre] | Le cercle glisse de 300 px vers le bas à gauche, comme en 3.12 : sept parts vont contre le parcours et reçoivent un « − » `--muted`. | Glissement de 1 s, parts recalculées à chaque image ; retour sur P en 1 s. | 2,8 s |
| 9.8 | [e1-circulation] | Un arc `--chalk` rassemble les seize parts ; à droite, fiche « CIRCULATION ». | L'arc fait le tour en 1 s. | 3,6 s |
| 9.9 | [e1-recette] | Dans la colonne, l'équation de la scène 04 revient : $\lim_{r\to0} \dfrac{\text{flux}}{\pi r^2}$ ; le mot « flux » se change en « circulation ». | `Kit.morph` du numérateur en 0,8 s. | 4 s |
| 9.10 | [e1-divaire] | Le disque se voile à 12 % ; le cercle rétrécit vers P de 180 à 20 px. Aucun compteur (champ linéaire). | Rayon en 2,5 s, inOutCubic. | 4 s |
| 9.11 | [e1-vorticite] | L'équation complète : $\omega(P) = \lim_{r\to0} \dfrac{\text{circulation}}{\pi r^2}$, même mise en page que la divergence. | Le membre de gauche s'écrit. | 2,8 s |
| 9.12 | [e1-vortsens] | Autour de P, des traceurs `--u` à 40 % montrent l'écoulement qui s'écarte en tournant un peu ; une petite flèche courbe `--u` trigonométrique à côté de P. | Traceurs continus. | 4,4 s |
| 9.13 | [e1-carre] | Le petit cercle se morphose en carré en tirets de 240 px, centré sur P. | Morphose de 0,8 s. | 2,8 s |
| 9.14 | [e1-croise] | En haut de la colonne, rappel à 40 % : $\nabla\cdot\mathbf{u} = \partial_x u_x + \partial_y u_y$, avec ses traits verticaux de la scène 05. En dessous : $\omega = \partial_x u_y - \partial_y u_x$ ; dans chaque terme, les deux indices en `--chalk` reliés par un trait diagonal. | Écriture terme à terme ; les traits de croisement se dessinent au `Kit.pen` (arrow, sans pointe). | 2,4 s |
| 9.15 | [e1-vertdroite] | Sur le carré, côtés droit et gauche en plein ; au milieu de chacun, la part verticale de la flèche, le long du côté : vers le haut à droite, vers le bas à gauche, dans le sens du parcours des deux côtés. Le terme $\partial_x u_y$ s'allume. | Les parts poussent ; le terme pulse. | 4,4 s |
| 9.16 | [e1-horizhaut] | Côtés haut et bas en plein ; au milieu de chacun, la part horizontale : vers la gauche en haut, vers la droite en bas. À côté du côté haut, une petite flèche de parcours vers la gauche : sur ce côté, le parcours va à contre-sens de l'axe horizontal, d'où le signe. Le signe « − » et le terme $\partial_y u_x$ s'allument. | Les parts poussent ; le signe, puis le terme, pulsent ; maintien. | 4,8 s |

### ep01.10 · `10_rotationnel_roue.html` · P17, P18 · 56 s

Plans 10.1 à 10.8 : le champ et le panneau de la scène 09. Plans 10.9 à 10.14 : rotation solide $\mathbf{u} = (-y, x)$, panneau de 1000 × 720 px à gauche, flèches `--u` à 50 %. Un disque de fluide `--chalk` à 8 %, centré sur l'origine, porte un rayon marqué. Roue à aubes posée à 200 px de l'origine, portée par le fluide. Vitesse angulaire du fluide : 1 rad par seconde de scène, un tour en 6,3 s.

Perspective : transformation affine du dessin 2D (parallélogramme, inclinaison de 55°), pas de 3D CSS. Vue de face, une flèche qui sort de l'écran se dessine ⊙ (cercle et point central), une flèche qui y entre ⊗ (cercle et croix), en `--u`.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 10.1 | [e1-fleche3d] | Le carré s'efface. Le panneau bascule en perspective ; au point P, une flèche `--u` qui sort du plan vers le haut ; à droite, $\nabla\times\mathbf{u}$. | Bascule de 1,2 s ; la flèche pousse ; formule avec la voix. | 4,8 s |
| 10.2 | [e1-plan] | Une grille de neuf flèches identiques, perpendiculaires au plan, une par point (ω vaut 0,8 partout). Puis le panneau revient de face : chaque flèche devient un ⊙. | Les flèches poussent ; retour de face en 1 s, les flèches se raccourcissent en perspective jusqu'au ⊙. | 4 s |
| 10.3 | [e1-signe] | Le panneau s'efface. Deux petits disques en perspective, côte à côte : à gauche, flèche courbe `--u` trigonométrique dans le disque et flèche droite qui monte, étiquette $\omega > 0$ ; à droite, flèche courbe horaire et flèche qui descend sous le disque, $\omega < 0$. Puis les deux disques reviennent de face : ⊙ à gauche, qui grossit un peu comme s'il venait vers nous ; ⊗ à droite, qui rapetisse un peu comme s'il s'éloignait. | Les flèches poussent, puis retour de face en 1 s. | 4,8 s |
| 10.4 | [e1-longueur3d] | Un seul disque en perspective, flèche verticale à son centre, accolade `--muted` le long de la flèche, étiquette $\lvert\omega\rvert$. La vorticité du disque diminue, passe par zéro et devient négative : la flèche raccourcit, disparaît, puis pousse vers le bas ; l'étiquette $\omega > 0$, puis $\omega = 0$, puis $\omega < 0$ suit. Aucun nombre. | Variation continue en 3 s. | 3,6 s |
| 10.5 | [e1-roue] | Retour au panneau de la scène 09, à plat. Une petite roue à aubes (section 0) se pose **sur P**, point de vitesse nulle : elle n'est pas emportée. | Descente de 0,6 s, petit amorti (dépassement ≤ 3 %). | 4,8 s |
| 10.6 | [e1-pousse] | Zoom de 1,8× sur la roue. Au bout de chaque aube, la flèche du fluide en ce point ; sa part le long du cercle des aubes en `--u` plein, sa part radiale en tirets `--muted`. L'aube marquée porte un petit arc `--chalk` entre un trait de référence fixe et elle-même, étiqueté « α » : l'angle est défini avant son premier emploi en 10.7 (arbitrage de la session principale). | Dès qu'elle est posée, la roue tourne dans le sens trigonométrique à 0,4 rad par seconde de scène (ω/2 pour ω = 0,8), angle en forme fermée, jusqu'à 10.8. | 5,2 s |
| 10.7 | [e1-moitie] | Retour au plan large ; à droite, en grand : $\dot\alpha_{\text{roue}} = \dfrac{\omega}{2}$. | Écriture. | 4 s |
| 10.8 | [e1-exemple] | L'équation monte en haut de la colonne et y reste ; le panneau s'efface. | Glissement de 0,6 s. | 2,4 s |
| 10.9 | [e1-reprends] | Panneau de la rotation solide ; la roue posée à 200 px de l'origine. | Fondu ; le fluide tourne (traceurs, 200 particules, et rayon marqué) ; la roue tourne avec lui. | 2,8 s |
| 10.10 | [e1-disque] | Le disque de fluide et son rayon marqué s'allument ; tous les traceurs gardent leurs distances. | Rotation continue. | 4,4 s |
| 10.11 | [e1-vitesseun] | Sous l'équation, un cadran `--muted` : un trait de référence fixe `--muted`, horizontal vers la droite ; une aiguille `--u` qui suit l'angle du rayon marqué ; entre les deux, un arc `--muted` étiqueté α, qui grandit dans le sens trigonométrique avec l'aiguille et repart de zéro à chaque tour. Aucun mot. Sous le cadran, $\dot\alpha_{\text{disque}} = 1$. | Rotation continue ; l'arc se dessine avec l'aiguille ; la formule s'écrit. | 3,6 s |
| 10.12 | [e1-colle] | Second cadran à côté, même construction (trait de référence, arc α) : son aiguille `--chalk` suit l'aube marquée ; sous lui, $\dot\alpha_{\text{roue}} = 1$. Les deux aiguilles restent alignées ; l'aube marquée reste parallèle au rayon marqué. | Rotation continue ; au bout d'un tour, un trait bref `--chalk` sur les deux cadrans. | 4 s |
| 10.13 | [e1-affiche] | Un cercle en tirets de 70 px, centré sur la roue et emporté avec elle ; son compteur « VORTICITÉ » (circulation ÷ aire, calculée) : 2. | Le cercle se trace, le compteur s'allume. | 2,8 s |
| 10.14 | [e1-retiens] | Rapprochement : $\dot\alpha_{\text{roue}} = 1$ glisse en face du compteur, $\omega = 2$ ; l'équation $\dot\alpha_{\text{roue}} = \omega/2$ du haut entourée au `Kit.pen`. | Glissement de 0,6 s ; trait de 0,6 s. | 5,2 s |

### ep01.11 · `11_cisaillement.html` · P19, P20 · 51 s

Cisaillement $\mathbf{u} = (y, 0)$, panneau de 1100 × 640 px à gauche (x 120 à 1220, y 136 à 776), y = 0 au milieu (à l'écran y = 456), unité 160 px, y de −2 à 2. Flèches `--u` : vers la droite en haut, vers la gauche en bas, longueur proportionnelle à |y|, nulles sur la ligne du milieu. Colonne d'équation à droite (x 1300 à 1800). Roue posée au centre du panneau, (670, 456).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 11.1 | [e1-surprises] | Panneau vide ; la ligne du milieu en `--muted` fin. | Fondu. | 1,6 s |
| 11.2 | [e1-cisail] | En haut de la colonne : $\mathbf{u} = (y, 0)$. | Écriture. | 2 s |
| 11.3 | [e1-haut] | Flèches de la moitié haute, vers la droite. | Entrée ligne par ligne en 1 s, de la ligne du milieu vers le bord ; traceurs `--u` à 40 % qui glissent à droite. | 3,2 s |
| 11.4 | [e1-bas] | Flèches de la moitié basse, vers la gauche. | Même entrée ; traceurs qui glissent à gauche. | 2,8 s |
| 11.5 | [e1-milieu] | Sur la ligne du milieu, des points `--chalk` à la place des flèches ; les traceurs qui la touchent sont immobiles. | Les points s'allument. | 3,2 s |
| 11.6 | [e1-loin] | Une colonne de flèches s'allume, du bas vers le haut ; un trait `--chalk` relie leurs pointes : une droite inclinée, le profil des vitesses. | Tracé du profil en 0,8 s. | 4 s |
| 11.7 | [e1-courant] | Fiche « LIGNE DE COURANT » dans la colonne. Un traceur `--fg` part d'un point du haut et laisse derrière lui un trait `--u` qui suit partout les flèches. | Le traceur avance vers la droite en 3 s. | 5,6 s |
| 11.8 | [e1-droites] | Sept lignes de courant horizontales `--u`, droites (`Kit.fieldLines`). | Tracé en 1 s. | 4,8 s |
| 11.9 | [e1-pose] | La roue à aubes descend et se pose **sur la ligne du milieu**, au centre du panneau. | Descente de 0,6 s ; son centre reste immobile, puisque la vitesse y est nulle. | 3,2 s |
| 11.10 | [e1-aubeshaut] | Sur l'aube du haut, une flèche `--u` vers la droite. | La flèche pousse. | 3,6 s |
| 11.11 | [e1-aubesbas] | Sur l'aube du bas, une flèche `--u` vers la gauche. | La flèche pousse. | 3,6 s |
| 11.12 | [e1-horaire] | La roue tourne **dans le sens horaire** à ½ rad par seconde de scène ; une flèche courbe `--chalk` horaire à côté, sans chiffre. | Rotation continue jusqu'à la fin de la scène. | 3,2 s |
| 11.13 | [e1-moinsun] | Cercle en tirets de 80 px autour de la roue, compteur « VORTICITÉ » : −1. Dans la colonne : $\omega = \partial_x u_y - \partial_y u_x = 0 - 1 = -1$. | Écriture terme à terme. | 2,4 s |
| 11.14 | [e1-undemi] | En dessous : $\dot\alpha_{\text{roue}} = \omega/2 = -\tfrac12$, la flèche courbe horaire posée à côté du signe moins : le signe moins est le sens horaire. Jamais « ½ » seul. | Écriture ; la flèche courbe glisse jusqu'au signe. | 3,2 s |
| 11.15 | [e1-lecon1] | Le panneau se réduit en vignette dans le coin haut droit : lignes droites, roue qui tourne, ω = −1. La vignette reste jusqu'à la fin de la scène. | Réduction de 0,8 s. | 4,8 s |

### ep01.12 · `12_tourbillon.html` · P21, P22 · 58 s

Tourbillon ponctuel $\mathbf{u} = \dfrac{(-y, x)}{x^2 + y^2}$, sens trigonométrique, centre au milieu du panneau (1000 × 760 px, à gauche, x 120 à 1120, y 100 à 860 ; centre à l'écran en (620, 480)) ; colonne à droite x 1180 à 1780. Unité : 100 px. Flèches `--u`, longueur compressée (section 0, I_s = 0,8), disque vide de 30 px autour du centre, point `--fg` au centre. Contrainte : **la roue n'est jamais posée sur le centre** ; aucun cercle ne rétrécit vers le centre. Roue de rayon a = 0,5 (50 px) sur le cercle R = 2,2 (220 px).

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 12.1 | [e1-tourbillon] | Panneau vide, point du centre. | Fondu. | 2 s |
| 12.2 | [e1-autour] | Flèches du tourbillon ; cinq lignes de courant circulaires `--u`. | Flèches de l'extérieur vers l'intérieur ; lignes tracées en 1,2 s. | 3,2 s |
| 12.3 | [e1-diminue] | À droite, $\lvert\mathbf{u}\rvert = \dfrac{1}{r}$, et un petit schéma : r est le segment `--muted` du centre à un point. | Formule avec la voix. | 4 s |
| 12.4 | [e1-double] | Sur un rayon `--muted`, deux flèches s'allument, à r = 1,5 et r = 3 (150 et 300 px) : la seconde est exactement deux fois plus courte (intensités 0,67 et 0,33, sous le seuil). Deux graduations `--muted` « r » et « 2r ». | Pulsation des deux flèches. | 4 s |
| 12.5 | [e1-loincentre] | La roue se pose sur le cercle R = 2,2 et fait le tour du centre dans le sens trigonométrique, celui du fluide, à vitesse constante (un tour en 9 s de scène), **sans pivoter** : l'aube marquée reste pointée vers le haut. Un trait `--muted` fixe à côté sert de référence verticale. | Orbite continue. | 4,4 s |
| 12.6 | [e1-cabine] | Des fantômes de la roue à 25 %, laissés tous les 45° de son orbite : tous ont l'aube marquée vers le haut. | Un fantôme se dépose à chaque passage ; orbite continue. | 4,8 s |
| 12.7 | [e1-surplace] | Cadran à droite, son aiguille `--chalk` suit l'aube marquée : immobile. | — | 2,4 s |
| 12.8 | [e1-bords] | Les fantômes s'effacent. La roue s'arrête à droite du centre (position 3 h). Zoom de 1,8× sur elle. | Ralenti jusqu'à l'arrêt, zoom de 0,8 s. | 2,8 s |
| 12.9 | [e1-proche] | Deux flèches de vitesse `--u` sur ses deux bords, la plus longue du côté du centre, rapport des longueurs exact : 1/(R − a) contre 1/(R + a), soit 0,59 contre 0,37, sous le seuil 0,8. Rappel $\lvert\mathbf{u}\rvert = 1/r$ dans le calque de formule. | Les deux flèches poussent. | 5,2 s |
| 12.10 | [e1-unsens] | Une petite flèche courbe `--u` horaire au-dessus de la roue : ce que ferait cet écart. | La flèche courbe se dessine. | 4,4 s |
| 12.11 | [e1-courbure] | L'arc de la trajectoire en `--chalk`, de part et d'autre de la roue. | Tracé de l'arc. | 2 s |
| 12.12 | [e1-virage] | Une seconde flèche courbe `--u` trigonométrique, de même taille, sous la roue : ce que ferait la courbure. | La flèche courbe se dessine. | 3,6 s |
| 12.13 | [e1-annulent] | Les deux flèches courbes se rapprochent et s'annulent ; l'aiguille du cadran reste immobile. | Glissement de 0,8 s, puis fondu des deux. | 4,4 s |
| 12.14 | [e1-exo2] | Chip `plain` dans la colonne : « MODULE 1 · EXERCICE 2 (C) », un petit crayon `--chalk` à côté. Dessous, la question, présentée comme à calculer : $\mathbf{u} = \dfrac{(-y,\ x)}{x^2 + y^2}$ et $\omega = \partial_x u_y - \partial_y u_x = \ ?$ pour $r > 0$ ; le point d'interrogation reste, aucune valeur ne le remplace dans ce plan. À côté du champ, en `--muted`, $\Gamma = 2\pi$ : le tourbillon de l'écran est celui de l'énoncé, $\mathbf{u} = \frac{\Gamma}{2\pi r}\mathbf{e}_\theta$, pour cette valeur. | Le chip s'écrit, puis la question, puis $\Gamma = 2\pi$ ; le crayon trace un petit trait. | 5,6 s |
| 12.15 | [e1-lecon2] | Retour au plan large. En vignettes côte à côte, à droite : le cisaillement (lignes droites, roue qui tourne, $\omega = -1$) et le tourbillon (lignes courbes, roue qui ne tourne pas, $\omega = 0$ pour $r > 0$). | Les vignettes jouent leur mouvement en boucle courte. | 5,2 s |

### ep01.13 · `13_tourbillon_centre.html` · P23 · 30 s

Même tourbillon, même panneau et mêmes réglages que la scène 12. Les valeurs 2π et 0 de 13.5 à 13.7 sont symboliques : écrites, non calculées. Les petits cercles de 13.2, eux, portent des compteurs calculés.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 13.1 | [e1-ou] | Les vignettes s'effacent ; le point du centre pulse. | — | 3,6 s |
| 13.2 | [e1-nullepartout] | Dix petits cercles en tirets de 30 px, posés partout sur la carte à plus de 80 px du centre ; aucun ne l'entoure. Chacun porte un petit compteur « CIRCULATION ÷ AIRE » : 0. Dans la colonne : $\omega = 0$ pour $r > 0$. | Les cercles apparaissent un à un ; les compteurs, calculés, affichent 0. | 2,8 s |
| 13.3 | [e1-nondef] | Le disque vide du centre se borde d'un trait `--muted` ; les flèches les plus proches du centre sont les plus longues de la carte, dans la partie compressée. Dans la colonne : $\lvert\mathbf{u}\rvert = \dfrac{1}{r} \to \infty$ quand $r \to 0$. | Pulsation des flèches proches du centre. | 4,8 s |
| 13.4 | [e1-entiere] | Les petits cercles s'effacent ; le point du centre s'allume en `--u-hi`. | Pulsation lente. | 4 s |
| 13.5 | [e1-revele] | Un cercle en tirets de 120 px centré sur le centre ; à côté, sa valeur « CIRCULATION » : 2π, sans division par l'aire. | Le cercle se trace, la valeur s'écrit. | 5,2 s |
| 13.6 | [e1-memecirc] | Deux autres cercles qui **entourent** le centre, du plus petit au plus grand (jamais un rétrécissement) : rayon 220 px **décentré**, centre à (70, 40) px du centre du tourbillon, qui l'entoure toujours ; rayon 320 px centré. Chacun : 2π. | Chaque cercle se trace, sa valeur s'écrit. | 3,6 s |
| 13.7 | [e1-zerocirc] | Un quatrième cercle, qui n'entoure pas le centre : rayon 70 px, centre à (−380, 250) px du centre, à l'écran en (240, 230), hors du grand cercle. Valeur : 0. | Tracé, valeur. | 3,6 s |
| 13.8 | [e1-image] | Tout baisse à 40 % sauf le centre et les trois valeurs 2π. | Fondu ; maintien. | 2,8 s |

### ep01.14 · `14_cellules_limite.html` · P24 · 40 s

L'écoulement cellulaire de la scène 01 (section 0), panneau carré de 780 px à gauche (x 120 à 900, y 80 à 860). Cercle centré en C = (1,4 ; 1,8), le point de la scène 01, dans la cellule en bas à gauche, loin des droites x = π et y = π. Valeur attendue : ω(C) = 2 sin 1,4 sin 1,8 ≈ 1,92. À droite, un graphe `Kit.plot` (x 1040 à 1780, y 160 à 700) : axe horizontal « RAYON », axe vertical « CIRCULATION ÷ AIRE ». Aucun ψ, aucune carte de couleur.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 14.1 | [e1-retour] | La carte de l'ouverture, au centre, comme en 1.1. | Fondu d'entrée. | 2,8 s |
| 14.2 | [e1-engrenages] | Lignes de courant fermées `--u` à 45 % ; traceurs (300 particules, 40 %) ; dans chaque cellule, une flèche courbe `--u` : trigonométrique en bas à gauche et en haut à droite, horaire dans les deux autres. | Lignes tracées en 1,5 s ; les traceurs font tourner les cellules côte à côte. | 5,6 s |
| 14.3 | [e1-coin] | La carte glisse à gauche. Calque de formule en bas à droite, étiquette « CHAMP » : $\mathbf{u} = (\sin x\cos y,\ -\cos x\sin y)$. | Glissement de 0,8 s ; le calque s'ouvre. | 3,2 s |
| 14.4 | [e1-paslire] | Le calque baisse à 60 % et y reste jusqu'à la fin de la scène. Les flèches courbes s'effacent. | Fondu. | 2,8 s |
| 14.5 | [e1-dedans] | Cercle en tirets centré sur C, rayon 1,2 unité, à l'intérieur de la cellule ; compteur « CIRCULATION ÷ AIRE » à sa droite. | Le cercle se trace ; le compteur s'allume. | 2,8 s |
| 14.6 | [e1-varie] | Le graphe s'ouvre ; le point (rayon, valeur) se pose, puis le cercle rétrécit et le point trace la courbe, du grand rayon vers le petit. | Rayon de 1,2 à 0,6 ; la valeur du compteur change visiblement. | 7,6 s |
| 14.7 | [e1-rapetisse] | La courbe s'aplatit. | Rayon de 0,6 à 0,15, plus lentement ; le compteur ralentit. | 4,4 s |
| 14.8 | [e1-fixe] | Le compteur s'arrête sur 1,92. | Rayon de 0,15 à 0,05 ; arrêt. | 2,8 s |
| 14.9 | [e1-valeur] | Ligne horizontale `--muted` en tirets sur le graphe à 1,92, étiquette $\omega(C)$ ; point C `--chalk` au centre du cercle. | `P.hline`. | 3,6 s |
| 14.10 | [e1-visible] | La courbe entière reste ; son extrémité gauche et la ligne se touchent, entourées au `Kit.pen`. | Trait de 0,6 s. | 4,4 s |

### ep01.15 · `15_enigme.html` · P25 · 24 s

Même carte, même panneau qu'à la fin de la scène 14 ; graphe effacé ; calque de formule en bas à droite, à 60 %, jusqu'à la fin de la scène. Compteurs « FLUX ÷ AIRE » calculés, jamais « −0 ».

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 15.1 | [e1-autreq] | Le pictogramme « sort » de l'ouverture se pose à droite de la carte. Un cercle en tirets de 90 px et son compteur « FLUX ÷ AIRE ». | Les flèches du pictogramme poussent ; le cercle se trace. | 4,8 s |
| 15.2 | [e1-promene] | Le cercle se promène sur une trajectoire fixée qui traverse plusieurs cellules et franchit les droites de séparation ; son rayon varie de 60 à 200 px. Compteur : 0. | Trajectoire et rayon continus. | 3,6 s |
| 15.3 | [e1-zero] | Même mouvement ; le compteur pulse, toujours 0. | Pulsation à mi-plan. | 3,6 s |
| 15.4 | [e1-nullepart] | Douze petits cercles en tirets de 40 px s'allument d'un coup sur toute la carte, sur les droites de séparation comme au milieu des cellules ; chacun avec son compteur : 0. | Apparition en vague de 1 s. | 4,4 s |
| 15.5 | [e1-hasard] | Les petits cercles s'effacent ; le grand s'arrête. | Fondu de 0,4 s. | 2 s |
| 15.6 | [e1-pourquoi] | Un point d'interrogation `--chalk` de 120 px à côté du compteur. | Pulsation du compteur. | 2,8 s |
| 15.7 | [e1-ouverte] | Le point d'interrogation se réduit et va se loger dans le coin haut gauche, où il reste jusqu'à la fin de la scène. | Glissement de 0,8 s. | 2,8 s |

### ep01.16 · `16_cloture.html` · P26, P27 · 36 s

Les deux pictogrammes de l'ouverture en colonne à gauche (x 160 à 360) ; chacun reçoit sa formule en face (x 420 à 1200). Colonne de droite (x 1280 à 1800) : vignettes, puis carte d'exercices.

| # | Repère | Image | Mouvement | Durée |
|---|---|---|---|---|
| 16.1 | [e1-retenir] | Les deux pictogrammes, « sort » en haut, « tourne » en bas. | Apparition échelonnée. | 1,2 s |
| 16.2 | [e1-sortir] | En face de « sort » : $\nabla\cdot\mathbf{u} = \lim_{r\to0} \dfrac{\text{flux}}{\pi r^2} = \partial_x u_x + \partial_y u_y$. | Écriture ; le cercle du pictogramme rétrécit un peu et revient. | 5,6 s |
| 16.3 | [e1-tourner] | En face de « tourne » : $\omega = \lim_{r\to0} \dfrac{\text{circulation}}{\pi r^2} = \partial_x u_y - \partial_y u_x$. | Écriture. | 3,6 s |
| 16.4 | [e1-rouemoitie] | Sous la ligne de ω : $\dot\alpha_{\text{roue}} = \omega/2$, avec une petite roue. | Écriture ; la roue fait un quart de tour **dans le sens trigonométrique**, comme pour ω > 0. | 4,4 s |
| 16.5 | [e1-rappelcis] | À droite, vignette du cisaillement de la scène 11 : lignes droites, roue qui tourne dans le sens horaire, $\omega = -1$. | La vignette joue sa boucle. | 5,2 s |
| 16.6 | [e1-rappeltour] | En dessous, vignette du tourbillon de la scène 12 : lignes circulaires, roue qui fait le tour sans pivoter, $\omega = 0$ pour $r > 0$. | La vignette joue sa boucle. | 5,2 s |
| 16.7 | [e1-crayon] | Les vignettes s'effacent ; à leur place, la carte d'exercices : « EXERCICES » en mono, puis trois lignes 1 (b) · 2 (b) · 2 (c) ; dessous, l'ancre « #exercices » en `--muted`. Petit crayon `--chalk`. | Lignes en cascade. | 2,4 s |
| 16.8 | [e1-exos] | En face de chaque ligne, une miniature de l'image qu'elle met en calcul : 1 (b), les deux formules de gauche, posées à côté de la ligne sans signe d'égalité entre elles et l'énoncé (l'exercice les applique à un autre champ, en trois dimensions) ; 2 (b), la roue du cisaillement ; 2 (c), la roue du tourbillon. | Les miniatures apparaissent une à une. | 4 s |
| 16.9 | [e1-suivant] | Tout baisse à 40 %, sauf un petit cercle en tirets au centre, qui se démultiplie en un carrelage de 3 × 2 carreaux dont le contour s'épaissit. | Carrelage en 1,2 s ; maintien, puis fondu au noir de 1 s en fin de scène (3 s de pause conseillée). | 4 s |

## 3. Contraintes physiques : où elles portent

| Contrainte | Plans |
|---|---|
| Axe y vers le haut ; la cellule en bas à gauche tourne dans le sens trigonométrique | 1.1, 1.4, 14.2, 15.x ; vérification sur image fixe (section 0) |
| Cercle centré ou cercle déplacé, selon le cas | 3.11, 3.12, 7.1 à 7.13, 9.6, 9.7, 13.5 à 13.7 |
| Un cercle déplacé ne montre des parts entrantes que s'il est assez loin (3.12 : \|c\| > 167 px ; 7.5 : \|c\| ≈ 244 px > 130 px, phase 11,25°, cinq parts entrantes franches) ; des parts à contre-parcours que si t·(A c) < −0,4 R (9.7 : environ 154°, sept points) | 3.12, 7.5, 9.7 |
| Aucun « + » ni « − » sur une part de moins de 2 px | 3.11, 3.12, 7.2 à 7.6, 9.6, 9.7 |
| Flèches d'une même colonne de l'écoulement cellulaire : même direction, longueurs 0,5 et 1 | 1.2, 1.3 |
| Le flux d'un grand cercle dépasse celui d'un petit ; divisés par l'aire, ils s'égalent pour un champ de divergence uniforme | 4.1, 4.2 |
| Le robinet et la bonde sont vus de dessus : l'eau semble naître sous le jet, elle quitte la carte par la bonde ; le jet s'éloigne de l'œil, aucun ⊙ ni ⊗ dans son disque ; gerbes en 1/r, donc sans divergence hors du disque : $\nabla\cdot\mathbf{u} > 0$ accroché au disque du jet, $\nabla\cdot\mathbf{u} < 0$ au disque de la bonde | 3.4, 4.5, 4.8 |
| Le petit carré : h = 1,2 < 1,6, sens des quatre flèches conservé ; les deux points de mesure séparés de h | 5.3 à 5.12 |
| Une raison montrée pour chaque dérivée : graphe de pente 1 pour la source, graphe plat pour la rotation, sur des droites de marche à hauteur ou abscisse fixe | 6.4, 6.5, 6.10, 6.11 |
| Le compteur affiche exactement 2 ou 0, où que soit le cercle et quelle que soit sa taille, sur ces deux champs seulement ; pas de stabilisation montrée sur un champ linéaire | 7.4, 7.11, 7.12, 9.10 |
| Tache transportée par un écoulement sans divergence qui la déforme, pas par la rotation solide ; aire calculée constante | 8.3 à 8.5 |
| La rivière illustre le volume dans l'espace, pas une aire en surface | 8.6 à 8.8 |
| La circulation se calcule dans le sens trigonométrique | 9.3 à 9.8, 9.16, 13.5 à 13.7 |
| Rotationnel : perpendiculaire à l'écran, il sort pour ω > 0 (⊙), il entre pour ω < 0 (⊗) ; sa longueur est \|ω\| | 10.1 à 10.4 |
| La roue posée en un point de vitesse nulle, ou portée par le fluide ; son sens et sa vitesse valent ω/2 | 10.5 à 10.7, 10.9 à 10.14, 11.12 à 11.14, 16.4 |
| Rotation solide : $\dot\alpha_{\text{disque}} = 1$, $\dot\alpha_{\text{roue}} = 1$, α compté positivement dans le sens trigonométrique ; l'aube marquée reste parallèle au rayon marqué ; compteur de vorticité à 2 | 10.11 à 10.14 |
| Le cisaillement : à droite en haut, à gauche en bas, immobile au milieu ; roue posée sur la ligne du milieu, sens horaire, $\dot\alpha_{\text{roue}} = -\tfrac12$ | 11.3 à 11.14, vignettes 12.15 et 16.5 |
| La roue fait le tour du tourbillon dans le sens trigonométrique, à vitesse constante, sans pivoter | 12.5, 12.6 |
| Volume de la boule conservé : demi-axes de produit 1 à chaque image | 8.6 |
| La roue jamais sur le centre du tourbillon ; aucun cercle ne rétrécit vers ce centre | 12.5 à 12.13, 13.2 (petits cercles à plus de 80 px du centre), 13.5 à 13.7 (cercles apparus du petit au grand) |
| Flèches du tourbillon : longueur strictement croissante, linéaire sous le seuil, rapports exacts quand la voix compare | 12.4, 12.9 |
| Vorticité du tourbillon nulle pour r > 0, non définie au centre ; même circulation 2π pour tout cercle qui entoure le centre, 0 sinon | 13.2 à 13.7 |
| Cercle rétrécissant loin des droites qui séparent les cellules ; valeur limite ω(C) ≈ 1,92 | 14.5 à 14.10 |
| Rien sur la fonction de courant, aucun ψ à l'écran | scènes 01, 14, 15 |

## 4. Points signalés à la narration (non modifiée)

1. **P1, ligne « écran ».** Elle prévoit d'écrire les deux questions, « est-ce que ça sort ? » et « est-ce que ça tourne ? », que la voix dit au même moment. Le storyboard met à la place deux pictogrammes, « sort » et « tourne » (1.6, 1.7), qui reviennent aux scènes 09, 15 et 16.
2. **P4, ligne « écran ».** Elle prévoit le sous-titre « dériver en x en gardant y fixe », qui redit [e1-avance]. Le storyboard écrit l'étiquette $y = 1$ sur la droite de marche (2.7), puis $x = 1$ (2.10).
3. **P6, ligne « écran ».** Elle prévoit des parts vertes vers l'extérieur et rouges vers l'intérieur. Le vert `--param` est réservé aux paramètres de contrôle et le thème n'a pas de rouge. Le storyboard garde `--u` pour toutes les parts, avec « + » `--chalk` et « − » `--muted` (3.11, 3.12), comme l'ancien storyboard.
4. **P7, ligne « écran ».** Elle prévoit « divergence = flux sortant ÷ aire, quand le cercle rétrécit », c'est-à-dire la phrase de la voix. Le storyboard écrit la formule $\nabla\cdot\mathbf{u}(P) = \lim_{r\to0} \text{flux}/\pi r^2$ (4.4).
5. **P14, ligne « écran ».** Elle prévoit « divergence nulle : l'aire se conserve » et « dans l'espace : le volume se conserve », qui redisent la voix. Le storyboard montre $\nabla\cdot\mathbf{u} = 0$ et deux jauges, AIRE et VOLUME, immobiles pendant que la tache et la boule se déforment (8.5, 8.6).
6. **P18, ligne « écran ».** Elle prévoit « vitesse de rotation de la roue = ω ÷ 2 » et « vitesse de rotation du disque : 1 », ce que la bible reprend (section 1, rotation solide). Le storyboard écrit $\dot\alpha_{\text{roue}} = \omega/2$ (10.7) et $\dot\alpha_{\text{disque}} = 1$ sous un cadran (10.11), où α, l'angle du rayon marqué compté dans le sens trigonométrique, est défini sans mot par un arc entre un trait de référence fixe et l'aiguille. La lettre grecque majuscule du domaine n'est pas employée : `docs/specs/notations.md` et ep02 la réservent au domaine. Le sens est le même, sans recopier la phrase dite à [e1-vitesseun]. Si la session principale tient à la ligne de la bible, elle s'écrit sous le cadran à la place de la formule.
7. **P20, ligne « écran ».** Elle prévoit « vitesse de rotation de la roue = 1/2, sens horaire ». Le storyboard écrit $\dot\alpha_{\text{roue}} = \omega/2 = -\tfrac12$, la flèche horaire posée contre le signe moins (11.14), comme le veut la correction 2 de l'ancien storyboard : jamais « ½ » seul.
8. **P23, ligne « écran ».** Elle prévoit « vorticité nulle hors du centre » et le centre marqué « non définie », qui redisent la voix. Le storyboard écrit $\omega = 0$ pour $r > 0$ (13.2), fait voir des compteurs à 0 sur dix petits cercles, et écrit $\lvert\mathbf{u}\rvert = 1/r \to \infty$ au centre (13.3), qui donne la raison au lieu de redire le mot.
9. **P25, ligne « écran ».** Elle prévoit le mot « pourquoi ? ». Le storyboard garde le seul point d'interrogation (15.6, 15.7), qui reste dans le coin.
10. **P23, valeurs du compteur de circulation.** La ligne « écran » de P23 parle d'un compteur « circulation » ; le storyboard écrit les valeurs 2π et 0 comme symboliques (13.5 à 13.7), comme l'ancien storyboard, pour ne pas afficher 6,28 sur un cercle qui entoure une singularité.

## 5. Écarts proposés

Rien de ceci n'est appliqué : à accepter ou refuser par l'auteur.

1. **Composant « roue à aubes » (`Kit.paddleWheel`).** Il n'existe pas. Il servirait aux scènes 10, 11, 12 et 16. Options : position (fonction de t), angle propre (fonction de t, en forme fermée), quatre aubes `--chalk`, une aube marquée `--fg`, flèches d'aubes facultatives (couleur `--u`), fantômes facultatifs (12.6). Raison : le même objet dans quatre scènes doit avoir le même dessin, et son angle doit rester une fonction pure du temps.
2. **Composant « compteur » (`Kit.readout`).** `Kit.chip` affiche un texte fixe. Il faut une valeur qui change à chaque image, en chiffres tabulaires (`.tnum`), avec un libellé mono, une position qui peut suivre un objet, un **séparateur décimal en virgule** (« 1,92 »), alors que `Kit.fmt` écrit un point, et une normalisation du zéro signé : toute valeur qui s'arrondit à zéro s'affiche « 0 », jamais « −0 ». Raison : le compteur est un motif de la bible ; il sert aux scènes 07, 08, 10, 11, 13, 14 et 15.
3. **Composant « cercle-sonde » (`Kit.probe`).** Cercle ou contour fermé en tirets `--chalk`, donné par une paramétrisation γ(s), avec ses parts de flèches perpendiculaires ou tangentes au bord (style plein ou en tirets selon le mode `flux` ou `circulation`), et le calcul par quadrature du flux ou de la circulation sur 256 points, pondéré par l'élément d'arc \|γ'(s)\| Δs, normale orientée vers l'extérieur, parcours trigonométrique, divisé ou non par l'aire, qui alimente le compteur. Raison : c'est l'objet central de l'épisode (scènes 01, 03, 04, 07 à 11, 13 à 15) ; le compteur doit afficher une valeur calculée, pas écrite à la main.
4. **Compression de longueur dans `Kit.arrows`.** Option `compress: {k, threshold}` : L(I) = k·I sous le seuil, k·I_s·(2 − I_s/I) au-dessus, fonction strictement croissante, continue et de pente continue, sans plafond dur ; et option `hole` (disque vide autour d'un point). Aujourd'hui la longueur est normalisée par le maximum de la grille, ce qui rend le tourbillon illisible (une flèche géante près du centre, toutes les autres invisibles), et un plafond dur ferait mentir « plus longue = plus forte ». Seuil I_s = 0,8 pour les scènes 12 et 13. Ce sera aussi le cas de la charge, dans ep02 (I_s = 1,2, ancien storyboard).
5. **Couleur `--fg-2` pour le champ de la charge.** Aucun plan de ep01 ne l'utilise : la charge et l'aimant sont passés dans ep02. Je garde la proposition pour la continuité : le thème n'a pas de couleur clé pour le champ électrique, et `--fg-2`, neutre, servirait à la charge et à l'aimant tant qu'il n'est pas nommé, pour ne pas donner la réponse en le colorant en `--b`. Ce n'est pas une couleur nouvelle, c'est un rôle nouveau pour un jeton existant. Raison : à trancher avant le storyboard de ep02.
6. **Dessins en perspective et pictogrammes.** Pas de composant ; code de scène en SVG ou canvas 2D. Perspective : plan incliné et flèches perpendiculaires (10.1 à 10.4), boule et ellipsoïde (8.6), rivière (8.7). Pictogrammes : robinet et table, vue de côté puis de dessus (3.2 à 3.4), évier et bonde (4.7, 4.8), seringues (8.8), cadran d'horloge (9.4), ⊙ et ⊗ (10.2, 10.3). Je propose de les factoriser plus tard dans `motifs.js` si un épisode suivant les reprend ; la sphère et les cubes reviendront dans ep02. Raison : tous restent dans les couleurs du thème (`--matter`, `--matter-dark`, `--u`, `--chalk`, `--muted`), mais aucun composant ne les dessine aujourd'hui.
7. **Fiches de vocabulaire.** Quatre mots seulement s'écrivent à l'écran (CHAMP VECTORIEL, FLUX, CIRCULATION, LIGNE DE COURANT), en mono capitales, au moment de leur définition (section 0). Ce n'est pas un composant nouveau (`Kit.chip` kind `plain` ou texte `.mono`), mais c'est une exception à la règle « aucun texte ne répète la voix », demandée par les lignes « écran » de la narration. À valider comme règle pour tout le film.

## 6. Journal des corrections

Relectures arbitrées par la session principale, tous les points retenus.

1. Notation : α, angle de l'aube marquée ou du rayon marqué, compté positivement dans le sens trigonométrique, vitesse $\dot\alpha$ ; 10.7 et 16.4 en $\dot\alpha_{\text{roue}} = \omega/2$, 10.11 en $\dot\alpha_{\text{disque}} = 1$ avec α défini sans mot par un arc entre un trait de référence fixe et l'aiguille, 10.12 et 10.14 en $\dot\alpha_{\text{roue}} = 1$, 11.14 en $\dot\alpha_{\text{roue}} = \omega/2 = -\tfrac12$ ; section 0, table de la section 3 et section 4 (points 6 et 7) réécrites ; la majuscule du domaine n'est plus employée.
2. Scène 09 : arc à contre-parcours corrigé, environ 154° du bord, soit 7 des 16 points (de 270° à 45°) ; 9.7 : « sept parts vont contre le parcours ».
3. Scène 07 : phase des seize points fixée à 11,25°, cinq parts entrantes franches à gauche (environ 3 px au plus court) ; seuil d'affichage ajouté en section 0 : aucun « + » ni « − » sur une part de moins de 2 px, d'où sept « − » et sept « + » à droite.
4. 3.4 : le jet tombe vers la table, en s'éloignant de l'œil ; son disque reste vide, sans point ni croix.
5. 3.4, 4.5, 4.8 : flèches des gerbes en 1/r, plus courtes loin du disque ; $\nabla\cdot\mathbf{u} > 0$ accroché au disque du jet, $\nabla\cdot\mathbf{u} < 0$ au disque de la bonde (via le point de 4.6).
6. 8.8 : seringue d'air vide ou à points épars, sans bulles ; aucune étiquette compressible ou incompressible.
7. 8.6 : demi-axes finaux $2 \times \tfrac{1}{\sqrt2} \times \tfrac{1}{\sqrt2}$, produit 1 à chaque image.
8. 8.5 : libellé des compteurs « FLUX ÷ AIRE ».
9. 1.2 et 1.3 : flèches des nœuds (π/2 ; 2π/3) et (π/2 ; π), sur la même colonne, vers la gauche, longueurs 0,5 et 1.
10. 10.12 : l'aube marquée « reste parallèle au rayon marqué ».
11. 12.5 : orbite de la roue dans le sens trigonométrique, à vitesse constante.
12. 12.14 : question présentée comme à calculer, « Γ = 2π » ajouté en `--muted` ; 16.8 : aucun signe d'égalité entre la miniature et l'énoncé de l'exercice 1 (b).
13. 1.10 : un seul emplacement de verdict, vide, en filet plein `--muted`, distinct des cadres en tirets de 1.5.
