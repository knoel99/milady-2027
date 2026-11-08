# Scenes ch01 — build report (batch 1, 2026-11-08)

Builder: scene-builder session, batch 1. No independent review pass (tight token budget; the launch prompt asked
to skip it). The builder looked at every still on both timings' reports and at mid-move frames of the draft.
**A reviewer pass is still owed** (SESSION-BRIEF §6 step 6).

## 0. Status

| Scene | Page | en: errors/warnings/QA | fr | det | draft fps |
|---|---|---|---|---|---|
| 01.1 | `01_1_no_magnet_inside.html` | 0/0/0 | 0/0/0 | ok | 47 |
| 01.2 | `01_2_lines_never_end.html` | 0/0/8 (false positive, §1) | 0/0/8 | ok | 49 |
| 01.3 | `01_3_the_squeal.html` | 0/0/0 | 0/0/0 | ok | 63 |
| 01.4 | `01_4_who_pays_the_bill.html` | 0/0/0 | 0/0/0 | ok | 58 |
| 01.5 | `01_5_which_way_is_up.html` | 0/0/0 | 0/0/0 | ok | 57 |
| 01.6 | `01_6_checkpoint_the_big_picture.html` | 0/0/0 | 0/0/0 | ok | 55 |
| ch01.Q | `01_Q_question.html` | 0/0/0 | 0/0/0 | ok | 50 |

Estimated length 3:04 (en), 3:27 (fr). Determinism: every sampled frame direct-identical; sequential = anti-aliasing.
Unit helpers: `ch01_kit.js` (`C1.dipoleLines`, `C1.heads`, `C1.earth`, `C1.churn`, label/fade helpers), `ch01.css`.

## 1. Deviations from the `visual` (the AS BUILT paragraphs in `script/ch01.json` hold the details)

- 01.1: flat cutaway, glyph question mark, closed-form churn (1400 particles); SCHEMATIC chip above the cutaway.
- 01.2: lines traced from a magnetic-charge model of the bar (not `Kit.fieldLines` with point dipoles: point dipoles
  inside the bar make singular lines). Counts 36/36 and 26/26 at the rests (computed). Layout QA reports 8 `overlap`
  items between the ∂V subscript of the formula's first line and its second line: checked on the still, the lines do
  not touch (KaTeX subscript box taller than its ink): false positive.
- 01.3: shots switch with 0.5 s fades, not T1 morphs; no ghost sketches under the PREDICT buttons; the slow curve
  does not reach its plateau inside the 14 drawn turns (it would plateau later; drawing it flat would overstate it).
- 01.4: closed-form token schedule; layout lifted for the two-line formula.
- 01.5: own PREDICT card (both answers light together), own mirror plane, emphasis by line width instead of dimming.
- 01.6: no polarity strip under the tiles.

## 2. Script fields changed

`visual` only (AS BUILT paragraph on every scene). No data file, no `deps` change. Narration untouched.

## 3. Findings for the writer

None contradicting the model or the data (all ch01 visuals are SCHEMATIC or sourced CONTEXT; numbers on screen come
from the script's params and formulas only).

## 4. Kit issues

1. `runtime/components/motifs.js`, `Kit.mirror` (mode `plane`): always draws its own B / −B arrows and the
   `S = diag(…)` label is on by default; a scene that needs only the reflecting plane (01.5 twins) must redraw it.
   Proposed fix: `arrows: false` option. Workaround: own plane in 01.5.
2. `runtime/components/cards.js`, `Kit.predictCard`: one `pick` only; 01.5's answer is "neither / both equally".
   Proposed fix: `pick: [0, 1]`. Workaround: own card in 01.5.
3. `runtime/components/field.js`, `Kit.fieldLines`: no helper for fields of finite magnets (point-dipole rows give
   singular lines inside the bar). Proposed: a `Kit.barField({x0, x1, yc, h})` charge-sheet model with through-magnet
   continuation (the 01.2 tracer is a candidate for promotion).
4. `runtime/components/kit.js`, `Kit.fitFormula`: 01.2's statement (P1 Prop. 3.8) was split after "= " leaving
   "0 for every closed surface ∂V" on line 2, and `__QA__` reports the ∂V subscript box overlapping line 2.
   Workaround: a `\quad` before `\text{for every…}` in the page's copy of the item. Proposed fix: prefer a split
   before a top-level `\text{}` that follows a relation.
