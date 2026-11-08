# STATS

Journal de comparaison. Une case n’est remplie que si la valeur a été observée. Sinon : `unavailable`. Aucune estimation.

## Exécution

| Champ | Valeur |
|---|---|
| Phase | 1, planification seulement |
| Début (horodatage du message qui lance la phase) | 2026-11-08T07:04:00Z |
| Branche créée | 2026-11-08T07:08:28Z |
| Fin de phase | 2026-11-08T07:16:35Z (755 s) |
| Agents | 1 (cette exécution) |
| Agents cloud lancés en plus | 0 |
| Sous-agents | 0 |
| Simulations, entraînements, bancs | 0 |
| Locations cloud payantes | 0 |
| Requêtes Fish | 0 |
| Minutes de synthèse facturées | 0 |
| Films rendus | 0 |
| Tailles MP4 | sans objet |
| Temps de rendu | sans objet |
| Défauts trouvés par une relecture adverse | 0 (relectures non lancées) |
| Défauts corrigés par une relecture adverse | 0 |
| Tokens consommés | unavailable |
| Coût | unavailable |

Les compteurs de tokens et le coût ne sont pas exposés à cette exécution. Ils ne sont pas estimés.

## Durée par phase

Horloge de la machine. La lecture des sources va jusqu’à la création de la branche (07:08:28Z). La rédaction des documents va de là jusqu’à l’horloge ci-dessous, commit dans la foulée.

| Phase | Début | Fin | Durée murale |
|---|---|---|---|
| 1a. Lecture des sources | 2026-11-08T07:04:00Z | 2026-11-08T07:08:28Z | 268 s |
| 1b. Rédaction | 2026-11-08T07:08:28Z | 2026-11-08T07:16:35Z | 487 s |
| 1. Planification (somme) | 2026-11-08T07:04:00Z | 2026-11-08T07:16:35Z | 755 s (12,6 min) |
| 2. Fondations | — | — | non commencée |
| 3. Scripts | — | — | non commencée |
| 4. Pilote | — | — | non commencée |
| 5. Animation | — | — | non commencée |
| 6. Rendu | — | — | non commencée |

## Ce qui n’a pas été fait

- Les quatre films, les sous-titres, les pistes séparées, le kit de narration, les convertisseurs, la fiche vouvoyée finale, le document d’état de l’art rédigé pour les encadrants (le plan en tient lieu, pas le livrable §4.7).
- À la clôture de la phase 1, les deux relectures n’existaient pas encore. Elles ont été écrites ensuite, sur d’autres branches. Cette branche ne les modifie pas.
- L’épinglage des faits externes du §E de `INCERTITUDES.md`.
- Toute mesure de coût Fish, de tokens, ou de temps GPU.

## Exécution 2, correctif des constats G0

Une exécution. Pas de sous-agent. Pas d’appel Fish. Pas de simulation. Tokens et coût toujours `unavailable`.

| Champ | Valeur |
|---|---|
| Début (horodatage du message) | 2026-11-08T08:59:00Z |
| Rapport science lu | `a050a7fbb9f229f8c80e388fcaa0357571d99318`, fichier `video-grok/revues/SCIENCE.md` sur `grok/revue-science` |
| Rapport pédagogie lu | `d4a3979d5c588e2a2695cd481c2fc8e5f5d4bc4e`, fichier `video-grok/revues/PEDAGOGIE.md` sur `grok/revue-pedagogie` |
| Sous-agents | 0 |
| Requêtes Fish | 0 |
| Tokens | unavailable |
| Coût | unavailable |
| G0 | non close. Ce correctif n’est pas une approbation |

Horloge de fin écrite juste avant le commit de ce correctif.

- correction_end: 2026-11-08T09:06:37Z
- correction_elapsed_s: 457

## Clôture de la phase 1

Horloge lue juste avant le commit.

- phase_1_end: 2026-11-08T07:16:35Z
- phase_1_elapsed: 755 s
