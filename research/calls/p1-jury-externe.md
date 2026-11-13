single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran. Scope is Proposition 1 only. The rest of `docs/specs/theory-brief.md` was not examined. There is no separate supervisor verdict. The encadrant text in `research/calls/p1-encadrant.md` is the same session, not an independent review.

| Claim | Location | Verdict | Evidence | Required change |
|---|---|---|---|---|
| If x = C(z) and the image of C lies in S, then q(S) = 1 for any law of z | `docs/specs/theory-brief.md` line 25, first sentence | CONFIRMED | The sentence is the definition of the support of a pushforward, provided q is the law of C(z) and S is measurable. The brief has no proof block. | Add the one-line argument and state those two hypotheses. |
| The examples u = curl-perp psi and B = curl A put the fields in that set | same line | TO BE SPECIFIED | Periodic Fourier check, n = 16, seed 0, max absolute divergence of curl A is 2.033691978340166e-12. One grid, not the solver, not a wall. `docs/specs/notation.md` defines the potentials and does not define S. | Check the solver's discrete curl, and a wall, before citing the examples as properties of this code. |
| In a bounded domain, C must also match the boundary conditions | same line, second sentence | CONFIRMED | The sentence states an extra requirement. It does not claim the first sentence implies the boundary condition. | Give one worked boundary condition with the function space. |

Pre-defence note, Proposition 1 only.

The strength is that the first sentence does not depend on the training loss. A decoder whose image lies in S cannot place mass outside S.

The weakness is that the examples are not tied to a function space, a gauge, or a test in this repository. Section 8 of `docs/specs/sources/literature.md` already treats the 3D vector-potential generator as an open gap. That gap does not refute the first sentence.

Changes required before this one claim is defended.

1. Write the pushforward argument and the measurability hypothesis.
2. State the space S for a periodic box and for a wall, including the gauge of A.
3. Show the identity on the solver that the project will actually run, on more than one grid.

Unverified here. Propositions 2 through 9, the E1 to E3 numbers, and every literature page not already tagged in `docs/specs/sources/literature.md`.
