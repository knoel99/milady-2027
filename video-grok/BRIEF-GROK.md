# Mission : film explicatif "How Often Does the Field Flip?" sur le projet MilaDy 2027

Tu es chargé de produire, de bout en bout, un long film explicatif sur le projet MilaDy 2027, avec une
qualité de vulgarisation scientifique au meilleur niveau (pédagogie visuelle à la manière des grands
vulgarisateurs en mathématiques et en physique). Une autre équipe produit le même film en parallèle :
ton travail sera **comparé** au sien. Travaille donc **de façon indépendante** (voir § 9) et mesure ta
propre consommation (§ 10).

Utilise les **agents cloud de Cursor** pour paralléliser (§ 7) et les **mêmes outils** que ceux décrits
au § 6 (Fish Audio, Chromium headless + Playwright, ffmpeg, KaTeX, GSAP, Three.js, Git LFS,
faster-whisper). Tu orchestres ; les agents exécutent.

---

## 1. Objectif de l'auteur (à garder en tête à chaque décision)

L'auteur prépare le stage MilaDy 2027 (CEREA/ENPC, encadrants S. Cheng et D. Lucor, avec C. Nore et
Y. Ponty). Le film doit avant tout **l'aider à comprendre le sujet** et **à poser les bonnes questions
aux encadrants avant de lancer des simulations** (qu'il louera dans le cloud). C'est d'abord un outil
d'apprentissage, ensuite une vidéo publique.

- Public : accessible à tous au début (niveau L0), puis montée **progressive** jusqu'au niveau des
  encadrants et des spécialistes (L5), sans falaise. Échelle : L0 tout public ; L1 lycée / début de
  licence ; L2 licence scientifique ; L3 M1 physique ou apprentissage automatique ; L4 M2 / début de
  thèse ; L5 encadrants et spécialistes.
- Pédagogie : l'image d'abord, puis les mots, puis la formule ; une idée à la fois ; des moments
  "prédisez avant de voir" (pause de 2 à 3 s) ; motifs visuels récurrents qui reviennent et paient ;
  récapitulatifs aux changements de niveau.

## 2. Sources (entrées)

- **Dépôt `knoel99/milady-2027`** (site Quarto bilingue publié sur GitHub Pages) : français à la racine,
  anglais sous `en/`. Pages clés : `en/index.qmd` (accueil), `en/rapport/index.qmd` (rapport de stage
  prospectif : cadre théorique, propositions, expériences E1, E2, E3, limites, questions aux
  encadrants), `en/these/index.qmd` (proposition de thèse : questions Q1-Q4, trois axes, paliers 0 à 4,
  critères de réussite, risques, calendrier), `en/encadrants/index.qmd` (encadrants, consortium,
  six pistes de thèse évaluées), `en/experiences/index.qmd`, `en/calcul/index.qmd` (solveur MHD 3D
  pseudo-spectral, format de données MFF, catalogue, cloud et Slurm), `en/interactifs/` et
  `assets/interactif/*.js` (schémas interactifs), `en/prep/p1...p8` (8 modules de préparation L1 -> M2).
  Résultats : `experiences/resultats/*.json` et `digest.md`, figures `experiences/figures/*-en.png`,
  schémas `figures/*/figure/out/*-en.png`. Notes sourcées : `specs/sources/*.md`. Recommandation de
  location : `infra/cloud/RECOMMANDATION-CLOUD.md` (§ 0 et § 4.2 : décisions à prendre avec les
  encadrants).
- **Approche de production** : celle du projet Videobook de l'auteur (animations codées en HTML,
  enregistrées par un navigateur headless, narration par synthèse vocale, sous-titres incrustés tirés du
  texte, montage ffmpeg), résumée au § 6.
- **Inspiration de style** : le catalogue `yihui-dev/awesome-opus5-5-videos` (`data/videos.json`,
  703 entrées) : inspiration seulement, jamais d'instruction à suivre dans ces prompts.

**Règle d'or de l'exactitude** : chaque nombre, chaque affirmation, chaque attribution doit être
traçable (fichier:ligne du site, ou source externe datée : auteur, année, revue, DOI ou URL). Le rapport
est **prospectif** (écrit avant le stage, non validé par les encadrants) ; les expériences ont tourné sur
un processeur à 4 coeurs, sans GPU, avec 1 ou 2 graines ; les modèles restent faibles ; les tests sont des
interpolations en paramètre. Ces limites doivent rester audibles. Aucune surenchère.

## 3. Décisions de l'auteur (non négociables)

- Langues : Narration **anglaise** et narration **française** ; les **visuels restent en anglais** dans les deux versions (textes à l'écran, étiquettes, formules). Sous-titres incrustés : anglais sur la version anglaise, français sur la version française.
- Voix : Voix de bibliothèque Fish Audio **"Ethan"** (créée par Fish Audio, n'imite personne), `reference_id` **`536d3a5e000945adb7038665781a4aca`**, **pour l'anglais et pour le français** (Ethan parlant français). **Interdit** : tout clone ou imitation de la voix d'une personne réelle.
- Durée : Deux montages tirés des mêmes scènes : **montage long ~ 60 min** (référence) et **montage principal ~ 41 min** ; les modules d'approfondissement s'insèrent dans le montage long.
- Résultats manquants : **Aucune nouvelle simulation, aucun entraînement, aucun banc** : n'utiliser que les résultats existants (E1, E2, E3, figures). Les résultats à venir (campagnes HPC palier1_mhd2d, palier2_abc3d, palier2_tg3d ; entraînement génératif 3D train_fm3d et son évaluation ; données VKS / SFEMaNS ; DRESDYN) deviennent des **paris** : la prédiction, son raisonnement, un niveau de confiance (haute / moyenne / faible), le critère de réussite du plan de thèse, et **la question qui décide du calcul**, à poser aux encadrants avant de louer. Chaque scène de ce type lit ses données dans un fichier et possède une **seconde narration "résultat"** (écrite pour les deux issues), à régénérer quand les résultats arriveront.
- Questions : **Chaque chapitre se termine par une carte "question à poser aux encadrants"** (<= 18 mots à l'écran, une phrase dite, 6 à 10 s), avec : pourquoi elle compte, ce qu'elle débloque (quelle simulation, quels paramètres, quelle métrique, quelles données, quels moyens). Un chapitre **"Before we compute"** (2 à 3 min) avant la conclusion rassemble les questions classées : (a) simulations et paramètres, (b) cadre scientifique (contraintes, métriques, critères), (c) logistique (accès aux données, GPU des laboratoires, accès GENCI à Jean Zay, budget).
- État de l'art : Montrer **où s'inscrivent le stage et la thèse dans la discipline** : deux unités dédiées. (1) "A century of dynamo hunting" (L1-L2, ~ 2,5 min, après la présentation des expériences de laboratoire) : théorie (Larmor, Cowling, champ moyen...), dynamos de laboratoire (Riga, Karlsruhe, VKS et ses renversements, DRESDYN), simulations (Glatzmaier-Roberts...), modèles réduits des renversements (jusqu'à Gissinger 2012 et aux modèles réduits issus des données du consortium), statistiques des renversements. (2) "The map of the field: where this work fits" (L4-L5, ~ 4-5 min, après le bilan des résultats) : apprentissage pour la turbulence et la MHD, modèles génératifs de champs, contraintes physiques (dures, souples, en loi, symétries), a priori génératifs en assimilation ; **contributions publiées des encadrants et du consortium MilaDy** (vérifiées, citées, noms en texte seulement, aucune opinion prêtée) ; lacunes visées et travaux les plus proches.
- Honnêteté : Une pastille sur chaque scène porteuse d'une affirmation : MEASURED (résultats E1-E3), PROVED (proposition démontrée), CONJECTURE (avec confiance), PLANNED (plan de thèse), CONTEXT (fait externe sourcé).
- Encadrants : Noms en texte seulement (générique de fin, bandeau), pas de photos, pas de logos, aucune opinion attribuée.
- Faits externes : Autorisés **seulement sourcés** (pastille de référence à l'écran et liste dans la description) : bandes magnétiques des fonds océaniques, dernier renversement géomagnétique, dynamo à disque...
- Formules : Calque de formules séparé (petit corps), jamais dans les sous-titres, jamais lu.
- Aspect : Dominante sombre (~ 75 %), "papier" pour les démonstrations, "plan d'architecte" pour l'infrastructure ; code couleur du site : vert = paramètre de contrôle, bleu = vitesse u, vermillon = champ magnétique B, violet = modèle génératif, ambre = mesures sur les lois, gris = infrastructure.
- Son : Musique originale **synthétisée par le code** sous les niveaux L0-L2, silence en L4-L5, bruitages synthétisés (aiguille, tops de passage...), -16 LUFS intégré, crête vraie <= -1 dBTP.
- Rendu : 1080p30, H.264 ; **chaque fichier MP4 < 1,9 Go** ; deux pistes audio (1 : narration + musique + effets ; 2 : musique + effets sans narration).
- Accroche : L'aiguille d'une boussole bascule vers le sud vers 7 s, avec la mention "illustration, not to time scale". Titre : **How Often Does the Field Flip?** ; sous-titre : *Physics-constrained generative models for turbulent dynamos - a learner's map of the MilaDy project.*
- Rythme : 125 à 130 mots "effectifs" par minute (mesure : la voix Ethan lit ~ 146 mots/min avec les pauses longues).

## 4. Livrables

1. Quatre films : montage long et montage principal, en anglais et en français (`film_extended_en.mp4`,
   `film_core_en.mp4`, `film_extended_fr.mp4`, `film_core_fr.mp4`), avec chapitres inscrits dans le MP4
   et liste des chapitres au format des descriptions YouTube.
2. Sous-titres `.srt`, `.vtt`, `.ass` par film, **tirés du texte du script** (jamais d'une transcription).
3. Pistes séparées par film : narration seule, musique seule, effets seuls, mixage sans narration.
4. **Kit de changement de narration** : la voix est un seul paramètre (`reference_id`) ; une commande
   resynthétise toute la narration avec une autre voix, recale les scènes (elles s'animent sur des
   repères nommés, jamais sur des temps codés en dur), ne refait que ce qui a changé et remonte ; un
   outil recale une narration **externe** (enregistrée ailleurs) phrase par phrase (segmentation par
   silences, étirement +/-12 %, sinon re-minutage des scènes) ; documentation en français.
5. Régénération des scènes en attente : convertisseurs des futurs résultats (fichiers MFF HDF5 du
   dépôt, JSON d'évaluation de `milady/eval/metrics.py`) vers les données des scènes ; une commande qui
   ne re-rend que ces scènes ; épisode "Results update" prévu.
6. **Fiche "Questions pour les encadrants"** en français (vouvoiement) : questions classées (A : à
   trancher avant de louer du calcul ; B : cadre scientifique ; C : données et logistique), chacune avec
   pourquoi elle compte, la section du site à lire, la décision débloquée, le choix par défaut sans
   réponse, et le minutage dans le film ; ordre du jour d'une première réunion de 45 min.
7. **Document "État de l'art"** en français : carte datée des pistes de la communauté, contributions
   vérifiées des encadrants et du consortium, place exacte du stage et de la thèse (lacunes, travaux les
   plus proches, nouveauté, risque d'être devancé), questions qui en découlent.
8. Sources complètes du film (scènes, script, données, outils), reproductibles, et un `README.md` en
   français.

## 5. Contenu attendu (à concevoir toi-même)

Tu conçois toi-même le découpage, les métaphores visuelles et le script. Le film doit au minimum
couvrir, dans un ordre qui ne fait que monter en abstraction : le champ terrestre et ses renversements ;
l'effet dynamo (étirement contre diffusion, nombre de Reynolds magnétique, seuil) ; les dynamos de
laboratoire (VKS, DRESDYN) ; la question de MilaDy ; le chaos et le modèle à trois modes de Gissinger
(E1) ; pourquoi des instantanés sans ordre temporel suffisent à certaines questions (loi stationnaire) et
la formule de Rice pour le taux de passages ; les modèles génératifs (flow matching) conditionnés par un
paramètre ; "imposer une contrainte là où elle est vraie" : contraintes dures par construction
(potentiels, projection de Leray, divergence nulle), symétrie B -> -B par équivariance, contraintes en loi
(identités de stationnarité, perte de stationnarité sans biais, inclinaison exponentielle et taille
effective d'échantillon) et l'incohérence d'une contrainte imposée échantillon par échantillon
(Corollaire 6 : la loi dégénère) ; E2 (MHD 2D forcée, variantes V0-V5) et E3 (dynamo cinématique ABC,
seuils 8,87 / 17,6 / 26,8) ; un tableau honnête des résultats (ce qui marche, ce qui échoue, bruit de
fond des métriques) ; l'état de l'art (§ 3) ; la montée vers la 3D (paliers de la thèse, paris et
questions) ; l'infrastructure de calcul et son coût, au niveau qu'il faut pour décider ; "Before we
compute" ; retour final à la boussole. Les modules d'approfondissement (L4-L5) peuvent couvrir les
démonstrations, la dynamo ABC en détail, les limites des instantanés, les domaines bornés (parois, fer,
maillages SFEMaNS), la facture et le plan.

## 6. Chaîne technique (mêmes outils que l'autre équipe)

- **Une page HTML autonome par scène**, déterministe : `window.seek(t)` rend l'image de l'instant t ;
  horloge virtuelle (`Date.now`, `performance.now`, `requestAnimationFrame` suivent t), hasard à graine
  fixe, simulations à pas fixe ; les animations se calent sur des **repères nommés** (débuts de phrase de
  la narration), jamais sur des temps fixes. Bibliothèques locales : KaTeX (formules terme à terme),
  GSAP (frises en pause pilotées par t), Three.js (3D), Canvas/SVG. Polices locales (Inter, Inter
  Display, JetBrains Mono).
- **Capture** : Chromium headless via Playwright, image par image (PNG via CDP), envoyée directement à
  ffmpeg (libx264, `yuv420p`, BT.709, CRF 18-23 selon la scène, `-maxrate` si besoin, image clé toutes
  les 2 s, `+faststart`) ; aucune image écrite sur disque ; plusieurs navigateurs en parallèle ; une
  scène n'est re-rendue que si ses entrées ont changé (empreinte) ; assemblage par copie de flux.
- **Narration** : Fish Audio, `POST https://api.fish.audio/v1/tts`, en-tête `model: drama-3`, corps :
  `temperature` 0.1, `format` mp3, `mp3_bitrate` 192, `sample_rate` 44100, `latency` normal, `normalize`
  true, `condition_on_previous_chunks` true, `prosody` {`speed` 1.0, `normalize_loudness` true},
  `reference_id` de la voix. Une requête par paragraphe ; une seule indication de jeu au début
  (`[calm, natural narrator voice]`) et `[long pause]` uniquement entre paragraphes principaux ; pas de
  `<emphasis>` ni `<stress>` ; pour ralentir, jamais `speed` < 1 mais `atempo` ffmpeg ; prononciations
  épinglées en phonèmes (`<|phoneme_start|>...<|phoneme_end|>`) pour MHD, ABC, VKS, DRESDYN, SFEMaNS,
  MilaDy, Gissinger (prononciation française), Reynolds, Rm... ; cache par (texte, voix, réglages) pour ne
  jamais payer deux fois. La clé d'API est fournie par l'auteur hors du dépôt (jamais commitée).
- **Minutage** : début de chaque phrase par détection de silences dans chaque paragraphe ; durée de
  scène = amorce + audio + pauses + fin ; les repères de la scène = débuts de phrase.
- **Contrôle de la narration** : transcription automatique (faster-whisper, modèle `base`/`small`, en
  anglais et en français), comparaison au script (mots manquants, ajoutés, prononciations fautives),
  resynthèse des paragraphes défectueux.
- **Sous-titres** : depuis le texte du script ; 2 lignes de 42 caractères au plus, <= 17 caractères/s ;
  boîte sombre semi-opaque (lisible sur les particules) ; incrustés scène par scène (pas de réencodage
  du film entier).
- **Livraison** : Git LFS pour les MP4 (ou une release GitHub si tu y as accès), jamais de fichier
  > 1,9 Go.

## 7. Organisation et parallélisme (agents cloud Cursor)

1. **Planification** : inventaire du contenu (concepts L0-L5 avec sources, chiffres exacts avec
   fichier:ligne, ressources réutilisables, résultats manquants), guide de style, plan chapitré avec durées
   et statut de chaque scène (prête / en attente). **Deux relectures adverses** du plan avant toute
   écriture : exactitude scientifique (vérifier chaque affirmation contre le site) et pédagogie
   (accroche dans les 30 premières secondes, pas de falaise, chaque notion motivée avant d'être
   formalisée, durées réalistes).
2. **Fondations** (un agent) : moteur de scène déterministe, bibliothèque de composants partagés (carte
   de chapitre, pastilles d'honnêteté, bandeaux, carte de question, emplacements de résultats à venir,
   formules terme à terme, graphiques, champs, motifs récurrents), chaîne de capture, de narration, de
   mixage et de montage, kit de changement de narration.
3. **Script** : un agent rédacteur par chapitre ou module, puis **un agent relecteur adverse** par unité
   (exactitude, oral et synthèse vocale, pédagogie, rythme, cadrage du § 3), puis une passe de cohérence
   globale (continuité entre chapitres, feuille de symboles, chiffres identiques partout, registre des
   questions).
4. **Pilote** : une unité représentative entièrement animée et relue, pour valider les composants
   avant de multiplier les agents.
5. **Animation en parallèle** : lance **plusieurs agents cloud Cursor**, un par lot d'unités, chacun sur
   sa branche (`grok/video-<lot>`), avec des fichiers disjoints ; chacun construit ses scènes, contrôle
   une image par repère et un brouillon animé, fait relire par un agent indépendant (chevauchements,
   coupures au bord, lisibilité, couleurs, exactitude de ce qui est dessiné), corrige, puis fusionne dans
   la branche d'intégration `grok/video`. La traduction française (fichiers séparés, mêmes identifiants
   de phrase) et sa relecture par un relecteur francophone exigeant peuvent tourner en parallèle.
6. **Revue transversale** sur les images de toutes les unités (homogénéité du style), puis rendu des
   quatre films, contrôle final : aucune erreur de page, aucune image noire, synchronisation
   son/image, sous-titres, loudness, taille des fichiers.

## 8. Barre de qualité

- Exactitude : zéro chiffre non sourcé, zéro surenchère (rien de présenté comme obtenu qui ne soit que
  prévu ; aucune affirmation sur des renversements en 3D générés).
- Clarté : une idée par plan, texte >= 28 px en 1080p, rien ne se chevauche ni ne sort du cadre, code
  couleur respecté, images déterministes.
- Écoute : phrases courtes, écrites pour l'oreille ; nombres écrits comme ils se disent ; pas
  d'abréviation que la voix lirait mal sans épinglage.
- Le film fonctionne entièrement **sans** les résultats à venir (paris et questions), et s'améliore
  quand ils arrivent.

## 9. Indépendance et périmètre

- Travaille **uniquement** dans un dossier `video-grok/` du dépôt et sur des branches `grok/...` ; **ne
  pousse jamais sur `main`** ; ne modifie aucun fichier du site.
- **N'ouvre pas et ne réutilise pas** le dossier `video/` du dépôt (production de l'autre équipe) ni ses
  scripts, scènes, plans ou données : la comparaison doit porter sur deux productions indépendantes
  partant des mêmes sources.
- Aucun secret dans le dépôt (clés d'API par variables d'environnement ou secrets de l'agent).
- Aucune simulation, aucun entraînement, aucun banc de performance.

## 10. Mesures pour la comparaison

Tiens un journal `video-grok/STATS.md` : durée murale totale et par phase, nombre d'agents (dont agents
cloud Cursor) et d'exécutions, tokens consommés et coût si disponibles, nombre de requêtes et minutes de
synthèse vocale facturées, temps de rendu par film, tailles des fichiers, nombre de défauts trouvés et
corrigés par les relectures, et ce qui n'a pas pu être fait. Termine par un rapport en français :
livrables, liens, limites, et ce que tu ferais avec plus de temps.
