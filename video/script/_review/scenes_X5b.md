# Scenes X5b — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

| Scene | Status | Check (est. and fr) | det | Draft |
|---|---|---|---|---|
| X5.5 | pending (seat gauge) | 0 err; 3 warnings (2 formulas too long, blank first frame = ink change); 29 QA = clipped formula glyphs + seat gauge SUCCESS/AWAITING labels | exit 0 | in 1:35 unit draft |
| X5.6 | ready | 0 err; 1 warning (blank first frame = ink change); 0 QA | exit 0 | idem |
| X5b.Q | ready | 0 err; 1 warning (card text fit) | exit 0 | idem |

Deviations: AS BUILT paragraphs in `script/X5b.json`. X5.5 tier labels in a staggered legend row (tiers 0-1 too thin);
X5.6 "shrink" done by fading the axis bands and long labels and moving the bars up (a scale would put text under 28 px);
no M7 staircase icons on the timeline rows. Result variant of X5.5 not rendered (no data).

Findings for the writer: two X5.5 formulas overflow the formula layer; X5b.Q "what it unblocks" overflows by a few px.

Kit issues: `Kit.seat` gauge labels SUCCESS and AWAITING DATA overlap at small frame heights; no `why` field.

## Review

Not run (batch instruction).
