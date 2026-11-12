#!/usr/bin/env python3
"""Lock and measure each team's quantified objectives: progress and remaining work (RAF).

    python3 tools/race_progress.py check FILE
        Validate an objectives file against race/objectives.common.toml.
    python3 tools/race_progress.py lock --team T --checkout DIR
        Record the sha256 of DIR/race/teams/T/objectives.toml in race/locks.json (day 1).
    python3 tools/race_progress.py measure --team T --checkout DIR [--json]
        Run every measurement command in DIR (a clean checkout of race/T), compute progress
        (value - baseline) / (target - baseline) clipped to [0, 1], list the remaining work,
        and summarise the role-call ledger with tools/check_calls.py.
    python3 tools/race_progress.py report --checkouts DIR
        One table for every team whose checkout is DIR/<team>.

Measurement commands are the teams' code: run `measure` and `report` on a throwaway machine
or container, never where credentials live. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMON = ROOT / "race" / "objectives.common.toml"
LOCKS = ROOT / "race" / "locks.json"
CONFIG = ROOT / "race" / "config.toml"
MAX_OWN = 5
TIMEOUT = 600


def objectives_path(checkout: Path, team: str) -> Path:
    return checkout / "race" / "teams" / team / "objectives.toml"


def load(path: Path) -> tuple[str, list[dict]]:
    """Team name and objectives, each completed with the common definition when it has one."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    common = {o["id"]: o for o in tomllib.loads(COMMON.read_text(encoding="utf-8"))["objective"]}
    out = []
    for o in data.get("objective", []):
        merged = dict(common.get(o.get("id"), {}))
        merged.update(o)
        out.append(merged)
    return data.get("team", ""), out


def problems(path: Path) -> list[str]:
    team, objs = load(path)
    common_ids = [o["id"] for o in tomllib.loads(COMMON.read_text(encoding="utf-8"))["objective"]]
    found = [o.get("id") for o in objs]
    errs = [f"missing common objective {c}" for c in common_ids if c not in found]
    own = [i for i in found if i not in common_ids]
    if len(own) > MAX_OWN:
        errs.append(f"{len(own)} own objectives, at most {MAX_OWN}")
    errs += [f"duplicate id {i}" for i in set(found) if found.count(i) > 1]
    for o in objs:
        for key in ("id", "metric", "direction", "target", "baseline", "command"):
            if key not in o:
                errs.append(f"{o.get('id', '?')}: missing {key}")
        if o.get("direction") not in ("lower", "higher"):
            errs.append(f"{o.get('id')}: direction must be lower or higher")
        if not isinstance(o.get("target"), (int, float)):
            errs.append(f"{o.get('id')}: target must be a number")
        b = o.get("baseline")
        if not (isinstance(b, (int, float)) or b == "none"):
            errs.append(f"{o.get('id')}: baseline must be a number or \"none\"")
        if o.get("id") in own and not o.get("offer"):
            errs.append(f"{o.get('id')}: own objective without the sentence of the offer it serves")
    if not team:
        errs.append("missing team")
    return errs


def reached(value: float, target: float, direction: str) -> bool:
    return value <= target if direction == "lower" else value >= target


def progress(value, baseline, target: float, direction: str) -> float:
    """Share of the way from baseline to target, in [0, 1]; 0 when the value is missing."""
    if value is None:
        return 0.0
    if baseline == "none" or baseline == target:
        return 1.0 if reached(value, target, direction) else 0.0
    gained = (baseline - value) if direction == "lower" else (value - baseline)
    span = (baseline - target) if direction == "lower" else (target - baseline)
    if span <= 0:  # target set on the wrong side of the baseline: only reaching it counts
        return 1.0 if reached(value, target, direction) else 0.0
    return max(0.0, min(1.0, gained / span))


def run_command(command: str, cwd: Path) -> tuple[float | None, str]:
    try:
        r = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True,
                           timeout=TIMEOUT, check=False)
    except subprocess.TimeoutExpired:
        return None, f"timeout after {TIMEOUT} s"
    lines = [x for x in r.stdout.strip().splitlines() if x.strip()]
    if r.returncode != 0 or not lines:
        return None, f"exit {r.returncode}: {(r.stderr or r.stdout)[-300:].strip()}"
    try:
        value = json.loads(lines[-1])["value"]
        return float(value), ""
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None, f"last line is not {{\"value\": <number>}}: {lines[-1][:120]}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_locks() -> dict:
    return json.loads(LOCKS.read_text(encoding="utf-8")) if LOCKS.exists() else {}


def ledger_summary(checkout: Path, team: str) -> dict:
    sys.path.insert(0, str(ROOT / "tools"))
    from call_model import load_providers
    from check_calls import verdict

    path = checkout / "research" / "model-calls.jsonl"
    if not path.exists():
        return {"calls": 0, "nonconforming": 0, "by_role": {}}
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = [r for r in rows if r.get("provider") == team]
    providers = load_providers()
    by_role: dict[str, int] = {}
    bad = 0
    for r in rows:
        by_role[r.get("role") or r.get("tier")] = by_role.get(r.get("role") or r.get("tier"), 0) + 1
        bad += bool(verdict(providers, r))
    return {"calls": len(rows), "nonconforming": bad, "by_role": by_role,
            "tokens": sum((r.get("input_tokens") or 0) + (r.get("output_tokens") or 0) for r in rows)}


def measure(team: str, checkout: Path) -> dict:
    path = objectives_path(checkout, team)
    if not path.exists():
        return {"team": team, "error": f"no {path.relative_to(checkout)}"}
    lock = read_locks().get(team)
    status = "unlocked" if not lock else ("locked" if lock["sha256"] == sha256(path) else "VOID: changed after lock")
    _, objs = load(path)
    rows, raf = [], []
    for o in objs:
        value, err = run_command(o["command"], checkout)
        p = progress(value, o["baseline"], o["target"], o["direction"])
        if status.startswith("VOID"):
            p = 0.0
        rows.append({"id": o["id"], "direction": o["direction"], "baseline": o["baseline"],
                     "target": o["target"], "value": value, "progress": round(p, 3), "error": err})
        if p < 1:
            gap = "" if value is None else f", gap {abs(value - o['target']):.3g}"
            raf.append(f"{o['id']}: {err or 'target not reached'}{gap}")
    mean = sum(r["progress"] for r in rows) / len(rows) if rows else 0.0
    return {"team": team, "time": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%MZ"), "lock": status,
            "check": problems(path), "objectives": rows, "mean_progress": round(mean, 3),
            "remaining": raf, "ledger": ledger_summary(checkout, team)}


def as_markdown(m: dict) -> str:
    if "error" in m:
        return f"## {m['team']}\n\n{m['error']}\n"
    out = [f"## {m['team']}: mean progress {m['mean_progress']:.0%} ({m['lock']}, {m['time']})", "",
           "| objective | baseline | target | value | progress |", "|---|---|---|---|---|"]
    for r in m["objectives"]:
        v = "–" if r["value"] is None else f"{r['value']:.4g}"
        out.append(f"| {r['id']} | {r['baseline']} | {r['target']} | {v} | {r['progress']:.0%} |")
    out += ["", "Remaining work (RAF):"] + [f"- {x}" for x in m["remaining"] or ["none"]]
    led = m["ledger"]
    out += ["", f"Role calls: {led['calls']} ({led['nonconforming']} not conforming), by role {led['by_role']}"]
    if m["check"]:
        out += ["", "Objectives file problems:"] + [f"- {x}" for x in m["check"]]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").add_argument("file", type=Path)
    for name in ("lock", "measure"):
        s = sub.add_parser(name)
        s.add_argument("--team", required=True)
        s.add_argument("--checkout", type=Path, required=True)
        if name == "measure":
            s.add_argument("--json", action="store_true")
    sub.add_parser("report").add_argument("--checkouts", type=Path, required=True)
    a = ap.parse_args()

    if a.cmd == "check":
        errs = problems(a.file)
        print("\n".join(errs) or "ok")
        return 1 if errs else 0
    if a.cmd == "lock":
        path = objectives_path(a.checkout, a.team)
        errs = problems(path)
        if errs:
            print("\n".join(errs))
            return 1
        ref = subprocess.run(["git", "rev-parse", "HEAD"], cwd=a.checkout, capture_output=True,
                             text=True, check=False).stdout.strip()
        locks = read_locks()
        locks[a.team] = {"sha256": sha256(path), "commit": ref,
                         "time": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%MZ")}
        LOCKS.write_text(json.dumps(locks, indent=2) + "\n", encoding="utf-8")
        print(f"locked {a.team} at {ref[:12]}")
        return 0
    if a.cmd == "measure":
        m = measure(a.team, a.checkout)
        print(json.dumps(m, indent=2) if a.json else as_markdown(m))
        return 0
    teams = tomllib.loads(CONFIG.read_text(encoding="utf-8"))["teams"]
    parts = [as_markdown(measure(t, a.checkouts / t)) for t in teams if (a.checkouts / t).exists()]
    print("# Race status\n\n" + "\n".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
