# Datasets, evaluation metrics and prior art for distribution-level ("in law") constraints

Fact base for the M2 MilaDy internship (CEREA/ENPC, LISN): conditional generative models of MHD/dynamo fields.
Search carried out on 2026-11-06. Independent verification carried out on 2026-11-06 (see summary below).

## Verification summary

Method: each DOI was re-queried in the Crossref API (70 DOIs) and each arXiv identifier in the arXiv API (59 identifiers). The PDFs of the sources from which specific content is cited were downloaded and re-read: The Well, PDEBench, Lemoine 2022, Sejdinovic 2013, Kolouri 2019, Lienen 2024, GenCFD, GenCast, Behme–Schnurr, WGS, Khalifa 2021, Gorham 2019, Tauberschmidt, Wu 2020, Guan 2023, Chattopadhyay v1 and v2, DySLIM, Tao 2013, Bastek, Botvinick-Greenhouse, Young 2002, Amrouche–Seloula 2011. The publisher pages opened are PMLR, JMLR, NeurIPS, ICLR, OpenReview, the dataset pages of The Well and the HAL record.

- **Entries verified without change: 132** (`[verified]` tags)
- **Entries corrected or completed: 27** (`[corrected: …]` tags)
- **Unconfirmed entries: 5** (`[UNCONFIRMED]` tags, grouped in the final section "Unconfirmed")

Important corrections:
1. **Sejdinovic et al. 2013**: the energy distance is not equal to the MMD. It equals **D_E = 2 γ_k²**, i.e. twice the squared MMD for the distance-induced kernel (eq. of § 4, PDF l. 679).
2. **Leray projection (Tao 2013)**: the quotation is faithful to the arXiv PDF, but the printed formula P u := Δ⁻¹(∇×∇×u) has a **sign error** with the usual Laplacian. Since ∇×∇× = ∇∇· − Δ, the correct formula is **P = −Δ⁻¹∇×∇× = I − ∇Δ⁻¹∇·**. The remark "amounts to the same formula" was therefore false.
3. **Tauberschmidt et al. (arXiv:2508.09156)**: the paper is **published at ICLR 2026** (PDF v3 header), whereas the entry said "without venue". The experiments also include Stokes (lid-driven cavity), guidance on sparse observations and natural images. The reward is built on the mean of the squared weak residuals.
4. **WGS (Cai et al.)**: the paper is **published in SIAM J. Sci. Comput. 48(4):C708–C735 (2026)**, DOI 10.1137/24M1665271, whereas the entry said "no journal publication". It also contains an example in d = 10.
5. **Botvinick-Greenhouse et al. 2023**: the Markov matrix derived from an upwind discretization of the continuity equation belongs to Yang et al. 2023 (their ref. 18). Botvinick-Greenhouse **replace** it with the stationary Fokker–Planck equation.
6. **Lienen et al. 2024**: the metrics are in **§ 6.3**, not in § 4. W2,R applies to the normalized **velocity, vorticity and pressure**, not only to velocity and pressure.
7. **Young 2002, zero-noise limit**: the selection of the SRB measure by the zero-noise limit is established only in the **Axiom A setting** (Thm 1). Young writes (§ 2.3) that there is "no general result" beyond it, and that not all zero-noise limits are SRB. The caveats of § 3.6 were qualified accordingly.
8. **Published versions omitted**:
   - Giorgini et al.: PRL 133:267302 (2024);
   - Giorgini: PRE 114:L012102 (2026);
   - Del Felice & Giorgini: Chaos 36:063143 (2026);
   - PINN-IMSM: Physica D 496:135326 (2026);
   - Oommen et al.: Proc. R. Soc. A 481:20240819 (2025);
   - Kohl et al.: Neural Networks 199:108641 (2026);
   - GenCFD: Nat. Commun. 17:9846 (2026), with a new title and B. Raonić as first author;
   - Martin et al.: ApJS 277(2):48 (2025);
   - Chattopadhyay et al.: Environ. Data Sci. 2:e1 (2023);
   - Boffi & Vanden-Eijnden: MLST 4:035012 (2023).
9. **JHTDB mhd1024**: a second source that uses the database (Jafari, arXiv:2605.11305) gives a pseudo-spectral code, Re_λ ≈ 186, ν = η = 1.1×10⁻⁴ and **Taylor–Green forcing at k_f = 2**. This last point **contradicts** the "random force" of Lemoine (2022). This discrepancy is flagged in "Unconfirmed".
10. **Moved from "unconfirmed" to "verified"**:
    - the ICLR 2024 venue of Universal Guidance (OpenReview);
    - Khalafi et al. at NeurIPS 2024 (DOI 10.52202/079017-0836, pp. 26543–26576);
    - Jiang et al. at NeurIPS 2023 (OpenReview);
    - the Christensen 2009 erratum: PEPI 172:356, DOI 10.1016/j.pepi.2008.09.014, where E_kin of case 1 is 30.773 ± 0.020 and not 30.733.
11. Minor corrections:
    - the references to cite for the MHD datasets of The Well are [142, 149, 146, 150];
    - the author's name is N. Seloula, not "N. El Houda Seloula";
    - the full title of Peyré & Cuturi is given;
    - the BSMSE and BSNMSE metrics of The Well were added;
    - the ICML 2023 venue of FP-Diffusion was added.

**Legend**
- `[verified]`: primary source opened by the verifier (Crossref/arXiv API, publisher page, PDF) and consistent. When only the bibliographic record was checked, this is stated ("metadata").
- `[corrected: old → new]`: error or omission corrected in place.
- `[UNCONFIRMED]`: not found or inaccessible in a primary source. These entries are grouped in the final section.
- Passages marked **(synthesis)** or **(derivation)** are reasoning by the author of this entry and not sourced facts. Writers must present them as such.

---

## 1. Datasets

### 1.1 The Well (Ohana et al., NeurIPS 2024 Datasets & Benchmarks)

**Reference.** R. Ohana, M. McCabe, L. Meyer, R. Morel, F. J. Agocs, M. Beneitez, M. Berger, B. Burkhart, K. Burns, S. B. Dalziel, D. B. Fielding, D. Fortunato, J. A. Goldberg, K. Hirashima, Y.-F. Jiang, R. R. Kerswell, S. Maddu, J. Miller, P. Mukhopadhyay, S. S. Nixon, J. Shen, R. Watteaux, B. Régaldo-Saint Blancard, F. Rozet, L. H. Parker, M. Cranmer, S. Ho, "The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning", NeurIPS 2024, Track on Datasets and Benchmarks. arXiv:2412.00568 (v1 2024-11-30, v2 2025-02-21). https://arxiv.org/abs/2412.00568 ; PDF v2: https://arxiv.org/pdf/2412.00568v2 `[verified]` (27 authors, dates and arXiv comment consistent)

General facts (PDF v2):
- 15 TB, 16 datasets (abstract; § "Format"). `[verified]`
- HDF5 format, arrays `(n_traj, n_steps, coord1, coord2, (coord3))` in fp32; scalar, vector and tensor fields distinguished; random train/test/val split = 0.8/0.1/0.1 × n_traj (§ "Format"). `[verified]`
- Table 1: row `MHD | (x,y,z) | 64³ and 256³ | n_steps = 100 | n_traj = 100`. `[verified]`
- Size table (appendix): `MHD_256 : 4580 GB, 48 h, 64 C (cores), Fortran MPI` ; `MHD_64 : 72 GB` (no cost of its own: downsampled). `[verified]`

**MHD_64 / MHD_256** (PDF v2, § 3.1.7 and appendix C.7; pages https://polymathic-ai.org/the_well/datasets/MHD_64/ and https://polymathic-ai.org/the_well/datasets/MHD_256/):
- Physics: **compressible isothermal** MHD turbulence, without self-gravity ("such as found in the diffuse ISM"). `[verified]`
- Scheme: "third-order-accurate hybrid essentially non-oscillatory (ENO) scheme" for the **ideal MHD equations** (appendix C.7): `[verified]`
  - ∂ρ/∂t + ∇·(ρv) = 0 (eq. 21)
  - ∂(ρv)/∂t + ∇·[ρvv + (p + B²/8π) I − BB/4π] = f (eq. 22)
  - ∂B/∂t − ∇×(v×B) = 0 (eq. 23)
  - Isothermal equation of state p = c_s² ρ; forcing f: "random large-scale solenoidal driving at a wave number k ≈ 2.5 (i.e., 1/2.5 of the box size), with continuous driving".
  - The dataset web page gives a simplified form without forcing or 4π factors (∂(ρv)/∂t + ∇·(ρvv − BB) + ∇p = 0).
- Boundary conditions: periodic; uniform Cartesian grid; "uniform IC" initial conditions (web pages). `[verified]`
- Control parameters (appendix C.7: "Ms ≡ |v|/cs, and MA ≡ |v|/⟨vA⟩ … ⟨·⟩ signifies averages over the entire simulation box"): sonic Mach number M_s and Alfvén Mach number M_A. `[verified]`
  - Values: **M_s ∈ {0.5, 0.7, 1.5, 2.0, 7.0}**, **M_A ∈ {0.7, 2.0}**, i.e. 10 combinations × 10 initial conditions = **100 trajectories** (web pages: "10 Initial conditions x 10 combination of parameters").
  - Appendix C.7: sub-Alfvénic regime M_A ≈ 0.7 (strong field) or super-Alfvénic M_A = 2.0. In the super-Alfvénic runs, "the initial Alfvén Mach number … is 7.0, but after the small-scale dynamo saturates, the final M_A value is around 2".
- Time: 100 stored steps, Δt = 0.01 (arbitrary units), t ∈ [0, 1] (web pages). `[verified]`
- Resolution: generated at 256³; MHD_64 = downsampling to 64³ "after anti-aliasing with an ideal low-pass filter". `[verified]`
- Fields: density (scalar), velocity (vector), magnetic field (vector). `[verified]`
- Sizes: MHD_256 = 4.58 TB (page) / 4580 GB (table); MHD_64 = 71.6 GB (page) / 72 GB (table). `[verified]`
- Cost: 48 h per simulation on 64 CPU cores (Fortran + MPI); appendix C.7: "On 64 CPU cores, it takes 48 hours per simulation". `[verified]`
- Domain expert: Blakesley Burkhart (CCA, Flatiron Institute & Rutgers University). References to cite (appendix C.7): [142] Cho & Lazarian 2003, MNRAS 345:325–339; [149] Burkhart, Falceta-Gonçalves, Kowal, Lazarian 2009, ApJ 693:250–266; [146] Portillo & Finkbeiner 2018, ApJ 862:119; [150] CATS (Burkhart et al. 2020, see § 1.4). The web pages ask only for CATS. `[corrected: "CATS and Cho & Lazarian 2003" → full list [142, 149, 146, 150] of appendix C.7]`
- Metrics suggested by the MHD_256 page: "Power spectrum, two points correlation function". `[verified]`
- Baselines: `[verified]`
  - Table 2, one-step VRMSE on the test set, for MHD_64: FNO 0.3605, TFNO 0.3561, U-net 0.1798, **CNextU-net 0.1633**. The web page displays "3561" for TFNO: this is a typo.
  - Table 3, mean VRMSE per window 6:12 / 13:30, for MHD_64: FNO 1.24/1.61, TFNO 1.25/1.81, U-net 1.65/4.66, CNextU-net 1.30/2.23.
  - Values above 1 are worse than predicting the mean. Table captions: "predicting the mean value of the target field results in a score of 1".
- **Note for the internship (synthesis)**: these datasets are parametrized by (M_s, M_A), not by (Re, Rm). The equations solved are ideal, with purely numerical dissipation. For a parametric study in Re/Rm, one must produce one's own data or use other databases. Appendix C.7 mentions a small-scale dynamo in the super-Alfvénic runs.

**Metrics provided by The Well** (PDF v2, appendix E.3): `[corrected: BSMSE/BSNMSE added; Fig. 6 uses BSNMSE]`
- Pointwise errors:
  - MSE and RMSE;
  - NMSE = ⟨|u−v|²⟩/(⟨|u|²⟩+ε), with ε = 10⁻⁷, and NRMSE;
  - VMSE = ⟨|u−v|²⟩/(⟨|u−ū|²⟩+ε), and **VRMSE** = √VMSE. We have VRMSE(u, ū) ≈ 1: predicting the spatial mean gives 1;
  - L∞.
- Spectral metrics:
  - **BSMSE_B** = ⟨|u_B − v_B|²⟩, where u_B = F⁻¹[F[u] 1_B] and B is one of 3 wavenumber bands uniformly spaced on a log scale;
  - **BSNMSE_B** = ⟨|u_B − v_B|²⟩/⟨|v_B|²⟩, normalized by the band energy. This is the one used by Fig. 6: "we divide the isotropic power spectrum into three bins whose boundaries are evenly distributed in log space and evaluate the growth of RMSE per bin normalized by the true bin energy".

Other datasets of The Well with a magnetic field: `post_neutron_star_merger` ("general relativistic equations of ideal magnetohydrodynamics", νbhlight code). Size table: 110 GB. `[verified]`

### 1.2 PDEBench (Takamoto et al., NeurIPS 2022 D&B)

**Reference.** M. Takamoto, T. Praditia, R. Leiteritz, D. MacKinlay, F. Alesiani, D. Pflüger, M. Niepert, "PDEBench: An Extensive Benchmark for Scientific Machine Learning", NeurIPS 2022 Datasets and Benchmarks Track. arXiv:2210.07182 (v1 2022-10-13; v7 2024-08-26). https://arxiv.org/abs/2210.07182 `[verified]`

- Table 1 (11 rows): `[verified]`
  - 1D advection (1024, 200 steps, 10 000 samples);
  - 1D Burgers (1024, 200, 10 000);
  - 1D diffusion-reaction (1024, 200, 10 000) and 2D (128², 100, 1000);
  - 1D diffusion-sorption (1024, 100, 10 000);
  - compressible Navier–Stokes 1D (1024, 100, 10 000), 2D (512², 21, 1000) and 3D (128³, 21, 100);
  - incompressible Navier–Stokes 2D (256², 1000, 1000);
  - stationary 2D Darcy (128², 10 000);
  - 2D shallow water (128², 100, 1000).
  - **No MHD dataset.**
- Metrics (§ 4 and appendix B): `[verified]`
  - RMSE;
  - nRMSE = ‖u_pred − u_true‖₂ / ‖u_true‖₂;
  - max error;
  - **cRMSE**, the deviation on a conserved quantity;
  - **bRMSE**, the boundary error;
  - **fRMSE** in Fourier space by bands: "Low: kmin = 0, kmax = 4, Middle: kmin = 5, kmax = 12, and High: kmin = 13, kmax = ∞" (appendix B, eq. 5). In multi-D, |F[u_pred − u_true](k)|² is integrated over the angular coordinate and then summed in k.
- Baselines: FNO, U-Net, PINN, gradient-based inverse method (abstract). `[verified]`

### 1.3 JHTDB: forced 1024³ MHD turbulence ("mhd1024")

- Facts verified in a primary source that uses the database: M. Lemoine, "First-principles Fermi acceleration in magnetized turbulence", Phys. Rev. Lett. 129, 215101 (2022), DOI 10.1103/PhysRevLett.129.215101, arXiv:2210.01038, **appendix B** (PDF re-read) `[verified]`:
  - "direct numerical simulation of **incompressible MHD** on a **periodic grid containing 1 024³ cells**, sampled on **1 024 time steps**";
  - "visco-resistive, with magnetic Reynolds number at the Taylor scale ≃ 140, and magnetic Prandtl number unity";
  - snapshots archived "after the simulation has reached a statistically stationary state";
  - forcing: "external random force acting on velocity fluctuations on a stirring scale equal to 0.5 in units of the size of the simulation box";
  - "There is no guide field".
- Second source that uses the database: A. Jafari, "Non-Dynamic Alignment in Magnetohydrodynamic Turbulence", arXiv:2605.11305 (2026), § 3.1.1, PDF read. According to it, this is a "forced, periodic, pseudospectral full-MHD … with no imposed uniform guide field" simulation, with "Taylor-scale Reynolds number Re_λ ≃ 186", "ν = η = 1.1 × 10⁻⁴", "Taylor–Green forcing at k_f = 2" and Re_b = b′L_b/η = 764. `[corrected: second source added; the forcing type diverges from Lemoine, see "Unconfirmed"]`
- Reference of the database cited by Lemoine ([42]): G. Eyink, E. Vishniac, C. Lalescu, H. Aluie, K. Kanov, K. Bürger, R. Burns, C. Meneveau, A. Szalay, "Flux-freezing breakdown in high-conductivity magnetohydrodynamic turbulence", Nature 497(7450):466–469 (2013), https://doi.org/10.1038/nature12128 `[verified]`.
- Reference paper of the JHTDB cluster: Y. Li, E. Perlman, M. Wan, Y. Yang, C. Meneveau, R. Burns, S. Chen, A. Szalay, G. Eyink, "A public turbulence database cluster and applications to study Lagrangian evolution of velocity increments in turbulence", J. Turbulence 9, N31 (2008), https://doi.org/10.1080/14685240802376389 `[verified]`.
- The official README (https://turbulence.idies.jhu.edu/docs/mhd/README-MHD.pdf) still returns HTTP 503 (WebFetch), and the server's TLS chain fails with curl. See "Unconfirmed".

### 1.4 CATS (Catalogue for Astrophysical Turbulence Simulations)

B. Burkhart, S. M. Appel, S. Bialy, J. Cho, A. J. Christensen, D. Collins, C. Federrath, D. B. Fielding, D. Finkbeiner, A. S. Hill, J. C. Ibáñez-Mejía, M. R. Krumholz, A. Lazarian, M. Li, P. Mocz, M.-M. Mac Low, J. Naiman, S. K. N. Portillo, B. Shane, Z. Slepian, Y. Yuan, "The Catalogue for Astrophysical Turbulence Simulations (CATS)", ApJ 905(1):14 (2020), https://doi.org/10.3847/1538-4357/abc484 ; arXiv:2010.11227 `[verified]`.
- Content (arXiv abstract): box MHD turbulence simulations produced with the public codes athena++, arepo, enzo and flash; synthetic observational products (turbulent HI cubes); power spectra and 3-point correlation functions for part of the data. Site: www.mhdturbulence.com. The MHD pages of The Well point to CATS as the associated paper. `[verified]`

### 1.5 Numerical dynamo benchmarks (reference values, not ML datasets)

- U. R. Christensen, J. Aubert, P. Cardin, E. Dormy, S. Gibbons, G. A. Glatzmaier, E. Grote, Y. Honkura, C. Jones, M. Kono, M. Matsushima, A. Sakuraba, F. Takahashi, A. Tilgner, J. Wicht, K. Zhang, "A numerical dynamo benchmark", Phys. Earth Planet. Inter. 128(1–4):25–34 (2001), https://doi.org/10.1016/S0031-9201(01)00275-8 `[verified]`. Erratum: "Erratum to "A numerical dynamo benchmark"", PEPI 172:356 (2009), https://doi.org/10.1016/j.pepi.2008.09.014. Its HAL record insu-00447063 was read via the HAL API: "Table 4 … contains a typographical error. In case 1 the correct value for the kinetic energy Ekin is 30.773 ± 0.020 (not 30.733 ± 0.020)". `[corrected: erratum "found by search but not opened" → full reference and content verified]`
- C. A. Jones, P. Boronski, A. S. Brun, G. A. Glatzmaier, T. Gastine, M. S. Miesch, J. Wicht, "Anelastic convection-driven dynamo benchmarks", Icarus 216(1):120–135 (2011), https://doi.org/10.1016/j.icarus.2011.08.014 `[verified]`.
- H. Matsui et al. (37 authors, including J.-L. Guermond), "Performance benchmarks for a next generation numerical dynamo model", Geochem. Geophys. Geosyst. 17(5):1586–1607 (2016), https://doi.org/10.1002/2015GC006159 `[verified]` (37 authors counted in Crossref).

### 1.6 Other generative MHD work (data produced, useful as comparison)

- S. Kacmaz, E. A. Huerta, R. Haas, "Resolving Turbulent Magnetohydrodynamics: A Hybrid Operator-Diffusion Framework", Mach. Learn.: Sci. Technol. 6, 035057 (2025), DOI 10.1088/2632-2153/ae054c, arXiv:2507.02106 `[verified]`.
  - This is **2D resistive incompressible** MHD. The method combines a PINO and a conditional diffusion for the high-frequency residuals.
  - The training set covers **Re ∈ {100, 250, 500, 750, 1000, 3000, 10000}**.
  - The model reproduces the spectral energy distributions of velocity and magnetic field at Re = 1000 and 3000 (abstract).
  - Public availability of the data was not verified: see "Unconfirmed".
- J. Martin, J. Lübke, T. Li, M. Buzzicotti, R. Grauer, L. Biferale, "Generation of Cosmic-Ray Trajectories by a Diffusion Model Trained on Test Particles in 3D Magnetohydrodynamic Turbulence", ApJS 277(2):48 (2025), https://doi.org/10.3847/1538-4365/adb432, arXiv:2412.12923. Metrics: velocity increments, spatial transport, curvature statistics. `[corrected: "accepted ApJS according to arXiv comment" → published ApJS 277(2):48, 2025]`
- C. Pedersen, L. Zanna, J. Bruna, "Thermalizer: Stable autoregressive neural emulation of spatiotemporal chaos", arXiv:2503.18731, ICML 2025 (poster, OpenReview) `[verified]`.
  - A diffusion model trained on the **invariant measure** serves as an implicit score estimator. It makes it possible to "thermalize" (denoise) an autoregressive emulator online.
  - The stability horizon is extended "by an order of magnitude" (abstract).

---

## 2. Metrics for generative models of physical fields

### 2.1 Deterministic errors (reference, poorly suited to generation)
VRMSE and NRMSE (The Well, § 1.1), nRMSE/cRMSE/bRMSE/fRMSE (PDEBench, § 1.2). **(synthesis)** For samples from a distribution, these pointwise errors are dominated by the intrinsic variance. They must be replaced by distances between distributions and physical statistics (§ 2.2–2.8).

### 2.2 Energy spectra and "spectral error"
- Reference works: U. Frisch, *Turbulence: The Legacy of A. N. Kolmogorov*, CUP (1995), https://doi.org/10.1017/CBO9781139170666 `[verified]`; D. Biskamp, *Magnetohydrodynamic Turbulence*, CUP (2003), https://doi.org/10.1017/CBO9780511535222 `[verified]`.
- Published variants of the spectral error:
  - The Well: BSNMSE per band (3 log-uniform bands), normalized by the true band energy (appendix E.3 and Fig. 6, arXiv:2412.00568v2) `[verified]`.
  - PDEBench: fRMSE low/mid/high (bands k ∈ [0,4], [5,12], [13,∞), appendix B) `[verified]`.
  - Lienen et al. (ICLR 2024): L2 distance between **turbulent kinetic energy (TKE) log-spectra**, then W₂ between sets of samples ("W2,TKE"), § 6.3 eq. (7) and appendix E (see § 2.6) `[corrected: § 4 → § 6.3]`.
  - Chattopadhyay & Hassanzadeh: spectral regularization (§ 3.5).
  - GenCast (Price et al., Nature 637(8044):84–90, 2025, https://doi.org/10.1038/s41586-024-08252-9 ; arXiv:2312.15796): comparison of the spatial power spectra of the samples to ERA5 (Fig. 2, panels g and m) `[verified]`.
- G. Kohl, L.-W. Chen, N. Thuerey, "Benchmarking Autoregressive Conditional Diffusion Models for Turbulent Flow Simulation", Neural Networks 199:108641 (2026), https://doi.org/10.1016/j.neunet.2026.108641, arXiv:2309.01745: evaluates "accuracy, posterior sampling, spectral behavior, and temporal stability" on 3 2D cases (incompressible, transonic, isotropic turbulence). `[corrected: arXiv only → published in Neural Networks 199:108641 (2026)]`
- V. Oommen, A. Bora, Z. Zhang, G. E. Karniadakis, "Integrating neural operators with diffusion models improves spectral representation in turbulence modeling", Proc. R. Soc. A 481(2309):20240819 (2025), https://doi.org/10.1098/rspa.2024.0819, arXiv:2409.08477: diffusion conditioned by a neural operator to correct the spectral bias; validated on a high-Re jet and on Schlieren velocimetry. `[corrected: arXiv only → published Proc. R. Soc. A 481:20240819 (2025)]`

### 2.3 Increment PDFs, structure functions, flatness
- K41 framework and intermittency: Frisch (1995), above.
- MHD: H. Politano, A. Pouquet, "von Kármán–Howarth equation for magnetohydrodynamics and its consequences on third-order longitudinal structure and correlation functions", Phys. Rev. E 57(1):R21–R24 (1998), https://doi.org/10.1103/PhysRevE.57.R21 `[verified]` (metadata; exact order-3 laws for the Elsässer variables: content not re-read).
- Use for a diffusion model: T. Li, L. Biferale, F. Bonaccorso, M. A. Scarpolini, M. Buzzicotti, "Synthetic Lagrangian turbulence by generative diffusion models", Nat. Mach. Intell. 6(4):393–403 (2024), https://doi.org/10.1038/s42256-024-00810-0, arXiv:2307.08529 `[verified]`.
  - The abstract says the model reproduces "the fat-tail distribution for velocity increments, the anomalous power law, and the increased intermittency around the dissipative scale".
  - Discrepancies remain below the dissipative scale (acceleration, flatness).

### 2.4 Helicities (kinetic, magnetic, cross)
Usual definitions: H_K = ∫ u·ω dV ; H_M = ∫ A·B dV (B = ∇×A) ; H_C = ∫ u·B dV.
- H. K. Moffatt, "The degree of knottedness of tangled vortex lines", J. Fluid Mech. 35(1):117–129 (1969), https://doi.org/10.1017/S0022112069000991 `[verified]`.
- L. Woltjer, "A theorem on force-free magnetic fields", PNAS 44(6):489–491 (1958), https://doi.org/10.1073/pnas.44.6.489 `[verified]` (invariant ∫A·B in ideal MHD; metadata).
- M. A. Berger, G. B. Field, "The topological properties of magnetic helicity", J. Fluid Mech. 147:133–148 (1984), https://doi.org/10.1017/S0022112084002019 `[verified]`. Abstract read via Crossref: "There exists no absolute measure of the helicity within a subvolume of space if that subvolume is not bounded by a magnetic surface. However, a topologically meaningful and gauge-invariant relative measure of helicity for such volumes is presented here".
- H. K. Moffatt, R. L. Ricca, "Helicity and the Călugăreanu invariant", Proc. R. Soc. Lond. A 439(1906):411–429 (1992), https://doi.org/10.1098/rspa.1992.0159 `[verified]`.
- **(synthesis, supported by the Berger & Field abstract)** H_M is gauge-invariant only if the volume is bounded by a magnetic surface (B·n = 0 at the boundary). If flux leaves the bounded domain, the relative helicity must be used. `[verified]`

### 2.5 Divergence (∇·B, ∇·u)
- Effect of a numerical ∇·B ≠ 0: J. U. Brackbill, D. C. Barnes, "The Effect of Nonzero ∇·B on the numerical solution of the magnetohydrodynamic equations", J. Comput. Phys. 35(3):426–430 (1980), https://doi.org/10.1016/0021-9991(80)90079-0 `[verified]`; G. Tóth, "The ∇·B=0 Constraint in Shock-Capturing Magnetohydrodynamics Codes", J. Comput. Phys. 161(2):605–652 (2000), https://doi.org/10.1006/jcph.2000.6519 `[verified]`.
- **(synthesis)** Possible nondimensional metric: ‖∇·B‖₂ / (‖∇B‖₂) or ‖∇·B‖₂ · Δx / ‖B‖₂. It must be computed with **the same discrete operator** as that of the projection (spectral or finite differences), otherwise the truncation error dominates.

### 2.6 Distances between distributions
- **MMD**: A. Gretton, K. M. Borgwardt, M. J. Rasch, B. Schölkopf, A. Smola, "A Kernel Two-Sample Test", JMLR 13(25):723–773 (2012), https://jmlr.org/papers/v13/gretton12a.html `[verified]`. γ_k²(P,Q) = E k(Z,Z′) + E k(W,W′) − 2E k(Z,W) (form recalled by Sejdinovic et al. 2013, eq. (3.3), PDF re-read) `[verified]`.
- **Energy distance (Székely)**: G. J. Székely, M. L. Rizzo, "Energy statistics: A class of statistics based on distances", J. Stat. Plan. Inference 143(8):1249–1272 (2013), https://doi.org/10.1016/j.jspi.2013.03.018 `[verified]`. Definition D_E(P,Q) = 2E‖Z−W‖₂ − E‖Z−Z′‖₂ − E‖W−W′‖₂ (eq. 2.3 of Sejdinovic et al.) `[verified]`.
- **Link MMD ↔ energy distance**: D. Sejdinovic, B. Sriperumbudur, A. Gretton, K. Fukumizu, "Equivalence of distance-based and RKHS-based statistics in hypothesis testing", Ann. Statist. 41(5):2263–2291 (2013), https://doi.org/10.1214/13-AOS1140, arXiv:1207.6076 (PDF re-read). For a "distance kernel" k induced by the semimetric ρ, we have **D_{E,ρ}(P,Q) = 2 γ_k²(P,Q)**: the energy distance equals twice the square of the MMD. `[corrected: "the MMD … coincides exactly with the energy distance" → D_E = 2·MMD² (equality up to a factor 2, squared MMD)]`
- **Wasserstein**: C. Villani, *Optimal Transport: Old and New*, Grundlehren der math. Wiss., Springer (2009), https://doi.org/10.1007/978-3-540-71050-9 `[verified]`; G. Peyré, M. Cuturi, "Computational Optimal Transport: With Applications to Data Science", Found. Trends Mach. Learn. 11(5–6):355–607 (2019), https://doi.org/10.1561/2200000073 `[corrected: abridged title → full title with subtitle]`.
- **Sliced Wasserstein**: `[verified]`
  - References: J. Rabin, G. Peyré, J. Delon, M. Bernot, "Wasserstein Barycenter and Its Application to Texture Mixing", SSVM 2011, LNCS pp. 435–446 (2012), https://doi.org/10.1007/978-3-642-24785-9_37 ; N. Bonneel, J. Rabin, G. Peyré, H. Pfister, "Sliced and Radon Wasserstein Barycenters of Measures", J. Math. Imaging Vis. 51(1):22–45 (2015), https://doi.org/10.1007/s10851-014-0506-3.
  - Definition: SW_p(μ,ν) = (∫_{S^{d−1}} W_p^p(Rμ(·,θ), Rν(·,θ)) dθ)^{1/p}, via the Radon transform. It is computed by Monte Carlo over the directions θ, with closed-form 1D transport problems.
  - Source of the definition: Kolouri, Nadjahi, Şimşekli, Badeau, Rohde, "Generalized Sliced Wasserstein Distances", arXiv:1902.00434, eq. (7) (PDF re-read).
- **Sinkhorn divergence** (between OT and MMD): J. Feydy, T. Séjourné, F.-X. Vialard, S. Amari, A. Trouvé, G. Peyré, "Interpolating between Optimal Transport and MMD using Sinkhorn Divergences", arXiv:1810.08278 `[verified]`. Used as an evaluation metric in DySLIM (Fig. 1b, Lorenz 63; DySLIM cites Genevay et al. 2018) `[verified]`.
- **KID** (MMD on descriptors): Bińkowski, Sutherland, Arbel, Gretton, "Demystifying MMD GANs", ICLR 2018, arXiv:1801.01401 `[verified]`.
- Uses in generative turbulence:
  - Lienen, Lüdke, Hansen-Palmus, Günnemann, "From Zero to Turbulence: Generative Modeling for 3D Flow Simulation", ICLR 2024, arXiv:2306.01776 (PDF re-read, § 6.3 and appendix E). The paper proposes two new metrics:
    - **W2,TKE**: W₂ between sets, with the L2 distance between TKE log-spectra as cost, computed by blocks (eq. 7, 9, 10);
    - **W2,R**: W₂ between sets of normalized values of **velocity, vorticity and pressure** per cell. The homogeneous regions are obtained by k-means on Gaussian approximations of the velocity marginals (eq. 8).
    - Motivation: FID-type metrics rely on learned embeddings, and the Euclidean distance is unsuited to turbulent fields.
    - `[corrected: "§ 4" → "§ 6.3"; "velocity+pressure" → "velocity, vorticity and pressure"]`
  - GenCFD: Molinaro, Lanthaler, Raonić et al., "Generative AI for fast and accurate statistical computation of fluids", arXiv:2409.18359, § 6.9 re-read. `[corrected: arXiv only → published version: B. Raonić, R. Molinaro, S. Lanthaler et al. (author order changed), "Generative AI for efficient statistical computation of fluids", Nat. Commun. 17:9846 (2026), https://doi.org/10.1038/s41467-026-76390-x]` § 6.9 of the arXiv version defines:
    - the L2 error on the mean, e_μ (eq. 78);
    - the L2 error on the standard deviation, e_σ, normalized (eq. 79);
    - the **1-point W_s** over M points, computed via inverse cumulative distribution functions (eq. 80);
    - the ensemble CRPS (eq. 81–83).

### 2.7 Probabilistic scores (CRPS, energy score)
- J. E. Matheson, R. L. Winkler, "Scoring Rules for Continuous Probability Distributions", Manag. Sci. 22(10):1087–1096 (1976), https://doi.org/10.1287/mnsc.22.10.1087 `[verified]`.
- T. Gneiting, A. E. Raftery, "Strictly Proper Scoring Rules, Prediction, and Estimation", JASA 102(477):359–378 (2007), https://doi.org/10.1198/016214506000001437 `[verified]` (metadata; standard reference for CRPS and the multivariate energy score, cited as such by GenCast § E.2.1; content not re-read).
- H. Hersbach, "Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems", Weather Forecast. 15(5):559–570 (2000), https://doi.org/10.1175/1520-0434(2000)015<0559:DOTCRP>2.0.CO;2 `[verified]`.
- C. A. T. Ferro, "Fair scores for ensemble forecasts", Q. J. R. Meteorol. Soc. 140(683):1917–1923 (2014), https://doi.org/10.1002/qj.2270 `[verified]`.
- Ensemble estimator used in GenCast (arXiv:2312.15796, appendix E.2.1, eq. E1, re-read): `[verified]`
  - CRPS = (1/M)Σ_m |x_m − y| − (1/(2M²)) Σ_{m,m′} |x_m − x_m′|, averaged over the grid points weighted by a_i and over the dates.
  - GenCast uses the "traditional" estimator and not the "fair CRPS".
  - Key figure: GenCast is "significantly more skillful (p < 0.05) than ENS's on **97.4%** of our **1320** variable, lead time, and vertical level combinations" (Fig. 3).

### 2.8 Topological metrics
**Persistent homology (foundations)**
- H. Edelsbrunner, D. Letscher, A. Zomorodian, "Topological Persistence and Simplification", Discrete Comput. Geom. 28(4):511–533 (2002), https://doi.org/10.1007/s00454-002-2885-2 `[verified]`.
- A. Zomorodian, G. Carlsson, "Computing Persistent Homology", Discrete Comput. Geom. 33(2):249–274 (2005), https://doi.org/10.1007/s00454-004-1146-y `[verified]`.
- D. Cohen-Steiner, H. Edelsbrunner, J. Harer, "Stability of Persistence Diagrams", Discrete Comput. Geom. 37(1):103–120 (2007), https://doi.org/10.1007/s00454-006-1276-5 `[verified]` (stability of diagrams: basis for using bottleneck/Wasserstein between diagrams as a metric).
- R. J. Adler, O. Bobrowski, M. S. Borman, E. Subag, S. Weinberger, "Persistent homology for random fields and complexes", IMS Collections 6:124–143 (2010), https://doi.org/10.1214/10-IMSCOLL609 `[verified]`.
- H. Adams et al., "Persistence Images: A Stable Vector Representation of Persistent Homology", JMLR 18(8):1–35 (2017), arXiv:1507.06217 `[verified]`.
- Software: C. Maria, J.-D. Boissonnat, M. Glisse, M. Yvinec, "The Gudhi Library: Simplicial Complexes and Persistent Homology", ICMS 2014, LNCS pp. 167–174, https://doi.org/10.1007/978-3-662-44199-2_28 `[verified]`.

**Applications to physical fields**
- M. Kramár, R. Levanger, J. Tithof, B. Suri, M. Xu, M. Paul, M. F. Schatz, K. Mischaikow, "Analysis of Kolmogorov flow and Rayleigh–Bénard convection using persistent homology", Physica D 334:82–98 (2016), https://doi.org/10.1016/j.physd.2016.02.003 `[verified]`.
- P. Pranav, H. Edelsbrunner, R. van de Weygaert, G. Vegter, M. Kerber, B. J. T. Jones, M. Wintraecken, "The topology of the cosmic web in terms of persistent Betti numbers", MNRAS 465(4):4281–4310 (2017), https://doi.org/10.1093/mnras/stw2862 `[verified]`.
- **MHD**: I. Makarenko, A. Shukurov, R. Henderson, L. F. S. Rodrigues, P. Bushby, A. Fletcher, "Topological signatures of interstellar magnetic fields – I. Betti numbers and persistence diagrams", MNRAS 475(2):1843–1858 (2018), https://doi.org/10.1093/mnras/stx3337, arXiv:1708.04558 `[verified]`.
  - TDA (Betti numbers, persistence diagrams) is applied to the density of an MHD simulation of the multiphase interstellar medium **with dynamo action**.
  - TDA is "sensitive to all statistical moments".
  - It detects the effect of the magnetic field beyond correlation analysis: the field makes the ISM more homogeneous, with fewer isolated clouds and cavities (abstract).
- I. Makarenko, P. Bushby, A. Fletcher, R. Henderson, N. Makarenko, A. Shukurov, "Topological data analysis and diagnostics of compressible magnetohydrodynamic turbulence", J. Plasma Phys. 84(4):735840403 (2018), https://doi.org/10.1017/S0022377818000752 `[verified]`.
- R. Henderson, I. Makarenko, P. Bushby, A. Fletcher, A. Shukurov, "Statistical Topology and the Random Interstellar Medium", JASA 115(530):625–635 (2020), https://doi.org/10.1080/01621459.2019.1647841 `[verified]`.
- B. A. Carreras, I. Llerena, L. Garcia, I. Calvo, "Topological characterization of flow structures in resistive pressure-gradient-driven turbulence", Phys. Rev. E 78, 066402 (2008), arXiv:0811.3548 `[verified]` (the PDF uses Betti numbers and contains no occurrence of "persistence").

**TDA as a metric for generative models**
- V. Khrulkov, I. Oseledets, "Geometry Score: A Method For Comparing Generative Adversarial Networks", ICML 2018, arXiv:1802.02664 `[verified]`.
- S. Barannikov et al., "Manifold Topology Divergence: a Framework for Comparing Data Manifolds", NeurIPS 2021, arXiv:2106.04024 `[verified]`.

**Magnetic topology: null points, skeleton, connectivity**
- C. E. Parnell, J. M. Smith, T. Neukirch, E. R. Priest, "The structure of three-dimensional magnetic neutral points", Phys. Plasmas 3(3):759–770 (1996), https://doi.org/10.1063/1.871810 `[verified]`.
- J. M. Greene, "Locating three-dimensional roots by a bisection method", J. Comput. Phys. 98(2):194–198 (1992), https://doi.org/10.1016/0021-9991(92)90137-N `[verified]`.
- A. L. Haynes, C. E. Parnell, "A trilinear method for finding null points in a three-dimensional vector space", Phys. Plasmas 14(8):082107 (2007), https://doi.org/10.1063/1.2756751 `[verified]`.
- A. L. Haynes, C. E. Parnell, "A method for finding three-dimensional magnetic skeletons", Phys. Plasmas 17(9):092903 (2010), https://doi.org/10.1063/1.3467499 `[verified]`.
- V. S. Titov, G. Hornig, P. Démoulin, "Theory of magnetic connectivity in the solar corona", J. Geophys. Res. 107(A8) (2002), https://doi.org/10.1029/2001JA000278 `[verified]` (the abstract describes "strongly squashed" flux tubes, hence the "squashing factor" Q).

### 2.9 Proposed evaluation battery (synthesis)
For each condition (parameters p) and N generated samples vs N reference samples:
1. 1-point statistics: 1-point W₁ (GenCFD), mean/standard deviation;
2. spectra E_u(k), E_B(k), spectral helicity, log-spectral error by bands (The Well / PDEBench / Lienen);
3. increment PDFs δ_ℓu, δ_ℓB and flatness F(ℓ) (Frisch; Li et al. 2024);
4. integrated invariants: energy, H_K, H_M (Coulomb gauge, periodic domain), H_C, then distance between their distributions (CRPS or W₁);
5. normalized ‖∇·B‖ (same discrete operator);
6. global distances: MMD/energy (linked by D_E = 2·MMD², Sejdinovic 2013), sliced-W₂ on fields or descriptors;
7. topology: persistence diagrams of |B|, |ω| or J·B (Wasserstein distance between diagrams, Cohen-Steiner stability); number and type of null points (Haynes–Parnell).

---

## 3. Prior art: imposing a physical constraint on the generated **law**

### 3.0 Statement of the idea and mathematical foundation
Idea to be situated: "the constraint on the law of a statistically stationary state is the weak form of the stationary Liouville / Fokker–Planck equation, E_μ[F·∇φ + (σ²/2)Δφ] = 0 for every test function φ; the energy balance is the case φ = energy; it is imposed on a conditional generative model by exponential tilting at sampling time (I-projection) or by a stationarity-discrepancy loss".

Established facts:
- **Generator criterion ↔ invariance.** `[verified]`
  - Quotation: "a probability measure µ on R^d is invariant … for the Feller process X … if and only if ∫ Af(x) µ(dx) = 0 holds for all f in a core of the generator A". This is Thm 3.37 of Liggett, *Continuous Time Markov Processes* (2010), cited by A. Behme, A. Schnurr, "A criterion for invariant measures of Itô processes based on the symbol", Bernoulli 21(3):1697–1718, 2015, DOI 10.3150/14-BEJ618, arXiv:1310.4333 (§ 1, PDF re-read).
  - The same authors note that, for general Markov processes, **necessity** still holds (Ethier–Kurtz, Prop. 9.2). **Sufficiency**, however, requires additional assumptions (Echeverría 1982; Bhatt–Karandikar 1993).
  - A measure that satisfies only the condition is called "infinitesimal invariant".
  - P. Echeverría, "A criterion for invariant measures of Markov processes", Z. Wahrscheinlichkeitstheorie verw. Gebiete 61(1):1–16 (1982), https://doi.org/10.1007/BF00537221 `[verified]` (metadata; text not consulted).
  - S. N. Ethier, T. G. Kurtz, *Markov Processes: Characterization and Convergence*, Wiley (1986), https://doi.org/10.1002/9780470316658 `[verified]`.
  - V. Bogachev, N. Krylov, M. Röckner, S. Shaposhnikov, *Fokker–Planck–Kolmogorov Equations*, AMS Math. Surveys Monogr. 207 (2015), https://doi.org/10.1090/surv/207 `[verified]` (reference [1] of WGS for the weak form, checked in the WGS bibliography).
- **Exact weak form (published).** `[verified]`
  - For dX = b dt + √2 σ dW, with D = σσᵀ: ⟨L*φ, p⟩ = 0 ∀φ ∈ C_c^∞, where **L*φ = b·∇φ + D:∇∇φ** is "the infinitesimal generator of the stochastic process". Source: Cai, Cao, Huang, Zhou, WGS, eq. (1), (2), (6) (PDF re-read).
  - With isotropic additive noise dX = F dt + s dW, we have D = s²/2 and L*φ = F·∇φ + (s²/2)Δφ: this is exactly the formula of the idea.
- **Deterministic and dissipative case (σ = 0).** L. S. Young, "What Are SRB Measures, and Which Dynamical Systems Have Them?", J. Stat. Phys. 108(5–6):733–754 (2002), https://doi.org/10.1023/A:1019762724717 (text re-read, the author's PDF). What the text says:
  - "SRB measures are the invariant measures most compatible with volume when volume is not preserved";
  - near an attractor, the map is often volume-contracting, "ruling out the possibility of an invariant measure equivalent to volume";
  - the SRB measure has a density along the unstable directions but is "usually singular with respect to Lebesgue measure" in the stable direction;
  - the support of a genuinely contracting attractor has zero Lebesgue measure;
  - the SRB measure is the **zero-noise limit** of small random perturbations (Thm 1 (iv)), **in the Axiom A setting only**. Outside this setting, Young writes (§ 2.3): "it is conceivable that under suitable conditions, SRB measures are stochastically stable … but as of now there is no general result to that effect. Evidently, not all zero-noise limits are SRB".
  - `[corrected: Axiom A restriction and § 2.3 caveat added]`
  - **(synthesis)** Consequence: for turbulence and the dynamo, the Liouville equation is expected to have no density solution. Only the **weak form** (tests φ) therefore makes sense, which supports the proposed formulation.
- **Non-uniqueness.** DySLIM (PDF re-read, note 4 of § 3): "We note that invariant measures may not be unique". `[verified]`
  - **(synthesis)** E_μ[F·∇φ] = 0 ∀φ is satisfied by every invariant measure (fixed points, unstable periodic orbits). The stationarity constraint therefore does not select the physical measure.
  - It must be combined with a data-fidelity term, or go through the low-noise limit. This selection is guaranteed only in the Axiom A setting (Young 2002, Thm 1 and § 2.3).
  - Botvinick-Greenhouse et al. moreover model with Fokker–Planck (D > 0) rather than with the continuity equation (contribution 1 of their introduction) `[verified]`.
- **Energy balance as a special case (derivation, unsourced).** `[verified: calculation redone, no source]`
  - For forced incompressible Navier–Stokes/MHD: F(u,B) = (−P[(u·∇)u − (∇×B)×B] + νΔu + f, ∇×(u×B) + ηΔB).
  - With φ = E = ½∫(|u|²+|B|²) and zero noise: F·∇φ = dE/dt = ∫u·f − ν∫|∇u|² − η∫|∇B|² (periodic domain).
  - The verifier redid the computation: ∫u·(u·∇)u = 0; the Lorentz term ∫u·((∇×B)×B) and the induction term ∫B·∇×(u×B) = −∫u·((∇×B)×B) cancel.
  - The condition E_μ[F·∇E] = 0 is therefore written "mean injection = mean dissipation".
  - With white stochastic forcing of covariance Q, the Itô term (s²/2)·tr(Q) is added, which is the noise injection rate.
  - With φ = H_M (periodic domain, no magnetic forcing), one obtains E_μ[−2η ∫ J·B] = 0.
  - **These formulas remain derivations to be written up by the authors. No source states them in this form.**

### 3.1 (a) I-projection and maximum entropy → exponential tilting
- E. T. Jaynes, "Information Theory and Statistical Mechanics", Phys. Rev. 106(4):620–630 (1957), https://doi.org/10.1103/PhysRev.106.620 `[verified]`.
- I. Csiszár, "I-Divergence Geometry of Probability Distributions and Minimization Problems", Ann. Probab. 3(1):146–158 (1975), https://doi.org/10.1214/aop/1176996454 `[verified]`. Metadata and abstract read via Crossref: "The minimum discrimination information problem is viewed as that of projecting a PD onto a convex set of PD's … existence theorems for and characterizations of the minimizing PD". Full text not accessible.
- Statement verified in Khalifa et al. (ICLR 2021, § 2.1 and appendix A.1, PDF re-read) `[verified]`:
  - for nonempty C = {c : E_c[φ_i] = μ̄_i}, the problem p = argmin_{c∈C} KL(c‖a) has a unique solution **p(x) ∝ a(x) 1[x∈X_C] exp(Σ_i λ_i φ_i(x))** (exponential-family form, Thm 1(A));
  - the Pythagorean identity KL(c‖a) = KL(c‖p) + KL(p‖a) holds ∀c ∈ C (Thm 1(C));
  - Thm 1 restates Remark 3.1 (p. 444) and Thm 3.2 (p. 442) of Csiszár & Shields (2004), which assume X finite; "generalizations to infinite (countable and/or continuous) X spaces are possible, see (Csiszar, 1975)";
  - the case a = uniform recovers Jaynes' MaxEnt.
- Practical computation of the λ (Khalifa et al., Algorithm 1) `[verified]`:
  - sample x_j ~ a;
  - compute the weights w_j = exp(λ·φ(x_j)) and the self-normalized moments μ̂(λ) = Σ w_j φ(x_j)/Σ w_j;
  - fit λ by SGD on ‖μ̄ − μ̂(λ)‖².
  - **(synthesis)** This is self-normalized importance sampling, directly applicable to a field generator.
- **Precedent in molecular simulation**: J. W. Pitera, J. D. Chodera, "On the Use of Experimental Observations to Bias Simulated Ensembles", J. Chem. Theory Comput. 8(10):3445–3451 (2012), https://doi.org/10.1021/ct300112v `[verified]` (metadata; MaxEnt bias of a simulated ensemble to reproduce experimental means: content not re-read).

### 3.2 (b) Stein discrepancy and the generator approach
- A. D. Barbour, "Stein's method and Poisson process convergence", J. Appl. Probab. 25(A):175–184 (1988), https://doi.org/10.2307/3214155 `[verified]`; A. D. Barbour, "Stein's method for diffusion approximations", Probab. Theory Relat. Fields 84(3):297–322 (1990), https://doi.org/10.1007/BF01197887 `[verified]`.
- J. Gorham, L. Mackey, "Measuring Sample Quality with Stein's Method", Advances in NeurIPS 28 (NIPS 2015), https://proceedings.neurips.cc/paper/2015/hash/698d51a19d8a121ce581499d7b701668-Abstract.html (page opened; the official BibTeX has no pages); arXiv:1506.03039 `[verified]`. Computable measure: sup, over a class of test functions, of the gap between expectations under the sample and under the target.
- J. Gorham, A. B. Duncan, S. J. Vollmer, L. Mackey, "Measuring sample quality with diffusions", Ann. Appl. Probab. 29(5):2884–2928 (2019), https://doi.org/10.1214/19-AAP1467, arXiv:1611.06972 (§ 2.1 re-read) `[verified]`:
  - "generator method construction of Barbour and Götze": if Z_t is a Feller process with invariant measure P, its generator A satisfies E_P[(Au)(Z)] = 0;
  - the diffusion Stein operator is (T g)(x) = (1/p(x))⟨∇, p(x)(a(x)+c(x)) g(x)⟩ (eq. 8);
  - it depends on P **"only through ∇ log p"**.
- Q. Liu, J. Lee, M. Jordan, "A Kernelized Stein Discrepancy for Goodness-of-fit Tests", ICML 2016, PMLR 48:276–284, https://proceedings.mlr.press/v48/liub16.html `[verified]`.
- K. Chwialkowski, H. Strathmann, A. Gretton, "A Kernel Test of Goodness of Fit", ICML 2016, PMLR 48:2606–2615, https://proceedings.mlr.press/v48/chwialkowski16.html `[verified]`.
- **Difference from the idea (synthesis)**:
  - Classical Stein discrepancies test a sample Q against a **target P known through its score**, and build an ad hoc generator that leaves P invariant.
  - In the MilaDy idea, the target density is unknown, but the **physical generator A (PDE) is known**. One tests whether the generated law is invariant for A, by means of a "stationarity discrepancy" sup_φ |E_μθ[Aφ]|.
  - This is the form used by WAN (in min-max) and WGS (with random test functions), see § 3.3.

### 3.3 (c) Learning the dynamics or the law via the invariant measure
- **Yang et al. 2023**: Y. Yang, L. Nurbekyan, E. Negrini, R. Martin, M. Pasha, "Optimal Transport for Parameter Identification of Chaotic Dynamics via Invariant Measures", SIAM J. Appl. Dyn. Syst. 22(1):269–310 (2023), https://doi.org/10.1137/21M1421337, arXiv:2104.15138 `[verified]`.
  - The Wasserstein distance serves as the gap between physical measures.
  - The measures are approximated as fixed points of Perron–Frobenius operators discretized by PDE. According to Botvinick-Greenhouse et al., this is the Markov matrix of an upwind finite-volume discretization of the continuity equation.
- **Botvinick-Greenhouse, Martin, Yang 2023**: "Learning dynamics on invariant measures using PDE-constrained optimization", Chaos 33(6):063152, https://doi.org/10.1063/5.0149673, arXiv:2301.05193 (PDF re-read). `[corrected: the "Markov matrix from an upwind finite-volume discretization of the continuity equation" is the earlier approach of Yang et al. (their ref. 18); Botvinick-Greenhouse et al. replace it with the stationary Fokker–Planck equation]`
  - The learning of ODEs/SDEs from invariant measures is reformulated there as **PDE-constrained optimization**.
  - The forward model is the stationary **Fokker–Planck equation**. It replaces the continuity equation of Yang et al. and reduces to it when D = 0.
  - Tests: Van der Pol, Lorenz-63, Hall-effect thruster, temperature.
- **Jiang, Lu, Orlova, Willett 2023**: "Training neural operators to preserve invariant measures of chaotic attractors", NeurIPS 2023 (OpenReview: "NeurIPS 2023 poster"), arXiv:2306.01187 `[verified]`. Two approaches: (1) an optimal transport loss between statistics chosen by expertise; (2) contrastive learning without prior knowledge, almost as good.
- **DySLIM**: Y. Schiff, Z. Y. Wan, J. B. Parker, S. Hoyer, V. Kuleshov, F. Sha, L. Zepeda-Núñez, "DySLIM: Dynamics Stable Learning by Invariant Measure for Chaotic Systems", ICML 2024, PMLR 235:43649–43684, https://proceedings.mlr.press/v235/schiff24b.html, arXiv:2402.04467 (PDF re-read) `[verified]`.
  - Regularized objective L_λD(θ) = L(θ) + λ D(μ*, μ*_θ) (eq. 9), with **D = MMD** (Gretton 2012), in conditional and unconditional versions.
  - The invariant measure is approximated by unrolling trajectories.
  - Systems: Lorenz 63, Kuramoto–Sivashinsky, Kolmogorov flow.
  - Additional cost: "quadratically on the batch size" (note 3).
  - Code: github.com/google-research/swirl-dynamics.
- **WGS, the closest prior art to the "stationarity-discrepancy loss"**: Z. Cai, Y. Cao, Y. Huang, X. Zhou, "Weak Generative Sampler to Efficiently Sample Invariant Distribution of Stochastic Differential Equation", **SIAM J. Sci. Comput. 48(4):C708–C735 (2026)**, https://doi.org/10.1137/24M1665271 ; arXiv:2405.19256 (v1 2024-05-29, v2 2025-06-05), PDF re-read. `[corrected: "no journal publication found" → published SIAM J. Sci. Comput. 48(4):C708–C735 (2026); d = 10 example added]`
  - "randomized weak loss" loss: **min_θ E_{φ∼P} ( E_{z∼ρ} [L*φ(G_θ(z))] )²** (eq. 8–10), L*φ = b·∇φ + D:∇∇φ;
  - test functions: Gaussian kernels, adaptive centers tied to the generated samples; the randomization avoids the min-max (eq. 7);
  - generator: normalizing flow (Real NVP), but "neither the computationally intensive calculation of the Jacobian determinant nor the invertibility" is required;
  - examples: 2D unimodal (§ 4.1), 2D bistable (§ 4.2), Lorenz (§ 4.3), problem in **d = 10** (§ 4.4), problems of dimension **d = 40 and d = 100** (§ 4.5).
  - Min-max precedent: Y. Zang, G. Bao, X. Ye, H. Zhou, "Weak adversarial networks for high-dimensional partial differential equations", J. Comput. Phys. 411:109409 (2020), https://doi.org/10.1016/j.jcp.2020.109409 `[verified]`.
- **PINN-IMSM**: Y. Chen, S. Das, W. Guo, X. Zhong, "Physics-informed machine learning for reconstruction of dynamical systems with invariant measure score matching", Physica D 496:135326 (2026), https://doi.org/10.1016/j.physd.2026.135326 ; arXiv:2601.12675 (2026-01-19). `[corrected: arXiv only → published Physica D 496:135326 (2026)]`
  - The invariant density satisfies the stationary Fokker–Planck equation, written with the score. The score is learned by denoising score matching.
  - A PINN then reconstructs the drift.
  - The tests go up to 5 dimensions: Van der Pol, active swimmer, Lorenz-63, Lorenz-96.
- **Score and effective Langevin dynamics** (Giorgini et al.): `[corrected: published versions added]`
  - L. T. Giorgini, K. Deck, T. Bischoff, A. Souza, "Response Theory via Generative Score Modeling", PRL 133(26):267302 (2024), https://doi.org/10.1103/PhysRevLett.133.267302, arXiv:2402.01029. Combines a score model and the generalized fluctuation-dissipation theorem.
  - L. T. Giorgini, "Score-Based Modeling of Effective Langevin Dynamics", PRE 114(1):L012102 (2026), https://doi.org/10.1103/6qpv-lqmt, arXiv:2505.01895.
  - L. T. Giorgini, "Score-based stochastic reduced-order models of barotropic quasi-geostrophic turbulence", arXiv:2609.34028 (2026) `[verified]` (no published version found).
  - G. Del Felice, L. T. Giorgini, "Integrating score-based generative modeling and neural ODEs for accurate representation of multiscale chaotic dynamics", Chaos 36(6):063143 (2026), https://doi.org/10.1063/5.0326565, arXiv:2511.03862. Langevin equation whose drift is informed by a score (KGMM) to reproduce the invariant measure, plus a NODE for the fast forcing.
- Thermalizer (Pedersen, Zanna, Bruna, ICML 2025), § 1.6. `[verified]`

### 3.4 (d) Guidance, tilting and alignment at sampling time
- **Classifier guidance**: P. Dhariwal, A. Nichol, "Diffusion Models Beat GANs on Image Synthesis", NeurIPS 2021, arXiv:2105.05233 `[verified]` (FID 2.97 on ImageNet 128², 4.59 at 256², 7.72 at 512², abstract).
- **Universal guidance**: A. Bansal, H.-M. Chu, A. Schwarzschild, S. Sengupta, M. Goldblum, J. Geiping, T. Goldstein, "Universal Guidance for Diffusion Models", ICLR 2024 (OpenReview: "ICLR 2024 poster"; also CVPR Workshops 2023), arXiv:2302.07121. `[corrected: venue "according to the offer, unconfirmed" → ICLR 2024 confirmed on OpenReview]`
- **DPS**: H. Chung, J. Kim, M. T. McCann, M. L. Klasky, J. C. Ye, "Diffusion Posterior Sampling for General Noisy Inverse Problems", ICLR 2023, arXiv:2209.14687 `[verified]`.
- **TDS (twisted SMC)**: L. Wu, B. L. Trippe, C. A. Naesseth, D. M. Blei, J. P. Cunningham, "Practical and Asymptotically Exact Conditional Sampling in Diffusion Models", NeurIPS 2023, arXiv:2306.17775 `[verified]`. SMC with "twisting", asymptotically exact; empirical gains "with as few as two particles".
- **FK steering**: R. Singhal, Z. Horvitz, R. Teehan, M. Ren, Z. Yu, K. McKeown, R. Ranganath, "A General Framework for Inference-time Scaling and Steering of Diffusion Models", ICML 2025, PMLR 267:55810–55827, https://proceedings.mlr.press/v267/singhal25b.html, arXiv:2501.06848 `[verified]`. Interacting particles are resampled according to potentials (intermediate rewards). A 0.8 B-parameter model steered by FK outperforms a fine-tuned 2.6 B model (abstract).
- **Adjoint Matching**: C. Domingo-Enrich, M. Drozdzal, B. Karrer, R. T. Q. Chen, "Adjoint Matching: Fine-tuning Flow and Diffusion Generative Models with Memoryless Stochastic Optimal Control", ICLR 2025, arXiv:2409.08861 `[verified]`.
  - Venue: header "Published as a conference paper at ICLR 2025" of the PDF https://proceedings.iclr.cc/paper_files/paper/2025/file/852f50969a9e523ec41d26f2f68bd456-Paper-Conference.pdf.
  - Reward fine-tuning is seen there as a stochastic optimal control problem.
  - A "memoryless" noise schedule is required.
  - The target is the reward-tilted law (confirmed by Tauberschmidt et al., § 3.3).
- **Tilting by weak PDE residual (important prior art)**: J. Tauberschmidt, S. Fellenz, S. J. Vollmer, A. B. Duncan, "Physics-Constrained Fine-Tuning of Flow-Matching Models for Generation and Inverse Problems", **ICLR 2026** (PDF v3 header, 2026-06-30), arXiv:2508.09156, PDF re-read. `[corrected: "2025, no venue given" → ICLR 2026; list of experiments completed; exact form of the residual]`
  - Method: post-training fine-tuning of a flow matching model towards the tilted law **p_r(x) ∝ e^{λ r(x)} p(x)** (§ 3 "Method"), carried out by Adjoint Matching (§ 3.3).
  - Reward (§ 3.1 "Reward"): it is built on the **weak-form** residual R_weak(x, α) = (1/N_test) Σ_i ⟨L_α x, ψ⁽ⁱ⁾⟩²_{L²(Ω)}. The ψ⁽ⁱ⁾ are local polynomial kernels with compact support, whose centers and scales are drawn at random.
  - Experiments: Darcy (§ 4.1), guidance on sparse observations (§ 4.2), plane linear elasticity (§ 4.3), Helmholtz (§ 4.4), lid-driven cavity Stokes (§ 4.5), natural images (§ 4.6). A latent-parameter predictor is used for the inverse problems.
  - **Difference from the MilaDy idea (synthesis)**:
    - In Tauberschmidt et al., the residual is computed **on each sample**: the stationary PDE must be satisfied field by field, and the residual serves as the reward. The weights λ_x, λ_α are hyperparameters.
    - In the MilaDy idea, the constraint E_μ[Aφ] = 0 is **linear in the law**, since it expresses the statistical stationarity of a chaotic dynamics. No sample satisfies it on its own. λ is the multiplier of the I-projection, fixed by the constraint.
    - Vollmer and Duncan are also coauthors of Gorham et al. 2019 (diffusion Stein operators).
- **Distributional (moment) constraints on a pretrained generator: direct prior art of the I-projection applied to a generative model**: M. Khalifa, H. Elsahar, M. Dymetman, "A Distributional Approach to Controlled Text Generation", ICLR 2021, arXiv:2012.11635, PDF re-read `[verified]`.
  - The paper combines "pointwise" and "distributional" constraints E[φ_i] = μ̄_i.
  - It minimizes the KL towards the initial model, which gives an explicit EBM solution (exponential family).
  - This solution is then distilled by "distributional policy gradient".
  - The authors present it as "to our knowledge, the first model with such generality".
- **Diffusion under constraints on the law**: S. Khalafi, D. Ding, A. Ribeiro, "Constrained Diffusion Models via Dual Training", Advances in NeurIPS 37, pp. 26543–26576 (2024), https://doi.org/10.52202/079017-0836, arXiv:2408.15094. `[corrected: DOI and pages "unverified" → confirmed by Crossref; OpenReview "NeurIPS 2024 poster"]`
  - Training is posed as an optimization of the law under constraints (KL) towards target laws.
  - The algorithm is dual (Lagrangian).
  - The optimal law is a mixture.
- **Exponential tilting + moment constraints + FK steering for a simulation emulator (closest on the mechanism)**: J. Mun, "Multifidelity Computer Model Emulation Via Diffusion Model Steering and Targeted Maximum Likelihood", arXiv:2608.30096 (2026-08-31) `[verified]`.
  - The paper seeks "the exponentially tilted high-resolution distribution that minimizes KL divergence from the biased baseline, subject to moment constraints derived from low-resolution simulations".
  - The base is a score-based diffusion model.
  - The tilts are carried out "at inference time" by FK steering.
- **Moment constraints in the sampler**: Z. Yao, D. Paulin, "Training-Free Generative Sampling via Moment-Matched Score Smoothing", arXiv:2605.14276 (2026) `[verified]`. It is a particle system whose stationary limit is a Gibbs–Boltzmann density obtained by **exponential tilting**, with a mean and a covariance equal to the empirical moments.
- C. McDonald, P. Bartlett, "Internal Guidance as a Sampling Method for Tilted Diffusion Models", arXiv:2610.29086 (2026) `[verified]`: "Reward guidance methods sample an exponential tilt of a base density".

### 3.5 (e) Statistical and spectral constraints for turbulence and climate
- **Direct prior art "statistical constraint on a turbulence generator"**: J.-L. Wu, K. Kashinath, A. Albert, D. Chirila, Prabhat, H. Xiao, "Enforcing statistical constraints in generative adversarial networks for modeling chaotic dynamical systems", J. Comput. Phys. 406:109209 (2020), https://doi.org/10.1016/j.jcp.2019.109209, arXiv:1905.06841 (PDF re-read, § 2.2) `[verified]`.
  - Loss: L_c(D,G) = L(D,G) + λ d(Σ(p_data), Σ(p_G)) (eq. 4), where Σ is the **covariance** estimated on the samples.
  - The distance d retained is the Frobenius norm. The symmetrized KL, the Riemannian distance and the JBLD were also compared.
  - Case study: Rayleigh–Bénard convection simulated by lattice Boltzmann.
  - Training time is reduced "by up to 80%" (abstract).
  - The paper notes that Σ(p_data) "can also be estimated from the governing equation".
- **Global balance constraint (enstrophy) in a loss**: Y. Guan, A. Subel, A. Chattopadhyay, P. Hassanzadeh, "Learning physics-constrained subgrid-scale closures in the small-data regime for stable and accurate LES", Physica D 443:133568 (2023), https://doi.org/10.1016/j.physd.2022.133568, arXiv:2201.07347 `[verified]`. The paper compares three approaches, including "loss functions that enforce a **global enstrophy-transfer conservation** (EnsCon)", in a "40x fewer samples" regime. See also Guan, Chattopadhyay, Subel, Hassanzadeh, "Stable a posteriori LES of 2D turbulence using convolutional neural networks…", J. Comput. Phys. 458:111090 (2022), https://doi.org/10.1016/j.jcp.2022.111090 `[verified]`.
- **Spectral regularization**: A. Chattopadhyay, P. Hassanzadeh, arXiv:2304.07029 `[verified]`.
  - Title v1: "Long-term instabilities of deep learning-based digital twins of the climate system: The cause and a solution".
  - Title v2: "Challenges of learning multi-scale dynamics with AI weather models: Implications for stability and one solution" (v2 authors: Chattopadhyay, Y. Q. Sun, Hassanzadeh).
  - Cause identified: the **spectral bias**.
  - FouRKS remedy (PDF v2, § 5.4.1 re-read): a term μ(θ) = Σ_t ‖ X̂(t+Δt)|_{k_x ≥ k_T} − Ĥ[N(X(t),θ)]|_{k_x ≥ k_T} ‖² on the zonal Fourier coefficients, with λ = 0.8 and k_T = 30 (QG) or 40 (ERA5), plus a differentiable RK4 integrator.
  - The v2 abstract announces "hundreds of years of time-integration".
- A. Chattopadhyay, J. Pathak, E. Nabizadeh, W. Bhimji, P. Hassanzadeh, "Long-term stability and generalization of observationally-constrained stochastic data-driven models for geophysical turbulence", Environ. Data Sci. 2:e1 (2023), https://doi.org/10.1017/eds.2022.30, arXiv:2205.04601: stochastic VAE, 2-layer QG, transfer to noisy observations. `[corrected: arXiv only → published Environ. Data Sci. 2:e1 (2023)]`
- FourCastNet: J. Pathak et al., arXiv:2202.11214 `[verified]`. The abstract mentions **no spectral or statistical constraint**: it is a deterministic AFNO emulator at 0.25°. To be cited as context, not as prior art for a constraint on the law.
- **Per-sample constraints (for contrast)**:
  - J.-H. Bastek, W. Sun, D. M. Kochmann, "Physics-Informed Diffusion Models", ICLR 2025, arXiv:2403.14404 (PDF re-read § 3) `[verified]`.
    - The PDE residual is treated as a "virtual observable", evaluated on x̂₀ = E[x₀|x_t].
    - The authors note that R(E[x₀|x_t]) ≠ E[R(x₀)|x_t] and propose DDIM sampling.
    - The residual is reduced "by up to two orders of magnitude" (abstract).
    - This is a constraint on **each sample**.
  - J. Richter-Powell, Y. Lipman, R. T. Q. Chen, "Neural Conservation Laws: A Divergence-Free Perspective", NeurIPS 2022, arXiv:2210.01741 `[verified]`: divergence-free fields by construction (differential forms), universal.
  - A. T. Mohan, N. Lubbers, M. Chertkov, D. Livescu, "Embedding hard physical constraints in neural network coarse-graining of three-dimensional turbulence", Phys. Rev. Fluids 8(1):014604 (2023), https://doi.org/10.1103/PhysRevFluids.8.014604, arXiv:2002.00021 `[verified]`: incompressibility enforced in the CNN (hard constraint), better local mass conservation in 3D turbulence.
- **Fokker–Planck in the diffusion models themselves (not to be confused)**:
  - C.-H. Lai et al., "FP-Diffusion: Improving Score-based Diffusion Models by Enforcing the Underlying Score Fokker-Planck Equation", ICML 2023 (OpenReview), arXiv:2210.04296. The paper imposes the Fokker–Planck PDE of the **noising process** on the learned score, and not a physical stationarity. `[corrected: ICML 2023 venue added]`
  - Z. Shen et al., "Self-Consistency of the Fokker-Planck Equation", COLT 2022, arXiv:2206.00860 `[verified]`.
  - N. M. Boffi, E. Vanden-Eijnden, "Probability flow solution of the Fokker–Planck equation", Mach. Learn.: Sci. Technol. 4(3):035012 (2023), https://doi.org/10.1088/2632-2153/ace2aa, arXiv:2206.04642. Solution of **time-dependent** Fokker–Planck PDEs by probability flow. `[corrected: arXiv only → published MLST 4:035012 (2023)]`

### 3.6 Summary: what is published, what appears new

| Building block of the idea | Already published (evidence) |
|---|---|
| Invariance ⟺ E_μ[Aφ] = 0 for φ in a core | Yes: Liggett Thm 3.37 via Behme–Schnurr 2015; Echeverría 1982; Ethier–Kurtz 1986. Sufficiency is delicate outside the Feller setting. |
| Weak form of the stationary Fokker–Planck equation as the **loss of a sample generator** | **Yes**: WGS (Cai et al., SIAM J. Sci. Comput. 2026), loss E_φ(E_z[L*φ(G_θ(z))])², random Gaussian test functions, d ≤ 100; min-max WAN (Zang et al. 2020). |
| Learning via the invariant measure (OT, MMD, PDE constraint) | Yes: Yang et al. 2023, Botvinick-Greenhouse et al. 2023, Jiang et al. 2023, DySLIM 2024, PINN-IMSM 2026. |
| I-projection / MaxEnt → exponential tilting on a **pretrained generator** | Yes: Khalifa et al. 2021 (language); Pitera–Chodera 2012 (molecular ensembles); Khalafi et al. 2024 (diffusion, KL constraints). |
| Exponential tilting under moment constraints, carried out **at inference** in a diffusion model by FK steering, for **simulation** outputs | Yes, very recent: Mun (arXiv:2608.30096, August 2026); tools: TDS 2023, FK steering 2025, adjoint matching. |
| Statistical constraints (covariance, spectrum, global balance) on a turbulence generator or emulator | Yes: Wu et al. 2020 (covariance, GAN); Guan et al. 2023 (EnsCon); Chattopadhyay–Hassanzadeh (spectrum); Lienen 2024 / GenCFD (evaluation on the law). |
| Constraint on each sample (PDE residual, ∇·u = 0) | Yes: Bastek et al. 2025, Richter-Powell et al. 2022, Mohan et al. 2023 (FunDiff, Fukami–Taira: treated elsewhere). |
| Exponential tilting of a flow matching model by a **weak-form PDE residual** (per-sample reward) via Adjoint Matching | **Yes**: Tauberschmidt, Fellenz, Vollmer, Duncan, ICLR 2026 (arXiv:2508.09156). |

(Table re-read against the verified entries above; WGS and Tauberschmidt updated.) `[corrected: WGS and Tauberschmidt venues updated in the table]`

**What appears new (synthesis, subject to further monitoring; no publication found combining these elements):** see also "Unconfirmed".
1. Taking as constraint functional the **physical generator of a field PDE** (Navier–Stokes/MHD, F(u,B) with Leray projection, possibly stochastic forcing) and not a low-dimensional SDE. WGS stops at d = 100, PINN-IMSM at 5 and Botvinick-Greenhouse at low-dimensional systems.
2. Applying the constraint **per condition** in a **parametric conditional** generative model (Re, Rm, material properties), with tilting multipliers λ(Re, Rm). The cited works are unconditional or have a non-physical condition.
3. Choosing **physically interpretable** test functions in addition to generic kernels:
   - the energy, which gives the injection = dissipation balance;
   - the helicities, which give the helicity balances;
   - the energy per spectral band, which gives a scale-by-scale balance.
   - The energy balance then appears as the case φ = E of the same identity.
   - Unlike Mun 2026 or Khalifa 2021, the target moments are not external data. They are **identities** (E_μ[Aφ] = 0) that require no target value.
4. Combining the two routes on 3D MHD/dynamo fields: the **stationarity-discrepancy loss at training time** (WGS-type or KSD with a known generator) and the **I-projection at sampling time** (exponential weighting via SMC/FK).

**Caveats to write in the report (synthesis)**
- The constraint is **necessary but not sufficient**, because of the non-uniqueness of invariant measures (DySLIM). Without noise, the selection of the physical measure by the zero-noise limit is established only in the Axiom A setting. Young (2002, § 2.3) states that there is "no general result" beyond it, and that not all zero-noise limits are SRB. The data-fidelity term must therefore be kept. `[corrected: Axiom A nuance added]`
- Liouville in the dissipative regime: the SRB measure is in general singular in the stable directions (Young 2002). No density is therefore expected, and the weak form is the natural formulation.
- Cost: Aφ requires F(u) on each sample (spatial derivatives, nonlocal pressure via Leray) and ∇φ (functional derivative). It is simple for quadratic φ (energy, helicities).
- For a constraint linear in the law (E_μ[g] = 0 with g = Aφ), the I-projection gives exactly p* ∝ p_θ exp(λ g) (Khalifa Thm 1, finite setting; Csiszár 1975 for the continuous case).
- Difference from classical Stein discrepancies: they require the score of the target (Gorham et al. 2019: T depends on P "only through ∇ log p"). Here, the target is unknown and it is the generator that is known.

---

## 4. Leray projection, Helmholtz–Hodge, vector potential

### 4.1 Textbook references and papers
- J. Leray, "Sur le mouvement d'un liquide visqueux emplissant l'espace", Acta Math. 63:193–248 (1934), https://doi.org/10.1007/BF02547354 `[verified]`.
- A. J. Chorin, "Numerical solution of the Navier-Stokes equations", Math. Comp. 22(104):745–762 (1968), https://doi.org/10.1090/S0025-5718-1968-0242392-2 `[verified]` (projection method).
- V. Girault, P.-A. Raviart, *Finite Element Methods for Navier-Stokes Equations*, Springer Series in Computational Mathematics (1986), https://doi.org/10.1007/978-3-642-61623-5 `[verified]`.
- F. Boyer, P. Fabrie, *Mathematical Tools for the Study of the Incompressible Navier-Stokes Equations and Related Models*, Applied Mathematical Sciences, Springer (2013), https://doi.org/10.1007/978-1-4614-5975-0 `[verified]`.
- H. Bhatia, G. Norgard, V. Pascucci, P.-T. Bremer, "The Helmholtz-Hodge Decomposition—A Survey", IEEE TVCG 19(8):1386–1404 (2013), https://doi.org/10.1109/TVCG.2012.316 `[verified]` (metadata only; content not re-read).
- Definition of the Leray projection: T. Tao, "Localisation and compactness properties of the Navier–Stokes global regularity problem", Anal. PDE 6(1):25–107 (2013), https://doi.org/10.2140/apde.2013.6.25, arXiv:1108.1165 (p. 18 re-read, page image checked). `[corrected: the remark "amounts to the same formula" was false; sign corrected]`
  - Tao's text: "P u := Δ⁻¹(∇ × ∇ × u). If u is square-integrable, then P u is the orthogonal projection of u onto the space of square-integrable divergence-free vector fields".
  - **Beware of the sign.** With the usual Laplacian (that of u_t = Δu in Tao), ∇×∇×u = ∇(∇·u) − Δu, hence Δ⁻¹(∇×∇×u) = ∇Δ⁻¹∇·u − u = −P u.
  - The correct formula is **P u = −Δ⁻¹(∇×∇×u) = u − ∇Δ⁻¹(∇·u)**. The same sign error affects his Biot–Savart law (17), which should read u = −Δ⁻¹(∇×ω).
  - **(synthesis)** In Fourier, on a periodic domain: P̂(k) = I − k kᵀ/|k|².

### 4.2 Vector potential in a bounded domain (verified statements)
Source: C. Amrouche, N. Seloula (Nour El Houda Seloula), "L^p-theory for vector potentials and Sobolev's inequalities for vector fields", C. R. Math. Acad. Sci. Paris 349(9–10):529–534 (2011), https://doi.org/10.1016/j.crma.2011.04.008, PDF re-read (https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2011.04.008.pdf). `[corrected: "N. El Houda Seloula" → "N. Seloula" (family name Seloula)]` The Hilbertian case (p = 2) is that of C. Amrouche, C. Bernardi, M. Dauge, V. Girault, "Vector potentials in three-dimensional non-smooth domains", Math. Methods Appl. Sci. 21(9):823–864 (1998), https://doi.org/10.1002/(SICI)1099-1476(199806)21:9<823::AID-MMA976>3.0.CO;2-B `[verified]`.

Setting: Ω ⊂ R³ bounded, connected, of class C^{1,1}, boundary Γ with connected components Γ_0 (exterior), …, Γ_I; J "cuts" Σ_j making Ω° = Ω \ ∪Σ_j simply connected (Ω not necessarily simply connected). `[verified]`
- **Thm 3.1 (no boundary condition)**: u ∈ H^p(div, Ω) satisfies div u = 0 and ⟨u·n, 1⟩_{Γ_i} = 0 for 0 ≤ i ≤ I **if and only if** u = curl ψ₀ with ψ₀ ∈ W^{1,p}(Ω). One can choose div ψ₀ = 0 (Coulomb gauge), with ‖ψ₀‖_{W^{1,p}} ≤ C‖u‖_{L^p}. `[verified]`
- **Thm 3.2 (normal condition on the potential)**: under the same conditions (1), there exists a **unique** ψ with u = curl ψ, **div ψ = 0** in Ω, **ψ·n = 0 on Γ**, ⟨ψ·n, 1⟩_{Σ_j} = 0 (1 ≤ j ≤ J). `[verified]`
- **Thm 3.4 (tangential condition on the potential)**: if div u = 0, **u·n = 0 on Γ** and ⟨u·n, 1⟩_{Σ_j} = 0, there exists a **unique** ψ with u = curl ψ, **div ψ = 0**, **ψ × n = 0 on Γ**, ⟨ψ·n, 1⟩_{Γ_i} = 0 (0 ≤ i ≤ I). `[verified]`
- Kernels (harmonic fields): K_T (div = curl = 0, v·n = 0) of dimension J; K_N (div = curl = 0, v × n = 0) of dimension I; K_T = {0} if J = 0 and K_N = {0} if Γ = Γ_0 (§ 1). `[verified]`
- **(synthesis, use for the internship)**:
  - In the periodic case, take B = ∇×A with ∇·A = 0, which is trivial in Fourier: Â = i k × B̂/|k|², the k = 0 mode being treated separately. The verifier redid the computation: i k × (i k × Â) = |k|² Â when k·Â = 0.
  - In a bounded domain (VKS/SFEMaNS-type dynamo), the choice ψ·n = 0 (Thm 3.2) holds for any B with zero flux through each boundary component.
  - The choice ψ × n = 0 (Thm 3.4) requires B·n = 0 at the boundary, which corresponds to an idealized perfectly conducting wall, and zero flux through the cuts.
  - A generative model that outputs A exactly guarantees ∇·B = 0. The boundary conditions on B then translate into conditions on A according to this framework.
  - Magnetic helicity ∫A·B is gauge-dependent if B·n ≠ 0 (Berger & Field 1984, abstract verified, § 2.4).

---

## 5. Unconfirmed / limitations

- **JHTDB mhd1024, official README** (https://turbulence.idies.jhu.edu/docs/mhd/README-MHD.pdf ; https://turbulence.pha.jhu.edu/Forced_MHD_turbulence.aspx) `[UNCONFIRMED]`
  - The README returns HTTP 503 via WebFetch, and curl fails on the server's TLS chain, even with the proxy's CA bundle.
  - A search engine snippet (unverified) indicates a pseudo-spectral solver in Elsasser formulation, a Kolmogorov scale ≈ 3.3×10⁻³ (velocity) and 2.8×10⁻³ (magnetic), integral scales of 0.56 (velocity) and 0.35 (magnetic), an average over t = 0 to 2.56, and forcing at k = 2 with amplitude 0.25.
  - Only the pseudo-spectral code is corroborated by a primary source (Jafari 2026).
  - **Unresolved discrepancy on the forcing**: Lemoine (2022) writes "external random force acting on velocity fluctuations on a stirring scale equal to 0.5", whereas Jafari (2026) writes "Taylor–Green forcing at k_f = 2". The two are compatible on the scale (k = 2, i.e. half the box), but not on the random or Taylor–Green nature of the forcing.
  - The published Reynolds numbers differ depending on the definition: Rm_λ ≃ 140 (Lemoine), Re_λ ≃ 186 and Re_b = 764 (Jafari). The README must settle this before any citation.
- **Gorham & Mackey 2015, NeurIPS proceedings pages**: "226–234", seen on a bibliographic record. The official NeurIPS BibTeX has an empty `pages` field, and DBLP was inaccessible (anti-bot). `[UNCONFIRMED]`
- **Kacmaz et al. 2025**: public availability of the data not verified. `[UNCONFIRMED]`
- **"New" character of the four points of § 3.6** `[UNCONFIRMED]`
  - The agent's search found no publication combining a field-PDE generator, a parametric conditional generative model and exponential tilting. It covered the arXiv API with the combinations "Stein discrepancy / invariant measure / Liouville / stationary Fokker–Planck / exponential tilting / moment constraints / diffusion model / turbulence / MHD", and an extended web search.
  - The verifier did not find any such combination either during the checks. This is not proof of absence: monitoring must be redone (Google Scholar, OpenReview ICLR/NeurIPS 2026–2027) before final writing.
- **"Continuous" statement of the I-projection (Csiszár 1975)**: only the abstract of Csiszár 1975 was read (existence and characterization of the projection onto a convex set). The explicit form p ∝ a·exp(λ·φ) is verified only in the finite setting (Khalifa Thm 1 / Csiszár & Shields 2004). The extension to the continuous case (fields) rests on Khalifa's remark "generalizations … are possible", with no statement read. `[UNCONFIRMED]`

Content limitations (existing references, metadata verified, text not re-read): Echeverría 1982, Bhatia et al. 2013, Gneiting & Raftery 2007, Politano & Pouquet 1998, Pitera & Chodera 2012, Woltjer 1958. Formulas and interpretations cited "via" other sources are flagged as such in the body text.
