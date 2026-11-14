single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H18, after the five n = 160 points. The five-seed mean stays within 0.001 of 0.007837087876697964, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n160/`: 0.008647848, 0.007458429, 0.007834113, 0.008695044, 0.008795699. All finite. The largest max_div_b is 5.016311482458478e-16. The mean is 0.008286226691078903. The absolute difference from the control is 0.0004491388143809394, which is below 0.001.

Verdict. The refutation criterion is not met. The 0.001 bound was not moved after the run.
