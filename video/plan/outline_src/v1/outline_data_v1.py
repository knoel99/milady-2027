# -*- coding: utf-8 -*-
"""Structured source of the MilaDy explainer outline.

build_outline.py turns this into outline.json (machine-readable) and outline.md (human-readable).
Paths in `assets` and `data` are relative to the site repository /home/user/milady-2027 unless they
start with "proto/" (the render prototype under video_plan/proto). Scene data files written by the
extractor ("data/...json") live under the film project root (today: video_plan/proto/data/).
"""

R, P, N = "READY", "PROVISIONAL", "PENDING"


def sc(id, title, level, dur, key, visual, on_screen, assets=(), data=(), status=R, regen=None,
       register="NIGHT", motifs=(), render="flat", flags=(), sources=(), predict=None):
    return {
        "id": id, "title": title, "level": level, "duration_s": dur, "key_idea": key,
        "visual": visual, "on_screen": on_screen, "assets": list(assets), "data": list(data),
        "status": status, "regen": regen, "register": register, "motifs": list(motifs),
        "render_class": render, "flags": list(flags), "sources": list(sources), "predict": predict,
    }


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

# --------------------------------------------------------------------------------------------
# CORE CUT
# --------------------------------------------------------------------------------------------

C0 = {
    "id": "C0", "cut": "core", "title": "Cold open: the needle and the stripes", "levels": "L0",
    "learning_goal": "Feel that Earth's field is not permanent: it has flipped many times, irregularly.",
    "takeaway": "The field has flipped many times, with no schedule; we can ask when, and we can ask how often.",
    "scenes": [
        sc("C0.1", "A needle that settles", "L0", 12,
           "A compass points north and seems permanent.",
           "Macro shot of a compass in a grey hand; the vermillion needle tip swings and settles with a "
           "3% overshoot; slow 1.00 to 1.02 push. The polarity needle (M1) is born here; at the end of the "
           "chapter it shrinks into the top-right corner and stays for the whole film.",
           "none", render="webgl", motifs=["M1 polarity needle"]),
        sc("C0.2", "Pull back to the planet", "L0", 8,
           "The compass follows a field that wraps the whole planet.",
           "T2 scale dive from the hand to a landscape to Earth seen from space (plain grey sphere, no photo "
           "texture); vermillion dipole field lines bloom from pole to pole.",
           "chip SCHEMATIC", render="webgl", motifs=["T2 scale dive"]),
        sc("C0.3", "The seafloor tape recorder", "L0", 20,
           "Cooling lava freezes the field's direction; spreading seafloor records it as stripes.",
           "Cross-section of a mid-ocean ridge: magma rises and cools, short vermillion grain segments align "
           "with the field and freeze, the floor slides away on two conveyor belts. Stripes accumulate "
           "mirror-symmetrically: solid vermillion = normal polarity, pale vermillion = reversed.",
           "labels 'normal' / 'reversed'; chip SCHEMATIC; reference chip (to be sourced)",
           flags=["EXTERNAL_FACT: seafloor magnetic stripes (Vine and Matthews 1963), source before use"],
           motifs=["M1 barcode / polarity strip"]),
        sc("C0.4", "Not on a schedule", "L0", 8,
           "The stripes have irregular widths: the flips are irregular.",
           "Camera tilts to look down on the barcode; stripe widths visibly irregular; the barcode slides "
           "left and becomes the polarity strip under a thin D(t) trace (T1 morph).",
           "'irregular: every 10^5 to 10^6 years'", sources=["en/prep/p3 ch. 7 (Rincon 2019)"],
           motifs=["barcode", "T1 morph"]),
        sc("C0.5", "Two questions", "L0", 12,
           "When will it flip next? How often does it flip? The first is hopeless, the second is not.",
           "Two cards: 'When will it flip next?' with a grey clock, 'How often does it flip?' with amber "
           "tally marks. The clock card's border turns dashed and dims; the tally card stays lit. The "
           "altitude rail (M8) fades in on the right edge at L0.",
           "the two questions", motifs=["M8 altitude rail"],
           sources=["en/prep/p4 §7.3 (when vs how often)"]),
        sc("C0.6", "Title", "L0", 10,
           "Title card.",
           "Title words sit in a vermillion field-line field; the dipole flips and the lines reorganise "
           "around the letters; one soft impact sound.",
           "working title (decision D13)", motifs=["M1 flip"]),
    ],
}

C1 = {
    "id": "C1", "cut": "core", "title": "A planet that makes its own magnet", "levels": "L0-L1",
    "learning_goal": "Understand that the field must be regenerated by moving liquid metal, that a dynamo is a "
                     "self-amplifying loop with a threshold, and that physics prefers neither polarity.",
    "takeaway": "A moving conducting fluid can turn a tiny field into a large one once its loop gain passes a "
                "threshold, and the laws do not prefer north or south.",
    "scenes": [
        sc("C1.1", "No magnet inside", "L0", 25,
           "The core is liquid iron and too hot to stay magnetized: the field must be continuously regenerated.",
           "Earth cutaway in grey shells (solid inner core, liquid outer core); a bar magnet glyph is heated "
           "and its arrows scatter; the outer core starts to churn (grey matter, no colour until fields appear).",
           "'liquid iron outer core'; 'too hot to stay magnetized'",
           flags=["EXTERNAL_FACT: Curie temperature of iron vs core temperature, source before use"],
           render="webgl", sources=["R:86 (dynamo effect)"]),
        sc("C1.2", "Lines never end", "L0", 30,
           "Magnetic field lines close on themselves: through any imaginary box, as many enter as leave.",
           "Iron filings around a bar magnet morph into vermillion field lines; a dashed box is dragged "
           "around the picture; two counters 'in' and 'out' always agree. Planted for div B = 0 (C7).",
           "'lines in = lines out' (no symbol yet)",
           assets=["prep/p1-calcul-vectoriel/fig-monopole-dipole-en.png"], render="dense2d",
           motifs=["the box (callback in C7.3)"]),
        sc("C1.3", "The squeal", "L1", 45,
           "A loop with gain above one grows exponentially from almost nothing, then saturates.",
           "Microphone pointed at its own speaker: whisper, then squeal past a green gain knob (M2). Morph into "
           "a self-exciting disc: grey copper disc, coil, current arrows; below the threshold the seed dies, "
           "above it the field grows exponentially, then the plateau (the field brakes the disc).",
           "Predict Q2 with 3-s countdown; after the reveal: dB/dt = (gain - loss) B, so B grows like e^(lambda t)",
           predict="Q2: spin a little faster each time: does the field grow a little each time, or nothing until "
                   "a certain speed? (Answer: nothing, then exponential growth, then saturation.)",
           flags=["EXTERNAL_FACT: self-exciting homopolar disc (Bullard 1955), source before use"],
           motifs=["M2 knob (first appearance)", "squeal / loop gain"]),
        sc("C1.4", "Who pays the bill", "L1", 20,
           "A dynamo converts mechanical power into magnetic energy and heat; it creates no energy.",
           "Loop diagram: motor power -> flow (blue) -> field (vermillion) by induction -> Lorentz force brakes "
           "the flow -> heat (viscous and Joule losses, grey).",
           "loop labels",
           assets=["en/prep/p3-mhd-dynamo/index.qmd"],
           sources=["en/prep/p3 ch. 5 loop diagram (inline SVG, redraw in palette)"]),
        sc("C1.5", "Which way is up?", "L1", 25,
           "The equations are unchanged under B -> -B: both polarities are equally lawful; which one you get is history.",
           "Predict card; then a vertical mirror plane (M10) appears; the Earth's field and its mirror twin side "
           "by side; the corner needle flips.",
           "Predict Q1; then 'B -> -B: same equations'",
           predict="Q1: physics does not care whether the field points north or south. Which polarity should "
                   "Earth prefer? (Answer: neither.)",
           motifs=["M10 mirror (first appearance)"]),
        sc("C1.6", "Checkpoint: the big picture", "L1", 12,
           "Exit ramp for viewers who only wanted the big picture.",
           "Recap with motifs only (needle, barcode, squeal); the altitude rail climbs one notch, brightening to 80% for 2 s.",
           "'Level 0 -> Level 1'", motifs=["M8 rail"]),
    ],
}

C2 = {
    "id": "C2", "cut": "core", "title": "Stretch versus smudge", "levels": "L1-L2",
    "learning_goal": "Read the induction equation as a race between stretching and diffusion; know Rm, thresholds, "
                     "kinematic vs dynamic, and the ABC dynamo windows.",
    "takeaway": "A flow amplifies a field when stretching beats diffusion, and the dynamo can switch on, off, and on again.",
    "scenes": [
        sc("C2.1", "Frozen threads", "L1", 35,
           "A conducting flow drags field lines; stretching a line strengthens the field; diffusion smudges it.",
           "Blue tracer particles stretch and fold a vermillion material line (brightness follows stretch). "
           "Split screen: honey (threads stay sharp) vs water (a grey blur wins).",
           "'stretching' / 'diffusion'",
           assets=["prep/p3-mhd-dynamo/figures/expulsion-en.svg", "proto/scenes/a_fieldlines.html"],
           data=["proto/data/fieldlines.json"], render="dense2d", motifs=["M3 two inks"]),
        sc("C2.2", "One number for the race", "L1", 30,
           "Rm = UL/eta compares stretching with smudging; the growth rate crosses zero at a threshold.",
           "Green Rm knob turns; a schematic growth-rate curve lambda(Rm) rises through zero; the zero crossing "
           "is marked as the threshold Rm_c.",
           "Rm = U L / eta (U blue, eta green); chip SCHEMATIC",
           sources=["en/prep/p3 ch. 2"], motifs=["M2 knob"]),
        sc("C2.3", "The induction equation, term by term", "L2", 40,
           "The whole race in one equation.",
           "Equation built with the 10-step protocol: terms light in narrative order, leader lines to a "
           "stretched thread (advection term) and a fading thread (diffusion term).",
           "dB/dt = curl(u x B) + eta Laplacian(B), braces 'stretching by the flow', 'diffusion'",
           assets=["proto/scenes/b_induction.html"]),
        sc("C2.4", "A conveyor belt that does not feel its cargo", "L2", 30,
           "Kinematic dynamo: imposed flow, exponential growth (an eigenvalue problem). Dynamic: the field brakes the flow and saturates.",
           "Log plot of ||B||(t): a straight line of slope lambda (kinematic), then the same curve bending into "
           "a plateau when the Lorentz force j x B acts (dynamic). Side chip plants the anti-dynamo theorems.",
           "'kinematic: B = e^(lambda t) B_hat'; chip 'anti-dynamo: no planar dynamo (Zeldovich), no axisymmetric field (Cowling)'",
           sources=["R:240", "en/prep/p3 §5.2"], motifs=["anti-dynamo planted (paid off in C7.2)"]),
        sc("C2.5", "Twisting rooms: the ABC flow", "L2", 25,
           "A simple periodic flow whose streamlines are corkscrews (velocity parallel to its curl).",
           "A periodic box of fat blue corkscrew streamlines (Three.js Line2), slow orbit, long lens.",
           "u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x);  curl u = u",
           assets=["proto/scenes/c_abc3d.html"], render="webgl", sources=["R:1063"]),
        sc("C2.6", "Predict: once on, always on?", "L2", 45,
           "Dynamo windows: the ABC dynamo switches on near Rm 8.9, off near 17.6, on again above about 27.",
           "Predict card; then lambda(Rm) drawn live, left to right, from E3: 24 points, 48^3 checks as open "
           "markers, windows shaded green at 12%; inset z = 0 slices of |B| of the dominant mode at Rm 8, 12, 16, 20.",
           "thresholds 8.87 / 17.6 / 26.8 (32^3) vs published 8.9 / 17.5 / about 27; source chip DATA · E3",
           assets=["experiences/figures/e3_abc-en.svg", "assets/interactif/abc-dynamo.js"],
           data=["experiences/resultats/e3_abc.json", "assets/interactif/data/abc-dynamo.json"],
           predict="Q3: lowering diffusion only helps stretching; once the dynamo turns on, it stays on. Right? "
                   "(Answer: no, windows.)",
           flags=["CAVEAT: kinematic test bench, no generative model in E3"], sources=["R:1070-1112", "D:170-198"]),
    ],
}

C3 = {
    "id": "C3", "cut": "core", "title": "Dynamos you can build, and why they are rare", "levels": "L1-L2",
    "learning_goal": "Know why lab dynamos are hard (sodium, turbulence), what VKS showed (iron impellers, reversals), "
                     "that the knob is a panel of knobs, and that simulations are too costly to cover it.",
    "takeaway": "Real dynamos depend on many knobs, flip irregularly and cost too much to simulate at every setting: "
                "we need something that fills the gaps.",
    "scenes": [
        sc("C3.1", "The sodium problem", "L2", 30,
           "With Pm = nu/eta about 1e-5, reaching Rm of 10 to 50 forces Re to 1e6-1e7: any lab dynamo is violently turbulent.",
           "Two gauges: Rm (green) climbs slowly, Re (blue) races; a turbulent texture fills the background.",
           "Pm = nu / eta ~ 1e-5;  Rm ~ 10-50 needs Re ~ 1e6-1e7",
           sources=["en/prep/p3 ch. 6 (line 1145)", "en/prep/p3 Ex. 1.6"]),
        sc("C3.2", "Three tanks that worked", "L1", 30,
           "Only three liquid-sodium experiments have produced a dynamo; DRESDYN is trying with precession.",
           "Horizontal timeline cards (one moment per card): Riga (helical flow), Karlsruhe (52 helical cells), "
           "Cadarache VKS (150 litres of sodium, motors up to 300 kW); a fourth card, dashed: DRESDYN, under way.",
           "names and one plain line each; dates only after checking p3 ch. 6",
           assets=["prep/p3-mhd-dynamo/figures/vks-en.svg"], sources=["R:86", "en/prep/p3 ch. 6"]),
        sc("C3.3", "VKS: two impellers and an iron surprise", "L1", 35,
           "Counter-rotating impellers stir liquid sodium; the dynamo appeared only with soft-iron impellers.",
           "3D cutaway of the cylinder (grey matter), two bladed impellers counter-rotating, blue flow cells "
           "and recirculation; the impeller material is swapped steel -> soft iron: only then does a vermillion "
           "axial dipole grow.",
           "chip SCHEMATIC geometry; 'stainless steel: no dynamo' / 'soft iron: dynamo'",
           assets=["figures/vks/figure/out/vks-en.svg", "prep/p3-mhd-dynamo/figures/vks-en.svg"],
           render="webgl", sources=["R:90", "T:138"], motifs=["matter grey, fields coloured"]),
        sc("C3.4", "VKS flips too", "L1", 25,
           "With impellers at different speeds, the lab dynamo reverses irregularly, like the Earth.",
           "D(t) with reversals (qualitative curve from the VKS figure, panel b) with the barcode strip under it; "
           "corner needle flips in sync.",
           "'16 Hz vs 22 Hz: polarities last 120 s and 50 s on average; a reversal takes about 5 s (ohmic time about 0.4 s)'; chip 'qualitative curve'",
           assets=["figures/vks/figure/out/vks-en.svg"], sources=["en/prep/p3 line 1166 (Berhanu et al. 2007)"],
           motifs=["barcode", "M1 flip"]),
        sc("C3.5", "A panel of knobs", "L2", 30,
           "The control parameter is a vector: Re, Rm, materials, boundary conditions, forcing asymmetry, precession.",
           "The single green knob splits into a panel (Re, Rm, mu_r, asymmetry, Po). One boundary-condition "
           "switch moves the threshold marker from 90 to 130. Then the same VKS impeller wears three labels.",
           "'Rm_c = 90 +/- 5 (pseudo-vacuum) -> 130 +/- 10 (vacuum)'; 'same threshold: Rm_c = 31, 44 or 52-71, three definitions'",
           sources=["R:90", "en/prep/p3 line 1167", "en/prep/p3 line 722"], motifs=["M2 knob panel"]),
        sc("C3.6", "A handful of dots", "L2", 25,
           "Each 3D turbulent simulation is expensive, so only a few knob settings exist, each a huge dataset.",
           "A green parameter axis with a few filled dots; each dot grows a tall grey stack of data files; the "
           "gaps between dots stay empty.",
           "'each simulation: a few settings, terabytes'",
           sources=["H:64", "T:62", "T:927-939 (VKS sizes)"]),
        sc("C3.7", "The question of this film", "L2", 40,
           "Can a machine learn the family of possible fields for any knob setting, respect physics exactly where it is exact "
           "and statistically where it is statistical, and tell us how often the field flips?",
           "The question typeset word by word in the colour key (knobs green, fields blue and vermillion, "
           "'exactly' as a single card, 'statistically' as an amber stack, 'how often' amber). Three promise chips. "
           "Project lower-third.",
           "central question; promises 1-3; lower-third 'MilaDy · ANR-25-CE51-0077 · since January 2026 · 48 months · LISN, Lagrange (OCA), CEREA (ENPC)'",
           sources=["S:57-62", "H:72"]),
        sc("C3.8", "Who is telling you this", "L2", 20,
           "Honesty frame: an independent, prospective study with small CPU experiments, not endorsed by the project.",
           "T3 ink change to PAPER; a single page card with the disclaimer, typed on.",
           "'An independent, prospective study prepared for an internship application. Small CPU experiments. "
           "Not produced or endorsed by the MilaDy project, its partners or the supervisors. No MilaDy simulation data were used.'",
           register="PAPER", sources=["H:43-46", "R:51", "T:55-58"], flags=["DISCLAIMER (decision D14)"]),
        sc("C3.9", "Checkpoint: Level 1 done", "L2", 12,
           "Exit ramp; the climb steepens.",
           "Motif recap (threads, knob panel, barcode); rail climbs to L2.",
           "'Level 1 -> Level 2'", motifs=["M8 rail"]),
    ],
}

C4 = {
    "id": "C4", "cut": "core", "title": "Chaos and the shoebox of photographs", "levels": "L2",
    "learning_goal": "See reversals in a three-mode model, understand why 'when' is unpredictable, and why the "
                     "stationary distribution (a shuffled box of snapshots) is the stable object; meet crowd laws.",
    "takeaway": "The date of the next flip is unknowable, but the cloud of states is stable, and some laws hold only for the cloud.",
    "scenes": [
        sc("C4.1", "Three dials", "L2", 30,
           "Three coupled modes (quadrupole Q, dipole D, velocity V) with the B -> -B symmetry already reverse.",
           "Three dials (D vermillion, Q light vermillion, V blue) linked by springs; then the equations appear "
           "term by term in the same colours.",
           "Qdot = mu Q - V D;  Ddot = -nu D + V Q;  Vdot = Gamma - V + Q D;  (Q, D, V) -> (-Q, -D, V);  mu = 0.119, nu = 0.1; chip 'phenomenological model (Gissinger 2012)'",
           assets=["assets/interactif/gissinger.js"], sources=["R:434", "R:784"]),
        sc("C4.2", "Two whirlpools and a corridor", "L2", 45,
           "Below Gamma about 0.86 each trajectory is trapped in one of two mirror whirlpools; above, a corridor opens and it flips.",
           "Live RK4 integration in Canvas: (Q, D) phase portrait with a fading trail; green Gamma knob turned "
           "from 0.80 to 1.00; the two mirror whirlpools touch; a two-note sound at each crossing; scrolling "
           "magnetogram strip D(t) with its barcode underneath.",
           "Gamma knob value; 'merging crisis'",
           assets=["assets/interactif/gissinger.js", "prep/p4-systemes-dynamiques/figures/gissinger-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#config"], render="dense2d",
           motifs=["two whirlpools and the corridor", "M1 flip sound", "M2 knob"], sources=["P4:1513-1541"]),
        sc("C4.3", "Listen to the rate", "L2", 25,
           "The flip rate switches on at a threshold between Gamma = 0.86 and 0.865 and grows with Gamma.",
           "Ticks per zero crossing; the simulated crossing rate vs Gamma builds point by point (41 values); "
           "training values as filled dots.",
           "'0 up to 0.86 · 0.00194 per unit time at 0.865 · about 0.011 at 1.00'",
           assets=["proto/scenes/d_curve.html"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine.taux_simulation", "proto/data/e1_rate.json"],
           sources=["R:871", "D:93-121"]),
        sc("C4.4", "Predict: when is the next flip?", "L2", 40,
           "Errors grow by e every ~11 time units while a polarity lasts more than 100: 'when' is out of reach.",
           "Predict card; two trajectories started 1e-6 apart, drawn in two shades; their separation on a log "
           "axis climbs with slope ~0.09; a ruler compares 11 units with the >100-unit polarity length.",
           "'Lyapunov time ~11 · mean polarity > 100'",
           predict="Q4: we know the state to six decimals. Can we predict the date of the next reversal? (Answer: no.)",
           render="dense2d", sources=["P4:1627", "P4:1778"]),
        sc("C4.5", "The long exposure", "L2", 30,
           "Different trajectories paint the same glow: the stationary (invariant) distribution is reproducible.",
           "Two trajectories from different starts leave long-exposure glows that converge to the same shape; "
           "an amber histogram of D (bimodal) builds below and becomes identical for both.",
           "'invariant measure mu_Gamma'", render="dense2d", motifs=["M5 amber histogram (first)"],
           sources=["P4:928"]),
        sc("C4.6", "The shoebox", "L2", 35,
           "Cut the film into frames, shuffle, drop the timestamps: a sample of the stationary distribution. A snapshot does not know its own future.",
           "A film strip of the trajectory is cut into frames that fall, shuffled, into a shoebox; their time "
           "labels flutter away; the box's contents redraw the same cloud.",
           "'a snapshot does not know its own future'",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.90"], motifs=["shoebox (first)"],
           sources=["R:321", "R:320-322"]),
        sc("C4.7", "Crowd laws", "L2", 40,
           "dE/dt fluctuates from snapshot to snapshot; only its mean is zero. The energy budget is a law of the crowd.",
           "Each shoebox photo drops a marble into an amber histogram of dE/dt (computed from the model's right-hand side); "
           "the histogram breathes around zero; its mean marker sits exactly at 0. A bank-account ledger flashes as a preview.",
           "'true on average, not for each'; amber E[P - eps] = 0",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.93"], motifs=["M5 amber histogram"],
           sources=["R:321", "R:265-278"]),
    ],
}

C5 = {
    "id": "C5", "cut": "core", "title": "Counting crossings from still photographs", "levels": "L2-L3",
    "learning_goal": "Understand Rice's formula as 'a toll counter without a clock' and see it reproduce the true flip rate from snapshots alone.",
    "takeaway": "A shoebox of snapshots plus the equations gives the flip rate without running time forward.",
    "scenes": [
        sc("C5.1", "A toll counter without a clock", "L2", 40,
           "From one aerial photo with readable speedometers, count cars in a thin strip, weight by speed, divide by the width: crossings per hour.",
           "Aerial highway with a line across it; a thin strip around the line highlighted; cars inside the "
           "strip glow with their speed; a counter computes the rate; no clock anywhere.",
           "'rate = (cars in strip x speed) / strip width'"),
        sc("C5.2", "Rice for the dipole", "L3", 50,
           "For D, the strip is |D| < h and each snapshot's speed Ddot = -nu D + V Q comes from the equations.",
           "Shoebox points spread in the (D, Ddot) plane; the strip |D| < h (h = 0.2) lights up; each point's "
           "|Ddot| drawn as a bar; equation morph to the formula.",
           "nu_0 = lim_{h->0} (1/2h) E[ |Ddot| 1{|D|<h} ];  reference chip 'Kac 1943; Rice 1944-1945'",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.90"], sources=["R:510-538", "R:703-709"]),
        sc("C5.3", "Check against the truth", "L3", 35,
           "On the true distribution, with no time order, Rice reproduces direct counting within 4% near the threshold and 6% above.",
           "Rates vs Gamma: direct count (solid vermillion) and Rice on reference snapshots (amber) drawn on together.",
           "'cumulative error 4% (0.865 <= Gamma <= 0.885) · 6% (Gamma >= 0.89)'; source chip DATA · E1",
           assets=["experiences/figures/e1_seuil-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine.taux_rice_ref"], sources=["R:883"]),
        sc("C5.4", "What Rice does not say", "L3", 20,
           "Rice counts every zero crossing (excursions too), needs the right-hand side, gives no waiting times, and was tested on a 3-variable deterministic system.",
           "Four caveat cards slide in, one per sentence.",
           "four caveat cards", sources=["pedagogy P15"]),
        sc("C5.5", "Photographs on demand", "L3", 20,
           "So all we need is a cheap source of snapshots at any knob setting. Checkpoint L2 -> L3.",
           "The green parameter axis from C3.6 returns, gaps glowing; rail climbs to L3.",
           "'Level 2 -> Level 3'", motifs=["M8 rail", "callback C3.6"]),
    ],
}

C6 = {
    "id": "C6", "cut": "core", "title": "A machine that dreams snapshots", "levels": "L3",
    "learning_goal": "Understand conditional flow matching as learning an average wind from noise to data, conditioned on the knob, "
                     "and how generated distributions are judged against a noise floor.",
    "takeaway": "A generative model learns a wind that carries noise to data, one model for every knob setting, judged against the noise floor.",
    "scenes": [
        sc("C6.1", "From noise to data", "L3", 35,
           "A wind field carries a cloud of random points onto the shape of the data.",
           "Round violet Gaussian cloud (M4); a time-dependent wind bends particle paths onto two symmetric "
           "blobs; granular hiss under the motion.",
           "'generative model: new, plausible examples on demand'",
           assets=["assets/interactif/flow-matching.js", "figures/flow-matching/figure/out/flow-matching-en.svg"],
           render="dense2d", motifs=["M4 violet cloud (first)"], sources=["R:282-296"]),
        sc("C6.2", "Straight strings, average wind", "L3", 50,
           "Training is plain regression: at each place and moment, learn the average direction of straight noise-to-data strings.",
           "Thousands of straight strings from noise points to data points; at a probe location the passing "
           "strings average into one violet arrow; the learned field's trajectories curve but never cross.",
           "x_t = (1 - t) x_0 + t x_1;  J(v) = E || v(x_t, t, lambda) - (x_1 - x_0) ||^2;  v* = E[x_1 - x_0 | x_t, lambda]",
           assets=["figures/flow-matching/figure/out/flow-matching-en.svg", "prep/p7-modeles-generatifs/fig-chemins-en.png"],
           render="dense2d", sources=["R:282-296", "R:593-601"]),
        sc("C6.3", "Turn the knob, reshape the cloud", "L3", 30,
           "One model for a continuum of knob settings, including settings never simulated (interpolation).",
           "Green knob drives lambda; target blobs drift and the violet cloud follows; on the knob axis training "
           "values are filled dots, test values open dots.",
           "'trained on filled dots, tested on open dots (interpolation only)'",
           assets=["prep/p7-modeles-generatifs/fig-fm-conditionnel-en.png"], render="dense2d",
           sources=["R:743"], motifs=["M2 knob", "M4 cloud"]),
        sc("C6.4", "Two clocks, two velocities", "L3", 20,
           "The generator's time t in [0, 1] is not physical time, and its velocity v_theta (violet) is not the fluid velocity u (blue).",
           "Side-by-side chips: violet clock 't: transport time' vs grey clock 'physical time'; violet arrow v_theta vs blue arrow u.",
           "'the generator makes snapshots, not movies'", sources=["R:320-322"]),
        sc("C6.5", "The noise floor", "L3", 45,
           "Two honest samples of the same truth differ; compare models with that floor at equal sample size, never with zero.",
           "A die rolled 1000 times, twice: two amber histograms differ; their distance becomes a dashed grey "
           "floor line. Then the energy distance built term by term over two point clouds with faint pairwise lines.",
           "E(P, Q) = 2 E||X - Y|| - E||X - X'|| - E||Y - Y'||; dashed 'floor'",
           assets=["prep/p5-probabilites-transport/fig-wasserstein-1d-en.png"],
           motifs=["dashed grey floor (first)"], sources=["R:715-725", "R:747"]),
        sc("C6.6", "A lopsided machine", "L3", 35,
           "A plain conditional model reproduces the cloud's shape but inherits the training data's polarity imbalance.",
           "(Q, D) clouds at Gamma = 0.85: reference (grey, solid chip SIMULATED) vs baseline model A (violet chip "
           "GENERATED); a polarity balance bar shows A's tilt. Ends on a question mark at the mirror.",
           "'Gamma = 0.85, a value never seen in training'",
           data=["experiences/resultats/e1_echantillons.npz#ref|0.85", "experiences/resultats/e1_echantillons.npz#A_reference|0.85"],
           render="dense2d", sources=["R:855-873"]),
    ],
}

C7 = {
    "id": "C7", "cut": "core", "title": "Physics, where it is true", "levels": "L3-L4",
    "learning_goal": "Sort physical constraints into per-sample laws (build in) and crowd laws (impose on the distribution), "
                     "see exact mechanisms beat penalties, equivariance beat augmentation, and per-sample enforcement of a crowd law fail.",
    "takeaway": "Enforce a constraint where it is true: build per-sample laws into every output, impose crowd laws on the crowd, "
                "never force a crowd law onto each individual.",
    "scenes": [
        sc("C7.1", "Two shelves", "L3", 45,
           "Taxonomy C1-C4: true for every field (C1 linear, C2 nonlinear algebraic) vs true only for the crowd (C3 symmetry, C4 stationary budgets).",
           "Two shelves; laws arrive as cards and are placed: left shelf with a single-card icon in neutral ink, "
           "right shelf with an amber card-stack icon; each shelf gets its tools. Redrawn taxonomy (no blue for per-sample).",
           "'Enforce a constraint where it is true'; C1: x in ker A · C2: c(x) = 0 · C3: g#mu = mu · C4: E_mu[L phi] = 0",
           assets=["figures/taxonomie/figure/out/taxonomie-en.svg"],
           flags=["REDRAW: site figure uses blue for per-sample, which clashes with blue = u"], sources=["R:304-317", "R:1199"]),
        sc("C7.2", "Predict: does clean data make clean outputs?", "L3", 35,
           "A model trained only on divergence-free fields still outputs a relative divergence of 0.41; a soft penalty only reaches 0.34 (u) / 0.16 (B) and inflates magnetic energy 2.7x.",
           "Predict card; generated 2D MHD maps (u silver-blue, B silver-orange) reconstructed from Fourier "
           "coefficients at eta = 0.00951, free model V0 vs reference; a divergence map lights up hot spots; penalty bars follow.",
           "'free: 0.41 · penalty: 0.34 (u) / 0.16 (B) · penalty E_B x2.68'; chip 'forced 2D MHD: not a dynamo (Zeldovich)'",
           assets=["experiences/figures/e2_mecanismes-en.svg", "experiences/figures/e2_spectres-en.svg"],
           data=["experiences/resultats/e2_echantillons.npz#V0_libre", "experiences/resultats/e2_echantillons.npz#ref",
                 "experiences/resultats/e2_mhd2d.json#evaluation"],
           predict="Q5: trained only on perfectly divergence-free fields, are the outputs divergence-free? (Answer: no, 0.41.)",
           render="dense2d", flags=["HYPOTHESIS label for 'the penalty is gamed by inflating the swirl part'"],
           sources=["R:1023-1027", "R:931-961"], motifs=["anti-dynamo payoff"]),
        sc("C7.3", "Hill maps and swirl minus slope", "L3", 50,
           "Generate potentials (a landscape) and take the curl: zero divergence for free. Or project: remove each wave's component along its own direction.",
           "A landscape psi with water walking its contour lines (the C1.2 box returns: nothing piles up); then "
           "Fourier space: each wave's arrow loses its component along k (projector motif M6). A gauge needle drops to 1e-17.",
           "u = (d_y psi, -d_x psi);  u_k -> (I - k k^T / |k|^2) u_k;  gauges: final projection 5e-17 · potentials 1.7e-17 · projected flow 2e-8 (single precision)",
           assets=["assets/interactif/leray.js", "prep/p1-calcul-vectoriel/fig-helmholtz-en.png", "prep/p1-calcul-vectoriel/fig-courant-en.png"],
           data=["experiences/resultats/e2_mhd2d.json#evaluation", "experiences/resultats/e2_echantillons.npz#V4_potentiels"],
           render="dense2d", flags=["CAVEAT: divergence measured with the same spectral operator (P16)"],
           motifs=["M6 projector", "callback C1.2 box"], sources=["R:1023-1029"]),
        sc("C7.4", "Why almost is not exactly", "L4", 40,
           "The ideal wind must squeeze the off-constraint part at a rate 1/(1 - t) that blows up at the end; a bounded network cannot.",
           "T3 ink change to PAPER; plot of 1/(1 - t) shooting up near t = 1, with a capped curve for a bounded "
           "network; the residual gap stays O(1).",
           "Prop. 2: v* = m(P x, t) - (I - P) x / (1 - t); Remark 3.6",
           register="PAPER", sources=["R:345-386"]),
        sc("C7.5", "Predict: the mirror test", "L3", 55,
           "Augmentation symmetrizes only where data exist; a mirror built into the network keeps both polarities equally likely at every knob value.",
           "Predict card; training data lopsided below threshold (P(D > 0) = 0.375 at Gamma 0.80, 0.3125 at 0.86). "
           "Asymmetry vs Gamma for A, B, C drawn per Gamma (train filled, test open): A spikes, B dips only at training values, "
           "C sits on the dashed floor. Then (Q, D) clouds A vs C at 0.85 and the mirror gate S acting on the violet cloud.",
           "'A: 0.183 at 0.86, 0.085 at unseen 0.87 · B: 0.020-0.025 between training values · C: about 0.004 (floor) everywhere'; v_sym = 1/2 [v(x) + S v(S x)], S = diag(-1, -1, 1)",
           assets=["experiences/figures/e1_symetrie_projection-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#evaluation", "experiences/resultats/e1_gissinger.json#donnees",
                 "experiences/resultats/e1_echantillons.npz#A_reference|0.85", "experiences/resultats/e1_echantillons.npz#C_equivariant|0.85"],
           predict="Q6: one student learns from mirrored copies, the other has a mirror built in. At an unseen knob value, who stays symmetric? (Answer: the built-in mirror.)",
           render="dense2d", motifs=["M10 mirror", "two whirlpools"], sources=["R:855-873", "R:400-412"]),
        sc("C7.6", "The budget is blind to the mirror", "L4", 20,
           "Any mixture of the two polarities satisfies the energy identities, so symmetry must be imposed separately.",
           "A slider p mixes the two whirlpool clouds; the amber identity gauge stays at zero for every p; the "
           "lopsided model A shows the smallest control residual.",
           "p mu+ + (1 - p) mu- satisfies E[L phi] = 0 (Remark 3.7); 'A: degree-3 control residual 0.0167 (lowest)'",
           data=["experiences/resultats/e1_gissinger.json#evaluation"], sources=["R:415-417", "R:873"]),
        sc("C7.7", "Predict: balance every snapshot?", "L4", 55,
           "Forcing the stationary budget on each sample makes a spike that the truth never produces: worse, not better (Corollary 6).",
           "Predict card; bank-account ledger; the amber dE/dt histogram (reference, Gamma = 0.93) and a hand "
           "that pushes every marble onto zero: the histogram collapses into a spike. Numbers land after the picture.",
           "'E1: energy distance x9 (0.0231 vs 0.00257) · sigma(dE/dt) -> 4e-17 · E2: dissipation spread x 8.6e-4'; "
           "Cor. 6: no atom at 0 => any nu on {L phi = 0} is singular: KL = inf, W1 >= E|L phi| / L",
           assets=["assets/interactif/contrainte-loi.js", "experiences/figures/e1_symetrie_projection-en.svg"],
           data=["experiences/resultats/e1_echantillons.npz#E_projection_C|0.93", "experiences/resultats/e1_echantillons.npz#ref|0.93",
                 "experiences/resultats/e2_mhd2d.json#en_loi"],
           predict="Q7: energy in must equal energy out. Force every snapshot to balance exactly: better or worse? (Answer: worse.)",
           motifs=["the spike (first)", "M5 histogram"], sources=["R:448-460", "R:881", "R:1035"]),
        sc("C7.8", "Enforce it on the crowd, with two juries", "L4", 50,
           "Impose the budget on the generated distribution during training, even at knob values with no data; estimate it with two independent half-batches.",
           "A batch of violet samples votes; squaring one batch mean secretly adds a variance penalty (a hidden "
           "spike-maker); splitting into two juries and multiplying their means removes it.",
           "E[gbar^2] = (E g)^2 + Var(g)/n;  E[gbar_a gbar_b] = (E g)^2;  S_lambda(theta) = sum_k (E_q[L phi_k] / s_k)^2",
           motifs=["two juries"], sources=["R:663-683", "R:488-496"]),
        sc("C7.9", "Three ways to fix a budget", "L4", 60,
           "At unseen eta, the crowd-level loss cuts the energy distance from 2.58 to 0.70 while a control run gains nothing; tilting collapses the effective sample; per-sample rescaling makes a spike.",
           "Bar race over three lanes with the dashed floor: (1) training loss V5 vs base V4 vs control; (2) exponential "
           "tilting with an ESS counter ticking down ('a poll that shrank to two people'); (3) per-sample rescaling "
           "whose dissipation histogram collapses while its spectral distance looks fine.",
           "'V4 2.58 · control 2.52 · V5 0.70' · 'energy errors 26% / 37% -> 7% / 6%' · 'sigma(D) ratio 0.66 -> 0.79' · "
           "'tilting: residual 0.47 -> 0.19, distance 2.62 -> 4.15, mean ESS/N 0.29' · 'rescaling: sigma ratio 8.6e-4, distance 1.1'; chip 'one seed per variant'",
           assets=["experiences/figures/e2_en_loi-en.svg"],
           data=["experiences/resultats/e2_mhd2d.json#evaluation", "experiences/resultats/e2_mhd2d.json#en_loi"],
           flags=["CAVEAT: one seed, interpolation only (P10, P11)"], motifs=["M5", "dashed floor", "the spike"],
           sources=["R:1031-1035", "D:132-162"]),
        sc("C7.10", "The whole machine", "L4", 35,
           "Recap of the framework, then checkpoint L3 -> L4.",
           "The report's framework figure revealed panel by panel (a latent flow to a symmetric law, b potential "
           "decoder, c VKS geometry, d distributional control, e downstream uses); rail to L4.",
           "panel labels; 'Level 3 -> Level 4'",
           assets=["figures/cadre/figure/out/cadre-en.svg"], motifs=["M8 rail"], sources=["R:300"]),
    ],
}

C8 = {
    "id": "C8", "cut": "core", "title": "The honest scoreboard", "levels": "L4",
    "learning_goal": "See the 'how often' payoff with its error bars, why a smooth generator must blur a jump, and what remains weak.",
    "takeaway": "On a toy model the flip rate is predicted from generated snapshots alone, well far from the threshold and poorly near it, "
                "for a reason that is geometry, not bad luck.",
    "scenes": [
        sc("C8.1", "How often, from generated photographs", "L4", 55,
           "Rice applied to generated snapshots predicts the crossing rate with 14% cumulative error for Gamma >= 0.89 (up to 65% at a single value) and 42% near the threshold.",
           "The C4.3 curve returns; Rice on reference (amber) and Rice on generated samples of model C (dashed, violet chip) "
           "and model F are drawn on; error bands per region.",
           "'far from threshold: 14% cumulative, pointwise mean 17%, up to 65% at 0.905-0.91 · near threshold: 42%'",
           assets=["experiences/figures/e1_seuil-en.svg", "proto/scenes/d_curve.html"],
           data=["experiences/resultats/e1_gissinger.json#grille_fine", "proto/data/e1_rate.json"],
           flags=["CAVEAT: cumulative vs pointwise; zero crossings, not reversals (P15)"],
           motifs=["callback: 'how often' (cold open)"], sources=["R:883", "D:79-121"]),
        sc("C8.2", "Predict: early, late or on time?", "L4", 40,
           "Near the threshold the generator switches on late, then overshoots.",
           "Predict card; zoom on 0.86-0.90; the generated curve lags then crosses above the truth.",
           "'0.865: 0.00030 predicted vs 0.00194 true · 0.88: 0.00500 vs 0.00340 · onset delayed by 0.005-0.01'",
           data=["experiences/resultats/e1_gissinger.json#grille_fine"],
           predict="Q8: near the threshold, will the predicted flip rate switch on early, late or on time? (Answer: late, then overshoot.)",
           sources=["R:883"]),
        sc("C8.3", "A rubber sheet over a staircase", "L4", 45,
           "A generator that varies smoothly with the knob must be far from a distribution that jumps (Proposition 9).",
           "An elastic sheet stretched over a cliff, rounding the edge; then the generated (Q, D) cloud swept across the 21 "
           "Gamma values next to the reference, with the bridge mass P(|D| < 0.25) as a bar that fills too early and too softly.",
           "W1(q_lambda, q_lambda') <= K |lambda - lambda'|  =>  max error near lambda_c >= (J_delta - 2 K delta) / 2",
           data=["experiences/resultats/e1_gissinger.json#grille_fine.pont_ref",
                 "experiences/resultats/cache_e1/e1_echantillons_complet.npz"],
           render="dense2d", flags=["LOCAL_ONLY: cache_e1 is gitignored, present on this machine only"],
           motifs=["squeal callback", "M2 knob"], sources=["R:544-564"]),
        sc("C8.4", "The loss is not a clean win", "L4", 30,
           "On a good model the crowd loss halves stationarity residuals but narrows dE/dt; on a biased model it fails.",
           "Bars with floors: enforced residual 0.0136 vs 0.0324 (control); energy distance within seed spread; "
           "sigma ratio 1.04 -> 0.75; the biased model's bars blow off the chart (one seed diverged).",
           "'good model: residuals / 2, sigma ratio 0.75 · biased model: one seed diverged, the other worse'",
           assets=["experiences/figures/e1_variantes-en.svg"],
           data=["experiences/resultats/e1_gissinger.json#evaluation"], sources=["R:875-877"]),
        sc("C8.5", "Still far from the data", "L4", 30,
           "The models remain well above the data's own noise floor; few seeds; interpolation only.",
           "Spectral error bars of all variants against the data floor on a log axis; seed counters; 'interpolation' chip.",
           "'spectral error 0.07-0.23 (log10) vs 0.002-0.011 for data · E1: 2 seeds · E2: 1 seed · interpolation only'",
           data=["experiences/resultats/e2_mhd2d.json#evaluation"], sources=["R:80", "R:1039", "R:743-745"]),
        sc("C8.6", "Scoreboard", "L4", 30,
           "Eight mechanisms, each with its class, where it acts, exactness, cost and effect.",
           "Eight cards dealt onto the two shelves of C7.1 (potentials, final projection, projected flow, penalty, "
           "equivariance, stationarity loss, tilting, per-sample projection).",
           "mechanism table (report R:1149-1158)", sources=["R:1149-1158"]),
        sc("C8.7", "Recap: three lessons", "L4", 20,
           "Exact where exact; on the crowd where statistical; judge against the floor.",
           "Motif recap only (box, mirror, spike, floor).",
           "three one-line lessons", motifs=["recap beat"]),
    ],
}


def regen(scene_data, upstream, provisional_run, final_run, extractor, shippable_now, criterion=None,
          narration="two variants: pending (bet + criterion) and result (slots filled from the data file; wording for met / not met / inconclusive)"):
    return {"scene_data": scene_data, "upstream": upstream, "provisional_run": provisional_run,
            "final_run": final_run, "extractor": extractor, "shippable_now": shippable_now,
            "criterion": criterion, "narration": narration}


C9 = {
    "id": "C9", "cut": "core", "title": "The climb to 3D: bets on the staircase", "levels": "L4-L5",
    "learning_goal": "See the PhD plan as a staircase of test benches and the data factory that will feed it; read each upper step as a "
                     "pre-registered bet with its success criterion.",
    "takeaway": "Every step up the staircase is a bet written down before the data exist, with the criterion that will settle it.",
    "scenes": [
        sc("C9.1", "The staircase", "L4", 30,
           "Tiers 0-4: reduced reversal models, 2D MHD, 3D periodic dynamos, the VKS cylinder, the precessing DRESDYN cylinder.",
           "Staircase (M7) built step by step; T1 morph: the 2D square tiles into a 3D periodic box, which rounds into a "
           "cylinder, which starts to precess. Current tier lit.",
           "tier names; chip 'PhD proposal: not accepted, not funded'",
           assets=["figures/plan-these/figure/out/plan-these-en.svg"], motifs=["M7 staircase (first)"],
           flags=["CAVEAT: proposal only (P27)"], sources=["T:878-953"]),
        sc("C9.2", "The data factory", "L4", 45,
           "A reproducible pipeline: campaign recipe -> simulations -> labelled files -> catalog -> dataset -> training -> evaluation.",
           "BLUEPRINT register; a kitchen line of grey stations: recipe card (YAML, green knob on it), ovens (local, Docker, "
           "Slurm), jars with tamper-proof labels (MFF: HDF5 + UUID, commit, SHA-256), ledger (catalog), tasting menu, "
           "chef in training (violet), critic (amber).",
           "'tested end to end on CPU (68 automated tests) · not yet run on a GPU or a real cluster'",
           assets=["figures/architecture/figure/out/architecture-en.svg", "assets/interactif/architecture.js"],
           register="BLUEPRINT", sources=["C:45", "C:88-149", "C:190"], flags=["CAVEAT: HPC not yet run (P25)"]),
        sc("C9.3", "First product off the line: the 2D sweep", "L4", 35,
           "Ensembles of 2D MHD maps across 11 values of eta; injection and dissipation fluctuate around equality: the crowd law on real data.",
           "A grid of 11 small (omega, j) map tiles, one per eta (silver-to-hue maps); under each, a short trace of "
           "injection vs dissipation crossing and recrossing; an amber histogram of dE/dt per eta centred on zero.",
           "per-eta mean and spread of dE/dt from the data file; stamp 'SIMULATED · palier1_mhd2d · 32^2 · run <id>'",
           data=["data/palier1_sweep.json"], status=P, render="dense2d", register="NIGHT",
           regen=regen("data/palier1_sweep.json",
                       "11 MFF files {store}/palier1_mhd2d/{uuid}/fields.h5: t1_fields/velocity, magnetic_field (16, 150, 32, 32, 2) float32; "
                       "milady_diagnostics/injection, dissipation, kinetic_energy, magnetic_energy; catalog rows campaign/simulation/file",
                       "make sweep CONFIG=infra/configs/palier1_mhd2d.yaml  (CPU; the campaign as configured; same workload as the E2 data, about 30 min, X:69)",
                       "tier 1 at full scale (128^2, 8 x 8 (nu, eta) grid, about 700 GPU h, T:898-904): not configured yet",
                       "tools/extract_data.py: palier1_sweep() (to write; replaces the demo stub palier1_eta_sweep())",
                       "empty seat, or E2 samples at eta = 0.00951 only (experiences/resultats/e2_echantillons.npz) stamped PROVISIONAL",
                       None),
           sources=["CFG palier1_mhd2d.yaml", "C:93"]),
        sc("C9.4", "Bet 1: the ABC windows at 64^3", "L4", 40,
           "The dynamo windows measured at 32^3 should persist and sharpen at 64^3, up to Rm = 40, and the sign at Rm = 17.5 should be settled.",
           "The E3 32^3 curve as a grey ghost; the 64^3 points (two seeds each) drawn over it from the data file; "
           "windows re-shaded from the new zero crossings; inset 3D mode renders on both sides of each threshold.",
           "'bet: windows 8.9 < Rm < 17.5 and Rm > ~27 (published)'; stamp from data meta",
           assets=["experiences/figures/e3_abc-en.svg"], data=["data/palier2_abc3d.json", "experiences/resultats/e3_abc.json"],
           status=P, render="flat",
           regen=regen("data/palier2_abc3d.json",
                       "37 MFF files (Rm 4-40): magnetic_field (2, 20, 64, 64, 64, 3); diagnostics log_b_rms, growth_rate; catalog diagnostic growth_rate_fit "
                       "(query: python -m milady.catalog sims --campaign palier2_abc3d)",
                       "copy infra/configs/palier2_abc3d.yaml to $RUNS/configs/palier2_abc3d_n32.yaml with grid.N: 32 and name: palier2_abc3d_n32_provisional; "
                       "python -m milady.sweep $RUNS/configs/palier2_abc3d_n32.yaml --scheduler local --max-parallel 2 --device cpu  (estimate 1-1.5 h, unmeasured)",
                       "make sweep CONFIG=infra/configs/palier2_abc3d.yaml  (64^3; estimate ~15 h serial on 2 CPU threads, or GPU / Slurm array)",
                       "tools/extract_data.py: palier2_abc3d() (to write): (Rm, lambda, lambda_last_quarter, seed), interpolated thresholds, downsampled modes (.f32)",
                       EMPTY_SEAT + " The E3 32^3 curve is drawn as a labelled ghost.",
                       "published windows 8.9 < Rm < 17.5 and Rm >~ 27 (R:1112); sign of lambda at Rm = 17.5 resolved"),
           sources=["CFG palier2_abc3d.yaml", "R:1112-1114"]),
        sc("C9.5", "Bet 2: a dynamo that saturates (Taylor-Green)", "L5", 40,
           "A forced Taylor-Green flow should grow a weak seed field exponentially above a threshold in Rm = Re x Pm, then saturate: the first true dynamo of the staircase.",
           "Grid of log E_B(t) curves, one per (Re, Pm); each starts at the 1e-3 seed, grows or decays, then bends into a "
           "plateau; a (Re, Pm) map colours each point dynamo / no dynamo; optional 3D insert of saturated B.",
           "'anchor: Rm_c = 30 at Pm = 1 (Ponty et al. 2005), different forcing convention: qualitative only'",
           data=["data/palier2_tg3d.json"], status=P, render="webgl",
           regen=regen("data/palier2_tg3d.json",
                       "12 MFF files (Re 25-200 x Pm 0.5-2): velocity and magnetic_field (1, 40, 64, 64, 64, 3); diagnostics energies, dissipations, injection, "
                       "helicities, max divergences, growth_rate, b_rms, log_b_rms; catalog growth_rate_fit",
                       "copy infra/configs/palier2_tg3d.yaml to $RUNS/configs/palier2_tg3d_n32.yaml (grid.N: 32, new name); "
                       "python -m milady.sweep <copy> --scheduler local --device cpu --indices <Re <= 100, read the order with --dry-run>  (estimate 1-1.5 h, unmeasured; check resolution)",
                       "make sweep CONFIG=infra/configs/palier2_tg3d.yaml  (64^3, GPU, 10 h limit per simulation; estimate ~8 h CPU for all 12)",
                       "tools/extract_data.py: palier2_tg3d() (to write): per (Re, Pm) time series log E_B(t), fitted rate, saturated E_B, mean spectra",
                       EMPTY_SEAT,
                       "qualitative at this scale; tier-2 criterion 'Rm_c within 10% at a Pm without data' needs the full tier (T:912-918)"),
           flags=["CAVEAT: Re = 200, Pm = 2 may be under-resolved even at 64^3 (CFG palier2_tg3d.yaml:12-14)"],
           sources=["CFG palier2_tg3d.yaml", "T:908"]),
        sc("C9.6", "Bet 3a: a 3D generator, exact by construction", "L5", 25,
           "Generating vector potentials in Coulomb gauge makes div u = div B = 0 to rounding, and the B -> -B symmetry exact, whatever the training quality.",
           "Generated 3D field lines (violet frame, vermillion lines) beside the divergence gauge at ~1e-16; a mirror "
           "gate maps each generated sample onto its exact twin.",
           "'by construction (Prop. 1, Prop. 4): this shows the mechanism, not quality'; stamp 'GENERATED · fm3d smoke · kmax 3'",
           data=["data/fm3d_exactness.json"], status=P, render="webgl",
           regen=regen("data/fm3d_exactness.json",
                       "fm3d checkpoint + evaluation JSON (python -m milady.eval --out): metrics div_rel_u, div_rel_b; mirrored-sample check computed by the extractor",
                       "after the C9.5 provisional run: python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml --files <provisional TG fields.h5> "
                       "--set train.iters=200 data.kmax=3  (smoke scale: 6 iterations at kmax 3 took 5 s, IR:370; time at kmax 8 unmeasured); "
                       "python -m milady.eval --config infra/configs/train_fm3d.yaml --model <uuid> --out $RUNS/eval/fm3d_smoke.json",
                       "make train CONFIG=infra/configs/train_fm3d.yaml NGPUS=4; make eval CONFIG=infra/configs/train_fm3d.yaml EVAL_ARGS=\"--out eval_fm3d.json\"",
                       "tools/extract_data.py: fm3d_exactness() (to write)",
                       EMPTY_SEAT,
                       "relative divergence < 1e-12 (T:906-918)"),
           sources=["CFG train_fm3d.yaml", "R:327-335", "R:400-412"]),
        sc("C9.7", "Bet 3b: does it get the statistics right?", "L5", 35,
           "At a held-out point (Re = 50, Pm = 2) the generated spectra, energy budget and distribution distances are judged against the PhD plan's criteria.",
           "Spectra E_u(k), E_B(k): simulated (solid) vs generated (dashed, violet chip) at the held-out point; a criteria panel "
           "with three lamps (met / not met / inconclusive) filled from the evaluation file; bars vs dashed floor for train / val / test.",
           "criteria: log-spectrum error < 0.1 decade per band · budget residual and energy distance vs floor · Rm_c within 10% at a Pm without data (later)",
           data=["data/fm3d_eval.json"], status=N, render="flat",
           regen=regen("data/fm3d_eval.json",
                       "evaluation JSON {model, model_id, created, results: [{point, physical_parameters, metrics, details, seconds}]} with err_spectre_u_log10, "
                       "err_spectre_b_log10, residu_bilan_total, dist_energie, plancher_dist_energie; details spectrum_u, spectrum_b, spectrum_u_ref, spectrum_b_ref",
                       None,
                       "make train CONFIG=infra/configs/train_fm3d.yaml NGPUS=4 (GPU); make eval CONFIG=infra/configs/train_fm3d.yaml [MODEL=<uuid>] EVAL_ARGS=\"--out eval_fm3d.json\"",
                       "tools/extract_data.py: fm3d_eval() (to write)",
                       EMPTY_SEAT,
                       "tier-2 criteria of the PhD plan (T:906-918): divergence < 1e-12; log-spectrum error < 0.1 decade; Rm_c within 10% at a Pm without data; error at threshold / 2 with branch conditioning"),
           sources=["CFG train_fm3d.yaml", "milady/eval/metrics.py:588-662, 894-907"]),
        sc("C9.8", "The top steps: VKS and DRESDYN", "L5", 40,
           "The last two steps need consortium data that are not public: the bets and their criteria are written now.",
           "Two empty seats on the top steps: VKS cylinder (D, Q) plane with a dashed density frame; DRESDYN Rm_c(Po) axis "
           "with a dashed band; each with its data tag. If extension X6 is in the cut, this scene shortens to a 15 s bridge.",
           "VKS: 4 POD energy fractions within 10% · (D, Q) distance < 2x floor · Rice in the 95% Poisson interval; "
           "DRESDYN: Rm_c within 10% and correct symmetry class at a Po without data",
           data=["data/tier3_vks.json", "data/tier4_dresdyn.json"], status=N,
           regen=regen("data/tier3_vks.json + data/tier4_dresdyn.json",
                       "SFEMaNS / LATU simulations from the consortium (not public) converted to MFF grid_type fourier_fe_axisym "
                       "(milady_fourier_fe/fields/velocity (B, T, M, 2, N_fluid, 3), magnetic_field ...); generated u fields + kinematic eigenvalues per Po (format to define)",
                       None,
                       "consortium data access; native SFEMaNS reader to write (milady/data/convert.py:9-12); then train / eval as tier 2",
                       "tools/extract_data.py: tier3_vks(), tier4_dresdyn() (to write)",
                       EMPTY_SEAT + " Fallback: VKS schematic + Gissinger as 'pocket dynamo' proxy, chip SCHEMATIC.",
                       "T:927-953 criteria (a)-(d) for VKS, (a)-(b) for DRESDYN"),
           flags=["CAVEAT: no MilaDy data used (P3)"], sources=["T:927-953", "S:100"]),
    ],
}

C10 = {
    "id": "C10", "cut": "core", "title": "Back to the compass", "levels": "L5-L0",
    "learning_goal": "Separate what was measured from what is bet, and leave with the one-sentence lesson.",
    "takeaway": "We cannot say when the needle will turn, but we are learning to answer how often, by enforcing each law where it is true.",
    "scenes": [
        sc("C10.1", "Measured, and bet", "L5", 35,
           "Two columns: what the small experiments measured, and what the staircase bets.",
           "MEASURED column (E1, E2, E3 headline numbers with caveat chips); BET column (tiers 1-4 with data tags and a "
           "status pill READY / PROVISIONAL / PENDING read from timeline.json at build time, so it updates itself).",
           "headline numbers; status pills",
           data=["proto/timeline.json"], sources=["H:80-90"]),
        sc("C10.2", "The compass again", "L0", 60,
           "Closing narration: we cannot say when; we can learn how often; enforce each law where it is true.",
           "The compass in the hand returns (same shot as C0.1); behind it, faintly layered, every motif: barcode, "
           "threads, whirlpools, shoebox, violet cloud, mirror, the amber histogram that keeps its width; rail descends to L0.",
           "none until the last line; then the lesson in three short lines",
           render="webgl", motifs=["M1", "all motifs"]),
        sc("C10.3", "End card", "L0", 15,
           "Credits, sources, disclaimer, link to the site.",
           "Static card with a slow field-line drift.",
           "site URL; 'narration: original synthetic voice'; 'animations generated in code'; disclaimer; supervisors as listed in the public offer (decision D6)",
           flags=["DISCLAIMER"]),
    ],
}

# --------------------------------------------------------------------------------------------
# EXTENSION MODULES
# --------------------------------------------------------------------------------------------

X1 = {
    "id": "X1", "cut": "extension", "insert_after": "C2", "title": "Inside the twisting box (E3 in depth)", "levels": "L2-L4",
    "learning_goal": "See how a 3D solver is validated and what the dominant dynamo mode looks like.",
    "takeaway": "The 3D test bench passes an exact check and recovers the known windows, with honest limits on precision.",
    "scenes": [
        sc("X1.1", "A built-in answer key", "L3", 35,
           "B = u is an exact eigenmode of the ABC flow decaying at -1/Rm: the solver must return -0.5 at Rm = 2.",
           "A gauge lands on -0.5001 next to the exact -0.5.",
           "'exact: -1/Rm = -0.5 · measured: -0.5001'",
           data=["experiences/resultats/e3_abc.json#taux"], sources=["R:1116"]),
        sc("X1.2", "The mode in 3D", "L3", 45,
           "The dominant growing mode changes shape across the windows; it carries the flow's symmetries.",
           "Three.js render of the dominant mode B(x) at Rm 8, 12, 16, 20 (fat vermillion field lines and a |B| isosurface), "
           "orbiting slowly; a symmetry badge.",
           "'symmetry group of 24 elements; first-window mode has all even symmetries (Bouya and Dormy 2013)'",
           data=["experiences/resultats/e3_modes.npz"], render="webgl", sources=["R:1120"]),
        sc("X1.3", "How sure are the thresholds?", "L4", 35,
           "48^3 checks agree; the sign at Rm = 17.5 is unresolved; the third threshold is known to about one unit.",
           "Zoom on Rm = 17.5 with three tiny markers straddling zero (+2.3e-4, -2.2e-4, -5.2e-4); divergence gauge 3e-19 to 1.5e-16.",
           "'48^3: lambda = 0.00812 at Rm 12, -5.2e-4 at 17.5'",
           data=["experiences/resultats/e3_abc.json#convergence"], sources=["R:1114", "R:1118", "D:197"]),
        sc("X1.4", "Three definitions of Rm", "L3", 25,
           "A model conditioned on Rm must fix its convention.",
           "The same VKS impeller with three labels sliding on: 31, 44, 52-71.",
           "'Rm_c ~ 31 (Monchaux) · ~44 (Miralles) · 52-71 (Nore)'",
           sources=["en/prep/p3 line 1167", "en/prep/p3 line 1202"]),
    ],
}

X2 = {
    "id": "X2", "cut": "extension", "insert_after": "C7", "title": "The proofs behind the pictures", "levels": "L4",
    "learning_goal": "State Propositions 1-5 and their scope, as the specialists will want them.",
    "takeaway": "Each picture of C7 is backed by an elementary statement with a precise scope, often known in other forms.",
    "scenes": [
        sc("X2.1", "Proposition 1: build it in", "L4", 35,
           "If the decoder's image lies in the constraint subspace, every sample satisfies the constraint, whatever the training quality.",
           "PAPER; statement typed on; a decoder box whose output arrows all land on a plane.",
           "Prop. 1 statement", register="PAPER", sources=["R:327-335"]),
        sc("X2.2", "Proposition 2 in full", "L4", 50,
           "The optimal flow on a subspace splits into a learnable part and a stiff contraction; a bounded network leaves O(1) residuals.",
           "PAPER; the formula grows term by term; the contraction term is plotted against t; V3's 2e-8 explained by single precision.",
           "v* = m(P x, t) - (I - P) x / (1 - t); Remark 3.6", register="PAPER", sources=["R:345-386"]),
        sc("X2.3", "Proposition 3: the Jensen gap", "L4", 40,
           "A penalty on the end-of-path prediction is unbiased for linear constraints and biased for nonlinear ones.",
           "A curved constraint arc; the mean of two points falls off the arc: the gap is shaded.",
           "Prop. 3 statement", register="PAPER", sources=["R:389-395"]),
        sc("X2.4", "Proposition 4: the mirror, proved", "L4", 45,
           "Equivariant velocity + invariant noise give an exactly invariant distribution at every parameter; symmetrization never increases the population loss; it doubles network evaluations.",
           "Mirror gate on the violet flow, then the proof in three lines.",
           "v(g x, t, lambda) = g v(x, t, lambda), g#gamma = gamma => g#q(.|lambda) = q(.|lambda) for every lambda; 'cost: 0.5 s vs 0.25 s per 1000 samples'",
           register="PAPER", sources=["R:400-412", "R:885"], flags=["P22: classical for equivariant flows"]),
        sc("X2.5", "Proposition 5 and its limits", "L4", 40,
           "For every test function, E_mu[L phi] = 0; the energy budget is one case. Necessary, not sufficient: fixed points and unstable orbits satisfy it too.",
           "Amber identity, then a fixed point and an unstable orbit each pass the same test (warning lamp); degree <= 2 monomials enforced, degree 3 kept as a control.",
           "E_mu[L phi] = 0; Remark 3.11; 'enforced: degree <= 2 · control: degree 3'",
           register="PAPER", sources=["R:422-430", "R:569-571", "R:434", "R:727"]),
    ],
}

X3 = {
    "id": "X3", "cut": "extension", "insert_after": "X2", "title": "Crowd laws, deeper", "levels": "L4-L5",
    "learning_goal": "Understand exponential tilting as an I-projection, why it cannot create mass, the per-eta detail, and the 3D bet.",
    "takeaway": "Reweighting cannot visit places the model never went; the crowd loss must be tested again in 3D.",
    "scenes": [
        sc("X3.1", "The least-distorting correction", "L4", 40,
           "Exponential tilting is the I-projection: the reweighting that fixes a mean with minimal KL change, without moving any sample.",
           "Dots whose size is their weight; the tilted density slides to the target mean; Pythagorean triangle for KL.",
           "nu* = e^(beta . g) q / Z(beta);  beta* = argmin log Z(beta) - beta . c (Csiszar 1975); supp nu* = supp q",
           assets=["prep/p5-probabilites-transport/fig-inclinaison-en.png", "prep/p8-contraintes-physiques/fig-inclinaison-en.png"],
           sources=["R:465-485"]),
        sc("X3.2", "The poll that shrank", "L4", 45,
           "Effective sample size collapses exactly where the model is poor.",
           "Per-eta ESS bars from the data: 0.99 at the easiest eta, 0.002 at the three largest test eta; in E1 one sample swells to 33x the mean weight.",
           "ESS = 1 / sum w_i^2; 'E2: mean ESS/N 0.29 · 0.002 at large eta · E1 Gamma = 0.85: ESS/N 0.67, one weight 33x the mean'",
           data=["experiences/resultats/e2_mhd2d.json#en_loi.ess_frac_b", "experiences/resultats/e1_gissinger.json#evaluation"],
           sources=["R:1033", "R:879", "D:162"]),
        sc("X3.3", "Where the model never went", "L4", 35,
           "No weight can conjure samples in a region the model never produced; tilting is not a fallback.",
           "The 'missing support' toggle of the distributional widget: the bridge region is empty, weights explode, ESS counter falls.",
           "'reweighting cannot create mass'", assets=["assets/interactif/contrainte-loi.js"], sources=["R:465-485", "T:988-1000"]),
        sc("X3.4", "Per-eta detail", "L4", 30,
           "The crowd loss helps where the base model is worst and does nothing where it is already good.",
           "Three grouped bars per test eta (V4 / control / V5).",
           "'eta 0.01903: 7.74 / 7.63 / 2.22 · 0.01345: 3.63 / 3.51 / 0.792 · 0.00476: 0.184 / 0.178 / 0.186 · V4 signed residual +1.22 at 0.01903'",
           data=["experiences/resultats/e2_mhd2d.json#en_loi"], sources=["R:999-1013"]),
        sc("X3.5", "Bet: the crowd law in 3D", "L5", 35,
           "Does the distribution-level budget loss still help in 3D, without narrowing the dissipation, against a control run of equal length?",
           "The C7.9 three-lane race redrawn as empty seats for the 3D model: budget residual before/after, control lane, "
           "dissipation-spread gauge (needs a new metric).",
           "'bet: residual down, sigma(D)/sigma_ref in [0.8, 1.2], control gains nothing'",
           data=["data/fm3d_stationarity.json"], status=N,
           regen=regen("data/fm3d_stationarity.json",
                       "second fm3d model fine-tuned with the stationarity loss + control run (weight 0) + evaluation JSONs (residu_bilan_total, dist_energie, "
                       "plus a per-sample spread of the budgets, NOT computed by milady.eval today: C:166)",
                       None,
                       "python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml --init-from <final.pt> --set stationarity.enabled=true "
                       "stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 train.lr=1e-4 train.warmup=0; same command with the loss weight set to 0 "
                       "for the control (key name to check in train_fm3d.yaml); python -m milady.eval ... --out <file> for both",
                       "tools/extract_data.py: fm3d_stationarity() (to write) + add the sigma(dissipation) metric to milady.eval in the compute clone",
                       EMPTY_SEAT,
                       "tier-1/2 criteria: budget residual < 5% at parameters without data; sigma(D) ratio 0.8-1.2 (T:892-918)"),
           flags=["RISK: stationarity-loss variance in 3D (T:988-1000)"], sources=["CFG train_fm3d.yaml:13-15", "C:166"]),
    ],
}

X4 = {
    "id": "X4", "cut": "extension", "insert_after": "C8", "title": "What snapshots can and cannot tell", "levels": "L4-L5",
    "learning_goal": "Know the Rice estimator's bias and variance, the threshold bound on reversal rates, why waiting times need dynamics, "
                     "and the open questions on branches and tier 0.",
    "takeaway": "A snapshot generator bounds and estimates rates, but waiting times and hysteresis branches need more than the one-time law.",
    "scenes": [
        sc("X4.1", "Rice, the estimator", "L4", 40,
           "The window estimator has bias O(h^2) and variance O(1/(N h)); E1 uses h = 0.2.",
           "A slider on h trades a blurry strip against a noisy count; sanity checks: a cosine crosses twice per period; Gaussian case.",
           "bias O(h^2), variance O(1/(N h)); Gaussian: nu_0 = sigma' / (pi sigma)", sources=["R:703-709"]),
        sc("X4.2", "A bound from thresholds", "L5", 40,
           "Counting crossings of levels +/- a bounds the reversal rate: r <= nu_a (Prop. 2.30); the plateau conjecture 2.33 says when the bound is tight.",
           "Rates of crossings of +/- a vs a, from reference and generated snapshots, with the true reversal rate as a floor line; tightness band.",
           "r <= nu_a (Prop. 2.30); Conjecture 2.33; tier-0 criterion 'bound tight within 30%'",
           data=["data/x4_rice_levels.json"], status=P,
           regen=regen("data/x4_rice_levels.json",
                       "E1 reference trajectories (re-integrated, CPU minutes) and generated samples at all 21 Gamma (experiences/resultats/cache_e1/e1_echantillons_complet.npz, local only)",
                       "new extractor rice_levels(): level-a crossing rates on re-integrated Gissinger trajectories + Rice at level a on generated samples (CPU, minutes; code to write)",
                       "tier-0 campaign with 1e6 snapshots per parameter and 3 seeds (T:878-890, CPU, about 1e3 h assumption)",
                       "tools/extract_data.py: rice_levels() (to write)",
                       EMPTY_SEAT,
                       "Prop. 2.30 bound tight within 30% (T:878-890)"),
           sources=["T:683-727"]),
        sc("X4.3", "Waiting times need the movie", "L5", 35,
           "The one-time law does not determine the distribution of waiting times (Prop. 2.32); in the three-mode model they are quantized at short times and Poissonian at long times.",
           "Histogram of waiting times between reversals from a long live integration at Gamma = 0.90, with the short-time comb and the exponential tail.",
           "Prop. 2.32; 'quantized short, Poissonian long'", render="dense2d",
           sources=["T:683-727", "P4:1541"]),
        sc("X4.4", "Steep cliffs and the branch", "L5", 40,
           "Near a supercritical threshold a smooth generator obeys a square-root bound (Prop. 2.36); near a subcritical one, conditioning on the branch could remove it (Conjecture 2.38).",
           "A hysteresis loop drawn by a knob going up then down; two branches; an empty seat for 'error at threshold with vs without branch conditioning'.",
           "Prop. 2.36; Conjecture 2.38; criterion 'error at threshold / 2 with branch conditioning'",
           data=["data/x4_branch.json"], status=N,
           regen=regen("data/x4_branch.json",
                       "tier-2 full-scale campaign with hysteresis runs (Taylor-Green, up and down sweeps) + branch-conditioned model and its evaluation",
                       None,
                       "not configured beyond palier2_tg3d / train_fm3d (T:912-918; about 3900 GPU h for tier 2)",
                       "tools/extract_data.py: branch_conditioning() (to write)",
                       EMPTY_SEAT,
                       "error at the threshold divided by 2 with branch conditioning (T:906-918)"),
           sources=["T:768-788"]),
        sc("X4.5", "Tier 0, the next round", "L5", 30,
           "Three seeds, a derived reversal model (DQVU) and a joint state-parameter mirror R_pi that also flips the forcing asymmetry.",
           "Gissinger panel gains a third seed lane; a DQVU card (Re 1594, Rm 531, asymmetry 0.058, mu_r 16, POD on 2000 snapshots); R_pi mirror flips both the state and the asymmetry knob.",
           "Prop. 2.24; tier-0 criteria: asymmetry below floor at all Gamma, non-enforced residuals / 2 vs control, Rice within 20%",
           data=["data/x4_tier0.json"], status=P,
           regen=regen("data/x4_tier0.json",
                       "E1-style JSON (per-parameter metrics, fine-grid Rice) with 3 seeds; DQVU results later",
                       "run experiences/e1_gissinger.py from a working copy with seeds {0, 1, 2} (seeds are fixed in code; 2-3 h CPU, X:71), then experiences/digest.py",
                       "tier-0 plan (T:878-890); DQVU needs the published coefficients (Bousquet et al. 2026 appendix); no DQVU code in the repository",
                       "tools/extract_data.py: tier0() (to write)",
                       "E1 two-seed results with a '2 seeds' chip",
                       "T:878-890 criteria"),
           sources=["T:878-890", "S:98", "T:613"]),
    ],
}

X5 = {
    "id": "X5", "cut": "extension", "insert_after": "C9", "title": "The factory floor and the bill", "levels": "L3-L5",
    "learning_goal": "Open the data factory: one solver step, one file, one campaign trace, a new metric, the compute bill and the plan.",
    "takeaway": "Reproducibility is designed in, the bill is estimated with a factor-two uncertainty, and every number will be replaced by a measured one.",
    "scenes": [
        sc("X5.1", "One solver step", "L3", 40,
           "A pseudo-spectral MHD step goes back and forth between Fourier and physical space, with 2/3 dealiasing and an integrating-factor RK4.",
           "BLUEPRINT; a field tile hops between a Fourier grid and a physical grid; the 2/3 mask trims the corners; memory bar 6 N^3 x 4 bytes.",
           "'64^3 dynamic step: 0.08 s on 2 CPU threads · ~6 GB at 256^3, ~48 GB at 512^3'",
           assets=["figures/solveur/figure/out/solveur-en.svg"], register="BLUEPRINT", sources=["C:153", "C:176"]),
        sc("X5.2", "A jar with a label", "L4", 35,
           "Each simulation is one MFF file (HDF5, The Well convention) with UUID, commit and checksum, mirrored by a catalog row.",
           "File tree unfolds: t1_fields/velocity, magnetic_field, milady_diagnostics/*, scalars; a ledger row lights with the same UUID.",
           "MFF tree; catalog tables campaign, simulation, file, diagnostic, dataset, model, evaluation, job",
           assets=["figures/solveur/figure/out/solveur-en.svg"], register="BLUEPRINT", sources=["C:107-139"]),
        sc("X5.3", "The life of one campaign", "L4", 40,
           "From one command to files and catalog rows: a real trace with measured wall times.",
           "Terminal-style trace (mono) of a sweep: jobs light up, jars fill, ledger rows appear with wall_time_s; numbers from the run, not typed.",
           "command line; counts and wall times from the data file",
           data=["data/x5_campaign_trace.json"], status=P, register="BLUEPRINT",
           regen=regen("data/x5_campaign_trace.json",
                       "catalog dump of the palier1_mhd2d campaign (simulation rows with wall_time_s, file sizes, checksums)",
                       "same run as C9.3 (make sweep CONFIG=infra/configs/palier1_mhd2d.yaml), then python -m milady.catalog sims --campaign palier1_mhd2d",
                       "the same trace on the GPU VM or Slurm cluster for a palier2 campaign",
                       "tools/extract_data.py: campaign_trace() (to write)",
                       "architecture.js walk-through with a SCHEMATIC chip (no numbers)"),
           sources=["C:143-149", "IR:386"]),
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
           flags=["P20: no topology metrics were computed in the report"], sources=["R:739", "T:872-876"]),
        sc("X5.5", "The bill", "L5", 40,
           "The plan budgets about 1.1e4 A100 GPU hours (factor-two uncertainty); measured costs will replace the estimates.",
           "Stacked bar per tier (tier 1 ~700, tier 2 ~3900, tier 3 ~3200, tier 4 ~1200, 20% reserve) with a dashed second bar for measured hours, filled from the catalog.",
           "'plan: ~1.1e4 GPU h, uncertainty x2 · anchor: PCDM ~1150 GPU h'",
           data=["data/x5_compute_bill.json"], status=N, register="BLUEPRINT",
           regen=regen("data/x5_compute_bill.json",
                       "GPU solver benchmarks + catalog wall_time_s per campaign and per training run",
                       None,
                       "python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50 (IR:436); catalog SQL on simulation.wall_time_s (C:143-147)",
                       "tools/extract_data.py: compute_bill() (to write)",
                       "planned numbers only (T:955-974), each chip 'estimate'",
                       "within the plan's factor-two band (T:955-974)"),
           sources=["T:955-974"]),
        sc("X5.6", "The plan on one page", "L5", 45,
           "36 months, three axes, five tiers, three papers, named risks; chosen after scoring six directions.",
           "The thesis timeline SVG animated bar by bar (tiers, visits, committees, code releases, papers at months 10, 22, 33); "
           "risk cards; a small score table (A 4.10, B 3.90, merged).",
           "'papers: month 10 (distributional constraints) · 22 (hard constraints in bounded domains) · 33 (reversals and threshold)'",
           assets=["figures/plan-these/figure/out/plan-these-en.svg", "en/these/index.qmd"],
           flags=["CAVEAT: proposal, not accepted or funded (P27)"], sources=["T:1014-1126", "S:418-453", "T:988-1000"]),
    ],
}

X6 = {
    "id": "X6", "cut": "extension", "insert_after": "X5", "title": "Walls, metals and meshes", "levels": "L5",
    "learning_goal": "Meet the specialist frontier: gauges in bounded domains, permeability jumps, vacuum matching, hybrid meshes, "
                     "VKS and DRESDYN bets, and downstream assimilation.",
    "takeaway": "Leaving the periodic box changes what 'exact' means, and the real tests (VKS, DRESDYN) are written down as bets.",
    "scenes": [
        sc("X6.1", "A gauge for a bounded world", "L5", 45,
           "In a bounded domain the vector potential needs a fixed gauge (Coulomb, with A.n = 0 or A x n = 0), or its distribution is not well defined.",
           "The periodic box rounds into a cylinder; potential arrows at the wall snap to the boundary condition; two gauge choices side by side.",
           "div A = 0, A.n = 0 or A x n = 0 (Amrouche-Seloula)", register="PAPER", sources=["R:339", "T:211-260"]),
        sc("X6.2", "Iron changes the rules", "L5", 40,
           "Across a permeability jump, B.n and tangential B/mu_r are continuous: the potential has a kink; matching to vacuum outside is linear but nonlocal.",
           "An iron disc interface: field lines refract; the potential profile shows a kink; an exterior potential field wraps the cylinder.",
           "Prop. 2.6; 'vacuum matching without a Laplace solve per sample'", register="PAPER",
           sources=["T:114-115", "T:259", "T:272"]),
        sc("X6.3", "Two scalars and a hybrid mesh", "L5", 40,
           "Poloidal-toroidal storage (Prop. 2.8) in the box; SFEMaNS data are azimuthal Fourier modes times meridian finite elements, where div B is only weakly controlled.",
           "A meridian triangle mesh revolves into Fourier modes; a divergence gauge relabels itself 'with the solver's operator'.",
           "Prop. 2.8; MFF extension milady_fourier_fe; 'native SFEMaNS reader not implemented'",
           register="PAPER", flags=["P16 operator caveat"], sources=["T:324", "T:341", "R:1185", "milady/data/convert.py:9-12"]),
        sc("X6.4", "Bet 4: VKS in the generator", "L5", 45,
           "With consortium data, the generator should reproduce the dominant POD modes, the bimodal and asymmetric (D, Q) law, and a Rice rate within the Poisson interval.",
           "VKS cylinder with an empty (D, Q) density frame (dashed), four empty POD bars with 10% bands, a Rice gauge with a Poisson interval.",
           "criteria (a)-(d) of the PhD plan; joint mirror R_pi flips the asymmetry parameter (Prop. 2.24)",
           data=["data/tier3_vks.json"], status=N, render="webgl",
           regen=regen("data/tier3_vks.json",
                       "SFEMaNS / LATU VKS simulations (non-public): 384^3-equivalent snapshots ~1.4 GB each, 2000 snapshots ~2.7 TB; filtered 128^3 ~100 GB; "
                       "MFF grid_type fourier_fe_axisym",
                       None,
                       "consortium data access; SFEMaNS reader (to write); training and evaluation as tier 2 (about 3200 GPU h, T:968)",
                       "tools/extract_data.py: tier3_vks() (to write)",
                       EMPTY_SEAT + " Fallback: figures/vks schematic + Gissinger 'pocket dynamo' proxy (SCHEMATIC).",
                       "4 POD energy fractions within 10%; (D, Q) energy distance < 2x floor; interface residual < 1%; Rice in 95% Poisson CI (T:927-939)"),
           assets=["figures/vks/figure/out/vks-en.svg"], flags=["CAVEAT: data not public (P3)"], sources=["T:927-939"]),
        sc("X6.5", "Bet 5: DRESDYN, the precession knob", "L5", 35,
           "From generated velocity fields, recover the dynamo threshold Rm_c(Po) and the symmetry class of the dominant mode at a Po without data.",
           "Precessing cylinder (green Po knob); an empty Rm_c(Po) chart with a 10% band and a symmetry-class badge left blank.",
           "criteria (a)-(b) of the PhD plan; qualitative reference Botez et al. 2026",
           data=["data/tier4_dresdyn.json"], status=N, render="webgl",
           regen=regen("data/tier4_dresdyn.json",
                       "SFEMaNS precession simulations at the partners; generated u fields + kinematic eigenvalue results per Po (format to define)",
                       None,
                       "partner data; kinematic eigenvalue solver on generated flows (about 1200 GPU h for tier 4, T:968)",
                       "tools/extract_data.py: tier4_dresdyn() (to write)",
                       EMPTY_SEAT,
                       "Rm_c within 10% and correct symmetry class at a Po without data (T:941-953)"),
           sources=["T:941-953", "S:100"]),
        sc("X6.6", "Downstream: assimilation with a mirror", "L5", 35,
           "A generator as a prior: the reduced drift by conditional expectation (Prop. 2.40), and a posterior that is bimodal in +/-B (Prop. 2.41) unless the prior respects the mirror.",
           "Observation dots pull a violet ensemble; the posterior splits into two mirror humps; a lopsided prior biases one hump.",
           "Prop. 2.40; Prop. 2.41", motifs=["M10 mirror callback"], sources=["T:816-831"]),
    ],
}

CHAPTERS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, X1, X2, X3, X4, X5, X6]

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

LOGLINE = ("Nobody can say when Earth's magnetic field will flip next, but we can learn how often. "
           "One film climbs from a compass to the frontier of physics-constrained generative AI for dynamos.")

SYNOPSIS = ("It opens on a compass and the striped seafloor, then builds the physics picture by picture: "
            "stretch versus smudge, thresholds, and liquid-sodium experiments that flip like the Earth. "
            "Chaos hides the date of the next flip, yet a shuffled box of snapshots still holds the flip rate, through Rice's formula. "
            "Generative models then learn to dream such snapshots for any knob setting. "
            "At its heart is one lesson from a prospective internship study for the MilaDy project: "
            "enforce each law where it is true, exactly for every field, or on average for the crowd. "
            "Small CPU experiments show what works and what fails. "
            "It ends on written bets for 3D dynamos, VKS and DRESDYN, filled in as simulations arrive.")

OPENING = {
    "scenes": ["C0.1", "C0.2", "C0.3", "C0.4", "C0.5"],
    "tts_text": (
        "[calm, natural narrator voice] Hold a compass. The needle swings, hesitates, and settles. North. "
        "It has pointed north your whole life. It feels permanent. [long pause] "
        "It is not. Along the ridges of the ocean floor, fresh lava cools, and tiny magnetic grains freeze in place. "
        "Each grain remembers which way a compass would have pointed. As the seafloor spreads, these memories line up into stripes. "
        "And the stripes tell a strange story. The field has flipped. Not once. Many times. With no schedule at all. [long pause] "
        "So, two questions. When will it flip next? And how often does it flip? "
        "The first question turns out to be hopeless. The second one is not. "
        "Finding out why will take us from this needle to liquid metal, to chaos, and to machines that must be taught "
        "where the laws of physics are exact, and where they only hold on average."
    ),
    "cue_map": [
        ["Hold a compass", "C0.1"], ["It is not.", "C0.2"], ["Along the ridges", "C0.3"],
        ["The field has flipped", "C0.4"], ["So, two questions", "C0.5"],
    ],
    "notes": "The seafloor sentences rely on an external fact (decision D7). Site-only alternative for C0.3: "
             "'In a tank of liquid sodium in Cadarache, the field flips too.'",
}

CLOSING = {
    "scenes": ["C10.2"],
    "tts_text": (
        "[calm, natural narrator voice] Back to the compass in your hand. [long pause] "
        "We still cannot tell you when this needle will turn around. Nobody can. "
        "The dynamo below is chaotic. Its memory fades too fast. "
        "But it does answer another question: how often. That answer hides in a cloud of snapshots, "
        "and a machine can learn to draw such clouds, even at settings nobody has simulated. [long pause] "
        "On small test problems, it partly works. The mirror symmetry holds by construction. "
        "On a three-variable model, the flip rate comes out with a cumulative error of fourteen percent far from the threshold, "
        "and forty-two percent near it. The real tests, in three dimensions and in liquid metal, are still ahead. "
        "You have seen the bets. [long pause] "
        "One lesson remains. Enforce each law where it is true. Exactly, where it is exact. On average, where it only holds on average."
    ),
    "cue_map": [
        ["Back to the compass", "C10.2 compass"], ["We still cannot", "motifs layer in"],
        ["On small test problems", "E1 numbers as faint chips"], ["One lesson remains", "three-line lesson"],
    ],
    "notes": "Numbers follow pitfall P15 (cumulative error, two regimes). 'Holds by construction' refers to Proposition 4.",
}

DECISIONS = [
    {"id": "D1", "topic": "Narrator voice",
     "question": "Which original narrator voice (Fish Audio reference_id) should read the film? The request named a real public figure's "
                 "voice; the film will not clone or imitate any real person. The session task list mentions a voice called 'Ethan': "
                 "if that is an original or licensed library voice, please confirm and give its reference_id.",
     "options": ["an original Fish Audio library voice: we send 2-3 clips of the opening 60 s to choose from",
                 "a voice you hold the rights to (a consenting narrator)"],
     "default": "send 2-3 test clips of the opening", "blocks": "all narration audio, scene durations, subtitles timing"},
    {"id": "D2", "topic": "Fish Audio access",
     "question": "Provide FISH_API_KEY in the environment (never in a file) and confirm the validated drama-3 settings for English.",
     "options": ["key now: first live test on one scene", "later: build with the placeholder voice"],
     "default": "one-scene live test first (pace in words per minute, [long pause] length, phoneme pins)", "blocks": "live narration"},
    {"id": "D3", "topic": "Length and cut",
     "question": "Which cut ships first?",
     "options": ["core only (about 40 min)", "core + all extensions (about 60 min)",
                 "two episodes: Part 1 C0-C6 (L0-L3), Part 2 C7-C10 + extensions (L3-L5)", "core + chosen extensions"],
     "default": "core first; extensions as a second release or a long cut", "blocks": "script length, render budget"},
    {"id": "D4", "topic": "Provisional CPU runs",
     "question": "Launch the provisional CPU runs now, writing outside the site repository? Cheapest first: X-points on E2 samples "
                 "(minutes), Rice levels (minutes), palier1 2D sweep (~30 min), ABC 32^3 (~1-1.5 h, estimate), Taylor-Green 32^3 "
                 "subset (~1-1.5 h, estimate), fm3d smoke training, E1 with 3 seeds (2-3 h). Disk free: 8.7 GB.",
     "options": ["yes, on this machine", "yes, on the cloud VM", "no, ship empty seats"],
     "default": "yes, cheapest first", "blocks": "8 PROVISIONAL scenes"},
    {"id": "D5", "topic": "HPC and consortium data",
     "question": "When might the palier2 campaigns at 64^3, the GPU fm3d training and evaluation, and VKS (SFEMaNS/LATU) or DRESDYN data "
                 "be available? Ship with empty seats now, or hold the release?",
     "options": ["ship now with empty seats, update later", "hold until tier 2 results"],
     "default": "ship now; empty seats are part of the story", "blocks": "7 PENDING scenes"},
    {"id": "D6", "topic": "Supervisors on screen",
     "question": "Name the supervisors (as listed in the public offer: S. Cheng and D. Lucor, with C. Nore and Y. Ponty) in the "
                 "project lower-third and credits, or only 'the project's supervisors' with names in the video description?",
     "options": ["names in text, no photos, no logos, no opinions attributed", "no names on screen"],
     "default": "names in text only (C3.7, C10.3)", "blocks": "C3.7, C10.3"},
    {"id": "D7", "topic": "Facts not on the site",
     "question": "May the film use sourced external facts (seafloor magnetic stripes, Curie-temperature argument, self-exciting disc)?",
     "options": ["yes, with on-screen reference chips and sources in the description", "no: open on VKS reversals instead"],
     "default": "yes, sourced", "blocks": "C0.3, C1.1, C1.3 and the opening narration"},
    {"id": "D8", "topic": "Formula density at L4-L5",
     "question": "Show full statements of the propositions on screen (core C7-C8, extension X2), or statements in words with a pointer to the site?",
     "options": ["full statements, narration stays intuitive", "words only + site pointer"],
     "default": "full statements on a separate layer, never in subtitles", "blocks": "C7.4, C7.7, C8.3, X2, X6"},
    {"id": "D9", "topic": "Look",
     "question": "Dark-dominant film (NIGHT about 75%, PAPER for derivations, BLUEPRINT for infrastructure) or light, closer to the site? "
                 "Key-coloured field maps (silver for negative values) or a conventional red-blue map in single-field shots?",
     "options": ["dark + key-coloured maps", "light + site look", "dark + red-blue maps"],
     "default": "dark + key-coloured maps", "blocks": "every scene template"},
    {"id": "D10", "topic": "Music",
     "question": "No music, an original bed synthesized in code under L0-L2, or a licensed track?",
     "options": ["none", "original bed under L0-L2 only", "licensed"], "default": "original bed under L0-L2, silence under L4-L5",
     "blocks": "audio mix"},
    {"id": "D11", "topic": "Frame rate, resolution, render machine",
     "question": "1080p30 master (about 2 h for the core cut on this 4-core machine), 60 fps for particle and 3D chapters, or 4K "
                 "(needs a bigger machine and more than 8.7 GB of disk)? Render here or on a rented VM?",
     "options": ["1080p30 here", "1080p30, 60 fps for C4/C6/C9 heavy shots", "4K on a cloud VM"],
     "default": "1080p30 here", "blocks": "final render"},
    {"id": "D12", "topic": "Pronunciations",
     "question": "Confirm: Gissinger (French or English), DRESDYN, SFEMaNS, MilaDy, Karman.",
     "options": ["as in audio/lexicon.json", "your corrections"], "default": "lexicon entries marked CHECK", "blocks": "phoneme pins"},
    {"id": "D13", "topic": "Title",
     "question": "Pick a title: " + " / ".join(TITLE_OPTIONS) + ".",
     "options": TITLE_OPTIONS, "default": TITLE_OPTIONS[0], "blocks": "C0.6, thumbnails"},
    {"id": "D14", "topic": "Disclaimer",
     "question": "Approve the disclaimer wording (C3.8) and its placements (C3.8, end card, description).",
     "options": ["as drafted", "edited"], "default": "as drafted", "blocks": "C3.8, C10.3"},
    {"id": "D15", "topic": "Short vertical version",
     "question": "Produce a 9:16 Short from the long version? Candidates: C7.7 (the spike) or C4.2-C4.4 (whirlpools and 'when vs how often').",
     "options": ["yes, C7.7", "yes, C4.2-C4.4", "no"], "default": "yes, C7.7", "blocks": "nothing in the long cut"},
    {"id": "D16", "topic": "Subtitle timing",
     "question": "Sentence-level subtitle timing (ready) or word-by-word emphasis (install a CPU aligner, about 0.5 GB)?",
     "options": ["sentence level", "word level"], "default": "sentence level", "blocks": "subtitle style only"},
]

NOTES = [
    "Prototype script proto/script/demo_script.json, scene d_e1_rate, says the generative model 'reproduces the whole curve': "
    "this overclaims (42% error near the threshold). Use C8.1 wording instead.",
    "Prototype extractor palier1_eta_sweep() labels the E2 'recalage' series 'recalibrated'; 'recalage' is per-sample rescaling, "
    "the degenerate method of Corollary 6. Do not reuse that stand-in; C9.3 uses data/palier1_sweep.json from the real campaign.",
    "The site's taxonomy figure uses blue for 'true for each sample'; redraw it (C7.1) so blue keeps meaning velocity u.",
    "The 3D evaluation does not compute the per-sample spread of the budgets (C:166); add it before X3.5 can show a result.",
    "C8.3 reads experiences/resultats/cache_e1/e1_echantillons_complet.npz, which is gitignored and present only on this machine: "
    "copy it into the film project's data before moving the build elsewhere.",
    "Every PENDING scene ships as an 'empty seat' (part of the story), not as the hatched AWAITING preview, which is for drafts only.",
    "Status rule from the pipeline: a PENDING scene whose data file appears is promoted to PROVISIONAL automatically and stamped "
    "PROVISIONAL DATA until a human marks it READY in the script.",
]
