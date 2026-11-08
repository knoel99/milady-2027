# Chaptered outline: How Often Does the Field Flip?

*Teaching generative models the physics of dynamos, from a compass to the research frontier.* Long English explainer about the MilaDy 2027 site. Outline version 2026-11-08 (v2, after review), generated from `outline_src/outline_data.py` by `outline_src/build_outline.py` (the same data as `outline.json`). This version applies the accuracy review (`critique_accuracy.md`) and the pedagogy and production review (`critique_pedagogy.md`); every change is listed in section 9 and version 1 is kept in `outline_src/v1/`. Sources: `inventory.md`, `pedagogy.md`, `styles.md`, `pipeline.md` and the site under `/home/user/milady-2027/en/`. Source references use the inventory's abbreviations (R report, T thesis proposal, S supervisors, C computing, H home, P3/P4 prep modules 3/4, D digest, X experiments page, IR infra README, CFG configs). Ids: chapters ch00-ch11, core scenes NN.k, extension scenes X…; each scene shows its version-1 id ('was').

## 0. At a glance

| Cut | Units | Duration now | With all results | Scenes | READY | PROVISIONAL | PENDING | Render estimate, 1080p30, 4 cores |
|---|---|---|---|---|---|---|---|---|
| Core cut | ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11 | **40:55** | 41:35 | 73 | 68 | 3 | 2 | 1.34 h |
| Extension modules | X2, X3a, X4a, X5a, X1, X4b, X3b, X6, X5b | **19:15** | 20:20 | 32 | 23 | 4 | 5 | 0.47 h |
| Extended cut (core + modules; 10.8 skipped, 10.9 as bridge) | see section 3 | **59:15** | 60:45 | 104 | 90 | 7 | 7 | 1.8 h |

Two-episode option: Part 1 = ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07 (25:21, L0 to L4); Part 2 = 60-s recap + ch08, ch09, ch10, ch11 + all modules (34:54; 16:34 without modules). Part 2 opens on a 60-s 'previously' scene (needle, shoebox, Rice, violet cloud, lopsided machine, mirror) (I6); ch07 (the mirror) closes Part 1 with its cliffhanger and payoff. Part 2 carries all extension modules.

Results update episode (when the HPC results arrive): 7:05 with every result in. Stand-alone 'Results update' episode (H1): a 45-s recap of 10.1, then the regenerable scenes in their result variants, then 11.1. Scenes whose data are still missing are dropped from the episode, not shown empty. The full film is re-published as v2 on the site and the GitHub release, with a pinned link from the original upload.

Time per level (as shipped now):

| Cut | L0 | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|---|
| Core | 3:34 | 4:57 | 9:07 | 9:52 | 10:10 | 3:15 |
| Extended | 3:34 | 4:57 | 9:07 | 9:52 | 21:35 | 10:10 |

Render estimates use the measured throughput per scene class (flat 44 fps, dense 2D 7.5 fps, WebGL 4.1 fps) and exclude narration and assembly (a few minutes). Durations are targets; final durations come from the narration audio.

## 1. Logline and synopsis

**Logline.** No one can yet say when Earth's magnetic field will flip next, but in the dynamos we can compute, we can learn how often. One film climbs from a compass to the frontier of physics-constrained generative AI for dynamos.

**Synopsis.** It opens on a compass needle that flips and on the striped seafloor, then builds the physics picture by picture: stretch versus smudge, thresholds, and a liquid-sodium experiment, VKS, that flips like the Earth. Chaos hides the date of the next flip, yet a shuffled box of snapshots, plus the equations, still holds the crossing rate, through Rice's formula. Generative models then learn to dream such snapshots between the knob settings that were simulated. At its heart is one lesson from an independent, prospective internship study around the MilaDy project: enforce each law where it is true, exactly for every field, or on average for the crowd. Small CPU experiments show what works and what fails. It ends on written bets for 3D dynamos, VKS and DRESDYN, filled in as simulations arrive.

(171 words.)

## 2. Conventions

- **Levels.** L0: anyone; L1: curious high school / early undergraduate; L2: science undergraduate; L3: M1 physics or ML; L4: M2 / early PhD; L5: supervisors and specialists. An altitude rail on the left edge shows the level at chapter cards and checkpoints only (3 s). The climb only goes up, except in the closing; the one declared side-step is the ch08 chapter card ('new test bench', L4 -> L3). Extension modules are asides: the rail marks them and returns.
- **Status.** **READY**: all data exist, or are computed at build time with no external run (repository results, site assets, live integrations, random-weight decoder); **PROVISIONAL**: a reduced or CPU run can produce the data now; replaced later by the HPC result; **PENDING**: needs HPC, GPU or consortium results; ships now as an 'empty seat' (READY anchor + bet + criterion).
- **Durations.** duration_s = as shipped now (pending variant / provisional data); duration_result_s = with final data; targets assume about 130 effective words per minute (speech at about 150 + visual breathing room).
- **Pending device.** Each PENDING scene is an *empty seat*: READY anchor visual, dashed chart frame, labelled axes, shaded success band, data tag; two narration variants (pending / result); vary the frame type (curve, map, lamp panel, gauge). It is shippable. The hatched AWAITING preview of the pipeline is for drafts only.
- **Formula layer.** Exact values and statements that the ladder does not allow in narration sit on a separate formula layer (small type, never in subtitles, never narrated) (decision D8).
- **Colour key (NIGHT values).** green `#1BAF7A` control parameter, blue `#3987E5` velocity u, vermillion `#EB6834` magnetic field B, violet `#B49CF0` generative model, amber `#EDA100` distribution-level metrics, grey `#6B7A8C` infrastructure. On PAPER: the site values `#009E73`, `#0072B2`, `#D55E00`, `#6C4BA0`, `#E69F00`. Matter is grey. Polarity is a shade of vermillion, never a new hue.
- **Paths.** Assets and data are relative to `/home/user/milady-2027` (read-only) unless they start with `proto/` (`video`) or `data/` (scene data files written by `tools/extract_data.py` into `video/data`).
- **Run environment for every regeneration run.** In a clone of the repository on the compute machine (never in /home/user/milady-2027 here): export MILADY_DB_URL=sqlite:///$RUNS/catalog.sqlite MILADY_STORAGE_URI=$RUNS/store MILADY_SWEEP_DIR=$RUNS/sweeps MILADY_MODELS_URI=$RUNS/models (check the accepted URI forms with --dry-run first); then copy the outputs or the catalog dump next to the film project and run `python3 -I tools/extract_data.py` (writes data/*.json; unchanged content does not re-render).
- **Motifs** (M1 needle and flip, M2 knob, M3 two inks, M4 violet cloud, M5 amber histogram, M6 projector, M7 staircase, M8 altitude rail, M9 pen, M10 mirror) and transitions (T1 morph, T2 scale dive, T3 ink change, T4 chapter card, T5 hard cut, T6 equation morph) follow `styles.md` §3.5-3.6. Every chapter opens with T4. The corner needle (M1) shows only while the dipole D is on screen. Recurring devices: the two shelves (07.1 -> 08.6), the shoebox (04.6 -> 06.4), the toll counter (05.1 -> 09.1), the three promise cards (03.7 -> 05.3, 08.6, 09.1).
- **Symbol sheet** (one meaning per mark; lint the script against it):
  - s: growth rate of the field (real part); never lambda (D1)
  - lambda: a generic knob, always green; name the specific knob whenever there is one (Gamma, eta, Rm, Re, Pm, Po)
  - D: the dipole, everywhere; eps: dissipation (never sigma(D) for its spread: sigma(eps)) (D4)
  - r_0: rate of zero crossings of D; r: reversal rate; r_a: rate of crossings of +/- a (Rice, D3)
  - Gissinger coefficients: numbers only (0.119, 0.1), no mu or nu on screen (D3)
  - q: generated law; q*: tilted law (never nu*) (D3)
  - mu_Gamma, mu_+/-: stationary laws, only in X2 and X4; in the core, 'the long-exposure glow (stationary distribution)' (B5)
  - mu_r: 'iron (permeability)' in words until L5 (D3)
  - 'distribution distance' (amber) on screen and in narration; 'energy distance' only as a technical chip in 06.5 and in X3.0 (D2)
  - 'crossing rate' on screen; 'how often it flips (counted as crossings)' in the closing (D5)
  - t: transport time of the generator in [0, 1]; v_theta: generator velocity (violet); u: fluid velocity (blue) (06.2)
  - C1-C4: the report's constraint classes, on screen only in the formal row of 08.6; chapter ids are ch00-ch11 (D6)
  - Lip(phi): Lipschitz constant (never L, which is the generator of the dynamics) (B6)

## 3. Running order

Extended cut, segment by segment. Rows marked *core* make up the core cut on their own (in the core cut, 10.8 plays and 10.9 runs at full length).

| # | Segment | Cut | Title | Levels | Duration (extended) | Takeaway |
|---|---|---|---|---|---|---|
| 1 | ch00 | core | Cold open: the needle and the stripes | L0 | 1:14 | The field has flipped many times, with no schedule; we can ask when, and we can ask how often. |
| 2 | ch01 | core | A planet that makes its own magnet | L0-L1 | 2:47 | A moving conducting fluid can turn a tiny field into a large one once its loop gain passes a threshold, and the laws do not prefer north or south. |
| 3 | ch02 | core | Stretch, smudge, and three tanks of sodium | L1 | 3:05 | A flow amplifies a field when stretching beats smudging; only three sodium experiments got there, and one of them, VKS, flips like the Earth. |
| 4 | ch03 | core | The equation, the windows, and the question | L2 | 4:22 | A dynamo can switch on, off and on again, real dynamos depend on many knobs, and simulations cover only a handful of settings: we need something that fills the gaps, and respects the physics. |
| 5 | ch04 | core | Chaos and the shoebox of photographs | L2 | 4:05 | The date of the next flip is unknowable, but the cloud of states is stable, and some laws hold only for the cloud. |
| 6 | ch05 | core | Counting crossings from still photographs | L2-L3 | 2:40 | A shoebox of snapshots plus the equations gives the crossing rate without running time forward. |
| 7 | ch06 | core | A machine that dreams snapshots | L3 | 3:05 | A generative model learns a wind that carries noise to data, one model for every knob setting, judged against the noise floor. |
| 8 | ch07 | core | The mirror and the crowd | L3-L4 | 4:03 | Build the mirror into the machine, impose crowd laws on the crowd, and never force a crowd law onto each snapshot. |
| 9 | ch08 | core | Fields have stricter laws | L3-L4 | 4:49 | Enforce each law at the level where it is true: build per-snapshot laws into every output, impose crowd laws on the crowd. |
| 10 | X2 | ext. (after 08.7) | The proofs behind the pictures | L4 | 3:30 | Each picture of ch07-ch08 is backed by an elementary statement with a precise scope, often known in other forms. |
| 11 | X3a | ext. (after X2) | Crowd laws, deeper | L4 | 2:50 | Reweighting cannot visit places the model never went. |
| 12 | ch09 | core | The honest scoreboard | L4 | 4:00 | On a toy model the crossing rate is predicted from generated snapshots and the model's equations, without running time forward: roughly right far from the threshold and poorly near it, as expected from a generator that varies smoothly with the knob. |
| 13 | X4a | ext. (after 09.6) | What snapshots can and cannot tell | L4-L5 | 2:25 | A snapshot generator bounds and estimates rates, but waiting times need the dynamics; tier 0 needs more seeds and a joint mirror. |
| 14 | ch10 (10.1-10.3) | core | The climb to 3D: bets on the staircase | L4-L5 | 1:25 | Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the data exist, with the criterion that will settle it. |
| 15 | X5a | ext. (after 10.3) | The factory floor | L4 | 2:30 | Reproducibility is designed in: every number on screen traces back to a file, a commit and a catalog row. |
| 16 | X1 | ext. (after X5a) | Inside the twisting box (E3 in depth) | L4 | 1:55 | The 3D test bench passes an exact check and recovers the known windows, with honest limits on precision. |
| 17 | ch10 (10.4-10.5) | core | The climb to 3D: bets on the staircase | L4-L5 | 1:20 | Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the data exist, with the criterion that will settle it. |
| 18 | X4b | ext. (after 10.5) | Steep slopes and the branch | L5 | 0:25 | Near a subcritical threshold, conditioning on the branch could remove the smoothing error; it is a bet. |
| 19 | ch10 (10.6-10.7) | core | The climb to 3D: bets on the staircase | L4-L5 | 0:50 | Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the data exist, with the criterion that will settle it. |
| 20 | X3b | ext. (after 10.7) | The crowd law in 3D | L5 | 0:25 | The crowd loss must be tested again in 3D, against a control run, without narrowing the dissipation. |
| 21 | ch10 (10.9-bridge) | core | The climb to 3D: bets on the staircase | L4-L5 | 0:15 | Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the data exist, with the criterion that will settle it. |
| 22 | X6 | ext. (after 10.9) | Walls, metals and meshes | L5 | 4:00 | Leaving the periodic box changes what 'exact' means, and the real tests (VKS, DRESDYN) are written down as bets. |
| 23 | X5b | ext. (after X6) | The bill and the plan | L5 | 1:15 | The bill is estimated with at least a factor-two uncertainty, and every estimate will be replaced by a measured number. |
| 24 | ch11 | core | Back to the compass | L5-L0 | 2:00 | We cannot say when the needle will turn, but we are learning to answer how often, by enforcing each law where it is true. |

Core chapters on their own:

| Id | Chapter | Levels | Duration now | With results | Scenes | R / P / N | Was |
|---|---|---|---|---|---|---|---|
| ch00 | Cold open: the needle and the stripes | L0 | 1:14 | 1:14 | 5 | 5 / 0 / 0 | C0 |
| ch01 | A planet that makes its own magnet | L0-L1 | 2:47 | 2:47 | 6 | 6 / 0 / 0 | C1 |
| ch02 | Stretch, smudge, and three tanks of sodium | L1 | 3:05 | 3:05 | 6 | 6 / 0 / 0 | C2.1-C2.2 + C3.1-C3.4 |
| ch03 | The equation, the windows, and the question | L2 | 4:22 | 4:22 | 8 | 8 / 0 / 0 | C2.3-C2.6 + C3.5-C3.9 |
| ch04 | Chaos and the shoebox of photographs | L2 | 4:05 | 4:05 | 7 | 7 / 0 / 0 | C4 |
| ch05 | Counting crossings from still photographs | L2-L3 | 2:40 | 2:40 | 5 | 5 / 0 / 0 | C5 |
| ch06 | A machine that dreams snapshots | L3 | 3:05 | 3:05 | 5 | 5 / 0 / 0 | C6.1-C6.5 |
| ch07 | The mirror and the crowd | L3-L4 | 4:03 | 4:03 | 6 | 6 / 0 / 0 | C6.6 + C7.5-C7.8 (E1 half of C7) |
| ch08 | Fields have stricter laws | L3-L4 | 4:49 | 4:49 | 7 | 7 / 0 / 0 | C7.1-C7.4 + C7.9-C7.10 + new (E2 half of C7) |
| ch09 | The honest scoreboard | L4 | 4:00 | 4:00 | 6 | 6 / 0 / 0 | C8 |
| ch10 | The climb to 3D: bets on the staircase | L4-L5 | 4:45 | 5:25 | 9 | 4 / 3 / 2 | C9 |
| ch11 | Back to the compass | L5-L0 | 2:00 | 2:00 | 3 | 3 / 0 / 0 | C10 |

Predict beats in film order: Q1 (01.3), Q2 (01.5), Q3 (03.4), Q4 (04.4), Q5 (07.2), Q6 (07.5), Q7 (08.2), Q8 (09.2).

## 4. Narration drafts: the first and the last minute

Written for TTS (Fish Audio drama-3, temperature 0.1, prosody.speed 1.0, one acting cue at the start, [long pause] only between paragraphs; predict holds via hold_after (production notes)). Short sentences; `[long pause]` only between paragraphs.

### Opening (scenes 00.1, 00.2, 00.3, 00.4)

146 words, 2 long pauses: about 61.4 s at 150 words per minute, 70.4 s at 130 effective words per minute.

```text
[calm, natural narrator voice] This needle has pointed north your whole life. Rocks on the ocean floor say it has pointed south too. Again and again, with no schedule. [long pause]

That needle follows a field that wraps the whole planet. It feels permanent. It is not. Along the ridges of the ocean floor, fresh lava cools, and tiny magnetic grains freeze in place, each remembering which way a compass pointed. As the seafloor spreads, they line up into stripes of very uneven widths. [long pause]

So, two questions. When will it flip next? And how often does it flip? In the dynamos we can compute, the first question turns out to be hopeless. The second one is not. Finding out why takes us from this needle to liquid metal, to chaos, and to machines that dream up magnetic fields, and must learn where physics is exact, and where it only holds on average.
```

Cue map: "This needle has pointed" → 00.1 (needle flips on 'pointed south too'); "That needle follows" → 00.2; "Along the ridges" → 00.3; "So, two questions" → 00.4 (violet teaser on 'machines that dream').

Note: The reversal lands at about 7 s and the two questions at about 0:34 (A1). Per-scene word budgets now match the cue map at about 135 words per minute (A2): about 25 / 16 / 36 / 68 words for 11 / 7 / 16 / 30 s. The seafloor sentences rely on an external fact (decision D7). Site-only alternative for 00.3: 'In a tank of liquid sodium in Cadarache, the field flips too.'

### Closing (scenes 11.2)

155 words, 3 long pauses: about 66.5 s at 150 words per minute, 76.0 s at 130 effective words per minute.

```text
[calm, natural narrator voice] Back to the compass in your hand. [long pause]

We still cannot tell you when this needle will turn around. In the dynamos we can compute, chaos erases the memory of the present too fast. But those dynamos do answer another question: how often. That answer hides in a cloud of snapshots, and a machine can learn to draw such clouds, even between the settings that were simulated. [long pause]

On small test problems, it partly works. The mirror symmetry holds by construction. On a three-variable model, the rate at which the dipole crosses zero comes out roughly right far from the tipping point, and poorly right at it, because a smooth machine cannot follow a steep change. The real tests, in three dimensions and in liquid metal, are still ahead. You have seen the bets. [long pause]

One lesson remains. Enforce each law where it is true. Exactly, where it is exact. On average, where it only holds on average.
```

Results-in variant: Paragraph 3, used when timeline.json marks at least one of 10.4, 10.5 or 10.7 as final: 'On small test problems, it partly works. The mirror symmetry holds by construction. On a three-variable model, the rate at which the dipole crosses zero comes out roughly right far from the tipping point, and poorly right at it. In three dimensions, the first bets are now settled: {bets_met} of {bets_total} criteria met. The tests in liquid metal are still ahead.'

Cue map: "Back to the compass" → 11.2 compass; "We still cannot" → montage: barcode, whirlpools, shoebox; "On small test problems" → montage: mirror, histogram; E1 numbers as chips; "One lesson remains" → clean compass, three-line lesson.

Note: Numbers are on chips, not spoken (J); the narration says 'crosses zero' (B16) and follows pitfall P15. 'Holds by construction' refers to Proposition 4. Paragraph 3 has two variants keyed to timeline.json (H2).

## 5. Core cut: chapters and scenes

### ch00. Cold open: the needle and the stripes

`L0` · 1:14 · was C0 · 5 scenes: 5 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Feel that Earth's field is not permanent: it has flipped many times, irregularly.
- **Takeaway (one sentence).** The field has flipped many times, with no schedule; we can ask when, and we can ask how often.

#### 00.1 A needle that flips  
`L0` · 11 s · **READY** · NIGHT · render webgl · was C0.1

- **Key idea.** This needle has pointed north your whole life; the rocks say it has pointed south too, again and again.
- **Visual.** Stylized 3D compass in macro, no hand (G3). The vermillion needle tip swings and settles north; at about 7 s it swings round to south, holds, and settles back north. The polarity needle (M1) is born here; later it appears as a small corner needle only in scenes where the dipole D is on screen (E7).
- **On screen.** chip 'illustration, not to time scale'
- **Motifs.** M1 polarity needle (first)
- **Assets.** none (new animation)
- **Data.** none

#### 00.2 Pull back to the planet  
`L0` · 7 s · **READY** · NIGHT · render flat · was C0.2

- **Key idea.** The needle follows a field that wraps the whole planet. It feels permanent. It is not.
- **Visual.** 'Powers of Ten' zoom made of flat layered illustrations cross-faded on scale (compass, room, landscape), ending on a grey sphere where vermillion dipole field lines bloom from pole to pole. Only the last 3 s are WebGL, rendered as a separate shot (G4). The narration describes what is on screen (A3).
- **On screen.** chip SCHEMATIC
- **Motifs.** T2 scale dive
- **Assets.** none (new animation)
- **Data.** none

#### 00.3 The seafloor tape recorder  
`L0` · 16 s · **READY** · NIGHT · render flat · was C0.3 + C0.4

- **Key idea.** Cooling lava freezes the field's direction; the spreading seafloor records it as stripes of uneven width: the flips are irregular.
- **Visual.** Cross-section of a mid-ocean ridge: magma rises and cools, short grain segments align with the field and freeze, the floor slides away on two conveyor belts. Stripes accumulate mirror-symmetrically as a true barcode: solid vermillion = normal, near-background = reversed, labels kept (A5). The camera tilts down on the barcode, whose widths are visibly irregular; it slides left and becomes the polarity strip under a thin D(t) trace (T1 morph).
- **On screen.** labels 'normal' / 'reversed'; 'every few hundred thousand years, irregularly' (no powers of ten at L0); chip SCHEMATIC; reference chip (to be sourced)
- **Motifs.** M1 barcode / polarity strip, T1 morph
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** EXTERNAL_FACT: seafloor magnetic stripes (Vine and Matthews 1963), source before use (decision D7)
- **Sources.** P3:1230 (Rincon 2019: irregular, 1e5 to 1e6 years)

#### 00.4 Two questions  
`L0` · 30 s · **READY** · NIGHT · render flat · was C0.5

- **Key idea.** When will it flip next? How often does it flip? In the dynamos we can compute, the first is hopeless and the second is not.
- **Visual.** Two cards: 'When will it flip next?' with a grey clock, 'How often does it flip?' with amber tally marks. The clock card's border turns dashed and dims; the tally card stays lit. On the words 'machines that dream up magnetic fields', a 3-s teaser of the violet cloud (M4), the film's second protagonist (A6).
- **On screen.** the two questions; violet-cloud teaser
- **Motifs.** M4 violet cloud (teaser)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** P4:1627 (when vs how often, shown for the three-mode model)

#### 00.5 Title  
`L0` · 10 s · **READY** · NIGHT · render flat · was C0.6

- **Key idea.** Title card.
- **Visual.** Title words sit in a vermillion field-line field; the dipole flips and the lines reorganise around the letters; one soft impact sound (SFX event, G2).
- **On screen.** working title (decision D13)
- **Motifs.** M1 flip
- **Assets.** none (new animation)
- **Data.** none

### ch01. A planet that makes its own magnet

`L0-L1` · 2:47 · was C1 · 6 scenes: 6 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Understand that the field must be regenerated by moving liquid metal, that a dynamo is a self-amplifying loop with a threshold, and that physics prefers neither polarity.
- **Takeaway (one sentence).** A moving conducting fluid can turn a tiny field into a large one once its loop gain passes a threshold, and the laws do not prefer north or south.

#### 01.1 No magnet inside  
`L0` · 25 s · **READY** · NIGHT · render dense2d · was C1.1

- **Key idea.** Left alone, a field in Earth's core would fade within some ten thousand years; the field is billions of years old, so moving liquid iron must keep regenerating it.
- **Visual.** Flat Earth cutaway in grey shells (solid inner core, liquid outer core). A 'left alone' timer makes a field fade in about 10^4 years while a geological clock runs on to billions of years. Then the outer core starts to churn, drawn as a Canvas 2D advected texture (G5: no full-screen shader). Grey matter, no colour until fields appear.
- **On screen.** 'liquid iron outer core'; 'a field left alone fades in about 10,000 years' vs 'the field is billions of years old'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** P3:269 (Tobias 2021), P3:1471, R:86

#### 01.2 Lines never end  
`L0` · 30 s · **READY** · NIGHT · render dense2d · was C1.2

- **Key idea.** Cut a magnet in half and you get two magnets, never a lone north pole: field lines never start or stop, so through any box as many lines enter as leave.
- **Visual.** Surprise first (C5): a bar magnet is sawn in half and each half has both poles. Then iron filings morph into vermillion field lines; a dashed box is dragged around the picture; two counters 'in' and 'out' always agree. Planted for div B = 0 (payoff in 08.2-08.3).
- **On screen.** 'lines in = lines out' (no symbol yet)
- **Motifs.** the box (callback in 08.2 and 08.3)
- **Assets.** `prep/p1-calcul-vectoriel/fig-monopole-dipole-en.png`
- **Data.** none

#### 01.3 The squeal  
`L1` · 55 s · **READY** · NIGHT · render flat · was C1.3

- **Key idea.** A loop whose gain per turn exceeds one grows from almost nothing, then saturates.
- **Visual.** Opens on a bicycle dynamo: motion makes electricity, with a magnet built in; the Earth must make its own magnet (J). A microphone pointed at its own speaker: whisper, then squeal past a green gain knob (M2); the squeal sits in a narration gap (SFX event, G2). Morph into a self-exciting disc: grey copper disc, coil, current arrows; below the threshold the seed dies, above it the field grows turn after turn, then reaches a plateau (the field brakes the disc). A staircase of bars 'each turn: B x (gain / loss)' smooths into the curve e^(s t) (B8).
- **On screen.** Predict Q1 with a 3-s hold; after the reveal: 'each turn: B x (gain / loss)', then 'B grows like e^(s t)', s = growth rate (D1)
- **Predict beat.** Q1: spin a little faster each time: does the field grow a little each time, or nothing until a certain speed? (Answer: nothing, then exponential growth, then saturation.)
- **Motifs.** M2 knob (first), squeal / loop gain
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** EXTERNAL_FACT: self-exciting homopolar disc (Bullard 1955), source before use (decision D7)

#### 01.4 Who pays the bill  
`L1` · 20 s · **READY** · NIGHT · render flat · was C1.4

- **Key idea.** A dynamo converts mechanical power into magnetic energy and heat; it creates no energy.
- **Visual.** Loop diagram: motor power -> flow (blue) -> field (vermillion) by induction -> 'the field brakes the flow' -> heat (grey). Forces and losses are named in words only (J).
- **On screen.** loop labels in words
- **Assets.** `en/prep/p3-mhd-dynamo/index.qmd`
- **Data.** none
- **Sources.** en/prep/p3 ch. 5 loop diagram (inline SVG, redraw in palette)

#### 01.5 Which way is up?  
`L1` · 25 s · **READY** · NIGHT · render flat · was C1.5

- **Key idea.** The equations are unchanged under B -> -B: both polarities are equally lawful; which one you get is history.
- **Visual.** Predict card; then a vertical mirror plane (M10) appears; the Earth's field and its mirror twin side by side; the needle flips.
- **On screen.** Predict Q2; then 'B -> -B: same equations'
- **Predict beat.** Q2: physics does not care whether the field points north or south. Which polarity should Earth prefer? (Answer: neither.)
- **Motifs.** M10 mirror (first)
- **Assets.** none (new animation)
- **Data.** none

#### 01.6 Checkpoint: the big picture  
`L1` · 12 s · **READY** · NIGHT · render flat · was C1.6

- **Key idea.** Recap, then the next question: what kind of motion can do this, and how fast must it be?
- **Visual.** Recap with motifs only (needle, barcode, squeal); the altitude rail (M8, left edge) shows for 3 s and climbs one notch. Ends on the open question, not on an exit ramp (E8).
- **On screen.** 'Level 0 -> Level 1'; the open question
- **Motifs.** M8 rail
- **Assets.** none (new animation)
- **Data.** none

### ch02. Stretch, smudge, and three tanks of sodium

`L1` · 3:05 · was C2.1-C2.2 + C3.1-C3.4 · 6 scenes: 6 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** See a dynamo as a race between stretching and smudging measured by Rm, understand why liquid-sodium dynamos are hard and turbulent, and meet the three that worked, including VKS, which flips.
- **Takeaway (one sentence).** A flow amplifies a field when stretching beats smudging; only three sodium experiments got there, and one of them, VKS, flips like the Earth.

#### 02.1 Frozen threads  
`L1` · 35 s · **READY** · NIGHT · render dense2d · was C2.1

- **Key idea.** A conducting flow drags field lines; stretching a line strengthens the field; diffusion smudges it, faster in a poorer conductor.
- **Visual.** Blue tracer particles stretch and fold a vermillion material line (brightness follows stretch). Split screen with the same flow on both sides: slow-smudging ink (good conductor, small diffusivity: threads stay sharp) vs fast-smudging ink (poor conductor, large diffusivity: a grey blur wins). No viscosity metaphor (B5, J).
- **On screen.** 'stretching' / 'diffusion'; split labels 'small diffusivity' / 'large diffusivity'
- **Motifs.** M3 two inks
- **Assets.** `prep/p3-mhd-dynamo/figures/expulsion-en.svg`, `proto/scenes/a_fieldlines.html`
- **Data.** `proto/data/fieldlines.json`

#### 02.2 One number for the race  
`L1` · 30 s · **READY** · NIGHT · render flat · was C2.2

- **Key idea.** Rm = UL/eta compares stretching with smudging; the growth rate s crosses zero at a threshold Rm_c.
- **Visual.** Green Rm knob turns; a schematic growth-rate curve s(Rm) rises through zero; the zero crossing is marked as the threshold Rm_c.
- **On screen.** Rm = U L / eta (U blue, eta green); s = growth rate; chip SCHEMATIC
- **Motifs.** M2 knob
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** en/prep/p3 ch. 2

#### 02.3 The sodium problem  
`L1` · 30 s · **READY** · NIGHT · render flat · was C3.1

- **Key idea.** Liquid sodium is as runny as water but smudges fields fast (Pm = nu/eta about 1e-5): reaching Rm of 10 to 50 means stirring so hard that the flow is violently turbulent.
- **Visual.** Two gauges: Rm (green) climbs slowly while Re (blue) races to millions; a turbulent texture fills the background. Level lowered to L1: one ratio, no exponents in the narration.
- **On screen.** Pm = nu / eta ~ 1e-5; 'Rm ~ 10-50 needs Re ~ millions'; formula layer: Re ~ 1e6-1e7
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** P3:281, R:137, en/prep/p3 Ex. 1.6

#### 02.4 Three tanks that worked  
`L1` · 30 s · **READY** · NIGHT · render flat · was C3.2

- **Key idea.** Only three liquid-sodium experiments have produced a dynamo, each with a different field, and only one of them flips; DRESDYN is trying with precession.
- **Visual.** Horizontal timeline cards (one moment per card): Riga (helical flow; an oscillating, rotating field), Karlsruhe (52 vortex generators; a steady dipole), Cadarache VKS (150 litres of sodium, motors up to 300 kW; a dipole that can flip); a fourth card, dashed: DRESDYN, under way.
- **On screen.** names and one plain line each; 'first dynamo: 1999' for Riga and Karlsruhe (R:139)
- **Assets.** `prep/p3-mhd-dynamo/figures/vks-en.svg`
- **Data.** none
- **Sources.** R:139, P3:1149, S:72, R:86

#### 02.5 VKS: two impellers and an iron surprise  
`L1` · 35 s · **READY** · NIGHT · render webgl · was C3.3

- **Key idea.** Counter-rotating impellers stir liquid sodium; the dynamo appeared only with soft-iron impellers.
- **Visual.** 3D cutaway of the cylinder (grey matter), two bladed impellers counter-rotating, blue flow cells and recirculation; the impeller material is swapped steel -> soft iron: only then does a vermillion axial dipole grow.
- **On screen.** chip SCHEMATIC geometry; 'stainless steel: no dynamo' / 'soft iron: dynamo'
- **Motifs.** matter grey, fields coloured
- **Assets.** `figures/vks/figure/out/vks-en.svg`, `prep/p3-mhd-dynamo/figures/vks-en.svg`
- **Data.** none
- **Sources.** R:139, R:90, T:138

#### 02.6 VKS flips too  
`L1` · 25 s · **READY** · NIGHT · render flat · was C3.4

- **Key idea.** With impellers at different speeds, the lab dynamo reverses irregularly, like the Earth, every minute or two.
- **Visual.** Qualitative D(t) with reversals (VKS figure, panel b) over the barcode strip; the corner needle (M1) is shown because D is on screen, and flips in sync. This re-hooks the cold open at about 6 min (B2). The measured numbers sit on a separate card, not on the qualitative curve (C6).
- **On screen.** 'flips every minute or two, irregularly'; separate card '16 Hz vs 22 Hz: polarities last 120 s and 50 s on average; a reversal takes about 5 s' (Berhanu et al. 2007); curve chip 'qualitative (normal form): durations are not those of VKS'
- **Motifs.** barcode, M1 flip, callback: cold open
- **Assets.** `figures/vks/figure/out/vks-en.svg`
- **Data.** none
- **Sources.** R:149, R:163, P3:1166

### ch03. The equation, the windows, and the question

`L2` · 4:22 · was C2.3-C2.6 + C3.5-C3.9 · 8 scenes: 8 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Read the induction equation as the race in symbols; know kinematic vs dynamic and the ABC dynamo windows; see that the knob is a panel of knobs, that simulations are too costly to cover it, and what this film asks.
- **Takeaway (one sentence).** A dynamo can switch on, off and on again, real dynamos depend on many knobs, and simulations cover only a handful of settings: we need something that fills the gaps, and respects the physics.

#### 03.1 The induction equation, term by term  
`L2` · 40 s · **READY** · NIGHT · render flat · was C2.3

- **Key idea.** The whole race in one equation.
- **Visual.** Equation built with the 10-step protocol: terms light in narrative order, leader lines to a stretched thread ('carried and stretched by the flow', C1) and a fading thread ('diffusion'); pen beats (M9) circle each term.
- **On screen.** dB/dt = curl(u x B) + eta Laplacian(B); braces 'carried and stretched by the flow', 'diffusion'
- **Motifs.** M9 pen
- **Assets.** `proto/scenes/b_induction.html`
- **Data.** none
- **Sources.** P3:254

#### 03.2 A conveyor belt that does not feel its cargo  
`L2` · 32 s · **READY** · NIGHT · render flat · was C2.4

- **Key idea.** Kinematic dynamo: the flow is imposed and the field grows exponentially (an eigenvalue problem). Dynamic: the field pushes back on the flow and saturates.
- **Visual.** Log plot of |B|(t): a straight line of slope s (kinematic), then the same curve bending into a plateau when the field pushes back on the flow (dynamic). One idea only: no Lorentz-force symbol and no anti-dynamo chip here (F2, E6).
- **On screen.** 'kinematic: B = e^(s t) B_hat, s = real growth rate (modes may also oscillate)'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:240, en/prep/p3 §5.2, R:1114 (oscillating modes)

#### 03.3 Twisting rooms: the ABC flow  
`L2` · 25 s · **READY** · NIGHT · render webgl · was C2.5

- **Key idea.** To test our tools we need a flow simple enough to write on one line, yet able to make a dynamo: the ABC flow, whose streamlines are corkscrews (velocity parallel to its curl).
- **Visual.** The motivating line first (C3). A periodic box of fat blue corkscrew streamlines (Three.js Line2), slow orbit, long lens. The box glows for a moment on the faint staircase map (M7, tier-2 preview, E1).
- **On screen.** u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x);  curl u = u
- **Motifs.** M7 staircase (tier-2 preview)
- **Assets.** `proto/scenes/c_abc3d.html`
- **Data.** none
- **Sources.** R:1063

#### 03.4 Predict: once on, always on?  
`L2` · 45 s · **READY** · NIGHT · render flat · was C2.6

- **Key idea.** Dynamo windows: the ABC dynamo switches on near Rm 9, off near 17.5, on again above about 27.
- **Visual.** Predict card; then s(Rm) drawn live, left to right, from E3 (24 points); windows shaded green at 12%; inset z = 0 slices of |B| of the dominant mode (least damped or fastest growing) at Rm 8, 12, 16 and 20: below, inside and just after the first window (B7). The 48^3 check markers move to X1.3 (F3).
- **On screen.** thresholds 'about 9 · 17.5 · 27'; formula layer: 8.87 / 17.6 / 26.8 (32^3) vs published 8.9 / 17.5 / about 27; source chip DATA · E3
- **Predict beat.** Q3: lowering diffusion only helps stretching; once the dynamo turns on, it stays on. Right? (Answer: no, windows.)
- **Assets.** `experiences/figures/e3_abc-en.svg`, `assets/interactif/abc-dynamo.js`
- **Data.** `experiences/resultats/e3_abc.json`, `assets/interactif/data/abc-dynamo.json`
- **Flags.** CAVEAT: kinematic test bench, no generative model in E3
- **Sources.** R:1070-1112, D:170-198

#### 03.5 A panel of knobs  
`L2` · 30 s · **READY** · NIGHT · render flat · was C3.5

- **Key idea.** The control parameter is a vector: Re, Rm, materials, boundary conditions, forcing asymmetry, precession.
- **Visual.** The single green knob splits into a panel (Re, Rm, iron, asymmetry, precession). One boundary-condition switch moves a threshold marker up by about 40%, with the chip 'simulations, Nore et al. 2018' (B15). The three definitions of Rm leave this scene (they live in X6.0).
- **On screen.** knob names in words ('iron', not mu_r: D3); 'boundary condition: threshold +40% (simulations)'; formula layer: Rm_c = 90 ± 5 (pseudo-vacuum) -> 130 ± 10 (vacuum) at Re = 1.5e3, mu_r = 50
- **Motifs.** M2 knob panel
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:143, R:90, en/prep/p3 line 722

#### 03.6 A handful of dots  
`L2` · 25 s · **READY** · NIGHT · render flat · was C3.6

- **Key idea.** Each 3D turbulent simulation is expensive, so only a few knob settings exist, each a huge dataset.
- **Visual.** A green parameter axis with a few filled dots; each dot grows a tall grey stack of data files; the gaps between dots stay empty.
- **On screen.** 'each simulation: a few settings, terabytes'; chip 'order-of-magnitude estimate' (C12)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** H:64, T:62, T:931 (VKS sizes)

#### 03.7 The question of this film  
`L2` · 50 s · **READY** · NIGHT · render flat · was C3.7 + C3.8

- **Key idea.** This study asks: can a machine learn the family of possible fields for any knob setting, respect physics exactly where it is exact and statistically where it is statistical, and tell us how often the field flips?
- **Visual.** Lower-third 1, on screen for at least 4 s and not narrated (J): the project context (B1). Then 'This study asks:' and the question, typeset word by word in the colour key, splits into three promise cards that the film ticks off on screen at 05.3, 08.6 and 09.1 (F6); a small violet cloud sits on card 1 (A6). The staircase map of the film (M7) appears with tiers 0-4 all grey (E1). Lower-third 2 with one spoken sentence: the disclaimer (F4; former C3.8 folded in).
- **On screen.** lower-third 1 'MilaDy (context) · ANR-25-CE51-0077 · since January 2026 · 48 months · LISN, Lagrange (OCA), CEREA (ENPC) · goals: reduced models of reversals and bursts; DRESDYN optimisation'; three promise cards; staircase map; lower-third 2 'Independent, prospective study · small CPU experiments · not produced or endorsed by MilaDy, its partners or the supervisors · no MilaDy data used' (full text on the end card and in the description)
- **Motifs.** M7 staircase (planted), M4 violet cloud
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** DISCLAIMER (decision D14)
- **Sources.** S:57-72, H:72, H:43-46, R:51, T:55-58

#### 03.8 Checkpoint: Level 1 done  
`L2` · 15 s · **READY** · NIGHT · render flat · was C3.9

- **Key idea.** Full simulations cost too much, so we start with a caricature that has three dials and already flips.
- **Visual.** Motif recap (threads, knob panel, barcode); rail (left edge) shows for 3 s and climbs to L2; ends on the bridge sentence into ch04 (C4, E8).
- **On screen.** 'Level 1 -> Level 2'
- **Motifs.** M8 rail
- **Assets.** none (new animation)
- **Data.** none

### ch04. Chaos and the shoebox of photographs

`L2` · 4:05 · was C4 · 7 scenes: 7 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** See reversals in a three-mode model, understand why 'when' is unpredictable, and why the stationary distribution (a shuffled box of snapshots) is the stable object; meet crowd laws.
- **Takeaway (one sentence).** The date of the next flip is unknowable, but the cloud of states is stable, and some laws hold only for the cloud.

#### 04.1 Three dials  
`L2` · 30 s · **READY** · NIGHT · render flat · was C4.1

- **Key idea.** Three coupled modes (quadrupole Q, dipole D, velocity V) with the B -> -B symmetry already reverse.
- **Visual.** Three dials (D vermillion, Q light vermillion, V blue) linked by springs; then the equations appear term by term in the same colours; the staircase map lights tier 0 (E1).
- **On screen.** Qdot = 0.119 Q - V D;  Ddot = -0.1 D + V Q;  Vdot = Gamma - V + Q D;  (Q, D, V) -> (-Q, -D, V); coefficients as numbers only (D3); chip 'phenomenological model (Gissinger 2012)'
- **Motifs.** M7 staircase (tier 0 lit)
- **Assets.** `assets/interactif/gissinger.js`
- **Data.** none
- **Sources.** R:159, R:434, R:784

#### 04.2 Two whirlpools and a corridor  
`L2` · 45 s · **READY** · NIGHT · render dense2d · was C4.2

- **Key idea.** Below Gamma about 0.86 each trajectory is trapped in one of two mirror whirlpools; above, a corridor opens and it flips.
- **Visual.** Live RK4 integration in Canvas: (Q, D) phase portrait with a fading trail; green Gamma knob turned from 0.80 to 1.00; the two mirror whirlpools touch; a two-note sound at each crossing (SFX events, G2); scrolling magnetogram strip D(t) with its barcode underneath.
- **On screen.** Gamma knob value; chip 'attractor-merging crisis (shown in mu by Gissinger 2012; expected in Gamma)' (C3)
- **Motifs.** two whirlpools and the corridor, M1 flip sound, M2 knob
- **Assets.** `assets/interactif/gissinger.js`, `prep/p4-systemes-dynamiques/figures/gissinger-en.svg`
- **Data.** `experiences/resultats/e1_gissinger.json#config`
- **Sources.** P4:1513-1541, R:784

#### 04.3 Listen to the rate  
`L2` · 25 s · **READY** · NIGHT · render flat · was C4.3

- **Key idea.** We count every time D crosses zero (most crossings are flips, some are near-misses): the crossing rate switches on at a threshold between Gamma = 0.86 and 0.865 and grows with Gamma.
- **Visual.** Ticks per zero crossing; the simulated crossing rate vs Gamma builds point by point (41 values); training values as filled dots.
- **On screen.** 'crossing rate: 0 up to 0.86 · about 2 per 1,000 time units at 0.865 · about 11 per 1,000 at 1.00' (F5, D5); formula layer: 0.00194 and 0.0112 per unit time
- **Assets.** `proto/scenes/d_curve.html`
- **Data.** `experiences/resultats/e1_gissinger.json#grille_fine.taux_simulation`, `proto/data/e1_rate.json`
- **Sources.** R:871, R:528, D:93-121

#### 04.4 Predict: when is the next flip?  
`L2` · 40 s · **READY** · NIGHT · render dense2d · was C4.4

- **Key idea.** At Gamma = 0.9, errors grow by a factor e every ~11 time units while the mean interval between crossings is about 230: 'when' is out of reach.
- **Visual.** Predict card; two trajectories started 1e-6 apart at Gamma = 0.9, drawn in two shades; their separation on a log axis climbs with slope ~0.09; a ruler compares 11 units with the ~230-unit mean interval (B12).
- **On screen.** 'Gamma = 0.9 · Lyapunov time ~11 · mean interval between crossings ~230'
- **Predict beat.** Q4: we know the state to six decimals. Can we predict the date of the next reversal? (Answer: no.)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** P4:1627, P4:1778, D fine grid (0.00442 crossings per unit time at 0.9)

#### 04.5 The long exposure  
`L2` · 30 s · **READY** · NIGHT · render dense2d · was C4.5

- **Key idea.** Above the threshold, different trajectories paint the same glow: the stationary distribution is reproducible. Below it, each start paints one whirlpool.
- **Visual.** At Gamma = 0.93, shown on screen, two trajectories from different starts leave long-exposure glows that converge to the same shape; an amber histogram of D (bimodal) builds below and becomes identical for both. One closing line: below the threshold, each start paints its own whirlpool (B6).
- **On screen.** 'Gamma = 0.93'; 'the long-exposure glow (stationary distribution)' (B5: mu_Gamma is kept for X2 and X4)
- **Motifs.** M5 amber histogram (first)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** P4:928, R:871, R:901

#### 04.6 The shoebox  
`L2` · 35 s · **READY** · NIGHT · render flat · was C4.6

- **Key idea.** Cut the film into frames, shuffle, drop the timestamps: a sample of the stationary distribution. A snapshot carries no timestamp and no time order.
- **Visual.** A film strip of the trajectory is cut into frames that fall, shuffled, into a shoebox; their time labels flutter away; the box's contents redraw the same cloud.
- **On screen.** 'a snapshot carries no timestamp and no time order' (A4)
- **Motifs.** shoebox (first)
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_echantillons.npz#ref|0.9`
- **Sources.** R:320-322

#### 04.7 Crowd laws  
`L2` · 40 s · **READY** · NIGHT · render flat · was C4.7

- **Key idea.** dE/dt fluctuates from snapshot to snapshot; only its mean is zero. The energy budget is a law of the crowd.
- **Visual.** Each shoebox photo drops a marble into an amber histogram of dE/dt (computed from the model's right-hand side); the histogram breathes around zero; its mean marker sits exactly at 0. A bank-account ledger flashes as a preview.
- **On screen.** 'true on average, not for each'; amber E[P - eps] = 0 (eps = dissipation, never D: D4)
- **Motifs.** M5 amber histogram
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_echantillons.npz#ref|0.93`
- **Sources.** R:321, R:265-278

### ch05. Counting crossings from still photographs

`L2-L3` · 2:40 · was C5 · 5 scenes: 5 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Understand Rice's formula as 'a toll counter without a clock' and see it reproduce the true crossing rate from snapshots plus the equations.
- **Takeaway (one sentence).** A shoebox of snapshots plus the equations gives the crossing rate without running time forward.

#### 05.1 A toll counter without a clock  
`L2` · 40 s · **READY** · NIGHT · render flat · was C5.1

- **Key idea.** From one aerial photo with readable speedometers, count cars in a thin strip, weight by speed, divide by the width: crossings per hour.
- **Visual.** Aerial highway with a line across it; a thin strip around the line highlighted; cars inside the strip glow with their speed; a counter computes the rate; no clock anywhere.
- **On screen.** 'rate = (cars in strip x speed) / strip width'
- **Motifs.** toll counter (first)
- **Assets.** none (new animation)
- **Data.** none

#### 05.2 Rice for the dipole  
`L3` · 50 s · **READY** · NIGHT · render flat · was C5.2

- **Key idea.** For D, the strip is |D| < h and each snapshot's speed Ddot = -0.1 D + V Q comes from the equations.
- **Visual.** Shoebox points spread in the (D, Ddot) plane; the strip |D| < h (h = 0.2) lights up; each point's |Ddot| is drawn as a bar; equation morph to the formula with pen beats (M9). Only about 21 of the 8,000 reference points at Gamma = 0.9 fall in the strip: zoom on the strip and use a denser re-integrated set (C13).
- **On screen.** r_0 = lim_{h->0} (1/2h) E[ |Ddot| 1{|D|<h} ] (r_0 = crossings per unit time, D3); reference chip 'Kac 1943; Rice 1944-1945'
- **Motifs.** M9 pen
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_echantillons.npz#ref|0.9`
- **Flags.** DATA: for a dense strip, re-integrate one long Gissinger trajectory at Gamma = 0.9 in the extractor (CPU seconds), or read experiences/resultats/cache_e1/sim_fine.pkl (local only)
- **Sources.** R:510-538, R:703-709

#### 05.3 Check against the truth  
`L3` · 35 s · **READY** · NIGHT · render flat · was C5.3

- **Key idea.** On the true distribution, with no time order, Rice reproduces direct counting with a cumulative error of 4% near the threshold and 6% above.
- **Visual.** Rates vs Gamma: direct count (solid vermillion) and Rice on reference snapshots (amber) drawn on together. 'Cumulative error' is defined visually once: the shaded area between the two curves divided by the area under the true curve (C7); the same shading returns in 09.1. Promise card 3 gets a first tick.
- **On screen.** 'cumulative error 4% (0.865 <= Gamma <= 0.885) · 6% (Gamma >= 0.89)'; source chip DATA · E1
- **Assets.** `experiences/figures/e1_seuil-en.svg`
- **Data.** `experiences/resultats/e1_gissinger.json#grille_fine.taux_rice_ref`
- **Sources.** R:883

#### 05.4 Crossings are not reversals  
`L3` · 15 s · **READY** · NIGHT · render flat · was C5.4

- **Key idea.** Rice counts every zero crossing, near-misses included, not only clear-cut reversals.
- **Visual.** One caveat card: a D(t) trace with an excursion that touches zero and returns is counted. The other caveats move: 'needs the equations' and 'a rate, not waiting times' to 09.1, 'tested on a 3-variable deterministic system' to X4.1 (F).
- **On screen.** 'crossings, not reversals'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:528, pedagogy P15

#### 05.5 Photographs on demand  
`L3` · 20 s · **READY** · NIGHT · render flat · was C5.5

- **Key idea.** So all we need is a cheap source of snapshots at any knob setting. But how do you get snapshots at a setting nobody simulated?
- **Visual.** The green parameter axis from 03.6 returns, gaps glowing; rail (left edge) shows for 3 s and climbs to L3; ends on the open question (E8).
- **On screen.** 'Level 2 -> Level 3'
- **Motifs.** M8 rail, callback 03.6
- **Assets.** none (new animation)
- **Data.** none

### ch06. A machine that dreams snapshots

`L3` · 3:05 · was C6.1-C6.5 · 5 scenes: 5 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Understand conditional flow matching as learning an average wind from noise to data, conditioned on the knob, and how generated distributions are judged against a noise floor with a distribution distance.
- **Takeaway (one sentence).** A generative model learns a wind that carries noise to data, one model for every knob setting, judged against the noise floor.

#### 06.1 From noise to data  
`L3` · 35 s · **READY** · NIGHT · render dense2d · was C6.1

- **Key idea.** A wind field carries a cloud of random points onto the shape of the data.
- **Visual.** Round violet Gaussian cloud (M4); a time-dependent wind bends particle paths onto two symmetric blobs; granular hiss under the motion (SFX event, G2).
- **On screen.** 'generative model: new, plausible examples on demand'
- **Motifs.** M4 violet cloud (first full appearance)
- **Assets.** `assets/interactif/flow-matching.js`, `figures/flow-matching/figure/out/flow-matching-en.svg`
- **Data.** none
- **Sources.** R:282-296

#### 06.2 Two clocks, two velocities  
`L3` · 20 s · **READY** · NIGHT · render flat · was C6.4

- **Key idea.** The generator's time t in [0, 1] is not physical time, and its velocity v_theta (violet) is not the fluid velocity u (blue).
- **Visual.** Side-by-side chips: violet clock 't: transport time' vs grey clock 'physical time'; violet arrow v_theta vs blue arrow u. Moved before the formulas that use t and v (C6).
- **On screen.** 'the generator makes snapshots, not movies'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:320-322

#### 06.3 Straight strings, average wind  
`L3` · 50 s · **READY** · NIGHT · render dense2d · was C6.2

- **Key idea.** Training is plain regression: at each place and moment, learn the average direction of straight noise-to-data strings.
- **Visual.** Thousands of straight strings from noise points to data points; at a probe location the passing strings average into one violet arrow; the learned trajectories, drawn with transport time t on the horizontal axis (1D state vs t), curve but never cross (C9); pen beats (M9) on the regression target.
- **On screen.** x_t = (1 - t) x_0 + t x_1;  J(v) = E || v(x_t, t, lambda) - (x_1 - x_0) ||^2;  v* = E[x_1 - x_0 | x_t, lambda] (lambda = the knob, green)
- **Motifs.** M9 pen
- **Assets.** `figures/flow-matching/figure/out/flow-matching-en.svg`, `prep/p7-modeles-generatifs/fig-chemins-en.png`
- **Data.** none
- **Sources.** R:282-296, R:593-605

#### 06.4 Turn the knob, reshape the cloud  
`L3` · 30 s · **READY** · NIGHT · render dense2d · was C6.3

- **Key idea.** One model for a continuum of knob settings, including settings never simulated, between those that were (interpolation).
- **Visual.** Green knob drives lambda; target blobs drift and the violet cloud follows; on the knob axis training values are filled dots, test values open dots. Ends with generated violet photos dropping into the 04.6 shoebox (E3).
- **On screen.** 'trained on filled dots, tested on open dots (interpolation only)'
- **Motifs.** M2 knob, M4 cloud, shoebox callback
- **Assets.** `prep/p7-modeles-generatifs/fig-fm-conditionnel-en.png`
- **Data.** none
- **Sources.** R:743

#### 06.5 The noise floor  
`L3` · 50 s · **READY** · NIGHT · render flat · was C6.5

- **Key idea.** Two honest samples of the same truth differ; compare models with that floor at equal sample size, never with zero. A distribution distance measures how far apart two crowds are.
- **Visual.** A die rolled 1000 times, twice: two amber histograms differ; their distance becomes a dashed grey floor line. Then an 8-s 'distance between crowds' beat: the earth-mover picture, sand moved from one histogram onto the other (B6). The formula is not narrated (F).
- **On screen.** dashed 'floor'; amber 'distribution distance'; chip 'technical names: energy distance (used in the experiments), Wasserstein W1 (earth-mover)' (D2, B6); formula layer only: E(P, Q) = 2 E||X - Y|| - E||X - X'|| - E||Y - Y'||
- **Motifs.** dashed grey floor (first), M5 amber histogram
- **Assets.** `prep/p5-probabilites-transport/fig-wasserstein-1d-en.png`
- **Data.** none
- **Sources.** R:715-725, R:747

### ch07. The mirror and the crowd

`L3-L4` · 4:03 · was C6.6 + C7.5-C7.8 (E1 half of C7) · 6 scenes: 6 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** On the three-mode model: see a plain generator inherit the data's polarity bias, a built-in mirror fix it at every knob value while augmentation fixes it only where data exist, the budget check stay blind to the mirror, and a crowd law forced onto each snapshot become a spike; meet the two-jury estimator.
- **Takeaway (one sentence).** Build the mirror into the machine, impose crowd laws on the crowd, and never force a crowd law onto each snapshot.

#### 07.1 A lopsided machine  
`L3` · 40 s · **READY** · NIGHT · render dense2d · was C6.6

- **Key idea.** A plain conditional model reproduces the cloud's shape but inherits the training data's polarity imbalance.
- **Visual.** Opens on two empty shelves labelled in plain words, 'true for every snapshot' and 'true only for the crowd' (C1: the taxonomy becomes the chapter pair's payoff, 08.6). Then (Q, D) clouds at Gamma = 0.85: reference (grey, chip SIMULATED) vs baseline model A (violet chip GENERATED); a polarity balance bar shows A's tilt. Ends on a question mark at the mirror.
- **On screen.** two empty shelves; 'Gamma = 0.85, a value never seen in training'
- **Motifs.** two shelves (empty)
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_echantillons.npz#ref|0.85`, `experiences/resultats/e1_echantillons.npz#A_reference|0.85`
- **Sources.** R:855-873

#### 07.2 Predict: the mirror test  
`L3` · 40 s · **READY** · NIGHT · render dense2d · was C7.5 (first half)

- **Key idea.** A mirror built into the network keeps both polarities equally likely at every knob value. It is built into the machine but acts on the crowd: each snapshot stays lopsided, the crowd is balanced.
- **Visual.** Predict card (one student learns from mirrored copies, the other has a mirror built in); (Q, D) clouds A vs C at 0.85; the mirror gate S acts on the violet cloud: each generated point stays on one side, the crowd balances (C2). The mirror card is placed on the crowd shelf with the tag 'built in, exactly'.
- **On screen.** shelf tag 'built in, exactly'; formula layer: v_sym = 1/2 [v(x) + S v(S x)], S = diag(-1, -1, 1)
- **Predict beat.** Q5: one student learns from mirrored copies, the other has a mirror built in. At an unseen knob value, who stays symmetric? (Answer: the built-in mirror.)
- **Motifs.** M10 mirror, two whirlpools, shelves
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_echantillons.npz#A_reference|0.85`, `experiences/resultats/e1_echantillons.npz#C_equivariant|0.85`, `experiences/resultats/e1_echantillons.npz#ref|0.85`
- **Sources.** R:400-412, R:855-873

#### 07.3 Only where the data are  
`L3` · 35 s · **READY** · NIGHT · render dense2d · was C7.5 (second half)

- **Key idea.** Augmentation symmetrizes only at the knob values it was trained on; between them the network interpolates freely.
- **Visual.** Training data lopsided below the threshold (P(D > 0) = 0.375 at Gamma 0.80, 0.3125 at 0.86). Asymmetry vs Gamma for A, B, C drawn per Gamma (train filled, test open) against the dashed floor: A spikes, B dips only at training values, C sits on the floor everywhere.
- **On screen.** 'A: 0.183 at 0.86, 0.085 at unseen 0.87 · B: 0.003-0.006 at training values, 0.007-0.025 between them (mean 0.016) · C: about 0.004 (floor) everywhere' (B11)
- **Motifs.** dashed floor
- **Assets.** `experiences/figures/e1_symetrie_projection-en.svg`
- **Data.** `experiences/resultats/e1_gissinger.json#evaluation`, `experiences/resultats/e1_gissinger.json#donnees`
- **Sources.** R:839, R:871-873

#### 07.4 The budget is blind to the mirror  
`L3` · 20 s · **READY** · NIGHT · render flat · was C7.6

- **Key idea.** Any mix of the two polarities passes the energy-budget check, so symmetry must be imposed separately.
- **Visual.** A slider p mixes the two whirlpool clouds; the amber budget gauge stays at zero for every p; the lopsided model A even scores best on the budget check (B4).
- **On screen.** 'A: lowest budget-check residual of A, B, C (0.0167 vs 0.0223 and 0.0217)' (C7); formula layer: Remark 3.7
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_gissinger.json#evaluation`
- **Sources.** R:415-417, R:873

#### 07.5 Predict: balance every snapshot?  
`L4` · 58 s · **READY** · NIGHT · render flat · was C7.7

- **Key idea.** Forcing the stationary budget onto each snapshot makes a spike that the truth never produces: worse where it counts (Corollary 6).
- **Visual.** Predict card; bank-account ledger; the amber dE/dt histogram of 04.7 (reference, Gamma = 0.93) and a hand that pushes every marble onto zero: the histogram collapses into a spike. Numbers land after the picture. The budget card goes on the crowd shelf. Closing line sets up 08.5: 'in the next test, a cruder score is fooled by the same spike' (A10).
- **On screen.** 'distribution distance x9 (0.0231 vs 0.00257) · spread of dE/dt -> 4e-17'; formula layer: Cor. 6: no atom at 0 => any law on {L phi = 0} is singular: KL = infinity ('infinitely surprised'), W1 >= E|L phi| / Lip(phi) (B6)
- **Predict beat.** Q6: energy in must equal energy out. Force every snapshot to balance exactly: better or worse? (Answer: worse.)
- **Motifs.** the spike (first), M5 histogram, shelves
- **Assets.** `assets/interactif/contrainte-loi.js`, `experiences/figures/e1_symetrie_projection-en.svg`
- **Data.** `experiences/resultats/e1_echantillons.npz#E_projection_C|0.93`, `experiences/resultats/e1_echantillons.npz#ref|0.93`
- **Sources.** R:448-460, R:881

#### 07.6 Enforce it on the crowd, with two juries  
`L4` · 50 s · **READY** · NIGHT · render flat · was C7.8

- **Key idea.** Impose the budget on the generated distribution during training, even at knob values with no data; estimate it with two independent half-batches.
- **Visual.** A batch of violet samples votes; squaring one batch mean secretly adds a variance penalty (a hidden spike-maker); splitting into two juries and multiplying their means removes it; pen beats (M9).
- **On screen.** E[gbar^2] = (E g)^2 + Var(g)/n;  E[gbar_a gbar_b] = (E g)^2;  S_lambda(theta) = sum_k (E_q[L phi_k] / s_k)^2
- **Motifs.** two juries, M9 pen
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:663-683, R:488-496

### ch08. Fields have stricter laws

`L3-L4` · 4:49 · was C7.1-C7.4 + C7.9-C7.10 + new (E2 half of C7) · 7 scenes: 7 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Meet the 2D MHD test bench; see that clean training data do not give clean outputs, that exact mechanisms (potentials, projection) beat a penalty, that the crowd-level budget loss beats a control run while tilting and per-sample rescaling fail; sort every law onto its shelf.
- **Takeaway (one sentence).** Enforce each law at the level where it is true: build per-snapshot laws into every output, impose crowd laws on the crowd.

#### 08.1 A flat sheet of plasma  
`L3` · 30 s · **READY** · NIGHT · render dense2d · was new (C7.b0)

- **Key idea.** A second test bench with whole fields: forced 2D MHD in a periodic square, with one knob, the magnetic diffusivity eta. A flat world cannot sustain a dynamo on its own: this is a training ground for laws, not a dynamo.
- **Visual.** The chapter card declares a side-step on the rail ('new test bench: from three numbers to whole fields', L4 -> L3). The periodic square tiles itself; blue u and vermillion B maps from the reference samples (32^2, zero-padded in Fourier space to 256^2 for display, G7); the green eta knob with 11 values (6 filled training dots, 5 open test dots). The staircase map lights tier 1 (E1). The anti-dynamo payoff is narrated here (E6, B1 of the pedagogy review).
- **On screen.** 'forced 2D MHD · periodic square · knob: eta · 6 training values, 5 test values'; chip 'not a dynamo: a planar flow cannot sustain a field (Zeldovich); here B is kept alive by its own forcing'; chip 'display interpolation (spectral)'
- **Motifs.** M7 staircase (tier 1 lit), M2 knob
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e2_echantillons.npz#ref`, `experiences/resultats/e2_mhd2d.json#config`
- **Sources.** R:905-919, R:1179, R:240, P3:872-875

#### 08.2 Predict: does clean data make clean outputs?  
`L3` · 42 s · **READY** · NIGHT · render dense2d · was C7.2

- **Key idea.** A model trained only on divergence-free fields still outputs a relative divergence of 0.41; a soft penalty only reaches 0.34 (u) / 0.16 (B).
- **Visual.** Predict card; generated u and B maps (same display interpolation; divergence measured on the native grid) at eta = 0.00951, free model V0 vs reference; a divergence map lights up hot spots; the 'lines in = lines out' box of 01.2 fails its count; penalty bars follow. The divergence card goes on the per-snapshot shelf.
- **On screen.** 'free: 0.41', then 'penalty: 0.34 (u) / 0.16 (B)'; chip 'penalty inflates magnetic energy x2.7' (F)
- **Predict beat.** Q7: trained only on perfectly divergence-free fields, are the outputs divergence-free? (Answer: no, 0.41.)
- **Motifs.** callback 01.2 box, shelves
- **Assets.** `experiences/figures/e2_mecanismes-en.svg`, `experiences/figures/e2_spectres-en.svg`
- **Data.** `experiences/resultats/e2_echantillons.npz#V0_libre`, `experiences/resultats/e2_echantillons.npz#ref`, `experiences/resultats/e2_mhd2d.json#evaluation`
- **Flags.** HYPOTHESIS label for 'the penalty is gamed by inflating the swirl part'
- **Sources.** R:1023-1027, R:931-961

#### 08.3 Hill maps and swirl minus slope  
`L3` · 50 s · **READY** · NIGHT · render dense2d · was C7.3

- **Key idea.** Generate potentials (a landscape) and take the curl: zero divergence for free. Or project: remove each wave's component along its own direction.
- **Visual.** A landscape psi with water walking its contour lines (the 01.2 box returns: nothing piles up); then Fourier space: each wave's arrow loses its component along k (projector motif M6). A gauge needle drops to 1e-17.
- **On screen.** u = (d_y psi, -d_x psi);  u_k -> (I - k k^T / |k|^2) u_k;  gauges: final projection 5e-17 · potentials 1.7e-17 · projected flow 2e-8 (single precision)
- **Motifs.** M6 projector (first), callback 01.2 box
- **Assets.** `assets/interactif/leray.js`, `prep/p1-calcul-vectoriel/fig-helmholtz-en.png`, `prep/p1-calcul-vectoriel/fig-courant-en.png`
- **Data.** `experiences/resultats/e2_mhd2d.json#evaluation`, `experiences/resultats/e2_echantillons.npz#V4_potentiels`
- **Flags.** CAVEAT: divergence measured with the same spectral operator (P16)
- **Sources.** R:1023-1029

#### 08.4 Why almost is not exactly  
`L3` · 30 s · **READY** · NIGHT · render flat · was C7.4

- **Key idea.** To land exactly on the constraint, the ideal wind needs a spring that becomes infinitely stiff at the very end; a network of bounded strength cannot, so a residue always remains.
- **Visual.** NIGHT, no ink change: a ball pulled onto a line by a spring whose stiffness meter shoots up near t = 1; a capped spring (bounded network) leaves a visible gap. No formula in the core cut (B3): Proposition 2 and Remark 3.6 live in X2.2.
- **On screen.** 'needs infinite stiffness at the end' / 'bounded network: a gap remains'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:345-386

#### 08.5 Three ways to fix a budget  
`L4` · 62 s · **READY** · NIGHT · render flat · was C7.9

- **Key idea.** At unseen eta, the crowd-level loss cuts the distribution distance from 2.52 (control run) to 0.70; tilting collapses the effective sample; per-sample rescaling turns the dissipation into a spike while a spectrum-based score even improves.
- **Visual.** Bar race over three lanes with the dashed floor, one number per lane (F): (1) training loss V5 vs a control run of equal length; (2) exponential tilting with an ESS counter ticking down, 'a poll of 500 that shrank to one person' where the model is worst (B10); (3) per-sample rescaling: the dissipation histogram collapses into the spike of 07.5 while the spectrum-based score improves; only the spread of the dissipation reveals it (A10).
- **On screen.** lane 1 '0.70 vs 2.52 (control)'; lane 2 'mean ESS/N 0.29 · one effective sample in 500 at the largest test eta'; lane 3 'spread of eps x 8.6e-4 · spectrum-based distance 2.62 -> 1.1: fooled'; chip 'one seed per variant'; the other numbers go to the description and X3.4
- **Motifs.** M5, dashed floor, the spike
- **Assets.** `experiences/figures/e2_en_loi-en.svg`
- **Data.** `experiences/resultats/e2_mhd2d.json#evaluation`, `experiences/resultats/e2_mhd2d.json#en_loi`
- **Flags.** CAVEAT: one seed, interpolation only (P10, P11)
- **Sources.** R:1031-1035, D:132-162

#### 08.6 Two shelves  
`L4` · 40 s · **READY** · NIGHT · render flat · was C7.1

- **Key idea.** Enforce each law at the level where it is true: per-snapshot laws are built into every output, crowd laws are imposed on the crowd; the mirror is a crowd law that can be built in exactly.
- **Visual.** The two shelves of 07.1, now full: every card placed during ch07-ch08 slides to its final place; in the last 10 s the formal row of the report's classes appears under the shelves (C1). Redrawn taxonomy, no blue for per-sample. Promise card 2 gets its tick.
- **On screen.** 'Enforce a constraint where it is true'; formal row (last 10 s): C1 x in ker A · C2 c(x) = 0 · C3 g#mu = mu · C4 E_mu[L phi] = 0
- **Motifs.** shelves (payoff)
- **Assets.** `figures/taxonomie/figure/out/taxonomie-en.svg`
- **Data.** none
- **Flags.** REDRAW: site figure uses blue for per-sample, which clashes with blue = u
- **Sources.** R:304-317, R:1199

#### 08.7 The proposed machine  
`L4` · 35 s · **READY** · NIGHT · render flat · was C7.10

- **Key idea.** The framework this study proposes, panel by panel; the experiments tested pieces of it only. Checkpoint L3 -> L4.
- **Visual.** The report's framework figure revealed panels a (latent flow to a symmetric law), b (potential decoder) and d (distributional control) only (E9); the tested pieces light up: potentials in 2D, equivariance in 3 variables, the crowd loss, Rice. Rail (left edge) shows for 3 s and climbs to L4; ends on the open question 'so how well does it answer how often?' (E8).
- **On screen.** title 'The proposed machine'; chip 'PROPOSED · not implemented as a whole · E1-E3 tested pieces only' (A6); 'Level 3 -> Level 4'
- **Motifs.** M8 rail
- **Assets.** `figures/cadre/figure/out/cadre-en.svg`
- **Data.** none
- **Sources.** R:300, R:1179, H:41

### ch09. The honest scoreboard

`L4` · 4:00 · was C8 · 6 scenes: 6 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** See the 'how often' payoff with its error bars, why a smooth generator must lag a steep onset, and what remains weak.
- **Takeaway (one sentence).** On a toy model the crossing rate is predicted from generated snapshots and the model's equations, without running time forward: roughly right far from the threshold and poorly near it, as expected from a generator that varies smoothly with the knob.

#### 09.1 How often, from generated photographs  
`L4` · 55 s · **READY** · NIGHT · render flat · was C8.1

- **Key idea.** Rice applied to generated snapshots of model C (seed 0) predicts the crossing rate with 14% cumulative error for Gamma >= 0.89 (up to 65% at a single value) and 42% near the threshold.
- **Visual.** The toll counter of 05.1 returns with violet 'generated cars' (E3). The 04.3 curve returns; Rice on reference (amber) and Rice on generated samples of model C (dashed, violet chip) are drawn on, model F faint; the cumulative error is the shaded area of 05.3 (C7). Two caveat chips moved from 05.4. Promise card 3 gets its tick.
- **On screen.** 'model C, seed 0 · far from threshold: 14% cumulative, pointwise mean 17%, up to 65% at 0.905-0.91 · near threshold: 42%'; chips 'needs the equations' / 'a rate, not waiting times'
- **Motifs.** callback: 'how often' (cold open), toll counter callback
- **Assets.** `experiences/figures/e1_seuil-en.svg`, `proto/scenes/d_curve.html`
- **Data.** `experiences/resultats/e1_gissinger.json#grille_fine`, `proto/data/e1_rate.json`
- **Flags.** CAVEAT: cumulative vs pointwise; zero crossings, not reversals (P15); one model, one seed (B16)
- **Sources.** R:883, R:528, D:79-121

#### 09.2 Predict: early, late or on time?  
`L4` · 40 s · **READY** · NIGHT · render flat · was C8.2

- **Key idea.** Near the threshold the generator leaks a little below, lags at the threshold and overshoots just above.
- **Visual.** Predict card; zoom on 0.80-0.90: tiny spurious crossings below the threshold, a lag at 0.865, an overshoot at 0.875-0.88 (B17).
- **On screen.** 'below: up to 2e-4 per unit time (truth: 0) · 0.865: 0.00030 predicted vs 0.00194 true · 0.88: 0.00500 vs 0.00340'
- **Predict beat.** Q8: near the threshold, will the predicted crossing rate switch on early, late or on time? (Answer: a little leakage below, late at the threshold, then an overshoot just above.)
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_gissinger.json#grille_fine`
- **Sources.** R:883, D fine grid

#### 09.3 A stiff sheet on a steep ramp  
`L4` · 45 s · **READY** · NIGHT · render dense2d · was C8.3

- **Key idea.** A generator that varies smoothly with the knob cannot follow a law whose bridge mass and crossing rate are born with a steep slope (Proposition 9, attenuated form).
- **Visual.** A stiff sheet laid on a steep ramp rounds its knee (no cliff: the symmetrized law varies continuously, A5); then the generated (Q, D) cloud is swept across the 21 Gamma values next to the reference, with the bridge mass P(|D| < 0.25) as a bar that leaks a little below, lags at the threshold and overshoots just above (B17); pen beat on the bound (M9).
- **On screen.** chip 'consistent with Prop. 9 · one model, seed 0'; formula layer: W1(q_lambda, q_lambda') <= K |lambda - lambda'|  =>  max error near lambda_c >= (J_delta - 2 K delta) / 2
- **Motifs.** squeal callback, M2 knob, M9 pen
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e1_gissinger.json#grille_fine.pont_ref`, `experiences/resultats/cache_e1/e1_echantillons_complet.npz`
- **Flags.** LOCAL_ONLY: cache_e1 is gitignored, present on this machine only
- **Sources.** R:544-564, R:883, R:901

#### 09.4 The loss is not a clean win  
`L4` · 30 s · **READY** · NIGHT · render flat · was C8.4

- **Key idea.** On a good model the crowd loss halves stationarity residuals but narrows dE/dt; on a biased model it fails.
- **Visual.** Bars with floors: enforced residual 0.0136 vs 0.0324 (control); distribution distance within the seed spread; spread ratio 1.04 -> 0.75; the biased model's bars blow off the chart (one seed diverged).
- **On screen.** 'good model: residuals / 2, spread ratio 0.75 · biased model: one seed diverged, the other worse'
- **Assets.** `experiences/figures/e1_variantes-en.svg`
- **Data.** `experiences/resultats/e1_gissinger.json#evaluation`
- **Sources.** R:875-877

#### 09.5 Still far from the data  
`L4` · 30 s · **READY** · NIGHT · render flat · was C8.5

- **Key idea.** The models remain well above the data's own noise floor; few seeds; interpolation only.
- **Visual.** Spectral error bars of all variants against the data floor on a log axis; seed counters; 'interpolation' chip.
- **On screen.** 'spectral error 0.07-0.23 (log10) vs 0.002-0.011 for data · E1: 2 seeds · E2: 1 seed · interpolation only'
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e2_mhd2d.json#evaluation`
- **Sources.** R:80, R:1039, R:743-745

#### 09.6 Scoreboard and three lessons  
`L4` · 40 s · **READY** · NIGHT · render flat · was C8.6 + C8.7

- **Key idea.** Eight mechanisms on their shelves, each with a verdict; then three lessons: exact where exact, on the crowd where statistical, judge against the floor.
- **Visual.** Eight cards dealt onto the two shelves of 08.6 (potentials, final projection, projected flow, penalty, equivariance, stationarity loss, tilting, per-sample projection), each with a verdict icon only (exact / approximate / harmful); then the three one-line lessons over a motif recap (box, mirror, spike, floor) (F8).
- **On screen.** verdict icons; three lessons; the full table (R:1149-1158) goes in the description
- **Motifs.** recap beat
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:1149-1158

### ch10. The climb to 3D: bets on the staircase

`L4-L5` · 4:45 (5:25 with results) · was C9 · 9 scenes: 4 READY, 3 PROVISIONAL, 2 PENDING

- **Learning goal.** See the PhD proposal as a staircase of test benches and the data factory that will feed it; separate what is guaranteed by construction from what must be measured; read each upper step as a pre-registered bet.
- **Takeaway (one sentence).** Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the data exist, with the criterion that will settle it.

#### 10.1 The staircase  
`L4` · 25 s · **READY** · NIGHT · render flat · was C9.1

- **Key idea.** Here is where we are on the map planted at the start: tiers 0-1 lit by small experiments; tiers 2-4 are the PhD proposal's bets.
- **Visual.** The staircase map of 03.7 returns as a payoff (E1); T1 morph: the 2D square tiles into a 3D periodic box, which rounds into a cylinder, which starts to precess. Current tier lit.
- **On screen.** tier names; chip 'Independent PhD proposal · not requested or validated by the supervisors' (B13)
- **Motifs.** M7 staircase (payoff)
- **Assets.** `figures/plan-these/figure/out/plan-these-en.svg`
- **Data.** none
- **Flags.** CAVEAT: proposal only (P27)
- **Sources.** T:46-56, T:878-953

#### 10.2 The data factory  
`L4` · 45 s · **READY** · BLUEPRINT · render flat · was C9.2

- **Key idea.** A reproducible pipeline: campaign recipe -> simulations -> labelled files -> catalog -> dataset -> training -> evaluation.
- **Visual.** BLUEPRINT register; a kitchen line of grey stations: recipe card (YAML, green knob on it), ovens (local, Docker, Slurm), jars with checksummed labels (MFF: HDF5 + UUID, commit, SHA-256; C10), ledger (catalog), tasting menu, chef in training (violet), critic (amber). One sentence on stamps: 'a stamp marks results from small trial runs; the full runs will replace them' (H6).
- **On screen.** 'tested end to end on CPU (68 automated tests) · not yet run on a GPU or a real cluster'; stamp legend
- **Assets.** `figures/architecture/figure/out/architecture-en.svg`, `assets/interactif/architecture.js`
- **Data.** none
- **Flags.** CAVEAT: HPC not yet run (P25)
- **Sources.** C:45, C:88-149, C:190

#### 10.3 First product off the line  
`L4` · 15 s · **PROVISIONAL** · NIGHT · render dense2d · was C9.3

- **Key idea.** The first real campaign: ensembles of 2D MHD maps across 11 values of eta, where the dissipation fluctuates around the constant injected power: the crowd law on fresh data.
- **Visual.** A grid of 11 small (omega, j) map tiles, one per eta; under each, the dissipation eps(t) fluctuating around a flat, labelled line eps_inj (Ito rate) (A3); an amber histogram of eps_inj - eps per eta, centred on zero. A short beat (F7): the full sweep is in X5.3.
- **On screen.** per-eta mean and spread of eps_inj - eps from the data file; stamp 'SIMULATED · palier1_mhd2d · 32^2 · run <id>'
- **Assets.** none (new animation)
- **Data.** `data/palier1_sweep.json`
- **Sources.** CFG palier1_mhd2d.yaml, C:93, R:442, R:919
- **Regeneration hook.**
  - scene data: `data/palier1_sweep.json`
  - upstream: 11 MFF files {store}/palier1_mhd2d/{uuid}/fields.h5: t1_fields/velocity, magnetic_field (16, 150, 32, 32, 2) float32; milady_diagnostics/injection (constant Ito rate, np.full: milady/sim/run.py:256-273), dissipation, kinetic_energy, magnetic_energy; catalog rows campaign/simulation/file
  - provisional run (now, CPU): make sweep CONFIG=infra/configs/palier1_mhd2d.yaml  (CPU; the campaign as configured; same workload as the E2 data, about 30 min, X:69)
  - final run: tier 1 at full scale (128^2, 8 x 8 (nu, eta) grid, about 700 GPU h, T:898-904): not configured yet
  - extractor: tools/extract_data.py: palier1_sweep() (to write; replaces the demo stub palier1_eta_sweep()): per eta, dissipation series, the flat injection line, histogram of injection - dissipation, one map tile
  - ships now as: empty seat, or E2 samples at eta = 0.00951 only (experiences/resultats/e2_echantillons.npz) stamped PROVISIONAL
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### 10.4 Bet 1: the ABC windows at 64^3  
`L4` · 40 s now / 45 s with results · **PROVISIONAL** · NIGHT · render flat · was C9.4

- **Key idea.** The dynamo windows measured at 32^3 should persist and sharpen at 64^3, up to Rm = 40, and the second threshold should be pinned between Rm = 17 and 18.
- **Visual.** The E3 32^3 curve as a grey ghost with its 48^3 check marks (READY anchor, H3); the new points drawn over it from the data file; windows re-shaded from the new zero crossings; inset 3D mode renders on both sides of each threshold (meshes precomputed offline, G8).
- **On screen.** 'bet: windows 8.9 < Rm < 17.5 and Rm > ~27 (published) · s(17) > 0 > s(18), with |s - s_q| below |s|' (A2); stamp from the data meta
- **Assets.** `experiences/figures/e3_abc-en.svg`
- **Data.** `data/palier2_abc3d.json`, `experiences/resultats/e3_abc.json`
- **Sources.** CFG palier2_abc3d.yaml, R:1112-1114
- **Regeneration hook.**
  - scene data: `data/palier2_abc3d.json`
  - upstream: 37 MFF files (Rm 4-40 in integer steps, CFG palier2_abc3d.yaml:36): magnetic_field (2, 20, 64, 64, 64, 3); diagnostics log_b_rms, growth_rate; catalog diagnostic growth_rate_fit (query: python -m milady.catalog sims --campaign palier2_abc3d); plus 3 files at Rm 17.25, 17.5, 17.75 if decision D17 adds them
  - provisional run (now, CPU): copy infra/configs/palier2_abc3d.yaml to $RUNS/configs/palier2_abc3d_n48.yaml with grid.N: 48, name: palier2_abc3d_n48_provisional and sweep Rm: [8, 8.5, 9, 9.5, 17, 17.25, 17.5, 17.75, 18, 26, 26.5, 27, 27.5, 28] (a list, as in palier2_tg3d.yaml); python -m milady.sweep <copy> --scheduler local --max-parallel 2 --device cpu, after --dry-run; duration unmeasured (time one point first). Not at 32^3: it would redraw the E3 curve (H5)
  - final run: make sweep CONFIG=infra/configs/palier2_abc3d.yaml  (64^3, integer Rm 4-40; estimate ~15 h serial on 2 CPU threads, or GPU / Slurm array) + a copy with Rm: [17.25, 17.5, 17.75] (decision D17)
  - extractor: tools/extract_data.py: palier2_abc3d() (to write): (Rm, s, s_last_quarter, seed), interpolated thresholds, downsampled modes (.f32)
  - criterion: published windows 8.9 < Rm < 17.5 and Rm >~ 27 (R:1112); s(17) > 0 > s(18) with |s - s_q| < |s| at both (the sign at 17.5 only if the extra points are run)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists. The E3 32^3 curve is drawn as a labelled ghost.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### 10.5 Bet 2: a dynamo that saturates (Taylor-Green)  
`L5` · 40 s now / 45 s with results · **PROVISIONAL** · NIGHT · render flat · was C9.5

- **Key idea.** A forced Taylor-Green flow should grow a weak seed field exponentially above a threshold in Rm = Re x Pm, then saturate where the run is long enough: the first true dynamo of the staircase.
- **Visual.** READY anchor first (H3): the Taylor-Green cell flow and a schematic grow-then-saturate curve (chip SCHEMATIC). Then a grid of log E_B(t) curves, one per (Re, Pm), from the data file: each starts at the 1e-3 seed, grows or decays, and bends into a plateau where the run is long enough; runs whose kept window is not saturated are drawn hatched and labelled 'still growing' (A8); a (Re, Pm) map colours each point dynamo / no dynamo / not saturated. Render flat; an optional 3D insert of saturated B is a separate short WebGL shot (G9).
- **On screen.** 'anchor: Rm_c = 30 at Pm = 1 (Ponty et al. 2005), different forcing convention: qualitative only'; 'saturated' flag per run
- **Assets.** none (new animation)
- **Data.** `data/palier2_tg3d.json`
- **Flags.** CAVEAT: Re = 200, Pm = 2 may be under-resolved even at 64^3 (CFG palier2_tg3d.yaml:12-14); CAVEAT: with a 1e-3 seed, the kept window t in [100, 140] may still be pre-saturation near the threshold (A8)
- **Sources.** CFG palier2_tg3d.yaml, T:908
- **Regeneration hook.**
  - scene data: `data/palier2_tg3d.json`
  - upstream: 12 MFF files (Re 25-200 x Pm 0.5-2): velocity and magnetic_field (1, 40, 64, 64, 64, 3) kept for t in [100, 140] (CFG palier2_tg3d.yaml:41-43); diagnostics energies, dissipations, injection, helicities, max divergences, growth_rate, b_rms, log_b_rms; catalog growth_rate_fit
  - provisional run (now, CPU): copy infra/configs/palier2_tg3d.yaml to $RUNS/configs/palier2_tg3d_n32.yaml (grid.N: 32, new name); python -m milady.sweep <copy> --scheduler local --device cpu --indices <Re <= 100, read the order with --dry-run>  (estimate 1-1.5 h, unmeasured; check resolution)
  - final run: make sweep CONFIG=infra/configs/palier2_tg3d.yaml  (64^3, GPU, 10 h limit per simulation; estimate ~8 h CPU for all 12); longer t_burn / t_keep near the threshold if decision D18 says so
  - extractor: tools/extract_data.py: palier2_tg3d() (to write): per (Re, Pm) time series log E_B(t), fitted rate, saturated E_B, mean spectra, and a stationarity flag: saturated only if the slope of log E_B over the kept window is near 0 (threshold to fix, e.g. below 10% of the kinematic rate) (A8)
  - criterion: qualitative at this scale; saturated runs only; the tier-2 criterion 'Rm_c within 10% at a Pm without data' needs the full tier (T:917)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists. The schematic anchor is shown in both variants.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### 10.6 What is guaranteed  
`L5` · 25 s · **READY** · NIGHT · render webgl · was C9.6

- **Key idea.** Generating vector potentials in Coulomb gauge makes div u = div B = 0 to rounding, and the B -> -B mirror exact, whatever the training quality: it holds even for an untrained network.
- **Visual.** The 3D generator with random (untrained) weights emits fields: field lines (violet frame, vermillion lines) beside the divergence gauge at ~1e-16; the projector motif (M6) shows the potential-to-field step (E4); a mirror gate maps the sample generated from z onto the one generated from S z. Paired with 10.7 as 'what is guaranteed' vs 'what must be measured' (H4).
- **On screen.** 'by construction (Prop. 1, Prop. 4): this shows the mechanism, not quality'; stamp 'GENERATED · fm3d · untrained weights'
- **Motifs.** M6 projector (callback), M10 mirror
- **Assets.** `milady/train/fm3d.py`
- **Data.** none
- **Flags.** BUILD-TIME DATA: tools/extract_data.py fm3d_guarantees() (to write) builds the fm3d velocity field with random weights and unit normalisation on CPU (seconds, needs torch) and writes data/fm3d_guarantees.json (div_rel_u, div_rel_b, mirror error); no simulation or training needed, so the scene is READY
- **Sources.** C:164-166, CFG train_fm3d.yaml, R:327-335, R:400-412

#### 10.7 What must be measured  
`L5` · 25 s now / 40 s with results · **PENDING** · NIGHT · render flat · was C9.7

- **Key idea.** Does the 3D generator get the statistics right? The spectra at the training points face the plan's criterion; the held-out point (Re = 50, Pm = 2) is a diagnostic; saturated runs only.
- **Visual.** READY anchor (H3): a lamp panel with three unlit lamps and the criteria written beside them. Result variant: spectra E_u(k), E_B(k) simulated (solid) vs generated (dashed, violet chip) at the training points with the 0.1-decade band; the held-out point as a separate panel 'diagnostic, no criterion'; bars vs dashed floor for train / val / test.
- **On screen.** criterion (b) at the training points: log-spectrum error < 0.1 decade per band up to half the cutoff; lamps labelled 'indicative at 12 x 40 snapshots; plan: about 20 x 5000' (A7); criterion (c) 'Rm_c within 10% at a Pm without data': later
- **Assets.** none (new animation)
- **Data.** `data/fm3d_eval.json`
- **Sources.** CFG train_fm3d.yaml, T:912-917, milady/eval/metrics.py:588-662, 894-907
- **Regeneration hook.**
  - scene data: `data/fm3d_eval.json`
  - upstream: evaluation JSON {model, model_id, created, results: [{point, physical_parameters, metrics, details, seconds}]} with err_spectre_u_log10, err_spectre_b_log10, residu_bilan_total, dist_energie, plancher_dist_energie; details spectrum_u, spectrum_b, spectrum_u_ref, spectrum_b_ref; plus the stationarity flags of 10.5's extractor (A8)
  - final run: make train CONFIG=infra/configs/train_fm3d.yaml NGPUS=4 (GPU); make eval CONFIG=infra/configs/train_fm3d.yaml [MODEL=<uuid>] EVAL_ARGS="--out eval_fm3d.json" (val point Re 100, Pm 1; test point Re 50, Pm 2: CFG train_fm3d.yaml)
  - requires: 10.5 final run (palier2_tg3d at 64^3); final fm3d training
  - extractor: tools/extract_data.py: fm3d_eval() (to write)
  - criterion: tier-2 criterion (b) of the PhD plan, log-spectrum error < 0.1 decade per band up to half the cutoff, at the training points (T:917), indicative only at 12 x 40 snapshots (plan: about 20 x 5000, T:912); held-out and validation points are diagnostics; (a) divergence is shown in 10.6; (c) and (d) need the full tier
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists. The lamp panel and its criteria are the anchor.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### 10.8 Walls and iron  
`L5` · 40 s · **READY** · PAPER · render flat · was new (merge of X6.1 + X6.2)

- **Key idea.** Leaving the periodic box changes what 'exact' means: in a bounded domain the potential needs a gauge with a boundary condition, and across iron the field refracts, so the potential has a kink; matching to the vacuum outside is linear but nonlocal.
- **Visual.** PAPER (T3 ink change): the periodic box rounds into a cylinder; potential arrows at the wall snap to the boundary condition; an iron disc interface where field lines refract and the potential profile kinks; an exterior potential field wraps the cylinder. Core merge of X6.1 and X6.2 (B7 of the pedagogy review); the extended cut plays X6.1 and X6.2 in full instead.
- **On screen.** div A = 0 with A.n = 0 or A x n = 0 (Amrouche-Seloula); 'B.n and tangential B / mu_r continuous'; chip 'vacuum matching: candidate routes, an open question of the PhD plan' (C11)
- **Assets.** none (new animation)
- **Data.** none
- **Extended cut.** Skipped; X6.1, X6.2 play in full instead.
- **Sources.** R:339, T:114-115, T:211-266, T:272

#### 10.9 The top steps: VKS and DRESDYN  
`L5` · 30 s now / 45 s with results · **PENDING** · NIGHT · render flat · was C9.8

- **Key idea.** The last two steps need consortium data that are not public: the bets and their criteria are written now.
- **Visual.** READY anchor (H3): the VKS and DRESDYN schematics. Two empty seats on the top steps: VKS cylinder (D, Q) plane with a dashed density frame; DRESDYN Rm_c(Po) axis with a dashed band; each with its data tag. In the extended cut, the 15-s entry '10.9-bridge' replaces it (H8).
- **On screen.** VKS: 4 POD energy fractions within 10% · (D, Q) distribution distance < 2x floor · Rice in the 95% Poisson interval; DRESDYN: Rm_c within 10% and correct symmetry class at a Po without data
- **Assets.** `figures/vks/figure/out/vks-en.svg`
- **Data.** `data/tier3_vks.json`, `data/tier4_dresdyn.json`
- **Extended cut.** Replaced by the entry `10.9-bridge` (15 s): bridge into X6: names the two top steps and hands over.
- **Flags.** CAVEAT: no MilaDy data used (P3)
- **Sources.** T:927-953, S:100
- **Regeneration hook.**
  - scene data: `data/tier3_vks.json + data/tier4_dresdyn.json`
  - upstream: SFEMaNS / LATU simulations from the consortium (not public) converted to MFF grid_type fourier_fe_axisym (milady_fourier_fe/fields/velocity (B, T, M, 2, N_fluid, 3), magnetic_field ...); generated u fields + kinematic eigenvalues per Po (format to define)
  - final run: consortium data access; native SFEMaNS reader to write (milady/data/convert.py:9-12); then train / eval as tier 2
  - extractor: tools/extract_data.py: tier3_vks(), tier4_dresdyn() (to write)
  - criterion: T:927-953 criteria (a)-(d) for VKS, (a)-(b) for DRESDYN
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists. Fallback: VKS schematic + Gissinger as 'pocket dynamo' proxy, chip SCHEMATIC.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

### ch11. Back to the compass

`L5-L0` · 2:00 · was C10 · 3 scenes: 3 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Separate what was measured from what is bet, and leave with the one-sentence lesson.
- **Takeaway (one sentence).** We cannot say when the needle will turn, but we are learning to answer how often, by enforcing each law where it is true.

#### 11.1 Measured, and bet  
`L5` · 35 s · **READY** · NIGHT · render flat · was C10.1

- **Key idea.** Two columns: what the small experiments measured, and what the staircase bets.
- **Visual.** MEASURED column (E1, E2, E3 headline numbers with caveat chips); BET column (tiers 1-4 with data tags and a status pill READY / PROVISIONAL / PENDING read from timeline.json at build time). Every regenerable data file is a declared dependency, so the hash-based rebuild re-renders this scene when any of them changes (H2).
- **On screen.** headline numbers; status pills
- **Assets.** none (new animation)
- **Data.** `proto/timeline.json`
- **Re-render when these change.** `proto/timeline.json`, `data/palier1_sweep.json`, `data/palier2_abc3d.json`, `data/palier2_tg3d.json`, `data/fm3d_eval.json`, `data/tier3_vks.json`, `data/tier4_dresdyn.json`
- **Sources.** H:80-90

#### 11.2 The compass again  
`L0` · 70 s · **READY** · NIGHT · render webgl · was C10.2

- **Key idea.** Closing narration: we cannot say when; we can learn how often; enforce each law where it is true.
- **Visual.** The stylized compass of 00.1 returns (no hand). A sequenced montage, one motif per closing sentence, 3-4 s each (barcode, threads, whirlpools, shoebox, violet cloud, mirror, the amber histogram that keeps its width), then a fade to the clean compass for the three-line lesson (G6). Rail descends to L0.
- **On screen.** numbers as chips only (J): '14% far from the threshold · 42% near it · model C, seed 0'; then the lesson in three short lines
- **Motifs.** M1, motif montage
- **Assets.** none (new animation)
- **Data.** none
- **Re-render when these change.** `proto/timeline.json`, `data/palier1_sweep.json`, `data/palier2_abc3d.json`, `data/palier2_tg3d.json`, `data/fm3d_eval.json`, `data/tier3_vks.json`, `data/tier4_dresdyn.json`
- **Flags.** NARRATION VARIANTS: paragraph 3 has a pending and a results-in variant keyed to timeline.json (H2)

#### 11.3 End card  
`L0` · 15 s · **READY** · NIGHT · render flat · was C10.3

- **Key idea.** Credits, sources, full disclaimer, link to the site.
- **Visual.** Static card with a slow field-line drift.
- **On screen.** site URL; 'narration: original synthetic voice'; 'animations generated in code'; full disclaimer text (decision D14); supervisors as listed in the public offer (decision D6)
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** DISCLAIMER

## 6. Extension modules

Each module is self-contained and slots in after its anchor (a scene or another module); the core cut never refers to them. Order of appearance in the extended cut: X2 → X3a → X4a → X5a → X1 → X4b → X3b → X6 → X5b.

### X2. The proofs behind the pictures

`L4` · 3:30 · inserted after 08.7 · was X2 · 5 scenes: 5 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** State Propositions 1-5 and their scope, as the specialists will want them.
- **Takeaway (one sentence).** Each picture of ch07-ch08 is backed by an elementary statement with a precise scope, often known in other forms.

#### X2.1 Proposition 1: build it in  
`L4` · 35 s · **READY** · PAPER · render flat · was X2.1

- **Key idea.** If the decoder's image lies in the constraint subspace, every sample satisfies the constraint, whatever the training quality.
- **Visual.** PAPER; statement typed on; a decoder box whose output arrows all land on a plane.
- **On screen.** Prop. 1 statement
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:327-335

#### X2.2 Proposition 2 in full  
`L4` · 50 s · **READY** · PAPER · render flat · was X2.2 (+ C7.4 formula)

- **Key idea.** The optimal flow on a subspace splits into a learnable part and a stiff contraction; a bounded network leaves O(1) residuals.
- **Visual.** PAPER; the formula grows term by term; the contraction term 1/(1 - t) is plotted against t (the spring of 08.4); V3's 2e-8 explained by single precision. Sole home of the formula since 08.4 became intuitive (B3, I5).
- **On screen.** v* = m(P x, t) - (I - P) x / (1 - t); Remark 3.6
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:345-386

#### X2.3 Proposition 3: the Jensen gap  
`L4` · 40 s · **READY** · PAPER · render flat · was X2.3

- **Key idea.** A penalty on the end-of-path prediction is unbiased for linear constraints and biased for nonlinear ones.
- **Visual.** A curved constraint arc; the mean of two points falls off the arc: the gap is shaded.
- **On screen.** Prop. 3 statement
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:389-395

#### X2.4 Proposition 4: the mirror, proved  
`L4` · 45 s · **READY** · PAPER · render flat · was X2.4

- **Key idea.** Equivariant velocity + invariant noise give an exactly invariant distribution at every parameter; if each mu_lambda is symmetric, symmetrization never increases the population loss; it doubles network evaluations.
- **Visual.** Mirror gate on the violet flow, then the proof in three lines.
- **On screen.** v(g x, t, lambda) = g v(x, t, lambda), g#gamma = gamma => g#q(.|lambda) = q(.|lambda) for every lambda; condition 'if each mu_lambda is G-invariant' on the loss statement (C10); 'cost: 0.5 s vs 0.25 s per 1000 samples'
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** P22: classical for equivariant flows
- **Sources.** R:400-412, R:885

#### X2.5 Proposition 5 and its limits  
`L4` · 40 s · **READY** · PAPER · render flat · was X2.5

- **Key idea.** For every test function, E_mu[L phi] = 0; the energy budget is one case. Necessary, not sufficient: fixed points and unstable orbits satisfy it too.
- **Visual.** Amber identity, then a fixed point and an unstable orbit each pass the same test (warning lamp); degree <= 2 monomials enforced, degree 3 kept as a control. The generator L and the degrees are introduced here, not in the core (B4).
- **On screen.** E_mu[L phi] = 0; Remark 3.11; 'enforced: degree <= 2 · control: degree 3'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:422-430, R:569-571, R:434, R:727

### X3a. Crowd laws, deeper

`L4` · 2:50 · inserted after X2 · was X3.1-X3.4 · 5 scenes: 5 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** Define the distribution distance, understand exponential tilting as an I-projection and why it cannot create mass, and read the per-eta detail.
- **Takeaway (one sentence).** Reweighting cannot visit places the model never went.

#### X3.0 The distribution distance, defined  
`L4` · 20 s · **READY** · PAPER · render flat · was new (from C6.5)

- **Key idea.** The energy distance compares two crowds through average pairwise distances; it is zero only when the crowds have the same law.
- **Visual.** The formula built term by term over two point clouds with faint pairwise lines (moved from 06.5, F).
- **On screen.** E(P, Q) = 2 E||X - Y|| - E||X - X'|| - E||Y - Y'||; 'called distribution distance in the film' (D2)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:715-725

#### X3.1 The least-distorting correction  
`L4` · 40 s · **READY** · NIGHT · render flat · was X3.1

- **Key idea.** Exponential tilting is the I-projection: the reweighting that fixes a mean with minimal KL change, without moving any sample.
- **Visual.** Dots whose size is their weight; the tilted density slides to the target mean; Pythagorean triangle for KL.
- **On screen.** q* = e^(beta . g) q / Z(beta);  beta* = argmin log Z(beta) - beta . c (Csiszar 1975); supp q* = supp q (q* for the tilted law, D3)
- **Assets.** `prep/p5-probabilites-transport/fig-inclinaison-en.png`, `prep/p8-contraintes-physiques/fig-inclinaison-en.png`
- **Data.** none
- **Sources.** R:465-485

#### X3.2 The poll that shrank  
`L4` · 45 s · **READY** · NIGHT · render flat · was X3.2

- **Key idea.** Effective sample size collapses exactly where the model is poor.
- **Visual.** Per-eta ESS bars from the data: 0.99 at the easiest eta, 0.002 at the three largest test eta, about one effective sample in 500 (B10); in E1 one sample swells to 33x the mean weight.
- **On screen.** ESS = 1 / sum w_i^2; 'E2: mean ESS/N 0.29 · 0.002 at large eta (1 in 500) · E1 Gamma = 0.85: ESS/N 0.67, one weight 33x the mean'
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e2_mhd2d.json#en_loi.ess_frac_b`, `experiences/resultats/e1_gissinger.json#evaluation`
- **Sources.** R:1033, R:879, D:162

#### X3.3 Where the model never went  
`L4` · 35 s · **READY** · NIGHT · render flat · was X3.3

- **Key idea.** No weight can conjure samples in a region the model never produced; tilting is not a fallback.
- **Visual.** The 'missing support' toggle of the distributional widget: the bridge region is empty, weights explode, ESS counter falls.
- **On screen.** 'reweighting cannot create mass'
- **Assets.** `assets/interactif/contrainte-loi.js`
- **Data.** none
- **Sources.** R:465-485, T:988-1000

#### X3.4 Per-eta detail  
`L4` · 30 s · **READY** · NIGHT · render flat · was X3.4

- **Key idea.** The crowd loss helps where the base model is worst and does nothing where it is already good.
- **Visual.** Three grouped bars per test eta (V4 / control / V5), distribution distance.
- **On screen.** 'eta 0.01903: 7.74 / 7.63 / 2.22 · 0.01345: 3.63 / 3.51 / 0.792 · 0.00476: 0.184 / 0.178 / 0.186 · V4 signed residual +1.22 at 0.01903'
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e2_mhd2d.json#en_loi`
- **Sources.** R:999-1013

### X4a. What snapshots can and cannot tell

`L4-L5` · 2:25 (2:30 with results) · inserted after 09.6 · was X4.1-X4.3 + X4.5 · 4 scenes: 2 READY, 2 PROVISIONAL, 0 PENDING

- **Learning goal.** Know the Rice estimator's bias and variance and its test conditions, the threshold bound on reversal rates, why waiting times need dynamics, and the next round of tier 0.
- **Takeaway (one sentence).** A snapshot generator bounds and estimates rates, but waiting times need the dynamics; tier 0 needs more seeds and a joint mirror.

#### X4.1 Rice, the estimator  
`L4` · 40 s · **READY** · NIGHT · render flat · was X4.1 (+ C5.4 caveats)

- **Key idea.** The window estimator has bias O(h^2) and variance O(1/(N h)); E1 uses h = 0.2. It needs the right-hand side, and it was validated on a 3-variable deterministic system only.
- **Visual.** A slider on h trades a blurry strip against a noisy count; sanity checks: a cosine crosses twice per period; Gaussian case; two caveat cards moved from 05.4.
- **On screen.** bias O(h^2), variance O(1/(N h)); Gaussian: r_0 = sigma' / (pi sigma); 'needs F' · 'tested on a 3-variable deterministic system'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:510-528, R:703-709, R:901

#### X4.2 A bound from thresholds  
`L5` · 40 s · **PROVISIONAL** · NIGHT · render flat · was X4.2

- **Key idea.** Counting crossings of levels +/- a bounds the reversal rate: r <= r_a (Prop. 2.30); the plateau conjecture 2.33 says when the bound is tight.
- **Visual.** Rates of crossings of +/- a vs a, from reference and generated snapshots, with the true reversal rate as a floor line; tightness band.
- **On screen.** r <= r_a (Prop. 2.30; r = reversal rate, r_a = rate of crossings of +/- a, D3); Conjecture 2.33; tier-0 criterion 'bound tight within 30%'
- **Assets.** none (new animation)
- **Data.** `data/x4_rice_levels.json`
- **Sources.** T:683-727
- **Regeneration hook.**
  - scene data: `data/x4_rice_levels.json`
  - upstream: E1 reference trajectories (re-integrated, CPU minutes) and generated samples at all 21 Gamma (experiences/resultats/cache_e1/e1_echantillons_complet.npz, local only)
  - provisional run (now, CPU): new extractor rice_levels(): level-a crossing rates on re-integrated Gissinger trajectories + Rice at level a on generated samples (CPU, minutes; code to write)
  - final run: tier-0 campaign with 1e6 snapshots per parameter and 3 seeds (T:878-890, CPU, about 1e3 h assumption)
  - extractor: tools/extract_data.py: rice_levels() (to write)
  - criterion: Prop. 2.30 bound tight within 30% (T:878-890)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### X4.3 Waiting times need the movie  
`L5` · 35 s · **READY** · NIGHT · render dense2d · was X4.3

- **Key idea.** The one-time law does not determine the distribution of waiting times (Prop. 2.32); in the three-mode model they are quantized at short times and Poissonian at long times.
- **Visual.** Histogram of waiting times between reversals from a long live integration at Gamma = 0.90, with the short-time comb and the exponential tail.
- **On screen.** Prop. 2.32; 'quantized short, Poissonian long'
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** T:683-727, P4:1541

#### X4.5 Tier 0, the next round  
`L5` · 30 s now / 35 s with results · **PROVISIONAL** · NIGHT · render flat · was X4.5

- **Key idea.** Three seeds, a derived reversal model (DQVU) and a joint state-parameter mirror R_pi that also flips the forcing asymmetry.
- **Visual.** Gissinger panel gains a third seed lane; a DQVU card (Re 1594, Rm 531, asymmetry 0.058, iron mu_r 16, POD on 2000 snapshots); R_pi mirror flips both the state and the asymmetry knob. The staircase is known since 03.7, so tiers can be named here (I3).
- **On screen.** Prop. 2.24; tier-0 criteria: asymmetry below floor at all Gamma, non-enforced residuals / 2 vs control, Rice within 20%
- **Assets.** none (new animation)
- **Data.** `data/x4_tier0.json`
- **Sources.** T:878-890, T:931, S:98, T:613
- **Regeneration hook.**
  - scene data: `data/x4_tier0.json`
  - upstream: E1-style JSON (per-parameter metrics, fine-grid Rice) with 3 seeds; DQVU results later
  - provisional run (now, CPU): run experiences/e1_gissinger.py from a working copy with seeds {0, 1, 2} (seeds are fixed in code; about 3-4.5 h CPU: X:71 gives 2-3 h for two seeds, unless the seed-0/1 caches in cache_e1 are reused) (C12), then experiences/digest.py
  - final run: tier-0 plan (T:878-890); DQVU needs the published coefficients (Bousquet et al. 2026 appendix); no DQVU code in the repository
  - extractor: tools/extract_data.py: tier0() (to write)
  - criterion: T:878-890 criteria
  - ships now as: E1 two-seed results with a '2 seeds' chip
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

### X5a. The factory floor

`L4` · 2:30 · inserted after 10.3 · was X5.1-X5.4 · 4 scenes: 2 READY, 2 PROVISIONAL, 0 PENDING

- **Learning goal.** Open the data factory: one solver step, one file, one campaign trace, a new metric.
- **Takeaway (one sentence).** Reproducibility is designed in: every number on screen traces back to a file, a commit and a catalog row.

#### X5.1 One solver step  
`L4` · 40 s · **READY** · BLUEPRINT · render flat · was X5.1

- **Key idea.** A pseudo-spectral MHD step goes back and forth between Fourier and physical space, with 2/3 dealiasing and an integrating-factor RK4.
- **Visual.** BLUEPRINT; a field tile hops between a Fourier grid and a physical grid; the 2/3 mask trims the corners; memory bar for the state 6 N^3 x 4 bytes, with the measured-peak factor drawn separately (B14).
- **On screen.** '64^3 dynamic step: 0.08 s on 2 CPU threads · state 0.4 GB at 256^3 · peak about 15x the state: about 6 GB at 256^3, about 48 GB at 512^3 (estimates from a 128^3 measurement)'
- **Assets.** `figures/solveur/figure/out/solveur-en.svg`
- **Data.** none
- **Sources.** C:153, C:176

#### X5.2 A jar with a label  
`L4` · 35 s · **READY** · BLUEPRINT · render flat · was X5.2

- **Key idea.** Each simulation is one MFF file (HDF5, The Well convention) with UUID, commit and checksum, mirrored by a catalog row.
- **Visual.** File tree unfolds: t1_fields/velocity, magnetic_field, milady_diagnostics/*, scalars; a ledger row lights with the same UUID.
- **On screen.** MFF tree; catalog tables campaign, simulation, file, diagnostic, dataset, model, evaluation, job; 'checksummed, --force rewrites and updates the SHA-256' (C10)
- **Assets.** `figures/solveur/figure/out/solveur-en.svg`
- **Data.** none
- **Sources.** C:93, C:107-139

#### X5.3 The life of one campaign  
`L4` · 40 s · **PROVISIONAL** · BLUEPRINT · render flat · was X5.3

- **Key idea.** From one command to files and catalog rows: a real trace with measured wall times, then the 11 eta tiles of 10.3 in full.
- **Visual.** Terminal-style trace (mono) of a sweep: jobs light up, jars fill, ledger rows appear with wall_time_s; numbers from the run, not typed; ends on the full per-eta sweep (tiles, flat injection line, histograms) (F7).
- **On screen.** command line; counts and wall times from the data file
- **Assets.** none (new animation)
- **Data.** `data/x5_campaign_trace.json`
- **Sources.** C:143-149, IR:386
- **Regeneration hook.**
  - scene data: `data/x5_campaign_trace.json`
  - upstream: catalog dump of the palier1_mhd2d campaign (simulation rows with wall_time_s, file sizes, checksums)
  - provisional run (now, CPU): same run as 10.3 (make sweep CONFIG=infra/configs/palier1_mhd2d.yaml), then python -m milady.catalog sims --campaign palier1_mhd2d
  - final run: the same trace on the GPU VM or Slurm cluster for a palier2 campaign
  - requires: 10.3 provisional run
  - extractor: tools/extract_data.py: campaign_trace() (to write)
  - ships now as: architecture.js walk-through with a SCHEMATIC chip (no numbers)
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### X5.4 A new instrument for the critic: counting X-points  
`L4` · 35 s · **PROVISIONAL** · NIGHT · render dense2d · was X5.4

- **Key idea.** Topology metrics were requested by the internship offer and not yet computed: count saddle (X) and extremum (O) points of the magnetic potential.
- **Visual.** Contours of the magnetic potential a with X-points (crosses) and O-points (dots) marked, reference vs generated variants; a check badge 'saddles = extrema on the torus (Poincare-Hopf)'.
- **On screen.** per-variant X-point counts; chip '8 samples per variant: provisional'
- **Assets.** none (new animation)
- **Data.** `data/x5_xpoints.json`, `experiences/resultats/e2_echantillons.npz`
- **Flags.** P20: no topology metrics were computed in the report
- **Sources.** R:739, T:872-876
- **Regeneration hook.**
  - scene data: `data/x5_xpoints.json`
  - upstream: experiences/resultats/e2_echantillons.npz (8 samples x variants at eta = 0.00951); later palier1 / tier-1 MFF fields
  - provisional run (now, CPU): new extractor xpoints(): reconstruct a on 32^2 (or 64^2 by zero-padding) and count critical points (CPU, minutes; code to write)
  - final run: same metric on palier1_mhd2d and tier-1 data (T:872-876, T:902)
  - extractor: tools/extract_data.py: xpoints() (to write)
  - criterion: distribution of X-point counts generated vs reference (T:872-876)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

### X1. Inside the twisting box (E3 in depth)

`L4` · 1:55 · inserted after X5a · was X1.1-X1.3 · 3 scenes: 3 READY, 0 PROVISIONAL, 0 PENDING

- **Learning goal.** See how the 3D solver is validated, what the dominant mode looks like, and how precise the thresholds are: the provenance of Bet 1.
- **Takeaway (one sentence).** The 3D test bench passes an exact check and recovers the known windows, with honest limits on precision.

#### X1.1 A built-in answer key  
`L4` · 35 s · **READY** · NIGHT · render flat · was X1.1

- **Key idea.** B = u is an exact eigenmode of the ABC flow decaying at -1/Rm, so the dominant rate can be no lower than -1/Rm = -0.5 at Rm = 2; the solver finds -0.5001.
- **Visual.** A gauge lands on -0.5001 next to the exact bound -0.5.
- **On screen.** 'exact mode: -1/Rm = -0.5 · dominant rate >= -0.5 · measured: -0.5001' (B8)
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e3_abc.json#taux`
- **Sources.** R:1116

#### X1.2 The mode in 3D  
`L4` · 45 s · **READY** · NIGHT · render webgl · was X1.2

- **Key idea.** The dominant mode (least damped or fastest growing) at Rm 8, 12, 16 and 20: below, inside and just after the first window.
- **Visual.** Fat vermillion field lines and a |B| isosurface, precomputed offline (spectral upsampling, marching cubes, field-line tracing in extract_data.py -> .f32 meshes and polylines, G8), orbiting slowly; a symmetry badge.
- **On screen.** badge 'published: the first-window mode has all even symmetries of a 24-element group (Bouya and Dormy 2013); not checked on these modes' (B7); no second-window mode is stored
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e3_modes.npz`
- **Sources.** R:1077, R:1092, R:1120

#### X1.3 How sure are the thresholds?  
`L4` · 35 s · **READY** · NIGHT · render flat · was X1.3

- **Key idea.** 48^3 agrees at Rm 12; at 17.5 the sign flips between resolutions, so it is unresolved; the third threshold is known to about one unit.
- **Visual.** Zoom on Rm = 17.5 with three tiny markers straddling zero (+2.3e-4 and -2.2e-4 at 32^3, -5.2e-4 at 48^3); the 48^3 check markers moved here from 03.4 (F3); divergence gauge 3e-19 to 1.5e-16.
- **On screen.** '48^3: s = 0.00812 at Rm 12 (agrees) · at 17.5: +2.3e-4 (32^3) vs -5.2e-4 (48^3): unresolved' (B9)
- **Assets.** none (new animation)
- **Data.** `experiences/resultats/e3_abc.json#convergence`
- **Sources.** R:1114, R:1118, D:197

### X4b. Steep slopes and the branch

`L5` · 0:25 (0:40 with results) · inserted after 10.5 · was X4.4 · 1 scenes: 0 READY, 0 PROVISIONAL, 1 PENDING

- **Learning goal.** Know the square-root bound near a supercritical threshold and the branch-conditioning conjecture near a subcritical one.
- **Takeaway (one sentence).** Near a subcritical threshold, conditioning on the branch could remove the smoothing error; it is a bet.

#### X4.4 Steep slopes and the branch  
`L5` · 25 s now / 40 s with results · **PENDING** · NIGHT · render flat · was X4.4

- **Key idea.** Near a supercritical threshold a smooth generator obeys a square-root bound (Prop. 2.36); near a subcritical one, conditioning on the branch could remove it (Conjecture 2.38).
- **Visual.** READY anchor: a hysteresis loop drawn by a knob going up then down on the Taylor-Green picture of 10.5; two branches; an empty seat for 'error at threshold with vs without branch conditioning'.
- **On screen.** Prop. 2.36; Conjecture 2.38; criterion 'error at threshold / 2 with branch conditioning'
- **Assets.** none (new animation)
- **Data.** `data/x4_branch.json`
- **Sources.** T:768-788, T:917
- **Regeneration hook.**
  - scene data: `data/x4_branch.json`
  - upstream: tier-2 full-scale campaign with hysteresis runs (Taylor-Green, up and down sweeps) + branch-conditioned model and its evaluation
  - final run: not configured beyond palier2_tg3d / train_fm3d (T:912-918; about 3900 GPU h for tier 2)
  - requires: 10.5 final run; a hysteresis campaign (not configured)
  - extractor: tools/extract_data.py: branch_conditioning() (to write)
  - criterion: error at the threshold divided by 2 with branch conditioning (T:917 (d))
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

### X3b. The crowd law in 3D

`L5` · 0:25 (0:35 with results) · inserted after 10.7 · was X3.5 · 1 scenes: 0 READY, 0 PROVISIONAL, 1 PENDING

- **Learning goal.** See the 3D version of the crowd-loss experiment as a bet with an adapted criterion.
- **Takeaway (one sentence).** The crowd loss must be tested again in 3D, against a control run, without narrowing the dissipation.

#### X3.5 Bet: the crowd law in 3D  
`L5` · 25 s now / 35 s with results · **PENDING** · NIGHT · render flat · was X3.5

- **Key idea.** Does the distribution-level budget loss still help in 3D, without narrowing the dissipation, against a control run of equal length?
- **Visual.** READY anchor: the three-lane race of 08.5 redrawn as empty seats for the 3D model: budget residual before / after, control lane, dissipation-spread gauge (needs a new metric). Saturated runs only (A8).
- **On screen.** 'bet adapted from the tier-1 criteria (the plan sets none for 3D): residual down, sigma(eps)/sigma_ref in [0.8, 1.2], control gains nothing' (A9, D4)
- **Assets.** none (new animation)
- **Data.** `data/fm3d_stationarity.json`
- **Flags.** RISK: stationarity-loss variance in 3D (T:992)
- **Sources.** CFG train_fm3d.yaml:13-15, C:166, T:903, T:917
- **Regeneration hook.**
  - scene data: `data/fm3d_stationarity.json`
  - upstream: second fm3d model fine-tuned with the stationarity loss + control run (weight 0) + evaluation JSONs (residu_bilan_total, dist_energie, plus a per-sample spread of the budgets, NOT computed by milady.eval today: C:166); stationarity flags from 10.5
  - final run: python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml --init-from <final.pt> --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0; same command with the loss weight set to 0 for the control (key name to check in train_fm3d.yaml); python -m milady.eval ... --out <file> for both
  - requires: 10.7 final fm3d model; sigma(dissipation) metric in milady.eval
  - extractor: tools/extract_data.py: fm3d_stationarity() (to write) + add the sigma(dissipation) metric to milady.eval in the compute clone
  - criterion: adapted from tier-1 criteria (b) budget residual < 5% at parameters without data and (d) dissipation spread ratio 0.8-1.2 (T:903); the plan's tier-2 criteria set no budget target (T:917); control run gains nothing; saturated runs only
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

### X6. Walls, metals and meshes

`L5` · 4:00 (4:25 with results) · inserted after 10.9 · was X6 + X1.4 · 7 scenes: 5 READY, 0 PROVISIONAL, 2 PENDING

- **Learning goal.** Meet the specialist frontier: conventions for Rm, gauges in bounded domains, permeability jumps, vacuum matching, hybrid meshes, VKS and DRESDYN bets, and downstream assimilation.
- **Takeaway (one sentence).** Leaving the periodic box changes what 'exact' means, and the real tests (VKS, DRESDYN) are written down as bets.

#### X6.0 Which Rm?  
`L5` · 25 s · **READY** · NIGHT · render flat · was X1.4

- **Key idea.** Published VKS thresholds depend on the definition of Rm; a model conditioned on Rm must fix its convention.
- **Visual.** The same VKS impeller with labels sliding on: about 31 with the impeller efficiency factor K, 52-71 without it; a third card 'another definition (Miralles et al. 2013)' without a number (B15).
- **On screen.** 'Rm_c ~ 31 (Monchaux 2007, with K) · 52-71 (Nore 2018, without K) · Miralles 2013: another definition'
- **Assets.** `figures/vks/figure/out/vks-en.svg`
- **Data.** none
- **Flags.** SITE NOTE: P3:1167 gives 'Rm_c ~ 44 (Miralles)' while P3:1202 converts Miralles to about 1.05 x Nore; the film omits 44 (decision D19)
- **Sources.** R:141, P3:1202

#### X6.1 A gauge for a bounded world  
`L5` · 45 s · **READY** · PAPER · render flat · was X6.1

- **Key idea.** In a bounded domain the vector potential needs a fixed gauge (Coulomb, with A.n = 0 or A x n = 0), or its distribution is not well defined.
- **Visual.** The periodic box rounds into a cylinder; potential arrows at the wall snap to the boundary condition; two gauge choices side by side; the projector motif (M6) returns (E4).
- **On screen.** div A = 0, A.n = 0 or A x n = 0 (Amrouche-Seloula)
- **Motifs.** M6 projector
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** R:339, T:211-260

#### X6.2 Iron changes the rules  
`L5` · 40 s · **READY** · PAPER · render flat · was X6.2

- **Key idea.** Across a permeability jump, B.n and tangential B/mu_r are continuous: the potential has a kink; matching to vacuum outside is linear but nonlocal.
- **Visual.** An iron disc interface: field lines refract; the potential profile shows a kink; an exterior potential field wraps the cylinder.
- **On screen.** Prop. 2.6; Remark 2.5; chip 'vacuum matching without a Laplace solve per sample: a candidate route, an open sub-question of Q1' (C11)
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** T:114-115, T:259-266, T:272

#### X6.3 Two scalars and a hybrid mesh  
`L5` · 40 s · **READY** · PAPER · render flat · was X6.3

- **Key idea.** Poloidal-toroidal storage (Prop. 2.8) in the box; SFEMaNS data are azimuthal Fourier modes times meridian finite elements, where div B is only weakly controlled.
- **Visual.** A meridian triangle mesh revolves into Fourier modes; a divergence gauge relabels itself 'with the solver's operator'.
- **On screen.** Prop. 2.8; MFF extension milady_fourier_fe; 'native SFEMaNS reader not implemented'
- **Assets.** none (new animation)
- **Data.** none
- **Flags.** P16 operator caveat
- **Sources.** T:324, T:341, R:1185, milady/data/convert.py:9-12

#### X6.4 Bet 4: VKS in the generator  
`L5` · 30 s now / 45 s with results · **PENDING** · NIGHT · render webgl · was X6.4

- **Key idea.** With consortium data, the generator should reproduce the dominant POD modes, the bimodal and asymmetric (D, Q) law, and a Rice rate within the Poisson interval.
- **Visual.** READY anchor: the VKS cylinder. An empty (D, Q) density frame (dashed), four empty POD bars with 10% bands, a Rice gauge with a Poisson interval.
- **On screen.** criteria (a)-(d) of the PhD plan; joint mirror R_pi flips the asymmetry parameter (Prop. 2.24)
- **Assets.** `figures/vks/figure/out/vks-en.svg`
- **Data.** `data/tier3_vks.json`
- **Flags.** CAVEAT: data not public (P3)
- **Sources.** T:927-939
- **Regeneration hook.**
  - scene data: `data/tier3_vks.json`
  - upstream: SFEMaNS / LATU VKS simulations (non-public): 384^3-equivalent snapshots ~1.4 GB each, 2000 snapshots ~2.7 TB; filtered 128^3 ~100 GB; MFF grid_type fourier_fe_axisym
  - final run: consortium data access; SFEMaNS reader (to write); training and evaluation as tier 2 (about 3200 GPU h, T:968)
  - extractor: tools/extract_data.py: tier3_vks() (to write)
  - criterion: 4 POD energy fractions within 10%; (D, Q) distribution distance < 2x floor; interface residual < 1%; Rice in 95% Poisson CI (T:939)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists. Fallback: figures/vks schematic + Gissinger 'pocket dynamo' proxy (SCHEMATIC).
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### X6.5 Bet 5: DRESDYN, the precession knob  
`L5` · 25 s now / 35 s with results · **PENDING** · NIGHT · render webgl · was X6.5

- **Key idea.** From generated velocity fields, recover the dynamo threshold Rm_c(Po) and the symmetry class of the dominant mode at a Po without data.
- **Visual.** READY anchor: the precessing cylinder (green Po knob). An empty Rm_c(Po) chart with a 10% band and a symmetry-class badge left blank.
- **On screen.** criteria (a)-(b) of the PhD plan; qualitative reference Botez et al. 2026
- **Assets.** none (new animation)
- **Data.** `data/tier4_dresdyn.json`
- **Sources.** T:941-953, S:100
- **Regeneration hook.**
  - scene data: `data/tier4_dresdyn.json`
  - upstream: SFEMaNS precession simulations at the partners; generated u fields + kinematic eigenvalue results per Po (format to define)
  - final run: partner data; kinematic eigenvalue solver on generated flows (about 1200 GPU h for tier 4, T:968)
  - extractor: tools/extract_data.py: tier4_dresdyn() (to write)
  - criterion: Rm_c within 10% and correct symmetry class at a Po without data (T:941-953)
  - ships now as: an 'empty seat': dashed grey chart frame, axes labelled, success band shaded, grey data tag; pending narration states the bet and the criterion. No number is drawn until the data file exists.
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### X6.6 Downstream: assimilation with a mirror  
`L5` · 35 s · **READY** · NIGHT · render flat · was X6.6

- **Key idea.** A generator as a prior: the reduced drift by conditional expectation (Prop. 2.40); with a mirror-symmetric prior, a dipole observation near zero gives a posterior with two mirror humps whose mean is not a physical state (Prop. 2.41).
- **Visual.** Observation dots near zero pull a violet ensemble; the posterior splits into two mirror humps and its mean marker falls between them, on no physical state; a lopsided prior would wrongly favour one hump; an equivariant prior handles it exactly (symmetric pairs, or a latent 4D-Var started from z and S z) (A1).
- **On screen.** Prop. 2.40; Prop. 2.41 (i)-(ii)
- **Motifs.** M10 mirror callback
- **Assets.** none (new animation)
- **Data.** none
- **Sources.** T:816-843

### X5b. The bill and the plan

`L5` · 1:15 (1:25 with results) · inserted after X6 · was X5.5-X5.6 · 2 scenes: 1 READY, 0 PROVISIONAL, 1 PENDING

- **Learning goal.** See the compute bill, its uncertainty and the 36-month plan on one page.
- **Takeaway (one sentence).** The bill is estimated with at least a factor-two uncertainty, and every estimate will be replaced by a measured number.

#### X5.5 The bill  
`L5` · 30 s now / 40 s with results · **PENDING** · BLUEPRINT · render flat · was X5.5

- **Key idea.** The plan budgets about 1.1e4 A100 GPU hours, with an uncertainty of at least a factor of two; measured costs will replace the estimates.
- **Visual.** Stacked bar per tier (tier 1 ~700, tier 2 ~3900, tier 3 ~3200, tier 4 ~1200, 20% reserve) with a dashed second bar for measured hours, filled from the catalog.
- **On screen.** 'plan: ~1.1e4 GPU h, uncertainty at least x2 · anchor: PCDM ~1150 GPU h' (C11)
- **Assets.** none (new animation)
- **Data.** `data/x5_compute_bill.json`
- **Sources.** T:955-974
- **Regeneration hook.**
  - scene data: `data/x5_compute_bill.json`
  - upstream: GPU solver benchmarks + catalog wall_time_s per campaign and per training run
  - final run: python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50 (IR:436); catalog SQL on simulation.wall_time_s (C:143-147)
  - extractor: tools/extract_data.py: compute_bill() (to write)
  - criterion: within the plan's band of at least a factor of two (T:974)
  - ships now as: planned numbers only (T:955-974), each chip 'estimate'
  - narration: two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)

#### X5.6 The plan on one page  
`L5` · 45 s · **READY** · NIGHT · render flat · was X5.6

- **Key idea.** 36 months, three axes, five tiers, three papers, named risks; chosen after scoring six directions.
- **Visual.** The thesis timeline SVG animated bar by bar (tiers, visits, committees, code releases, papers at months 10, 22, 33); risk cards; a small score table (A 4.10, B 3.90, merged).
- **On screen.** 'papers: month 10 (distributional constraints) · 22 (hard constraints in bounded domains) · 33 (reversals and threshold)'
- **Assets.** `figures/plan-these/figure/out/plan-these-en.svg`, `en/these/index.qmd`
- **Data.** none
- **Flags.** CAVEAT: independent proposal, not requested or validated by the supervisors (P27, B13)
- **Sources.** T:1014-1126, S:418-453, T:988-1000

## 7. Regenerable sections index

| Scene | Cut | Status | Scene data | Exists now | Now / with results | Provisional run (CPU, now) | Final run | Requires |
|---|---|---|---|---|---|---|---|---|
| X4.2 A bound from thresholds | extension | PROVISIONAL | `data/x4_rice_levels.json` | no | 40 s / 40 s | new extractor rice_levels(): level-a crossing rates on re-integrated Gissinger trajectories + Rice at level a on generated samples (CPU, minutes; code to write) | tier-0 campaign with 1e6 snapshots per parameter and 3 seeds (T:878-890, CPU, about 1e3 h assumption) | - |
| X4.5 Tier 0, the next round | extension | PROVISIONAL | `data/x4_tier0.json` | no | 30 s / 35 s | run experiences/e1_gissinger.py from a working copy with seeds {0, 1, 2} (seeds are fixed in code; about 3-4.5 h CPU: X:71 gives 2-3 h for two seeds, unless the seed-0/1 caches in cache_e1 are reused) (C12), then experiences/digest.py | tier-0 plan (T:878-890); DQVU needs the published coefficients (Bousquet et al. 2026 appendix); no DQVU code in the repository | - |
| 10.3 First product off the line | core | PROVISIONAL | `data/palier1_sweep.json` | no | 15 s / 15 s | make sweep CONFIG=infra/configs/palier1_mhd2d.yaml  (CPU; the campaign as configured; same workload as the E2 data, about 30 min, X:69) | tier 1 at full scale (128^2, 8 x 8 (nu, eta) grid, about 700 GPU h, T:898-904): not configured yet | - |
| X5.3 The life of one campaign | extension | PROVISIONAL | `data/x5_campaign_trace.json` | no | 40 s / 40 s | same run as 10.3 (make sweep CONFIG=infra/configs/palier1_mhd2d.yaml), then python -m milady.catalog sims --campaign palier1_mhd2d | the same trace on the GPU VM or Slurm cluster for a palier2 campaign | 10.3 provisional run |
| X5.4 A new instrument for the critic: counting X-points | extension | PROVISIONAL | `data/x5_xpoints.json` | no | 35 s / 35 s | new extractor xpoints(): reconstruct a on 32^2 (or 64^2 by zero-padding) and count critical points (CPU, minutes; code to write) | same metric on palier1_mhd2d and tier-1 data (T:872-876, T:902) | - |
| 10.4 Bet 1: the ABC windows at 64^3 | core | PROVISIONAL | `data/palier2_abc3d.json` | no | 40 s / 45 s | copy infra/configs/palier2_abc3d.yaml to $RUNS/configs/palier2_abc3d_n48.yaml with grid.N: 48, name: palier2_abc3d_n48_provisional and sweep Rm: [8, 8.5, 9, 9.5, 17, 17.25, 17.5, 17.75, 18, 26, 26.5, 27, 27.5, 28] (a list, as in palier2_tg3d.yaml); python -m milady.sweep <copy> --scheduler local --max-parallel 2 --device cpu, after --dry-run; duration unmeasured (time one point first). Not at 32^3: it would redraw the E3 curve (H5) | make sweep CONFIG=infra/configs/palier2_abc3d.yaml  (64^3, integer Rm 4-40; estimate ~15 h serial on 2 CPU threads, or GPU / Slurm array) + a copy with Rm: [17.25, 17.5, 17.75] (decision D17) | - |
| 10.5 Bet 2: a dynamo that saturates (Taylor-Green) | core | PROVISIONAL | `data/palier2_tg3d.json` | no | 40 s / 45 s | copy infra/configs/palier2_tg3d.yaml to $RUNS/configs/palier2_tg3d_n32.yaml (grid.N: 32, new name); python -m milady.sweep <copy> --scheduler local --device cpu --indices <Re <= 100, read the order with --dry-run>  (estimate 1-1.5 h, unmeasured; check resolution) | make sweep CONFIG=infra/configs/palier2_tg3d.yaml  (64^3, GPU, 10 h limit per simulation; estimate ~8 h CPU for all 12); longer t_burn / t_keep near the threshold if decision D18 says so | - |
| X4.4 Steep slopes and the branch | extension | PENDING | `data/x4_branch.json` | no | 25 s / 40 s | none | not configured beyond palier2_tg3d / train_fm3d (T:912-918; about 3900 GPU h for tier 2) | 10.5 final run; a hysteresis campaign (not configured) |
| 10.7 What must be measured | core | PENDING | `data/fm3d_eval.json` | no | 25 s / 40 s | none | make train CONFIG=infra/configs/train_fm3d.yaml NGPUS=4 (GPU); make eval CONFIG=infra/configs/train_fm3d.yaml [MODEL=<uuid>] EVAL_ARGS="--out eval_fm3d.json" (val point Re 100, Pm 1; test point Re 50, Pm 2: CFG train_fm3d.yaml) | 10.5 final run (palier2_tg3d at 64^3); final fm3d training |
| X3.5 Bet: the crowd law in 3D | extension | PENDING | `data/fm3d_stationarity.json` | no | 25 s / 35 s | none | python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml --init-from <final.pt> --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0; same command with the loss weight set to 0 for the control (key name to check in train_fm3d.yaml); python -m milady.eval ... --out <file> for both | 10.7 final fm3d model; sigma(dissipation) metric in milady.eval |
| 10.9 The top steps: VKS and DRESDYN | core | PENDING | `data/tier3_vks.json + data/tier4_dresdyn.json` | no | 30 s / 45 s | none | consortium data access; native SFEMaNS reader to write (milady/data/convert.py:9-12); then train / eval as tier 2 | - |
| X6.4 Bet 4: VKS in the generator | extension | PENDING | `data/tier3_vks.json` | no | 30 s / 45 s | none | consortium data access; SFEMaNS reader (to write); training and evaluation as tier 2 (about 3200 GPU h, T:968) | - |
| X6.5 Bet 5: DRESDYN, the precession knob | extension | PENDING | `data/tier4_dresdyn.json` | no | 25 s / 35 s | none | partner data; kinematic eigenvalue solver on generated flows (about 1200 GPU h for tier 4, T:968) | - |
| X5.5 The bill | extension | PENDING | `data/x5_compute_bill.json` | no | 30 s / 40 s | none | python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50 (IR:436); catalog SQL on simulation.wall_time_s (C:143-147) | - |

Cheapest-first order for the provisional runs: X5.4 X-points (minutes) → X4.2 Rice levels (minutes) → 10.3 / X5.3 palier1 sweep (~30 min) → 10.5 Taylor-Green 32^3 subset with stationarity flags (~1-1.5 h, estimate) → 10.4 ABC at 48^3 near the thresholds (hours, unmeasured: time one point first) → X4.5 E1 with three seeds (~3-4.5 h). CPU times marked 'estimate' are extrapolations from solver benchmarks; none of these runs has been launched. 10.6 needs no run (random-weight decoder computed at build time).

## 8. Production notes

- Predict beats need real silences: each paragraph of the script may carry hold_after (seconds, e.g. 3.0); build.js splits the TTS chunk at the aligned paragraph boundary, inserts silence and shifts the later cues. Test it on 01.3 first (G1).
- Sound effects: scenes export an event list (window.__EVENTS__: t, sample id, gain); build.js mixes the samples with adelay + amix under the same side-chain duck as the music; the squeal of 01.3 is timed in a narration gap (G2).
- E2 fields are 32^2: the extractor zero-pads them in Fourier space to 256^2 for display only, with the chip 'display interpolation (spectral)'; divergences are always measured on the native grid (G7).
- Isosurfaces and field lines of 3D fields (X1.2, 10.4 insets, 10.6) are precomputed offline in extract_data.py (spectral upsampling, marching cubes, field-line tracing) into compact .f32 meshes and polylines; scenes only draw them (G8).
- Benchmark one 6-s full-screen fragment shader on SwiftShader before committing to any shader-based background; 01.1 uses a Canvas 2D advected texture instead (G5).
- Regenerable scenes declare `requires` in the index; add a `make plan` check that refuses to render a result variant whose upstream is missing (H7). 11.1 and 11.2 depend on every regenerable data file, so they re-render whenever one changes (H2).
- Durations: duration_s is the scene as it ships now (pending variant for PENDING scenes, provisional data for PROVISIONAL scenes, assuming decision D4 = yes); duration_result_s is the length once the final data exist (H3).
- Keep the symbol sheet (section 2) in the script file and lint the script against it (D3).
- Prototype script proto/script/demo_script.json, scene d_e1_rate, says the generative model 'reproduces the whole curve': this overclaims (42% error near the threshold). Use the 09.1 wording instead.
- Prototype extractor palier1_eta_sweep() labels the E2 'recalage' series 'recalibrated'; 'recalage' is per-sample rescaling, the degenerate method of Corollary 6. Do not reuse that stand-in; 10.3 uses data/palier1_sweep.json from the real campaign, and draws the injection as the flat Ito line it is.
- The site's taxonomy figure uses blue for 'true for each sample'; redraw it (08.6) so blue keeps meaning velocity u.
- The 3D evaluation does not compute the per-sample spread of the budgets (C:166); add it before X3.5 can show a result.
- 09.3 reads experiences/resultats/cache_e1/e1_echantillons_complet.npz, which is gitignored and present only on this machine: copy it into the film project's data before moving the build elsewhere.
- Every PENDING scene ships as an 'empty seat' with a READY anchor visual (part of the story), not as the hatched AWAITING preview, which is for drafts only. A PENDING scene whose data file appears is promoted to PROVISIONAL automatically and stamped PROVISIONAL DATA until a human marks it READY in the script.

## 9. Changes after review

**In numbers.** Version 1: core cut 39:59 (73 scenes), extended cut 59:54, 104 scenes (89 READY, 8 PROVISIONAL, 7 PENDING). Version 2: core cut 40:55 now, 41:35 with results (73 scenes), extended cut 59:15 now, 60:45 with results, 105 scenes defined (91 READY, 7 PROVISIONAL, 7 PENDING), of which the extended cut plays 104 (10.8 is replaced there by X6.1-X6.2).

**Outcome counts.** accuracy review: 39 applied, 1 partly applied; pedagogy review: 65 applied, 5 modified.

**How the accuracy review was checked.** Each item was verified against the cited site lines, configs, code or result files before it was applied (the note says what was checked). No item was found wrong in substance. Two carried a wrong detail, corrected here: A8 cites T:992, which is about the variance of the stationarity loss, but the concern stands on the Taylor-Green config alone; C13 says `ref|0.9` holds 4,000 points, but it holds 8,000 (about 21 in the Rice strip), and the cache has no 20,000-sample reference set. One item (B15) exposed an inconsistency in the site itself (P3:1167 vs P3:1202), raised as question D19; the site was not modified.

**Structural changes.**

- Ids renamed: chapters ch00-ch11 (no collision with the report's classes C1-C4), core scenes NN.k; each scene keeps 'was'.
- Hook: the needle flips at about 7 s, the two questions arrive at about 0:34; the opening narration fits the scene budgets.
- Old C2 and C3 interleaved so the ladder climbs: ch02 (race, Rm, sodium, three tanks, VKS flips; all L1), ch03 (equation, windows, knob panel, the question; all L2). The disclaimer card became a lower-third inside 03.7.
- Old C7 split in two chapters, known system first: ch07 'The mirror and the crowd' (E1, opens with the lopsided machine moved from C6), ch08 'Fields have stricter laws' (E2, opens with the new scene 08.1 that introduces the 2D test bench). The taxonomy shelves start empty and become the payoff (08.6).
- ch10: 10.6 'What is guaranteed' is READY (no longer a fake bet); new READY core scene 10.8 'Walls and iron' (L5); 10.3 shortened to 15 s; every seat has a READY anchor and two durations.
- Extensions re-anchored at scene level so the ladder only climbs: X2 → X3a after ch08; X4a after ch09; X5a → X1 after 10.3; X4b after 10.5; X3b after 10.7; X6 → X5b after 10.9 (bridge). X1.4 moved to X6.0; new X3.0 holds the distance formula.
- Release model for pending results: a stand-alone 'Results update' episode plus a v2 of the film; the closing has a results-in variant.

### Accuracy review (`critique_accuracy.md`)

| Item | Where (v2 ids) | Outcome | What was checked or changed |
|---|---|---|---|
| A1 | X6.6 | applied | Verified T:831-843: a symmetric prior gives the two humps; wording and visual inverted accordingly. |
| A2 | 10.4, D17 | applied | Verified CFG palier2_abc3d.yaml:36 (integer Rm). Bet restated as s(17) > 0 > s(18); extra points offered as D17. |
| A3 | 10.3 | applied | Verified milady/sim/run.py:256-273 (injection = np.full of the Ito rate) and R:442: flat eps_inj line, fluctuating dissipation. |
| A4 | 04.6, synopsis, ch09 takeaway, logline | applied | Verified R:321 and R:514-528: 'no timestamp and no time order'; 'plus the equations'. |
| A5 | 09.3, ch09 takeaway, closing | applied | Verified R:564 (E1 is intermediate) and R:883/R:901: steep ramp, not cliff; 'consistent with Prop. 9'; 'not bad luck' dropped. |
| A6 | 08.7 | applied | Verified R:300, R:1179, H:41: retitled 'The proposed machine', PROPOSED chip, tested pieces highlighted. |
| A7 | 10.7 | applied | Verified T:912, T:917, CFG palier2_tg3d.yaml, train_fm3d.yaml (val Re 100 Pm 1; test Re 50 Pm 2). |
| A8 | 10.5, 10.7, X3.5, D18 | applied | Verified CFG palier2_tg3d.yaml:9-10, 41-43 and the growth_rate term of train_fm3d.yaml. Evidence corrected: T:992 is about the loss's variance, not data stationarity; the concern stands on the config alone. |
| A9 | X3.5 | applied | Verified T:903 vs T:917: criterion relabelled 'adapted from tier 1; the plan sets none for 3D'. |
| A10 | 07.5, 08.5 | applied | Verified R:1035 and R:961/R:993: 'worse where it counts'; the E2 nuance lands in 08.5 lane 3. |
| B1 | 03.7 | applied | Verified H:72, S:72: project context and 'this study asks' are separate lower-thirds. |
| B2 | opening, closing, logline, D7 | applied | Verified P4:1627, R:743: 'in the dynamos we can compute'; 'between the settings that were simulated'. |
| B3 | synopsis, 02.4 | applied | Verified R:139, R:149, P3:1149: only VKS reversed; each tank's field described. |
| B4 | 01.2 | applied | Lines never start or stop; they need not close. |
| B5 | 02.1 | applied | Verified P3:281, R:137: same flow, two diffusivities; honey removed. |
| B6 | 04.5 | applied | Verified R:871, R:901: Gamma = 0.93 on screen, 'below, each start paints one whirlpool'. |
| B7 | X1.2, 03.4 | applied | Verified R:1077, R:1092 (s < 0 at Rm 8 and 20), e3_modes.npz keys Rm8/12/16/20, R:1120. |
| B8 | X1.1 | applied | Verified R:1116: the exact mode gives a lower bound on the dominant rate. |
| B9 | X1.3 | applied | Verified R:1114. |
| B10 | 08.5, X3.2 | applied | Verified R:1033: one effective sample in 500. |
| B11 | 07.3 | applied | Verified e1_gissinger.json (B test asymmetry 0.0071-0.0246, mean 0.0157) and R:839, R:873. |
| B12 | 04.4 | applied | Verified P4:1627 and the digest (0.00442 at Gamma 0.9): ~11 vs ~230. |
| B13 | 10.1, X5.6 | applied | Verified T:46-56: source wording used. |
| B14 | X5.1 | applied | Verified C:176: state 0.4 GB, peak ~15x, estimates. |
| B15 | 03.5, X6.0 (was X1.4), D19 | applied | Verified P3:1167 vs P3:1194/1202 and R:141, R:143: 44 dropped, simulation chip added; the inconsistency is in the site itself (P3:1167), raised as D19. |
| B16 | 04.3, 09.1, closing | applied | Verified R:528, R:883: crossings defined once, 'model C, seed 0'. |
| B17 | 09.2, 09.3 | applied | Verified R:883 and the digest fine grid: leak / lag / overshoot. |
| C1 | 03.1 | applied | Verified P3:254: 'carried and stretched by the flow'. |
| C2 | 03.2 | applied | Cowling chip removed with the anti-dynamo chip (E6); growth rate renamed s, 'modes may also oscillate' (R:1114). |
| C3 | 04.2 | applied | Verified R:159, R:784: crisis shown in mu, expected in Gamma. |
| C4 | 01.1 | applied | Verified P3:269, P3:1471: one EXTERNAL_FACT flag removed. |
| C5 | 00.3 | applied | Verified P3:1230. |
| C6 | 02.6 | applied | Verified R:163: numbers on a separate card. |
| C7 | 07.4 | applied | Verified R:873, R:875. |
| C8 | 05.3 | applied | Verified R:883. |
| C9 | 06.3 | applied | Trajectories drawn with t on the horizontal axis. |
| C10 | 10.2, X5.2, X2.4 | applied | Verified C:93 and R:401. |
| C11 | 10.8, X6.2, X5.5 | applied | Verified T:259-266 and T:974. |
| C12 | X4.5, 03.6 | applied | X:71 is for two seeds; three seeds estimated at 3-4.5 h. Terabytes chip added. |
| C13 | 04.6, 05.2 | partly applied | Key fixed to ref|0.9. Correction to the review: ref|0.9 holds 8,000 points (not 4,000), about 21 in |D| < 0.2, and the cache has no 20,000-sample reference set; the dense strip comes from a re-integrated trajectory instead. |

### Pedagogy and production review (`critique_pedagogy.md`)

| Item | Where (v2 ids) | Outcome | What was checked or changed |
|---|---|---|---|
| A1 | 00.1-00.4, opening | applied | Needle flips at ~7 s; questions at ~0:34 (C0.3 and C0.4 merged into 00.3). |
| A2 | 00.2, 00.4, opening, 11.2 | applied | Budgets re-cut to match the cue map (7 s and 30 s); the closing scene gets 70 s for its 155 words. |
| A3 | 00.2 | applied | Narration describes the visual. |
| A4 | 00.3 | applied | 'every few hundred thousand years, irregularly'. |
| A5 | 00.3 | applied | True barcode: solid vermillion vs near-background. |
| A6 | 00.4, 03.7 | applied | Violet-cloud teaser and promise-card cloud. |
| B1 | 08.1 (new) | applied | E2 introduced before its first predict beat. |
| B2 | ch02, ch03 | applied | Reordered: race and Rm, then sodium and VKS (L1), then the equation and windows (L2); 02.3 lowered to L1. |
| B3 | 08.4, X2.2 | applied | Intuitive spring at L3; the formula lives only in X2.2. |
| B4 | 07.4, X2.5 | applied | No L-phi or degrees in the core. |
| B5 | 04.5 | applied | 'long-exposure glow (stationary distribution)'. |
| B6 | 06.5, 07.5 | applied | Earth-mover beat names W1; Lip(phi); KL only on the formula layer. |
| B7 | 10.8 (new), D3 | modified | Merged X6.1 + X6.2 into the core as 10.8 (READY, L5) instead of moving X4.3, which would have broken the climbing ladder; the flagship question goes to D3 with the extended cut recommended. |
| B8 | 01.3 | applied | Staircase of bars 'B x (gain / loss)' -> e^(s t). |
| C1 | 07.1, 08.6 | applied | Shelves empty at the start of ch07, filled by predict beats, formal row only at the end of ch08. |
| C2 | 07.2 | applied | 'built into the machine, acts on the crowd'; mirror on the crowd shelf, tag 'built in, exactly'. |
| C3 | 03.3 | applied | Motivating line for the ABC flow. |
| C4 | 03.8, 04.1 | applied | Bridge sentence into the three-dial model. |
| C5 | 01.2 | applied | Cut-magnet surprise first. |
| C6 | 06.2 | applied | 'Two clocks' moved before the formulas. |
| C7 | 05.3, 09.1 | applied | Cumulative error defined once as a shaded area. |
| D1 | all | applied | Growth rate s; lambda only for the knob (symbol sheet). |
| D2 | all | applied | 'distribution distance' everywhere; technical name on a chip in 06.5 and in X3.0. |
| D3 | 04.1, 05.2, X3.1, X4.2, 03.5 | applied | Numbers for Gissinger coefficients, r_0 / r / r_a, q*, 'iron'. |
| D4 | 04.7, 08.5, X3.5 | applied | eps for dissipation. |
| D5 | 04.3 onward | applied | 'crossing rate' after one definition. |
| D6 | all ids | applied | Chapters ch00-ch11, scenes NN.k; every scene keeps its version-1 id in 'was'. |
| E1 | 03.3, 03.7, 04.1, 08.1, 10.1 | applied | Staircase planted in 03.7, lit tier by tier, paid off in 10.1. |
| E2 | 09.3 | modified | Renamed 'A stiff sheet on a steep ramp': 'cliff' was rejected by accuracy A5, 'staircase' collided with M7. |
| E3 | 06.4, 09.1 | applied | Shoebox filled by generated photos; toll counter returns with violet cars. |
| E4 | 10.6, X6.1 | applied | Projector reused. |
| E5 | 03.1, 05.2, 06.3, 07.6, 09.3 | applied | Pen beats scheduled. |
| E6 | 03.2, 08.1 | applied | Anti-dynamo chip removed from 03.2; narrated payoff in 08.1. |
| E7 | conventions, 00.1 | applied | Needle only when D is on screen; rail on the left, at chapter cards and checkpoints only. |
| E8 | 01.6, 03.8, 05.5, 08.7 | applied | Checkpoints end on an open question. |
| E9 | 08.7, 09.6 | applied | Recaps merged; framework panels a, b, d only. |
| F (table) | durations | applied | Overrun scenes re-budgeted or trimmed (00.4, 01.3, 03.2, 03.5, 05.4, 06.5, 08.2, 07.2-07.3, 07.5, 08.5, 09.6, 10.3). |
| F1 | ch07, ch08 | applied | C7 split: ch07 'The mirror and the crowd' (E1), ch08 'Fields have stricter laws' (E2). ch08 opens with a declared side-step L4 -> L3 on the rail (new test bench). |
| F2 | 03.2 | applied | One idea; 'the field pushes back on the flow'. |
| F3 | 03.4, X1.3 | applied | Rounded thresholds; 48^3 markers moved. |
| F4 | 03.7, 11.3 | applied | Disclaimer folded into a lower-third with one spoken sentence; full text on the end card. |
| F5 | 02.6, 04.3 | applied | Plain-language rates; exact values on the formula layer. |
| F6 | 03.7, 05.3, 08.6, 09.1 | applied | Three promise cards ticked off on screen. |
| F7 | 10.3, X5.3 | modified | Kept as a separate 15-s PROVISIONAL scene instead of a beat inside 10.2, so 10.2 stays READY and the regenerable part stays isolated; the full sweep moved to X5.3. |
| F8 | 09.6 | applied | Scoreboard and lessons merged (40 s). |
| G1 | production notes | applied | hold_after per paragraph. |
| G2 | production notes, D10 | applied | SFX event track; squeal in a narration gap. |
| G3 | 00.1, 11.2 | applied | Stylized compass, no hand. |
| G4 | 00.2 | applied | Layered 2D zoom; WebGL only for the last 3 s. |
| G5 | 01.1, production notes | applied | Canvas 2D churn; shader benchmark before any shader background. |
| G6 | 11.2 | applied | Sequenced montage, one motif per sentence. |
| G7 | 08.1, 08.2, production notes | applied | Spectral zero-padding for display only. |
| G8 | X1.2, 10.4, production notes | applied | Meshes and polylines precomputed offline. |
| G9 | 10.5 | applied | Render class flat; 3D insert as a separate shot. |
| H1 | results-update cut, D5 | applied | Stand-alone 'Results update' episode plus v2 of the film. |
| H2 | 11.1, 11.2, closing | applied | Closing paragraph 3 has two variants; both scenes depend on every regenerable file. |
| H3 | 10.4-10.9, X3.5, X4.4, X5.5, X6.4, X6.5 | applied | READY anchor in every seat; two durations per regenerable scene. |
| H4 | 10.6, 10.7 | applied | 10.6 'What is guaranteed' is READY (random-weight decoder, no run); 10.7 'What must be measured'. |
| H5 | 10.4 | applied | Provisional run at 48^3 near the thresholds, not 32^3. |
| H6 | 10.2 | applied | One sentence explains stamps. |
| H7 | regenerable index | applied | `requires` column added. |
| H8 | 10.9 | applied | Extended-cut entry 10.9-bridge (15 s). |
| I1 | X1, X6.0 | modified | X1 anchored before 10.4 as the provenance of Bet 1; X1.4 kept but moved to X6 as X6.0 (the three Rm definitions left 03.5), with 44 dropped (B15). |
| I2 | X3b | applied | X3.5 after 10.7. |
| I3 | X4a, X4b | modified | X4.4 after 10.5 as asked; X4.5 stays with X4.1-X4.3 after ch09 because the staircase is now planted in 03.7 (the review's own alternative). |
| I4 | X5a, X5b | applied | X5.1-X5.4 after 10.3; X5.5-X5.6 after X6 as the L5 finale; X5.1 raised to L4. |
| I5 | X2.2 | applied | Resolved by B3. |
| I6 | two-episode option | applied | ch07 closes Part 1; Part 2 opens on a 60-s recap. |
| J | 02.1, 01.4, 11.2, 03.7, predict ids, 01.3 | applied | Ink metaphor; words for forces and heat; closing numbers on chips; lower-third not narrated; predict beats renumbered Q1-Q8 in film order; bicycle-dynamo anchor. |
| speech rate | conventions, D21 | applied | Durations assume 125-130 effective words per minute. |

### Rejected, modified or partly applied, and why

No item was rejected outright. These were applied differently:

- **accuracy C13** (partly applied): Key fixed to ref|0.9. Correction to the review: ref|0.9 holds 8,000 points (not 4,000), about 21 in |D| < 0.2, and the cache has no 20,000-sample reference set; the dense strip comes from a re-integrated trajectory instead.
- **pedagogy B7** (modified): Merged X6.1 + X6.2 into the core as 10.8 (READY, L5) instead of moving X4.3, which would have broken the climbing ladder; the flagship question goes to D3 with the extended cut recommended.
- **pedagogy E2** (modified): Renamed 'A stiff sheet on a steep ramp': 'cliff' was rejected by accuracy A5, 'staircase' collided with M7.
- **pedagogy F7** (modified): Kept as a separate 15-s PROVISIONAL scene instead of a beat inside 10.2, so 10.2 stays READY and the regenerable part stays isolated; the full sweep moved to X5.3.
- **pedagogy I1** (modified): X1 anchored before 10.4 as the provenance of Bet 1; X1.4 kept but moved to X6 as X6.0 (the three Rm definitions left 03.5), with 44 dropped (B15).
- **pedagogy I3** (modified): X4.4 after 10.5 as asked; X4.5 stays with X4.1-X4.3 after ch09 because the staircase is now planted in 03.7 (the review's own alternative).

### Id map, version 1 → version 2

- **ch00**: 00.1 ← C0.1, 00.2 ← C0.2, 00.3 ← C0.3 + C0.4, 00.4 ← C0.5, 00.5 ← C0.6
- **ch01**: 01.1 ← C1.1, 01.2 ← C1.2, 01.3 ← C1.3, 01.4 ← C1.4, 01.5 ← C1.5, 01.6 ← C1.6
- **ch02**: 02.1 ← C2.1, 02.2 ← C2.2, 02.3 ← C3.1, 02.4 ← C3.2, 02.5 ← C3.3, 02.6 ← C3.4
- **ch03**: 03.1 ← C2.3, 03.2 ← C2.4, 03.3 ← C2.5, 03.4 ← C2.6, 03.5 ← C3.5, 03.6 ← C3.6, 03.7 ← C3.7 + C3.8, 03.8 ← C3.9
- **ch04**: 04.1 ← C4.1, 04.2 ← C4.2, 04.3 ← C4.3, 04.4 ← C4.4, 04.5 ← C4.5, 04.6 ← C4.6, 04.7 ← C4.7
- **ch05**: 05.1 ← C5.1, 05.2 ← C5.2, 05.3 ← C5.3, 05.4 ← C5.4, 05.5 ← C5.5
- **ch06**: 06.1 ← C6.1, 06.2 ← C6.4, 06.3 ← C6.2, 06.4 ← C6.3, 06.5 ← C6.5
- **ch07**: 07.1 ← C6.6, 07.2 ← C7.5 (first half), 07.3 ← C7.5 (second half), 07.4 ← C7.6, 07.5 ← C7.7, 07.6 ← C7.8
- **ch08**: 08.1 ← new (C7.b0), 08.2 ← C7.2, 08.3 ← C7.3, 08.4 ← C7.4, 08.5 ← C7.9, 08.6 ← C7.1, 08.7 ← C7.10
- **ch09**: 09.1 ← C8.1, 09.2 ← C8.2, 09.3 ← C8.3, 09.4 ← C8.4, 09.5 ← C8.5, 09.6 ← C8.6 + C8.7
- **ch10**: 10.1 ← C9.1, 10.2 ← C9.2, 10.3 ← C9.3, 10.4 ← C9.4, 10.5 ← C9.5, 10.6 ← C9.6, 10.7 ← C9.7, 10.8 ← new (merge of X6.1 + X6.2), 10.9 ← C9.8
- **ch11**: 11.1 ← C10.1, 11.2 ← C10.2, 11.3 ← C10.3
- **X2**: X2.1 ← X2.1, X2.2 ← X2.2 (+ C7.4 formula), X2.3 ← X2.3, X2.4 ← X2.4, X2.5 ← X2.5
- **X3a**: X3.0 ← new (from C6.5), X3.1 ← X3.1, X3.2 ← X3.2, X3.3 ← X3.3, X3.4 ← X3.4
- **X4a**: X4.1 ← X4.1 (+ C5.4 caveats), X4.2 ← X4.2, X4.3 ← X4.3, X4.5 ← X4.5
- **X5a**: X5.1 ← X5.1, X5.2 ← X5.2, X5.3 ← X5.3, X5.4 ← X5.4
- **X1**: X1.1 ← X1.1, X1.2 ← X1.2, X1.3 ← X1.3
- **X4b**: X4.4 ← X4.4
- **X3b**: X3.5 ← X3.5
- **X6**: X6.0 ← X1.4, X6.1 ← X6.1, X6.2 ← X6.2, X6.3 ← X6.3, X6.4 ← X6.4, X6.5 ← X6.5, X6.6 ← X6.6
- **X5b**: X5.5 ← X5.5, X5.6 ← X5.6

## 10. Questions for the user

Decisions that remain open. Each has a default that the production will follow if you say nothing.

**D1. Narrator voice** · *open (unchanged)*. Which original narrator voice (Fish Audio reference_id) should read the film? The film will not clone or imitate any real person. The session task list mentions a voice called 'Ethan': if that is an original or licensed library voice, please confirm and give its reference_id.  
Options: an original Fish Audio library voice: we send 2-3 clips of the opening 60 s to choose from / a voice you hold the rights to (a consenting narrator). Default: send 2-3 test clips of the opening. Blocks: all narration audio, scene durations, subtitle timing.

**D2. Fish Audio access** · *open (unchanged)*. Provide FISH_API_KEY in the environment (never in a file) and confirm the validated drama-3 settings for English. The first live test will also measure the real pace and the length of a [long pause].  
Options: key now: first live test on one scene (00.1-00.4) / later: build with the placeholder voice. Default: one-scene live test first. Blocks: live narration.

**D3. Which cut is the flagship** · *open (updated: B7, I6)*. You asked for a long film that climbs to the supervisors' level. The core cut reaches L5 only briefly; the extended cut does it properly. Which ships as the main video?  
Options: extended cut as the flagship, core cut as a shorter edition from the same scenes / core cut as the flagship, extensions as a second release / two episodes (Part 1 ch00-ch07, Part 2 ch08-ch11 + extensions, with a 60-s recap). Default: extended cut as the flagship, core cut as a shorter edition. Blocks: script length, render budget, thumbnails.

**D4. Provisional CPU runs** · *open (updated: H4, H5, A8, C12)*. Launch the provisional CPU runs now, writing outside the site repository? Cheapest first: X-points on E2 samples (minutes), Rice levels (minutes), palier1 2D sweep (~30 min), Taylor-Green 32^3 subset with stationarity flags (~1-1.5 h, estimate), ABC at 48^3 near the three thresholds (hours, unmeasured: one point is timed first), E1 with 3 seeds (~3-4.5 h). The 3D decoder data of 10.6 need no run any more (built from random weights). Disk free: 8.7 GB.  
Options: yes, on this machine / yes, on the cloud VM / no, ship empty seats. Default: yes, cheapest first. Blocks: 7 PROVISIONAL scenes.

**D5. HPC timing and the release model** · *open (updated: H1)*. When might the palier2 campaigns at 64^3, the GPU fm3d training and evaluation, and VKS (SFEMaNS/LATU) or DRESDYN data be available? YouTube cannot replace a published file: when results arrive, publish a stand-alone 'Results update' episode (5-8 min) and a v2 of the full film on the site and the GitHub release, or re-upload the film?  
Options: ship now with empty seats; Results update episode + v2 later / ship now; re-upload later (views and comments lost) / hold the release until tier-2 results. Default: ship now; Results update episode + v2 later. Blocks: 7 PENDING scenes, release plan.

**D6. Supervisors on screen** · *open (unchanged)*. Name the supervisors (as listed in the public offer: S. Cheng and D. Lucor, with C. Nore and Y. Ponty) in the end-card credits, or only 'the project's supervisors' with names in the video description?  
Options: names in text, no photos, no logos, no opinions attributed / no names on screen. Default: names in text only (11.3). Blocks: 03.7 lower-third wording, 11.3.

**D7. Facts not on the site** · *open (updated: C4, B2)*. May the film use sourced external facts: seafloor magnetic stripes, the self-exciting disc, and 'no one can yet predict when Earth's field will flip' (logline)? The Curie-temperature argument is gone (replaced by the site's own 'a free field fades in ~10^4 years' argument).  
Options: yes, with on-screen reference chips and sources in the description / no: open on VKS reversals instead. Default: yes, sourced. Blocks: 00.3, 01.3, logline and the opening narration.

**D8. Formula density at L4-L5** · *open (unchanged)*. Full statements of the propositions on a separate formula layer (never in subtitles, not narrated), or words only with a pointer to the site?  
Options: formula layer, narration stays intuitive / words only + site pointer. Default: formula layer. Blocks: 07.5, 09.3, X2, X6.

**D9. Look** · *open (unchanged)*. Dark-dominant film (NIGHT about 75%, PAPER for derivations, BLUEPRINT for infrastructure) or light, closer to the site? Key-coloured field maps (silver for negative values) or a conventional red-blue map in single-field shots?  
Options: dark + key-coloured maps / light + site look / dark + red-blue maps. Default: dark + key-coloured maps. Blocks: every scene template.

**D10. Music and sound effects** · *open (updated: G2)*. Music: none, an original bed synthesized in code under L0-L2, or a licensed track? Sound effects (needle, squeal, crossing ticks, hiss) need a new SFX track in the pipeline (scene event lists mixed by build.js): keep them?  
Options: original bed under L0-L2 + SFX / SFX only / none / licensed music. Default: original bed under L0-L2, silence under L4-L5, SFX kept. Blocks: audio mix, 00.5, 01.3, 04.2, 06.1.

**D11. Frame rate, resolution, render machine** · *open (unchanged)*. 1080p30 master (render estimates in section 0), 60 fps for particle and 3D shots, or 4K (needs a bigger machine and more than 8.7 GB of disk)? Render here or on a rented VM?  
Options: 1080p30 here / 1080p30, 60 fps for heavy shots / 4K on a cloud VM. Default: 1080p30 here. Blocks: final render.

**D12. Pronunciations** · *open (updated)*. Confirm: Gissinger (French or English), DRESDYN, SFEMaNS, MilaDy, Karman, Zeldovich, Kac.  
Options: as in audio/lexicon.json / your corrections. Default: lexicon entries marked CHECK. Blocks: phoneme pins.

**D13. Title** · *open (unchanged)*. Pick a title: How Often Does the Field Flip? / Exact Where It Is Exact: physics-constrained generative models for dynamos / The Compass and the Crowd.  
Options: How Often Does the Field Flip? / Exact Where It Is Exact: physics-constrained generative models for dynamos / The Compass and the Crowd. Default: How Often Does the Field Flip?. Blocks: 00.5, thumbnails.

**D14. Disclaimer** · *open (updated: F4)*. Approve the disclaimer wording and its new placements: a lower-third with one spoken sentence in 03.7 (the separate 20-s card is gone), the full text on the end card and in the description.  
Options: as drafted / edited / keep a separate disclaimer card. Default: as drafted. Blocks: 03.7, 11.3.

**D15. Short vertical version** · *open (ids updated)*. Produce a 9:16 Short from the long version? Candidates: 07.5 (the spike) or 04.2-04.4 (whirlpools and 'when vs how often').  
Options: yes, 07.5 / yes, 04.2-04.4 / no. Default: yes, 07.5. Blocks: nothing in the long cut.

**D16. Subtitle timing** · *open (unchanged)*. Sentence-level subtitle timing (ready) or word-by-word emphasis (install a CPU aligner, about 0.5 GB)?  
Options: sentence level / word level. Default: sentence level. Blocks: subtitle style only.

**D17. How Bet 1 is settled** · *new (A2)*. The configured 64^3 ABC campaign sweeps integer Rm only, so 'the sign at Rm = 17.5' cannot be settled as written. State the bet as s(17) > 0 > s(18), or also add Rm = 17.25, 17.5 and 17.75 in a copy of the config (3 more runs)?  
Options: both: restate the bet and add the 3 points / restate the bet only / add the 3 points only. Default: both. Blocks: 10.4 wording and its final run.

**D18. Taylor-Green stationarity** · *new (A8)*. The Taylor-Green runs keep t in [100, 140] from a 1e-3 seed; near the threshold the field may still be growing. Flag and exclude non-saturated runs (no config change), or lengthen t_burn / t_keep for points near the threshold?  
Options: flag and exclude / lengthen the runs near the threshold / both: flag now, rerun longer later. Default: flag and exclude now; decide on longer runs after the first 64^3 results. Blocks: 10.5, 10.7, X3.5.

**D19. A site inconsistency** · *new (B15)*. P3:1167 says the VKS threshold reads 'Rm_c ~ 44 (Miralles)', but P3:1202 converts Miralles' definition to about 1.05 x Nore's (so about 54-75). The film drops 44 (following R:141). Fix the site page separately? (This work does not modify the site.)  
Options: yes, fix P3 (FR and EN) in a separate task / leave the site as is. Default: flag it for a separate site fix. Blocks: nothing in the film.

**D20. A needle that flips in the first 10 s** · *new (A1)*. The new hook shows the compass needle swinging to south and back at about 7 s, with the chip 'illustration, not to time scale'. Acceptable, or keep the needle still and let the stripes carry the surprise (hook at about 0:20)?  
Options: needle flip with chip / stripes carry the surprise. Default: needle flip with chip. Blocks: 00.1, opening narration.

**D21. Narration pace** · *new (pedagogy F)*. Script at about 125-130 effective words per minute (speech at about 150 plus visual breathing room) as the review recommends, which is what the durations in this outline assume?  
Options: yes, 125-130 effective wpm / tighter, about 145 wpm (shorter film). Default: 125-130 effective wpm. Blocks: script length per scene.
