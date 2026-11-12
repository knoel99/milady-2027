"""Tests of the null-point finder ``milady.eval.topology`` (trilinear method)."""

from __future__ import annotations

import numpy as np
import torch

from milady.eval.topology import null_count, null_points
from milady.train.data import FourierPotentialSpace


def _grid(n: int, shift: float = 0.1) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = 2 * np.pi * np.arange(n) / n + shift
    return np.meshgrid(x, x, x, indexing="ij")


def test_known_nulls() -> None:
    """B = (sin x, sin y, sin z): 8 nulls at x, y, z ∈ {0, π}, 4 of each sign (det ∇B = cos x cos y cos z)."""
    n = 24
    X, Y, Z = _grid(n)
    b = np.stack([np.sin(X), np.sin(Y), np.sin(Z)], axis=-1)
    out = null_points(b)
    assert int(out["count"]) == 8 and int(out["positive"]) == 4 and int(out["negative"]) == 4
    pos = (out["position"] * 2 * np.pi / n + 0.1) % (2 * np.pi)
    dist = np.minimum(np.abs(pos % np.pi), np.pi - np.abs(pos % np.pi))
    assert dist.max() < 2e-2                     # located to the interpolation error


def test_no_null_in_a_uniform_field() -> None:
    n = 12
    X, Y, Z = _grid(n)
    b = np.stack([1.0 + 0.2 * np.sin(Y), 0.1 * np.cos(Z), 0.1 * np.sin(X)], axis=-1)
    assert int(null_points(b)["count"]) == 0


def test_index_sum_vanishes_on_the_torus() -> None:
    """Random band-limited solenoidal fields: as many positive as negative nulls (Poincaré–Hopf)."""
    space = FourierPotentialSpace(3, fields=("magnetic_field",))
    x = torch.randn(6, space.n_modes, space.n_channels, generator=torch.Generator().manual_seed(0)).double()
    b = space.decode(x, 32)["magnetic_field"].numpy()
    out = null_points(b)
    assert (out["count"] > 0).all()
    assert (out["positive"] == out["negative"]).all()
    assert (out["count"] == out["positive"] + out["negative"]).all()
    assert (out["candidates"] >= out["count"]).all()
    assert (null_count(b, chunk=4) == out["count"]).all()
    assert out["position"].shape == (int(out["count"].sum()), 3)
