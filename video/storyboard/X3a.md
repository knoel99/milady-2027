# X3a · Les lois de foule, de plus près (≈ 4 min 27 s)

**Objectif :** savoir comment on mesure l'écart entre deux foules, comprendre la repondération par
inclinaison exponentielle et pourquoi elle ne peut pas créer de masse, puis lire le détail par valeur
d'êta. **À retenir :** repondérer ne fait pas visiter les endroits où le modèle n'est jamais allé.
**Niveau :** L4. **Version :** longue seulement (inséré après X2, avant ch09).

## X3.0 · Une cousine du tas de sable · ≈ 27 s · reprend X3.0
**On voit :** toujours le papier de X2. Lower-third « EXTENSION · X3a · Crowd laws, deeper ». En haut à
gauche, le petit tas de sable de 06.5, à l'encre.
**Animation :** sur « des paires » : le tas glisse hors du cadre, deux foules de points apparaissent,
noire (simulée) et violette cerclée (générée), qui se chevauchent d'un tiers. Sur « un instantané » : un
point violet grossit, étiquette, puis reprend sa taille.
**Textes à l'écran (EN) :** « distribution distance » · « simulated crowd » · « generated crowd » · « one
dot = one snapshot » · puces « technical name: energy distance · REFERENCE · Székely & Rizzo 2013 »,
« SCHEMATIC · two toy crowds » · badge CONTEXT.
**Voix off :**
> Encore un détour, parce que les lois de foule posent deux questions très pratiques. Comment mesurer
> qu'une foule ressemble à une autre ? Et peut-on corriger une foule après coup ?
>
> D'abord, la mesure. Au chapitre 6, une distance entre distributions, c'était du sable à déplacer. Les
> expériences en utilisent surtout une cousine, construite à partir de paires. Chaque point, ici, c'est un
> instantané.

## X3.0b · Les paires · ≈ 20 s · reprend X3.0 (P2)
**On voit :** les deux foules, l'équation en bandeau au-dessus.
**Animation :** sur « faites la moyenne, et doublez-la » : des
traits fins relient des points d'une foule à l'autre, le premier terme de la formule s'allume « ×2 ». Sur
« à l'intérieur » : traits à l'intérieur de chaque foule, les deux termes soustraits s'allument. Sur
« Zéro » : les deux foules glissent l'une sur l'autre et se superposent ; une jauge ambre tombe… et
s'arrête un peu au-dessus de zéro, sur une ligne pointillée « noise floor ».
**Textes à l'écran (EN) :** formule de la distance d'énergie (trois termes) · « across the two crowds ·
×2 » · « within each crowd » · « 0 ⇔ same law » · « noise floor ».
**Voix off :**
> Prenez toutes les distances entre un point d'une foule et un point de l'autre, faites la moyenne, et
> doublez-la. Retirez la distance moyenne à l'intérieur de chaque foule. Zéro : même loi. Et comme pour le
> sable, on compare au plancher de bruit, jamais à zéro.

**Note :** « on compare au plancher de bruit, jamais à zéro » vient de la couche formule v2 (R:723), dit
ici à l'oral pour relier à 06.5.

## X3.1 · Redresser un sondage · ≈ 26 s · reprend X3.1 (P1–P2)
**On voit :** changement d'encre PAPER → NIGHT : la foule violette s'écrase sur un axe horizontal et
devient une rangée de points (raccord, pas de fondu). Axe ambre « energy change of one snapshot · r =
dE/dt », histogramme violet au-dessus, vraie densité en gris pointillé.
**Animation :** sur « rate sa moyenne » : deux triangles sous l'axe, violet sur la moyenne du modèle,
gris sur zéro, un écart entre les deux. Sur « On ne bouge aucun instantané » : les points restent en
place, seule leur taille change, l'histogramme se reprofile, le triangle violet glisse vers zéro. Sur
« Beaucoup de pondérations » : trois façons de repondérer défilent (« drop the top », « linear »,
« w ∝ exp(β r) ») avec une petite barre de coût chacune ; la troisième est la plus courte.
**Textes à l'écran (EN) :** « truth » · « model q » · « target: average 0 (energy budget) » · « misses the
target » · « no snapshot moves · only its weight » · « drop the top », « linear », « w ∝ exp(β r) » ·
« cost: how much the crowd is distorted » · « I-projection » · puces « SCHEMATIC · toy law of the
report's interactive diagram », « REFERENCE · Csiszár 1975 » · badge PROVED.
**Voix off :**
> Maintenant, corriger après coup. La foule du modèle rate sa moyenne cible : ici, son bilan d'énergie
> penche du mauvais côté. L'idée : on ne bouge aucun instantané. On change seulement combien chacun
> compte. Comme un sondage qu'on redresse : on ne réinterroge personne, on repondère.
>
> Beaucoup de pondérations atteignent la cible. La moins déformante s'appelle une inclinaison
> exponentielle. Dans le jargon : une I-projection.

## X3.1b · Le pied de la perpendiculaire · ≈ 25 s · reprend X3.1 (P3)
**On voit :** un encart géométrique remplace l'axe : un point « model q », une droite « every crowd with
average 0 ».
**Animation :** sur « une droite » : la droite se trace. Sur « le pied de la perpendiculaire » : une
perpendiculaire descend du point q, son pied s'allume « tilted q* ». Sur « n'importe quelle autre
correction » : un autre point p sur la droite ; un triangle rectangle se ferme, les trois côtés
s'étiquettent « cost of q* », « extra », « cost of p ». Sur « rien ne bouge » : retour à l'axe ; une
zone sans aucun point se hachure en gris : « no dot here ».
**Textes à l'écran (EN) :** « every crowd with average 0 » · « model q » · « tilted q* » · « another fix
p » · « cost of q* », « extra », « cost of p » · « no dot here: no mass, before or after ».
**Voix off :**
> Une image. Représentez chaque foule par un point. Celles qui ont la bonne moyenne forment une droite. La
> foule inclinée, c'est le pied de la perpendiculaire. N'importe quelle autre correction paie le même
> coût, plus un supplément, comme dans Pythagore.
>
> Et rien ne bouge : la foule inclinée ne vit que là où la foule du modèle était déjà.

## X3.2 · Le sondage qui rétrécit · ≈ 29 s · reprend X3.2 (P1–P2)
**On voit :** à gauche, un « sondage » de 20 points violets en grille 4 × 5 ; sous lui, un compteur ambre
« effective sample size » à 20. À droite, un axe vert logarithmique des onze valeurs d'êta.
**Animation :** sur « Poids égaux » : le compteur reste à 20. Sur « un poids géant » : un point gonfle,
les autres deviennent de simples contours, le compteur dégringole jusqu'à 1. Sur « la nappe plane » : le
sondage devient une icône ; onze barres ambre poussent sur l'axe, une ligne pointillée grise « one
snapshot: the minimum » en bas. Sur « quatre-vingt-dix-neuf » : une barre s'allume, tout en haut. Sur
« cinq cents » : trois barres collées au plancher s'allument ensemble.
**Textes à l'écran (EN) :** « a poll of 20 » · « effective sample size » · « equal weights: the whole
crowd » · « one giant weight: one person » · « ESS/N of the tilt · 500 snapshots per η (half b) » · « the
poll keeps 99 % » · « one snapshot in 500 » · puces « SCHEMATIC · a poll of 20 », « GENERATED · V4, one
seed », « mean over the 11 values: 0.29 », « REFERENCE · effective sample size: Kish 1965 » · badge
MEASURED.
**Voix off :**
> Bon, combien reste-t-il d'une foule repondérée ? C'est la taille effective de l'échantillon qui le dit.
> Poids égaux : toute la foule compte. Un poids géant : il ne reste qu'une personne, qui parle pour tout le
> monde.
>
> Sur la nappe plane, à la plus petite valeur de test d'êta, le sondage garde quatre-vingt-dix-neuf pour
> cent de sa foule. Aux trois plus grandes, il s'effondre : un instantané effectif sur cinq cents.

## X3.2b · Il s'effondre là où il faudrait corriger · ≈ 25 s · reprend X3.2 (P3–P4)
**On voit :** les mêmes barres.
**Animation :** sur « Classez » : les barres se réordonnent selon l'erreur de bilan du modèle de base
(nouvel axe « how far the base model's energy budget was off ») ; elles forment un escalier descendant
presque parfait (une seule paire échangée, petite marque). Sur « presque rien à corriger » : la gauche
s'éclaire ; sur « il s'effondre » : la droite. Sur « trois cadrans » : vignette de la citation du
rapport.
**Textes à l'écran (EN) :** « how far the base model's energy budget was off » · « little to fix » · « much
to fix: the poll collapses » · « REPORT · E1, model C, seed 0, Γ = 0.85 » · « ESS/N 0.67 · one weight 33×
the mean · no distribution improved » · puces « the tilt fixes three budgets: energy, cross helicity,
⟨A²⟩ », « rank order: one swap (η = 0.004 and 0.0067) ».
**Voix off :**
> Maintenant, classez les réglages selon l'erreur de bilan du modèle. Le sondage rétrécit presque dans le
> même ordre. Là où il survit, il n'y avait presque rien à corriger. Là où il fallait beaucoup corriger,
> il s'effondre.
>
> Sur les trois cadrans, même verdict : la repondération n'a amélioré aucune foule. Un seul instantané
> pesait trente-trois fois la moyenne.

## X3.3 · Le pont vide · ≈ 18 s · reprend X3.3 (P1, « predict »)
**On voit :** le nuage de 05.2, mais en violet (modèle C à Γ = 0,93) : les points répartis selon D, la
bande |D| < h à la craie. À droite, la jauge ambre du compteur de péage.
**Animation :** sur « ne visite jamais le pont » : un interrupteur « missing support » bascule ; les points
de la bande s'effacent, la bande se hachure, l'aiguille de la jauge tombe à zéro. Pastille PREDICT, deux
réponses A et B. Silence de 2 s.
**Textes à l'écran (EN) :** « D · dipole » · « the bridge · |D| < h » · « missing support » · « crossing
rate read in the strip » · « PREDICT » · « Can reweighting bring back the crossing rate? » · « A · yes,
with big enough weights » · « B · no » · puces « GENERATED · model C, Γ = 0.93 », « SCHEMATIC · the bridge
removed by hand » · badge PROVED.
**Voix off :**
> Poussons l'idée jusqu'au bout. Imaginez un modèle qui ne visite jamais le pont entre les deux polarités,
> là où se font tous les passages. Est-ce que la repondération peut ramener la fréquence des passages ?

## X3.3b · Zéro fois n'importe quoi · ≈ 37 s · reprend X3.3 (P2–P3)
**On voit :** la même bande vide.
**Animation :** sur « Non » : la réponse B s'allume. Sur « zéro » : « 0 × any weight = 0 » s'écrit dans la
bande. Sur « si vous forcez » : les points au bord de la bande gonflent l'un après l'autre, le compteur de
taille effective plonge ; l'aiguille de la jauge ne bouge pas. Sur « la phrase » : bandeau « reweighting
cannot create mass ». Sur « table des risques » : une fiche « PhD plan · risk table » glisse, une ligne
soulignée.
**Textes à l'écran (EN) :** « empty strip: 0 × any weight = 0 » · « still 0 » · « weights pile up at the
edge » · « reweighting cannot create mass » · « PhD plan · risk table » · « tilting alone is not a
fallback ».
**Voix off :**
> Non. La formule de Rice lit la fréquence dans la bande, et la bande est vide. Zéro, multiplié par
> n'importe quel poids, ça fait zéro. Et si vous forcez, tout le poids s'empile sur quelques instantanés
> du bord.
>
> Retenez la phrase : repondérer ne fait pas visiter les endroits où le modèle n'est jamais allé. Un
> sondage ne fera jamais parler un village où personne n'a été interrogé. D'ailleurs, la table des
> risques du plan de thèse le dit aussi : la repondération seule n'est pas une solution de repli.

## X3.4 · Valeur par valeur · ≈ 31 s · reprend X3.4
**On voit :** même cadre que les barres de X3.2. L'axe vert ne garde que les cinq valeurs de test d'êta ;
pour chacune, trois barres : V4 (violet pointillé), témoin (gris), V5 avec la perte sur la foule (ambre).
Ligne pointillée « honest noise floor ».
**Animation :** sur « la plus grande » : le groupe de droite s'allume, les autres pâlissent ; accolade
« dissipates 2.2× the energy fed in ». Sur « sept virgule sept à deux virgule deux » : la barre V5
redescend de la hauteur du témoin à la sienne. Sur « la plus petite » : le groupe de gauche s'allume,
« no change ». Sur « témoin » : les barres grises clignotent, « stays put ».
**Textes à l'écran (EN) :** « distribution distance · test values of η (never seen) » · « V4 · base » ·
« control · same length, no loss » · « V5 · crowd loss » · « dissipates 2.2× the energy fed in » ·
« 7.7 → 2.2 » · « no change » · « stays put » · puces « GENERATED · one seed per variant », « interpolation only », « part of the gain could be a global
rescaling of the energy level: argued against, not ruled out » · badge MEASURED.
**Voix off :**
> Et l'autre route, celle qui change l'entraînement ? Regardons chaque valeur de test d'êta. À la plus
> grande, les instantanés du modèle de base dissipent, en moyenne, plus de deux fois l'énergie injectée.
> La perte sur la foule fait tomber la distance de sept virgule sept à deux virgule deux. À la plus
> petite, le modèle était déjà bon : rien ne change. Et le témoin, entraîné aussi longtemps sans la perte,
> ne bouge pas.

## X3.4b · Les poids n'y arrivaient pas · ≈ 16 s · reprend X3.4 (P3)
**On voit :** les groupes de barres ; sous eux, la rangée de barres de X3.2.
**Animation :** sur « les mêmes valeurs » : la rangée de X3.2 revient en fondu sous les groupes, les
effondrements du sondage alignés avec les plus gros gains ; un trait vertical relie chaque paire. Sur
« Une seule graine » : la puce « GENERATED · one seed per variant » clignote. Sur « Fin du détour » : tout
pâlit, une petite icône du compteur de péage apparaît au centre.
**Textes à l'écran (EN) :** « ESS/N of the tilt (X3.2) » · « the loss moves the crowd · weights cannot ».
**Voix off :**
> Et regardez : ce sont les mêmes valeurs que celles où le sondage s'effondrait. L'entraînement a
> déplacé la foule ; les poids n'y arrivaient pas. Une seule graine, quand même.
>
> Fin du détour. Retour au compteur de péage.

## X3a.Q · Question pour les encadrants · ≈ 13 s · reprend X3a.Q
**On voit :** la carte « ASK · Q12 · X3A · S. Cheng / D. Lucor » ; en fond pâle, des barres groupées.
**Animation :** soulignés au stylo sur « fallback » et « reweighting ».
**Textes à l'écran (EN) :** texte de Q12 (registre), catégorie FRAMING.
**Voix off :**
> Question pour les encadrants : si la perte sur la foule échoue, quel est le plan de repli… puisque la
> repondération échoue justement là où le modèle est mauvais ?

**Durée totale estimée :** 4 min 27 s · **Mots :** ≈ 610

**Points à valider :**
1. Le sondage sert de fil rouge (X3.1 à X3.3) et s'arrête explicitement : « un sondage ne fera jamais
   parler un village où personne n'a été interrogé ».
2. « Et l'autre route, celle qui change l'entraînement ? » ouvre X3.4 : phrase nouvelle, tirée de R:462
   (deux routes : incliner après coup, ou modifier l'entraînement).
3. Le passage de main (« Retour au compteur de péage ») précède la carte Q12 ; 09.1 enchaîne sur « Le
   compteur de péage est de retour », ce qui fait un léger écho voulu. À couper dans 09.1 si c'est trop.
4. La note du visuel v2 de X3a.Q (« suivi de ch08.Q ») est périmée : dans l'ordre actuel, c'est 09.1 qui
   suit.
