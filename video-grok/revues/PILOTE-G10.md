# Revue indépendante du pilote g10

Le pilote ne débloque pas les lots d’animation. La porte G3 reste fermée.

Les critères 1 à 5 tiennent sur le code, les tests exécutés et les images du test de capture. Le critère 6 reste pending : la carte de 8 s est dans la capture, et la limite E2 n’est audible dans aucune des deux langues. Cette relecture coche la liste (critère 7) et refuse le lancement des lots. Hors voix, aucun défaut bloquant.

## Périmètre

Relecture de la PR #6, `feat(g10): animer le pilote classes, sample et la carte`. L’auteur du pilote est l’agent `bc-a0ce4bb5-39c2-5602-8236-612b8bef6b35`. Cette revue ne réécrit aucune scène.

- Branche source : `grok/video-pilot`.
- Commit demandé : `9b7b32b6559c640ab022c4c3aa067b1ea66415e2`.
- Tête de la PR au moment de la relecture : `ee68423e5bbb7cf0f0b8aa03bd53ce95f8729cf8`.
- Base : `grok/video` @ `927890bc6778d9357e007ea660b6247862627e9b`.

`git diff --name-only 9b7b32b ee68423` ne contient que `video-grok/tools/test/g10.test.mjs`. Les scènes, le moteur et le digest sont identiques entre les deux commits. Le commit de tête ferme le navigateur si l’écriture échoue et place les PNG dans un dossier temporaire. Les critères ci-dessous sont lus sur les scènes du commit demandé, et les tests sont exécutés sur la tête, qui est ce que la PR fusionnerait.

`video/` n’a pas été ouvert. Aucun appel Fish, aucune synthèse.

Le magasin d’artefacts de l’auteur n’était pas monté ici. Les sept PNG cités dans le corps de la PR ont été produits par le test de capture de la tête, puis lus. Ce ne sont pas les fichiers hébergés par l’auteur. Les scènes qui les produisent sont celles du commit demandé.

## Exécution

Dans l’arbre `ee68423` :

- `node --test engine/scene.test.mjs` depuis `video-grok` : 13 tests, 13 réussites.
- `node --test test/*.test.mjs` depuis `video-grok/tools` : 17 tests, 17 réussites, dont les 6 tests de `g10.test.mjs`.

Les captures font 1920×1080. Le test affirme que deux seeks du même repère donnent le même tampon PNG.

## 1. Seek déterministe — pass

Deux captures du même repère sont le même fichier pour les sept repères du test : `cue.g10.classes.c4`, `cue.g10.sample.div`, `cue.g10.sample.predict`, `cue.g10.sample.e1`, `cue.g10.sample.e1.spread`, `cue.g10.sample.formula`, `cue.g10.card`.

Preuve. `video-grok/tools/test/g10.test.mjs` cherche le repère, avance d’une seconde, revient au repère, et compare les tampons (`first.equals(second)`). Le test a réussi. `window.seek` (`video-grok/engine/runtime.js`) cale l’horloge virtuelle et `Math.random` sur la graine de scène et l’image. `video-grok/engine/clock.js` ne lit pas l’horloge du mur. Les tests moteur « deux lectures du même instant donnent la même vue » et « la graine et l'image fixent le hasard » ont aussi réussi.

Les repères qui dessinent un champ (`cue.g10.classes.c1`, `cue.g10.classes.c2`) ne sont pas dans la paire d’images. Leur tirage passe par `randomAt(seed, frame)`. Le mécanisme est le même. La preuve d’image porte sur les sept repères ci-dessus.

## 2. Texte, marge, barre logarithmique — pass

Le test « le texte reste à 28 px, hors marge, et ne coupe pas les barres » a réussi dans Chrome headless, viewport 1920×1080. Il mesure le `font-size` calculé de chaque nœud de texte visible et ses rectangles. Il exige une taille d’au moins 28 px, un rectangle dans `[80, 1840] × [80, 1000]`, et aucune intersection avec `.bar-fill` ni `.floor-line`. Il exige aussi que deux textes hors KaTeX ne se coupent pas. Les repères couverts incluent la divergence à huit barres, la pause, la distance, la barre écrasée, la formule, les quatre classes et la carte.

La feuille de style fixe le corps à 28 px ou plus (`video-grok/components/stage.css` : pastille 28 px, titres et nombres 32 px, formule 36 px). La zone sûre est `left: 80px; top: 80px; width: 1760px; height: 920px`.

L’image `g10-sample-divergence.png` montre les huit étiquettes à droite de la piste, la pastille MEASURED et « L3 » dans le cadre, le sous-titre dans la bande basse. Aucun glyphe ne coupe les barres violettes. L’image des quatre classes montre des barres d’égale longueur, sans chiffre, et la mention `schematic, not a measurement`.

## 3. Corollaire 6 — pass

La formule du corollaire 6, dans `en/rapport/index.qmd:447-455`, est l’hypothèse d’absence de masse en 0, puis la singularité et la KL infinie, puis la borne W1 sous hypothèse lipschitzienne. Cette formule n’est dans aucun sous-titre.

Les sous-titres de `sample.json` sont des extraits de `video-grok/narration/en/g10.md`. Le test « les sous-titres sont des extraits du script » refuse `KL`, `infty`, `∞` et `Hypothesis` dans ces lignes. Il a réussi.

Le calque, `sample.json:196`, est `\text{Hypothesis: no mass at 0.}`. Il est visible de `cue.g10.sample.formula` (38 s) à la fin. À cet instant, `viewAt` donne `subtitle: null`, `bars: null`, `badges: []`, matière `paper`. L’image `g10-sample-formula.png` montre cette phrase seule sur le papier, avec « L3 », sans pastille MEASURED, sans `4.17e-17`, sans `8.64e-04`, sans `KL = ∞`.

La pastille MEASURED s’arrête au repère formule (`sample.json`, calque `badge`, `until: cue.g10.sample.formula`). L’hypothèse n’est pas présentée comme une mesure.

## 4. Pause predict — pass

`cue.g10.sample.predict` est à 22 s, `cue.g10.sample.e1` à 25 s. La durée est 3 s, dans l’intervalle 2 à 3 s. La narration gelée porte `pause: 3s` (`narration/en/g10.md:67`).

`visible` est ouvert à gauche et fermé à droite. À t = 22 s, les barres de dissipation sont déjà parties et le sous-titre est `Does the crushed bar help?`. Au milieu de la pause, `bars` est `null` et le document ne contient pas `4.17e-17`. L’image `g10-sample-predict.png` est cet écran : pastille MEASURED, « L3 », la question, aucune barre.

La barre écrasée commence à `cue.g10.sample.e1.spread`, 31 s, après la pause. Son étiquette E est `4.17e-17`, inférieure à la barre C `0.384`. L’image `g10-sample-crushed.png` le montre. Entre les deux, le panneau de distance (25 s) n’est pas la barre écrasée.

## 5. Chiffres et pastille MEASURED — pass

Chaque étiquette de barre a été comparée à la cellule du digest, pas seulement au sac de jetons du test. Le test « les chiffres affichés sont ceux du digest » a réussi. Il accepte tout jeton des lignes 14, 19 et 134 à 144, donc il ne prouve pas la colonne à lui seul. `0.162`, div. rel. B de V1, est sur la ligne 135 et passerait ce filtre. Il est absent de `sample.json`.

Colonne div. rel. u, lignes 134 à 141, ordre fixe V0, V1, V2, V3, V4, V5, witness, subsample. Cet ordre n’est pas l’ordre des valeurs. subsample a le rôle `infra`. Les autres ont le rôle `model`.

| Écran | Étiquette | Digest |
|---|---|---|
| V0 | `0.408` | ligne 134, div. rel. u |
| V1 | `0.34` | ligne 135, div. rel. u |
| V2 | `5.05e-17` | ligne 136, div. rel. u |
| V3 | `2.03e-08` | ligne 137, div. rel. u |
| V4 | `1.78e-17` | ligne 138, div. rel. u |
| V5 | `1.74e-17` | ligne 139, div. rel. u |
| witness | `1.78e-17` | ligne 140, V5_temoin, div. rel. u |
| subsample | `1.52e-17` | ligne 141, reference_sous_echantillon, div. rel. u |
| résidu V0 | `0.491` | ligne 134, résidu énergie |
| résidu recalage | `8.27e-06` | ligne 144, résidu énergie |
| dissipation V0 | `0.68` | ligne 134, σ(D)/σ_ref |
| dissipation recalage | `8.64e-04` | ligne 144, σ(D)/σ_ref |
| distance E | `0.0231` | ligne 19, E_projection_C, dist. énergie |
| σ(dE/dt) E | `4.17e-17` | ligne 19, E_projection_C, σ(dE/dt) |

L’orthographe affichée est celle du digest, y compris `2.03e-08`, `8.27e-06` et `8.64e-04`. La pastille principale est MEASURED sur tous ces panneaux (`sample.json`, calque badge, couleur `#C98A00`). Les images de divergence, de distance et de barre écrasée la montrent.

Deux étiquettes de comparaison viennent de la ligne 14, C_equivariant, parce que la narration gelée les dit : `0.00257` (dist. énergie) et `0.384` (σ(dE/dt)). Elles ne sont pas sur les lignes 134 à 144 ni sur la ligne 19. Ce sont les bonnes cellules, pas des nombres inventés. Le quotient `0.0231 / 0.00257` vaut 8,99. Le sous-titre dit « a factor of 9 », qui est la phrase gelée, pas une cellule du digest. La légende du plancher affiche `n = 10000`, présent à la ligne 5. La valeur du plancher `0.0012269410015240956` est celle de `n_gen.energie` à la ligne 48. Elle place le trait, elle n’est pas imprimée comme mesure.

Les quatre classes portent la pastille PROVED et aucun chiffre à l’écran (`schematic: true`). Leur valeur interne `1` n’est pas peinte.

## 6. Carte de 8 s et limite E2 audible — pending

La carte tient. La voix ne tient pas. Le critère entier reste pending.

Carte. `card.json` dure 8 s, de `cue.g10.card` à `cue.g10.card.end`. À t = 0 et à t = 7,9 s, la phrase est `Must stationarity fine-tuning be anchored first?`, classe A, pastille PLANNED. À t = 8 s la carte est absente. La phrase est celle de `QUESTIONS.md` `q.g10` et de `narration/en/g10.md`. L’image `g10-card.png` la montre. Le test de capture inclut ce repère et a réussi.

Voix. `scenes/g10/cues.json` réserve deux créneaux `cue.g10.law.caveat`. Les deux ont `audio: null` et `status: "PENDING"`. Le créneau anglais pointe vers `narration/en/g10.md`. Le créneau français a `source: null`. Le test « le caveat de g10.law est branché sans voix et sans français » a réussi, y compris le refus de lecture de `narration/fr/g10.md`.

L’arbre `ee68423` ne contient aucun fichier `narration/fr/` et aucun `.wav`, `.mp3`, `.ogg`, `.m4a` ou `.flac`. Les pages `classes.html`, `sample.html` et `card.html` montent leur JSON de scène. Elles ne chargent pas `cues.json` et n’ont pas d’élément audio.

Le texte anglais existe, gelé, dans `narration/en/g10.md:51` : « E2 is two-dimensional and forced. One seed. The tests are interpolation. This is not a dynamo. » Il n’est pas lu. Aucune phrase française n’existe dans ce dossier. Le texte anglais ne suffit pas.

## 7. Relecture indépendante — pass

Cette revue coche les sept critères. Elle n’a pas animé le pilote. Le critère 6 étant pending, la liste n’est pas acceptée : les lots d’animation ne partent pas.

## Écarts non bloquants

Le plafond de 42 caractères coupe des phrases du script. À l’écran, le dernier sous-titre avant la formule est « A positive variance does not prove ». La suite gelée, « there is no mass at 0 », n’est pas dans ce sous-titre. Elle arrive au repère suivant, sur le calque non lu. Le critère 3 reste satisfait : le calque énonce l’hypothèse, et la variance mesurée n’est plus à l’écran.

« The energy-budget spread falls » et « C4 is a stationarity identity » sont aussi des préfixes. La narration complète est dans `narration/en/g10.md`.

Le filtre de jetons du test de chiffres inclut la ligne 14 et ne fixe pas la colonne. Le tableau du critère 5 est la vérification directe. Elle ne change pas le verdict.

## Porte

G3 demande un pilote g10 accepté avant les lots d’animation (`LOTS.md`). Les critères 1 à 5 et 7 ne fournissent pas ce refus. Le critère 6, obligatoire, n’est pas passé. Le pilote ne débloque pas `grok/video-a-open`, `grok/video-b-labs`, `grok/video-c-e1`, `grok/video-d-gen`, `grok/video-e-results`, `grok/video-f-bets` ni `grok/video-x-deep`.
