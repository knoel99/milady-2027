# Race report, team cursor

Status: open. The shared GPU budget is not exhausted. This file is a living record. It is not a claim that the race is finished.

## Measured

- Kinematic ABC growth rates, float64, t = 120, cfl = 1 unless noted. A single non-positive seed refutes an "every lambda > 0" claim. These runs are not 3D generator results.
- Stopped brackets, where a neighbour of the opposite sign is already known and a cfl = 0.5 check did not flip the floor-level sign: n = 32, 48, 64, and both n = 96 seed groups. See `research/journal.md`.
- n = 128, seeds 0-4: negative at Rm = 8.98681640625 (H135, seed 0, lambda -1.98e-6) and positive at Rm = 8.9871826171875 (H142, seed 0, lambda 4.76e-7). H144 tests the midpoint and is in flight.
- n = 128, seeds 5-9: negative at Rm = 9.0546875 (H136, seed 5) and negative at Rm = 9.056640625 (H143, seed 9, lambda -5.35e-6). Positive at Rm = 9.05859375 (H140). The bracket is not being bisected while C1 is far from its target.
- At Rm = 9, seeds 0-4: n = 128 is positive (H102). n = 136 is negative (H141, seeds 2 and 4, most negative lambda -3.97e-4). n = 144 is negative (H137). n = 160 is negative (H128). The open resolution bracket is (128, 136).
- Constraint comparison, CPU, n = 16, kmax = 2, held-out Rm = 12, seeds 0-4, 40 Adam steps. File `experiments/results/cursor_constraint_cmp.json`. A second run with the same seeds reproduced the ratios and the divergences exactly. Not a generator at the resolution of the ABC runs.
- H145, supported. Mean maximum relative divergence of the sampling constraint is 1.560e-8. The unconstrained baseline is 0.645. The constraint is strictly smaller.
- H146, refuted. Mean energy-distance ratio of the sampling constraint is 757.56, above the target 1.2.
- `experiments/results/cursor_metrics.json` holds the sampling-constraint aggregates. C1 = 757.56. C2 = 2.204e-8 (maximum over samples). C3 = 0.876 (mean absolute magnetic balance residual). C4 = 457.41 (relative L2 spectrum error plus relative helicity error). C5 is absent, so the command still prints the sentinel.
- T1, from `research/gpu-logs/bench-float32.log`: 0.0087 s/step at n = 128, float32. The target is 0.05 s/step.
- C7 reads 1 after `src/milady/train/constraints.py` and `tests/test_constraints.py`. The target is 2.
- Spend from `python3 tools/runpod_job.py spend` was about 20 USD of the shared 150 after H141, plus 0.365 USD for H143. In-flight pods are not in that sum until they finish.
- No cursor command passed a quoted argument with spaces after `--`. Nothing was rerun for that bug.

## Published

- The page and the thesis cite the published statements in `docs/specs/theory-brief.md` and `docs/specs/sources/`. This report does not restate a published dynamo threshold. The numbers above were measured in this repository.

## Conjectured

- The all-positive kinematic Rm rises with resolution. The sign change between n = 128 and n = 136 at Rm = 9 is measured. The value of the threshold at n = 132 is not.
- A Fourier vector-potential model may bring the energy-distance ratio down. That comparison is not yet registered, and this sentence is not a result.

## Remaining work

- C1, C3, and C4 are measured and far above their targets. The next comparison has to change the model, not the Rm grid. C2 is below 0.001 on this n = 16 run. C5 stays the sentinel until a Haynes–Parnell null count exists. None is implemented in `src/`.
- C6. H145 and H146 are the first two five-seed constraint comparisons with a verdict. The target is 4.
- C7. One new module. The target is 2.
- T1. Already below the target on the measured bench. No further bench is planned.
- Deliverables. `site/teams/cursor/` does not exist, so `tools/check_deliverables.py --team cursor --built` does not pass.
- In flight, and not stopped to write this file: H138 (n = 160, Rm = 9.0625) and H144 (n = 128, seeds 0-4).
