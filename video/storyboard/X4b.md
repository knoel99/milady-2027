# X4b · Seuils raides et branches (≈ 45 s)

**Objectif :** connaître la borne en racine carrée près d'un seuil supercritique et la conjecture du
conditionnement par branche près d'un seuil sous-critique, ainsi que la simulation qui la testerait.
**À retenir :** près d'un seuil sous-critique, indiquer au générateur la branche suivie pourrait réduire
l'erreur de lissage ; c'est une hypothèse de travail, et le balayage descendant qui la testerait n'est pas
encore configuré.
**Niveau :** L5. **Version :** longue seulement (inséré après 10.5, avant 10.6).

## X4.4 · Seuil supercritique, seuil sous-critique · ≈ 27 s · reprend X4.4 (P1–P2)
**On voit :** NIGHT. Lower-third « EXTENSION X4b · LEVEL 5 · AN ASIDE ». En haut à gauche, la tranche
Taylor-Green de 10.5 en gris. À gauche, un graphe qualitatif : « Rm » en abscisse (below, threshold,
above), « field strength » en ordonnée.
**Animation :** sur « racine carrée » : la courbe vermillon part du seuil, verticale au départ. Sur
« arrondit » : une courbe violette lisse coupe le coin, l'écart hachuré. Sur « plus souple » : une seconde
courbe violette, plus proche du coin, ondule ailleurs sur l'axe. Sur « sous-critique » : le titre change ;
deux branches vermillon se chevauchent sur une zone ; une flèche monte (allumage tardif), une autre
redescend le long de la branche haute ; repères « on: 206 », « held to: 70 » ; lower-third Ponty et al.
2007. Sur « mélange » : une courbe violette passe entre les deux branches.
**Textes à l'écran (EN) :** « Taylor-Green · knob: Rm » · « gentle (supercritical) threshold » · « truth:
a square root » · « stiff machine: rounds the corner » · « supple machine: smaller error, narrower window,
jumpy » · « subcritical threshold: two states » · « sweep up: switches on late » · « sweep down: holds
on » · « on: 206 » · « held to: 70 » · « knob only: a blend, weights set by the protocol » · puces
« SCHEMATIC · normal forms, no data », « Ponty et al. 2007 (PRL 99, 224501): on at Rm_c = 206 (R_V = 563),
held down to Rm = 70 · Reynolds numbers on other scales » · badge CONJECTURE, confiance faible (note :
Prop. 2.36 démontrée).
**Voix off :**
> Ce module traite de l'erreur d'un générateur au voisinage d'un seuil. Près d'un seuil supercritique,
> l'amplitude croît comme une racine carrée. Un générateur régulier arrondit ce coin ; un générateur plus souple réduit l'erreur, mais devient sensible au
> paramètre partout. Près d'un seuil sous-critique, deux états coexistent : selon Ponty et ses coauteurs
> en 2007, la dynamo de Taylor-Green se maintient jusqu'à environ un tiers de son seuil.

## X4.4b · Le conditionnement par branche · ≈ 18 s · reprend X4.4 (P3–P4, siège en attente)
**On voit :** à droite, le cadre vide d'une jauge « error without branch ÷ error with branch, at the
threshold », zone « halved or better » ombrée ; les quatre cases du siège.
**Animation :** sur « branche » : étiquettes « b = on », « b = off » sur les branches ; la courbe violette se
dédouble et suit chacune. Sur « faible » : CONFIDENCE. Sur « balayage descendant » : la flèche descendante
se grise, la puce de configuration apparaît. Sur « reprend » : la tranche Taylor-Green revient au centre.
**Textes à l'écran (EN) :** « told its branch » · « b = on », « b = off » · « halved or better · criterion
(d) » · « DATA · X4_BRANCH · AWAITING » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK · puce
« configured runs all start from a 10⁻³ seed: no downward sweep (palier2_tg3d.yaml:34) ».
**Voix off :**
> Conditionné sur ce seul paramètre, un générateur mélange les deux états. Selon l'hypothèse de travail
> du plan de thèse, indiquer la branche divise au moins par deux l'erreur au seuil. La confiance est
> faible ; aucun balayage descendant n'est configuré. Le chapitre reprend son fil principal.

**Note :** variante « résultat » (v2 X4.4.r1–r8) à réécrire au même registre.

**Durée totale estimée :** 45 s · **Mots :** ≈ 105

**Points à valider :**
1. L'analogie du vélo et le rappel de la plaque rigide de 09.3 sont retirés.
2. La raison de la confiance faible (stabilité statistique le long des branches non démontrée en
   turbulence) n'est plus dite, faute de temps ; elle reste dans la note de badge et les sources.
3. « Environ un tiers » : 70 / 206 (Ponty et al. 2007, déjà sourcé) ; l'échelle des Reynolds diffère de
   celle du projet, dit sur la puce seulement.
4. La question de la case ASK (à partir de quelles simulations saturées, jusqu'où descendre) n'est plus
   dite ; elle reste à l'écran.
