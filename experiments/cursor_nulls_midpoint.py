"""Null counts of the kmax=6 midpoint against the held-out Rm=12 field.

The midpoint is the quoted generator. The held-out field is the baseline.
Eight times, seeds 0-4. The per-seed error is the mean over times of
|n_gen - n_ref| / max(n_ref, 1).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))

from cursor_constraint_cmp import pack, snapshot, unpack

from milady.eval.nulls import count_nulls
from milady.train.data import half_ball_modes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kmax", type=float, default=6.0)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    n = 16
    kmax = args.kmax
    modes = half_ball_modes(kmax)
    times = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
    rows = []
    for seed in (0, 1, 2, 3, 4):
        errs = []
        pairs = []
        for t in times:
            ref = snapshot(n, 12.0, seed, t)
            left = pack(snapshot(n, 11.0, seed, t), modes)
            right = pack(snapshot(n, 13.0, seed, t), modes)
            gen = unpack(0.5 * (left + right), modes, n)
            n_ref = count_nulls(ref[None])
            n_gen = count_nulls(gen[None])
            rel = abs(n_gen - n_ref) / max(n_ref, 1)
            errs.append(rel)
            pairs.append({"t": t, "n_ref": n_ref, "n_gen": n_gen, "relative_error": rel})
        row = {"seed": seed, "relative_error": float(np.mean(errs)), "times": pairs}
        rows.append(row)
        print("seed", seed, row["relative_error"], flush=True)
    dest = args.out or Path(f"experiments/results/cursor_nulls_midpoint_kmax{kmax:g}.json")
    dest.write_text(json.dumps({"kmax": kmax, "n": n, "held_out_rm": 12.0, "seeds": rows}, indent=2) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
