"""Training of MilaDy generative models (stage 2: 3D MHD fields).

- ``milady.train.data``: MFF files → latent "Fourier vector potential" representation (Coulomb
  gauge, Craya–Herring basis, per-mode normalization), conditioning, datasets;
- ``milady.train.fm3d``: conditional flow matching under hard constraints (zero divergence, symmetry
  B → −B), stationarity loss, DDP, checkpoints, MLflow, catalog.

Usage: ``python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml`` (see ``make train``).
Submodules are not imported here (``import milady.train`` stays lightweight); the usual names are
available on demand: ``from milady.train import load_model``.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["FourierPotentialSpace", "GenerativeModel", "load_model", "smoke_step", "train"]

_LAZY = {
    "FourierPotentialSpace": "milady.train.data",
    "GenerativeModel": "milady.train.fm3d",
    "load_model": "milady.train.fm3d",
    "smoke_step": "milady.train.fm3d",
    "train": "milady.train.fm3d",
}


def __getattr__(name: str) -> Any:
    """Lazy import of public names (torch is only loaded on first use)."""
    if name in _LAZY:
        return getattr(import_module(_LAZY[name]), name)
    raise AttributeError(f"module 'milady.train' has no attribute {name!r}")
