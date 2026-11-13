"""Export a small JSON bundle for the team explorer.

    python3 experiments/export_explorer.py --team cursor
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def export(team: str) -> Path:
    results = ROOT / "experiments" / "results"
    names = [
        "cursor_constraint_cmp.json",
        "cursor_constraint_ceiling.json",
        "cursor_constraint_midpoint_kmax6.json",
        "cursor_stationary.json",
        "cursor_nulls.json",
        "cursor_metrics.json",
    ]
    bundle = {name: json.loads((results / name).read_text(encoding="utf-8")) for name in names}
    dest = ROOT / "site" / "teams" / team / "explorer" / "data" / "bundle.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--team", required=True)
    args = parser.parse_args()
    print(export(args.team))


if __name__ == "__main__":
    main()
