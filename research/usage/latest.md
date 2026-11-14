# Usage report (2026-11-14T07:08:35Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-14T07:08:14.248Z; span 38.3 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$455.57** (prices of race/config.toml [pricing]).
GPU: 82 job(s), 66.881 h, **$59.79** of a $140.0 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 1982 | 3,944 | 5,977,315 | 4,745,607 | 795,484,994 | 3,804,181 | 1,875,101 | $447.0 |
| claude-sonnet-5-5 | 201 | 470 | 1,464,623 | 0 | 23,497,224 | 255,753 | 107,746 | $8.57 |

Sub-agents: 48 call(s), 0 not conforming to agents/roles/; by type {'general-purpose': 9, 'jury-externe': 11, 'encadrant': 23, 'biblio': 2, 'physicien': 3}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| general-purpose | claude-sonnet-5-5 | medium | – | 20 | 33,210 | $0.9517 | Schematics: bottleneck and identities |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 39,710 | $1.1535 | Schematics: problem and metrics |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 17 | 144,770 | $8.7387 | Jury review: report v1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 9 | 41,023 | $3.5912 | Encadrant: verdict H28 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 26 | 47,538 | $4.0773 | Encadrant: corrections v4 and H28 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 9 | 12,983 | $1.4367 | Encadrant: digest additions v3 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 10 | 132,697 | $10.0026 | Jury review: report v2 |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 16 | 20,224 | $2.0365 | Encadrant: verdicts H22-H24 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 26 | 32,251 | $4.404 | Encadrant verdicts H29-H31 |
| general-purpose | claude-sonnet-5-5 | medium | – | 8 | 8,752 | $0.4125 | Redraw linear-part schematic |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 14,273 | $1.3043 | Encadrant: H21 and G1 replication |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 9 | 24,012 | $1.8442 | Encadrant verdicts H38 H39 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 41 | 76,650 | $7.1746 | Jury review: deliverable figures |
| general-purpose | claude-sonnet-5-5 | medium | – | 9 | 8,373 | $0.4509 | Update two schematics with G1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 7 | 18,508 | $1.5404 | Encadrant check of closing results |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 7 | 118,663 | $6.8616 | Jury review: report v3 and test plan |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 13 | 95,825 | $7.0858 | Jury verifies release and corrections |
| general-purpose | claude-sonnet-5-5 | medium | – | 15 | 18,805 | $0.6994 | Fix five schematics after jury |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 16 | 34,636 | $2.775 | Encadrant review H25-H27 |
| general-purpose | claude-sonnet-5-5 | medium | – | 20 | 36,970 | $0.9731 | Schematics: pipeline and mechanisms |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 25,950 | $2.2439 | Encadrant: H11 and E4 reference protocol |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 12 | 22,684 | $2.5401 | Encadrant verdicts H33 H32 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 17 | 29,231 | $2.7162 | Encadrant check of v4 numbers |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 42 | 118,475 | $9.2777 | Jury-externe review report v4 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 41 | 74,907 | $7.1977 | Jury review report v6 on offer |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 17 | 65,969 | $4.3532 | Physicien: next conjectures E4 |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 6 | 6,708 | $0.1622 | Biblio: E4 references and prior art |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 14,452 | $1.3883 | Encadrant verdict H40 |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 31,422 | $0.9916 | Schematics: protocol and compute path |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 11 | 19,806 | $1.9591 | Encadrant review: e4_main and bug |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 5 | 14,521 | $1.1234 | Encadrant verdict H34 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 32 | 119,394 | $8.4819 | Jury externe: report v5 draft |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 22 | 22,835 | $3.1373 | Jury review: deliverable figures |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 14,374 | $1.6818 | Encadrant verdict H41 + offer |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 19,260 | $1.6337 | Encadrant: verdicts H4-H10, H12-H14 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 13 | 23,395 | $2.1457 | Encadrant: H35 criterion |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 14 | 22,018 | $2.054 | Encadrant: H18 and replication |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 6 | 21,215 | $1.7548 | Encadrant verdicts H35 H36 |
| general-purpose | claude-sonnet-5-5 | medium | – | 47 | 26,060 | $1.3093 | Fix three Archify diagrams |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 10,684 | $1.1972 | Encadrant: verdicts H15-H20 main run |
| general-purpose | claude-sonnet-5-5 | medium | – | 32 | 45,046 | $1.4153 | Archify diagrams for team claude |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 23 | 157,462 | $15.2902 | Final jury review of report |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 7 | 21,514 | $1.8329 | Encadrant verdict H37 |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 1386, 'Read': 55, 'Agent': 48, 'Write': 18, 'SendMessage': 10, 'ToolSearch': 9, 'ReadNotifications': 5, 'mcp__github__get_job_logs': 3, 'mcp__claude-code-remote__send_message': 2, 'mcp__github__actions_list': 2, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'mcp__runpod-api__list-pods': 1, 'mcp__claude-code-remote__read_documentation': 1, 'TaskStop': 1}.
