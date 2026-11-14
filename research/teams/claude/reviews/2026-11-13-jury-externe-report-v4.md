# Pre-defence report: report v4, team claude (jury-externe, 2026-11-13)

Text returned by the `jury-externe` role (read-only), saved by the main session. The role reached its turn limit before handing back and
was asked to deliver its report from the checks already made, with no new investigation.

**Verdict: not yet fit to defend; three groups of sentences still go beyond the evidence.** Every number of the new section that the role
recomputed matches the result files on both data realisations, and the digest regenerates from the JSON files with no differing line. T1
kept as registered and the status of H27 are handled correctly.

**Which version this covers.** The report was read in full at 056e34f. The branch moved to c8178e8 during the review (report corrected in
3abe952). The changes were checked by word-diff and one grep; quotes below are the wording at that HEAD, except lines 113, 496, 722, 776 and
840, reconstructed from the diff. The `encadrant` review of the same commit was not read.

## 1. Verdict per claim

| # | Claim | Where | Verdict | Evidence (keys in `e4_mhd3d_s<k>_<group>.json`, `e4_reference.json`) |
|---|---|---|---|---|
| 1 | Reference third-order production from +0.14 to −0.31; W9 holds 0.6 and 0.4 of it, opposite sign at the third η | abstract, sec-nongauss, conclusion 5 | holds | `prod_fluct_over_d_jack`: +0.139 ± 0.014 (η = 0.08) to −0.308 ± 0.003 (η = 0.03), zero at 0.0658; second realisation +0.127 to −0.317. W9 `prod_fluct_over_d`: −0.0055, −0.0817, −0.1180, 5 of 5 seeds; ratios −0.10, 0.60, 0.44 (second: −0.19, 0.63, 0.41) |
| 2 | W9 and W11 "are the only laws of the study with a third-order part" | line 776 | wrong | W10 in tbl-split: −0.012, −0.043, −0.064, 5 of 5 seeds (0.31 and 0.24 of the reference); no other variant was measured |
| 3 | Balance of W9 is two errors that partly cancel | line 492 | holds at the two lower η; overstated wherever the balance is called good or better | Error on the mean-flow part −0.151, −0.130, −0.133; on the third-order part −0.060, +0.055, +0.152; sum −0.211, −0.074, +0.019. `balance_residual_magnetic`: W9 0.118, 0.039, 0.009; G1 0.038, 0.055, 0.123 |
| 4 | G1 has 2.1 times the reference null points; the low count is non-Gaussian | line 504, discussion, conclusion 6 | holds | `null_count` over reference: training η 2.45, 2.31, 1.60; held-out 2.43, 2.12, 1.80 (second: 2.38, 2.22, 1.60; 2.28, 2.07, 1.69). G3 − G1: +0.024 ± 0.011 and −0.002 ± 0.010 |
| 5 | G1 leaves the stationary energy; stationarity is non-Gaussian | same | holds as now hedged; the role's control says the hedge can be lifted | Files: no `restart_anchor` in the `train` rows. Control: section 3 |
| 6 | "no model of this report has learned either" | line 504 | overstated for stationarity | Post hoc, G2 passes 0.024 higher than W9 |
| 7 | The drift of the objectives does not rank; T1 = 0.124, not met, with a caveat | sec-metrics, objectives, conclusion | holds | (1 + a(4))/(1 + a(0)) − 1 = 0.9857/0.8772 − 1 = 0.124; a perfect return gives 0.140; G1 scores 0.064 while moving 10 % away |
| 8 | "every law that starts at or below the reference gains 10 to 21 %" | abstract, lines 496, 776, 889, Limits | overstated | True of the six such laws of this job (rise 0.104 to 0.208). Digest, older runs to τ = 4: W12 −0.173 to −0.107, width 2048 −0.098 to −0.033, width 5632 −0.344 to −0.058 |
| 9 | H26 confirmed on its registered criterion | line 494 | holds | Overshoot W9 0.0045 / 0.0048, \|a(16)\| 0.0102 / 0.0133, G1 0.0914 / 0.1029, G0 0.1732 / 0.1986 |
| 10 | H27: invalid on the first realisation, refuted on the second; excursion a conjecture | lines 498–500 | holds | Paired −0.0051 ± 0.0005 and −0.0056 ± 0.0005; null control −0.0236 ± 0.0131 and −0.0004 ± 0.0036; excursion +0.0237 ± 0.0036 and +0.0256 ± 0.0030, 5 of 5 |
| 11 | The excursion "is what its missing third-order sink of production would give" | lines 500, 891 | not supported at one η of three | η = 0.0725: `prod_over_d` 0.790 (G2) and 0.789 (W9), yet the difference is largest: +0.039 ± 0.008 (second: +0.043 ± 0.005), against +0.021 and +0.011 |
| 12 | G2 "does not overshoot the reference energy at restart more than it does" | line 857 | wrong as worded | Same numbers as claim 10 |
| 13 | What Gaussianising W9 changes on the other metrics | line 502 | holds | `std_residual_rel` 1.632 and 2.449; null error +0.043 ± 0.028 and +0.044 ± 0.018; 0.428 and 0.433 floors apart; drift at τ = 4 +0.045 ± 0.007 and +0.046 ± 0.006 |
| 14 | Conjecture: covariance of G1 plus the reference's third-order production gives the right topology | line 891 | not supported; the report's own number goes against it | W9's third-order part changes its null count by 0.04 out of 1.7 |
| 15 | Counts | introduction, abstract, negative results | holds | 27 registered; H4–H27 = 24; 10 supported, 13 refuted, 1 dropped |
| 16 | "The next steps follow from these results" | line 893 | overstated for two items | W10 at 43.6 floors (H19); W11 not below G0 (H20) |

## 2. The three required changes

**A. The magnetic balance of W9 is not an advantage.** The section shows a compensation of errors, but four other places still credit it.

- Line 492, replace the sentence beginning "The good magnetic energy balance of W9" with: "The magnetic energy balance of W9 (production over dissipation 0.79, 0.93 and 1.02) is the sum of two errors: a mean-flow part too small by 0.15, 0.13 and 0.13 of the dissipation, and a third-order part off by −0.06, +0.06 and +0.15. At the two lower η they have opposite signs and cancel, almost exactly at η = 0.033; at the largest they add, and W9 under-produces by 21 %. Its lower residual on the mean (0.055 against 0.072 for G1) comes from this cancellation."
- Line 886, replace "The learned models with the affine term have the better magnetic energy balance on the mean over the held-out values." with: "The learned models with the affine term have a lower residual of the magnetic energy balance on the mean (0.055 against 0.072), through two errors that cancel at the two lower values and add at the largest (item 5)."
- Line 776: add the same qualifier, and replace "are the only laws of the study with a third-order part of the magnetic production" with: "are, among the laws close to the reference, those with a third-order part of the magnetic production (W10 has one of 0.3 and 0.2 times the reference's at the two lower η; the other variants were not measured)".
- Line 840, replace the list with: "the split of the magnetic production into a mean-flow part and a third-order part (the residual alone hid two errors of W9 that cancel), the null count, and the restart curve anchored on the reference".

**B. The restart statements still generalise from six laws and offer a cause the data contradict.**

- Line 496 and its copies: replace "every law that starts at or below the reference energy" with "the six laws of this job that start at or below the reference energy (G0, G1, G2, G3, W9, W11)". Add: "This is not a rule: in the older runs, to τ = 4 and with an approximate initial energy, W12 and the network of width 2048 gain 0.07 and the network of width 5632 gains 0.29."
- Same line: replace "so a rise of the same size takes it away" with: "and a rise of 0.11 takes it away. That the two rises have one cause is not established: W9 may simply relax to the stationary energy, as W10 does from above."
- Line 857, replace the H27 clause with: "and, on the measure registered for the test (the largest deviation from the reference energy beyond the initial one), the Gaussian law with its first two moments does not move farther than the model does (H27 predicted that it would; refuted on one realisation, the null control failing on the other). That measure cannot see a passage above the reference smaller than the 12 % initial deficit; computed after the fact, the Gaussian law passes 2.4 % higher."
- Line 500, replace "which is what its missing third-order sink of production would give" with: "A missing third-order sink would give this at the two lower η (production over dissipation 1.01 and 1.13 for G2, 0.93 and 1.02 for W9). It is not the whole explanation: the difference is largest at η = 0.0725 (0.039 ± 0.008), where both have a production of 0.79." Add the same caveat at line 891.
- Line 722: replace "Lower is better in every column." with "Lower is better in every column except the two restart drifts, which do not rank the laws (@sec-nongauss)."
- Line 587: replace "and on the restart drift of the magnetic energy at τ = 4 (0.072 against 0.124; …)" with "; its restart drift at τ = 4 is lower (0.072 against 0.124), which is not an improvement: …".

**C. Conjectures and next steps.**

- Line 891: drop "the right topology and". The null count depends on the law of B alone, and under B → −B its odd moments vanish, so the third-order production is a different object. Replacement: "…would be closer to stationary under the solver; which statistic of the magnetic field sets its number of null points is not known."
- Line 893: replace "and as the anchor of the flow-matching field … to learn" with: "Whether it can also anchor the flow-matching field is a hypothesis to register: the two anchored models of this report did not stay as close as the law they were anchored on (H19, H20), and a full sample covariance cannot be estimated at 64³."
- Line 893: replace "the magnetic energy balance, the production split and the anchored restart curve" with: "the two parts of the production split, each against the reference, and the largest deviation from the reference energy over the anchored curve, initial deviation included".
- Line 893, add: "Register the passage of the Gaussianised model above the reference as a hypothesis, signed, per η, with all 512 samples restarted; restart the learned model with its magnetic energy rescaled to the reference."

## 3. Claim (iii): the control that was missing, and what the role ran

**Null count.** The inference is valid. At a training η, G1 has exactly the sample moments. For a Gaussian field the expected number of zeros depends on the covariance only through the local covariance of (B, ∇B), which is well estimated, so the rank deficiency is harmless. G3 confirms it.

**Restart.** The files test G1 only at held-out η, with an interpolated covariance. The role ran the missing control on CPU on the local data (`experiments/data_e4`, a third realisation; τ ≤ 4, three draws of 96 samples):

| η (training) | Rise of E_B, exact sample moments | Rise, covariance from 12 of 24 trajectories |
|---|---|---|
| 0.08 | 0.105 (0.102 to 0.110) | 0.115 |
| 0.054 | 0.107 (0.097 to 0.119) | 0.107 |
| 0.03 | 0.091 (0.086 to 0.096) | 0.089 |

Reference snapshots move by 0.0002 over τ = 1. The interpolated G1 in the files rises by 0.123, 0.105 and 0.096. Neither the interpolation nor the sample size of the covariance explains the excursion. **These numbers are not quotable: the team must re-run them in its protocol.** Then replace the end of line 504 with: "…and so is its stationarity under the solver: the Gaussian law with the sample moments of a training η, without interpolation, leaves the stationary energy by the same amount; no model of this report reproduces either."

## 4. Minor points

- Abstract: "after a second review" should read "after the review of the third version".
- Line 882: "with five seeds, on parameter values that were not used for training" is untrue of item 5 (reference property, jackknife, end values are training η). Write "five seeds for the models, a jackknife over the 24 trajectories for the reference; held-out values unless said otherwise".
- Line 690: "in the other direction" should read "away from the reference instead of towards it".
- "move 9 and 17 % away" are overshoots; the largest deviations are 10 and 20 %. "Before returning": on the second realisation G1 is still 3.1 % above at τ = 16 (7.6 % at η = 0.0725).
- Line 889, "at least twice": true on the mean; G1 is at 1.8 at η = 0.0331.
- H22: its statement says "and not from its Gaussianity", while G1 keeps half of the excess null points and an overshoot of 0.09. One sentence in sec-g1 should say the statement goes beyond its criterion.
- Worth adding: at the training η the third-order part of W9 is +0.008, −0.069 and −0.121 (0.06, 0.73 and 0.39 of the reference). The failure at the largest η is therefore not an interpolation error.
- The reference null count at η = 0.0331 is 44.11 in the main reference file and 42.73 in this job, on identical data (another subset of 400 snapshots). Null-count errors carry about 2.5 % of common uncertainty not in the seed SE.
- The role's own check, one realisation: at η = 0.08, 44 % of the reference third-order part comes from differences between the time-mean flows of the trajectories; at η = 0.0331, 10 %.

## 5. What research/race-report.md must contain or drop

Must contain:

- T1 = 0.124, not met, as registered; the drift does not rank.
- H25 refuted, per-η numbers, opposite sign at the largest η, mean-flow part 10 to 16 % low, and the cancellation (adding at the largest η).
- H26 "confirmed on its registered criterion", with the caveat that it does not show W9 closer to the attractor.
- H27 invalid on the first realisation, refuted on the second; drift at τ = 4 of 0.170 against 0.124; excursion as a conjecture.
- G1: 2.1 times the null points on the mean (2.5 to 1.6); restart measured at held-out η only.
- Counts 10 / 13 / 1, and which verdicts rest on one realisation.

Must drop or change:

- "W9 has the better magnetic balance" as an advantage.
- "every law that starts at or below…": scope to the six laws.
- The topology conjecture.
- The third-order mechanism without the η = 0.0725 caveat.
- "the null control of H27 lacked samples": write "attributed to".
- "anchor the flow on G1" as a remedy for C1.
- Any plain-language "G2 does not overshoot more than W9".

## 6. Three next experiments, ranked

1. **Recolour the W9 samples mode by mode to the data-fitted second moments at sampling time, then restart all 512.** C3, C4 and the deficit behind T1 are second-order errors: the Gaussianised W9 has the same energy residual (0.057) and spectrum error (0.148), while G0 is at 0.0015 and 0.024. This can meet C3 and C4, and it is the equal-energy restart that settles the reading of H26.
2. **G1 restart at the training η, and with half the trajectories, in the team's protocol, plus the signed excursion of G2 against W9 per η.** It lifts the hedge on claim (iii), gives H27 a valid null control, and tests the mechanism at η = 0.0725.
3. **For C5, split the factor 2.1 between the reference and G1 into the density of B at zero and the mean |det ∇B| there, then test a surrogate that keeps the data's k = 1 amplitudes and Gaussianises the rest.** No result so far suggests any variant can reach 0.2 (G1 is at 1.10). This tells whether C5 is a target a model can be given or must be reported as out of reach. The k = 1 idea is the role's guess.

## 7. Not checked

- `research/reviews/2026-11-13-encadrant-report-v4-numbers.md`.
- The rendered HTML and PDF at HEAD, the explorer, the schematic figures.
- The changes to `research/hypotheses.json` in 3abe952.
- Convergence of the restart solver in time step and resolution.
- A Monte Carlo null for the energy distance.
- Check 2 of H25 at the three unevaluated training η.
- The GPU logs; the "few milliseconds per step" claim; the novelty claims.

No tracked file was changed by the role (git status clean at 06:59 UTC). Its scripts and logs are in the session's scratchpad, not in the repository.
