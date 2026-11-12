# Pilot: one team, Claude Code cloud

The pilot runs the race with a single team before the nine-provider race: one Claude Code cloud session in the `milady-2027` environment, its own branch, and GPU jobs on RunPod. Its purpose is to test the brief, the roles, the GPU path and the monitoring on real work, and to measure what a team really costs. Where this file and [`BRIEF.md`](BRIEF.md) differ, this file wins.

## Setting

| | Pilot |
|---|---|
| Harness | Claude Code, cloud session of the `milady-2027` environment (its setup script installs the RunPod plugin and the `runpod-api` MCP entry; the RunPod key is a network secret injected by the proxy) |
| Main session | Claude Fable 5.2, effort `high` (`/model fable`, `/effort high`; `race/config.toml` `[main_session]`) |
| Roles | Claude Code sub-agents `.claude/agents/*.md`, generated from `agents/roles/`: `encadrant` Fable/medium, `physicien` Fable/high, `biblio` Sonnet 5.5/medium, `jury-externe` Fable/max. `tools/call_model.py` and `tools/run_role.py` need an Anthropic API key and are not used in the pilot |
| CPU | the session's own container (quick runs, measurements) |
| GPU | `tools/runpod_job.py run`: the `[gpu]` `fallback` list of `race/config.toml` (RTX PRO 4500 Blackwell, RTX 5090, RTX 4090, RTX A6000, A40, L40S, RTX PRO 6000, A100), each tried on Secure Cloud, then the list again on Community Cloud; the stock shown by the catalog is unreliable, so a refused create is not the end: rerun later or widen `--gpu`. H100 only for float64 validation |
| Budgets | GPU: 140 USD of the 150 USD prepaid RunPod credit, all usable (`race/config.toml` `[gpu]` `budget_usd`; 10 USD margin for storage and rounding). Claude: the plan's usage limit; `tools/usage_report.py` gives the API-equivalent cost |
| Duration | one week from the start, or until a budget is spent |

## Results and data storage

- `tools/runpod_job.py` brings each job's outputs back into this checkout (default `experiments/results` and `site/experiments/figures`, or the paths given with `--outputs`) with the job log in `research/gpu-logs/`. Commit and push them right after the job.
- Small results (JSON, figures, digests, logs) go into git. Never commit a file above 50 MB: GitHub refuses files above 100 MB and the repository must stay light.
- Where large data lives (3D fields in MFF/HDF5, training sets, checkpoints) is your decision. Before producing more than about 1 GB, choose a storage, write the choice and its reasons in `research/data-storage.md` (what is stored where, how a pod and this session read it back, what it costs, what happens to it after the pilot), and record it in the journal. Use what the repository already has where it fits (`docs/specs/data-format.md`, `src/milady/storage.py`, `src/milady/catalog/`), and keep every dataset regenerable from a committed script and its parameters.

## Monitoring

`tools/usage_report.py --write research/usage` reads the session transcripts and writes `research/usage/latest.md` and `latest.json`:

- tokens per model (input, cache writes 5 min and 1 h, cache reads, output, thinking) and the API-equivalent cost;
- the main session's model and effort against the prescribed Fable / `high`;
- every sub-agent call with its type, model and effort, checked against `agents/roles/`;
- the number of tool calls of the main session, the time span of the work;
- the GPU jobs, hours and dollars of `research/compute-ledger.jsonl`, against the GPU budget.

`tools/runpod_job.py spend` gives the GPU spend alone; `tools/runpod_job.py cleanup` deletes any pod a failed job left behind. The session commits the report after each hypothesis and at least every four hours of work, so that the owner can follow it on the branch from any client.

## Reviews over time

The `encadrant` and the `jury-externe` step in when `python3 tools/review_due.py due` says so, not once a week: after new results or hypotheses, after `encadrant_max_gap_hours` of work without a review, at each quarter of the span from `[reviews]` `start` to the deadline, and when the report changes (`race/config.toml` `[reviews]`). Run it after every commit that adds a result and at least every hour; run every due review before going on; record it with `tools/review_due.py log`, so that `research/reviews.jsonl` shows when each role stepped in and what it found.

## Stop rules

1. The whole GPU budget may be used, but a job starts only if its worst case (time limit × hourly price) fits in what is left: `tools/runpod_job.py` checks it, so no job is cut off by an empty credit. Commit and push the outputs and `research/compute-ledger.jsonl` right after each job: the session's container is the only other copy.
2. The plan's usage limit warns: finish the current hypothesis, write the usage report, commit, push, stop (`AGENTS.md` rule 7).
3. The deadline is reached: write `research/race-report.md`, the usage report, commit, push, stop.
4. Never leave a pod running: every GPU job goes through `tools/runpod_job.py`, which deletes the pod; end every working block with `tools/runpod_job.py cleanup`.
