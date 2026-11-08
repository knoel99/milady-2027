# Pilote g10

Ouvrez `classes.html`, `sample.html` ou `card.html`. Chaque page monte un document de scène et expose `window.seek`. Les images se calent sur les repères ci-dessous. Elles ne se calent pas sur l'horloge du mur.

## classes.html

La scène dure 45 s. La pastille principale est PROVED, le niveau est L3.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.classes.show` | 0 | La phrase d'ouverture. Pas encore de rangée. |
| `cue.g10.classes.c1` | 5 | C1, et le champ u. |
| `cue.g10.classes.c2` | 12 | C1 puis C2, et le champ B. |
| `cue.g10.classes.c3` | 19 | C1, C2, C3. |
| `cue.g10.classes.c4` | 26 | C1, C2, C3, C4. |
| `cue.g10.classes.bar` | 33 | "A short bar is not a prize." |
| `cue.g10.classes.claim` | 39 | "The place of the constraint is the claim." |
| `cue.g10.classes.end` | 45 | Fin. |

L'ordre des rangées reste C1, C2, C3, C4. Les longueurs sont égales. Le panneau porte `schematic, not a measurement`, donc aucun chiffre n'est affiché. La couleur de C1 est celle de u, celle de C2 celle de B, celle de C3 celle du modèle, celle de C4 celle du paramètre. C1 et C2 portent chacun sur les deux champs. La couleur sépare u et B. Elle ne réduit pas la classe à un seul champ.

Les sous-titres sont des extraits de `narration/en/g10.md`.

## sample.html

La scène dure 40 s. La pastille principale est MEASURED.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.sample.div` | 0 | Divergence relative de u, échelle log, une graine. |
| `cue.g10.sample.div.order` | 3 | La même barre. Le sous-titre interdit de trier par gagnant. |
| `cue.g10.sample.e2` | 6 | Résidu d'énergie, V0 puis rescaled. |
| `cue.g10.sample.e2.spread` | 12 | Rapport de dissipation. Le titre dit dissipation, pas D. |
| `cue.g10.sample.predict` | 22 | Question, 3 s, aucune barre. |
| `cue.g10.sample.e1` | 25 | Distances d'énergie C puis E, deux graines, plancher. |
| `cue.g10.sample.e1.spread` | 31 | Écart de budget, C puis E. E est la barre écrasée. |
| `cue.g10.sample.paper` | 37.733 | Fondu de 8 images vers le papier. |
| `cue.g10.sample.formula` | 38 | Hypothèse non lue, sur papier, sans pastille MEASURED. |
| `cue.g10.sample.end` | 40 | Fin. |

`cue.g10.sample.predict` dure 3 s, de 22 s à 25 s. `cue.g10.sample.e1.spread` arrive à 31 s. La barre `4.17e-17` est absente pendant la pause.

L'ordre du panneau de divergence est V0, V1, V2, V3, V4, V5, witness, subsample. Ce n'est pas l'ordre des valeurs. subsample est gris. Les variantes restent violet. La colonne lue est div. rel. u, lignes 134 à 141 de `experiences/resultats/digest.md`. La div. rel. B de V1, 0.162, n'est pas sur ce panneau.

Les autres étiquettes viennent des mêmes lignes, plus la ligne 19 pour `0.0231` et `4.17e-17`, et la ligne 14 pour `0.00257` et `0.384`. Le facteur 9 est celui du script. Il n'est pas une barre. Le plancher d'énergie est le nombre `n_gen` de la ligne 48. `n = 10000` est le nombre d'échantillons de la ligne 5. L'échelle log laisse une décade sous le plus petit échantillon, pour que ce plancher ne colle pas au bord gauche.

`cue.g10.sample.formula` affiche `Hypothesis: no mass at 0.` sur le papier, après le fondu. La pastille MEASURED s'arrête avant ce repère, pour ne pas présenter l'hypothèse comme une mesure. Le calque n'écrit pas KL = ∞, et il ne place pas cette hypothèse à côté de `4.17e-17` ni de `8.64e-04`. Le sous-titre ne reprend pas la formule.

## card.html

L'extrait dure 8 s, de `cue.g10.card` à `cue.g10.card.end`. La phrase de `q.g10` est `Must stationarity fine-tuning be anchored first?` La classe est A. La pastille est PLANNED.

## Caveat oral de g10.law

`cues.json` réserve deux créneaux `cue.g10.law.caveat`.

Le créneau anglais pointe vers `narration/en/g10.md`. La phrase gelée est "E2 is two-dimensional and forced. One seed. The tests are interpolation. This is not a dynamo." Il n'y a pas de fichier audio.

Le créneau français pointe vers `narration/fr/g10.law.caveat.md`. La phrase est "E2 est bidimensionnel et forcé. Une graine. Les tests sont de l’interpolation. Ce n’est pas une dynamo." Ce fichier ne reprend pas le chapitre. `narration/fr/g10.md` n'existe pas.

Les deux créneaux sont PENDING. Le critère audible, en anglais et en français, attend la voix. Le critère du relecteur indépendant n'est pas un test de cette branche.
