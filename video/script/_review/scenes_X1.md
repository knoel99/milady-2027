# Scenes X1 — build report (batch 4, 2026-11-08)

No independent subagent review was run (batch instruction). CONTRACT 13.5 item 8 is open for this unit.

## 0. Status

| Scene | Check (est. and fr) | Notes |
|---|---|---|
| X1.1 | 0 err; 1 warning (formula too long); 0 QA | e3_growth |
| X1.2 | 0 err; 3 warnings (formulas too long); 38 QA = formula clipping | **flat instead of WebGL**, e3_modes |
| X1.3 | 0 err; 2 warnings (formulas too long); 18 QA = formula clipping | e3_growth |
| X1.Q | 0 err; 2 warnings (card WHY / UNBLOCKS fit) | question shrunk by scene CSS |

`make det U=X1`: exit 0. Draft 2:18; capture 45–60 fps.

## 1. Script fields changed

- X1.2 `deps` and `entry.data.modes`: `data/X1_modes3d.json` → `data/e3_modes.json` (the requested file does not exist;
  see §3.1). Every scene: AS BUILT paragraph in `visual`.

## 2. Data checks

- X1.1: exact_check s = −0.500053 vs bound −0.5 (relative 1.1 × 10⁻⁴); late fit −0.500007; difference 4.6 × 10⁻⁵.
- X1.2: |B| at the stagnation points read from the stored 32³ field at the nearest grid point; ≥ 0.9 at four points for
  Rm 8, 16, 20 as the narration says (none for Rm 12) — the scene shows whatever the data give.
- X1.3: at Rm 17.5, long +2.34 × 10⁻⁴, late −2.2 × 10⁻⁴, 48³ −5.2 × 10⁻⁴ (signs split); at Rm 12 the three agree;
  max |s − s_q| for 20 ≤ Rm ≤ 26 ≈ 2.2 × 10⁻³.

## 3. Findings for the writer / lead

1. X1.2 asks for `data/X1_modes3d.json` (isosurfaces, field lines, at_stagnation, blobs) from a new converter in
   tools/data_existing.py (not a builder's file). Not available: the scene was built flat from e3_modes.json. If the
   converter is written later, the WebGL version can replace this page; the narration's "surface wraps its strong parts;
   threads trace its lines" is only half shown (no threads).
2. data/e3_growth.json names series[0] "whole run" although it is the second-half fit (noted in the script); never shown.
3. Nine onscreen formulas in the unit overflow the formula layer (X1.1 fade; X1.2 eight, still, target; X1.3 edge, why).
4. X1.Q text overflows the card (question three lines, WHY and UNBLOCKS boxes).

## 4. Kit issues

1. `Kit.questionCard`: a three-line question overlaps the WHY / UNBLOCKS rows (QA overlap). Workaround: scene CSS
   `.kit-qcard .qc-q { font-size: 46px }`. Proposed: fit the question to the space above the rows.
2. `Kit.plot`: `out: null` throws "time spec missing" (only `undefined` is accepted). Proposed: treat null as no exit.

## Review

Not run (batch instruction).
