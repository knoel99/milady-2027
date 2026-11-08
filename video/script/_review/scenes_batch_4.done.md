# Batch 4 — scenes done (2026-11-08)

Units, in build order: X2, X3a, X4a, X5a, X1, X3b, X4b, X5b, X6. Every unit passed `make check` (est. and fr) with
0 errors and `make det` (exit 0), and was drafted with `node build.js --unit <U> --draft`. No independent subagent
review was run (batch instruction), so CONTRACT 13.5 item 8 is open for all nine units. Per-unit reports:
`script/_review/scenes_<unit>.md`; AS BUILT paragraphs appended to every scene's `visual` in `script/<unit>.json`.

**X2** (`a03a2fc`, draft 3:51). Six pages (X2.1–X2.5, X2.Q). Known issues: blank first frame of X2.1 (ink change, intended);
four false-positive QA hits on an X2.3 formula; X2.Q card text fit warning.

**X3a** (`ebffc05`, 3:21). X3.0–X3.4 and X3a.Q. Six formulas overflow the formula layer (writer). X3.2 scatter reads
`per_eta.V4_potentiels` `residu_bilan_energie` because `en_loi.base` holds no per-η values.

**X4a** (`967c2b0`, 3:01). X4.1, X4.2 (pending curve), X4.3, X4.5 (pending lamps), X4a.Q. Added `tools/data_X4a.py` and
`data/X4a_tier0_anchor.json` (first-round values asserted against the report). X4.3 runs a bounded RK4 in the page.
Writer finding: 0.00485 displays as 0.0049.

**X5a** (`c964409`, 2:37). X5.1, X5.2, X5.3 (pending gauge), X5.4 (pending curve), X5a.Q. Over-long formulas.

**X1** (`4319309`, 2:18). X1.1, X1.2 (built flat, not WebGL: `deps` and `entry.data.modes` changed to
`data/e3_modes.json` because `X1_modes3d.json` does not exist), X1.3, X1.Q (question font 46 px by a CSS workaround).

**X3b** (`040df99`, 0:39). X3.5, pending lamps placed under the lanes.

**X4b** (`42d948b`, 0:45). X4.4, pending gauge; the plot fades and the seat replaces it; two formulas too long.

**X5b** (`af6bd4e`, 1:35). X5.5 (pending gauge; tier labels in a staggered legend row), X5.6 (the plan on one page; the
"shrink" is a fade and a move), X5b.Q. Seat gauge labels SUCCESS / AWAITING DATA touch; two formulas too long.

**X6** (`3ee4c6e`, 4:49). X6.0–X6.6 and X6.Q. New `tools/data_X6.py` and `data/X6_rm_conventions.json` (P3 Ex. 6.1,
transcribed and re-derived, no run). X6.4/X6.5 flat instead of Three.js; X6.4 without the 2 × 2 mini-frames; T1/T2
morphs approximated by cross-fades; no M1 needle in X6.6; 12 formulas too long; X6.Q card texts overflow.

Kit issues across the batch: formula layer clips long formulas; question-card fit; `Kit.seat` (no `why`, tag runs into
the column, single-line lamp labels, no lamp mini-frames); staircase labels overlap in small boxes; `ctx.at` cannot chain
offsets; `Kit.plot` throws on `out: null`; `Kit.knob` `ticks: 0` gives NaN; `predictCard` has no "neither" answer.
