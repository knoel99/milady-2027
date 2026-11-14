# Spec: compute-path

**Takeaway:** The session has no GPU: each GPU job is a rented pod that clones a pushed commit, runs under a time limit, returns its outputs and is deleted, with its cost written to a ledger.
**Size:** 183 mm x 100 mm, journal format, Arial 5.5-7 pt, panel letters 8 pt.
**Hero:** none, flow/protocol diagram of boxes, axes and set schematics; route flat (no 3D, no Blender, no illustrated finish needed).
**Structure:** pipeline (a) with the five failures attached to the arrow or box where they occurred, the failure list (b) and measured costs (c).

## Colour key (shared by the team)
velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing grey. Splits: training green (#009E73, circle), validation gold (#B39500, square), held-out test purple (#8E3FA8, diamond). Failure badges (dark red, used only for failures) are numbered as in panel b.

## Source
Every label comes from `site/teams/claude/figures/FACTS.md`; no pending number is drawn. Dot and bar positions that are schematic are stated in the caption.

## Render and gate
Run from the repository root; the engine is referenced in place (`--root`), not copied. As root, Chrome needs `--no-sandbox`: set `CHROME` to a wrapper that adds it.
```
CHROME=<chrome-with---no-sandbox when root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/compute-path --fig site/teams/claude/figures/compute-path/figure/figure.js
CHROME=<chrome-with---no-sandbox when root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/compute-path --fig site/teams/claude/figures/compute-path/figure/figure.js --quick
node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/compute-path --fig site/teams/claude/figures/compute-path/figure/figure.js
```
Outputs: `figure/out/compute-path.svg`, `.pdf`, `.png` (600 dpi). Last gate: green, no FAIL.

## Negative constraints
No number from FACTS.md marked pending; no claim beyond FACTS.md; no 3D.
