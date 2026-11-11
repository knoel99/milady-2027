# Thèse — relecteur-physicien (Fable)

Lue l.1-1060 (frise SVG et bibliographie non relues). Aucune source externe.

## Bloquant
1. §2.3 l.513 : σ(dE/dt)/σ_ref 0,77 (8 pas) vs 0,82 (50 pas) absents du digest (enveloppe 0,699-0,796, moyenne ≈ 0,75).
2. §1.2 E1 l.88, §4.3 l.1006 : « saut de la loi » au seuil non mesuré (taux 0 → 0,0019 compatible avec saut ou pente infinie) ; seuil en Γ mesuré ici, non publié, 16 trajectoires de 3000 (taux < 2e-5 non exclus). Brief §3 ligne E1 : « crise de fusion… dès 0,8625 » non étayé (0,8625 absent du digest, grille à 0,005).
3. l.1006, l.66, l.158 : passages de D par zéro présentés comme renversements (l.680 le dit pourtant) ; même ambiguïté dans le brief (titre Prop. 8, revendication 3).

## Important
4. Pourcentages de Rice (4-6 %, 14 %, 65 %, 42 %) absents du digest ; grille fine = modèle C graine 0.
5. E1 : nombre de graines (2) non dit.
6. E3 : seuils 8,87 ; 17,6 ; 26,8 non convergés (≈ 8,90 ; 17,46 ; 26,1 avec l'autre estimateur) ; « compatible avec » plutôt que « retrouve ». Brief : « seuil Rm_c » au singulier.
7. Palier 3 : Ḋ sur champs filtrés omet la f.é.m. sous-filtre (effet α) ; Rice biaisée. Calculer ℓ(F) à pleine résolution.
8. Déf. 2.27 : dipôle défini sur B, mode POD de H ; μ_r variable dans le temps.
9. §3.5 : raccord au vide et pli appliqués aux données LATU (périodiques, μ_r lissé) ; critère (c) sans référence.
10. §3.5 (d) : intervalle poissonien inadapté (renversements périodiques, peu d'événements) ; ~100 renversements pour 10 %.
11. Pont de Rice : quelques à une centaine d'instantanés sur 2000 ; risque et condition d'arrêt.
12. Kazantsev en phase linéaire : pas stationnaire, pas de gamme d'échelles à 64³.
13. Taylor–Green à 64³ : Pm = 0,3 demande 256³ ; deux Pm insuffisants ; 10 % = incertitude des seuils de référence.
14. Rm grandeur de réponse (Ponty 2005) ; conditionner par les paramètres de contrôle.
15. ABC en MHD complète : seuils cinématiques valables seulement si l'écoulement reste laminaire.
16. Trois définitions de Re et Rm (SFEMaNS, Bousquet, Kreuzahler) non comparables ; disponibilité des séries saturées non établie.
17. Perte de stationnarité en domaine borné : bilans à dériver pour chaque code.
18. VKS : 0,77 n'est pas 1/2 ; seuil 31 à 35 selon l'ajustement.
19. Rem. 2.26 : poids ½ vrai en simulation, pas dans l'expérience (T+ = 120 s, T− = 50 s).
20. Cor. 2.16 (et brief, Cor. 6) : Var > 0 n'implique pas une densité ; mélange avec l'état éteint.

## Mineur
21. Partie théorique : ne contredit pas le brief mais pas à l'identique (Prop. 1 → 2.3, 2 → 2.10 sans (c)(d), Cor. 6 → 2.16, Prop. 7 → 2.21 c = 0, Prop. 8 → 2.29 hypothèses changées, Prop. 9 scindée en 2.34-2.36). Tableau de correspondance ou remonter dans le brief. Brief fragile : « Fourier tronquée = POD » (ligne E2).
22. Prop. 2.6 (iii) : pales à arêtes vives ; cylindre fini pas C^{1,1}.
23. Déf. 2.11 : α sur B et forçage g nuls aux paliers 2-4.
24. Notations Γ, λ, μ, ν ; Ponty 2007a/b ; Woltjer 1958 vs 1960 ; coquille l.908.
25. « may be offered » absent de encadrants.md ; palier 4 = régression ; palier 0 DQVU à vérifier ; 5 % demande ~400 passages ; Pm ≈ 1/3 vs 1e-5.

Bilan : trois bloquants de statut, aucun dans les démonstrations ; faits publiés conformes ; paliers 0-2 réalistes (Pm ∈ [0,5 ; 1] à 64³), palier 3 sous-spécifié.
