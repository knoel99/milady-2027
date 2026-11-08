# Adversarial review of chSOA2 "The map of the field: where this work fits" (script/chSOA2.json)

Reviewer pass, 2026-11-08. I checked every narrated sentence, on-screen label, pin citation, gate verdict and the question card against:

- `video/ETAT-DE-L-ART.md` §1.4-3.5 and `video/plan/state_of_the_art.md` §0-7;
- the site lines they cite (R, T, E, S, L and Dy);
- `video/BRIEF.md` §1-6, 9 and 10;
- the neighbouring units: chSOA1 (whose map this unit reopens), ch09 (09.6 and ch09.Q), X4a and ch10 (10.1).

I treated external sources as data:

- the arXiv abstracts and OpenAlex/Crossref records the writer saved in the scratchpad (`soa/chSOA2_check/`);
- four full texts I read today:
  - arXiv:2507.02106 (Kacmaz, Huerta, Haas);
  - arXiv:2603.12834v1 (PCDM);
  - arXiv:2405.19256v2 (Weak Generative Sampler);
  - the abstract of arXiv:2412.01786v2 (ECI).

Nothing outside `video/` and the scratchpad was touched, and nothing was committed. After the fixes:

- `tools/assemble_cut.py --unit chSOA2 --strict` passes with no warning: 653 words, about 294 s.
- A scratch outline with `extra_units` `{"unit": "chSOA2", "before": "ch10"}` puts the unit right after ch09.Q in the core cut and right after X4a.Q in the extended cut. In both cuts it is followed by 10.1.
- The JSON is valid. The formatting round-trips byte for byte, with indent 1 and literal UTF-8.

## Verified as correct (no change)

- **Bousquet et al. 2026 (abstract re-read).** "Two numerical solvers … agree well on the resulting mechanism". The U variable and its interactions "are shown to be essential for reproducing the main features of magnetic field dynamics". This supports SOA2.6.s3. MilaDy funding is confirmed by S:31 and S:99.
- **Bousquet, Nore, Lucor 2025.** The AE/VAE models are trained on Navier–Stokes *velocity* fields (the OpenAlex abstract), so the paper is hydrodynamic. "None of the four has published a generative model trained on dynamo data" therefore still holds, and it is said with "in what we found" [NEG; E:513-519; S:103; S:299]. The pin keeps its "not MilaDy-funded" tag.
- **TorchDA (abstract).** Kalman filter, EnKF, 3DVar and 4DVar, with deep networks as the transition and observation functions. Kreuzahler et al. 2017 (abstract): an axisymmetric mode above a permeability threshold.
- **Other quotes and abstracts:**
  - the PBFM quote is verbatim (arXiv:2506.08604v4);
  - "regress to the mean flow" is in the arXiv:2409.18359v2 abstract and is attributed to the preprint;
  - the Galletti et al. abstract has statistically steady, saturated states conditioned on dimensionless parameters;
  - the da Silva et al. abstract has a diffusion model in the spherical-harmonic domain, where the scalar is the magnetic potential;
  - Gwirtz et al. 2022 found no reliable precursor, and the record holds five reversals.
- **Site facts:**
  - R:137, Pm = 0.82e-5;
  - R:149, 5 s against 120 s and 50 s;
  - R:161;
  - R:240-245;
  - T:57, the independent proposal, not requested or validated;
  - T:94, "the model remains far from the data", which matches the E2 MEASURED tag;
  - T:111-117 and T:156-158;
  - E:491, E:496 and E:506-520.
- **Supervisor pins.** Every ring and diamond says only what the cited paper showed. The narration names no person and attributes no opinion or intention. The CONJECTURE badge on SOA2.8 and the "search result, not a proof" sentence follow E:520.

## Changes

| # | Where | Change | Why (evidence) |
|---|---|---|---|
| 1 | `insert_after`, notes | `extended`: "ch09.Q" → "X4a.Q". The ANCHOR note is rewritten. | The writer said X4a sits before ch09.Q. It does not: `script/X4a.json` has `insert_after` "ch09.Q", and the unit's string overrides the outline's "09.6". The extended order is 09.6, ch09.Q, X4.1…X4a.Q, SOA2.1 (assembler, scratch outline). |
| 2 | SOA2.1.s1 | "The scoreboard was for toy models. Before climbing toward real dynamos, step back to the map of the field." → "So far, every test ran on toy models. Before real dynamos, back to the map of the field." | The new line is true after both predecessors: ch09.Q in the core cut, X4a.Q in the extended cut. It also saves 2 words. |
| 3 | SOA2.1.s3 | "three dimensions, walls, vacuum and iron, a tiny Pm, and flips that are rare" → "three dimensions, walls with iron and a vacuum, a tiny Pm, and rare flips" | Read aloud, the nested list sounded like six tests, not four. |
| 4 | SOA2.1 card | `num` "MAP" → "09+". New field `levelFrom_by_cut` {core L4, extended L5}, with a side-step note. | chSOA1 uses "02+". In the extended cut the unit follows X4a.Q, which is L5. |
| 5 | SOA2.1 map | `from_chSOA1` and the visual now describe the map chSOA1 actually leaves: the INTERN dot and the THESIS ring, not "? · 2027-", plus chSOA1's pin ids. New `carry_over`: D2022 and D2016 go to SURROGATES. The ring glyph now reads "co-signed by a supervisor". | chSOA1 SOA1.1 `catalog` and SOA1.6. The Gwirtz pin sits in DATA-DRIVEN, not EARTH'S RECORD, as the writer had it. |
| 6 | SOA2.2.s4 | "a twenty twenty-two study found that the machine-learning methods it tried…" → "recall the twenty twenty-two study: the methods it tried…" | chSOA1 SOA1.6 already narrates this study, so this is now a callback. It saves 2 words. |
| 7 | SOA2.3 sub-tags | WALLS "no divergence constraint" → "irregular domains · no divergence constraint found". RARE "user-defined events · never a dynamo" → "user-defined events · none on a dynamo found". | Plan "Non vérifié": "no physical constraint" for TurbDiff and CoNFiLD is read from silent abstracts. "Never" is a negative claim, so it must be said as "found". |
| 8 | SOA2.4.s2 | "or project every sample at the end" → "or project each sample while drawing it" | ECI corrects "during each iterative sampling step" (abstract). PCFM projects at each step and then once more at the end (L:270). |
| 9 | SOA2.4.s6, c_cmp label | "A 2026 comparison on flat flows found that no single strategy dominates" → "A 2026 preprint compared ways to impose zero divergence on flat flows: no single strategy dominates". The label adds "divergence only". | After the four families, the old line implied the paper compared all four, which overclaims its scope. Genuist et al. compare Leray/divergence variants only, in 2D (abstract; L:279 says "La comparaison porte sur la seule divergence … préciser « préprint 2026 »"). |
| 10 | SOA2.4.s7 | "the turbulence generators we found … work in a periodic box; another …" → "we found two exactly divergence-free generators, both preprints: periodic-box turbulence, and a current-free field in the Sun's corona" | Only one 3D turbulence generator was found (PCDM), so the plural was wrong. Both are preprints, which the narration never said. Li X. 2026 is 2D (L:289-292). |
| 11 | SOA2.4 pins | c_pcdm, c_wgs and c_proj cites now say what was read today. PCDM: periodic domain (App. A.1) and "divergence-free at machine precision" (§IV.3). WGS: d = 100 (§4.5). ECI: the abstract. | These numbers were on the plan's "do not show without a new reading" list. They are now verified. |
| 12 | SOA2.5 | s1 and s2 tightened (−2 words). The RARE sub-tag "two polarities not studied" → "two polarities · none found for MHD". The ring legend now reads "met in SOA1.4", not "first appearance". | NEG wording. chSOA1 introduced the ring in SOA1.4. |
| 13 | SOA2.6.s1, badge | "the supervisors' own papers" → "papers co-signed by the supervisors" | Several rings are co-authored, not "own": Kreuzahler et al. (Ponty second author), Cai et al. (Lucor last), Bousquet et al. The new wording matches chSOA1 SOA1.4. |
| 14 | SOA2.6 pins | Added `reuse` ids: S1997, S2005, S2016, S2017, [S2026B, R2026] and S2026C. r_nore97, r_ponty05 and r_ponty07 now sit on SIMULATIONS, as in chSOA1. The Botez diamond keeps its green tick. The Bousquet names now read "Y. PONTY, C. NORE et al." (author order, as in chSOA1). The visual is updated. | Before, the same papers jumped lanes between the two map visits (chSOA1 catalog). |
| 15 | SOA2.6.s4 | "the latent spaces of autoencoders, read…" → "autoencoder latent spaces read…" | Pace (−2 words). |
| 16 | SOA2.7.s1 | "…cross the dynamo tracks, the map is empty" → "…we found the map empty" | A negative claim must be said as "we found" (plan §0 and §6; E:520). |
| 17 | SOA2.7.s2 | Dropped "from fall twenty twenty-seven" and "pinned". The ring now carries `years_note` and `from` (chSOA1's THESIS ring moves into the crossing). | T:49 gives fall 2027 as a "working assumption", not a fact. The ring label already shows 2027-2030. |
| 18 | SOA2.7 tag | "E1 · Rice on three dials · far ✓ · near ≈" → "far ≈ · near ✗" | T:88 gives 14 % error far from the threshold and 42 % near it. 09.6 says "roughly right far from the threshold, poor near it". The old tag overstated both. |
| 19 | SOA2.7 gap 1 | `lacks` "no zero divergence of B in the generator" → "2D, where a self-sustained dynamo is ruled out (Zel'dovich); Pm = 1 only" | In the Kacmaz et al. full text, the model's magnetic channel is the vector potential A (B = curl A). B is therefore solenoidal by representation, which contradicts R:240, T:163 and L:301 (see below). Pm = 1 and the 0.85 error of gap 5 were verified in the same text. |
| 20 | SOA2.7.s8 | Tightened (−3 words) | Pace. |
| 21 | SOA2.8.s2 | "The study's result on constraints forced on each snapshot must be placed against it." → "The study's lesson, never force a crowd law on each snapshot, must be placed against it." | This states the claim being positioned (R:121, T:157), using 09.6's own words ("Crowd laws: … never on each snapshot"), for the same word count. |
| 22 | chSOA2.Q | "should the generator learn the LATU periodic grid" → "First VKS data: should the generator train on the LATU periodic grid, or the SFEMaNS cylinder mesh?" (17 words, 9.5 s). In `why`/`why_fr`, "reproduce VKS reversals" → "produce reversals in simulated VKS". Both now also say that E2's Fourier basis alone no longer suffices and that SFEMaNS controls ∇·B only weakly (R:1185). | A generator learns fields, not grids. "Reproduce" could be heard as matching the experiment. The added nuance comes from the very line the card cites. |
| 23 | holds | `hold_after` 0.4 s after the first paragraph of SOA2.4 and SOA2.6, and after the gap list of SOA2.7 | This leaves time for the strands, rings and gap pins to land. Each scene stays within ±15 % of its target. |

## Pace

The writer stated 125-130 effective words per minute. In fact the draft had 671 words for 300 s of `target_s`, which is 134 wpm. Scenes SOA2.4-SOA2.7 ran at 137-141 wpm.

After review the unit has 653 words, about 131 wpm, with an assembler estimate of 294 s. The neighbouring units run at about the same pace: ch08 133, ch09 136, ch10 132, X4a 140.

| Scene | Words | Target s | Assembler s | Words per min of target |
|---|---|---|---|---|
| SOA2.1 | 53 | 28 | 27.1 | 114 |
| SOA2.2 | 76 | 34 | 33.3 | 134 |
| SOA2.3 | 48 | 23 | 22.4 | 125 |
| SOA2.4 | 113 | 50 | 49.1 | 136 |
| SOA2.5 | 66 | 29 | 29.2 | 137 |
| SOA2.6 | 96 | 42 | 42.0 | 137 |
| SOA2.7 | 111 | 52 | 49.0 | 128 |
| SOA2.8 | 73 | 32 | 32.5 | 137 |
| chSOA2.Q | 17 | 10 | 9.5 | 102 |

## For the lead (outside this file)

1. **Site discrepancy (Kacmaz et al. 2025).** R:240, T:163 and L:301 say this generator "does not enforce ∇·B = 0". The arXiv:2507.02106 full text, read 2026-11-08, shows something else. The solver evolves A "to satisfy the solenoidal constraint … to machine precision", and the model's data channels are "the velocity and magnetic vector potential". So in this 2D model, B = curl A would be divergence-free by representation. The same point should be re-checked in:
   - `ETAT-DE-L-ART.md` §1.4 A1 and §3.2 G1;
   - `plan/state_of_the_art.md` §5 gap 1;
   - E:514 context and R:240.

   It does not touch gap 1 itself: the model is still 2D and still Pm = 1.
2. **Placement.** The assembler still needs `{"unit": "chSOA2", "before": "ch10"}` in `extra_units` (outline or `EXTRA_UNITS`). With it, the order is right in both cuts.
3. **French narration.** chSOA1 already carries `text_fr`. chSOA2 does not yet (French wave, BRIEF §9). The question card's `fr`, `why_fr` and `unblocks_fr` are updated.
4. **Not verified today, not narrated:**
   - the Botez et al. 2026 full text;
   - the Zhuang et al. 2025 abstract (the title supports the label);
   - the gate verdicts, which are our synthesis and carry a chip saying so.
