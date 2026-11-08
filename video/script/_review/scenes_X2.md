# Scenes X2 — build report (batch 4, 2026-11-08)

Builder: batch-4 scene session. Token budget for this batch was tight: per the batch instructions **no independent
subagent review was run** (CONTRACT 13.5 item 8 is therefore open for this unit; the lead or a later pass should review).

## 0. Status

| Scene | Page | Check (est.) | Check (fr) | Notes |
|---|---|---|---|---|
| X2.1 | `X2_1_build_it_in.html` | 0 err, 1 warning (blank first frame, intended: T3 ink change starts on the NIGHT background), 0 QA | same | flat |
| X2.2 | `X2_2_proposition_2_in_full.html` | 0 / 0 / 0 | same | flat, e2_eval |
| X2.3 | `X2_3_the_jensen_gap.html` | 0 / 0 / 4 QA (false positive: formula layer's own `x^2` and hat accent) | same | flat |
| X2.4 | `X2_4_the_mirror_proved.html` | 0 / 0 / 0 | same | flat, e1_samples_0.85 |
| X2.5 | `X2_5_proposition_5_and_its_limits.html` | 0 / 0 / 0 | same | Canvas 8,000 dots, e1_samples_0.9 + e1_finegrid |
| X2.Q | `X2_Q_question.html` | 0 / 2 warnings (question card text does not fit, see §3) / 0 | same | card |

`make det U=X2`: exit 0 (direct seeks identical, sequential = anti-aliasing only). Draft 3:51 at 960×540; capture
49.8–68.7 fps per scene.

## 1. Unit helpers

`scenes/X2/X2_kit.js` = the batch helpers `XK` (timed fade, labels, title, draw-on, card, inline TeX, lamp, ink change,
sentence fraction) + `XK.strip` (the X2 strip of the five propositions). `X2.css`: tokens only. Both are copies of the
same batch-4 helper used in every unit of the batch (candidate for promotion: `XK.timed`, `XK.inkChange`).

## 2. Per scene (deviations = the AS BUILT paragraph of each `visual`)

See `script/X2.json`, each scene's "AS BUILT (2026-11-08, batch 4)" paragraph. Main deviations: X2.1 last beat fades the
picture instead of dimming it; X2.2 redraws no large spring (inset meter only, from 'lands'), the hero leaves at 'lands',
the 08.2 gauge thumbnail is a text readout; X2.4 draws the point mirror by hand; X2.5 histogram range ±3σ instead of ±2.

Numbers on screen and their sources: X2.2 0.41 (`e2_eval.json` variants.V0_libre.mean.test.div_rel_u), 5.05 × 10⁻¹⁷,
1.78 × 10⁻¹⁷, 2.03 × 10⁻⁸ (V2, V4, V3 test means); X2.4 Γ = 0.85 (`e1_samples_0.85.json` gamma), Γ knob range = known
parameter range; X2.5 Γ = 0.9 and 8,000 (`e1_samples_0.9.json` gamma, n). Chip texts are the script's `onscreen.chips`.

## 3. Findings for the writer

1. **X2.Q**: `question.why` and `question.unblocks` overflow the card's boxes at 28 px (`cards.js` warns: 590×208 > 590×173
   and 590×174 > 590×130). The text still renders inside the ticket, but the card asks for shorter text.
2. **X2.2**: "the plain generator's zero point four one reads as a missing pull" — the 0.41 is a relative divergence of
   the plain generator (E2, test values), not a value of the schematic stray-part axis; the scene shows it as a separate
   readout to avoid implying it is read off the curve.

## 4. Kit issues

1. `runtime/components/cards.js` `Kit.questionCard`: the fit warning fires on texts that visibly fit (X2.Q end still);
   either the limit is conservative or the measured box is not the drawn one. Proposed: check the measured height
   against the ticket's real free space. No workaround.
2. `ctx.at` rejects compound specs such as `'zero+1.5+0.3'` (entry params like `tiles.at = 'zero+1.5'` cannot take an
   extra offset). Workaround: `ctx.at(spec) + dt` in the scene. Proposed: accept chained offsets.

## Review

Not run (batch instruction: no subagent, no separate review pass).
