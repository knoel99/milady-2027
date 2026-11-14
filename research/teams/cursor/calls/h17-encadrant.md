single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H17, before any n = 128, cfl = 0.5 growth rate. The five-seed mean of seeds 0-4 stays within 0.002 of 0.007691065668965582. Each point stays finite and its final max_div_b stays below 1e-8.

Protocol check. The control mean is the H12 result. The 0.002 tolerance is the one used at n = 64 in H8 and at n = 96 in H13. No cfl = 0.5 point at n = 128 exists yet.

Verdict. UNCHECKED. The protocol can be run.
