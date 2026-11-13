single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| H165 mean is 0.160 and misses 0.1 | race report, Measured | CONFIRMED | cursor_nulls_kmax6.json | Do not replace the quoted C5 with this miss |
| Two truncation widths are dropped | race report, Remaining | CONFIRMED | H164 0.428 and H165 0.160, both above 0.1 | Do not launch a third truncation of the same snapshot |
| H166 has no result yet | race report, Measured | CONFIRMED | status registered, no result file at the review | Score it only after the run that was registered first |
| Quoted C5 remains 0.428 | race report, Remaining | CONFIRMED | cursor_metrics.json | Keep the label on the kmax=4 file |

Pre-defence. The truncation route to C5 is a negative result. The midpoint comparison is the remaining registered test of that objective.
