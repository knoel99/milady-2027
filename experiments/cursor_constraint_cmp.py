"""Compare a sampling constraint with an unconstrained baseline on one held-out Rm.

Both variants are small conditional flows on the same low-mode Fourier
coefficients of a kinematic ABC field. The sampling-constraint variant removes
the longitudinal part after every Heun step. The baseline does not.

This is a CPU comparison at n = 16. It is not a 3D generator result at the
resolution of the ABC threshold runs. ``--quick`` writes a git-ignored file
and is not a quoted result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn

from milady.eval.metrics import compare_ensembles, divergence_relative
from milady.sim.mhd3d import MHD3D, MHD3DConfig
from milady.train.constraints import project_solenoidal
from milady.train.data import half_ball_modes
from milady.train.flow import fm_loss, heun_sample


def snapshot(n: int, rm: float, seed: int, t_end: float) -> np.ndarray:
    """One real-space B, shape (n, n, n, 3), float64."""
    sim = MHD3D(
        MHD3DConfig(
            n=n,
            mode="kinematic",
            flow="abc",
            eta=1.0 / rm,
            b0_amp=1.0,
            seed=seed,
            device="cpu",
            dtype="float64",
        )
    )
    dt = min(0.05, float(sim.cfl_dt(1.0)))
    for _ in range(max(1, round(t_end / dt))):
        sim.step(dt)
    return sim._ifft(sim.bh)[0].movedim(0, -1).detach().cpu().numpy()


def pack(field: np.ndarray, modes: np.ndarray) -> np.ndarray:
    """Real vector of the half-ball coefficients, length M*6."""
    n = field.shape[0]
    hat = np.fft.rfftn(np.moveaxis(field, -1, 0), axes=(1, 2, 3), norm="forward")
    cols = []
    for mx, my, mz in modes:
        coeff = hat[:, int(mx) % n, int(my) % n, int(mz)]
        cols.append(np.stack((coeff.real, coeff.imag), axis=-1).reshape(-1))
    return np.concatenate(cols).astype(np.float64)


def unpack(vec: np.ndarray, modes: np.ndarray, n: int) -> np.ndarray:
    """Real field (n, n, n, 3) from a packed coefficient vector."""
    hat = np.zeros((3, n, n, n // 2 + 1), dtype=np.complex128)
    arr = np.asarray(vec, dtype=np.float64).reshape(len(modes), 3, 2)
    for i, (mx, my, mz) in enumerate(modes):
        coeff = arr[i, :, 0] + 1j * arr[i, :, 1]
        hat[:, int(mx) % n, int(my) % n, int(mz)] = coeff
        if int(mz) == 0:
            hat[:, (-int(mx)) % n, (-int(my)) % n, 0] = np.conjugate(coeff)
    field = np.fft.irfftn(hat, s=(n, n, n), axes=(1, 2, 3), norm="forward")
    return np.moveaxis(field, 0, -1)


class _Velocity(nn.Module):
    def __init__(self, dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim + 2, 64), nn.SiLU(), nn.Linear(64, dim))

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat((x, t[:, None], c), dim=-1))


def _to_complex(vec: torch.Tensor, n_modes: int) -> torch.Tensor:
    real = vec.reshape(*vec.shape[:-1], n_modes, 3, 2)
    return torch.view_as_complex(real.contiguous())


def _to_real(coeff: torch.Tensor) -> torch.Tensor:
    return torch.view_as_real(coeff).reshape(*coeff.shape[:-2], -1)


def train_one(data: torch.Tensor, cond: torch.Tensor, steps: int, seed: int) -> _Velocity:
    """Adam on the conditional flow loss. Both variants share this training."""
    torch.manual_seed(seed)
    model = _Velocity(data.shape[-1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(steps):
        loss = fm_loss(model, data, cond)
        loss.backward()
        opt.step()
        opt.zero_grad(set_to_none=True)
    return model


def sample(model: _Velocity, rm: float, n_samples: int, steps: int, project: bool, k: torch.Tensor) -> torch.Tensor:
    dim = model.net[-1].out_features
    z = torch.randn(n_samples, dim)
    c = torch.full((n_samples, 1), float(rm))
    proj = None
    if project:
        n_modes = k.shape[0]

        def proj(state: torch.Tensor, wave=k, modes=n_modes) -> torch.Tensor:
            return _to_real(project_solenoidal(_to_complex(state, modes), wave))

        z = proj(z)
    return heun_sample(model, z, c, steps=steps, project=proj).detach()


def score(gen: np.ndarray, ref: np.ndarray, rm: float) -> dict[str, float]:
    params = {"mode": "kinematic", "flow": "abc", "eta": 1.0 / rm, "nu": 1.0 / rm, "A": 1.0, "B": 1.0, "C": 1.0}
    out = compare_ensembles({"magnetic_field": gen}, {"magnetic_field": ref}, params, n_shells=4)
    m = out["metrics"]
    floor = float(m.get("energy_distance_floor", float("nan")))
    dist = float(m["energy_distance"])
    ratio = dist / floor if floor > 0 else float("nan")
    div = divergence_relative(gen, per_sample=True)
    hel_g = float(m["magnetic_helicity_mean"])
    # The reference helicity is not in the comparison row. Recompute it on the reference ensemble.
    ref_cmp = compare_ensembles({"magnetic_field": ref}, None, params, n_shells=4)
    hel_r = float(ref_cmp["metrics"]["magnetic_helicity_mean"])
    hel = abs(hel_g - hel_r) / max(abs(hel_r), 1e-30)
    sg = np.asarray(out["details"]["spectrum_b"], dtype=np.float64)
    sr = np.asarray(out["details"]["spectrum_b_ref"], dtype=np.float64)
    spectrum_l2 = float(np.linalg.norm(sg - sr) / max(np.linalg.norm(sr), 1e-30))
    residual = abs(float(m.get("balance_residual_magnetique", float("nan"))))
    return {
        "c1": ratio,
        "div_max": float(np.max(div)),
        "c3": residual,
        "spectrum_l2": spectrum_l2,
        "helicity_rel": hel,
        "c4": spectrum_l2 + hel,
        "finite": bool(np.isfinite(gen).all() and all(np.isfinite(v) for v in m.values())),
    }


def run(seeds: list[int], steps: int, n_samples: int) -> dict:
    n = 16
    modes = half_ball_modes(2.0)
    k = torch.tensor(modes, dtype=torch.float64)
    train_rm = (8.0, 16.0)
    held = 12.0
    ref = np.stack([snapshot(n, held, s, 1.0) for s in range(n_samples)], axis=0)
    rows = []
    for seed in seeds:
        xs, cs = [], []
        for rm in train_rm:
            for t_end in (0.5, 1.0):
                xs.append(pack(snapshot(n, rm, seed, t_end), modes))
                cs.append([rm])
        data = torch.tensor(np.stack(xs), dtype=torch.float32)
        cond = torch.tensor(cs, dtype=torch.float32)
        row: dict = {"seed": seed}
        for name, project in (("projected", True), ("free", False)):
            model = train_one(data, cond, steps, seed)
            drawn = sample(model, held, n_samples, steps=8, project=project, k=k.to(torch.float32))
            fields = np.stack([unpack(v, modes, n) for v in drawn.numpy()], axis=0)
            stats = score(fields, ref, held)
            row[name] = stats
        rows.append(row)
        print("seed", seed, "projected_div", row["projected"]["div_max"], "free_div", row["free"]["div_max"], flush=True)
    return {"held_out_rm": held, "n": n, "steps": steps, "seeds": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.quick:
        result = run([0], steps=5, n_samples=2)
        dest = args.out or Path("experiments/results/cursor_constraint_quick.json")
    else:
        result = run([0, 1, 2, 3, 4], steps=40, n_samples=8)
        dest = args.out or Path("experiments/results/cursor_constraint_cmp.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
