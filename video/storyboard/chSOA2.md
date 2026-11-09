# chSOA2 · État de l'art : la place du projet (≈ 4 min 55 s)

**Objectif :** présenter les quatre axes de l'apprentissage automatique proches du projet, les exigences
qu'une dynamo de laboratoire leur impose, les travaux des encadrants, et l'intersection non couverte que vise
le projet de thèse, avec ses travaux voisins et ses limites. **À retenir :** des substituts rapides, des
modèles génératifs, des méthodes de contrainte et des a priori appris existent ; aucun travail recensé ne
s'applique à une dynamo à parois, à faible nombre de Prandtl magnétique, qui s'inverse.
**Niveau :** L4 → L5 (passage en SOA2.4). **Version :** courte et longue (dans la longue, l'unité suit X4a).

## SOA2.1 · Quatre axes, quatre exigences · ≈ 29 s · reprend SOA2.1
**On voit :** carte de chapitre « 09+ » (3,2 s, muette), puis la carte du domaine laissée par chSOA1 : six
couloirs, l'accolade MilaDy, le point INTERN et l'anneau en pointillés THESIS.
**Animation :** sur « fondées sur les données » : plongée dans le couloir « données » ; l'axe du temps se
resserre sur 2012–2031, les couloirs anciens se tassent en une bande « DYNAMO TRACKS » en haut, et le couloir des
données se déplie en quatre pistes, une par nom. Sur « quatre exigences » : quatre colonnes s'inscrivent au bord
droit, une par exigence (« 3D », « WALLS », « LOW Pm », « RARE ») ; les cases sous chaque colonne restent vides,
en pointillés.
**Textes à l'écran (EN) :** « The map of the field: where this work fits » · « DYNAMO TRACKS » · « SURROGATES »
· « GENERATIVE MODELS » · « CONSTRAINTS » (HARD · SOFT · DISTRIBUTIONAL · SYMMETRY) · « ASSIMILATION PRIORS » ·
« NOW · NOV 2026 » · « 3D · three dimensions » · « WALLS · walls, vacuum, iron » · « LOW Pm · a tiny magnetic
Prandtl number » · « RARE · rare flips » · calque formule (Pm du sodium ≈ 0,82 × 10⁻⁵ ; « no dynamo in 2D
(Zel'dovich 1957) ») · puce « gate verdicts in the next scenes: our reading of published abstracts » · badge
CONTEXT.
**Voix off :**
> Les expériences précédentes portent sur des modèles réduits. Les approches fondées sur les données proches
> du projet se répartissent en quatre axes : les substituts rapides, les modèles génératifs, les méthodes de
> contrainte et l'assimilation de données.
>
> Une dynamo de laboratoire leur impose quatre exigences : un écoulement tridimensionnel, des parois avec du fer
> et un vide extérieur, un nombre de Prandtl magnétique très faible, et des inversions rares.

**Note :** le théorème de Zel'dovich (pas de dynamo en deux dimensions) et la valeur de Pm du sodium sont
affichés, non dits. Les verdicts des cases (✓, ≈, ✗) restent marqués « our reading of published abstracts ».

## SOA2.2 · Les substituts rapides · ≈ 31 s · reprend SOA2.2
**On voit :** la piste SURROGATES s'éclaire, les autres pâlissent ; les repères s'inscrivent un à un. Puis un
encart : la distribution du dipôle à deux bosses (± D).
**Animation :** sur « solveur » : trois repères (équations dans la perte, correspondances entre champs,
préentraînement). Sur « bidimensionnelle » : deux repères avec une icône carrée « 2D ». Sur « Gwirtz » : un repère
en croix, avec un petit glyphe d'inversion ; référence à l'écran. Sur « vers l'écoulement moyen » : dans
l'encart, les deux bosses se fondent en une seule bosse grise centrée sur zéro ; ligne du miroir en filigrane.
Puis la ligne de cases SURROGATES se remplit : 3D ≈, WALLS ✗, LOW Pm ✗, RARE ✗.
**Textes à l'écran (EN) :** « 2019 · physics in the loss » · « 2021 · maps between fields » · « 2024 · pretrained
on many flows » · « 2023 · 2D MHD · laminar » · « 2025 · 2D MHD · turbulent » · « 2022 · no reliable precursor of
flips » · « 2024 · MSE ensembles: 'regress to the mean flow' » · puces « quote: arXiv preprint 2024 (Molinaro
et al.) · published 2026 (Raonić et al., Nat. Commun.) », « illustration · a mean-square fit returns the
average » · référence « Gwirtz et al. 2022, Geophys. J. Int. » · calque formule (minimiseur de l'erreur
quadratique) · badge CONTEXT.
**Voix off :**
> Un substitut rapide est un réseau de neurones entraîné à reproduire les résultats d'un solveur numérique à
> moindre coût. Pour les fluides conducteurs, ces substituts atteignent la turbulence bidimensionnelle. Appliquées
> au champ terrestre, les méthodes testées par Gwirtz et ses coauteurs en 2022 n'ont pas identifié de précurseur
> fiable des inversions.
>
> Entraînés à minimiser une erreur quadratique moyenne, ces modèles tendent vers l'écoulement moyen : une
> distribution à deux polarités se réduit alors à sa moyenne, nulle.

**Note :** l'image v3 de la « boussole moyenne » est retirée ; l'encart à deux bosses de v2 suffit.

## SOA2.3 · Les modèles génératifs · ≈ 30 s · reprend SOA2.3
**On voit :** la piste GENERATIVE MODELS s'éclaire.
**Animation :** sur « distribution entière » : l'encart à deux bosses revient, en violet, et garde ses deux
bosses. Sur « 2014 », « 2020 », « 2023 » : trois repères violets, le troisième étiqueté « E1 used this ». Sur
« tridimensionnelle », « météorologique », « paramètres » : petit cube, petit globe, petit cran de bouton vert.
Sur « aucun » : une case violette vide en pointillés à 2026, « dynamo fields · none found ». Puis la ligne de
cases : 3D ✓, WALLS ≈, LOW Pm ✗, RARE ≈.
**Textes à l'écran (EN) :** « 2014 · adversarial networks » · « 2020 · diffusion » · « 2023 · flow matching » ·
« 2024 · 3D turbulence » · « 2025 · weather ensembles » · « 2026 · statistics of 3D flows » · « 2026 · steady
turbulent states, conditioned · preprint » · « 2026 · dynamo fields · none found » · puce « none found ·
literature search to 6 Nov 2026, re-checked 8 Nov 2026 » · badge CONTEXT.
**Voix off :**
> Les modèles génératifs apprennent la distribution entière des données, et non sa seule moyenne. Après les
> réseaux antagonistes en 2014, la diffusion en 2020 et le flow matching en 2023, méthode employée par l'étude,
> ils produisent de la turbulence tridimensionnelle, des ensembles de prévision météorologique et des états
> turbulents conditionnés par des paramètres. La recherche bibliographique du projet, arrêtée au 6 novembre
> 2026, n'a recensé aucun modèle génératif entraîné sur des simulations de dynamo.

## SOA2.4 · Les méthodes de contrainte · ≈ 28 s · reprend SOA2.4 (premier paragraphe ; passage L4 → L5)
**On voit :** la piste CONSTRAINTS s'ouvre en quatre brins : HARD, SOFT, DISTRIBUTIONAL, SYMMETRY. Le rail des
niveaux monte de L4 à L5 (3 s).
**Animation :** un brin s'allume par phrase, ses repères s'inscrivent. Sur « potentiel vecteur » : le calque
formule (rotationnel d'un potentiel, projection de Leray). Sur « distribution » : brin DISTRIBUTIONAL en ambre,
quatre repères. Sur « équivariant » : brin SYMMETRY ; un petit nuage à deux bosses se replie sur lui-même dans le
miroir.
**Textes à l'écran (EN) :** « CONSTRAINTS » · « HARD » · « SOFT » · « DISTRIBUTIONAL » · « SYMMETRY » · les
repères de SOA2.4 v2 (« 2022 · divergence-free networks », « 2025 · projection at sampling time », « 2025 · PDE
residual in the loss », « 2026 · PBFM · physics vs distribution », « 2020 · covariance imposed on a
generator », « 2026 · weak Fokker–Planck as a loss · up to dimension 100 », « 2023 · equivariant flow
matching », etc.) · badge CONTEXT.
**Voix off :**
> Les méthodes de contrainte forment quatre familles. Les contraintes exactes intègrent la loi à
> l'architecture, par exemple au moyen d'un potentiel vecteur, ou projettent chaque échantillon pendant la
> génération. Les contraintes approchées ajoutent une pénalité à la perte. Les contraintes statistiques portent
> sur la distribution, par sa covariance ou par l'équation que vérifie une distribution stationnaire. Enfin, un
> générateur équivariant produit une distribution symétrique.

## SOA2.4b · L'absence de parois · ≈ 27 s · reprend SOA2.4 (second paragraphe)
**On voit :** les quatre brins, la plupart des étiquettes réduites à des points.
**Animation :** sur « aucune stratégie » : une puce de comparaison s'étend sur les quatre brins à 2026. Sur
« périodique » : un cube en fil de fer avec ses copies fantômes. Sur « couronne solaire » : une sphère avec des
boucles de champ. Sur « Aucun » : sur le brin HARD, une case vide en pointillés avec un petit cylindre (paroi,
disque de fer hachuré, halo pointillé du vide). Puis la ligne de cases CONSTRAINTS se remplit.
**Textes à l'écran (EN) :** « 2026 · 'no single strategy dominates' · divergence only, 2D · preprint » · « 2026 ·
Leray · 3D periodic · preprint » · « 2025 · current-free field · Sun's corona · preprint » · « 2026 · walls ·
vacuum · iron · none found » · puce « preprint: not peer-reviewed » · références Genuist et al. 2026 ; Li,
Buzzicotti, Bonaccorso, Biferale 2026 ; da Silva et al. 2025 · badge CONTEXT.
**Voix off :**
> D'après une prépublication de Genuist et ses coauteurs, qui compare en 2026 plusieurs façons d'imposer une
> divergence nulle à des écoulements plans, aucune stratégie ne domine. En trois dimensions, deux générateurs à
> divergence exactement nulle ont été recensés, tous deux en prépublication : l'un en domaine périodique,
> l'autre pour un champ sans courant dans la couronne solaire. Aucun ne traite de parois, de vide extérieur ni
> de fer.

## SOA2.5 · L'assimilation de données · ≈ 29 s · reprend SOA2.5
**On voit :** la piste ASSIMILATION PRIORS s'éclaire ; en tête de piste, une courbe de modèle et trois points de
mesure.
**Animation :** sur « mesures éparses » : les trois points se posent et tirent la courbe vers eux. Sur « espaces
latents » puis « diffusion » : les repères s'inscrivent ; deux anneaux « S. CHENG » (légende « ring = co-signed by
a supervisor », 3 s). Sur « aucun » : case vide « conducting fluids · none found ». Sur « deux polarités » :
encart à deux bosses ; sur « symétrie miroir », un a priori gris dissymétrique glisse dessous et la bosse de
gauche s'affaisse ; la ligne du miroir s'allume et les bosses se remettent à niveau.
**Textes à l'écran (EN) :** « 2021 · latent-space assimilation » · « 2022 · generalised latent assimilation » ·
« 2023 · score-based assimilation » · « 2024 · diffusion priors · weather scale » · « 2025 · TorchDA · deep nets
in Kalman and variational methods » · « 2026 · conducting fluids · none found » · « +D », « −D », « prior
ignores the mirror » · puces « illustration · no numbers », « none found · search to 6 Nov 2026 » · calque
formule (loi a posteriori) · badge CONTEXT.
**Voix off :**
> L'assimilation de données combine un modèle et des mesures éparses à partir d'un a priori, la distribution
> attendue avant la mesure. Des a priori appris ont été introduits par des espaces latents, puis par
> des modèles de diffusion ; aucun n'a été recensé pour les fluides conducteurs. Près d'une inversion, la
> distribution recherchée comporte deux polarités, et un a priori qui ne respecte pas la symétrie miroir
> pourrait la biaiser vers l'une d'elles.

## SOA2.6 · Les travaux des encadrants · ≈ 40 s · reprend SOA2.6
**On voit :** l'axe du temps se rouvre sur 1995–2031, la bande DYNAMO TRACKS se déplie en ses quatre couloirs.
Seuls les anneaux et les losanges gardent une étiquette, avec les noms en capitales.
**Animation :** sur « cosignés » : tous les anneaux s'allument. Sur « Taylor-Green » : les anneaux de
SIMULATIONS. Sur « deux codes » : les deux anneaux « CODE ». Sur « inversions » : les losanges (glyphe
d'inversion, petite icône D Q V U) ; légende « diamond = declares MilaDy funding », 3 s. Sur « apprentissage » :
les anneaux de SURROGATES et de GENERATIVE MODELS, dont « D. LUCOR, C. NORE » avec la sous-étiquette grise « not
MilaDy-funded ». Sur « Aucun » : la puce de la recherche négative.
**Textes à l'écran (EN) :** les étiquettes des anneaux et losanges de SOA2.6 v2 (C. NORE · 1997 …, Y. PONTY ·
2005 …, D. LUCOR …, S. CHENG …) · « dynamo simulations and a reversal model » · « representation learning on
von Kármán flows » · « assimilation and generative surrogates, outside MHD » · référence « Bousquet, Ponty,
Botez, Plihon, Nore 2026, Phys. Rev. Fluids » · puces « none of the four: a generative model trained on dynamo
data · none found (search to 6 Nov 2026) », « names in text only · what each paper showed, no opinions » ·
badge CONTEXT.
**Voix off :**
> Les repères cerclés désignent des articles cosignés par les encadrants du projet. Du côté des dynamos, ils
> portent sur des dynamos de Taylor-Green à faible nombre de Prandtl magnétique et sur l'expérience V K S,
> simulée dans deux codes. En 2026, les deux codes ont reproduit des inversions de
> V K S, et un modèle réduit à quatre modes en restitue les principales caractéristiques. Du côté de
> l'apprentissage, ils portent sur des autoencodeurs appliqués à l'écoulement de von Kármán, et sur
> l'assimilation et la diffusion hors des fluides conducteurs. Aucun ne présente de modèle génératif entraîné
> sur des données de dynamo.

**Note :** aucun nom d'encadrant n'est prononcé (BRIEF D6) ; les noms ne sont qu'à l'écran.

## SOA2.7 · L'intersection non couverte · ≈ 35 s · reprend SOA2.7 (premier paragraphe et cinq lacunes)
**On voit :** retour à l'axe 2012–2031. Les pistes GENERATIVE MODELS et CONSTRAINTS s'éclairent faiblement ; une
bande verticale en pointillés monte de leur croisement jusqu'à la bande DYNAMO TRACKS, sur 2027–2030.
**Animation :** sur « aucun travail recensé » : la bande reste vide, 1 s. Sur « projet de thèse » : l'anneau
THESIS de chSOA1 glisse dans le croisement, « THESIS · 2027-2030 · PLANNED ». Sur chaque lacune : un repère
numéroté s'ouvre autour de l'anneau, suivi 0,6 s plus tard de son voisin le plus proche, en gris.
**Textes à l'écran (EN) :** « THESIS · 2027-2030 · PLANNED » · « independent proposal · not requested or
validated by the supervisors » · « 1 · a generator of dynamo fields » · « 2 · ∇·u = ∇·B = 0 exactly · walls,
iron, vacuum » · « 3 · budgets on the distribution · no target · no data needed » · « 4 · flip rate from
snapshots · Rice » · « 5 · across the dynamo threshold » · les cinq puces « voisin » de v2 · puce « empty =
nothing found · search to 6 Nov 2026, re-checked 8 Nov 2026 » · badge PLANNED.
**Voix off :**
> À l'intersection des modèles génératifs, des contraintes et des dynamos, aucun travail n'a été recensé. Un
> projet de thèse indépendant, ni demandé ni validé par les encadrants, vise cette intersection et identifie
> cinq lacunes : un générateur de champs de dynamo ; des champs à divergence exactement nulle dans un cylindre
> avec fer et vide ; des bilans d'énergie imposés à la distribution, sans valeur cible ni données ; la fréquence
> des inversions déduite d'instantanés par la formule de Rice ; un générateur unique qui traverse le seuil de
> l'effet dynamo.

## SOA2.7b · Éléments déjà testés · ≈ 14 s · reprend SOA2.7 (dernier paragraphe)
**On voit :** l'anneau et ses cinq repères.
**Animation :** sur chaque exemple, une étiquette MEASURED s'accroche aux repères 2, 3 et 4, avec son seul
verdict (✓, ≈, « far ≈ · near ✗ »). Puis la ligne de cases de la thèse : 3D ?, WALLS ?, LOW Pm ✗, RARE ?.
**Textes à l'écran (EN) :** « E2 · potentials · exact on a flat sheet » · « E2 · budget imposed without data ·
still far from the data » · « E1 · Rice on three dials · far ≈ · near ✗ » · MEASURED.
**Voix off :**
> L'étude a testé trois de ces éléments sur des modèles réduits : les potentiels exacts en deux dimensions, un
> bilan imposé sans données et la formule de Rice sur le modèle à trois variables.

## SOA2.8 · Travaux voisins et limites · ≈ 32 s · reprend SOA2.8
**On voit :** retour à la carte entière ; les cinq repères réduits en cinq points autour de l'anneau.
**Animation :** sur « ICLR » : le repère PBFM s'éclaire, carte-citation en italique. Sur « situé » : un carré creux
« prospective report » apparaît sur le brin DISTRIBUTIONAL, relié au repère PBFM par un trait gris à double
pointe « to be positioned ». Sur « ne prétend » : titre gris NOT CLAIMED et quatre étiquettes posées sur leur
ancre. Sur « non une preuve » : chaque zone vide de la carte reçoit une loupe qui la balaie une fois.
**Textes à l'écran (EN) :** « 2026 · PBFM · physics vs distribution » · « “Our work is the first to recognize the
trade-off between distributional and physical accuracy.” » · « Baldan, Liu, Guardone, Thuerey · ICLR 2026 » ·
« PROSPECTIVE REPORT · NOV 2026 · per-snapshot budget: inconsistent » · « to be positioned » · « NOT CLAIMED » ·
« waiting times between flips » · « sodium's Pm » · « the Earth's core » · « real laboratory data » · puce
« searched to 6 Nov 2026 · re-checked 8 Nov 2026 · to be re-checked before every paper » · badge CONJECTURE
(medium).
**Voix off :**
> Un article de la conférence ICLR 2026 affirme être le premier à identifier un compromis entre
> exactitude physique et fidélité à la distribution ; le résultat de l'étude sur les contraintes imposées à
> chaque instantané doit être situé par rapport à lui. Le projet ne traite ni les temps d'attente entre
> inversions, ni le nombre de Prandtl magnétique du sodium, ni le noyau terrestre, ni des données
> expérimentales. Une case vide sur la carte est un résultat de recherche bibliographique, non une preuve.

**Durée totale estimée :** 4 min 55 s · **Mots :** ≈ 720

**Points à valider :**
1. Durée (≈ 295 s) juste sous la somme des `target_s` v2 (300 s, carte-question comprise) ; SOA2.5 peut
   sortir de la version courte (− 29 s), l'assimilation restant dans les questions ouvertes (Q35).
2. Le plan chSOA2.Q est supprimé ; sa question (Q15, grille périodique de LATU ou maillage cylindrique de
   SFEMaNS pour les premières données V K S) est reprise dans l'unité « Ouvertures », ainsi que Q31 (PBFM).
3. Vocabulaire des quatre familles de SOA2.4 : *hard* = contrainte exacte, *soft* (pénalité) = contrainte
   approchée, *distributional* = contrainte statistique. Le glossaire rend *soft* par « statistique » : ici,
   *soft* et *distributional* sont deux familles distinctes, d'où « approchée » pour la pénalité.
4. Simplifications à l'oral (tout reste à l'écran) : les familles de substituts, TorchDA, le théorème de
   Zel'dovich, la valeur de Pm du sodium, la phrase « dans ce que nous avons trouvé » devenue « aucun travail
   recensé ». Seuls Gwirtz et ses coauteurs (2022) et Genuist et ses coauteurs (2026) sont nommés à l'oral.
5. La transition vers ch10 (« marche par marche ») est retirée ; ch10 s'ouvre sur sa propre définition de
   l'escalier.
