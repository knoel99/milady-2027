# Spec: metrics

**Assumptions:** mode=describe, style=own (clean flat, physics readers), route=flat, depth=full, web=off, width=183 mm.

**Takeaway (one sentence):** Seven metrics are computed on a generated ensemble against a reference ensemble at held-out eta, each in its own small panel with one glyph for generated (green) and one for reference (ink).
**Size:** 183 mm x 86 mm
**Hero:** none, a set of small metric panels (flat route, library primitives only; no 3D object to render)

**Structure:** small multiples on one template (controlled comparison): panel a is the key, panels b to h one metric each, same glyph pair everywhere.

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
node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/metrics --fig site/teams/claude/figures/metrics/figure/figure.js
node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/metrics --fig site/teams/claude/figures/metrics/figure/figure.js --final
```

The engine is referenced in place (`.claude/skills/schematic-figure/foundation/`, `--root` option), not copied. Outputs: `figure/out/metrics.{svg,pdf,png}`.

## Negative constraints
- No number marked (pending) in FACTS.md; no value that is not in FACTS.md; trend lines and bars are qualitative (positions and heights illustrative).
- No claim about which generator is better.

## Panels
| Panel | Metric (FACTS.md "Metrics") |
|---|---|
| a | key: generated, reference, colour key |
| b | energy distance / noise floor (floor = two reference subsamples) |
| c | relative divergence of B |
| d | mean energy balance: injection vs ν and η dissipations |
| e | shell spectrum E_B(k) (k = 1…8) and mean magnetic helicity H_M |
| f | magnetic null points (B = 0), mean count |
| g | restart drift over τ = 4, mean E_B |
| h | polarity symmetry B → −B, |P(⟨u·B⟩ > 0) − ½| |
