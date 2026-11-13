"""Nulls of a trilinear interpolant on a periodic grid.

On each cell the field is the trilinear interpolant of the eight corners.
One coordinate is eliminated. The other two components become polynomial
equations, and their resultant is solved in one variable. A candidate is kept
only if the interpolant itself is numerically zero there. A root on the upper
face of a cell is left to the next cell, so a periodic grid counts each null
once.

This is the elimination behind the trilinear null finder of Haynes and
Parnell, Physics of Plasmas 14, 082107 (2007). It is not a sign-change octree.
"""

from __future__ import annotations

import numpy as np
from numpy.polynomial.polynomial import polyadd, polymul

_TOL_COEFF = 1e-12


def _is_zero(poly: np.ndarray) -> bool:
    return float(np.max(np.abs(poly))) <= _TOL_COEFF


def _det(matrix: list[list[np.ndarray]]) -> np.ndarray:
    """Determinant of a matrix of polynomials, lowest degree first."""
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    acc = np.zeros(1, dtype=np.float64)
    for col in range(n):
        minor = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        term = polymul(matrix[0][col], _det(minor))
        acc = polyadd(acc, term if col % 2 == 0 else -term)
    return acc


def _bilinear_product(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Product of two bilinears. Order: 1, x, y, xy, x², y², x²y, xy², x²y²."""
    a00, a10, a01, a11 = (float(v) for v in p)
    b00, b10, b01, b11 = (float(v) for v in q)
    return np.array(
        [
            a00 * b00,
            a00 * b10 + a10 * b00,
            a00 * b01 + a01 * b00,
            a00 * b11 + a11 * b00 + a10 * b01 + a01 * b10,
            a10 * b10,
            a01 * b01,
            a10 * b11 + a11 * b10,
            a01 * b11 + a11 * b01,
            a11 * b11,
        ],
        dtype=np.float64,
    )


def _group(coeff: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A2(y) x² + A1(y) x + A0(y), each quadratic in y, lowest degree first."""
    a2 = np.array([coeff[4], coeff[6], coeff[8]], dtype=np.float64)
    a1 = np.array([coeff[1], coeff[3], coeff[7]], dtype=np.float64)
    a0 = np.array([coeff[0], coeff[2], coeff[5]], dtype=np.float64)
    return a2, a1, a0


def _resultant(a2, a1, a0, b2, b1, b0) -> np.ndarray:
    """Resultant in y. Degrees fall back when a leading coefficient is identically zero."""
    zero = np.zeros(1, dtype=np.float64)
    if _is_zero(a2) and _is_zero(b2):
        return polyadd(polymul(a1, b0), -polymul(a0, b1))
    if _is_zero(a2):
        return _resultant(b2, b1, b0, a2, a1, a0)
    if _is_zero(b2):
        # degree 2 and degree 1: 3×3 Sylvester matrix
        return _det(
            [
                [a2, a1, a0],
                [b1, b0, zero],
                [zero, b1, b0],
            ]
        )
    return _det(
        [
            [a2, a1, a0, zero],
            [zero, a2, a1, a0],
            [b2, b1, b0, zero],
            [zero, b2, b1, b0],
        ]
    )


def _eval_bilinear(coeff: np.ndarray, x: float, y: float) -> float:
    return float(coeff[0] + coeff[1] * x + coeff[2] * y + coeff[3] * x * y)


def _interpolate(corners: np.ndarray, point: np.ndarray) -> np.ndarray:
    x, y, z = (float(v) for v in point)
    acc = np.zeros(3, dtype=np.float64)
    for i in (0, 1):
        wx = x if i else 1.0 - x
        for j in (0, 1):
            wy = y if j else 1.0 - y
            for k in (0, 1):
                wz = z if k else 1.0 - z
                acc += wx * wy * wz * corners[i, j, k]
    return acc


def _cell_nulls(corners: np.ndarray) -> list[tuple[float, float, float]]:
    """Nulls with coordinates in [0, 1). ``corners`` has shape (2, 2, 2, 3)."""
    found: list[tuple[float, float, float]] = []
    for pivot in range(3):
        others = [i for i in range(3) if i != pivot]
        local = np.transpose(corners, (others[0], others[1], pivot, 3))
        c000, c100 = local[0, 0, 0], local[1, 0, 0]
        c010, c001 = local[0, 1, 0], local[0, 0, 1]
        c110, c101 = local[1, 1, 0], local[1, 0, 1]
        c011, c111 = local[0, 1, 1], local[1, 1, 1]
        a = c000
        b = c100 - c000
        c = c010 - c000
        d = c001 - c000
        e = c110 - c100 - c010 + c000
        f = c101 - c100 - c001 + c000
        g = c011 - c010 - c001 + c000
        h = c111 - c110 - c101 - c011 + c100 + c010 + c001 - c000
        n_piv = np.array([a[2], b[2], c[2], e[2]])
        d_piv = np.array([d[2], f[2], g[2], h[2]])
        equations = []
        for comp in (0, 1):
            n_comp = np.array([a[comp], b[comp], c[comp], e[comp]])
            d_comp = np.array([d[comp], f[comp], g[comp], h[comp]])
            equations.append(_group(_bilinear_product(d_piv, n_comp) - _bilinear_product(n_piv, d_comp)))
        res = _resultant(*equations[0], *equations[1])
        if _is_zero(res):
            continue
        for raw_y in np.roots(res[::-1]):
            if abs(raw_y.imag) > 1e-7 or not (0.0 <= float(raw_y.real) < 1.0):
                continue
            yy = float(raw_y.real)
            a2, a1, a0 = (float(np.polyval(coeff[::-1], yy)) for coeff in equations[0])
            if abs(a2) < _TOL_COEFF and abs(a1) < _TOL_COEFF:
                continue
            for raw_x in np.roots([a2, a1, a0] if abs(a2) >= _TOL_COEFF else [a1, a0]):
                if abs(raw_x.imag) > 1e-7 or not (0.0 <= float(raw_x.real) < 1.0):
                    continue
                xx = float(raw_x.real)
                den = _eval_bilinear(d_piv, xx, yy)
                if abs(den) <= _TOL_COEFF:
                    continue
                zz = -_eval_bilinear(n_piv, xx, yy) / den
                if not (0.0 <= zz < 1.0):
                    continue
                point = np.zeros(3, dtype=np.float64)
                point[others[0]] = xx
                point[others[1]] = yy
                point[pivot] = zz
                if np.max(np.abs(_interpolate(corners, point))) <= 1e-6:
                    found.append((float(point[0]), float(point[1]), float(point[2])))
    unique: list[tuple[float, float, float]] = []
    for pt in found:
        if all(max(abs(pt[i] - old[i]) for i in range(3)) > 1e-4 for old in unique):
            unique.append(pt)
    return unique


def count_nulls(field: np.ndarray) -> int:
    """Number of trilinear nulls of a periodic vector field ``(..., n, n, n, 3)``."""
    data = np.asarray(field, dtype=np.float64)
    if data.shape[-1] != 3 or data.ndim < 4:
        raise ValueError("field must have shape (..., n, n, n, 3)")
    lead = int(np.prod(data.shape[:-4], dtype=int))
    grid = data.reshape((lead, *data.shape[-4:]))
    total = 0
    n = int(grid.shape[1])
    for sample in range(lead):
        vol = grid[sample]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    corners = vol[np.ix_((i, (i + 1) % n), (j, (j + 1) % n), (k, (k + 1) % n))]
                    total += len(_cell_nulls(np.asarray(corners)))
    return total
