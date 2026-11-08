# fr/ch04 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch04.json` against the frozen `script/ch04.json`, "Chaos and the shoebox of photographs". The English script was not modified.

Validation: the JSON parses. All 56 sentence ids are present, in the English order, with no extras. `variants` is `{}` (no pending scene) and the voice block is the Ethan / drama-3 one, identical to the English. The markup tags match the English sentence by sentence (`{b}` ×7, `{u}` ×1, `{param}` ×4, `{metric}` ×2), every tag is closed, and the unit has no `{{field}}` placeholder. No digit is spoken. A no-break space (U+00A0) comes before every `?`, `:` and `;`.

`tools/assemble_cut.py --unit ch04 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences (623 words, 8 scenes, 1 question card). Nothing was written to `script/_build/`. The spoken text was read offline through `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`: only Gissinger is pinned, "Jissinjé"). Nothing was synthesized, and `audio/` and `scenes/` were not touched. No French ch04 take is in the cache, so these edits waste no paid audio.

## Changes

1. **04.7.s1: "Prenez une photo." became "Choisissez une photo."**
   - In French, "prendre une photo" means *to take a picture*. By ear, the line said "Take a picture", which is the opposite of the image: the photo is drawn from the shoebox, not shot.
   - "Choisissez" is *pick*, as in the English. The list of imperatives in the notes is updated.

2. **04.2.s4: "Chaque départ reste piégé." became "D'où qu'il parte, l'état reste piégé."**
   - What is trapped is the state, not its start. "Un départ piégé" is a calque of "each start is trapped" and sounds odd.
   - "D'où qu'il parte" (*wherever it starts from*) keeps the claim for every initial condition. It is not "où qu'il parte" (*wherever it goes*). "L'état" repeats 04.2.s2, so the subject is the dot on the map.
   - +1 word.

3. **04.4.s5: "Après environ cent cinquante, elles n'ont plus rien à voir." became "Au bout d'environ cent cinquante, elles n'ont plus rien en commun."**
   - "Au bout de" is the French idiom for elapsed time. With the unit left out, as in the English, "après environ cent cinquante" sounds clipped.
   - "N'avoir plus rien à voir" without "l'une avec l'autre" is colloquial and elliptical. "N'ont plus rien en commun" says *disagree completely* plainly.
   - The number is unchanged: "environ cent cinquante" is the horizon shown on screen, "six decimals used up · ≈ 150".

4. **04.5.s1: "La trajectoire est perdue" became "La trajectoire nous échappe".**
   - "Est perdue" can also be heard as *is doomed* or *is gone*. The English means that the path can no longer be followed, which is the lesson of 04.4.
   - "Nous" is the viewer and the narrator, as allowed (BRIEF §6). Same word count.

5. **04.7.s7: "sur des années" became "au fil des ans".**
   - "Over the years" in a bank account image is "au fil des ans". "Sur des années" is loose.
   - The contrast "mais chaque jour, le solde monte ou baisse" is unchanged. It matches the ledger card, where the running balance wanders and comes back.

6. **Translator notes updated.**
   - The notes said "later units: 'le halo'". No later French unit uses the glow image, and no later English unit says "glow". The note now says so.
   - The notes now record changes 1 to 5 and their reasons, the updated word counts, and the echoes that other overlays rely on.

## Checked and kept

- **Meaning, numbers and hedges match the English and the sources.**
  - The threshold is "Juste au-dessus de zéro virgule huit six" (E1: no crossing at Γ ≤ 0.86, crossings from 0.865).
  - The rates are "environ deux clics pour mille unités de temps" (1.94 per 1,000 at 0.865) and "À Gamma égal à un, environ onze" (11.2).
  - The chaos numbers are "triple presque toutes les onze unités" (×e per 1/0.089 ≈ 11), "environ cent cinquante", "plus de deux cents" (mean wait 226, ≈ 230 on screen) and "environ vingt-cinq" (ln 10 / 0.089 ≈ 26).
  - The hedges are kept: "peut" (an excursion *can*), "environ", "presque", "en moyenne", "pas pour chaque photo" and "Avec le temps". The CONTEXT scenes overclaim nothing.
  - 04.6.s8 keeps "avec les équations" at the head of the sentence (critique A4: the box alone is not enough).
  - 04.4.s8 keeps "avant la fin de l'attente moyenne". It is word for word in the 11.2.s4 callback.
  - 04.7 (PROVED) keeps the law for the crowd only: "sa moyenne est à zéro", "en moyenne", "Elle vaut pour la boîte à chaussures, pas pour chaque photo".
- **Terms against the French site and the symbol sheet.**
  - Prep P4 gives: loi stationnaire, couloir (ch. 4.4), passage par zéro, fréquence des passages (also the rapport and the PhD plan), excursion, renversement, "on ne peut donc pas prédire quand aura lieu le prochain renversement".
  - Rapport §E1 gives: instantanés, "sans ordre temporel".
  - From earlier overlays: "bilan d'énergie" and "Autant d'énergie entre qu'il en sort" (ch01.4, ch08.5, X3.5).
  - Glossary §5 of the symbol sheet: "image" for the frames of 04.6, "instantané" for the snapshot, "photo" only from 04.7 (it continues into 05.1-05.2). "Renversement" is never said as a rate: what is counted is "passages par zéro".
- **Echoes other overlays rely on (kept as is).**
  - "boîte à chaussures": 05.2, 05.5, 06.4, 07.5, X4.3, 11.2
  - "couloir", "juste au-dessus de zéro virgule huit six": 09.3
  - "tourbillon": 06.1, 07.1, 07.4
  - "fréquence des passages": 05.2, 09.x, X3.3, X4.2, 11.2
  - "loi de la foule": 07-11, X2-X5
  - "la première marche de l'escalier": X4.2, X4.5
  - "caricature à trois cadrans": 03.8.s2 → 04.1.s1
  - "fonds marins", "bandes": 00.3, 02.6
  - "jumeau en miroir": 01.5
- **Register.**
  - Vouvoiement in every imperative: Inversez, Faites, Augmentez, Comptez, Réglez, lancez, laissez, Filmez, Découpez, Mettez-les, secouez, jetez, Videz, Choisissez, lâchez.
  - "On" and "nous" are the viewer and the narrator.
  - There is no anglicism and no first-person anecdote.
- **Read-aloud checks.**
  - The predict beats end on a clean question before their holds: 04.2.s8 "réglés comme une horloge ?" (2.5 s) and 04.4.s2 "Peut-on prédire la date du prochain renversement ?" (3.0 s).
  - There are no tongue-twisters. "Lyapunov" is on screen only.
  - "Tous les clics ne sont pas des renversements" is the standard *not every*. "Toutes les deux unités de temps" is *every two time units*.
- **ch04.Q.s1** matches `question.fr` word for word, so the narration and the French question sheet agree.

## Length and timing (estimates, `audio/tts.py` word count, French rate about 146 words per minute)

| Scene | EN words | FR words | Change | Target | French speech, about |
|---|---|---|---|---|---|
| 04.1 | 65 | 69 | +6 % | 30 s | 28 s |
| 04.2 | 96 | 117 | +22 % | 45 s | 48 s + 2.5-s predict hold |
| 04.3 | 55 | 66 | +20 % | 25 s | 27 s |
| 04.4 | 87 | 98 | +13 % | 40 s | 40 s + 3.0-s predict hold |
| 04.5 | 66 | 68 | +3 % | 30 s | 28 s |
| 04.6 | 77 | 91 | +18 % | 35 s | 37 s |
| 04.7 | 87 | 100 | +15 % | 40 s | 41 s |
| ch04.Q | 16 | 14 | −12 % | 9 s | 6 s + 1.0-s hold |
| Total | 549 | 623 | +13.5 % | | about 4.7 min |

The review added 4 words in net (translator's draft: 619). Every scene stays inside the target ±15 % except 04.2 (+7 % over its target in speech alone). The French timeline absorbs that, because scenes animate on cue names.

## Remaining doubts (for the lead or the audio engineer; not changed)

- **Film-wide number reading: "zéro virgule huit six".** Spoken French says "zéro virgule quatre-vingt-six". The digit-by-digit reading is understood, and it matches "zéro virgule huit six cinq" (09.2.s6). It is already used in 07.3.s2, 09.2.s1 and 09.3.s2, and 09.3.s2 is a word-for-word callback of 04.2.s6. Changing it here alone would break that, so it should change in all four units or none.
- **TTS liaison risks, to check on the first take.**
  - "un halo se forme" (04.5.s2): the *h* of *halo* is aspirated, so there is no liaison.
  - "toutes les onze unités" (04.4.s4): no liaison before *onze*.
  - If the voice liaises in either place, use "le halo se forme peu à peu" or "Mais leur écart triple presque en onze unités de temps, et ainsi de suite", or add a respelling to `audio/lexicon_fr.json` (audio engineer's file).
- **"quadrupôle" against the site's "quadripôle".** P4, the rapport and the PhD plan write "quadripôle". P3 writes "quadrupôle", and so do the other overlays (X6, ch10). It is kept as is, because "quadripôle" is also the electrical two-port network and the spoken difference is one vowel. If the lead wants the site's majority spelling, change it in ch04, X6 and ch10 together.
- **"clic" for *tick*.** It is kept: the sound effect is a counter's click, and "un tic" would be heard as a nervous tic. "Un top" is the alternative if the lead prefers a time-signal sound.
- **Stale estimates.** `audio/scenes_fr/04.*.align.json` still hold the English text (estimated, no wav), and `script/_build/core_fr_cues.json` predates this review. The next French dry run refreshes both. This review did not touch them.
