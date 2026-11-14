"""E4 diagnostic - polarity of the large-scale magnetic field along the trajectories of the reference data.

The internship offer places the work in the context of polarity reversals. In E4 the magnetic field of largest
scale lives on the three wavevectors of modulus 1. The ABC force at kf = 2 is invariant under a shift of π along
an axis, which changes the sign of the modes k = 1 along that axis: the law of each of these modes is symmetric
under a change of sign, and a *reversal* of one of them is a passage of its complex amplitude to the opposite
half-plane. This script measures, on the snapshots of ``experiments/e4_data.py`` (24 trajectories of 198 time
units per η, one snapshot every 2), for each of the three modes:

- the autocorrelation ρ(τ) = ⟨Re b̂(t)·b̂*(t+τ)⟩ / ⟨|b̂|²⟩ (1: frozen polarity; 0: forgotten; negative: reversed),
  and the lag at which it falls under 1/e;
- the fraction of (trajectory, mode) pairs whose projection on its initial value Re b̂(t)·b̂*(t₀) is negative at
  the end of the window, and at some time of the window;
- the share of the magnetic energy held by the modes k = 1.

Descriptive only: no hypothesis, no threshold, and the data of the session container (another draw of the same
law than the data of the GPU pods). Output: ``results/e4_polarity_diag.json``.

    python3 e4_polarity_diag.py
"""
from __future__ import annotations

import json

import numpy as np
import torch

import e4_data as D

TAUS = (2, 10, 20, 50, 100, 150, 198)


def measure(eta: float) -> dict:
    d = D.load(eta)
    sp = D.space()
    n_traj = int(d["traj"].max()) + 1
    x = torch.as_tensor(d["x"]).double()
    bh = sp.field_hat(x)[:, 1]                                  # (N, M, 3) complex coefficients of B
    k2 = (sp.k * sp.k).sum(-1)
    big = torch.nonzero(k2 == 1).flatten()
    b1 = bh[:, big].reshape(n_traj, -1, len(big), 3).numpy()    # (traj, t, 3 modes, 3)
    e_all = (bh.abs() ** 2).sum((-1, -2)).mean().item()
    e_big = (np.abs(b1) ** 2).sum((-1, -2)).mean()
    n_t = b1.shape[1]
    dt = float(d["t"][1] - d["t"][0])
    norm = (np.abs(b1) ** 2).sum(-1).mean()
    rho = {}
    for tau in TAUS:
        lag = int(round(tau / dt))
        if lag < n_t:
            rho[str(tau)] = float((b1[:, :-lag] * b1[:, lag:].conj()).sum(-1).real.mean() / norm)
    full = [1.0] + [float((b1[:, :-lag] * b1[:, lag:].conj()).sum(-1).real.mean() / norm) for lag in range(1, n_t)]
    below = next((i for i, r in enumerate(full) if r < np.exp(-1)), None)       # first lag under 1/e, interpolated
    tau_e = None if below is None else dt * (below - 1 + (full[below - 1] - np.exp(-1)) / (full[below - 1] - full[below]))
    proj = (b1 * b1[:, :1].conj()).sum(-1).real               # (traj, t, mode): projection on the initial value
    per_traj = (b1[:, :-1] * b1[:, 1:].conj()).sum(-1).real.mean(1) / (np.abs(b1) ** 2).sum(-1).mean(1)
    return {"eta": eta, "split": D.split_of(D.ETAS.index(eta)), "n_traj": n_traj, "n_t": n_t, "window": dt * (n_t - 1),
            "share_of_E_B_at_k1": float(e_big / e_all), "rho": rho, "tau_1_over_e": tau_e,
            "rho_lag1_sd_between_traj": float(per_traj.mean(-1).std(ddof=1)),
            "fraction_opposite_at_end": float((proj[:, -1] < 0).mean()),
            "fraction_opposite_at_some_time": float((proj < 0).any(1).mean()),
            "pairs": int(proj.shape[0] * proj.shape[2])}


def main() -> None:
    torch.set_num_threads(4)
    out = {"note": "descriptive diagnostic on the data of the session container; no hypothesis, no threshold",
           "taus": list(TAUS), "values": {f"{e:.5f}": measure(e) for e in D.ETAS}}
    (D.RESULTS / "e4_polarity_diag.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for e, v in out["values"].items():
        print(e, v["split"], f"k=1 share {v['share_of_E_B_at_k1']:.3f}", f"tau_1/e {v['tau_1_over_e']:.1f}", "rho", {k: round(r, 3) for k, r in v["rho"].items()},
              f"opposite at end {v['fraction_opposite_at_end']:.2f}, at some time {v['fraction_opposite_at_some_time']:.2f}")


if __name__ == "__main__":
    main()
