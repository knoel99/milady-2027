single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H17, after the five cfl = 0.5 points at n = 128. The five-seed mean stays within 0.002 of 0.007691065668965582, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n128_cfl05/`: 0.009017586147426314, 0.007115078374217372, 0.007133687033050278, 0.00777024117608828, 0.007418735609609641. All finite. The largest max_div_b is 4.815705908852919e-16. The mean is 0.007691065668078377. The absolute difference from the cfl = 1 control is 8.872052398301022e-13, which is below 0.002.

Verdict. The refutation criterion is not met. The 0.002 bound was not moved after the run.
