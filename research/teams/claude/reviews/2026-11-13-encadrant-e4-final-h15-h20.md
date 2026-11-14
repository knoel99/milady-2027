# Review by `encadrant` — commit 991d682: main run `e4_final`, hypotheses H15, H16, H17, H19, H20

Due review named by `tools/review_due.py`. Role `encadrant` (sub-agent, model and effort of the role file), 2026-11-13 00:24 UTC. Everything was recomputed by the role from `experiments/results/e4_mhd3d_s<k>*.json`, not from the digest; nothing was written to the repository.

## A. Integrity of the promoted set — CONFIRMED

1. Each of the 5 merged files holds 18 variants and 3 `h12` rows, device cuda, the right seed; the 25 part files equal the merged rows; the 18 "== variant" lines of each per-seed log match the JSON to print precision: the rename of the misnamed files mixed nothing.
2. Groups A and B against `replications/e4_gpu`: not bit-identical; the energy-distance ratio differs by at most 1.4e-8 relative, the restart drifts by at most 7.6e-5 relative.
3. `e4_selection.json` reproduces on 5 seeds; W9_skip_sym (8.863) is the argmin excluding G0 (3.952). The choice of W9 over W11 (9.158) is not significant: paired validation difference −0.29 ± 0.60.

## B. Hypotheses (held-out η, paired, SE over 5 seeds)

| Hypothesis | Verdict | Clauses |
|:---|:---|:---|
| H15 | REFUTED | Ratio W4c/W4 = 215.4/256.3 = 0.84, above 0.5: not met. Difference 40.9 ± 6.8 (6.0 SE), 5 of 5 seeds: both met. At the training η the difference is 0.34 ± 0.32. |
| H16 | CONFIRMED | G0 3.52 against W0–W6 at 177–519 (W3 lowest, 176.6); best per seed 153–194 against G0 3.36–3.70, 5 of 5. |
| H17 | CONFIRMED | Ratio W9/W4s = 9.35/209.8 = 0.045, below 0.2; difference 200.4 ± 2.2 (91 SE), 5 of 5; final loss of W9 1.18, below π/2. |
| H19 | REFUTED | Energy distance: W10 − G0 = +40.0 ± 0.26, not met. Restart drift of E_B: G0 − W10 = 0.090 ± 0.003, 5 of 5, met. Nulls: −0.229 ± 0.014, 0 of 5, not met. |
| H20 | REFUTED | Energy distance: W11 − G0 = +5.08 ± 0.22 (24 SE), 0 of 5, not met. Restart drift of E_B: 0.092 ± 0.003, 5 of 5, met. Nulls: 0.539 ± 0.014, 5 of 5, met. |

## C. Headline claim of the report draft — partly REFUTED

- "Factor of about twenty": CONFIRMED. W4s/W9 is 22.4 at the held-out η (15.5, 22.9, 27.8 per η) and 30.2 at the training η; W4s/W11 is 24.4; all seeds agree at every η.
- "G0 closer in energy distance": CONFIRMED, 5 of 5 seeds at all 8 values of η; the margin is thin at the training η = 0.08 (W9 − G0 = 0.41 ± 0.10).
- "Better than G0 only on the restart drift and the null count": REFUTED. The residual of the magnetic energy balance (`balance_residual_magnetic`) is 0.998 for G0 against 0.055 (W9) and 0.060 (W11), at every η and seed: a Gaussian law has essentially no mean magnetic production. This is a third advantage of W9 and W11, and the most physical one. And the restart drift of E_u goes the other way: G0 0.026 against 0.053 for W9 and W11, G0 better in 5 of 5 seeds; the claim holds for E_B only (0.212 against 0.124 and 0.120).
- "Worse on the energy balance and spectra": true in part. Total balance 0.0015 against 0.057 and 0.052; spectrum of B and helicity worse in 5 of 5 seeds at every η; spectrum of u not worse at η = 0.049 and 0.040.
- "W9 and W11 indistinguishable": CONFIRMED with one exception (training-η nulls: −0.022 ± 0.008, a 1.3 % effect).

## D. Objectives table — CONFIRMED

`race_metrics.py --all` matches the recomputation for W9: c1 9.349, c2 1.61e-8, c3 0.0567, c4 0.3405, c5 1.665, t1 0.1242, t2 0.0186.

## Defects by severity

1. Major: the headline and the abstract omit the magnetic balance, where G0 fails completely; "only on restart drift and nulls" is false.
2. Major: "restart drift" means E_B only in the criteria, T1, the digest and the tables; the E_u drift, which goes the other way, is stored and reported nowhere.
3. Medium: W9 is selected over W11 inside the noise; the report should say the selection is arbitrary between the two.
4. Medium: both null-count errors remain large (3.2 and 2.7 times the reference count): "better" is relative.
5. Minor: the H16 row of the digest uses the best variant by seed mean, the criterion asks for the best per seed; the verdict is unchanged.
6. Minor: uncommitted changes in `experiments/e4_report_tables.py` and the plots.

## What the main session did with it

Verdicts written to `research/hypotheses.json`. The magnetic energy balance and the restart drift of E_u were added to the comparative table, the plots and the explorer; the abstract, the results and the conclusion of the report were rewritten on defects 1 to 4.
