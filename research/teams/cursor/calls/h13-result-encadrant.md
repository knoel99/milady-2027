single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H13, after the five cfl = 0.5 points at n = 96. The five-seed mean stays within 0.002 of 0.008095872179936526, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n96_cfl05/`: 0.008229370001128933, 0.00774253163556308, 0.007331630775539529, 0.008767483001384512, 0.008408345474516105. All finite. The largest max_div_b is 5.582656921038302e-16. The mean is 0.008095872177626431. The absolute difference from the cfl = 1 control is 2.3100948237653185e-12, which is below 0.002.

Verdict. The refutation criterion is not met. The 0.002 bound was not moved after the run.
