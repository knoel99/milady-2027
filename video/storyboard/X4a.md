# X4a · Ce que les instantanés peuvent dire, et ce qu'ils ne diront pas (≈ 4 min 02 s)

**Objectif :** connaître le biais et la variance de l'estimateur de Rice et ses conditions de test, le
plafond sur la fréquence des inversions par niveaux, pourquoi les temps d'attente demandent la dynamique,
et ce que le prochain tour de la première marche doit montrer. **À retenir :** un générateur
d'instantanés estime et borne des fréquences, mais les temps d'attente demandent le film ; la première
marche a besoin de plus de graines, d'un second modèle, d'un miroir de plus et de critères qui résistent
au bruit.
**Niveau :** L4 → L5. **Version :** longue seulement (inséré après ch09.Q, avant chSOA2).

## X4.1 · Quelle largeur pour la bande ? · ≈ 30 s · reprend X4.1 (P1)
**On voit :** NIGHT. Lower-third « EXTENSION X4a · LEVEL 4–5 · AN ASIDE ». À gauche, le plan
(D, vitesse) de 05.2 rempli de points synthétiques ; la bande |D| < h à la craie, un curseur « strip
half-width h ». À droite, un graphe « estimate ÷ true rate » avec la ligne « true rate » à 1.
**Animation :** sur « Élargissez-la » : le curseur s'ouvre, la bande s'élargit ; à droite, la colonne de
30 petites estimations ambre dérive vers le haut d'un bloc (« wide: bias ∝ h² »). Sur « Rétrécissez-la » :
la bande se resserre, la colonne s'étale en hauteur (« narrow: variance ∝ 1/(N h) »). Sur « zéro
virgule deux » : retour sur le nuage réel des trois cadrans, 26 points dans la bande, marque « h = 0.2 ».
**Textes à l'écran (EN) :** « What snapshots can and cannot tell » · « strip · |D| < h » · « h (units of
σ) » · « 30 shoeboxes of N snapshots » · « wide: bias ∝ h² » · « narrow: variance ∝ 1/(N h) » · « the
three-dial experiment · Γ = 0.93 » · « in the strip: 26 of 8,000 snapshots » · « h = 0.2 » · puces
« illustration · synthetic Gaussian snapshots, true rate known · no data », « error bars assume
independent snapshots: generated ones are, one simulation's are not » · badge PROVED.
**Voix off :**
> Un aparté, avant de prendre du recul. On va bâtir beaucoup de choses sur la formule de Rice : autant
> connaître ses limites. Première question : quelle largeur donner à la bande ?
>
> Élargissez-la, et l'estimation devient floue : son biais grandit comme le carré de la largeur.
> Rétrécissez-la, et l'estimation tremble, parce que moins d'instantanés tombent dedans. L'expérience des
> trois cadrans prenait les instantanés à moins de zéro virgule deux de zéro.

## X4.1b · Et si on la rendait infiniment fine ? · ≈ 33 s · reprend X4.1 (P2–P3)
**On voit :** le curseur, la flèche « h → 0 ? ».
**Animation :** sur « nuage lisse » : le nuage synthétique se fond en un dégradé continu. Sur « un
cosinus » : il est remplacé par un anneau mince (un cosinus trace une ellipse dans le plan valeur-vitesse),
le dégradé disparaît. Sur « deux passages par période » : deux tics à la craie sur la trace du cosinus,
coche « the formula: two per period ». Sur « Le chaos » : le nuage réel des trois cadrans revient, fin et
filamenteux ; sur « dépend de la largeur » : la puce « the answer depends on h ».
**Textes à l'écran (EN) :** « h → 0 ? » · « D = cos(ωt + φ) » · « snapshots on a thin ring: no smooth
density » · « two crossings per period » · « the formula: two per period » · « deterministic chaos:
smooth density not guaranteed » · « the answer depends on h » · « only test so far: three deterministic
dials » · puce « tested on a 3-variable deterministic system only ».
**Voix off :**
> Avec une infinité d'instantanés, pourquoi ne pas la rendre infiniment fine ? Parce que la formule exacte
> suppose un nuage lisse.
>
> Prenez un cosinus : ses instantanés vivent sur un anneau mince, rien de lisse. Et pourtant, la formule
> trouve bien deux passages par période. Le chaos, lui aussi, peut manquer de nuage lisse. Alors rien ne
> garantit la limite. Et sur les trois cadrans, le seul test à ce jour, la réponse dépend de la largeur de
> bande.

## X4.2 · Relever la barre · ≈ 37 s · reprend X4.2 (variante en attente, P1–P2)
**On voit :** le rail monte de Level 4 à Level 5. En haut, une trace D(t) dessinée à la main
(SCHEMATIC), les lignes « +a », « −a », « D = 0 ».
**Animation :** sur « relevez la barre » : les lignes ±a s'écartent de zéro. Sur « son reflet en miroir » :
une vraie inversion s'allume (point plein là où elle passe sous −a). Sur « plafonne » : le cadre vide d'un
graphe s'ouvre en bas, « crossings per unit time » en fonction du niveau a ; deux étiquettes « r_a » et
« r ». Sur « petites oscillations » : sur la trace, un frémissement qui traverse +a sans inverser,
étiquette « wobble ». Sur « tout un plateau » : une zone plate se dessine en pointillé (« plateau
(Conjecture 2.33) »).
**Textes à l'écran (EN) :** « Level 4 → Level 5 » · « a reversal: from above a to below −a » · « wobble:
crosses a, no reversal » · « r · reversals per unit time » · « r_a · crossings of the level a, either way
(Rice: snapshots + equations) » · « plateau (Conjecture 2.33) » · « SCHEMATIC · the conjecture's
picture, no data » · « DATA · X4_RICE_LEVELS · AWAITING » · badge CONJECTURE, confiance moyenne.
**Voix off :**
> On monte d'une marche. Pour compter des inversions, et pas de simples passages, il faut relever la
> barre : une inversion doit partir d'au-dessus d'un certain niveau et finir sous son reflet en miroir.
> Du coup, la fréquence de passage de ce niveau, que Rice lit dans les instantanés, plafonne la fréquence
> des inversions. Ça, c'est démontré.
>
> Les petites oscillations autour du niveau desserrent ce plafond. La conjecture : si une inversion dure
> bien plus longtemps qu'une oscillation, le plafond devient presque exact, sur tout un plateau de
> niveaux.

## X4.2b · Le pari du plateau · ≈ 23 s · reprend X4.2 (cases du siège vide)
**On voit :** le graphe vide avec ses deux ancres réelles (silhouette de |D| à Γ = 0,9, point du comptage à
a = 0) ; à droite, les quatre cases du siège.
**Animation :** sur « Le pari » : la case THE BET se remplit, une bande « within 30 % of r » se dessine
autour du plateau en pointillé. Sur « Confiance : moyenne » : CONFIDENCE. Sur « quelle largeur » : la case
ASK s'allume, la bande du plateau clignote.
**Textes à l'écran (EN) :** « where snapshots sit · |D| at Γ = 0.9 » · « a = 0: every zero crossing,
counted » · « within 30 % of r » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK BEFORE WE COMPUTE ·
puce « bet written before the data · tier-0 campaign: up to 10⁶ snapshots per setting, 3 seeds, about 10³
CPU hours (assumption) ».
**Voix off :**
> Le pari, écrit avant les données et tiré du plan de thèse : sur la première marche de l'escalier, le
> plafond tombe à trente pour cent près de la fréquence comptée, sur ce plateau. Confiance : moyenne. Le
> plafond est démontré ; le plateau, non. Question à poser d'abord : quelle largeur doit avoir ce
> plateau ?

**Note :** variante « résultat » (v2 X4.2.r1–r8) à réécrire au même ton quand x4_rice_levels existera.

## X4.3 · Même photo, autre rythme · ≈ 18 s · reprend X4.3 (P1)
**On voit :** deux signaux l'un au-dessus de l'autre, « one frequency » et « two frequencies ». À droite,
deux petits nuages (D, Ḋ).
**Animation :** sur « la même loi d'instantanés » : les deux nuages glissent l'un vers l'autre et se
superposent exactement ; une jauge ambre « Rice rate: the same », une seule aiguille. Sur « écoutez » :
des tics tombent sur chaque passage par zéro, dans l'ordre du temps, avec un petit son : régulier en
haut, irrégulier en bas. Sous chaque trace, un mini-histogramme des écarts : un pic unique en haut, une
large bosse en bas.
**Textes à l'écran (EN) :** « same snapshot law » · « Rice rate: the same » · « metronome » · « uneven
gaps » · « gap between zeros » · puce « illustration · synthetic Gaussian signals » · badge PROVED.
**Voix off :**
> Une autre limite, démontrée celle-là. Ces deux signaux, aléatoires et lisses, ont exactement la même loi
> d'instantanés : mêmes valeurs, mêmes vitesses. Donc la même fréquence de Rice.
>
> Et pourtant, écoutez. L'un passe par zéro comme un métronome. L'autre, par à-coups.

## X4.3b · Il faut le film · ≈ 26 s · reprend X4.3 (P2–P3)
**On voit :** un histogramme ambre des attentes entre deux inversions, échelle logarithmique, à Γ = 0,9.
**Animation :** sur « un peigne » : à gauche de l'histogramme, une rangée de pics serrés s'allume. Sur
« sans mémoire » : la queue droite se pose sur une droite pointillée. Lower-third de référence Gissinger
2012. Sur « boîte à chaussures » : une boîte de photos s'ouvre devant l'histogramme… vide de cette forme ;
une pellicule de film se déroule à côté. Sur « dans le couloir » : vignette du plan (Q, D) avec les
points violets générés, la bande du couloir |D| < 0,25 ; de courtes trajectoires partent de quelques
points.
**Textes à l'écran (EN) :** « wait between flips (time units) » · « count (log scale) » · « comb:
quantized short waits (unstable orbits) » · « memoryless tail · exponential » · « generated snapshots ·
model C · Γ = 0.9 » · « corridor · |D| < 0.25 » · « short runs of the true equations, from generated
states » · puces « illustration · live integration of the model · shape as in Gissinger 2012, Fig. 12 »,
« open question · PhD plan, T:131 ».
**Voix off :**
> Sur les trois cadrans, Gissinger a trouvé une forme bien précise dans les attentes entre deux
> inversions : un peigne d'attentes courtes, comme quantifiées, puis une longue queue exponentielle, sans
> mémoire.
>
> Cette forme, aucune boîte à chaussures ne la contient : il faut le film. Question ouverte : de courtes
> simulations, lancées depuis des états générés dans le couloir, peuvent-elles fournir ces attentes ?

## X4.5 · Le deuxième tour · ≈ 25 s · reprend X4.5 (variante en attente, P1–P2)
**On voit :** l'escalier en haut à gauche, première marche allumée, puce « second round ». Trois tuiles
apparaissent l'une après l'autre.
**Animation :** sur « Trois graines » : tuile 1, trois couloirs « seed 0 », « seed 1 » pleins, « seed 2 ·
awaiting » en pointillé. Sur « un deuxième modèle » : tuile 2, la carte DQVU et un cylindre VKS gris ;
lower-third de référence Bousquet et al. 2026. Sur « le miroir » : tuile 3, un point vermillon se reflète
et le bouton vert Γ passe de + à −. Sur « Quatre voyants » : les tuiles s'effacent, quatre voyants gris
s'alignent, chacun s'étiquette au mot dit.
**Textes à l'écran (EN) :** « tier 0 · three numbers » · « second round » · « first round: 2 seeds » ·
« DQVU · Bousquet et al. 2026 » · « reduced model of VKS reversal simulations » · « no DQVU code in this
repository yet » · « joint mirror R_π · the impeller swap » · « R_π: D → −D, V → −V and Γ → −Γ » · « tier
0 · success criteria of the PhD plan » · quatre voyants (mirror, crowd laws not enforced, Rice, level
bound) · « DATA · X4_TIER0 · AWAITING » · badge CONJECTURE, confiance moyenne.
**Voix off :**
> Dernier point de l'aparté : la première marche de l'escalier aura un deuxième tour. Trois graines au
> lieu de deux. Un deuxième modèle, distillé à partir des simulations de VKS. Et le miroir de l'échange
> des turbines, qui inverse aussi le bouton Gamma.
>
> Quatre voyants devront s'allumer : le déséquilibre, les lois jamais imposées, Rice, et le plafond par
> niveaux.

## X4.5b · Pile ou face · ≈ 38 s · reprend X4.5 (cases du siège vide)
**On voit :** les quatre voyants, chacun avec sa valeur du premier tour en petit.
**Animation :** sur « un virgule quatre-vingt-dix-huit » : le deuxième voyant affiche « ×1.98 » contre une
barre à 2, l'aiguille tremble sur la limite. Sur « pile ou face » : une pièce tourne dans un coin. Sur
« un piège » : le premier voyant ; une courbe en cloche des écarts d'un modèle parfaitement symétrique,
la ligne du plancher en son milieu, la moitié droite hachurée. Sur « test statistique » : la case ASK.
Sur « on referme l'aparté » : tout recule, le cadre s'élargit.
**Textes à l'écran (EN) :** « first round: ×1.98 (0.0113 vs 0.0224) » · « first round, 2 seeds: 0.0037 to
0.0048 vs floor 0.0040 » · « first round, seed 0: cumulative 14 % far from the threshold (pointwise up to
65 %), 42 % near » · « not measured yet » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK · puces
« first round = E1 · 2 seeds instead of the 3 planned », « bet written before the data · tier 0:
perceptrons on CPU, simulations about 10³ CPU hours (assumption) ».
**Voix off :**
> Le pari : les résidus des lois non imposées sont encore divisés par deux, à peu près. La dernière fois,
> « divisé par deux », c'était un virgule quatre-vingt-dix-huit, pour une barre fixée à deux. Autant dire
> pile ou face. Confiance : moyenne.
>
> Un piège, aussi : un modèle parfaitement symétrique tombe au-dessus du plancher de bruit presque
> une fois sur deux, puisque le plancher, c'est sa moyenne. D'où la question à poser d'abord : faut-il un
> vrai test statistique pour ce premier voyant ?
>
> On referme l'aparté, et on prend du recul sur tout le domaine.

**Note :** variante « résultat » (v2 X4.5.r1–r8) à réécrire au même ton plus tard.

## X4a.Q · Question pour les encadrants · ≈ 12 s · reprend X4a.Q
**On voit :** la carte « ASK · Q14 · X4a · C. Nore / Y. Ponty » ; en fond pâle, la texture peigne-et-queue
de X4.3.
**Animation :** soulignés au stylo sur « how often » et « waiting times ».
**Textes à l'écran (EN) :** texte de Q14 (registre), catégorie RUNS.
**Voix off :**
> Question pour les encadrants : au-delà de la fréquence, pour VKS, faut-il aussi viser les temps
> d'attente, avec de courtes simulations lancées depuis des états générés ?

**Durée totale estimée :** 4 min 02 s · **Mots :** ≈ 560

**Points à valider :**
1. Le passage de main vise chSOA2 (« on prend du recul sur tout le domaine ») sans dire « la carte »,
   pour laisser SOA2.1 « Retour à la carte » faire son effet.
2. « Le plancher, c'est sa moyenne » : formulation orale de R:832 (le plancher est l'espérance de
   l'écart d'un modèle exactement symétrique) ; « presque une fois sur deux » arrondit 0,42–0,45.
3. X4.1 ne dit pas « optimum en N puissance moins un cinquième » (couche formule seulement), comme la v2.
4. X4.2 et X4.5 sont des sièges vides : la v3 garde la structure ancre → pari → confiance → question ; les
   variantes « résultat » restent à réécrire.
