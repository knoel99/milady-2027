# Race host: several teams on one Scaleway VM

One VM runs the teams that have no cloud agent of their own (today: `openai`, `google`, `mistral`, `zhipu`, `moonshot`, `deepseek`, `alibaba`; `claude` runs in a Claude Code cloud session, `xai` in Cursor). Each team gets its own Linux user, its own clone of the repository on its own branch `race/<team>`, its own Python environment, its own harness and credentials, and its own systemd service; GPU work goes to RunPod with the team's pod prefix.

**Why clones and not worktrees.** Git worktrees of one clone share one `.git` directory: every team could read and rewrite the branches of the others, and `race/BRIEF.md` says a team cannot see the other teams. A clone per Linux user (home in mode 700, `/proc` mounted with `hidepid`, systemd CPU and memory quotas per team) keeps files, credentials and processes apart for the price of a few hundred MB per clone.

## 1. The VM

| | Choice |
|---|---|
| Type | POP2-HC-32C-64G (32 dedicated vCPU, 64 GB, about 0.85 EUR/h), or COMPUTE3-X32C-64G; one per zone with the current quotas (pl-waw-2, it-mil-1, nl-ams-1). Each team gets 4 cores and 12 GB (`CPU_QUOTA`, `MEM_MAX` of `race-host.sh`) |
| Image, disk | Ubuntu 24.04 (noble), 150 GB local or block SSD (seven Python environments, harnesses, data of `--quick` runs) |
| Access | your SSH key in the Scaleway console; no secret in the cloud-init user data |

## 2. Install

On the VM, as root:

```bash
git clone https://github.com/knoel99/milady-2027.git /opt/milady-src && cd /opt/milady-src
install -d -m 700 /etc/race && nano /etc/race/secrets.env      # see below, then chmod 600
TEAMS="openai google mistral zhipu moonshot deepseek alibaba" bash infra/deploy/race-host.sh
```

`/etc/race/secrets.env`, one `KEY=value` per line: the provider key of each team, named as in `race/config.toml` `[teams]` (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `ZAI_API_KEY`, `MOONSHOT_API_KEY`, `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY`), `RUNPOD_API_KEY`, `GITHUB_TOKEN` (fine-grained, this repository only, contents read and write), and optionally `<TEAM>_GPU_BUDGET_USD`. Cap every API key in the provider's console. Each team's `/etc/race/<team>.env` receives only its own key and the shared ones (`tools/race_host.py env`).

## 3. Log in, check, start

```bash
racectl login openai      # subscriptions only: prints the login command, opens a shell as race-openai
racectl check openai      # model and effort per role, a dry run of the harness, one API call per role
racectl start openai      # systemd service race@openai: loops race/TEAM-PROMPT.md, pushes race/openai
racectl status            # every team: state, iteration, last commit, last log line
racectl logs openai 100
racectl stop openai       # ends after the current invocation; `systemctl stop race@openai` stops now
```

Logins with a subscription (`tools/race_host.py login --team <team>`): Codex `codex login --device-auth`, Antigravity OAuth code over SSH (or `GEMINI_API_KEY`), Kimi `kimi login`. Mistral, Z.ai, DeepSeek and Alibaba use their key directly.

## 4. What the loop does

`infra/deploy/race-team-loop.sh` invokes the team's harness with `race/TEAM-PROMPT.md` (main session model and effort of `race/config.toml` `[main_session]`, mapped by `agents/providers.toml`), pushes `race/<team>` after every invocation, and stops when `~/STOP` exists, when the team commits `research/GOAL-MET` (its goal met, on the budget, as for the Claude pilot), or after three short failures in a row (cap spent or login expired). There is no deadline. At the end it runs `tools/runpod_job.py cleanup`, which deletes only that team's own pods.

## 5. Before starting all teams

Start one team first (for example `mistral`, the cheapest), watch one or two invocations (`racectl logs`), and only then the others. Untested so far on a real VM: the non-interactive flags of each harness (`agents/providers.toml` `[<provider>.harness]`, from their documentation), the Kimi and DeepSeek effort settings, and `npx playwright install --with-deps` on the host.

## 6. No access to the other teams' work

A team must not see the reports, results or branches of the other teams, nor the published site (`race/BRIEF.md`). Three locks:

1. **Its own repository, without any team's work.** On a machine with the main repository, `python3 tools/race_snapshot.py list` shows what is removed (every `site/teams/<team>/`, `race/teams/<team>/`, `experiments/<team>_*`, `experiments/results/<team>_*`, and `research/` except its README); `python3 tools/race_snapshot.py build --branch race-start` makes one commit without history. Create one private repository per team (for example `knoel99/milady-race-mistral`), push `race-start` to it as `main`, and name it in the secrets: `REPO_MISTRAL=https://github.com/knoel99/milady-race-mistral.git`.
2. **A token that reaches that repository only**: a fine-grained token per team, contents read and write on its repository only, as `GITHUB_TOKEN_MISTRAL=…`. `tools/race_host.py env` gives the team its own repository and token instead of the shared ones; with the shared token the team could fetch every branch of the main repository.
3. **The site closed**: `race-host.sh` maps `knoel99.github.io` to nowhere in `/etc/hosts`.

At the end, the owner brings each team's branch back into the main repository under its own paths (`research/teams/<team>/`, `site/teams/<team>/`). A Claude Code cloud session or a Cursor Cloud Agent on the main repository sees everything it holds: for them, start from the same snapshot in a repository of their own.
