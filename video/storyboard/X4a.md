# X4a · Ce que les instantanés permettent d'estimer (≈ 2 min 49 s)

**Objectif :** connaître le biais et la variance de l'estimateur de Rice et ses conditions de validité, la
borne sur la fréquence des inversions obtenue par niveaux, la raison pour laquelle les temps d'attente
exigent la dynamique, et ce que le second tour du palier 0 doit établir. **À retenir :** un générateur
d'instantanés estime et borne des fréquences, mais les temps d'attente demandent la dynamique.
**Niveau :** L4 → L5. **Version :** longue seulement (inséré après 09.6, avant chSOA2).

## X4.1 · La largeur de la bande · ≈ 27 s · reprend X4.1 (P1)
**On voit :** NIGHT. Lower-third « EXTENSION X4a · LEVEL 4–5 · AN ASIDE ». À gauche, le plan (D, vitesse)
de 05.2 rempli de points synthétiques ; la bande |D| < h, un curseur « strip half-width h ». À droite, un
graphe « estimate ÷ true rate », ligne « true rate » à 1.
**Animation :** sur « large » : la bande s'élargit ; à droite, la colonne de 30 estimations ambre dérive
vers le haut (« wide: bias ∝ h² »). Sur « étroite » : la bande se resserre, la colonne s'étale (« narrow:
variance ∝ 1/(N h) »). Sur « zéro virgule deux » : retour sur le nuage réel du modèle de Gissinger,
26 points dans la bande, « h = 0.2 ».
**Textes à l'écran (EN) :** « What snapshots can and cannot tell » · « strip · |D| < h » · « h (units of
σ) » · « 30 shoeboxes of N snapshots » · « wide: bias ∝ h² » · « narrow: variance ∝ 1/(N h) » · « the
three-dial experiment · Γ = 0.93 » · « in the strip: 26 of 8,000 snapshots » · « h = 0.2 » · puces
« illustration · synthetic Gaussian snapshots, true rate known · no data », « error bars assume
independent snapshots: generated ones are, one simulation's are not » · badge PROVED.
**Voix off :**
> Ce module précise ce qu'un générateur d'instantanés permet d'estimer sur les inversions. La formule de
> Rice s'applique sur une bande de largeur finie autour de zéro. Une bande large introduit un biais qui
> croît comme le carré de la largeur ; une bande étroite contient moins d'instantanés, et la variance
> augmente. L'expérience sur le modèle de Gissinger retenait une demi-largeur de zéro virgule deux.

## X4.1b · La limite d'une bande infiniment fine · ≈ 21 s · reprend X4.1 (P2–P3)
**On voit :** le curseur, la flèche « h → 0 ? ».
**Animation :** sur « densité régulière » : le nuage synthétique se fond en un dégradé continu. Sur
« cosinus » : il est remplacé par un anneau mince ; deux marques sur la trace du cosinus, « the formula:
two per period ». Sur « chaotique » : le nuage réel revient, fin et filamenteux ; sur « dépend de la
largeur » : la puce « the answer depends on h ».
**Textes à l'écran (EN) :** « h → 0 ? » · « D = cos(ωt + φ) » · « snapshots on a thin ring: no smooth
density » · « two crossings per period » · « the formula: two per period » · « deterministic chaos:
smooth density not guaranteed » · « the answer depends on h » · puce « tested on a 3-variable
deterministic system only ».
**Voix off :**
> La limite d'une bande infiniment fine suppose une densité régulière. Pour un cosinus, les instantanés
> occupent un anneau mince, et la formule donne pourtant deux passages par période. Pour une dynamique
> chaotique, cette densité n'est pas garantie ; sur le modèle de Gissinger, le résultat dépend de la
> largeur.

## X4.2 · Une borne par niveaux · ≈ 27 s · reprend X4.2 (variante en attente, P1–P2)
**On voit :** le rail monte de Level 4 à Level 5. En haut, une trace D(t) dessinée à la main (SCHEMATIC),
les lignes « +a », « −a », « D = 0 ».
**Animation :** sur « un niveau » : les lignes ±a s'écartent de zéro. Sur « son opposé » : une inversion
s'allume là où la trace passe sous −a. Sur « majore » : en bas, le cadre vide d'un graphe « crossings per
unit time » en fonction de a ; étiquettes « r_a » et « r ». Sur « oscillations » : un frémissement traverse
+a sans inverser, « wobble ». Sur « plateau » : une zone plate en pointillé.
**Textes à l'écran (EN) :** « Level 4 → Level 5 » · « a reversal: from above a to below −a » · « wobble:
crosses a, no reversal » · « r · reversals per unit time » · « r_a · crossings of the level a, either way
(Rice: snapshots + equations) » · « plateau (Conjecture 2.33) » · « SCHEMATIC · the conjecture's picture,
no data » · « DATA · X4_RICE_LEVELS · AWAITING » · badge CONJECTURE, confiance moyenne.
**Voix off :**
> Une inversion part d'au-dessus d'un niveau et finit au-dessous de son opposé. La fréquence de
> franchissement de ce niveau, estimée par la formule de Rice, majore donc la fréquence des inversions.
> Les oscillations autour du niveau relâchent cette borne. Selon une conjecture du plan de thèse, la borne
> est presque atteinte sur un plateau de niveaux lorsqu'une inversion dure bien plus qu'une oscillation.

## X4.2b · L'hypothèse de travail sur le plateau · ≈ 16 s · reprend X4.2 (cases du siège)
**On voit :** le graphe vide et ses deux ancres réelles (silhouette de |D| à Γ = 0,9, point du comptage à
a = 0) ; à droite, les quatre cases du siège.
**Animation :** sur « hypothèse de travail » : case THE BET, bande « within 30 % of r » autour du plateau.
Sur « moyenne » : CONFIDENCE. Sur « largeur » : la case ASK s'allume, la bande du plateau clignote.
**Textes à l'écran (EN) :** « where snapshots sit · |D| at Γ = 0.9 » · « a = 0: every zero crossing,
counted » · « within 30 % of r » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK BEFORE WE COMPUTE ·
puce « bet written before the data · tier-0 campaign: up to 10⁶ snapshots per setting, 3 seeds, about
10³ CPU hours (assumption) ».
**Voix off :**
> L'hypothèse de travail est un écart inférieur à trente pour cent sur ce plateau, au palier 0. La
> confiance est moyenne : la borne est démontrée, le plateau ne l'est pas, et sa largeur requise n'est pas
> fixée.

**Note :** variante « résultat » (v2 X4.2.r1–r8) à réécrire au même registre.

## X4.3 · Les temps d'attente exigent la dynamique · ≈ 30 s · reprend X4.3 (P1–P3)
**On voit :** deux signaux superposés, « one frequency » et « two frequencies », et deux petits nuages
(D, Ḋ) ; puis un histogramme ambre des attentes entre inversions, échelle logarithmique, à Γ = 0,9.
**Animation :** sur « même loi » : les deux nuages se superposent exactement ; jauge « Rice rate: the
same ». Sur « régulier » / « inégaux » : des marques sur chaque passage par zéro, régulières en haut,
irrégulières en bas. Sur « peigne » : une rangée de pics serrés à gauche de l'histogramme ; sur
« exponentielle » : la queue se pose sur une droite pointillée ; lower-third de référence Gissinger 2012.
Sur « états générés » : vignette du plan (Q, D), couloir |D| < 0,25 ; de courtes trajectoires partent de
quelques points.
**Textes à l'écran (EN) :** « same snapshot law » · « Rice rate: the same » · « metronome » · « uneven
gaps » · « wait between flips (time units) » · « count (log scale) » · « comb: quantized short waits
(unstable orbits) » · « memoryless tail · exponential » · « corridor · |D| < 0.25 » · « short runs of the
true equations, from generated states » · puces « illustration · synthetic Gaussian signals »,
« illustration · live integration of the model · shape as in Gissinger 2012, Fig. 12 », « open question ·
PhD plan, T:131 » · badge PROVED.
**Voix off :**
> Deux signaux aléatoires réguliers peuvent avoir la même loi d'instantanés, donc la même fréquence de
> Rice, l'un franchissant zéro à intervalle régulier, l'autre à intervalles inégaux. Or les attentes entre
> inversions ont une forme précise : selon Gissinger en 2012, un peigne d'attentes courtes, puis une queue
> exponentielle. Cette forme exige la dynamique. Son estimation par de courtes simulations lancées depuis
> des états générés n'a pas encore été établie.

## X4.5 · Le second tour du palier 0 · ≈ 22 s · reprend X4.5 (variante en attente, P1–P2)
**On voit :** l'escalier en haut à gauche, première marche allumée, puce « second round ». Trois tuiles
apparaissent l'une après l'autre, puis quatre voyants gris.
**Animation :** sur « trois graines » : tuile 1, « seed 0 », « seed 1 » pleins, « seed 2 · awaiting » en
pointillé. Sur « second modèle » : tuile 2, la carte DQVU et un cylindre VKS gris ; lower-third de
référence Bousquet et al. 2026. Sur « turbines » : tuile 3, un point vermillon se reflète, Γ passe de + à
−. Sur « quatre critères » : les tuiles s'effacent, quatre voyants s'étiquettent au fil des mots.
**Textes à l'écran (EN) :** « tier 0 · three numbers » · « second round » · « first round: 2 seeds » ·
« DQVU · Bousquet et al. 2026 » · « reduced model of VKS reversal simulations » · « no DQVU code in this
repository yet » · « joint mirror R_π · the impeller swap » · « R_π: D → −D, V → −V and Γ → −Γ » · « tier
0 · success criteria of the PhD plan » · quatre voyants (mirror, crowd laws not enforced, Rice, level
bound) · « DATA · X4_TIER0 · AWAITING » · badge CONJECTURE, confiance moyenne.
**Voix off :**
> Le palier 0 prévoit un second tour : trois graines, un second modèle réduit tiré de simulations de VKS,
> et la symétrie d'échange des turbines, qui change aussi le signe de Gamma. Quatre critères sont fixés :
> la symétrie, les lois non imposées, la formule de Rice et la borne par niveaux.

## X4.5b · Un critère à la limite du bruit · ≈ 26 s · reprend X4.5 (cases du siège)
**On voit :** les quatre voyants, chacun avec sa valeur du premier tour en petit.
**Animation :** sur « un virgule quatre-vingt-dix-huit » : le deuxième voyant affiche « ×1.98 » contre une
barre à 2. Sur « plancher » : le premier voyant ; une courbe en cloche des écarts d'un modèle exactement
symétrique, la ligne du plancher en son milieu, moitié droite hachurée. Sur « test statistique » : case
ASK. Sur « état de l'art » : tout recule, le cadre s'élargit.
**Textes à l'écran (EN) :** « first round: ×1.98 (0.0113 vs 0.0224) » · « first round, 2 seeds: 0.0037 to
0.0048 vs floor 0.0040 » · « first round, seed 0: cumulative 14 % far from the threshold (pointwise up to
65 %), 42 % near » · « not measured yet » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK · puces
« first round = E1 · 2 seeds instead of the 3 planned », « bet written before the data · tier 0:
perceptrons on CPU, simulations about 10³ CPU hours (assumption) ».
**Voix off :**
> L'hypothèse de travail est une nouvelle division par deux des résidus non imposés ; au premier tour, le
> facteur était de un virgule quatre-vingt-dix-huit. La confiance est moyenne. Un modèle exactement
> symétrique dépasse le plancher de bruit presque une fois sur deux ; le recours à un test statistique
> n'est pas décidé. Le module suivant revient à l'état de l'art.

**Note :** variante « résultat » (v2 X4.5.r1–r8) à réécrire au même registre.

**Durée totale estimée :** 2 min 49 s · **Mots :** ≈ 390

**Points à valider :**
1. La carte X4a.Q (Q14 : viser aussi les temps d'attente pour VKS) est supprimée ; la question passe dans
   l'unité finale « Ouvertures ».
2. Les questions des cases ASK de X4.2 (largeur du plateau) et X4.5 (test statistique) sont énoncées
   comme des choix non arrêtés, et restent à l'écran.
3. « Pile ou face » et l'image du métronome sont retirées de la voix ; « métronome » reste une étiquette.
4. « Le plancher, c'est sa moyenne » (R:832) n'est plus dit ; « presque une fois sur deux » arrondit
   0,42–0,45 comme en v3.
5. La transition finale vise chSOA2 ; à harmoniser avec l'ouverture v4 de SOA2.1.
