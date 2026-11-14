# Review by `encadrant` — commit d7aa2bd: long trainings (H18), independent replication, first width scan

Due review named by `tools/review_due.py`. Role `encadrant` (sub-agent, model and effort of the role file), 2026-11-13 01:35 UTC. Everything recomputed by the role from the group JSON files with a read-only loader; nothing retrained, nothing written.

## 1. `e4_final_long`

**H18: CONFIRMED (not refuted)**, clause by clause, G0 − W9L, held-out η, 5 seeds: restart drift of E_B 0.070 ± 0.011 (6.4 SE), 5 of 5; null-count error 0.856 ± 0.035 (25 SE), 5 of 5. Caveats on the wording: W9 at the base budget already meets both clauses (drift 0.124, nulls 1.67 against 0.212 and 2.24); the long training does not improve the drift (W9L − W9 = +0.018 ± 0.010); at η = 0.033 the drift gain vanishes (0.008 ± 0.019, 3 of 5); the E_u drift is worse than that of G0 in 5 of 5 seeds (−0.052 ± 0.009).

- (a) CONFIRMED: G0, W9, W10 and W11 are bit-identical to the main run (1205 of 1205 stored scalars each, and the losses); training times differ, so they were recomputed, not copied.
- (b) CONFIRMED in every seed: loss 1.176 → 1.075 (W9) and 1.174 → 1.075 (W11); held-out ED ratio 18.8 ± 1.4 and 19.5 ± 1.5 against 9.35 and 8.60 (paired +9.4 ± 1.3 and +10.9 ± 1.6, 5 of 5); training η 11.9 and 12.0 against 5.5 (3 of the 6 training η are evaluated). Robust: not carried by one seed or one η; the size comes mostly from η = 0.033; at η = 0.0725 W11L is not separable.
- (c) Partly REFUTED: nulls 1.38 and 1.41 against 1.67 and 1.70 (5 of 5), magnetic balance 0.049 and 0.043, total balance 0.057 → 0.096 and 0.052 → 0.098 (5 of 5): confirmed. "Restart drifts get worse" fails for E_B of W9L (1.7 SE, 3 of 5); W11L E_B is at 2.0 SE; E_u is at 2.7 SE (5 of 5) and 2.2 SE (4 of 5). Replacement: "the E_u drift rises; the E_B drift is not separable for W9L".

## 2. `e4_indep`

- (a) CONFIRMED: `data_seed_offset` is 100; every value differs; over 66 comparisons the rms z is 1.16, 8 above 2, mostly at η = 0.0444.
- (b) CONFIRMED, with one wording REFUTED: Spearman 0.963 over 18 variants; all 8 inversions involve the half-sample or tilted rows; the 15 other variants keep their order. W4s/W9 = 23.3 (main 22.4); G0 (2.90) below W9 (8.20) and W11 (7.28) in 5 of 5 seeds; W10 43.3 ± 0.2; no verdict of H4–H7, H9–H17, H19, H20 changes; H8 stays not discriminating. New: W9 − W11 = 0.91 ± 0.18 (main 0.75 ± 0.51).
- (c) REFUTED as worded: the factor 1.61 between the floors at η = 0.0725 is right, but the ratios move from −18 % (G0) to +12 %, and for G0, W9 and W11 the raw distance itself moves by −8, −11 and −13 %: the floors are not the main cause.

## 3. `e4_final_scan` (no verdict on H21)

- Losses of S_w512: CONFIRMED, 1.601–1.614 (mean 1.608 ± 0.002), above π/2.
- Matched control: CONFIRMED (`experiments/e4_mhd3d.py`: both are `SignSymmetrized` ResMLP 512 × 4 with `cond_scale` 0.5, same seed, iterations, learning rate and batch; the only difference is `ModewiseAffineSkip`). S_w512/W9 = 21.9 (205.6 ± 0.5 against 9.40 ± 0.19; per seed 20.3–23.1).
- "1.60–1.63" for W0, W4, W4s: NOT CHECKABLE (not stored in the JSON).

## Defects by severity

1. Report, replication paragraph: range and causal attribution wrong (item 2c).
2. "In the same order" needs the half-sample and tilted rows excluded.
3. "Restart drifts get worse" overstates the E_B result.
4. The H18 statement credits the long training for what W9 already achieves.
5. W9 in the scan job differs from the main run by up to 7.7 % per seed: "to the last digit" applies to the long job only.
6. At 2 seeds: S_w512_long has a loss of 1.53, below π/2, with a ratio of 216; S_w5632 a loss of 0.77 with a ratio of 98.6: the loss does not track the distance.

## What the main session did with it

H18 verdict written to the register with its caveats; the three sentences of the report corrected (long trainings, replication, order).
