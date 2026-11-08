# The supervisors' and the MilaDy consortium's contributions (verified 2026-11-08)

Working note for the film units `chSOA1`/`chSOA2` and for `video/ETAT-DE-L-ART.md` (BRIEF §10,
`video/BRIEF.md:194-205`). It covers S. Cheng (CEREA, ENPC), D. Lucor (LISN, CNRS), C. Nore (LISN, Université
Paris-Saclay), Y. Ponty (Lagrange, Observatoire de la Côte d'Azur) and the ANR MilaDy project. It starts from
`en/encadrants/index.qmd` and `specs/sources/encadrants.md` (checked 2026-11-06), re-checks every item on
2026-11-08, and adds the landmark papers that were missing.

## 0. Rules, method and legend

- **Contribution** = one factual sentence taken from the paper's abstract or full text (source given by
  the check codes). No opinions or intentions are attributed to anyone. Self-descriptions are quoted only
  when they come from the person's own public page, and they are marked as such.
- **Thesis builds on it** = how the PhD proposal on the site (`en/these/index.qmd`, cited as `these:LINE`) or
  the candidate directions (`en/encadrants/index.qmd`, cited as `enc:LINE`) use the paper. When neither does,
  the use is labelled **"proposal of this note"**: a suggestion, not a position of the site or the supervisors.
- **Check codes** (all on 2026-11-08 unless marked PREV):
  - `[CR]` DOI resolved in the Crossref API; authors, title, venue, volume and pages match.
  - `[CRs]` found by a Crossref bibliographic search (DOI and metadata read from the search result).
  - `[AX]` arXiv API record read (id, authors, title; journal-ref/DOI when given).
  - `[HAL]` HAL API record read.
  - `[ABS-OA]`, `[ABS-AX]`, `[ABS-HAL]` abstract read today, from OpenAlex, arXiv or HAL respectively.
  - `[PDF]` full text or offer PDF opened today. `[WEB]` web page opened today.
  - `[PREV]` checked on 2026-11-06 per `specs/sources/encadrants.md` (line given), not re-read today.
  - `[UNVERIFIED]` could not be checked; do not use on screen without a check.
- Raw verification outputs: `video/plan/soa/ (copies de travail non versionnées pour dl/ et work/) sup/out/`
  (`crossref.tsv`, `arxiv.tsv`, `abstracts.txt`, `arxiv_abs.txt`) and downloaded pages in
  `video/plan/soa/ (copies de travail non versionnées pour dl/ et work/) sup/web/` and `.../sup/dl/`.

**Tally.**
- About 100 DOIs resolved in Crossref (90 by DOI, 10 by bibliographic search). No metadata (authors,
  venue, volume, pages) contradicts the site.
- 31 arXiv records resolved, all matching.
- HAL queries: the ANR reference, three theses and one HDR, the 2025–2026 records of all four people, and
  the full lists of Ponty (30 records) and Nore (journal articles).
- 12 web pages and 8 PDFs opened.
- **New items** relative to the site: 31 (marked **NEW**). **Flags**: 21 (section 7).

---

## 1. The ANR MilaDy project and its own outputs

### 1.1 Fact sheet (ANR page, opened today) `[WEB]` https://anr.fr/Projet-ANR-25-CE51-0077

- *Modélisation par apprentissage automatique des dynamos turbulentes – MilaDy*, ANR-25-CE51-0077,
  committee CE51 "Sciences de l'ingénierie et des procédés", 2025 call.
- Coordination: Caroline Nore (LISN). Partners: LISN; LAGRANGE, Observatoire de la Côte d'Azur, Nice;
  CEREA, École nationale des ponts et chaussées.
- ANR funding €560,612. Start January 2026, 48 months.
- The abstract has two objectives: (i) magnetic field reversals and "explosive" dynamos, with reduced
  models that identify the precursor, reversal and recovery phases; (ii) optimising DRESDYN with
  parametric reduced models, for example precession/rotation frequency ratios. It names the **TorchDA**
  platform. Same text as at `specs/sources/encadrants.md:55-58`.
- Other public sources give different figures `[WEB]`/`[PDF]`:
  - S. Cheng's home page: "MILADY — ANR PRC (2025–2029): machine learning for computational fluid dynamics".
  - His research page: "Role: Co-Investigator … Start: 2026".
  - Y. Ponty's 2026 CV: "2026 (février) – 2030 … Duration: 48 months (550k€)".
  - Use the ANR values.

### 1.2 Offers (all three PDFs opened today) `[PDF]`

| Offer | Verified content |
|---|---|
| M2 internship 2027, "Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems (with potential PhD position)", https://scheng2024.github.io/stage_milady_2027.pdf | Supervision S. Cheng (ENPC) and D. Lucor (LISN), "in collaboration with Pr. Caroline Nore (LISN) and Dr. Yannick Ponty (Observatoire de la Côte d'Azur, CNRS)". Conditional generation by "diffusion or flow matching". Constraints: "energy balance and divergence-free conditions". Metrics: "energy spectra, helicity, divergence control, and topology preservation". Recommended reading: FunDiff (Wang et al. 2026) and Fukami & Taira 2023. A funded PhD "may be offered". S. Cheng's Opportunities page `[WEB]`: "The PhD student will be co-supervised by Sibo Cheng and Didier Lucor". D. Lucor's Opportunities page `[WEB]` lists the same internship. |
| M2 internship 2026, "Physics-aware Representation Learning for Turbulent Dynamo Data", https://stages.phys.ens.psl.eu/OffresPDF/Offre-30818.pdf | 3D outputs of the "Cadarache (France) and … Dresden (Germany)" configurations; latent-space regression; contrastive learning. Contacts: the four supervisors. Cites Bousquet, Nore, Lucor 2025. |
| 24-month LISN postdoc, "Turbulent Dynamos Reduced-Order Modeling via Machine learning", https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf | Contacts "Pr. UPS C. Nore" and "DR CNRS D. Lucor". DNS "typically restricted to Pm~1 regimes". The DRESDYN dynamo's "success remains uncertain". Cites Bousquet et al. 2024, Bousquet, Nore, Lucor 2025, and Yang & Schmid 2025. |

### 1.3 The project's own papers

**(a) Papers that acknowledge MilaDy funding.** HAL field `anrProjectReference_s:"ANR-25-CE51-0077"` returns 3
records today `[HAL]`. Crossref funder metadata gives "ANR-25-CE51-0077-02" for the first two `[CR]`.

| # | Reference | Check | Contribution (factual) | Thesis builds on it |
|---|---|---|---|---|
| M1 | Bousquet R., Ponty Y., Botez V., Plihon N., Nore C. (2026). *Magnetic field reversals in numerical simulations of the von Kármán sodium experiment.* Physical Review Fluids 11(6), 063703. doi:10.1103/9tx2-1m13; hal-05668081. Full text: https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf | `[CR][HAL][ABS-OA][PDF]` | Two solvers (LATU and SFEMaNS) agree on the reversal mechanism of VKS with ferromagnetic impellers. A POD on 2000 snapshots gives four dominant axisymmetric modes (D, Q, V, U). The DQVU Galerkin model is derived from the MHD equations and identified by constrained regression (PySINDy). Reference run: Re = 1594, Rm = 531, asymmetry 0.058, μr = 16 in the impellers. A conducting surrounding medium was "necessary for these inversions to occur" in the explored range. Data "available … upon reasonable request". All re-read today in the PDF (lines 75, 121-127, 149, 348, 364, 425-426, 481 of the extracted text). | Reference data and reduced model of tier 3 (these:929-937). DQVU identification question (these:135, these:828). Dipole read-out through POD mode ψ_D (these:645). μr = 16 interface constraint (these:269). Directions A and B (enc:249, enc:261). |
| M2 | Botez V., Giesecke A., Nore C., Cappanera L., Stefani F. (2026). *Impact of boundary conditions on onset and symmetry of precession-driven dynamos.* Physical Review Fluids 11(8), 083701 (published online 2026-08-14). doi:10.1103/rx1h-5zxp; hal-05782992 | `[CR][HAL][ABS-OA]`; funders ANR-25-CE51-0077-02 and DFG 532905681 `[CR]` | Kinematic precession dynamo in a cylinder, computed from time-averaged velocity fields in the narrow Poincaré-number range where dynamo action is most likely. Two competing families: a centro-symmetric, higher-frequency quadrupolar mode and a centro-antisymmetric, lower-frequency dipolar mode. Vanishing-tangential-field boundary conditions systematically underestimate Rm_c; conducting or permeable walls can promote or suppress the dynamo. | Tier 4, DRESDYN (these:943-947). Direction D (enc:285). |
| M3 | Barré J., Horii H. (2026). *Large deviations, gradient flows and fluctuating hydrodynamics for fractional diffusion.* HAL preprint hal-05796131 | `[HAL]` (title, authors, ANR field) | Mathematical work on large deviations that also acknowledges MilaDy. Its thematic link to dynamos is weak. | None. |

**(b) Consortium papers written before the grant and cited by the project's offers as its starting point.**
None of them carries MilaDy funding.

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| M4 | Bousquet R., Nore C., Lucor D. (2025). *AutoEncoders latent space interpretability in the light of proper orthogonal decomposition: Machine learning of periodically forced fluid flows.* Computer Physics Communications 315, 109728. doi:10.1016/j.cpc.2025.109728; hal-05407939 | `[CR][HAL][ABS-OA]`. Funder metadata: GENCI only, **no ANR MilaDy** `[CR]` | AEs and VAEs reconstruct Navier–Stokes velocity fields (oscillating cylinder, von Kármán swirling flow). Raising VAE regularisation degrades reconstruction, "a significant limitation of the Gaussian prior". Latent organisation is linked to POD modes, and equivariance relations are stated between latent and physical variables; VAEs preserve them better. | AE/VAE baselines of tier 3 (these:935). Direction A (enc:249). Cited in the 2026 internship and postdoc offers `[PDF]`. |
| M5 | Bousquet R., Chaffard O., Creff M., Lucor D., Nore C. (2024). *Large scale analysis of three-dimensional turbulent von Kármán swirling flows.* Physics of Fluids 36(10), 105133. doi:10.1063/5.0227495; hal-04723526 | `[CR][HAL][ABS-OA]` | LES and POD of 3D-3C von Kármán flows "corroborate for the first time" numerically a metastable state at Re > 10⁴ (exponent lost in the metadata, see flag F12). This axisymmetric one-cell state breaks the Rπ symmetry and causes long-term intermittent fluctuations of the angular momentum. A POD per azimuthal Fourier mode follows. | Symmetry facts behind the Rπ-equivariance discussion. Data source for direction A (enc:249). |
| M6 | Botez V., Bousquet R., Nore C. (2025). *Large scale analysis of the von Kármán sodium experiment using proper orthogonal decomposition.* Magnetohydrodynamics 61(1/2), 13–24. doi:10.22364/mhd.61.1-2.2 | `[CR][ABS-OA]` | POD of VKS simulations. Growth phase: essentially an axial dipole with secondary structures from the α-effect. Saturated phase: the magnetic feedback breaks the symmetry of the velocity field even in exact counter-rotation. | Symmetry test for generated saturated fields (proposal of this note; also enc:180-189). |

**(c) Consortium outputs of 2026 without stated MilaDy funding (NEW in part).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| M7 | Bousquet R., Faucheu A., Dumas L., Nore C., Lucor D. (2026). *Polynomial autoencoders with quantifiable errors for nonlinear fluid flow reconstruction.* Research Square preprint (posted 2026-06-19), doi:10.21203/rs.3.rs-10008570/v1 | `[CR][ABS-OA]`. Not peer-reviewed; no funder metadata | Two-layer AEs with learnable polynomial activations, initialised to be exactly equivalent to POD before improving on it. POD initialisation speeds up training "by an order of magnitude in the number of epochs" (oscillating cylinder). | Latent-space option (enc:164). |
| M8 **NEW** | Bousquet R., Nore C. (2026). *Simulation and modeling of the von Kármán sodium experiment.* Poster abstract, Rencontres du Non-Linéaire, 24–26 March 2026, Paris. https://rnl2026.sciencesconf.org/712616 | `[WEB][PDF]` (abstract only; not peer-reviewed) | SFEMaNS simulations of VKS reproduce stable global dipoles, hemispherical dipoles and reversing solutions as the forcing asymmetry varies. Reversals form a "five-stage sequence" through a transient quadrupolar state. The abstract states that accounting for the impellers' high permeability "introduces new first-order couplings" in the DQVU model affecting the threshold ("inversely proportional to mu") and saturation. | Same use as M1; the μ-dependent couplings are the parametric dependence a conditional generator must learn (proposal of this note). |

**Not confirmed (unchanged since 2026-11-06).** An article by Botez, Bousquet and Nore in *Journal of
Computational Physics* ("In press, 559"). Searched again today in Crossref (authors Botez, Bousquet, Nore since
2025-06): **not found** `[UNVERIFIED]`. No new MilaDy preprint was found on arXiv `[AX]`, although arXiv
author search is incomplete. One 2025 item was found: a recorded seminar of the CPC 2025 paper (Cassyni,
doi:10.52843/cassyni.n6t69b, 2025-11-17) `[CRs]`.

---

## 2. Sibo Cheng (CEREA, École nationale des ponts et chaussées)

### 2.1 Profile (verified)

- **Position.** "Tenure-Track Junior Professor (Chaire de Professeur Junior) at ENPC, Institut Polytechnique de
  Paris" and "Honorary Research Fellow at Imperial College London". Research Associate at the Data Science
  Institute, Imperial College, with R. Arcucci, 2020–2024 `[WEB https://scheng2024.github.io/]`.
- **PhD.** *Error covariance specification and localization in data assimilation with industrial application*,
  Université Paris-Saclay, defended 2020-11-18, director **Didier Lucor**, with EDF R&D, tel-03117151 `[HAL][WEB]`.
- **Projects** `[WEB research page]`:
  - MilaDy: Co-Investigator.
  - OFML, ANR-25-CE56-0198, 2025–2029: PI.
  - Hi! PARIS fellowship, differentiable digital twin for wildfire: PI.
  - QWERTY, PEPR FORESTT, ANR-25-PEFO-0008: Co-I.
- **His page describes the CEREA role in MilaDy as** "physics-aware representation learning and reduced-order
  modelling of three-dimensional velocity and magnetic fields, connecting learned representations to data
  assimilation" `[WEB https://scheng2024.github.io/research/]`.
- **Software.** TorchDA (CPC 2025) and PyTorchFire (EMS 2025) `[CR]`.
- **No dynamo or MHD publication** was found: HAL 2025–2026 records, the publications page (updated
  2026-10-20) and arXiv `[HAL][WEB]`.

### 2.2 Research lines and publications

**Line 1: error-covariance specification in data assimilation (PhD with D. Lucor and EDF R&D).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C1 **NEW** | Cheng S., Argaud J.-P., Iooss B., Lucor D., Ponçot A. (2019). *Background error covariance iterative updating with invariant observation measures for data assimilation.* Stochastic Environmental Research and Risk Assessment 33(11–12), 2033–2051. doi:10.1007/s00477-019-01743-6 | `[CR][ABS-HAL hal-02307657]` | Introduces two non-parametric adaptive methods, CUTE and PUB, that iteratively update the background error covariance; tested in shallow-water twin experiments. | Background (Cheng–Lucor lineage); not used directly. |
| C2 **NEW** | Cheng S., Argaud J.-P., Iooss B., Lucor D., Ponçot A. (2021; online 2020-11-21). *Error covariance tuning in variational data assimilation: application to an operating hydrological model.* SERRA 35(5), 1019–1038. doi:10.1007/s00477-020-01933-7 | `[CR][ABS-HAL hal-02992507]` | Chains existing online and offline covariance-tuning algorithms in an order that satisfies their assumptions, and applies them to an industrial precipitation–flow model with real data. | Background. |
| C3 **NEW** | Cheng S., Argaud J.-P., Iooss B., Ponçot A., Lucor D. (2021). *A Graph Clustering Approach to Localization for Adaptive Covariance Tuning in Data Assimilation Based on State-Observation Mapping.* Mathematical Geosciences 53(8), 1751–1780. doi:10.1007/s11004-021-09951-z | `[CR][ABS-HAL meteo-02460851]` | Unsupervised graph-clustering localization that splits state and observation variables into clusters from a linearized state–observation measure, with no cut-off radius. | Background. |
| C4 | Cheng S., Lucor D., Argaud J.-P. (2021). *Observation data compression for variational assimilation of dynamical systems.* Journal of Computational Science 53, 101405. doi:10.1016/j.jocs.2021.101405; arXiv:2106.05427 | `[CR][AX][ABS-AX]` | Combines covariance tuning with PCA-type observation compression to reduce the cost of each assimilation step; shallow water, then an industrial hydrological model. | Background (enc:157). |

**Line 2: latent data assimilation and reduced surrogates.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C5 | Cheng S., Prentice I.C., Huang Y., Jin Y., Guo Y.-K., Arcucci R. (2022). *Data-driven surrogate model with latent data assimilation: Application to wildfire forecasting.* Journal of Computational Physics 464, 111302. doi:10.1016/j.jcp.2022.111302 | `[CR][ABS-HAL hal-03709573]` | Combines reduced-order modelling, an LSTM surrogate, data assimilation and error-covariance tuning. The surrogate runs "around 1000 times faster" than the cellular-automaton simulation (three Californian fires, 2017–2020). | Background for latent assimilation. |
| C6 | Cheng S., Chen J., Anastasiou C., Angeli P., Matar O.K., Guo Y.-K., Pain C.C., Arcucci R. (2022). *Generalised Latent Assimilation in Heterogeneous Reduced Spaces with Machine Learning Surrogate Models.* Journal of Scientific Computing 94(1), 11. doi:10.1007/s10915-022-02059-4; arXiv:2204.03497 | `[CR][AX][ABS-OA]` | Variational DA in latent space, using local smooth surrogate functions between the encoded space and the observation space. Handles nonlinear observation operators that earlier latent assimilation could not, with an upper bound on the cost-function error. | Latent variational assimilation from z and its symmetric Sz "extends the generalized latent assimilation of Cheng et al. (2022)" (these:843). Direction C (enc:273). |
| C7 **NEW** | Cheng S., Jin Y., Harrison S.P., Quilodrán-Casas C., Prentice I.C., Guo Y.-K., Arcucci R. (2022). *Parameter Flexible Wildfire Prediction Using Machine Learning Techniques: Forward and Inverse Modelling.* Remote Sensing 14(13), 3228. doi:10.3390/rs14133228 | `[CR][ABS-OA]` | A parameter-flexible ROM-plus-ML forward model, with inverse parameter estimation by latent assimilation in the reduced space; validated with satellite observations of two Californian fires. | Precedent for a parameter-conditioned surrogate used inversely (proposal of this note: parameter inference from a conditional generator). |
| C8 **NEW** | Gong H., Cheng S., Chen Z., Li Q., Quilodrán-Casas C., Xiao D., Arcucci R. (2022). *An efficient digital twin based on machine learning SVD autoencoder and generalised latent assimilation for nuclear reactor physics.* Annals of Nuclear Energy 179, 109431. doi:10.1016/j.anucene.2022.109431 | `[CRs]`; abstract not read (title only) | Per its title, combines an SVD autoencoder with generalised latent assimilation in a reactor-physics digital twin. | Background. |
| C9 **NEW** | Zhuang Y., Cheng S., Kovalchuk N., Simmons M., Matar O.K., Guo Y.-K., Arcucci R. (2022). *Ensemble latent assimilation with deep learning surrogate model: application to drop interaction in a microfluidics device.* Lab on a Chip 22, 3187–3202. doi:10.1039/D2LC00303A | `[CRs]`; abstract only partly available | Ensemble latent assimilation with a deep-learning surrogate, assimilating observations (recorded videos) that were excluded from training. | Ensemble variant of direction C (proposal of this note). |
| C10 | Cheng S., Zhuang Y., Kahouadji L., Liu C., Chen J., Matar O.K., Arcucci R. (2024). *Multi-domain encoder–decoder neural networks for latent data assimilation in dynamical systems.* CMAME 430, 117201. doi:10.1016/j.cma.2024.117201 | `[CR][ABS-HAL hal-04660347]` | MEDLA: encoders and decoders of several data sources share one latent space, which removes explicit surrogate mapping functions between heterogeneous latent spaces. | Proposal of this note: a shared latent space for u and B, or for probes and fields. |
| C11 **NEW** | Wang K., Cheng S., Piggott M.D., Dance S.L., Wang Y., Arcucci R. (2025). *Latent data assimilation with non-explicit observation operator in hydrology.* QJRMS 151(772), e5009. doi:10.1002/qj.5009 | `[CR][ABS-OA]` | A neural "latent neural mapping" serves as observation operator inside latent 3D-Var when no explicit state-to-observation map exists. | Learned observation operator for magnetic probes (proposal of this note). |
| C12 **NEW** | Lin Z., Zhang S., Liu Z., Jin Y., Wan L., Cheng S., Gao Y., Yu X., Li M. (2026). *Non-Gaussian Assimilation of Atmospheric and Oceanic Data in Latent Space for Paleoclimate Reconstruction.* JAMES 18(7), e2026MS005767. doi:10.1029/2026MS005767 | `[CR][ABS-OA]` | VAE-Var: a VAE-learned latent prior represents non-Gaussian background errors, with an adjustable Gaussian constraint, for sparse paleoclimate proxies. | Bears on the bimodal (±B) posterior near a reversal (these:843). Not cited there: proposal of this note. |

**Line 3: software and sparse-sensor reconstruction.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C13 | Cheng S., Min J., Liu C., Arcucci R. (2025; online 2024). *TorchDA: A Python package for performing data assimilation with deep learning forward and transformation functions.* Computer Physics Communications 306, 109359. doi:10.1016/j.cpc.2024.109359; arXiv:2409.00244 | `[CR][AX][ABS-OA]` | Implements KF, EnKF, 3D-Var and 4D-Var with deep networks as transition and observation functions (Lorenz 63, 2D shallow water), in full or reduced space; GPL v3. **Named in the ANR abstract** `[WEB]`. | The generator as a source of background ensembles and a change of variable inside TorchDA (these:136, these:843). Direction C (enc:273). |
| C14 | Cheng S., Liu C., Guo Y., Arcucci R. (2024; page says 2023). *Efficient deep data assimilation with sparse observations and time-varying sensors.* Journal of Computational Physics 496, 112581. doi:10.1016/j.jcp.2023.112581; arXiv:2310.16187 | `[CR][AX][ABS-OA]` | VIVID: a Voronoi-tessellation plus CNN inverse operator inside the variational cost handles sparse, unstructured, time-varying sensors and couples to POD. | Direction C (enc:273). |
| C15 | Zhou H., Cheng S., Arcucci R. (2024). *Multi-fidelity physics constrained neural networks for dynamical systems.* CMAME 420, 116758. doi:10.1016/j.cma.2024.116758; arXiv:2402.02031 | `[CR][AX][ABS-OA]` | MSPCNN: a multi-fidelity autoencoder maps fidelities into one latent space, so physical-constraint losses can be evaluated in low-fidelity fields (2D Burgers, shallow water). | Cheaper constraints on 3D fields, direction A (enc:249). |
| C16 | Wang H., Zhou H., Cheng S. (2024; page says 2025). *Dynamical system prediction from sparse observations using deep neural networks with Voronoi tessellation and physics constraint.* CMAME 432, 117339. doi:10.1016/j.cma.2024.117339; arXiv:2409.00458 | `[CR][AX][ABS-OA]` | DSOVT: Voronoi tessellation with CED-LSTM or ConvLSTM, plus physics constraints in training, for sparse time-varying observations (sea-surface data, shallow water). | Background. |
| C17 | Cheng S. *et al.* (23 authors) (2025). *Machine learning for modelling unstructured grid data in computational physics: A review.* Information Fusion 123, 103255. doi:10.1016/j.inffus.2025.103255; arXiv:2502.09346 | `[CR][AX][ABS-OA]` | Reviews GNNs, spatial-attention transformers, interpolation-integrated methods and PINNs for unstructured grids; lists generative models on unstructured data among emerging directions. | SFEMaNS data are azimuthal Fourier modes on a meridian FE mesh (these:348). Direction E (enc:297). |

**Line 4: generative models for physical fields.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C18 | Cheng S., Guo Y., Arcucci R. (2023). *A Generative Model for Surrogates of Spatial-Temporal Wildfire Nowcasting.* IEEE TETCI 7(5), 1420–1430. doi:10.1109/TETCI.2023.3298535; arXiv:2308.02810 | `[CR][AX][ABS-OA]` | A 3D VQ-VAE generates unseen spatio-temporal burned-area sequences, accounting for vegetation and slope. The generated data train a surrogate tested on the real Chimney fire. | Precedent for generated fields feeding a downstream model, as the 2027 offer asks ("input for reduced-order models or data assimilation") (enc:132). |
| C19 **NEW** | Zhu K., Cheng S., Kovalchuk N., Simmons M., Guo Y.-K., Matar O.K., Arcucci R. (2023). *Analyzing drop coalescence in microfluidic devices with a deep learning generative model.* Physical Chemistry Chemical Physics 25, 15744–15755. doi:10.1039/D2CP05975D | `[CRs][ABS-OA]`. Title differs on Cheng's page (flag F2) | DSCVAE: a conditional VAE with label constraints in both latent and original space generates synthetic labelled data that improve classifiers. | Precedent for constraints imposed in both latent and data space (proposal of this note). |
| C20 | Zhuang Y., Cheng S., Duraisamy K. (2025). *Spatially-aware diffusion models with cross-attention for global field reconstruction with sparse observations.* CMAME 435, 117623. doi:10.1016/j.cma.2024.117623; arXiv:2409.00230 | `[CR][AX][ABS-AX]` | Score-based diffusion with a condition encoding (sparse observations plus interpolated field) and cross-attention, benchmarked on static and time-dependent PDEs. Diffusion wins under noise, the deterministic method on noiseless data; ensembles improve fused results. | Related work for reconstruction by diffusion (these:843). Priority reading (enc:144). |
| C21 | Yu W., Ghosh A., Finn T.S., Arcucci R., Bocquet M., Cheng S. (2026). *A probabilistic approach to wildfire spread prediction using a denoising diffusion surrogate model.* Geoscientific Model Development 19(2), 1027–1054. doi:10.5194/gmd-19-1027-2026; arXiv:2507.00761 | `[CR][AX][ABS-OA]` | A conditional diffusion surrogate with ensemble sampling is compared with a regression model of identical architecture. Averaged over two fire datasets, it gives a 67.6 % lower MSE at training size 900. | Protocol for comparing a generator with a regression model, and the uncertainty-aware "hit rate" score (enc:138, direction F enc:309). |
| C22 **NEW** | Zhou Y., Lin C., Kikumoto H., Ooka R., Cheng S. (2026). *Rooftop wind field reconstruction using sparse sensors: From deterministic to generative learning methods.* Building and Environment 296, 114480. doi:10.1016/j.buildenv.2026.114480; arXiv:2603.13077 | `[CR][AX][ABS-OA]` | Benchmarks kriging against UNet, ViTAE and a conditional Wasserstein GAN on wind-tunnel PIV data, with deep models up to 32.7 % better in SSIM. | Background (experimental-data generative benchmark). |
| C23 | Sabnis A.A., Mitrea M., Lugon L., Sartelet K., Bocquet M., Cheng X., Zhu S., Cheng S. (2026). *From Deterministic to Generative Deep Learning for Urban Air Quality Reconstruction from Sparse Observations.* arXiv:2607.25687 (preprint) | `[AX][ABS-AX]` | A diffusion framework reconstructs four pollutants in Paris from 9–28 stations and is benchmarked against deterministic models. | Background. |

**Line 5: physics-informed operators, chaos and Koopman representations.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C24 | Cheng X., He Y., Yang Y., Xue X., Cheng S., Giles D., Tang X., Hu Y. (2025). *Learning Chaos In A Linear Way.* ICLR 2025. arXiv:2503.14702 | `[AX][ABS-AX]`; ICLR status `[PREV encadrants.md:153]` | PFNN: an autoencoder and learned linear evolution operators enforce contraction and invariance of the measure "without any explicit knowledge of the invariant measure". | Closest supervisor-side precedent for learning through the invariant measure (enc:137). Not in the these:148 table: proposal of this note to add it there. |
| C25 | Yang Y., Cheng X., Giles D., Cheng S., He Y., Xue X., Chen B., Hu Y. (2025). *Tensor-Var: Efficient Four-Dimensional Variational Data Assimilation.* ICML 2025, PMLR 267:70649–70679 | `[PREV encadrants.md:154]`; title differs on Cheng's page today (flag F1) | Kernelised 4D-Var in a tensor-product feature space (per title and page). | Background. |
| C26 | Cheng X., Yuan W., Yang Y., Zhang Y., Cheng S., He Y., Sun Z. (2026). *Information Shapes Koopman Representation.* ICLR 2026 (oral per OpenReview, `[PREV]`). arXiv:2510.13025 | `[AX][ABS-AX]` | An information-theoretic Lagrangian balances latent mutual information (simplicity) against von Neumann entropy (expressiveness, against mode collapse) in Koopman learning. | Background (latent dynamics). |
| C27 | Xue X., ten Eikelder M.F.P., Gao M., Cheng X., Yang Y., He Y., Wang S., Cheng S., Hu Y., Coveney P.V. (2026). *Fast-forward prediction of lattice Boltzmann dynamics with physics-informed neural operators.* Nature Communications 17, 9243. doi:10.1038/s41467-026-75730-1 | `[CR][ABS-OA]` | A neural operator predicts LBE evolution over large time jumps. It embeds moment-matching constraints and global equivariance, and is discretization-invariant (coarse training, finer inference). | Moment constraints and equivariance built in, direction E (enc:297). |
| C28 **NEW** | Zhou H., Cheng S. (2025). *Improving long-term autoregressive spatiotemporal predictions: A proof of concept with fluid dynamics.* CMAME 447, 118332. doi:10.1016/j.cma.2025.118332 | `[CR][ABS-OA]` | Stochastic PushForward (SPF) keeps one-step-ahead training while enabling multi-step learning, to limit error accumulation in long autoregressive rollouts. | Proposal of this note: training a transition generator (direction B, these:784) for long rollouts. |
| C29 | Zhang Z., Yuan W., Cheng X., Behnoudfar P., Chen C., Moser C., Tarumi Y., Wu J.-L., Arcucci R., Miyoshi T., Chen N., Bocquet M., Cheng S. (2026). *When Latent Dynamics Meet Data Assimilation: A Benchmark of Koopman-Type Representations.* arXiv:2611.03916 (preprint) | `[AX][ABS-AX]` | Compares seven methods on five systems and reports "a trade-off between representational flexibility and optimization tractability" in deep latent DA. | Background for direction C. |
| C30 | Zhou Q., Zhu X., Joli P., Cong Y., Cheng S. (2026). *Variational Parameter Calibration with Physics-Aware Latent-Space Surrogates.* arXiv:2608.11435 (preprint) | `[AX][ABS-AX]` | A differentiable parameters-to-fields latent surrogate with observable supervision. It finds that "reconstruction accuracy alone is insufficient for inverse modeling". | Directions A and D (enc:249, enc:285). |

**Line 6: generative dynamics inside data assimilation, and reviews.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| C31 | Bocquet M., Finn T.S., Cheng S. (2026). *Accounting for model error in ensemble variational data assimilation through learned generative dynamics.* arXiv:2610.17333 (preprint) | `[AX][ABS-AX]` | IEnKF-G: a learned conditional stochastic forecast replaces additive Gaussian model error in a one-step weak-constraint 4D-Var. It is generally more accurate than IEnKF-Q on stochastic Lorenz-63 and multiscale Lorenz-96, with "substantial gains under partial observations". | Most direct bridge between generative models and DA (these:843; enc:140). |
| C32 **NEW** | Bocquet M., Finn T.S., Cheng S., Farchi A. (2026). *Elucidating the performance of data assimilation neural networks for chaotic dynamics.* Nonlinear Processes in Geophysics 33(3), 401–424. doi:10.5194/npg-33-401-2026 | `[CR][ABS-OA]` | Analyses analysis operators learned from a true trajectory and its observations, which reach EnKF-like accuracy on low-order chaotic dynamics with a single forecast instead of an ensemble. | Background for direction C. |
| C33 | Cheng S. *et al.* (17 authors, including D. Lucor) (2023). *Machine Learning With Data Assimilation and Uncertainty Quantification for Dynamical Systems: A Review.* IEEE/CAA J. Autom. Sinica 10(6), 1361–1387. doi:10.1109/JAS.2023.123537; arXiv:2303.10462 | `[CR][AX][ABS-OA]` | Describes itself as "the first overview" of ML combined with DA and UQ (system identification, reduced surrogates, error-covariance specification, model-error correction). | Shared vocabulary (enc:131). |
| C34 **NEW** | Arcucci R., Healy S., Dance S., … Cheng S., Bocquet M., … (35 authors) (2026). *The convergence of machine learning and data assimilation in Earth system science.* npj Artificial Intelligence 2(1), 48. doi:10.1038/s44387-026-00107-0 | `[CR][ABS-OA]` | Perspective: ML accelerates DA, while DA provides uncertainty quantification and physical constraints to ML. | Background. |

**Other lines, less related.** These are not detailed here:
- wildfire risk and remote sensing (PyTorchFire, Xia & Cheng 2025, EMS 188, 106401, doi:10.1016/j.envsoft.2025.106401 `[CR]`);
- microfluidics and chemical engineering;
- nuclear-reactor reconstruction (Gong *et al.* 2024, NST 35(5), 43 `[CR]`);
- field reconstruction with ViTAE-SL (Fan *et al.* 2025, CPC 308, 109464, doi:10.1016/j.cpc.2024.109464 `[CR]`, abstract not read).

**Résumé (FR).** Sibo Cheng est professeur junior (chaire CPJ) à l'École nationale des ponts et chaussées, au CEREA. Il a fait sa thèse (Université Paris-Saclay, 2020) sous la direction de Didier Lucor, avec EDF R&D, sur la spécification des covariances d'erreur en assimilation de données (méthodes CUTE et PUB, réglage adaptatif, localisation par clustering de graphe). Ses publications suivent ensuite trois fils.
- **Assimilation dans un espace latent.** Assimilation latente généralisée (2022), encodeurs-décodeurs multi-domaines (2024), assimilation latente non gaussienne par VAE (2026).
- **Logiciel.** TorchDA (2025), que cite le résumé ANR de MilaDy, avec filtres de Kalman et 3D-/4D-Var à réseaux profonds.
- **Modèles génératifs pour des champs physiques.** VQ-VAE pour les incendies (2023), diffusion conditionnelle pour la reconstruction (2025) et pour la prévision probabiliste (GMD, 2026), dynamique générative dans un 4D-Var à contrainte faible (préprint 2026).

S'y ajoutent des réseaux à contraintes physiques (multi-fidélité 2024, opérateur neuronal à contraintes de moments 2026) et des représentations de dynamiques chaotiques qui préservent la mesure invariante (ICLR 2025). Il est co-investigateur de MilaDy et sa page annonce le co-encadrement de la thèse avec D. Lucor. Aucune publication de lui sur les dynamos n'a été trouvée : la thèse s'appuierait sur son travail pour l'assimilation (a priori génératif, TorchDA) et pour le protocole d'évaluation des générateurs.

---

## 3. Didier Lucor (LISN, CNRS)

### 3.1 Profile (verified `[WEB]` https://perso.lisn.upsaclay.fr/lucor/ and /people.html)

- **Position.** CNRS research director at LISN, member of the DATAFLOT group; one of the two deputy directors of
  LISN in 2022–2025.
- **Career.** MSc and PhD in applied mathematics, Brown University, 2004. Two years as a postdoc in Ocean
  Engineering at MIT. Ten years at the Institut d'Alembert.
- **Stated research interests (own page).** "stochastic modeling and computational mechanics, with emphasis on:
  physics-informed statistical learning, reduced-order modeling, uncertainty quantification, data assimilation,
  sensitivity analysis and robust optimization".
- **Supervisions listed on his page.**
  - S. Cheng: PhD, joined 12/2017, graduated 11/2020, with EDF R&D.
  - R. Bousquet: MSc M2, LISN, 2022.
  - L. Achard: joint PhD with the University of Exeter, 2025–present, "co-supervised by researchers from …
    Exeter, CEREA at ENPC/IPP and L2S".
- **No dynamo-theory paper.** His dynamo-related outputs are co-authored with C. Nore (M4, M5, M7) `[HAL]`.

### 3.2 Research lines and publications

**Line 1: uncertainty quantification with generalized polynomial chaos (landmarks).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| L1 **NEW** | Xiu D., Lucor D., Su C.-H., Karniadakis G.E. (2002; online 2001). *Stochastic Modeling of Flow-Structure Interactions Using Generalized Polynomial Chaos.* Journal of Fluids Engineering 124(1), 51–59. doi:10.1115/1.1436089 | `[CR][ABS-OA]` | Represents stochastic inputs with Askey-scheme orthogonal polynomials and a Galerkin projection in random space, generalising Wiener–Hermite chaos. Applied to oscillators, then coupled to incompressible Navier–Stokes. | Origin of the parametric-uncertainty view (background). |
| L2 **NEW** | Lucor D., Su C.-H., Karniadakis G.E. (2004). *Generalized polynomial chaos and random oscillators.* IJNME 60(3), 571–596. doi:10.1002/nme.976 | `[CR][ABS-OA]` | gPC solutions for linear random oscillators with error estimates; it can be "orders of magnitude faster" than Monte Carlo for compact distributions. | Background. |
| L3 | Lucor D., Karniadakis G.E. (2004). *Adaptive Generalized Polynomial Chaos for Nonlinear Random Oscillators.* SIAM J. Sci. Comput. 26(2), 720–735. doi:10.1137/S1064827503427984 | `[CR][ABS-OA]` | Adaptive gPC for the random Duffing oscillator with Gaussian and non-Gaussian excitations. | Background. |
| L4 | Lucor D., Karniadakis G.E. (2004). *Noisy Inflows Cause a Shedding-Mode Switching in Flow Past an Oscillating Cylinder.* PRL 92(15), 154501. doi:10.1103/PhysRevLett.92.154501 | `[CR][ABS-OA]` | Stochastic simulations with a polynomial chaos method show that inflow noise switches the wake from a P+S to a 2S shedding mode. | Background (noise-induced switching between flow states). |
| L5 | Lucor D., Meyers J., Sagaut P. (2007). *Sensitivity analysis of large-eddy simulations to subgrid-scale-model parametric uncertainty using polynomial chaos.* JFM 585, 255–279. doi:10.1017/S0022112007006751 | `[CR][ABS-OA]` | Non-intrusive gPC sensitivity of LES statistics of decaying isotropic turbulence to the Smagorinsky constant: small scales are mainly affected. | Dependence of turbulent statistics on a parameter (enc:156). |

**Line 2: reduced-order models and latent spaces.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| L6 | El Garroussi S., Ricci S., De Lozzo M., Goutal N., Lucor D. (2022; online 2021). *Tackling random fields non-linearities with unsupervised clustering of polynomial chaos expansion in latent space: application to global sensitivity analysis of river flooding.* SERRA 36(3), 693–718. doi:10.1007/s00477-021-02060-7 | `[CR][ABS-OA]` | Autoencoder dimension reduction plus a mixture of local PCEs on ML-clustered input space, for the sensitivity analysis of a Telemac-2D model of the Garonne. | Background. |
| L7 | Nony B.X., Rochoux M.C., Jaravel T., Lucor D. (2023). *Reduced-order modeling for parameterized large-eddy simulations of atmospheric pollutant dispersion.* SERRA 37(6), 2117–2144. doi:10.1007/s00477-023-02383-7 | `[CR][ABS-HAL hal-04310872]` | POD with Gaussian-process regression predicts first- and second-order concentration statistics of parameterized LES; GPR hyperparameters are tuned through the POD mode hierarchy by Bayesian optimisation. | Few costly simulations for many parameters, the dynamo-data situation (enc:159). |
| L8 | M4, M5, M7 (with C. Nore): AE/VAE versus POD, von Kármán LES/POD, polynomial AEs. | see §1.3 | | AE/VAE baselines (these:935). |

**Line 3: physics-informed learning, invariances and turbulence.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| L9 | Lucor D., Agrawal A., Sergent A. (2022). *Simple computational strategies for more effective physics-informed neural networks modeling of turbulent natural convection.* Journal of Computational Physics 456, 111022. doi:10.1016/j.jcp.2022.111022. Preprint arXiv:2103.03565 (title "Physics-aware deep neural networks for surrogate modeling of turbulent natural convection") | `[CR][AX][ABS-AX]`, preprint abstract only | PINNs for turbulent Rayleigh–Bénard convection from DNS temperature data. Two ingredients: a "padding" of collocation points, and relaxing the incompressibility condition "in such a way that it drastically benefits the optimization search". Ra = 2·10⁹ in the preprint. | Hard-versus-soft constraint trade-off, direction E (enc:297). |
| L10 | Cai J., Angeli P.-E., Martinez J.-M., Damblin G., Lucor D. (2024). *Revisiting Tensor Basis Neural Network for Reynolds stress modeling: Application to plane channel and square duct flows.* Computers & Fluids 275, 106246. doi:10.1016/j.compfluid.2024.106246; arXiv:2403.11746 | `[CR][AX][ABS-AX]` | Tensor-basis networks preserve Galilean and rotational invariance. They predict the anisotropy tensor at unobserved Re_τ (channel), and transfer learning handles the square duct. | Symmetry imposed by architecture (enc:160). |
| L11 | Sundar R., Majumdar D., Lucor D., Sarkar S. (2024), JFS 125, 104066, doi:10.1016/j.jfluidstructs.2024.104066; Sundar R., Lucor D., Sarkar S. (2025), JFS 139, 104421, doi:10.1016/j.jfluidstructs.2025.104421; arXiv:2503.15679 | `[CR][AX]`; contribution `[PREV encadrants.md:192-193]` | PINNs with moving immersed boundaries; sequential (time-decomposed) learning with transfer for long unsteady integration. | Background. |
| L12 | Volk M.-C., Sergent A., Lucor D., Mommert M., Bauer C., Wagner C. (2025). *A PINN methodology for temperature field reconstruction in the PIV measurement plane: Case of Rayleigh–Bénard convection.* ICHMT 167, 109284. doi:10.1016/j.icheatmasstransfer.2025.109284 | `[CR][ABS-OA]` | A PINN infers temperature from stereo-PIV velocity in one plane (Ra = 10⁷, Pr = 0.7), with dynamic collocation sampling. | Background (reconstruction from partial observations). |
| L13 **NEW** | Brichet L., Carbonneau N., Bernard E., Braun R., Méthivier L., Fraigneau Y., Lucor D., Chillà F., *et al.* (2025). *Universal scaling law in turbulent Rayleigh–Bénard convection with and without roughness.* JFM, doi:10.1017/jfm.2025.10938; hal-04434081 | `[HAL][ABS-OA]`; volume and pages not checked | New experimental and numerical Nu–Ra measurements up to Ra ≈ 10¹² with smooth or mixed smooth–rough boundaries. | Background (turbulence physics). |

**Line 4: calibrated uncertainty, robust optimisation, data fusion.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| L14 | Jaber E., Blot V., Brunel N.J.-B., Chabridon V., Remy E., Iooss B., Lucor D., Mougeot M., Leite A. (2025). *Conformal approach to Gaussian process surrogate evaluation with marginal coverage guarantees.* JMLMC 6(3), 37–68. doi:10.1615/JMachLearnModelComput.2025054687 | `[CR][ABS-OA]`. Title variants (flag F4) | Adaptive cross-conformal intervals that weight the nonconformity score by the GP posterior standard deviation, with marginal coverage guarantees. | Calibration check of a generator's uncertainty, direction F (enc:309). |
| L15 | Zhou H., Wang Z., Lucor D., Sauret E. (2026). *New Bayesian optimisation framework for robust multi-objective design: decoupling performance and uncertainty.* RESS 274, 112359. doi:10.1016/j.ress.2026.112359 | `[CR][ABS-OA]` | Variance-constrained robust Bayesian optimisation with a robust GP and variance-penalised scalarisation. | DRESDYN exploration under uncertainty, direction D (enc:285). |
| L16 | Jaber E., Remy E., Chabridon V., Mougeot M., Lucor D. (2026). *Fusion of heterogeneous data for robust degradation prognostics.* RESS 274, 112435. doi:10.1016/j.ress.2026.112435 | `[CR][ABS-OA]` | Offline assimilation in two steps: Bayesian model updating (MCMC with kernel sensitivity ranking), then ensemble Kalman smoothing. | Background. |

**Line 5: data assimilation.** Co-author of C1–C4 and C33 with S. Cheng; director of Cheng's PhD (tel-03117151).

**Résumé (FR).** Didier Lucor est directeur de recherche CNRS au LISN (groupe DATAFLOT). Sa carrière commence à Brown (thèse 2004) avec le chaos polynomial généralisé : interaction fluide-structure (2002), oscillateurs aléatoires (2004), changement de mode de lâcher tourbillonnaire induit par le bruit (PRL 2004), sensibilité des LES à la constante de Smagorinsky (JFM 2007). Ses travaux récents couvrent :
- les modèles réduits paramétriques (POD et processus gaussiens pour des LES de dispersion, 2023 ; autoencodeurs et chaos polynomial, 2021) ;
- l'apprentissage informé par la physique : PINN pour la convection turbulente, avec relaxation de l'incompressibilité (JCP 2022) ; réseaux à base tensorielle qui respectent les invariances galiléenne et rotationnelle (2024) ;
- la prédiction conforme pour évaluer des surrogates (2025) ;
- l'optimisation robuste et la fusion de données (2026).

Il a dirigé la thèse de Sibo Cheng sur les covariances en assimilation. Avec Caroline Nore, il a co-signé les travaux qui comparent autoencodeurs, VAE et POD sur des écoulements forcés et sur l'écoulement de von Kármán (CPC 2025, préprint 2026). Aucune publication de lui sur la théorie de la dynamo n'a été trouvée. Pour la thèse, ses travaux servent de référence de base pour l'espace latent et de cadre pour juger le compromis entre contraintes strictes et relâchées et pour calibrer l'incertitude.

---

## 4. Caroline Nore (LISN, Université Paris-Saclay)

### 4.1 Profile (verified)

- **Affiliation and role.** "Laboratoire Interdisciplinaire des Sciences du Numérique – Université Paris-Saclay,
  CNRS" (RNL 2026 abstract `[WEB]`). Called "Pr." in the three offers `[PDF]`. Coordinator of MilaDy `[WEB ANR]`.
  HAL structures of her recent papers include the COMET team `[HAL]`.
- **SFEMaNS.** Her own seminar abstract (LadHyX, 18 January, LIMSI affiliation) says: "We have been developing a
  so-called code SFEMaNS since 2002 … capable of simulating the nonlinear magnetohydrodynamic (MHD) equations in
  heterogeneous domains (with electrical conductivity or magnetic permeability jumps) in axisymmetric
  geometries". It names J.-L. Guermond, J. Léorat, F. Luddens, W. Herreman, L. Cappanera and D. Castanon-Quiroz
  as collaborators `[PDF https://www.ladhyx.polytechnique.fr/media/evenement/180118_CarolineNore.pdf]`.
- **SFEMaNS documentation** `[WEB https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html]`: "Fourier
  decomposition in the azimuthal direction and Lagrange finite elements in the meridian section"; entropy-viscosity
  stabilisation; permeability that may depend on time and azimuth.
- **Theses supervised (HAL)** `[HAL]`:
  - M. Creff, *Role of energy transfers in the dynamo effect: application to the von Kármán flow*, 2023, with
    B. Dubrulle, tel-04477539.
  - M. Quattromini, *Graph Neural Networks for fluid mechanics: data-assimilation and optimization*, 2024,
    co-directed with S. Cherubini, O. Semeraro and M. A. Bucci, tel-04964013.
  - Earlier: F. Luddens 2012 and L. Cappanera 2015 `[PREV encadrants.md:261]`.

### 4.2 Research lines and publications

**Line 1: early dynamo and von Kármán hydrodynamics (landmarks).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| N1 **NEW** | Nore C., Brachet M.E., Politano H., Pouquet A. (1997). *Dynamo action in the Taylor–Green vortex near threshold.* Physics of Plasmas 4(1), 1–3. doi:10.1063/1.872578 | `[CR][ABS-OA]` | Numerical demonstration of dynamo action in the forced Taylor–Green vortex, a confined swirling flow of two counter-rotating eddies. The threshold "depends crucially on the fundamental symmetries" of the flow, and the magnetic boundary conditions select the fastest-growing mode. | Taylor–Green is the tier-2 reference flow (these:908); this is its first dynamo study by a supervisor. |
| N2 **NEW** | Nore C., Tuckerman L.S., Daube O., Xin S. (2003). *The 1:2 mode interaction in exactly counter-rotating von Kármán swirling flow.* JFM 477, 51–88. doi:10.1017/S0022112002003075 | `[CR][ABS-OA]` | As Re increases, the axisymmetric counter-rotating flow goes through m = 1 steady states, travelling waves, near-heteroclinic cycles and m = 2 states, explained by a near codimension-two bifurcation with O(2) symmetry. | Symmetry-breaking background for the Rπ and equivariance discussion (proposal of this note). |
| N3 **NEW** | Nore C., Tartar M., Daube O., Tuckerman L.S. (2004). *Survey of instability thresholds of flow between exactly counter-rotating disks.* JFM 511, 45–65. doi:10.1017/S0022112004008559 | `[CR][ABS-OA]` | Linear-stability survey for 0.5 ≤ Γ ≤ 3: the dominant modes are non-axisymmetric and stationary. | Background. |
| N4 **NEW** | Nore C., Moisy F., Quartier L. (2005). *Experimental observation of near-heteroclinic cycles in the von Kármán swirling flow.* Physics of Fluids 17(6), 064103. doi:10.1063/1.1926827 | `[CR][ABS-OA]` | Visualisations and PIV observe robust near-heteroclinic cycles linking two unstable m = 2 states, compared with the 2003 simulations. | Background (intermittent switching in the VKS geometry). |

**Line 2: numerical MHD in heterogeneous domains (the SFEMaNS method papers).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| N5 | Guermond J.-L., Laguerre R., Léorat J., Nore C. (2007). *An interior penalty Galerkin method for the MHD equations in heterogeneous domains.* JCP 221(1), 349–369. doi:10.1016/j.jcp.2006.06.045 | `[CR][ABS-HAL hal-02365556]` | Lagrange finite elements with interior-penalty continuity across conducting and non-conducting regions; stable and convergent; Ohmic decay and kinematic dynamos. | Interface-penalty route for vacuum matching (these:266). Direction E (enc:297). |
| N6 | Guermond J.-L., Laguerre R., Léorat J., Nore C. (2009). *Nonlinear magnetohydrodynamics in axisymmetric heterogeneous domains using a Fourier/finite element technique and an interior penalty method.* JCP 228(8), 2739–2757. doi:10.1016/j.jcp.2008.12.026 | `[CR][ABS-HAL hal-02365547]` | Finite elements in the meridian plane and Fourier modes in azimuth, parallelised over the Fourier modes, with interior-penalty continuity; kinematic and full dynamos. | Fixes the data structure (modes m × meridian FE) of the generated fields (these:266, these:348). |
| N7 | Guermond J.-L., Léorat J., Luddens F., Nore C., Ribeiro A. (2011). *Effects of discontinuous magnetic permeability on magnetodynamic problems.* JCP 230(16), 6299–6319. doi:10.1016/j.jcp.2011.04.026 | `[CR][ABS-HAL hal-02365526]` | A Lagrange-FE technique for discontinuous permeability and non-smooth interfaces, validated on benchmarks and used for kinematic studies of VKS2. | Permeability-jump conditions at the soft-iron impellers (these:269). |

**Line 3: VKS and the role of ferromagnetic impellers.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| N8 | Laguerre R., Nore C., Ribeiro A., Léorat J., Guermond J.-L., Plunian F. (2008). *Impact of Impellers on the Axisymmetric Magnetic Mode in the VKS2 Dynamo Experiment.* PRL 101(10), 104501. doi:10.1103/PhysRevLett.101.104501; arXiv:0805.2805 | `[CR][AX][ABS-OA]` | Modelling the induction (α effect) of the spiralling flow between blades in a kinematic code excites the axisymmetric mode. The observed Rm_c ≈ 32 "can be reached easily with ferromagnetic boundary conditions". | Why material properties are conditioning parameters (enc:180). |
| N9 **NEW** | Léorat J., Nore C. (2008). *Interplay between experimental and numerical approaches in the fluid dynamo problem.* Comptes Rendus Physique 9(7), 741–748. doi:10.1016/j.crhy.2008.07.006 | `[CR][ABS-OA]` | Outlines ten years of numerical work accompanying VKS and how it contributed to optimising the facility. | Background (history for chSOA1). |
| N10 **NEW** | Giesecke A., Nore C., Plunian F., Laguerre R., Ribeiro A., Stefani F., Gerbeth G., Léorat J., Guermond J.-L. (2010). *Generation of axisymmetric modes in cylindrical kinematic mean-field dynamos of VKS type.* GAFD 104, 249–271. doi:10.1080/03091920903366303 | `[CRs][ABS-OA]` (issue number not checked) | Simple α-effect distributions require "unrealistically large values" of α to explain the axisymmetric VKS mode. | Background. |
| N11 | Giesecke A., Nore C., Stefani F., Gerbeth G., Léorat J., Luddens F., Guermond J.-L. (2010). *Electromagnetic induction in non-uniform domains.* GAFD 104(5–6), 505–529. doi:10.1080/03091929.2010.507202 | `[CR][ABS-OA]` | Two codes are cross-validated. High-permeability disks lower Rm_c of the simplest non-axisymmetric mode, but not enough to explain VKS. | Background. |
| N12 | Giesecke A., Nore C., Stefani F., Gerbeth G., Léorat J., Herreman W., Luddens F., Guermond J.-L. (2012). *Influence of high-permeability discs in an axisymmetric model of the Cadarache dynamo experiment.* NJP 14, 053005. doi:10.1088/1367-2630/14/5/053005; arXiv:1112.1780 | `[CR][AX][ABS-OA]` | Rm_c(μr) − Rm_c(∞) ∝ μr^(−1/2), suggesting a skin effect. At large μr, a purely toroidal axisymmetric mode localised in the discs dominates. | μr as a conditioning parameter with a known scaling (proposal of this note). Direction E (enc:297). |
| N13 | Nore C., Léorat J., Guermond J.-L., Giesecke A. (2015). *Mean-field model of the von Kármán sodium dynamo experiment using soft iron impellers.* PRE 91, 013008. doi:10.1103/PhysRevE.91.013008 | `[CR][ABS-OA]` | A mean-field model (axisymmetric mean flow, localised permeability and α effect) confirms "the leading role played by the ferromagnetic impellers"; the dynamo is oscillatory or stationary depending on permeabilities. | Background. |
| N14 **NEW** | Varela J., Brun S., Dubrulle B., Nore C. (2015). *Role of boundary conditions in helicoidal flow collimation: Consequences for the von Kármán sodium dynamo experiment.* PRE 92, 063015. doi:10.1103/PhysRevE.92.063015. Follow-up: Varela *et al.* (2017), Physics of Plasmas 24, 053518, doi:10.1063/1.4983313 | `[CRs][ABS-OA]` | PLUTO simulations of one impeller cavity: a helicoidal vortex between the blades collimates field lines, enhancing the radial field more for ferromagnetic than for conducting blades. | Background. |
| N15 | Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2016). *Direct numerical simulation of the axial dipolar dynamo in the Von Kármán Sodium experiment.* EPL 114(6), 65002. doi:10.1209/0295-5075/114/65002 | `[CR][ABS-OA]` | "For the first time", a fully nonlinear MHD DNS of VKS with both impellers. The threshold decreases as impeller permeability increases. Ferromagnetic impellers give a mostly axisymmetric axial dipole. | Tier-3 data (these:929, these:933). |
| N16 | Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2018). *Numerical simulation of the von Kármán sodium dynamo experiment.* JFM 854, 164–195. doi:10.1017/jfm.2018.582 | `[CR][ABS-OA]` (abstract truncated after the μ result; the Re dependence is `[PREV encadrants.md:225]`) | Soft-iron impellers enter through a pseudo-penalty method, with LES at high Re (Kolmogorov-like spectrum, helical vortices at the blade tips). At fixed Re, raising impeller permeability lowers Rm_c. | Vacuum condition and nondimensional induction equation (these:256, these:650). Divergence control of the data (these:348). Tier 3 (these:929). |
| N17 | Creff M., Faller H., Dubrulle B., Guermond J.-L., Nore C. (2024). *Tracking dynamo mechanisms from local energy transfers: Application to the von Kármán sodium dynamo.* Physics of Plasmas 31(2), 022306. doi:10.1063/5.0174251 | `[CR][ABS-OA]` | Local energy budgets in space, scale and time, through a filtering usable on unstructured meshes, applied to VKS DNS with steel or soft-iron impellers. | Tier-3 data (these:929). Fine-grained physical metric, direction F (enc:309). |
| N18 | M4–M6, M1, M8 (with Bousquet, Botez, Lucor, Ponty): AE/VAE vs POD, POD of VKS, reversals and DQVU. | §1.3 | | §1.3 |

**Line 4: precession and DRESDYN.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| N19 | Nore C., Léorat J., Guermond J.-L., Luddens F. (2011). *Nonlinear dynamo action in a precessing cylindrical container.* PRE 84(1), 016317. doi:10.1103/PhysRevE.84.016317; arXiv:1102.1846 | `[CR][AX][ABS-OA]` | Precession can trigger dynamo action in a cylinder. The flow loses centro-symmetry and becomes quasiperiodic, and the field is unsteady and quadrupolar, which "may be useful" for the planned Dresden experiment. | Physics behind objective (ii), direction D (enc:285). |
| N20 **NEW** | Hollerbach R., Nore C., Marti P., Vantieghem S., Luddens F., Léorat J. (2013). *Parity-breaking flows in precessing spherical containers.* PRE 87, 053020. doi:10.1103/PhysRevE.87.053020 | `[CR][ABS-OA]` | Bifurcation sequences that break the antipodal symmetry U(−r) = −U(r) in precessing spheres and shells up to Re ≈ 1280. | Background. |
| N21 | Stefani F., Albrecht T., Gerbeth G., Giesecke A., Gundrum T., Herault J., Nore C., Steglich C. (2015). *Towards a precession driven dynamo experiment.* Magnetohydrodynamics 51(2), 275–284. doi:10.22364/mhd.51.2.11 | `[CR][ABS-OA]` | Scientific background, water pre-experiments, numerical predictions and design problems of the DRESDYN precession dynamo machine. | Direction D (enc:285). |
| N22 **NEW** | Nore C., Castanon Quiroz D., Guermond J.-L., Léorat J., Luddens F. (2015). *Numerical dynamo action in cylindrical containers.* European Physical Journal Applied Physics 70(3), 31101. doi:10.1051/epjap/2015150049 | `[CR][ABS-OA]` | Simulations of dynamo action for the VKS and DRESDYN cylinders. | Background linking both objectives. |
| N23 | Cappanera L., Guermond J.-L., Léorat J., Nore C. (2016). *Two spinning ways for precession dynamo.* PRE 93(4), 043113. doi:10.1103/PhysRevE.93.043113 | `[CR][ABS-OA]` | With the spin–precession angle at π/2, equatorial spinning breaks the flow's centro-symmetry more efficiently than axial spinning, and its unsteady asymmetric flow sustains dynamo action. | Direction D (enc:285). |
| N24 | M2: Botez *et al.* (2026), PRFluids 11, 083701 | §1.3 | | Tier 4 (these:943). |

**Line 5: other dynamo geometries and community benchmarks.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| N25 | Nore C., Guermond J.-L., Laguerre R., Léorat J., Luddens F. (2012). *Nonlinear dynamo in a short Taylor–Couette setup.* Physics of Fluids 24(9), 094106. doi:10.1063/1.4752756 | `[CR][AX 1204.0555][ABS-OA]` | A short Taylor–Couette setup with a body force sustains dynamo action. The nonlinear regime shows a tilted dipole whose axial component "exhibits aperiodic reversals". | Second reversal system, direction B (enc:261). |
| N26 **NEW** | Jackson A., Sheyko A., Marti P., Tilgner A., Cébron D., Vantieghem S., Simitev R., Busse F., Zhan X., Schubert G., Takehiro S., Sasaki Y., Hayashi Y.-Y., Ribeiro A., Nore C., Guermond J.-L. (2014). *A spherical shell numerical dynamo benchmark with pseudo-vacuum magnetic boundary conditions.* GJI 196(2), 712–723. doi:10.1093/gji/ggt425 | `[CR][ABS-OA]` (which code the SFEMaNS co-authors ran is not checked) | Community comparison of codes on a rotating Boussinesq convection-driven dynamo in a spherical shell with pseudo-vacuum magnetic boundary conditions. | Background (chSOA1, numerical dynamos). |

**Line 6: machine learning.** Co-author of M4 and M7. Co-director of the Quattromini thesis (GNN for data
assimilation and optimisation, 2024) `[HAL]`.

**Other lines, not related to the thesis.**
- Liquid-metal batteries: Herreman *et al.* 2015, JFM 771, 79–114; Nore *et al.* 2021, PRL 126, 184501 `[CR]`.
- Ferrofluid cooling (IEEE TMAG papers) and superfluid turbulence (1997–2003) `[HAL]`.

**Résumé (FR).** Caroline Nore (LISN, Université Paris-Saclay) coordonne MilaDy. Elle a d'abord publié en 1997 l'une des premières dynamos numériques dans le tourbillon de Taylor–Green, avec un seuil qui dépend des symétries de l'écoulement. Puis, de 2003 à 2005, des travaux sur les bifurcations de l'écoulement de von Kármán contrarotatif : cycles quasi hétéroclines, en simulation et en expérience. Depuis 2002, selon ses propres termes, elle développe avec J.-L. Guermond le code SFEMaNS (Fourier en azimut, éléments finis de Lagrange dans le plan méridien, pénalisation intérieure, sauts de perméabilité ; JCP 2007, 2009, 2011). Avec ce code, elle a étudié :
- le rôle des turbines ferromagnétiques dans VKS : mode axisymétrique (PRL 2008), disques de forte perméabilité (NJP 2012), modèle de champ moyen (PRE 2015), première DNS non linéaire complète de VKS avec turbines (EPL 2016, JFM 2018) ;
- les dynamos de précession pour DRESDYN (PRE 2011, 2016 ; MHD 2015 ; PRFluids 2026) ;
- la dynamo de Taylor–Couette à inversions apériodiques (PoF 2012) ;
- les bilans d'énergie locaux (PoP 2024).

Avec R. Bousquet, D. Lucor et Y. Ponty, elle a montré le mécanisme des inversions de VKS et construit le modèle réduit DQVU (PRFluids 2026). Elle a co-dirigé une thèse sur les GNN pour l'assimilation de données (2024). Pour la thèse, ses travaux fournissent les données de référence (SFEMaNS, VKS, précession), la structure des champs à générer et les conditions d'interface et de vide qu'un générateur doit respecter.

---

## 5. Yannick Ponty (Lagrange, Observatoire de la Côte d'Azur, CNRS)

### 5.1 Profile (verified `[PDF]` CV 2026, https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf)

- **Career.**
  - CNRS research director since October 2014 at the J.-L. Lagrange laboratory (UMR 7293), OCA.
  - Head of the "Turbulence Fluide et Plasma" team since October 2025 (also 2011–2021).
  - External member of the Inria CASTOR team.
  - CNRS chargé de recherche 2000–2014; research fellow in the Exeter MHD group 1997–2000.
- **Degrees.** PhD 1997, "Textures convectives dans un fluide en rotation et effet dynamo dans un écoulement
  chaotique". HDR 31 January 2012, "Rôle de la turbulence sur l'effet dynamo et l'induction magnétique"
  (tel-00922148 `[HAL]`).
- **Keywords (own CV).** "Magnétohydrodynamique (MHD), Effet Dynamo, Turbulence, HPC (High Performance Computing),
  Contrôle Optimale".
- **His "5 Publications significatives" (CV):** Bousquet *et al.* 2026; Ponty, Politano, Pouquet 2025;
  Mannix, Ponty, Marcotte 2022; Kreuzahler *et al.* 2017; Ponty *et al.* 2007 (PRL).
- **Supervision.** Co-supervised S. Kreuzahler's PhD (Bochum, with R. Grauer, 2012–2015) on penalisation
  methods for VKS. Supervises a MilaDy postdoc since February 2026 (name written "Hiroshi Hiiro"; flag F14).
- **No machine-learning publication** among his 30 HAL records (all read today) `[HAL]`.

### 5.2 Research lines and publications

**Line 1: kinematic dynamo theory.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| P1 **NEW** | Ponty Y., Gilbert A.D., Soward A.M. (2001). *Kinematic dynamo action in large magnetic Reynolds number flows driven by shear and convection.* JFM 435, 261–287. doi:10.1017/S0022112001003755 | `[CR][ABS-OA]` | Kinematic dynamo action in a dynamically driven plane-layer flow: an Ekman layer destabilised by convection or shear, as a local model of the solar tachocline. | Background. |

**Line 2: low-Pm dynamos in the Taylor–Green flow (a von Kármán proxy).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| P2 | Ponty Y., Politano H., Pinton J.-F. (2004). *Simulation of Induction at Low Magnetic Prandtl Number.* PRL 92(14), 144503. doi:10.1103/PhysRevLett.92.144503 | `[CR][ABS-OA]` | A mixed scheme (resolved magnetic fluctuations, LES for velocity) computes induction by a forced Taylor–Green flow in an applied field, in agreement with experimental data and with a 1/f behaviour at long times. | Background. |
| P3 | Ponty Y., Mininni P.D., Montgomery D.C., Pinton J.-F., Politano H., Pouquet A. (2005). *Numerical Study of Dynamo Action at Low Magnetic Prandtl Numbers.* PRL 94(16), 164502. doi:10.1103/PhysRevLett.94.164502; arXiv:physics/0410046 | `[CR][AX][ABS-OA][ABS-AX]` | Combining DNS, a Lagrangian-averaged model and LES, Taylor–Green dynamos are found from P_M = 1 down to 10⁻². Rm_c rises sharply with P_M⁻¹ and then saturates. "a Kazantsev k^{3/2} spectrum develops" in the linear phase (arXiv abstract; flag F5). | Kazantsev slope metric (these:868). Published thresholds for tier 2 (these:908). |
| P4 **NEW** | Mininni P.D., Ponty Y., Montgomery D.C., Pinton J.-F., Politano H., Pouquet A. (2005). *Dynamo Regimes with a Nonhelical Forcing.* The Astrophysical Journal 626(2), 853–863. doi:10.1086/429911 | `[CR][ABS-OA]` (HAL says "ApJ Letters"; Crossref says ApJ; flag F6) | Taylor–Green-forced dynamo followed to saturation. At moderate Re, persistent oscillations with kinetic and magnetic energies out of phase "but with no reversal of the magnetic field"; at higher Re the oscillations disappear. | Background (saturated Taylor–Green regimes for tier 2). |
| P5 | Ponty Y., Mininni P.D., Pinton J.-F., Politano H., Pouquet A. (2007). *Dynamo action at low magnetic Prandtl numbers: mean flow versus fully turbulent motions.* NJP 9, 296. doi:10.1088/1367-2630/9/8/296 | `[CR][ABS-OA]` | Kinematic thresholds with the time-averaged flow have two branches. The dynamical threshold lies on the low branch at low Re and moves toward the high branch at high Re. | Background. |
| P6 | Ponty Y., Laval J.-P., Dubrulle B., Daviaud F., Pinton J.-F. (2007). *Subcritical Dynamo Bifurcation in the Taylor-Green Flow.* PRL 99(22), 224501. doi:10.1103/PhysRevLett.99.224501; arXiv:0707.2498 | `[CR][AX][ABS-OA]` | The Taylor–Green dynamo bifurcation is subcritical, with hysteresis linked to hydrodynamic changes induced by the Lorentz force. | Bistability and conditioning on the branch (these:784). Tier 2 (these:908, these:1048). |
| P7 | Ponty Y. *et al.* (10 authors) (2008). *Linear and non-linear features of the Taylor–Green dynamo.* Comptes Rendus Physique 9(7), 749–756. doi:10.1016/j.crhy.2008.07.007 | `[CR][ABS-OA]` | Review of the Taylor–Green dynamo, "a model flow sharing many properties with the von Kármán flow": turbulence, scale-to-scale transfer, neutral-mode structure, bifurcation, saturation. | Background (chSOA1). |
| P8 | Homann H., Ponty Y., Krstulovic G., Grauer R. (2014). *Structures and Lagrangian statistics of the Taylor–Green dynamo.* NJP 16, 075014. doi:10.1088/1367-2630/16/7/075014 | `[CR][ABS-OA]` | Magnetic-field PDFs go from strongly non-Gaussian (kinematic) to quasi-Gaussian (saturated), and their flatness delimits the three regimes. | Flatness as a regime-sensitive metric for generated fields (proposal of this note). |

**Line 3: intermittency, rare events and subcritical branches.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| P9 | Alexakis A., Ponty Y. (2008). *Effect of the Lorentz force on on-off dynamo intermittency.* PRE 77(5), 056308. doi:10.1103/PhysRevE.77.056308; arXiv:0710.0063 | `[CR][AX][ABS-OA]` | Near the ABC-flow threshold, the Lorentz force reduces fluctuations and lengthens the "on" phases. Their durations follow a power law at large Re, while at small Re the system becomes laminar periodic. | Tier 2, ABC flow (these:908). Direction B (enc:261). |
| P10 | Ponty Y., Plunian F. (2011). *Transition from Large-Scale to Small-Scale Dynamo.* PRL 106(15), 154502. doi:10.1103/PhysRevLett.106.154502; arXiv:2004.11028 | `[CR][AX][ABS-OA]` | With Roberts-type helical forcing, onset is controlled by long time scales (as in Karlsruhe). Beyond onset the generalised α effect scales as O(Rm⁻¹), indicating a takeover by small-scale dynamo action. | Parametric regime change, direction F (enc:309). |
| P11 | Mannix P.M., Ponty Y., Marcotte F. (2022). *Systematic Route to Subcritical Dynamo Branches.* PRL 129(2), 024502. doi:10.1103/PhysRevLett.129.024502; arXiv:2112.11376 | `[CR][AX][ABS-OA]` | Nonlinear optimisation of a finite-amplitude disturbance identifies subcritical dynamo branches and their critical perturbations without prior knowledge of the amplification mechanism. | Bistability (these:784). |
| P12 | Ponty Y., Politano H., Pouquet A. (2025). *Intermittency assessed through a model of kurtosis–skewness relation in MHD in fast dynamo regimes.* Journal of Plasma Physics 91(2), E69. doi:10.1017/S0022377825000169 | `[CR][ABS-OA]` | K(S) relations for velocity, magnetic field and their dissipations in Taylor–Green and ABC MHD DNS run "for up to 3.14 × 10⁵ turn-over times". | Kurtosis–skewness metric (these:871). |
| P13 | Pouquet A., Marino R., Politano H., Ponty Y., Rosenberg D. (2025). *Intermittency in fluid and magnetohydrodynamics (MHD) turbulence analyzed through the prism of moment scaling predictions of multifractal models.* Nonlinear Processes in Geophysics 32(3), 243–259. doi:10.5194/npg-32-243-2025 | `[CR][ABS-OA]` | Kurtosis–skewness power laws are recovered with multifractal frameworks; a She–Lévêque model generalised to MHD gives a parabolic K(S) for maximal intermittency. | Background for the same metric. |

**Line 4: turbulence modelling for MHD.**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| P14 **NEW** | Baerenzung J., Politano H., Ponty Y., Pouquet A. (2008). *Spectral modeling of magnetohydrodynamic turbulent flows.* PRE 78(2), 026310. doi:10.1103/PhysRevE.78.026310 | `[CR][ABS-OA]` | An EDQNM-based dynamical spectral LES model for incompressible MHD with non-Kolmogorov spectra and eddy noise, in better agreement with DNS, "an important point for dynamo computations". | Background. |

**Line 5: the VKS geometry in a pseudo-spectral code (LATU).**

| # | Reference | Check | Contribution | Thesis builds on it |
|---|---|---|---|---|
| P15 | Kreuzahler S., Schulz D., Homann H., Ponty Y., Grauer R. (2014). *Numerical study of impeller-driven von Kármán flows via a volume penalization method.* NJP 16(10), 103001. doi:10.1088/1367-2630/16/10/103001 | `[CR]`; abstract truncated, contribution from title and `[PREV encadrants.md:287]` | Impeller-driven von Kármán flows simulated by volume penalisation. | VKS geometry in a periodic box (enc:209). |
| P16 | Kreuzahler S., Ponty Y., Plihon N., Homann H., Grauer R. (2017). *Dynamo Enhancement and Mode Selection Triggered by High Magnetic Permeability.* PRL 119(23), 234501. doi:10.1103/PhysRevLett.119.234501; arXiv:1706.00260 | `[CR][AX][ABS-OA][PDF arXiv v4]` | Penalised impellers with permeability jumps reproduce VKS observations: a time-averaged axisymmetric dynamo mode is self-generated above a permeability threshold. Fourier pseudo-spectral code, periodic (3π)³ box with 384³ points (re-read today). This is the "LATU" solver of Bousquet *et al.* 2026, whose ref. [22] is this paper `[PDF]`. | Size estimate of tier-3 snapshots (these:933). Tier 3 (these:929). Visit to OCA (these:1046). |
| P17 | M1: Bousquet *et al.* (2026) | §1.3 | | §1.3 |

**Other items.**
- Ponty Y. (2008), *Course 6: Numerical modeling of liquid metal dynamo experiments*, Les Houches *Dynamos*,
  pp. 359–382, doi:10.1016/S0924-8099(08)80010-8 `[CR]` (content not read).
- Courvoisier, Gilbert, Ponty (2005), GAFD, cat's-eye dynamos, doi:10.1080/03091920500334159 `[HAL]`.
- Gilbert, Ponty, Zheligovsky (2010), GAFD, doi:10.1080/03091929.2010.513332 `[HAL]`.
- Gibbon *et al.* (2016), PRE 93, 043104 `[HAL]`.
- Marcotte F., Ponty Y. (2026), *On the edge of subcritical baroclinic instability in a local model of accretion
  disc*, hal-05751296, preprint `[HAL; not read]`.

**Résumé (FR).** Yannick Ponty est directeur de recherche CNRS au laboratoire Lagrange (OCA, Nice). Il travaille sur la dynamo turbulente par simulation numérique haute performance. Après des travaux de dynamo cinématique (JFM 2001), il a publié une série de référence sur les dynamos à faible nombre de Prandtl magnétique dans l'écoulement de Taylor–Green, proxy de l'écoulement de von Kármán :
- induction à bas Pm (PRL 2004) ;
- dynamos de Pm = 1 à 10⁻², avec un seuil qui monte puis sature (PRL 2005) ;
- régimes oscillants sans inversion (ApJ 2005) ;
- bifurcation sous-critique avec hystérésis (PRL 2007) ;
- statistiques lagrangiennes (NJP 2014).

Il a aussi étudié l'intermittence on-off près du seuil avec l'écoulement ABC (PRE 2008), la transition de la dynamo grande échelle à la dynamo petite échelle (PRL 2011), la recherche systématique de branches sous-critiques par optimisation non linéaire (PRL 2022) et les relations kurtosis–asymétrie sur des simulations très longues (JPP 2025). Il a co-encadré la thèse qui a introduit la pénalisation des turbines de VKS dans un code pseudo-spectral (NJP 2014, PRL 2017) : c'est le solveur LATU de l'article MilaDy sur les inversions (PRFluids 2026), dont il est co-auteur. Aucune publication en apprentissage automatique n'a été trouvée à son nom. Pour la thèse, ses travaux fournissent les bancs d'essai périodiques (Taylor–Green, ABC), les seuils publiés, les cas de bistabilité et des métriques statistiques d'ordre élevé.

---

## 6. Map: which part of the PhD builds on whom

| PhD component (site) | Supervisor-side work it builds on |
|---|---|
| Hard constraints in a bounded cylinder: vacuum matching, μr jumps, FE potentials (these:256-348) | Guermond, Nore *et al.* 2007, 2009, 2011 (N5–N7); Nore *et al.* 2018 (N16); Giesecke *et al.* 2012 (N12) |
| Tier-2 periodic dynamos, thresholds, bistability (these:784, these:868-871, these:908) | Nore *et al.* 1997 (N1); Ponty *et al.* 2005, 2007 (P3, P6); Alexakis & Ponty 2008 (P9); Mannix *et al.* 2022 (P11); Ponty *et al.* 2025 (P12) |
| Tier-3 VKS data, baselines, metrics (these:929-937) | Bousquet *et al.* 2026 (M1); Nore *et al.* 2016, 2018 (N15, N16); Creff *et al.* 2024 (N17); Kreuzahler *et al.* 2017 (P16); Bousquet, Nore, Lucor 2025 (M4) |
| Reduced model from generated snapshots (these:135, these:828) | Bousquet *et al.* 2026, DQVU (M1); Bousquet & Nore 2026 poster (M8) |
| Tier-4 DRESDYN (these:943-947) | Botez *et al.* 2026 (M2); Nore *et al.* 2011 (N19); Cappanera *et al.* 2016 (N23); Stefani *et al.* 2015 (N21) |
| Generative prior in data assimilation (these:136, these:843) | GLA 2022 (C6); TorchDA 2025 (C13); Zhuang *et al.* 2025 (C20); Bocquet, Finn, Cheng 2026 (C31); latent non-Gaussian DA 2026 (C12, proposal) |
| Protocol and probabilistic evaluation (enc:138, enc:309) | Yu *et al.* 2026 (C21); Jaber *et al.* 2025 (L14) |
| Latent space and architecture choices (enc:249) | Bousquet, Nore, Lucor 2025 (M4); polynomial AEs 2026 (M7); MSPCNN 2024 (C15); unstructured-grid review 2025 (C17) |
| Hard-vs-soft constraint trade-off (enc:297) | Lucor, Agrawal, Sergent 2022 (L9); Xue *et al.* 2026 (C27); Cai *et al.* 2024 (L10) |

**What none of the four has published** (searches 2026-11-06 and 2026-11-08, HAL, Crossref, arXiv, personal pages):
- a generative model (diffusion or flow matching) trained on dynamo or MHD data;
- a machine-learning paper by Y. Ponty;
- a dynamo paper by S. Cheng;
- a dynamo-theory paper by D. Lucor (only von Kármán and VKS co-authorships with C. Nore).

This matches `en/encadrants/index.qmd:513-519` (gap 1) and `:237`. These are negative statements: they hold
"to our knowledge".

---

## 7. Flags and unverified points

| # | Item | Status |
|---|---|---|
| F1 | Tensor-Var title: Cheng's page (today) still says "…in Tensor Product Feature Space"; PMLR says "Tensor-Var: Efficient Four-Dimensional Variational Data Assimilation" `[PREV encadrants.md:154]` | Use the PMLR title |
| F2 | PCCP 2023: Cheng's page says "Predicting drop coalescence in microfluidic device…"; Crossref says "**Analyzing** drop coalescence in microfluidic **devices**…" `[CRs]` | Use Crossref |
| F3 | Year mismatches between Cheng's page and Crossref: TorchDA 2024 vs 2025 (issue Jan 2025); VIVID 2023 vs 2024; DSOVT 2025 vs 2024 (issue Dec 2024); SERRA "Error covariance tuning" 2020 (online) vs 2021 (issue) | Cite the issue year, online year in brackets |
| F4 | Jaber *et al.* 2025: Crossref "…with marginal coverage guarantees"; HAL "…with Coverage Guarantees" | Use Crossref |
| F5 | Ponty *et al.* 2005: the Kazantsev k^{3/2} sentence is in the arXiv abstract (physics/0410046v1); the PRL abstract via OpenAlex instead says unstable modes "move to smaller scales" | Attribute to the arXiv version, or check the PRL full text |
| F6 | Mininni *et al.* 2005: HAL "ApJ Letters"; Crossref "The Astrophysical Journal 626(2), 853–863" | Use Crossref |
| F7 | Bousquet, Nore, Lucor 2025 (CPC) is **not** MilaDy-funded (Crossref funder: GENCI; no ANR in HAL). It predates the project and is its starting point | Do not call it a "MilaDy paper" on screen; say "consortium paper" |
| F8 | Bousquet *et al.* 2026 Research Square preprint and the RNL 2026 poster: not peer-reviewed; no MilaDy funding stated | Label as preprint or poster |
| F9 | RNL 2026 abstract: "dynamo threshold - inversely proportional to mu". Conference-abstract statement; compare with Giesecke *et al.* 2012's μr^(−1/2) scaling of Rm_c(μr) − Rm_c(∞), a different quantity | Do not combine the two claims |
| F10 | Botez, Bousquet, Nore, *JCP* "In press, 559": not in Crossref or HAL (re-searched today) | UNVERIFIED |
| F11 | Botez *et al.* 2026: no Poincaré numbers or Rm_c values extracted (APS PDF not opened) | Use only the abstract's wording |
| F12 | Bousquet *et al.* 2024: "Re>104" in metadata, read as 10⁴ | Exponent not seen typeset |
| F13 | Lucor *et al.* 2022 JCP: Ra = 2·10⁹ and the error figures are from the arXiv preprint abstract only | UNVERIFIED in the JCP version |
| F14 | OCA MilaDy postdoc: CV says "Hiroshi Hiiro"; HAL (hal-05796131, MilaDy-funded) has "Hiroshi Horii" at OCA | Probably Horii; UNVERIFIED |
| F15 | LISN MilaDy postdoc: recruit unknown | UNVERIFIED |
| F16 | C. Nore's rank "Pr." comes from the offers only; her institutional page was not opened | Say "C. Nore (LISN)" |
| F17 | SFEMaNS authorship: Nore's own seminar abstract says "We have been developing … SFEMaNS since 2002"; the code headers were not seen | Say "SFEMaNS, developed by J.-L. Guermond, C. Nore and colleagues" |
| F18 | HAL lists "Sibo Cheng" on the CEPC Technical Design Report (particle physics, 2025) | Almost certainly a homonym; **not attributed** |
| F19 | Gong *et al.* 2022, ViTAE-SL 2025, Les Houches 2008, Kreuzahler 2014, Sundar 2024/2025: abstracts not read today | Contribution from title or PREV only |
| F20 | ICLR 2025 poster and ICLR 2026 oral statuses: OpenReview checked 2026-11-06, not today; "top 1.2%" only from Cheng's page | PREV |
| F21 | Project dates and amount: ANR (Jan 2026, 48 months, €560,612) vs Ponty CV (Feb 2026–2030, 550k€) vs Cheng home page (2025–2029) | Use the ANR values |

---

## 8. Film-ready one-liners for `chSOA2` (names in text only, no opinions; each sourced above)

1. "S. Cheng: latent data assimilation (2022) and the TorchDA library (2025), named in the MilaDy abstract." (C6, C13, §1.1)
2. "S. Cheng and co-authors: diffusion models for field reconstruction (2025) and probabilistic forecasting (2026)." (C20, C21)
3. "D. Lucor: polynomial chaos for uncertainty in flows (2002–2007); PINNs and invariance-preserving networks for turbulence (2022–2024)." (L1–L5, L9, L10)
4. "D. Lucor and C. Nore: autoencoders read through POD on forced flows (2025)." (M4)
5. "C. Nore: SFEMaNS simulations of the VKS dynamo with ferromagnetic impellers (2016, 2018) and of precession dynamos for DRESDYN (2011, 2016, 2026)." (N15, N16, N19, N23, M2)
6. "Y. Ponty: Taylor–Green dynamos at low magnetic Prandtl number (2005), a subcritical dynamo (2007), on-off intermittency (2008)." (P3, P6, P9)
7. "Y. Ponty and co-authors: the LATU pseudo-spectral solver with penalised impellers (2014, 2017)." (P15, P16)
8. "MilaDy's first paper: the reversal mechanism of VKS and the DQVU reduced model, from two solvers (2026)." (M1)
9. "No generative model trained on dynamo simulations was found: that is the gap the thesis targets." (§6, enc:513)

---

## 9. Sources opened on 2026-11-08

- ANR: https://anr.fr/Projet-ANR-25-CE51-0077
- S. Cheng: https://scheng2024.github.io/ ; /research/ ; /publications/ (updated 2026-10-20) ; /opportunities/ ; /cv/ ;
  https://scheng2024.github.io/stage_milady_2027.pdf
- D. Lucor: https://perso.lisn.upsaclay.fr/lucor/ ; /people.html ; /publications.html ; /opportunities.html ;
  https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf
- 2026 internship: https://stages.phys.ens.psl.eu/OffresPDF/Offre-30818.pdf
- Y. Ponty CV: https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf
- C. Nore: https://www.ladhyx.polytechnique.fr/media/evenement/180118_CarolineNore.pdf ;
  https://rnl2026.sciencesconf.org/712616 (and /document)
- SFEMaNS: https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html
- Full texts: https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf ; https://arxiv.org/pdf/1706.00260v4
- APIs: api.crossref.org (works by DOI and by bibliographic query, including funder metadata);
  export.arxiv.org (id_list, author search); api.archives-ouvertes.fr (anrProjectReference_s, authFullName_s,
  halId_s, doiId_s); api.openalex.org (abstracts).
- Web search (data only): "Caroline Nore LISN professeur Université Paris-Saclay dynamo SFEMaNS".
