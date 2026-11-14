# Spec: mhd-dynamo-problem

**Assumptions:** mode=describe, style=own (clean flat, physics readers), route=flat, depth=full, web=off, width=183 mm.

**Takeaway (one sentence):** A helical force at k = 2 in a periodic box drives a flow that, above a threshold in Rm, sustains a magnetic field with a k = 1 part; the control parameter eta (11 values, Rm 6.25 to 16.7) changes the stationary state, and the generator must produce (u, B) snapshots at values of eta it never saw.
**Size:** 183 mm x 100 mm
**Hero:** none, a parametric-problem schematic (flat route, library primitives only; no 3D object to render)

**Structure:** a zoom from system to parameter: (a) the physical system, (b) the parameter axis with trends and the train/validation/test split, (c) the equations, (d) the task of the generative model at held-out eta.

## Colour key (shared by the sibling figures)

| Role | Colour |
|---|---|
| velocity u | blue `#0072B2` |
| magnetic field B (and H_M, null points) | vermillion `#D55E00` |
| forcing f | grey `#6E6E6E` |
| generated ensemble / what the model produces | green `#009E73` |
| reference (solver) ensemble | dark ink `#2B2B2B` |
| train / validation / held-out test glyphs (fig. mhd-dynamo-problem) | filled ink / grey fill with ink ring / hollow ring |

## Render and gate (from the repository root; Node >= 22 and a Chromium browser, set CHROME if needed, add --no-sandbox in a wrapper when running as root)

```bash
node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/mhd-dynamo-problem --fig site/teams/claude/figures/mhd-dynamo-problem/figure/figure.js
node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/mhd-dynamo-problem --fig site/teams/claude/figures/mhd-dynamo-problem/figure/figure.js --final
```

The engine is referenced in place (`.claude/skills/schematic-figure/foundation/`, `--root` option), not copied. Outputs: `figure/out/mhd-dynamo-problem.{svg,pdf,png}`.

## Negative constraints
- No number marked (pending) in FACTS.md; no value that is not in FACTS.md; trend lines and bars are qualitative (positions and heights illustrative).
- No claim about which generator is better.

## Panels
| Panel | Job |
|---|---|
| a | periodic box [0, 2π)³ with forcing helix (grey), flow helix (blue), large-scale B loop (vermillion) |
| b | η axis, 11 values, train/validation/test glyphs, trends of E_u, E_B, H_M (end values from FACTS.md, straight segment = direction only), Rm ≈ 5 threshold marked exploratory |
| c | the two equations and the solenoidal/helicity definitions, colour-coded; ν fixed |
| d | generative model, held-out η in, generated (green) vs reference (ink) snapshot pair out |
