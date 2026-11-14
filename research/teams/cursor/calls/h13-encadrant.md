single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H13, before any n = 96, cfl = 0.5 growth rate. The five-seed mean stays within 0.002 of the cfl = 1 mean 0.008095872179936526. Each point stays finite and its final max_div_b stays below 1e-8.

Protocol check. The control mean is the H9 result. The 0.002 tolerance is the one used at n = 64 in H8. No cfl = 0.5 point at n = 96 exists yet.

Verdict. UNCHECKED. The protocol can be run.
