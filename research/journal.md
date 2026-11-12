# Lab journal

One entry per working session, newest first, at most ten lines.

## 2026-11-12 — Pilot day 1: start-up checks and objectives
- Goal of the session: the five checks of `race/PILOT-PROMPT.md`, then the day-1 objectives.
- Checks 1–4 passed: session `claude-fable-5-2` / `high` (`get_session`); `runpod-api` connected and `runpod_job.py prices` lists RTX PRO 4500 Blackwell $0.72/h, RTX 5090 $1.19/h, RTX A6000 $0.59/h (all stock LOW); `make test` and `sync_agents.py --check` pass; the four roles answered one question on Proposition 1 and `research/usage/latest.md` reports the main session and the 4 role calls as conforming.
- Check 5 (GPU bench of `milady.sim.mhd3d`, float32 then float64): **not passed yet**. `create-pod` is refused for the three configured GPUs, with and without the data-centre list ("no longer any instances available"): a capacity shortage, nothing billed, no pod created, no ledger entry. Retries are logged below when they succeed. Until then no GPU timing exists: planning uses the CPU timings measured in this container only.
- Role answers on Proposition 1 worth keeping (not verdicts on a hypothesis): `encadrant`: zero divergence holds only for the decoder's own discrete operator (spectral curl + centred differences leaves an O(h²) residual); `physicien`: the periodic curl misses only the mean field, which the induction equation conserves; `jury-externe`: Proposition 1 is a one-line fact to cite, not a contribution.
- Done: `race/teams/claude/objectives.toml` (C1–C7, T1, T2; `race_progress.py check`: ok) and `experiments/race_metrics.py` (measurement commands). Baselines on the starting repository: C6 = 0, C7 = 0, the others not measurable (no 3D generator).
- Next: register the E4 hypotheses (3D forced ABC MHD, constraint mechanisms), write `experiments/e4_data.py` and `e4_mhd3d.py`, `--quick` on CPU.
- Cost (tokens, CPU time): usage report of 16:53 UTC: $4.34 API-equivalent, 4 role calls ($0.81); GPU $0.

<!-- Template
## YYYY-MM-DD — H<id>: <short title>
- Goal of the session:
- Done (commands, runs, seeds):
- Result (digest keys) and encadrant verdict:
- Decision (supported / refuted / dropped / next step):
- Cost (tokens, CPU time):
-->
