# fr/ch05 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch05.json` against the frozen `script/ch05.json`, "Counting crossings from still photographs". The English script was not modified.

Validation: the JSON parses. All 31 sentence ids are present, in the English order, with no extras. `variants` is `{}` (no pending scene) and the voice block is the Ethan / drama-3 one. The markup tags (`{b}` ×1, `{param}` ×2, `{metric}` ×2) match the English sentence by sentence and every tag is closed. The unit has no `{{field}}` placeholder, no digit and no parenthesis. A no-break space (U+00A0) comes before every `:`, `;` and `?`.

`tools/assemble_cut.py --unit ch05 --lang fr --strict --out <scratchpad>` reports 0 untranslated sentences and no lint warning on the text (419 words, 6 scenes, 1 question card). Its two warnings are about the data file `data/ch05_rice.json`, which is still missing for 05.2 and 05.3 and is not a narration matter. Nothing was written to `script/_build/`.

The spoken text was checked offline with `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`): Rice is said "Raïsse" and VKS "vé ka esse". Nothing was synthesized. No French ch05 take is in `audio/cache/` (the `audio/scenes_fr/05.*.align.json` files are estimates on the English text), so these edits waste no paid audio. `audio/` and `scenes/` were not touched.

## Changes

1. **05.3.s6: "Quatre pour cent près du seuil, six pour cent au-dessus" became "Près du seuil, quatre pour cent ; au-dessus, six pour cent".**
   - Heard aloud, "quatre pour cent près du seuil" contains "pour cent près". Elsewhere the film uses that idiom for *within*: "à dix pour cent près" (X6), "à cinq pour cent près" (ch10).
   - Here the number is a cumulative error, not a tolerance. Critique C8 forbids "within 4 %", and R:883 gives "erreur cumulée de 4 %".
   - The new order removes the collision and matches 09.1.s6, "Près du seuil, l'erreur grimpe à quarante-deux pour cent".
   - The on-screen brackets both appear on the same cue, so the order inside the sentence does not matter.

2. **05.1.s5: "Une voiture rapide y passe peu de temps : en surprendre une à l'intérieur compte donc davantage" became "Une voiture rapide reste peu de temps dans la bande : en surprendre une compte donc davantage".**
   - "Y" came right after "autour de la ligne" (05.1.s4), so it could point to the line rather than to the strip. The idea is time spent in the strip, so the strip is now named.
   - "En surprendre une" no longer needs "à l'intérieur".
   - Same length.

3. **05.2.s4: "l'équation du dipôle tire une vitesse des trois cadrans de la photo" became "l'équation du dipôle calcule une vitesse à partir des trois cadrans de la photo".**
   - By ear, "une vitesse des trois cadrans" can be parsed as *a speed belonging to the three dials*.
   - "Calcule … à partir de" says what the English "turns … into a speed" says: Ḋ = −0.1 D + V Q, computed on the snapshot (R:701-709).
   - +2 words.

4. **05.2.s5: "gardez la valeur sans le signe" became "oubliez le signe".**
   - "La valeur" was left hanging: the value of what? "Oubliez le signe" is how a French maths teacher says *take the absolute value*.
   - It fits the visual: the plane folds, and the up and down arrows merge into one.
   - −3 words.

5. **05.2.s1: "Étalez ses photos selon leur dipôle" became "Étalez ses photos selon la valeur de leur dipôle".**
   - The English is "by their dipole reading". "Selon leur dipôle" lost the reading, so it was unclear what the photos are sorted on.
   - ch04 already uses "les valeurs de ses trois cadrans" (04.6.s6, 04.7.s1). The `{b}` tag stays on "dipôle".
   - +3 words.

6. **05.1.s2: "Juste une photo prise d'en haut" became "Rien qu'une photo prise d'en haut".**
   - "Juste" in the sense of *seulement* is a calque of English "just". The Académie lists it in *Dire, ne pas dire*.
   - "Rien qu'une" is the idiomatic spoken form, with the same length.
   - Correct uses of "juste au-dessus" elsewhere (ch04) are unaffected.

7. **05.3.s5: "Coloriez l'écart" became "Colorez l'écart".**
   - "Colorier" is the children's colouring-in verb. "Colorer" is the neutral one. Same length.

8. **Translator notes updated.**
   - The notes now record changes 1-7 and their reasons.
   - The stale TTS line is fixed: `lexicon_fr.json` already pins Rice and VKS, so "French lexicon wanted" is gone.
   - The length figures are updated, and the notes point to this file.

## Checked and kept

- **Meaning, numbers and hedges match the English.**
  - The numbers are "environ deux douzaines sur huit mille" (26 of 8,000, from the data note), "quarante et un réglages" (the fine grid), and "quatre / six pour cent" (R:883).
  - The hedges are kept:
    - "En moyenne" (05.1.s7)
    - "pour les systèmes qui se comportent bien" (exact only under Rice's assumptions, R:517, R:522)
    - "rien ne garantit que … se comportent bien" (the density assumption is not guaranteed for deterministic chaos, R:528, R:901)
    - "presque" (05.3.s4)
  - "La recette est exacte" is limited to the h → 0 limit ("Rendez la bande infiniment fine"), as in the English.
  - "Divisez … par le nombre total de photos" (all 8,000, not only those in the strip) matches the estimator of R:701-709.
  - "Le projet de thèse compte les passages par un niveau éloigné, de l'autre côté de zéro" matches T:680 and Prop. 2.30, a reversal going from D ≥ a to D ≤ −a. The badge stays PROVED (Prop. 2.30), and the PLANNED framing of "le projet de thèse" stays.
- **Terms against the French site.**
  - From the rapport (Prop. 8, §m-rice, R:883): "fréquence des passages (de D) par zéro", "passages", "comptage", "erreur cumulée", "excursions", "renversements".
  - From the PhD plan (T:684, T:938): "seuil" for the level a on the question card, and "niveau" in 05.4.s3.
  - From prep P5, Remarque 6.12: "franchissement" belongs to the remark; the film keeps "passage", as ch04, ch09, ch11 and X4a do.
  - Inside the scenes, "niveau" (level a) and "seuil" (the Γ threshold) never share a sentence. The exception is ch05.Q, where "quel seuil fait d'un passage par zéro un renversement" makes the sense clear.
- **Planted pairs and echoes.**
  - "La ligne" and "les voitures" in 05.1 are called back by 09.1.s1, "Revoici la route et sa ligne".
  - "Fréquence" is planted in the predict beat (05.1.s3) and paid off by "la fréquence des passages par zéro" (05.2.s7, the same words as 11.2.s10 and 04.6.s9).
  - "Boîte à chaussures", "instantanés", "photos" (05.1-05.2 only) and "trois cadrans" follow ch04.
  - "Entre les points" echoes 03.6.s5. "Réglages" carries `{param}`, as in ch03.
  - "Bande" for the strip matches X3a and X4a ("la bande de Rice").
- **Question card.**
  - ch05.Q.s1 is word for word `question.fr` of the English script and Q7 of `question_register.json`, so the French question sheet and the narration agree. "Suivre" was kept for that reason, although "à quel dipôle appliquer la formule de Rice" would be a little more idiomatic. If the lead prefers it, change the register and the overlay together.
- **Register.**
  - Vouvoiement in every imperative: Tracez, Additionnez, Étalez, Rendez, Confrontez, Colorez, oubliez. "Vous" in the predict beat, "on" for "Out comes".
  - There is no anglicism and no first-person anecdote. "Le hic" is familiar but already used in the film (ch06 "Un hic, toutefois", X4a "Seul hic"), so it was kept for consistency.
- **Read-aloud checks.**
  - The liaisons are natural ("nombreux et bon marché", "quarante et un").
  - There are no digits, abbreviations or tongue-twisters. Gamma is read natively.
  - "Oui." lands right after the 2.5-s predict hold.

## Length and timing (estimates, French rate about 146 words per minute)

| Scene | EN words | FR words | Change | Target | French speech, about |
|---|---|---|---|---|---|
| 05.1 | 82 | 91 | +11 % | 40 s | 37 s + 2.5-s hold + breaks |
| 05.2 | 110 | 126 | +15 % | 50 s | 52 s + breaks |
| 05.3 | 73 | 87 | +19 % | 35 s | 36 s + break |
| 05.4 | 35 | 44 | +26 % | 15 s | 18 s |
| 05.5 | 45 | 51 | +13 % | 20 s | 21 s |
| ch05.Q | 16 | 20 | +25 % | 9 s | 8 s + 1.0-s hold |
| Total | 361 | 419 | +16 % | | about 3.2 min |

Words are counted without markup or punctuation tokens. The review added 2 words in net. 05.4 and ch05.Q go past the 15-20 % expected (BRIEF §9). This is structural: "Rice" becomes "la formule de Rice", and the question card follows `question.fr`. The French timeline absorbs the 1-3 s.

## Remaining doubts (for the lead; not changed here)

- **05.2.s8, "pour les systèmes qui se comportent bien".** This is a light calque of "well-behaved". It was kept because 05.3.s7 calls it back ("se comportent bien"). The alternative "suffisamment réguliers" would clash with "chaotiques" (heard as *periodic*).
- **05.5.s2, "les simulations de vraies dynamos".** It reads well and avoids implying that the 41 runs of 05.3 were not real. "Les simulations de dynamos en trois dimensions" would echo 03.6.s1 more strictly but is longer.
