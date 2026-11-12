# Usage report (2026-11-12T23:25:23Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-12T23:25:12.991Z; span 6.58 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$66.6** (prices of race/config.toml [pricing]).
GPU: 17 job(s), 3.848 h, **$2.96** of a $140.0 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 247 | 477 | 295,041 | 881,291 | 120,754,599 | 510,440 | 235,300 | $61.62 |
| claude-sonnet-5-5 | 108 | 242 | 858,665 | 0 | 12,003,537 | 162,650 | 74,183 | $4.97 |

Sub-agents: 13 call(s), 0 not conforming to agents/roles/; by type {'general-purpose': 5, 'biblio': 2, 'jury-externe': 1, 'encadrant': 3, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| general-purpose | claude-sonnet-5-5 | medium | – | 18 | 30,801 | $0.8776 | Schematics: bottleneck and identities |
| general-purpose | claude-sonnet-5-5 | medium | – | 15 | 30,507 | $0.8845 | Schematics: problem and metrics |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| general-purpose | claude-sonnet-5-5 | medium | – | 18 | 32,224 | $0.8736 | Schematics: pipeline and mechanisms |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 25,950 | $2.2439 | Encadrant: H11 and E4 reference protocol |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 6 | 6,708 | $0.1622 | Biblio: E4 references and prior art |
| general-purpose | claude-sonnet-5-5 | medium | – | 21 | 31,422 | $0.9916 | Schematics: protocol and compute path |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 8 | 19,260 | $1.6337 | Encadrant: verdicts H4-H10, H12-H14 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |
| general-purpose | claude-sonnet-5-5 | medium | – | 28 | 30,291 | $1.1342 | Archify diagrams for team claude |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 227, 'Read': 17, 'Agent': 13, 'Write': 6, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'ToolSearch': 1}.
