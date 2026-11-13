# Encadrant review of commits 3abe952, bf0198e, 1312fb6 (E4, team claude)

Text returned by the `encadrant` role (read-only), saved by the main session. The role reached its turn limit before handing back and was
asked to deliver its report from the checks already made. Everything was recomputed from
`experiments/results/replications/e4_nongauss{,_indep}/e4_mhd3d_s<k>_<group>.json` and `e4_reference.json`, not from the digest. "Main" is
`e4_nongauss`; "repl." is `e4_nongauss_indep`.

**Headline:** the digest, every number recomputed, and the R1-R6 and jury A/B/C rewordings are confirmed. Seven sentences still say more
than the data (five in the report, two of them repeated in the race report, plus two of the race report's own), and the H28 criterion has
loopholes to close before the full run. No error seen in `FullGaussianAnchoredField` or in group F.

Side effects and scope: no tracked file edited; `digest.py` run on a copy of `experiments/` in the scratchpad; `e4_mhd3d.py` not run (only
its `--quick` output read, not quotable); the test passed (1 passed); the uncommitted `moment_recolouring` work was not reviewed.

## 1. Report `site/teams/claude/report/index.qmd`

### Rewordings

| Item | Verdict | Evidence |
|---|---|---|
| R1 (sec-nongauss, discussion, limits "Metrics") | CONFIRMED | Drift at τ = 4 of 0.124 against 0.170 is now stated in all three places. |
| R2 (paragraph on H18) | CONFIRMED | 0.170 / 0.212 / 0.124 / 0.064 as asked. |
| R3 (abstract and four other places) | CONFIRMED, one imprecision | No "every law" is left in the report. See S2 for "at or below". |
| R4 (limits) | CONFIRMED | "barely separates (0.43 floors, about twice the sampling value; 0.6 to 0.9 floors farther)". |
| R5 | CONFIRMED | Restart is scoped to held-out η, where G1 is interpolated. |
| R6 and the two captions | CONFIRMED | "about a fifth" is 0.270 / 1.270 = 0.213. "more than a quarter … at the smallest η" is −0.308 at η = 0.03. |
| Jury A | CONFIRMED | See S3 for one word. |
| Jury B | CONFIRMED as applied | Two of the jury's own wordings do not survive the files: S1 and S4. |
| Jury C | CONFIRMED | "the right topology" is dropped; the G1 anchor is "a hypothesis, registered as H28 and not yet run". |
| Jury minor points | CONFIRMED except one | The common uncertainty of the null count: see S6. |

### Recomputed figures

| Sentence | Verdict | Figures (keys) |
|---|---|---|
| Mean-flow part "too small by 0.15, 0.13 and 0.13"; third-order part "off by −0.06, +0.06 and +0.15"; "under-produces by 21 %" | CONFIRMED | `prod_mean_over_d` of W9 minus reference: −0.151, −0.130, −0.134. `prod_fluct_over_d`: −0.060, +0.055, +0.152. `prod_over_d` 0.789. Repl.: −0.130, −0.121, −0.158 and −0.072, +0.051, +0.161. |
| Residual "0.055 against 0.072 for G1" | CONFIRMED | Mean of abs(`balance_residual_magnetic`): 0.0553 and 0.0720. |
| W10 "0.3 and 0.2 times that of the reference at the two lower η" | CONFIRMED | 0.31 and 0.24 (repl. 0.33 and 0.22); opposite sign at η = 0.0725 in 5 of 5 seeds. |
| "gain 0.07 … gains 0.29" | Numbers CONFIRMED, inference REFUTED | W12 −0.173 to −0.107 (0.066); S_w2048 −0.0977 to −0.0331 (0.065); S_w5632 −0.344 to −0.0576 (0.286). See S1. |
| "largest at η = 0.0725 (0.039 ± 0.008), where both have a production of 0.79" | CONFIRMED | 0.0385 ± 0.0076, 5 of 5 seeds; P/D 0.790 and 0.789. Repl. 0.0433 ± 0.0051. See S4. |
| W9 at the training η: "+0.008, −0.069 and −0.121, that is 0.06, 0.73 and 0.39" | CONFIRMED | 0.0082 (0.059), −0.0693 (0.728), −0.1206 (0.392), 5 of 5 seeds. Repl. 0.0079 (0.062), −0.0690 (0.745), −0.1336 (0.422). |
| "the lowest ratio, G1 at the smallest held-out η, is 1.8" | CONFIRMED on main only | 1.801; repl. 1.69; training η = 0.03: 1.60 on both. See S5. |
| "Twenty-eight … twenty-five of them in this experiment (H4 to H28) … H28 registered and not yet run" | CONFIRMED | 28 entries; H4-H28 = 25; H28 `registered`. |
| "Twenty-four hypotheses were registered and decided" | CONFIRMED | H4-H27: 10 supported, 13 refuted, 1 dropped. |
| "six were registered after external reviews of the first and third versions" | UNCHECKED | The `origin` fields cite a jury review for five (H22, H23, H25, H26, H27); H24 cites the dropped H8. |

### Sentences that still say more than the data

- **S1, REFUTED as evidence:** "Nor is the size of the rise a rule: in the older runs, to τ = 4 … gain 0.07, and the network of width 5632 gains 0.29." It compares a gain at τ = 4 with a maximum rise to τ = 16. At τ = 4 the six laws of this job have gained 0.21 (G0), 0.146 (G2), 0.109 (W9), 0.105 (W11), 0.064 (G1) and 0.061 (G3): 0.07 lies inside the like-for-like range. W12 and width 2048 are still rising at τ = 4, 0.107 and 0.033 below the reference. Only 0.29 is outside. Replacement: "The older runs stop at τ = 4, where the six laws above have gained 0.06 to 0.21: there the model fine-tuned with the stationarity loss and the network of width 2048 have gained 0.07 and are still rising (0.11 and 0.03 below the reference), which does not contradict the range; the network of width 5632, which starts 34 % low, has gained 0.29, above it."
- **S2, imprecise** (five places; race report): "start at or below the reference energy". Seed-mean a(0) of G1 is −0.009, −0.014, +0.013 on main and +0.018, +0.005, +0.009 on repl.; G3 is +0.014 at η = 0.0331 on main and +0.010 on the mean on repl. Replacement: "that start on the reference energy (within 0.04) or below it".
- **S3, minor:** "At the two lower η they have opposite signs and cancel, almost exactly at η = 0.033". At η = 0.049 the sum is −0.074: 0.055 of 0.130 cancels. Replacement: "… and cancel, in part at η = 0.049 (−0.07 is left) and almost exactly at η = 0.033 (+0.02)".
- **S4, weaker than the data** (two places; race report "Conjectured"): "It is not the whole explanation" and "part of what keeps it from passing above". The per-η differences of the excursion are 0.039, 0.021 and 0.011 (repl. 0.043, 0.028, 0.006); the production gaps between G2 and W9 are 0.001, 0.084 and 0.115. The order is the reverse of what the mechanism predicts. At η = 0.0331, where the missing sink is largest, the difference is 1.5 SE with 3 of 5 seeds positive (repl. 2.0 SE, 3 of 5). Replacement: "The per-η differences do not support this: the difference decreases as the missing third-order part grows (0.039, 0.021, 0.011 for production gaps of 0.00, 0.08, 0.12) and is not significant at the smallest η (1.5 SE, 3 of 5 seeds)." In the conjecture list, replace "is part of what keeps it" with "may contribute to keeping it … (the per-η order is the opposite of what this predicts)".
- **S5, minor** (conclusion 6): replacement: "the lowest ratio at a held-out η, G1 at the smallest, is 1.8 (1.7 on the second realisation; 1.6 at the training η = 0.03)".
- **S6, jury minor point not applied:** `null_count_mean` at η = 0.0331 is 44.11 in `e4_main/e4_reference.json` (and in the report's data table) and 42.73 in `e4_nongauss/e4_reference.json`, on the same data. With 44.11 the "1.8" becomes 1.74. Add: "the reference count carries about 3 % of subsampling uncertainty (400 snapshots) that the seed SE does not include".
- **S7, REFUTED (inconsistency):** C7. The objectives table says 14; the abstract, the contributions ("thirteen registered constraint mechanisms") and the race report (13) do not. `REGISTRY` at 1312fb6 has 14 entries; the fourteenth is `gaussian_full_anchor`, tested but used only by H28, which has not run. Use one number everywhere: "fourteen, one of them (the anchor on the full-covariance Gaussian) tested but not yet used in a full run".
- **S8, minor:** "passes 2.4 % higher" against "about 2.5 %". The files give 0.0237 on main and 0.0256 on repl. Write "2.4 % (2.6 % on the second realisation)" everywhere.

Not changed and acceptable: "no model of this report has learned either". W9 starts 12 % off the reference, so it does not hold stationarity.

## 2. Digest

| Item | Verdict | Evidence |
|---|---|---|
| `results/digest.md` equals what `digest.py` prints | CONFIRMED | Empty `diff`, 2777 lines. |
| "Third-order part … at the eleven η" | CONFIRMED | Main +0.139 … −0.308; repl. +0.127 … −0.317; jackknife SE identical to the files. |
| "Third-order part of W9_skip_sym at the training η evaluated" | CONFIRMED | Values in the table of section 1. |
| "Null points of G1_gaussian_full over those of the reference" | CONFIRMED | Main 2.43, 2.12, 1.80 (held-out) and 2.45, 2.31, 1.60 (training). Repl. 2.28, 2.07, 1.69 and 2.38, 2.22, 1.60. |
| "H25, check at the validation η" | Differences CONFIRMED | Main −0.0037 and −0.0013; repl. −0.0121 and +0.0026. The SE ratios were not recomputed in this pass. |
| "Post hoc (not registered), per held-out η: excursion" | CONFIRMED | Main 0.0385 ± 0.0076, 0.0212 ± 0.0060, 0.0113 ± 0.0076, with P/D 0.790 / 0.789, 1.01 / 0.926, 1.13 / 1.02. Repl. 0.0433 ± 0.0051, 0.0277 ± 0.0029, 0.0057 ± 0.0029. |

Suggested addition to the per-η line: the number of positive seeds (5, 4, 3 on main; 5, 5, 3 on repl.).

## 3. `research/race-report.md`

"Must contain" list of the jury: CONFIRMED, every item is present. "Must drop" list: CONFIRMED except the first item below.

- **REFUTED** ("Conjectured"): "Why every law that starts at or below the reference energy gains magnetic energy at restart is not explained." Replacement: "Why the six laws tested that start on or below the reference energy gain magnetic energy at restart is not explained."
- **REFUTED (stale header):** "stopped because the goal of the pilot was reached, not on a budget". The goal in `race/PILOT-PROMPT.md` now ends on the budget, 17.08 of 140 USD is spent, and H28 is registered and being prepared. Replacement: "in progress; next step H28".
- Same as S4 (reversed per-η order), S2 ("at or below"), S7 (C7 says 13).
- Minor: "No law within 60 floors … (2.1 to 3.5 times)" are means over the held-out η; add "on the mean over η".
- Minor: "0.7 % off at τ = 16" is the signed mean curve (−0.007); the registered |a(16)| is 0.0102 (repl. 0.0133). Quote the registered one.
- Budget line: 18.4 h and 17.08 USD CONFIRMED from `research/compute-ledger.jsonl`. "30 jobs" UNCHECKED: the ledger has 44 rows, and 28 distinct pods with a cost.

## 4. H28

### Code of `FullGaussianAnchoredField`

- **Closed-form field: CONFIRMED.** Cov(x₁ − x₀, x_t) = tΣ − (1 − t)I and Var(x_t) = t²Σ + (1 − t)²I, so the gain is right. Row-vector use of Q is right. Mixed conditions are routed correctly. The interpolation is the same as `FullGaussian.sample`, including the edge cases at a training η.
- **Jitter: CONFIRMED necessary and harmless.** With the jitter, a Heun scheme of step h leaves a variance floor of (h/2)² per direction: 1e-4 at 50 steps and 1.7e-3 at 12, in per-mode-normalised units, which is negligible.
- **`__deepcopy__`: no error seen.** It shares the buffers, the factors and the cache; the moving average only updates `parameters()`; `state_dict` keys match; the cache holds 11 η against `max_cache` = 16. Fragile but not wrong: a later in-place change of a shared buffer would hit both copies.
- **Test:** CONFIRMED, 1 passed. The last tolerance (`atol=0.35` on the singular case) is loose.

### Integration of the anchored field

The role had flagged it; the diagnostic of the main session answers it and the role's own computation on the local data agrees:

| Training η | Top eigenvalue | Heun 50: top direction | Heun 50: trace | Heun 12: top direction |
|---|---|---|---|---|
| 0.08 | 31.5 | 0.997 | 0.9996 | 0.94 |
| 0.03 | 104 | 0.989 | 0.9985 | 0.79 |

The `--quick` gap between iteration 0 and G1 is this 12-step artefact, not a code error. At 50 steps iteration 0 should have about 1 % too little magnetic energy at low η: inside the registered tolerance, but not zero: report it.

### Group F against the protocol

| Item | Verdict | Evidence |
|---|---|---|
| Same network as W10 | CONFIRMED | `sym(net(pot_sym, 0.5))`. |
| Same optimiser and budget | CONFIRMED | `train()`: AdamW, one-cycle, 4000 iterations, batch 128, lr 5e-4. |
| Checkpoints of the moving average | CONFIRMED | Decay min(0.999, (1+it)/(10+it)): a window of about it/9, with no bias towards the initial weights. |
| Iteration 0 evaluated before training | CONFIRMED | Same `generate()` and same noise as every model. |
| G1 fitted with the sign symmetry | CONFIRMED | Same call as group G. |
| Training mechanics on a synthetic non-Gaussian case | UNCHECKED | |

Three remarks, none of them an error: `train_loss` draws its noise and times from the global RNG, so the loss at different checkpoints is measured on different draws: pass a fixed generator. The checkpoints at 250 to 2000 are states along one 4000-iteration one-cycle schedule, at high learning rate; they are not models "trained for k iterations". In the quick run, 150 iterations leave W14 at iteration 0 to three digits, while W10 moved to about 10 floors in 150 iterations: plausible, but check in the full-run log that the loss on the fixed sample actually falls.

### What to tighten before the full run (dated amendment)

1. **Add second-order clauses.** The statement says "without losing the second-order accuracy of G1", but the criterion tests only the energy distance, which is blind to the production (G0 is at 3.5 floors with none), and 1.5 × 2.55 = 3.8 floors is worse than G0. Add, at k* and at each held-out η, on seed means: |mean-flow part − reference| ≤ 0.05 (G1 is within 0.02; W9 is off by 0.13 to 0.15; W10 by 0.50 to 0.60); |E_B/E_B,ref − 1| ≤ 0.05 on the 512 samples (G1 ≤ 0.02; W9 0.10 to 0.15; W10 +0.12 to +0.29). Without these, a W9-like outcome would pass.
2. **Add an upper bound on the third-order part:** between 0.3 and 1.5 times the reference.
3. **Say what 0.3 means.** It is W10's own level (0.31 and 0.24 at 43.6 floors) and below W9 (0.60 and 0.44). Either raise it to 0.4, or state that "supported" means "at least what W10 has, at G1's distance" and report it next to W9.
4. **Remove the ambiguities.** Energy-distance ratio: the mean over the two validation η (selection) and over the three held-out η (test). "In more than one seed": paired, seed s at k* against seed s at iteration 0. Reference value of the third-order part: `prod_fluct_over_d` of the job's `e4_reference.json`. k* is chosen separately on each realisation. Denominator: iteration 0 (same noise, paired).
5. **Two realisations:** state the combined verdict: supported only if not refuted on both; otherwise "refuted on one realisation" or "refuted on both".
6. **Measurement check:** say "on seed means, iteration 0 against G1 of the same job"; add |E_B(it 0)/E_B(G1) − 1| ≤ 0.03; say what happens on failure (re-run with more Heun steps, which counts as one cycle of rule 5).
7. **Reported items:** add the sign and ratio of the third-order part at η = 0.0725 and at the training η = 0.08, where W9 fails.
8. **Wording:** replace "at the training length k*" with "at the checkpoint k* along one 4000-iteration schedule".
9. **Rule 8:** code the selection of k* and the verdict in `e4_digest.py` and commit it before the full run. Also check that `select()` cannot pick `W14_full_anchor_it0` as the generator of the objectives: it is G1, which the report excludes from the candidates.

## 5. Not checked

The rendered HTML and PDF, the explorer and the plots; the SE ratios of the validation-η digest lines; "30 jobs" in the race report and "six registered after reviews" in the report; the cost estimate of H28; convergence of the restart solver; a Monte Carlo null for the energy distance.

**Verdict on the whole:** the three commits apply the requested corrections faithfully, and the digest and every recomputed number are confirmed on both realisations. Before these are quoted, correct the sentences listed in sections 1 and 3, and amend the H28 criterion (points 1, 2, 4, 5 and 9 at least) before the full run.
