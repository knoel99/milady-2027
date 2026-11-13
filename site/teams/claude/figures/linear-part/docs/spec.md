# Spec: linear-part
**Takeaway:** see brief.md. **Size:** 183 x 104 mm. Hero: none, a conceptual diagram (flat route, glyphs of one Fourier mode: 4 blue cells for u, 4 orange/red cells for B).
**Structure:** zoom from the principle (panel a: field = linear part + rest; network narrower than latent, neck drawn to scale 512/5320) to four controlled variants (panel b) on the same glyphs (green exact/learned affine, purple network), compared on one shared log axis.
Colour key (team): velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing grey (#6f6f6f). Extra roles in this figure only: network and "the rest" purple (#6A4C93); linear part / exact Gaussian field green (#00896A).

## Panels
| Panel | Job |
|---|---|
| a | v = linear part + rest; latent 5320 vs network width 512 (conjecture); measured loss of W0, W4, W4s 1.60-1.63 vs pi/2; latent 5320 (potentials) / 7980 (free components); width statement is a conjecture (H21) |
| b | G0, G1, W9, W10, W11 as sums of glyphs; 5-seed mean energy distance / floor on a log axis (W4s 210, W10 43.6, W9 9.3, W11 8.6, G0 3.5, G1 2.6) with null-count error and restart drift table |

## Components (labels exact, all from FACTS.md "Why the first generators fail")
Latent bar 5320 (potentials; 7980 for W0), network neck width 512, linear part A(t)x+b(t), the rest, loss ruler (pi/2 = 1.571; 1.60-1.63), log axis 1-300 with W4s 210, W10 43.6, W9 9.3, W11 8.6, G0 3.5, G1 2.6; table null-count error / restart drift (W4s 1.83/0.38, W10 2.46/0.12, W9 1.67/0.12, W11 1.70/0.12, G0 2.24/0.21, G1 1.10/0.06).

## Relations
Linear part -> neck (dashed, blocked, cross; conjecture); the rest -> through neck (solid).

## Conventions
Green = linear/exact Gaussian (solid = exact, dashed = learned); purple = network. Dots are values from FACTS.md; the loss ruler and axis are drawn to their stated numbers; widths of the two boxes in the decomposition are illustrative.

## Negative constraints
No verdicts, no 2-seed or CPU numbers; the width explanation is labelled "Conjecture (tested by a width scan, H21)".

## Render and gate (from the repository root)
`CHROME=<path of Chrome/Chromium, add --no-sandbox in a wrapper if running as root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/linear-part --fig site/teams/claude/figures/linear-part/figure/figure.js`
`node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/linear-part --fig site/teams/claude/figures/linear-part/figure/figure.js --out site/teams/claude/figures/linear-part/figure/out`
The engine is referenced in place (no copy): .claude/skills/schematic-figure/foundation/.
