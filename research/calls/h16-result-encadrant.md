single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H16, after seeds 5-9 at n = 128, Rm = 12, cfl = 1. Their mean stays within 0.001 of 0.007691065668965582, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n128_s5/`: 0.008666520, 0.009022376, 0.007353518, 0.007157869, 0.007715268. All finite. The largest max_div_b is 7.952441911505939e-16. The mean is 0.007983110084430346. The absolute difference from the control is 0.00029204441546476414, which is below 0.001.

Verdict. The refutation criterion is not met. The 0.001 bound was not moved after the run.
