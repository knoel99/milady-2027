single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H24, before any Rm = 11 growth rate. At n = 64, cfl = 1, each seed 0-4 has lambda strictly between that seed's finished Rm = 10 and Rm = 12 values, and every point stays finite with final max_div_b below 1e-8.

Protocol check. The ten bounds were recomputed from the JSON files. Seed 0: Rm=10 0.004856755237684226 < lambda < Rm=12 0.00715725269647649. Seed 1: Rm=10 0.004424512451073159 < lambda < Rm=12 0.008144094832181672. Seed 2: Rm=10 0.005993760181833761 < lambda < Rm=12 0.009024448884006341. Seed 3: Rm=10 0.006179606623621823 < lambda < Rm=12 0.008284867491019794. Seed 4: Rm=10 0.00439954791290452 < lambda < Rm=12 0.008028351341713934. No file under experiments/results matches n64_rm11. The ordering is not already known. Divergence is part of the criterion. Five seeds are named. This is a kinematic sign-of-ordering check, not a 3D generator claim.

Verdict. UNCHECKED. The protocol can be run when a parallel slot is free and H23 is not waiting on the last slot.
