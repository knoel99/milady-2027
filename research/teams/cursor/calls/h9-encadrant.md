single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H9, before any n = 96, Rm = 12 growth rate. The five-seed mean at cfl = 1 stays within 0.001 of the n = 64 control mean 0.008127803049079646. Each point stays finite and its final max_div_b stays below 1e-8.

Protocol check. The control mean is the H5 n = 64, Rm = 12, seeds 0-4 mean. The 0.001 bound is tighter than the H8 timestep bound and was written before an n = 96, Rm = 12 number existed. The n = 48 versus n = 64 gap of 8.68e-5 is the reason for that width. It is not an n = 96 result.

Verdict. UNCHECKED. The protocol can be run. No n = 96, Rm = 12 point has been computed.
