#!/usr/bin/env python3
"""Energy budget of the dynamic solver, same residuals as tests/test_mhd3d.py.

One point is ``n,forcing,kf,seed``. This script reports the residuals. It does
not apply the pass thresholds. Those stay in the hypothesis that scheduled the run.

    python3 experiments/cursor_energy_budget.py --device cpu --point 16,tg,1,1
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from milady.sim.mhd3d import MHD3D, MHD3DConfig


def run_point(n: int, forcing: str, kf: int, seed: int, device: str) -> dict:
    dt = 5e-3
    steps = 60
    cfg = MHD3DConfig(
        n=n,
        mode="dynamic",
        nu=0.05,
        eta=0.08,
        forcing=forcing,
        kf=kf,
        forcing_amp=0.5,
        u0="random",
        u0_amp=1.0,
        b0_amp=0.5,
        seed=seed,
        device=device,
        dtype="float64",
    )
    sim = MHD3D(cfg)
    energy, injection, dissipation = [], [], []
    for _ in range(steps):
        diag = sim.diagnostics()
        kinetic = float(np.asarray(diag["kinetic_energy"]).reshape(-1)[0])
        magnetic = float(np.asarray(diag["magnetic_energy"]).reshape(-1)[0])
        energy.append(kinetic + magnetic)
        injection.append(float(np.asarray(diag["injection"]).reshape(-1)[0]))
        dissipation.append(
            float(np.asarray(diag["kinetic_dissipation"]).reshape(-1)[0])
            + float(np.asarray(diag["magnetic_dissipation"]).reshape(-1)[0])
        )
        sim.step(dt)
    energy_a = np.asarray(energy, dtype=np.float64)
    injection_a = np.asarray(injection, dtype=np.float64)
    dissipation_a = np.asarray(dissipation, dtype=np.float64)
    dEdt = (energy_a[2:] - energy_a[:-2]) / (2 * dt)
    rhs = (injection_a - dissipation_a)[1:-1]
    rel = np.abs(dEdt - rhs) / np.maximum(np.abs(rhs), 1e-12)
    scale = np.abs(dEdt - rhs) / np.maximum(injection_a, dissipation_a)[1:-1]
    finite = bool(np.isfinite(rel).all() and np.isfinite(scale).all() and np.isfinite(rhs).all())
    return {
        "n": n,
        "forcing": forcing,
        "kf": kf,
        "seed": seed,
        "steps": steps,
        "dt": dt,
        "finite": finite,
        "rel_max": float(rel.max()) if finite else None,
        "scale_max": float(scale.max()) if finite else None,
        "rhs_abs_min": float(np.abs(rhs).min()) if finite else None,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--point", action="append", required=True, help="n,forcing,kf,seed")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out-dir", default="experiments/results/cursor_energy")
    args = ap.parse_args(argv)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rc = 0
    for spec in args.point:
        n_s, forcing, kf_s, seed_s = spec.split(",")
        n, kf, seed = int(n_s), int(kf_s), int(seed_s)
        info = run_point(n, forcing, kf, seed, args.device)
        if not info["finite"]:
            rc = 1
        name = f"n{n}_{forcing}_kf{kf}_s{seed}.json"
        (out / name).write_text(json.dumps(info) + "\n", encoding="utf-8")
        print(json.dumps(info), flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
