# Supervisors and the ANR MilaDy project: fact base

## Verification summary

*Independent cross-check carried out on 6 November 2026. Every DOI (63) was resolved in the Crossref API, every arXiv identifier (31) in the arXiv API, every cited HAL record in the HAL API. The ANR page, the pages of Cheng and Lucor, the PDFs of the offers (2027 internship, 2026 internship, postdoc, Nore–Lucor M2), the two CVs of Ponty, the full text of Bousquet et al. 2026 and the arXiv text of Kreuzahler et al. 2017 were opened. The APS abstracts missing from Crossref were read via OpenAlex.*

- **Verified: about 125 entries** (135 “[verified]” markers, 5 of them in the final section and 4 on additions). Authors, years, journals, volumes, pages and DOIs agree with Crossref for the 63 DOIs. The figures of Bousquet 2026 (Re = 1594, Rm = 531, asymmetry 0.058, μ_r = 16, 2000 snapshots), the definitions of Re and Rm and the regression constraints (A_uvv + A_vvu = 0; X²·f(X,p) = 0) were re-read in the article.
- **Corrected: 4 entries.**
- **Unconfirmed: 12 points**, grouped in the final section “9. Unconfirmed”.
- **Additions: 5** (Bousquet–Nore–Lucor 2026 preprint, Quattromini thesis co-supervised by Nore, COMET team, doctoral student Qiyao Zhou, content of Cappanera 2016).

**Important corrections**
1. Botez et al., PRFluids 11, 083701: “2026-10-07” → **published on 14 August 2026** (received on 27 April 2026). The date of 7 October is that of the HAL record.
2. Tensor-Var (ICML 2025): the published title is **“Tensor-Var: Efficient Four-Dimensional Variational Data Assimilation”** (PMLR 267:70649–70679), and not “… in Tensor Product Feature Space” (title on Cheng's page). The 8 authors are now listed.
3. Jaber et al. 2025 (JMLMC): title “with (marginal) coverage guarantees” → “with marginal coverage guarantees”.
4. MilaDy postdoc on Lucor's page: the announcement “Starting in April/May 2026” is **no longer displayed**. It sits in a commented-out block of the source code, which suggests that the offer is closed. The PDF of the offer is still online.

**Useful additions for the writers**: Nore co-supervised a thesis on GNNs and data assimilation (Quattromini, 2024), and the §6 matrix has been updated accordingly. The Research Square preprint of June 2026 (POD-initialised polynomial autoencoders) extends CPC 2025. The OCA postdoc is very probably named **Hiroshi Horii**: HAL attaches him to the OCA, and “Hiiro” would be a typo in the CV. No machine-learning publication by Ponty was found, which is confirmed.

---

*Collection: 6 November 2026. All cited URLs were opened during the collection (HTML pages, PDFs, HAL API `api.archives-ouvertes.fr`, Crossref API `api.crossref.org`, arXiv API `export.arxiv.org`). The `hal.science` and `lisn.upsaclay.fr` pages are protected by an anti-bot system: their records were therefore read via the HAL API. The APS pages (journals.aps.org) returned a 403 error. This document is a fact base for the writers, not a final text.*

---

## 0. Key points

- **MilaDy** = « Modélisation par apprentissage automatique des dynamos turbulentes » [English: Machine learning modelling of turbulent dynamos] / “Machine learning modelling for turbulent Dynamos”, **ANR-25-CE51-0077**, committee CE51 (« Sciences de l'ingénierie et des procédés » [English: Engineering and process sciences], AAPG 2025). Coordinator: **Caroline Nore (LISN)**. Partners: LISN, Lagrange (OCA, Nice), CEREA (ENPC). ANR funding: **560 612 €**. Start **January 2026**, duration **48 months**. Source: https://anr.fr/Projet-ANR-25-CE51-0077 [verified]
- The two official objectives: (i) study **magnetic-field reversals** and “explosive” (burst) dynamos, with ROMs able to identify the precursor / reversal / recovery phases; (ii) **optimise DRESDYN** (precessing cylinder, HZDR) with **parametric ROMs** (precession/rotation frequency ratio). The summary cites **TorchDA**, S. Cheng's software. [verified]
- The 2027 internship follows a 2026 internship of the same consortium, “Physics-aware Representation Learning for Turbulent Dynamo Data” (compression, latent regression, contrastive learning). The 2027 internship moves to **generative** modelling: conditional diffusion and flow matching, physical constraints. The thesis would be **co-supervised by S. Cheng and D. Lucor** (https://scheng2024.github.io/opportunities/). [verified]
- First publications attached to MilaDy: **Bousquet, Ponty, Botez, Plihon, Nore, PRFluids 11, 063703 (2026)**, on reversals in VKS (POD on 2000 snapshots, **DQVU** reduced Galerkin model identified by PySINDy under constraints), and **Botez, Giesecke, Nore, Cappanera, Stefani, PRFluids 11, 083701 (2026)**, on the kinematic precession dynamo for DRESDYN. [verified]
- **Data**: SFEMaNS (Guermond and Nore; hybrid method with azimuthal Fourier + meridian finite elements, permeability jumps, penalisation, entropy viscosity) and the second solver “LATU” (pseudo-spectral Fourier + penalisation, Kreuzahler, Ponty et al. 2017). The data of Bousquet et al. 2026 are **not public** (“available from the authors upon reasonable request”). [verified]
- Links between supervisors: Cheng was a doctoral student of Lucor (2017–2020, with EDF R&D). Lucor and Nore co-supervise R. Bousquet (VAE/POD). Nore and Ponty publish together on VKS reversals. Cheng and Lucor were guest editors of the same special issue of *Computer Physics Communications*, “Advances in Physics-Aware Machine Learning”. [verified]

---

## 1. The ANR project MilaDy

### 1.1 Identity sheet

| Field | Value | Source |
|---|---|---|
| Title FR | Modélisation par apprentissage automatique des dynamos turbulentes – MilaDy [English: Machine learning modelling of turbulent dynamos – MilaDy] [verified] | https://anr.fr/Projet-ANR-25-CE51-0077 |
| Title EN | Machine learning modelling for turbulent Dynamos – MilaDy [verified] | ANR EN page: https://anr.fr/en/funded-projects-and-impact/funded-projects/project/funded/project/b2d9d3668f92a3b9fbbf7866072501ef-8f0bea4141/?tx_anrprojects_funded%5Bcontroller%5D=Funded&cHash=f7b87490b7ffc2a2a9c7dc94387c163f |
| Reference | ANR-25-CE51-0077 [verified] | ANR page; Cheng's “Research” page (https://scheng2024.github.io/research/) |
| Instrument | ANR PRC (projet de recherche collaborative [English: collaborative research project]) [verified] | Cheng's home page (https://scheng2024.github.io/) shows “MILADY — ANR PRC (2025–2029)” |
| Committee | CE51 – Sciences de l'ingénierie et des procédés [English: Engineering and process sciences], 2025 [verified] | ANR page |
| Coordination | Caroline Nore (LISN) [verified] | ANR page |
| Partners | LISN (Laboratoire Interdisciplinaire des Sciences du Numérique); LAGRANGE, Observatoire de la Côte d'Azur, Nice; CEREA, École nationale des ponts et chaussées [verified] | ANR page |
| Role of Cheng | “Co-Investigator” [verified] | https://scheng2024.github.io/research/ |
| ANR funding | 560 612 € [verified] | ANR page |
| Start / duration | January 2026, 48 months [verified] | ANR page |
| Variant of the reference | “Grant No. ANR-25-CE51-0077-02” (acknowledgements of Bousquet et al. 2026) [verified; same number in the Crossref “funder” metadata of Bousquet 2026 and of Botez 2026] | https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf |

**Official summary (FR, verbatim, ANR page):** [verified: text identical, word for word, to the ANR page]
> La magnétohydrodynamique (MHD) étudie les interactions entre les fluides électriquement conducteurs et les champs magnétiques, essentielles pour des applications industrielles et la compréhension de phénomènes comme l'effet dynamo (DyE). Ce dernier implique l'amplification de bruits magnétiques dans des fluides turbulents, comme dans les étoiles ou les noyaux planétaires, ce qui le rend rare et complexe à reproduire. Seules trois expériences, dont celle de Cadarache en France, ont réussi à obtenir un DyE avec du sodium liquide. L'expérience DRESDYN en cours en Allemagne vise à reproduire le DyE à l'aide d'un cylindre en précession.
> La simulation du DyE est difficile en raison du couplage non linéaire entre les équations de Navier-Stokes et l'équation d'induction, rendant les simulations numériques directes (DNS) très coûteuses en temps calcul. Les modèles réduits (ROM) sont utiles pour simplifier ces simulations, tandis que l'apprentissage automatique (ML) présente un potentiel pour traiter les dynamiques à haute dimension, bien que la capture des événements rares reste un défi. L'assimilation de données (DA) avec ML devient plus accessible, notamment grâce à la plateforme TorchDA.
> MilaDy vise à faire progresser la recherche en MHD avec deux objectifs principaux : (i) Étudier les inversions de champ magnétique et les phénomènes de dynamo « explosive » grâce à des méthodes basées sur les données pour identifier les caractéristiques clés et développer des ROMs qui reproduisent les dynamiques observées. Le projet étudie si le ML peut améliorer la compréhension des inversions magnétiques et créer des modèles plus rapides qui identifient les phases comme le précurseur, l'inversion et le rebond. (ii) Optimiser le dispositif DRESDYN avec des ROMs paramétriques pour explorer les conditions du DyE, telles que les ratios de fréquences précession/rotation. Les ROMs permettent une exploration efficace des paramètres, aidant les expérimentateurs à gérer ces systèmes complexes.

> [English translation, paragraph by paragraph: Magnetohydrodynamics (MHD) studies the interactions between electrically conducting fluids and magnetic fields, which are essential for industrial applications and for understanding phenomena such as the dynamo effect (DyE). The latter involves the amplification of magnetic noise in turbulent fluids, as in stars or planetary cores, which makes it rare and complex to reproduce. Only three experiments, including the one at Cadarache in France, have succeeded in obtaining a DyE with liquid sodium. The DRESDYN experiment under way in Germany aims to reproduce the DyE using a precessing cylinder.
> Simulating the DyE is difficult because of the nonlinear coupling between the Navier–Stokes equations and the induction equation, which makes direct numerical simulations (DNS) very costly in computing time. Reduced-order models (ROMs) are useful for simplifying these simulations, while machine learning (ML) has potential for handling high-dimensional dynamics, although capturing rare events remains a challenge. Data assimilation (DA) with ML is becoming more accessible, notably thanks to the TorchDA platform.
> MilaDy aims to advance MHD research with two main objectives: (i) To study magnetic-field reversals and “explosive” dynamo phenomena using data-based methods to identify key features and develop ROMs that reproduce the observed dynamics. The project investigates whether ML can improve the understanding of magnetic reversals and create faster models that identify phases such as the precursor, the reversal and the recovery. (ii) To optimise the DRESDYN device with parametric ROMs to explore DyE conditions, such as precession/rotation frequency ratios. ROMs allow efficient exploration of the parameters, helping experimenters manage these complex systems.]

**Key wordings of the EN summary (verbatim)**: “burst dynamo phenomena”; “faster surrogate models that distinguish phases like precursor, reversal, and recovery”; “precession-to-spin frequency ratios”; “thanks in particular to the TorchDA framework”. [verified]

**Description of MilaDy by Cheng** (https://scheng2024.github.io/research/) reads: “MilaDy combines machine learning and numerical simulation to study turbulent magnetohydrodynamic dynamos […] investigates magnetic-field reversals, rare dynamical events and the influence of physical parameters. At CEREA/ENPC, our research focuses on physics-aware representation learning and reduced-order modelling of three-dimensional velocity and magnetic fields, connecting learned representations to data assimilation.” [verified]

**Description in Ponty's CV (2026)** (https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf) reads: « 2026 (février) – 2030 Contrat ANR : MiLaDy ; Machine Learning modeling for turbulent Dynamos coordinatrice C. Nore LISN (Saclay) /Y. Ponty (OCA)/ S. Cheng (CEREA, ENPC). Duration: 48 months (550k€). » The same CV also mentions: « février 2026 - … Encadrement de Hiroshi Hiiro Postdoc ANR Projet MiLady ». [English of the French wording only, dates omitted: “(February) – … ANR contract: MiLaDy; … coordinator …”; “February … – … Supervision of Hiroshi Hiiro, ANR postdoc, MiLady project”.] [verified: exact quotations from the CV]

### 1.2 Offers related to the project

**a) 2027 M2 internship (the target offer)** [verified: PDF opened on 6/11/2026; Lucor's Opportunities page points to a local copy pdf/stage_milady_2027.pdf], https://scheng2024.github.io/stage_milady_2027.pdf (also at https://perso.lisn.upsaclay.fr/lucor/opportunities.html) — key points:
- Title: “Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems (with potential PhD position)”.
- The context explicitly mentions “abrupt reversals of the magnetic field polarity” and “large 3D datasets that are difficult to store, interpret, and reuse for modelling and data assimilation”.
- Targeted constraints: “energy balance and divergence-free conditions”. Parameters: “Reynolds number, magnetic Reynolds number, material properties…”. Outputs: “3D fields that can serve as input for reduced-order models or data assimilation frameworks developed elsewhere in the project”.
- Methods: “diffusion or flow matching”. Constraints imposed “through model design, training losses, or sampling procedures”. Metrics: “energy spectra, helicity, divergence control, and topology preservation”.
- Deliverables: comparative study, code integrated into the “MilaDy project toolbox”. A funded thesis is possible.
- Practical details: 5–6 months starting in spring 2027, ENPC Champs-sur-Marne, 1–2 days of remote work per week. Applications to sibo.cheng@enpc.fr and didier.lucor@cnrs.fr.
- Cheng's “Opportunities” page: “The PhD student will be co-supervised by Sibo Cheng and Didier Lucor”, CEREA (ENPC) – LISN collaboration (https://scheng2024.github.io/opportunities/).

**b) Previous M2 internship (spring 2026)** [verified: PDF opened], “Physics-aware Representation Learning for Turbulent Dynamo Data (leading to a potential PhD position within the project)”, https://stages.phys.ens.psl.eu/OffresPDF/Offre-30818.pdf — key points:
- Data: “3D simulation outputs from dynamo configurations used in two experiments in Cadarache (France) and in Dresden (Germany)”.
- Methods: convolutional or attention-based encoder–decoder architectures; “latent-space regression so that the reduced representation correlates with physical parameters”; “contrastive learning”; same physical metrics (spectra, helicity, divergence, topology).
- Listed parameters: “Reynolds number, magnetic Reynolds number, material properties, precession rate, or geometry”.
- References: Fukami & Taira 2023 (Nature Communications 14, 6480, DOI 10.1038/s41467-023-42213-6 [verified]); Brandstetter, Worrall, Welling 2022 (arXiv:2202.03376); Bousquet, Nore, Lucor 2025 (CPC).
- Contacts: Cheng, Lucor, Nore, Ponty.

**c) 24-month LISN postdoc** [verified: PDF opened, it was not blocked], https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf — key points:
- Title: “Turbulent Dynamos Reduced-Order Modeling via Machine learning”. Contacts: “Pr. UPS C. Nore” and “DR CNRS D. Lucor”.
- Objectives: interpretable pROMs for reversals and bursts; optimisation of DRESDYN (“precession, rotation, geometry”).
- Methods: linear spectral approaches combined with (v)AEs; physics-informed (v)AEs through latent regression on the parameters, temporal or parametric contrastive learning, physical invariants; constrained reduced dynamics in the latent space (LSTM for small datasets, transformers for large ones).
- Context: dynamo “rare in liquid metals, occurs only in 3D turbulent regimes at low magnetic Prandtl number (Pm)”; DNS “typically restricted to Pm~1 regimes”.
- Salary: 3 131.32 € to 3 569.85 € gross per month. Position subject to the **PPST** (protection of scientific and technical potential, prior MESR authorisation).
- References: Bousquet, Nore, Lucor 2025; Bousquet et al. 2024; Yang & Schmid 2025, JFM 1011:A30 (reversals in 2D convection, complex networks). DOI 10.1017/jfm.2025.371 [verified]
- Lucor's page: “Starting in April/May 2026 […] funded by the MILADY ANR in collaboration with colleagues from the Lagrange lab (Nice) and CEREA lab (ENPC, EDF R&D)” (https://perso.lisn.upsaclay.fr/lucor/opportunities.html). [corrected: presented as a displayed announcement → this paragraph is now in a commented-out block (<!-- … -->) of the source code of opportunities.html and is no longer displayed, which suggests that the offer is closed]
- Public announcement of the postdoc by Sibo Cheng on the ml-news list, 24 January 2026: https://groups.google.com/g/ml-news/c/lr8uwyCAl_M [verified: message from Sibo Cheng, 24 Jan. 2026, postdoc PDF attached]

**d) Earlier work: Nore–Lucor M2 internship “Machine learning analysis of local energy transfers in turbulence”** (undated in the PDF; listed on Lucor's page with the spring 2022 offers), https://perso.lisn.upsaclay.fr/lucor/pdf/M2Stage_Nore_Lucor.pdf — analysis of 3D SFEMaNS data from the CEA-SPEC von Kármán experiment, unsupervised clustering, detection of rare and extreme events. [verified: PDF opened; it speaks of “our massively parallel research code SFEMaNS”; the corresponding entry is in a commented-out block of Lucor's page]

### 1.3 Publications already attached to MilaDy in HAL (field `anrProjectReference_s`)

Query: https://api.archives-ouvertes.fr/search/?q=anrProjectReference_s:%22ANR-25-CE51-0077%22 (3 results) [verified: 3 results on 6/11/2026]:
1. Bousquet, Ponty, Botez, Plihon, Nore, *Magnetic field reversals in numerical simulations of the von Kármán sodium experiment*, PRFluids 11, 063703 (2026), DOI 10.1103/9tx2-1m13 (hal-05668081). Details in §4. [verified]
2. Botez, Giesecke, Nore, Cappanera, Stefani, *Impact of boundary conditions on onset and symmetry of precession-driven dynamos*, PRFluids 11, 083701 (2026), DOI 10.1103/rx1h-5zxp (hal-05782992). Details in §4. [verified]
3. J. Barré, H. Horii, *Large deviations, gradient flows and fluctuating hydrodynamics for fractional diffusion* (hal-05796131, 2026), which also acknowledges two other ANR projects. Weak thematic link. HAL attaches H. Horii to the Observatoire de la Côte d'Azur and to the Université Côte d'Azur. [verified]

No MilaDy publication by Cheng or Lucor on dynamos was found at this date (arXiv search `au:Cheng_Sibo`, HAL search). [verified: arXiv `au:Cheng_Sibo` or `au:Lucor` with `abs:dynamo` or `abs:magnetohydrodynamic` → 0 results on 6/11/2026]

---

## 2. Sibo Cheng (ENPC, CEREA)

### 2.1 Background and themes
Sources: https://scheng2024.github.io/ , /cv/ , /research/ , /people/
- **Position**: “Tenure-Track Junior Professor (Chaire de Professeur Junior) at ENPC, Institut Polytechnique de Paris”, at CEREA, since 2024. Also “Honorary Research Fellow” at Imperial College London. [verified]
- **Before**: Research Associate at the Data Science Institute of Imperial College London (2020–2024), with Rossella Arcucci. [verified]
- **Doctorate**: Université Paris-Saclay, 2020, “under the supervision of Didier Lucor, working on error covariance specification in data assimilation in collaboration with EDF R&D”. According to Lucor's page: arrived in 12/2017, doctor in 11/2020; graduate of the École Centrale de Nantes and of UCLouvain (https://perso.lisn.upsaclay.fr/lucor/people.html). [verified]
- **Declared themes**: data assimilation and inverse problems; reduced and latent-space modelling; scientific ML (neural networks coupled to physical models, differentiable simulation, neural operators); “Generative modelling: probabilistic forecasting and field reconstruction using conditional generative models”; applications to wildfires, air pollution and geophysical systems. [verified]
- **Projects**: Hi! PARIS Fellowship 2026–2030 (PI; “Differentiable Digital Twin for Wildfire Prediction & Control”); **OFML**, ANR JCJC **ANR-25-CE56-0198**, 2025–2029 (PI; wildfires and firefighting); **MilaDy** (Co-I); **QWERTY**, PEPR FORESTT ANR-25-PEFO-0008 (Co-I). [verified]
- **Software**: **TorchDA** (data assimilation with deep networks, CPC); **PyTorchFire** (differentiable cellular automaton on GPU, EMS 2025). [verified: Environmental Modelling & Software 188, 106401 (2025)]
- **Editorial responsibilities**: “Executive Guest Editor, Computer Physics Communications, special issue “Advances in Physics-Aware Machine Learning”” (2024–2025); head of the “Data Assimilation” theme, SAMA group of the IPSL (2025–2027). [verified]
- **Doctoral students related to generative modelling**: Zhiwei Zhang (2026–, “Multi-fidelity Air Pollution Field Reconstruction via Generative AI and Data Assimilation”); Wenbo Yu (2025–, “Self-Supervised Representation Learning for Data Assimilation”); Lisa Achard (2025–, main supervisors Lucor and Zeyu Fu, “Generative Multimodal Fusion and Uncertainty Quantification…”). [verified] Addition: Qiyao Zhou (2025–, Université Paris-Saclay, main supervisor Pierre Joli, “Reduced-order and inverse modeling for fluid dynamics”), first author of the arXiv:2608.11435 preprint cited below. [verified, addition]
- **Declared main collaborators**: M. Bocquet, R. Arcucci, D. Lucor, N. Chen, L. Xu, X. Zhu. [verified]

### 2.2 Publications relevant to the offer (verified)

The references come from the Publications page (https://scheng2024.github.io/publications/), verified via Crossref and arXiv (DOIs given). “*” marks the corresponding author, as on Cheng's page.

1. **Cheng S., Quilodrán-Casas C., Ouala S., Farchi A., Liu C., Tandeo P., Fablet R., Lucor D., Iooss B., Brajard J., Xiao D., Janjic T., Ding W., Guo Y., Carrassi A., Bocquet M., Arcucci R. (2023).** *Machine Learning With Data Assimilation and Uncertainty Quantification for Dynamical Systems: A Review.* IEEE/CAA Journal of Automatica Sinica **10(6), 1361–1387**. DOI **10.1109/JAS.2023.123537**; arXiv:2303.10462. [verified]
   Contribution: review presented as “the first overview” of the ML / DA / UQ intersection (system identification, reduced surrogates, specification of error covariances, model-error correction). Co-written with Lucor.
2. **Cheng S., Chen J., Anastasiou C., Angeli P., Matar O.K., Guo Y.-K., Pain C.C., Arcucci R. (2022).** *Generalised Latent Assimilation in Heterogeneous Reduced Spaces with Machine Learning Surrogate Models.* Journal of Scientific Computing **94(1), 11**. DOI **10.1007/s10915-022-02059-4**; arXiv:2204.03497. [verified]
   Contribution: GLA performs variational assimilation in the latent space with local surrogate functions that link the encoded space and the observation space, which allows nonlinear observation operators. An upper bound on the gap between the surrogate cost function and the original cost function is given. Figure (arXiv abstract): surrogate “nearly 1000 times faster than the CFD simulation” (two-phase liquid–liquid flow).
3. **Cheng S., Prentice I.C., Huang Y., Jin Y., Guo Y.-K., Arcucci R. (2022).** *Data-driven surrogate model with latent data assimilation: Application to wildfire forecasting.* Journal of Computational Physics **464, 111302**. DOI **10.1016/j.jcp.2022.111302**. [verified]
   Contribution: reduced surrogate and latent assimilation (LA) for wildfire forecasting.
4. **Cheng S.\*, Liu C., Guo Y., Arcucci R.** *Efficient deep data assimilation with sparse observations and time-varying sensors.* Journal of Computational Physics **496, 112581**. Dated 2024 by Crossref, 2023 on Cheng's page. DOI **10.1016/j.jcp.2023.112581**; arXiv:2310.16187. [verified]
   Contribution: **VIVID** (“Voronoi-tessellation Inverse operator for VariatIonal Data assimilation”). A learned inverse operator (Voronoi + CNN) is built into the variational cost function; it handles sparse, unstructured and time-varying sensors, and is coupled to the POD.
5. **Cheng S.\*, Zhuang Y., Kahouadji L., Liu C., Chen J., Matar O.K., Arcucci R. (2024).** *Multi-domain encoder–decoder neural networks for latent data assimilation in dynamical systems.* Computer Methods in Applied Mechanics and Engineering **430, 117201**. DOI **10.1016/j.cma.2024.117201**. [verified]
   Contribution: latent assimilation across heterogeneous physical domains (multi-domain encoders and decoders).
6. **Cheng S.\*, Guo Y., Arcucci R. (2023).** *A Generative Model for Surrogates of Spatial-Temporal Wildfire Nowcasting.* IEEE Transactions on Emerging Topics in Computational Intelligence **7(5), 1420–1430**. DOI **10.1109/TETCI.2023.3298535**; arXiv:2308.02810. [verified]
   Contribution: **3D VQ-VAE** that generates new spatio-temporal wildfire sequences (Chimney fire), conditioned on vegetation and slope. The generated data are used to train a surrogate. This is a precedent for conditional generation of fields.
7. **Zhuang Y., Cheng S., Duraisamy K. (2025).** *Spatially-aware diffusion models with cross-attention for global field reconstruction with sparse observations.* Computer Methods in Applied Mechanics and Engineering **435, 117623**. DOI **10.1016/j.cma.2024.117623**; arXiv:2409.00230. [verified]
   Contribution: score-based diffusion with condition encoding (sparse observations + interpolated field) and cross-attention, arbitrary moving sensors, benchmark on steady and unsteady PDEs. Result (abstract): diffusion wins under noisy conditions, the deterministic method under noiseless conditions; ensemble sampling is used for covariance-based corrections. This is **the reference closest to the offer** on Cheng's side.
8. **Yu W., Ghosh A., Finn T.S., Arcucci R., Bocquet M., Cheng S.\* (2026).** *A probabilistic approach to wildfire spread prediction using a denoising diffusion surrogate model.* Geoscientific Model Development **19(2), 1027–1054**. DOI **10.5194/gmd-19-1027-2026** (https://gmd.copernicus.org/articles/19/1027/2026/) ; arXiv:2507.00761. [verified]
   Contribution: conditional diffusion surrogate with ensemble sampling, compared with a supervised regression of the same architecture. It does better in MSE, SSIM and FID, and on the “hit rate (HR)” score, introduced as an uncertainty-sensitive verification measure. Data: probabilistic cellular automaton (Chimney 2016, Ferguson 2018). The arXiv entry presents it as “the first denoising diffusion model for predicting wildfire spread”.
9. **Cheng S.\*, Min J., Liu C., Arcucci R.** *TorchDA: A Python package for performing data assimilation with deep learning forward and transformation functions.* Computer Physics Communications **306, 109359**. Dated 2025 by Crossref, 2024 on Cheng's page. DOI **10.1016/j.cpc.2024.109359**; arXiv:2409.00244. [verified]
   Contribution: KF, EnKF, 3D-Var and 4D-Var with deep networks as transition model and observation operator (tests on Lorenz 63 and shallow water). **Cited in the ANR summary of MilaDy.**
10. **Zhou H., Cheng S.\*, Arcucci R. (2024).** *Multi-fidelity physics constrained neural networks for dynamical systems.* Computer Methods in Applied Mechanics and Engineering **420, 116758**. DOI **10.1016/j.cma.2024.116758**; arXiv:2402.02031. [verified]
    Contribution: **MSPCNN**. A multi-fidelity autoencoder places the different fidelities in a common latent space, which makes it possible to evaluate the physical constraints at low fidelity (lower training cost). Tests on 2D Burgers and shallow water.
11. **Wang H., Zhou H., Cheng S.\*** *Dynamical system prediction from sparse observations using deep neural networks with Voronoi tessellation and physics constraint.* Computer Methods in Applied Mechanics and Engineering **432, 117339** (2025 on Cheng's page, 2024 according to Crossref). DOI **10.1016/j.cma.2024.117339**; arXiv:2409.00458. [verified]
    Contribution: **DSOVT** (Voronoi + CED-LSTM or ConvLSTM) with physical constraints in the loss, for prediction from sparse, time-varying observations (real SST, shallow water).
12. **Gong H.-L., Li H., Xiao D., Cheng S.\* (2024).** *Reactor field reconstruction from sparse and movable sensors using Voronoi tessellation-assisted convolutional neural networks.* Nuclear Science and Techniques **35(5), 43**. DOI **10.1007/s41365-024-01400-w**. [verified]
13. **Cheng S.\*, Bocquet M., Ding W., Finn T.S., et al., Arcucci R. (2025).** *Machine learning for modelling unstructured grid data in computational physics: A review.* Information Fusion **123, 103255**. DOI **10.1016/j.inffus.2025.103255**; arXiv:2502.09346. [verified]
    Interest: the SFEMaNS outputs are on an unstructured finite-element mesh in the meridian plane (see §4.1).
14. **Xue X., ten Eikelder M.F.P., Gao M., Cheng X., Yang Y., He Y., Wang S., Cheng S., Hu Y., Coveney P.V. (2026).** *Fast-forward prediction of lattice Boltzmann dynamics with physics-informed neural operators.* Nature Communications **17(1), 9243** (online on 29 July 2026). DOI **10.1038/s41467-026-75730-1** (https://www.nature.com/articles/s41467-026-75730-1). [verified]
    Contribution: neural operator that predicts LBE evolution over large time jumps. It builds in “moment-matching” constraints and global equivariance, and is discretisation-invariant (coarse training, fine inference).
15. **Koopman operators and latent dynamics (ML conferences)**:
    - Cheng X., He Y., Yang Y., Xue X., Cheng S., Giles D., Tang X., Hu Y., *Learning Chaos In A Linear Way*, ICLR 2025 (https://openreview.net/forum?id=Llh6CinTiy ; arXiv:2503.14702). **PFNN**: autoencoder and linear operator that respect contraction and measure invariance. [verified: “ICLR 2025 Poster” on OpenReview]
    - Yang Y., Cheng X., Giles D., Cheng S., He Y., Xue X., Chen B., Hu Y., *Tensor-Var: Efficient Four-Dimensional Variational Data Assimilation*, ICML 2025, PMLR 267:70649–70679. [corrected: title “Tensor-Var: Variational Data Assimilation in Tensor Product Feature Space” (taken from Cheng's page) → “Tensor-Var: Efficient Four-Dimensional Variational Data Assimilation” (published title, proceedings.mlr.press/v267)]
    - Cheng X., Yuan W., Yang Y., Zhang Y., Cheng S., He Y., Sun Z., *Information Shapes Koopman Representation*, ICLR 2026, **Oral** (“top 1.2%” according to Cheng's page); arXiv:2510.13025. [verified: “ICLR 2026 Oral” on OpenReview; the “top 1.2%” comes only from Cheng's page]
16. **Cheng S.\*, Lucor D., Argaud J.-P. (2021).** *Observation data compression for variational assimilation of dynamical systems.* Journal of Computational Science **53, 101405**. DOI **10.1016/j.jocs.2021.101405**; arXiv:2106.05427. Joint Cheng–Lucor publication (thesis). [verified]

**Relevant 2026 preprints (arXiv, unpublished at the collection date)**:
- Bocquet M., Finn T.S., Cheng S., *Accounting for model error in ensemble variational data assimilation through learned generative dynamics*, arXiv:2610.17333. **IEnKF-G**: a stochastic generative forecast model replaces the additive Gaussian model error in a weak-constraint 4D-Var. Tests on stochastic Lorenz 63 and multi-scale Lorenz 96; substantial gains under partial observation. [verified]
- Zhou Q., Zhu X., Joli P., Cong Y., Cheng S., *Variational Parameter Calibration with Physics-Aware Latent-Space Surrogates*, arXiv:2608.11435. Differentiable parameters → fields surrogate through a latent space, with observable supervision so that the latents carry the parameter information. Finding: “reconstruction accuracy alone is insufficient for inverse modeling”. [verified]
- Zhang Z. et al. (including Cheng S.), *When Latent Dynamics Meet Data Assimilation: A Benchmark of Koopman-Type Representations*, arXiv:2611.03916. Compares 7 methods on 5 systems; trade-off between representation flexibility and optimisation tractability. [verified]
- Sabnis A.A. et al. (including Cheng S.), *From Deterministic to Generative Deep Learning for Urban Air Quality Reconstruction from Sparse Observations*, arXiv:2607.25687. Multi-pollutant diffusion framework (NO2, O3, PM2.5, PM10) in Paris, evaluated on 9 to 28 stations. [verified]
- Zhou Y., Lin C., Kikumoto H., Ooka R., Cheng S., *Rooftop wind field reconstruction using sparse sensors: From deterministic to generative learning methods*, Building and Environment 296, 114480 (2026) according to Cheng's page; arXiv:2603.13077. Kriging compared with UNet, ViTAE and CWGAN on PIV data; gain of up to 32.7% in SSIM over kriging. [verified: DOI 10.1016/j.buildenv.2026.114480]

---

## 3. Didier Lucor (LISN, CNRS)

### 3.1 Background and themes
Sources: https://perso.lisn.upsaclay.fr/lucor/ and /people.html
- “CNRS research director at the LISN lab”, member of the **DATAFLOT** group (“DAta science, TrAnsition, FLuid instabiLity, contrOl & Turbulence”) of the mechanics department. Deputy director of the LISN from 2022 to 2025. [verified]
- MSc and PhD in applied mathematics, **Brown University (2004)**; two years of postdoc at the Department of Ocean Engineering of **MIT**; ten years at the **Institut d'Alembert** (Sorbonne Université), then LIMSI, which merged with the LRI in 2021 to form the LISN. [verified]
- Declared themes: “stochastic modeling and computational mechanics, with emphasis on: physics-informed statistical learning, reduced-order modeling, uncertainty quantification, data assimilation, sensitivity analysis and robust optimization”. Applications: turbulence modelling, heat transfer, fluid–structure interaction, biomechanics, environmental flows, energy. [verified]
- Position on physical ML (home page): “generalization errors of those models are considerably improved if some "physics information" (in the form of invariant, first principles, symmetries, etc...) is included/enforced”. [verified]
- Guest editor of the special issue of **Computer Physics Communications** “Advances in physics aware machine learning” (same issue as Cheng). [verified; on Lucor's home page this paragraph is now in a commented-out block, not displayed; Cheng's role appears in his CV]
- Related supervisions: Sibo Cheng (EDF–LIMSI thesis, 2017–2020); Rémi Bousquet (LISN M2 2022, then co-author of the VAE/POD work with Nore); Lisa Achard (2025–, joint supervision with Exeter, co-supervised by CEREA). [verified]

### 3.2 Relevant publications (verified, Crossref or HAL or arXiv)

1. **Bousquet R., Nore C., Lucor D. (2025).** *AutoEncoders latent space interpretability in the light of proper orthogonal decomposition: Machine learning of periodically forced fluid flows.* Computer Physics Communications **315, 109728** (October 2025). DOI **10.1016/j.cpc.2025.109728**; hal-05407939 (abstract read via the HAL API: https://api.archives-ouvertes.fr/search/?q=halId_s:hal-05407939&fl=abstract_s). No arXiv version found. [verified]
   Contribution: AEs and VAEs on Navier–Stokes velocity fields (oscillating cylinder, parametric study; von Kármán flow).
   - Increasing the regularisation of the VAEs degrades the reconstruction, which shows a limit of the Gaussian prior.
   - AEs train robustly; VAEs show a “sharper transition between non-learning and learning regimes”.
   - Latent organisation linked to the POD modes; **symmetry analysis and latent ↔ physics equivariance relations**, better preserved by the VAEs; interpretation by clustering of the POD temporal coefficients.
   - This is **the baseline reference of MilaDy on the representation side**, cited in the postdoc and in the 2026 internship.
2. **Bousquet R., Chaffard O., Creff M., Lucor D., Nore C. (2024).** *Large scale analysis of three-dimensional turbulent von Kármán swirling flows.* Physics of Fluids **36(10), 105133**. DOI **10.1063/5.0227495**; hal-04723526. [verified; the abstract reads “Re>104” in Crossref, HAL and on the AIP page (superscript lost): the reading 10⁴ is consistent but the exponent was not seen typeset]
   Contribution: LES (“scheme-consistency preserving large eddy simulations model”) at several Re; POD on the 3D-3C fields. Numerically corroborates “for the first time” a metastable state for **Re > 10⁴**: one-cell axisymmetric structure that breaks the **Rπ** symmetry (rotation by π about a radial axis), with intermittent fluctuations of the angular momentum. Then POD of the azimuthal Fourier modes (2D-3C). The exponent of “Re>104” is lost in the metadata and read as 10⁴ on the AIP page (https://pubs.aip.org/aip/pof/article/36/10/105133/3317096).
3. **Lucor D., Agrawal A., Sergent A. (2022).** *Simple computational strategies for more effective physics-informed neural networks modeling of turbulent natural convection.* Journal of Computational Physics **456, 111022**. DOI **10.1016/j.jcp.2022.111022**. Preprint: arXiv:2103.03565 (“Physics-aware deep neural networks for surrogate modeling of turbulent natural convection”). [verified for the reference; figures: see below]
   Contribution: PINNs for turbulent Rayleigh–Bénard (rough or smooth cavities) from DNS temperature data; “padding” technique for the collocation points; **relaxation of the incompressibility constraint** to ease optimisation.
   Figures (abstract of the arXiv **preprint**, to be re-checked in the JCP version): Ra = 2·10⁹, relative L2 errors from 0.3% to 4% over about 0.5 billion DNS points, training with 1.6% of the points. [verified in the arXiv abstract; UNCONFIRMED in the JCP version, whose abstract is inaccessible (ScienceDirect 403, absent from Crossref and OpenAlex)]
4. **Volk M.-C., Sergent A., Lucor D., Mommert M., Bauer C., Wagner C. (2025).** *A PINN methodology for temperature field reconstruction in the PIV measurement plane: Case of Rayleigh–Bénard convection.* International Communications in Heat and Mass Transfer **167, 109284**. DOI **10.1016/j.icheatmasstransfer.2025.109284**. [verified]
5. **Sundar R., Lucor D., Sarkar S. (2025).** *Sequential learning based PINNs to overcome temporal domain complexities in unsteady flow past flapping wings.* Journal of Fluids and Structures **139, 104421**. DOI **10.1016/j.jfluidstructs.2025.104421**; arXiv:2503.15679. Contribution: temporal decomposition and transfer learning for long PINN integration. [verified]
6. **Sundar R., Majumdar D., Lucor D., Sarkar S. (2024).** *Physics-informed neural networks modelling for systems with moving immersed boundaries: Application to an unsteady flow past a plunging foil.* Journal of Fluids and Structures **125, 104066**. DOI **10.1016/j.jfluidstructs.2024.104066**. [verified]
7. **Cai J., Angeli P.-E., Martinez J.-M., Damblin G., Lucor D. (2024).** *Revisiting Tensor Basis Neural Network for Reynolds stress modeling: Application to plane channel and square duct flows.* Computers & Fluids **275, 106246**. DOI **10.1016/j.compfluid.2024.106246**; arXiv:2403.11746. Contribution: networks that respect Galilean and rotational invariances; transfer learning to unseen Re_τ. [verified; clarification: the transfer learning is used for the square duct]
8. **Jaber E., Blot V., Brunel N., Chabridon V., Remy E., Iooss B., Lucor D., Mougeot M., Leite A. (2025).** *Conformal approach to Gaussian process surrogate evaluation with marginal coverage guarantees.* Journal of Machine Learning for Modeling and Computing **6(3), 37–68**. DOI **10.1615/JMachLearnModelComput.2025054687**. Useful for assessing the uncertainty of generators or surrogates. [corrected: “with (marginal) coverage guarantees” → “with marginal coverage guarantees” (Crossref title; Lucor's page and arXiv give “With Coverage Guarantees”)]
9. **El Garroussi S., Ricci S., De Lozzo M., Goutal N., Lucor D.** *Tackling random fields non-linearities with unsupervised clustering of polynomial chaos expansion in latent space: application to global sensitivity analysis of river flooding.* Stochastic Environmental Research and Risk Assessment **36(3), 693–718** (online in 2021). DOI **10.1007/s00477-021-02060-7**. Combines PCE and latent space. [verified]
10. **Nony B.X., Rochoux M.C., Jaravel T., Lucor D. (2023).** *Reduced-order modeling for parameterized large-eddy simulations of atmospheric pollutant dispersion.* SERRA **37(6), 2117–2144**. DOI **10.1007/s00477-023-02383-7**. Parametric ROM on LES. [verified]
11. **Lucor D., Meyers J., Sagaut P. (2007).** *Sensitivity analysis of large-eddy simulations to subgrid-scale-model parametric uncertainty using polynomial chaos.* Journal of Fluid Mechanics **585, 255–279**. DOI **10.1017/S0022112007006751**. Polynomial chaos applied to LES. [verified]
12. **Lucor D., Karniadakis G.E. (2004).** *Adaptive Generalized Polynomial Chaos for Nonlinear Random Oscillators.* SIAM J. Sci. Comput. **26(2), 720–735**. DOI **10.1137/S1064827503427984**. And **Lucor D., Karniadakis G.E. (2004)**, *Noisy Inflows Cause a Shedding-Mode Switching in Flow Past an Oscillating Cylinder*, PRL **92(15), 154501**, DOI **10.1103/PhysRevLett.92.154501**. [verified]
- Recent publications on robust optimisation and data fusion (DOIs read on Lucor's home page): Zhou H., Wang Z., Lucor D., Sauret E., *New Bayesian optimisation framework for robust multi-objective design: decoupling performance and uncertainty*, RESS **274**, 112359 (2026), DOI 10.1016/j.ress.2026.112359; Jaber E., Remy E., Chabridon V., Mougeot M., Lucor D., *Fusion of heterogeneous data for robust degradation prognostics*, RESS **274**, 112435 (2026), DOI 10.1016/j.ress.2026.112435. [verified; titles and volume 274 added from Crossref]
- Joint with Cheng: the IEEE/CAA JAS 2023 review (§2.2 no. 1) and JCS 2021 (§2.2 no. 16); Cheng et al., *A graph clustering approach to localization…*, Mathematical Geosciences 53(8), 1751–1780 (2021); two SERRA articles (2019, 2020), according to the publication pages of both authors. [verified: Math. Geosci. DOI 10.1007/s11004-021-09951-z; SERRA 33(11-12), 2033–2051 (2019), DOI 10.1007/s00477-019-01743-6; SERRA 35(5), 1019–1038 (online in 2020), DOI 10.1007/s00477-020-01933-7]
- Addition (preprint, no MilaDy funding indicated): **Bousquet R., Faucheu A., Dumas L., Nore C., Lucor D. (2026).** *Polynomial autoencoders with quantifiable errors for nonlinear fluid flow reconstruction.* Research Square, submitted on 19 June 2026, DOI 10.21203/rs.3.rs-10008570/v1. Autoencoders with learnable polynomial activations, initialised to be exactly equivalent to the POD; the POD initialisation speeds up training by an order of magnitude (oscillating cylinder). Direct continuation of CPC 2025. [verified, addition]

---

## 4. Caroline Nore (LISN, Université Paris-Saclay)

### 4.1 Positioning and the SFEMaNS tool
- Status: “Pr. UPS C. Nore” in the MilaDy postdoc PDF (https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf) ; “Pr. Caroline Nore (LISN)” in the internship offer [English: “Pr.” = Professor; “UPS” = Université Paris-Saclay]. Coordinator of MilaDy (ANR page). [verified] HAL affiliation of the MilaDy articles: LISN, **COMET** team (plus DATAFLOT for CPC 2025). [verified, addition]
- **SFEMaNS** (documentation v5.3: https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html). The code headers credit J.-L. Guermond and C. Nore (finding from the web search, headers not opened directly). [UNCONFIRMED for the headers; on the other hand the Nore–Lucor M2 offer speaks of “our massively parallel research code SFEMaNS”: verified]
  - Equations: incompressible Navier–Stokes (Re), heat, Maxwell in a conducting domain with permeability μ^c and conductivity σ (Rm), with jump conditions across a discontinuous-permeability interface Σ_μ, and scalar potential φ in the vacuum (H = ∇φ). Modes: NST, MXW (kinematic), MHD (Lorentz force), FHD (ferrofluids, Kelvin force). [verified]
  - Discretisation: “cylindrical coordinates (r,θ,z) and assumes a priori that the computational domain is axi-symmetric. The approximation method consists of using a Fourier decomposition in the azimuthal direction and Lagrange finite elements in the meridian section”. [verified]
  - Extensions: “Stabilization method, called entropy viscosity, for problems with large kinetic Reynolds numbers”, non-axisymmetric geometry, multiphase, “Magnetic permeability depending of the time and the azimuthal direction”, quasi-static approximation. [verified]
  - Consequence for learning: the data are a **hybrid representation (Fourier modes m) × (unstructured meridian FE mesh)**, and not a Cartesian grid. [verified: follows from the documentation]
- Entropy viscosity (not co-written by Nore): Guermond J.-L., Pasquetti R., Popov B. (2011), *Entropy viscosity method for nonlinear conservation laws*, JCP **230(11), 4248–4267**, DOI 10.1016/j.jcp.2010.11.043 (Crossref). [verified]

### 4.2 Relevant publications (verified, HAL or Crossref)

Full HAL list (82 documents [verified on 6/11/2026]): https://api.archives-ouvertes.fr/search/?q=authFullName_s:%22Caroline%20Nore%22

1. **Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2016).** *Direct numerical simulation of the axial dipolar dynamo in the Von Karman Sodium experiment.* EPL **114, 65002**. DOI **10.1209/0295-5075/114/65002**; hal-02365015. [verified]
   Contribution: “For the first time”, full nonlinear MHD DNS of VKS with both counter-rotating turbines represented. The dynamo threshold **decreases as the magnetic permeability of the turbines increases**. Two magnetic families compete at low Re and merge at higher Re. Soft iron favours an **essentially axisymmetric axial dipole**, as in the experiment.
2. **Nore C., Castanon Quiroz D., Cappanera L., Guermond J.-L. (2018).** *Numerical simulation of the von Kármán sodium dynamo experiment.* Journal of Fluid Mechanics **854, 164–195**. DOI **10.1017/jfm.2018.582** (abstract read via Crossref). [verified]
   Contribution: soft-iron turbines represented by a **pseudo-penalisation**; LES at high Re; Kolmogorov-type spectrum; helical vortices at the blade tips; undulating equatorial shear layer (3 co-rotating radial vortices).
   - Rm_c decreases as μ increases (Re fixed) and as Re increases (μ fixed), hence the conjecture that Rm_c tends to a constant as Re → ∞.
   - Essentially axisymmetric axial dipole dynamo; speculative mechanism proposed.
3. **Bousquet R., Ponty Y., Botez V., Plihon N., Nore C. (2026).** *Magnetic field reversals in numerical simulations of the von Kármán sodium experiment.* Physical Review Fluids **11(6), 063703** (received on 19/01/2026, published on 18/06/2026). DOI **10.1103/9tx2-1m13**; hal-05668081. Full text: https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf [verified: PDF opened; dates, parameters, definitions of Re and Rm, constraints (10)–(11), problem (12), Tables I–II and data availability re-read in the text]
   - **Two solvers**: LATU (ref. [22] = Kreuzahler et al. 2017) and SFEMaNS (ref. [23] = Nore et al. 2018). Turbines by penalisation (ref. [28] Pasquetti et al. 2008); variable μ_r(x,t) for non-axisymmetric soft-iron turbines (disc + 8 curved blades).
   - Forcing parameters: asymmetry (F1 − F2)/(F1 + F2); Re = 2πF R_cyl R_imp/ν; Rm = 2πF R_cyl R_imp μ0σ.
   - Reference simulation (LATU geometry): **Re = 1594, Rm = 531, asymmetry = 0.058, μ_r = 16 in the turbines** (1 elsewhere), σ_r = 1. A strong asymmetry (≈ 1/4) triggers periodic reversals.
   - “a conductive surrounding medium was found to be necessary for these inversions to occur” (in the explored range).
   - **5-step** mechanism: dipole, weakening near the fast turbine, quadrupolar state, weakening near the slow turbine, reversed dipole. It is interpreted as two localised dipoles, one per turbine.
   - **POD on 2000 snapshots** of u and H: 4 dominant axisymmetric modes, ψ_D (dipole), ψ_Q (quadrupole), φ_V (zonal, Rπ-antisymmetric) and φ_U (Rπ-symmetric). m = 8 signature of the blades; POD modes n = 3, 4 (m = 2) associated with the Kelvin–Helmholtz vortices.
   - **DQVU Galerkin model** obtained by projection of the MHD equations, which reduces to the already known DQV model. Coefficients identified by **constrained Galerkin regression with PySINDy**, under two constraints: quadratic Navier–Stokes A_uvv + A_vvu = 0, and statistical conservation of the 3rd moment X²·f(X,p) = 0. Time derivatives computed with a Savitzky–Golay filter. DQVU reproduces the **asymmetric bimodal** distribution of V, which DQV does not. Coefficients given in the appendix (Tables I and II).
   - **Data not public** (“available from the authors upon reasonable request”). Computing: GENCI and OPAL (Université Côte d'Azur).
4. **Botez V., Giesecke A., Nore C., Cappanera L., Stefani F. (2026).** *Impact of boundary conditions on onset and symmetry of precession-driven dynamos.* Physical Review Fluids **11(8), 083701** (received on 27/04/2026, published on 14/08/2026). DOI **10.1103/rx1h-5zxp**; hal-05782992 (abstract read via the HAL API, Crossref and OpenAlex; PDF blocked by the anti-bot system). [corrected: “2026-10-07” (date of the HAL record) → published on 14 August 2026 (Crossref, August 2026 issue)]
   Contribution: **kinematic** precession dynamo in a cylinder, in a “narrow range of Poincaré numbers where dynamo action is most likely”, from time-averaged velocity fields.
   - Two families of modes: centro-symmetric quadrupolar at higher frequency, centro-antisymmetric dipolar at lower frequency.
   - The simplified “vanishing-tangential-field” conditions **systematically underestimate Rm_c**. Conducting or permeable walls can favour or suppress the dynamo.
   - Direct application to **DRESDYN**.
5. **Botez V., Bousquet R., Nore C. (2025).** *Large scale analysis of the von Kármán sodium experiment using proper orthogonal decomposition.* Magnetohydrodynamics **61(1/2), 13–24**. DOI **10.22364/mhd.61.1-2.2** (https://mhd.sal.lv/contents/2025/1/MG.61.1.2.R.html). [verified]
   Contribution: POD of VKS simulations in growth and saturation phases. In growth, axial dipole with secondary structures from the α effect. In saturation, the magnetic feedback **breaks the symmetry of the velocity field** even with exact counter-rotation.
6. **Creff M., Faller H., Dubrulle B., Guermond J.-L., Nore C. (2024).** *Tracking dynamo mechanisms from local energy transfers: Application to the von Kármán sodium dynamo.* Physics of Plasmas **31(2), 022306**. DOI **10.1063/5.0174251**.
   Contribution: local energy budgets in space, scale and time, with a filtering applicable to **unstructured meshes**. For steel turbines, the dynamo comes from transfers in the volume and near the turbines; for soft iron, mainly from the rotation of the blades. Precursors of anomalous dissipation and of fast dynamo. This is a **physical metric** tool for generated fields. Associated thesis: M. Creff, *Rôle des transferts d'énergie dans l'effet dynamo : application à l'écoulement de von Kármán* [English: Role of energy transfers in the dynamo effect: application to the von Kármán flow], Université Paris-Saclay, 21/12/2023, supervised by C. Nore and B. Dubrulle (tel-04477539 ; https://api.archives-ouvertes.fr/search/?q=halId_s:tel-04477539). [verified]
7. **Nore C., Léorat J., Guermond J.-L., Luddens F. (2011).** *Nonlinear dynamo action in a precessing cylindrical container.* Physical Review E **84(1), 016317**. DOI **10.1103/PhysRevE.84.016317**; arXiv:1102.1846. Contribution: numerical demonstration (MHD code) that **precession can trigger the dynamo effect** in a cylinder. [verified]
8. **Cappanera L., Guermond J.-L., Léorat J., Nore C. (2016).** *Two spinning ways for precession dynamo.* Physical Review E **93(4), 043113**. DOI **10.1103/PhysRevE.93.043113**. [verified; abstract read via OpenAlex]
   Contribution: spin–precession angle fixed at π/2; two configurations, “axial spin” (cylinder axis parallel to the spin) and “equatorial spin” (axis perpendicular). The centro-symmetry of the flow breaks as Re increases, more efficiently in equatorial spin; the mean flow tends towards a counter-rotation with respect to the spin axis. In equatorial spin, the asymmetric unsteady flow sustains a dynamo (linear and nonlinear regimes), with a mostly dipolar field; in axial spin, the field is mostly quadrupolar. Scaling law of the mean kinetic energy as a function of Re (axial spin). [addition]
9. **Nore C., Guermond J.-L., Laguerre R., Léorat J., Luddens F. (2012).** *Nonlinear dynamo in a short Taylor–Couette setup.* Physics of Fluids **24(9), 094106**. DOI **10.1063/1.4752756**.
   Contribution: dynamo in a short Taylor–Couette setup with a body force. Threshold comparable to spherical geometries; linear dynamo with a rotating equatorial dipole; nonlinear regime with a tilted dipole whose axial component shows **aperiodic reversals**. [verified]
10. **Giesecke A., Nore C., Stefani F., Gerbeth G., Léorat J., Herreman W., Luddens F., Guermond J.-L. (2012).** *Influence of high-permeability discs in an axisymmetric model of the Cadarache dynamo experiment.* New Journal of Physics **14, 053005**. DOI **10.1088/1367-2630/14/5/053005**; arXiv:1112.1780.
    Figure: Rm_c(μ) − Rm_c(μ→∞) ∼ μ^(−1/2) (skin effect in the discs). An axisymmetric toroidal mode localised in the discs dominates at large μ. The idealised pseudo-vacuum conditions (H×n = 0) do not recover this role of the discs. [verified]
11. **Laguerre R., Nore C., Ribeiro A., Léorat J., Guermond J.-L., Plunian F. (2008).** *Impact of Impellers on the Axisymmetric Magnetic Mode in the VKS2 Dynamo Experiment.* PRL **101(10), 104501**. DOI **10.1103/PhysRevLett.101.104501**; arXiv:0805.2805. Figure (abstract): observed Rm_c ≈ 32, reachable with ferromagnetic boundary conditions and an α effect of the turbines. [verified]
12. **Numerical methods (foundations of SFEMaNS)**:
    - Guermond, Laguerre, Léorat, Nore (2007), *An interior penalty Galerkin method for the MHD equations in heterogeneous domains*, JCP **221, 349–369**, DOI 10.1016/j.jcp.2006.06.045.
    - Guermond, Laguerre, Léorat, Nore (2009), *Nonlinear magnetohydrodynamics in axisymmetric heterogeneous domains using a Fourier/finite element technique and an interior penalty method*, JCP **228, 2739–2757**, DOI 10.1016/j.jcp.2008.12.026.
    - Guermond, Léorat, Luddens, Nore, Ribeiro (2011), *Effects of discontinuous magnetic permeability on magnetodynamic problems*, JCP **230, 6299–6319**, DOI 10.1016/j.jcp.2011.04.026.
    All three taken from HAL. [verified: identical Crossref metadata]
- Others: Nore, Léorat, Guermond, Giesecke (2015), *Mean-field model of the von Karman sodium dynamo experiment using soft iron impellers*, PRE **91, 013008**, DOI 10.1103/PhysRevE.91.013008; Stefani, Albrecht, Gerbeth, Giesecke, Gundrum, Herault, Nore, Steglich (2015), *Towards a precession driven dynamo experiment*, Magnetohydrodynamics **51, 275–284**, DOI 10.22364/mhd.51.2.11 (DRESDYN); Giesecke et al. (2010), *Electromagnetic induction in non-uniform domains*, GAFD **104(5-6), 505–529**, DOI 10.1080/03091929.2010.507202. [verified: 3 references]
- DRESDYN context, without Nore as co-author: Giesecke A., Vogt T., Gundrum T., Stefani F. (2018), *Nonlinear Large Scale Flow in a Precessing Cylinder and Its Ability To Drive Dynamo Action*, PRL **120(2), 024502**, DOI 10.1103/PhysRevLett.120.024502 (Crossref). [verified]
- Other lines of work of Nore, little related to the offer: liquid-metal batteries (Tayler instability, JFM 771, 2015; metal pad roll, PRL 126, 184501, 2021), ferrofluids, electrovortices. [verified: Herreman, Nore, Cappanera, Guermond, JFM 771, 79–114 (2015), DOI 10.1017/jfm.2015.159; Nore, Cappanera, Guermond, Weier, Herreman, PRL 126, 184501 (2021), DOI 10.1103/PhysRevLett.126.184501]
- **Relevant supervised theses (HAL)**: F. Luddens (2012, with Guermond, MHD and dynamo); L. Cappanera (2015, nonlinear stabilisation of MHD); M. Creff (2023, with Dubrulle, energy transfers and VKS dynamo). Query: https://api.archives-ouvertes.fr/search/?q=director_s:%22Caroline%20Nore%22 [verified]
- **Addition, machine-learning thesis co-supervised by Nore**: M. Quattromini, *Graph Neural Networks pour la mécanique des fluides : assimilation de données et optimisation* [English: Graph neural networks for fluid mechanics: data assimilation and optimisation], defended on 13/12/2024 (tel-04964013), co-supervised by C. Nore, S. Cherubini, O. Semeraro and M. A. Bucci. Nore has therefore already co-supervised a thesis in ML and data assimilation. [verified, addition]

---

## 5. Yannick Ponty (Observatoire de la Côte d'Azur, Lagrange, CNRS)

### 5.1 Background
Sources: two-page CV 2026 (https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf) and long CV (https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-Yannick-Ponty.pdf). The lagrange.oca.eu mirror has an expired TLS certificate and was not used.
- CNRS research director since October 2014 (section 10, then 12) at the laboratoire J.-L. Lagrange (UMR 7293), OCA, Nice. Head of the « Turbulence Fluide et Plasma » [English: Fluid and Plasma Turbulence] team since October 2025 (already from 2011 to 2021). External member of the INRIA CASTOR team. [verified]
- CNRS CR from 2000 to 2014; Research Fellow in the MHD group of the University of Exeter from 1997 to 2000; thesis in 1997 (« Textures convectives dans un fluide en rotation et effet dynamo dans un écoulement chaotique » [English: Convective textures in a rotating fluid and dynamo effect in a chaotic flow]); HDR in 2012 (« Rôle de la turbulence sur l'effet dynamo et l'induction magnétique » [English: Role of turbulence on the dynamo effect and magnetic induction], tel-00922148). [verified]
- Declared keywords: « Magnétohydrodynamique (MHD), Effet Dynamo, Turbulence, HPC (High Performance Computing), Contrôle Optimale » [English: Magnetohydrodynamics (MHD), Dynamo Effect, Turbulence, HPC (High Performance Computing), Optimal Control]. « 30 publications avec comité de lecture » [English: peer-reviewed publications, same count], including two PRL covers and one “Editor Suggestion”. [verified]
- Supervision: co-supervision of the thesis of S. Kreuzahler (Bochum, with R. Grauer, 2012–2015) on **penalisation for VKS**; MilaDy postdoc since February 2026; M1 intern in 2025 on HPC with Kokkos. [verified]

### 5.2 Relevant publications (verified, HAL, Crossref or arXiv)

HAL list: https://api.archives-ouvertes.fr/search/?q=authFullName_s:%22Yannick%20Ponty%22 (30 documents [verified on 6/11/2026]).

1. **Ponty Y., Mininni P.D., Montgomery D.C., Pinton J.-F., Politano H., Pouquet A. (2005).** *Numerical study of dynamo action at low magnetic Prandtl numbers.* PRL **94, 164502**. DOI **10.1103/PhysRevLett.94.164502**; arXiv:physics/0410046; hal-00133225. [verified]
   Contribution: Taylor–Green forcing, approach combining DNS, averaged Lagrangian model and LES. Figures (abstract): dynamos observed “from P_M=1 down to P_M=10⁻²”; Rm_c increases strongly with P_M⁻¹ then saturates; **Kazantsev k^(3/2)** spectrum in the linear phase.
2. **Ponty Y., Plunian F. (2011).** *Transition from Large-Scale to Small-Scale Dynamo.* PRL **106, 154502**. DOI **10.1103/PhysRevLett.106.154502**; arXiv:2004.11028. [verified; arXiv preprint submitted in 2020, with the PRL 2011 reference]
   Contribution: Roberts-type helical forcing (link with Karlsruhe). The threshold is controlled by the long time scales; generalised α effect ∼ **O(Rm⁻¹)** beyond the threshold, which indicates a takeover by the small-scale dynamo.
3. **Ponty Y., Laval J.-P., Dubrulle B., Daviaud F., Pinton J.-F. (2007).** *Subcritical Dynamo Bifurcation in the Taylor-Green Flow.* PRL **99(22), 224501** (cover). DOI **10.1103/PhysRevLett.99.224501**; arXiv:0707.2498. **Subcritical** bifurcation, hysteresis linked to the hydrodynamic changes induced by the Lorentz force. [verified]
4. **Ponty Y., Mininni P.D., Pinton J.-F., Politano H., Pouquet A. (2007).** *Dynamo action at low magnetic Prandtl numbers: mean flow versus fully turbulent motions.* New Journal of Physics **9, 296**. DOI **10.1088/1367-2630/9/8/296**. [verified]
5. **Alexakis A., Ponty Y. (2008).** *Effect of the Lorentz force on on-off dynamo intermittency.* PRE **77, 056308**. DOI **10.1103/PhysRevE.77.056308**; arXiv:0710.0063. [verified]
   Contribution: ABC forcing near the threshold, **on-off intermittency**. At large Re, the duration of the “on” phases follows a **power law**; at small Re, the Lorentz force suppresses the noise (periodic “laminar” flow). Directly related to the **bursts and rare events** of MilaDy.
6. **Kreuzahler S., Schulz D., Homann H., Ponty Y., Grauer R. (2014).** *Numerical study of impeller-driven von Kármán flows via a volume penalization method.* New Journal of Physics **16(10), 103001**. DOI **10.1088/1367-2630/16/10/103001**. [verified]
7. **Kreuzahler S., Ponty Y., Plihon N., Homann H., Grauer R. (2017).** *Dynamo Enhancement and Mode Selection Triggered by High Magnetic Permeability.* PRL **119(23), 234501** (cover). DOI **10.1103/PhysRevLett.119.234501**; arXiv:1706.00260.
   - Method (arXiv text): “standard Fourier pseudospectral method on a regular Cartesian grid”, turbines and walls by **penalisation**, “sharpened raised cosine” filter against the Gibbs phenomenon at the μ jumps, periodic box **(3π)³ with 384³ points**, cylinder of radius 3.0 and height 6.0, μ_r from 1 to 16.
   - Result: self-generated axisymmetric dynamo mode beyond a permeability threshold.
   - This code is the **“LATU” solver** of Bousquet et al. 2026 (ref. [22]). [verified: Bousquet 2026 writes “LATU [22]”, and [22] = Kreuzahler et al. 2017; arXiv text v4 re-read]
8. **Homann H., Ponty Y., Krstulovic G., Grauer R. (2014).** *Structures and Lagrangian statistics of the Taylor–Green dynamo.* New Journal of Physics **16(7), 075014**. DOI **10.1088/1367-2630/16/7/075014**. [verified]
9. **Mannix P.M., Ponty Y., Marcotte F. (2022).** *Systematic Route to Subcritical Dynamo Branches.* PRL **129(2), 024502** (Editor's Suggestion). DOI **10.1103/PhysRevLett.129.024502**; arXiv:2112.11376. Nonlinear optimisation of a finite-amplitude perturbation that identifies the **subcritical dynamo branches** and their critical perturbations without knowing the amplification mechanism (adjoint or optimisation approach). [verified]
10. **Ponty Y., Politano H., Pouquet A. (2025).** *Intermittency assessed through a model of kurtosis–skewness relation in MHD in fast dynamo regimes.* Journal of Plasma Physics **91(2), E69**. DOI **10.1017/S0022377825000169**.
    Figures (HAL abstract): DNS with Taylor–Green and ABC forcings up to **3.14 × 10⁵ turnover times**; K(S) ∼ S^α laws with 0.2 ≲ α ≲ 3.0; α ≈ 2.5 with the She–Lévêque model. Useful as a **high-order statistical metric** to validate generated fields. [verified; clarification: the range 0.2 ≲ α ≲ 3.0 concerns the dissipation]
11. **Pouquet A., Marino R., Politano H., Ponty Y., Rosenberg D. (2025).** *Intermittency in fluid and magnetohydrodynamics (MHD) turbulence analyzed through the prism of moment scaling predictions of multifractal models.* Nonlinear Processes in Geophysics **32, 243–259**. DOI **10.5194/npg-32-243-2025**. [verified; issue 3]
12. **Bousquet R., Ponty Y., Botez V., Plihon N., Nore C. (2026)**, PRFluids **11, 063703**, see §4.2 no. 3. Ponty lists it among his “5 Publications significatives” [English: significant publications] (CV 2026). [verified]
- Also: Ponty Y. (2008), *Course 6 Numerical modeling of liquid metal dynamo experiments*, Les Houches, pp. 359–382, DOI 10.1016/S0924-8099(08)80010-8 (Crossref); Ponty, Politano, Pinton (2004), *Simulation of Induction at Low Magnetic Prandtl Number*, PRL **92, 144503**, DOI 10.1103/PhysRevLett.92.144503; Ponty et al. (2008), *Linear and non-linear features of the Taylor-Green dynamo*, C. R. Physique **9, 749–756**, DOI 10.1016/j.crhy.2008.07.007. [verified: 3 references]
- **ML / AI**: no publication by Ponty on machine learning was found (HAL, Crossref, arXiv). His skills close to the offer are nonlinear optimisation and optimal control (Mannix 2022, keyword “Contrôle Optimale” [English: Optimal Control]), HPC (Kokkos), intermittency statistics and pseudo-spectral codes with penalisation. [verified: arXiv `au:Ponty_Y` with `abs:learning` or `abs:neural` → 0; HAL likewise → 0]

---

## 6. Skills matrix (summary for the writers) [revised: Nore completed (CPC 2025, Quattromini thesis)]

| Skill required by the offer | Cheng | Lucor | Nore | Ponty |
|---|---|---|---|---|
| Diffusion and conditional generative modelling | Zhuang 2025; Yu 2026 GMD; VQ-VAE 2023; IEnKF-G 2026 (preprint) | (Achard thesis, generative, ongoing) | – | – |
| Latent space, ROM, interpretability | GLA 2022; LDA; Koopman (ICLR 2025, 2026) | AE/VAE vs POD (CPC 2025); polynomial AEs (2026 preprint); LES ROM | AE/VAE vs POD (CPC 2025, co-author); POD of VKS (PoF 2024, MHD 2025); DQVU Galerkin (2026) | DQVU (2026) |
| Physical constraints in the losses | MSPCNN 2024; DSOVT 2025; LBM Nat Commun 2026 | PINNs for Rayleigh–Bénard (JCP 2022, ICHMT 2025); TBNN with invariances | – | – |
| Data assimilation | TorchDA; VIVID; JAS 2023 review | JAS 2023 review; Cheng's thesis (covariances) | co-supervision of the Quattromini thesis (GNN, DA, 2024) | – |
| UQ | JAS 2023 review | gPC (SISC 2004, JFM 2007); conformal prediction (JMLMC 2025) | – | – |
| 3D MHD and dynamo data | – | (co-author VKS 2024, 2025) | SFEMaNS: VKS, precession/DRESDYN, Taylor–Couette | LATU (pseudo-spectral + penalisation); Taylor–Green, ABC, Roberts |
| Physics of reversals and rare events | – | – | VKS reversals (2026) and Taylor–Couette (2012) | on-off (2008), subcritical (2007, 2022) |
| Physical metrics | – | – | local energy transfers (Creff 2024) | kurtosis–skewness, intermittency (2025) |

---

## 7. Thesis topic leads (intersection of the 4 supervisors)

*These are drafting proposals. The bottlenecks and risks are deduced from the cited sources; they are not stated as such by the supervisors.*

*Verification: the leads are proposals and cannot be verified like facts. The references and figures they cite (Re = 1594, Rm = 531, μ_r = 16, 2000 snapshots, “narrow” window in Poincaré, 3.14×10⁵ turnover times, FunDiff = Wang et al. 2026 cited in the 2027 offer) point to entries verified above. [verified]*

### Lead A: Conditional generator of parametric 3D MHD fields in a physically structured latent space
- **Statement**: learn p(u, H | Re, Rm, μ_r, forcing asymmetry) for VKS by latent diffusion or latent flow matching. The autoencoder is constrained by the symmetries (Rπ, latent ↔ physics equivariance), regressed on the parameters and possibly aligned on the POD modes.
- **Bottleneck**: generalise beyond the few simulated (Re, Rm, μ) points; preserve ∇·(μ_r H) = 0 and ∇·u = 0 after decoding; preserve the symmetries; Fourier × unstructured finite-element representation.
- **Extends**: Bousquet, Nore, Lucor 2025 (CPC); Bousquet et al. 2024 (PoF); MilaDy 2026 internship (latent regression, contrastive); Zhuang, Cheng, Duraisamy 2025 (conditional diffusion); Zhou et al. 2024 (MSPCNN); Zhou et al. 2026 (preprint, “physics-aware” latent surrogates for calibration).
- **Data**: SFEMaNS VKS (Nore et al. 2016, 2018: sweeps in μ and Re; Creff et al. 2024: steel or soft-iron turbines); LATU (Kreuzahler et al. 2017, μ_r from 1 to 16).
- **Risks**: few parametric points, because each MHD DNS is costly (the ANR summary speaks of “very costly” DNS); 3D data volume; non-public data (access through the consortium); reconstruction/regularisation tension already observed for the VAEs (Bousquet 2025).

### Lead B: Probabilistic generation and forecasting of magnetic reversals and rare events, guided by a reduced model
- **Statement**: temporal generative model (autoregressive diffusion or state-conditioned diffusion) producing ensembles of field trajectories in the neighbourhood of reversals. It is guided at sampling time (“universal guidance”) by the DQVU model or by Galerkin constraints, to estimate probabilities, waiting times and precursor / reversal / recovery phases.
- **Bottleneck**: rarity of the events (few reversals per simulation), heavy-tailed statistics (power laws of the “on” phases), consistency between generated 3D field and reduced dynamics, probabilistic calibration.
- **Extends**: Bousquet et al. 2026 (PRFluids: DQVU, POD on 2000 snapshots, constrained identification); Alexakis & Ponty 2008 (on-off); Ponty et al. 2007 and Mannix et al. 2022 (subcriticality); Nore et al. 2012 (aperiodic reversals in Taylor–Couette); Yu et al. 2026 GMD (diffusion ensembles, HR score); Cheng X. et al., ICLR 2025 (measure invariance).
- **Data**: LATU and SFEMaNS reversal simulations of Bousquet 2026 (Re = 1594, Rm = 531, μ_r = 16, external conducting layer); Ponty's ABC and Taylor–Green DNS for intermittency.
- **Risks**: long time series needed (cost); the DQVU model only imperfectly reproduces the distribution of Q (Bousquet 2026); rare-event metrics are hard to validate statistically.

### Lead C: Latent data assimilation with a generative prior for reconstructing dynamos from sparse measurements
- **Statement**: reconstruct 3D states (u, H) from synthetic sparse observations, of the simulated magnetic-probe type, by combining a generative prior (conditional diffusion) and a latent variational or ensemble assimilation (GLA, TorchDA, IEnKF-G).
- **Bottleneck**: multimodal posterior (± polarity of the dipole, hence non-Gaussian posteriors), nonlinear observation operator, dimension, physical consistency of the analysis.
- **Extends**: Cheng et al. 2022 (GLA); Cheng et al. 2024 (VIVID); Cheng et al. 2025 (TorchDA, cited by the ANR); Bocquet, Finn, Cheng 2026 (IEnKF-G); Zhang et al. 2026 (Koopman-LDA benchmark); Cheng et al. 2023 (review with Lucor); Jaber et al. 2025 (conformal coverage).
- **Data**: subsampled SFEMaNS and LATU outputs; intermediate Lorenz and shallow-water benchmarks (already in TorchDA).
- **Risks**: no experimental VKS or DRESDYN data identified as accessible (not verified); synthetic observations would probably be needed; cost of diffusion sampling inside an assimilation loop.

### Lead D: Parametric generative surrogate for exploring DRESDYN (precession)
- **Statement**: generate mean or fluctuating velocity fields conditioned on the Poincaré number, Re and the wall properties, then estimate Rm_c and the symmetry of the dominant mode. This can be done with a kinematic solver (SFEMaNS MXW) applied to the generated fields, or with a prediction head. The framework is robust Bayesian optimisation under uncertainty.
- **Bottleneck**: the Poincaré window where the dynamo is likely is “narrow” (Botez 2026); abrupt transitions between hydrodynamic states; strong sensitivity of Rm_c to the electromagnetic conditions (pseudo-vacuum or real vacuum, conducting or permeable walls).
- **Extends**: Botez et al. 2026 (PRFluids 083701); Nore et al. 2011 (PRE); Cappanera et al. 2016 (PRE); Stefani et al. 2015; Giesecke et al. 2018; Zhou, Wang, Lucor, Sauret 2026 (RESS, robust Bayesian optimisation); Zhou et al. 2026 (preprint, latent variational calibration).
- **Data**: hydrodynamic precession simulations and averaged fields of Botez et al. (SFEMaNS, with HZDR). Objective (ii) of the ANR explicitly targets “parametric ROMs” for DRESDYN.
- **Risks**: few simulated configurations; propagation of the generator error in a sensitive eigenvalue problem; dependence on the DRESDYN schedule (the ANR summary speaks of an experiment “under way” and the postdoc of a success that is “uncertain”).

### Lead E: Hard constraints in generative models on hybrid Fourier–finite-element meshes
- **Statement**: formulate diffusion or flow matching in function space (FunDiff-type) or on the SFEMaNS representation (m modes × meridian FE), by exactly imposing ∇·B = 0 (vector potentials or poloidal–toroidal decomposition), the interface conditions at the μ jumps and the vacuum conditions, and by controlling the energy budget (projection at sampling time or loss).
- **Bottleneck**: unstructured meshes, μ discontinuities (H×n and μH·n conditions), penalised zones (turbines); trade-off between hard constraint and sample quality.
- **Extends**: Guermond, Nore et al. 2007, 2009, 2011 (JCP: interior penalty, discontinuous permeability); Giesecke et al. 2012 (role of the boundary conditions); Cheng et al. 2025 (review on unstructured meshes); Xue et al. 2026 (Nat Commun: moment constraints, discretisation invariance); Lucor et al. 2022 (relaxation of incompressibility in PINNs).
- **Data**: native SFEMaNS outputs; prior validation on simple PDEs, as the offer requires.
- **Risks**: implementation cost on unstructured meshes; hard constraints can degrade sample diversity; software integration with a Fortran code (the web search lists documentation pages of `.f90` sources, for example `main_8f90_source.html`; not opened).

### Lead F (cross-cutting): Test benches and physical metrics for MHD generators, from Taylor–Green and ABC to VKS
- **Statement**: build a ladder of benchmarks (simple PDEs, then periodic Taylor–Green, ABC and Roberts dynamos on Ponty's codes, then VKS and precession on SFEMaNS and LATU) and a battery of metrics: spectra (including Kazantsev k^(3/2)), helicity, divergence, topology, local energy transfers (Creff 2024), kurtosis–skewness relations (Ponty 2025), conformal coverage (Jaber 2025), HR score (Yu 2026).
- **Bottleneck**: define discriminating, mesh-invariant metrics; cost of the 3D diagnostics.
- **Extends**: Ponty et al. 2005, 2007; Ponty & Plunian 2011; Ponty et al. 2025 (JPP); Creff et al. 2024; 2026 internship (identical metrics).
- **Data**: periodic DNS in a Cartesian box, simpler to learn; long series up to 3.14×10⁵ turnover times (Ponty 2025).
- **Risks**: more methodological topic, with a risk that the “benchmark” contribution is judged incremental; it is better to attach it to A or B.

---

## 8. Main sources opened

- ANR, FR page: https://anr.fr/Projet-ANR-25-CE51-0077
- ANR, EN page: https://anr.fr/en/funded-projects-and-impact/funded-projects/project/funded/project/b2d9d3668f92a3b9fbbf7866072501ef-8f0bea4141/?tx_anrprojects_funded%5Bcontroller%5D=Funded&cHash=f7b87490b7ffc2a2a9c7dc94387c163f
- 2027 internship offer: https://scheng2024.github.io/stage_milady_2027.pdf
- 2026 internship: https://stages.phys.ens.psl.eu/OffresPDF/Offre-30818.pdf
- LISN postdoc: https://perso.lisn.upsaclay.fr/lucor/pdf/postdoc_milady_LISN.pdf
- Nore–Lucor M2 internship: https://perso.lisn.upsaclay.fr/lucor/pdf/M2Stage_Nore_Lucor.pdf
- ml-news announcement: https://groups.google.com/g/ml-news/c/lr8uwyCAl_M
- Cheng: https://scheng2024.github.io/ ; /research/ ; /publications/ ; /cv/ ; /people/ ; /opportunities/
- Lucor: https://perso.lisn.upsaclay.fr/lucor/ ; /publications.html ; /people.html ; /opportunities.html
- Ponty: https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-2pages-2026.pdf ; https://c2pu.oca.eu/images/LAGRANGE/pages_perso/ponty/pdf/cv-Yannick-Ponty.pdf
- SFEMaNS: https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html
- Bousquet et al. 2026, full text: https://perso.ens-lyon.fr/nicolas.plihon/Publis/Bousquet_PRF_11.pdf
- Kreuzahler et al. 2017, arXiv text: https://arxiv.org/pdf/1706.00260v4
- GMD 2026: https://gmd.copernicus.org/articles/19/1027/2026/
- Nature Communications 2026: https://www.nature.com/articles/s41467-026-75730-1
- Magnetohydrodynamics 2025: https://mhd.sal.lv/contents/2025/1/MG.61.1.2.R.html
- Physics of Fluids 2024: https://pubs.aip.org/aip/pof/article/36/10/105133/3317096
- HAL API: https://api.archives-ouvertes.fr/search/ (queries by halId_s, authFullName_s, anrProjectReference_s, director_s)
- Crossref API: https://api.crossref.org/works (queries by DOI or by title and author)
- arXiv API: https://export.arxiv.org/api/query (queries by id_list, ti:, au:)
- Added during the cross-check: OpenAlex API (`api.openalex.org`, APS abstracts); PMLR v267 (https://proceedings.mlr.press/v267/) ; OpenReview API (ICLR status); source code of Lucor's Opportunities and home pages; arXiv text of Kreuzahler 2017 (v4).

---

## 9. Unconfirmed

*Points that remained open after the cross-check of 6 November 2026. The points resolved during this verification are listed at the end.*

- **Start date and amount of MilaDy** [UNCONFIRMED: divergence between sources, each verified]: the ANR gives 560 612 €, January 2026, 48 months; Ponty's CV gives “550k€” and “2026 (février) – 2030”; Cheng's home page gives “2025–2029” and his Research page “Start: 2026”. Retain the ANR values.
- **Suffix “-02”** [UNCONFIRMED]: “ANR-25-CE51-0077-02” appears in the acknowledgements of Bousquet 2026 and in the Crossref “funder” metadata of Bousquet 2026 and of Botez 2026. It is probably a partner agreement number, but the partner is not identified.
- **Name of the MilaDy postdoc at the OCA** [UNCONFIRMED, but probable]: Ponty's CV writes “Hiroshi Hiiro”. The HAL record hal-05796131, funded by ANR-25-CE51-0077, has “Hiroshi Horii” as co-author, whom HAL attaches to the Observatoire de la Côte d'Azur and to the Université Côte d'Azur. “Hiiro” is therefore probably a typo in the CV, but no OCA page confirms it.
- **Recruitment of the LISN postdoc** [UNCONFIRMED]: identity not found. The announcement is now commented out in Lucor's page, which suggests that the position is filled or the offer closed.
- **MaDICS** [UNCONFIRMED]: no MaDICS page mentioning MilaDy (web search redone on 6/11/2026).
- **Page of the 2026 offer on the LISN site** [UNCONFIRMED]: page not opened. The content is verified in the ENS PDF (Offre-30818), which says “in spring 2026”.
- **Article by Botez, Bousquet, Nore in the Journal of Computational Physics (2026, “In press, 559”)** [UNCONFIRMED]: absent from Crossref (search by authors since 2025) and from HAL. Only the Magnetohydrodynamics 61 (2025) version is confirmed.
- **Status of Caroline Nore**: “Pr. UPS” in the postdoc PDF and “Pr. Caroline Nore” in the internship offers [verified in these documents]; institutional page not opened [UNCONFIRMED].
- **Figures of Lucor et al. 2022** (Ra = 2·10⁹, errors of 0.3 to 4%, 1.6% of the data) [UNCONFIRMED in the JCP version]: verified only in the abstract of the arXiv preprint arXiv:2103.03565.
- **Figures of Botez et al. 2026** (Poincaré number, Rm_c) [UNCONFIRMED]: PDF inaccessible (HAL anti-bot, APS), no figure extracted. The abstract is verified.
- **Credit of the SFEMaNS headers to Guermond and Nore** [UNCONFIRMED]: headers not seen (the main.f90 page of the documentation does not show them). The attachment of the code to Nore's team is, however, verified: “our massively parallel research code SFEMaNS” (Nore–Lucor M2 offer) and the JCP articles 2007, 2009 and 2011.
- **Availability of experimental VKS or DRESDYN data for assimilation** [UNCONFIRMED].

**Points resolved during the cross-check**:
- Attachment of Nore to the COMET team of the LISN: confirmed by the HAL structures of the three MilaDy articles and of CPC 2025 [verified].
- Cappanera et al. 2016 (PRE 93, 043113): abstract read via OpenAlex and added in §4.2 no. 8 [verified].
- Ponty & Plunian 2011: the arXiv abstract arXiv:2004.11028 carries the reference PRL 106, 154502 (2011); content retained [verified].
- Absence of a Ponty publication on machine learning: arXiv and HAL searches redone, 0 results. Do not attribute AI work to him [verified].
