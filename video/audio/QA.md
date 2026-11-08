# Narration QA — English, voice "Ethan" (Fish Audio drama-3), 2026-11-08

Audio engineer's report. Machine-readable details per paragraph: `audio/qa_report.json` (text, transcript,
word error rate, missing/added words, lexicon terms, pace, loudness, silences, cue checks). Transcripts:
`audio/cache/asr/<key>.json` (ignored by git, like the rest of the cache). Tool: `audio/qa.py`.

## Summary

| | Core cut | Extended cut |
|---|---:|---:|
| Scenes | 105 | 143 |
| Paragraphs (TTS requests) | 233 | 333 |
| Narrated words | 6,955 | 9,754 |
| **Speech** (paragraph audio, pauses inside paragraphs included) | **50:01** | **70:23** |
| Narration track (+ 0.9 s paragraph breaks and `hold_after`) | 52:56 | 74:39 |
| **Film running time** (+ `lead_in`, `tail`) | **56:05** | **78:53** |
| Sum of the scripts' `target_s` | 53:10 | 74:51 |
| Brief's estimate (D3) | ≈ 41 min | ≈ 60 min |
| Effective pace (words / running time) | 124 wpm | 124 wpm |

- All 339 distinct paragraphs of the 24 unit scripts were synthesized: only the main paragraphs, never the
  `result` variants (they wait for the data). No failure, no retry, no refusal from the API.
- Defects found and fixed: 7 pronunciations (lexicon), 24 paragraphs re-synthesized once; 12 sentence cues
  that the aligner had placed 0.75–1.5 s off (`align.py`, version 3).
- Speech recognition finds no missing word and no added word in any paragraph. Mean word error rate is
  0.6 % (293 of 339 paragraphs exact), and every residual is a recognizer spelling or homophone, or a
  proper name said on purpose in French.
- The acting cue is never read aloud, and neither is any `[long pause]` or phoneme tag. Every paragraph
  break is present, at its nominal length.
- **The main open issue is length, not audio.** The voice keeps to the scripts' budgets (+5 %). The scripts'
  budgets themselves add up to 53 / 75 min, against ≈ 41 / ≈ 60 min in the brief. This is the lead's call:
  trim the scripts, or accept the longer cuts.

## 1. Synthesis

- Request: one `POST https://api.fish.audio/v1/tts` per paragraph, header `model: drama-3`, body exactly as
  validated (temperature 0.1, mp3 192 kb/s, 44.1 kHz, latency normal, language en, normalize, condition on
  previous chunks, prosody speed 1.0 + normalize_loudness). Voice: `536d3a5e000945adb7038665781a4aca` in all
  24 scripts (no `audio/voice.json` override). The text is `[calm, natural narrator voice] ` followed by the
  paragraph, with the subtitle markup stripped and the lexicon pins applied.
- Order of work: a `--mode dry-run` of both cuts first, giving 339 distinct requests and 9,914 words, under the
  15,000-word guard. Then the extended cut live, 2 requests at a time (333 paragraphs), and the core cut live
  (the 6 core-only paragraphs of 10.8 and 10.9). The whole first pass took about 8 minutes.
- Billed in total today: 411 requests, 12,060 words, about 88 KB of text and 91 min of audio. That is the first
  pass, 48 A/B pronunciation tests and 24 re-takes. Every take stays in `audio/cache/` (674 MB), so going back
  to an earlier pin costs nothing.
- `tts.py` change: an HTTP 401, 402 or 403, or a "quota / insufficient / balance / credit" message, now stops the
  whole run at once. The run no longer moves on paragraph after paragraph against a refusing account.
  Retryable codes (429, 5xx) keep their exponential backoff.

## 2. Durations: timelines built, nothing rendered

`node build.js --cut core|extended --plan` (no `make data`, no render) wrote `script/_build/<cut>_timeline.json`,
`<cut>_cues.json` and `subs/<cut>.{srt,vtt,ass}` from the real narration. Per unit, in mm:ss:

### Core cut: 105 scenes

| Unit | Scenes | Words | Target (sum of `target_s`) | Actual | Actual / target | Speech only |
|---|---:|---:|---:|---:|---:|---:|
| ch00 | 6 | 181 | 1:24 | 1:29 | 1.06 | 1:16 |
| ch01 | 7 | 385 | 2:57 | 3:03 | 1.04 | 2:38 |
| ch02 | 7 | 411 | 3:14 | 3:23 | 1.05 | 2:59 |
| chSOA1 | 6 | 336 | 2:39 | 3:06 | 1.17 | 2:48 |
| ch03 | 9 | 574 | 4:31 | 4:27 | 0.99 | 3:59 |
| ch04 | 8 | 549 | 4:14 | 4:29 | 1.06 | 4:00 |
| ch05 | 6 | 361 | 2:49 | 2:49 | 1.00 | 2:28 |
| ch06 | 6 | 437 | 3:14 | 3:32 | 1.09 | 3:09 |
| ch07 | 7 | 542 | 4:12 | 4:23 | 1.04 | 3:55 |
| ch08 | 8 | 663 | 4:58 | 5:11 | 1.04 | 4:37 |
| ch09 | 7 | 578 | 4:14 | 4:40 | 1.10 | 4:12 |
| chSOA2 | 9 | 653 | 5:00 | 5:31 | 1.10 | 5:06 |
| ch10 | 10 | 653 | 4:54 | 5:08 | 1.05 | 4:36 |
| ch10q | 6 | 367 | 2:50 | 2:51 | 1.01 | 2:31 |
| ch11 | 3 | 265 | 2:00 | 2:02 | 1.01 | 1:45 |
| **total** | **105** | **6955** | **53:10** | **56:05** | **1.05** | **50:01** |

### Extended cut: 143 scenes

| Unit | Scenes | Words | Target (sum of `target_s`) | Actual | Actual / target | Speech only |
|---|---:|---:|---:|---:|---:|---:|
| ch00 | 6 | 181 | 1:24 | 1:29 | 1.06 | 1:16 |
| ch01 | 7 | 385 | 2:57 | 3:03 | 1.04 | 2:38 |
| ch02 | 7 | 411 | 3:14 | 3:23 | 1.05 | 2:59 |
| chSOA1 | 6 | 336 | 2:39 | 3:06 | 1.17 | 2:48 |
| ch03 | 9 | 574 | 4:31 | 4:27 | 0.99 | 3:59 |
| ch04 | 8 | 549 | 4:14 | 4:29 | 1.06 | 4:00 |
| ch05 | 6 | 361 | 2:49 | 2:49 | 1.00 | 2:28 |
| ch06 | 6 | 437 | 3:14 | 3:32 | 1.09 | 3:09 |
| ch07 | 7 | 542 | 4:12 | 4:23 | 1.04 | 3:55 |
| ch08 | 8 | 663 | 4:58 | 5:11 | 1.04 | 4:37 |
| X2 | 6 | 503 | 3:56 | 3:52 | 0.98 | 3:28 |
| X3a | 6 | 382 | 2:59 | 3:07 | 1.05 | 2:44 |
| ch09 | 7 | 578 | 4:14 | 4:40 | 1.10 | 4:12 |
| X4a | 5 | 399 | 2:51 | 3:14 | 1.14 | 2:57 |
| chSOA2 | 9 | 653 | 5:00 | 5:31 | 1.10 | 5:06 |
| ch10 | 9 | 522 | 3:59 | 4:11 | 1.05 | 3:45 |
| X5a | 5 | 339 | 2:39 | 2:47 | 1.05 | 2:29 |
| X1 | 4 | 302 | 2:24 | 2:24 | 1.00 | 2:10 |
| X4b | 1 | 97 | 0:45 | 0:49 | 1.10 | 0:44 |
| X3b | 1 | 85 | 0:40 | 0:41 | 1.03 | 0:37 |
| X6 | 8 | 622 | 4:47 | 5:04 | 1.06 | 4:30 |
| X5b | 3 | 201 | 1:35 | 1:46 | 1.12 | 1:34 |
| ch10q | 6 | 367 | 2:50 | 2:51 | 1.01 | 2:31 |
| ch11 | 3 | 265 | 2:00 | 2:02 | 1.01 | 1:45 |
| **total** | **143** | **9754** | **74:51** | **78:53** | **1.05** | **70:23** |

Scenes outside `target_s` ± 15 %. None is short. These are over:

- Both cuts (15 scenes): 00.1 (11 → 13.3 s, +21 %); 00.3 (16 → 18.8 s, +18 %); SOA1.1 (21 → 26.2 s, +25 %);
  SOA1.3 (20 → 25.1 s, +25 %); SOA1.4 (40 → 49.8 s, +24 %); 04.2 (45 → 51.8 s, +15 %); 05.4 (15 → 17.3 s, +16 %);
  06.1 (35 → 41.6 s, +19 %); **09.6 (45 → 60.0 s, +33 %)**; SOA2.3 (23 → 27.0 s, +17 %); SOA2.4 (50 → 60.3 s, +21 %);
  SOA2.6 (42 → 48.8 s, +16 %); 10.4 (40 → 46.1 s, +15 %); 10.5 (40 → 46.7 s, +17 %); ch10.Q (9 → 10.5 s, +16 %).
- Extended cut only (5 more): X4.5 (40 → 49.7 s, +24 %); X4a.Q (9 → 10.6 s, +18 %); X5.4 (35 → 40.3 s, +15 %);
  X6.Q (9 → 11.3 s, +26 %); X5.6 (45 → 52.6 s, +17 %).
- Question cards over the 6–10 s rule: ch10.Q 10.5 s, X4a.Q 10.6 s, X6.Q 11.3 s. The other 16 cards run
  7.8–10 s.

Pace. Words per minute of speech are 139 over the whole film (median paragraph 143; 5–95 % range 120–174).
That is slower than the 146 wpm in D21 and in the `make plan` lint (`RAW_WPM`), so the lint underestimates
lengths by about 5 %. Measured on this voice, about 139 wpm of speech would be the right figure. The effective
pace is 124 wpm, just under the 125–130 target of D21. The slowest paragraphs are lists and dates (X4.5 p2 at
95 wpm, SOA1.4 p1 at 103). The fastest are short predict-beat questions (02.5 p2, 10 words in 2.35 s; 05.1 p2;
11.2 p1; ch09.Q): brisk, but complete, and their `hold_after` follows.

## 3. Speech-recognition check

Method: faster-whisper `small.en` (CPU, int8, beam 5, word timestamps, no prompt, so the script cannot bias
it) on every paragraph's cached take. It was installed with 8.4 GB free; 6.4 GB are free now. Its transcript is
compared with the script, both normalized: lower case, no punctuation, digits expanded to the form that best
matches the script ("0.86" → "zero point eight six"), UK/US spellings and true homophones merged, and split
compounds joined. The recognizer is only a QA tool: subtitles still come from the script text (D16), and the
build never calls it.

- **Missing words: none.** No paragraph has a deleted script word, and no paragraph was cut short. Two
  residuals are normalization artifacts, not speech: X5.5 "eleven hundred and fifty" written as "1,150", and
  X4.3 "a proved" heard as "approved".
- **Added words: none in the speech.** The recognizer wrote one extra word in 8 paragraphs: at the very end of
  6 ("out", "treatment", "time", "week", "end", "quickly": 05.2 p3, 06.3 p3, 07.6 p2, 08.5 p4, X5.1 p1, X5.3 p1)
  and between two sentences in 2 ("savings" in SOA1.4 p2, "cloud" in SOA2.4 p1). Most have a probability
  of 0.01–0.25; "time" and "end" reach 0.6–0.8 and echo the last syllable. The waveform shows each one sits
  on the decay of the word before or on a breath, 10–25 dB under the voice (−26 to −46 dBFS), so they are
  recognizer hallucinations, not words. No repetition, no babble, no stutter. The other "insertions" in
  the report come from splitting names (Gissinger, Jean Zay, SFEMaNS, "Dressed Dine").
- Acting cue and tags read aloud: none ("calm", "narrator voice", "long pause", "phoneme" appear in no
  transcript).
- Word error rate, final takes: mean 0.64 %, 293 of 339 paragraphs exact, at most 13 % (X4.3 p2: Gissinger in
  French, plus a "waits/weights" homophone). The residual substitutions are recognizer spelling or homophones
  (poll/pole, reweighting/rewaiting, waits/weights, their/there, halve/have, eta/ada, vermillion, poloidal,
  Prandtl, Cadarache) or the names below.

### Lexicon terms: recognizer's reading, first pass → after the fixes

| Term | Occurrences | First pass (heard as written) | Fix | After |
|---|---:|---|---|---|
| VKS | 21 paragraphs | 13 / 21 (also "vicus", "VKEA", "case", "VK") | pin → respelling `V-K-S` | **21 / 21** |
| Rm | 17 | 12 / 17 (also "arum", "rem", "arim", "arm") | pin → respelling `R-M` | **17 / 17** |
| precessing | 4 | 0 / 4 (all "processing") | new pin `P R IY0 S EH1 S IH0 NG` | **4 / 4** |
| quadrupole | 4 | 3 / 4 (04.2 p1 "quadruple"); a pin did not help | new respelling `quadru-pole` | **4 / 4** |
| MilaDy | 5 | 1 / 5 ("malady", "melody") | `M IH0…` → `M IH1 L EY1 D IY0` | **5 / 5** (X5b.Q "Milliday's") |
| DRESDYN | 6 | 1 / 6 (mostly "Dresden") | pin → respelling `Dress-dine` | 4 / 6 ("dress-dine", "Dressdyne"); 03.5 p1 and 10.9 p2 still "Dresden" |
| SFEMaNS | 1 | heard "SMN" | pin → respelling `S-FEM-ans` | heard "S-Femin" |
| Reynolds, Pm, Rice, ABC, LATU | 8, 7, 16, 1, 1 | all as written, except Rice heard "rise" once (ch05.Q) | none | all as written (ch05.Q re-taken for VKS) |
| Gissinger (French, D12), Jean Zay | 2, 1 | "G-Zan J", "Zisanger"; "Jan Z" | none: the French reading is intended | to confirm by ear |

How the fixes were chosen: two candidate entries per term were synthesized on every flagged paragraph and
transcribed (48 test requests, kept in the cache). The winning entry then went into `audio/lexicon.json`,
with a dated note, and only the paragraphs containing the term were re-synthesized: 22 in the extended cut
plus 2 core-only, 772 words. Then those paragraphs were transcribed again. Each paragraph was re-synthesized
once.

## 4. Sentence cues: aligner fix

The recognizer's word times give an independent check of the cue times found by `align.py`. In the first
pass, 12 of 515 sentence starts after the first were 0.75–1.5 s off: 02.1.s6, 02.2.s3, 02.4.s2, 02.4.s3,
SOA1.2.s2, 05.2.s9, 06.4.s6, 07.1.s6, 07.4.s2, 09.6.s5, 09.6.s6, X6.5.s4. Animations on those cues would have
fired a second early or late, and their subtitles changed at the wrong moment. The cause: the silence
programme took a comma or colon pause for the sentence end, either because the predicted position, from
character counts, was skewed by the pauses themselves, or because the script sentence holds two spoken
sentences ("No. Each whirlpool…").

Fix in `align.py`, now version 3, so every scene was re-aligned:

1. The prediction is made in voiced time, with the detected pauses taken out, and long pauses get a stronger
   bonus (`LEN_BONUS` 1.5).
2. `audio/align_hints.json`, written by `python3 -I audio/qa.py hints` from the recognizer pass, gives the
   approximate start of each later sentence (507 starts on 264 paragraphs). A hinted boundary takes the
   pause whose end is nearest. Hints too far from any pause (8 of them) are dropped and the programme decides
   there. Times remain silence-based and the text the script's (D16); without the file, the build works as
   before.

Result: the 12 starts now sit on the right pause, each one checked against the waveform and the transcript.
Against the recognizer, the median deviation is 0.06 s and 95 % of starts are within 0.26 s. The 6 remaining
deviations over 0.6 s (SOA2.7 p2, 11.1 p1, X3.2 p2, X5.2 p2, 10q.2 p2) come from the recognizer's own
timestamps: it puts a word inside the pause before it. On the placeholder test voice the aligner still reads
5.2 ms mean and 14 ms max against the truth. Two script sentences hold a deliberate inner pause of about
0.9 s: 04.5.s5 "…spend its time? Two humps…" and X4.2.s6 "Confidence: medium; …". Split them if a scene
needs a cue there.

## 5. Loudness and silences

- Per-paragraph loudness (EBU R128) is −22.0 LUFS median, standard deviation 0.5 LU, range −23.7 to −20.7. The
  5 quietest are short paragraphs of 5–19 words, at most 1.7 LU under the median. Neither the ear nor the
  mixer's single master gain will notice; the final mix goes to −16 LUFS. Raw true peak at most −0.2 dBTP,
  sample peak at most 0.97: nothing clips.
- Silence at the start of each take: 0.10–0.29 s; at the end: 0.39–1.18 s. Both are trimmed by `align.py`,
  which keeps 0.05 s before and 0.12 s after the speech.
- Pauses between sentences inside a paragraph (the voice's own): 515 pauses, median 0.71 s, 5–95 % range
  0.51–0.92 s, from 0.27 s (X4.5 p3) to 1.31 s (02.1 p1). All natural. No sentence runs into the next.
- Pauses inside a sentence over 0.9 s: only the two deliberate ones in section 4.
- `[long pause]`: never sent. Each paragraph is its own request, so the tag can be neither read aloud nor
  ignored. Each of the 146 paragraph breaks measures exactly 0.9 s + `hold_after` + 0.17 s (the trimming
  pads), within 0.02 s. `hold_after` values used: 0, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 2.5 and 3 s.
- Contrast: a plain paragraph break (1.07 s of silence) is only about 0.35 s longer than a typical
  sentence pause (0.71 s). If the reviewers want the paragraph breaks to stand out more, set `LONG_PAUSE_S`
  to 1.1–1.2 s in `tts.py`. It costs no API call, but adds about 0.2 s × 190 breaks ≈ 40 s to the extended
  cut and re-times every scene.

## 6. Remaining issues

1. **Length (lead's decision):** 56:05 and 78:53 against ≈ 41 and ≈ 60 min (D3). The voice is on budget
   (+5 %); the scripts' `target_s` sums are not. Twenty scenes run over +15 % (section 2), led by 09.6 (+33 %),
   X6.Q, SOA1.1, SOA1.3, SOA1.4 and X4.5, and three question cards run over 10 s.
2. To confirm by ear: two DRESDYN takes still heard as "Dresden" (03.5 p1, 10.9 p2); Gissinger in French
   (04.1 p2, X4.3 p2); Jean Zay (10q.4 p2); SFEMaNS and LATU (chSOA2.Q); and three possible slips the
   recognizer is unsure of: "wins" heard "winds" (02.2 p1, new take), "seed" heard "seat" (08.5 p5),
   "spectra" heard "spectrum" (09.5 p1). Each needs one listen. A re-take is a lexicon or text change,
   since the cache key is the text.
3. Preferred pronunciations still to settle with the user or the supervisors (`lexicon.json` → `check`):
   MilaDy (now stressed "MIL-ay-dee" with a full first vowel; the prototype had "MIL-a-dee"), DRESDYN,
   SFEMaNS, LATU, CEREA, LISN, GENCI, Kármán. Changing an entry re-synthesizes only the paragraphs that
   contain it: one command, a few cents.
4. `RAW_WPM` = 146 in `tts.py` and `tools/assemble_cut.py` makes the lint underestimate by about 5 %. About
   139 wpm of speech is the measured figure. The constant belongs to the foundation engineer: noted, not
   changed.
5. `make test` was not rerun; it renders. The align change was checked on the test units' placeholder audio
   (5.2 ms mean error), and `tts.py` dry, live and auto modes ran normally all session.

## 7. Files and commands

- Changed: `audio/lexicon.json` (VKS, Rm, DRESDYN, SFEMaNS, MilaDy; new precessing, quadrupole; each with a
  dated note), `audio/tts.py` (stop on refusal), `audio/align.py` (version 3: voiced-time prediction and
  hints). The French-narration work (`lang`, `scenes_fr`, `lexicon_fr.json`) changed the same files at the
  same time; both sets of changes are in the files.
- New: `audio/qa.py` (QA tool), `audio/qa_report.json`, `audio/align_hints.json`, `audio/QA.md`;
  transcripts in `audio/cache/asr/`.
- Rebuilt, nothing rendered: `script/_build/{core,extended}_{tts,timeline,cues}.json`, `film_*.json`,
  `subs/{core,extended}.*`, `audio/scenes/*`.
- To rerun after a script or voice change. The recognizer is optional (`pip install faster-whisper`, model
  `small.en`, ≈ 0.5 GB):

  ```bash
  python3 -I tools/assemble_cut.py --cut extended; python3 -I tools/assemble_cut.py --cut core
  python3 -I audio/tts.py script/_build/film_extended.json --mode dry-run --quiet    # words to bill
  python3 -I audio/tts.py script/_build/film_extended.json --mode live --jobs 2      # then the core cut
  python3 -I audio/qa.py transcribe && python3 -I audio/qa.py hints && python3 -I audio/qa.py report
  node build.js --cut extended --plan; node build.js --cut core --plan              # align, timelines, subtitles
  ```
