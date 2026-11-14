# Review by `encadrant` — commit 133934a: second width scan (H21), G1 on the second data realisation

Due review named by `tools/review_due.py`. Role `encadrant` (sub-agent, model and effort of the role file), 2026-11-13 03:50 UTC. Everything recomputed from the group JSON files; nothing written or trained.

## 1. H21: REFUTED as registered

Held-out ED / floor, per seed (0–4), `experiments/results/replications/e4_scan2`:

| Variant | Per seed | Mean ± SE | FM loss |
|---|---|---|---|
| S_w512 | 205.6, 203.4, 206.7, 205.2, 205.8 | 205.33 ± 0.54 | 1.613 |
| S_w2048 | 26.5, 25.3, 25.7, 24.4, 26.1 | 25.61 ± 0.36 | 1.222 |
| S_w5632 | 94.7, 83.8, 102.3, 114.4, 127.0 | 104.44 ± 7.52 | 0.777 |
| S_w512_long | 214.3, 212.8, 221.7, 210.7, 217.9 | 215.48 ± 1.94 | 1.525 |
| S_w2048_long | 57.3, 53.4, 55.8, 59.4, 68.2 | 58.84 ± 2.55 | 0.949 |

- Clause 1 (order) triggered: 2048 − 5632 = −78.8 ± 7.6, negative in 5 of 5 seeds. Clause 2 (one fifth) triggered: 5632/512 = 0.51 (per seed 0.41–0.62). Clause 3 (long below half) not triggered: ratio 1.05.
- Git order CONFIRMED: criterion and builder unchanged since 5027f7c; first results at d7aa2bd.
- Pooling of the three jobs CONFIRMED: reference and floors differ by at most 8.9e-11 between jobs; G0 identical per seed across the second scan, the first scan and the main run. Seed 4 ran on another GPU: W9 is 8.41 there against 8.89 in the main run; seeds 0–3 reproduce the main run to 1e-11.
- The first scan agrees on the conclusions (205.59 and 25.29); it is not seed-reproducible for width 5632 (83.8 against 90.6, 127.0 against 106.5).

## 2. Statements of the report

- (a), (b), (c) CONFIRMED: W9 9.25, factor 22.2, 512 − W9 = 196.1 ± 0.8.
- (d) numbers CONFIRMED, wording REFUTED: at width 512 the long training is slightly worse (+10.2 ± 1.6, 5 of 5), not "the law does not move"; at 2048, +33.2 ± 2.5, 5 of 5.
- (e) CONFIRMED: training-η ratios 165.8, 25.8, 70.0; 5632 above 2048 and below 512 in all 15 seed × η cells of both splits.
- (f) omissions: S_w5632 has the best null-count error of any network (0.96 against 2.01 at width 2048 and 1.67 for W9, 5 of 5 seeds) and the best magnetic balance (0.037), and the worst restart drift of E_B (0.45); S_w2048 beats W9 on the restart drift of E_B (0.072 against 0.124, 5 of 5) and on the total energy residual (0.012 against 0.057). The long runs improve nothing notable.

## 3. H22 on the second realisation: CONFIRMED

Magnetic balance of G1 0.0718 (per seed 0.070–0.074); restart drift of E_B, W9 − G1 = 0.0638 ± 0.0052 (12.4 SE), 5 of 5; null-count error, W9 − G1 = 0.556 ± 0.023 (24 SE), 5 of 5. The sentence of the report is confirmed (1.98, 8.07, 2.90, 0.072, 1.00 against 1.56, 0.063 against 0.126); the data are those of `e4_indep`.

## Defects by severity

1. "The explicit affine term at width 512 does better than any width tried" holds for the energy distance only.
2. "Does not move" (width 512, long) should read "slightly worse".
3. "The law gets worse" for the long training at width 2048 is not true at every η: the damage sits at η = 0.03.
4. "Same outcome" for G1 omits that, on this realisation too, W9 is better on the magnetic balance (0.050 against 0.072) and G1 worse on the restart drift of E_u (0.081 against 0.059).
5. The group S result files record `cond_scale` 8.0 (the default of the run) while the builders of these variants fix it to 0.5.
6. The register entry of H21 is still "registered".

## What the main session did with it

H21 recorded as refuted; defects 1–5 corrected in the report (wording and a note on `cond_scale`).
