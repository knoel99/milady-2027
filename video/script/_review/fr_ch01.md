# fr/ch01 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch01.json` against the frozen `script/ch01.json`, "A planet that makes its own magnet". The English script was not modified.

Validation: the JSON parses. All 39 sentence ids are present, in the English order, with no extra ids, and `variants` is `{}` (ch01 has no pending scene). The markup tags match the English sentence by sentence (`{b}` ×5, `{param}` ×1, `{u}` ×1), and there are no `{{field}}` placeholders. A no-break space (U+00A0) comes before every `?`, `:` and `;`. `tools/assemble_cut.py --unit ch01 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences (441 words, 7 scenes, 1 question card), and nothing was written to `script/_build/`. The spoken text was read offline through `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`; ch01 needs no French pin). Nothing was synthesized, and `audio/` and `scenes/` were not touched.

## Changes

1. **01.1.s2: "Tout au fond, le noyau externe…" became "Loin sous la surface, le noyau externe…".**
   - "Tout au fond" means *at the very bottom*. The outer core is not the bottom: the solid inner core lies deeper, and the cutaway on screen shows it ("solid inner core").
   - "Loin sous la surface" says *deep down* with no false claim. "Sous nos pieds" was avoided because the narrator never presents itself as a person.

2. **01.2.s1: "le nord à un bout, le sud à l'autre" became "un pôle nord à un bout, un pôle sud à l'autre".**
   - "Le nord" on its own, said of a magnet, is loose at L0. "Pôle" also prepares "pôle magnétique isolé" two sentences later.

3. **01.2.s3: "qui ont chacun un nord et un sud" became "chacun avec son nord et son sud".**
   - Lighter to say, one word shorter. With "pôle" already planted in s1, it does not repeat.

4. **01.3.s6: "relié à une bobine enroulée autour de son axe" became "relié par un fil à une bobine autour de l'axe".**
   - In the English, "wired to a coil" plants the wire that 01.6.s2 calls back: "But the disc had wires; liquid iron has none". The old French had no wire, so "Mais le disque avait des fils" came out of nowhere.
   - "L'axe" replaces "son axe", because "son" could now be read as the wire's. "Enroulée" was dropped because a "bobine" is already wound.

5. **01.5.s2: "Inversez chaque ligne de champ" became "Inversez le sens de chaque ligne de champ".**
   - B → −B keeps the shape of every line and reverses its orientation. That is exactly the visual: the arrowheads swing round along unchanged lines.
   - "Inverser une ligne" alone can be heard as flipping the curve over, like a mirror image. That is the wrong picture just before the "jumeaux en miroir" metaphor, which the visual notes say is only a metaphor.
   - It also continues the scene's thread on "sens": "pointe dans un sens" → "le sens de chaque ligne" → "le sens qu'on obtient" → 01.6 "aucun sens privilégié".

6. **01.5.s3: "tout aussi permis par les lois" became "autorisés au même titre par les lois".**
   - "Tout aussi permis", with no term of comparison and the weak adjective "permis", is clumsy. "Au même titre" says *equally* plainly.
   - "Également" was avoided because the ear can take it as *also*.
   - The new phrase still ends on "les lois", which 01.5.s4 ("pas des lois") and 01.5.s5 ("rien dans les lois") pick up.

7. **Translator notes rewritten.**
   - Removed the imperative "Changez", which appears nowhere in the text.
   - Corrected the length figures.
   - Added the reasons for changes 1, 2, 4 and 5.
   - Listed the echoes that other overlays rely on: "il entre autant de lignes qu'il en sort" (08.3.s3), "la boîte" (08.2-08.3), "champ germe / germe" (ch02.2), "le larsen" (ch02.2.s7), "jumeau en miroir" (ch04.2), "renversement" for the flip (ch00).
   - Added the P1 and P3 wordings the terms come from.

## Checked and kept

- **Meaning, hedges, badges.**
  - 01.1.s3 "en quelques dizaines de milliers d'années" keeps the English review's hedge. It matches τ ≈ 4 × 10⁴ years on the formula layer and the counter's 40,000, and stays compatible with Tobias' "of order 10⁴ years". "Livré à lui-même" matches the "left alone" counter.
  - 01.4.s4 keeps both qualifiers: "Une fois la croissance arrêtée" and "en moyenne". This is the steady-regime key point under P3 Theorem 3.3 (PROVED), which holds for the law, not for each snapshot.
  - 01.5.s2 "les équations de la dynamo restent les mêmes" is the P3:239 invariance (PROVED).
  - 01.5.s4 keeps the scope "dans le disque".
  - 01.5.s5 "rien dans les lois n'interdit" is a permission, not a prediction, as in the English.
  - No number is spoken in ch01. "Plusieurs milliards" and "quelques dizaines de milliers" match the English.
- **Terms against the French site.**
  - "champ germe" is P3's term (§5 and exercise 2). "seuil" and "taux de croissance" are P3's.
  - "l'écoulement étire le champ ; le champ freine l'écoulement" is P3 chapter 5 word for word.
  - "lignes de champ… n'ont ni début ni fin" follows P1 ("une ligne de champ ne peut ni commencer ni finir"). There is no "se referment" (critique B4).
  - "pôle magnétique isolé" is kept at L0, rather than P1's "monopôle".
  - "renversement" is the flip (ch00 decision). "Noyau externe", "barreau aimanté" and "dynamo de vélo" are standard French.
  - "Germe" (the field's seed) and "graine" (the training seed) never collide.
- **Register.**
  - Vouvoiement throughout: Prenez, Coupez-le, Tracez, comptez, Gardez, Approchez, montez, Faites, Inversez. "On" is the impersonal *you* (01.5.s4).
  - No anglicisms. "Gain" is the French sound-engineering word and the on-screen knob label.
- **Read-aloud checks.**
  - "Pourtant" (not "Or", which can be heard as *gold*).
  - 01.3.s4 keeps "un certain point" so that "seuil" arrives only with the answer to the predict beat (01.3.s9, "Pas du tout, jusqu'à un seuil", which echoes "ou pas du tout").
  - "du haut-parleur qui le diffuse" avoids the calque "son propre haut-parleur".
  - The "-t-il" and "-il" inversions read cleanly. There are no clusters that are hard to say.
  - "Watt" and "micro" read natively.
- **ch01.Q.s1** matches `question.fr` word for word, so the narration and the French question sheet agree.

## Length and timing (estimates, French rate about 145 words per minute, BRIEF §9)

| Scene | EN words | FR words | Target | FR speech + holds | Note |
|---|---|---|---|---|---|
| 01.1 | 53 | 58 | 25 s | ≈ 24 s | |
| 01.2 | 64 | 71 | 30 s | ≈ 29 s | |
| 01.3 | 122 | 138 | 55 s | ≈ 62 s (incl. 5 s holds) | +13 % |
| 01.4 | 48 | 50 | 20 s | ≈ 21 s | |
| 01.5 | 54 | 72 | 25 s | ≈ 32 s (incl. 2.5 s hold) | largest overrun; changes 5 and 6 add 4 words (≈ 1.7 s), kept for accuracy; the needle flip is on a cue (`forbid+0.5`), so the French timeline absorbs it |
| 01.6 | 28 | 34 | 13 s | ≈ 14 s | |
| ch01.Q | 16 | 18 | 9 s | ≈ 8.4 s (incl. 1 s hold) | |
| Total | 385 | 441 | | | +14.5 % (translator's draft: 434, +12.7 %) |

## Remaining doubts (for the lead, not changed)

- **01.5.s1 "pointe aujourd'hui dans un sens."** "Dans un sens" is also the idiom *in a way*. The verb "pointe" forces the literal reading, so it was kept. If a take sounds ambiguous, "dans un sens bien précis" would remove the doubt for two words.
- **ch01.Q "d'un germe fort, ou des deux"** comes from the frozen `question.fr`. "Partir… des deux" is slightly elliptical ("ou essayer les deux" would be smoother), but the French question sheet has to stay in agreement, so it was left as is.
