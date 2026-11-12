# Usage report (2026-11-12T16:59:30Z)

Sessions: 1; first response 2026-11-12T16:50:21.852Z; last 2026-11-12T16:59:17.201Z; span 0.15 h.
Main session: models ['claude-fable-5-2'], efforts ['high']; expected claude-fable-5-2 / high: conforms.
API-equivalent cost of the Claude calls: **$8.03** (prices of race/config.toml [pricing]).
GPU: 0 job(s), 0 h, **$0** of a $140 budget.

| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |
|---|---|---|---|---|---|---|---|---|
| claude-fable-5-2 | 30 | 57 | 46,485 | 292,160 | 4,598,109 | 48,088 | 30,979 | $7.98 |
| claude-sonnet-5-5 | 2 | 4 | 16,980 | 0 | 9,599 | 697 | 0 | $0.05 |

Sub-agents: 4 call(s), 0 not conforming to agents/roles/; by type {'biblio': 1, 'jury-externe': 1, 'encadrant': 1, 'physicien': 1}.

| type | models | efforts | expected | API calls | output | cost | description |
|---|---|---|---|---|---|---|---|
| biblio | claude-sonnet-5-5 | medium | claude-sonnet-5-5 / medium | 2 | 697 | $0.0504 | Role check: biblio Prop 1 |
| jury-externe | claude-fable-5-2 | max | claude-fable-5-2 / max | 2 | 5,052 | $0.444 | Role check: jury-externe Prop 1 |
| encadrant | claude-fable-5-2 | medium | claude-fable-5-2 / medium | 1 | 998 | $0.1537 | Role check: encadrant Prop 1 |
| physicien | claude-fable-5-2 | high | claude-fable-5-2 / high | 1 | 1,298 | $0.1633 | Role check: physicien Prop 1 |

Role calls through tools/call_model.py or run_role.py: 0.
Tool calls of the main session: {'Bash': 24, 'Read': 16, 'Agent': 4, 'mcp__claude-code-remote__get_session': 1, 'Grep': 1, 'Write': 1}.
