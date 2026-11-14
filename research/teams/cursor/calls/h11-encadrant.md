single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H11, before the 1000-step energy runs. At n = 64, rel_max < 0.01 and scale_max < 1e-3 for Taylor-Green kf = 1 and ABC kf = 2, seeds 1 to 5, and every residual is finite.

Protocol check. Those two bounds are the ones in `test_energy_budget`. H7 was refuted by rhs_abs_min, and this claim does not reuse that threshold. The length is 1000 steps, not the 60 steps of the test. No n = 64 residual at this length exists yet.

Verdict. UNCHECKED. The protocol can be run.
