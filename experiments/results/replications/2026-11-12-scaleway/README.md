# Replication of E1–E3 on another machine (Scaleway, 12 November 2026)

**Question.** Do the five-seed results of PR #31 (`experiments/results/digest.md`, commit `6c1c03b`)
survive a change of machine, with the same code and the same seeds?

**Criterion, written before the comparison.** A verdict is reproduced if, under the protocol of the
thesis (§3.1: paired mean difference above two standard errors **and** the same sign in at least four
seeds out of five), it is retained in both runs or rejected in both runs. Numerical identity is not
required: a change of processor changes floating-point rounding.

This folder is a replication record. It does not replace the reference digest, and the site pages keep
citing `experiments/results/digest.md`.

## What ran where

| Part | Machine | Duration |
|---|---|---|
| E1 simulations, E2 data, E3 (step 1) | Scaleway BASIC2-A16C-32G (16 shared vCPU, nl-ams-1) | 52 min |
| E1 training and fine-tuning, seeds 0–4 (step 2) | same VM | ≈ 2 h 45 |
| E2 training, seeds 0–4 (step 2) | same VM | 9 300 s per seed (seeds 0–2), 8 100 s (seeds 3–4) |
| E1 evaluation over the five seeds (step 3), figures, digest | the reference container (4 cores), from the VM's model cache | 30 min |

The VM was stopped by its 6-hour guard during step 3; everything step 3 needs was archived and
recovered, then the VM was deleted. Reference run: about 2 300 s per E2 seed, so the shared-vCPU VM
was about four times slower per process. Launcher: `infra/deploy/scaleway.py`, run of commit `6c1c03b`.

Files: `digest.md` (output of `experiments/digest.py` on these results), the JSON results, the logs
(`logs/vm_status.txt` is the VM's status file). Model caches and sample files are not versioned.

## Bitwise checks

| Part | Result |
|---|---|
| E3 (all Rm, thresholds, N = 48 check) | identical to the reference up to ≈ 1e-14 relative; thresholds 8.87, 17.6, 26.8 |
| E1 simulations (data, reference statistics, Monte Carlo floors) | identical |
| E1 variants A, B, C, C_short, E, F0 | median relative difference ≈ 4e-7 (float32 rounding of the training); a handful of near-zero quantities (bridge mass, Rice rates built on few crossings) move by more than 1 %; the digest tables are unchanged at the printed precision, and the Rice table of model C on the fine grid is unchanged |
| E2 data | **different**: the metrics of the reference subsample, which depend on the data only, differ. Forced 2D MHD is chaotic, and the different rounding of the VM's processor changes the trajectories |
| E2 seeds 3 and 4 recomputed in the reference container (data regenerated there) | identical to the reference, field by field (705 numeric fields each) |
| E1 stationarity fine-tuning (F_stationarity_C, F_stationarity_Cshort) | **different**; the set of diverging seeds changes (below) |

So the pipeline is deterministic on a given machine type; across machines, E3 and the E1 simulations
reproduce exactly, the plain E1 training to float32 rounding, while E2 (chaotic data) and the E1 stationarity fine-tuning (unstable
optimization) reproduce only statistically.

## Verdicts

| Comparison | Reference (PR #31) | Replication | Verdict reproduced? |
|---|---|---|---|
| H1, E1: energy dist. A_reference − C_equivariant | 0.0104 ± 0.0012, 8.8 SE, 5 of 5 | identical | yes (retained) |
| H2, E1: Liouville deg 3, F0_control_C − F_stationarity_C | −0.0165 ± 0.0133, −1.2 SE, 2 of 5 | −0.562 ± 0.5, −1.1 SE, 2 of 5 | yes (rejected) |
| E1: Liouville deg ≤ 2, same pair | −0.0014 ± 0.011, −0.1 SE, 4 of 5 | −0.052 ± 0.044, −1.2 SE, 3 of 5 | yes (rejected) |
| E1: energy dist. F_stationarity_C − F0_control_C | 0.0011 ± 0.0012, 1.0 SE, 2 of 5 | 0.0065 ± 0.0039, 1.6 SE, 5 of 5 | yes (not retained), but the sign is now 5 of 5 |
| H3, E2: energy dist. V5_control − V5_potentials_stat | 1.50 ± 0.27, 5.6 SE, 5 of 5 | 1.43 ± 0.14, 10.3 SE, 5 of 5 | yes (retained) |
| E2: V2_final_projection − V3_projected_flow | 0.945 ± 0.063, 15.1 SE, 5 of 5 | 0.996 ± 0.063, 15.9 SE, 5 of 5 | yes (retained) |
| E2: V4_potentials − V3_projected_flow | 0.717 ± 0.234, 3.1 SE, 5 of 5 | 0.567 ± 0.164, 3.5 SE, 5 of 5 | yes (retained) |
| E3: thresholds | 8.87, 17.6, 26.8 | identical | yes |

Per test η (H3, control − V5):

| η | Reference | Replication | Verdict reproduced? |
|---|---|---|---|
| 0.00476 | −0.403 ± 0.334, −1.2 SE, 2 of 5 | −0.245 ± 0.214, −1.1 SE, 1 of 5 | yes (not retained) |
| 0.00673 | −0.149 ± 0.262, −0.6 SE, 2 of 5 | −0.241 ± 0.286, −0.8 SE, 3 of 5 | yes (not retained) |
| 0.00951 | 0.534 ± 0.296, 1.8 SE, 5 of 5 | 0.364 ± 0.155, 2.3 SE, 4 of 5 | **no**: not retained in the reference, retained here |
| 0.01345 | 2.42 ± 0.41, 6.0 SE, 5 of 5 | 2.28 ± 0.23, 10.0 SE, 5 of 5 | yes (retained) |
| 0.01903 | 5.13 ± 0.37, 13.9 SE, 5 of 5 | 5.02 ± 0.27, 18.6 SE, 5 of 5 | yes (retained) |

E2 energy distances over the test η (mean ± sd over five seeds), reference → replication: V0 4.37 ± 0.09
→ 4.47 ± 0.11; V1 5.62 ± 0.28 → 5.52 ± 0.48; V2 2.66 ± 0.08 → 2.74 ± 0.08; V3 1.72 ± 0.08 →
1.75 ± 0.07; V4 2.44 ± 0.52 → 2.31 ± 0.31; V5 0.93 ± 0.33 → 0.87 ± 0.33; V5 control 2.43 ± 0.52 →
2.30 ± 0.29. Every mean moves by less than about one seed standard deviation.

Diverging stationarity fine-tunings (σ(dE/dt) more than ten times the reference):
F_stationarity_C none → seed 4; F_stationarity_Cshort seeds 1, 2, 3, 4 → seeds 0, 2, 3.
The ratio of mean energy distances F_stationarity_C / F0_control_C goes from 1.41 to 3.34, driven by
the diverging seed 4.

Rice's formula on the fine grid (model F is F_stationarity_C, seed 0, which did not diverge in either
run):

| Distribution | Cumulative error near threshold | Cumulative error above | Max pointwise error above (Γ) |
|---|---|---|---|
| model C, reference → replication | 0.594 → 0.594 | 0.122 → 0.122 | 0.408 (0.895) → 0.408 (0.895) |
| model F, reference → replication | 0.406 → **0.688** | 0.168 → **0.587** | 0.528 (0.905) → **0.757 (0.945)** |

Spurious crossings of F below the threshold: at most 6.34e-04 (5.6 % of the rate at Γ = 1) →
2.66e-04 (2.4 %).

## Reading

- **All the headline verdicts (H1, H2, H3, V2 > V3, V4 > V3, E3 thresholds) are reproduced.**
- **One marginal verdict flips:** H3 at η = 0.00951 sits at the edge of the two-SE rule
  (1.8 SE then 2.3 SE). It should be reported as borderline, not as an established gain.
- **The stationarity fine-tuning is fragile across machines:** which seeds diverge depends on rounding.
  Statements about it should rest on the non-diverging seeds and say how many diverged, as the
  reference digest already does for C_short.
- **The Rice result for model F is not reproduced:** on the same seed, which converged in both runs,
  the error above the threshold goes from 0.168 to 0.587, so F goes from slightly worse than C (0.122)
  to much worse. Any statement that the stationarity fine-tuning keeps or improves Rice's prediction
  rests on one seed and one machine; it needs the five seeds before being quoted. Model C's Rice
  result is unchanged.
- **E2 is not bitwise reproducible across processors** because its data are chaotic trajectories;
  only its statistics are. A replication of E2 should regenerate and compare the data, not expect
  identical numbers.
