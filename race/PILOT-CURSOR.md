# Pilot: one team on Cursor, Grok Bot orchestrating Cloud Agents

The second pilot runs the race brief with Cursor only (Cursor Ultra: Grok and Composer models). Grok Bot is the orchestrator: it launches Cursor Cloud Agents on this repository with `tools/cursor_agents.py`, follows them, sends the next task and keeps the time. The Cloud Agents do the research. Where this file and [`BRIEF.md`](BRIEF.md) differ, this file wins; [`PILOT.md`](PILOT.md) applies for everything this file does not change (results, storage, monitoring, stop rules).

## Setting

| | Cursor pilot |
|---|---|
| Orchestrator | Grok Bot (Cursor desktop or phone app), on its persistent cloud computer: a clone of this repository and `CURSOR_API_KEY` in its environment. Grok Bot chooses its own model (no picker) |
| Workers | Cursor Cloud Agents launched through the Cloud Agents API by `tools/cursor_agents.py`, on branches `cursor/...` of `knoel99/milady-2027`. Main session: `grok-4.7`, effort `high`, Fast (`race/config.toml` `[main_session]`, `agents/providers.toml` `[cursor]`) |
| Roles | Cursor sub-agents `.cursor/agents/*.md`, generated from `agents/roles/`: `encadrant` grok-4.7 medium, `physicien` grok-4.7 high, `biblio` grok-4.7 medium, `jury-externe` grok-4.7 xhigh, all Fast. A role can also run as its own Cloud Agent: `tools/cursor_agents.py launch --role <role>` |
| Speed | Fast everywhere (`[cursor] fast = true`): about 2x the price, the plan ends on 2026-11-13 and its credit is meant to be used |
| GPU | `tools/runpod_job.py`, with `RUNPOD_API_KEY` as a Cloud Agent secret; this team's share `MILADY_GPU_BUDGET_USD` (Cloud Agent secret: set it, e.g. 40; without it the 140 USD of `[gpu]` `budget_usd` applies). The guard of `[gpu]` `credit_usd` keeps every pilot together under the 150 USD prepaid credit |
| Dates | no deadline, only the budget; `MILADY_START` (ISO 8601) as a Cloud Agent secret: the start of the pilot, for `tools/review_due.py` |
| Monitoring | `tools/cursor_agents.py report` (agents, models, parameters applied, run status, usage returned by the API) on Grok Bot's side; `research/journal.md`, `research/reviews.jsonl`, `research/compute-ledger.jsonl` on the branch |

## Organisation

1. **One main agent, follow-ups for each step.** Grok Bot launches one main Cloud Agent with `race/PILOT-CURSOR-AGENT.md`; when a run ends, it reads the summary and the branch, then sends the next step as a follow-up to the same agent (`send`), so that the branch, the journal and the register stay in one place.
2. **Parallel workers for independent hypotheses.** At most two more Cloud Agents at a time, each owning one registered hypothesis, writing only its own files (`experiments/e*_<id>*`, `research/notes/<id>.md`) and pushing its own branch. The main agent merges their branches and arbitrates. No two agents edit the same file.
3. **Reviews over time.** The agents run `tools/review_due.py due` after every commit that adds a result and at least every hour; a due `encadrant` or `jury-externe` review runs as a sub-agent before work goes on and is recorded with `tools/review_due.py log`. Grok Bot checks `research/reviews.jsonl` on the branch at every follow-up and asks for any review that `review_due.py` lists.
4. **No deadline, a budget.** Grok Bot keeps the agents busy while the budget and the Cursor plan last: whenever a run ends, a new step is sent. When either is about to end: the final report (`research/race-report.md`), the usage report, `tools/runpod_job.py cleanup`, commit and push.

## Deliverables

The same as the Claude pilot, `race/DELIVERABLES.md`, under `site/teams/cursor/`. The skills are installed into `.cursor/skills/` by `bash tools/install_skills.sh`.

## Stop rules

The stop rules of `PILOT.md` apply. In addition: a run whose `report` row shows a model parameter not applied (`dropped`) is not conforming; fix `agents/providers.toml` `[cursor]` after `tools/cursor_agents.py models`, rerun `tools/sync_agents.py`, and relaunch.
