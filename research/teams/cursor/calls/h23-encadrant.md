single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H23, before any Rm = 9.5 growth rate. At n = 64, seeds 0-4, every lambda is positive, and every point stays finite with final max_div_b below 1e-8.

Protocol check. lambda(9) was negative for two seeds at this resolution. lambda(10) is positive for all five. Rm = 9.5 has no point yet. The positive sign was fixed before the run and is allowed to fail.

Verdict. UNCHECKED. The protocol can be run when a parallel slot is free.
