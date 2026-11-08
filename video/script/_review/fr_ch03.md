# fr/ch03 review changelog (native-quality French review, 2026-11-08)

Unit: `script/fr/ch03.json` against the frozen `script/ch03.json`, "The equation, the windows, and the question". The English script was not modified.

Validation: the JSON parses. All 49 sentence ids are present, in the English order, with no extras (48 in 03.1-03.8, 1 in ch03.Q). `variants` is `{}` (no pending scene) and the voice block is the Ethan / drama-3 one. The markup tags (`{u}` ×3, `{b}` ×3, `{param}` ×3, `{model}` ×1, `{metric}` ×2) match the English sentence by sentence, every tag is closed, and the unit has no `{{field}}` placeholder. No digit is spoken. A no-break space (U+00A0) comes before every `:`, `;` and `?`.

`tools/assemble_cut.py --unit ch03 --lang fr --strict --out <scratch>` reports 0 warnings and 0 untranslated sentences (632 words, 9 scenes, 1 question card). Nothing was written to `script/_build/`.

The spoken text was checked offline with `audio/tts.py` (`spoken_text` plus `lexicon_fr.json`). Nothing was synthesized. `audio/` and `scenes/` were not touched. No French ch03 take is in the cache: `audio/scenes_fr/03.*.align.json` are estimates with no wav, so these edits waste no paid audio.

## Changes

1. **03.2.s4: "comme il freinait le disque de cuivre" became "comme il a freiné le disque de cuivre".**
   - "Comme" + imparfait is the French temporal construction: "comme il freinait" is first heard as *while it was braking*. That reads as if the field were braking the disc at the same moment.
   - The English "as it braked the copper disc" is a callback to a past scene (01.3.s12, "Puis le champ freine le disque"). The passé composé says so.
   - Same word count.

2. **03.2.s6: "C'est sur le plateau que vivent les renversements" became "C'est sur le plateau que se produisent les renversements".**
   - "Vivre" said of events is a calque of "Flips live on the plateau". In French, events "se produisent" or "ont lieu".
   - The meaning is unchanged: reversals belong to the saturated, nonlinear regime (R:149, R:159). The cleft and the on-screen label "flips live here" stay.

3. **03.4.s5: "Puis la croissance devient positive" became "Puis le taux devient positif".**
   - What turns positive is the growth rate *s*, the quantity plotted ("Voici le taux de croissance", one sentence earlier). A French physicist says "le taux de croissance devient positif". "La croissance devient positive" is loose.
   - "Le taux" alone avoids saying "taux de croissance" twice in a row. "Il devient positif" was rejected because "tout champ s'éteint" comes in between, so "il" could be heard as the field.
   - +1 word.

4. **03.7.s2: "L'étude sur laquelle s'appuie ce film pose trois questions" became "L'étude sur laquelle il s'appuie pose trois questions".**
   - 03.7.s1 ends on "ce film". Saying "ce film" again in the next sentence was heavy. "Il" can only be the film: "ces vides" is plural.
   - −1 word. The translator's choice to avoid the calque "derrière" is kept.

5. **03.7.s4: "là où elle s'applique" became "là où elle est vraie".**
   - "Là où elle est vraie" is the French site's own phrase for this idea. The report states its thesis as "une contrainte doit être imposée là où elle est vraie" (rapport :577, :1199).
   - It is also the film's French refrain. 08.6.s5 says "imposez chaque loi là où elle est vraie" and 11.2.s14 says "Imposez chaque loi là où elle est vraie". 03.7.s4 plants it; those lines pay it off.
   - "Peut-elle respecter chaque loi là où elle s'applique" let "elle" be heard as the machine ("where it is applied"). With "est vraie", "elle" can only be the law.
   - +1 word.

6. **ch03.Q.s1: "Avec une poignée de simulations" became "Avec seulement une poignée de simulations".**
   - The English is "With only a handful of runs". The constraint *few runs* is the reason for the question (T:912, T:915: about 20 points, where to put them), so the "only" stays.
   - The rest of the line already matched 10q.2.s4 ("Des réglages espacés régulièrement, ou resserrés près de chaque seuil ?"). +1 word.

7. **Translator notes updated.**
   - The notes now record changes 1-6 and their reasons.
   - The TTS remark was stale and is fixed. `audio/lexicon_fr.json` already pins every name in this unit (Rm "erre ème", VKS "vé ka esse", DRESDYN "Dresdine", MilaDy "Milédi", ABC "a bé cé"), so the line no longer says "French lexicon wanted".
   - The word counts are updated (table below), and the notes point to this file.

## Checked and kept

- **Meaning, numbers and hedges match the English.**
  - The numbers are "vingt-quatre réglages", "environ neuf", "Autour de dix-sept et demi" (the sign at 17.5 is unresolved, R:1114), "environ vingt-sept", "environ quarante pour cent" and "en trois dimensions". They match R:1066, R:1099, R:1101, R:143 and the symbol sheet §6 (03.4, 03.5).
  - "Cela concorde avec les résultats publiés" and "on ne teste ici que le solveur" keep the MEASURED scope of E3: kinematic test bench, no generative model (R:1179).
  - "Dans des simulations de VKS … a relevé le seuil" keeps critique B15: this is a simulation result (Nore et al. 2018), not the experiment. No "44" (D19).
  - "Peut peser plus d'un gigaoctet" and "quelques renversements" keep T:933 (an order-of-magnitude estimate) and T:62.
  - "Le plan de l'étude gravit un escalier" keeps the PLANNED status (the English review's change 3). The staircase is the plan's ladder, not a result.
  - The disclaimer is still one spoken sentence (D14). It keeps "indépendante", "prospective", "petites expériences", "un simple ordinateur" and "n'est validée ni par MilaDy, ni par ses partenaires, ni par les encadrants". This follows the site's "ni produit ni validé par … les encadrants". The supervisors' names stay on the lower-third only (D6).
- **Terms against the French site.**
  - P3 chapters 2 and 5 give: écoulement, étirer, transporter, diffusivité magnétique, taux de croissance, seuil, dynamo cinématique, champ germe, "le champ freine l'écoulement", saturation.
  - Rapport §E3 gives: fenêtres de dynamo, écoulement ABC, banc d'essai, solveur.
  - Other sources: "effet dynamo" (chSOA1, ch02 review), "en tire-bouchon" (02.4), cuve en précession, paroi, condition magnétique, apprentissage automatique (chSOA1, X5.2).
  - "Régimes cinématique et dynamique" agrees each adjective in the singular, as French physics writes it.
- **Planted pairs and echoes.**
  - Back from earlier units:
    - "la course" and "l'étirement contre l'estompage" (chSOA1.6.s4)
    - "comme un fil", singular, as in ch02 after its review
    - "Dans un mauvais conducteur" (02.1.s8)
    - "bouton" and "réglages" (02.2, 02.6)
    - "disques", not "turbines" (ch02 defines "deux disques à pales, les turbines")
  - Forward to later units:
    - "la boîte tourbillonnante" (10.1.s3, 10.4.s1)
    - "une caricature à trois cadrans" (04.1.s1 "Voici la caricature")
    - "Entre les points" (05.5.s3, 06.4.s6, 09.6.s5)
    - "Première / Deuxième / Troisième" (09.6.s5-s7)
    - "Qui peut dire quand aura lieu son prochain renversement ?" (00.4.s2)
- **Register.**
  - Vouvoiement in the imperatives: Imaginez, tournez, souvenez-vous.
  - "Nous" and "notre" mean the viewer and the narrator only ("notre ascension", "nous commençons").
  - There is no anglicism and no first-person anecdote.
- **Read-aloud checks.**
  - Rm, VKS, DRESDYN, ABC and MilaDy come out as "erre ème", "vé ka esse", "Dresdine", "a bé cé" and "Milédi".
  - The liaisons are natural: "tout un tableau", "de petites expériences", "quelques renversements".
  - There are no digits, abbreviations or tongue-twisters. "Les fils" (a homograph) is avoided.
  - "N'est-ce pas ?" carries the predict beat before the 3.0-s hold.

## Length and timing (estimates, `audio/tts.py` word count, French rate about 146 words per minute)

French elisions such as *l'écoulement* count as one word, so French syllables run higher than the word ratio suggests (03.1 and 03.6 look shorter than the English only for this reason).

| Scene | EN words | FR words | Change | Target | French, about |
|---|---|---|---|---|---|
| 03.1 | 79 | 77 | −3 % | 40 s | 32 s speech + 0.9 s break |
| 03.2 | 72 | 82 | +14 % | 32 s | 34 s + 0.9 s |
| 03.3 | 54 | 65 | +20 % | 25 s | 27 s + 0.9 s |
| 03.4 | 96 | 101 | +5 % | 45 s | 42 s + 4.8 s (3.0-s predict hold) |
| 03.5 | 67 | 81 | +21 % | 30 s | 33 s + 0.9 s |
| 03.6 | 51 | 50 | −2 % | 25 s | 21 s + 0.9 s |
| 03.7 | 105 | 118 | +12 % | 50 s | 48 s + 2.7 s |
| 03.8 | 33 | 40 | +21 % | 15 s | 16 s |
| ch03.Q | 17 | 18 | +6 % | 9 s | 7 s + 1.0 s hold |
| Total | 574 | 632 | +10 % | | about 4.8 min |

The review added 3 words in net. The word increase stays at or under the expected 15-20 % (BRIEF §9) in every scene but 03.5 and 03.8 (+21 % each). 03.2, 03.3, 03.5 and 03.8 run about 1 to 4 s over their targets, which the French timeline absorbs (scenes animate on cue names).

## Remaining doubts (for other reviewers or the lead; not changed here)

- **ch09 (other unit): 09.6.s6 should now say "là où elle est vraie".** 09.6.s6 ("Deuxième, chaque loi là où elle s'applique : …") calls back 03.7.s4, which now says "là où elle est vraie", as do 08.6.s5 and 11.2.s14. The suggested line is "Deuxième, chaque loi là où elle est vraie : exactement, oui ; {metric}en moyenne{/}, en partie."
- **ch10 (other unit): 10.4.s4 says "une croissance encore positive à dix-sept, déjà négative à dix-huit".** For the same reason as change 3, "un taux de croissance encore positif à dix-sept, déjà négatif à dix-huit" would be the precise phrasing. "Croissance négative" is an economist's oxymoron in physics.
- **03.5.s1 and 03.8.s1, "tout un tableau de bord".** It was kept because it is idiomatic and clear by ear. Strictly, a panel of knobs one turns is a "tableau de commande", while a "tableau de bord" is first a set of indicators. Change both together if the lead prefers the strict term.
- **03.3.s3, "pièces identiques".** "Pièces" can also be heard as *pieces*. In a tiling of the box that reading still works, and "rooms" stays the image. "Cellules" was not used because ch02.4.s3 uses it for the Karlsruhe spin generators.
