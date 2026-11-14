# Review by `jury-externe` — commit 8184bc9: schematics and diagrams of the deliverables

Due review named by `tools/review_due.py` ("milestone changed", path `site/teams`). Role `jury-externe` (sub-agent, model and effort of the role file), 2026-11-12/13. A first run was cut by a restart of the container; the second reached its turn limit and delivered the report below when asked (PNGs seen at overview size only: fine legibility not checked). Paths relative to the repository root.

**Outcome: 2 ACCEPT, 8 CORRECT, 1 REDRAW (panel b of `linear-part`).** The 5-seed aggregates were recomputed from `experiments/results/replications/e4_gpu/`.

## Verdict per item

1. **mhd-dynamo-problem — ACCEPT.** Energies, H_M, Rm and the split match `experiments/results/e4_reference.json` and `experiments/e4_data.py:48-51`. Equations not compared with the solver.
2. **generative-pipeline — ACCEPT.** 665 and 5320 match the config keys `modes`, `dim_potentials`. Encoding in `train/data.py` not read.
3. **constraint-mechanisms — CORRECT.** W0 is under "Training loss"; REGISTRY says `components` = design, unconstrained baseline (`src/milady/train/constraints.py:80`). G0 is under "Model design"; REGISTRY says `gaussian_modes` = model (`:89`). W6 (`:87`) is missing. W3 is not sampling-only: its own network is trained with projected noise (`experiments/e4_mhd3d.py:504-506`). W7 is drawn with spread weights; the measured `ess_frac` is 1/256 in 14 of 15 held-out cells.
4. **stationarity-identities — CORRECT.** Equations match `stationarity_residuals` (`constraints.py:339-344`); 0.29 → 0.19 confirmed. "Below 4×10⁻⁴" holds for the CPU reference (3.96e-4), not for the GPU reference (4.15e-4 at η = 0.06575). Panel b is a post hoc reading: H11 was REFUTED as registered; the k = 2 bar equals k = 1, in `J_shell` it is 3 to 16 times smaller. Panel c omits that W7 collapsed (H8 dropped).
5. **metrics — CORRECT.** The drift bracket spans reference level to generated end; the code measures the generated ensemble's own change (`e4_mhd3d.py:266-267`). "Noise floor = 1": the floor is a mean of 10 splits (`:187-193`) with a standard deviation of 26–99 % of it; a perfect generator scores about 0.6.
6. **protocol — CORRECT (minor).** Split, 24 × 100 and 512 confirmed. The floor is a mean of 10 splits, not one; seeds are 0–4; `experiments/results/e4_selection.json` selects on seeds 0 and 1.
7. **linear-part — REDRAW panel b, CORRECT panel a.** A ranking is quoted on 2 seeds (rule 4); H16–H21 have no verdict. W11 (9.3, 7.6) is in no committed file. "W0–W6: 1.60–1.63" holds for W0, W4, W4s, W5_control only (W1 1.97–1.99, W5 1.70, W3 1.26–1.27, W6 0.84–0.85). "2–3× too many nulls": W1 has 0.30× and W6 0.64× the reference count. W0–W3 are 7980-dimensional, not 5320. The W10 explanation is hypothesis H20, drawn as fact. G0 "3.3×" against W9/W11 "error 1.7" (= 2.7×): use one unit. CPU dots and GPU band use different reference realisations. Tick "1" hidden by the dashed line.
8. **compute-path — CORRECT (minor).** 83 min, 1.02 USD and 35–60 s confirmed. "4–5 ms" merges two GPUs and two dtypes. The committed `experiments/results/digest.md` has no E4 section.
9. **agent-organisation — CORRECT.** Tiers and efforts confirmed. `make test` is pytest only; ruff and the agents sync are separate CI steps. The ledger has start, end and correction rows, not one row per job. The Sonnet workers that drew the figures are absent.
10. **code-architecture — CORRECT, partly NOT CHECKED.** The "model design" box holds `FourierComponentSpace`, the unconstrained baseline. W11, G0, W4s, W7, W8 are unlabelled.
11. **experiment-workflow — CORRECT, partly NOT CHECKED.** `e4_floor.py` reads the data through `Context`, not `e4_reference.json`. Verdicts come from `encadrant`, not from `race_metrics.py`: that step is missing. "Pod deleted in every case" contradicts two orphaned jobs.

## Three most serious problems

1. `linear-part` panel b quotes a ranking on 2 seeds, for hypotheses without a verdict, with W11 absent from the commit.
2. Statements about "W0–W6" are false for W1, W3, W5 and W6 (loss, nulls, dimension); W7 and the H11 reading appear without their negative verdicts.
3. Definitions are drawn otherwise than coded (W0/G0 columns, drift bracket, sharp floor). Captions cite FACTS.md instead of result files.

Not checked: `src/milady/eval/topology.py`, `src/milady/sim/mhd3d.py`.

## What the main session did with it

The fact sheet `site/teams/claude/figures/FACTS.md` and the text of the report were corrected on the points of items 4, 7 and 8 (loss values and null counts stated per variant, dimensions, H11 and H8 with their verdicts); every figure marked CORRECT or REDRAW is redrawn by a worker with the list above (journal of 2026-11-13).
