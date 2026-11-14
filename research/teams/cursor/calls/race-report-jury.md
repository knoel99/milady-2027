single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| H141, seeds 2 and 4 negative at n=136, Rm=9 | race report, Measured | CONFIRMED | experiments/results/cursor_abc_n136_rm9, most negative lambda -3.971e-4 | None for this claim |
| H143, seed 9 negative at Rm=9.056640625 | race report, Measured | CONFIRMED | experiments/results/cursor_abc_n128_rm9056640625_s5, lambda -5.351e-6 | None for this claim |
| H145, constraint divergence 1.56e-8 against baseline 0.645 | race report, Measured | CONFIRMED | cursor_constraint_cmp.json, reproduced by a second run | Say the grid is n=16. The report already does |
| H146, energy-distance ratio 757.56 | race report, Measured | CONFIRMED | same file, mean of the five ratios | Do not describe this model as meeting C1 |
| C5 still the sentinel | race report, Remaining | CONFIRMED | cursor_objectives.py --metric c5 prints 1.0, and src/ has no Haynes-Parnell count | Implement the count before quoting C5 |
| The race is not finished | race report, Status | CONFIRMED | spend near 21 USD of 150, site/teams/cursor is absent, H138 and H144 were in flight when the report was written | Build the deliverables only when the measurements they would show exist |

Pre-defence. The divergence gap is large and was reproduced. The energy-distance ratio is about 600 times the target, on four training fields at n=16, so it does not support a generator claim. The kinematic ABC signs are not generator metrics.

Three changes before this document can be defended. Replace the n=16 flow with a model whose energy-distance ratio can move toward 1.2, and keep the criterion fixed before that run. Add a tested null-point count before any C5 number. Build site/teams/cursor so the deliverable check can pass. The threshold at n=132 remains unverified, and H138 and H144 were not scored in this note.
