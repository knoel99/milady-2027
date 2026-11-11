"""Evaluation of MilaDy generative models: physical metrics and distances between distributions.

``milady.eval.metrics``: relative divergence, E_u(k) and E_B(k) spectra in shells, kinetic /
magnetic / cross helicities, energy budgets (injection, dissipations, magnetic production) and
their residuals in distribution, energy distance (Székely), sliced Wasserstein; evaluation of a trained model
with registration in the catalog.

Command line: ``python -m milady.eval --config infra/configs/train_fm3d.yaml [--model <uuid>]``
(equivalent to ``python -m milady.eval.metrics``).
"""

from __future__ import annotations

from milady.eval.metrics import (
    compare_ensembles,
    divergence_relative,
    energy_budget,
    energy_distance,
    energy_spectrum,
    features,
    helicities,
    sliced_wasserstein,
)

__all__ = [
    "compare_ensembles",
    "divergence_relative",
    "energy_budget",
    "energy_distance",
    "energy_spectrum",
    "features",
    "helicities",
    "sliced_wasserstein",
]
