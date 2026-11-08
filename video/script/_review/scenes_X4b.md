# Scenes X4b — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

| Scene | Status | Check (est. and fr) | det | Draft |
|---|---|---|---|---|
| X4.4 | pending (seat gauge) | 0 err; 2 warnings (formulas `round`, `bet` too long); 76 QA = clipped formula glyphs | exit 0 | 0:45, 60 fps |

Deviations: AS BUILT paragraph in `script/X4b.json` (crossfade between the two normal-form plots, plot leaves at
'bet+1.0' instead of shrinking, grey circling-dot ghost instead of Kit.tracers, 'why' not drawn). SCHEMATIC shapes only;
the published values 206 and 70 come from the entry (Ponty et al. 2007) and are placed on a schematic axis (chip says
so). Result variant not rendered (no data, D4).

Findings for the writer: two formulas overflow the formula layer.

Kit issues: `Kit.seat` has no field for the entry's `why`; `Kit.knob` with `showValue: false` is used for a schematic
knob (fine).

## Review

Not run (batch instruction).
