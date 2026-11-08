# Scenes X6 — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

| Scene | Status | Check (est. and fr) | det | Draft |
|---|---|---|---|---|
| X6.0 | ready (new data file) | 0 err; 2 warnings (1 formula too long, blank first frame = ink change); QA = clipped formula glyphs + pen circle over 'Rm = ?' (intended) | exit 0 | unit draft 4:49 |
| X6.1 | ready | 0 err; 2 formulas too long | exit 0 | idem |
| X6.2 | ready | 0 err; 1 formula too long | exit 0 | idem |
| X6.3 | ready | 0 err; 2 formulas too long | exit 0 | idem |
| X6.4 | pending (seat lamps) | 0 err; 3 formulas too long, blank first frame (ink change) | exit 0 | idem |
| X6.5 | pending (seat curve) | 0 err; 3 formulas too long; QA = clipped glyphs, knob label 'Po' clipped | exit 0 | idem |
| X6.6 | ready | 0 err; 0 warnings; QA = clipped formula glyphs | exit 0 | idem |
| X6.Q | ready | 0 err; 2 card text fit warnings | exit 0 | idem |

Data: `data/X6_rm_conventions.json` (new) from `tools/data_X6.py`, a transcription of P3 Example 6.1 and R:141 whose
printed values (30.9, 42.5, 51.5, 70.8; ratios 1.67 and 1.05) are re-derived from the example's formulas and asserted;
no run. The data contract named `tools/data_existing.py`, a shared tool this batch may not edit, hence a unit tool.

Deviations (AS BUILT paragraphs in `script/X6.json`): X6.4 and X6.5 are flat SVG, not Three.js; X6.4 lamps are the kit's
four rows, without the 2 × 2 mini-frames; the T1/T2 morphs and zooms of X6.1/X6.2 are cross-fades; X6.0 and X6.1
"shrink" beats are fades (text would go under 28 px); X6.6 has no M1 corner needle and draws the mirror links itself.
Result variants of X6.4/X6.5 not rendered (no data).

Findings for the writer: 12 formulas across the unit overflow the formula layer; X6.Q card texts overflow.

Kit issues: `Kit.seat` lamps cannot carry mini-frames or a 2 × 2 layout, has no `why`; `Kit.knob` with `ticks: 0` writes
NaN coordinates; `Kit.chip` cannot hold the three-line MFF chip.

## Review

Not run (batch instruction).
