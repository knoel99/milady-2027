# Review of H28 (verdict), H33 and H32 (criteria) - encadrant role, 2026-11-13

Text returned by the `encadrant` role (read-only), saved by the main session. Everything was recomputed by the role from the JSON files; it
ran a CPU replica in the session's scratchpad, did not run `experiments/e4_mhd3d.py`, started no GPU job and did not regenerate the digest.

**Verdict in one line:** H28 is REFUTED by clause (a) on both realisations, the measurement check passes on both, and reading (iv) holds:
the network was trained and the evaluated moving-average copy is the trained one.

## Part 1: H28

### Pre-registration and trace

- **Amended criterion before the run: CONFIRMED.** The amendment is in commit 425210f (07:37Z). Both jobs started at 08:20Z on commit aeac08c (`research/compute-ledger.jsonl`, rc=0). `h28_lines` exists at aeac08c, and the diff aeac08c..60e8998 of `experiments/e4_digest.py` does not touch its selection or verdict lines.
- **Digest numbers: CONFIRMED, with one REFUTED item.** All H28 lines match the recomputation. The value "0.8945" is not in `digest.md`: the FM loss column prints 0.894 / 0.895 / 0.894. The report may not quote 0.8945 or "fifth digit" until the digest prints it. Smallest fix: in `h28_lines`, print the FM loss with 5 significant digits and add a column "FM loss − iteration 0" in scientific notation.

### (i) Measurement check (iteration 0 against G1, held-out η, seed means): CONFIRMED on both

| Check | Limit | Main (`e4_anchor`) | Second (`e4_anchor_indep`) |
|---|---|---|---|
| ED/floor difference | 0.5 | −0.1015 (2.4453 vs 2.5468) | −0.0026 (1.9745 vs 1.9770) |
| Largest \|third-order part\| | 0.02 | 3.87e-4 | 1.66e-3 |
| Largest mean-flow difference | 0.02 | 0.0100 (η = 0.0331) | 0.0042 |
| Largest \|E_B(it0)/E_B(G1) − 1\| | 0.03 | 0.0117 | 0.0045 |

Caveat to state with it: the ED check is on the mean over three η. Per η the main-run gap reaches −0.26 floor (η = 0.0490: 3.059 vs 3.324), with a seed sd of 0.22–0.37 per η. The check therefore resolves about one seed sd, not the integration error alone.

### (ii) Clauses

- **Clause (a): REFUTED on both realisations (CONFIRMED as stated).** Reference third-order part at η = 0.0403: −0.1991 (main), −0.2023 (second).

  | Third-order ratio to reference at η = 0.0403 | it250 | it500 | it1000 | it2000 | it4000 |
  |---|---|---|---|---|---|
  | Main | −2.88e-4 | −3.09e-4 | −3.18e-4 | −2.82e-4 | −2.58e-4 |
  | Second | +4.48e-3 | +4.49e-3 | +4.47e-3 | +4.50e-3 | +4.50e-3 |

  The largest single-seed |ratio| at any checkpoint is 0.021 (main) and 0.023 (second), against 0.3 required. The seed sd of the third-order part at iteration 0 is 0.0026–0.0030, against a threshold of 0.3 × 0.20 = 0.06. No seed is near it.
- **Clauses (b)–(e): NOT APPLICABLE**, since no k* exists; the report must not call them "passed". For information only, taking any checkpoint: (b) would fail (|ratio| ≤ 0.0013 on the main data and ≤ 0.0061 on the second at the two lower held-out η); (c) would hold (seed-mean ED per η changes by at most 0.2 % from iteration 0); (d) would hold (largest |mean-flow − ref| 0.0147 and 0.0025, limit 0.05); (e) would hold (largest |E_B/ref − 1| 0.0137 and 0.0212, limit 0.05).
- **Verdict:** main REFUTED (a); second REFUTED (a); combined "refuted on both".

### (iii) "The model does not move": CONFIRMED in substance, wording to correct

- Checkpoint differences from iteration 0, per seed (four keys checked: `ed_ratio`, `prod_fluct_over_d`, `prod_mean_over_d`, `E_B`, on validation and held-out η): ED ratio at most 0.017 on about 3 (0.5 %); third-order part at most 2.8e-5; mean-flow part at most 1.0e-3; E_B at most 6e-5 (4e-4 relative). "Every metric" is UNCHECKED beyond these four keys, apart from the digest table rows, which agree to 2–3 digits.
- "Equal to three digits" is slightly too strong for ED: the seed mean at validation η = 0.0596 is 3.2274 at iteration 0 and 3.2223 at iteration 250. Write "within 0.2 % on seed means".
- `fm_loss_train_sample` is 0.8945 only on the main run. On the second realisation it is 0.8916. The origin text of H33 says "0.8945 at every checkpoint, on both data realisations": correct it.
- Sign and size of the loss change: from iteration 0, +0.9e-5 to +2.8e-5 at iteration 250 (main) and +1.0e-5 to +1.4e-5 (second). At iteration 4000 the main run gives −4.0e-6 to +4.3e-6 over the seeds, mean +0.6e-6. The loss is not lowered; it is first raised slightly.
- "Running loss 0.90 against 0.8945" must not be read as an effect of the network: REFUTED as evidence. The running loss uses random samples, noise and times; the fixed sample uses 2048 draws with fixed seeds. The role's CPU replica shows the same offset while the raw network changes the fixed loss by under 1e-4.

### (iv) Did the network train, and is the evaluated copy the trained one: CONFIRMED

1. The checkpoints are not copies of the untrained model. At iteration 0, `fm_loss_train_sample` is identical in the five seeds, which ran as five processes (0.8944888 main, 0.8915678 second). At every later checkpoint it differs between seeds and between iterations by 1e-6 to 3e-5, well above float32 round-off on a mean of 2048 × 5320 entries. Generation metrics also differ in every seed.
2. Code path: no flaw found. `AdamW(field.parameters())` holds the parameters of `base`; `__deepcopy__` gives the copy its own `base` and shares only buffers, factors and cache; the moving average updates the copy in place; `keep[it]` is a deep copy of the copy's `state_dict` and is loaded into the returned object; the decay is 0.965 at iteration 250 and 0.9978 at 4000.
3. CPU replica of the null case (the repository's network, `SignSymmetrized`, `FullGaussianAnchoredField`, `fm_loss`, a verbatim copy of `train()`; synthetic, exactly Gaussian, sign-symmetric data, 2 × 2400 samples in dimension 5320): gradients are non-zero (norm 0.035 at iteration 1; `out.weight` receives gradient at iteration 1 and `inp.weight` from iteration 2); fixed-sample loss of the moving-average copy against iteration 0: +8.9e-6 and +1.1e-5 at it250 (two seeds), +6.6e-6 at it500; raw network +2.2e-5 to +8.0e-5. Same sign and size as the GPU runs: the GPU numbers are what a genuinely trained network gives when the residual holds nothing it can learn. Diagnostic, 2 seeds, not a result of the study: the gradient norm falls to 0.004–0.007 by iteration 250 and the network settles at a near-zero output.
4. Positive controls: the unit test `test_gaussian_full_anchor_learns_a_non_gaussian_law` passes (dimension 6, small MLP, plain Adam: not the E4 network or `train()`). In the role's replica, same code and dimension as E4, with one planted skewed direction, the moving-average copy at it250 lowers the fixed loss by 1.44e-4 (null: +1e-5). The planted set also differs from the anchor in second moments, so this shows that gradient reaches the network and that the evaluated copy is the trained one, not sensitivity to skewness alone.
5. A fact that bears on the reading: in the H25 runs, `times/W9_skip_sym/fm_loss_train_sample` is 1.176 ± 0.003 (main) and 1.172 ± 0.003 (second), against 0.8945 and 0.8916 for the exact Gaussian field. W9 produces its third-order part with a field far worse in flow-matching loss than G1's. This supports asking H33; it does not answer it.

Not done: training on the real E4 data. Better still, write the fixed loss of the raw network beside the moving-average copy, `out.weight` rms and the gradient norm as keys in `times/<variant>` in the next GPU job, so that the claim "trained" is in the digest.

### Sentences the report may write

- "H28 is refuted on both realisations of the data by clause (a): at no checkpoint (250 to 4000 iterations) does the model anchored on G1 hold 0.3 of the third-order part of the reference at the validation η = 0.0403 (seed means −3.2e-4 to −2.6e-4 of the reference on the main data, +4.5e-3 on the second realisation; largest single seed 0.023; measured, 5 seeds each)."
- "The measurement check passes on both realisations: integrated with 50 Heun steps, the untrained model reproduces G1 sampled exactly (ED within 0.10 floor on the mean of the held-out η, E_B within 1.2 %)."
- "Over 4000 iterations (batch 128, lr 5e-4, ResMLP 512 × 4, 14 400 snapshots in dimension 5320) the network added to the exact Gaussian field of G1 does not lower the flow-matching loss on a fixed training sample (change between −4e-6 and +3e-5 around 0.8945 and 0.8916), and the generated law stays that of G1 within 0.2 % on the energy-distance ratio." This needs the digest to print the loss to 5 digits.
- "A network given the exact Gaussian part learns nothing more in this budget" is SUPPORTED if "in this budget, with this optimiser and schedule" stays in the sentence and it is labelled measured (5 seeds × 2 realisations).
- "The training did run: the checkpoints differ from the untrained model and between seeds, and the same code learns a planted non-Gaussian component (unit test; CPU diagnostic in dimension 5320)." Label the CPU part as a diagnostic.

### What must NOT be concluded

- That the data hold no learnable non-Gaussian structure, or that the Gaussian field is the flow-matching optimum. The anchor is fitted on the same 2400 snapshots per η (rank-deficient covariance, in-sample).
- Anything about a larger or different network, more data, a larger batch, more iterations, another optimiser or learning rate, a non-zero initialisation, or another loss weighting in t. None was run. Low gradient signal-to-noise at batch 128 with a zero-initialised output is a plausible cause, but it is CONJECTURED.
- That clauses (c), (d), (e) "pass". They are not applicable without k*.
- That the comparison of 0.90 (running) with 0.8945 (fixed) shows anything.
- That W9's third-order part is spurious. That is H33, not yet run.
- Words to avoid: "confirms", "proves", "cannot learn".

## Part 2

### H33: decidable in size, but two loopholes and one check missing from the code

Size of the effect: CONFIRMED decidable. W9 third-order part per seed in the H25 runs: −0.0817 ± 0.0023 (sd) and −0.1180 ± 0.0029 on the main data, −0.0848 ± 0.0026 and −0.1126 ± 0.0053 on the second, with a G1 seed sd of 0.002–0.003: the threshold 0.3 × 0.082 = 0.025 is about 10 seed sd. Group Z code: CONFIRMED (surrogate drawn at the normalised training conditions, as many draws as snapshots, from G1 fitted with the sign symmetry; `seed_all(seed)` before each training).

- **Loophole 1: the ratio is signed. REFUTED.** A surrogate-trained model with a large third-order part of the opposite sign gives a negative ratio and "NOT REFUTED". Replace in the criterion: "…is 0.3 or more in absolute value on the seed means, or is 0.3 or more in absolute value in more than one of the 5 seeds (same seed, paired); or if the third-order part of the model trained on the data does not have the sign of the reference in at least 4 of the 5 seeds at these two η (the ratio is then undefined: measurement invalid)."
- **Loophole 2: a registered check is not implemented. REFUTED.** The check "the model trained on the data reproduces the values of H25 within 0.02" is not in `h33_lines`. Add it, and make the verdict line print "MEASUREMENT INVALID" when a check fails.
- **Surrogate set: right for the question, with two limits to write down.** Independence: 2400 independent draws carry more information on the covariance than 2400 snapshots from 24 trajectories. If W9's third-order part comes from fitting a covariance known from few effective samples, the independent surrogate will not reproduce it and H33 would be "supported" wrongly. Add to the combined-verdict text: "'supported' means: not produced by this model from independent Gaussian data with these two moments; it does not exclude an effect of the finite number of trajectories." A third arm closes this (a surrogate of 24 × 100 draws built as Gaussian time series with the measured autocorrelation per trajectory); it is optional and must be registered before it is run. The surrogate set itself is not checked: add "the third-order part computed on the surrogate training set itself is below 0.02 in absolute value at each training η" (one call of the production split on the surrogate set, written to `times/W9Z_skip_sym_gaussdata`).
- **Further tightening.** State in the protocol that the surrogate is redrawn per seed, so the seed spread of W9Z includes the draw of the set. Report `fm_loss_train_sample` of both models with the fixed seeds of group F, next to the loss of the Gaussian field. Report the ED of W9Z against G1 draws. Correct the origin text: "0.8945 (main data) and 0.8916 (second realisation)".

### H32: decidable, but weakly falsifiable as written

Code: CONFIRMED by reading (`null_density_factors` and `h32_lines`); the test was not run by the role.

- **Weakness 1: the outcome is nearly fixed by what was known at registration. REFUTED as a discriminating criterion.** The count ratio is 2.1 and the CPU diagnostic gave share-of-weak-field ratios of 0.24, 0.82 and 1.07 at the three training η examined: if the Kac-Rice product holds within 20 %, the Jacobian ratio is at least about 1.6. Only a failed measurement check can then refute. The words "where it is weak" in the statement are not tested at all. Add one clause that can fail: "and the ratio G1 over reference of the unconditional mean of |det ∇B| (all cells, same units) is below 1.25 at each held-out η: the excess of G1 is specific to the places where B is weak. If it is 1.25 or more, the statement is amended to 'varies faster everywhere'." This needs one more key, `kr_jacobian_all`.
- **Weakness 2: no uncertainty on the reference factors. REFUTED.** They come from 400 snapshots of a few trajectories. Add: "The factors of the reference carry a jackknife standard error over trajectories; refuted if the ratio is below 1.5 (or the density ratio above 1.25); supported only if the ratio minus two standard errors is at least 1.5 (plus two at most 1.25); otherwise inconclusive, which counts as one cycle of rule 5."
- Smaller points: each ensemble is scaled by its own rms; state that G1's E_B is within about 1–2 % of the reference, so the rms³ effect is at most 3–4 %. Status wording: "decomposition measured", not "explains".

## Checks not run

Training on the real E4 data, raw-network loss and weight norms on the GPU checkpoints (not saved); "every metric" of (iii) beyond the four keys and the digest table; regeneration of the digest; `null_density_factors` and its test. The repository was not modified by the role.

**Verdict on the claim as a whole:** readings (i), (ii) and (iv) are CONFIRMED and (iii) is confirmed with corrected wording (0.8916 on the second realisation, "within 0.2 %", no reading of the running loss), so H28 is REFUTED by clause (a) on both realisations; the report may say the anchored network learns nothing more in this budget, and nothing beyond this budget and optimiser.
