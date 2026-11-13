single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H5 in `research/hypotheses.json`, registered before the GPU grid. The torch kinematic ABC growth rate (float64, t = 120, dt cap 0.05, CFL 1) matches the E3 digest signs at Rm 6, 12, 20 and 30 for n = 48 and n = 64, keeps final max_div_b below 1e-8, and at Rm = 12 the five seeds 0-4 stay positive at both resolutions with sample standard deviation below 0.005 and with five-seed means within 0.005 of each other.

Re-run. `python3 experiments/cursor_abc_growth.py --quick` (n = 16, t = 2, Rm = 12, seed 0, CPU) exited 0. The JSON line was lambda 0.23421565701123412, max_div_b 3.464642421029581e-16, cfl_dt0 0.04714045207910316, 44 steps. CONFIRMED that the script prints a finite rate and a divergence below 1e-8 on that smoke. REFUTED as evidence for H5: t = 2 is inside the transient (the fit starts at t = 1), and the grid in the claim was not run.

Trace. Digest signs used by the claim, `experiments/results/digest.md` E3 table: Rm 6 gamma -0.04598 (line 468), Rm 12 gamma 0.007653 (line 475), Rm 20 gamma -0.003185 (line 484), Rm 30 gamma 0.01043 (line 489). The N = 48 point at Rm 12 is 0.008124492445079803 (line 491). The absolute gap between the N = 32 and N = 48 rates at Rm 12 is about 0.00047, which is below the pre-set 0.005 tolerance. CONFIRMED that the sign list and the tolerance match the digest and were not fit to a GPU number. No GPU number for H5 exists.

Status. H5 is registered, verdict empty, results empty. The smoke is a script check, not a measurement of the claim. CONFIRMED as a pre-registered protocol. REFUTED if anyone quotes the smoke lambda as the dynamo rate.

Physics. The signs are the three windows of the ABC dynamo stated in `docs/specs/theory-brief.md` section 3 (growth rate changes sign near 8.9, 17.5 and 26-27). Rm 6 and 20 sit in decay windows, Rm 12 and 30 in growth windows, on the digest table. The word reversal is not used. CONFIRMED for that reading of the table. The torch solver uses another initial field than `induction3d.py`, so equality of the rates is not claimed.

Numerical protocol. CFL is requested at 1, under the RK4 note of about 2.8 in `cfl_dt`. The smoke's first CFL step was 0.047, so the cap was active. Five seeds are required at Rm = 12 for both resolutions before the mean comparison, and the 0.005 floor is written in the criterion. Divergence is an output of the script. Resolution is two grids, not a continuum limit. The GPU points, the five seeds, and t = 120 are UNCHECKED. Dynamic energy balance is not part of this kinematic claim.

Verdict. UNCHECKED. The protocol is specific enough to run, and the smoke does not support the claim.
