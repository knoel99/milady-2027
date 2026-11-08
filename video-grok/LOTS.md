# Lots, intégration, portes, pilote

## Branche d’intégration

`grok/video` **n’existe pas** sur `origin` au moment de ce plan (seul `origin/main` était présent). Elle ne doit pas être créée en fusionnant `main` avec quoi que ce soit d’autre, ni en y poussant un film.

Création prévue, au début des fondations, par une commande qui ne fait que pointer le commit source `4e42429716c093df34ba05b47ada542a13d39c50`, puis y recevoir des fusions **depuis** des branches `grok/video-*` par pull requests. Personne ne pousse `main`. Personne ne merge cette planification dans `main`.

Cette branche `grok/video-plan` porte les documents de phase 1. Tant que `grok/video` n’existe pas, une pull request éventuelle n’a que `main` comme base. Elle reste ouverte et **non fusionnée**. Quand `grok/video` existera, la base sera retargetée vers `grok/video`.

## Porte G0, avant toute écriture

Deux relectures adverses indépendantes, par des agents qui n’ont pas rédigé ce plan. Périmètre exact : `REVUES.md`. Tant que les deux rapports ne sont pas dans `video-grok/revues/` et que les défauts bloquants ne sont pas corrigés dans le plan, il est interdit de :

- créer `video-grok/narration/` ;
- écrire une scène HTML ;
- appeler Fish ;
- lancer un agent d’animation.

Les relecteurs ajoutent des fichiers neufs. Ils ne réécrivent pas `PLAN.md` eux-mêmes.

## Fondations (un agent, après G0)

Branche `grok/video-foundations`. Fichiers seulement :

- `video-grok/engine/**`
- `video-grok/components/**`
- `video-grok/tools/**`
- `video-grok/vendor/**` (polices et bibliothèques locales)

Contenu : `window.seek(t)`, horloge virtuelle, graine fixe, repères nommés, pastille, carte de chapitre, carte question, emplacement « not yet run », calque KaTeX, graphes, champs, motifs de `STYLE.md`, capture Playwright vers ffmpeg sans PNG sur disque, cache de narration, mixage deux pistes, kit de changement de `reference_id`, documentation du kit en français. Pas une scène de chapitre.

## Lots de script (après G0, fichiers disjoints)

Mêmes identifiants de repères en anglais et en français. Le lot français ne touche que `narration/fr/`.

| Branche | Fichiers | Chapitres |
|---|---|---|
| `grok/video-script-l0` | `narration/*/g00` … `g06` | ouverture jusqu’au récapitulatif L2 |
| `grok/video-script-l3` | `narration/*/g07` … `g11` | E1, Rice, flot, contraintes, tableau |
| `grok/video-script-l5` | `narration/*/g12` … `g15` | carte, paris, questions, aiguille |
| `grok/video-script-x` | `narration/*/x01` … `x05` | modules |
| `grok/video-script-fr` | `narration/fr/**` seulement | traduction, peut tourner en parallèle une fois les identifiants d’anglais gelés |

Un relecteur adverse par lot (exactitude, oral, pédagogie, rythme, cadrage du §3 du brief), puis une passe de cohérence : symboles de `STYLE.md` §6, chiffres identiques à `INVENTAIRE.md`, registre de `QUESTIONS.md`.

## Pilote (avant de multiplier les agents d’animation)

Unité : `g10`. Scènes animées : `g10.classes` et `g10.sample`. La séquence d’essai ajoute deux extraits, sans animer tout le chapitre.

- Carte `g10.card`, 8 s, phrase de `QUESTIONS.md` `q.g10`.
- Caveat oral de `g10.law`, en anglais et en français : une graine, interpolation, ce n’est pas une dynamo. Le texte anglais ne suffit pas.

Pourquoi celles-là : elles croisent pastille PROVED et pastille MEASURED, les quatre couleurs de rôle, un calque formule, une pause predict, une carte question, un plancher, et l’interdiction de trier les barres par « gagnant ». Si ces composants échouent, les multiplier est inutile. Le pilote ne prouve pas le passage g06 vers g08. Ce passage se relit à G1 et G2.

Le pilote est sur `grok/video-pilot`, fichiers :

- `video-grok/scenes/g10/classes.html`
- `video-grok/scenes/g10/sample.html`
- `video-grok/scenes/g10/card.html` (extrait de 8 s, pas le chapitre)
- `video-grok/scenes/g10/README.md` (comment les repères sont branchés, y compris le caveat oral)

Critères de sortie du pilote, tous obligatoires :

1. `seek` déterministe : deux captures du même repère, même image.
2. Texte ≥ 28 px, rien dans la marge de 80 px, rien qui se chevauche sur la barre de divergence logarithmique.
3. La formule du corollaire 6 n’est pas dans le sous-titre. Le calque énonce l’absence de masse en 0 comme hypothèse. Il n’écrit pas « KL = ∞ » à côté de 4,17×10⁻¹⁷ ni de 8,64×10⁻⁴.
4. La pause predict dure 2 à 3 s et précède la barre écrasée.
5. Les chiffres affichés sont ceux de `digest.md:134-144` et `digest.md:19`, avec pastille MEASURED.
6. La capture comprend la carte de 8 s et une limite E2 audible dans les deux langues.
7. Un relecteur qui n’a pas animé le pilote coche la liste. S’il refuse, on ne lance pas les lots d’animation.

## Lots d’animation (après le pilote)

Une branche par lot, fichiers disjoints sous `video-grok/scenes/<id>/`. Fusion vers `grok/video` seulement.

| Branche | Scènes | Pourquoi ce découpage |
|---|---|---|
| `grok/video-a-open` | g00, g01, g02, g15 | le motif aiguille est aux deux bouts ; un seul agent le tient |
| `grok/video-b-labs` | g03, g04, g05, g06 | CONTEXT historique et projet |
| `grok/video-c-e1` | g07, g08 | mesures E1 et Rice |
| `grok/video-d-gen` | g09, g10 | flot et contraintes ; g10 réutilise le pilote sans le réécrire |
| `grok/video-e-results` | g11, g12 | tableau et carte bibliographique |
| `grok/video-f-bets` | g13, g14 | emplacements vides et registre |
| `grok/video-x-deep` | x01, x02, x03, x04, x05 | étendu seul |

Chaque lot : une image par repère, un brouillon animé, une relecture indépendante (chevauchements, bords, lisibilité, couleurs, exactitude de ce qui est dessiné), correction, puis pull request vers `grok/video`.

La traduction française de l’animation n’existe pas : les visuels restent anglais. Seule la voix et les sous-titres changent.

## Portes suivantes

| Porte | Quand | Bloque |
|---|---|---|
| G0 | deux revues du plan | toute narration et toute scène |
| G1 | relecture adverse de chaque lot de script | le gel des identifiants |
| G2 | cohérence globale des scripts | le pilote sonore |
| G3 | pilote g10 accepté | les lots d’animation |
| G4 | relecture image de chaque lot | la fusion dans `grok/video` |
| G5 | homogénéité transversale | le rendu des quatre films |
| G6 | aucun écran noir, synchro, sous-titres, loudness, taille < 1,9 Go | la prétention que les films existent |

## Hors lots

- Pas d’agent sur `video/`.
- Pas de simulation, pas d’entraînement, pas de banc, pas de location.
- Fish seulement après G1, avec la clé hors dépôt, cache activé (`FISH.md`).
- Les scènes `waiting` se construisent avec le rectangle « not yet run ». Leur créneau `result-*` reste vide jusqu’à un JSON réel.
