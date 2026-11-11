# Thèse — relecteur-ml (Fable)

Lue en entier (1240 lignes). Calculs à la main sur le digest ; rien exécuté.

## Bloquant
1. §2.3 l.513 : 0,77 (8 pas) / 0,82 (50 pas) absents du digest (≈ 0,75 à 50 pas).
2. §1.4 l.157, réf. l.1202 : Baldan et al. (2026, « ICLR 2026 ») absent des sources ; arXiv 2506.08604 ne donne aucun lieu de publication.
3. §4.2 l.992 vs §3.2 l.890 : « l'inclinaison n'a amélioré aucune loi » faux (E2 : 0,185 → 0,170, 0,345 → 0,182, 0,0839 → 0,073 quand l'ESS tient) ; contradiction avec la règle d'arrêt du palier 0 qui en fait le repli.
4. §2.7 l.852, l.828 : une dérive réduite estimée sur une loi générée non invariante hérite des identités seulement à hauteur des résidus de stationnarité.

## Important
5. Inclinaison : ESS 0,29 = moyenne sur 11 η ; en test 0,99 / 0,116 / 0,00215 / 0,002 / 0,002 ; condition de faisabilité (0 dans l'enveloppe convexe) absente de la Prop. 2.21 ; reg = 1.0 ; contrainte non satisfaite sur l'autre moitié. « corrigé en loi » plutôt qu'« imposé ».
6. Prop. 9 n'explique pas l'erreur d'E1 au seuil (masse du pont 0 → 0,0017, SW1 du modèle C 0,033) ; c'est Rice (fonctionnelle de la densité en D = 0) qui amplifie. Calculer J = W₁(μ_0,86, μ_0,865). Brief §3 même imprécision.
7. Prop. 2.35 : borne non triviale seulement pour δ < J/(2K), K exponentiel en L_x ; L_x non borné pour la cible (terme en 1/(1−t)). Énoncer la largeur, mesurer K.
8. Rice : pourcentages hors digest ; modèle C graine 0 ; 50-130 échantillons dans la fenêtre → bruit 10-15 %, donc 14 % ≈ plancher ; passages par zéro, pas renversements ; il faut F.
9. « flot projeté » : V3 projeté en float32 (2e-8 = précision simple), réentraîné avec bruit projeté ; V3 meilleur en test (1,85 ; 0,135 ; 0,236 ; 0,335), pire en entraînement (1,12 vs 1,03), une graine. Potentiels et flot projeté non départagés.
10. La pénalité d'E2 est un rapport ‖Ax̂₁‖²/‖x̂₁‖²_k (10·div_rel_t), pas celle de la Prop. 3 ; son gradient pousse l'amplitude (explique E_B 1,68, σ(D)/σ_ref 1,21).
11. Recalage : améliore ℰ (1,10 vs 2,62) et le spectre ; l'incohérence ne se lit que sur σ(D)/σ_ref ; descripteurs sans dissipation.
12. Gain de V5 surestimé : tiré par les deux plus grands η ; nul à η = 0,00476 ; pire que V4 à 4 η d'entraînement ; σ(D)/σ_ref 0,57 ; une graine. Meilleur argument : ⟨a²⟩ 0,43 → 0,061.
13. Distance d'énergie non définie (common.py renvoie D², V-statistique, biais en 1/n ; rééchantillonnage pondéré biais 1/ESS) ; rapports 4,6 brut vs ≈ 8 après retrait du plancher.
14. Plancher par sous-échantillon = celui que la page juge optimiste (0,0018 vs 0,030) ; bootstrap par blocs pour séries corrélées.
15. Protocole : aucun jeu n'isole le gain en λ ; pas de jeu d'extrapolation ; pas de validation pour les hyperparamètres (β = 20, 50) ; deux Pm ; palier 3 sans test de mémorisation.
16. Graines (3) insuffisantes ; budget sans le facteur graines ; 128³ à 1200 h contredit H1-H2 (≈ 2300 h).
17. Critères non discriminants ou circulaires (asymétrie acquise par construction ; facteur 2 déjà atteint dans le bruit ; critère sur l'identité optimisée ; 1e-12 hors de portée en float32).
18. Seuil déduit du générateur non défini ; δ₀ sous le seuil ; intervalle poissonien infalsifiable ; ν_a borne, pas estimateur.
19. Prop. 2.41 : symétrique ≠ bimodal ; « exact » trompeur ; 3D-Var = mode ; min de J(z) ≠ MAP en x.
20. §2.4 l.629 : conséquence de (i), pas de (iii).
21. DRESDYN : champ moyen déterministe (régression suffit) ; taux cinématique dépend des corrélations temporelles.

## Mineur
22. Prop. 2.10 : (c)(d) omis, « en général » perdu ; brief (c)(d) imprécis (Euler exact).
23. Prop. 2.3 (ii) : équivalence en norme H¹.
24. Revendication 5 (demi-lots) classique ; vérifier Cai et al. 2026.
25. Rem. 2.26 : A vs C dans le bruit ; plancher d'asymétrie 0,004 hors digest.

Bilan : fidèle au brief sans contradiction (écarts : Prop. 2 (c)(d), « en général ») ; brief à corriger (Prop. 2 (c)(d), E1 ↔ Prop. 9, revendication 5) ; protocole à durcir (constats 13-18) avant de pouvoir conclure sur les critères chiffrés.
