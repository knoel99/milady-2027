# Lab journal

One entry per working session, newest first, at most ten lines.

## 2026-11-12 - shared GPU budget, team cursor
- Kim set the hard shared limit to 150 USD, the prepaid credit from main PR #39, first come first served with the Claude team.
- This session exports MILADY_GPU_BUDGET_USD=150. A new job is refused when main's reservation (account spend, plus the worst case still reserved by live milady-job pods, plus the new job) would cross that credit.
- H5 is registered before any growth-rate run. CPU smoke `experiments/cursor_abc_growth.py --quick` exited 0 (n = 16, t = 2, Rm = 12, max_div_b 3.46e-16). That short lambda is a transient, not the H5 sample. The float32 bench was already in flight on an RTX 4090. No H100.

## 2026-11-12 - pod incident, team cursor
- Incident. `python3 tools/runpod_job.py cleanup` in this session deleted two Claude-team pods this session had not created: `hd6qx71mm6jekm` (`milady-job-329724d4`) and `00t6s3l481flvm` (`milady-job-a24b1ae9`). The cleanup then in this branch deleted every pod whose name started with `milady-job-`.
- Fix used. Main commit `ce0c796` (PR #39) now deletes only pods past their time limit, and `run` reserves the worst-case cost of pods already running, up to `max_parallel` 4. This branch merged that file and did not rewrite it. `make test` exited 0 after the merge.
- Any role text added after this line is a single-model simulation (no independent sub-agent).

## 2026-11-12 - pilot step 1, team cursor
- Goal: steps 1 to 5 of race/PILOT-CURSOR-AGENT.md, stop at the first failed check.
- Done: CPU install from infra/env/requirements.txt then `pip install -e ".[dev]"` in `.venv` (torch 2.14.1+cpu). `make test` failed while `MILADY_GPU_BUDGET_USD=40` hid the budget the job tests set. The fixture now clears that variable. `make test` and `python3 tools/sync_agents.py --check` then exited 0.
- Prices: every `[gpu].fallback` id has a Secure and a Community rate (`python3 tools/runpod_job.py prices`, exit 0). Stock was LOW or NONE. `python3 tools/review_due.py due` printed "no review due" and exited 0.
- Stopped at step 3. This session has no sub-agent tool, and `CURSOR_API_KEY` is unset, so `encadrant`, `physicien`, `biblio` and `jury-externe` did not answer Proposition 1. Nothing was logged with `review_due.py log`.
- Not done: the float32 and float64 GPU benches, timings, and `race/teams/cursor/objectives.toml`. This branch's ledger is 0 USD. `python3 tools/runpod_job.py cleanup` deleted two pre-existing pods this session did not create: `hd6qx71mm6jekm` (`milady-job-329724d4`) and `00t6s3l481flvm` (`milady-job-a24b1ae9`).
- Next: rerun step 3 on a session that can spawn `.cursor/agents/`, then the two benches.

<!-- Template
## YYYY-MM-DD — H<id>: <short title>
- Goal of the session:
- Done (commands, runs, seeds):
- Result (digest keys) and encadrant verdict:
- Decision (supported / refuted / dropped / next step):
- Cost (tokens, CPU time):
-->
