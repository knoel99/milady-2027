# Scenes ch09 — build report (batch 3, 2026-11-08)

## 0. Status

| Scene | Page | Class | Badge | Estimated check | French check | Determinism |
|---|---|---|---|---|---|---|
| 09.1 | `09_1_how_often_from_generated_photographs.html` | flat | MEASURED | 0 errors · 0 warnings · 0 QA | same | identical / anti-aliasing |
| 09.2 | `09_2_early_late_or_on_time.html` | flat | MEASURED | 0 · 0 · 0 | same | ok |
| 09.3 | `09_3_a_stiff_sheet_on_a_steep_ramp.html` | dense 2D (2 canvases, pre-rasterized frames) | PROVED | 0 · 0 · 0 | same | ok |
| 09.4 | `09_4_the_loss_is_not_a_clean_win.html` | flat | MEASURED | 0 · 0 · 0 | same | ok |
| 09.5 | `09_5_still_far_from_the_data.html` | flat | MEASURED | 0 · 0 · 0 | same | ok |
| 09.6 | `09_6_scoreboard_and_three_lessons.html` | flat | MEASURED | 0 · 0 · 0 | same | ok |
| ch09.Q | `09_Q_question.html` | flat | — | 0 · 2 warnings (writer's text too long, §4) · 0 | same | ok |

Timing: estimated (146 wpm) and French estimate; no narration in this clone. `make det U=ch09` exit 0 (no DIFFERENT
frame). Draft `out/draft/unit_ch09/unit_ch09_draft.mp4`, 4:25, capture 49–78 fps at 960×540.
Unit helpers: `ch09_kit.js` (`UK.label`, `UK.fade`, `UK.series`, `UK.onscreen`, `UK.frac`, `UK.formulaItems`), `ch09.css`.

**Process deviation (lead's instruction for this batch):** no independent subagent review was run (token budget);
the builder reviewed every still and a few mid-move draft frames. CONTRACT §13.5 item 8 is therefore NOT met: an
independent review is still owed.

## 1. Per scene (what was built, deviations)

The same text is appended to each scene's `visual` as "AS BUILT (2026-11-08, batch 3)". Short version:

- **09.1** toll counter with violet cars drawn in the page (no shared road helper); cars stop at `rice`, amber speed
  bars, road shrinks to the top-right icon before `far`. Chart: counted + Rice-on-reference (50 %) pre-drawn,
  generated Rice dashed over Γ ≥ 0.89, amber area between, grey hatch under the counted curve (not a dimmed
  vermillion). Near range fogged; near bracket and label placed low in the fog. Both formulas shown in two steps.
  Simplified promise card 3.
- **09.2** hard cut (no T1 morph); PREDICT card, then a compact card with pen ticks on early/late and a strike
  through "on time"; generated curve in three stretches; inset moved 60 px down; caption at y 780.
- **09.3** clouds from the four existing `e1_samples_<Γ>.json` (0.85, 0.87, 0.9, 0.93) instead of the 21-Γ
  `ch09_sweep.json` (its LOCAL_ONLY source is absent here); sheet = Gaussian smoothing of the monotone envelope.
- **09.4** bar pairs; no histogram / spike / two-juries glyphs; no seed-spread whisker.
- **09.5** panels moved down (entry.params); factors from data; "3 numbers" glyph dropped; E2 ruler shortened.
- **09.6** planks and cards drawn in the page (no shared shelves component); promise cards of 03.7 re-drawn with the
  same texts; lessons with chalk glyphs.
- **ch09.Q** question card over a 10 % backdrop of the 09.1 curves.

## 2. Script fields changed

- `visual` (all 7 scenes): AS BUILT paragraph appended.
- 09.3 `deps` / `entry`: `data/ch09_sweep.json` replaced by `e1_samples_0.85/0.87/0.9/0.93.json`; entry.params
  `clouds.range` 3.2 (±2.4 clipped points), knob y 612 r 40, `smooth_sigma` added.
- 09.5 `deps` / `entry`: + `data/ch09_rice.json` (factors) and `data/e1_finegrid.json` (Γ train/test);
  panel y0/y1 220/560, ruler_y 722.
- 09.6 and ch09.Q `deps` / `entry.data`: `data/ch09_rice.json`, `data/e1_finegrid.json`.

## 3. Data added

`tools/data_ch09.py` → `data/ch09_rice.json` (meta with source SHA-256): n_settings 41, n_unseen 30, threshold,
cumulative errors C/F/ref near and far (asserts 42/14/32/23 % and pointwise 17/65 % of R:883), pointwise misses,
below-threshold leak (1.55e-4 at 0.845), onset (0.865: 3.04e-4 vs 1.94e-3), overshoot rows, counted crossings per Γ
(93 … 572), factors best/floor (E1 2.1, E2 6.13), spread ratios (1.04, 0.75, 19.2, 1.28). Bookkeeping only.
`data/ch09_sweep.json` was NOT produced (source cache not in the clone): a question for the lead (re-run the
extraction where the cache exists, then 09.3 can use 21 Γ).

## 4. Findings for the writer

1. ch09.Q: `question.why` and `question.unblocks` overflow the card at 28 px (why 174 px > 173, unblocks
   174 px > 130): shorten `unblocks` by about a third.
2. 09.3: with the clouds available (four Γ), the "early strays" read only at 0.85 (1 of 4,000); at 0.87 the small
   generated cloud has fewer corridor points than the reference (6/4,000 vs 9/8,000 ×2 mirrored), consistent with
   the visual's own warning. No narration change needed.
3. 09.5 formula (and 09.1) contain more than the layer can show at 28 px: they are shown in two steps.
4. 09.5's formula layer brings a vermillion `B` into a shot that already has amber, violet and green (4 key
   colours, CONTRACT §7): consider `\B` → plain B in that formula.

## 5. Kit issues

1. `runtime/components/hud.js`, `Kit.chip` with `maxWidth` and `anchor: 'br'`: the wrapped chip collapsed to a
   narrow multi-line column (09.6 first build, "full table…" chip at maxWidth 700 rendered about 150 px wide).
   Workaround: a two-line mono `UK.label`. Proposed fix: set `width: max-content; max-width: …` on wrapped chips.
2. `Kit.formulaLayer`: long statements are only warned about; a helper that splits a statement into successive
   items (here `UK.formulaItems`, top-level `;` else `+`) would be worth promoting.
3. Script `entry.params` silently override a page's default params of a different shape (09.1 `road`, 09.3
   `clouds.range` as an object → NaN geometry). A schema check or a warning when a param's type changes would help.
4. Promotion candidates: `UK.label` / `UK.fade` (timed label/element), `UK.frac` (time of a fraction of a sentence).
