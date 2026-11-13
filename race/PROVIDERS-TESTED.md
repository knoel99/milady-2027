# Providers tested (2026-11-13)

Tests run from a Claude Code cloud session with each provider's API key as a network secret of the `milady-2027` environment. Record of the calls: `research/provider-tests/2026-11-13/`. "Native sub-agent" was tested by giving the main session a random code it must not pass on and asking a sub-agent defined on another model for it: an answer "UNKNOWN" and the other model in the usage show a separate context and a separate model.

| Team | API: each role reaches its model and effort (`tools/call_model.py`) | Effort validated by the API (an invented value is refused) | Harness headless (version) | Role as a headless instance (`tools/run_role.py`) | Native sub-agent: own context / own model / own effort |
|---|---|---|---|---|---|
| xai | ✅ grok-4.7, the 4 roles | ✅ (`max` refused: `xhigh` is the top) | ✅ Grok Build 1.0.77 | ✅ physicien high | ✅ / ✅ (`[subagents.models]`, grok-4.6 seen) / ❓ (personas carry `reasoning_effort`, binding to a type undocumented) |
| openai | ✅ gpt-6-astra, gpt-6.1-sol | ✅ | ✅ Codex 0.169.0 (`< /dev/null`, `--trust` for project agents, `--enable multi_agent_v2`) | ✅ (dry run; same command as the exec test) | ✅ / ✅ (gpt-6-luna) / ✅ (`low`, in the child's session file) |
| google | ✅ gemini-4-carbon and 4-argon through the OpenAI-compatible endpoint; ❌ `call_model.py` native endpoint: 401 | ✅ (valid: none, minimal, low, medium, high, xhigh) | ❌ Antigravity 1.5.8: 401 `API_KEY_SERVICE_BLOCKED` | ❌ same | not tested |
| zhipu | ✅ glm-5.3 | ✅ (accepts medium: mapping fixed) | ✅ Claude Code on `api.z.ai/api/anthropic` | ✅ (dry run) | ✅ / ✅ (glm-5.3-flash) / ✅ recorded by Claude Code (`low`); applied by Z.ai not observable |
| moonshot | ✅ kimi-k3.1-pro (3 requests per minute on this key) | ⚠️ the API accepts any value; low vs max changes the reasoning tokens (35 vs 77) | ✅ Kimi Code 2.6.1 (`KIMI_MODEL_*` variables) | ✅ `KIMI_MODEL_THINKING_EFFORT` is read by the CLI (source) | not supported per sub-agent (no model or effort field) |
| deepseek | ✅ deepseek-flash, deepseek-v4-pro | ✅ (accepts medium) | ✅ dsh 0.2.2-rc.1 | ✅ after the fix: `DSH_MODEL`, `DSH_REASONING_EFFORT` through the profile patch (dsh accepts off, low, high, max) | not tested |
| alibaba | ✅ qwen3.8-max-0902, qwen3.8-flash | ✅ (accepts high: mapping fixed) | ✅ Qwen Code 0.27.3 | effort only in `settings.json` | ✅ / ✅ (qwen3.8-flash) / no effort field |
| mistral | ✅ mistral-large-4 | ✅ (Large 4: up to `high`) | ❌ Vibe 3.1.2: 429 "Rate limit exceeded" (code 1300) on this key's tier; direct calls pass | not tested (same) | not tested; Vibe needs `[[models]]` aliases with `thinking` |

## What remains to make every team run its roles with their model and effort

1. **google**: add the key to the environment's network secrets with header `x-goog-api-key` (the credential form only injects `Authorization: Bearer`, which the native endpoint reads as an OAuth token); then retest Antigravity and `call_model.py`.
2. **mistral**: a key with a higher rate limit (paid tier or Vibe subscription key); then test Vibe with one `[[models]]` alias per effort level.
3. **xai**: native sub-agents give the model per role; the effort per role is proven only through `run_role.py`.
4. **moonshot, alibaba**: no effort per native sub-agent; roles run as headless instances (`run_role.py`), and for alibaba the effort stays the one of `settings.json`.
5. **zhipu**: the project `.claude/agents/` carry Claude models (`fable`, `sonnet`); the zhipu team needs its own role files with GLM models before using native sub-agents.
