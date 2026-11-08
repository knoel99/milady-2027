# Scenes ch11 — build report (batch 3, 2026-11-08)

## 0. Status

| Scene | Badge | Estimated check | French check | Determinism |
|---|---|---|---|---|
| 11.1 | MEASURED / PLANNED | 0 errors · 0 warnings · 5 QA (pen over text, false positive, §4.1) | same | ok |
| 11.2 | — | 0 · 0 · 0 | same | ok |
| 11.3 | — | 0 · 0 · 0 | same | ok |

`make det U=ch11` exit 0. Draft `out/draft/unit_ch11/unit_ch11_draft.mp4`, 2:06. Timing: estimated and French
estimate only (no narration in this clone).

**Process deviation (lead's instruction for this batch):** no independent subagent review (token budget). CONTRACT
§13.5 item 8 is NOT met.

## 1. What was built

`ch11_kit.js` (unit helpers), three pages. Per-scene deviations are in each `visual` ("AS BUILT (2026-11-08, batch 3)").
Main ones: no WebGL compass in 11.2 (2D dial); the montage redraws earlier scenes from data instead of capturing them;
11.1 bet texts are ellipsised to one line.

## 2. Script fields changed

`entry.data` of 11.1 (`ledger`, `measured`) and 11.2 (`measured`, `e1`: e1_finegrid, `s093`: e1_samples_0.93);
`deps` unchanged (already listed these files); `visual` (AS BUILT appended, 3 scenes).

## 3. Data

`tools/data_ch11.py` → `data/ch11_measured.json` (the E1/E2/E3 numbers the chapter narrates, read from the existing
result files, plus the caveats list) and `data/ch11_ledger.json` (the six bets; every row `pending: true` until the cloud
results exist). The notes asked for these files from `tools/data_existing.py` / `tools/data_cloud.py`; they are
written here by a unit tool with the requested fields. The ledger must still be refreshed by `data_cloud.py` after each
cloud conversion (not done: no cloud file exists).

## 4. Findings and notes

1. 11.1: the layout QA reports the pen underline over the caveat label; the underline targets a span inside that label
   (intended), the stills are clean.
2. 11.1: the bet texts of the script are too long for a one-line row at 28 px; shorter bet titles would avoid the ellipsis.
3. 11.3: the credits and disclaimer are long; at the current length they fit (left column ends near y 760), any addition
   will not.

## 5. Kit issues

None new (see ch10 report for `Kit.seat` / `Kit.formulaLayer`).
