# X3a · Les lois statistiques : distance et repondération (≈ 2 min 52 s)

**Objectif :** définir la distance entre distributions employée dans les expériences, comprendre
l'inclinaison exponentielle comme une I-projection et pourquoi elle ne crée pas de masse, puis lire le
détail par valeur de la diffusivité magnétique. **À retenir :** une repondération ne peut pas atteindre les
régions que le modèle ne visite pas.
**Niveau :** L4. **Version :** longue seulement (inséré après X2, avant ch09).

## X3.0 · La distance d'énergie · ≈ 30 s · reprend X3.0 (P1–P2)
**On voit :** papier de X2. Lower-third « EXTENSION · X3a · Crowd laws, deeper ». En haut à gauche, le
petit tas de sable de 06.5, à l'encre ; il sort du cadre, deux nuages de points apparaissent, noir
(simulé) et violet cerclé (généré), qui se chevauchent d'un tiers. La formule en bandeau au-dessus.
**Animation :** sur « paires » : des traits fins relient des points d'un nuage à l'autre ; le premier
terme de la formule s'allume, « ×2 ». Sur « à l'intérieur » : traits à l'intérieur de chaque nuage, les
deux termes soustraits s'allument. Sur « nul » : les nuages se superposent ; une jauge ambre descend et
s'arrête un peu au-dessus de zéro, sur la ligne pointillée « noise floor ».
**Textes à l'écran (EN) :** « distribution distance » · « simulated crowd » · « generated crowd » · « one
dot = one snapshot » · formule de la distance d'énergie (trois termes) · « across the two crowds · ×2 » ·
« within each crowd » · « 0 ⇔ same law » · « noise floor » · puces « technical name: energy distance ·
REFERENCE · Székely & Rizzo 2013 », « SCHEMATIC · two toy crowds » · badge CONTEXT.
**Voix off :**
> Ce module précise deux outils liés aux lois statistiques : la distance entre distributions et la
> repondération. Les expériences emploient surtout la distance d'énergie, définie par Székely et Rizzo.
> Elle double la distance moyenne entre les points des deux distributions, puis retranche la distance
> moyenne à l'intérieur de chacune. Elle est nulle si et seulement si les lois sont égales ; en pratique,
> elle est comparée au plancher de bruit.

**Note :** le passage du papier à la nuit (T3) a lieu au début de X3.1, comme en v2.

## X3.1 · L'inclinaison exponentielle · ≈ 20 s · reprend X3.1 (P1–P2)
**On voit :** changement d'encre PAPER → NIGHT : le nuage violet s'écrase sur un axe horizontal ambre
« energy change of one snapshot · r = dE/dt », histogramme violet au-dessus, densité vraie en gris
pointillé.
**Animation :** sur « s'écarte » : deux triangles sous l'axe, violet sur la moyenne du modèle, gris sur
zéro. Sur « seul son poids » : les points restent en place, leur taille change, le triangle violet glisse
vers zéro. Sur « plusieurs pondérations » : trois pondérations défilent (« drop the top », « linear »,
« w ∝ exp(β r) ») avec chacune une barre de coût ; la troisième est la plus courte.
**Textes à l'écran (EN) :** « truth » · « model q » · « target: average 0 (energy budget) » · « misses the
target » · « no snapshot moves · only its weight » · « drop the top », « linear », « w ∝ exp(β r) » ·
« cost: how much the crowd is distorted » · « I-projection » · puces « SCHEMATIC · toy law of the report's
interactive diagram », « REFERENCE · Csiszár 1975 » · badge PROVED.
**Voix off :**
> Ici, le bilan d'énergie moyen du modèle s'écarte de sa valeur cible, zéro. La repondération ne déplace
> aucun instantané : seul son poids change. Plusieurs pondérations atteignent la cible ; la moins
> déformante est l'inclinaison exponentielle, ou I-projection, selon Csiszár en 1975.

## X3.1b · Une projection orthogonale · ≈ 19 s · reprend X3.1 (P3)
**On voit :** un encart géométrique : un point « model q », une droite « every crowd with average 0 ».
**Animation :** sur « une droite » : la droite se trace. Sur « perpendiculaire » : une perpendiculaire
descend de q, son pied s'allume, « tilted q* ». Sur « toute autre correction » : un point p sur la droite ;
un triangle rectangle se ferme, côtés « cost of q* », « extra », « cost of p ». Sur « déjà visitées » :
retour à l'axe ; une zone sans point se hachure, « no dot here ».
**Textes à l'écran (EN) :** « every crowd with average 0 » · « model q » · « tilted q* » · « another fix
p » · « cost of q* », « extra », « cost of p » · « no dot here: no mass, before or after ».
**Voix off :**
> Les distributions de bonne moyenne forment une droite ; la distribution inclinée est le pied de la
> perpendiculaire issue du modèle. Toute autre correction coûte davantage, selon une identité
> pythagoricienne. La distribution inclinée reste limitée aux régions déjà visitées.

## X3.2 · La taille effective de l'échantillon · ≈ 38 s · reprend X3.2 (P1–P4)
**On voit :** à gauche, un échantillon de 20 points violets en grille 4 × 5 ; sous lui, un compteur ambre
« effective sample size » à 20. À droite, un axe vert logarithmique des onze valeurs de η.
**Animation :** sur « poids égaux » : le compteur reste à 20. Sur « domine » : un point gonfle, les autres
deviennent des contours, le compteur tombe à 1. Sur « bidimensionnelle » : onze barres ambre poussent ; une
ligne grise « one snapshot: the minimum ». Sur « quatre-vingt-dix-neuf » : une barre s'allume en haut. Sur
« cinq cents » : trois barres au plancher s'allument. Sur « classées » : les barres se réordonnent selon
l'erreur de bilan du modèle de base ; elles forment un escalier presque parfait (une paire échangée). Sur
« Gissinger » : vignette de la citation du rapport.
**Textes à l'écran (EN) :** « a poll of 20 » · « effective sample size » · « equal weights: the whole
crowd » · « one giant weight: one person » · « ESS/N of the tilt · 500 snapshots per η (half b) » · « the
poll keeps 99 % » · « one snapshot in 500 » · « how far the base model's energy budget was off » · « little
to fix » · « much to fix: the poll collapses » · « REPORT · E1, model C, seed 0, Γ = 0.85 » · « ESS/N 0.67 ·
one weight 33× the mean · no distribution improved » · puces « SCHEMATIC · a poll of 20 », « GENERATED ·
V4, one seed », « mean over the 11 values: 0.29 », « the tilt fixes three budgets: energy, cross helicity,
⟨A²⟩ », « rank order: one swap (η = 0.004 and 0.0067) », « REFERENCE · effective sample size: Kish 1965 » ·
badge MEASURED.
**Voix off :**
> La taille effective de l'échantillon mesure ce qui reste après repondération : tout l'échantillon pour
> des poids égaux, un seul instantané quand un poids domine. Dans l'expérience bidimensionnelle, à la plus
> petite valeur de test de la diffusivité, elle reste de quatre-vingt-dix-neuf pour cent ; aux trois plus
> grandes, elle tombe à un instantané sur cinq cents. Elle décroît presque dans l'ordre de l'erreur de
> bilan du modèle de base. Sur le modèle de Gissinger non plus, la repondération n'a amélioré aucune
> distribution.

## X3.3 · Une région jamais visitée · ≈ 27 s · reprend X3.3 (P1–P3, sans la pause « predict »)
**On voit :** le nuage de 05.2 en violet (modèle C à Γ = 0,93), points répartis selon D, la bande |D| < h à
la craie ; à droite, la jauge ambre de 05.1.
**Animation :** sur « jamais » : un interrupteur « missing support » bascule ; les points de la bande
s'effacent, la bande se hachure, l'aiguille tombe à zéro. Sur « nulle » : « 0 × any weight = 0 » s'écrit
dans la bande. Sur « forcée » : les points du bord gonflent l'un après l'autre, la taille effective plonge ;
l'aiguille ne bouge pas. Sur « table des risques » : une fiche « PhD plan · risk table » glisse, une ligne
soulignée.
**Textes à l'écran (EN) :** « D · dipole » · « the bridge · |D| < h » · « missing support » · « crossing
rate read in the strip » · « empty strip: 0 × any weight = 0 » · « weights pile up at the edge » ·
« reweighting cannot create mass » · « PhD plan · risk table » · « tilting alone is not a fallback » ·
puces « GENERATED · model C, Γ = 0.93 », « SCHEMATIC · the bridge removed by hand · weights for
illustration » · badge PROVED.
**Voix off :**
> Si un modèle ne visite jamais la région de transition entre les deux polarités, la formule de Rice y
> lit une contribution nulle, qu'aucun poids ne peut relever. Une correction forcée concentre le poids
> sur quelques instantanés du bord. La table des risques du plan de thèse en conclut que la repondération
> seule ne constitue pas une solution de repli.

## X3.4 · Le terme de perte statistique, valeur par valeur · ≈ 38 s · reprend X3.4 (avec X3.4b)
**On voit :** même cadre que les barres de X3.2 ; l'axe ne garde que les cinq valeurs de test de η ; pour
chacune, trois barres : V4 (violet pointillé), témoin (gris), V5 avec le terme de perte statistique
(ambre). Ligne pointillée « honest noise floor ».
**Animation :** sur « la plus grande » : le groupe de droite s'allume ; accolade « dissipates 2.2× the
energy fed in ». Sur « deux virgule deux » : la barre V5 descend de la hauteur du témoin à la sienne. Sur
« la plus petite » : le groupe de gauche, « no change ». Sur « témoin » : les barres grises clignotent. Sur
« les mêmes valeurs » : la rangée de X3.2 revient sous les groupes, alignée. Sur « une seule graine » : la
puce clignote.
**Textes à l'écran (EN) :** « distribution distance · test values of η (never seen) » · « V4 · base » ·
« control · same length, no loss » · « V5 · crowd loss » · « dissipates 2.2× the energy fed in » · « 7.7 →
2.2 » · « no change » · « stays put » · « ESS/N of the tilt (X3.2) » · « the loss moves the crowd · weights
cannot » · puces « GENERATED · one seed per variant », « interpolation only », « part of the gain could be a
global rescaling of the energy level: argued against, not ruled out », « slight cost at small training η »
· badge MEASURED.
**Voix off :**
> L'autre voie modifie l'entraînement par le terme de perte statistique. À la plus grande valeur de test,
> le modèle de base dissipe en moyenne plus de deux fois l'énergie injectée ; ce terme ramène la distance
> de sept virgule sept à deux virgule deux. À la plus petite, aucun changement, et le témoin, entraîné
> aussi longtemps sans ce terme, ne bouge pas. Les gains apparaissent aux valeurs où la repondération
> échouait. Ces résultats reposent sur une seule graine. Le chapitre suivant revient à la fréquence des
> inversions.

**Durée totale estimée :** 2 min 52 s · **Mots :** ≈ 375

**Points à valider :**
1. La carte X3a.Q (Q12 : solution de repli si le terme de perte statistique échoue) est supprimée ; la
   question passe dans l'unité finale « Ouvertures ».
2. Le sondage (fil rouge de la v3), le village jamais interrogé et la pause « predict » de X3.3 sont
   retirés ; la distance d'énergie est nommée à l'oral, avec Székely et Rizzo.
3. Les plans X3.2b et X3.4b de la v3 sont fusionnés dans X3.2 et X3.4 ; « un seul instantané pesait
   trente-trois fois la moyenne » n'est plus dit, seulement affiché.
4. La transition finale annonce ch09 ; « Retour au péage » est retiré.
