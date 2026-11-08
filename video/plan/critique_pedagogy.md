# Pedagogy and production review of the outline

Reviewed: `outline.md` / `outline.json` (version 2026-11-08, 17 chapters, 104 scenes), checked against `pedagogy.md` (level ladder §0.1, motifs §3), `styles.md` §3.5 and `pipeline.md` (measured throughput, audio and subtitle chain). Asset paths: every static asset and READY data file named in the outline exists. The only missing files are the 16 regenerable `data/*.json`, which is expected. Wording rule kept: the narrator is an original voice. Nothing in this review asks for an imitation of any real person.

## Verdict

The bones are excellent: two questions at the start ("when" and "how often") that come back at the end, a picture-first climb, eight predict beats, honest caveats and a clean idea for pending results (the "empty seat"). The script should not be written yet, though. The outline has six structural faults and a dozen density faults:

1. **The hook comes too late.** The first surprise ("the field has flipped") lands at about 40 s on the visual timeline, and the two questions at about 48 s. The draft opening narration also does not fit its scene slots (C0.5 needs 25 s and has 12 s).
2. **The 2D MHD test bench (E2) is never introduced.** C7.2 drops "generated 2D MHD maps ... at η = 0.00951, model V0" on a viewer who has only met the three-dial model. This is the steepest cliff in the film.
3. **C7 is 7:25 long, opens with the formal taxonomy before any example, and contains the four most overloaded scenes.** C7.2, C7.5, C7.7 and C7.9 hold 4 to 15 numbers each and each runs 6 to 16 s over its slot.
4. **Symbols and words collide.** λ is both the growth rate and the knob. ν has four meanings, μ has four, and D is both the dipole and the dissipation. "Energy distance" (a statistic) sits next to the "energy budget" (physics) in the same scenes. The film says "flip rate" where the data are zero-crossing rates.
5. **The extended cut breaks its own ladder.** X1 sits after C2, so its L4 scene comes before C3's L1 scenes, and X1.4 uses VKS before VKS is introduced. X3.5 bets on the 3D generator before C9 shows it. X4.4 and X4.5 talk about tiers and Taylor-Green before the staircase. X5 drops from L5 back to L3 after C9.
6. **The pending sections are isolated in C9, but the release model is not.** C10.2's narration and C10.1 depend on the status of the bets. Five empty seats in a row make a monotonous C9. C9.6 is not a falsifiable bet. YouTube cannot replace a published file, so "regenerate later" needs a plan for releasing updates.

Two pipeline gaps also block faithful execution. The 3-s predict holds cannot come out of a single TTS request, and the four sound effects the outline uses have no SFX track in the pipeline.

Severity: **B** = fix before writing the script; **M** = fix before the animatic; **m** = polish.

## A. Hook and opening (C0)

| # | Sev | Scene | Problem | Fix |
|---|---|---|---|---|
| A1 | B | C0.1-C0.4 | The surprise ("it has flipped, many times, with no schedule") arrives at 0:40 of the visual timeline, and the questions at 0:48. The first 12 s are a needle settling, which is a mood and not a hook. | Put the reversal in the first 10 s. Narration: "This needle has pointed north your whole life. Rocks on the ocean floor say it has pointed south too, again and again, with no schedule." Visual: the C0.1 needle flips once at about 8 s and settles back. Then the seafloor serves as evidence (C0.3) and the two questions come at about 0:30. Keep the "hopeless / not hopeless" pair: it is the real promise. |
| A2 | B | C0.5 | The draft gives this scene 62 words (about 25 s) against a 12 s slot. C0.2 gets 3 words ("It is not.") against 8 s. Per-scene budgets do not match the cue map. | Re-budget C0.2 to 6 s and C0.5 to 25 s (or cut its last sentence to the roadmap clause). C0 becomes about 1:20. |
| A3 | M | C0.2 | Non sequitur: the visual says "the field wraps the planet" while the words say "It is not [permanent]". | Narrate the visual: "That needle follows a field that wraps the whole planet. It feels permanent. It is not." |
| A4 | m | C0.4 | `10^5 to 10^6 years` is notation on an L0 card. The ladder allows numbers only. | "every few hundred thousand years, irregularly" (or "100,000 to 1,000,000 years"). |
| A5 | m | C0.3/C0.4 | Normal and reversed stripes are two shades of vermillion on NIGHT. They will band and blur after YouTube compression, and they are weak for colour-blind viewers. | Use solid vermillion against near-background (a true barcode), with the labels kept. The polarity rule (a shade, not a new hue) still holds. |
| A6 | m | C0.5/C3.7 | The generator, the film's second protagonist, first appears at 18:09 (C6.1). Viewers who come for "AI for physics" wait 18 minutes. | Add a 3-s violet-cloud teaser to C0.5 ("machines that must be taught...") and again among the C3.7 promise chips. |

## B. Abstraction climb (ladder violations and cliffs)

Core-cut time per level (target durations): L0 about 2:05 plus the 1:15 closing, L1 about 4:15, **L2 about 9:40**, L3 about 8:45, L4 about 11:00, **L5 about 2:55**. The climb is smooth up to L3. It has one cliff (B1) and several sawtooth dips that break pedagogy rule 1 ("never go down without saying so").

| # | Sev | Scene | Problem | Fix |
|---|---|---|---|---|
| B1 | B | C7.2 | **E2 is never introduced.** A periodic square, u and B maps, a knob η, the fact that it is not a dynamo, and why it is used: none of it is on screen before the predict beat. | New scene **C7.b0 "A flat sheet of plasma"** (L3, 30 s, READY, flat): the periodic square tiles in, blue u and vermillion B maps from `e2_echantillons.npz#ref`, the green η knob (11 values, filled and open dots). The narrated anti-dynamo payoff goes here: "a flat world cannot keep a dynamo going; this is a training ground for laws, not a dynamo". The staircase lights tier 1. |
| B2 | M | C2 → C3 | The level drops from L2 (induction equation, ABC formula, curl u = u) to L1 (C3.2-C3.4). The rail says "only climbs". | Either say so on screen ("a step back to the lab"), or move C3.2-C3.4 (three tanks, VKS, VKS flips) before C2.3. That reorder works well: C1 → C2.1-C2.2 (race, Rm) → C3.1-C3.4 (sodium, tanks, VKS, VKS flips) → C2.3-C2.6 (equation, kinematic, ABC windows) → C3.5-C3.9. Rm is introduced before C3.1 needs it, and VKS flips re-hook the cold open at about 6 min. |
| B3 | M | C7.4 | An L4 PAPER scene sits between two L3 scenes. It has the same formula and remark as X2.2, so the extended cut shows it twice. | In the core cut, make C7.4 intuitive at L3, with no formula: "a spring that must become infinitely stiff at the very end; a network with bounded strength cannot". Keep the formula and Remark 3.6 for X2.2 only. |
| B4 | M | C7.1, C7.6 | `E_mu[L phi] = 0` and "degree-3 control residual" appear in the core cut, but the generator 𝓛 is L4 vocabulary (ladder §0.1) and degree-3 controls are only defined in X2.5. | Core: write "the crowd average of d(φ)/dt is zero, for every observable φ", with energy as the example. C7.6: "the lopsided model even scores best on the budget check". Keep 𝓛φ and the degrees for X2.5. |
| B5 | M | C4.5 | 'invariant measure mu_Gamma' sits on an L2 card, but it is L4 vocabulary. | Label it "the long-exposure glow (stationary distribution)". Keep μ_Γ for X2 and X4. |
| B6 | M | C7.7, C8.3 | KL, W₁ and Lipschitz bounds are on screen without ever being introduced. C7.7's `W1 >= E|L phi| / L` uses L for two different things (generator and Lipschitz constant). | One 8-s "distance between crowds" beat in C6.5 (earth-mover picture) names W₁. In C7.7, write Lip(φ). KL appears only in the formula layer, with the words "infinitely surprised". |
| B7 | M | core L5 | Substantive L5 content in the core cut is about 2:55, and most of it is empty seats. The requested climb "up to the level of the supervisors and specialists" really only happens in the extended cut. | Either make the extended cut (about 60 min) the flagship (this answers the "longue vidéo" request; see D3), or move one READY L5 scene into the core: X4.3 "Waiting times need the movie" (35 s, dense2d, READY) after C8.3, and/or a 40 s merge of X6.1 and X6.2 before C9.8. |
| B8 | m | C1.3 | `dB/dt = (gain - loss) B` is a differential equation at L1. The ladder allows one ratio and one exponential. | Show "each turn: B × (gain/loss)" as a staircase of bars that turns into e^(st). Save d/dt for C2.3. |

## C. Motivation before formalism

| # | Sev | Scene | Problem | Fix |
|---|---|---|---|---|
| C1 | B | C7.1 | The film opens its most important chapter with the formal taxonomy (C1: x ∈ ker A, C2: c(x) = 0, C3: g#μ = μ, C4: 𝔼_μ[𝓛φ] = 0) before a single example. That breaks "picture, then words, then symbols". | Make the shelves the **payoff** of C7, not its premise. Show them empty at the start with plain-language labels only ("true for every snapshot" / "true only for the crowd"). Each law is placed on its shelf as its predict beat resolves. The formal row goes in the last 10 s of C7.10 (or in X2). |
| C2 | M | C7.5 + C7.1 | Conceptual inconsistency: the mirror is a **crowd** law (single snapshots are lopsided), yet it is "built in" by an equivariant network. That looks like it contradicts "build per-sample laws in, impose crowd laws on the crowd". | Say it explicitly in C7.5: "the mirror is built into the machine, but it acts on the crowd: each snapshot stays lopsided, the crowd is balanced". Put the mirror on the crowd shelf with a "built in, exactly" tag. The takeaway should read "enforce each law at the level where it is true". |
| C3 | M | C2.5 | The ABC flow arrives with no reason given. | Add one line: "To test our tools we need a flow simple enough to write on one line, yet able to make a dynamo: physicists use this one." |
| C4 | M | C4.1 | The motivation for jumping from VKS to a three-dial caricature is implicit. | Close C3.9 / open C4.1 with: "Full simulations cost too much (C3.6). So we start with a caricature with three dials, which already flips." |
| C5 | M | C1.2 | "Lines in = lines out" in a dragged box is an abstract 30 s at L0. Its only motivation is a payoff 20 minutes later. | Open with an L0 surprise: "cut a magnet in half and you get two magnets, never a lone north pole". Then do the box. |
| C6 | M | C6.2 vs C6.4 | C6.2's formulas use t and v (transport time, generator velocity) two scenes before C6.4 explains that they are not physical time or fluid velocity. A physicist misreads C6.2. | Move C6.4 right after C6.1 (or fold it into the end of C6.1). |
| C7 | M | C5.3, C8.1, C10.2 | "Cumulative error" is never defined, yet it carries the film's headline numbers (4 %, 6 %, 14 %, 42 %). | Define it visually once, in C5.3, as the shaded area between the two curves divided by the area under the true curve. Reuse the same shading in C8.1. |

## D. Words and symbols (one meaning per mark)

| # | Sev | Scope | Clash | Fix |
|---|---|---|---|---|
| D1 | B | C1.3, C2.2-C2.6, C9.4 vs C6.2-C8.3 | λ is the growth rate in C1-C2 and the green knob from C6 on. Pedagogy §0.2 says "λ always green". | Use **s** (or σ_B) for the growth rate everywhere. Keep λ only for the knob (green), and name the specific knob (Γ, η, Rm) whenever there is one. |
| D2 | B | C6.5, C7.7, C7.9, C8.4, X3.4 | "Energy distance" (statistic, amber) sits next to "energy budget", "magnetic energy ×2.68" and "energy errors 26 %". To anyone below L4 the sentence "forcing the energy budget multiplies the energy distance by 9" is gibberish. | On screen and in narration call it the **distribution distance** (or "mismatch score"), amber. Give its technical name once, as a chip in C6.5. Never say "energy" for it. |
| D3 | M | C4.1, C3.1, C5.2/X4, C7.6, X3.1 | ν: Gissinger coefficient, viscosity, Rice rate ν₀/ν_a, tilted law ν\*. μ: Gissinger coefficient, μ_Γ, μ_r, mixtures μ±. | Show Gissinger coefficients as numbers only. Rice rate becomes r₀ (crossings) and r (reversals). Tilted law becomes q\*. μ_r is "iron (permeability)" in words until L5. Keep a symbol sheet in the script file and lint against it. |
| D4 | M | C7.9, X3.5 | `sigma(D)` means the dissipation spread while D is the dipole everywhere else. | Use ε for dissipation (C4.7 already writes E[P - ε] = 0): σ(ε)/σ_ref. |
| D5 | M | C4.3, C5, C8.1, Q8, closing | The data are **zero-crossing rates of D** (excursions included, pitfall P15), but C4.3's key idea, the C5/C8 takeaways, Q8 and the closing all say "flip rate". | Define once in C4.3: "we count every time D crosses zero; most crossings are flips, some are near-misses". Then always say "crossing rate" on screen. The closing can say "how often it flips (counted as crossings)". |
| D6 | m | production docs | Constraint classes C1-C4 share names with chapter ids C1-C4. Script writers will cross-reference wrongly. | Rename chapter ids `ch00`-`ch10` (or constraint classes `K1`-`K4` in the docs only; the screen keeps the report's names). |

## E. Motifs and callbacks

| # | Sev | Motif / scene | Problem | Fix |
|---|---|---|---|---|
| E1 | M | M7 staircase | First appears in C9.1, at minute 33. styles.md §3.5 says "end of L1 ... every chapter card". The extended modules (X4.4, X4.5, X3.5) talk about tiers before it exists. | Plant it in C3.7 as the map of the film (tiers 0-4, all grey). Light tier 0 at C4.1 (three dials), tier 1 at C7.b0 (E2), and the 3D box at C2.5/X1 as a preview. C9.1 is then a payoff ("here is where we are"), not an introduction. |
| E2 | M | C8.3 title | "A rubber sheet over a **staircase**" collides with M7, and the visual is a cliff anyway. | Rename it "A rubber sheet over a cliff". |
| E3 | M | shoebox | pedagogy §3.1 promises "ch. 6: the generator fills the shoebox", but no C6 scene does it. | End C6.3: generated violet photos drop into the C4.6 shoebox. In C8.1, the toll counter (C5.1) comes back with violet "generated cars" (that callback is missing too). |
| E4 | m | M6 projector | Used once (C7.3), so it is not a motif. | Reuse it in C9.6 (3D Coulomb-gauge decoder) and X6.1 (bounded-domain gauge), or drop the motif label. |
| E5 | m | M9 pen | Defined in the style guide, never scheduled. | Assign pen beats (circle, underbrace) to the equation scenes C2.3, C5.2, C6.2, C7.8 and C8.3. |
| E6 | m | anti-dynamo | Planted as a chip in C2.4 and paid off as a chip in C7.2. A chip-to-chip callback is invisible. | Drop it from C2.4 (that scene is already overloaded, see F2). Pay it off in narration in C7.b0 (B1). |
| E7 | m | M1 corner needle, M8 rail | A needle top-right for the whole film, a rail on the right edge (pedagogy says left), source chips, lower-thirds, stamps and a subtitle box: too much persistent HUD. The needle means nothing in the ML chapters. | Show the needle only where D is on screen (pedagogy §3.1 says so). Put the rail on the left edge and show it only at chapter cards and checkpoints (3 s). |
| E8 | m | checkpoints | Exit-ramp wording ("you can stop here") invites drop-off at 4, 10 and 17 min. | Keep the honest recap, but end each checkpoint on an open question for the next level ("but how do you get snapshots at a setting nobody simulated?"). The chapter markers already serve viewers who want to leave. |
| E9 | m | recaps | C7.10, C8.6, C8.7, C10.1 and C10.2 are five recaps in the last 12 minutes. | Merge C8.6 and C8.7 (see F8). In C7.10 reveal only framework panels a, b and d. Panels c (VKS geometry) and e (downstream uses) have not been earned in the core cut. |

## F. Length and density (one idea per scene)

Speech rate assumed: 145 words/min, plus the 3-s holds of predict beats. "Need" is the word count the key idea and on-screen items require, estimated from the outline's own content.

| Scene | Target | Need (words) | Realistic | Gap | What to cut or split |
|---|---|---|---|---|---|
| C0.5 | 12 s | 62 (draft) | 26 s | +14 | see A2 |
| C1.3 | 45 s | about 115 + hold + 2 s squeal | 53 s | +8 | set to 55 s, or split mic / disc |
| C2.4 | 30 s | about 90 | 37 s | +7 | drop the anti-dynamo chip (E6) |
| C3.5 | 30 s | about 95 | 39 s | +9 | keep the knob panel and one boundary switch (no ± numbers). The three Rm definitions live only in X1.4/X6. |
| C5.4 | 20 s | about 55 | 23 s | +3 | keep only "crossings are not reversals". Move "needs the RHS" and "3-variable test" to C8.1 or X4.1. |
| C6.5 | 45 s | about 130 | 54 s | +9 | two ideas: the noise floor (die) here; the distance formula as a 15 s beat at C7.7's first use, or in X3 |
| C7.2 | 35 s | about 105 + hold | 47 s | +12 | 2 numbers on screen (0.41, then 0.34/0.16). Move ×2.68 to a chip. |
| C7.5 | 55 s | about 165 + hold | 71 s | +16 | split: (a) predict and A vs C clouds (40 s); (b) asymmetry vs Γ with the floor (35 s) |
| C7.7 | 55 s | about 140 + hold | 61 s | +6 | keep the E1 numbers only; E2's 8.6e-4 already appears in C7.9 lane 3 |
| C7.9 | 60 s | about 175 (15 numbers) | 72 s | +12 | one number per lane against the floor (0.70, ESS 0.29, σ ratio 8.6e-4). The rest go in the description / X3.4. |
| C8.1 | 55 s | about 130 | 54 s | 0 | fine if "cumulative" is shown as area (C7) |
| C8.6 | 30 s | about 95 (8 cards × 5 columns) | 39 s | +9 | cards carry a shelf and a verdict icon only (exact / approximate / harmful). Merge with C8.7 at 40 s. |
| C10.2 | 60 s | 140 + 3 pauses | 61 s | 0 | fine (but see H2 and G6) |

| # | Sev | Chapter | Problem | Fix |
|---|---|---|---|---|
| F1 | B | C7 (7:25) | It is the longest chapter, at L3-L4, with four overrun scenes. Realistic length is about 8:30 once E2 is introduced. The C6.6 cliffhanger (the lopsided mirror) is paid off only 4 scenes later. | **Split it into two chapters, known system first:** **C7a "The mirror and the crowd" (E1, about 3:40):** C6.6 (moved here) → C7.5 → C7.6 → C7.7 (the C4.7 histogram becomes the spike) → C7.8 two juries. **C7b "Fields have stricter laws" (E2, about 4:30):** C7.b0 (B1) → C7.2 → C7.3 → C7.4 (intuitive) → C7.9 (trimmed) → shelves synthesis (C1) → C7.10. This resolves the cliffhanger at once, keeps one test bench per half, and makes per-sample laws arrive naturally when the film moves from three numbers to fields. |
| F2 | M | C2.4 | Three ideas in 30 s: kinematic vs dynamic, j × B (j never defined), anti-dynamo theorems. | Keep kinematic vs dynamic. Say "the field pushes back on the flow" instead of j × B. Drop the anti-dynamo chip (E6). |
| F3 | M | C2.6 | Numbers to the third digit and 48³ open markers belong at L4 (X1.3), not inside an L2 predict beat. | Keep the windows surprise with rounded thresholds (about 9, 17.5, 27). Move the 48³ markers to X1.3. |
| F4 | M | C3 (4:07, 9 scenes) | C3.5 (specialist numbers), C3.8 (a 20 s disclaimer card on PAPER, a momentum break at minute 10) and C3.9 make it sag. | Trim C3.5 (table above). Fold the C3.8 disclaimer into C3.7 as a second lower-third with one spoken sentence (10 s). Keep the full text on the end card and in the description (D14). |
| F5 | m | C3.4, C4.3 | Numbers like "120 s and 50 s on average ... ohmic time about 0.4 s" and "0.00194 per unit time" sit on L1/L2 cards. | "flips about every minute, irregularly"; "about 2 per 1,000 time units". Exact values go in the formula layer only. |
| F6 | m | C3.7 | The central question has three clauses, and "exactly where exact / statistically where statistical" has not been earned yet (crowd laws arrive in C4.7). | Split it into three promise cards that the film ticks off on screen at C5.3, C7a/C7b and C8.1. |
| F7 | m | C9.3 | A 35 s scene repeats C4.7's lesson (crowd law) on the same workload as E2 data. It also uses the same run as X5.3. | Fold it into C9.2 as a 10 s "first product off the line" beat. Move the full sweep to X5. |
| F8 | m | C8.6 + C8.7 | Two recaps back to back. | One 40 s scene: cards dealt onto the shelves, then the three one-line lessons. |

Net effect on the core cut: the overruns add about 1:50, the E2 intro about 0:30, and the trims (C3.8, C2.4, C3.5, C7.9, C8.6/7, C9.3) remove about 1:15. Plan on **about 41-42 min**, not 39:59, and script against 125-130 effective words/min (150 words/min speech plus 15 % visual breathing room, the 3B1B rhythm).

## G. Feasibility on the 4-core machine

| # | Sev | Scene | Problem | Fix |
|---|---|---|---|---|
| G1 | B | all predict beats (Q1-Q8) | A 3-s countdown hold cannot be produced by TTS. pipeline.md allows `[long pause]` only between paragraphs (about 1 s, not measured), and there is one request per scene. | Add `hold_after: 3.0` per paragraph in the script. `build.js` splits the chunk at the aligned paragraph boundary, inserts silence and shifts later cues (the alignment already gives paragraph times). Test it on C1.5. |
| G2 | M | C0.6, C1.3, C4.2, C6.1 | Sound design (impact, squeal, two-note crossing tick, granular hiss) has no SFX track in the pipeline. The C1.3 squeal would also mask the narration. | Scenes export an event list (`window.__EVENTS__`: t, sample id, gain). `build.js` mixes the samples via `adelay` + `amix` under the same side-chain duck as the music. Time the squeal in a narration gap. |
| G3 | M | C0.1, C10.2 | A "grey hand" holding a compass in Three.js: a convincing procedural hand is out of reach and an uncanny one would undermine the opening. | Use a stylized 3D compass with no hand (or a flat vector hand silhouette under a WebGL compass). This also lowers geometry cost. |
| G4 | M | C0.2 | An 8-s 3D scale dive hand → landscape → space needs terrain modelling. | Use a "Powers of Ten" layered 2D zoom (flat illustrations cross-faded on scale) → grey sphere with field lines (WebGL only for the last 3 s). |
| G5 | M | C1.1 | "Churning outer core" suggests a full-screen noise shader. The WebGL benchmark was geometry-bound, but a full-screen fragment shader on SwiftShader is pixel-bound and has not been measured. | Benchmark one 6 s shader test before committing, or render the churn as Canvas 2D advected texture (dense2d class, measured). |
| G6 | M | C10.2 | Seven motifs "faintly layered" behind a WebGL compass make a visual mush and mix two expensive render classes. | Run the motifs as a sequenced montage, one motif per closing sentence (3-4 s each). Then fade to the clean compass for the three-line lesson. |
| G7 | m | C7.2, C9.3, X5.4 | E2 fields are 32² and look blocky full-screen at 1080p. | The extractor zero-pads in Fourier space to 256² for display, with a chip "display interpolation (spectral)". Divergence is still measured on the native grid. |
| G8 | m | X1.2, C9.6 | Isosurfaces and field lines from 32³ / kmax-3 fields computed in the browser are slow and non-deterministic. | Precompute offline (spectral upsampling, marching cubes, field-line tracing in `extract_data.py`) to compact `.f32` meshes and polylines. The scene only draws them. |
| G9 | m | C9.5 | Render class is webgl, but the scene is mostly flat curves with an optional 3D insert. | Set the class to flat and render the 3D insert as a separate short WebGL shot. This saves about 7 min of render per pass. |

## H. Pending sections: isolation and release

| # | Sev | Scene | Problem | Fix |
|---|---|---|---|---|
| H1 | B | release model | YouTube cannot replace a published video file. "Generate sections later" means either re-uploading (views and comments lost) or a separate release. | Design the **result variants of C9 (and X3.5, X4.x, X6.4-5) to stand alone as a "Results update" episode** (5-8 min: a 45 s recap of C9.1, then the filled seats, then C10.1). Publish the full film as v2 on the site and GitHub release, with a pinned link from the original. |
| H2 | B | C10.2, C10.1, synopsis | They are READY scenes whose truth depends on pending status. "The real tests ... are still ahead. You have seen the bets." becomes false once C9.4-C9.7 report. | Give the third closing paragraph two narration variants keyed to `timeline.json` (pending / results in). Declare every regenerable data file as a dependency of C10.1 and C10.2 so the hash-based rebuild re-renders them. |
| H3 | M | C9.4-C9.8 | In the pending state, C9 is five dashed empty frames in a row (about 3 min), which is monotonous and thin. Durations are given as single numbers although pending and result narrations differ. | Give every seat a READY anchor visual: C9.4 the E3 ghost curve, C9.5 Taylor-Green flow plus schematic growth/saturation, C9.6 a mechanism demo (H4), C9.8 the VKS/DRESDYN schematics. Budget two durations per regenerable scene (pending about 20-25 s, result about 35-45 s). Vary the frame type (curve, map, lamp panel, gauge). |
| H4 | M | C9.6 | "Bet 3a" is not a bet: div = 0 and the mirror hold by construction (Prop. 1, Prop. 4) whatever the training. The 1e-12 criterion cannot fail, and the scene still waits for a provisional TG run. | Make it **READY now**: run the decoder with untrained or smoke weights on CPU. Retitle it "What is guaranteed" and pair it with C9.7 "What must be measured". That leaves one real core bet scene for the 3D generator. |
| H5 | M | C9.4 provisional | The provisional run is ABC at 32³, the same resolution as the E3 ghost already on screen. The two curves will overlap and add no information (except Rm up to 40). | Run the provisional set at 48³ near the three thresholds only, or keep the empty seat with the ghost until 64³ exists. |
| H6 | M | C9 status stamps | PROVISIONAL DATA stamps on four core scenes are unexplained to L0-L3 viewers. | One sentence in C9.2: "a stamp marks results from small trial runs; the full runs will replace them". |
| H7 | m | dependency chain | C9.6 provisional depends on the C9.5 provisional TG fields, and C9.7 on the final fm3d model. This is only implicit in the hooks. | Add `requires:` to the regenerable index and a `make plan` check. |
| H8 | m | C9.8 | Its duration depends on the cut (15 s bridge if X6 is in the cut). | Two script entries (`C9.8-core`, `C9.8-bridge`) selected by the cut file, so the hashes stay clean. |

## I. Extended cut and two-episode option

| # | Sev | Module | Problem | Fix |
|---|---|---|---|---|
| I1 | B | X1 after C2 | X1.3 is L4, then C3 drops to L1. X1.4 shows "the same VKS impeller" before VKS appears (C3.3), and it duplicates C3.5. | Anchor **X1 before C9.4** as the provenance of Bet 1: the 32³ curve, its exact check and its uncertainty set up the 64³ bet. Drop X1.4, or keep it only if C3.5 loses its three definitions. |
| I2 | B | X3.5 | It bets on the 3D generator (fm3d) before C9 shows it. | Move X3.5 to directly after C9.7. |
| I3 | B | X4.4, X4.5 | Tiers, Taylor-Green hysteresis and tier 0/DQVU come before the staircase (C9.1) and Taylor-Green (C9.5) exist. | Keep X4.1-X4.3 after C8. Move X4.4 after C9.5 and X4.5 after C9.1 (or plant the staircase early, E1). |
| I4 | M | X5 after C9 | The ladder drops from L5 to L3 (X5.1). The factory floor belongs with C9.2. | Split X5: X5.1-X5.4 after C9.2 (and C9.2 shortens in the extended cut). X5.5-X5.6 (bill, plan on one page) come after X6 as the L5 finale before C10. |
| I5 | M | X2.2 | Duplicates C7.4 (see B3). | Resolved by making C7.4 intuitive. |
| I6 | m | two-episode option | Part 2 opens at C7 (L3) with no recap of C4-C6, and runs 35:50 against 21:44. | Add a 60 s "previously" scene (needle, shoebox, Rice, violet cloud, lopsided machine). Move C7a (the mirror) into Part 1 as its cliffhanger-and-payoff ending, which rebalances to about 26 / 32 min. |

Proposed extended running order:

C0, C1, C2.1-C2.2, C3.1-C3.4, C2.3-C2.6, C3.5-C3.9, C4, C5, C6, C7a, C7b, X2, X3.1-X3.4, C8, X4.1-X4.3, C9.1, X4.5, C9.2, X5.1-X5.4, X1.1-X1.3, C9.4, C9.5, X4.4, C9.6/C9.7, X3.5, C9.8-bridge, X6, X5.5-X5.6, C10.

The ladder then only climbs. The one exception is the deliberate L5 → L0 closing.

## J. Smaller notes

- C2.1: **"honey vs water" contradicts the Pm lesson of C3.1.** Honey reads as "viscous", but liquid sodium is the opposite case: a fluid as runny as water that smudges the field fast. Frame the split as "slow-smudging ink vs fast-smudging ink", with the same flow on both sides and no viscosity metaphor. (Sev M.)
- C1.4: "Lorentz force" and "Joule losses" at L1. Say "the field brakes the flow" and "heat"; symbols come later.
- C10.2 closing: the narration speaks "a cumulative error of fourteen percent ... forty-two percent" at L0. Put the numbers on chips. Say "it works well far from the tipping point, and poorly right at it, for a reason we now understand".
- C3.7: the lower-third with the ANR number, dates and labs is about 25 words of text. Show it on screen for 4 s minimum, and do not narrate it.
- Predict beats are numbered Q2 before Q1 in film order (C1.3, C1.5). Renumber by order of appearance.
- C1.3 / C1.4: a bicycle dynamo is a cheap L0 anchor ("motion → electricity"). The twist that Earth's dynamo makes its own magnet then lands better.
