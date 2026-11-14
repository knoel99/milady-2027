single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H7, after the twenty GPU points. At n = 32 and n = 48 the dynamic energy budget holds for Taylor-Green kf = 1 and ABC kf = 2, on seed 1 and on seeds 2, 3, 4 and 5. Bounds: rhs_abs_min > 0.05, rel_max < 0.01, scale_max < 1e-3, residuals finite.

Re-run. The pod was not started again. The twenty JSON files in `experiments/results/cursor_energy/` were read. Every residual is finite. The largest rel_max is 1.578970246318361e-4. The largest scale_max is 3.364142627466731e-5. Both stay inside their bounds.

The failure. `n32_abc_kf2_s2.json` has rhs_abs_min 0.024927235243765333, which is not above 0.05. The other nineteen points have rhs_abs_min above 0.05.

Verdict. REFUTED. One pre-set inequality fails. The 0.05 bound was not moved after the run.
