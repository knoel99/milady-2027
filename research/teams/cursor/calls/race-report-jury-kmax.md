single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| kmax=4 ratio 791.02 does not beat 757.56 | race report, Measured | CONFIRMED | cursor_constraint_kmax4.json, five finite seeds | None for this negative result |
| The metrics file stays on the smaller ratio | race report, Measured | CONFIRMED | cursor_metrics.json c1 is 757.56, not 791 | Do not swap in the worse run |
| C6 has four verdicts | race report, Remaining | CONFIRMED | cursor_objectives.py --metric c6 prints 4 | A further comparison is still useful if it can move C1 |
| The report is not defendable | race report, Status | CONFIRMED | C1 is 757 against a target of 1.2, C5 is the sentinel, site/teams/cursor is absent | A wider model, a null count, and the deliverables |

Pre-defence. The kmax change was the one variable, and it moved the ratio the wrong way. That is a real negative result. The document still cannot be defended as a generator study. Three changes remain: a model whose ratio can fall, a tested Haynes-Parnell count before any C5 number, and the team deliverables. H138 and H144 were still in flight.
