# chSOA1 review changelog (adversarial script review, 2026-11-08)

Unit: `script/chSOA1.json`, "A century of dynamo hunting" (6 scenes, L1 to L2). The JSON validates and keeps its serialization (UTF-8, indent 1). `tools/assemble_cut.py --unit chSOA1 --strict` passes with 0 warnings and 0 errors; the check's build outputs were deleted. All 3 TeX items render with `vendor/katex` and the kit macros. Original file: `/tmp/claude-0/-home-user/7f944193-0bd4-5776-8423-148e13f15fcf/scratchpad/soa/rev_soa1/chSOA1.orig.json`.

Checked against `video/ETAT-DE-L-ART.md` (§1.2, §1.3 D1-D5, §2.1-2.3), `video/plan/state_of_the_art.md` (§0-2, §4, §6-7), the site lines cited in each scene, `specs/sources/encadrants.md:25-35, 215-242`, and these primary texts read today: the OpenAlex abstracts of Berhanu et al. 2007, Ponty et al. 2005, Nore et al. 2016, Kreuzahler et al. 2017 and Bousquet et al. 2026; Stefani et al. 2018 (arXiv:1803.03421, §2.1); Rincon 2019 (arXiv:1903.07829, §1.3-1.4); Constable 2003 (§1); and the Crossref title of Brunhes 1906.

## Changes

1. **SOA1.3.s4: "the first flips seen in a laboratory" became "the first flips of a turbulent sodium dynamo"** (FR: "les premières inversions d'une dynamo turbulente au sodium").
   - Berhanu et al. 2007 make a narrower claim in their abstract: "the first experimental observation of reversals of a dynamo field generated in a laboratory experiment based on a turbulent flow of liquid sodium".
   - Stefani et al. 2018, §2.1, say that the iron-cylinder models of Lowes and Wilkinson "even led to a sort of reversals similar to those of the geomagnetic field (Wilkinson 1984)". That pin sits two sentences earlier in the same lane, so the broad wording was an overclaim.
   - A source line was added.

2. **SOA1.4 pin labels no longer suggest that a supervisor is first author** (catalog in SOA1.1 `entry.params.catalog`, SOA1.6 labels and visual). The author lists were checked today in OpenAlex.
   - S2017 "Y. PONTY et al." became "KREUZAHLER, Y. PONTY et al. · 2017".
   - S2026B "Y. PONTY, C. NORE et al." became "BOUSQUET, Y. PONTY … C. NORE · 2026".
   - S2026C "C. NORE et al. · 2026" became "BOTEZ, GIESECKE, C. NORE et al. · 2026". In Botez, Giesecke, Nore, Cappanera, Stefani, C. Nore is third author (E:100).
   - Line 2 of these pins now carries the journal.

3. **SOA1.4.s8: "inside a conducting layer" became "with conducting surroundings"**, and the on-screen label became 'conducting surroundings'.
   - The paper's words are "a conductive surrounding medium was found to be necessary for these inversions to occur" (S:231). E:98 says "a conducting outer medium".
   - FR: "les deux codes obtiennent des inversions … avec un milieu conducteur autour". The old "les deux la font s'inverser" had an unclear "la".

4. **SOA1.4 Ponty et al. 2005: the method is now on the formula layer and in the pin's line 2** ("DNS, Lagrangian-averaged model, LES"; "DNS + LES").
   - The abstract says the dynamos down to P_M = 10⁻² come from "a three-pronged numerical approach". At the lowest Pm the result relies on turbulence models (ETAT §2.3, D1.d: an LES plateau for 10⁻² ≤ Pm ≤ 10⁻¹).
   - The narration ("such dynamos still work at a Pm of one hundredth") is the abstract's finding (i) and is kept.

5. **SOA1.6.s1: "MilaDy began in twenty twenty-six, where tanks, computers and dials meet" became "…, bringing machine learning where tanks, computers and dials meet".**
   - MilaDy's title is "Machine learning modelling for turbulent Dynamos" (S:28, ANR page). The old line placed a machine-learning project on the map without saying what it brings.
   - The MilaDy callout gains the line 'machine learning for turbulent dynamos' (`params.milady.subtitle`).
   - The takeaway was aligned. Nothing in it is an opinion or an intention: it is the published title.

6. **SOA1.6.s2: "one study's machine learning could not…" became "Yet the data-driven lane is thin: … the learning methods one study tried could not reliably foresee a geomagnetic flip."**
   - This keeps the scope of Gwirtz et al. 2022 ("the ML techniques we tried"), reads better aloud, and links to s1 with "Yet".
   - FR: "les méthodes d'apprentissage essayées par une étude".

7. **SOA1.6.s4: "Every lane starts from the same race" became "Behind every lane, the same race: stretching against smudging."**
   - The Earth's-record lane does not "start from" the induction race; every lane is about the dynamo that the race describes.
   - FR: "Derrière chaque piste, la même course : l'écoulement étire le champ, la diffusion l'estompe". This replaces "étirer le champ plus vite que la diffusion ne l'estompe", which stated the winning condition rather than the race. It uses the two verbs of 03.1.s1 ("the flow stretches the field, and diffusion smudges it").

8. **SOA1.1.s1: "Those three tanks crowned a hunt of nearly a century" became "Riga, Karlsruhe and VKS crowned a hunt of nearly a century."** The line just before it is the Pm question card (ch02.Q), and 02.4 is about 75 s back, so "those three tanks" had nothing to point to by ear. The three thumbnails come back on the same cue. The word count is unchanged.

9. **SOA1.3.s1: "Lane three, building one" became "Lane three: building a dynamo"** (FR "Troisième piste : construire une dynamo"). The bare "one" could only be resolved from the scene title.

10. **SOA1.2.s2:** "moving, conducting fluid" became "a moving, conducting fluid", for the ear.
11. **SOA1.1.s5 (FR):** "dont les chances changent" became "dont la probabilité change". Cox 1968 models p, the probability of a reversal per cycle.

12. **Placement: `insert_after` is now the string "ch02.Q"** (BRIEF §5 form; the same anchor in both cuts).
    - `tools/assemble_cut.py` tests `anchor in alias`, and alias is a dict. An object-valued anchor would raise `TypeError` if the unit were ever listed as a module.
    - The core cut still needs `{"unit": "chSOA1", "before": "ch03"}` in EXTRA_UNITS (or in `extra_units` of `plan/outline.json`). That is for the foundation engineer.

13. **Pace.** SOA1.3 target 19 → 20 s and SOA1.6 target 28 → 30 s, to carry the added words.
    - Totals: 336 words, about 155 s estimated, 159 s target, 127 effective words per minute.
    - Per scene: 117, 132, 126, 129, 125 and 128 words per minute. SOA1.1 is lower because of its 3.4 s chapter card.
    - All scenes are within ±15 % of target. The unit is about 6 % above the plan's ≈ 150 s.

## Verified and kept

- **Lane 1.** Brunhes 1906: the Crossref title is "Recherches sur la direction d'aimantation des roches volcaniques", and Constable §1 gives the opposite direction, so "lavas magnetized backwards" stands. Vine and Matthews 1963 and Cox 1968 (p ≈ 0.05 per cycle, at least 100 times smaller in the Permian) check out against their abstracts.
- **Lane 2.** Larmor 1919, Cowling 1933 and Herzenberg/Backus 1958 ("first mathematical working examples") check out against Rincon §1.3-1.4. Roberts and Ponomarenko as the blueprints of Karlsruhe and Riga check out against R:139 and P3:909-911.
- **Lane 3.** Riga in November 1999 and Karlsruhe in December 1999 check out against R:139 and P3:1212-1213. VKS 2006 with soft-iron impellers only checks out against R:139 and P3:1214. DRESDYN is silent, with no 2026 status.
- **Lane 4.** Meneguzzi et al. 1981 checks out against its abstract and Rincon. Glatzmaier and Roberts 1995 is used by title only. The Nore et al. 1997 abstract has the two counter-rotating eddies. Nore et al. 2016 has ferromagnetic impellers, "for the first time". Kreuzahler et al. 2017 has penalized impellers with permeability jumps, VKS-like. Bousquet et al. 2026 (R:161, E:98): two solvers, Re = 1594, conducting surroundings.
- **Lane 5.** Rikitake 1958, Pétrélis and Fauve 2008 and Gissinger 2012 (deterministic) check out. DQVU is "derived from the MHD equations", with coefficients fitted by constrained PySINDy regression (S:233). It is never called "first".
- **Lane 6.** Gwirtz et al. 2022 checks out against its abstract.
- **Supervisors.** The narration never names them. Rings say only what each paper showed. The grey chip "INDEPENDENT SUMMARY · NOT REVIEWED BY THE PEOPLE NAMED" stays (E:43, T:57).
- **Planned work.** The thesis is "a proposed thesis" with the chip 'PLANNED · INDEPENDENT PROPOSAL', and the internship is a PLANNED pin. Nothing claims novelty.

## Open items (not changed here)

- **No question card.** The writer's task instruction excluded one, but BRIEF §3.1 says every chapter ends with a card. The plan's chSOA1.Q (wall and outer-medium properties; ask C. Nore / Y. Ponty) is with the consistency editor.
- **"First laboratory reversals" elsewhere.** The same broad wording is on the site (R:149), in `video/ETAT-DE-L-ART.md` (§1.2 row 2007, §D2 item 4), in `plan/state_of_the_art.md` §6 and in `script/_review/ch02.md` item 4. Berhanu et al. restrict it to a turbulent liquid-sodium dynamo, and Lowes and Wilkinson's models showed "a sort of reversals". The lead should narrow these.
- **Same anchor form in chSOA2.** `script/chSOA2.json` uses the same object-form `insert_after` and should get the same fix.
- **French wording to keep in step.** ch02 and ch03 have no `text_fr` yet. The French of 03.1.s1 should reuse "l'écoulement étire le champ, la diffusion l'estompe".
- **French lexicon.** The French lexicon needs Pm, VKS, MilaDy and Karlsruhe.

## Unverified (kept off screen)

- The title and pages of Larmor 1919.
- The wording of the Glatzmaier and Roberts 1995 abstract.
- DRESDYN's status in 2026. The last source, from April 2025, says "being set up".
- The full text of Botez et al. 2026: only its abstract was read.
