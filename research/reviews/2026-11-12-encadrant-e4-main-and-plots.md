# Review by `encadrant` — commit 8184bc9: job `e4_main`, result-file bug, plots script

Due review named by `tools/review_due.py` (3 commits on results since 23:10 UTC). Role `encadrant` (sub-agent, model and effort of the role file), 2026-11-12 23:39 UTC. Text of the role, shortened only by the removal of its scratch paths.

## Verdicts

1. **`e4_gpu` and `e4_main` agree — CONFIRMED, but vacuous.** Recomputed from the JSON with `per_seed`: every seed mean of the test `ed_ratio` is identical in the two sets (difference 0 for all 13 variants on test, validation and training η); the ranking is identical. Leaf by leaf, 2600 of 2681 evaluation leaves per seed are bit-identical; only the `restart_*` leaves differ, by at most 7.6e-5 relative. `e4_data.json` and `e4_reference.json` differ only in wall times. `e4_main` is a deterministic re-run (same data seeds `1000 + index`, same model seeds, same GPU model), not an independent replication: the 2 SE test carries no information.
2. **The bug of the `tag` loop variable.** (a) CONFIRMED with a wording error: at 62e31c9, line 557 has `for tag, keys in …`, whose last value `"ab"` gives `e4_mhd3dab_*`; the rebind comes after `W5_control_half`, not "after W7". (b) CONFIRMED: the 13 rows per seed are present, the merged file equals parts A + B, `h14` is identical to `e4_gpu`, `h12` is empty. (c) CONFIRMED: the test fails on a copy of the 62e31c9 script and passes on HEAD.
3. **`e4_gpu` was not affected — CONFIRMED.** Each of its 5 files holds 13 variants and 3 `h12` rows with the `tilt_a/b/ab` keys; H12 recomputed: 0.238 ± 0.095, r_b/r_a = 0.504, 0 of 5 seeds, as in the earlier review.
4. **`runpod_job.py exec` refuses another team's pod — CONFIRMED** (lines 462–464 and the test; no API call made).
5. **`e4_plots.py` states the data correctly — REFUTED**, defects below.

## Defects, by severity

1. `e4_main` must not be called a second or independent replication, nor pooled into 10 seeds: it is a bitwise reproducibility check of groups A and B on a second pod. An independent replication needs other data seeds.
2. `plot_floors` plots `traj_split_512["mean"]` (20 splits) under the label "used for the ratio"; the ratio uses the first 10 splits (`mean_first_10` = `ed_floor_512`); the gap is −20 % to +19 %.
3. `mean_se` returns SE = 0 for one seed and drops NaN seeds silently: a variant with fewer than 5 seeds shows an under-sized bar. Print n; no bar when n < 5 (rule 4).
4. Bars on log axes with a floating baseline (`plot_long`, `plot_scan`, `plot_tradeoff`): the bar lengths mean nothing. Use points, or a linear axis from 0.
5. `plot_nulls` fits over another list of variants than the digest's H13 fit (slope 4.85 over 120 points against 4.87 over 135): use the same list.
6. Running the plots writes into the results: `load()` calls `merge()`, which rewrites the merged files.
7. Journal entry of 23:35: "C–E lost for seeds 2–4" is inexact; `e4_main` has no C–E file for any of the five seeds.
8. Minor: `merge` counts the duration of an `all` run twice; `exec` caps the timeout at 25 s silently and returns 0 when the exit code is missing; the convergence caption omits the "same hardware" series; the axis title "k²H(k)" for `J_shell` is approximate.

Not checked: GPU re-training, the copy loop on the pod of `e4_final`, plots on final data (not on disk yet).

## What the main session did with it

Defects 1–8 corrected in the commit that adds this file (journal entry of 23:55 UTC); an independent replication with other data seeds (`E4_DATA_SEED`) is launched.
