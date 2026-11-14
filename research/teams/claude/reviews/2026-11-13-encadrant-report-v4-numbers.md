# Encadrant review of commit 056e34f (E4, team claude): digest additions, H25-H27 verdicts, report section sec-nongauss, two plots

Text returned by the `encadrant` role (read-only), saved by the main session. Everything was recomputed by the role from
`experiments/results/replications/e4_nongauss{,_indep}/e4_mhd3d_s<k>_<group>.json` and `e4_reference.json`, not taken from the digest.
"Main" is `e4_nongauss`; "repl." is `e4_nongauss_indep`.

**Headline:** every number recomputed matches the result files and the digest, and the digest, the table and the two plots regenerate
identically. No number is wrong. Six sentences of the report say more than the data, and two of them are refuted by rows already in the
digest (items R1 and R2 below).

Side effects disclosed by the role: `python3 digest.py` rewrote `experiments/results/e4_selection.json` with identical content (git shows
it unchanged). Tables and plots were written to the scratchpad only.

## 1. Digest additions

| Item | Verdict | Evidence |
|---|---|---|
| `results/digest.md` equals what `digest.py` prints now | CONFIRMED | `diff` of the regenerated file against the stored one is empty. The stale-digest finding of the previous review is fixed. |
| "H25, η = …" lines with the jackknife SE | CONFIRMED | Main: 0.0542 ± 0.00695 trajectory SE (7.8), jackknife ± 0.00781 (6.9); −0.137, jackknife ± 0.00429 (−32); −0.270, jackknife ± 0.00712 (−38). Repl.: jackknife ± 0.0121 (4.9), ± 0.00567 (−24), ± 0.00793 (−34.5). Ratios W9/reference −0.10 / 0.60 / 0.44 and −0.19 / 0.63 / 0.41. Seeds at half magnitude 0 / 5 / 0. The jackknife formula in `e4_mhd3d.py` is the correct delete-one form. |
| "H25, check at the training η = …" lines | CONFIRMED | Main: differences +0.00629 (1.65 / 0.47 / 0.45 in SE of G1 / of the reference / combined), −0.00584 (−1.09 / −1.07 / −0.76), +0.00782 (1.83 / 2.31 / 1.44). Repl.: 0.39 / 0.09 / 0.09, 1.31 / 0.62 / 0.56, 1.28 / 0.59 / 0.54. The SE convention is written in each line. |
| The same check at the validation η (not in the digest) | REFUTED on one cell | The files also hold the two validation η, where G1 is interpolated. Main is fine (at most 0.68 SE). Repl. at η = 0.0596: G1 P/D 1.0446 against a mean-flow part of 1.0567, i.e. −4.2 SE of G1, −2.6 SE of the reference, −2.2 combined. Outside the registered check (training η only), but it bounds "G1 has the mean-flow part right" at interpolated η to about 1 %. |
| Three training η (0.0658, 0.0444, 0.0365) | UNCHECKED | Still not evaluated in the files. |
| "Post hoc (review of H25-H27, not registered)" line | CONFIRMED | Rise: W9 0.1197, G2 0.1553, G1 0.1077, G3 0.1035, G0 0.2079 (repl. 0.125 / 0.160 / 0.108 / 0.109 / 0.210). Largest \|a\|: 0.128 / 0.134 / 0.104 / 0.093 / 0.196 (repl. 0.114 / 0.122 / 0.118 / 0.119 / 0.211). Excursion: 0.0029 / 0.0265 / 0.104 / 0.092 / 0.188 (repl. 0.018 / 0.043 / 0.118 / 0.119 / 0.207). Labelled post hoc. |
| Paired row "excursion … (post hoc, not registered)" | CONFIRMED | Main 0.0237 ± 0.0036 (6.5 SE, 5 of 5); repl. 0.0256 ± 0.0030 (8.4 SE, 5 of 5). |
| "H27, energy distance between the samples of G2 and of W9N …" | CONFIRMED | 15 rows per run. Main 0.4275, halves 0.4111, at equal size 0.2056, ratio 2.08, 14 of 15 cells above. Repl. 0.4334, 0.3839, 0.1920, ratio 2.26, 15 of 15. |
| Monte Carlo null for the energy distance | UNCHECKED | Samples are not stored; the 1/n + 1/m scaling of the V statistic is analytic. |

The "about 2.2 times" of the previous review was the mean of per-cell ratios (2.25 and 2.34). The digest gives the ratio of means (2.1 and 2.3). Both are right; quote the digest.

## 2. Verdict texts in `research/hypotheses.json`

| Hypothesis | Verdict | What to change |
|---|---|---|
| H25 | CONFIRMED | Faithful to the review; every number recomputed. Add the validation-η cell above (repl., η = 0.0596, −2.2 combined SE) as a reported item. |
| H26 | CONFIRMED on the criterion; one caveat too narrow | "every law gains 11 to 16 % of E_B,ref" came from the previous review and is too narrow. Rises are G3 0.10, G1 0.11, W9 0.12, G2 0.16, G0 0.21, and W10 (evaluated in the same job, a(0) = +0.21) loses energy: rise −0.045. Replace with "every law that starts at or below the reference energy gains 10 to 21 % of E_B,ref (W10, which starts 21 % above, relaxes downwards)". "W9 0.127" should be 0.128; 0.127 is the maximum of the mean curve. |
| H27 | CONFIRMED; two additions | "2.2 times" should read "2.1 times (2.3 in the replication)" to match the digest. Missing: the registered reported item "signed restart curves" shows that the drift at τ = 4 does separate G2 from W9: 0.170 against 0.124, paired +0.045 ± 0.007 (6.5 SE, 5 of 5); repl. 0.172 against 0.126, +0.046 ± 0.006 (7.7 SE, 5 of 5). The report contradicts this (R1). |

Registration, status labels and the seed count are correct.

## 3. Report numbers

**Table `tbl-split`:** CONFIRMED. All nine data rows are verbatim in `e4_report_tables.py --print`. The reference row (0.00388, 0.00108, 0.00375) is computed from the mean curve of the 4 draws; the caption does not say this, and the per-draw stored values are 0.0051 and 0.0073. Add "from the mean curve of the 4 draws" to the caption.

| Sentence | Verdict | Evidence |
|---|---|---|
| Third-order part "decreases steadily from +0.14 at η = 0.08 to −0.31 at η = 0.03 and changes sign near η = 0.066" | CONFIRMED | 11 values: +0.139, +0.054, −0.0015, −0.049, −0.095, −0.137, −0.159, −0.199, −0.239, −0.270, −0.308, strictly monotone. Linear zero crossing at 0.0659 (repl. 0.0670, also monotone, +0.127 to −0.317). The numbers are in the reference file but only the three held-out ones are in the digest: add an eleven-value line to the digest. |
| "G1 has the mean-flow part right within 2 %" | CONFIRMED, at the limit | Seed means against the reference at held-out η: −1.9 %, −1.7 %, +0.7 % (repl. −0.3, −0.5, +0.4). Single seeds reach −2.3 %. At the training η: +0.8, −0.3, +0.5 %. |
| "the mean-flow part of W9 is 10 to 16 % below that of the reference at every η" | CONFIRMED for held-out η only | Held-out: −16.0, −11.4, −10.5 % (repl. −13.8, −10.7, −12.4). At the training η = 0.08 it is −18.1 % (repl. −18.6). Replace "at every η" with "at every held-out η". |
| "G1 … has 2.1 times the null points of the reference" | CONFIRMED as a mean over η | Mean `null_count_err_rel` 1.116 on test and 1.120 on train, so 2.12 times. Per η it runs from 2.46 (η = 0.08) to 1.60 (η = 0.03). Repl. 2.01 (test) and 2.07 (train). Say "2.1 times on the mean over η (2.5 at the largest η to 1.6 at the smallest)". |
| Rise "0.12 for W9, 0.11 for G1 and 0.21 for G0" | CONFIRMED | 0.1197, 0.1077, 0.2079. |
| Largest distance "0.13 for W9, 0.10 for G1; 0.11 and 0.12 on the second realisation" | CONFIRMED | 0.128, 0.104; 0.114, 0.118. |
| "the excursion of G1 is present at each held-out η, including the largest, where its production is below its dissipation" | CONFIRMED | Excursion per η 0.114, 0.091, 0.109; smallest single seed 0.071, 0.068, 0.095. P/D of G1 at η = 0.0725 is 0.928 (repl. 0.939). |
| W12: "starts 17 % below it and is still 11 % below at τ = 4, where the control goes from −12 % to −2 %" | CONFIRMED | Digest "Restart anchored" of `e4_mech`: −0.173 to −0.107; control −0.125 to −0.018. |
| S_w2048: "starts 10 % below and is 3 % below at τ = 4" | CONFIRMED | Digest of `e4_scan2`: −0.0977 to −0.0331. |
| The approximate initial energy behind those two | Measured here | In the two new runs, where both values exist, the approximation differs from the exact one by at most 0.009 on a(0) and 0.009 on a(4). The two sentences hold to ± 0.01; say so once. |
| Null-count difference "0.04 ± 0.03 (second realisation 0.04 ± 0.02), out of 1.7" | CONFIRMED | 0.0427 ± 0.0283 (1.5 SE, 4 of 5); 0.0436 ± 0.0178 (2.5 SE, 5 of 5); W9 is at 1.69 (repl. 1.57). |
| "G2 is 0.6 to 0.9 floors farther from the reference than W9" | CONFIRMED | +0.557 ± 0.263 (2.1 SE, 4 of 5); +0.895 ± 0.040 (22 SE, 5 of 5). |
| "σ(dE/dt) 1.63 for W9 and 2.45 for G2" | CONFIRMED | 1.632 and 2.449 (repl. 1.699 and 2.453). |

Other numbers of the section and of the sentences elsewhere: CONFIRMED, all in the digest (courses of W9, G1 and G0; overshoots; P/D of W9; over-production of G1; H27 differences and null control; excursion difference; drifts at τ = 4; "9 and 17 %"; "24 hypotheses").

**Sentences that say more than the data:**

- **R1, REFUTED** (sec-nongauss, last paragraph): "on the two metrics in which the model had seemed to stand out, the null count and the restart drift, its non-Gaussian part changes little: the registered measures do not separate it from its Gaussianisation." The restart drift of the objectives does change: 0.124 for W9 against 0.170 for G2, +0.045 ± 0.007 (5 of 5 seeds, both realisations): digest row "\|drift of E_B\| at τ = 4: G2 − its base W9". Only the registered overshoot is blind to it. Replacement: "on the null count its non-Gaussian part changes little (0.04 out of 1.7), and the overshoot registered for the restart does not separate the model from its Gaussianisation; the drift at τ = 4 does (0.124 against 0.170 for G2, in the five seeds on both realisations), as does the excursion above the reference computed after the fact." Same correction in the discussion and in the limits.
- **R2, REFUTED** (paragraph on H18): "the drift … is lower for the learned models than for G0 because of how their second moments relax, not because of what a Gaussian law cannot hold." G0 is at 0.212, G2 (the second moments of W9) at 0.170, W9 at 0.124: about half of the gap to G0 is second-order and half is lost on Gaussianising. Replacement: "… is lower than for G0 partly because of their second moments (the Gaussian law fitted to the samples of W9 is at 0.170 against 0.212 for G0) and partly because of their non-Gaussian part (0.124 for W9); and a Gaussian law, G1, is lower still (0.064), so the clause does not measure what a Gaussian law cannot hold."
- **R3, REFUTED as worded** (sec-nongauss, abstract, comparative text, conclusion 6): "every law gains magnetic energy after the restart, by about the same amount." W10, in `tbl-split` with a(0) = +0.211 and overshoot −0.045, loses energy monotonically; G0 first loses 16 %; the rises span 0.10 to 0.21, a factor of two. Replacement: "every law that starts at or below the reference energy ends up gaining magnetic energy, by 0.10 to 0.21 of the reference energy (0.12 for W9, 0.11 for G1, 0.16 for G2, 0.21 for G0, which first falls by 16 %); W10, which starts 21 % above, relaxes downwards."
- **R4, overstated** (limits): "the distance does not separate the best learned model from its Gaussianisation." Replacement: "the distance barely separates … (0.43 floors, about twice the sampling value; G2 is 0.6 to 0.9 floors farther from the reference)".
- **R5, status** (sec-nongauss, last sentence; discussion; conclusion 6): "G1, at the training η as at the held-out ones, has 2.1 times its null points and leaves its stationary energy at restart." The restart is run only at held-out η, where G1 is interpolated in η; G1 is fitted on 2400 snapshots. Replacement: "G1 has 2.1 times its null points on the mean over η, at the training η as at the held-out ones, and at the held-out η, the only ones where the restart was run, leaves the stationary energy by 9 to 11 %". "The topology and the stationarity of the reference are non-Gaussian properties" is then measured for the null count; for stationarity write "as far as G1 at interpolated η shows".
- **R6, minor wording:** "a quarter of what the mean flow produces" is 21 % at η = 0.0331 (write "about a fifth"); "none at the third" should be "a small part of the opposite sign at the third"; "equally far" should be "comparably far (0.13 and 0.10; 0.11 and 0.12)"; W10 also has anchored curves; "for lack of restart samples (128)" should be "traced by the review to the sampling noise of a(0) on 128 restart samples"; "H26 is confirmed" against "supported" in the register: use one word.

## 4. The two data plots

| Item | Verdict | Evidence |
|---|---|---|
| Plots regenerate from the code and files | CONFIRMED | `e4_plots.py --out <scratchpad>` gives PNG files byte-identical to the committed ones. |
| `plot_production` | CONFIRMED | Reference bars carry ± 2 × the jackknife SE; laws carry seed mean ± 2 × SE over 5 seeds; W9 is read from `W9N_skip_sym`, bit-identical to `W9_skip_sym`. The report caption matches. |
| `plot_restart` | CONFIRMED, caption incomplete | Laws: per-seed mean over the three η, then mean ± 2 SE over 5 seeds. Band: mean over η of the 4-draw mean, ± 2 × the mean over η of the 4-draw SE. Replace the caption with "(bars: ± 2 standard errors over the five seeds); grey band: reference snapshots, mean ± 2 standard errors over 4 draws of 128". The band uses the mean of the three per-η SE, not the SE of the mean over η, so it is wider by up to √3: conservative. The 4 draws are taken from the same 2400 snapshots and may overlap. |

## 5. Not checked

- Convergence of the restart solver in time step and resolution (GPU needed).
- Small-sample bias of the split: the mean flow includes each sample's own velocity, which biases the third-order part towards zero by roughly 1/N_eff (at most about 4 % of its value for the reference, 0.2 % for the laws). It would not change a verdict.
- A Monte Carlo null for the energy distance.
- The H25 check at the three training η missing from the files.
- The H18 figures and other numbers from before commit 245c783.
- The rendered PDF and HTML of the report; only the `.qmd` source was read.

**Verdict on the whole:** the digest additions, the table, the two plots and every quoted number are confirmed against the result files. The H25-H27 verdict texts are faithful, with two additions (the range of the rise with W10 excluded; the drift at τ = 4 of G2 against W9). The report needs the six rewordings above before these results are quoted. R1 and R2 are contradicted by digest rows, R3 by a row of the report's own table; the rest are scope or status.
