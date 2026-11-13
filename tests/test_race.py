"""Race tooling: progress and lock (race_progress), quota and cache (compute_broker), launch
scripts for every team (race_launch). No cloud call: the broker runs against a fake cloud."""

from __future__ import annotations

import base64
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import compute_broker
import race_launch
import race_progress

COMMON_IDS = [o["id"] for o in race_progress.tomllib.loads(race_progress.COMMON.read_text())["objective"]]


@pytest.mark.parametrize(("value", "baseline", "target", "direction", "expected"), [
    (5.0, 10.0, 0.0, "lower", 0.5),
    (12.0, 10.0, 0.0, "lower", 0.0),     # worse than the baseline
    (-1.0, 10.0, 0.0, "lower", 1.0),     # beyond the target
    (3.0, 1.0, 5.0, "higher", 0.5),
    (None, 1.0, 5.0, "higher", 0.0),     # measurement failed
    (1.5, "none", 2.0, "lower", 1.0),    # nothing existed: reached
    (2.5, "none", 2.0, "lower", 0.0),    # nothing existed: not reached
    (0.5, 1.0, 2.0, "lower", 1.0),       # target on the wrong side: only reaching counts
])
def test_progress(value, baseline, target, direction, expected):
    assert race_progress.progress(value, baseline, target, direction) == pytest.approx(expected)


def objectives_file(team: str, values: dict[str, float]) -> str:
    out = [f'team = "{team}"']
    for cid in COMMON_IDS:
        direction = "higher" if cid in ("C6-comparative-study", "C7-toolbox") else "lower"
        target = 4 if direction == "higher" else 1.0
        out += ["", "[[objective]]", f'id = "{cid}"', f"target = {target}", "baseline = 2.0",
                f"command = \"echo '{{\\\"value\\\": {values.get(cid, 2.0)}}}'\""]
        if direction == "higher":
            out[-2] = "baseline = 0"
    out += ["", "[[objective]]", 'id = "T1-own"', 'offer = "comparative study"', 'metric = "m"',
            'direction = "lower"', "target = 0.0", "baseline = 1.0", "command = \"exit 3\""]
    return "\n".join(out) + "\n"


def test_template_and_common_file_parse():
    race_progress.load(ROOT / "race" / "objectives.template.toml")
    assert len(COMMON_IDS) == 7


def test_lock_measure_and_void(tmp_path, monkeypatch):
    monkeypatch.setattr(race_progress, "LOCKS", tmp_path / "locks.json")
    team = "openai"
    co = tmp_path / team
    f = race_progress.objectives_path(co, team)
    f.parent.mkdir(parents=True)
    f.write_text(objectives_file(team, {"C1-3d-generator": 1.5}))
    assert race_progress.problems(f) == []
    subprocess.run(["git", "init", "-q"], cwd=co, check=True)
    assert subprocess.run([sys.executable, str(ROOT / "tools" / "race_progress.py"), "check", str(f)],
                          capture_output=True, check=False).returncode == 0
    locks = {team: {"sha256": race_progress.sha256(f), "commit": "x", "time": "t"}}
    race_progress.LOCKS.write_text(json.dumps(locks))
    m = race_progress.measure(team, co)
    assert m["lock"] == "locked"
    by_id = {r["id"]: r for r in m["objectives"]}
    assert by_id["C1-3d-generator"]["progress"] == pytest.approx(0.5)  # 2.0 -> 1.5, target 1.0
    assert by_id["T1-own"]["value"] is None and "exit 3" in by_id["T1-own"]["error"]
    assert any(x.startswith("T1-own") for x in m["remaining"])
    assert "Remaining work" in race_progress.as_markdown(m)
    f.write_text(f.read_text().replace("target = 1.0", "target = 1.4", 1))  # lowered ambition after the lock
    m = race_progress.measure(team, co)
    assert m["lock"].startswith("VOID") and m["mean_progress"] == 0


def test_check_rejects_incomplete_file(tmp_path):
    f = tmp_path / "o.toml"
    f.write_text('team = "x"\n[[objective]]\nid = "C1-3d-generator"\ntarget = 1\nbaseline = "none"\ncommand = "true"\n')
    errs = race_progress.problems(f)
    assert any("missing common objective C2-divergence" in e for e in errs)


class FakeCloud:
    def __init__(self):
        self.created, self.deleted, self.status, self.results = [], [], "", b"tarball"

    def create(self, name, user_data, vm_type):
        self.created.append((name, user_data, vm_type))
        return f"srv{len(self.created)}"

    def ip(self, sid):
        return "10.0.0.1"

    def get(self, url):
        return self.status.encode() if url.endswith("status.txt") else self.results

    def delete(self, sid):
        self.deleted.append(sid)


def archive(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for name, text in files.items():
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


@pytest.fixture()
def broker(tmp_path):
    (tmp_path / "tokens.json").write_text(json.dumps({"openai": "tok-a", "claude": "tok-b"}))
    cfg = compute_broker.config()
    cfg["budget"]["cpu_hours"] = 40
    return compute_broker.Broker(tmp_path, "http://broker:8080", FakeCloud(), cfg)


def test_cache_key_ignores_journal_but_not_code():
    a = archive({"experiments/e.py": "x = 1", "research/journal.md": "day 1"})
    b = archive({"experiments/e.py": "x = 1", "research/journal.md": "day 2"})
    c = archive({"experiments/e.py": "x = 2", "research/journal.md": "day 1"})
    k = compute_broker.cache_key
    assert k(a, "run", ["out"], "T") == k(b, "run", ["out"], "T")
    assert k(a, "run", ["out"], "T") != k(c, "run", ["out"], "T")
    assert k(a, "run", ["out"], "T") != k(a, "run --seed 1", ["out"], "T")


def test_broker_quota_cache_and_charge(broker):
    req = {"archive": base64.b64encode(archive({"experiments/e.py": "x"})).decode(),
           "command": "python3 experiments/e.py", "hours": 2}
    assert broker.team_of("tok-a") == "openai" and broker.team_of("nope") is None
    job = broker.submit("openai", req)
    assert job["state"] == "running" and "token" not in job
    script = broker.cloud.created[0][1]
    assert "__" not in script.replace("__pycache__", "")  # every placeholder filled
    assert "http://broker:8080/archives/" in script
    assert broker.submit("openai", req)["state"] == "waiting"  # identical run in progress: attached, free
    assert "error" in broker.submit("openai", dict(req, command="python3 experiments/e.py --seed 1"))  # 32 + 32 > 40
    assert "error" in broker.submit("openai", dict(req, hours=5))  # over max_job_hours
    broker.cloud.status = "DONE rc=0 results.tar.gz ready"
    broker.poll()
    done = broker.db["jobs"][job["id"]]
    assert done["state"] == "done" and broker.cloud.deleted == ["srv1"]
    assert broker.results(done) == b"tarball"
    other = broker.submit("claude", req)  # another team, same code and command: cached, free
    assert other["state"] == "done" and other["cached"] and other["charged"] == 0
    assert len(broker.cloud.created) == 1


def test_broker_failed_job_is_not_cached(broker):
    req = {"archive": base64.b64encode(archive({"experiments/e.py": "y"})).decode(),
           "command": "false", "hours": 1}
    job = broker.submit("openai", req)
    broker.cloud.status = "DONE rc=1 results.tar.gz ready"
    broker.poll()
    assert broker.db["jobs"][job["id"]]["state"] == "failed"
    assert broker.submit("claude", req)["state"] == "running"  # not served from the cache


def test_launch_scripts_for_every_team(monkeypatch):
    cfg = race_launch.config()
    for team, key_var in cfg["teams"].items():
        monkeypatch.setenv(key_var, f"dummy-{team}")
        ud = race_launch.user_data(team, "http://broker:8080", "tok", "abc")
        assert not [w for w in ud.split() if "__" in w and "__TEAM__" not in w and w.isupper()]
        env_b64 = ud.split('" | base64 -d > /etc/race.env')[0].rsplit('echo "', 1)[1]
        env = base64.b64decode(env_b64).decode()
        assert f"MILADY_PROVIDER={team}" in env and f"dummy-{team}" in env
        ms = cfg["main_session"]
        cmd, *_ = race_launch.build_command(team, ms["tier"], ms["reasoning"], 10, "P")
        assert cmd[0] in {"claude", "codex", "agy", "grok", "vibe", "kimi", "qwen", "dsh"} and "P" in cmd
    assert "| claude |" in race_launch.plan()


def test_env_file_survives_bash(monkeypatch, tmp_path):
    key = "sk-$HOME`id`\\'\"x"
    monkeypatch.setenv("OPENAI_API_KEY", key)
    ud = race_launch.user_data("openai", "http://b", "tok", "abc")
    env_b64 = ud.split('" | base64 -d > /etc/race.env')[0].rsplit('echo "', 1)[1]
    f = tmp_path / "race.env"
    f.write_bytes(base64.b64decode(env_b64))
    out = subprocess.run(["bash", "-c", f'set -a; . {f}; printf %s "$OPENAI_API_KEY"'], capture_output=True,
                         text=True, check=True).stdout
    assert out == key


def test_identical_concurrent_run_waits_for_its_twin(broker):
    req = {"archive": base64.b64encode(archive({"experiments/e.py": "z"})).decode(), "command": "run", "hours": 1}
    first = broker.submit("openai", req)
    second = broker.submit("claude", req)
    assert first["state"] == "running" and second["state"] == "waiting" and second["charged"] == 0
    assert len(broker.cloud.created) == 1 and broker.used("claude") == (0.0, 0)
    broker.cloud.status = "DONE rc=0 results.tar.gz ready"
    broker.poll()
    broker.poll()
    assert broker.db["jobs"][second["id"]]["state"] == "done"
    assert broker.results(broker.db["jobs"][second["id"]]) == b"tarball"


def test_goal_is_the_same_in_every_prompt():
    """race/GOAL.md is the one goal: the team prompt and the pilot prompt carry it verbatim."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    goal = (root / "race/GOAL.md").read_text()
    block = re.search(r"## The goal\n\n```\n(.*?)\n```", goal, re.DOTALL).group(1)
    assert "{team}" in block and "GOAL-MET" in block
    assert block in (root / "race/TEAM-PROMPT.md").read_text()
    assert "/goal " + block.replace("{team}", "claude") in (root / "race/PILOT-PROMPT.md").read_text()
