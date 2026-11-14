# Spec: generative-pipeline
Hero: none, a schematic of glyphs and labels; route flat (no 3D object to render). Style: own, clean flat, physics readers. Width 183 mm, journal format, labels 5-7.5 pt.
Colour key (shared by the team's figures): velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing f grey (#8c8c8c); neutral ink for generic objects.
Source of every element: site/teams/claude/figures/FACTS.md only; no number marked pending is drawn.
Render: `CHROME=<chrome wrapper adding --no-sandbox if root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/generative-pipeline --fig site/teams/claude/figures/generative-pipeline/figure/figure.js` (add `--crop` etc. as needed; engine = the skill's foundation, no copy).
Gate: `node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/generative-pipeline --fig site/teams/claude/figures/generative-pipeline/figure/figure.js --out site/teams/claude/figures/generative-pipeline/figure/out`
(as root, Chrome needs a wrapper script that execs google-chrome with --no-sandbox, passed through the CHROME environment variable.)

## Structure
Skeleton: pipeline, left to right (six stages, one arrow between each), because the claim is a chain of representations. Stage glyphs: two grids (u blue behind, B orange front); 11x11 mode lattice (a 2D slice, illustrative); a plane with e1, e2 and k (u and B planes); noise cloud to data with straight paths, x_t and its velocity, network box v_theta(x,t,c); one trajectory in steps; closed B field lines. A bracket marks the generated representation (stages 3-5); an orange tag marks the result: every sample has div B = 0.
Concepts considered: (a) pipeline with the constraint tag (kept); (b) two-row figure with a zoom on the decoding. (a) reads in 5 s and fits one row; (b) wasted space. Only (a) drawn.
## Negative constraints
No claim that generated samples match the reference law or conserve quadratic budgets (the user's wording "quadratic budgets are those of the solver" is not in FACTS.md, so not drawn). No result numbers. The lattice, clouds and field lines are illustrative, not data.
## Labels
Snapshots (u, B); 16^3 grid; Fourier modes; |m_i| <= 5; 665 complex modes; Vector potentials; Craya-Herring basis; latent: 5320 reals; Conditional flow matching; noise -> data, straight paths; conditioned on log eta; Sampling; Decoding; B = curl A (u alike); div B = 0; "every sample: div B = 0".
