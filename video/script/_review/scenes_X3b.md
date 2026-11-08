# Scenes X3b — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

| Scene | Status | Check (est. and fr) | det | Draft |
|---|---|---|---|---|
| X3.5 | pending (seat lamps) | 0 err; 1 warning (formula `why` too long for the formula layer); 0 QA | exit 0 | 0:39, 59 fps |

Deviations: AS BUILT paragraph in `script/X3b.json` (seat lamps under the lanes, compact lanes, no dashed tracks, title
moved, 'why' not drawn). Numbers on screen: 2D ghosts 6.1 %, 46 %, 0.79 (and the 0.66 control tick) read from
data/e2_eval.json (V5_potentiels_stat / V5_temoin, mean.test). Result variant not rendered (no data, D4).

Findings for the writer: the `why` formula overflows the formula layer.

Kit issues: `Kit.seat` lamps cannot be placed at external positions (here the lane ends) and its lampsTitle is
single-line SVG text that runs under the right column; workaround: lamps listed in the frame under the lanes, title as
an HTML label. Proposed: options `lampPositions` and a wrapped title.

## Review

Not run (batch instruction).
