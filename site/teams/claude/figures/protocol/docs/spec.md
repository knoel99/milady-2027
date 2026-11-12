# Spec: protocol

**Takeaway:** A hypothesis is written with its refutation criterion before the computation; models are trained on 6 values of eta, chosen on 2 validation values and judged on 3 held-out values, over 5 seeds, against a noise floor measured on the reference itself.
**Size:** 183 mm x 101 mm, journal format, Arial 5.5-7 pt, panel letters 8 pt.
**Hero:** none, flow/protocol diagram of boxes, axes and set schematics; route flat (no 3D, no Blender, no illustrated finish needed).
**Structure:** controlled-comparison protocol: loop (a), splits on the eta axis (b), seeds (c), noise floor (d).

## Colour key (shared by the team)
velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing grey. Splits: training green (#009E73, circle), validation gold (#B39500, square), held-out test purple (#8E3FA8, diamond). Panels a-d are linked by the colour/shape key of the splits and by the measure 'energy distance / floor'.

## Source
Every label comes from `site/teams/claude/figures/FACTS.md`; no pending number is drawn. Dot and bar positions that are schematic are stated in the caption.

## Render and gate
Run from the repository root; the engine is referenced in place (`--root`), not copied. As root, Chrome needs `--no-sandbox`: set `CHROME` to a wrapper that adds it.
```
CHROME=<chrome-with---no-sandbox when root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/protocol --fig site/teams/claude/figures/protocol/figure/figure.js
CHROME=<chrome-with---no-sandbox when root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/protocol --fig site/teams/claude/figures/protocol/figure/figure.js --quick
node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/protocol --fig site/teams/claude/figures/protocol/figure/figure.js
```
Outputs: `figure/out/protocol.svg`, `.pdf`, `.png` (600 dpi). Last gate: green, no FAIL.

## Negative constraints
No number from FACTS.md marked pending; no claim beyond FACTS.md; no 3D.
