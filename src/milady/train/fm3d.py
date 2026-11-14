"""Conditional flow matching of 3D MHD fields (u, B) under hard physical constraints — stage 2 of the thesis.

Model (takes up E2, variant V4/V5, and E1, fine-tuning, in 3D):

- **representation**: vector potentials A_u, A_B in Coulomb gauge, truncated Fourier coefficients
  |m| ≤ kmax in the Craya–Herring basis, normalized per mode (``milady.train.data``);
- **hard constraint**: decoding u = ∇×A_u, B = ∇×A_B in Fourier space, zero divergence by construction;
- **B → −B symmetry** (optional): equivariant symmetrization v(x) = ½ (v(x) + S v(S x)) with
  S: A_B → −A_B; the generated distribution is then exactly invariant (symmetric Gaussian noise);
- **flow matching**: linear path x_t = (1 − t) x₀ + t x₁, target x₁ − x₀, conditioning on normalized
  parameters (log Re, log Pm, log Rm…); sampling by the Heun scheme;
- **stationarity loss** (optional): at conditions drawn over the whole range (including between the
  training values), differentiable sampling (Heun with a few steps) then penalty on the mean energy
  budget E[injection − dissipation] (or on the kinetic / magnetic budgets), estimated **without bias**
  by the product of the means of two half-batches (the square of a single mean would penalize the variance);
- **networks**: residual MLP with adaLN modulation, or light transformer (DiT) on mode tokens;
- **compute**: single process or DDP (``torchrun``), optional bf16 on GPU, local or S3 checkpoints
  (``milady.storage``), automatic resumption (Slurm: same ``SLURM_JOB_ID`` after requeue), MLflow log if
  ``MLFLOW_TRACKING_URI`` is defined (otherwise ``metrics.jsonl``), model, task and evaluations in the catalog.

Usage ::

    python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml \\
        [--dataset NAME[:VERSION] | --files URI…]
    torchrun --standalone --nproc-per-node=4 -m milady.train.fm3d --config infra/configs/train_fm3d.yaml
    # fine-tuning with the stationarity loss, from a trained model:
    python -m milady.train.fm3d --config … --init-from s3://milady-models/…/final.pt \\
        --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 \\
              train.iters=2000 train.lr=1e-4
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as _dt
import json
import logging
import math
import os
import re
import signal
import socket
import sys
import tempfile
import time
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Self

import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch import nn

from milady import __version__, git_commit, project_root, storage
from milady.train.data import (
    CondSpec,
    EpochSampler,
    FourierPotentialSpace,
    build_data,
    param_value,
    physical_parameters,
    resolve_uris,
)
from milady.train.flow import FourierEmbedding, fm_loss, heun_sample

__all__ = [
    "DEFAULT_CONFIG",
    "FlowMatchingLoss",
    "GenerativeModel",
    "ModeTransformer",
    "ResMLP",
    "SignSymmetrized",
    "apply_overrides",
    "build_field",
    "default_config",
    "fm_loss",
    "heun_sample",
    "latest_model_id",
    "load_checkpoint",
    "load_config",
    "load_model",
    "main",
    "smoke_step",
    "train",
]

LOG = logging.getLogger("milady.train")
_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$")

# =============================================================================================
# Configuration
# =============================================================================================
#: Default values; the YAML (``infra/configs/train_fm3d.yaml``) only needs to specify the differences.
DEFAULT_CONFIG: dict[str, Any] = {
    "name": "fm3d",
    "description": "",
    "data": {
        "dataset": None,
        "version": None,
        "campaign": None,
        "auto_dataset": {"val": [], "test": []},
        "files": [],
        "val_files": [],
        "test_files": [],
        "fields": ["velocity", "magnetic_field"],
        "kmax": 8,
        "conditioning": [],
        "t_min": None,
        "stride": 1,
        "max_snapshots_per_file": None,
        "read_chunk": 8,
        "cache_dir": "${MILADY_CACHE_DIR:-/tmp/milady-cache}",
        "on_device": True,
    },
    "model": {
        "architecture": "mlp",
        "symmetry_b_sign": True,
        "mlp": {"width": 1024, "depth": 6, "expansion": 2, "emb_dim": 256, "n_freq": 16, "dropout": 0.0},
        "transformer": {
            "d_model": 192,
            "depth": 6,
            "heads": 6,
            "mlp_ratio": 4,
            "modes_per_token": 4,
            "emb_dim": 256,
            "n_freq": 16,
            "dropout": 0.0,
        },
    },
    "train": {
        "iters": None,
        "epochs": 100,
        "batch_size": 64,
        "lr": 3e-4,
        "lr_min": 1e-5,
        "warmup": 200,
        "weight_decay": 0.0,
        "grad_clip": 1.0,
        "ema": 0.999,
        "precision": "auto",
        "seed": 0,
        "log_every": 50,
        "val_every": 500,
        "ckpt_every": 1000,
        "augment_b_sign": False,
        "t_sampling": "uniform",
        "device": "auto",
        "num_threads": None,
        "init_from": None,
        "resume": "auto",
        "workdir": "${MILADY_RUN_DIR:-data/runs}",
    },
    "stationarity": {
        "enabled": False,
        "beta": 10.0,
        "start_iter": 0,
        "every": 1,
        "n_cond": 4,
        "n_per": 16,
        "steps": 8,
        "balance": "total",
        "injection": "forcing",
        "injection_param": "eps",
        "growth_rate": 0.0,
        "cond_range": [0.0, 1.0],
        # Fine-tuning safeguards (experiment E1: the loss alone can diverge from a biased model):
        "anchor": 0.0,       # weight of the anchoring to the starting weights: anchor × mean of (θ − θ₀)²
        "beta_warmup": 0,    # linear ramp-up of beta over this number of active iterations (0: beta right away)
    },
    "sampling": {"steps": 50},
    "checkpoint": {"uri": None},
    "mlflow": {"experiment": "milady-fm3d", "log_checkpoint": False},
    "catalog": {"enabled": True, "url": None, "required": False},
    "eval": {
        "after_train": True,
        "points": [],
        "n_samples": 32,
        "seed": 0,
        "steps": 50,
        "grid": None,
        "batch_size": 16,
        "n_ref": 128,
        "max_points": 6,
    },
}

_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def _expand_env(obj: Any) -> Any:
    """Expand ``${VAR}`` and ``${VAR:-default}`` in strings (recursive)."""
    if isinstance(obj, str):
        return _ENV_RE.sub(lambda m: os.environ.get(m.group(1)) or (m.group(2) or ""), obj)
    if isinstance(obj, list):
        return [_expand_env(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _expand_env(v) for k, v in obj.items()}
    return obj


def _merge(base: dict[str, Any], over: Mapping[str, Any]) -> dict[str, Any]:
    for key, val in over.items():
        if isinstance(val, Mapping) and isinstance(base.get(key), dict):
            _merge(base[key], val)
        else:
            base[key] = copy.deepcopy(val)
    return base


def default_config() -> dict[str, Any]:
    """Copy of the default configuration (environment variables expanded)."""
    return _expand_env(copy.deepcopy(DEFAULT_CONFIG))


def load_config(path: str | os.PathLike[str] | None) -> dict[str, Any]:
    """Read a training YAML merged with :data:`DEFAULT_CONFIG` (``${VAR:-default}`` expanded)."""
    import yaml

    cfg = copy.deepcopy(DEFAULT_CONFIG)
    if path:
        text = Path(path).read_text(encoding="utf-8")
        _merge(cfg, yaml.safe_load(text) or {})
        cfg["_source"] = {"path": str(path), "yaml": text}
    return _expand_env(cfg)


def apply_overrides(cfg: dict[str, Any], items: Sequence[str]) -> dict[str, Any]:
    """Apply ``section.key=value`` overrides (value read as YAML: numbers, lists, booleans)."""
    import yaml

    for item in items:
        if "=" not in item:
            raise ValueError(f"override {item!r}: form section.key=value expected")
        key, val = item.split("=", 1)
        node = cfg
        parts = key.strip().split(".")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = yaml.safe_load(val)
    return cfg


def _flatten(d: Mapping[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in d.items():
        if str(k).startswith("_"):
            continue
        key = f"{prefix}{k}"
        if isinstance(v, Mapping):
            out.update(_flatten(v, key + "."))
        else:
            out[key] = v
    return out


# =============================================================================================
# Networks
# =============================================================================================
class ConditionEmbedding(nn.Module):
    """Shared embedding of time t and of the n_cond normalized parameters → vector of dimension ``emb_dim``."""

    def __init__(self, n_cond: int, emb_dim: int = 256, n_freq: int = 16, cond_scale: float = 8.0) -> None:
        """``cond_scale``: largest (if > 1) or smallest (if < 1) frequency of the condition embedding, in
        cycles over the normalized range [0, 1]; the other end is 1 cycle. With the default 8, features
        oscillate faster than a coarse grid of training values can resolve (E4, hypothesis H15); 0.5 gives
        a smooth embedding (periods between 1 and 2 ranges)."""
        super().__init__()
        self.n_cond = n_cond
        self.t_emb = FourierEmbedding(n_freq, 30.0)
        self.c_emb = FourierEmbedding(n_freq, cond_scale)
        d_in = (2 * n_freq + 1) * (1 + n_cond)
        self.mlp = nn.Sequential(nn.Linear(d_in, emb_dim), nn.SiLU(), nn.Linear(emb_dim, emb_dim))

    def forward(self, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        parts = [self.t_emb(t)] + [self.c_emb(c[:, j]) for j in range(self.n_cond)]
        return self.mlp(torch.cat(parts, dim=1))


def _modulate(h: torch.Tensor, shift: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    return h * (1 + scale) + shift


def _zero(layer: nn.Linear) -> nn.Linear:
    nn.init.zeros_(layer.weight)
    nn.init.zeros_(layer.bias)
    return layer


class ResBlock(nn.Module):
    """Residual block of the MLP, modulated by the embedding (adaLN-Zero)."""

    def __init__(self, width: int, expansion: int, emb_dim: int, dropout: float) -> None:
        super().__init__()
        self.norm = nn.LayerNorm(width, elementwise_affine=False, eps=1e-6)
        self.fc1 = nn.Linear(width, width * expansion)
        self.fc2 = nn.Linear(width * expansion, width)
        self.drop = nn.Dropout(dropout)
        self.ada = _zero(nn.Linear(emb_dim, 3 * width))

    def forward(self, h: torch.Tensor, e: torch.Tensor) -> torch.Tensor:
        shift, scale, gate = self.ada(F.silu(e)).chunk(3, dim=-1)
        y = self.fc2(self.drop(F.silu(self.fc1(_modulate(self.norm(h), shift, scale)))))
        return h + gate * y


class ResMLP(nn.Module):
    """Velocity field v_θ(x, t, c): residual MLP on the flattened latent (M × C)."""

    def __init__(
        self,
        n_modes: int,
        n_channels: int,
        n_cond: int,
        width: int = 1024,
        depth: int = 6,
        expansion: int = 2,
        emb_dim: int = 256,
        n_freq: int = 16,
        dropout: float = 0.0,
        cond_scale: float = 8.0,
    ) -> None:
        super().__init__()
        dim = n_modes * n_channels
        self.embed = ConditionEmbedding(n_cond, emb_dim, n_freq, cond_scale)
        self.inp = nn.Linear(dim, width)
        self.blocks = nn.ModuleList(ResBlock(width, expansion, emb_dim, dropout) for _ in range(depth))
        self.norm_out = nn.LayerNorm(width, elementwise_affine=False, eps=1e-6)
        self.ada_out = _zero(nn.Linear(emb_dim, 2 * width))
        self.out = _zero(nn.Linear(width, dim))

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        e = self.embed(t, c)
        h = self.inp(x.flatten(1))
        for blk in self.blocks:
            h = blk(h, e)
        shift, scale = self.ada_out(F.silu(e)).chunk(2, dim=-1)
        return self.out(_modulate(self.norm_out(h), shift, scale)).view_as(x)


class DiTBlock(nn.Module):
    """Transformer block with adaLN-Zero modulation (attention over mode tokens, then MLP)."""

    def __init__(self, d: int, heads: int, mlp_ratio: int, emb_dim: int, dropout: float) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(d, elementwise_affine=False, eps=1e-6)
        self.attn = nn.MultiheadAttention(d, heads, dropout=dropout, batch_first=True)
        self.norm2 = nn.LayerNorm(d, elementwise_affine=False, eps=1e-6)
        self.mlp = nn.Sequential(
            nn.Linear(d, d * mlp_ratio),
            nn.GELU(approximate="tanh"),
            nn.Dropout(dropout),
            nn.Linear(d * mlp_ratio, d),
        )
        self.ada = _zero(nn.Linear(emb_dim, 6 * d))

    def forward(self, h: torch.Tensor, e: torch.Tensor) -> torch.Tensor:
        s1, c1, g1, s2, c2, g2 = self.ada(F.silu(e)).unsqueeze(1).chunk(6, dim=-1)
        y = _modulate(self.norm1(h), s1, c1)
        h = h + g1 * self.attn(y, y, y, need_weights=False)[0]
        return h + g2 * self.mlp(_modulate(self.norm2(h), s2, c2))


def _mode_features(m: np.ndarray, kmax: float) -> np.ndarray:
    """Position features of a mode: m/kmax, |m|/kmax and sinusoids of π m 2^j / kmax."""
    base = m.astype(np.float64) / kmax
    feats = [base, np.linalg.norm(base, axis=1, keepdims=True)]
    for j in range(3):
        feats += [np.sin(math.pi * base * 2**j), np.cos(math.pi * base * 2**j)]
    return np.concatenate(feats, axis=1)


class ModeTransformer(nn.Module):
    """Velocity field v_θ(x, t, c): light transformer on tokens of ``modes_per_token`` modes.

    Since the modes are sorted by |m|, a token groups modes that are neighbors in wavenumber; the position
    of a token is learned from the wave vectors of its modes.
    """

    mode_feats: torch.Tensor

    def __init__(
        self,
        modes: np.ndarray,
        kmax: float,
        n_channels: int,
        n_cond: int,
        d_model: int = 192,
        depth: int = 6,
        heads: int = 6,
        mlp_ratio: int = 4,
        modes_per_token: int = 4,
        emb_dim: int = 256,
        n_freq: int = 16,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        M = int(modes.shape[0])
        p = max(1, int(modes_per_token))
        self.n_modes, self.n_channels, self.p = M, n_channels, p
        self.n_tokens = math.ceil(M / p)
        pad = self.n_tokens * p - M
        feats = _mode_features(np.asarray(modes), kmax)
        feats = np.concatenate([feats, np.zeros((M, 1))], axis=1)
        if pad:
            filler = np.zeros((pad, feats.shape[1]))
            filler[:, -1] = 1.0  # padding indicator
            feats = np.concatenate([feats, filler])
        self.register_buffer(
            "mode_feats", torch.as_tensor(feats.reshape(self.n_tokens, -1), dtype=torch.float32)
        )
        self.embed = ConditionEmbedding(n_cond, emb_dim, n_freq)
        self.inp = nn.Linear(p * n_channels, d_model)
        self.pos = nn.Linear(self.mode_feats.shape[1], d_model)
        self.blocks = nn.ModuleList(
            DiTBlock(d_model, heads, mlp_ratio, emb_dim, dropout) for _ in range(depth)
        )
        self.norm_out = nn.LayerNorm(d_model, elementwise_affine=False, eps=1e-6)
        self.ada_out = _zero(nn.Linear(emb_dim, 2 * d_model))
        self.out = _zero(nn.Linear(d_model, p * n_channels))

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        b = x.shape[0]
        pad = self.n_tokens * self.p - self.n_modes
        xp = F.pad(x, (0, 0, 0, pad)) if pad else x
        h = self.inp(xp.reshape(b, self.n_tokens, self.p * self.n_channels)) + self.pos(self.mode_feats)
        e = self.embed(t, c)
        for blk in self.blocks:
            h = blk(h, e)
        shift, scale = self.ada_out(F.silu(e)).unsqueeze(1).chunk(2, dim=-1)
        y = self.out(_modulate(self.norm_out(h), shift, scale))
        return y.reshape(b, self.n_tokens * self.p, self.n_channels)[:, : self.n_modes]


class SignSymmetrized(nn.Module):
    """v_S(x, t, c) = ½ (v(x, t, c) + S v(S x, t, c)): exactly equivariant for S = diag(±1) (A_B → −A_B).

    If x₀ ~ N(0, I) (invariant under S), the equivariant flow transports an invariant distribution: the generated
    distribution is symmetric under B → −B, to machine precision and whatever the training.
    """

    sign: torch.Tensor

    def __init__(self, base: nn.Module, sign: torch.Tensor) -> None:
        super().__init__()
        self.base = base
        self.register_buffer("sign", sign.detach().clone().to(torch.float32))

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        s = self.sign.to(x.dtype)
        return 0.5 * (self.base(x, t, c) + s * self.base(s * x, t, c))


def build_field(model_cfg: Mapping[str, Any], space: FourierPotentialSpace, n_cond: int) -> nn.Module:
    """Velocity field network (``model.architecture``: ``mlp``, ``transformer``), symmetrized if needed."""
    arch = str(model_cfg.get("architecture", "mlp"))
    if arch == "mlp":
        o = dict(DEFAULT_CONFIG["model"]["mlp"], **(model_cfg.get("mlp") or {}))
        base: nn.Module = ResMLP(
            space.n_modes,
            space.n_channels,
            n_cond,
            int(o["width"]),
            int(o["depth"]),
            int(o["expansion"]),
            int(o["emb_dim"]),
            int(o["n_freq"]),
            float(o["dropout"]),
        )
    elif arch == "transformer":
        o = dict(DEFAULT_CONFIG["model"]["transformer"], **(model_cfg.get("transformer") or {}))
        base = ModeTransformer(
            space.m.cpu().numpy(),
            space.kmax,
            space.n_channels,
            n_cond,
            int(o["d_model"]),
            int(o["depth"]),
            int(o["heads"]),
            int(o["mlp_ratio"]),
            int(o["modes_per_token"]),
            int(o["emb_dim"]),
            int(o["n_freq"]),
            float(o["dropout"]),
        )
    else:
        raise ValueError(f"architecture {arch!r} unknown (mlp, transformer)")
    if (
        bool(model_cfg.get("symmetry_b_sign", False))
        and space.symmetric_b
        and "magnetic_field" in space.fields
    ):
        return SignSymmetrized(base, space.sign)
    return base


# =============================================================================================
# Flow matching, sampling, stationarity loss
# =============================================================================================
class FlowMatchingLoss(nn.Module):
    """Complete training loss (a single ``forward`` per iteration: DDP-compatible).

    ``forward(x1, c, stationarity)`` → (total loss, flow matching loss, stationarity loss).
    """

    forcing_hat: torch.Tensor
    flow_hat: torch.Tensor

    def __init__(
        self,
        field: nn.Module,
        space: FourierPotentialSpace,
        cond_specs: Sequence[CondSpec],
        fixed_params: Mapping[str, Any],
        stat_cfg: Mapping[str, Any] | None = None,
        autocast: tuple[str, torch.dtype] | None = None,
        t_sampling: str = "uniform",
    ) -> None:
        super().__init__()
        self.field = field
        self.space = space
        self.cond_specs = list(cond_specs)
        self.fixed = dict(fixed_params)
        self.autocast = autocast
        self.t_sampling = t_sampling
        self.stat = dict(DEFAULT_CONFIG["stationarity"], **(stat_cfg or {}))
        self.forcing_kind: str | None = None
        self.register_buffer("forcing_hat", torch.zeros(0, 3, dtype=torch.complex64), persistent=False)
        self.register_buffer("flow_hat", torch.zeros(0, 3, dtype=torch.complex64), persistent=False)
        if self.stat.get("enabled"):
            self._prepare_stationarity()

    def _prepare_stationarity(self) -> None:
        """Check that the requested budget is computable and precompute forcing / imposed flow at the modes."""
        from milady.eval import metrics

        sp, st = self.space, self.stat
        if int(st["n_per"]) < 2 or int(st["n_per"]) % 2:
            raise ValueError("stationarity.n_per: even integer ≥ 2 (two half-batches)")
        balance = str(st["balance"])
        if balance not in ("total", "kinetic", "magnetic"):
            raise ValueError("stationarity.balance: total, kinetic or magnetic")
        n = sp.default_grid()
        grid = (n, n, n)
        mode = str(self.fixed.get("mode", "dynamic"))
        if "velocity" not in sp.fields and mode == "kinematic":
            flow = metrics.imposed_flow(self.fixed, grid, sp.lengths)
            if flow is not None:
                self.flow_hat = sp.vector_modes(flow).to(torch.complex64)
        has_u = "velocity" in sp.fields or self.flow_hat.numel() > 0
        if balance in ("total", "kinetic") and "velocity" not in sp.fields:
            raise ValueError(f"budget {balance}: the field \"velocity\" must be generated (data.fields)")
        if balance == "magnetic" and ("magnetic_field" not in sp.fields or not has_u):
            raise ValueError("magnetic budget: generated B and generated or imposed u (kinematic mode) required")
        if balance in ("total", "kinetic") and st["injection"] == "forcing":
            kind = str(self.fixed.get("forcing", ""))
            if mode != "dynamic" or kind not in ("abc", "tg"):
                raise ValueError(
                    "\"forcing\" injection: constant ABC or TG forcing common to all files required "
                    "(otherwise stationarity.injection: param or none)"
                )
            self.forcing_kind = kind
            shape = metrics._shape_field(kind, self.fixed, grid, sp.lengths)
            fh = sp.vector_modes(shape)
            captured = float(2 * (fh.abs() ** 2).sum()) / max(float((shape**2).sum(-1).mean()), 1e-30)
            if captured < 0.99:
                raise ValueError(
                    f"the forcing is only {captured:.0%} inside the ball |m| ≤ kmax: increase kmax"
                )
            self.forcing_hat = fh.to(torch.complex64)

    # -- flow matching ------------------------------------------------------------------------
    def fm_loss(
        self, x1: torch.Tensor, c: torch.Tensor, generator: torch.Generator | None = None
    ) -> torch.Tensor:
        """Flow matching loss ‖v(x_t, t, c) − (x₁ − x₀)‖² (mean); see :func:`milady.train.flow.fm_loss`."""
        return fm_loss(
            self.field, x1, c, t_sampling=self.t_sampling, generator=generator, autocast=self.autocast
        )

    # -- stationarity -------------------------------------------------------------------------
    def _physics(self, cn: torch.Tensor) -> dict[str, torch.Tensor]:
        """Physical parameters (ν, η, injection amplitude, λ) of the normalized conditions ``cn``."""
        from milady.eval.metrics import forcing_amplitude

        rows = cn.detach().cpu().numpy()
        out: dict[str, list[float]] = {"nu": [], "eta": [], "inj": [], "lam": []}
        for row in rows:
            cond = {s.name: float(s.denormalize(row[j])) for j, s in enumerate(self.cond_specs)}
            p = physical_parameters(cond, self.fixed, self.space.lengths)
            out["nu"].append(float(p.get("nu", 0.0) or 0.0))
            out["eta"].append(float(p.get("eta", 0.0) or 0.0))
            if self.forcing_kind is not None:
                out["inj"].append(forcing_amplitude(p, self.space.lengths))
            elif self.stat["injection"] == "param":
                out["inj"].append(param_value(p, str(self.stat["injection_param"])))
            else:
                out["inj"].append(0.0)
            g = self.stat.get("growth_rate", 0.0)
            out["lam"].append(float(g) if isinstance(g, (int, float)) else param_value(p, str(g)))
        return {k: torch.tensor(v, dtype=torch.float32, device=cn.device) for k, v in out.items()}

    def stationarity_loss(self) -> torch.Tensor:
        """Unbiased penalty of (E[budget residual])² at conditions drawn in ``cond_range``.

        For each condition: ``n_per`` samples by differentiable Heun (``steps`` steps), residual
        normalized by the scale of the sinks (detached), product of the means of the two half-batches.
        """
        st = self.stat
        nc, nper = int(st["n_cond"]), int(st["n_per"])
        dev = self.space.mean.device
        lo, hi = (float(v) for v in st.get("cond_range", (0.0, 1.0)))
        n_c = len(self.cond_specs)
        cn = lo + (hi - lo) * torch.rand(nc, n_c, device=dev)
        z = torch.randn(nc * nper, self.space.n_modes, self.space.n_channels, device=dev)
        z = heun_sample(self.field, z, cn.repeat_interleave(nper, 0), int(st["steps"]), self.autocast)
        phys = {k: v.repeat_interleave(nper) for k, v in self._physics(cn).items()}
        x = self.space.denormalize(z.float())
        balance = str(st["balance"])
        with torch.autocast(device_type=dev.type, enabled=False):
            terms = self.space.budget_terms(
                x,
                phys["nu"],
                phys["eta"],
                forcing_hat=self.forcing_hat if self.forcing_kind else None,
                flow_hat=self.flow_hat if self.flow_hat.numel() else None,
                injection=phys["inj"] if (self.forcing_kind or st["injection"] == "param") else None,
                production=balance == "magnetic"
                or (balance == "kinetic" and "magnetic_field" in self.space.fields),
            )
        zero = torch.zeros_like(phys["nu"])
        d_nu, d_eta = terms.get("kinetic_dissipation", zero), terms.get("magnetic_dissipation", zero)
        prod = terms.get("magnetic_production", zero)
        if balance == "total":
            res, scale = terms["injection"] - d_nu - d_eta, d_nu + d_eta
        elif balance == "kinetic":
            res, scale = terms["injection"] - prod - d_nu, d_nu + prod.abs()
        else:
            b2 = 2.0 * terms["magnetic_energy"]
            res, scale = prod - d_eta - phys["lam"] * b2, d_eta + prod.abs()
        r = res.view(nc, 2, nper // 2).mean(2)
        s = scale.detach().view(nc, nper).mean(1).clamp_min(1e-12)
        rn = r / s[:, None]
        return (rn[:, 0] * rn[:, 1]).mean()

    def forward(
        self, x1: torch.Tensor, c: torch.Tensor, stationarity: bool = False
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        fm = self.fm_loss(x1, c)
        st = self.stationarity_loss() if stationarity else torch.zeros((), device=x1.device)
        return fm + float(self.stat["beta"]) * st, fm.detach(), st.detach()


# =============================================================================================
# Trained model (inference)
# =============================================================================================
class GenerativeModel:
    """Model ready to sample: latent space, network (EMA weights), conditioning, context."""

    def __init__(
        self,
        space: FourierPotentialSpace,
        field: nn.Module,
        cond_specs: Sequence[CondSpec],
        fixed_params: Mapping[str, Any],
        meta: Mapping[str, Any] | None = None,
        device: torch.device | str = "cpu",
        sampling_steps: int = 50,
    ) -> None:
        self.device = torch.device(device)
        self.space = space.to(self.device).eval()
        self.field = field.to(self.device).eval()
        self.cond_specs = list(cond_specs)
        self.fixed = dict(fixed_params)
        self.meta = dict(meta or {})
        self.sampling_steps = int(sampling_steps)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], device: torch.device | str = "cpu") -> GenerativeModel:
        """Rebuild the model from a checkpoint (dictionary from :func:`load_checkpoint`)."""
        space = FourierPotentialSpace(**payload["space"]["config"])
        space.load_state_dict(payload["space"]["state"])
        specs = [CondSpec.parse(s) for s in payload["cond_specs"]]
        field = build_field(payload["model_config"], space, len(specs))
        field.load_state_dict(payload.get("ema_state") or payload["field_state"])
        steps = int(payload.get("config", {}).get("sampling", {}).get("steps", 50))
        return cls(space, field, specs, payload.get("fixed_params", {}), payload.get("meta"), device, steps)

    def default_grid(self) -> int:
        """Default reconstruction grid (even, ≥ 3 kmax + 1)."""
        return self.space.default_grid()

    def cond_vector(self, point: Mapping[str, Any]) -> torch.Tensor:
        """Normalized condition ``(n_cond,)`` of a point ``{"Re": 50, …}``."""
        missing = [s.name for s in self.cond_specs if s.name not in point]
        if missing:
            raise KeyError(f"missing conditioning parameters: {missing}")
        vals = [float(s.normalize(float(point[s.name]))) for s in self.cond_specs]
        return torch.tensor(vals, dtype=torch.float32, device=self.device)

    def physical_parameters(self, point: Mapping[str, Any]) -> dict[str, Any]:
        """Complete physical parameters at point ``point`` (ν, η, forcing…)."""
        cond = {s.name: float(point[s.name]) for s in self.cond_specs if s.name in point}
        return physical_parameters(cond, self.fixed, self.space.lengths)

    @torch.no_grad()
    def sample_latent(
        self, point: Mapping[str, Any], n: int, seed: int = 0, steps: int | None = None
    ) -> torch.Tensor:
        """``n`` raw latents ``(n, M, C)`` at point ``point`` (reproducible seed ``seed``)."""
        g = torch.Generator().manual_seed(int(seed))
        z = torch.randn(n, self.space.n_modes, self.space.n_channels, generator=g).to(self.device)
        c = self.cond_vector(point).expand(n, -1)
        z = heun_sample(self.field, z, c, int(steps or self.sampling_steps))
        return self.space.denormalize(z)

    @torch.no_grad()
    def sample_fields(
        self,
        point: Mapping[str, Any],
        n: int,
        seed: int = 0,
        steps: int | None = None,
        grid: int | Sequence[int] | None = None,
    ) -> dict[str, np.ndarray]:
        """Generated physical fields ``{name: (n, nx, ny, nz, 3)}`` (numpy float32), zero divergence."""
        x = self.sample_latent(point, n, seed, steps)
        return {k: v.float().cpu().numpy() for k, v in self.space.decode(x, grid).items()}


# =============================================================================================
# Checkpoints, catalog, logging
# =============================================================================================
def _checkpoint_base(cfg: Mapping[str, Any]) -> str:
    base = (cfg.get("checkpoint") or {}).get("uri") or os.environ.get("MILADY_MODELS_URI")
    return str(base) if base else storage.join(storage.base_uri(), "_models")


def save_checkpoint(payload: Mapping[str, Any], local: Path, uri: str) -> str:
    """Write ``payload`` locally (temporary file then atomic rename) then copy it to ``uri``."""
    local.parent.mkdir(parents=True, exist_ok=True)
    tmp = local.with_name(f".{local.name}.{uuid.uuid4().hex[:8]}.part")
    try:
        torch.save(dict(payload), tmp)
        os.replace(tmp, local)
    finally:
        tmp.unlink(missing_ok=True)
    if storage.is_local(uri) and storage.local_path(uri).resolve() == local.resolve():
        return uri
    storage.put(local, uri)
    return uri


def load_checkpoint(ref: str, map_location: str | torch.device = "cpu") -> dict[str, Any]:
    """Load a local or remote checkpoint (``s3://``: downloaded to a temporary file).

    MilaDy checkpoints contain Python dictionaries (configuration, parameters):
    ``weights_only=False`` — only load trusted files (produced by this code).
    """
    if storage.is_local(ref):
        return torch.load(storage.local_path(ref), map_location=map_location, weights_only=False)
    with tempfile.TemporaryDirectory(prefix="milady-ckpt-") as tmp:
        path = storage.get(ref, Path(tmp) / Path(storage.split_uri(ref)[1]).name)
        return torch.load(path, map_location=map_location, weights_only=False)


def latest_model_id(catalog: Any, name: str) -> str | None:
    """Identifier of the latest model ``name`` of the catalog that has a checkpoint, or ``None``."""
    from sqlalchemy import select

    from milady.catalog.models import Model

    with catalog.session() as s:
        row = s.scalars(
            select(Model)
            .where(Model.name == name, Model.checkpoint_uri.is_not(None))
            .order_by(Model.created_at.desc())
        ).first()
        return str(row.id) if row is not None else None


def load_model(
    ref: str, device: str | torch.device | None = None, catalog: Any | None = None
) -> tuple[GenerativeModel, str | None]:
    """Load a model from its catalog identifier (UUID) or a checkpoint path / URI.

    Returns ``(model, catalog identifier or None)``.
    """
    model_id: str | None = None
    uri = str(ref)
    if _UUID_RE.match(uri) and not Path(uri).exists():
        if catalog is None:
            from milady.catalog.api import Catalog

            catalog = Catalog()
        row = catalog.get_model(uri)
        if row is None:
            raise KeyError(f"model {uri} absent from the catalog")
        if not row.get("checkpoint_uri"):
            raise ValueError(f"model {uri} without checkpoint (unfinished training?)")
        model_id, uri = uri, str(row["checkpoint_uri"])
    payload = load_checkpoint(uri)
    if model_id is None:
        model_id = (payload.get("meta") or {}).get("model_id")
    dev = _resolve_device(str(device or "auto"))
    return GenerativeModel.from_payload(payload, dev), model_id


class RunLogger:
    """Metrics log: ``metrics.jsonl`` and, if ``MLFLOW_TRACKING_URI`` is defined, MLflow."""

    def __init__(
        self,
        active: bool,
        workdir: Path,
        run_name: str,
        cfg: Mapping[str, Any],
        resume_run_id: str | None = None,
    ) -> None:
        self.active, self.mlflow, self.run_id = active, None, None
        self.path = workdir / "metrics.jsonl"
        if not active:
            return
        workdir.mkdir(parents=True, exist_ok=True)
        uri = os.environ.get("MLFLOW_TRACKING_URI")
        if not uri:
            LOG.info("MLFLOW_TRACKING_URI not defined: local log %s", self.path)
            return
        try:
            import mlflow

            mlflow.set_experiment(str((cfg.get("mlflow") or {}).get("experiment") or "milady-fm3d"))
            run = (
                mlflow.start_run(run_id=resume_run_id)
                if resume_run_id
                else mlflow.start_run(run_name=run_name)
            )
            self.mlflow, self.run_id = mlflow, run.info.run_id
            if not resume_run_id:
                params = {
                    k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in _flatten(cfg).items()
                }
                mlflow.log_params({k: str(v)[:500] for k, v in params.items()})
                mlflow.set_tags({"milady.git_commit": git_commit(), "milady.host": socket.gethostname()})
            LOG.info("MLflow: run %s (%s)", self.run_id, uri)
        except Exception as exc:  # noqa: BLE001 — tracking must never stop a training run
            LOG.warning("MLflow unavailable (%s): local log %s", exc, self.path)
            self.mlflow = None

    def log(self, metrics: Mapping[str, float], step: int) -> None:
        """Record metrics at iteration ``step``."""
        if not self.active:
            return
        row = {"step": int(step), "time": time.time(), **{k: float(v) for k, v in metrics.items()}}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        if self.mlflow is not None:
            try:
                self.mlflow.log_metrics({k: float(v) for k, v in metrics.items()}, step=int(step))
            except Exception as exc:  # noqa: BLE001
                LOG.warning("MLflow log_metrics: %s", exc)

    def artifact(self, path: Path) -> None:
        """Add a file to the artifacts of the MLflow run (if active)."""
        if self.active and self.mlflow is not None:
            try:
                self.mlflow.log_artifact(str(path))
            except Exception as exc:  # noqa: BLE001
                LOG.warning("MLflow log_artifact: %s", exc)

    def close(self, ok: bool) -> None:
        """End the MLflow run."""
        if self.active and self.mlflow is not None:
            with contextlib.suppress(Exception):
                self.mlflow.end_run(status="FINISHED" if ok else "FAILED")


class _Catalog:
    """Fault-tolerant catalog access (warning), unless ``catalog.required: true``."""

    def __init__(self, enabled: bool, url: str | None, required: bool) -> None:
        self.cat, self.required = None, required
        if not enabled:
            return
        try:
            from milady.catalog.api import Catalog

            self.cat = Catalog(url)
        except Exception as exc:
            if required:
                raise
            LOG.warning("catalog unavailable (%s): model not registered", exc)

    def call(self, method: str, *args: Any, **kwargs: Any) -> Any:
        if self.cat is None:
            return None
        try:
            return getattr(self.cat, method)(*args, **kwargs)
        except Exception as exc:
            if self.required:
                raise
            LOG.warning("catalog: %s failed (%s)", method, exc)
            return None


def _scheduler() -> tuple[str, str]:
    if os.environ.get("SLURM_JOB_ID"):
        return "slurm", os.environ["SLURM_JOB_ID"]
    if Path("/.dockerenv").exists() or os.environ.get("MILADY_IN_DOCKER"):
        return "docker", socket.gethostname()
    return "local", str(os.getpid())


# =============================================================================================
# Distribution and devices
# =============================================================================================
def _resolve_device(pref: str, local_rank: int = 0) -> torch.device:
    pref = (pref or "auto").lower()
    if pref == "auto":
        return torch.device(f"cuda:{local_rank}") if torch.cuda.is_available() else torch.device("cpu")
    if pref == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("device cuda requested but no GPU visible")
        return torch.device(f"cuda:{local_rank}")
    return torch.device(pref)


def _setup_distributed(pref: str) -> tuple[int, int, int, torch.device]:
    """Initialize DDP if launched by torchrun (``WORLD_SIZE`` > 1): NCCL on GPU, gloo on CPU."""
    world = int(os.environ.get("WORLD_SIZE", "1"))
    rank = int(os.environ.get("RANK", "0"))
    local = int(os.environ.get("LOCAL_RANK", "0"))
    device = _resolve_device(pref, local)
    if world > 1 and not dist.is_initialized():
        if device.type == "cuda":
            torch.cuda.set_device(device)
        dist.init_process_group(backend="nccl" if device.type == "cuda" else "gloo")
        rank, world = dist.get_rank(), dist.get_world_size()
    return rank, world, local, device


def _broadcast(obj: Any, world: int) -> Any:
    if world <= 1:
        return obj
    box = [obj]
    dist.broadcast_object_list(box, src=0)
    return box[0]


class _StopFlag:
    """Stop signal (SIGTERM, Slurm SIGUSR1 before the end): checkpoint then exit."""

    def __init__(self) -> None:
        self.stop = False
        self._old: dict[int, Any] = {}

    def __enter__(self) -> Self:
        for sig in (signal.SIGTERM, signal.SIGUSR1):
            with contextlib.suppress(ValueError, OSError):
                self._old[sig] = signal.signal(sig, self._handler)
        return self

    def _handler(self, signum: int, _frame: Any) -> None:
        LOG.warning("signal %d received: checkpoint then stop", signum)
        self.stop = True

    def __exit__(self, *exc: object) -> None:
        for sig, old in self._old.items():
            with contextlib.suppress(ValueError, OSError):
                signal.signal(sig, old)


# =============================================================================================
# Training
# =============================================================================================
def _lr_lambda(warmup: int, total: int, ratio_min: float) -> Any:
    def f(step: int) -> float:
        if warmup > 0 and step < warmup:
            return (step + 1) / warmup
        prog = min(1.0, (step - warmup) / max(1, total - warmup))
        return ratio_min + (1 - ratio_min) * 0.5 * (1 + math.cos(math.pi * prog))

    return f


def _constraint_name(cfg: Mapping[str, Any], space: FourierPotentialSpace) -> str:
    parts = ["vector_potential_fourier"]
    if space.symmetric_b and cfg["model"].get("symmetry_b_sign"):
        parts.append("b_sign_equivariant")
    if cfg["stationarity"].get("enabled"):
        parts.append(f"stationarity_{cfg['stationarity'].get('balance', 'total')}")
    return "+".join(parts)


def _ema_update(ema: nn.Module, model: nn.Module, decay: float) -> None:
    with torch.no_grad():
        for pe, p in zip(ema.parameters(), model.parameters(), strict=True):
            pe.lerp_(p.detach(), 1.0 - decay)
        for be, b in zip(ema.buffers(), model.buffers(), strict=True):
            be.copy_(b)


def train(
    cfg: dict[str, Any],
    *,
    files: Sequence[str] | None = None,
    dataset: str | None = None,
    run_name: str | None = None,
    resume: str | None = None,
    init_from: str | None = None,
) -> dict[str, Any]:
    """Train a model according to ``cfg`` (see :data:`DEFAULT_CONFIG`); returns a summary (rank 0).

    Launched by ``torchrun``, each process runs this function (DDP); only rank 0 writes the checkpoints,
    the log and the catalog.
    """
    tcfg = cfg["train"]
    rank, world, _local, device = _setup_distributed(str(tcfg.get("device") or "auto"))
    main_rank = rank == 0
    if tcfg.get("num_threads"):
        torch.set_num_threads(int(tcfg["num_threads"]))
    seed = int(tcfg.get("seed", 0))
    torch.manual_seed(seed + 1000 * rank)
    np.random.seed(seed + 1000 * rank)
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    prec = str(tcfg.get("precision", "auto"))
    if prec == "auto":
        prec = "bf16" if device.type == "cuda" and torch.cuda.is_bf16_supported() else "fp32"
    autocast = (device.type, torch.bfloat16) if prec == "bf16" else None

    # -- run name, locations ------------------------------------------------------------------
    if main_rank and not run_name:
        run_name = os.environ.get("MILADY_RUN_NAME") or (
            f"{cfg['name']}-slurm{os.environ['SLURM_JOB_ID']}"
            if os.environ.get("SLURM_JOB_ID")
            else f"{cfg['name']}-{_dt.datetime.now(_dt.UTC):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:6]}"
        )
    run_name = _broadcast(run_name, world)
    run_uri = storage.join(_checkpoint_base(cfg), cfg["name"], run_name)
    if storage.is_local(run_uri):
        workdir = storage.local_path(run_uri)
    else:
        wd = Path(os.path.expandvars(str(tcfg.get("workdir") or "data/runs"))).expanduser()
        workdir = (wd if wd.is_absolute() else project_root() / wd) / run_name
    last_uri, final_uri = storage.join(run_uri, "last.pt"), storage.join(run_uri, "final.pt")

    # -- resumption or initialization from a model ---------------------------------------------
    resume = resume or str(tcfg.get("resume") or "auto")
    init_from = init_from or tcfg.get("init_from")
    payload: dict[str, Any] | None = None
    resumed = False
    if resume not in ("never", "none", "false", "False"):
        src = last_uri if resume == "auto" else resume
        exists = storage.exists(src) if resume == "auto" else True
        if exists:
            payload, resumed = load_checkpoint(src), True
            LOG.info("resuming from %s (iteration %d)", src, payload["step"])
    if payload is None and init_from:
        payload = load_checkpoint(str(init_from))
        LOG.info("initialization from %s", init_from)

    # -- data ---------------------------------------------------------------------------------
    cat = _Catalog(
        main_rank and bool(cfg["catalog"].get("enabled", True)),
        cfg["catalog"].get("url"),
        bool(cfg["catalog"].get("required", False)),
    )
    uris = None
    if main_rank:
        uris = resolve_uris(cfg["data"], files=files, dataset=dataset, catalog=cat.cat)
    uris = _broadcast(uris, world)
    sym = bool(cfg["model"].get("symmetry_b_sign", False))
    bundle = build_data(
        cfg["data"],
        uris,
        symmetric_b=sym,
        space_state=payload["space"] if payload is not None else None,
        cond_specs=payload["cond_specs"] if payload is not None else None,
    )
    space = bundle.space.to(device)
    train_ds = bundle.splits["train"]
    val_ds = bundle.splits.get("val")
    if bool(cfg["data"].get("on_device", True)):
        train_ds = train_ds.to(device)
        val_ds = val_ds.to(device) if val_ds is not None else None
    fixed = (
        dict(payload["fixed_params"])
        if payload is not None and payload.get("fixed_params")
        else bundle.fixed_params
    )

    # -- model, loss, optimizer ---------------------------------------------------------------
    n_cond = len(bundle.cond_specs)
    model_cfg = payload["model_config"] if payload is not None else cfg["model"]
    field = build_field(model_cfg, space, n_cond).to(device)
    if payload is not None:
        field.load_state_dict(payload["field_state"])
    ema_decay = float(tcfg.get("ema") or 0.0)
    ema = copy.deepcopy(field).eval() if ema_decay > 0 else None
    if ema is not None and payload is not None and payload.get("ema_state"):
        ema.load_state_dict(payload["ema_state"])
    for p in ema.parameters() if ema is not None else []:
        p.requires_grad_(False)
    # Fine-tuning anchoring: reference = weights of ``init_from`` if given (including after a
    # resumption), otherwise weights at the start of this run.
    anchor_w = float(cfg["stationarity"].get("anchor") or 0.0)
    anchor_ref: list[torch.Tensor] = []
    if anchor_w > 0:
        ref_field = build_field(model_cfg, space, n_cond).to(device)
        if init_from:
            ref_field.load_state_dict(load_checkpoint(str(init_from))["field_state"])
        else:
            ref_field.load_state_dict(field.state_dict())
            if resumed:
                LOG.warning("stationarity.anchor without init_from: anchoring to the resumed weights, not to the original model")
        anchor_ref = [q.detach().clone() for q in ref_field.parameters()]
        del ref_field
    n_anchor = max(1, sum(q.numel() for q in anchor_ref))
    loss_mod = FlowMatchingLoss(
        field,
        space,
        bundle.cond_specs,
        fixed,
        cfg["stationarity"],
        autocast,
        str(tcfg.get("t_sampling", "uniform")),
    ).to(device)
    ddp: nn.Module = loss_mod
    if world > 1:
        ddp = nn.parallel.DistributedDataParallel(
            loss_mod, device_ids=[device.index] if device.type == "cuda" else None, broadcast_buffers=False
        )
    opt = torch.optim.AdamW(
        field.parameters(),
        lr=float(tcfg["lr"]),
        weight_decay=float(tcfg.get("weight_decay", 0.0)),
        betas=(0.9, 0.99),
    )
    sampler = EpochSampler(len(train_ds), int(tcfg["batch_size"]), rank, world, seed)
    per_epoch = len(sampler)
    total = int(tcfg["iters"]) if tcfg.get("iters") else int(tcfg.get("epochs") or 1) * per_epoch
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt,
        _lr_lambda(
            min(int(tcfg.get("warmup", 0)), total // 10),
            total,
            float(tcfg.get("lr_min", 0.0)) / float(tcfg["lr"]),
        ),
    )
    step = 0
    if resumed and payload is not None:
        opt.load_state_dict(payload["optimizer"])
        sched.load_state_dict(payload["scheduler"])
        step = int(payload["step"])
    n_params = sum(p.numel() for p in field.parameters())

    # -- log, catalog ---------------------------------------------------------------------
    meta_prev = dict(payload.get("meta") or {}) if (payload is not None and resumed) else {}
    logger = RunLogger(main_rank, workdir, run_name, cfg, meta_prev.get("mlflow_run_id"))
    arch = f"fm3d-{model_cfg.get('architecture', 'mlp')}"
    hyper = {
        "model": model_cfg,
        "train": {k: v for k, v in tcfg.items() if k not in ("workdir",)},
        "stationarity": cfg["stationarity"],
        "data": {
            "kmax": space.kmax,
            "fields": list(space.fields),
            "conditioning": [s.to_dict() for s in bundle.cond_specs],
            "n_snapshots": bundle.info["n_snapshots"],
            "t_min": cfg["data"].get("t_min"),
            "stride": cfg["data"].get("stride"),
        },
        "latent_dim": bundle.info["latent_dim"],
        "n_params": n_params,
        "world_size": world,
        "precision": prec,
        "run_name": run_name,
    }
    model_id = meta_prev.get("model_id")
    if main_rank and not model_id:
        model_id = cat.call(
            "register_model",
            cfg["name"],
            arch,
            _constraint_name(cfg, space),
            hyper,
            dataset_id=uris.get("dataset_id") if uris else None,
            mlflow_run_id=logger.run_id,
            checkpoint_uri=None,
            git_commit=git_commit(),
        )
    sched_name, ext_id = _scheduler()
    job_id = (
        cat.call(
            "register_job",
            "train",
            sched_name,
            external_id=ext_id,
            model_id=model_id,
            status="running",
            log_uri=str(logger.path),
        )
        if main_rank and model_id
        else None
    )
    meta = {
        "run_name": run_name,
        "model_id": model_id,
        "mlflow_run_id": logger.run_id,
        "dataset_id": uris.get("dataset_id") if uris else None,
        "dataset_name": uris.get("dataset_name") if uris else None,
        "dataset_version": uris.get("dataset_version") if uris else None,
        "data_uris": bundle.info["data_uris"],
        "eval_points": bundle.eval_points,
        "git_commit": git_commit(),
        "host": socket.gethostname(),
        "n_params": n_params,
        "latent_dim": bundle.info["latent_dim"],
        "milady_version": __version__,
        "torch_version": torch.__version__,
        "world_size": world,
        "architecture": arch,
        "constraint_mechanism": _constraint_name(cfg, space),
    }
    if main_rank:
        LOG.info(
            "run %s: %d parameters, %d iterations (%d per epoch), %d processes, %s, %s",
            run_name,
            n_params,
            total,
            per_epoch,
            world,
            device,
            prec,
        )

    def make_payload(final: bool) -> dict[str, Any]:
        return {
            "format": "milady-fm3d",
            "format_version": 1,
            "final": final,
            "config": {k: v for k, v in cfg.items() if k != "_source"},
            "config_yaml": (cfg.get("_source") or {}).get("yaml", ""),
            "model_config": model_cfg,
            "space": {"config": space.config(), "state": {k: v.cpu() for k, v in space.state_dict().items()}},
            "cond_specs": [s.to_dict() for s in bundle.cond_specs],
            "fixed_params": fixed,
            "field_state": {k: v.cpu() for k, v in field.state_dict().items()},
            "ema_state": {k: v.cpu() for k, v in ema.state_dict().items()} if ema is not None else None,
            "optimizer": opt.state_dict(),
            "scheduler": sched.state_dict(),
            "step": step,
            "meta": {**meta, "saved": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds")},
        }

    # -- loop -----------------------------------------------------------------------------------
    st_cfg = cfg["stationarity"]
    use_stat_any = bool(st_cfg.get("enabled"))
    beta0 = float(loss_mod.stat["beta"])
    log_every = max(1, int(tcfg.get("log_every", 50)))
    val_every = int(tcfg.get("val_every") or 0)
    ckpt_every = int(tcfg.get("ckpt_every") or 0)
    augment = bool(tcfg.get("augment_b_sign")) and space.symmetric_b
    acc = {"loss": 0.0, "fm": 0.0, "stat": 0.0, "n": 0, "n_stat": 0}
    last: dict[str, float] = {}
    ok = False
    t_start = time.time()
    epoch = step // per_epoch
    batches = sampler.epoch(epoch)
    pos = step % per_epoch
    try:
        with _StopFlag() as stopper:
            loss_mod.train()
            while step < total:
                if pos >= len(batches):
                    epoch, pos = epoch + 1, 0
                    batches = sampler.epoch(epoch)
                idx = batches[pos].to(train_ds.x.device)
                pos += 1
                x1, c = train_ds.x[idx].to(device), train_ds.cond[idx].to(device)
                if augment:
                    flip = torch.rand(x1.shape[0], 1, 1, device=device) < 0.5
                    x1 = torch.where(flip, x1 * space.sign, x1)
                use_stat = (
                    use_stat_any
                    and step >= int(st_cfg.get("start_iter", 0))
                    and ((step - int(st_cfg.get("start_iter", 0))) % max(1, int(st_cfg.get("every", 1))) == 0)
                )
                if use_stat and int(st_cfg.get("beta_warmup") or 0) > 0:
                    n_act = (step - int(st_cfg.get("start_iter", 0))) // max(1, int(st_cfg.get("every", 1))) + 1
                    loss_mod.stat["beta"] = beta0 * min(1.0, n_act / int(st_cfg["beta_warmup"]))
                loss, fm, st = ddp(x1, c, use_stat)
                if anchor_ref:
                    drift = sum(((q - q0) ** 2).sum() for q, q0 in zip(field.parameters(), anchor_ref)) / n_anchor
                    loss = loss + anchor_w * drift
                opt.zero_grad(set_to_none=True)
                loss.backward()
                gnorm = torch.nn.utils.clip_grad_norm_(
                    field.parameters(), float(tcfg.get("grad_clip") or 1e9)
                )
                opt.step()
                sched.step()
                if ema is not None:
                    _ema_update(ema, field, min(ema_decay, (1 + step) / (10 + step)))
                step += 1
                acc["loss"] += float(loss.detach())
                acc["fm"] += float(fm)
                acc["stat"] += float(st)
                acc["n"] += 1
                acc["n_stat"] += int(use_stat)
                if step % log_every == 0 or step == total:
                    vec = torch.tensor(
                        [acc["loss"], acc["fm"], acc["stat"], acc["n"], acc["n_stat"]],
                        dtype=torch.float64,
                        device=device,
                    )
                    if world > 1:
                        dist.all_reduce(vec)
                    n = max(float(vec[3]), 1.0)
                    last = {
                        "loss": float(vec[0]) / n,
                        "loss_fm": float(vec[1]) / n,
                        "lr": float(sched.get_last_lr()[0]),
                        "grad_norm": float(gnorm),
                        "epoch": float(epoch),
                    }
                    if float(vec[4]) > 0:
                        last["loss_stationarity"] = float(vec[2]) / float(vec[4])
                    if main_rank:
                        logger.log(last, step)
                        LOG.info(
                            "it %d/%d  loss %.4f  fm %.4f%s  %.0f s",
                            step,
                            total,
                            last["loss"],
                            last["loss_fm"],
                            f"  stat {last['loss_stationarity']:.3e}" if "loss_stationarity" in last else "",
                            time.time() - t_start,
                        )
                    acc = {k: 0 if k.startswith("n") else 0.0 for k in acc}
                if (
                    main_rank
                    and val_ds is not None
                    and val_every
                    and (step % val_every == 0 or step == total)
                ):
                    vl = _val_loss(loss_mod, ema or field, val_ds, int(tcfg["batch_size"]), seed)
                    logger.log({"val_loss_fm": vl}, step)
                    last["val_loss_fm"] = vl
                stop = stopper.stop
                if world > 1:
                    flag = torch.tensor([float(stop)], device=device)
                    dist.all_reduce(flag, op=dist.ReduceOp.MAX)
                    stop = bool(flag.item() > 0)
                if main_rank and ((ckpt_every and step % ckpt_every == 0) or stop):
                    save_checkpoint(make_payload(False), workdir / "last.pt", last_uri)
                if stop:
                    LOG.warning("stop requested at iteration %d (checkpoint %s)", step, last_uri)
                    break
        finished = step >= total
        result: dict[str, Any] = {
            "run_name": run_name,
            "model_id": model_id,
            "steps": step,
            "total": total,
            "finished": finished,
            "metrics": last,
            "mlflow_run_id": logger.run_id,
            "n_params": n_params,
            "checkpoint_uri": None,
        }
        if main_rank:
            uri = save_checkpoint(
                make_payload(finished),
                workdir / ("final.pt" if finished else "last.pt"),
                final_uri if finished else last_uri,
            )
            if finished:
                save_checkpoint(make_payload(True), workdir / "last.pt", last_uri)
            result["checkpoint_uri"] = uri
            if bool((cfg.get("mlflow") or {}).get("log_checkpoint")):
                logger.artifact(workdir / ("final.pt" if finished else "last.pt"))
            if model_id:
                cat.call(
                    "update_model",
                    model_id,
                    checkpoint_uri=uri,
                    mlflow_run_id=logger.run_id,
                    hyperparams={**hyper, "final": last, "steps": step},
                )
            if finished and cfg["eval"].get("after_train") and model_id:
                result["evaluation"] = _evaluate_after_train(
                    cfg, space, ema or field, bundle, fixed, meta, cat, model_id, device
                )
        ok = True
        if job_id:
            cat.call("update_job", job_id, status="done" if finished else "cancelled")
        return result
    except BaseException:
        if job_id:
            cat.call("update_job", job_id, status="failed")
        raise
    finally:
        logger.close(ok)
        if world > 1 and dist.is_initialized():
            # No barrier: after the loop, rank 0 no longer performs collective operations (saving,
            # catalog, evaluation); waiting for its evaluation would exceed the NCCL timeout on a large model.
            dist.destroy_process_group()


@torch.no_grad()
def _val_loss(loss_mod: FlowMatchingLoss, field: nn.Module, ds: Any, batch: int, seed: int) -> float:
    """Validation flow matching loss (fixed noise and time: comparable from one time to the next)."""
    g = torch.Generator().manual_seed(seed + 12345)
    saved = loss_mod.field
    loss_mod.field = field
    try:
        tot, n = 0.0, 0
        for i in range(0, len(ds), batch):
            x1, c = ds.x[i : i + batch], ds.cond[i : i + batch]
            tot += float(loss_mod.fm_loss(x1, c, generator=g)) * x1.shape[0]
            n += x1.shape[0]
        return tot / max(n, 1)
    finally:
        loss_mod.field = saved


def _evaluate_after_train(
    cfg: Mapping[str, Any],
    space: FourierPotentialSpace,
    field: nn.Module,
    bundle: Any,
    fixed: Mapping[str, Any],
    meta: Mapping[str, Any],
    cat: _Catalog,
    model_id: str,
    device: torch.device,
) -> list[dict[str, Any]] | None:
    """Quick evaluation at the end of training (data points), recorded in the catalog."""
    from milady.eval.metrics import evaluate_model

    ev = cfg["eval"]
    model = GenerativeModel(
        space,
        copy.deepcopy(field),
        bundle.cond_specs,
        fixed,
        meta,
        device,
        int(cfg["sampling"].get("steps", 50)),
    )
    points = [dict(p) for p in (ev.get("points") or bundle.eval_points)][: int(ev.get("max_points", 6))]
    try:
        res = evaluate_model(
            model,
            points,
            n_samples=int(ev.get("n_samples", 32)),
            seed=int(ev.get("seed", 0)),
            steps=int(ev.get("steps", 50)),
            grid=ev.get("grid"),
            reference=bundle.info["data_uris"],
            n_ref=int(ev.get("n_ref", 128)),
            batch_size=int(ev.get("batch_size", 16)),
            cache_dir=cfg["data"].get("cache_dir"),
            catalog=cat.cat,
            model_id=model_id,
        )
    except Exception as exc:  # noqa: BLE001 — training is finished and saved: only warn
        LOG.warning("end-of-training evaluation impossible: %s", exc)
        return None
    return [{"point": r["point"], **r["metrics"]} for r in res]


# =============================================================================================
# Smoke test (infra/deploy/smoke.py)
# =============================================================================================
def smoke_step(data: Any, device: str = "cpu", workdir: str | None = None) -> dict[str, Any]:
    """One training iteration on snapshots of B ``(n_t, 3, n, n, n)`` (``make smoke``).

    Encodes B into a vector potential (kmax ≤ 4), fits the normalization, performs an AdamW step with the
    flow matching loss (reduced MLP, B → −B symmetry), checks the divergence of a decoded sample.
    """
    del workdir
    from milady.eval.metrics import divergence_relative

    dev = torch.device(device)
    b = torch.as_tensor(data, dtype=torch.float32).permute(0, 2, 3, 4, 1).contiguous()
    n = min(b.shape[1:4])
    space = FourierPotentialSpace(min(4.0, n // 2 - 1), ("magnetic_field",), symmetric_b=True).to(dev)
    x = space.encode({"magnetic_field": b.to(dev)})
    space.fit(x)
    torch.manual_seed(0)
    field = build_field(
        {
            "architecture": "mlp",
            "symmetry_b_sign": True,
            "mlp": {"width": 64, "depth": 2, "emb_dim": 32, "n_freq": 4},
        },
        space,
        0,
    ).to(dev)
    loss_mod = FlowMatchingLoss(field, space, [], {}).to(dev)
    opt = torch.optim.AdamW(field.parameters(), lr=1e-3)
    loss, _, _ = loss_mod(space.normalize(x), torch.zeros(x.shape[0], 0, device=dev))
    opt.zero_grad()
    loss.backward()
    opt.step()
    with torch.no_grad():
        z = heun_sample(
            field,
            torch.randn(2, space.n_modes, space.n_channels, device=dev),
            torch.zeros(2, 0, device=dev),
            steps=4,
        )
        bgen = space.decode(space.denormalize(z), n)["magnetic_field"]
    return {
        "loss": float(loss.detach()),
        "state_dict": {k: v.cpu() for k, v in field.state_dict().items()},
        "kmax": space.kmax,
        "div_rel": divergence_relative(bgen.cpu().numpy()),
        "n_modes": space.n_modes,
    }


# =============================================================================================
# Command line
# =============================================================================================
def _setup_logging(verbose: bool) -> None:
    rank = os.environ.get("RANK", "0")
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=f"%(asctime)s [rank {rank}] %(levelname)s %(name)s: %(message)s",
    )
    if rank != "0" and not verbose:
        logging.getLogger("milady").setLevel(logging.WARNING)


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point: ``python -m milady.train.fm3d`` (or via ``torchrun``)."""
    ap = argparse.ArgumentParser(
        prog="python -m milady.train.fm3d",
        description="Conditional 3D flow matching under constraints (vector potential).",
    )
    ap.add_argument("--config", default=None, help="training YAML (infra/configs/train_fm3d.yaml)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--dataset", default=None, help="catalog dataset (NAME or NAME:VERSION)")
    src.add_argument("--files", nargs="+", default=None, help="MFF files (paths, file://, s3://, .zarr)")
    ap.add_argument("--iters", type=int, default=None)
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=None)
    ap.add_argument("--lr", type=float, default=None)
    ap.add_argument("--device", default=None, help="auto (default), cpu, cuda")
    ap.add_argument("--run-name", default=None, help="run name (automatic resumption if a last.pt exists)")
    ap.add_argument(
        "--resume", default=None, help="auto (default), never, or path/URI of a checkpoint"
    )
    ap.add_argument("--init-from", default=None, help="initialization checkpoint (fine-tuning)")
    ap.add_argument("--no-catalog", action="store_true", help="do not register anything in the catalog")
    ap.add_argument("--db-url", default=None, help="catalog URL (default MILADY_DB_URL)")
    ap.add_argument(
        "--set",
        nargs="+",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="configuration overrides, e.g. --set train.lr=1e-4 stationarity.enabled=true",
    )
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    _setup_logging(args.verbose)
    cfg = load_config(args.config) if args.config else default_config()
    apply_overrides(cfg, [item for group in args.set for item in group])
    for key, val in (
        ("iters", args.iters),
        ("epochs", args.epochs),
        ("batch_size", args.batch_size),
        ("lr", args.lr),
        ("device", args.device),
    ):
        if val is not None:
            cfg["train"][key] = val
    if args.iters is not None:
        cfg["train"]["iters"] = args.iters
    elif args.epochs is not None:
        cfg["train"]["iters"] = None
    if args.no_catalog:
        cfg["catalog"]["enabled"] = False
    if args.db_url:
        cfg["catalog"]["url"] = args.db_url
    result = train(
        cfg,
        files=args.files,
        dataset=args.dataset,
        run_name=args.run_name,
        resume=args.resume,
        init_from=args.init_from,
    )
    if int(os.environ.get("RANK", "0")) == 0:
        print(json.dumps(result, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
