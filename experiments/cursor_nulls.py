"""Null counts of a kinematic ABC field and of its kmax=4 truncation.

The truncation is the representation constraint. The full field is the
baseline. The relative error is |n_trunc - n_full| / max(n_full, 1).
``--quick`` is one seed and is not a quoted result.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))

from cursor_constraint_cmp import pack, snapshot, unpack

from milady.eval.nulls import count_nulls
from milady.train.data import half_ball_modes


def one(seed: int, kmax: float) -> dict:
    full = snapshot(16, 12.0, seed, 1.0)
    modes = half_ball_modes(kmax)
    truncated = unpack(pack(full, modes), modes, 16)
    n_full = count_nulls(full[None])
    n_trunc = count_nulls(truncated[None])
    rel = abs(n_trunc - n_full) / max(n_full, 1)
    return {"seed": seed, "n_full": n_full, "n_trunc": n_trunc, "relative_error": rel}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seeds = [0] if args.quick else [0, 1, 2, 3, 4]
    rows = []
    for seed in seeds:
        row = one(seed, 4.0)
        rows.append(row)
        print("seed", seed, row, flush=True)
    dest = args.out or Path(
        "experiments/results/cursor_nulls_quick.json" if args.quick else "experiments/results/cursor_nulls.json"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"kmax": 4.0, "n": 16, "rm": 12.0, "seeds": rows}, indent=2) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
