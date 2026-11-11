"""MilaDy "MFF" (MilaDy Field Format) data format, version 1.0.

One file = one simulation (one or more trajectories with the same parameters). The hierarchy follows
exactly the HDF5 format of The Well (PolymathicAI/the_well, ``docs/data_format.md``):

- root attributes ``dataset_name``, ``grid_type``, ``n_spatial_dims``, ``n_trajectories``,
  ``simulation_parameters`` and one attribute per parameter;
- groups ``dimensions/`` (``time``, ``x``, ``y``, ``z``), ``boundary_conditions/``, ``scalars/``,
  ``t0_fields/`` (scalars), ``t1_fields/`` (vectors), ``t2_fields/`` (tensors) with their attributes
  (``field_names``, ``dim_varying``, ``sample_varying``, ``time_varying``…);
- float32 fields, of shape ``(n_trajectories, n_t, nx, ny[, nz][, D[, D]])`` (D = n_spatial_dims).

On top of this come ``milady_*`` root attributes (provenance, parameters as JSON, catalog identifier)
and two optional groups: ``milady_diagnostics/`` (time series) and
``milady_spectral/`` (``numpy.fft.rfftn`` coefficients of the fields, periodic domains).
The Zarr variant (chunked reading from S3) has the same hierarchy: :func:`to_zarr`, then
:func:`read_mff` / :func:`validate` on a URI ending in ``.zarr``.

Readable specification: ``docs/specs/data-format.md``; metadata schema: ``schema.json``.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import hashlib
import json
import math
import os
import re
import shlex
import socket
import sys
import tempfile
import uuid as _uuid
from collections.abc import Iterator, Mapping, Sequence
from functools import lru_cache
from pathlib import Path
from typing import Any

import h5py
import numpy as np

from milady import git_commit as _git_commit
from milady import storage

__all__ = [
    "BC_TYPES",
    "FORMAT_VERSION",
    "GRID_TYPES",
    "STANDARD_FIELDS",
    "TENSOR_GROUPS",
    "WELL_GROUPS",
    "describe",
    "grid_info",
    "load_schema",
    "open_mff",
    "read_mff",
    "sha256_file",
    "to_zarr",
    "validate",
    "write_mff",
]

FORMAT_VERSION = "1.0"
WELL_GROUPS = ("dimensions", "boundary_conditions", "scalars", "t0_fields", "t1_fields", "t2_fields")
TENSOR_GROUPS = ("t0_fields", "t1_fields", "t2_fields")
GRID_TYPES = ("cartesian", "spherical", "fourier_fe_axisym")
BC_TYPES = ("periodic", "wall", "open")
#: Standard MilaDy fields and expected group.
STANDARD_FIELDS = {
    "velocity": "t1_fields",  # u
    "magnetic_field": "t1_fields",  # B, in Alfvén units (same unit as u)
    "vector_potential": "t1_fields",  # A, B = ∇×A
    "pressure": "t0_fields",
}
#: Root attributes reserved by The Well: forbidden as parameter names.
_WELL_ROOT_ATTRS = ("dataset_name", "grid_type", "n_spatial_dims", "n_trajectories", "simulation_parameters")
_MAX_CHUNK_BYTES = 32 * 2**20
SCHEMA_PATH = Path(__file__).with_name("schema.json")


# =============================================================================================
# Tools
# =============================================================================================
@lru_cache(maxsize=1)
def load_schema() -> dict[str, Any]:
    """JSON schema of the metadata (``src/milady/data/schema.json``)."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _py(v: Any) -> Any:
    """Convert an HDF5/Zarr attribute value (numpy, bytes) into a native Python object (JSON types)."""
    if isinstance(v, bytes):
        return v.decode("utf-8")
    if isinstance(v, np.ndarray):
        return _py(v.item()) if v.ndim == 0 else [_py(x) for x in v.tolist()]
    if isinstance(v, np.generic):
        return _py(v.item())
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    return v


def _str_list(v: Any) -> list[str]:
    """List of strings from an attribute (The Well sometimes stores a single string: ``'x'``)."""
    v = _py(v)
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    return [str(x) for x in v]


def _attrs(node: Any) -> dict[str, Any]:
    return {k: _py(v) for k, v in node.attrs.items()}


def _jsonable(obj: Any) -> Any:
    """JSON-serializable object (numpy types converted, NaN/inf → None)."""
    if isinstance(obj, Mapping):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, np.ndarray)):
        return [_jsonable(x) for x in (obj.tolist() if isinstance(obj, np.ndarray) else obj)]
    if isinstance(obj, np.generic):
        obj = obj.item()
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, (bool, np.bool_))


def _is_zarr(path: str | os.PathLike[str]) -> bool:
    return os.fspath(path).rstrip("/").endswith(".zarr")


def _is_group(node: Any) -> bool:
    if isinstance(node, h5py.Group):
        return True
    try:
        import zarr
    except ImportError:  # pragma: no cover
        return False
    return isinstance(node, zarr.Group)


def _members(group: Any) -> list[str]:
    return sorted(group.keys())


def _set_attr(node: Any, key: str, value: Any) -> None:
    """Write an HDF5 attribute (lists of strings as variable-length UTF-8 strings, even when empty)."""
    if isinstance(value, (list, tuple)) and all(isinstance(x, str) for x in value):
        node.attrs.create(key, np.array(list(value), dtype=h5py.string_dtype()))
    elif isinstance(value, (list, tuple)):
        node.attrs[key] = np.asarray(value)
    else:
        node.attrs[key] = value


def sha256_file(path: str | os.PathLike[str]) -> str:
    """SHA-256 sum of a local file, read in 8 MiB blocks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8 * 2**20):
            h.update(chunk)
    return h.hexdigest()


def _chunks(shape: tuple[int, ...], itemsize: int, lead: int = 2) -> tuple[int, ...]:
    """Blocks ``(1, 1, *spatial, *components)``; if a block exceeds 32 MiB (3D ≥ 160³ × 3), the x axis is split."""
    chunks = [1] * lead + list(shape[lead:])
    while lead < len(chunks) and math.prod(chunks) * itemsize > _MAX_CHUNK_BYTES and chunks[lead] > 1:
        chunks[lead] = math.ceil(chunks[lead] / 2)
    return tuple(max(1, c) for c in chunks)


def _create(
    group: h5py.Group,
    name: str,
    data: np.ndarray,
    dtype: Any,
    compression: str | None,
    level: int,
    lead: int = 2,
) -> h5py.Dataset:
    data = np.asarray(data)
    kw: dict[str, Any] = {}
    if data.ndim > lead and data.size > 0:
        kw["chunks"] = _chunks(data.shape, np.dtype(dtype).itemsize, lead)
        if compression:
            kw["compression"] = compression
            kw["shuffle"] = True
            if compression == "gzip":
                kw["compression_opts"] = level
    return group.create_dataset(name, data=data.astype(dtype, copy=False), **kw)


# =============================================================================================
# Opening (local or remote HDF5, local or remote Zarr)
# =============================================================================================
def _open_zarr(uri: str, mode: str = "r") -> Any:
    import zarr

    if storage.is_local(uri):
        return zarr.open_group(str(storage.local_path(uri)), mode=mode)
    proto, path = storage.split_uri(uri)
    return zarr.open_group(f"{proto}://{path}", mode=mode, storage_options=storage.storage_options(uri))


@contextlib.contextmanager
def open_mff(path: str | os.PathLike[str], mode: str = "r") -> Iterator[Any]:
    """Open an MFF file and return the root group (context manager).

    - local ``*.h5``: ``h5py.File``; ``s3://…/*.h5``: ``h5py.File`` on an fsspec object read in blocks
      (read-only);
    - ``*.zarr`` (local or ``s3://``): ``zarr.Group``, with the same read interface (``f["t1_fields"]
      ["velocity"][0, :5]``, ``.attrs``).
    """
    p = os.fspath(path)
    if _is_zarr(p):
        yield _open_zarr(p, mode)
        return
    if storage.is_local(p):
        with h5py.File(storage.local_path(p), mode) as f:
            yield f
        return
    if mode != "r":
        raise ValueError(
            "a remote HDF5 file is opened read-only; write locally, then storage.put"
        )
    with (
        storage.open(p, "rb", block_size=8 * 2**20, cache_type="blockcache") as fobj,
        h5py.File(fobj, "r") as f,
    ):
        yield f


# =============================================================================================
# Writing
# =============================================================================================
def _infer_flags(shape: tuple[int, ...], n_traj: int, n_t: int, what: str) -> tuple[bool, bool]:
    """(sample_varying, time_varying) of a scalar series according to its shape."""
    if shape in ((), (1,)):
        return False, False
    if shape == (n_traj, n_t):
        return True, True
    if shape == (n_t,):
        return False, True
    if shape == (n_traj,):
        return True, False
    raise ValueError(f"{what}: shape {shape} incompatible with (n_traj={n_traj}, n_t={n_t})")


def _domain_lengths(coords: Mapping[str, np.ndarray], dims: Sequence[str]) -> list[float]:
    out = []
    for d in dims:
        c = np.asarray(coords[d], dtype=np.float64)
        out.append(float(len(c) * np.mean(np.diff(c))) if len(c) > 1 else 1.0)
    return out


def _split_key(key: str) -> tuple[str | None, str]:
    if "/" in key:
        grp, name = key.split("/", 1)
        if grp not in TENSOR_GROUPS:
            raise ValueError(f"unknown field group: {grp!r} (expected: {TENSOR_GROUPS})")
        return grp, name
    return None, key


def _boundary_specs(
    boundary: Mapping[str, Any] | None, dims: Sequence[str], sizes: Sequence[int]
) -> dict[str, dict[str, Any]]:
    """Normalize ``boundary`` into {group_name: specification}.

    Accepted forms: ``None`` (periodic in all directions, the MilaDy case); ``{"x": "periodic",
    "y": "wall"}``; or ``{"name": {"associated_dims": [...], "bc_type": ..., "mask": ..., "values": ...,
    "associated_fields": [...]}}``.
    """
    size_of = dict(zip(dims, sizes))
    if boundary is None:
        boundary = {d: "periodic" for d in dims}
    specs: dict[str, dict[str, Any]] = {}
    for key, val in boundary.items():
        if isinstance(val, str):
            if key not in size_of:
                raise ValueError(f"boundary condition on an unknown dimension: {key!r}")
            bc = val.lower()
            mask = np.zeros(size_of[key], dtype=bool)
            mask[0] = mask[-1] = (
                True  # The Well: true where the boundary is defined (first and last point)
            )
            specs[f"{key}_{bc}"] = {
                "associated_dims": [key],
                "associated_fields": [],
                "bc_type": bc,
                "mask": mask,
                "values": None,
                "sample_varying": False,
                "time_varying": False,
            }
        else:
            spec = dict(val)
            assoc = _str_list(spec.get("associated_dims", [key]))
            bc = str(spec["bc_type"]).lower()
            shape = tuple(size_of[d] for d in assoc)
            mask = np.asarray(spec.get("mask", np.ones(shape, bool)), dtype=bool)
            specs[key] = {
                "associated_dims": assoc,
                "associated_fields": _str_list(spec.get("associated_fields", [])),
                "bc_type": bc,
                "mask": mask,
                "values": spec.get("values"),
                "sample_varying": bool(spec.get("sample_varying", False)),
                "time_varying": bool(spec.get("time_varying", False)),
            }
    for name, spec in specs.items():
        if spec["bc_type"] not in BC_TYPES:
            raise ValueError(f"{name}: bc_type {spec['bc_type']!r} not in {BC_TYPES}")
    return specs


def _milady_attrs(meta: Mapping[str, Any] | None, params: Mapping[str, Any]) -> dict[str, Any]:
    m = dict(meta or {})
    sim_uuid = m.pop("uuid", None)
    out: dict[str, Any] = {
        "milady_format_version": FORMAT_VERSION,
        "milady_code": str(m.pop("code", None) or "unknown"),
        "milady_code_version": str(m.pop("code_version", "") or ""),
        "milady_git_commit": str(m.pop("git_commit", None) or _git_commit()),
        "milady_parameters": json.dumps(_jsonable(params), sort_keys=True, ensure_ascii=False),
        "milady_nondimensionalization": str(m.pop("nondimensionalization", "") or ""),
        "milady_created": str(m.pop("created", None) or _now_iso()),
        "milady_host": str(m.pop("host", None) or socket.gethostname()),
        "milady_command": str(m.pop("command", None) or " ".join(shlex.quote(a) for a in sys.argv)),
        "milady_uuid": str(_uuid.UUID(str(sim_uuid))) if sim_uuid else str(_uuid.uuid4()),
    }
    for key, val in m.items():
        name = key if key.startswith("milady_") else f"milady_{key}"
        if not re.fullmatch(r"milady_[A-Za-z0-9_]+", name):
            raise ValueError(f"invalid metadata key: {key!r}")
        if isinstance(val, (str, bool, np.bool_)) or _is_number(val):
            out[name] = val
        else:
            out[name] = json.dumps(_jsonable(val), sort_keys=True, ensure_ascii=False)
    return out


def write_mff(
    path: str | os.PathLike[str],
    fields: Mapping[str, Any],
    coords: Mapping[str, Any],
    params: Mapping[str, Any],
    *,
    meta: Mapping[str, Any] | None = None,
    boundary: Mapping[str, Any] | None = None,
    scalars: Mapping[str, Any] | None = None,
    diagnostics: Mapping[str, Any] | None = None,
    spectral: Mapping[str, Any] | bool | None = None,
    dataset_name: str = "milady",
    grid_type: str = "cartesian",
    compression: str | None = "gzip",
    compression_level: int = 4,
) -> str:
    """Write a simulation in MFF 1.0 format and return the SHA-256 sum of the written file.

    Parameters
    ----------
    path : local ``*.h5`` path or remote URI (``s3://bucket/…/fields.h5``: written locally then uploaded).
    fields : ``{name: array}`` of shape ``(n_traj, n_t, *spatial)`` (scalar, → ``t0_fields``),
        ``(n_traj, n_t, *spatial, D)`` (vector, → ``t1_fields``) or ``(…, D, D)`` (tensor, → ``t2_fields``),
        with D = number of spatial dimensions (3 in 3D, 2 in 2D). A name may be prefixed by its group
        (``"t1_fields/velocity"``). Standard names: ``velocity``, ``magnetic_field``, ``vector_potential``,
        ``pressure``.
    coords : ``{"time": (n_t,), "x": (nx,), "y": (ny,)[, "z": (nz,)]}``; the order of the spatial keys is
        that of the array axes.
    params : physical parameters. Numerical values become root attributes, entries of
        ``simulation_parameters`` and scalars of ``scalars/`` (The Well convention); all of them (including
        strings, lists) are in the JSON attribute ``milady_parameters``.
    meta : ``milady_*`` metadata: ``code``, ``code_version``, ``git_commit``, ``nondimensionalization``,
        ``created``, ``host``, ``command``, ``uuid`` (= identifier of the simulation in the catalog); missing
        values are filled in automatically; any other key ``k`` becomes ``milady_k``
        (JSON if it is neither a string nor a number).
    boundary : boundary conditions (default: periodic in all directions), see
        :func:`_boundary_specs`.
    scalars : additional scalar series ``{name: value}`` (shape ``()``, ``(n_t,)``, ``(n_traj,)`` or
        ``(n_traj, n_t)``) or ``{name: {"data": …, "sample_varying": …, "time_varying": …}}``.
    diagnostics : time series → ``milady_diagnostics/``; optional key ``"time"`` (own grid,
        default ``coords["time"]``); series of shape ``(n_td,)`` or ``(n_traj, n_td)``.
    spectral : ``True`` (rfftn of all fields) or ``{name: complex array}`` / ``{name: {"data": …,
        "physical_field": …, "kmax": …, "description": …}}`` → ``milady_spectral/``; shape
        ``(n_traj, n_t, nx, ny, nz//2+1[, D…])``.
    compression : ``"gzip"`` (level ``compression_level``, default 4), ``"lzf"`` or ``None``.
    """
    target = os.fspath(path)
    if _is_zarr(target):
        raise ValueError("write_mff writes HDF5; for Zarr: write_mff(...h5) then to_zarr(h5, uri)")
    if grid_type not in ("cartesian", "spherical"):
        raise ValueError("grid_type 'fourier_fe_axisym': use milady.data.convert.write_fourier_fe_mff")
    remote = not storage.is_local(target)
    if remote:
        tmpdir = tempfile.mkdtemp(prefix="milady-mff-")
        local = Path(tmpdir) / Path(storage.split_uri(target)[1]).name
    else:
        local = storage.local_path(target)
    local.parent.mkdir(parents=True, exist_ok=True)
    tmp = local.with_name(f".{local.name}.{_uuid.uuid4().hex[:8]}.part")
    try:
        with h5py.File(tmp, "w") as f:
            _write_tree(
                f,
                fields,
                coords,
                params,
                meta=meta,
                boundary=boundary,
                scalars=scalars,
                diagnostics=diagnostics,
                spectral=spectral,
                dataset_name=dataset_name,
                grid_type=grid_type,
                compression=compression,
                level=compression_level,
            )
        os.replace(tmp, local)
    finally:
        tmp.unlink(missing_ok=True)
    digest = sha256_file(local)
    if remote:
        try:
            storage.put(local, target)
        finally:
            local.unlink(missing_ok=True)
            os.rmdir(local.parent)
    return digest


def _write_tree(
    f: h5py.File,
    fields: Mapping[str, Any],
    coords: Mapping[str, Any],
    params: Mapping[str, Any],
    *,
    meta: Mapping[str, Any] | None,
    boundary: Mapping[str, Any] | None,
    scalars: Mapping[str, Any] | None,
    diagnostics: Mapping[str, Any] | None,
    spectral: Mapping[str, Any] | bool | None,
    dataset_name: str,
    grid_type: str,
    compression: str | None,
    level: int,
) -> None:
    # --- geometry ------------------------------------------------------------------------
    if "time" not in coords:
        raise ValueError("coords must contain 'time'")
    dims = [k for k in coords if k != "time"]
    if not 1 <= len(dims) <= 3:
        raise ValueError(f"1 to 3 spatial dimensions expected, got {dims}")
    D = len(dims)
    sizes = [int(np.asarray(coords[d]).shape[-1]) for d in dims]
    time = np.asarray(coords["time"], dtype=np.float64)
    if time.ndim != 1:
        raise ValueError("coords['time'] must be 1D (time shared by all trajectories)")
    if not fields:
        raise ValueError("at least one field is required")

    # --- fields: group deduced from the shape --------------------------------------------
    specs: list[tuple[str, str, np.ndarray]] = []
    n_traj = n_t = -1
    for key, arr in fields.items():
        grp, name = _split_key(key)
        a = np.asarray(arr)
        order = a.ndim - 2 - D
        if order not in (0, 1, 2):
            raise ValueError(f"{name}: shape {a.shape} incompatible with {D} spatial dimensions")
        if list(a.shape[2 : 2 + D]) != sizes:
            raise ValueError(f"{name}: spatial dimensions {a.shape[2 : 2 + D]} ≠ coords {tuple(sizes)}")
        if any(s != D for s in a.shape[2 + D :]):
            raise ValueError(
                f"{name}: {a.shape[2 + D :]} components, expected {D} per index (n_spatial_dims={D});"
                " an out-of-plane component in 2D is stored in t0_fields"
            )
        group = f"t{order}_fields"
        if grp is not None and grp != group:
            raise ValueError(f"{name}: shape of order {order} incompatible with group {grp}")
        if name in STANDARD_FIELDS and STANDARD_FIELDS[name] != group:
            raise ValueError(f"{name}: standard field expected in {STANDARD_FIELDS[name]}, not {group}")
        if not np.issubdtype(a.dtype, np.number) or np.iscomplexobj(a):
            raise ValueError(f"{name}: real values expected (complex: spectral argument)")
        if n_traj < 0:
            n_traj, n_t = a.shape[:2]
        elif a.shape[:2] != (n_traj, n_t):
            raise ValueError(f"{name}: (n_traj, n_t) = {a.shape[:2]} ≠ {(n_traj, n_t)}")
        specs.append((group, name, a))
    if n_t != len(time):
        raise ValueError(f"len(coords['time']) = {len(time)} ≠ n_t = {n_t}")

    # --- root attributes (The Well) -------------------------------------------------------
    numeric = {k: float(v) for k, v in params.items() if _is_number(v)}
    for k in params:
        if k in _WELL_ROOT_ATTRS or k.startswith("milady_") or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k):
            raise ValueError(f"reserved or invalid parameter name: {k!r}")
    _set_attr(f, "simulation_parameters", list(numeric))
    for k, v in numeric.items():
        f.attrs[k] = v
    f.attrs["dataset_name"] = dataset_name
    f.attrs["grid_type"] = grid_type
    f.attrs["n_spatial_dims"] = D
    f.attrs["n_trajectories"] = int(n_traj)
    for k, v in _milady_attrs(meta, params).items():
        f.attrs[k] = v

    # --- dimensions ----------------------------------------------------------------------
    g = f.create_group("dimensions")
    _set_attr(g, "spatial_dims", dims)
    ds = g.create_dataset("time", data=time.astype(np.float32))
    ds.attrs["sample_varying"] = False
    for d in dims:
        ds = g.create_dataset(d, data=np.asarray(coords[d], dtype=np.float32))
        ds.attrs["sample_varying"] = False
        ds.attrs["time_varying"] = False

    # --- boundary conditions -------------------------------------------------------------
    g = f.create_group("boundary_conditions")
    for name, spec in _boundary_specs(boundary, dims, sizes).items():
        sub = g.create_group(name)
        _set_attr(sub, "associated_dims", spec["associated_dims"])
        _set_attr(sub, "associated_fields", spec["associated_fields"])
        sub.attrs["bc_type"] = spec["bc_type"]
        sub.attrs["sample_varying"] = spec["sample_varying"]
        sub.attrs["time_varying"] = spec["time_varying"]
        sub.create_dataset("mask", data=spec["mask"])
        n_true = int(spec["mask"].sum())
        values = (
            np.zeros(n_true, np.float32) if spec["values"] is None else np.asarray(spec["values"], np.float32)
        )
        sub.create_dataset("values", data=values)

    # --- scalars (numerical parameters + additional series) -----------------------------
    g = f.create_group("scalars")
    names = []
    for k, v in numeric.items():
        ds = g.create_dataset(k, data=np.float32(v))
        ds.attrs["sample_varying"] = False
        ds.attrs["time_varying"] = False
        names.append(k)
    for k, v in (scalars or {}).items():
        if k in names:
            raise ValueError(f"scalar {k!r} already defined as a parameter")
        if isinstance(v, Mapping):
            data = np.asarray(v["data"], dtype=np.float32)
            sv, tv = bool(v.get("sample_varying", False)), bool(v.get("time_varying", False))
            expected = ((n_traj,) if sv else ()) + ((n_t,) if tv else ())
            if data.shape != expected and not (expected == () and data.shape == (1,)):
                raise ValueError(f"scalar {k}: shape {data.shape} ≠ {expected}")
        else:
            data = np.asarray(v, dtype=np.float32)
            sv, tv = _infer_flags(data.shape, n_traj, n_t, f"scalar {k}")
        ds = g.create_dataset(k, data=data)
        ds.attrs["sample_varying"] = sv
        ds.attrs["time_varying"] = tv
        names.append(k)
    _set_attr(g, "field_names", names)

    # --- t0/t1/t2 fields -----------------------------------------------------------------
    for order, group in enumerate(TENSOR_GROUPS):
        g = f.create_group(group)
        mine = [(name, a) for grp, name, a in specs if grp == group]
        _set_attr(g, "field_names", [name for name, _ in mine])
        for name, a in mine:
            ds = _create(g, name, a, np.float32, compression, level)
            ds.attrs["dim_varying"] = np.ones(D, dtype=bool)
            ds.attrs["sample_varying"] = True
            ds.attrs["time_varying"] = True
            if order == 2:
                at = np.swapaxes(a, -1, -2)
                scale = float(np.max(np.abs(a))) if a.size else 0.0
                ds.attrs["symmetric"] = bool(np.allclose(a, at, atol=1e-6 * scale))
                ds.attrs["antisymmetric"] = bool(np.allclose(a, -at, atol=1e-6 * scale))

    # --- diagnostics ---------------------------------------------------------------------
    if diagnostics:
        diag = dict(diagnostics)
        td = np.asarray(diag.pop("time", time), dtype=np.float64)
        g = f.create_group("milady_diagnostics")
        g.create_dataset("time", data=td)
        dnames = []
        for k, v in diag.items():
            a = np.asarray(v, dtype=np.float64)
            if a.shape == td.shape:
                sv = False
            elif a.shape == (n_traj, len(td)):
                sv = True
            else:
                raise ValueError(
                    f"diagnostic {k}: shape {a.shape}, expected {td.shape} or {(n_traj, len(td))}"
                )
            ds = g.create_dataset(k, data=a)
            ds.attrs["sample_varying"] = sv
            ds.attrs["time_varying"] = True
            dnames.append(k)
        _set_attr(g, "field_names", dnames)

    # --- spectral coefficients -----------------------------------------------------------
    if spectral:
        axes = list(range(2, 2 + D))
        if spectral is True:
            spectral = {
                name: {"data": np.fft.rfftn(np.asarray(a, np.float64), axes=axes), "physical_field": name}
                for _, name, a in specs
            }
        kshape = sizes[:-1] + [sizes[-1] // 2 + 1]
        g = f.create_group("milady_spectral")
        _set_attr(g, "field_names", list(spectral))
        g.attrs["transform"] = "numpy.fft.rfftn"
        g.attrs["norm"] = "backward"
        g.attrs["axes"] = np.asarray(axes, dtype=np.int64)
        g.attrs["real_shape"] = np.asarray(sizes, dtype=np.int64)
        _set_attr(g, "spatial_dims", dims)
        g.attrs["domain_lengths"] = np.asarray(_domain_lengths(coords, dims), dtype=np.float64)
        g.attrs["wavenumbers"] = (
            "k_i = 2π/L_i × numpy.fft.fftfreq(n_i, 1/n_i) ; last axis: numpy.fft.rfftfreq(n_i, 1/n_i)"
        )
        physical_names = {name for _, name, _ in specs}
        for name, v in spectral.items():
            spec = dict(v) if isinstance(v, Mapping) else {"data": v}
            a = np.asarray(spec["data"])
            order = a.ndim - 2 - D
            if (
                order not in (0, 1, 2)
                or a.shape[:2] != (n_traj, n_t)
                or list(a.shape[2 : 2 + D]) != kshape
                or any(s != D for s in a.shape[2 + D :])
            ):
                raise ValueError(
                    f"spectral {name}: shape {a.shape}, expected ({n_traj}, {n_t}, *{kshape}[, {D}…])"
                )
            phys = str(spec.get("physical_field", name if name in physical_names else ""))
            if phys and phys not in physical_names:
                raise ValueError(f"spectral {name}: physical_field {phys!r} absent from the fields")
            ds = _create(g, name, a, np.complex64, compression, level)
            ds.attrs["tensor_order"] = order
            ds.attrs["physical_field"] = phys
            ds.attrs["kmax"] = int(spec.get("kmax", -1))
            ds.attrs["sample_varying"] = True
            ds.attrs["time_varying"] = True
            if spec.get("description"):
                ds.attrs["description"] = str(spec["description"])


# =============================================================================================
# Reading
# =============================================================================================
def _time_selector(t: int | slice | Sequence[int] | np.ndarray) -> slice | np.ndarray:
    if isinstance(t, slice):
        return t
    if isinstance(t, (int, np.integer)):
        t = int(t)
        return slice(t, t + 1 if t != -1 else None)
    return np.asarray(t, dtype=np.int64)


def _read_sel(node: Any, sel: tuple[Any, ...]) -> np.ndarray:
    """Read ``node[sel]``; selections by index array are applied after a slice-wise read."""
    basic = tuple(s if isinstance(s, slice) else slice(None) for s in sel)
    data = np.asarray(node[basic] if basic else node[()])
    for axis, s in enumerate(sel):
        if not isinstance(s, slice):
            data = np.take(data, s, axis=axis)
    return data


def _field_index(f: Any) -> dict[str, str]:
    """{short name: path} of the fields; the full path is used as the name in case of homonyms."""
    out: dict[str, str] = {}
    seen: dict[str, int] = {}
    paths = []
    for group in TENSOR_GROUPS:
        if group in f:
            for name in _str_list(f[group].attrs.get("field_names", [])):
                paths.append((name, f"{group}/{name}"))
                seen[name] = seen.get(name, 0) + 1
    for name, path in paths:
        out[name if seen[name] == 1 else path] = path
    return out


def _decode_meta_value(v: Any) -> Any:
    if isinstance(v, str) and v[:1] in "{[":
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return v
    return v


def read_mff(
    path: str | os.PathLike[str],
    fields: Sequence[str] | None = None,
    t: int | slice | Sequence[int] = slice(None),
    *,
    traj: int | slice | Sequence[int] = slice(None),
    spectral: bool | Sequence[str] = False,
) -> dict[str, Any]:
    """Read an MFF file (HDF5 or Zarr, local or ``s3://``) and return a dictionary.

    Keys: ``fields`` ({name: array}, ``[traj, t]`` selection applied to the axes that exist),
    ``coords`` (selected ``time``, ``x``, ``y``[, ``z``]), ``params`` (decoded ``milady_parameters``, or
    ``simulation_parameters`` attributes for a The Well file), ``meta`` (``milady_*`` attributes without
    prefix + The Well attributes + boundary conditions), ``diagnostics`` (``milady_diagnostics``,
    own ``time`` grid, not cut by ``t``), ``scalars`` and, if requested, ``spectral``.

    ``fields``: short names (``"velocity"``) or paths (``"t1_fields/velocity"``), ``None`` = all.
    ``t`` / ``traj``: integer (the axis is kept, with length 1), slice or list of indices.
    """
    with open_mff(path) as f:
        return _read(f, fields, t, traj, spectral)


def _read(
    f: Any, fields: Sequence[str] | None, t: Any, traj: Any, spectral: bool | Sequence[str]
) -> dict[str, Any]:
    attrs = _attrs(f)
    tsel = _time_selector(t)
    bsel = _time_selector(traj)
    grid_type = attrs.get("grid_type", "cartesian")
    dims = f["dimensions"]
    spatial = _str_list(dims.attrs.get("spatial_dims", []))
    time_all = np.asarray(dims["time"][()])
    time = _read_sel(dims["time"], (bsel, tsel)) if time_all.ndim == 2 else _read_sel(dims["time"], (tsel,))
    coords: dict[str, Any] = {"time": time}
    for d in spatial:
        if d in dims:
            coords[d] = np.asarray(dims[d][()])

    # Fields
    if grid_type == "fourier_fe_axisym" and "milady_fourier_fe" in f:
        fe = f["milady_fourier_fe"]
        index = {n: f"milady_fourier_fe/fields/{n}" for n in _str_list(fe.attrs.get("field_names", []))}
        coords["modes"] = np.asarray(fe["modes"][()])
    else:
        index = _field_index(f)
    wanted = list(index) if fields is None else list(fields)
    out_fields: dict[str, np.ndarray] = {}
    for name in wanted:
        key = name if name in index else next((k for k, p in index.items() if p == name), None)
        if key is None:
            raise KeyError(f"field {name!r} absent (available: {sorted(index)})")
        node = f[index[key]]
        sel: tuple[Any, ...] = ()
        if bool(_py(node.attrs.get("sample_varying", True))):
            sel += (bsel,)
        if bool(_py(node.attrs.get("time_varying", True))):
            sel += (tsel,)
        out_fields[key] = _read_sel(node, sel)

    # Parameters
    if "milady_parameters" in attrs:
        params = json.loads(attrs["milady_parameters"])
    else:
        params = {p: attrs.get(p) for p in _str_list(attrs.get("simulation_parameters", []))}

    # Metadata
    meta: dict[str, Any] = {k: attrs[k] for k in _WELL_ROOT_ATTRS if k in attrs}
    meta["spatial_dims"] = spatial
    for k, v in attrs.items():
        if k.startswith("milady_") and k != "milady_parameters":
            meta[k[len("milady_") :]] = _decode_meta_value(v)
    meta["boundary_conditions"] = {}
    if "boundary_conditions" in f:
        for name in _members(f["boundary_conditions"]):
            a = _attrs(f["boundary_conditions"][name])
            meta["boundary_conditions"][name] = {
                "bc_type": str(a.get("bc_type", "")).lower(),
                "associated_dims": _str_list(a.get("associated_dims", [])),
            }
    meta["field_paths"] = dict(index)

    # Scalars
    scal: dict[str, Any] = {}
    if "scalars" in f:
        g = f["scalars"]
        for name in _str_list(g.attrs.get("field_names", [])):
            if name not in g:
                continue
            node = g[name]
            sel = ()
            if bool(_py(node.attrs.get("sample_varying", False))):
                sel += (bsel,)
            if bool(_py(node.attrs.get("time_varying", False))):
                sel += (tsel,)
            val = _read_sel(node, sel)
            scal[name] = val.item() if val.size == 1 and not sel else val

    # Diagnostics
    diag: dict[str, Any] = {}
    if "milady_diagnostics" in f:
        g = f["milady_diagnostics"]
        diag["time"] = np.asarray(g["time"][()])
        for name in _str_list(g.attrs.get("field_names", [])):
            node = g[name]
            sv = bool(_py(node.attrs.get("sample_varying", False)))
            diag[name] = _read_sel(node, (bsel,)) if sv else np.asarray(node[()])

    out = {
        "fields": out_fields,
        "coords": coords,
        "params": params,
        "meta": meta,
        "diagnostics": diag,
        "scalars": scal,
    }

    # Spectral (on demand: often as large as the fields)
    if spectral and "milady_spectral" in f:
        g = f["milady_spectral"]
        names = _str_list(g.attrs.get("field_names", []))
        if spectral is not True:
            names = [n for n in names if n in set(spectral)]
        out["spectral"] = {n: _read_sel(g[n], (bsel, tsel)) for n in names}
        out["spectral_meta"] = {k: v for k, v in _attrs(g).items() if k != "field_names"}
    return out


def grid_info(path_or_file: Any) -> dict[str, Any]:
    """Compact description of the grid (for the ``grid`` column of the catalog)."""

    def _info(f: Any) -> dict[str, Any]:
        attrs = _attrs(f)
        dims = f["dimensions"]
        spatial = _str_list(dims.attrs.get("spatial_dims", []))
        time = np.asarray(dims["time"][()])
        info: dict[str, Any] = {
            "type": attrs.get("grid_type"),
            "n_spatial_dims": attrs.get("n_spatial_dims"),
            "dims": spatial,
            "n_trajectories": attrs.get("n_trajectories"),
            "n_t": int(time.shape[-1]),
            "t_start": float(time.min()) if time.size else None,
            "t_end": float(time.max()) if time.size else None,
        }
        present = [d for d in spatial if d in dims]
        if present:
            coords = {d: np.asarray(dims[d][()]) for d in present}
            info["shape"] = [int(coords[d].shape[-1]) for d in present]
            info["lengths"] = _domain_lengths(coords, present)
        if "boundary_conditions" in f:
            info["bc"] = sorted(
                {
                    str(_py(f["boundary_conditions"][n].attrs.get("bc_type", ""))).lower()
                    for n in _members(f["boundary_conditions"])
                }
            )
        return info

    if isinstance(path_or_file, (str, os.PathLike)):
        with open_mff(path_or_file) as f:
            return _info(f)
    return _info(path_or_file)


# =============================================================================================
# Validation
# =============================================================================================
def _validator(ref: str) -> Any:
    import jsonschema

    schema = load_schema()
    return jsonschema.Draft202012Validator({"$ref": f"#/$defs/{ref}", "$defs": schema["$defs"]})


def _schema_errors(ref: str, obj: Mapping[str, Any], where: str) -> list[str]:
    return [
        f"{where}: {'/'.join(map(str, e.absolute_path)) or 'attributes'} — {e.message}"
        for e in sorted(_validator(ref).iter_errors(dict(obj)), key=lambda e: list(e.absolute_path))
    ]


def validate(
    path: str | os.PathLike[str],
    *,
    well_only: bool = False,
    check_values: bool = True,
    full_scan: bool = False,
) -> list[str]:
    """Check the conformity of an MFF file (HDF5 or Zarr); return the list of problems (empty if conforming).

    Checks: The Well groups and attributes (shapes, exhaustive ``field_names``, ``dim_varying``,
    float32, boundary conditions), ``milady_*`` attributes against ``schema.json``, consistency of the
    parameters, diagnostics and spectral coefficients (``irfftn`` ≈ physical field on one
    snapshot), finite values (``check_values``) on the first, middle and last snapshot
    of the first trajectory; ``full_scan=True`` checks them on all trajectories and all
    snapshots (full read, one block at a time: to be reserved for archiving a dataset).
    ``well_only=True`` only checks the The Well part (files from The Well itself).
    """
    errors: list[str] = []
    values: bool | str = "all" if full_scan else check_values
    try:
        with open_mff(path) as f:
            _validate_tree(f, errors, well_only, values)
    except (OSError, KeyError, ValueError, TypeError) as exc:
        errors.append(f"unreadable or incomplete file: {exc}")
    return errors


def _validate_tree(f: Any, errors: list[str], well_only: bool, check_values: bool | str) -> None:
    E = errors.append
    attrs = _attrs(f)
    errors += _schema_errors("well_root", attrs, "root")
    for g in WELL_GROUPS:
        if g not in f or not _is_group(f[g]):
            E(f"missing group: /{g}")
    if errors:
        return
    grid_type = attrs["grid_type"]
    B = int(attrs["n_trajectories"])
    D = int(attrs["n_spatial_dims"])

    # --- dimensions ----------------------------------------------------------------------
    dims = f["dimensions"]
    spatial = _str_list(dims.attrs.get("spatial_dims", []))
    errors += _schema_errors("dimensions_group", {"spatial_dims": spatial}, "/dimensions")
    if "time" not in dims:
        E("/dimensions/time missing")
        return
    errors += _schema_errors("dimension", _attrs(dims["time"]), "/dimensions/time")
    time = np.asarray(dims["time"][()])
    t_sv = bool(_py(dims["time"].attrs.get("sample_varying", False)))
    if time.ndim != (2 if t_sv else 1) or (t_sv and time.shape[0] != B):
        E(f"/dimensions/time: shape {time.shape} inconsistent (sample_varying={t_sv}, n_trajectories={B})")
    elif time.shape[-1] > 1 and not np.all(np.diff(time, axis=-1) > 0):
        E("/dimensions/time: time not strictly increasing")
    T = int(time.shape[-1])

    if grid_type == "fourier_fe_axisym":
        _validate_fourier_fe(f, errors, B, T, check_values)
    else:
        if len(spatial) != D:
            E(f"/dimensions@spatial_dims = {spatial}: {len(spatial)} names for n_spatial_dims = {D}")
        sizes: list[int] = []
        for d in spatial:
            if d not in dims:
                E(f"/dimensions/{d} missing")
                sizes.append(-1)
                continue
            node = dims[d]
            errors += _schema_errors("dimension", _attrs(node), f"/dimensions/{d}")
            c = np.asarray(node[()])
            sizes.append(int(c.shape[-1]) if c.ndim else -1)
            if c.ndim != 1:
                E(f"/dimensions/{d}: 1D expected, shape {c.shape}")
            elif c.size > 1 and not np.all(np.diff(c) > 0):
                E(f"/dimensions/{d}: coordinates not strictly increasing")
        size_of = dict(zip(spatial, sizes))
        _validate_boundaries(f, errors, spatial, size_of)
        _validate_tensor_groups(f, errors, B, T, D, sizes, check_values)
    _validate_scalars(f, errors, attrs, B, T, well_only)
    if well_only:
        return

    # --- MilaDy part ---------------------------------------------------------------------
    meta = {k: v for k, v in attrs.items() if k.startswith("milady_")}
    params: Any = None
    if "milady_parameters" in meta:
        try:
            params = json.loads(meta["milady_parameters"])
            meta["milady_parameters"] = params
        except (TypeError, json.JSONDecodeError) as exc:
            E(f"root: @milady_parameters is not valid JSON ({exc})")
            meta["milady_parameters"] = {}
    errors += _schema_errors("milady_root", meta, "root")
    if isinstance(params, dict):
        for p in _str_list(attrs.get("simulation_parameters", [])):
            if (
                p in params
                and _is_number(params[p])
                and _is_number(attrs.get(p))
                and not math.isclose(float(params[p]), float(attrs[p]), rel_tol=1e-6, abs_tol=0.0)
            ):
                E(f"parameter {p}: @{p} = {attrs[p]} ≠ milady_parameters[{p!r}] = {params[p]}")
            if p not in params:
                E(f"parameter {p} absent from milady_parameters")
    if grid_type != "fourier_fe_axisym":
        for name, group in STANDARD_FIELDS.items():
            for other in TENSOR_GROUPS:
                if other != group and name in _str_list(f[other].attrs.get("field_names", [])):
                    E(f"standard field {name} in {other} (expected: {group})")
    if "milady_diagnostics" in f:
        _validate_diagnostics(f["milady_diagnostics"], errors, B)
    if "milady_spectral" in f and grid_type != "fourier_fe_axisym":
        _validate_spectral(f, errors, B, T, D, spatial, check_values)


def _validate_boundaries(f: Any, errors: list[str], spatial: list[str], size_of: dict[str, int]) -> None:
    E = errors.append
    g = f["boundary_conditions"]
    names = _members(g)
    if not names:
        E("/boundary_conditions: no boundary condition described")
    for name in names:
        sub = g[name]
        where = f"/boundary_conditions/{name}"
        if not _is_group(sub):
            E(f"{where}: group expected")
            continue
        a = _attrs(sub)
        errors += _schema_errors("boundary", a, where)
        assoc = _str_list(a.get("associated_dims", []))
        unknown = [d for d in assoc if d not in size_of]
        if unknown:
            E(f"{where}: unknown associated_dims {unknown}")
            continue
        if "mask" not in sub:
            E(f"{where}/mask missing")
            continue
        mask = np.asarray(sub["mask"][()])
        expected = tuple(size_of[d] for d in assoc)
        if mask.dtype != np.bool_:
            E(f"{where}/mask: type {mask.dtype}, boolean expected")
        if mask.shape != expected:
            E(f"{where}/mask: shape {mask.shape} ≠ {expected}")
        if "values" in sub:
            values = np.asarray(sub["values"][()])
            if values.shape[:1] != (int(mask.sum()),):
                E(f"{where}/values: {values.shape[:1]} values for {int(mask.sum())} mask points")


def _validate_scalars(
    f: Any, errors: list[str], attrs: dict[str, Any], B: int, T: int, well_only: bool
) -> None:
    E = errors.append
    g = f["scalars"]
    ga = _attrs(g)
    errors += _schema_errors("named_group", ga, "/scalars")
    names = _str_list(ga.get("field_names", []))
    members = set(_members(g))
    for extra in sorted(members - set(names)):
        E(f"/scalars/{extra} absent from @field_names")
    for name in names:
        where = f"/scalars/{name}"
        if name not in members:
            E(f"{where} listed in @field_names but absent")
            continue
        node = g[name]
        errors += _schema_errors("scalar", _attrs(node), where)
        sv = bool(_py(node.attrs.get("sample_varying", False)))
        tv = bool(_py(node.attrs.get("time_varying", False)))
        expected = ((B,) if sv else ()) + ((T,) if tv else ())
        if tuple(node.shape) != expected and not (expected == () and tuple(node.shape) == (1,)):
            E(f"{where}: shape {tuple(node.shape)} ≠ {expected}")
    for p in _str_list(attrs.get("simulation_parameters", [])):
        if p not in attrs:
            E(f"parameter {p} listed in @simulation_parameters without root attribute @{p}")
        elif not _is_number(attrs[p]):
            E(f"parameter {p}: non-numeric value {attrs[p]!r}")
        if not well_only and p not in names:
            E(f"parameter {p} absent from /scalars (The Well convention)")


def _validate_tensor_groups(
    f: Any, errors: list[str], B: int, T: int, D: int, sizes: list[int], check_values: bool | str
) -> None:
    E = errors.append
    for order, group in enumerate(TENSOR_GROUPS):
        g = f[group]
        ga = _attrs(g)
        errors += _schema_errors("named_group", ga, f"/{group}")
        names = _str_list(ga.get("field_names", []))
        members = set(_members(g))
        for extra in sorted(members - set(names)):
            E(f"/{group}/{extra} absent from @field_names")
        for name in names:
            where = f"/{group}/{name}"
            if name not in members:
                E(f"{where} listed in @field_names but absent")
                continue
            node = g[name]
            a = _attrs(node)
            errors += _schema_errors("t2_field" if order == 2 else "field", a, where)
            dv = a.get("dim_varying", [True] * D)
            dv = [bool(x) for x in (dv if isinstance(dv, list) else [dv])]
            if len(dv) != D:
                E(f"{where}: @dim_varying of length {len(dv)} ≠ {D}")
                continue
            sv, tv = bool(a.get("sample_varying", True)), bool(a.get("time_varying", True))
            expected = (
                ((B,) if sv else ())
                + ((T,) if tv else ())
                + tuple(s for s, used in zip(sizes, dv) if used)
                + (D,) * order
            )
            if tuple(node.shape) != expected:
                E(f"{where}: shape {tuple(node.shape)} ≠ {expected}")
                continue
            if np.dtype(node.dtype) != np.float32:
                E(f"{where}: type {node.dtype}, float32 expected (The Well)")
            if check_values and node.size:
                # Sample (default): 1st trajectory, first, middle and last snapshots;
                # full scan (full_scan): every (trajectory, snapshot), one block at a time.
                trajs = range(B) if (sv and check_values == "all") else range(1)
                if not tv:
                    steps: list[int | None] = [None]
                elif check_values == "all":
                    steps = list(range(T))
                else:
                    steps = sorted({0, T // 2, T - 1})
                bad = []
                for b in trajs:
                    for t in steps:
                        i = ((b,) if sv else ()) + ((t,) if t is not None else ())
                        if not np.all(np.isfinite(np.asarray(node[i]))):
                            bad.append(i)
                if bad:
                    more = f" (and {len(bad) - 3} more)" if len(bad) > 3 else ""
                    E(f"{where}: non-finite values at {bad[:3]}{more}")


def _validate_diagnostics(g: Any, errors: list[str], B: int) -> None:
    E = errors.append
    ga = _attrs(g)
    errors += _schema_errors("named_group", ga, "/milady_diagnostics")
    if "time" not in g:
        E("/milady_diagnostics/time missing")
        return
    td = np.asarray(g["time"][()])
    if td.ndim != 1 or (td.size > 1 and not np.all(np.diff(td) > 0)):
        E("/milady_diagnostics/time: 1D strictly increasing expected")
    names = _str_list(ga.get("field_names", []))
    for extra in sorted(set(_members(g)) - set(names) - {"time"}):
        E(f"/milady_diagnostics/{extra} absent from @field_names")
    for name in names:
        where = f"/milady_diagnostics/{name}"
        if name not in g:
            E(f"{where} listed but absent")
            continue
        node = g[name]
        errors += _schema_errors("diagnostic", _attrs(node), where)
        sv = bool(_py(node.attrs.get("sample_varying", False)))
        expected = ((B,) if sv else ()) + td.shape
        if tuple(node.shape) != expected:
            E(f"{where}: shape {tuple(node.shape)} ≠ {expected}")


def _validate_spectral(
    f: Any, errors: list[str], B: int, T: int, D: int, spatial: list[str], check_values: bool
) -> None:
    E = errors.append
    g = f["milady_spectral"]
    ga = _attrs(g)
    errors += _schema_errors("spectral_group", ga, "/milady_spectral")
    sizes = [int(f["dimensions"][d].shape[-1]) for d in spatial]
    if ga.get("real_shape") != sizes:
        E(f"/milady_spectral@real_shape = {ga.get('real_shape')} ≠ grid {sizes}")
        return
    kshape = tuple(sizes[:-1] + [sizes[-1] // 2 + 1])
    index = _field_index(f)
    names = _str_list(ga.get("field_names", []))
    for extra in sorted(set(_members(g)) - set(names)):
        E(f"/milady_spectral/{extra} absent from @field_names")
    for name in names:
        where = f"/milady_spectral/{name}"
        if name not in g:
            E(f"{where} listed but absent")
            continue
        node = g[name]
        a = _attrs(node)
        errors += _schema_errors("spectral_field", a, where)
        order = int(a.get("tensor_order", 0))
        expected = (B, T) + kshape + (D,) * order
        if tuple(node.shape) != expected:
            E(f"{where}: shape {tuple(node.shape)} ≠ {expected}")
            continue
        if not np.issubdtype(np.dtype(node.dtype), np.complexfloating):
            E(f"{where}: type {node.dtype}, complex expected")
            continue
        phys = str(a.get("physical_field", ""))
        if phys:
            if phys not in index:
                E(f"{where}: physical_field {phys!r} absent from the fields")
            elif check_values and T > 0:
                spec = np.asarray(node[0, 0], dtype=np.complex128)
                field = np.asarray(f[index[phys]][0, 0], dtype=np.float64)
                rec = np.fft.irfftn(spec, s=sizes, axes=tuple(range(D)))
                scale = float(np.sqrt(np.mean(field**2))) or 1.0
                err = float(np.sqrt(np.mean((rec - field) ** 2))) / scale
                if err > 1e-3:
                    E(f"{where}: irfftn ≠ {phys} (relative error {err:.2e} on [0, 0])")


def _validate_fourier_fe(f: Any, errors: list[str], B: int, T: int, check_values: bool) -> None:
    """Checks of the ``grid_type = "fourier_fe_axisym"`` extension (meridian mesh × Fourier modes)."""
    E = errors.append
    if "milady_fourier_fe" not in f:
        E("grid_type fourier_fe_axisym without /milady_fourier_fe group")
        return
    fe = f["milady_fourier_fe"]
    ga = _attrs(fe)
    errors += _schema_errors("fourier_fe_group", ga, "/milady_fourier_fe")
    for req in ("modes", "meshes", "fields"):
        if req not in fe:
            E(f"/milady_fourier_fe/{req} missing")
    if errors:
        return
    modes = np.asarray(fe["modes"][()])
    M = int(modes.shape[0])
    if ga.get("n_modes") != M:
        E(f"/milady_fourier_fe@n_modes = {ga.get('n_modes')} ≠ {M} modes")
    if np.any(modes < 0) or len(set(modes.tolist())) != M:
        E("/milady_fourier_fe/modes: distinct positive integers expected")
    meshes: dict[str, tuple[int, int]] = {}
    for name in _members(fe["meshes"]):
        mesh = fe["meshes"][name]
        where = f"/milady_fourier_fe/meshes/{name}"
        a = _attrs(mesh)
        errors += _schema_errors("fourier_fe_mesh", a, where)
        if "nodes" not in mesh or "connectivity" not in mesh:
            E(f"{where}: nodes and connectivity required")
            continue
        nodes = np.asarray(mesh["nodes"][()])
        conn = np.asarray(mesh["connectivity"][()])
        n_loc = {"P1": 3, "P2": 6}.get(str(a.get("element_type")), -1)
        if nodes.ndim != 2 or nodes.shape[1] != 2:
            E(f"{where}/nodes: shape {nodes.shape}, (n_nodes, 2) expected (r, z)")
        elif np.any(nodes[:, 0] < 0):
            E(f"{where}/nodes: negative radius")
        if conn.ndim != 2 or conn.shape[1] != n_loc:
            E(f"{where}/connectivity: shape {conn.shape}, ({a.get('n_elements')}, {n_loc}) expected")
        elif conn.size and (conn.min() < 0 or conn.max() >= nodes.shape[0]):
            E(f"{where}/connectivity: indices outside [0, n_nodes)")
        if a.get("n_nodes") != nodes.shape[0] or a.get("n_elements") != conn.shape[0]:
            E(f"{where}: @n_nodes/@n_elements inconsistent with the arrays")
        n_vert = int(mesh["vertices"].shape[0]) if "vertices" in mesh else nodes.shape[0]
        meshes[name] = (int(nodes.shape[0]), n_vert)
    names = _str_list(ga.get("field_names", []))
    for extra in sorted(set(_members(fe["fields"])) - set(names)):
        E(f"/milady_fourier_fe/fields/{extra} absent from @field_names")
    for name in names:
        where = f"/milady_fourier_fe/fields/{name}"
        if name not in fe["fields"]:
            E(f"{where} listed but absent")
            continue
        node = fe["fields"][name]
        a = _attrs(node)
        errors += _schema_errors("fourier_fe_field", a, where)
        if a.get("mesh") not in meshes:
            E(f"{where}: unknown mesh {a.get('mesh')!r}")
            continue
        n_all, n_vert = meshes[a["mesh"]]
        n = n_vert if a.get("node_set") == "vertices" else n_all
        expected = (B, T, M, 2, n) + ((3,) if int(a.get("tensor_order", 0)) == 1 else ())
        if tuple(node.shape) != expected:
            E(
                f"{where}: shape {tuple(node.shape)} ≠ {expected} (traj, t, mode, cos/sin, node[, component])"
            )
        elif check_values and not np.all(np.isfinite(np.asarray(node[0, 0]))):
            E(f"{where}[0, 0]: non-finite values")


# =============================================================================================
# Zarr
# =============================================================================================
def _copy_attrs(src: Any, dst: Any) -> None:
    dst.attrs.update({k: _py(v) for k, v in src.attrs.items()})


def to_zarr(path_h5: str | os.PathLike[str], uri: str, *, overwrite: bool = False) -> str:
    """Copy an HDF5 MFF file to the same hierarchy in Zarr (v3), local or ``s3://…/name.zarr``.

    Identical blocks (one time step per block), default Zarr compression (zstd), attributes converted
    to JSON. The copy is done block by block (bounded memory). Returns ``uri``.
    """
    if not _is_zarr(uri):
        raise ValueError("the Zarr URI must end with .zarr")
    if not overwrite and storage.exists(uri):
        raise FileExistsError(f"{uri} already exists (overwrite=True to replace)")
    if overwrite and storage.exists(uri):
        storage.rm(uri, recursive=True)
    if not storage.is_local(uri):
        storage.ensure_bucket(uri)
    root = _open_zarr(uri, "w")
    with open_mff(path_h5) as f:
        _copy_attrs(f, root)

        def visit(src: h5py.Group, dst: Any) -> None:
            for key in src:
                node = src[key]
                if isinstance(node, h5py.Group):
                    sub = dst.create_group(key)
                    _copy_attrs(node, sub)
                    visit(node, sub)
                    continue
                chunks = node.chunks or (node.shape if node.shape else ())
                if node.shape and 0 in node.shape:
                    chunks = tuple(max(1, c) for c in node.shape)
                arr = dst.create_array(key, shape=node.shape, dtype=node.dtype, chunks=chunks)
                if node.ndim >= 3 and node.chunks:
                    for i in range(node.shape[0]):
                        arr[i] = node[i]
                elif node.size:
                    arr[...] = node[()]
                _copy_attrs(node, arr)

        visit(f, root)
    return uri


# =============================================================================================
# Readable description (equivalent of h5dump -H)
# =============================================================================================
def describe(path: str | os.PathLike[str], max_list: int = 8) -> str:
    """Readable tree of the file (groups, datasets, shapes, types, attributes), like ``h5dump -H``."""
    lines: list[str] = []

    def fmt(v: Any) -> str:
        v = _py(v)
        if isinstance(v, list) and len(v) > max_list:
            return repr(v[:max_list])[:-1] + ", …]"
        s = repr(v)
        return s if len(s) <= 100 else s[:97] + "…"

    def walk(node: Any, name: str, depth: int) -> None:
        pad = "  " * depth
        if _is_group(node):
            lines.append(f"{pad}{name}/")
            for k, v in sorted(node.attrs.items()):
                lines.append(f"{pad}  @{k} = {fmt(v)}")
            for k in _members(node):
                walk(node[k], k, depth + 1)
        else:
            extra = ""
            if isinstance(node, h5py.Dataset):
                if node.chunks:
                    extra += f" chunks={node.chunks}"
                if node.compression:
                    extra += f" {node.compression}"
                    if node.compression_opts is not None:
                        extra += f"({node.compression_opts})"
            lines.append(f"{pad}{name}: {np.dtype(node.dtype)}{tuple(node.shape)}{extra}")
            for k, v in sorted(node.attrs.items()):
                lines.append(f"{pad}  @{k} = {fmt(v)}")

    with open_mff(path) as f:
        walk(f, "", 0)
    return "\n".join(lines)
