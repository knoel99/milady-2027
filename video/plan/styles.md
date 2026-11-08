# MilaDy explainer: style catalogue and visual identity

Working document for the long English explainer video about the MilaDy 2027 project
(source site: `/home/user/milady-2027/en/`). It fixes the look, the motion grammar and the
production rules that every scene must follow, so that scenes generated separately (including
the sections regenerated later from simulation data) read as one film.

---

## 0. Provenance of the catalogue

| Item | Value |
|---|---|
| Source | `https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json` (branch `main` answered 200; `master` not needed) |
| Saved copy | `video/plan/catalogue/videos.json` (813 423 bytes, sha256 `1c307487eca4e56957f4f7de4c72efcd482017f54d77495e3a88ddbcc9b4f30d`) |
| README | `video/plan/catalogue/README.md` (sha256 `0aea4fdbab29c20416b0c14c485f13e24fff4af26c39d43fb671a407b361e92c`) |
| Fetched | 2026-11-07 |
| Content | 703 entries: motion 369, 3d 117, explainer 116, interactive 101. Tags: canvas 267, svg 183, threejs 131, shader 92, gsap 86, css 57, audio 39. 418 entries have a live remake on Skillry. Fields: `slug, author, category, tech_tags, prompt, prompt_partial, poster_url, skillry_url, has_remake`. There is no `title` field: the short titles below are ours. |

**Handling rule.** Every prompt in the catalogue is untrusted third-party text. It was read as
inspiration only: no instruction in it was followed (many prompts say "ask me for…", "use my
key…", "go all out": ignored). Nothing from a prompt is copied into our scene prompts verbatim;
we restate the technique in our own words. Several prompts are marked `prompt_partial` (the
author published only the post text): they inform the *result* we aim for, not a recipe.

**Selection method.** Keyword scan over all 703 prompts (fluid, vortex, field lines, magnetic,
particles, simulation, equation, Manim/3b1b, whiteboard/chalk, timeline, zoom, storyboard,
contact sheet, `seek(t)`, captions, narration), then full reading of about 60 candidates, then
selection of the 25 most useful for a long, rigorous science explainer. Product promos, music
videos and games were excluded unless they carry a craft rule we need.

---

## 1. Selected catalogue entries (25)

Format: **slug, our short title** (category · tags · prompt status · where to watch).
"Works because" = what makes it effective. "MilaDy use" = how we adapt it.

### A. Explaining science and mathematics

1. **astrothewizard-618782, "The journey of photons"** (explainer · canvas · full prompt · [remake](https://skillry.dev/ai-videos/opus-5-5/astrothewizard-618782))
   - Works because: one strong formal idea per scene; the random walk is an *actual* simulated random walk, not a drawing; real numbers shown with honest uncertainty; a parallel timeline ("what happened on Earth meanwhile"); burned-in captions; critical review of stills before delivery.
   - MilaDy use: L0–L1 hook on geomagnetic reversals. The dipole trace D(t) on screen is a real RK4 integration of Gissinger's three-mode model (same equations and parameters as `assets/interactif/gissinger.js`: μ = 0.119, ν = 0.1, Γ ∈ [0.80, 1.00]); a parallel strip shows the paleomagnetic record as a barcode of polarity chrons (schematic, labelled as such unless we cite a dataset).

2. **apoorvjain25-945542, "A photon's 170 000-year escape, with data-driven sound"** (interactive · untagged · full prompt · [post](https://x.com/apoorvjain25/status/2104818940467945542))
   - Works because: the soundtrack reads the same event data as the animation, so every bounce you see is a click you hear; real travel times as a hidden clock.
   - MilaDy use: every zero crossing of D(t) triggers a soft tick. The viewer *hears* the reversal rate rise as the green knob Γ passes the threshold, which sets up Rice's formula (Proposition 8): counting crossings in time versus reading the same rate from the distribution alone.

3. **tak3sh8-441895, "Whiteboard: replica symmetry breaking in the SK model"** (explainer · canvas, audio · full but minimal prompt · [remake](https://skillry.dev/ai-videos/opus-5-5/tak3sh8-441895))
   - Works because: a hard statistical-physics concept fits a hand-drawn whiteboard register with narration; the drawing order *is* the argument.
   - MilaDy use: the PAPER register for derivations at L4–L5 (stationarity identity E[𝓛φ] = 0, Rice counting formula, Leray projector I − kkᵀ/|k|²), drawn on as the narrator speaks.

4. **eleanorina-653042, "3b1b-style explainer of Hoeffding's D"** (explainer · untagged · full but minimal prompt · [post](https://x.com/_eleanorina/status/2107841006909653042)). See also **linearuncle-971663** (Manim derivative lesson with examples first, [remake](https://skillry.dev/ai-videos/opus-5-5/linearuncle-971663)).
   - Works because: a dependence statistic explained with the 3b1b grammar (point clouds, pairwise geometry, terms built one at a time); examples come before the definition.
   - MilaDy use: the distribution-level metrics (energy distance between distributions of spectral descriptors, amber). Two clouds of points; pairwise distances drawn as faint lines; the three expectation terms of the energy distance appear one by one; the number 0.70 versus 2.52 (E2, digest) lands only after the viewer knows what it measures.

5. **gdgtify-393073, "There is no last prime" (kinetic proof)** (motion · untagged · full prompt · [post](https://x.com/Gdgtify/status/2107054188836393073))
   - Works because: the mechanism *performs* the proof instead of decorating narration; locked copy; a timecoded storyboard; an explicit "important logic" clause that forbids the common wrong claim; a disciplined type system (tabular mono for calculations, grotesque for declarations, technical serif for the conclusion).
   - MilaDy use: Proposition 4 (exact symmetry through equivariance) staged as a mechanism: the mirror gate S = diag(−1, −1, 1) acts on the sample cloud; a symmetric velocity field carries mirrored points to mirrored points, so both polarities stay equally likely at every Γ. We copy the "important logic" practice: each proposition shown on screen is quoted from the report with its scope (for example, invariance holds for every λ *given* an equivariant field and an invariant base distribution).

6. **gdgtify-130294, "Build the floor" (magnetic-field typography)** (explainer · untagged · full prompt · [post](https://x.com/Gdgtify/status/2105570411870130294)). See also **gdgtify-989608** ("Escape the orbit": abstract orbital metaphor that explicitly refuses to imply a physical simulation).
   - Works because: words respond to a field (streamlines, flux, a null point, one pole reversed so the field reorganizes); typography stays crisp while particles are only atmosphere; a banned list of clichés (horseshoe magnets, lightning, electron diagrams, sci-fi arcs).
   - MilaDy use: title and chapter cards. Key words ("dynamo", "reversal", "threshold", "constraint") sit in a vermillion field-line field that reorganizes when the dipole flips. From 989608 we keep the honesty rule: a metaphor is labelled SCHEMATIC and never carries invented numbers.

### B. Simulations, fluids, particles, data

7. **egeberkina-949521, "Earthquake in a tectonic sandbox"** (interactive · untagged · full prompt · [post](https://x.com/egeberkina/status/2105029713445949521))
   - Works because: it feels like watching someone explore a live simulation, not a slideshow; a live seismograph strip reacts to the physics; something new is revealed every few seconds; minimal typography with dynamic labels.
   - MilaDy use: the "dynamo sandbox" at L2–L3: the (Q, D) phase portrait of Gissinger's model with its fixed points, a scrolling magnetogram strip of D(t) under it, the green knob Γ turned live. The same layout returns for E3 (growth rate λ versus Rm) with the field energy strip.

8. **nathanwilbanks-981110, "GPU fire, rendered offline"** (explainer · threejs, shader, audio · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/nathanwilbanks-981110)). See also **pagustafsson-566609** (3D Navier–Stokes smoke in WebGL2) and **cagrimbakirci-842869** (every retina image computed, not drawn).
   - Works because: a real fluid solver drives the image; frames are rendered offline with scripted camera moves, not screen-recorded; a self-critique loop on rendered stills.
   - MilaDy use: L0–L1 "liquid metal in motion" shots (a stable-fluids shader for intuition only, labelled SCHEMATIC). Every scientific panel, by contrast, is *computed from our data*: 2D MHD maps from `experiences/resultats/e2_echantillons*.npz`, ABC modes from `e3_modes.npz`, later the campaign outputs.

9. **cyrilxbt-149036, "108 000 particles in one HTML file"** (explainer · canvas, physics · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/cyrilxbt-149036))
   - Works because: dense particle systems at 60 fps give matter a tangible feel.
   - MilaDy use: blue tracer particles advected by u; vermillion "iron filings" (short segments aligned with B); and above all the violet sample cloud of flow matching (tens of thousands of points transported from Gaussian noise to the data distribution).

10. **rneayan-417829, "Population as 8 144 marbles"** (explainer · untagged · full prompt · [post](https://x.com/rneayan/status/2103400657856417829))
    - Works because: real data physicalized at a stated scale (1 marble = 1 million people); sound synced to simulated collisions.
    - MilaDy use: "one sample versus the law": each generated sample drops as a marble into an amber histogram of a descriptor (magnetic energy, dissipation). It shows why per-sample rescaling onto the energy budget satisfies the budget exactly but collapses the variance of the dissipation to zero (E2, Corollary 6): the histogram turns into a spike.

11. **parkerrex-701462, "Token bucket rate limiter"** (explainer · canvas, physics · full prompt · [remake](https://skillry.dev/ai-videos/opus-5-5/parkerrex-701462))
    - Works because: a mechanism explained with nothing but canvas, with every frame a pure function of time so a renderer can screenshot any frame.
    - MilaDy use: the technical contract of every scene (§3.11), and the mechanism style for the compute pipeline (jobs flowing as tokens through Slurm queues).

### C. 3D scientific scenes, scale dives, cutaways

12. **kgonia7-746268, "From a hillside to the observable universe"** (explainer · threejs, shader, canvas, particles · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/kgonia7-746268))
    - Works because: one continuous scale change with no external assets.
    - MilaDy use: the opening dive, in reverse: a compass in a hand, Earth, the liquid outer core, convection columns, one grid cell of a simulation, its Fourier modes. The same dive closes the film by zooming back out.

13. **acoramaa-053577, "From a desk to one atom, with a scale ruler"** (explainer · threejs, shader · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/acoramaa-053577))
    - Works because: a ruler on the right edge tracks the scale during the whole shot.
    - MilaDy use: our "abstraction rail" (motif M8): a thin ruler on the right edge tracks the audience level L0 → L5 for the whole film, the way the ruler tracks metres to nanometres.

14. **konstantinsaifo-587629, "A fusion reactor you can take apart"** (explainer · threejs, shader · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/konstantinsaifo-587629))
    - Works because: drag one parameter and see a consequence at human scale.
    - MilaDy use: the VKS cylinder (tier 3) and the DRESDYN precessing cylinder (tier 4): turn the green rotation or precession knob and watch the vermillion field appear. Mechanical detail stays schematic unless the supervisors validate the geometry.

15. **aichrislee-408244, "Camera lens cutaway with an Explode button"** (explainer · threejs, shader, svg · full prompt · [remake](https://skillry.dev/ai-videos/opus-5-5/aichrislee-408244)). See also **0xspikez-483865** (turbofan stages, each labelled with one plain line).
    - Works because: a cutaway shows the hidden parts; an exploded view slides parts apart along one axis, each with a one-line label.
    - MilaDy use: the exploded view of the generative pipeline (noise, velocity network v_θ, the divergence-free decoder layer, the Leray projector, the sampler), and of the compute stack (YAML config, Slurm job, pseudo-spectral solver, MFF files, catalogue, training, evaluation). One plain line per part.

16. **voxyz-ai-345550, "Gravitational lensing lab"** (explainer · threejs, shader, canvas, gsap · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/voxyz-ai-345550))
    - Works because: a direct-manipulation physics lab, then three review rounds (two reviewers ranking P0/P1/P2 issues, a fixer, a final "does it ship" pass including a science-communication review).
    - MilaDy use: our QA loop per scene (§3.11): two reviewers (visual craft; scientific accuracy against the report), P0 issues must be fixed before the full render.

### D. Timelines and long-form structure

17. **niirajrshah-163739, "Life timeline, one scene per moment"** (3d · untagged · full prompt · [post](https://x.com/niirajrshah/status/2104551261270163739))
    - Works because: the year set large, the moment in one line; a contact sheet of stills checked for overlaps and spelling before the MP4 render.
    - MilaDy use: the history of dynamo science (Larmor's 1919 question "How could a rotating body such as the Sun become a magnet?", Cowling's anti-dynamo theorem, the Riga and Karlsruhe experiments, VKS, DRESDYN) and the project timeline (ANR-25-CE51-0077, started January 2026, 48 months). Dates must be checked against the site sources before scripting.

18. **dotey-927166, "Epic chronicle with HUD and chapter seals"** (explainer · untagged · full prompt · [post](https://x.com/dotey/status/2103964025683927166))
    - Works because: a persistent but minimal HUD (chapter number, a time ruler); chapter boundaries marked by one strong, consistent transition; beat grid and shot table fixed before rendering; maps drawn only as schematics.
    - MilaDy use: the chapter card (transition T4) and the staircase of tiers 0 → 4 that recurs at each chapter boundary.

19. **deedydas-407965, "Seven-minute SQLite repository explainer"** (explainer · untagged · full prompt · [post](https://x.com/deedydas/status/2104391577091407965))
    - Works because: a long-form structure for a technical system: what it is and why it matters, a map of the code, the life of one query, the core abstractions, a real execution trace.
    - MilaDy use: the infrastructure chapter as "the life of one simulation": from `infra/configs/palier1_mhd2d.yaml` to a Slurm job, the solver, MFF files, the catalogue, training (`milady.train.fm3d`) and evaluation.

20. **superalesha-970412, "A 6.5-minute short, 9 363 frames of canvas"** (motion · untagged · full prompt · [post](https://x.com/superalesha/status/2103052154931970412))
    - Works because: proof that code-drawn animation holds at length; scene-specific textures (torn paper, chalk on black, tissue paper) inside one coherent story; a recurring audio motif (a secret knock) that carries meaning.
    - MilaDy use: registers that change by chapter without breaking identity (§3.1), and a recurring two-note "flip" sound for every dipole reversal across the whole film.

### E. Craft rules and production discipline

21. **heyiamnick-119558, "One line, three inks"** (motion · canvas · full prompt · [remake](https://skillry.dev/ai-videos/opus-5-5/heyiamnick-119558))
    - Works because: one line is promoted through three inks (graphite on paper, wire on a blueprint, light on black) and never leaves the screen; every shot is built from the previous one; the same geometry is redrawn in whichever ink is current; locked camera; a ban list (glows, lens flares, camera shake, RGB split, crossfades, bouncy easing).
    - MilaDy use: our three registers PAPER → BLUEPRINT → NIGHT (§3.1) and the "ink change" transition T3: the induction equation written on paper becomes field lines in the night simulation.

22. **ik-builds-585923, "Marker notes that draw themselves on"** (motion · canvas, svg · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/ik-builds-585923))
    - Works because: hand-drawn notes drawn on with stroke-dashoffset; no invented results (no percentages, multipliers or names that are not in the source); every from-state set at t = 0 so any frame can be sought.
    - MilaDy use: the narrator's pen (motif M9): chalk circles, arrows and underbraces that point at the term or region being discussed.

23. **stokebuilder-356793, "35 to 50 animations for a podcast"** (explainer · canvas, svg · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/stokebuilder-356793))
    - Works because: a shared style bible and component kit written *first* so that every animation looks like the same show; copy verbatim or faithful, never invent facts or numbers; one judging pass for consistency, with only the egregious cues sent back.
    - MilaDy use: this document is the style bible; `scenes/_kit/` (to be built) is the component kit; every number on screen comes from `experiences/resultats/digest.md` or the JSON files.

24. **l3d1c-632524, "Launch ad built on the site's own CSS tokens"** (motion · svg · partial · [remake](https://skillry.dev/ai-videos/opus-5-5/l3d1c-632524))
    - Works because: the video imports the site's tokens and fonts; about 20 stills tiled into a contact sheet to review a whole cut before rendering; captions measured in the real font and shrunk to fit the safe zone; several cuts (16:9 and 9:16, different lengths) as different scene lists from one codebase.
    - MilaDy use: our palette derives from `assets/paper.css` and the widgets' dark palette; contact sheet per chapter; subtitles measured in Inter; the YouTube Short is a scene list, not a separate production.

25. **yankis0x-174321, "Every frame is a pure function of time"** (explainer · untagged · full prompt · [post](https://x.com/yankis0x/status/2103502194578174321)). See also **koushikde-937635** (seek(t), Playwright + ffmpeg, springs instead of linear, no fake HUD numbers).
    - Works because: `seek(t)` with no timers and no CSS transitions; springs as closed-form maths so any frame renders in any order; Playwright shoots sub-frames that ffmpeg blends into motion blur; one frame per beat is rendered and checked before the full render.
    - MilaDy use: our beat grid is the narration's word timings (from forced alignment), not a music BPM; sub-frame motion blur only for fast particle shots.

---

## 2. Design principles (one screen)

1. **Colour means a quantity, never decoration.** Matter (rock, liquid metal, glass, steel) is grey. Fields, parameters, models and statistics are coloured with the site key.
2. **Intuition before formulas.** Every symbol appears after the picture it names, with its name spoken.
3. **One idea per shot, one primary motion per transition.**
4. **Computed, not drawn.** Whenever a plot or field claims to be a result, it is generated from a data file and stamped with its source. Metaphors are stamped SCHEMATIC.
5. **Continuity over cuts.** Objects become the next scene; hard cuts only at paragraph boundaries.
6. **Restraint.** No glows, lens flares, camera shake, glitch, RGB split, bouncy easing or decorative particle bursts.

---

## 3. Visual identity

### 3.1 Registers: dark by default, paper for derivations, blueprint for infrastructure

| Register | Share of runtime | Used for | Background |
|---|---|---|---|
| **NIGHT** (default) | about 75 % | the hook, all simulations and fields, generative-model scenes, plots of results, 3D apparatus | `#0B0F14` (the site's dark-mode background) |
| **PAPER** | about 15 % | derivations and propositions (L4–L5), history and quotes, excerpts of the report and thesis, the site's own figures | `#F4F1EA` warm paper, page cards `#FFFFFF` |
| **BLUEPRINT** | about 10 % | the compute infrastructure: solver, MFF format, catalogue, Slurm/cloud, campaigns | `#0B0F14` with a cool-grey grid `#1A222D`, greys only plus data packets in key colours |

Why dark by default:
- Field lines, tracer particles and sample clouds read as light on dark: brightness can encode magnitude without fighting the background.
- The site's interactive diagrams already use a dark-tuned version of the colour key; all five key colours pass WCAG AA for text on `#0B0F14` (table in §3.2), so we inherit a tested palette.
- A 40–60 minute video is easier on the eyes on a dark ground, and dark frames suit phones (OLED) and the burned-in subtitle box.
- Viewers associate this look with mathematical explainers; it signals "we will think carefully" without words.

Why a light paper register at all:
- It marks a change of *mode*: "now we read the mathematics carefully", like opening the report.
- The site's figures (`figures/*/figure/out/*-en.png`, `experiences/figures/*-en.png`) are drawn on white and can be shown natively on a page card.
- It gives the eye a rest in a long film.

Rules: switch registers at most every 3–5 minutes, always through the ink-change transition T3 (never a hard cut from night to paper, which flashes). Dark gradients band under H.264: add 1–2 % animated grain or dithering on every NIGHT frame, master in 10-bit if possible.

### 3.2 Palette tokens

Semantic key (from the site; names are the CSS variable names to use in every scene):

| Role | Token | NIGHT value | contrast on `#0B0F14` | PAPER stroke | PAPER text | contrast on `#F4F1EA` (text) |
|---|---|---|---|---|---|---|
| Control parameter (Γ, η, Rm, rotation, precession) | `--param` | `#1BAF7A` | 6.8 | `#009E73` | `#007A5A` | 4.7 |
| Velocity u, vorticity ω, flow | `--u` | `#3987E5` | 5.3 | `#0072B2` | `#0072B2` | 4.6 |
| Magnetic field B, current j | `--b` | `#EB6834` | 6.0 | `#D55E00` | `#B34D00` | 4.7 |
| Generative model (v_θ, samples, "generated") | `--model` | `#B49CF0` | 8.2 | `#6C4BA0` | `#6C4BA0` | 5.9 |
| Distribution-level metrics (histograms, energy distance, Rice estimate) | `--metric` | `#EDA100` | 8.9 | `#E69F00` | `#8F6200` | 4.8 |
| Infrastructure (lines, boxes) | `--infra` | `#6B7A8C` (lines only) | 4.4 | `#6B7280` | `#4B5563` | 6.7 |

NIGHT values are the ones already used by the site's widgets (`assets/interactif/*.js`), so the video and the interactive diagrams match. The site's light values `#0072B2` (3.7) and `#6C4BA0` (2.9) are too dark for text on NIGHT and are not used there.

Neutrals:

```css
:root {                       /* NIGHT */
  --bg: #0B0F14;  --panel: #10151C;  --grid: #1A222D;
  --fg: #F2F4F7;  --fg-2: #C7D0DA;   --muted: #9AA6B2;
  --chalk: #E8E4D8;                  /* the narrator's pen */
  --matter: #7C8794;  --matter-dark: #3A3F47;   /* metal, rock, glass */
}
[data-register="paper"] {
  --bg: #F4F1EA;  --panel: #FFFFFF;  --grid: #E3DED2;
  --fg: #0A0A0A;  --fg-2: #1F2937;   --muted: #4B5563;
  --chalk: #1F2937;                  /* graphite pen on paper */
}
```

Encoding rules:
- At most three key colours in one shot. If u, B and the parameter are on screen, model and metric wait.
- **Provenance** is shown by line style and a chip, not by recolouring the physics: reference simulation = solid line in the field's colour with a white chip SIMULATED; generated = the same colour, dashed, with a violet chip GENERATED and a violet frame on maps; schematic = grey outline chip SCHEMATIC; laboratory measurements (VKS) = white ring chip MEASURED.
- Parameter axes are green; training values are filled dots, test values open dots (the site's convention); threshold zones and dynamo windows are green at 12 % opacity.
- Scalar field maps (ω, j, ψ, a): dark centre at 0, the family hue for positive values and a cold silver `#C9D3E0` for negative values, symmetric in lightness: flow maps go silver → `--bg` → `#6FB1FF`, magnetic maps silver → `--bg` → `#FF8A4C`. The hue tells *which* field, the lightness tells the value. (A conventional red–blue map would read as "magnetic versus flow"; if the supervisors prefer it, use it only in shots that show a single field.)
- Field direction textures: line-integral convolution or short aligned segments ("iron filings") in `--b` for B; tracer particles in `--u` for u.

### 3.3 Typography

All fonts are open-licensed (SIL OFL) and installed locally (checked with `fc-list`): Inter, Inter Display, JetBrains Mono. They are also on Google Fonts. Scenes **vendor the font files** (woff2 next to the HTML) and wait for `document.fonts.ready` before the first frame, so headless renders never fall back to another font.

| Role | Font | Size at 1920×1080 | Notes |
|---|---|---|---|
| Film and chapter titles | Inter Display ExtraBold | 96–128 px | tracking −1 %, sentence case |
| Scene headings (rare) | Inter Display SemiBold | 56–64 px | |
| Labels on diagrams | Inter Medium | 28–32 px | `font-feature-settings: "tnum"` for all numbers |
| Subtitles | Inter Medium | 42 px | §3.9 |
| Lower-third line 2 | Inter SemiBold | 28 px | |
| Small caps labels, chips, file names, YAML, code | JetBrains Mono Medium | 20–24 px | uppercase for chips, tracking +6 to +8 % |
| Mathematics | KaTeX fonts (KaTeX_Main, KaTeX_Math) | base 48–64 px in display | Computer Modern look = "this is the paper" |
| Historical quotes (optional) | Source Serif 4 Italic (Google Fonts, OFL) | 44–52 px | only on PAPER |

No handwriting font for mathematics. The hand-drawn feel comes from the pen strokes (motif M9), not from the glyphs.

### 3.4 Mathematics with KaTeX

- Library: KaTeX vendored locally. A copy is already on disk at `(dossier de travail d'une autre session)` (version 0.19.0): copy `dist/` into the kit rather than loading a CDN at render time.
- Options: `displayMode: true, output: "html", strict: "ignore", trust: ctx => ["\\htmlClass", "\\htmlId", "\\htmlData"].includes(ctx.command)`.
- **Every term is addressable**: the script's equations are written with `\htmlId{term-adv}{…}` and a role class, so a scene can light, colour, move or annotate one term.
- Kit macros (one source of truth, also used for subtitles' Unicode forms):

```js
const MACROS = {
  "\\U": "\\htmlClass{k-u}{\\mathbf{u}}",      "\\B": "\\htmlClass{k-b}{\\mathbf{B}}",
  "\\Rm": "\\htmlClass{k-param}{Rm}",           "\\etaP": "\\htmlClass{k-param}{\\eta}",
  "\\Gam": "\\htmlClass{k-param}{\\Gamma}",     "\\vth": "\\htmlClass{k-model}{v_\\theta}",
  "\\Edist": "\\htmlClass{k-metric}{\\mathcal{E}}"
};
/* .k-u{color:var(--u)} .k-b{color:var(--b)} .k-param{color:var(--param)} … */
```
  (Macros never redefine a built-in such as `\eta`, which would recurse: hence `\etaP`.)
- **Write-on**: a left-to-right `clip-path` wipe per term with a small chalk dot at the wipe edge, 350–600 ms per term. For two or three hero equations (induction equation, flow-matching loss, Rice's formula) a true stroke draw-on can be done with MathJax 3 SVG output and `stroke-dashoffset`; everywhere else KaTeX.
- **Equation morphs** (Manim's "transform matching terms"): render both states, match elements by `\htmlId`, interpolate positions (FLIP: measure bounding boxes in both states, animate transforms), fade unmatched terms. All of it computed inside `seek(t)`.

### 3.5 Recurring motifs

| # | Motif | Colour | First appears | Returns in |
|---|---|---|---|---|
| M1 | **The flip**: a dipole arrow / compass needle that reverses, with its two-note sound | `--b` | L0 hook (Earth's field has reversed many times) | E1 sign changes of D, Rice's formula, VKS reversals, final shot |
| M2 | **The knob**: a dial for the control parameter with a shaded threshold window | `--param` | L0 ("turn up the stirring") | Γ (E1), η (E2), Rm (E3), rotation and precession (VKS, DRESDYN) |
| M3 | **Two inks**: blue flow lines carry vermillion field lines; stretch, twist, fold | `--u`, `--b` | L1 | induction equation, ABC dynamo, 3D tiers |
| M4 | **The cloud**: violet samples transported from a Gaussian blob to the data | `--model` | L3 (what a generative model does) | every generative result, Proposition 4, the 3D model |
| M5 | **The shadow**: an amber histogram under a trajectory or a sample cloud ("one sample versus the law") | `--metric` | L2 (a coin, a die, then D(t)) | stationarity loss, per-sample rescaling, energy distance, Rice |
| M6 | **The projector**: a vector dropped onto a plane (the divergence-free subspace), and a ∇·B gauge reading ≈ 10⁻¹⁶ | `--infra` + field colour | L1 (∇·B = 0 as "no magnetic charges") | five mechanisms of E2, Leray projection, divergence-free decoders |
| M7 | **The staircase**: tiers 0 → 4 (three modes, 2D square, 3D periodic box, VKS cylinder, precessing cylinder) | greys + current tier lit | end of L1 (the plan) | every chapter card, the thesis plan, the conclusion |
| M8 | **The abstraction rail**: a faint ruler on the right edge, L0 → L5 | `--muted` | first frame | always on, brightens on level changes |
| M9 | **The pen**: chalk circles, arrows, underbraces drawn on as the narrator speaks | `--chalk` | L1 | every level |
| M10 | **The mirror**: the symmetry S = diag(−1, −1, 1), B → −B, as a reflecting plane | `--fg` | L2 (polarity is a symmetry) | Proposition 4, VKS symmetries and equivariance (thesis 2.4) |

### 3.6 Transitions

| Code | Transition | When | Duration |
|---|---|---|---|
| T1 | **Morph continuity**: an object of shot n becomes the frame of shot n+1 (the compass needle becomes the D axis; the 2D square tiles into a 3D periodic box; the box becomes a cylinder) | default inside a chapter | 1.2–2.5 s |
| T2 | **Scale dive**: continuous zoom across scales | moving between Earth, core, flow, grid, modes | 4–12 s |
| T3 | **Ink change**: the same geometry redrawn in the next register, with a wipe along a drawn line | NIGHT ↔ PAPER ↔ BLUEPRINT | 1.5–2.5 s |
| T4 | **Chapter card**: the staircase (M7) with the current tier lit, the rail (M8) climbs one notch, chapter title in a field-line field (entry 6) | chapter boundaries | 3–5 s |
| T5 | **Hard cut** on a still frame | only at a narration paragraph boundary (`[long pause]`), both sides at rest for at least 6 frames | 0 |
| T6 | **Equation morph** (matching terms) | rewriting an equation | 0.8–1.5 s |

Banned: crossfades between scenes (a dissolve is allowed only *inside* a simulation for time-lapse), glitch, RGB split, lens flares, light leaks, camera shake, whip pans, bouncy or elastic easing, decorative particle bursts, starfield wallpaper, horseshoe magnets, lightning bolts, fake telemetry numbers.

### 3.7 Pacing grammar

Narration rate: Fish Audio `drama-3` at `prosody.speed` 1.0 (the validated setting in the Videobook brainstorm). Measure words per minute on the first chapter and budget the script from it (expect roughly 140–160 wpm). Slowing down is done with an ffmpeg `atempo` filter in post-production, never with `speed` < 1.

Shot length by audience level:

| Level | Audience | Shot length | New visual idea every | Equations | Register |
|---|---|---|---|---|---|
| L0 | everyone | 4–8 s | 6–10 s | none | NIGHT, 3D |
| L1 | secondary school, first-year undergraduate | 5–10 s | 8–12 s | symbols only, one per minute at most, always named | NIGHT |
| L2 | undergraduate (fluids, MHD) | 6–12 s | 10–15 s | first full equations, at most 2 new ones per minute | NIGHT + first PAPER |
| L3 | master's (dynamical systems, probability, transport) | 8–15 s | 12–20 s | phase portraits, densities, short formulas | NIGHT |
| L4 | machine learning, generative models | 10–20 s | 15–25 s | losses, constraints, five mechanisms | NIGHT + PAPER |
| L5 | supervisors and specialists | 15–40 s holds | 20–40 s | propositions, identities, scope statements | PAPER + NIGHT results |

Rules at every level:
- Never more than 3 s of complete stillness: an idle layer keeps breathing (a 1.00 → 1.02 push over the shot, drifting tracers, a slow highlight walking along an equation).
- After every payoff, 1.0–1.5 s of breath with nothing new on screen. This is where the script's `[long pause]` falls.
- **Predict beats** (1 to 2 per chapter): a question on screen ("What happens if we turn the knob past 0.9?"), then 2.5–3.5 s of hold before the answer.
- **Recap beats**: 15–25 s at the end of each level, reusing the motifs only (no new information).
- Motion durations: micro (labels, chips) 150–250 ms; standard (term appears, small morph) 400–700 ms; macro (camera, scene morph) 1.2–2.5 s; camera rotations ≤ 15° per second. Easing: cubic in-out or critically damped springs in closed form; overshoot ≤ 3 % only for physical objects (needles, knobs).
- Sync: visual events are keyed to the narration's word onsets (forced alignment of the TTS audio against the script text), appearing 120–200 ms *before* the word.

**How an equation builds up, term by term** (the protocol every equation follows):
1. The picture first: the phenomenon is on screen and named in words.
2. Optional ghost skeleton: the whole equation at 15 % opacity, only when the viewer must see its shape before its parts.
3. Terms light up in *narrative* order, not left to right, each one when it is spoken, coloured by role (u blue, B vermillion, parameters green, v_θ violet, metrics amber, operators and constants in `--fg`).
4. As each term lights, a thin leader line connects it to the part of the picture it describes for about 1.5 s (for the induction equation: ∇×(u×B) to a field line being stretched; η∇²B to a field line fading).
5. Plain-word labels under braces appear 300 ms after the term ("stretching by the flow", "diffusion"); at most two labels on screen at once.
6. Hold the complete equation for at least 2 s plus 0.5 s per term.
7. Focus: terms not under discussion drop to 35 % opacity.
8. Transform with T6; never retype an equation from scratch.
9. One new symbol per sentence at most. The first time a symbol appears it gets a glossary chip (symbol, name, unit) that can be recalled later ("recall: η, magnetic diffusivity").
10. Every number has its unit, its uncertainty when it has one, and a source chip.

### 3.8 HUD, lower-thirds, chapter cards

- **Persistent HUD**: only the abstraction rail (M8): right edge, x = 1856 px, from y = 180 to 900 px, six ticks labelled L0…L5 in JetBrains Mono 16 px, at 25 % opacity, current level marked by a 4 px bar; it brightens to 80 % for 2 s when the level changes. No corner telemetry, no timecode.
- **Lower-thirds** (four kinds): chapter tag ("Level 2 · How a flow makes a field"); source chip ("DATA · E2 · experiences/resultats/e2_mhd2d.json"); reference chip ("Gissinger 2012"; "Kac 1943; Rice 1944–1945"); regenerable stamp (§3.10). Position: bottom-left, x = 96 px, baseline just above the subtitle zone (y ≈ 830–900 px), max width 760 px. Layout: 3 px vertical bar in the topic's key colour, line 1 JetBrains Mono 20 px uppercase in `--muted`, line 2 Inter SemiBold 28 px in `--fg`, on a panel `rgba(16,21,28,0.55)`. In: mask reveal left to right, 350 ms. Hold 4–6 s. Out: 250 ms fade. At most one lower-third at a time.
- **Chapter cards**: transition T4 with the chapter number in JetBrains Mono and the title in Inter Display ExtraBold, 3–5 s, one consistent soft impact sound.
- **People**: the narrator never appears and is not a real person. Supervisors and project partners are named in text only (lower-thirds, credits), without photos or logos unless the user provides cleared assets.

### 3.9 Subtitles (burned in)

Per the Videobook brainstorm: always burned in, dynamic but restrained, taken from the **script text** (not a transcription of the audio).

- Source and timing: cues are split from the script; timings come from forced alignment of the TTS audio against that same text. A cue starts 80 ms before its first word and ends 250 ms after its last word; minimum gap 80 ms; 1.2–6 s per cue; at most 2 lines of 42 characters; reading speed at most 17 characters per second (scientific content).
- Look: Inter Medium 42 px, line height 1.25, `#F2F4F7` on a box `rgba(11,15,20,0.78)`, padding 12 × 20 px, radius 8 px, centred, bottom margin 64 px, max width 1400 px. The same dark box on PAPER, for one consistent look.
- Motion: a cue enters with a 120 ms fade and a 4 px rise and leaves with a 100 ms fade. The word being spoken is at 100 % opacity, the others at 80 %: no colour change per word, no scaling, no bounce.
- Key terms: the first occurrence *in a chapter* of a key term ("velocity", "magnetic field", "control parameter", "generative model", "distribution") takes its key colour; at most one coloured word per cue.
- Mathematics: subtitles show a Unicode form written in the script (∇·B = 0, Rm ≈ 8.87), never LaTeX source. When an equation is being built on screen, subtitles show the spoken words.
- Safe zone: the bottom 180 px are reserved for subtitles; scenes keep important content above y = 880 px.
- Delivery: an `.ass` file generated from the cue JSON (styles above, word emphasis with `\t` alpha transitions), so the editing team (Grok Bot and Clip Editor in the brainstorm) can burn it with ffmpeg/libass or restyle it.

### 3.10 Regenerable sections: visual contract

Sections that depend on results not yet computed (HPC campaigns for tiers 1–2: `infra/configs/palier1_mhd2d.yaml`, `palier2_abc3d.yaml`, `palier2_tg3d.yaml`; 3D generative training `milady.train.fm3d` and its evaluation; SFEMaNS/VKS data; DRESDYN) follow one contract:

- A regenerable scene is a **template** (HTML) plus **data** (JSON and binary arrays converted to Float32) plus a **cue sheet** (word timings). Rendering is deterministic from (template version, data hash, cue sheet).
- No number is typed into scene code. Every value on screen is read from the data file; the template fails loudly (the QA catches it) if a required field is missing.
- Each regenerable shot carries a stamp lower-third filled from the data's metadata: `SIMULATED · palier2_abc3d · 64³ · run <id> · <date>` or `GENERATED · fm3d · checkpoint <id>`.
- **Preview mode** for animatics before the data exist: same layout, axes and frames, data areas filled with 45° grey hatching at 12 % opacity and a mono label `AWAITING · palier1_mhd2d campaign`. Never in the final cut.
- **Fallback**: each regenerable section also has a schematic variant (chip SCHEMATIC, no numbers) in case results are late, so the film can ship without waiting.

### 3.11 Scene technical contract (style-relevant parts)

- One self-contained HTML file per scene, 1920 × 1080 CSS pixels, exposing `window.DURATION`, `window.seek(t)` (pure function of time) and `window.READY` (true once fonts are loaded, KaTeX is rendered and data are parsed).
- No timers, no CSS transitions, no `requestAnimationFrame` state; randomness from a seeded generator (for example mulberry32 with a seed per scene). GSAP is allowed only as paused timelines driven by `timeline.seek(t)`; Three.js and KaTeX vendored at pinned versions.
- 3D look: matte materials, unlit fat lines (Three.js `Line2`) 2–4 px for field lines, long-lens perspective (field of view 25–35°) or orthographic, no glossy chrome.
- Plots: axes `--muted` 2 px, tick labels Inter 22 px with tabular numbers, axis titles with symbol and word ("Rm, magnetic Reynolds number"), curves drawn on left to right with the narration, uncertainty always shown.
- Record with headless Chromium (Playwright; `/usr/bin/google-chrome` and `/usr/bin/ffmpeg` are present on this machine) at 60 fps; motion blur (2–4 sub-frames blended with ffmpeg `tmix`) only for fast particle shots.
- QA per scene: a contact sheet (one still per cue plus every transition) checked for overlaps, spelling, colour-key violations and the subtitle safe zone; then two review passes (visual craft; scientific accuracy against the report), P0 issues fixed before the full render (entry 16).

### 3.12 Short vertical version (9:16)

The brainstorm plans a YouTube Short derived from the long version. The Short is a scene list over the same scenes; hero scenes accept `?aspect=9x16` and re-lay out (no crop of 16:9 frames for equations). Subtitles 56 px, centred at 62 % of the height to clear the platform's buttons; the abstraction rail is hidden.

### 3.13 Sound identity (brief)

Narration first. Music, if any, is a quiet bed under L0–L2 and absent or nearly so under L4–L5. Sound motifs: the two-note flip for every reversal (M1), soft detent ticks when the knob turns (M2), a granular hiss when the sample cloud moves (M4), zero-crossing ticks for Rice's formula (entry 2). Loudness target for delivery around −14 LUFS integrated, true peak −1 dBTP, music ducked by about 12 dB under the voice.

---

## 4. Open questions for the user (style)

1. **Narrator voice.** The request names a real public figure's voice. We will not clone or imitate a real person's voice. Which original Fish Audio narrator voice (`reference_id`) should we use, or may we choose a warm, curious English narrator from the library and send two test clips?
2. Is the dark-dominant look with paper derivations acceptable, or do you prefer a light-dominant film closer to the site's default light theme?
3. Field maps: the proposed key-coloured maps (silver for negative values) or a conventional red–blue map limited to single-field shots?
4. Logos (ANR, LISN, Lagrange, CEREA, ENPC) and photos of the supervisors: allowed, with which files? Default: names in text only.
5. Music: none, or a quiet score synthesized in code?
6. Frame rate: 60 fps everywhere (smoother, about twice the render time) or 30 fps for the long L4–L5 stretches?
7. Target total length (this changes shot lengths at L4–L5 and the number of predict and recap beats).
