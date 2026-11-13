"""Dynamic ABC ensemble and the mean energy balance on two time halves.

The flow is forced and the magnetic seed is small. The first half is the
transient baseline. The second half is the window used for the stationarity
constraint. ``--quick`` is one short seed and is not a quoted result.

The total residual is (mean injection − mean dissipation) / mean dissipation.
The magnetic residual keeps the exchange term and subtracts no growth rate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from milady.eval.metrics import budget_summary, energy_budget
from milady.sim.mhd3d import MHD3D, MHD3DConfig

PARAMS = {
    "mode": "dynamic",
    "forcing": "abc",
    "nu": 0.05,
    "eta": 0.05,
    "kf": 1,
    "U_ref": 1.0,
    "forcing_rule": "laminar",
    "A": 1.0,
    "B": 1.0,
    "C": 1.0,
}


def one_seed(seed: int, t_end: float, n_snap: int) -> dict:
    sim = MHD3D(
        MHD3DConfig(
            n=16,
            mode="dynamic",
            forcing="abc",
            nu=PARAMS["nu"],
            eta=PARAMS["eta"],
            b0_amp=1e-3,
            seed=seed,
            device="cpu",
            dtype="float64",
        )
    )
    dt = min(0.02, float(sim.cfl_dt(0.5)))
    times = np.linspace(t_end / (2 * n_snap), t_end, 2 * n_snap)
    us, bs = [], []
    nxt = 0
    while nxt < len(times):
        sim.step(dt)
        if float(sim.t) + 1e-12 >= times[nxt]:
            us.append(sim._ifft(sim.velocity_hat)[0].movedim(0, -1).detach().cpu().numpy())
            bs.append(sim._ifft(sim.bh)[0].movedim(0, -1).detach().cpu().numpy())
            nxt += 1
    u = np.stack(us)
    b = np.stack(bs)

    def residual(sl: slice) -> dict[str, float]:
        summary = budget_summary(energy_budget(u[sl], b[sl], PARAMS))
        return {
            "total": float(summary["balance_residual_total"]),
            "magnetic": float(summary["balance_residual_magnetique"]),
            "finite": bool(np.isfinite(u[sl]).all() and np.isfinite(b[sl]).all()),
        }

    return {"seed": seed, "first": residual(slice(0, n_snap)), "second": residual(slice(n_snap, None))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    seeds = [0] if args.quick else [0, 1, 2, 3, 4]
    t_end = 2.0 if args.quick else 8.0
    rows = []
    for seed in seeds:
        row = one_seed(seed, t_end, n_snap=4 if args.quick else 8)
        rows.append(row)
        print("seed", seed, "second_total", row["second"]["total"], "second_magnetic", row["second"]["magnetic"], flush=True)
    result = {"t_end": t_end, "n": 16, "nu": PARAMS["nu"], "eta": PARAMS["eta"], "seeds": rows}
    dest = args.out or Path(
        "experiments/results/cursor_stationary_quick.json" if args.quick else "experiments/results/cursor_stationary.json"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
