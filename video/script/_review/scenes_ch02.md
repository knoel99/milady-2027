# Scenes ch02 — build report (batch 1, 2026-11-08)

Builder: scene-builder session, batch 1. No independent review pass (tight token budget; the launch prompt asked to
skip it). Every still was looked at, plus mid-move frames of the draft. **A reviewer pass is still owed.**

## 0. Status

| Scene | en: errors/warnings/QA | fr | det | draft fps |
|---|---|---|---|---|
| 02.1 Frozen threads | 0/0/0 | 0/0/0 | ok | 40 |
| 02.2 One number for the race | 0/0/0 | 0/0/0 | ok | 65 |
| 02.3 The sodium problem | 0/0/0 | 0/0/0 | ok | 57 |
| 02.4 Three tanks that worked | 0/0/0 | 0/0/0 | ok | 64 |
| 02.5 VKS: two impellers | 0/0/0 | 0/0/0 | ok | 65 |
| 02.6 VKS flips too | 0/0/0 | 0/0/0 | ok | 65 |
| ch02.Q | 0/0/0 | 0/0/0 | ok | 54 |

Estimated length 3:12 (en); French timing about 15 % longer, every scene holds. `make det U=ch02` exit 0.
Unit helpers: `ch02_kit.js` (copy of the ch01 helpers under `C2`), `ch02.css`.

## 1. Deviations (details in the AS BUILT paragraphs of `script/ch02.json`)

- 02.1: two inks drawn in the page; flow time at 0.4 of scene time (`time_scale`, a scene-side tuning value, not in
  the script): at the script's speed the line outgrew any resolution within the scene.
- 02.2: knob right, plot left (the plot's axis title met the formula layer on the right).
- 02.3: own dials (Re linked to Rm every frame).
- 02.5: flat cutaway instead of WebGL; single cut plane; no camera orbit.
- 02.6: narrow plot from the start instead of a shrink at 'quick'.

## 2. Script fields changed

`visual` (AS BUILT) on every scene. No data file, no `deps` change. Narration untouched.

## 3. Findings for the writer

None: the numbers on screen come from the script's params, labels and formulas (all sourced); `fig_vks.json` is used
for shapes only, under the SCHEMATIC chip.

## 4. Kit issues

1. `runtime/components/motifs.js`, `Kit.twoInks`: no per-segment stretch brightness, no diffusion (ribbon width
   sqrt(2 kappa tau)), no time scale, and its line resolution caps at 6000 points (straight chords after long
   stretching). 02.1 reimplements it. Proposed: options `stretchBrightness`, `kappa`, `timeScale`, `panels`.
2. `runtime/components/cards.js`, `Kit.predictCard`: warns without `options`; 02.5's predict beat has none. Proposed:
   allow a question-only card.
3. `runtime/components/motifs.js`, `Kit.knob`: no way to drive a knob from another quantity each frame (`value: (t) =>`),
   needed for 02.3's Re = Rm / Pm. Workaround: own dials.
