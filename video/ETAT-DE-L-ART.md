# Où s'inscrivent le stage et la thèse — état de l'art pour MilaDy 2027

Document compagnon du film *How Often Does the Field Flip?* (unités `chSOA1` et `chSOA2`, `video/BRIEF.md` §10),
rédigé le 8 novembre 2026 pour vous, qui préparez le stage de M2 « Physics-Constrained Generative AI Modelling
of Parametric Dynamical Systems » (S. Cheng, D. Lucor, en collaboration avec C. Nore et Y. Ponty) et la thèse
qui pourrait le prolonger. Il répond à quatre questions : quelles pistes la communauté a explorées (§1), ce que
les encadrants et le consortium ont publié (§2), où se placent exactement le stage et la thèse (§3), et quelles
questions en découlent pour vos encadrants (§4).

## Comment lire les marques de source

Chaque affirmation porte une marque. Les vérifications datées ont toutes été faites le **8 novembre 2026**.

| Marque | Sens |
|---|---|
| `[site f:l]` | Fait déjà vérifié dans le dépôt (bases de faits recoupées le 6 novembre 2026). Chemins relatifs à `/home/user/milady-2027`. `R` = `en/rapport/index.qmd`, `T` = `en/these/index.qmd`, `E` = `en/encadrants/index.qmd`, `S` = `specs/sources/encadrants.md`, `Dy` = `specs/sources/dynamo.md`, `L` = `specs/sources/litterature.md`, `P3` = `en/prep/p3-mhd-dynamo/index.qmd`. |
| `[RÉS]` | Résumé de l'éditeur ou de l'auteur lu (OpenAlex, arXiv ou HAL). |
| `[TI : X]` | Texte intégral de X lu ; l'affirmation vient de ce texte. |
| `[sec : X]` | Connu seulement par la revue de synthèse X, lue en entier ; la source primaire n'a pas été lue. |
| `[WEB]` | Page web ou PDF public consulté (adresse au §6.6). |
| `[SYNTHÈSE]` | Lecture ou rapprochement propre à ce document, **pas** une affirmation des auteurs cités. |
| `[NON VÉRIFIÉ]` | Non confirmé ; à ne pas reprendre sans nouvelle vérification. |

Les métadonnées bibliographiques (auteurs, titre, revue, volume, pages, DOI) de toutes les références du §6 ont
été vérifiées dans l'API Crossref (DOI) ou l'API arXiv (identifiant) ; les exceptions sont signalées dans la
liste. Les revues de synthèse lues en entier et utilisées comme sources secondaires sont Rincon (2019), Tobias
(2021), Stefani et al. (2018, arXiv:1803.03421) et la prépublication de Constable (2001, publiée en 2003).
Les affirmations négatives (« aucun travail trouvé ») résultent de recherches dans arXiv, Crossref, HAL et sur le
web ; une absence ne se prouve pas.

---

## 0. En bref

- **Côté dynamo**, un siècle de recherche a suivi cinq pistes qui se nourrissent mutuellement : la théorie
  (Larmor 1919 → Cowling 1933 → Herzenberg et Backus 1958 → champ moyen, écoulements modèles, dynamos rapides,
  dynamo à petite échelle), les expériences (Lowes et Wilkinson 1963 → Riga et Karlsruhe 1999 → VKS 2006-2007 →
  DRESDYN en préparation), les simulations (Glatzmaier et Roberts 1995 → benchmarks → simulations des expériences
  avec SFEMaNS et LATU), les modèles réduits d'inversions (Rikitake 1958 → Pétrélis et Fauve 2008 → Gissinger
  2012 → DQVU 2026) et la statistique des inversions du champ terrestre (Brunhes 1906 → Cox 1968 → débat
  Poisson contre regroupement).
- **Côté apprentissage**, de 2018 à 2026, quatre pistes : substituts et opérateurs neuronaux, modèles génératifs
  de champs (GAN puis diffusion et flow matching), contraintes physiques dans les modèles génératifs (dures,
  souples, en loi, symétries), a priori génératifs en assimilation de données.
- **Aucune piste d'apprentissage ne passe les quatre épreuves** d'une dynamo de laboratoire : la 3D, un domaine
  borné avec vide extérieur et sauts de perméabilité, un faible nombre de Prandtl magnétique, des événements
  rares (§1.5).
- **Le consortium possède déjà trois ingrédients** : les simulations et le modèle réduit des inversions de VKS
  (Nore, Ponty), l'apprentissage de représentations sur l'écoulement de von Kármán (Lucor, Nore), l'assimilation
  de données et des substituts génératifs hors MHD (Cheng) (§2).
- **Le stage et la thèse visent l'intersection manquante** : un générateur conditionnel de champs de dynamo,
  avec des contraintes dures (divergence nulle en géométrie bornée), des contraintes en loi (identités de
  stationnarité), la symétrie B → −B, et la fréquence des inversions tirée d'instantanés par la formule de
  Rice (§3).
- **Point d'attention n° 1** : PBFM (Baldan et al., ICLR 2026), absent du site, revendique « the first to
  recognize the trade-off between distributional and physical accuracy » ; la revendication 2 du rapport et de
  la thèse doit être repositionnée par rapport à ce travail avant toute soumission (§3.3, question Q-1).

---

## 1. La carte des pistes explorées par la communauté

### 1.1 Les pistes et leurs repères

Le film dessine la carte comme des **couloirs** (une piste par couloir) le long d'un axe du temps, avec des
**épingles** pour les travaux repères. Les neuf couloirs utilisés ici :

| Code | Piste | Question de la piste |
|---|---|---|
| D1 | Théorie de la dynamo | Un fluide conducteur peut-il entretenir un champ contre la diffusion ohmique ? Quels écoulements, à quelle vitesse, à quelles échelles ? |
| D2 | Dynamos de laboratoire | Peut-on construire une dynamo, et que fait une dynamo réelle, turbulente, à faible Pm ? |
| D3 | Dynamos numériques | Les équations complètes de la MHD reproduisent-elles les dynamos naturelles et de laboratoire, alors que les paramètres réels sont hors d'atteinte ? |
| D4 | Modèles réduits d'inversions | Pourquoi un système turbulent, symétrique sous B → −B, bascule-t-il entre deux polarités, et quelques équations suffisent-elles ? |
| D5 | Statistique des inversions | À quelle fréquence le champ terrestre s'inverse-t-il, le hasard suffit-il, que permet l'enregistrement ? |
| A1 | Apprentissage pour la turbulence, la MHD et les dynamos | Apprendre une application déterministe (état → état suivant, paramètres → solution), une fermeture ou un modèle réduit. |
| A2 | Modèles génératifs de champs physiques | Échantillonner la loi des champs, conditionnellement à des paramètres. |
| A3 | Contraintes physiques dans les modèles génératifs | Faire respecter les lois (divergence nulle, bilans, symétries) par les échantillons ou par leur loi. |
| A4 | A priori génératifs en assimilation | Utiliser un modèle génératif comme loi a priori dans une assimilation bayésienne. |

### 1.2 Frise datée

| Année | Événement | Piste | Source |
|---|---|---|---|
| 1906 | Brunhes trouve des laves aimantées en sens inverse du champ actuel. | D5 | Brunhes 1906 ; contenu `[TI : Constable 2003 §1]` |
| 1919 | Larmor propose que les mouvements d'un fluide conducteur entretiennent le champ des taches solaires : l'idée de dynamo fluide auto-excitée. | D1 | `[TI : Rincon 2019 §1.3-1.4]` ; titre et pages du rapport de Larmor `[NON VÉRIFIÉ]` |
| 1929 | Matuyama : directions d'aimantation de basaltes du Japon, de Corée et de Mandchourie. | D5 | Matuyama 1929 (contenu non lu) |
| 1933 | Cowling : un champ axisymétrique ne peut pas être entretenu par effet dynamo. | D1 | `[site Dy:435-440]` |
| 1937 | Taylor et Green introduisent le tourbillon qui servira plus tard de forçage de dynamo. | D1, D3 | Taylor et Green 1937 |
| 1946-1954 | Elsasser, puis Bullard et Gellman : théorie de la dynamo sphérique pour le noyau terrestre. | D1 | `[TI : Rincon §1.4]` |
| 1950 | Batchelor soutient qu'il n'y a pas de dynamo (à petite échelle) pour Pm < 1. | D1 | `[sec : Rincon §3.3.2]` |
| 1955 | Parker : rotation différentielle et mouvements cycloniques excitent des champs à grande échelle et des ondes dynamo. Bullard : stabilité de la dynamo homopolaire à disque. | D1, D4 | `[TI : Rincon §1.4]` |
| 1957 | Zel'dovich : un écoulement plan ne peut pas être une dynamo. | D1 | `[site Dy:441-442]` |
| 1958 | Herzenberg (deux tourbillons dans une sphère) et Backus : premières dynamos fluides démontrées rigoureusement. Rikitake : deux dynamos à disque couplées s'inversent. | D1, D4 | `[RÉS]` ; `[TI : Rincon §1.4]` |
| 1963 | Lowes et Wilkinson : un modèle de dynamo « quasi homogène » de laboratoire (cylindres de fer doux en rotation). Vine et Matthews : les anomalies magnétiques des dorsales enregistrent les inversions. | D2, D5 | `[TI : Stefani et al. 2018 §2.1]` ; `[TI : Constable 2003 §1]` |
| 1964 | Cox, Doell et Dalrymple rassemblent des inversions globales datées par radiochronologie. | D5 | `[TI : Constable 2003 §1]` |
| 1966 | Steenbeck, Krause et Rädler : électrodynamique de champ moyen et effet α. | D1 | `[site P3:918]` |
| 1967-1968 | Kazantsev : modèle de dynamo à petite échelle dans un écoulement aléatoire. Cox (1968) : modèle de type épreuves de Bernoulli (Poisson) des intervalles de polarité. | D1, D5 | Kazantsev : notice JETP, texte non lu ; Cox `[RÉS]` |
| 1970-1973 | Écoulements dynamos cinématiques : Childress (1970), G. O. Roberts (1970, 1972), Ponomarenko (1973). Vainshtein et Zel'dovich (1972) : dynamo rapide, étirement–torsion–repliement. | D1 | `[site Dy:416-431]` ; `[TI : Rincon §2.3.3]` |
| 1981 | Meneguzzi, Frisch et Pouquet : premières dynamos turbulentes numériques, hélicitaire et non hélicitaire. | D1, D3 | `[TI : Rincon §1.4]` |
| 1983-1986 | Dynamo de l'écoulement ABC (Arnol'd et Korkina ; Galloway et Frisch). | D1 | `[site Dy:386-412]` |
| 1987 | Soward : existence de dynamos rapides dans un écoulement stationnaire. | D1 | `[RÉS]` |
| 1995 | Glatzmaier et Roberts : simulation 3D auto-cohérente de la géodynamo, avec inversion ; début de « l'ère moderne ». Échelle de polarité CK95 (Cande et Kent). | D3, D5 | `[TI : Tobias 2021 §8.3]`, qui cite l'article *PEPI* 91 de 1995 ; l'inversion est le sujet de l'article *Nature* 377 (titre) |
| 1997 | Nore, Brachet, Politano et Pouquet : dynamo dans le tourbillon de Taylor–Green, seuil fixé par les symétries de l'écoulement. | D3 | `[RÉS]` |
| 1999 | **Riga** (11 novembre) et **Karlsruhe** (décembre) : premières dynamos fluides auto-excitées. | D2 | `[site Dy:36, Dy:106]` |
| 2001 | Benchmark communautaire de géodynamo (Christensen et al.). Hoyng et al. : la géodynamo comme oscillateur bistable à α fluctuant. | D3, D4 | Christensen : définition des cas `[NON VÉRIFIÉ]` ; Hoyng `[RÉS]` |
| 2005 | Ponty et al. : dynamos de Taylor–Green de Pm = 1 à 10⁻². Schekochihin et al. : à bas Pm, Rm_c croît avec Re sans limite visible. | D1, D3 | `[site Dy:573-595]` ; `[RÉS]` |
| 2006 | Carbone et al. : inversions regroupées dans le temps, écart à la statistique de Poisson. | D5 | `[RÉS]` |
| 2007 | **VKS** : première dynamo dans un écoulement pleinement turbulent, seulement avec des turbines en fer doux ; premières inversions de laboratoire. Iskakov et al. : dynamo de fluctuations à Pm ≪ 1. | D2, D1 | `[site Dy:111-153]` ; `[RÉS]` |
| 2008 | Pétrélis et Fauve : forme normale dipôle–quadripôle des inversions. | D4 | `[site Dy:260-287]` |
| 2012 | Gissinger : modèle déterministe à trois modes. Description de l'installation DRESDYN (Stefani et al.). | D4, D2 | `[site Dy:308-367]` ; `[RÉS]` |
| 2014 | Réseaux antagonistes génératifs (GAN, Goodfellow et al.). | A2 | page des actes NIPS `[WEB]` |
| 2016 | SINDy (Brunton, Proctor et Kutz). Première DNS non linéaire de VKS avec turbines (Nore et al., SFEMaNS). | A1, D3 | `[RÉS]` |
| 2017 | LATU : une forte perméabilité sélectionne le mode axisymétrique (Kreuzahler et al.). Géodynamos turbulentes à E = 10⁻⁷ (Schaeffer et al.). | D3 | `[RÉS]` |
| 2018 | tempoGAN (super-résolution 3D d'écoulements). Régression de Galerkin parcimonieuse contrainte (Loiseau et Brunton). Nore et al. : Rm_c ≈ 70 à grand Re dans VKS simulé. | A2, A1, D3 | `[RÉS]` ; `[site Dy:212-233]` |
| 2019 | PINN (Raissi et al.). Fermeture de champ moyen apprise (Nauman et Nättilä). Singer et al. : dernière inversion achevée vers 773 ka. | A1, D5 | `[RÉS]` |
| 2020 | DDPM (Ho et al.). Covariance imposée à un GAN de convection (Wu et al.). Flots équivariants (Köhler et al.). | A2, A3 | `[RÉS]` |
| 2021 | Opérateur neuronal de Fourier (Li et al.), DeepONet (Lu et al.), modèles génératifs par EDS (Song et al.). | A1, A2 | `[RÉS]` |
| 2022 | Gwirtz et al. : l'apprentissage ne détecte pas de précurseur fiable des inversions géomagnétiques. Réseaux à divergence nulle (Richter-Powell et al.). Assimilation latente généralisée (Cheng et al.). | A1, A3, A4 | `[RÉS]` |
| 2023 | Flow matching (Lipman et al.). Potentiel vecteur et rotationnel dans un CNN 3D périodique (Mohan et al.). Assimilation par score (SDA). PINO pour la MHD 2D (Rosofsky et Huerta). Dynamo à petite échelle jusqu'à Pm = 0,0031 (Warnecke et al.). | A2, A3, A4, A1, D1 | `[RÉS]` ; Mohan `[TI : arXiv:2002.00021v2]` |
| 2024 | Génération 3D de turbulence (TurbDiff, CoNFiLD). Assimilation par diffusion (DiffDA, EnSF). Diffusion contrainte par dualité (Khalafi et al.). | A2, A4, A3 | `[site L:193-214, L:221-224]` ; `[RÉS]` |
| 2025 | Opérateur + diffusion pour la MHD 2D à Pm = 1 (Kacmaz et al.). GenCast (Nature, en ligne fin 2024). PIDM, ECI, PCFM. TorchDA (Cheng et al.). DRESDYN : expérience de précession « en cours d'installation » (avril). | A1, A2, A3, A4, D2 | `[site L:301, L:227]` ; `[TI : arXiv:2410.14449v3]` |
| 2026 | ANR MilaDy démarre (janvier). Bousquet et al. (juin) : inversions de VKS simulées et modèle DQVU. Botez et al. (août) : conditions aux limites et seuil des dynamos de précession. PCDM (Leray 3D périodique, préprint), Genuist et al. (préprint), PBFM et Tauberschmidt et al. (ICLR), Weak Generative Sampler (SISC), FunDiff et GenCFD (Nat. Commun.), Galletti et al. (préprint), Guseva, Skene et Tobias (préprint). | D3, D4, A2, A3 | `[site S:28-33, S:227-240]` ; `[WEB ANR]` ; `[RÉS]` |

### 1.3 Les pistes de la dynamo

#### D1. Théorie

**a. Fondements.** Larmor (1919) propose l'idée d'une dynamo fluide auto-excitée pour le magnétisme des taches
solaires `[TI : Rincon §1.3]`. Cowling (1933) montre qu'aucun champ axisymétrique s'annulant à l'infini ne peut
être entretenu `[site Dy:435-440]` ; la preuve cinématique complète du cas couplé est due à Kaiser et Tilgner
(2014) `[site Dy:440]`. Parker (1955) montre que la rotation différentielle et des mouvements cycloniques à
petite échelle excitent des champs à grande échelle, avec des « ondes de Parker » `[TI : Rincon §1.4]`.
Herzenberg (1958) démontre rigoureusement qu'une paire de tourbillons dans une sphère conductrice est une
dynamo stationnaire `[RÉS]`, et Backus (1958) construit une autre classe ; selon Rincon, « the spell of
Cowling's theorem was definitely broken » `[TI : Rincon §1.4]`. Steenbeck, Krause et Rädler (1966) fondent
l'électrodynamique de champ moyen et l'effet α des écoulements sans symétrie miroir `[site P3:918-924]`
(monographie : Krause et Rädler 1980).

**b. Écoulements dynamos cinématiques, gabarits des expériences.** L'écoulement de G. O. Roberts (1972),
u = (cos y − cos z, sin z, sin y), est une dynamo pour presque toutes les résistivités ; c'est le gabarit de
Karlsruhe `[site Dy:416-420]`. Ponomarenko (1973) : un mouvement hélicoïdal rigide dans un conducteur au repos,
Rm_c = 17,7 ; c'est le gabarit de Riga `[site Dy:424-431]`. L'écoulement ABC (A = B = C = 1) a deux fenêtres
dynamo, 8,9 < Rm < 17,5 et Rm > 27 `[site Dy:386-412]` (fenêtres vérifiées par Archontis et al. 2003, qui citent
Galloway et Frisch) ; l'expérience E3 du stage les retrouve (seuils interpolés 8,87, 17,6 et 26,8)
`[site T:97]`. Le tourbillon de Taylor–Green (1937) devient un forçage de dynamo avec Nore et al. (1997) : le
seuil dépend des symétries de l'écoulement et les conditions aux limites magnétiques sélectionnent le mode le
plus rapide `[RÉS]`.

**c. Dynamos rapides.** Vainshtein et Zel'dovich (1972) posent le concept de dynamo rapide et l'image
étirement–torsion–repliement `[TI : Rincon §2.3.3]` ; Soward (1987) en démontre l'existence dans un écoulement
stationnaire 2D périodique à vorticité singulière `[RÉS]` ; Galloway et Proctor (1992) en calculent dans des
écoulements lisses périodiques en temps `[TI : Rincon §2.3.3]` ; synthèse dans Childress et Gilbert (1995).

**d. Dynamo à petite échelle et problème du faible Pm.** Batchelor (1950) soutient qu'il n'y a pas de dynamo
pour Pm < 1 `[sec : Rincon §3.3.2]`. Kazantsev (1967 en russe, 1968 en anglais) propose un modèle statistique
de dynamo à petite échelle dans des écoulements aléatoires non hélicitaires `[TI : Rincon §1.4]`, avec un spectre
magnétique en k^{3/2}, observé dans les runs de Taylor–Green de Ponty et al. (2005) `[site Dy:584]`. Schekochihin et al. (2005) trouvent que Rm_c croît avec Re sans limite visible, jusqu'à
Rm_c ≈ 500 pour Re ≈ 3000 `[RÉS]`. Ponty et al. (2005), avec un forçage de Taylor–Green, obtiennent Rm_c = 30 à
Pm = 1, 226 à Pm = 0,3, puis un plateau Rm_c ≈ 150 en LES pour 10⁻² ≤ Pm ≤ 10⁻¹ `[site Dy:573-595]`. Iskakov et
al. (2007) montrent qu'une dynamo de fluctuations existe pour Pm ≪ 1, avec Rm_c ≲ 200 pour Re ≳ 6000 contre
≈ 60 pour Pm ≥ 1 `[RÉS]`. Warnecke et al. (2023) la trouvent jusqu'à Pm = 0,0031, plus facile à exciter sous
Pm ≈ 0,05 `[RÉS]`.

**État en 2026.** La théorie cinématique est mûre ; Tobias (2021) qualifie d'« uncertain » la théorie des
dynamos turbulentes et liste quatre questions : turbulence à Pm extrême, organisation à grande échelle,
saturation, rotation `[TI : Tobias §3, §10]`.

#### D2. Dynamos de laboratoire

L'obstacle : Pm ≈ 10⁻⁵ pour le sodium, donc quelques dizaines de Rm exigent des Re de plusieurs millions et une
centaine de kilowatts `[site P3:1145]` ; Pm = 0,82·10⁻⁵ à 120 °C `[site R:137]`.

1. **Lowes et Wilkinson (1963, 1968)** : dynamos « quasi homogènes » de type Herzenberg, faites de cylindres de
   fer doux tournant dans des blocs du même matériau ; les améliorations successives donnent « a sort of
   reversals » (Wilkinson 1984) `[TI : Stefani et al. 2018 §2.1]`.
2. **Riga** (écoulement hélicoïdal de type Ponomarenko) : premier mode propre auto-excité le 11 novembre 1999,
   taux de croissance 0,0315 s⁻¹, fréquence 1,326 Hz ; régime saturé en juillet 2000 `[site Dy:36, Dy:51-74]`.
3. **Karlsruhe** (écoulement à deux échelles de Roberts–Busse) : premier fonctionnement en décembre 1999, champ
   stationnaire de type dipôle `[site Dy:85-107]`.
4. **VKS** (von Kármán sodium, Cadarache) : première dynamo dans un écoulement fortement turbulent, seulement avec
   des turbines en fer doux, Rm_c ≈ 31 (définition avec K = 0,6) (Monchaux et al. 2007) `[site Dy:111-136]` ;
   premières inversions de laboratoire, polarités de durées moyennes 120 s et 50 s à F1 = 16 Hz, F2 = 22 Hz,
   inversion en ≈ 5 s (Berhanu et al. 2007) `[site Dy:138-153 ; R:149]`. Précurseurs : VKS1 jusqu'à Rm ≈ 50
   sans dynamo (Bourgoin et al. 2002) `[RÉS]`, optimisation des turbines (Ravelet et al. 2005) `[RÉS]`.
5. **Expériences sans auto-excitation** qui mesurent l'induction turbulente : sphère de Madison (Spence et al.
   2006, un dipôle induit qu'aucun écoulement laminaire axisymétrique ne produit) `[RÉS]` ; tore freiné de Perm
   (Frick et al. 2010, diffusivité effective jusqu'à ≈ 50 % au-dessus de la valeur laminaire) `[RÉS]` ; sphère de
   3 m du Maryland (Zimmerman et al. 2014, contenu non lu).
6. **DRESDYN** (HZDR, Dresde) : deux projets phares, une dynamo entraînée seulement par précession et une grande
   expérience de Taylor–Couette (Stefani et al. 2012) `[RÉS]`. Cylindre de ≈ 2 m, rotation jusqu'à 10 Hz,
   précession jusqu'à 1 Hz ; masse de sodium 8 t selon Pizzi et al. (2023) ou 6 t selon Stefani et al. (2018)
   (divergence). Bâtiment achevé en 2017 `[TI : Stefani et al. 2018]` ; expérience « being set up » en avril
   2025 `[TI : arXiv:2410.14449v3]` ; **aucun premier essai au sodium trouvé au 8 novembre 2026 [NON VÉRIFIÉ]**.
7. **Dynamos de plasma** : amplification turbulente par laser jusqu'à près de l'équipartition (Tzeferacos et al.
   2018) `[RÉS]` ; Madison Plasma Dynamo Experiment (Cooper et al. 2014, cible Rm > 1000) `[RÉS]`.

**État en 2026.** Trois dynamos au sodium seulement ; le résumé ANR de MilaDy parle de « seulement trois »
expériences `[site S:56]`. La seule à écoulement peu contraint (Tobias oppose les « constrained designs » de
Riga et Karlsruhe aux « less constrained flows » de VKS `[TI : Tobias §9]`), VKS, exige des turbines
ferromagnétiques, et pourquoi sa topologie diffère des prédictions « is still a matter of ongoing research »
`[TI : Stefani et al. 2018 §2.1]` ; Tobias se demande même si VKS « can be classed as a dynamo in the strictest
sense » `[TI : Tobias §9]`. Une dynamo homogène « driven solely by precession » (DRESDYN, Stefani et al. 2012)
`[RÉS]` reste à obtenir ; Karlsruhe était déjà une dynamo homogène sans turbines, mais à écoulement guidé
(Stieglitz et Müller 2001, « homogeneous two-scale dynamo ») `[RÉS]`.

#### D3. Dynamos numériques

**Géodynamo.** Glatzmaier et Roberts (1995) : convection anélastique en rotation, champ ressemblant à celui de la
Terre, inversions ; début de « l'ère moderne » `[TI : Tobias §8.3]` (formulation exacte du résumé
`[NON VÉRIFIÉ]` ; Tobias cite ici l'article *PEPI* 91, 63-75, de 1995, et c'est l'article *Nature* 377 de la même
année qui porte sur l'inversion ; « anélastique » est le mot de Tobias, non revérifié dans les articles). Kageyama et Sato (1995), même année `[RÉS]`. Benchmarks communautaires : Christensen et al.
(2001), Jones et al. (2011, anélastique), Matsui et al. (2016, 15 codes jusqu'à 16 384 cœurs) `[RÉS]`. Kutzner et
Christensen (2002) : dipolaire à faible nombre de Rayleigh, multipolaire à fort, inversions et excursions entre
les deux `[RÉS]`. Schaeffer et al. (2017) : Pm = 0,1, Rm > 500, E = 10⁻⁷ `[RÉS]` ; Aubert et al. (2017) : chemin
vers le régime asymptotique `[RÉS]`. Le noyau terrestre est à E ≈ 10⁻¹⁵ et Pm ≈ 10⁻⁶ `[site P3:1353]`.

**Turbulence et géométrie des expériences.** Meneguzzi, Frisch et Pouquet (1981) `[TI : Rincon §1.4]`. Taylor–
Green comme substitut de von Kármán : Nore et al. (1997), Ponty et al. (2005), Mininni et al. (2005), Krstulovic
et al. (2011, dipôle axial de type VKS) `[RÉS]`. Rôle des turbines : Laguerre et al. (2008, Rm_c ≈ 32 atteint
avec des conditions ferromagnétiques) `[RÉS]`, Giesecke et al. (2010, 2012) `[site Dy:188-196]`. **SFEMaNS**
(Fourier en azimut, éléments finis de Lagrange dans le plan méridien) : première DNS non linéaire de VKS avec
turbines (Nore et al. 2016), puis Rm_c → ≈ 70 à grand Re, dans la plage expérimentale 52-71 ; les conditions de
pseudo-vide et de vide décalent Rm_c d'environ 40 % (Rm_c = 90 ± 5 contre 130 ± 10) (Nore et al. 2018)
`[site Dy:198-233 ; R:143]`. **LATU** (pseudo-spectral avec pénalisation volumique) : Kreuzahler et al. (2014,
2017), mode axisymétrique sélectionné par une forte perméabilité `[site Dy:235-245]`. Inversions simulées :
Gissinger, Dormy et Fauve (2010, à Pm < 0,5 elles mettent en jeu dipôle axial et quadripôle) `[site Dy:291-304]` ;
Nore et al. (2012, inversions apériodiques dans une dynamo de Taylor–Couette courte) `[RÉS]` ; Bousquet et al.
(2026, VKS, voir D4). Précession : Nore et al. (2011), Cappanera et al. (2016), Giesecke et al. (2018), Botez et
al. (2026), Giesecke et al. (2024-2025, arXiv:2410.14449) `[RÉS ; TI]`.

**État en 2026.** Les géodynamos atteignent E = 10⁻⁷ à 10⁻⁸, loin de 10⁻¹⁵ ; les simulations sont « too viscous
and too slowly rotating » pour les planètes `[TI : Tobias §10]`. Les simulations des expériences reproduisent
seuils et inversions, mais à Re ≈ 10³ au lieu de 10⁶-10⁷, et leurs données ne sont pas publiques
`[site R:161 ; T:929]`.

#### D4. Modèles réduits d'inversions

1. **Dynamos à disque** : Bullard (1955) ; Rikitake (1958), deux dynamos à disque couplées montrent des
   inversions du courant et du champ, contrairement à une seule `[RÉS]` ; Nozières (1978), modèle de relaxation
   (contenu non lu).
2. **Modèles stochastiques de champ moyen** : Hoyng, Ossendrijver et Schmitt (2001) : un α fluctuant reproduit
   inversions, inversions avortées, excursions et intervalles poissoniens `[RÉS]` ; Stefani et al. (2007).
3. **Forme normale fondée sur la symétrie** : Pétrélis et Fauve (2008), A = D + iQ, équation de phase
   θ̇ = μᵢ − ρ sin 2θ, col-nœud à μᵢ = ρ, inversions aléatoires sous le seuil sous l'effet du bruit ; application à
   la Terre avec P[T] ∝ exp(−T/⟨T⟩) (Pétrélis et al. 2009) `[site Dy:260-287]`.
4. **Chaos déterministe** : Gissinger (2012), trois modes (Q, D, V), crise à μc ≈ 0,11928, temps d'attente
   poissoniens aux temps longs `[site Dy:308-367]` ; c'est le banc E1 du stage et le palier 0 de la thèse
   `[site T:88, T:878-880]`.
5. **Modèles réduits identifiés à partir de données** : SINDy (Brunton et al. 2016) ; version de Galerkin
   contrainte avec termes quadratiques conservant l'énergie (Loiseau et Brunton 2018) `[RÉS]`. **DQVU**
   (Bousquet et al. 2026) : POD de 2000 instantanés de simulations de VKS, quatre modes axisymétriques
   (dipôle D, quadripôle Q, deux modes de vitesse V et U), modèle de Galerkin identifié par régression contrainte
   (PySINDy) sous conservation de l'énergie quadratique et d'un moment d'ordre 3 ; il reproduit la distribution
   bimodale asymétrique de V, ce que DQV ne fait pas `[site S:227-235 ; R:161]`. Ailleurs : DMD + SINDy retrouvent
   les équations d'un cycle de dynamo α–Ω 1D (Guseva, Skene et Tobias 2026, préprint) `[AX]`.
6. **Prédiction par apprentissage** : Gwirtz et al. (2022) entraînent SVM et LSTM sur des modèles (du plus simple
   à la géodynamo 3D) et sur deux reconstructions paléomagnétiques ; l'enregistrement exploitable (0-2 Ma) ne
   contient que cinq inversions ; conclusion : « the ML techniques we tried are not currently capable of reliably
   identifying an axial dipole moment (ADM) precursor for geomagnetic reversals » `[RÉS]`.

**État en 2026.** Les modèles de petite dimension expliquent les traits qualitatifs (bimodalité, excursions,
rôle de la brisure de symétrie) mais restent phénoménologiques ; DQVU, obtenu par projection de Galerkin des
équations MHD et identifié sous contraintes sur des simulations de VKS, ajoute la variable U au modèle DQV à trois
variables (« improves upon previous three-variable versions ») `[RÉS ; site S:230-234]` ; il reste déterministe et
ajusté en un seul point de paramètres `[SYNTHÈSE pour « un seul point »]`.

#### D5. Statistique des inversions

Découverte et datation : Brunhes (1906), Matuyama (1929), Vine et Matthews (1963), Cox, Doell et Dalrymple
(1964) ; les preuves ne furent « not generally accepted as conclusive until the 1960's »
`[TI : Constable 2003 §1]`. Cox (1968) : probabilité ≈ 0,05 par cycle dipolaire sur les 10 derniers Ma, au moins
100 fois plus faible au Permien `[RÉS]` ; depuis, les inversions sont traitées comme des événements « described
by a Poisson process with a varying rate parameter » `[TI : Constable 2003 §4.1]`. Taux variable et
superchrons : Cande et Kent (1995) ; Constable (2000) : sur 0-158 Ma la dérivée du taux change de signe au moins
une fois, taux nul pendant le superchron normal du Crétacé (≈ 40 Ma, fin vers 83 Ma) `[TI : Constable 2003]`.
Au-delà de Poisson : Carbone et al. (2006), regroupement temporel et corrélations à longue portée `[RÉS]`.
Enregistrements individuels : Valet et Fournier (2016), « questions remain regarding the dynamical processes »
`[RÉS]` ; Singer et al. (2019), dernière bascule vers 773 ka après un processus commencé vers 795 ka `[RÉS]`.

**État en 2026.** L'échelle de polarité est bien datée sur ≈ 160 Ma `[RÉS : Gwirtz et al. 2022]`, mais elle est
courte pour une statistique de ce qui précède une inversion ; le débat entre Poisson à taux lentement variable et
regroupement à longue mémoire reste ouvert (Constable contre Carbone et al.).

### 1.4 Les pistes de l'apprentissage

#### A1. Apprentissage pour la turbulence, la MHD et les dynamos

- **Substituts et opérateurs neuronaux.** PINN (Raissi et al. 2019) : la physique est une pénalité dans la perte.
  DeepONet (Lu et al. 2021), opérateur neuronal de Fourier (Li et al. 2021), cadre général (Kovachki et al.
  2023) ; FNO se dit « the first ML-based method to successfully model turbulent flows with zero-shot
  super-resolution » `[RÉS]`. Solveurs appris et modèles de fondation : Kochkov et al. (2021), McCabe et al.
  (2024), Herde et al. (2024, Poseidon). **Limite** : entraînés à minimiser l'erreur quadratique, des ensembles
  de modèles déterministes « regress to the mean flow » en turbulence 3D (GenCFD) `[RÉS de la prépublication
  arXiv:2409.18359v2 ; le résumé publié dans *Nat. Commun.* dit seulement que la perte quadratique « fails to
  accurately characterize statistical features of chaotic dynamics »]` ;
  un tel substitut ne peut pas représenter une loi bimodale ±B `[SYNTHÈSE]`.
- **Bancs d'essai.** PDEBench (2022) ; The Well (2024), qui contient de la MHD 3D compressible à 64³ et 256³, de
  type milieu interstellaire et non une dynamo de laboratoire `[site L:308 ; R:226]`. Aucun banc public de
  simulations de dynamo de laboratoire n'a été trouvé `[SYNTHÈSE, recherche non systématique]`.
- **Fermetures apprises.** Revues : Duraisamy et al. (2019), Brunton et al. (2020). Beck et al. (2019), Maulik et
  al. (2019), Guan et al. (2023). **Mohan, Lubbers, Chertkov et Livescu (2023)** : un autoencodeur convolutif
  pour la turbulence homogène isotrope 3D (128³) dont le décodeur produit un potentiel vecteur, puis un
  rotationnel par différences finies : la sortie est à divergence nulle par construction ; conditions
  périodiques, pas de jauge fixée `[TI : arXiv:2002.00021v2]`. Non génératif, c'est le précédent 3D le plus
  proche du décodeur en potentiel vecteur de la thèse (Q1).
- **Apprentissage pour la MHD.** Rosofsky et Huerta (2023) : PINO pour la MHD 2D, laminaire (Re ≤ 250)
  `[RÉS]`. **Kacmaz, Huerta et Haas (2025)** : PINO pour les basses fréquences et diffusion conditionnelle pour
  les hautes, MHD 2D résistive à 128², Pm = 1, Re de 100 à 10 000 ; ∇·B = 0 garanti par le solveur, pas par le
  générateur `[site L:301 ; R:226]`. Duarte et al. (2025, préprint, FNO sur Orszag–Tang 2D) `[RÉS]`. Gopakumar et
  al. (2024, FNO pour les plasmas de tokamak) `[RÉS]`. Jarolim et al. (2023, PINN pour le champ coronal ; divergence
  en pénalité selon un résumé de la prépublication `[NON VÉRIFIÉ dans la version publiée]`). Kaptanoglu et al.
  (2021, modèles réduits de MHD contraints par les lois de conservation globales). Scheinker (2026, préprint) :
  un modèle de diffusion latente conditionnel et bidirectionnel (pas en avant ou en arrière dans le temps) dont
  l'écart aller-retour estime ses propres erreurs de déroulement ; la MHD compressible est l'un de ses trois cas
  tests ; aucune contrainte sur ∇·B mentionnée `[RÉS]`.
- **Apprentissage pour les dynamos.** (a) Fermetures de champ moyen apprises : Nauman et Nättilä (2019) ;
  Illarionov et al. (2026, quenching de α par équations différentielles neuronales, dynamo solaire) `[RÉS]`.
  (b) Modèles réduits identifiés : DQVU (Bousquet et al. 2026) ; Yang et Schmid (2025, réseaux complexes,
  inversions en convection 2D) `[RÉS]`. (c) Prédiction : Gwirtz et al. (2022, résultat négatif) ; outils
  génériques (Pathak et al. 2018 ; Qi et Majda 2020 ; Lucente et al. 2022, algorithmes d'événements rares et
  fonctions de committor apprises). Aucune application d'algorithmes d'événements rares aux inversions de dynamo
  n'a été trouvée `[SYNTHÈSE, affirmation négative]`. (d) Apprentissage par la mesure invariante : Yang et al.
  (2023), Botvinick-Greenhouse et al. (2023), Jiang et al. (2023), DySLIM (Schiff et al. 2024), Chen et al. (2026)
  `[site T:148]`.

#### A2. Modèles génératifs de champs physiques

- **L'ère des GAN (2014-2021).** Goodfellow et al. (2014). tempoGAN (Xie et al. 2018) : super-résolution 3D
  temporellement cohérente `[RÉS]`. Kim et al. (2021) : CycleGAN non apparié pour la super-résolution de
  turbulence. **Wu et al. (2020)** imposent la covariance des données à un générateur antagoniste de convection
  de Rayleigh–Bénard : la plus ancienne contrainte en loi sur un générateur de champs turbulents de cette carte
  `[site R:218]`.
- **Diffusion, score, flow matching, interpolants (2020-2025).** DDPM (Ho et al. 2020), EDS (Song et al. 2021),
  EDM (Karras et al. 2022), guidage sans classifieur (Ho et Salimans 2022), flow matching (Lipman et al. 2023),
  rectified flow (Liu et al. 2023), interpolants stochastiques (Albergo et Vanden-Eijnden 2023 ; Albergo et al.
  2025), OT-CFM (Tong et al. 2024) ; versions fonctionnelles (Kerrigan et al. 2024 ; Lim et al. 2025)
  `[site R:177 ; L:107-136]`. E1 et E2 du stage utilisent le flow matching conditionnel `[site T:88-90]`.
- **Turbulence.** Shu et al. (2023, reconstruction 2D) ; **TurbDiff** (Lienen et al. 2024 : états 3D sans état
  initial, sans contrainte d'incompressibilité explicite) `[site L:193-198]` ; ACDM (Kohl et al. 2026, conditionné
  par Re et Mach) ; **CoNFiLD** (Du et al. 2024 : diffusion latente sur champs neuronaux, géométries irrégulières
  2D et 3D, sans contrainte de divergence) `[site L:210-214]` ; **GenCFD** (Raonić et al. 2026) `[RÉS]` ;
  **Galletti et al. (2026, préprint)** : flow matching latent qui génère les états statistiquement stationnaires
  d'une turbulence gyrocinétique conditionnés par des paramètres sans dimension, sans contrainte physique
  `[RÉS ; site R:183]` — l'analogue le plus proche d'un générateur d'instantanés d'états saturés `[SYNTHÈSE]`.
  **FunDiff** (Wang et al. 2026) : autoencodeur fonctionnel et DiT latent, fonction de courant en 2D
  `[site L:140-160]` ; première des deux lectures recommandées par l'offre de stage, avec Fukami et Taira (2023)
  `[WEB : offre 2027, relue le 8 novembre 2026]`. Finzi et al. (2023) : échantillonnage conditionnel d'événements rares
  définis par l'utilisateur, « matches data statistics even when sampling from the tails » `[RÉS]`.
- **Météorologie.** SEEDS (2024), GenCast (Price et al. 2025 : mieux que l'ensemble opérationnel sur 97,2 % de
  1320 cibles, sans contrainte physique explicite) `[site L:227-228]`, CorrDiff (2025).
- **MHD.** Kacmaz et al. (2025) ; da Silva et al. (2025, préprint : diffusion sur les coefficients en harmoniques
  sphériques d'un champ potentiel coronal 3D, conditionnée par la phase du cycle solaire ; les fonctions de base
  satisfont l'équation de Laplace, donc ∇·B = 0 par la représentation, pour un champ sans courant)
  `[RÉS ; TI : arXiv:2510.01441v1]` ; Martin et al. (2025,
  trajectoires de particules test dans une turbulence MHD 3D) `[site R:226]`. **Aucun modèle de diffusion ou de
  flow matching entraîné sur des simulations de dynamo n'a été trouvé** (recherches arXiv et web du 8 novembre
  2026), ce qui concorde avec le site `[site R:228 ; T:163 ; E:514]` ; c'est une affirmation négative.

#### A3. Contraintes physiques dans les modèles génératifs

- **Dures, par construction.** Réseaux à divergence nulle issus des formes différentielles, universels sur le
  tore (Richter-Powell et al. 2022) `[site L:239-243]` ; fonction de courant en 2D (FunDiff) ; potentiel scalaire
  en harmoniques sphériques, en 3D sphérique mais pour un champ potentiel sans courant (da Silva et al. 2025,
  préprint) `[TI : arXiv:2510.01441v1]` ; potentiel vecteur et rotationnel en 3D périodique (Mohan et al.
  2023) ; **PCDM** (Li, Buzzicotti, Bonaccorso et Biferale 2026, préprint) : projection de Leray de l'estimation
  propre du débruiteur, turbulence 3D périodique en rotation à 64³, divergence nulle à la précision machine
  `[site R:193 ; L:282-287]` ; mesure de référence gaussienne à divergence nulle pour le flow matching (Li X. et
  al. 2026, préprint) `[site L:289-292]` ; couches contraintes par optimisation différentiable (Négiar et al. 2023)
  et lois de conservation intégrales (ProbConserv, Hansen et al. 2024) `[RÉS]`.
- **Dures, par projection à l'échantillonnage.** Diffusion projetée (Christopher et al. 2024), miroir (Liu et al.
  2023), réfléchie (Fishman et al. 2023), ECI (Cheng C. et al. 2025, sans lien connu avec S. Cheng), PCFM (Utkarsh
  et al. 2025, projection de Gauss–Newton pour des contraintes non linéaires) `[site R:191 ; L:244-273]`.
- **Souples (pénalité, guidage).** PIDM (Bastek et al. 2025) et son analyse de l'écart de Jensen, DiffusionPDE
  (2024), CoCoGen (2025), DPS (2023), guidage universel (2024), D-Flow (2024), PISD (2026, préprint)
  `[site R:179-187]`. **PBFM** (Baldan, Liu, Guardone et Thuerey, ICLR 2026, arXiv:2506.08604) : impose les résidus
  d'EDP à l'entraînement par des mises à jour de gradient sans conflit et un déroulement contre l'écart de Jensen ;
  les auteurs écrivent « Our work is the first to recognize the trade-off between distributional and physical
  accuracy » `[RÉS, relu le 8 novembre 2026]`. **Absent du site.**
- **Comparaisons.** **Genuist, Savin, Gatti et Clouteau (2026, préprint)** comparent six façons d'imposer
  l'incompressibilité dans un EDM autorégressif en turbulence 2D : la pénalité souple « performs poorly across all
  metrics » en loi et en déroulement, mais est la meilleure hors distribution sur Taylor–Green, avec une divergence
  non nulle ; « no single strategy dominates » `[site R:193 ; L:274-279]`. L'expérience E2 du stage compare cinq
  mécanismes sur la MHD 2D périodique à 32² `[site T:90-93]`.
- **En loi (statistiques, distributions).** Covariance dans un GAN (Wu et al. 2020) ; contrainte d'énergie issue
  des statistiques turbulentes (Genuist et al. 2025, préprint) `[RÉS]` ; I-projection et inclinaison exponentielle
  vers des moments cibles externes (Csiszár 1975 ; Jaynes 1957 ; Pitera et Chodera 2012 ; Khalifa et al. 2021 ;
  Mun 2026, préprint) ; diffusion contrainte par dualité (Khalafi et al. 2024) `[site T:149 ; R:220]` ; **forme
  faible de l'équation de Fokker–Planck stationnaire comme perte d'un échantillonneur, EDS jusqu'en dimension 100
  (Weak Generative Sampler, Cai et al. 2026)** et son antécédent WAN (Zang et al. 2020) `[site T:147 ; R:218]` ;
  **inclinaison d'un modèle de flow matching par un résidu d'EDP en forme faible, évalué échantillon par
  échantillon (Tauberschmidt et al., ICLR 2026)** `[site T:149 ; E:507]`.
- **Symétries.** Un flot construit avec des applications équivariantes produit une densité invariante (Köhler,
  Klein et Noé 2020) `[site en/prep/p8-contraintes-physiques/index.qmd:347]` ; flow matching équivariant (Klein et
  al. 2023) ; diffusion équivariante 3D (Hoogeboom et al. 2022) ; symétries dans les modèles de dynamique
  turbulente (Wang, Walters et Yu 2021).

#### A4. A priori génératifs en assimilation de données

- **Assimilation latente** (a priori par autoencodeur) : Amendola et al. (2021), Peyron et al. (2021) ; lignée de
  S. Cheng (voir §2.5) : assimilation latente généralisée (2022), assimilation latente pour les incendies (2022),
  encodeurs-décodeurs multi-domaines (2024), VIVID (2024), TorchDA (2025).
- **Par score et diffusion** : SDA (Rozet et Louppe 2023, testé sur l'écoulement de Kolmogorov) `[site L:216-219]` ;
  a priori de diffusion appris à partir d'observations bruitées par EM (Rozet et al. 2024) ; DiffDA (Huang et al.
  2024, échelle météorologique) `[site L:221-224]` ; filtre à score d'ensemble EnSF (Bao et al. 2024) et
  Latent-EnSF (Si et Chen 2024, préprint) `[RÉS]` ; Zhuang, Cheng et Duraisamy (2025) ; Bocquet, Finn et Cheng
  (2026, préprint) `[RÉS]`.
- **Précédent historique non appris** : assimilation géomagnétique avec des modèles de dynamo 3D et
  quasi géostrophiques (Fournier et al. 2010).
- **Limite** : aucune assimilation par diffusion appliquée à la MHD n'a été trouvée `[site L:385]` ; près d'une
  inversion, la loi a posteriori est bimodale en ±B, et un a priori qui ne respecte pas B → −B biaiserait
  l'analyse vers une polarité `[site E:491]`.

### 1.5 Problèmes ouverts et épreuves

**Sept problèmes ouverts de la dynamo**, chacun tiré d'une source :

1. **Dynamos à faible Pm avec écoulement moyen et fluctuations** : la dynamo à petite échelle semble possible à
   Pm ≪ 1 (Iskakov 2007 ; Warnecke 2023), mais les fluctuations relèvent les seuils des dynamos d'écoulement moyen
   (≈ 8 fois pour Taylor–Green, ordre de grandeur rappelé par Ponty et al. 2007 d'après des travaux antérieurs)
   `[site Dy:605]` et VKS exige des turbines magnétiques
   `[TI : Tobias §9]`.
2. **L'écart de paramètres** : E ≈ 10⁻¹⁵ et Pm ≈ 10⁻⁶ dans le noyau, contre E ≈ 10⁻⁷ et Pm = 0,1 dans les
   meilleures simulations `[site P3:1353]`.
3. **Mécanisme et prévisibilité des inversions** : aucun moyen d'identifier quand le champ « has entered a
   transitional state destined to lead to a reversal » `[TI : Constable 2003, résumé]` ; détection de précurseurs
   limitée par cinq inversions sur 0-2 Ma `[RÉS : Gwirtz et al. 2022]`.
4. **Statistique des inversions** : Poisson à taux variable (Constable) ou regroupement à longue mémoire (Carbone
   et al. 2006) ; les causes des changements de taux et des superchrons ne peuvent être ni retenues ni exclues
   `[TI : Constable 2003 §4.1]`.
5. **L'énigme VKS** : pourquoi le fer doux est nécessaire et pourquoi le dipôle axisymétrique observé diffère des
   prédictions cinématiques `[TI : Stefani et al. 2018 §2.1]` ; les conditions aux limites décalent les seuils
   numériques d'environ 40 % `[site R:143]`.
6. **Une dynamo de laboratoire homogène** : la dynamo de précession n'est pas encore démontrée ; dans les
   simulations, son seuil dépend des couches extérieures et des conditions aux limites (Botez et al. 2026 ;
   Giesecke et al. 2025) `[RÉS ; AX]`.
7. **Des simulations aux modèles réduits et statistiques** : données de simulation coûteuses et privées
   (Bousquet et al. 2026) `[site R:161]`, modèles réduits ajustés en un point de paramètres, aucun modèle génératif
   entraîné sur des simulations de dynamo `[site T:163]`.

**Les quatre épreuves d'une dynamo de laboratoire pour les pistes d'apprentissage** `[SYNTHÈSE à partir des
sources citées dans chaque case]` :

| Épreuve | Pourquoi | A1 substituts | A2 génératifs | A3 contraintes | A4 assimilation |
|---|---|---|---|---|---|
| **3D** | Zel'dovich : une dynamo auto-entretenue exige trois dimensions ; la MHD 2D est un banc d'essai, pas une dynamo `[site R:240]` | parfois | oui (TurbDiff, CoNFiLD, GenCFD) | divergence dure en 3D : PCDM (périodique, champ turbulent) ; da Silva et al. 2025 (sphère, champ potentiel sans courant) | oui (météo) |
| **Domaine borné, vide, sauts de μr, maillage non cartésien** | VKS et DRESDYN sont des cylindres à parois ; B·n et la composante tangentielle de B/μr sont continus ; SFEMaNS = modes de Fourier × éléments finis `[site T:111-117 ; R:143-145]` | surtout grilles périodiques | partiellement (CoNFiLD, TurbDiff : géométries complexes, sans divergence) | **aucune contrainte dure ne traite à la fois parois, raccord au vide et sauts de μr** `[site R:241-242 ; E:518]` | grilles météo |
| **Faible Pm** | sodium Pm = 0,82·10⁻⁵ `[site R:137]` ; DNS « typically restricted to Pm~1 regimes » `[site S:88]` ; run de référence Re = 1594, Rm = 531, donc Pm ≈ 0,33 `[site R:161]` (calcul de ce document) | non | non | non | non |
| **Événements rares** | inversion ≈ 5 s contre polarités de 120 s et 50 s `[site R:149]` ; cinq inversions sur 0-2 Ma `[RÉS : Gwirtz 2022]` | résultats négatifs ou partiels | échantillonnage d'événements rares (Finzi 2023), jamais sur une dynamo | non | loi a posteriori bimodale non étudiée pour la MHD |

---

## 2. Les contributions des encadrants et du consortium MilaDy

Règle suivie : on n'attribue à chacun que ce que ses publications montrent (une phrase factuelle tirée du résumé
ou du texte), sans opinion ni intention. Source principale : `specs/sources/encadrants.md` (vérifié le 6 novembre
2026), revérifié le 8 novembre 2026 dans Crossref, arXiv, HAL et sur les pages personnelles.

### 2.1 Le projet ANR MilaDy

- *Modélisation par apprentissage automatique des dynamos turbulentes – MilaDy*, ANR-25-CE51-0077, comité CE51,
  appel 2025 ; coordination Caroline Nore (LISN) ; partenaires LISN, Lagrange (Observatoire de la Côte d'Azur),
  CEREA (École nationale des ponts et chaussées) ; aide ANR 560 612 € ; début janvier 2026, 48 mois `[WEB ANR]`.
  D'autres pages donnent d'autres dates et montants (CV de Y. Ponty : février 2026-2030, 550 k€ ; page de
  S. Cheng : 2025-2029) : retenez les valeurs ANR.
- Deux objectifs : (i) les inversions et les dynamos « explosives », avec des modèles réduits qui identifient
  les phases de précurseur, d'inversion et de récupération ; (ii) l'optimisation de DRESDYN par des modèles réduits
  paramétriques (rapport des fréquences de précession et de rotation, par exemple). Le résumé cite la plateforme
  **TorchDA** `[WEB ANR ; site S:55-58]`.
- **Publications qui déclarent le financement MilaDy** (HAL et Crossref) `[site S:28-33]` :
  - **Bousquet, Ponty, Botez, Plihon et Nore (2026)**, *Phys. Rev. Fluids* 11, 063703 : deux solveurs (LATU et
    SFEMaNS) s'accordent sur le mécanisme d'inversion de VKS à turbines ferromagnétiques (cinq étapes : dipôle,
    affaiblissement près de la turbine rapide, état quadripolaire, affaiblissement près de la turbine lente,
    dipôle inversé) ; POD sur 2000 instantanés ; modèle DQVU ; run de référence Re = 1594, Rm = 531, asymétrie de
    forçage 0,058, μr = 16 ; un milieu environnant conducteur s'est révélé « necessary for these inversions to
    occur » dans la plage explorée ; données « available from the authors upon reasonable request » `[site
    R:161 ; S:227-235]` (texte intégral relu le 8 novembre 2026).
  - **Botez, Giesecke, Nore, Cappanera et Stefani (2026)**, *Phys. Rev. Fluids* 11, 083701 : dynamo cinématique de
    précession dans un cylindre, calculée à partir de champs de vitesse moyennés dans l'étroite plage de nombre
    de Poincaré où la dynamo est la plus probable ; deux familles de modes en compétition (quadripolaire
    centro-symétrique et dipolaire centro-antisymétrique) ; des conditions de champ tangentiel nul sous-estiment
    systématiquement Rm_c ; des parois conductrices ou perméables peuvent favoriser ou supprimer la dynamo
    `[RÉS ; site T:943]`.
  - Barré et Horii (2026, prépublication HAL) : grandes déviations, lien thématique faible avec les dynamos.
- **Articles du consortium antérieurs au financement**, cités par les offres comme point de départ (aucun ne
  déclare MilaDy) : **Bousquet, Nore et Lucor (2025)**, *Comput. Phys. Commun.* 315, 109728 : autoencodeurs et
  VAE comparés à la POD sur des écoulements forcés (cylindre oscillant, écoulement de von Kármán) ; augmenter la
  régularisation du VAE dégrade la reconstruction, « a significant limitation of the Gaussian prior » ; relations
  d'équivariance entre variables latentes et physiques, mieux préservées par les VAE `[RÉS]` (financement déclaré :
  GENCI seulement : parlez d'« article du consortium », pas d'« article MilaDy ») ; **Bousquet, Chaffard, Creff,
  Lucor et Nore (2024)**, *Phys. Fluids* 36, 105133 : LES et POD d'écoulements de von Kármán 3D, un état
  métastable qui brise la symétrie R_π pour Re > 10⁴ `[RÉS]` (exposant lu dans les métadonnées, non vu composé) ;
  **Botez, Bousquet et Nore (2025)**, *Magnetohydrodynamics* 61, 13-24 : POD de VKS, phase de croissance dominée
  par un dipôle axial, phase saturée où la rétroaction magnétique brise la symétrie de la vitesse même en
  contra-rotation exacte `[RÉS]`.
- **Sorties 2026 sans financement déclaré** : autoencodeurs polynomiaux initialisés comme la POD (Bousquet,
  Faucheu, Dumas, Nore et Lucor, Research Square, préprint non évalué) `[RÉS]` ; poster de Bousquet et Nore aux
  Rencontres du Non-Linéaire (mars 2026, non évalué), qui annonce des couplages nouveaux du premier ordre dans
  DQVU liés à la perméabilité `[WEB]`.
- **Non confirmé** : un article de Botez, Bousquet et Nore annoncé « in press » au *Journal of Computational
  Physics* n'a été trouvé ni dans Crossref ni dans HAL `[NON VÉRIFIÉ]`.

### 2.2 Caroline Nore (LISN, Université Paris-Saclay ; coordinatrice de MilaDy)

- **Dynamo et écoulement de von Kármán, premiers travaux** : dynamo dans le tourbillon de Taylor–Green, seuil
  fixé par les symétries (Nore et al. 1997) `[RÉS]` ; bifurcations de l'écoulement de von Kármán contrarotatif
  et cycles quasi hétéroclines, en simulation (2003, 2004) et en expérience (2005) `[RÉS]`.
- **Le code SFEMaNS** : ses termes, « We have been developing a so-called code SFEMaNS since 2002 », un code MHD
  non linéaire en domaines hétérogènes (sauts de conductivité ou de perméabilité) en géométrie axisymétrique
  `[WEB : résumé de séminaire LadHyX]` ; dites « développé par J.-L. Guermond, C. Nore et collègues ». Articles de
  méthode : Guermond, Laguerre, Léorat et Nore (2007, 2009), Guermond et al. (2011, perméabilité discontinue)
  `[RÉS]`.
- **VKS et turbines ferromagnétiques** : l'effet α de l'écoulement entre les pales et des conditions
  ferromagnétiques atteignent Rm_c ≈ 32 (Laguerre et al. 2008) `[RÉS]` ; disques de forte perméabilité,
  Rm_c(μr) − Rm_c(∞) ∝ μr^(−1/2) (Giesecke et al. 2012) `[RÉS]` ; modèle de champ moyen (Nore et al. 2015) ;
  **première DNS non linéaire de VKS avec les deux turbines** (Nore et al. 2016) et Rm_c → ≈ 70 à grand Re (Nore
  et al. 2018) `[RÉS ; site Dy:198-233]` ; transferts d'énergie locaux sur maillages non structurés (Creff et al.
  2024) `[RÉS]`.
- **Précession et DRESDYN** : la précession peut déclencher une dynamo dans un cylindre (Nore et al. 2011) ;
  Stefani et al. (2015, avec Nore) ; Cappanera et al. (2016) ; Botez et al. (2026) `[RÉS]`.
- **Autres géométries** : dynamo de Taylor–Couette courte dont le dipôle axial « exhibits aperiodic reversals »
  (Nore et al. 2012) `[RÉS]` ; co-autrice d'un benchmark de dynamo en coquille sphérique (Jackson et al. 2014)
  `[RÉS]`.
- **Apprentissage** : co-autrice de Bousquet, Nore et Lucor (2025) et de DQVU (2026) ; co-directrice d'une thèse
  sur les réseaux de graphes pour l'assimilation et l'optimisation (Quattromini 2024) `[WEB HAL]`.

### 2.3 Yannick Ponty (Lagrange, Observatoire de la Côte d'Azur, CNRS)

- **Dynamo cinématique** : écoulement de couche plane entraîné par cisaillement et convection (Ponty, Gilbert et
  Soward 2001) `[RÉS]`.
- **Dynamos à faible Pm dans l'écoulement de Taylor–Green** (substitut de von Kármán) : induction à faible Pm
  (2004) ; dynamos de Pm = 1 à 10⁻² en combinant DNS, modèle lagrangien moyenné et LES (Ponty et al. 2005) `[RÉS]`
  (le spectre de Kazantsev en k^{3/2} n'est mentionné que dans le résumé arXiv, pas dans celui publié) ; régimes
  oscillants « but with no reversal of the magnetic field » (Mininni et al. 2005) `[RÉS]` ; dynamo cinématique de
  l'écoulement moyen à deux branches, le seuil dynamique passant de la branche basse au voisinage de la branche
  haute quand Re augmente (Ponty et al. 2007, NJP) `[RÉS]` ; **bifurcation sous-critique avec hystérésis** (Ponty et
  al. 2007, PRL) `[RÉS]` ; statistiques lagrangiennes, lois de B passant de fortement non gaussiennes à quasi
  gaussiennes (Homann et al. 2014) `[RÉS]`.
- **Intermittence et branches sous-critiques** : intermittence on-off près du seuil de l'écoulement ABC (Alexakis
  et Ponty 2008) ; transition de la dynamo à grande échelle à la dynamo à petite échelle (Ponty et Plunian 2011) ;
  route systématique vers les branches sous-critiques par optimisation non linéaire (Mannix, Ponty et Marcotte
  2022) ; relations kurtosis–asymétrie sur des DNS de Taylor–Green et ABC jusqu'à 3,14 × 10⁵ temps de
  retournement (Ponty, Politano et Pouquet 2025) `[RÉS]`.
- **Modélisation de la turbulence MHD** : modèle LES spectral fondé sur EDQNM (Baerenzung et al. 2008) `[RÉS]`.
- **LATU** : écoulements de von Kármán entraînés par turbines par pénalisation volumique (Kreuzahler et al. 2014) ;
  turbines pénalisées avec sauts de perméabilité, mode axisymétrique auto-généré au-delà d'un seuil de
  perméabilité, boîte périodique (3π)³ à 384³ points (Kreuzahler et al. 2017) — c'est le solveur LATU de Bousquet
  et al. (2026) `[RÉS ; TI arXiv:1706.00260v4]`.
- **Apprentissage** : aucune publication en apprentissage automatique trouvée parmi ses 30 notices HAL
  `[site S:299 ; WEB HAL]`.

### 2.4 Didier Lucor (LISN, CNRS)

- **Chaos polynomial généralisé** (premiers travaux d'application, co-signés avec D. Xiu et G. E. Karniadakis) :
  interaction fluide-structure stochastique (Xiu, Lucor, Su et
  Karniadakis 2002), oscillateurs aléatoires (2004), changement de mode de lâcher tourbillonnaire induit par le
  bruit (PRL 2004), sensibilité des LES à la constante de Smagorinsky (JFM 2007) `[RÉS]`.
- **Modèles réduits et espaces latents** : chaos polynomial en espace latent (2022) ; POD et processus gaussiens
  pour des LES paramétriques de dispersion (Nony et al. 2023) ; avec C. Nore, autoencodeurs et POD (2025), LES et
  POD de von Kármán (2024), autoencodeurs polynomiaux (2026, préprint) `[RÉS]`.
- **Apprentissage informé par la physique** : PINN pour la convection naturelle turbulente, en relâchant la
  condition d'incompressibilité « in such a way that it drastically benefits the optimization search » (Lucor,
  Agrawal et Sergent 2022) `[RÉS de la prépublication]` ; réseaux à base tensorielle respectant les invariances
  galiléenne et rotationnelle (Cai et al. 2024) `[RÉS]` ; reconstruction de température par PINN à partir de PIV
  (Volk et al. 2025).
- **Incertitude calibrée** : prédiction conforme pour évaluer des substituts par processus gaussiens (Jaber et al.
  2025) ; optimisation bayésienne robuste (2026) `[RÉS]`.
- **Assimilation** : directeur de la thèse de S. Cheng (2020, covariances d'erreur, avec EDF R&D) ; co-auteur de la
  revue apprentissage + assimilation + quantification d'incertitude (Cheng et al. 2023) `[RÉS ; WEB]`.
- **Dynamo** : aucune publication de théorie de la dynamo ; ses travaux liés aux dynamos sont co-signés avec
  C. Nore `[site S:103]`.

### 2.5 Sibo Cheng (CEREA, École nationale des ponts et chaussées)

- **Covariances en assimilation** (thèse avec D. Lucor) : méthodes adaptatives CUTE et PUB (2019), réglage des
  covariances (2021), localisation par clustering de graphe (2021), compression des observations (2021) `[RÉS]`.
- **Assimilation latente** : substitut et assimilation latente pour les incendies, « around 1000 times faster »
  que la simulation (2022) ; **assimilation latente généralisée** dans des espaces réduits hétérogènes, avec borne
  sur l'erreur de la fonction coût (2022) ; encodeurs-décodeurs multi-domaines (2024) ; opérateur d'observation
  appris (2025) ; assimilation latente non gaussienne par VAE (2026) `[RÉS]`.
- **Logiciel** : **TorchDA** (2025) : filtre de Kalman, EnKF, 3D-Var et 4D-Var avec des réseaux profonds comme
  opérateurs de transition et d'observation ; cité dans le résumé ANR de MilaDy `[RÉS ; WEB ANR]`. VIVID (2024)
  pour des capteurs épars et mobiles `[RÉS]`.
- **Modèles génératifs de champs physiques** : VQ-VAE 3D générant des séquences d'incendie (2023) ; diffusion
  conditionnelle avec attention croisée pour reconstruire des champs à partir d'observations éparses, meilleure
  sous bruit, la méthode déterministe l'étant sans bruit (Zhuang, Cheng et Duraisamy 2025) ; substitut de
  diffusion pour la propagation des incendies, avec échantillonnage d'ensemble (Yu et al. 2026) ; dynamique
  générative apprise dans un 4D-Var à contrainte faible (Bocquet, Finn et Cheng 2026, préprint) `[RÉS]`.
- **Contraintes et chaos** : réseaux multi-fidélité contraints par la physique (2024) ; PFNN, « Learning Chaos in
  a Linear Way », contraction et invariance de la mesure « without any explicit knowledge of the invariant
  measure » (ICLR 2025) ; opérateur neuronal à contraintes de moments et équivariance globale (Xue et al. 2026) ;
  revue de l'apprentissage sur maillages non structurés (2025) ; représentations de Koopman (Cheng X. et al.,
  ICLR 2026, S. Cheng co-auteur) `[RÉS ; site S:155]`.
- **Dynamo** : aucune publication sur les dynamos ou la MHD trouvée `[site S:103 ; WEB]`. Sa page décrit le rôle
  du CEREA dans MilaDy comme « physics-aware representation learning and reduced-order modelling of
  three-dimensional velocity and magnetic fields, connecting learned representations to data assimilation » et
  annonce le co-encadrement de la thèse avec D. Lucor `[WEB, autodescription]`.

### 2.6 Tableau croisé : pistes × encadrants (publications seulement)

| Piste | C. Nore | Y. Ponty | D. Lucor | S. Cheng |
|---|---|---|---|---|
| D1 théorie | Taylor–Green 1997 | faible Pm 2005, sous-critique 2007, on-off 2008, transition 2011, branches 2022, intermittence 2025 | — | — |
| D2 expériences | aucune expérience de dynamo ; expérience hydrodynamique de von Kármán en eau (2005) ; modèles numériques de VKS et DRESDYN | aucune expérience de dynamo trouvée ; LATU de VKS | — | — |
| D3 simulations | SFEMaNS, VKS 2008-2018, précession 2011-2026, Taylor–Couette 2012, transferts locaux 2024 | LATU 2014, 2017 ; Taylor–Green 2005-2014 | LES/POD de von Kármán 2024 (avec Nore) | — |
| D4 modèles réduits | DQVU 2026 ; POD de VKS 2025 | DQVU 2026 | AE/VAE et POD 2025 (avec Nore) | — |
| D5 statistiques | statistiques simulées de VKS (2026) | idem | — | — |
| A1 apprentissage | DQVU (PySINDy contraint) | aucune | PINN, réseaux invariants, chaos polynomial | Koopman, PFNN, opérateurs à moments |
| A2 génératifs | — | — | — | VQ-VAE 2023, diffusion 2025-2026 |
| A3 contraintes | moment d'ordre 3 dans DQVU | — | incompressibilité relâchée 2022, invariances 2024, équivariance latente 2025 | contraintes multi-fidélité 2024, moments 2026 |
| A4 assimilation | co-direction d'une thèse GNN et assimilation | — | covariances (avec Cheng), revue 2023 | assimilation latente, TorchDA, IEnKF-G |

Sources : §2.2-2.5 ; `[site S:217-299]`. **Ce qu'aucun des quatre n'a publié**, après recherches HAL, Crossref,
arXiv et pages personnelles : un modèle génératif (diffusion ou flow matching) entraîné sur des données de dynamo
ou de MHD ; un article d'apprentissage de Y. Ponty ; un article sur les dynamos de S. Cheng ; un article de théorie
de la dynamo de D. Lucor `[site E:513-519, S:103, S:299]`. Aucun n'est auteur d'une expérience de dynamo de
laboratoire ni d'une statistique paléomagnétique ; C. Nore a en revanche publié une expérience hydrodynamique de
von Kármán en eau (Nore, Moisy et Quartier 2005, visualisations et PIV) et co-signé Stefani et al. (2015), qui
présente des pré-expériences en eau pour DRESDYN `[RÉS]`.

---

## 3. La place précise du stage et de la thèse

### 3.1 Position sur la carte

MilaDy est ancré là où se rejoignent D2 (VKS, DRESDYN), D3 (SFEMaNS, LATU) et D4 (DQVU), avec le côté données
apporté par D. Lucor (représentations latentes) et S. Cheng (assimilation), que les pistes de la dynamo
commencent à peine à utiliser (Gwirtz 2022, Bousquet 2026, Guseva 2026) `[SYNTHÈSE]`. La thèse place un
**générateur conditionnel** entre les simulations (D3) et les modèles réduits et la statistique des inversions
(D4, D5) : paramètres λ = (Re, Rm, μr) → flow matching latent → décodeur en potentiels qui rend ∇·u = 0 et
∇·B = 0 exactes → symétrie B → −B par équivariance → bilan d'énergie imposé en loi → usages en aval (modèles
réduits, assimilation, fréquence des inversions par Rice) `[site T:82]`. Elle est organisée en quatre questions
(Q1 contraintes dures 3D en géométrie bornée, Q2 contraintes en loi, Q3 seuil et inversions, Q4 usages en aval)
`[site T:111-136]` et cinq paliers (0 Gissinger et DQVU ; 1 MHD 2D ; 2 dynamos 3D périodiques ABC et
Taylor–Green ; 3 VKS ; 4 DRESDYN) `[site T:857]`. Côté apprentissage, c'est l'intersection des pistes A2 et A3
appliquée à des champs de dynamo, avec A4 en aval ; c'est ce que demande l'offre de stage (« energy balance and
divergence-free conditions », génération « by diffusion or flow matching ») `[WEB offre 2027 ; site S:69-76]`.

Le **stage** est prospectif : trois expériences sur CPU, une ou deux graines, qui valident la chaîne de calcul et
testent les propositions de la note sur des cas où la vérité est connue (E1 Gissinger, E2 MHD 2D périodique,
E3 dynamo cinématique ABC sans générateur) ; il ne démontre pas la faisabilité en 3D, en domaine borné ou à haute
résolution `[site T:84-105]`.

### 3.2 Lacunes visées et travaux les plus proches

| # | Lacune | Stage (mesuré sur cas jouets) | Thèse (prévu) | Travaux les plus proches | Ce qu'ils ne font pas |
|---|---|---|---|---|---|
| G1 | Aucun générateur (diffusion, flow matching) de champs de dynamo | E2 : générateur conditionnel de MHD 2D sur η ; E3 : dynamo ABC 3D sans générateur `[site T:90-97]` | paliers 2-4 | Kacmaz et al. 2025 (MHD 2D, Pm = 1) ; Galletti et al. 2026 (états stationnaires, paramètres) ; GenCFD 2026 (statistiques 3D) | la 2D ne peut pas porter de dynamo ; pas de ∇·B dans le générateur ; pas de champ magnétique (Galletti, GenCFD) `[site R:240 ; L:301]` |
| G2 | ∇·u = ∇·B = 0 dures et conjointes en 3D, dans un cylindre borné avec raccord au vide, sauts de μr, maillage Fourier × éléments finis | E2 : potentiels (ψ, a) à 1,8·10⁻¹⁷ sans perte de qualité ; E3 : forme rotationnelle, ∇·B < 1,6·10⁻¹⁶ en 3D périodique `[site T:92, T:97]` | Q1 `[site T:111-117]` | PCDM 2026 (Leray 3D périodique) ; Mohan et al. 2023 (potentiel vecteur 3D, périodique, non génératif, sans jauge) ; FunDiff (fonction de courant 2D) ; Richter-Powell 2022 (tore) ; ECI, PCFM (valeurs au bord, 1D-2D) | aucun ne traite parois + raccord au vide + coudes de perméabilité, ni u et B ensemble `[site R:241-242 ; E:518]` |
| G3 | Identités de stationnarité d'une EDP de champ comme contraintes en loi d'un générateur conditionnel paramétrique, sans valeur cible, imposables là où il n'y a pas de données | E2 : résidu du bilan moyen 0,46 → 0,061 et distance d'énergie 2,52 → 0,70 aux η de test, encore au-dessus du plancher de bruit honnête (0,030) `[site T:94]` | Q2 `[site T:119-124]` | Weak Generative Sampler (EDS, dimension ≤ 100, non conditionnel) ; Tauberschmidt 2026 (résidu faible, par échantillon) ; Khalifa 2021, Mun 2026, Khalafi 2024 (cibles externes) ; Wu 2020 (covariance) ; DySLIM | aucun ne combine EDP de champ, conditionnement paramétrique, identités sans cible et entraînement sans données `[site T:147-149, T:156 ; R:120]` |
| G4 | Incohérence d'une contrainte par échantillon pour un bilan stationnaire (corollaire 6), mesurée | E2 : la remise à l'échelle par échantillon annule le résidu mais réduit l'écart-type de la dissipation à 8,6·10⁻⁴ fois celui des données ; E1 : la projection par échantillon multiplie la distance d'énergie par 9 `[site T:88, T:95]` | mesure sur dynamos 3D `[site E:516]` | **PBFM (ICLR 2026)** ; analyse de l'écart de Jensen de PIDM ; Genuist et al. 2026 | PBFM énonce un compromis à l'entraînement pour des résidus d'EDP par échantillon ; il n'énonce pas qu'une contrainte valable seulement en moyenne est incohérente si on l'impose par échantillon `[SYNTHÈSE d'après le résumé]` |
| G5 | Symétrie B → −B et R_π par équivariance, complémentaire de la stationnarité | E1 : champ équivariant, asymétrie au plancher (0,004) aux Γ jamais vus ; l'augmentation ne suffit pas `[site T:88]` | §2.4, action conjointe état-paramètre `[site T:151]` | Köhler et al. 2020 ; Klein et al. 2023 ; Wang, Walters et Yu 2021 ; Bousquet, Nore et Lucor 2025 | la complémentarité avec les identités et l'action conjointe état-paramètre `[site T:159 ; R:123]` |
| G6 | Fréquence des inversions tirée d'un générateur d'instantanés par la formule de Rice, sans intégration temporelle | E1 : erreur relative cumulée 4-6 % sur la loi de référence, 14 % sur la loi générée loin du seuil, 42 % près du seuil `[site T:88]` | Q3 `[site T:126-131]` | Gwirtz 2022 (séries temporelles, négatif) ; Yang et Schmid 2025 (convection 2D) ; Finzi 2023 (événements rares) ; Lucente 2022 (committors) ; Rice 1944-1945, Azaïs et Wschebor 2009 | tous exigent des trajectoires ou une définition cible de l'événement ; aucun ne transforme une loi stationnaire d'instantanés et le second membre en fréquence de traversées `[site T:158 ; R:122]` |
| G7 | Erreur d'un générateur régulier en λ près d'un seuil (proposition 9) ; conditionnement à travers le seuil | E1 : 42 % d'erreur de Rice près du seuil `[site T:88]` | Q3 ; palier 2 | ACDM (extrapolation en Re) ; Kacmaz (erreur > 0,85 à Re = 100 pour un modèle entraîné à Re = 1000) `[site L:382]` ; Galletti | aucun modèle génératif n'étudie la traversée d'une bifurcation ni ne conditionne conjointement sur (Re, Rm) `[site R:244 ; E:518]` |
| G8 | Modèle réduit identifié à partir d'instantanés générés et du second membre, sans dériver de séries temporelles | — | Q4, DQVU `[site T:133-136]` | Bousquet et al. 2026 (PySINDy contraint sur séries de DNS) ; Loiseau et Brunton 2018 ; Kaptanoglu et al. 2021 | identification à partir de séries temporelles, jamais d'un générateur `[SYNTHÈSE]` |
| G9 | A priori génératif pour l'assimilation de (u, B) avec loi a posteriori bimodale ±B | — | Q4 avec TorchDA, mois 25-27 `[site T:136 ; E:491]` | SDA 2023 ; Rozet et al. 2024 ; EnSF 2024 ; GLA et TorchDA ; Zhuang, Cheng et Duraisamy 2025 ; Bocquet, Finn et Cheng 2026 ; Fournier et al. 2010 | aucune assimilation par diffusion sur la MHD ; aucun a priori qui respecte la polarité `[site L:385 ; E:491]` |
| G10 | Métriques MHD pour des champs générés (spectres, hélicités, bilans, topologie) | métriques de E2 ; le résidu d'hélicité croisée ne discrimine pas les modèles `[site R:1037]` | protocole commun §3.1 `[site T:859-876]` | Lienen 2024 (W2 sur spectres) ; GenCFD (CRPS) ; Biferale et Buzzicotti 2026 ; Creff et al. 2024 ; Ponty et al. 2025 | aucun travail n'évalue hélicités, bilans ou topologie des lignes de champ de champs générés `[site R:243]` |

### 3.3 Ce qui serait nouveau, et l'état de chaque revendication

Le rapport et la thèse revendiquent six points, « to our knowledge, after a literature search closed on
November 6, 2026 » `[site R:118-125 ; T:154-161]`. Leur état après la synthèse du 8 novembre 2026 :

| Revendication | Travaux les plus proches trouvés | État `[SYNTHÈSE]` |
|---|---|---|
| 1. Identités de stationnarité d'une EDP de champ comme contraintes en loi d'un générateur conditionnel paramétrique, sans valeur cible, imposables sans données | Weak Generative Sampler (Cai et al. 2026) ; Tauberschmidt et al. 2026 ; Khalifa 2021 ; Mun 2026 ; Khalafi 2024 | tient ; le site cite déjà ces travaux `[site T:147-149]` |
| 2. Énoncé et mesure de l'incohérence d'une contrainte par échantillon pour un bilan stationnaire | **PBFM (Baldan et al., ICLR 2026)**, absent du site ; PIDM (écart de Jensen) ; Genuist et al. 2026 | **à repositionner** : PBFM revendique la découverte du compromis exactitude en loi / exactitude physique ; la nuance (contrainte valable seulement en moyenne, imposée par échantillon) doit être énoncée explicitement et PBFM cité |
| 3. Formule de Rice appliquée à un générateur d'instantanés | aucun précédent trouvé ; Gwirtz 2022 et Finzi 2023 sont les plus proches | tient |
| 4. Complémentarité symétrie / stationnarité | Köhler et al. 2020 (invariance par équivariance) | tient ; le résultat d'équivariance lui-même est classique et cité comme tel `[site R:115]` |
| 5. Estimateur sans biais par produit des moyennes de deux demi-lots | aucune recherche dédiée faite | point technique ; l'astuce d'estimer (E g)² sans biais par le produit de deux moyennes indépendantes est élémentaire et peut figurer ailleurs `[NON VÉRIFIÉ]` |
| 6. Borne inférieure de l'erreur près d'un saut de la loi (proposition 9) | ACDM, Kacmaz (extrapolation) | tient ; aucun travail sur la traversée d'une bifurcation par un générateur |

Autre absence que le site présente comme lacune 1 : aucun modèle génératif entraîné sur des simulations de dynamo
`[site E:514]`. Elle reste confirmée par la recherche du 8 novembre 2026, mais c'est une affirmation négative.

### 3.4 Risques d'être devancé

Ce qui suit est une lecture de ce document `[SYNTHÈSE]` : chaque ligne nomme un travail publié (sourcé au §1.4) et
ce qu'il lui manquerait pour recouvrir une partie du stage ou de la thèse. Elle ne prête aucune intention aux
auteurs.

| Travail ou groupe | Ce qu'il fait déjà | Recouvrement possible | Ce qui resterait propre à la thèse |
|---|---|---|---|
| PBFM (Baldan, Liu, Guardone, Thuerey ; ICLR 2026) | compromis entre exactitude en loi et résidus d'EDP, flow matching | revendication 2 | contrainte valable en moyenne seulement ; identités sans cible ; MHD |
| PCDM (Li, Buzzicotti, Bonaccorso, Biferale ; 2026, préprint) | diffusion 3D à divergence nulle exacte, périodique | G2 en périodique | géométrie bornée, raccord au vide, μr ; u et B conjoints |
| Même communauté : Martin, Lübke, Li, Buzzicotti, **Grauer**, Biferale (2025) | diffusion entraînée sur des particules test dans une turbulence MHD 3D | passage à des champs B 3D périodiques | R. Grauer est co-auteur des articles LATU avec Y. Ponty (Kreuzahler et al. 2014, 2017) : une collaboration possible plutôt qu'un concurrent, à discuter avec Y. Ponty |
| Kacmaz, Huerta, Haas (2025) | opérateur + diffusion pour la MHD 2D | G1 si passage en 3D | dynamo (3D), ∇·B dans le générateur, inversions |
| Scheinker (2026, préprint) | diffusion latente conditionnelle bidirectionnelle qui estime ses erreurs de déroulement ; MHD compressible parmi trois cas tests | G1 (recouvrement faible) | contraintes dures, dynamo, statistique des inversions |
| Galletti et al. (2026, préprint) | flow matching conditionnel d'états saturés | idée du générateur d'instantanés d'états stationnaires | champ magnétique, contraintes, Rice |
| Genuist, Savin, Gatti, Clouteau (2026, préprint) | comparaison de six stratégies de divergence nulle | comparaison du stage (E2) | MHD, contraintes en loi, 3D bornée |
| Cai et al. (2026) ; Tauberschmidt et al. (2026) | forme faible de Fokker–Planck ; résidu faible par échantillon | revendication 1 si extension aux EDP de champ conditionnelles | conditionnement paramétrique, identités sans cible, MHD |
| Guseva, Skene, Tobias (2026, préprint) | équations d'un cycle de dynamo par DMD + SINDy | Q4 (modèles réduits identifiés) | identification à partir d'un générateur, VKS |

**Parade déjà prévue par le site** : une veille bibliographique avant chaque soumission `[site T:163]` et un
premier article (contraintes en loi) au mois 10 `[site E:493-499]`.

### 3.5 Ce que ni le stage ni la thèse ne prétendent résoudre

- La **loi des temps d'attente** entre inversions : elle n'est pas déterminée par la loi stationnaire et demande
  de courtes trajectoires lancées depuis des échantillons générés `[site T:80, T:131]`.
- Un **Pm de type sodium** : le générateur hérite du Pm des DNS sur lesquelles il est entraîné, ≈ 0,33 dans le run
  de référence des inversions de VKS `[site R:161, calcul de ce document]`.
- La **géodynamo** et les **mesures expérimentales de VKS** : l'assimilation est prévue à partir de sondes
  magnétiques synthétiques `[site E:491]`.
- La **faisabilité en 3D borné**, que E1-E3 ne démontrent pas `[site T:105]`.

---

## 4. Questions à poser aux encadrants

Chaque question découle de l'état de l'art ci-dessus. « Pourquoi » dit ce qui la motive (avec la source), « ce
que la réponse débloque » dit la décision qu'elle permet. Les questions déjà posées par le film (cartes `chXX.Q`)
sont signalées pour éviter les doublons.

**Q-1. PBFM et la revendication 2.** « Baldan et al. (ICLR 2026) revendiquent la découverte du compromis entre
exactitude en loi et exactitude physique : comment formuler notre résultat sur l'incohérence d'une contrainte par
échantillon pour un bilan stationnaire, et faut-il ajouter PBFM comme méthode de comparaison au palier 1 ? »
- À qui : S. Cheng, D. Lucor.
- Pourquoi : la revendication 2 `[site R:121 ; T:157]` ne cite pas PBFM ; le résumé de PBFM revendique
  « the first to recognize the trade-off » `[RÉS]`.
- Ce que la réponse débloque : la formulation de l'article 1 et la liste des méthodes de référence.

**Q-2. Accès aux inversions simulées de VKS.** « Quelles séries de Bousquet et al. (2026) peuvent nous être
transmises, dans quel format, combien d'inversions contient chacune, et à quels (Re, Rm, μr, asymétrie) ? »
- À qui : C. Nore, Y. Ponty.
- Pourquoi : le palier 3 dépend de données non publiques, « available from the authors upon reasonable request »
  `[site R:161 ; T:929, T:982]` ; le risque « trop peu d'inversions pour valider Rice » est noté élevé
  `[site T:995]`.
- Ce que la réponse débloque : la demande d'accès au premier trimestre et le calendrier du palier 3. Complète la
  carte `ch09.Q` (durée des runs).

**Q-3. Quels paramètres de conditionnement, couche extérieure comprise ?** « Faut-il ajouter au vecteur λ la
conductivité ou la perméabilité du milieu extérieur et des parois, en plus de Re, Rm, μr et de l'asymétrie de
forçage ? »
- À qui : C. Nore.
- Pourquoi : un milieu environnant conducteur s'est révélé « necessary for these inversions to occur »
  (Bousquet et al. 2026) `[site S:227-235]` ; des parois conductrices ou perméables favorisent ou suppriment la
  dynamo de précession (Botez et al. 2026) `[RÉS]` ; vide et pseudo-vide décalent Rm_c d'environ 40 %
  (Nore et al. 2018) `[site R:143]`.
- Ce que la réponse débloque : la définition de λ, donc le plan des simulations et l'architecture du
  conditionnement.

**Q-4. LATU d'abord ou SFEMaNS d'abord ?** « Dans LATU, comment les sauts de perméabilité et le milieu extérieur
sont-ils représentés par la pénalisation, et quelle condition de divergence est exacte sur sa grille ? »
- À qui : Y. Ponty (LATU), C. Nore (SFEMaNS).
- Pourquoi : le site propose de commencer par LATU, dont la grille cartésienne est la plus simple `[site E:485]` ;
  mais LATU calcule dans une boîte périodique (3π)³ à 384³ points `[TI : Kreuzahler et al. 2017]`, où la
  projection de Leray ou les potentiels suffisent (E2, E3, PCDM), alors que la question Q1 porte sur les parois, le
  vide et les sauts de μr, que seul SFEMaNS représente nativement `[site T:111-117]` `[SYNTHÈSE]`.
- Ce que la réponse débloque : l'ordre du palier 3 et la contrainte à construire en premier. Complète la carte
  `ch08.Q`.

**Q-5. Des données LES comme données d'entraînement ?** « Les simulations LES à grand Re (Nore et al. 2018 ;
Ponty et al. 2005) peuvent-elles servir à entraîner le générateur, et que peut-on alors affirmer des petites
échelles générées ? »
- À qui : C. Nore, Y. Ponty.
- Pourquoi : le faible Pm est un problème ouvert (§1.5) ; le générateur hérite du Pm des données ; ces deux
  travaux atteignent des Re ou des Pm inaccessibles en DNS grâce à la LES `[site S:223-225, S:279-280]`.
- Ce que la réponse débloque : le choix des données des paliers 2 et 3 (DNS seulement, ou DNS et LES). Complète la
  carte `ch02.Q` (quelles valeurs de Pm).

**Q-6. Quelle symétrie imposer ?** « Puisque les données brisent R_π (état métastable de Bousquet et al. 2024 ;
phase saturée de Botez et al. 2025), faut-il imposer l'équivariance R_π avec action conjointe sur l'asymétrie de
forçage, ou seulement B → −B ? »
- À qui : C. Nore, D. Lucor.
- Pourquoi : la thèse prévoit une action conjointe état-paramètre `[site T:151]` ; imposer une symétrie que la loi
  stationnaire n'a pas biaiserait le générateur `[SYNTHÈSE]` ; les deux brisures sont publiées `[RÉS]`.
- Ce que la réponse débloque : l'architecture du champ de vitesse du flot (palier 3).

**Q-7. Précurseurs ou fréquences ?** « L'objectif (i) de MilaDy (phases de précurseur, d'inversion et de
récupération) attend-il de la thèse des précurseurs, ou la fréquence des inversions suffit-elle ? »
- À qui : C. Nore, S. Cheng, D. Lucor.
- Pourquoi : la formule de Rice donne une fréquence moyenne, pas les précurseurs ni les temps d'attente
  `[site T:131]` ; Gwirtz et al. (2022) n'ont pas trouvé de précurseur fiable par apprentissage sur les données
  géomagnétiques `[RÉS]`.
- Ce que la réponse débloque : le périmètre de Q3. Prolonge la carte `ch00.Q`.

**Q-8. La contrainte de moment d'ordre 3 de DQVU.** « Comment cette contrainte a-t-elle été choisie, et
l'identification d'un modèle de type DQVU à partir d'instantanés générés (Q4) doit-elle la conserver ? »
- À qui : C. Nore, Y. Ponty.
- Pourquoi : DQVU est identifié sous conservation de l'énergie quadratique et d'un moment d'ordre 3
  `[site S:234]` ; le site y voit, selon sa propre lecture, une contrainte sur des moyennes déjà utilisée dans le
  consortium `[site E:487]`.
- Ce que la réponse débloque : le protocole de Q4 (quels invariants préserver en identifiant depuis un générateur).

**Q-9. Assimilation : quelles sondes et quelle méthode ?** « Quelle disposition de sondes magnétiques synthétiques
viser (proche de celle de VKS ?) et quelle méthode de TorchDA (EnKF, 4D-Var latent, dynamique générative) pour la
direction C ? »
- À qui : S. Cheng, C. Nore.
- Pourquoi : aucune assimilation par diffusion n'a été appliquée à la MHD `[site L:385]` ; la loi a posteriori est
  bimodale près d'une inversion `[site E:491]` ; TorchDA et IEnKF-G sont les outils du consortium `[RÉS]`.
- Ce que la réponse débloque : la conception de Q4 (mois 25-27).

**Q-10. DRESDYN et le palier 4.** « Où en est l'expérience de précession, et les champs de vitesse moyennés de
Botez et al. (2026) seront-ils accessibles ? »
- À qui : C. Nore.
- Pourquoi : aucun premier essai au sodium n'a été trouvé au 8 novembre 2026 `[NON VÉRIFIÉ]` ; l'offre de
  post-doctorat MilaDy écrit que le succès de la dynamo DRESDYN « remains uncertain » `[WEB : offre de post-doctorat LISN]` ; le
  palier 4 dépend de ces champs « if they are accessible » `[site E:491]`.
- Ce que la réponse débloque : le maintien ou l'abandon du palier 4, le premier sacrifié en cas de retard
  `[site T:999]`.

**Q-11. Outils de métriques MHD.** « L'outil de transferts d'énergie locaux sur maillage non structuré de Creff
et al. (2024) est-il disponible pour évaluer des champs générés, et les relations kurtosis–asymétrie de Ponty et
al. (2025) peuvent-elles servir de critère ? »
- À qui : C. Nore, Y. Ponty.
- Pourquoi : aucun travail n'évalue hélicités, bilans ou topologie de champs générés (G10) `[site R:243]` ; la
  revue de Biferale et Buzzicotti (2026) ne propose pas de métrique MHD `[site L:233]`.
- Ce que la réponse débloque : le protocole d'évaluation commun `[site T:859-876]`. Précise la carte `ch06.Q`.

**Q-12. Espace latent : POD, autoencodeur polynomial ou VAE ?** « Pour un modèle latent de type FunDiff, faut-il
partir d'une base POD ou des autoencodeurs polynomiaux initialisés comme la POD, plutôt que d'un VAE ? »
- À qui : D. Lucor.
- Pourquoi : Bousquet, Nore et Lucor (2025) montrent qu'augmenter la régularisation du VAE dégrade la
  reconstruction `[RÉS]` ; les autoencodeurs polynomiaux de 2026 (préprint) accélèrent l'entraînement par
  l'initialisation POD `[RÉS]` ; l'hypothèse H2 sur le coût du modèle latent est à mesurer au palier 1
  `[site T:960]`.
- Ce que la réponse débloque : le choix de représentation des paliers 1 à 3.

**Q-13. Veille et calendrier de publication.** « Qui assure la veille bibliographique, et faut-il avancer un
premier article sur les contraintes en loi (paliers 0-1) avant le mois 10 ? »
- À qui : les quatre encadrants.
- Pourquoi : plusieurs groupes publient sur des sujets voisins en 2025-2026 (§3.4) ; le site prévoit une veille
  avant chaque soumission `[site T:163]`.
- Ce que la réponse débloque : l'ordre des articles et la première échéance.

---

## 5. Divergences entre sources et points non vérifiés

**Divergences relevées** (citez la valeur indiquée en gras) :
- Second article de Lowes et Wilkinson : 1967 dans le texte de Stefani et al. (2018), **1968** dans Crossref.
- Masse de sodium de DRESDYN : 6 t (Stefani et al. 2018) ou 8 t (Pizzi et al. 2023) : donnez les deux ou aucune.
- Kazantsev : 1967 (original russe) ou **1968** (traduction JETP).
- Stefani et al. (2007) : titre arXiv (*Reversals in nature and the nature of reversals*) différent du titre de la
  revue (*Oscillation or rotation: a comparison of two simple reversal models*) : citez le titre de la revue.
- Superchron permo-carbonifère (Kiaman) : 312-262 Ma (Stefani et al. 2007) ou 302-252 Ma (Constable).
- Dernière inversion : ≈ 780 ka (sources anciennes) ou **≈ 773 ka** (Singer et al. 2019, datation plus récente).
- Premier essai de Riga : 1986 ou 1987 selon les sources `[site Dy:615]`.
- Dates et montant de MilaDy : retenez la page ANR (§2.1).
- Ponty et al. (2005) : la phrase sur le spectre de Kazantsev est dans le résumé arXiv, pas dans le résumé publié.
- Mininni et al. (2005) : *ApJ* (Crossref), non *ApJ Letters* (HAL).
- Titres sur la page de S. Cheng différents des titres publiés (Tensor-Var ; article de *Phys. Chem. Chem. Phys.*
  2023) et années décalées d'un an (TorchDA, VIVID, DSOVT) : citez Crossref ou PMLR.
- Ordre des auteurs différent entre arXiv et la revue pour Mohan et al. (2023) et Illarionov et al. (2026) : citez
  la revue.
- GenCFD : premier auteur, titre et résumé diffèrent entre arXiv:2409.18359 (Molinaro et al., « fast and
  accurate », « regress to the mean flow ») et *Nat. Commun.* 17, 9846 (Raonić et al., « efficient ») : citez la
  revue, et attribuez la citation « regress to the mean flow » à la prépublication.
- Une notice HAL au nom de « Sibo Cheng » (rapport technique de physique des particules, 2025) est un homonyme ;
  elle n'est pas attribuée.

**Non vérifié** (ne pas reprendre sans nouvelle vérification) :
- Larmor (1919) : titre et pages du rapport (sources secondaires seulement).
- Glatzmaier et Roberts (1995) : formulation exacte du résumé.
- Christensen et al. (2001) : définition des cas du benchmark.
- Contenu de Nozières (1978), Jonkers (2003), Valet et al. (2005), Ogg (2020), Zimmerman et al. (2014) : titres
  seulement.
- Steenbeck et al. (1967, mesure d'un effet α dans le sodium) et Gans (1971, précession) : sources secondaires.
- État de DRESDYN en 2026.
- Jarolim et al. (2023) : termes de perte (résumé de prépublication) ; chiffres de PBFM sur Darcy (résumé web).
- Réservoirs de calcul sur les données de l'expérience de 3 m du Maryland : résumés de conférence APS seulement.
- Article JCP de Botez, Bousquet et Nore annoncé « in press » : introuvable.
- Nom du post-doctorant MilaDy à l'OCA (« Hiiro » dans le CV de Y. Ponty, « Horii » dans HAL).
- Chiffres de la version JCP de Lucor et al. (2022) (Ra = 2·10⁹ vient de la prépublication).
- Exposant « Re > 10⁴ » de Bousquet et al. (2024), lu dans les métadonnées.

---

## 6. Sources

Toutes les références ci-dessous ont leurs métadonnées vérifiées le 8 novembre 2026 dans Crossref (DOI) ou dans
l'API arXiv (identifiant), sauf mention contraire.

### 6.1 Fichiers du site (`/home/user/milady-2027`)

- `en/these/index.qmd` (T) : §1.2 expériences du stage (l. 84-105), questions Q1-Q4 (l. 111-136), §1.4 travaux
  antérieurs et revendications (l. 140-163), paliers (l. 857-950), risques (l. 982-999).
- `en/rapport/index.qmd` (R) : revendications (l. 118-125), contexte VKS et données (l. 137-163), lacunes
  (l. 240-245).
- `en/encadrants/index.qmd` (E) : continuité stage-thèse et directions C, D (l. 482-491), ce qui reste à faire
  (l. 497-519).
- `en/prep/p3-mhd-dynamo/index.qmd` (P3) ; `en/prep/p8-contraintes-physiques/index.qmd`.
- `specs/sources/encadrants.md` (S), `specs/sources/dynamo.md` (Dy), `specs/sources/litterature.md` (L),
  `specs/sources/donnees-metriques.md`.
- `video/BRIEF.md` §10.

### 6.2 Revues de synthèse lues en entier

- Rincon F. (2019). Dynamo theories. *J. Plasma Phys.* 85(4), 205850401. doi:10.1017/S0022377819000539 ;
  arXiv:1903.07829.
- Tobias S. M. (2021). The turbulent dynamo. *J. Fluid Mech.* 912, P1. doi:10.1017/jfm.2020.1055 ;
  arXiv:1907.03685.
- Stefani F., Gailitis A., Gerbeth G., Giesecke A., Gundrum T., Rüdiger G., Seilmayer M., Vogt T. (2019). The
  DRESDYN project: liquid metal experiments on dynamo action and magnetorotational instability. *Geophys.
  Astrophys. Fluid Dyn.* 113(1-2), 51-70. doi:10.1080/03091929.2018.1501481 ; prépublication arXiv:1803.03421
  (titre différent).
- Constable C. (2003). Geomagnetic reversals: rates, timescales, preferred paths, statistical models and
  simulations. In Jones, Soward, Zhang (dir.), *Earth's Core and Lower Mantle*, Taylor & Francis, 77-99.
  doi:10.1201/9780203207611.ch4 (texte lu : prépublication de l'autrice, 2001).

### 6.3 Dynamo

*Théorie (D1)*
- Larmor J. (1919). How could a rotating body such as the Sun become a magnet? *Rep. Brit. Assoc. Adv. Sci.*,
  159-160 `[NON VÉRIFIÉ : titre et pages]`.
- Cowling T. G. (1933). The magnetic field of sunspots. *MNRAS* 94, 39-48. doi:10.1093/mnras/94.1.39.
- Kaiser R., Tilgner A. (2014). The axisymmetric antidynamo theorem revisited. *SIAM J. Appl. Math.* 74(2),
  571-597. doi:10.1137/130928376 `[site Dy:440]`.
- Taylor G. I., Green A. E. (1937). Mechanism of the production of small eddies from large ones. *Proc. R. Soc.
  A* 158, 499-521. doi:10.1098/rspa.1937.0036.
- Batchelor G. K. (1950). On the spontaneous magnetic field in a conducting liquid in turbulent motion. *Proc. R.
  Soc. A* 201, 405-416. doi:10.1098/rspa.1950.0069.
- Parker E. N. (1955). Hydromagnetic dynamo models. *ApJ* 122, 293. doi:10.1086/146087.
- Herzenberg A. (1958). Geomagnetic dynamos. *Phil. Trans. R. Soc. A* 250, 543-583. doi:10.1098/rsta.1958.0007.
- Backus G. (1958). A class of self-sustaining dissipative spherical dynamos. *Ann. Phys.* 4, 372-447.
  doi:10.1016/0003-4916(58)90054-X.
- Steenbeck M., Krause F., Rädler K.-H. (1966). *Z. Naturforsch. A* 21, 369-376. doi:10.1515/zna-1966-0401.
- Krause F., Rädler K.-H. (1980). *Mean-Field Magnetohydrodynamics and Dynamo Theory*. Pergamon / Akademie-Verlag.
  doi:10.1515/9783112729694.
- Kazantsev A. P. (1968). Enhancement of a magnetic field by a conducting fluid. *Sov. Phys. JETP* 26(5), 1031
  (ZhETF 53, 1806, 1967) `[notice seulement]`.
- Childress S. (1970). New solutions of the kinematic dynamo problem. *J. Math. Phys.* 11, 3063-3076.
  doi:10.1063/1.1665095.
- Roberts G. O. (1970). Spatially periodic dynamos. *Phil. Trans. R. Soc. A* 266, 535-558.
  doi:10.1098/rsta.1970.0011 ; (1972) Dynamo action of fluid motions with two-dimensional periodicity. *Phil.
  Trans. R. Soc. A* 271, 411-454. doi:10.1098/rsta.1972.0015.
- Ponomarenko Yu. B. (1973). Theory of the hydromagnetic generator. *J. Appl. Mech. Tech. Phys.* 14, 775-778.
  doi:10.1007/BF00853190.
- Vainshtein S. I., Zel'dovich Ya. B. (1972). Origin of magnetic fields in astrophysics. *Sov. Phys. Usp.* 15,
  159-172. doi:10.1070/PU1972v015n02ABEH004960.
- Galloway D., Frisch U. (1986). Dynamo action in a family of flows with chaotic streamlines. *GAFD* 36, 53-83.
  doi:10.1080/03091928608208797.
- Archontis et al. (2003) : fenêtres dynamo de l'écoulement ABC, vérifiées par le site dans cette source (la
  source primaire de Galloway et Frisch 1984 étant inaccessible) `[site Dy:41, Dy:386-412]` ; métadonnées non
  revérifiées le 8 novembre 2026.
- Soward A. M. (1987). Fast dynamo action in a steady flow. *J. Fluid Mech.* 180, 267-295.
  doi:10.1017/S0022112087001800.
- Galloway D. J., Proctor M. R. E. (1992). *Nature* 356, 691-693. doi:10.1038/356691a0.
- Childress S., Gilbert A. D. (1995). *Stretch, Twist, Fold: The Fast Dynamo*. Springer.
  doi:10.1007/978-3-540-44778-8.
- Schekochihin A. A., Haugen N. E. L., Brandenburg A., Cowley S. C., Maron J. L., McWilliams J. C. (2005). The
  onset of a small-scale turbulent dynamo at low magnetic Prandtl numbers. *ApJ* 625, L115-L118.
  doi:10.1086/431214.
- Iskakov A. B., Schekochihin A. A., Cowley S. C., McWilliams J. C., Proctor M. R. E. (2007). Numerical
  demonstration of fluctuation dynamo at low magnetic Prandtl numbers. *PRL* 98, 208501.
  doi:10.1103/PhysRevLett.98.208501.
- Warnecke J., Korpi-Lagg M. J., Gent F. A., Rheinhardt M. (2023). Numerical evidence for a small-scale dynamo
  approaching solar magnetic Prandtl numbers. *Nature Astron.* 7, 662-668. doi:10.1038/s41550-023-01975-1.

*Expériences (D2)*
- Lowes F. J., Wilkinson I. (1963). Geomagnetic dynamo: a laboratory model. *Nature* 198, 1158-1160.
  doi:10.1038/1981158a0 ; (1968) *Nature* 219, 717-718. doi:10.1038/219717a0.
- Gailitis A. et al. (2000). Detection of a flow induced magnetic field eigenmode in the Riga dynamo facility.
  *PRL* 84, 4365-4368. doi:10.1103/PhysRevLett.84.4365.
- Stieglitz R., Müller U. (2001). Experimental demonstration of a homogeneous two-scale dynamo. *Phys. Fluids*
  13, 561-564. doi:10.1063/1.1331315.
- Bourgoin M. et al. (2002). *Phys. Fluids* 14, 3046-3058. doi:10.1063/1.1497376.
- Ravelet F., Chiffaudel A., Daviaud F., Léorat J. (2005). *Phys. Fluids* 17, 117104. doi:10.1063/1.2130745.
- Monchaux R. et al. (2007). Generation of a magnetic field by dynamo action in a turbulent flow of liquid sodium.
  *PRL* 98, 044502. doi:10.1103/PhysRevLett.98.044502.
- Berhanu M. et al. (2007). Magnetic field reversals in an experimental turbulent dynamo. *EPL* 77, 59001.
  doi:10.1209/0295-5075/77/59001.
- Spence E. J., Nornberg M. D., Jacobson C. M., Kendrick R. D., Forest C. B. (2006). *PRL* 96, 055002.
  doi:10.1103/PhysRevLett.96.055002.
- Frick P., Noskov V., Denisov S., Stepanov R. (2010). *PRL* 105, 184502. doi:10.1103/PhysRevLett.105.184502.
- Zimmerman D. S., Triana S. A., Nataf H.-C., Lathrop D. P. (2014). *JGR Solid Earth* 119, 4538-4557.
  doi:10.1002/2013JB010733 (contenu non lu).
- Stefani F. et al. (2012). DRESDYN – a new facility for MHD experiments with liquid sodium.
  *Magnetohydrodynamics* 48(1), 103-114. doi:10.22364/mhd.48.1.13.
- Pizzi F. et al. (2023). arXiv:2301.08076 (introduction lue).
- Giesecke A., Wilbert M., Šimkanin J., Grauer R., Stefani F. (2024-2025). arXiv:2410.14449 (v3, introduction lue).
- Tzeferacos P. et al. (2018). *Nat. Commun.* 9, 591. doi:10.1038/s41467-018-02953-2.
- Cooper C. M. et al. (2014). *Phys. Plasmas* 21, 013505. doi:10.1063/1.4861609.
- Gailitis A., Lielausis O., Platacis E., Gerbeth G., Stefani F. (2002). Colloquium: Laboratory experiments on
  hydromagnetic dynamos. *Rev. Mod. Phys.* 74, 973-990. doi:10.1103/RevModPhys.74.973.

*Simulations (D3)*
- Meneguzzi M., Frisch U., Pouquet A. (1981). Helical and nonhelical turbulent dynamos. *PRL* 47, 1060-1064.
  doi:10.1103/PhysRevLett.47.1060.
- Glatzmaier G. A., Roberts P. H. (1995). A three-dimensional self-consistent computer simulation of a geomagnetic
  field reversal. *Nature* 377, 203-209. doi:10.1038/377203a0 ; et (1995) A three-dimensional convective dynamo
  solution with rotating and finitely conducting inner core and mantle. *PEPI* 91, 63-75.
  doi:10.1016/0031-9201(95)03049-3 (l'article que cite Tobias §8.3 pour « l'ère moderne »).
- Kageyama A., Sato T. (1995). *Phys. Plasmas* 2, 1421-1431. doi:10.1063/1.871485.
- Christensen U. R. et al. (2001). A numerical dynamo benchmark. *PEPI* 128, 25-34.
  doi:10.1016/S0031-9201(01)00275-8.
- Kutzner C., Christensen U. R. (2002). From stable dipolar towards reversing numerical dynamos. *PEPI* 131,
  29-45. doi:10.1016/S0031-9201(02)00016-X.
- Jones C. A. et al. (2011). *Icarus* 216, 120-135. doi:10.1016/j.icarus.2011.08.014.
- Matsui H. et al. (2016). *G-cubed* 17, 1586-1607. doi:10.1002/2015GC006159.
- Schaeffer N., Jault D., Nataf H.-C., Fournier A. (2017). Turbulent geodynamo simulations: a leap towards
  Earth's core. *GJI* 211, 1-29. doi:10.1093/gji/ggx265.
- Aubert J., Gastine T., Fournier A. (2017). *J. Fluid Mech.* 813, 558-593. doi:10.1017/jfm.2016.789.
- Krstulovic G., Thorner G., Vest J.-P., Fauve S., Brachet M. (2011). *PRE* 84, 066318.
  doi:10.1103/PhysRevE.84.066318.
- Gissinger C., Dormy E., Fauve S. (2010). *EPL* 90, 49001 `[site Dy:291-304]`.
- Giesecke A., Stefani F., Gerbeth G. (2010). *PRL* 104, 044503 `[site Dy:188-196]`.
- Giesecke A., Vogt T., Gundrum T., Stefani F. (2018). *PRL* 120, 024502 `[site S:259]`.

*Modèles réduits (D4)*
- Bullard E. (1955). The stability of a homopolar dynamo. *Math. Proc. Camb. Phil. Soc.* 51, 744-760.
  doi:10.1017/S0305004100030814.
- Rikitake T. (1958). Oscillations of a system of disk dynamos. *Math. Proc. Camb. Phil. Soc.* 54, 89-105.
  doi:10.1017/S0305004100033223.
- Nozières P. (1978). *PEPI* 17, 55-74. doi:10.1016/0031-9201(78)90047-X (contenu non lu).
- Hoyng P., Ossendrijver M. A. J. H., Schmitt D. (2001). The geodynamo as a bistable oscillator. *GAFD* 94,
  263-314. doi:10.1080/03091920108203410.
- Stefani F., Xu M., Sorriso-Valvo L., Gerbeth G., Günther U. (2007). Oscillation or rotation: a comparison of two
  simple reversal models. *GAFD* 101, 227-248. doi:10.1080/03091920701523311.
- Pétrélis F., Fauve S. (2008). Chaotic dynamics of the magnetic field generated by dynamo action in a turbulent
  flow. *J. Phys.: Condens. Matter* 20, 494203. doi:10.1088/0953-8984/20/49/494203.
- Pétrélis F., Fauve S., Dormy E., Valet J.-P. (2009). *PRL* 102, 144503 `[site Dy:260-287]`.
- Gissinger C. (2012). A new deterministic model for chaotic reversals. *Eur. Phys. J. B* 85, 137.
  doi:10.1140/epjb/e2012-20799-5.
- Brunton S. L., Proctor J. L., Kutz J. N. (2016). Discovering governing equations from data by sparse
  identification of nonlinear dynamical systems. *PNAS* 113(15), 3932-3937. doi:10.1073/pnas.1517384113.
- Loiseau J.-C., Brunton S. L. (2018). Constrained sparse Galerkin regression. *J. Fluid Mech.* 838, 42-67.
  doi:10.1017/jfm.2017.823.
- Guseva A., Skene C., Tobias S. M. (2026). arXiv:2603.29079 (préprint).
- Gwirtz K., Davis T., Morzfeld M., Constable C., Fournier A., Hulot G. (2022). Can machine learning reveal
  precursors of reversals of the geomagnetic axial dipole field? *GJI* 231(1), 520-535. doi:10.1093/gji/ggac195.

*Statistique des inversions (D5)*
- Brunhes B. (1906). *J. Phys. Théor. Appl.* 5, 705-724. doi:10.1051/jphystap:019060050070500.
- Matuyama M. (1929). *Proc. Imperial Acad.* 5(5), 203-205. doi:10.2183/pjab1912.5.203.
- Vine F. J., Matthews D. H. (1963). Magnetic anomalies over oceanic ridges. *Nature* 199, 947-949.
  doi:10.1038/199947a0.
- Cox A., Doell R. R., Dalrymple G. B. (1964). Reversals of the Earth's magnetic field. *Science* 144, 1537-1543.
  doi:10.1126/science.144.3626.1537.
- Cox A. (1968). Lengths of geomagnetic polarity intervals. *JGR* 73, 3247-3260. doi:10.1029/JB073i010p03247.
- Cande S. C., Kent D. V. (1995). *JGR* 100, 6093-6095. doi:10.1029/94JB03098.
- Constable C. (2000). On rates of occurrence of geomagnetic reversals. *PEPI* 118, 181-193.
  doi:10.1016/S0031-9201(99)00139-9.
- Carbone V. et al. (2006). Clustering of polarity reversals of the geomagnetic field. *PRL* 96, 128501.
  doi:10.1103/PhysRevLett.96.128501.
- Valet J.-P., Fournier A. (2016). Deciphering records of geomagnetic reversals. *Rev. Geophys.* 54, 410-446.
  doi:10.1002/2015RG000506.
- Singer B. S., Jicha B. R., Mochizuki N., Coe R. S. (2019). *Sci. Adv.* 5, eaaw4621.

### 6.4 Apprentissage

*A1*
- Raissi M., Perdikaris P., Karniadakis G. E. (2019). Physics-informed neural networks. *J. Comput. Phys.* 378,
  686-707. doi:10.1016/j.jcp.2018.10.045.
- Lu L., Jin P., Pang G., Zhang Z., Karniadakis G. E. (2021). DeepONet. *Nat. Mach. Intell.* 3, 218-229.
  doi:10.1038/s42256-021-00302-5.
- Li Z. et al. (2021). Fourier neural operator for parametric partial differential equations. *ICLR 2021*.
  arXiv:2010.08895.
- Kovachki N. et al. (2023). Neural operator. *JMLR* 24(89). arXiv:2108.08481.
- Kochkov D. et al. (2021). *PNAS* 118(21), e2101784118. doi:10.1073/pnas.2101784118.
- McCabe M. et al. (2024). Multiple physics pretraining. *NeurIPS 37*. arXiv:2310.02994.
- Herde M. et al. (2024). Poseidon. *NeurIPS 37*. arXiv:2405.19101.
- Takamoto M. et al. (2022). PDEBench. arXiv:2210.07182.
- Ohana R. et al. (2024). The Well. *NeurIPS 37*. doi:10.52202/079017-1430.
- Duraisamy K., Iaccarino G., Xiao H. (2019). *Annu. Rev. Fluid Mech.* 51, 357-377.
  doi:10.1146/annurev-fluid-010518-040547.
- Brunton S. L., Noack B. R., Koumoutsakos P. (2020). *Annu. Rev. Fluid Mech.* 52, 477-508.
  doi:10.1146/annurev-fluid-010719-060214.
- Beck A., Flad D., Munz C.-D. (2019). *J. Comput. Phys.* 398, 108910. doi:10.1016/j.jcp.2019.108910.
- Maulik R., San O., Rasheed A., Vedula P. (2019). *J. Fluid Mech.* 858, 122-144. doi:10.1017/jfm.2018.770.
- Guan Y., Subel A., Chattopadhyay A., Hassanzadeh P. (2023). *Physica D* 443, 133568.
  doi:10.1016/j.physd.2022.133568.
- Mohan A. T., Lubbers N., Chertkov M., Livescu D. (2023). Embedding hard physical constraints in neural network
  coarse-graining of three-dimensional turbulence. *Phys. Rev. Fluids* 8, 014604.
  doi:10.1103/PhysRevFluids.8.014604 ; arXiv:2002.00021.
- Rosofsky S. G., Huerta E. A. (2023). *Mach. Learn.: Sci. Technol.* 4, 035002. doi:10.1088/2632-2153/ace30a.
- Kacmaz S., Huerta E. A., Haas R. (2025). Resolving turbulent magnetohydrodynamics: A hybrid operator-diffusion
  framework. *Mach. Learn.: Sci. Technol.* 6, 035057. doi:10.1088/2632-2153/ae054c.
- Duarte R., Nemmen R., Santos-Lima R. (2025). arXiv:2507.01388 (préprint).
- Gopakumar V. et al. (2024). *Nucl. Fusion* 64, 056025. doi:10.1088/1741-4326/ad313a.
- Jarolim R., Thalmann J. K., Veronig A. M., Podladchikova T. (2023). *Nature Astron.* 7, 1171-1179.
  doi:10.1038/s41550-023-02030-9.
- Kaptanoglu A. A., Morgan K. D., Hansen C. J., Brunton S. L. (2021). *PRE* 104, 015206.
  doi:10.1103/PhysRevE.104.015206.
- Scheinker A. (2026). Round-trip consistency: bidirectional diffusion models can predict their own rollout
  errors. arXiv:2608.00675 (préprint).
- Nauman F., Nättilä J. (2019). *A&A* 629, A89. doi:10.1051/0004-6361/201935945.
- Illarionov E., Kisielius V., Stepanov R., Kuzanyan K. (2026). *PRE* 113, L053202. doi:10.1103/dpsp-bwkh.
- Yang R., Schmid P. J. (2025). Complex-network modeling of reversal events in two-dimensional turbulent thermal
  convection. *J. Fluid Mech.* 1011, A30. doi:10.1017/jfm.2025.371.
- Pathak J. et al. (2018). *PRL* 120, 024102. doi:10.1103/PhysRevLett.120.024102.
- Qi D., Majda A. J. (2020). *PNAS* 117(1), 52-59. doi:10.1073/pnas.1917285117.
- Lucente D., Rolland J., Herbert C., Bouchet F. (2022). *J. Stat. Mech.* 083201. doi:10.1088/1742-5468/ac7aa7.
- Yang Y., Nurbekyan L., Negrini E., Martin R., Pasha M. (2023). *SIAM J. Appl. Dyn. Syst.* 22(1), 269-310.
  doi:10.1137/21M1421337.
- Botvinick-Greenhouse J., Martin R., Yang Y. (2023). *Chaos* 33, 063152. doi:10.1063/5.0149673.
- Jiang R., Lu P. Y., Orlova E., Willett R. (2023). *NeurIPS 2023*. arXiv:2306.01187.
- Schiff Y. et al. (2024). DySLIM. *ICML 2024*, PMLR 235 `[site T:1214]`.
- Chen Y., Das S., Guo W., Zhong X. (2026). *Physica D* 496, 135326. doi:10.1016/j.physd.2026.135326.
- Fournier A. et al. (2010). An introduction to data assimilation and predictability in geomagnetism. *Space Sci.
  Rev.* 155, 247-291. doi:10.1007/s11214-010-9669-4.

*A2*
- Goodfellow I. J. et al. (2014). Generative adversarial nets. *NIPS 27*. arXiv:1406.2661.
- Xie Y., Franz E., Chu M., Thuerey N. (2018). tempoGAN. *ACM Trans. Graph.* 37(4), 95.
  doi:10.1145/3197517.3201304.
- Kim H., Kim J., Won S., Lee C. (2021). *J. Fluid Mech.* 910, A29. doi:10.1017/jfm.2020.1028.
- Wu J.-L. et al. (2020). Enforcing statistical constraints in generative adversarial networks for modeling
  chaotic dynamical systems. *J. Comput. Phys.* 406, 109209. doi:10.1016/j.jcp.2019.109209.
- Ho J., Jain A., Abbeel P. (2020). DDPM. *NeurIPS 2020*. arXiv:2006.11239.
- Song Y. et al. (2021). Score-based generative modeling through SDEs. *ICLR 2021*. arXiv:2011.13456.
- Karras T. et al. (2022). EDM. *NeurIPS 2022*. arXiv:2206.00364.
- Ho J., Salimans T. (2022). Classifier-free diffusion guidance. arXiv:2207.12598.
- Lipman Y. et al. (2023). Flow matching for generative modeling. *ICLR 2023*. arXiv:2210.02747.
- Liu X., Gong C., Liu Q. (2023). Rectified flow. *ICLR 2023*. arXiv:2209.03003.
- Albergo M. S., Vanden-Eijnden E. (2023). *ICLR 2023*. arXiv:2209.15571 ; Albergo, Boffi, Vanden-Eijnden (2025).
  *JMLR* 26(209). arXiv:2303.08797.
- Tong A. et al. (2024). OT-CFM. *TMLR*. arXiv:2302.00482.
- Kerrigan G., Migliorini G., Smyth P. (2024). Functional flow matching. *AISTATS 2024*. arXiv:2305.17209.
- Lim J. H. et al. (2025). Score-based diffusion models in function space. *JMLR* 26(158). arXiv:2302.07400.
- Shu D., Li Z., Barati Farimani A. (2023). *J. Comput. Phys.* 478, 111972. doi:10.1016/j.jcp.2023.111972.
- Lienen M., Lüdke D., Hansen-Palmus J., Günnemann S. (2024). From zero to turbulence (TurbDiff). *ICLR 2024*.
  arXiv:2306.01776.
- Kohl G., Chen L.-W., Thuerey N. (2026). ACDM. *Neural Networks* 199, 108641. doi:10.1016/j.neunet.2026.108641.
- Du P., Parikh M. H., Fan X., Liu X.-Y., Wang J.-X. (2024). CoNFiLD. *Nat. Commun.* 15, 10416.
  doi:10.1038/s41467-024-54712-1.
- Raonić B. et al. (2026). Generative AI for efficient statistical computation of fluids (GenCFD). *Nat. Commun.*
  17, 9846. doi:10.1038/s41467-026-76390-x ; prépublication arXiv:2409.18359 (Molinaro R., Lanthaler S., Raonić B.
  et al., titre « Generative AI for fast and accurate statistical computation of fluids ») : c'est son résumé, pas
  le résumé publié, qui contient « regress to the mean flow ».
- Galletti G. et al. (2026). A shortcut to statistically steady-state turbulence with flow matching.
  arXiv:2607.13022 (préprint).
- Wang S., Dou Z., Shan S., Liu T.-R., Lu L. (2026). FunDiff. *Nat. Commun.* 17, 5749.
  doi:10.1038/s41467-026-72292-0.
- Finzi M., Boral A., Wilson A. G., Sha F., Zepeda-Núñez L. (2023). *ICML 2023*. arXiv:2306.07526.
- Li L. et al. (2024). SEEDS. *Sci. Adv.* 10, eadk4489. doi:10.1126/sciadv.adk4489.
- Price I. et al. (2025). GenCast. *Nature* 637, 84-90. doi:10.1038/s41586-024-08252-9.
- Mardani M. et al. (2025). CorrDiff. *Commun. Earth Environ.* 6, 124. doi:10.1038/s43247-025-02042-5.
- da Silva D. E., Kirk M., Mathews N., Muñoz-Jaramillo A. (2025). arXiv:2510.01441 (préprint).
- Martin J., Lübke J., Li T., Buzzicotti M., Grauer R., Biferale L. (2025). *ApJS* 277(2), 48.
  doi:10.3847/1538-4365/adb432 ; arXiv:2412.12923.
- Biferale L., Buzzicotti M. (2026). Generative AI in turbulence. arXiv:2610.35123 (préprint).

*A3*
- Richter-Powell J., Lipman Y., Chen R. T. Q. (2022). Neural conservation laws. *NeurIPS 35*.
  doi:10.52202/068431-2759.
- Li T., Buzzicotti M., Bonaccorso F., Biferale L. (2026). Physics-constrained diffusion model for synthesis of 3D
  turbulent data (PCDM). arXiv:2603.12834 (préprint).
- Li X. et al. (2026). Project and generate. arXiv:2603.24500 (préprint).
- Négiar G., Mahoney M. W., Krishnapriyan A. S. (2023). *ICLR 2023*. arXiv:2207.08675.
- Hansen D. et al. (2024). ProbConserv. *Physica D* 457, 133952. doi:10.1016/j.physd.2023.133952.
- Christopher J. K., Baek S., Fioretto F. (2024). *NeurIPS 37*. doi:10.52202/079017-2834.
- Liu G.-H., Chen T., Theodorou E., Tao M. (2023). *NeurIPS 36*. doi:10.52202/075280-1858.
- Fishman N. et al. (2023). *TMLR*. arXiv:2304.05364.
- Cheng C. et al. (2025). ECI. *ICLR 2025*. arXiv:2412.01786.
- Utkarsh U. et al. (2025). PCFM. *NeurIPS 38*. doi:10.52202/085713-5354.
- Bastek J.-H., Sun W., Kochmann D. M. (2025). Physics-informed diffusion models. *ICLR 2025*. arXiv:2403.14404.
- Huang J. et al. (2024). DiffusionPDE. *NeurIPS 37*. doi:10.52202/079017-4140.
- Jacobsen C., Zhuang Y., Duraisamy K. (2025). CoCoGen. *SIAM J. Sci. Comput.* 47(2), C399-C425.
  doi:10.1137/24M1636071.
- Chung H. et al. (2023). DPS. *ICLR 2023*. arXiv:2209.14687 ; Bansal A. et al. (2024). *ICLR 2024*.
  arXiv:2302.07121 ; Ben-Hamu H. et al. (2024). D-Flow. *ICML 2024*. arXiv:2402.14017 ; Gallon D. et al. (2026).
  arXiv:2602.09708 (préprint).
- **Baldan G., Liu Q., Guardone A., Thuerey N. (2026). Physics vs distributions: Pareto optimal flow matching with
  physics constraints (PBFM). *ICLR 2026*. arXiv:2506.08604** (résumé relu le 8 novembre 2026).
- Genuist W., Savin É., Gatti F., Clouteau D. (2026). Divergence-free diffusion models for incompressible fluid
  flows. arXiv:2601.19368 (préprint) ; (2025) arXiv:2505.24145 (préprint).
- Khalifa M., Elsahar H., Dymetman M. (2021). *ICLR 2021*. arXiv:2012.11635.
- Khalafi S., Ding D., Ribeiro A. (2024). Constrained diffusion models via dual training. *NeurIPS 37*.
  doi:10.52202/079017-0836.
- Mun J. (2026). arXiv:2608.30096 (préprint).
- Tauberschmidt J., Fellenz S., Vollmer S. J., Duncan A. B. (2026). Physics-constrained fine-tuning of
  flow-matching models. *ICLR 2026*. arXiv:2508.09156.
- Cai Z., Cao Y., Huang Y., Zhou X. (2026). Weak generative sampler. *SIAM J. Sci. Comput.* 48(4), C708-C735.
  doi:10.1137/24M1665271.
- Zang Y., Bao G., Ye X., Zhou H. (2020). Weak adversarial networks. *J. Comput. Phys.* 411, 109409.
  doi:10.1016/j.jcp.2020.109409.
- Köhler J., Klein L., Noé F. (2020). Equivariant flows. *ICML 2020*, PMLR 119, 5361-5370. arXiv:2006.02425.
- Klein L., Krämer A., Noé F. (2023). Equivariant flow matching. *NeurIPS 36*. doi:10.52202/075280-2617.
- Hoogeboom E., Garcia Satorras V., Vignac C., Welling M. (2022). *ICML 2022*. arXiv:2203.17003.
- Wang R., Walters R., Yu R. (2021). *ICLR 2021*. arXiv:2002.03061.
- Ancrages classiques vérifiés par le site, non revérifiés le 8 novembre 2026 : Csiszár 1975 ; Jaynes 1957 ;
  Pitera et Chodera 2012 ; Echeverría 1982 ; Ethier et Kurtz 1986 ; Rice 1944, 1945 ; Azaïs et Wschebor 2009
  `[site T:1128-1238]`.

*A4*
- Amendola M. et al. (2021). *ICCS 2021, LNCS*, 373-386. doi:10.1007/978-3-030-77977-1_30.
- Peyron M. et al. (2021). *QJRMS* 147, 3759-3777. doi:10.1002/qj.4153.
- Rozet F., Louppe G. (2023). Score-based data assimilation. *NeurIPS 36*. doi:10.52202/075280-1763.
- Rozet F., Andry G., Lanusse F., Louppe G. (2024). *NeurIPS 37*. doi:10.52202/079017-2783.
- Huang L. et al. (2024). DiffDA. *ICML 2024*. arXiv:2401.05932.
- Bao F., Zhang Z., Zhang G. (2024). An ensemble score filter. *CMAME* 432, 117447. doi:10.1016/j.cma.2024.117447.
- Si P., Chen P. (2024). Latent-EnSF. arXiv:2409.00127 (préprint).
- Manshausen P. et al. (2024). arXiv:2406.16947 (préprint).

### 6.5 Encadrants et consortium

*Projet MilaDy et consortium*
- Bousquet R., Ponty Y., Botez V., Plihon N., Nore C. (2026). Magnetic field reversals in numerical simulations
  of the von Kármán sodium experiment. *Phys. Rev. Fluids* 11(6), 063703. doi:10.1103/9tx2-1m13 (DOI revérifié le
  8 novembre 2026).
- Botez V., Giesecke A., Nore C., Cappanera L., Stefani F. (2026). Impact of boundary conditions on onset and
  symmetry of precession-driven dynamos. *Phys. Rev. Fluids* 11(8), 083701. doi:10.1103/rx1h-5zxp (DOI revérifié).
- Barré J., Horii H. (2026). hal-05796131 (prépublication HAL).
- Bousquet R., Nore C., Lucor D. (2025). AutoEncoders latent space interpretability in the light of proper
  orthogonal decomposition. *Comput. Phys. Commun.* 315, 109728. doi:10.1016/j.cpc.2025.109728.
- Bousquet R., Chaffard O., Creff M., Lucor D., Nore C. (2024). Large scale analysis of three-dimensional turbulent
  von Kármán swirling flows. *Phys. Fluids* 36, 105133. doi:10.1063/5.0227495.
- Botez V., Bousquet R., Nore C. (2025). *Magnetohydrodynamics* 61(1/2), 13-24. doi:10.22364/mhd.61.1-2.2.
- Bousquet R., Faucheu A., Dumas L., Nore C., Lucor D. (2026). Research Square. doi:10.21203/rs.3.rs-10008570/v1
  (préprint).
- Bousquet R., Nore C. (2026). Poster, Rencontres du Non-Linéaire, https://rnl2026.sciencesconf.org/712616.

*C. Nore*
- Nore C., Brachet M. E., Politano H., Pouquet A. (1997). Dynamo action in the Taylor–Green vortex near threshold.
  *Phys. Plasmas* 4, 1-3. doi:10.1063/1.872578.
- Nore C., Tuckerman L. S., Daube O., Xin S. (2003). *J. Fluid Mech.* 477, 51-88. doi:10.1017/S0022112002003075 ;
  Nore C., Tartar M., Daube O., Tuckerman L. S. (2004). *J. Fluid Mech.* 511, 45-65.
  doi:10.1017/S0022112004008559 ; Nore C., Moisy F., Quartier L. (2005). Experimental observation of
  near-heteroclinic cycles in the von Kármán swirling flow. *Phys. Fluids* 17, 064103. doi:10.1063/1.1926827.
- Guermond J.-L., Laguerre R., Léorat J., Nore C. (2007). *J. Comput. Phys.* 221, 349-369.
  doi:10.1016/j.jcp.2006.06.045 ; (2009) *J. Comput. Phys.* 228, 2739-2757. doi:10.1016/j.jcp.2008.12.026.
- Guermond J.-L., Léorat J., Luddens F., Nore C., Ribeiro A. (2011). *J. Comput. Phys.* 230, 6299-6319.
  doi:10.1016/j.jcp.2011.04.026.
- Laguerre R. et al. (2008). Impact of impellers on the axisymmetric magnetic mode in the VKS2 dynamo
  experiment. *PRL* 101, 104501. doi:10.1103/PhysRevLett.101.104501.
- Giesecke A. et al. (2012). Influence of high-permeability discs in an axisymmetric model of the Cadarache
  dynamo experiment. *New J. Phys.* 14, 053005. doi:10.1088/1367-2630/14/5/053005.
- Nore C., Léorat J., Guermond J.-L., Giesecke A. (2015). *PRE* 91, 013008. doi:10.1103/PhysRevE.91.013008.
- Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2016). Direct numerical simulation of the axial
  dipolar dynamo in the Von Kármán Sodium experiment. *EPL* 114, 65002. doi:10.1209/0295-5075/114/65002.
- Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2018). Numerical simulation of the von Kármán sodium
  dynamo experiment. *J. Fluid Mech.* 854, 164-195. doi:10.1017/jfm.2018.582.
- Creff M., Faller H., Dubrulle B., Guermond J.-L., Nore C. (2024). Tracking dynamo mechanisms from local energy
  transfers. *Phys. Plasmas* 31, 022306. doi:10.1063/5.0174251.
- Nore C., Léorat J., Guermond J.-L., Luddens F. (2011). Nonlinear dynamo action in a precessing cylindrical
  container. *PRE* 84, 016317. doi:10.1103/PhysRevE.84.016317.
- Stefani F. et al. (2015). Towards a precession driven dynamo experiment. *Magnetohydrodynamics* 51(2), 275-284.
  doi:10.22364/mhd.51.2.11.
- Cappanera L., Guermond J.-L., Léorat J., Nore C. (2016). Two spinning ways for precession dynamo. *PRE* 93,
  043113. doi:10.1103/PhysRevE.93.043113.
- Nore C., Guermond J.-L., Laguerre R., Léorat J., Luddens F. (2012). Nonlinear dynamo in a short Taylor–Couette
  setup. *Phys. Fluids* 24, 094106. doi:10.1063/1.4752756.
- Jackson A. et al. (2014). A spherical shell numerical dynamo benchmark with pseudo-vacuum magnetic boundary
  conditions. *GJI* 196(2), 712-723. doi:10.1093/gji/ggt425.
- Quattromini M. (2024). Thèse, tel-04964013.

*Y. Ponty*
- Ponty Y., Gilbert A. D., Soward A. M. (2001). *J. Fluid Mech.* 435, 261-287. doi:10.1017/S0022112001003755.
- Ponty Y., Politano H., Pinton J.-F. (2004). *PRL* 92, 144503. doi:10.1103/PhysRevLett.92.144503.
- Ponty Y., Mininni P. D., Montgomery D. C., Pinton J.-F., Politano H., Pouquet A. (2005). Numerical study of
  dynamo action at low magnetic Prandtl numbers. *PRL* 94, 164502. doi:10.1103/PhysRevLett.94.164502 ;
  arXiv:physics/0410046.
- Mininni P. D. et al. (2005). Dynamo regimes with a nonhelical forcing. *ApJ* 626, 853-863. doi:10.1086/429911.
- Ponty Y., Mininni P. D., Pinton J.-F., Politano H., Pouquet A. (2007). *New J. Phys.* 9, 296.
  doi:10.1088/1367-2630/9/8/296.
- Ponty Y., Laval J.-P., Dubrulle B., Daviaud F., Pinton J.-F. (2007). Subcritical dynamo bifurcation in the
  Taylor-Green flow. *PRL* 99, 224501. doi:10.1103/PhysRevLett.99.224501.
- Homann H., Ponty Y., Krstulovic G., Grauer R. (2014). *New J. Phys.* 16, 075014.
  doi:10.1088/1367-2630/16/7/075014.
- Alexakis A., Ponty Y. (2008). Effect of the Lorentz force on on-off dynamo intermittency. *PRE* 77, 056308.
  doi:10.1103/PhysRevE.77.056308.
- Ponty Y., Plunian F. (2011). Transition from large-scale to small-scale dynamo. *PRL* 106, 154502.
  doi:10.1103/PhysRevLett.106.154502.
- Mannix P. M., Ponty Y., Marcotte F. (2022). Systematic route to subcritical dynamo branches. *PRL* 129, 024502.
  doi:10.1103/PhysRevLett.129.024502.
- Ponty Y., Politano H., Pouquet A. (2025). *J. Plasma Phys.* 91(2), E69. doi:10.1017/S0022377825000169.
- Baerenzung J., Politano H., Ponty Y., Pouquet A. (2008). *PRE* 78, 026310. doi:10.1103/PhysRevE.78.026310.
- Kreuzahler S., Schulz D., Homann H., Ponty Y., Grauer R. (2014). *New J. Phys.* 16, 103001.
  doi:10.1088/1367-2630/16/10/103001.
- Kreuzahler S., Ponty Y., Plihon N., Homann H., Grauer R. (2017). Dynamo enhancement and mode selection
  triggered by high magnetic permeability. *PRL* 119, 234501. doi:10.1103/PhysRevLett.119.234501 ;
  arXiv:1706.00260.

*D. Lucor*
- Xiu D., Lucor D., Su C.-H., Karniadakis G. E. (2002). *J. Fluids Eng.* 124(1), 51-59. doi:10.1115/1.1436089.
- Lucor D., Su C.-H., Karniadakis G. E. (2004). *IJNME* 60(3), 571-596. doi:10.1002/nme.976.
- Lucor D., Karniadakis G. E. (2004). *PRL* 92, 154501. doi:10.1103/PhysRevLett.92.154501.
- Lucor D., Meyers J., Sagaut P. (2007). *J. Fluid Mech.* 585, 255-279. doi:10.1017/S0022112007006751.
- El Garroussi S. et al. (2022). *SERRA* 36(3), 693-718. doi:10.1007/s00477-021-02060-7.
- Nony B. X., Rochoux M. C., Jaravel T., Lucor D. (2023). *SERRA* 37(6), 2117-2144.
  doi:10.1007/s00477-023-02383-7.
- Lucor D., Agrawal A., Sergent A. (2022). *J. Comput. Phys.* 456, 111022. doi:10.1016/j.jcp.2022.111022 ;
  arXiv:2103.03565.
- Cai J., Angeli P.-E., Martinez J.-M., Damblin G., Lucor D. (2024). *Comput. Fluids* 275, 106246.
  doi:10.1016/j.compfluid.2024.106246.
- Volk M.-C. et al. (2025). *ICHMT* 167, 109284. doi:10.1016/j.icheatmasstransfer.2025.109284.
- Jaber E. et al. (2025). *JMLMC* 6(3), 37-68. doi:10.1615/JMachLearnModelComput.2025054687.
- Zhou H., Wang Z., Lucor D., Sauret E. (2026). *RESS* 274, 112359. doi:10.1016/j.ress.2026.112359.

*S. Cheng*
- Cheng S., Argaud J.-P., Iooss B., Lucor D., Ponçot A. (2019). *SERRA* 33, 2033-2051.
  doi:10.1007/s00477-019-01743-6 ; (2021) *SERRA* 35, 1019-1038. doi:10.1007/s00477-020-01933-7 ; Cheng et al.
  (2021) *Math. Geosci.* 53, 1751-1780. doi:10.1007/s11004-021-09951-z.
- Cheng S., Lucor D., Argaud J.-P. (2021). *J. Comput. Sci.* 53, 101405. doi:10.1016/j.jocs.2021.101405.
- Cheng S. et al. (2022). *J. Comput. Phys.* 464, 111302. doi:10.1016/j.jcp.2022.111302.
- Cheng S. et al. (2023, en ligne 2022). Generalised latent assimilation in heterogeneous reduced spaces. *J. Sci.
  Comput.* 94(1), 11. doi:10.1007/s10915-022-02059-4.
- Cheng S. et al. (2024). Multi-domain encoder–decoder neural networks for latent data assimilation. *CMAME* 430,
  117201. doi:10.1016/j.cma.2024.117201.
- Wang K. et al. (2025). *QJRMS* 151, e5009. doi:10.1002/qj.5009.
- Lin Z. et al. (2026). *JAMES* 18(7), e2026MS005767. doi:10.1029/2026MS005767.
- Cheng S., Min J., Liu C., Arcucci R. (2025). TorchDA. *Comput. Phys. Commun.* 306, 109359.
  doi:10.1016/j.cpc.2024.109359.
- Cheng S., Liu C., Guo Y., Arcucci R. (2024). VIVID. *J. Comput. Phys.* 496, 112581.
  doi:10.1016/j.jcp.2023.112581.
- Zhou H., Cheng S., Arcucci R. (2024). *CMAME* 420, 116758. doi:10.1016/j.cma.2024.116758.
- Cheng S. et al. (2025). Machine learning for modelling unstructured grid data in computational physics: A
  review. *Inf. Fusion* 123, 103255. doi:10.1016/j.inffus.2025.103255.
- Cheng S., Guo Y., Arcucci R. (2023). A generative model for surrogates of spatial-temporal wildfire nowcasting.
  *IEEE TETCI* 7(5), 1420-1430. doi:10.1109/TETCI.2023.3298535.
- Zhuang Y., Cheng S., Duraisamy K. (2025). Spatially-aware diffusion models with cross-attention for global field
  reconstruction with sparse observations. *CMAME* 435, 117623. doi:10.1016/j.cma.2024.117623.
- Yu W., Ghosh A., Finn T. S., Arcucci R., Bocquet M., Cheng S. (2026). *Geosci. Model Dev.* 19(2), 1027-1054.
  doi:10.5194/gmd-19-1027-2026.
- Cheng X. et al. (2025). Learning chaos in a linear way. *ICLR 2025*. arXiv:2503.14702.
- Cheng X., Yuan W., Yang Y., Zhang Y., Cheng S., He Y., Sun Z. (2026). Information shapes Koopman
  representation. *ICLR 2026* (commentaire arXiv). arXiv:2510.13025.
- Xue X. et al. (2026). *Nat. Commun.* 17, 9243. doi:10.1038/s41467-026-75730-1.
- Bocquet M., Finn T. S., Cheng S. (2026). arXiv:2610.17333 (préprint).
- Cheng S. et al. (17 auteurs, dont D. Lucor) (2023). Machine learning with data assimilation and uncertainty
  quantification for dynamical systems: A review. *IEEE/CAA J. Autom. Sinica* 10(6), 1361-1387.
  doi:10.1109/JAS.2023.123537.
- Cheng S. (2020). Thèse, Université Paris-Saclay, tel-03117151.

### 6.6 Pages web et API consultées le 8 novembre 2026

- ANR : https://anr.fr/Projet-ANR-25-CE51-0077
- Offre de stage 2027 : https://scheng2024.github.io/stage_milady_2027.pdf ; offre de stage 2026 :
  https://stages.phys.ens.psl.eu/OffresPDF/Offre-30818.pdf ; offre de post-doctorat LISN :
  https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf
- S. Cheng : https://scheng2024.github.io/ (pages research, publications, opportunities, cv).
- D. Lucor : https://perso.lisn.upsaclay.fr/lucor/ (people, publications, opportunities).
- Y. Ponty, CV 2026 : https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf
- C. Nore, résumé de séminaire : https://www.ladhyx.polytechnique.fr/media/evenement/180118_CarolineNore.pdf ;
  poster RNL 2026 : https://rnl2026.sciencesconf.org/712616
- SFEMaNS : https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html
- Texte intégral de Bousquet et al. (2026) : https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf
- Constable (2001, prépublication) :
  https://igpppublic.ucsd.edu/~cathy/Publications/Preprints/geomag_reversals_preprint.pdf
- API : api.crossref.org, export.arxiv.org, api.openalex.org, api.archives-ouvertes.fr.
- Offre de stage 2027 relue le 8 novembre 2026 (texte extrait du PDF) ; HAL : dates de dépôt des trois notices
  MilaDy ; OpenReview : acceptation de PBFM et de Tauberschmidt et al. à ICLR 2026.

---

## Non vérifié

Contrôle adverse des citations et des attributions du 8 novembre 2026 (journal des corrections :
`video/plan/soa/ (copies de travail non versionnées pour dl/ et work/) check_soa.md`). Les points
ci-dessous n'ont pas pu être confirmés dans une source primaire lue ce jour ; ils reposent sur le site ou sur une
source secondaire, et ne doivent pas être montrés à l'écran sans nouvelle lecture.

- Glatzmaier et Roberts (1995) : le mot « anélastique » (Tobias) et le contenu de l'article *Nature* ; le texte
  des deux articles de 1995 n'a pas été lu.
- Christensen et al. (2001) : statut de « premier » benchmark et définition des cas (aucun résumé disponible).
- Lucor, Agrawal et Sergent (2022) : la relaxation de l'incompressibilité vient du résumé de la prépublication
  arXiv:2103.03565 (titre différent) ; le résumé de la version *J. Comput. Phys.* n'est pas disponible.
- Nony et al. (2023) : « POD et processus gaussiens » (titre seul lu ; aucun résumé disponible).
- Kohl et al. (2026, ACDM) : le conditionnement « par Re et Mach » n'est pas écrit dans le résumé, qui parle de
  paramètres d'écoulement hors du domaine d'entraînement, en 2D.
- Chiffres repris du site sans relecture du texte intégral ce jour : Kacmaz et al. (128², Pm = 1), PCDM (64³,
  « machine precision »), Weak Generative Sampler (dimension 100), Nore et al. 2018 (Rm_c ≈ 70 ; le résumé dit
  seulement que Rm_c tend vers une constante), Genuist et al. 2026 (six variantes).
- Absences tirées de résumés (« sans contrainte physique » pour Galletti et al., TurbDiff, CoNFiLD, GenCast) :
  un résumé muet ne prouve pas l'absence dans l'article.
- Botez et al. (2026) : texte intégral non lu (PDF bloqué) ; seules les affirmations du résumé sont reprises.
- État de DRESDYN en 2026 (dernière source lue : « being set up », avril 2025).
