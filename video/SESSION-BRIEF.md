# Session brief: building a batch of scene units (parallel cloud session)

You are a **scene builder** for the explainer film *How Often Does the Field Flip?* (MilaDy 2027). You build the
HTML scene pages of a batch of units, check them, have them reviewed independently, fix them, and push them to
`main`. Other agents work on the same repository at the same time. One agent synthesises the narration; another
translates. The lead merges and renders. This brief is self-contained. Where it and `video/BRIEF.md` disagree,
BRIEF.md wins, then `video/CONTRACT.md`.

## 1. Repository, branch, batch

- Repository **`knoel99/milady-2027`**, branch **`main`**. Work directly on `main`; there are no feature branches.
  Every path below is relative to `video/` unless it starts with `video/`.
- **Your batch**: the prompt that launched you gives a batch number `<n>` and a list of units (for example
  `ch05, ch06, ch07`). If either is missing, stop and say so.
- **Unit**: one script file `script/<unit>.json` (schema 2), one folder `scenes/<unit>/`, one page per scene.
  The pilot unit `ch04` is done: copy its patterns, not its workarounds.

## 2. Read first, in this order

1. `video/BRIEF.md`: decisions D1–D21, writing and quality rules. Read it all.
2. `video/CONTRACT.md` §1–§12 (page format, `Scene.define`, cues, every component, data, pending seats, layout,
   performance, determinism, what not to do, reviewer checklist). Then **§13 "Lessons from the pilot (ch04)"**:
   the patterns to copy, the pitfalls, the verification routine and the definition of done. Then the Pipeline
   section P2–P7 (what your page receives, checks).
3. `video/plan/styles.md` §2–§3 (design principles, registers, palette, type, motifs, transitions, pacing).
4. `video/README.md` (French): the commands.
5. For each of your units: `script/<unit>.json` (narration, cues, `onscreen`, `visual`, `badge`, `sources`,
   `entry`), `script/fr/<unit>.json` (French timing will be longer), and `script/_shared/` (symbols, glossary).
6. `script/_review/scenes_ch04.md`: the pilot's build report and independent review (the level of rigour expected).
7. The worked examples: `scenes/ch04/*.html`, and the gallery `scenes/_gallery/gallery.html`. To open it, run
   `make serve`, then go to `http://127.0.0.1:8765/scenes/_gallery/gallery.html?plate=K`. Its stills are in `out/gallery/`.

## 3. Allowed files (and only these)

| Path (in `video/`) | What |
|---|---|
| `scenes/<unit>/**` | your pages `<id>_<slug>.html`, the unit's helpers `<unit>_kit.js`, `<unit>.css` |
| `tools/data_<unit>.py` | extractor of values that `data/` lacks, from files that already exist in the repository |
| `data/<unit>_*.json` | written by that tool only (with `meta`) |
| `script/_review/scenes_<unit>.md` | build report, independent review, kit issues |
| `script/<unit>.json` | **only** the fields `file`, `deps`, `entry`, `visual` of its scenes (`visual`: append an "AS BUILT" paragraph; never rewrite the writer's text) |
| `script/_review/scenes_batch_<n>.done.md` | the completion marker (§8) |

Everything else is read-only for you. That includes `runtime/`, `runtime/components/`, `build.js`, `capture.js`,
`stills.js`, `subs.js`, `Makefile`, `tools/*` except your own `data_<unit>.py`, `audio/`, `data/` except your
files, `script/_build/`, `subs/`, `script/fr/`, `script/_shared/`, other units, `BRIEF.md`, `CONTRACT.md`, the site
outside `video/`.

## 4. Forbidden

- **No edit to the shared kit or the pipeline.** If a component is missing or wrong, write a workaround inside
  `scenes/<unit>/<unit>_kit.js`, marked `WORKAROUND (kit issue: …)`, and **report** it (§7). Never patch `runtime/`.
- **No narration edit.** This covers sentence text, cues, paragraphs, `hold_after`, `onscreen`, `badge`, `question`,
  `sources`, `status`, the French overlays. When a sentence contradicts what the model or the data shows (the pilot
  found two), draw what is true and report it to the writer in your review file.
- **No API call.** Never call the Fish Audio API or any paid service. Never run `make film`, `make films`,
  `make scene`, `make narration`, `make tts-test`, `make fit`, `make plan`, `make test`, or `make draft` without
  `U=`. Some of these bill the narration; others write into `audio/` or `script/_build/`.
- **No simulation, training or benchmark** (BRIEF D4). Only results that already exist in the repository are used.
  A live integration of the three-mode model *inside a page* (`Kit.threeModes`, a few thousand RK4 steps,
  illustration only) is allowed, as in ch04. Anything heavier is not. A number that does not exist in the
  repository stays PENDING; it becomes a question for the supervisors.
- No number typed in a scene, no hex colour, no CDN, no text under 28 px, nothing in the subtitle band (y ≥ 900),
  no synthetic or test file in `data/` (CONTRACT §10).
- Never `git add -A` or `git add .`, never `--force`, never rewrite published history, never commit `out/`, `.tmp/`,
  `node_modules/`, `script/_build/`, `subs/` or anything under `audio/`.

## 5. Environment

```bash
cd video
export NODE_PATH=/opt/node22/lib/node_modules        # where playwright lives on the lead's machine
node -e "require('playwright')" && ffmpeg -version | head -1 && python3 --version
```

If `require('playwright')` fails: run `npm install -g playwright@1.63.0 && npx playwright install --with-deps chromium`,
then `export NODE_PATH=$(npm root -g)`. Never add a dependency to `package.json`.

The narration audio is **not** in git: `audio/scenes/` is ignored. Your checks therefore run on the **estimated
timing** (146 words per minute, 0.9 s between paragraphs, plus the holds). The real narration will move every cue
by up to a few seconds, and the French one runs 15–20 % longer. Hang everything on cue names and sentence fractions
(CONTRACT §3, §13.1) and the lead's re-check on the real timing will pass. `data/*.json` are committed. Do not run
`make data`.

## 6. Per-unit routine

For each unit of the batch, in order:

1. **Prepare.** Read the unit's script entirely and list, per scene, every cue, every on-screen number and the data
   file it comes from (CONTRACT §5). Check each claim of the `visual` against the data or the model *before* drawing
   it. If a value is missing from `data/`, write `tools/data_<unit>.py` on the pattern of `tools/data_ch04.py`: it
   reads existing files, writes `meta` with the source's SHA-256, and rewrites a file only when its content changes.
   Run it with `python3 -I tools/data_<unit>.py`, and add the file to the scene's `deps` and `entry.data`.
2. **Build** each page (CONTRACT §1–§9 and §13.1). The base layout enters at a negative `at`, so frame 0 is never
   black. Visual events lead their cue by 120–200 ms (`'cue-0.15'`). Use the kit components: badge, formula layer,
   lower-thirds, `Kit.predictCard`, `Kit.questionCard`, `Kit.seat` for PENDING scenes, and `Kit.threeModes`,
   `Kit.dial`, `Kit.photo`, `Kit.shoebox` for the E1 story. A seeded search re-run against the real cue times
   covers any timing-sensitive integration. Sound comes through `window.__EVENTS__`. Preview with `make serve`.
3. **Stills, and look at every one.**
   ```bash
   make check U=<unit>                      # estimated timing here (no narration in the clone)
   make check U=<unit> LANG=fr              # the French timing (longer): the scene must hold there too
   ```
   Read `out/check/unit_<unit>/report.json` and `out/check/unit_<unit>_fr/report.json`. Required: 0 page errors,
   no unexplained scene warning, no layout-QA issue (§13.5). Then **open every PNG**: the pre-cue still
   `<cue>-pre`, the post-cue still, the lead-in, the first and last frames. Apply the checklist of CONTRACT §11:
   cues, safe area, text size and overlap, colour key (≤ 3 key colours, the formula layer included), honesty
   badge, numbers traceable, pending seats, motion. Fix, and re-run.
4. **Draft and determinism.**
   ```bash
   node build.js --unit <unit> --draft      # out/draft/unit_<unit>/unit_<unit>_draft.mp4 (960x540, 15 fps)
   make det U=<unit>                        # exit 0: direct seeks identical, sequential = anti-aliasing only
   ```
   Extract frames in the middle of every move: `ffmpeg -ss <t> -i … -frames:v 1 x.png`. Look at them; the
   transitions are where the pilot's problems hid. Check `capture_fps` in `out/draft/unit_<unit>/scenes/*.metrics.json`
   (≥ 30 at draft size) and the performance budget of CONTRACT §8.
5. **Write the build report** at the top of `script/_review/scenes_<unit>.md`, on the model of `scenes_ch04.md`
   §0–§7: a status table, then per scene what was built, the components used, and the deviations from the `visual`
   (the same text goes into the "AS BUILT" paragraph). Add the script fields you changed, the data added, the
   findings for the writer, and kit issues (§7).
6. **Independent review by a subagent.** Start a fresh subagent that did not build the pages. Give it this brief,
   CONTRACT §11 and §13, the unit's script, the report files and stills of step 3, the draft and its mid-move
   frames. Ask it for an adversarial visual and accuracy review: every number against `data/` and the cited
   sources, every cue against the narration, every still against the checklist, transitions, determinism,
   performance. It writes its findings, each with evidence and a proposed fix, into a "## Review" section of
   `script/_review/scenes_<unit>.md`. It does not edit the pages.
7. **Fix** every confirmed finding. Mark each one fixed, or rejected with the reason. Re-run steps 3–4 on both
   timings. A unit is done only when CONTRACT §13.5 holds.
8. **Commit and push the unit** (§8). Then start the next unit.

## 7. Kit and pipeline issues

Report, never patch. In `script/_review/scenes_<unit>.md`, under a "Kit issues" heading, write one numbered item per
problem: the file and function (`runtime/components/hud.js`, `Kit.chip`), the evidence (scene, time, still path,
measurement), the impact, a proposed fix, and the workaround you used, if any. The component maintainer collects these
from every batch.

## 8. Commit-and-push protocol

Commit per unit, once its definition of done holds, and never a half-built unit. If time runs out, commit what is
finished and say so in the marker.

```bash
cd "$(git rev-parse --show-toplevel)"
git add -- video/scenes/<unit> video/script/_review/scenes_<unit>.md video/script/<unit>.json \
           [video/tools/data_<unit>.py video/data/<unit>_*.json]
git diff --cached --name-only        # every line must match the allowed paths of §3; unstage anything else
git diff --cached video/script/<unit>.json   # only file / deps / entry / visual may differ
git commit -m "Vidéo : scènes <unit> (lot <n>)"
for i in 1 2 3 4 5; do
  if git pull --rebase origin main && git push origin main; then echo pushed; break; fi
  git rebase --abort 2>/dev/null; sleep $((5 * 2 ** i))       # 10, 20, 40, 80, 160 s
done
```

- **Up to 5 attempts** with this backoff. **Never** `--force` or `--force-with-lease`, and never push to another branch.
- A rebase conflict can only come from another agent's change to a shared file, most likely `script/<unit>.json`
  (a writer may edit the narration while you build). Resolve it by taking `origin/main`'s version of the file and
  re-applying only your `file` / `deps` / `entry` / `visual` changes with a small script. Never resolve a conflict
  in a file outside §3: abort the rebase, stop, and report it in the marker.
- After 5 failed attempts: stop, keep the commit local, and write the reason in the marker (§9).

## 9. Completion marker

When the whole batch is done, or when you stop, write `script/_review/scenes_batch_<n>.done.md` and push it with the
same protocol. Push it last. Its presence tells the lead the batch is finished. Content:

- the batch number, the units, and the date;
- per unit: status `done` or `incomplete` (with the reason), the commit hash, the check results on the estimated
  and French timings (errors, warnings, QA issues), the determinism verdict, and the draft length;
- script fields changed (per scene), data files and tools added;
- the kit issues reported (unit, item number, one line each);
- the findings for the writer (narration claims that the model or the data contradict);
- anything that blocked you (push failures, missing data, ambiguous `visual`).

## 10. Unit inventory (2026-11-08)

| Unit | Scenes | Status | Level | Registers | Title |
|---|---|---|---|---|---|
| ch00 | 6 | ready | L0 | night | Cold open: the needle and the stripes |
| ch01 | 7 | ready | L0–L1 | night | A planet that makes its own magnet |
| ch02 | 7 | ready | L1 | night | Stretch, smudge, and three tanks of sodium |
| chSOA1 | 6 | ready | L1–L2 | night | A century of dynamo hunting |
| ch03 | 9 | ready | L2 | night | The equation, the windows, and the question |
| ch04 | 8 | ready | L2 | night | **built (pilot)** |
| ch05 | 6 | ready | L2–L3 | night | Counting crossings from still photographs |
| ch06 | 6 | ready | L3 | night | A machine that dreams snapshots |
| ch07 | 7 | ready | L3–L4 | night | The mirror and the crowd |
| ch08 | 8 | ready | L3–L4 | night | Fields have stricter laws |
| ch09 | 7 | ready | L4 | night | The honest scoreboard |
| chSOA2 | 9 | ready | L4–L5 | night | The map of the field: where this work fits |
| ch10 | 11 | 6 ready, 5 pending | L4–L5 | night, paper, blueprint | The climb to 3D: bets on the staircase |
| ch10q | 6 | ready | L3–L4 | night | Before we compute |
| ch11 | 3 | 2 ready, 1 pending | L5–L0 | night | Back to the compass |
| X1 | 4 | ready | L4 | night | Inside the twisting box (E3 in depth) |
| X2 | 6 | ready | L4 | paper | The proofs behind the pictures |
| X3a | 6 | ready | L4 | night, paper | Crowd laws, deeper |
| X3b | 1 | pending | L5 | night | The crowd law in 3D |
| X4a | 5 | 3 ready, 2 pending | L4–L5 | night | What snapshots can and cannot tell |
| X4b | 1 | pending | L5 | night | Steep slopes and the branch |
| X5a | 5 | 3 ready, 2 pending | L4 | night, blueprint | The factory floor |
| X5b | 3 | 2 ready, 1 pending | L5 | night, blueprint | The bill and the plan |
| X6 | 8 | 6 ready, 2 pending | L5 | night, paper | Walls, metals and meshes |

Reuse across units: the E1 story's pieces (`Kit.threeModes`, `Kit.dial`, `Kit.photo`, `Kit.shoebox`) return in 05.2,
06.4, 07.x and 09.x. The knob, needle, staircase and mirror return everywhere. A chapter starts with `Kit.chapterCard`
(at `-0.3`) and ends with its `chXX.Q` question card. Pending scenes use `Kit.seat` and vary its type (`curve`, `map`,
`lamps`, `gauge`).
