# X3a review changelog (adversarial script review, 2026-11-08)

Unit: `script/X3a.json`, "Crowd laws, deeper" (extension, `insert_after: "X2"`; scenes X3.0-X3.4 plus `X3a.Q`).

- **Validation.** The JSON validates and keeps its formatting (indent 1, UTF-8, exact round trip).
  - `tools/assemble_cut.py --unit X3a` (output in the scratchpad) raises no lint warning.
  - All 14 TeX items (formula layers and the `$…$` label) render with `vendor/katex` and the `Kit.MACROS` table plus `\term`.
- **Pace.** The unit has 382 words and runs about 179.7 s. The content scenes are within −2.7 % to +5.1 % of their targets, at 127-130 words per minute of target.

| Scene | Target s | Words | Est. s | Dev. |
|---|---|---|---|---|
| X3.0 | 20 | 43 | 20.4 | +2.0 % |
| X3.1 | 40 | 86 | 39.5 | −1.2 % |
| X3.2 | 45 | 97 | 43.8 | −2.7 % |
| X3.3 | 35 | 74 | 36.8 | +5.1 % |
| X3.4 | 30 | 65 | 29.7 | −1.0 % |
| X3a.Q | 9 | 17 | 9.5 | within 6-10 s |

## Changes (what, why, evidence)

1. **X3.1.s5: wrong direction in "weights that grow exponentially with the quantity being fixed".**
   - In this toy the model's average r is too high (bias +0.4), so β* < 0. The weights *shrink* exponentially with r, and the scene's own visual shows low-r dots swelling and high-r dots shrinking (`contrainte-loi.js` formula 4; default b = 0.4).
   - New text: "The least distorting one is an exponential tilt, known as the I-projection." This also defines "tilt" before s7 and s9 say "the tilted crowd". The term was not defined in narration before; 08.5 says only "reweight".
2. **X3.1 P3: two long sentences for the ear (21 words, one colon and one semicolon).**
   - s6 is now "Picture crowds as points: those with the right average lie on a line." The old line could be heard as "each crowd is a line".
   - s7 is split into "foot" and a new cue `extra`: "Any other fix pays the tilt's cost plus an extra, as in Pythagoras." This states the identity KL(p‖q) = KL(p‖q*) + KL(q*‖q) (R:476-480) instead of only "costs more".
   - The visual is updated: the side labels 'extra' and 'cost of p' now appear on `extra`. Sentence ids are renumbered s7-s9. No scene page exists yet, so nothing else depends on them.
3. **X3.2.s7: overclaim.** "The further off, the smaller the poll" is stated as a rule, but the data show one swap.
   - `data/e2_eval.json` `en_loi`, checked: η = 0.004 has |residual| 0.100 and ESS/N 0.076; η = 0.0067 has 0.141 and 0.116.
   - New text: "...the poll shrinks in nearly the same order." A plain chip 'rank order: one swap (η = 0.004 and 0.0067)' is added.
4. **X3.2 visual: false data claim.** "The ⟨a²⟩ error follows the same order in the data" is not true: against ESS/N, the ⟨a²⟩ error gives three swaps and the cross-helicity error gives no order (14 inversions). The visual text and the source line now say so.
5. **X3.2.s10: unclear logic.** "The three-dial tests agree" did not say what they agree with. E1 also does not show a collapse: ESS/N there is 0.67, and its failure is one heavy weight plus the transfer from half a to half b (R:879).
   - New text: "On the three dials, too, reweighting improved no crowd: one snapshot weighed thirty-three times the average." The "too" calls back to 08.5, "the crowd gets worse", which is R:1033: 2.62 → 4.15.
   - s6 now reads "one snapshot in five hundred" (one word saved, B10 wording kept).
6. **X3.3.s1: the hypothetical model was presented as real.**
   - It now opens with "Picture a model…". The bridge is removed by hand (SCHEMATIC chip), and the old "Now a model that never visits…" could be heard as a result.
   - s3: the colon before "Zero, times any weight, is zero" is now a full stop, for TTS prosody.
7. **X3.4.s2: a 29-word sentence with a physics shortcut.** "The base model dissipates over twice the energy it receives" names neither snapshots nor average.
   - The budget is a crowd law, which is the core lesson of ch07, so "on average" matters: E_q[ε] = 2.22 P at η = 0.0190 (R:1031; `per_eta.V4_potentiels.test.residu_bilan_energie` = 1.2197).
   - The sentence is split: "At the largest, the base model's snapshots dissipate, on average, over twice the energy fed in." / "The crowd loss cuts the distribution distance from seven point seven to two point two." The second sentence has the new cue `cut`, and the visual moves the V5 bar redraw onto `cut`.
   - The label changes from 'the energy it receives' to 'the energy fed in'. s1 is shortened to "One test eta at a time." to hold the pace. Ids are renumbered s4-s7.
8. **Symbol sheet (one meaning per mark).**
   - X3.0 wrote E(P, Q) on the same formula layer as "E1: the state (Q, D, V)", where Q is the quadrupole dial. X3.2 and X3.4 also use P for the injection rate. Changed to E(P₁, P₂), as 06.5 already does, in the equation label and two formulas.
   - X3.4's formula layer used β = 50 for the loss weight in the unit where β means the tilt multipliers (X3.1-X3.3). It now reads "loss weight 50" and "loss weight 0" (R:681).
9. **X3.0.s1-s2: accuracy against 06.5.** 06.5 calls *a* distribution distance a score and the earth-mover *one kind*, and E1 also used sliced W1 (06.5 chip; T:888).
   - New text: "Earlier, a distribution distance meant moving sand." / "The experiments mainly use a cousin, built from pairs."
10. **X3a.Q `why`: overstatement.** "Its risk table rules reweighting out" is stronger than T:992, which says "tilting alone is not a fallback".
    - Also, "one effective snapshot in 500" is E2 only, at the three largest test η (R:1033). In E1 it was ESS/N 0.67 with one weight 33× (R:879).
    - `why` and `why_fr` are rewritten accordingly. `question.chapter: "X3a"` is added, as in the other extension cards (X1, X2, X4a…).
11. **Badges.** A `note` is added to each badge, taken from the visual text, as in ch08 and X2. For example, X3.1 gets 'Prop. 7 · exact on the sample, when β* exists'.
12. **Notes.** The SYMBOLS, LEXICON and PACE sections are updated.

## Checked and correct (no change)

- **Proposition 7** (R:465-485): the I-projection, the dual, the Pythagorean identity, supp q* = supp q, and β* exists only if c is in the convex hull. The formula layers are transcribed correctly, with q* and never ν* (D3), and KL appears only on the formula layer.
- **Energy distance** (R:715-723): the three terms, "zero iff same law", the 1/n bias of the all-pairs estimator, 2·MMD², and the 21 descriptors.
- **E2 ESS** (Table 7, R:999-1013; R:1033; `e2_eval.json`):
  - ESS/N is 0.99 at η = 0.00476 and 0.002 at the three largest test values. With half b = 500, that is the floor 1/500.
  - The mean is 0.287 and the tilt is tuned on half a and applied to half b (R:695).
- **X3.4 numbers** (R:1031; `per_eta`):
  - Distances: 7.74 / 7.63 / 2.22 at η = 0.0190, and 0.184 / 0.178 / 0.186 at η = 0.00476. The control stays at V4's level at all five test values.
  - The three smallest ESS values sit under the three largest absolute V5 gains. There is a slight cost at η = 0.004: 0.41 against 0.364.
  - Floor 0.030 (R:747). Seed and rescaling caveats: R:1175.
- **X3.3**:
  - Rice needs |D| < h (R:507-517). A model missing the bridge appears in R:485, R:826 and T:564, and the risk table in T:992.
  - h = 0.2 matches 05.2. The predict beat is real: X3.1.s9 gives the tool to answer it.
- **Question card premise**: T:890 (the tier-0 stopping rule falls back on tilting) contradicts T:992 (tilting alone is not a fallback). The supervisors named are S. Cheng and D. Lucor (S:110).
- **Continuity**:
  - "Flat sheet", "three dials", "poll … one person", "crowd loss" and "Rice" are all established in ch05-ch09.
  - 08.6 "Reweighting afterwards fails where the model is poor" sets up the card.

## Open points (not fixable in this file)

- **Placement.** In the extended cut, X3a.Q is followed directly by ch08.Q (assembled order: … X3.4, X3a.Q, ch08.Q, 09.1). That is for the consistency editor: fold X3a.Q into ch10q, or move it.
- **Number.** `n` stays null until the question register numbers the card.
- **Typed numbers.** "ESS/N 0.67 · one weight 33× the mean" (X3.2 lower-third) exists only in the report text (R:879), not in `data/e1_eval.json`. That conflicts with a strict reading of CONTRACT §5. One option is a `report_quotes` block in `tools/data_existing.py`; the other is to keep the numbers in narration only.
- **Lexicon.** The pin for "I-projection" (`{"say": "eye projection"}`) and the one for "eta" are not yet in `audio/lexicon.json`.
- **Symbol sheet (outside this unit).** 08.5 uses β for the loss weight on its formula layer.
