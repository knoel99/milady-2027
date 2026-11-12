"""tools/call_model.py and tools/check_calls.py against a local fake of the four API styles.

The fake server records each request body and echoes the requested model, so the tests check
that every provider gets the model id of the role's tier and the effort value of its level, in
the right field, and that check_calls accepts conforming ledgers and rejects tampered ones.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import call_model
import check_calls

PROVIDERS = call_model.load_providers()
TEAMS = [k for k, v in PROVIDERS.items() if "api" in v]
SEEN: list[dict] = []


class Fake(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append({"path": self.path, "body": body})
        model = body.get("model") or self.path.split("/models/")[-1].split(":")[0]
        if self.path.endswith("/messages"):
            out = {"model": model, "content": [{"type": "text", "text": "OK"}],
                   "usage": {"input_tokens": 5, "output_tokens": 3}}
        elif self.path.endswith("/responses"):
            out = {"model": model, "output": [{"content": [{"type": "output_text", "text": "OK"}]}],
                   "usage": {"input_tokens": 5, "output_tokens": 3, "output_tokens_details": {"reasoning_tokens": 7}}}
        elif self.path.endswith("/chat/completions"):
            out = {"model": model, "choices": [{"message": {"content": "OK"}}],
                   "usage": {"prompt_tokens": 5, "completion_tokens": 3,
                             "completion_tokens_details": {"reasoning_tokens": 7}}}
        else:
            out = {"modelVersion": model, "candidates": [{"content": {"parts": [{"text": "OK"}]}}],
                   "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 3, "thoughtsTokenCount": 7}}
        raw = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass


@pytest.fixture()
def fake(tmp_path, monkeypatch):
    server = HTTPServer(("127.0.0.1", 0), Fake)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setenv("MILADY_BASE_URL", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setenv("MILADY_LEDGER", str(tmp_path / "ledger.jsonl"))
    SEEN.clear()
    yield tmp_path / "ledger.jsonl"
    server.shutdown()


def get(body: dict, dotted: str):
    for k in dotted.split("."):
        body = body[k]
    return body


@pytest.mark.parametrize("team", TEAMS)
def test_every_role_gets_its_model_and_effort(fake, team):
    api = PROVIDERS[team]["api"]
    for role in sorted(p.stem for p in call_model.ROLES.glob("*.md")):
        meta, body = call_model.load_role(role)
        e = call_model.call(team, meta["tier"], meta["reasoning"], body, "task", role=role, save=False)
        model, effort = call_model.resolve(PROVIDERS[team], meta["tier"], meta["reasoning"])
        sent = SEEN[-1]["body"]
        assert e["status"] == 200 and e["text"] == "OK"
        assert e["model"] == model and e["response_model"] == model
        if effort is not None:
            assert get(sent, api["effort_field"]) == effort
        for key, value in api.get("extra", {}).items():
            assert sent[key] == value
    assert check_calls.cmd_ledger(type("A", (), {"provider": team, "since": None})()) == 0


def test_exam_and_tampering_are_detected(fake):
    team = "openai"
    since = "0"
    args = type("A", (), {"provider": team, "since": since})()
    assert check_calls.cmd_exam(args) == 1  # nothing called yet
    for role in sorted(p.stem for p in call_model.ROLES.glob("*.md")):
        meta, body = call_model.load_role(role)
        call_model.call(team, meta["tier"], meta["reasoning"], body, "task", role=role, save=False)
    assert check_calls.cmd_exam(args) == 0
    rows = [json.loads(x) for x in fake.read_text().splitlines()]
    rows[0]["effort"] = "low" if rows[0]["effort"] != "low" else "max"  # a call with the wrong effort
    fake.write_text("".join(json.dumps(r) + "\n" for r in rows))
    assert check_calls.cmd_ledger(type("A", (), {"provider": team, "since": None})()) == 1


def test_run_role_dry_run_builds_the_harness_command():
    for team in [k for k, v in PROVIDERS.items() if "harness" in v]:
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "run_role.py"), "--provider", team,
                            "--role", "encadrant", "--task", "-", "--dry-run"],
                           input="claim", capture_output=True, text=True, check=True)
        out = json.loads(r.stdout)
        assert out["command"][0] in {"claude", "codex", "agy", "grok", "vibe", "kimi", "qwen"}
        assert any("<prompt" in c for c in out["command"])
