single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H12, after the five n = 128 points. The five-seed mean at Rm = 12, cfl = 1 stays within 0.0005 of 0.008127803049079646, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n128/`: 0.009017586, 0.007115078, 0.007133687, 0.007770241, 0.007418736. All finite. The largest max_div_b is 4.986046417382597e-16. The mean is 0.007691065668965582. The absolute difference from the control is 0.0004367373801140639, which is below 0.0005.

Verdict. The refutation criterion is not met. The 0.0005 bound was not moved after the run.
