"""E4 release - reload a law from the released files and draw samples (CPU).

    python3 experiments/e4_release_example.py --dir e4_release --download --law G1 --eta 0.04899 --n 256
    python3 experiments/e4_release_example.py --dir e4_release --download --law W16 --seed 0 --out samples.h5

``--dir`` is a folder that holds the files of the release (``--download`` fetches the ones that are needed from the GitHub
release and checks their SHA-256 against ``SHA256SUMS``). The laws:

- ``G0``, ``G1``: the Gaussian laws, from their parameter files (no network);
- ``W9``: the flow-matching model with the mode-wise affine term, from the weights of ``--seed``;
- ``W16``: the samples of W9 sent through the linear map that gives them the mean and covariance of G1, from the map file
  of ``--seed`` (stored at the three held-out η; at another η, or with ``--n-recolour N``, the map is recomputed from N
  samples of W9 and the parameters of G1).

Prints the mean energies of the samples and the largest |∇·B|, against the data when the file of that η is in the folder;
``--out`` writes the fields in the MFF format (``milady_code = "generated"``). In a few lines, from Python:

    import sys; sys.path[:0] = ["src", "experiments"]
    import e4_release_example as R
    space = R.load_space("e4_release")                          # latent space and its normalisation
    g1 = R.load_gaussian("e4_release", "G1")                    # Gaussian law with the full covariance
    w9 = R.load_w9("e4_release", space, seed=0)                 # flow-matching model
    z = R.sample_w9(w9, space, eta=0.04899, n=64)               # normalised latents (64, 665, 8)
    fields = R.to_fields(space, z)                              # {"velocity", "magnetic_field"}: (64, 16, 16, 16, 3)
    z1 = g1.sample(R.cn(0.04899), 64)                           # the same for the Gaussian law
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from milady.train import constraints as C  # noqa: E402
from milady.train.data import FourierPotentialSpace  # noqa: E402
from milady.train.flow import heun_sample  # noqa: E402
from milady.train.fm3d import ResMLP, SignSymmetrized  # noqa: E402

RELEASE_URL = "https://github.com/knoel99/milady-2027/releases/download/e4-data-v1.0"
LOG_LO, LOG_HI = np.log(0.028), np.log(0.085)          # normalisation range of the condition (experiments/e4_mhd3d.py)
SPACE, GAUSS, WEIGHTS, MAP = "e4_latent_space.pt", "e4_gaussian_{law}.pt", "e4_model_W9_skip_sym_s{seed}.pt", "e4_W16_map_s{seed}.pt"


def cn(eta: float) -> float:
    """Condition of the models: log η mapped to [0, 1]."""
    return float(np.float32((np.log(eta) - LOG_LO) / (LOG_HI - LOG_LO)))


def fetch(folder: str | Path, name: str, url: str = RELEASE_URL) -> Path:
    """Download ``name`` from the release into ``folder`` (if absent) and check it against ``SHA256SUMS``."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for n in ("SHA256SUMS", name):
        if not (folder / n).exists():
            print(f"downloading {n}", flush=True)
            urllib.request.urlretrieve(f"{url}/{n}", folder / n)  # noqa: S310 - fixed https URL of the release
    sums = dict(line.split()[::-1] for line in (folder / "SHA256SUMS").read_text().splitlines() if line.strip())
    h = hashlib.sha256()
    with open(folder / name, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    if sums.get(name) != h.hexdigest():
        raise ValueError(f"{name}: SHA-256 {h.hexdigest()} differs from SHA256SUMS ({sums.get(name)})")
    return folder / name


def load_space(folder: str | Path) -> FourierPotentialSpace:
    """Latent space of the models (vector potentials on the 665 modes of the solver) with its normalisation."""
    rec = torch.load(Path(folder) / SPACE, map_location="cpu")
    space = FourierPotentialSpace(rec["kmax"], symmetric_b=rec["symmetric_b"], truncation=rec["truncation"])
    space.load_state_dict(rec["state_dict"])
    return space


def load_gaussian(folder: str | Path, law: str) -> C.ModewiseGaussian | C.FullGaussian:
    """G0 (one covariance per Fourier mode) or G1 (full covariance) from its parameter file."""
    state = torch.load(Path(folder) / GAUSS.format(law=law), map_location="cpu")
    return (C.ModewiseGaussian if law == "G0" else C.FullGaussian).from_state(state)


def load_w9(folder: str | Path, space: FourierPotentialSpace, seed: int = 0) -> torch.nn.Module:
    """The flow-matching model W9 of ``seed`` from its weight file (written by a run with ``E4_SAVE_MODELS=1``)."""
    rec = torch.load(Path(folder) / WEIGHTS.format(seed=seed), map_location="cpu")
    cfg = rec["config"]
    net = ResMLP(space.n_modes, space.n_channels, 1, width=cfg["width"], depth=cfg["depth"], cond_scale=0.5)
    model = SignSymmetrized(C.ModewiseAffineSkip(net, space.n_modes, space.n_channels, 1, cond_scale=0.5), space.sign)
    model.load_state_dict(rec["state_dict"])
    return model.eval()


@torch.no_grad()
def sample_w9(model: torch.nn.Module, space: FourierPotentialSpace, eta: float, n: int, seed: int = 0, steps: int = 50,
              batch: int = 512) -> torch.Tensor:
    """``n`` normalised latents (n, M, 8) of W9 at ``eta`` (Heun scheme, ``steps`` steps)."""
    g = torch.Generator().manual_seed(seed)
    out = []
    for i in range(0, n, batch):
        z0 = torch.randn(min(batch, n - i), space.n_modes, space.n_channels, generator=g)
        out.append(heun_sample(model, z0, torch.full((len(z0), 1), cn(eta)), steps=steps))
    return torch.cat(out)


@torch.no_grad()
def moments_w9(model: torch.nn.Module, space: FourierPotentialSpace, eta: float, n: int, seed: int = 0, steps: int = 50,
               batch: int = 512) -> tuple[torch.Tensor, torch.Tensor]:
    """Mean (D,) and covariance (D, D), float64, of ``n`` samples of W9 at ``eta``, accumulated batch by batch."""
    g = torch.Generator().manual_seed(seed)
    d = space.n_modes * space.n_channels
    s1, s2 = torch.zeros(d, dtype=torch.float64), torch.zeros(d, d, dtype=torch.float64)
    for i in range(0, n, batch):
        z0 = torch.randn(min(batch, n - i), space.n_modes, space.n_channels, generator=g)
        z = heun_sample(model, z0, torch.full((len(z0), 1), cn(eta)), steps=steps).flatten(1).double()
        s1 += z.sum(0)
        s2 += z.T @ z
    mean = s1 / n
    return mean, s2 / n - torch.outer(mean, mean)


def recolouring(mean_src: torch.Tensor, cov_src: torch.Tensor, g1: C.FullGaussian, eta: float) -> dict[str, torch.Tensor]:
    """Map of W16 at ``eta`` from the moments of W9: x → mean_tgt + (x − mean_src) A, with the moments of G1 as target."""
    mu_t, cov_t = g1.moments(cn(eta))
    return {"mean_src": mean_src.float(), "map": C.recolouring_map(cov_src, cov_t).float(), "mean_tgt": mu_t.float()}


def recolour(z: torch.Tensor, rec: dict[str, torch.Tensor]) -> torch.Tensor:
    """Samples of W9 (n, M, 8) sent through the map ``rec``: samples of W16."""
    out = rec["mean_tgt"].double() + (z.flatten(1).double() - rec["mean_src"].double()) @ rec["map"].double()
    return out.float().view_as(z)


def load_map(folder: str | Path, seed: int, eta: float) -> dict[str, torch.Tensor] | None:
    """The stored map of W16 for ``seed`` at ``eta``, or ``None`` when the file does not hold that η."""
    rec = torch.load(Path(folder) / MAP.format(seed=seed), map_location="cpu")
    for i, e in enumerate(rec["eta"]):
        if abs(e - eta) < 1e-6:
            return {k: rec[k][i] for k in ("mean_src", "map", "mean_tgt")}
    return None


def to_fields(space: FourierPotentialSpace, z: torch.Tensor) -> dict[str, np.ndarray]:
    """Normalised latents → fields ``velocity`` and ``magnetic_field`` (n, 16, 16, 16, 3), float32."""
    return {k: v.numpy().astype(np.float32) for k, v in space.decode(space.denormalize(z).double(), 16).items()}


def max_div(v: np.ndarray) -> float:
    """Largest |∇·v| (spectral derivative) of fields (n, N, N, N, 3) on the box [0, 2π)³."""
    n = v.shape[-2]
    k = np.fft.fftfreq(n, 1.0 / n)
    vh = np.fft.fftn(v.astype(np.float64), axes=(1, 2, 3))
    div = 1j * (k[:, None, None] * vh[..., 0] + k[None, :, None] * vh[..., 1] + k[None, None, :] * vh[..., 2])
    return float(np.abs(np.fft.ifftn(div, axes=(1, 2, 3)).real).max())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="e4_release", help="folder of the release files")
    ap.add_argument("--download", action="store_true", help="fetch the files that are needed from the GitHub release")
    ap.add_argument("--url", default=RELEASE_URL)
    ap.add_argument("--law", default="G1", choices=("G0", "G1", "W9", "W16"))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--eta", type=float, default=0.04899)
    ap.add_argument("--n", type=int, default=256)
    ap.add_argument("--n-recolour", type=int, default=0, help="recompute the map of W16 from this many samples of W9")
    ap.add_argument("--out", default=None, help="write the samples to this MFF file")
    a = ap.parse_args()
    need = [SPACE] + {"G0": [GAUSS.format(law="G0")], "G1": [GAUSS.format(law="G1")], "W9": [WEIGHTS.format(seed=a.seed)],
                      "W16": [WEIGHTS.format(seed=a.seed), MAP.format(seed=a.seed)]}[a.law]
    if a.download:
        for name in need:
            fetch(a.dir, name, a.url)
    space = load_space(a.dir)
    if a.law in ("G0", "G1"):
        z = load_gaussian(a.dir, a.law).sample(cn(a.eta), a.n, generator=torch.Generator().manual_seed(a.seed))
    else:
        model = load_w9(a.dir, space, a.seed)
        z = sample_w9(model, space, a.eta, a.n, seed=a.seed)
        if a.law == "W16":
            rec = None if a.n_recolour else load_map(a.dir, a.seed, a.eta)
            if rec is None:
                if a.download:
                    fetch(a.dir, GAUSS.format(law="G1"), a.url)
                n_rec = a.n_recolour or 8192
                print(f"recomputing the map of W16 from {n_rec} samples of W9", flush=True)
                rec = recolouring(*moments_w9(model, space, a.eta, n_rec, seed=1000 + a.seed), load_gaussian(a.dir, "G1"), a.eta)
            z = recolour(z, rec)
    f = to_fields(space, z)
    eb, eu = (0.5 * (f[k].astype(np.float64) ** 2).sum(-1).mean() for k in ("magnetic_field", "velocity"))
    print(f"{a.law} at eta = {a.eta}: {a.n} samples, E_B = {eb:.4f}, E_u = {eu:.4f}, max |div B| = {max_div(f['magnetic_field'][:16]):.1e}")
    data = Path(a.dir) / f"e4_eta{a.eta:.5f}.h5"
    if data.exists():
        from milady.data import read_mff

        d = read_mff(data, fields=["velocity", "magnetic_field"], t=slice(0, None, 4))["fields"]
        rb, ru = (0.5 * (d[k].astype(np.float64) ** 2).sum(-1).mean() for k in ("magnetic_field", "velocity"))
        print(f"data at that eta: E_B = {rb:.4f}, E_u = {ru:.4f}; ratio of the magnetic energies {eb / rb:.3f}")
    if a.out:
        from milady.data import write_mff

        x = 2 * np.pi * np.arange(16) / 16
        write_mff(a.out, {k: v[:, None] for k, v in f.items()}, {"time": np.zeros(1), "x": x, "y": x, "z": x},
                  {"nu": 0.05, "eta": a.eta, "Re": 10.0, "Rm": 1.0 / (2 * a.eta), "kf": 2.0, "forcing": "ABC"},
                  meta={"code": "generated", "code_version": f"E4 release, law {a.law}, seed {a.seed}", "experiment": "E4"},
                  dataset_name="milady_e4_generated")
        print(f"written {a.out}: {a.n} independent samples (one trajectory of one snapshot each)")


if __name__ == "__main__":
    main()
