"""Export the JSON bundle read by a team's explorer page (site/teams/<team>/explorer/).

    python3 experiments/export_explorer.py --team cursor

The bundle copies, without recomputing anything:
  - every summary result file experiments/results/<team>_*.json, and <team>_fm/metrics.json if present;
  - the hypothesis register research/hypotheses.json (id, statement, criterion, status, verdict);
  - the finished GPU jobs of research/compute-ledger.jsonl (time, GPU, hours, USD, command, exit code);
  - the list of the team's SVG data plots and schematics, for the figure gallery.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 10 * 1024 * 1024  # race/DELIVERABLES.md: at most 10 MB per file


def results(team: str) -> dict:
    res = ROOT / "experiments" / "results"
    files = sorted(res.glob(f"{team}_*.json"))
    fm = res / f"{team}_fm" / "metrics.json"
    if fm.exists():
        files.append(fm)
    return {p.relative_to(res).as_posix(): json.loads(p.read_text(encoding="utf-8")) for p in files}


def hypotheses() -> list[dict]:
    path = ROOT / "research" / "hypotheses.json"
    if not path.exists():
        return []
    keep = ("id", "statement", "refutation_criterion", "status", "verdict", "script")
    return [{k: h.get(k) for k in keep} for h in json.loads(path.read_text(encoding="utf-8"))["hypotheses"]]


def gpu_jobs() -> list[dict]:
    path = ROOT / "research" / "compute-ledger.jsonl"
    if not path.exists():
        return []
    keep = ("time", "gpu", "hours", "usd", "command", "rc", "commit")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [{k: r.get(k) for k in keep} for r in rows if "usd" in r]


def figures(team: str) -> list[dict]:
    """SVG data plots (plots/) and schematics (figures/<name>/figure/out/<name>.svg), relative to the team."""
    base = ROOT / "site" / "teams" / team
    out = [{"name": p.stem, "kind": "data plot", "path": p.relative_to(base).as_posix()}
           for p in sorted((base / "plots").glob("*.svg"))]
    out += [{"name": p.stem, "kind": "schematic", "path": p.relative_to(base).as_posix()}
            for p in sorted((base / "figures").glob("*/figure/out/*.svg"))]
    return out


def export(team: str) -> Path:
    bundle = {"team": team, "results": results(team), "hypotheses": hypotheses(), "gpu_jobs": gpu_jobs(),
              "figures": figures(team)}
    text = json.dumps(bundle, indent=1, allow_nan=False) + "\n"
    if len(text.encode()) > MAX_BYTES:
        raise SystemExit(f"bundle is {len(text.encode())} bytes, above {MAX_BYTES}")
    dest = ROOT / "site" / "teams" / team / "explorer" / "data" / "bundle.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--team", required=True)
    args = parser.parse_args()
    print(export(args.team))


if __name__ == "__main__":
    main()
