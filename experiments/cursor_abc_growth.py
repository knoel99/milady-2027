#!/usr/bin/env python3
"""One kinematic ABC growth-rate point from the torch 3D solver.

The fit is the slope of ln‖B‖ on the second half of the run, as in
``tests/test_mhd3d.py``. The step is at most ``--dt`` and at most the
solver CFL step (``--cfl``, default 1, below the RK4 note of about 2.8).

    python3 experiments/cursor_abc_growth.py --quick
    python3 experiments/cursor_abc_growth.py --rm 12 --n 64 --seed 0 --device cuda --out experiments/results/cursor_abc/rm12_n64_s0.json

Prints one JSON object on the last stdout line.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

from milady.sim.mhd3d import MHD3D, MHD3DConfig, growth_rate_fit


def run_point(rm: float, n: int, seed: int, t_total: float, dt: float, cfl: float, device: str) -> dict:
    sim = MHD3D(
        MHD3DConfig(
            n=n,
            mode="kinematic",
            flow="abc",
            eta=1.0 / rm,
            b0_amp=1.0,
            seed=seed,
            device=device,
            dtype="float64",
        )
    )
    cfl_dt0 = sim.cfl_dt(cfl)
    ts: list[float] = []
    logs: list[float] = []
    steps = 0
    while sim.t < t_total - 1e-9:
        steps += sim.advance_to(min(sim.t + 1.0, t_total), dt=dt, cfl=cfl)
        ts.append(sim.t)
        logs.append(float(sim.diagnostics()["log_b_rms"][0]))
    diag = sim.diagnostics()
    lam = growth_rate_fit(ts, logs, t_min=t_total / 2)
    return {
        "Rm": rm,
        "n": n,
        "seed": seed,
        "t": t_total,
        "dt_cap": dt,
        "cfl": cfl,
        "cfl_dt0": cfl_dt0,
        "steps": steps,
        "lambda": lam,
        "max_div_b": float(diag["max_div_b"][0]),
        "finite": bool(math.isfinite(lam)),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true", help="CPU smoke: n=16, t=2, Rm=12, seed 0")
    ap.add_argument("--rm", type=float, default=12.0)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--t", type=float, default=120.0)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--cfl", type=float, default=1.0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default="", help="JSON path to write (the stdout line is always printed)")
    args = ap.parse_args(argv)
    if args.quick:
        args.rm, args.n, args.seed, args.t, args.device = 12.0, 16, 0, 2.0, "cpu"
    try:
        info = run_point(args.rm, args.n, args.seed, args.t, args.dt, args.cfl, args.device)
        info["ok"] = True
    except FloatingPointError as exc:
        info = {"ok": False, "error": str(exc), "Rm": args.rm, "n": args.n, "seed": args.seed, "finite": False}
    line = json.dumps(info)
    if args.out and info.get("ok"):
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(line + "\n", encoding="utf-8")
    print(line, flush=True)
    return 0 if info.get("ok") and np.isfinite(info.get("lambda", np.nan)) else 1


if __name__ == "__main__":
    sys.exit(main())
