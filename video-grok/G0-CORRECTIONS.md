# Correctif des constats G0

Ce fichier répond aux rapports lus, sans les modifier et sans les approuver. G0 n’est pas close. Une revue indépendante doit relire le commit qui introduit ce correctif.

Science lue : commit `a050a7fbb9f229f8c80e388fcaa0357571d99318` sur `grok/revue-science`, fichier `video-grok/revues/SCIENCE.md`.

Pédagogie lue : commit `d4a3979d5c588e2a2695cd481c2fc8e5f5d4bc4e` sur `grok/revue-pedagogie`, fichier `video-grok/revues/PEDAGOGIE.md`. Repères de lignes de ce rapport-là visent l’ancien plan `b3517f5`. Les ancres ci-dessous sont les identifiants de scènes, stables.

Sources gelées inchangées : `4e42429716c093df34ba05b47ada542a13d39c50`. Aucune source n’a été fabriquée.

## S18 à S25

| Id | Changement | Preuve rouverte | Validation qui reste |
|---|---|---|---|
| S18 | `g08.rice` dit que la densité continue de (D, Ḋ) est une hypothèse, non garantie sur E1 déterministe, et que PROVED ne couvre pas les pourcentages. `g08.numbers` porte h = 0,2 et dit que 4 % et 6 % sont le contrôle numérique de la fenêtre. Inventaire, lignes Prop. 8, limites, contrôle numérique. `INCERTITUDES.md` U5. | `en/rapport/index.qmd:509-517`, `:528`, `:883`, `:901`. `digest.md:5`. | Relecture indépendante. Les sommes 4, 6, 14 et 42 % n’ont pas été recalculées. Elles restent celles de la ligne 883. |
| S19 | `x01.c6` énonce l’absence de masse en 0 comme hypothèse. Une variance positive ne la démontre pas. W1 demande en plus le caractère lipschitzien. Le calque de `g10.sample` n’écrit pas une KL infinie à côté de 4,17×10⁻¹⁷ ni de 8,64×10⁻⁴. Inventaire, ligne Cor. 6. `INCERTITUDES.md` U4. | `en/rapport/index.qmd:447-455`. La glose « générique dès que Var > 0 » est à la ligne 449. Elle n’est pas traitée comme une preuve. `digest.md:19` et `:49` et `:144`. | Relecture indépendante. La KL infinie reste la conclusion du corollaire sous hypothèse, pas un chiffre mesuré. |
| S20 | `g11.e3` dure 1:20. Il nomme Rm = 1/η, les arrondis 8,87, 17,6 et 26,8, l’interpolation sur la seconde moitié, environ 0,1 près de 17,5, environ une unité pour le troisième seuil, et refuse l’intervalle de confiance. `x02.sign` répète la précision du troisième seuil. `INCERTITUDES.md` U3 ne dit plus « ± ». | `en/rapport/index.qmd:1112-1114`. `e3_abc.json:9` et `:167-171`. | Relecture indépendante. x02 ne suffit pas. Le cœur porte la précision. |
| S21 | Inventaire §7, ligne Fukami et Taira. Trois variables latentes, Re = 100, `en/rapport/index.qmd:169`. `g12.learn` pointe vers cette ligne. | Ligne 169 relue. Le profil est un NACA 0012. Le plan ne montre que les deux nombres demandés. | Relecture indépendante. |
| S22 | Inventaire §5.5, ligne Groupe ABC. 24 éléments, symétries paires, `dynamo.md:400` et `en/rapport/index.qmd:1120`. `x02.group` interdit les autres nombres du paragraphe. | Ligne 400 relue. Rm1, Rm2, ω et σ à 25 000 ne sont pas ajoutés. | Relecture indépendante. |
| S23 | Inventaire §5.1, ligne Pont \|D\| < 0,25, sources `:729`, `:807`, `:1269`. Ce n’est pas D1 de Riga. `x03.bridge` cite 729 pour 0,25 et 883 pour 2×10⁻⁴. | Les trois lignes du rapport ont été relues. 883 ne contient pas 0,25. | Relecture indépendante. |
| S24 | `x04.iron` est coupé en trois plans. Mode axisymétrique, `dynamo.md:193`. μr d’ordre 50, `:220`. μr ≈ 100, `:160`. `x04.mur-note` dit que ce n’est pas un intervalle. Inventaire §7, ligne Perméabilité VKS. | Les trois lignes ont été relues. 193 dit m = 0. 194 dit aussi μr maximal 60 et mesures 65 à 70. Ces deux nombres ne sont pas à l’écran. | Relecture indépendante. Giesecke 2010 n’est pas fusionné avec Nore ni Monchaux. |
| S25 | La date reste à l’écran, avec le statut à reconfirmer. Inventaire §7, ligne Clôture EDARI. `x05.genci` cite `RECOMMANDATION-CLOUD.md:872-873`. Ce n’est pas une date confirmée par les encadrants. | Lignes 872-873 relues. Le texte dit 08/02/2027 à 9 h, source EDARI, dans une recommandation du 2026-11-08. | Les encadrants n’ont pas confirmé la date. Le film doit le dire. |

S20 emporte aussi la réserve S8. L’idée de `g11.e3` contient Rm = 1/η, déjà dans `e3_abc.json:9` et `en/rapport/index.qmd:1112`. Ce n’est pas un neuvième bloquant traité à part. La revue suivante dit si la réserve est levée.

## Réserves pédagogiques

| Id | Résolution dans ce correctif | Vérification plus tard |
|---|---|---|
| R1 | x01 somme 5:00. x02 somme 3:30. x03 somme 3:00. x04 somme 4:00. x05 somme 3:30. Total des modules 19:00. Cœur 41:00. Étendu 60:00. Les cartes visibles sont à 0:08. Le temps retiré aux cartes trop longues a d’abord servi à rentrer dans l’enveloppe. x01.p4 passe de 0:50 à 0:40 et x01.p9 de 0:50 à 0:42. x01.c6 reste 0:50. x04 gagne les plans de perméabilité au lieu de combler par du silence. | Recompter les tables au prochain commit. Script de somme relancé sur `PLAN.md` pendant ce correctif. Sortie : cœur 2460 s, modules 180+300+210+240+210 = 1140 s. |
| R2 | Chaque carte visible est 0:08. Le solde de l’ancien créneau 0:20 à 0:30 est un `*.close` nommé, dans la même enveloppe de chapitre. `STYLE.md` §8 et `QUESTIONS.md` disent la même durée. g06 est 0:27 de récapitulatif plus 0:08 de carte. | G1 vérifie qu’aucune carte affichée ne dépasse 10 s, en anglais et en français, quand les scripts existeront. Pas de voix dans ce correctif. |
| R3 | Pas de script. `PLAN.md`, section « Contrôles nommés, plus tard », liste R3-g03 à R3-x03. Les comparaisons de `g10.sample` ont deux repères successifs. `g11.e3` a `show` puis `caveat`. `g12.learn` est une carte de familles. x03 est marqué facultatif. | G1 et G2, cœur seul. Si une scène exige un prérequis absent ou deux fois son budget de mots, le point redevient bloquant. |
| R4 | `PLAN.md`, section « Obligations orales ». E1, E2, E3, rapport prospectif, paris. Les deux langues. | Script puis écoute du pilote. L’absence de voix n’est pas une clôture. |
| R5 | `LOTS.md`, pilote. La séquence ajoute `g10.card` (8 s) et le caveat oral de `g10.law`, sans animer tout g10. Le calque suit S19. Le pilote ne prouve pas g06 vers g08. | Capture du pilote, plus tard. Fichiers HTML non écrits ici. |
| R6 | `g02.disk` n’est pas une scène tant que §E est ouvert. Ses 0:15 sont dans `g02.stretch`, sans notion nouvelle. g02 reste 3:20. Si une source datée arrive, le stretch revient à 0:45 et le disque prend 0:15. | La source du disque manque toujours. Ne pas inventer de seuil. |

## Cohérence d’horloge trouvée en vérifiant

Les lignes de `g11` au commit `b3517f5` sommaient 3:10 alors que l’en-tête et l’horloge disaient 3:40. Les 0:30 manquantes sont maintenant dans `g11.e3` (1:20 au lieu de 0:50), pour dire la précision de S20 sans raccourcir le chapitre. Le cœur reste 41:00.

## Non corrigé dans ce passage

Réserves science S17, S26, S27 et S28. Elles n’étaient pas dans le mandat S18 à S25.

- S17. `g09.sizes` cite encore `digest.md:127` pour les 50 pas de Heun d’E2. Le digest ne le dit pas pour E2. La ligne qui le dit est `en/rapport/index.qmd:595`.
- S26. `x02.beltrami` dit encore que le test est tenu à Rm = 2. Le JSON vaut −0,500053, soit quelques 10⁻⁵ sous −0,5.
- S27. `g04.sim` ne répète pas Re = 1,5×10³ ni μr = 50 à côté de 90 ± 5 et 130 ± 10. `x04.bc` le fait.
- S28. L’inventaire dit encore « SW1 par 3 » pour 0,107 / 0,0333. Le quotient vaut 3,21. Le plan n’affiche pas ce facteur.

Faits externes du §E toujours sans source. Pas de narration, pas de scène, pas de Fish, pas de calcul.
