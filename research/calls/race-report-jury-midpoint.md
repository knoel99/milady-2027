single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| Midpoint mean ratio 0.743 | race report, Measured | CONFIRMED | cursor_constraint_midpoint.json, five finite seeds. Seed 0 is 1.80 | Keep the seed-0 exception visible. The report does |
| C1 and C2 meet their targets on that map | race report, Remaining | CONFIRMED | cursor_objectives.py prints 0.743 and 4.80e-16 | Do not describe the flow-matching runs as the quoted model |
| C3 is 0.0986 and C4 is 0.150 | race report, Remaining | CONFIRMED | same midpoint file, means of the five seeds | A later cutoff can still move these. They miss 0.05 and 0.1 |
| H138, all five seeds positive | race report, Remaining | CONFIRMED | cursor_abc_n160_rm90625, smallest lambda 5.84e-5 | Do not bisect that bracket while C3 and C4 are the open objectives |
| Spend 21.56 USD | race report, Measured | CONFIRMED | runpod_job.py spend after the H138 ledger row | None |

Pre-defence. The quoted generator is a linear midpoint at n=16, not a trained flow. C1 and C2 meet their targets on that map. C3, C4, and C5 do not, and the deliverables are absent, so the document is not defendable. H144 was still in flight.
