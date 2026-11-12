#!/usr/bin/env python3
"""Drive Cursor Cloud Agents for the Cursor pilot (race/PILOT-CURSOR.md): launch, follow up, wait, report.

Run by the orchestrator (Grok Bot on its cloud computer, or any shell) with CURSOR_API_KEY set
(a Cursor API key, created in the Cursor dashboard). The model and reasoning effort of each run come
from agents/providers.toml [cursor] and the role files, never from the caller: `--role main` is the
main session (race/config.toml [main_session]), any other name is a role of agents/roles/.
Every launch and follow-up is appended to research/cursor-runs.jsonl (model, params, agent, run,
status, usage as returned by the API). Standard library only.

    python3 tools/cursor_agents.py models                    # model ids and parameters the key can use
    python3 tools/cursor_agents.py check                     # every configured model and parameter exists
    python3 tools/cursor_agents.py launch --task FILE [--role main] [--ref main] [--name NAME]
    python3 tools/cursor_agents.py send --agent ID --task FILE [--steer]
    python3 tools/cursor_agents.py wait --agent ID [--run RUN] [--hours 2]
    python3 tools/cursor_agents.py status [--agent ID]
    python3 tools/cursor_agents.py report [--write research/usage/cursor.md]
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "research" / "cursor-runs.jsonl"
STATE = Path(os.environ.get("MILADY_CURSOR_STATE", Path.home() / ".milady" / "cursor-agents.json"))
TERMINAL = {"FINISHED", "ERROR", "CANCELLED", "EXPIRED"}


def cfg() -> dict:
    return tomllib.loads((ROOT / "agents" / "providers.toml").read_text(encoding="utf-8"))["cursor"]


def race() -> dict:
    return tomllib.loads((ROOT / "race" / "config.toml").read_text(encoding="utf-8"))


def role_meta(role: str) -> dict:
    if role == "main":
        ms = race()["main_session"]
        return {"tier": ms["tier"], "reasoning": ms["reasoning"]}
    sys.path.insert(0, str(ROOT / "tools"))
    from sync_agents import parse_role

    meta, _ = parse_role(ROOT / "agents" / "roles" / f"{role}.md")
    return meta


def model_for(role: str) -> dict:
    c, meta = cfg(), role_meta(role)
    params = [{"id": c["cloud_api"]["effort_param"], "value": c["reasoning"][meta["reasoning"]]}]
    if c.get("fast"):
        params.append({"id": c["cloud_api"]["fast_param"], "value": "true"})
    return {"id": c["tier"][meta["tier"]], "params": params}


class API:
    def __init__(self, key: str | None = None):
        self.key = key or os.environ.get(cfg()["cloud_api"]["key_env"])
        if not self.key:
            sys.exit(f"set {cfg()['api']['key_env']} (a Cursor API key from the Cursor dashboard)")
        self.base = cfg()["cloud_api"]["base_url"]

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        auth = base64.b64encode(f"{self.key}:".encode()).decode()
        req = urllib.request.Request(self.base + path, method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    text = r.read().decode()
                    return json.loads(text) if text else {}
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:800]
                if e.code == 429 and attempt < 4:
                    time.sleep(int(e.headers.get("Retry-After", "30")))
                    continue
                raise RuntimeError(f"{method} {path}: HTTP {e.code}: {detail}") from e
        raise RuntimeError(f"{method} {path}: rate limited")


def available(api: API) -> dict[str, set[tuple[str, str]]]:
    """model id (and aliases) -> set of (parameter id, value) the API accepts."""
    out: dict[str, set[tuple[str, str]]] = {}
    for m in api.call("GET", "/models").get("items", []):
        pairs = {(p["id"], str(v.get("value", v) if isinstance(v, dict) else v))
                 for p in m.get("parameters", []) for v in p.get("values", [])}
        for name in [m["id"], *m.get("aliases", [])]:
            out[name] = pairs
    return out


def fit(model: dict, avail: dict) -> tuple[dict, list[str]]:
    """Keep the parameters the API offers for this model; return the dropped ones."""
    if model["id"] not in avail:
        sys.exit(f"model {model['id']} is not offered to this key: run `cursor_agents.py models`")
    keep = [p for p in model["params"] if (p["id"], p["value"]) in avail[model["id"]]]
    dropped = [f"{p['id']}={p['value']}" for p in model["params"] if p not in keep]
    return {"id": model["id"], "params": keep}, dropped


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {"agents": {}}


def save(s: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=1))


def run_id(resp: dict) -> str | None:
    run = resp.get("run") or resp.get("latestRun") or {}
    return run.get("id") or resp.get("runId") or resp.get("id")


def cmd_check(api: API) -> int:
    avail, bad = available(api), 0
    roles = ["main"] + sorted(p.stem for p in (ROOT / "agents" / "roles").glob("*.md"))
    for r in roles:
        m = model_for(r)
        if m["id"] not in avail:
            print(f"FAIL {r}: model {m['id']} not offered")
            bad += 1
            continue
        _, dropped = fit(m, avail)
        print(f"{'FAIL' if dropped else 'ok  '} {r}: {m['id']} {m['params']}" +
              (f"  not offered: {dropped}" if dropped else ""))
        bad += bool(dropped)
    return 1 if bad else 0


def cmd_launch(api: API, a: argparse.Namespace) -> int:
    model, dropped = fit(model_for(a.role), available(api))
    if dropped and not a.allow_dropped:
        sys.exit(f"parameters {dropped} are not offered for {model['id']}: fix agents/providers.toml [cursor] "
                 "or pass --allow-dropped")
    body = {"name": a.name or f"milady-{a.role}-{now()}", "prompt": {"text": Path(a.task).read_text()},
            "model": model, "repos": [{"url": race()["gpu"]["repo"].removesuffix(".git"), "startingRef": a.ref}],
            "workOnCurrentBranch": False, "autoCreatePR": False, "mode": "agent"}
    resp = api.call("POST", "/agents", body)
    agent = resp.get("agent", resp)
    aid, rid = agent.get("id"), run_id(resp)
    s = state()
    s["agents"][aid] = {"role": a.role, "model": model, "launched": now(), "name": body["name"]}
    save(s)
    log({"time": now(), "event": "launch", "agent": aid, "run": rid, "role": a.role, "model": model,
         "dropped": dropped, "task": a.task, "ref": a.ref})
    print(json.dumps({"agent": aid, "run": rid, "model": model, "branch": agent.get("branch")
                      or agent.get("target", {}).get("branchName")}, indent=1))
    return 0


def cmd_send(api: API, a: argparse.Namespace) -> int:
    body = {"prompt": {"text": Path(a.task).read_text()}}
    if a.steer:
        body["delivery"] = "steer"
    resp = api.call("POST", f"/agents/{a.agent}/runs", body)
    rid = run_id(resp)
    log({"time": now(), "event": "send", "agent": a.agent, "run": rid, "task": a.task, "steer": a.steer,
         "delivery": resp.get("delivery")})
    print(json.dumps({"agent": a.agent, "run": rid, "delivery": resp.get("delivery")}))
    return 0


def latest_run(api: API, aid: str) -> dict:
    agent = api.call("GET", f"/agents/{aid}")
    run = agent.get("latestRun") or agent.get("run") or {}
    if not run:
        runs = api.call("GET", f"/agents/{aid}/runs").get("items", [])
        run = runs[0] if runs else {}
    return {"agent": agent, "run": run}


def cmd_wait(api: API, a: argparse.Namespace) -> int:
    t0 = time.time()
    while True:
        if a.run:
            run = api.call("GET", f"/agents/{a.agent}/runs/{a.run}")
        else:
            run = latest_run(api, a.agent)["run"]
        status = run.get("status", "?")
        if status in TERMINAL:
            break
        if time.time() - t0 > a.hours * 3600:
            print(f"still {status} after {a.hours} h", file=sys.stderr)
            return 2
        time.sleep(60)
    agent = api.call("GET", f"/agents/{a.agent}")
    log({"time": now(), "event": "done", "agent": a.agent, "run": run.get("id"), "status": status,
         "usage": run.get("usage") or agent.get("usage"), "summary": str(run.get("summary", ""))[:500]})
    print(json.dumps({"status": status, "summary": run.get("summary"), "usage": run.get("usage") or agent.get("usage"),
                      "branch": agent.get("branch") or agent.get("target", {}).get("branchName")}, indent=1))
    return 0 if status == "FINISHED" else 1


def cmd_status(api: API, a: argparse.Namespace) -> int:
    ids = [a.agent] if a.agent else list(state()["agents"])
    for aid in ids:
        lr = latest_run(api, aid)
        meta = state()["agents"].get(aid, {})
        print(f"{aid}  {meta.get('role', '?'):<12} agent {lr['agent'].get('status')}  "
              f"run {lr['run'].get('id')} {lr['run'].get('status')}")
    return 0


def report() -> str:
    rows = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()] if LEDGER.exists() else []
    launches = [r for r in rows if r["event"] == "launch"]
    done = [r for r in rows if r["event"] == "done"]
    lines = ["# Cursor pilot: runs and usage", "", f"Generated {now()} by `tools/cursor_agents.py report`.", "",
             (f"- agents launched: {len(launches)}; follow-ups: {sum(r['event'] == 'send' for r in rows)}; "
              f"runs finished: {sum(r['status'] == 'FINISHED' for r in done)}; failed: "
              f"{sum(r['status'] != 'FINISHED' for r in done)}"), "",
             "| time | agent | role | model | params | dropped |", "|---|---|---|---|---|---|"]
    for r in launches:
        p = ", ".join(f"{x['id']}={x['value']}" for x in r["model"]["params"])
        lines.append(f"| {r['time']} | {r['agent']} | {r['role']} | {r['model']['id']} | {p} | "
                     f"{', '.join(r['dropped']) or '-'} |")
    lines += ["", "| time | agent | run | status | usage |", "|---|---|---|---|---|"]
    for r in done:
        lines.append(f"| {r['time']} | {r['agent']} | {r['run']} | {r['status']} | `{json.dumps(r.get('usage'))}` |")
    off = [r for r in launches if r["dropped"]]
    lines += ["", f"Runs with a parameter not applied: {len(off)}" + (" (NOT CONFORMING)" if off else "")]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    sub.add_parser("check")
    s = sub.add_parser("launch")
    s.add_argument("--task", required=True)
    s.add_argument("--role", default="main")
    s.add_argument("--ref", default="main", help="branch or commit the agent starts from")
    s.add_argument("--name")
    s.add_argument("--allow-dropped", action="store_true", help="launch even if a parameter is not offered")
    s = sub.add_parser("send")
    s.add_argument("--agent", required=True)
    s.add_argument("--task", required=True)
    s.add_argument("--steer", action="store_true", help="add to the running turn instead of queueing")
    s = sub.add_parser("wait")
    s.add_argument("--agent", required=True)
    s.add_argument("--run")
    s.add_argument("--hours", type=float, default=2)
    s = sub.add_parser("status")
    s.add_argument("--agent")
    s = sub.add_parser("report")
    s.add_argument("--write")
    a = ap.parse_args()
    if a.cmd == "report":
        text = report()
        if a.write:
            Path(a.write).parent.mkdir(parents=True, exist_ok=True)
            Path(a.write).write_text(text)
        print(text)
        return 0
    api = API()
    if a.cmd == "models":
        for m in api.call("GET", "/models").get("items", []):
            params = {p["id"]: [v.get("value", v) if isinstance(v, dict) else v for v in p.get("values", [])]
                      for p in m.get("parameters", [])}
            print(f"{m['id']:<28} {m.get('displayName', ''):<28} aliases={m.get('aliases', [])} params={params}")
        return 0
    return {"check": cmd_check, "launch": cmd_launch, "send": cmd_send, "wait": cmd_wait,
            "status": cmd_status}[a.cmd](api, *([] if a.cmd == "check" else [a]))


if __name__ == "__main__":
    sys.exit(main())
