# Usage report (2026-11-13T00:29:37Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-13T00:29:31.965Z; span 7.65 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$112.15** (prices of race/config.toml [pricing]).
GPU: 19 job(s), 5.71 h, **$4.3** of a $140.0 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 501 | 1,003 | 952,113 | 1,423,834 | 188,147,943 | 852,363 | 381,145 | $104.03 |
| claude-sonnet-5-5 | 192 | 444 | 1,348,968 | 0 | 22,717,346 | 247,380 | 105,954 | $8.12 |

Sub-agents: 21 call(s), 0 not conforming to agents/roles/; by type {'general-purpose': 8, 'jury-externe': 4, 'biblio': 2, 'encadrant': 5, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| general-purpose | claude-sonnet-5-5 | medium | – | 20 | 33,210 | $0.9517 | Schematics: bottleneck and identities |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 39,710 | $1.1535 | Schematics: problem and metrics |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 1,129 | $0.2534 | Jury review: report v1 |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| general-purpose | claude-sonnet-5-5 | medium | – | 8 | 8,752 | $0.4125 | Redraw linear-part schematic |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 41 | 76,650 | $7.1746 | Jury review: deliverable figures |
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
| general-purpose | claude-sonnet-5-5 | medium | – | 47 | 26,060 | $1.3093 | Fix three Archify diagrams |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 10,684 | $1.1972 | Encadrant: verdicts H15-H20 main run |
| general-purpose | claude-sonnet-5-5 | medium | – | 32 | 45,046 | $1.4153 | Archify diagrams for team claude |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 377, 'Read': 33, 'Agent': 21, 'Write': 10, 'ToolSearch': 2, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'SendMessage': 1}.
