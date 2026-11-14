# Review by the `jury-externe` role: report v6 against the criteria of the internship offer

Date: 2026-11-14, 00:08–00:30 UTC. Scope: `site/teams/claude/report/index.qmd` at commit b227bd5 (version 6, organised around the requirements of the offer), the results of H38 to H41, the polarity diagnostic, the data release. The criteria of the offer (`docs/specs/sources/supervisors.md` §1.2 a) were given in the task, with the request to judge whether the work and the report answer them and to name what departs from them or is detail without impact. The role edits nothing; its report is copied below, and the follow-up of the main session is at the end.

**Basis.** I read `/home/user/milady-2027/site/teams/claude/report/index.qmd` in full (PDF not opened). I recomputed H28, H38, H40, H41 and rank 30 from the raw JSON, the polarity diagnostic through the committed `measure()` (identical to the committed JSON) and the forcing symmetry. I ran the e4 format test, three checksums and three validations. No GPU job; `git status` clean afterwards. The two late changes (symmetry sentence, regenerated release) were not re-read.

## Verdicts

| Point | Verdict | Evidence |
|---|---|---|
| A `@tbl-offer` | REFUTED on 4 rows, 8 CONFIRMED | (1) "Generative models: Covered" is Partly: one diffusion model, first generation only, at 519 floors, never retrained with the affine term; no learned model as trained beats G1 (2.55) or G0 (3.52). (2) "Sixteen mechanisms": `REGISTRY` holds 11 constraint mechanisms (4 design, 2 loss, 5 sampling), the unconstrained baseline and 4 model families; the B → −B equivariance is not in it. (3) "the fields are written in the data format": only reference fields are (manifest `model_files: []`; the Toolbox paragraph says so). (4) "Comparative study: Covered" lacks its restriction: 12 of 16 lines are models 117 to 519 floors away. Undersold: the Rice route (D). |
| B Abstract | REFUTED on 4 sentences | "about twice its null points": 2.0 (G1, W16), 2.7 (W9), 3.2 (G0). "sixteen … constraint mechanisms, a diffusion sampler" double-counts. "the same conditions" has no antecedent. "each registered … before its computation": H35 and H36 had checks amended after a first cycle. Confirmed: 665, 5320, Rm, 38, 10⁻⁸, 205 → 9.3, 3.5 and 2.5, 0.6 and 0.4, 17 to 80. Not recomputed: W16 figures, 0.05 to 0.13, 64 against 32. |
| C H40/H41 | CONFIRMED, 3 specifications | Recomputed: 1.208 → 1.151; 2.52 → 16.4 floors; E_B +11 to +15 %; H41 differences −2×10⁻⁵, 1.0×10⁻⁴, 1.3×10⁻⁴; 0.31 and 0.24; 43.8 and 44.1 floors; 0.43 to 0.60. "0.11" is the main-run mean (0.103, 0.106, 0.116; second realisation 0.085, 0.090, 0.114). "Below 0.003" holds for seed means (largest 0.0017); single seeds reach 0.0046. Omitted: the eigenvalue floor of the H28 and H38 anchors is untested (review of H41). No causal wording, no threshold in the rank. |
| D `{#sec-polarity}` | Numbers and symmetry CONFIRMED; one sentence REFUTED | Shares 0.202 to 0.244; 1/e times 17.1, then 67.0, 80.5, 66.2; opposite at the end 0.403 to 0.597; 198/τ = 2.46 to 11.6; 1/η = 12.5 to 33.3. The solver force equals the report's formula and is invariant under a shift of π along each axis (1.6×10⁻¹⁶; not under π/2); your replacement sentence is correct. "None of the dynamics" contradicts Proposition 8 of the theory brief: the mean rate of sign changes depends only on the law and the equations. Also, the shell k = 1 of `@tbl-data` (0.37 to 0.44) includes the six wavevectors of modulus √2; the text gives 0.20 to 0.24 without saying so. |
| E `{#sec-beyond}` | CONFIRMED, 2 specifications, 1 UNCHECKED | 318 024 and 2 456 496 coefficients; 1.42×10⁷ and 5.06×10¹⁰ entries; 194 MiB; Pm 0.625 to 1.67; 6 to 16; 2.5 to 12. Berhanu, Nore and The Well match the source files; Proposition 9 is described correctly. "The best one passes 4.6 %" is the main run only (6.3 % on the second realisation, per the H30 paragraph). Threshold figures (0.09 to 0.095, factor ten): record not looked for. "Whose format the tools read": UNCHECKED. |
| F Release | CONFIRMED in part | Test: 1 passed. SHA-256 of the η = 0.08, 0.049 and 0.03 files match. `validate --full`: valid for two files and the sample. README states the realisation and the missing W9 weights. Manifest gaps −2.5 to +1.9 %, round trip at most 1.7×10⁻⁷. But `experiments/data_e4/` holds four checkpoints (W4s, W5; seeds 0, 1): "the weights of the trained models were not kept" is false as worded. Catalogue against `e4_recolour`: UNCHECKED (cut off, and regenerated since). |
| G Summaries | REFUTED on 1, 2 loose | H36 "is not reduced": the appendix gives 0.159, 0.097, 0.141 against 0.151, 0.119, 0.110 and concludes only "not halved". H32 "1.4 to 1.6 … holds at the two lower ones": the appendix gives 1.4 to 1.5 there. H34 "no deficit": −5 % at one value. H35, H39 and `{#sec-complements}` agree with the appendices. |
| H Consistency | Counts CONFIRMED; 3 gaps | 41, 38, 19, 17, 2; 16 entries; 18 tests (not run). No "running" seen on a full read. `@tbl-commits` stops at H25 to H27, yet its caption vouches for all registrations. "The exceptions are named" fails for H38 and H39. C6 shows 32. `research/race-report.md`: UNCHECKED. |
| 1 Generative models | Partly answered | As A(1); a flattened vector of 5320 coefficients. |
| 2 Conditioning | "Partly" CONFIRMED | η alone, Pm moving with it, Re = 10, saturated branch; five unseen values interpolated. |
| 3 Constraints | Divergence CONFIRMED; energy balance "Partly" CONFIRMED | At most 3.1×10⁻⁸ against 0.26 to 0.45. The loss buys its residual and degrades the law (9.3 → 16.4). |
| 4 Metrics | CONFIRMED as measurements; topology not preserved | Eight shells at Re = 10, so no inertial range; errors of means. |
| 5 Fields for ROM or DA | Not answered | No generated field in the format; every ensemble leaves the stationary energy. |
| 6 Context | Not answered | Reversals: symmetry and one descriptive diagnostic. Data: 2.08 GiB. |
| 7 Deliverables | Study answered with A(4); toolbox "Partly" CONFIRMED | |

**(i) Departures.** Fourteen of 38 hypotheses (H28 to H41) ask why a network learns or misses a third-order part, which no criterion asks; the anchor chain ends "cause not identified".

**(ii) To an appendix.**
- The H28/H38/H40/H41 paragraph, keeping three sentences.
- The "ceiling" paragraph of H37, which concludes it is neither a ceiling nor an explanation.
- The objectives paragraph closing `{#sec-origin}`.
- The `encadrant` paragraph of H26 and the detail of H27.
- `@tbl-hypotheses`, `@fig-workflow`, `@fig-agents`.
- The version history in "Negative results".

**(iii) Limits.** Stated early and clearly (status note, abstract, table, lead of Limits). Missing from the first page: the flow is smooth, not turbulent, and Pm is of order one.

## Required corrections

1. **BLOCKING.** "…has the symmetry and none of the dynamics; what a study of reversals would need is in @sec-beyond." → "…has the symmetry and, of the dynamics, only what the law and the equations fix: the mean rate of sign changes of a large-scale amplitude (Rice formula, Proposition 8 of the theory brief), not computed here; it gives neither waiting times nor the course of a reversal." In `{#sec-beyond}`, "A generator of independent snapshots cannot reproduce them." → "…cannot reproduce their course or waiting times; their mean rate can be estimated from snapshots (Proposition 8), on the reference first: not done."
2. **BLOCKING.** "the fields are written in the data format of the project" → "only the reference fields are written in the data format of the project".
3. **BLOCKING.** Row 1: "Covered" → "Partly", adding "one diffusion model, of the first generation only; no learned model as trained is closer to the reference than a Gaussian law". Comparative-study row: add "twelve of sixteen lines are models more than 100 floors away". Then "three are covered only in part" → "four".
4. **BLOCKING.** "sixteen tested constraint mechanisms, a diffusion sampler" → "sixteen tested registry entries (eleven constraint mechanisms, the unconstrained baseline, a diffusion model, three Gaussian laws)"; same in `@tbl-offer`, contribution 5 and `@tbl-toolbox`.
5. **BLOCKING.** "about twice its magnetic null points" → "two to three times its magnetic null points" (abstract and conclusion 8). "meets the same conditions" → "reaches a null-count error of at most 0.2 with a magnetic energy within 5 %".
6. "flow matching interpolates in η better than the diffusion model" → "…than the one diffusion model tried, both being more than 150 floors from the reference".
7. "…so a fault specific to that case is not excluded." → "…and the eigenvalue floor used only by the anchors of H28 and H38 is not exercised at all, so a fault specific to those cases is not excluded." "(below 0.003 of the dissipation)" → "(seed means below 0.002; at most 0.005 in any seed)".
8. "is not reduced" (H36 summary, conclusion 7) → "is not halved (0.16, 0.10, 0.14 against 0.15, 0.12, 0.11)".
9. "which hold 0.20 to 0.24 of the magnetic energy" → add "(the shell k = 1 of @tbl-data also holds the six wavevectors of modulus √2)".
10. "(the best one passes 4.6 %…)" → "(the recoloured model passes 4.6 %, 6.3 % on the second realisation…)". Give the result file of the threshold diagnostic or delete its figures.
11. "the weights of the trained models were not kept" → "the weights of the cited flow-matching model were not kept; the job option that returns them was not run".
12. Complete `@tbl-commits` for H28 to H41 or restrict its caption. "each registered … before its computation" → add "(the checks of H35 and H36 were amended after a first cycle)".
13. Add to `{#sec-beyond}` the size of the nearest published MilaDy data set (Bousquet et al. 2026 in `supervisors.md`: Re = 1594, Rm = 531, 2000 snapshots), a cost for the 64³ step, and a refutation criterion per first step.

## Not checked

- The rendered PDF, cross-references, `check_gates.py`, `make test` (only the e4 format test ran).
- `research/race-report.md`.
- The catalogue against `e4_recolour/e4_mhd3d_s0.json`; the regenerated catalogue and manifest; `e4_release_example.py`, which says it reloads W9 from a weight file that does not exist.
- Raw recomputation of H29 to H37 and H39 (read in the report and register only).
- The offer PDF itself: the quotation "reproducible code integrated into the project toolbox" is not verbatim in the fact base.
- What `race_metrics.py` counts for C6.

Scratch files, outside the repository: `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/pol_check.py`, `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/sym_check.py`, `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/pol_recomputed.json`.

## Follow-up of the main session

- Blocking corrections 1 to 5: applied as proposed (what a snapshot generator fixes of the dynamics, with Proposition 8; "only the reference fields are written in the data format"; "Generative models" and the comparative study restricted in the table of the offer, "four are covered only in part"; "sixteen tested registry entries (eleven constraint mechanisms, the unconstrained baseline, a diffusion model, three Gaussian laws)" in the abstract, the table, the contributions and the toolbox table; "two to three times its null points" and the explicit conditions of the relaxation time).
- Corrections 6 to 10 and 12: applied (the one diffusion model; the eigenvalue floor untested and the per-seed bound of the third-order part; H36 "not halved" with its numbers, H34 with the signed deviations, H32 with the value at the two lower η; the shell k = 1 of the data table; 4.6 % and 6.3 %; the caption of the table of commits restricted to H4 to H27 with a pointer to the register; the amended checks of H35 and H36 named in the abstract; the exceptions to "two realisations" named).
- Correction 10, threshold diagnostic: it is the main session's own CPU diagnostic, recorded in the journal on 13 November (six trajectories per η over 800 time units) without a committed result file; the sentence now says so and gives only what the journal records.
- Correction 11 (weights): superseded by the release asked by the owner on 14 November: the section "Data and models" is rewritten with the published files; the checkpoints W4s and W5 of the container are early models that the report does not cite.
- Correction 13: the published data set of the project (Bousquet et al. 2026: Re = 1594, Rm = 531, 2000 snapshots, not public), a cost for the 64³ step from the measured solver timing, and two proposed criteria (marked as proposals, not registered) were added to the section on what larger systems need.
- Moves to an appendix asked in (ii): not done for the H28 to H41 paragraph and the hypotheses table, which the owner's goal asks to keep summarised in the text or in an appendix; the choice is recorded here: the anchor chain stays in the main text as one paragraph because the abstract and the conclusion cite it. Not blocking according to the review.
- Second reading asked from the role on the corrected text and on the published downloads (links, reload of a model, samples): see the next review file.
