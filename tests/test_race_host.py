"""tools/race_host.py: a team's environment file holds its own provider key and the shared keys only;
race_launch renders the generic team prompt; the host scripts parse."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import race_host
import race_launch

SECRETS = "OPENAI_API_KEY=sk-o\nGEMINI_API_KEY=g-k\nexport RUNPOD_API_KEY='rp'\nGITHUB_TOKEN=gh\nOPENAI_GPU_BUDGET_USD=20\n"


def test_env_file_keeps_other_teams_keys_out():
    env = race_host.env_file("openai", race_host.parse_secrets(SECRETS))
    assert "OPENAI_API_KEY=sk-o" in env and "RUNPOD_API_KEY=rp" in env and "GITHUB_TOKEN=gh" in env
    assert "GEMINI_API_KEY" not in env and "g-k" not in env
    assert "MILADY_PROVIDER=openai" in env and "MILADY_JOB_PREFIX=milady-openai-job-" in env
    assert "MILADY_GPU_BUDGET_USD=20" in env and not env.startswith("# MISSING")


def test_env_file_flags_a_missing_key():
    env = race_host.env_file("deepseek", race_host.parse_secrets(SECRETS))
    assert env.startswith("# MISSING: DEEPSEEK_API_KEY")


def test_every_team_has_a_setup_and_a_login_note():
    for team in race_host.teams():
        assert race_host.providers()[team]["harness"]["setup"]
        assert team in race_host.LOGIN


def test_team_prompt_is_rendered_for_the_team(monkeypatch):
    seen = {}

    def fake_run(cmd, env, cwd, check, stdin=None):
        seen["prompt"] = next(c for c in cmd if "MilaDy race" in c)
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(race_launch.subprocess, "run", fake_run)
    assert race_launch.run_main("mistral", ROOT / "race" / "TEAM-PROMPT.md", 2) == 0
    p = seen["prompt"]
    assert "{team}" not in p and "team `mistral`" in p and "race/teams/mistral/objectives.toml" in p
    assert "no deadline" in p and "research/GOAL-MET" in p


def test_host_scripts_parse():
    for f in ("race-host.sh", "race-team-loop.sh", "racectl"):
        subprocess.run(["bash", "-n", str(ROOT / "infra" / "deploy" / f)], check=True)


def test_team_repository_and_token_replace_the_shared_ones(monkeypatch):
    import race_host

    monkeypatch.setattr(race_host, "config", lambda: {"teams": {"mistral": "MISTRAL_API_KEY"}})
    text = race_host.env_file("mistral", {"MISTRAL_API_KEY": "k", "RUNPOD_API_KEY": "r", "GITHUB_TOKEN": "shared",
                                          "GITHUB_TOKEN_MISTRAL": "own", "REPO_MISTRAL": "https://x/race-mistral.git"})
    assert "GITHUB_TOKEN=own" in text and "shared" not in text
    assert "RACE_REPO=https://x/race-mistral.git" in text


def test_snapshot_removes_every_team_work():
    import race_snapshot

    teams = ["claude", "cursor", "mistral"]
    work = ["site/teams/cursor/report/index.qmd", "race/teams/claude/objectives.toml", "research/journal.md",
            "research/calls/h1-encadrant.md", "experiments/cursor_fm_train.py", "experiments/results/cursor_abc/x.json"]
    keep = ["research/README.md", "race/teams/README.md", "site/teams/index.qmd", "experiments/e1_gissinger.py",
            "tools/race_snapshot.py", "src/milady/storage.py"]
    assert race_snapshot.check(work + keep, teams) == work
