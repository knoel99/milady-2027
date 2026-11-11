# Rapport — relecteur-ml (Fable)

Lu en entier sauf références. Points de contrôle sans problème : « 100 évaluations » correct (l.601) ; interpolation dite comme telle ; V-statistique documentée (l.721-723) ; Jensen et contrainte en loi bien distingués (Prop. 3, l.121, 181) ; biais attribué à DPS (l.187) ; demi-lots implémentés ; tableaux 1-8 conformes au digest.

## Bloquant
1. Prop. 2 (d) (l.360, 371, repris l.377, 1023 ; brief l.30) : faux (Euler aligné exact) ; seul vrai problème : correcteur de Heun en t = 1 (common.py l.117-123), résidu ≈ h/2 ≈ 1 %, pas 0,41 ; divergence de V0 = défaut de représentation. Corriger brief, rapport, thèse.
2. Légende fig. 10 l.1019 « seule la perte de stationnarité réduit à la fois le résidu et la distance » contredite (recalage : 0,47 → 8,27e-6, 2,62 → 1,1 ; 0,422 vs 0,863 en entraînement). « …sans écraser σ(D) ».
3. Hors digest : 0,7 % en D < 0 (l.871) ; vérification de l'inclinaison sur la moitié a sans chiffre (l.879) ; sorties --quick citées (l.124) ; « erreur moyenne 17 % » (l.883). Rice 4, 6, 14, 42, 32, 23, 65 % recalculés cohérents mais à produire par digest.py.

## Important
4. P1 l.1135, l.1031 : « interpole correctement » contredit (V4 : 1,03 / 3,63 / 7,74 en test vs voisins 0,08-3,97 ; moyennes 2,58 test vs 1,03 entraînement) ; l'erreur dominante est l'interpolation, que V5 corrige.
5. Prop. 9 invoquée pour E1 (l.68, 78, 883, 896, 1135, contribution 6, tableau l.1171) sans saut J > 0 ; seuil entre deux Γ d'entraînement, une graine.
6. Inclinaison « exacte en loi » (l.1157, 1139, 68, légende 2 d) : ESS = 1 à 3 η de test sur 5 ; le résidu réduit est celui d'un échantillon sélectionné (σ(D)/σ_ref = 0,204) ; 0,29 = moyenne sur 11 η (0,22 en test).
7. Distance d'énergie des nuages inclinés : rééchantillonnage avec doublons + V-statistique → plancher en 1/ESS ; hausse en partie artefact.
8. « estimée sans biais, n'écrase pas la variance » (l.1031, 1139, 1199) : faux aux η d'entraînement (0,666 → 0,568) et dans E1 (1,04 → 0,75).
9. Résidu de ⟨a²⟩ pas indépendant (contient 2ηE_B).
10. Contribution 5 (demi-lots) classique (double échantillonnage Bellman, U-statistique MMD²), sans comparaison dans le digest.
11. « flot projeté » (Prop. 2 (b)) ≠ V3 (flot dans S) ; (b) ne couvre pas V3 et E2 ne teste pas (b).
12. Écarts au brief : Prop. 2 (c), Cor. 6, Prop. 7, 8, 9 ; versions du rapport plus rigoureuses sauf (d) : aligner le brief puis la thèse. Brief faux/imprécis : (d) et fin de (c), Prop. 9 (intervalle), C2 « (PCFM, ECI) », « dès 0,8625 » (0,865).
13. Nombre de graines absent des synthèses (E2 : 1 ; E1 : 2 ; Rice : graine 0) ; gain « divisé par deux » de F (2,0-2,4) exactement au seuil fixé l.901.
14. Nouveauté adossée à une entrée [NON CONFIRMÉ] (donnees-metriques.md l.513) ; six revendications, veille non documentée pour 3, 5, 6.
15. E1 inclinaison l.879 : moyenne dominée par Γ = 0,83 ; ESS/N 0,82 ≠ « quelques échantillons » ; « queues lourdes » = hypothèse.
16. ECI classé C2 (projection non linéaire) l.314 et brief l.17 : contredit litterature.md (C1, linéaire).

## Mineur
17. Résumé « divise par 4,6 » sans référence ; B divise déjà par 3,3.
18. Ex. 4.2 : pénalité par échantillon de poids 1/n.
19. « Fourier tronquée = POD » : E2 ne réduit rien ; rotation ψ/a dès que H_C ≠ 0.
20. Légende 2 e : ensemble climatologique, perspective.
21. Cor. 6 l.449 : Var > 0 n'exclut pas un atome.
22. l.883 « validation de la Prop. 8 » : h fixé.
23. « Cheng et al. 2025 » = deux équipes (S. Cheng TorchDA, C. Cheng ECI) : ne pas attribuer ECI à l'encadrant.
24. Csiszár 1975 [NON CONFIRMÉ] (l.220, glossaire) : renvoyer à la Prop. 7.

Bilan : trois bloquants (Prop. 2 (d), légende fig. 10, mesures hors digest) ; lectures d'E1/E2 trop favorables ; graines tues ; le brief est à réaligner sur le rapport.
