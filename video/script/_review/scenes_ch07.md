# Scenes ch07 — build report (batch 2, 2026-11-08)

Builder: scene-builder session of batch 2. No independent subagent review (the launch prompt forbade subagents and a
separate review pass); the builder looked at every still on the estimated timing and the French check report.
**The independent review of CONTRACT §13.5.8 is still owed.**

## 0. Status

| Scene | Page | Badge | Est. | FR | QA (non-formula) | Notes |
|---|---|---|---|---|---|---|
| 07.1 | 07_1_lopsided_machine.html | MEASURED | ok | ok | 0 | formula split (workaround) |
| 07.2 | 07_2_mirror_test.html | PROVED | ok | ok | 0 | formula 2 split; 12 formula-glyph QA false positives |
| 07.3 | 07_3_only_where_the_data_are.html | MEASURED | ok | ok | 0 | 8 formula-glyph QA false positives |
| 07.4 | 07_4_budget_blind_to_mirror.html | PROVED | ok | ok | 0 | |
| 07.5 | 07_5_balance_every_snapshot.html | PROVED | ok | ok | 0 | formula in three clauses |
| 07.6 | 07_6_two_juries.html | PROVED | ok | ok | 0 | pen workaround |
| ch07.Q | 07_Q_question.html | none | ok | ok | 0 | 2 card text-fit warnings (writer) |

`make det U=ch07 TIMING=estimate`: exit 0. Draft `out/draft/unit_ch07_est/unit_ch07_draft.mp4` 4:11 (estimate);
capture 49–66 fps at draft size.

## 1. Data added

`tools/data_ch07.py` → `data/ch07_mirror.json` (ref_sym_085, runs, asym, check3) and `data/ch07_spike.json`
(distance, spread, also_worse, juries). Sources: `experiences/resultats/e1_gissinger.json` (donnees, resume, config),
`video/data/e1_samples_0.85.json` (the stored reference rows; the full archive `cache_e1/…npz` is not in the clone),
`video/data/e1_eval.json` (per-Γ asymmetry, noise floors). Checks in the tool: 6 and 5 of 16 runs up (P(D>0)_train ×
16 integral), energy-distance ratio rounds to 9. Values match the script's spec (0.183, 0.0854, 0.0825; B 0.003–0.006 /
0.007–0.025, mean 0.016; check3 0.0167 / 0.0223 / 0.0217, floor 0.0078; distances 0.00257 / 0.0231, floor 0.00123;
spread 4.17 × 10⁻¹⁷). One difference: C's asymmetry range in e1_eval is 0.0037–0.0049, the report prints 0.0048; the
scene shows only 'about 0.004'.

## 2. Per scene

As in the AS BUILT paragraphs of `script/ch07.json`. Script fields changed: `visual` (all scenes), `entry.params` of
07.1 (panels y1, balance), 07.2 (cards y), 07.3 (plot box).

## 3. Findings for the writer

1. **Formula layer**: the formulas of 07.1, 07.2 (item 2) and 07.5 do not fit one layer item at 28 px; the pages split
   them at existing breaks into items shown in turn. Shorter statements or `;` breaks would remove the workarounds.
2. **ch07.Q**: `why` and `unblocks` are too long for the card at 28 px (by 35 and 44 px).
3. **07.5 'the half per cent beyond the range'**: kept the axis at ±1.6 as specified; values beyond are not drawn.

## 4. Kit issues

1. **Shelves**: the device is in `scenes/ch07/ch07_kit.js` (`C7.shelves`, `C7.balance`, `C7.panel`); ch08 and ch09
   reuse it, so promotion to `runtime/components/` as `Kit.shelves` is proposed (strip labels must stay ≥ 28 px:
   the strip cannot be a plain scale of the full state).
2. `Kit.equation` `E.box(id)` in `setup` (07.6, as in 05.2): boxes measured before the first render misplace pens
   (a box over `(E g)²` instead of `Var(g)/n`). Proposed fix: measure on the first render, or document that
   `E.box` is valid only in `render`. Workaround: pen marks drawn in render from the live box.
3. `Kit.plot` has only circle markers (07.3 asks for squares and triangles per series). Proposed: `marker` option.
4. `__QA__` formula-layer glyph overlaps (07.2, 07.3), as in ch05 issue 1.
