# Review by the `jury-externe` role: the report with H28 to H34 (draft of version 5)

Date: 2026-11-13, 15:52–16:13 UTC, commit 62d14b9. Milestone review due at 25 % of the GPU budget and for the changed report: the new section {#sec-origin}, the updated abstract, contributions, discussion, negative results and limits. The conclusion and the objectives text were not yet updated and were left out of the scope. The role edits nothing; its report is copied below, and the follow-up of the main session is at the end.

Numbers are recomputed from the raw JSON under `experiments/results/replications/` with the role's own scripts, not `e4_digest.py`; brackets give the second data realisation. Unit tests of the three new tools pass. No GPU run. S1 to S7 are the sentence changes below.

## Verdicts

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | H28 "learns nothing more", and its scope | HOLDS | Third-order part at the validation η: −3×10⁻⁴ (+4.5×10⁻³) of the reference at every checkpoint, per-seed values equal to iteration 0 to four decimals; energy distance (ED) within 0.06 %; loss 0.89449 → 0.89451. |
| 2a | H33/H34: no third-order production from Gaussian data; ED across the three training sets | HOLDS | At most 0.004 of the dissipation in any seed. ED values and 27 of 30 pairs reproduced. |
| 2b | "no such deficit of second moments"; abstract "no deficit of magnetic energy" | WRONG; OVERSTATED | Trained on independent Gaussian draws, the model is 0.104, 0.081, 0.058 below the reference in mean-flow production (0.078, 0.073, 0.070): 43 to 69 % of the deficit of the data-trained model; G1 is within 0.02. On Gaussian trajectories at η = 0.0331: 89 to 97 %. Magnetic energy on trajectories: +8 to +15 % at five of the eight η evaluated; "in either direction" rests on one value (−5 %). (S1, S2) |
| 3a | W16 values and the three restrictions | HOLDS, one restriction OVERSTATED | ED 2.07 against 2.55, paired −0.48 ± 0.04 (−0.37 ± 0.04), +0.20 (+0.13) at η = 0.0725; third-order 0.74, 0.58 (0.79, 0.59); balance 0.034 against 0.072. Target moments use the training η only: no leak. But G0 → G1 gains 0.97 floors, so the inter-mode covariance does count in the ED. |
| 3b | Objectives paragraph | HOLDS, incomplete | C3 and C4 are functions of the mean and covariance alone, T2 of the symmetry: G1 (0.0034, 0.063), G4 and G0 meet them. Only T1 depends on W9. (S3) |
| 3c | "the only laws of the committed runs…" | WRONG by the letter | In `e4_relax` (committed), G1 relaxed 4 time units has 4.55, 0.007, 0.10, 0.041; relaxed W16 1.58, 0.002, 0.046, 0.019. Without the solver it holds, but G1 fails on T1 alone (0.065 against 0.05). (S4) |
| 4 | H30 "halves the passage" | HOLDS; Discussion NOT SUPPORTED | 0.095 against 0.046, paired 0.049 ± 0.005 (0.051 ± 0.003). At η = 0.0725 the two laws have the same magnetic balance and initial slope and still differ by 0.055: the section rightly excludes the third-order part. The Discussion ties the effect to that part and to learning from the data; neither is tested. A lead: the sample spread of the dissipation (1.4 to 1.75 times the reference's for G1, 1.0 to 1.5 for W16). (S5) |
| 5 | H31 and its limit | HOLDS | 0.132, 0.084, 0.088 (0.124, 0.101, 0.090); lowest seed 0.062. |
| 6 | H32 descriptive statement; "smoothness" | Numbers HOLD; wording WRONG | Ratios 1.61, 1.49, 1.39 (1.55, 1.46, 1.36). But G1 has the rms gradient of the reference by construction (Taylor-wavenumber ratio 1.007, 1.006, 0.997): it does not "vary faster". The 35 % (53 %) is the change of the Jacobian factor, not of the density (24 %, 34 %). (S6) |
| 7 | Abstract; "thirty-one" | Count HOLDS | H4 to H34: 14 supported, 15 refuted, 2 dropped. Other new sentences: rows 2b, 3b, 6. |

## Method (claim 8)

The amendments of H28 to H33 precede their launches in the compute ledger: compatible with a registered protocol.

**H35: defensible in form, not neutral in effect.** The repair adopts the reference null count of the H29 job, 4 % and 10 % higher (28.7 against 27.6; 47.1 against 42.7). Recomputed on `e4_relax`: the tightest ratio of clause (a) moves from 0.589 to 0.529 (limit 0.6) and the relaxation time of W16 from 4 to 2. Check (3) becomes vacuous, and the outcome on the first realisation is known before the run. Also, G1 relaxed 4 time units meets all five thresholds of clause (b) (null-count error 0.13), so (b) is a statement about the solver. To be quotable: reference null count on all 2400 snapshots; relaxed G1 beside relaxed W16; margins of (a) and (c) stated; only the second realisation counted as a test.

**H36: acceptable.** The failed check was tighter than its noise (5 % limit, 4 % standard error); new data, thresholds unchanged. To be quotable: verdict on the second cycle alone; independent states measured. With 17 to 75 time units of decorrelation, 96 × 50 against 24 × 200 time units multiplies them by 1 to 3, not 4.

Neither mid-run amendment has been read by the `encadrant` (`review_due.py`: due).

## Sentences to change

- S1. "…no such deficit of second moments." → "…no such deficit of magnetic energy (at most 5.3 %), but still 0.06 to 0.10 of the dissipation missing in mean-flow production, about half of what the data-trained model misses."
- S2. Abstract: "…and no deficit of magnetic energy." → "…; its magnetic energy is within 5 % on independent draws and 8 to 15 % too high at most η on correlated ones."
- S3. Abstract: "brings the energy distance, the energy balance, the spectrum and the restart drift within the thresholds" → "takes the energy balance and spectrum of the Gaussian law (within thresholds by construction), lowers the energy distance from 9.3 to 2.1 floors (G1: 2.5) and the restart drift to 0.021 (G1: 0.065; threshold 0.05)".
- S4. "are the only laws of the committed runs that are within the thresholds…" → "are the only laws sampled without the solver whose restart drift is also below its threshold; G1 meets the other three".
- S5. "Where this part is learned, it matters under the solver…" → "At equal moments, what W9 holds beyond its second moments halves the passage (H30); this is not the third-order production, and it is not shown to be learned from the data."
- S6. "varies faster everywhere", "smoother", "The smoothness…" → "at equal spectrum, the Gaussian field has 1.4 to 1.6 times the mean |det ∇B| of the reference: the reference's gradient tensor is closer to singular".
- S7. Limits: "about 3 %" → "4 to 10 % (two draws of 400 snapshots)".

## What a jury asks first (claim 9)

1. Recolour the model trained on Gaussian surrogates through the same map, with W16 and G4, 512 restarts: is the gain in ED, T1 and excursion learned from the data? About 1 GPU-h per realisation.
2. Oracle: held-out reference snapshots recoloured onto the moments of G1: the ceiling of the construction. About 0.6 GPU-h per realisation.
3. Reference null count on all 2400 snapshots, every C5 recomputed from stored counts. About 0.6 GPU-h per realisation, or CPU.
4. Positive control of H28 at full size: the anchored model trained on 14 400 samples of W9, whose third-order part is known. About 1 GPU-h.
5. Statements, no run: what W16 copies (5320 + 1.4×10⁷ numbers per training η) against what it learns; cost of the full map at larger size.

The four runs on both realisations: about 6 GPU-h, 5 to 6 USD.

## Pre-defence report

Strengths. Every recomputed value matches; refutations and restrictions are reported with the results.

Weaknesses. The narrative credits the recolouring with what the copied moments do. One sentence contradicts the committed files (2b), one a committed run (3c), one the physics (6).

Required before defence. (i) S1 to S7. (ii) Controls 1 and 3. (iii) An `encadrant` reading of the mid-run amendments, and H35 re-read under a full reference count.

Unverified. The `encadrant`'s replica and its factor 1.7; anything needing the snapshots; the figures; the second cycles. The ED unit depends on the number of trajectories (floor 0.070 → 0.043 at η = 0.0725 with 96).

## Follow-up of the main session

- S1 to S7 applied to the report in the commit that adds this file.
- Control 3 (reference null count on all the snapshots): script `experiments/e4_refnulls.py`, run on the data of the main run (CPU of the session) and on the second realisation (a pod); the null-count errors of H35 are reported against both counts.
- Control 1 (recolouring of the model trained on Gaussian surrogates) and control 2 (the oracle) are registered as a hypothesis before any run (H37).
- H35: the verdict is read as the jury asks: the second realisation is the test; the first realisation, whose outcome under the repaired measurement was computable before its second cycle, is reported as such; G1 relaxed is given beside W16 relaxed, with the margins of clauses (a) and (c). The `encadrant` reads the two mid-run amendments with the verdicts.
- Control 4 and the count of independent states of H36 are written in the remaining work unless the budget allows them after H37.
