# Lab journal

One entry per working session, newest first, at most ten lines.

## 2026-11-12 - pilot step 1, team cursor
- Goal: steps 1 to 5 of race/PILOT-CURSOR-AGENT.md, stop at the first failed check.
- Done: CPU install from infra/env/requirements.txt then `pip install -e ".[dev]"` in `.venv` (torch 2.14.1+cpu). `make test` failed while `MILADY_GPU_BUDGET_USD=40` hid the budget the job tests set. The fixture now clears that variable. `make test` and `python3 tools/sync_agents.py --check` then exited 0.
- Prices: every `[gpu].fallback` id has a Secure and a Community rate (`python3 tools/runpod_job.py prices`, exit 0). Stock was LOW or NONE. `python3 tools/review_due.py due` printed "no review due" and exited 0.
- Stopped at step 3. This session has no sub-agent tool, and `CURSOR_API_KEY` is unset, so `encadrant`, `physicien`, `biblio` and `jury-externe` did not answer Proposition 1. Nothing was logged with `review_due.py log`.
- Not done: the float32 and float64 GPU benches, `research/journal.md` timings, `race/teams/cursor/objectives.toml`. GPU spend 0 USD. No pod was started.
- Next: rerun step 3 on a session that can spawn `.cursor/agents/`, then the two benches.

<!-- Template
## YYYY-MM-DD — H<id>: <short title>
- Goal of the session:
- Done (commands, runs, seeds):
- Result (digest keys) and encadrant verdict:
- Decision (supported / refuted / dropped / next step):
- Cost (tokens, CPU time):
-->
