"""The trilinear count finds one interior null and does not double-count grid nulls."""

from __future__ import annotations

import numpy as np

from milady.eval.nulls import _cell_nulls, count_nulls


def _corners_of(fn) -> np.ndarray:
    corners = np.zeros((2, 2, 2, 3))
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                corners[i, j, k] = fn(i, j, k)
    return corners


def test_a_linear_null_is_found_inside_the_cell():
    corners = _corners_of(lambda x, y, z: (x - 0.3, y - 0.4, z - 0.2))
    found = _cell_nulls(corners)
    assert len(found) == 1
    assert np.allclose(found[0], (0.3, 0.4, 0.2), atol=1e-6)


def test_a_trilinear_factor_does_not_move_the_null():
    corners = _corners_of(lambda x, y, z: ((x - 0.3) * (1.0 + 0.2 * y), y - 0.4, z - 0.2))
    found = _cell_nulls(corners)
    assert len(found) == 1
    assert np.allclose(found[0], (0.3, 0.4, 0.2), atol=1e-6)


def test_a_uniform_field_has_no_null():
    field = np.zeros((4, 4, 4, 3))
    field[..., 0] = 1.0
    assert count_nulls(field) == 0


def test_grid_nulls_of_a_sine_field_are_counted_once():
    n = 8
    axis = np.linspace(0.0, 1.0, n, endpoint=False)
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    field = np.stack((np.sin(2 * np.pi * x), np.sin(2 * np.pi * y), np.sin(2 * np.pi * z)), axis=-1)
    # sin(2π i / 8) = 0 at i = 0 and i = 4, so eight combinations, each shared by eight cells.
    assert count_nulls(field) == 8
