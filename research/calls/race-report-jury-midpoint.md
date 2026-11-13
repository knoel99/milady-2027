single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| H166 mean is 0.172 and misses 0.1 | race report, Measured | CONFIRMED | cursor_nulls_midpoint_kmax6.json | Do not quote it as a pass |
| Quoted C5 stays 0.428 | race report, Remaining | CONFIRMED | cursor_metrics.json still has the kmax=4 error | Change it only after H167 is scored |
| H167 has no result yet | race report, Measured | CONFIRMED | status registered | A second midpoint miss drops this comparison |

Pre-defence. C5 is still a measured miss on every scored generator. The kmax=7 midpoint is the last registered test of that bound.
