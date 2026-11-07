# Faits — figure « simulations »

| Libellé (FR / EN) | Source |
|---|---|
| « Système », « Schéma numérique », « Balayage du paramètre », « Données et chaîne » / « System », « Numerical scheme », « Parameter sweep », « Data and pipeline » | en-têtes de colonnes |
| « E1 », « Gissinger, 3 modes » | experiences/e1_gissinger.py, en-tête (modèle (Q, D, V) de Gissinger 2012) |
| « E2 », « MHD 2D forcée » / « forced 2D MHD » | experiences/mhd2d.py, e2_donnees.py |
| « E3 », « dynamo ABC » / « ABC dynamo » | experiences/e3_abc.py |
| « D », « t » (vignette E1) | plan-these/figure/data/plan_data.json (série D(t), Γ = 0,9) |
| vignette E2 (j et isolignes de a) | plan_data.json (`mhd2d`) |
| vignette E3 (|B| sur trois faces, Rm = 12) | plan_data.json (`abc`) |
| « RK4, Δt = 0,01 », « transitoire 300 » / « RK4, Δt = 0.01 », « transient 300 » | e1_gissinger.py `simulate(…, t_burn=300, …, dt=0.01)` |
| « pseudo-spectral 32² », « forçage blanc, Δt = 0,01 » / « white forcing, Δt = 0.01 » | e2_donnees.py (N = 32, dt = 1e-2) ; mhd2d.py (forçage blanc en temps) |
| « pseudo-spectral 32³ », « RK4 à facteur intégrant » / « integrating-factor RK4 » | e3_abc.py (n = 32, « RK4 à facteur intégrant pour la diffusion ») |
| « passages de D par 0 » / « zero crossings of D » ; courbe | e1_gissinger.json `grille_fine[*].taux_simulation` (41 valeurs de Γ, 0,80 à 1,00) |
| « seuil » / « threshold » (bande 0,86–0,865) | grille fine : taux nul jusqu'à 0,86, 0,00194 à 0,865 |
| « Γ », « 0,80 », « 0,90 », « 1,00 » (EN « 0.80 », « 0.90 », « 1.00 ») ; points pleins (11) et vides (10) | e1_gissinger.json `config.G_train`, `config.G_test` |
| « E_B » (affiché « EB ») ; courbe et bande (moyenne ± écart-type) | **recalcul** : make_data.py (solveur et réglages de E2, graines 300 + i) ; sim_data.json `e2.points` |
| « η », « 0,004 », « 0,008 », « 0,016 » (EN « 0.004 », « 0.008 », « 0.016 ») ; points pleins (6) et vides (5) | e2_donnees.py `ETA_TRAIN`, `ETA_TEST` |
| « λ », « 0 », « Rm », « 0 », « 10 », « 20 », « 30 » ; courbe, flèches hors échelle (Rm = 2, 4, 6) | e3_abc.json `taux` (24 valeurs de Rm) |
| « 8,87 », « 17,6 », « 26,8 » / « 8.87 », « 17.6 », « 26.8 » ; fenêtres teintées | e3_abc.json `seuils_interpoles` |
| « 16 trajectoires × 1 500 », « états par Γ » / « 16 trajectories × 1,500 », « states per Γ » | e1_gissinger.py : n_traj = 16, t_keep = 3000, every = 2 → 1 500 états par trajectoire |
| « 16 membres × 150 », « instantanés par η » / « 16 members × 150 », « snapshots per η » | e2_donnees.py : batch = 16, n_tr = 150 (référence : 75) |
| « λ(Rm) et », « modes propres de B » / « λ(Rm) and », « B eigenmodes » | e3_abc.py (sorties e3_abc.json, e3_modes.npz) |
| « script autonome » / « standalone script » | E1 n'a pas de campagne dans infra/configs |
| « → palier1_mhd2d » | infra/configs/palier1_mhd2d.yaml (« MHD 2D forcée (E2) », code `mhd2d_numpy`) |
| « → palier2_abc3d » | infra/configs/palier2_abc3d.yaml (dynamo cinématique ABC 1:1:1, 64³, Rm 4–40) |
| « entraînement (E1, E2) », « test » / « training (E1, E2) », « test » | légende des points |
