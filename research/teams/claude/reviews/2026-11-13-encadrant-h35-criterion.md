# Review by the `encadrant` role: criterion and code of H35 before any full run

Date: 2026-11-13, 13:35–13:45 UTC, commit 1e00f23. Scope: the entry H35 of the register, `Context.relax` and group X of `experiments/e4_mhd3d.py`, `h35_lines` of `experiments/e4_digest.py`, the `--quick` outputs (a code test). No result exists yet. The role edits nothing; its report is copied below, and the follow-up of the main session is at the end.

**One blocking flaw in the control, two smaller fixes, three register amendments.** About 5 min of CPU used, 2 threads, nothing written in the repository.

## 1. Criterion against `h35_lines`: OK, with one FLAW

- OK: (a), (b), (c) are quantitative and decidable from group X. The code matches the register on the error definitions (per-seed mean over held-out η, then seeds), τ* (null ≤ 0.2 and mean |E_B/ref − 1| ≤ 0.05), (a) per η on seed means, and ties or two infinite values refuting (c).
- FLAW: `seed_mean` uses `nanmean` and nothing checks the number of seeds or the τ grid. The quick file (1 seed) already prints a verdict line.
- Fix: print "INCOMPLETE" unless seeds 0–4 all hold every `*X_tau{0,1,2,4,8}` and `REFX_tau{0,1,4}`.

## 2. Triviality and circularity: OK, with a wording FLAW

- (b) is not trivial: the diagnostic of the `physicien` role leaves G1 at 1.29 (τ = 2) and 1.06 (τ = 8), so τ = 4 sits near the 0.2 threshold.
- Only C5 can discriminate in (b), if W16 already meets the other four at τ = 0 as the earlier facts suggest; not checked in the digest.
- (c) has low power: a tie on the grid is likely and refutes. It may also be decided by the E_B condition (G1 at +10 % at τ = 2) rather than by null points.
- (b) is not circular: the relaxed model states are not in the reference. But τ → ∞ satisfies it for any law, so "supported" establishes only that τ = 4 suffices for five means.
- FLAW: "samples the stationary law" overstates this (amendment below).

## 3. Relaxation code: OK

- A copy of `Context.relax` (same `D.solver_config`, `D.DT`, `D.CFL`, float32 solver, float32 encoding) was run on 24 full-data snapshots at η = 0.0725 and 0.0331. It reproduces the stored snapshots at t + 2, 4, 8 to a relative L2 of 0.5–2.7e-6 (persistence baseline 0.27–0.72).
- Quick file: G0X, G1X, W9X and W16X at τ = 0 equal G0 (D), G1 (G), W9R and W16 (R) to all printed digits, at the 5 η.
- Consequence: REFX at τ = 4 is the stored snapshot at t + 4. It tests the code; only τ = 1 tests stationarity. The REFX energy distance is leaked and should not be quoted.

## 4. Checks of the measurement: FLAW in check (1)

- `pick` is sorted and `evaluate` counts nulls on `fh[:200]`, so the control always uses trajectories 0–9 of 24, for every seed.
- Measured on 300 snapshots per η: that block sits at −8 %, +2 %, +5 % of the mean, with a relative SE of 0.06, 0.04, 0.08. The 0.1 limit is therefore reachable by noise alone at η = 0.0725 and 0.0331.
- Fix: drop `np.sort` in group X. The expected seed-mean error is then about 0.03–0.04, which makes the 0.1 limit sound.
- E_B limit 0.03: OK (seed-mean deviation at most 0.017).
- Checks (2) and (3): limits OK, but they compare different seed sets. `e4_recolour` currently has W16 for seeds 0, 3, 4 only, and `e4_recolour_indep` does not exist, which gives INVALID. Fix: use the same five seeds on both sides.
- Reference null count: its SE over trajectories is 0.03–0.06, not the 0.025 of `null_count_se`. Two reference files of the same realisation give 44.11 and 42.73 at η = 0.0331. This error is common to all seeds.

## 5. Amendments to the register (dated 2026-11-13, before the full run)

- Replace the end of the "Supported" sentence with: "…meets the five thresholds of the pilot (means of five statistics; 512 states, 200 for the null count, 128 for the restart). It does not show that the relaxed ensemble samples the stationary law: the large-scale field decorrelates in 17 to 75 time units and comes from the generator."
- Add to (c): "A tie on the grid refutes (c) and is reported as 'not resolved by the grid', distinct from τ*(W16) > τ*(G1); the condition (null count or E_B) that sets each τ*, and τ* per seed, are reported."
- Add to the checks: "Null counts of the control use 200 snapshots drawn over all trajectories. Verdict only with seeds 0–4 complete; checks (2) and (3) on the same seeds. Noise floor: reference null count ±0.03 to 0.06 relative (between trajectories), common to all seeds. The control at τ = 4 reproduces stored snapshots and tests the code only."

Note only: use one reference file per realisation for all three jobs. The (a) limit of 0.6 was set after a diagnostic on the same η = 0.049.

Verdict: the criterion and the relaxation code are sound; do not launch the full run before the REFX sort fix, the five-seed guard and the three amendments.

## Follow-up of the main session (before any full run)

- Code: the draw of the control is no longer sorted; `h35_lines` prints INCOMPLETE unless the seeds 0 to 4 hold every law at every τ, compares the same seeds in the checks (2) and (3), reports which condition sets each τ*, τ* per seed, and a tie as "not resolved by the grid". `--quick` run again.
- Register: the three amendments, dated, with the original text kept (`amendments` of H35); no threshold of a clause changed. The two notes of the review are written in the reason of the amendment.
- The three jobs of a realisation run the same commit and the same number of restart samples, so their reference files are identical (the data are bit-identical between pods of this run: `assembly.json`).
