"""Number of magnetic null points of the E4 reference on ALL its snapshots (the reference stage counts them on 400).

    python3 e4_refnulls.py [--device cuda] [--etas test]      # writes results/e4_refnulls.json

Asked by the review of the jury-externe role of 2026-11-13: the count on 400 snapshots drawn at random differs by 4 to 10 %
between two draws at the two lower held-out η, which is the uncertainty of every null-count error of the study. For each η:
the mean count over all the snapshots, its standard error over the trajectories (the snapshots of one trajectory are
correlated), and the mean of each trajectory. Same grid (48³) and method as ``e4_mhd3d.py --reference``.
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import torch

import e4_data as D
from e4_mhd3d import NULL_GRID, RESULTS, save_json
from milady.eval.topology import null_count


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--device", default=None, help="cuda to count on a GPU")
    ap.add_argument("--etas", default="all", help="all, or test (the held-out η only)")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="first snapshots of each trajectory only (timing test)")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    sp = D.space()
    etas = D.ETA_TEST if a.etas == "test" else D.ETAS
    out: dict = {"config": {"null_grid": NULL_GRID, "data_seed_offset": D.SEED_OFFSET, "n_traj": D.FULL["n_traj"], "etas": a.etas}, "values": {}}
    t0 = time.time()
    for e in etas:
        d = D.load(e)
        x, traj = d["x"], d["traj"]
        if a.limit:
            keep = np.concatenate([np.flatnonzero(traj == i)[: a.limit] for i in np.unique(traj)])
            x, traj = x[keep], traj[keep]
        counts = []
        for i in range(0, len(x), 200):
            fh = sp.field_hat(torch.as_tensor(x[i:i + 200]))
            b = sp.to_grid(fh[:, 1:2].to(torch.complex128), (NULL_GRID,) * 3)[:, 0].numpy()
            counts.append(null_count(b, device=a.device))
        c = np.concatenate(counts).astype(float)
        per = np.array([c[traj == i].mean() for i in np.unique(traj)])
        out["values"][f"{e:.5f}"] = {"split": D.split_of(D.ETAS.index(e)), "n": int(len(c)), "n_traj": int(len(per)),
                                    "null_count_mean": float(c.mean()), "null_count_se_traj": float(per.std(ddof=1) / np.sqrt(len(per))),
                                    "null_count_sd": float(c.std()), "per_trajectory": per.tolist()}
        print(f"eta {e:.5f}: {c.mean():.2f} ± {per.std(ddof=1) / np.sqrt(len(per)):.2f} null points over {len(c)} snapshots "
              f"({time.time() - t0:.0f} s)", flush=True)
    out["duration_s"] = time.time() - t0
    if not a.limit:
        save_json(out, "e4_refnulls.json")


if __name__ == "__main__":
    main()
