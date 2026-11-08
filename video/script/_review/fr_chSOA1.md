# fr/chSOA1 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/chSOA1.json`, checked against the frozen `script/chSOA1.json` ("A century of dynamo hunting"). The English script was not modified.

Validation:
- The JSON parses.
- All 31 sentence ids are present, in the English order, with no extra ids and no merged or split sentences.
- `variants` is `{}` (no pending scene). The unit has no `{{field}}` and no question card.
- The markup matches the English sentence by sentence: `{param}` on Pm (SOA1.4.s6) and on nombre de Reynolds (SOA1.4.s9), `{model}` on machines (SOA1.6.s3).
- A no-break space (U+00A0) comes before every `:` and `;`.
- `voice` matches the English script's `voice_fr`.
- `tools/assemble_cut.py --unit chSOA1 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences (444 words, 6 scenes). Nothing was written to `script/_build/`.
- The spoken text was rendered offline through `audio/tts.py` (`spoken_text` with `lexicon_fr.json`): VKS becomes "vé ka esse", Pm "pé ème", Reynolds "Rénolds", MilaDy "Milédi".
- Nothing was synthesized. `audio/`, `scenes/`, `runtime/` and the components were not touched.

## Changes

1. **SOA1.1.s1: "ont couronné une traque de près d'un siècle" became "ont couronné près d'un siècle de chasse à la dynamo".**
   - "Couronner une traque" is an odd collocation. One crowns years of effort ("couronner un siècle de recherches"), not a pursuit.
   - "Une traque", with no object, left the French listener guessing what was hunted. The English relies on the on-screen title "A century of dynamo hunting", which stays in English, so the French viewer may not read it.
   - "La chasse à la dynamo" is the idiom of French science writing ("la chasse au boson"). It also echoes the unit's takeaway ("have chased the dynamo together"). The sentence gains 2 words (about 0.8 s).

2. **SOA1.2.s4: "les premiers exemples démontrés d'écoulements qui en sont capables" became "les premiers exemples rigoureux d'écoulements capables d'entretenir un champ".**
   - One proves a theorem, not an example, so "exemple démontré" is not idiomatic. "Exemple rigoureux" is the mathematicians' phrase. It keeps the hedge "proven" and the source's wording (Rincon 2019: "the first mathematical working examples of fluid dynamos").
   - "Qui en sont capables" takes up the whole verb phrase of SOA1.2.s3, so the ear can hear "capable of sustaining a field symmetric around an axis", which is the opposite of Cowling's theorem. That risk is real at L1. The explicit "capables d'entretenir un champ" removes it.
   - Repeating "entretenir un champ" makes the parallel audible: 1919 might sustain, 1933 cannot sustain, 1958 can. Same word count.

3. **SOA1.5.s2: "deux dynamos à disque, couplées, se renversent déjà" became "avec deux dynamos à disque couplées, le champ se renverse déjà".**
   - With a machine as its subject, "se renverser" is first heard as *to tip over*. The two copper discs on screen invite exactly that picture.
   - In ch00-ch04 the subject of "se renverse" is the field or the dipole, with one exception (03.8.s2, see the doubts below). Rikitake 1958 reports "reversals of electric current and magnetic field", so the field is the right subject. +2 words.

4. **SOA1.5.s3: "trois cadrans qui se renversent sous le seul effet du chaos" became "trois cadrans, où le chaos suffit à renverser le champ".**
   - Same rule as change 3: the field flips, not the dials. "Le chaos suffit" keeps "by chaos alone": Gissinger 2012 is deterministic, with no noise.
   - After "le champ" (singular), the plural "eux" in "nous jouerons bientôt avec eux" can only mean the dials. Same word count.

5. **SOA1.4.s6: "fonctionnent encore pour un Pm d'un centième" became "à un Pm d'un centième".**
   - "À" is the preposition French physicists use for a parameter value: "des dynamos à Pm = 0,01", "à faible nombre de Prandtl magnétique" (encadrants page).

6. **SOA1.5.s4: "une méthode qui découvre les équations dans les données" became "… des équations …".**
   - The English says "finds equations in data", with an indefinite article.
   - The definite "les équations" claims the true governing equations. DQVU is a Galerkin model whose coefficients were fitted by sparse regression.

7. **SOA1.6.s2: "un renversement géomagnétique" became "un renversement du champ terrestre".**
   - The meaning is the same. "Du champ terrestre" is clearer for the ear at L2 and keeps "le champ", the film's word since ch00.
   - The scope of Gwirtz et al. 2022 is unchanged: "les méthodes d'apprentissage essayées par une étude n'ont pas su prévoir de façon fiable". +2 words.

8. **Translator notes corrected and completed.**
   - Fixed a factual slip: the notes listed Karlsruhe among the French lexicon pins, but `audio/lexicon_fr.json` has no Karlsruhe entry (ch02's notes say the same). The respellings are now quoted as the lexicon writes them ("vé ka esse", "pé ème", "Rénolds", "Milédi").
   - Recorded the rule "a flip has the field as its subject, never the device".
   - Added the reasons for changes 1-7.
   - Replaced the length paragraph (see below). The first estimate of "+15 % syllables" was too low.

## Checked and kept

- **Meaning, numbers, hedges, badges** (all CONTEXT, plus PLANNED from SOA1.6 `bet`):
  - "Pourrait entretenir" for Larmor's 1919 idea.
  - "Aucun écoulement ne peut entretenir un champ symétrique autour d'un axe" is Cowling as stated in P3 Theorem 5.3. "Symétrique autour d'un axe" is kept rather than "à symétrie axiale", which French school maths uses for a reflection across a line. It is also kept rather than "axisymétrique", which is heavy at L1.
   - "First" is used only for the 1958 examples and for "les premiers renversements d'une dynamo turbulente au sodium". It is never used for Lowes and Wilkinson, and it is never "premiers en laboratoire" (the English review's wording traps).
   - "Dans VKS, l'effet dynamo n'apparaît qu'avec des disques en fer" (R:139). "Deux codes … turbines en fer comprises" (2016 SFEMaNS, 2017 LATU).
   - "Dans les cas explorés, seulement avec un milieu conducteur tout autour" is the paper's "necessary … in the explored range", and P3:1347 has "un milieu conducteur autour du cylindre dans la gamme explorée".
   - "Un nombre de Reynolds d'environ mille six cents, et non des millions" (Re = 1594, R:161). "Un Pm d'un centième" (Ponty et al. 2005).
   - "Un projet de thèse" and "un pari" keep the PLANNED proposal status. The rings are described only by what they mark ("les articles cosignés par les encadrants du projet"). No name is narrated (D6).
- **Terms against the French site and the earlier overlays.**
  - These terms all appear in R:139-161, P3 chapters 5-7 and the encadrants page: "renversement / se renverser", "effet dynamo", "entretenir", "simulation de référence", "turbines en fer", "contrarotatifs", "milieu conducteur", "apprentissage automatique" (the project's French title), "encadrants".
  - These come from the earlier overlays: "la carte" (never the staircase), "piste", "cuve", "cadrans" (ch03, ch04, chSOA2), "repères cerclés" (chSOA2), "les fonds marins" and "bandes" (ch00, ch02), "fabrique son propre champ" (02.4), "l'étirement contre l'estompage" (02.1-02.2, 03.1.s7).
  - Not using the verbs here avoids repeating 03.1.s1 one sentence later, so I kept the translator's departure from the English review.
  - `video/ETAT-DE-L-ART.md` says "inversions". That is the companion document; the narration follows the ch00 decision.
- **Symbol sheet.** Pm and Reynolds number are green (control parameters), machines are violet. "Flip rate" is never used. "Nous" means the viewer and the narrator (SOA1.5.s3).
- **Register.** The unit addresses no one directly, so there is no imperative. There are no anglicisms (VKS and MilaDy are names).
- **Read-aloud.**
  - Years are written as words, as read in France ("mille neuf cent six" … "deux mille vingt-six", "les années soixante-dix").
  - There are no parentheses and no unpinned abbreviations. "Pourtant", not "Or". There is no "fils" homograph.
  - The ":" and ";" pauses fall where the English has its breaks. "Contrarotatifs" and "quatre-vingt-dix-sept" read cleanly.
  - "Une maquette de dynamo" is kept: French labs call a working reduced setup a "maquette" (as in the "maquette en eau" of an experiment), and the word matches the solid-iron, non-fluid nature of Lowes and Wilkinson's device.

## Length and timing (estimates)

Both voices run at about 3.8 syllables per second, measured with the same vowel-group counter on 3,900 s of English takes and on the French test takes. The French narration is estimated as the real English take of each scene, scaled by the French-to-English syllable ratio (722 / 569 syllables, +27 %).

| Scene | EN words | FR words | Target | EN take | FR estimate |
|---|---|---|---|---|---|
| SOA1.1 | 41 | 59 | 21 s | 22.0 s | ≈ 25.5 s |
| SOA1.2 | 53 | 65 | 24 s | 26.0 s | ≈ 34 s |
| SOA1.3 | 42 | 57 | 20 s | 23.5 s | ≈ 27 s |
| SOA1.4 | 86 | 117 | 40 s | 48.6 s | ≈ 58 s |
| SOA1.5 | 50 | 63 | 24 s | 23.8 s | ≈ 28 s |
| SOA1.6 | 64 | 83 | 30 s | 30.8 s | ≈ 39 s |
| Total | 336 | 444 | 159 s | 174.6 s | ≈ 212 s (+21 %) |

- The translator's draft had 438 words. The review adds 6 words (changes 1, 3 and 7), about 2 s in all.
- The assembler's word-based estimate (146 words per minute, about 3.3 min) overstates the French: a 19xx year is four French words for two English ones.
- The French timeline absorbs the difference, because cues are names.

## Remaining doubts (for the lead, not changed)

- **Karlsruhe has no French pin** (SOA1.1.s1, SOA1.2.s5, SOA1.3.s3, and ch02). Listen to the first French take; if it sounds German or English, the audio engineer can add a respelling such as "Karlsrouhé".
- **Fixed-second offsets after cues.** Several offsets come early against the French words, because the French sentences are longer and put the illustrated word later: `sodium+1.4` (Karlsruhe card), `vks+1.6` (flip glyph), `discs+1.4` (arrow turns), `geodynamo+1.2`, `flipsim+1.0`, `four+1.2`. For example, "Karlsruhe" comes about 6 s into SOA1.3.s3 in French, against about 4 s in English. The visual simply anticipates the word, so nothing breaks. If the French render shows it, the scene builder could scale these offsets by the sentence length.
- **SOA1.4.s5 to s6.** "En simulation, deux tourbillons contrarotatifs produisent un effet dynamo" is followed by "ces dynamos", whose antecedent is only implied (English: "make a dynamo … such dynamos"). It is kept because "produisent une dynamo" is not idiomatic. "Forment une dynamo" is the alternative if a strict antecedent is wanted.
- **03.8.s2** ("une caricature à trois cadrans, qui se renverse déjà", outside this unit) uses the model as the subject of "se renverse". It reads acceptably, since a caricature cannot tip over, but the ch03 reviewer may align it with the rule recorded here.
