# Scenes X3a — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction: tight token budget, no separate review pass). CONTRACT
13.5 item 8 is open for this unit.

## 0. Status

| Scene | Check (est.) | Check (fr) | Notes |
|---|---|---|---|
| X3.0 | 0 err / 0 warn / 0 QA | same | flat, schematic toy crowds |
| X3.1 | 0 / 3 warnings: two onscreen formulas too long for the formula layer (writer), blank first frame (intended: ink change from PAPER) / 0 | same | toy law computed in setup |
| X3.2 | 0 / 1 warning (formula too long) / 24 QA = that formula's clipped glyphs | same | e2_eval |
| X3.3 | 0 / 2 warnings (formulas too long) / 20 QA = clipped formula glyphs | same | e1_samples_0.93, Canvas |
| X3.4 | 0 / 1 warning (formula too long) / 13 QA = clipped formula glyphs | same | e2_eval |
| X3a.Q | 0 / 2 warnings (question card WHY/UNBLOCKS too long) / 0 | same | card |

`make det U=X3a`: exit 0. Draft 3:21 at 960×540, capture 44–63 fps.

## 1. Deviations

See each scene's "AS BUILT (2026-11-08, batch 4)" paragraph in `script/X3a.json`.

## 2. Data checks

- X3.2: 0.99 (0.989882) at η = 0.00476; three largest test values 0.00215, 0.002, 0.002 (≈ one in 500 = n_gen/2);
  mean 0.287 → "0.29". The entry's `en_loi.base.residu_bilan_energie (per η)` does not exist (train/test means only);
  per-η values come from `per_eta.V4_potentiels` (all generated samples, not half b). With them the order of ESS/N
  has one swap (η = 0.004 and 0.0067), as the chip says.
- X3.4: 7.74 → 2.22 at η = 0.0190 (control 7.63); 0.184 vs 0.186 at η = 0.00476; budget error +122 % → 2.2×.
- X3.1: the tilt's KL is the smallest of the three weightings (checked in setup).

## 3. Findings for the writer

1. Formula layer: six onscreen formulas do not fit the layer even at 28 px on two lines (X3.1 `least`, `moves`; X3.2
   `sheet`; X3.3 `no`, `push`; X3.4 `control`): they are clipped at the right edge. Shorten or split them with `;`.
2. X3a.Q: `why` and `unblocks` overflow the card's boxes (cards.js warning).
3. X3.2: the scatter's x quantity is described as "on the same half b"; the per-η values available are on all samples.

## 4. Kit issues

1. `Kit.formulaLayer` / `Kit.fitFormula`: when a statement cannot fit, it is clipped at the frame edge (QA `clipped`).
   Proposed: allow a third line or a smaller floor for the formula layer only, or fail the build. No workaround.
2. Same `ctx.at` chained-offset and question-card fit items as X2 (see scenes_X2.md §4).

## Review

Not run (batch instruction).
