# X5a · La chaîne de production des données (≈ 2 min 32 s)

**Objectif :** décrire la chaîne de production des données étape par étape (un pas de solveur, un fichier
documenté, le déroulement d'une campagne, un nouvel instrument d'évaluation) et distinguer, pour chaque
chiffre, ce qui est mesuré, estimé ou en attente d'un calcul. **À retenir :** la reproductibilité est
prévue dès la conception : chaque chiffre affiché renvoie à un fichier, à une version du code et à une
ligne du catalogue.
**Niveau :** L4. **Version :** longue seulement (inséré après 10.3, avant X1).

## X5.1 · Un pas du solveur · ≈ 30 s · reprend X5.1 (P1)
**On voit :** changement d'encre NIGHT → BLUEPRINT. Lower-third « EXTENSION X5a · LEVEL 4 · AN ASIDE ». En
haut à gauche, le petit four de 10.2 ; deux panneaux en sortent : « Fourier space » à gauche, « physical
space (grid) » à droite.
**Animation :** sur « coefficients de Fourier » : deux grilles de points 11 × 11, bleue « û » et vermillon
« B̂ ». Sur « multiplication » : « curl = multiply by ik × » s'allume. Sur « sur la grille » : flèche
« inverse FFT », le produit « u × ω + j × B · u × B » s'y calcule, retour par « FFT ». Sur « tiers
supérieur » : la couronne extérieure se grise et disparaît. Sur « divergence nulle » : coche
« projection » ; sur « exactement » : « Lawson RK4 · diffusion solved exactly ».
**Textes à l'écran (EN) :** « The factory floor » · « Fourier space » · « physical space (grid) » · « 2/3
dealiasing · |m| ≤ 21 at 64³ » · « projection · ∇·u = ∇·B = 0 to machine precision » · « Lawson RK4 ·
diffusion solved exactly · 4 evaluations per step » · « milady.sim.mhd3d · periodic 3D MHD · PyTorch, CPU or
GPU » · badge MEASURED.
**Voix off :**
> Ce module décrit la chaîne de production des données, en distinguant les grandeurs mesurées des
> grandeurs estimées. Le solveur représente l'écoulement et le champ par leurs coefficients de Fourier,
> où un rotationnel devient une multiplication. Les produits sont calculés sur la grille ; le tiers
> supérieur des fréquences est supprimé pour éviter le repliement de spectre. Une projection maintient la
> divergence nulle, et la diffusion est intégrée exactement.

## X5.1b · Temps de calcul et mémoire · ≈ 18 s · reprend X5.1 (P2)
**On voit :** les panneaux passent en vignette ; un chronomètre et un histogramme de mémoire occupent le
cadre.
**Animation :** sur « huit centièmes » : le chronomètre s'arrête sur 0.08 s. Barre pleine « 128³ · peak
717 MB ». Sur « estimé » : deux barres en pointillés, 256³ et 512³. Sur « carte graphique » : case grise
« no GPU timing yet ».
**Textes à l'écran (EN) :** « 64³ dynamic step: 0.08 s · development CPU, 2 threads » · « memory, GB » ·
« 128³ · peak 717 MB · measured on CPU » · « 256³ · state 0.4 GB · peak ≈ 6 GB (estimate) » · « 512³ · peak
≈ 48 GB (estimate) » · « peak ≈ 15 × state » · puces « no GPU timing yet · … bench --device cuda measures it
on site », « peak ≈ 15 × state: measured once at 128³ on CPU, extrapolated ».
**Voix off :**
> Un pas à soixante-quatre points de côté dure huit centièmes de seconde sur un processeur ordinaire. Le
> pic de mémoire est estimé à six gigaoctets à deux cent cinquante-six points. Aucun temps n'a encore été
> mesuré sur carte graphique.

## X5.2 · Un fichier par simulation · ≈ 27 s · reprend X5.2
**On voit :** BLUEPRINT. Le bocal étiqueté de 10.2 au centre ; plongée dans l'étiquette, qui devient la
fiche « fields.h5 » avec son chemin.
**Animation :** sur « The Well » : l'arborescence se tape ligne par ligne, les entrées de la convention en
gris. Sur « instantané par instantané » : derrière « velocity » et « magnetic_field », une bande de six
vignettes. Sur « identifiant » et « version du code » : les deux attributs s'allument. Sur « catalogue » :
à droite, le catalogue ; un fil relie les deux identifiants. Sur « seuls fichiers » : les lignes se
reconstruisent (flèche « ingest »). Sur « non inviolable » : le tampon « --force » frappe le fichier, la
somme de contrôle se réécrit.
**Textes à l'écran (EN) :** « fields.h5 » · « {campaign}/{uuid}/fields.h5 » · « in grey: The Well
convention » · « milady_uuid », « milady_git_commit » · « same UUID in the file and in the catalog » · « the
checksum lives in the catalog » · « checksummed, not tamper-proof » · puces « MFF · HDF5 following The Well
(Ohana et al. 2024) · read back by replaying The Well's loader », « rebuilt from the files: simulations,
files, diagnostics · not restored: compute time, resources, campaign YAML » · badge MEASURED.
**Voix off :**
> Chaque simulation produit un fichier au format de The Well, une collection de référence pour
> l'apprentissage automatique. Il contient la vitesse et le champ magnétique, instantané par instantané,
> un identifiant unique et la version du code. Le catalogue ajoute une somme de contrôle et peut être
> reconstruit à partir des seuls fichiers. Le contenu est vérifiable, non inviolable.

## X5.3 · Le déroulement d'une campagne · ≈ 33 s · reprend X5.3 (variante en attente)
**On voit :** en haut, les sept étapes de la chaîne en petites boîtes grises, de « 1 campaign » à
« 7 evaluation » (5 à 7 pâles, « later »). Dessous, un terminal.
**Animation :** sur « une commande » : la commande se tape ; au-dessus, la configuration et ses onze
points verts sur un axe logarithmique. Sur « une tâche par valeur » : onze lignes « task k/11 · queued » ;
onze petits fours s'allument, seize traits fins par four. Sur « catalogue » : colonnes statut, sha256,
durée, valeurs grises. Sur « pas encore été exécutée » : tampon « AWAITING ». Sur « hypothèse de
travail » : le cadre vide d'une jauge « tasks finished » de 0 à 11, cible « all eleven ». Sur « élevée » :
barres pleines « 4 s » et « 10 s », puis « ≈ 30 min ».
**Textes à l'écran (EN) :** « $ make sweep CONFIG=infra/configs/palier1_mhd2d.yaml » · « η: 11 values,
log-spaced, 0.004 → 0.0226 · 16 runs each · 32² · burn-in 30 · 150 snapshots » · « tasks finished » · « all
eleven » · « DATA · x5_campaign_trace · AWAITING » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK BEFORE
WE COMPUTE (« Where do campaigns run first: lab GPUs, Jean Zay, or a rented VM? ») · puces « SCHEMATIC ·
walk-through, no run yet », « reduced test campaigns (3D, 2 × 2, 12³): 4 simulations done in 4 s in laptop
mode, 10 s in Docker », « E2's data, same solver (mhd2d.py): about 30 min on CPU », « a factory check, not a
criterion of the PhD plan » · badge CONJECTURE, confiance haute.
**Voix off :**
> Une commande lit la configuration d'une campagne : le cas bidimensionnel, onze valeurs de la
> diffusivité magnétique. Le lanceur crée une tâche par valeur ; chacune intègre seize simulations et
> inscrit au catalogue son statut, sa somme de contrôle et sa durée. Cette campagne n'a pas encore été
> exécutée. L'hypothèse de travail est que les onze tâches aboutissent. La confiance est élevée : des
> campagnes de test réduites ont abouti en quelques secondes.

**Note :** variante « résultat » (v2 X5.3.r1–r8) à réécrire au même registre. La question de la case ASK
reste à l'écran, non dite (comme en v2).

## X5.4 · Le nombre de points X · ≈ 44 s · reprend X5.4 (P1, réponse et siège, sans la pause « predict »)
**On voit :** changement d'encre BLUEPRINT → NIGHT. À gauche, un carré dont les bords opposés sont
recollés ; dedans, les courbes de niveau d'un potentiel jouet. Puis, à droite, le cadre vide d'un graphe
« X-points per snapshot » / « share of snapshots », silhouettes « simulated » et « generated ».
**Animation :** sur « courbes de niveau » : les contours se dessinent. Sur « points O » : un point plein
pulse au centre d'une boucle. Sur « points X » : une croix là où deux lignes se croisent. Sur « autant » :
tous les points O et X se marquent, deux compteurs montent ensemble et s'arrêtent sur le même nombre. Sur
« aucune » : puce « none computed in the report ». Sur « seuil » : case SUCCESS CRITERION grise,
« tolerance: not set ». Sur « module suivant » : la grille résiduelle s'efface.
**Textes à l'écran (EN) :** « field lines = contours of the potential A » · « O-point · island centre » ·
« X-point · lines cross » · « O », « X » · « saddles = extrema on the torus · Poincaré–Hopf » · « DATA ·
x5_xpoints · AWAITING » · « tolerance: not set » · cases THE BET, CONFIDENCE, SUCCESS CRITERION, ASK · puces
« SCHEMATIC · toy field on the periodic square », « a metric requested by the internship offer · none
computed in the report (R:739) » · badge CONJECTURE, confiance faible.
**Voix off :**
> Un nouvel instrument d'évaluation porte sur la topologie. En deux dimensions, les lignes de champ sont
> les courbes de niveau d'un potentiel : elles entourent les points O et se croisent aux points X. Sur un
> domaine périodique, un potentiel générique a autant de points X que de points O, selon le théorème de
> Poincaré-Hopf. L'offre de stage demande de telles mesures ; le rapport n'en a calculé aucune.
> L'hypothèse de travail, de confiance faible, est que les champs générés reproduisent le nombre de points
> X simulé ; aucun seuil n'est fixé. Le module suivant porte sur la validation du solveur
> tridimensionnel.

**Note :** variante « résultat » (v2 X5.4.r1–r9) à réécrire au même registre.

**Durée totale estimée :** 2 min 32 s · **Mots :** ≈ 335

**Points à valider :**
1. La carte X5a.Q (Q16 : quelle mesure de topologie, quel écart fait échouer un modèle) est supprimée ; la
   question passe dans l'unité finale « Ouvertures ».
2. Les images de l'usine, du four et du bocal restent à l'écran ; la voix dit « solveur », « fichier »,
   « catalogue », « somme de contrôle » (au lieu d'« empreinte »).
3. La roue de diligence, la carte de randonnée et la pause « predict » de X5.4 sont retirées ; « un
   potentiel générique » résume l'hypothèse de fonction de Morse (T:876).
4. Ce qui n'est plus dit, faute de temps : « environ quinze fois l'état » (X5.1b), la réécriture forcée
   (X5.2), la demi-heure des données du rapport (X5.3) ; tout reste à l'écran.
