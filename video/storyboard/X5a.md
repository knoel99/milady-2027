# X5a · L'usine, poste par poste (≈ 4 min 18 s)

**Objectif :** ouvrir l'usine à données une station à la fois (un pas de solveur, un fichier étiqueté, la
vie d'une campagne, un nouvel instrument pour le critique) et savoir, pour chaque chiffre, s'il est
mesuré, estimé, ou en attente d'un calcul. **À retenir :** la reproductibilité est prévue dès le départ :
chaque chiffre à l'écran remonte à un fichier, un commit et une ligne du registre.
**Niveau :** L4. **Version :** longue seulement (inséré après 10.3, avant X1).

## X5.1 · On ouvre un four · ≈ 52 s · reprend X5.1 (P1)
**On voit :** changement d'encre NIGHT → BLUEPRINT (grille bleue technique qui balaie l'écran derrière un
trait). Lower-third « EXTENSION X5a · LEVEL 4 · AN ASIDE ». En haut à gauche, le petit four de 10.2 ; sa
porte s'ouvre et deux panneaux en sortent : « Fourier space » à gauche, « physical space (grid) » à
droite.
**Animation :** sur « des ondes » : deux grilles de points 11 × 11, bleue « û » et vermillon « B̂ ». Sur
« une simple multiplication » : l'étiquette « curl = multiply by ik × » s'allume sur une flèche qui reste
dans le panneau Fourier. Sur « l'aller-retour » : une flèche « inverse FFT » vers la grille, le produit
« u × ω + j × B · u × B » s'y calcule, retour par « FFT ». Sur « le tiers supérieur » : la couronne
extérieure de points se grise et disparaît. Sur « diligence » : petite vignette d'une roue à rayons qui
semble tourner à l'envers, puis s'efface. Sur « sans divergence » : une coche « projection » ; sur
« exactement » : « Lawson RK4 · diffusion solved exactly ».
**Textes à l'écran (EN) :** « The factory floor » · « Fourier space » · « physical space (grid) » ·
« 2/3 dealiasing · |m| ≤ 21 at 64³ » · « projection · ∇·u = ∇·B = 0 to machine precision » · « Lawson
RK4 · diffusion solved exactly · 4 evaluations per step » · « milady.sim.mhd3d · periodic 3D MHD ·
PyTorch, CPU or GPU » · badge MEASURED.
**Voix off :**
> Petit détour par l'usine. Si vous encadrez ce projet, vous voudrez savoir ce qu'il y a dans les fours,
> ce qu'il y a dans les bocaux, et quels chiffres sont mesurés ou seulement estimés. Alors on ouvre,
> poste par poste.
>
> Premier poste : un four. Le solveur garde l'écoulement et le champ sous forme d'ondes. Dans ce
> langage-là, un rotationnel, c'est une simple multiplication. Les produits, eux, se calculent mieux sur
> la grille : à chaque pas, le calcul fait l'aller-retour.
>
> Au passage, il coupe le tiers supérieur des ondes. Sinon, les produits se replieraient en fausses
> ondes, un peu comme les roues de diligence qui semblent tourner à l'envers au cinéma. Une projection
> garde les deux champs sans divergence, et la diffusion est résolue exactement.

**Note :** l'image de la roue de diligence (repliement de fréquence) est une analogie ajoutée, sans fait
nouveau ; elle illustre ce que la v2 appelait « fold back as fakes ».

## X5.1b · Ce que ça coûte · ≈ 28 s · reprend X5.1 (P2)
**On voit :** les deux panneaux glissent en vignette ; un chronomètre et un histogramme de mémoire
occupent le cadre.
**Animation :** sur « huit centièmes » : le chronomètre s'arrête sur 0.08 s (trait plein). Sur « cent
vingt-huit » : barre pleine « 128³ · peak 717 MB ». Sur « estimation » : deux barres en pointillés,
256³ et 512³ ; la puce « estimate » clignote une fois. Sur « carte graphique » : une case grise vide
« no GPU timing yet ».
**Textes à l'écran (EN) :** « 64³ dynamic step: 0.08 s · development CPU, 2 threads » · « memory, GB » ·
« 128³ · peak 717 MB · measured on CPU » · « 256³ · state 0.4 GB · peak ≈ 6 GB (estimate) » · « 512³ ·
peak ≈ 48 GB (estimate) » · « peak ≈ 15 × state » · puces « no GPU timing yet · … bench --device cuda
measures it on site », « peak ≈ 15 × state: measured once at 128³ on CPU, extrapolated ».
**Voix off :**
> Combien ça coûte ? Un pas, en soixante-quatre au cube : huit centièmes de seconde, sur un processeur
> ordinaire. Ça, c'est mesuré.
>
> La mémoire, au pic, c'est environ quinze fois l'état. Mesuré une seule fois, en cent vingt-huit au cube.
> Extrapolé à deux cent cinquante-six au cube : à peu près six gigaoctets. Ça, c'est une estimation, d'où
> les pointillés. Et sur carte graphique, aucun chronométrage pour l'instant.

## X5.2 · On ouvre un bocal · ≈ 44 s · reprend X5.2
**On voit :** BLUEPRINT. Le bocal étiqueté de 10.2 au centre.
**Animation :** sur « un bocal » : plongée dans l'étiquette, qui devient la fiche « fields.h5 » avec son
chemin. Sur « The Well » : l'arborescence se tape ligne par ligne, les entrées de la convention The Well
en gris. Sur « instantané après instantané » : derrière « velocity » (bleu) et « magnetic_field »
(vermillon), une bande de six vignettes glisse ; puis « milady_diagnostics/ » et une mini-courbe. Sur
« identifiant unique » et « commit » : les deux attributs s'allument. Sur « Le registre » : à droite, le
registre ; un fil relie l'identifiant du fichier à celui de la ligne. Sur « coupé d'Internet » : les
lignes du registre se reconstruisent à partir de la fiche (flèche « ingest »). Sur « contrôlé, pas
scellé » : le tampon « --force » frappe le fichier, la somme de contrôle se réécrit.
**Textes à l'écran (EN) :** « fields.h5 » · « {campaign}/{uuid}/fields.h5 » · « in grey: The Well
convention » · « milady_uuid », « milady_git_commit » · « same UUID in the file and in the catalog » ·
« the checksum lives in the catalog » · « checksummed, not tamper-proof » · puces « MFF · HDF5 following
The Well (Ohana et al. 2024) · read back by replaying The Well's loader », « rebuilt from the files:
simulations, files, diagnostics · not restored: compute time, resources, campaign YAML » · badge MEASURED.
**Voix off :**
> Deuxième poste : un bocal. Une simulation, un fichier, rangé comme dans The Well, un jeu de données de
> référence pour l'apprentissage automatique. Dedans : la vitesse et le champ magnétique, instantané après
> instantané, plus des séries d'énergies et de divergences. Sur l'étiquette : un identifiant unique, et le
> commit du code qui l'a produit.
>
> Le registre répète cet identifiant et ajoute une somme de contrôle. Du coup, un cluster coupé d'Internet
> peut reconstruire ses lignes du registre à partir des seuls fichiers.
>
> Et soyons précis : tout à l'heure, j'ai dit « scellé ». C'est contrôlé, pas scellé. Une réécriture
> forcée met simplement à jour la somme de contrôle.

## X5.3 · La vie d'une campagne · ≈ 46 s · reprend X5.3 (variante en attente)
**On voit :** en haut, les sept étapes de la chaîne en petites boîtes grises, de « 1 campaign » à
« 7 evaluation » (5 à 7 pâles, « later »). Dessous, un terminal.
**Animation :** sur « Une commande » : la commande se tape ; au-dessus, la fiche recette et ses onze
points verts sur un petit axe logarithmique. Sur « une tâche par réglage » : onze lignes « task k/11 ·
queued » ; onze petits fours s'allument chacun leur tour, seize traits fins par four. Sur « une ligne » :
le registre se remplit, colonnes statut, sha256, temps de calcul, valeurs encore grises. Sur « pas encore
tourné » : tout se fige, tampon « AWAITING ». Sur « Le pari » : le cadre vide d'une jauge « tasks
finished » de 0 à 11, la cible « all eleven ». Sur « Confiance : élevée » : deux petites barres pleines
« 4 s » et « 10 s » (campagnes de test), puis une barre « ≈ 30 min » (données du rapport).
**Textes à l'écran (EN) :** « $ make sweep CONFIG=infra/configs/palier1_mhd2d.yaml » · « η: 11 values,
log-spaced, 0.004 → 0.0226 · 16 runs each · 32² · burn-in 30 · 150 snapshots » · « tasks finished » ·
« all eleven » · « DATA · x5_campaign_trace · AWAITING » · cases THE BET, CONFIDENCE, SUCCESS CRITERION,
ASK BEFORE WE COMPUTE (« Where do campaigns run first: lab GPUs, Jean Zay, or a rented VM? ») · puces
« SCHEMATIC · walk-through, no run yet », « reduced test campaigns (3D, 2 × 2, 12³): 4 simulations done
in 4 s in laptop mode, 10 s in Docker », « E2's data, same solver (mhd2d.py): about 30 min on CPU », « a
factory check, not a criterion of the PhD plan » · badge CONJECTURE, confiance haute.
**Voix off :**
> Troisième poste : on suit une campagne entière sur la chaîne. Une commande lit la fiche recette : la
> nappe plane, onze diffusivités. Le lanceur ouvre une tâche par réglage ; chaque tâche fait tourner seize
> simulations côte à côte, et écrit un fichier. Et chaque tâche ajoute une ligne au registre : son statut,
> sa somme de contrôle, son temps de calcul.
>
> Sauf que… cette campagne n'a pas encore tourné. Alors on parie : les onze tâches vont au bout, chacune
> avec son fichier contrôlé. Confiance : élevée. Des campagnes de test plus petites ont déjà fini, en
> quelques secondes. Et les données du rapport, sorties du même solveur, ont pris environ une demi-heure.

**Note :** la variante « résultat » (v2 X5.3.r1–r8) est à réécrire au même ton quand le fichier
x5_campaign_trace existera. La question de la case ASK reste à l'écran, non dite (comme en v2).

## X5.4 · Des sommets, des cols · ≈ 24 s · reprend X5.4 (P1)
**On voit :** changement d'encre BLUEPRINT → NIGHT. À gauche, un carré dont les bords opposés sont
recollés (petites flèches appariées sur les bords) ; dedans, les courbes de niveau d'un potentiel jouet,
deux nuances de vermillon.
**Animation :** sur « courbes de niveau » : les contours se dessinent du centre vers l'extérieur. Sur
« points O » : un point plein pulse au centre d'une boucle. Sur « points X » : une croix se pose là où
deux lignes se croisent, la ligne qui passe par le col s'épaissit un instant.
**Textes à l'écran (EN) :** « field lines = contours of the potential A » · « O-point · island centre » ·
« X-point · lines cross » · puce « SCHEMATIC · toy field on the periodic square » · badge CONJECTURE,
confiance faible.
**Voix off :**
> Dernier poste : un nouvel instrument pour le critique. Dans la nappe plane, les lignes de champ sont les
> courbes de niveau d'un seul potentiel, comme sur une carte de randonnée. Autour d'un sommet ou d'un
> creux, les lignes font des boucles : ce sont les points O. Au col, elles se croisent : ce sont les
> points X.

## X5.4b · Plus de cols ou plus de sommets ? · ≈ 26 s · reprend X5.4 (« predict » et réponse)
**On voit :** le même carré ; pastille PREDICT, deux compteurs vides « O » et « X ».
**Animation :** silence de 2,5 s après la question, seuls les contours respirent. Sur « Ni les uns ni les
autres » : tous les points O et X se marquent d'un coup, les deux compteurs montent ensemble et
s'arrêtent sur le même nombre ; tampon « = ».
**Textes à l'écran (EN) :** « PREDICT » · « periodic square: more X-points or more O-points? » · « O »,
« X » · « saddles = extrema on the torus · Poincaré–Hopf ».
**Voix off :**
> Question : sur ce carré, dont les bords se rejoignent, qu'est-ce qui est le plus fréquent, les cols ou
> les sommets ?
>
> Ni l'un ni l'autre : il y en a exactement autant. Sur une surface refermée comme celle-ci, chaque sommet
> ou creux est compensé par un col. C'est une vérification gratuite pour n'importe quel programme qui
> compte.

## X5.4c · Un instrument sans barème · ≈ 26 s · reprend X5.4 (siège vide)
**On voit :** le carré glisse à gauche ; à droite, le cadre vide d'un graphe « X-points per snapshot » /
« share of snapshots », deux silhouettes en pointillés « simulated » et « generated ».
**Animation :** sur « aucune » : puce rouge pâle « none computed in the report ». Sur « Le pari » : la case
THE BET se remplit. Sur « aucun seuil » : la case SUCCESS CRITERION reste grise, « tolerance: not set ».
Sur « On referme l'usine » : la grille BLUEPRINT résiduelle s'efface, le petit four se referme en coin.
**Textes à l'écran (EN) :** « DATA · x5_xpoints · AWAITING » · « tolerance: not set » · cases THE BET,
CONFIDENCE, SUCCESS CRITERION, ASK · puce « a metric requested by the internship offer · none computed in
the report (R:739) ».
**Voix off :**
> L'offre de stage demande de la topologie ; le rapport n'en a calculé aucune. D'où un pari, à faible
> confiance : les champs générés auront autant de points X que les champs simulés. Le plan de thèse
> prévoit ce comptage… mais ne fixe aucun seuil de réussite.
>
> On referme l'usine. Et avant le premier pari, un dernier coup d'œil dans la boîte tourbillonnante.

**Note :** variante « résultat » (v2 X5.4.r1–r9) à réécrire au même ton plus tard.

## X5a.Q · Question pour les encadrants · ≈ 12 s · reprend X5a.Q
**On voit :** la carte « ASK · Q16 · X5A · C. Nore / Y. Ponty » ; en fond, des anneaux de contours pâles.
**Animation :** soulignés au stylo sur « topology » et « X-point counts ».
**Textes à l'écran (EN) :** texte de Q16 (registre), catégorie FRAMING.
**Voix off :**
> Question pour les encadrants : quelle mesure de topologie doit juger les champs générés… et quel écart
> dans le nombre de points X fait échouer un modèle ?

**Durée totale estimée :** 4 min 18 s · **Mots :** ≈ 600

**Points à valider :**
1. « Tout à l'heure, j'ai dit scellé » : rappel volontaire de 10.2 (« sealed in a labelled jar ») ; à
   garder seulement si le storyboard de ch10 dit bien « scellé ».
2. Les « cols et sommets » de la carte de randonnée remplacent « X-points, O-points » à l'oral (les sigles
   restent à l'écran) ; « points O / points X » dits une fois chacun.
3. « Chaque sommet ou creux est compensé par un col » : formulation orale du résultat de Poincaré–Hopf
   (T:876, P8:1482), valable pour un potentiel générique (fonction de Morse), précision laissée à
   l'écran.
4. La phrase de passage vers X1 (« un dernier coup d'œil dans la boîte tourbillonnante ») est nouvelle :
   X1 s'ouvre ensuite sur « Petit détour avant le premier pari ».
