# MilaDy explainer video: pedagogy and visual metaphors

Working document for the script, storyboard and scene authors. Sources: the English site under `/home/user/milady-2027/en/` (index, rapport §1–7, these §1–4, interactifs, calcul, encadrants, prep p1–p8) and `experiences/resultats/digest.md`. Every number quoted below comes from those pages; facts that the site does **not** contain are marked **[external, source before use]**.

---

## 0. Ground rules for the whole video

### 0.1 The audience ladder (the "altitude meter")

The video climbs six levels. A small vertical altitude meter on the left edge of the frame shows the current level throughout, so every viewer always knows where they are and when the climb steepens.

| Level | Who it is for | Vocabulary allowed | Math on screen | Matching site material |
|---|---|---|---|---|
| **L0** | anyone curious | compass, magnet, field line, flip, liquid metal | none (numbers only: years, liters, degrees) | home page, VKS figure panel a |
| **L1** | high school, early undergrad | current, induction, feedback, threshold, ratio, exponential growth | one ratio ($Rm = UL/\eta$), one exponential | p1 ch1, p3 ch1–2 |
| **L2** | undergrad science and engineering | divergence, curl, eigenvalue, growth rate, chaos, attractor, histogram | short equations, each introduced by its picture | p1–p4 |
| **L3** | M1/M2 in physics or ML | distribution, sample, generative model, ODE flow, regression loss, projection, Fourier mode, equivariance, metric between distributions | full equations of the method | p5–p8, report §4 |
| **L4** | research level (M2 → PhD) | invariant measure, generator $\mathcal{L}$, stationarity identity, singular measure, KL, I-projection, ESS, Rice formula, Lipschitz bound | the propositions of report §3, stated (not proved) | report §3, these §2 |
| **L5** | supervisors and specialists | SRB measure, gauge, vacuum matching, permeability jumps, hybrid Fourier × finite elements, hysteresis branches, DQVU, bimodal posterior, compute budget | statements plus their failure modes and open conjectures | these §2–4, encadrants |

Rules of the climb:

1. **Never go down without saying so.** The level only rises, except in the closing, which deliberately returns to L0 (the compass).
2. **Picture, then words, then symbols.** Each idea appears first as a moving picture, then is named in plain words, then (from L2) gets its symbol. Symbols fade in on top of the picture element they name, in that element's colour.
3. **One idea per scene.** A scene introduces one new idea; at most one callback to an older one.
4. **Checkpoints and exit ramps.** At each level change, a 10–15 s checkpoint recaps the previous level in one sentence and says, honestly, "if you only wanted the big picture, you can stop here: here is what you now know". Chapter markers in the video description match these checkpoints.
5. **Two tracks above L3.** The narration keeps speaking intuition; the on-screen formula carries the precision for specialists. The burned-in subtitles carry the narration text (as the Videobook brainstorm requires); formulas live in a separate on-screen layer, never inside the subtitle line.

### 0.2 Colour rule (Okabe–Ito, colour-blind safe, site key)

| Colour | Means | Used for |
|---|---|---|
| green `#009E73` | control parameter $\boldsymbol\lambda$ | the "knob" glyph, sliders, $\Gamma$, $\eta$, $Rm$, $Re$, $Pm$, $\mu_r$, $Po$ |
| blue `#0072B2` | velocity $\mathbf{u}$ | flow arrows, streamlines, impellers' flow, $V$ mode of Gissinger |
| vermillion `#D55E00` | magnetic field $\mathbf{B}$ | field lines, compass needle tip, dipole $D$, quadrupole $Q$ (lighter tint) |
| violet `#6C4BA0` | generative model | noise blob, particle swarm, $v_\theta$, $q_\theta$, generated samples |
| amber `#E69F00` | distribution-level quantities | histograms, means $\mathbb{E}[\cdot]$, energy distance, ESS, stationarity identities |
| greys | infrastructure and reference | pipeline boxes, noise-floor dashed line, reference data clouds |

Consequences:

- **Polarity is encoded by shade, not by a new hue**: normal polarity = solid vermillion, reversed polarity = pale vermillion (or cream with vermillion outline). The paleomagnetic barcode uses the same two shades.
- **Per-sample vs distribution-level constraints**: the site's taxonomy figure (`figures/taxonomie/figure/out/taxonomie-en.png`) uses blue for "true for each sample". In the video, blue already means $\mathbf{u}$. Re-draw the taxonomy in the video palette: per-sample = ink/neutral plus a "single card" icon; distribution-level = amber plus a "stack of cards / histogram" icon. Do not show the site figure unmodified next to blue velocity arrows.
- **Every symbol inherits the colour of its picture.** $\mathbf{B}$ is always vermillion, $\lambda$ always green, $q_\theta$ always violet, $\mathbb{E}_\mu[\cdot]$ always amber.

### 0.3 Narrator persona

An original narrator: warm, curious, unhurried, wonder-driven, speaks in "we", asks the viewer real questions and waits for them. No catchphrases borrowed from real people; no line written as, or attributed to, any real named person. Enthusiasm is spent on ideas, never on overstated results (see section 4).

---

## 1. Narrative arc

Indicative runtime: about 60 minutes in 12 chapters. Durations are guidance for the script; chapters marked **[R]** contain regenerable beats that depend on results that do not exist yet.

| # | Chapter | Level | ≈ min | Role in the arc |
|---|---|---|---|---|
| 0 | Cold open: the compass that will one day lie | L0 | 2.5 | hook |
| 1 | The planet makes its own magnet | L0 → L1 | 5 | hook deepens, first principle |
| 2 | Stretch versus smudge | L1 → L2 | 6 | first rung of the climb |
| 3 | Dynamos you can build | L1 → L2 | 5 | grounding; central question and promise |
| 4 | Chaos, and the shoebox of photographs | L2 | 6 | the key reframing: trajectory → distribution |
| 5 | Counting crossings from still photographs | L2 → L3 | 4 | the promise sharpened (Rice, on the true data) |
| 6 | A machine that dreams snapshots | L3 | 7 | the tool |
| 7 | Teaching the machine physics, where physics is true | L3 → L4 | 10 | the core idea of MilaDy's framework |
| 8 | The honest scoreboard | L4 | 5 | payoff (and its limits) |
| 9 | The climb to 3D **[R]** | L4 → L5 | 5 | the bridge to the thesis |
| 10 | The frontier: open problems **[R]** | L5 | 4 | open problems at specialist level |
| 11 | Closing: back to the compass | L0 | 1.5 | callback, resolution |

### 1.1 The hook (ch. 0–1, L0)

**Open on a compass in a hand.** The needle settles. Pull back through the clouds to the whole Earth, vermillion field lines looping from pole to pole. Then the ocean floor: a long ridge, and on each side, a barcode of stripes, mirror images of each other. The narrator:

> "Every rock in this stripe remembers which way a compass would have pointed when it froze. Look at the pattern: the field has flipped. Not once. Many times. And not on a schedule."

The hook is a pair of questions that the whole video will answer:

- *When will it flip next?* We will discover that this question has no answer, even in principle, for a chaotic dynamo.
- *How often does it flip?* This question does have an answer, and a surprisingly cheap one. This is the thread that ties the cold open to the payoff (Rice formula, ch. 5 and ch. 8) and to the closing.

Why anyone should care, at L0, without doom: the field is generated by moving liquid metal, not by a permanent magnet; it can only exist if something keeps making it; that "something" is a machine we can barely simulate. Its flips are written in the rocks, and they also happen in a laboratory tank of liquid sodium in Cadarache (VKS). Do not claim any consequence of a reversal for life on Earth (see pitfalls).

### 1.2 The central question of MilaDy (end of ch. 3, L2)

After the laboratory dynamos, state the project's question in one sentence, on screen, with the colour key:

> "Simulating a dynamo is so expensive that we only get a handful of settings of the **knobs** (green). Can a machine learn the whole family of possible **fields** (blue and vermillion) for any setting of the knobs, respect the laws of physics **exactly where they are exact** and **statistically where they are statistical**, and tell us **how often the field flips**?"

Source: the ANR objectives (reversals and burst dynamos; DRESDYN exploration with parametric reduced models) and the internship offer (conditional generative models that respect the energy budget and zero divergence), as summarized in `en/encadrants` and `en/index`.

The status disclaimer belongs here, in plain words and on screen (see pitfall P1): this is a prospective study by a candidate, with small CPU experiments, not endorsed by the project or the supervisors.

### 1.3 The promise (end of ch. 3)

Three promises, each paid off later:

1. "We will see why the question *when* is hopeless, and why *how often* is not." (paid in ch. 4, 5, 8)
2. "We will see that 'make the AI obey physics' means two very different things, and that confusing them destroys the answer." (paid in ch. 7: Corollary 6 and the spike)
3. "And we will be honest about what works today on toy problems, and what has not been tried yet." (paid in ch. 8–10)

### 1.4 The climb (ch. 2–7)

The climb is a single chain of reframings. Each chapter ends on a question that the next one answers.

1. *Ch. 2 (L1→L2)*: a flow can amplify a field if it stretches faster than diffusion smudges. → "So why is it so hard to build one?"
2. *Ch. 3*: because liquid metals diffuse field fast and flow is turbulent at the needed speeds; three experiments succeeded; simulations are costly. → "And when it works, it flips. Can we predict the flips?"
3. *Ch. 4 (L2)*: no: chaos kills prediction of *when* within ~11 time units, while polarities last > 100. But the cloud of states is stable. → "If the cloud is all we can know, what can the cloud alone tell us?"
4. *Ch. 5 (L2→L3)*: the rate of flips, from still photographs (Rice), checked on the true data of the three-mode model. → "So all we need is a cheap source of photographs, for any knob setting."
5. *Ch. 6 (L3)*: a generative model by flow matching produces new photographs on demand, conditioned on the knob. → "But a machine trained on data does not automatically obey physics."
6. *Ch. 7 (L3→L4)*: the taxonomy. Some laws hold for every field (build them in); some hold only for the crowd of fields (enforce them on the crowd); forcing a crowd law on each individual destroys the crowd.

### 1.5 The payoff (ch. 8, L4)

- The equivariant model keeps both polarities equally likely at every knob value, including unseen ones, where data augmentation fails.
- Rice applied to the **generated** photographs predicts the crossing rate of the three-mode model with 14% cumulative error far from the threshold (up to 65% at a single value) and 42% near the threshold, where a smooth generator cannot follow the jump (Proposition 9). This is the "how often" payoff of the cold open, with its error bars shown, not hidden.
- In 2D MHD, the distribution-level energy budget brings the energy distance at unseen $\eta$ from 2.58 to 0.70 while a control run gains nothing; forcing the budget on each sample crushes the spread of dissipation to $8.6\times10^{-4}$ of the truth.
- And the honest twist: the models remain weak compared with the data noise floor, and the stationarity loss fails on a biased model in E1.

### 1.6 The open problems (ch. 9–10, L4→L5) **[R]**

The thesis ladder (tiers 0–4) as a staircase. Each upper step is presented as a **pre-registered bet**: what the theory predicts, the success criterion written in the PhD plan, and the data file that will settle it. These are the regenerable sections (section 1.8). Then the specialist frontier: bounded cylinders, vacuum matching, permeability jumps, hybrid meshes, branch conditioning near a subcritical threshold, waiting times that the distribution cannot give, bimodal posteriors in data assimilation.

### 1.7 The closing (ch. 11, L0)

Return to the compass in the hand, now with all the motifs layered faintly behind it: the barcode, the stretch-and-smudge threads, the two whirlpools, the shoebox, the violet swarm, the mirror, the amber histogram that keeps its width.

> "We still cannot tell you when this needle will turn around. Nobody can. But we are learning to ask the question the planet can answer: how often. And we are learning to teach machines a lesson that sounds simple and is not: obey a law exactly where it is exact, and on average where it is only true on average."

End card: what is measured, what is planned, link to the site.

### 1.8 Regenerable sections: how they work pedagogically

Missing results (HPC campaigns of tiers 1–2, 3D generative training and evaluation, SFEMaNS/VKS data, DRESDYN) are handled with one recurring device: **the empty seat**.

- Each regenerable beat is a scene with a chart frame drawn in dashed grey, axes already labelled, the success band already shaded, and a small grey tag naming its data source (for example `palier2_abc3d`). The narration states the bet *before* the data exist. This is good pedagogy in its own right: it shows how honest science is set up.
- Each beat has **two narration variants** written from the start: a *pending* variant ("this is the bet; this is how we will know") and a *result* variant with slots filled from the data file (value, comparison with the criterion, verdict "met / not met / inconclusive"). The *result* variant must have wording for failure as well as success; no slot may assume success.
- The *pending* variant is shippable as is. When data arrive, only that scene's narration audio, its subtitles and its chart are regenerated; the surrounding scenes do not change.

| Regenerable beat | Chapter | Data source (when it exists) | The bet, as stated now | Criterion to show (source) |
|---|---|---|---|---|
| R1 ABC at higher resolution | 9 | campaign `palier2_abc3d` ($64^3$, $Rm$ 4–40, 37 sims) | the dynamo windows of E3 (8.87, 17.6, 26.8 at $32^3$) persist and sharpen; the second threshold's sign at $Rm=17.5$ gets resolved | published windows $8.9 < Rm < 17.5$ and $Rm \gtrsim 27$ (report §5 E3) |
| R2 Taylor–Green forced MHD | 9 | campaign `palier2_tg3d` ($64^3$, $Re \in \{25,50,100,200\}$, $Pm \in \{0.5, 1, 2\}$) | a threshold appears and moves with $Pm$; near it, the distribution may jump (subcritical) | qualitative only at this reduced scale; published anchor $Rm_c = 30$ at $Pm = 1$ (Ponty et al. 2005, cited in these §3.4) |
| R3 3D generator | 9 | `train_fm3d` + `milady.eval` (Taylor–Green, conditioned on $(Re, Pm)$, vector potentials, exact $\mathbf{B}\to-\mathbf{B}$; test point $Re=50$, $Pm=2$) | divergence exact by construction; spectra and budgets at the held-out point within the plan's bars | these §3.4 tier-2 criteria: relative divergence $< 10^{-12}$; log-spectrum error $< 0.1$ decade per band; $Rm_c$ from the generator within 10% at a $Pm$ without data; label them "criteria of the PhD plan" |
| R4 Tier 1 at useful resolution | 9 | `palier1_mhd2d` today reuses the E2 dataset ($32^2$); the $128^2$, $8\times8$ $(\nu,\eta)$ plan is future | the E2 conclusions survive a field architecture and more seeds | these §3.3: energy residual $< 5\%$ at parameters without data; dissipation spread ratio in $[0.8, 1.2]$ |
| R5 VKS (SFEMaNS, LATU) | 10 | consortium data, not public | four dominant POD modes and the $(D, Q)$ distribution reproduced; Rice rate inside the Poisson interval of the simulated count | these §3.5 criteria (a)–(d) |
| R6 DRESDYN | 10 | SFEMaNS precession simulations | $Rm_c(Po)$ and the symmetry class of the dominant mode recovered at a $Po$ without data | these §3.6 criteria (a)–(b) |
| R7 Compute bill | 9 | catalog query (GPU hours per campaign) | the plan's $\approx 1.1\times10^4$ GPU hours (uncertainty factor 2) | these §3.7 |

---

## 2. Key ideas: picture first, then the aha, then the formula

Each card gives the level, the chapter, the intuition-first visual metaphor, the "aha" moment, the formula that arrives only after the picture, the misconception to defuse, the assets and data, and the callbacks. Existing site assets are listed so scene authors can copy their logic (the interactive widgets in `assets/interactif/*.js` already contain the exact formulas and data paths).

### K1. Magnetic field and compasses — L0, ch. 0–1

- **Picture first.** Iron filings around a bar magnet morph into vermillion field lines, then into "rivers of direction" filling space. A compass is a tiny boat that turns to follow the local river. Zoom out: Earth wrapped in the same pattern, roughly a giant bar magnet.
- **Aha.** Field lines never start or stop: they close on themselves. Draw an imaginary box anywhere: as many lines leave as enter.
- **Formula after the picture.** None at L0. The box picture is planted here and cashed in at L2 as $\nabla\cdot\mathbf{B} = 0$ ("no magnetic sources or sinks", p1 §3.3, p3 Prop. 1.2).
- **Misconception to defuse.** "There is a giant permanent magnet inside the Earth." The core is liquid iron and far too hot to stay magnetized **[external, source: Curie temperature of iron ≈ 770 °C vs core temperatures of thousands of degrees]**; the field must be continuously regenerated. That is the reason a dynamo is needed.
- **Assets.** New animation. Vermillion lines, a small compass glyph that becomes the recurring **polarity needle** (section 3).
- **Callbacks.** The box picture returns in K12 (divergence-free by construction); the needle returns in ch. 11.

### K2. Geomagnetic reversals and paleomagnetic stripes — L0, ch. 0–1

- **Picture first.** The seafloor as a **tape recorder**: at a mid-ocean ridge, fresh lava cools; tiny magnetic grains freeze the direction of the field like a photograph; the floor spreads away on both sides like two conveyor belts. The result is a **barcode**, symmetric about the ridge, in two shades of vermillion.
- **Aha.** The barcode is mirror-symmetric because both belts recorded the same history; its irregular stripe widths mean the flips are irregular.
- **Formula after the picture.** At L1, one line: stripe width = spreading speed × duration of the polarity interval. Nothing more.
- **Misconceptions to defuse.**
  - "Reversals are periodic, so we are *overdue*." No: they are irregular; the site says reversals happen "irregularly, on time scales of a hundred thousand to a million years" (p3 ch. 7, citing Rincon 2019). In the three-mode model, waiting times are Poissonian at long times (Gissinger 2012, report §2).
  - "The planet flips over" or "the poles move across the crust." The rocks stay put; the field direction flips.
  - Any statement about consequences for life or technology: out of scope, not in the sources.
- **Assets.** New animation **[external facts, source before use: seafloor magnetic stripes (Vine & Matthews 1963; Morley); date of the last full reversal, about 780,000 years ago]**. The barcode morphs into the time series $D(t)$ of the VKS figure panel b (`figures/vks/figure/out/vks-en.png`) and, later, into the Gissinger $D(t)$.
- **Callbacks.** The barcode becomes the **polarity strip** drawn under every $D(t)$ curve in the video (ch. 4, 5, 8).

### K3. The dynamo effect and the self-exciting disc — L1, ch. 1

- **Picture first.** A copper disc spinning in a magnet's field drives a current (Faraday disc, the ancestor of all dynamos, p3 exercise 2). Now remove the magnet and route the disc's own current through a coil around the axle: the coil makes the field that makes the current that feeds the coil **[external: self-exciting homopolar disc, Bullard 1955, source before use]**. Sound analogy: a microphone pointed at its own speaker. Whisper: nothing. Turn the gain past one: the squeal grows by itself.
- **Aha.** No magnet is needed. Motion, a conductor and the right geometry turn a vanishingly small seed field into a large one, exponentially, once the loop gain exceeds one. Then the field brakes the disc (the motor must work harder): growth saturates.
- **Formula after the picture.** At L1: $\dfrac{\mathrm{d}B}{\mathrm{d}t} = (\text{gain} - \text{loss})\,B \Rightarrow B \propto e^{\lambda t}$. At L2, the real thing, written as two coloured terms: $\partial_t\mathbf{B} = \underbrace{\nabla\times(\mathbf{u}\times\mathbf{B})}_{\text{stretch (blue acts on vermillion)}} + \underbrace{\eta\,\Delta\mathbf{B}}_{\text{smudge (grey)}}$.
- **Misconceptions to defuse.**
  - "A dynamo creates energy from nothing." No: mechanical power (motors, convection) is converted into magnetic energy and dissipated as heat; p3 ch. 5 has the loop diagram (flow → field by induction, field → flow by the Lorentz force, losses by viscosity and Joule heating). Reuse it.
  - "Any fast swirl will do." No: anti-dynamo theorems forbid some geometries (Cowling: axisymmetric fields; Zeldovich: planar flows, p3 §5.2). Plant this: it explains later why E2 (2D) is **not** a dynamo.
- **Assets.** p3 ch. 5 dynamo-loop SVG (redraw in palette).
- **Callbacks.** The squeal returns for every threshold: ABC windows (K6), Proposition 9 (K18), DRESDYN's narrow window (K7).

### K4. Magnetic Reynolds number and the threshold — L1 → L2, ch. 2

- **Picture first.** **Stretch versus smudge.** Vermillion threads embedded in a blue flow get stretched and folded like taffy (frozen flux, Alfvén; p3 §2.3: field strength grows with the stretching of material lines). Meanwhile a grey blur (diffusion) smudges them. Side by side: dye in honey (stretching wins, threads stay sharp) and dye in water (smudging wins).
- **Aha.** Whether the field grows is a race. One number says who wins: how fast the flow stretches compared with how fast the metal smudges. Plot the growth rate $\lambda$ against that number: it crosses zero at the **threshold**; above it, a seed grows.
- **Formula after the picture.** $Rm = UL/\eta$; growth rate $\lambda(Rm)$; threshold $Rm_c$ where $\lambda = 0$. Then the sodium reality (p3 Ex. 1.6): $\eta \approx 0.08\ \mathrm{m^2/s}$, so $U = 10$ m/s and $L = 0.2$ m give $Rm \approx 24$ but $Re \approx 3\times10^6$, because $Pm = \nu/\eta \approx 10^{-5}$: any laboratory dynamo is violently turbulent.
- **Misconception to defuse.** "$Rm$ values can be compared between experiments or papers." No: for the same VKS rotation the threshold reads $Rm_c \approx 31$, $\approx 44$ or $52$–$71$ depending on the definition (p3 Example 6.1). Show the same spinning impeller with three labels.
- **Assets.** E3 curve `experiences/figures/e3_abc-en.png`; widget data `assets/interactif/data/abc-dynamo.json`.
- **Callbacks.** "Stretch vs smudge" returns for $Pm$ (ch. 3) and for the kinematic eigenvalue problem (K5).

### K5. Kinematic versus dynamic dynamo — L2, ch. 2

- **Picture first.** Kinematic: the flow is a **conveyor belt that does not feel its cargo**; we impose $\mathbf{u}$ and ask whether $\mathbf{B}$ grows. On a log plot, $\|\mathbf{B}\|$ is a straight line (slope $\lambda$). Dynamic: the cargo pushes back; the Lorentz force brakes the belt; the straight line bends into a plateau.
- **Aha.** The *threshold* is a linear question (an eigenvalue); the *saturated* state, where reversals live, is nonlinear. E3 answers the first kind of question only.
- **Formula after the picture.** $\partial_t\mathbf{B} = \mathcal{L}_\eta\mathbf{B}$, $\mathbf{B} = e^{\lambda t}\hat{\mathbf{B}}$, $\sigma(Rm) = \max\operatorname{Re}\lambda$ (p3 Def. 5.1); dynamic case adds $\mathbf{j}\times\mathbf{B}$ to Navier–Stokes.
- **Misconception to defuse.** "E3 is a dynamo simulation with an AI in it." E3 contains no generative model; it is a kinematic test bench that validates the 3D solver and its divergence handling.
- **Assets.** E3 table and figure; `milady.sim.mhd3d` has both modes (calcul page).
- **Callbacks.** Kinematic eigenvalue reappears in DRESDYN (kinematic dynamo on averaged precession flows, Botez et al. 2026) and in R1.

### K6. ABC and Taylor–Green flows — L2, ch. 2 (ABC) and ch. 9 (Taylor–Green) **[R for Taylor–Green]**

- **Picture first.** ABC: a box tiled with identical "twisting rooms" where three crossed sinusoidal winds make every streamline a corkscrew (velocity parallel to its own curl: maximal helicity; partly chaotic streamlines, p2 §5.4). Taylor–Green: a lattice of counter-rotating eddies, like meshing gears; its counter-rotating cells are "reminiscent of the von Kármán flow" of VKS (p2 Remark 5.4: keep that cautious wording).
- **Aha.** Turning down diffusion does not always help. ABC is a dynamo for $8.9 < Rm < 17.5$, stops, then restarts above about 27: **windows**. E3 measures 8.87, 17.6 and 26.8. Taylor–Green shows a **subcritical** bifurcation (Ponty et al. 2007): the state can jump, with hysteresis; this is exactly where a smooth generator struggles (K18).
- **Formula after the picture.** $\mathbf{u} = (A\sin z + C\cos y,\ B\sin x + A\cos z,\ C\sin y + B\cos x)$, $\nabla\times\mathbf{u} = \mathbf{u}$. Elegant integrator check: $\mathbf{B} = \mathbf{u}$ is an exact eigenmode decaying at $-1/Rm$; measured $-0.5001$ at $Rm = 2$ (report §5 E3).
- **Misconception to defuse.** "Periodic boxes are the experiments." They are test benches with no walls; real devices are walled cylinders with materials (K7, ch. 10).
- **Assets.** `abc-dynamo.js` widget (curve plus eigenmode slice); E3 results. Taylor–Green and ABC at $64^3$: regenerable R1, R2.
- **Callbacks.** Windows echo the squeal threshold (K3); subcritical jump prepares K18.

### K7. VKS and DRESDYN — L1 → L2, ch. 3; DRESDYN again in ch. 10 **[R]**

- **Picture first.** VKS: a horizontal cylinder holding 150 liters of liquid sodium, two bladed impellers at the ends turning in opposite directions (up to 300 kW of motors). Blue: two counter-rotating cells plus a poloidal recirculation. Vermillion: an axial dipole that appears only above threshold, and **only with soft-iron impellers** (stainless steel: no dynamo). Make the impellers turn at different speeds: the dipole starts flipping (VKS figure panels a–c). DRESDYN: a cylinder spinning about its axis while that axis slowly turns (precession), no impeller at all.
- **Aha.** The "knob" is not one number. Materials and boundary conditions move the threshold as much as speed: in simulations, $Rm_c$ goes from $90\pm5$ to $130\pm10$ when the pseudo-vacuum condition is replaced by the vacuum condition (Nore et al. 2018). The green knob becomes a panel of knobs: $Re$, $Rm$, $\mu_r$, forcing asymmetry, Poincaré number $Po$.
- **Formula after the picture.** $\boldsymbol\lambda = (Re, Rm, \mu_r, \text{asymmetry})$; $Po$ = precession frequency / rotation frequency. Reversal numbers (Berhanu et al. 2007): at $F_1 = 16$ Hz, $F_2 = 22$ Hz, polarities last 120 s and 50 s on average, a reversal takes about 5 s, versus an ohmic time of about 0.4 s.
- **Misconceptions to defuse.** "DRESDYN already produces a dynamo." It is ongoing (ANR abstract). "Simulations reproduce VKS easily." The reversal simulations of Bousquet et al. (2026) needed a conducting outer medium; their data are not public.
- **Assets.** `figures/vks/figure/out/vks-en.png` (qualitative curves, say so on screen); p3 VKS diagram. DRESDYN: schematic only until R6.
- **Callbacks.** The panel of knobs becomes the conditioning input of the generator (K11); DRESDYN's narrow $Po$ window echoes the squeal threshold.

### K8. Chaos and the Gissinger three-mode model — L2, ch. 4

- **Picture first.** Three coupled dials: $D$ (dipole, vermillion), $Q$ (quadrupole, light vermillion), $V$ (a velocity mode, blue). In the $(Q, D)$ plane: below the threshold, **two whirlpools**, mirror images, each trapping its own trajectory forever; raise the green knob $\Gamma$ past about 0.86: the whirlpools touch through a narrow corridor, and the trajectory lingers in one, then slips to the other (a merging crisis, p4 §4.4). Then the butterfly: launch two trajectories $10^{-6}$ apart and watch them separate.
- **Aha.** Reversals need no randomness: three deterministic equations with the symmetry of $\mathbf{B}\to-\mathbf{B}$ already flip irregularly. And *when* is unknowable: errors grow by a factor $e$ every ~11 time units (Lyapunov exponent ≈ 0.09–0.1), while a polarity lasts more than 100 units on average (p4 §7.3). By the time the next flip comes, any prediction has dissolved.
- **Formula after the picture.** $\dot Q = \mu Q - VD$, $\dot D = -\nu D + VQ$, $\dot V = \Gamma - V + QD$; symmetry $(Q, D, V)\to(-Q, -D, V)$; here $\mu = 0.119$, $\nu = 0.1$; threshold between $\Gamma = 0.86$ and $0.865$ (E1 fine grid).
- **Misconceptions to defuse.** "Chaos means no structure." The statistics are perfectly reproducible (K9). "Three equations describe the Earth." The model is phenomenological: its coefficients are not derived from MHD (p3 §7.3); the DQVU model of Bousquet et al. (2026) is the derived cousin, built from VKS simulations.
- **Assets.** `gissinger.js` widget (RK4 in the browser, symmetry button, live Rice counter); p4 figure `prep/p4-systemes-dynamiques/figures/gissinger-en.png`. A scene can integrate the model live in Canvas.
- **Callbacks.** The two whirlpools are the visual source for the mirror (K13), the bridge $|D|\approx0$ for Rice (K10) and tilting (K15), and the threshold for Proposition 9 (K18).

### K9. Stationary distributions: why snapshots are enough for some questions — L2 → L3, ch. 4

- **Picture first.** A **long-exposure photograph** of the chaotic trajectory: the path is unpredictable, but the glow it leaves converges to the same shape for any starting point (two different trajectories paint the same glow). Then the **shoebox**: cut the film into frames, shuffle them, throw away the timestamps. The shoebox is a sample of the stationary distribution.
- **Aha.** For many questions (averages, energy budgets, how often something happens) the shoebox is enough; you do not need the film. Second aha: **a single snapshot does not know its own future**. Every state is a valid starting point of a solution, so a lone snapshot cannot "satisfy" or "violate" an evolution equation (report Remark 3.4, p8 Prop. 1.4). What the equations constrain is the shoebox as a whole: on average, energy in equals energy out.
- **Formula after the picture.** Time average = ensemble average (Birkhoff). Stationarity identities $\mathbb{E}_{\mu_\lambda}[\mathcal{L}_\lambda\varphi] = 0$ with $\mathcal{L}\varphi = F\cdot\nabla\varphi$ (+ the Itô term with noise); with $\varphi = E$: $\mathbb{E}[P - \varepsilon] = 0$ (Prop. 5). Show these in amber: they are crowd laws.
- **Misconceptions to defuse.** "A physical snapshot must have $\mathrm{d}E/\mathrm{d}t = 0$." No: $\mathrm{d}E/\mathrm{d}t$ fluctuates snapshot to snapshot; only its mean is zero. "Snapshots are enough for everything." No: not for *when*, and not for the distribution of waiting times between reversals, which needs the dynamics (these §2.5).
- **Assets.** p4 Gissinger widget (two mirror histograms below threshold, coinciding bimodal histograms above). Amber histogram panel.
- **Callbacks.** The shoebox is filled by the generator in ch. 6; the "crowd law" is the hinge of ch. 7 (K14).

### K10. Rice formula: crossing rates from still photographs — L3 → L4, ch. 5 (truth) and ch. 8 (generated)

- **Picture first.** The **toll counter without a clock**. You want to know how many cars cross a line per hour, but you only have one aerial photograph, with each car's speedometer readable. Count the cars inside a thin strip around the line, weight each by its speed, divide by the strip's width: that is the crossing rate. For the dipole: the strip is $|D| < h$, the speedometer is $\dot D$, and the physics gives the speedometer for free on each snapshot ($\dot D = -\nu D + VQ$).
- **Aha.** A timeless shoebox predicts a rate. The cold open's "how often" becomes computable without simulating time.
- **Formula after the picture.** $\nu_0 = \int |\dot u|\,p(0, \dot u)\,\mathrm{d}\dot u = \lim_{h\to0}\frac{1}{2h}\,\mathbb{E}_\mu\big[|\ell(F(\mathbf{x}))|\,\mathbf{1}_{|\ell(\mathbf{x})|<h}\big]$ (Prop. 8; Kac 1943, Rice 1944–45). Sanity check on screen: $D = \cos(\omega t + \phi)$ gives two crossings per period; Gaussian case $\nu_0 = \sigma'/(\pi\sigma)$. Estimator bias $O(h^2)$, variance $O(1/(Nh))$; E1 uses $h = 0.2$.
- **Truth check (ch. 5).** On the reference distribution, with no time order, Rice reproduces direct counting within 4% near the threshold and 6% above it (report §5 E1).
- **Misconceptions to defuse.** "Rice counts reversals." It counts all zero crossings, including excursions and chattering around zero. It needs the right-hand side $F$. It says nothing about waiting-time distributions. For deterministic chaos its density assumption is not guaranteed (hence the finite window).
- **Assets.** `gissinger.js` (live comparison of count vs Rice); `experiences/figures/e1_seuil-en.png` (left: rates vs $\Gamma$; right: bridge mass).
- **Callbacks.** Paid off in ch. 8 on generated samples (K18); in MHD, $\dot D = \ell(\nabla\times(\mathbf{u}\times\mathbf{B}) + \eta\Delta\mathbf{B})$ from a generated $(\mathbf{u},\mathbf{B})$ (ch. 10).

### K11. Generative models and flow matching — L3, ch. 6

- **Picture first.** A round violet cloud of noise. A **wind** blows through it and the particles drift, bend and land in the shape of the data (two symmetric blobs). The wind depends on time $t$ and on the green knob. Training: draw a straight string from a random noise point to a random data point; thousands of strings cross; at each place and moment, the network learns the **average direction** of the strings passing there. Straight strings, curved trajectories, never two particles at the same place at the same time.
- **Aha.** Training is plain regression: predict the average direction. No likelihood, no adversary. And turning the green knob reshapes the whole cloud: one model, a continuum of settings, including settings never simulated.
- **Formula after the picture.** $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\,\mathbf{x}_1$; $\mathcal{J}(v) = \mathbb{E}\|v(\mathbf{x}_t, t, \boldsymbol\lambda) - (\mathbf{x}_1 - \mathbf{x}_0)\|^2$; minimizer $v^\star = \mathbb{E}[\mathbf{x}_1 - \mathbf{x}_0 \mid \mathbf{x}_t, \boldsymbol\lambda]$; sample by integrating $\dot{\mathbf{z}} = v_\theta(\mathbf{z}, t, \boldsymbol\lambda)$ (Heun, 50 steps); $q_\theta(\cdot\mid\boldsymbol\lambda) = (\Phi_1^{\boldsymbol\lambda})_\#\mathcal{N}(0, I)$.
- **Misconceptions to defuse.**
  - "Flow time $t$ is physical time." **No**, and say it twice: $t\in[0,1]$ is the time of the generative transport; the generator makes snapshots, not trajectories. $v_\theta$ is not the fluid velocity $\mathbf{u}$ (violet vs blue).
  - "It copies training snapshots." It learns a distribution; a generated field has no "true" twin, so pointwise errors are meaningless; we compare distributions (K16).
- **Assets.** `flow-matching.js` widget (exact marginal field for two symmetric Gaussians, $\lambda$ slider, conditional strings vs marginal trajectories): the best template for this chapter.
- **Callbacks.** The violet swarm reappears whenever the model acts; its symmetric target prepares K13.

### K12. Hard constraints by construction: potentials, Leray projection, divergence-free — L2 → L3 (Props 1–3 at L4), ch. 7

- **Picture first.** A **hill map**: generate a landscape (stream function $\psi$, or magnetic potential $a$) instead of arrows, and let the flow walk along the contour lines. Water moving along contour lines can never pile up or leak, whatever the landscape: zero divergence for free. The second tool, **swirl minus slope**: any arrow field is a swirl part plus a slope part (Helmholtz); the Leray projection deletes the slope part. In Fourier space: for each wave, remove the component of its arrow along its own direction $\mathbf{k}$.
- **Aha (counterintuitive).** A model trained only on perfectly divergence-free data still produces fields with a relative divergence of 0.41 (E2, V0). Why: to land exactly in the subspace, the ideal wind must squeeze the off-subspace part at a rate $1/(1-t)$ that blows up at the end, and a bounded network cannot represent it (Prop. 2 (c)–(d); Remark 3.6). "Almost right" is not "exactly right". And the soft penalty is gamed: divergence only drops to 0.34 ($\mathbf{u}$) and 0.16 ($\mathbf{B}$), while the magnetic energy comes out 2.7 times too high (the normalized penalty can be lowered by inflating the swirl part: a hypothesis, label it so).
- **Formula after the picture.** $\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$, $\nabla\cdot\mathbf{u} = 0$; $\mathbf{B} = \nabla\times\mathbf{A}$, Coulomb gauge $\hat{\mathbf{A}}_\mathbf{k} = i\,\mathbf{k}\times\hat{\mathbf{B}}_\mathbf{k}/|\mathbf{k}|^2$; Leray $\hat{\mathbf{u}}_\mathbf{k}\mapsto(I - \mathbf{k}\mathbf{k}^\top/|\mathbf{k}|^2)\hat{\mathbf{u}}_\mathbf{k}$; Prop. 2: $v^\star = m(P\mathbf{x}, t) - (I-P)\mathbf{x}/(1-t)$. Results: final projection $5\times10^{-17}$, potentials $1.7\times10^{-17}$ (double-precision rounding), projected flow $2\times10^{-8}$ (single precision).
- **Misconceptions to defuse.** "Exactness costs quality." Potentials give the same distribution quality as the final projection (energy distance 2.58 vs 2.61) and halve the dimension in 2D. "A penalty is good enough." Not for a linear constraint for which exact tools are nearly free.
- **Assets.** `leray.js` widget; `experiences/figures/e2_mecanismes-en.png`; `e2_spectres-en.png` (free model's excess energy at most scales).
- **Callbacks.** The K1 box (lines in = lines out) returns as the reason potentials work; at L5 (ch. 10) the hill map meets walls (Remark 3.5; these Q1).

### K13. Symmetry $\mathbf{B}\to-\mathbf{B}$ and equivariance — L2 → L3, ch. 7 (Prop. 4 at L4)

- **Picture first.** **The mirror.** The equations do not know which polarity is "up": a field and its mirror image are equally lawful. Two ways to teach this to the machine. *Augmentation*: show the student each photo and its mirror image during training. *Equivariance*: build the machine around a mirror, so that whatever it draws, its mirror twin is exactly as likely ($v_{\text{sym}} = \tfrac12[v(\mathbf{x}) + S\,v(S\mathbf{x})]$).
- **Aha.** Below the threshold each training trajectory is stuck in one whirlpool, so finite data are lopsided (37.5% and 31.25% of $D>0$ at $\Gamma = 0.80$ and $0.86$). The plain model inherits the lopsidedness (asymmetry 0.18 at $\Gamma = 0.86$, still 0.085 at unseen 0.87 where the truth is symmetric). Augmentation fixes it only where it has data (0.02 at unseen 0.81, 0.025 at 0.85). The mirror-built model sits at the noise floor (0.004) at every $\Gamma$. Second aha: the energy-budget laws are blind to this: any mixture $p\,\mu_+ + (1-p)\,\mu_-$ satisfies them (Remark 3.7); the most lopsided model even has the smallest control residual.
- **Formula after the picture.** $v(g\mathbf{x}, t, \boldsymbol\lambda) = g\,v(\mathbf{x}, t, \boldsymbol\lambda)$ and $g_\#\gamma = \gamma$ ⟹ $g_\# q(\cdot\mid\boldsymbol\lambda) = q(\cdot\mid\boldsymbol\lambda)$ for **every** $\boldsymbol\lambda$ (Prop. 4); $S = \operatorname{diag}(-1, -1, 1)$; symmetrization never increases the population loss.
- **Misconceptions to defuse.** "More data or augmentation is as good as built-in symmetry." Not between parameter values. "A symmetric distribution means symmetric snapshots." No: each snapshot has a polarity; the symmetry is a crowd law (C3). Cost: equivariance doubles network evaluations.
- **Assets.** `experiences/figures/e1_symetrie_projection-en.png` (centre and right panels: $(Q,D)$ clouds at $\Gamma = 0.85$ for A and C); report Table 2.
- **Callbacks.** The mirror returns at L5 for VKS's $R_\pi$ (a joint state–parameter symmetry that also flips the sign of the forcing asymmetry, untested) and for data assimilation, where a mirror-respecting prior avoids biasing a bimodal $\pm\mathbf{B}$ posterior.

### K14. Distributional versus per-sample constraints; Corollary 6 and the variance collapse — L3 → L4, ch. 7

- **Picture first.** **The bank account.** Over the years, income equals spending on average; on any given day you gain or lose. Forcing every single day to balance exactly gives a fake ledger that no real account ever produces. Same with energy: injection = dissipation only on average. Visual: the amber histogram of $\mathrm{d}E/\mathrm{d}t$ breathing around zero; a hand forces every sample onto zero; the histogram collapses into a **spike**. The spike is the video's warning sign: "when you see a spike, someone forced a crowd law onto each individual".
- **Aha.** Per-sample enforcement of a stationary budget does not just add error: it produces a distribution that the truth gives zero probability to (singular), whatever the quality of the generator. Measured: in E1, projecting each sample onto $\mathrm{d}E/\mathrm{d}t = 0$ multiplies the energy distance to the truth by 9; in E2, rescaling each sample onto the budget shrinks the spread of dissipation to $8.6\times10^{-4}$ of the data's.
- **The right route, and its subtlety (L4).** Enforce the budget on the crowd, during training, including at knob values with no data at all. A trap: estimating "(mean)²" from one mini-batch secretly penalizes the variance too, i.e., sneaks the per-sample constraint back in. The fix: **two independent juries**, multiply the means of two half-batches. Results: in E2, energy distance at unseen $\eta$ from 2.58 to 0.70, energy errors from 26%/37% to 7%/6%, a control run with the same iterations gains nothing, an unenforced budget ($\langle a^2\rangle$) improves too, and the dissipation spread is not crushed (0.66 → 0.79 of the data's). In E1 the story is mixed (K-pitfalls): residuals halve on a good model but $\sigma(\mathrm{d}E/\mathrm{d}t)$ shrinks to 0.75 of the truth, and the loss fails on a deliberately biased model.
- **Formula after the picture.** Corollary 6: if $\mathcal{L}\varphi$ has no atom at 0 under $\mu$, any $\nu$ concentrated on $\{\mathcal{L}\varphi = 0\}$ is singular, $\mathrm{KL}(\nu\|\mu) = \infty$ and $W_1(\nu,\mu) \ge \mathbb{E}_\mu|\mathcal{L}\varphi|/L > 0$. Loss: $\mathcal{S}_\lambda(\theta) = \sum_k(\mathbb{E}_{q_\theta}[\mathcal{L}_\lambda\varphi_k]/s_k)^2$. Bias: $\mathbb{E}[\bar g^2] = (\mathbb{E}g)^2 + \mathrm{Var}(g)/n$, while $\mathbb{E}[\bar g_a\bar g_b] = (\mathbb{E}g)^2$.
- **Misconceptions to defuse.** "Physics-informed means enforcing the equation on every output." For statistics of an unsteady system that is a category error. "The identities are sufficient." They are necessary only: every invariant measure satisfies them, including a fixed point or an unstable orbit (Remark 3.11), so the data-fitting term must stay.
- **Assets.** `contrainte-loi.js` widget (true distribution, per-sample projection, exponential tilt); re-drawn taxonomy (C1–C4) in video palette; `e2_en_loi-en.png`; `e1_symetrie_projection-en.png` (left panel, log density of $\mathrm{d}E/\mathrm{d}t$).
- **Callbacks.** The spike reappears in the scoreboard; the "two juries" motif returns in L5 risks (variance of the loss in 3D).

### K15. Exponential tilting and effective sample size — L4, ch. 7

- **Picture first.** **Reweighting a poll.** A biased poll can be corrected by giving some respondents more weight; the least-distorting reweighting is exponential. Show samples as dots whose size is their weight. Then two failure scenes: (1) a group that never answered (the bridge $|D|\approx0$, or the right tail): no weight can conjure them; (2) one respondent swells until he carries the weight of 500: the "1000-person poll" is now a 2-person poll. A counter labelled **ESS** ticks down.
- **Aha.** Reweighting can only rearrange what the model already produced; it fails exactly where the model is poor, which is where you needed it. E2: mean ESS/N 0.29, with 0.99 at the easiest $\eta$ and 0.002 at the three largest test $\eta$ (about one effective sample in 500); the budget residual drops (0.47 → 0.19) but the distribution gets worse (energy distance 2.62 → 4.15). E1: tilting improved no distribution (at $\Gamma = 0.85$ one sample weighs 33 times the mean).
- **Formula after the picture.** $\nu^\star = e^{\boldsymbol\beta^\star\cdot\mathbf{g}}\,q/Z(\boldsymbol\beta^\star)$, $\boldsymbol\beta^\star = \arg\min \log Z(\boldsymbol\beta) - \boldsymbol\beta\cdot\mathbf{c}$ (I-projection, Csiszár 1975); Pythagorean identity for KL; $\mathrm{ESS} = 1/\sum_i w_i^2$; support of $\nu^\star$ = support of $q$.
- **Misconception to defuse.** "Post-hoc reweighting is a free fix." It needs held-out validation (tuned on half $a$, tested on half $b$) and fails with heavy-tailed constraint functions.
- **Assets.** `contrainte-loi.js` ("missing support" option); report Table 7 (per-$\eta$ ESS).
- **Callbacks.** "You cannot reweight your way to places you never visited" returns in the thesis risk matrix: tilting alone is not a fallback.

### K16. The noise floor — L3, ch. 6 (introduced) and ch. 8 (used)

- **Picture first.** Roll a fair die 1,000 times, twice. The two histograms differ. The distance between two honest samples of the same truth is the **floor**: a dashed grey line under every bar chart in the video. A model whose bar touches the floor is "as good as we can tell at this sample size".
- **Aha.** Never compare with zero; compare with the floor at equal sample size. And check how the floor was built: at E2's test values it compares overlapping samples and is optimistic; the honest floor (training values) is 0.030. With that lens, the models are still far from the data: spectrum errors 0.07–0.23 against 0.002–0.011 for data.
- **Formula after the picture.** Energy distance $\mathcal{E}(P,Q) = 2\mathbb{E}\|X-Y\| - \mathbb{E}\|X-X'\| - \mathbb{E}\|Y-Y'\|$ (zero iff $P = Q$); estimator bias $(\mathbb{E}\|X-X'\| + \mathbb{E}\|Y-Y'\|)/n$; asymmetry floor $\sqrt{2/\pi}\cdot\tfrac12/\sqrt n \approx 0.004$ for $n = 10^4$.
- **Misconceptions to defuse.** "Smaller number = better model" without a floor. "One metric is enough": per-sample rescaling *improved* the spectral energy distance in E2 (2.62 → 1.1) while its dissipation was degenerate; only $\sigma(\mathcal{D})/\sigma_{\mathrm{ref}}$ unmasked it. A noise-dominated metric (cross-helicity residual against correlated snapshots) ranks nothing.
- **Assets.** `experiences/figures/e1_variantes-en.png` (dashed floor lines already drawn).
- **Callbacks.** The dashed floor recurs in every results scene and in every regenerable chart frame.

### K17. The HPC pipeline — L3 (with L5 detail), ch. 9 **[R]**

- **Picture first.** A **labelled kitchen line**: a recipe card (YAML campaign) → many ovens at once (sweep: local processes, Docker containers or a Slurm job array) → jars with tamper-proof labels (MFF files following The Well's HDF5 convention, with UUID, code commit and SHA-256 checksum) → a ledger (PostgreSQL or SQLite catalog) → a tasting menu (dataset split) → the chef in training (flow matching on vector potentials) → the critic (evaluation) → back into the ledger. Grey boxes, with the green knob on the recipe card and violet only at the training station.
- **Aha.** Reproducibility is designed in: the same UUID sits in the file and in the catalog, so the simulation part of the catalog can be rebuilt from files alone, which is what makes an offline cluster usable.
- **Formula after the picture.** Cost ≈ Σ duration × GPUs × hourly price + storage + outbound data; a single-precision $(\mathbf{u},\mathbf{B})$ state is $6N^3\times4$ bytes (≈ 0.4 GB at $256^3$; measured peak ≈ 15× the state); plan budget ≈ $1.1\times10^4$ A100 GPU hours, uncertainty at least a factor 2.
- **Misconception to defuse.** "It already ran at scale." The pipeline was tested end to end **without a GPU** (68 automated tests; Slurm templates with a simulated scheduler). Not yet run: a GPU, a real Slurm cluster, Apptainer, a rented VM.
- **Assets.** `architecture.js` widget ("follow a campaign" walk-through); calcul Figures 1 and 2.
- **Callbacks.** Each regenerable chart frame (section 1.8) shows which pipeline stage will fill it.

### K18. Parametric conditioning and the jump at a threshold (Proposition 9) — L4, ch. 8

- **Picture first.** **A rubber sheet over a staircase.** The true distribution jumps at the threshold (a cliff); a generator that depends smoothly on the knob is an elastic sheet stretched over it, rounding the edge. Somewhere near the cliff, the sheet must be far from the truth.
- **Aha.** This is not a training failure, it is geometry: a smooth generator makes an error of at least about half the jump near a discontinuous transition. E1 shows the fingerprint: onset delayed by 0.005–0.01 in $\Gamma$ (0.00030 crossings per unit time predicted at 0.865 vs 0.00194 true), then overshoot (0.0050 vs 0.0034 at 0.88), and 42% cumulative Rice error near the threshold vs 14% far from it.
- **Formula after the picture.** $W_1(q_\lambda, q_{\lambda'}) \le K|\lambda-\lambda'|$, $K = L_\lambda(e^{L_x}-1)/L_x$; $\max_{\lambda_c\pm\delta} W_1(q_\lambda,\mu_\lambda) \ge (J_\delta - 2K\delta)/2$.
- **Misconception to defuse.** "More data will fix it." Only steeper models (large $K$), denser parameters near the threshold, or conditioning on the branch/state (hysteresis) can; these are thesis questions (Q3, Conjecture 2.38).
- **Assets.** `e1_seuil-en.png` (left panel is the payoff image of the whole video).
- **Callbacks.** Squeal threshold (K3), ABC windows (K6), Taylor–Green subcritical jump (R2), DRESDYN transitions in $Po$ (R6).

### K19 (organizing idea). "Enforce a constraint where it is true" — the taxonomy C1–C4 — L3, ch. 7

- **Picture first.** Two shelves. Left, "true for every single field" (single-card icon): zero divergence, linear boundary conditions (C1), stationary algebraic relations (C2). Right, "true only for the crowd" (stack-of-cards icon, amber): symmetry (C3), stationary budgets (C4). Each law is placed on its shelf, and each shelf has its tool: build it in or project (left); equivariance, crowd-level loss or reweighting (right).
- **Aha.** The single sentence that summarizes the report: *a constraint must be enforced where it is true.* Two classic category errors: handling C1 with a soft penalty (an exact tool exists and is nearly free), and enforcing C3/C4 on each sample (the spike).
- **Formula after the picture.** Definition 3.3 table (C1: $\mathbf{x}\in\ker A$; C2: $c(\mathbf{x})=0$; C3: $g_\#\mu = \mu$; C4: $\mathbb{E}_\mu[\mathcal{L}\varphi] = 0$). Prop. 3 (Jensen gap): a penalty on the end-of-path prediction is unbiased for linear constraints only.
- **Assets.** Re-drawn taxonomy (section 0.2); report Figure 2 (`figures/cadre/figure/out/cadre-en.png`) as the "full machine" recap at the end of ch. 7.

---

## 3. Recurring motifs, callbacks and "predict before you see"

### 3.1 Recurring visual motifs

| Motif | First appearance | Recurs in | What it carries |
|---|---|---|---|
| **Polarity needle** (small compass, top corner) | ch. 0 | every scene showing $D$; flips when $D$ changes sign | the question "which way, and how often?" |
| **Barcode / polarity strip** | ch. 0–1 (seafloor) | under every $D(t)$ plot (VKS, Gissinger, Rice) | irregular flips; the same object in rocks, tanks and equations |
| **Green knob** | ch. 2 ($Rm$) | ch. 3 (panel of knobs), ch. 4 ($\Gamma$), ch. 6 (conditioning), ch. 8 (rubber sheet), ch. 9 ($Re$, $Pm$) | the control parameter $\boldsymbol\lambda$ |
| **Stretch vs smudge threads** | ch. 2 | ch. 3 (sodium, $Pm$), ch. 9 (solver step) | the induction equation, $Rm$ |
| **Squeal / loop gain** | ch. 1 | ch. 2 (threshold, ABC windows), ch. 8 (Prop. 9), ch. 9 (Taylor–Green jump), ch. 10 (DRESDYN) | thresholds |
| **Two whirlpools and the corridor** | ch. 4 | ch. 5 (bridge), ch. 7 (mirror, tilting), ch. 8 (threshold) | bistability, symmetry, rare passages |
| **Shoebox of shuffled photographs** | ch. 4 | ch. 5 (Rice), ch. 6 (the generator fills the shoebox), ch. 11 | snapshots, stationary distribution |
| **Violet swarm** | ch. 6 | ch. 7, 8, 9 | the generative model at work |
| **Mirror** | ch. 7 | ch. 8, ch. 10 ($R_\pi$, assimilation) | $\mathbf{B}\to-\mathbf{B}$, equivariance |
| **Breathing amber histogram / the spike** | ch. 4 (histogram), ch. 7 (spike) | ch. 8, ch. 11 | crowd laws; the category error |
| **Dashed grey floor line** | ch. 6 | every results chart, every empty seat | honest comparison |
| **Altitude meter L0–L5** | ch. 0 | throughout, on the left edge | where the viewer is in the climb |
| **Staircase of tiers 0–4** | ch. 9 | ch. 10 | the thesis plan; empty seats on the upper steps |
| **Empty seat** (dashed chart frame with data tag) | ch. 9 | ch. 10, end card | regenerable results, pre-registered bets |

### 3.2 Callbacks (setup → payoff)

1. **"When vs how often"**: cold open (setup) → ch. 4 Lyapunov time vs polarity length (why *when* fails) → ch. 5 Rice on the truth → ch. 8 Rice on generated samples → ch. 11 closing line.
2. **The box with lines in = lines out** (K1) → potentials and Leray (K12) → bounded domains at L5.
3. **The squeal** (K3) → windows (K6) → rubber sheet (K18) → DRESDYN's narrow window.
4. **"A snapshot does not know its future"** (K9) → the bank account and the spike (K14).
5. **The shoebox** (K9) → filled by the violet swarm (K11) → reweighted photos and the poll that shrank to two people (K15).
6. **The mirror** (K13) → "the budget laws are blind to the mirror" (Remark 3.7) → bimodal posterior in assimilation (ch. 10).
7. **Anti-dynamo planted in ch. 1** → "E2 is 2D, so it is not a dynamo, and that is on purpose" (ch. 7–8).
8. **Rm has three definitions** (K4) → "a model conditioned on $Rm$ must fix its convention" (ch. 10).

### 3.3 "Predict before you see" questions

Format for each: the question appears on screen with a 3-second visual countdown and the line "pause and make your guess"; the narrator waits in silence (a `[long pause]` in the TTS text); the reveal follows with the data. Answers are taken from the site.

| # | Chapter / level | Question | Reveal |
|---|---|---|---|
| Q1 | ch. 1, L0 | "The laws of physics do not care whether the field points north or south. So which polarity should Earth prefer?" | Neither: both are equally lawful; which one you get is history. Sets up the mirror (K13). |
| Q2 | ch. 1, L1 | "Spin the self-exciting disc a little faster each time. Does the field grow a little each time, or does nothing happen until a certain speed?" | Nothing, then exponential growth past the threshold (loop gain > 1), then saturation. |
| Q3 | ch. 2, L2 | "In the ABC flow, we keep lowering the diffusion, so stretching wins more and more. Once the dynamo turns on, it stays on. Right?" | No: dynamo for $8.9 < Rm < 17.5$, off, then on again above about 27 (E3: 8.87, 17.6, 26.8). |
| Q4 | ch. 4, L2 | "We know the state of the three-mode model to six decimal places. Can we predict the date of the next reversal?" | No: errors grow by $e$ every ~11 time units; polarities last > 100. But *how often* is predictable from the cloud alone. |
| Q5 | ch. 7, L3 | "A generator trained only on perfectly divergence-free fields. Are its outputs divergence-free?" | No: relative divergence 0.41. A soft penalty only brings it to 0.34/0.16 and inflates the magnetic energy 2.7×. Potentials: $10^{-17}$. |
| Q6 | ch. 7, L3 | "Two students learn the mirror symmetry: one from mirrored copies of the training data, one with a mirror built into its brain. At a knob value neither has seen, who stays symmetric?" | Only the built-in mirror (asymmetry 0.004, at the floor); augmentation drifts to 0.02–0.025 between training values. |
| Q7 | ch. 7, L4 | "Energy in must equal energy out. Let's force every generated snapshot to balance exactly. Better or worse?" | Worse: the histogram collapses to a spike; energy distance ×9 (E1); dissipation spread down to $8.6\times10^{-4}$ (E2). |
| Q8 | ch. 8, L4 | "Near the reversal threshold, will the generator's predicted flip rate switch on early, late, or right on time?" | Late (by 0.005–0.01 in $\Gamma$), then it overshoots: a smooth model rounds the cliff (Prop. 9); 42% error there vs 14% far away. |

Optional L4 bonus for the tilting scene: "If the model never produced snapshots near $D = 0$, can reweighting fix the flip rate?" → No; ESS collapses; reweighting cannot create mass.

---

## 4. Pitfalls: what the video must not overstate

### 4.1 Status and provenance (say these on screen and in narration)

- **P1. Prospective work.** The report is written as if it concluded an internship that has **not** taken place. Its experiments are small, real and reproducible, run on a 4-core CPU without a GPU (E1 last run ≈ 56 min, E2 ≈ 67 min, E3 ≈ 23 min). Say it in ch. 3 and again at the scoreboard.
- **P2. No endorsement.** The site is "neither produced nor endorsed" by ENPC, LISN, Observatoire de la Côte d'Azur, the ANR or the supervisors. Nothing has been reviewed by S. Cheng, D. Lucor, C. Nore or Y. Ponty. The supervisors may be named factually as the supervisors listed in the public offer; never attribute an opinion, a quote or an endorsement to them, and do not use their photos, voices or institutional logos as if they backed the video.
- **P3. No MilaDy data.** No SFEMaNS, LATU or VKS simulation data were used. The VKS reversal data of Bousquet et al. (2026) are not public.
- **P4. No generative model of a dynamo exists in this work.** E1 is a 3-variable toy model; E2 is forced 2D MHD, which **cannot** be a dynamo (Zeldovich), with the field sustained by forcing; E3 is a kinematic dynamo with **no** generative model. Never say "we built an AI that generates dynamos" or "AI predicts Earth's reversals".

### 4.2 Physics facts

- **P5. External facts.** Paleomagnetic stripes, the date of the last reversal, the Curie temperature argument and the self-exciting (Bullard) disc are not in the site. Source each from a primary or textbook reference before use.
- **P6. Reversal timing.** Do not claim reversals are periodic, "overdue" or imminent; do not claim effects on life or technology. The site's wording: irregular, on time scales of a hundred thousand to a million years.
- **P7. $Rm$ definitions.** Never compare threshold values across experiments or papers without the definition (VKS: 31, ≈44, 52–71 for the same physics).
- **P8. Geodynamo parameters are out of reach** of any simulation ($Pm\sim10^{-6}$, Ekman $\sim10^{-15}$); the video must not suggest that the toy benches model the Earth's core.
- **P9. Gissinger model is phenomenological**; reversals there are deterministic chaos, a model of the mechanism, not of the Earth or of VKS in detail. Taylor–Green is only "reminiscent" of the von Kármán flow.

### 4.3 Results: quote with their caveats

- **P10. Seeds.** E1 has 2 seeds per variant (3 were planned), E2 has 1. Only differences by a factor ≥ 2 (E1) or ≥ 3 (E2) should be presented as findings. Do not rank V2/V3/V4 (V3's better test distance is not significant).
- **P11. Interpolation only.** All "unseen" parameter values lie between training values; nothing was tested in extrapolation.
- **P12. Models are weak.** Spectral errors 0.07–0.23 (log10) vs 0.002–0.011 for data; even the best E2 model (V5) has a spectrum error about six times the honest floor (0.0696 vs 0.0114). Energy distance in E2 remains far above the honest floor (0.030).
- **P13. The stationarity loss is not a clean win.** E2: strong gain at unseen $\eta$, mostly at large $\eta$ where the base model is worst; slight cost at some small training $\eta$; one scalar identity only. E1: residuals halved on a good model but energy distance barely moves (within seed spread) and $\sigma(\mathrm{d}E/\mathrm{d}t)$ shrinks to 0.75; on the biased model, one seed diverged and the other got worse. The loss is applied on an 8-step sampler and evaluated on 50 steps. Part of the E2 gain could be a global rescaling of the energy level (argued against, not ruled out).
- **P14. Tilting is a negative result** in both E1 and E2 (it improved no distribution). Present it as such.
- **P15. Rice numbers.** Quote "14% cumulative error for $\Gamma \ge 0.89$, up to 65% at a single value; 42% near the threshold; 4–6% on the reference distribution". Never "Rice predicts reversals within 14%" without the cumulative/pointwise distinction. Rice counts zero crossings (excursions included), needs $F$, gives no waiting-time distribution, and was tested only on a deterministic 3-variable system.
- **P16. "Machine precision"** for potentials is partly by construction: the divergence is measured with the same spectral operator. With finite-element data (SFEMaNS, where $\nabla\cdot\mathbf{B}$ is only weakly controlled), "zero divergence" must be redefined with the solver's operator.
- **P17. Per-sample rescaling improved the spectral energy distance** in E2 (2.62 → 1.1) despite degenerate dissipation: say it; it is a lesson about metrics, not a point to hide.
- **P18. Hypotheses labelled as hypotheses**: the penalty being "gamed" by inflating the solenoidal part (V1), the narrowing of $\mathrm{d}E/\mathrm{d}t$ by the stationarity loss in E1, the cause of tilting's E2 cross-helicity degradation.
- **P19. E3 precision.** The second threshold is resolved only to ~0.1 (sign of the rate at $Rm = 17.5$ unresolved), the third only to ~1 unit; the published maximum growth rate was not verified.
- **P20. No topology metrics** were computed, although the offer asks for them.

### 4.4 Theory and novelty claims

- **P21. "To our knowledge."** Every novelty claim (stationarity identities of a field PDE as distributional constraints of a parametric conditional generator; Corollary 6 stated and measured; Rice applied to a snapshot generator; no generative model of dynamo simulations found) must carry "to our knowledge, after a literature search closed on November 6, 2026". Absence cannot be proven. Most building blocks are published and must be credited (Echeverría; Ethier & Kurtz; Weak Generative Sampler; Csiszár; Lipman et al.; FunDiff; PCDM; Genuist et al.).
- **P22. Propositions are elementary**, several "probably known in other forms"; present them as clarifying statements, not breakthroughs. Proposition 4 is classical for equivariant flows.
- **P23. Necessary, not sufficient.** Stationarity identities do not identify the physical measure; physical-measure selection is guaranteed only under Axiom A assumptions (Young 2002).
- **P24. "Physics-constrained" does not mean "physically correct".** Only the enforced constraints hold; spectra, intermittency and topology can still be wrong.

### 4.5 Infrastructure and the future

- **P25. HPC not yet run at scale.** No GPU, no real Slurm, no Apptainer, no rented VM yet. Campaigns `palier2_*` keep 20–40 snapshots per simulation vs ~5000 planned; `palier1_mhd2d` reuses the $32^2$ E2 data. Present them as prepared, not executed.
- **P26. Regenerable beats must not invent numbers.** Pending variants state bets and criteria (labelled "criteria of the PhD plan"); result variants read values from files, and include wording for failure. No placeholder value may look like a result.
- **P27. The PhD plan is a proposal** (36 months, ≈ $10^4$ GPU hours ± factor 2, three papers, no acceptance promised); funding beyond the nominal end of MilaDy is undocumented. Do not present the thesis as accepted, funded or scheduled.

### 4.6 Language traps (do not say → say instead)

| Do not say | Say instead |
|---|---|
| "AI predicts the next reversal of Earth's field" | "on a three-variable toy model, the flip *rate* is predicted from generated snapshots, with these errors" |
| "the first AI dynamo" | "to our knowledge, no generative model of dynamo simulations has been published; this work prepares one" |
| "proves", "solves", "guarantees physics" | "states and tests on toy models"; "enforces exactly the constraints it targets" |
| "the supervisors / the project think" | nothing: no opinions are attributed |
| "simulated time" for the generator's $t$ | "the generator's transport time, not physical time" |
| "the model learned the dynamics" | "the model learned the distribution of snapshots" |
| "perfect", "machine precision" for E1/E2 overall | only for the divergence of exact mechanisms, with the operator caveat |

---

## 5. Questions to raise with the user (pedagogy-related)

1. Target runtime: is ≈ 60 minutes in 12 chapters right, or should the video be split into a series (e.g. L0–L2 public episode, L3–L5 specialist episode)?
2. May the video use facts not in the site (paleomagnetic stripes, the last reversal's date, the self-exciting disc), provided they are sourced?
3. Should supervisors be named on screen at all, or only "the project's supervisors" with names in the description?
4. Formula density at L4–L5: full propositions on screen, or statements only with a pointer to the site?
5. Narrator: confirm an original narrator voice for the script persona (the script is written not to imitate or be attributed to any real person).
