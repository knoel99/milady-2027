# Scenes X4a — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

## 0. Status

| Scene | Status | Check (est. and fr) | Notes |
|---|---|---|---|
| X4.1 | ready | 0 err; 1 warning (formula too long); 17 QA: formula clipping + 'TRUE RATE' over the tick column | synthetic demo + E1 shoebox |
| X4.2 | pending (seat curve) | 0 err; 3 warnings (formulas too long); 50 QA = formula clipping | READY anchors from e1_samples_0.9 + e1_finegrid |
| X4.3 | ready | 0 err; 3 warnings (formulas too long); 7 QA = formula clipping | live RK4 (bounded), e1_samples_0.9 |
| X4.5 | pending (seat lamps) | 0 err; 3 warnings (formulas too long); 48 QA = formula clipping | new data X4a_tier0_anchor.json |
| X4a.Q | ready | 0 err; 2 warnings (card WHY / UNBLOCKS too long) | card |

`make det U=X4a`: exit 0. Draft 3:01; capture 37–62 fps. Result variants not rendered (no seat data, D4).

## 1. Data added

`tools/data_X4a.py` → `data/X4a_tier0_anchor.json` (meta with the SHA-256 of experiences/resultats/e1_gissinger.json).
It recomputes and asserts the report's first-round values: model C |P(D>0) − ½| min 0.0037, max 0.00485 (seed means over
the 21 Γ); floor √(2/π)/(2√n) = 0.0040 (n = 10,000); degree-3 residual 0.0113 (F) vs 0.0224 (F0), ×1.98; Rice on model C
seed 0, cumulative 14 % (Γ ≥ 0.89), 42 % (0.865–0.885), pointwise max 65 %.

## 2. Deviations

See the AS BUILT paragraphs in `script/X4a.json`. Main ones: X4.3 waits from one bounded run (≈ 650 waits, dt 0.02)
instead of 1,500 at dt 0.01 (setup budget); X4.1 crossfade instead of morph; X4.5 lamp c text shortened and lamp
labels at 28 px with the seat column moved right by scene CSS.

## 3. Findings for the writer

1. Onscreen label "first round, 2 seeds: 0.0037 to 0.0048 vs floor 0.0040": the recorded maximum is 0.00485, which the
   page formats as 0.0049 (toFixed(4)); the report and the label say 0.0048. Decide which to print.
2. Ten onscreen formulas in this unit do not fit the formula layer even at 28 px (X4.1 chaos; X4.2 cap, plateau, bet;
   X4.3 twins, dials, short; X4.5 mirror, bet, catch): clipped at the right edge. Shorten or split.
3. X4a.Q: WHY and UNBLOCKS overflow the card's boxes.
4. X4.3: the comb shows clearly at bins = 60 with the bounded run; no change to coefficients or Γ was needed.

## 4. Kit issues

1. `Kit.staircase` with a small box (420 × 210, as the entry asks) overlaps its own tier labels; workaround: drawn large
   during one beat only. Proposed: scale label size/positions with the box or drop labels below a width.
2. `Kit.seat` (lamps): long lamp labels are single-line SVG text and run under the fixed right column (`.kit-seat-col`
   left 1216). Workaround: 28 px labels and the column moved to 1256 by scene CSS. Proposed: wrap lamp labels to the
   frame width, or make the column position an option.
3. `Kit.seat`: no field for the confidence block's "why" text (X4.2, X4.5 entries carry `why`). Not shown.
4. Formula layer clipping and question-card fit: see scenes_X3a.md §4 and scenes_X2.md §4.

## Review

Not run (batch instruction).
