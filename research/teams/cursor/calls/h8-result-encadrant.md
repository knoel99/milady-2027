single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H8, after the five cfl = 0.5 points. At n = 64 and Rm = 12 the five-seed mean stays within 0.002 of the cfl = 1 control mean 0.008127803049079646, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. The five JSON files in `experiments/results/cursor_abc_cfl05/` were read. Lambdas: 0.007711343, 0.007720344, 0.007940879, 0.008459742, 0.007190694. All finite. The largest max_div_b is 5.62760495599137e-16. The mean is 0.007804600426952867. The absolute difference from the control is 0.0003232026221267788, which is below 0.002.

Verdict. The refutation criterion is not met. The 0.002 bound was not moved after the run. This is not a 3D generator result.
