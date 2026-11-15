# Overall ranking of the eight graded teams

Team B is not graded (its provider refused every call). Grades are in `grades.json`; this ranking also weighs the
use of the budget and time, and each team's incidents.

| rank | team | scientific quality | compliance | delivered | LLM USD | GPU USD | hours |
|---:|---|---:|---:|---|---:|---:|---:|
| 1 | Team D | 7.5 | 7.5 | yes | 0.64 | 0.23 | 0.33 |
| 2 | Team H | 6.5 | 6.5 | yes | 0.28 | 0.00 | 1.15 |
| 3 | Team G | 6.0 | 5.5 | yes | 1.53 | 0.00 | 1.31 |
| 4 | Team F | 6.0 | 5.0 | yes | 4.35 | 0.54 | 1.04 |
| 5 | Team A | 5.0 | 5.5 | yes | 0.52 | 0.31 | 1.41 |
| 6 | Team C | 3.5 | 4.0 | yes | 2.33 | 1.13 | 1.36 |
| 7 | Team I | 4.5 | 4.5 | no | 4.80 | 0.00 | — |
| 8 | Team E | 1.5 | 1.0 | no | 3.18 | 0.00 | — |

**1. Team D.** The only study in which every claim is backed at the level a reviewer would ask for: three training
seeds per model, independent test sets, a reference-versus-reference floor on each metric, operator tests, a
convergence check and an intervention test of the parameter response, on an analytic heat benchmark and then on a
nonlinear 3D MHD system. Its negative results (the soft loss does not help on MHD, the parameter response is too
weak) are reported as plainly as the positive ones, and data, checkpoints and models are published. It is also the
cheapest and by far the fastest delivery. What keeps it from a higher grade is its own choice: an 8³ grid with a
handful of modes, no constraint-by-design arm, and seventy unused minutes.

**2. Team H.** A well-run CPU-only pilot on Burgers and 2D MHD with the right controls (truncation floor,
unseen-parameter grid, seeds, significance tests) and a decision log that shows real self-correction. Its sober
conclusion on the physics loss is credible. It stands below D because its two positive claims are weaker than they
are worded: the unconstrained baseline did not train, and the parameter-response gain rests on one seed and is
partly contradicted by its own interpolation numbers. It is 2D, and its generators remain far from the data.

**3. Team G.** The broadest clean comparison of the three constraint routes on real MHD fields (six strategies, own
2D solver, noise floor, held-out parameter band, topology count), delivered on CPU alone after a framework failure
removed its GPU and half an hour. Every number matches its result files and the report opens with its own caveat.
One seed and 400 training steps mean no ranking is established, there is no 3D and no separate simple benchmark,
and nothing was published.

**4. Team F.** The best-trained models of the race and firm, traceable numbers, but on 2D hydrodynamics only: no
magnetic field, no 3D, no helicity or topology, one seed, no held-out Reynolds number. Its exact-versus-soft
divergence result and its analysed failure of the stream-function model are solid. It ranks just below G because G
covers more of the subject under worse conditions, and because F used 4.35 USD of model calls for a narrower study.

**5. Team A.** It has the most relevant physics of the delivered teams, a validated 3D kinematic dynamo solver, and
measured all three constraint routes on 3D solenoidal fields. But a lost GPU pod and three re-scopes left a
22-second study of 120 training steps, the simple benchmark was never run, and the report went out unfinished, with
placeholders and a validation figure contradicted by its own table. The honesty of its limits section keeps it
ahead of the teams below.

**6. Team C.** A sound plan and real GPU work, undone by solver bugs found late and by a session cut outside its
control. What was measured is one small negative 2D table, itself questionable; the 3D comparison was trained and
never evaluated, and the result files the report cites are not in the repository. It delivered on time and within
budget and said what was missing, which places it above the two teams that did not deliver.

**7. Team I.** Its repository holds more checkable science than Team C's: an honest three-benchmark comparison whose
result files reproduce the report, with negative results stated as such. But the experiments are too small for most
models to learn, and the team spent 4.80 USD of model calls in 23 minutes and never delivered, mostly by its own
handling of context size. On substance alone it would stand sixth; on the use of its means it cannot.

**8. Team E.** Three incidents outside its control left it about twenty working minutes and no way to deliver, and
none of that is held against it. There is, however, nothing to grade but an unexecuted code skeleton, and its
benchmark generators prescribe the physics instead of simulating it.

## How close the calls are

First place is clear: Team D leads on both grades, on cost and on time. Second place is fairly safe but depends on
result tables of Team H that the repository lists and my extract did not show; if they held a surprise, H and G
would swap. G over F is the closest call among the delivered teams: equal scientific grade, F with stronger
evidence per claim, G with wider coverage of the subject, an outside incident and a third of the model spend; a
judge who weights statistical firmness over coverage would reverse them. A is separated from F and G by a full
point of scientific quality and from C by a point and a half. C over I is the other genuinely open call: I is one
point better on science and half a point better on compliance, and is placed below only because non-delivery and the
exhaustion of the budget were largely within its control; a ranking on the two grades alone would put I sixth.
Last place is not in doubt.
