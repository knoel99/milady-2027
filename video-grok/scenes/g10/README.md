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

## hard.html

La scène dure 43 s. La pastille principale est MEASURED.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.hard.show` | 0 | V0, divergence 0,408. |
| `cue.g10.hard.penalty` | 8 | V0 puis V1 sur u, 0,34. |
| `cue.g10.hard.magnetic` | 14 | V1 sur B, 0,162. |
| `cue.g10.hard.projection` | 20 | V2 et V4, autour de 10⁻¹⁷. |
| `cue.g10.hard.flow` | 28 | V3, flot projeté 2,03×10⁻⁸. |
| `cue.g10.hard.order` | 34 | L'ordre reste fixe. |
| `cue.g10.hard.winner` | 38 | « Do not sort them by a winner. » |
| `cue.g10.hard.end` | 43 | Fin. |

L'ordre des rangées reste V0, V1 u, V1 B, V2, V4, V3. Ce n'est pas l'ordre des valeurs. Les chiffres sont ceux de `digest.md` lignes 134 à 138. L'échelle est logarithmique.

## sym.html

La scène dure 30 s. La pastille principale est PROVED. Les deux barres sont schématiques et de même longueur. Le champ dessiné est B.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.sym.show` | 0 | Changer le signe de B. |
| `cue.g10.sym.sign` | 6 | B vers −B est une symétrie de la loi. |
| `cue.g10.sym.equivariance` | 12 | L'équivariance tient cette symétrie. |
| `cue.g10.sym.budget` | 18 | Les identités de budget ne fixent pas les poids. |
| `cue.g10.sym.weights` | 24 | Les deux polarités. |
| `cue.g10.sym.end` | 30 | Fin. |

## law.html

La scène dure 39 s. La pastille principale est MEASURED. `cue.g10.law.caveat` est à 19,5 s, la moitié du créneau, pour rester l'horloge des deux pistes.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.law.show` | 0 | V5, distance 0,699. |
| `cue.g10.law.witness` | 7 | Le témoin à 2,52. |
| `cue.g10.law.floor` | 13 | Plancher 0,0304. |
| `cue.g10.law.caveat` | 19.5 | E2 forcé, une graine, interpolation, pas une dynamo. |
| `cue.g10.law.seed` | 25 | « One seed. » |
| `cue.g10.law.interpolation` | 29 | Interpolation. |
| `cue.g10.law.dynamo` | 34 | Pas une dynamo. |
| `cue.g10.law.end` | 39 | Fin. |

L'ordre des rangées reste V5, witness, floor. Le témoin est la barre la plus haute. Il ne gagne pas. Les chiffres 0,699 et 2,52 viennent des lignes 139 et 140 de `digest.md`. Le plancher 0,0304 est la distance d'énergie du sous-échantillon sur les η d'entraînement, ligne 157.

## bias.html

La scène dure 25 s. La pastille principale est PROVED. Les deux demi-lots sont schématiques et de même longueur. Aucun chiffre n'est affiché.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.bias.show` | 0 | Le carré d'une moyenne empirique. |
| `cue.g10.bias.variance` | 6 | Ce carré pénalise la variance. |
| `cue.g10.bias.halves` | 12 | Deux demi-lots indépendants. |
| `cue.g10.bias.removes` | 17 | Leur produit retire ce biais. |
| `cue.g10.bias.model` | 21 | L'identité ne choisit pas un modèle. |
| `cue.g10.bias.end` | 25 | Fin. |

## close.html

La scène dure 17 s. Pas de pastille. Pas de carte question. Le niveau reste L3.

| Repère | t (s) | Écran |
|---|---|---|
| `cue.g10.close.show` | 0 | Pas de masse en zéro. |
| `cue.g10.close.zero` | 4 | La valeur tombe exactement sur zéro. |
| `cue.g10.close.anchor` | 8 | L'ancrage limite le réglage fin. |
| `cue.g10.close.states` | 12 | Le chapitre énonce les propositions. |
| `cue.g10.close.prove` | 15 | Il ne les prouve pas. |
| `cue.g10.close.end` | 17 | Fin. |

## Caveat oral de g10.law

`cues.json` réserve deux créneaux `cue.g10.law.caveat`.

Le créneau anglais pointe vers `narration/en/g10.md`. La phrase gelée est "E2 is two-dimensional and forced. One seed. The tests are interpolation. This is not a dynamo." Il n'y a pas de fichier audio.

Le créneau français pointe vers `narration/fr/g10.law.caveat.md`. La phrase est "E2 est bidimensionnel et forcé. Une seule graine aléatoire testée. Valeurs intermédiaires dans la plage d’entraînement. Pas une dynamo." Ce fichier ne reprend pas le chapitre. `narration/fr/g10.md` n'existe pas.

Les deux créneaux sont PENDING. Le critère audible, en anglais et en français, attend la voix. Le critère du relecteur indépendant n'est pas un test de cette branche.
