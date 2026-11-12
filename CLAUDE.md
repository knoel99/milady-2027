# CLAUDE.md

@AGENTS.md

## Claude Code specifics

The rules above are provider-neutral. For Claude Code only:

- Sub-agents are `.claude/agents/*.md`, generated from `agents/roles/` by `tools/sync_agents.py` with the `claude` section of `agents/providers.toml`: never edit them by hand.
- Model and reasoning level: read them with `get_session` in the cloud (otherwise ask); change them with `/model` and `/effort`.
- No ultracode as a session mode: the keyword is reserved for repeated tasks over many independent, verifiable items, naming the model of each step.
