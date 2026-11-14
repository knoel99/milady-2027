single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H168 is still registered. The first GPU attempt produced no energy-distance ratio. The bound stays 1.2.

| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Re-run of the quoted five-seed training | UNCHECKED | A pod is already running that protocol. Starting a second one would double the spend. `experiments/results/cursor_fm/metrics.json` does not exist. |
| The failed log is not a score | CONFIRMED | `research/gpu-logs/h168.log` ends on `RuntimeError` at the subtraction, exit code 1, 88 s. No ratio is printed. |
| The device fix is in the committed trainer | CONFIRMED | `experiments/cursor_fm_train.py` moves `data`, `cond`, `mean`, and `std` onto `device` before the subtraction. |
| The criterion was not softened | CONFIRMED | H168 in `research/hypotheses.json` is `registered`, verdict empty, refuted if the five-seed mean exceeds 1.2. |
| The kmax=6 midpoint baseline still matches the metrics file | CONFIRMED | Recomputed mean of `cursor_constraint_midpoint_kmax6.json` is 0.013966666402533533, equal to `cursor_metrics.json` field `c1`. |

Verdict on the claim as a whole. CONFIRMED that H168 has no result yet. The learned ratio itself is UNCHECKED until the running pod writes `metrics.json`.
