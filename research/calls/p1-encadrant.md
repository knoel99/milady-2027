single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. Proposition 1 (C1 by construction) in `docs/specs/theory-brief.md`, line 25. If the decoder is x = C(z) with the image of C inside S, then q(S) = 1 for any law of z. In a bounded domain, C must also respect the boundary conditions.

Re-run. The claim is a statement, not a script in `experiments/`. A periodic Fourier check was run in this session, outside the repository, on a 16³ grid, seed 0. The curl of a random vector potential had max absolute divergence 2.033691978340166e-12. The same field plus a gradient had max absolute divergence 21101.848169129164. CONFIRMED for that periodic identity on that one grid. The MHD solver in `src/milady/sim/mhd3d.py` was not run for this claim. UNCHECKED for the solver.

Trace. No E1 to E3 number is used as proof. The statement matches `docs/specs/theory-brief.md` line 25. `docs/specs/notation.md` defines the stream function, the vector potential, and q as the generated law. It does not define the symbol S. CONFIRMED that the sentence matches the brief. UNCHECKED against a definition of S outside that sentence.

Status. The first sentence is the definition of the support of a pushforward, and the brief gives no proof block. It is not a measurement. Calling the examples a property of this repository's solver would be a wrong status. CONFIRMED as an unproved elementary statement. REFUTED as a measured solver result, because no solver output was produced.

Physics. For a smooth vector potential, the divergence of a curl is zero. The second sentence correctly adds boundary conditions instead of deriving them from the first sentence. The word reversal is not used. CONFIRMED.

Numerical protocol. This is not a simulation campaign. The Fourier check has one grid and one seed, and it is periodic. It does not settle a wall, a gauge, or the solver. Those missing checks are UNCHECKED, not a refutation of the pushforward sentence.

Verdict. CONFIRMED for the pushforward sentence as written. The periodic curl example holds on the one grid above. The solver and the bounded-domain example are UNCHECKED.
