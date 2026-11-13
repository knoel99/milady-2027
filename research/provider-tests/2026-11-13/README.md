# Provider tests, 2026-11-13

Test calls made by the preparation session to check, provider by provider, that each role of
`agents/roles/` reaches its model with its reasoning effort: `tools/call_model.py` (API, one call per
role, prompt "Reply with the single word OK.") and `tools/run_role.py` (headless harness). The keys
are network secrets of the `milady-2027` cloud environment, injected by its proxy. These files are a
test record, not race calls: they are kept out of `research/model-calls.jsonl` and `research/calls/`.
The summary of the results is in `race/PROVIDERS-TESTED.md`.
