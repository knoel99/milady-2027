#!/usr/bin/env python3
"""Per-team settings of a shared race host (infra/deploy/race-host.sh): one Linux user, one clone,
one branch and one systemd service per team on a single VM.

    python3 tools/race_host.py teams                       # teams of race/config.toml with a harness
    python3 tools/race_host.py env --team T --secrets F    # the team's environment file, from the secrets file
    python3 tools/race_host.py setup --team T              # shell commands that install the team's harness
    python3 tools/race_host.py login --team T              # how to log in to the harness with a subscription

The secrets file (root only) holds one KEY=value per line: the provider keys named in
race/config.toml [teams], RUNPOD_API_KEY, GITHUB_TOKEN, and optionally <TEAM>_GPU_BUDGET_USD. For isolation,
REPO_<TEAM> (the team's own private repository, started from tools/race_snapshot.py) and
GITHUB_TOKEN_<TEAM> (a fine-grained token on that repository only) replace the shared REPO and token.
A team's environment file receives only its own provider key and the shared keys, never the keys
of the other teams. Standard library only.
"""

from __future__ import annotations

import argparse
import shlex
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ("RUNPOD_API_KEY", "GITHUB_TOKEN")
# How to log in with a subscription instead of an API key (official docs read on 2026-11-13).
LOGIN = {
    "claude": "claude setup-token   # then put CLAUDE_CODE_OAUTH_TOKEN in the team's environment file",
    "openai": "codex login --device-auth   # enable device-code login in ChatGPT security settings first",
    "google": "agy   # first run asks for an OAuth code over SSH; GEMINI_API_KEY avoids it",
    "xai": "grok login --device-auth",
    "mistral": "none: the Vibe key of the subscription is MISTRAL_API_KEY (chat.mistral.ai, Code > Vibe CLI)",
    "zhipu": "none: the GLM Coding Plan key is ZAI_API_KEY",
    "moonshot": "kimi login   # device code; or MOONSHOT_API_KEY for the API",
    "deepseek": "none: API key DEEPSEEK_API_KEY",
    "alibaba": "none: Model Studio API key DASHSCOPE_API_KEY (the Coding Plan forbids automated use)",
}


def config() -> dict:
    return tomllib.loads((ROOT / "race" / "config.toml").read_text(encoding="utf-8"))


def providers() -> dict:
    return tomllib.loads((ROOT / "agents" / "providers.toml").read_text(encoding="utf-8"))


def teams() -> list[str]:
    p = providers()
    return [t for t in config()["teams"] if p.get(t, {}).get("harness")]


def parse_secrets(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip().removeprefix("export ").strip()] = v.strip().strip("'\"")
    return out


def env_file(team: str, secrets: dict[str, str]) -> str:
    key_var = config()["teams"][team]
    env = {"MILADY_PROVIDER": team, "MILADY_JOB_PREFIX": f"milady-{team}-job-",
           "PATH": f"/home/race-{team}/.npm-global/bin:/home/race-{team}/.local/bin:/usr/local/bin:/usr/bin:/bin"}
    for k in (key_var, *SHARED, "CLAUDE_CODE_OAUTH_TOKEN" if team == "claude" else ""):
        if k and secrets.get(k):
            env[k] = secrets[k]
    # Isolation (race/HOST.md): a team's own repository and a token that reaches it only.
    if secrets.get(f"GITHUB_TOKEN_{team.upper()}"):
        env["GITHUB_TOKEN"] = secrets[f"GITHUB_TOKEN_{team.upper()}"]
    if secrets.get(f"REPO_{team.upper()}"):
        env["RACE_REPO"] = secrets[f"REPO_{team.upper()}"]
    budget = secrets.get(f"{team.upper()}_GPU_BUDGET_USD")
    if budget:
        env["MILADY_GPU_BUDGET_USD"] = budget
    missing = [k for k in (key_var, *SHARED) if k not in env]
    lines = [f"{k}={shlex.quote(v)}" for k, v in env.items()]
    if missing:
        lines.insert(0, f"# MISSING: {' '.join(missing)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("teams")
    for name in ("env", "setup", "login"):
        s = sub.add_parser(name)
        s.add_argument("--team", required=True)
        if name == "env":
            s.add_argument("--secrets", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "teams":
        print(" ".join(teams()))
        return 0
    if a.team not in teams():
        sys.exit(f"unknown team {a.team!r}: {' '.join(teams())}")
    if a.cmd == "env":
        text = env_file(a.team, parse_secrets(a.secrets.read_text(encoding="utf-8")))
        print(text, end="")
        return 1 if text.startswith("# MISSING") else 0
    if a.cmd == "setup":
        print(providers()[a.team]["harness"]["setup"])
        return 0
    print(LOGIN.get(a.team, "see the provider's documentation"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
