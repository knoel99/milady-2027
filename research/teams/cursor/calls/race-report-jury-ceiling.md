single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| Perfect kmax=4 mean ratio 0.728 | race report, Measured | CONFIRMED | cursor_constraint_ceiling.json, five finite seeds. Seed 0 alone is 1.75 | Keep saying this is not a learned model. The report does |
| kmax=6 and kmax=7 are far under 1.2 | race report, Measured | CONFIRMED | means 0.0092 and 0.0028 | None |
| Learned C1 stays 757 | race report, Measured | CONFIRMED | cursor_metrics.json was not replaced by the ceiling | The next learned run has to move this number, or the report must keep it |
| C6 is past its target | race report, Remaining | CONFIRMED | cursor_objectives.py --metric c6 prints 9 | Do not add comparisons that cannot move C1 |

Pre-defence. The representation can meet the target and the trained flow does not. That is the useful split. The document is still not defendable: the quoted generator ratio is 757, C5 has no null count, and site/teams/cursor does not exist. H138 and H144 were still in flight.
