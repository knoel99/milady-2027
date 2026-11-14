# encadrant, 2026-11-12 23:05 UTC — verdicts on H4–H10 and H12–H14 (registered protocol of E4)

Scope: the ten hypotheses registered in commit 68e2fd4, on the 5 seeds of the GPU run `experiments/results/replications/e4_gpu` (data regenerated on the pod) and, for the sign, on the two CPU seeds of the session container. The role recomputed every figure from the JSON files with its own script, checked that the registered criteria did not change (`git diff 68e2fd4 HEAD -- research/hypotheses.json`), and edited nothing. Condensed by the main session from the role's answer.

| Hypothesis | Verdict | Recomputed (GPU, 5 seeds; mean ± SE of the paired differences over the 3 held-out η) | CPU, 2 seeds |
|---|---|---|---|
| H4 potentials better than free components | REFUTED | W0 − W4 = −20.05 ± 3.21 (−6.2 SE), 0 of 5, negative at each η | −26.9, 0 of 2 |
| H5 the divergence penalty does not enforce the constraint | CONFIRMED | div B 0.2064 against 0.3797 (ratio 0.544); W0 − W1 = −228.2 ± 12.7, 0 of 5 | ratio 0.515, −265 |
| H6 projected flow better than final projection | REFUTED | W2 − W3 = 2.69 ± 3.72 (0.72 SE), 4 of 5: fails on the 2 SE clause | 6.0 ± 7.5, 1 of 2 |
| H7 stationarity loss lowers the energy residual | CONFIRMED | 0.0988 ± 0.0108 (9.1 SE), 5 of 5 (0.290 → 0.191); ED ratio W5/control 1.023 | 0.097, ratio 1.047 |
| H8 training-time identities better than tilting | NOT DISCRIMINATING | criterion formally met (30.0 ± 10.1, 5 of 5), but ESS/N = 1/256 in 14 of 15 cells: the tilted "law" is one sample, the measurement is invalid; with the bias estimate the sign flips (−13.9 ± 9.5) | 5.0 ± 2.3 |
| H9 equivariance lowers the polarity asymmetry | REFUTED (first clause) | W4 − W4s = 0.0004 ± 0.0058, 3 of 5, both at the binomial floor 0.0176; ED clause holds: W4s/W4 = 0.819 (−46.5 ± 4.8) | +0.0065, inside the floor; 0.796 |
| H10 flow matching better than diffusion | CONFIRMED as registered | W6 − W4 = 262.4 ± 12.1, 5 of 5; but at the training η W6 is better than W4 (−15.06 ± 0.90, 0 of 5): the result is about interpolation in η, not about the family at fixed η | 272.5; −15.3 at training η |
| H12 the helicity identity has more leverage | REFUTED | r_b/r_a = 0.504, r_b > r_a in 0 of 5; the tilting clause is met (0.238 ± 0.095, 5 of 5) against a degenerate comparator (tilt on the energy identity: ESS/N 0.0096) | 0.499; tilting sign not reproduced |
| H13 nulls ∝ k_λ³ (slope in [2, 4]) | REFUTED on the slope | slope 4.875, R² 0.902, 135 points, bootstrap [4.83, 4.92]; intercept 1.08: about 2.9 times too many nulls at the right k_λ | 4.96, R² 0.90 |
| H14 the divergence of the free model is not an integration error | CONFIRMED | 0.3792 at 50 steps, 0.3788 at 200; ratio 0.998–1.000 per seed | 0.3821, 0.3820 |

Attempts to break the comparisons: pairing and `per_seed` correct; rows at n = 256 must never be compared with rows at n = 512 (the H8 code respects it); variants of one latent space share their noise per (seed, η); the SE covers model and sampling variability, not the data realization or the floor (sd of the floor over splits about half its mean); in the GPU data the small floor is at η = 0.049, which dominates the test mean; H4 and H10 hold at each η, H6 at none.

Overall claim: "every trained generator is far from the reference law" CONFIRMED (176.6–518.7 at held-out η, 105.8–274.5 at training η). π/2 CONFIRMED as the mean over t of Var(x₁ − x₀ | x_t) for unit Gaussians. "The cause is the width below the latent dimension": REFUTED as a stated cause, it is a conjecture (a rank-512 linear field on 5320 independent coordinates would give a loss of 1.96, not 1.60–1.63; the loss cannot separate width from budget or from the absence of an input skip). What would refute it: width 512 trained 10 times longer going below π/2; width ≥ 5320 at the same budget staying above π/2; no monotone trend in a width scan; the gain of the affine term disappearing at 5 seeds.

Housekeeping noted: `e4_digest.load()` rewrites the merged JSON files; the GPU `e4_data.json` records `device: cpu` (the data were generated on the pod's CPU cores).
