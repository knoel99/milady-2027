#!/usr/bin/env python3
"""Run several kinematic ABC growth points in one process.

Each point is ``n,Rm,seed``. JSON files land in ``--out-dir`` and one JSON
object is printed per point. Exit status is 0 only if every point is finite.

    python3 experiments/cursor_abc_batch.py --device cpu --t 2 --out-dir /tmp/abc \
        --point 16,12,0
    python3 experiments/cursor_abc_batch.py --device cuda --point 48,6,0 --point 48,12,0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cursor_abc_growth import run_point


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--point", action="append", required=True, help="n,Rm,seed")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--t", type=float, default=120.0)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--cfl", type=float, default=1.0)
    ap.add_argument("--out-dir", default="experiments/results/cursor_abc")
    args = ap.parse_args(argv)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rc = 0
    for spec in args.point:
        n_s, rm_s, seed_s = spec.split(",")
        n, rm, seed = int(n_s), float(rm_s), int(seed_s)
        try:
            info = run_point(rm, n, seed, args.t, args.dt, args.cfl, args.device)
            info["ok"] = True
        except FloatingPointError as exc:
            info = {"ok": False, "error": str(exc), "Rm": rm, "n": n, "seed": seed, "finite": False}
            rc = 1
        if not info.get("finite"):
            rc = 1
        name = f"n{n}_rm{rm:g}_s{seed}.json"
        (out / name).write_text(json.dumps(info) + "\n", encoding="utf-8")
        print(json.dumps(info), flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
