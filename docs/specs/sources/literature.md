# State of the art: physics-constrained generative models for PDEs (2020–2026)

## Verification summary (independent verifier, 6 November 2026)

**Method.** Each reference was reopened on a primary source, without reusing the URLs of the file as they stood:
- arXiv API for the 53 identifiers (title, authors, dates, comment, journal-ref);
- Crossref API for the 21 DOIs;
- proceedings pages (PMLR, JMLR, ICLR, NeurIPS, ML Anthology, AISTATS 2024 award page);
- PMC for FunDiff, Solera-Rico, CoNFiLD and GenCast;
- full text of the 53 arXiv PDFs, for every figure and every equation;
- PDF of the offer and ANR page.

**Count.** 55 bibliographic entries:
- **46 [verified]**, of which 5 completed with a DOI or pages;
- **9 [corrected]**;
- **0 reference not found.**

**3 claims [UNCONFIRMED]** (see "Unconfirmed" at the end of the file): two bibliographic details ("spotlight" status of Lipman et al. 2023, first name of Sengupta in Bansal et al. 2024) and the negative claim "no generative model on dynamo simulations", central to the positioning of the topic.

**Important corrections:**
1. **ECI: the "inconsistency ×310 vs ×4.9" does not exist.** Table 4 gives the memory per batch: 5.4 GB for 128 samples versus 26.4 GB for 2 samples (D-Flow). Per sample, the ratio is about ×313, consistent with the "×310" of the text. The opposite claim of the research report is false.
2. **Solera-Rico et al.**: all the figures (89.8% / 64.4% / 69 modes, β = 0.05, d = 20, 78.1% / 64.6%) are confirmed in the **published version** (PMC10866995). They do not come only from the preprint.
3. **Eivazi et al.**: 87.36% versus 32.41% is confirmed in Eivazi's own paper.
4. **Albergo, Boffi, Vanden-Eijnden**: *JMLR* 26(209):1–80 (2025). The volume had been recorded as unconfirmed.
5. **"Project and Generate"**: the O(10⁻⁷) divergence and the divergence ("Inf") of unconstrained flow matching at Re = 1000 are verified in Table 1.
6. **Genuist et al. 2026**:
   - the text also calls the flow "Kolmogorov flow", but it is an unforced decaying turbulence with Ekman friction;
   - on out-of-distribution Taylor–Green, L has the best MSE but a nonzero divergence (ε_div 1.84×10⁻²).
7. **Galletti et al. 2026**: the actual title is "A Shortcut to Statistically Steady-State Turbulence with Flow Matching". GyroFlow is the name of the model.
8. **Confirmed statuses**: DDPM at NeurIPS 2020, AISTATS 2024 award for FFM, PDM and D-Flow (DOI, PMLR pages).
9. **FunDiff**: "below 10%" (Burgers) appears only in the published version (PMC), not in arXiv v2.

**Confirmed without change:**
- **FunDiff**: reference (Nat. Commun. 17, 5749, DOI, dates, T.-R. Liu at Laboratoire Navier, ENPC) and equations in the paper (ψ with u = ∂ψ/∂y, v = −∂ψ/∂x; γ = [cos x, sin x, cos y, sin y]; symmetry with 4 evaluations; L_PDE; rectified flow; z̃₁ = z₁ + E(c)). Error of 5.12%.
- **PIDM**: Eq. 14, c = 10⁻³ / 10⁻⁵, +23% / +69%, Table 1.
- **Genuist**: quotations and Tables 1 and 2.
- **PCDM**: about ×5, i.e. 12 days versus 56.
- **Kacmaz**: Table 1.
- **Fukami & Taira**: reference and figures confirmed.
- **GenCast**: 97.2% versus 97.4%.

The absence of generative models on dynamo simulations remains a negative claim. A complementary search (arXiv API, web) did not contradict it.

---

Fact base for the site, the prospective internship report and the thesis topic of **MilaDy** (M2 internship "Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems", CEREA/ENPC).
Sources consulted: 6 November 2026. Each fact is followed by the URL actually opened. Synthesis judgments (not from a source) are marked **[synthesis]**.

Convention: "hard" = constraint satisfied by construction or to machine precision; "soft" = penalty or guidance that reduces the violation without cancelling it.

---

## 0. Verified context (offer and ANR project)

- **Internship offer** [verified] (PDF: https://scheng2024.github.io/stage_milady_2027.pdf). Tasks: (i) conditional generative models by diffusion or flow matching of physical fields conditioned on parameters; (ii) constraints coming from PDEs and boundary conditions, imposed "through model design, training losses, or sampling procedures"; (iii) validation on simple PDEs then MHD fields with metrics "energy spectra, helicity, divergence control, and topology preservation". Expected deliverable: "A comparative study of physics-constrained generative modelling strategies for parameter-dependent MHD fields". Duration 5–6 months starting in spring 2027, ENPC Champs-sur-Marne; funded thesis possible. References of the offer: FunDiff (Wang et al. 2026), Fukami & Taira 2023; "Other References": Bansal et al. 2024, Bastek et al. 2025, Solera-Rico et al. 2024.
- **ANR project MilaDy** [verified] (ANR-25-CE51-0077, https://anr.fr/Projet-ANR-25-CE51-0077) titled "Modélisation par apprentissage automatique des dynamos turbulentes" [Machine-learning modelling of turbulent dynamos]. Coordinator Caroline Nore (LISN). Partners: LISN, Lagrange (Observatoire de la Côte d'Azur), CEREA (ENPC). ANR funding 560 612 €, 48 months, starting January 2026. Objectives: (1) study magnetic field reversals and "explosive" dynamo phenomena with data-driven methods, build ROMs that reproduce precursor, reversal and rebound; (2) optimize the DRESDYN experiment (precessing cylinder) via parametric ROMs (precession / rotation frequency ratio).

---

## 1. Foundations: diffusion and score-based models

### 1.1 Ho, Jain, Abbeel (2020) — DDPM [corrected: venue "unverified" → NeurIPS 2020 confirmed (ML Anthology)]
- Ref.: J. Ho, A. Jain, P. Abbeel, "Denoising Diffusion Probabilistic Models", NeurIPS 2020. arXiv:2006.11239 (v1 19 June 2020, v2 16 Dec. 2020). https://arxiv.org/abs/2006.11239
- Contribution: forward Gaussian noising process with discrete steps, network trained to predict the noise, sampling by reverse Markov chain.
- Figures (abstract): unconditional CIFAR-10 **FID 3.17**, **Inception score 9.46**; LSUN 256×256 of quality "similar to ProgressiveGAN".
- Physical constraint: none.
- Venue: **NeurIPS 2020** confirmed at https://mlanthology.org/neurips/2020/ho2020neurips-denoising/ (the arXiv page does not mention it).

### 1.2 Song, Sohl-Dickstein, Kingma, Kumar, Ermon, Poole (2021) — Score SDE [verified]
- Ref.: "Score-Based Generative Modeling through Stochastic Differential Equations", **ICLR 2021 (Oral)** (arXiv comment). arXiv:2011.13456. https://arxiv.org/abs/2011.13456
- Contribution: unifies DDPM and score matching as forward/reverse SDEs; introduces the probability flow ODE (deterministic sampling and exact likelihood) and predictor-corrector sampling.
- Figures (abstract): CIFAR-10 **IS 9.89**, **FID 2.20**, **2.99 bits/dim**; first 1024×1024 generation by a score-based model.
- Physical constraint: none. Framework reused by CoCoGen, SDA, DDO.

### 1.3 Karras, Aittala, Aila, Laine (2022) — EDM [verified]
- Ref.: "Elucidating the Design Space of Diffusion-Based Generative Models", **NeurIPS 2022** (arXiv comment). arXiv:2206.00364. https://arxiv.org/abs/2206.00364
- Contribution: separates the design choices (network preconditioning, noise schedule, sampler); fast sampler.
- Figures (abstract): CIFAR-10 **FID 1.79** (conditional) and **1.97** (unconditional) with **35 network evaluations** per image; ImageNet-64: FID 2.07 → **1.55** (pre-trained model), **1.36** after retraining.
- PDE usage: DiffusionPDE follows the EDM denoiser (https://arxiv.org/html/2406.17763v2) and GenCast follows the EDM framework (https://pmc.ncbi.nlm.nih.gov/articles/PMC11666454/) and Genuist et al. 2026 use a "vanilla EDM" as reference (https://arxiv.org/html/2601.19368).

### 1.4 Ho & Salimans (2022) — Classifier-free guidance (CFG) [verified]
- Ref.: J. Ho, T. Salimans, "Classifier-Free Diffusion Guidance", arXiv:2207.12598 (26 July 2022). Short version at the **NeurIPS 2021 Workshop on Deep Generative Models and Downstream Applications**. https://arxiv.org/abs/2207.12598
- Contribution: a single network trained both conditionally and unconditionally (the condition is replaced by ∅ with probability p_uncond); at sampling time, **ε̃ = (1+w)·ε(z,c) − w·ε(z)** (Eq. 6). https://ar5iv.labs.arxiv.org/html/2207.12598
- Figures: p_uncond tested at 0.1 / 0.2 / 0.5 (0.1 and 0.2 equivalent, 0.5 worse). ImageNet 64×64: FID 1.8 (w=0); **best FID 1.55** (w=0.1); FID 26.22 / IS 260.2 at w=4. ImageNet 128×128: FID 7.27 (w=0) → **2.43** (w=0.3).
- Relevance to MilaDy **[synthesis]**: standard mechanism to condition on (Re, Rm, material properties). Shu et al. 2023 use it with the gradient of the PDE residual as "condition" (see 3.4).

### 1.5 Chung, Kim, McCann, Klasky, Ye (2023) — DPS [verified]
- Ref.: "Diffusion Posterior Sampling for General Noisy Inverse Problems", **ICLR 2023 (spotlight)**. arXiv:2209.14687. https://arxiv.org/abs/2209.14687
- Method: Tweedie estimate x̂₀ = (1/√ᾱᵢ)(xᵢ + (1−ᾱᵢ)ŝ), then gradient step x_{i−1} ← x'_{i−1} − ζᵢ ∇_{xᵢ}‖y − 𝒜(x̂₀)‖²; ζᵢ = ζ'/‖y − 𝒜(x̂₀)‖. Approximation p(y|x_t) ≃ p(y|x̂₀) whose error is quantified by the **Jensen gap** (bound that decreases as σ grows). https://ar5iv.labs.arxiv.org/html/2209.14687
- Figures: FFHQ "about 95 seconds per image (1000 NFE)" on an RTX 2080Ti.
- Constraint: sampling-time guidance, **soft**. Basis of DiffusionPDE, CoNFiLD, PISD, SDA (improved version).

### 1.6 Bansal, Chu, Schwarzschild, Sengupta, Goldblum, Geiping, Goldstein (2024) — Universal guidance [verified]
- Ref.: "Universal Guidance for Diffusion Models", **ICLR 2024**. arXiv:2302.07121 (14 Feb. 2023). Proceedings: https://proceedings.iclr.cc/paper_files/paper/2024/hash/dfbb3d1807b21dadee735eb75069ada4-Abstract-Conference.html ; arXiv: https://arxiv.org/abs/2302.07121
- Method (https://arxiv.org/html/2302.07121) :
  - *Forward guidance*: ẑ₀ = (z_t − √(1−α_t)ε_θ)/√α_t then ε̂ = ε_θ + s(t)·∇_{z_t} ℓ(c, f(ẑ₀)), with f any guidance network (not trained on noisy data).
  - *Backward guidance*: Δz₀ = argmin_Δ ℓ(c, f(ẑ₀+Δ)) by m descent steps, then ε̃ = ε_θ − √(α_t/(1−α_t))·Δz₀; "prioritizes enforcing the constraint".
  - *Per-step self-recurrence*: re-noising z′_t = √(α_t/α_{t−1}) z_{t−1} + √(1−α_t/α_{t−1}) ε′, repeated k times.
- Reported hyperparameters: Stable Diffusion + CLIP s(t)=10·√(1−α_t), k=8, m=0; segmentation s=400·√(1−α_t), k=10; face recognition s=20000·√(1−α_t), k=2. The paper states that the hyperparameters must be chosen per guidance network.
- Constraint: **soft**, at sampling time, without retraining. Cost **[synthesis]**: k × (forward + backpropagation through f) per step.
- Remark: the ICLR proceedings write "Roni Sengupta", arXiv/OpenReview "Soumyadip Sengupta" (same person according to common usage; identity not formally verified, see "Unconfirmed"). The internship offer cites "Sengupta, R.".

---

## 2. Flow matching, stochastic interpolants, generative models in function space

### 2.1 Lipman, Chen, Ben-Hamu, Nickel, Le (2023) — Flow Matching [verified]
- Ref.: "Flow Matching for Generative Modeling", **ICLR 2023** (https://mlanthology.org/iclr/2023/lipman2023iclr-flow/, OpenReview id PqvMRDCJT9t). arXiv:2210.02747. https://arxiv.org/abs/2210.02747
- Contribution: simulation-free training of CNFs by regression of a velocity field on Gaussian conditional probability paths; diffusion paths are a special case; the OT displacement path is more efficient (faster training and sampling).
- "Spotlight" status: **[UNCONFIRMED]** (OpenReview inaccessible; a mirror of the ICLR 2023 lists indicates "notable top 25%"). See final section.

### 2.2 Liu, Gong, Liu (2023) — Rectified flow [verified]
- Ref.: X. Liu, C. Gong, Q. Liu, "Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow", **ICLR 2023** (https://mlanthology.org/iclr/2023/liu2023iclr-flow/). arXiv:2209.03003. https://arxiv.org/abs/2209.03003
- Method: min ∫₀¹ E‖(X₁−X₀) − v(X_t,t)‖² dt with X_t = tX₁ + (1−t)X₀; iterative "reflow" that straightens the trajectories. https://ar5iv.labs.arxiv.org/html/2209.03003
- Figure: "state-of-the-art result of FID (4.85) and recall (0.51) on CIFAR10 for one-step" (introduction).
- PDE usage: **FunDiff trains its latent DiT by rectified flow** (https://arxiv.org/html/2506.07902v2).

### 2.3 Albergo & Vanden-Eijnden (2023); Albergo, Boffi, Vanden-Eijnden (JMLR 2025) — Stochastic interpolants [verified (ref. 1); corrected (ref. 2): JMLR volume "unconfirmed" → *JMLR* 26(209):1–80, 2025]
- Ref. 1: M. S. Albergo, E. Vanden-Eijnden, "Building Normalizing Flows with Stochastic Interpolants", **ICLR 2023**. arXiv:2209.15571. https://arxiv.org/abs/2209.15571 — quadratic loss on the velocity, without backpropagation through an ODE solver; competitive with diffusion on CIFAR-10 and ImageNet 32×32, up to 128×128.
- Ref. 2: M. S. Albergo, N. M. Boffi, E. Vanden-Eijnden, "Stochastic Interpolants: A Unifying Framework for Flows and Diffusions", ***JMLR* 26(209):1–80 (2025)** (https://jmlr.org/papers/v26/23-1605.html ; JMLR bib opened). arXiv:2303.08797 (v4, 9 Oct. 2025, comment "JMLR Version"). https://arxiv.org/abs/2303.08797 — unifies ODEs and SDEs with tunable diffusion coefficient; recovers the Schrödinger bridge if the interpolant is optimized.
- Ref. 2: volume, issue and pages confirmed by the JMLR page and .bib file (submitted 12/23, published 9/25).

### 2.4 Tong et al. (2024) — OT-CFM [verified]
- Ref.: A. Tong, K. Fatras, N. Malkin, G. Huguet, Y. Zhang, J. Rector-Brooks, G. Wolf, Y. Bengio, "Improving and generalizing flow-based generative models with minibatch optimal transport", **TMLR 2024** (https://mlanthology.org/tmlr/2024/tong2024tmlr-improving/). arXiv:2302.00482. https://arxiv.org/abs/2302.00482
- Contribution: *generalized conditional flow matching* (CFM), without mandatory Gaussian source; the OT-CFM variant (minibatch OT coupling) gives simpler flows, more stable to train and faster at inference.

### 2.5 Kerrigan, Migliorini, Smyth (2024) — Functional Flow Matching (FFM) [corrected: award "seen in a search result" → confirmed on the official AISTATS 2024 page]
- Ref.: "Functional Flow Matching", **AISTATS 2024, PMLR 238:3934–3942**. https://proceedings.mlr.press/v238/kerrigan24a.html ; arXiv:2305.17209. "Outstanding Student Paper" award: confirmed at https://aistats.org/aistats2024/awards.html (the UCI page https://ics.uci.edu/2024/05/30/mlstats-collaboration-leads-to-outstanding-student-paper-at-aistats/ returned a 503 error during verification).
- Contribution: flow matching in infinite dimension; path of measures from a fixed Gaussian measure; without likelihood or simulation.
- Usage: FFM + FNO prior for ECI (https://arxiv.org/html/2412.01786v2) ; baseline in PCFM.

### 2.6 Lim et al. (2025) — Score-based diffusion in function space (DDO) [verified]
- Ref.: J. H. Lim, N. B. Kovachki, R. Baptista, C. Beckham, K. Azizzadenesheli, J. Kossaifi, V. Voleti, J. Song, K. Kreis, J. Kautz, C. Pal, A. Vahdat, A. Anandkumar, "Score-Based Diffusion Models in Function Space", **JMLR 26(158):1–62, 2025**. https://jmlr.org/papers/v26/23-1472.html ; arXiv:2302.07400.
- Contribution: *Denoising Diffusion Operators*; noising by Gaussian process, function-valued Langevin dynamics, sampling cost independent of the resolution. Tests: Navier–Stokes, volcanic InSAR, MNIST-SDF.

---

## 3. Generative models for PDEs and flows

### 3.1 FunDiff — Wang, Dou, Shan, Liu, Lu (2026) ★ main reference of the offer [verified]
- **Verified ref.**: S. Wang, Z. Dou, S. Shan, T.-R. Liu, L. Lu, "FunDiff: diffusion models over function spaces for physics-informed generative modeling", ***Nature Communications* 17, 5749 (2026)**, **DOI 10.1038/s41467-026-72292-0**. Received 7 July 2025, accepted 7 Apr. 2026, published **27 Apr. 2026**. https://pmc.ncbi.nlm.nih.gov/articles/PMC13324421/ — arXiv preprint arXiv:2506.07902 (v1 9 June 2025, v2 25 Nov. 2025). https://arxiv.org/abs/2506.07902
- Affiliations (PMC): Yale (Wang, Dou, Shan, Lu); **Tong-Rui Liu: Laboratoire Navier, École nationale des ponts et chaussées** (same institution as CEREA → potential local contact **[synthesis]**). Code: https://github.com/sifanexisted/fundiff
- **Architecture** (https://arxiv.org/html/2506.07902v2) :
  - *Function autoencoder (FAE)*. Encoder: ViT-type patchification, trainable positional embeddings interpolated (variable discretizations), **Perceiver-type cross-attention** (N learned latent queries), then Transformer blocks. Decoder: **CViT**-type; query coordinates encoded (random Fourier features or grid), K cross-attention blocks (queries = coordinates, keys/values = latents), output MLP → function evaluable at any point.
  - Hyperparameters: encoder 8 layers, decoder 4 layers, dim. 256, MLP 512; DiT 8 blocks, dim. 256, 8 heads, AdaLN-Zero.
  - *Latent diffusion*: DiT trained by **rectified flow**; conditioning by coarse measurements c encoded by the frozen FAE encoder and added: z̃₁ = z₁ + E(c); 20–50 typical evaluations (100 steps for the sinusoidal example).
  - Training: FAE (MSE on random points, 4 096 points/sample, AdamW, batch 16, random subsampling ×1/2/4/8) then DiT (frozen FAE, batch 128, 10⁵ iterations).
- **Constraint imposition**:
  - **Zero divergence (hard, architecture)**: the decoder outputs a **stream function ψ**, u = ∂ψ/∂y, v = −∂ψ/∂x (Kolmogorov). Predicted divergence "negligible"; without the constraint "higher" / "large" (Fig. S1–S3). **No numerical value** in the text.
  - **Periodicity (hard, architecture)**: embedding γ(x,y) = [cos x, sin x, cos y, sin y] → period 2π on [0,2π]² ("hard constraint" approach attributed to Lu et al. 2021).
  - **PDE residual (soft, loss)**: L_PDE = ‖R(f̂)‖², derivatives by automatic differentiation (Burgers; w_data = 100, w_physics = 1).
  - **Symmetry (hard, architecture)**: D(z,x,y)+D(z,1−x,y)+D(z,x,1−y)+D(z,1−x,1−y) (linear elasticity).
- **Benchmarks and figures**:
  - Damped sinusoid: n = 16 to 256 training samples, 8 192 generated samples.
  - **2D Kolmogorov, Re = 1000**, forcing −4cos(4x₂) − 0.1ω, domain (0,2π)²; data: pseudo-spectral solver 2048² → 256², **40 sequences** of 10 s, Δt = 1/32 s, 320 frames. 64×64 reconstruction + 20% noise; spectra correct up to k ~ O(10²) then artificial high-frequency components. Baselines: FNO, ViT, UNet, CViT, DPOT, CNextU-Net, AViT, DPS, DiffusionPDE, Spatially-Aware Diffusion (errors only in figure 3d–e).
  - **Burgers** (ν = 0.001, 4 000 GRF ICs, 200×201): relative L2 error "below 10%" (sentence present in the published PMC version, absent from arXiv v2); residual "O(10⁻²)" (Fig. S4).
  - **Linear elasticity** (7 500 RVEs 256×256): **relative L2 error 5.12%** at 256×256 from 32×32 + 10% noise (Fig. 5a).
  - Turbulent mass transfer (RANS, 900 training / 55 test): graphical only.
- **Theory**: minimax rate for density estimation in infinite dimension; RKHS ball (polynomial decay) W₁ ≲ (log log n / log n)^β; lower bound (1/log n)^β, gap O(poly(log log n)).
- GPU training cost: **not reported** in the text read.

### 3.2 PIDM — Bastek, Sun, Kochmann (2025) ★ reference of the offer [verified]
- **Verified ref.**: J.-H. Bastek, W. Sun, D. M. Kochmann, "Physics-Informed Diffusion Models", **ICLR 2025** ("ICLR 2025 camera ready contribution"). arXiv:2403.14404 (v4, 13 Mar. 2025). https://arxiv.org/abs/2403.14404
- **Formulation** (https://arxiv.org/html/2403.14404v4) : residual treated as a **virtual observable** r̂ = 0 with likelihood q_R(r̂|x₀*) = N(r̂; R(x₀*), Σ_t/c · I). Total loss (Eq. 14):
  L_PIDM = E[ λ_t‖x₀ − x̂₀(x_t,t)‖² + (1/(2Σ̄_t))‖R(x₀*(x_t,t))‖² ], Σ̄_t = Σ_t/c, λ_t = Min-SNR-5.
  - *Mean estimation*: x₀* = x̂₀ = E[x₀|x_t]; c = 10⁻³ (Darcy).
  - *Sample estimation*: x₀* = deterministic 2-step DDIM sample; c = 10⁻⁵ (Darcy).
  - x₀ parametrization; training on ε or μ "leads to larger residual errors".
- **Jensen gap**: R(E[x₀|x_t]) ≠ E[R(x₀)|x_t]; the estimate coincides with a true sample only at the last step; growing conflict between data loss and residual loss as t increases; *sample estimation* "drastically improves the alignment of the two losses".
- **Darcy** (64×64, 10 000 training / 1 000 validation, U-Net): residual reduced "by around two orders of magnitude" compared with standard DDPM (abstract: "up to two orders of magnitude" vs prior work); PG-Diffusion (Shu et al.) without significant reduction; CoCoGen moderate improvement. **Training overhead: +23% (mean) and +69% (sample)**. Exact MAE values: **only in Fig. 2**, no table.
- **Topology optimization** (Table 1): in-distribution R_MAE 1.86×10⁻³ (diffusion) → **1.24×10⁻³** (PIDM, −33%); out-of-distribution 1.97×10⁻³ → 1.29×10⁻³ (−35%). Handles equality and inequality constraints (volume, c = 0.1).
- Constraint: **soft, at training time**. Regularizing effect against overfitting.

### 3.3 DiffusionPDE — Huang, Yang, Wang, Park (NeurIPS 2024) [verified; completed: pages 130291–130323]
- Ref.: J. Huang, G. Yang, Z. Wang, J. J. Park, "DiffusionPDE: Generative PDE-Solving under Partial Observation", **NeurIPS 2024 (Advances in NeurIPS 37), pp. 130291–130323**, DOI 10.52202/079017-4140. https://proceedings.neurips.cc/paper_files/paper/2024/hash/eb3878c1dcbfff9ee95d5d033e5f5942-Abstract.html ; arXiv:2406.17763.
- Method (https://arxiv.org/html/2406.17763v2) : **joint** diffusion on coefficient a and solution u (stacked channels); DPS guidance with L_obs and L_pde (ζ_obs, ζ_pde; e.g. Darcy ζ_obs = 2.5×10³ for a, 10⁶ for u, ζ_pde = 10³); **PDE guidance only after 80% of the iterations**, ζ_obs divided by 10 afterwards. For NS: f = ∇·w (horizon too long for the true PDE). EDM denoiser.
- Figures (Table 1, ~500 observations ≈ 3%, relative error): Darcy forward **2.5%** (FNO 28.2%, PINO 35.2%); inverse 3.2%; Poisson 4.5% / 20.0%; Helmholtz 8.8% / 22.6%; NS 6.9% / 10.4%. Caveat: baselines trained on full observations; once optimized (Appendix H) they improve strongly (optimized PINN 6.9% on Darcy forward, Table 5, discussed in Appendix H).
- Constraint: **soft, sampling**.

### 3.4 Shu, Li, Barati Farimani (2023) — Physics-informed diffusion for flow reconstruction [verified]
- Ref.: D. Shu, Z. Li, A. Barati Farimani, "A physics-informed diffusion model for high-fidelity flow field reconstruction", ***J. Comput. Phys.* 478, 111972 (2023)**, DOI 10.1016/j.jcp.2023.111972 (Crossref: https://api.crossref.org/works/10.1016/j.jcp.2023.111972). arXiv:2211.14680.
- Method (https://arxiv.org/html/2211.14680v2) : DDPM trained only on high-fidelity data; SDEdit-type reconstruction (partial noising of the low-fidelity field then DDIM denoising, K = 1 to 3 iterations). Physics via c = ∂r/∂x (gradient of the residual of the vorticity transport equation): (a) *learned guidance* (c as U-Net input, CFG style); (b) *direct gradient guidance* (−λ·∂r/∂x at each step).
- Data: **2D Kolmogorov, Re = 1000**, DNS 2048² → 256², 40 sequences (36/4).
- Figures (Table 1, L2 / equation loss): 64→256: 0.5622 / **0.2178** vs direct UNet 0.6048 / 0.5438 vs bicubic 1.3355 / 10.6639; 32→256: 1.3035 / 0.2039 vs 1.3700 / 9.9291; 5% → 256: 0.9318 / 0.2815; 1.5625% → 256: 1.8213 / 0.2290. L2 gain "marginal", gain on the residual large.
- Constraint: **soft** (conditioning + guidance). Called "PG-Diffusion" by Bastek et al.

### 3.5 CoCoGen — Jacobsen, Zhuang, Duraisamy [verified]
- Ref.: C. Jacobsen, Y. Zhuang, K. Duraisamy, "CoCoGen: Physically Consistent and Conditioned Score-Based Generative Models for Forward and Inverse Problems", ***SIAM J. Sci. Comput.* 47(2), C399–C425 (2025)**, DOI 10.1137/24M1636071 (Crossref). arXiv:2312.10527 (v2 20 Oct. 2024). https://arxiv.org/abs/2312.10527
- Method (https://arxiv.org/html/2312.10527v2) : gradient step on the discretized residual y ← y − 2ε r∇_y r added at the **last N steps** of the solver (SDE or flow ODE), then M additional steps at t = 0; applied to pressure only; ε = 2×10⁻⁴ / max∇_y r. Lightweight conditional models on a frozen unconditional backbone.
- Figures: Darcy 64×64 (10 000 samples): with τ = 2000, M = 1, N = 3 (**4 operator evaluations**), residuals ≤ those of the training set. 1D Burgers: residual 8.84 → 6.24 (500 steps), RMSE ≈ 3.5×10⁻². Surrogate s = 256: L2 error 7.0×10⁻⁴ (pressure).
- Constraint: **soft, sampling (post-correction)**.

### 3.6 Lienen, Lüdke, Hansen-Palmus, Günnemann (ICLR 2024) — "From Zero to Turbulence" [verified]
- Ref.: "From Zero to Turbulence: Generative Modeling for 3D Flow Simulation", **ICLR 2024**. arXiv:2306.01776. https://arxiv.org/abs/2306.01776
- Method (https://arxiv.org/html/2306.01776v3) : **TurbDiff**, DDPM (N = 500 steps, log-linear SNR schedule), 3D U-Net (4 levels + attention at the coarsest level); generates turbulent states without an initial state. Dirichlet conditions imposed by fixing the boundary cells (only the free cells are denoised). **No explicit incompressibility constraint**.
- Data: 45 OpenFOAM LES (27/9/9), channel 0.4×0.1×0.1 m, 20 m/s, **Re = 2×10⁵**, grid **192×48×48**, 5 000 states per simulation, 2.2 TB.
- New metrics: W₂,TKE (Wasserstein-2 on log-TKE spectra) and W₂,ℛ (velocity regions).
- Figures (Table 1): TurbDiff W₂,TKE 3.9 ± 0.4; W₂,ℛ 1.38 ± 0.04; **≈ 20 s per sample (A100) vs ≈ 602 s of solver (16 cores)** → factor ≈ 30.

### 3.7 Kohl, Chen, Thuerey — Autoregressive conditional diffusion (ACDM) [verified]
- Ref.: G. Kohl, L.-W. Chen, N. Thuerey, "Benchmarking autoregressive conditional diffusion models for turbulent flow simulation", ***Neural Networks* 199, 108641 (July 2026)**, DOI 10.1016/j.neunet.2026.108641 (Crossref). arXiv:2309.01745 (v3 11 Dec. 2024). https://arxiv.org/abs/2309.01745
- Method (https://arxiv.org/html/2309.01745v3) : DDPM conditioned on k = 2 previous states and parameters (Re, Ma); **noise added to the conditioning** ("crucial for temporal stability"); 20–100 diffusion steps.
- Cases: Inc (Re ∈ [200, 900] training, test Re ∈ [100,180] and [920,1000]), Tra (Mach), Iso (JHTDB). Generalization outside the parameter range required.
- Figures: Iso MSE 3.7 ± 0.8 (×10⁻²) vs U-Net 26 ± 35; ACDM "on par" with unrolled training; inference cost ∝ number of steps (20–100×). **No physical constraint**.

### 3.8 Gao et al. (2024) — Bayesian conditional diffusion for turbulence [verified]
- Ref.: H. Gao, X. Han, X. Fan, L. Sun, L.-P. Liu, L. Duan, J.-X. Wang, "Bayesian conditional diffusion models for versatile spatiotemporal turbulence generation", ***CMAME* 427, 117023 (2024)**, DOI 10.1016/j.cma.2024.117023 (Crossref). arXiv:2311.07896.
- Method: conditions differentiably linked to the output → gradient added to the unconditional score (without retraining); otherwise condition as input; long sequences by autoregressive conditional sampling. Cases: URANS → LES, wall turbulence, boundary-layer super-resolution. Constraint: **soft/none** (no explicit PDE constraint in the abstract).

### 3.9 CoNFiLD — Du, Parikh, Fan, Liu, Wang (2024) [verified]
- Ref.: P. Du, M. H. Parikh, X. Fan, X.-Y. Liu, J.-X. Wang, "Conditional neural field latent diffusion model for generating spatiotemporal turbulence", ***Nature Communications* 15, 10416 (29 Nov. 2024)**, DOI 10.1038/s41467-024-54712-1 (Crossref). arXiv:2403.05940.
- Method (https://arxiv.org/html/2403.05940v2) : conditional neural field (SIREN + FiLM, auto-decoding, mesh-free decoding) → per-snapshot latents stacked into a latent "image" (N_l × N_t) → latent diffusion (U-Net); zero-shot DPS-type conditioning in the latent space.
- Cases: irregular 2D duct (mean gap 0.041 ≈ 4%), 3D channel Re_τ = 180, periodic hill Re_h = 2800, 3D roughness Re_h = 3200; reconstruction from 10 sensors (0.1%, periodic hill) or 100 sensors (0.17%, roughness) — figures confirmed in the published version (PMC11607081). **No explicit divergence constraint**.
- Relevance **[synthesis]**: "functional autoencoder + latent diffusion" architecture close to FunDiff, on complex 3D geometries.

### 3.10 Rozet & Louppe (2023) — Score-based Data Assimilation (SDA) [verified]
- Ref.: F. Rozet, G. Louppe, "Score-based Data Assimilation", **NeurIPS 2023 (Advances in NeurIPS 36), pp. 40521–40541**, DOI 10.52202/075280-1763 (Crossref). arXiv:2306.10574.
- Method (https://arxiv.org/html/2306.10574v2) : score of a long trajectory decomposed into local scores on segments of length 2k+1 (Markov pseudo-blanket); generation of the whole trajectory at once; observation model decoupled from training; approximate likelihood with term σ²/μ²·AΓAᵀ (Γ = 10⁻² I), improvement of DPS; Langevin correctors.
- Cases: Lorenz 63; **Kolmogorov Re = 10³**, jax-cfd 256² → 64², 1 024 trajectories of 64 states, k = 2. **No explicit physical constraint**.

### 3.11 DiffDA — Huang, Gianinazzi, Yu, Dueben, Hoefler (ICML 2024) [verified]
- Ref.: "DiffDA: a Diffusion model for weather-scale Data Assimilation", **ICML 2024, PMLR 235:19798–19815**. https://proceedings.mlr.press/v235/huang24h.html ; arXiv:2401.05932.
- Method: pre-trained GraphCast adapted as a denoiser; conditioning on the forecast state (training + inference) and on sparse observations (inference only, guidance).
- Figures: 0.25° (~30 km), 13 levels; observations < 0.96% of the points; loss ≤ 24 h lead time vs ERA5.

### 3.12 Generative weather: GenCast and SEEDS
- **GenCast** [verified]: I. Price et al., "Probabilistic weather forecasting with machine learning", ***Nature* 637(8044), 84–90** (online 4 Dec. 2024, 2025 issue), DOI 10.1038/s41586-024-08252-9 (Crossref + https://pmc.ncbi.nlm.nih.gov/articles/PMC11666454/). Conditional diffusion (EDM framework), graph-transformer on an icosahedral mesh (41 162 nodes). **Better than ENS on 97.2% of 1 320 targets** (Nature; the arXiv:2312.15796 preprint states 97.4%); 15 days, 0.25°, 12 h step, > 80 variables; ≈ 8 min per forecast on one TPUv5. **No explicit physical constraint** (noise sampled on the sphere, area-weighted loss).
- **SEEDS** [verified] ("Li et al."): L. Li, R. Carver, I. Lopez-Gomez, F. Sha, J. Anderson, "Generative emulation of weather forecast ensembles with diffusion models", ***Science Advances* 10(13), eadk4489 (29 Mar. 2024)**, DOI 10.1126/sciadv.adk4489 (Crossref). arXiv:2306.14066 (different arXiv title: "SEEDS: Emulation of Weather Forecast Ensembles with Diffusion Models"). Emulation of operational ensembles by diffusion; bias correction, better forecasting of extremes.

### 3.13 Other useful recent work
- **PISD** [verified]: D. Gallon, P. von Wurstemberger, P. Cheridito, A. Jentzen, "Physics-informed diffusion models in spectral space", arXiv:2602.09708 (v2 2 June 2026). Latent diffusion on spectral representations, constraints and measurements imposed by Adam updates at each step (DPS); Poisson, Helmholtz, incompressible NS. https://arxiv.org/abs/2602.09708
- **Li, Biferale et al. 2024** [verified]: T. Li, L. Biferale, F. Bonaccorso, M. A. Scarpolini, M. Buzzicotti, "Synthetic Lagrangian turbulence by generative diffusion models", *Nature Machine Intelligence* 6(4), 393–403 (2024), DOI 10.1038/s42256-024-00810-0 (arXiv journal-ref :2307.08529, https://arxiv.org/abs/2307.08529). 3D trajectories at high Re; reproduces increments, intermittency; discrepancies below the dissipative scale.
- **Review** [verified]: L. Biferale, M. Buzzicotti, "Generative AI in Turbulence: Foundations, Applications, Validations and Benchmarks", arXiv:2610.35123 (26 Oct. 2026), submitted to JFM Perspectives; argues for validation on energy transfer, structure functions, PDF tails, conservation laws. MHD appears there only as a recommended "data layer" for benchmarks (§5.1) and via Martin et al. 2025; no specific MHD metric. https://arxiv.org/abs/2610.35123

---

## 4. Hard constraints and constrained generation

### 4.1 Richter-Powell, Lipman, Chen (2022) — Neural Conservation Laws [verified]
- Ref.: "Neural Conservation Laws: A Divergence-Free Perspective", **NeurIPS 2022 (Advances in NeurIPS 35), pp. 38075–38088**, DOI 10.52202/068431-2759 (Crossref). arXiv:2210.01741.
- Method (https://ar5iv.labs.arxiv.org/html/2210.01741) : **divergence-free by construction** networks via differential forms (d² = 0): (a) *matrix-field*: row-wise divergence of an antisymmetric matrix field A (O(n²) component functions, one fewer Jacobian); (b) *vector-field*: A = J_b − J_bᵀ. Universal on the torus (up to a constant field). Cost quadratic in the dimension. Continuity equation satisfied exactly by parametrizing v = [ρ, ρu]; Hodge in dimension up to 100.
- Constraint: **hard, architecture**. Theoretical basis for imposing ∇·B = 0 in 3D **[synthesis]**.

### 4.2 Fishman, Klarner, De Bortoli, Mathieu, Hutchinson (2023) — Diffusion on constrained domains [verified]
- Ref.: "Diffusion Models for Constrained Domains", **TMLR (July 2023)** (arXiv comment; confirmed at https://mlanthology.org/tmlr/2023/fishman2023tmlr-diffusion/). arXiv:2304.05364. https://arxiv.org/abs/2304.05364
- Method: manifolds defined by **inequalities**; two noising processes: log-barrier metric and reflected Brownian motion. Applications in robotics, proteins. Constraint: **hard (support)**, inequalities only **[synthesis: not directly suited to ∇·B = 0, a linear equality constraint]**.

### 4.3 Liu, Chen, Theodorou, Tao (2023) — Mirror Diffusion Models [verified]
- Ref.: G.-H. Liu, T. Chen, E. Theodorou, M. Tao, "Mirror Diffusion Models for Constrained and Watermarked Generation", **NeurIPS 2023 (Advances in NeurIPS 36), pp. 42898–42917**, DOI 10.52202/075280-1858 (Crossref). arXiv:2310.01236.
- Method: diffusion in the unconstrained dual space via a mirror map; return to the constrained domain by the inverse; computable forms for simplices and ℓ₂ balls. Constraint: **hard (convex)**.

### 4.4 Christopher, Baek, Fioretto (2024) — Projected Diffusion Models (PDM) [verified; completed: DOI 10.52202/079017-2834]
- Ref.: J. K. Christopher, S. Baek, F. Fioretto, "Constrained Synthesis with Projected Diffusion Models", **NeurIPS 2024**, DOI 10.52202/079017-2834 (https://mlanthology.org/neurips/2024/christopher2024neurips-constrained/). arXiv:2402.03559. https://arxiv.org/abs/2402.03559
- Method (https://arxiv.org/html/2402.03559v3) : projection after each Langevin step: x = P_C(x + γg + √(2γ)ε); feasibility guarantee for convex sets (Corollary 5.4); non-convex: "warm-started" projection (interior point), without formal guarantee.
- Figures: microstructures (porosity) FID 30.7 ± 6.8 with exact satisfaction; motion under gravity: 0 violations (Moon, out of distribution); trajectories 100% success vs 77.1% / 53.3%. **Cost** (Table 2 of the appendix, s/sample; interior-point projection on CPU for human motion): materials 26.89 (vs 18.51 cond.); physics 48.85 (vs 35.30); human motion 682.40 (vs 13.79).
- Constraint: **hard, sampling**.

### 4.5 Ben-Hamu et al. (2024) — D-Flow [verified; completed: PMLR 235:3462–3483]
- Ref.: H. Ben-Hamu, O. Puny, I. Gat, B. Karrer, U. Singer, Y. Lipman, "D-Flow: Differentiating through Flows for Controlled Generation", **ICML 2024, PMLR 235:3462–3483** (https://mlanthology.org/icml/2024/benhamu2024icml-dflow/). arXiv:2402.14017. https://arxiv.org/abs/2402.14017
- Method: optimizes the initial noise by backpropagating through the whole flow. Constraint: **soft, costly optimization** (ECI baseline: 28.774 s/sample, see 4.6).

### 4.6 ECI — Cheng et al. (ICLR 2025) [corrected: "internal inconsistency ×310 vs ×4.9" → ×310 consistent, reported per sample (5.4 GB/128 vs 26.4 GB/2 ≈ ×313)]
- Ref.: C. Cheng, B. Han, D. C. Maddix, A. F. Ansari, A. Stuart, M. W. Mahoney, Y. Wang, "Gradient-Free Generation for Hard-Constrained Systems", **ICLR 2025**. arXiv:2412.01786. https://arxiv.org/abs/2412.01786 ; proceedings: https://proceedings.iclr.cc/paper_files/paper/2025/hash/f9d7d6c695bc983fcfb5b70a5fbdfd2f-Abstract-Conference.html
- Method (https://arxiv.org/html/2412.01786v2) : FFM + FNO prior; at each step: **E**xtrapolation u₁ = u_t + (1−t)v_θ(u_t); **C**orrection (imposed values for IC/BC; shift for integral conservation laws); **I**nterpolation u_{t′} = (1−t′)u₀ + t′û₁; M mixing iterations (1–10). Exact satisfaction proven if the correction is exact. **Gradient-free**.
- Figures: CE = 0 everywhere (Table 3); Stokes IC MMSE 0.090×10⁻² vs 2.068×10⁻² (unconstrained FFM); **0.065 s vs 28.774 s (D-Flow) ≈ ×440** (time per sample); memory: text "×310 memory saving". Table 4 gives the GPU memory **per batch**: 5.4 GB for 128 samples (ECI-1) versus 26.4 GB for 2 samples (D-Flow), i.e. ≈ 0.042 GB versus 13.2 GB **per sample** → ≈ ×313, **consistent with "×310"** (the raw ratio 26.4/5.4 ≈ ×4.9 ignores the batch size).
- Constraint: **hard (linear / value constraints), sampling, zero-shot**.

### 4.7 PCFM — Utkarsh, Cai, Edelman, Gómez-Bombarelli, Rackauckas (NeurIPS 2025) [verified; completed: DOI 10.52202/085713-5354]
- Ref.: "Physics-Constrained Flow Matching: Sampling Generative Models with Hard Constraints", **NeurIPS 2025** (Advances in NeurIPS 38), DOI 10.52202/085713-5354 (https://papers.nips.cc/paper_files/paper/2025/hash/eacce1f7d11e2c3a7568468e0eff5d33-Abstract-Conference.html). arXiv:2506.04171 (v1 4 June 2025, v2 25 Nov. 2025).
- Method (https://arxiv.org/html/2506.04171v2) : (1) shooting to τ = 1; (2) Gauss–Newton projection u_proj = u₁ − Jᵀ(JJᵀ)⁻¹h(u₁); (3) return by OT interpolant; (4) relaxed correction (3–5 gradient steps); (5) exact final projection (Newton solver by Schur complement). **Nonlinear** constraints.
- Figures (Table 3, MMSE ×10⁻²): heat 0.241 (ECI 0.697, DiffusionPDE 4.49); NS 4.59 (ECI 5.23); reaction-diffusion 0.026; Burgers (IC) **0.052 vs ECI 10.0** ("up to 99.5%"); Burgers (BC) 0.335 vs D-Flow 0.224 (D-Flow better). CE = 0 for PCFM ("machine precision"); ECI keeps CE ≠ 0 on nonlinear constraints (Burgers BC, reaction-diffusion BC). Final projection = 1–3% of the total time.
- Constraint: **hard, sampling, zero-shot**.

### 4.8 "Genuist et al. (2026)" — VERIFICATION [corrected (clarification): "the abstract says Kolmogorov flow, the text describes a decaying turbulence" → the text also calls it "Kolmogorov flow" (§1.3), but the simulated flow is unforced, f = −αu]
- **The paper exists.** W. Genuist, É. Savin, F. Gatti, D. Clouteau, "**Divergence-Free Diffusion Models for Incompressible Fluid Flows**", **arXiv:2601.19368** (v1, 27 Jan. 2026), physics.flu-dyn; **preprint, no journal reference**. https://arxiv.org/abs/2601.19368
- Method (https://arxiv.org/html/2601.19368) : autoregressive score-based diffusion (EDM base), incompressibility by **Leray spectral projector**. Six variants compared (Table 1): 𝒱 vanilla EDM; **M** projection on the manifold (noise, state, denoiser — strict); **D** Leray at the denoiser output (strict, architecture); **L** PINN-type divergence residual (**soft**); SC per-frame a posteriori projection (soft); **PC** progressive projection (strict).
- Data: 2D periodic, Fourier-Galerkin 512², fields 256², ν = 5.0×10⁻⁴, L = 2π, 10 seeds × 100 frames; the text (§1.3, §6) and the abstract call it "Kolmogorov flow", but the dataset is an **unforced** decaying turbulence with Ekman friction f = −αu, α = 3.75×10⁻⁴ (§2.3, Table A.3).
- Figures: short rollout (Table 2, "Rollout predictions averaged metrics") PC MSE 1.15×10⁻⁴, ε_div 0; 𝒱 MSE 1.41×10⁻⁴, ε_div 8.07×10⁻³; **L MSE 2.07×10⁻⁴, ε_div 5.21×10⁻³**. OOD "VS" (Fig. 10): M MSE 1.44×10⁻³ (ε_div 0); L 2.62×10⁻³. **OOD Taylor–Green (Fig. 11): L "achieves the best overall performance"** (MSE 4.53×10⁻⁴ vs 𝒱 1.49×10⁻³), but with ε_div 1.84×10⁻²; PC is the only one to keep ε_div = 0.
- **Verdict on the claim of the earlier report**: partially correct. Quotation: "(L) performs poorly across all metrics, consistently under-performing both in in-distribution assessment and in the rollout evaluation" (§5.2.1). **But** on the out-of-distribution Taylor–Green case, the soft variant L is the best. Conclusions (§6): M most accurate in distribution; strict constraints better near the distribution and at short horizon; softer constraints or corrected models preferable in long rollout and out of distribution; **"no single strategy dominates"**. Any citation must keep this nuance and specify "2026 preprint". The comparison concerns the divergence alone (not a full PDE residual).
- Earlier work by the same authors [verified]: "Autoregressive regularized score-based diffusion models for multi-scenarios fluid flow prediction", arXiv:2505.24145 (30 May 2025): **energy constraint** based on turbulent statistics, low overhead. https://arxiv.org/abs/2505.24145

### 4.9 PCDM — Li, Buzzicotti, Bonaccorso, Biferale (2026) [verified]
- Ref.: "Physics-Constrained Diffusion Model for Synthesis of 3D Turbulent Data", arXiv:2603.12834 (13 Mar. 2026), submitted to a journal. https://arxiv.org/abs/2603.12834
- Method (https://arxiv.org/html/2603.12834v1) : Fourier projection (I − kkᵀ/|k|²) and û(0) → 0 applied to the **clean estimate** 𝒱₀,θ; corrected noise deduced from the projected estimate; x_t and the noise need not be divergence-free.
- Data: **3D rotating turbulence**, DNS 256³ → 64³ (Galerkin truncation), Ro ≈ 0.1.
- Figures: zero divergence "at machine precision"; **training time ≈ ×5 shorter** than DDPM-prog (8×10⁵ iterations ≈ 12 days vs 4×10⁶ ≈ 56 days, on 4 A100 GPUs; Appendix D). Spectra and flatness: figure only.
- Constraint: **hard, architecture/sampling**. Closest 3D analogue of what MilaDy requires for ∇·u = 0 and ∇·B = 0 **[synthesis]**.

### 4.10 "Project and Generate" — Li X. et al. (2026) [corrected: "O(10⁻⁷) … unverified figure" → verified in Table 1]
- Ref.: X. Li, H. Zhang, R. Jiang, D. Chen, C. Lin, L. Han, Y. Qi, X. Guo, Y. Cheng, "Project and Generate: Divergence-Free Neural Operators for Incompressible Flows", arXiv:2603.24500 (25 Mar. 2026). https://arxiv.org/abs/2603.24500
- Method: Helmholtz-Hodge spectral projection (deterministic); for the generative case, **divergence-free Gaussian reference measure** built by pushforward via the curl of stream functions + Leray → flow matching paths remaining in the constrained space. Results (Table 1, periodic 2D NS, Re = 1000, FNO backbone): divergence of the constrained generative model ≈ 4×10⁻⁷ (prediction), 2×10⁻⁷ (short term), 1.6×10⁻⁷ (long term, t ∈ [201, 300]) → **O(10⁻⁷)** confirmed; unconstrained flow matching diverges in the long term ("Inf", numerical overflow).

---

## 5. Generative models applied to MHD, dynamos, astrophysics (2022–2026)

Main result of the search: **no diffusion or flow matching model applied to dynamo simulations** (geodynamo, experimental VKS/DRESDYN dynamo, turbulent dynamo) **was found** (queries: "generative model dynamo", "diffusion model geodynamo", "flow matching MHD", "diffusion magnetohydrodynamics", "super-resolution MHD diffusion", "3D MHD helicity diffusion"). Closest works:

| Work | Verified ref. | What is generated | ∇·B = 0 constraint |
|---|---|---|---|
| **Kacmaz, Huerta, Haas (2025)** "Resolving Turbulent Magnetohydrodynamics: A Hybrid Operator-Diffusion Framework" | [verified] *Mach. Learn.: Sci. Technol.* 6(3), 035057 (2025), DOI 10.1088/2632-2153/ae054c ; arXiv:2507.02106 (https://arxiv.org/abs/2507.02106) | Spatio-temporal evolution of 2D incompressible resistive MHD; PINO (low frequencies, **soft** PDE losses) + conditional diffusion (high-frequency correction) | In the **solver** (Dedalus) via vector potential A, B = ∇×A; the generative model imposes no hard constraint. Data: 128², Pm = 1, Re ∈ {100,…,10 000}, 1 000 simulations per Re. Averaged relative L2 error: Re = 1000: 0.2548 (PINO) → **0.1033** (PINO+diffusion); Re = 10 000: 0.3914 → 0.2052; Re = 100: 0.0072 → 0.0080 (slight degradation). Kinetic/magnetic spectra in figure only; **no helicity**. Only baseline: their PINO. (https://arxiv.org/html/2507.02106v2) |
| **Martin, Lübke, Li, Buzzicotti, Grauer, Biferale (2025)** | [verified] *ApJS* 277(2), 48 (2025), DOI 10.3847/1538-4365/adb432 (Crossref) ; arXiv:2412.12923 | Test particle trajectories (cosmic rays) in 3D MHD turbulence | Not applicable (trajectories) |
| **da Silva, Kirk, Mathews, Muñoz-Jaramillo (2025)** "Diffusion Modeling of the Three-Dimensional Magnetic Field in the Sun's Corona" | [verified] arXiv:2510.01441 (1 Oct. 2025), no journal | Spherical harmonic coefficients G, H (degree 90, output 8 281) of the ADAPT-WSA potential field, conditioned by the solar cycle phase S ∈ [0,1] | **Hard by representation**: B = −∇V with ∇×B ≈ 0, harmonics satisfying Laplace → ∇·B = 0. DDPM T = 1000, DDIM 20 steps; 27.3 M augmented examples; **qualitative evaluation only**. (https://arxiv.org/html/2510.01441v1) |
| **Ramunno et al. (2024)** "Magnetogram-to-Magnetogram" | [verified] arXiv:2407.11659, ESA SPAICE 2024 conference | LoS magnetograms at +24 h (DDPM) | No (2D, LoS component) |
| **Xu D. et al. (2025)** "Exploring Magnetic Fields in Molecular Clouds through DDPM" | [verified] *ApJ* 980(1), 52 (2025), DOI 10.3847/1538-4357/ada8a0 (Crossref) ; arXiv:2410.07032 | Estimation of the intensity of B from synthetic observables | No |
| **Galletti et al. (2026)** "A Shortcut to Statistically Steady-State Turbulence with Flow Matching" (model GyroFlow) | [corrected: title missing ("GyroFlow") → full arXiv title ; G. Galletti, G. Gutenbrunner, W. Hornsby, L. Zanisi, N. Carey, S. Pamela, J. Brandstetter, F. Paischer] arXiv:2607.13022 (14 July 2026), preprint | Saturated states of gyrokinetic turbulence (latent flow matching conditioned on dimensionless parameters); solver warm start | Not mentioned |
| **Mudur & Finkbeiner (2022)** | [verified] arXiv:2211.12444 ("Machine Learning and the Physical Sciences" workshop, NeurIPS 2022, according to the arXiv comment) | Dark matter fields, interstellar dust | No |
| **The Well** (Ohana, McCabe, Meyer, Morel et al.) | [verified; completed: DOI 10.52202/079017-1430] NeurIPS 2024 Datasets & Benchmarks (https://proceedings.neurips.cc/paper_files/paper/2024/hash/4f9a5acd91ac76569f2fe291b1f4772b-Abstract.html) ; arXiv:2412.00568 | Dataset: isothermal MHD without self-gravity, 256³ and 64³, 100 trajectories × 100 steps | — (dataset; useful as a public 3D MHD benchmark **[synthesis]**) |

---

## 6. Model reduction by learning

### 6.1 Fukami & Taira (2023) ★ reference of the offer [verified]
- **Verified ref.**: K. Fukami, K. Taira, "Grasping extreme aerodynamics on a low-dimensional manifold", ***Nature Communications* 14, 6480 (14 Oct. 2023)**, **DOI 10.1038/s41467-023-42213-6** (Crossref). arXiv:2305.08024.
- Details (https://arxiv.org/html/2305.08024v2) : **Re = u∞c/ν = 100**; **NACA 0012**; α ∈ [20°, 60°] (20°, 30°, 40°, 50°, 60°; the text writes "six different angles" but lists only five); vortical gusts: G ∈ [−10, 10], L = 2R/c ∈ [0.5; 2], y₀/c ∈ [−0.5; 0.5], x₀/c = −2; AE training on G ∈ [−4, 4]. 40 cases per angle (20 training / 20 test), 1 200 snapshots per case over 10.2 convective times, 240×120 subdomain; **1.26×10⁵ frames** for training (100 cases with gust + 5 cases without perturbation × 1 200 snapshots).
- **Lift-augmented autoencoder**: CNN encoder → **3 latent variables**; mirror decoder; lift MLP on the latent; loss min ‖q − q̂‖₂ + β‖C_L − Ĉ_L‖₂, **β = 0.05** (L-curve), tanh, Adam.
- Results: PCA "completely fails" to detect the vortex; the standard AE has a higher SSIM but a less structured latent; SSIM "over 90%" on two-vortex cases; extreme case α = 20°, G = 3.8: lift **+714% then −656% in 1.8 convective time**; extrapolation to |G| > 4 (G = 6.4, −6.0); ξ₃ ≈ effective angle of attack.
- Not in the paper: number of pressure sensors (only "a small number of sensors"); phase-amplitude analysis and control = perspectives.
- Physical constraint: **no PDE constraint**; physics enters through the **augmentation by an observable** (lift) that organizes the latent.

### 6.2 Solera-Rico et al. (2024) ★ reference of the offer [corrected: figures "from the preprint only, the published version may differ" → all confirmed in the published version (PMC10866995)]
- **Verified ref.**: A. Solera-Rico, C. Sanmiguel Vila, M. Gómez-López, Y. Wang, A. Almashjary, S. T. M. Dawson, R. Vinuesa, "β-Variational autoencoders and transformers for reduced-order modelling of fluid flows", ***Nature Communications* 15, 1361 (14 Feb. 2024)**, **DOI 10.1038/s41467-024-45578-4** (Crossref). arXiv:2304.03571.
- Figures (verified in the published version, https://pmc.ncbi.nlm.nih.gov/articles/PMC10866995/, identical to arXiv:2304.03571v2): 2D flow around **two collinear plates**; periodic case **Re = 40**, angle 90°, 1 000 fields; chaotic case **Re = 100**, angle 80°, 150 000 fields; domain 96c × 28c, 300×98 points.
  - Re = 40: 2 POD modes = 98.4%; β-VAE (β = 0.001) E = 97.5%, R₁₂ = 0.0015.
  - Re = 100: **β = 0.05**, **d = 20**; E = 89.8% (training) / 80.1% (test); d = 10: 82.0% / 61.6%. POD with 20 modes: 64.4%; **69 POD modes** needed to match the β-VAE ("over 69 modes" to exceed E = 90%).
  - Dynamics: transformer (self-attention and easy-attention), delay 64 steps; compared with LSTM and KNF (Koopman with Non-linear Forcing); β-VAE + transformer ROM: **E = 78.1% at t + t_c and 64.6% at t + 10 t_c** (unseen data).
- Physical constraint: **none**; near-perfect orthogonality of the latent through β regularization.

### 6.3 Eivazi, Le Clainche, Hoyas, Vinuesa (2022) [corrected: 87.36% vs 32.41% "unverified in Eivazi" → confirmed in Eivazi et al. (arXiv:2109.01514)]
- Ref.: "Towards extraction of orthogonal and parsimonious non-linear modes from turbulent flows", ***Expert Systems with Applications* 202, 117038 (2022)**, DOI 10.1016/j.eswa.2022.117038 (Crossref). arXiv:2109.01514.
- Contribution: β-VAE + CNN, ranking of modes by contribution; turbulent flow in a simplified urban environment (LES). Figure cited by Solera-Rico et al. (arXiv:2304.03571v2, p. 2): **87.36% of the energy with 5 latent variables vs 32.41% with 5 POD modes**, confirmed in Eivazi et al. (arXiv:2109.01514v1: CNN-βVAE with 5 modes; the non-variational CNN-AE reaches 94.22%).

### 6.4 Lusch, Kutz, Brunton (2018) [verified]
- Ref.: "Deep learning for universal linear embeddings of nonlinear dynamics", ***Nature Communications* 9, 4950 (2018)**, DOI 10.1038/s41467-018-07210-0 (Crossref). arXiv:1712.09707.
- Contribution: autoencoder whose latent evolves linearly (Koopman eigenfunctions); auxiliary network parametrizing the frequency for continuous spectra (pendulum, nonlinear optics, turbulence).

### 6.5 Champion, Lusch, Kutz, Brunton (2019) — SINDy-autoencoder [verified]
- Ref.: "Data-driven discovery of coordinates and governing equations", ***PNAS* 116(45), 22445–22451 (2019)**, DOI 10.1073/pnas.1906995116 (Crossref). arXiv:1904.02107.
- Contribution: joint learning of the latent coordinates (autoencoder) and of a sparse SINDy model in this latent.

---

## 7. Summary table: method → constraint type → hard/soft → cost

The quantified costs come from the sources cited above; "[synthesis]" = qualitative estimate not quantified in the source.

| Method | Where the constraint acts | Constraint type | Hard / soft | Cost (quantified if available) |
|---|---|---|---|---|
| FunDiff (stream function ψ) | Architecture (decoder) | ∇·u = 0 in 2D | Hard (exact up to the derivative computation) | One differentiation of the decoder [synthesis]; training cost not reported |
| FunDiff (Fourier [cos, sin]) | Architecture (embedding) | Periodicity | Hard | Negligible [synthesis] |
| FunDiff (symmetry) | Architecture (4 decoder evaluations) | Reflection symmetries | Hard | ×4 decoder evaluations [synthesis] |
| FunDiff / PIDM (PDE residual) | Training loss | Full PDE residual | Soft | PIDM: +23% (mean) / +69% (sample) training time |
| Shu et al. 2023 | Conditioning + guidance | Vorticity residual | Soft | Gradient of the residual at each step |
| CoCoGen | Correction at the last N steps | Discrete residual | Soft | 4 operator evaluations suffice for Darcy (N = 3, M = 1) |
| DPS / DiffusionPDE / PISD | Sampling-time guidance | Observations + residual | Soft | DPS: 1000 NFE, ≈ 95 s/image (FFHQ, 2080Ti) |
| Universal guidance | Guidance (forward/backward + k repetitions) | Any differentiable function | Soft | k × (forward + backward of f) per step [synthesis] |
| CFG | Conditioning | Parameters (Re, Rm…) | — (not a constraint) | 2 network evaluations per step [synthesis] |
| Neural Conservation Laws | Architecture | Zero divergence / continuity | Hard | Quadratic in the dimension (function evaluations) |
| Leray at the denoiser output (Genuist "D", PCDM) | Architecture / estimate x̂₀ | ∇·u = 0 (and zero mean) | Hard | FFT per step; PCDM: training ≈ ×5 shorter than DDPM-prog |
| Leray on the manifold (Genuist "M") | Noise + state + denoiser | ∇·u = 0 | Hard | FFT per step [synthesis] |
| PINN divergence penalty (Genuist "L") | Loss | ∇·u = 0 | Soft | ε_div 5.21×10⁻³ in rollout (nonzero) |
| A posteriori projection (Genuist "SC") | After each frame | ∇·u = 0 | Outside the model (projection) | 1 projection per frame [synthesis] |
| PDM (Christopher et al.) | Projection after each Langevin step | Convex set (guaranteed) / non-convex | Hard (convex) | 26.89 vs 18.51 s; 682.40 vs 13.79 s depending on the task |
| Mirror DM | Change of variable (mirror) | Convex domain (simplex, ball) | Hard | Low if analytic mirror [synthesis] |
| Fishman et al. | Noising process (barrier / reflection) | Inequalities | Hard | Not quantified |
| D-Flow | Optimization of the initial noise | Any differentiable constraint | Soft | 28.774 s/sample (Stokes, Table 4 of ECI) |
| ECI | Correction at each step (gradient-free) | IC/BC, integral conservation (linear) | Hard | 0.065 s/sample (≈ ×440 faster than D-Flow); memory per sample ≈ ×310 lower |
| PCFM | Gauss–Newton projection + final projection | Nonlinear (conservation, BC, flux) | Hard | Final projection = 1–3% of the total time |
| Potential field (da Silva et al.) | Representation (harmonic coefficients) | ∇·B = 0, ∇×B = 0 | Hard | No overhead [synthesis] |
| Vector potential A (Kacmaz: solver only) | Data | ∇·B = 0 | Hard in the data, not in the generative model | — |
| Fukami & Taira (lift) | Loss (auxiliary observable) | Latent structure | Soft (not a PDE constraint) | Auxiliary MLP [synthesis] |

---

## 8. Gaps in the literature relevant to MilaDy [argued synthesis]

1. **No generative model for the dynamo.** No diffusion or flow matching model was found on dynamo simulations (neither geodynamo, nor VKS, nor DRESDYN, nor 3D turbulent dynamo). The closest MHD work (Kacmaz et al. 2025) is in **2D**, a configuration where a self-sustained dynamo is excluded by the anti-dynamo theorems (Zeldovich) **[synthesis, general knowledge not sourced here]**. Its generative model does not impose ∇·B = 0: only the solver guarantees it.
2. **No joint hard constraint on ∇·u = 0 and ∇·B = 0 in 3D in a generative MHD model.** The building blocks exist separately: 3D Leray in Fourier space (PCDM, 3D rotation, 64³), divergence-free networks (Richter-Powell), stream function (FunDiff, 2D only), scalar potential (da Silva, potential field only). None has been applied to generated 3D MHD fields. The **vector potential A** (B = ∇×A) is the direct 3D generalization of the FunDiff stream function; it imposes a **gauge** to be chosen.
3. **Non-periodic domains and magnetic boundary conditions.** The Leray projection in Fourier space assumes periodicity (PCDM, Genuist). Experimental dynamos (VKS, DRESDYN) have **cylindrical geometry with walls** and matching to an external field. No method found handles a hard divergence constraint with these conditions. Leads: functional decoder (FunDiff, CoNFiLD) + vector potential; PCFM/ECI for the boundary conditions.
4. **No MHD metrics in the evaluation of generative models.** No work found evaluates **magnetic or cross helicity**, the topology of field lines or magnetic energy budgets. Kacmaz et al. show spectra in a figure, without a quantified error. The review Biferale & Buzzicotti (2026) calls for physics-oriented validations; it cites MHD turbulence as a benchmark "data layer" (§5.1) but proposes no MHD metric.
5. **Parametric conditioning and extrapolation.** Kohl et al. and Kacmaz et al. test outside the training Re range; Kacmaz: the Re = 1000 model applied to Re = 100 has an error > 0.85. **No work conditions on (Re, Rm) or Pm together**, nor studies the crossing of the **dynamo threshold** (bifurcation) by a generative model.
6. **No systematic comparison of strategies on coupled PDEs.** The most direct comparison, Genuist et al. 2026 (preprint), concerns the divergence alone in 2D hydrodynamics. It shows that **no strategy dominates**: strict best in distribution, soft sometimes better out of distribution (Taylor–Green). PCFM and ECI compare linear or integral constraints on simple 1D/2D PDEs. The deliverable of the offer ("comparative study […] for parameter-dependent MHD fields") therefore fills a real gap.
7. **Jensen gap and cost.** Residual penalties evaluated on x̂₀ suffer from the Jensen gap (DPS, PIDM). The "sample" variant of PIDM costs +69%. Projection methods (PCDM, ECI, PCFM) avoid it for **linear** constraints such as the divergence, which argues for separating: linear constraints hard (projection or architecture), energy budgets and nonlinear residuals soft or by PCFM-type projection.
8. **Link with model reduction and assimilation.** FunDiff, CoNFiLD and Solera-Rico/Fukami provide compact latents, but none links the generative latent and a **reduced dynamics** for field reversals (objective 1 of the ANR). Assimilation by diffusion (SDA, DiffDA) has not been applied to MHD.
9. **Public 3D MHD data.** The Well (isothermal MHD 64³/256³) can serve as an intermediate benchmark before the consortium's dynamo data (the consortium's simulation code has not been verified here).

---

## 9. Points of vigilance (updated after verification)

- **FunDiff**: no numerical value of divergence, nor of Kolmogorov reconstruction error, in the text (figures only). No GPU cost. The body text cites Fig. 3e for the divergence comparison, whereas the caption of 3e speaks of "PDE constraints" (flagged by the PMC reading).
- **PIDM**: the "two orders of magnitude" gain on Darcy is **visible in Fig. 2 only**; do not invent an exact MAE.
- **ECI**: [corrected] no inconsistency. "×310 memory saving" is a ratio **per sample**: Table 4, 5.4 GB/128 samples versus 26.4 GB/2 samples ≈ ×313.
- **GenCast**: 97.2% (Nature) vs 97.4% (arXiv preprint) of the 1 320 targets; cite the Nature version.
- **Genuist et al. 2026**: non-peer-reviewed preprint; claim "soft penalties perform worse" **true in distribution and in rollout, false on out-of-distribution Taylor–Green**; the authors call it "Kolmogorov flow" (abstract and text), but the flow is an unforced decaying turbulence with Ekman friction.
- **"Project and Generate"** (arXiv:2603.24500): [corrected] "O(10⁻⁷)" and divergence ("Inf") of unconstrained flow matching at Re = 1000 verified in Table 1.
- **Kacmaz et al.**: the abstract mentions non-Gaussian statistics and cross-correlations, but I found no corresponding quantified metric in the text read.
- **Solera-Rico et al.**: [corrected] figures confirmed in the published version via PMC (PMC10866995).
- **Eivazi et al.**: [corrected] 87.36% vs 32.41% confirmed in Eivazi et al. (arXiv:2109.01514v1).
- **Albergo, Boffi, Vanden-Eijnden**: [corrected] *JMLR* 26(209):1–80, 2025 (JMLR page and .bib).
- **DDPM**: [corrected] NeurIPS 2020 confirmed (ML Anthology).
- **Lipman et al.**: "spotlight" status still [UNCONFIRMED] (see final section); ICLR 2023 confirmed.
- **Christopher et al. (PDM)** and **D-Flow**: [corrected] venues confirmed outside arXiv (PDM: DOI 10.52202/079017-2834; D-Flow: PMLR 235:3462–3483, ML Anthology).
- **Kerrigan et al.**: FNO architecture used by ECI as a prior, internal details of FFM not reread.
- **Fukami & Taira**: number of sensors not specified in the paper; read via arXiv v2 (journal-ref Nat. Commun. 14, 6480); the text announces "six" angles of attack but lists five.
- **Nature.com** blocks WebFetch (redirect to idp.nature.com): the *Nature Communications* metadata were verified via Crossref and PMC.
- **FunDiff**: the sentence "relative L2 errors below 10%" (Burgers) exists only in the published version (PMC), not in arXiv v2.

---

## 10. Index of identifiers (all reopened on 6 Nov. 2026: arXiv API, Crossref, proceedings, PMC)

| Paper | Venue | DOI / arXiv |
|---|---|---|
| Ho et al. 2020 DDPM | NeurIPS 2020 | arXiv:2006.11239 |
| Song et al. 2021 | ICLR 2021 (Oral) | arXiv:2011.13456 |
| Karras et al. 2022 EDM | NeurIPS 2022 | arXiv:2206.00364 |
| Ho & Salimans 2022 CFG | NeurIPS 2021 Workshop (short version) | arXiv:2207.12598 |
| Chung et al. 2023 DPS | ICLR 2023 | arXiv:2209.14687 |
| Bansal et al. 2024 | ICLR 2024 | arXiv:2302.07121 |
| Lipman et al. 2023 | ICLR 2023 | arXiv:2210.02747 |
| Liu, Gong, Liu 2023 | ICLR 2023 | arXiv:2209.03003 |
| Albergo & Vanden-Eijnden 2023 | ICLR 2023 | arXiv:2209.15571 |
| Albergo, Boffi, Vanden-Eijnden 2025 | JMLR 26(209):1–80 | arXiv:2303.08797 |
| Tong et al. 2024 OT-CFM | TMLR 2024 | arXiv:2302.00482 |
| Kerrigan et al. 2024 FFM | AISTATS 2024, PMLR 238:3934–3942 | arXiv:2305.17209 |
| Lim et al. 2025 DDO | JMLR 26(158):1–62 | arXiv:2302.07400 |
| Wang et al. 2026 FunDiff | Nat. Commun. 17, 5749 | 10.1038/s41467-026-72292-0 ; arXiv:2506.07902 |
| Bastek et al. 2025 PIDM | ICLR 2025 | arXiv:2403.14404 |
| Huang et al. 2024 DiffusionPDE | NeurIPS 2024, pp. 130291–130323 | 10.52202/079017-4140 ; arXiv:2406.17763 |
| Shu et al. 2023 | J. Comput. Phys. 478, 111972 | 10.1016/j.jcp.2023.111972 ; arXiv:2211.14680 |
| Jacobsen et al. 2025 CoCoGen | SIAM J. Sci. Comput. 47(2), C399–C425 | 10.1137/24M1636071 ; arXiv:2312.10527 |
| Lienen et al. 2024 | ICLR 2024 | arXiv:2306.01776 |
| Kohl et al. 2026 | Neural Networks 199, 108641 | 10.1016/j.neunet.2026.108641 ; arXiv:2309.01745 |
| Gao et al. 2024 | CMAME 427, 117023 | 10.1016/j.cma.2024.117023 ; arXiv:2311.07896 |
| Du et al. 2024 CoNFiLD | Nat. Commun. 15, 10416 | 10.1038/s41467-024-54712-1 ; arXiv:2403.05940 |
| Rozet & Louppe 2023 SDA | NeurIPS 2023, pp. 40521–40541 | 10.52202/075280-1763 ; arXiv:2306.10574 |
| Huang et al. 2024 DiffDA | ICML 2024, PMLR 235:19798–19815 | arXiv:2401.05932 |
| Price et al. GenCast | Nature 637, 84–90 | 10.1038/s41586-024-08252-9 ; arXiv:2312.15796 |
| Li et al. 2024 SEEDS | Sci. Adv. 10(13), eadk4489 | 10.1126/sciadv.adk4489 ; arXiv:2306.14066 |
| Richter-Powell et al. 2022 | NeurIPS 2022, pp. 38075–38088 | 10.52202/068431-2759 ; arXiv:2210.01741 |
| Fishman et al. 2023 | TMLR 2023 | arXiv:2304.05364 |
| Liu et al. 2023 Mirror DM | NeurIPS 2023, pp. 42898–42917 | 10.52202/075280-1858 ; arXiv:2310.01236 |
| Christopher et al. 2024 PDM | NeurIPS 2024 | 10.52202/079017-2834 ; arXiv:2402.03559 |
| Ben-Hamu et al. 2024 D-Flow | ICML 2024, PMLR 235:3462–3483 | arXiv:2402.14017 |
| Cheng et al. 2025 ECI | ICLR 2025 | arXiv:2412.01786 |
| Utkarsh et al. 2025 PCFM | NeurIPS 2025 | 10.52202/085713-5354 ; arXiv:2506.04171 |
| Genuist et al. 2026 | preprint | arXiv:2601.19368 |
| Genuist et al. 2025 | preprint | arXiv:2505.24145 |
| Li T. et al. 2026 PCDM | preprint | arXiv:2603.12834 |
| Li X. et al. 2026 | preprint | arXiv:2603.24500 |
| Gallon et al. 2026 PISD | preprint | arXiv:2602.09708 |
| Kacmaz et al. 2025 | Mach. Learn.: Sci. Technol. 6, 035057 | 10.1088/2632-2153/ae054c ; arXiv:2507.02106 |
| Martin et al. 2025 | ApJS 277(2), 48 | 10.3847/1538-4365/adb432 ; arXiv:2412.12923 |
| da Silva et al. 2025 | preprint | arXiv:2510.01441 |
| Xu D. et al. 2025 | ApJ 980(1), 52 | 10.3847/1538-4357/ada8a0 ; arXiv:2410.07032 |
| Li T. et al. 2024 (Lagrangian) | Nat. Mach. Intell. 6, 393–403 | 10.1038/s42256-024-00810-0 ; arXiv:2307.08529 |
| Fukami & Taira 2023 | Nat. Commun. 14, 6480 | 10.1038/s41467-023-42213-6 ; arXiv:2305.08024 |
| Solera-Rico et al. 2024 | Nat. Commun. 15, 1361 | 10.1038/s41467-024-45578-4 ; arXiv:2304.03571 |
| Eivazi et al. 2022 | Expert Syst. Appl. 202, 117038 | 10.1016/j.eswa.2022.117038 ; arXiv:2109.01514 |
| Lusch et al. 2018 | Nat. Commun. 9, 4950 | 10.1038/s41467-018-07210-0 ; arXiv:1712.09707 |
| Champion et al. 2019 | PNAS 116(45), 22445–22451 | 10.1073/pnas.1906995116 ; arXiv:1904.02107 |
| Ohana et al. 2024 The Well | NeurIPS 2024 D&B | 10.52202/079017-1430 ; arXiv:2412.00568 |
| Galletti et al. 2026 (GyroFlow) | preprint | arXiv:2607.13022 |
| Ramunno et al. 2024 | ESA SPAICE 2024 | arXiv:2407.11659 |
| Mudur & Finkbeiner 2022 | NeurIPS 2022 workshop (ML4PS) | arXiv:2211.12444 |

---

## 11. Unconfirmed

No bibliographic entry is missing. The following details could not be confirmed on a primary source:
- **Lipman et al. 2023, "spotlight" status** [UNCONFIRMED]: OpenReview inaccessible (anti-robot verification). ICLR 2023 is confirmed. A mirror of the ICLR 2023 lists indicates "notable top 25%".
- **Bansal et al. 2024, "Roni" = "Soumyadip" Sengupta** [UNCONFIRMED]: the ICLR proceedings and arXiv differ on the first name. The identity has not been formally established.
- **"No generative model on dynamo simulations"** [UNCONFIRMED, negative claim]: nothing to the contrary found (arXiv API: "diffusion AND dynamo AND generative", "flow matching AND magnetohydrodynamic", "score-based AND dynamo"; web search), but an absence cannot be proven.


## Entries added on 2026-11-11 (review §2.9)

Checked by the `biblio` agent on 2026-11-11.

**Köhler, Klein & Noé (2020).** J. Köhler, L. Klein, F. Noé, "Equivariant Flows: Exact Likelihood Generative Learning for Symmetric Densities", ICML 2020, PMLR 119, 5361–5370, arXiv:2006.02425. [verified, primary]
- Theorem 1 (§3): an H-equivariant diffeomorphism maps a G-invariant density (G > H) to an H-invariant density. Theorem 2 (§4): the flow of an H-equivariant vector field is H-equivariant, so the push-forward of a G-invariant density is H-invariant. They assume |det R_g| = 1, not isometries. [verified]
- Use on this site: P8 Proposition 2.8 is the continuous-time statement of these theorems, with isometries.

**Cohen & Welling (2016).** T. S. Cohen, M. Welling, "Group Equivariant Convolutional Networks", ICML 2016, PMLR 48, 2990–2999, arXiv:1602.07576. [verified, abstract]
- G-convolutions for discrete groups generated by translations, reflections and rotations, "negligible computational overhead" relative to the gain in weight sharing. [verified, abstract] A group convolution costs about |G| times an ordinary one: do not claim that it "avoids the factor |G|".

**Baldan et al. (2026).** G. Baldan, Q. Liu, A. Guardone, N. Thuerey, "Physics vs Distributions: Pareto Optimal Flow Matching with Physics Constraints", arXiv:2506.08604 (v1 June 2025, v4 23 February 2026). [verified, primary: abstract and HTML] Venue: [UNCONFIRMED] (no ICLR statement found; cite as a preprint).
- "Our work is the first to recognize the trade-off between distributional and physical accuracy"; §3.2: "optimizing for physical fidelity often degrades distributional accuracy, and vice versa"; training loss = flow-matching term + PDE-residual term on a predicted clean sample x₁; PBFM uses conflict-free gradients (ConFIG) and unrolling to reduce the Jensen gap. [verified]

**Rice formula and transition-state theory (prior art for the Rice claim of the theory brief).**
- S. O. Rice, "Mathematical analysis of random noise", *Bell Syst. Tech. J.* **23** (1944), **24** (1945): origin of the crossing-rate formula. [UNCONFIRMED: not retrieved]
- D. Chandler, "Statistical mechanics of isomerization dynamics in liquids and the transition state approximation", *J. Chem. Phys.* **68**, 2959 (1978); C. H. Bennett (1977), in Christoffersen (ed.), *Algorithms for Chemical Computation*, ACS, p. 63. [verified, bibliographic data only] The transition-state-theory rate is an equilibrium flux through a dividing surface, the same structure as Rice's formula applied to a stationary law (general knowledge, not checked in these papers).
- Consequence: the formula itself is prior art. The claim of this work is only its application to the law produced by a snapshot generator, with "no earlier application found in our search (2026-11-11, shallow search)".


## Entries added on 2026-11-12 (race pilot, experiment E4)

Checked by the `biblio` agent on 2026-11-12 (about 17 web requests; arXiv abstract pages, ar5iv HTML and Crossref; the page text was summarised by the fetch tool, so quotations are as returned by it and must be re-read in the PDF before being quoted verbatim).

**Salimans & Ho (2022).** T. Salimans, J. Ho, "Progressive Distillation for Fast Sampling of Diffusion Models", ICLR 2022, arXiv:2202.00512. [verified]
- Section 4 "Diffusion model parameterization and training loss" lists the parameterization "Predicting v ≡ α_t ε − σ_t x", with x̂ = α_t z_t − σ_t v̂_θ(z_t). [verified, ar5iv HTML] The abstract only says "new parameterizations of diffusion models that provide increased stability when using few sampling steps": cite Section 4, not the abstract. Appendix D (DDIM derivation) not checked.
- Use here: `src/milady/train/diffusion.py` (v-prediction on a trigonometric variance-preserving path).

**Song, Meng & Ermon (2021).** J. Song, C. Meng, S. Ermon, "Denoising Diffusion Implicit Models", ICLR 2021, arXiv:2010.02502. [verified, abstract]
- DDIMs "define a class of non-Markovian diffusion processes" with the same training objective as DDPMs; samples 10 to 50 times faster in wall-clock time. [verified, abstract]
- That the σ_t = 0 member is a **deterministic** sampler is in the body, not in the abstract. [UNCONFIRMED: body not opened] Do not cite "deterministic sampler (Song et al. 2021)" without checking the section.

**Brandenburg (2001).** A. Brandenburg, "The inverse cascade and nonlinear alpha-effect in simulations of isotropic helical hydromagnetic turbulence", *Astrophys. J.* **550**, 824–840 (2001), arXiv:astro-ph/0006186, DOI 10.1086/319783. [verified]
- Abstract: helically forced turbulence in a periodic box "generates a strong large-scale magnetic field at the box scale", nearly force-free and stronger than equipartition; a higher magnetic Reynolds number gives a longer time to build the large-scale field. [verified, abstract]
- Section III.6: "the growth of the large scale field is limited by the microscopic resistivity"; saturation time increases with Rm. [verified, ar5iv] [corrected: "saturation on a resistive time scale" is a paraphrase, not the paper's wording]
- Section III.3: magnetic helicity of opposite sign at large scales. [UNCONFIRMED wording: quotation returned by the fetch tool without certainty]
- Section I attributes the inverse cascade of magnetic helicity to Frisch et al. (1975) and Pouquet et al. (1976). [verified, ar5iv]

**Pouquet, Frisch & Léorat (1976).** A. Pouquet, U. Frisch, J. Léorat, "Strong MHD helical turbulence and the nonlinear dynamo effect", *J. Fluid Mech.* **77**(2), 321–354 (1976), DOI 10.1017/S0022112076002140. [verified, bibliographic data via Crossref]
- The inverse cascade of magnetic helicity is attributed to this paper by Brandenburg (2001, Section I); the statement itself was not read in the paper. [UNCONFIRMED at primary level]

**Brandenburg & Subramanian (2005).** A. Brandenburg, K. Subramanian, "Astrophysical magnetic fields and nonlinear dynamo theory", *Phys. Rep.* **417**, 1–209 (2005), arXiv:astro-ph/0405052, DOI 10.1016/j.physrep.2005.06.005. [verified, bibliographic data]
- Section 3.4 "Magnetic helicity", Eq. (3.34): dH/dt = −2∫E·B dV + surface terms = −2ηC with C = ∫J·B dV; the surface terms vanish in closed domains. [verified with a caveat: from the fetch tool's summary of the ar5iv page, not a verbatim read; re-read Eq. (3.34) before quoting] The sign and the factor 2 are those of the identity d⟨A·B⟩/dt = −2η⟨j·B⟩ used in E4, which `tests/test_constraints.py::test_stationarity_identities` checks against the solver independently of this reference.

**Zeros of a Gaussian random vector field (Kac–Rice).** J.-M. Azaïs, M. Wschebor, *Level Sets and Extrema of Random Processes and Fields*, Wiley, 2009, ISBN 978-0-470-40933-6. [UNCONFIRMED: seen as a search result only; no DOI found] Survey found but not opened: Berzin, Latour, León, "Kac-Rice formula: A contemporary overview", arXiv:2205.08742. [UNCONFIRMED] Adler & Taylor (2007) not searched. Consequence: the constant of the null-count estimate N ≈ 4.88 k_λ³ (physicien, 2026-11-12, own Monte Carlo) has no verified source; present it as a conjecture.

**Prior art for the E4 constraints and metrics (search of 2026-11-12, WebSearch only; a "not found" is not a proof of novelty).**
- Magnetic helicity budget or the identity E[⟨j·B⟩] = 0 as a loss or constraint of a generative model of MHD fields: nothing found. Number or type of magnetic null points as an evaluation metric of a generative model: nothing found (null points appear only in physics papers, e.g. arXiv:1509.05915, arXiv:2406.06328, not opened). [UNCONFIRMED, negative claims]
- "Restart" test (generated snapshots advanced by the solver, drift of an invariant measured): nothing found in MHD. Closest in fluids: arXiv:2508.04318, "Turbulent Injection assisted by Diffusion Models for Scale Resolving Simulations" (diffusion model trained on decaying homogeneous isotropic turbulence, samples injected as inlet conditions; the search snippet reports spectra and autocorrelations, not a drift of an invariant). [UNCONFIRMED: not opened; open it before claiming that no restart-type test exists there]
- Flow matching against diffusion at equal budget for turbulence or MHD fields: no published comparison found. Closest: X. Dong, H. Yang, J.-L. Wu, arXiv:2602.17089 (2D Kolmogorov flows; favours flow matching in a latent space for fast sampling: a speed claim) [verified, abstract]; H. Wang et al., "FourierFlow", arXiv:2506.00862 (argues that diffusion models suffer from spectral bias; no matched-budget comparison in the abstract) [verified, abstract]; arXiv:2511.19379 (MNIST, low step budgets) [UNCONFIRMED, snippet only].
- Székely & Rizzo (2013) is already in `data-metrics.md` (§ energy distance), [verified]; not re-checked.
