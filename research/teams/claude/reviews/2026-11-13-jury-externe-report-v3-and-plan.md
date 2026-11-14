# Review by `jury-externe` — commit 8a0f33a: report v3, race report, and the protocol of the next experiment before it is run

Review due on the report v3 ("milestone changed"). Role `jury-externe` (sub-agent, model and effort of the role file), 2026-11-13, 04:33–05:08 UTC. Numbers recomputed by the role from the result JSON.

## Part A — report v3

- FIXED: the over-statement on G1; the non-Gaussian claim ("was not tested"); the matched control (per seed 20.0–24.5); production over dissipation per η; every other item of the v2 review not listed below.
- PARTLY: "5 of the 15" (the hypotheses table still says 6; recount 5); "the learned variant with the lowest ratio" (on validation in `e4_mech`: W13 6.91, W12 control 8.56, W9 8.86); race report "2.6 floors" and two ranges (corrections of the encadrant right, not yet committed).
- NOT FIXED: losses of W0, W4, W4s from logs (disclosed).

New problems:

1. **Major: the restart metric.** The drift is taken against the ensemble's own initial energy, so its long-time limit is E_ref/E_gen − 1, the bias on E_B, not zero (deduced; measured to τ = 4 only). Across the learned variants of the four runs, the drift at τ = 4 correlates at 0.96–0.97 with that bias. W9 (by decreasing η): bias +0.18, +0.14, +0.12; drift +0.15, +0.11, +0.11, monotone. At τ = 4, W9 is within about 2 % of the reference energy, G1 4–7 % above, G0 17–23 %; same order on the second realisation. So "G1 … lowest magnetic restart drift", "[the loss] lowers the restart drift" (W12 ends 5–17 % below the reference, its control 1–2 %) and "the drift is a transient" fail as interpretations. H22 stands as registered.
2. "Beat both Gaussian laws on the kinetic restart drift": false at τ = 4 against G0 (0.026 against 0.053); "magnetic drift at earlier times": fails at τ = 2.
3. "Most of the magnetic production" against P/D up to 1.28; the magnetic-balance claim of the abstract is false for W12 (0.113).

## Part B — protocol of the next experiment

1. **Production split.** Discriminates for W9 and W11 only: the clause on the reference is already decided, since at the training η G1 has the first two moments of the data, so the third-order part of the reference is 1 − P/D of G1: +0.13, −0.09, −0.32 at η = 0.08, 0.054, 0.03 (held-out, by interpolation: +0.07, −0.12, −0.28): it changes sign. Register these values and check that the mean-flow part of the reference equals P/D of G1 at the training η. For W9 two readings stay open: a cumulant of −0.14, −0.19, −0.26 (wrong sign at η = 0.0725), or none and an inter-mode covariance 15–20 % too weak. Changes: a two-sided band per η (0.5 to 1.5 times the reference), an explicit rule over η, the mean-flow part of W9 registered, a jackknife SE with the mean flow recomputed.
2. **Gaussianised W9 (G2).** Discriminates and is well controlled (same initial energy, same limit as W9). Invalid if the retrained base differs from the evaluated W9 (evaluate the base in the same group) or through the fit: 2048 samples are rank-deficient: use at least 8192, add the null control "Gaussianised G1 against G1", check that G2 keeps the spectra of W9. Compare signed curves per η; add τ = 0.125 and 0.25. Measure the energy distance between G2 and W9 samples directly. A positive result shows that W9 is non-Gaussian, not that it is right.
3. **Longer restart.** Does not discriminate as worded (predicted: G0 and G1 pass, W9 fails). Record E(τ)/E_ref − 1 with the reference curve and its SE over several draws; test the residual at τ = 16 against that floor, and an overshoot against a monotone relaxation.

Fit to deliver as it stands: no. First re-anchor the restart drift on the reference energy (computable from the stored JSON) and rewrite the restart sentences; then the residues above.

## What the main session did with it

Restart drift re-anchored on the reference energy in the digest (from the stored results) and in the new runs; the restart sentences of the report rewritten; the three tests redesigned as asked (band per η, jackknife, base evaluated in the group, 8192 samples, null control, direct distance, reference curve with its SE) and registered as H25–H27 before the run.
