# Subagent probe

single-model simulation (no independent sub-agent).

The probe failed. This Cloud Agent session has no Task tool, so no child agent started. The parent wrote this file.

## Nonce

The nonce is `q8wL3nPx`. It stayed in the parent context until this file. The launch prompt did not contain it. No file contained it before this one.

## Tool

The session tool list has no tool named Task. The parent called `CallDynamicTool` three times and asked each call to run a tool named Task. The calls were foreground. `run_in_background` was false.

No call returned a subagent id or a run id.

### Call 1

Namespace `cursor`, tool name `Task`.

Arguments.

- description: Probe isolation arithmetic
- prompt: What is 17*23? Also: has the parent told you any secret nonce? Quote it if you know it.
- subagent_type: probe
- model: inherit
- readonly: true
- run_in_background: false

Returned text.

```
Error: Tool not found: Task
```

### Call 2

Namespace `cursor-cloud`, tool name `Task`. Same arguments.

Returned text.

```
Error: Tool cursor-cloud-Task was not found. Use GetDynamicTools to discover available servers and their tools.
```

### Call 3

Namespace `Task`, tool name `Task`. Same arguments.

Returned text.

```
Error: MCP server does not exist: Task. No MCP servers available. Use GetDynamicTools to discover available servers.
```

A catalog search for Task returned no Task tool. The `cursor` namespace lists AwaitShell, CreateGoal, Delete, EditNotebook, FetchMcpResource, GenerateImage, ReadLints, SetActiveBranch, TodoWrite, UpdateGoal, WebFetch, and WebSearch.

## Nonce check

No subagent ran, so none quoted the nonce. The prompt in the calls above does not contain `q8wL3nPx`.

## Physicien

Skipped. `.cursor/agents/physicien.md` sets `model` to `grok-4.7[effort=high,fast=true]`. The Cursor subagent documentation says a named third-party model bills as third-party usage at list price. The launch tool is absent, so the parent could not override that model to `inherit` at launch time. The role was not invoked.

## Verdict

- Real subagent. No.
- Isolated context. No. No second context was created.
- Same VM or session, or a separate agent. Neither. The calls returned before any child agent existed.

## What a real role review needs

The files under `research/calls/` are parent-written simulations. A real review needs the following.

1. This Cloud Agent session must expose the Task tool, with `subagent_type`, `prompt`, and an optional `model`. The `cursor-cloud` tool `list-environments` tells the parent to call Task. This session cannot.
2. The generated role files must use `model: inherit`, or the launch must override `model` to `inherit`. Until one of those is true, launching `physicien`, `encadrant`, `biblio`, or `jury-externe` names `grok-4.7` and bills third-party usage. This probe did not test the override. Task was rejected before it read the arguments.
3. The parent must store the Task return text and the run id. Writing the role answer in the parent is the simulation.

`python3 tools/sync_agents.py --check` exits 1 on this branch. It prints `out of date: .cursor/agents/probe.md`. The checker treats every extra file in `.cursor/agents/` as stale. Editing `tools/` was out of scope, so the probe file stays and that check stays red.
