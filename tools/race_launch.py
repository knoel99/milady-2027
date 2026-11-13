#!/usr/bin/env python3
"""Launch and collect the race: one Scaleway VM per team running its own harness headless.

On the user's machine (holds the provider keys, the Scaleway key and GitHub access):
    python3 tools/race_launch.py plan                          # harness, models and efforts per team
    python3 tools/race_launch.py user-data --team T --broker-url URL --broker-token TOK > ud.sh
    python3 tools/race_launch.py launch --team T --broker-url URL --state DIR
    python3 tools/race_launch.py collect --team T --state DIR [--push]
On the team VM (called by infra/deploy/race-team.sh):
    python3 tools/race_launch.py run-main --team T --prompt-file race/BRIEF.md --iteration 3

The team's provider key is read from the variable named in race/config.toml [teams] and written
into the VM's user data: use only keys capped in the provider's console. Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import secrets
import shlex
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from call_model import load_providers, load_role, resolve
from run_role import build_command

CONFIG = ROOT / "race" / "config.toml"
TEAM_SCRIPT = ROOT / "infra" / "deploy" / "race-team.sh"


def config() -> dict:
    return tomllib.loads(CONFIG.read_text(encoding="utf-8"))


def deadline_epoch(cfg: dict) -> int:
    return int(dt.datetime.fromisoformat(cfg["deadline"]).timestamp())


def plan() -> str:
    cfg, providers = config(), load_providers()
    roles = sorted(p.stem for p in (ROOT / "agents" / "roles").glob("*.md"))
    ms = cfg["main_session"]
    lines = ["| team | harness | main session | " + " | ".join(roles) + " |",
             "|---" * (3 + len(roles)) + "|"]
    for team in cfg["teams"]:
        p = providers[team]
        main_m, main_e = resolve(p, ms["tier"], ms["reasoning"], api=False)
        cells = []
        for r in roles:
            meta, _ = load_role(r)
            m, e = resolve(p, meta["tier"], meta["reasoning"])
            cells.append(f"{m} / {e}")
        lines.append(f"| {team} | {p['harness']['name']} | {main_m} / {main_e} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def user_data(team: str, broker_url: str, broker_token: str, token: str) -> str:
    cfg, providers = config(), load_providers()
    key_var = cfg["teams"][team]
    key = os.environ.get(key_var)
    if not key:
        sys.exit(f"{key_var} is not set: export the capped key of {team} first")
    env = {"MILADY_PROVIDER": team, key_var: key, "BROKER_URL": broker_url, "BROKER_TOKEN": broker_token,
           "PATH": "/root/.local/bin:/usr/local/bin:/usr/bin:/bin",
           "IS_SANDBOX": "1"}  # the VM is a throwaway sandbox; some harnesses check it before skipping prompts
    env_text = "".join(f"{k}={shlex.quote(v)}\n" for k, v in env.items())  # sourced by bash: no expansion
    setup = providers[team]["harness"]["setup"]
    script = TEAM_SCRIPT.read_text()
    for k, v in {"__TOKEN__": token, "__TEAM__": team, "__REPO__": cfg["repo"], "__TAG__": cfg["start_tag"],
                 "__DEADLINE__": str(deadline_epoch(cfg)),
                 "__ENV_B64__": base64.b64encode(env_text.encode()).decode(),
                 "__SETUP_B64__": base64.b64encode(setup.encode()).decode()}.items():
        script = script.replace(k, v)
    return script


def run_main(team: str, prompt_file: Path, iteration: int | None) -> int:
    cfg = config()
    ms = cfg["main_session"]
    prompt = prompt_file.read_text(encoding="utf-8").replace("{team}", team)
    if iteration:
        now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
        prompt += (f"\n\n---\n\nYou are team `{team}`. Invocation {iteration} of your harness; now {now}; "
                   "there is no deadline, only the budget. You have no memory of earlier invocations: read "
                   "`research/journal.md`, `research/hypotheses.json` and `git log` first, then carry on "
                   "where the previous invocation stopped. Commit before you finish.\n")
    cmd, env, model, effort, _ = build_command(team, ms["tier"], ms["reasoning"], ms["max_turns"], prompt)
    print(f"[run-main {team} model={model} effort={effort} iteration={iteration}]", flush=True)
    return subprocess.run(cmd, env=env, cwd=ROOT, check=False).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    s = sub.add_parser("user-data")
    s.add_argument("--team", required=True)
    s.add_argument("--broker-url", required=True)
    s.add_argument("--broker-token", required=True)
    s = sub.add_parser("launch")
    s.add_argument("--team", required=True)
    s.add_argument("--broker-url", required=True)
    s.add_argument("--state", type=Path, required=True, help="directory holding tokens.json of the broker")
    s = sub.add_parser("collect")
    s.add_argument("--team", required=True)
    s.add_argument("--state", type=Path, required=True)
    s.add_argument("--push", action="store_true", help="push race/<team> to origin")
    s = sub.add_parser("run-main")
    s.add_argument("--team", required=True)
    s.add_argument("--prompt-file", type=Path, required=True)
    s.add_argument("--iteration", type=int)
    a = ap.parse_args()

    if a.cmd == "plan":
        print(plan())
        return 0
    if a.cmd == "user-data":
        print(user_data(a.team, a.broker_url, a.broker_token, secrets.token_hex(16)))
        return 0
    if a.cmd == "run-main":
        return run_main(a.team, a.prompt_file, a.iteration)

    teams_path = a.state / "teams.json"
    teams = json.loads(teams_path.read_text()) if teams_path.exists() else {}
    if a.cmd == "launch":
        from compute_broker import Scaleway

        cfg = config()
        broker_token = json.loads((a.state / "tokens.json").read_text())[a.team]
        token = secrets.token_hex(16)
        sid = Scaleway(cfg["machines"]["zone"]).create(f"race-team-{a.team}",
                                                       user_data(a.team, a.broker_url, broker_token, token),
                                                       cfg["machines"]["team_vm"])
        teams[a.team] = {"server": sid, "token": token, "launched": dt.datetime.now(dt.UTC).isoformat()}
        teams_path.write_text(json.dumps(teams, indent=1))
        teams_path.chmod(0o600)
        print(f"{a.team}: server {sid}; status at http://<ip>:8000/{token}/status.txt")
        return 0
    # collect
    from compute_broker import Scaleway

    t = teams[a.team]
    ip = Scaleway(config()["machines"]["zone"]).ip(t["server"])
    base = f"http://{ip}:8000/{t['token']}/"
    print(urllib.request.urlopen(base + "status.txt", timeout=60).read().decode()[-1500:])
    bundle = a.state / f"{a.team}.bundle"
    bundle.write_bytes(urllib.request.urlopen(base + "branch.bundle", timeout=300).read())
    branch = f"race/{a.team}"
    subprocess.run(["git", "fetch", "-q", str(bundle), f"+{branch}:{branch}"], cwd=ROOT, check=True)
    print(f"fetched {branch} at {subprocess.check_output(['git', 'rev-parse', '--short', branch], cwd=ROOT, text=True).strip()}")
    if a.push:
        subprocess.run(["git", "push", "-q", "--force", "origin", branch], cwd=ROOT, check=True)
        print(f"pushed {branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
