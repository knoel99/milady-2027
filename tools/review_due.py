#!/usr/bin/env python3
"""Say when the supervisor (`encadrant`) and the external examiner (`jury-externe`) must step in.

The race has no weeks: reviews are triggered by what happens and by the time that passes,
from milady.toml [reviews] and the review register research/reviews.jsonl.

- `encadrant` is due when commits touching the watched results (experiments/results, the
  hypothesis register, the simulator) exist since its last review, or when work went on for
  more than `encadrant_max_gap_hours` since then.
- `jury-externe` is due at each fraction of the GPU budget spent (`jury_fractions`, from the
  jobs of research/compute-ledger.jsonl; there is no deadline) not yet covered by a jury review
  made after it, and when a milestone file (the race report, the report) changed since its last review.

    python3 tools/review_due.py due            # lists the due reviews; exit 1 if any is due
    python3 tools/review_due.py log --role encadrant --scope "H3, results of e4 seeds 0-4" --verdict "2 refuted, 1 holds"

Run `due` after every commit that adds a result, and at least every hour of work; when a review
is due, run it through the role (sub-agent or tools/call_model.py / run_role.py) before going on,
then record it with `log`. MILADY_START (ISO 8601) overrides the start of [reviews] and
MILADY_GPU_BUDGET_USD the budget of [gpu]. Standard library only.
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


LEDGER = ROOT / "research" / "compute-ledger.jsonl"


def settings() -> dict:
    cfg = tomllib.loads((ROOT / "milady.toml").read_text(encoding="utf-8"))
    r = dict(cfg.get("reviews", {}))
    r["start"] = parse(os.environ.get("MILADY_START") or r["start"])
    gpu = cfg.get("gpu", {})
    r["budget_usd"] = float(os.environ.get("MILADY_GPU_BUDGET_USD") or gpu.get("budget_usd") or gpu.get("credit_usd") or 0)
    return r


def spending() -> list[tuple[dt.datetime, float]]:
    """(time, dollars) of every finished GPU job of this checkout's ledger, in time order."""
    if not LEDGER.exists():
        return []
    rows = [json.loads(x) for x in LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]
    return sorted((parse(r["time"].replace("Z", "+00:00")), float(r.get("usd") or 0))
                  for r in rows if r.get("event") != "start" and r.get("time"))


def crossed(spend: list[tuple[dt.datetime, float]], amount: float) -> dt.datetime | None:
    """When the cumulative spend first reached ``amount``, or None."""
    total = 0.0
    for t, usd in spend:
        total += usd
        if total >= amount:
            return t
    return None


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
        commits=commits_since, s: dict | None = None,
        spend: list[tuple[dt.datetime, float]] | None = None) -> list[tuple[str, str]]:
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

    # The pilots have no deadline, only a budget: the jury steps in at fractions of the GPU budget spent.
    jury = [parse(r["time"]) for r in rows if r["role"] == "jury-externe"]
    spend = spending() if spend is None else spend
    budget = s.get("budget_usd", 0)
    for f in sorted(s.get("jury_fractions", [0.25, 0.5, 0.75, 0.95]), reverse=True):  # the latest passed
        t = crossed(spend, f * budget) if budget else None
        if t is not None and not any(j >= t for j in jury):
            out.append(("jury-externe", f"{f:.0%} of the GPU budget (${f * budget:.2f} of ${budget:.0f}) spent at "
                                        f"{t:%Y-%m-%d %H:%M} without a jury review since"))
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
