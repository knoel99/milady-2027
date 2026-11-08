# fr/ch02 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch02.json` against the frozen `script/ch02.json`. The English script was not modified.

Validation: the JSON parses. All 39 sentence ids are present, in the English order, with no extras. `variants` is `{}` (no pending scene) and the voice block is the Ethan / drama-3 one. The markup tags (`{b}`, `{u}`, `{param}`) match the English sentence by sentence, with no `{{field}}` placeholder in the unit. A no-break space (U+00A0) comes before every `?` and `:`.

`tools/assemble_cut.py --unit ch02 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences. Nothing was written to `script/_build/`.

The spoken text was checked offline with `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`). Nothing was synthesized and `audio/` was not touched. The French `02.x.align.json` files are estimates with no wav, and no French ch02 take is in the cache, so these edits waste no paid audio.

## Changes

1. **02.1.s2, s4, s7, s8: the threads are now in the singular ("le fil"), never "les fils".**
   - The plural "fils" is a homograph. A French TTS voice can read it [fis] ("sons") instead of [fil] ("threads"). The ch03 and X1 notes already avoid it for this reason (03.1.s4 "comme un fil"; X1 "des filaments"). ch02, the unit that plants the image, still used it four times.
   - The new lines:
     - s2: "chaque ligne de champ serait un fil gelé dans le fluide"
     - s4: "le fil s'estompe, comme de l'encre qui s'étale"
     - s7: "le fil reste net"
     - s8: "le fil se fond dans le flou"
   - The singular also matches the picture. The scene draws one material line, and one per panel after the split (visual of 02.1).
   - The meaning is unchanged, and so is the hedge "dans un conducteur parfait … serait".

2. **02.1.s8: "Dans un mauvais, il est rapide" became "Dans un mauvais conducteur, il est rapide".**
   - After a preposition, the elliptical "dans un mauvais" sounds cut off in French.
   - It now mirrors s7 and echoes 03.1.s6 ("Dans un mauvais conducteur, le champ s'estompe vite").

3. **02.5.s4: "il n'y a eu aucune dynamo" became "il n'y a eu aucun effet dynamo".**
   - "Aucune dynamo" can be heard as "no generator".
   - "Effet dynamo" is the French physics idiom. chSOA1.3.s4 already says "l'effet dynamo n'apparaît qu'avec des disques en fer".

4. **02.5.s6: "ne dépend donc pas que de Rm" became "ne dépend donc pas seulement de Rm".**
   - "Pas que" is colloquial.
   - The claim keeps its English scope, R:90: the threshold depends on Rm *and* on the materials.

5. **02.6.s3: "mais toutes les une à deux minutes" became "mais à une ou deux minutes d'intervalle".**
   - "Toutes les une à deux minutes" is not spoken French.
   - The new phrase keeps the English value, "every minute or two". The mean polarity durations are 120 s and 50 s (R:149), and the on-screen label is "flips every minute or two".

6. **ch02.Q.s1: "Impossible de simuler le tout petit Pm du sodium : … dans les premières simulations en trois dimensions ?" became "Les simulations n'atteignent pas le très petit {param}Pm{/} du sodium : quelles valeurs de Pm couvrir dans les premiers calculs en trois dimensions ?".**
   - "Simuler le Pm" is a wrong collocation. A simulation runs *at* a Pm; it does not simulate one.
   - The first half now follows `question.fr` and the French question sheet (A6: "Les simulations n'atteignent pas le Pm … du sodium"). The narration and the companion sheet now say the same thing.
   - "Très petit" before the noun keeps the translator's good point that "le Pm minuscule" can be heard as "lowercase pm".
   - The infinitive question is kept: it is easier to follow by ear than the long inversion of `question.fr`.
   - "Runs" is now "calculs", the French site's word for runs ("quels calculs lancer ou louer"), so "simulations" is not said twice in one line.
   - "En trois dimensions" is kept; "3D" is never spoken.
   - The `{param}` tag stays on the first Pm, as in the English.

7. **Translator notes rewritten.**
   - The notes now record the singular "fil" and why, plus the choices "effet dynamo", "pas seulement", "à une ou deux minutes d'intervalle" and the new card wording.
   - The stale TTS remark is fixed. `audio/lexicon_fr.json` already pins Rm, Pm, VKS, DRESDYN, Reynolds and Prandtl, so it is no longer "French lexicon wanted".
   - The word counts are updated (see below).

## Checked and kept

- **Meaning, numbers and hedges match the English.**
  - "environ cent mille fois"
  - "un sur cent mille" gives the direction of Pm = ν/η, as the English review intended.
  - "quelques dizaines"
  - "cent cinquante litres"
  - "cinquante-deux cellules"
  - "Pour certains réglages": unequal speeds do not guarantee flips.
  - "environ cinq secondes"
  - "cherche à les rejoindre": DRESDYN has made no dynamo yet.
  - "seule l'expérience VKS": of the three, only VKS flips, and Riga's field "oscille", which is not a flip.
  - "comme celles des fonds marins": a likeness of look, not of statistics.
  - All badges are CONTEXT and no line overclaims.
- **Terms against the French site (prep P3, chapters 2 and 6).**
  - nombre de Reynolds magnétique, nombre de Prandtl magnétique, diffusivité magnétique
  - gel du flux → "gelé dans le fluide"
  - champ stationnaire de type dipolaire → "champ stationnaire, proche d'un dipôle"
  - turbines (contrarotatives), disques en acier inoxydable, fer doux
  - brasser, renversement / se renverser
  - "Toute dynamo de laboratoire est … turbulente", word for word from P3.
- **Planted pairs and echoes.**
  - étirement / estompage, used again in 03.1.s7, 03.4.s2 and chSOA1.6.s4.
  - champ germe / germe, as in ch01.
  - "sans aucun calendrier", from ch00.1.s4.
  - "fonds marins" and "bandes", from ch00.3.
  - "en tire-bouchon", reused in 03.3.s4.
  - "les turbines", reused in X2, X4a, X6, 10.8, 10.9, chSOA1 and chSOA2.
  - "comme le larsen" is the right French word for the 01.3 squeal, which is heard there but not named.
- **Register.**
  - Vouvoiement in the imperatives: Tournez, observez, Remplacez-les, Faites.
  - There is no anglicism and no first person.
- **Read-aloud checks.**
  - Rm and Pm come out as "erre ème" and "pé ème". The liaisons "grand erre ème", "petit erre ème" and "un erre ème" are natural.
  - VKS is read "vé ka esse" and DRESDYN "Dresdine". "DRESDYN, à Dresde" is fine.
  - There are no digits, abbreviations or tongue-twisters.

## Length and timing (estimates, `audio/tts.py` word count, French rate about 146 words per minute)

| Scene | EN words | FR words | Increase | Target | French speech, about |
|---|---|---|---|---|---|
| 02.1 | 75 | 87 | +16 % | 35 s | 36 s |
| 02.2 | 65 | 74 | +14 % | 30 s | 31 s |
| 02.3 | 66 | 79 | +20 % | 30 s | 33 s |
| 02.4 | 66 | 77 | +17 % | 30 s | 32 s |
| 02.5 | 71 | 80 | +13 % | 35 s | 35 s, plus 3.5 s of holds |
| 02.6 | 53 | 61 | +15 % | 25 s | 26 s |
| ch02.Q | 15 | 22 | +47 % | 9 s | 9 s, plus a 1.0 s hold and a 1.2 s tail |
| Total | 411 | 480 | +17 % | | about 3.7 min |

The review added 3 words: +1 each in 02.1, 02.5 and ch02.Q. Every scene stays inside the expected 15–20 % overrun (BRIEF §9), apart from the question card, whose card animations wait on the cue anyway.

## Remaining doubts (for the lead or the audio engineer; not changed)

- **TTS homograph in ch01, which is not this unit.** 01.6.s2 says "le disque avait des fils" (*wires*, [fil]), and the voice may read it [fis].
  - The ch01 reviewer can rephrase it, for example "le disque était relié à une bobine" or "avait un circuit".
  - Or the audio engineer can add `"fils": {"say": "fil"}` to `audio/lexicon_fr.json`. No French unit uses "fils" in the sense of *sons*.
- **Karlsruhe is not pinned in `audio/lexicon_fr.json`.** French speakers say "karlsrou-é". If the first take sounds German or spelled out, pin it as `{"say": "Karlsrouhé"}`.
- **Stale estimates.** `audio/scenes_fr/02.*.align.json` and `audio/requests/core_fr.jsonl` still hold the old text. They are estimates with no wav, and the next French dry run refreshes them. This review did not touch them.
