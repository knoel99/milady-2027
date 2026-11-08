# State of the art: brief for chSOA1 and chSOA2

Prepared 2026-11-08 for the script writers and scene builders of the two state-of-the-art units (`BRIEF.md` §10).
It gives the facts, dates and citations to use, the visual map both units share, and a scene-by-scene plan.
The French companion for the author is `video/ETAT-DE-L-ART.md`; its §6 holds the full reference list, and every
pin below repeats the citation it needs.

## 0. Rules for these two units

- **Sources.** Every pin, number and claim below carries a source. Marks: `[site f:l]` = fact already verified in
  the repository (paths relative to `/home/user/milady-2027`; `R` = `en/rapport/index.qmd`, `T` =
  `en/these/index.qmd`, `E` = `en/encadrants/index.qmd`, `S` = `specs/sources/encadrants.md`, `Dy` =
  `specs/sources/dynamo.md`, `L` = `specs/sources/litterature.md`, `P3` = `en/prep/p3-mhd-dynamo/index.qmd`);
  `[ABS]` = publisher or arXiv abstract read 2026-11-08; `[FT: X]` = full text of X read 2026-11-08; `[via X]` =
  known only through review X (read in full); `[NEG]` = negative claim ("not found"), which cannot be proved and
  must be said as "we found no…". All DOIs and arXiv ids below were resolved in Crossref or the arXiv API on
  2026-11-08. Scene `sources` entries for external facts use the form
  `external: <Authors year>, <venue>, doi:<…> (checked 2026-11-08)` (BRIEF D7).
- **Badges** (BRIEF §3.4). External history and literature: `CONTEXT`. The thesis and its gaps: `PLANNED`.
  Callbacks to E1-E3 numbers: `MEASURED`. Propositions of the note: `PROVED`.
- **Names** (BRIEF D6). Supervisors are named in text only (pin labels, lower-thirds), no photos, no logos, no
  opinions or intentions attributed. A pin says what a paper *showed*, nothing else.
- **No "first" unless a source says "first".** The pins below flag the ones that may say it.
- **Spoken names.** Prefer names on screen and plain descriptions in the narration ("a British physicist, in
  1919"). Names already pinned in `audio/lexicon.json`: Brunhes, Matuyama, Zeldovich, Gissinger, Kármán, VKS,
  DRESDYN, SFEMaNS, LATU, MilaDy, TorchDA, Rice, Reynolds, Rm, Pm, MHD, ABC. Any other spoken name (Larmor,
  Cowling, Rikitake, Glatzmaier, Nore, Ponty, Lucor, Cheng…) needs a lexicon entry first; acronyms such as DQVU,
  PBFM, PCDM, FNO, PINN stay on screen only.
- **Do not show** anything listed in §6 (unverified or discrepant items) without a new check.
- **French narration** (BRIEF §9): the map labels stay in English; `text_fr` follows the same beats. French terms
  for the lanes: "théorie", "dynamos de laboratoire", "simulations", "modèles réduits", "inversions du champ
  terrestre", "substituts neuronaux", "modèles génératifs de champs", "contraintes physiques" (dures, souples, en
  loi, symétries), "a priori génératifs en assimilation".

## 1. The shared visual map

One canvas, built in chSOA1 and reopened in chSOA2 (motif: "the map", a new recurring device; it should get an
id in `styles.md` §3.5 from the consistency editor).

- **Register.** NIGHT for both units. ch02, ch03, ch09 and ch10 are NIGHT; a PAPER history map would force two
  register switches 2.5 minutes apart, against `styles.md` §3.1 ("at most every 3-5 minutes"). Draw the map in
  chalk ink (`--chalk`, `--fg-2`) on `--bg`.
- **Time axis.** Horizontal, piecewise linear so that the dense recent decades get room: 1900-1990 over the left
  55 % of the drawable width, 1990-2026 over the next 40 %, a short dashed stub 2026-2031 for planned work. A
  vertical "now" hairline at November 2026, label "NOW · NOV 2026". Decade ticks only; years appear on pins.
- **Lanes, top to bottom** (lane labels in the left gutter, Inter SemiBold ≥ 28 px):
  1. `EARTH'S RECORD` (statistics of reversals),
  2. `THEORY`,
  3. `LAB DYNAMOS`,
  4. `SIMULATIONS`,
  5. `REDUCED MODELS`,
  6. `DATA-DRIVEN` (thin, dashed, appears only from 2016; it is the lane chSOA2 opens).
  Lanes are neutral (`--grid` separators, `--muted` labels). In chSOA2 lane 6 unfolds into four sub-lanes:
  `SURROGATES`, `GENERATIVE MODELS`, `CONSTRAINTS` (with four thin strands `HARD` · `SOFT` · `DISTRIBUTIONAL` ·
  `SYMMETRY`), `ASSIMILATION PRIORS`.
- **Pin glyphs** (one meaning each):
  - filled dot = community landmark;
  - **ring with a name label** = a supervisor's own paper (label like `C. NORE · 1997`, JetBrains Mono, uppercase);
  - diamond = MilaDy-funded output (only Bousquet et al. 2026 and Botez et al. 2026 qualify, `[site S:28-33]`);
  - `×` = a no-go theorem or a negative result (Cowling 1933, Zel'dovich 1957, Gwirtz et al. 2022);
  - dashed ring = planned or not yet achieved (DRESDYN precession dynamo; the thesis);
  - colour follows the key only: generative-model pins violet (`--model`); a pin about reversals carries a small
    vermillion flip glyph (`--b`); a pin about a knob or threshold a green tick (`--param`); everything else
    chalk. Polarity is a shade of vermillion, never a new hue (outline §2).
- **MilaDy marker.** A bracket spanning lanes 3-5 at 2026, label `MILADY · ANR · 2026-2029` (ANR: start January
  2026, 48 months, `[site S:28-33]`, ANR page). The thesis marker is a dashed violet ring at 2027-2030 on the
  intersection of `GENERATIVE MODELS` × `CONSTRAINTS` × lanes 3-5, badge `PLANNED`.
- **Legibility** (BRIEF §8, `styles.md` §3.8). Text ≥ 28 px; at most about eight labelled pins visible at once;
  when a lane fills, earlier pins shrink to unlabelled dots keeping their year. One reference lower-third at a
  time, for the pin being narrated (kind `reference`, e.g. `Reference` / `Monchaux et al. 2007 · PRL`).
- **Arrows** (thin, `--muted`): Roberts 1972 → Karlsruhe 1999; Ponomarenko 1973 → Riga 1999; Taylor–Green
  1937 → Nore et al. 1997; VKS 2007 → SFEMaNS 2016; Gissinger 2012 → E1 (callback in chSOA2); SINDy 2016 →
  DQVU 2026. They show that the tracks feed each other.

## 2. chSOA1 "A century of dynamo hunting" (L1 → L2, ≈ 150 s, after ch02, before ch03, both cuts)

- **Learning goal.** See the five tracks the community followed for a century, where the three sodium dynamos
  of ch02 sit among them, and where MilaDy stands in 2026.
- **Takeaway (one sentence).** For a hundred years, theory, laboratory tanks, computer simulations and
  few-dial models have chased the dynamo together; MilaDy starts where the tanks, the simulations and the
  few-dial models meet.
- **Level rail.** Enters at L1 (ch02 is L1), reaches L2 by SOA1.4; ch03 opens at L2.
- **Word budget.** About 128 effective words per minute (BRIEF D21): ≈ 2.1 words per second of `target_s`,
  ≈ 315 words in all.

| Scene | target_s | Lane(s) | Beats (facts to say) | Pins drawn (label · source) | Badge |
|---|---|---|---|---|---|
| SOA1.1 The empty map | 18 | 1 | Chapter card. The time axis draws itself. The Earth kept a record long before anyone explained it: lavas magnetized backwards (1906); stripes on the seafloor (1963, callback to 00.3); the flips look like random events whose rate changes over geological time (Cox 1968, as summarized by Constable). | `1906 · reversed lavas` (Brunhes); `1963 · seafloor stripes` (Vine & Matthews); `1968 · random flips` (Cox) | CONTEXT |
| SOA1.2 Can a fluid make a magnet? | 32 | 2 | 1919: the idea that moving conducting fluid could sustain the Sun's field. 1933: a no-go result, no axisymmetric dynamo. 1958: the first rigorous working fluid dynamos. 1966: the mean-field α effect. 1972-1973: simple flows proved to be dynamos, which later became the blueprints of the Riga and Karlsruhe tanks. Then the hard part: liquid metals have a tiny Pm (callback to 02.3); simulations between 2005 and 2023 showed that dynamos can still exist at small Pm. | `1919 · the idea` (Larmor, via Rincon); `× 1933 · no axisymmetric dynamo` (Cowling); `1958 · first proofs` (Herzenberg; Backus); `1966 · α effect` (Steenbeck, Krause, Rädler); `1972-73 · dynamo flows` (Roberts; Ponomarenko); ring `C. NORE · 1997 · Taylor–Green dynamo`; ring `Y. PONTY · 2005 · down to Pm 0.01`; `2007 · small Pm works` (Iskakov et al.) | CONTEXT |
| SOA1.3 Building one | 28 | 3 | 1963: a first laboratory model, made of spinning iron cylinders. 1999: Riga and Karlsruhe, the first self-excited fluid dynamos (cards of 02.4 fly in and become pins). 2006-2007: VKS, the first dynamo in a fully turbulent flow, works only with soft-iron impellers, and it flips. The next big tank, DRESDYN in Dresden, aims at a dynamo driven by precession alone; in 2025 it was still being set up. | `1963 · iron cylinders` (Lowes & Wilkinson); `1999 · Riga`, `1999 · Karlsruhe`; `2007 · VKS dynamo + flips` (Monchaux et al.; Berhanu et al.); dashed `DRESDYN · precession` (Stefani et al. 2012; Giesecke et al. 2025) | CONTEXT |
| SOA1.4 Computing one | 24 | 4 | 1981: turbulent dynamos in a computer. 1995: a full 3D simulation of the Earth's core produces a reversal. Benchmarks let codes check each other (2001). From 2016, the VKS tank itself is simulated, impellers included, with two codes. But simulations stay far from sodium: Reynolds numbers of about a thousand instead of millions. And the walls matter: in the cases explored, the simulated VKS flips only with a conducting layer around it. | `1981 · turbulent dynamos` (Meneguzzi, Frisch, Pouquet); `1995 · reversal in a geodynamo model` (Glatzmaier & Roberts); `2001 · benchmark` (Christensen et al.); ring `C. NORE · 2016 / 2018 · VKS in SFEMaNS`; ring `Y. PONTY · 2017 · VKS in LATU`. Numbers: Re = 1594 in the reference reversal run `[site R:161]`, sodium Re of millions `[site R:137; P3:1145]`; conducting layer "necessary for these inversions to occur" `[site S:227-235]` | CONTEXT |
| SOA1.5 A few dials | 24 | 5, 6 | 1958: two coupled disc dynamos already flip. 2008: a symmetry argument links flips to the dipole and the quadrupole. 2012: three dials that flip chaotically, the model of chapter 4 (forward pointer). 2016: a method that finds equations from data. 2026: a four-dial model fitted on VKS simulations, MilaDy's first paper. | `1958 · coupled discs flip` (Rikitake); `2008 · dipole + quadrupole` (Pétrélis & Fauve); `2012 · three dials` (Gissinger); `2016 · equations from data` (SINDy) on lane 6; diamond `C. NORE, Y. PONTY et al. · 2026 · DQVU` | CONTEXT |
| SOA1.6 Where MilaDy sits | 16 | 3-5, 6 | MilaDy began in 2026 where the tanks, the simulations and the few-dial models meet. The data-driven lane is thin: a 2022 attempt found no reliable early warning of geomagnetic flips by machine learning. A violet question mark: can a machine that dreams snapshots join this map? We come back here near the end. | bracket `MILADY · 2026-2029`; `× 2022 · no reliable precursor` (Gwirtz et al.); dashed violet `? · 2027-` | CONTEXT, PLANNED (for "?") |
| chSOA1.Q | 8 | — | Question card (below). | — | — |

**Question card chSOA1.Q** (does not repeat ch02.Q, ch08.Q or ch09.Q):
```json
{"en": "Besides stirring speeds and iron, which wall and outer-layer properties must the simulations vary?",
 "fr": "En plus des vitesses des turbines et du fer, quelles propriétés des parois et du milieu extérieur faut-il faire varier ?",
 "why": "In the explored range, VKS simulations reversed only with a conducting surrounding medium (Bousquet et al. 2026); wall conditions shift onset (Botez et al. 2026; vacuum vs pseudo-vacuum moves Rm_c by about 40 %, Nore et al. 2018).",
 "unblocks": "The list of knobs of the simulation campaign, hence the number of runs, and the conditioning vector of the generator.",
 "ask_who": "C. Nore / Y. Ponty"}
```
Sources: `[site S:227-235]` (Bousquet: "necessary for these inversions to occur"), Botez et al. 2026 `[ABS]`,
`[site R:143]`.

## 3. chSOA2 "The map of the field: where this work fits" (L4 → L5, ≈ 270 s, after ch09, before ch10, both cuts)

- **Learning goal.** Know the four machine-learning tracks that touch this work, why each fails at least one
  of the four tests a laboratory dynamo imposes, what the four supervisors have published, and the exact empty
  spot the internship and the thesis aim at, with its nearest neighbours.
- **Takeaway (one sentence).** Fast surrogates, field generators, constraint machinery and generative priors
  each exist, but none has been built for a walled, low-Pm, reversing dynamo; the thesis targets that
  intersection, using what the consortium already has.
- **Level rail.** ch09 is L4 and 10.1 opens at L4 (`script/_review/ch10.md:138` already flags this). Either keep
  the narration at L4 and put the L5 content (constraint classes, Rice, vector potential) on the formula layer
  (D8), or reach L5 at SOA2.4 and ask the consistency editor to set 10.1 `levelFrom` to L5. Do not step down.
- **Word budget.** ≈ 570 words.

### 3.1 The four tests (drawn as four gates at the right edge of the map, reused in every scene)

| Gate | Why a dynamo imposes it | Source |
|---|---|---|
| `3D` | a self-sustained dynamo needs three dimensions (Zel'dovich 1957, recalled by Tobias 2021); 2D MHD is a test bench, not a dynamo | `[site R:240]` |
| `WALLS · VACUUM · IRON` | VKS and DRESDYN are walled cylinders; across the iron impellers B·n and the tangential part of B/μr are continuous; SFEMaNS data are azimuthal Fourier modes on a finite-element meridian mesh; vacuum vs pseudo-vacuum shifts Rm_c by about 40 % | `[site T:111-117; R:143-145]` |
| `LOW Pm` | sodium Pm = 0.82 × 10⁻⁵; simulations "typically restricted to Pm~1 regimes" (MilaDy postdoc offer); the reference reversal run has Re = 1594, Rm = 531, so Pm ≈ 0.33 (arithmetic of this brief) | `[site R:137; S:88; R:161]` |
| `RARE EVENTS` | a VKS reversal lasts about 5 s against mean polarity durations of 120 s and 50 s; the usable geomagnetic record of 0-2 Ma "contains only five reversals" | `[site R:149]`; Gwirtz et al. 2022 `[ABS]` |

### 3.2 Scenes

| Scene | target_s | Beats (facts to say) | Pins drawn (label · source) | Gate verdict shown | Badge |
|---|---|---|---|---|---|
| SOA2.1 Back to the map | 20 | The century map returns (T1 morph from chSOA1's layout); zoom into the data-driven lane, 2014-2026, which unfolds into four lanes. Four gates appear: 3D, walls, low Pm, rare events. | lanes only | gates drawn empty | CONTEXT |
| SOA2.2 Fast, but average | 30 | Networks that learn a solver: physics in the loss (2019), operators between function spaces (2021), foundation models (2024). For MHD: laminar 2D (2023), then 2D turbulence with a diffusion correction, at Pm equal to one (2025). For dynamos: learned mean-field closures, and a 2022 study that found no reliable early warning of geomagnetic flips. Trained to minimize the mean-square error, ensembles of such models "regress to the mean flow" in 3D turbulence: a cloud with two polarities collapses to its middle. | `2019 · PINN` (Raissi et al.); `2021 · neural operators` (Li et al.; Lu et al.); `2024 · foundation models` (McCabe et al.; Herde et al.); `2023 · MHD 2D, laminar` (Rosofsky & Huerta); `2025 · MHD 2D, Pm 1` (Kacmaz, Huerta, Haas); `2019 · learned α` (Nauman & Nättilä); `× 2022 · no reliable precursor` (Gwirtz et al.); `2026 · "regress to the mean"` (GenCFD, Raonić et al.) | 3D: some; walls: no; low Pm: no; rare: negative | CONTEXT |
| SOA2.3 Machines that sample | 30 | Generative models learn a whole distribution, not its mean: adversarial networks (2014-2021, a covariance already imposed on a convection generator in 2020), then diffusion (2020) and flow matching (2023). They now generate 3D turbulence (2024), global weather ensembles (2025), statistics of 3D flows and steady turbulent states conditioned on parameters (2026). We found no diffusion or flow-matching model trained on dynamo simulations. | `2014 · GAN` (Goodfellow et al.); `2018 · tempoGAN` (Xie et al.); `2020 · covariance constraint` (Wu et al.); `2020 · diffusion` (Ho et al.); `2023 · flow matching` (Lipman et al.); `2024 · 3D turbulence` (TurbDiff, Lienen et al.; CoNFiLD, Du et al.); `2025 · GenCast` (Price et al.); `2026 · GenCFD` (Raonić et al.), `2026 · steady states` (Galletti et al., preprint), `2026 · FunDiff` (Wang et al.); empty violet slot `dynamo fields · none found` | 3D: yes; walls: partly, no divergence; low Pm: no; rare: user-defined events (Finzi et al. 2023), never a dynamo | CONTEXT; `[NEG]` chip on the empty slot |
| SOA2.4 Making samples obey | 45 | Four ways to make samples obey a law. Hard, by construction: divergence-free networks (2022), a vector potential and its curl in a periodic 3D box (2023), a Leray projection in 3D periodic turbulence (2026), a stream function in 2D (2026). Hard, at sampling time: projections (2025). Soft: a penalty in the loss (2025-2026). On the whole distribution: a covariance (2020), dual constraints (2024), the stationary Fokker–Planck equation in weak form as a loss (2026), a weak-form residual used to tilt a flow-matching model (2026). Symmetry: an equivariant flow gives a symmetric distribution (2020). A 2026 comparison: "no single strategy dominates". In 3D, the only exact divergence constraint we found lives in a periodic box, and none handles walls, a vacuum outside and iron inside. | HARD: `2022 · divergence-free nets` (Richter-Powell, Lipman, Chen); `2023 · vector potential, 3D periodic` (Mohan et al.); `2026 · Leray, 3D periodic` (PCDM, Li, Buzzicotti, Bonaccorso, Biferale, preprint); `2026 · stream function` (FunDiff). AT SAMPLING: `2025 · ECI`, `2025 · PCFM`. SOFT: `2025 · PIDM` (Bastek et al.), `2026 · PBFM` (Baldan et al.). DISTRIBUTIONAL: `2020 · covariance` (Wu et al.), `2024 · dual training` (Khalafi et al.), `2026 · weak Fokker–Planck` (Cai et al.), `2026 · weak residual tilt` (Tauberschmidt et al.). SYMMETRY: `2020 · equivariant flows` (Köhler, Klein, Noé), `2023 · equivariant flow matching` (Klein et al.). Comparison chip: `2026 · "no single strategy dominates"` (Genuist et al., preprint) | 3D: one periodic preprint; walls + vacuum + iron: none found; low Pm: no; rare: no | CONTEXT |
| SOA2.5 Priors for assimilation | 25 | Data assimilation merges a model with sparse measurements. Learned priors entered it through autoencoder latent spaces (2021-2022), then diffusion (2023-2024), and a library that plugs deep networks into Kalman filters and variational methods (2025). None was applied to MHD in what we found. Near a flip the answer has two polarities; a prior that ignores the B to minus B symmetry would favour one. | `2021 · latent DA` (Amendola et al.; Peyron et al.); ring `S. CHENG · 2022 · generalised latent assimilation`; `2023 · score-based DA` (Rozet & Louppe); `2024 · DiffDA`, `2024 · EnSF` (Huang et al.; Bao et al.); ring `S. CHENG · 2025 · TorchDA` | 3D: weather scale; walls: weather grids; low Pm: no; rare: bimodal posterior not studied for MHD | CONTEXT |
| SOA2.6 Who brings what | 40 | The four supervisors' published work, as pins (names in text only, one line each, see §4). The consortium already holds three ingredients: dynamo simulations and a reversal model (C. Nore, Y. Ponty), representation learning on von Kármán flows (D. Lucor, C. Nore), data assimilation and generative surrogates outside MHD (S. Cheng). None of the four has published a generative model trained on dynamo data. | rings from §4 appear in their lanes; diamond DQVU 2026 pulses | — | CONTEXT; `[NEG]` chip on the last sentence |
| SOA2.7 The empty intersection | 45 | The generative and constraint lanes cross the dynamo lanes at an empty spot: the thesis, 2027-2030, planned. Five gaps, each pinned next to its nearest neighbour: (1) a generator of dynamo fields; (2) zero divergence of u and B, exact, in a walled cylinder with iron and vacuum; (3) budgets imposed on the distribution, without target values, even where there is no data; (4) the flip rate read from snapshots with Rice's formula; (5) a generator that crosses the dynamo threshold. The internship tested pieces of this on toy cases (callback to ch09's scoreboard). | dashed violet ring `THESIS · 2027-2030`; five gap pins with neighbour chips, see §5 | — | PLANNED; MEASURED on callbacks |
| SOA2.8 Neighbours and limits | 25 | The field moves fast. A 2026 paper (ICLR) claims to be the first to recognize the trade-off between distributional and physical accuracy; the internship's per-sample result must be positioned against it. Close neighbours exist: exact divergence in a periodic 3D box, generators of 2D MHD, flow matching of steady turbulent states. What neither the internship nor the thesis claims: waiting times between flips, sodium's Pm, the Earth's core, real laboratory data. A literature watch precedes each submission. | `2026 · PBFM` highlighted (Baldan, Liu, Guardone, Thuerey); neighbour halos around PCDM, Kacmaz, Galletti; four grey "not claimed" tags | — | CONTEXT, PLANNED |
| chSOA2.Q | 8 | Question card (below). | — | — | — |

**Question card chSOA2.Q** (category: scientific framing):
```json
{"en": "A 2026 paper claims the physics-versus-distribution trade-off first: how should our per-sample result be positioned?",
 "fr": "Un article de 2026 revendique ce compromis entre physique et loi : comment situer notre résultat par échantillon ?",
 "why": "The report and the thesis claim the statement and measurement of the inconsistency of a per-sample constraint for a stationary budget (R:121, T:157); PBFM (Baldan et al., ICLR 2026) writes that it is 'the first to recognize the trade-off between distributional and physical accuracy' and is not cited on the site.",
 "unblocks": "The framing of the first paper (distributional constraints, month 10) and whether PBFM joins the baselines of tier 1.",
 "ask_who": "S. Cheng / D. Lucor"}
```
Sources: `[site R:121; T:157; E:493-499]`; Baldan et al. 2026 `[ABS, re-read 2026-11-08]`.

## 4. Supervisor pins (names in text only; facts only)

Each line is one pin label plus the one sentence a narrator or lower-third may use. All from the supervisors'
own publications (`[site S:...]` lines, re-checked 2026-11-08).

| Pin label | Lane | One factual line | Citation |
|---|---|---|---|
| `C. NORE · 1997` | Theory / Simulations | Dynamo action in the Taylor–Green vortex; the threshold depends on the flow's symmetries. | Nore, Brachet, Politano, Pouquet, *Phys. Plasmas* 4, 1-3, doi:10.1063/1.872578 `[ABS]` |
| `C. NORE · 2016 / 2018` | Simulations | First fully nonlinear simulation of VKS with both impellers (2016, the paper's words "for the first time"); onset near Rm ≈ 70 at large Re (2018). | *EPL* 114, 65002, doi:10.1209/0295-5075/114/65002; *J. Fluid Mech.* 854, 164-195, doi:10.1017/jfm.2018.582 `[ABS; site Dy:198-233]` |
| `C. NORE · 2011-2026` | Simulations | Precession can drive a dynamo in a cylinder (2011); boundary conditions change onset and symmetry (2026). | *PRE* 84, 016317, doi:10.1103/PhysRevE.84.016317; Botez et al., *Phys. Rev. Fluids* 11, 083701, doi:10.1103/rx1h-5zxp `[ABS]` |
| `C. NORE · SFEMaNS` | Simulations | SFEMaNS, developed by J.-L. Guermond, C. Nore and colleagues since 2002 (her seminar abstract). | Guermond et al. 2007, 2009, *J. Comput. Phys.*; `[site S:217-226]`; LadHyX seminar abstract `[FT]` |
| `Y. PONTY · 2005` | Theory | Taylor–Green dynamos from Pm = 1 down to 10⁻². | *PRL* 94, 164502, doi:10.1103/PhysRevLett.94.164502 `[ABS; site Dy:573-595]` |
| `Y. PONTY · 2007` | Theory | The Taylor–Green dynamo bifurcation is subcritical, with hysteresis. | *PRL* 99, 224501, doi:10.1103/PhysRevLett.99.224501 `[ABS]` |
| `Y. PONTY · 2008` | Theory | On-off intermittency near the ABC-flow dynamo threshold. | Alexakis & Ponty, *PRE* 77, 056308, doi:10.1103/PhysRevE.77.056308 `[ABS]` |
| `Y. PONTY · 2014 / 2017` | Simulations | The LATU pseudo-spectral solver with penalised impellers; high permeability selects the axisymmetric mode. | Kreuzahler et al., *NJP* 16, 103001; *PRL* 119, 234501, doi:10.1103/PhysRevLett.119.234501 `[ABS; FT arXiv:1706.00260v4]` |
| `D. LUCOR · 2002-2007` | Surrogates | Generalized polynomial chaos for uncertainty in flows. | Xiu, Lucor, Su, Karniadakis, *J. Fluids Eng.* 124, 51-59, doi:10.1115/1.1436089; Lucor, Meyers, Sagaut, *J. Fluid Mech.* 585, 255-279 `[ABS]` |
| `D. LUCOR · 2022 / 2024` | Surrogates / Constraints | PINNs for turbulent convection with a relaxed incompressibility constraint (2022); networks that respect Galilean and rotational invariance (2024). | *J. Comput. Phys.* 456, 111022, doi:10.1016/j.jcp.2022.111022; Cai et al., *Comput. Fluids* 275, 106246 `[ABS]` |
| `D. LUCOR, C. NORE · 2025` | Surrogates / Symmetry | Autoencoders read through POD on forced flows, including von Kármán; equivariance relations between latent and physical variables. | Bousquet, Nore, Lucor, *Comput. Phys. Commun.* 315, 109728, doi:10.1016/j.cpc.2025.109728 `[ABS]` (consortium paper, **not** MilaDy-funded) |
| `S. CHENG · 2022` | Assimilation priors | Variational assimilation in a latent space, with surrogate observation maps and an error bound. | *J. Sci. Comput.* 94, 11 (issue 2023, online 2022), doi:10.1007/s10915-022-02059-4 `[ABS]` |
| `S. CHENG · 2025` | Assimilation priors | TorchDA: Kalman filters and variational assimilation with deep networks; named in the MilaDy abstract. | *Comput. Phys. Commun.* 306, 109359, doi:10.1016/j.cpc.2024.109359 `[ABS]`; ANR page |
| `S. CHENG · 2025 / 2026` | Generative models | Diffusion models for field reconstruction from sparse sensors (2025) and for probabilistic wildfire forecasts (2026). | Zhuang, Cheng, Duraisamy, *CMAME* 435, 117623, doi:10.1016/j.cma.2024.117623; Yu et al., *GMD* 19, 1027-1054, doi:10.5194/gmd-19-1027-2026 `[ABS]` |
| diamond `C. NORE, Y. PONTY et al. · 2026` | Reduced models / Simulations | VKS reversals reproduced with both solvers; a four-mode reduced model (DQVU) fitted under constraints. MilaDy's first paper. | Bousquet, Ponty, Botez, Plihon, Nore, *Phys. Rev. Fluids* 11, 063703, doi:10.1103/9tx2-1m13 `[ABS; FT; site S:227-235]` |

Closing line allowed on screen and in narration: "None of the four has published a generative model trained on
dynamo data" `[NEG; site E:513-519; S:103; S:299]`. Also true, if needed: no machine-learning paper by Y. Ponty,
no dynamo paper by S. Cheng, no laboratory experiment by any of the four.

## 5. Gap pins for SOA2.7 (the thesis, PLANNED) and their nearest neighbours

| Gap pin label (screen) | What the internship measured (MEASURED callbacks) | Nearest neighbour chip | What the neighbour does not do | Sources |
|---|---|---|---|---|
| `1 · a generator of dynamo fields` | E2: conditional generator of periodic 2D MHD; E3: kinematic ABC dynamo in 3D, no generator | Kacmaz et al. 2025 (2D MHD, Pm 1); Galletti et al. 2026 (steady states, preprint) | 2D cannot host a dynamo; no ∇·B in the generator; no magnetic field (Galletti) | `[site T:90-97; R:240; L:301]` |
| `2 · exact ∇·u = ∇·B = 0, walls, iron, vacuum` | potentials reach a relative divergence of 1.8 × 10⁻¹⁷ in 2D; curl form keeps ∇·B < 1.6 × 10⁻¹⁶ in 3D periodic | PCDM 2026 (3D periodic Leray, preprint); Mohan et al. 2023 (3D vector potential, periodic, not generative) | no walls, no vacuum matching, no permeability jump, not u and B together | `[site T:92, T:97; R:241-242; E:518]` |
| `3 · budgets on the distribution, no target, no data needed` | E2: mean energy-budget residual 0.46 → 0.061 at unseen η; still above the honest noise floor | Weak Generative Sampler (Cai et al. 2026, SDEs up to dimension 100); Tauberschmidt et al. 2026 (per-sample weak residual) | not a parametric field generator; not target-free identities | `[site T:94, T:147-149; R:120]` |
| `4 · flip rate from snapshots (Rice)` | E1: 4-6 % error on the reference distribution, 14 % on generated samples far from the threshold, 42 % near it | Gwirtz et al. 2022 (time series, negative); Finzi et al. 2023 (rare-event sampling) | all need trajectories or a target event; none turns snapshots into a crossing rate | `[site T:88, T:158; R:122]` |
| `5 · across the dynamo threshold` | E1: the smooth generator smooths the jump (42 % near threshold) | ACDM 2026 (extrapolation in Re); Kacmaz 2025 (error above 0.85 at Re = 100 for a model trained at Re = 1000) | no generative model studies the crossing of a bifurcation or conditions on (Re, Rm) jointly | `[site T:88, T:126-131; R:244; L:382]` |

Optional sixth pin, if time allows: `6 · prior for assimilation, two polarities` (no MHD diffusion assimilation
found; thesis Q4 with TorchDA) `[site L:385; E:491; T:136]`.

What the thesis does **not** claim (grey tags in SOA2.8): waiting-time distribution between flips (the
stationary distribution does not fix it) `[site T:80, T:131]`; sodium-like Pm (the generator inherits the Pm of
its training simulations) `[site R:161]`; the geodynamo; experimental VKS data (assimilation planned from
synthetic probes) `[site E:491]`; feasibility in 3D bounded domains, which E1-E3 do not show `[site T:105]`.

## 6. Do not show without a new check

- **Unverified:** Larmor 1919 title and pages (say only "the idea, 1919", chip "via Rincon 2019"); the wording of
  the Glatzmaier–Roberts 1995 abstract (use only the paper's title); case definitions of the 2001 benchmark;
  contents of Nozières 1978, Jonkers 2003, Valet et al. 2005, Ogg 2020, Zimmerman et al. 2014; Steenbeck 1967
  (sodium α-effect measurement) and Gans 1971 (secondary sources only); **DRESDYN's status in 2026** (the last
  source read says "being set up", April 2025); Jarolim et al. 2023 loss terms; PBFM benchmark numbers; the
  Botez–Bousquet–Nore *J. Comput. Phys.* paper (not found); reservoir computing on the Maryland three-metre
  experiment (conference abstracts only).
- **Discrepancies (pick the bold value or say neither):** Lowes–Wilkinson second paper 1967 vs **1968**
  (Crossref); DRESDYN sodium mass 6 t vs 8 t (show neither); Kazantsev 1967 (Russian) vs **1968** (English);
  last reversal ≈ 780 ka vs ≈ 773 ka: the cold open uses the polarity time scale value 0.78 Ma (00.3, Gee & Kent
  2007 via Tauxe), Singer et al. 2019 give ≈ 773 ka; chSOA1 does not need the date, so leave it out; Permian
  superchron 312-262 vs 302-252 Ma (leave out); Riga first attempt 1986 vs 1987 (leave out); MilaDy dates: use the
  ANR page (January 2026, 48 months), not the CVs.
- **Attribution traps:** Bousquet, Nore, Lucor 2025 is a consortium paper, not a MilaDy paper (no ANR funding
  in Crossref or HAL); ECI's first author is Chaoran Cheng, unrelated to S. Cheng; the Kazantsev k^{3/2} sentence
  is in the arXiv abstract of Ponty et al. 2005, not the published one; Mininni et al. 2005 is in *ApJ*, not
  *ApJ Letters*.
- **Wording traps:** "first" only where marked above (Riga and Karlsruhe first self-excited fluid dynamos; VKS
  first dynamo in a fully turbulent flow and first laboratory reversals; Nore et al. 2016 "for the first time";
  PBFM's own claim, quoted as a claim). "No generative model of a dynamo" is always "we found no…".

## 7. Citations for every pin (metadata checked 2026-11-08)

*Earth's record:* Brunhes 1906, *J. Phys. Théor. Appl.* 5, 705-724, doi:10.1051/jphystap:019060050070500 · Vine
& Matthews 1963, *Nature* 199, 947-949, doi:10.1038/199947a0 · Cox 1968, *JGR* 73, 3247-3260,
doi:10.1029/JB073i010p03247 (content: Constable 2003, doi:10.1201/9780203207611.ch4, §4.1, full text read) ·
Singer et al. 2019, *Sci. Adv.* 5, eaaw4621.

*Theory:* Larmor 1919 via Rincon 2019, *J. Plasma Phys.* 85, 205850401, doi:10.1017/S0022377819000539 (§1.3-1.4)
· Cowling 1933, *MNRAS* 94, 39-48, doi:10.1093/mnras/94.1.39 · Herzenberg 1958, *Phil. Trans. R. Soc. A* 250,
543-583, doi:10.1098/rsta.1958.0007 · Backus 1958, *Ann. Phys.* 4, 372-447, doi:10.1016/0003-4916(58)90054-X ·
Steenbeck, Krause, Rädler 1966, *Z. Naturforsch. A* 21, 369-376, doi:10.1515/zna-1966-0401 · Roberts 1972,
*Phil. Trans. R. Soc. A* 271, 411-454, doi:10.1098/rsta.1972.0015 · Ponomarenko 1973, *J. Appl. Mech. Tech.
Phys.* 14, 775-778, doi:10.1007/BF00853190 · Iskakov et al. 2007, *PRL* 98, 208501,
doi:10.1103/PhysRevLett.98.208501 · Warnecke et al. 2023, *Nature Astron.* 7, 662-668,
doi:10.1038/s41550-023-01975-1 · Zel'dovich 1957 `[site Dy:441-442]` · Tobias 2021, *J. Fluid Mech.* 912, P1,
doi:10.1017/jfm.2020.1055.

*Lab dynamos:* Lowes & Wilkinson 1963, *Nature* 198, 1158-1160, doi:10.1038/1981158a0 (content: Stefani et al.
2018, arXiv:1803.03421 §2.1) · Gailitis et al. 2000, *PRL* 84, 4365-4368, doi:10.1103/PhysRevLett.84.4365 ·
Stieglitz & Müller 2001, *Phys. Fluids* 13, 561-564, doi:10.1063/1.1331315 · Monchaux et al. 2007, *PRL* 98,
044502, doi:10.1103/PhysRevLett.98.044502 · Berhanu et al. 2007, *EPL* 77, 59001, doi:10.1209/0295-5075/77/59001 ·
Stefani et al. 2012, *Magnetohydrodynamics* 48, 103-114, doi:10.22364/mhd.48.1.13 · Giesecke et al. 2024-2025,
arXiv:2410.14449v3 ("being set up").

*Simulations:* Meneguzzi, Frisch, Pouquet 1981, *PRL* 47, 1060-1064, doi:10.1103/PhysRevLett.47.1060 ·
Glatzmaier & Roberts 1995, *Nature* 377, 203-209, doi:10.1038/377203a0 · Christensen et al. 2001, *PEPI* 128,
25-34, doi:10.1016/S0031-9201(01)00275-8 · Nore et al. 2016, 2018 and Kreuzahler et al. 2017 (§4) · Bousquet et
al. 2026 (§4).

*Reduced models:* Rikitake 1958, *Math. Proc. Camb. Phil. Soc.* 54, 89-105, doi:10.1017/S0305004100033223 ·
Pétrélis & Fauve 2008, *J. Phys.: Condens. Matter* 20, 494203, doi:10.1088/0953-8984/20/49/494203 · Gissinger
2012, *Eur. Phys. J. B* 85, 137, doi:10.1140/epjb/e2012-20799-5 · Brunton, Proctor, Kutz 2016, *PNAS* 113,
3932-3937, doi:10.1073/pnas.1517384113 · Gwirtz et al. 2022, *GJI* 231, 520-535, doi:10.1093/gji/ggac195.

*Surrogates:* Raissi, Perdikaris, Karniadakis 2019, *J. Comput. Phys.* 378, 686-707,
doi:10.1016/j.jcp.2018.10.045 · Li et al. 2021, ICLR, arXiv:2010.08895 · Lu et al. 2021, *Nat. Mach. Intell.* 3,
218-229, doi:10.1038/s42256-021-00302-5 · McCabe et al. 2024, NeurIPS 37, arXiv:2310.02994 · Herde et al. 2024,
NeurIPS 37, arXiv:2405.19101 · Rosofsky & Huerta 2023, *Mach. Learn.: Sci. Technol.* 4, 035002,
doi:10.1088/2632-2153/ace30a · Kacmaz, Huerta, Haas 2025, *Mach. Learn.: Sci. Technol.* 6, 035057,
doi:10.1088/2632-2153/ae054c · Nauman & Nättilä 2019, *A&A* 629, A89, doi:10.1051/0004-6361/201935945 · Raonić
et al. 2026 (GenCFD), *Nat. Commun.* 17, 9846, doi:10.1038/s41467-026-76390-x (quote "regress to the mean flow"
from the abstract).

*Generative models:* Goodfellow et al. 2014, NIPS 27, arXiv:1406.2661 · Xie et al. 2018, *ACM Trans. Graph.* 37,
95, doi:10.1145/3197517.3201304 · Wu et al. 2020, *J. Comput. Phys.* 406, 109209, doi:10.1016/j.jcp.2019.109209 ·
Ho, Jain, Abbeel 2020, arXiv:2006.11239 · Lipman et al. 2023, ICLR, arXiv:2210.02747 · Lienen et al. 2024, ICLR,
arXiv:2306.01776 · Du et al. 2024, *Nat. Commun.* 15, 10416, doi:10.1038/s41467-024-54712-1 · Price et al. 2025,
*Nature* 637, 84-90, doi:10.1038/s41586-024-08252-9 · Galletti et al. 2026, arXiv:2607.13022 (preprint) · Wang
et al. 2026 (FunDiff), *Nat. Commun.* 17, 5749, doi:10.1038/s41467-026-72292-0 · Finzi et al. 2023, ICML,
arXiv:2306.07526.

*Constraints:* Richter-Powell, Lipman, Chen 2022, NeurIPS 35, doi:10.52202/068431-2759 · Mohan, Lubbers,
Chertkov, Livescu 2023, *Phys. Rev. Fluids* 8, 014604, doi:10.1103/PhysRevFluids.8.014604 (full text of
arXiv:2002.00021v2 read: periodic, no gauge fixed) · Li, Buzzicotti, Bonaccorso, Biferale 2026 (PCDM),
arXiv:2603.12834 (preprint) · Cheng C. et al. 2025 (ECI), ICLR, arXiv:2412.01786 · Utkarsh et al. 2025 (PCFM),
NeurIPS 38, doi:10.52202/085713-5354 · Bastek, Sun, Kochmann 2025 (PIDM), ICLR, arXiv:2403.14404 · **Baldan,
Liu, Guardone, Thuerey 2026 (PBFM), ICLR, arXiv:2506.08604** (abstract re-read 2026-11-08: "Our work is the first
to recognize the trade-off between distributional and physical accuracy") · Khalafi, Ding, Ribeiro 2024,
NeurIPS 37, doi:10.52202/079017-0836 · Cai, Cao, Huang, Zhou 2026, *SIAM J. Sci. Comput.* 48, C708-C735,
doi:10.1137/24M1665271 · Tauberschmidt, Fellenz, Vollmer, Duncan 2026, ICLR, arXiv:2508.09156 · Köhler, Klein,
Noé 2020, ICML, PMLR 119, 5361-5370 · Klein, Krämer, Noé 2023, NeurIPS 36, doi:10.52202/075280-2617 · Genuist,
Savin, Gatti, Clouteau 2026, arXiv:2601.19368 (preprint; quote "no single strategy dominates" `[site L:274-279]`).

*Assimilation priors:* Amendola et al. 2021, ICCS, doi:10.1007/978-3-030-77977-1_30 · Peyron et al. 2021,
*QJRMS* 147, 3759-3777, doi:10.1002/qj.4153 · Rozet & Louppe 2023, NeurIPS 36, doi:10.52202/075280-1763 · Huang
et al. 2024 (DiffDA), ICML, arXiv:2401.05932 · Bao, Zhang, Zhang 2024 (EnSF), *CMAME* 432, 117447,
doi:10.1016/j.cma.2024.117447 · Cheng et al. 2022/2023 and 2025 (§4).

*Neighbours named in SOA2.8 besides PBFM and PCDM:* Martin, Lübke, Li, Buzzicotti, Grauer, Biferale 2025,
*ApJS* 277, 48, doi:10.3847/1538-4365/adb432 (a diffusion model trained on test particles in 3D MHD turbulence;
R. Grauer is also a co-author of the LATU papers with Y. Ponty) — mention only if useful, as a fact, without
implying intent.
