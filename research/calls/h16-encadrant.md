single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H16, before any growth rate for seeds 5-9. At n = 128, Rm = 12, cfl = 1, the mean of those five seeds stays within 0.001 of 0.007691065668965582. Each point stays finite and its final max_div_b stays below 1e-8.

Protocol check. The control mean is the H12 result. Seeds 5-9 do not exist yet. The 0.001 bound is wider than the H12 sample std of 0.000788 and was fixed before the run.

Verdict. UNCHECKED. The protocol can be run after H15 has a pod, or when a second slot is free.
