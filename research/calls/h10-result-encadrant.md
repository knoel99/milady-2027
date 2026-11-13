single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H10, after seeds 1-4 of the (8, 9) bracket. lambda(8) < 0 < lambda(9) at n = 64 and n = 96, and every point is finite with final max_div_b below 1e-8.

Re-run. The pod was not started again. The sixteen files in `experiments/results/cursor_abc_sign89/` were read. Every lambda is finite. The largest max_div_b is 5.270254732213699e-16. lambda(8) is negative at all eight points. lambda(9) is positive at all four n = 96 seeds and at n = 64 seeds 2 and 3. At n = 64, seed 1 has lambda(9) = -3.775685e-4 and seed 4 has lambda(9) = -3.276007e-4.

Verdict. REFUTED. Two of the sixteen sign conditions fail. The rule was not changed after the run.
