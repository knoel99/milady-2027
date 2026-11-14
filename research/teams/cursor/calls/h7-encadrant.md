single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H7, before any n = 32 or n = 48 energy residual. The dynamic budget of `test_energy_budget` holds at both resolutions, for Taylor-Green kf = 1 and ABC kf = 2, on seed 1 and on seeds 2, 3, 4 and 5.

Protocol check. The bounds are the ones in `tests/test_mhd3d.py`: rhs_abs_min > 0.05, rel_max < 0.01, scale_max < 1e-3, residuals finite. They were copied before a higher-resolution number existed. The n = 16 CPU smoke only checked that `experiments/cursor_energy_budget.py` reproduces that test. Those n = 16 residuals are not H7 points and do not move the bounds.

Verdict. UNCHECKED. The protocol can be run. No GPU point has been computed.
