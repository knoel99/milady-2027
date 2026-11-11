"""Simulation campaigns: expansion of a YAML file into simulations, registration in the catalog,
local execution, in Docker containers or as a Slurm job array.

Usage ::

    python -m milady.sweep infra/configs/stage2_abc3d.yaml --scheduler local  [--max-parallel 2]
    python -m milady.sweep infra/configs/stage2_abc3d.yaml --scheduler docker [--max-parallel 4]
    python -m milady.sweep infra/configs/stage2_abc3d.yaml --scheduler slurm  [--dry-run]
    python -m milady.sweep CONFIG --scheduler local --dry-run                  # plan, without running anything

Format of a campaign (see ``infra/configs/*.yaml``) ::

    name: stage2_abc3d                 # identifier (letters, digits, "_", "-", ".")
    description: free text
    code: mhd3d_torch                   # or mhd2d_numpy
    grid: {N: 64, domain: 2pi}          # N integer or [nx, ny, nz]; domain number, "2pi" or list
    fixed: {mode: kinematic, flow: abc} # parameters common to all simulations
    sweep:                              # Cartesian product (the last key varies fastest)
      Rm: [6, 8, 10]                    #   list
      Pm: {start: 0.5, stop: 4, num: 4, scale: log}   # range: num points (lin or log), bounds included
      Re: {start: 50, stop: 200, step: 50}            # range: fixed step, upper bound included
    runtime: {dt: 0.02, t_burn: 100, t_keep: 100, every: 5, n_traj: 2, diag_every: 0.5,
              cfl: 1.0, device: auto, dtype: float32, checkpoint_every_s: 900}
    resources: {gpus: 1, cpus: 8, time: "02:00:00", mem: null, max_parallel: 16,
                account: null, partition: null, qos: null, constraint: null}
    output: {format: mff, uri: "${MILADY_STORAGE_URI}", fields: [velocity, magnetic_field],
             spectral: false, dataset_name: milady_stage2_abc3d}

Each simulation receives a **deterministic** identifier (UUID v5 of the campaign name, the index,
the parameters, the grid and the time settings): ``milady.sweep`` registers it in the catalog
(status ``queued``) and ``milady.sim.run CONFIG --index i`` finds it again without any exchange between them
(Slurm array, containers). Relaunching a campaign is therefore idempotent: ``done`` simulations
are skipped (``--force`` to redo everything), ``failed`` and ``queued`` ones are relaunched,
``running`` ones too with ``--retry-running`` (lost node, preemptible instance recovered).

This module depends only on PyYAML to expand a campaign: on a VM, it can drive the
containers from the host (``--scheduler docker``) without PyTorch or direct access to the catalog.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as _dt
import itertools
import json
import math
import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from milady import __version__, git_commit, project_root
from milady.sim import CODES, physical_parameters

__all__ = [
    "Campaign",
    "SweepPoint",
    "expand_values",
    "grid_spec",
    "load_campaign",
    "main",
    "output_times",
    "parse_indices",
    "simulation_id",
    "sweep_points",
]

#: Namespace of the deterministic simulation identifiers (UUID v5).
SIM_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://knoel99.github.io/milady-2027/simulation")
_TOP_KEYS = {"name", "description", "code", "grid", "fixed", "sweep", "runtime", "resources", "output"}
_RUNTIME_KEYS = {
    "dt", "t_burn", "t_keep", "every", "n_traj", "diag_every", "cfl", "device", "dtype",
    "checkpoint_every_s", "checkpoint_to_storage", "keep_checkpoint",
}  # fmt: skip
#: Time settings that change the result of a simulation (they enter its identifier).
_RUNTIME_ID_KEYS = ("dt", "t_burn", "t_keep", "every", "n_traj", "diag_every", "cfl")
_RESOURCE_KEYS = {"gpus", "cpus", "time", "mem", "max_parallel", "account", "partition", "qos", "constraint"}
_OUTPUT_KEYS = {"format", "uri", "fields", "spectral", "dataset_name"}
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_PARAM_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PENDING_TAG = "MILADY_PENDING"


# =============================================================================================
# Campaign
# =============================================================================================
@dataclass
class Campaign:
    """Simulation campaign read from a YAML file (see the module docstring)."""

    name: str
    code: str
    grid: dict[str, Any]
    runtime: dict[str, Any]
    description: str = ""
    fixed: dict[str, Any] = field(default_factory=dict)
    sweep: dict[str, Any] = field(default_factory=dict)
    resources: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    path: Path | None = None
    text: str = ""

    @property
    def n_dims(self) -> int:
        """Number of spatial dimensions of the code."""
        return 2 if self.code == "mhd2d_numpy" else 3

    @property
    def shape(self) -> list[int]:
        """Grid points per direction."""
        n = self.grid["N"]
        return [int(v) for v in n] if isinstance(n, (list, tuple)) else [int(n)] * self.n_dims

    @property
    def lengths(self) -> list[float]:
        """Domain lengths per direction."""
        d = self.grid.get("domain", 2 * math.pi)
        return [float(v) for v in d] if isinstance(d, (list, tuple)) else [float(d)] * self.n_dims


def _parse_length(v: Any) -> float:
    """Length: number, or string ``2pi``, ``2π``, ``pi``, ``4*pi``…"""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    s = str(v).strip().lower().replace("π", "pi").replace(" ", "").replace("*", "")
    m = re.fullmatch(r"([0-9.eE+-]*)pi", s)
    if m:
        return (float(m.group(1)) if m.group(1) else 1.0) * math.pi
    return float(s)


def load_campaign(path: str | os.PathLike[str]) -> Campaign:
    """Read and validate a YAML campaign (known keys, parameter names, consistent times)."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise TypeError(f"{path}: YAML dictionary expected")
    unknown = set(raw) - _TOP_KEYS
    if unknown:
        raise ValueError(f"{path}: unknown keys {sorted(unknown)} (expected: {sorted(_TOP_KEYS)})")
    for key in ("name", "code", "grid", "runtime"):
        if key not in raw:
            raise ValueError(f"{path}: required key \"{key}\" missing")
    name = str(raw["name"])
    if not _NAME_RE.match(name):
        raise ValueError(f"invalid campaign name: {name!r}")
    code = str(raw["code"])
    if code not in CODES:
        raise ValueError(f"code {code!r} unknown (expected: {', '.join(CODES)})")
    grid = dict(raw["grid"] or {})
    if "N" not in grid:
        raise ValueError("grid.N required")
    d = grid.get("domain", 2 * math.pi)
    grid["domain"] = [_parse_length(x) for x in d] if isinstance(d, (list, tuple)) else _parse_length(d)
    runtime = dict(raw["runtime"] or {})
    bad = set(runtime) - _RUNTIME_KEYS
    if bad:
        raise ValueError(f"runtime: unknown keys {sorted(bad)} (accepted: {sorted(_RUNTIME_KEYS)})")
    for key in ("dt", "t_keep", "every"):
        if key not in runtime:
            raise ValueError(f"runtime.{key} required")
    runtime.setdefault("t_burn", 0.0)
    runtime.setdefault("n_traj", 1)
    resources = dict(raw.get("resources") or {})
    bad = set(resources) - _RESOURCE_KEYS
    if bad:
        raise ValueError(f"resources: unknown keys {sorted(bad)} (accepted: {sorted(_RESOURCE_KEYS)})")
    output = dict(raw.get("output") or {})
    bad = set(output) - _OUTPUT_KEYS
    if bad:
        raise ValueError(f"output: unknown keys {sorted(bad)} (accepted: {sorted(_OUTPUT_KEYS)})")
    fields = output.get("fields") or ["velocity", "magnetic_field"]
    if not isinstance(fields, list) or not fields or set(fields) - {"velocity", "magnetic_field"}:
        raise ValueError(
            f"output.fields: non-empty subset of [velocity, magnetic_field], got {fields!r}"
        )
    fixed = dict(raw.get("fixed") or {})
    sweep = dict(raw.get("sweep") or {})
    overlap = set(fixed) & set(sweep)
    if overlap:
        raise ValueError(f"parameters both fixed and swept: {sorted(overlap)}")
    for key in list(fixed) + list(sweep):
        if not _PARAM_RE.match(str(key)) or str(key).startswith("milady_"):
            raise ValueError(f"invalid parameter name: {key!r}")
    camp = Campaign(
        name=name,
        code=code,
        grid=grid,
        runtime=runtime,
        description=str(raw.get("description") or ""),
        fixed=fixed,
        sweep=sweep,
        resources=resources,
        output=output,
        path=path,
        text=text,
    )
    output_times(camp.runtime)  # time consistency check
    if code == "mhd2d_numpy" and (
        len(camp.shape) != 2 or any(abs(L - 2 * math.pi) > 1e-9 for L in camp.lengths)
    ):
        raise ValueError("mhd2d_numpy: square 2D grid on [0, 2π)² only (integer N, domain 2pi)")
    return camp


def _clean(x: float) -> float | int:
    """Round to 12 significant digits (avoids 0.30000000000000004); integers kept."""
    if isinstance(x, int):
        return x
    return float(f"{x:.12g}")


def expand_values(spec: Any) -> list[Any]:
    """Values of a swept parameter: list, scalar, or range ``{start, stop, num[, scale]}`` /
    ``{start, stop, step}`` (bounds included) / ``{values: [...]}``."""
    if isinstance(spec, (list, tuple)):
        if not spec:
            raise ValueError("empty list of values")
        return list(spec)
    if not isinstance(spec, Mapping):
        return [spec]
    if "values" in spec:
        return expand_values(list(spec["values"]))
    if "start" not in spec or "stop" not in spec:
        raise ValueError(f"invalid range {dict(spec)}: start and stop required")
    a, b = float(spec["start"]), float(spec["stop"])
    if "num" in spec:
        n = int(spec["num"])
        if n < 1:
            raise ValueError("num ≥ 1")
        scale = str(spec.get("scale", "lin")).lower()
        if n == 1:
            return [_clean(a)]
        if scale in ("log", "geom", "geometric"):
            if a <= 0 or b <= 0:
                raise ValueError("log scale: bounds > 0")
            la, lb = math.log(a), math.log(b)
            return [_clean(math.exp(la + (lb - la) * i / (n - 1))) for i in range(n)]
        if scale not in ("lin", "linear"):
            raise ValueError(f"scale {scale!r}: lin or log")
        return [_clean(a + (b - a) * i / (n - 1)) for i in range(n)]
    if "step" in spec:
        step = float(spec["step"])
        if step == 0 or (b - a) / step < 0:
            raise ValueError("zero step or wrong sign")
        n = math.floor((b - a) / step + 1e-9) + 1
        ints = all(
            isinstance(spec[k], int) and not isinstance(spec[k], bool) for k in ("start", "stop", "step")
        )
        return [int(a + i * step) if ints else _clean(a + i * step) for i in range(n)]
    raise ValueError(f"invalid range {dict(spec)}: num or step required")


def output_times(runtime: Mapping[str, Any]) -> tuple[list[float], list[float]]:
    """(times of the kept fields, times of the diagnostics).

    Fields: t_burn + k × every, k = 1…round(t_keep/every) (E2 convention). Diagnostics: every
    ``diag_every`` (default ``every``) from t = 0 up to t_burn + t_keep (inclusive).
    """
    dt, every, t_keep = float(runtime["dt"]), float(runtime["every"]), float(runtime["t_keep"])
    t_burn = float(runtime.get("t_burn", 0.0))
    if dt <= 0 or every <= 0 or t_keep <= 0 or t_burn < 0:
        raise ValueError("runtime: dt, every, t_keep > 0 and t_burn ≥ 0 required")
    n_keep = round(t_keep / every)
    if n_keep < 1 or abs(n_keep * every - t_keep) > 1e-6 * t_keep:
        raise ValueError(f"runtime: t_keep = {t_keep} must be a multiple of every = {every}")
    snaps = [_clean(t_burn + k * every) for k in range(1, n_keep + 1)]
    t_end = t_burn + t_keep
    de = float(runtime.get("diag_every", every))
    if de <= 0:
        raise ValueError("runtime.diag_every > 0 required")
    n_d = math.floor(t_end / de + 1e-9)
    diags = [_clean(j * de) for j in range(n_d + 1)]
    if abs(diags[-1] - t_end) > 1e-9 * max(1.0, t_end):
        diags.append(_clean(t_end))
    return [float(t) for t in snaps], [float(t) for t in diags]


@dataclass
class SweepPoint:
    """One simulation of the campaign."""

    index: int
    point: dict[str, Any]  # parameters as written (fixed + swept)
    params: dict[str, Any]  # complete physical parameters (catalog, MFF file)
    sim_id: str


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def simulation_id(campaign: Campaign, index: int, params: Mapping[str, Any]) -> str:
    """Deterministic identifier (UUID v5) of a campaign simulation."""
    key = {
        "campaign": campaign.name,
        "code": campaign.code,
        "index": int(index),
        "params": dict(params),
        "grid": {"shape": campaign.shape, "lengths": campaign.lengths},
        "runtime": {k: campaign.runtime[k] for k in _RUNTIME_ID_KEYS if k in campaign.runtime},
    }
    return str(uuid.uuid5(SIM_NAMESPACE, _canonical(key)))


def sweep_points(campaign: Campaign) -> list[SweepPoint]:
    """Expand the campaign: Cartesian product of the swept values (YAML order, last key fastest)."""
    keys = list(campaign.sweep)
    values = [expand_values(campaign.sweep[k]) for k in keys]
    grid = {"domain": campaign.lengths[0]}
    out = []
    for index, combo in enumerate(itertools.product(*values) if keys else [()]):
        point = {**campaign.fixed, **dict(zip(keys, combo))}
        params = physical_parameters(campaign.code, point, grid)
        out.append(SweepPoint(index, point, params, simulation_id(campaign, index, params)))
    return out


def grid_spec(campaign: Campaign) -> dict[str, Any]:
    """Description of the grid for the ``grid`` column of the catalog (same keys as ``format.grid_info``)."""
    snaps, _ = output_times(campaign.runtime)
    dims = ["x", "y", "z"][: campaign.n_dims]
    return {
        "type": "cartesian",
        "n_spatial_dims": campaign.n_dims,
        "dims": dims,
        "shape": campaign.shape,
        "lengths": campaign.lengths,
        "bc": ["periodic"],
        "dealias": "2/3",
        "n_trajectories": int(campaign.runtime.get("n_traj", 1)),
        "n_t": len(snaps),
        "t_start": snaps[0],
        "t_end": snaps[-1],
    }


def parse_indices(spec: str | None, n: int) -> list[int]:
    """``"0,3,5-7"`` → [0, 3, 5, 6, 7] (bounds checked); ``None`` → all."""
    if not spec:
        return list(range(n))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = (int(x) for x in part.split("-", 1))
            out.extend(range(a, b + 1))
        else:
            out.append(int(part))
    bad = [i for i in out if not 0 <= i < n]
    if bad:
        raise ValueError(f"indices outside [0, {n - 1}]: {bad}")
    return sorted(set(out))


def _ranges(indices: Sequence[int]) -> str:
    """[0, 1, 2, 5, 7, 8] → "0-2,5,7-8" (syntax of ``sbatch --array``)."""
    parts: list[str] = []
    for _, grp in itertools.groupby(enumerate(sorted(indices)), key=lambda p: p[1] - p[0]):
        g = [v for _, v in grp]
        parts.append(str(g[0]) if len(g) == 1 else f"{g[0]}-{g[-1]}")
    return ",".join(parts)


# =============================================================================================
# Catalog
# =============================================================================================
def register(
    campaign: Campaign,
    points: Sequence[SweepPoint],
    *,
    force: bool = False,
    retry_running: bool = False,
    log: Any = print,
) -> list[SweepPoint]:
    """Create the campaign and the ``queued`` simulations in the catalog; return those to run.

    Simulations already present: ``done`` skipped (unless ``force``), ``running`` skipped (unless
    ``force`` or ``retry_running``), ``failed``/``queued`` put back in the queue.
    """
    from milady.catalog.api import Catalog

    cat = Catalog()
    camp_id = cat.create_campaign(campaign.name, config_yaml=campaign.text, description=campaign.description)
    existing = {s["id"]: s for s in cat.query_simulations(campaign=campaign.name)}
    grid = grid_spec(campaign)
    gpus, cpus = int(campaign.resources.get("gpus", 0) or 0), int(campaign.resources.get("cpus", 0) or 0)
    commit = git_commit()
    pending: list[SweepPoint] = []
    skipped: dict[str, int] = {}
    for p in points:
        sim = existing.get(p.sim_id)
        if sim is None:
            cat.register_simulation(
                camp_id,
                campaign.code,
                p.params,
                grid,
                code_version=__version__,
                git_commit=commit,
                host="",
                n_gpus=gpus,
                n_cpus=cpus,
                sim_id=p.sim_id,
            )
            pending.append(p)
            continue
        status = sim["status"]
        if (status == "done" and not force) or (status == "running" and not (force or retry_running)):
            skipped[status] = skipped.get(status, 0) + 1
            continue
        if status != "queued":
            cat.update_simulation(
                p.sim_id, status="queued", started_at=None, finished_at=None, wall_time_s=None
            )
        pending.append(p)
    cat.close()
    if skipped:
        log(
            "simulations skipped: "
            + ", ".join(f"{n} {s}" for s, n in sorted(skipped.items()))
            + " (--force to rerun everything, --retry-running for orphaned \"running\" ones)"
        )
    return pending


# =============================================================================================
# Execution
# =============================================================================================
def _gpu_count() -> int:
    """Number of visible NVIDIA GPUs (``nvidia-smi -L``), 0 without a driver; without importing torch."""
    visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    if visible is not None:
        return len([v for v in visible.split(",") if v.strip() and v.strip() != "-1"])
    exe = shutil.which("nvidia-smi")
    if not exe:
        return 0
    try:
        out = subprocess.run([exe, "-L"], capture_output=True, text=True, timeout=20, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return 0
    return sum(1 for line in out.splitlines() if line.startswith("GPU"))


def _sweep_dir(campaign: Campaign) -> Path:
    """Folder of the launched campaign (frozen copy of the configuration, scripts, logs)."""
    stamp = _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    env = os.environ.get("MILADY_SWEEP_DIR")
    base = Path(os.path.expandvars(env)).expanduser() if env else project_root() / "data" / "sweeps"
    path = base / campaign.name / stamp
    path.mkdir(parents=True, exist_ok=True)
    return path


def _freeze_config(campaign: Campaign, sweep_dir: Path) -> Path:
    """Frozen copy of the configuration: queued jobs re-read it as is (stable identifiers)."""
    frozen = sweep_dir / f"{campaign.name}.yaml"
    frozen.write_text(campaign.text, encoding="utf-8")
    return frozen


def _repo_relative(path: Path) -> str:
    """Path relative to the repository root if possible (visible as is in the containers), otherwise absolute."""
    root = project_root()
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path.resolve())


def _child_env(extra: Mapping[str, str]) -> dict[str, str]:
    env = dict(os.environ)
    root = str(project_root())
    env["PYTHONPATH"] = root + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env.setdefault("MILADY_GIT_COMMIT", git_commit())
    env.update(extra)
    return env


def _run_pool(
    points: Sequence[SweepPoint], max_parallel: int, gpus: int, launch: Any, log: Any
) -> dict[int, int]:
    """Run ``launch(point, slot)`` with at most ``max_parallel`` simultaneous tasks.

    ``slot``: assigned GPU index (round-robin) or ``None`` without GPU. Returns {index: return code}.
    """
    slots: queue.Queue[int | None] = queue.Queue()
    for k in range(max_parallel):
        slots.put(k % gpus if gpus > 0 else None)
    results: dict[int, int] = {}
    lock = threading.Lock()
    t0 = time.monotonic()

    def task(p: SweepPoint) -> None:
        slot = slots.get()
        try:
            code = launch(p, slot)
        finally:
            slots.put(slot)
        with lock:
            results[p.index] = code
            state = "ok" if code == 0 else f"FAILED (code {code})"
            log(
                f"[{len(results)}/{len(points)}] simulation {p.index} ({p.sim_id[:8]}) : {state} "
                f"— {time.monotonic() - t0:.0f} s elapsed"
            )

    with cf.ThreadPoolExecutor(max_workers=max_parallel) as ex:
        list(ex.map(task, points))
    return results


def _sim_command(cfg_arg: str, index: int, extra: Sequence[str]) -> list[str]:
    return ["python", "-m", "milady.sim.run", cfg_arg, "--index", str(index), *extra]


def run_local(
    campaign: Campaign,
    cfg_path: Path,
    points: Sequence[SweepPoint],
    *,
    max_parallel: int,
    log_dir: Path,
    run_args: Sequence[str],
    use_catalog: bool,
    log: Any = print,
) -> dict[int, int]:
    """Run the simulations in subprocesses of the current machine."""
    gpus = _gpu_count()
    # Threads per simulation: never more than the available cores / simultaneous simulations
    # (oversubscription slows down FFTs by a factor of 10 to 100 on a loaded machine).
    share = max(1, (os.cpu_count() or 1) // max_parallel)
    cpus = min(int(campaign.resources.get("cpus", 0) or 0) or share, share)
    cat = None
    if use_catalog:
        from milady.catalog.api import Catalog

        cat = Catalog()
    log_dir.mkdir(parents=True, exist_ok=True)

    def launch(p: SweepPoint, slot: int | None) -> int:
        log_path = log_dir / f"sim-{p.index:05d}.log"
        extra = {"MILADY_SCHEDULER": "local", "OMP_NUM_THREADS": str(cpus), "MKL_NUM_THREADS": str(cpus)}
        if slot is not None:
            extra["CUDA_VISIBLE_DEVICES"] = str(slot)
        job_id = None
        if cat is not None:
            job_id = cat.register_job(
                "simulation",
                "local",
                simulation_id=p.sim_id,
                status="queued",
                log_uri=log_path.resolve().as_uri(),
            )
            extra["MILADY_JOB_ID"] = job_id
        cmd = _sim_command(str(cfg_path), p.index, run_args)
        cmd[0] = sys.executable
        with open(log_path, "w", encoding="utf-8") as fh:
            proc = subprocess.Popen(
                cmd, cwd=project_root(), env=_child_env(extra), stdout=fh, stderr=subprocess.STDOUT
            )
            if cat is not None and job_id is not None:
                cat.update_job(job_id, external_id=str(proc.pid))
            code = proc.wait()
        if code != 0 and cat is not None and job_id is not None:
            job = cat.get_job(job_id) if hasattr(cat, "get_job") else None
            if job is None or job.get("status") not in ("failed", "cancelled"):
                cat.update_job(job_id, status="failed")
        return code

    log(
        f"local execution: {len(points)} simulation(s), {max_parallel} in parallel, {cpus} thread(s) each"
        + (f", {gpus} GPU" if gpus else ", CPU")
        + f"; logs: {log_dir}"
    )
    try:
        return _run_pool(points, max_parallel, gpus, launch, log)
    finally:
        if cat is not None:
            cat.close()


def _compose_base() -> list[str]:
    env = os.environ.get("MILADY_COMPOSE")
    if env:
        return shlex.split(env)
    root = project_root()
    return [
        "docker",
        "compose",
        "-f",
        str(root / "infra/docker/docker-compose.yml"),
        "--env-file",
        str(root / "infra/docker/.env"),
    ]


def _compose_worker() -> str:
    if os.environ.get("MILADY_WORKER"):
        return os.environ["MILADY_WORKER"]
    env_file = project_root() / "infra/docker/.env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("MILADY_WORKER="):
                return line.split("=", 1)[1].strip() or "worker"
    return "worker"


def _docker_register(cfg_arg: str, args: argparse.Namespace, log: Any) -> list[int]:
    """Register the campaign from a container (access to the catalog of the compose network); return the indices to run."""
    cmd = [
        *_compose_base(),
        "run",
        "--rm",
        "-T",
        _compose_worker(),
        "python",
        "-m",
        "milady.sweep",
        cfg_arg,
        "--scheduler",
        "docker",
        "--register-only",
    ]
    if args.indices:
        cmd += ["--indices", args.indices]
    if args.force:
        cmd.append("--force")
    if args.retry_running:
        cmd.append("--retry-running")
    log("registration in the catalog (container): " + shlex.join(cmd))
    env = _child_env({"GIT_COMMIT": os.environ.get("GIT_COMMIT") or git_commit()})
    out = subprocess.run(cmd, cwd=project_root(), env=env, capture_output=True, text=True, check=False)
    sys.stderr.write(out.stderr)
    if out.returncode != 0:
        sys.stdout.write(out.stdout)
        raise RuntimeError(f"registration in the container failed (code {out.returncode})")
    for line in reversed(out.stdout.splitlines()):
        if line.startswith(_PENDING_TAG):
            return [int(i) for i in json.loads(line[len(_PENDING_TAG) :])["pending"]]
    raise RuntimeError("unreadable registration response:\n" + out.stdout)


def run_docker(
    campaign: Campaign,
    cfg_arg: str,
    points: Sequence[SweepPoint],
    *,
    max_parallel: int,
    log_dir: Path,
    run_args: Sequence[str],
    log: Any = print,
) -> dict[int, int]:
    """Run each simulation in a ``docker compose run --rm worker`` container (GPU assigned per task)."""
    worker = _compose_worker()
    gpus = _gpu_count() if worker.endswith("gpu") else 0
    log_dir.mkdir(parents=True, exist_ok=True)
    env = _child_env({"GIT_COMMIT": os.environ.get("GIT_COMMIT") or git_commit()})

    def launch(p: SweepPoint, slot: int | None) -> int:
        cmd = [*_compose_base(), "run", "--rm", "-T", "-e", "MILADY_SCHEDULER=docker"]
        if slot is not None:
            cmd += ["-e", f"CUDA_VISIBLE_DEVICES={slot}"]
        cmd += [worker, *_sim_command(cfg_arg, p.index, run_args)]
        with open(log_dir / f"sim-{p.index:05d}.log", "w", encoding="utf-8") as fh:
            fh.write("$ " + shlex.join(cmd) + "\n")
            fh.flush()
            return subprocess.run(
                cmd, cwd=project_root(), env=env, stdout=fh, stderr=subprocess.STDOUT, check=False
            ).returncode

    log(
        f"Docker execution ({worker}): {len(points)} simulation(s), {max_parallel} container(s) in parallel"
        + (f", {gpus} GPU" if gpus else "")
        + f"; logs: {log_dir}"
    )
    return _run_pool(points, max_parallel, gpus, launch, log)


# --- Slurm -------------------------------------------------------------------------------------
_FALLBACK_SBATCH = """#!/bin/bash
# Slurm job array of MilaDy (minimal template: infra/slurm/gen_data.sbatch missing).
#SBATCH --job-name=milady-sim
#SBATCH --array=0-0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=04:00:00
#SBATCH --output=%x-%A_%a.out
set -euo pipefail
CONFIG="${1:?campaign.yaml}"
shift
cd "${MILADY_ROOT:-${SLURM_SUBMIT_DIR:-.}}"
python -m milady.sim.run "${CONFIG}" --index "${SLURM_ARRAY_TASK_ID:-0}" "$@"
"""


def _job_name(campaign: Campaign) -> str:
    """Name of the campaign Slurm jobs (``%x`` in log file names)."""
    return f"milady-sim-{campaign.name}"[:64]


def _read_simple_env(path: Path) -> dict[str, str]:
    """Lines ``KEY=value`` of a shell-like file (without execution; ``$VAR`` expanded)."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
        if m:
            val = m.group(2).strip().strip("'\"")
            out[m.group(1)] = os.path.expandvars(val)
    return out


def slurm_catalog_defaults(log: Any = print) -> None:
    """Login-node catalog = the one of the jobs: same defaults as ``infra/slurm/env.sh``.

    If ``MILADY_DB_URL`` is not defined: ``sqlite:///$MILADY_STATE/catalog.sqlite`` with
    ``MILADY_STATE`` = ``$WORK/milady`` (otherwise ``<root>/data``), after reading
    ``~/.config/milady/slurm.env`` (lines ``KEY=value``). The variable is exported: ``sbatch``
    passes it to the jobs, which therefore write into the same database.
    """
    if os.environ.get("MILADY_DB_URL"):
        return
    conf = _read_simple_env(Path.home() / ".config/milady/slurm.env")
    if conf.get("MILADY_DB_URL"):
        url = conf["MILADY_DB_URL"]
    else:
        state = conf.get("MILADY_STATE") or os.environ.get("MILADY_STATE")
        if not state:
            work = os.environ.get("WORK")
            state = f"{work}/milady" if work else str(project_root() / "data")
        Path(state).mkdir(parents=True, exist_ok=True)
        url = f"sqlite:///{state}/catalog.sqlite"
    os.environ["MILADY_DB_URL"] = url
    log(f"catalog (as infra/slurm/env.sh): {url}")


def render_sbatch(
    campaign: Campaign,
    indices: Sequence[int],
    log_dir: Path,
    max_parallel: int | None,
    template: str | None = None,
) -> str:
    """sbatch script of the array: template ``infra/slurm/gen_data.sbatch`` whose #SBATCH options are
    replaced by those of the campaign (array, duration, cores, GPU, account, partition…)."""
    if template is None:
        tpl_path = project_root() / "infra/slurm/gen_data.sbatch"
        template = tpl_path.read_text(encoding="utf-8") if tpl_path.is_file() else _FALLBACK_SBATCH
    res = campaign.resources
    array = _ranges(indices) + (f"%{max_parallel}" if max_parallel else "")
    opts: dict[str, str | None] = {
        "job-name": _job_name(campaign),
        "array": array,
        "output": str(log_dir / "%x-%A_%a.out"),
        "error": str(log_dir / "%x-%A_%a.out"),
        "cpus-per-task": str(int(res["cpus"])) if res.get("cpus") else None,
        "time": str(res["time"]) if res.get("time") else None,
        "mem": str(res["mem"]) if res.get("mem") else None,
        "gres": f"gpu:{int(res['gpus'])}" if int(res.get("gpus", 0) or 0) > 0 else "",
        "account": res.get("account"),
        "partition": res.get("partition"),
        "qos": res.get("qos"),
        "constraint": res.get("constraint"),
    }
    lines = template.splitlines()
    seen: set[str] = set()
    out: list[str] = []
    last_sbatch = -1
    rx = re.compile(r"^#SBATCH\s+--([A-Za-z-]+)(?:[=\s]+(.*))?$")
    for line in lines:
        m = rx.match(line.strip())
        if m and m.group(1) in opts:
            key = m.group(1)
            seen.add(key)
            val = opts[key]
            if val is None:  # campaign option absent: keep the one of the template
                out.append(line)
            elif val != "":  # empty string: option removed (e.g. --gres without GPU)
                out.append(f"#SBATCH --{key}={val}")
            last_sbatch = len(out) - 1
            continue
        out.append(line)
        if line.startswith("#SBATCH"):
            last_sbatch = len(out) - 1
    extra = [f"#SBATCH --{k}={v}" for k, v in opts.items() if k not in seen and v]
    if extra:
        header = ["# --- options added by milady.sweep (campaign " + campaign.name + ") ---", *extra]
        out[last_sbatch + 1 : last_sbatch + 1] = header
    return "\n".join(out) + "\n"


def run_slurm(
    campaign: Campaign,
    cfg_arg: str,
    points: Sequence[SweepPoint],
    *,
    sweep_dir: Path,
    max_parallel: int | None,
    sbatch_args: Sequence[str],
    run_args: Sequence[str],
    dry_run: bool,
    use_catalog: bool,
    log: Any = print,
) -> int:
    """Write the job array script and submit it (``sbatch --parsable``); register the tasks."""
    script = render_sbatch(campaign, [p.index for p in points], sweep_dir, max_parallel)
    cmd = ["sbatch", "--parsable", *sbatch_args, "<script>", cfg_arg, *run_args]
    if dry_run:
        log("--- sbatch script (not submitted) ---\n" + script + "--- end of script ---")
        log("command: " + shlex.join(cmd))
        return 0
    path = sweep_dir / "gen_data.sbatch"
    path.write_text(script, encoding="utf-8")
    path.chmod(0o755)
    cmd[cmd.index("<script>")] = str(path)
    if shutil.which("sbatch") is None:
        raise RuntimeError(f"sbatch not found (no Slurm here); script written: {path}")
    log("submission: " + shlex.join(cmd))
    env = _child_env({"MILADY_ROOT": str(project_root())})
    out = subprocess.run(cmd, cwd=project_root(), env=env, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise RuntimeError(
            f"sbatch failed (code {out.returncode}): {out.stderr.strip() or out.stdout.strip()}"
        )
    job_id = out.stdout.strip().splitlines()[-1].split(";")[0].strip()
    log(
        f"array submitted: job {job_id} ({len(points)} tasks); monitor: squeue -j {job_id}; logs: {sweep_dir}"
    )
    if use_catalog:
        from milady.catalog.api import Catalog

        cat = Catalog()
        try:
            for p in points:
                log_uri = (sweep_dir / f"{_job_name(campaign)}-{job_id}_{p.index}.out").as_uri()
                cat.register_job(
                    "simulation",
                    "slurm",
                    external_id=f"{job_id}_{p.index}",
                    simulation_id=p.sim_id,
                    status="submitted",
                    log_uri=log_uri,
                )
        finally:
            cat.close()
    (sweep_dir / "slurm_job_id").write_text(job_id + "\n", encoding="utf-8")
    return 0


# =============================================================================================
# Command line
# =============================================================================================
def _print_plan(
    campaign: Campaign, points: Sequence[SweepPoint], selected: Sequence[SweepPoint], log: Any
) -> None:
    snaps, diags = output_times(campaign.runtime)
    rt = campaign.runtime
    log(
        f"campaign {campaign.name} ({campaign.code}): {len(points)} simulation(s), {len(selected)} selected"
    )
    log(
        f"  grid {campaign.shape} on {[round(L, 6) for L in campaign.lengths]}; dt ≤ {rt['dt']}, "
        f"t_burn = {rt.get('t_burn', 0)}, {len(snaps)} snapshots from {snaps[0]} to {snaps[-1]}, "
        f"{len(diags)} diagnostics, {rt.get('n_traj', 1)} trajectory(ies)"
    )
    swept = list(campaign.sweep)
    for p in selected:
        vals = ", ".join(f"{k}={p.point[k]}" for k in swept) or "(no sweep)"
        log(f"  [{p.index:4d}] {p.sim_id}  {vals}")


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point of ``python -m milady.sweep``."""
    ap = argparse.ArgumentParser(prog="python -m milady.sweep", description=__doc__.split("\n\n")[0])
    ap.add_argument("config", help="campaign YAML (infra/configs/*.yaml)")
    ap.add_argument("--scheduler", choices=["local", "docker", "slurm"], default="local")
    ap.add_argument("--dry-run", action="store_true", help="show the plan and the commands, run nothing")
    ap.add_argument(
        "--max-parallel",
        type=int,
        default=None,
        help="simultaneous simulations (local/docker: default = number of GPUs or 1; slurm: %%N of the array)",
    )
    ap.add_argument("--indices", default=None, help="subset of indices, e.g. 0,3,5-7")
    ap.add_argument("--force", action="store_true", help="also rerun already finished simulations")
    ap.add_argument(
        "--retry-running", action="store_true", help="rerun simulations left as \"running\""
    )
    ap.add_argument(
        "--no-catalog", action="store_true", help="do not use the catalog (files only)"
    )
    ap.add_argument("--register-only", action="store_true", help="register in the catalog without running")
    ap.add_argument("--device", default=None, help="passed to milady.sim.run (cpu, cuda, auto)")
    ap.add_argument(
        "--sbatch-arg",
        action="append",
        default=[],
        metavar="ARG",
        help="extra sbatch option (repeatable), e.g. --sbatch-arg=--account=abc@h100",
    )
    args = ap.parse_args(argv)

    def log(msg: str) -> None:
        print(msg, flush=True)

    campaign = load_campaign(args.config)
    points = sweep_points(campaign)
    chosen = set(parse_indices(args.indices, len(points)))
    selected = [p for p in points if p.index in chosen]
    run_args: list[str] = []
    if args.device:
        run_args += ["--device", args.device]
    if args.no_catalog:
        run_args.append("--no-catalog")

    if args.register_only:
        pending = (
            selected
            if args.no_catalog
            else register(campaign, selected, force=args.force, retry_running=args.retry_running, log=log)
        )
        print(_PENDING_TAG + json.dumps({"pending": [p.index for p in pending]}), flush=True)
        return 0

    _print_plan(campaign, points, selected, log)
    gpus = _gpu_count()
    default_par = max(1, gpus) if args.scheduler in ("local", "docker") else None
    max_parallel = args.max_parallel or campaign.resources.get("max_parallel") or default_par
    if args.scheduler in ("local", "docker"):
        max_parallel = max(1, int(max_parallel or 1))

    if args.dry_run:
        cfg_arg = _repo_relative(Path(args.config))
        log(f"--dry-run: nothing is registered or run ({args.scheduler}, max_parallel = {max_parallel})")
        if args.scheduler == "slurm":
            return run_slurm(
                campaign,
                cfg_arg,
                selected,
                sweep_dir=project_root() / "data/sweeps" / campaign.name / "<timestamp>",
                max_parallel=max_parallel,
                sbatch_args=args.sbatch_arg,
                run_args=run_args,
                dry_run=True,
                use_catalog=False,
                log=log,
            )
        for p in selected:
            cmd = _sim_command(cfg_arg, p.index, run_args)
            if args.scheduler == "docker":
                cmd = [
                    *_compose_base(),
                    "run",
                    "--rm",
                    "-T",
                    "-e",
                    "MILADY_SCHEDULER=docker",
                    _compose_worker(),
                    *cmd,
                ]
            log("  " + shlex.join(cmd))
        return 0

    if args.scheduler == "slurm" and not args.no_catalog:
        slurm_catalog_defaults(log)
    sweep_dir = _sweep_dir(campaign)
    frozen = _freeze_config(campaign, sweep_dir)
    cfg_arg = _repo_relative(frozen)
    log(f"frozen configuration: {frozen}")

    if args.scheduler == "docker":
        if args.no_catalog:
            pending_idx = [p.index for p in selected]
        else:
            pending_idx = _docker_register(cfg_arg, args, log)
        pending = [p for p in selected if p.index in set(pending_idx)]
    elif args.no_catalog:
        pending = selected
    else:
        pending = register(campaign, selected, force=args.force, retry_running=args.retry_running, log=log)
    if not pending:
        log("nothing to run: all the selected simulations are finished or running.")
        return 0
    log(f"{len(pending)} simulation(s) to run: indices {_ranges([p.index for p in pending])}")

    if args.scheduler == "slurm":
        return run_slurm(
            campaign,
            cfg_arg,
            pending,
            sweep_dir=sweep_dir,
            max_parallel=max_parallel,
            sbatch_args=args.sbatch_arg,
            run_args=run_args,
            dry_run=False,
            use_catalog=not args.no_catalog,
            log=log,
        )
    if args.scheduler == "docker":
        results = run_docker(
            campaign,
            cfg_arg,
            pending,
            max_parallel=max_parallel,
            log_dir=sweep_dir / "logs",
            run_args=run_args,
            log=log,
        )
    else:
        results = run_local(
            campaign,
            Path(cfg_arg),
            pending,
            max_parallel=max_parallel,
            log_dir=sweep_dir / "logs",
            run_args=run_args,
            use_catalog=not args.no_catalog,
            log=log,
        )
    failed = sorted(i for i, c in results.items() if c != 0)
    log(
        f"finished: {len(results) - len(failed)} succeeded, {len(failed)} failed"
        + (f" (indices {_ranges(failed)}; logs in {sweep_dir / 'logs'})" if failed else "")
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
