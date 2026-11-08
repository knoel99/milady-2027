# Scenes ch08 — build report (batch 2, 2026-11-08)

Builder: scene-builder session of batch 2. No independent subagent review (the launch prompt forbade subagents and a
separate review pass); the builder looked at the stills of every scene on the estimated timing and the French check
report. **The independent review of CONTRACT §13.5.8 is still owed.** This unit was built last, under a tight budget:
it carries the most simplifications (see the AS BUILT paragraphs).

## 0. Status

| Scene | Page | Badge | Est. | FR | QA (non-formula) | Notes |
|---|---|---|---|---|---|---|
| 08.1 | 08_1_a_flat_sheet_of_plasma.html | MEASURED | ok | ok | 0 | |
| 08.2 | 08_2_does_clean_data_make_clean_outputs.html | MEASURED | ok | ok | 1 | strip tag over a dimmed map (intended) |
| 08.3 | 08_3_hill_maps_and_swirl_minus_slope.html | PROVED | ok | ok | 0 | formula split |
| 08.4 | 08_4_why_almost_is_not_exactly.html | PROVED | ok | ok | 0 | |
| 08.5 | 08_5_three_ways_to_fix_a_budget.html | MEASURED | ok | ok | 0 | formulas split, layer 900 px wide |
| 08.6 | 08_6_two_shelves.html | PROVED | ok | ok | 0 | |
| 08.7 | 08_7_the_proposed_machine.html | PLANNED | ok | ok | 0 | |
| ch08.Q | 08_Q_question.html | none | ok | ok | 0 | 1 card text-fit warning (writer) |

`make det U=ch08 TIMING=estimate`: exit 0. Draft `out/draft/unit_ch08_est/unit_ch08_draft.mp4` 5:06 (estimate);
capture 41–65 fps at draft size. The remaining formula-layer QA items are glyph overlaps inside one item (false
positives, ch05 kit issue 1).

## 1. Data added

`tools/data_ch08.py` (numpy) → `data/ch08_hillmap.json`: ψ and A of V4 sample 0 at η = 0.00951 by inverse Laplacian of
the stored vorticity and current of `data/e2_maps.json` (128² spectral display grid), and 12 low modes of the V0
sample-0 velocity rebuilt from its stored vorticity and divergence (swirl + slope), normalized. The script asked
for this block in `tools/data_existing.py` (read from the npz); builders may not edit it, and the npz-derived
`e2_maps.json` holds the same fields.

## 2. Per scene

As in the AS BUILT paragraphs of `script/ch08.json`. Script fields changed: `visual` (all scenes), `entry.params` of
08.2 (maps, gauge), 08.3 (map), 08.5 (lanes).

## 3. Findings for the writer

1. Formula-layer statements of 08.3 (gauge), 08.5 (loss, rescale and others) do not fit one item at 28 px; the pages
   split them into items shown in turn.
2. ch08.Q `unblocks` is 9 px too tall for the card at 28 px.
3. 08.5's read note says the ESS mean is 0.287 'computed by the scene': it is the mean over the 11 η of
   `en_loi.ess_frac_b` (the mean over the 5 test η alone is 0.22); the scene shows 0.29.

## 4. Kit issues

1. Shelves: `scenes/ch08/ch08_kit.js` is a copy of `scenes/ch07/ch07_kit.js` (units may not load each other's files).
   Promotion to `runtime/components/` (`Kit.shelves`) is needed before ch09 reuses it, or a third copy appears.
2. `Kit.chapterCard`: no explicit 'sidestep' (downward rail) option; 08.1 passes levelFrom L4, level L3.
3. `Kit.chip` with `anchor: 'tr'` and `maxWidth` near the right edge wraps to a narrow column (ch06 issue 2), again in 08.7.
4. `Kit.formulaLayer` fixed width (760): long statements need splitting in every page; an option to show a statement
   across two items, or a three-line fit, would remove the workarounds.
