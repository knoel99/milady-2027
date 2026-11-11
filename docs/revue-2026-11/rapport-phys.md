# Rapport — relecteur-physicien (Fable)

Chiffres dérivés recalculés depuis le digest.

## Bloquant
1. Prop. 2 (d) et preuve l.360, 371 (repris l.377, 1023) : faux, dans le rapport et dans le brief. y' = −y/(1−t) a une solution affine ; Euler aligné sur t = 1 est exact (produit télescopique). Vrai : correcteur de Heun en t = 1 (0/0) ; grille non alignée instable si 1 − t_n < h/2 ; erreur bornée r laisse h·r(t_{N−1}). L'intégrateur n'explique pas la divergence 0,41 de V0 (aucun essai à nombre de pas variable). Réécrire dans le brief puis le rapport ; attribuer V0 au point (c), comme hypothèse.
2. Prop. 9 dite confirmée par E1 (l.68, 78, 883, 896, 1135, contribution 6 l.125) alors qu'elle suppose un saut J > 0 en W₁ ; la loi symétrisée varie continûment (l.564 ; masse du pont 0,00167 à Γ = 0,865, J ≈ 0). « montée raide », « compatible avec l'esprit de la Prop. 9 ».

## Important
3. « fréquence des renversements » vs passages de D par zéro (l.68, 122, 510 titre Prop. 8, 1143, 1201) ; indice : 74 renversements (≈ 0,0038) vs 0,0044-0,0047 passages.
4. Pourcentages de Rice (4, 6, 14, 17, 23, 32, 42, 65 %) absents du digest (4, 14, 32, 42, 65 recalculés exacts) ; un modèle, graine 0, dit seulement l.883.
5. « crise » en Γ affirmée (l.901, 1359, glossaire, brief §3).
6. « chaotique » sur toute la plage de E1 (l.528) : publié seulement à Γ = 0,9.
7. Cor. 6 : « loi étrangère, KL infinie » ne discrimine rien en E1 (mesure physique singulière) ; s'appuyer sur la borne W₁ et la variance annulée ; KL vaut pour E2.
8. Contribution 3 « aucune antériorité » : théorie de l'état de transition, facteur de Bennett–Chandler (à vérifier sur source primaire, absent de litterature.md).
9. E3 : croisement de modes publié Rm₁ ∈ [24,05 ; 24,10] (Bouya & Dormy 2013) ; 150 unités trop courtes ; modes de e3_modes.npz à Rm ≥ 20 non convergés ; 3e seuil 26,8 (λ) vs ≈ 26,1 (λ_q).
10. E3 « test exact » à Rm = 2 ne teste que la diffusion ; vrai test : B = u.
11. Prop. 9 « de part et d'autre des seuils » d'E3 mal posé : la discontinuité est au croisement de modes (Rm ≈ 24).
12. Seuil VKS 31 seul (l.141) : 31 ou 35 selon l'ajustement.
13. Prop. 2 (c) ≠ brief ; « est donc d'ordre un » ne découle pas de la borne.
14. « confirme la Remarque 3.7 » : écart 0,005 < dispersion entre graines (0,0039) ; 7 Γ de test sur 10 au-dessus du seuil.
15. Chiffres hors digest (0,7 % en D < 0, vérification de l'inclinaison sans chiffre, liste des six modèles) ; le rapport s'autorise « ou des fichiers JSON ».

## Mineur
16. Écarts rédactionnels au brief (Prop. 1, 4, Cor. 6, Prop. 8, 9) : le rapport est souvent plus rigoureux, c'est le brief qu'il faut corriger. Brief §3 : « dès 0,8625 » absent du digest ; « seuil Rm_c » au singulier.
17. l.137 : seuil nécessaire, pas suffisant (fenêtre sans dynamo 17,6-26,8).
18. E3 : seuils à trois chiffres sans incertitude dans le résumé ; N = 48 ne couvre pas Rm 26-30 ; un seul champ initial.
19. Notations : λ (contrôle, taux, Lyapunov) → γ pour le taux ; μ, ν ; ε ; Σ vs σ.
20. Monômes à résidu nul par symétrie mêlés aux autres dans les moyennes « Liouville ».
21. Rice en MHD suppose μ_r, σ_r uniformes.
22. Pour relecteur-ml : preuves Props 3 et 7, contribution 5, divergence de V0, 8 vs 50 pas, inclinaison régularisée.

Bilan : physique publiée et chiffres des tableaux conformes ; à corriger avant diffusion : Prop. 2 (d) (brief et rapport) et Prop. 9 dite confirmée ; statuts trop affirmatifs ailleurs.
