# X3b, X4b, X5b review changelog (adversarial script review, 2026-11-08)

Units: `script/X4b.json` (X4.4, after 10.5), `script/X3b.json` (X3.5, after 10.7), `script/X5b.json` (X5.5, X5.6, X5b.Q, after X6).

- **Validation.**
  - The three files are valid JSON with their formatting kept (indent 1, UTF-8).
  - `tools/assemble_cut.py --unit <u> --strict` (output in the scratchpad) gives no warning on the shipped variants.
  - All 8 TeX items render with `vendor/katex` and `Kit.MACROS`.
  - In the assembled extended cut the order is 10.5 → X4.4 → 10.6, 10.7 → X3.5 → 10.9-bridge, and X6.Q → X5.5 → X5.6 → X5b.Q → ch10.Q.
- **Result variants.** Tested with throwaway fixtures in a scratchpad mirror of the assembler, for met, not met and inconclusive, with numeric fields and with today's string fields. Nothing was written to `data/`.

| Scene | Target s | Words | Est. s | Dev. | Result variant (words, est. s) |
|---|---|---|---|---|---|
| X4.4 | 45 | 97 | 45.2 | +0.4 % | 77-89, 35.9-40.9 (target 40) |
| X3.5 | 40 | 85 | 39.3 | −1.8 % | 84-87, 38.8-40.1 |
| X5.5 | 40 | 86 | 40.4 | +1.0 % | 75-81, 35.9-38.4 |
| X5.6 | 45 | 97 | 44.5 | −1.1 % | — |
| X5b.Q | 10 | 18 (16 on screen) | 9.9 | — | — |

## Changes (what, why, evidence)

1. **X4.4: "branch stability" meant the wrong thing.**
   - To a dynamicist, "branch stability" is the stability of a solution branch, and the upper branch *is* stable (P4:567-575).
   - The conjecture's open hypothesis is *statistical* stability along each branch: λ ↦ μ_{λ,b} Lipschitz, "not established in general for turbulent systems" (T:788-791).
   - s7 now reads "statistical stability along branches is unproven in turbulence". `seat.why` was changed the same way.
2. **X4.4: the published numbers sat on the wrong scale for this place in the film.**
   - 10.5, just before, shows "Rm_c ≈ 30 at Pm = 1" and says that published runs define the Reynolds number differently.
   - The old s4, "switched on near two hundred, yet held on down to seventy", gave raw numbers on another scale.
   - s4 now gives the scale-free fact: "a dynamo, once on, survived down to a third of its threshold".
   - Checked in the arXiv PDF of Ponty et al. 2007: onset R_M^c = 206 at R_V = 563; Table I, point A9, R_M = 70 with b = 1.6; A10, R_M = 56, b = 0. So 70/206 = 0.34.
   - The chip keeps 206 and 70, and a new on-screen label gives "held down to about a third of the onset".
3. **X4.4: tied back to 09.3.**
   - 09.3 ends "Unless it is very supple, or told which state the system is in". X4.4 is the payoff of both escapes, but called the second machine "steeper".
   - s2 now reads "A stiff machine rounds the corner; a supple one errs less, but turns jumpy everywhere" (Prop. 2.36 and T:780: a larger K lowers the error but raises the sensitivity everywhere).
   - The labels, the generator labels and the visual were updated to match, and the second curve now enters at 'round+2.4', on "a supple one".
   - The 09.3 quotation in `sources` was wrong and has been replaced by the actual text.
4. **X4.4 smaller changes.**
   - "knob" is marked {param}.
   - s6 was shortened ("its threshold error at least halves").
   - The ASK is now "from which saturated runs, and how far down?" (palier2_tg3d.yaml:34: every run starts from a 10⁻³ seed).
   - Formula 3 now says the error tends to zero "as training parameters get denser", as in T:788.
5. **X3.5: the ASK posed a non-question.**
   - "Impose it near the threshold, where runs may still be growing?" is not a real choice: the crowd law holds for any statistically stationary state, near the threshold too. The conflict is between the law and snapshots that are not yet stationary (A8).
   - The loss is imposed over the whole normalised range, `cond_range [0, 1]` (train_fm3d.yaml:110).
   - The ASK is now "where runs may still be growing, trust the data or the crowd law?" The notes spell out both options, and the link to 10.5's ASK (lengthen or exclude).
6. **X3.5: wording aligned with the core.**
   - s4 "three-variable test … narrowed the budget's spread … failed from a poor start" now uses 09.4's words: "On three dials, the loss shrank the spread of energy changes, and failed from a biased start" (R:875 σ(dE/dt)/σ_ref 1.04 → 0.75; R:877 two fine-tunings out of two unusable).
   - "budget error" and "spread" are marked {metric}, since amber is used in the lanes.
   - s2 was shortened ("an equal-length control run").
   - Numbers re-checked: R:956-957 (0.0611 vs 0.462), `data/e2_eval.json` (0.061117, 0.461716, 0.788209, 0.66268), and T:903 (b) and (d).
7. **X3.5 result: two errors.**
   - r2 "Each lane shows the budget error" was wrong, because lane 3 shows the spread. It now reads "Dots mark each scored setting: budget error with the loss, then with the control, then the spread."
   - r5 said "the crowd *law* carries over". The physics law is not what is being tested; it now reads "the crowd *loss* carries over".
   - The ghost entrance times now follow the narration (`ghost_2d.at`: race+4.2 / 5.8 / 7.6 instead of 0.4 / 2.6 / 3.8, which came before the words).
   - "(A8)", a critique id, was removed from an on-screen chip.
8. **All three result variants: the bet was never restated.** In v2 the viewer would have heard "Verdict on the bet: met" without the bet. Each verdict line now states it first, for example "The bet: the branch at least halves the error. Verdict: {{verdict}}." 10.4 restates its bet the same way. The meaning lines were shortened to stay within budget.
9. **Placeholders read aloud.**
   - `{{ratio}}`, `{{worst_residual_percent}}` and `{{measured_hours}}` would read all digits of a float (2.3456 → "two point three four five six"), or digit strings with today's `say()` output.
   - They are now `{{ratio:1}}`, `{{worst_residual_percent:1}}` and `{{measured_hours:0}}`. The modifiers are ignored for strings, so both data shapes work.
10. **X5.5 result claimed work the converter does not do.**
    - r2b ("each measured hour is converted to the plan's class of card") was unconditional, but `conv_bill` converts nothing.
    - It is now gated on `fields.a100_factor`. A new r2c ("These are raw hours, not yet converted…") speaks when the factor is absent, and the visual tags match.
    - r4 no longer says "like for like", which is not true for raw hours.
    - New request (d), from C:141: `wall_time_s × max(n_gpus, 1)` gives GPU hours only if each simulation had its own GPU. palier2_tg3d runs up to 12 on one VM GPU (yaml:55), so the measured bar could be up to twelve times too high.
11. **X5.5 not_met, and the pending variant.**
    - not_met assumed an overrun. A ratio below 0.5 is also "outside the band". It now reads "rescale the plan; if costs run over, the three-dimensional box can drop resolution first" (T:974).
    - Pending s3 said lines "scale up" the PCDM run. Most lines scale *down* from it (latent ≈ a quarter, 2D ≈ 1/16 per iteration, T:959-961). It now reads "are scaled from one published training run".
    - s6 now reads "the plan's own error bar is at least twofold" (T:974; C11). The scene is at 86 words.
12. **X5.6 changes.**
    - s4 "the top two … on top under all three weightings" now reads "the two best-scored of six directions; they stay on top under all three weightings tried" (S:433).
    - s5 now reads "Among its named risks:". The table names nine (T:988-1000), and the film shows four.

## Checked and correct (no change)

- **Prop. 2.36** (T:768-780): square-root bound, an error proportional to 1/K over a window proportional to 1/K², an infinite slope at the threshold.
- **Remark 2.37** (T:783-785): a knob-only blend whose weight is set by the protocol.
- **Criterion (d)** (T:917): the error halved.
- **Risk ratings:** T:992 and T:996.
- **Schedule:** months 13-15 (T:1048).
- **P4 Prop. 3.7:** branches, fold at −1/4.
- **X5.5 budget figures** (T:957-974): 700, 3900, 3200 and 1200, totalling 9000; × 1.2 = 10 800 ≈ 1.1 × 10⁴; PCDM ≈ 1150; H1-H5; CPU ≈ 2 × 10⁴ h "and more"; 0.08 s per step at 64³ (C:153).
- **X5.6:** the schedule against T:1040-1063, papers at months 10, 22 and 33 (T:1014), scores 4.10, 3.90 and 3.50 (S:422-433, with the caveat S:437), and the funding risk (T:982, T:1000).
- **X5b.Q:** the question is on the plan's own list (T:1000), is ≤ 18 words on screen, runs 9.9 s, and the FR, why and unblocks fields are consistent. No other card asks it.
- **Badges** are present and fit each scene: CONJECTURE low ×3, PLANNED, none on the card.
- Every pending scene has its anchor, bet, criterion, confidence, ASK and result variant.

## Remaining doubts (for the lead or the foundation engineer)

- **Duration targets.** These were raised against the outline (X4.4 25 → 45 s, X3.5 25 → 40 s, X5.5 30 → 40 s). I kept the raises: the BRIEF §3.2 framing does not fit in 25 s. The extended cut gains about 55 s with the new card.
- **Booleans in the data.** Without the met / not_met / inconclusive booleans in `fields` (requested in all three notes, and by ch10 and X4a), no "meaning" sentence plays. The X4.4 "met" path then drops to 70 words.
- **Result-variant targets in the lint.** The assembler lints result variants against the scene's `target_s`, not `variants.result.target_s`. X4.4 inconclusive (35.9 s, −10 % of its 40 s) is flagged against 45 s.
- **X4.4 v2 loses the learning goal.** The result variant drops the supercritical (Prop. 2.36) half of the learning goal. That is acceptable as an aside, but worth knowing.
