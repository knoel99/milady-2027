# Scenes ch03 — build report (batch 1, 2026-11-08)

Builder: scene-builder session, batch 1. No independent review pass (tight token budget; the launch prompt asked to
skip it). Every still looked at on the estimated timing, French timing checked by the report, mid-move frames of the
draft looked at. **A reviewer pass is still owed.**

## 0. Status

| Scene | en: errors/warnings/QA | fr | det | draft fps |
|---|---|---|---|---|
| 03.1 The induction equation | 0/0/1 (false positive, §1) | same | ok | 73 |
| 03.2 Conveyor belt | 0/0/0 | 0/0/0 | ok | 71 |
| 03.3 ABC flow | 0/0/0 | 0/0/0 | ok | 52 |
| 03.4 Once on, always on? | 0/0/0 | 0/0/0 | ok | 61 |
| 03.5 A panel of knobs | 0/0/0 | 0/0/0 | ok | 63 |
| 03.6 A handful of dots | 0/0/0 | 0/0/0 | ok | 64 |
| 03.7 The question of this film | 0/0/0 | 0/0/0 | ok | 67 |
| 03.8 Checkpoint | 0/0/0 | 0/0/0 | ok | 59 |
| ch03.Q | 0/0/0 | 0/0/0 | ok | 44 |

Estimated length 4:24 (en), 4:48 (fr). `make det U=ch03`: 0 DIFFERENT.
03.1's remaining QA item: `overlap: formula ∇ / formula B` between the two lines of its first formula item (a KaTeX
fraction's box touches the second line; on the still the glyphs do not touch).

## 1. Deviations (details in the AS BUILT paragraphs of `script/ch03.json`)

- 03.3: Canvas 2D orthographic projection instead of Three.js; no A/B/C letter pulses.
- 03.4: the PREDICT card becomes a one-line reminder (a shrunk card would fall under 28 px); the knob fades instead of
  morphing into the axis; no ghost sketches on the card; the legend fades at 'bench'.
- 03.5: the knob row moves up without shrinking (28 px floor); the dynamo region is a thin full-vermillion bar.
- 03.6: stacks narrowed to fit the 105 px gap between the dots at 0.34 and 0.41; no brace on that gap.
- 03.7: own violet dot cloud on card 1 (not Kit.cloud); cards lose their text when they go to the top row.
- Formula layer: in 03.1-03.6 every statement that does not fit two lines at 28 px is shown in two consecutive
  parts (same words, split at a `;`, `:\quad`, `\qquad` or arrow). See kit issue 2.

## 2. Script fields changed

`visual` (AS BUILT) on every scene. No data file, no `deps` change (03.4 reads e3_growth and e3_modes, 03.8 and
ch03.Q read e3_growth, as declared). Narration untouched.

## 3. Findings for the writer

1. 03.4: `data/e3_growth.json` names series[0] "s, 32³ (whole run)" while the visual (and R:1066) says it is fitted
   on the second half of each run; the page shows params.series as the legend, as asked. The extractor's label
   should be corrected (data owner).
2. Several onscreen.formulas are too long for the formula layer at 28 px (03.2 both, 03.3, 03.4, 03.5, 03.6): consider
   writing them with a `;` or `\quad` where a break reads well, or shortening them.

## 4. Kit issues

1. `runtime/components/equation.js`: the pen's `target` for a term needs the term element; `E.box(id)` returns a box
   only, so `__QA__` reports `pen-over-text` for a circle around its own term (03.1). Workaround: `data-qa="ignore"` on
   those pen paths. Proposed: `E.el(id)`, and `Kit.pen({ term: [E, id] })`.
2. `runtime/components/kit.js`, `Kit.fitFormula` / `Kit.formulaLayer`: no third line and no automatic paging for
   long statements; six ch03 items warned "does not fit in 716px even at 28px". Workaround: the page splits the
   statement into two consecutive items. Proposed: `formulaLayer({ page: true })` that pages a long item.
3. `runtime/components/motifs.js`, `Kit.knob`: no `value(t)` override and no way to restyle labels (03.5 needed glosses
   under each knob in the knob's group). Minor.
