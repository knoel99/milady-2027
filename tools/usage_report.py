#!/usr/bin/env python3
"""Usage report of a Claude Code session: tokens, API-equivalent cost, sub-agents, time, GPU spend.

Reads the session transcripts Claude Code keeps under ~/.claude/projects/<project>/ (one JSONL file
per session, one per sub-agent under <session>/subagents/ with a .meta.json naming its type), counts
each API response once (by message id), and reports per model: input, cache writes (5 min and
1 h), cache reads, output (with thinking) and the cost at the prices of milady.toml
[pricing]. In a Claude Code session on a subscription the cost is an API-equivalent figure, not
a bill. It also lists every sub-agent call with its type, model and effort, checks the roles of
agents/roles/ against their prescribed model and effort, and adds the GPU spend of
research/compute-ledger.jsonl and the role calls of research/model-calls.jsonl.

    python3 tools/usage_report.py                         # markdown to stdout
    python3 tools/usage_report.py --write research/usage  # also writes latest.md and latest.json
    python3 tools/usage_report.py --all                   # every session of the project, not only the latest
    python3 tools/usage_report.py --projects DIR          # another transcripts directory

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "milady.toml"
TOKEN_KEYS = ("input", "cache_write_5m", "cache_write_1h", "cache_read", "output", "thinking")


def default_projects() -> Path:
    return Path.home() / ".claude" / "projects" / ("-" + str(ROOT).strip("/").replace("/", "-"))


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def responses(rows: list[dict]) -> list[dict]:
    """One record per API response (assistant lines repeat per content block)."""
    seen: dict[str, dict] = {}
    out = []
    for d in rows:
        if d.get("type") != "assistant":
            continue
        m = d.get("message", {})
        key = m.get("id") or d.get("requestId") or d.get("uuid")
        tools = [c.get("name") for c in m.get("content", []) if c.get("type") == "tool_use"]
        if key in seen:  # same response, another content block
            seen[key]["tools"] += tools
            continue
        if not m.get("usage"):
            continue
        u = m["usage"]
        cc = u.get("cache_creation") or {}
        w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
        w5m = cc.get("ephemeral_5m_input_tokens")
        if w5m is None:
            w5m = (u.get("cache_creation_input_tokens") or 0) - w1h
        out.append({"model": m.get("model") or d.get("requestedModel"), "effort": d.get("effort"),
                    "time": d.get("timestamp"), "speed": u.get("speed"),
                    "input": u.get("input_tokens") or 0, "cache_write_5m": w5m, "cache_write_1h": w1h,
                    "cache_read": u.get("cache_read_input_tokens") or 0, "output": u.get("output_tokens") or 0,
                    "thinking": (u.get("output_tokens_details") or {}).get("thinking_tokens") or 0,
                    "tools": tools})
        seen[key] = out[-1]
    return out


def cost(r: dict, pricing: dict) -> float:
    p = pricing.get(r["model"]) or {}
    if not p:
        return 0.0
    inp, out = p["input"], p["output"]
    m = 2.0 if r.get("speed") == "fast" else 1.0
    return m * (r["input"] * inp + r["cache_write_5m"] * inp * p.get("cache_write_5m_x", 1.25)
                + r["cache_write_1h"] * inp * p.get("cache_write_1h_x", 2.0)
                + r["cache_read"] * p.get("cache_read", inp * 0.1) + r["output"] * out) / 1e6


def role_expectations() -> dict[str, tuple[str, str]]:
    sys.path.insert(0, str(ROOT / "tools"))
    from call_model import load_providers, load_role, resolve

    claude = load_providers()["claude"]
    out = {}
    for f in sorted((ROOT / "agents" / "roles").glob("*.md")):
        meta, _ = load_role(f.stem)
        out[f.stem] = resolve(claude, meta["tier"], meta["reasoning"])  # (model id, effort)
    return out


def off_spec(rs: list[dict], model: str, effort: str) -> int:
    """Number of responses served by another model or at another effort than prescribed."""
    return sum(1 for r in rs if r["model"] != model or (r["effort"] and r["effort"] != effort))


def collect(projects: Path, session: str | None = "latest") -> dict:
    """session: a session id, "latest" (most recently written transcript) or None for all sessions."""
    cfg = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    pricing = cfg.get("pricing", {})
    expected = role_expectations()
    sessions, agents = [], []
    files = sorted(projects.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)
    if session == "latest":
        files = files[-1:]
    elif session:
        files = [f for f in files if f.stem == session]
    for f in files:
        sessions.append({"id": f.stem, "responses": responses(read_jsonl(f))})
        for sub in sorted((projects / f.stem / "subagents").glob("agent-*.jsonl")):
            meta_path = sub.with_suffix("").with_suffix(".meta.json")
            meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
            agents.append({"id": sub.stem, "session": f.stem, "type": meta.get("agentType", "?"),
                           "description": meta.get("description", ""), "responses": responses(read_jsonl(sub))})
    by_model: dict[str, dict] = defaultdict(lambda: dict.fromkeys((*TOKEN_KEYS, "calls", "usd"), 0))
    times = []
    for scope in [s["responses"] for s in sessions] + [a["responses"] for a in agents]:
        for r in scope:
            b = by_model[r["model"] or "?"]
            for k in TOKEN_KEYS:
                b[k] += r[k]
            b["calls"] += 1
            b["usd"] += cost(r, pricing)
            if r["time"]:
                times.append(r["time"])
    tool_counts: dict[str, int] = defaultdict(int)
    for s in sessions:
        for r in s["responses"]:
            for t in r["tools"]:
                tool_counts[t] += 1
    agent_rows, mismatches = [], []
    for a in agents:
        rs = a["responses"]
        models = sorted({r["model"] for r in rs if r["model"]})
        efforts = sorted({r["effort"] for r in rs if r["effort"]})
        usd = sum(cost(r, pricing) for r in rs)
        row = {"id": a["id"], "type": a["type"], "description": a["description"][:80], "models": models,
               "efforts": efforts, "calls": len(rs), "output": sum(r["output"] for r in rs), "usd": round(usd, 4)}
        if a["type"] in expected:
            want_model, want_effort = expected[a["type"]]
            row["off_spec"] = off_spec(rs, want_model, want_effort)
            ok = row["off_spec"] == 0
            row["expected"] = f"{want_model} / {want_effort}"
            row["conforms"] = ok
            if not ok:
                mismatches.append(row)
        agent_rows.append(row)
    ms = cfg.get("main_session", {})
    main_rs = [r for x in sessions for r in x["responses"]]
    sys.path.insert(0, str(ROOT / "tools"))
    from call_model import load_providers, resolve

    want_main = resolve(load_providers()["claude"], ms.get("tier", "frontier"), ms.get("reasoning", "high"))
    main_models = sorted({r["model"] for r in main_rs if r["model"]})
    main_efforts = sorted({r["effort"] for r in main_rs if r["effort"]})
    main = {"models": main_models, "efforts": main_efforts, "expected": f"{want_main[0]} / {want_main[1]}",
            "responses": len(main_rs), "off_spec": off_spec(main_rs, *want_main)}
    main["conforms"] = bool(main_rs) and main["off_spec"] == 0
    start, end = (min(times), max(times)) if times else (None, None)
    hours = None
    if start:
        t = [dt.datetime.fromisoformat(x) for x in (start, end)]
        hours = round((t[1] - t[0]).total_seconds() / 3600, 2)
    sys.path.insert(0, str(ROOT / "tools"))
    from runpod_job import spend

    role_ledger = ROOT / "research" / "model-calls.jsonl"
    role_calls = len([x for x in role_ledger.read_text().splitlines() if x.strip()]) if role_ledger.exists() else 0
    by_type: dict[str, int] = defaultdict(int)
    for a in agents:
        by_type[a["type"]] += 1
    return {"generated": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "projects": str(projects),
            "sessions": len(sessions), "main_session": main, "first": start, "last": end, "span_hours": hours,
            "by_model": {k: {**v, "usd": round(v["usd"], 2)} for k, v in by_model.items()},
            "total_usd": round(sum(v["usd"] for v in by_model.values()), 2),
            "subagents": {"count": len(agents), "by_type": dict(by_type), "calls": agent_rows,
                          "nonconforming": len(mismatches)},
            "tool_calls": dict(sorted(tool_counts.items(), key=lambda x: -x[1])),
            "role_calls_via_tools": role_calls, "gpu": spend()}


def markdown(r: dict) -> str:
    out = [f"# Usage report ({r['generated']})", "",
           f"Sessions: {r['sessions']}; first response {r['first']}; last {r['last']}; span {r['span_hours']} h.",
           f"Main session: models {r['main_session']['models']}, efforts {r['main_session']['efforts']}; expected "
           f"{r['main_session']['expected']}: " + ("conforms." if r["main_session"]["conforms"] else
           f"**NOT CONFORMING** ({r['main_session']['off_spec']} of {r['main_session']['responses']} responses off spec)."),
           f"API-equivalent cost of the Claude calls: **${r['total_usd']}** (prices of milady.toml [pricing]).",
           f"GPU: {r['gpu']['jobs']} job(s), {r['gpu']['hours']} h, **${r['gpu']['usd']}**"
           + (f" of a ${r['gpu']['budget_usd']} budget." if r["gpu"].get("budget_usd") else "."), "",
           "| model | API calls | input | cache write 5m | cache write 1h | cache read | output | of which thinking | cost |",
           "|---|---|---|---|---|---|---|---|---|"]
    for m, v in sorted(r["by_model"].items(), key=lambda x: -x[1]["usd"]):
        out.append(f"| {m} | {v['calls']} | {v['input']:,} | {v['cache_write_5m']:,} | {v['cache_write_1h']:,} | "
                   f"{v['cache_read']:,} | {v['output']:,} | {v['thinking']:,} | ${v['usd']} |")
    s = r["subagents"]
    out += ["", f"Sub-agents: {s['count']} call(s), {s['nonconforming']} not conforming to agents/roles/; by type {s['by_type']}.", ""]
    if s["calls"]:
        out += ["| type | models | efforts | expected | API calls | output | cost | description |", "|---|---|---|---|---|---|---|---|"]
        for a in s["calls"]:
            flag = "" if a.get("conforms", True) else f" **NOT CONFORMING** ({a['off_spec']}/{a['calls']} off spec)"
            out.append(f"| {a['type']} | {', '.join(a['models'])} | {', '.join(a['efforts'])} | "
                       f"{a.get('expected', '–')}{flag} | {a['calls']} | {a['output']:,} | ${a['usd']} | {a['description']} |")
    out += ["", f"Role calls through tools/call_model.py or run_role.py: {r['role_calls_via_tools']}.",
            f"Tool calls of the main session: {r['tool_calls']}."]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--projects", type=Path, default=None)
    ap.add_argument("--write", type=Path, help="directory for latest.md and latest.json")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--session", help="one session id (default: the most recently written transcript)")
    g.add_argument("--all", action="store_true", help="every session of the project")
    a = ap.parse_args()
    projects = a.projects or default_projects()
    if not projects.exists():
        sys.exit(f"no transcripts in {projects}")
    r = collect(projects, None if a.all else (a.session or "latest"))
    md = markdown(r)
    if a.write:
        a.write.mkdir(parents=True, exist_ok=True)
        (a.write / "latest.md").write_text(md, encoding="utf-8")
        (a.write / "latest.json").write_text(json.dumps(r, indent=1), encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
