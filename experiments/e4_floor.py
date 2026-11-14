"""E4 - noise floors of the energy distance (protocol check asked by the encadrant, 2026-11-12).

The C1 ratio divides the energy distance of a generated set by a floor measured between two
reference subsamples drawn from **disjoint halves of the trajectories**. This script quantifies
that floor and what it hides, for each η: its mean, standard deviation, minimum and maximum over
the splits (the splits reuse the same 24 trajectories, so averaging them does not remove the
uncertainty), the floor of a random split that ignores the trajectories (pure sampling noise of n
snapshots), and the mean pairwise distance E|Y − Y'| of the reference in the standardized feature
space, from which the digest estimates the extra V-statistic bias of a weighted sample,
(Σ w² − 1/n) E|X − X'| ≈ (1/ESS − 1/n) E|Y − Y'|.

Usage: python3 e4_floor.py     -> results/e4_floor.json (no model, a few minutes on one core)
"""
from __future__ import annotations

import time

import numpy as np
import torch

from common import save_json
from e4_mhd3d import ETAS, Context
from milady.eval import metrics as M


def main() -> None:
    torch.set_num_threads(1)
    t0 = time.time()
    ctx = Context(False, need=("pot",))
    out: dict = {"config": {"splits": 20, "sizes": [512, 256]}, "values": {}}
    for e in ETAS:
        f = ctx.standardize(ctx.ref[e]["features"])
        row: dict = {}
        for n in (512, 256):
            traj = [M.energy_distance(f[ia], f[ib], n=n) for ia, ib in (ctx.half_split(e, k, n) for k in range(20))]
            rnd = []
            for k in range(20):
                perm = np.random.default_rng(5000 + k).permutation(len(f))
                rnd.append(M.energy_distance(f[perm[:n]], f[perm[n:2 * n]], n=n))
            row[f"traj_split_{n}"] = {"mean": float(np.mean(traj)), "sd": float(np.std(traj, ddof=1)),
                                      "min": float(np.min(traj)), "max": float(np.max(traj)),
                                      "mean_first_10": float(np.mean(traj[:10]))}
            row[f"random_split_{n}"] = {"mean": float(np.mean(rnd)), "sd": float(np.std(rnd, ddof=1))}
        sub = f[np.random.default_rng(0).choice(len(f), size=1000, replace=False)]
        d = np.sqrt(np.maximum(((sub[:, None, :] - sub[None, :, :]) ** 2).sum(-1), 0.0))
        row["mean_pairwise_distance"] = float(d.sum() / (len(sub) * (len(sub) - 1)))
        out["values"][f"{e:.5f}"] = row
        print(f"eta {e:.5f}: trajectory floor {row['traj_split_512']['mean']:.4f} ± {row['traj_split_512']['sd']:.4f} "
              f"[{row['traj_split_512']['min']:.4f}, {row['traj_split_512']['max']:.4f}], random floor "
              f"{row['random_split_512']['mean']:.4f}, E|Y-Y'| {row['mean_pairwise_distance']:.3f}", flush=True)
    out["duration_s"] = time.time() - t0
    save_json(out, "e4_floor.json")


if __name__ == "__main__":
    main()
