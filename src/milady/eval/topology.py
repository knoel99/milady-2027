"""Magnetic topology: null points of a periodic 3D vector field.

A null point is a point where B = 0; around it the field is B ≈ M·r with M = ∇B, and the sign of
det M separates the two kinds of nulls (two eigenvalues with a negative real part and one positive,
or the reverse; Parnell, Smith, Neukirch & Priest 1996). The nulls and the separatrix surfaces and
spines that leave them form the skeleton of the field, hence their use as a topology metric for
generated magnetic fields.

Method (trilinear method of Haynes & Parnell 2007, in three stages): on each cell of the grid the
field is the trilinear interpolant of its eight corner values;

1. *reduction*: a cell can hold a null only if each of the three components changes sign among its
   eight corners (the interpolant of a component is bounded by its corner values);
2. *location*: in the remaining cells, the roots of the trilinear system are found by Newton's
   method from nine starting points (centre and centres of the eight octants), with the analytic
   Jacobian; a root is kept if it lies in the half-open cell [0, 1)³ and if the field vanishes
   there to round-off relative to the corner values; duplicates within a cell are merged;
3. *type*: sign of the determinant of the Jacobian of the interpolant at the root.

(The original method solves the bilinear systems on the cell faces to certify the reduction; here
stage 2 is tried in every cell kept by stage 1, which costs more and needs no face test.)

Check: the interpolant is a continuous vector field on the 3-torus, so by the Poincaré–Hopf theorem
the indices of its (non-degenerate) zeros sum to zero: the numbers of positive and negative nulls
must be equal. ``tests/test_topology.py`` uses it.

The count depends on the grid through the interpolation: evaluate band-limited fields on a grid
at least three times finer than their smallest wavelength (``FourierPotentialSpace.to_grid``).
"""

from __future__ import annotations

from typing import Any

import numpy as np
import torch

__all__ = ["null_count", "null_points"]

_STARTS = [(0.5, 0.5, 0.5)] + [(a, b, c) for a in (0.25, 0.75) for b in (0.25, 0.75) for c in (0.25, 0.75)]


def _trilinear(corners: torch.Tensor, p: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Value (n, 3) and Jacobian (n, 3, 3) of the trilinear interpolant at ``p`` (n, 3) ∈ cell coordinates.

    ``corners``: (n, 2, 2, 2, 3), index (a, b, c) = corner at offsets (a, b, c) along (x, y, z).
    """
    x, y, z = p[:, 0, None], p[:, 1, None], p[:, 2, None]
    c = corners
    # interpolate along z, then y, then x
    cz = c[:, :, :, 0] * (1 - z)[:, None, None] + c[:, :, :, 1] * z[:, None, None]     # (n, 2, 2, 3)
    dz = c[:, :, :, 1] - c[:, :, :, 0]
    cy = cz[:, :, 0] * (1 - y)[:, None] + cz[:, :, 1] * y[:, None]                      # (n, 2, 3)
    dy = cz[:, :, 1] - cz[:, :, 0]
    dzy = dz[:, :, 0] * (1 - y)[:, None] + dz[:, :, 1] * y[:, None]
    val = cy[:, 0] * (1 - x) + cy[:, 1] * x
    jx = cy[:, 1] - cy[:, 0]
    jy = dy[:, 0] * (1 - x) + dy[:, 1] * x
    jz = dzy[:, 0] * (1 - x) + dzy[:, 1] * x
    return val, torch.stack([jx, jy, jz], dim=-1)


def null_points(b: Any, newton_iters: int = 20, tol: float = 1e-8) -> dict[str, np.ndarray]:
    """Null points of periodic fields ``b`` of shape ``(..., nx, ny, nz, 3)``.

    Returns ``sample`` (index of the field in the flattened leading dimensions), ``position``
    (n_null, 3) in grid units (cell index + position in the cell), ``sign`` (±1: sign of det ∇B),
    ``count``, ``positive`` and ``negative`` (per field, shape of the leading dimensions) and
    ``candidates`` (number of cells kept by the reduction, per field).
    """
    f = torch.as_tensor(np.asarray(b), dtype=torch.float64)
    lead = f.shape[:-4]
    f = f.reshape(-1, *f.shape[-4:])
    ns, nx, ny, nz, _ = f.shape
    # corner values of every cell: (ns, nx, ny, nz, 2, 2, 2, 3)
    corners = torch.stack([torch.stack([torch.stack([torch.roll(f, shifts=(-a, -b_, -c), dims=(1, 2, 3))
                                                     for c in (0, 1)], dim=4)
                                        for b_ in (0, 1)], dim=4)
                           for a in (0, 1)], dim=4)
    flat = corners.reshape(ns, nx, ny, nz, 8, 3)
    lo, hi = flat.amin(dim=4), flat.amax(dim=4)
    cand = ((lo < 0) & (hi > 0)).all(dim=-1)                               # reduction
    idx = cand.nonzero()                                                   # (n_c, 4): sample, i, j, k
    cc = corners[idx[:, 0], idx[:, 1], idx[:, 2], idx[:, 3]]               # (n_c, 2, 2, 2, 3)
    scale = cc.abs().amax(dim=(1, 2, 3, 4)).clamp_min(1e-300)
    found_cell, found_pos, found_sign = [], [], []
    for start in _STARTS:
        p = torch.tensor(start, dtype=torch.float64).expand(cc.shape[0], 3).clone()
        for _ in range(newton_iters):
            val, jac = _trilinear(cc, p)
            step = torch.linalg.solve(jac + 1e-14 * scale[:, None, None] * torch.eye(3, dtype=torch.float64), val)
            p = (p - step).clamp(-1.0, 2.0)
        val, jac = _trilinear(cc, p)
        ok = (val.abs().amax(dim=1) < tol * scale) & (p >= 0).all(dim=1) & (p < 1).all(dim=1)
        found_cell.append(ok.nonzero()[:, 0])
        found_pos.append(p[ok])
        found_sign.append(torch.sign(torch.linalg.det(jac[ok])))
    cell = torch.cat(found_cell)
    pos = torch.cat(found_pos)
    sign = torch.cat(found_sign)
    # merge duplicates: same cell and same position to 1e-4 of a cell
    key = torch.cat([cell[:, None].double(), torch.round(pos * 1e4)], dim=1)
    _, first = np.unique(key.numpy(), axis=0, return_index=True)
    first = torch.as_tensor(np.sort(first))
    cell, pos, sign = cell[first], pos[first], sign[first]
    sample = idx[cell, 0]
    count = torch.bincount(sample, minlength=ns)
    positive = torch.bincount(sample[sign > 0], minlength=ns)
    negative = torch.bincount(sample[sign < 0], minlength=ns)
    return {
        "sample": sample.numpy(),
        "position": (idx[cell, 1:].double() + pos).numpy(),
        "sign": sign.numpy(),
        "count": count.numpy().reshape(lead),
        "positive": positive.numpy().reshape(lead),
        "negative": negative.numpy().reshape(lead),
        "candidates": cand.reshape(ns, -1).sum(1).numpy().reshape(lead),
    }


def null_count(b: Any, chunk: int = 8) -> np.ndarray:
    """Number of null points of each field of ``b`` ``(n, nx, ny, nz, 3)``, computed by chunks of fields."""
    arr = np.asarray(b)
    return np.concatenate([np.atleast_1d(null_points(arr[i : i + chunk])["count"]) for i in range(0, arr.shape[0], chunk)])
