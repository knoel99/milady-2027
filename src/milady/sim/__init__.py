"""MilaDy simulations: 3D MHD solver (``milady.sim.mhd3d``) and execution of a campaign simulation
(``milady.sim.run``).

This module stays lightweight (neither torch nor numpy): it only contains the resolution of the physical
parameters of a campaign point, shared by ``milady.sweep`` (which registers the simulations
in the catalog) and ``milady.sim.run`` (which runs them), so that the two register exactly
the same parameters.

Supported codes:

- ``mhd3d_torch``  : :mod:`milady.sim.mhd3d` (PyTorch, CPU/GPU);
- ``mhd2d_numpy``  : 2D solver of the experiments (``experiments/mhd2d.py``, NumPy, CPU).

Nondimensionalization (3D): reference velocity ``U_ref`` (default 1, amplitude of the imposed flow
or of the forcing), reference length ``L_ref`` = 1/k_f (k_f = 2π kf / L, default 1/kf in the box
2π); Re = U_ref L_ref / ν, Rm = U_ref L_ref / η, Pm = ν/η = Rm/Re. For the ABC flow
(A = B = C = 1, kf = 1), Rm = 1/η: convention of Arnold & Korkina and of Galloway & Frisch, the one
of ``experiments/e3_abc.py``.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

__all__ = ["CODES", "NONDIM_2D", "NONDIM_3D", "SOLVER_KEYS_2D", "SOLVER_KEYS_3D", "physical_parameters"]

#: Known simulation codes (value of ``code`` in a campaign).
CODES = ("mhd3d_torch", "mhd2d_numpy")

#: Parameter keys accepted per code (fixed or swept); any other key is rejected.
SOLVER_KEYS_3D = frozenset(
    {
        "mode", "flow", "forcing", "nu", "eta", "Re", "Rm", "Pm", "kf", "U_ref", "L_ref",
        "abc_A", "abc_B", "abc_C", "forcing_amp", "eps", "kf_min", "kf_max",
        "u0", "u0_amp", "u_noise", "b0_amp", "b0_kwidth", "renormalize", "renorm_every",
        "project_every", "seed",
    }
)  # fmt: skip
SOLVER_KEYS_2D = frozenset(
    {"nu", "eta", "Re", "Rm", "Pm", "alpha", "eps_u", "eps_b", "kf_min", "kf_max", "seed"}
)

NONDIM_3D = (
    "Periodic box [0, L)³; B in Alfvén units (B/√(μ₀ρ), same unit as u); U_ref = amplitude of "
    "the imposed flow or of the response targeted by the forcing, L_ref = 1/k_f with k_f = 2π kf/L; "
    "Re = U_ref L_ref/ν, Rm = U_ref L_ref/η, Pm = ν/η; time in units of L_ref/U_ref. "
    "ABC/TG forcing: f = forcing_amp × shape; |k|² = eigenvalue of −∇² of the shape (k_f² for ABC, "
    "3 k_f² for TG); “laminar”: forcing_amp = ν |k|² U_ref (Stokes response of amplitude U_ref), "
    "“turbulent”: forcing_amp = |k| U_ref² (targets u_rms ~ U_ref in the turbulent regime, order of magnitude)."
)
NONDIM_2D = (
    "Periodic domain [0, 2π)²; B in Alfvén units; ν and η dimensionless (inverses of "
    "Reynolds numbers built on length 1 and velocity 1); white-in-time forcing with mean injection rates "
    "eps_u (vorticity) and eps_b (potential), band kf_min ≤ |k| ≤ kf_max; linear friction α."
)


def _num(v: Any, name: str) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise TypeError(f"parameter {name}: number expected, got {v!r}")
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(f"parameter {name}: non-finite value {v!r}")
    return x


def physical_parameters(
    code: str, point: Mapping[str, Any], grid: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Complete parameters of a campaign point (fixed + swept), in a stable order.

    Fills in the derived parameters: ν and η from (Re, Rm) or (Re, Pm); Re, Rm, Pm from
    ν and η; numerical forcing amplitude (``laminar`` or ``turbulent`` rule). The values
    returned are those recorded in the catalog (``parameters`` column) and in the MFF file
    (``milady_parameters`` and The Well attributes). Raises ``ValueError`` for an unknown key or an
    incomplete combination, ``TypeError`` for a non-numeric value where a number is expected.
    """
    if code == "mhd3d_torch":
        return _params_3d(point, grid or {})
    if code == "mhd2d_numpy":
        return _params_2d(point)
    raise ValueError(f"code {code!r} unknown (expected: {', '.join(CODES)})")


def _params_3d(point: Mapping[str, Any], grid: Mapping[str, Any]) -> dict[str, Any]:
    unknown = set(point) - SOLVER_KEYS_3D
    if unknown:
        raise ValueError(
            f"unknown parameters for mhd3d_torch: {sorted(unknown)} (accepted: {sorted(SOLVER_KEYS_3D)})"
        )
    p = dict(point)
    mode = str(p.pop("mode", "dynamic"))
    if mode not in ("dynamic", "kinematic"):
        raise ValueError(f"mode {mode!r}: dynamic or kinematic")
    kf = _num(p.pop("kf", 1), "kf")
    if kf != int(kf) or kf < 1:
        raise ValueError("kf: integer ≥ 1 (index of the forcing / flow mode)")
    domain = float(grid.get("domain", 2 * math.pi)) if grid else 2 * math.pi
    k_phys = 2 * math.pi * kf / domain
    U = _num(p.pop("U_ref", 1.0), "U_ref")
    L = _num(p.pop("L_ref", 1.0 / k_phys), "L_ref")
    Re = p.pop("Re", None)
    Rm = p.pop("Rm", None)
    Pm = p.pop("Pm", None)
    nu = p.pop("nu", None)
    eta = p.pop("eta", None)
    # ν
    if nu is not None:
        nu = _num(nu, "nu")
    elif Re is not None:
        nu = U * L / _num(Re, "Re")
    elif Pm is not None and (eta is not None or Rm is not None):
        eta_ = _num(eta, "eta") if eta is not None else U * L / _num(Rm, "Rm")
        nu = _num(Pm, "Pm") * eta_
    elif mode == "kinematic":
        nu = 0.0
    else:
        raise ValueError("dynamic mode: specify nu, Re, or Pm together with (eta or Rm)")
    # η
    if eta is not None:
        eta = _num(eta, "eta")
    elif Rm is not None:
        eta = U * L / _num(Rm, "Rm")
    elif Pm is not None and nu > 0:
        eta = nu / _num(Pm, "Pm")
    else:
        raise ValueError("specify eta, Rm, or Pm together with (nu or Re)")
    if eta <= 0 or nu < 0:
        raise ValueError("nu ≥ 0 and eta > 0 required")
    out: dict[str, Any] = {"mode": mode}
    if mode == "kinematic":
        out["flow"] = str(p.pop("flow", "abc"))
        p.pop("forcing", None)
    else:
        out["forcing"] = str(p.pop("forcing", "abc"))
        p.pop("flow", None)
    out.update({"nu": nu, "eta": eta})
    if nu > 0:
        out["Re"] = U * L / nu
    out["Rm"] = U * L / eta
    if nu > 0:
        out["Pm"] = nu / eta
    out.update({"kf": kf, "U_ref": U, "L_ref": L})
    flow_kind = out.get("flow") or out.get("forcing")
    if flow_kind == "abc":
        for key in ("abc_A", "abc_B", "abc_C"):
            out[key] = _num(p.pop(key, 1.0), key)
    else:
        for key in ("abc_A", "abc_B", "abc_C"):
            p.pop(key, None)
    if mode == "dynamic" and out["forcing"] in ("abc", "tg"):
        rule = p.pop("forcing_amp", "laminar")
        k_shape2 = k_phys**2 * (1.0 if out["forcing"] == "abc" else 3.0)  # −∇² of the ABC or TG shape
        if rule is None or rule == "laminar":
            out["forcing_amp"] = nu * k_shape2 * U
            out["forcing_rule"] = "laminar"
        elif rule == "turbulent":
            out["forcing_amp"] = math.sqrt(k_shape2) * U * U
            out["forcing_rule"] = "turbulent"
        else:
            out["forcing_amp"] = _num(rule, "forcing_amp")
            out["forcing_rule"] = "fixed"
    else:
        p.pop("forcing_amp", None)
    if mode == "dynamic" and out["forcing"] == "random":
        out["eps"] = _num(p.pop("eps", 0.1), "eps")
        out["kf_min"] = _num(p.pop("kf_min", 1.0), "kf_min")
        out["kf_max"] = _num(p.pop("kf_max", 2.5), "kf_max")
    else:
        for key in ("eps", "kf_min", "kf_max"):
            p.pop(key, None)
    defaults: dict[str, Any] = {"b0_amp": 1.0 if mode == "kinematic" else 1e-3}
    if mode == "dynamic":
        defaults.update({"u0": "laminar", "u0_amp": U, "u_noise": 0.0})
    for key, default in defaults.items():
        val = p.pop(key, default)
        out[key] = val if isinstance(val, str) else _num(val, key)
    for key in ("u0", "u0_amp", "u_noise") if mode == "kinematic" else ():
        p.pop(key, None)
    out.update(p)  # remaining: b0_kwidth, renormalize, renorm_every, project_every, seed
    return out


def _params_2d(point: Mapping[str, Any]) -> dict[str, Any]:
    unknown = set(point) - SOLVER_KEYS_2D
    if unknown:
        raise ValueError(
            f"unknown parameters for mhd2d_numpy: {sorted(unknown)} (accepted: {sorted(SOLVER_KEYS_2D)})"
        )
    p = dict(point)
    nu = _num(p.pop("nu"), "nu") if "nu" in p else 1.0 / _num(p.pop("Re"), "Re") if "Re" in p else None
    p.pop("Re", None)
    eta = p.pop("eta", None)
    Rm, Pm = p.pop("Rm", None), p.pop("Pm", None)
    if eta is not None:
        eta = _num(eta, "eta")
    elif Rm is not None:
        eta = 1.0 / _num(Rm, "Rm")
    elif Pm is not None and nu is not None:
        eta = nu / _num(Pm, "Pm")
    if nu is None and Pm is not None and eta is not None:
        nu = _num(Pm, "Pm") * eta
    if nu is None or eta is None:
        raise ValueError("mhd2d_numpy: specify (nu or Re) and (eta, Rm or Pm)")
    out: dict[str, Any] = {
        "nu": nu,
        "eta": eta,
        "Re": 1.0 / nu,
        "Rm": 1.0 / eta,
        "Pm": nu / eta,
        "alpha": _num(p.pop("alpha", 0.02), "alpha"),
        "eps_u": _num(p.pop("eps_u", 0.05), "eps_u"),
        "eps_b": _num(p.pop("eps_b", 0.05), "eps_b"),
        "kf_min": _num(p.pop("kf_min", 2.0), "kf_min"),
        "kf_max": _num(p.pop("kf_max", 3.0), "kf_max"),
    }
    out.update(p)  # seed
    return out
