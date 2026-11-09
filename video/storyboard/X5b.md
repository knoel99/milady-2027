# X5b · Coût de calcul et calendrier (≈ 1 min 30 s)

**Objectif :** présenter le coût de calcul estimé, son incertitude et ce qu'il exclut, puis le plan de
36 mois sur une page, avec ses risques identifiés et celui qui n'est pas encore évalué. **À retenir :** le
coût est estimé à un facteur deux près au moins, et chaque estimation sera remplacée par une mesure ; le
plan est une proposition dont le financement des derniers mois n'est pas documenté.
**Niveau :** L5. **Version :** longue seulement (inséré après X6, avant ch11).

## X5.5 · Le coût de calcul estimé · ≈ 24 s · reprend X5.5 (variante en attente, P1)
**On voit :** changement d'encre NIGHT → BLUEPRINT. Lower-third « EXTENSION X5b · LEVEL 5 · AN ASIDE ». Une
barre horizontale empilée se construit segment par segment, une petite marche au-dessus de chaque segment.
**Animation :** sur « onze mille » : les segments des paliers 0 à 4 se posent l'un après l'autre (le palier
0 n'est qu'un fil), puis la réserve hachurée ; au bout, « plan ≈ 1.1 × 10⁴ ». Sur « la plus grande part » :
le segment du palier 2 s'éclaire, son détail glisse dessous. Sur « un seul entraînement publié » : une
courte barre pleine « PCDM · ≈ 1150 GPU h » ; des fils gris la relient à la plupart des segments.
**Textes à l'écran (EN) :** « tier 0 » … « tier 4 » · « ≈ 0 · CPU », « ≈ 700 », « ≈ 3900 », « ≈ 3200 »,
« ≈ 1200 » · « reserve 20 % (H5) » · « estimate » · « plan ≈ 1.1 × 10⁴ A100-class GPU hours » · « 3 latent
models × 300 h · 12 ablations × 150 h · 1 model at 128³ × 1200 h » · « PCDM · Li et al. 2026 · ≈ 1150 GPU
h » · « published anchor (H1) » · « × 300 h per latent model (≈ a quarter: H2, unverified) » · puce « A100-
class GPU hours · estimates (T:957) » · badge CONJECTURE, confiance faible.
**Voix off :**
> Ce module présente le coût de calcul et le calendrier du plan de thèse. Le coût est estimé à environ
> onze mille heures de carte graphique, réserve de vingt pour cent comprise ; le palier
> tridimensionnel en représente la plus grande part. La plupart des postes sont extrapolés d'un seul
> entraînement publié, d'environ mille cent cinquante heures.

## X5.5b · Aucune mesure encore · ≈ 20 s · reprend X5.5 (siège en attente)
**On voit :** sous la barre du plan, une seconde barre vide « measured: no GPU hour yet » ; à droite, une
jauge « measured ÷ planned, like for like » avec la bande du plan.
**Animation :** sur « aucune heure » : la barre du bas reste vide, tampon « AWAITING ». Sur « facteur
deux » : la bande 0,5–2 s'ombre sur la jauge, la puce « the plan's own band » clignote. Sur « simulations de
référence » : une troisième barre grise, en heures de processeur, glisse hors de l'estimation.
**Textes à l'écran (EN) :** « measured: no GPU hour yet » · « measured ÷ planned, like for like » · « the
plan's own band (T:974) » · « simulations (CPU) · ≈ 10³ h tier 0 + ≈ 2 × 10⁴ h tier 2, and more ·
assumptions (H4) » · « DATA · X5_COMPUTE_BILL · AWAITING » · cases THE BET, CONFIDENCE, SUCCESS CRITERION,
ASK · puces « no GPU timing yet · one 64³ step: 0.08 s on CPU (C:153) », « palier2_tg3d.yaml: resources.gpus
1 · the solver also runs on GPU (C:153) ».
**Voix off :**
> Aucune heure n'a encore été mesurée. L'hypothèse de travail est un coût mesuré à un facteur deux du
> plan ; la confiance est faible, le plan annonçant lui-même cette incertitude. Les simulations de
> référence, vingt mille heures de processeur ou davantage, sont exclues de l'estimation.

**Note :** variante « résultat » (v2 X5.5.r1–r8) à réécrire au même registre.

## X5.6 · Le plan sur une page · ≈ 16 s · reprend X5.6 (P1)
**On voit :** changement d'encre BLUEPRINT → NIGHT. Un axe des mois de 0 à 36, trois bandes d'année ; les
barres des cinq paliers se dessinent une à une, puis « writing » en pointillé.
**Animation :** sur « trois axes » : trois bandes fines au-dessus des barres, avec leurs pastilles. Sur
« cylindre en précession » : une flèche parcourt les paliers. Sur « trois articles » : trois jalons aux
mois 10, 22 et 33 ; la puce « no acceptance promised ».
**Textes à l'écran (EN) :** « months from the start of the thesis » · « Year 1 », « Year 2 », « Year 3 » ·
« tier 0 » … « tier 4 » · « writing » · « Axis 1 · hard constraints » · « Axis 2 · crowd laws and symmetry » ·
« Axis 3 · threshold and reversals » · « from three dials to a precessing cylinder » · « paper 1 ·
distributional constraints », « paper 2 · hard constraints in bounded domains », « paper 3 · reversals and
threshold » · « committee », « code release », « data decision », « PhD defense » · puce « no acceptance
promised (T:1014) » · badge PLANNED.
**Voix off :**
> Le plan couvre trente-six mois, en trois axes et cinq paliers, du modèle de Gissinger au cylindre en
> précession. Trois articles sont prévus aux mois dix, vingt-deux et trente-trois, sans garantie
> d'acceptation.

## X5.6b · Les risques identifiés · ≈ 30 s · reprend X5.6 (P2–P3)
**On voit :** le calendrier se réduit en haut ; dessous, trois barres de score, puis une matrice de
risques à cinq lignes.
**Animation :** sur « les mieux notées » : barres A, B, F ; A et B fusionnent, « this topic: A + B merged ».
Sur chaque risque nommé : sa ligne s'allume avec ses pastilles probabilité / impact. Sur « financement » :
la cinquième ligne, probabilité vide « to be clarified », impact « high ». Sur « ni validée » : la puce de
bas d'écran s'allume. Sur « conclusion » : le cadre s'assombrit.
**Textes à l'écran (EN) :** « A 4.10 », « B 3.90 », « F 3.50 » · « this topic: A + B merged » · « top two
under all three weightings tried (S:433) » · « non-public VKS and precession data » · « 3D compute above
budget » · « crowd loss unstable in 3D » · « irreducible error near thresholds » · « funding beyond MilaDy's
nominal end » · « to be clarified » · puces « scores: the author's judgments, not validated by the
supervisors (S:437) », « ratings: the proposal author's estimates (T:986) », « Independent PhD proposal ·
not requested or validated by the supervisors (T:57) ».
**Voix off :**
> Le sujet réunit les deux directions les mieux notées parmi six. Les risques identifiés comprennent des
> données non publiques, un dépassement du budget et l'instabilité du terme de perte statistique en trois
> dimensions ; la probabilité du risque de financement après la fin nominale de MilaDy reste à
> clarifier. Ce plan est une proposition indépendante, ni demandée ni validée par les encadrants. La
> conclusion du film suit.

**Durée totale estimée :** 1 min 30 s · **Mots :** ≈ 200

**Points à valider :**
1. La carte X5b.Q (Q20 : financement des derniers mois d'une thèse commencée à l'automne 2027) est
   supprimée ; la question passe dans l'unité finale « Ouvertures ».
2. La transition finale annonce ch11, qui suit X5b maintenant que ch10q est placée en fin de film ; à
   vérifier avec l'ordre de montage v4.
3. La question de la case ASK de X5.5 (sur quelles machines tournent les simulations de référence) n'est
   plus dite ; elle reste à l'écran. L'erreur irréductible près des seuils n'est plus citée à l'oral.
4. « Le palier tridimensionnel » désigne le palier 2 (Taylor-Green et ABC à 64³).
