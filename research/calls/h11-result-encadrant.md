single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H11, after the ten 1000-step points. At n = 64, rel_max < 0.01 and scale_max < 1e-3 for both forcings and seeds 1 to 5, and every residual is finite.

Re-run. The pod was not started again. The files in `experiments/results/cursor_energy_long/` were read. Every residual is finite. The largest scale_max is 3.462754598992323e-05, under 1e-3. rel_max exceeds 0.01 for ABC seed 1 (0.012180143), seed 3 (0.358329596) and seed 4 (0.016123789). Seed 3 has rhs_abs_min 6.414980609992238e-06. The five Taylor-Green points stay under 0.01.

Verdict. REFUTED. Three pre-set relative residuals fail. The 0.01 bound was not moved after the run.
