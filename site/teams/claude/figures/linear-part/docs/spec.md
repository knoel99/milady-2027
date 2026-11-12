# Spec: linear-part
**Takeaway:** see brief.md. **Size:** 183 x 104 mm. Hero: none, a conceptual diagram (flat route, glyphs of one Fourier mode: 4 blue cells for u, 4 orange/red cells for B).
**Structure:** zoom from the principle (panel a: field = linear part + rest; network narrower than latent, neck drawn to scale 512/5320) to four controlled variants (panel b) on the same glyphs (green exact/learned affine, purple network), compared on one shared log axis.
Colour key (team): velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing grey (#6f6f6f). Extra roles in this figure only: network and "the rest" purple (#6A4C93); linear part / exact Gaussian field green (#00896A).

## Panels
| Panel | Job |
|---|---|
| a | v = linear part + rest; latent 5320 vs network width 512 (conjecture); measured loss 1.60-1.63 vs pi/2 and over-dispersion |
| b | G0, W9, W10, W11 as sums of glyphs; 2-seed CPU energy distance / floor on a log axis; what each gets right or wrong |

## Components (labels exact, all from FACTS.md "Why the first generators fail")
Latent bar 5320 (mode glyphs), network neck width 512, linear part A(t)x+b(t), the rest, loss ruler (pi/2 = 1.571; 1.60-1.63), W0-W6 band 177-519 (5 seeds, GPU), dots G0 3.3; W9 9.1, 10.6; W10 44.7, 46.3; W11 9.3, 7.6 (2 seeds, CPU); G0 residual 0.002, drift 0.21; W9/W11 nulls error 1.7, drift 0.12.

## Relations
Linear part -> neck (dashed, blocked, cross; conjecture); the rest -> through neck (solid).

## Conventions
Green = linear/exact Gaussian (solid = exact, dashed = learned); purple = network. Dots are values from FACTS.md; the loss ruler and axis are drawn to their stated numbers; widths of the two boxes in the decomposition are illustrative.

## Negative constraints
No pending 5-seed number; the width explanation is labelled "Conjecture".

## Render and gate (from the repository root)
`CHROME=<path of Chrome/Chromium, add --no-sandbox in a wrapper if running as root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/linear-part --fig site/teams/claude/figures/linear-part/figure/figure.js`
`node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/linear-part --fig site/teams/claude/figures/linear-part/figure/figure.js --out site/teams/claude/figures/linear-part/figure/out`
The engine is referenced in place (no copy): .claude/skills/schematic-figure/foundation/.
