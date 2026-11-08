# Scenes ch06 — build report (batch 2, 2026-11-08)

Builder: scene-builder session of batch 2. No independent subagent review (the launch prompt forbade subagents and a
separate review pass); the builder looked at every still on the estimated timing, the French check report and
mid-move frames of the draft. **The independent review of CONTRACT §13.5.8 is still owed.**

## 0. Status

| Scene | Page | Badge | Est. | FR | QA | Notes |
|---|---|---|---|---|---|---|
| 06.1 | 06_1_from_noise_to_data.html | CONTEXT | ok | ok | 0 | exact toy wind, Heun precomputed |
| 06.2 | 06_2_two_clocks_two_velocities.html | SCHEMATIC | ok | ok | 0 | |
| 06.3 | 06_3_straight_strings_average_wind.html | PROVED | ok | ok | 0 | |
| 06.4 | 06_4_turn_the_knob_reshape_the_cloud.html | MEASURED (from 'dots') | ok | ok | 0 | |
| 06.5 | 06_5_the_noise_floor.html | CONTEXT | ok | ok | 0 | formula 2 split (workaround) |
| ch06.Q | 06_Q_question.html | none | ok | ok | 0 | 1 card text-fit warning (writer) |

`make det U=ch06 TIMING=estimate`: exit 0. Draft `out/draft/unit_ch06_est/unit_ch06_draft.mp4` 3:22 (estimate);
capture 49–57 fps at draft size.

## 1. Data

No new data file. `data/fig_flow_matching.json` (SCHEMATIC: shapes only, no number on screen), `data/e1_eval.json`
(train / test Γ of model A) and `data/e1_samples_0.93.json` (simulated and model-A snapshots) are read as the script's
`deps` say. Some blocks of `fig_flow_matching.json` are stored as Python-repr strings (`params`, `fan`); the unit kit
parses them (`C6.val`).

## 2. Per scene

As in the AS BUILT paragraph of each scene's `visual` in `script/ch06.json` (only `visual` changed in the script).

## 3. Findings for the writer

1. **06.5 formula 2** (`\mathcal{E}(P_1, P_2) = …`) does not fit the formula layer at 28 px; shown with a `\quad` break
   before the parenthesis. A `;` break in the script would avoid the page workaround.
2. **ch06.Q**: the `unblocks` text is about 40 px too tall for the card at 28 px; shorten it.
3. **06.4 'Q at 60 % --b'** (visual): the kit's `Kit.photo` draws Q in `--b-light` (the quadrupole token); kept.

## 4. Kit issues

1. `runtime/components/motifs.js` `Kit.knob`: `ticks: 0` divides by zero (NaN attributes, page error). Proposed fix:
   skip the tick ring when `ticks` is 0. Workaround: default ticks.
2. `runtime/components/hud.js` `Kit.chip` with `maxWidth` and `anchor: 'tr'` near the right edge: the absolutely placed
   chip shrink-wraps to the space left of its `left` (x 1760 → 160 px), so it wraps to many narrow lines although
   `maxWidth` is 640+. Proposed fix: set `width: max-content` with `max-width`, or position by `right`. Workaround:
   left-anchored chip.
3. `Kit.formulaLayer`: no way to target an item's sub-term for a pen beat (06.3 asks for an underline on the regression
   target `(x_1 − x_0)` in the layer). Proposed: expose the item rows (`layer.items[i].el`) or accept `\term{}` ids.
