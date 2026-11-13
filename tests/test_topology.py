"""Tests of the null-point finder ``milady.eval.topology`` (trilinear method)."""

from __future__ import annotations

import numpy as np
import torch

from milady.eval.topology import null_count, null_density_factors, null_points
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


def test_null_density_factors_predict_the_count() -> None:
    """Kac-Rice: density of the field at zero times the mean Jacobian there gives the mean number of nulls."""
    space = FourierPotentialSpace(3, fields=("magnetic_field",))
    x = torch.randn(48, space.n_modes, space.n_channels, generator=torch.Generator().manual_seed(1)).double()
    b = space.decode(x, 32)["magnetic_field"].numpy()
    counted = float(null_count(b).mean())
    out = {e: null_density_factors(b, eps=e) for e in (0.1, 0.2)}
    for e, o in out.items():
        assert o["n_small"] > 2000 and abs(o["predicted_count"] / counted - 1) < 0.15, (e, o["predicted_count"], counted)
    # the two factors do not depend on the threshold beyond the sampling noise, nor on the amplitude of the field
    assert abs(out[0.2]["density_at_zero"] / out[0.1]["density_at_zero"] - 1) < 0.1
    assert abs(out[0.2]["jacobian_at_zero"] / out[0.1]["jacobian_at_zero"] - 1) < 0.1
    scaled = null_density_factors(3.0 * b, eps=0.1)
    assert abs(scaled["density_at_zero"] / out[0.1]["density_at_zero"] - 1) < 1e-9
    assert abs(scaled["jacobian_at_zero"] / out[0.1]["jacobian_at_zero"] - 1) < 1e-9
    # a field that is twice as rough where it is weak has more nulls through the Jacobian, at equal density at zero:
    # the sum of two independent fields at wavenumbers 1 and 2 against the first alone, both normalised by their rms
    xg, yg, zg = _grid(32)
    rng = np.random.default_rng(0)
    def helical(k: int, m: int) -> np.ndarray:
        ph = rng.uniform(0, 2 * np.pi, size=(m, 3, 1, 1, 1))
        a = rng.normal(size=(m, 3, 1, 1, 1))
        return np.stack([a[:, 0] * np.sin(k * yg + ph[:, 0]) + a[:, 2] * np.cos(k * zg + ph[:, 2]),
                         a[:, 1] * np.sin(k * zg + ph[:, 1]) + a[:, 0] * np.cos(k * xg + ph[:, 0]),
                         a[:, 2] * np.sin(k * xg + ph[:, 2]) + a[:, 1] * np.cos(k * yg + ph[:, 1])], axis=-1)
    smooth, rough = helical(1, 64), helical(1, 64) + helical(2, 64)
    fs, fr = null_density_factors(smooth, eps=0.2), null_density_factors(rough, eps=0.2)
    assert fr["jacobian_at_zero"] > 1.3 * fs["jacobian_at_zero"]
    assert float(null_count(rough).mean()) > float(null_count(smooth).mean())

