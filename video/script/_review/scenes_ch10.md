# Scenes ch10 — build report (batch 3, 2026-11-08)

## 0. Status

| Scene | Status | Badge | Estimated check | French check | Determinism |
|---|---|---|---|---|---|
| 10.1 | ready | PLANNED | 0 errors · 0 warnings · 0 QA | same | ok |
| 10.2 | ready (BLUEPRINT) | MEASURED | 0 · 0 · 0 | same | ok |
| 10.3 | pending (seat curve) | CONJECTURE high | 0 · 0 · 0 | same | ok |
| 10.4 | pending (seat curve) | CONJECTURE medium | 0 · 0 · 0 | same | ok |
| 10.5 | pending (seat map) | CONJECTURE medium | 0 · 1 warning (formula too long, §4) · 0 | same | ok |
| 10.6 | ready, **data missing** → rendered as pending | PROVED | 0 · 0 · 0 | same | ok |
| 10.7 | pending (seat lamps) | CONJECTURE low | 0 · 0 · 0 | same | ok |
| 10.8 | ready (PAPER) | PROVED | 0 · 1 warning (formula too long, §4) · 0 | same | ok |
| 10.9 | pending (two seats) | CONJECTURE low | 0 · 0 · 0 | same | ok |
| ch10.Q | ready | — | 0 · 1 warning (unblocks 9 px too tall) · 0 | same | ok |
| 10.9-bridge | ready (extended) | PLANNED | 0 · 0 · 0 | same | ok |

`make det U=ch10` exit 0. Draft `out/draft/unit_ch10/unit_ch10_draft.mp4`. Timing: estimated + French estimate only.
Only the **pending** variant was checked: no cloud data file exists, so the result variants (Kit.seat drawing the
converter's data) are untested.

**Process deviation (lead's instruction for this batch):** no independent subagent review (token budget). CONTRACT
§13.5 item 8 is NOT met.

## 1. What was built

Per-scene deviations are in each `visual` ("AS BUILT (2026-11-08, batch 3)"). Unit helpers in `ch10_kit.js`: `UK.seat`
(Kit.seat with the script's seat params; cues that only the result narration has, `data` / `verdict`, fall back to
frame + 0.8; the `why` line under CONFIDENCE), `UK.formulaItems` (splits a long statement at its top-level `;`, `+`,
`\ \`, `\quad` or `\Rightarrow`, up to four steps) and `UK.formulaLayers` (one layer per step, the steps of one
statement share the time to the next statement, optional bottom-left placement when a seat column fills the right).
Main simplifications: no WebGL in 10.6 (2D SVG), no box→cylinder morphs in 10.1/10.8, several small icons and insets
dropped (10.4 two-fit inset, 48³ squares and window shading; 10.2 jar zoom and chef cloud; 10.3 strips; 10.7 spectrum
frame; 10.9 DRESDYN result drawing).

## 2. Script fields changed

`visual` only (AS BUILT appended, 11 scenes). `deps` / `entry` unchanged.

## 3. Data

No new file. **`data/fm3d_guarantees.json` (10.6) is missing**: the scene is `ready` in the script but the assembler
renders it as pending; the page draws the mechanism schematically and the gauge reads AWAITING. It should be produced
by the foundation engineer (fm3d decoder, random weights, float64 decode) before the final render.

## 4. Findings for the writer

1. 10.5 formula "saturated if |slope of ln E_B over the kept window|/2 < 0.1 s_kin" and 10.8 formula "pseudo-vacuum
   shifts the threshold: Rm_c = 90 ± 5 vs 130 ± 10 …" do not fit the 760-px layer at 28 px even after splitting:
   shorten or add a `;`.
2. ch10.Q `unblocks` overflows by one line: shorten slightly.
3. 10.6 depends on a file that does not exist; until it does, "even with untrained weights … to rounding" is drawn
   without its number.

## 5. Kit issues

1. `runtime/components/seat.js`, `Kit.seat`: it calls `ctx.at` on every cue it is given, including `data` / `verdict`,
   which exist only in the result narration, so a pending page throws unless it strips them (workaround `UK.seat`).
   Proposed fix: ignore unknown cues in the pending variant.
2. `Kit.seat` does not return its plot (`P`), so a page cannot add the extra marks a `visual` asks for (48³ squares,
   window shading, pen marks in data coordinates); return it.
3. `Kit.seat` map type: the 'AWAITING DATA' text and the default axis letters 'x' / 'y' cannot be turned off.
4. Kit.formulaLayer and the column of Kit.seat share the bottom-right: with a seat, the layer had to move to the
   bottom-left (workaround in `UK.formulaLayers`).
