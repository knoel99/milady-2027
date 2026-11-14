"""E4 release - reload the cited laws from the released files and draw samples (CPU, about one minute).

    python3 experiments/e4_release_example.py [--eta 0.04899] [--n 256] [--weights FILE.pt …]

Reads the data set in the MFF format (``experiments/data_e4_mff``, or the folder given by ``--data``), rebuilds the latent
space of the models from the six training files, and draws ``n`` fields (u, B) on the 16³ grid at ``--eta`` from:

- G0 and G1, the Gaussian laws: closed-form fits to the training files, no weight file;
- W9, the flow-matching model with the mode-wise affine term, for each ``--weights`` file written by a job run with
  ``E4_SAVE_MODELS=1`` (``e4_model_W9_skip_sym_s<seed>.pt``);
- W16: the samples of W9 sent through the linear map that gives them the mean and covariance of G1 (the moments of W9
  are estimated on ``--n-recolour`` of its samples; 131 072 in the report, fewer here by default).

For each law it prints the mean magnetic and kinetic energies of the samples against those of the data file at that η
(when the data set holds it) and the largest |∇·B|. The same steps, as functions: ``load_training_set``, ``gaussian_laws``,
``load_w9``, ``sample_w9``, ``to_fields``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from milady.data import convert, read_mff  # noqa: E402
from milady.train import constraints as C  # noqa: E402
from milady.train.data import FourierPotentialSpace  # noqa: E402
from milady.train.flow import heun_sample  # noqa: E402
from milady.train.fm3d import ResMLP, SignSymmetrized  # noqa: E402

LOG_LO, LOG_HI = np.log(0.028), np.log(0.085)          # normalisation range of the condition (experiments/e4_mhd3d.py)


def cn(eta: float) -> float:
    """Condition of the models: log η mapped to [0, 1]."""
    return float(np.float32((np.log(eta) - LOG_LO) / (LOG_HI - LOG_LO)))


def load_training_set(data: Path) -> tuple[FourierPotentialSpace, torch.Tensor, torch.Tensor, dict[float, Path]]:
    """Latent space fitted on the training files, normalised training latents (N, M, 8), conditions (N,), files by η."""
    files = {float(read_mff(p, fields=[])["params"]["eta"]): p for p in sorted(data.glob("e4_eta*.h5"))}
    train = [e for e, p in files.items() if read_mff(p, fields=[])["meta"]["split"] == "train"]
    xs, cs = [], []
    for e in sorted(train, reverse=True):
        x = torch.as_tensor(convert.e4_latents(files[e])).flatten(0, 1)        # (2400, 665, 8)
        xs.append(x)
        cs.append(torch.full((len(x),), cn(e)))
    space = FourierPotentialSpace(5, symmetric_b=True, truncation="cube")
    xs = torch.cat(xs)
    space.fit(xs)
    return space, space.normalize(xs), torch.cat(cs), files


def gaussian_laws(space: FourierPotentialSpace, x: torch.Tensor, c: torch.Tensor) -> dict:
    """G0 (one covariance per Fourier mode) and G1 (full covariance), fitted on the training latents."""
    return {"G0": C.ModewiseGaussian(sign=space.sign).fit(x, c), "G1": C.FullGaussian(sign=space.sign).fit(x, c)}


def load_w9(path: Path, space: FourierPotentialSpace) -> tuple[torch.nn.Module, dict]:
    """The flow-matching model W9 from a weight file of ``E4_SAVE_MODELS=1``; returns the module and the saved record."""
    rec = torch.load(path, map_location="cpu")
    cfg = rec["config"]
    net = ResMLP(space.n_modes, space.n_channels, 1, width=cfg["width"], depth=cfg["depth"], cond_scale=0.5)
    model = SignSymmetrized(C.ModewiseAffineSkip(net, space.n_modes, space.n_channels, 1, cond_scale=0.5), space.sign)
    model.load_state_dict(rec["state_dict"])
    return model.eval(), rec


@torch.no_grad()
def sample_w9(model: torch.nn.Module, space: FourierPotentialSpace, eta: float, n: int, seed: int = 0, steps: int = 50) -> torch.Tensor:
    """``n`` normalised latents of W9 at ``eta`` (Heun scheme, ``steps`` steps)."""
    g = torch.Generator().manual_seed(seed)
    out = []
    for i in range(0, n, 256):
        z0 = torch.randn(min(256, n - i), space.n_modes, space.n_channels, generator=g)
        out.append(heun_sample(model, z0, torch.full((len(z0), 1), cn(eta)), steps=steps))
    return torch.cat(out)


def to_fields(space: FourierPotentialSpace, z: torch.Tensor) -> dict[str, np.ndarray]:
    """Normalised latents → fields ``velocity`` and ``magnetic_field`` (n, 16, 16, 16, 3)."""
    return {k: v.numpy() for k, v in space.decode(space.denormalize(z).double(), 16).items()}


def describe(name: str, f: dict[str, np.ndarray], ref: dict | None) -> None:
    eb, eu = (0.5 * (f[k] ** 2).sum(-1).mean() for k in ("magnetic_field", "velocity"))
    div = convert._max_div3(f["magnetic_field"][:8].astype(np.float32))
    txt = f"{name:28s} E_B = {eb:.4f}  E_u = {eu:.4f}  max |div B| = {div:.1e}"
    if ref:
        txt += f"   (data: E_B = {ref['E_B']:.4f}, E_u = {ref['E_u']:.4f}; E_B ratio {eb / ref['E_B']:.3f})"
    print(txt)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(ROOT / "experiments" / "data_e4_mff"))
    ap.add_argument("--eta", type=float, default=0.04899)
    ap.add_argument("--n", type=int, default=256)
    ap.add_argument("--n-recolour", type=int, default=8192)
    ap.add_argument("--weights", nargs="*", default=[])
    a = ap.parse_args()
    torch.manual_seed(0)
    space, x, c, files = load_training_set(Path(a.data))
    ref = None
    if (path := next((p for e, p in files.items() if abs(e - a.eta) < 1e-5), None)) is not None:
        d = read_mff(path, fields=["velocity", "magnetic_field"], t=slice(0, None, 4))
        ref = {"E_B": 0.5 * (d["fields"]["magnetic_field"] ** 2).sum(-1).mean(), "E_u": 0.5 * (d["fields"]["velocity"] ** 2).sum(-1).mean()}
    laws = gaussian_laws(space, x, c)
    for name, law in laws.items():
        describe(f"{name} (Gaussian law)", to_fields(space, law.sample(cn(a.eta), a.n, generator=torch.Generator().manual_seed(1))), ref)
    for w in a.weights:
        model, rec = load_w9(Path(w), space)
        describe(f"W9 seed {rec['seed']}", to_fields(space, sample_w9(model, space, a.eta, a.n, seed=rec["seed"])), ref)
        zs = sample_w9(model, space, a.eta, a.n_recolour, seed=1000 + rec["seed"]).flatten(1).double()   # moments of the model
        mu1, cov1 = laws["G1"].moments(cn(a.eta))
        amap = C.recolouring_map(torch.cov(zs.T), cov1.double())
        z = sample_w9(model, space, a.eta, a.n, seed=rec["seed"]).flatten(1).double()
        z16 = (mu1.flatten().double() + (z - zs.mean(0)) @ amap.T).float().view(-1, space.n_modes, space.n_channels)
        describe(f"W16 (W9 seed {rec['seed']} recoloured)", to_fields(space, z16), ref)


if __name__ == "__main__":
    main()
