# Pilot prompt

Paste the text below as the first message of a new Claude Code cloud session on the `milady-2027` environment, after `/model fable` and `/effort high`. Then set the goal with the `/goal` line at the end. The goal ends on the budget, not on a report: a goal made only of end-state conditions lets the session stop as soon as its first report is written (pilot of 2026-11-12, stopped with objectives not met and budget left). The pilot chooses its strategy freely; there is no time limit.

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
/goal Advance the research of the internship offer as far as the budget allows: after each result, take the next step of the remaining work of research/race-report.md that you judge most useful, with your own strategy. The goal is met only when the GPU budget cannot pay for another useful job or the usage limit warns, or when you show in research/race-report.md, with evidence, that no step left within the budget can change a verdict or an objective. At that point: race/teams/claude/objectives.toml passes `python3 tools/race_progress.py check`; research/race-report.md states what is measured, published and conjectured and the remaining work for each objective; `python3 tools/check_deliverables.py --team claude --built` passes; research/usage/latest.md is up to date and shows no non-conforming role call; no pod of the team is left running; everything is committed and pushed.
```

## Goal set by the owner on the running Claude pilot

Set by the owner in session `session_019DLE2XTZBM3CAyB1594sVV` on 2026-11-13 at about 07:05 UTC (recorded in the session as active), verbatim:

```
/goal Fais avancer la recherche du sujet de stage aussi loin que le budget le permet, avec ta propre stratégie : après chaque résultat, choisis l'étape suivante la plus utile. Le goal n'est atteint que si le budget GPU ne permet plus un job utile, si la limite d'usage prévient, ou si tu montres preuves à l'appui dans research/race-report.md qu'aucune étape restante dans le budget ne peut changer un verdict ou un objectif. À ce moment : objectives.toml valide, race-report.md à jour (mesuré, publié, conjecturé, reste à faire), `tools/check_deliverables.py --team claude --built` passe, rapport d'usage à jour, aucun pod de l'équipe en marche, tout commité et poussé.
```

It is the French form of the `/goal` above; for another team, replace `--team claude` by its team.
