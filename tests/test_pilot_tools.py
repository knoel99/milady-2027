"""tools/runpod_job.py against a fake RunPod MCP, and tools/usage_report.py on synthetic transcripts."""

from __future__ import annotations

import argparse
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
    row = json.loads((job_env / "ledger.jsonl").read_text())
    assert row["gpu"] == "NVIDIA GeForce RTX 5090" and row["usd_per_hour"] == 1.19 and row["rc"] == 0


def test_pod_deleted_even_when_polling_crashes(job_env, monkeypatch):
    def boom(url):
        raise KeyboardInterrupt
    monkeypatch.setattr(runpod_job, "http_get", boom)
    mcp = FakeMCP(fail_first=False)
    with pytest.raises(KeyboardInterrupt):
        runpod_job.run(args(log=str(job_env / "job.log")), mcp=mcp, sleep=lambda s: None)
    assert mcp.deleted == ["pod123"]
    assert json.loads((job_env / "ledger.jsonl").read_text())["rc"] is None


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
    assert json.loads((job_env / "ledger.jsonl").read_text())["usd_per_hour"] == 0.34
