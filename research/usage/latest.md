# Usage report (2026-11-12T22:59:32Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-12T22:59:25.469Z; span 6.15 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$53.46** (prices of race/config.toml [pricing]).
GPU: 15 job(s), 3.596 h, **$2.59** of a $140.0 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 220 | 425 | 275,936 | 786,843 | 100,512,343 | 444,727 | 212,430 | $53.24 |
| claude-sonnet-5-5 | 8 | 16 | 50,639 | 0 | 118,669 | 7,405 | 343 | $0.21 |

Sub-agents: 8 call(s), 0 not conforming to agents/roles/; by type {'biblio': 2, 'jury-externe': 1, 'encadrant': 3, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 25,950 | $2.2439 | Encadrant: H11 and E4 reference protocol |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 6 | 6,708 | $0.1622 | Biblio: E4 references and prior art |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 5 | 10,112 | $1.0354 | Encadrant: verdicts H4-H10, H12-H14 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 198, 'Read': 17, 'Agent': 8, 'Write': 6, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'ToolSearch': 1}.
