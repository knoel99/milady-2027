# Parcours — apprenant (Sonnet)

Lecture ciblée (objectifs, prérequis, plans, définitions, récapitulatifs, recherches par mots-clés), pas des 16 000 lignes.

C1 (le plus grave). Niveau de départ annoncé L1, exigé L2 dès P2/P5/P3/P4 : équations différentielles linéaires, changement de variables (jacobien), séries de Fourier, diagonalisation ; aucun module ne les enseigne.

P1 (20 h annoncées, 35-40 h estimées) : intégrales de surface et de volume hors L1 ; Fourier azimutal au ch. 1 avant le ch. 5 ; induction, η, Rm, ABC avant P3 ; L², Neumann non définis ; doublons Leray (P1 ch. 6 / P2 th. 2.4 / P8 §3.1) et potentiels (P1 ch. 4 / P6 prop. 6.11-6.12).
P2 (25 h, 38-45 h) : multiplicateur de Lagrange ; tenseurs, ⊗, probabilités, ergodicité avant P5 ; Cauchy–Lipschitz, difféomorphisme avant P4 ; η en collision avec P3 ; S6-S7 surchargées.
P5 (25 h, 40 h) : construction générale (tribu, boréliens) sans probabilités préalables ; jacobien non enseigné ; ch. 4-6 : décrochage (I-projection, Wasserstein, MMD, EDS, Itô, Fokker–Planck, flow matching en 3 h par séance) ; redites avec P7 (prop. 6.15, flots normalisants), P4 (Fokker–Planck), P8 (I-projection).
P3 (30 h, 45-50 h) : BLOQUANT : « Rappels » d'électromagnétisme jamais vu ; Bessel et harmoniques sphériques ; bifurcations de P4 utilisées avant ; Gissinger traité en P3 §7.2 et en P4 ch. 7 ; résidus à l'ex. 14.
P4 (25 h, 35 h) : fin ch. 5 et ch. 6 surchargés (Krylov–Bogoliubov, Birkhoff, SRB, Kramers, Rice, Dirac) ; identités de stationnarité reprises à l'identique en P8 prop. 6.3.
P6 (30 h, 40 h) : convexité forte, L-lipschitz, groupes ; doublons avec P1 et P8 ; ch. 5 : ELBO et β-VAE avant de savoir ce qu'est un modèle génératif.
P7 (30 h, 50 h) : redites avec P5 et P8 (Jensen) ; DDPM → EDS → ODE → score → EDM en trois séances (M1).
P8 (30 h, 45 h) : topologie (Betti, persistance, bottleneck, Morse, Poincaré–Hopf) jamais préparée ; DPS traité deux fois ; ch. 8 (5 articles) en 4 h irréaliste.

Total : 215 h annoncées, 330-360 h estimées (22-24 semaines à 15 h, contre 16).

Ordre : globalement bon ; variante conseillée 1, 2, 5, 4, 3, 6, 7, 8 (P4 avant P3 : bifurcations et Gissinger). Garder les numéros des dossiers (identifiants stables, liens du site, de l'anglais, du rapport, de la thèse, des specs) ; ajouter une colonne « ordre de lecture » au tableau #modules.

Manques pour le but final : lecture critique d'un article (apport, protocoles, baselines) ; entraînement de bout en bout d'un flow matching conditionnel sur des champs 2D/3D (U-Net ou FNO, GPU, normalisation, EMA, points de reprise) ; production d'un jeu de données MHD ; domaines à parois et maillages ; turbulence MHD (Elsasser, Iroshnikov–Kraichnan, Goldreich–Sridhar) ; introduction à l'électromagnétisme et compléments L2 ; reproductibilité et cluster ; protocole statistique de comparaison de modèles.
