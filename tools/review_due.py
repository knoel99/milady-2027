#!/usr/bin/env python3
"""Say when the supervisor (`encadrant`) and the external examiner (`jury-externe`) must step in.

The race has no weeks: reviews are triggered by what happens and by the time that passes,
from race/config.toml [reviews] and the review register research/reviews.jsonl.

- `encadrant` is due when commits touching the watched results (experiments/results, the
  hypothesis register, the simulator) exist since its last review, or when work went on for
  more than `encadrant_max_gap_hours` since then.
- `jury-externe` is due at each fraction of the race (`jury_fractions` of the span from
  `start` to the deadline) not yet covered by a jury review made after it, and when a
  milestone file (the race report, the internship report) changed since its last review.

    python3 tools/review_due.py due            # lists the due reviews; exit 1 if any is due
    python3 tools/review_due.py log --role encadrant --scope "H3, results of e4 seeds 0-4" --verdict "2 refuted, 1 holds"

Run `due` after every commit that adds a result, and at least every hour of work; when a review
is due, run it through the role (sub-agent or tools/call_model.py / run_role.py) before going on,
then record it with `log`. MILADY_START and MILADY_DEADLINE (ISO 8601) override the dates of the
config for a pilot with other dates. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "research" / "reviews.jsonl"


def parse(t: str) -> dt.datetime:
    return dt.datetime.fromisoformat(t)


def settings() -> dict:
    cfg = tomllib.loads((ROOT / "race" / "config.toml").read_text(encoding="utf-8"))
    r = dict(cfg.get("reviews", {}))
    r["start"] = parse(os.environ.get("MILADY_START") or r["start"])
    r["deadline"] = parse(os.environ.get("MILADY_DEADLINE") or cfg["deadline"])
    return r


def reviews() -> list[dict]:
    if not REGISTER.exists():
        return []
    return [json.loads(x) for x in REGISTER.read_text(encoding="utf-8").splitlines() if x.strip()]


def last(role: str, rows: list[dict]) -> dt.datetime | None:
    times = [parse(r["time"]) for r in rows if r["role"] == role]
    return max(times) if times else None


def commits_since(since: dt.datetime, paths: list[str]) -> list[str]:
    out = subprocess.run(["git", "log", f"--since={since.isoformat()}", "--format=%h %cI %s", "--", *paths],
                         cwd=ROOT, capture_output=True, text=True, check=False).stdout
    return [x for x in out.splitlines() if x.strip()]


def due(now: dt.datetime | None = None, rows: list[dict] | None = None,
        commits=commits_since, s: dict | None = None) -> list[tuple[str, str]]:
    now = now or dt.datetime.now(dt.UTC)
    rows = reviews() if rows is None else rows
    s = s or settings()
    out: list[tuple[str, str]] = []

    enc = last("encadrant", rows) or s["start"]
    new = commits(enc, s.get("encadrant_watch", ["experiments/results", "research/hypotheses.json"]))
    if new:
        out.append(("encadrant", (f"{len(new)} commit(s) on results or hypotheses since its last review "
                                  f"({enc:%Y-%m-%d %H:%M}), e.g. {new[0]}")))
    elif (now - enc).total_seconds() > 3600 * s.get("encadrant_max_gap_hours", 6) and commits(enc, ["."]):
        out.append(("encadrant", f"no review for {(now - enc).total_seconds() / 3600:.1f} h while work went on"))

    span = s["deadline"] - s["start"]
    jury = [parse(r["time"]) for r in rows if r["role"] == "jury-externe"]
    for f in sorted(s.get("jury_fractions", [0.25, 0.5, 0.75, 0.95]), reverse=True):  # the latest passed
        t = s["start"] + f * span
        if t <= now and not any(j >= t for j in jury):
            out.append(("jury-externe", f"{f:.0%} of the race passed at {t:%Y-%m-%d %H:%M} without a jury review"))
            break  # one review covers every fraction passed before it
    lj = max(jury) if jury else s["start"]
    changed = commits(lj, s.get("jury_watch", ["research/race-report.md", "site/report"]))
    if changed and not any(r == "jury-externe" for r, _ in out):
        out.append(("jury-externe", f"milestone changed since its last review: {changed[0]}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("due")
    lg = sub.add_parser("log")
    lg.add_argument("--role", required=True, choices=["encadrant", "jury-externe", "physicien", "biblio"])
    lg.add_argument("--scope", required=True, help="what was reviewed (hypotheses, files, commit range)")
    lg.add_argument("--verdict", required=True, help="one line: the verdicts per criterion or claim")
    lg.add_argument("--file", default="", help="where the full answer is written")
    a = ap.parse_args()
    if a.cmd == "log":
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=False).stdout.strip()
        REGISTER.parent.mkdir(parents=True, exist_ok=True)
        with REGISTER.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"time": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "role": a.role,
                                "commit": head, "scope": a.scope, "verdict": a.verdict, "file": a.file}) + "\n")
        print(f"logged {a.role} review at {head}")
        return 0
    items = due()
    for role, why in items:
        print(f"DUE {role}: {why}")
    if not items:
        print("no review due")
    return 1 if items else 0


if __name__ == "__main__":
    sys.exit(main())
