# Scenes X5a — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

## 0. Status

| Scene | Status | Check (est. and fr) | Notes |
|---|---|---|---|
| X5.1 | ready | 0 err; 3 warnings: two formulas too long (writer), blank first frame (intended ink change); 12 QA = formula clipping | entry values (C:153, C:176) |
| X5.2 | ready | 0 / 0 / 0 | schema drawing, no numbers |
| X5.3 | pending (seat gauge) | 0 / 0 / 0 | campaign file values only |
| X5.4 | pending (seat curve) | 0 err; 3 warnings: two formulas too long, blank first frame (ink change from BLUEPRINT); 0 QA | toy from the entry |
| X5a.Q | ready | 0 err; 1 warning (card text fit) | card |

`make det U=X5a`: exit 0 (one earlier run exited 2 while a check ran in parallel; re-run alone: all identical or
anti-aliasing). Draft 2:37; capture 47–53 fps. Result variants not rendered (no seat data, D4).

## 1. Deviations

See the AS BUILT paragraphs in `script/X5a.json`.

## 2. Findings for the writer

1. Four onscreen formulas do not fit the formula layer (X5.1 smudge, memory; X5.4 lines, answer): clipped.
2. X5a.Q: card text overflow warning (cards.js).
3. X5.1's numbers (0.08 s, 717 MB, 0.4/6/48 GB, 24/80 GB cards) live in the script entry, not in a data file: the
   contract's "every number from data/" would want a tools/data_X5a.py reading en/calcul/index.qmd; not done (the
   values are quoted page text with their line references).

## 3. Kit issues

1. `Kit.seat`: the data tag (frame top-left) is long and runs into the fixed right column at x 1216 when the frame is
   narrow; workaround X5.3: column moved down by scene CSS. Proposed: clip/wrap the tag to the frame width.
2. `Kit.seat`: no field for the entry's `why` (X5.3, X5.4).
3. `Kit.predictCard` cannot show an answer that is none of the options (X5.4 "neither"); the card simply leaves.

## Review

Not run (batch instruction).
