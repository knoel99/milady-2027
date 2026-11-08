# Scenes chSOA2 — build report (batch 3, 2026-11-08)

## 0. Status

| Scene | Page | Badge | Estimated check | French check | Determinism |
|---|---|---|---|---|---|
| SOA2.1 | `SOA2_1_back_to_the_map.html` | CONTEXT | 0 errors · 0 warnings · 0 QA | same | ok |
| SOA2.2 | `SOA2_2_fast_but_average.html` | CONTEXT | 0 · 0 · 0 | same | ok |
| SOA2.3 | `SOA2_3_machines_that_sample.html` | CONTEXT | 0 · 0 · 0 | same | ok |
| SOA2.4 | `SOA2_4_making_samples_obey.html` | CONTEXT | 0 · 0 · 0 | same | ok |
| SOA2.5 | `SOA2_5_priors_for_assimilation.html` | CONTEXT | 0 · 0 · 0 | same | ok |
| SOA2.6 | `SOA2_6_who_brings_what.html` | CONTEXT | 0 · 0 · 0 | same | ok |
| SOA2.7 | `SOA2_7_the_empty_intersection.html` | PLANNED | 0 · 0 · 4 QA (false positive, §4.3) | same | ok |
| SOA2.8 | `SOA2_8_neighbours_and_limits.html` | CONJECTURE medium | 0 · 0 · 0 | same | ok |
| chSOA2.Q | `SOA2_Q_question.html` | — | 0 · 3 warnings (writer's text too long, §4.1) · 0 | same | ok |

`make det U=chSOA2` exit 0. Draft `out/draft/unit_chSOA2/unit_chSOA2_draft.mp4`, 4:54, capture 50–68 fps (960×540).
Timing: estimated and French estimate only (no narration in this clone).

**Process deviation (lead's instruction for this batch):** no independent subagent review (token budget). The builder
looked at every contact sheet and a few full-size stills and draft frames. CONTRACT §13.5 item 8 is NOT met.

## 1. What was built

One shared helper, `SM.map` in `chSOA2_kit.js`: lanes as rows on a year axis (2012–2031, 1995–2031 in SOA2.6,
1900–2031 for the century map of SOA2.1), the focused row grows and its pins get stacked labels, other rows shrink
with unlabelled dots; NOW hairline (pulsing), dashed stub to 2031; a gate grid (3D · WALLS · LOW Pm · RARE) with one row
of verdict cells per lane. `SM.laneScene` builds SOA2.2–SOA2.5 from their `entry.params` (pins, verdicts,
lower-thirds); earlier scenes' pins and verdict rows stay dimmed. `SM.ALL_PINS` / `SM.ALL_VERDICTS` transcribe the
pins and verdicts of every scene's `entry.params` (dated facts with citations in the script); regenerate them if the
script changes. Per-scene deviations are in each `visual` ("AS BUILT (2026-11-08, batch 3)"). Main ones:

- the chSOA1 map module does not exist: SOA2.1 redraws a simple century map, then cross-fades into the zoom;
- no gate-head icons and no verdict sub-tags (`verdict_notes`): no room in 118-px columns;
- several small glyphs dropped (strand glyphs, 'E1 used this', code brackets, magnifier sweep, two-hump cloud of 2.3);
- SOA2.7: the map fades out entirely for the five-gap list (text over a 25 % map failed the layout QA);
- chSOA2.Q: card enlarged by a page workaround (§4.1).

## 2. Script fields changed

`visual` only (AS BUILT appended, 9 scenes). `deps` stay empty (no data file read).

## 3. Data

None. All years and verdicts are the script's `entry.params` (as the unit notes allow); if CONTRACT §5 is read
strictly, `tools/data_existing.py` should transcribe them into `data/soa_map.json` and `SM.ALL_PINS` would read it.

## 4. Findings for the writer

1. chSOA2.Q: `why` (≈ 13 lines at 28 px) and `unblocks` (≈ 7 lines) are 2.6× and 1.9× what the card holds; the
   question itself needs three lines at 60 px. Shorten all three (≤ 4 lines each); the page currently shrinks the card's
   type to fit (workaround).
2. SOA2.2 `two_polarity_inset.box` and SOA2.5 `posterior_inset.box` overlap the formula layer / gate grid; moved.
3. SOA2.7: the Rice formula's subscript $p_{D,\dot D}$ is reported overlapping its second line by the QA; the stills
   show clear space (false positive of the line-box comparison).

## 5. Kit issues

1. `runtime/components/hud.js`, `Kit.formulaLayer`: between an item's `out` and the next item the empty layer (frame and
   "FORMULA" label) stays on screen (SOA2.4, between 'nowinner' and 'walls'). Workaround `UK.formulaLayers` (one layer
   per item). Proposed fix: hide the layer when no row is visible.
2. `runtime/components/cards.js`, `Kit.questionCard`: text that does not fit is only warned about and then overlaps the
   question and rows; the pen underlines live in an SVG whose viewBox is fixed at 1600×676, so they are misplaced if the
   card is resized. Proposed fix: shrink the rows' type to ≥ 28 px before warning, and position underlines in stage px.
3. A shared map component (chSOA1 and chSOA2 both need it): `SM.map` here is a candidate for `runtime/components/`.
