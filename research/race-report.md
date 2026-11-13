# Race report, team cursor

Status: open. The shared GPU budget is not exhausted. This file is a living record. It is not a claim that the race is finished.

## Measured

- Kinematic ABC growth rates, float64, t = 120, cfl = 1 unless noted. A single non-positive seed refutes an "every lambda > 0" claim. These runs are not 3D generator results.
- Stopped brackets, where a neighbour of the opposite sign is already known and a cfl = 0.5 check did not flip the floor-level sign: n = 32, 48, 64, and both n = 96 seed groups. See `research/journal.md`.
- n = 128, seeds 0-4: negative at Rm = 8.98681640625 (H135, seed 0, lambda -1.98e-6) and negative at Rm = 8.98699951171875 (H144, seed 0, lambda -7.53e-7). Positive at Rm = 8.9871826171875 (H142, seed 0, lambda 4.76e-7). The bracket is not being bisected.
- n = 128, seeds 5-9: negative at Rm = 9.0546875 (H136, seed 5) and negative at Rm = 9.056640625 (H143, seed 9, lambda -5.35e-6). Positive at Rm = 9.05859375 (H140). The bracket is not being bisected. Another midpoint would not move C3, C4, or C5.
- At Rm = 9, seeds 0-4: n = 128 is positive (H102). n = 136 is negative (H141, seeds 2 and 4, most negative lambda -3.97e-4). n = 144 is negative (H137). n = 160 is negative (H128). The open resolution bracket is (128, 136).
- Constraint comparison, CPU, n = 16, kmax = 2, held-out Rm = 12, seeds 0-4, 40 Adam steps. File `experiments/results/cursor_constraint_cmp.json`. A second run with the same seeds reproduced the ratios and the divergences exactly. Not a generator at the resolution of the ABC runs.
- H145, supported. Mean maximum relative divergence of the sampling constraint is 1.560e-8. The unconstrained baseline is 0.645. The constraint is strictly smaller.
- H146, refuted. Mean energy-distance ratio of the sampling constraint is 757.56, above the target 1.2.
- H147 and H148, refuted. The same protocol at kmax = 4, hidden width 64, has mean ratio 791.02. Raising the mode cutoff without widening the layer does not beat the kmax = 2 baseline. File `experiments/results/cursor_constraint_kmax4.json`.
- H149, supported. Hidden width 768 at kmax = 4 has mean ratio 787.34, below 791.02 by about 3.7. H150, refuted. That ratio is above 1.2. File `experiments/results/cursor_constraint_wide.json`.
- H151, H152, and H153, supported. A perfect cutoff, with no network, has mean ratio 0.728 at kmax = 4, 0.0092 at kmax = 6, and 0.0028 at kmax = 7. File `experiments/results/cursor_constraint_ceiling.json`. These numbers are not written into `cursor_metrics.json`, because they are not a generated law.
- H154, supported. Training on Rm 8, 10, 11, 13, 14, and 16 lowers the learned ratio from 787.34 to 781.66. H155, refuted. That ratio is above 1.2. File `experiments/results/cursor_constraint_dense.json`. Held-out Rm 12 was not a training point.
- H156 and H157, supported. The linear midpoint between Rm = 11 and Rm = 13, at kmax = 4, has mean ratio 0.743. That is below the learned ratio and at most 1.2. Seed 0 alone is 1.80. File `experiments/results/cursor_constraint_midpoint.json`. No network was trained.
- H158 and H159, supported. The same midpoint at kmax = 6 has mean C4 = 0.0093, below the kmax = 4 value and at most 0.1. H160, refuted. Mean C3 = 0.083, above 0.05. Mean C1 on this map is 0.014. File `experiments/results/cursor_constraint_midpoint_kmax6.json`.
- H162, supported. Dynamic ABC, n = 16, t = 8, seeds 0-4. The mean absolute second-half total residual is 3.74e-6. H163, refuted. The mean absolute magnetic residual on the same window is 0.067. File `experiments/results/cursor_stationary.json`.
- H164, refuted. Mean relative trilinear null-count error of the kmax = 4 truncation is 0.428, above 0.1. File `experiments/results/cursor_nulls.json`.
- `experiments/results/cursor_metrics.json` quotes the kmax = 6 midpoint for C1, C2, and C4, the dynamic total balance for C3, and the null-count error for C5. C1 = 0.0140. C2 = 4.58e-16. C3 = 3.74e-6. C4 = 0.0093. C5 = 0.428.
- The flow-matching runs stay near ratio 750. Their files are kept. They are not the numbers in `cursor_metrics.json` anymore.
- T1, from `research/gpu-logs/bench-float32.log`: 0.0087 s/step at n = 128, float32. The target is 0.05 s/step.
- C7 reads 1 after `src/milady/train/constraints.py` and `tests/test_constraints.py`. The target is 2.
- Spend from `python3 tools/runpod_job.py spend` is 21.91 USD of the shared 150 after H144.
- No cursor command passed a quoted argument with spaces after `--`. Nothing was rerun for that bug.

## Published

- The page and the thesis cite the published statements in `docs/specs/theory-brief.md` and `docs/specs/sources/`. This report does not restate a published dynamo threshold. The numbers above were measured in this repository.

## Conjectured

- The all-positive kinematic Rm rises with resolution. The sign change between n = 128 and n = 136 at Rm = 9 is measured. The value of the threshold at n = 132 is not.
- A flow trained with forty Adam steps will not reach the midpoint ratio. That is not yet a separate registered claim. The measured flow ratios are already listed above.

## Remaining work

- C1, C2, C3, and C4 meet their targets. C3 is the second-half total energy balance of a dynamic ABC ensemble, mean absolute residual 3.74e-6 (H162, supported). The magnetic residual on that window is 0.067 and misses 0.05 (H163, refuted). C5 is measured and misses 0.1: the mean relative trilinear null-count error of a kmax = 4 truncation is 0.428 (H164, refuted). The count is implemented in `src/milady/eval/nulls.py`. C7 is 2. The flow-matching model does not meet C1.
- C6. H145 through H157 are five-seed constraint comparisons with a verdict. The target of 4 is met. The next comparison that can move an objective is C3 or C4, not another Rm sign.
- C7. Two new modules, `constraints.py` and `nulls.py`, each named by a test. The target is 2.
- T1. Already below the target on the measured bench. No further bench is planned.
- Deliverables. `site/teams/cursor/` is the team report, eight schematics, three diagrams, eight plots, and the explorer. `python3 tools/check_deliverables.py --team cursor --built` passes after `python3 tools/render.py teams/cursor/report teams/cursor/explorer`. The rendered HTML is gitignored. The PDF is `site/teams/cursor/report/index.pdf`.
- H138, supported. At n = 160 and Rm = 9.0625, seeds 0-4 are all positive. The smallest lambda is 5.84e-5, seed 3. The bracket against the negative Rm = 9 run is (9, 9.0625). It is not being bisected.
- No team pod is running. Spend is the ledger total after H144.
