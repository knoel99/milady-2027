single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| C5 is 0.428 and misses 0.1 | race report, Remaining | CONFIRMED | cursor_nulls.json, mean of five seeds | Do not say the target is met |
| The null count lives in src/milady/eval/nulls.py | race report, Remaining | CONFIRMED | the module and tests/test_nulls.py | None |
| The built deliverable check passes after render | race report, Remaining | CONFIRMED | check_deliverables.py --team cursor --built, 33/33 | Keep the HTML gitignored and name the render command |
| No team pod is running | race report, Remaining | CONFIRMED | no milady-cursor-job pod after the H144 ledger row | None |

Pre-defence. C1 through C4 meet the named targets. C5 is a measured miss. The team report exists. The document is not a finished race, because a finer truncation could still move C5 and that comparison is not yet registered.
