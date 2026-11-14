single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/physicien.md`. No separate role process ran. Files read for this answer: `docs/specs/theory-brief.md` line 25, `docs/specs/notation.md`, `research/hypotheses.json` (H1, H2, and H3, none of which is Proposition 1), and `docs/specs/sources/literature.md` section 8. `experiments/results/digest.md` was not re-opened for this question.

All three items are conjectured.

Conjecture 1, highest. On a periodic grid, B = curl A has a divergence at roundoff for any smooth A. The identity is linear and does not depend on Re or Rm. One check, n = 16, seed 0, max absolute divergence 2.033691978340166e-12. Refutation criterion: the same construction at n = 16 with five seeds has a max absolute divergence above 1e-6 on any seed. Protocol: the Fourier script in a temporary directory, `--quick` is that one grid, then five seeds. Cost: seconds on CPU. This one grid does not meet the refutation threshold. It is not five seeds, so the conjecture stays open.

Conjecture 2. If the stream function is not constant on an impermeable wall, the normal velocity on that wall is the tangential derivative of the boundary value, so the image of C is not in the divergence-free space with the wall condition. Refutation criterion: on a 32² box, max |u·n| on the wall is below 1e-8 when psi is constant on the wall, and above 1e-2 when the boundary value is a sine of amplitude 1. Protocol: a 2D finite-difference check, one resolution first, then 32 and 64. Cost: under a minute on CPU. Not run.

Conjecture 3. A gauge change of A changes A and leaves B = curl A, and therefore leaves the support of the law of B, unchanged. Refutation criterion: two gauges of one periodic A on n = 16 satisfy |B1 − B2| / |B1| above 1e-6. Protocol: Coulomb residual versus an added gradient, one grid. Cost: seconds on CPU. Not run.

Test conjecture 1 first. The check is already cheap, and Proposition 1's magnetic example is that identity.
