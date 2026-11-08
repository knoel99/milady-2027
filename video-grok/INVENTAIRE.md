# Inventaire de contenu

Commit source : `4e42429716c093df34ba05b47ada542a13d39c50`.

Règle : un chiffre à l’écran doit apparaître ici avec `fichier:ligne`. Si deux fichiers arrondissent différemment, les deux lignes sont citées et `INCERTITUDES.md` dit laquelle montrer. Les faits externes sans ligne dans le dépôt sont **bloqués** (`INCERTITUDES.md` §E), pas inventés.

Pastilles : MEASURED (E1–E3), PROVED (énoncé démontré dans le rapport), CONJECTURE (confiance haute / moyenne / faible), PLANNED (plan de thèse), CONTEXT (fait externe déjà sourcé dans le dépôt).

## 1. Progression L0–L5

Échelle du brief, pas celle des modules de prépa (L1 universitaire ≠ L1 du film).

| Niveau | Public | Ce que le cœur a le droit d’introduire | Préparation du site (carte, pas un script) |
|---|---|---|---|
| L0 | tout public | boussole, champ qui change de sens, question « how often », illustration hors échelle | — |
| L1 | lycée / début de licence | étirement contre diffusion, Rm comme rapport, seuil, trois expériences de sodium en récit | `en/prep/index.qmd:52-53` modules 1 et 3, niveau universitaire plus haut que L1 film |
| L2 | licence scientifique | équation d’induction nommée sans dérivation, VKS avec ses chiffres sourcés, trois modes de Gissinger comme histoire, stationnarité en une phrase | modules 2–4 |
| L3 | M1 physique ou apprentissage | flow matching conditionnel, classes C1–C4, formule de Rice énoncée, tableau E1–E3 lu contre un plancher | modules 5–7 |
| L4 | M2 / début de thèse | propositions nommées, corollaire 6, estimateur sans biais, limites (graines, interpolation, modèles faibles), carte du champ | module 8 |
| L5 | encadrants | jauge, parois, fer, SFEMaNS, critères chiffrés des paliers, budget, questions qui décident d’un calcul | `en/these/index.qmd`, `en/calcul/index.qmd` |

Le cœur monte seulement. Les modules `x01`–`x05` sont L4–L5 et sortent du montage de 41 min. Un récapitulatif visuel ferme L2 (`g06`) et L4 est porté par la carte du champ (`g12`) plus le palier « Before we compute ».

## 2. Cadre du projet (CONTEXT, site)

| Affirmation autorisée | Source |
|---|---|
| Stage M2 « Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems », printemps 2027, 5 à 6 mois, surtout au CEREA (ENPC, IPP, Champs-sur-Marne) | `en/index.qmd:72` |
| Encadrement : Sibo Cheng (ENPC) et Didier Lucor (LISN, Université Paris-Saclay), avec Caroline Nore (LISN) et Yannick Ponty (OCA, CNRS). Télétravail 1 à 2 jours par semaine | `en/index.qmd:72` |
| Offre : modèles génératifs conditionnels (diffusion ou flow matching), contraintes dont budget d’énergie et divergence nulle, paramètres de contrôle, champs 3D pour modèles réduits et assimilation | `en/index.qmd:64-68` |
| MilaDy, ANR-25-CE51-0077, titre anglais *Machine learning modelling for turbulent Dynamos*, coordination Caroline Nore, partenaires LISN, Lagrange (OCA), CEREA. Début janvier 2026, 48 mois. Financement ANR 560 612 € | `en/encadrants/index.qmd:56-62`, rappel `en/index.qmd:78` |
| Deux objectifs : (i) renversements et dynamos explosives, phases précurseur / renversement / récupération ; (ii) optimiser DRESDYN par modèles réduits paramétriques (rapport des fréquences précession / rotation) | `en/encadrants/index.qmd:72-78` |
| Le site est indépendant, non endossé par l’ENPC, le LISN, l’OCA, l’ANR ni les encadrants. Le rapport est prospectif | `en/index.qmd:43-45` |
| Trois offres publiques : stage 2026 (représentation), postdoc 24 mois annoncé en janvier 2026 (contacts Nore et Lucor ; annonce ensuite absente de la page de Lucor ; recrutement non établi), stage 2027 (génération) | `en/encadrants/index.qmd:86-92` |
| Thèse proposée : fusion des pistes A et B. Générateur d’instantanés conditionnel, pas un générateur de trajectoires comme objet principal | `en/encadrants/index.qmd:443-453` |
| Scores des six pistes : jugements de l’auteur du site, non validés par les encadrants. A 4,10 ; B 3,90 ; F 3,50 ; E 3,40 ; D 3,20 ; C 3,00 (poids du site). Le 4,45 de la fusion est « favorable par construction » | `en/encadrants/index.qmd:420-437`, `en/encadrants/index.qmd:451` |
| Financement des derniers mois d’une thèse automne 2027 → automne 2030, au-delà de la fin nominale du projet : non documenté | `en/these/index.qmd:982` |

Noms à l’écran seulement (générique, bandeau). Pas de photo, pas de logo, pas d’opinion prêtée.

## 3. Physique déjà sourcée dans le dépôt (CONTEXT)

Base : `specs/sources/dynamo.md`, contre-vérifiée le 2026-11-06 (`dynamo.md:3-16`). Le film cite la source primaire, pas seulement la note, et garde les réserves du §7 et du §9.

### 3.1 Seuils et nombres sans dimension

| Fait | Valeur | Ligne |
|---|---|---|
| Pm du sodium | « about 10⁻⁵ » ; à 120 °C, Pm = μ₀σν = 0,82×10⁻⁵ (ν = 6,78×10⁻⁷ m²/s, ρ = 932 kg/m³, σ = 9,6×10⁶ S/m), d’après Nore 2018 §2.1 | `dynamo.md:35` |
| Rm | UL/η, induction contre diffusion ; dynamo au-dessus d’un seuil | `en/rapport/index.qmd:137` |
| Trois expériences sodium auto-excitées, plus DRESDYN (cylindre en précession, en cours, Allemagne) | récit du résumé MilaDy, repris par le rapport | `en/rapport/index.qmd:86` |

### 3.2 Riga

Gailitis et al. 2000, PRL 84, 4365–4368, DOI 10.1103/PhysRevLett.84.4365. `dynamo.md:51-62`.

- Campagne 6–11 novembre 1999. Auto-excitation à 2150 tr/min, 205 °C : mode A₂ = 0,133 mT, p₂ = 0,0315 ± 0,0009 s⁻¹, f₂ = 1,326 Hz.
- Géométrie : D1 = 0,25 m, D2 = 0,43 m, D3 = 0,80 m, L = 2,91 m. Sodium 2 m³. Débit jusqu’à 0,6 m³/s. Deux moteurs de 55 kW dans le PRL 2000.
- Réserves : 2×100 kW dans le C. R. Physique 2008 ; « up to 200 kW » dans Gailitis et al. 2018. Première tentative 1986 ou 1987 selon la source. Débit 0,67 m³/s **non confirmé** (`dynamo.md:703-705`). Ne pas l’afficher.

### 3.3 Karlsruhe

- Premier fonctionnement réussi en décembre 1999, « quelques semaines » après Riga (Rädler & Brandenburg 2003, PRE 67, 026401). `dynamo.md:106`.
- 52 générateurs, R = 0,85 m, H = 0,71 m, a = 0,21 m. Rm critique de conception < 10. Débit de conception 115–143 m³/h. `dynamo.md:37`, `dynamo.md:94`.
- Champ saturé stationnaire de type dipôle, deux états quasi équivalents. À 115 m³/h : B_Y moyen = 260 G, RMS = 0,58 G. `dynamo.md:97-98`.
- Stieglitz & Müller 2001 : texte intégral payant non lu ; ne pas ajouter de chiffres au-delà du résumé (`dynamo.md:85-88`, `dynamo.md:613`).

### 3.4 VKS — ne jamais superposer des Rm de définitions différentes

| Fait | Valeur | Ligne |
|---|---|---|
| Monchaux et al. 2007, PRL 98, 044502 | disques rayon 154,5 mm, écart 371 mm, cylindre 2R = 412 mm, longueur 524 mm, 8 pales de hauteur 41,2 mm, jusqu’à 26 Hz, 300 kW, sodium 150 l | `dynamo.md:116-120` |
| Inox : pas de dynamo jusqu’à 26 Hz. Fer doux : dynamo au-dessus de Rm ≈ 30 | | `dynamo.md:124-125` |
| Avec K ≈ 0,6 : Rm_c ≈ 31 (ajustement de ⟨B_y⟩ ou B_rms) ; R′m ≈ 35 (ajustement de ⟨B²⟩) | | `dynamo.md:126-127` |
| Re jusqu’à 5×10⁶ ; Rm max ≈ 49 à 120 °C | | `dynamo.md:122` |
| ~40 G quand Rm passe de 19 à 40 ; fluctuations 3 à 8 G à 30 % au-dessus du seuil | | `dynamo.md:131-132` |
| Berhanu et al. 2007, EPL 77, 59001 | premiers renversements B → −B en laboratoire, turbines à fréquences différentes | `dynamo.md:138-140` |
| Régime de renversements | F1 = 16 Hz, F2 = 22 Hz, T = 123 °C ; ⟨T+⟩ = 120 s, ⟨T−⟩ = 50 s ; τ ≈ 5 s ; temps intégral ≈ 0,05 s ; temps ohmique ≈ 0,4 s | `dynamo.md:148-149` |
| Volume sodium | ≈ 160 L dans Berhanu 2007, 150 l dans le PRL 2007 | `dynamo.md:143`, réserve `dynamo.md:619` |
| Monchaux 2009 | autre définition encore ; +w : Rm_c = 32 ; −w/o : Rm_c ≈ 43 ; μr ≈ 100 | `dynamo.md:159-165` |
| Miralles 2013 | Rm sans le facteur K : Rm_c ≃ 44 (fer/fer, pales courbes) | `dynamo.md:182-184` |
| Nore et al. 2018 | définition sans K : dynamo pour 16–22 Hz, 52 ≤ Rm_c ≤ 71. Pm = 0,82×10⁻⁵ | `dynamo.md:215-220` |
| Même article, Table 3, Re = 1,5×10³, μr = 50 | H×n = 0 : Rm_c = 90 ± 5 ; condition de vide : 130 ± 10, « about 40 % » de plus | `dynamo.md:223-225`, rappel rapport `en/rapport/index.qmd:143` |
| Table 4, μr = 50, H×n = 0 | Rm_c de 135 ± 5 à Re = 500 jusqu’à 70 ± 5 à Re = 10⁵ | `dynamo.md:228-230` |
| Anneau médian | diamètre intérieur 175 mm (PRL 2007) contre rayon 175 mm (Berhanu) et diamètre 350 mm (Monchaux 2009). Coquille probable du PRL. Ne pas figer une cote | `dynamo.md:136` |

La figure VKS du site est **qualitative** : courbes issues de la forme normale de Pétrélis & Fauve 2008 avec bruit et paramètres choisis à la main, « neither the durations nor the amplitudes are those of VKS » (`en/rapport/index.qmd:163`). Pastille CONTEXT pour la géométrie sourcée, jamais MEASURED pour ces courbes.

### 3.5 Modèles de renversement publiés

Équations de Gissinger 2012, EPJB 85, 137, arXiv:1109.6569, convention μ sur Q (`dynamo.md:311-317`) :

dQ/dt = μQ − VD, dD/dt = −νD + VQ, dV/dt = Γ − V + QD.

Symétrie (D, Q, V) → (−D, −Q, V), image de B → −B (`dynamo.md:322`).

- Pour ν = 0,1 et Γ = 0,9, crise à μ_c ≈ 0,11928. À μ = 0,119, renversements chaotiques, λ ≃ 0,1. À μ = 0,12, chaos sans renversement (`dynamo.md:345-351`).
- L’article varie **μ** à Γ = 0,9. E1 varie **Γ** à μ = 0,119 fixé. Ce n’est pas le même chemin (`en/rapport/index.qmd:784`).
- Coquilles de l’arXiv v2 à ne pas « corriger » en silence : « dissipative for μ > 1+ν » alors que la divergence μ − ν − 1 est négative pour μ < 1+ν ; légende Fig. 11 avec Γ = 0,1 au lieu de 0,9 (`dynamo.md:321`, `dynamo.md:367`).
- Vérification interne d’équipe (pas un fait publié) : 74 renversements à μ = 0,119 sur le script RK4 (`dynamo.md:372-380`). Ne pas la présenter comme le résultat E1.
- Pétrélis & Fauve 2008 : θ̇ = μᵢ − ρ sin 2θ ; bifurcation nœud-col à μᵢ = ρ (`dynamo.md:266-270`).
- Pétrélis et al. 2009 : paramètres de **leur** figure, ⟨T⟩ ≈ 170 kyr. C’est un ajustement de modèle, pas une mesure géologique à afficher comme « le » taux terrestre (`dynamo.md:285-287`).
- Gissinger, Dormy & Fauve 2010 : mêmes trois modes avec D et Q échangés (`dynamo.md:298-303`).
- Bousquet et al. 2026, Phys. Rev. Fluids 11, 063703, DOI 10.1103/9tx2-1m13. Simulation de référence Re = 1594, Rm = 531, asymétrie (F1−F2)/(F1+F2) = 0,058, μr = 16. POD sur 2000 instantanés, quatre modes axisymétriques, modèle DQVU. Données non publiques (`en/rapport/index.qmd:161`, `en/encadrants/index.qmd:98`).
- Un milieu extérieur conducteur a été nécessaire aux renversements dans la gamme explorée (`en/encadrants/index.qmd:98`).
- DQVU reproduit la bimodalité asymétrique de V ; la distribution de Q n’est reproduite qu’imparfaitement (`en/encadrants/index.qmd:265`).

### 3.6 ABC, anti-dynamos, Taylor–Green

| Fait | Valeur | Ligne |
|---|---|---|
| ABC 1:1:1, Rm = 1/η | fenêtres publiées 8,9 < Rm < 17,5 (fermée) et Rm > 27, citées par Archontis et al. 2003 d’après Galloway & Frisch 1984. PDF primaire inaccessible (403) | `dynamo.md:41`, `dynamo.md:393`, `dynamo.md:706` |
| Maximum de croissance dans la 1re fenêtre | vers Rm = 12 selon Archontis citant Galanti et al. 1993 ; **la valeur du taux n’est pas connue** | `dynamo.md:395`, `dynamo.md:706` |
| Alexakis 2011 | R_M = √3/η pour l’ABC 1:1:1, pas 1/η | `dynamo.md:412` |
| Cowling 1933 | un champ axisymétrique qui s’annule à l’infini ne peut pas être entretenu (énoncé via Tobias) | `dynamo.md:435-437` |
| Zel’dovich 1957 | un écoulement plan ne peut pas être une dynamo (énoncé via Tobias §2.4.3 ; original non lu au-delà des métadonnées) | `dynamo.md:441-442` |
| Donc E2 n’est pas une dynamo | le champ magnétique y est entretenu par le forçage f_a | `en/rapport/index.qmd:925` |
| Ponty et al. 2005, PRL 94, 164502 | Taylor–Green, R_M^c = 30 à P_M = 1, 226 à P_M = 0,3, ≈ 200 à P_M = 0,2, LES ≈ 150 pour 10⁻² ≤ P_M ≤ 10⁻¹ | `dynamo.md:581-583` |
| Ponty et al. 2007 | bifurcation sous-critique ; fenêtre cinématique sur l’écoulement moyen [22, 51] puis branche haute R_M^{c3} ≈ 158 (±15 %) | `dynamo.md:600-604` |
| Kreuzahler et al. 2017 | LATU, boîte (3π)³, 384³, pénalisation, sauts de μr | `dynamo.md:238-239` |

### 3.7 DRESDYN

- Expérience de précession au HZDR (Dresde), objectif (ii) (`en/encadrants/index.qmd:78`).
- Botez et al. 2026, Phys. Rev. Fluids 11, 083701 : dynamo cinématique sur des champs de vitesse moyennés ; dynamo vraisemblable seulement dans une « narrow range » du nombre de Poincaré ; deux familles de modes ; les conditions aux limites simplifiées (champ tangentiel nul) sous-estiment systématiquement Rm_c (`en/these/index.qmd:943`, `en/encadrants/index.qmd:100`).
- Aucun chiffre de fenêtre en Po n’est donné dans les pages lues. Ne pas en inventer.
- Nore et al. 2011, PRE 84, 016317 : démonstration numérique qu’une précession peut entretenir une dynamo dans un cylindre (`en/encadrants/index.qmd:183`).
- Le palier 4 est le premier abandonné en cas de retard (`en/these/index.qmd:953`, `en/these/index.qmd:999`).

### 3.8 Faits demandés par le brief et absents du dépôt

Bandes magnétiques des fonds océaniques, date du dernier renversement géomagnétique, dynamo à disque, Larmor, Glatzmaier–Roberts, théorie du champ moyen comme chapitre historique : **aucune ligne** dans `specs/sources/` au moment de cette lecture. Statut `blocked-source`. Le siècle des dynamos peut nommer Cowling, Riga, Karlsruhe, VKS, DRESDYN, les simulations VKS de Nore et les modèles réduits déjà cités. Il ne donne pas d’année ni de taux pour les entrées bloquées tant que la relecture science n’a pas ajouté une source datée dans un fichier sous `video-grok/` (sans rien commettre hors de ce dossier).

## 4. Théorie du rapport (PROVED dans le périmètre écrit)

Le rapport dit que plusieurs énoncés sont classiques ou élémentaires et que six points sont, **à sa connaissance au 6 novembre 2026**, non trouvés dans la littérature (`en/rapport/index.qmd:118-125`). Une absence n’est pas une preuve (`en/rapport/index.qmd:228`). Confiance de l’étiquette « aucun modèle génératif de dynamo publié » : moyenne, datée, à revérifier avant chaque article (`en/these/index.qmd:163`).

| Id | Énoncé utilisable à l’écran | Ligne |
|---|---|---|
| Déf. 3.1 | instantanés d’un régime statistiquement stationnaire ; μ_λ mesure invariante | `en/rapport/index.qmd:264-278` |
| Déf. 3.2 | flow matching conditionnel, chemin linéaire, perte de régression | `en/rapport/index.qmd:281-294` |
| Déf. 3.3 | C1 linéaire locale, C2 non linéaire locale, C3 symétrie de la loi, C4 identité de stationnarité | `en/rapport/index.qmd:308-317` |
| Rem. 3.4 | dE/dt = P − ε est une identité sur un instantané ; la contrainte est E[P − ε] = 0 | `en/rapport/index.qmd:319-322` |
| Prop. 1 | si l’image du décodeur est dans S, la divergence nulle est exacte quelle que soit la qualité de l’apprentissage | `en/rapport/index.qmd:326-333` |
| Prop. 2 | les mécanismes exacts visent la même loi ; la divergence d’un modèle libre vient d’une contraction en 1/(1−t) non représentée | `en/rapport/index.qmd:344-360` |
| Prop. 4 | un champ équivariant et une base invariante donnent une loi invariante pour **tout** λ, même sans donnée | `en/rapport/index.qmd:399-401` |
| Rem. 3.7 | les identités de stationnarité ne fixent pas le poids des deux polarités | `en/rapport/index.qmd:414-417` |
| Prop. 5 | invariance ⇒ E[Lφ] = 0 ; le budget d’énergie moyen est le cas φ = E | `en/rapport/index.qmd:421-424` |
| Cor. 6 | Hypothèse explicite : la loi de Lφ ne met pas de masse en 0. Une variance strictement positive ne démontre pas cette absence d’atome. Si l’hypothèse est admise, une loi portée par {Lφ = 0} est singulière et la KL vers μ est infinie. Si de plus Lφ est lipschitzienne, W1 est minoré par E\|Lφ\|/L. Le rapport ajoute qu’une densité rend l’hypothèse vraie, et appelle cela générique dès que la variance est positive (`:449`). Cette glose n’est pas une preuve, et la variance mesurée d’E1 ne l’est pas non plus. Ne pas écrire qu’une KL mesurée est infinie. | `en/rapport/index.qmd:447-455` |
| Prop. 7 | I-projection = inclinaison exponentielle ; un repondération ne crée pas de masse ; ESS = 1/Σ wᵢ² | `en/rapport/index.qmd:464-473` |
| Déf. 3.9 | perte de stationnarité, utilisable aux paramètres sans donnée | `en/rapport/index.qmd:487-496` |
| Ex. 4.2 | (moyenne)² a pour espérance (E g)² + Var(g)/n et pousse donc à réduire la variance ; le produit de deux demi-lots est sans biais | `en/rapport/index.qmd:662-676` |
| Prop. 8 | formule de Rice : fréquence des passages par 0 à partir de la loi et de F, sans intégration en temps. Hypothèses : processus stationnaire, trajectoires C¹, observable linéaire, densité continue du couple (D, Ḋ). Fenêtre h : biais O(h²), variance O(1/(Nh)) | `en/rapport/index.qmd:509-517` |
| Limites de Rice | F doit être connu ; tous les passages, y compris les excursions et le brouhaha autour de 0 ; pas la loi des temps d’attente ; pour une dynamique déterministe comme E1, la densité continue n’est pas garantie | `en/rapport/index.qmd:528` |
| Contrôle numérique de Rice | Les 4 % près du seuil et 6 % au-dessus, sur la référence, sont le contrôle de l’estimateur de fenêtre là où la densité n’est pas garantie. Ce n’est pas le théorème appliqué sous ses hypothèses. h = 0,2 | `en/rapport/index.qmd:883`, `:901` |
| Prop. 9 | un générateur lipschitzien en λ rate au moins la moitié du saut de la loi près d’une discontinuité | `en/rapport/index.qmd:543-557` |
| Rem. 3.11 | les identités sont nécessaires, non suffisantes | `en/rapport/index.qmd:568-571` |

E1 utilise neuf monômes de degré ≤ 2 comme tests et dix monômes de degré 3 comme contrôle (`en/rapport/index.qmd:434`).

## 5. Expériences MEASURED

Machine : Intel Xeon, 4 cœurs, 2,30 GHz, sans GPU. Python 3.13, NumPy 2.5, SciPy 1.18, Matplotlib 3.11, PyTorch 2.15 CPU (`en/experiences/index.qmd:43`). Graines E1 : 0 et 1. E2 : une graine par variante. Tests = interpolation en paramètre, jamais extrapolation (`en/rapport/index.qmd:743-745`).

Durées mesurées sur cette machine, en partie avec d’autres calculs : E3 1366 s ; E2 complet 4023 s ; dernier passage du script E1 3350 s, dont environ un quart d’heure d’évaluation. Ce ne sont pas des temps GPU (`en/experiences/index.qmd:68-75`, `experiences/resultats/digest.md:123`, `:166`, `:199`).

### 5.1 E1 — configuration

| Paramètre | Valeur | Ligne |
|---|---|---|
| μ, ν | 0,119 et 0,1 | `digest.md:5` |
| Γ d’entraînement | 0,80 ; 0,82 ; … ; 1,00 (11 valeurs) | `digest.md:5` |
| Γ de test | 0,81 ; 0,83 ; … ; 0,99 (10 valeurs) | `digest.md:5` |
| Trajectoires | 16 par Γ d’entraînement, 32 pour la référence, plus leurs images par S | `en/rapport/index.qmd:786` |
| Intégration | RK4, Δt = 0,01 ; transitoire 300 ; 3000 gardés ; un instantané toutes les 2 unités (1500 par trajectoire) | `en/rapport/index.qmd:786` |
| Itérations | A, B, C : 12 000 ; C court : 1 200 | `digest.md:5` |
| Réseau | MLP 256×4, SiLU ; Heun 50 pas ; 10 000 échantillons par Γ ; h_Rice = 0,2 | `digest.md:5`, `en/rapport/index.qmd:593-595` |
| Seuil mesuré | aucun passage de D par 0 jusqu’à Γ = 0,86 ; des passages dès Γ = 0,865 (0,00194 par unité de temps) | `en/rapport/index.qmd:871`, `digest.md:94` |
| Pont \|D\| < 0,25 | masse P(\|D\| < 0,25). Ce seuil n’est pas le diamètre D1 = 0,25 m de Riga (`dynamo.md:55`) | `en/rapport/index.qmd:729`, rappel figure `:807` et annexe `:1269` |
| Plancher d’asymétrie | √(2/π)·(1/2)/√n ≈ 0,0040 pour n = 10 000 | `en/rapport/index.qmd:832` |
| Plancher d’énergie (n_gen) | 0,0012269… | `digest.md:48` |
| σ_ref(dE/dt) | 0,37772… | `digest.md:49` |
| Erreur Rice de la référence (digest) | 0,000361… | `digest.md:49` |

Le digest donne σ(dE/dt) **absolu**. Le rapport, table 1, donne le **rapport** σ/σ_ref (`en/rapport/index.qmd:838`). À l’écran, écrire l’unité. Exemple : variante C, test, σ = 0,384 (`digest.md:14`) soit un rapport ≈ 1,02 dans la table du rapport (`en/rapport/index.qmd:840`). Projection E : σ = 4,17×10⁻¹⁷ dans le digest (`digest.md:19`), rapport 1,1×10⁻¹⁶ dans la table (`en/rapport/index.qmd:852`).

### 5.2 E1 — moyennes sur les Γ de test (deux graines)

Source primaire des barres : `digest.md:11-26`. Lecture du rapport : `en/rapport/index.qmd:834-853`. Distance d’énergie, SW1, |P(D>0)−1/2|, Liouville degré ≤ 2, Liouville degré 3, erreur de taux Rice :

| Variante | dist. énergie | asymétrie | Liouville ≤ 2 | Liouville deg. 3 | err. Rice |
|---|---|---|---|---|---|
| A référence | 0,0118 | 0,0322 | 0,0326 | 0,0167 | 0,00125 |
| B augmentation | 0,00356 | 0,0157 | 0,044 | 0,0223 | 0,00108 |
| C équivariant | 0,00257 | 0,00439 | 0,0265 | 0,0217 | 0,00106 |
| C court | 0,0043 | 0,00444 | 0,0322 | 0,0292 | 0,00316 |
| F stationnarité sur C | 0,0031 | 0,00344 | 0,0136 | 0,0113 | 0,0011 |
| F0 témoin sur C | 0,00345 | 0,00443 | 0,0324 | 0,0224 | 0,000835 (digest 8,35×10⁻⁴) |
| F sur C court | 0,0785 | 0,0032 | 0,456 | 1,72 | 0,00608 |
| E projection de C | 0,0231 | 0,00434 | 0,0359 | 0,0204 | 0,0026 |
| D inclinaison de C | 0,00483 | 0,0119 | 0,0448 | 0,0586 | 0,00155 ; ESS/N 0,851 |

Lecture autorisée, déjà écrite dans le rapport :

- Seule l’équivariance tient l’asymétrie au plancher **entre** les valeurs d’entraînement. L’augmentation la tient aux valeurs vues (0,0028 à 0,0063 sur les onze Γ d’entraînement) mais pas entre elles : 0,0203 à Γ = 0,81 et 0,0246 à Γ = 0,85 (`en/rapport/index.qmd:873`).
- À Γ = 0,86, P(D>0) des données = 0,3125 (5 trajectoires sur 16) ; asymétrie du modèle A = 0,183 (`en/rapport/index.qmd:859-871`).
- Distance d’énergie : 0,0118 (A) → 0,00356 (B) → 0,00257 (C), environ deux fois le plancher 0,00123 (`en/rapport/index.qmd:873`).
- La perte de stationnarité sur C, aux Γ de test, amène le résidu imposé de 0,0324 (témoin) à 0,0136 et le résidu de contrôle de 0,0224 à 0,0113. Le témoin ne gagne rien. Le rapport σ(dE/dt) passe de 1,04 à 0,75. La distance d’énergie bouge peu (0,00310 contre 0,00345), dans l’écart entre graines (`en/rapport/index.qmd:875`).
- Sur C court, une graine sur deux diverge (|x| ≈ 18, rapport de σ = 19,2). Les deux réglages fins sont jugés inutilisables par le rapport (`en/rapport/index.qmd:877`).
- L’inclinaison a posteriori n’améliore aucune distribution d’E1 (`en/rapport/index.qmd:879`).
- La projection par échantillon multiplie la distance d’énergie par 9 (0,0231 / 0,00257) et SW1 par 3 (0,107 / 0,0333) (`en/rapport/index.qmd:881`).
- Rice sur la référence : erreur cumulée 4 % près du seuil (0,865 ≤ Γ ≤ 0,885) et 6 % au-dessus (Γ ≥ 0,89). Sur C, graine 0, 20 000 échantillons : 14 % pour Γ ≥ 0,89, jusqu’à 65 % en un point (Γ = 0,905 et 0,91 ; à 0,91, 0,00937 contre 0,00567), et 42 % près du seuil. Le modèle donne 0,00030 à Γ = 0,865 contre 0,00194, puis 0,00500 contre 0,00340 à Γ = 0,88 (`en/rapport/index.qmd:883`, cellules `digest.md:94-103`).
- Passages parasites sous le seuil : au plus 2×10⁻⁴ par unité de temps (`en/rapport/index.qmd:883`).
- Deux graines seulement : ne retenir comme robuste qu’un facteur deux ou plus (`en/rapport/index.qmd:901`).

Page d’accueil : « cumulative error of 14% … (up to 65% at a single value) and of 42% at the threshold » (`en/index.qmd:87`). Le 65 % n’est pas « au seuil » ; il est ponctuel à Γ = 0,905 et 0,91. Le film ne doit pas fusionner les deux phrases.

Grille fine complète : `digest.md:79-121`. Taux à Γ = 1 : simulation 0,0112 (`digest.md:75` et `digest.md:121`).

### 5.3 E2 — configuration

| Paramètre | Valeur | Ligne |
|---|---|---|
| N, ν, α, bande | 32, 0,008, 0,02, [2, 3] | `digest.md:127` |
| η entraînement | 0,004 ; 0,00566 ; 0,008 ; 0,01131 ; 0,016 ; 0,02263 | `digest.md:127` |
| η test | 0,00476 ; 0,00673 ; 0,00951 ; 0,01345 ; 0,01903 | `digest.md:127` |
| Dimension | 220 modes, 880 (potentiels) ou 1760 (composantes) | `digest.md:127` |
| MLP, budget | largeur 1024, 6000 itérations, 1000 échantillons par η, 2400 instantanés d’entraînement par η | `digest.md:127` |
| Injection d’Itô mesurée | ε_u, ε_b, ε_{a²} = 0,04479 ; 0,04476 ; 0,00726 | `digest.md:127` |
| Le YAML `palier1_mhd2d` écrit eps_u = eps_b = 0,05 | ce n’est pas le taux d’Itô mesuré d’E2 | `infra/configs/palier1_mhd2d.yaml:25-26` |
| Pm | de 2 à environ 0,35 | `en/rapport/index.qmd:919` |
| Pas une dynamo | théorème de Zel’dovich ; forçage f_a | `en/rapport/index.qmd:925` |

### 5.4 E2 — moyennes sur les η de test

`digest.md:132-144`. Chiffres à l’écran, déjà interprétés dans `en/rapport/index.qmd:931-961` et `en/index.qmd:84-85` :

| Variante | div. rel. u | div. rel. B | err. spectre | err. E_B | résidu énergie | σ(D)/σ_ref | dist. énergie |
|---|---|---|---|---|---|---|---|
| V0 libre | 0,408 | 0,408 | 0,23 | 0,562 | 0,491 | 0,68 | 4,31 |
| V1 pénalité | 0,34 | 0,162 | 0,18 | 1,68 | 0,895 | 1,21 | 5,86 |
| V2 projection finale | 5,05×10⁻¹⁷ | 5,00×10⁻¹⁷ | 0,168 | 0,337 | 0,469 | 0,677 | 2,61 |
| V3 flot projeté | 2,03×10⁻⁸ | 2,03×10⁻⁸ | 0,135 | 0,236 | 0,335 | 0,565 | 1,85 |
| V4 potentiels | 1,78×10⁻¹⁷ | 1,68×10⁻¹⁷ | 0,168 | 0,369 | 0,472 | 0,672 | 2,58 |
| V5 potentiels + perte | 1,74×10⁻¹⁷ | 1,62×10⁻¹⁷ | 0,0696 | 0,0621 | 0,0611 | 0,788 | 0,699 |
| V5 témoin | 1,78×10⁻¹⁷ | 1,67×10⁻¹⁷ | 0,165 | 0,355 | 0,462 | 0,663 | 2,52 |
| sous-échantillon | 1,52×10⁻¹⁷ | 0 | 0,00212 | 0,00248 | 0,00661 | 0,998 | 0,00178 |
| inclinaison (moitié b) | ~10⁻¹⁷ | ~10⁻¹⁷ | 0,143 | 0,115 | 0,193 | 0,204 | 4,15 |
| recalage par échantillon | ~10⁻¹⁷ | ~10⁻¹⁷ | 0,0804 | 0,188 | 8,27×10⁻⁶ | 8,64×10⁻⁴ | 1,1 |

- « divise par environ 3,6 (0,70 contre 2,52) » compare V5 au **témoin** (`en/index.qmd:85`). 2,52 / 0,699 ≈ 3,6. Contre V4 (2,58), le facteur est un peu plus grand. Le dire explicitement.
- Erreur relative 1,68 sur E_B : le rapport en déduit une énergie magnétique moyenne 2,68 fois celle de la référence, parce qu’une erreur relative > 1 ne peut venir que d’un excès (`en/rapport/index.qmd:1025`). C’est une lecture, à étiqueter comme telle.
- Plancher de test 0,00178 **optimiste** (recouvrement). Plancher honnête, η d’entraînement : distance 0,0304 (`digest.md:160`). V5 reste loin du plancher (`en/rapport/index.qmd:1039`).
- ESS/N moyen de l’inclinaison : 0,287 (`digest.md:162`). À η = 0,00951 ; 0,01345 ; 0,01903 : ESS/N = 0,00215 ; 0,002 ; 0,002 (`en/rapport/index.qmd:1008-1012`).
- À η = 0,01903 (test) : distance V4 = 7,74, témoin 7,63, V5 = 2,22. Le rapport dit « divisée par 3,5 » en ce point (`en/rapport/index.qmd:1135`, table `en/rapport/index.qmd:1011`).
- Une graine : un écart de quelques dizaines de pour cent entre V2, V3 et V4 n’est pas significatif ; un facteur 3 l’est probablement, sans intervalle de confiance (`en/rapport/index.qmd:1175`).
- Topologie : aucune métrique calculée (`en/rapport/index.qmd:739`).
- U-Net périodique présent (`experiences/unet.py`) mais non utilisé dans les résultats finaux : environ 0,3 s par pas sur ce CPU (`en/experiences/index.qmd:101`).

### 5.5 E3 — MEASURED, sans modèle génératif

`experiences/resultats/e3_abc.json` et `digest.md:168-199`. N = 32, A = B = C = 1, dt = 0,05, t_total = 150, Rm = 1/η.

Seuils interpolés exacts du JSON (`e3_abc.json:167-171`) : 8,87069372523019 ; 17,602540347824316 ; 26,796269592804332. Affichage du rapport : 8,87 ; 17,6 ; 26,8 (`en/rapport/index.qmd:1099`).

| Point à ne pas lisser | Valeur | Ligne |
|---|---|---|
| Rm = 2, λ | −0,500053… (dernier quart −0,500007…) ; mode exact −1/Rm = −0,5 | `e3_abc.json:13-16`, `en/rapport/index.qmd:1116` |
| Rm = 12, λ | 0,007653 ; à N = 48, 0,008124 | `e3_abc.json:68`, `:160` |
| Rm = 17,5 | λ = +2,34×10⁻⁴ sur la seconde moitié, −2,17×10⁻⁴ sur le dernier quart, −5,20×10⁻⁴ à N = 48. Le signe n’est pas résolu | `e3_abc.json:104-106`, `:163`, `en/rapport/index.qmd:1114` |
| Second seuil | à environ 0,1 près de 17,5. 17,6 est l’interpolation de la seconde moitié, pas un intervalle de confiance | `en/rapport/index.qmd:1114` |
| Troisième seuil | connu à environ une unité près. Pas un intervalle de confiance | `en/rapport/index.qmd:1114` |
| Groupe ABC | le mode de la première fenêtre a les symétries paires du groupe, 24 éléments. Ne pas importer les autres nombres du même paragraphe (Rm1, Rm2, ω, σ à 25 000) | `dynamo.md:400`, `en/rapport/index.qmd:1120` |
| div. rel. maximale citée | 1,52×10⁻¹⁶ à Rm = 22 | `digest.md:191` |
| Durée | 1365,53 s dans le JSON ; 1366 s dans le digest | `e3_abc.json:172`, `digest.md:199` |
| Pas de générateur | E3 valide le solveur et les fenêtres | `en/these/index.qmd:97` |

Comparer à 8,9 / 17,5 / « au-dessus de 27 » (Archontis 2003), pas à une décimale de plus que la précision du taux (`en/rapport/index.qmd:1112-1114`).

## 6. Paliers de thèse (PLANNED)

Échelle : palier 0 Gissinger et DQVU ; 1 MHD 2D périodique ; 2 ABC et Taylor–Green 3D ; 3 VKS (SFEMaNS, LATU) ; 4 DRESDYN. Les paliers 0 à 2 prolongent E1–E3 (`en/these/index.qmd:857`).

Critères d’arrêt utiles aux cartes « question » :

- Palier 0 : (a) asymétrie sous le plancher à tout Γ ; (b) résidus de Liouville non imposés divisés par au moins 2 aux Γ sans donnée ; (c) fréquence de Rice à 20 % du comptage là où celui-ci est connu à mieux que 5 % ; (d) borne de la prop. 2.30 serrée à 30 %. Si (b) échoue avec l’estimateur sans biais et trois graines, abandonner la perte au profit de l’inclinaison — en sachant que l’inclinaison n’a amélioré aucune loi en E1 ni en E2 (`en/these/index.qmd:889-890`, risque `en/these/index.qmd:992`).
- Palier 1 : divergence relative < 10⁻¹² ; résidu de budget < 5 % aux paramètres sans donnée ; distance d’énergie divisée par ≥ 2 sans dégrader le spectre de plus de 10 % ; σ(dissipation)/σ_ref dans [0,8 ; 1,2] (`en/these/index.qmd:903`).
- Palier 2 : divergence < 10⁻¹² ; erreur de log-spectre < 0,1 décade par bande jusqu’à la moitié du nombre d’onde de coupure, aux paramètres d’entraînement ; Rm_c du générateur à 10 % du seuil simulé à un Pm sans donnée ; dans la région sous-critique, erreur au seuil réduite d’un facteur ≥ 2 par un conditionnement sur la branche (`en/these/index.qmd:917`).
- Budget : ≈ 700 h (palier 1) + ≈ 3 900 h (palier 2) + ≈ 3 200 h (palier 3) + ≈ 1 200 h (palier 4), réserve 20 %, total ≈ 1,1×10⁴ h GPU de classe A100. Incertitude au moins un facteur deux. Hypothèses H1–H5, dont « les simulations de référence ne sont pas comptées en GPU » (H4), non mesurées sur GPU (`en/these/index.qmd:955-973`).
- H1 cite PCDM : environ 1 150 h GPU pour un modèle 3D à 64³ (12 jours sur 4 A100, 8×10⁵ itérations). C’est un chiffre **publié par d’autres**, pas une mesure MilaDy (`en/these/index.qmd:959`).

Campagnes écrites, **non exécutées** comme résultats de ce dépôt (aucun JSON de campagne dans `experiences/resultats/` hors E1–E3) :

| Campagne | Grille écrite | Fichier |
|---|---|---|
| `palier1_mhd2d` | 11 valeurs de η, 16 trajectoires, réutilise le solveur E2, autres graines | `infra/configs/palier1_mhd2d.yaml:12-15`, `en/calcul/index.qmd:161` |
| `palier2_abc3d` | 64³, Rm de 4 à 40 pas 1 (37 points), 2 germes, cinématique | `infra/configs/palier2_abc3d.yaml:18-21`, `en/calcul/index.qmd:162` |
| `palier2_tg3d` | 64³, Re ∈ {25, 50, 100, 200}, Pm ∈ {0,5 ; 1 ; 2}, 12 simulations, `n_traj: 1`, 40 instantanés | `infra/configs/palier2_tg3d.yaml:18-21`, `:45`, `en/calcul/index.qmd:163` |
| `train_fm3d` | potentiels vecteurs, |m| ≤ 8, symétrie B → −B, validation Re = 100, Pm = 1, test Re = 50, Pm = 2. Commentaire : ≈ 48 M paramètres | `infra/configs/train_fm3d.yaml:22-39`, `:18` |

Le YAML Taylor–Green prévient que Re = 200, Pm = 2 donne Rm = 400 et que 64³ doit être vérifié (`palier2_tg3d.yaml:12-14`). Aucun spectre de ce pilote n’existe.

Décisions écrites **avant** toute location (`infra/cloud/RECOMMANDATION-CLOUD.md:19-35` et `:251-261`) : moyens déjà disponibles (GPU de laboratoire, projet GENCI), priorité des campagnes contre les données LATU/SFEMaNS, convention de forçage, plage de Re et Pm, 64³ suffit-il à Re ≥ 100, `n_traj`, métriques à coder avant de louer, droit de publier. La recommandation nomme une instance et des prix datés du 2026-11-08 ; le film ne les transforme pas en décision prise. Niveau « pour décider » : ordre de grandeur 10⁴ h, facteur deux, location inutile si un GPU ou Jean Zay est déjà ouvert, ne pas lancer le 256³ par défaut (`RECOMMANDATION-CLOUD.md:831-835`).

Pipeline testé sans GPU : 68 tests (66 passés et 1 sauté lors de la mesure avec PostgreSQL et MinIO ; un 68e test ajouté ensuite passe aussi). Non testé : GPU, Slurm réel, Apptainer, VM louée (`en/calcul/index.qmd:45`, `:180-190`).

Format MFF : HDF5 aligné sur The Well (Ohana et al., NeurIPS 2024), attributs `milady_*` (`en/calcul/index.qmd:109`). Clés d’évaluation déjà nommées dans le code, pour les scènes en attente : `div_rel_u`, `div_rel_b`, `err_spectre_u_log10`, `err_spectre_b_log10`, `dist_energie`, `plancher_dist_energie`, `residu_bilan_total` (`milady/eval/metrics.py:600-604`, `milady/eval/metrics.py:454-462`).

## 7. Carte bibliographique courte pour l’unité L4–L5

À citer, ne pas revendiquer. Recherche fermée le 6 novembre 2026.

| Bloc | Référence telle que le site la donne | Ce que le stage ajoute, selon le site |
|---|---|---|
| Flow matching | Lipman et al. 2023 ; chemin linéaire = rectified flow, Liu et al. 2023 | choix du stage, trois raisons en `en/rapport/index.qmd:601` |
| Offre | FunDiff, Wang et al. 2026 ; Fukami & Taira 2023, Nat. Commun. 14, 6480 | `en/index.qmd:74` |
| Fukami et Taira 2023 | trois variables latentes, profil NACA 0012 à Re = 100 | `en/rapport/index.qmd:169` |
| Perméabilité VKS, trois faits | fer doux et mode axisymétrique m = 0 (`dynamo.md:193`) ; μr d’ordre 50, Nore et al. 2018 (`dynamo.md:220`) ; μr ≈ 100, Monchaux et al. 2009 (`dynamo.md:160`). Pas d’intervalle 50 à 100 | mêmes lignes |
| Clôture EDARI | la recommandation du 2026-11-08 écrit que la prochaine clôture de l’accès régulier est le 08/02/2027 à 9 h, source EDARI. CONTEXT, à reconfirmer. Pas une décision des encadrants | `RECOMMANDATION-CLOUD.md:872-873` |
| Divergence | potentiels (FunDiff) ; Leray (Genuist et al. 2026, prépublication ; PCDM, Li et al. 2026) | comparaison V0–V5 sur MHD 2D couplée |
| Perte faible | Weak Generative Sampler, Cai et al. 2026, dimension ≤ 100 | perte conditionnelle de champ, sans valeur cible, aux paramètres sans donnée |
| Inclinaison | Csiszár 1975 ; Khalifa et al. 2021 ; Mun 2026 | identités sans valeur cible ; mesure de l’échec quand la masse manque |
| Résidu par échantillon | PIDM, Bastek et al. 2025 ; Tauberschmidt et al. 2026 | le corollaire 6 dit pourquoi un budget stationnaire n’est pas de cette classe |
| MHD générative proche | Kacmaz et al. 2025, MHD 2D, le générateur n’impose pas ∇·B = 0 | `en/rapport/index.qmd:226` |
| Encadrants | listes datées `en/encadrants/index.qmd:130-212` | noms et titres seulement |

Six lacunes structurantes (`en/rapport/index.qmd:238-245`) : pas de modèle génératif de dynamo trouvé ; pas de contrainte dure jointe ∇·u et ∇·B en 3D ; pas de domaine borné ; pas de métriques MHD (hélicité, budget, topologie) sur des champs générés ; pas de conditionnement joint (Re, Rm) ni de franchissement de seuil ; pas de comparaison systématique sur EDP couplées ni de contrainte en loi pour un champ.

## 8. Actifs réutilisables (hors `video/`)

Autorisés comme planches ou comme données. Les redessiner dans les scènes plutôt que d’embarquer le runtime du site. Ne pas utiliser les fichiers `*_quick*` comme mesures : ce sont des passes réduites (`en/experiences/index.qmd:75`).

| Actif | Usage licite | Réserve |
|---|---|---|
| `figures/cadre/figure/out/cadre-en.png` (+ svg) | schéma du cadre, glyphes explicitement non mesurés | légende `en/rapport/index.qmd:300` |
| `figures/taxonomie/figure/out/taxonomie-en.png` | quatre classes ; courbes illustratives, pas des mesures | `en/rapport/index.qmd:306` |
| `figures/flow-matching/figure/out/flow-matching-en.png` | jouet 1D calculé exactement, pas un résultat E1–E3 | `en/rapport/index.qmd:605` |
| `figures/vks/figure/out/vks-en.png` | géométrie qualitative | durées et amplitudes ≠ VKS, `en/rapport/index.qmd:163` |
| `figures/simulations/figure/out/simulations-en.png` | les trois bancs ; E2 sur la figure est **recalculé** pour le schéma | `en/experiences/index.qmd:46` |
| `figures/architecture/figure/out/architecture-en.png` | pipeline à sept étapes ; spectre de l’étape 7 illustratif | `en/calcul/index.qmd:86` |
| `figures/solveur/figure/out/solveur-en.png` | un pas pseudo-spectral, fichier MFF | `en/calcul/index.qmd:155` |
| `figures/plan-these/figure/out/plan-these-en.png` | cinq paliers ; la hauteur est un rang, pas une mesure | `en/these/index.qmd:857` |
| `experiences/figures/e1_seuil-en.png`, `e1_variantes-en.png`, `e1_symetrie_projection-en.png` | MEASURED | lire avec `en/rapport/index.qmd:807-811` |
| `experiences/figures/e2_mecanismes-en.png`, `e2_en_loi-en.png`, `e2_spectres-en.png` | MEASURED ; les spectres de la figure 9 sont sur huit échantillons gardés pour la figure | `en/rapport/index.qmd:1017` |
| `experiences/figures/e3_abc-en.png` | MEASURED | |
| `experiences/resultats/digest.md`, `e1_gissinger.json`, `e2_mhd2d.json`, `e3_abc.json` | source des chiffres | |
| `experiences/resultats/e1_echantillons.npz`, `e2_echantillons.npz`, `e3_modes.npz` | redessin déterministe plus tard | binaires, pas de ligne |
| `assets/interactif/*.js` et `assets/interactif/data/abc-dynamo.json` | référence de comportement (flow matching, Leray, contrainte en loi, Gissinger, ABC, pipeline) | réimplémenter sous `window.seek` ; ne pas copier le widget comme moteur du film |
| `assets/paper.css:47-75` | thème sombre du site | le film en fait sa dominante, voir `STYLE.md` |
| `figures/cadre/figure/parts.js:4-6` | couleurs sémantiques | |

Polices prévues au moment du moteur (pas encore vendues) : Inter, Inter Display, JetBrains Mono, fichiers locaux (`BRIEF-GROK.md` §6).

## 9. Ce qui n’est pas un résultat

- Aucun champ 3D généré. Aucun renversement 3D généré. Aucune fréquence de Rice sur VKS ou DRESDYN.
- Aucun temps GPU. La commande de banc existe (`en/calcul/index.qmd:153`) ; elle n’a pas été lancée, et elle ne le sera pas dans la production de ce film.
- Les prix de location du 2026-11-08 sont une méthode datée, pas une facture (`RECOMMANDATION-CLOUD.md:170` dit d’ailleurs, pour le guide d’infra, de ne pas figer de prix ; la recommandation, elle, en donne). Le cœur montre l’ordre de grandeur du plan de thèse et la question « faut-il louer », pas un panier.
- `unet.py` n’est pas un résultat.
- Les glyphes « données » des schémas cadre, taxonomie et flow matching ne portent aucune valeur mesurée.
