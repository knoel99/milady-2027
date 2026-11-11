"""Pseudo-spectral solver for 3D periodic incompressible MHD (PyTorch, CPU or GPU).

Equations solved on the periodic box [0, L)³, magnetic field in Alfvén units
(B ← B / √(μ₀ρ), same unit as the velocity):

    ∂t u = u × ω + j × B − ∇Π + ν ∇²u + f,      ∇·u = 0,   ω = ∇×u,  j = ∇×B,  Π = p + |u|²/2
    ∂t B = ∇ × (u × B) + η ∇²B,                  ∇·B = 0

Two modes:

- ``dynamic``: Navier–Stokes + induction, Lorentz force j × B; constant ABC or
  Taylor–Green (TG) forcing, white-in-time random forcing with fixed injected power, or none;
- ``kinematic``: imposed flow (ABC or TG), only the induction equation evolves (problem
  linear in B: the field is renormalized regularly, the true amplitude is tracked by
  ``log_b_rms``).

Numerical scheme:

- ``torch.fft.rfftn`` transforms on the last three axes; state = Fourier coefficients
  (n_traj, 3, nx, ny, nz//2+1); several trajectories (different seeds) advance together;
- nonlinear terms in physical space (rotational form), dealiasing by the 2/3 rule
  (cube |m_i| ≤ (n_i − 1)//3, which excludes any aliasing onto the retained modes: the quadratic
  invariants of the truncated Galerkin system — energy, magnetic and cross helicities — are
  conserved exactly by the nonlinear terms);
- integrating-factor RK4 (Lawson): the diffusion ν k², η k² is integrated exactly;
- Leray projection of u (pressure) and of B (∇·B correction, cleaning of rounding
  errors), both exact mode by mode; ∇·u and ∇·B stay at machine precision;
- random forcing: Euler–Maruyama after the deterministic step; increment Δu = √(2 ε dt) ξ with ξ
  solenoidal, band-limited to |k| ∈ [kf_min, kf_max], normalized to ⟨|ξ|²⟩ = 1: the Itô part of the injected
  energy is exactly ε dt at each step.

Diagnostics (spatial means ⟨·⟩, per trajectory, computed by Parseval): kinetic
and magnetic energies, dissipations ν⟨|ω|²⟩ and η⟨|j|²⟩, injected power ⟨u·f⟩, kinetic
⟨u·ω⟩, magnetic ⟨A·B⟩ (Coulomb gauge) and cross ⟨u·B⟩ helicities, max |∇·u| and max |∇·B|,
instantaneous magnetic growth rate γ = d ln‖B‖/dt = (⟨B·∇×(u×B)⟩ − η⟨|j|²⟩) / ⟨|B|²⟩.
Budget: d(E_u + E_B)/dt = injection − ν⟨|ω|²⟩ − η⟨|j|²⟩ (checked by tests/test_mhd3d.py).

Checkpoint: :meth:`MHD3D.save_checkpoint` / :meth:`MHD3D.load_checkpoint` (``.npz`` file
without pickle: arrays + JSON metadata), bit-for-bit resumption on the same hardware.

Performance (measured on CPU, GPU measurement method): see ``BENCHMARK_NOTES``.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import os
import time
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch

__all__ = [
    "BENCHMARK_NOTES",
    "DIAGNOSTIC_NAMES",
    "MHD3D",
    "MHD3DConfig",
    "benchmark",
    "growth_rate_fit",
    "load_npz_checkpoint",
    "resolve_device",
    "save_npz_checkpoint",
    "smoke_run",
]

#: Time per step measured on the development machine (CPU) and measurement method on GPU.
BENCHMARK_NOTES = """
Time per step measured on 2026-11-07 with ``python -m milady.sim.mhd3d bench`` (1 trajectory; one
RK4 step = 4 right-hand-side evaluations, i.e. 18 scalar 3D FFTs each in dynamic mode), on the
development machine: 4 CPU cores shared with other computations (load ≈ 4.5), torch 2.15 CPU.

                          1 thread       2 threads
    dynamic    float32    32³ : 0.014 s  0.011–0.015 s
                          64³ : 0.15 s   0.073–0.083 s
    dynamic    float64    32³ : 0.021 s  0.024 s
                          64³ : 0.31 s   0.19 s
    kinematic  float32    32³ : 0.0046 s 0.0043 s
                          64³ : 0.052 s  0.031 s

The kinematic mode costs ≈ 1/3 to 1/2 of the dynamic mode; from 32³ to 64³ the cost is multiplied by
≈ 7 to 10 (N³ log N, plus cache effects). Beware of oversubscription: with 4 threads on
these already loaded 4 cores, the step rose to ≈ 1 s (32³) and ≈ 4 s (64³). Set OMP_NUM_THREADS (or
``resources.cpus``, ``--cpus-per-task`` under Slurm) to the number of really free cores.

CPU memory (7 November 2026, torch 2.14.1 CPU, 4 threads, dynamic float32, 2 steps): peak resident
memory minus that of Python and torch after import ≈ 100 MB at 64³ and 717 MB at 128³, i.e. ≈ 15 times
the state (u, B) of 6 × N³ × 4 bytes (see infra/README.md § 6.2).

GPU: no figure is given here (no GPU on the development machine; do not extrapolate
the CPU figures). To measure on the rented VM or the Slurm node, before sizing a campaign:

    python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --dtype float32 --steps 50
    python -m milady.sim.mhd3d bench --n 64 128 --device cuda --mode kinematic --n-traj 4

(the measurement synchronizes the GPU — ``torch.cuda.synchronize()`` —, discards warm-up steps and prints
the maximum allocated memory). Duration of a simulation ≈ time per step × (t_burn + t_keep) / dt_effective
(dt_effective = min(dt, CFL step)); the catalog then records the actual duration (``wall_time_s``),
to be used to set ``resources.time`` of the following campaigns.
"""

#: Names of the series returned by :meth:`MHD3D.diagnostics` (one value per trajectory).
DIAGNOSTIC_NAMES = (
    "kinetic_energy",
    "magnetic_energy",
    "kinetic_dissipation",
    "magnetic_dissipation",
    "injection",
    "kinetic_helicity",
    "magnetic_helicity",
    "cross_helicity",
    "max_div_u",
    "max_div_b",
    "growth_rate",
    "magnetic_production",
    "u_rms",
    "b_rms",
    "log_b_rms",
)

_MODES = ("dynamic", "kinematic")
_FLOWS = ("abc", "tg")
_FORCINGS = ("abc", "tg", "random", "none")
_INITS = ("laminar", "zero", "random")


# =============================================================================================
# Configuration
# =============================================================================================
@dataclass
class MHD3DConfig:
    """Solver parameters (all quantities are dimensionless).

    Grid and numerics
        ``n``: points per direction (integer or triplet); ``length``: box size (default 2π);
        ``dealias``: 2/3 rule; ``project_every``: Leray projection of u and B every
        ``project_every`` steps (0 = never; B stays solenoidal by construction, the projection only
        removes rounding errors); ``device`` (``cpu``, ``cuda``, ``cuda:1``, ``auto``);
        ``dtype`` (``float32`` or ``float64``).
    Physics
        ``mode``: ``dynamic`` or ``kinematic``; ``nu``, ``eta``: viscosity and magnetic
        diffusivity; ``kf``: (integer) index of the mode of the imposed flow or of the ABC/TG forcing
        (physical wavenumber kf·2π/L); ``flow``: imposed flow (kinematic) ``abc`` or
        ``tg`` of amplitude ``flow_amp`` (ABC: coefficients ``abc`` = (A, B, C) × ``flow_amp``);
        ``forcing`` (dynamic): ``abc``, ``tg``, ``random`` or ``none``, of amplitude
        ``forcing_amp`` (``None``: ν |k|² × flow_amp, |k|² = k_f² for ABC and 3 k_f² for TG: laminar
        response of amplitude ``flow_amp``);
        random forcing: power ``eps`` and band ``kf_band`` = (|k|min, |k|max).
    Initial conditions
        ``u0``: ``laminar`` (shape of the forcing, amplitude ``u0_amp``), ``zero`` or ``random``
        (spectrum ∝ exp(−k²/(2 b0_kwidth²)), mean square velocity ``u0_amp``); ``u_noise``:
        random perturbation (rms) added to u0; ``b0_amp``: rms of the seed magnetic field
        (random, solenoidal, zero-mean, spectrum ∝ exp(−k²/(2 b0_kwidth²)));
        ``renormalize`` (kinematic): resets ‖B‖ to 1 every ``renorm_every`` steps and at each
        output; ``n_traj`` trajectories (seeds ``seed``, successive draws of the same generator).
    """

    n: int | tuple[int, int, int] = 32
    length: float | tuple[float, float, float] = 2 * math.pi
    mode: str = "dynamic"
    nu: float = 0.05
    eta: float = 0.05
    kf: int = 1
    flow: str = "abc"
    flow_amp: float = 1.0
    abc: tuple[float, float, float] = (1.0, 1.0, 1.0)
    forcing: str = "abc"
    forcing_amp: float | None = None
    eps: float = 0.1
    kf_band: tuple[float, float] = (1.0, 2.5)
    u0: str = "laminar"
    u0_amp: float = 1.0
    u_noise: float = 0.0
    b0_amp: float = 1e-3
    b0_kwidth: float = 2.0
    renormalize: bool = True
    renorm_every: int = 20
    project_every: int = 1
    dealias: bool = True
    n_traj: int = 1
    seed: int = 0
    device: str = "cpu"
    dtype: str = "float64"

    def __post_init__(self) -> None:
        if isinstance(self.n, int):
            self.n = (self.n, self.n, self.n)
        self.n = tuple(int(v) for v in self.n)  # type: ignore[assignment]
        if isinstance(self.length, (int, float)):
            self.length = (float(self.length),) * 3
        self.length = tuple(float(v) for v in self.length)  # type: ignore[assignment]
        self.abc = tuple(float(v) for v in self.abc)  # type: ignore[assignment]
        self.kf_band = tuple(float(v) for v in self.kf_band)  # type: ignore[assignment]
        if len(self.n) != 3 or len(self.length) != 3 or len(self.abc) != 3 or len(self.kf_band) != 2:
            raise ValueError("n, length, abc: 3 values; kf_band: 2 values")
        if min(self.n) < 8 or any(v % 2 for v in self.n):
            raise ValueError(f"n = {self.n}: even integers ≥ 8 expected")
        if self.mode not in _MODES:
            raise ValueError(f"mode {self.mode!r} unknown (expected: {_MODES})")
        if self.flow not in _FLOWS:
            raise ValueError(f"flow {self.flow!r} unknown (expected: {_FLOWS})")
        if self.forcing not in _FORCINGS:
            raise ValueError(f"forcing {self.forcing!r} unknown (expected: {_FORCINGS})")
        if self.u0 not in _INITS:
            raise ValueError(f"u0 {self.u0!r} unknown (expected: {_INITS})")
        if self.dtype not in ("float32", "float64"):
            raise ValueError("dtype: float32 or float64")
        if self.eta < 0 or self.nu < 0:
            raise ValueError("nu and eta must be non-negative")
        if self.mode == "dynamic" and self.nu <= 0:
            raise ValueError("dynamic mode: nu > 0 required")
        if int(self.kf) != self.kf or self.kf < 1:
            raise ValueError("kf: integer ≥ 1 (mode index, periodicity of the box)")
        self.kf = int(self.kf)
        if self.n_traj < 1:
            raise ValueError("n_traj ≥ 1")

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dictionary."""
        return json.loads(json.dumps(dataclasses.asdict(self)))

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> MHD3DConfig:
        """Inverse of :meth:`to_dict` (unknown keys rejected)."""
        names = {f.name for f in dataclasses.fields(cls)}
        unknown = set(d) - names
        if unknown:
            raise ValueError(f"unknown keys for MHD3DConfig: {sorted(unknown)}")
        kw = dict(d)
        for key in ("n", "length", "abc", "kf_band"):
            if isinstance(kw.get(key), list):
                kw[key] = tuple(kw[key])
        return cls(**kw)


def resolve_device(device: str | torch.device | None) -> torch.device:
    """``auto`` → ``cuda`` if a GPU is visible, otherwise ``cpu`` (MPS not supported: complex FFTs)."""
    if device is None or str(device) == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)


# =============================================================================================
# Generic checkpoints (.npz without pickle)
# =============================================================================================
def save_npz_checkpoint(
    path: str | os.PathLike[str], arrays: Mapping[str, Any], meta: Mapping[str, Any]
) -> Path:
    """Write ``arrays`` (numpy arrays) and ``meta`` (JSON) to ``path`` (.npz), atomically."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.stem}.{uuid.uuid4().hex[:8]}.part.npz")
    payload = {k: np.asarray(v) for k, v in arrays.items()}
    payload["__meta__"] = np.asarray(json.dumps(meta, ensure_ascii=False))
    try:
        np.savez(tmp, **payload)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return path


def load_npz_checkpoint(path: str | os.PathLike[str]) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    """Read back a checkpoint written by :func:`save_npz_checkpoint` → (arrays, meta)."""
    with np.load(path, allow_pickle=False) as d:
        arrays = {k: d[k] for k in d.files if k != "__meta__"}
        meta = json.loads(str(d["__meta__"])) if "__meta__" in d.files else {}
    return arrays, meta


# =============================================================================================
# Solver
# =============================================================================================
class MHD3D:
    """Pseudo-spectral 3D MHD solver (see the module docstring).

    Example ::

        cfg = MHD3DConfig(n=32, mode="kinematic", flow="abc", eta=1 / 12, b0_amp=1.0)
        sim = MHD3D(cfg)
        sim.advance_to(50.0, dt=0.05)
        print(sim.diagnostics()["growth_rate"])
    """

    def __init__(self, config: MHD3DConfig | None = None, **kwargs: Any) -> None:
        if config is not None and kwargs:
            config = dataclasses.replace(config, **kwargs)
        self.cfg = config if config is not None else MHD3DConfig(**kwargs)
        cfg = self.cfg
        self.device = resolve_device(cfg.device)
        self.rdtype = torch.float64 if cfg.dtype == "float64" else torch.float32
        self.cdtype = torch.complex128 if cfg.dtype == "float64" else torch.complex64
        self.kinematic = cfg.mode == "kinematic"
        self.shape: tuple[int, int, int] = tuple(cfg.n)  # type: ignore[assignment]
        self.lengths: tuple[float, float, float] = tuple(cfg.length)  # type: ignore[assignment]
        nx, ny, nz = self.shape
        self.n_total = nx * ny * nz
        dev, rd = self.device, self.rdtype

        # --- wavenumbers (integer indices m, k = 2π m / L) ----------------------------------
        mx = torch.fft.fftfreq(nx, 1.0 / nx, dtype=torch.float64)
        my = torch.fft.fftfreq(ny, 1.0 / ny, dtype=torch.float64)
        mz = torch.fft.rfftfreq(nz, 1.0 / nz, dtype=torch.float64)
        sx, sy, sz = (2 * math.pi / L for L in self.lengths)
        self.kx = (sx * mx).view(nx, 1, 1).to(dev, rd)
        self.ky = (sy * my).view(1, ny, 1).to(dev, rd)
        self.kz = (sz * mz).view(1, 1, -1).to(dev, rd)
        self.k2 = self.kx**2 + self.ky**2 + self.kz**2
        self.inv_k2 = torch.where(
            self.k2 > 0, 1.0 / torch.clamp(self.k2, min=1e-30), torch.zeros_like(self.k2)
        )
        self.kmax_index = tuple((n - 1) // 3 for n in self.shape)
        if cfg.dealias:
            keep = (
                (mx.abs() <= self.kmax_index[0]).view(nx, 1, 1)
                & (my.abs() <= self.kmax_index[1]).view(1, ny, 1)
                & (mz.abs() <= self.kmax_index[2]).view(1, 1, -1)
            )
        else:
            keep = torch.ones(nx, ny, mz.numel(), dtype=torch.bool)
        self.mask = keep.to(dev, rd)
        kmax_phys = [s * k for s, k in zip((sx, sy, sz), self.kmax_index)]
        self.kmax_norm = math.sqrt(sum(k * k for k in kmax_phys))
        # Parseval weights for rfftn: the planes 0 < kz < nz/2 also represent their conjugates.
        w = torch.full((mz.numel(),), 2.0, dtype=torch.float64)
        w[0] = 1.0
        if nz % 2 == 0:
            w[-1] = 1.0
        self.parseval_w = (w / self.n_total**2).view(1, 1, -1).to(dev, rd)

        # --- physical grid, imposed flow or forcing ----------------------------------------
        axes = [torch.arange(n, dtype=torch.float64) * (L / n) for n, L in zip(self.shape, self.lengths)]
        self.coords = {name: a.numpy().copy() for name, a in zip("xyz", axes)}
        X, Y, Z = torch.meshgrid(*axes, indexing="ij")
        kf_phys = [s * cfg.kf for s in (sx, sy, sz)]
        self.kf_phys = float(sx * cfg.kf)
        shape_abc = self._abc_field(X, Y, Z, kf_phys, cfg.abc)
        shape_tg = self._tg_field(X, Y, Z, kf_phys)
        self.forcing_amp = 0.0
        self.f_phys: torch.Tensor | None = None
        self.f_hat: torch.Tensor | None = None
        self.u_imp: torch.Tensor | None = None
        self.uh_imp: torch.Tensor | None = None
        if self.kinematic:
            base = shape_abc if cfg.flow == "abc" else shape_tg
            self.u_imp = (cfg.flow_amp * base).to(dev, rd)
            self.uh_imp = self._fft(self.u_imp) * self.mask
        elif cfg.forcing in ("abc", "tg"):
            base = shape_abc if cfg.forcing == "abc" else shape_tg
            # "Laminar" amplitude: the Stokes response −ν∇²u = f has amplitude flow_amp
            # (−∇² of the shape: k_f² for ABC, 3 k_f² for TG).
            lap = self.kf_phys**2 * (1.0 if cfg.forcing == "abc" else 3.0)
            amp = cfg.forcing_amp if cfg.forcing_amp is not None else cfg.nu * lap * cfg.flow_amp
            self.forcing_amp = float(amp)
            self.f_phys = (amp * base).to(dev, rd)
            self.f_hat = self._project(self._fft(self.f_phys) * self.mask)
        # "Laminar" shape of u0: that of the constant forcing, otherwise that of ``flow``.
        lam = cfg.forcing if cfg.forcing in _FLOWS else cfg.flow
        self._laminar_shape = (shape_abc if lam == "abc" else shape_tg).to(dev, rd)
        if cfg.forcing == "random":
            kk = torch.sqrt(self.k2)
            self.band = ((kk >= cfg.kf_band[0]) & (kk <= cfg.kf_band[1])).to(rd) * self.mask
            if float(self.band.sum()) == 0:
                raise ValueError(f"forcing band {cfg.kf_band} empty for the grid {self.shape}")

        # --- state --------------------------------------------------------------------------
        self.generator = torch.Generator(device=self.device)
        self.generator.manual_seed(int(cfg.seed))
        self.t = 0.0
        self.step_count = 0
        self.log_b = np.zeros(cfg.n_traj, dtype=np.float64)  # cumulative renormalizations (kinematic)
        self.inj_acc = np.zeros(cfg.n_traj, dtype=np.float64)  # injected energy (random forcing)
        self.inj_t0 = 0.0
        self._factors_cache: tuple[float, tuple[torch.Tensor, ...]] | None = None
        self.uh: torch.Tensor | None = None
        self.bh = self._initial_b()
        if not self.kinematic:
            self.uh = self._initial_u()
        elif cfg.renormalize:
            self.renormalize()

    # -----------------------------------------------------------------------------------------
    # Analytical fields
    # -----------------------------------------------------------------------------------------
    @staticmethod
    def _abc_field(
        X: torch.Tensor, Y: torch.Tensor, Z: torch.Tensor, k: Sequence[float], abc: Sequence[float]
    ) -> torch.Tensor:
        """ABC: (A sin kz + C cos ky, B sin kx + A cos kz, C sin ky + B cos kx); ∇×u = k u (Beltrami)."""
        A, B, C = abc
        kx, ky, kz = k
        return torch.stack(
            (
                A * torch.sin(kz * Z) + C * torch.cos(ky * Y),
                B * torch.sin(kx * X) + A * torch.cos(kz * Z),
                C * torch.sin(ky * Y) + B * torch.cos(kx * X),
            )
        )

    @staticmethod
    def _tg_field(X: torch.Tensor, Y: torch.Tensor, Z: torch.Tensor, k: Sequence[float]) -> torch.Tensor:
        """Taylor–Green: (sin kx cos ky cos kz, −cos kx sin ky cos kz, 0), divergence-free."""
        kx, ky, kz = k
        return torch.stack(
            (
                torch.sin(kx * X) * torch.cos(ky * Y) * torch.cos(kz * Z),
                -torch.cos(kx * X) * torch.sin(ky * Y) * torch.cos(kz * Z),
                torch.zeros_like(X),
            )
        )

    # -----------------------------------------------------------------------------------------
    # Spectral tools
    # -----------------------------------------------------------------------------------------
    def _fft(self, v: torch.Tensor) -> torch.Tensor:
        return torch.fft.rfftn(v, dim=(-3, -2, -1))

    def _ifft(self, vh: torch.Tensor) -> torch.Tensor:
        return torch.fft.irfftn(vh, s=self.shape, dim=(-3, -2, -1))

    def _curl(self, vh: torch.Tensor) -> torch.Tensor:
        """i k × v̂ (curl in Fourier space); components on axis −4."""
        vx, vy, vz = vh.unbind(-4)
        return 1j * torch.stack(
            (self.ky * vz - self.kz * vy, self.kz * vx - self.kx * vz, self.kx * vy - self.ky * vx), dim=-4
        )

    def _div(self, vh: torch.Tensor) -> torch.Tensor:
        vx, vy, vz = vh.unbind(-4)
        return 1j * (self.kx * vx + self.ky * vy + self.kz * vz)

    def _project(self, vh: torch.Tensor) -> torch.Tensor:
        """Leray projection v̂ − k (k·v̂)/k² (solenoidal part, mode by mode)."""
        vx, vy, vz = vh.unbind(-4)
        d = (self.kx * vx + self.ky * vy + self.kz * vz) * self.inv_k2
        return torch.stack((vx - self.kx * d, vy - self.ky * d, vz - self.kz * d), dim=-4)

    @staticmethod
    def _cross(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        ax, ay, az = a.unbind(-4)
        bx, by, bz = b.unbind(-4)
        return torch.stack((ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx), dim=-4)

    def _inner(self, ah: torch.Tensor, bh: torch.Tensor) -> np.ndarray:
        """⟨a·b⟩ (spatial mean) per trajectory, by Parseval on the rfftn coefficients."""
        prod = (ah * bh.conj()).real.sum(dim=-4)  # sum over the components
        val = (prod * self.parseval_w).sum(dim=(-3, -2, -1))
        return np.atleast_1d(val.detach().to("cpu", torch.float64).numpy()).copy()

    def _random_solenoidal(self, weight: torch.Tensor, rms: float) -> torch.Tensor:
        """Zero-mean solenoidal random field, filtered by ``weight`` (spectrum), imposed rms."""
        noise = torch.randn(
            (self.cfg.n_traj, 3, *self.shape), generator=self.generator, device=self.device, dtype=self.rdtype
        )
        vh = self._project(self._fft(noise) * weight * self.mask)
        vh[..., 0, 0, 0] = 0
        norm = torch.sqrt(torch.as_tensor(self._inner(vh, vh), device=self.device, dtype=self.rdtype))
        return vh * (rms / torch.clamp(norm, min=1e-300)).view(-1, 1, 1, 1, 1)

    def _initial_b(self) -> torch.Tensor:
        width = self.cfg.b0_kwidth
        spectrum = torch.exp(-self.k2 / (2 * width * width))
        return self._random_solenoidal(spectrum, self.cfg.b0_amp)

    def _initial_u(self) -> torch.Tensor:
        cfg = self.cfg
        if cfg.u0 == "zero":
            uh = torch.zeros((cfg.n_traj, 3, *self.k2.shape), device=self.device, dtype=self.cdtype)
        elif cfg.u0 == "laminar":
            base = self._project(self._fft(self._laminar_shape) * self.mask)
            uh = (cfg.u0_amp * base).unsqueeze(0).repeat(cfg.n_traj, 1, 1, 1, 1)
        else:
            spectrum = torch.exp(-self.k2 / (2 * cfg.b0_kwidth**2))
            uh = self._random_solenoidal(spectrum, cfg.u0_amp)
        if cfg.u_noise > 0:
            spectrum = torch.exp(-self.k2 / (2 * cfg.b0_kwidth**2))
            uh = uh + self._random_solenoidal(spectrum, cfg.u_noise)
        uh[..., 0, 0, 0] = 0
        return uh

    # -----------------------------------------------------------------------------------------
    # Dynamics
    # -----------------------------------------------------------------------------------------
    def _rhs(self, uh: torch.Tensor | None, bh: torch.Tensor) -> tuple[torch.Tensor | None, torch.Tensor]:
        """Nonlinear right-hand sides (and constant forcing) in Fourier space, dealiased."""
        b = self._ifft(bh)
        if self.kinematic:
            assert self.u_imp is not None
            e = self._cross(self.u_imp, b)
            nu_h = None
        else:
            assert uh is not None
            u = self._ifft(uh)
            w = self._ifft(self._curl(uh))
            j = self._ifft(self._curl(bh))
            nu_h = self._project(self._fft(self._cross(u, w) + self._cross(j, b)) * self.mask)
            if self.f_hat is not None:
                nu_h = nu_h + self.f_hat
            nu_h[..., 0, 0, 0] = 0
            e = self._cross(u, b)
        nb_h = self._curl(self._fft(e) * self.mask)
        return nu_h, nb_h

    def _factors(self, dt: float) -> tuple[torch.Tensor, ...]:
        """Integrating factors exp(−ν k² dt), exp(−ν k² dt/2), exp(−η k² dt), exp(−η k² dt/2)."""
        if self._factors_cache is not None and self._factors_cache[0] == dt:
            return self._factors_cache[1]
        k2 = self.k2
        out = (
            torch.exp(-self.cfg.nu * k2 * dt),
            torch.exp(-self.cfg.nu * k2 * dt / 2),
            torch.exp(-self.cfg.eta * k2 * dt),
            torch.exp(-self.cfg.eta * k2 * dt / 2),
        )
        self._factors_cache = (dt, out)
        return out

    def step(self, dt: float) -> None:
        """Advance by one step ``dt``: Lawson RK4 (integrating factor), then random forcing and projections."""
        Eu, Eu2, Eb, Eb2 = self._factors(dt)
        b0 = self.bh
        if self.kinematic:
            _, k1 = self._rhs(None, b0)
            _, k2 = self._rhs(None, Eb2 * (b0 + 0.5 * dt * k1))
            _, k3 = self._rhs(None, Eb2 * b0 + 0.5 * dt * k2)
            _, k4 = self._rhs(None, Eb * b0 + dt * Eb2 * k3)
            self.bh = Eb * b0 + (dt / 6) * (Eb * k1 + 2 * Eb2 * (k2 + k3) + k4)
        else:
            u0 = self.uh
            assert u0 is not None
            k1u, k1b = self._rhs(u0, b0)
            assert k1u is not None
            k2u, k2b = self._rhs(Eu2 * (u0 + 0.5 * dt * k1u), Eb2 * (b0 + 0.5 * dt * k1b))
            assert k2u is not None
            k3u, k3b = self._rhs(Eu2 * u0 + 0.5 * dt * k2u, Eb2 * b0 + 0.5 * dt * k2b)
            assert k3u is not None
            k4u, k4b = self._rhs(Eu * u0 + dt * Eu2 * k3u, Eb * b0 + dt * Eb2 * k3b)
            assert k4u is not None
            self.uh = Eu * u0 + (dt / 6) * (Eu * k1u + 2 * Eu2 * (k2u + k3u) + k4u)
            self.bh = Eb * b0 + (dt / 6) * (Eb * k1b + 2 * Eb2 * (k2b + k3b) + k4b)
            if self.cfg.forcing == "random":
                self._random_kick(dt)
        self.step_count += 1
        self.t += dt
        pe = self.cfg.project_every
        if pe and self.step_count % pe == 0:
            self.bh = self._project(self.bh)
            if self.uh is not None:
                self.uh = self._project(self.uh)
        if self.kinematic and self.cfg.renormalize and self.step_count % max(1, self.cfg.renorm_every) == 0:
            self.renormalize()

    def _random_kick(self, dt: float) -> None:
        """White forcing: u ← u + √(2 ε dt) ξ, ⟨|ξ|²⟩ = 1; accumulates the realized injected energy."""
        assert self.uh is not None
        amp = math.sqrt(2.0 * self.cfg.eps * dt)
        du = self._random_solenoidal(self.band, amp)
        # ΔE = ⟨u·Δu⟩ + ½⟨|Δu|²⟩; the second term equals exactly ε dt by construction.
        self.inj_acc += self._inner(self.uh, du) + 0.5 * self._inner(du, du)
        self.uh = self.uh + du

    def renormalize(self) -> None:
        """Bring ‖B‖ (rms) back to 1 per trajectory and accumulate ln‖B‖ in ``log_b`` (linear problem)."""
        rms = np.sqrt(np.maximum(self._inner(self.bh, self.bh), 1e-300))
        self.log_b += np.log(rms)
        scale = torch.as_tensor(1.0 / rms, device=self.device, dtype=self.rdtype).view(-1, 1, 1, 1, 1)
        self.bh = self.bh * scale

    def max_speed(self) -> float:
        """max |u| + max |B| on the grid (all trajectories): reference velocity of the CFL."""
        vmax = 0.0
        if self.kinematic:
            assert self.u_imp is not None
            vmax += float(torch.linalg.vector_norm(self.u_imp, dim=0).max())
            return vmax
        assert self.uh is not None
        vmax += float(torch.linalg.vector_norm(self._ifft(self.uh), dim=-4).max())
        vmax += float(torch.linalg.vector_norm(self._ifft(self.bh), dim=-4).max())
        return vmax

    def cfl_dt(self, cfl: float) -> float:
        """Time step such that dt (max|u| + max|B|) |k|max = cfl (RK4 stability: cfl ≲ 2.8)."""
        speed = self.max_speed()
        return math.inf if speed <= 0 else cfl / (speed * self.kmax_norm)

    def advance_to(self, t_target: float, dt: float, cfl: float | None = None) -> int:
        """Advance to exactly ``t_target``, with steps ≤ ``dt`` (and ≤ CFL step if ``cfl``).

        The step is constant over the interval (integer number of steps): the output times are
        reached exactly. Returns the number of steps taken; raises ``FloatingPointError`` if
        the state ceases to be finite (numerical instability: reduce ``dt`` or ``cfl``).
        """
        remaining = float(t_target) - self.t
        if remaining <= 1e-12 * max(1.0, abs(t_target)):
            return 0
        h_max = float(dt)
        if cfl is not None and cfl > 0:
            h_max = min(h_max, self.cfl_dt(cfl))
        n_sub = max(1, math.ceil(remaining / h_max - 1e-9))
        h = remaining / n_sub
        for _ in range(n_sub):
            self.step(h)
        self.t = float(t_target)
        if self.kinematic and self.cfg.renormalize:
            self.renormalize()
        if not self.is_finite():
            raise FloatingPointError(
                f"non-finite state at t = {self.t:.4g} (step {h:.3g}): reduce dt or cfl, or increase the resolution"
            )
        return n_sub

    def is_finite(self) -> bool:
        """True if all coefficients are finite."""
        ok = bool(torch.isfinite(torch.view_as_real(self.bh)).all())
        if self.uh is not None:
            ok = ok and bool(torch.isfinite(torch.view_as_real(self.uh)).all())
        return ok

    # -----------------------------------------------------------------------------------------
    # Diagnostics and outputs
    # -----------------------------------------------------------------------------------------
    @property
    def velocity_hat(self) -> torch.Tensor:
        """û (n_traj, 3, nx, ny, nz//2+1); in kinematic mode, the imposed flow repeated."""
        if self.kinematic:
            assert self.uh_imp is not None
            return self.uh_imp.unsqueeze(0).expand(self.cfg.n_traj, -1, -1, -1, -1)
        assert self.uh is not None
        return self.uh

    @torch.no_grad()
    def diagnostics(self, reset_injection: bool = True) -> dict[str, np.ndarray]:
        """Instantaneous diagnostics per trajectory (numpy float64 arrays of shape (n_traj,)).

        ``injection``: instantaneous ⟨u·f⟩ (constant forcing) or, for random forcing, mean power
        actually injected since the previous call (reset to zero if ``reset_injection``).
        ``growth_rate``: instantaneous d ln‖B‖/dt (exact, deduced from the induction equation).
        """
        cfg = self.cfg
        uh, bh = self.velocity_hat, self.bh
        wh, jh = self._curl(uh), self._curl(bh)
        ah = jh * self.inv_k2  # vector potential in Coulomb gauge: Â = i k × B̂ / k²
        eu = 0.5 * self._inner(uh, uh)
        b2 = self._inner(bh, bh)
        eb = 0.5 * b2
        j2 = self._inner(jh, jh)
        _, ind = self._rhs(None if self.kinematic else uh, bh)
        production = self._inner(bh, ind)  # ⟨B·∇×(u×B)⟩
        out: dict[str, np.ndarray] = {
            "kinetic_energy": eu,
            "magnetic_energy": eb,
            "kinetic_dissipation": cfg.nu * self._inner(wh, wh),
            "magnetic_dissipation": cfg.eta * j2,
            "kinetic_helicity": self._inner(uh, wh),
            "magnetic_helicity": self._inner(ah, bh),
            "cross_helicity": self._inner(uh, bh),
            "max_div_u": self._max_abs(self._div(uh)),
            "max_div_b": self._max_abs(self._div(bh)),
            "growth_rate": (production - cfg.eta * j2) / np.maximum(b2, 1e-300),
            "magnetic_production": production,
            "u_rms": np.sqrt(2 * eu),
            "b_rms": np.sqrt(b2),
            "log_b_rms": self.log_b + 0.5 * np.log(np.maximum(b2, 1e-300)),
        }
        if self.kinematic or cfg.forcing == "none":
            out["injection"] = np.zeros(cfg.n_traj)
        elif cfg.forcing == "random":
            elapsed = self.t - self.inj_t0
            out["injection"] = self.inj_acc / elapsed if elapsed > 0 else np.full(cfg.n_traj, cfg.eps)
            if reset_injection:
                self.inj_acc = np.zeros(cfg.n_traj)
                self.inj_t0 = self.t
        else:
            assert self.f_hat is not None
            out["injection"] = self._inner(uh, self.f_hat)
        return {k: np.asarray(out[k], dtype=np.float64) for k in DIAGNOSTIC_NAMES}

    def _max_abs(self, sh: torch.Tensor) -> np.ndarray:
        phys = self._ifft(sh)
        return phys.abs().amax(dim=(-3, -2, -1)).detach().to("cpu", torch.float64).numpy().reshape(-1).copy()

    @torch.no_grad()
    def fields(self, dtype: Any = np.float32) -> dict[str, np.ndarray]:
        """Physical fields ``velocity`` and ``magnetic_field`` of shape (n_traj, nx, ny, nz, 3)."""

        def conv(vh: torch.Tensor) -> np.ndarray:
            v = self._ifft(vh).permute(0, 2, 3, 4, 1).contiguous()
            return v.to("cpu").numpy().astype(dtype, copy=False)

        return {"velocity": conv(self.velocity_hat), "magnetic_field": conv(self.bh)}

    @torch.no_grad()
    def energy_spectra(self) -> dict[str, np.ndarray]:
        """Shell spectra E_u(k), E_B(k) (k integer = rounded |m|), shape (n_traj, k_max + 1)."""
        mx = torch.fft.fftfreq(self.shape[0], 1.0 / self.shape[0], dtype=torch.float64).view(-1, 1, 1)
        my = torch.fft.fftfreq(self.shape[1], 1.0 / self.shape[1], dtype=torch.float64).view(1, -1, 1)
        mz = torch.fft.rfftfreq(self.shape[2], 1.0 / self.shape[2], dtype=torch.float64).view(1, 1, -1)
        shell = torch.round(torch.sqrt(mx**2 + my**2 + mz**2)).long().to(self.device)
        nshell = int(shell.max()) + 1
        out = {}
        for name, vh in (("kinetic", self.velocity_hat), ("magnetic", self.bh)):
            dens = 0.5 * ((vh * vh.conj()).real.sum(dim=1) * self.parseval_w)
            spec = torch.zeros((dens.shape[0], nshell), dtype=dens.dtype, device=self.device)
            spec.index_add_(1, shell.reshape(-1), dens.reshape(dens.shape[0], -1))
            out[name] = spec.to("cpu", torch.float64).numpy()
        return out

    # -----------------------------------------------------------------------------------------
    # Checkpoints
    # -----------------------------------------------------------------------------------------
    def state_dict(self) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        """Full state → (numpy arrays, JSON metadata)."""
        arrays: dict[str, np.ndarray] = {
            "bh": self.bh.detach().cpu().numpy(),
            "log_b": self.log_b.copy(),
            "inj_acc": self.inj_acc.copy(),
            "rng_state": self.generator.get_state().cpu().numpy(),
        }
        if self.uh is not None:
            arrays["uh"] = self.uh.detach().cpu().numpy()
        meta = {
            "config": self.cfg.to_dict(),
            "t": self.t,
            "step_count": self.step_count,
            "inj_t0": self.inj_t0,
            "rng_device": self.device.type,
            "torch_version": torch.__version__,
        }
        return arrays, meta

    def load_state_dict(self, arrays: Mapping[str, np.ndarray], meta: Mapping[str, Any]) -> None:
        """Restore a state produced by :meth:`state_dict` (same physical configuration)."""
        self.bh = torch.as_tensor(np.asarray(arrays["bh"]), device=self.device).to(self.cdtype)
        if not self.kinematic:
            self.uh = torch.as_tensor(np.asarray(arrays["uh"]), device=self.device).to(self.cdtype)
        self.log_b = np.asarray(arrays["log_b"], dtype=np.float64).copy()
        self.inj_acc = np.asarray(arrays["inj_acc"], dtype=np.float64).copy()
        self.t = float(meta["t"])
        self.step_count = int(meta["step_count"])
        self.inj_t0 = float(meta.get("inj_t0", 0.0))
        if meta.get("rng_device") == self.device.type:
            self.generator.set_state(torch.as_tensor(np.asarray(arrays["rng_state"]), dtype=torch.uint8))
        else:  # state of another generator type: derived deterministic seed
            self.generator.manual_seed(int(self.cfg.seed) * 1_000_003 + self.step_count)
        self._factors_cache = None

    def save_checkpoint(
        self,
        path: str | os.PathLike[str],
        extra: Mapping[str, np.ndarray] | None = None,
        extra_meta: Mapping[str, Any] | None = None,
    ) -> Path:
        """Write the state (and ``extra`` arrays prefixed ``extra/``) to an atomic ``.npz`` file."""
        arrays, meta = self.state_dict()
        arrays = {f"solver/{k}": v for k, v in arrays.items()}
        for k, v in (extra or {}).items():
            arrays[f"extra/{k}"] = np.asarray(v)
        return save_npz_checkpoint(path, arrays, {"solver": meta, "extra": dict(extra_meta or {})})

    @classmethod
    def load_checkpoint(
        cls, path: str | os.PathLike[str], device: str | None = None, dtype: str | None = None
    ) -> tuple[MHD3D, dict[str, np.ndarray], dict[str, Any]]:
        """Recreate the solver from a checkpoint → (solver, ``extra`` arrays, ``extra`` meta)."""
        arrays, meta = load_npz_checkpoint(path)
        cfg = MHD3DConfig.from_dict(meta["solver"]["config"])
        changes: dict[str, Any] = {}
        if device is not None:
            changes["device"] = device
        if dtype is not None:
            changes["dtype"] = dtype
        if changes:
            cfg = dataclasses.replace(cfg, **changes)
        sim = cls(cfg)
        solver_arrays = {k.split("/", 1)[1]: v for k, v in arrays.items() if k.startswith("solver/")}
        sim.load_state_dict(solver_arrays, meta["solver"])
        extra = {k.split("/", 1)[1]: v for k, v in arrays.items() if k.startswith("extra/")}
        return sim, extra, dict(meta.get("extra", {}))


# =============================================================================================
# Utilities
# =============================================================================================
def growth_rate_fit(
    t: Sequence[float] | np.ndarray, log_amp: Sequence[float] | np.ndarray, t_min: float | None = None
) -> float:
    """Slope of a linear regression of ln‖B‖ against t (over t ≥ ``t_min``): growth rate λ."""
    t = np.asarray(t, dtype=np.float64)
    y = np.asarray(log_amp, dtype=np.float64)
    sel = np.isfinite(y) & (t >= (t_min if t_min is not None else -np.inf))
    if sel.sum() < 2:
        return float("nan")
    return float(np.polyfit(t[sel], y[sel], 1)[0])


def benchmark(
    n: int,
    steps: int = 10,
    device: str = "cpu",
    dtype: str = "float32",
    mode: str = "dynamic",
    n_traj: int = 1,
    warmup: int = 2,
) -> dict[str, Any]:
    """Measure the mean time per step (s) at resolution n³; synchronizes the GPU if applicable."""
    dev = resolve_device(device)
    cfg = MHD3DConfig(
        n=n,
        mode=mode,
        nu=0.01,
        eta=0.01,
        forcing="tg",
        kf=2,
        b0_amp=0.1,
        n_traj=n_traj,
        device=str(dev),
        dtype=dtype,
    )
    sim = MHD3D(cfg)
    sync = torch.cuda.synchronize if dev.type == "cuda" else (lambda: None)
    if dev.type == "cuda":
        torch.cuda.reset_peak_memory_stats(dev)
    for _ in range(warmup):
        sim.step(1e-3)
    sync()
    t0 = time.perf_counter()
    for _ in range(steps):
        sim.step(1e-3)
    sync()
    sec = (time.perf_counter() - t0) / steps
    info: dict[str, Any] = {
        "n": n,
        "mode": mode,
        "dtype": dtype,
        "device": str(dev),
        "n_traj": n_traj,
        "seconds_per_step": sec,
        "threads": torch.get_num_threads(),
    }
    if dev.type == "cuda":
        info["max_memory_gb"] = torch.cuda.max_memory_allocated(dev) / 2**30
        info["gpu"] = torch.cuda.get_device_name(dev)
    return info


def smoke_run(n: int = 16, n_t: int = 3, device: str = "cpu") -> dict[str, Any]:
    """Tiny simulation (dynamic, ABC forcing) for ``infra/deploy/smoke.py``.

    Returns ``{"fields", "coords", "diagnostics", "params", "code"}`` in the format expected by
    :func:`milady.data.format.write_mff` (one trajectory, ``n_t`` snapshots spaced by 0.1).
    """
    cfg = MHD3DConfig(
        n=n,
        mode="dynamic",
        nu=0.05,
        eta=0.05,
        forcing="abc",
        u0="laminar",
        u_noise=0.05,
        b0_amp=0.1,
        device=device,
        dtype="float32",
        seed=0,
    )
    sim = MHD3D(cfg)
    times, snaps_u, snaps_b, diags = [], [], [], []
    for k in range(n_t):
        sim.advance_to(0.1 * k, dt=0.02)
        times.append(sim.t)
        f = sim.fields()
        snaps_u.append(f["velocity"])
        snaps_b.append(f["magnetic_field"])
        diags.append(sim.diagnostics())
    diag = {name: np.array([d[name][0] for d in diags]) for name in DIAGNOSTIC_NAMES}
    return {
        "fields": {"velocity": np.stack(snaps_u, 1), "magnetic_field": np.stack(snaps_b, 1)},
        "coords": {"time": np.asarray(times), **sim.coords},
        "diagnostics": diag,
        "params": {
            "nu": cfg.nu,
            "eta": cfg.eta,
            "Re": 1 / cfg.nu,
            "Rm": 1 / cfg.eta,
            "Pm": cfg.nu / cfg.eta,
            "kf": float(cfg.kf),
            "forcing_amp": sim.forcing_amp,
        },
        "code": "mhd3d_torch",
    }


# =============================================================================================
# Command line: performance measurement and quick test
# =============================================================================================
def _main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m milady.sim.mhd3d", description="3D MHD solver: tools.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bench", help="time per step at different resolutions")
    b.add_argument("--n", type=int, nargs="+", default=[32, 64])
    b.add_argument("--steps", type=int, default=10)
    b.add_argument("--device", default="auto")
    b.add_argument("--dtype", default="float32", choices=["float32", "float64"])
    b.add_argument("--mode", default="dynamic", choices=list(_MODES))
    b.add_argument("--n-traj", type=int, default=1)
    b.add_argument("--threads", type=int, default=None, help="torch CPU threads (default: torch setting)")
    g = sub.add_parser("growth", help="kinematic ABC growth rate for a few Rm")
    g.add_argument("--rm", type=float, nargs="+", default=[6.0, 12.0])
    g.add_argument("--n", type=int, default=24)
    g.add_argument("--t", type=float, default=60.0)
    g.add_argument("--dt", type=float, default=0.05)
    g.add_argument("--device", default="auto")
    args = ap.parse_args(argv)
    if args.cmd == "bench":
        if args.threads:
            torch.set_num_threads(args.threads)
        for n in args.n:
            info = benchmark(
                n, steps=args.steps, device=args.device, dtype=args.dtype, mode=args.mode, n_traj=args.n_traj
            )
            print(json.dumps(info), flush=True)
        return 0
    for rm in args.rm:
        sim = MHD3D(
            MHD3DConfig(
                n=args.n,
                mode="kinematic",
                flow="abc",
                eta=1.0 / rm,
                b0_amp=1.0,
                device=args.device,
                dtype="float64",
            )
        )
        ts, logs = [], []
        while sim.t < args.t - 1e-9:
            sim.advance_to(sim.t + 1.0, dt=args.dt)
            ts.append(sim.t)
            logs.append(float(sim.diagnostics()["log_b_rms"][0]))
        lam = growth_rate_fit(ts, logs, t_min=args.t / 2)
        print(json.dumps({"Rm": rm, "n": args.n, "lambda": lam}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
