# Production brief — "How Often Does the Field Flip?" (MilaDy 2027 explainer film)

This brief is the single source of truth for everyone producing the film. Read it fully before any
work. The plan documents in `plan/` (outline, styles, pedagogy, inventory, pipeline, critiques) are
reference material; where they conflict with this brief, **this brief wins**.

## 1. Purpose and audience

- **Primary purpose (user's own words, 2026-11-08):** the film must help the author *understand the
  subject* and *ask the right questions to the supervisors before launching the simulations*. It is a
  learning tool first, a public explainer second.
- Audience ladder L0 (anyone) → L5 (supervisors, specialists), climbing smoothly (outline §2). Pedagogy
  in the spirit of the best visual-mathematics and science communicators: picture first, then words,
  then the formula; one idea at a time; predict-before-you-see beats; recurring motifs and payoffs.
- Language: English narration and on-screen text. The companion question sheet is in French.

## 2. Decisions (resolved; do not reopen)

| Id | Decision |
|---|---|
| D1 voice | Fish Audio library voice **"Ethan"** (author "Fish Official", an original voice that imitates no real person), `reference_id` **`536d3a5e000945adb7038665781a4aca`**. No other voice, and never a clone or imitation of a real person. The voice is a single parameter of the script (`voice.reference_id`) so the narration can be swapped later (section 7). |
| D2 access | Fish Audio API key is injected by the network proxy for `api.fish.audio`: send `Authorization: Bearer proxy-injected`. Model header `model: drama-3`; body settings exactly as in `/home/user/videobook/BRAINSTORM.md` ("Paramétrage validé"). |
| D3 cuts | Two cuts from the same scenes: **extended cut** (core + modules, ≈ 60 min, flagship) and **core cut** (≈ 41 min). Running orders: `plan/outline.json` → `cuts`. |
| D4 runs | **No new simulation, training or benchmark is run for the film.** Only results that already exist in the repository are used (E1, E2, E3, figures, result JSON). Every scene the outline marks PROVISIONAL becomes **PENDING** (empty seat). |
| D5 release | Ship now with empty seats. When the cloud results arrive: re-render only the affected scenes; publish a "Results update" episode + a v2 of the film. |
| D6 names | Supervisors' names in text only (end card, lower-third of 03.7), no photos, no logos, no opinions attributed to them. |
| D7 facts | External facts (seafloor magnetic stripes, last geomagnetic reversal, self-exciting disc dynamo…) are allowed **only with a source** (scene `sources`, on-screen reference chip, and the description). |
| D8 formulas | Formula layer: full statements on a separate on-screen layer (small type), never in subtitles, never narrated. |
| D9 look | Dark-dominant (NIGHT ≈ 75 %, PAPER for derivations, BLUEPRINT for infrastructure), key-coloured field maps (styles.md). |
| D10 sound | Original music bed synthesized in code under L0–L2, silence under L4–L5; sound effects kept (needle, crossing ticks…). |
| D11 render | 1080p30 master, rendered on this machine. Keep every final MP4 file under 1.9 GB (release-asset limit): CRF 20–23 and a `-maxrate` cap where needed. |
| D12 pronunciation | `audio/lexicon.json` entries; Gissinger pronounced in French. |
| D13 title | **How Often Does the Field Flip?** Subtitle: *Physics-constrained generative models for turbulent dynamos — a learner's map of the MilaDy project.* |
| D14 disclaimer | As drafted in the outline (03.7 lower-third + one spoken sentence; full text on the end card). |
| D15 Short | Not now. |
| D16 subtitles | Sentence-level timing (silence-based alignment), burned in from the **script text**, never from a transcription. |
| D17 Bet 1 | State it as s(17) > 0 > s(18) (the configured 64³ ABC campaign sweeps integer Rm). Whether to add Rm = 17.25, 17.5, 17.75 becomes a **question for the supervisors**. |
| D18 Taylor–Green | Flag and exclude non-saturated runs; whether to lengthen runs near the threshold becomes a **question for the supervisors**. |
| D19 site | The VKS threshold inconsistency on prep module 3 is fixed on the site separately; the film drops "44". |
| D20 hook | Compass needle flips at ≈ 7 s with the chip "illustration, not to time scale". |
| D21 pace | Script at 125–130 **effective** words per minute. Measured raw pace of the Ethan voice with the validated settings: ≈ 146 words per minute including `[long pause]` breaks (95 words → 39 s). Budget each scene's words from its target duration. |

## 3. What changes from the outline (new framing, user's request)

1. **A question card ends every chapter.** One question the viewer (the author) should bring to the
   supervisors, born from what the chapter just explained, with *why it matters* and *what decision it
   unblocks* (which simulation to run, with which parameters; which metric; which data). Short on
   screen (≤ 18 words), spoken in one sentence, 6–10 s, its own scene id `chXX.Q`.
2. **Results that do not exist yet are predictions plus the question that decides the computation.**
   Every PENDING scene shows the bet, the reasoning, the success criterion from the PhD plan, the
   confidence level, and the question to settle with the supervisors *before* renting compute. Two
   narration variants: `pending` (now) and `result` (written for both outcomes, numbers injected from
   the data file).
3. **A new chapter "Before we compute" (`ch10q`) precedes the closing `ch11`**: the questions gathered
   and ranked by what they unblock — (a) which simulations and with which parameters, (b) the
   scientific framing (constraints, metrics, success criteria), (c) logistics (data access, lab GPUs,
   GENCI Jean Zay access, budget). ≈ 2–3 min. It points to `infra/cloud/RECOMMANDATION-CLOUD.md` §0.
4. **Honesty badges** on every claim-bearing scene: `MEASURED` (E1–E3 results), `PROVED` (a
   proposition of the note/report), `CONJECTURE` (with confidence: high/medium/low), `PLANNED` (PhD
   plan), `CONTEXT` (external, sourced fact). Small chip, top-right.
5. The report's own limits stay audible: prospective report, CPU-only experiments, 1–2 seeds, weak
   spectra, interpolation only.

## 4. Repository layout (`/home/user/milady-2027/video/`)

| Path | Content | Who writes |
|---|---|---|
| `BRIEF.md` | this brief | lead only |
| `plan/` | outline, styles, pedagogy, inventory, pipeline, critiques | read-only |
| `script/<unit>.json` | narration + scene specs of one unit (schema §5) | that unit's writer and reviewer |
| `script/_shared/` | symbol sheet, glossary, question register, continuity notes | consistency editor |
| `scenes/<unit>/*.html` | one page per scene | that unit's scene builder |
| `runtime/`, `runtime/components/` | deterministic runtime and shared components | foundation engineer only |
| `data/*.json` | scene data, produced by `tools/extract_data.py` from repository results | foundation engineer and builders (via the tool) |
| `audio/` | `tts.py`, `align.py`, `lexicon.json`; `cache/` (ignored) | foundation / audio engineer |
| `build.js`, `capture.js`, `subs.js`, `stills.js`, `Makefile`, `tools/` | pipeline | foundation engineer only |
| `out/` | renders (ignored by git) | build only |

Never modify anything outside `video/` (the site, `milady/`, `infra/`…). Never run simulations,
training or benchmarks. Never commit or push: the lead does.

## 5. Script schema (`script/<unit>.json`, schema version 2)

```json
{
  "schema": 2,
  "unit": "ch04",
  "title": "Chaos and the shoebox of photographs",
  "cut": "core",
  "level_range": "L2-L3",
  "voice": {"provider": "fish", "model": "drama-3", "reference_id": "536d3a5e000945adb7038665781a4aca"},
  "scenes": [
    {
      "id": "04.1",
      "was": "C4.1",
      "title": "Three dials",
      "file": "scenes/ch04/04_1_three_dials.html",
      "status": "ready",
      "level": "L2",
      "register": "NIGHT",
      "badge": {"kind": "CONTEXT", "confidence": null},
      "target_s": 30,
      "lead_in": 0.4,
      "tail": 0.8,
      "deps": [],
      "entry": {"data": {}, "params": {}},
      "paragraphs": [
        {"hold_after": 0.0, "sentences": [
          {"id": "04.1.s1", "cue": "dials", "text": "Picture three dials, linked by springs."},
          {"id": "04.1.s2", "cue": "eqs", "text": "One is the {b}dipole{/}, the north-south part of the field."}
        ]},
        {"hold_after": 2.5, "sentences": [
          {"id": "04.1.s3", "cue": "predict", "text": "Before we run it: will the dipole ever change sign?"}
        ]}
      ],
      "onscreen": {"title": "", "labels": [], "formulas": [{"cue": "eqs", "tex": "\\dot Q = 0.119\\,Q - V D"}], "chips": ["phenomenological model (Gissinger 2012)"]},
      "visual": "What moves, in which colour, on which cue (from the outline, refined).",
      "assets": ["assets/interactif/gissinger.js"],
      "sources": ["R:159", "en/rapport/index.qmd#e1", "external: <author year, URL> (CONTEXT facts only)"],
      "variants": null,
      "question": null
    }
  ]
}
```

- `status`: `ready` or `pending` only (D4). `deps` lists every data file the scene reads.
- `paragraphs`: TTS is requested per paragraph; `[long pause]` is inserted only between paragraphs;
  `hold_after` (seconds) adds silence after a paragraph for predict beats.
- Cues are the sentence starts; the scene animates on cue *names*, never on hard-coded times.
- Subtitle markup in `text`: `{u}…{/}` velocity (blue), `{b}…{/}` magnetic field (vermillion),
  `{param}…{/}` control parameter (green), `{model}…{/}` generative model (violet), `{metric}…{/}`
  distribution-level metric (amber). Markup is stripped for TTS.
- Pending scenes: `"variants": {"result": {"paragraphs": [...], "data_fields": ["..."]}}` — the result
  narration with `{{field}}` placeholders filled from the data file at build time; the main
  `paragraphs` are the `pending` variant.
- Question cards: `"question": {"en": "...", "fr": "...", "why": "...", "unblocks": "...", "ask_who": "S. Cheng / D. Lucor / C. Nore / Y. Ponty or 'the supervisors'"}`.
- Extension units also carry `"insert_after": "<scene id>"`.

## 6. Writing rules

- Written for the ear and for TTS: short sentences, concrete nouns, no parentheses, no abbreviations
  the voice would spell oddly (write "Rm" only with a lexicon pin), numbers written as they should be
  read ("zero point eight six", "about nine times"). No stage directions in the text except what the
  TTS settings allow (the leading `[calm, natural narrator voice]` and `[long pause]` are added by the
  tool, never written by hand).
- Pace: 125–130 effective words per minute (§2 D21). Respect each scene's `target_s` ± 15 %.
- Every number and claim traceable to `sources` (file:line or anchor in the site, or a dated external
  source for CONTEXT facts). Use the symbol sheet of `plan/outline.md` §2 strictly.
- Use the corrections already applied in the revised outline (`plan/outline.md` §9) — do not
  reintroduce errors listed in `plan/critique_accuracy.md`.
- No hype, no overclaiming: the report is prospective; say what is measured, what is proved, what is
  conjectured, what is planned.
- The narrator never claims to be a person; no first-person anecdotes; "we" means "the report" or
  "the viewer and the narrator" only.

## 7. Narration swap kit (deliverable)

The narration must be replaceable without touching the animations:
- `voice.reference_id` per script; `make narration VOICE=<id>` re-synthesizes every paragraph, re-aligns,
  re-times the timeline (scenes animate on cue names), re-renders only what moved, re-assembles.
- An external narration (recorded elsewhere) can be fitted cue by cue (`tools/fit_narration.py`:
  per-sentence time-stretch within ±12 %, or re-timing of the scenes).
- Deliver separate stems: film without narration (music + effects), narration alone, music alone,
  effects alone; the final MP4 carries narration+mix as track 1 and the no-narration mix as track 2;
  `subs/film.srt` and `script/cues.json` give every sentence's timing.

## 8. Quality bar

- Accuracy first: every claim checked against the site (`en/rapport`, `en/these`, `en/experiences`,
  `en/encadrants`, `en/calcul`, `experiences/resultats/*.json`).
- Visual clarity: one idea per shot, text ≥ 28 px at 1080p, nothing overlapping, nothing cut at the
  frame edge, colour key respected, deterministic frames.
- Every scene renders without page errors; no blank frames; cues line up with the narration.
