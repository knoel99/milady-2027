"""E4 release - parameter files of the laws: latent space, G0, G1, and the recolouring maps of W16 with their evaluation.

    python3 experiments/e4_release_models.py --weights DIR --out DIR [--n-recolour 16384] [--seeds 0 1 2 3 4] [--no-laws]

Reads the data of ``$E4_DATA`` (the snapshots of ``e4_data.py``) and the weights of W9 written by
``E4_SAVE_MODELS=1 python3 e4_mhd3d.py --group D`` in ``--weights``. Writes in ``--out``:

- ``e4_latent_space.pt``: the latent space of the models and its normalisation (fitted on the training η);
- ``e4_gaussian_G0.pt``, ``e4_gaussian_G1.pt``: the parameters of the two Gaussian laws (``state()`` of the classes);
- ``e4_W16_map_s<seed>.pt``: for each seed and each held-out η, the linear map of W16 estimated on ``--n-recolour`` samples
  of W9 (the report used 131 072 on a GPU; the number used here is recorded in the file);
- ``e4_release_w16_s<seed>.json``: the metrics of 512 samples of W16 per held-out η that did not enter the estimate of the
  map (``Context.evaluate``: energy distance over its floor, energies, balances, production split, spectra, null count; no
  restart in the solver).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

import e4_release_example as R
from e4_data import ETA_TEST
from e4_mhd3d import Context
from milady.train import constraints as C


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weights", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-recolour", type=int, default=16384)
    ap.add_argument("--n-eval", type=int, default=512)
    ap.add_argument("--seeds", type=int, nargs="*", default=[0, 1, 2, 3, 4])
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--no-laws", action="store_true", help="do not write the latent space and the Gaussian laws (jobs split by seed)")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    ctx = Context(False, need=("pot_sym",))
    sp = ctx.pot_sym
    g1 = C.FullGaussian(sign=sp.sign).fit(ctx.x_pot_sym, ctx.c_train[:, 0])
    if not a.no_laws:
        torch.save({"state_dict": sp.state_dict(), "kmax": 5, "symmetric_b": True, "truncation": "cube", "n_modes": sp.n_modes,
                    "n_channels": sp.n_channels, "class": "milady.train.data.FourierPotentialSpace"}, out / R.SPACE)
        g0 = C.ModewiseGaussian(sign=sp.sign).fit(ctx.x_pot_sym, ctx.c_train[:, 0])
        torch.save(g0.state(), out / R.GAUSS.format(law="G0"))
        torch.save(g1.state(), out / R.GAUSS.format(law="G1"))
        print(f"[{time.time() - t0:.0f} s] latent space, G0, G1 written", flush=True)
    for seed in a.seeds:
        rows: list = []
        if not (Path(a.weights) / R.WEIGHTS.format(seed=seed)).exists():
            print(f"seed {seed}: no weights", flush=True)
            continue
        model = R.load_w9(a.weights, sp, seed)
        rec: dict[str, list] = {"mean_src": [], "map": [], "mean_tgt": []}
        for e in ETA_TEST:
            zs = R.sample_w9(model, sp, e, a.n_recolour, seed=100003 * seed + 211 + int(1e5 * e))
            m = R.recolouring(zs, g1, e)
            for k in rec:
                rec[k].append(m[k])
            del zs
            z = R.recolour(R.sample_w9(model, sp, e, a.n_eval, seed=100003 * seed + 977 + int(1e5 * e)), m)
            row = ctx.evaluate(sp.field_hat(sp.denormalize(z)).cpu(), e, None, nulls=True)
            rows.append({k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in row.items()})
            print(f"[{time.time() - t0:.0f} s] seed {seed} eta {e}: ed_ratio {row['ed_ratio']:.2f}, E_B error {row['err_Eb_rel']:+.3f}, "
                  f"third-order {row['prod_fluct_over_d']:+.3f}, nulls {row['null_count_err_rel']:.2f}", flush=True)
        torch.save({"seed": seed, "n_recolour": a.n_recolour, "eta": list(ETA_TEST), "cond": [R.cn(e) for e in ETA_TEST], **rec,
                    "formula": "x16 = mean_tgt + (x9 − mean_src) @ map, on the flattened normalised latents (5320,)"},
                   out / R.MAP.format(seed=seed))
        (out / f"e4_release_w16_s{seed}.json").write_text(json.dumps(
            {"config": {"seed": seed, "n_recolour": a.n_recolour, "n_eval": a.n_eval, "steps": 50, "etas": list(ETA_TEST), "restart": False},
             "evaluation": rows}, indent=1, default=float), encoding="utf-8")
    print(f"[{time.time() - t0:.0f} s] done", flush=True)


if __name__ == "__main__":
    main()
