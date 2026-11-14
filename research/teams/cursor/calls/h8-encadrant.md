single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H8, before any cfl = 0.5 growth rate. At n = 64 and Rm = 12, the five-seed mean at cfl = 0.5 stays within 0.002 of the cfl = 1 control mean 0.008127803049079646. Each cfl = 0.5 point stays finite and its final max_div_b stays below 1e-8.

Protocol check. The control mean is the H5 n = 64, Rm = 12, seeds 0-4 mean, already committed. The 0.002 bound was written before a cfl = 0.5 number existed. The cfl = 1 runs are the control. The cfl = 0.5 runs are the variant.

Verdict. UNCHECKED. The protocol can be run. No cfl = 0.5 point has been computed.
