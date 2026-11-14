single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H6, after the twelve GPU points. At seed 0 the growth rate changes sign in (8, 9), (17, 18) and (26, 28), at n = 64 and n = 96, and final max_div_b stays below 1e-8.

Re-run. The pods were not started again. The inequalities were recomputed from the twelve JSON files in `experiments/results/cursor_abc/`. Every lambda is finite. The largest max_div_b is 9.923962863776048e-16, so the divergence clause holds. Signs:

- n = 64. lambda(8) = -0.008263401, lambda(9) = 0.0002858035, lambda(17) = 0.001143872, lambda(18) = 3.152835e-6, lambda(26) = -0.004083938, lambda(28) = -0.0006356954. lambda(18) is not negative. lambda(28) is not positive.
- n = 96. lambda(8) = -0.008377626, lambda(9) = 0.0004219442, lambda(17) = 0.0004629413, lambda(18) = -0.001579518, lambda(26) = 0.0004187395, lambda(28) = 0.007401556. lambda(26) is not negative.

Trace. The brackets were the digest crossings at lines 470, 472, 480, 482, 487 and 488 of `experiments/results/digest.md`, and the interpolated thresholds 8.87, 17.6 and 26.8 on line 492. CONFIRMED that the test applied those brackets and not a new ones chosen after the run.

Verdict. REFUTED. Three of the six sign pairs fail. The (8, 9) pair holds at both resolutions, and the (17, 18) pair holds at n = 96 only. A second campaign was not run.
