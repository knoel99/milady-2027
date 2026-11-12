# Usage report (2026-11-12T22:25:43Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-12T22:25:28.237Z; span 5.59 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$48.94** (prices of race/config.toml [pricing]).
GPU: 15 job(s), 3.596 h, **$2.59** of a $140 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 200 | 387 | 215,637 | 753,323 | 88,837,132 | 418,784 | 202,659 | $48.73 |
| claude-sonnet-5-5 | 8 | 16 | 50,639 | 0 | 118,669 | 7,405 | 343 | $0.21 |

Sub-agents: 7 call(s), 0 not conforming to agents/roles/; by type {'biblio': 2, 'jury-externe': 1, 'encadrant': 2, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 10 | 25,950 | $2.2439 | Encadrant: H11 and E4 reference protocol |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 6 | 6,708 | $0.1622 | Biblio: E4 references and prior art |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 182, 'Read': 17, 'Agent': 7, 'Write': 6, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'ToolSearch': 1}.
