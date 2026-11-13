# Review by `jury-externe` — commit 9e947e8: internship report v2 and race report

Due review named by `tools/review_due.py` ("milestone changed"). Role `jury-externe` (sub-agent, model and effort of the role file), 2026-11-13, 03:47–04:10 UTC. All table values recomputed by the role match.

**Verdict: not fit to deliver as it stood: v2 fixes the central error of v1 but overstates the G1 result.**

## 1. Corrections asked on v1

- FIXED: central interpretation; stationarity-loss claims; description of the network and of the rank argument (exact; its causal role a conjecture; the bound is 1024 for the equivariant field); protocol bullets; mechanisms tried on W9; limits; numbers; citations; hypotheses table.
- Methods remark on the magnetic production of a Gaussian law: exact (Isserlis theorem, E[B] = 0). The conclusion for independent modes is correct and stronger than written: the production is exactly zero. "Can have the right production" for a Gaussian law with the inter-mode covariance is inexact.
- PARTLY: the factor of twenty is quoted against 210 (W4s) where the matched control is at 205; production over dissipation per η not quoted; the losses of W0, W4, W4s still come from logs; section title "null points follow the small scales"; selection of the generator ("the variant with the lowest ratio" is false; "G0, which has the lowest": G1 has, 2.50 against 3.95); restart curve measured but headline claims still at τ = 4.

## 2. New claims

- "G1 is the best generator on almost every metric": OVERSTATED. It is the best on the energy distance only. Magnetic balance: W9 0.055, W13 0.038, S_w5632 0.037, G1 0.072, G0 0.998 (gap of 7 to 21 SE, on both data realisations for W9). G1 has production over dissipation 0.93, 1.12, 1.28 at the three held-out η (W9: 0.79, 0.93, 1.02): the residual of G1 is the third-order cumulant that a Gaussian law lacks. Restart drift of E_B at τ = 0.5, 1, 2, 4: W9 0.012, 0.043, 0.086, 0.124; S_w2048 0.031, 0.043, 0.045, 0.072; G1 0.058, 0.097, 0.104, 0.064: G1 beats W9 at τ = 4 only; over the curve S_w2048 (0.074) and W12 (0.080) are below G1 (0.108). σ(dE/dt) over the reference: W9 1.63, G1 2.99, G0 1.37. Null error: W6 0.43, W8 0.71, S_w5632 0.96, G1 1.10. H22 stands as registered.
- "Nothing measured here shows that any learned model captures a non-Gaussian feature": OVERSTATED, because it was not tested. Proposed wording: no learned model beats G1 in energy distance; several beat both Gaussian laws on the magnetic balance, the kinetic restart drift and the magnetic drift before τ = 4; whether these are non-Gaussian features was not tested. Settling tests: a full-covariance Gaussian fitted to W9 samples; the production split into mean flow × covariance and cumulant; a restart to τ ≥ 16.
- Abstract: holds except "Thirteen variants … a Gaussian baseline", "best … on the null points" (true within 60 floors only), "restart of the magnetic energy" (τ = 4 only) and the non-Gaussian sentence.
- Conclusion: items 1, 2, 4, 5 hold; item 3 overstated ("lowest error on the null count" is wrong); one conjecture stated as a result in the discussion.
- Mechanisms: holds; "6 of the 15" is 5; "four quantities" omits the kinetic-energy error. Long and wide: holds; "in every seed and at every η" fails at η = 0.0725 for W11L; "best null-count error of all the networks" is wrong.
- Race report: numbers verified; wrong: "best: 2.1 times", "no law is below 1.10", "1.67 for the best learned model"; overstated: "No learned model beats two Gaussian laws", "changes no verdict" (H18, H21, H23, H24 have one data realisation).

## 3. Remaining problems by severity

1. Over-correction on G1 (abstract, section on the two Gaussian laws, comparative text, conclusion 3, race report).
2. Null-count superlatives and single-time restart claims, contradicted by the report's own table and curve.
3. Stale sentences from v1 in seven places.
4. Form: no "??", no broken reference; tables legible, some adjacent columns touch.

Not checked: C6 = 17; "26 to 99 %" (the floor file gives 35 to 74 %); registration order of H4–H14; primary papers.

## What the main session did with it

Every item of sections 1 to 3 corrected in the report v3 and in the race report (journal, closing entry); the numbers of section 2 were recomputed by the main session from the result files before being written. The three settling tests are listed as remaining work. No further review was run on v3.
