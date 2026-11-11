"""Forced incompressible 2D MHD solver of experiment E2: moved to ``milady.sim.mhd2d`` (re-exported here)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import milady  # noqa: F401
except ImportError:  # repository checkout without `pip install -e .`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from milady.sim.mhd2d import MHD2D  # noqa: E402, F401

__all__ = ["MHD2D"]
