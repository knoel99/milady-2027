# Preflight exam: calling the roles autonomously

Give this file, unchanged, as the prompt of a headless session of the team's harness, with
`MILADY_PROVIDER` set to the team's section of `agents/providers.toml`. Note the UTC time
before starting (format `YYYYMMDDTHHMMSS`). Then run
`python3 tools/check_calls.py exam --provider <team> --since <time>`: the exam passes when every
role was called at least once with the model and the effort that `agents/providers.toml` and
`agents/roles/` prescribe, and the call succeeded.

---

Read `AGENTS.md`. Do not ask any question; work alone.

The claim to examine is in `docs/specs/theory-brief.md`: the first proposition stated there.

1. Obtain from `physicien` at most three conjectures on what could make this proposition fail in
   the setting of experiment E1.
2. Obtain from `encadrant` a verdict on the proposition, criterion by criterion. Give it the
   statement, the proof and anything it needs to check them.
3. Obtain from `biblio` whether the result is already published, using only
   `docs/specs/sources/*.md`.
4. Obtain from `jury-externe` a one-paragraph verdict on whether the proposition, as stated, can
   be defended.

Use the role mechanism described in `AGENTS.md`, with the provider set in `MILADY_PROVIDER`.
Then run `python3 tools/check_calls.py ledger --provider "$MILADY_PROVIDER"` and write
`research/preflight-report.md`: one line per role (how it was called, model, effort, outcome) and
the output of the check. Commit nothing.
