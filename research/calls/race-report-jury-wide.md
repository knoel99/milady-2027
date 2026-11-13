single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| Width 768 ratio 787.34 is below 791.02 | race report, Measured | CONFIRMED | cursor_constraint_wide.json, hidden 768, five finite seeds | State the gap is about 3.7. The report does |
| That ratio is not a C1 success | race report, Measured | CONFIRMED | 787.34 against target 1.2, and the metrics file is still the kmax=2 value 757.56 | Do not present the wide run as the best model |
| A perfect cutoff might still meet 1.2 | race report, Conjectured | TO BE SPECIFIED | Not measured yet | Run the projection ceiling before another learned model |

Pre-defence. Widening the layer moved the ratio by less than one percent. The generator claim is still not defendable. The next evidence that would change the conclusion is the projection ceiling at a few cutoffs. C5 and the deliverables are unchanged. H138 and H144 were still in flight.
