# Scenes ch10q — build report (batch 3, 2026-11-08)

## 0. Status

| Scene | Badge | Estimated check | French check | Determinism |
|---|---|---|---|---|
| 10q.1 | PLANNED | 0 errors · 0 warnings · 7 QA (tickets crossing mid-move, §4.1) | same | ok |
| 10q.2 | PLANNED | 0 · 0 · 0 | same | ok |
| 10q.3 | PLANNED | 0 · 0 · 0 | same | ok |
| 10q.4 | CONJECTURE medium | 0 · 0 · 0 | same | ok |
| 10q.5 | CONJECTURE medium | 0 · 0 · 31 QA (tickets crossing during the opening move, t ≈ 1 s, §4.1) | same | ok |
| 10q.6 | CONJECTURE medium | 0 · 0 · 13 QA (same, t ≈ 1 s) | same | ok |

`make det U=ch10q` exit 0 (after a fix: the column heads' alpha was applied one frame late, which made sequential
seeks differ). Draft `out/draft/unit_ch10q/unit_ch10q_draft.mp4`. Timing: estimated and French estimate only.

**Process deviation (lead's instruction for this batch):** no independent subagent review (token budget). CONTRACT
§13.5 item 8 is NOT met.

## 1. What was built

The board is built from the **current** question register (`script/_shared/question_register.json`, 37 entries,
`order_for_ch10q`; priorities 13 / 14 / 10), transcribed into `scenes/ch10q/ch10q_board.js`, not from the 30-ticket
`params.board` of 10q.1. Q15 is now the chSOA2 card (LATU grid vs SFEMaNS mesh); Q31 is the PBFM positioning; Q32–Q37
are register-only. `ch10q_kit.js` holds the board component `CQ` (tickets that move between layouts A, B, C as pure
functions of t; the LATER pile marked `data-qa="ignore"` because it is a deliberate stack) and the question panel.
The callback thumbnails of the `visual` (schematic redraws of each question's origin scene) are replaced by a panel
showing the focused question's full register text and its card: more useful for the purpose of the chapter, and no
invented drawing. Per-scene deviations are in each `visual` ("AS BUILT (2026-11-08, batch 3)").

## 2. Script fields changed

`visual` only (AS BUILT appended, 6 scenes).

## 3. Data

None (`deps` empty). The board is a transcript of the register; regenerate `ch10q_board.js` when the register changes
(the builder's script is in the batch notes: register entries → id, category, priority, card, plays_in → ext,
hook, short label).

## 4. Findings and notes

1. QA overlaps listed in §0 are tickets passing over each other during a 0.6-s move (the stills at cue + 0.6 s and at
   t ≈ 1 s catch them mid-flight); every resting layout is clean.
2. For the writer / consistency editor: `params.board` of 10q.1 and the on-screen labels of 10q.1–10q.6 still describe
   the old 30-ticket register (Q15 'Positioning the first paper?', 'Q1 … Q30'); the narration is unaffected, but those
   labels should be refreshed from the current register (Q15 LATU/SFEMaNS, Q31 PBFM, Q32–Q37). Short labels written
   by the builder: Q15 'LATU grid or SFEMaNS mesh?', Q31 'Paper position vs PBFM?', Q32 'Large-eddy runs as data?',
   Q33 'Half-turn symmetry too?', Q34 'DQVU moment: keep it?', Q35 'Probes and DA method?', Q36 'POD, autoencoder or
   VAE?', Q37 'Literature watch, first paper?'.
3. 10q.1 narrates bets under step 2 'BET 1 · BOX 64³' etc.; with 96-px slots the hook labels are shortened to
   'BET 1', 'BET 2', '3D GEN.'.

## 5. Kit issues

None new (the board is unit-specific). Promotion candidate: a ticket glyph (question-card stub in miniature) in
`cards.js`, used by ch10q and by any later index of questions.
