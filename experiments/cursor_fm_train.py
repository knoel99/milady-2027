"""Train a conditional flow on kinematic ABC coefficients and score it.

The network is ``milady.train.fm3d.ResMLP``. The loss and the sampler are
``milady.train.flow``. The sampling constraint projects the physical Fourier
coefficients after every Heun step. The Fourier midpoint is not trained. It
is scored by the same function so the comparison is on one protocol.

``--quick`` is one seed and a short run. It is not a quoted result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from cursor_constraint_cmp import pack, score, snapshot, unpack

from milady.train.constraints import project_solenoidal
from milady.train.data import half_ball_modes
from milady.train.flow import fm_loss, heun_sample
from milady.train.fm3d import ResMLP

TRAIN_RM = (8.0, 10.0, 11.0, 13.0, 14.0, 16.0)
TIMES = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
HELD = 12.0


def _project_packed(vec: torch.Tensor, modes: torch.Tensor) -> torch.Tensor:
    coeff = vec.reshape(*vec.shape[:-1], modes.shape[0], 3, 2)
    comp = torch.view_as_complex(coeff.contiguous())
    proj = project_solenoidal(comp, modes)
    return torch.view_as_real(proj).reshape(*vec.shape[:-1], -1)


def build_rows(seed: int, rms: tuple[float, ...], times: tuple[float, ...], modes: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    xs, cs = [], []
    for rm in rms:
        for t_end in times:
            xs.append(pack(snapshot(n, rm, seed, t_end), modes))
            cs.append([rm])
    return np.stack(xs).astype(np.float32), np.stack(cs).astype(np.float32)


def train_seed(
    data: torch.Tensor,
    cond: torch.Tensor,
    modes: torch.Tensor,
    steps: int,
    seed: int,
    device: torch.device,
    mean: torch.Tensor,
    std: torch.Tensor,
) -> ResMLP:
    torch.manual_seed(seed)
    dim = data.shape[-1]
    model = ResMLP(dim // 6, 6, n_cond=1, width=256, depth=4, expansion=2, emb_dim=128, n_freq=8).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    x = ((data - mean) / std).to(device)
    c = ((cond - HELD) / 4.0).to(device)
    batch = min(32, x.shape[0])
    for step in range(steps):
        pick = torch.randint(0, x.shape[0], (batch,), device=device)
        loss = fm_loss(model, x[pick], c[pick])
        loss.backward()
        opt.step()
        opt.zero_grad(set_to_none=True)
        if step % 200 == 0:
            print("step", step, "loss", float(loss.detach()), flush=True)
    return model


def draw(model: ResMLP, rm: float, n_samples: int, modes: torch.Tensor, mean: torch.Tensor, std: torch.Tensor, device: torch.device) -> torch.Tensor:
    dim = modes.shape[0] * 6
    z = torch.randn(n_samples, dim, device=device)
    c = torch.full((n_samples, 1), (rm - HELD) / 4.0, device=device)

    def project(state: torch.Tensor) -> torch.Tensor:
        physical = state * std + mean
        return (_project_packed(physical, modes) - mean) / std

    z = project(z)
    out = heun_sample(model, z, c, steps=32, project=project)
    return (out * std + mean).detach().cpu()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--steps", type=int, default=4000)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--kmax", type=float, default=4.0)
    parser.add_argument("--out-dir", type=Path, default=Path("experiments/results/cursor_fm"))
    args = parser.parse_args()
    n = 16
    modes_np = half_ball_modes(args.kmax)
    modes = torch.tensor(modes_np, dtype=torch.float32)
    device = torch.device(args.device)
    seeds = [0] if args.quick else [0, 1, 2, 3, 4]
    rms = (8.0, 16.0) if args.quick else TRAIN_RM
    times = (0.5, 1.0) if args.quick else TIMES
    steps = min(args.steps, 200) if args.quick else args.steps
    out = Path("/tmp/cursor_fm_quick") if args.quick else args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    saved_x, saved_c = [], []
    for seed in seeds:
        x, c = build_rows(seed, rms, times, modes_np, n)
        print("built", seed, x.shape, flush=True)
        data = torch.tensor(x)
        cond = torch.tensor(c)
        mean = data.mean(0)
        std = data.std(0).clamp_min(1e-6)
        saved_x.append(data.numpy())
        saved_c.append(cond.numpy())
        model = train_seed(data, cond, modes.to(device), steps, seed, device, mean.to(device), std.to(device))
        torch.save(
            {"state": model.state_dict(), "steps": steps, "kmax": args.kmax, "seed": seed, "mean": mean, "std": std},
            out / f"weights_s{seed}.pt",
        )
        drawn = draw(model, HELD, 8, modes.to(device), mean.to(device), std.to(device), device)
        gen = np.stack([unpack(v.numpy(), modes_np, n) for v in drawn], axis=0)
        ref = np.stack([snapshot(n, HELD, seed, t) for t in TIMES], axis=0)
        learned = score(gen, ref, HELD)
        mids = []
        for t_end in TIMES:
            left = pack(snapshot(n, 11.0, seed, t_end), modes_np)
            right = pack(snapshot(n, 13.0, seed, t_end), modes_np)
            mids.append(unpack(0.5 * (left + right), modes_np, n))
        baseline = score(np.stack(mids), ref, HELD)
        rows.append({"seed": seed, "learned": learned, "midpoint": baseline})
        print("seed", seed, "learned", learned["c1"], "midpoint", baseline["c1"], flush=True)
    np.savez(
        out / "dataset.npz",
        coefficients=np.concatenate(saved_x),
        rm=np.concatenate(saved_c),
        modes=modes_np,
    )
    payload = {"kmax": args.kmax, "n": n, "steps": steps, "held_out_rm": HELD, "seeds": rows, "quick": args.quick}
    (out / "metrics.json").write_text(json.dumps(payload, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
