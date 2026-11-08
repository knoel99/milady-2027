# Symbol sheet and glossary (final)

Consistency editor, 2026-11-08. This sheet supersedes `plan/outline.md` §2 "Symbol sheet" (it keeps every rule
of that sheet and adds what the written scripts needed). It governs narration, subtitles, on-screen labels and
chips in every unit, and every formula layer for the symbols listed here. A symbol that appears only on one
formula layer and is defined there (for example `G`, `M` in X4.1, `K` in 09.3 or X6.0, `κ` in X2.2 or 10.8) is
local: it must not be promoted to a label, a chip or narration.

Writers and builders: lint a new script against §2 and §5 before review. The question numbers `Q1`-`Q30` are
defined in `question_register.json`; the devices and the running order in `continuity.md`.

## 1. Colour key and subtitle markup (unchanged)

| Markup | Colour (NIGHT / PAPER) | Means | Typical words |
|---|---|---|---|
| `{u}…{/}` | blue `#3987E5` / `#0072B2` | fluid velocity **u** | flow, swirl of the flow, velocity |
| `{b}…{/}` | vermillion `#EB6834` / `#D55E00` | magnetic field **B**, dipole, quadrupole, polarity | field, dipole, seed field |
| `{param}…{/}` | green `#1BAF7A` / `#009E73` | control parameter (knob) | Gamma, eta, Rm, Pm, knob, diffusivities |
| `{model}…{/}` | violet `#B49CF0` / `#6C4BA0` | generative model and its outputs | machine, generator, wind, model |
| `{metric}…{/}` | amber `#EDA100` / `#E69F00` | distribution-level metric or law | distribution distance, noise floor, crossing rate, how often, on average |

Grey `#6B7A8C` is infrastructure (factory, tags). Matter is grey. Polarity is a shade of vermillion, never a new
hue. Markup is stripped for TTS.

## 2. Symbols: one meaning each

| Symbol | Meaning | First on screen | Rule |
|---|---|---|---|
| **B**, `B` | magnetic field | 01.3 | vermillion; `\B` in TeX |
| **u**, `U` | fluid velocity | 03.1 | blue; never the generator's velocity |
| `D` | the dipole, everywhere | 02.6, 04.1 | never a dissipation (the report's `σ(D)` is written `σ(ε)`) |
| `Q` | the quadrupole | 04.1 | `Q1`-`Q30` on a question-card stub are question numbers (stub typography only) |
| `V` | the flow pattern of the three-mode model | 04.1 | blue |
| `Γ` | forcing knob of the three-mode model (green) | 04.1 | flips sign under the impeller swap `R_π` (X4.5) |
| `η` | magnetic diffusivity, the knob of the flat sheet (green) | 02.2 (`Rm = UL/η`), 03.1 chip | narrated "eta" only in 08.1, 08.5, X3.2, X3.4 (lexicon pin requested); elsewhere "magnetic diffusivity" or "diffusivities" |
| `Rm` | magnetic Reynolds number `UL/η` | 02.2 | `Rm_c` = its threshold (see §4 for plain strings) |
| `Re`, `Pm`, `Po` | Reynolds number, magnetic Prandtl number `ν/η`, Poincaré number (precession ratio) | 02.3, 10.9 | green |
| `λ` | a generic knob (green) | 06.4 | never a growth rate, never a Lyapunov exponent; name the specific knob when there is one |
| `s` | growth rate of the field (real part) | 01.3 | `s_q`: the late-fit growth rate (10.4, X1.3); never λ |
| `r_0` | rate of zero crossings of `D` | 05.2 (formula layer) | "crossing rate" on screen and in narration |
| `r` | reversal rate | 05.4 | |
| `a`, `±a` | the level of the Rice level bound | 05.4 | `r_a`: crossing rate of the level ±a. **Only meaning of italic `a`** (changed in this pass: the 2D magnetic potential is now `A`, the forcing-asymmetry knob of X2.4 has ticks `−`, `0`, `+`) |
| `h` | half-width of Rice's strip | 05.2 | `h = 0.2` in E1 |
| `A` | magnetic potential: the flat sheet's scalar potential (hill map of the field, `B = ∇⊥A`, 08.3, X3.2, X5.4, X5.6) and the 3D vector potential (bold, `B = ∇×A`, X2.1, X6.1, X6.3, 10.8) | 08.3 | exception: `A = B = C = 1` and "ABC flow" (03.3) name the flow's three coefficients |
| `ψ` | stream function, the flow's hill map | 08.3 | `ψ_D`, `ψ_Q`, `φ_V`, `φ_U` (X6.4) are the names of the four VKS POD modes, always subscripted |
| `ε` | dissipation of one snapshot | 10.3 | `σ(ε)`: its spread (X3.5) |
| `P` | injected power (E2 and 3D budgets, the report's notation) | 10.3 | `P(…)` with an event in parentheses is a probability (07.1, 07.3, 09.3) |
| `E` | energy; `E(k)` energy spectrum; `E_B` magnetic energy | 04.7, 10.7, 10.5 | `E1`, `E2`, `E3` are experiment names (labels) |
| `q`, `q*` | generated law, tilted law | 07.x, X3.1 | violet; never `ν*` |
| `μ_Γ`, `μ_±`, `μ_λ` | stationary laws | X2, X4a, X4b only | in the core: "the long-exposure glow (stationary distribution)" |
| `μ_r` | relative permeability | 10.8 (L5) | "iron (permeability)" in words below L5 |
| `t` | see §3 (declared double use) | | |
| `v_θ` | the generator's velocity ("the wind"), violet | 06.2 | never the fluid velocity |
| `S` | the mirror `B → −B`; on the three dials `S = diag(−1, −1, 1)` | 07.2 | |
| `R_π` | the impeller swap, joint mirror; on the three-mode model `(Q, D, V, Γ) → (Q, −D, −V, −Γ)` | X2.4 | always called "impeller swap" or "joint mirror", never just "the mirror" |
| `ℒ` (calligraphic) | generator of the dynamics | X2.5 | italic `L` is a length (`Rm = UL/η`); `Lip(·)` a Lipschitz constant (09.3, X4.4) |
| `F`, `F₁`, `F₂` | impeller rotation frequency (Hz), green | 02.6, X6.0, X6.4 | changed in this pass: the right-hand side of the equations is now `f` on the X2.5 and X6.6 formula layers, `f*` the reduced drift (X6.6); the X4.1 chip no longer says "needs F"; E1 variant F is always "model F" (09.4, X2.5) |
| `C1`-`C4` | the report's constraint classes | 08.6 (formal row only) | chapter ids are ch00-ch11 |
| `t · transport time` | — | — | see §3 |
| `n_traj`, `t_keep`, `t_burn` | configuration keys | X5.1, cards | monospace, code names only |

Letters used as names, not symbols: `jury a / jury b` (07.6), `half a / half b` (08.5, X3.2 formula layers),
`panels a, b, d` (08.7 chip), the PhD plan's criteria `(a)`-`(d)`, models A-F of E1, V0-V5 of E2, answer
options `A · …`, `B · …` on PREDICT cards.

## 3. Declared exception: the letter t

`t` has two meanings that never share a screen:

1. physical time inside physics formulas and plots (`∂B/∂t`, `dE/dt`, `e^{st}`, `ε(t)`, "t = 150", "kept window ·
   t 100-140"); time axes are labelled with the word "time" (02.6, 03.2, 04.x);
2. the generator's transport time `t ∈ [0, 1]`, always labelled "t · transport time" wherever it is on screen
   (06.2, 06.3, 08.4, X2.2, X2.3), and narrated as "the transport clock", never "time".

## 4. Notation in plain on-screen strings (request to the foundation engineer)

`Kit.markup` (labels, cards, seat text) renders `$…$` as KaTeX but has no subscript rule; `Kit.chip` and plot
labels print plain text, upper-cased for chips. Plain strings in the scripts therefore carry `Rm_c`, `r_a`, `μ_r`,
`R_π`, `ψ_D`, `φ_V`, `E_B`, `s_q`, `v_θ`, `R_V` (about 60 strings in 02.2, 10.5, 10.7, 10.9, X4.2, X4.4, X4.5,
X5.6, X6.0, X6.2, X6.4, X6.5, 06.2, 10.4, 10.8). Convention: in a plain string, `X_y` (one character after the
underscore) and `X_{…}` mean a subscript. **Request:** one subscript rule in `Kit.markup`, `Kit.upper` (applied
before upper-casing) and the plot text writer, so that `Rm_c` renders as Rm with a subscript c everywhere. Until
it exists, a builder that meets such a string in a chip or an axis label writes it as "threshold Rm" (as ch11 did)
rather than printing the underscore.

## 5. Glossary of narration terms (one term per meaning)

| Term in narration | Meaning | Planted in | Also on screen as / never say |
|---|---|---|---|
| the field | Earth's or the dynamo's magnetic field | 00.2 | never "the magnetic" alone |
| dipole, quadrupole | north-south part, four-pole part of the field | 02.4, 04.1 | `D`, `Q` |
| seed field, seed | the weak initial magnetic field | 01.3 | **"training seed"** for the random initialization of a network, at its first use in a chapter (08.5, 09.1, 11.1; changed in this pass) |
| threshold | the knob value where growth turns positive | 01.3 | `Rm_c`; "tipping point" is not used |
| growth rate | `s` | 01.3 | |
| the mirror | `B → −B`: the laws read the same with every field line reversed | 01.5 ("mirror twins") | "built-in mirror" = equivariance (07.2); the impeller swap is always qualified (X2.4, X4.5, X2.Q) |
| stretch / smudge, the race | induction against magnetic diffusion | 02.1, 02.2 | |
| magnetic diffusivity | `η` | 02.1 | "eta" in E2 scenes |
| Rm, Pm, Reynolds number | dimensionless numbers | 02.2, 02.3 | lexicon pins exist for Rm, Pm |
| kinematic, dynamic | field too weak to act on the flow / field brakes the flow | 03.2 | |
| the twisting box (rooms) | ABC flow in a periodic box | 03.3 | "the third step", E3 |
| windows | ranges of Rm where the ABC dynamo is on | 03.4 | |
| knob, panel of knobs | control parameter(s) | 02.2, 03.5 | green |
| dots | simulated settings; filled = trained, open = tested | 03.6, 06.4 | "between the dots" = interpolation |
| the study | the independent, prospective internship study (the report) | 03.7 | "the report" for the document; never "our study" |
| the PhD plan | the independent PhD proposal (`en/these`) | 05.4 | "PhD proposal" in 10.1 and X5.6 (its caveat chip); "thesis plan" is no longer used (X3.3 changed) |
| the study's three questions | promise cards 1-3 of 03.7 | 03.7 | narration says "questions", visuals say "promise cards"; never confuse with the question cards for the supervisors |
| the staircase, step | the PhD plan's ladder of test benches | 03.7 | narration: "step" (first step = three dials); screens: "tier k" with k = step − 1; "tier" is narrated only as part of a label read aloud (none left after this pass: X5.6 and 10.7 changed) |
| three dials | Gissinger's three-mode model, tier 0, E1 | 04.1 | "three numbers" on the staircase |
| whirlpools, corridor | the two attractor lobes and the bridge between them | 04.2 | `|D| < 0.25` on screen |
| crossing (tick), excursion, reversal | `D` crosses zero; crosses and comes back; goes from one polarity to the other | 04.3, 05.4 | "flip rate" is never used; "how often it flips, counted as crossings" in the closing |
| crossing rate | ticks per unit time | 04.3 | amber |
| the long exposure, the glow | the stationary distribution | 04.5 | `μ_Γ` only in X2, X4 |
| shoebox; snapshot (frame, photo) | shuffled snapshots without timestamps | 04.6 | "photo" only in 04.7-05.2 and the 05.1 analogy |
| law of the crowd, crowd law | a law true only on average over the distribution (stationarity identity) | 04.7 | "crowd" = the distribution |
| energy budget | energy in equals energy out, on average | 01.4, 04.7 | |
| toll counter | Rice's formula as an analogy | 05.1 | |
| Rice's formula, the strip | crossing rate from snapshots plus the equations | 05.2 | |
| machine / generator / generative model / network | the generative model; "network" for the neural net inside | 06.1 | "machine" up to L3, "generator" from 07.1; models A, B, C named on screen |
| the wind | the learned velocity field `v_θ` | 06.1 | |
| transport clock | `t ∈ [0, 1]` | 06.2 | never "time" |
| straight strings | the conditional flow-matching paths | 06.3 | |
| distribution distance | the score between two crowds | 06.5 | technical names (energy distance, Wasserstein W1) only on chips of 06.5 and X3.0 |
| noise floor | what a perfect model scores against data at equal sample size | 06.5 | amber dashed line |
| augmentation / equivariance (built-in mirror) | the two ways to teach the mirror | 07.2 | |
| the two shelves | "for every snapshot" (hard) and "for the crowd" (distributional) | 07.1 | never "hard / soft" in narration |
| the spike | a crowd law forced onto each snapshot | 07.5 | |
| crowd loss | the stationarity loss, imposed on the crowd during training | 07.6 (named there in this pass) | "two juries" = the unbiased two-half-batch estimator (07.6) |
| the flat sheet (of plasma) | periodic forced 2D MHD, E2, the second step | 08.1 | "not a dynamo" |
| the box test | zero divergence: lines in = lines out | 01.2, 08.2 | |
| hill map | stream function or magnetic potential in 2D; potentials in 3D | 08.3 | `ψ`, `A` |
| projection (swirl minus slope) | Leray projection | 08.3 | "both projections" is not narrated (09.6 changed) |
| penalty | a soft constraint in the loss | 08.2 | |
| reweighting (tilt), the poll | exponential tilting; effective sample size | 08.5, X3.1, X3.2 | "I-projection" only in X3.1 (lexicon pin requested) |
| control run | the same training without the loss | 08.5 | |
| the stiff sheet | a generator that varies smoothly with the knob | 09.3 | |
| the scoreboard, three lessons | recap of the eight mechanisms | 09.6 | |
| data factory: recipe card, ovens, jars, ledger, menu, chef, critic | the reproducible pipeline (YAML, simulations, MFF files, catalog, dataset, training, evaluation) | 10.2 | grey |
| bet, confidence, criterion, ask | the four parts of an empty seat | 10.1 (bet), X4.2 in the extended cut | "Bet one" = ABC at 64³ (10.4), "Bet two" = Taylor-Green (10.5) |
| empty frame (seat), grey tag, lamp | a pending result: dashed frame, the file it awaits, one lamp per criterion | 10.2, 10.7 | "lamp", not "light" (11.1 changed) |
| the partners, the consortium | MilaDy's partner laboratories and their solvers (SFEMaNS, LATU) | 10.9 | the narrator never says "your" or "our runs" (ch08.Q, ch10.Q changed) |
| question for the supervisors | a question card, `Q<n>` | ch00.Q | "A question to settle before we compute" (card kicker) |
| the map | the century map of dynamo hunting (planned M11) | chSOA1 (planned) | never use "the map" for the staircase in narration |
| "we" | the viewer and the narrator, or the study | 00.4 | no first-person anecdote; "our per-sample result" (Q31) means the study's |

## 6. Recurring numbers (one value, one spoken form)

| Quantity | Value (source) | Spoken | Scenes |
|---|---|---|---|
| Gissinger threshold | between 0.86 and 0.865 (R:871) | "zero point eight six" | 04.2, 04.3, 07.3, 09.2, 09.3 |
| crossing rate near and above it | 1.94 per 1,000 at 0.865; ≈ 11 at Γ = 1; 3.4 at 0.88 | "about two", "about eleven", "three point four" | 04.3, 09.2 |
| Lyapunov time, horizon, mean wait | ×e per ≈ 11; ≈ 150; ≈ 230; +1 decimal ≈ +25 | "nearly triples every eleven", "about a hundred and fifty", "over two hundred", "about twenty-five" | 04.4, 11.2 |
| Rice on true snapshots | 4 % near, 6 % above (R:883) | | 05.3 |
| Rice on generated snapshots (model C, seed 0) | 14 % far (cumulative), 17 % pointwise mean, 65 % at two settings, 42 % near (R:883) | | 09.1, 11.1, 11.2, X4.5 |
| plain model's lopsidedness | P(D > 0) = 0.43; 5 of 16 runs up at 0.86 | "about four in ten", "five of sixteen" | 07.1, 07.3 |
| spike | distance × 9 | "ninefold" | 07.5, 11.1 |
| crowd loss on E1 | unenforced residuals ÷ 1.98; spread 1.04 → 0.75 | "halves", "by a quarter" | 09.4, X4.5, Q9 |
| distance to the noise floor | E1 best ≈ 2×; E2 best ≈ 6× the honest floor | "about twice", "sixfold" | 09.5, 09.6 |
| E2 divergence | 0.41 free; 0.34 / 0.16 penalty; E_B × 2.7 | | 08.2, X2.2, 09.6, 11.1 |
| E2 crowd loss | distance 0.70 vs 2.52 (control), base 2.58; budget error 6 % vs 46 % (control) | "from two point five to zero point seven" | 08.5, 11.1, X3.5 |
| reweighting poll | 500 → 1 | | 08.5, X3.2, Q12 |
| E3 windows | measured 8.87, 17.6, 26.8; published 8.9, 17.5, ≈ 27; exact check −0.5001 at Rm 2 | "about nine", "seventeen and a half", "about twenty-seven" | 03.4, X1.1-X1.3, 10.4, 11.1 |
| configured campaigns | palier1: 11 η × 16 runs, 32²; ABC: 64³, Rm 4-40 integers, 2 seeds; TG: 12 runs, Re 25-200 × Pm 0.5-2, 64³, 40 snapshots per run, seed 10⁻³, kept t 100-140 | | 10.3-10.5, X5.3, Q3, Q6, Q24 |
| plan | 36 months, five steps (tiers), three axes, papers at months 10, 22, 33; ≈ 1.1 × 10⁴ GPU h incl. 20 % reserve; anchor ≈ 1150 GPU h; reference runs ≈ 2 × 10⁴ CPU h; 5,000 snapshots per 3D point | "about eleven thousand", "eleven hundred and fifty" | X5.5, X5.6, 10.7, Q6, Q27 |
| VKS | 150 L, 300 kW, 16 and 22 Hz, polarities 120 s and 50 s, flip ≈ 5 s; one threshold read 31 or 52-71; wall condition ≈ +40 % | | 02.5, 02.6, 03.5, X6.0, Q4, Q19 |
| factory | 68 tests; 0.08 s per 64³ step on CPU; ≈ 6 GB at 256³ (estimate) | "eight hundredths of a second" | 10.2, X5.1 |

## 7. Honesty badges

- Every claim-bearing scene carries exactly one badge; titles, checkpoints, recaps that add no claim and question
  cards carry none. Pending scenes carry `CONJECTURE` with a confidence.
- `MEASURED`: a number from E1-E3, from the pipeline's own tests (10.2, X5.1, X5.2: confirmed) or from the
  repository's results. `PROVED`: a statement proved on the site, in the report, the PhD plan or a prep module
  (01.4, 01.5, 03.1 cite P3 theorems; kept PROVED). `CONTEXT`: an external sourced fact. `PLANNED`: the PhD plan.
- `SCHEMATIC` (supported by `Kit.badge` for metaphors) is used only on 05.1 and 06.2, two metaphor or notation
  scenes that make no claim. It is not one of the five kinds of BRIEF §3.4: the lead keeps it or removes the
  badge on those two scenes.
- A note names the evidence on every `MEASURED`, `PROVED`, `PLANNED` and `CONJECTURE` badge (added in this pass
  to 00.4, 01.4, 01.5, 03.1, 03.4, 03.7, 04.2-04.4, 04.6, 04.7, 05.2-05.4, 06.3, 06.4, from their visuals).
  `CONTEXT` badges may omit it when a reference chip is on screen.
- 11.1 carries `MEASURED` for its left column; its right column shows `CONJECTURE` pills per bet.

## 8. Symbol and term changes made in this pass

| Where | Before | After |
|---|---|---|
| 08.3, X3.2, X5.4, X5.6 (labels, chips, formula layers) | potential `a`, `⟨a²⟩` | `A`, `⟨A²⟩` |
| X2.4 labels, X2.Q `why` | asymmetry ticks `−a`, `+a` | `−`, `+`; "negative / positive asymmetry" |
| X2.5, X6.6 formula layers | drift `F` | `f` |
| X4.1 chip | "needs F: the speedometer comes from the equations" | "needs the equations: they give the speedometer" |
| 09.4 label, X2.5 chip | "(F)", "variants D, F" | "(model F)", "models D, F" |
| 08.5, 09.1 narration | "One seed each", "one seed" | "One training seed each", "one training seed" |
| 07.6 narration | "this penalty vanishes…" | "this penalty, the crowd loss, vanishes…" |
| X3.3 narration | "The thesis plan's risk table" | "The PhD plan's risk table" |
| X5.6, 10.7 (result) narration | "five tiers", "the full tier" | "five steps", "the full campaign" |
| 11.1 narration | "Each light" | "Each lamp" |
| 09.6 narration | "hill maps and both projections" | "hill maps and projection" |
| ch08.Q, ch10.Q | "your solvers", "our … runs … yours" | "the partners' solver snapshots", "the Taylor–Green runs … published ones" |
