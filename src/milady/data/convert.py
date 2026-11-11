"""Converters to the MFF 1.0 format, and skeleton of the SFEMaNS extension (Fourier × finite elements).

- **E2** (``experiments/e2_data.py``): ``eta_<η>_<split>.npz`` files containing the Fourier coefficients
  (``numpy.fft.rfft2``, ``[ky, kx]`` layout of ``mhd2d.py``) of the vorticity ω and of the magnetic
  potential a for 16 members × n snapshots. Each file becomes a 2D MFF simulation: fields
  ``velocity`` and ``magnetic_field`` (32² grid, The Well ``[x, y]`` layout), coefficients
  ``milady_spectral/{vorticity, magnetic_potential}`` (``rfftn`` over ``[x, y]``), per-snapshot
  diagnostics (energies, enstrophy, dissipation, cross helicity, max |∇·B|).
- **SFEMaNS** (``grid_type = "fourier_fe_axisym"``): :func:`write_fourier_fe_mff` writes fields
  given by a meridian mesh (r, z) × azimuthal modes m; :func:`fourier_fe_to_grid` and
  :func:`fourier_fe_to_cartesian` interpolate them onto a regular grid. Reading the native
  SFEMaNS files is not implemented (non-public data): see ``docs/specs/data-format.md``.

Command line:

    python -m milady.data.convert e2 <npz_dir> <output> [--catalog [URL]] [--store URI] [--limit N]
    python -m milady.data.convert validate <file> [...]
    python -m milady.data.convert info <file>
    python -m milady.data.convert zarr <file.h5> <uri.zarr>
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time as _time
import uuid as _uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import h5py
import numpy as np

from milady import git_commit, storage
from milady.data import format as mff

__all__ = [
    "E2_DEFAULTS",
    "convert_e2",
    "convert_e2_file",
    "e2_physical",
    "fourier_fe_to_cartesian",
    "fourier_fe_to_grid",
    "main",
    "write_fourier_fe_mff",
]

# =============================================================================================
# E2: forced 2D MHD (experiments/e2_data.py, experiments/mhd2d.py)
# =============================================================================================
#: Values from e2_data.py used if meta.json is absent or incomplete.
E2_DEFAULTS: dict[str, Any] = {
    "N": 32,
    "nu": 8e-3,
    "alpha": 0.02,
    "kf": [2.0, 3.0],
    "eps": 0.05,
    "dt": 1e-2,
    "intervalle": 1.0,
    "membres": 16,
    "t_burn": 30.0,
    "kmax": 10,
}
E2_NONDIM = (
    "Periodic domain [0, 2π)²; B in Alfvén units (same unit as u); ν and η dimensionless "
    "(inverses of Reynolds numbers built on length 1 and velocity 1); white-in-time forcing "
    "with mean injection rates eps_u (vorticity) and eps_b (potential), band kf_min ≤ |k| ≤ kf_max; "
    "linear friction α at large scales."
)
_E2_NAME = re.compile(r"eta_(?P<eta>[0-9.]+)_(?P<split>[a-z]+)\.npz$")


def _e2_wavenumbers(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Wavenumbers of ``mhd2d.py``: arrays ``(n, n//2+1)``, axis 0 = ky (fftfreq), axis 1 = kx (rfftfreq)."""
    k = np.fft.fftfreq(n, 1.0 / n)
    kr = np.fft.rfftfreq(n, 1.0 / n)
    kx, ky = np.meshgrid(kr, k)
    k2 = kx**2 + ky**2
    k2i = np.where(k2 > 0, 1.0 / np.maximum(k2, 1e-30), 0.0)
    return kx, ky, k2i


def e2_physical(w: np.ndarray, a: np.ndarray, n: int) -> dict[str, np.ndarray]:
    """Physical fields (float64, ``[..., x, y]`` layout) from ω̂ and â (``[..., ky, kx]`` layout).

    Conventions of ``mhd2d.py``: ψ̂ = ω̂/k², u = (∂yψ, −∂xψ), B = (∂y a, −∂x a), j = −Δa. The physical
    arrays from ``irfft2`` are indexed ``[y, x]``; they are transposed to ``[x, y]`` (The Well convention:
    axes in the order of ``dimensions@spatial_dims``).
    """
    kx, ky, k2i = _e2_wavenumbers(n)
    k2 = kx**2 + ky**2
    w = np.asarray(w, dtype=np.complex128)
    a = np.asarray(a, dtype=np.complex128)
    psi = w * k2i

    def phys(fh: np.ndarray) -> np.ndarray:
        return np.swapaxes(np.fft.irfft2(fh, s=(n, n)), -1, -2)

    return {
        "velocity": np.stack([phys(1j * ky * psi), phys(-1j * kx * psi)], axis=-1),
        "magnetic_field": np.stack([phys(1j * ky * a), phys(-1j * kx * a)], axis=-1),
        "vorticity": phys(w),
        "magnetic_potential": phys(a),
        "current": phys(k2 * a),
    }


def _max_div(v: np.ndarray, lengths: Sequence[float]) -> np.ndarray:
    """max |∇·v| per snapshot (spectral derivatives); v of shape ``(B, T, nx, ny, 2)``."""
    nx, ny = v.shape[2:4]
    kx = 2 * np.pi / lengths[0] * np.fft.fftfreq(nx, 1.0 / nx)[:, None]
    ky = 2 * np.pi / lengths[1] * np.fft.rfftfreq(ny, 1.0 / ny)[None, :]
    vh = np.fft.rfftn(v.astype(np.float64), axes=(2, 3))
    div = np.fft.irfftn(1j * kx * vh[..., 0] + 1j * ky * vh[..., 1], s=(nx, ny), axes=(2, 3))
    return np.abs(div).max(axis=(2, 3))


def _e2_meta(src_dir: Path) -> dict[str, Any]:
    meta = dict(E2_DEFAULTS)
    path = src_dir / "meta.json"
    if path.is_file():
        meta.update(json.loads(path.read_text(encoding="utf-8")))
    return meta


def _e2_seed(meta: Mapping[str, Any], eta: float, split: str) -> int | None:
    """Seed of e2_data.py: 100 + i (train) or 200 + i (ref), i = rank of η in eta_train + eta_test."""
    etas = list(meta.get("eta_train", [])) + list(meta.get("eta_test", []))
    for i, e in enumerate(etas):
        if abs(e - eta) <= 1e-9 * abs(eta):
            return (100 if split == "train" else 200) + i
    return None


def _existing_uuid(path: Path) -> str | None:
    try:
        with h5py.File(path, "r") as f:
            v = f.attrs.get("milady_uuid")
        return mff._py(v) if v is not None else None
    except OSError:
        return None


def convert_e2_file(
    npz: str | os.PathLike[str],
    out: str | os.PathLike[str],
    *,
    meta: Mapping[str, Any] | None = None,
    sim_id: str | None = None,
    max_members: int | None = None,
    max_snapshots: int | None = None,
) -> dict[str, Any]:
    """Convert an E2 ``eta_<η>_<split>.npz`` file into an MFF file; returns a summary.

    The summary contains ``path``, ``sha256``, ``size_bytes``, ``uuid``, ``eta``, ``split``, ``params``,
    ``grid``, ``n_t``, ``t_start``, ``t_end`` and ``diagnostics_mean`` (series averaged over the trajectories,
    for the catalog). ``max_members`` / ``max_snapshots`` shrink the file (quick tests).
    """
    npz = Path(npz)
    meta = dict(meta) if meta is not None else _e2_meta(npz.parent)
    m = _E2_NAME.search(npz.name)
    split = m.group("split") if m else "unknown"
    with np.load(npz) as d:
        w, a = d["w"], d["a"]
        eta = float(d["eta"]) if "eta" in d else float(m.group("eta")) if m else float("nan")
        inj_u = float(d["inj_u"]) if "inj_u" in d else float("nan")
        inj_b = float(d["inj_b"]) if "inj_b" in d else float("nan")
    n = int(meta["N"])
    members = int(meta.get("membres", 16))
    if w.shape[0] % members:
        raise ValueError(f"{npz.name}: {w.shape[0]} snapshots not divisible by {members} members")
    n_snap = w.shape[0] // members
    # Layout of e2_data.py: index = member × n_snap + snapshot ("grouped by member").
    w = w.reshape(members, n_snap, n, n // 2 + 1)
    a = a.reshape(members, n_snap, n, n // 2 + 1)
    if max_members:
        w, a = w[:max_members], a[:max_members]
    if max_snapshots:
        w, a = w[:, :max_snapshots], a[:, :max_snapshots]
    n_traj, n_t = w.shape[:2]

    phys = e2_physical(w, a, n)
    x = 2 * np.pi * np.arange(n) / n
    t_burn, every = float(meta.get("t_burn", 30.0)), float(meta.get("intervalle", 1.0))
    time = t_burn + every * np.arange(1, n_t + 1)
    nu, alpha = float(meta["nu"]), float(meta["alpha"])
    kf = list(meta.get("kf", [2.0, 3.0]))
    eps = float(meta.get("eps", 0.05))
    params = {
        "nu": nu,
        "eta": eta,
        "Pm": nu / eta,
        "alpha": alpha,
        "eps_u": eps,
        "eps_b": eps,
        "kf_min": float(kf[0]),
        "kf_max": float(kf[1]),
    }

    u, b = phys["velocity"], phys["magnetic_field"]
    eu = 0.5 * np.mean(np.sum(u**2, -1), axis=(2, 3))
    eb = 0.5 * np.mean(np.sum(b**2, -1), axis=(2, 3))
    zw = np.mean(phys["vorticity"] ** 2, axis=(2, 3))
    jj = np.mean(phys["current"] ** 2, axis=(2, 3))
    diagnostics = {
        "kinetic_energy": eu,
        "magnetic_energy": eb,
        "enstrophy": zw,
        "mean_square_current": jj,
        "dissipation": nu * zw + eta * jj + 2 * alpha * (eu + eb),
        "cross_helicity": np.mean(np.sum(u * b, -1), axis=(2, 3)),
        "max_div_b": _max_div(b.astype(np.float32), [2 * np.pi, 2 * np.pi]),
    }
    spectral = {
        "vorticity": {
            "data": np.fft.rfftn(phys["vorticity"], axes=(2, 3)),
            "physical_field": "",
            "kmax": int(meta.get("kmax", n // 3)),
            "description": "ω = ∂x u_y − ∂y u_x = −Δψ ; u = (∂yψ, −∂xψ) ; state of the mhd2d.py solver",
        },
        "magnetic_potential": {
            "data": np.fft.rfftn(phys["magnetic_potential"], axes=(2, 3)),
            "physical_field": "",
            "kmax": int(meta.get("kmax", n // 3)),
            "description": "a (out-of-plane vector potential, A = a ẑ) ; B = (∂y a, −∂x a) = ∇×A",
        },
    }
    seed = _e2_seed(meta, eta, split)
    sim_id = sim_id or str(_uuid.uuid4())
    file_meta = {
        "uuid": sim_id,
        "code": "mhd2d_numpy",
        "code_version": "experiments/mhd2d.py",
        "git_commit": git_commit(),
        "nondimensionalization": E2_NONDIM,
        "split": split,
        "seed": -1 if seed is None else seed,
        "source": npz.name,
        "source_sha256": mff.sha256_file(npz),
        "solver": {
            "scheme": "pseudo-spectral, 2/3 dealiasing, integrating-factor RK4 + Euler–Maruyama",
            "dt": float(meta.get("dt", 1e-2)),
            "t_burn": t_burn,
            "sampling_interval": every,
            "members": members,
        },
        "experiment": "E2",
    }
    out = Path(out)
    digest = mff.write_mff(
        out,
        {"velocity": u, "magnetic_field": b},
        {"time": time, "x": x, "y": x},
        params,
        meta=file_meta,
        scalars={"injection_rate_u": inj_u, "injection_rate_b": inj_b},
        diagnostics=diagnostics,
        spectral=spectral,
        dataset_name="milady_e2_mhd2d",
    )
    return {
        "path": str(out),
        "sha256": digest,
        "size_bytes": out.stat().st_size,
        "uuid": sim_id,
        "eta": eta,
        "split": split,
        "params": params,
        "grid": mff.grid_info(out),
        "n_t": int(n_t),
        "t_start": float(time[0]),
        "t_end": float(time[-1]),
        "time": time,
        "diagnostics_mean": {k: v.mean(axis=0) for k, v in diagnostics.items()},
    }


def convert_e2(
    src_dir: str | os.PathLike[str],
    out_dir: str | os.PathLike[str],
    *,
    catalog: Any = None,
    campaign: str = "e2_mhd2d",
    store: str | None = None,
    pattern: str = "eta_*.npz",
    limit: int | None = None,
    max_members: int | None = None,
    max_snapshots: int | None = None,
    overwrite: bool = False,
    verbose: bool = True,
) -> list[dict[str, Any]]:
    """Convert all ``eta_*.npz`` files of ``src_dir`` into ``out_dir`` (idempotent).

    - a file that is already converted and valid is kept (its identifier is reused) unless ``overwrite``;
    - ``catalog`` (instance of :class:`milady.catalog.api.Catalog`): registers campaign, simulations,
      files, mean diagnostics and, if the whole collection is converted without reduction, the dataset
      ``e2_mhd2d`` v1.0 (train → train, ref → test);
    - ``store``: storage URI (``s3://milady-data``…) where to copy the files following the convention
      ``{store}/{campaign}/{uuid}/fields.h5``; otherwise the registered URI is the local file.
    """
    src_dir, out_dir = Path(src_dir), Path(out_dir)
    files = sorted(src_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"no file {pattern} in {src_dir}")
    reduced = bool(limit or max_members or max_snapshots)
    if limit:
        files = files[:limit]
    meta = _e2_meta(src_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    camp_id = None
    if catalog is not None:
        import yaml

        camp_id = catalog.create_campaign(
            campaign,
            config_yaml=yaml.safe_dump(
                {"source": "experiments/e2_data.py", "meta": meta}, allow_unicode=True, sort_keys=False
            ),
            description="E2: forced 2D MHD, range of magnetic diffusivities η (ν = 8e-3 fixed), 32² grid.",
        )
    records = []
    for npz in files:
        m = _E2_NAME.search(npz.name)
        stem = f"e2_eta{m.group('eta')}_{m.group('split')}" if m else npz.stem
        out = out_dir / f"{stem}.h5"
        t0 = _time.time()
        sim_id = _existing_uuid(out) if out.is_file() else None
        reuse = out.is_file() and not overwrite and sim_id is not None and not mff.validate(out)
        if catalog is not None and sim_id is None:
            sim_id = str(_uuid.uuid4())
        if reuse:
            rec = {
                "path": str(out),
                "sha256": mff.sha256_file(out),
                "size_bytes": out.stat().st_size,
                "uuid": sim_id,
                "split": m.group("split") if m else "unknown",
                "reused": True,
            }
            if verbose:
                print(f"{npz.name}: already converted ({out.name})", flush=True)
        else:
            if catalog is not None and catalog.get_simulation(sim_id) is None:
                catalog.register_simulation(
                    camp_id,
                    "mhd2d_numpy",
                    {},
                    {},
                    code_version="experiments/mhd2d.py",
                    git_commit=git_commit(),
                    host=socket.gethostname(),
                    n_cpus=1,
                    sim_id=sim_id,
                    status="running",
                )
            rec = convert_e2_file(
                npz, out, meta=meta, sim_id=sim_id, max_members=max_members, max_snapshots=max_snapshots
            )
            if verbose:
                print(
                    f"{npz.name} → {out.name}: {rec['size_bytes'] / 2**20:.1f} MiB, "
                    f"{_time.time() - t0:.1f} s",
                    flush=True,
                )
        uri = out.resolve().as_uri()
        if store:
            uri = storage.simulation_uri(campaign, rec["uuid"], "fields", ".h5", base=store)
            storage.put(out, uri)
        rec["uri"] = uri
        if catalog is not None:
            if not rec.get("reused"):
                catalog.update_simulation(
                    rec["uuid"],
                    parameters=rec["params"],
                    grid=rec["grid"],
                    status="done",
                    wall_time_s=_time.time() - t0,
                )
            rec["file_id"] = (
                catalog.ingest_mff(uri, campaign=campaign)["file_id"]
                if rec.get("reused")
                else catalog.register_file(
                    rec["uuid"],
                    "fields",
                    uri,
                    rec["sha256"],
                    rec["size_bytes"],
                    n_t=rec["n_t"],
                    t_start=rec["t_start"],
                    t_end=rec["t_end"],
                )
            )
            if not rec.get("reused"):
                for name, series in rec["diagnostics_mean"].items():
                    catalog.add_diagnostics(rec["uuid"], name, rec["time"], series)
        records.append(rec)
    if catalog is not None and not reduced:
        split_map = {"train": "train", "ref": "test"}
        members = [(r["file_id"], split_map.get(r["split"], "test")) for r in records]
        file_ids = [fid for fid, _ in members]
        if all(isinstance(fid, str) for fid in file_ids):
            catalog.register_dataset(
                "e2_mhd2d",
                "1.0",
                members,
                description="E2: 2D MHD snapshots 32²; train = training η, "
                "test = reference trajectories (training η and test η).",
            )
    for r in records:  # no arrays in the return value
        r.pop("time", None)
        r.pop("diagnostics_mean", None)
    return records


# =============================================================================================
# Extension SFEMaNS : grid_type = "fourier_fe_axisym"
# =============================================================================================
AZIMUTHAL_CONVENTION = (
    "f(r, θ, z) = Σ_m [ f_m^c(r, z) cos(mθ) + f_m^s(r, z) sin(mθ) ] ; index 0 = cos, 1 = sin"
)


def write_fourier_fe_mff(
    path: str | os.PathLike[str],
    meshes: Mapping[str, Mapping[str, Any]],
    modes: Sequence[int],
    fields: Mapping[str, Mapping[str, Any]],
    time: Sequence[float],
    params: Mapping[str, Any],
    *,
    meta: Mapping[str, Any] | None = None,
    dataset_name: str = "milady_sfemans",
    compression: str | None = "gzip",
    compression_level: int = 4,
) -> str:
    """Write "azimuthal Fourier × meridian finite elements" fields (SFEMaNS) in MFF format; returns the SHA-256.

    meshes: ``{name: {"nodes": (n, 2) [r, z], "connectivity": (n_elem, 3|6) 0-based indices, "element_type": "P1"|"P2",
             "vertices": (n_v,) optional, "boundary_nodes": (n_b,) optional, "region": (n_elem,) optional}}``.
             SFEMaNS uses distinct meshes (fluid, conductor, vacuum): one name per mesh.
    modes: azimuthal wavenumbers m (integers ≥ 0, ``len = M``).
    fields: ``{name: {"data": (n_traj, n_t, M, 2, n_nodes[, 3]), "mesh": name, "node_set": "all"|"vertices"}}``;
             axis 3 = (cos, sin); last axis of vectors = cylindrical components (r, θ, z).
    """
    path = Path(storage.local_path(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    modes = np.asarray(modes, dtype=np.int32)
    M = len(modes)
    time = np.asarray(time, dtype=np.float64)
    n_traj = None
    for name, spec in fields.items():
        data = np.asarray(spec["data"])
        if n_traj is None:
            n_traj = data.shape[0]
        if data.shape[:4] != (n_traj, len(time), M, 2):
            raise ValueError(
                f"{name}: shape {data.shape}, expected ({n_traj}, {len(time)}, {M}, 2, n_nodes[, 3])"
            )
        if spec["mesh"] not in meshes:
            raise ValueError(f"{name}: unknown mesh {spec['mesh']!r}")
    if n_traj is None:
        raise ValueError("at least one field is required")
    tmp = path.with_name(f".{path.name}.{_uuid.uuid4().hex[:8]}.part")
    try:
        with h5py.File(tmp, "w") as f:
            numeric = {k: float(v) for k, v in params.items() if mff._is_number(v)}
            mff._set_attr(f, "simulation_parameters", list(numeric))
            for k, v in numeric.items():
                f.attrs[k] = v
            f.attrs["dataset_name"] = dataset_name
            f.attrs["grid_type"] = "fourier_fe_axisym"
            f.attrs["n_spatial_dims"] = 3
            f.attrs["n_trajectories"] = int(n_traj)
            for k, v in mff._milady_attrs(meta, params).items():
                f.attrs[k] = v
            g = f.create_group("dimensions")
            mff._set_attr(g, "spatial_dims", ["r", "theta", "z"])
            ds = g.create_dataset("time", data=time.astype(np.float32))
            ds.attrs["sample_varying"] = False
            g = f.create_group("boundary_conditions")
            g.attrs["milady_note"] = (
                "unstructured mesh: boundary nodes in milady_fourier_fe/meshes/*/boundary_nodes"
            )
            g = f.create_group("scalars")
            for k, v in numeric.items():
                ds = g.create_dataset(k, data=np.float32(v))
                ds.attrs["sample_varying"] = False
                ds.attrs["time_varying"] = False
            mff._set_attr(g, "field_names", list(numeric))
            for group in mff.TENSOR_GROUPS:
                mff._set_attr(f.create_group(group), "field_names", [])
            fe = f.create_group("milady_fourier_fe")
            mff._set_attr(fe, "field_names", list(fields))
            fe.attrs["azimuthal_convention"] = AZIMUTHAL_CONVENTION
            fe.attrs["component_basis"] = "cylindrical"
            fe.attrs["n_modes"] = M
            fe.create_dataset("modes", data=modes)
            gm = fe.create_group("meshes")
            for name, spec in meshes.items():
                mg = gm.create_group(name)
                nodes = np.asarray(spec["nodes"], dtype=np.float64)
                conn = np.asarray(spec["connectivity"], dtype=np.int32)
                mg.attrs["element_type"] = str(spec.get("element_type", "P1"))
                mg.attrs["n_nodes"] = int(nodes.shape[0])
                mg.attrs["n_elements"] = int(conn.shape[0])
                mg.create_dataset("nodes", data=nodes)
                mg.create_dataset("connectivity", data=conn)
                for opt in ("vertices", "boundary_nodes", "region"):
                    if spec.get(opt) is not None:
                        mg.create_dataset(opt, data=np.asarray(spec[opt], dtype=np.int32))
            gf = fe.create_group("fields")
            for name, spec in fields.items():
                data = np.asarray(spec["data"])
                ds = mff._create(gf, name, data, np.float32, compression, compression_level, lead=3)
                ds.attrs["mesh"] = str(spec["mesh"])
                ds.attrs["node_set"] = str(spec.get("node_set", "all"))
                ds.attrs["tensor_order"] = 1 if data.ndim == 6 else 0
                ds.attrs["sample_varying"] = True
                ds.attrs["time_varying"] = True
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return mff.sha256_file(path)


def _fe_eval(
    path: str | os.PathLike[str],
    field: str,
    r: np.ndarray,
    z: np.ndarray,
    theta: np.ndarray,
    *,
    traj: int,
    t: int,
) -> np.ndarray:
    """Evaluate a Fourier–FE field at points (r, θ, z) (arrays of the same shape); cylindrical components.

    Piecewise linear interpolation on a Delaunay triangulation of the nodes (exact for fields
    affine in (r, z); order-2 approximation for P2 elements); NaN outside the meridian domain.
    """
    from scipy.interpolate import LinearNDInterpolator

    with mff.open_mff(path) as f:
        fe = f["milady_fourier_fe"]
        node = fe["fields"][field]
        mesh = fe["meshes"][mff._py(node.attrs["mesh"])]
        nodes = np.asarray(mesh["nodes"][()])
        if mff._py(node.attrs.get("node_set", "all")) == "vertices":
            nodes = nodes[np.asarray(mesh["vertices"][()])]
        modes = np.asarray(fe["modes"][()])
        vals = np.asarray(node[traj, t], dtype=np.float64)  # (M, 2, n[, 3])
    M = len(modes)
    comps = vals.shape[3] if vals.ndim == 4 else 1
    table = np.moveaxis(vals.reshape(M, 2, nodes.shape[0], comps), 2, 0).reshape(nodes.shape[0], -1)
    pts = np.stack([np.ravel(r), np.ravel(z)], axis=-1)
    coef = LinearNDInterpolator(nodes, table)(pts).reshape(-1, M, 2, comps)
    th = np.ravel(theta)[:, None]
    basis_c, basis_s = np.cos(modes[None, :] * th), np.sin(modes[None, :] * th)
    out = np.einsum("pmc,pm->pc", coef[:, :, 0], basis_c) + np.einsum("pmc,pm->pc", coef[:, :, 1], basis_s)
    out = out.reshape(*np.shape(r), comps)
    return out[..., 0] if vals.ndim == 3 else out


def fourier_fe_to_grid(
    path: str | os.PathLike[str],
    field: str,
    r: Sequence[float],
    theta: Sequence[float],
    z: Sequence[float],
    *,
    traj: int = 0,
    t: int = 0,
) -> np.ndarray:
    """Interpolate a Fourier–FE field onto a regular cylindrical grid ``(nr, nθ, nz[, 3])`` (components r, θ, z)."""
    R, TH, Z = np.meshgrid(
        np.asarray(r, float), np.asarray(theta, float), np.asarray(z, float), indexing="ij"
    )
    return _fe_eval(path, field, R, Z, TH, traj=traj, t=t)


def fourier_fe_to_cartesian(
    path: str | os.PathLike[str],
    field: str,
    x: Sequence[float],
    y: Sequence[float],
    z: Sequence[float],
    *,
    traj: int = 0,
    t: int = 0,
) -> np.ndarray:
    """Interpolate a Fourier–FE field onto a Cartesian grid ``(nx, ny, nz[, 3])`` (components x, y, z; NaN outside the domain)."""
    X, Y, Z = np.meshgrid(np.asarray(x, float), np.asarray(y, float), np.asarray(z, float), indexing="ij")
    R, TH = np.hypot(X, Y), np.arctan2(Y, X)
    out = _fe_eval(path, field, R, Z, TH, traj=traj, t=t)
    if out.ndim == 4:
        ur, ut, uz = out[..., 0], out[..., 1], out[..., 2]
        c, s = np.cos(TH), np.sin(TH)
        out = np.stack([ur * c - ut * s, ur * s + ut * c, uz], axis=-1)
    return out


def read_sfemans_native(*_: Any, **__: Any) -> None:
    """Reading of native SFEMaNS files (Fortran "suites"): not implemented.

    SFEMaNS data are not public; when they become accessible, this reader will have to produce
    the arrays expected by :func:`write_fourier_fe_mff` (meshes per domain, modes, cos/sin
    coefficients per node) without interpolation. See ``docs/specs/data-format.md``, SFEMaNS section.
    """
    raise NotImplementedError(
        "native SFEMaNS reader to be written when the data become available "
        "(see docs/specs/data-format.md); use write_fourier_fe_mff with arrays"
    )


# =============================================================================================
# Command line
# =============================================================================================
def main(argv: Sequence[str] | None = None) -> int:
    """Entry point of ``python -m milady.data.convert``."""
    ap = argparse.ArgumentParser(prog="python -m milady.data.convert", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("e2", help="convert the E2 .npz files into MFF files")
    p.add_argument("source", help="folder of eta_*.npz (and meta.json)")
    p.add_argument("sortie", help="output folder for the .h5 files")
    p.add_argument("--pattern", default="eta_*.npz")
    p.add_argument("--limit", type=int, default=None, help="maximum number of files")
    p.add_argument("--max-members", type=int, default=None, help="trajectories kept per file")
    p.add_argument("--max-snapshots", type=int, default=None, help="snapshots kept per trajectory")
    p.add_argument(
        "--catalog",
        nargs="?",
        const="",
        default=None,
        help="register in the catalog (SQLAlchemy URL; without value: MILADY_DB_URL or default SQLite)",
    )
    p.add_argument("--campaign", default="e2_mhd2d")
    p.add_argument(
        "--store", default=None, help="storage URI where to copy the files (e.g. s3://milady-data)"
    )
    p.add_argument("--overwrite", action="store_true")
    p = sub.add_parser("validate", help="validate MFF files")
    p.add_argument("files", nargs="+")
    p.add_argument("--well-only", action="store_true", help="check only the The Well part")
    p.add_argument(
        "--full",
        action="store_true",
        help="finite values checked on all snapshots (full read)",
    )
    p = sub.add_parser("info", help="display the tree of a file (like h5dump -H)")
    p.add_argument("file")
    p = sub.add_parser("zarr", help="copy an HDF5 MFF file to Zarr (local or s3://)")
    p.add_argument("h5")
    p.add_argument("uri")
    p.add_argument("--overwrite", action="store_true")
    p = sub.add_parser("sfemans", help="(skeleton) conversion of native SFEMaNS data")
    p.add_argument("source")
    p.add_argument("sortie")
    args = ap.parse_args(argv)

    if args.cmd == "e2":
        catalog = None
        if args.catalog is not None:
            from milady.catalog.api import Catalog

            catalog = Catalog(args.catalog or None)
        recs = convert_e2(
            args.source,
            args.sortie,
            catalog=catalog,
            campaign=args.campaign,
            store=args.store,
            pattern=args.pattern,
            limit=args.limit,
            max_members=args.max_members,
            max_snapshots=args.max_snapshots,
            overwrite=args.overwrite,
        )
        print(json.dumps([{k: r.get(k) for k in ("uri", "uuid", "split", "sha256")} for r in recs], indent=1))
        return 0
    if args.cmd == "validate":
        bad = 0
        for path in args.files:
            errs = mff.validate(path, well_only=args.well_only, full_scan=args.full)
            print(f"{path}: {'valid' if not errs else f'{len(errs)} problem(s)'}")
            for e in errs:
                print(f"  - {e}")
            bad += bool(errs)
        return 1 if bad else 0
    if args.cmd == "info":
        print(mff.describe(args.file))
        return 0
    if args.cmd == "zarr":
        print(mff.to_zarr(args.h5, args.uri, overwrite=args.overwrite))
        return 0
    if args.cmd == "sfemans":
        try:
            read_sfemans_native(args.source, args.sortie)
        except NotImplementedError as exc:
            print(f"not implemented: {exc}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
