"""E4 data - saturated 3D MHD dynamo forced by a constant ABC force, for 11 values of η.

System: ``milady.sim.mhd3d`` in dynamic mode on the periodic box [0, 2π)³, ABC forcing (A = B = C = 1)
at the mode kf = 2 with the laminar amplitude ν kf², ν fixed, η swept (Rm = U_ref L_ref / η with
U_ref = 1 and L_ref = 1/kf, i.e. Rm = 1/(2η); Re = 1/(2ν)). Grid N³ with the 2/3 rule: the solver
keeps the modes |m_i| ≤ (N − 1)//3, and the snapshots are stored as **every one of these modes**
(vector potentials in the Craya–Herring basis, ``FourierPotentialSpace(truncation="cube")``), so the
quadratic budgets computed from a snapshot are exactly those of the Galerkin system that was integrated.

For each η: ``N_TRAJ`` trajectories (random magnetic seed and random velocity perturbation), a
transient of ``T_BURN`` time units, then one snapshot every ``EVERY`` time units over ``T_KEEP``.
The values of η are split into training, validation and held-out test values, interleaved.

Usage:
    python3 e4_data.py [--quick] [--jobs 4] [--index i …] [--n 16]
Output: ``$E4_DATA`` (default ``experiments/data_e4``, git-ignored; ``data_e4_quick`` with --quick),
one file ``eta_<η>.npz`` per value: ``x`` (snapshots, M modes, 8 reals), ``traj``, ``t`` and the time
series of the diagnostics per trajectory. The summary ``results/e4_data[_quick].json`` (committed)
holds the statistics quoted by the digest. Regenerating the full data takes about 25 min on 4 cores.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import torch

try:
    import milady  # noqa: F401
except ImportError:  # repository checkout without `pip install -e .`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from milady.sim.mhd3d import MHD3D, MHD3DConfig
from milady.train.data import FourierPotentialSpace

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

N = 16                      # grid; the generated modes are |m_i| ≤ (N − 1)//3
NU = 0.05
KF = 2
ETAS = [float(f"{v:.5g}") for v in np.geomspace(0.08, 0.03, 11)]
TRAIN_IDX = [0, 2, 4, 6, 8, 10]
VAL_IDX = [3, 7]
TEST_IDX = [1, 5, 9]
ETA_TRAIN = [ETAS[i] for i in TRAIN_IDX]
ETA_VAL = [ETAS[i] for i in VAL_IDX]
ETA_TEST = [ETAS[i] for i in TEST_IDX]
DIAGS = ("kinetic_energy", "magnetic_energy", "injection", "kinetic_dissipation", "magnetic_dissipation",
         "magnetic_helicity", "cross_helicity", "kinetic_helicity")
FULL = dict(n_traj=24, t_burn=200.0, t_keep=200.0, every=2.0)
QUICK = dict(n_traj=8, t_burn=60.0, t_keep=60.0, every=2.0)
DT, CFL = 0.05, 1.5


def kcut(n: int = N) -> int:
    return (n - 1) // 3


def variant_tag(n: int = N, cfl: float = CFL) -> str:
    """Suffix of the outputs of a convergence check (other grid or other CFL number); empty for E4 itself."""
    return ("" if n == N else f"_n{n}") + ("" if cfl == CFL else f"_cfl{cfl:g}")


def data_dir(quick: bool = False, n: int = N, cfl: float = CFL) -> Path:
    root = os.environ.get("E4_DATA")
    base = Path(root) if root else HERE / "data_e4"
    return base.with_name(base.name + variant_tag(n, cfl) + ("_quick" if quick else ""))


def eta_file(eta: float, quick: bool = False, n: int = N, cfl: float = CFL) -> Path:
    return data_dir(quick, n, cfl) / f"eta_{eta:.5f}.npz"


# Offset of the seeds of the initial conditions (environment variable E4_DATA_SEED, default 0: the E4 data).
# Another value gives an independent realisation of the reference data, for a replication.
SEED_OFFSET = int(os.environ.get("E4_DATA_SEED", "0"))
# Another number of trajectories or kept duration for a job (H36: E4_N_TRAJ=96 E4_T_KEEP=50, the same number of snapshots
# from four times the trajectories); recorded in the configuration of the data file (n_traj, t_keep).
for _key, _env, _cast in (("n_traj", "E4_N_TRAJ", int), ("t_keep", "E4_T_KEEP", float)):
    if os.environ.get(_env):
        FULL[_key] = QUICK[_key] = _cast(os.environ[_env])


def solver_config(eta: float, n_traj: int, seed: int, n: int = N, dtype: str = "float32",
                  device: str = "cpu") -> MHD3DConfig:
    """Configuration of the E4 solver at ``eta`` (also used to restart from generated snapshots)."""
    return MHD3DConfig(n=n, mode="dynamic", nu=NU, eta=eta, forcing="abc", kf=KF, u0="laminar", u_noise=0.05,
                       b0_amp=0.1, n_traj=n_traj, seed=seed, device=device, dtype=dtype)


def space(n: int = N) -> FourierPotentialSpace:
    """Latent space of the E4 snapshots: every mode of the solver's truncation."""
    return FourierPotentialSpace(kcut(n), truncation="cube")


def simulate(index: int, quick: bool = False, n: int = N, cfl: float = CFL, device: str = "cpu") -> dict:
    """Integrate the trajectories of ``ETAS[index]``, write the snapshot file, return its summary."""
    torch.set_num_threads(1)
    cfg = QUICK if quick else FULL
    eta = ETAS[index]
    sim = MHD3D(solver_config(eta, cfg["n_traj"], seed=1000 + SEED_OFFSET + index, n=n, device=device))
    sp = space(n)
    t0 = time.time()
    steps = 0
    diag_t, diag = [], {k: [] for k in DIAGS}
    xs, ts = [], []
    t_end = cfg["t_burn"] + cfg["t_keep"]
    n_out = int(round(t_end / cfg["every"]))
    for i in range(1, n_out + 1):
        t = i * cfg["every"]
        steps += sim.advance_to(t, dt=DT, cfl=cfl)
        d = sim.diagnostics()
        diag_t.append(t)
        for k in DIAGS:
            diag[k].append(d[k])
        if t > cfg["t_burn"] + 1e-9:
            xs.append(sp.encode(sim.fields()).numpy())          # fields() returns CPU arrays
            ts.append(t)
    x = np.stack(xs, axis=1)                                   # (n_traj, n_t, M, 8)
    n_traj, n_t = x.shape[:2]
    traj = np.repeat(np.arange(n_traj), n_t)
    tt = np.tile(np.asarray(ts), n_traj)
    series = {k: np.stack(v) for k, v in diag.items()}         # (n_out, n_traj)
    path = eta_file(eta, quick, n, cfl)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, x=x.reshape(n_traj * n_t, *x.shape[2:]).astype(np.float32), traj=traj, t=tt,
                        diag_t=np.asarray(diag_t), **{f"diag_{k}": v for k, v in series.items()},
                        config=json.dumps(sim.cfg.to_dict()))
    keep = np.asarray(diag_t) > cfg["t_burn"] + 1e-9
    half = keep & (np.asarray(diag_t) <= cfg["t_burn"] + cfg["t_keep"] / 2)
    stats: dict = {"eta": eta, "Rm": 1.0 / (KF * eta), "split": split_of(index), "n_snapshots": int(len(traj)),
                   "n_traj": int(n_traj), "steps": int(steps), "dt_mean": float(t_end / steps),
                   "wall_time_s": round(time.time() - t0, 1), "forcing_amp": sim.forcing_amp}
    for k, v in series.items():
        kept = v[keep]
        per_traj = kept.mean(0)
        stats[k] = {"mean": float(kept.mean()), "sd": float(kept.std()),
                    "sd_between_traj": float(per_traj.std(ddof=1)),
                    # drift of the ensemble mean between the two halves of the kept window, in units of
                    # its standard error (trajectories are independent): |·| ≲ 2 if stationary
                    "half_drift_se": float((v[half].mean(0) - v[keep & ~half].mean(0)).mean()
                                           / max((v[half].mean(0) - v[keep & ~half].mean(0)).std(ddof=1)
                                                 / np.sqrt(n_traj), 1e-30))}
    sinks = series["kinetic_dissipation"][keep].mean() + series["magnetic_dissipation"][keep].mean()
    stats["balance_residual_total"] = float((series["injection"][keep].mean() - sinks) / sinks)
    stats["shells"] = shell_stats(sp, x.reshape(n_traj * n_t, *x.shape[2:]))
    return stats


def shell_stats(sp: FourierPotentialSpace, x: np.ndarray, chunk: int = 600) -> dict:
    """Mean shell spectra of the snapshots ``x`` (N, M, 8): E_u(k), E_B(k), magnetic helicity H(k), ⟨j·B⟩(k)."""
    from milady.train.data import _cross

    k = sp.k
    k2 = (k * k).sum(-1)
    ns = int(sp.shell.max()) + 1
    acc = {name: torch.zeros(ns, dtype=torch.float64) for name in ("E_u", "E_B", "H", "J")}
    for i in range(0, len(x), chunk):
        fh = sp.field_hat(torch.as_tensor(x[i:i + chunk]).double())
        uh, bh = fh[:, 0], fh[:, 1]
        jdens = 2.0 * ((1j * _cross(k.to(bh.dtype), bh)) * bh.conj()).real.sum(-1)
        for name, dens in (("E_u", (uh.abs() ** 2).sum(-1)), ("E_B", (bh.abs() ** 2).sum(-1)), ("H", jdens / k2), ("J", jdens)):
            acc[name] += torch.zeros(ns, dtype=torch.float64).index_add(0, sp.shell, dens.sum(0))
    return {name: (v[1:] / len(x)).tolist() for name, v in acc.items()}


def split_of(index: int) -> str:
    return "train" if index in TRAIN_IDX else ("val" if index in VAL_IDX else "test")


def load(eta: float, quick: bool = False, n: int = N) -> dict:
    """Snapshots of one η: ``x`` (N, M, 8) float32, ``traj`` (N,), ``t`` (N,)."""
    d = np.load(eta_file(eta, quick, n))
    return {"x": d["x"], "traj": d["traj"], "t": d["t"]}


def _run(args: tuple) -> dict:
    return simulate(*args)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--jobs", type=int, default=4, help="simulations run in parallel (one thread each)")
    ap.add_argument("--index", type=int, nargs="*", help="indices of ETAS to compute (default: all)")
    ap.add_argument("--n", type=int, default=N, help="grid size (default 16; other sizes go to data_e4_n<N>)")
    ap.add_argument("--cfl", type=float, default=CFL, help="CFL number of the time step (convergence check)")
    ap.add_argument("--device", default="cpu", help="device of the solver (cuda: use --jobs 1)")
    a = ap.parse_args()
    todo = a.index if a.index else list(range(len(ETAS)))
    t0 = time.time()
    with get_context("spawn").Pool(min(a.jobs, len(todo))) as pool:
        rows = pool.map(_run, [(i, a.quick, a.n, a.cfl, a.device) for i in todo], chunksize=1)
    tag = variant_tag(a.n, a.cfl) + ("_quick" if a.quick else "")
    out = RESULTS / f"e4_data{tag}.json"
    old = json.loads(out.read_text())["values"] if out.exists() and a.index else []
    rows = sorted([r for r in old if r["eta"] not in {x["eta"] for x in rows}] + rows, key=lambda r: -r["eta"])
    cfg = QUICK if a.quick else FULL
    summary = {"config": {"N": a.n, "kcut": kcut(a.n), "modes": space(a.n).n_modes, "nu": NU, "kf": KF,
                          "Re": 1.0 / (KF * NU), "etas": ETAS, "eta_train": ETA_TRAIN, "eta_val": ETA_VAL,
                          "eta_test": ETA_TEST, **cfg, "dt": DT, "cfl": a.cfl, "dtype": "float32", "device": a.device,
                          "data_seed_offset": SEED_OFFSET},
               "values": rows, "duration_s": round(time.time() - t0, 1)}
    out.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    for r in rows:
        print(f"eta {r['eta']:.5f} ({r['split']:5s}) Eu {r['kinetic_energy']['mean']:.3f} Eb {r['magnetic_energy']['mean']:.3f} "
              f"Hm {r['magnetic_helicity']['mean']:+.3f} (drift {r['magnetic_helicity']['half_drift_se']:+.1f} SE) "
              f"balance {r['balance_residual_total']:+.4f}  {r['wall_time_s']:.0f} s", flush=True)
    print(f"total {time.time() - t0:.0f} s -> {out}")


if __name__ == "__main__":
    main()
