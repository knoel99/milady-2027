# Dynamo physics and toy models: verified fact base

## Verification summary (independent cross-check of 2026-11-06)

- **Method**: all references were cross-checked against Crossref (more than 40 DOIs) and the arXiv API (25 identifiers). The figures were reread in the full text: arXiv PDFs of the cited articles, plus the author or publisher PDFs of VKS 2007 and 2009, Pétrélis & Fauve 2008, Pétrélis 2009, Gissinger 2010, Boisson 2012, Miralles 2013, Nore 2016 and 2018, Karlsruhe 2008, and the Ponty 2016 slides. The SFEMaNS, GHOST, Dedalus, The Well, JETP and Math-Net.Ru web pages were also opened.
- **Gissinger 2012**: equations (1)–(3), fixed points M± and N±, eigenvalues of O and polynomials (13)–(14) recomputed numerically: all exact. The team's RK4 script, rerun, gives the same results (74 reversals at µ = 0.119, etc.).
- **Count**: 103 [verified] marks; 5 corrected entries; 4 [UNCONFIRMED] entries, grouped in §9.
- **Important corrections**:
  1. Kaiser & Tilgner: the file said they consider Cowling's proof "incomplete". In fact, they point out that the proof for the coupled system (meridional ↔ azimuthal, kinematic case) was missing and **provide it**. Reference added: SIAM J. Appl. Math. 74(2), 571–597 (2014).
  2. Yin et al. (pseudo-vacuum): 2021 → **2022**, J. Comput. Phys. **451**, 110866.
  3. Ponomarenko 1973: pp. 775–779 → **775–778** (Crossref), with title and DOI 10.1007/BF00853190.
  4. Rädler & Brandenburg: "volume not rechecked" → PRE **67**, 026401 (2003), confirmed.
  5. Alexakis 2011: "not reread" → result A = B ≃ 2C/5, γ ≃ 0.12 confirmed. **Pitfall added**: his R_M equals √3/η for the ABC 1:1:1.
- **Additions and clarifications**: Pouquet 2019 (ESS **6**(3), 351–369, DOI). Riga: first attempt dated 1986 or 1987 depending on the source; 2×100 kW confirmed by Gailitis 2018. Gissinger: convergence to O for any initial condition only if µ < 0.063. JHTDB: 1024 time steps confirmed (Lemoine 2022), but forcing described differently depending on the source. VKS: 150 l or about 160 L of sodium.
- **No error found** in the other figures: Riga, Karlsruhe, VKS, Nore 2016 and 2018, Kreuzahler, Ponty 2005 and 2007, Bouya & Dormy, Archontis, Tobias, Krstulovic and The Well. The typos noted in Gissinger 2012 ("µ > 1+ν", Γ = 0.1 in Fig. 11) are indeed in arXiv v2.
- **Still unconfirmed** (§9): the "CUBBY" code; secondary JHTDB parameters (official pages returning 503); Riga flow rate 0.67 m³/s; primary reading of Galloway & Frisch (403) and the value of the maximal ABC growth rate.

---

*Research carried out on 2026-11-06 for the MilaDy file (M2 internship CEREA/ENPC–LISN). The facts below were read in the primary source (arXiv PDF, publisher or HAL version, author page), then cross-checked against Crossref metadata (api.crossref.org) for the bibliographic references.*

Conventions:
- **[src]**: URL actually opened (full text read, unless marked "abstract only").
- **⚠**: discrepancy between sources or probable typo in the source. Do not "correct" without flagging it.
- Equation and figure numbers refer to the cited article.
- Everything that could not be verified is in the final section 9 ("Unconfirmed"); §7 groups the discrepancies between sources.
- **[verified]**, **[corrected: old → new]**, **[UNCONFIRMED]**: marks set by the independent verifier (cross-check of 2026-11-06).

---

## 0. Key figures (summary)

| Quantity | Value | Source |
|---|---|---|
| Pm of sodium | "about 10⁻⁵"; Pm = µ0σν = 0.82×10⁻⁵ at 120 °C (ν = 6.78×10⁻⁷ m²/s, ρ = 932 kg/m³, σ = 9.6×10⁶ S/m) | Monchaux 2009; Nore 2018 §2.1 [verified] |
| Riga, 1st self-excitation | 11 Nov. 1999, 2150 rpm, 205 °C, growth rate p₂ = 0.0315 ± 0.0009 s⁻¹, f₂ = 1.326 Hz | Gailitis 2000 [verified; date of 11 Nov. 1999 confirmed by Gailitis 2008] |
| Karlsruhe, design | 52 spin generators, R = 0.85 m, H = 0.71 m, a = 0.21 m; design critical Rm < 10; V̇ = 115–143 m³/h | Müller 2008; Rädler & Brandenburg [verified] |
| VKS, threshold (2007) | Rm_c ≈ 31 (linear fit of ⟨B_y⟩, B_rms); R′m ≈ 35 (linear fit of ⟨B²⟩); ~40 G at 30 % above threshold | Monchaux 2007 PRL [verified] |
| VKS, maximal Re | Re up to 5×10⁶; maximal Rm = 49 (120 °C); 300 kW of motor power | Monchaux 2007; Berhanu 2007 [verified] |
| Gissinger model (chaotic reversals) | µ = 0.119, ν = 0.1, Γ = 0.9; crisis at µ_c ≈ 0.11928 | Gissinger 2012 EPJB [verified] |
| ABC 1:1:1, dynamo windows | 8.9 < Rm < 17.5 (closed); Rm > 27 (open), with Rm = 1/η | Archontis 2003, citing Galloway & Frisch 1984 [verified in Archontis 2003; primary source inaccessible] |
| Ponomarenko | Rm_c = 17.7 (convective instability, radius taken as the scale) | Gailitis & Freibergs 1976, cited by Gailitis 2008 [verified in Gailitis 2008] |
| Taylor–Green, low Pm | Rm_c = 30 (Pm = 1) → 226 (Pm = 0.3) → ≈ 200 (Pm = 0.2) → ≈ 150 in LES (10⁻² ≤ Pm ≤ 10⁻¹) | Ponty 2005 PRL [verified] |

---

## 1. Laboratory dynamos

### 1.1 Riga (Latvia): Ponomarenko-type flow

**Gailitis, Lielausis, Dement'ev, Platacis, Cifersons, Gerbeth, Gundrum, Stefani, Christen, Hänel, Will (2000).** "Detection of a flow induced magnetic field eigenmode in the Riga dynamo facility". *Phys. Rev. Lett.* **84**, 4365–4368. DOI 10.1103/PhysRevLett.84.4365. arXiv:physics/9912026. [verified]
[src] https://arxiv.org/pdf/physics/9912026 ; metadata: https://api.crossref.org/works/10.1103/PhysRevLett.84.4365

- **Contribution**: first detection of a self-excited magnetic eigenmode in a liquid-metal experiment. Campaign from 6 to 11 November 1999. The mode grows slowly for about 15 s and decays at slightly reduced rotation. The measured growth rates and frequencies agree with the numerical predictions.
- **Geometry (Fig. 1)**: D1 = 0.25 m (central helical tube), D2 = 0.43 m (return), D3 = 0.80 m (sodium at rest), L = 2.91 m. Velocity in the central tube "up to the order of 15 m/s". Total sodium: 2 m³. Flow rate up to 0.6 m³/s, provided by a propeller driven by **two 55 kW motors**.
- **Physics**: only the azimuthal mode m = 1 plays a role at the accessible Rm. A low-frequency alternating field, slowly rotating around the axis, is expected.
- **Conductivity**: σ ≈ 10⁷ (Ωm)⁻¹ at 100 °C, hence µ0σ ≈ 10 s/m². For Rm_c = 10, one would need L·v = 1 m²/s.
- **Self-excitation figures** (2150 rpm, T = 205 °C, 2-mode fit on 1500 points taken every 10 ms):
  - amplified mode: A₁ = 0.476 mT, p₁ = −0.0012 ± 0.0003 s⁻¹, f₁ = 0.995 Hz;
  - self-excited mode: **A₂ = 0.133 mT, p₂ = 0.0315 ± 0.0009 s⁻¹, f₂ = 1.326 Hz**.
  - At 1980 rpm: f = 1.1 s⁻¹ and decay rate p = −0.3 s⁻¹.
  - The facility could exceed the threshold by about 20 % in Rm.

**Gailitis et al. (2001).** "Magnetic field saturation in the Riga dynamo experiment". *Phys. Rev. Lett.* **86**, 3024–3027. DOI 10.1103/PhysRevLett.86.3024. arXiv:physics/0010047. [verified]
[src] https://arxiv.org/pdf/physics/0010047

- **Contribution**: 2nd campaign (22–25 July 2000), at lower temperature (higher σ). It is the first study of the saturated regime at Riga.
- **Spontaneous growth**: without external excitation, the field grows exponentially towards t = 130 s, at 1920 min⁻¹. Saturation occurs around t = 240 s.
- **Agreement with predictions**: offset of about 10 % on the growth rate and about 5 % on the frequency. The steel walls, not modelled, increase Rm_c by about 8 % according to 1D calculations.
- **Marginal state**: at 157 °C and 1840 min⁻¹, a mode decays "extremely slowly".
- **Saturation**:
  - B_r reaches 7 mT; B_z is estimated at about 30 mT in the dynamo.
  - Laws (Ωc − 1840 min⁻¹)^β with β = 0.417 (H2), 0.275 (H4), 0.216 (H6), 0.205 (coil).
  - Ohmic losses estimated at about 10 kW. The motor power outside the dynamo follows Ω³.

**Gailitis, Gerbeth, Gundrum, Lielausis, Platacis, Stefani (2008).** "History and results of the Riga dynamo experiments". *C. R. Physique* **9**, 721–728. DOI 10.1016/j.crhy.2008.07.004. arXiv:0807.0305. [verified]
[src] https://arxiv.org/pdf/0807.0305

- **History**: first attempt in 1986 with a "helical labyrinth", with no self-excitation observed [verified; ⚠ the PRL 2000 and Gailitis et al. 2018 (J. Plasma Phys. 84, 735840301, arXiv:1801.01749) date this attempt to 1987]. Installation at Salaspils between 1995 and 1999. Eight campaigns in total, including February–March 2005 and July 2007.
- **Measured fields**: in 2005, B goes from 27 mT at 2000 rpm to 120 mT at 2500 rpm at the upper sensor.
- ⚠ Fig. 1 of this article: "Two 100 kW motors". The PRL 2000 states "two 55 kW motors" (the motorization was probably changed in between). [verified; Gailitis et al. 2018 writes "two DC-motors, which can be driven up to 200 kW"]

### 1.2 Karlsruhe: two-scale dynamo (Roberts–Busse)

**Stieglitz & Müller (2001).** "Experimental demonstration of a homogeneous two-scale dynamo". *Phys. Fluids* **13**(3), 561–564. DOI 10.1063/1.1331315. [verified: Crossref metadata and abstract]
[src] metadata and abstract: https://api.crossref.org/works/10.1063/1.1331315 ; publisher page https://pubs.aip.org/aip/pof/article/13/3/561/450962 (paywalled full text, not read)

- **Contribution**: experimental realization of Busse's concept (1975), which takes up G.O. Roberts's periodic flow with a second scale for a finite domain. The abstract confirms dynamo action, without giving figures.

**Müller, Stieglitz, Busse, Tilgner (2008).** "The Karlsruhe two-scale dynamo experiment". *C. R. Physique* **9**, 729–740. DOI 10.1016/j.crhy.2008.07.005. [verified]
[src] https://comptes-rendus.academie-sciences.fr/physique/item/10.1016/j.crhy.2008.07.005.pdf

- **Busse criterion**: Re_mC·Re_mH > 4π²(H/a)[1 + 1.149(H/R)²], with Re_mH = u_H a/λ and Re_mC = u_C a/λ.
- **Optimization**: critical Rm "less than 10", i.e. V̇_C = V̇_H = 115–143 m³/h. Parameters: Z = 52 vortex generators, a = 0.21 m, h = 0.19 m, r = 0.055 m, R/H = 1.21, χ = 3.7 turns.
- **Materials and operation**: stainless steel module; 120 °C < T < 125 °C; λ ≈ 0.1 m²/s. Three independent loops, each with an MHD pump of flow rate up to 150 m³/h (two helical loops, one axial). Ambient field below 0.5 G.
- **Results**:
  - stationary saturated field of dipole type; two nearly equivalent dipolar states (imperfect bifurcation);
  - at V̇ = 115 m³/h: mean B_Y = 260 G, RMS = 0.58 G, i.e. about 0.2 % fluctuations;
  - share of Joule dissipation in the total dissipation close to 50 % at the highest flow rates;
  - axial velocity reduced by about 17 % beyond V̇_H ≈ 106 m³/h.

**Rädler & Brandenburg (2003)**, mean-field theory for the Karlsruhe module. arXiv:physics/0208023; *Phys. Rev. E* **67**(2), 026401 (2003), DOI 10.1103/PhysRevE.67.026401. [corrected: "publication announced, volume not rechecked" → reference confirmed by Crossref and by the arXiv journal-ref]
[src] https://arxiv.org/pdf/physics/0208023

- **Dimensions**: R = 0.85 m, H = 0.71 m, a = 0.21 m, h = 0.19 m, r₁/a = 0.25, r₂/a = 0.5, η = 0.1 m²/s.
- **History**: first successful operation in **December 1999**, "a few weeks" after Riga.
- **Link with Roberts**: the Roberts flow is periodic in x and y (period 2a) and independent of z.

### 1.3 VKS (von Kármán Sodium, CEA Cadarache)

**Monchaux, Berhanu, Bourgoin, Moulin, Odier, Pinton, Volk, Fauve, Mordant, Pétrélis, Chiffaudel, Daviaud, Dubrulle, Gasquet, Marié, Ravelet (2007).** "Generation of a magnetic field by dynamo action in a turbulent flow of liquid sodium". *Phys. Rev. Lett.* **98**, 044502. DOI 10.1103/PhysRevLett.98.044502. arXiv:physics/0701075 (16 authors). [verified]
[src] https://www.phys.ens.fr/~petrelis/pdf/P1PRL_98_044502.pdf

- **Contribution**: first dynamo in a strongly turbulent flow, where the fluctuations and the mean flow have comparable energies.
- **Geometry**:
  - discs of radius 154.5 mm, 371 mm apart, in a cylinder of inner diameter 2R = 412 mm and length 524 mm;
  - 8 curved blades of height 41.2 mm;
  - up to 26 Hz, with 300 kW of motor power available;
  - oil at 110–160 °C;
  - sodium at rest in a shell of inner diameter 578 mm; total sodium volume: 150 l;
  - ring in the mid-plane, 5 mm thick (inner diameter, see ⚠ below).
- **Dimensionless numbers**: Re = K R² Ω/ν with K ≈ 0.6 (turbine efficiency); Re up to 5×10⁶; Rm = K µ0 σ R² Ω ≈ 49 at most (120 °C).
- **Threshold**:
  - with **stainless steel** discs: no dynamo up to 26 Hz;
  - with **soft-iron discs**: dynamo above Rm ≈ 30;
  - linear fits of ⟨B_y⟩ or B_i,rms: **Rm_c ≈ 31**;
  - linear fit of ⟨B²⟩: **R′m ≈ 35** (relevant value for a supercritical pitchfork);
  - no hysteresis;
  - kinematic thresholds based on the mean flow: Rm_c ≈ 43 to 150 depending on the BCs.
- **Field**:
  - B_y (tangent to the cylinder) goes from a value close to the Earth's field to about 40 G when Rm goes from 19 to 40;
  - fluctuations of 3 to 8 G at 30 % above threshold;
  - the scaling law ⟨B²⟩ ∝ (ρ/µ0σ²R²)(Rm − Rm_c)/Rm_c collapses the data at different temperatures.
- **Power**: at 30 % above threshold, ohmic dissipation represents an extra cost of 15–20 % on a driving power of about 100 kW.
- **Iron**: threshold about 20 % higher during the first run (magnetization), then reproducible. Axisymmetry rules out a Herzenberg-type dynamo (rotor).
- ⚠ Ring: "inner diameter 175 mm" in the PRL 2007, but "inner radius 175 mm" in Berhanu 2007 and "inner diameter of 350 mm" in Monchaux 2009. The PRL probably contains a typo. [verified in the three texts]

**Berhanu, Monchaux, Fauve, Mordant, Pétrélis, Chiffaudel, Daviaud, Dubrulle, Marié, Ravelet, Bourgoin, Odier, Pinton, Volk (2007).** "Magnetic field reversals in an experimental turbulent dynamo". *EPL* **77**, 59001. DOI 10.1209/0295-5075/77/59001. arXiv:physics/0701076. [verified]
[src] https://arxiv.org/pdf/physics/0701076

- **Contribution**: first B → −B reversals observed in the laboratory. Time hierarchy similar to that of the Earth's field. Excursions are also observed. Reversals and excursions coincide with minima of the mechanical power.
- **Parameters**:
  - sodium: σ = 10⁷ Ω⁻¹m⁻¹, ρ = 930 kg/m³, melting at 98 °C; about 160 L (⚠ the PRL 2007 gives 150 l);
  - copper vessel of radius 289 mm and length 604 mm; inner cylinder R = 206 mm;
  - Re_i = 2πK R² F_i/ν ≤ 5×10⁶; Rm_i = 2πK µ0 σ R² F_i up to 49 at 120 °C.
- **Threshold in exact counter-rotation**: dynamo for **F > about 17 Hz (Rm = 31)**.
- **Reversal regime (Fig. 3)**:
  - F1 = 16 Hz, F2 = 22 Hz, T = 123 °C;
  - ⟨T+⟩ = 120 s, ⟨T−⟩ = 50 s; duration of a reversal τ ≈ 5 s, versus an integral time of about 0.05 s and an ohmic time τη ≈ 0.4 s;
  - followed for 45 min, i.e. 54 000 forcing times; rms fluctuations of about 20 %;
  - exponential decay at about 0.8 s⁻¹ before the reversal, then overshoot afterwards;
  - power drop of more than 20 % (20 kW out of 90 kW);
  - Rm1 = Rm2 = 42.5 corresponds to 22–22 Hz.

**Monchaux et al. (2009).** "The von Kármán Sodium experiment: Turbulent dynamical dynamos". *Phys. Fluids* **21**, 035108. DOI 10.1063/1.3085724. HAL hal-00492266 (no arXiv found). [verified; 15 authors according to Crossref: Monchaux, Berhanu, Aumaître, Chiffaudel, Daviaud, Dubrulle, Ravelet, Fauve, Mordant, Pétrélis, Bourgoin, Odier, Pinton, Plihon, Volk]
[src] https://www.phys.ens.fr/~petrelis/pdf/Monchaux2009_PoF.pdf

- **Contribution**: supercritical bifurcation, neutral mode mainly **axisymmetric** under Rπ-symmetric forcing. Dynamical regimes (reversals, oscillations) under asymmetric forcing. Low-dimensional dynamics despite the turbulence.
- **Definitions**: Re = K 2π R² F/ν and Rm = K µ0 σ 2π R² F, with F = (F1 + F2)/2 and K = 0.6. Motors up to about 27 Hz, 300 kW.
- **Turbines** in pure soft iron, of relative permeability µr ≈ 100.
- **Thresholds**:
  - +w: F = 16 Hz, i.e. Rm_c = 32; −w/o: F = 18 Hz, i.e. Rm_c ≈ 43;
  - power consumed from 40 to 150 kW depending on the configuration;
  - K₊ = 0.6 or K₋ = 0.7 depending on the direction of the blades;
  - best fit: B_θ ∝ (Rm − 32)^0.77.
- **Pm**: "about 10⁻⁵ for sodium".

**Boisson, Aumaître, Bonnefoy, Bourgoin, Daviaud, Dubrulle, Odier, Pinton, Plihon, Verhille (2012).** "Symmetry and couplings in stationary Von Kármán sodium dynamos". *New J. Phys.* **14**, 013044. DOI 10.1088/1367-2630/14/1/013044. [verified]
[src] https://perso.ens-lyon.fr/nicolas.plihon/Publis/Boisson_NJP_14_013044.pdf (abstract and beginning read)

- **Set-up**: 40 3D probes; iron/iron and iron/stainless steel configurations.
- **Results**:
  - (i) no dynamo without at least one iron turbine rotating at more than 15 Hz;
  - (ii) dipolar dynamo, essentially axisymmetric;
  - (iii) dependence on the flow between the turbines.
- **Interpretation**: superposition of two single-turbine dynamos, nonlinearly coupled. The normal form resembles the model of Pétrélis et al. 2009.

**Miralles, Bonnefoy, Bourgoin, Odier, Pinton, Plihon, Verhille, Boisson, Daviaud, Dubrulle (2013).** "Dynamo threshold detection in the von Kármán sodium experiment". *Phys. Rev. E* **88**, 013002. DOI 10.1103/PhysRevE.88.013002. [verified]
[src] https://perso.ensta-paris.fr/~boisson/papiers/PhysRevE.88.013002.pdf

- **Contribution**: estimation of the threshold from below the threshold, by critical slowing down (relaxation after magnetic impulses) and by divergence of the susceptibility.
- **New definition**: Rm = µ0 σ 2π F R_imp R_o, with R_imp = 154.5 mm and R_o = 289 mm. It differs from the old definition by a factor K (note 1 of the article), hence numerically different Rm_c.
- **Conditions**: Pm of order 10⁻⁵, Re > 10⁶, fluctuations of order 1, motors up to about 25 Hz, 300 kW.
- **Thresholds**: Rm_c ≃ 44 (iron/iron, curved blades); Rm_c = 68 in "scooping" direction. Other configurations (Rm_c = 70, 60) appear in Table I.

### 1.4 Simulations: role of ferromagnetic turbines

**Giesecke, Stefani, Gerbeth (2010).** "Role of soft-iron impellers on the mode selection in the von Kármán–sodium dynamo experiment". *Phys. Rev. Lett.* **104**, 044503. DOI 10.1103/PhysRevLett.104.044503. arXiv:0907.0123. [verified]
[src] https://arxiv.org/pdf/0907.0123v2

- **Method**: kinematic induction with a localized turbine-shaped distribution of µr, plus a small α effect.
- **Results**:
  - soft iron favours the axisymmetric mode m = 0;
  - maximal µr = 60, in agreement with measurements µr ≈ 65–70 on a VKS-type turbine;
  - the "zero tangential field" condition at the lids, which mimics infinite µr, is not justified for these turbines;
  - reminder: Rm_c ≈ 32 experimentally; earlier axisymmetric predictions gave m = 1.

**Nore, Castanon Quiroz, Cappanera, Guermond (2016).** "Direct numerical simulation of the axial dipolar dynamo in the Von Kármán Sodium experiment". *EPL* **114**, 65002. DOI 10.1209/0295-5075/114/65002. [verified]
[src] https://www.math.uh.edu/~lcappan/PUBLICATIONS/Nore_castanon_cappanera_guermond_EPL_2016.pdf

- **Contribution**: first nonlinear MHD DNS of VKS with the turbines represented (SFEMaNS, pseudo-penalization). The threshold decreases when µr of the turbines increases. Axial dipole essentially axisymmetric, with an azimuthal component concentrated in the turbines.
- **Table 2 (Re = 500)**:

| µr^imp | Rm_c family 0 | Rm_c family 1 | Pm_c family 0 | Pm_c family 1 |
|---|---|---|---|---|
| 5 | 240 ± 5 | 147 ± 1 | ≈ 0.48 | ≈ 0.29 |
| 50 | 130 ± 2 | 138 ± 2 | ≈ 0.26 | ≈ 0.28 |
| 100 | 82 ± 2 | 144 ± 2 | ≈ 0.16 | ≈ 0.29 |

- Effective µr of the TM73 turbines estimated at about 65.

**Nore, Castanon Quiroz, Cappanera, Guermond (2018).** "Numerical simulation of the von Kármán sodium dynamo experiment". *J. Fluid Mech.* **854**, 164–195. DOI 10.1017/jfm.2018.582. [verified]
[src] https://www.math.uh.edu/~lcappan/PUBLICATIONS/Nore_etal_VKS_JFM_2018.pdf

- **VKS2 experimental data recalled (§2.1)**:
  - R_cyl = 206 mm; copper R_in = 289 mm, R_out = 330 mm;
  - discs R_b = 155 mm, thickness 20 mm; blades of 41 mm, thickness 5 mm, curvature 24°; distance between discs 370 mm (aspect ratio 1.8);
  - about 150 l of sodium at 120 °C; **Pm = µ0σν = 0.82×10⁻⁵**;
  - dynamo observed for **16 Hz ≤ f ≤ 22 Hz**, i.e. 6.3×10⁶ ≤ Re = 2πf R²_cyl/ν ≤ 8.7×10⁶ and **52 ≤ Rm_c = µ0σ2πf R²_cyl ≤ 71** (definition without K);
  - soft-iron turbines of µr of the order of 50; no dynamo with stainless steel turbines.
- ⚠ The text also states "Both containers have a total height H = 412 mm", whereas the PRL 2007 gives a length of 524 mm (the simulation neglects the fluid behind the turbines).
- **Nondimensional equations**: see §4.2. The term ∇×((1/σr)∇×(B/µr)) appears in the induction equation. "Perfect ferromagnetic" BC H×n = 0, also called **pseudo-vacuum**.
- **Table 3 (Re = 1.5×10³)**:
  - H×n = 0: µr = 1 → Rm_c = 190 ± 10; µr = 5 → 170 ± 5; µr = 50 → 90 ± 5;
  - vacuum BC: µr = 1 → 310 ± 30; µr = 50 → 130 ± 10.
- **Table 4 (µr = 50, H×n = 0)**:

| Re | 5×10² | 1.5×10³ | 2.5×10³ | 5×10³ | 10⁴ | 10⁵ |
|---|---|---|---|---|---|---|
| Rm_c | 135 ± 5 | 90 ± 5 | 84 ± 5 | 75 ± 5 | 70 ± 5 | 70 ± 5 |
| Pm_c | ≈ 0.27 | ≈ 0.06 | ≈ 0.034 | ≈ 0.015 | 7.5×10⁻³ | 7×10⁻⁴ |

- **Conclusion**: Rm_c∞ ≈ 70, within the experimental interval [52, 71]. High Re are handled by an entropy viscosity (LES).

**Kreuzahler, Ponty, Plihon, Homann, Grauer (2017).** "Dynamo enhancement and mode selection triggered by high magnetic permeability". *Phys. Rev. Lett.* **119**, 234501. DOI 10.1103/PhysRevLett.119.234501. arXiv:1706.00260. [verified]
[src] https://arxiv.org/pdf/1706.00260

- **Method**: full MHD, Fourier pseudo-spectral; turbines by penalization; µr jumps handled by a "sharpened raised cosine" filter; periodic BCs for b; (3π)³ box at **384³** points.
- **Definitions**: Re = ΩR_d R_c/ν = 10.125/ν and Rm = µ0σΩR_d R_c.
- **Results**:
  - for µr = 1, Rm_c increases with turbulence then saturates for Re > 1000;
  - at Re = 1500, Rm_c ≈ 740 for µr = 1;
  - at Rm = 500 (below this threshold), dynamos for µr ≥ 12 ("full impeller"); dynamos also for µr > 8 in the Fig. 1 configuration;
  - self-generated mean axisymmetric mode beyond a threshold in µr.
- Computations on GENCI (IDRIS/CINES/TGCC).

### 1.5 Comparative review of the experiments

**Pétrélis, Mordant, Fauve (2007).** "On the magnetic fields generated by experimental dynamos". *Geophys. Astrophys. Fluid Dyn.* **101**, 289–323. DOI 10.1080/03091920701523410. arXiv:0709.0234. [verified]
[src] https://arxiv.org/pdf/0709.0234

- Review of the Riga, Karlsruhe and VKS experiments. Reminder of the Ponomarenko dynamo (§3.3 below). The resting conducting cylinder is essential (Galilean invariance and invariance in a rotating frame of the induction).

---

## 2. Reversals and low-dimensional models

### 2.1 Pétrélis & Fauve (2008): dipole–quadrupole coupling, normal form

**Pétrélis & Fauve (2008).** "Chaotic dynamics of the magnetic field generated by dynamo action in a turbulent flow". *J. Phys.: Condens. Matter* **20**, 494203. DOI 10.1088/0953-8984/20/49/494203. [verified]
[src] https://www.phys.ens.fr/~petrelis/pdf/petrelisjcm2008.pdf

- **Hypothesis**: B = dipole D + quadrupole Q, with A = D + iQ. The invariance B → −B imposes A → −A, hence:
  Ȧ = µA + νĀ + β₁A³ + β₂A²Ā + β₃AĀ² + β₄Ā³.
- **Reduction**: with β₁r ≈ β₃r ≈ β₄r ≈ 0, β₂r = −1, A = R e^{i(θ+θ₀)} and ν e^{−2iθ₀} = ρ real:
  **θ̇ = µᵢ − ρ sin 2θ** (eq. 5).
- **Analysis**:
  - symmetric forcing (F1 = F2): µᵢ = 0, two stable dipoles;
  - µᵢ < ρ: four fixed points (two stable θ_c and π + θ_c, two unstable) with 2θ_c = arcsin(µᵢ/ρ);
  - at µᵢ = ρ: **saddle-node bifurcation**, then limit cycle (periodic reversals) for µᵢ > ρ.
- **Role of noise**: just below the threshold, turbulent noise causes random reversals.

### 2.2 Pétrélis, Fauve, Dormy, Valet (2009): application to the geodynamo

**Pétrélis, Fauve, Dormy, Valet (2009).** "Simple mechanism for reversals of Earth's magnetic field". *Phys. Rev. Lett.* **102**, 144503. DOI 10.1103/PhysRevLett.102.144503. arXiv:0806.3756. [verified]
[src] https://www.phys.ens.fr/~petrelis/pdf/renversementsPRL2009.pdf and https://ar5iv.labs.arxiv.org/html/0806.3756 (equations)

- **Equations**:
  - eq. (2): Ȧ = µA + νĀ + γ₁A³ + γ₂A²Ā + γ₃AĀ² + γ₄Ā³;
  - eq. (3): θ̇ = α₀ + Σ_{n≥1}(α_n cos 2nθ + β_n sin 2nθ);
  - **eq. (4): θ̇ = α₀ + α₁ sin(2θ) + Δ ζ(t)**, with ζ a Gaussian white noise; dipole D = R cos(θ + θ₀).
- **Polarity statistics**:
  - eq. (5): P[T] ∝ exp(−T/⟨T⟩);
  - eq. (6): ⟨T⟩ = π/√(α₁² − α₀²) · exp[2|α₁| (2(α₁ + α₀)/α₁)^{3/2} / (3Δ²)].
- **Parameters (Fig. 2)**: α₁ = −185 Myr⁻¹, α₀/α₁ = −0.9, θ₀ = 0.3, Δ/√|α₁| = 0.2, hence **⟨T⟩ ≈ 170 kyr**.
  ⚠ The minus signs are lost in the text extraction of the publisher PDF; the values are taken from ar5iv. [verified: the arXiv v3 PDF also gives α₁ = −185 Myr⁻¹, α₀/α₁ = −0.9, Δ/√|α₁| = 0.2]
- **Interpretation**: the model explains the overshoot after a reversal, absent from excursions. Validity linked to **small Pm**.

### 2.3 Gissinger, Dormy, Fauve (2010): morphology of reversals

**Gissinger, Dormy, Fauve (2010).** "Morphology of field reversals in turbulent dynamos". *EPL* **90**, 49001. DOI 10.1209/0295-5075/90/49001. [verified]
[src] https://www.phys.ens.fr/~gissinger/pdf/Gissinger_etal2010.pdf

- **Simulations**: DNS in a sphere, with Rm = µ0σa·max|v|, Pm = νµ0σ and Re = Rm/Pm.
  - Pm ≈ 1: the axial dipole reverses in the presence of a strong equatorial dipole (Rm = 300, Pm = 1, C = 2);
  - **Pm < 0.5**: the reversals mainly involve the axial dipole and the axial quadrupole, coupled by a symmetry breaking of the flow;
  - at Re = 330, the correlation r between dipole and quadrupole goes from 0.4 to 0.9 when Pm decreases from 1 to 0.3.
- **3-mode model (eq. 3–5)**, ⚠ with the roles of D and Q swapped relative to the 2012 article:
  - Ḋ = µD − VQ
  - Q̇ = −νQ + VD
  - V̇ = Γ − V + QD
- **Rπ symmetry**: D → −D, Q → Q, V → −V. Γ ≠ 0 expresses a forcing that breaks Rπ (turbines at different speeds); for Γ = 0 (C = 1), no stable stationary state with a dominant axial dipole.
- Figures 5–6 obtained with **µ = 0.119, ν = 0.1, Γ = 0.9**.
- The model is deterministic: no need for external noise. The two ±B attractors are connected by a crisis.

### 2.4 Gissinger (2012): 3-mode model (Q, D, V), reference for the simulation

**Gissinger (2012).** "A new deterministic model for chaotic reversals". *Eur. Phys. J. B* **85**(4), 137. DOI 10.1140/epjb/e2012-20799-5. **arXiv:1109.6569** (v2 of 2 March 2012). [verified: full text of arXiv v2 reread; equations (1)–(14) rechecked]
[src] full text: https://arxiv.org/pdf/1109.6569 — equations cross-checked on https://ar5iv.labs.arxiv.org/html/1109.6569 — metadata: https://api.crossref.org/works/10.1140/epjb/e2012-20799-5

**Exact equations (eq. 1–3)**:

```
dQ/dt = µ Q − V D        (1)   [verified]
dD/dt = −ν D + V Q       (2)
dV/dt = Γ − V + Q D      (3)
```

- **Properties**:
  - µ, ν, Γ real; quadratic nonlinearities; the relative signs guarantee bounded solutions;
  - divergence of the vector field = µ − ν − 1. ⚠ The article writes "dissipative for µ > 1+ν", whereas a negative divergence corresponds to µ < 1 + ν: probable typo. [verified: the sentence is indeed in arXiv v2; the divergence is indeed µ − ν − 1]
- **Symmetry**: **(D, Q, V) → (−D, −Q, V)**, image of B → −B. It is "crucial[ ]" for the reversals.
- **Interpretation (§4)**: D = dipole, Q = quadrupole, V = velocity mode that breaks the equatorial mirror symmetry, forced by Γ. The term QD in (3) represents the Lorentz force. V does not change sign during reversals.
- **Neighbouring models**: Rikitake (without damping of V); Nozières (MHD truncation); Proctor & Hughes (Γ = 0). Γ ≠ 0 is crucial.

**Trivial fixed point O and stability**:
- O: Q = 0, D = 0, V = Γ (eq. 4).
- Eigenvalues (eq. 5–6): λ₁,₂ = (µ−ν)/2 ± ½√((µ+ν)² − 4Γ²) and λ₃ = −1.
- µ + ν > 2Γ: real eigenvalues. µ + ν < 2Γ: complex eigenvalues and Hopf bifurcation for µ > ν. Codimension-2 point at µ = ν = Γ.

**Nontrivial fixed points**:
- **M±**, which exist if √(µν) − Γ > 0:
  Q = ±√(ν − Γ√(ν/µ)), D = ±√(µ − Γ√(µ/ν)), V = +√(µν) (eq. 7–9).
- **N±**:
  Q = ±√(ν + Γ√(ν/µ)), D = ∓√(µ + Γ√(µ/ν)) (sign of D opposite to that of Q), V = −√(µν) (eq. 10–12).
- Characteristic polynomials (eq. 13–14):
  - M±: λ³ + λ²(1 + ν − µ) + λΓ(ν − µ)/√(µν) + 4µν − 4Γ√(µν) = 0;
  - N±: same form with −λΓ(ν − µ)/√(µν) and +4Γ√(µν).
  [verified: fixed points M±, N± and polynomials (13)–(14) recomputed numerically from the Jacobian, zero residuals, identical coefficients]

**Scenario in µ (Γ = 0.9, ν = 0.1 fixed)**:
- µ > 0.2: stationary solutions N±.
- µ < 0.2: periodic orbit around each N.
- **µ < 0.138**: cascade of period doublings (bifurcation diagram plotted for µ from 0.15 to 0.1, Fig. 2).
- **Attractor-merging crisis at µ_c ≈ 0.11928**:
  - no reversal after an integration time t > 1×10⁵ (text: "t > 1.10⁵");
  - reversals observed for µ = 0.119275;
  - mean waiting time τ ∼ (µ − µ_c)^{−γ} with γ ≃ 1/2, but "difficult to conclude", because the result is very sensitive to µ_c;
  - each τ is averaged over a series of 1000 reversals.
- **µ = 0.119**: chaotic reversals, with a Lyapunov exponent λ ≃ 0.1 (unchanged by the crisis). These reversals exist only if O is an unstable focus.
- **µ = 0.12**: chaos around a single fixed point, without reversal (Fig. 3).
- **µ = 0.101**: **non-chaotic** reversals (Fig. 7).
- **µ ≤ ν**: O becomes linearly stable (bistability, "strongly subcritical" bifurcation); the system converges to O whatever the IC only for **µ < 0.063**. [verified; clarification added]
- **0.065 < µ < 0.1**: intermittency between the neighbourhood of a fixed point and an unstable orbit around O.
- **µ = 0.065**: asymmetric reversals despite the symmetry of the equations.

**Other regimes**:
- µ = ν = 0.35, Γ = 0.1: four nontrivial fixed points (Fig. 9).
- µ = 0.3, ν = 0.2, Γ = 5: exotic intermittency (Fig. 10).

**Comparison with terrestrial data**:
- Fig. 11: SINT2000, last 2 Myr. Fig. 12: CK95.
- Waiting-time distribution: quantized at short times (unstable periodic orbits), **Poissonian** at long times, P(τ) = e^{−τ/⟨τ⟩}/⟨τ⟩ (eq. 17).
- Bimodal PDF of D, with a very low probability at 0.
- Overshoot after the reversals; excursions present.
- Prediction: when D goes through 0 during a reversal, Q increases strongly (dipole → quadrupole transfer).
- ⚠ The caption of Fig. 11 states "µ = 0.119, ν = 0.1 and **Γ = 0.1**", whereas the text and the other figures use Γ = 0.9 (probable typo). [verified in arXiv v2]

**Notes for the simulation (E1)**:
1. Conventions: EPJB 2012 puts µ on Q; EPL 2010 puts µ on D. The two systems are identical up to the exchange D ↔ Q. Cite the convention used.
2. The reference regime (µ, ν, Γ) = (0.119; 0.1; 0.9) is very close to µ_c ≈ 0.11928: the waiting times are very sensitive to µ and to numerical precision.
3. **Internal numerical check** (team computation, not a published fact):
   - settings: RK4, dt = 0.01, t ∈ [0; 2×10⁴], transient of 500 removed, initial condition (Q, D, V) = (0.1; 0.1; 0); a reversal is counted when D crosses ±0.5 with a change of sign;
   - **µ = 0.119**: 74 reversals, D ∈ [−2.95; 3.13];
   - µ = 0.12 and 0.15: 0 reversals;
   - µ = 0.25: fixed point D = −1.293, V = −0.158, consistent with the N± formulas (√(0.25 + 0.9√2.5) = 1.2935; −√0.025 = −0.158);
   - µ = 0.101: 1036 reversals;
   - µ = 0.065: convergence to O with this IC, which illustrates the bistability.
   - Script: [`docs/specs/sources/scripts/gissinger_check.py`](scripts/gissinger_check.py) (`python3 docs/specs/sources/scripts/gissinger_check.py 0.119 0.12 0.15 0.25 0.101 0.065`).
   - [verified: script rerun as is by the verifier; same results for µ = 0.119 (74; D ∈ [−2.947; 3.133]), 0.12 (0), 0.15 (0), 0.25 (D = −1.293, V = −0.158), 0.101 (1036), 0.065 (O)]

---

## 3. Reference kinematic dynamos

### 3.1 ABC flow (Arnold–Beltrami–Childress), A = B = C = 1

- **Form used by Bouya & Dormy**:
  u = (A sin z + C cos y) e_x + (B sin x + A cos z) e_y + (C sin y + B cos x) e_z, on a **2π-periodic** domain.
- **Induction**: ∂B/∂t = ∇×(u×B) − Rm⁻¹ ∇×∇×B, hence **Rm = 1/η** with u of amplitude O(1) (A = B = C = 1).
  [src] Bouya & Dormy (2013) "Revisiting the ABC flow dynamo", *Phys. Fluids* **25**, 037103, DOI 10.1063/1.4795546, arXiv:1206.5186: https://arxiv.org/pdf/1206.5186 [verified]
- **Form of Archontis et al.**: u_ABC = A(0, sin kx, cos kx) + B(cos ky, 0, sin ky) + C(sin kz, cos kz, 0), with the same equation in 1/Re_m and a periodicity of 2π. For A = B = C = k = 1 ("normal" ABC):
  > "two windows of dynamo action […]: A closed one in the interval Re_m = 8.9–17.5, and an open one for magnetic Reynolds numbers above 27 (Galloway et al. 1984)".

  The maximum of the growth rate in the 1st window is reached at Re_m = 12 (cited from Galanti et al. 1993, rate value not given).
  [src] Archontis, Dorch, Nordlund (2003) *A&A* **397**, 393–399, DOI 10.1051/0004-6361:20021568, arXiv:astro-ph/0204208: https://arxiv.org/pdf/astro-ph/0204208 [verified: exact quotation found on p. 2; posted online on 17/12/2002, January 2003 issue]
- **Bouya & Dormy (2013)**, results:
  - two kinks in σ(Rm): **Rm1 ∈ [24.05; 24.10]**, eigenvalue crossing located in the stable window reported by Galloway & Frisch near Rm ≈ 20, and **Rm2 ∈ [215.0; 215.4]**, coalescence beyond which the dominant eigenvalue becomes real;
  - angular frequency ω = Im λ ≈ 0.53 in the 1st window (Arnold & Korkina 1983) and ≈ 0.13 in the 2nd (Galloway & Frisch 1986);
  - the mode of the 1st window has all the "even" symmetries of the ABC group (24 elements);
  - σ ≈ 0.1 at **Rm = 25 000** (resolution up to 1024³), with no asymptote reached;
  - Lyapunov exponent of the flow ≈ 0.055; h_line ≈ 0.09;
  - conservation of ∇·B is ensured by the spectral scheme.
  - [verified: all the Bouya & Dormy figures above found in arXiv:1206.5186]
- **Primary references** (metadata verified):
  - V.I. Arnol'd, E.I. Korkina (1983), "Growth of the magnetic field in three-dimensional steady flow of incompressible fluid", *Vestnik Moskov. Univ. Ser. 1 Mat. Mekh.* no. 3, 43–46. Abstract: Galerkin-type numerical experiment with about 20 000 harmonics, at Reynolds numbers of the order of 60; exponential growth in a range of Reynolds numbers, then decay. [src] https://mathnet.ru/eng/vmumm3491 [verified]
  - D. Galloway, U. Frisch (1984), "A numerical investigation of magnetic field generation in a flow with chaotic streamlines", *Geophys. Astrophys. Fluid Dyn.* **29**, 13–18, DOI 10.1080/03091928408248180. [src] https://api.crossref.org/works/10.1080/03091928408248180 [verified: metadata]
  - D. Galloway, U. Frisch (1986), "Dynamo action in a family of flows with chaotic streamlines", *Geophys. Astrophys. Fluid Dyn.* **36**(1), 53–83, DOI 10.1080/03091928608208797. [src] https://api.crossref.org/works/10.1080/03091928608208797 (full text inaccessible, 403) [verified: metadata; full text still 403]
- **Alexakis (2011)**, "Searching for the fastest dynamo: Laminar ABC flows", *Phys. Rev. E* **84**, 026321, DOI 10.1103/PhysRevE.84.026321, arXiv:1105.3692. [verified]
  - Note by Bouya & Dormy: the 1:1:1 case has very small chaotic regions and is probably not optimal.
  - A = B ≃ 2C/5 (and permutations) gives the fastest dynamo, with γ ≃ 0.12 at the largest R_M examined. [corrected: "not reread, would give" → confirmed in the abstract and text of arXiv:1105.3692]
  - ⚠ Convention: Alexakis normalizes by U = √(A² + B² + C²), i.e. R_M = √3/η for the ABC 1:1:1 (and not 1/η). His "R_M = 33.3, no-dynamo window" corresponds to 1/η ≈ 19, consistent with the window 8.9–17.5. [verifier's addition]

### 3.2 G.O. Roberts flow (1972)

**G.O. Roberts (1972).** "Dynamo action of fluid motions with two-dimensional periodicity". *Phil. Trans. R. Soc. Lond. A* **271**(1216), 411–454. DOI 10.1098/rsta.1972.0015. [verified]
[src] abstract: https://api.crossref.org/works/10.1098/rsta.1972.0015

- **Statement of the abstract**: spatially periodic motions whose three components depend only on (y, z) are studied. The motion **u = (cos y − cos z, sin z, sin y)** is a first-order dynamo, for almost all resistivities. Three other motions, which are not first-order dynamos, give growing fields in a multi-scale version.
- **Link with Karlsruhe**: the form "stream function ∝ sin(πx/a) sin(πy/a), u_z ∝ sin(πx/a) sin(πy/a)" is used by Rädler & Brandenburg (§1.2) to describe the Roberts flow underlying the experiment.

### 3.3 Ponomarenko dynamo

- **Reference**: Yu. B. Ponomarenko (1973), "Theory of the hydromagnetic generator", *J. Appl. Mech. Tech. Phys.* **14**(6), 775–778, DOI 10.1007/BF00853190 (Crossref; original not consulted). [corrected: pages 775–779 → 775–778 according to Crossref; Gailitis 2008 and Monchaux 2007 write 775–779]
- **Model**: rigid conducting cylinder of radius R, in solid rotation Ω and translation V, in sliding contact with an infinite medium of the same conductivity.
- **Threshold**:
  - Gailitis & Freibergs (1976), *Magnetohydrodynamics* **12**, 127–129: **Rm_c = 17.7** for the convective instability, "with the radius taken as the defining length scale" [src: arXiv:0807.0305] [verified in Gailitis 2008; ref. [10] = *Magnetohydrodynamics* 12 (1976) 127–129];
  - adding a coaxial axial return makes the instability absolute (Gailitis & Freibergs 1980, *Magnetohydrodynamics* **16**, 116–121). [verified in Gailitis 2008, refs. [10]–[11]]
- ⚠ **Divergent definitions of this 17.7**:
  - Pétrélis, Mordant, Fauve (2007): Rm_c = µ0σR√((RΩ)² + V²) = 17.7 at the optimal Rossby number Ro = V/(RΩ) = 1.3; Hopf bifurcation, travelling wave. [src] https://arxiv.org/pdf/0709.0234 [verified]
  - Dobler, Frick, Stepanov (2003), arXiv:astro-ph/0301222: Rm = U r₀/η = 17.7, with U the longitudinal velocity alone. [src] https://arxiv.org/pdf/astro-ph/0301222 [verified; published in *Phys. Rev. E* **67**, 056309 (2003), DOI 10.1103/PhysRevE.67.056309]

### 3.4 Anti-dynamo theorems

- **Cowling (1933)**: "The magnetic field of sunspots", *MNRAS* **94**, 39–48. DOI 10.1093/mnras/94.1.39 (Crossref: published on 10 November 1933; some sources cite 1934). [verified]
  - **Statement (Tobias)**: "An axisymmetric field vanishing at infinity can not be maintained by dynamo action". [verified, §2.4.3]
  - **Proof idea**: a non-axisymmetric flow immediately generates a non-axisymmetric field, so one restricts to the axisymmetric case. For the poloidal potential A: d/dt ∫ ½ s²A² dV = −η ∫ |∇(sA)|² dV, so the poloidal part decays, then the toroidal part, deprived of a source.
  - **Cartesian version**: no field vanishing at infinity and independent of z can be generated by dynamo action.
  - [src] Tobias, "The turbulent dynamo", arXiv:1907.03685 (§2.4.3): https://arxiv.org/pdf/1907.03685 ; published in *J. Fluid Mech.* **912**, P1 (2021), DOI 10.1017/jfm.2020.1055 (Crossref). [verified]
  - Kaiser & Tilgner (2014), "The axisymmetric antidynamo theorem revisited", *SIAM J. Appl. Math.* **74**(2), 571–597, DOI 10.1137/130928376, arXiv:1210.7122: they note that before their work "a proof of the axisymmetric theorem using the full (coupled) set of dynamo equations is still missing" (meridional ↔ azimuthal coupling of the **kinematic** problem), then **prove it** (exponential, pointwise and unconditional decay). [corrected: "argue that the proof remains incomplete" → they fill this gap; text reread]
- **Zel'dovich (1957)**: "The magnetic field in the two-dimensional motion of a conducting turbulent liquid", *JETP* **4**(3), 460 (original *ZhETF* **31**). [src] https://ns.jetp.ras.ru/cgi-bin/r/index/e/4/3/p460?a=list (metadata only) [verified: metadata; March 1957; the JETP page gives the original *ZhETF* **31**(3), 154]
  - **Statement (Tobias §2.4.3)**: the theorems of Bullard & Gellman (1954), Backus (1958) and, in Cartesian geometry, Zel'dovich (1957) show that a velocity field must have all three components to act as a dynamo; a planar (purely poloidal) flow cannot be a dynamo. Minimal requirement: a three-dimensional field and a non-planar flow.
- **Backus bound (1958)**: necessary condition on Rm in a finite domain, related to the magnetic energy balance (Tobias eq. 2.29). Exact statement not copied here. [verified: eq. (2.29), §2.4.4 of Tobias]

---

## 4. MHD equations, balances, invariants, boundary conditions

### 4.1 Dimensional form (Tobias, arXiv:1907.03685, eq. 2.1–2.6) [verified]

- ∂u/∂t + u·∇u = −(1/ρ)∇p + (1/ρ) j×B + ν∇²u + F/ρ
- ∂B/∂t = ∇×(u×B) − ∇×(η∇×B), with ∇·B = 0
- j = (1/µ)∇×B and η = (µσ)⁻¹. If η is constant: ∂B/∂t = ∇×(u×B) + η∇²B.

### 4.2 Nondimensional forms

- **SFEMaNS (Nore et al. 2018, eq. 2.1a–d)**: [verified]
  - ∂_t u = −(∇×u)×u + (1/Re)Δu − ∇p + f
  - ∂_t B = ∇×(u×B) − (1/Rm)∇×((1/σr)∇×(B/µr))
  - ∇·u = 0, ∇·B = 0, with f = (∇×H)×B and H = B/(µ0µr)
  - Alfvén scale B = U√(ρµ0) with U = ωR_cyl; **Rm = µ0σ0R²_cyl ω**, **Re = R²_cyl ω/ν**; L_ref = R_cyl.
- **Ponty et al. (2005), eq. (1–2)**: [verified]
  - ∂v/∂t + v·∇v = −∇P + j×B + ν∇²v + F
  - ∂B/∂t + v·∇B = B·∇v + η∇²B
  - ∇·v = 0, ∇·B = 0, with v normalized by the rms velocity and B in Alfvén units (j = ∇×B).
  - Definitions: R_V = UL/ν (U rms, L integral scale), R_M = P_M R_V = UL/η, P_M = ν/η.

### 4.3 Energy balance

- **Tobias eq. (2.11–2.12)**, without surface term, incompressible case: [verified]
  - d/dt ∫ B²/(2µ) dV = −∫ u·(j×B) dV − ηµ ∫ j² dV
  - d/dt ∫ ρu²/2 dV = +∫ u·(j×B) dV − ∫ 2νρ S² dV
  - The kinetic ↔ magnetic exchange occurs through the work of the Lorentz force.
- **With forcing** (derived from (2.1) by adding u·F; team derivation, to be presented as such; [verified: consistent with (2.11)–(2.12)]):
  d/dt (E_K + E_M) = ∫ u·F dV − ∫ 2νρ S² dV − ηµ ∫ j² dV.
  In a periodic domain, ∫ 2νρ S² = νρ ∫ |ω|². [verified by computation: identity ∫ 2 S:S = ∫ |ω|² for a periodic solenoidal field]

### 4.4 Helicities and ideal invariants (3D)

- **Ideal hydrodynamics**: E_k = ½∫ρu·u dV and **H_k = ∫ρu·ω dV** (kinetic helicity) are conserved (Moreau 1961; Moffatt 1969). [src: Tobias eq. 2.10] [verified]
- **Ideal 3D MHD**: invariants **E_T = E_V + E_M**, **H_M = ⟨A·B⟩** (B = ∇×A) and **H_C = ⟨u·B⟩** (cross-helicity) (Woltjer 1960; Pouquet 1996; Blackman 2015). In this framework, H_k is no longer conserved. [src] Pouquet, Rosenberg, Stawarz, Marino (2019), "Helicity dynamics, inverse and bi-directional cascades in fluid and MHD turbulence: A brief review", *Earth and Space Science* **6**(3), 351–369, DOI 10.1029/2018EA000432, arXiv:1807.03239: https://arxiv.org/pdf/1807.03239 [verified; completed: volume, pages and DOI added from Crossref]
- **Cascades**: the total energy cascades towards small scales; **H_M undergoes an inverse cascade** towards large scales (same review, §3.3). [verified]

### 4.5 2D MHD: (ψ, a) formulation, equivalent to (ω, a)

[src] Krstulovic, Brachet, Pouquet (2011), "Alfvén waves and ideal two-dimensional Galerkin truncated magnetohydrodynamics", *Phys. Rev. E* **84**, 016410, DOI 10.1103/PhysRevE.84.016410, arXiv:1101.1078: https://arxiv.org/pdf/1101.1078 [verified: eq. (1)–(6), (9)–(11), (16)–(17) reread]

- **Variables**: u = ∇×(ψ ẑ), b = ∇×(a ẑ), ∇·u = ∇·b = 0, bracket {f, g} = ∂ₓf ∂ᵧg − ∂ₓg ∂ᵧf.
- **Ideal equations**:
  - (1) ∂ψ/∂t = ∇⁻²[{ψ, ∇²ψ} − {a, ∇²a}]
  - (2) ∂a/∂t = {ψ, a}
  - (3) equivalent: ∂a/∂t + u·∇a = 0, so a is advected as a passive scalar; the Lorentz force j×b breaks the conservation of vorticity.
- **With dissipation (usual form)**: ∂ω/∂t + u·∇ω = b·∇j + ν∇²ω + (rot f)_z and ∂a/∂t + u·∇a = η∇²a, with j = −∇²a and ω = −∇²ψ (the sign depends on conventions). The dissipative terms do not appear in KBP (ideal case): check the signs in the code. [verified by computation: with u = ∇×(ψẑ), ω_z = −∇²ψ and j_z = −∇²a; standard form, not taken from a source]
- **Ideal invariants**:
  - energy E = ½∫(|u|² + |b|²) d²x;
  - infinity of Casimirs C = ∫[f(a) + ∇²ψ g(a)] d²x;
  - f(a) = a², g = 0 gives **A = ⟨a²⟩** (quadratic potential, positive definite);
  - f = 0, g(a) = −a gives **H_c = ∫b·u d²x** (cross-helicity);
  - in Galerkin truncation, only the quadratic invariants (E, H_c, A) remain conserved;
  - absolute equilibrium: αE + βA + γH_c.
- **Classical Orszag–Tang initial condition** (eq. 16–17): ψ = 2(cos k₀x + cos k₀y), a = 2 cos k₀x + cos 2k₀y, with k₀ = 1, E_u = E_b = 2 at t = 0 and u_rms ≈ b_rms ≈ 2.
- **Cascades**: in 2D, "the purely magnetic invariant, A², is positive definite" (Pouquet et al. 2019, §3.5). [verified]
  - The direction of the cascades (direct or inverse) of the magnetic potential and of the kinetic energy depends on the ratio of the injection rates ε_M/ε_V; the critical points differ slightly for the two (Seshasayanan & Alexakis 2016, cited in the same §3.5).
  - At weak magnetic forcing, the kinetic energy undergoes an inverse cascade.
  - Do not claim an inverse cascade of A without specifying the forcing.

### 4.6 Magnetic boundary conditions

- **Jumps at an interface** (Tobias eq. 2.7): [n·B] = 0, [n×B] = µ j_S, [n×E] = 0, [n·E] = ρ_S/ε. [verified]
- **Exterior insulator** (j_ext = 0): B is continuous (µ constant) and matches an exterior potential field; B = O(|x|⁻³) at infinity.
  - SFEMaNS solves for B in the conductor and a scalar potential in the insulator. The coupling goes through an interior penalty method, with control of ∇·B in a negative Sobolev norm (Nore 2018 §2.2).
- **Static perfect conductor** (Tobias eq. 2.8) [verified]: n·B = 0 and n×j = 0. In Cartesian geometry on z = const: ∂B_x/∂z = ∂B_y/∂z = B_z = 0; in spherical geometry: B_r = ∂(rB_θ)/∂r = ∂(rB_φ)/∂r = 0.
- **Pseudo-vacuum**:
  - tangential component of B zero on the boundary (normal field) [src] Yin, Yang, Ma, Cai, Zhang (2022), *J. Comput. Phys.* **451**, 110866, arXiv:2009.02171, DOI 10.1016/j.jcp.2021.110866: https://www.arxiv.org/pdf/2009.02171v2 [corrected: year 2021 → 2022 (volume 451, February 2022, according to Crossref; the DOI keeps "2021")];
  - first adopted by Kageyama & Sato (1995); simple for local methods but can give solutions "quite different" from the insulating BC (Harder & Hansen 2005; Jackson et al. 2014, cited by Yin) [verified];
  - in SFEMaNS: H×n = 0, called "perfect ferromagnetic" or pseudo-vacuum; it mimics walls of infinite µr (Giesecke 2010).
- **Quantitative impact (Nore 2018, Table 3)**: at Re = 1.5×10³ and µr = 50, Rm_c = 90 ± 5 in pseudo-vacuum versus 130 ± 10 in vacuum, i.e. about 40 % more. [verified: "we observe a 40 % increase"; for µr = 1, 190 → 310, i.e. "approximately 60 %"]

---

## 5. Codes and datasets

### 5.1 SFEMaNS (Spectral/Finite Elements for Maxwell and Navier–Stokes)

- **Method**: Fourier decomposition in azimuth; Lagrange finite elements (Hood–Taylor P1–P2) in the meridional section. The linear problems of each Fourier mode are decoupled (MPI parallelism); METIS partitioning; PETSc linear algebra.
- **Physics**: B in the conductors, scalar potential in the insulator, interior penalty at discontinuous σ/µ interfaces. Turbines represented by pseudo-penalization. LES by **entropy viscosity**.
- **Validation**: manufactured solutions and comparisons with other MHD codes. [src] Nore et al. 2018 §2.2. [verified]
- **Documentation v5.3** (Doxygen, 17 August 2021): https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html
  - modes NST, MXW, MHD and FHD (ferrohydrodynamics); axisymmetric domains in (r, θ, z);
  - license **GNU GPL v3 or later** (page about.html). [verified: pages doc_intro.html and about.html, generated on 17 August 2021, version 5.3]
- **Methodological references** (Crossref verified):
  - Guermond, Laguerre, Léorat, Nore (2007), "An interior penalty Galerkin method for the MHD equations in heterogeneous domains", *J. Comput. Phys.* **221**(1), 349–369, DOI 10.1016/j.jcp.2006.06.045 [verified];
  - Guermond, Laguerre, Léorat, Nore (2009), "Nonlinear magnetohydrodynamics in axisymmetric heterogeneous domains using a Fourier/finite element technique and an interior penalty method", *J. Comput. Phys.* **228**(8), 2739–2757, DOI 10.1016/j.jcp.2008.12.026 [verified];
  - Guermond, Léorat, Luddens, Nore, **Ribeiro** (2011), "Effects of discontinuous magnetic permeability on magnetodynamic problems", *J. Comput. Phys.* **230**(16), 6299–6319, DOI 10.1016/j.jcp.2011.04.026 [verified];
  - related application: Nore, Léorat, Guermond, Luddens (2011), "Nonlinear dynamo action in a precessing cylindrical container", *Phys. Rev. E* **84**, 016317, DOI 10.1103/PhysRevE.84.016317 [verified].

### 5.2 Pseudo-spectral codes (Ponty and collaborators, GHOST, Dedalus)

- **Ponty et al. 2005**: periodic 3D pseudo-spectral code, explicit 2nd-order Runge–Kutta, dealiasing with last wavenumber k = N/3, resolutions from 64³ to 512³. Three approaches: DNS, LAMHD model (Lagrangian-averaged α-model) and LES with spectral eddy viscosity ν(k, t) = 0.27[1 + 3.58(k/K_c)⁸]√(E_V(K_c, t)/K_c). [verified: eq. (4) and methods section of Ponty 2005]
- **Y. Ponty's slides** (AGAT school 2016, "Periodic box simulations and tools"): mention the codes **MIRA (P. Mininni)** and **LaTu (Holger Homann)**, the latter with a pencil decomposition (p3dfft) and MPI + multithreading parallelization. [src] https://casoca.oca.eu/images/LAGRANGE/EcolesThematiques/agat2016/pdf/Yannick_Ponty_12.pdf [verified]
- **GHOST** ("Geophysical High-Order Suite for Turbulence"):
  - pseudo-spectral, periodic 2D/3D domains; compressible and incompressible MHD, Hall-MHD, rotating or stratified Boussinesq, etc.;
  - MPI + OpenMP, CUDA; Fortran 90/95; scalability announced up to 100 000 cores; repository https://github.com/pmininni/GHOST
  - [src] https://wp.df.uba.ar/mininni/ghost [verified; the page does link to github.com/pmininni/GHOST]
  - Reference: Mininni, Rosenberg, Reddy, Pouquet (2011), "A hybrid MPI–OpenMP scheme for scalable parallel pseudospectral computations for fluid turbulence", *Parallel Computing* **37**(6–7), 316–326, DOI 10.1016/j.parco.2011.05.004. [verified]
- **Dedalus**: "solves differential equations using spectral methods", in Python, free and open source. [src] https://dedalus-project.org/ [verified]
  - Reference: Burns, Vasil, Oishi, Lecoanet, Brown (2020), "Dedalus: A flexible framework for numerical simulations with spectral methods", *Phys. Rev. Research* **2**, 023068, DOI 10.1103/PhysRevResearch.2.023068. [verified]

### 5.3 Public MHD datasets

- **JHTDB "Forced MHD turbulence" (mhd1024)**:
  - DNS of 3D incompressible MHD, 2π-periodic domain, **1024³**;
  - Pm = 1 with ν = 1.1×10⁻⁴;
  - stationary Taylor–Green forcing f = f₀[sin(k_f x)cos(k_f y)cos(k_f z) eₓ − cos(k_f x)sin(k_f y)cos(k_f z) e_y] with f₀ = 0.25 and k_f = 2;
  - ε_u = 1.1×10⁻², ε_b = 2ε_u; Re_λ^u ≈ 186, Re_λ^b ≈ 144; ⟨b²⟩/⟨u²⟩ = 1.1;
  - [src] Kuzzay, Alexandrova, Matteini (2019), *Phys. Rev. E* **99**, 053202, DOI 10.1103/PhysRevE.99.053202, arXiv:1812.06031: https://arxiv.org/pdf/1812.06031 [verified: §III.A of the article]
  - 1024 time steps stored after the stationary state: confirmed by Lemoine (2022), arXiv:2210.01038, appendix B [verified]. ⚠ Lemoine describes a forcing by "an external random force", whereas Kuzzay writes "steady Taylor-Green body force": discrepancy to be settled on the official page.
  - Official page https://turbulence.pha.jhu.edu/Forced_MHD_turbulence.aspx still returned 503 during the cross-check, README-MHD.pdf too (see §9).
- **The Well (PolymathicAI)**, datasets **MHD_64** and MHD_256:
  - **compressible isothermal** MHD without self-gravity (diffuse interstellar medium);
  - generated at 256³, then downsampled to 64³ by an ideal low-pass filter;
  - 10 ICs × 10 parameter combinations = 100 trajectories; 100 time steps (Δt = 0.01, t ∈ [0, 1]);
  - Mₛ ∈ {0.5; 0.7; 1.5; 2.0; 7.0}, M_A ∈ {0.7; 2.0}; periodic BCs; about 71.6 GB (MHD_64);
  - original simulations: Burkhart et al. (2020) *ApJ* **905**(1), 14 (CATS catalogue), DOI 10.3847/1538-4357/abc484 [verified];
  - [src] https://huggingface.co/datasets/polymathic-ai/MHD_64/blob/main/README.md [verified: all the figures above found in the README]
  - Article: Ohana et al. (2024), "The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning", *NeurIPS 2024 (Advances in Neural Information Processing Systems 37)*, 44989–45037, arXiv:2412.00568 (Crossref). [verified; DOI 10.52202/079017-1430]
  - ⚠ Compressible and non-dynamo: poorly suited to the ∇·u = 0 constraints of the offer, but useful as an ML benchmark.

---

## 6. Taylor–Green dynamo at low Pm

**Ponty, Mininni, Montgomery, Pinton, Politano, Pouquet (2005).** "Numerical study of dynamo action at low magnetic Prandtl numbers". *Phys. Rev. Lett.* **94**, 164502. DOI 10.1103/PhysRevLett.94.164502. arXiv:physics/0410046. [verified: text, Table I and eq. (1)–(4) reread]
[src] https://arxiv.org/pdf/physics/0410046

- **Taylor–Green forcing (eq. 3)**: F_TG(k₀) = 2F [sin(k₀x)cos(k₀y)cos(k₀z), −cos(k₀x)sin(k₀y)cos(k₀z), 0]ᵀ, with **k₀ = 2** (k_f = k₀√3).
  - Local differential rotation and helicity, but zero net helicity in the 2π box; small scales statistically non-helical.
  - Analogy with the Maryland, Cadarache and Wisconsin experiments.
- **Results**:
  - dynamos from P_M = 1 down to P_M = 10⁻²;
  - **R_M^c = 30 at P_M = 1**; **70 at P_M = 0.5**; **226 at P_M = 0.3**; then slight decrease, **≈ 200 at P_M = 0.2** (DNS);
  - LAMHD: plateau above 250 down to P_M = 0.09 (systematic overestimate);
  - **LES: R_M^c ≈ 150 constant for 10⁻² ≤ P_M ≤ 10⁻¹**;
  - Kazantsev spectrum k^{3/2} in the linear phase.
- **Table I (excerpts)**: code, N, R_V, L, R_M^c, 1/P_M^c

| Code | N | R_V | L | R_M^c | 1/P_M^c |
|---|---|---|---|---|---|
| DNS | 64 | 30.5 | 2.15 | 28.8 | 1.06 |
| DNS | 64 | 128 | 1.9 | 62.5 | 2.05 |
| DNS | 256 | 675 | 1.35 | 226.4 | 2.98 |
| DNS | 512 | 874.3 | 1.31 | 192.6 | 4.54 |
| LAMHD | 512 | 3052.3 | 1.22 | 276.4 | 11.05 |
| LES | 128 | 2236.3 | 1.37 | 151.9 | 14.72 |
| LES | 512 | 12550 | 1.42 | 154.6 | 81.19 |

**Ponty, Mininni, Pinton, Politano, Pouquet (2007).** "Dynamo action at low magnetic Prandtl numbers: mean flow versus fully turbulent motions". *New J. Phys.* **9**, 296. DOI 10.1088/1367-2630/9/8/296. arXiv:physics/0601105. [verified]
[src] https://arxiv.org/pdf/physics/0601105

- **Kinematic dynamo on the TG mean flow**: **two branches**, positive growth for R_M,kin ∈ [22, 51], then for R_M,kin > R_M^c3, where **R_M^c3 ≈ 158** (within ±15 %). L_kin ≈ π, U_kin ≈ 3.0.
- **Dynamic threshold**:
  - at low R_V, it lies in the lower window;
  - for **R_V > 200**, it lies in the immediate vicinity of the upper branch;
  - in developed turbulence, it is well approximated by the kinematic threshold of the upper branch computed on the mean flow.
- **Reminder from the authors**: the laminar threshold is multiplied by about 8 when unsteadiness develops (earlier work). [verified: "eightfold increase"]

---

## 7. Discrepancies and reservations (the unconfirmed is grouped in §9)

1. **ABC windows "8.9 < Rm < 17.5" and "> 27"**: confirmed in Archontis et al. 2003, who attribute them to "Galloway et al. 1984" [verified in Archontis 2003]. Consistent with Alexakis 2011, once his normalization R_M = √3/η is taken into account [verified]. Bouya & Dormy place the mode crossing at Rm1 ∈ [24.05; 24.10], "in the stable window reported by Galloway and Frisch [1986] near Rm = 20" [verified]. The direct reading of Galloway & Frisch and the value of the maximal growth rate remain unconfirmed (see §9).
2. **Arnold & Korkina**: year 1983 (Math-Net.Ru: Vestnik Moskov. Univ. Ser. 1 Mat. Mekh., no. 3, 43–46, received 26/11/1982); Galloway's slides (MREP60) write "Arnold and Korkina (1984)". [verified]
3. **Stieglitz & Müller 2001**: paywalled full text, not read. The Karlsruhe figures come from Müller et al. 2008 (C. R. Physique) and from Rädler & Brandenburg. [verified: Crossref metadata and abstract]
4. **Rädler & Brandenburg**: *Phys. Rev. E* **67**, 026401 (2003), DOI 10.1103/PhysRevE.67.026401. [verified: correction reported in §1.2]
5. **Riga**: motorization of 2×55 kW (PRL 2000) versus 2×100 kW (C. R. Physique 2008); Gailitis et al. 2018: "two DC-motors, which can be driven up to 200 kW". First attempt dated 1986 (2008) or 1987 (PRL 2000 and JPP 2018). Flow rate "0.6 m³/s" in the PRL 2000. [verified in the three texts]
6. **VKS** [verified]:
   - three definitions of Rm coexist: K µ0σR²Ω with K = 0.6 (2007–2009); µ0σ2πF R_imp R_o (Miralles 2013); µ0σ2πf R²_cyl without K (Nore 2018, which gives 52–71);
   - the values 31, 32, 35, 44 and 52–71 are therefore not directly comparable;
   - diameter or radius of the ring: see §1.3; sodium volume 150 l (PRL 2007) or about 160 L (Berhanu 2007).
7. **Gissinger 2012** [verified in arXiv:1109.6569v2]:
   - "dissipative for µ > 1+ν" (probable typo: the divergence µ − ν − 1 is negative for µ < 1 + ν);
   - Γ = 0.1 in the caption of Fig. 11 (probable typo);
   - "t > 1.10⁵" read as 1×10⁵;
   - exponent γ ≃ 1/2 given with reservation by the author.
   - The publisher version (EPJB) was not consulted: the typos may not be present there.
8. **Pétrélis et al. 2009**: α₁ = −185 Myr⁻¹, α₀/α₁ = −0.9, θ₀ = 0.3, Δ/√|α₁| = 0.2, confirmed both on ar5iv and in the arXiv v3 PDF. [verified]
9. **Zel'dovich theorem**: exact statement not read in the original (only the JETP metadata); formulation taken from Tobias §2.4.3. [verified: metadata and Tobias's formulation]
10. **Helicities**: the sentence "kinetic helicity is not invariant in MHD" is a standard deduction, consistent with Tobias ("In the presence of a magnetic field these quantities are no longer conserved") and Pouquet et al. 2019 (list of MHD invariants without H_V). [verified]
11. **JHTDB MHD**: main parameters confirmed via Kuzzay et al. 2019; 1024 time steps confirmed via Lemoine 2022; nature of the forcing divergent (stationary Taylor–Green for Kuzzay, "external random force" for Lemoine). The rest is in §9.

---

## 8. URLs consulted (primary sources)

**Experiments**
- Riga 2000: https://arxiv.org/pdf/physics/9912026
- Riga 2001: https://arxiv.org/pdf/physics/0010047
- Riga, history 2008: https://arxiv.org/pdf/0807.0305
- Riga 2018 (J. Plasma Phys.): https://arxiv.org/pdf/1801.01749
- Karlsruhe 2008: https://comptes-rendus.academie-sciences.fr/physique/item/10.1016/j.crhy.2008.07.005.pdf
- Rädler & Brandenburg: https://arxiv.org/pdf/physics/0208023
- VKS PRL 2007: https://www.phys.ens.fr/~petrelis/pdf/P1PRL_98_044502.pdf
- Berhanu 2007: https://arxiv.org/pdf/physics/0701076
- Monchaux 2009: https://www.phys.ens.fr/~petrelis/pdf/Monchaux2009_PoF.pdf
- Boisson 2012: https://perso.ens-lyon.fr/nicolas.plihon/Publis/Boisson_NJP_14_013044.pdf
- Miralles 2013: https://perso.ensta-paris.fr/~boisson/papiers/PhysRevE.88.013002.pdf

**VKS simulations**
- Giesecke 2010: https://arxiv.org/pdf/0907.0123v2
- Nore 2016: https://www.math.uh.edu/~lcappan/PUBLICATIONS/Nore_castanon_cappanera_guermond_EPL_2016.pdf
- Nore 2018: https://www.math.uh.edu/~lcappan/PUBLICATIONS/Nore_etal_VKS_JFM_2018.pdf
- Kreuzahler 2017: https://arxiv.org/pdf/1706.00260

**Reversals**
- Pétrélis & Fauve 2008: https://www.phys.ens.fr/~petrelis/pdf/petrelisjcm2008.pdf
- Pétrélis et al. 2009: https://www.phys.ens.fr/~petrelis/pdf/renversementsPRL2009.pdf and https://ar5iv.labs.arxiv.org/html/0806.3756
- Gissinger et al. 2010: https://www.phys.ens.fr/~gissinger/pdf/Gissinger_etal2010.pdf
- Gissinger 2012: https://arxiv.org/pdf/1109.6569 and https://ar5iv.labs.arxiv.org/html/1109.6569

**Kinematic dynamos**
- ABC: https://arxiv.org/pdf/1206.5186 ; https://arxiv.org/pdf/astro-ph/0204208 ; https://mathnet.ru/eng/vmumm3491
- Ponomarenko: https://arxiv.org/pdf/0709.0234 ; https://arxiv.org/pdf/astro-ph/0301222

**MHD theory and boundary conditions**
- Tobias: https://arxiv.org/pdf/1907.03685
- Pouquet et al. 2019: https://arxiv.org/pdf/1807.03239
- Krstulovic et al. 2011: https://arxiv.org/pdf/1101.1078
- Pseudo-vacuum: https://www.arxiv.org/pdf/2009.02171v2

**Taylor–Green**
- Ponty 2005: https://arxiv.org/pdf/physics/0410046
- Ponty 2007: https://arxiv.org/pdf/physics/0601105

**Codes and data**
- SFEMaNS: https://people.tamu.edu/~guermond/SFEMaNS/html/doc_intro.html
- GHOST: https://wp.df.uba.ar/mininni/ghost
- Dedalus: https://dedalus-project.org/
- Ponty slides: https://casoca.oca.eu/images/LAGRANGE/EcolesThematiques/agat2016/pdf/Yannick_Ponty_12.pdf
- JHTDB via Kuzzay: https://arxiv.org/pdf/1812.06031
- The Well: https://huggingface.co/datasets/polymathic-ai/MHD_64/blob/main/README.md

**Metadata**
- Crossref: https://api.crossref.org/works/<DOI> for each cited DOI.

**Added during the cross-check**
- arXiv metadata (API export.arxiv.org) for the 25 cited arXiv identifiers: titles, authors, DOI and journal-ref agree.
- Riga 2018 (JPP 84, 735840301): https://arxiv.org/pdf/1801.01749
- Alexakis 2011: https://arxiv.org/pdf/1105.3692
- Kaiser & Tilgner 2014: https://arxiv.org/pdf/1210.7122
- Galloway slides (MREP60): https://mhd.ens.fr/MREP60/ols/Galloway.pdf
- Lemoine 2022 (JHTDB, 1024 time steps): https://arxiv.org/pdf/2210.01038
- Arnold & Korkina: https://www.mathnet.ru/eng/vmumm3491
- Ponomarenko 1973: https://api.crossref.org/works/10.1007/BF00853190
- SFEMaNS, license: https://people.tamu.edu/~guermond/SFEMaNS/html/about.html
- The Well, raw README: https://huggingface.co/datasets/polymathic-ai/MHD_64/raw/main/README.md

---

## 9. Unconfirmed

*Entries that neither the researcher nor the verifier could confirm in an open primary source. Do not use them without new verification.*

1. **Ponty's "CUBBY" code** [UNCONFIRMED]: no source found (web search redone by the verifier, without result). The open sources cite only **MIRA** (Mininni) and **LaTu** (Homann) in Ponty's slides (AGAT 2016); Kreuzahler 2017 and Ponty 2005 do not name their code.
2. **JHTDB MHD, secondary parameters** [UNCONFIRMED]: interval t ∈ [0; 2.56], η = 1.1×10⁻⁴ independently of Pm = 1, and injection scale (L = π/2 for Kuzzay, "stirring scale equal to 0.5 in units of the size of the simulation box" for Lemoine). The official page (turbulence.pha.jhu.edu) and README-MHD.pdf (turbulence.idies.jhu.edu) still return 503 or present a self-signed certificate.
3. **Riga, flow rate 0.67 m³/s** [UNCONFIRMED]: value attributed to an HZDR page not reread; only the "0.6 m³/s" of the PRL 2000 is verified.
4. **ABC 1:1:1, primary reading of the windows and maximal growth rate** [UNCONFIRMED]: Galloway & Frisch 1984 (GAFD 29, 13–18) and 1986 (GAFD 36, 53–83) remain inaccessible (tandfonline: 403). The bounds 8.9 / 17.5 / 27 are therefore verified only via Archontis 2003. The **value** of the maximal growth rate of the 1st window (reached around Re_m ≈ 12 according to Archontis, from Galanti et al. 1993) is not known.
