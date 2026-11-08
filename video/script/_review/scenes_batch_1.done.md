# Scene batch 1 — done (2026-11-08)

Units: ch00, ch01, ch02, chSOA1, ch03 (35 scenes), all `done` on the definition of CONTRACT §13.5 except item 8:
**no independent review pass was run** (the batch was launched with a tight token budget and an instruction to
skip it); each unit's report says so and a reviewer pass is still owed. Checks ran on the estimated (146 wpm) and
French timings; no narration audio was in the clone. No API call, no simulation, nothing written outside the
allowed paths; no data file or extractor added.

**ch00** (6 scenes, commit 6797125). Compass (Kit.needle) flip, flat reverse dive to a grey Earth with tilted dipole
lines, seafloor spreading from the script's polarity ages morphing into the strip, two questions with the E1 cloud
teaser, title with a field flip, Q1 card. Checks en/fr: 0 errors, 0 warnings, 0 QA. det 0 DIFFERENT, draft 1:28,
46-62 fps. Flat instead of WebGL for 00.1/00.2. `entry.params` of 00.4 and ch00.Q gained the 00.3 polarity ages.

**ch01** (7 scenes, db0196b). Earth cutaway with decay and age counters, bar magnet lines from a charge-sheet model
with computed in/out box counts (36/36, 26/26), bicycle / feedback / self-exciting disc shots with predict beat and
growth curves, energy loop, mirror twins, recap, Q2. en/fr: 0 errors, 0 warnings; 01.2 keeps 8 QA overlaps of a
KaTeX subscript box in the formula layer (false positive, documented). det ok, draft 3:04, 47-63 fps.

**ch02** (7 scenes, 5b9a684). Two inks with stretch brightness and diffusing ribbons in two panels, Rm equation +
schematic s(Rm), sodium pours / smudging blobs / Re-linked-to-Rm dials, the four experiment cards, VKS flat cutaway
with fig_vks field lines (shapes only), VKS flips with the corner needle and the seafloor callback, Q3. en/fr: 0/0/0.
det ok, draft 3:12, 40-65 fps. Flat instead of WebGL for 02.5; 02.1 flow time scaled by 0.4.

**chSOA1** (6 scenes, aebe46d). The shared map (`map.js`, generated verbatim from the script, and `SOA.map` in the
unit kit) with label placement, roster of supervisors' papers, Pm dial, Re gauge, MilaDy bracket, thesis ring.
en/fr: 0 errors, 0 QA; documented warnings only: "no room for the named label of <pin>" (T1958, L2006, LDRES, S2026B,
R2012, R2026, S2026C, INTERN, THESIS) — the map is too dense at 28 px for every keep_named label (finding for the map
designer). det 0 DIFFERENT, draft 2:35, 61-67 fps.

**ch03** (9 scenes, 760451f). Induction equation with looping picture panels, conveyor belt and plateau, ABC flow
(Canvas projection, not WebGL), E3 s(Rm) with windows and mode insets from data, panel of knobs with the wall switch,
handful of dots, the study's questions and the staircase, checkpoint dials, Q5 card. en/fr: 0 errors, 0 warnings,
1 QA item in 03.1 (KaTeX fraction box, false positive). det 0 DIFFERENT, draft 4:24, 44-73 fps.

**Script fields changed**: `visual` (an AS BUILT paragraph) on all 35 scenes; `entry.params` of 00.4 and ch00.Q.
No `deps` changes. Narration untouched.

**Kit issues reported** (details in each `scenes_<unit>.md`):
ch00 #1 Kit.needle start angle · #2 Kit.cloud Float32Array doc · #3 reference lower-third wraps (one-line rule).
ch01 #1 Kit.mirror plane without arrows · #2 Kit.predictCard multiple picks · #3 bar-magnet field helper · #4 fitFormula split after "=".
ch02 #1 Kit.twoInks (stretch brightness, diffusion, time scale, 6000-point cap) · #2 question-only predict card · #3 knob value(t).
chSOA1 #1 promote SOA.map to Kit.map (chSOA2 needs it) · #2 chip anchors 'tc'/'bc'.
ch03 #1 equation term element for pen targets · #2 formula layer paging for long statements (6 items) · #3 knob labels/value(t).

**Findings for the writer**: ch03 — e3_growth.json mislabels series[0] ("whole run" vs "second half", R:1066);
several onscreen formulas are too long for the formula layer at 28 px (03.2, 03.3, 03.4, 03.5, 03.6; shown in two
parts as a workaround). chSOA1 — keep_named lists exceed what the map can hold at 28 px.

**Blockers**: none (all five pushes succeeded on the first attempt).
