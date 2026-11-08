# ch04 scenes: pilot build report (2026-11-08)

Unit `ch04` "Chaos and the shoebox of photographs": 8 scenes (04.1–04.7, ch04.Q), built as the pilot of the
shared components before the other 23 units. This file covers what was built, the components each scene uses,
the workarounds, and every problem or missing feature found in the shared kit. Each problem names the file and a
fix for foundation engineer B (runtime, components) or A (pipeline).

## 0. Status

| Item | Result |
|---|---|
| Pages | `scenes/ch04/04_1_three_dials.html` … `04_7_crowd_laws.html`, `04_Q_question.html`. The `file` fields of the script were already correct. |
| Unit helpers | `scenes/ch04/ch04_kit.js` (shared JS of the unit) and `scenes/ch04/ch04.css` (tokens only). Both count in every ch04 scene's render hash (build.js P3). |
| New data | `data/ch04_lyapunov.json`, written by `tools/data_ch04.py` (see §3, 04.4). It is the only new file in `data/`. |
| Unit check, estimated timing | 8/8 scenes, 0 page errors. Report: `out/check/unit_ch04/report.json`, one contact sheet per scene. |
| Unit check, real narration | 8/8 scenes, 0 page errors. This run reads `audio/scenes/<id>.align.json` read-only (the narration agent wrote them at 08:34). Report: `out/check/unit_ch04_real/`. |
| Remaining scene warnings | One, intended: 04.3 uses the schematic excursion inset that the script prescribes (§3). |
| Remaining layout QA | ch04.Q: 3 false positives from `__QA__` (§4 item 5). Nothing else. |
| Draft (960×540, 15 fps, subtitles burned in) | `out/draft/unit_ch04/unit_ch04_draft.mp4`, estimated timing, no sound, 4:14. |
| Draft with narration | `out/draft/unit_ch04/unit_ch04_draft_real.mp4`, real timing, narration muxed from `audio/scenes/*.wav` (read-only), 4:29. |
| Motion scan of the draft | No flicker. Each scene was checked frame by frame (mean absolute difference, plus an A-B-A test). Difference spikes appear only on deliberate moves: the 04.1 bench shrink, the 04.3 strip exit, the 04.4 PREDICT card exit. I looked at frames in the middle of every transition. |
| Determinism (`tools/determinism.js`) | A frame reached by a direct seek is bit-identical in two fresh browsers for every scene tested (04.2, 04.4, 04.5, 04.6, 04.7). A frame reached by sequential seeking differs only by anti-aliasing: at most 5 grey levels in 04.6 and 04.7, 86 edge pixels on the knob and needle in 04.2. 04.4 and 04.5 are identical either way. |
| Performance | Setup takes 0.13–0.47 s (04.2's seeded search is the slowest). Seek costs 1.6–7.6 ms per frame, except 04.5 (glow canvases) at 16 ms. Draft capture runs at 43–72 fps. All within CONTRACT §8. |

`audio/` and the narration text were never written. How the checks ran without touching `audio/` is in §5.1.

## 1. What every ch04 scene shares

- **`C4.fixAt(ctx)`**, the first call in every `setup`. It works around a runtime bug: `'cue-0.15'` throws (§4 item 1).
- **Frame 0 is never black.** A scene is hard-cut to the previous one. Any layout keyed to the first cue (0.4 s) would flash black for 8 frames. Badges, chips, panels, strips and the chapter card therefore enter at a negative time (`at: -0.3`). Only the content keyed to the narration waits for its cue.
- **The formula layer shows one item at a time** (`C4.formulas(ctx)`, §4 item 3).
- **The quadrupole colour** is a light vermillion, `--b` mixed with `--fg`. It comes from `C4.qcol()` and the `.k-q` class through `--q` on `#stage`.
  - The script asked for `--b` at 60 % opacity. On NIGHT that gives #914427, almost the same as `--b-neg` #9C3F18, so Q would read as negative polarity (§4 item 9).
  - `q_shade_opacity` now means the share of `--b` in the mix.
- **Live integrations of the three-mode model** go through `C4.model(mu, nu)`.
  - It is the same RK4 as `assets/interactif/gissinger.js`, with the coefficients read from `ctx.data.e1.config`.
  - It is used in 04.2, 04.3, 04.4, 04.5 and 04.6, and is labelled 'illustration · live integration of the model' where the script says so.
  - Starting states come from seeded searches. The searches are re-run against the real cue times, so a scene stays correct whatever the narration timing. A failed search warns through `__SCENE_WARNINGS__`.
- **Badges** take their kind from the script, and their note from `ctx.script.badge.note` (§4 item 2).

## 2. Per scene

### 04.1 Three dials (CONTEXT, 33.8 s real)

- **Built**
  - The T4 chapter card runs in the lead-in, with the staircase at tier 0 and the rail at L2.
  - Three schematic dials (Q, D, V) are joined by zig-zag springs. The pointers swing in on a spring with at most 3 % overshoot, then idle with a coupled jiggle while the springs breathe.
  - Labels have small dipole and quadrupole icons. The knob Γ has a green arrow into V.
  - Three equation rows are built on `eqs`; the coefficients come from `e1_finegrid.json` config. Dashed leaders run from each row to its dial.
  - On `mirror`, Q and D swing to the other side and D's shade goes from `--b` to `--b-neg`. The rows pulse, the pen ticks them, and 'same equations' appears.
  - On `bench`, the text fades and the dial group shrinks onto tier 0 of a centred staircase. The pen circles tier 0, with the label underneath.
- **Components:** `Kit.chapterCard` (with `K.staircase`, `K.rail`), `Kit.badge`, `Kit.knob`, `Kit.equation` ×3, `Kit.pen` (arrow, check, circle), `Kit.lowerThird` (reference), `Kit.chip` (schematic), `Kit.staircase` (`svg:` option, so it can breathe), the formula layer.
- **Changes from the visual** (all recorded in the script under "AS BUILT")
  - The rows are left-aligned under the dials. Straight leaders would have crossed the rows, so they are routed around them.
  - The knob sits right of the V dial, not under it: under it there was no room above the lower-third.
  - The SCHEMATIC chip is top-right: it did not fit at the end of the dial row.
  - `dial_y` is 290 and `dial_radius_px` is 110 (entry params changed).

### 04.2 Two whirlpools and a corridor (MEASURED, dense, 51.8 s real)

- **Built**
  - Phase map: Q across, D up. The axes are born from two mini dials (T1).
  - The trail fades and is shaded by polarity. A faint grey outline shows the last 300 units of A and of its mirror image, so the two whirlpools and their touching stay visible.
  - The mirror twin is drawn as S·A.
  - The knob uses the E1 threshold window `[last_zero, first_nonzero]` from the data. The integration uses the knob's own `value(t)`, so the dial and the dynamics agree.
  - A scrolling D(t) strip carries 600 units of pre-history, with the polarity strip below it.
  - The corner needle flips at the computed crossings. Pairs closer than 0.4 s cancel, so the needle's polarity stays right.
  - Sound: `needle` page events.
  - The PREDICT card sits in the right column.
  - On `barcode` the seafloor thumbnail appears: 00.3's `normal_Ma`, copied into `entry.params`, drawn grey at 40 %.
  - The starting state is a seeded search over 128 states on the D > 0 lobe at Γ = 0.80. With real timing, the first crossing falls 0.80 s after `flip` (0.64 s on the estimated timing).
- **Components:** `Kit.knob`, `Kit.needle` (corner), `Kit.pen` (circles, box), `Kit.lowerThird`, `Kit.chip`, `C4.dial`, `C4.predict`, `C4.model`, two `Kit.canvasLayer`s.
- **Finding for the writer and the reviewer:** "the outlines touch at the centre" is wrong for this model.
  - The passage from one lobe to the other runs round the outside of the lobes, at |Q| ≈ 2.5 and D ≈ 0, never through the origin.
  - The corridor is therefore drawn where the chosen path really crosses: a chalk guide along its first crossing after `touch`, drawn on `touch`.
  - The dot then follows that guide on `flip`.
- **Changes from the visual**
  - The PREDICT card is in the right column, not top centre, so the phase map stays visible during the hold. The knob fades under the card, and the corner needle stays visible.
  - The polarity strip keeps full opacity: dimmed, D > 0 looked like `--b-neg`. On `barcode` it gets a pen box instead.

### 04.3 Listen to the rate (MEASURED, 26.0 s real)

- **Built**
  - Part 1: a large central D(t) strip at Γ = 1 (live integration) scrolls at 40 units/s. A white tick drops into a tray at each crossing, with a counter and a heard `tick` page event.
  - Then the excursion, and the line '**crossing rate** = ticks per unit of time'.
  - Part 2: the strip drifts up and fades. The E1 plot follows: the 13 zero points land one by one (filled dots for training values), the threshold band appears, and the 0.865 point pops up with its callout.
  - The remaining 27 points then land left to right behind the solid curve, with the callout 'about 11 per 1,000 at Γ = 1.00'. Its numbers are rounded from the data.
  - A tick stream follows the rate of the latest point and pulses a ring on it.
  - The source lower-third and a formula layer with the exact rates complete the scene.
- **Components:** `Kit.plot` (axes, `curve`, `band` with `labelX`/`labelY`), custom landing dots, `Kit.pen` (`svg:` option), `Kit.chip`, `Kit.lowerThird` (source), the formula layer.
- **Finding for the writer and the reviewer:** "Not every tick is a flip: an excursion can cross and come straight back" has no real example in this model.
  - The script defines an excursion as two crossings less than 15 units apart.
  - At Γ = 1 (RK4, dt 0.01, 20,000 units) no two successive crossings are closer than about 29 time units, over 225 crossings. At Γ = 0.95 and 0.93 the minimum is about 30.
  - So the scene shows the schematic inset that the script prescribes for this case: a grey dashed frame, the chip 'SCHEMATIC · excursion' and two ticks. Nothing pretends the strip has one.
  - Short stays do exist: 44 of 225 gaps are under 40 units, a few turns on the other side and back. If wanted, the sentence could become "an excursion can cross, turn a few times, and come back".
  - R:528 also mentions "chattering" near zero. On the attractor, with this integrator, there is none.
- **Change from the visual:** the strip is large in the centre, not small at the top, so the counting reads.

### 04.4 Predict: when is the next flip? (MEASURED, 41.7 s real)

- **Built**
  - D traces of copy A and copy B, 10⁻⁶ apart, are revealed by a clip that follows model time. Time runs so that the horizon is reached at `lost+0.3`.
  - The gap is drawn on a log plot against the dashed reference δ0·e^{λt}, with a slope triangle '×e every 11 time units'.
  - Marks:
    - the horizon, on `lost`;
    - the Lyapunov time and the mean wait, on `wait`, with a bracket from the horizon to the wait;
    - two hops '+1 decimal ≈ +25' on `decimal`, never three, as the review asked.
  - The answer beat is a compact PREDICT card with B lit. The traces dim, and a faint amber histogram of D appears.
  - Every number on screen is derived from data:
    - the Lyapunov time is 1/0.089 → 11;
    - the horizon label is 11 ln 10⁶ → 150, as on the formula layer, while the mark sits at the exact 155;
    - the mean wait is 1/r_0(0.9) → 226 → '≈ 230';
    - one decimal is 11 ln 10 → 25.
- **Data:** the exponent was a hard-coded param, so I added `tools/data_ch04.py`, which writes `data/ch04_lyapunov.json`.
  - It reads the recorded output of P4 exercise 14: `# T = 4000 : exponents ≈ +0.089, -0.000, -1.070` at `en/prep/p4-systemes-dynamiques/index.qmd:1774`.
  - It also checks the exercise's `mu, nu, G = 0.119, 0.1, 0.9`.
  - Each output carries `meta` = {source, sha256, generator, extracted, stamp 'P4 · exercise 14 · Lyapunov exponents', anchor, note}. It is rewritten only when the content changes.
  - Nothing is recomputed.
  - In the script, `deps` and `entry.data.lyap` were added, and `params.lyapunov_exponent` was replaced by a pointer to the file.
- **Pair choice:** 64 seeded candidates (`entry.params.candidates`).
  - The score asks for the gap to first exceed 0.5 near the horizon, and for copy B's D to change sign soon after it.
  - That way "they disagree completely" shows on the D traces: B flips at about 185, A does not.
- **Components:** `Kit.plot` (log y axis, empty x label), `Kit.histogram` (faint), `Kit.needle`, `Kit.pen` (arrows), `C4.predict` ×2, `Kit.lowerThird`, the formula layer.

### 04.5 The long exposure (CONTEXT, dense, 30.7 s real)

- **Built**
  - Two (Q, D) panels with long-exposure glows: log-scaled light, `--b` for D > 0 and `--b-neg` for D < 0, on a 152 × 80 grid that is smoothed and blurred by 2 px.
  - Each panel has a live amber histogram of D drawn from the same visits.
  - The integration has two speeds: `units_per_s_slow` 25 until `same`, then a ramp to 400. Each copy first paints only its own lobe, as the narration says ("at first … the mirror image"). At a constant 400 units/s, both lobes would fill in about a second.
  - The starting states come from a seeded search for stays of the right polarity and length. Copy B starts at a random position within such a stay, so it is not the mirror of A.
  - The shutter icon opens on `shutter`.
  - On `same+1.5` the right histogram slides under the left one and becomes its outline: 'same glow, same humps'.
  - On `hist` the pen circles the two humps and underlines the empty middle.
  - On `name`, a caption and the Birkhoff reference lower-third.
  - On `below`, the inset at Γ = 0.80 shows one glow per start.
- **Components:** `Kit.canvasLayer` ×2, SVG histograms drawn by the scene (§4 item 6), `Kit.pen`, `Kit.chip` (Γ chips), `Kit.lowerThird`, the formula layer, `Scene.stepper` (the glow and the histograms accumulate on a fixed 1/120 s step).

### 04.6 The shoebox (MEASURED, 37.7 s real)

- **Built**
  - The empty film strip is on screen from frame 0. The 12 frames of a live trajectory (Γ = 0.93, one every 2 units) are exposed one by one, with 'time 0' … 'time 22' under them.
  - On `alike`, a pen box marks two neighbouring frames.
  - On `cut`, chalk cut lines appear and the frames separate.
  - On `shuffle`, the frames fall in seeded random order into the shoebox, the timestamps peel off and drift up, and the box shakes twice.
  - On `pour`, the box moves right of the map, tips, and pours the 8,000 reference snapshots of `e1_samples_0.93.json` into the map, with b / b-neg points at α 0.5.
  - A grey dashed contour of the glow comes from a marching-squares outline of the same snapshots, smoothed.
  - The label '8,000 snapshots · Γ = 0.93' is built from the data. The SIMULATED chip and the source lower-third accompany it.
  - On `photo`, snapshot 0 lifts out with its readings (1.27, −0.98, −0.20, from the data).
  - On `notime`, a pen crosses out the clock.
  - On `enough`, the map shrinks to the left, and the box and the equation card sit side by side.
  - On `tags`, three tags appear on their words, using the sentence's start and end. The last one is a dashed amber promise for chapter 05.
- **Components:** `C4.frame`, `C4.shoebox`, `C4.dial`, `Kit.pen` (box, cross), `Kit.chip`, `Kit.lowerThird`, `Kit.tex`, a canvas for the points, the formula layer.

### 04.7 Crowd laws (PROVED, 38.5 s real)

- **Built**
  - The small shoebox sits top-left. A photo card with its readings slides out of it.
  - An energy bar shows E = ½(Q² + D² + V²) from the readings.
  - On `rate`, an up or down arrow shows the photo's `dEdt`, a column computed by the extractor.
  - On `marble`, amber marbles drop into their bins: the first one, then 12 more, with the card switching photos (`tick` page events).
  - Then the remaining 7,987 rain down in seeded order. Bar height is the landed count over the largest final count, and the 13 marbles melt into the bars.
  - Out-of-range values (0.6 % and 0.5 %) collect into small edge markers instead of being dropped.
  - On `mean`, a marker at the sample mean computed in the scene (0.00018), 'mean ≈ 0', circled by the pen.
  - On `budget`, the amber main-layer formula E[dE/dt] = 0 with the tag 'true on average, not for each'.
  - On `bank`, a schematic ledger flashes for 3 s. Its daily flows are centred, so the balance comes back.
  - On `crowd`, the stack icon with 'law of the crowd', and one marble lifted out: the photo with the largest gaining dE/dt.
  - The photo and marble timings compress automatically if the narration leaves less room before `mean`.
- **Components:** `C4.shoebox`, `C4.frame`, an SVG histogram drawn by the scene, a canvas for the rain, `Kit.pen`, `Kit.chip`, `Kit.lowerThird`, `Kit.tex`, the formula layer.
- **Note:** the histogram is very peaked. That is the data: std 0.43 with heavy tails. "The pile spreads wide" reads through the tails and the edge markers.

### ch04.Q (no badge, 8.3 s real)

- **Built:** `Kit.questionCard(ctx, {chapter: 'ch04', category: 'runs', at: -0.4})`. The text, `n` (6) and who-to-ask come from the script.
  - Behind the card, at 10 %: 11 film frames with slowly varying, schematic readings, and the shoebox.
  - The chime comes from the script `sfx`.
- **Finding:** the visual said `Kit.questionCard(ctx, {n: 5, …})`, but the script's `question.n` is 6. In `cards.js`, opts override the script for `n`, so following the visual would have printed **Q5**. `n` is not passed (§4 item 4).
- **Finding:** the stub prints "Y. Ponty / D." on one line and "Lucor" on the next (§4 item 4).

## 3. Script fields changed (only `file`, `deps`, `entry`, `visual`; narration untouched)

- **04.1**
  - `entry.params`: `dial_radius_px` 110, `dial_y` 290, new `rest_deg`, new `knob_x`.
- **04.2**
  - `entry.params`: `seafloor_window_Ma`, `seafloor_normal_Ma` and `seafloor_source`, copied from 00.3.
- **04.3**
  - `entry.params`: `window_units`, `scroll_units_per_s`, `dt`, `transient_units`, `excursion_max_units`.
- **04.4**
  - `deps` gains `data/ch04_lyapunov.json`.
  - `entry.data` gains `lyap`.
  - `entry.params`: `lyapunov_exponent` replaced by `lyapunov_from`; `candidates` 64.
- **04.5**
  - `entry.params`: `units_per_s_slow`.
- **04.6**
  - `entry.params`: `dt`, `transient_units`, `seed`, `photo_index`.
- **04.7**
  - `entry.params`: `seed`.
- **ch04.Q**
  - `entry.params`: `bg_opacity`, `frames`.
- **Every scene:** the `visual` ends with an "AS BUILT (pilot, 2026-11-08)" paragraph listing the deviations. The writer's text before it is unchanged.

## 4. Shared components: problems and missing features (most urgent first)

1. **`runtime/scene.js`, `ctx.at`: a minus offset fails.**
   - **Problem:** the cue-name pattern `[A-Za-z_][\w.:-]*` swallows "-0.15", so `ctx.at('flip-0.15')` throws `unknown cue "flip-0.15"`. Only the `+` form works.
   - **Impact:** CONTRACT §3 and every script visual use the minus form ("lead the word by 120–200 ms"). Every builder hits this.
   - **Fix:** try an exact cue name first. Otherwise match `^([A-Za-z_]\w*(?:-[A-Za-z_]\w*)*)\s*([+-])\s*(\d+(?:\.\d+)?)$`; hyphenated cue names are allowed by P4.
   - **Workaround:** `C4.fixAt(ctx)` in `scenes/ch04/ch04_kit.js` wraps `ctx.at` the same way. Delete it once the runtime is fixed.
2. **`runtime/components/hud.js`, `Kit.badge`: the script's `badge.note` is ignored.**
   - Only `opts.note` is read, yet the consistency editor wrote notes into the scripts.
   - **Fix:** `note: o.note ?? (sb && sb.note)`.
   - **Workaround:** pass `note: ctx.script.badge && ctx.script.badge.note`.
3. **`hud.js`, `Kit.formulaLayer`: items pile up and the layer grows into the scene.**
   - Each item stays to the end, because `out` defaults to Infinity.
   - Long items wrap inside `max-width: 760px`.
   - With two or three items, the layer reaches up to y ≈ 640. It covered 04.2's polarity strip and 04.3's axis title.
   - Without an entry (preview), it throws instead of skipping.
   - **Fix:**
     - make the default `out` the next item's cue, with `stack: true` to opt back in;
     - fit each item (`Kit.fit`, at least 28 px, at most two lines);
     - return null when there is no item.
   - **Workaround:** `C4.formulas(ctx)`.
4. **`runtime/components/cards.js`, `Kit.questionCard`: opts override the script; the stub breaks initials.**
   - **Precedence:** `n: o.n ?? sq.n` and `chapter: o.chapter ?? sq.chapter` let opts override the script. CONTRACT says "`n` and `category` from opts unless the script has them", and `category` is already done that way.
   - **Fix:** `n: sq.n ?? o.n` (same for `chapter`).
   - **Stub:** `.qc-who` breaks "D. Lucor" after the initial.
   - **Fix:** `q.ask.replace(/\b([A-Z])\. /g, '$1. ')`, or one `nowrap` span per name.
5. **`runtime/scene.js`, `window.__QA__`: false positives and false negatives.**
   - **(a) False positive on inline boxes.** Inline `<em>` boxes on two wrapped lines of the question card overlap. Their content area (60 px font) is taller than `line-height: 1.14`, so every card reports 3 overlaps.
     - **Fix:** compare `getClientRects()` per line, shrunk by `(fontSize − lineHeight)/2`, or skip pairs inside one `.qc-q`.
   - **(b) Text scaled down by a transform is not flagged.** The font-size test reads the computed `font-size`, so text shrunk by a CSS or SVG transform passes. Example: 04.6's map letters during the shrink. I hid them myself.
     - **Fix:** scale by `rect.height / el.offsetHeight` for HTML, or by the CTM for SVG.
6. **`runtime/components/motifs.js`, `Kit.histogram`: no live mode.**
   - It is static: values are fixed at setup, and the bars only grow at the entrance.
   - 04.5 needs bars that accumulate with the visits, and a "slide under and become the outline" move. 04.7 needs a count that fills with falling marbles.
   - **Fix:**
     - a `live: (t) => counts` option, or `H.update(counts)`;
     - an `outline: true` mode;
     - an `edges: true` mode that collects out-of-range values into edge markers instead of dropping them, as the 04.7 script asks.
   - **Workaround:** both scenes draw their own bars (same look: amber, 1.5 px gaps, `--muted` baseline).
7. **Missing component: a PREDICT card.**
   - CONTRACT §3 defines predict beats, but the kit has no card. 04.2 and 04.4 both need one, and the outline has 1–2 predict beats per chapter.
   - **Proposal:** promote `C4.predict` (in `scenes/ch04/ch04_kit.js`) to `cards.js` as `Kit.predictCard`. It provides:
     - a mono 'PREDICT' kicker;
     - the question in Inter Display 44;
     - two grey outline buttons;
     - `answerAt` and `pick`, which light the chosen button and dim the other;
     - a compact variant (`question: ''`) for the answer beat.
8. **Missing shared motifs that later units reuse.**
   - The model integrator, the dial, the film frame and the shoebox (`C4.model`, `C4.dial`, `C4.frame`, `C4.shoebox` in `ch04_kit.js`) are needed by 05.2 ("Back to the shoebox"), 06.4 (violet photos dropping into the shoebox), 07.x (the three dials) and 09.x.
   - The script says the shoebox "must be reusable as is by 06.4 and 05.2".
   - **Fix:** move them to `runtime/components/` (or `scenes/_shared/`) as `Kit.threeModes`, `Kit.dial`, `Kit.photo` and `Kit.shoebox`.
   - Until then, other units can load `../ch04/ch04_kit.js`. But a file outside their own folder does not enter their render hash (build.js P3), so a promotion is the right fix.
9. **`runtime/theme.css`: no light vermillion for the quadrupole.**
   - `--b` at 60 % on NIGHT is about `--b-neg`, which breaks the polarity rule.
   - **Fix:** a token `--b-light` (≈ mix(--b, --fg, 0.6) = #EEA082 on NIGHT; a paper value too), a `.k-q`/`.k-b-light` class, and a KaTeX macro `\cq{}`.
   - The same need returns in 07.x and 09.x, wherever Q and D share a shot.
10. **`hud.js`, `Kit.chip`: one line only, no green kind.**
    - It is a single line with a fixed 46 px height. 'crisis in Γ: expected, not proved' and 'illustration · live integration of the model' (about 860 px) do not fit beside the content.
    - There is no green kind for "Γ = 0.93" chips.
    - **Fix:** a `maxWidth` option that wraps to two lines, and `kind: 'param'` (green outline and text).
    - **Workaround:** `.c4-chip-wrap` and `.c4-chip-param` in `scenes/ch04/ch04.css`.
11. **`motifs.js`, `Kit.knob`: label placement and a thin threshold window.**
    - The label sits at a fixed `R + 92` below the centre, far away on small knobs.
    - The threshold window [0.86, 0.865] is only 6.75° of arc, a 12-px blob at R 80.
    - **Fix:** a `labelDy` option, and a minimum arc length for the window (or a tick mark).
12. **`hud.js`, `Kit.lowerThird` (source): the line can wrap to a three-line block.**
    - 'source: experiences/resultats/e1_echantillons.npz · f44a28e7' wraps, and the box then rises to y ≈ 730.
    - **Fix:** print the basename, or fit l2 to one line (`Kit.fit`, at least 28 px).
13. **`equation.js`, `Kit.equation`: no extra macros.**
    - It cannot take extra macros (only `\term`), so `\htmlClass{k-q}{Q}` has to be written by hand.
    - **Fix:** pass an `o.macros` option through to `Kit.tex`.
14. **`cards.js`, `Kit.chapterCard`: the first frame is black.**
    - With `at: 0` the card fades in over 0.4 s, so the chapter's first frame is black.
    - **Fix:** document `at: -0.3`, or start fully visible when `at ≤ 0`.
15. **Undocumented, very useful: `Kit.pen({svg: <g>})`.**
    - The pen accepts any SVG parent, so a pen mark can ride with moving content: the 04.3 excursion circle scrolls with the strip.
    - Kit components with `parent:` can be grouped and transformed together (04.1's bench shrink).
    - **Fix:** document both in CONTRACT §4.

## 5. Pipeline notes (for foundation engineer A)

1. **`make check` writes into `audio/`.**
   - `tts.py --mode auto` writes placeholders into `audio/cache/placeholder/`, and `align.py` writes `audio/scenes/<id>.wav` and `.align.json`.
   - That is unsafe while the narration agent works in `audio/` at the same time.
   - I checked through an equivalent scratch script instead:
     - it runs `assemble_cut.py --unit ch04 --out <scratch>`;
     - it builds the timeline exactly as build.js does, either with align.py's estimated timing (146 wpm, 0.9 s breaks, holds) or by reading existing `audio/scenes/*.align.json` read-only when their sentence texts match the script;
     - then it calls `stills.js --timeline`.
   - **Proposal:**
     - `node build.js --unit ch04 --check --no-audio-write`, with an estimate fallback;
     - `--draft --unit ch04` (today `make draft` builds a whole cut);
     - the draft muxes the narration when it exists.
2. **`stills.js` check samples 0.6 s after each cue.**
   - It never sees the lead-in (04.1's chapter card) or the middle of long transitions.
   - **Proposal:** add one still in the middle of `lead_in` when it is longer than 1 s, and one at the end of the scene's longest transition.

## 6. Rules for the builders of the other units (learned here)

- Call the `ctx.at` shim first (or wait for fix 1). Write `'cue-0.15'` as the script does.
- Never start on a black frame. Give the base layout negative `at` times.
- Keep the formula layer one item at a time (`C4.formulas`), and budget the space for it: about 140 px tall for one wrapped item, bottom-right, from y ≈ 740.
- Plan the lower-third: a source lower-third is up to 3 lines tall (y ≈ 730–880). Keep content in that column above y 720 while it shows.
- Labels in the right column must stay left of x 1720 when the corner needle is used. Long badge notes take the top-right down to y 100, starting at x ≈ 1000.
- Live integrations must be seeded and re-run against the real cue times; when the narration says something precise about the timing, search for the starting state. Warn on failure, never fake.
- Check the model before drawing the visual's claim. Two claims here were wrong for this model: the corridor through the centre, and the 15-unit excursion.
- Box measurements (`Kit.box`, `E.box(id)`) work in `setup`. Group components with `parent:` to move them together.
- Polarity in canvases: `--b` and `--b-neg` at full alpha. Never dim a `--b` surface: it turns into `--b-neg`.

## 7. Files

- **Created:**
  - the 8 pages, `ch04_kit.js` and `ch04.css` in `scenes/ch04/`;
  - `tools/data_ch04.py`;
  - `data/ch04_lyapunov.json`;
  - this file.
- **Edited:** `script/ch04.json`, only in `deps`, `entry` and `visual` (§3).
- **Outputs (not tracked):**
  - `out/check/unit_ch04/` (estimated timing);
  - `out/check/unit_ch04_real/` (real narration timing);
  - `out/draft/unit_ch04/` (per-scene drafts, `unit_ch04_draft.mp4`, `unit_ch04_draft_real.mp4` with narration).
- **Not touched:** `runtime/`, `audio/`, narration text, other units.

## Review (adversarial visual and accuracy review, 2026-11-08)

### R0. Method

- **Stills:** one per cue (cue + 0.6 s), plus the first and last frames, on both timings. The real timing comes from `audio/scenes/*.align.json`, read only; the estimated timing is the 146 wpm estimate. The scratch equivalent of `make check` writes nothing into `audio/`, and its outputs are `out/check/review_unit_ch04{,_real}/`.
- **Extra stills** at 1080p cover the lead-in, the middle of every transition, and the words the narration times precisely. For those words, the speech spans of `audio/scenes/04.2.wav` and `04.3.wav` were measured (energy envelope, read only).
- **Draft with narration:** `out/draft/review_unit_ch04/unit_ch04_draft_real.mp4` (4:29). Frames were extracted in the middle of the moves. A frame-difference scan, with an A-B-A flicker test, finds no flicker; the largest jumps are the deliberate moves.
- **Determinism, with the real script entry injected:** a direct seek gives the same frame in two fresh browsers for all 8 scenes (PNG SHA-256 identical). Sequential arrival differs only by anti-aliasing (04.1: ≤ 3 030 px, at most 9 levels; elsewhere: ≤ 271 px, up to 63 levels on pen, knob and needle edges), after the 04.3 fix below.
- **Performance** (wall clock, 15 fps sequential pass, IPC included). Setup time: 0.13–0.46 s, except 04.2 at 1.5 s (see the 04.2 fix). Median seek: 1–8 ms; 04.5 is 18 ms (p95 46 ms, dense class, budget 60). Draft capture runs at 46–72 fps.
- **Numbers on screen** were checked against `experiences/resultats/digest.md`, `data/e1_finegrid.json`, `data/e1_samples_0.93.json`, `data/ch04_lyapunov.json` and the cited site lines:
  - r₀(0.865) = 0.00194; r₀(0.9) = 0.00442, so the mean wait is 226; r₀(1.00) = 0.0112 (data 0.01125, digest 0.0112);
  - the threshold window is 0.86 / 0.865;
  - Lyapunov exponent 0.089 at Γ = 0.9 (P4:1774), so 11 and ln 10⁶ × 11 ≈ 150;
  - snapshot 0 = (1.27, −0.98, −0.20);
  - dE/dt: mean 0.00018, std 0.43, 52 % positive;
  - the 5 000 and 40 snapshots per point of the question card (these.md:912, palier2_tg3d.yaml).
  
  All of them are right. No number of a SCHEMATIC file appears on screen.

### R1. Problems found and fixed (in `scenes/ch04/`, plus one `entry.params` value in `script/ch04.json`)

| # | Scene | Problem (evidence) | Fix |
|---|---|---|---|
| 1 | 04.2 | **Cue mismatch on the key event.** The first crossing (needle flip + `needle` sound) fell 0.8 s after the start of the `flip` sentence, at 30.3 s, while the narrator says "The state lingers on one side". The words "The dipole flips" come at 33.45–34.85 (speech spans measured on `audio/scenes/04.2.wav`). | The crossing window is now a fraction of the `flip` sentence (`params.first_flip_frac` [0.58, 0.8]). The old seconds rule stays as the fallback in preview. The needle now flips at 33.31 s, 0.14 s before "The dipole flips". |
| 2 | 04.2 | **The flip undid itself.** The new pick crossed back within a second, so at `predict` the dot was back on the D > 0 side. | The search keeps starts that stay on the new side until `irregular`. It runs up to three rounds of `candidates`, because most starts cross during the knob's turn (see R3). Setup is now 1.5 s. |
| 3 | 04.2 | **Polygonal trajectory at Γ = 1.** The trail was linearly interpolated between scene samples 0.375 model units apart at 90 units/s, and stepped every 0.12 units, so the excursions showed straight sides 50–110 px long. | Every RK4 step is recorded (fine path). The trail, outline, dot and corridor guide are drawn from it, with 2.5 px / 4 px decimation and strokes batched by colour and age. Median seek is 8 ms. |
| 4 | 04.2 | **Trajectory through the axis label.** The Γ = 1 attractor (\|Q\| up to 2.8) runs through "Q · quadrupole", and the labels sat *under* the canvas (no z-index; the canvas is z 8). | The map labels are at z 30 with a background-coloured halo. The "corridor" label now sits inside the loop: it was on the chalk guide. The guide and its label leave 1 s after the actual crossing, instead of at the fixed `flip+2.5`. |
| 5 | 04.2 | **Answer beat too short.** "B · irregular" was lit for only 0.5 s before the card left. | The card stays until `irregular+1.2`, and the knob comes back afterwards. |
| 6 | all | **Formula layer broke inside relations:** "Γ ≤ \| 0.86", "Γ = \| 0.9", "16 runs × \| 3000 units", "≈ \| 11". | `C4.formulas` now calls `C4.fitFormulas`. An item wider than the layer is split at its most balanced separator (`;` `:` `,` + space, top level or inside `\text{}`, or `\quad`), one KaTeX line per half, and shrinks to ≥ 28 px if needed. Items that fit are untouched. |
| 7 | all | **"north - south", "four - pole", "three - mode model", "long - exposure".** `theme.css` sets `font-feature-settings: "tnum"` on the stage, and Inter's tabular hyphen is a figure wide: 577 px against 529 px for "north-south 0.119" at 64 px. | `C4.nbhy(stage)`, called last in every setup, swaps a hyphen between letters for U+2011 outside KaTeX. U+2011 is present in Inter and JetBrains Mono. |
| 8 | 04.3 | **Late payoff.** The Γ = 1 point and the "about 11 per 1,000" callout landed at 24.5–24.7 s, after "about eleven" starts (24.2 s). | The sweep ends at 55 % of the `grows` sentence. The callout comes at 62 % (24.04 s, 0.16 s ahead of the word). |
| 9 | 04.3 | **Non-deterministic canvas state.** The tick loop left `lineCap = 'round'` behind, so the strip (dashes, trace caps) depended on seek history: 7 131 px differ, max 224 levels. | The context state is reset at the start of each frame. 4 corner pixels remain (anti-aliasing). |
| 10 | 04.3 | **Preview crashed** (`make serve`): `ctx.at('_tail')` exists only in a built entry. | `ctx.cue('_tail', duration − 0.8)`. |
| 11 | 04.4 | **Unlabelled amber histogram inside the log gap plot** at the answer beat. It read as data on the gap axes ("Only the statistics survive" had no readable picture). | It is now a marginal histogram of D on the right end of the D panel: bars along D, on a background mask, labelled "D · long run" in amber. The "one example pair" chip leaves first. |
| 12 | 04.4 | **"time (model units)" stacked on "Lyapunov time ≈ 11", on the same row as "+1 decimal ≈ +25".** It read as one block. | The x title is at the axis end, right-aligned under 250–300. |
| 13 | 04.4 | **PREDICT card over the D panel during the 9 s question and hold.** The two dots, the subject of the question, were hidden; the lower 70 % of the frame was empty. | The question card sits at y 400, in the empty middle, and leaves at `together-0.6`, before the plot comes in. |
| 14 | 04.5 | **The D axis label sat at the bottom (negative) end** of both panels. | It is now at the top. |
| 15 | 04.5 | **The name caption "the long-exposure glow (stationary distribution)" ran across panel A's D axis and over the glow.** | It moved to the right column on two lines, in place of "same glow, same humps", and gives way to the `below` caption. "copy A" stays. |
| 16 | 04.5 | **For 7.6 s one small panel sat top-left and the right 60 % of the frame was empty.** | Panel A (canvas, frame, histogram, labels, shutter) starts centred and slides to its place as copy B arrives (T1, 0.8 s). |
| 17 | 04.6 | **Film strip at y 124–332, leaving 70 % of the frame empty for 10 s.** "a snapshot carries no timestamp and no time order", the line of the sentence, was 30 px `--fg-2` with "order" alone on line 3. | The strip is at y 256–458 and clears the box rim. The `notime` line is 34 px `--fg`, balanced on three lines. |
| 18 | 04.6 | **Four key colours in the `tags` shot:** b, u, param (green Γ in the equation card) and the amber "chapter 05" tag. | Γ is plain in the card. |
| 19 | 04.7 | **"The pile spreads wide" over a spike.** The axis ±1.6 is 3.7 σ, while half the photos have \|dE/dt\| < 0.1 (IQR −0.088…0.102, 1–99 % = −1.12…1.0), so the histogram read as "each photo ≈ 0", the opposite of the scene's point. | `entry.params.range` is now [−0.6, 0.6] (script and scene default). The bars show the spread, and the 2.7 % beyond fall into the existing edge markers. The crowd icon is placed by fraction, and the lifted marble's label is clamped inside the safe area. |
| 20 | 04.7 | **The pen ellipse round "mean ≈ 0" touched the "true on average, not for each" tag.** A first attempt moved the tag and overlapped the big equation (QA). | The mean label and ellipse are 12 px lower, and the mean line starts under the label. |
| 21 | ch04.Q | **The stub read "Y. Ponty / D." then "Lucor".** | A no-break space after the initials, in the page. The shared fix stays wanted (R2 4). |
| 22 | 04.1 | **The chapter card was still fading while the dials faded in:** a 3-frame double exposure. The D-row leader ran through the letters of "north-south". | The card leaves at `caricature-0.55`, and the leader stops left of the label. |

The checks after the fixes:
- Both timings: 8/8 scenes, 0 page errors.
- Warnings:
  - 04.3: the intended schematic-excursion warning only.
  - ch04.Q: the 3 known `__QA__` inline-box false positives only.
- Preview (no entry): every page renders, except ch04.Q, where `Kit.questionCard` needs the script (R2 7).

### R2. Shared component issues (runtime/, runtime/components/, pipeline), with evidence

1. **`runtime/theme.css` — global `font-feature-settings: "tnum"` widens every hyphen in Inter.**
   - Evidence: R1 7, measured on the vendored Inter-Medium.otf. The en dash is unaffected.
   - It hits every unit ("three-mode", "long-exposure", "x-axis"…).
   - Fix: drop tnum from `body`. Apply `font-variant-numeric: tabular-nums` only where figures must align (`.kt-tick`, counters, readouts), or have `Kit.markup`/`Kit.el` text use U+2011.
2. **`hud.js` `Kit.formulaLayer` — KaTeX can only wrap after a relation or operator, so long items break inside "Γ ≤ 0.86" or "16 runs × 3000".**
   - Evidence: R1 6; stills in `out/check/unit_ch04_real/04.2_02340_touch.png`, `04.3_02300_grows.png`, `04.4_01860_apart.png` of the pilot run.
   - Fix: adopt `C4.fitFormulas` / `C4.breakCandidates` from `scenes/ch04/ch04_kit.js`.
   - This adds to the builder's item 3 (one item at a time, fit, null without items).
3. **`runtime/scene.js` `ctx.at` minus-offset bug: confirmed.** The regex `^\s*([A-Za-z_][\w.:-]*)…` takes "flip-0.15" as the cue name (`scene.js:215`). `C4.fixAt` is still needed.
4. **Confirmed as reported:**
   - the `Kit.badge` script note is ignored (`hud.js:43` reads only `o.note`);
   - `Kit.questionCard` lets opts override the script's `n` and `chapter` (`cards.js:63`);
   - `.qc-who` breaks after an initial (R1 21).
5. **Canvas state leaks between frames are not caught by the tools.**
   - `tools/determinism.js` runs pages **without** `__ENTRY__`, so it tests preview cues and misses timing-dependent code paths (04.2's search, 04.3's sentence-relative timing). It also prints only hashes, so anti-aliasing and real differences look the same.
   - The 04.3 leak (R1 9) passed the builder's run.
   - Fix:
     - give it `--entry` (or `--timeline`, as in `stills.js`) and a differing-pixel count with max delta;
     - have `Kit.canvasLayer` offer `g.reset()` (Canvas 2D `reset()`) or reset the state at each render.
6. **`window.__QA__` blind spots:**
   - text crossed by Canvas data (the Γ = 1 trajectory through "Q · quadrupole", R1 4);
   - pen or SVG shapes touching text boxes (R1 20);
   - labels hidden *under* a canvas layer: `Kit.canvasLayer` z 5–8 sits above `Kit.el` labels that have no z-index, and nothing warns.
   
   Fix:
   - give labels created by `Kit.el` / `Kit.chip` a default z above content layers, or document the z ladder in CONTRACT §7;
   - add a QA pass that samples Canvas pixels under text boxes.
7. **Preview without an entry:**
   - `_tail` and `_speech_end` are unknown cues in preview, so a scene that uses them throws (R1 10). Fix: the runtime defines them from `duration`.
   - `Kit.questionCard` throws without a script `question`. Fix: render a placeholder ticket in preview, so `make serve` works on `chXX.Q` pages.
8. **`stills.js` check mode** samples only cue + 0.6 s. Every transition problem in R1 (1, 5, 13, 16, 22) was invisible there. This supports the builder's pipeline item 2.
   - Proposal: add a still at each cue −0.2 s, one in the lead-in, and an optional `--every 1.0`.
9. **`motifs.js` `Kit.knob` window:** the 6.75° window [0.86, 0.865] is still unreadable at R 80 (builder's item 11). A tick and "0.86" at the window would let the knob carry the threshold the narration names.

### R3. Notes for the writer and the other builders (not fixed here)

- **A fast Γ ramp alone makes flips in this model.**
  - Of 128 starts on the Γ = 0.80 whirlpool, 64 cross D = 0 within 1.5 s of the start of the 3 s turn to 0.86, while Γ is still ≤ 0.86.
  - At that Γ the stationary regime has no crossing at all. These are transients: the state is off the new attractor.
  - 15 more cross during the step to 0.87.
  - 04.2 selects a start that does not. Any later scene that turns a knob over a live integration (05.x, 07.x, X-modules) must do the same, or narrate the transient.
- **04.7, at `rate`–`mean`, has four key colours.** The formula layer's `\Gam` (green) joins b, u (photo dials) and amber (marbles). The fix is writer-side: write `\Gamma` in that `onscreen.formulas` item.
- **04.1: the formula layer's `\cb{Q}` is full vermillion,** while the scene's Q is the light quadrupole vermillion. Writer-side: `\htmlClass{k-q}{Q}`, or a shared `\cq` macro (builder's item 9).
- **Still weak, not changed:**
  - 04.4's 5.6 s `twins` shot is sparse: only the D panel, with two dots at its left edge.
  - The SCHEMATIC chip of 04.1 sits 7 px above the third dial's bezel.
  - 04.3's excursion is schematic, the honest choice given the builder's finding; the sentence still claims "come straight back".

### R4. Files

- **Changed:**
  - `scenes/ch04/ch04_kit.js` (`C4.fitFormulas`, `C4.breakCandidates`, `C4.nbhy`);
  - all 8 pages (every edit marked `REVIEW`);
  - `script/ch04.json`: only 04.7 `entry.params.range`, from [−1.6, 1.6] to [−0.6, 0.6]. Narration, `visual` and the other fields are untouched.
- **Outputs:**
  - `out/check/review_unit_ch04/` (estimated timing);
  - `out/check/review_unit_ch04_real/` (real timing);
  - `out/draft/review_unit_ch04/unit_ch04_draft_real.mp4` (narration muxed, read only from `audio/scenes/`).
- **Not touched:** `audio/`, `runtime/`, the pipeline, data files.
