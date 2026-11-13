#!/usr/bin/env python3
"""Print one race objective as a last-line JSON value.

C1 to C5 have no 3D generator yet. Until experiments/results/cursor_metrics.json
holds a finite number for that id, the command prints a sentinel on the far
side of the target so progress stays 0. C6 counts hypotheses that already
have an encadrant verdict and a five-seed protocol. C7 counts Python modules
under src/milady that differ from origin/main and are named by a test.
T1 reads the committed float32 bench log.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "experiments" / "results" / "cursor_metrics.json"
BENCH32 = ROOT / "research" / "gpu-logs" / "bench-float32.log"
HYPO = ROOT / "research" / "hypotheses.json"

# Far side of each lower-is-better target. Not a measurement.
SENTINEL = {"c1": 1.0e6, "c2": 1.0, "c3": 1.0, "c4": 1.0, "c5": 1.0}


def from_file(metric: str) -> float:
    if METRICS.exists():
        data = json.loads(METRICS.read_text(encoding="utf-8"))
        if metric in data and isinstance(data[metric], (int, float)):
            return float(data[metric])
    return SENTINEL[metric]


def c6() -> float:
    doc = json.loads(HYPO.read_text(encoding="utf-8"))
    n = 0
    for h in doc["hypotheses"]:
        verdict = h.get("verdict") or ""
        if "CONFIRMED" not in verdict and "REFUTED" not in verdict:
            continue
        blob = f"{h.get('statement', '')}\n{h.get('protocol', '')}".lower()
        five = any(s in blob for s in ("five", "5 seed", "seeds 0-4", "0-4"))
        compares = any(s in blob for s in ("constraint", "baseline", "control", "variant"))
        if five and compares:
            n += 1
    return float(n)


def c7() -> float:
    diff = subprocess.run(
        ["git", "diff", "--name-only", "origin/main", "--", "src/milady"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    n = 0
    for line in diff.stdout.splitlines():
        path = Path(line)
        if path.suffix != ".py" or path.stem in {"__init__"}:
            continue
        hit = subprocess.run(
            ["grep", "-R", "-l", "-F", "--include=*.py", path.stem, "tests"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if hit.returncode == 0 and hit.stdout.strip():
            n += 1
    return float(n)


def t1() -> float:
    if not BENCH32.exists():
        return 1.0
    for line in BENCH32.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        row = json.loads(line)
        if row.get("n") == 128 and row.get("dtype") == "float32":
            return float(row["seconds_per_step"])
    return 1.0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--metric", required=True, choices=["c1", "c2", "c3", "c4", "c5", "c6", "c7", "t1"])
    args = ap.parse_args(argv)
    if args.metric in SENTINEL:
        value = from_file(args.metric)
    elif args.metric == "c6":
        value = c6()
    elif args.metric == "c7":
        value = c7()
    else:
        value = t1()
    print(json.dumps({"value": value}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
