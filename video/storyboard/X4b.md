# X4b · Pentes raides et branches (≈ 1 min 34 s)

**Objectif :** connaître la borne en racine carrée près d'un seuil doux, la conjecture du
conditionnement par branche près d'un seuil sous-critique, et la simulation qui la testerait. **À
retenir :** près d'un seuil sous-critique, dire à la machine sur quelle branche elle est pourrait
supprimer l'erreur de lissage ; c'est un pari, et le balayage descendant qui le testerait n'est pas
encore configuré.
**Niveau :** L5. **Version :** longue seulement (inséré après 10.5, avant 10.6).

## X4.4 · Le seuil doux · ≈ 32 s · reprend X4.4 (P1, cadrage revu)
**On voit :** NIGHT. Lower-third « EXTENSION X4b · LEVEL 5 · AN ASIDE ». En haut à gauche, la tranche
Taylor-Green de 10.5 en fantôme gris. À gauche, un graphe qualitatif : « Rm » en abscisse (below,
threshold, above), « field strength » en ordonnée. En coin, la petite plaque rigide de 09.3.
**Animation :** sur « la plaque rigide » : la vignette de 09.3 pulse une fois. Sur « racine carrée » : la
vraie courbe vermillon part du seuil, verticale au départ, puis s'infléchit. Sur « arrondit le virage » :
une courbe violette lisse coupe le coin ; l'écart se hachure. Sur « se trompe moins » : une seconde courbe
violette, plus près du coin… mais qui ondule ailleurs sur tout l'axe.
**Textes à l'écran (EN) :** « Taylor-Green · knob: Rm » · « gentle (supercritical) threshold » ·
« truth: a square root » · « stiff machine: rounds the corner » · « supple machine: smaller error,
narrower window, jumpy » · puce « SCHEMATIC · normal forms, no data » · badge CONJECTURE, confiance
faible (note : Prop. 2.36 démontrée).
**Voix off :**
> Petit aparté, puisqu'on parle de seuil. Rappelez-vous la plaque rigide du chapitre 9 : devant une pente
> raide, une machine trop lisse arrondit. Il y avait deux échappatoires : être très souple, ou savoir dans
> quel état se trouve le système. Les voici.
>
> Près d'un seuil doux, la vérité monte comme une racine carrée : verticale au départ. Une machine raide
> arrondit le virage. Une machine souple se trompe moins… mais devient nerveuse partout. Ça, c'est
> démontré.

## X4.4b · Deux états à la fois · ≈ 30 s · reprend X4.4 (P2)
**On voit :** le graphe change de titre : « subcritical threshold: two states ».
**Animation :** sur « deux états coexistent » : deux branches vermillon, une allumée, une éteinte, qui se
chevauchent sur une zone. Sur « une fois allumée » : une flèche monte en balayage (allumage tardif), une
autre redescend le long de la branche haute et tient bien plus bas ; deux repères « on: 206 », « held to:
70 » ; lower-third de référence Ponty et al. 2007. Sur « le vélo » : petite icône de vélo qui démarre,
puis roule sur le plat. Sur « elle mélange » : une courbe violette passe au milieu, entre les deux
branches.
**Textes à l'écran (EN) :** « sweep up: switches on late » · « sweep down: holds on » · « on: 206 » ·
« held to: 70 » · « held down to about a third of the onset » · « knob only: a blend, weights set by the
protocol » · puce « Ponty et al. 2007 (PRL 99, 224501): on at Rm_c = 206 (R_V = 563), held down to
Rm = 70 · Reynolds numbers on other scales ».
**Voix off :**
> Près d'un seuil sous-critique, en revanche, deux états coexistent. Dans des simulations publiées de
> Taylor-Green, une dynamo, une fois allumée, a tenu jusqu'à environ un tiers de son seuil d'allumage. Un
> peu comme un vélo : il faut un bon coup de pédale pour démarrer, mais une fois lancé, un effort bien
> plus faible suffit.
>
> Si on ne donne à la machine que la position du bouton, elle mélange les deux états.

## X4.4c · Le pari de la branche · ≈ 32 s · reprend X4.4 (P3–P4, siège vide)
**On voit :** à droite, le cadre vide d'une jauge « error without branch ÷ error with branch, at the
threshold », la zone « halved or better » ombrée ; les quatre cases du siège.
**Animation :** sur « sur quelle branche » : deux petites étiquettes « b = on », « b = off » se collent
sur les branches, la courbe violette se dédouble et suit chacune. Sur « Confiance : faible » : CONFIDENCE.
Sur « aucun balayage descendant » : la flèche descendante du plan précédent se grise, la puce de
configuration apparaît. Sur « Fin de l'aparté » : le fantôme Taylor-Green grandit et reprend le centre.
**Textes à l'écran (EN) :** « told its branch » · « b = on », « b = off » · « halved or better · criterion
(d) » · « DATA · X4_BRANCH · AWAITING » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK · puce
« configured runs all start from a 10⁻³ seed: no downward sweep (palier2_tg3d.yaml:34) ».
**Voix off :**
> Le pari du plan de thèse : dites-lui sur quelle branche elle est, et son erreur au seuil est au moins
> divisée par deux.
>
> Confiance : faible. La stabilité statistique le long des branches n'est pas démontrée en turbulence. Et
> aucun balayage descendant n'est configuré. Question à poser : à partir de quelles simulations saturées,
> et jusqu'où descendre ?
>
> Fin de l'aparté. Retour à la boîte en trois dimensions, et à ce qui, là-dedans, ne demande aucun pari.

**Note :** variante « résultat » (v2 X4.4.r1–r8) à réécrire au même ton plus tard.

**Durée totale estimée :** 1 min 34 s · **Mots :** ≈ 220

**Points à valider :**
1. L'analogie du vélo (hystérésis) est ajoutée ; elle s'arrête à l'idée « démarrer coûte plus que
   continuer » et ne dit rien des mécanismes.
2. « Environ un tiers » : 70 / 206 (Ponty et al. 2007, déjà sourcé en v2) ; l'échelle des Reynolds est
   différente de celle du projet, dit sur la puce seulement.
3. Le rappel de 09.3 (« deux échappatoires ») reprend la phrase du cœur « Unless it is very supple, or
   told which state the system is in » : à garder seulement si le storyboard de ch09 la garde.
