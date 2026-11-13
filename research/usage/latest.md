# Usage report (2026-11-13T04:25:34Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-13T04:25:30.891Z; span 11.59 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$164.01** (prices of race/config.toml [pricing]).
GPU: 28 job(s), 16.628 h, **$15.78** of a $140.0 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 689 | 1,367 | 1,903,034 | 1,690,489 | 274,979,332 | 1,358,780 | 682,106 | $155.44 |
| claude-sonnet-5-5 | 201 | 470 | 1,464,623 | 0 | 23,497,224 | 255,753 | 107,746 | $8.57 |

Sub-agents: 26 call(s), 0 not conforming to agents/roles/; by type {'general-purpose': 9, 'jury-externe': 5, 'biblio': 2, 'encadrant': 8, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| general-purpose | claude-sonnet-5-5 | medium | – | 20 | 33,210 | $0.9517 | Schematics: bottleneck and identities |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 39,710 | $1.1535 | Schematics: problem and metrics |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 17 | 144,770 | $8.7387 | Jury review: report v1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 10 | 132,697 | $10.0026 | Jury review: report v2 |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 16 | 20,224 | $2.0365 | Encadrant: verdicts H22-H24 |
| general-purpose | claude-sonnet-5-5 | medium | – | 8 | 8,752 | $0.4125 | Redraw linear-part schematic |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 14,273 | $1.3043 | Encadrant: H21 and G1 replication |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 41 | 76,650 | $7.1746 | Jury review: deliverable figures |
| general-purpose | claude-sonnet-5-5 | medium | – | 9 | 8,373 | $0.4509 | Update two schematics with G1 |
| general-purpose | claude-sonnet-5-5 | medium | – | 15 | 18,805 | $0.6994 | Fix five schematics after jury |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| general-purpose | claude-sonnet-5-5 | medium | – | 20 | 36,970 | $0.9731 | Schematics: pipeline and mechanisms |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 25,950 | $2.2439 | Encadrant: H11 and E4 reference protocol |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 6 | 6,708 | $0.1622 | Biblio: E4 references and prior art |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 31,422 | $0.9916 | Schematics: protocol and compute path |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 11 | 19,806 | $1.9591 | Encadrant review: e4_main and bug |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 22 | 22,835 | $3.1373 | Jury review: deliverable figures |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 19,260 | $1.6337 | Encadrant: verdicts H4-H10, H12-H14 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 14 | 22,018 | $2.054 | Encadrant: H18 and replication |
| general-purpose | claude-sonnet-5-5 | medium | – | 47 | 26,060 | $1.3093 | Fix three Archify diagrams |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 10,684 | $1.1972 | Encadrant: verdicts H15-H20 main run |
| general-purpose | claude-sonnet-5-5 | medium | – | 32 | 45,046 | $1.4153 | Archify diagrams for team claude |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 496, 'Read': 35, 'Agent': 26, 'Write': 11, 'ToolSearch': 2, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'SendMessage': 1}.
