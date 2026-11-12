# Pilot prompt

Paste the text below as the first message of a new Claude Code cloud session on the `milady-2027` environment, after `/model fable` and `/effort high`. Then set the goal with the `/goal` line at the end.

---

You are the only team of the pilot of the MilaDy race. Read `race/PILOT.md`, then `race/BRIEF.md` and `AGENTS.md`, and follow them; where they differ, `race/PILOT.md` wins. Work alone: do not ask me questions, except to approve a GPU job on an H100 or a spend above the budgets.

Start with these checks, and stop to tell me if one fails:

1. `get_session` shows the model `claude-fable-5-2` and the effort `high`.
2. `claude mcp list` shows `runpod-api` connected, and `python3 tools/runpod_job.py prices` lists the GPUs of `race/config.toml` with a price.
3. `make test` and `python3 tools/sync_agents.py --check` pass.
4. Each of the four roles (`encadrant`, `physicien`, `biblio`, `jury-externe`) answers one short question on Proposition 1 of `docs/specs/theory-brief.md` through its sub-agent; then `python3 tools/usage_report.py --write research/usage` reports the main session and every role as conforming.
5. One GPU job measures the simulator: `python3 tools/runpod_job.py run --hours 0.5 -- python -m milady.sim.mhd3d bench --n 64 128 --device cuda --dtype float32 --steps 50`, then the same with `--dtype float64`. Write the timings in `research/journal.md`: they replace the extrapolated GPU costs in your planning.

Then carry out the race brief: quantify your objectives in `race/teams/claude/objectives.toml` on day 1, register each hypothesis with its refutation criterion before computing, use the roles as `AGENTS.md` prescribes, run GPU work only through `tools/runpod_job.py`, and commit and push at least every hour. After each hypothesis and at least every four hours of work, run `python3 tools/usage_report.py --write research/usage` and `python3 tools/runpod_job.py spend`, commit the report, and add a line to `research/journal.md`: hypothesis, verdict, tokens, cost, GPU hours.

```
/goal race/teams/claude/objectives.toml exists and passes `python3 tools/race_progress.py check`; research/race-report.md states what is measured, published and conjectured and the remaining work for each objective; research/usage/latest.md is up to date and shows no non-conforming role call; `python3 tools/runpod_job.py spend` is within budget and no pod is left running; everything is committed and pushed. If the usage limit warns, a budget is spent or the deadline in race/config.toml is reached, write the report, commit, push and stop.
```
