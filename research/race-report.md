# Race report, team cursor

Status: open. The shared GPU budget is not exhausted, and several objectives are still the sentinel. This file is a living record. It is not a claim that the race is finished.

## Measured

- Kinematic ABC growth rates, float64, t = 120, cfl = 1 unless noted. A single non-positive seed refutes an "every lambda > 0" claim. These runs are not 3D generator results.
- Stopped brackets, where a neighbour of the opposite sign is already known and a cfl = 0.5 check did not flip the floor-level sign: n = 32, 48, 64, and both n = 96 seed groups. See `research/journal.md`.
- n = 128, seeds 0-4: negative at Rm = 8.98681640625 (H135, seed 0, lambda -1.98e-6) and positive at Rm = 8.9871826171875 (H142, seed 0, lambda 4.76e-7). H144 tests the midpoint and is in flight.
- n = 128, seeds 5-9: negative at Rm = 9.0546875 (H136) and positive at Rm = 9.05859375 (H140). H143 tests the midpoint and is in flight.
- At Rm = 9, seeds 0-4: n = 128 is positive (H102). n = 136 is negative (H141, seeds 2 and 4, most negative lambda -3.97e-4). n = 144 is negative (H137). n = 160 is negative (H128). The open resolution bracket is (128, 136). It was not bisected, because C1–C5 were still the sentinel.
- T1, from `research/gpu-logs/bench-float32.log`: 0.0087 s/step at n = 128, float32. The target is 0.05 s/step.
- Spend from `python3 tools/runpod_job.py spend` was about 20 USD of the shared 150 after H141. In-flight pods are not in that sum until they finish.
- No cursor command passed a quoted argument with spaces after `--`. Nothing was rerun for that bug.

## Published

- The page and the thesis cite the published statements in `docs/specs/theory-brief.md` and `docs/specs/sources/`. This report does not restate a published dynamo threshold. The numbers above were measured in this repository.

## Conjectured

- The all-positive kinematic Rm rises with resolution. The sign change between n = 128 and n = 136 at Rm = 9 is measured. The value of the threshold at n = 132 is not.
- A sampling constraint that removes the longitudinal Fourier component should lower the relative divergence of a small flow model. H145 states that comparison and was registered before the run. It is not yet a result.

## Remaining work

- C1–C5. Baseline `none`. `experiments/cursor_objectives.py` still prints the sentinels, because `experiments/results/cursor_metrics.json` does not exist. H145 and H146 are the next measurement: two constraint mechanisms, five seeds, held-out Rm = 12, on CPU at n = 16. C5 stays the sentinel until a Haynes–Parnell null count exists. None is implemented in `src/`.
- C6. Zero hypotheses have a `CONFIRMED` or `REFUTED` verdict that also compares a constraint with a baseline on five seeds. Rm-sign results are not rewritten to count.
- C7. Zero new modules under `src/milady` relative to `origin/main` are named by a test. `src/milady/train/constraints.py` is the candidate. It counts only after it is committed and the test names it.
- T1. Already below the target on the measured bench. No further bench is planned.
- Deliverables. `site/teams/cursor/` does not exist, so `tools/check_deliverables.py --team cursor --built` does not pass.
- In flight, and not to be stopped to write this file: H138 (n = 160, Rm = 9.0625), H143 (n = 128, seeds 5-9), H144 (n = 128, seeds 0-4).
