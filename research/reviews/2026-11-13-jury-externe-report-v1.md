# Review by `jury-externe` — commit c0f3cdf: internship report v1 of team claude

Due review named by `tools/review_due.py` ("milestone changed"). Role `jury-externe` (sub-agent, model and effort of the role file), 2026-11-13, 00:29–00:58 UTC. Reviewed: `site/teams/claude/report/index.qmd` and `index.pdf`; the three pending parts (long trainings, width scan, replication) excluded. The role recomputed the comparative table from `experiments/results/e4_mhd3d_s<k>.json` (all values match), regenerated the digest (identical) and ran the 16 toolbox tests (pass).

Strengths noted: registration precedes results in git (H15–H21 checked), negative results are kept, the table is exactly reproducible.

## Verdict per claim

| Claim (location) | Verdict | Evidence and correction |
|---|---|---|
| "Factor of about twenty" (abstract, H17) | HOLDS | 209.8 → 9.35 floors (22.4; 30.2 at the training η), 5 of 5 seeds. Add that W9 also changes the embedding (`cond_scale` 0.5 against 8): not "the same network". |
| G0 "is not a dynamo"; remark on independent modes | Fact HOLDS, argument WRONG | Production over dissipation P/D is −0.003, but because the modes are independent, not because the law is Gaussian or homogeneous: the mean flow holds 70 % of E_u, and in the reference, mean flow × inter-mode covariance of B gives P/D = 0.94, 1.13, 1.28 at the held-out η. Delete "one thousandth": the residual saturates at −1 for P ≤ 0 (9 of 15 cells). |
| "Restore the balance (0.06 against 1), halve the drift" | OVERSTATED | The residual is normalised by abs(P) + D: 0.06 means production 2 to 21 % off (signed −0.118, −0.039, +0.009); first-generation models were at 0.15–0.26. Drift 0.212 → 0.124 is −42 %. Quote P/D per η. |
| Identities "including E⟨j·B⟩ = 0 lower the residual they target … and nothing else" | WRONG | That identity's residual `r_b`: 0.090 → 0.086 (−0.004 ± 0.009). Against the control: magnetic residual 0.251 → 0.516, null error +0.56 ± 0.06, B-spectrum error −0.56 ± 0.08. Claim the energy identity only. |
| Proposition, π/2 | HOLDS | Verified numerically. π/2 only needs unit mean second moment. |
| Rank argument | WRONG description | `ResMLP` is Linear(5320 → 512), blocks, Linear(512 → 5320): no identity term, rank ≤ 512 exactly. Only its causal role is conjectural (H21). |
| Protocol bullets (Results) | HOLD, two errors | "Equivalent at training η": diffusion is better, −15.06 ± 0.90, 0 of 5 seeds. "Doubled": 50 → 200 steps. "Twice as far" holds (1.97, one penalty weight). |
| Losses 1.60–1.63 | OVERSTATED status | Only in CPU training logs, seeds 0–2; absent from result files and digest. Store `fm_loss_train_sample` for W0, W4, W4s. |
| Null counts | WRONG | "Every generator has too many": W1 0.28×, W6 0.58×. "Follow the small scales": digest intercept 1.04, 2.8× at the reference k_λ. |
| State of the art | HOLDS, three caveats | Brandenburg–Subramanian Eq. 3.34 is tagged "re-read before quoting"; Csiszár 1975: exponential form unconfirmed beyond the finite case; Galloway–Frisch unread. |
| Prose numbers | HOLD, four errors | About 30 match. Wrong: "three to five times" (3.0–6.0), "some thirty features" (21), "35 to 60 s" (up to 98). "About 0.6" is an extrapolation. |
| Comparative study | Form HOLDS; selection OVERSTATED | 217(14) is explained. "Lowest ratio on validation" is false: G0 has 3.95; its exclusion entered in commit 1c21afc, after its results. G0 would meet 7 of 9 objectives, W9 5. The W7 row is one sample. |
| Limits | OVERSTATED (incomplete) | Add: C1 is inside the floor uncertainty (9.95 with the 20-split floors; seed 1 at 10.15); the "homogeneity" limit is false here. |
| Form | HOLDS, defects | No "??", 35 of 35 references. Hypotheses table: nine literal `$-$`, "/x/" for absolute values, verdicts cut mid-sentence. |

## Five most serious problems

1. **The central interpretation is refuted.** "The third-order correlations that make the field a dynamo" is not measured and is false. An oracle Gaussian with the full covariance of the reference at each held-out η gives magnetic residual 0.07, E_B restart drift 0.058 and null error about 1.05, against 0.055, 0.124 and 1.67 for W9; its E_u drift is worse, 0.087 against 0.053. On the four stored W9 fields the mean-flow part alone gives P/D = 1.02. Required: a baseline G1 with inter-mode covariance, fitted on the training η, in the table.
2. **The stationarity-loss claims** of the abstract, contribution 4 and conclusion 4 contradict the report's own table.
3. **Mechanisms are compared only in the failed regime.** No loss or sampling mechanism was tested on W9, and the selection rule changed after the fact.
4. **The diagnosis rests on unstored numbers and a misdescribed architecture**; the matched control for W9 is the pending width-512 scan variant.
5. **Fragile metrics.** At a single τ the restart test hides a transient: in a rerun at η = 0.049, G0's E_B is −16 % at τ = 0.5 and +22 % at τ = 4, and its E_u +16 % at τ = 1, so "G0 better on E_u" is an artefact. Report several τ.

Not checked: pending parts; registration order of H4–H14; primary papers. The oracle uses held-out data (two draws of 128 samples): it refutes the attribution but is not a fair baseline.

## What the main session did with it

See the journal entry of 2026-11-13 (01:10 UTC and later): hypothesis H22 and the baseline G1 (Gaussian law with the full covariance of the latent, fitted at the training η) registered and run with restart curves at several τ; the abstract, the methods, the results, the limits and the conclusion rewritten on every line of the table above.
