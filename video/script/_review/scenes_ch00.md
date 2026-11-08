# Scenes ch00 — build report (batch 1, 2026-11-08)

Builder: scene-builder session, batch 1. No independent review pass: the batch was launched with a tight token budget
and an explicit instruction to skip the separate review (the builder looked at every still and at mid-move frames of
the draft itself). **A reviewer pass is still owed** (SESSION-BRIEF §6 step 6).

## 0. Status

| Scene | Page | Check en / fr (errors, warnings, QA) | det | draft fps |
|---|---|---|---|---|
| 00.1 | `scenes/ch00/00_1_a_needle_that_flips.html` | 0/0/0 · 0/0/0 | ok | 57 |
| 00.2 | `scenes/ch00/00_2_pull_back_to_the_planet.html` | 0/0/0 · 0/0/0 | ok | 46 |
| 00.3 | `scenes/ch00/00_3_the_seafloor_tape_recorder.html` | 0/0/0 · 0/0/0 | ok | 62 |
| 00.4 | `scenes/ch00/00_4_two_questions.html` | 0/0/0 · 0/0/0 | ok | 61 |
| 00.5 | `scenes/ch00/00_5_title.html` | 0/0/0 · 0/0/0 | ok | 48 |
| ch00.Q | `scenes/ch00/00_Q_question.html` | 0/0/0 · 0/0/0 | ok | 55 |

Estimated length 1:28 (en), French timing longer (00.3: 20 s, 00.4: 35.6 s); every scene hangs on cues and holds on both.
Unit helpers: `ch00_kit.js` (`C0.runs` polarity runs from `normal_Ma`, `C0.flips`, `C0.needlePaths`, `C0.dipoleLines`), `ch00.css`.

## 1. What was built (deviations = the AS BUILT paragraphs of `script/ch00.json`)

- **00.1**: flat SVG compass (Kit.needle), not WebGL. Swing-in from east in the lead-in (spring), flip on `flip-0.15`,
  ghosts on `again`, back to north at `again+0.6`; 5 % push-in. The reference lower-third leaves at `flip-0.4`.
- **00.2**: flat reverse dive (compass on a tabletop → dot on a matte grey sphere; no room/coast/cloud layers); dipole
  lines tilted by `params.dipole_tilt_deg`, thinning (width, not alpha) on `not`; everything clipped at y 880.
  The shrinking compass group has `data-qa="ignore"`: its N/S letters pass under 28 px only while vanishing (false positive).
- **00.3**: cross-section, grains, spreading driven by `params.normal_Ma` (22 boundaries, checked against
  `flips_in_window`), page tick per boundary, morph of the left half into the strip (own SVG, not Kit.barcode), sign trace.
- **00.4**: strip → top band; cards; roadmap across the left half leading to the cloud on the right (not a row under
  the cards); Kit.cloud from `e1_samples_0.9.json` variant C_equivariant (D horizontal, Q vertical); tags; formula layer.
- **00.5**: dipole lines with drifting arrowheads, title on two lines, flip in the tail (arrowheads reverse, shade swap).
- **ch00.Q**: question card from the script; faint polarity strips behind.

## 2. Script fields changed

- `visual`: an AS BUILT paragraph appended to every scene.
- `entry.params` of 00.4 and ch00.Q: `window_Ma` and `normal_Ma` copied from 00.3 (the strip is drawn there too; no
  number typed in the pages). Narration untouched.

## 3. Data

No new data file. Numbers on screen: polarity ages and the "about 20 flips" caption come from the script (params,
onscreen labels; external CONTEXT sources); formulas from `onscreen.formulas`; the cloud from `data/e1_samples_0.9.json`
(source lower-third with stamp and SHA-256 prefix).

## 4. Findings for the writer

None contradicting the narration. Note: 00.1/00.2 are flat, not WebGL (render class "webgl" in the visual).

## 5. Kit issues

1. `runtime/components/motifs.js`, `Kit.needle`: no option for a start angle other than north/south (00.1 needs a
   swing-in from east). Workaround in the page: wrap `N.angle` with an entry offset. Proposed fix: `start` in degrees.
2. `runtime/components/motifs.js`, `Kit.cloud`: the `pts()` helper calls `Scene.f32`, which accepts a Float32Array,
   but the doc says "pts (n×2 data coordinates)"; a short note that an interleaved Float32Array works would help.
3. `runtime/components/hud.js`, `Kit.lowerThird` (kind `reference`): a long l2 wraps to three lines (00.3, 55 characters).
   Workaround: `white-space: nowrap` + `Kit.fit` on `.l2`. Proposed fix: the same one-line rule as `kind: 'source'`.
