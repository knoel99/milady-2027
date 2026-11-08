# Adversarial review of X4a "What snapshots can and cannot tell" (script/X4a.json)

Reviewer pass, 2026-11-08. I checked the script against R (en/rapport), T (en/these), P4, S (en/encadrants), the data files, `experiences/resultats/e1_gissinger.json`, `experiences/e1_gissinger.py`, `tools/data_cloud.py` and `tools/assemble_cut.py`, plan/critique_accuracy.md, critique_pedagogy.md and pedagogy.md P15, and the neighbouring units ch05, ch09 (09.4-09.6, ch09.Q), X2, X3a and ch10. I also read Gissinger 2012 (ar5iv 1109.6569) as data. Nothing outside `video/` was touched. The assembler lint was run on `--unit X4a` (auto and result variants) and `--cut extended`, with output in the scratchpad. The only X4a warning in auto is the known missing `data/ch05_rice.json`. In the result variant, the expected "data missing" warnings appear.

## Verified as correct (no change)

- Data: `e1_samples_0.93.json` has 26 of 8,000 reference snapshots with |D| < 0.2. `e1_samples_0.9.json` has 21 such snapshots, median |D| 1.06 and 99 % below 2.28. `e1_finegrid.json` gives a counted zero-crossing rate of 0.00442 at Γ = 0.9.
- Statements: Prop. 2.30 (r₊₋ ≤ ν₋ₐ/2, so r ≤ r_a; r_a counts one level, both ways), Prop. 2.31 (bias G''(0)h²/6, variance M(0)/(2Nh), error² ∝ N^-4/5), Prop. 2.32 (ω₂ = √7 ω/2, same (D, Ḋ) law), Example 3.10 (cosine), Conjecture 2.33 (T:727) and the tier-0 criteria (a)-(d) (T:889) all match the site.
- R_π on the Gissinger model, (Q, D, V, Γ) → (Q, −D, −V, −Γ), was re-derived from the three equations and matches T:603.
- Numbers: S:98 values for DQVU. R:875 values: 0.0113 / 0.0224 = 1.983. The floor is √(2/π)/(2√n) = 0.00399 for n = 10,000. P(|Z| > √(2/π)) = 0.425.
- Gissinger 2012: Fig. 12 and eq. (17) are confirmed at the source. The figure shows oscillations at short waits ("quantification of the unstable periodic orbits") and a Poisson law at long waits, at μ = 0.119, ν = 0.1, Γ = 0.9.

## Changes

| # | Scene | Change | Why (evidence) |
|---|---|---|---|
| 1 | X4.1 s1 | "Rice's formula, as an estimator." → "How wide should Rice's strip be?" | Pedagogy: the aside opened on a label right after 09.6. It now opens on the question the scene answers (motivation before formalism). The title stays on screen. |
| 2 | X4.1 s5 | "Why not shrink it to nothing?" → "With endless snapshots, why not shrink it to nothing?" | Logic: the question came right after "Narrow it: the estimate jitters", so the viewer's answer would be "because of jitter", while the narration answered about the density. Ruling out the variance makes it the real question of R:528. |
| 3 | X4.1 s7 | "Chaos may lack a smooth cloud too. So on three chaotic dials…" → "…too, so nothing guarantees the limit: on the three dials, the only test so far, the answer depends on the strip." | Non-sequitur. The cosine example shows a missing density is not fatal, so "So" did not follow. R:528 and R:901 give the reason: not guaranteed, so a finite h is kept. "Chaotic" was dropped after "Chaos". |
| 4 | X4.1 s4, s2, s6 | "kept snapshots within" → "used snapshots within". "Widen the strip" → "Widen it". "cloud of states" → "cloud". | "Kept" could be heard as E1 confining its snapshots. The other two edits trim words. |
| 5 | X4.1 target | 40 → 42 s | The fixes add 6 words (98 words; assembler 43.5 s; +10 % effective). |
| 6 | X4.2 s4 | "with slow flips and fast jitter, a band of levels makes it nearly exact, a plateau" → "if a flip lasts far longer than a wobble, the cap is nearly exact on a plateau of levels" | "Slow flips" can be heard as *rare* flips. Conjecture 2.33 is about flip *duration* against the correlation time (T:727). "It" had no clear referent. "Wobble" reuses s3's word, and the plateau is now defined in the sentence. |
| 7 | X4.2 s2 | "crossing rate" now carries `{metric}` markup | Colour key, as in 05.2 and 09.1. |
| 8 | X4.2 label | "(Rice: from snapshots)" → "(Rice: snapshots + equations)" | critique_accuracy line 51: snapshots alone cannot give a rate. |
| 9 | X4.2 r8 | "read from snapshots alone" → "from its snapshots and the equations, with no time series" | Same error as #8 (critique_accuracy line 51), in the result variant. |
| 10 | X4.2 r5 | "the cap sits within {{best_gap_percent}} percent … Rice can count reversals" → "stays within thirty percent …, and comes as close as {{best_gap_percent}} percent: on this model, the plateau is real" | A *best* gap does not bound the whole plateau. The old line also overclaimed beyond tier 0 (a three-variable model). The visual's data contract now defines best_gap_percent. |
| 11 | X4.2 r6 | "No level brings the cap within thirty percent…" → "No band of levels passes the test, so on this model the plateau is missing; the conjecture waits for the sodium experiment's simulations." | not_met also covers an estimated cap that falls below r (verdict rule "r ≤ r_a everywhere and …"). "The next step" was vague: T:731 says tier 0, then the VKS series. |
| 12 | X4.2 seat.why | "+ on dials without turbulent jitter (T:1006)" | Reason for medium confidence. Tier 0 has no turbulent chattering, so it tests the conjecture's premise only loosely. |
| 13 | X4.5 s8 → s8 + s9 | The "catch" line had no question in it. It is now split into "One catch: a perfectly symmetric model lands above the noise floor nearly half the time; the floor is its average." (new cue `catch`) and "Ask first: should the first lamp use a statistical test?" (cue `ask`). Visual and formula cues updated. | BRIEF 3.2 asks for a question to settle before compute, as in X4.2 and ch10. The old line ended without one. "Nearly half" holds for the criterion's mean of 2–3 seeds: P ≈ 0.45 (computed). For one seed, P = 0.42. The formula layer now says both. |
| 14 | X4.5 s5, s6, r3, r4, lamp b | "never-imposed residuals" → "unenforced laws / unenforced residuals". The bet is now "unenforced residuals halve again, roughly. Last time, halving meant one point nine eight, against a bar of two: a toss-up." Lamp b label: "crowd laws not enforced: residuals ÷ 2 vs control, Γ without data". | Continuity: 09.4 narrates "it halves the crowd-law residuals, even for laws it never enforced", and its label reads "crowd laws not enforced". The bet now pays that off: 09.4's "halves" was ×1.98, just under the ÷ 2 bar. The bar is now said aloud (the old line said only "stays near two"). |
| 15 | X4.5 s4 | "And a mirror that also flips the forcing." → "And the impeller-swap mirror, which also flips Gamma." The tile label adds "· the impeller swap", and an X2.4 two-impeller glyph sits in the visual. | "Flips the forcing" can be heard as reversing the drive. In the Gissinger model, the image of R_π flips the sign of Γ (T:603). X2.4 (played earlier in the extended cut) introduced the impeller swap and the forcing asymmetry. |
| 16 | X4.5 s3 | "distilled from simulations of the sodium experiment" → "distilled from VKS simulations" | ch02 shows three sodium experiments, so "the sodium experiment" is ambiguous (same finding as the X2 review). VKS is pinned in the lexicon. It also saves 3 words. |
| 17 | X4.5 lamp c label, sources | "14 % cumulative … 42 % near" → "cumulative 14 % far from the threshold (pointwise up to 65 %), 42 % near". The source now says 65 % at *two* values (0.905 and 0.91), not "one value". | pedagogy P15 (keep the cumulative and pointwise figures together), R:883, 09.1 ("at two settings"). |
| 18 | X4.5 sources, notes | Added: per seed, E1's model C sits near 0.002 for one seed and 0.006–0.007 for the other at **every** Γ. The mean is above the 0.0040 floor at 19 of 21 Γ. The reason: `torch.manual_seed(1000 + seed)` before each Γ (e1_gissinger.py:284). | This is evidence for the ask: a model that is symmetric by construction fails lamp (a) read literally. It also shows the 21 values are not independent draws, which the "at each Γ" probability must not hide. |
| 19 | X4a.Q | "should we also target waiting times, with short solver runs launched from generated states?" → "Beyond how often: for VKS, should we also target waiting times, with short solver runs from generated states?" (18 words). The why/why_fr now say "snapshots plus the equations" and "tier 0 already plans them cheaply (T:888)". | Tier 0 already lists waiting times from generated states as a metric (T:888), so the open decision is the VKS tier: partner solver time and valid starts, which C. Nore and Y. Ponty can answer. #8 also applies to the why ("snapshots fix how often"). The card is 9.9 s, under 10. |

Durations after review (assembler: 146 raw wpm plus pauses; "effective" = words at 127.5 wpm plus holds):

| Scene | Words | Target | Assembler | Effective |
|---|---|---|---|---|
| X4.1 | 98 | 42 | 43.5 | 46.1 (+10 %) |
| X4.2 | 105 | 45 | 48.3 | 50.2 (+12 %) |
| X4.3 | 82 | 35 | 36.7 | 38.6 (+10 %) |
| X4.5 | 92 | 40 | 41.6 | 43.9 (+10 %) |
| X4a.Q | 18 | 9 | 9.9 | 9.3 |
| Module | 395 | 171 | 180 | |

Result variants are within ±15 % of 45 s and 40 s in every branch. X4.2 met: 97 words, 46.1 s.

## Remaining doubts (not changed)

- **Lamp (c) wording.** T:889 does not say whether "within 20 %" is cumulative or pointwise. The first round passes cumulatively (14 %) and fails pointwise (65 %). This could be a second ask. It was not added, to keep one ask per seat.
- **Stakes of lamp (b).** T:890: if (b) fails with the unbiased estimator and three seeds, the loss is dropped for tilting. That is high stakes for a toss-up, but it is not narrated, because X3a.Q already asks about the fallback. The result variant (r6, "stays dark for now") does not invoke the stopping rule: the E1 rerun is not the full tier-0 campaign.
- **Data.** X4.1 waits for `data/ch05_rice.json`. X4.5 needs `data/X4a_tier0_anchor.json` (foundation engineer) and the conv_tier0 changes the writer requested: numeric n_seeds, resid_ratio, resid_met and cumulative_error_percent. As written, "{{n_seeds}}" would come out as digits.
- **Symbol sheet r_a.** The writer's request stands: the sheet and 05.4 should read "crossings of the level a (either way)".
- **Running order.** X4a.Q plays right before ch09.Q (two cards back to back). This is for the question register and the lead.
