"""tools/runpod_job.py against a fake RunPod MCP, and tools/usage_report.py on synthetic transcripts."""

from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import sys
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import runpod_job
import usage_report


class FakeMCP:
    def __init__(self, fail_first: bool = True):
        self.calls, self.fail_first, self.deleted = [], fail_first, []

    def call(self, tool, args):
        self.calls.append((tool, args))
        if tool == "list-gpu-types":
            return {"gpuTypes": [
                {"id": "NVIDIA RTX PRO 4500 Blackwell", "availability": "LOW", "price": {"secure": 0.72}},
                {"id": "NVIDIA GeForce RTX 5090", "availability": "LOW", "price": {"secure": 1.19}},
                {"id": "NVIDIA RTX A6000", "availability": "NONE", "price": {"secure": 0.59}}]}
        if tool == "create-pod":
            if self.fail_first and args["body"]["gpu"]["id"] == "NVIDIA RTX PRO 4500 Blackwell":
                raise RuntimeError("no capacity")
            return {"id": "pod123", "name": args["body"]["name"]}
        if tool == "list-pods":
            return {"pods": getattr(self, "pods", [])}
        if tool == "list-billing":
            return {"metadata": {"totals": {"totalAmount": 0.0}}}
        if tool == "delete-pod":
            self.deleted.append(args["id"])
            return {}
        raise AssertionError(tool)


def results_tar() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        data = b"{}"
        info = tarfile.TarInfo("experiments/results/pilot_test_output.json")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


@pytest.fixture()
def job_env(tmp_path, monkeypatch):
    monkeypatch.setattr(runpod_job, "LEDGER", tmp_path / "ledger.jsonl")
    monkeypatch.setattr(runpod_job, "ROOT", tmp_path)
    monkeypatch.setattr(runpod_job, "pushed_commit", lambda ref: "a" * 40)
    return tmp_path


def args(**kw):
    base = {"hours": "0.5", "gpu": None, "ref": "HEAD", "outputs": None, "log": "", "command": ["--", "echo", "hi"],
            "over_budget_approved": False}
    base.update(kw)
    return argparse.Namespace(**base)


def test_fallback_collect_delete_and_ledger(job_env, monkeypatch):
    served = {"status.txt": b"2026 boot\n2026 DONE rc=0\n", "results.tar.gz": results_tar(), "job.log": b"ok"}
    monkeypatch.setattr(runpod_job, "http_get", lambda url: served.get(url.rsplit("/", 1)[-1]))
    mcp = FakeMCP()
    rc = runpod_job.run(args(log=str(job_env / "job.log")), mcp=mcp, sleep=lambda s: None)
    assert rc == 0
    created = [a["body"]["gpu"]["id"] for t, a in mcp.calls if t == "create-pod"]
    assert created[0] == "NVIDIA RTX PRO 4500 Blackwell"            # tried first, no capacity
    assert created[-1] == "NVIDIA GeForce RTX 5090"                 # fallback rented
    body = [a["body"] for t, a in mcp.calls if t == "create-pod"][-1]
    assert body["gpu"]["minCudaVersion"] == "12.8" and body["cloud"] == "SECURE" and "8000/http" in body["ports"]
    assert mcp.deleted == ["pod123"]
    assert (job_env / "experiments/results/pilot_test_output.json").exists()
    row = json.loads((job_env / "ledger.jsonl").read_text().splitlines()[-1])
    assert row["gpu"] == "NVIDIA GeForce RTX 5090" and row["usd_per_hour"] == 1.19 and row["rc"] == 0


def test_pod_deleted_even_when_polling_crashes(job_env, monkeypatch):
    def boom(url):
        raise KeyboardInterrupt
    monkeypatch.setattr(runpod_job, "http_get", boom)
    mcp = FakeMCP(fail_first=False)
    with pytest.raises(KeyboardInterrupt):
        runpod_job.run(args(log=str(job_env / "job.log")), mcp=mcp, sleep=lambda s: None)
    assert mcp.deleted == ["pod123"]
    assert json.loads((job_env / "ledger.jsonl").read_text().splitlines()[-1])["rc"] is None


def test_http_get_sends_an_explicit_user_agent(monkeypatch):
    """The RunPod proxy refuses the default Python-urllib agent (403): the status was never read."""
    seen = {}

    class Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(req, timeout=None):
        seen["agent"] = req.get_header("User-agent")
        return Resp(b"DONE rc=0")

    monkeypatch.setattr(runpod_job.urllib.request, "urlopen", fake_urlopen)
    assert runpod_job.http_get("https://pod-8000.proxy.runpod.net/token/status.txt") == b"DONE rc=0"
    assert seen["agent"] == runpod_job.USER_AGENT and "urllib" not in seen["agent"].lower()


def test_prefix_is_per_team_and_a_deleted_pod_stops_the_job(job_env, monkeypatch, tmp_path):
    """Another session sharing the account deleted this session's running pods with its clean-up (pilot)."""
    teams = tmp_path / "race" / "teams" / "alpha"
    teams.mkdir(parents=True)
    (teams / "objectives.toml").write_text('team = "alpha"\n')
    monkeypatch.setattr(runpod_job, "ROOT", tmp_path)
    assert runpod_job.job_prefix() == "milady-alpha-job-"
    monkeypatch.setenv("MILADY_JOB_PREFIX", "x-")
    assert runpod_job.job_prefix() == "x-"

    class Gone:
        def call(self, tool, args):
            raise RuntimeError('get-pod: {"detail": "pod not found", "status": 404}')

    class Unknown:
        def call(self, tool, args):
            raise KeyError(tool)

    assert runpod_job.pod_gone(Gone(), "p") and not runpod_job.pod_gone(Unknown(), "p")


def test_bootstrap_is_valid_bash_and_survives_debian_packages(tmp_path):
    """The pod image has Debian-installed packages that pip cannot uninstall (pilot, 2026-11-12)."""
    import subprocess

    script = tmp_path / "bootstrap.sh"
    script.write_text(runpod_job.BOOTSTRAP)
    assert subprocess.run(["bash", "-n", str(script)], check=False).returncode == 0
    assert "--system-site-packages" in runpod_job.BOOTSTRAP and "--ignore-installed" in runpod_job.BOOTSTRAP


def test_hours_limit_and_no_stock(job_env):
    with pytest.raises(SystemExit):
        runpod_job.run(args(hours="5"), mcp=FakeMCP(), sleep=lambda s: None)
    class Full(FakeMCP):
        def call(self, tool, a):
            if tool == "create-pod":
                self.calls.append((tool, a))
                raise RuntimeError("There are no longer any instances available")
            return super().call(tool, a)
    full = Full()
    assert runpod_job.run(args(gpu="NVIDIA RTX A6000"), mcp=full, sleep=lambda s: None) == 1
    assert {a["body"]["cloud"] for t, a in full.calls if t == "create-pod"} == {"SECURE"}  # NONE is still tried


def line(model, msg_id, effort, out, tools=(), cache_1h=0, read=0, ts="2026-11-20T10:00:00Z"):
    content = [{"type": "tool_use", "name": t} for t in tools] or [{"type": "text", "text": "x"}]
    return json.dumps({"type": "assistant", "effort": effort, "timestamp": ts, "message": {
        "id": msg_id, "model": model, "content": content, "usage": {
            "input_tokens": 10, "output_tokens": out, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": cache_1h,
            "cache_creation": {"ephemeral_1h_input_tokens": cache_1h, "ephemeral_5m_input_tokens": 0},
            "output_tokens_details": {"thinking_tokens": out // 2}}}})


def test_usage_report_counts_costs_and_conformity(tmp_path, monkeypatch):
    monkeypatch.setattr(runpod_job, "LEDGER", tmp_path / "none.jsonl")
    proj = tmp_path / "proj"
    (proj / "s1" / "subagents").mkdir(parents=True)
    (proj / "s1.jsonl").write_text("\n".join([
        line("claude-fable-5-2", "m1", "high", 1000, tools=["Agent"], cache_1h=100_000),
        line("claude-fable-5-2", "m1", "high", 1000, tools=["Bash"]),          # same response, 2nd block
        line("claude-fable-5-2", "m2", "high", 500, read=1_000_000, ts="2026-11-20T12:00:00Z"),
    ]) + "\n")
    sub = proj / "s1" / "subagents"
    (sub / "agent-a1.jsonl").write_text(line("claude-sonnet-5-5", "s1", "medium", 200) + "\n")
    (sub / "agent-a1.meta.json").write_text(json.dumps({"agentType": "biblio", "description": "prior art"}))
    (sub / "agent-a2.jsonl").write_text(line("claude-fable-5-2", "s2", "low", 300) + "\n")
    (sub / "agent-a2.meta.json").write_text(json.dumps({"agentType": "encadrant", "description": "check"}))
    (proj / "s0.jsonl").write_text(line("claude-opus-5-5", "old", "medium", 9999) + "\n")   # an older session
    import os
    os.utime(proj / "s0.jsonl", (1, 1))
    assert usage_report.collect(proj, None)["by_model"]["claude-opus-5-5"]["output"] == 9999     # --all
    r = usage_report.collect(proj)                                                               # latest only
    assert "claude-opus-5-5" not in r["by_model"]
    fable = r["by_model"]["claude-fable-5-2"]
    assert fable["calls"] == 3 and fable["output"] == 1800 and fable["cache_write_1h"] == 100_000
    # main: m1 = 10*8 + 100000*8*2 + 1000*40 ; m2 = 10*8 + 1e6*0.2 + 500*40 ; a2 = 10*8 + 300*40  (per 1e6)
    expected = (80 + 1_600_000 + 40_000 + 80 + 200_000 + 20_000 + 80 + 12_000) / 1e6
    assert fable["usd"] == pytest.approx(round(expected, 2))
    assert r["main_session"]["conforms"] and r["span_hours"] == 2.0
    assert r["tool_calls"] == {"Agent": 1, "Bash": 1}
    calls = {a["type"]: a for a in r["subagents"]["calls"]}
    assert calls["biblio"]["conforms"] is True                    # sonnet / medium as prescribed
    assert calls["encadrant"]["conforms"] is False and calls["encadrant"]["off_spec"] == 1   # effort low
    assert r["subagents"]["nonconforming"] == 1
    assert "NOT CONFORMING" in usage_report.markdown(r)


def test_budget_is_enforced(job_env, monkeypatch):
    cfg = dict(runpod_job.config(), budget_usd=3.0, approval_fraction=0.8)
    monkeypatch.setattr(runpod_job, "config", lambda: cfg)
    monkeypatch.setattr(runpod_job, "http_get", lambda url: b"DONE rc=0" if url.endswith("status.txt") else None)
    monkeypatch.setattr(runpod_job, "spend", lambda: {"usd": 2.5})            # 83 % of 3: refused
    with pytest.raises(SystemExit, match="80%"):
        runpod_job.run(args(), mcp=FakeMCP(), sleep=lambda s: None)
    monkeypatch.setattr(runpod_job, "spend", lambda: {"usd": 1.0})            # 33 %: allowed, but ...
    mcp = FakeMCP(fail_first=False)
    rc = runpod_job.run(args(hours="2", gpu="NVIDIA GeForce RTX 5090,NVIDIA RTX PRO 4500 Blackwell",
                             log=str(job_env / "j.log")), mcp=mcp, sleep=lambda s: None)
    rented = [a["body"]["gpu"]["id"] for t, a in mcp.calls if t == "create-pod"]
    assert rc == 0 and rented == ["NVIDIA RTX PRO 4500 Blackwell"]          # 2 h x $1.19 would pass $3


def test_missing_pod_id_is_cleaned_up(job_env, monkeypatch):
    class Odd(FakeMCP):
        name = "not-created-yet"

        def call(self, tool, args):
            if tool == "create-pod":
                self.name = args["body"]["name"]
                return {"text": "created"}
            if tool == "list-pods":
                return {"pods": [{"id": "podX", "name": self.name}, {"id": "other", "name": "someone-else"}]}
            return super().call(tool, args)
    mcp = Odd(fail_first=False)
    with pytest.raises(SystemExit, match="without a pod id"):
        runpod_job.run(args(), mcp=mcp, sleep=lambda s: None)
    assert mcp.deleted == ["podX"]


def test_whole_budget_usable_when_no_approval_needed(job_env, monkeypatch):
    cfg = dict(runpod_job.config(), budget_usd=3.0, approval_fraction=1.0)
    monkeypatch.setattr(runpod_job, "config", lambda: cfg)
    monkeypatch.setattr(runpod_job, "http_get", lambda url: b"DONE rc=0" if url.endswith("status.txt") else None)
    monkeypatch.setattr(runpod_job, "spend", lambda: {"usd": 2.6})            # 87 %: allowed, job fits
    mcp = FakeMCP(fail_first=False)
    assert runpod_job.run(args(hours="0.5", log=str(job_env / "j.log")), mcp=mcp, sleep=lambda s: None) == 0
    monkeypatch.setattr(runpod_job, "spend", lambda: {"usd": 2.9})            # 0.5 h x $0.72 would not fit
    late = FakeMCP(fail_first=False)
    assert runpod_job.run(args(hours="0.5"), mcp=late, sleep=lambda s: None) == 1
    assert not [c for c in late.calls if c[0] == "create-pod"]


def test_community_cloud_is_tried_when_secure_has_no_capacity(job_env, monkeypatch):
    monkeypatch.setattr(runpod_job, "http_get", lambda url: b"DONE rc=0" if url.endswith("status.txt") else None)

    class SecureFull(FakeMCP):
        def call(self, tool, args):
            if tool == "list-gpu-types":
                return {"gpuTypes": [{"id": "NVIDIA GeForce RTX 4090", "availability": "LOW", "community": True,
                                      "secure": True, "price": {"secure": 0.89, "community": 0.34}},
                                     {"id": "NVIDIA RTX PRO 4500 Blackwell", "availability": "LOW", "community": False,
                                      "secure": True, "price": {"secure": 0.72, "community": 0.34}}]}
            if tool == "create-pod":
                self.calls.append((tool, args))
                if args["body"]["cloud"] == "SECURE":
                    raise RuntimeError("There are no longer any instances available")
                return {"id": "podC", "cost": 0.34}
            return super().call(tool, args)
    mcp = SecureFull()
    assert runpod_job.run(args(gpu="NVIDIA RTX PRO 4500 Blackwell,NVIDIA GeForce RTX 4090",
                               log=str(job_env / "j.log")), mcp=mcp, sleep=lambda s: None) == 0
    community = [a["body"]["gpu"]["id"] for t, a in mcp.calls if t == "create-pod" and a["body"]["cloud"] == "COMMUNITY"]
    assert community == ["NVIDIA GeForce RTX 4090"]          # PRO 4500 is not offered on Community Cloud
    assert json.loads((job_env / "ledger.jsonl").read_text().splitlines()[-1])["usd_per_hour"] == 0.34


def test_shared_credit_guard(job_env, monkeypatch):
    class Billed(FakeMCP):
        def call(self, tool, a):
            if tool == "list-billing":
                return {"metadata": {"totals": {"totalAmount": 144.9}}}
            return super().call(tool, a)
    mcp = Billed(fail_first=False)
    assert runpod_job.run(args(hours="0.5"), mcp=mcp, sleep=lambda s: None) == 1   # 144.9 + 0.36 > 150 - 5
    assert not [c for c in mcp.calls if c[0] == "create-pod"]


def test_team_budget_from_environment(job_env, monkeypatch):
    monkeypatch.setenv("MILADY_GPU_BUDGET_USD", "0.1")
    mcp = FakeMCP(fail_first=False)
    assert runpod_job.run(args(hours="0.5"), mcp=mcp, sleep=lambda s: None) == 1     # 0.5 h x $0.72 > $0.1


def test_review_schedule():
    import review_due
    t = review_due.parse
    s = {"start": t("2026-11-12T00:00:00Z"), "deadline": t("2026-11-14T00:00:00Z"), "encadrant_max_gap_hours": 6}
    none = lambda since, paths: []
    assert review_due.due(t("2026-11-12T03:00:00Z"), [], none, s) == []
    results = lambda since, paths: ["abc 2026 add e4 results"] if "experiments/results" in paths else []
    assert [r for r, _ in review_due.due(t("2026-11-12T03:00:00Z"), [], results, s)] == ["encadrant"]
    work = lambda since, paths: ["abc 2026 code"] if paths == ["."] else []
    assert [r for r, _ in review_due.due(t("2026-11-12T07:00:00Z"), [], work, s)] == ["encadrant"]
    assert review_due.due(t("2026-11-12T05:00:00Z"), [], work, s) == []                     # gap not reached
    jury = review_due.due(t("2026-11-13T01:00:00Z"), [{"role": "encadrant", "time": "2026-11-13T00:30:00Z"}], none, s)
    assert [r for r, _ in jury] == ["jury-externe"] and "50%" in jury[0][1]                 # 25 % and 50 % passed
    done = [{"role": "jury-externe", "time": "2026-11-13T00:10:00Z"}, {"role": "encadrant", "time": "2026-11-13T00:30:00Z"}]
    assert review_due.due(t("2026-11-13T01:00:00Z"), done, none, s) == []


def test_cursor_launch_uses_role_model_and_logs(tmp_path, monkeypatch):
    import cursor_agents as ca
    monkeypatch.setattr(ca, "LEDGER", tmp_path / "runs.jsonl")
    monkeypatch.setattr(ca, "STATE", tmp_path / "state.json")
    sent = []

    class Fake(ca.API):
        def __init__(self):
            pass

        def call(self, method, path, body=None):
            if path == "/models":
                return {"items": [{"id": "grok-4.7", "parameters": [
                    {"id": "fast", "values": [{"value": "true"}, {"value": "false"}]},
                    {"id": "effort", "values": [{"value": v} for v in ("low", "medium", "high", "xhigh")]}]},
                    {"id": "composer-2.5", "parameters": [{"id": "fast", "values": ["true", "false"]}]}]}
            sent.append((method, path, body))
            return {"agent": {"id": "bc-1"}, "run": {"id": "run-1"}}
    task = tmp_path / "t.md"
    task.write_text("do it")
    ns = argparse.Namespace(task=str(task), role="physicien", ref="main", name=None, allow_dropped=False)
    assert ca.cmd_launch(Fake(), ns) == 0
    body = sent[0][2]
    assert body["model"] == {"id": "grok-4.7", "params": [{"id": "effort", "value": "high"}, {"id": "fast", "value": "true"}]}
    assert body["repos"][0]["url"] == "https://github.com/knoel99/milady-2027"
    row = json.loads((tmp_path / "runs.jsonl").read_text())
    assert row["agent"] == "bc-1" and row["run"] == "run-1" and row["dropped"] == []
    assert ca.cmd_check(Fake()) == 0


def test_parallel_jobs_reserve_budget_and_are_capped(job_env, monkeypatch):
    import datetime as dt
    cfg = dict(runpod_job.config(), budget_usd=3.0, max_parallel=2)
    monkeypatch.setattr(runpod_job, "config", lambda: cfg)
    monkeypatch.setattr(runpod_job, "spend", lambda: {"usd": 0.0})
    started = (dt.datetime.now(dt.UTC) - dt.timedelta(minutes=10)).isoformat()
    pod = {"id": "busy", "name": "milady-job-x", "cost": 1.19, "createdAt": started, "env": {"MAX_MIN": "120"}}
    mcp = FakeMCP(fail_first=False)
    mcp.pods = [pod]                       # 1.19 $/h x (2.25 - 0.17) h = $2.48 reserved
    assert runpod_job.run(args(hours="1"), mcp=mcp, sleep=lambda s: None) == 1     # + 0.72 > $3
    assert not [c for c in mcp.calls if c[0] == "create-pod"]
    mcp.pods = [pod, dict(pod, id="busy2")]
    assert runpod_job.run(args(hours="0.1"), mcp=mcp, sleep=lambda s: None) == 1   # max_parallel reached
    jobs = runpod_job.running_jobs(mcp)
    assert len(jobs) == 2 and jobs[0]["reserved_usd"] == pytest.approx(1.19 * (2.25 - 10 / 60), rel=1e-2)


def test_cleanup_deletes_only_this_teams_own_pods(job_env, monkeypatch):
    import datetime as dt
    monkeypatch.setattr(runpod_job, "PREFIX", "milady-cursor-job-")
    old = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=5)).isoformat()      # past every time limit
    new = dt.datetime.now(dt.UTC).isoformat()
    pod = lambda pid, name, created=old: {"id": pid, "name": name, "cost": 0.72, "createdAt": created,
                                           "env": {"MAX_MIN": "30"}}
    mcp = FakeMCP(fail_first=False)
    mcp.pods = [pod("c1", "milady-cursor-job-aaaa"),          # ours, in our ledger, orphan: deleted
                pod("c2", "milady-cursor-job-bbbb"),          # our prefix but not in our ledger: kept
                pod("c3", "milady-cursor-job-cccc", new),     # ours, still running: kept unless --all
                pod("k1", "milady-claude-job-dddd"),          # another team: never
                pod("g1", "milady-job-eeee"),                 # no team prefix: never
                pod("x1", "someone-else")]
    for pid in ("c1", "c3", "k1", "g1"):                      # even a ledger row cannot make another team's pod ours
        runpod_job.ledger_append({"event": "start", "pod": pid})
    runpod_job.cleanup(mcp)
    assert mcp.deleted == ["c1"]
    runpod_job.cleanup(mcp, everything=True)
    assert mcp.deleted == ["c1", "c1", "c3"]                  # the fake list still holds c1
    assert not {"c2", "k1", "g1", "x1"} & set(mcp.deleted)
    assert runpod_job.spend()["jobs"] == 0                    # start rows are not spending
    assert len(runpod_job.running_jobs(mcp)) == 5             # the reservation still sees every team's pods


def test_cleanup_refuses_without_a_team_prefix(job_env, monkeypatch):
    monkeypatch.setattr(runpod_job, "PREFIX", "milady-job-")
    mcp = FakeMCP(fail_first=False)
    mcp.pods = [{"id": "g1", "name": "milady-job-eeee", "createdAt": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(SystemExit, match="team prefix"):
        runpod_job.cleanup(mcp, everything=True)
    assert mcp.deleted == []


def test_run_writes_a_start_row_with_the_pod_id(job_env, monkeypatch):
    monkeypatch.setattr(runpod_job, "http_get", lambda url: b"DONE rc=0" if url.endswith("status.txt") else None)
    assert runpod_job.run(args(log=str(job_env / "j.log")), mcp=FakeMCP(fail_first=False), sleep=lambda s: None) == 0
    rows = [json.loads(x) for x in (job_env / "ledger.jsonl").read_text().splitlines()]
    assert rows[0]["event"] == "start" and rows[0]["pod"] == "pod123" and rows[-1]["rc"] == 0
    assert runpod_job.own_pod_ids() == {"pod123"} and runpod_job.spend()["jobs"] == 1


def test_collect_takes_over_a_pod_after_a_session_restart(job_env, monkeypatch):
    """The session's worker restarted while a job was running: the `run` process and its secret path are gone."""
    monkeypatch.setattr(runpod_job, "PREFIX", "milady-alpha-job-")
    served, execs = {}, []
    # a pod created ten minutes ago: inside its time limit whenever the test runs (a fixed date made the test
    # fail once the real clock passed the limit, 2026-11-13)
    created = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")

    class Pod(FakeMCP):
        def call(self, tool, args):
            if tool == "get-pod":
                return {"id": "pod9", "name": "milady-alpha-job-12345678", "cost": 0.72, "createdAt": created,
                        "gpu": {"id": "NVIDIA RTX PRO 4500 Blackwell"},
                        "env": {"OUTPUTS": "experiments/results", "MAX_MIN": "120", "REF": "a" * 40}}
            if tool == "exec-pod":
                cmd = args["body"]["command"][2]
                execs.append(cmd)
                if cmd.startswith("cat /srv/www/*/status.txt"):
                    return {"stdout": "boot\njob started\n" + ("DONE rc=0\n" if len(execs) > 1 else ""), "exitCode": 0}
                token = cmd.split("/srv/www/")[1].split(" ")[0]
                served[token] = True
                return {"stdout": "", "exitCode": 0}
            return super().call(tool, args)

    def fake_get(url):
        token = url.split("/")[-2]
        if token not in served:
            return None
        return results_tar() if url.endswith("results.tar.gz") else b"bench output"

    monkeypatch.setattr(runpod_job, "http_get", fake_get)
    mcp = Pod()
    a = argparse.Namespace(pod="pod9", outputs=None, log=str(job_env / "collected.log"), now=False)
    assert runpod_job.collect(a, mcp=mcp, sleep=lambda s: None) == 0
    assert mcp.deleted == ["pod9"]
    assert (job_env / "collected.log").read_bytes().startswith(b"bench output")
    row = json.loads((job_env / "ledger.jsonl").read_text().splitlines()[-1])
    assert row["pod"] == "pod9" and row["rc"] == 0 and row["usd_per_hour"] == 0.72 and "collected" in row["command"]
    # a pod of another team is refused before anything is run in it
    monkeypatch.setattr(runpod_job, "PREFIX", "milady-beta-job-")
    with pytest.raises(SystemExit):
        runpod_job.collect(a, mcp=Pod(), sleep=lambda s: None)


def test_exec_runs_only_in_a_pod_of_this_team(job_env, monkeypatch, capsys):
    """`exec` repairs a job in flight: it runs from the clone, in this team's pods only."""
    monkeypatch.setattr(runpod_job, "PREFIX", "milady-alpha-job-")
    seen = []

    class Pod(FakeMCP):
        def call(self, tool, args):
            if tool == "get-pod":
                return {"id": args["id"], "name": "milady-alpha-job-1" if args["id"] == "mine" else "milady-beta-job-1"}
            if tool == "exec-pod":
                seen.append(args["body"]["command"][2])
                return {"stdout": "ok\n", "exitCode": 0}
            return super().call(tool, args)

    a = argparse.Namespace(pod="mine", timeout=30, command=["--", "ls", "experiments/results"])
    assert runpod_job.exec_in_pod(a, mcp=Pod()) == 0
    assert seen == ["cd /workspace/milady && ls experiments/results"] and capsys.readouterr().out == "ok\n"
    with pytest.raises(SystemExit):
        runpod_job.exec_in_pod(argparse.Namespace(pod="theirs", timeout=30, command=["ls"]), mcp=Pod())
    assert len(seen) == 1
