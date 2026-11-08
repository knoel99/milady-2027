# fr/ch00 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch00.json` against the frozen `script/ch00.json`. The English script was not modified.

Validation: the JSON parses. All 23 sentence ids are present, in the English order, with no extra ids, and `variants` is `{}` (no pending scene). `tools/assemble_cut.py --unit ch00 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences; nothing was written to `script/_build/`. The spoken text was checked offline with `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`). Nothing was synthesized, and `audio/` was not touched: the French `00.x.align.json` files are estimates with no wav.

## Changes

1. **00.3.s1: "la lave fraîche refroidit" became "la lave qui remonte refroidit".**
   - In French, "fraîche" first means *cool*, so "la lave fraîche refroidit" sounds like "the cool lava cools".
   - "Qui remonte" keeps the idea of new rock (the on-screen label "new rock") and is physically right: magma rises at the ridge.

2. **00.4.s5: "la première est sans espoir" became "la première est hors de portée".**
   - "Sans espoir" said of a question is a calque of *hopeless*.
   - "Hors de portée" is the French scientific idiom and keeps the strength of the claim (prep P4: "on ne peut donc pas prédire quand aura lieu le prochain renversement").
   - "La seconde, non." still answers it. The scope hedge "dans un modèle numérique simple" is unchanged, and matches 11.2.s4.

3. **00.2.s1: "suit un {b}champ{/}" became "suit un {b}champ magnétique{/}".**
   - This is the first mention of the field. In French, "un champ" with no qualifier first means a farm field, and at L0 it does not explain itself the way "field" does next to "compass".
   - Every later mention says "le champ", the site's own shorthand ("le champ se renverse").
   - Cost: about 0.4 s. 00.2 is estimated at about 7.8 s for a 7 s target, which is within 15 %.

4. **00.3.s3: "ouvre une nouvelle bande" became "commence une nouvelle bande".**
   - "Ouvrir une bande" is not idiomatic. "Commencer" is the plain verb for *starts a new stripe*.

5. **Translator notes rewritten.**
   - The old notes said "never 'inversion'" while 00.1.s3 uses "se sont inversés". The notes now separate the two: *flip* is always "renversement" or "se renverser", as on the French site, and "s'inverser" in 00.1.s3 translates *swapped* (the two poles trade places).
   - The stale TTS remark is fixed: `MilaDy` is already pinned as "Milédi" in `audio/lexicon_fr.json`, and is still on that file's check list.
   - The notes now list the echoes that other units rely on, so a later edit does not break them: "sans aucun calendrier" (02.6.s2), "fonds marins" and "bandes" (02.6, 04.2, chSOA1), "modèle numérique simple" (11.2.s4), "imaginent" (ch11, chSOA1).
   - The length and flip-timing figures are corrected (next section).

## Checked and kept

- **Meaning and hedges.**
  - 00.1.s2 "ont la mémoire plus longue" keeps the swap in the past, as the English review intended.
  - 00.4.s5 is scoped to the simple model, never to Earth (badge MEASURED, note "three-mode model").
  - In 00.4.s9 "doivent obéir exactement… seulement en moyenne", the laws are imposed, not learned (English review item 2).
  - ch00.Q.s1 matches `question.fr` word for word, including "juste avant", so the narration and the French question sheet agree.
- **Numbers.** "Cinq millions d'années" and "une vingtaine de renversements" match the English. No digits are narrated.
- **Terms against the French site.**
  - "renversement" and "fréquence des renversements" (rapport, these, prep P3 and P4).
  - "quand aura lieu le prochain renversement" and "à quelle fréquence" (P4, word for word).
  - "instantanés" and "machines" as in ch04 to ch11.
  - "dorsales océaniques" is the standard geoscience term.
- **Register.** Vouvoiement throughout. "Nous" and "on" mean the viewer and the narrator. There are no anglicisms, and ch00 has no English ML term.
- **Read-aloud checks.**
  - "de la boussole jusqu'à la recherche d'aujourd'hui" is kept on purpose: with plain "à", the line could be heard as "à la recherche de…" (*in search of*).
  - "La seconde, non." is clear after "la première".
  - The "-t-il" inversions read cleanly, and no clusters are hard to say.
- **Markup.**
  - `{b}` sits on champ magnétique, champ (00.3.s2, 00.4.s5, 00.5.s1) and champs magnétiques.
  - `{metric}` sits on "à quelle fréquence" and "la fréquence", and `{model}` on "machines".
  - "Le champ" in 00.4.s3 and ch00.Q stays unmarked, as "it" and "the field" are in the English.
  - There are no `{{field}}` placeholders in ch00. A no-break space (U+00A0) comes before every "?", as in every other French overlay.

## Length and timing (estimates, French rate about 146 words per minute)

| Scene | EN words | FR words | Target | Note |
|---|---|---|---|---|
| 00.1 | 25 | 30 | 11 s | flip cue at about 7.3 s from the scene start, against 6.3 s in the English: about 0.9 s later, absorbed by the French timeline (BRIEF D20 says "≈ 7 s") |
| 00.2 | 16 | 19 | 7 s | about 7.8 s |
| 00.3 | 36 | 46 | 16 s | about 18.8 s, the longest relative overrun (+18 %), inside the expected 15-20 % |
| 00.4 | 67 | 79 | 30 s | about 34 s |
| 00.5 | 19 | 22 | 10 s | about 8.6 s |
| ch00.Q | 18 | 20 | 10 s | |
| Total | 181 | 216 | | +19 % |

## Remaining doubts (for the lead, not changed)

- **ch11 11.2.s2**, which is not this unit, renders the callback "When will this needle turn?" as "se retourner". ch00 uses "renversement". The English also changes the verb (*flip* → *turn*), so this is acceptable, but the ch11 reviewer may want "Quand cette aiguille va-t-elle se renverser ?" so the callback is word for word.
- **"Signes annonciateurs"** in ch00.Q comes from the frozen `question.fr`. "Signes avant-coureurs" would be slightly more idiomatic, but changing it would break agreement with the French question sheet, so it was left as is.
