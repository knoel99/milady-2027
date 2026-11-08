# Adversarial accuracy review of the outline

Reviewed: `outline.md` (version 2026-11-08) and `outline.json`. Both are built from `outline_src/outline_data.py`, and every flagged phrase appears in both files. Fix the data file and rebuild.

Sources checked (paths relative to `/home/user/milady-2027`):
- `en/rapport/index.qmd` (R)
- `en/these/index.qmd` (T)
- `en/index.qmd` (H)
- `en/encadrants/index.qmd` (S)
- `en/calcul/index.qmd` (C)
- `en/experiences/index.qmd` (X)
- `en/prep/p3-mhd-dynamo/index.qmd` (P3)
- `en/prep/p4-systemes-dynamiques/index.qmd` (P4)
- `experiences/resultats/digest.md` (D), `e1_gissinger.json` (J1), `e2_mhd2d.json` (J2), `e3_abc.json` (J3) and the `.npz` archives
- `infra/configs/*.yaml` (CFG), `milady/sim/run.py`, `milady/train/fm3d.py`

"Outline:N" means line N of `outline.md`.

## Verdict

Most numbers are copied correctly. I checked about 120 figures, and all the E1, E2 and E3 headline numbers match the report and the digest (see the list at the end).

The problems are interpretive. Some scenes:
- overstate what a proposition proves;
- present proposals as machinery that exists;
- set bets the configured campaigns cannot settle;
- contain four physics or mathematics errors (X6.6, C9.3, C4.6, C1.2).

No scene claims that the generative model reproduces reversals in 3D. Every 3D result is correctly marked as a bet, PROVISIONAL or PENDING. The disclaimer and the supervisor attribution follow H:43-46 and R:48-59.

Severity counts: 10 HIGH, 17 MEDIUM, 13 LOW.

## HIGH

**A1 · X6.6 · Outline:1430.** Quote: "a posterior that is bimodal in +/-B (Prop. 2.41) unless the prior respects the mirror".
- **Problem:** The logic is inverted. A mirror-symmetric prior is exactly what produces the symmetric, bimodal posterior when the observations are near zero or even in B. A lopsided prior does not remove the bimodality; it falsely favours one hump.
- **Evidence:** T:831-839 (Prop. 2.41 (i)-(ii)); T:843 ("posterior is bimodal if the prior is ... mean-based methods biased toward a nonphysical mean").
- **Fix:** "With a mirror-symmetric prior, a dipole observation near zero gives a posterior with two mirror humps, whose mean is not a physical state. A lopsided prior would wrongly favour one hump. An equivariant prior handles this exactly (symmetric pairs, or a latent 4D-Var started from z and Sz)."

**A2 · C9.4 · Outline:871, 883.** Quote: "the sign at Rm = 17.5 should be settled".
- **Problem:** The configured campaign sweeps integer Rm (4, 5, ..., 40). Rm = 17.5 is never simulated, so the bet cannot be settled as written.
- **Evidence:** CFG palier2_abc3d.yaml:36 (`Rm: {start: 4, stop: 40, step: 1}`); R:1114.
- **Fix:** Either state the bet as "λ(17) > 0 > λ(18) with |λ − λ_q| below |λ|", or add Rm = 17.25, 17.5 and 17.75 to a copy of the config. Mention it in the criterion line.

**A3 · C9.3 · Outline:854.** Quote: "a short trace of injection vs dissipation crossing and recrossing".
- **Problem:** With forcing that is white in time, the stored `injection` diagnostic is the constant Itô rate. It is a flat line, and only the dissipation fluctuates. A fluctuating injection trace would be fabricated physics.
- **Evidence:** milady/sim/run.py:256 and 273 ("injection (constante d'Itô)", `np.full`); R:442; R:919.
- **Fix:** Draw the dissipation D(t) fluctuating around a flat, labelled line ε_inj (Itô rate). The histogram should show ε_inj − D, centred on zero.

**A4 · C4.6 (Outline:472-474), synopsis (Outline:21), C8 takeaway (Outline:50, 743).** Quotes: "a snapshot does not know its own future"; "a shuffled box of snapshots still holds the flip rate"; "predicted from generated snapshots alone".
- **Problem:** In a deterministic model, a snapshot plus the equations determines its future, and Rice's formula relies on exactly that: Ḋ = −νD + VQ is computed on each snapshot. Snapshots alone cannot give a rate, which has units of 1/time. The C4.6 line contradicts C5.2 two minutes later.
- **Evidence:** R:321 (Remark 3.4); R:514-517 (Prop. 8 needs F); R:528 ("F must be known"); T:681.
- **Fix:** C4.6: "a snapshot carries no timestamp and no time order". Synopsis: "a shuffled box of snapshots, plus the equations, still holds the rate". C8: "from generated snapshots and the model's equations, without running time forward".

**A5 · C8.3 (Outline:771-773) and C8 takeaway (Outline:50, 743).** Quotes: "An elastic sheet stretched over a cliff"; "for a reason that is geometry, not bad luck".
- **Problem 1:** Prop. 9 bounds the error at a jump in the distribution, and the report says E1 is "intermediate". The symmetrized law that the generator learns varies continuously. Only the bridge mass and the crossing rate are born with a steep slope.
- **Problem 2:** The lag near the threshold is "consistent with" Prop. 9, not proven by it: one model, seed 0. Prop. 9 is a lower bound and does not explain the overshoot.
- **Evidence:** R:557; R:564; R:883 (C seed 0); R:901 (two seeds; only factor-2 differences count).
- **Fix:** Use a steep ramp instead of a cliff ("a stiff sheet cannot follow a steep ramp"). Takeaway: "...poorly near it, as expected from a generator that varies smoothly with the knob (Prop. 9, attenuated form)". Drop "not bad luck".

**A6 · C7.10 · Outline:731.** Quote: "The whole machine ... framework figure revealed panel by panel (a latent flow ..., c VKS geometry ...)".
- **Problem:** The figure shows the proposed framework. The experiments used a perceptron on Fourier coefficients: no latent space, no functional decoder, no VKS. Calling it "the whole machine" right after the results suggests it exists and was trained.
- **Evidence:** R:300 ("the model has not been trained on VKS ... data glyphs schematic"); R:1179 (perceptron, no field architecture); H:41 ("framework under study").
- **Fix:** Retitle "The proposed machine". Add a chip "PROPOSED · panels a, b, c not implemented; E1-E3 tested pieces only". Highlight which pieces were tested: potentials in 2D, equivariance in 3 variables, crowd loss, Rice.

**A7 · C9.7 · Outline:929-931, 940.** Quote: "At a held-out point (Re = 50, Pm = 2) the generated spectra ... judged against the PhD plan's criteria".
- **Problem 1:** In the plan, the spectrum criterion (b) applies at the training parameters. The held-out criterion is (c), Rm_c within 10% at a Pm without data.
- **Problem 2:** The plan assumes about 20 points with 5000 snapshots each. The configured campaign has 12 runs with 40 snapshots each, so "met / not met" lamps would overstate.
- **Evidence:** T:917; T:912; CFG palier2_tg3d.yaml:35-43; CFG train_fm3d.yaml:36-39 (val Re 100, Pm 1; test Re 50, Pm 2).
- **Fix:** Show the spectra at the test point as "diagnostic, no criterion". Apply criterion (b) at the training points. Label the lamps "indicative at 12 × 40 snapshots; plan: about 20 × 5000".

**A8 · C9.5, C9.7, X3.5 (Outline:890-903, 1159-1171).** Stationarity is assumed but not checked.
- **Problem:** The TG runs keep snapshots for t in [100, 140] from a seed of 10⁻³. Near threshold the field may still be growing exponentially. Those snapshots are not draws from an invariant measure, so E[dE/dt] ≠ 0 and the budget loss of X3.5 would be wrong there. C9.5 also promises a plateau that may not be reached by t = 140.
- **Evidence:** CFG palier2_tg3d.yaml:9-10 and 41-42; CFG train_fm3d.yaml:109 (`growth_rate` term for non-saturated budgets); R:278 (data are snapshots of a statistically stationary state); T:992 (risk: stationarity loss in 3D).
- **Fix:** Add a check in the extractor: flag a run as stationary only if E_B has saturated, meaning the slope of log E_B over the kept window is near 0. The C9.5 narration says "grows, and saturates where the run is long enough". X3.5 and C9.7 use saturated points only.

**A9 · X3.5 · Outline:1161, 1171.** Quote: "criterion: tier-1/2 criteria: budget residual < 5% ...; sigma(D) ratio 0.8-1.2".
- **Problem:** Both thresholds are tier-1 (2D) criteria. The plan's tier-2 criteria contain no budget or σ(D) target, so the scene invents a 3D criterion and attributes it to the plan.
- **Evidence:** T:903 (tier 1 (b), (d)); T:917 (tier 2 (a)-(d)).
- **Fix:** "Bet adapted from the tier-1 criteria (the plan sets none for 3D)". Keep the control-run clause.

**A10 · C7.7 · Outline:695.** Quote: "Forcing the stationary budget on each sample makes a spike ...: worse, not better".
- **Problem:** True for E1, where the energy distance is ×9. In E2, per-sample rescaling improved the descriptor distance (2.62 → 1.1) and the spectrum error, and was even better than V5 at the training values (0.422 vs 0.863). Only a dedicated metric, σ(D)/σ_ref = 8.6e-4, reveals the spike. The scene states a general rule that half its own evidence contradicts.
- **Evidence:** R:881; R:1035; Tables 4 and 6 at R:961 and R:993.
- **Fix:** "Worse where it counts: in E1 the distance is ×9. In E2 a spectrum-based score even improves, and only the spread of the dissipation shows the spike." This sets up C7.9's "looks fine".

## MEDIUM

**B1 · C3.7 · Outline:381-383.** The film's central question ("respect physics exactly ... statistically ... how often") sits on a MilaDy project lower-third.
- **Problem:** The project's stated objectives are reduced models for reversals and bursts, and DRESDYN optimisation. The constraint taxonomy and Rice are this study's framing (S:72; H:72).
- **Fix:** Split it: "MilaDy (context): reduced models of reversals; DRESDYN" / "This study asks: ...". Or move the C3.8 disclaimer before C3.7.

**B2 · Opening and closing narration · Outline:70, 84.** Quotes: "The first question turns out to be hopeless"; "Nobody can. The dynamo below is chaotic. Its memory fades too fast."; "even at settings nobody has simulated".
- **Problem 1:** The unpredictability argument on the site is for the Gissinger model (Lyapunov time ~11 vs polarity length > 100). Applying it to Earth is an external, unsourced claim.
- **Problem 2:** For Earth, "how often" is measured from rocks. The film's method predicts rates for models.
- **Problem 3:** Generation is interpolation between simulated settings only.
- **Evidence:** P4:1627; R:743; R:1179.
- **Fix:** Add an EXTERNAL_FACT flag (geodynamo predictability), or say "in the models we can study, ...". Change "nobody has simulated" to "between the settings that were simulated". Opening: "the second one, for a model, is not".

**B3 · Synopsis · Outline:21.** Quote: "liquid-sodium experiments that flip like the Earth".
- **Problem:** Only VKS reversed. Riga's field is an oscillating m = 1 mode. Karlsruhe's field is a stationary dipole with two states and no reversals.
- **Evidence:** R:139; R:149 ("first ... reversals in the laboratory, in VKS"); P3:1149.
- **Fix:** "a liquid-sodium experiment (VKS) that flips like the Earth".

**B4 · C1.2 · Outline:188.** Quote: "Magnetic field lines close on themselves".
- **Problem:** div B = 0 means lines have no ends. It does not mean they close: they can wind ergodically or chaotically, as in the ABC fields shown later in C2.5 and X1.2.
- **Fix:** "Field lines never start or stop: through any box, as many enter as leave". Keep the counters.

**B5 · C2.1 · Outline:249.** Quote: "honey (threads stay sharp) vs water (a grey blur wins)".
- **Problem:** This conflates viscosity with magnetic diffusivity. Liquid sodium has the viscosity of water and a large η (Pm ~ 10⁻⁵), so the analogy suggests viscous fluids make better dynamos.
- **Evidence:** P3:281; R:137.
- **Fix:** Compare a good conductor with a poor conductor (small vs large η), or dye in cold vs hot water with the label "diffusivity". Avoid honey.

**B6 · C4.5 · Outline:461.** Quote: "Different trajectories paint the same glow".
- **Problem:** Only true above the threshold. Below Γ ≈ 0.86 each trajectory stays in its own whirlpool, which is the point of C4.2 and C7.5.
- **Evidence:** R:871; R:901 ("reference is symmetrized by construction").
- **Fix:** Fix Γ = 0.93 on screen. One line: "above the threshold; below it, each start paints one whirlpool".

**B7 · X1.2 · Outline:1024-1026.** Quote: "The dominant growing mode changes shape across the windows; it carries the flow's symmetries".
- **Problem 1:** At Rm 8 and 20 the dominant mode decays (λ < 0).
- **Problem 2:** No mode from the second window (Rm > 27) is stored.
- **Problem 3:** The 24-element group and "all even symmetries" are published facts (Bouya and Dormy 2013). They were not checked on these modes.
- **Evidence:** R:1077, R:1092 (λ < 0); e3_modes.npz keys Rm8/12/16/20; R:1120.
- **Fix:** "Dominant mode (least damped or fastest growing) at Rm 8, 12, 16 and 20: below, inside and just after the first window". Badge: "published: first-window mode has all even symmetries".

**B8 · X1.1 · Outline:1014.** Quote: "the solver must return -0.5 at Rm = 2".
- **Problem:** The exact eigenmode only gives λ_dominant ≥ −1/Rm. Another mode could decay more slowly.
- **Evidence:** R:1116.
- **Fix:** "The dominant rate can be no lower than −1/Rm = −0.5; the solver finds −0.5001."

**B9 · X1.3 · Outline:1034.** Quote: "48^3 checks agree".
- **Problem:** They agree at Rm 12. At 17.5 the sign differs between resolutions (+2.3e-4 at 32³, −5.2e-4 at 48³).
- **Evidence:** R:1114.
- **Fix:** "48³ agrees at Rm 12; at 17.5 the sign flips: unresolved".

**B10 · C7.9 · Outline:719.** Quote: "a poll that shrank to two people".
- **Problem:** ESS/N = 0.002 on half b of 1000 samples is about one effective sample in 500.
- **Evidence:** R:695; R:1033 ("about one effective sample out of 500").
- **Fix:** "a poll of 500 that shrank to one person".

**B11 · C7.5 · Outline:675.** Quote: "B: 0.020-0.025 between training values".
- **Problem:** Cherry-picked. At the ten unseen values, B ranges from 0.007 to 0.025 (mean 0.0157), including above the threshold (0.0203 at 0.93).
- **Evidence:** J1 evaluation B_augmentation test (0.81: 0.0203; 0.83: 0.013; 0.85: 0.0246; 0.87: 0.0111; 0.93: 0.0203); R:839; R:873.
- **Fix:** "B: 0.003-0.006 at training values, 0.007-0.025 between them (mean 0.016)".

**B12 · C4.4 · Outline:450-452.** Quote: "mean polarity > 100".
- **Problem:** The source restricts this to Γ ≤ 0.95. At Γ = 1 the rate is 0.0112, an interval of about 89.
- **Evidence:** P4:1627; D fine grid.
- **Fix:** Show it at Γ = 0.9 (Lyapunov time ~11 vs a mean interval of ~230), or say "for Γ ≤ 0.95".

**B13 · C9.1 · Outline:832.** Quote: chip "PhD proposal: not accepted, not funded".
- **Problem:** The source does not say this. It says "independent proposal, neither requested nor validated by the supervisors". A funded PhD "may be offered".
- **Evidence:** T:46; T:56.
- **Fix:** Use the source wording: "Independent PhD proposal · not requested or validated by the supervisors".

**B14 · X5.1 · Outline:1269-1270.** Quote: "memory bar 6 N^3 x 4 bytes" next to "~6 GB at 256^3".
- **Problem:** 6N³ × 4 bytes is the state, 0.4 GB at 256³. The 6 GB figure is about 15 times the state, extrapolated from a 128³ peak. The visual mislabels it as measured.
- **Evidence:** C:176.
- **Fix:** "state 0.4 GB at 256³ · peak ≈ 15× state ≈ 6 GB (estimate)"; give 48 GB at 512³ the same treatment.

**B15 · C3.5 and X1.4 · Outline:361-362, 1046.** Quotes: "same threshold: Rm_c = 31, 44 or 52-71"; "~44 (Miralles)".
- **Problem 1:** The site's own conversion says Miralles' definition is about 1.05 × Nore's, which gives 54-75 at 16-22 Hz. So the 44 cannot be the same threshold under another definition; it likely comes from a different campaign.
- **Problem 2:** "90 → 130" is a simulation result (Nore et al. 2018, Re = 1.5e3, μ_r = 50), not the experiment.
- **Evidence:** P3:1167 vs P3:1194 and 1202; R:141 (no Miralles value); R:143.
- **Fix:** Drop 44, or label it "another campaign and definition". Add the chip "simulations, Nore et al. 2018" on the boundary-condition switch.

**B16 · C4.3, C8.1, closing narration (Outline:440, 748, 86).** Quote: "flip rate".
- **Problem:** The measured quantity is the rate of zero crossings of D, which counts excursions and chattering too. Pitfall P15 is applied on screen but not in the narration.
- **Evidence:** R:528; R:883.
- **Fix:** Closing narration: "the rate at which the dipole crosses zero comes out with a cumulative error of ... (one model, one seed)". Add "model C, seed 0" to C8.1.

**B17 · C8.2 and C8.3 · Outline:760, 772.** Quotes: "switches on late, then overshoots"; "fills too early and too softly".
- **Problem:** The two wordings contradict each other. The data show three things:
  - small spurious crossings and bridge mass below the threshold (up to 2e-4 and 3.5e-4, where the truth is 0);
  - a lag at 0.865 (0.0003 vs 0.00194);
  - an overshoot at 0.875-0.88.
- **Evidence:** R:883; D fine grid ("pont C").
- **Fix:** In both scenes: "leaks a little below, lags at the threshold, overshoots just above".

## LOW

- **C1 · C2.3, Outline:271.** curl(u×B) is transport plus stretching, and the leader line calls it "advection". Fix: label it "carried and stretched by the flow" (P1:523; P3:254).
- **C2 · C2.4, Outline:280.** "no axisymmetric field (Cowling)" should read "no exactly axisymmetric dynamo field". The ABC modes oscillate, so write λ as a real growth rate, or Re e^{λt} (R:1114: frequency about 0.53).
- **C3 · C4.2, Outline:431.** "merging crisis" in Γ is expected, not shown; Gissinger located it in μ. Fix: chip "attractor-merging crisis (shown in μ by Gissinger 2012; expected in Γ)" (R:159; R:784).
- **C4 · C1.1, Outline:177.** Replace the external Curie-temperature fact with the site's sourced argument: a free field decays in about 10⁴ years, while Earth's field is billions of years old (P3:269; P3:1471). This removes one EXTERNAL_FACT flag.
- **C5 · C0.4, Outline:140.** "every 10^5 to 10^6 years" sounds periodic. Write "typically 10⁵-10⁶ years apart, very irregular" (P3:1230).
- **C6 · C3.4, Outline:351.** The 120 s, 50 s and 5 s numbers sit on a qualitative normal-form curve whose durations "are not those of VKS". Put the numbers on a separate card (R:163).
- **C7 · C7.6, Outline:687.** "(lowest)" should read "lowest of A, B, C"; F on C reaches 0.0113 (R:873; R:875).
- **C8 · C5.3, Outline:520.** "within 4%" should read "cumulative error 4%" (R:883).
- **C9 · C6.2, Outline:569.** "never cross" holds in the (t, x) picture at fixed λ. In a state-space animation paths can cross at different t. Draw it with t on the horizontal axis (R:605).
- **C10 · C9.2, Outline:843.** "tamper-proof labels" should read "checksummed labels"; `--force` rewrites the file and updates the SHA-256 (C:93). X2.4, Outline:1091: add the condition "if each μ_λ is symmetric" (R:401).
- **C11 · X6.2, Outline:1374.** "vacuum matching without a Laplace solve per sample" is a candidate route, an open sub-question of Q1 (T:259-266). X5.5, Outline:1328: "uncertainty x2" should read "at least ×2" (T:974).
- **C12 · X4.5, Outline:1251.** "seeds {0, 1, 2} ... 2-3 h" — X:71 times two seeds, so three seeds take about 3-4.5 h unless the s2 caches are reused. C3.6, Outline:373: "terabytes" is an order-of-magnitude estimate; add a chip (T:931).
- **C13 · Data keys.** C4.6 and C5.2 cite `e1_echantillons.npz#ref|0.90`, but the archive key is `ref|0.9` (the 0.85, 0.87 and 0.93 keys match). Fix it in the extractor or the outline. Also note that `ref|0.9` holds 4000 points, so only about 10 fall in |D| < 0.2. The C5.2 strip will look sparse; use the cache's 20,000-sample set or say so.

## Checked and correct (no change)

- **E1:** threshold between 0.86 and 0.865; 0.00194 at 0.865 and about 0.011 at Γ = 1; P(D > 0) = 0.375 and 0.3125; A asymmetry 0.183 and 0.0854; C at about 0.004.
- **E1 distances:** 0.0118, 0.00356 and 0.00257 vs the 0.00123 floor; projection ×9 (0.0231); σ = 4e-17.
- **E1 Rice:** 4% and 6% on the reference; 14%, 17% and 65% far from the threshold; 42% near it; 0.00030 vs 0.00194; 0.00500 vs 0.00340.
- **E1 stationarity loss:** F 0.0136 vs 0.0324 and 0.0113 vs 0.0224; σ 1.04 → 0.75.
- **E1 tilting:** ESS/N 0.67 and 33× at Γ = 0.85; generation cost 0.5 vs 0.25 s.
- **E2 divergence:** 0.408; 0.34 and 0.162; E_B ×2.68; 5e-17, 1.7e-17 and 2.03e-8.
- **E2 distributions:** 2.58, 2.52 and 0.699; 26/37% → 6.7/6.2%; σ 0.663 → 0.788; tilting 0.47 → 0.193, 2.62 → 4.15, ESS 0.287; rescaling 8.64e-4 and 1.1.
- **E2 per-η table:** all values match Table 7.
- **E3:** thresholds 8.87, 17.6 and 26.8 vs published 8.9, 17.5 and about 27; −0.5001; N = 48 values 0.00812 and −5.2e-4; divergence 3e-19 to 1.52e-16.
- **VKS:** 16/22 Hz, 120/50 s, 5 s and 0.4 s; 150 L and 300 kW.
- **Pm and Re:** Pm ~ 1e-5 implies Re ~ 10⁶-10⁷.
- **Project:** ANR-25-CE51-0077, January 2026, 48 months, partners.
- **Thesis plan:** tier budget 700, 3900, 3200 and 1200 GPU h plus 20% ≈ 1.1e4 GPU h; PCDM ≈ 1150 GPU h; papers at months 10, 22 and 33; scores 4.10 and 3.90; tier 0, 1, 3 and 4 criteria; TG anchor Rm_c = 30 at Pm = 1.
- **fm3d:** Coulomb-gauge potentials for u and B and B → −B equivariance (C:164-166; CFG train_fm3d.yaml), so C9.6 is supported.
- **Infrastructure:** 68 tests; 0.08 s per 64³ step.
- **Formulas:** Props 1-9, Cor. 6, the two-half-batch estimator, Rice, the energy distance and the ESS formulas are transcribed correctly.
