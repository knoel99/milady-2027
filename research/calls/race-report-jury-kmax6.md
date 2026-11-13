single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| kmax=6 C4 is 0.0093 and meets 0.1 | race report, Measured | CONFIRMED | cursor_constraint_midpoint_kmax6.json | None |
| C1 on that map is 0.014 | race report, Measured | CONFIRMED | same file, mean of five seeds | The quoted model is a midpoint, not a flow. The report says so |
| C3 is 0.083 and misses 0.05 | race report, Remaining | CONFIRMED | same file | Do not claim the energy balance meets its target |
| C5 is still the sentinel | race report, Remaining | CONFIRMED | cursor_objectives.py --metric c5 prints 1 | A Haynes-Parnell count is still required before any C5 number |

Pre-defence. Three of the five generator metrics now meet their targets on a linear midpoint at n=16. The energy balance does not, there is no null count, and the deliverables are absent. The document is not defendable. H144 was still in flight. Spend was 21.56 USD of 150 before this CPU run, which cost nothing.
