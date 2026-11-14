single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H25, before any Rm = 9.25 growth rate. At n = 64, cfl = 1, seeds 0-4, every lambda is positive, and every point stays finite with final max_div_b below 1e-8.

Protocol check. Rm = 9 has two negative seeds at this resolution. Rm = 9.5 is positive for seeds 0-4. No file matches n64_rm9.25. The sign is not already known. Five seeds are named. Divergence is part of the criterion.

Verdict. UNCHECKED. The protocol can be run when a parallel slot is free.
