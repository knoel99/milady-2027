# Faits — figure « solveur »

| Libellé (FR / EN) | Source |
|---|---|
| équations « ∂t u = u × ω + j × B − ∇Π + ν∇²u + f », « ∂t B = ∇ × (u × B) + η∇²B » | src/milady/sim/mhd3d.py l. 4-7 |
| « Espace de Fourier » / « Fourier space » ; « Espace physique » / « Physical space » | mhd3d.py l. 19-24 (état = coefficients de Fourier ; termes non linéaires en espace physique) |
| « û, B̂ », forme « (n_traj, 3, 64, 64, 33) » | mhd3d.py l. 19-20 (n_traj, 3, nx, ny, nz//2+1) ; palier2_tg3d.yaml N = 64 |
| « ik× » (rotationnels ω̂ = ik×û, ĵ = ik×B̂) | mhd3d.py `_rhs` l. 496-498 (`self._curl`) |
| « irfftn », « rfftn » | mhd3d.py l. 419-422 (`torch.fft.rfftn`, `torch.fft.irfftn`) |
| « u × ω + j × B », « u × B » | mhd3d.py `_rhs` l. 499, 503 |
| « désaliasage 2/3 » / « 2/3 dealiasing », « |m| ≤ 21 » | mhd3d.py l. 21-24 (cube |m_i| ≤ (n_i − 1)//3 ; 63//3 = 21 à 64³) ; `* self.mask` l. 499, 504 |
| « projection de Leray » / « Leray projection », « P = I − kkᵀ/|k|² » | mhd3d.py l. 25-26, `_project` l. 435 ; appliquée au terme de quantité de mouvement l. 499 |
| « ik × (u × B) » : second membre de B solénoïdal par construction | mhd3d.py l. 504 (`self._curl(self._fft(e) * self.mask)`) |
| « + f » (forçage constant ABC ou TG) | mhd3d.py l. 500-501 |
| « RK4 de Lawson » / « Lawson RK4 », « e^{−νk²Δt} », « e^{−ηk²Δt} », « ×4 » | mhd3d.py `_factors` l. 507-519, `step` l. 521-545 (quatre appels à `_rhs`) |
| « forçage aléatoire » / « random forcing », « √(2εΔt) ξ » | mhd3d.py l. 27-29, `_random_kick` |
| « nettoyage : projection de û et B̂ » / « clean-up » | mhd3d.py l. 547-552 (`project_every`) |
| « diagnostics (Parseval) » | mhd3d.py l. 31-36 |
| « mise en régime » / « burn-in » 100 ; « fenêtre gardée » / « kept window » 40 ; « 40 instantanés » / « 40 snapshots » ; « diagnostics tous les 0,1 » | palier2_tg3d.yaml runtime (t_burn 100, t_keep 40, every 1, diag_every 0.1) ; src/milady/sim/run.py, en-tête étape 3 |
| « point de contrôle .npz » / « .npz checkpoint », « toutes les 900 s » / « every 900 s » | run.py, en-tête étape 3 ; palier2_tg3d.yaml `checkpoint_every_s: 900` |
| « SIGTERM », « reprise » / « resume » | run.py, en-tête étape 3 ; infra/slurm/gen_data.sbatch `--signal=TERM@120` |
| « queued », « running », « done », « failed » | src/milady/sweep.py, en-tête ; run.py étapes 2, 5 et « En cas d'erreur » |
| fichier : attributs racine `dataset_name`, `grid_type`, `n_spatial_dims`, `n_trajectories`, `simulation_parameters` ; `milady_uuid`, `milady_parameters`, `milady_git_commit` ; groupes `dimensions/`, `boundary_conditions/`, `scalars/`, `t1_fields/` (`velocity`, `magnetic_field`), `milady_diagnostics/`, `milady_spectral/` | src/milady/data/format.py, en-tête ; calcul/index.qmd l. 102-113 |
| catalogue : `simulation` (`id`, `parameters`, `git_commit`, `status`, `wall_time_s`), `file` (`uri`, `sha256`, `size_bytes`, `n_t`), `diagnostic` (`name`, `t`, `value`), `job` (`scheduler`, `external_id`, `status`) | src/milady/catalog/models.py (classes Simulation, File, Diagnostic, Job) ; run.py étapes 2 et 5 |
| correspondances `milady_uuid` → `simulation.id`, `milady_parameters` → `simulation.parameters`, `milady_diagnostics/` → `diagnostic` | src/milady/catalog/api.py `ingest_mff` l. 700-721 ; docs/ARCHITECTURE.md § 4 |

## Libellés exacts affichés (FR / EN)

| FR | EN | Source |
|---|---|---|
| « Un pas de temps » | « One time step » | titre du panneau a |
| « Une simulation dans le temps » | « One simulation over time » | titre du panneau b |
| « Ce qui est écrit » | « What is written » | titre du panneau c |
| « u, B, ω, j », « grille 64³ » | « u, B, ω, j », « 64³ grid » | mhd3d.py `_rhs` (u, ω = ∇×u, j = ∇×B, B en espace physique) ; palier2_tg3d.yaml N = 64 |
| « ik × ( · ) » | idem | mhd3d.py l. 504 (rotationnel de la transformée de u × B) |
| « 4 évaluations par pas » | « 4 evaluations per step » | mhd3d.py `step` (k1…k4) ; BENCHMARK_NOTES (« un pas RK4 = 4 évaluations du second membre ») |
| « e−νk²Δt », « e−ηk²Δt » (exposants) | idem | mhd3d.py `_factors` l. 507-519 |
| « N̂u + f̂ », « N̂B » | idem | mhd3d.py `_rhs` : `nu_h` (+ `f_hat`), `nb_h` |
| « puis : forçage aléatoire, projection périodique » | « then: random forcing, periodic projection » | mhd3d.py `step` l. 541-552 (`_random_kick`, `project_every`) |
| « diagnostics tous les 0,1 » | « diagnostics every 0.1 » | palier2_tg3d.yaml `diag_every: 0.1` |
| « 40 instantanés (u, B) » | « 40 snapshots (u, B) » | palier2_tg3d.yaml `t_keep: 40`, `every: 1.0` |
| « mise en régime », « fenêtre gardée » | « burn-in », « kept window » | palier2_tg3d.yaml `t_burn: 100`, `t_keep: 40` ; run.py étape 3 |
| « point de contrôle (toutes les 900 s de calcul) » | « checkpoint (every 900 s of compute) » | palier2_tg3d.yaml `checkpoint_every_s: 900` |
| « SIGTERM : point de contrôle, puis reprise » | « SIGTERM: checkpoint, then resume » | run.py étape 3 ; gen_data.sbatch `--signal=TERM@120` |
| « reprise » | « resume » | run.py étape 3 (« reprise automatique au lancement suivant ») |
| « en gris : convention The Well » | « in grey: The Well convention » | format.py, en-tête |
| « fields.h5 », « dataset_name, grid_type, … », « dimensions/ », « boundary_conditions/ », « t1_fields/ », « velocity, magnetic_field », « milady_uuid », « milady_parameters », « milady_git_commit », « milady_diagnostics/ », « milady_spectral/ » | idem | format.py, en-tête ; calcul/index.qmd l. 102-113 |
| « file », « uri », « sha256 », « size_bytes », « n_t » ; « simulation », « id », « parameters », « git_commit », « status » ; « diagnostic », « name », « t », « value » | idem | src/milady/catalog/models.py |
| « 0 », « 100 », « 140 », « t » | idem | palier2_tg3d.yaml (t_burn + t_keep = 140) |
| « queued », « running », « done » | idem | sweep.py, run.py |
| « k » | idem | variable d'onde |
