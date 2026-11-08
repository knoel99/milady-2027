# -*- coding: utf-8 -*-
"""Structured source of the MilaDy explainer outline (version 2, after the accuracy and pedagogy reviews).

build_outline.py turns this into outline.json (machine-readable) and outline.md (human-readable).
Paths in `assets` and `data` are relative to the site repository /home/user/milady-2027 unless they
start with "proto/" (the render prototype under video_plan/proto). Scene data files written by the
extractor ("data/...json") live under the film project root (today: video_plan/proto/data/).

Version 1 (before review) is kept in outline_src/v1/.

Ids: chapters are ch00-ch11 (they no longer collide with the report's constraint classes C1-C4);
core scenes are NN.k; extension scenes keep their X ids. Every scene carries `was` (its version-1 id).
"""

R, P, N = "READY", "PROVISIONAL", "PENDING"


def sc(id, title, level, dur, key, visual, on_screen, assets=(), data=(), status=R, regen=None,
       register="NIGHT", motifs=(), render="flat", flags=(), sources=(), predict=None, was="new",
       dur_result=None, depends_on=(), ext=None):
    """dur: duration as shipped now (pending variant for PENDING scenes, provisional data for PROVISIONAL).
    dur_result: duration once the final data exist (defaults to dur).
    ext: extended-cut variant, {"id", "duration_s", "note"} or {"skip": True, "replaced_by": [...]}."""
    return {
        "id": id, "was": was, "title": title, "level": level, "duration_s": dur,
        "duration_result_s": dur_result if dur_result is not None else dur, "key_idea": key,
        "visual": visual, "on_screen": on_screen, "assets": list(assets), "data": list(data),
        "status": status, "regen": regen, "register": register, "motifs": list(motifs),
        "render_class": render, "flags": list(flags), "sources": list(sources), "predict": predict,
        "depends_on": list(depends_on), "extended_variant": ext,
    }


def regen(scene_data, upstream, provisional_run, final_run, extractor, shippable_now, criterion=None,
          narration="two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)",
          requires=()):
    return {"scene_data": scene_data, "upstream": upstream, "provisional_run": provisional_run,
            "final_run": final_run, "extractor": extractor, "shippable_now": shippable_now,
            "criterion": criterion, "narration": narration, "requires": list(requires)}


# Common preamble for every run that produces regenerable data. Runs happen in a clone of the
# repository on the compute machine; /home/user/milady-2027 on this machine stays read-only.
RUNENV = (
    "In a clone of the repository on the compute machine (never in /home/user/milady-2027 here): "
    "export MILADY_DB_URL=sqlite:///$RUNS/catalog.sqlite MILADY_STORAGE_URI=$RUNS/store "
    "MILADY_SWEEP_DIR=$RUNS/sweeps MILADY_MODELS_URI=$RUNS/models (check the accepted URI forms with "
    "--dry-run first); then copy the outputs or the catalog dump next to the film project and run "
    "`python3 -I tools/extract_data.py` (writes data/*.json; unchanged content does not re-render)."
)

EMPTY_SEAT = ("an 'empty seat': dashed grey chart frame, axes labelled, success band "
              "shaded, grey data tag; pending narration states the bet and the criterion. No number "
              "is drawn until the data file exists.")

# Every data file a regenerable scene reads; 11.1 and 11.2 depend on all of them (H2).
REGEN_FILES = ["proto/timeline.json", "data/palier1_sweep.json", "data/palier2_abc3d.json", "data/palier2_tg3d.json",
               "data/fm3d_eval.json", "data/tier3_vks.json", "data/tier4_dresdyn.json"]

# --------------------------------------------------------------------------------------------
# CORE CUT
# --------------------------------------------------------------------------------------------

CH00 = {
    "id": "ch00", "cut": "core", "title": "Cold open: the needle and the stripes", "levels": "L0", "was": "C0",
    "learning_goal": "Feel that Earth's field is not permanent: it has flipped many times, irregularly.",
    "takeaway": "The field has flipped many times, with no schedule; we can ask when, and we can ask how often.",
    "scenes": [
        sc("00.1", "A needle that flips", "L0", 11,
           "This needle has pointed north your whole life; the rocks say it has pointed south too, again and again.",
           "Stylized 3D compass in macro, no hand (G3). The vermillion needle tip swings and settles north; at about "
           "7 s it swings round to south, holds, and settles back north. The polarity needle (M1) is born here; "
           "later it appears as a small corner needle only in scenes where the dipole D is on screen (E7).",
           "chip 'illustration, not to time scale'", render="webgl", motifs=["M1 polarity needle (first)"], was="C0.1"),
        sc("00.2", "Pull back to the planet", "L0", 7,
           "The needle follows a field that wraps the whole planet. It feels permanent. It is not.",
           "'Powers of Ten' zoom made of flat layered illustrations cross-faded on scale (compass, room, landscape), "
           "ending on a grey sphere where vermillion dipole field lines bloom from pole to pole. Only the last 3 s "
           "are WebGL, rendered as a separate shot (G4). The narration describes what is on screen (A3).",
           "chip SCHEMATIC", render="flat", motifs=["T2 scale dive"], was="C0.2"),
        sc("00.3", "The seafloor tape recorder", "L0", 16,
           "Cooling lava freezes the field's direction; the spreading seafloor records it as stripes of uneven "
           "width: the flips are irregular.",
           "Cross-section of a mid-ocean ridge: magma rises and cools, short grain segments align with the field "
           "and freeze, the floor slides away on two conveyor belts. Stripes accumulate mirror-symmetrically as a "
           "true barcode: solid vermillion = normal, near-background = reversed, labels kept (A5). The camera tilts "
           "down on the barcode, whose widths are visibly irregular; it slides left and becomes the polarity strip "
           "under a thin D(t) trace (T1 morph).",
           "labels 'normal' / 'reversed'; 'every few hundred thousand years, irregularly' (no powers of ten at L0); "
           "chip SCHEMATIC; reference chip (to be sourced)",
           flags=["EXTERNAL_FACT: seafloor magnetic stripes (Vine and Matthews 1963), source before use (decision D7)"],
           sources=["P3:1230 (Rincon 2019: irregular, 1e5 to 1e6 years)"],
           motifs=["M1 barcode / polarity strip", "T1 morph"], was="C0.3 + C0.4"),
        sc("00.4", "Two questions", "L0", 30,
           "When will it flip next? How often does it flip? In the dynamos we can compute, the first is hopeless "
           "and the second is not.",
           "Two cards: 'When will it flip next?' with a grey clock, 'How often does it flip?' with amber tally "
           "marks. The clock card's border turns dashed and dims; the tally card stays lit. On the words "
           "'machines that dream up magnetic fields', a 3-s teaser of the violet cloud (M4), the film's second "
           "protagonist (A6).",
           "the two questions; violet-cloud teaser",
           sources=["P4:1627 (when vs how often, shown for the three-mode model)"],
           motifs=["M4 violet cloud (teaser)"], was="C0.5"),
        sc("00.5", "Title", "L0", 10,
           "Title card.",
           "Title words sit in a vermillion field-line field; the dipole flips and the lines reorganise "
           "around the letters; one soft impact sound (SFX event, G2).",
           "working title (decision D13)", motifs=["M1 flip"], was="C0.6"),
    ],
}

CH01 = {
    "id": "ch01", "cut": "core", "title": "A planet that makes its own magnet", "levels": "L0-L1", "was": "C1",
    "learning_goal": "Understand that the field must be regenerated by moving liquid metal, that a dynamo is a "
                     "self-amplifying loop with a threshold, and that physics prefers neither polarity.",
    "takeaway": "A moving conducting fluid can turn a tiny field into a large one once its loop gain passes a "
                "threshold, and the laws do not prefer north or south.",
    "scenes": [
        sc("01.1", "No magnet inside", "L0", 25,
           "Left alone, a field in Earth's core would fade within some ten thousand years; the field is billions of "
           "years old, so moving liquid iron must keep regenerating it.",
           "Flat Earth cutaway in grey shells (solid inner core, liquid outer core). A 'left alone' timer makes a "
           "field fade in about 10^4 years while a geological clock runs on to billions of years. Then the outer core "
           "starts to churn, drawn as a Canvas 2D advected texture (G5: no full-screen shader). Grey matter, no colour "
           "until fields appear.",
           "'liquid iron outer core'; 'a field left alone fades in about 10,000 years' vs 'the field is billions of years old'",
           render="dense2d", sources=["P3:269 (Tobias 2021)", "P3:1471", "R:86"], was="C1.1"),
        sc("01.2", "Lines never end", "L0", 30,
           "Cut a magnet in half and you get two magnets, never a lone north pole: field lines never start or stop, "
           "so through any box as many lines enter as leave.",
           "Surprise first (C5): a bar magnet is sawn in half and each half has both poles. Then iron filings morph "
           "into vermillion field lines; a dashed box is dragged around the picture; two counters 'in' and 'out' "
           "always agree. Planted for div B = 0 (payoff in 08.2-08.3).",
           "'lines in = lines out' (no symbol yet)",
           assets=["prep/p1-calcul-vectoriel/fig-monopole-dipole-en.png"], render="dense2d",
           motifs=["the box (callback in 08.2 and 08.3)"], was="C1.2"),
        sc("01.3", "The squeal", "L1", 55,
           "A loop whose gain per turn exceeds one grows from almost nothing, then saturates.",
           "Opens on a bicycle dynamo: motion makes electricity, with a magnet built in; the Earth must make its "
           "own magnet (J). A microphone pointed at its own speaker: whisper, then squeal past a green gain knob "
           "(M2); the squeal sits in a narration gap (SFX event, G2). Morph into a self-exciting disc: grey copper "
           "disc, coil, current arrows; below the threshold the seed dies, above it the field grows turn after "
           "turn, then reaches a plateau (the field brakes the disc). A staircase of bars 'each turn: B x (gain / "
           "loss)' smooths into the curve e^(s t) (B8).",
           "Predict Q1 with a 3-s hold; after the reveal: 'each turn: B x (gain / loss)', then 'B grows like e^(s t)', "
           "s = growth rate (D1)",
           predict="Q1: spin a little faster each time: does the field grow a little each time, or nothing until "
                   "a certain speed? (Answer: nothing, then exponential growth, then saturation.)",
           flags=["EXTERNAL_FACT: self-exciting homopolar disc (Bullard 1955), source before use (decision D7)"],
           motifs=["M2 knob (first)", "squeal / loop gain"], was="C1.3"),
        sc("01.4", "Who pays the bill", "L1", 20,
           "A dynamo converts mechanical power into magnetic energy and heat; it creates no energy.",
           "Loop diagram: motor power -> flow (blue) -> field (vermillion) by induction -> 'the field brakes the "
           "flow' -> heat (grey). Forces and losses are named in words only (J).",
           "loop labels in words",
           assets=["en/prep/p3-mhd-dynamo/index.qmd"],
           sources=["en/prep/p3 ch. 5 loop diagram (inline SVG, redraw in palette)"], was="C1.4"),
        sc("01.5", "Which way is up?", "L1", 25,
           "The equations are unchanged under B -> -B: both polarities are equally lawful; which one you get is history.",
           "Predict card; then a vertical mirror plane (M10) appears; the Earth's field and its mirror twin side "
           "by side; the needle flips.",
           "Predict Q2; then 'B -> -B: same equations'",
           predict="Q2: physics does not care whether the field points north or south. Which polarity should "
                   "Earth prefer? (Answer: neither.)",
           motifs=["M10 mirror (first)"], was="C1.5"),
        sc("01.6", "Checkpoint: the big picture", "L1", 12,
           "Recap, then the next question: what kind of motion can do this, and how fast must it be?",
           "Recap with motifs only (needle, barcode, squeal); the altitude rail (M8, left edge) shows for 3 s and "
           "climbs one notch. Ends on the open question, not on an exit ramp (E8).",
           "'Level 0 -> Level 1'; the open question", motifs=["M8 rail"], was="C1.6"),
    ],
}

CH02 = {
    "id": "ch02", "cut": "core", "title": "Stretch, smudge, and three tanks of sodium", "levels": "L1",
    "was": "C2.1-C2.2 + C3.1-C3.4",
    "learning_goal": "See a dynamo as a race between stretching and smudging measured by Rm, understand why liquid-sodium "
                     "dynamos are hard and turbulent, and meet the three that worked, including VKS, which flips.",
    "takeaway": "A flow amplifies a field when stretching beats smudging; only three sodium experiments got there, "
                "and one of them, VKS, flips like the Earth.",
    "scenes": [
        sc("02.1", "Frozen threads", "L1", 35,
           "A conducting flow drags field lines; stretching a line strengthens the field; diffusion smudges it, "
           "faster in a poorer conductor.",
           "Blue tracer particles stretch and fold a vermillion material line (brightness follows stretch). Split "
           "screen with the same flow on both sides: slow-smudging ink (good conductor, small diffusivity: threads "
           "stay sharp) vs fast-smudging ink (poor conductor, large diffusivity: a grey blur wins). No viscosity "
           "metaphor (B5, J).",
           "'stretching' / 'diffusion'; split labels 'small diffusivity' / 'large diffusivity'",
           assets=["prep/p3-mhd-dynamo/figures/expulsion-en.svg", "proto/scenes/a_fieldlines.html"],
           data=["proto/data/fieldlines.json"], render="dense2d", motifs=["M3 two inks"], was="C2.1"),
        sc("02.2", "One number for the race", "L1", 30,
           "Rm = UL/eta compares stretching with smudging; the growth rate s crosses zero at a threshold Rm_c.",
           "Green Rm knob turns; a schematic growth-rate curve s(Rm) rises through zero; the zero crossing "
           "is marked as the threshold Rm_c.",
           "Rm = U L / eta (U blue, eta green); s = growth rate; chip SCHEMATIC",
           sources=["en/prep/p3 ch. 2"], motifs=["M2 knob"], was="C2.2"),
        sc("02.3", "The sodium problem", "L1", 30,
           "Liquid sodium is as runny as water but smudges fields fast (Pm = nu/eta about 1e-5): reaching Rm of 10 "
           "to 50 means stirring so hard that the flow is violently turbulent.",
           "Two gauges: Rm (green) climbs slowly while Re (blue) races to millions; a turbulent texture fills the "
           "background. Level lowered to L1: one ratio, no exponents in the narration.",
           "Pm = nu / eta ~ 1e-5; 'Rm ~ 10-50 needs Re ~ millions'; formula layer: Re ~ 1e6-1e7",
           sources=["P3:281", "R:137", "en/prep/p3 Ex. 1.6"], was="C3.1"),
        sc("02.4", "Three tanks that worked", "L1", 30,
           "Only three liquid-sodium experiments have produced a dynamo, each with a different field, and only one of "
           "them flips; DRESDYN is trying with precession.",
           "Horizontal timeline cards (one moment per card): Riga (helical flow; an oscillating, rotating field), "
           "Karlsruhe (52 vortex generators; a steady dipole), Cadarache VKS (150 litres of sodium, motors up to "
           "300 kW; a dipole that can flip); a fourth card, dashed: DRESDYN, under way.",
           "names and one plain line each; 'first dynamo: 1999' for Riga and Karlsruhe (R:139)",
           assets=["prep/p3-mhd-dynamo/figures/vks-en.svg"], sources=["R:139", "P3:1149", "S:72", "R:86"], was="C3.2"),
        sc("02.5", "VKS: two impellers and an iron surprise", "L1", 35,
           "Counter-rotating impellers stir liquid sodium; the dynamo appeared only with soft-iron impellers.",
           "3D cutaway of the cylinder (grey matter), two bladed impellers counter-rotating, blue flow cells "
           "and recirculation; the impeller material is swapped steel -> soft iron: only then does a vermillion "
           "axial dipole grow.",
           "chip SCHEMATIC geometry; 'stainless steel: no dynamo' / 'soft iron: dynamo'",
           assets=["figures/vks/figure/out/vks-en.svg", "prep/p3-mhd-dynamo/figures/vks-en.svg"],
           render="webgl", sources=["R:139", "R:90", "T:138"], motifs=["matter grey, fields coloured"], was="C3.3"),
        sc("02.6", "VKS flips too", "L1", 25,
           "With impellers at different speeds, the lab dynamo reverses irregularly, like the Earth, every minute or two.",
           "Qualitative D(t) with reversals (VKS figure, panel b) over the barcode strip; the corner needle (M1) is "
           "shown because D is on screen, and flips in sync. This re-hooks the cold open at about 6 min (B2). The "
           "measured numbers sit on a separate card, not on the qualitative curve (C6).",
           "'flips every minute or two, irregularly'; separate card '16 Hz vs 22 Hz: polarities last 120 s and 50 s "
           "on average; a reversal takes about 5 s' (Berhanu et al. 2007); curve chip 'qualitative (normal form): "
           "durations are not those of VKS'",
           assets=["figures/vks/figure/out/vks-en.svg"], sources=["R:149", "R:163", "P3:1166"],
           motifs=["barcode", "M1 flip", "callback: cold open"], was="C3.4"),
    ],
}

CH03 = {
    "id": "ch03", "cut": "core", "title": "The equation, the windows, and the question", "levels": "L2",
    "was": "C2.3-C2.6 + C3.5-C3.9",
    "learning_goal": "Read the induction equation as the race in symbols; know kinematic vs dynamic and the ABC dynamo "
                     "windows; see that the knob is a panel of knobs, that simulations are too costly to cover it, and "
                     "what this film asks.",
    "takeaway": "A dynamo can switch on, off and on again, real dynamos depend on many knobs, and simulations cover "
                "only a handful of settings: we need something that fills the gaps, and respects the physics.",
    "scenes": [
        sc("03.1", "The induction equation, term by term", "L2", 40,
           "The whole race in one equation.",
           "Equation built with the 10-step protocol: terms light in narrative order, leader lines to a stretched "
           "thread ('carried and stretched by the flow', C1) and a fading thread ('diffusion'); pen beats (M9) "
           "circle each term.",
           "dB/dt = curl(u x B) + eta Laplacian(B); braces 'carried and stretched by the flow', 'diffusion'",
           assets=["proto/scenes/b_induction.html"], sources=["P3:254"], motifs=["M9 pen"], was="C2.3"),
        sc("03.2", "A conveyor belt that does not feel its cargo", "L2", 32,
           "Kinematic dynamo: the flow is imposed and the field grows exponentially (an eigenvalue problem). "
           "Dynamic: the field pushes back on the flow and saturates.",
           "Log plot of |B|(t): a straight line of slope s (kinematic), then the same curve bending into a plateau "
           "when the field pushes back on the flow (dynamic). One idea only: no Lorentz-force symbol and no "
           "anti-dynamo chip here (F2, E6).",
           "'kinematic: B = e^(s t) B_hat, s = real growth rate (modes may also oscillate)'",
           sources=["R:240", "en/prep/p3 §5.2", "R:1114 (oscillating modes)"], was="C2.4"),
        sc("03.3", "Twisting rooms: the ABC flow", "L2", 25,
           "To test our tools we need a flow simple enough to write on one line, yet able to make a dynamo: the ABC "
           "flow, whose streamlines are corkscrews (velocity parallel to its curl).",
           "The motivating line first (C3). A periodic box of fat blue corkscrew streamlines (Three.js Line2), slow "
           "orbit, long lens. The box glows for a moment on the faint staircase map (M7, tier-2 preview, E1).",
           "u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x);  curl u = u",
           assets=["proto/scenes/c_abc3d.html"], render="webgl", sources=["R:1063"],
           motifs=["M7 staircase (tier-2 preview)"], was="C2.5"),
        sc("03.4", "Predict: once on, always on?", "L2", 45,
           "Dynamo windows: the ABC dynamo switches on near Rm 9, off near 17.5, on again above about 27.",
           "Predict card; then s(Rm) drawn live, left to right, from E3 (24 points); windows shaded green at 12%; inset "
           "z = 0 slices of |B| of the dominant mode (least damped or fastest growing) at Rm 8, 12, 16 and 20: below, "
           "inside and just after the first window (B7). The 48^3 check markers move to X1.3 (F3).",
           "thresholds 'about 9 · 17.5 · 27'; formula layer: 8.87 / 17.6 / 26.8 (32^3) vs published 8.9 / 17.5 / about 27; "
           "source chip DATA · E3",
           assets=["experiences/figures/e3_abc-en.svg", "assets/interactif/abc-dynamo.js"],
           data=["experiences/resultats/e3_abc.json", "assets/interactif/data/abc-dynamo.json"],
           predict="Q3: lowering diffusion only helps stretching; once the dynamo turns on, it stays on. Right? "
                   "(Answer: no, windows.)",
           flags=["CAVEAT: kinematic test bench, no generative model in E3"], sources=["R:1070-1112", "D:170-198"],
           was="C2.6"),
        sc("03.5", "A panel of knobs", "L2", 30,
           "The control parameter is a vector: Re, Rm, materials, boundary conditions, forcing asymmetry, precession.",
           "The single green knob splits into a panel (Re, Rm, iron, asymmetry, precession). One boundary-condition "
           "switch moves a threshold marker up by about 40%, with the chip 'simulations, Nore et al. 2018' (B15). "
           "The three definitions of Rm leave this scene (they live in X6.0).",
           "knob names in words ('iron', not mu_r: D3); 'boundary condition: threshold +40% (simulations)'; formula "
           "layer: Rm_c = 90 ± 5 (pseudo-vacuum) -> 130 ± 10 (vacuum) at Re = 1.5e3, mu_r = 50",
           sources=["R:143", "R:90", "en/prep/p3 line 722"], motifs=["M2 knob panel"], was="C3.5"),
        sc("03.6", "A handful of dots", "L2", 25,
           "Each 3D turbulent simulation is expensive, so only a few knob settings exist, each a huge dataset.",
           "A green parameter axis with a few filled dots; each dot grows a tall grey stack of data files; the "
           "gaps between dots stay empty.",
           "'each simulation: a few settings, terabytes'; chip 'order-of-magnitude estimate' (C12)",
           sources=["H:64", "T:62", "T:931 (VKS sizes)"], was="C3.6"),
        sc("03.7", "The question of this film", "L2", 50,
           "This study asks: can a machine learn the family of possible fields for any knob setting, respect physics "
           "exactly where it is exact and statistically where it is statistical, and tell us how often the field flips?",
           "Lower-third 1, on screen for at least 4 s and not narrated (J): the project context (B1). Then 'This "
           "study asks:' and the question, typeset word by word in the colour key, splits into three promise cards "
           "that the film ticks off on screen at 05.3, 08.6 and 09.1 (F6); a small violet cloud sits on card 1 (A6). "
           "The staircase map of the film (M7) appears with tiers 0-4 all grey (E1). Lower-third 2 with one spoken "
           "sentence: the disclaimer (F4; former C3.8 folded in).",
           "lower-third 1 'MilaDy (context) · ANR-25-CE51-0077 · since January 2026 · 48 months · LISN, Lagrange (OCA), "
           "CEREA (ENPC) · goals: reduced models of reversals and bursts; DRESDYN optimisation'; three promise cards; "
           "staircase map; lower-third 2 'Independent, prospective study · small CPU experiments · not produced or "
           "endorsed by MilaDy, its partners or the supervisors · no MilaDy data used' (full text on the end card and "
           "in the description)",
           sources=["S:57-72", "H:72", "H:43-46", "R:51", "T:55-58"], flags=["DISCLAIMER (decision D14)"],
           motifs=["M7 staircase (planted)", "M4 violet cloud"], was="C3.7 + C3.8"),
        sc("03.8", "Checkpoint: Level 1 done", "L2", 15,
           "Full simulations cost too much, so we start with a caricature that has three dials and already flips.",
           "Motif recap (threads, knob panel, barcode); rail (left edge) shows for 3 s and climbs to L2; ends on the "
           "bridge sentence into ch04 (C4, E8).",
           "'Level 1 -> Level 2'", motifs=["M8 rail"], was="C3.9"),
    ],
}

CH04 = {
    "id": "ch04", "cut": "core", "title": "Chaos and the shoebox of photographs", "levels": "L2", "was": "C4",
    "learning_goal": "See reversals in a three-mode model, understand why 'when' is unpredictable, and why the "
                     "stationary distribution (a shuffled box of snapshots) is the stable object; meet crowd laws.",
    "takeaway": "The date of the next flip is unknowable, but the cloud of states is stable, and some laws hold only for the cloud.",
    "scenes": [
        sc("04.1", "Three dials", "L2", 30,
           "Three coupled modes (quadrupole Q, dipole D, velocity V) with the B -> -B symmetry already reverse.",
           "Three dials (D vermillion, Q light vermillion, V blue) linked by springs; then the equations appear "
           "term by term in the same colours; the staircase map lights tier 0 (E1).",
           "Qdot = 0.119 Q - V D;  Ddot = -0.1 D + V Q;  Vdot = Gamma - V + Q D;  (Q, D, V) -> (-Q, -D, V); "
           "coefficients as numbers only (D3); chip 'phenomenological model (Gissinger 2012)'",
           assets=["assets/interactif/gissinger.js"], sources=["R:159", "R:434", "R:784"],
           motifs=["M7 staircase (tier 0 lit)"], was="C4.1"),
        sc("04.2", "Two whirlpools and a corridor", "L2", 45,
           "Below Gamma about 0.86 each trajectory is trapped in one of two mirror whirlpools; above, a corridor opens and it flips.",
           "Live RK4 integration in Canvas: (Q, D) phase portrait with a fading trail; green Gamma knob turned "
           "from 0.80 to 1.00; the two mirror whirlpools touch; a two-note sound at each crossing (SFX events, G2); "
           "scrolling magnetogram strip D(t) with its barcode underneath.",
           "Gamma knob value; chip 'attractor-merging crisis (shown in mu by Gissinger 2012; expected in Gamma)' (C3)",
           assets=["assets/interactif/gissinger.js", "prep/p4-systemes-dynamiques/figures/gissinger-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#config"], render="dense2d",
           motifs=["two whirlpools and the corridor", "M1 flip sound", "M2 knob"], sources=["P4:1513-1541", "R:784"],
           was="C4.2"),
        sc("04.3", "Listen to the rate", "L2", 25,
           "We count every time D crosses zero (most crossings are flips, some are near-misses): the crossing rate "
           "switches on at a threshold between Gamma = 0.86 and 0.865 and grows with Gamma.",
           "Ticks per zero crossing; the simulated crossing rate vs Gamma builds point by point (41 values); "
           "training values as filled dots.",
           "'crossing rate: 0 up to 0.86 · about 2 per 1,000 time units at 0.865 · about 11 per 1,000 at 1.00' (F5, D5); "
           "formula layer: 0.00194 and 0.0112 per unit time",
           assets=["proto/scenes/d_curve.html"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine.taux_simulation", "proto/data/e1_rate.json"],
           sources=["R:871", "R:528", "D:93-121"], was="C4.3"),
        sc("04.4", "Predict: when is the next flip?", "L2", 40,
           "At Gamma = 0.9, errors grow by a factor e every ~11 time units while the mean interval between crossings "
           "is about 230: 'when' is out of reach.",
           "Predict card; two trajectories started 1e-6 apart at Gamma = 0.9, drawn in two shades; their separation "
           "on a log axis climbs with slope ~0.09; a ruler compares 11 units with the ~230-unit mean interval (B12).",
           "'Gamma = 0.9 · Lyapunov time ~11 · mean interval between crossings ~230'",
           predict="Q4: we know the state to six decimals. Can we predict the date of the next reversal? (Answer: no.)",
           render="dense2d", sources=["P4:1627", "P4:1778", "D fine grid (0.00442 crossings per unit time at 0.9)"],
           was="C4.4"),
        sc("04.5", "The long exposure", "L2", 30,
           "Above the threshold, different trajectories paint the same glow: the stationary distribution is "
           "reproducible. Below it, each start paints one whirlpool.",
           "At Gamma = 0.93, shown on screen, two trajectories from different starts leave long-exposure glows that "
           "converge to the same shape; an amber histogram of D (bimodal) builds below and becomes identical for "
           "both. One closing line: below the threshold, each start paints its own whirlpool (B6).",
           "'Gamma = 0.93'; 'the long-exposure glow (stationary distribution)' (B5: mu_Gamma is kept for X2 and X4)",
           render="dense2d", motifs=["M5 amber histogram (first)"], sources=["P4:928", "R:871", "R:901"], was="C4.5"),
        sc("04.6", "The shoebox", "L2", 35,
           "Cut the film into frames, shuffle, drop the timestamps: a sample of the stationary distribution. A "
           "snapshot carries no timestamp and no time order.",
           "A film strip of the trajectory is cut into frames that fall, shuffled, into a shoebox; their time "
           "labels flutter away; the box's contents redraw the same cloud.",
           "'a snapshot carries no timestamp and no time order' (A4)",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.9"], motifs=["shoebox (first)"],
           sources=["R:320-322"], was="C4.6"),
        sc("04.7", "Crowd laws", "L2", 40,
           "dE/dt fluctuates from snapshot to snapshot; only its mean is zero. The energy budget is a law of the crowd.",
           "Each shoebox photo drops a marble into an amber histogram of dE/dt (computed from the model's right-hand side); "
           "the histogram breathes around zero; its mean marker sits exactly at 0. A bank-account ledger flashes as a preview.",
           "'true on average, not for each'; amber E[P - eps] = 0 (eps = dissipation, never D: D4)",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.93"], motifs=["M5 amber histogram"],
           sources=["R:321", "R:265-278"], was="C4.7"),
    ],
}

CH05 = {
    "id": "ch05", "cut": "core", "title": "Counting crossings from still photographs", "levels": "L2-L3", "was": "C5",
    "learning_goal": "Understand Rice's formula as 'a toll counter without a clock' and see it reproduce the true crossing "
                     "rate from snapshots plus the equations.",
    "takeaway": "A shoebox of snapshots plus the equations gives the crossing rate without running time forward.",
    "scenes": [
        sc("05.1", "A toll counter without a clock", "L2", 40,
           "From one aerial photo with readable speedometers, count cars in a thin strip, weight by speed, divide by "
           "the width: crossings per hour.",
           "Aerial highway with a line across it; a thin strip around the line highlighted; cars inside the "
           "strip glow with their speed; a counter computes the rate; no clock anywhere.",
           "'rate = (cars in strip x speed) / strip width'", motifs=["toll counter (first)"], was="C5.1"),
        sc("05.2", "Rice for the dipole", "L3", 50,
           "For D, the strip is |D| < h and each snapshot's speed Ddot = -0.1 D + V Q comes from the equations.",
           "Shoebox points spread in the (D, Ddot) plane; the strip |D| < h (h = 0.2) lights up; each point's |Ddot| "
           "is drawn as a bar; equation morph to the formula with pen beats (M9). Only about 21 of the 8,000 reference "
           "points at Gamma = 0.9 fall in the strip: zoom on the strip and use a denser re-integrated set (C13).",
           "r_0 = lim_{h->0} (1/2h) E[ |Ddot| 1{|D|<h} ] (r_0 = crossings per unit time, D3); reference chip 'Kac 1943; Rice 1944-1945'",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.9"],
           flags=["DATA: for a dense strip, re-integrate one long Gissinger trajectory at Gamma = 0.9 in the extractor "
                  "(CPU seconds), or read experiences/resultats/cache_e1/sim_fine.pkl (local only)"],
           motifs=["M9 pen"], sources=["R:510-538", "R:703-709"], was="C5.2"),
        sc("05.3", "Check against the truth", "L3", 35,
           "On the true distribution, with no time order, Rice reproduces direct counting with a cumulative error of "
           "4% near the threshold and 6% above.",
           "Rates vs Gamma: direct count (solid vermillion) and Rice on reference snapshots (amber) drawn on together. "
           "'Cumulative error' is defined visually once: the shaded area between the two curves divided by the area "
           "under the true curve (C7); the same shading returns in 09.1. Promise card 3 gets a first tick.",
           "'cumulative error 4% (0.865 <= Gamma <= 0.885) · 6% (Gamma >= 0.89)'; source chip DATA · E1",
           assets=["experiences/figures/e1_seuil-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine.taux_rice_ref"], sources=["R:883"], was="C5.3"),
        sc("05.4", "Crossings are not reversals", "L3", 15,
           "Rice counts every zero crossing, near-misses included, not only clear-cut reversals.",
           "One caveat card: a D(t) trace with an excursion that touches zero and returns is counted. The other "
           "caveats move: 'needs the equations' and 'a rate, not waiting times' to 09.1, 'tested on a 3-variable "
           "deterministic system' to X4.1 (F).",
           "'crossings, not reversals'", sources=["R:528", "pedagogy P15"], was="C5.4"),
        sc("05.5", "Photographs on demand", "L3", 20,
           "So all we need is a cheap source of snapshots at any knob setting. But how do you get snapshots at a "
           "setting nobody simulated?",
           "The green parameter axis from 03.6 returns, gaps glowing; rail (left edge) shows for 3 s and climbs to "
           "L3; ends on the open question (E8).",
           "'Level 2 -> Level 3'", motifs=["M8 rail", "callback 03.6"], was="C5.5"),
    ],
}

CH06 = {
    "id": "ch06", "cut": "core", "title": "A machine that dreams snapshots", "levels": "L3", "was": "C6.1-C6.5",
    "learning_goal": "Understand conditional flow matching as learning an average wind from noise to data, conditioned on the knob, "
                     "and how generated distributions are judged against a noise floor with a distribution distance.",
    "takeaway": "A generative model learns a wind that carries noise to data, one model for every knob setting, judged against the noise floor.",
    "scenes": [
        sc("06.1", "From noise to data", "L3", 35,
           "A wind field carries a cloud of random points onto the shape of the data.",
           "Round violet Gaussian cloud (M4); a time-dependent wind bends particle paths onto two symmetric "
           "blobs; granular hiss under the motion (SFX event, G2).",
           "'generative model: new, plausible examples on demand'",
           assets=["assets/interactif/flow-matching.js", "figures/flow-matching/figure/out/flow-matching-en.svg"],
           render="dense2d", motifs=["M4 violet cloud (first full appearance)"], sources=["R:282-296"], was="C6.1"),
        sc("06.2", "Two clocks, two velocities", "L3", 20,
           "The generator's time t in [0, 1] is not physical time, and its velocity v_theta (violet) is not the fluid velocity u (blue).",
           "Side-by-side chips: violet clock 't: transport time' vs grey clock 'physical time'; violet arrow v_theta "
           "vs blue arrow u. Moved before the formulas that use t and v (C6).",
           "'the generator makes snapshots, not movies'", sources=["R:320-322"], was="C6.4"),
        sc("06.3", "Straight strings, average wind", "L3", 50,
           "Training is plain regression: at each place and moment, learn the average direction of straight noise-to-data strings.",
           "Thousands of straight strings from noise points to data points; at a probe location the passing "
           "strings average into one violet arrow; the learned trajectories, drawn with transport time t on the "
           "horizontal axis (1D state vs t), curve but never cross (C9); pen beats (M9) on the regression target.",
           "x_t = (1 - t) x_0 + t x_1;  J(v) = E || v(x_t, t, lambda) - (x_1 - x_0) ||^2;  v* = E[x_1 - x_0 | x_t, lambda] "
           "(lambda = the knob, green)",
           assets=["figures/flow-matching/figure/out/flow-matching-en.svg", "prep/p7-modeles-generatifs/fig-chemins-en.png"],
           render="dense2d", motifs=["M9 pen"], sources=["R:282-296", "R:593-605"], was="C6.2"),
        sc("06.4", "Turn the knob, reshape the cloud", "L3", 30,
           "One model for a continuum of knob settings, including settings never simulated, between those that were (interpolation).",
           "Green knob drives lambda; target blobs drift and the violet cloud follows; on the knob axis training "
           "values are filled dots, test values open dots. Ends with generated violet photos dropping into the "
           "04.6 shoebox (E3).",
           "'trained on filled dots, tested on open dots (interpolation only)'",
           assets=["prep/p7-modeles-generatifs/fig-fm-conditionnel-en.png"], render="dense2d",
           sources=["R:743"], motifs=["M2 knob", "M4 cloud", "shoebox callback"], was="C6.3"),
        sc("06.5", "The noise floor", "L3", 50,
           "Two honest samples of the same truth differ; compare models with that floor at equal sample size, never "
           "with zero. A distribution distance measures how far apart two crowds are.",
           "A die rolled 1000 times, twice: two amber histograms differ; their distance becomes a dashed grey "
           "floor line. Then an 8-s 'distance between crowds' beat: the earth-mover picture, sand moved from one "
           "histogram onto the other (B6). The formula is not narrated (F).",
           "dashed 'floor'; amber 'distribution distance'; chip 'technical names: energy distance (used in the "
           "experiments), Wasserstein W1 (earth-mover)' (D2, B6); formula layer only: E(P, Q) = 2 E||X - Y|| - "
           "E||X - X'|| - E||Y - Y'||",
           assets=["prep/p5-probabilites-transport/fig-wasserstein-1d-en.png"],
           motifs=["dashed grey floor (first)", "M5 amber histogram"], sources=["R:715-725", "R:747"], was="C6.5"),
    ],
}

CH07 = {
    "id": "ch07", "cut": "core", "title": "The mirror and the crowd", "levels": "L3-L4", "was": "C6.6 + C7.5-C7.8 (E1 half of C7)",
    "learning_goal": "On the three-mode model: see a plain generator inherit the data's polarity bias, a built-in mirror fix it at "
                     "every knob value while augmentation fixes it only where data exist, the budget check stay blind to the "
                     "mirror, and a crowd law forced onto each snapshot become a spike; meet the two-jury estimator.",
    "takeaway": "Build the mirror into the machine, impose crowd laws on the crowd, and never force a crowd law onto each snapshot.",
    "scenes": [
        sc("07.1", "A lopsided machine", "L3", 40,
           "A plain conditional model reproduces the cloud's shape but inherits the training data's polarity imbalance.",
           "Opens on two empty shelves labelled in plain words, 'true for every snapshot' and 'true only for the "
           "crowd' (C1: the taxonomy becomes the chapter pair's payoff, 08.6). Then (Q, D) clouds at Gamma = 0.85: "
           "reference (grey, chip SIMULATED) vs baseline model A (violet chip GENERATED); a polarity balance bar shows "
           "A's tilt. Ends on a question mark at the mirror.",
           "two empty shelves; 'Gamma = 0.85, a value never seen in training'",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.85", "experiences/resultats/e1_echantillons.npz#A_reference|0.85"],
           render="dense2d", motifs=["two shelves (empty)"], sources=["R:855-873"], was="C6.6"),
        sc("07.2", "Predict: the mirror test", "L3", 40,
           "A mirror built into the network keeps both polarities equally likely at every knob value. It is built "
           "into the machine but acts on the crowd: each snapshot stays lopsided, the crowd is balanced.",
           "Predict card (one student learns from mirrored copies, the other has a mirror built in); (Q, D) clouds A "
           "vs C at 0.85; the mirror gate S acts on the violet cloud: each generated point stays on one side, the "
           "crowd balances (C2). The mirror card is placed on the crowd shelf with the tag 'built in, exactly'.",
           "shelf tag 'built in, exactly'; formula layer: v_sym = 1/2 [v(x) + S v(S x)], S = diag(-1, -1, 1)",
           data=["experiences/resultats/e1_echantillons.npz#A_reference|0.85",
                 "experiences/resultats/e1_echantillons.npz#C_equivariant|0.85", "experiences/resultats/e1_echantillons.npz#ref|0.85"],
           predict="Q5: one student learns from mirrored copies, the other has a mirror built in. At an unseen knob value, "
                   "who stays symmetric? (Answer: the built-in mirror.)",
           render="dense2d", motifs=["M10 mirror", "two whirlpools", "shelves"], sources=["R:400-412", "R:855-873"],
           was="C7.5 (first half)"),
        sc("07.3", "Only where the data are", "L3", 35,
           "Augmentation symmetrizes only at the knob values it was trained on; between them the network interpolates freely.",
           "Training data lopsided below the threshold (P(D > 0) = 0.375 at Gamma 0.80, 0.3125 at 0.86). Asymmetry "
           "vs Gamma for A, B, C drawn per Gamma (train filled, test open) against the dashed floor: A spikes, B dips "
           "only at training values, C sits on the floor everywhere.",
           "'A: 0.183 at 0.86, 0.085 at unseen 0.87 · B: 0.003-0.006 at training values, 0.007-0.025 between them "
           "(mean 0.016) · C: about 0.004 (floor) everywhere' (B11)",
           assets=["experiences/figures/e1_symetrie_projection-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#evaluation", "experiences/resultats/e1_gissinger.json#donnees"],
           render="dense2d", motifs=["dashed floor"], sources=["R:839", "R:871-873"], was="C7.5 (second half)"),
        sc("07.4", "The budget is blind to the mirror", "L3", 20,
           "Any mix of the two polarities passes the energy-budget check, so symmetry must be imposed separately.",
           "A slider p mixes the two whirlpool clouds; the amber budget gauge stays at zero for every p; the lopsided "
           "model A even scores best on the budget check (B4).",
           "'A: lowest budget-check residual of A, B, C (0.0167 vs 0.0223 and 0.0217)' (C7); formula layer: Remark 3.7",
           data=["experiences/resultats/e1_gissinger.json#evaluation"], sources=["R:415-417", "R:873"], was="C7.6"),
        sc("07.5", "Predict: balance every snapshot?", "L4", 58,
           "Forcing the stationary budget onto each snapshot makes a spike that the truth never produces: worse "
           "where it counts (Corollary 6).",
           "Predict card; bank-account ledger; the amber dE/dt histogram of 04.7 (reference, Gamma = 0.93) and a hand "
           "that pushes every marble onto zero: the histogram collapses into a spike. Numbers land after the picture. "
           "The budget card goes on the crowd shelf. Closing line sets up 08.5: 'in the next test, a cruder score is "
           "fooled by the same spike' (A10).",
           "'distribution distance x9 (0.0231 vs 0.00257) · spread of dE/dt -> 4e-17'; formula layer: Cor. 6: no atom "
           "at 0 => any law on {L phi = 0} is singular: KL = infinity ('infinitely surprised'), W1 >= E|L phi| / Lip(phi) (B6)",
           assets=["assets/interactif/contrainte-loi.js", "experiences/figures/e1_symetrie_projection-en.svg"],
           data=["experiences/resultats/e1_echantillons.npz#E_projection_C|0.93", "experiences/resultats/e1_echantillons.npz#ref|0.93"],
           predict="Q6: energy in must equal energy out. Force every snapshot to balance exactly: better or worse? (Answer: worse.)",
           motifs=["the spike (first)", "M5 histogram", "shelves"], sources=["R:448-460", "R:881"], was="C7.7"),
        sc("07.6", "Enforce it on the crowd, with two juries", "L4", 50,
           "Impose the budget on the generated distribution during training, even at knob values with no data; "
           "estimate it with two independent half-batches.",
           "A batch of violet samples votes; squaring one batch mean secretly adds a variance penalty (a hidden "
           "spike-maker); splitting into two juries and multiplying their means removes it; pen beats (M9).",
           "E[gbar^2] = (E g)^2 + Var(g)/n;  E[gbar_a gbar_b] = (E g)^2;  S_lambda(theta) = sum_k (E_q[L phi_k] / s_k)^2",
           motifs=["two juries", "M9 pen"], sources=["R:663-683", "R:488-496"], was="C7.8"),
    ],
}

CH08 = {
    "id": "ch08", "cut": "core", "title": "Fields have stricter laws", "levels": "L3-L4", "was": "C7.1-C7.4 + C7.9-C7.10 + new (E2 half of C7)",
    "learning_goal": "Meet the 2D MHD test bench; see that clean training data do not give clean outputs, that exact mechanisms "
                     "(potentials, projection) beat a penalty, that the crowd-level budget loss beats a control run while "
                     "tilting and per-sample rescaling fail; sort every law onto its shelf.",
    "takeaway": "Enforce each law at the level where it is true: build per-snapshot laws into every output, impose crowd laws on the crowd.",
    "scenes": [
        sc("08.1", "A flat sheet of plasma", "L3", 30,
           "A second test bench with whole fields: forced 2D MHD in a periodic square, with one knob, the magnetic "
           "diffusivity eta. A flat world cannot sustain a dynamo on its own: this is a training ground for laws, not a dynamo.",
           "The chapter card declares a side-step on the rail ('new test bench: from three numbers to whole fields', "
           "L4 -> L3). The periodic square tiles itself; blue u and vermillion B maps from the reference samples (32^2, "
           "zero-padded in Fourier space to 256^2 for display, G7); the green eta knob with 11 values (6 filled "
           "training dots, 5 open test dots). The staircase map lights tier 1 (E1). The anti-dynamo payoff is "
           "narrated here (E6, B1 of the pedagogy review).",
           "'forced 2D MHD · periodic square · knob: eta · 6 training values, 5 test values'; chip 'not a dynamo: a "
           "planar flow cannot sustain a field (Zeldovich); here B is kept alive by its own forcing'; chip 'display "
           "interpolation (spectral)'",
           data=["experiences/resultats/e2_echantillons.npz#ref", "experiences/resultats/e2_mhd2d.json#config"],
           render="dense2d", motifs=["M7 staircase (tier 1 lit)", "M2 knob"],
           sources=["R:905-919", "R:1179", "R:240", "P3:872-875"], was="new (C7.b0)"),
        sc("08.2", "Predict: does clean data make clean outputs?", "L3", 42,
           "A model trained only on divergence-free fields still outputs a relative divergence of 0.41; a soft penalty "
           "only reaches 0.34 (u) / 0.16 (B).",
           "Predict card; generated u and B maps (same display interpolation; divergence measured on the native "
           "grid) at eta = 0.00951, free model V0 vs reference; a divergence map lights up hot spots; the 'lines in = "
           "lines out' box of 01.2 fails its count; penalty bars follow. The divergence card goes on the per-snapshot shelf.",
           "'free: 0.41', then 'penalty: 0.34 (u) / 0.16 (B)'; chip 'penalty inflates magnetic energy x2.7' (F)",
           assets=["experiences/figures/e2_mecanismes-en.svg", "experiences/figures/e2_spectres-en.svg"],
           data=["experiences/resultats/e2_echantillons.npz#V0_libre", "experiences/resultats/e2_echantillons.npz#ref",
                 "experiences/resultats/e2_mhd2d.json#evaluation"],
           predict="Q7: trained only on perfectly divergence-free fields, are the outputs divergence-free? (Answer: no, 0.41.)",
           render="dense2d", flags=["HYPOTHESIS label for 'the penalty is gamed by inflating the swirl part'"],
           motifs=["callback 01.2 box", "shelves"], sources=["R:1023-1027", "R:931-961"], was="C7.2"),
        sc("08.3", "Hill maps and swirl minus slope", "L3", 50,
           "Generate potentials (a landscape) and take the curl: zero divergence for free. Or project: remove each "
           "wave's component along its own direction.",
           "A landscape psi with water walking its contour lines (the 01.2 box returns: nothing piles up); then "
           "Fourier space: each wave's arrow loses its component along k (projector motif M6). A gauge needle drops to 1e-17.",
           "u = (d_y psi, -d_x psi);  u_k -> (I - k k^T / |k|^2) u_k;  gauges: final projection 5e-17 · potentials "
           "1.7e-17 · projected flow 2e-8 (single precision)",
           assets=["assets/interactif/leray.js", "prep/p1-calcul-vectoriel/fig-helmholtz-en.png", "prep/p1-calcul-vectoriel/fig-courant-en.png"],
           data=["experiences/resultats/e2_mhd2d.json#evaluation", "experiences/resultats/e2_echantillons.npz#V4_potentiels"],
           render="dense2d", flags=["CAVEAT: divergence measured with the same spectral operator (P16)"],
           motifs=["M6 projector (first)", "callback 01.2 box"], sources=["R:1023-1029"], was="C7.3"),
        sc("08.4", "Why almost is not exactly", "L3", 30,
           "To land exactly on the constraint, the ideal wind needs a spring that becomes infinitely stiff at the "
           "very end; a network of bounded strength cannot, so a residue always remains.",
           "NIGHT, no ink change: a ball pulled onto a line by a spring whose stiffness meter shoots up near t = 1; a "
           "capped spring (bounded network) leaves a visible gap. No formula in the core cut (B3): Proposition 2 and "
           "Remark 3.6 live in X2.2.",
           "'needs infinite stiffness at the end' / 'bounded network: a gap remains'",
           sources=["R:345-386"], was="C7.4"),
        sc("08.5", "Three ways to fix a budget", "L4", 62,
           "At unseen eta, the crowd-level loss cuts the distribution distance from 2.52 (control run) to 0.70; tilting "
           "collapses the effective sample; per-sample rescaling turns the dissipation into a spike while a "
           "spectrum-based score even improves.",
           "Bar race over three lanes with the dashed floor, one number per lane (F): (1) training loss V5 vs a control "
           "run of equal length; (2) exponential tilting with an ESS counter ticking down, 'a poll of 500 that shrank "
           "to one person' where the model is worst (B10); (3) per-sample rescaling: the dissipation histogram "
           "collapses into the spike of 07.5 while the spectrum-based score improves; only the spread of the "
           "dissipation reveals it (A10).",
           "lane 1 '0.70 vs 2.52 (control)'; lane 2 'mean ESS/N 0.29 · one effective sample in 500 at the largest test "
           "eta'; lane 3 'spread of eps x 8.6e-4 · spectrum-based distance 2.62 -> 1.1: fooled'; chip 'one seed per "
           "variant'; the other numbers go to the description and X3.4",
           assets=["experiences/figures/e2_en_loi-en.svg"],
           data=["experiences/resultats/e2_mhd2d.json#evaluation", "experiences/resultats/e2_mhd2d.json#en_loi"],
           flags=["CAVEAT: one seed, interpolation only (P10, P11)"], motifs=["M5", "dashed floor", "the spike"],
           sources=["R:1031-1035", "D:132-162"], was="C7.9"),
        sc("08.6", "Two shelves", "L4", 40,
           "Enforce each law at the level where it is true: per-snapshot laws are built into every output, crowd laws "
           "are imposed on the crowd; the mirror is a crowd law that can be built in exactly.",
           "The two shelves of 07.1, now full: every card placed during ch07-ch08 slides to its final place; in the "
           "last 10 s the formal row of the report's classes appears under the shelves (C1). Redrawn taxonomy, no blue "
           "for per-sample. Promise card 2 gets its tick.",
           "'Enforce a constraint where it is true'; formal row (last 10 s): C1 x in ker A · C2 c(x) = 0 · "
           "C3 g#mu = mu · C4 E_mu[L phi] = 0",
           assets=["figures/taxonomie/figure/out/taxonomie-en.svg"],
           flags=["REDRAW: site figure uses blue for per-sample, which clashes with blue = u"],
           motifs=["shelves (payoff)"], sources=["R:304-317", "R:1199"], was="C7.1"),
        sc("08.7", "The proposed machine", "L4", 35,
           "The framework this study proposes, panel by panel; the experiments tested pieces of it only. Checkpoint L3 -> L4.",
           "The report's framework figure revealed panels a (latent flow to a symmetric law), b (potential decoder) "
           "and d (distributional control) only (E9); the tested pieces light up: potentials in 2D, equivariance in "
           "3 variables, the crowd loss, Rice. Rail (left edge) shows for 3 s and climbs to L4; ends on the open "
           "question 'so how well does it answer how often?' (E8).",
           "title 'The proposed machine'; chip 'PROPOSED · not implemented as a whole · E1-E3 tested pieces only' (A6); "
           "'Level 3 -> Level 4'",
           assets=["figures/cadre/figure/out/cadre-en.svg"], motifs=["M8 rail"], sources=["R:300", "R:1179", "H:41"],
           was="C7.10"),
    ],
}

CH09 = {
    "id": "ch09", "cut": "core", "title": "The honest scoreboard", "levels": "L4", "was": "C8",
    "learning_goal": "See the 'how often' payoff with its error bars, why a smooth generator must lag a steep onset, and what remains weak.",
    "takeaway": "On a toy model the crossing rate is predicted from generated snapshots and the model's equations, without running "
                "time forward: roughly right far from the threshold and poorly near it, as expected from a generator that varies "
                "smoothly with the knob.",
    "scenes": [
        sc("09.1", "How often, from generated photographs", "L4", 55,
           "Rice applied to generated snapshots of model C (seed 0) predicts the crossing rate with 14% cumulative error "
           "for Gamma >= 0.89 (up to 65% at a single value) and 42% near the threshold.",
           "The toll counter of 05.1 returns with violet 'generated cars' (E3). The 04.3 curve returns; Rice on "
           "reference (amber) and Rice on generated samples of model C (dashed, violet chip) are drawn on, model F "
           "faint; the cumulative error is the shaded area of 05.3 (C7). Two caveat chips moved from 05.4. Promise "
           "card 3 gets its tick.",
           "'model C, seed 0 · far from threshold: 14% cumulative, pointwise mean 17%, up to 65% at 0.905-0.91 · near "
           "threshold: 42%'; chips 'needs the equations' / 'a rate, not waiting times'",
           assets=["experiences/figures/e1_seuil-en.svg", "proto/scenes/d_curve.html"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine", "proto/data/e1_rate.json"],
           flags=["CAVEAT: cumulative vs pointwise; zero crossings, not reversals (P15); one model, one seed (B16)"],
           motifs=["callback: 'how often' (cold open)", "toll counter callback"], sources=["R:883", "R:528", "D:79-121"],
           was="C8.1"),
        sc("09.2", "Predict: early, late or on time?", "L4", 40,
           "Near the threshold the generator leaks a little below, lags at the threshold and overshoots just above.",
           "Predict card; zoom on 0.80-0.90: tiny spurious crossings below the threshold, a lag at 0.865, an "
           "overshoot at 0.875-0.88 (B17).",
           "'below: up to 2e-4 per unit time (truth: 0) · 0.865: 0.00030 predicted vs 0.00194 true · 0.88: 0.00500 vs 0.00340'",
           data=["experiences/resultats/e1_gissinger.json#grille_fine"],
           predict="Q8: near the threshold, will the predicted crossing rate switch on early, late or on time? (Answer: a "
                   "little leakage below, late at the threshold, then an overshoot just above.)",
           sources=["R:883", "D fine grid"], was="C8.2"),
        sc("09.3", "A stiff sheet on a steep ramp", "L4", 45,
           "A generator that varies smoothly with the knob cannot follow a law whose bridge mass and crossing rate are "
           "born with a steep slope (Proposition 9, attenuated form).",
           "A stiff sheet laid on a steep ramp rounds its knee (no cliff: the symmetrized law varies continuously, A5); "
           "then the generated (Q, D) cloud is swept across the 21 Gamma values next to the reference, with the bridge "
           "mass P(|D| < 0.25) as a bar that leaks a little below, lags at the threshold and overshoots just above "
           "(B17); pen beat on the bound (M9).",
           "chip 'consistent with Prop. 9 · one model, seed 0'; formula layer: W1(q_lambda, q_lambda') <= K |lambda - lambda'|  "
           "=>  max error near lambda_c >= (J_delta - 2 K delta) / 2",
           data=["experiences/resultats/e1_gissinger.json#grille_fine.pont_ref",
                 "experiences/resultats/cache_e1/e1_echantillons_complet.npz"],
           render="dense2d", flags=["LOCAL_ONLY: cache_e1 is gitignored, present on this machine only"],
           motifs=["squeal callback", "M2 knob", "M9 pen"], sources=["R:544-564", "R:883", "R:901"], was="C8.3"),
        sc("09.4", "The loss is not a clean win", "L4", 30,
           "On a good model the crowd loss halves stationarity residuals but narrows dE/dt; on a biased model it fails.",
           "Bars with floors: enforced residual 0.0136 vs 0.0324 (control); distribution distance within the seed "
           "spread; spread ratio 1.04 -> 0.75; the biased model's bars blow off the chart (one seed diverged).",
           "'good model: residuals / 2, spread ratio 0.75 · biased model: one seed diverged, the other worse'",
           assets=["experiences/figures/e1_variantes-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#evaluation"], sources=["R:875-877"], was="C8.4"),
        sc("09.5", "Still far from the data", "L4", 30,
           "The models remain well above the data's own noise floor; few seeds; interpolation only.",
           "Spectral error bars of all variants against the data floor on a log axis; seed counters; 'interpolation' chip.",
           "'spectral error 0.07-0.23 (log10) vs 0.002-0.011 for data · E1: 2 seeds · E2: 1 seed · interpolation only'",
           data=["experiences/resultats/e2_mhd2d.json#evaluation"], sources=["R:80", "R:1039", "R:743-745"], was="C8.5"),
        sc("09.6", "Scoreboard and three lessons", "L4", 40,
           "Eight mechanisms on their shelves, each with a verdict; then three lessons: exact where exact, on the crowd "
           "where statistical, judge against the floor.",
           "Eight cards dealt onto the two shelves of 08.6 (potentials, final projection, projected flow, penalty, "
           "equivariance, stationarity loss, tilting, per-sample projection), each with a verdict icon only (exact / "
           "approximate / harmful); then the three one-line lessons over a motif recap (box, mirror, spike, floor) (F8).",
           "verdict icons; three lessons; the full table (R:1149-1158) goes in the description",
           motifs=["recap beat"], sources=["R:1149-1158"], was="C8.6 + C8.7"),
    ],
}

CH10 = {
    "id": "ch10", "cut": "core", "title": "The climb to 3D: bets on the staircase", "levels": "L4-L5", "was": "C9",
    "learning_goal": "See the PhD proposal as a staircase of test benches and the data factory that will feed it; separate what is "
                     "guaranteed by construction from what must be measured; read each upper step as a pre-registered bet.",
    "takeaway": "Some properties are guaranteed by construction; everything else on the staircase is a bet written down before the "
                "data exist, with the criterion that will settle it.",
    "scenes": [
        sc("10.1", "The staircase", "L4", 25,
           "Here is where we are on the map planted at the start: tiers 0-1 lit by small experiments; tiers 2-4 are the "
           "PhD proposal's bets.",
           "The staircase map of 03.7 returns as a payoff (E1); T1 morph: the 2D square tiles into a 3D periodic box, "
           "which rounds into a cylinder, which starts to precess. Current tier lit.",
           "tier names; chip 'Independent PhD proposal · not requested or validated by the supervisors' (B13)",
           assets=["figures/plan-these/figure/out/plan-these-en.svg"], motifs=["M7 staircase (payoff)"],
           flags=["CAVEAT: proposal only (P27)"], sources=["T:46-56", "T:878-953"], was="C9.1"),
        sc("10.2", "The data factory", "L4", 45,
           "A reproducible pipeline: campaign recipe -> simulations -> labelled files -> catalog -> dataset -> training -> evaluation.",
           "BLUEPRINT register; a kitchen line of grey stations: recipe card (YAML, green knob on it), ovens (local, "
           "Docker, Slurm), jars with checksummed labels (MFF: HDF5 + UUID, commit, SHA-256; C10), ledger (catalog), "
           "tasting menu, chef in training (violet), critic (amber). One sentence on stamps: 'a stamp marks results "
           "from small trial runs; the full runs will replace them' (H6).",
           "'tested end to end on CPU (68 automated tests) · not yet run on a GPU or a real cluster'; stamp legend",
           assets=["figures/architecture/figure/out/architecture-en.svg", "assets/interactif/architecture.js"],
           register="BLUEPRINT", sources=["C:45", "C:88-149", "C:190"], flags=["CAVEAT: HPC not yet run (P25)"], was="C9.2"),
        sc("10.3", "First product off the line", "L4", 15,
           "The first real campaign: ensembles of 2D MHD maps across 11 values of eta, where the dissipation fluctuates "
           "around the constant injected power: the crowd law on fresh data.",
           "A grid of 11 small (omega, j) map tiles, one per eta; under each, the dissipation eps(t) fluctuating around "
           "a flat, labelled line eps_inj (Ito rate) (A3); an amber histogram of eps_inj - eps per eta, centred on "
           "zero. A short beat (F7): the full sweep is in X5.3.",
           "per-eta mean and spread of eps_inj - eps from the data file; stamp 'SIMULATED · palier1_mhd2d · 32^2 · run <id>'",
           data=["data/palier1_sweep.json"], status=P, render="dense2d",
           regen=regen("data/palier1_sweep.json",
                       "11 MFF files {store}/palier1_mhd2d/{uuid}/fields.h5: t1_fields/velocity, magnetic_field (16, 150, 32, 32, 2) float32; "
                       "milady_diagnostics/injection (constant Ito rate, np.full: milady/sim/run.py:256-273), dissipation, kinetic_energy, "
                       "magnetic_energy; catalog rows campaign/simulation/file",
                       "make sweep CONFIG=infra/configs/palier1_mhd2d.yaml  (CPU; the campaign as configured; same workload as the E2 data, about 30 min, X:69)",
                       "tier 1 at full scale (128^2, 8 x 8 (nu, eta) grid, about 700 GPU h, T:898-904): not configured yet",
                       "tools/extract_data.py: palier1_sweep() (to write; replaces the demo stub palier1_eta_sweep()): per eta, "
                       "dissipation series, the flat injection line, histogram of injection - dissipation, one map tile",
                       "empty seat, or E2 samples at eta = 0.00951 only (experiences/resultats/e2_echantillons.npz) stamped PROVISIONAL",
                       None),
           sources=["CFG palier1_mhd2d.yaml", "C:93", "R:442", "R:919"], was="C9.3"),
        sc("10.4", "Bet 1: the ABC windows at 64^3", "L4", 40,
           "The dynamo windows measured at 32^3 should persist and sharpen at 64^3, up to Rm = 40, and the second "
           "threshold should be pinned between Rm = 17 and 18.",
           "The E3 32^3 curve as a grey ghost with its 48^3 check marks (READY anchor, H3); the new points drawn over it "
           "from the data file; windows re-shaded from the new zero crossings; inset 3D mode renders on both sides of "
           "each threshold (meshes precomputed offline, G8).",
           "'bet: windows 8.9 < Rm < 17.5 and Rm > ~27 (published) · s(17) > 0 > s(18), with |s - s_q| below |s|' (A2); "
           "stamp from the data meta",
           assets=["experiences/figures/e3_abc-en.svg"], data=["data/palier2_abc3d.json", "experiences/resultats/e3_abc.json"],
           status=P, render="flat", dur_result=45,
           regen=regen("data/palier2_abc3d.json",
                       "37 MFF files (Rm 4-40 in integer steps, CFG palier2_abc3d.yaml:36): magnetic_field (2, 20, 64, 64, 64, 3); diagnostics "
                       "log_b_rms, growth_rate; catalog diagnostic growth_rate_fit (query: python -m milady.catalog sims --campaign palier2_abc3d); "
                       "plus 3 files at Rm 17.25, 17.5, 17.75 if decision D17 adds them",
                       "copy infra/configs/palier2_abc3d.yaml to $RUNS/configs/palier2_abc3d_n48.yaml with grid.N: 48, name: "
                       "palier2_abc3d_n48_provisional and sweep Rm: [8, 8.5, 9, 9.5, 17, 17.25, 17.5, 17.75, 18, 26, 26.5, 27, 27.5, 28] "
                       "(a list, as in palier2_tg3d.yaml); python -m milady.sweep <copy> --scheduler local --max-parallel 2 --device cpu, "
                       "after --dry-run; duration unmeasured (time one point first). Not at 32^3: it would redraw the E3 curve (H5)",
                       "make sweep CONFIG=infra/configs/palier2_abc3d.yaml  (64^3, integer Rm 4-40; estimate ~15 h serial on 2 CPU threads, "
                       "or GPU / Slurm array) + a copy with Rm: [17.25, 17.5, 17.75] (decision D17)",
                       "tools/extract_data.py: palier2_abc3d() (to write): (Rm, s, s_last_quarter, seed), interpolated thresholds, downsampled modes (.f32)",
                       EMPTY_SEAT + " The E3 32^3 curve is drawn as a labelled ghost.",
                       "published windows 8.9 < Rm < 17.5 and Rm >~ 27 (R:1112); s(17) > 0 > s(18) with |s - s_q| < |s| at both "
                       "(the sign at 17.5 only if the extra points are run)"),
           sources=["CFG palier2_abc3d.yaml", "R:1112-1114"], was="C9.4"),
        sc("10.5", "Bet 2: a dynamo that saturates (Taylor-Green)", "L5", 40,
           "A forced Taylor-Green flow should grow a weak seed field exponentially above a threshold in Rm = Re x Pm, "
           "then saturate where the run is long enough: the first true dynamo of the staircase.",
           "READY anchor first (H3): the Taylor-Green cell flow and a schematic grow-then-saturate curve (chip SCHEMATIC). "
           "Then a grid of log E_B(t) curves, one per (Re, Pm), from the data file: each starts at the 1e-3 seed, grows or "
           "decays, and bends into a plateau where the run is long enough; runs whose kept window is not saturated are "
           "drawn hatched and labelled 'still growing' (A8); a (Re, Pm) map colours each point dynamo / no dynamo / not "
           "saturated. Render flat; an optional 3D insert of saturated B is a separate short WebGL shot (G9).",
           "'anchor: Rm_c = 30 at Pm = 1 (Ponty et al. 2005), different forcing convention: qualitative only'; 'saturated' "
           "flag per run",
           data=["data/palier2_tg3d.json"], status=P, render="flat", dur_result=45,
           regen=regen("data/palier2_tg3d.json",
                       "12 MFF files (Re 25-200 x Pm 0.5-2): velocity and magnetic_field (1, 40, 64, 64, 64, 3) kept for t in [100, 140] "
                       "(CFG palier2_tg3d.yaml:41-43); diagnostics energies, dissipations, injection, helicities, max divergences, growth_rate, "
                       "b_rms, log_b_rms; catalog growth_rate_fit",
                       "copy infra/configs/palier2_tg3d.yaml to $RUNS/configs/palier2_tg3d_n32.yaml (grid.N: 32, new name); "
                       "python -m milady.sweep <copy> --scheduler local --device cpu --indices <Re <= 100, read the order with --dry-run>  "
                       "(estimate 1-1.5 h, unmeasured; check resolution)",
                       "make sweep CONFIG=infra/configs/palier2_tg3d.yaml  (64^3, GPU, 10 h limit per simulation; estimate ~8 h CPU for all 12); "
                       "longer t_burn / t_keep near the threshold if decision D18 says so",
                       "tools/extract_data.py: palier2_tg3d() (to write): per (Re, Pm) time series log E_B(t), fitted rate, saturated E_B, mean "
                       "spectra, and a stationarity flag: saturated only if the slope of log E_B over the kept window is near 0 "
                       "(threshold to fix, e.g. below 10% of the kinematic rate) (A8)",
                       EMPTY_SEAT + " The schematic anchor is shown in both variants.",
                       "qualitative at this scale; saturated runs only; the tier-2 criterion 'Rm_c within 10% at a Pm without data' "
                       "needs the full tier (T:917)"),
           flags=["CAVEAT: Re = 200, Pm = 2 may be under-resolved even at 64^3 (CFG palier2_tg3d.yaml:12-14)",
                  "CAVEAT: with a 1e-3 seed, the kept window t in [100, 140] may still be pre-saturation near the threshold (A8)"],
           sources=["CFG palier2_tg3d.yaml", "T:908"], was="C9.5"),
        sc("10.6", "What is guaranteed", "L5", 25,
           "Generating vector potentials in Coulomb gauge makes div u = div B = 0 to rounding, and the B -> -B mirror "
           "exact, whatever the training quality: it holds even for an untrained network.",
           "The 3D generator with random (untrained) weights emits fields: field lines (violet frame, vermillion lines) "
           "beside the divergence gauge at ~1e-16; the projector motif (M6) shows the potential-to-field step (E4); a "
           "mirror gate maps the sample generated from z onto the one generated from S z. Paired with 10.7 as 'what is "
           "guaranteed' vs 'what must be measured' (H4).",
           "'by construction (Prop. 1, Prop. 4): this shows the mechanism, not quality'; stamp 'GENERATED · fm3d · untrained weights'",
           assets=["milady/train/fm3d.py"], render="webgl",
           flags=["BUILD-TIME DATA: tools/extract_data.py fm3d_guarantees() (to write) builds the fm3d velocity field with random "
                  "weights and unit normalisation on CPU (seconds, needs torch) and writes data/fm3d_guarantees.json (div_rel_u, "
                  "div_rel_b, mirror error); no simulation or training needed, so the scene is READY"],
           motifs=["M6 projector (callback)", "M10 mirror"],
           sources=["C:164-166", "CFG train_fm3d.yaml", "R:327-335", "R:400-412"], was="C9.6"),
        sc("10.7", "What must be measured", "L5", 25,
           "Does the 3D generator get the statistics right? The spectra at the training points face the plan's criterion; "
           "the held-out point (Re = 50, Pm = 2) is a diagnostic; saturated runs only.",
           "READY anchor (H3): a lamp panel with three unlit lamps and the criteria written beside them. Result variant: "
           "spectra E_u(k), E_B(k) simulated (solid) vs generated (dashed, violet chip) at the training points with the "
           "0.1-decade band; the held-out point as a separate panel 'diagnostic, no criterion'; bars vs dashed floor for "
           "train / val / test.",
           "criterion (b) at the training points: log-spectrum error < 0.1 decade per band up to half the cutoff; lamps "
           "labelled 'indicative at 12 x 40 snapshots; plan: about 20 x 5000' (A7); criterion (c) 'Rm_c within 10% at a Pm "
           "without data': later",
           data=["data/fm3d_eval.json"], status=N, render="flat", dur_result=40,
           regen=regen("data/fm3d_eval.json",
                       "evaluation JSON {model, model_id, created, results: [{point, physical_parameters, metrics, details, seconds}]} with err_spectre_u_log10, "
                       "err_spectre_b_log10, residu_bilan_total, dist_energie, plancher_dist_energie; details spectrum_u, spectrum_b, spectrum_u_ref, "
                       "spectrum_b_ref; plus the stationarity flags of 10.5's extractor (A8)",
                       None,
                       "make train CONFIG=infra/configs/train_fm3d.yaml NGPUS=4 (GPU); make eval CONFIG=infra/configs/train_fm3d.yaml [MODEL=<uuid>] "
                       "EVAL_ARGS=\"--out eval_fm3d.json\" (val point Re 100, Pm 1; test point Re 50, Pm 2: CFG train_fm3d.yaml)",
                       "tools/extract_data.py: fm3d_eval() (to write)",
                       EMPTY_SEAT + " The lamp panel and its criteria are the anchor.",
                       "tier-2 criterion (b) of the PhD plan, log-spectrum error < 0.1 decade per band up to half the cutoff, at the training "
                       "points (T:917), indicative only at 12 x 40 snapshots (plan: about 20 x 5000, T:912); held-out and validation points "
                       "are diagnostics; (a) divergence is shown in 10.6; (c) and (d) need the full tier",
                       requires=["10.5 final run (palier2_tg3d at 64^3)", "final fm3d training"]),
           sources=["CFG train_fm3d.yaml", "T:912-917", "milady/eval/metrics.py:588-662, 894-907"], was="C9.7"),
        sc("10.8", "Walls and iron", "L5", 40,
           "Leaving the periodic box changes what 'exact' means: in a bounded domain the potential needs a gauge with a "
           "boundary condition, and across iron the field refracts, so the potential has a kink; matching to the vacuum "
           "outside is linear but nonlocal.",
           "PAPER (T3 ink change): the periodic box rounds into a cylinder; potential arrows at the wall snap to the "
           "boundary condition; an iron disc interface where field lines refract and the potential profile kinks; an "
           "exterior potential field wraps the cylinder. Core merge of X6.1 and X6.2 (B7 of the pedagogy review); the "
           "extended cut plays X6.1 and X6.2 in full instead.",
           "div A = 0 with A.n = 0 or A x n = 0 (Amrouche-Seloula); 'B.n and tangential B / mu_r continuous'; chip "
           "'vacuum matching: candidate routes, an open question of the PhD plan' (C11)",
           register="PAPER", ext={"skip": True, "replaced_by": ["X6.1", "X6.2"]},
           sources=["R:339", "T:114-115", "T:211-266", "T:272"], was="new (merge of X6.1 + X6.2)"),
        sc("10.9", "The top steps: VKS and DRESDYN", "L5", 30,
           "The last two steps need consortium data that are not public: the bets and their criteria are written now.",
           "READY anchor (H3): the VKS and DRESDYN schematics. Two empty seats on the top steps: VKS cylinder (D, Q) "
           "plane with a dashed density frame; DRESDYN Rm_c(Po) axis with a dashed band; each with its data tag. In the "
           "extended cut, the 15-s entry '10.9-bridge' replaces it (H8).",
           "VKS: 4 POD energy fractions within 10% · (D, Q) distribution distance < 2x floor · Rice in the 95% Poisson "
           "interval; DRESDYN: Rm_c within 10% and correct symmetry class at a Po without data",
           assets=["figures/vks/figure/out/vks-en.svg"],
           data=["data/tier3_vks.json", "data/tier4_dresdyn.json"], status=N, dur_result=45,
           ext={"id": "10.9-bridge", "duration_s": 15, "note": "bridge into X6: names the two top steps and hands over"},
           regen=regen("data/tier3_vks.json + data/tier4_dresdyn.json",
                       "SFEMaNS / LATU simulations from the consortium (not public) converted to MFF grid_type fourier_fe_axisym "
                       "(milady_fourier_fe/fields/velocity (B, T, M, 2, N_fluid, 3), magnetic_field ...); generated u fields + kinematic eigenvalues per Po (format to define)",
                       None,
                       "consortium data access; native SFEMaNS reader to write (milady/data/convert.py:9-12); then train / eval as tier 2",
                       "tools/extract_data.py: tier3_vks(), tier4_dresdyn() (to write)",
                       EMPTY_SEAT + " Fallback: VKS schematic + Gissinger as 'pocket dynamo' proxy, chip SCHEMATIC.",
                       "T:927-953 criteria (a)-(d) for VKS, (a)-(b) for DRESDYN"),
           flags=["CAVEAT: no MilaDy data used (P3)"], sources=["T:927-953", "S:100"], was="C9.8"),
    ],
}

CH11 = {
    "id": "ch11", "cut": "core", "title": "Back to the compass", "levels": "L5-L0", "was": "C10",
    "learning_goal": "Separate what was measured from what is bet, and leave with the one-sentence lesson.",
    "takeaway": "We cannot say when the needle will turn, but we are learning to answer how often, by enforcing each law where it is true.",
    "scenes": [
        sc("11.1", "Measured, and bet", "L5", 35,
           "Two columns: what the small experiments measured, and what the staircase bets.",
           "MEASURED column (E1, E2, E3 headline numbers with caveat chips); BET column (tiers 1-4 with data tags and a "
           "status pill READY / PROVISIONAL / PENDING read from timeline.json at build time). Every regenerable data file "
           "is a declared dependency, so the hash-based rebuild re-renders this scene when any of them changes (H2).",
           "headline numbers; status pills",
           data=["proto/timeline.json"], depends_on=REGEN_FILES, sources=["H:80-90"], was="C10.1"),
        sc("11.2", "The compass again", "L0", 70,
           "Closing narration: we cannot say when; we can learn how often; enforce each law where it is true.",
           "The stylized compass of 00.1 returns (no hand). A sequenced montage, one motif per closing sentence, 3-4 s "
           "each (barcode, threads, whirlpools, shoebox, violet cloud, mirror, the amber histogram that keeps its "
           "width), then a fade to the clean compass for the three-line lesson (G6). Rail descends to L0.",
           "numbers as chips only (J): '14% far from the threshold · 42% near it · model C, seed 0'; then the lesson in "
           "three short lines",
           render="webgl", motifs=["M1", "motif montage"], depends_on=REGEN_FILES,
           flags=["NARRATION VARIANTS: paragraph 3 has a pending and a results-in variant keyed to timeline.json (H2)"],
           was="C10.2"),
        sc("11.3", "End card", "L0", 15,
           "Credits, sources, full disclaimer, link to the site.",
           "Static card with a slow field-line drift.",
           "site URL; 'narration: original synthetic voice'; 'animations generated in code'; full disclaimer text "
           "(decision D14); supervisors as listed in the public offer (decision D6)",
           flags=["DISCLAIMER"], was="C10.3"),
    ],
}

# --------------------------------------------------------------------------------------------
# EXTENSION MODULES (inserted after a scene id or after another module)
# --------------------------------------------------------------------------------------------

X2 = {
    "id": "X2", "cut": "extension", "insert_after": "08.7", "title": "The proofs behind the pictures", "levels": "L4", "was": "X2",
    "learning_goal": "State Propositions 1-5 and their scope, as the specialists will want them.",
    "takeaway": "Each picture of ch07-ch08 is backed by an elementary statement with a precise scope, often known in other forms.",
    "scenes": [
        sc("X2.1", "Proposition 1: build it in", "L4", 35,
           "If the decoder's image lies in the constraint subspace, every sample satisfies the constraint, whatever the training quality.",
           "PAPER; statement typed on; a decoder box whose output arrows all land on a plane.",
           "Prop. 1 statement", register="PAPER", sources=["R:327-335"], was="X2.1"),
        sc("X2.2", "Proposition 2 in full", "L4", 50,
           "The optimal flow on a subspace splits into a learnable part and a stiff contraction; a bounded network leaves O(1) residuals.",
           "PAPER; the formula grows term by term; the contraction term 1/(1 - t) is plotted against t (the spring of 08.4); "
           "V3's 2e-8 explained by single precision. Sole home of the formula since 08.4 became intuitive (B3, I5).",
           "v* = m(P x, t) - (I - P) x / (1 - t); Remark 3.6", register="PAPER", sources=["R:345-386"], was="X2.2 (+ C7.4 formula)"),
        sc("X2.3", "Proposition 3: the Jensen gap", "L4", 40,
           "A penalty on the end-of-path prediction is unbiased for linear constraints and biased for nonlinear ones.",
           "A curved constraint arc; the mean of two points falls off the arc: the gap is shaded.",
           "Prop. 3 statement", register="PAPER", sources=["R:389-395"], was="X2.3"),
        sc("X2.4", "Proposition 4: the mirror, proved", "L4", 45,
           "Equivariant velocity + invariant noise give an exactly invariant distribution at every parameter; if each "
           "mu_lambda is symmetric, symmetrization never increases the population loss; it doubles network evaluations.",
           "Mirror gate on the violet flow, then the proof in three lines.",
           "v(g x, t, lambda) = g v(x, t, lambda), g#gamma = gamma => g#q(.|lambda) = q(.|lambda) for every lambda; condition "
           "'if each mu_lambda is G-invariant' on the loss statement (C10); 'cost: 0.5 s vs 0.25 s per 1000 samples'",
           register="PAPER", sources=["R:400-412", "R:885"], flags=["P22: classical for equivariant flows"], was="X2.4"),
        sc("X2.5", "Proposition 5 and its limits", "L4", 40,
           "For every test function, E_mu[L phi] = 0; the energy budget is one case. Necessary, not sufficient: fixed points and unstable orbits satisfy it too.",
           "Amber identity, then a fixed point and an unstable orbit each pass the same test (warning lamp); degree <= 2 "
           "monomials enforced, degree 3 kept as a control. The generator L and the degrees are introduced here, not in the core (B4).",
           "E_mu[L phi] = 0; Remark 3.11; 'enforced: degree <= 2 · control: degree 3'",
           register="PAPER", sources=["R:422-430", "R:569-571", "R:434", "R:727"], was="X2.5"),
    ],
}

X3A = {
    "id": "X3a", "cut": "extension", "insert_after": "X2", "title": "Crowd laws, deeper", "levels": "L4", "was": "X3.1-X3.4",
    "learning_goal": "Define the distribution distance, understand exponential tilting as an I-projection and why it cannot create mass, "
                     "and read the per-eta detail.",
    "takeaway": "Reweighting cannot visit places the model never went.",
    "scenes": [
        sc("X3.0", "The distribution distance, defined", "L4", 20,
           "The energy distance compares two crowds through average pairwise distances; it is zero only when the crowds have the same law.",
           "The formula built term by term over two point clouds with faint pairwise lines (moved from 06.5, F).",
           "E(P, Q) = 2 E||X - Y|| - E||X - X'|| - E||Y - Y'||; 'called distribution distance in the film' (D2)",
           register="PAPER", sources=["R:715-725"], was="new (from C6.5)"),
        sc("X3.1", "The least-distorting correction", "L4", 40,
           "Exponential tilting is the I-projection: the reweighting that fixes a mean with minimal KL change, without moving any sample.",
           "Dots whose size is their weight; the tilted density slides to the target mean; Pythagorean triangle for KL.",
           "q* = e^(beta . g) q / Z(beta);  beta* = argmin log Z(beta) - beta . c (Csiszar 1975); supp q* = supp q (q* for the tilted law, D3)",
           assets=["prep/p5-probabilites-transport/fig-inclinaison-en.png", "prep/p8-contraintes-physiques/fig-inclinaison-en.png"],
           sources=["R:465-485"], was="X3.1"),
        sc("X3.2", "The poll that shrank", "L4", 45,
           "Effective sample size collapses exactly where the model is poor.",
           "Per-eta ESS bars from the data: 0.99 at the easiest eta, 0.002 at the three largest test eta, about one "
           "effective sample in 500 (B10); in E1 one sample swells to 33x the mean weight.",
           "ESS = 1 / sum w_i^2; 'E2: mean ESS/N 0.29 · 0.002 at large eta (1 in 500) · E1 Gamma = 0.85: ESS/N 0.67, one weight 33x the mean'",
           data=["experiences/resultats/e2_mhd2d.json#en_loi.ess_frac_b", "experiences/resultats/e1_gissinger.json#evaluation"],
           sources=["R:1033", "R:879", "D:162"], was="X3.2"),
        sc("X3.3", "Where the model never went", "L4", 35,
           "No weight can conjure samples in a region the model never produced; tilting is not a fallback.",
           "The 'missing support' toggle of the distributional widget: the bridge region is empty, weights explode, ESS counter falls.",
           "'reweighting cannot create mass'", assets=["assets/interactif/contrainte-loi.js"], sources=["R:465-485", "T:988-1000"],
           was="X3.3"),
        sc("X3.4", "Per-eta detail", "L4", 30,
           "The crowd loss helps where the base model is worst and does nothing where it is already good.",
           "Three grouped bars per test eta (V4 / control / V5), distribution distance.",
           "'eta 0.01903: 7.74 / 7.63 / 2.22 · 0.01345: 3.63 / 3.51 / 0.792 · 0.00476: 0.184 / 0.178 / 0.186 · V4 signed residual +1.22 at 0.01903'",
           data=["experiences/resultats/e2_mhd2d.json#en_loi"], sources=["R:999-1013"], was="X3.4"),
    ],
}

X4A = {
    "id": "X4a", "cut": "extension", "insert_after": "09.6", "title": "What snapshots can and cannot tell", "levels": "L4-L5",
    "was": "X4.1-X4.3 + X4.5",
    "learning_goal": "Know the Rice estimator's bias and variance and its test conditions, the threshold bound on reversal rates, why "
                     "waiting times need dynamics, and the next round of tier 0.",
    "takeaway": "A snapshot generator bounds and estimates rates, but waiting times need the dynamics; tier 0 needs more seeds and a "
                "joint mirror.",
    "scenes": [
        sc("X4.1", "Rice, the estimator", "L4", 40,
           "The window estimator has bias O(h^2) and variance O(1/(N h)); E1 uses h = 0.2. It needs the right-hand side, and "
           "it was validated on a 3-variable deterministic system only.",
           "A slider on h trades a blurry strip against a noisy count; sanity checks: a cosine crosses twice per period; "
           "Gaussian case; two caveat cards moved from 05.4.",
           "bias O(h^2), variance O(1/(N h)); Gaussian: r_0 = sigma' / (pi sigma); 'needs F' · 'tested on a 3-variable deterministic system'",
           sources=["R:510-528", "R:703-709", "R:901"], was="X4.1 (+ C5.4 caveats)"),
        sc("X4.2", "A bound from thresholds", "L5", 40,
           "Counting crossings of levels +/- a bounds the reversal rate: r <= r_a (Prop. 2.30); the plateau conjecture 2.33 says when the bound is tight.",
           "Rates of crossings of +/- a vs a, from reference and generated snapshots, with the true reversal rate as a floor line; tightness band.",
           "r <= r_a (Prop. 2.30; r = reversal rate, r_a = rate of crossings of +/- a, D3); Conjecture 2.33; tier-0 criterion 'bound tight within 30%'",
           data=["data/x4_rice_levels.json"], status=P,
           regen=regen("data/x4_rice_levels.json",
                       "E1 reference trajectories (re-integrated, CPU minutes) and generated samples at all 21 Gamma (experiences/resultats/cache_e1/e1_echantillons_complet.npz, local only)",
                       "new extractor rice_levels(): level-a crossing rates on re-integrated Gissinger trajectories + Rice at level a on generated samples (CPU, minutes; code to write)",
                       "tier-0 campaign with 1e6 snapshots per parameter and 3 seeds (T:878-890, CPU, about 1e3 h assumption)",
                       "tools/extract_data.py: rice_levels() (to write)",
                       EMPTY_SEAT,
                       "Prop. 2.30 bound tight within 30% (T:878-890)"),
           sources=["T:683-727"], was="X4.2"),
        sc("X4.3", "Waiting times need the movie", "L5", 35,
           "The one-time law does not determine the distribution of waiting times (Prop. 2.32); in the three-mode model they are quantized at short times and Poissonian at long times.",
           "Histogram of waiting times between reversals from a long live integration at Gamma = 0.90, with the short-time comb and the exponential tail.",
           "Prop. 2.32; 'quantized short, Poissonian long'", render="dense2d",
           sources=["T:683-727", "P4:1541"], was="X4.3"),
        sc("X4.5", "Tier 0, the next round", "L5", 30,
           "Three seeds, a derived reversal model (DQVU) and a joint state-parameter mirror R_pi that also flips the forcing asymmetry.",
           "Gissinger panel gains a third seed lane; a DQVU card (Re 1594, Rm 531, asymmetry 0.058, iron mu_r 16, POD on 2000 "
           "snapshots); R_pi mirror flips both the state and the asymmetry knob. The staircase is known since 03.7, so tiers "
           "can be named here (I3).",
           "Prop. 2.24; tier-0 criteria: asymmetry below floor at all Gamma, non-enforced residuals / 2 vs control, Rice within 20%",
           data=["data/x4_tier0.json"], status=P, dur_result=35,
           regen=regen("data/x4_tier0.json",
                       "E1-style JSON (per-parameter metrics, fine-grid Rice) with 3 seeds; DQVU results later",
                       "run experiences/e1_gissinger.py from a working copy with seeds {0, 1, 2} (seeds are fixed in code; about 3-4.5 h CPU: "
                       "X:71 gives 2-3 h for two seeds, unless the seed-0/1 caches in cache_e1 are reused) (C12), then experiences/digest.py",
                       "tier-0 plan (T:878-890); DQVU needs the published coefficients (Bousquet et al. 2026 appendix); no DQVU code in the repository",
                       "tools/extract_data.py: tier0() (to write)",
                       "E1 two-seed results with a '2 seeds' chip",
                       "T:878-890 criteria"),
           sources=["T:878-890", "T:931", "S:98", "T:613"], was="X4.5"),
    ],
}

X5A = {
    "id": "X5a", "cut": "extension", "insert_after": "10.3", "title": "The factory floor", "levels": "L4", "was": "X5.1-X5.4",
    "learning_goal": "Open the data factory: one solver step, one file, one campaign trace, a new metric.",
    "takeaway": "Reproducibility is designed in: every number on screen traces back to a file, a commit and a catalog row.",
    "scenes": [
        sc("X5.1", "One solver step", "L4", 40,
           "A pseudo-spectral MHD step goes back and forth between Fourier and physical space, with 2/3 dealiasing and an integrating-factor RK4.",
           "BLUEPRINT; a field tile hops between a Fourier grid and a physical grid; the 2/3 mask trims the corners; memory bar "
           "for the state 6 N^3 x 4 bytes, with the measured-peak factor drawn separately (B14).",
           "'64^3 dynamic step: 0.08 s on 2 CPU threads · state 0.4 GB at 256^3 · peak about 15x the state: about 6 GB at 256^3, "
           "about 48 GB at 512^3 (estimates from a 128^3 measurement)'",
           assets=["figures/solveur/figure/out/solveur-en.svg"], register="BLUEPRINT", sources=["C:153", "C:176"], was="X5.1"),
        sc("X5.2", "A jar with a label", "L4", 35,
           "Each simulation is one MFF file (HDF5, The Well convention) with UUID, commit and checksum, mirrored by a catalog row.",
           "File tree unfolds: t1_fields/velocity, magnetic_field, milady_diagnostics/*, scalars; a ledger row lights with the same UUID.",
           "MFF tree; catalog tables campaign, simulation, file, diagnostic, dataset, model, evaluation, job; 'checksummed, "
           "--force rewrites and updates the SHA-256' (C10)",
           assets=["figures/solveur/figure/out/solveur-en.svg"], register="BLUEPRINT", sources=["C:93", "C:107-139"], was="X5.2"),
        sc("X5.3", "The life of one campaign", "L4", 40,
           "From one command to files and catalog rows: a real trace with measured wall times, then the 11 eta tiles of 10.3 in full.",
           "Terminal-style trace (mono) of a sweep: jobs light up, jars fill, ledger rows appear with wall_time_s; numbers "
           "from the run, not typed; ends on the full per-eta sweep (tiles, flat injection line, histograms) (F7).",
           "command line; counts and wall times from the data file",
           data=["data/x5_campaign_trace.json"], status=P, register="BLUEPRINT",
           regen=regen("data/x5_campaign_trace.json",
                       "catalog dump of the palier1_mhd2d campaign (simulation rows with wall_time_s, file sizes, checksums)",
                       "same run as 10.3 (make sweep CONFIG=infra/configs/palier1_mhd2d.yaml), then python -m milady.catalog sims --campaign palier1_mhd2d",
                       "the same trace on the GPU VM or Slurm cluster for a palier2 campaign",
                       "tools/extract_data.py: campaign_trace() (to write)",
                       "architecture.js walk-through with a SCHEMATIC chip (no numbers)",
                       requires=["10.3 provisional run"]),
           sources=["C:143-149", "IR:386"], was="X5.3"),
        sc("X5.4", "A new instrument for the critic: counting X-points", "L4", 35,
           "Topology metrics were requested by the internship offer and not yet computed: count saddle (X) and extremum (O) points of the magnetic potential.",
           "Contours of the magnetic potential a with X-points (crosses) and O-points (dots) marked, reference vs generated variants; a check "
           "badge 'saddles = extrema on the torus (Poincare-Hopf)'.",
           "per-variant X-point counts; chip '8 samples per variant: provisional'",
           data=["data/x5_xpoints.json", "experiences/resultats/e2_echantillons.npz"], status=P, render="dense2d",
           regen=regen("data/x5_xpoints.json",
                       "experiences/resultats/e2_echantillons.npz (8 samples x variants at eta = 0.00951); later palier1 / tier-1 MFF fields",
                       "new extractor xpoints(): reconstruct a on 32^2 (or 64^2 by zero-padding) and count critical points (CPU, minutes; code to write)",
                       "same metric on palier1_mhd2d and tier-1 data (T:872-876, T:902)",
                       "tools/extract_data.py: xpoints() (to write)",
                       EMPTY_SEAT,
                       "distribution of X-point counts generated vs reference (T:872-876)"),
           flags=["P20: no topology metrics were computed in the report"], sources=["R:739", "T:872-876"], was="X5.4"),
    ],
}

X1 = {
    "id": "X1", "cut": "extension", "insert_after": "X5a", "title": "Inside the twisting box (E3 in depth)", "levels": "L4", "was": "X1.1-X1.3",
    "learning_goal": "See how the 3D solver is validated, what the dominant mode looks like, and how precise the thresholds are: the provenance of Bet 1.",
    "takeaway": "The 3D test bench passes an exact check and recovers the known windows, with honest limits on precision.",
    "scenes": [
        sc("X1.1", "A built-in answer key", "L4", 35,
           "B = u is an exact eigenmode of the ABC flow decaying at -1/Rm, so the dominant rate can be no lower than -1/Rm = "
           "-0.5 at Rm = 2; the solver finds -0.5001.",
           "A gauge lands on -0.5001 next to the exact bound -0.5.",
           "'exact mode: -1/Rm = -0.5 · dominant rate >= -0.5 · measured: -0.5001' (B8)",
           data=["experiences/resultats/e3_abc.json#taux"], sources=["R:1116"], was="X1.1"),
        sc("X1.2", "The mode in 3D", "L4", 45,
           "The dominant mode (least damped or fastest growing) at Rm 8, 12, 16 and 20: below, inside and just after the first window.",
           "Fat vermillion field lines and a |B| isosurface, precomputed offline (spectral upsampling, marching cubes, "
           "field-line tracing in extract_data.py -> .f32 meshes and polylines, G8), orbiting slowly; a symmetry badge.",
           "badge 'published: the first-window mode has all even symmetries of a 24-element group (Bouya and Dormy 2013); "
           "not checked on these modes' (B7); no second-window mode is stored",
           data=["experiences/resultats/e3_modes.npz"], render="webgl", sources=["R:1077", "R:1092", "R:1120"], was="X1.2"),
        sc("X1.3", "How sure are the thresholds?", "L4", 35,
           "48^3 agrees at Rm 12; at 17.5 the sign flips between resolutions, so it is unresolved; the third threshold is "
           "known to about one unit.",
           "Zoom on Rm = 17.5 with three tiny markers straddling zero (+2.3e-4 and -2.2e-4 at 32^3, -5.2e-4 at 48^3); the "
           "48^3 check markers moved here from 03.4 (F3); divergence gauge 3e-19 to 1.5e-16.",
           "'48^3: s = 0.00812 at Rm 12 (agrees) · at 17.5: +2.3e-4 (32^3) vs -5.2e-4 (48^3): unresolved' (B9)",
           data=["experiences/resultats/e3_abc.json#convergence"], sources=["R:1114", "R:1118", "D:197"], was="X1.3"),
    ],
}

X4B = {
    "id": "X4b", "cut": "extension", "insert_after": "10.5", "title": "Steep slopes and the branch", "levels": "L5", "was": "X4.4",
    "learning_goal": "Know the square-root bound near a supercritical threshold and the branch-conditioning conjecture near a subcritical one.",
    "takeaway": "Near a subcritical threshold, conditioning on the branch could remove the smoothing error; it is a bet.",
    "scenes": [
        sc("X4.4", "Steep slopes and the branch", "L5", 25,
           "Near a supercritical threshold a smooth generator obeys a square-root bound (Prop. 2.36); near a subcritical one, conditioning on the branch could remove it (Conjecture 2.38).",
           "READY anchor: a hysteresis loop drawn by a knob going up then down on the Taylor-Green picture of 10.5; two "
           "branches; an empty seat for 'error at threshold with vs without branch conditioning'.",
           "Prop. 2.36; Conjecture 2.38; criterion 'error at threshold / 2 with branch conditioning'",
           data=["data/x4_branch.json"], status=N, dur_result=40,
           regen=regen("data/x4_branch.json",
                       "tier-2 full-scale campaign with hysteresis runs (Taylor-Green, up and down sweeps) + branch-conditioned model and its evaluation",
                       None,
                       "not configured beyond palier2_tg3d / train_fm3d (T:912-918; about 3900 GPU h for tier 2)",
                       "tools/extract_data.py: branch_conditioning() (to write)",
                       EMPTY_SEAT,
                       "error at the threshold divided by 2 with branch conditioning (T:917 (d))",
                       requires=["10.5 final run", "a hysteresis campaign (not configured)"]),
           sources=["T:768-788", "T:917"], was="X4.4"),
    ],
}

X3B = {
    "id": "X3b", "cut": "extension", "insert_after": "10.7", "title": "The crowd law in 3D", "levels": "L5", "was": "X3.5",
    "learning_goal": "See the 3D version of the crowd-loss experiment as a bet with an adapted criterion.",
    "takeaway": "The crowd loss must be tested again in 3D, against a control run, without narrowing the dissipation.",
    "scenes": [
        sc("X3.5", "Bet: the crowd law in 3D", "L5", 25,
           "Does the distribution-level budget loss still help in 3D, without narrowing the dissipation, against a control run of equal length?",
           "READY anchor: the three-lane race of 08.5 redrawn as empty seats for the 3D model: budget residual before / "
           "after, control lane, dissipation-spread gauge (needs a new metric). Saturated runs only (A8).",
           "'bet adapted from the tier-1 criteria (the plan sets none for 3D): residual down, sigma(eps)/sigma_ref in [0.8, 1.2], "
           "control gains nothing' (A9, D4)",
           data=["data/fm3d_stationarity.json"], status=N, dur_result=35,
           regen=regen("data/fm3d_stationarity.json",
                       "second fm3d model fine-tuned with the stationarity loss + control run (weight 0) + evaluation JSONs (residu_bilan_total, dist_energie, "
                       "plus a per-sample spread of the budgets, NOT computed by milady.eval today: C:166); stationarity flags from 10.5",
                       None,
                       "python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml --init-from <final.pt> --set stationarity.enabled=true "
                       "stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0; same command with the loss weight set to 0 "
                       "for the control (key name to check in train_fm3d.yaml); python -m milady.eval ... --out <file> for both",
                       "tools/extract_data.py: fm3d_stationarity() (to write) + add the sigma(dissipation) metric to milady.eval in the compute clone",
                       EMPTY_SEAT,
                       "adapted from tier-1 criteria (b) budget residual < 5% at parameters without data and (d) dissipation spread ratio "
                       "0.8-1.2 (T:903); the plan's tier-2 criteria set no budget target (T:917); control run gains nothing; saturated runs only",
                       requires=["10.7 final fm3d model", "sigma(dissipation) metric in milady.eval"]),
           flags=["RISK: stationarity-loss variance in 3D (T:992)"], sources=["CFG train_fm3d.yaml:13-15", "C:166", "T:903", "T:917"],
           was="X3.5"),
    ],
}

X6 = {
    "id": "X6", "cut": "extension", "insert_after": "10.9", "title": "Walls, metals and meshes", "levels": "L5", "was": "X6 + X1.4",
    "learning_goal": "Meet the specialist frontier: conventions for Rm, gauges in bounded domains, permeability jumps, vacuum matching, "
                     "hybrid meshes, VKS and DRESDYN bets, and downstream assimilation.",
    "takeaway": "Leaving the periodic box changes what 'exact' means, and the real tests (VKS, DRESDYN) are written down as bets.",
    "scenes": [
        sc("X6.0", "Which Rm?", "L5", 25,
           "Published VKS thresholds depend on the definition of Rm; a model conditioned on Rm must fix its convention.",
           "The same VKS impeller with labels sliding on: about 31 with the impeller efficiency factor K, 52-71 without it; "
           "a third card 'another definition (Miralles et al. 2013)' without a number (B15).",
           "'Rm_c ~ 31 (Monchaux 2007, with K) · 52-71 (Nore 2018, without K) · Miralles 2013: another definition'",
           assets=["figures/vks/figure/out/vks-en.svg"], sources=["R:141", "P3:1202"],
           flags=["SITE NOTE: P3:1167 gives 'Rm_c ~ 44 (Miralles)' while P3:1202 converts Miralles to about 1.05 x Nore; the film omits 44 (decision D19)"],
           was="X1.4"),
        sc("X6.1", "A gauge for a bounded world", "L5", 45,
           "In a bounded domain the vector potential needs a fixed gauge (Coulomb, with A.n = 0 or A x n = 0), or its distribution is not well defined.",
           "The periodic box rounds into a cylinder; potential arrows at the wall snap to the boundary condition; two gauge "
           "choices side by side; the projector motif (M6) returns (E4).",
           "div A = 0, A.n = 0 or A x n = 0 (Amrouche-Seloula)", register="PAPER",
           motifs=["M6 projector"], sources=["R:339", "T:211-260"], was="X6.1"),
        sc("X6.2", "Iron changes the rules", "L5", 40,
           "Across a permeability jump, B.n and tangential B/mu_r are continuous: the potential has a kink; matching to vacuum outside is linear but nonlocal.",
           "An iron disc interface: field lines refract; the potential profile shows a kink; an exterior potential field wraps the cylinder.",
           "Prop. 2.6; Remark 2.5; chip 'vacuum matching without a Laplace solve per sample: a candidate route, an open "
           "sub-question of Q1' (C11)", register="PAPER",
           sources=["T:114-115", "T:259-266", "T:272"], was="X6.2"),
        sc("X6.3", "Two scalars and a hybrid mesh", "L5", 40,
           "Poloidal-toroidal storage (Prop. 2.8) in the box; SFEMaNS data are azimuthal Fourier modes times meridian finite elements, where div B is only weakly controlled.",
           "A meridian triangle mesh revolves into Fourier modes; a divergence gauge relabels itself 'with the solver's operator'.",
           "Prop. 2.8; MFF extension milady_fourier_fe; 'native SFEMaNS reader not implemented'",
           register="PAPER", flags=["P16 operator caveat"], sources=["T:324", "T:341", "R:1185", "milady/data/convert.py:9-12"], was="X6.3"),
        sc("X6.4", "Bet 4: VKS in the generator", "L5", 30,
           "With consortium data, the generator should reproduce the dominant POD modes, the bimodal and asymmetric (D, Q) law, and a Rice rate within the Poisson interval.",
           "READY anchor: the VKS cylinder. An empty (D, Q) density frame (dashed), four empty POD bars with 10% bands, a "
           "Rice gauge with a Poisson interval.",
           "criteria (a)-(d) of the PhD plan; joint mirror R_pi flips the asymmetry parameter (Prop. 2.24)",
           data=["data/tier3_vks.json"], status=N, render="webgl", dur_result=45,
           regen=regen("data/tier3_vks.json",
                       "SFEMaNS / LATU VKS simulations (non-public): 384^3-equivalent snapshots ~1.4 GB each, 2000 snapshots ~2.7 TB; filtered 128^3 ~100 GB; "
                       "MFF grid_type fourier_fe_axisym",
                       None,
                       "consortium data access; SFEMaNS reader (to write); training and evaluation as tier 2 (about 3200 GPU h, T:968)",
                       "tools/extract_data.py: tier3_vks() (to write)",
                       EMPTY_SEAT + " Fallback: figures/vks schematic + Gissinger 'pocket dynamo' proxy (SCHEMATIC).",
                       "4 POD energy fractions within 10%; (D, Q) distribution distance < 2x floor; interface residual < 1%; Rice in 95% Poisson CI (T:939)"),
           assets=["figures/vks/figure/out/vks-en.svg"], flags=["CAVEAT: data not public (P3)"], sources=["T:927-939"], was="X6.4"),
        sc("X6.5", "Bet 5: DRESDYN, the precession knob", "L5", 25,
           "From generated velocity fields, recover the dynamo threshold Rm_c(Po) and the symmetry class of the dominant mode at a Po without data.",
           "READY anchor: the precessing cylinder (green Po knob). An empty Rm_c(Po) chart with a 10% band and a symmetry-class badge left blank.",
           "criteria (a)-(b) of the PhD plan; qualitative reference Botez et al. 2026",
           data=["data/tier4_dresdyn.json"], status=N, render="webgl", dur_result=35,
           regen=regen("data/tier4_dresdyn.json",
                       "SFEMaNS precession simulations at the partners; generated u fields + kinematic eigenvalue results per Po (format to define)",
                       None,
                       "partner data; kinematic eigenvalue solver on generated flows (about 1200 GPU h for tier 4, T:968)",
                       "tools/extract_data.py: tier4_dresdyn() (to write)",
                       EMPTY_SEAT,
                       "Rm_c within 10% and correct symmetry class at a Po without data (T:941-953)"),
           sources=["T:941-953", "S:100"], was="X6.5"),
        sc("X6.6", "Downstream: assimilation with a mirror", "L5", 35,
           "A generator as a prior: the reduced drift by conditional expectation (Prop. 2.40); with a mirror-symmetric prior, a "
           "dipole observation near zero gives a posterior with two mirror humps whose mean is not a physical state (Prop. 2.41).",
           "Observation dots near zero pull a violet ensemble; the posterior splits into two mirror humps and its mean marker "
           "falls between them, on no physical state; a lopsided prior would wrongly favour one hump; an equivariant prior "
           "handles it exactly (symmetric pairs, or a latent 4D-Var started from z and S z) (A1).",
           "Prop. 2.40; Prop. 2.41 (i)-(ii)", motifs=["M10 mirror callback"], sources=["T:816-843"], was="X6.6"),
    ],
}

X5B = {
    "id": "X5b", "cut": "extension", "insert_after": "X6", "title": "The bill and the plan", "levels": "L5", "was": "X5.5-X5.6",
    "learning_goal": "See the compute bill, its uncertainty and the 36-month plan on one page.",
    "takeaway": "The bill is estimated with at least a factor-two uncertainty, and every estimate will be replaced by a measured number.",
    "scenes": [
        sc("X5.5", "The bill", "L5", 30,
           "The plan budgets about 1.1e4 A100 GPU hours, with an uncertainty of at least a factor of two; measured costs will replace the estimates.",
           "Stacked bar per tier (tier 1 ~700, tier 2 ~3900, tier 3 ~3200, tier 4 ~1200, 20% reserve) with a dashed second bar for measured hours, filled from the catalog.",
           "'plan: ~1.1e4 GPU h, uncertainty at least x2 · anchor: PCDM ~1150 GPU h' (C11)",
           data=["data/x5_compute_bill.json"], status=N, register="BLUEPRINT", dur_result=40,
           regen=regen("data/x5_compute_bill.json",
                       "GPU solver benchmarks + catalog wall_time_s per campaign and per training run",
                       None,
                       "python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50 (IR:436); catalog SQL on simulation.wall_time_s (C:143-147)",
                       "tools/extract_data.py: compute_bill() (to write)",
                       "planned numbers only (T:955-974), each chip 'estimate'",
                       "within the plan's band of at least a factor of two (T:974)"),
           sources=["T:955-974"], was="X5.5"),
        sc("X5.6", "The plan on one page", "L5", 45,
           "36 months, three axes, five tiers, three papers, named risks; chosen after scoring six directions.",
           "The thesis timeline SVG animated bar by bar (tiers, visits, committees, code releases, papers at months 10, 22, 33); "
           "risk cards; a small score table (A 4.10, B 3.90, merged).",
           "'papers: month 10 (distributional constraints) · 22 (hard constraints in bounded domains) · 33 (reversals and threshold)'",
           assets=["figures/plan-these/figure/out/plan-these-en.svg", "en/these/index.qmd"],
           flags=["CAVEAT: independent proposal, not requested or validated by the supervisors (P27, B13)"],
           sources=["T:1014-1126", "S:418-453", "T:988-1000"], was="X5.6"),
    ],
}

CORE = [CH00, CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH09, CH10, CH11]
MODULES = [X2, X3A, X4A, X5A, X1, X4B, X3B, X6, X5B]

TWO_EPISODES = {
    "part1": ["ch00", "ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"],
    "part2": ["ch08", "ch09", "ch10", "ch11"],
    "part2_recap_s": 60,
    "note": "Part 2 opens on a 60-s 'previously' scene (needle, shoebox, Rice, violet cloud, lopsided machine, mirror) (I6); "
            "ch07 (the mirror) closes Part 1 with its cliffhanger and payoff. Part 2 carries all extension modules.",
}

RESULTS_UPDATE = {
    "recap_s": 45,
    "scenes": ["10.3", "10.4", "10.5", "X4.4", "10.7", "X3.5", "10.9", "X6.4", "X6.5", "11.1"],
    "note": "Stand-alone 'Results update' episode (H1): a 45-s recap of 10.1, then the regenerable scenes in their result "
            "variants, then 11.1. Scenes whose data are still missing are dropped from the episode, not shown empty. The full "
            "film is re-published as v2 on the site and the GitHub release, with a pinned link from the original upload.",
}

# --------------------------------------------------------------------------------------------
# TEXT BLOCKS
# --------------------------------------------------------------------------------------------

TITLE = "How Often Does the Field Flip?"
SUBTITLE = "Teaching generative models the physics of dynamos, from a compass to the research frontier"
TITLE_OPTIONS = [
    "How Often Does the Field Flip?",
    "Exact Where It Is Exact: physics-constrained generative models for dynamos",
    "The Compass and the Crowd",
]

LOGLINE = ("No one can yet say when Earth's magnetic field will flip next, but in the dynamos we can compute, we can learn "
           "how often. One film climbs from a compass to the frontier of physics-constrained generative AI for dynamos.")

SYNOPSIS = ("It opens on a compass needle that flips and on the striped seafloor, then builds the physics picture by picture: "
            "stretch versus smudge, thresholds, and a liquid-sodium experiment, VKS, that flips like the Earth. "
            "Chaos hides the date of the next flip, yet a shuffled box of snapshots, plus the equations, still holds the "
            "crossing rate, through Rice's formula. Generative models then learn to dream such snapshots between the knob "
            "settings that were simulated. At its heart is one lesson from an independent, prospective internship study "
            "around the MilaDy project: enforce each law where it is true, exactly for every field, or on average for the crowd. "
            "Small CPU experiments show what works and what fails. "
            "It ends on written bets for 3D dynamos, VKS and DRESDYN, filled in as simulations arrive.")

OPENING = {
    "scenes": ["00.1", "00.2", "00.3", "00.4"],
    "tts_text": (
        "[calm, natural narrator voice] This needle has pointed north your whole life. "
        "Rocks on the ocean floor say it has pointed south too. Again and again, with no schedule. [long pause] "
        "That needle follows a field that wraps the whole planet. It feels permanent. It is not. "
        "Along the ridges of the ocean floor, fresh lava cools, and tiny magnetic grains freeze in place, "
        "each remembering which way a compass pointed. As the seafloor spreads, they line up into stripes "
        "of very uneven widths. [long pause] "
        "So, two questions. When will it flip next? And how often does it flip? "
        "In the dynamos we can compute, the first question turns out to be hopeless. The second one is not. "
        "Finding out why takes us from this needle to liquid metal, to chaos, and to machines that dream up magnetic "
        "fields, and must learn where physics is exact, and where it only holds on average."
    ),
    "cue_map": [
        ["This needle has pointed", "00.1 (needle flips on 'pointed south too')"], ["That needle follows", "00.2"],
        ["Along the ridges", "00.3"], ["So, two questions", "00.4 (violet teaser on 'machines that dream')"],
    ],
    "notes": "The reversal lands at about 7 s and the two questions at about 0:34 (A1). Per-scene word budgets now match the "
             "cue map at about 135 words per minute (A2): about 25 / 16 / 36 / 68 words for 11 / 7 / 16 / 30 s. The seafloor sentences rely on an external "
             "fact (decision D7). Site-only alternative for 00.3: 'In a tank of liquid sodium in Cadarache, the field flips too.'",
}

CLOSING = {
    "scenes": ["11.2"],
    "tts_text": (
        "[calm, natural narrator voice] Back to the compass in your hand. [long pause] "
        "We still cannot tell you when this needle will turn around. In the dynamos we can compute, chaos erases the "
        "memory of the present too fast. But those dynamos do answer another question: how often. That answer hides in a "
        "cloud of snapshots, and a machine can learn to draw such clouds, even between the settings that were simulated. [long pause] "
        "On small test problems, it partly works. The mirror symmetry holds by construction. "
        "On a three-variable model, the rate at which the dipole crosses zero comes out roughly right far from the tipping "
        "point, and poorly right at it, because a smooth machine cannot follow a steep change. "
        "The real tests, in three dimensions and in liquid metal, are still ahead. You have seen the bets. [long pause] "
        "One lesson remains. Enforce each law where it is true. Exactly, where it is exact. On average, where it only holds on average."
    ),
    "variant_results_in": (
        "Paragraph 3, used when timeline.json marks at least one of 10.4, 10.5 or 10.7 as final: 'On small test problems, it "
        "partly works. The mirror symmetry holds by construction. On a three-variable model, the rate at which the dipole "
        "crosses zero comes out roughly right far from the tipping point, and poorly right at it. In three dimensions, the "
        "first bets are now settled: {bets_met} of {bets_total} criteria met. The tests in liquid metal are still ahead.'"
    ),
    "cue_map": [
        ["Back to the compass", "11.2 compass"], ["We still cannot", "montage: barcode, whirlpools, shoebox"],
        ["On small test problems", "montage: mirror, histogram; E1 numbers as chips"], ["One lesson remains", "clean compass, three-line lesson"],
    ],
    "notes": "Numbers are on chips, not spoken (J); the narration says 'crosses zero' (B16) and follows pitfall P15. 'Holds by "
             "construction' refers to Proposition 4. Paragraph 3 has two variants keyed to timeline.json (H2).",
}

SYMBOLS = [
    "s: growth rate of the field (real part); never lambda (D1)",
    "lambda: a generic knob, always green; name the specific knob whenever there is one (Gamma, eta, Rm, Re, Pm, Po)",
    "D: the dipole, everywhere; eps: dissipation (never sigma(D) for its spread: sigma(eps)) (D4)",
    "r_0: rate of zero crossings of D; r: reversal rate; r_a: rate of crossings of +/- a (Rice, D3)",
    "Gissinger coefficients: numbers only (0.119, 0.1), no mu or nu on screen (D3)",
    "q: generated law; q*: tilted law (never nu*) (D3)",
    "mu_Gamma, mu_+/-: stationary laws, only in X2 and X4; in the core, 'the long-exposure glow (stationary distribution)' (B5)",
    "mu_r: 'iron (permeability)' in words until L5 (D3)",
    "'distribution distance' (amber) on screen and in narration; 'energy distance' only as a technical chip in 06.5 and in X3.0 (D2)",
    "'crossing rate' on screen; 'how often it flips (counted as crossings)' in the closing (D5)",
    "t: transport time of the generator in [0, 1]; v_theta: generator velocity (violet); u: fluid velocity (blue) (06.2)",
    "C1-C4: the report's constraint classes, on screen only in the formal row of 08.6; chapter ids are ch00-ch11 (D6)",
    "Lip(phi): Lipschitz constant (never L, which is the generator of the dynamics) (B6)",
]

QUESTIONS = [
    {"id": "D1", "topic": "Narrator voice", "status": "open (unchanged)",
     "question": "Which original narrator voice (Fish Audio reference_id) should read the film? The film will not clone or imitate "
                 "any real person. The session task list mentions a voice called 'Ethan': if that is an original or licensed "
                 "library voice, please confirm and give its reference_id.",
     "options": ["an original Fish Audio library voice: we send 2-3 clips of the opening 60 s to choose from",
                 "a voice you hold the rights to (a consenting narrator)"],
     "default": "send 2-3 test clips of the opening", "blocks": "all narration audio, scene durations, subtitle timing"},
    {"id": "D2", "topic": "Fish Audio access", "status": "open (unchanged)",
     "question": "Provide FISH_API_KEY in the environment (never in a file) and confirm the validated drama-3 settings for English. "
                 "The first live test will also measure the real pace and the length of a [long pause].",
     "options": ["key now: first live test on one scene (00.1-00.4)", "later: build with the placeholder voice"],
     "default": "one-scene live test first", "blocks": "live narration"},
    {"id": "D3", "topic": "Which cut is the flagship", "status": "open (updated: B7, I6)",
     "question": "You asked for a long film that climbs to the supervisors' level. The core cut reaches L5 only briefly; the extended "
                 "cut does it properly. Which ships as the main video?",
     "options": ["extended cut as the flagship, core cut as a shorter edition from the same scenes",
                 "core cut as the flagship, extensions as a second release",
                 "two episodes (Part 1 ch00-ch07, Part 2 ch08-ch11 + extensions, with a 60-s recap)"],
     "default": "extended cut as the flagship, core cut as a shorter edition", "blocks": "script length, render budget, thumbnails"},
    {"id": "D4", "topic": "Provisional CPU runs", "status": "open (updated: H4, H5, A8, C12)",
     "question": "Launch the provisional CPU runs now, writing outside the site repository? Cheapest first: X-points on E2 samples "
                 "(minutes), Rice levels (minutes), palier1 2D sweep (~30 min), Taylor-Green 32^3 subset with stationarity flags "
                 "(~1-1.5 h, estimate), ABC at 48^3 near the three thresholds (hours, unmeasured: one point is timed first), E1 with "
                 "3 seeds (~3-4.5 h). The 3D decoder data of 10.6 need no run any more (built from random weights). Disk free: 8.7 GB.",
     "options": ["yes, on this machine", "yes, on the cloud VM", "no, ship empty seats"],
     "default": "yes, cheapest first", "blocks": "7 PROVISIONAL scenes"},
    {"id": "D5", "topic": "HPC timing and the release model", "status": "open (updated: H1)",
     "question": "When might the palier2 campaigns at 64^3, the GPU fm3d training and evaluation, and VKS (SFEMaNS/LATU) or DRESDYN "
                 "data be available? YouTube cannot replace a published file: when results arrive, publish a stand-alone 'Results "
                 "update' episode (5-8 min) and a v2 of the full film on the site and the GitHub release, or re-upload the film?",
     "options": ["ship now with empty seats; Results update episode + v2 later", "ship now; re-upload later (views and comments lost)",
                 "hold the release until tier-2 results"],
     "default": "ship now; Results update episode + v2 later", "blocks": "7 PENDING scenes, release plan"},
    {"id": "D6", "topic": "Supervisors on screen", "status": "open (unchanged)",
     "question": "Name the supervisors (as listed in the public offer: S. Cheng and D. Lucor, with C. Nore and Y. Ponty) in the "
                 "end-card credits, or only 'the project's supervisors' with names in the video description?",
     "options": ["names in text, no photos, no logos, no opinions attributed", "no names on screen"],
     "default": "names in text only (11.3)", "blocks": "03.7 lower-third wording, 11.3"},
    {"id": "D7", "topic": "Facts not on the site", "status": "open (updated: C4, B2)",
     "question": "May the film use sourced external facts: seafloor magnetic stripes, the self-exciting disc, and 'no one can yet "
                 "predict when Earth's field will flip' (logline)? The Curie-temperature argument is gone (replaced by the site's "
                 "own 'a free field fades in ~10^4 years' argument).",
     "options": ["yes, with on-screen reference chips and sources in the description", "no: open on VKS reversals instead"],
     "default": "yes, sourced", "blocks": "00.3, 01.3, logline and the opening narration"},
    {"id": "D8", "topic": "Formula density at L4-L5", "status": "open (unchanged)",
     "question": "Full statements of the propositions on a separate formula layer (never in subtitles, not narrated), or words only "
                 "with a pointer to the site?",
     "options": ["formula layer, narration stays intuitive", "words only + site pointer"],
     "default": "formula layer", "blocks": "07.5, 09.3, X2, X6"},
    {"id": "D9", "topic": "Look", "status": "open (unchanged)",
     "question": "Dark-dominant film (NIGHT about 75%, PAPER for derivations, BLUEPRINT for infrastructure) or light, closer to the "
                 "site? Key-coloured field maps (silver for negative values) or a conventional red-blue map in single-field shots?",
     "options": ["dark + key-coloured maps", "light + site look", "dark + red-blue maps"],
     "default": "dark + key-coloured maps", "blocks": "every scene template"},
    {"id": "D10", "topic": "Music and sound effects", "status": "open (updated: G2)",
     "question": "Music: none, an original bed synthesized in code under L0-L2, or a licensed track? Sound effects (needle, squeal, "
                 "crossing ticks, hiss) need a new SFX track in the pipeline (scene event lists mixed by build.js): keep them?",
     "options": ["original bed under L0-L2 + SFX", "SFX only", "none", "licensed music"],
     "default": "original bed under L0-L2, silence under L4-L5, SFX kept", "blocks": "audio mix, 00.5, 01.3, 04.2, 06.1"},
    {"id": "D11", "topic": "Frame rate, resolution, render machine", "status": "open (unchanged)",
     "question": "1080p30 master (render estimates in section 0), 60 fps for particle and 3D shots, or 4K (needs a bigger machine "
                 "and more than 8.7 GB of disk)? Render here or on a rented VM?",
     "options": ["1080p30 here", "1080p30, 60 fps for heavy shots", "4K on a cloud VM"],
     "default": "1080p30 here", "blocks": "final render"},
    {"id": "D12", "topic": "Pronunciations", "status": "open (updated)",
     "question": "Confirm: Gissinger (French or English), DRESDYN, SFEMaNS, MilaDy, Karman, Zeldovich, Kac.",
     "options": ["as in audio/lexicon.json", "your corrections"], "default": "lexicon entries marked CHECK", "blocks": "phoneme pins"},
    {"id": "D13", "topic": "Title", "status": "open (unchanged)",
     "question": "Pick a title: " + " / ".join(TITLE_OPTIONS) + ".",
     "options": TITLE_OPTIONS, "default": TITLE_OPTIONS[0], "blocks": "00.5, thumbnails"},
    {"id": "D14", "topic": "Disclaimer", "status": "open (updated: F4)",
     "question": "Approve the disclaimer wording and its new placements: a lower-third with one spoken sentence in 03.7 (the separate "
                 "20-s card is gone), the full text on the end card and in the description.",
     "options": ["as drafted", "edited", "keep a separate disclaimer card"], "default": "as drafted", "blocks": "03.7, 11.3"},
    {"id": "D15", "topic": "Short vertical version", "status": "open (ids updated)",
     "question": "Produce a 9:16 Short from the long version? Candidates: 07.5 (the spike) or 04.2-04.4 (whirlpools and 'when vs how often').",
     "options": ["yes, 07.5", "yes, 04.2-04.4", "no"], "default": "yes, 07.5", "blocks": "nothing in the long cut"},
    {"id": "D16", "topic": "Subtitle timing", "status": "open (unchanged)",
     "question": "Sentence-level subtitle timing (ready) or word-by-word emphasis (install a CPU aligner, about 0.5 GB)?",
     "options": ["sentence level", "word level"], "default": "sentence level", "blocks": "subtitle style only"},
    {"id": "D17", "topic": "How Bet 1 is settled", "status": "new (A2)",
     "question": "The configured 64^3 ABC campaign sweeps integer Rm only, so 'the sign at Rm = 17.5' cannot be settled as written. "
                 "State the bet as s(17) > 0 > s(18), or also add Rm = 17.25, 17.5 and 17.75 in a copy of the config (3 more runs)?",
     "options": ["both: restate the bet and add the 3 points", "restate the bet only", "add the 3 points only"],
     "default": "both", "blocks": "10.4 wording and its final run"},
    {"id": "D18", "topic": "Taylor-Green stationarity", "status": "new (A8)",
     "question": "The Taylor-Green runs keep t in [100, 140] from a 1e-3 seed; near the threshold the field may still be growing. "
                 "Flag and exclude non-saturated runs (no config change), or lengthen t_burn / t_keep for points near the threshold?",
     "options": ["flag and exclude", "lengthen the runs near the threshold", "both: flag now, rerun longer later"],
     "default": "flag and exclude now; decide on longer runs after the first 64^3 results", "blocks": "10.5, 10.7, X3.5"},
    {"id": "D19", "topic": "A site inconsistency", "status": "new (B15)",
     "question": "P3:1167 says the VKS threshold reads 'Rm_c ~ 44 (Miralles)', but P3:1202 converts Miralles' definition to about "
                 "1.05 x Nore's (so about 54-75). The film drops 44 (following R:141). Fix the site page separately? (This work does "
                 "not modify the site.)",
     "options": ["yes, fix P3 (FR and EN) in a separate task", "leave the site as is"],
     "default": "flag it for a separate site fix", "blocks": "nothing in the film"},
    {"id": "D20", "topic": "A needle that flips in the first 10 s", "status": "new (A1)",
     "question": "The new hook shows the compass needle swinging to south and back at about 7 s, with the chip 'illustration, not to "
                 "time scale'. Acceptable, or keep the needle still and let the stripes carry the surprise (hook at about 0:20)?",
     "options": ["needle flip with chip", "stripes carry the surprise"], "default": "needle flip with chip", "blocks": "00.1, opening narration"},
    {"id": "D21", "topic": "Narration pace", "status": "new (pedagogy F)",
     "question": "Script at about 125-130 effective words per minute (speech at about 150 plus visual breathing room) as the review "
                 "recommends, which is what the durations in this outline assume?",
     "options": ["yes, 125-130 effective wpm", "tighter, about 145 wpm (shorter film)"],
     "default": "125-130 effective wpm", "blocks": "script length per scene"},
]

NOTES = [
    "Predict beats need real silences: each paragraph of the script may carry hold_after (seconds, e.g. 3.0); build.js splits the TTS "
    "chunk at the aligned paragraph boundary, inserts silence and shifts the later cues. Test it on 01.3 first (G1).",
    "Sound effects: scenes export an event list (window.__EVENTS__: t, sample id, gain); build.js mixes the samples with adelay + amix "
    "under the same side-chain duck as the music; the squeal of 01.3 is timed in a narration gap (G2).",
    "E2 fields are 32^2: the extractor zero-pads them in Fourier space to 256^2 for display only, with the chip 'display interpolation "
    "(spectral)'; divergences are always measured on the native grid (G7).",
    "Isosurfaces and field lines of 3D fields (X1.2, 10.4 insets, 10.6) are precomputed offline in extract_data.py (spectral "
    "upsampling, marching cubes, field-line tracing) into compact .f32 meshes and polylines; scenes only draw them (G8).",
    "Benchmark one 6-s full-screen fragment shader on SwiftShader before committing to any shader-based background; 01.1 uses a "
    "Canvas 2D advected texture instead (G5).",
    "Regenerable scenes declare `requires` in the index; add a `make plan` check that refuses to render a result variant whose "
    "upstream is missing (H7). 11.1 and 11.2 depend on every regenerable data file, so they re-render whenever one changes (H2).",
    "Durations: duration_s is the scene as it ships now (pending variant for PENDING scenes, provisional data for PROVISIONAL "
    "scenes, assuming decision D4 = yes); duration_result_s is the length once the final data exist (H3).",
    "Keep the symbol sheet (section 2) in the script file and lint the script against it (D3).",
    "Prototype script proto/script/demo_script.json, scene d_e1_rate, says the generative model 'reproduces the whole curve': "
    "this overclaims (42% error near the threshold). Use the 09.1 wording instead.",
    "Prototype extractor palier1_eta_sweep() labels the E2 'recalage' series 'recalibrated'; 'recalage' is per-sample rescaling, "
    "the degenerate method of Corollary 6. Do not reuse that stand-in; 10.3 uses data/palier1_sweep.json from the real campaign, and "
    "draws the injection as the flat Ito line it is.",
    "The site's taxonomy figure uses blue for 'true for each sample'; redraw it (08.6) so blue keeps meaning velocity u.",
    "The 3D evaluation does not compute the per-sample spread of the budgets (C:166); add it before X3.5 can show a result.",
    "09.3 reads experiences/resultats/cache_e1/e1_echantillons_complet.npz, which is gitignored and present only on this machine: "
    "copy it into the film project's data before moving the build elsewhere.",
    "Every PENDING scene ships as an 'empty seat' with a READY anchor visual (part of the story), not as the hatched AWAITING "
    "preview, which is for drafts only. A PENDING scene whose data file appears is promoted to PROVISIONAL automatically and "
    "stamped PROVISIONAL DATA until a human marks it READY in the script.",
]

# --------------------------------------------------------------------------------------------
# CHANGES AFTER REVIEW
# outcome: applied | modified (applied differently, see note) | partly applied | rejected
# --------------------------------------------------------------------------------------------

def ch(review, item, where, outcome, note):
    return {"review": review, "item": item, "where": where, "outcome": outcome, "note": note}


ACC, PED = "accuracy", "pedagogy"

CHANGES = [
    # ---------------- accuracy review: HIGH ----------------
    ch(ACC, "A1", "X6.6", "applied", "Verified T:831-843: a symmetric prior gives the two humps; wording and visual inverted accordingly."),
    ch(ACC, "A2", "10.4, D17", "applied", "Verified CFG palier2_abc3d.yaml:36 (integer Rm). Bet restated as s(17) > 0 > s(18); extra points offered as D17."),
    ch(ACC, "A3", "10.3", "applied", "Verified milady/sim/run.py:256-273 (injection = np.full of the Ito rate) and R:442: flat eps_inj line, fluctuating dissipation."),
    ch(ACC, "A4", "04.6, synopsis, ch09 takeaway, logline", "applied", "Verified R:321 and R:514-528: 'no timestamp and no time order'; 'plus the equations'."),
    ch(ACC, "A5", "09.3, ch09 takeaway, closing", "applied", "Verified R:564 (E1 is intermediate) and R:883/R:901: steep ramp, not cliff; 'consistent with Prop. 9'; 'not bad luck' dropped."),
    ch(ACC, "A6", "08.7", "applied", "Verified R:300, R:1179, H:41: retitled 'The proposed machine', PROPOSED chip, tested pieces highlighted."),
    ch(ACC, "A7", "10.7", "applied", "Verified T:912, T:917, CFG palier2_tg3d.yaml, train_fm3d.yaml (val Re 100 Pm 1; test Re 50 Pm 2)."),
    ch(ACC, "A8", "10.5, 10.7, X3.5, D18", "applied", "Verified CFG palier2_tg3d.yaml:9-10, 41-43 and the growth_rate term of train_fm3d.yaml. "
       "Evidence corrected: T:992 is about the loss's variance, not data stationarity; the concern stands on the config alone."),
    ch(ACC, "A9", "X3.5", "applied", "Verified T:903 vs T:917: criterion relabelled 'adapted from tier 1; the plan sets none for 3D'."),
    ch(ACC, "A10", "07.5, 08.5", "applied", "Verified R:1035 and R:961/R:993: 'worse where it counts'; the E2 nuance lands in 08.5 lane 3."),
    # ---------------- accuracy review: MEDIUM ----------------
    ch(ACC, "B1", "03.7", "applied", "Verified H:72, S:72: project context and 'this study asks' are separate lower-thirds."),
    ch(ACC, "B2", "opening, closing, logline, D7", "applied", "Verified P4:1627, R:743: 'in the dynamos we can compute'; 'between the settings that were simulated'."),
    ch(ACC, "B3", "synopsis, 02.4", "applied", "Verified R:139, R:149, P3:1149: only VKS reversed; each tank's field described."),
    ch(ACC, "B4", "01.2", "applied", "Lines never start or stop; they need not close."),
    ch(ACC, "B5", "02.1", "applied", "Verified P3:281, R:137: same flow, two diffusivities; honey removed."),
    ch(ACC, "B6", "04.5", "applied", "Verified R:871, R:901: Gamma = 0.93 on screen, 'below, each start paints one whirlpool'."),
    ch(ACC, "B7", "X1.2, 03.4", "applied", "Verified R:1077, R:1092 (s < 0 at Rm 8 and 20), e3_modes.npz keys Rm8/12/16/20, R:1120."),
    ch(ACC, "B8", "X1.1", "applied", "Verified R:1116: the exact mode gives a lower bound on the dominant rate."),
    ch(ACC, "B9", "X1.3", "applied", "Verified R:1114."),
    ch(ACC, "B10", "08.5, X3.2", "applied", "Verified R:1033: one effective sample in 500."),
    ch(ACC, "B11", "07.3", "applied", "Verified e1_gissinger.json (B test asymmetry 0.0071-0.0246, mean 0.0157) and R:839, R:873."),
    ch(ACC, "B12", "04.4", "applied", "Verified P4:1627 and the digest (0.00442 at Gamma 0.9): ~11 vs ~230."),
    ch(ACC, "B13", "10.1, X5.6", "applied", "Verified T:46-56: source wording used."),
    ch(ACC, "B14", "X5.1", "applied", "Verified C:176: state 0.4 GB, peak ~15x, estimates."),
    ch(ACC, "B15", "03.5, X6.0 (was X1.4), D19", "applied", "Verified P3:1167 vs P3:1194/1202 and R:141, R:143: 44 dropped, simulation chip added; "
       "the inconsistency is in the site itself (P3:1167), raised as D19."),
    ch(ACC, "B16", "04.3, 09.1, closing", "applied", "Verified R:528, R:883: crossings defined once, 'model C, seed 0'."),
    ch(ACC, "B17", "09.2, 09.3", "applied", "Verified R:883 and the digest fine grid: leak / lag / overshoot."),
    # ---------------- accuracy review: LOW ----------------
    ch(ACC, "C1", "03.1", "applied", "Verified P3:254: 'carried and stretched by the flow'."),
    ch(ACC, "C2", "03.2", "applied", "Cowling chip removed with the anti-dynamo chip (E6); growth rate renamed s, 'modes may also oscillate' (R:1114)."),
    ch(ACC, "C3", "04.2", "applied", "Verified R:159, R:784: crisis shown in mu, expected in Gamma."),
    ch(ACC, "C4", "01.1", "applied", "Verified P3:269, P3:1471: one EXTERNAL_FACT flag removed."),
    ch(ACC, "C5", "00.3", "applied", "Verified P3:1230."),
    ch(ACC, "C6", "02.6", "applied", "Verified R:163: numbers on a separate card."),
    ch(ACC, "C7", "07.4", "applied", "Verified R:873, R:875."),
    ch(ACC, "C8", "05.3", "applied", "Verified R:883."),
    ch(ACC, "C9", "06.3", "applied", "Trajectories drawn with t on the horizontal axis."),
    ch(ACC, "C10", "10.2, X5.2, X2.4", "applied", "Verified C:93 and R:401."),
    ch(ACC, "C11", "10.8, X6.2, X5.5", "applied", "Verified T:259-266 and T:974."),
    ch(ACC, "C12", "X4.5, 03.6", "applied", "X:71 is for two seeds; three seeds estimated at 3-4.5 h. Terabytes chip added."),
    ch(ACC, "C13", "04.6, 05.2", "partly applied", "Key fixed to ref|0.9. Correction to the review: ref|0.9 holds 8,000 points (not 4,000), "
       "about 21 in |D| < 0.2, and the cache has no 20,000-sample reference set; the dense strip comes from a re-integrated trajectory instead."),
    # ---------------- pedagogy review ----------------
    ch(PED, "A1", "00.1-00.4, opening", "applied", "Needle flips at ~7 s; questions at ~0:34 (C0.3 and C0.4 merged into 00.3)."),
    ch(PED, "A2", "00.2, 00.4, opening, 11.2", "applied", "Budgets re-cut to match the cue map (7 s and 30 s); the closing scene gets 70 s for its 155 words."),
    ch(PED, "A3", "00.2", "applied", "Narration describes the visual."),
    ch(PED, "A4", "00.3", "applied", "'every few hundred thousand years, irregularly'."),
    ch(PED, "A5", "00.3", "applied", "True barcode: solid vermillion vs near-background."),
    ch(PED, "A6", "00.4, 03.7", "applied", "Violet-cloud teaser and promise-card cloud."),
    ch(PED, "B1", "08.1 (new)", "applied", "E2 introduced before its first predict beat."),
    ch(PED, "B2", "ch02, ch03", "applied", "Reordered: race and Rm, then sodium and VKS (L1), then the equation and windows (L2); 02.3 lowered to L1."),
    ch(PED, "B3", "08.4, X2.2", "applied", "Intuitive spring at L3; the formula lives only in X2.2."),
    ch(PED, "B4", "07.4, X2.5", "applied", "No L-phi or degrees in the core."),
    ch(PED, "B5", "04.5", "applied", "'long-exposure glow (stationary distribution)'."),
    ch(PED, "B6", "06.5, 07.5", "applied", "Earth-mover beat names W1; Lip(phi); KL only on the formula layer."),
    ch(PED, "B7", "10.8 (new), D3", "modified", "Merged X6.1 + X6.2 into the core as 10.8 (READY, L5) instead of moving X4.3, which would have "
       "broken the climbing ladder; the flagship question goes to D3 with the extended cut recommended."),
    ch(PED, "B8", "01.3", "applied", "Staircase of bars 'B x (gain / loss)' -> e^(s t)."),
    ch(PED, "C1", "07.1, 08.6", "applied", "Shelves empty at the start of ch07, filled by predict beats, formal row only at the end of ch08."),
    ch(PED, "C2", "07.2", "applied", "'built into the machine, acts on the crowd'; mirror on the crowd shelf, tag 'built in, exactly'."),
    ch(PED, "C3", "03.3", "applied", "Motivating line for the ABC flow."),
    ch(PED, "C4", "03.8, 04.1", "applied", "Bridge sentence into the three-dial model."),
    ch(PED, "C5", "01.2", "applied", "Cut-magnet surprise first."),
    ch(PED, "C6", "06.2", "applied", "'Two clocks' moved before the formulas."),
    ch(PED, "C7", "05.3, 09.1", "applied", "Cumulative error defined once as a shaded area."),
    ch(PED, "D1", "all", "applied", "Growth rate s; lambda only for the knob (symbol sheet)."),
    ch(PED, "D2", "all", "applied", "'distribution distance' everywhere; technical name on a chip in 06.5 and in X3.0."),
    ch(PED, "D3", "04.1, 05.2, X3.1, X4.2, 03.5", "applied", "Numbers for Gissinger coefficients, r_0 / r / r_a, q*, 'iron'."),
    ch(PED, "D4", "04.7, 08.5, X3.5", "applied", "eps for dissipation."),
    ch(PED, "D5", "04.3 onward", "applied", "'crossing rate' after one definition."),
    ch(PED, "D6", "all ids", "applied", "Chapters ch00-ch11, scenes NN.k; every scene keeps its version-1 id in 'was'."),
    ch(PED, "E1", "03.3, 03.7, 04.1, 08.1, 10.1", "applied", "Staircase planted in 03.7, lit tier by tier, paid off in 10.1."),
    ch(PED, "E2", "09.3", "modified", "Renamed 'A stiff sheet on a steep ramp': 'cliff' was rejected by accuracy A5, 'staircase' collided with M7."),
    ch(PED, "E3", "06.4, 09.1", "applied", "Shoebox filled by generated photos; toll counter returns with violet cars."),
    ch(PED, "E4", "10.6, X6.1", "applied", "Projector reused."),
    ch(PED, "E5", "03.1, 05.2, 06.3, 07.6, 09.3", "applied", "Pen beats scheduled."),
    ch(PED, "E6", "03.2, 08.1", "applied", "Anti-dynamo chip removed from 03.2; narrated payoff in 08.1."),
    ch(PED, "E7", "conventions, 00.1", "applied", "Needle only when D is on screen; rail on the left, at chapter cards and checkpoints only."),
    ch(PED, "E8", "01.6, 03.8, 05.5, 08.7", "applied", "Checkpoints end on an open question."),
    ch(PED, "E9", "08.7, 09.6", "applied", "Recaps merged; framework panels a, b, d only."),
    ch(PED, "F (table)", "durations", "applied", "Overrun scenes re-budgeted or trimmed (00.4, 01.3, 03.2, 03.5, 05.4, 06.5, 08.2, 07.2-07.3, 07.5, 08.5, 09.6, 10.3)."),
    ch(PED, "F1", "ch07, ch08", "applied", "C7 split: ch07 'The mirror and the crowd' (E1), ch08 'Fields have stricter laws' (E2). ch08 opens with a "
       "declared side-step L4 -> L3 on the rail (new test bench)."),
    ch(PED, "F2", "03.2", "applied", "One idea; 'the field pushes back on the flow'."),
    ch(PED, "F3", "03.4, X1.3", "applied", "Rounded thresholds; 48^3 markers moved."),
    ch(PED, "F4", "03.7, 11.3", "applied", "Disclaimer folded into a lower-third with one spoken sentence; full text on the end card."),
    ch(PED, "F5", "02.6, 04.3", "applied", "Plain-language rates; exact values on the formula layer."),
    ch(PED, "F6", "03.7, 05.3, 08.6, 09.1", "applied", "Three promise cards ticked off on screen."),
    ch(PED, "F7", "10.3, X5.3", "modified", "Kept as a separate 15-s PROVISIONAL scene instead of a beat inside 10.2, so 10.2 stays READY and "
       "the regenerable part stays isolated; the full sweep moved to X5.3."),
    ch(PED, "F8", "09.6", "applied", "Scoreboard and lessons merged (40 s)."),
    ch(PED, "G1", "production notes", "applied", "hold_after per paragraph."),
    ch(PED, "G2", "production notes, D10", "applied", "SFX event track; squeal in a narration gap."),
    ch(PED, "G3", "00.1, 11.2", "applied", "Stylized compass, no hand."),
    ch(PED, "G4", "00.2", "applied", "Layered 2D zoom; WebGL only for the last 3 s."),
    ch(PED, "G5", "01.1, production notes", "applied", "Canvas 2D churn; shader benchmark before any shader background."),
    ch(PED, "G6", "11.2", "applied", "Sequenced montage, one motif per sentence."),
    ch(PED, "G7", "08.1, 08.2, production notes", "applied", "Spectral zero-padding for display only."),
    ch(PED, "G8", "X1.2, 10.4, production notes", "applied", "Meshes and polylines precomputed offline."),
    ch(PED, "G9", "10.5", "applied", "Render class flat; 3D insert as a separate shot."),
    ch(PED, "H1", "results-update cut, D5", "applied", "Stand-alone 'Results update' episode plus v2 of the film."),
    ch(PED, "H2", "11.1, 11.2, closing", "applied", "Closing paragraph 3 has two variants; both scenes depend on every regenerable file."),
    ch(PED, "H3", "10.4-10.9, X3.5, X4.4, X5.5, X6.4, X6.5", "applied", "READY anchor in every seat; two durations per regenerable scene."),
    ch(PED, "H4", "10.6, 10.7", "applied", "10.6 'What is guaranteed' is READY (random-weight decoder, no run); 10.7 'What must be measured'."),
    ch(PED, "H5", "10.4", "applied", "Provisional run at 48^3 near the thresholds, not 32^3."),
    ch(PED, "H6", "10.2", "applied", "One sentence explains stamps."),
    ch(PED, "H7", "regenerable index", "applied", "`requires` column added."),
    ch(PED, "H8", "10.9", "applied", "Extended-cut entry 10.9-bridge (15 s)."),
    ch(PED, "I1", "X1, X6.0", "modified", "X1 anchored before 10.4 as the provenance of Bet 1; X1.4 kept but moved to X6 as X6.0 (the three Rm "
       "definitions left 03.5), with 44 dropped (B15)."),
    ch(PED, "I2", "X3b", "applied", "X3.5 after 10.7."),
    ch(PED, "I3", "X4a, X4b", "modified", "X4.4 after 10.5 as asked; X4.5 stays with X4.1-X4.3 after ch09 because the staircase is now planted in "
       "03.7 (the review's own alternative)."),
    ch(PED, "I4", "X5a, X5b", "applied", "X5.1-X5.4 after 10.3; X5.5-X5.6 after X6 as the L5 finale; X5.1 raised to L4."),
    ch(PED, "I5", "X2.2", "applied", "Resolved by B3."),
    ch(PED, "I6", "two-episode option", "applied", "ch07 closes Part 1; Part 2 opens on a 60-s recap."),
    ch(PED, "J", "02.1, 01.4, 11.2, 03.7, predict ids, 01.3", "applied", "Ink metaphor; words for forces and heat; closing numbers on chips; "
       "lower-third not narrated; predict beats renumbered Q1-Q8 in film order; bicycle-dynamo anchor."),
    ch(PED, "speech rate", "conventions, D21", "applied", "Durations assume 125-130 effective words per minute."),
]
