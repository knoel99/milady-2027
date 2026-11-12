# Usage report (2026-11-12T18:04:36Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-12T18:04:30.365Z; span 1.24 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$25.57** (prices of race/config.toml [pricing]).
GPU: 3 job(s), 0.457 h, **$0.33** of a $140 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 106 | 205 | 107,880 | 521,849 | 34,713,455 | 226,395 | 114,963 | $25.43 |
| claude-sonnet-5-5 | 6 | 12 | 42,051 | 0 | 64,158 | 3,248 | 172 | $0.14 |

Sub-agents: 6 call(s), 0 not conforming to agents/roles/; by type {'biblio': 2, 'jury-externe': 1, 'encadrant': 1, 'physicien': 2}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 5 | 27,689 | $1.7479 | Physicien: E4 conjectures |
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 4 | 2,551 | $0.0937 | Biblio: E4 references and prior art |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 92, 'Read': 17, 'Agent': 6, 'Write': 6, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'ToolSearch': 1}.
