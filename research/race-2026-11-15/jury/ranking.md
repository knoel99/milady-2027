# Jury ranking (absolute grades)

Eight teams graded; Team E is not graded (its file is empty). The ranking orders teams by scientific quality first, with compliance as the second consideration. Scale reminder: 30 is a small pilot with some supported results, 15 is preliminary runs with few supported claims, 5 is scaffolding.

| rank | team | scientific quality /100 | compliance /100 |
|---:|---|---:|---:|
| 1 | Team A | 31 | 57 |
| 2 | Team F | 30 | 53 |
| 3 | Team G | 26 | 40 |
| 4 | Team D | 23 | 43 |
| 5 | Team I | 18 | 43 |
| 6 | Team B | 17 | 40 |
| 7 | Team C | 10 | 24 |
| 8 | Team H | 3 | 5 |

## 1. Team A (31 / 57)

A small pilot with supported results. It is the only team with a nonlinear 3D incompressible MHD solver, a simple analytic benchmark, three training seeds per model, reference-versus-reference floors and committed operator and convergence tests, and every table number traces to a results file. It stays at the pilot level because the MHD box is 8³ with five modes per direction, the soft loss fails, the constraint results hold by construction, and the generated distributions and parameter response remain several times off the reference.

## 2. Team F (30 / 53)

Also a small pilot with supported results. It has a 2D MHD solver at 64², a Burgers benchmark, a PCA truncation floor, held-out and interpolation grids, significance tests and figures. It sits just under Team A because its comparisons are confounded: the raw baseline lives in a different representation, the physics-loss model was trained for 1600 steps against 3500, and its main positive claim about parameter response comes from one seed. The work is 2D with no sampling-time constraint measured.

## 3. Team G (26 / 40)

Between preliminary runs and a pilot. It has the best-trained single model of the race, a 7 M-parameter U-Net on forced 2D Kolmogorov flow up to Re about 600, and all three constraint routes under one protocol with numbers that match its metrics file. It is held down by a single seed, a temporally correlated split, a failed stream-function variant explained only by conjecture, and the absence of MHD, 3D, helicity and topology, which also costs it on compliance.

## 4. Team D (23 / 43)

Between preliminary runs and a pilot. It built a real parametric 2D MHD dataset and compared five divergence strategies with a noise floor and a held-out band, and its report states its limits bluntly. Every model is a 400-step, single-seed CPU run far from the floor, the solver validation is not evidenced, and there is no simple-benchmark stage, no 3D and no helicity.

## 5. Team I (18 / 43)

Slightly above preliminary runs; not delivered, graded on its repository. Three benchmarks, including 3D induction with helicity, and an exemplary separation of measured, published and conjectured. But the data are a handful of fields, the unconstrained MHD models have relative errors near 1, the 2D design route did not train, and the positive 3D result is one seed on four test fields.

## 6. Team B (17 / 40)

Preliminary runs with few supported claims. The spectral toolkit and identity checks are real, but the comparative table comes from 120 optimiser steps on 48 fields with one seed, in a parameter range where the field only decays. The report still has empty tables, cites a table and a study that were not produced, and gives two values for the same validation error.

## 7. Team C (10 / 24)

Between scaffolding and preliminary runs. Only a 2D evaluation on an under-fit model reached the repository; the 3D comparison at the centre of the report was trained but never evaluated, and the files cited for it are absent. The discussion concludes beyond what was measured.

## 8. Team H (3 / 5)

Scaffolding. Not delivered: untested package code and a decisions log, no run, no result, no report. Three incidents outside its control left it about twenty minutes of work.

## How close the calls are

- **A vs F (31 vs 30)** is the closest call and could go either way. F has more apparatus (floors, tests, figures, two grids); A has cleaner controls (equal budgets, three seeds everywhere) and a 3D nonlinear MHD system, at a far smaller resolution. I put A first because F's two main comparisons are confounded by representation and training length.
- **G vs D (26 vs 23)** is close. G's model is properly trained on turbulent data, but it never touches MHD; D addresses the subject's object (parametric MHD, topology metric) with models too under-trained to trust. On compliance D is ahead of G (43 vs 40). A judge who weighs the subject's MHD target more heavily could invert them.
- **I vs B (18 vs 17)** is a near tie. Both rest on barely trained models and a handful of test fields. I has three benchmarks, multi-seed Burgers and a consistent report; B has a better-validated toolkit and four routes on 16³ fields but an unfinished, inconsistent report. I did not deliver, which the framework scores separately.
- **The gaps F to G, D to I, B to C and C to H** are clear: each step loses either seeds and floors, or trained models, or the evaluation itself.
- All grades sit between 3 and 31 on science. None of the works reaches the level of a good internship report (45): the best are small pilots at toy resolution.
- I read every report and record in full and the code and result summaries that back the tables; the long raw JSON dumps and some code files were checked selectively against the reported numbers, not line by line.
