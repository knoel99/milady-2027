# Scenes ch05 — build report (batch 2, 2026-11-08)

Builder: scene-builder session of batch 2. Token budget: no independent subagent review was run (the launch prompt
forbade subagents and a separate review pass); the builder looked at every still on both timings and at mid-move
frames of the draft. **The independent review of CONTRACT §13.5.8 is still owed.**

## 0. Status

| Scene | Page | Badge | Est. timing | FR timing | QA | Notes |
|---|---|---|---|---|---|---|
| 05.1 | 05_1_toll_counter.html | SCHEMATIC | ok | ok | 0 | |
| 05.2 | 05_2_rice_for_the_dipole.html | PROVED | ok | ok | 12 (false positives) | formula-layer glyph overlaps |
| 05.3 | 05_3_check_against_the_truth.html | MEASURED | ok | ok | 0 | |
| 05.4 | 05_4_crossings_not_reversals.html | PROVED | ok | ok | 0 | formula split (workaround) |
| 05.5 | 05_5_photographs_on_demand.html | none | ok | ok | 0 | |
| ch05.Q | 05_Q_question.html | none | ok | ok | 0 | 2 card text-fit warnings (writer) |

`make det U=ch05 TIMING=estimate`: exit 0 (direct seeks identical, sequential = anti-aliasing). Draft
`out/draft/unit_ch05_est/unit_ch05_draft.mp4` 2:49 (estimate); capture 50–68 fps at draft size.

## 1. Data added

- `tools/data_ch05.py` → `data/ch05_rice.json` (meta with SHA-256 of `experiences/resultats/e1_gissinger.json` and
  `video/data/e1_samples_0.93.json`). `strip`: Γ 0.93, h 0.2, coefficient 0.1, n_total 8000, n_in_strip 26, sorted
  strip indices, highlight = median |Ḋ| of the strip. `check`: cumulative errors 0.0437 (Γ 0.865–0.885, n 5) and
  0.0593 (Γ ≥ 0.89, n 23); the tool asserts round(100 ×) = 4 and 6 (R:883). The script's visual asked for
  `tools/data_existing.py`; builders may not edit it, so the block lives in the unit tool.
- The E1 sample archive `cache_e1/e1_echantillons_complet.npz` is not in the clone; the strip block reads the
  already-extracted `data/e1_samples_0.93.json` (same rows).

## 2. Per scene (as built; same text as the AS BUILT paragraphs of `script/ch05.json`)

See the AS BUILT paragraph of each scene's `visual`. Script fields changed: `visual` (AS BUILT, all scenes);
`entry.params` of 05.1 (`stack.y` 200), 05.2 (`plane.Ddot_range_signed` [−1.5, 1.5], `plane.speed_range` [0, 1.5]),
05.4 (`trace.box.y0/y1` 180/580, `trace.zero_y` 380). `deps` / `entry.data` of 05.2 and 05.3 already pointed to
`data/ch05_rice.json`.

## 3. Findings for the writer

1. **05.2 visual, y ranges**: the planned ±4 range for Ḋ hides the plane: 98 % of the stored Ḋ lie within
   [−0.85, 0.96] at Γ = 0.93. Built at ±1.5 (params changed, no narration impact).
2. **05.2 formula 1 and 05.4 formula**: too long for the formula layer at 28 px (the runtime warns). The pages split
   them at existing breaks without changing the text; a shorter statement, or explicit `;`/`\quad` breaks, would let
   the layer show them as one item.
3. **ch05.Q**: `why` (≈ 2 px over) and `unblocks` (≈ 9 px over) do not fit the card at 28 px: shorten each by a few words.

## 4. Kit issues

1. `runtime/components/hud.js` formula layer + `__QA__` (`kit.js` QA): the layer's own two-line items report
   `overlap` between KaTeX glyphs of the two lines (05.2 item 2: `\textstyle\sum_{i=1}^{N}` and the line below;
   `formula: N / formula: 0.2`). The still shows no visible collision (crop checked): false positives, 12 in 05.2.
   Proposed fix: skip glyph-vs-glyph overlap inside one formula-layer item, or add line spacing for tall operators.
2. `runtime/components/cards.js` `Kit.predictCard`: no way to show a question without option buttons (05.1's beat
   reads PREDICT and the question only); it warns "no options". Workaround: own `.c5-card` markup in the page.
3. `Kit.equation`: `E.box(id)` taken in `setup` for a term inside `\frac` (`width = \frac{1}{2h}`) returned a box
   that misplaced a pen underline through the denominator. Workaround: no pen on that term, labels at a fixed offset.
