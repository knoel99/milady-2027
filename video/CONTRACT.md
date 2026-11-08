# Scene contract — how a scene builder writes a scene

For the scene builders of *How Often Does the Field Flip?* and for the visual reviewers. `BRIEF.md`
wins over this file; this file wins over `plan/styles.md` and `plan/pipeline.md` for anything about
how a scene page is written. Owner of everything here except the last section ("Pipeline"):
foundation engineer B (`runtime/`, `runtime/components/`, `tools/data_*.py`).

Quick look at every component: `scenes/_gallery/gallery.html` (16 plates of 8 s; open it in a
browser, `?plate=K` starts at plate K, key `g` shows the safe area) and its stills in `out/gallery/`.

---

## 1. One scene = one HTML page

- **File**: `scenes/<unit>/<id>_<slug>.html`, the scene id with `.` → `_`, a short lowercase slug:
  `scenes/ch04/04_3_listen_to_the_rate.html`, `scenes/ch04/04_Q_question.html`, `scenes/X1/X1_2_inside_the_box.html`.
  The same path goes in the script (`"file"`). One scene per file, no shared page between scenes.
- **Stage**: 1920 × 1080 CSS px, `<div id="stage"></div>`, everything inside it.
- **Boilerplate** (paths are relative to `scenes/<unit>/`; drop the lines you do not use):

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>04.3 Listen to the rate</title>
<link rel="stylesheet" href="../../vendor/katex/katex.min.css">   <!-- only with equations -->
<link rel="stylesheet" href="../../runtime/theme.css">
<script src="../../vendor/katex/katex.min.js"></script>             <!-- only with equations -->
<script src="../../runtime/scene.js"></script>
<script src="../../runtime/components/kit.js"></script>            <!-- always, before the others -->
<script src="../../runtime/components/hud.js"></script>            <!-- badge, lower-third, rail, formula layer, chip -->
<script src="../../runtime/components/plot.js"></script>           <!-- SVG plots (seat.js needs it) -->
<script src="../../runtime/components/field.js"></script>          <!-- Canvas fields, maps, tracers -->
<script src="../../runtime/components/equation.js"></script>       <!-- KaTeX equation builder -->
<script src="../../runtime/components/motifs.js"></script>         <!-- M1–M10 (cards.js needs it) -->
<script src="../../runtime/components/cards.js"></script>          <!-- chapter card, question card -->
<script src="../../runtime/components/seat.js"></script>           <!-- empty seat (pending results) -->
<style> /* scene-specific CSS only: no colours outside the tokens, no transitions, no animations */ </style>
</head><body><div id="stage"></div>
<script>
Scene.define({ /* §2 */ });
</script></body></html>
```

Three.js (`vendor/three/three.module.min.js`, r160, `addons/` for `Line2`) and GSAP
(`vendor/gsap/gsap.min.js`, paused timelines only) are the only other libraries. Nothing from a CDN.

## 2. `Scene.define({...})`

```js
Scene.define({
  duration: 30,                              // preview only: the build injects the real duration (audio)
  register: 'night',                         // preview default; the script's "register" wins (night | paper | blueprint)
  cues: { rate: 1.2, predict: 9.5, answer: 14 },   // EVERY cue name the scene uses, with a preview time
  data: { rate: 'data/e1_finegrid.json',            // "data/…" resolves from the video root at any depth
          seat: { url: 'data/palier2_abc3d.json', optional: true } },   // optional: may be absent
  params: {},                                // free parameters (the script's entry.params override them)
  setup(ctx) { /* build everything once: DOM, SVG, KaTeX, components, precomputed geometry */ },
  render(t, ctx) { /* optional: what the components do not do; a pure function of t */ },
});
```

`ctx` (in `setup` and `render`):

| field | meaning |
|---|---|
| `ctx.at(spec)` | time spec → seconds: `2.5`, `'rate'`, `'rate+0.4'`, `'rate-0.15'`, `{cue: 'rate', dt: 0.4}`. Unknown cue = scene error. |
| `ctx.cue(name, fallback)` | legacy helper of the prototype (no error on unknown names) |
| `ctx.data.<name>` | parsed JSON (or `null` for an optional / pending file) |
| `ctx.status`, `ctx.variant` | `ready`/`pending`; `pending`/`result` (which narration variant and which seat to draw) |
| `ctx.script` | the script entry injected by the build: `badge`, `level`, `register`, `onscreen` (`formulas`, `chips`, `labels`, `title`), `question`, `unit`, `id`, `sentences`, `sources` |
| `ctx.params`, `ctx.stage`, `ctx.duration`, `ctx.register` | as named |
| `ctx.add(component)` | register something with `render(t)`; kit components do it themselves |

Runtime helpers on `Scene`: `seg(t, a, b, ease)` (eased progress), `ease.{linear, inOutCubic, outCubic, inOutSine, smooth}`,
`spring(p, overshoot=0.03)` (closed form, ≤ 3 % overshoot for physical objects), `stepper(init, step, dt)` (fixed-step
simulation, identical frames whatever the seek order), `rng(key)` (independent seeded stream), `f32(packed)` (decode a
packed array of a data file), `col('b')` (token value for Canvas, register-aware), `hidpi(canvas, w, h)`, `url(path)`.

## 3. Time and cues

- The scene animates on **cue names from the script** (`"cue"` of each sentence), never on absolute times.
  The build also injects `s_<sentence id>` for every sentence, `_speech_end` and `_tail`.
- Declare every cue you use in `cues` with a believable preview time. If the script lacks one, the runtime
  warns (`window.__SCENE_WARNINGS__`) and the preview time is used: fix the scene or ask the writer.
- Visual events lead the word by 120–200 ms: `ctx.at('flip-0.15')`. Offsets after a cue are fine (`'eqs+0.4'`).
- Predict beats: the question appears on its cue and the answer on the next paragraph's cue; the hold is the
  script's `hold_after`, never a number in the scene.
- Durations of motion: labels and chips 0.15–0.25 s, terms 0.4–0.7 s, scene morphs 1.2–2.5 s. No bounce;
  `Scene.spring` only for needles and knobs.

## 4. Components (all in `runtime/components/`, all deterministic and cue-driven)

Every factory is `Kit.<name>(ctx, opts)`, called in `setup`. Common options: `at` (entrance, time spec),
`out` (exit, time spec, default: stays), `parent` (mount point, default the stage). Each returns an object with
`root` and `render(t)`; the runtime renders it on every seek before your `render`.

### HUD — `hud.js`

```js
Kit.badge(ctx, { note: 'E1 · 2 seeds' });                 // kind/confidence from the script's "badge"
Kit.badge(ctx, { kind: 'CONJECTURE', confidence: 'medium' });   // preview fallback (the script wins, a mismatch warns)
Kit.lowerThird(ctx, { kind: 'source', data: ctx.data.rate, at: 'rate+0.5', hold: 5 });
Kit.lowerThird(ctx, { kind: 'reference', l1: 'Reference', l2: 'Gissinger 2012', at: 'model' });
Kit.lowerThird(ctx, { kind: 'chapter', l1: 'Level 2 · chapter 4', l2: 'Chaos and the shoebox', color: 'param' });
Kit.lowerThird(ctx, { kind: 'stamp', l1: 'Regenerable · pending', l2: 'Re-rendered when palier2_abc3d arrives' });
Kit.rail(ctx, { from: 'L1', to: 'L2', at: 0.3, hold: 3 });   // M8: chapter cards and checkpoints only
Kit.formulaLayer(ctx);                                        // the script's onscreen.formulas [{cue, tex}] (D8)
Kit.formulaLayer(ctx, { label: 'Formula · R:514', items: [{ tex: 'r_0 = …', at: 'rice', out: 'check' }] });
Kit.chip(ctx, { text: 'illustration, not to time scale', kind: 'plain', x: 960, y: 820, anchor: 'c', at: 'flip' });
```

- **Badge kinds**: `MEASURED` (E1–E3 results), `PROVED` (a proposition of the report), `CONJECTURE` + confidence
  `high | medium | low`, `PLANNED` (PhD plan), `CONTEXT` (external sourced fact), `SCHEMATIC` (metaphor, no numbers).
  Top-right, one per scene; on every claim-bearing scene.
- **Lower-thirds**: four kinds (chapter tag, source chip, reference chip, regenerable stamp), one at a time (the
  runtime warns on overlap), bottom-left, line 1 mono capitals, line 2 Inter 32 px. `kind: 'source'` with `data`
  fills itself from the data file's `meta.stamp`, `meta.source` and the first 8 digits of its SHA-256.
- **Chip kinds**: `''` (simulated, white), `generated` (violet), `schematic` (grey dashed), `measured` (pill), `plain`.
- **Formula layer** (bottom-right): full statements in small type; never narrated, never in subtitles.

### Cards — `cards.js`

```js
Kit.chapterCard(ctx, { num: '04', title: 'Chaos and the shoebox of photographs', level: 'L2', levelFrom: 'L1', tier: 0, pending: [3, 4], at: 0.3 });
Kit.questionCard(ctx, { n: 4, chapter: 'ch04', category: 'runs', at: 'q', whyAt: 'why', unblocksAt: 'unblocks' });
```

- **Chapter card (T4)**: dipole field lines sweep in behind the title, chapter number in mono, title in Inter Display
  ExtraBold (fitted to two lines), staircase (M7) with the current tier lit and pending tiers dashed, rail (M8)
  climbing `levelFrom → level`. 3–5 s.
- **Question card** (`chXX.Q`, 6–10 s): the warm "ticket" with a perforated stub (`ASK`, `Q<n>`, chapter, who to ask),
  the question (≤ 18 words, `*word*` gets a graphite underline), WHY IT MATTERS, WHAT IT UNBLOCKS with a category tag:
  `runs` (which simulations, which parameters), `framing` (constraints, metrics, success criteria), `logistics`
  (data access, lab GPUs, Jean Zay, budget). Text comes from the script's `question` (`en`, `why`, `unblocks`,
  `ask_who`); `n` and `category` from opts unless the script has them. Too long = warning, then shorten. The card
  fills the frame: no lower-third, formula layer or seat beside it (the badge is optional: a question makes no claim).

### Equations — `equation.js` (KaTeX)

```js
const E = Kit.equation(ctx, { x: 960, y: 260, size: 84,
  tex: '\\term{lhs}{\\frac{\\partial \\B}{\\partial t}}\\term{eq}{\\;=\\;}\\term{adv}{\\nabla\\times(\\U\\times\\B)}\\term{plus}{\\;+\\;}\\term{diff}{\\etaP\\,\\nabla^{2}\\B}',
  reveal: [['lhs', 'eqs'], [['eq', 'adv'], 'stretch'], [['plus', 'diff'], 'smudge']],   // narrative order, on cues
  labels: [{ id: 'adv', text: 'carried and stretched by the flow', color: 'u', at: 'stretch+0.3' }],
  focus: [{ ids: ['adv'], at: 'race', out: 'ratio' }],   // other terms drop to 35 %
  ghost: false });
Kit.morph(ctx, { from: E, to: E2, at: 'rewrite', dur: 1.0 });   // T6: create E2 with at = the morph cue, register morph last
```

Macros (colour by role): `\U \B \Rm \etaP \Gam \RE \PM \Po \vth \Edist`, and `\cu{} \cb{} \cp{} \cm{} \ck{} \cg{}`
(velocity, field, parameter, model, metric, grey). `\term{id}{…}` makes a term addressable (`E.box(id)` gives its box).
Never redefine a built-in (`\eta` → use `\etaP`). Labels: at most two on screen (warned). Display size 64–96 px.

### Plots — `plot.js` (SVG)

```js
const P = Kit.plot(ctx, { box: { x0: 260, x1: 1640, y0: 200, y1: 620 }, at: 'rate',
  x: { label: 'Γ, control parameter', min: 0.8, max: 1.0, ticks: [0.8, 0.85, 0.9, 0.95, 1.0], param: true },
  y: { label: 'crossings of D per unit time', min: 0, max: 0.018 } });
P.fromData(ctx.data.rate, { at: 'rate', gen: 'model', only: ['simulation (counted crossings)', 'Rice, generated (model C)'] });
P.band({ x: [0.86, 0.865], kind: 'window', label: 'threshold' });      // window (green 12 %) | success | floor
P.hline({ y: ctx.data.ev.noise_floor.n_gen.energie, label: 'noise floor' });   // dashed grey floor line
P.errorbars({ x, lo, hi, field: 'metric' }); P.dots({ x, y, filled }); P.legend(rows, { x, y, row: true });
```

Curves draw on left to right (clip), simulated solid, generated dashed (16/11), ghost (READY anchor) grey dotted;
training values filled dots, test values open dots; `y.log: true` for decades (labels 10⁻³…). The y title sits
horizontally above the axis. Tick labels that would touch are dropped. Keep `y1 ≤ 640` when a lower-third or the
formula layer will show (the x title sits 96 px under the axis).

### Fields — `field.js` (Canvas)

```js
Kit.fieldMap(ctx, { grid: Scene.f32(M.variants.ref.samples[0].j), kind: 'b', vmax: M.vmax.j, x: 160, y: 190, w: 500, h: 500, label: 'current j · simulated' });
Kit.fieldMap(ctx, { grid: …V4…, kind: 'b', vmax: M.vmax.j, generated: true, … });   // violet frame = generated
Kit.fieldLines(ctx, { F, seeds, box, color: 'b', at, dur });   // RK4 streamlines, precomputed, drawn on
Kit.arrows(ctx, { F, box, nx: 12, ny: 8, color: 'u' });      Kit.tracers(ctx, { F, box, n: 600, trail: 10, color: 'u' });
Kit.cmap('u' | 'b', v)  // the key colour map: silver (−) → background (0) → hue (+), symmetric in lightness
```

`F(x, y) → [vx, vy]` in stage px (px/s for tracers), a pure function. Use the same `vmax` for every variant of a
comparison (the data files give it). Show the chip `display interpolation (spectral) · native grid 32²` on E2 maps.

### Motifs — `motifs.js`

| motif | call | notes |
|---|---|---|
| M1 needle | `Kit.needle(ctx, { flips: ['flip'], corner: false })` | big compass or the corner needle (`corner: true`, only while D is on screen); a flip is 180° with ≤ 3 % overshoot |
| polarity strip | `Kit.barcode(ctx, { box, series: { t, D }, label })` | sign runs of D in two shades of vermillion |
| M2 knob | `Kit.knob(ctx, { min, max, window: [lo, hi], label: 'Γ', keys: [{ at, v }, { at: 'turn', v: 0.93, dur: 1.4 }] })` | green pointer, threshold window shaded green |
| M3 two inks | `Kit.twoInks(ctx, { box, cells: [4, 2], amp: 200, run: 'stretch' })` | blue cellular flow carries a vermillion material line (stretch, fold); SCHEMATIC |
| M4 cloud | `Kit.cloud(ctx, { box, range, targets: [{ pts, at, dur }], strings: 120 })` | violet points on straight paths from a seeded Gaussian; several targets = conditioning |
| M5 histogram | `Kit.histogram(ctx, { box, values, ref, range, bins: 31, morph: { values, at } })` | amber bars, reference outline; the morph to a spike is clipped "↑ off scale" |
| M6 projector | `Kit.projector(ctx, { drop: 'project', field: 'b', gauge: { label: '∇·B', value } })` | the gauge value comes from data |
| M7 staircase | `Kit.staircase(ctx, { lit: 2, pending: [3, 4] })` | tiers 0–4: three modes, 2D square, 3D box, VKS cylinder, precessing cylinder |
| M9 pen | `Kit.pen(ctx, { kind: 'circle' | 'underline' | 'box' | 'brace' | 'arrow' | 'check' | 'cross', target: el | box, at })` | chalk, drawn on, seeded hand wobble |
| M10 mirror | `Kit.mirror(ctx, { mode: 'plane' | 'point', reflect: 'mirror' })` | `point`: S = diag(−1, −1, 1) sends (Q, D) to (−Q, −D) — a point reflection in the (Q, D) plane, not a line mirror; use `plane` only as the B → −B metaphor |

### Text helpers — `kit.js`

`Kit.upper(text)` capitals for mono labels **without touching symbols** (Greek letters and `{sym}…{/}` keep their
case: CSS `text-transform` would turn ω into Ω, η into Η, j into J — it is not used anywhere). `Kit.markup(text)`:
`{u}…{/} {b}…{/} {param}…{/} {model}…{/} {metric}…{/}` key colours, `*…*` pen target, `$…$` inline KaTeX.
`Kit.fmt(x, sig)` numbers with U+2212 minus and × 10ⁿ; `Kit.pow10(v)`; `Kit.fit(el, w, h, min)` shrinks to fit, never
below 28 px (warns); `Kit.tex(tex)`; `Kit.el`, `Kit.s` (SVG), `Kit.svgLayer`, `Kit.canvasLayer`, `Kit.box(el)`.

## 5. Data

Scenes never read the repository: `tools/data_existing.py` (READY results) and `tools/data_cloud.py` (cloud results)
write `data/*.json`. Every file has `meta = {source, sha256, generator, extracted, stamp, note, sources?}`; the stamp
(≤ 44 characters) is the source lower-third's first line. Big arrays are packed `{dtype: 'f32', shape, b64}`: decode
with `Scene.f32(x)` (a `Float32Array` with `.shape`). **No number is typed in a scene**: every number on screen is
read from a data file (or is an axis bound or tick of a known parameter range).

Refresh: `python3 -I tools/data_existing.py` (`--check` to see what would change; unchanged content is not rewritten).

| file | content | scenes |
|---|---|---|
| `e1_finegrid.json` | 41 Γ: counted crossings of D, Rice on reference / model C / model F (curve schema), bridge masses, threshold (0.86 → 0.865), config | 04.3, 05.3, 09.1–09.3 |
| `e1_data_rates.json` | the 21 data Γ: crossing rate, Rice reference, P(\|D\| < 0.25), P(D > 0) of the training data | 04.3, 07.1 |
| `e1_eval.json` | per variant (A, B, C, C short, D, E, F, F0, halves): per-Γ metrics (seed mean and spread), train/test means, noise floors | 07.3–07.6, 09.4, X3.2 |
| `e1_samples_<Γ>.json` (0.85, 0.87, 0.9, 0.93) | snapshots (Q, D, V) of the reference (8000 at 0.9) and of the variants (4000), plus Ḋ and dE/dt computed from the model's equations | 04.6, 04.7, 05.2, 07.1, 07.2, 07.5 |
| `e2_maps.json` | vorticity ω and current j maps (128², spectral interpolation of 32² modes), reference and V0, V1, V4, V5; divergence maps of V0 and V1; shared `vmax` | 08.1–08.3 |
| `e2_eval.json` | per variant train/test means, per-η tables, the "on the crowd" variants (base, tilting, rescaling) | 08.2, 08.5, 09.5, X3.2, X3.4 |
| `e3_growth.json` | s(Rm) at 32³ (whole run, last quarter), thresholds 8.87 / 17.6 / 26.8, published windows (R:1112), N = 48 checks, −1/Rm check | 03.4, X1.1, X1.3, ghost of 10.4 |
| `e3_modes.json` | dominant modes at Rm 8, 12, 16, 20: \|B\| on 32³, components at 16³, z = 0 slices | X1.2 |
| `digest.json` | every table of `experiences/resultats/digest.md`, parsed | any number quoted from the digest |
| `fig_<name>.json` | the site's figure data (`cadre`, `flow_matching`, `taxonomie`, `vks` are SCHEMATIC: show the chip, never their numbers; `plan_these`, `simulations` are computed from E1–E3) | 06.1, 06.3, 08.6, 08.7, 10.1, 02.5 |

Notes: E1 snapshots are float32, so per-sample projected snapshots show |dE/dt| ~ 10⁻⁸ instead of the report's
4 × 10⁻¹⁷: quote the number from `e1_eval.json` / the report, use the snapshots for shapes only. The growth rate is
**s** (symbol sheet), the files never say λ. The prototype files `e1_rate.json` (superseded by `e1_finegrid.json`)
and `palier1_eta_sweep.json` (a PROVISIONAL stand-in, contrary to D4) must not be used.

### Cloud results (PENDING scenes) — `tools/data_cloud.py`

Run in the repository venv (h5py) once the outputs exist; `python -I tools/data_cloud.py selftest` checks every
converter on tiny synthetic inputs (no simulation). Each output has `verdict` (`met | not_met | inconclusive`,
computed by the converter from the rule in `verdict_rule`), `verdict_text`, and `fields` (strings for the
`{{name}}` placeholders of the result narration).

| converter | input | output | scene | verdict rule | `fields` |
|---|---|---|---|---|---|
| `palier1 --mff …` | MFF of `palier1_mhd2d` | `palier1_sweep.json` (curve + per-η dissipation, flat Itô injection line, histogram of injection − dissipation, one j tile) | 10.3 | stationarity of the data: \|E[inj − D]\|/inj < 5 % | `n_eta, worst_eta, worst_residual_percent, verdict` |
| `abc3d --mff …` | MFF of `palier2_abc3d` | `palier2_abc3d.json` (s and s_q per Rm, seed spread, thresholds, 16³ modes) | 10.4 | D17: s(17) > 0 > s(18), \|s − s_q\| < \|s\| at both; missing points → inconclusive | `s17, s18, thresholds, n_thresholds, verdict` |
| `tg3d --mff …` | MFF of `palier2_tg3d` | `palier2_tg3d.json` (ln E_B(t), s_kin, saturation flag A8, spectra, Rm_c per Pm) | 10.5 | threshold bracketed at ≥ 2 Pm (qualitative) | `n_runs, n_saturated, n_growing, thresholds, verdict` |
| `fm3d-eval --eval r.json [--tg …]` | report of `python -m milady.eval … --out` | `fm3d_eval.json` (lamps a–d, per-point metrics and spectra) | 10.7 | (a) divergence < 10⁻¹²; (b) < 0.1 decade at training points (T:917); (c), (d) inconclusive at this scale; indicative (A7) | `worst_spectrum_error, max_divergence, n_points, verdict` |
| `fm3d-stat --eval … --control …` | two reports (loss / weight 0) | `fm3d_stationarity.json` (lamps) | X3.5 | residual < 5 %, control worse, σ ratio in [0.8, 1.2] (adapted from tier 1, A9) | `worst_residual_percent, verdict` |
| `trace --catalog sims.json` | `python -m milady.catalog sims --campaign C` | `x5_campaign_trace.json` | X5.3 | every simulation finished | `n_sims, n_done, hours, gigabytes` |
| `bill --catalog … --plan plan.json` | catalog dumps + the plan's hours (you transcribe T:955-974) | `x5_compute_bill.json` (gauge) | X5.5 | measured / planned in [0.5, 2] | `ratio, measured_hours, verdict` |
| `xpoints --mff … --generated g.npz [--tolerance]` | reference MFF + generated B fields | `x5_xpoints.json` | X5.4 | needs a tolerance (none in the plan: ask) | `mean_reference, mean_generated, verdict` |
| `tier0 --e1 e1_3seeds.json` | an E1-style JSON with 3 seeds | `x4_tier0.json` | X4.5 | inconclusive by design (the tier-0 criteria need 10⁶ snapshots) | `n_seeds, cumulative_error_percent` |
| `seat --in s.json --name tier3_vks` | generic seat JSON (format in the tool's docstring) | `tier3_vks.json`, `tier4_dresdyn.json`, `x4_branch.json`, `x4_rice_levels.json` | 10.9, X6.4, X6.5, X4.4, X4.2 | given by the producer, validated | as given |

## 6. Pending scenes: the empty seat and its result variant

A PENDING scene is shippable now (D4/D5). Same file, two variants chosen by `ctx.variant`:

```js
data: { seat: { url: 'data/palier2_abc3d.json', optional: true }, e3: 'data/e3_growth.json' },
setup(ctx) {
  Kit.badge(ctx, { kind: 'CONJECTURE', confidence: 'high' });   // preview fallback; the script's badge wins
  Kit.seat(ctx, { type: 'curve', variant: ctx.variant, data: ctx.data.seat, tag: 'palier2_abc3d', at: 'seat',
    x: { label: 'Rm, magnetic Reynolds number', min: 4, max: 40, ticks: [4, 10, 20, 30, 40], param: true },
    y: { label: 's, growth rate', min: -0.02, max: 0.015 }, zero: true, band: { x: [17, 18], label: 'decisive' },
    ghost: { x: ctx.data.e3.x.values, y: ctx.data.e3.series[0].y, label: 'E3 at 32³ (measured)', legendX: 230, legendY: 796 },
    bet: '…', confidence: 'high', criterion: '…', source: 'R:1112 · D17', ask: '…',
    cues: { frame: 'seat', bet: 'bet', criterion: 'criterion', ask: 'ask', data: 'seat+0.8' } });
}
```

- **Pending**: dashed grey frame, axes labelled, success band shaded, grey data tag `DATA · <tag> · AWAITING`, the
  READY anchor (a ghost curve, a schematic) and the right column: THE BET, CONFIDENCE (pips), SUCCESS CRITERION
  (+ source), and the boxed "ASK BEFORE WE COMPUTE" (the question that decides the computation). No number of the
  missing result anywhere. The hatched AWAITING frame of the prototype is for drafts only.
- **Result**: the same frame, solid, the data drawn (solid simulated, dashed generated), the tag carries the data
  stamp and SHA-256 prefix, and the RESULT block shows the converter's verdict and `verdict_text` (no verdict
  is ever computed in a scene). Vary the seat type across scenes: `curve`, `map`, `lamps` (`lamps: [{id, label, rule}]`,
  `lampsTitle`), `gauge` (`gauge: {label, min, max, band, ticks, log, unit}`).
- Keep the right column short (bet ≤ 14 words, criterion ≤ 16, ask ≤ 14): it must end above y = 880 (warned).

## 7. Layout, type and colour rules

- **Safe frame**: x 96–1824, y 56–880. **Subtitle band**: y ≥ 900 is reserved (nothing there, ever); nothing
  important between 880 and 900. Fixed zones: badge top-right (y 40–100), corner needle under it (x 1720–1824,
  y 124–228), rail in the left gutter (x 0–92), lower-thirds bottom-left (x 96–996, y 752–880), formula layer
  bottom-right (x 1064–1824, y 752–880). Keep your content out of the zones you use.
- **Text ≥ 28 px** for everything (tick labels, chips, mono labels included). Scale: titles 112–120, headings 60,
  lead 44, body 36, labels 32, minimum 28. KaTeX display 64–96 px, formula layer 32 px. Inter for words (tabular
  figures), Inter Display for titles, JetBrains Mono for chips and file names (capitals via `Kit.upper`).
- **Colour = quantity**: `--param` green, `--u` blue, `--b` vermillion (other polarity `--b-neg`, a shade, not a
  hue), `--model` violet, `--metric` amber, `--infra` grey lines; matter grey. At most three key colours per shot.
  Only tokens (`var(--b)`, `Scene.col('b')`, `Kit.c('b')`), never a hex in a scene. Registers switch the tokens.
- **Provenance**: simulated solid + white chip; generated dashed + violet chip / frame; schematic grey dashed chip;
  laboratory measurement ring chip. Metaphors carry `SCHEMATIC` and no invented numbers.
- One idea per shot; never more than 3 s of complete stillness (the kit's idle motion: field-line breathing,
  drifting tracers, a slow highlight); 1–1.5 s of breath after a payoff.

## 8. Performance budget per render class

The screenshot (raster + PNG) dominates, not the scene's JavaScript: keep `seek(t)` under 20 ms (flat) / 60 ms
(particles), and keep frames simple. Measured on the gallery (3 isolated workers, 1080p30, machine shared with
another job, load ≈ 7 on 4 cores; the idle machine is about 1.6× faster, plan/pipeline.md §3): equation and
lower-thirds 28 fps, question card 26, plot 26, chapter card (full-frame field lines) 22, cloud + histogram 23,
E2 field maps 20 (smooth gradients make 0.8 MB PNG frames).

| class | what | budget |
|---|---|---|
| flat | text, cards, equations, plots, seats, chips | ≥ 30 fps capture on an idle machine; DOM/SVG built once in `setup`; per frame only styles/attributes change |
| dense 2D | Canvas fields, tracers, clouds, two inks | ≤ 3000 particles, trails ≤ 12, `twoInks.maxPoints` ≤ 6000, streamlines precomputed; full-frame Canvas only when needed (give `canvasLayer` a box); maps at ≤ 3 per shot |
| 3D | Three.js | ≤ 28 000 fat-line segments, MSAA optional, no shadows, matte materials; cost is geometry, not pixels (pipeline.md §3.2) |

Simulations inside a scene go through `Scene.stepper` with a fixed `dt` (≥ 1/120 s); a capture worker renders its
frames in order, so the cost per frame is the cost of one step batch. Give heavy components an `out` time.

## 9. Determinism rules

- A frame is a pure function of `t` (and of the data and the entry). No `setTimeout`, `setInterval`, CSS
  transitions or animations, `requestAnimationFrame` loops, `Date`, `performance.now()` in scene logic.
- Randomness: `Scene.rng('name')` (or `Math.random`, seeded per scene); never an unseeded source.
- State that evolves: `Scene.stepper(init, step, dt)` only; `init` must rebuild from scratch (backward seeks replay).
- Build DOM, SVG, KaTeX and geometry in `setup`; `render` only sets styles/attributes/draws. Never create elements
  in `render`.
- GSAP only as paused timelines driven by `tl.seek(t)`; Three.js renders inside `render(t)` with `preserveDrawingBuffer: true`.
- Measured on the gallery (`tools/determinism.js`): a frame reached directly is bit-identical across fresh browsers;
  after sequential seeking, some SVG/Canvas edges differ by anti-aliasing (a few to ~500 edge pixels, invisible);
  workers always render in order, so a render is consistent.

## 10. What NOT to do

- No numbers typed in scene code (results, rates, thresholds): read them from `data/*.json`. No verdict computed in a scene.
- No text below 28 px, nothing in the subtitle band, nothing cut at the frame edge, no two lower-thirds at once.
- No CSS `text-transform` (symbols change case), no hex colours, no key colour used as decoration, no fourth key colour.
- No crossfades between scenes, glows, lens flares, camera shake, glitch, RGB split, bouncy or elastic easing,
  decorative particle bursts, starfields, horseshoe magnets, lightning, fake telemetry numbers.
- No λ for the growth rate (it is s), no "flip rate" for the crossing rate of D, no "energy distance" outside 06.5/X3.0
  (say "distribution distance"), no μ/ν Gissinger symbols on screen (the numbers 0.119, 0.1) — the symbol sheet of
  `plan/outline.md` §2 rules every label.
- No external assets from the web, no CDN, no fonts other than the vendored ones, no photos or logos (D6).
- Never write into `data/` by hand, never put a synthetic or test file in `data/` (a data file's presence promotes
  a pending scene), never edit `runtime/` (ask foundation engineer B).

## 11. Reviewer checklist (apply to the stills of every cue and every transition)

Run `node stills.js` on the scene (it reports page errors, `__SCENE_WARNINGS__` and the runtime's layout QA,
`window.__QA__(t)`: small text, clipping, subtitle band, overlapping text boxes), then look at every still.

1. **Renders**: no page error, no scene warning (unknown cue, overlapping lower-thirds, text that does not fit), no blank frame.
2. **Cues**: every visual event sits on a script cue (120–200 ms ahead of the word); no hard-coded time; predict holds come from `hold_after`.
3. **Safe area**: nothing below y = 880 except lower-third/formula layer (≤ 880); nothing in y ≥ 900; nothing cut at an edge; zones respected.
4. **Text**: every glyph ≥ 28 px; no overlap (QA empty); symbols in the right case (ω not Ω, η not Η, j not J); spelling; numbers with U+2212 minus and units.
5. **Colour key**: each colour means its quantity; ≤ 3 key colours; polarity as vermillion shades; generated = violet chip/frame + dashed; schematic = grey chip.
6. **Honesty**: badge present and right (MEASURED / PROVED / CONJECTURE + confidence / PLANNED / CONTEXT / SCHEMATIC); CONTEXT facts have a reference chip; the report's limits visible where the script says them.
7. **Data**: every number on screen traceable to a data file (source lower-third or seat tag shows the stamp and SHA-256 prefix); no number from a SCHEMATIC figure file.
8. **Pending seats**: bet, confidence, criterion with source, the question to ask, a READY anchor; no result number; result variant draws the converter's verdict only.
9. **Question card**: ≤ 18 words, why and unblocks present, category right, legible as a whole in 6–10 s.
10. **Motion**: one idea per shot, no element stays still > 3 s with nothing breathing, no banned effect, overshoot ≤ 3 % (needles, knobs only).
11. **Determinism**: the same still twice (fresh browser) is identical; heavy components have an `out`.
12. **Performance**: flat scenes `seek` < 20 ms, dense ≤ budgets of §8; 3D counts segments.

## 12. Gallery and stills

```bash
cd /home/user/milady-2027/video
NODE_PATH=/opt/node22/lib/node_modules node stills.js --scene scenes/_gallery/gallery.html \
  --times 7.4,15.4,23.4,31.4,39.4,47.4,55.4,63.4,71.4,79.4,87.4,95.4,103.4,111.4,119.4,127.4 --outdir out/gallery
```

Plates: 1 chapter card · 2 question card · 3 badges, chips, rail, corner needle, formula layer · 4 equation builder and
the four lower-thirds · 5 plots (E1 data, log axis, error bars, noise floor) · 6 seat curve pending (E3 ghost) · 7 seat
lamps pending · 8 seat gauge result (test fixture) · 9 seat map pending · 10 field maps (E2) · 11 field lines, arrows,
tracers · 12 needle, knob, polarity strip, staircase · 13 two inks · 14 cloud (E1 model C) and histogram spike ·
15 projector, pen, mirror · 16 seat curve result (fixture using the E3 data). Fixtures carry the chip
"TEST FIXTURE · NOT A RESULT" and never leave the gallery.

<!-- Section "Pipeline" is appended below by foundation engineer A. -->

---

## Pipeline (foundation engineer A: `build.js`, `capture.js`, `subs.js`, `stills.js`, `Makefile`, `audio/`, `tools/` except `tools/data_*.py`)

What the build does with your scene, and what it gives it. Commands: `README.md`; narration swap: `NARRATION.md`.

### P1. The chain

```
script/<unit>.json ─ tools/assemble_cut.py ─▶ script/_build/film_<cut>.json   running order, variant, {{fields}}, lint
   ─ audio/tts.py ─▶ audio/cache/<key>.wav        ONE Fish request per paragraph, cached by (text, voice, settings)
   ─ audio/align.py ─▶ audio/scenes/<id>.wav + .align.json   sentence times (silence detection inside each paragraph)
   ─ build.js ─▶ script/_build/<cut>_cues.json, _timeline.json, subs/<cut>.{srt,vtt,ass} + subs/<cut>_scenes/<id>.ass
   ─ capture.js ─▶ out/scenes/<id>.mp4 (+ .events.json, .metrics.json)   only scenes whose input hash changed
   ─ audio/mix.py ─▶ out/stems/<cut>_{full,narration,music,effects,nonarration}.m4a   -16 LUFS, TP <= -1 dBTP
   ─ build.js ─▶ out/film_<cut>.mp4   stream copy; audio 1 = full mix, audio 2 = no narration; chapters
```

French narration (`--lang fr`, `make … LANG=fr`, BRIEF §9): the same chain on `script/<unit>.json` + the overlay
`script/fr/<unit>.json` (same sentence ids and cues, French text), Fish `"language": "fr"`, `audio/lexicon_fr.json`;
every output is suffixed `_fr` (`film_<cut>_fr.json`, `<cut>_fr_cues.json`, `subs/<cut>_fr.*`, `stems/<cut>_fr_*`,
`out/film_<cut>_fr.mp4`) and kept apart (`audio/scenes_fr/`, `out/scenes_fr/`). The visuals stay English: a page
needs no change, it simply receives the French timing (longer: hang everything on cues, never on durations).

Cuts: `core` = `plan/outline.json` cuts.core.chapters + `ch10q` before `ch11`; `extended` = the same + every module
inserted after its `insert_after` (scene id, `chXX.Q`, or unit id = after that unit's last scene), so a chapter's
question card comes after the modules inserted inside the chapter; `update` = the "Results update" episode.
`"cuts": ["core"]` / `["extended"]` on a scene restricts it to one cut (otherwise the outline's `extended_variant`
applies: 10.8 skipped and 10.9 replaced by `10.9-bridge` in the extended cut). The extended order is checked against
the outline's `scene_order`. A missing unit file is skipped with a warning (`--strict` makes it an error).

### P2. What your page receives (`window.__ENTRY__`, i.e. `ctx.script`)

`id, unit, duration, fps, cues, sentences, status, variant, stamp, level, register, badge, question, title, onscreen,
sources, data, params, seed`.

- `duration` = `lead_in` (default 0.4 s) + narration + `tail` (default 0.8 s), rounded to whole frames. The
  narration track is: paragraph 1 | 0.9 s (`[long pause]`) + `hold_after` | paragraph 2 | … | last paragraph |
  its `hold_after`. A scene must work for ANY duration: everything hangs on cues. A scene with no paragraph
  lasts its `target_s`.
- `cues`: each sentence's start (`lead_in` + start in the track) under the sentence's `cue` name and under
  `s_<sentence id>`; plus `_speech_end` (end of the last sentence) and `_tail` (duration − tail).
  `sentences`: `[{id, cue, start, end}]` in scene time (for word-level effects, use `end` too).
  Timing accuracy: silence-based, measured at 4–5 ms on the placeholder voice; expect tens of ms on real speech.
- `status`: `ready | pending | provisional`; `variant`: `pending | result` (as the runtime expects). A pending scene
  becomes `provisional` + `result` when EVERY file of its `deps` exists (a file with `"pending": true` or
  `meta.pending` counts as missing); `stamp` = the `meta.stamp` of its first data file.
- `data`, `params`, `seed`: the script's `entry.data` (name → URL overrides), `entry.params`, `entry.seed` (12345).
- `badge`, `question`, `onscreen`, `sources`, `level`, `register`, `title`: copied from the script.
- `lang`: present only in a French build (`"fr"`); the on-screen text stays English (`question.en`, labels, chips).

### P3. Paths and what makes a scene re-render

- The recorder serves `video/` at `/` and the repository root (read-only) at `/site/`: a site asset is
  `/site/assets/…` (relative paths that climb out of `video/` are not served). Data: `data/x.json` (runtime-resolved) or `/data/x.json`.
- List in `deps` every data file the scene reads (pending logic + hash), and in `assets` every repository file
  it loads (path from the repository root, e.g. `assets/interactif/gissinger.js`).
- A scene re-renders when one of these changes (`make plan` prints which): its HTML; any non-HTML file in its
  folder (`scenes/<unit>/`, shared by the unit's scenes); `runtime/**`, `scenes/_shared/**`, `capture.js`,
  `tools/server.js`, `vendor/`; its `deps` and `assets` contents; its timeline entry (duration, cues, status,
  badge, onscreen…); its subtitles; the render settings or its `encode`. Neighbours and the cut do not matter:
  one render serves both cuts (subtitles are computed per scene, in scene time).

### P4. Script fields the pipeline reads (schema 2, BRIEF section 5)

- `paragraphs[].hold_after` (s), `paragraphs[].sentences[] {id, cue, text}`; ids are generated (`<scene>.s<k>`)
  when missing; cue names match `[A-Za-z_][\w-]*`, unique in the scene.
- `variants.result {data_fields, paragraphs}`: `{{name}}` is looked up in each dep's `fields` object, then as a
  dotted path from the file root (`{{seat.s17}}`). A number is spoken in words (`0.86` → "zero point eight six"),
  `{{x:2}}` with two decimals, `{{x:digits}}` raw; a string (the converters' `fields`) is used as is. To write both
  outcomes, a result paragraph or sentence may carry `"when": "field"` or `"when": "!field"` (truthiness of a
  field, e.g. a boolean the converter writes). Missing fields keep the pending narration (warned).
- Question cards: `question {en, fr, why, unblocks, ask_who}`; optional `question.say` = the spoken sentence with
  numbers in words (else `en` is spoken); with no `paragraphs`, one sentence with the cue `q` is generated. All
  cards of a cut: `script/_build/questions_<cut>.json` (for the French question sheet).
- `sfx` (sound effects), `music` (`false` or `{"gain": 0..1}`), `encode` (`{"crf": 20..23, "maxrate": "4M"}`),
  `cuts`, `lead_in`, `tail`, `target_s`.
- Lint (warnings, `make plan`): estimated length at 146 raw wpm vs `target_s` ± 15 %; question card 6–10 s and
  ≤ 18 words; brackets, parentheses, digits or symbols in narration; unbalanced `{u}…{/}` markup; empty text.

### P5. Sound

- Music: original bed synthesized by `audio/mix.py` (pads, sub-bass, sparse bells; one progression per unit), level
  by the scene's `level`: L0–L1 full, L2 0.8, L3 0.35, L4–L5 silent, 3-s crossfades, 15 LU under the voice in gaps
  and ducked 12 dB under speech. Override per scene with `"music"`.
- Effects (all synthesized): `needle` (= `flip`, the two-note M1), `tick` (zero crossing), `detent` (knob), `whoosh`
  (chapter card), `impact`, `hiss` (`dur`), `squeal` (`dur`), `chime` (question card), `pop`. Listen: `make sfx-demo`.
  Two ways to place them, both in scene seconds:
  - in the script, `"sfx": ["whoosh@0", "impact@title-0.1", "chime@q", {"id": "needle", "cue": "flip", "offset": 0.3,
    "gain_db": -12, "pan": 0.2}, {"id": "hiss", "t": 4.0, "dur": 2.5}]` (or the same list in `entry.params.sfx`);
  - from the page: `window.__EVENTS__ = [{t, id, gain_db?, pan?, dur?}]` (or a function of the duration returning
    that list), set in `setup()` from the same deterministic computation that draws them (crossing ticks, detents);
    read once after rendering, saved as `out/scenes/<id>.events.json`.
  `gain_db` = peak level in dBFS in the final −16 LUFS mix (defaults: needle −12, impact −11, whoosh −16, chime −16,
  tick −20, squeal −22, detent −24, pop −24, hiss −27). Effects duck 6 dB under speech; time a loud one in a gap.

### P6. Encoding, size, draft

- Final: 1080p30, H.264 high@4.1, preset medium, CRF 21, `-maxrate 6M -bufsize 12M`, `stitchable=1`, no tune, BT.709.
  Every scene file MUST share these stream parameters (the film is a stream copy): only `crf` and `maxrate` may
  change per scene (`"encode"`). Dense particle scenes: `{"crf": 23}` or `{"maxrate": "4M"}`. The build warns if
  the MP4 exceeds 1.9 GB and lists the heaviest scenes.
- Draft (`make draft`): 960×540, 15 fps, veryfast, in `out/draft/` (never mixed with finals); the page is the same
  (`devicePixelRatio` 0.5: size canvases with `Scene.hidpi`).
- Recording: 4 isolated browsers per scene, each renders a contiguous range of frames in order from a fresh page.

### P7. Checks

- `make check U=<unit>` (`node build.js --unit <unit> --check`): narration from the cache or a placeholder
  (never the API), real timings, then one still per cue (0.6 s after it, before the next), plus the first and
  last frames, with page errors (exit 1), `__SCENE_WARNINGS__` and `__QA__` issues: `out/check/unit_<unit>/`
  (stills, `<id>_sheet.png`, `report.json`).
- A 404 on a data URL is tolerated only while the scene is `pending`. Page errors of a render are in
  `out/<cut>_build_report.json` (`page_errors`); `--strict` makes them fatal.
- `make test` runs the whole chain on `script/_test` (units tc1, tq, tc2, tx; pages in `scenes/_test/`; test data
  in `script/_test/data/`, never in `data/`).
