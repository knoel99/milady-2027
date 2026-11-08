# The machine-learning and generative-modelling landscape around MilaDy (2018-2026)

A map of the community's tracks, what each one does and does not solve for turbulent dynamos, the supervisors' published contributions, and the exact gaps that the internship and the thesis address, each with its closest prior work.

Prepared 2026-11-08 for the MilaDy explainer film and learning kit. English. Not a site page: this is a fact base for the script writers.

## 0. How to read this file

**Status tags** (every bibliographic entry in section 10 carries one):

- `[V-API]`: authors, year, title, venue, volume and pages or article number re-checked on 2026-11-08 in the Crossref API (DOI) or the arXiv API (identifier; journal-ref and comment fields read).
- `[V-WEB]`: venue checked on 2026-11-08 on a proceedings or conference page (URL given in section 10).
- `[ABS]`: the description of the content comes from the abstract read on 2026-11-08 (arXiv API, Crossref or HAL API).
- `[SITE f:l]`: the content claim comes from the repository, file `f`, line `l`. Those files were themselves checked against primary sources on 2026-11-06 (see their headers).
- `[SYNTHESIS]`: my own reading or comparison, not a statement of the cited authors.
- `[UNVERIFIED]`: could not be confirmed today.

**Abbreviations for repository files** (all paths relative to `/home/user/milady-2027/`):
`T` = `en/these/index.qmd`; `R` = `en/rapport/index.qmd`; `E` = `en/encadrants/index.qmd`; `L` = `specs/sources/litterature.md`; `S` = `specs/sources/encadrants.md`; `M` = `specs/sources/donnees-metriques.md`; `P8` = `en/prep/p8-contraintes-physiques/index.qmd`.

**Method.** I started from the site's literature (T 1.4 table, R section 2 and contributions, E "What remains to be done", L, S, M), re-checked 89 DOIs in Crossref (8 more located by bibliographic query) and 67 arXiv identifiers in the arXiv API (all resolved, no error), checked venues of conference papers on proceedings pages, and ran web and arXiv-API searches for what the site does not cover: ML for MHD and dynamos specifically (reversal prediction, reduced models, learned dynamo closures), the GAN era, equivariant generative models, and generative data assimilation. Raw verification logs: `video/plan/soa/ (copies de travail non versionnées pour dl/ et work/) verify/` (`dois.out`, `arxiv.out`, `abstracts1.txt`).

## 1. Four stress tests that a method must pass to be useful for dynamos

Each track below is judged against these four properties of the MilaDy problem.

1. **3D.** A self-sustained dynamo needs three dimensions: the 2D configuration is ruled out by Zel'dovich's anti-dynamo theorem (1957, recalled by Tobias 2021) [SITE R:240]. 2D MHD is a test bench, not a dynamo.
2. **Bounded domain and non-Cartesian data.** VKS and DRESDYN are walled cylinders, with a vacuum (or conducting) exterior, permeability jumps in soft-iron impellers ($\mathbf{B}\cdot\mathbf{n}$ and the tangential part of $\mathbf{B}/\mu_r$ continuous), and SFEMaNS data are azimuthal Fourier modes on an unstructured meridian finite-element mesh [SITE T:111-117; R:143-145]. Boundary conditions shift the threshold by about 40% ($Rm_c = 90 \pm 5$ with pseudo-vacuum against $130 \pm 10$ with vacuum, Nore et al. 2018) [SITE R:143].
3. **Low magnetic Prandtl number.** Sodium has $Pm = 0.82\cdot10^{-5}$ at 120 °C, so $Re$ reaches several million at threshold [SITE R:137]; direct simulations are "typically restricted to Pm~1 regimes" (MilaDy postdoc offer) [SITE S:88]. The consortium's reference reversal run has $Re = 1594$, $Rm = 531$ [SITE R:161], hence $Pm = Rm/Re \approx 0.33$ (my arithmetic). No ML work in this map is trained at sodium-like $Pm$.
4. **Rare events.** Reversals are few per simulation; in VKS a reversal lasts about 5 s against mean polarity durations of 120 s and 50 s [SITE R:149]; the usable palaeomagnetic record over 0-2 Ma "contains only five reversals" (Gwirtz et al. 2022) [ABS]. Learning reversal statistics from time series is data-starved.

## 2. The map at a glance

| Track | What it does | Landmark works (2018-2026) | 3D | Bounded / non-Cartesian | Low Pm | Rare events |
|---|---|---|---|---|---|---|
| 1a Neural surrogates and operators | learn a deterministic map (state to next state, parameters to solution) | PINNs (Raissi et al. 2019); DeepONet (Lu et al. 2021); FNO (Li et al. 2021); Neural Operator (Kovachki et al. 2023); Kochkov et al. 2021; PDEArena (Gupta and Brandstetter 2023); MPP (McCabe et al. 2024); Poseidon (Herde et al. 2024) | yes (some) | mostly periodic grids | no | no (regress to the mean, see GenCFD) |
| 1b Benchmarks and datasets | shared data and pointwise metrics | PDEBench (Takamoto et al. 2022); The Well (Ohana et al. 2024), which includes 3D compressible MHD at $64^3$ and $256^3$ | yes | periodic boxes | no (interstellar-type MHD, not a lab dynamo) | no |
| 1c ML closures | learn subgrid stresses for LES | Duraisamy et al. 2019 (review); Beck et al. 2019; Maulik et al. 2019; Guan et al. 2023; Mohan et al. 2023 (hard divergence-free 3D CNN) | yes | periodic (Mohan: periodic HIT $128^3$) | indirect route only [SYNTHESIS] | no |
| 1d ML for MHD and plasmas | surrogates of MHD solvers | Rosofsky and Huerta 2023 (2D PINO, $Re\le250$); Gopakumar et al. 2024 (tokamak FNO); Kacmaz et al. 2025 (2D PINO plus diffusion, $Pm=1$); Duarte et al. 2025 (2D Orszag-Tang FNO, preprint); Jarolim et al. 2023 (coronal PINN); Kaptanoglu et al. 2021 (3D spheromak reduced models) | rarely | non-periodic cases exist (Jarolim: coronal volume), none in a dynamo geometry [SYNTHESIS] | no | no |
| 1e ML for dynamos | mean-field closures, reversal prediction, data-driven reduced models | Nauman and Nättilä 2019; Gwirtz et al. 2022; Yang and Schmid 2025 (convection reversals); Bousquet et al. 2026 (DQVU, PySINDy); Illarionov et al. 2026 (neural ODE, solar dynamo) | DNS input yes, models low-dimensional | via the DNS (Bousquet: SFEMaNS and LATU) | inherits DNS $Pm$ | addressed, with negative or partial results |
| 2 Generative models of physical fields | sample distributions of fields, conditionally | GAN era (tempoGAN 2018; Kim et al. 2021; Wu et al. 2020); diffusion and flow matching (DDPM, score SDE, EDM, FM, rectified flow, interpolants); turbulence: Shu et al. 2023, TurbDiff 2024, ACDM 2026, CoNFiLD 2024, GenCFD 2026, Galletti et al. 2026; weather: SEEDS 2024, GenCast 2025, CorrDiff 2025 | yes (TurbDiff, CoNFiLD, GenCFD, PCDM) | partly (CoNFiLD, TurbDiff: complex geometry, no divergence constraint) | no | conditional sampling of user-defined events (Finzi et al. 2023); no dynamo |
| 3 Physics constraints in generative models | make samples satisfy laws | hard: Richter-Powell et al. 2022, PDM 2024, ECI 2025, PCFM 2025, PCDM 2026, Genuist et al. 2026, Li X. et al. 2026, FunDiff 2026; soft: PIDM 2025, DiffusionPDE 2024, CoCoGen 2025, PBFM 2026; distributional: Wu et al. 2020, Khalafi et al. 2024, WGS 2026, Tauberschmidt et al. 2026, Mun 2026; symmetry: Köhler et al. 2020, Klein et al. 2023 | PCDM only (periodic $64^3$) | no hard divergence constraint with walls found | no | no |
| 4 Generative priors in data assimilation | Bayesian posterior sampling with a learned prior | latent DA (Amendola et al. 2021; Peyron et al. 2021; Cheng et al. 2023 GLA; TorchDA 2025); score-based (SDA 2023; Rozet et al. 2024; DiffDA 2024; EnSF 2024; Zhuang, Cheng, Duraisamy 2025; Bocquet, Finn, Cheng 2026); geomagnetic DA with dynamo models (Fournier et al. 2010) | weather-scale yes | yes for weather grids | no | posterior multimodality not studied for MHD [SYNTHESIS] |

## 3. Track 1: machine learning for turbulence and MHD

### 3.1 Neural surrogates and neural operators

- **PINNs.** Raissi, Perdikaris and Karniadakis (2019) solve forward and inverse PDE problems by putting the PDE residual in the loss [V-API]. The physics is a soft penalty. Lucor's group uses PINNs for turbulent natural convection and relaxes the incompressibility constraint to ease optimization (Lucor, Agrawal, Sergent 2022) [SITE S:188-190].
- **Operator learning.** DeepONet (Lu et al. 2021) [V-API] and the Fourier Neural Operator (Li et al. 2021, ICLR) [V-API, V-WEB] learn maps between function spaces; FNO is "the first ML-based method to successfully model turbulent flows with zero-shot super-resolution" and is "up to three orders of magnitude faster" than classical solvers on its benchmarks [ABS]. Kovachki et al. (2023, JMLR) give the general framework [V-API]. FNO relies on FFTs over a regular grid, hence periodic or padded Cartesian domains [SYNTHESIS].
- **Learned solvers and foundation models.** Kochkov et al. (2021, PNAS) accelerate CFD with machine learning [V-API, title only]. PDEArena (Gupta and Brandstetter, TMLR 2023) compares FNO, ResNet and U-Net families on fluid problems [V-WEB]. Multiple Physics Pretraining (McCabe et al., NeurIPS 2024) pretrains one transformer on heterogeneous systems [V-API, ABS]; Poseidon (Herde et al., NeurIPS 2024) is a PDE foundation model [V-API].
- **Limit for dynamos.** These models are trained to minimize mean-square error. GenCFD shows that "ensembles of deterministic ML algorithms, trained to minimize mean square errors, regress to the mean flow" on 3D turbulence (Molinaro et al. arXiv; published as Raonić et al. 2026) [ABS]. A regression-to-the-mean surrogate cannot represent a bimodal $\pm\mathbf{B}$ distribution [SYNTHESIS].

### 3.2 Benchmarks and datasets

- PDEBench (Takamoto et al., NeurIPS 2022 Datasets and Benchmarks) [V-API] and The Well (Ohana et al., NeurIPS 2024 Datasets and Benchmarks) [V-API]. Their metrics are mostly deterministic (VRMSE, error per spectral band, error on a conserved quantity) [SITE R:232].
- The Well contains isothermal compressible 3D MHD turbulence without self-gravity, at $256^3$ and $64^3$ [SITE L:308], "of the interstellar-medium type, which is not a simulation of a laboratory dynamo" [SITE R:226]. Useful as a public 3D MHD test bench before consortium data [SITE L:386].
- I found no public ML benchmark of laboratory-dynamo or geodynamo simulations [SYNTHESIS, negative claim, not searched systematically]; the VKS reversal data of Bousquet et al. (2026) are "available from the authors upon reasonable request" [SITE R:161; S:235].

### 3.3 Machine-learned closures (and the first hard-constrained 3D CNN)

- Reviews: Duraisamy, Iaccarino and Xiao (2019) [V-API]; Brunton, Noack and Koumoutsakos (2020) [V-API].
- Subgrid models: Beck, Flad and Munz (2019, JCP) [V-API]; Maulik, San, Rasheed and Vedula (2019, JFM) for 2D turbulence [V-API]; Guan et al. (2023, Physica D) add a global constraint on enstrophy transfer in the small-data regime [SITE R:218]. Lucor's group: tensor-basis networks that respect Galilean and rotational invariance for Reynolds stresses (Cai et al. 2024) [SITE S:194].
- **Mohan, Lubbers, Chertkov and Livescu (2023, Phys. Rev. Fluids)** [V-API] embed incompressibility *by construction* in a convolutional autoencoder for 3D homogeneous isotropic turbulence ($128^3$): the decoder outputs a vector potential $\tilde{\mathbf{A}}$ and a last CNN layer applies a finite-difference curl, so the output is divergence-free; boundary conditions are periodic and no gauge is fixed (text of arXiv:2002.00021v2, read today, lines on the Helmholtz decomposition, "the boundary conditions are periodic", "Our approach did not specify a gauge"). Already listed on the site [SITE M:431]. It is not generative, but it is the closest 3D precedent for the thesis's vector-potential decoder (Q1).
- **Limit for dynamos.** Closures are one route toward high $Re$ at fixed $Rm$, which is what low $Pm$ demands [SYNTHESIS]; the consortium already uses LES at high $Re$ (Nore et al. 2018) [SITE S:223-225] and Ponty et al. (2005) combined DNS, a Lagrangian-averaged model and LES to reach $Pm$ down to $10^{-2}$ [SITE S:279-280]. No learned closure for the induction equation of a dynamo was found; a 2024 APS DPP abstract on learned EMF subgrid models in reconnection exists but is a conference abstract only [UNVERIFIED content].

### 3.4 Machine learning for MHD and plasmas

- **Rosofsky and Huerta (2023, Mach. Learn.: Sci. Technol. 4, 035002)**: "first application of physics informed neural operators" to 2D incompressible MHD; accurate for laminar flows with $Re\le250$ [V-API, ABS].
- **Kacmaz, Huerta and Haas (2025, Mach. Learn.: Sci. Technol. 6, 035057)**: PINO for low frequencies plus a conditional diffusion model for high-frequency correction, 2D resistive incompressible MHD, $128^2$, $Pm = 1$, $Re$ from 100 to 10,000; relative $L^2$ error 0.2548 to 0.1033 at $Re = 1000$; $\nabla\cdot\mathbf{B} = 0$ only guaranteed by the solver (vector potential in Dedalus), not by the generator; no helicity [V-API; SITE L:301; R:226]. The site's closest MHD generative work.
- **Duarte, Nemmen and Santos-Lima (2025, arXiv:2507.01388, submitted to JCP)**: FNO for the 2D Orszag-Tang vortex across viscosities and magnetic diffusivities; spectra and dissipation within 96%, degradation at the smallest scales [V-API, ABS]. Preprint.
- **Gopakumar et al. (2024, Nucl. Fusion 64, 056025)**: FNO surrogates of tokamak plasma evolution "both in simulation and experimental domains", "six orders of magnitude" speed-up over the MHD solvers [V-API, ABS].
- **Jarolim et al. (2023, Nat. Astron. 7, 1171-1179)**: PINN for force-free coronal field extrapolation; the preprint describes minimizing the Lorentz force and the divergence in the volume as loss terms [V-API; loss terms from a web search summary of the preprint, UNVERIFIED in the published text]. Soft $\nabla\cdot\mathbf{B}$.
- **Kaptanoglu, Morgan, Hansen and Brunton (2021, Phys. Rev. E 104, 015206)**: low-dimensional Galerkin models of (Hall-)MHD with an energy inner product, then data-driven models from 3D spheromak simulations, "physics-informed machine learning constrained by global conservation laws" [V-API; content from the arXiv abstract via web search].
- **Scheinker (2026, arXiv:2608.00675)**: a conditional latent diffusion model stepping compressible MHD forward and backward in time, used to predict its own rollout error [V-API, ABS]. Preprint; no constraint on $\nabla\cdot\mathbf{B}$ is mentioned in the abstract.

### 3.5 Machine learning for dynamos specifically

Four sub-tracks exist. None uses a diffusion or flow-matching model on dynamo simulations (section 8, gap G1).

**(a) Learned closures of mean-field dynamo theory.**
- Nauman and Nättilä (2019, A&A 629, A89): helically forced turbulence DNS; the form of the turbulent EMF is learned by regularized linear regression and random forests; "regularized linear regression outperforms ensemble methods" (title) [V-API; content from web search summary].
- Illarionov, Kisielius, Stepanov and Kuzanyan (2026, Phys. Rev. E 113, L053202; arXiv:2603.10548): the $\alpha$-quenching function of a low-mode solar dynamo is a neural network inside neural differential equations fitted to sunspot data [V-API, ABS]. Note: author order differs between arXiv (Illarionov, Stepanov, Kuzanyan, Kisielius) and Crossref (Illarionov, Kisielius, Stepanov, Kuzanyan); cite the journal order.

**(b) Data-driven reduced models of reversals and bursts.**
- SINDy (Brunton, Proctor and Kutz 2016, PNAS) [V-API]; constrained sparse Galerkin regression (Loiseau and Brunton 2018, JFM 838, 42-67), which imposes energy-preserving quadratic constraints [V-API]; SINDy autoencoders (Champion et al. 2019) and Koopman autoencoders (Lusch et al. 2018) [V-API; SITE L:334-341].
- **Bousquet, Ponty, Botez, Plihon and Nore (2026, Phys. Rev. Fluids 11, 063703)**: reversals in VKS simulations with both consortium solvers; POD on 2000 snapshots gives four axisymmetric modes (dipole, quadrupole, two velocity modes); the DQVU Galerkin model, identified by constrained regression with PySINDy (quadratic Navier-Stokes constraint and conservation of a third-order moment), reproduces the asymmetric bimodal distribution of $V$, which DQV does not [V-API; SITE R:161; S:227-235]. This is the consortium's own anchor for track 1e.
- Yang and Schmid (2025, JFM 1011, A30): complex-network reduced model from snapshots, "robust in detecting and quantifying structures and predicting reversals" in 2D turbulent thermal convection [V-API, ABS]. Cited in the MilaDy postdoc offer [SITE S:90].
- Lab-dynamo time series: reservoir computers trained on Hall-sensor data of the Three-Meter liquid-sodium experiment appear in APS conference abstracts (DFD 2017, March Meeting 2018) only [UNVERIFIED: no peer-reviewed paper found].

**(c) Predicting reversals and rare events.**
- **Gwirtz, Davis, Morzfeld, Constable, Fournier and Hulot (2022, GJI 231(1), 520-535)**: support vector machines and LSTMs trained on axial-dipole time series, from simplified models to 3D geodynamo simulations and two palaeomagnetic reconstructions; standard classifiers needed a rare-event modification; conclusion: "the ML techniques we tried are not currently capable of reliably identifying an axial dipole moment (ADM) precursor for geomagnetic reversals", largely because the record is short and coarse [V-API, ABS (HAL abstract)].
- Nakano, Sato and Toh (2024, Earth Planets Space 76, 121): echo state network for short-term prediction of geomagnetic secular variation [V-API; title only].
- Generic tools: reservoir computing for large chaotic systems (Pathak et al. 2018, PRL) [V-API]; ML prediction of extreme events (Qi and Majda 2020, PNAS) [V-API]; rare-event algorithms coupled with learned committor functions (Lucente, Rolland, Herbert, Bouchet 2022, J. Stat. Mech.) [V-API]. No application of rare-event algorithms to dynamo reversals was found [SYNTHESIS from a web search, negative claim].

**(d) Learning dynamics through invariant measures (bridge to the thesis's stationarity identities).**
- Yang et al. 2023 (SIADS); Botvinick-Greenhouse, Martin and Yang 2023 (Chaos); Jiang et al. 2023 (NeurIPS); DySLIM (Schiff et al. 2024, ICML); Chen et al. 2026 (Physica D) [V-API; SITE T:148; R:218].
- Cheng's co-authored work: PFNN, "Learning Chaos in a Linear Way" (Cheng X. et al., ICLR 2025), an autoencoder plus linear operator respecting contraction and measure invariance [V-API; SITE S:153]; Xue et al. (2026, Nat. Commun. 17, 9243), a neural operator for lattice Boltzmann with "moment-matching" constraints and global equivariance [V-API; SITE S:150].

**Geomagnetic data assimilation with dynamo models (non-ML, but the historical precedent).** Fournier et al. (2010, Space Sci. Rev. 155, 247-291) review sequential and variational assimilation with 3D geodynamo models and quasi-geostrophic models, and estimate predictability limits [V-API, content from web search of the abstract].

### 3.6 What track 1 solves and does not solve for dynamos

- Solves: fast deterministic surrogates on periodic grids; learned closures; low-dimensional reduced models of reversals identified from DNS time series (Bousquet et al. 2026); a demonstration that reversal precursors are hard to learn from short records (Gwirtz et al. 2022).
- Does not solve: [SYNTHESIS] distributions (mean-square losses regress to the mean, see GenCFD); exact $\nabla\cdot\mathbf{B} = 0$ in MHD surrogates (Kacmaz: solver only; Jarolim: penalty); bounded domains with vacuum matching and $\mu_r$ jumps; sodium-like $Pm$ (all MHD surrogates found are at $Pm = 1$ or laminar $Re$); and reversal statistics from data that contain few events.

## 4. Track 2: generative models for physical fields

### 4.1 The GAN era (2014-2021)

- GANs: Goodfellow et al. (2014, NIPS 27) [V-WEB].
- Fluids: tempoGAN (Xie, Franz, Chu and Thuerey 2018, ACM TOG 37(4)): conditional GAN for temporally coherent 3D volumetric super-resolution of fluid flows [V-API, ABS]. Kim, Kim, Won and Lee (2021, JFM 910, A29): CycleGAN trained on unpaired data for super-resolution of homogeneous turbulence and channel flow, including LES to DNS-quality fields [V-API; content from web search summary of the paper]. Deterministic CNN super-resolution precedent: Fukami, Fukagata and Taira (2019, JFM 870) [V-API, ABS].
- **Statistical constraints already in GANs:** Wu et al. (2020, JCP 406, 109209) impose the covariance of the data on an adversarial generator of Rayleigh-Bénard convection [V-API; SITE R:218]. Earliest distributional constraint on a generator of turbulent fields in this map.
- Cheng's generative precedent: a 3D VQ-VAE that generates unseen spatio-temporal wildfire sequences conditioned on vegetation and slope, used to train surrogates (Cheng, Guo, Arcucci 2023, IEEE TETCI) [V-API; SITE S:135].

### 4.2 Diffusion, score-based models, flow matching and stochastic interpolants (2020-2025)

DDPM (Ho, Jain, Abbeel 2020); score SDE (Song et al. 2021, ICLR); EDM (Karras et al. 2022); classifier-free guidance (Ho and Salimans 2022); flow matching (Lipman et al. 2023); rectified flow (Liu, Gong, Liu 2023); stochastic interpolants (Albergo and Vanden-Eijnden 2023; Albergo, Boffi, Vanden-Eijnden 2025, JMLR); OT-CFM (Tong et al. 2024, TMLR); function-space versions: Functional Flow Matching (Kerrigan et al. 2024, AISTATS) and Denoising Diffusion Operators (Lim et al. 2025, JMLR) [all V-API; SITE R:177; L:107-136]. The internship's experiments E1 and E2 use conditional flow matching [SITE T:88-90].

### 4.3 Conditional generation of turbulent fields and super-resolution

- Shu, Li and Barati Farimani (2023, JCP 478): physics-informed diffusion for flow-field reconstruction (2D Kolmogorov, $Re = 1000$) [V-API; SITE L:180-186].
- TurbDiff (Lienen et al. 2024, ICLR): 3D turbulent states without an initial state, $192\times48\times48$ LES, about 20 s per sample against about 602 s for the solver, no explicit incompressibility constraint [V-API; SITE L:193-198].
- ACDM (Kohl, Chen and Thuerey 2026, Neural Networks 199): autoregressive conditional diffusion conditioned on $Re$ and Mach, tested outside the training range; no physical constraint [V-API; SITE L:200-205].
- Gao et al. (2024, CMAME 427) [V-API]; CoNFiLD (Du et al. 2024, Nat. Commun. 15): neural-field latent diffusion on irregular 2D and 3D geometries (channel $Re_\tau = 180$), no explicit divergence constraint [V-API; SITE L:210-214].
- Synthetic Lagrangian turbulence (Li T. et al. 2024, Nat. Mach. Intell.) [V-API; SITE L:232].
- **GenCFD** (Molinaro et al. arXiv 2024; published as Raonić, Molinaro, Lanthaler et al. 2026, Nat. Commun. 17, 9846): conditional score-based diffusion for statistics of 3D turbulent flows; deterministic ensembles regress to the mean [V-API, ABS].
- **Galletti et al. (2026, arXiv:2607.13022)**: latent flow matching that generates statistically steady states of gyrokinetic turbulence conditioned on dimensionless parameters, bypassing the transient to warm-start the solver; "no physical constraint is mentioned" [V-API, ABS; SITE R:183]. The closest analogue to a *snapshot* generator of saturated states.
- **FunDiff** (Wang, Dou, Shan, Liu and Lu 2026, Nat. Commun. 17, 5749), the offer's main reference: functional autoencoder plus latent DiT trained by rectified flow; stream-function decoder in 2D; T.-R. Liu is at Laboratoire Navier, ENPC [V-API; SITE L:140-160].
- Conditional sampling of rare user-defined events: Finzi et al. (2023, ICML): approximate conditional score that "matches data statistics even when sampling from the tails of the distribution" for chaotic systems [V-API, ABS].
- Cheng's contributions: score-based diffusion with cross-attention for global field reconstruction from sparse, moving sensors; diffusion wins in noisy conditions, the deterministic method in noise-free ones (Zhuang, Cheng, Duraisamy 2025, CMAME 435) [V-API; SITE S:137]; the first denoising diffusion surrogate for wildfire spread, with ensemble sampling (Yu, Ghosh, Finn, Arcucci, Bocquet, Cheng 2026, GMD 19) [V-API; SITE S:139].
- Review: Biferale and Buzzicotti (2026, arXiv:2610.35123, submitted to JFM Perspectives) argue for validation on energy transfer, structure functions, PDF tails and conservation laws; MHD appears only as a recommended data layer, with no MHD metric [V-API; SITE L:233].

### 4.4 Ensemble emulation in weather (the "GenCast-style" track)

- SEEDS (Li, Carver, Lopez-Gomez, Sha and Anderson 2024, Sci. Adv. 10, eadk4489): diffusion emulation of operational ensembles [V-API; SITE L:228].
- GenCast (Price et al., Nature 637, 84-90, online 2024, issue 2025): conditional diffusion on an icosahedral mesh, better than ENS on 97.2% of 1320 targets, no explicit physical constraint [V-API; SITE L:227].
- CorrDiff (Mardani et al. 2025, Commun. Earth Environ. 6, 124): residual corrective diffusion for km-scale downscaling [V-API; title only].
- Relevance [SYNTHESIS]: the proof that diffusion ensembles can reproduce calibrated uncertainty at scale; but on the sphere or regional grids, with no MHD and no conserved-flux constraint.

### 4.5 Generative models for MHD and astrophysical magnetic fields

Kacmaz et al. 2025 (section 3.4); da Silva, Kirk, Mathews and Muñoz-Jaramillo (2025, arXiv:2510.01441): diffusion on spherical-harmonic coefficients of a coronal potential field, so $\nabla\cdot\mathbf{B} = 0$ by representation, qualitative evaluation [V-API, ABS; SITE R:195; L:303]; Martin et al. (2025, ApJS 277, 48): test-particle trajectories in 3D MHD turbulence [V-API; SITE R:226]; Scheinker 2026 (section 3.4). Search on 2026-11-08 (arXiv API: "dynamo" with "flow matching", "diffusion model", "score-based", "denoising diffusion" in abstracts; web search) found no diffusion or flow-matching model trained on dynamo simulations, which agrees with the site [SITE R:228; T:163]; this remains a negative claim.

### 4.6 What track 2 solves and does not solve for dynamos

- Solves: sampling of turbulent statistics instead of regression to the mean (GenCFD); 3D generation (TurbDiff, CoNFiLD, GenCFD, PCDM); conditioning on physical parameters (ACDM, Galletti); ensembles at operational scale (GenCast).
- Does not solve [SYNTHESIS]: MHD dynamo fields; exact $\nabla\cdot\mathbf{B}$; joint conditioning on $(Re, Rm)$ and crossing of a bifurcation [SITE R:244]; statistics of rare reversals at fixed data budget; evaluation with MHD metrics (helicity, field topology, magnetic budgets) [SITE R:243].

## 5. Track 3: physics constraints in generative models

### 5.1 Hard constraints by construction (architecture or representation)

- Divergence-free networks from differential forms, universal on the torus, cost quadratic in dimension (Richter-Powell, Lipman and Chen 2022, NeurIPS) [V-API; SITE L:239-243].
- Stream function in 2D (FunDiff 2026); potential field in spherical harmonics (da Silva et al. 2025) [SITE R:195-197].
- Vector potential plus curl in a 3D CNN, periodic, no gauge fixed (Mohan et al. 2023) [V-API; text read today].
- Leray projection of the denoiser's clean estimate in 3D periodic rotating turbulence at $64^3$, zero divergence to machine precision, about five times shorter training (PCDM, Li, Buzzicotti, Bonaccorso and Biferale 2026, preprint) [V-API; SITE R:193; L:282-287].
- Divergence-free Gaussian reference measure so flow-matching paths stay in the constrained space, divergence $O(10^{-7})$ (Li X. et al. 2026, preprint) [V-API; SITE L:289-292].
- PDE-constrained layers by differentiable optimization (Négiar, Mahoney and Krishnapriyan 2023, ICLR) [V-API, ABS]; integral conservation laws via a Bayesian update (ProbConserv, Hansen et al., ICML 2023 and Physica D 457, 2024) [V-API, ABS].

### 5.2 Hard constraints by projection or correction at sampling time

Projected diffusion (Christopher, Baek, Fioretto 2024, NeurIPS 37, 89307-89333); mirror diffusion (Liu et al. 2023); reflected or barrier diffusion for inequality constraints (Fishman et al. 2023, TMLR); ECI, gradient-free correction for linear and value constraints (Cheng C. et al. 2025, ICLR; no relation to S. Cheng found); PCFM, Gauss-Newton projection for nonlinear constraints (Utkarsh et al. 2025, NeurIPS) [all V-API; SITE R:191; L:244-273].

### 5.3 Soft penalties and guidance

PIDM (Bastek, Sun, Kochmann 2025, ICLR) and its Jensen-gap analysis; DiffusionPDE (Huang et al. 2024); CoCoGen (Jacobsen, Zhuang, Duraisamy 2025, SISC); DPS (Chung et al. 2023); universal guidance (Bansal et al. 2024); D-Flow (Ben-Hamu et al. 2024); PISD (Gallon et al. 2026, preprint) [all V-API; SITE R:179-187; L:162-191].
**New, not on the site:** PBFM, "Physics vs Distributions: Pareto Optimal Flow Matching with Physics Constraints" (Baldan, Liu, Guardone and Thuerey, ICLR 2026, arXiv:2506.08604, first titled "Flow Matching Meets PDEs"): enforces PDE residuals at training time with conflict-free gradient updates and unrolling against the Jensen gap; the authors claim to be "the first to recognize the trade-off between distributional and physical accuracy" [V-API, V-WEB, ABS].

### 5.4 Comparative studies

- **Genuist, Savin, Gatti and Clouteau (2026, arXiv:2601.19368, preprint)**: six ways to enforce incompressibility in an autoregressive EDM on decaying 2D turbulence with Ekman friction; the soft penalty "performs poorly across all metrics" in distribution and in rollout, but is best on out-of-distribution Taylor-Green ($4.53\cdot10^{-4}$ against $1.49\cdot10^{-3}$) with nonzero divergence ($1.84\cdot10^{-2}$); "no single strategy dominates" [V-API; SITE R:193; L:274-279]. The same authors' earlier preprint adds an energy constraint "rooted in the statistical properties of turbulent flows" (arXiv:2505.24145) [V-API, ABS; SITE L:280].
- PIDM against PG-Diffusion and CoCoGen on Darcy; PCFM against ECI, D-Flow and DiffusionPDE [SITE L:162-176, 268-273].
- PBFM's Pareto front between residual and Wasserstein distance on Darcy, Kolmogorov flow and dynamic stall [ABS; Darcy numbers from a web search summary, UNVERIFIED].
- The site's own comparison: E2 tests five mechanisms for $\nabla\cdot\mathbf{u} = 0$ (free, soft penalty, final Leray projection, projected flow, potentials) on periodic 2D MHD at $32^2$ [SITE T:90-93].

### 5.5 Distributional and statistical constraints

- Covariance constraint in a GAN (Wu et al. 2020) [V-API]; energy constraint from turbulence statistics (Genuist et al. 2025) [ABS].
- I-projection and exponential tilting with external moment targets: Csiszár 1975, Jaynes 1957, Pitera and Chodera 2012, Khalifa et al. 2021 (ICLR), Mun 2026 (preprint); constrained diffusion by duality (Khalafi, Ding, Ribeiro 2024, NeurIPS) [V-API; SITE T:149; R:220].
- Weak form of the stationary Fokker-Planck equation as a sampler loss, SDEs up to dimension 100, random Gaussian test functions (Weak Generative Sampler, Cai, Cao, Huang and Zhou 2026, SISC 48(4)); min-max antecedent WAN (Zang et al. 2020) [V-API; SITE T:147; R:218].
- Tilting a flow-matching model by a weak-form PDE residual used as a per-sample reward (Tauberschmidt, Fellenz, Vollmer and Duncan 2026, ICLR) [V-API; SITE T:149; E:507; M:384-389].
- Invariant-measure learning for emulators (section 3.5 d).

### 5.6 Symmetries and equivariant generative models

- A flow built from equivariant maps yields an invariant density (Köhler, Klein and Noé 2020, ICML, PMLR 119:5361-5370) [V-API, V-WEB]; already the reference for Proposition 4 on the site [SITE P8:347].
- Equivariant flow matching (Klein, Krämer and Noé 2023, NeurIPS 36, 59886-59910) [V-API]; equivariant diffusion for 3D molecules (Hoogeboom et al. 2022, ICML) [V-API].
- Symmetry in deep dynamics models for turbulence: translation, rotation, uniform motion and scale, on Rayleigh-Bénard and ocean data (Wang, Walters and Yu 2021, ICLR) [V-WEB; content from web search summary].
- Supervisors: equivariance relations between physical and latent symmetries, better preserved by VAEs (Bousquet, Nore and Lucor 2025, CPC 315) [V-API; SITE S:180-185].

### 5.7 What track 3 solves and does not solve for dynamos

- Solves: exact zero divergence in periodic 2D and 3D (Leray, potentials); exact linear and nonlinear constraints at sampling time in 1D and 2D PDEs (ECI, PCFM); trade-off analyses between soft and hard (Genuist 2026, PBFM 2026); invariant densities by equivariance (Köhler 2020).
- Does not solve [SYNTHESIS; SITE R:241-245; E:518]: a joint hard constraint on $\nabla\cdot\mathbf{u}$ and $\nabla\cdot\mathbf{B}$ in 3D; any hard divergence constraint with walls, a vacuum exterior and permeability jumps; constraints on a hybrid Fourier by finite-element representation; stationarity identities of a field PDE as distributional constraints without target values, conditioned on parameters.

## 6. Track 4: generative priors in data assimilation

### 6.1 Latent data assimilation (autoencoder priors)

- Amendola et al. (2021, LNCS, ICCS 2021): DA in the latent space of a convolutional autoencoder [V-API]. Peyron et al. (2021, QJRMS 147, 3759-3777) [V-API].
- Cheng's line: Generalised Latent Assimilation in heterogeneous reduced spaces, variational DA in the latent space with local surrogate observation operators and an error bound on the surrogate cost (Cheng et al., J. Sci. Comput. 94(1), 11, issue 2023, online 2022) [V-API; SITE S:127]; latent DA for wildfire (JCP 2022) [V-API; SITE S:129]; multi-domain encoder-decoders (CMAME 2024) [V-API; SITE S:133]; VIVID for sparse, time-varying sensors (JCP 496, 2024) [V-API; SITE S:131]; TorchDA, KF, EnKF, 3D-Var and 4D-Var with deep networks as forward and transformation operators, cited in the ANR abstract (CPC 306, 109359, 2025) [V-API; SITE S:141; S:57]; review of ML with DA and UQ, co-written with Lucor (IEEE/CAA JAS 2023) [V-API; SITE S:125]; Tensor-Var (ICML 2025) [SITE S:154].

### 6.2 Score-based and diffusion data assimilation

- SDA (Rozet and Louppe 2023, NeurIPS 36): trajectory score from local scores, observation model decoupled from training, tested on Kolmogorov flow [V-API; SITE L:216-219]. Learning diffusion priors from noisy, incomplete observations by expectation-maximization, with moment-matching posterior sampling (Rozet, Andry, Lanusse and Louppe 2024, NeurIPS 37) [V-API; content from web search of the proceedings page].
- DiffDA (Huang et al. 2024, ICML): weather-scale DA with a GraphCast-based denoiser [V-API; SITE L:221-224]. Generative DA of sparse weather-station data at km scales (Manshausen et al. 2024, arXiv preprint) [V-API, ABS].
- Ensemble Score Filter, training-free score estimation for high-dimensional filtering (Bao, Zhang and Zhang 2024, CMAME 432, 117447) [V-API, ABS]; Latent-EnSF with a coupled VAE (Si and Chen 2024, arXiv preprint) [V-API, ABS].
- Cheng's line: Zhuang, Cheng and Duraisamy 2025 (section 4.3); IEnKF-G, a one-step weak-constraint 4D-Var in which "a learned conditional stochastic forecast replaces the prescribed additive Gaussian model error" (Bocquet, Finn and Cheng 2026, arXiv:2610.17333) [V-API, ABS; SITE S:159]; benchmark of Koopman-type latent dynamics for DA (Zhang Z. et al. 2026, arXiv:2611.03916) [V-API; SITE S:161].

### 6.3 What track 4 solves and does not solve for dynamos

- Solves: DA with learned priors in high dimension and with sparse sensors; tooling in the consortium (TorchDA).
- Does not solve [SYNTHESIS]: no diffusion-based DA applied to MHD was found [SITE L:385]; the posterior near a reversal is bimodal in $\pm\mathbf{B}$, and a prior that does not respect $\mathbf{B}\to-\mathbf{B}$ would bias the analysis toward one polarity [SITE E:491]; magnetic probes outside the fluid observe a field whose interior is constrained by $\nabla\cdot\mathbf{B} = 0$ and the vacuum matching, which no generative prior encodes.

## 7. The supervisors' published contributions, track by track

Only what their publications show (no opinions, no plans). Sources: S (checked on 2026-11-06) and Crossref today.

| Supervisor | Track 1 (ML for turbulence, MHD, dynamos) | Track 2 (generative) | Track 3 (constraints) | Track 4 (DA) | Dynamo physics and data |
|---|---|---|---|---|---|
| **Sibo Cheng** (CEREA, ENPC) | multi-fidelity physics-constrained networks MSPCNN (Zhou, Cheng, Arcucci 2024) [S:143]; Koopman and invariant-measure learning, PFNN (ICLR 2025), "Information Shapes Koopman Representation" (ICLR 2026) [S:153-155]; neural operator with moment-matching and equivariance (Xue et al. 2026) [S:150]; review of ML on unstructured grids (Cheng et al. 2025, Information Fusion 123, 103255) [S:148] | 3D VQ-VAE wildfire generator (2023) [S:135]; diffusion for field reconstruction (Zhuang, Cheng, Duraisamy 2025) [S:137]; diffusion wildfire surrogate (Yu et al. 2026) [S:139]; generative air-quality and wind reconstruction preprints [S:162-163] | physics constraints in losses (MSPCNN; Voronoi-based DSOVT, Wang, Zhou, Cheng 2024) [S:143-146] | core: GLA, latent DA, VIVID, TorchDA, review with Lucor, Tensor-Var, IEnKF-G preprint, Koopman-DA benchmark preprint [S:125-161] | no dynamo publication found as of 2026-11-06 [S:103] |
| **Didier Lucor** (LISN, CNRS) | PINNs for turbulent convection with relaxed incompressibility (2022) [S:188]; PINN reconstruction from PIV (2025) [S:191]; invariant tensor-basis networks (Cai et al. 2024) [S:194]; AE and VAE latent spaces against POD, with symmetry and equivariance analysis (Bousquet, Nore, Lucor 2025) [S:180]; polynomial autoencoders initialized as POD (Research Square preprint 2026) [S:202]; parametric ROM for LES (Nony et al. 2023) [S:197] | none found | invariance and equivariance through architecture (Cai 2024; Bousquet 2025) | review with Cheng (2023); observation compression for variational DA (Cheng, Lucor, Argaud 2021) [S:156] | LES and POD of 3D von Kármán flows with Nore (Bousquet et al. 2024, metastable $R_\pi$-breaking state for $Re > 10^4$) [S:186] |
| **Caroline Nore** (LISN, Univ. Paris-Saclay; MilaDy coordinator) | POD and constrained-PySINDy reduced model DQVU of VKS reversals (Bousquet et al. 2026) [S:227-235]; POD of VKS growth and saturation (Botez, Bousquet, Nore 2025) [S:241]; AE and VAE interpretability (2025) [S:180]; co-directed a PhD on graph neural networks and DA (Quattromini 2024) [S:262] | none found | statistical constraint in identification (third-order moment conservation in DQVU) [S:234; E:487] | GNN-based DA thesis (co-direction) [S:262] | SFEMaNS DNS of VKS (2016, 2018) [S:221-226]; local energy transfers on unstructured meshes (Creff et al. 2024) [S:243]; precession dynamos for DRESDYN (Botez et al. 2026) [S:236-240] |
| **Yannick Ponty** (Lagrange, OCA, CNRS) | none: "no publication of Ponty on machine learning was found" [S:299] | none | none | none | dynamo at low $Pm$ down to $10^{-2}$ (2005) [S:279]; subcritical Taylor-Green dynamo (2007) [S:283]; on-off intermittency (Alexakis and Ponty 2008) [S:285]; LATU pseudo-spectral penalization solver (Kreuzahler et al. 2017) [S:288]; subcritical branches by nonlinear optimization (Mannix et al. 2022) [S:293]; kurtosis-skewness intermittency statistics (2025) [S:294]; VKS reversals (Bousquet et al. 2026) [S:297] |

Reading [SYNTHESIS]: the consortium already covers tracks 1e (reversal ROMs on its own DNS), 4 (DA) and the data side; it has a generative precedent outside MHD (Cheng) and a representation-learning precedent on von Kármán flows (Lucor, Nore). The missing piece is the intersection of tracks 2 and 3 applied to dynamo fields, which is exactly what the internship offer asks for [SITE S:69-76].

## 8. The precise gaps the internship and the thesis address

"I" = internship (prospective report, CPU experiments E1-E3, 1-2 seeds) [SITE T:84-105]; "T" = PhD proposal (questions Q1-Q4, tiers 0-4) [SITE T:107-136]. Each gap names its closest prior work and the difference.

| # | Gap | Internship (measured on toy cases) | Thesis (planned) | Closest prior work | What the prior work does not do |
|---|---|---|---|---|---|
| G1 | No diffusion or flow-matching generator of dynamo fields | E2: conditional generator of periodic 2D MHD on $\eta$; E3: kinematic 3D ABC dynamo without a generator [T:90-97] | tiers 2-4: ABC and Taylor-Green 3D, VKS (SFEMaNS, LATU), DRESDYN [T:906-950] | Kacmaz et al. 2025 (2D MHD, $Pm = 1$); Galletti et al. 2026 (steady gyrokinetic states, parameter-conditioned FM); GenCFD 2026 (3D turbulence statistics) | 2D cannot sustain a dynamo; no $\nabla\cdot\mathbf{B}$ in the generator; no magnetic field (Galletti, GenCFD) [R:240; L:301] |
| G2 | Joint hard $\nabla\cdot\mathbf{u} = \nabla\cdot\mathbf{B} = 0$ in 3D, in a bounded cylinder with vacuum matching, $\mu_r$ jumps and a Fourier by finite-element mesh | E2: potentials $(\psi, a)$ reach $1.8\cdot10^{-17}$ without quality loss; E3: curl form keeps $\nabla\cdot\mathbf{B} < 1.6\cdot10^{-16}$ in 3D periodic [T:92, 97] | Q1 [T:111-117] | PCDM 2026 (3D periodic Leray); Mohan et al. 2023 (3D vector potential, periodic, not generative, no gauge); FunDiff (2D stream function); Richter-Powell 2022 (torus); ECI and PCFM (boundary values, 1D-2D); Cheng et al. 2025 review (ML on unstructured grids) | none handles walls plus vacuum matching plus permeability kinks, nor $\mathbf{u}$ and $\mathbf{B}$ jointly [R:241-242; E:518] |
| G3 | Stationarity identities of a field PDE as distributional constraints on a parametric conditional generator, without target values, enforceable where there are no data | E1 and E2: stationarity loss; E2 mean energy-budget residual 0.46 to 0.061 and energy distance 2.52 to 0.70 at unseen $\eta$, still above the honest noise floor [T:94] | Q2 [T:119-124] | Weak Generative Sampler (Cai et al. 2026, SDEs, dimension at most 100, unconditional); Tauberschmidt et al. 2026 (weak residual, per sample); Khalifa 2021, Mun 2026, Khalafi 2024 (external targets); Wu et al. 2020 (data covariance in a GAN); DySLIM and invariant-measure learning (emulators) | none combines field PDE, conditioning on parameters, target-free identities and training at parameters without data [T:147-149, 156; R:120] |
| G4 | Inconsistency of per-sample constraints for a stationary budget (Corollary 6), measured | E2: per-sample rescaling cancels the residual but the dissipation spread falls to $8.6\cdot10^{-4}$ of the data; E1: per-sample projection multiplies the energy distance by 9 [T:88, 95] | measure on 3D dynamos [E:516] | **PBFM (Baldan et al., ICLR 2026)**, which claims to be "the first to recognize the trade-off between distributional and physical accuracy"; PIDM's Jensen-gap analysis; Genuist et al. 2026 | PBFM states a training trade-off for per-sample PDE residuals; it does not state that a constraint valid only in mean (a stationary budget) is inconsistent when imposed per sample [SYNTHESIS; ABS]. **Not cited on the site: the claim of novelty R:121 / T:157 should be re-checked against PBFM before any submission.** |
| G5 | Symmetry $\mathbf{B}\to-\mathbf{B}$ and $R_\pi$ by equivariance, and its complementarity with stationarity (identities do not fix the weights of symmetric ergodic components) | E1: equivariant field keeps asymmetry at noise floor (0.004) at unseen $\Gamma$; augmentation does not [T:88] | §2.4, extension to joint state-parameter action [T:151] | Köhler, Klein, Noé 2020; Klein et al. 2023; Wang, Walters, Yu 2021; Bousquet, Nore, Lucor 2025 (latent equivariance) | the complementarity with stationarity identities and the joint state-parameter action are not in these works [T:151, 159; R:123] |
| G6 | Reversal frequency from a snapshot generator via the Rice formula, without time integration, with its limits | E1: cumulative relative error 4-6% on the reference distribution, 14% on the generated one far from the threshold, 42% near it [T:88] | Q3 [T:126-131] | ML reversal prediction from time series: Gwirtz et al. 2022 (negative result), Yang and Schmid 2025 (2D convection); rare-event sampling in diffusion models: Finzi et al. 2023; rare-event algorithms with learned committors: Lucente et al. 2022; Rice 1944-45, Azaïs and Wschebor 2009 (theory) | all need trajectories or target event definitions; none turns a stationary snapshot distribution plus the right-hand side into a crossing frequency [T:158; R:122] |
| G7 | Error of a generator smooth in $\boldsymbol\lambda$ near a dynamo or reversal threshold (Proposition 9); conditioning across the threshold | E1: 42% Rice error near the threshold where the generator smooths the jump [T:88] | Q3; tier 2 threshold of ABC and Taylor-Green [T:126-131, 906-925] | ACDM (extrapolation in $Re$); Kacmaz (a model trained at $Re = 1000$ applied at $Re = 100$ has error above 0.85) [L:382]; Galletti (parameter conditioning) | no generative model studies the crossing of a bifurcation or conditions jointly on $(Re, Rm)$ [R:244; E:518] |
| G8 | Reduced models identified from generated snapshots and the right-hand side, without differentiating time series | none | Q4, DQVU [T:133-136] | Bousquet et al. 2026 (constrained PySINDy on DNS time series with Savitzky-Golay derivatives); Loiseau and Brunton 2018; Kaptanoglu et al. 2021 | they identify from time series; none from a generator [SYNTHESIS] |
| G9 | Generative prior for DA of $(\mathbf{u}, \mathbf{B})$ with a bimodal $\pm\mathbf{B}$ posterior | none | Q4 with TorchDA, months 25-27 [T:136; E:491] | SDA 2023; Rozet et al. 2024; EnSF 2024 and Latent-EnSF; Cheng et al. GLA and TorchDA; Zhuang, Cheng, Duraisamy 2025; Bocquet, Finn, Cheng 2026; Fournier et al. 2010 (geomagnetic DA) | no diffusion-based DA on MHD; no symmetry-respecting prior for polarity [L:385; E:491] |
| G10 | MHD metrics for generated fields (spectra, helicities, budgets, topology) | E2 metrics; the cross-helicity residual does not discriminate between models [R:1037] | common protocol §3.1 [T:859-876] | Lienen 2024 ($W_2$ on TKE spectra); GenCFD (CRPS, one-point distances); Biferale and Buzzicotti 2026; Creff et al. 2024 (local energy transfers, Nore); Ponty et al. 2025 (kurtosis-skewness) | no work evaluates magnetic or cross helicity, budgets or field-line topology of generated fields [R:243] |

**What neither the internship nor the thesis claims to solve** [SITE T:80, T:131, R:708; SYNTHESIS]: the distribution of waiting times between reversals (not determined by the stationary distribution; needs short trajectories from generated samples); sodium-like $Pm$ (the generator inherits the $Pm$ of the DNS it is trained on, about 0.33 in the reference VKS reversal run); the geodynamo; experimental VKS measurements (assimilation is planned from synthetic magnetic probes [E:491]); feasibility in 3D bounded domains, which E1-E3 do not demonstrate [T:105].

## 9. Suggested narrative spine for the film chapter (the user asked how the work fits the field)

[SYNTHESIS, for the script writers; every beat maps to sections above.]

1. Four communities each solved part of the problem: fast surrogates (track 1), samplers of turbulent statistics (track 2), constraint machinery (track 3), Bayesian assimilation with learned priors (track 4).
2. Dynamos break each of them on at least one of the four stress tests (section 1): 3D, walls and vacuum, low $Pm$, rare events.
3. The consortium already owns three ingredients: the simulations and reversal ROMs (Nore, Ponty), representation learning on von Kármán flows (Lucor, Nore), DA and generative surrogates (Cheng).
4. The internship builds the missing intersection on toy problems and measures where per-sample constraints fail (G2-G6).
5. The thesis moves it to 3D bounded geometry and to reversals (G1, G2, G6-G9), with honest limits (section 8, last paragraph).

## 10. New items for the lead (not on the site as of 2026-11-08)

Priority: **PBFM (Baldan et al., ICLR 2026)** bears on contribution 2 of R:121 and T:157 (see G4). Then, by relevance: Mohan et al. 2023 (already in M:431, absent from T and R: closest 3D vector-potential precedent for Q1); Gwirtz et al. 2022 (ML reversal precursors, negative result: frames Q3); Finzi et al. 2023 (diffusion rare-event sampling); Kaptanoglu et al. 2021 and Loiseau and Brunton 2018 (constrained data-driven MHD and Galerkin models, context of DQVU); Rozet et al. 2024, Bao et al. 2024, Si and Chen 2024, Manshausen et al. 2024 (generative DA); Nauman and Nättilä 2019, Illarionov et al. 2026 (ML for dynamo closures); Rosofsky and Huerta 2023, Duarte et al. 2025, Gopakumar et al. 2024, Scheinker 2026 (ML for MHD); McCabe et al. 2024, Herde et al. 2024 (foundation models); Wang, Walters and Yu 2021, Klein et al. 2023, Hoogeboom et al. 2022 (equivariance); Fournier et al. 2010 (geomagnetic DA).

## 11. Unverified points and caveats

- Jarolim et al. 2023: the divergence and Lorentz-force loss terms come from a search summary of the preprint, not from the published text [UNVERIFIED].
- PBFM Darcy numbers (residual 0.838 against 4.159 for FM-OT, Wasserstein 0.138) come from a search summary [UNVERIFIED]; the trade-off claim is from the arXiv abstract [ABS].
- Kim et al. 2021 (CycleGAN), Wang, Walters and Yu 2021, Nauman and Nättilä 2019, Kaptanoglu et al. 2021, Rozet et al. 2024, Fournier et al. 2010: content from web search summaries of the abstract or proceedings page; metadata [V-API] or [V-WEB].
- Three-Meter reservoir-computing work: APS conference abstracts only, no peer-reviewed paper found [UNVERIFIED].
- 2024 APS DPP abstract on learned EMF subgrid models: conference abstract only [UNVERIFIED].
- Mohan et al.: author order is Mohan, Lubbers, Livescu, Chertkov on arXiv and Mohan, Lubbers, Chertkov, Livescu in Crossref (journal); cite the journal order.
- Illarionov et al.: author order differs between arXiv and Crossref; cite Crossref.
- GLA (Cheng et al.): Crossref issue year 2023, online 2022; the site writes 2022.
- Negative claims (no generative model of dynamo fields; no rare-event algorithm applied to dynamo reversals; no diffusion DA on MHD) cannot be proven; today's arXiv-API and web searches did not contradict them.
- ECI's first author is Chaoran Cheng; no link to Sibo Cheng is implied.

## 12. References (full citations, grouped by track; status as of 2026-11-08)

Verification URLs: Crossref `https://api.crossref.org/works/<DOI>`; arXiv `https://export.arxiv.org/api/query?id_list=<id>`.

### Context and site anchors
- Bousquet R., Ponty Y., Botez V., Plihon N., Nore C. (2026). Magnetic field reversals in numerical simulations of the von Kármán sodium experiment. *Phys. Rev. Fluids* 11(6), 063703. DOI 10.1103/9tx2-1m13 [V-API]
- Botez V., Giesecke A., Nore C., Cappanera L., Stefani F. (2026). Impact of boundary conditions on onset and symmetry of precession-driven dynamos. *Phys. Rev. Fluids* 11(8), 083701. DOI 10.1103/rx1h-5zxp [V-API]
- Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2016). Direct numerical simulation of the axial dipolar dynamo in the Von Kármán Sodium experiment. *EPL* 114(6), 65002. DOI 10.1209/0295-5075/114/65002 [V-API]
- Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2018). Numerical simulation of the von Kármán sodium dynamo experiment. *J. Fluid Mech.* 854, 164-195. DOI 10.1017/jfm.2018.582 [V-API]
- Creff M., Faller H., Dubrulle B., Guermond J.-L., Nore C. (2024). Tracking dynamo mechanisms from local energy transfers: Application to the von Kármán sodium dynamo. *Phys. Plasmas* 31(2), 022306. DOI 10.1063/5.0174251 [V-API]
- Ponty Y., Mininni P. D., Montgomery D. C., Pinton J.-F., Politano H., Pouquet A. (2005). Numerical study of dynamo action at low magnetic Prandtl numbers. *Phys. Rev. Lett.* 94(16), 164502. DOI 10.1103/PhysRevLett.94.164502 [V-API]
- Ponty Y., Laval J.-P., Dubrulle B., Daviaud F., Pinton J.-F. (2007). Subcritical dynamo bifurcation in the Taylor-Green flow. *Phys. Rev. Lett.* 99(22), 224501. DOI 10.1103/PhysRevLett.99.224501 [V-API]
- Alexakis A., Ponty Y. (2008). Effect of the Lorentz force on on-off dynamo intermittency. *Phys. Rev. E* 77(5), 056308. DOI 10.1103/PhysRevE.77.056308 [V-API]
- Kreuzahler S., Ponty Y., Plihon N., Homann H., Grauer R. (2017). Dynamo enhancement and mode selection triggered by high magnetic permeability. *Phys. Rev. Lett.* 119(23), 234501. DOI 10.1103/PhysRevLett.119.234501 [V-API]
- Mannix P. M., Ponty Y., Marcotte F. (2022). Systematic route to subcritical dynamo branches. *Phys. Rev. Lett.* 129(2), 024502. DOI 10.1103/PhysRevLett.129.024502 [V-API]
- Ponty Y., Politano H., Pouquet A. (2025). Intermittency assessed through a model of kurtosis-skewness relation in MHD in fast dynamo regimes. *J. Plasma Phys.* 91(2), E69. DOI 10.1017/S0022377825000169 [V-API]
- Gissinger C. (2012). A new deterministic model for chaotic reversals. *Eur. Phys. J. B* 85(4), 137. DOI 10.1140/epjb/e2012-20799-5 [V-API]
- Berhanu M. et al. (14 authors) (2007). Magnetic field reversals in an experimental turbulent dynamo. *EPL* 77(5), 59001. DOI 10.1209/0295-5075/77/59001 [V-API]
- Pétrélis F., Fauve S. (2008). Chaotic dynamics of the magnetic field generated by dynamo action in a turbulent flow. *J. Phys.: Condens. Matter* 20(49), 494203. DOI 10.1088/0953-8984/20/49/494203 [V-API]

### Track 1: ML for turbulence, MHD and dynamos
- Raissi M., Perdikaris P., Karniadakis G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *J. Comput. Phys.* 378, 686-707. DOI 10.1016/j.jcp.2018.10.045 [V-API]
- Lu L., Jin P., Pang G., Zhang Z., Karniadakis G. E. (2021). Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators. *Nat. Mach. Intell.* 3(3), 218-229. DOI 10.1038/s42256-021-00302-5 [V-API]
- Li Z., Kovachki N., Azizzadenesheli K., Liu B., Bhattacharya K., Stuart A., Anandkumar A. (2021). Fourier neural operator for parametric partial differential equations. *ICLR 2021*. arXiv:2010.08895 [V-API; V-WEB https://iclr.cc/virtual/2021/poster/3281]
- Kovachki N., Li Z., Liu B., Azizzadenesheli K., Bhattacharya K., Stuart A., Anandkumar A. (2023). Neural operator: Learning maps between function spaces. *J. Mach. Learn. Res.* 24(89). arXiv:2108.08481 [V-API, journal-ref]
- Kochkov D., Smith J. A., Alieva A., Wang Q., Brenner M. P., Hoyer S. (2021). Machine learning-accelerated computational fluid dynamics. *PNAS* 118(21), e2101784118. DOI 10.1073/pnas.2101784118 [V-API]
- Gupta J. K., Brandstetter J. (2023). Towards multi-spatiotemporal-scale generalized PDE modeling. *TMLR*. arXiv:2209.15616 [V-API; V-WEB https://mlanthology.org/tmlr/2023/gupta2023tmlr-multispatiotemporalscale]
- McCabe M., Régaldo-Saint Blancard B., Parker L. H., Ohana R., Cranmer M., et al. (2024). Multiple physics pretraining for spatiotemporal surrogate models. *NeurIPS 37*, 119301-119335. DOI 10.52202/079017-3791; arXiv:2310.02994 [V-API]
- Herde M., Raonić B., Rohner T., Käppeli R., Molinaro R., de Bézenac E., Mishra S. (2024). Poseidon: Efficient foundation models for PDEs. *NeurIPS 37*, 72525-72624. DOI 10.52202/079017-2311; arXiv:2405.19101 [V-API]
- Takamoto M. et al. (2022). PDEBench: An extensive benchmark for scientific machine learning. *NeurIPS 2022 Datasets and Benchmarks*. arXiv:2210.07182 [V-API]
- Ohana R., McCabe M., Meyer L., Morel R., et al. (26 authors) (2024). The Well: a large-scale collection of diverse physics simulations for machine learning. *NeurIPS 37*, 44989-45037. DOI 10.52202/079017-1430 [V-API]
- Duraisamy K., Iaccarino G., Xiao H. (2019). Turbulence modeling in the age of data. *Annu. Rev. Fluid Mech.* 51, 357-377. DOI 10.1146/annurev-fluid-010518-040547 [V-API]
- Brunton S. L., Noack B. R., Koumoutsakos P. (2020). Machine learning for fluid mechanics. *Annu. Rev. Fluid Mech.* 52, 477-508. DOI 10.1146/annurev-fluid-010719-060214 [V-API]
- Beck A., Flad D., Munz C.-D. (2019). Deep neural networks for data-driven LES closure models. *J. Comput. Phys.* 398, 108910. DOI 10.1016/j.jcp.2019.108910 [V-API]
- Maulik R., San O., Rasheed A., Vedula P. (2019). Subgrid modelling for two-dimensional turbulence using neural networks. *J. Fluid Mech.* 858, 122-144. DOI 10.1017/jfm.2018.770 [V-API]
- Guan Y., Subel A., Chattopadhyay A., Hassanzadeh P. (2023). Learning physics-constrained subgrid-scale closures in the small-data regime for stable and accurate LES. *Physica D* 443, 133568. DOI 10.1016/j.physd.2022.133568 [V-API]
- Mohan A. T., Lubbers N., Chertkov M., Livescu D. (2023). Embedding hard physical constraints in neural network coarse-graining of three-dimensional turbulence. *Phys. Rev. Fluids* 8(1), 014604. DOI 10.1103/PhysRevFluids.8.014604; arXiv:2002.00021 [V-API]
- Rosofsky S. G., Huerta E. A. (2023). Magnetohydrodynamics with physics informed neural operators. *Mach. Learn.: Sci. Technol.* 4(3), 035002. DOI 10.1088/2632-2153/ace30a [V-API]
- Kacmaz S., Huerta E. A., Haas R. (2025). Resolving turbulent magnetohydrodynamics: A hybrid operator-diffusion framework. *Mach. Learn.: Sci. Technol.* 6(3), 035057. DOI 10.1088/2632-2153/ae054c [V-API]
- Duarte R., Nemmen R., Santos-Lima R. (2025). Spectral learning of magnetized plasma dynamics: A neural operator application. Preprint arXiv:2507.01388 [V-API]
- Gopakumar V., Pamela S., Zanisi L., Li Z., Gray A., Brennand D., et al. (13 authors) (2024). Plasma surrogate modelling using Fourier neural operators. *Nucl. Fusion* 64(5), 056025. DOI 10.1088/1741-4326/ad313a [V-API]
- Jarolim R., Thalmann J. K., Veronig A. M., Podladchikova T. (2023). Probing the solar coronal magnetic field with physics-informed neural networks. *Nat. Astron.* 7(10), 1171-1179. DOI 10.1038/s41550-023-02030-9 [V-API]
- Kaptanoglu A. A., Morgan K. D., Hansen C. J., Brunton S. L. (2021). Physics-constrained, low-dimensional models for magnetohydrodynamics: First-principles and data-driven approaches. *Phys. Rev. E* 104(1), 015206. DOI 10.1103/PhysRevE.104.015206 [V-API]
- Scheinker A. (2026). Round-trip consistency: Bidirectional diffusion models can predict their own rollout errors. Preprint arXiv:2608.00675 [V-API]
- Nauman F., Nättilä J. (2019). Exploring helical dynamos with machine learning: Regularized linear regression outperforms ensemble methods. *Astron. Astrophys.* 629, A89. DOI 10.1051/0004-6361/201935945 [V-API]
- Illarionov E., Kisielius V., Stepanov R., Kuzanyan K. (2026). Neural differential equations for the solar dynamo. *Phys. Rev. E* 113(5), L053202. DOI 10.1103/dpsp-bwkh; arXiv:2603.10548 [V-API]
- Brunton S. L., Proctor J. L., Kutz J. N. (2016). Discovering governing equations from data by sparse identification of nonlinear dynamical systems. *PNAS* 113(15), 3932-3937. DOI 10.1073/pnas.1517384113 [V-API]
- Loiseau J.-C., Brunton S. L. (2018). Constrained sparse Galerkin regression. *J. Fluid Mech.* 838, 42-67. DOI 10.1017/jfm.2017.823 [V-API]
- Lusch B., Kutz J. N., Brunton S. L. (2018). Deep learning for universal linear embeddings of nonlinear dynamics. *Nat. Commun.* 9, 4950. DOI 10.1038/s41467-018-07210-0 [V-API]
- Champion K., Lusch B., Kutz J. N., Brunton S. L. (2019). Data-driven discovery of coordinates and governing equations. *PNAS* 116(45), 22445-22451. DOI 10.1073/pnas.1906995116 [V-API]
- Yang Y., Schmid P. J. (2025). Complex-network modeling of reversal events in two-dimensional turbulent thermal convection. *J. Fluid Mech.* 1011, A30. DOI 10.1017/jfm.2025.371 [V-API]
- Gwirtz K., Davis T., Morzfeld M., Constable C., Fournier A., Hulot G. (2022). Can machine learning reveal precursors of reversals of the geomagnetic axial dipole field? *Geophys. J. Int.* 231(1), 520-535. DOI 10.1093/gji/ggac195 [V-API]
- Nakano S., Sato S., Toh H. (2024). Short-term prediction of geomagnetic secular variation with an echo state network. *Earth Planets Space* 76, 121. DOI 10.1186/s40623-024-02064-x [V-API]
- Pathak J., Hunt B., Girvan M., Lu Z., Ott E. (2018). Model-free prediction of large spatiotemporally chaotic systems from data: A reservoir computing approach. *Phys. Rev. Lett.* 120(2), 024102. DOI 10.1103/PhysRevLett.120.024102 [V-API]
- Qi D., Majda A. J. (2020). Using machine learning to predict extreme events in complex systems. *PNAS* 117(1), 52-59. DOI 10.1073/pnas.1917285117 [V-API]
- Lucente D., Rolland J., Herbert C., Bouchet F. (2022). Coupling rare event algorithms with data-based learned committor functions using the analogue Markov chain. *J. Stat. Mech.* 2022(8), 083201. DOI 10.1088/1742-5468/ac7aa7 [V-API]
- Jiang R., Lu P. Y., Orlova E., Willett R. (2023). Training neural operators to preserve invariant measures of chaotic attractors. *NeurIPS 2023*. arXiv:2306.01187 [V-API]
- Schiff Y., Wan Z. Y., Parker J. B., Hoyer S., Kuleshov V., Sha F., Zepeda-Núñez L. (2024). DySLIM: Dynamics stable learning by invariant measure for chaotic systems. *ICML 2024*, PMLR 235, 43649-43684 [SITE T:1214; not re-checked today]
- Yang Y., Nurbekyan L., Negrini E., Martin R., Pasha M. (2023). Optimal transport for parameter identification of chaotic dynamics via invariant measures. *SIAM J. Appl. Dyn. Syst.* 22(1), 269-310. DOI 10.1137/21M1421337 [V-API]
- Botvinick-Greenhouse J., Martin R., Yang Y. (2023). Learning dynamics on invariant measures using PDE-constrained optimization. *Chaos* 33(6), 063152. DOI 10.1063/5.0149673 [V-API]
- Chen Y., Das S., Guo W., Zhong X. (2026). Physics-informed machine learning for reconstruction of dynamical systems with invariant measure score matching. *Physica D* 496, 135326. DOI 10.1016/j.physd.2026.135326 [V-API]
- Cheng X., He Y., Yang Y., Xue X., Cheng S., Giles D., Tang X., Hu Y. (2025). Learning chaos in a linear way. *ICLR 2025*. arXiv:2503.14702 [V-API]
- Xue X., ten Eikelder M. F. P., Gao M., Cheng X., Yang Y., He Y., Wang S., Cheng S., Hu Y., Coveney P. V. (2026). Fast-forward prediction of lattice Boltzmann dynamics with physics-informed neural operators. *Nat. Commun.* 17, 9243. DOI 10.1038/s41467-026-75730-1 [V-API]
- Fournier A., Hulot G., Jault D., Kuang W., Tangborn A., Gillet N., Canet E., Aubert J., Lhuillier F. (2010). An introduction to data assimilation and predictability in geomagnetism. *Space Sci. Rev.* 155(1-4), 247-291. DOI 10.1007/s11214-010-9669-4 [V-API]

### Track 2: generative models for physical fields
- Goodfellow I. J., Pouget-Abadie J., Mirza M., Xu B., Warde-Farley D., Ozair S., Courville A., Bengio Y. (2014). Generative adversarial nets. *NIPS 27*. arXiv:1406.2661 [V-API; V-WEB https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html]
- Xie Y., Franz E., Chu M., Thuerey N. (2018). tempoGAN: A temporally coherent, volumetric GAN for super-resolution fluid flow. *ACM Trans. Graph.* 37(4), 95. DOI 10.1145/3197517.3201304 [V-API; Crossref title field reads "tempoGAN" only]
- Fukami K., Fukagata K., Taira K. (2019). Super-resolution reconstruction of turbulent flows with machine learning. *J. Fluid Mech.* 870, 106-120. DOI 10.1017/jfm.2019.238 [V-API]
- Kim H., Kim J., Won S., Lee C. (2021). Unsupervised deep learning for super-resolution reconstruction of turbulence. *J. Fluid Mech.* 910, A29. DOI 10.1017/jfm.2020.1028 [V-API]
- Wu J.-L., Kashinath K., Albert A., Chirila D., Prabhat, Xiao H. (2020). Enforcing statistical constraints in generative adversarial networks for modeling chaotic dynamical systems. *J. Comput. Phys.* 406, 109209. DOI 10.1016/j.jcp.2019.109209 [V-API]
- Ho J., Jain A., Abbeel P. (2020). Denoising diffusion probabilistic models. *NeurIPS 2020*. arXiv:2006.11239 [V-API; venue SITE L:62-67]
- Song Y., Sohl-Dickstein J., Kingma D. P., Kumar A., Ermon S., Poole B. (2021). Score-based generative modeling through stochastic differential equations. *ICLR 2021*. arXiv:2011.13456 [V-API]
- Karras T., Aittala M., Aila T., Laine S. (2022). Elucidating the design space of diffusion-based generative models. *NeurIPS 2022*. arXiv:2206.00364 [V-API]
- Ho J., Salimans T. (2022). Classifier-free diffusion guidance. arXiv:2207.12598 (short version: NeurIPS 2021 Workshop) [V-API]
- Lipman Y., Chen R. T. Q., Ben-Hamu H., Nickel M., Le M. (2023). Flow matching for generative modeling. *ICLR 2023*. arXiv:2210.02747 [V-API; venue SITE L:107-111]
- Liu X., Gong C., Liu Q. (2023). Flow straight and fast: Learning to generate and transfer data with rectified flow. *ICLR 2023*. arXiv:2209.03003 [V-API; venue SITE L:112-117]
- Albergo M. S., Vanden-Eijnden E. (2023). Building normalizing flows with stochastic interpolants. *ICLR 2023*. arXiv:2209.15571 [V-API]
- Albergo M. S., Boffi N. M., Vanden-Eijnden E. (2025). Stochastic interpolants: A unifying framework for flows and diffusions. *J. Mach. Learn. Res.* 26(209), 1-80. arXiv:2303.08797 [V-API; volume SITE L:24]
- Tong A., Fatras K., Malkin N., Huguet G., Zhang Y., Rector-Brooks J., Wolf G., Bengio Y. (2024). Improving and generalizing flow-based generative models with minibatch optimal transport. *TMLR*. arXiv:2302.00482 [V-API]
- Kerrigan G., Migliorini G., Smyth P. (2024). Functional flow matching. *AISTATS 2024*, PMLR 238, 3934-3942. arXiv:2305.17209 [V-API; venue SITE L:127-131]
- Lim J. H., Kovachki N. B., Baptista R., et al. (13 authors) (2025). Score-based diffusion models in function space. *J. Mach. Learn. Res.* 26(158), 1-62. arXiv:2302.07400 [V-API; venue SITE L:132-135]
- Shu D., Li Z., Barati Farimani A. (2023). A physics-informed diffusion model for high-fidelity flow field reconstruction. *J. Comput. Phys.* 478, 111972. DOI 10.1016/j.jcp.2023.111972 [V-API]
- Lienen M., Lüdke D., Hansen-Palmus J., Günnemann S. (2024). From zero to turbulence: Generative modeling for 3D flow simulation. *ICLR 2024*. arXiv:2306.01776 [V-API]
- Kohl G., Chen L.-W., Thuerey N. (2026). Benchmarking autoregressive conditional diffusion models for turbulent flow simulation. *Neural Networks* 199, 108641. DOI 10.1016/j.neunet.2026.108641 [V-API]
- Gao H., Han X., Fan X., Sun L., Liu L.-P., Duan L., Wang J.-X. (2024). Bayesian conditional diffusion models for versatile spatiotemporal turbulence generation. *Comput. Methods Appl. Mech. Eng.* 427, 117023. DOI 10.1016/j.cma.2024.117023 [V-API]
- Du P., Parikh M. H., Fan X., Liu X.-Y., Wang J.-X. (2024). Conditional neural field latent diffusion model for generating spatiotemporal turbulence. *Nat. Commun.* 15, 10416. DOI 10.1038/s41467-024-54712-1 [V-API]
- Li T., Biferale L., Bonaccorso F., Scarpolini M. A., Buzzicotti M. (2024). Synthetic Lagrangian turbulence by generative diffusion models. *Nat. Mach. Intell.* 6(4), 393-403. DOI 10.1038/s42256-024-00810-0 [V-API]
- Raonić B., Molinaro R., Lanthaler S., Rohner T., Armegioiu V., Simonis S., et al. (12 authors) (2026). Generative AI for efficient statistical computation of fluids. *Nat. Commun.* 17, 9846. DOI 10.1038/s41467-026-76390-x (preprint: Molinaro et al., arXiv:2409.18359) [V-API]
- Galletti G., Gutenbrunner G., Hornsby W., Zanisi L., Carey N., Pamela S., Brandstetter J., Paischer F. (2026). A shortcut to statistically steady-state turbulence with flow matching. Preprint arXiv:2607.13022 [V-API]
- Wang S., Dou Z., Shan S., Liu T.-R., Lu L. (2026). FunDiff: diffusion models over function spaces for physics-informed generative modeling. *Nat. Commun.* 17, 5749. DOI 10.1038/s41467-026-72292-0 [V-API]
- Finzi M., Boral A., Wilson A. G., Sha F., Zepeda-Núñez L. (2023). User-defined event sampling and uncertainty quantification in diffusion models for physical dynamical systems. *ICML 2023*. arXiv:2306.07526 [V-API, venue from arXiv comment]
- Li L., Carver R., Lopez-Gomez I., Sha F., Anderson J. (2024). Generative emulation of weather forecast ensembles with diffusion models. *Sci. Adv.* 10(13), eadk4489. DOI 10.1126/sciadv.adk4489 [V-API]
- Price I., Sanchez-Gonzalez A., Alet F., Andersson T. R., El-Kadi A., Masters D., et al. (12 authors) (2025). Probabilistic weather forecasting with machine learning. *Nature* 637(8044), 84-90. DOI 10.1038/s41586-024-08252-9 [V-API]
- Mardani M., Brenowitz N., Cohen Y., Pathak J., Chen C.-Y., Liu C.-C., et al. (13 authors) (2025). Residual corrective diffusion modeling for km-scale atmospheric downscaling. *Commun. Earth Environ.* 6, 124. DOI 10.1038/s43247-025-02042-5 [V-API]
- da Silva D. E., Kirk M., Mathews N., Muñoz-Jaramillo A. (2025). Diffusion modeling of the three-dimensional magnetic field in the Sun's corona. Preprint arXiv:2510.01441 [V-API]
- Martin J., Lübke J., Li T., Buzzicotti M., Grauer R., Biferale L. (2025). Generation of cosmic ray trajectories by a diffusion model trained on test particles in 3D magnetohydrodynamic turbulence. *Astrophys. J. Suppl. Ser.* 277(2), 48. DOI 10.3847/1538-4365/adb432; arXiv:2412.12923 [V-API for arXiv; journal SITE L:302]
- Biferale L., Buzzicotti M. (2026). Generative AI in turbulence: Foundations, applications, validations and benchmarks. Preprint arXiv:2610.35123 [V-API]
- Cheng S., Guo Y., Arcucci R. (2023). A generative model for surrogates of spatial-temporal wildfire nowcasting. *IEEE Trans. Emerg. Top. Comput. Intell.* 7(5), 1420-1430. DOI 10.1109/TETCI.2023.3298535 [V-API]
- Zhuang Y., Cheng S., Duraisamy K. (2025). Spatially-aware diffusion models with cross-attention for global field reconstruction with sparse observations. *Comput. Methods Appl. Mech. Eng.* 435, 117623. DOI 10.1016/j.cma.2024.117623 [V-API]
- Yu W., Ghosh A., Finn T. S., Arcucci R., Bocquet M., Cheng S. (2026). A probabilistic approach to wildfire spread prediction using a denoising diffusion surrogate model. *Geosci. Model Dev.* 19(2), 1027-1054. DOI 10.5194/gmd-19-1027-2026 [V-API]

### Track 3: physics constraints in generative models
- Richter-Powell J., Lipman Y., Chen R. T. Q. (2022). Neural conservation laws: A divergence-free perspective. *NeurIPS 35*, 38075-38088. DOI 10.52202/068431-2759 [V-API]
- Christopher J. K., Baek S., Fioretto F. (2024). Constrained synthesis with projected diffusion models. *NeurIPS 37*, 89307-89333. DOI 10.52202/079017-2834 [V-API]
- Liu G.-H., Chen T., Theodorou E., Tao M. (2023). Mirror diffusion models for constrained and watermarked generation. *NeurIPS 36*, 42898-42917. DOI 10.52202/075280-1858 [V-API]
- Fishman N., Klarner L., De Bortoli V., Mathieu E., Hutchinson M. (2023). Diffusion models for constrained domains. *TMLR*. arXiv:2304.05364 [V-API]
- Ben-Hamu H., Puny O., Gat I., Karrer B., Singer U., Lipman Y. (2024). D-Flow: Differentiating through flows for controlled generation. *ICML 2024*, PMLR 235, 3462-3483. arXiv:2402.14017 [V-API; pages SITE L:258]
- Cheng C., Han B., Maddix D. C., Ansari A. F., Stuart A., Mahoney M. W., Wang Y. (2025). Gradient-free generation for hard-constrained systems. *ICLR 2025*. arXiv:2412.01786 [V-API]
- Utkarsh U., Cai P., Edelman A., Gomez-Bombarelli R., Rackauckas C. V. (2025). Physics-constrained flow matching: Sampling generative models with hard constraints. *NeurIPS 38*, 177845-177880. DOI 10.52202/085713-5354 [V-API]
- Genuist W., Savin É., Gatti F., Clouteau D. (2026). Divergence-free diffusion models for incompressible fluid flows. Preprint arXiv:2601.19368 [V-API]
- Genuist W., Savin É., Gatti F., Clouteau D. (2025). Autoregressive regularized score-based diffusion models for multi-scenarios fluid flow prediction. Preprint arXiv:2505.24145 [V-API]
- Li T., Buzzicotti M., Bonaccorso F., Biferale L. (2026). Physics-constrained diffusion model for synthesis of 3D turbulent data. Preprint arXiv:2603.12834 [V-API]
- Li X., Zhang H., Jiang R., Chen D., Lin C., Han L., Qi Y., Guo X., Cheng Y. (2026). Project and generate: Divergence-free neural operators for incompressible flows. Preprint arXiv:2603.24500 [V-API]
- Négiar G., Mahoney M. W., Krishnapriyan A. S. (2023). Learning differentiable solvers for systems with hard constraints. *ICLR 2023*. arXiv:2207.08675 [V-API]
- Hansen D., Maddix D. C., Alizadeh S., Gupta G., Mahoney M. W. (2024). Learning physical models that can respect conservation laws. *Physica D* 457, 133952 (ICML 2023). DOI 10.1016/j.physd.2023.133952; arXiv:2302.11002 [V-API]
- Bastek J.-H., Sun W., Kochmann D. M. (2025). Physics-informed diffusion models. *ICLR 2025*. arXiv:2403.14404 [V-API]
- Huang J., Yang G., Wang Z., Park J. J. (2024). DiffusionPDE: Generative PDE-solving under partial observation. *NeurIPS 37*, 130291-130323. DOI 10.52202/079017-4140 [V-API]
- Jacobsen C., Zhuang Y., Duraisamy K. (2025). CoCoGen: Physically consistent and conditioned score-based generative models for forward and inverse problems. *SIAM J. Sci. Comput.* 47(2), C399-C425. DOI 10.1137/24M1636071 [V-API]
- Chung H., Kim J., McCann M. T., Klasky M. L., Ye J. C. (2023). Diffusion posterior sampling for general noisy inverse problems. *ICLR 2023*. arXiv:2209.14687 [V-API]
- Bansal A., Chu H.-M., Schwarzschild A., Sengupta S., Goldblum M., Geiping J., Goldstein T. (2024). Universal guidance for diffusion models. *ICLR 2024*. arXiv:2302.07121 [V-API; venue SITE L:93-105]
- Gallon D., von Wurstemberger P., Cheridito P., Jentzen A. (2026). Physics-informed diffusion models in spectral space. Preprint arXiv:2602.09708 [V-API]
- Baldan G., Liu Q., Guardone A., Thuerey N. (2026). Physics vs distributions: Pareto optimal flow matching with physics constraints. *ICLR 2026*. arXiv:2506.08604 [V-API; V-WEB https://mlanthology.org/iclr/2026/baldan2026iclr-physics/]
- Khalifa M., Elsahar H., Dymetman M. (2021). A distributional approach to controlled text generation. *ICLR 2021*. arXiv:2012.11635 [V-API]
- Khalafi S., Ding D., Ribeiro A. (2024). Constrained diffusion models via dual training. *NeurIPS 37*, 26543-26576. DOI 10.52202/079017-0836 [V-API]
- Mun J. (2026). Multifidelity computer model emulation via diffusion model steering and targeted maximum likelihood. Preprint arXiv:2608.30096 [V-API]
- Tauberschmidt J., Fellenz S., Vollmer S. J., Duncan A. B. (2026). Physics-constrained fine-tuning of flow-matching models for generation and inverse problems. *ICLR 2026*. arXiv:2508.09156 [V-API; venue SITE M:17]
- Cai Z., Cao Y., Huang Y., Zhou X. (2026). Weak generative sampler to efficiently sample invariant distribution of stochastic differential equation. *SIAM J. Sci. Comput.* 48(4), C708-C735. DOI 10.1137/24M1665271 [V-API]
- Zang Y., Bao G., Ye X., Zhou H. (2020). Weak adversarial networks for high-dimensional partial differential equations. *J. Comput. Phys.* 411, 109409. DOI 10.1016/j.jcp.2020.109409 [V-API]
- Köhler J., Klein L., Noé F. (2020). Equivariant flows: Exact likelihood generative learning for symmetric densities. *ICML 2020*, PMLR 119, 5361-5370. arXiv:2006.02425 [V-API; V-WEB https://proceedings.mlr.press/v119/kohler20a.html]
- Klein L., Krämer A., Noé F. (2023). Equivariant flow matching. *NeurIPS 36*, 59886-59910. DOI 10.52202/075280-2617 [V-API]
- Hoogeboom E., Garcia Satorras V., Vignac C., Welling M. (2022). Equivariant diffusion for molecule generation in 3D. *ICML 2022*. arXiv:2203.17003 [V-API, venue from arXiv comment]
- Wang R., Walters R., Yu R. (2021). Incorporating symmetry into deep dynamics models for improved generalization. *ICLR 2021*. arXiv:2002.03061 [V-API; V-WEB https://iclr.cc/virtual/2021/poster/2785]
- Bousquet R., Nore C., Lucor D. (2025). AutoEncoders latent space interpretability in the light of proper orthogonal decomposition: Machine learning of periodically forced fluid flows. *Comput. Phys. Commun.* 315, 109728. DOI 10.1016/j.cpc.2025.109728 [V-API]
- Classical anchors (not re-checked today; checked by the site): Csiszár 1975; Jaynes 1957; Pitera and Chodera 2012; Echeverría 1982; Ethier and Kurtz 1986; Rice 1944, 1945; Azaïs and Wschebor 2009 [SITE T:1128-1238]

### Track 4: generative priors in data assimilation
- Amendola M., Arcucci R., Mottet L., Quilodrán Casas C., Fan S., Pain C., Linden P., Guo Y.-K. (2021). Data assimilation in the latent space of a convolutional autoencoder. *ICCS 2021, Lecture Notes in Computer Science*, 373-386. DOI 10.1007/978-3-030-77977-1_30 [V-API]
- Peyron M., Fillion A., Gürol S., Marchais V., Gratton S., Boudier P., Goret G. (2021). Latent space data assimilation by using deep learning. *Q. J. R. Meteorol. Soc.* 147, 3759-3777. DOI 10.1002/qj.4153 [V-API]
- Cheng S., Chen J., Anastasiou C., Angeli P., Matar O. K., Guo Y.-K., Pain C. C., Arcucci R. (2023, online 2022). Generalised latent assimilation in heterogeneous reduced spaces with machine learning surrogate models. *J. Sci. Comput.* 94(1), 11. DOI 10.1007/s10915-022-02059-4 [V-API]
- Cheng S., Prentice I. C., Huang Y., Jin Y., Guo Y.-K., Arcucci R. (2022). Data-driven surrogate model with latent data assimilation: Application to wildfire forecasting. *J. Comput. Phys.* 464, 111302. DOI 10.1016/j.jcp.2022.111302 [V-API]
- Cheng S., Liu C., Guo Y., Arcucci R. (2024). Efficient deep data assimilation with sparse observations and time-varying sensors. *J. Comput. Phys.* 496, 112581. DOI 10.1016/j.jcp.2023.112581 [V-API]
- Cheng S., Zhuang Y., Kahouadji L., Liu C., Chen J., Matar O. K., Arcucci R. (2024). Multi-domain encoder-decoder neural networks for latent data assimilation in dynamical systems. *Comput. Methods Appl. Mech. Eng.* 430, 117201. DOI 10.1016/j.cma.2024.117201 [V-API]
- Cheng S., Min J., Liu C., Arcucci R. (2025). TorchDA: A Python package for performing data assimilation with deep learning forward and transformation functions. *Comput. Phys. Commun.* 306, 109359. DOI 10.1016/j.cpc.2024.109359 [V-API]
- Cheng S., Quilodrán-Casas C., Ouala S., Farchi A., Liu C., Tandeo P., et al. (17 authors, including Lucor D.) (2023). Machine learning with data assimilation and uncertainty quantification for dynamical systems: A review. *IEEE/CAA J. Autom. Sinica* 10(6), 1361-1387. DOI 10.1109/JAS.2023.123537 [V-API]
- Cheng S., Bocquet M., Ding W., Finn T. S., et al. (23 authors) (2025). Machine learning for modelling unstructured grid data in computational physics: A review. *Inf. Fusion* 123, 103255. DOI 10.1016/j.inffus.2025.103255 [V-API]
- Zhou H., Cheng S., Arcucci R. (2024). Multi-fidelity physics constrained neural networks for dynamical systems. *Comput. Methods Appl. Mech. Eng.* 420, 116758. DOI 10.1016/j.cma.2024.116758 [V-API]
- Rozet F., Louppe G. (2023). Score-based data assimilation. *NeurIPS 36*, 40521-40541. DOI 10.52202/075280-1763 [V-API]
- Rozet F., Andry G., Lanusse F., Louppe G. (2024). Learning diffusion priors from observations by expectation maximization. *NeurIPS 37*, 87647-87682. DOI 10.52202/079017-2783 [V-API]
- Huang L., Gianinazzi L., Yu Y., Dueben P. D., Hoefler T. (2024). DiffDA: a diffusion model for weather-scale data assimilation. *ICML 2024*, PMLR 235, 19798-19815. arXiv:2401.05932 [V-API; pages SITE L:221]
- Bao F., Zhang Z., Zhang G. (2024). An ensemble score filter for tracking high-dimensional nonlinear dynamical systems. *Comput. Methods Appl. Mech. Eng.* 432, 117447. DOI 10.1016/j.cma.2024.117447; arXiv:2309.00983 [V-API]
- Si P., Chen P. (2024). Latent-EnSF: A latent ensemble score filter for high-dimensional data assimilation with sparse observation data. Preprint arXiv:2409.00127 [V-API]
- Manshausen P., Cohen Y., Harrington P., Pathak J., Pritchard M., Garg P., et al. (10 authors) (2024). Generative data assimilation of sparse weather station observations at kilometer scales. Preprint arXiv:2406.16947 [V-API]
- Bocquet M., Finn T. S., Cheng S. (2026). Accounting for model error in ensemble variational data assimilation through learned generative dynamics. Preprint arXiv:2610.17333 [V-API]
- Zhang Z., Yuan W., Cheng X., Behnoudfar P., Chen C., Moser C., et al. (13 authors, including Cheng S.) (2026). When latent dynamics meet data assimilation: A benchmark of Koopman-type representations. Preprint arXiv:2611.03916 [V-API]
- Yang Y., Cheng X., Giles D., Cheng S., He Y., Xue X., Chen B., Hu Y. (2025). Tensor-Var: Efficient four-dimensional variational data assimilation. *ICML 2025*, PMLR 267, 70649-70679 [SITE S:14, S:154; not re-checked today]

### Supervisors' other works cited in section 7
- Lucor D., Agrawal A., Sergent A. (2022). Simple computational strategies for more effective physics-informed neural networks modeling of turbulent natural convection. *J. Comput. Phys.* 456, 111022. DOI 10.1016/j.jcp.2022.111022 [V-API]
- Cai J., Angeli P.-E., Martinez J.-M., Damblin G., Lucor D. (2024). Revisiting tensor basis neural network for Reynolds stress modeling: Application to plane channel and square duct flows. *Comput. Fluids* 275, 106246. DOI 10.1016/j.compfluid.2024.106246 [V-API]
- Bousquet R., Chaffard O., Creff M., Lucor D., Nore C. (2024). Large scale analysis of three-dimensional turbulent von Kármán swirling flows. *Phys. Fluids* 36(10), 105133. DOI 10.1063/5.0227495 [V-API]
- Bousquet R., Faucheu A., Dumas L., Nore C., Lucor D. (2026). Polynomial autoencoders with quantifiable errors for nonlinear fluid flow reconstruction. Research Square preprint. DOI 10.21203/rs.3.rs-10008570/v1 [V-API]
- Zhou Y., Lin C., Kikumoto H., Ooka R., Cheng S. (2026). Rooftop wind field reconstruction using sparse sensors: From deterministic to generative learning methods. *Build. Environ.* 296, 114480. DOI 10.1016/j.buildenv.2026.114480 [V-API]
- Botez V., Bousquet R., Nore C. (2025); Volk et al. (2025); Nony et al. (2023); Wang, Zhou, Cheng (2024); Cheng, Lucor, Argaud (2021); Quattromini (2024, thesis): metadata as in S (lines given in section 7), not re-checked today [SITE].
