# Agents

Provider-neutral definitions of the project's sub-agents.

- `roles/*.md`: one file per role. Header fields: `name`, `description`, `tier` (`frontier`, `standard`, `light`), `reasoning` (`low`, `medium`, `high`, `max`), `read_only`, `needs` (`shell`, `web`), `max_turns`. The body is the mandate, usable as a prompt by any tool.
- `providers.toml`: how tiers, reasoning levels and needs map to each tool.
- `python3 tools/sync_agents.py` regenerates the tool-specific files (today `.claude/agents/*.md`); `--check` fails if they are out of date, and CI runs it.

Edit the roles here, never the generated files. A tool without sub-agents runs a role as a separate session with the body of its file as the prompt.
