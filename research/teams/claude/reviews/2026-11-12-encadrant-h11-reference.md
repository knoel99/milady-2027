# encadrant, 2026-11-12 18:15 UTC — H11 and the E4 reference protocol

Scope: hypothesis H11 and the protocol of the E4 reference data (no model existed yet). Recomputed single-threaded from the raw snapshots `experiments/data_e4/eta_*.npz`, independently of `e4_mhd3d.py` (own mode list, Craya basis and shells). Condensed by the main session from the role's answer; nothing was edited by the role.

| Claim | Verdict | Recomputed |
|---|---|---|
| 1. H11 as registered (H(1) < 0, Σ_{k≥2} H > 0 by 2 SE, E_B(1)/E_B in [0.2, 0.8] at the 11 η) | REFUTED (the main session's reading stands) | H(1) < 0 at 11 of 11 η (z −19 to −58); Σ_{k≥2} H > 0 by 2 SE at 8 of 11 (z = −1.4 at η = 0.0365, −1.2 at 0.03309, −5.5 at 0.03); E_B(1)/E_B in [0.370, 0.438]. Shell k = 2 is negative at every η (12 to 39 SE), Σ_{k≥3} H positive at every η: the sign change sits at \|m\| ≈ 2.4. "Negative for k ≤ 2, positive for k ≥ 3" is a post hoc reading and needs its own hypothesis. |
| 2. E[⟨j·B⟩] = 0 in the reference | CONFIRMED | z from −0.45 to +1.66, pooled z 1.65; cancellation between k ≤ 2 (negative) and k ≥ 3 (positive, peak at k = 4, shells 4–6 carry 79 to 86 % of the positive part). |
| 3. Energy balance closes, H_M stationary | CONFIRMED | max \|residual\| 3.96e-4; H_M drift max \|z\| 1.81. Qualifications: z = −2.07 at η = 0.07253; the residual equals the energy change over the kept window. |
| 4. Noise-floor protocol of C1 | Correctly coded, REFUTED as "a perfect generator gives 1" | The trajectory-split floor is 3 to 7 times the random-split floor; a perfect generator would score about 0.6 (extrapolation); sd over splits 26 to 99 % of the mean; weighted samples are penalized by the V statistic (+12 to +45 % of the n = 256 floor at ESS/N = 0.41). |
| 5. Null-point finder | CONFIRMED | positive = negative on 8 snapshots at 48³ and 64³ (two η); 73 Newton starts give the same counts. |

Missing in the protocol at that time: resolution and time-step convergence of the data (done afterwards: digest, "E4 - convergence"). Remarks applied: the C1 note of `race/teams/claude/objectives.toml`, the floors table of the digest (`experiments/e4_floor.py`), the H11 register entry.
