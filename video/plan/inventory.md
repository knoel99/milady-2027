# MilaDy 2027 explainer video: content inventory

Knowledge map for the long English explainer video. Everything below is taken from the repository
`/home/user/milady-2027` (read-only). Numbers are copied exactly; line numbers refer to the files as of
2026-11-07. Where I computed something myself (CPU cost estimates), it is labelled **estimate**.

## 0. Conventions

### 0.1 Source abbreviations (paths relative to `/home/user/milady-2027/`)

| Abbr. | File |
|---|---|
| H | `en/index.qmd` (home) |
| R | `en/rapport/index.qmd` (internship report, prospective) |
| T | `en/these/index.qmd` (PhD proposal) |
| S | `en/encadrants/index.qmd` (supervisors and MilaDy project) |
| X | `en/experiences/index.qmd` (experiments page) |
| C | `en/calcul/index.qmd` (computing and data) |
| I | `en/interactifs/index.qmd` (interactive diagrams) |
| P | `en/prep/index.qmd`; P1..P8 = `en/prep/pN-*/index.qmd` |
| D | `experiences/resultats/digest.md` (generated numerical digest; French labels) |
| J1, J2, J3 | `experiences/resultats/e1_gissinger.json`, `e2_mhd2d.json`, `e3_abc.json` |
| IR | `infra/README.md` (deployment guide, French) |
| CFG | `infra/configs/*.yaml` |

### 0.2 Abstraction ladder

| Level | Audience | Vocabulary allowed |
|---|---|---|
| L0 | anyone | magnets, compass, Earth, flips, "knobs", pictures |
| L1 | curious high-school / early undergrad | arrows as fields, histograms, averages, simulation, "rules on average vs every time" |
| L2 | science undergrad (L2-L3) | divergence, curl, Fourier modes, energy budget, Reynolds numbers, bifurcations |
| L3 | M1 ML or physics | flow matching, conditioning, POD, equivariance, invariant measure, I-projection |
| L4 | M2 / early PhD | Leray, stationarity identities, unbiased estimators, Rice formula, energy distance with floors |
| L5 | supervisors / specialists | stiff contraction term, Jensen gap, W1 bounds, gauges in bounded domains, interface kinks, hybrid Fourier-FE data, hypoellipticity |

### 0.3 Honesty frame (must survive into the script)

- The internship report is **prospective**: written before the internship, with real but small CPU
  experiments, not reviewed or validated by the supervisors (H:43-46; R:51; T:55-58).
- All experiments ran on a 4-core Xeon 2.30 GHz without GPU (X:41-44; R:753).
- E1 uses 2 seeds (3 planned), E2 one seed per variant (R:745, R:901, R:1175).
- The models remain weak: spectral errors 0.07-0.23 in log10 vs 0.002-0.011 for data samples (R:80, R:1039).
- Tests are interpolation in the parameter, never extrapolation (R:743).
- "To our knowledge" novelty claims, literature search closed 2026-11-06 (R:118; T:154).

### 0.4 Colour key (site identity, reuse in all scenes)

green `#009E73` control parameter (Gamma, eta, Rm, Re, Pm) · blue `#0072B2` velocity u (also "true for each
sample" in the taxonomy figure, R:306) · vermillion `#D55E00` magnetic field B · violet `#6C4BA0` generative
model · amber `#E69F00` distribution-level metrics (orange = "true only for the distribution" in R:306) ·
greys for infrastructure. Note: the taxonomy figure already uses blue = per-sample and orange = distributional;
the thesis timeline (T:1093-1099) uses amber/blue/green diamonds for papers of axes 2/1/3.

---

## 1. Key concepts (L0 to L5)

ID, concept, level, one-line plain explanation, source.

### L0 (anyone)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K01 | Dynamo effect | A moving, electrically conducting fluid can amplify and sustain a magnetic field against its natural decay; it explains the fields of the Earth and stars. | R:86; H:64 |
| K02 | Polarity reversals | The magnetic dipole sometimes flips sign abruptly; this happened to the Earth and was reproduced in the VKS lab experiment. | R:90; S:72; T:138 (fig vks) |
| K03 | Lab dynamos are rare | Only three liquid-sodium experiments, including Cadarache (VKS), have achieved a dynamo; DRESDYN (Dresden) tries with a precessing cylinder. | R:86; S:66 |
| K04 | VKS | Two counter-rotating impellers stir liquid sodium in a cylinder; it only worked with soft-iron impellers. | R:90; T:138 |
| K05 | Simulations are costly | Each 3D turbulent dynamo simulation is expensive, so only a few parameter settings exist, producing huge, hard-to-reuse datasets. | H:64; T:62 |
| K06 | Knobs and thresholds | The outcome depends on control parameters (Re, Rm, materials, forcing) and changes abruptly at thresholds. | H:66; R:90 |
| K07 | Generative model | A machine that invents new, plausible examples of fields, on demand, for a chosen knob setting. | H:66; R:74 |
| K08 | Physics rules for generated fields | Magnetic field lines never start or end; on average, energy injected equals energy dissipated. | H:66; R:76 |

### L1 (curious beginner)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K09 | Zero divergence | No sources or sinks: fluid is incompressible (div u = 0), magnetic field lines are closed (div B = 0). | R:313; P1 |
| K10 | Snapshot, not movie | A snapshot generator produces still frames of a turbulent state, never a time series. | R:320-322; R:507 |
| K11 | The distribution is the object | In chaos the trajectory is unpredictable but the histogram of visited states is reproducible. | P4:1821; R:278 |
| K12 | Seen vs unseen knob values | Train on some parameter values, test at values in between that the model never saw. | R:743 |
| K13 | Flip symmetry B -> -B | A field and its flipped twin must be equally likely. | R:315; R:400 |
| K14 | True for each vs true on average | Some rules hold for every single field, others only for the crowd of fields; the whole project rests on this distinction. | R:304; R:1199 |
| K15 | Magnetic Reynolds number Rm | Stretching of field lines by the flow vs magnetic diffusion; here Rm = 1/eta. | R:1066; P3 |
| K16 | Growth rate lambda | lambda > 0 means a weak seed field grows exponentially: a dynamo. | R:1066 |

### L2 (science undergrad)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K17 | Potentials | Generate a stream function psi or vector potential A; taking its curl gives a divergence-free field automatically. | R:335; P1 |
| K18 | Fourier modes, spectra, pseudo-spectral solvers | Fields as sums of waves; energy per wavenumber shell E(k); 2/3 dealiasing. | R:631; R:917; P1; P2 |
| K19 | Leray projection (Helmholtz-Hodge) | Remove the gradient part of a field, mode by mode in Fourier space. | R:645; I:61-72 |
| K20 | Energy budget is an identity | dE/dt = P - eps holds for each snapshot as a definition; the constraint is only E[P - eps] = 0. | R:321 |
| K21 | Gissinger three-mode model | (Q, D, V) = quadrupole, dipole, velocity; chaotic reversals appear when two symmetric attractors merge (crisis). | R:434; R:784; P4:1513-1515 |
| K22 | ABC flow and kinematic dynamo | A Beltrami flow imposed on the induction equation; dynamo windows 8.9 < Rm < 17.5 and Rm > 27. | R:1063; R:1112 |
| K23 | Bifurcations, hysteresis | Supercritical (continuous, sqrt growth) vs subcritical (jump, hysteresis) transitions. | R:551-564; T:768 |
| K24 | Zel'dovich anti-dynamo theorem | No self-sustained dynamo in 2D, hence E2 is magnetically forced. | R:240; R:925 |
| K25 | POD = Fourier in homogeneous turbulence | For statistically homogeneous periodic fields the optimal (POD) basis is the Fourier basis. | R:627-628 |

### L3 (M1 ML or physics)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K26 | Conditional flow matching | Learn a velocity field that transports Gaussian noise to the data along straight paths x_t = (1-t)x0 + t x1; the optimum is a conditional expectation learned by plain regression. | R:282-296; fig flow-matching (R:605) |
| K27 | Conditioning and sampling | Parameter enters through Fourier features; MLP; Heun scheme 50 steps = 100 network evaluations. | R:593-601 |
| K28 | Taxonomy C1-C4 | C1 local linear, C2 local nonlinear, C3 symmetry, C4 stationarity; each enforced where it is true. | R:309-317; fig taxonomie (R:306) |
| K29 | Hard constraint by construction (Prop 1) | If the decoder's image lies in the constraint subspace, every sample satisfies it whatever the training quality. | R:327-335 |
| K30 | Equivariance vs augmentation (Prop 4) | An equivariant velocity field plus invariant noise gives an exactly symmetric distribution at every parameter; augmentation only where data exist. | R:400-412; R:614-620 |
| K31 | Invariant measure, generator, stationarity identities (Prop 5) | For any test function phi, E_mu[L phi] = 0; the energy budget is phi = E. | R:265-278; R:422-430 |
| K32 | Exponential tilting / I-projection / ESS (Prop 7) | Reweight samples to fix a mean with minimal KL change; cannot create mass, ESS collapses where the model misses regions. | R:465-485 |
| K33 | Distribution metrics and noise floors | Energy distance, sliced Wasserstein; always read against the floor measured at equal sample size. | R:715-725; R:747 |
| K34 | Per-sample projection is inconsistent (Cor 6) | Forcing a stationary budget on each sample yields a Dirac, singular w.r.t. the truth (infinite KL, W1 bounded below). | R:448-460 |

### L4 (M2 / early PhD)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K35 | Prop 2: optimal flow on a subspace | v* = m(Px,t) - (I-P)x/(1-t); free models leave O(1) divergence because a bounded net cannot represent the 1/(1-t) contraction (Remark 3.6). | R:345-386 |
| K36 | Prop 3: penalty and Jensen gap | Penalty on end-of-path prediction is unbiased for linear constraints, biased for nonlinear ones. | R:389-395 |
| K37 | Remark 3.7: identities don't fix polarity weights | Any mixture p mu+ + (1-p) mu- is invariant, so symmetry must be imposed separately. | R:415-417 |
| K38 | Stationarity loss (Def 3.9) at parameters without data | Squared mean of L phi under the generated distribution, via differentiable 8-step sampling, at random parameter values. | R:488-496; R:679-683 |
| K39 | Unbiased half-batch estimator (Example 4.2) | Square of a batch mean has expectation (Eg)^2 + Var(g)/n, which secretly enforces the per-sample constraint; product of two half-batch means is unbiased. | R:663-677 |
| K40 | Rice formula (Prop 8) | Zero-crossing frequency of the dipole from the stationary distribution and the right-hand side alone, no time integration; window estimator h, bias O(h^2), variance O(1/(Nh)). | R:510-538; R:703-709 |
| K41 | Prop 9: smooth generators blur jumps | A Lipschitz-in-lambda generator makes an error >= (J_delta - 2K delta)/2 near a jump of the distribution. | R:544-564 |
| K42 | 2D MHD budget identities | E[D] = eps_inj; cross-helicity identity; <a^2> identity, all from Ito calculus on the forced system. | R:436-442 |
| K43 | Necessary, not sufficient (Remark 3.11) | Every invariant measure (fixed points, unstable orbits) satisfies the identities; keep the data term. | R:569-571 |
| K44 | Liouville residuals: enforced vs control | Degree <= 2 monomials enforced; degree-3 monomials kept as independent control. | R:434; R:727 |

### L5 (supervisors / specialists)

| ID | Concept | Plain-language line | Source |
|---|---|---|---|
| K45 | Vector potential in a bounded domain | Coulomb gauge, A.n = 0 or A x n = 0 (Amrouche-Seloula); gauge must be fixed for a well-defined distribution. | R:339; T:211-260 |
| K46 | Permeability jumps: interface kink | B.n continuous, tangential B/mu_r continuous, forcing a kink in the potential (Prop 2.6). | T:115; T:272 |
| K47 | Vacuum matching is nonlocal linear | Matching to an exterior potential field without solving a Laplace problem per sample. | T:114; T:259 |
| K48 | Poloidal-toroidal decomposition | Two scalars per field in a triply periodic box (Prop 2.8); storage choice for tier 2. | T:324; T:912 |
| K49 | SFEMaNS hybrid representation | Azimuthal Fourier modes x meridian finite elements; divergence of B controlled only weakly. | T:341; R:1185 |
| K50 | Joint state-parameter equivariance R_pi | With asymmetric forcing, R_pi also flips the asymmetry parameter (Prop 2.24). | T:613; R:1187 |
| K51 | Thresholds bound reversal rate | r <= nu_a (Prop 2.30); waiting times not determined by the one-time law (Prop 2.32); plateau conjecture 2.33. | T:683-727 |
| K52 | Supercritical sqrt bound, branch conditioning | Prop 2.36; Conjecture 2.38 (conditioning on the branch removes the bound). | T:768-788 |
| K53 | Polynomial identities characterization | Conjecture 2.17 (hypoellipticity, Echeverria core, moment determinacy). | T:494 |
| K54 | Downstream: reduced drift and assimilation | Reduced drift by conditional expectation on snapshots (Prop 2.40); posterior bimodal in +-B (Prop 2.41). | T:816-831 |
| K55 | Consistency and variance of the conditional loss | Props 2.19-2.20. | T:516-537 |
| K56 | 3D MHD identities under white forcing | Corollary 2.14. | T:451 |
| K57 | Topology metrics | X-points of a (Poincare-Hopf on the torus), persistent homology, null points. | T:872-876 |
| K58 | Kazantsev slope, intermittency | k^{3/2} magnetic spectrum in the linear phase; kurtosis-skewness relation. | T:868-871 |
| K59 | Infrastructure | MFF (The Well HDF5 + milady_* metadata), relational catalog, one-command VM, Slurm. | C:107-149 |

---

## 2. Key quantitative results

### 2.1 Project and context facts

| Fact | Value | Source |
|---|---|---|
| ANR reference, committee | ANR-25-CE51-0077, CE51 | S:57-58 |
| Funding, start, duration | EUR 560,612; January 2026; 48 months | S:61-62 |
| Coordination, partners | C. Nore (LISN); LISN, Lagrange (OCA), CEREA (ENPC) | S:59-60 |
| Two objectives | (i) reversals and burst dynamos via ROMs (precursor, reversal, recovery); (ii) optimize DRESDYN with parametric ROMs (precession/rotation ratio) | S:70-78 |
| Internship | 5-6 months from spring 2027, CEREA; supervised by S. Cheng and D. Lucor, with C. Nore and Y. Ponty | H:72 |
| VKS threshold sensitivity | Rm_c = 90 +- 5 (pseudo-vacuum) vs 130 +- 10 (vacuum) at Re = 1.5e3, mu_r = 50 | R:90; R:143 |
| Bousquet et al. 2026 reference simulation | Re = 1594, Rm = 531, asymmetry 0.058, mu_r = 16, POD on 2000 snapshots, DQVU model | S:98; T:933 |
| Preparation pathway | 8 modules, about 215 h, 122 exercises; 25 in-module interactive diagrams + 6 cross-cutting | H:52, H:56; P:40-60 |
| Report content | 9 proven statements (8 propositions + 1 corollary), 3 experiments | H:53 |

### 2.2 E1: Gissinger reversal model (dimension 3)

**Setup.** mu = 0.119, nu = 0.1; Gamma train {0.80, 0.82, ..., 1.00} (11), test {0.81, ..., 0.99} (10); RK4 dt = 0.01,
transient 300, keep 3000 time units, one snapshot every 2 units (1500 per trajectory); 16 trajectories per Gamma
(24,000 snapshots); reference 32 symmetrized trajectories per Gamma; fine grid 41 values step 0.005; MLP 256 x 4;
12,000 iterations (C short: 1200); seeds 0 and 1; 10,000 generated samples per Gamma; Heun 50 steps; Rice window
h = 0.2. Sources: R:784-801; D:5. Total last run 3350 s (D:123; R:885).

**Reversal threshold.** No zero crossings up to Gamma = 0.86; 0.00194 per unit time at 0.865; about 0.011 at
Gamma = 1 (R:871; D:93-94, D:121). Threshold between 0.86 and 0.865, between training values 0.86 and 0.88.
Training-data polarity imbalance: P(D>0) = 0.375 at 0.80 (6/16), 0.3125 at 0.86 (5/16) (R:871; D:55-61).

**Table 1 (test Gamma, mean of 2 seeds)** R:834-853 (also D:10-26; D gives sigma(dE/dt) in absolute units, reference 0.3777, D:49):

| Variant | energy dist. | SW1 | asym. | Liouville <=2 | Liouville 3 | sigma ratio | Rice err. | ESS/N |
|---|---|---|---|---|---|---|---|---|
| A baseline | 0.0118 | 0.0644 | 0.0322 | 0.0326 | 0.0167 | 1.02 | 0.00125 | - |
| B augmentation | 0.00356 | 0.0423 | 0.0157 | 0.0440 | 0.0223 | 1.03 | 0.00108 | - |
| C equivariant | 0.00257 | 0.0333 | 0.00439 | 0.0265 | 0.0217 | 1.02 | 0.00106 | - |
| C short | 0.00430 | 0.0460 | 0.00444 | 0.0322 | 0.0292 | 1.34 | 0.00316 | - |
| F: C + stat. loss | 0.00310 | 0.0451 | 0.00344 | 0.0136 | 0.0113 | 0.75 | 0.00110 | - |
| F0: C + control | 0.00345 | 0.0402 | 0.00443 | 0.0324 | 0.0224 | 1.04 | 0.00083 | - |
| F: C short + loss | 0.0785 | 0.224 | 0.00320 | 0.456 | 1.72 | 19.2 | 0.00608 | - |
| F0: C short + control | 0.00494 | 0.0514 | 0.00399 | 0.0430 | 0.0309 | 1.28 | 0.00136 | - |
| D: A + tilting | 0.0879 | 0.109 | 0.0499 | 0.151 | 0.147 | 1.05 | 0.00083 | 0.91 |
| D: C + tilting | 0.00483 | 0.0503 | 0.0119 | 0.0448 | 0.0586 | 1.20 | 0.00155 | 0.85 |
| D: C short + tilting | 1.54 | 0.510 | 0.0689 | 3.41 | 6.83 | 2.43 | 0.00368 | 0.62 |
| E: C + per-sample proj. | 0.0231 | 0.107 | 0.00434 | 0.0359 | 0.0204 | 1.1e-16 | 0.00260 | - |
| reference floors | 0.00123 | - | 0.0040 | 0.0083 | 0.0078 | 1 | 0.00036 | - |

**Headline factors.**
- Equivariance vs augmentation: energy distance 0.0118 (A) -> 0.00356 (B) -> 0.00257 (C), i.e. divided by 4.6 A->C, about 2x the floor 0.00123 (R:78, R:873; T:88).
- Asymmetry (Table 2, R:855-867): A at Gamma = 0.86 = 0.183 (data 0.1875), spills to unseen 0.85 (0.0825) and 0.87 (0.0854); B symmetric at training values (0.0028-0.0063) but not between (0.0203 at 0.81, 0.0246 at 0.85); C at floor everywhere (0.0037-0.0048) (R:873).
- Identities blind to polarity: A has the lowest degree-3 control residual (0.0167 vs 0.0223, 0.0217) (R:873).
- Per-sample projection E: sigma(dE/dt) = 4e-17; energy distance x9 (0.0231 vs 0.00257), SW1 x3 (0.107 vs 0.0333), Rice error x2.4 (0.00260 vs 0.00106) (R:881).
- Stationarity loss on good model C (test Gamma): enforced residual 0.0136 vs 0.0324 (control); control identities 0.0113 vs 0.0224 (1.5x floor 0.0078); energy distance 0.00310 vs 0.00345 (within seed spread ~0.001); cost: sigma ratio 1.04 -> 0.75 (8 vs 50 steps check: 0.77/0.82 seed 0, 0.74/0.78 seed 1). At training Gamma: 0.0139 vs 0.0227 and 0.0109 vs 0.0136, above starting model C (0.0108, 0.0095) (R:875; R:683).
- Stationarity loss on biased C short fails: seed 1 diverged (|x| ~ 18, sigma ratio 19.2); seed 0 recomputed at 4000 samples: distance 0.0196 vs 0.0140, degree-3 residual 0.118 vs 0.046 (R:877).
- Tilting improves no distribution: C distance 0.00295 -> 0.00483, degree-3 0.0238 -> 0.0586; C short collapses (1.54, ESS/N 0.62); A asymmetry worsens 0.0328 -> 0.0499; at Gamma = 0.85 (C, seed 0) ESS/N 0.67, one sample weighs 33x the mean (R:879).
- Rice formula: on the reference distribution cumulative error 4% near threshold (0.865 <= Gamma <= 0.885) and 6% above (Gamma >= 0.89). On generated C (seed 0, 20,000 samples/value): 14% for Gamma >= 0.89, pointwise mean 17%, up to 65% at 0.905 and 0.91 (0.00937 vs 0.00567 at 0.91); near threshold 42%: model 0.00030 vs 0.00194 at 0.865, overshoot 0.00500 vs 0.00340 at 0.88; onset delayed by ~0.005-0.01 in Gamma; spurious crossings below threshold <= 2e-4. Model F: 32% near threshold, 23% above, dip 0.00105 vs 0.00406 at 0.89 (R:883; fine grid D:79-121).
- Costs: A 146-366 s, B 720-756 s, C 221-282 s, C short 51-555 s, each F ~330 s, F0 15 s; equivariance doubles generation cost (0.5 s vs 0.25 s per 1000 samples) (R:885).

### 2.3 E2: forced 2D MHD conditioned on eta (dimension 880-1760)

**Setup.** Periodic [0, 2pi)^2, 32^2 grid, potentials (omega, a); nu = 8e-3, alpha = 0.02, white forcing on 2 <= |k| <= 3;
IF-RK4 + Euler-Maruyama, dt = 0.01; eps_u = 0.04479, eps_b = 0.04476, eps_a2 = 0.00726; eta train 0.004 ... 0.02263
(ratio sqrt 2, Pm 2 -> 0.35), test 0.00476, 0.00673, 0.00951, 0.01345, 0.01903; 2400 training snapshots per eta,
reference 1200; 220 independent Fourier modes, dim 880 (potentials) / 1760 (components); MLP width 1024, 6000
iterations, batch 256; 1000 samples per eta (R:911-925; D:127). Not a dynamo (R:925).

**Variants** (R:637-643): V0 free, V1 penalty (weight 10), V2 final Leray projection, V3 projected flow, V4
potentials (psi, a), V5 = V4 fine-tuned with stationarity loss (beta = 50, 600 iterations, 4 eta x 64 samples, 8 Heun
steps), V5 control (beta = 0) (R:681).

**Test eta means** (R:931-961; D:132-144):

| Variant | div u | div B | spectrum err | err E_u | err E_B | energy resid. | H_C resid. | <a^2> resid. | sigma(D) ratio | energy dist. |
|---|---|---|---|---|---|---|---|---|---|---|
| V0 free | 0.408 | 0.408 | 0.23 | 0.464 | 0.562 | 0.491 | 0.0182 | 0.543 | 0.68 | 4.31 |
| V1 penalty | 0.34 | 0.162 | 0.18 | 0.0995 | 1.68 | 0.895 | 0.00798 | 1.35 | 1.21 | 5.86 |
| V2 final proj. | 5.05e-17 | 5.00e-17 | 0.168 | 0.222 | 0.337 | 0.469 | 0.0172 | 0.421 | 0.677 | 2.61 |
| V3 projected flow | 2.03e-8 | 2.03e-8 | 0.135 | 0.0922 | 0.236 | 0.335 | 0.00595 | 0.322 | 0.565 | 1.85 |
| V4 potentials | 1.78e-17 | 1.68e-17 | 0.168 | 0.261 | 0.369 | 0.472 | 0.0169 | 0.443 | 0.672 | 2.58 |
| V5 pot. + stat. loss | 1.74e-17 | 1.62e-17 | 0.0696 | 0.0668 | 0.0621 | 0.0611 | 0.0237 | 0.0612 | 0.788 | 0.699 |
| V5 control | 1.78e-17 | 1.67e-17 | 0.165 | 0.252 | 0.355 | 0.462 | 0.0143 | 0.43 | 0.663 | 2.52 |
| data subsample (floor) | 1.52e-17 | 0 | 0.00212 | 0.00261 | 0.00248 | 0.00661 | 0.0782 | 0.0265 | 0.998 | 0.00178 |
| distributional: base (V4, half b) | 1.78e-17 | 1.69e-17 | 0.168 | 0.268 | 0.36 | 0.47 | 0.0272 | 0.438 | 0.644 | 2.62 |
| distributional: tilting | 1.76e-17 | 1.59e-17 | 0.143 | 0.098 | 0.115 | 0.193 | 0.388 | 0.143 | 0.204 | 4.15 |
| distributional: rescaling | 2.75e-17 | 2.71e-17 | 0.0804 | 0.113 | 0.188 | 8.27e-6 | 0.015 | 0.299 | 8.64e-4 | 1.1 |

Training-eta means: R:963-993; D:148-160 (honest floor energy distance 0.0304, spectrum 0.0114).

**Headline points.**
- Divergence: free 0.408 (test) / 0.459 (train); penalty 0.34 (u) and 0.162 (B); V2 ~5e-17, V4 ~1.7e-17 (double precision), V3 2.03e-8 (single precision) (R:1023-1027).
- Penalty side effect: E_B relative error 1.68, i.e. generated mean magnetic energy 2.68x the reference, above 2x at each test eta (R:1025).
- Equal exact divergence, same target (Prop 2b): train distances 1.09 / 1.12 / 1.03 (V2/V3/V4); test 2.61 / 1.85 / 2.58 (one seed, not significant) (R:1029).
- Distributional part, three-way comparison (the key L3-L4 scene):
  - **Stationarity loss (V5)**: energy distance 2.58 (V4) / 2.52 (control) -> 0.699 (about 3.6x, H:85); energy errors 26% / 37% -> 6.7% / 6.2%; spectrum error 0.165 -> 0.0696; non-enforced <a^2> residual 0.43 -> 0.0612; sigma(D) ratio rises 0.663 -> 0.788 (R:1031).
  - **Exponential tilting**: energy residual 0.47 -> 0.193, but distance 2.62 -> 4.15, sigma ratio 0.204, H_C residual 0.0272 -> 0.388; mean ESS/N 0.287 (D:162), 0.99 at eta = 0.00476, 0.002 at the three largest test eta (~1 effective sample in 500) (R:1033).
  - **Per-sample rescaling**: residual 8.27e-6, sigma ratio 8.64e-4 (1.40e-15 at train eta): dissipation becomes a Dirac (Cor 6); yet distance 1.1 vs 2.62, so per-shell spectra metrics do not see the degeneracy (R:1035).
- Per-eta detail (Table 7, R:999-1013; from J2 `en_loi`, J2:1440): V4 / control / V5 distances: eta 0.01903 -> 7.74 / 7.63 / 2.22; eta 0.01345 -> 3.63 / 3.51 / 0.792; eta 0.00476 -> 0.184 / 0.178 / 0.186 (no gain where V4 is good). V4 signed energy residual +1.22 at 0.01903 (122% excess dissipation).
- Cross-helicity residual is noise-dominated (floor 0.0782 > models 0.006-0.024) (R:1037).
- Timings: V0 1200 s, V1 1059 s, V3 424 s, V4 305 s training; V5 fine-tune 460 s, control 79 s; generation 4.5-19 ms per sample; total 4023 s (~67 min) (D:164-166; R:753).
- Earlier U-Net attempt: ~0.3 s per training step on CPU, abandoned (X:101).

### 2.4 E3: ABC kinematic dynamo (3D, 32^3)

**Setup.** dB/dt = curl(u x B) + eta Lap B, u = ABC with A = B = C = 1, Rm = 1/eta; pseudo-spectral 32^3, 2/3 rule,
IF-RK4 dt = 0.05 over 150 time units; curl form keeps k.B = 0; renormalize every 20 iterations; lambda = slope of
ln||B|| over second half, lambda_q over last quarter; 24 Rm values from 2 to 30; checks at N = 48 (R:1060-1066).

**Growth rates** (R:1070-1097; D:170-195; J3:11-156):

| Rm | 2 | 4 | 6 | 8 | 8.5 | 9 | 9.5 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lambda | -0.5001 | -0.1511 | -0.04598 | -0.007649 | -0.002755 | 9.61e-4 | 0.003694 | 0.00557 | 0.007483 | 0.007653 | 0.007328 | 0.006042 |

| Rm | 15 | 16 | 17 | 17.5 | 18 | 19 | 20 | 22 | 24 | 26 | 28 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lambda | 0.004152 | 0.002858 | 0.001394 | 2.34e-4 | -9.07e-4 | -0.002205 | -0.003185 | -0.004749 | -0.005743 | -0.002578 | 0.003897 | 0.01043 |

- Interpolated thresholds 8.87, 17.6, 26.8 (D:198; J3:167-171: 8.8707, 17.6025, 26.7963) vs published 8.9, 17.5, ~27 (Galloway & Frisch 1984 via Archontis et al. 2003) (R:1112).
- N = 48 checks: lambda = 0.00812 at Rm = 12; -5.2e-4 at Rm = 17.5 (D:197). Sign at 17.5 unresolved (+2.3e-4 / -2.2e-4 / -5.2e-4); third threshold known to ~1 unit (R:1114).
- Maximum ~0.00765 at Rm = 12 (lambda_q 0.00816 at 13) (R:1112).
- Exact test: B = u is an eigenmode with rate -1/Rm; measured -0.5001 at Rm = 2 (R:1116).
- Relative divergence 3e-19 to 1.52e-16 (R:1118). Cost 1366 s (~23 min) (D:199).
- Symmetry group of 24 elements; first-window mode has all even symmetries (Bouya & Dormy 2013) (R:1120).

### 2.5 Discussion-level syntheses (for the "what we learned" scene)

- Mechanism summary table: R:1149-1158 (potentials, final projection, projected flow, penalty, equivariance, stationarity loss, tilting, per-sample projection; class, where it acts, exactness, cost, effect).
- Answers to P1-P5: R:1135-1143. Five evaluation lessons: R:1141.
- Central thesis sentence: "a constraint must be enforced where it is true" (R:1199).
- Six claimed contributions with closest prior work: R:118-125, R:1164-1171.
- Threats to validity: R:1175-1179. What is missing for MilaDy data: R:1183-1195.
- Six open questions to supervisors: R:1209-1214. Internship roadmap months 1-6: R:1220-1226.

### 2.6 PhD proposal plan

**Title**: Conditional generative models with hard and distributional physical constraints for turbulent dynamos (T:44); 36 months, working assumption start fall 2027 (T:49).

**Why this direction** (S:418-453): six candidate directions A-F scored on 7 weighted criteria; A 4.10, B 3.90, F 3.50, E 3.40, D 3.20, C 3.00 (S:420-428); A and B first under all 3 weightings (S:431); merged A + B selected (S:443-453).

**Research questions**: Q1 hard constraints in 3D bounded geometry; Q2 distributional constraints for field PDEs; Q3 dynamo threshold and reversals; Q4 downstream uses (ROM, assimilation) (T:111-136).

**Three axes**: axis 1 3D hard constraints (blue), axis 2 distributional constraints and symmetries (orange), axis 3 threshold and reversals (green) (T:857 caption).

**Test-bench ladder (tiers)**:

| Tier | Content | Key numbers | Success criteria (abridged) | Source |
|---|---|---|---|---|
| 0 | Gissinger + DQVU reduced reversal models | up to 1e6 snapshots per parameter; CPU | asymmetry below floor at all Gamma; non-enforced residuals /2 vs control at Gamma without data; Rice within 20%; Prop 2.30 bound tight within 30% | T:878-890 |
| 1 | periodic 2D MHD | 128^2 (subset 256^2); 8 x 8 (nu, eta) log grid; 1e4 snapshots per point; ~37 GB + ~38 GB | div < 1e-12; budget residual < 5% at parameters without data (E2: 6.1%); energy distance /2; sigma(D) ratio 0.8-1.2 | T:892-904 |
| 2 | periodic 3D dynamos (ABC, Taylor-Green) | 64^3 (subset 128^3); ~20 parameter points; 5000 snapshots per point; ~1.3 MB per snapshot, ~130 GB; TG thresholds Rm_c = 30 at Pm = 1, 226 at Pm = 0.3 (Ponty et al. 2005) | div < 1e-12; log-spectrum error < 0.1 decade; Rm_c within 10% at Pm without data; error at threshold /2 with branch conditioning | T:906-918 |
| 3 | VKS cylinder (SFEMaNS, LATU) | non-public data; 384^3 snapshot ~1.4 GB, 2000 snapshots ~2.7 TB; filtered 128^3 ~50 MB, ~100 GB | 4 POD energy fractions within 10%; (D, Q) energy distance < 2x floor; interface residual < 1%; Rice in 95% Poisson CI | T:927-939 |
| 4 | DRESDYN precession | SFEMaNS precessing cylinder, few Po values | Rm_c within 10% and correct symmetry class at Po without data | T:941-953 |

**Budget** (T:955-974): A100-class GPU hours: tier 0 ~0, tier 1 ~700, tier 2 ~3900, tier 3 ~3200, tier 4 ~1200; total ~1.1e4 with 20% reserve; CPU simulations ~2e4 h and more; anchor point PCDM ~1150 GPU h (T:959); uncertainty at least x2.

**Risks** (T:988-1000): e.g. late data access (medium/high), stationarity-loss variance in 3D (high/medium), too few reversals for Rice (high/medium), funding beyond MilaDy end (to be clarified/high).

**Papers** (T:1014-1020): (1) distributional constraints, axis 2, month 10; (2) hard constraints in bounded domains, axis 1, month 22; (3) reversals and threshold from a snapshot generator, axis 3, month 33. Possible benchmark paper (NeurIPS D&B).

**Schedule** (T:1042-1055; SVG timeline T:1059-1126): tier 0 m1-6, tier 1 m1-9, tier 2 m6-20, tier 3 m15-33, tier 4 m24-34, writing m31-36; visits OCA m8-9, LISN m15-17; committees m12, m24; code releases m16, m30; defense m36.

**Toolbox modules** (T:1026-1034): data, constraints, losses, sampling, metrics, rom, da.

### 2.7 Infrastructure numbers (for the "how it scales" scene)

| Fact | Value | Source |
|---|---|---|
| Automated tests | 68 tests pass (66 passed + 1 skipped with PostgreSQL/MinIO, anchor test added since) | C:45; IR:387 |
| One-command VM install (CPU, Docker present) | 3 min (33 s rerun) | C:66; IR:71-72, IR:401-402 |
| Laptop setup / smoke test | 68 s / 4 s | C:80; IR:366-367 |
| Solver step, 64^3 dynamic, CPU 2 threads | 0.08 s (bench: 0.073-0.083 s float32) | C:153; `milady/sim/mhd3d.py`:75-90 |
| Kinematic 64^3 | 0.031 s/step (2 threads) | `milady/sim/mhd3d.py`:85-86 |
| Memory | state 6 N^3 x 4 bytes; peak ~15 states; ~6 GB at 256^3, ~48 GB at 512^3 | C:176; IR:258-262 |
| Pipeline stages | campaign -> launch -> simulation -> storage -> dataset -> training -> evaluation | C:88-96 |
| Not yet run | any GPU, real Slurm, Apptainer, rented VM, full-size campaigns | C:190; IR:429-453 |

---

## 3. Reusable assets

### 3.1 Schematic figures (publication-quality, vector sources available)

All at `figures/<name>/figure/out/<name>-en.{png,svg,pdf}` (+ `-en-thumb.png`; panel crops `<name>_a.png`/`_b.png` exist only for the French version).

| Path (-en.png) | px | Shows | Best video use |
|---|---|---|---|
| `figures/cadre/figure/out/cadre-en.png` | 4325x1706 | Framework in 5 panels: latent flow to symmetric bimodal law (a), potential decoder (b), VKS geometry (c), distributional control of dissipation (d), downstream uses incl. Rice (e) | Opening map and closing recap (L3-L5) |
| `figures/taxonomie/figure/out/taxonomie-en.png` | 4325x1894 | Four constraint classes C1-C4 with mechanisms; three dE/dt distributions (true, per-sample Dirac, tilted) | Central "true for each vs true on average" scene |
| `figures/flow-matching/figure/out/flow-matching-en.png` | 3219x2906 | Straight conditional paths, marginal field as average, conditioning on two parameter values, Heun in 4 steps | Flow matching chapter (L3) |
| `figures/vks/figure/out/vks-en.png` | 4325x2788 | VKS cylinder, mean flow (blue), dipole (vermillion), qualitative D(t) with reversals and excursion, (D, Q) plane | L0 hook and tier 3 placeholder |
| `figures/simulations/figure/out/simulations-en.png` | 4325x2363 | E1/E2/E3 on one template: system, scheme, parameter sweep and response, data kept, pipeline place (E2 response recomputed) | Overview of the three test benches |
| `figures/plan-these/figure/out/plan-these-en.png` | 4325x2838 | Tier staircase 0-4, three axes, toolbox and outlets, 36-month timeline | PhD plan chapter (L5) |
| `figures/architecture/figure/out/architecture-en.png` | 4325x2756 | 7-stage pipeline with catalog and storage bands; laptop / VM / Slurm | Infrastructure scene |
| `figures/solveur/figure/out/solveur-en.png` | 4325x2600 | One pseudo-spectral MHD step (Fourier <-> physical), simulation timeline with checkpoints, MFF tree linked to catalog | Solver / data scene |

The SVG versions can be split into layers for progressive reveal (vector, same colour key).

### 3.2 Result plots (measured data)

`experiences/figures/<name>-en.{png,svg}`. The `_quick` variants come from `--quick` runs: do not use their numbers.

| Path | px | Shows |
|---|---|---|
| `experiences/figures/e1_seuil-en.png` | 1720x660 | Zero-crossing frequency vs Gamma (simulation, Rice on reference, Rice on C and F) and bridge mass P(|D| < 0.25) |
| `experiences/figures/e1_variantes-en.png` | 2480x780 | Four bar charts per variant at test Gamma: energy distance, degree-3 Liouville residual, asymmetry, sigma(dE/dt) ratio, with floors |
| `experiences/figures/e1_symetrie_projection-en.png` | 2000x660 | dE/dt density at Gamma = 0.93 (projection collapses to 0); (Q, D) clouds at Gamma = 0.85 for A (asymmetric) and C |
| `experiences/figures/e2_mecanismes-en.png` | 2100x720 | Divergence, spectrum error, energy residual for V0-V5, control, data (log bars) |
| `experiences/figures/e2_spectres-en.png` | 1720x660 | Mean E_u(k), E_B(k) at eta = 0.00951: reference, V0, V4 |
| `experiences/figures/e2_en_loi-en.png` | 2000x680 | Residual, sigma(D) ratio, energy distance for V4 base, tilting, rescaling, V5 |
| `experiences/figures/e3_abc-en.png` | 1120x660 | lambda(Rm) at 32^3 with 48^3 checks, dynamo windows, thresholds |
| `experiences/figures/e1_*_quick-en.png` (3) | | quick-run versions (development only) |

Generator: `experiences/figures.py` (FR and EN). For the video, re-plot from the data (section 3.5) in the
site colour key rather than embedding raster plots, so values can be animated.

### 3.3 Preparation-module figures (EN)

| Path | Shows |
|---|---|
| `prep/p1-calcul-vectoriel/fig-monopole-dipole-en.png` | Field lines of a point charge vs a magnetic dipole |
| `prep/p1-calcul-vectoriel/fig-fourier-en.png` | Aliasing, Gibbs phenomenon, spectral convergence |
| `prep/p1-calcul-vectoriel/fig-helmholtz-en.png` | Helmholtz-Hodge decomposition on the torus |
| `prep/p1-calcul-vectoriel/fig-courant-en.png` | Velocity from a stream function |
| `prep/p1-calcul-vectoriel/fig-champs-en.png` | Vector fields (chapter 1) |
| `prep/p2-mecanique-fluides/ecoulements-en.png` | Reference flows (Poiseuille, 2D Taylor-Green, ...) |
| `prep/p2-mecanique-fluides/lagrange-en.png` | Material blob advected in Taylor-Green cells |
| `prep/p2-mecanique-fluides/cascade-en.png` | Model turbulence spectrum (Pope 2000) and cascade |
| `prep/p2-mecanique-fluides/kolmogorov64-en.png` | 2D Kolmogorov flow at Re = 40 on 64^2 |
| `prep/p3-mhd-dynamo/figures/expulsion-en.png` | Flux expulsion in cellular flow for Rm = 10, 40, 160 |
| `prep/p3-mhd-dynamo/figures/modes-sphere-en.png` | Free decay dipole mode of a sphere under 3 boundary conditions |
| `prep/p3-mhd-dynamo/figures/alpha2-en.png` | Mean-field alpha^2 dynamo growth rates |
| `prep/p3-mhd-dynamo/figures/vks-en.png` | VKS meridional cross-section (published dimensions) |
| `prep/p3-mhd-dynamo/figures/gissinger-en.png` | Gissinger D(t) at Gamma = 0.86 (no reversal) and 0.90 (reversals) |
| `prep/p4-systemes-dynamiques/figures/gissinger-en.png` | Gissinger on either side of the crisis, symmetric initial conditions |
| `prep/p4-systemes-dynamiques/figures/bifurcations-en.png` | Four normal-form bifurcation diagrams |
| `prep/p4-systemes-dynamiques/figures/lorenz-en.png` | Lorenz attractor (chaos intuition) |
| `prep/p4-systemes-dynamiques/figures/kramers-en.png` | Noisy double well, rare transitions |
| `prep/p5-probabilites-transport/fig-mesure-image-en.png` | Pushforward of a Gaussian (sinh) |
| `prep/p5-probabilites-transport/fig-inclinaison-en.png` | Exponential tilting of a bimodal density |
| `prep/p5-probabilites-transport/fig-flot-continuite-en.png`, `fig-monte-carlo-en.png`, `fig-ornstein-uhlenbeck-en.png`, `fig-wasserstein-1d-en.png` | Continuity equation flow, Monte Carlo error, OU process, 1D Wasserstein |
| `prep/p6-apprentissage-profond/fig-pod-fourier-en.png` | POD eigenvalues of a homogeneous field = spectrum |
| `prep/p6-apprentissage-profond/fig-pod-ae-en.png` | POD vs autoencoder on an advected pulse |
| `prep/p6-apprentissage-profond/fig-unet-equiv-en.png` | U-Net translation equivariance error |
| `prep/p7-modeles-generatifs/fig-bruitage-en.png` | DDPM forward noising of a 4-Gaussian mixture |
| `prep/p7-modeles-generatifs/fig-chemins-en.png` | Linear probability path noise -> mixture |
| `prep/p7-modeles-generatifs/fig-fm-conditionnel-en.png` | Conditional flow matching: data vs Heun samples for 4 parameter values |
| `prep/p8-contraintes-physiques/fig-mecanismes-divergence-en.png` | Divergence mechanisms toy comparison (1 seed, 1000 iterations) |
| `prep/p8-contraintes-physiques/fig-inclinaison-en.png` | Double well: hot model and its tilted correction |

### 3.4 Interactive widgets (self-contained JS, formulas in file headers)

Cross-cutting widgets in `assets/interactif/` (each mounts on `<div class="widget" data-widget="NAME">`):

| Script | What it computes / shows | Reuse for a scene |
|---|---|---|
| `flow-matching.js` | Exact marginal field for a two-Gaussian target +-m(lambda); straight conditional paths vs curved marginal trajectories; slider lambda | Port to a recorded scene for K26/K30 (symmetry by construction) |
| `leray.js` | Random periodic 2D field u = v + alpha grad phi; colour map of div u; Leray projection | K19 scene |
| `contrainte-loi.js` | Exact distribution of r = dE/dt (mixture with mean exactly 0); per-sample projection vs exponential tilting; "missing support" toggle and ESS collapse | K32/K34 scene |
| `gissinger.js` | Integrates Gissinger in the browser (mu = 0.119, nu = 0.1, Gamma 0.80-1.00 step 0.005); symmetry button; zero-crossing count vs Rice estimate from visited states | E1 hook and Rice scene |
| `abc-dynamo.js` (+ `assets/interactif/data/abc-dynamo.json`) | lambda(Rm) curve with windows; z = 0 slice of |B| and (Bx, By) of the dominant mode at Rm 8, 12, 16, 20 | E3 scene |
| `architecture.js` | 7-stage pipeline on three targets with commands | Infrastructure scene |

Module widgets (25 in total, P:93): `prep/p3-mhd-dynamo/widgets.js` (flux expulsion, alpha^2, Gissinger), `prep/p4-systemes-dynamiques/widgets.js` (bifurcations, Kramers, Gissinger), `prep/p5-probabilites-transport/widgets.js` (pushforward, OU, flow, tilt, Wasserstein), `prep/p7-modeles-generatifs/chemin-widget.js` (probability paths); others are inline SVG/canvas in the module pages.

### 3.5 Data files that can drive animations directly

| File | Content | Scenes it can drive |
|---|---|---|
| `experiences/resultats/digest.md` | All tables of E1-E3 (French labels) | Number cards, bar races |
| `experiences/resultats/e1_gissinger.json` (15,219 lines) | `config`; `donnees` per Gamma (sim crossing rates, P(D>0)); `entrainement` (times); `grille_fine` (line 315, 41 Gamma: sim rate, Rice ref/C/F, bridge masses); `evaluation` per variant per Gamma per seed (line 850); `resume` (line 14865) | Threshold curve build-up, per-Gamma asymmetry animation |
| `experiences/resultats/e1_echantillons.npz` | (Q, D, V) samples, 4000 per variant, Gamma in {0.85, 0.87, 0.90, 0.93}; ref 8000; C_grand 8000 at 0.85/0.90 | Point-cloud morphs (A vs C symmetry, projection collapse) |
| `experiences/resultats/cache_e1/e1_echantillons_complet.npz` (local, gitignored, 32 MB) | Same variants at all 21 Gamma values 0.80-1.00 (338 arrays) | Sweep animation of the generated law across the threshold |
| `experiences/resultats/cache_e1/sim_{train,ref,fine}.pkl` (local, gitignored) | Per-Gamma snapshot arrays x (24,000 or 48,000 x 3), crossing rate, P(D>0) | Training data clouds; true D(t) better re-integrated in JS (gissinger.js) |
| `experiences/resultats/e2_mhd2d.json` (2294 lines) | `config`; `variantes` (times); `evaluation` per variant per eta (line 70); `en_loi` per eta: base / tilting / rescaling metrics, ESS, lambdas (line 1440); `resume` (line 2003) | Per-eta bars (Table 7), ESS collapse |
| `experiences/resultats/e2_echantillons.npz` | 8 samples x 4 components (u_x, u_y, B_x, B_y) x 220 complex Fourier coefficients at eta = 0.00951, for V0-V5 and ref; `kx`, `ky` | Reconstruct real 32^2 maps of u, B, div u (V0 vs V4) and spectra |
| `experiences/resultats/e3_abc.json` | 24 rates (Rm, lambda, lambda last quarter, div), N48 checks, thresholds | lambda(Rm) curve drawn live |
| `experiences/resultats/e3_modes.npz` | Dominant 3D eigenmode B (3, 32, 32, 32) at Rm 8, 12, 16, 20 | Volume / isosurface rendering in Three.js |
| `assets/interactif/data/abc-dynamo.json` | Rates, thresholds, reference thresholds, z = 0 slices (|B|, Bx, By normalized) at Rm 8, 12, 16, 20 | Ready-to-use 2D slices |
| `experiences/resultats/*_quick.*` | Quick-run outputs (gitignored) | Development only |

Not present locally: `experiences/donnees_e2/` (E2 raw snapshot data, gitignored; ~30 min to regenerate with `e2_donnees.py`, X:69), `/data/` (no catalog or MFF files exist yet).

### 3.6 Other ready material

- Thesis timeline as inline SVG (T:1059-1126): bars per tier, visits, milestones; directly animatable.
- Mechanism summary table R:1149-1158 and positioning table R:1164-1171 (end-of-video recap cards).
- Equations, all in KaTeX-ready LaTeX in R and T (definitions 3.1-3.3, propositions 1-9).

---

## 4. Missing results (regenerable sections)

Contract proposed for every regenerable section: the scene reads one small derived JSON
(`video_plan/data/<scene>.json`) produced by a converter from the upstream artefact (MFF file, eval JSON or
catalog query). Each scene ships with a provisional dataset (flagged "provisional" on screen) and is re-rendered
when the upstream file changes. Narration for these sections should state only qualitative expectations plus
whatever the provisional data supports, with numbers injected from the JSON.

Upstream formats (from the code):
- **MFF** `{storage}/{campaign}/{uuid}/fields.h5` (C:93, C:109-124; `specs/format-donnees.md`): `t1_fields/velocity`, `t1_fields/magnetic_field` float32 `(n_traj, T, nx, ny[, nz], D)`; `milady_diagnostics/` time series (`kinetic_energy`, `magnetic_energy`, `kinetic_dissipation`, `magnetic_dissipation`, `injection`, `kinetic_helicity`, `magnetic_helicity`, `cross_helicity`, `max_div_u`, `max_div_b`, `growth_rate`, `magnetic_production`, `u_rms`, `b_rms`, `log_b_rms`; 2D: `enstrophy`, `mean_square_current`, `dissipation`); optional `milady_spectral/`; scalars = physical parameters.
- **Catalog** tables `campaign`, `simulation`, `file`, `diagnostic`, `dataset`, `dataset_member`, `model`, `evaluation`, `job`; view `v_eval_summary` (mean, std, n_runs per model x metric x parameters) (C:130-139; `milady/catalog/models.py`:364-375). CLI `python -m milady.catalog sims|summary`.
- **Evaluation JSON** (`python -m milady.eval ... --out <file>`; `milady/eval/metrics.py`:894-907): `{model, model_id, created, results: [{point, physical_parameters, metrics, details, seconds}]}` with metrics `div_rel_u`, `div_rel_b`, `kinetic_energy_mean`, `magnetic_energy_mean`, `*_helicity_mean`, `relative_*_helicity_mean`, `residu_bilan_total`, `residu_bilan_cinetique`, `residu_bilan_magnetique`, `err_spectre_u_log10`, `err_spectre_b_log10`, `err_Eu_rel`, `err_Eb_rel`, `dist_energie`, `wasserstein_tranche`, `plancher_dist_energie`; details `spectrum_u`, `spectrum_b`, `spectrum_u_ref`, `spectrum_b_ref`, `n_gen`, `n_ref`, `feature_names` (`milady/eval/metrics.py`:588-662). Gap: the per-sample spread sigma(dissipation)/sigma_ref, needed for the Corollary 6 scene, is **not** computed by the 3D evaluation (C:166).

CPU reference timings used below: kinematic 64^3 0.031 s/step, dynamic 64^3 0.073-0.083 s/step, dynamic 32^3
0.011-0.015 s/step, kinematic 32^3 0.0043 s/step, 2 threads, 1 trajectory (`milady/sim/mhd3d.py`:75-90; beware
oversubscription, same block lines 89-90).

### M1. Tier 1 campaign `palier1_mhd2d` (2D MHD through the infrastructure)

- **Video**: "the data factory": ensembles of 2D (u, B) maps across 11 eta values, energy and dissipation time series, injection vs dissipation fluctuating around equality (K20 visual proof on real data).
- **Producer**: `infra/configs/palier1_mhd2d.yaml` (11 eta, 16 trajectories, 150 snapshots, 32^2, CPU NumPy solver `experiences/mhd2d.py`), `make sweep CONFIG=...`.
- **Expected data**: 11 MFF files with `t1_fields/velocity`, `magnetic_field` float32 (16, 150, 32, 32, 2) and 2D diagnostics (format spec example, `specs/format-donnees.md`:72-80); catalog rows `simulation`, `file`, `diagnostic`. Derived scene JSON: per-eta snapshot thumbnails + energy/dissipation series.
- **Provisional CPU run**: yes, this is already the full config (gpus: 0, 2 CPUs, 2 h limit, CFG palier1_mhd2d.yaml:10, 37-42). Same workload as E2 data generation, ~30 min (X:69). Immediate substitute today: `e2_echantillons.npz` (8 samples at eta = 0.00951 only).

### M2. Tier 1 at full scale (128^2, 8 x 8 (nu, eta) grid, field architectures)

- **Video**: U-Net / functional-autoencoder generator vs E2 perceptron; budget residual at parameters without data (target < 5%), sigma(D) ratio within 0.8-1.2, X-point counts.
- **Producer**: not configured; T:898-904; ~700 GPU h (T:968); ~37 GB data.
- **Expected data**: MFF 2D at 128^2 (+ subset 256^2); eval JSON per (nu, eta) point; catalog.
- **Provisional**: only via M1 + E2 results (32^2 perceptron). Mark section as "planned".

### M3. Tier 2 campaign `palier2_abc3d` (ABC kinematic dynamo at 64^3, Rm 4-40)

- **Video**: lambda(Rm) extended to Rm = 40 at 64^3 and 3D eigenmodes B(x; Rm) rendered in volume on both sides of each threshold; growth curves ln||B||(t).
- **Producer**: `infra/configs/palier2_abc3d.yaml` (37 simulations, 2 seeds each, t_burn 150 + t_keep 100, 20 snapshots, 64^3, `milady.sim.mhd3d` kinematic), `make sweep` or Slurm array.
- **Expected data**: 37 MFF files, `t1_fields/magnetic_field` (2, 20, 64, 64, 64, 3) (+ constant velocity unless removed, CFG:58); diagnostics incl. `log_b_rms`, `growth_rate`; catalog diagnostic `growth_rate_fit` (CFG palier2_abc3d.yaml:6-8). Query: `python -m milady.catalog sims --campaign palier2_abc3d --param Rm__gt=8` (C:149). Derived JSON: (Rm, lambda) table + downsampled mode volumes.
- **Provisional CPU**: yes. Already available: E3 at 32^3 (Rm 2-30) + `e3_modes.npz` (Rm 8, 12, 16, 20). **Estimate** for the full config on CPU: 250 time units / CFL step ~0.01 (CFG:12) = 25,000 steps x 0.03 s x 2 trajectories ~ 25 min per simulation, ~15 h for 37 (2 threads, serial). **Estimate** at 32^3 (override N): ~2 min per simulation, ~1-1.5 h total (E3, same physics at 32^3, took 23 min for 24 Rm values with a larger IF step, D:199).

### M4. Tier 2 campaign `palier2_tg3d` (Taylor-Green dynamic MHD at 64^3)

- **Video**: a weak seed field (rms 1e-3) grows exponentially then saturates (dynamo onset as a function of Rm = Re x Pm); 3D field renderings; spectra E_u(k), E_B(k); this is the first true dynamo of the ladder (T:908).
- **Producer**: `infra/configs/palier2_tg3d.yaml` (Re in {25, 50, 100, 200} x Pm in {0.5, 1, 2} = 12 simulations, 64^3, t_burn 100 + t_keep 40, 40 snapshots, GPU, 10 h limit each).
- **Expected data**: 12 MFF files, `velocity` and `magnetic_field` (1, 40, 64, 64, 64, 3); diagnostics (energies, dissipations, injection, helicities, max divergences, growth_rate, magnetic_production, u_rms, b_rms, log_b_rms); catalog `growth_rate_fit`. Derived JSON: E_B(t) curves per (Re, Pm), fitted growth rates, dynamo / no-dynamo map, mean spectra.
- **Provisional CPU**: partial. **Estimate**: 140 time units at dt <= 0.005 = 28,000+ steps x ~0.08 s ~ 40 min per simulation at 64^3, ~8 h for 12 (more if CFL shrinks dt); at 32^3 ~5-7 min each, ~1-1.5 h total, but Re = 200, Pm = 2 (Rm = 400) may be under-resolved even at 64^3 (CFG palier2_tg3d.yaml:12-14). Recommended provisional subset: 32^3 or 64^3 with Re <= 100. Do not compare provisional thresholds to published TG values without matching forcing conventions.

### M5. 3D generative training `milady.train.fm3d` (`train_fm3d.yaml`)

- **Video**: generated 3D (u, B) at the held-out point (Re = 50, Pm = 2) next to the simulation; divergence at machine precision by construction (vector potentials, Coulomb gauge, |m| <= 8); exact B -> -B symmetry; loss curves.
- **Producer**: `infra/configs/train_fm3d.yaml` (MLP 1024 x 6 ~30 M parameters, 8432 dimensions at kmax = 8, 200 epochs, batch 64, EMA; val {Re 100, Pm 1}, test {Re 50, Pm 2}; CFG:18-21, 30-39, 54-77), `make train`.
- **Expected data**: checkpoints `{models_uri}/fm3d_tg3d/{run}/last.pt`, `final.pt`; MLflow run (loss curves, hyperparameters); catalog `model` row; quick eval after training (CFG:131-142). Derived JSON: loss curve, sampled fields downsampled for rendering.
- **Provisional CPU**: smoke level only: 6 iterations with kmax = 3 verified in 5 s (IR:370); time per iteration at kmax = 8 not measured, to be measured with `--set train.iters=200` (CFG:19-20). A CPU run at kmax 3-4 can illustrate the mechanism (exact divergence, symmetry), not quality. Depends on M4 data.

### M6. 3D evaluation `milady.eval` (metrics table for M5/M7)

- **Video**: 3D counterpart of the E2 bar charts: divergence, spectrum error, energy-budget residual, energy distance vs floor, per (Re, Pm) point, train / val / test.
- **Producer**: `make eval CONFIG=infra/configs/train_fm3d.yaml [MODEL=uuid]`, with `--out eval.json` (IR:386).
- **Expected data**: evaluation JSON (schema above) + catalog `evaluation` rows + `v_eval_summary`. Missing metric to add before the Corollary 6 scene: per-sample std of the budgets (C:166).
- **Provisional**: as M5.

### M7. 3D stationarity fine-tuning (V5 in 3D)

- **Video**: same three-way story as E2 (loss vs tilting vs per-sample) in 3D: budget residual before/after, control run, spread of dissipation.
- **Producer**: command in `train_fm3d.yaml`:13-15 (`--init-from final.pt --set stationarity.enabled=true stationarity.anchor=1.0 stationarity.beta_warmup=500 train.iters=2000 ...`); safeguards motivated by E1's failure (C:166).
- **Expected data**: second model + eval JSON; compare `residu_bilan_total`, `dist_energie`; a control run with beta = 0 is needed to separate the loss from extra iterations (as in E1/E2).
- **Provisional**: no meaningful CPU version beyond smoke scale.

### M8. Rm-conditioned generator of ABC eigenmodes (vector potential)

- **Video**: a generator crossing the dynamo thresholds 8.87 / 17.6 / 26.8; Proposition 9 seen in 3D (blurring at the threshold).
- **Producer**: internship roadmap month 2 (R:1120, R:1223); no ready config: requires a `train_fm3d` variant on `palier2_abc3d` with Rm conditioning (the data layer derives Rm from eta, `milady/train/data.py`:64-99; to be verified).
- **Expected data**: model checkpoint + eval JSON per Rm; derived JSON of generated vs simulated mode statistics per Rm.
- **Provisional**: plausible at 32^3 on CPU after M3-32^3 (untested).

### M9. Tier 0 extensions (DQVU, joint R_pi equivariance, waiting times, thresholds +-a, 3 seeds)

- **Video**: Rice bound r <= nu_a and the plateau conjecture; waiting-time distributions from short trajectories launched from generated states; DQVU asymmetric bimodality of V.
- **Producer**: no code in the repository (no DQVU implementation found); plan T:884-890; CPU only (~0 GPU h, ~1e3 CPU h assumption, T:967).
- **Expected data**: E1-style JSON (per-parameter metrics, fine-grid Rice values at several levels a).
- **Provisional**: Gissinger part yes (E1 code; full run 2-3 h, resumable, X:71); DQVU needs the published coefficients (Bousquet et al. 2026 appendix).

### M10. More seeds and confidence intervals for E1 and E2; U-Net for E2

- **Video**: error bars on the key bars (equivariance factor, V5 gain), replacing "one seed" caveats.
- **Producer**: `experiences/e1_gissinger.py` (seeds fixed in code; ~2-3 h per full run, X:71, R:745), `experiences/e2_mhd2d.py` (~67 min, X:70) after `e2_donnees.py` (~30 min); `experiences/unet.py` (~30 min per variant at 6000 iterations on CPU, X:101).
- **Expected data**: same JSON schemas (J1, J2) with more seeds; `digest.md` regenerated by `digest.py`.
- **Provisional CPU**: yes (hours).

### M11. Topology and helicity metrics

- **Video**: counting X-points and O-points of the magnetic potential a in 2D (Poincare-Hopf: #saddles = #extrema on the torus), persistence diagrams of |B|.
- **Producer**: not implemented (R:739, R:1141; plan T:872-876, T:902). 3D helicities exist in `milady/eval/metrics.py` (`helicities`).
- **Expected data**: per-variant distributions of X-point counts (JSON).
- **Provisional CPU**: yes, cheaply on `e2_echantillons.npz` (8 samples per variant) or on M1 data.

### M12. Tier 2 at full scale (latent 3D models, 128^3 subset)

- **Video**: threshold Rm_c deduced from the generator within 10% at a Pm without data; branch conditioning in subcritical TG.
- **Producer**: not configured beyond M4/M5 (T:912-918); ~3900 GPU h (T:969); ~130 GB.
- **Expected data**: MFF (poloidal-toroidal storage planned), eval JSON, catalog.
- **Provisional**: none beyond M3/M4/M5 reduced runs. "Planned" section.

### M13. Tier 3: VKS data (SFEMaNS, LATU)

- **Video**: generated VKS dipoles in the cylinder; energies of the 4 dominant POD modes; (D, Q) joint distribution with bimodality and asymmetry; Rice frequency vs counted reversals; interface residuals.
- **Producer**: data non-public, through the consortium (R:1183; T:929); MFF extension `milady_fourier_fe` specified (`specs/format-donnees.md`:300-340); writer and interpolators exist, native SFEMaNS reader not implemented (`milady/data/convert.py`:9-12).
- **Expected data**: MFF `grid_type = fourier_fe_axisym` with `milady_fourier_fe/fields/velocity (B, T, M, 2, N_fluid, 3)`, `magnetic_field (B, T, M, 2, N_cond, 3)`, meshes (nodes, connectivity, region).
- **Provisional**: none with real data. Placeholders: `figures/vks` schematic, Gissinger as "pocket dynamo" proxy, qualitative D(t) from the VKS figure (normal form, no VKS values).

### M14. Tier 4: DRESDYN precession

- **Video**: Rm_c(Po) and symmetry class of the dominant mode computed on generated velocity fields.
- **Producer**: SFEMaNS precession simulations at the partners (T:947); nothing in the repository.
- **Expected data**: generated u fields + kinematic eigenvalue results per Po (format to define).
- **Provisional**: none. Use Botez et al. 2026 findings qualitatively (S:100).

### M15. GPU timings and costs

- **Video**: real cost per simulation and per training run (for the "how it scales" scene).
- **Producer**: `python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50` (IR:436); catalog SQL on `wall_time_s` (C:143-147).
- **Expected data**: bench output + catalog rows.
- **Provisional**: CPU numbers only (section 2.7).

### Priority for provisional generation (cheapest first, all CPU)

1. M11 X-points on existing E2 samples (minutes). 2. M3 at 32^3 (~1-1.5 h, estimate). 3. M1 (~30 min).
4. M4 subset at 32^3 (~1-1.5 h, estimate). 5. M5 smoke-scale training on M4 output (mechanism only).
6. M10 extra seeds (hours). Everything else is GPU or data-access bound.

---

## 5. Gaps surfaced by the inventory (inputs to ask the user about)

- Narration voice: `/home/user/videobook/BRAINSTORM.md`:49 only notes the wish for a known voice, "to be checked" in a library or by cloning; the only `reference_id` given (line 57) belongs to another person and is reserved for a book preface. No narrator `reference_id` is defined for this project.
- Fish Audio access (API key, subscription) and the drama-3 settings (BRAINSTORM.md:52-60) are documented, but no key or voice is in the repository.
- Target length and chapter split; whether to show the supervisors' names and photos (public facts in S, but the work is not endorsed by them, H:43-46).
- Whether to launch the provisional CPU runs (section 4 priority list) before scripting, and when GPU or consortium data might be available.
- Whether the "prospective report" disclaimer and the caveats of 0.3 must appear on screen.
