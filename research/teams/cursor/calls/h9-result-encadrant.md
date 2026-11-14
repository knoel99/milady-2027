single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H9, after the five n = 96 points. The five-seed mean at Rm = 12, cfl = 1 stays within 0.001 of 0.008127803049079646, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. Lambdas from `experiments/results/cursor_abc_n96/`: 0.008229370, 0.007742532, 0.007331631, 0.008767483, 0.008408345. All finite. The largest max_div_b is 4.919003199354413e-16. The mean is 0.008095872179936526. The absolute difference from the control is 3.193086914311978e-05, which is below 0.001.

Verdict. The refutation criterion is not met. The 0.001 bound was not moved after the run.
