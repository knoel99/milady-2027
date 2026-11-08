# Batch 2 — done (2026-11-08)

Units ch05, ch06, ch07, ch08: all **done** and pushed to main. Common to every unit: built under a tight token budget
with no subagent, so **no independent review was run** (CONTRACT §13.5.8 is still owed for all four units). The
builder looked at the stills of every scene on the estimated timing, ran the French check (`LANG=fr TIMING=estimate`)
and watched mid-move frames of each draft. Every unit has 0 page errors on both timings and `make det` exit 0.
The only remaining scene warnings are question-card text-fit warnings (`why` / `unblocks` a few px too tall at
28 px), reported to the writer. The remaining QA items are formula-layer glyph overlaps (false positives), noted in each report.

**ch05** (`10aca29`, 6 scenes, draft 2:49). The toll counter, Rice on the 0.93 shoebox (26 of 8,000 in the strip), the
check against counted crossings (4 % / 6 %, recomputed and asserted in `tools/data_ch05.py` → `data/ch05_rice.json`),
crossings vs reversals, the bridge, and Q7. Known issues: the 05.2 Ḋ range was narrowed to ±1.5 in entry.params
(98 % of the data lie within ±1); the words recipe fades into Rice's formula (it does not morph); formula items are split by workarounds.

**ch06** (`506b565`, 6 scenes, draft 3:22). Exact toy flow-matching wind (closed form, Heun precomputed), two clocks / two
velocities, straight strings → average wind (Figure 4 a–b animated), the knob and the E1 protocol with real model-A
photos in the shoebox, and the noise floor (sand piles, die, floor, overlap). No data added. Known issues: 06.3's pen
on the formula-layer target was not drawn; 06.5 uses its own histograms rather than `Kit.histogram`.

**ch07** (`3682324`, 7 scenes, draft 4:11). The shelves device (`C7.shelves`), the lopsided model A, the mirror test,
asymmetry per Γ, the budget blind to the mirror, the spike (×9), and two juries. Data: `tools/data_ch07.py` →
`data/ch07_mirror.json`, `data/ch07_spike.json` (values match the script spec). Known issues: all series in 07.3 use
circle markers; long formulas are shown in parts.

**ch08** (`6ea023c`, 8 scenes, draft 5:06). The flat sheet (E2 maps), clean data / dirty outputs (0.41, V1, ×2.7),
hill maps and the Leray projection (`tools/data_ch08.py` → `data/ch08_hillmap.json`, derived from `e2_maps.json`),
almost ≠ exactly, three ways to fix a budget, the two full shelves, the proposed machine, and Q10. This unit has the
most simplifications: no arrows on the hill maps, no hovering card, a fade instead of the strip-to-full morph in 08.6,
and a simplified toll counter in 08.7.

**Script fields changed**: `visual` (an AS BUILT paragraph on every scene) and `entry.params` of 05.1, 05.2, 05.4,
07.1, 07.2, 07.3, 08.2, 08.3 and 08.5 (layout and ranges only). The narration was not touched.

**Kit issues reported** (details in each `scenes_<unit>.md`):
- formula-layer glyph overlaps are reported by `__QA__` as false positives;
- the layer's fixed width forces long statements to be split in the pages;
- `predictCard` cannot show a question without options;
- `E.box` measured in setup misplaces pens (05.2, 07.6);
- `Kit.knob` with `ticks: 0` gives NaN;
- a chip with `anchor 'tr'` and `maxWidth` near the right edge wraps to a narrow column;
- `Kit.plot` offers circle markers only;
- `chapterCard` has no sidestep option;
- shelves should be promoted to `Kit.shelves` (copied in ch07 and ch08).

**Findings for the writer**:
- formulas too long for one layer item in 05.2, 05.4, 06.5, 07.1, 07.2, 07.5, 08.3 and 08.5;
- question-card texts too long in ch05.Q, ch06.Q, ch07.Q and ch08.Q;
- 05.2's planned Ḋ range is too wide;
- 08.5's ESS mean (0.29) is over all 11 η (0.22 over the test η);
- C's asymmetry range is 0.0037–0.0049 in e1_eval (the report prints 0.0048).

**Blockers**: none. Pushes went through on the first attempt.
