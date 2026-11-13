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

__all__ = ["null_count", "null_density_factors", "null_density_jackknife", "null_points"]

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


def null_points(b: Any, newton_iters: int = 20, tol: float = 1e-8,
                device: str | torch.device | None = None) -> dict[str, np.ndarray]:
    """Null points of periodic fields ``b`` of shape ``(..., nx, ny, nz, 3)`` (computed on ``device``).

    Returns ``sample`` (index of the field in the flattened leading dimensions), ``position``
    (n_null, 3) in grid units (cell index + position in the cell), ``sign`` (±1: sign of det ∇B),
    ``count``, ``positive`` and ``negative`` (per field, shape of the leading dimensions) and
    ``candidates`` (number of cells kept by the reduction, per field).
    """
    f = torch.as_tensor(np.asarray(b), dtype=torch.float64, device=device)
    dev = f.device
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
        p = torch.tensor(start, dtype=torch.float64, device=dev).expand(cc.shape[0], 3).clone()
        for _ in range(newton_iters):
            val, jac = _trilinear(cc, p)
            step = torch.linalg.solve(jac + 1e-14 * scale[:, None, None] * torch.eye(3, dtype=torch.float64, device=dev), val)
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
    _, first = np.unique(key.cpu().numpy(), axis=0, return_index=True)
    first = torch.as_tensor(np.sort(first), device=dev)
    cell, pos, sign = cell[first], pos[first], sign[first]
    sample = idx[cell, 0]
    count = torch.bincount(sample, minlength=ns)
    positive = torch.bincount(sample[sign > 0], minlength=ns)
    negative = torch.bincount(sample[sign < 0], minlength=ns)
    return {
        "sample": sample.cpu().numpy(),
        "position": (idx[cell, 1:].double() + pos).cpu().numpy(),
        "sign": sign.cpu().numpy(),
        "count": count.cpu().numpy().reshape(lead),
        "positive": positive.cpu().numpy().reshape(lead),
        "negative": negative.cpu().numpy().reshape(lead),
        "candidates": cand.reshape(ns, -1).sum(1).cpu().numpy().reshape(lead),
    }


def null_count(b: Any, chunk: int = 8, device: str | torch.device | None = None) -> np.ndarray:
    """Number of null points of each field of ``b`` ``(n, nx, ny, nz, 3)``, computed by chunks of fields."""
    arr = np.asarray(b)
    return np.concatenate([np.atleast_1d(null_points(arr[i : i + chunk], device=device)["count"])
                           for i in range(0, arr.shape[0], chunk)])


def null_density_factors(b: Any, eps: float = 0.1, weights: Any = None, device: str | torch.device | None = None,
                         chunk: int = 16) -> dict:
    """The two factors of the expected number of null points of an ensemble of fields ``b`` ``(n, nx, ny, nz, 3)``.

    For a random field the mean number of zeros per unit volume is (Kac–Rice)

        p_B(0) · E[ |det ∇B|  given  B = 0 ],

    the density of the field at the value zero times the mean Jacobian where it vanishes. Both are estimated on
    the cells of the grid, with the value and the gradient of the trilinear interpolant at the cell centre: the
    density from the share of cells where |B| is below ``eps`` times the root-mean-square of |B| over the
    ensemble, the Jacobian as the mean of |det ∇B| over these cells. Returned, with B in units of that rms and
    lengths in grid cells: ``density_at_zero``, ``jacobian_at_zero``, their product times the number of cells
    ``predicted_count`` (to compare with :func:`null_count`), the share ``small_fraction`` and the number
    ``n_small`` of cells used, ``rms``, ``jacobian_all`` (the mean of |det ∇B| over all the cells, same units:
    is the field rougher everywhere or only where it is weak?) and ``per_field``, the sums of each field from
    which :func:`null_density_jackknife` recomputes the factors without a group of fields. Two ensembles with the same number of nulls can differ in both
    factors, and a Gaussian field is fixed by its covariance in both; the ratio of the factors between two
    ensembles tells whether one has fewer nulls because its field is more rarely weak or because it varies
    more slowly where it is weak. ``weights`` (n,): weights of the fields (default: equal).
    """
    arr = np.asarray(b)
    n = arr.shape[0]
    w = np.full(n, 1.0 / n) if weights is None else np.asarray(weights, dtype=np.float64) / float(np.sum(np.asarray(weights)))
    cells = arr.shape[1] * arr.shape[2] * arr.shape[3]
    rms = float(np.sqrt(np.sum(w * (arr.astype(np.float64) ** 2).sum(axis=(1, 2, 3, 4))) / cells))

    def nxt(a: torch.Tensor, ax: int) -> torch.Tensor:           # the next grid point along an axis (periodic)
        return torch.roll(a, -1, dims=ax)

    def avg(a: torch.Tensor, ax: int) -> torch.Tensor:
        return 0.5 * (a + nxt(a, ax))

    s_small, s_det, n_small = 0.0, 0.0, 0
    per = {"small": [], "det_small": [], "det_all": [], "b2": (arr.astype(np.float64) ** 2).sum(axis=(1, 2, 3, 4))}
    for i in range(0, n, chunk):                                  # by chunks of fields: the Jacobian takes 9 values per cell
        t = torch.as_tensor(arr[i:i + chunk], dtype=torch.float64, device=device)
        wf = torch.as_tensor(w[i:i + chunk], dtype=torch.float64, device=t.device).view(-1, 1, 1, 1)
        centre = avg(avg(avg(t, 1), 2), 3)
        jac = torch.stack([avg(avg(nxt(t, 1) - t, 2), 3), avg(avg(nxt(t, 2) - t, 1), 3), avg(avg(nxt(t, 3) - t, 1), 2)], dim=-1)
        small = (centre.norm(dim=-1) < eps * rms).to(torch.float64)
        det = torch.linalg.det(jac).abs()
        s_small += float((small * wf).sum())
        s_det += float((det * small * wf).sum())
        n_small += int(small.sum())
        per["small"].append(small.sum(dim=(1, 2, 3)).cpu().numpy())
        per["det_small"].append((det * small).sum(dim=(1, 2, 3)).cpu().numpy())
        per["det_all"].append(det.sum(dim=(1, 2, 3)).cpu().numpy())
    frac = s_small / cells                                        # weighted share of the cells with a weak field
    j0 = s_det / s_small / rms**3 if s_small > 0 else float("nan")
    p0 = frac / (4.0 / 3.0 * np.pi * eps**3)
    per = {k: (np.concatenate(v) if isinstance(v, list) else v) for k, v in per.items()}
    j_all = float(np.sum(w * per["det_all"]) / cells) / rms**3
    return {"eps": eps, "rms": rms, "density_at_zero": p0, "jacobian_at_zero": j0, "predicted_count": cells * p0 * j0,
            "small_fraction": frac, "n_small": n_small, "jacobian_all": j_all, "cells": cells, "per_field": per}


def null_density_jackknife(factors: dict, groups: Any) -> dict:
    """Delete-one-group jackknife standard errors of the factors returned by :func:`null_density_factors` (equal
    weights). ``groups`` (n,): the group of each field (the trajectory of a snapshot). The cells with a weak field
    are those of the whole ensemble (threshold ``eps`` times its rms); the units follow the rms of the fields kept.
    Returns ``density_at_zero_se``, ``jacobian_at_zero_se``, ``jacobian_all_se`` and ``predicted_count_se``."""
    per, eps, cells, rms = factors["per_field"], factors["eps"], factors["cells"], factors["rms"]
    g = np.asarray(groups)
    ids = np.unique(g)
    est = []
    for k in ids:
        keep = g != k
        m = int(keep.sum())
        r = float(np.sqrt(per["b2"][keep].sum() / (m * cells)))
        frac = per["small"][keep].sum() / (m * cells)
        p0 = frac / (4.0 / 3.0 * np.pi * eps**3) * (r / rms) ** 3
        j0 = per["det_small"][keep].sum() / per["small"][keep].sum() / r**3
        est.append((p0, j0, per["det_all"][keep].sum() / (m * cells) / r**3, cells * p0 * j0))
    est = np.asarray(est)
    se = np.sqrt((len(ids) - 1) / len(ids) * ((est - est.mean(0)) ** 2).sum(0))
    return {"density_at_zero_se": float(se[0]), "jacobian_at_zero_se": float(se[1]), "jacobian_all_se": float(se[2]),
            "predicted_count_se": float(se[3])}

