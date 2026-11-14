# Review by the `jury-externe` role: final reading of the report, and confirmation after its corrections

Date: 2026-11-14, 06:30–06:55 UTC. Scope: the final version of the report (`site/teams/claude/report/index.qmd`, PDF of 101 pages: 71 of text and nine appendices) at commit 8a97c22, after the moves to the appendices that the review of the version 6 had asked, then the same at commit 83c2d27 after the corrections of this reading. The criteria of the internship offer were given in the task, with the request to judge whether the work and the report answer each of them. The role edits nothing; its two answers are copied below, and the follow-up of the main session is between them.

## First answer: reading at 8a97c22

Two blocking points remain, both created by the move commit: the topology summary left the main text, and the new headline of the anchored-model summary over-generalises. Your seven corrections of 14 November are closed and `{#sec-release}` holds.

Basis: 15 tool calls, nothing edited, no GPU, tree clean afterwards. I read the whole `.qmd`, diffed 8a97c22~1 against 8a97c22 sentence by sentence, and read the register entries H26–H28, H31, H32, H35, H37–H41 and the digest lines of H31, H35, H39. I also read the map code of the cited run and of the release, and ran `make test` (exit 0), ruff (clean) and `check_deliverables.py` (29/29).

| Point | Verdict | Evidence |
|---|---|---|
| A. Moves | Numbers CONFIRMED; REFUTED on two points | Nothing was lost: the moved text is verbatim, and the 8 sentences that disappeared are leads or the sentences the summaries replace. Every number in the summaries equals the appendix and the register (10 to 21 %; 5×10⁻³; 2.5 → 16.4 floors; 0.81, 0.76 and 0.73, 0.68; 18.8, 19.5; five of nine). (i) Old L585, "Topology and the solver (H32, H35, H39)", had no blank line after the objectives paragraph and left with it: now L1160 in `{#sec-objectives}`, PDF p. 86, merged with L1159. (ii) The new headline of L562 says more than its paragraph and the verdicts of H28, H40, H41. |
| B. Consistency | REFUTED on the references to that paragraph and one abstract sentence | L560 "summarised at the end" (only H34 and H36 are); L630 "is in @sec-origin"; L148; L694. The caveats of the relaxation are now in appendices only (H35 is a test on one realisation; relaxed G1 passes too; stationarity of the relaxed ensemble not shown), while the abstract and conclusion 8 keep the numbers. `@fig-relax` (L610) is cited from appendices only. L115 "the same models retrained" against L769 "The released W16 is not the cited law". Otherwise confirmed: no unresolved reference in the `.qmd` or the PDF (101 pages, appendix A on p. 72); conclusion items 3, 5, 6, 8 and `{#sec-beyond}` agree with the appendices and the digest (L1547, L2341, L2572). |
| C. Seven corrections | CONFIRMED | Closed ×7: L640 and L897; L149; L138–L152; L115, L144, L165, L706 (`REGISTRY` has 16 entries: 11 + 1 + 1 + 3); L113, L148, L913; L747, L769 and the explorer; L812 and the explorer. |
| D. `{#sec-release}` | CONFIRMED | Both differences are in the code: `source_moments` symmetrises (`experiments/e4_mhd3d.py` L1189–1192), `moments_w9` does not (`experiments/e4_release_example.py` L111–122), and the default is 32768 samples (`experiments/e4_release_models.py` L38). Released W16 is at 2.94, 5.66, 5.37 against G1 1.26, 3.32, 3.06 and G0 1.81, 4.82, 3.94. Ranking not reproduced and no restart are both stated. The table is identical to the one the `encadrant` reviewed at fbb819f; rows B1 and B2 of that review support "both columns were recomputed". |
| E. Limits | REFUTED in part | 16³, Re = 10 and one parameter are on the first page (L97, L111). "Smooth" first appears at L363; the magnetic Prandtl number only at L899. `{#sec-beyond}` is CONFIRMED for the turbulent regime, the threshold and SFEMaNS (2.6 GPU hours, factor 160, Pm 0.6 to 1.7 recomputed). |
| 1 Generative models | Partly; report's status CONFIRMED | Flow matching on a flattened vector of 5320 coefficients; one diffusion model at 519 floors; no model as trained beats G1 (9.3 against 2.55). W16 leads G1 by 0.48 floor, under one floor, and trails it at η = 0.0725. |
| 2 Conditioning | Partly; CONFIRMED | η alone, with Rm and Pm moving together and Re fixed; three interpolated values inside the saturated branch. |
| 3 Constraints | Divergence answered, energy balance partly; CONFIRMED | 10⁻⁸ against 0.26 with the penalty; the loss halves its residual and costs 9.3 → 16.4 floors; the best balance is copied moments. |
| 4 Metrics | Measured; topology not achieved; CONFIRMED | Two to three times the null points; 0.05 to 0.13 only after 4 time units of the solver. Its account sits in the wrong appendix (A). |
| 5 Fields for ROM or DA | Not answered as a use; partly as availability | No reduced-order model or assimilation; no ensemble is stationary (W16 +4.6 %, +6.3 %); the released W16 is worse than the released Gaussian laws. |
| 6 Context | Not answered; CONFIRMED | Symmetry and one diagnostic without uncertainty; 2.08 GiB. |
| 7 Deliverables | Study answered with its restriction, toolbox partly; CONFIRMED | 12 of 16 lines are above 100 floors; tests pass; the release does not reproduce the first rank. |

**Departures and detail still in the main text.** In `{#sec-origin}`, L566, L574, L578 and conclusion 7 ask why the network loses second moments, which no criterion asks. `{#sec-compute}` with `@fig-compute`, the origin of each hypothesis (L134), the catalogue detail closing L769 and the third paragraph of "Negative results" are detail without impact.

## Required corrections

1. **BLOCKING.** Move L1160 ("**Topology and the solver (H32, H35, H39).** … samples the stationary law.") unchanged back into `{#sec-origin}`, between L576 and L578, with a blank line on each side.
   - This makes L560, L630, L148 and L694 true again and returns `@fig-relax` to the main text.
   - L171: "The appendices hold what has no bearing on the requirements of the offer:" → "The appendices hold the detail of what the text summarises and what has no bearing on the requirements of the offer:".
2. **BLOCKING.** L562, four edits in the same paragraph:
   - "**A network anchored on a Gaussian law does not learn the non-Gaussian part (H28, H38, H40, H41).**" → "**In this budget, a network anchored on a Gaussian law with inter-mode covariance acquired no third-order part (H28, H38, H40, H41).**" W10, anchored on the mode-wise law, holds 0.31 and 0.24 of the reference; the H28 verdict reads "Not to be concluded: … anything about another network, budget, batch, optimiser or initialisation".
   - "The failure belongs to the construction and not to the data:" → "The failure belongs to the anchored construction, or to its optimisation in this budget and dimension, and says nothing about the data:" (verdict of H38; L1004).
   - After "more than $5\times 10^{-3}$ of the third-order production of the reference" add "on the seed means (0.023 in one seed)".
   - "(H41, not refuted)." → "(H41, not refuted); the anchors of H28, H38 and H40 are dense, and a fault specific to a dense covariance is not excluded."
3. L115: before the closing parenthesis of "(the same models retrained on CPU …)" add "; the released recoloured law is not the cited one and is farther from the reference than the released Gaussian laws".
4. First-page limits, asked under (iii) on 14 November and still open:
   - L97: "Reynolds number 10, one conditioning parameter" → "Reynolds number 10, a smooth flow, a magnetic Prandtl number of 0.6 to 1.7, one conditioning parameter".
   - L111: "($Rm$ from 6 to 17, in the saturated regime)" → "($Rm$ from 6 to 17 and a magnetic Prandtl number from 0.6 to 1.7, in the saturated regime of a smooth flow)".
5. L525: "…computed after the fact." → "…computed after the fact ($0.024 \pm 0.004$ higher for G2; a **conjecture** until registered, @sec-app-origin)." The number and its status are now only at L1002.
6. L576: after "third-order production" add "at the two lower held-out $\eta$"; after "not neutral for real states" add "at this sample size (the map is estimated on the snapshots it moves, fewer than dimensions)".
7. L913: "by 9 and 17 %, at the training values as at the held-out ones" → "by 9 and 17 % at the held-out values (the first by 8 to 13 % at the training values, H31)". H31 restarted G1 only (digest L3769).
8. L847: "Three results" → "Four results" (four are listed). At the first use of "the thresholds of the pilot" (L148, L855, L911) add "(@tbl-objectives)".
9. L710: "(3 tests, …)" → "(4 tests, with the Poincaré–Hopf balance of signs and the Kac-Rice factors)".
10. L1016: "against 8 for G1 and for W9, in every seed" → "against 8 for G1 in every seed and for W9 on the seed means (4 in one seed)" (digest L2572).
11. Explorer: "uses a coarser map and is farther" → "uses a coarser map, from moments that are not symmetrised under the sign symmetry, and is farther".

Open blocking points: 2

## Not checked

- Raw result JSON of H29 to H41: I used the register, the digest and the report tables only.
- The rendered HTML, the layout and figures of the PDF (text extraction only), and `check_gates.py`.
- The release assets (not downloaded again), the catalogue, and the cause of the W16 gap.
- The explorer beyond its two sentences on W16; `research/race-report.md`.
- The source entries for Berhanu, Nore, Bousquet and The Well, and Propositions 8 and 9 (confirmed in earlier reviews, not re-read).
- Tests marked slow, and the five skipped ones (PostgreSQL, S3, E2 data).
- Whether G0 was restarted at the training η in any job; I looked at H31 only.

Files:
- `/home/user/milady-2027/site/teams/claude/report/index.qmd`
- `/home/user/milady-2027/site/teams/claude/report/index.pdf`
- `/home/user/milady-2027/research/hypotheses.json`
- `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/jury3/diff_moves.out` (the sentence-level diff, outside the repository)
- `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/jury3/diff_moves.py` (its script)

## Follow-up of the main session

The eleven corrections were applied as written at commit 83c2d27: the paragraph "Topology and the solver (H32, H35, H39)", which had left the text with the paragraph that preceded it for want of a blank line, is back in the section on the origin of the non-Gaussian part; the summary of the anchored models says what the verdicts of H28, H38, H40 and H41 allow and no more; the limits of the first page name the smooth flow and the magnetic Prandtl number; the nine other points are corrected. The parts that the role lists as "departures and detail still in the main text" (three paragraphs on why the network loses second moments, the compute section, the origin of each hypothesis, the catalogue detail) are left in the text: the role did not ask to move them.

## Second answer: confirmation at 83c2d27

Both blocking points are closed, and the nine other corrections are applied as written. I checked with a sentence-level diff 8a97c22 → 83c2d27 of the report and the explorer page (2 tool calls, nothing edited, tree clean).

- **Blocking 1: closed.** "Topology and the solver (H32, H35, H39)" is back in `{#sec-origin}` at L578, between the H37 paragraph and "Two side tests", with a blank line on each side; it is on PDF p. 40. `@fig-relax` is cited from the main text again, and L560, the pointer of `{#sec-nulls}`, L148 and the comparative text are true again. The outline sentence is the one proposed.
- **Blocking 2: closed.** The four edits of L562 are in place, word for word.
- **Corrections 3 to 11: applied.** No other sentence of the report changed. There is no unresolved reference in the `.qmd` or the PDF (101 pages, regenerated in the commit).

Verdicts per criterion: unchanged for all seven; point E is now confirmed.

Not checked: `research/race-report.md` (two lines changed), the rendered HTML, the PDF layout.

Open blocking points: 0

## Follow-up of the main session (2)

The goal of the owner asks that the detail without bearing on the criteria of the offer go to an appendix or be summarised. The parts that the role had listed as detail still in the main text were therefore moved or summarised at commit 3087e8f (the compute section and its figure, the origin of each group of hypotheses, the descriptive result of H33, the paragraph of H31, the catalogue detail, the third paragraph of "Negative results", item 7 of the conclusion), and the role read that commit.

## Third answer: check of 3087e8f

No blocking point: the commit only moves text, nothing left the main text by accident, and no reference is broken (6 tool calls, nothing edited, tree clean).

- **Moves.** In the sentence-level diff 83c2d27 → 3087e8f, the only whole paragraphs that changed place are the Compute paragraph with its figure and the third paragraph of "Negative results"; ten sentences moved verbatim. `{#sec-origin}` holds the seven expected paragraphs in the expected order, and no two paragraphs are glued.
- **Numbers.** "At most 5.3 %" and "0.08 to 0.13" match the register (H33, H31) and the digest. "About half" holds on the raw files of `e4_surrogate` and `e4_surrogate_indep`: the model trained on Gaussian draws misses 0.06 to 0.10 of the dissipation, against 0.12 to 0.16 for the model trained on the data. The counts of (e) match the register statuses.
- **References.** None is unresolved in the `.qmd` or the PDF (103 pages, appendix A on p. 73).

My seven verdicts do not change. The detail left in the main text is short and announced: the "Two side tests" paragraph (L570) and the two history sentences closing `{#sec-remedy}`. I ask for no further move.

Corrections, none blocking:

1. L558: "has no deficit of magnetic energy" → "has no such deficit of magnetic energy". The model is 5.3 % low at η = 0.0725 (digest L4205), and the moved text says "no such deficit".
2. L1221: "The costs are in the section [Reproducibility](#reproducibility)." → "The costs are in @sec-costs."
3. L1237: "added five (" → "added four refutations and one dropped hypothesis (". The antecedent of "five" stayed in the main text.
4. The digest does not print the mean-flow part of the model trained on Gaussian draws, so "0.06 to 0.10" (L1004) has no source there. Add it in `experiments/e4_digest.py`.

Open blocking points: 0

## Follow-up of the main session (3)

Corrections 1 to 3 applied word for word at commit 172d7bd. Correction 4 was not needed: the table of H33 in the digest already gives the mean-flow part of the model trained on Gaussian draws (0.842, 1.06, 1.21 against 0.946, 1.14, 1.27 for the reference); the role accepted this.

## Fourth answer: confirmation of the final version at 172d7bd

The final version holds, with no blocking point (1 tool call, nothing edited, tree clean).

- **Corrections 1 to 3:** applied word for word (L558, L1221, L1237). No other sentence changed, no reference is unresolved, and the PDF is regenerated (103 pages).
- **Correction 4:** I accept your point and withdraw it; my search of the digest stopped before line 4198. The digest, unchanged since 3087e8f, gives 0.842, 1.06, 1.21 against 0.946, 1.14, 1.27 (line 4422: 0.862, 1.06, 1.20 against 0.94, 1.14, 1.27). That matches my recomputation from the raw files.

My seven verdicts per criterion stand for this version.

Open blocking points: 0

## Fifth answer: the race report at 346cee0

One blocking point. The offer section agrees with `@tbl-offer` and with my seven verdicts (5 tool calls, nothing edited).

Confirmed: the objectives table equals `race_metrics.py --all`; the counts hold (38 as 19, 17, 2; 103 pages; 36 files, 4.58 GiB); nothing over is presented as active.

Corrections:

1. **BLOCKING.** Polarity bullet: "…and carry no such dynamics." → "…, which fix at most the mean rate of sign changes (not computed), not the course or waiting times of a reversal." (report L640).
2. C5 cell: "no law is below 0.95" → "no law within 60 floors of the reference is below 0.95" (W6: 0.43).
3. H28 bullet: after "below 0.005 of the reference" add "on the seed means (0.023 in one seed)"; "(below 0.003 of the dissipation)" → "(seed means below 0.002, at most 0.005 in any seed)".
4. H33 bullet: "no deficit of magnetic energy (at most 5 %)" → "no such deficit of magnetic energy (at most 5.3 %)".
5. After "written before its run" add "(the checks of H35 and H36 were amended after a first invalid cycle)".
6. Conjectured: "30 or more inter-mode directions" → "30 or 300 inter-mode directions, or the full sample covariance".
7. Offer section: "the reference fields and the models are published in the format of the project" → "the reference fields are published in the format of the project, with the models".

Not checked: the state of the pods.

Open blocking points: 1

## Follow-up of the main session (4)

The seven corrections were applied word for word at commit 6be3362. The cost of the session is given in the race report by reference to `research/usage/latest.md`, which is rewritten at the last commit.

## Sixth answer: confirmation of the race report at 6be3362

The blocking point is closed: the polarity sentence is replaced, and the six other corrections are in place word for word (1 tool call, nothing edited).

The race report and the report now agree on the criteria of the offer.

Not blocking, and not in my list: "about 3 % of subsampling uncertainty" sits beside "4 and 10 %" in the same file.

Open blocking points: 0

## Follow-up of the main session (5)

The remaining remark was applied in the next commit: "about 3 % of subsampling uncertainty" is replaced by "the reference count on 400 snapshots differs by 4 to 10 % between two draws".
