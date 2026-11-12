single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H5, after the sixteen GPU points in `experiments/results/cursor_abc/`. Seed-0 signs match the digest at Rm 6, 12, 20 and 30 for n = 48 and n = 64. Final max_div_b stays below 1e-8. At Rm = 12 the five seeds are positive, each sample standard deviation is below 0.005, and the five-seed means differ by less than 0.005.

Re-run. The GPU points were not started again. The aggregates were recomputed from the sixteen JSON files with `statistics.mean` and `statistics.stdev` (sample standard deviation, divisor n-1). n = 48, Rm = 12: mean 0.008040977512863952, std 0.0004973040443546106, all five positive. n = 64, Rm = 12: mean 0.008127803049079646, std 0.000667226918567827, all five positive. Absolute mean difference 8.682553621569382e-05. Largest max_div_b in the sixteen files is 9.331474506076454e-16. Seed-0 signs: n = 48 and n = 64 are negative, positive, negative, positive at Rm 6, 12, 20, 30. CONFIRMED that these files meet every numeric clause of the criterion. UNCHECKED as a second campaign.

Trace. Digest signs used as the target are in `experiments/results/digest.md` lines 468, 475, 484 and 489. The measured n = 48 seed-0 rate at Rm = 12 is 0.008813740207138356, next to the digest N = 48 value 0.008124492445079803 (line 491). The criterion did not require equality with that value. CONFIRMED that the sign list matches the table. The rate itself is a new measurement.

Status. Supported on the written criterion only. Not a generator comparison, and not five seeds at Rm 6, 20 or 30. Those Rm were specified as seed 0. CONFIRMED that the result text does not call this a 3D generator.

Numerical protocol. CFL 1 and dt cap 0.05 were the registered settings. Step counts are 7680 at n = 48 and 10800 at n = 64, so the CFL cap was active. Divergence was measured. Five seeds only at Rm = 12, as registered. Energy balance of the dynamic equations was not part of the claim.

Verdict. H5 is not refuted. The sixteen committed files meet the criterion. A second campaign was not run.
