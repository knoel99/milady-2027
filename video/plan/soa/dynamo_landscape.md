# The dynamo science landscape, 1919–2026: tracks, landmarks, open problems

Prepared 2026-11-08 for the MilaDy 2027 explainer film (units `chSOA1` and `chSOA2`, BRIEF.md §10) and for the
French companion document `video/ETAT-DE-L-ART.md`. Scope: dynamo physics only (theory, laboratory, numerics,
reduced models of reversals, reversal statistics), plus the first data-driven reduced models. Machine learning
for turbulence, generative models and physics constraints belong to the companion landscape for `chSOA2`; they
appear here only where they touch reversals.

## How to read the source marks

| Mark | Meaning |
|---|---|
| `[site: file:line]` | Fact already verified in the repository (fact bases cross-checked on 2026-11-06). Paths are relative to `/home/user/milady-2027`. |
| `[CR]` | Bibliographic metadata (authors, title, venue, volume, pages, year) checked today in the Crossref API (`api.crossref.org/works/<DOI>`). |
| `[OA]` | Abstract read today through the OpenAlex API (`api.openalex.org/works/doi:<DOI>`), i.e. the publisher's abstract. |
| `[AX]` | arXiv metadata or abstract read today through `export.arxiv.org`. |
| `[FT: X]` | Full text of X read today (PDF from arXiv or the author's site); a statement taken from X's text. |
| `[sec: X]` | Known only through review X, which was read today; the primary paper was not read. |
| `[UNVERIFIED]` | Could not be confirmed in a source opened today or in the site's fact bases. Do not use on screen without a new check. |

Reviews read in full today and used as secondary sources: Rincon (2019), *Dynamo theories*, J. Plasma Phys. 85(4),
205850401, doi:10.1017/S0022377819000539, arXiv:1903.07829 (§1.4 history, §2.3.3 fast dynamos, §3.3.2 low Pm);
Tobias (2021), *The turbulent dynamo*, J. Fluid Mech. 912, P1, doi:10.1017/jfm.2020.1055, arXiv:1907.03685
(§3, §8.3, §9, §10); Stefani, Gailitis, Gerbeth, Giesecke, Gundrum, Rüdiger, Seilmayer, Vogt (2018),
*Laboratory experiments on dynamo action and magnetically triggered flow instabilities*, arXiv:1803.03421, published
as Stefani et al. (2019), Geophys. Astrophys. Fluid Dyn. 113(1–2), 51–70, doi:10.1080/03091929.2018.1501481
`[CR][OA]` (title in the journal: *The DRESDYN project: liquid metal experiments on dynamo action and
magnetorotational instability*); Constable (2003), *Geomagnetic reversals: rates, timescales, preferred paths,
statistical models and simulations*, in Jones, Soward & Zhang (eds), *Earth's Core and Lower Mantle*, Taylor & Francis,
pp. 77–99, doi:10.1201/9780203207611.ch4 `[CR]` (text read: author's preprint dated 30 Sept. 2001,
igpppublic.ucsd.edu/~cathy/Publications/Preprints/geomag_reversals_preprint.pdf).

---

## 1. The map in one paragraph (for `chSOA1`)

A century of dynamo research has followed five tracks that keep feeding each other. **Theory** asked whether a
moving conductor can sustain a field at all (Larmor 1919), ran into an impossibility theorem (Cowling 1933), then
found working mechanisms: rigorous existence proofs (Herzenberg 1958, Backus 1958), the α effect of mean-field
electrodynamics (Parker 1955; Steenbeck, Krause and Rädler 1966), simple dynamo flows (Roberts 1972, Ponomarenko
1973, ABC, Taylor–Green), fast dynamos (Vainshtein and Zel'dovich 1972) and small-scale dynamos (Kazantsev 1968),
with the low magnetic Prandtl number of liquid metals as a persistent obstacle. **Laboratory dynamos** went from
solid-rotor models (Lowes and Wilkinson 1963) to the first fluid dynamos in Riga and Karlsruhe (1999) and to the
turbulent, reversing VKS dynamo (2006–2007); DRESDYN aims at a precession dynamo. **Numerical dynamos** produced
self-consistent reversing geodynamo models (Glatzmaier and Roberts 1995), community benchmarks (2001, 2011, 2016)
and simulations of the experiments themselves (SFEMaNS, LATU). **Reduced models** explained reversals with a few
modes (Rikitake 1958; Pétrélis and Fauve 2008; Gissinger 2012) and are now being identified from simulation data
(DQVU, Bousquet et al. 2026). **Reversal statistics** of the Earth's field (Cox 1968 onward) show irregular,
roughly Poisson-like waiting times with a rate that changes over geological time, and debated clustering. MilaDy
sits where tracks 2, 3 and 4 meet, and the thesis adds a distributional, generative layer between simulations
and reduced models (section 5).

---

## 2. Dated timeline (origins to 2026)

| Year | Event | Track | Source |
|---|---|---|---|
| 1906 | Brunhes reports volcanic rocks magnetized opposite to the present field. | 5 | Brunhes, J. Phys. Théor. Appl. 5, 705–724, doi:10.1051/jphystap:019060050070500 `[CR]`; content `[FT: Constable 2003 §1]` |
| 1919 | Larmor proposes that motions of a conducting fluid could sustain the Sun's (sunspot) field: the self-exciting fluid dynamo idea. | 1 | `[FT: Rincon 2019 §1.3–1.4]`; reference details `[sec]`, see §3.1 |
| 1929 | Matuyama, directions of magnetisation of basalts in Japan, Korea (Tyôsen) and Manchuria. | 5 | Proc. Imperial Acad. 5(5), 203–205, doi:10.2183/pjab1912.5.203 `[CR]` (content not read) |
| 1933 | Cowling: an axisymmetric field cannot be sustained by dynamo action. | 1 | `[site: specs/sources/dynamo.md:435-440]` |
| 1937 | Taylor and Green introduce the vortex flow later used as a dynamo forcing. | 1, 3 | Proc. R. Soc. A 158, 499–521, doi:10.1098/rspa.1937.0036 `[CR]` |
| 1946–1954 | Elsasser, then Bullard and Gellman, formulate spherical dynamo theory for the Earth's core. | 1 | `[CR]` both; role `[FT: Rincon §1.4]` |
| 1950 | Batchelor argues there could be no (small-scale) dynamo for Pm < 1. | 1 | `[sec: Rincon §3.3.2]`; Proc. R. Soc. A 201, 405–416 `[CR]` |
| 1955 | Parker: cyclonic motions plus differential rotation excite large-scale fields and dynamo waves. Bullard: stability of the homopolar disc dynamo. | 1, 4 | `[CR]`; `[FT: Rincon §1.4]` |
| 1957 | Zel'dovich: a planar flow cannot be a dynamo. | 1 | `[site: specs/sources/dynamo.md:441-442]` |
| 1958 | Herzenberg (two eddies in a sphere) and Backus: first rigorous working fluid dynamos. Rikitake: coupled disc dynamos reverse. | 1, 4 | `[CR][OA]`; `[FT: Rincon §1.4]` |
| 1963 | Lowes and Wilkinson: first laboratory model dynamo (rotating soft-iron cylinders). Vine and Matthews interpret seafloor magnetic anomalies as a record of reversals. | 2, 5 | `[CR]`; content `[FT: Stefani et al. 2018 §2.1]`, `[FT: Constable 2003 §1]` |
| 1964 | Cox, Doell and Dalrymple assemble radiometrically dated evidence of global reversals. | 5 | Science 144, 1537–1543 `[CR]`; role `[FT: Constable 2003 §1]` |
| 1966 | Steenbeck, Krause and Rädler: mean-field electrodynamics and the α effect. | 1 | `[site: en/prep/p3-mhd-dynamo/index.qmd:918]`, `[CR]` |
| 1967–1968 | Kazantsev's model of small-scale dynamo action in random flows. Steenbeck et al.: first liquid-sodium measurement of an α effect (1967). Cox: Bernoulli-trial (Poisson-type) model of polarity intervals (1968). Lowes and Wilkinson's improved model (1968). | 1, 2, 5 | Kazantsev `[web: JETP archive listing]`; Steenbeck 1967 `[sec: Stefani 2018 §2.1]`; Cox `[CR][OA]`; Lowes–Wilkinson `[CR]` |
| 1970–1973 | Kinematic dynamo flows: Childress (1970), G. O. Roberts (1970, 1972), Ponomarenko (1973). Fast-dynamo concept and stretch–twist–fold (Vainshtein and Zel'dovich 1972). | 1 | `[CR]`; `[site: specs/sources/dynamo.md:416-431]`; `[FT: Rincon §1.4, §2.3.3]` |
| 1978 | Nozières: relaxation model of reversals. | 4 | PEPI 17, 55–74 `[CR]` (content not read) |
| 1980 | Krause and Rädler's monograph on mean-field MHD and dynamo theory. | 1 | `[CR]` |
| 1981 | Meneguzzi, Frisch and Pouquet: first numerical demonstration of large-scale (helical) and small-scale (non-helical) turbulent dynamos. | 1, 3 | PRL 47, 1060–1064 `[CR]`; `[FT: Rincon §1.4]` |
| 1983–1986 | ABC-flow dynamo: Arnold and Korkina (1983), Galloway and Frisch (1984, 1986); chaotic ABC streamlines (Dombre et al. 1986). | 1 | `[site: specs/sources/dynamo.md:405-408]`; Dombre `[CR]` |
| 1987 | Soward: existence of fast dynamos in a steady flow. First Riga attempt (1986 or 1987 depending on the source). | 1, 2 | `[CR][OA]`; `[site: specs/sources/dynamo.md:79,615]` |
| 1992 | Galloway and Proctor: numerical fast dynamos in smooth, time-periodic flows. | 1 | `[CR]`; `[FT: Rincon §2.3.3]` |
| 1995 | Glatzmaier and Roberts: first self-consistent 3D geodynamo simulation with a dipole reversal. Kageyama and Sato: MHD dynamo in a rotating spherical shell. Cande and Kent: CK95 polarity time scale. Childress and Gilbert, *Stretch, Twist, Fold*. | 3, 5, 1 | `[CR]`; `[FT: Tobias §8.3]` |
| 1997 | Nore, Brachet, Politano and Pouquet: dynamo action in the Taylor–Green vortex (thresholds set by the flow symmetries). | 3 | Phys. Plasmas 4, 1–3 `[CR][OA]` |
| 1999 | **Riga** (11 Nov.) and **Karlsruhe** (Dec.): first self-excited fluid dynamos. | 2 | `[site: specs/sources/dynamo.md:36,106]` |
| 2000–2001 | Riga saturated regime (July 2000); Karlsruhe published (2001); Constable (2000) on time-varying reversal rates; first community geodynamo benchmark (Christensen et al. 2001). | 2, 5, 3 | `[site: specs/sources/dynamo.md:64-74,85-88]`; `[CR]` |
| 2002 | VKS1: induction measurements in a von Kármán sodium flow up to Rm ≈ 50, no dynamo. Kutzner and Christensen: transition from stable dipolar to reversing numerical dynamos. | 2, 3 | `[CR][OA]` both |
| 2005 | Ponty et al.: Taylor–Green dynamos down to Pm = 10⁻²; Schekochihin et al.: Rm_c keeps rising with Re at low Pm; Valet et al.: SINT-2000 dipole-moment record. | 1, 3, 5 | `[site: specs/sources/dynamo.md:573-595]`; `[CR][OA]` |
| 2006 | Madison sodium sphere: turbulence-induced dipole moment (no self-excitation). VKS2 reaches dynamo threshold (published 2007). Carbone et al.: reversals depart from Poisson statistics (clustering). | 2, 5 | `[CR][OA]`; `[FT: Stefani 2018 §2.1]` |
| 2007 | **VKS**: first dynamo in a fully turbulent flow, only with soft-iron impellers; first laboratory reversals. Iskakov et al.: fluctuation dynamo exists at Pm ≪ 1. | 2, 1 | `[site: specs/sources/dynamo.md:111-153]`; `[CR][OA]` |
| 2008–2010 | Pétrélis–Fauve normal form (2008) and its geodynamo version (2009); impeller role in simulations (Laguerre et al. 2008; Giesecke et al. 2010); Gissinger, Dormy and Fauve (2010): low-Pm spherical reversals; Perm: turbulent magnetic diffusivity measured (2010). | 4, 3, 2 | `[site: specs/sources/dynamo.md:188-196,260-304]`; Perm `[CR][OA]` |
| 2011–2012 | Precession can drive a dynamo in a cylinder (Nore et al. 2011, simulations). Gissinger (2012) deterministic three-mode model. DRESDYN facility described (Stefani et al. 2012). Tayler instability observed in a liquid-metal column (Seilmayer et al. 2012). | 3, 4, 2 | `[site: specs/sources/encadrants.md:245]`; `[site: specs/sources/dynamo.md:308-367]`; `[CR][OA]` |
| 2016 | SFEMaNS DNS of VKS with the impellers (Nore et al. 2016). Anelastic (2011) and performance (2016, 15 codes) geodynamo benchmarks. | 3 | `[site: specs/sources/dynamo.md:198-210]`; `[CR][OA]` |
| 2017 | LATU DNS: high permeability selects the axisymmetric mode (Kreuzahler et al.). Geodynamo simulations approach Earth's regime (Schaeffer et al.; Aubert et al.). DRESDYN building finalized. | 3, 2 | `[site: specs/sources/dynamo.md:235-245]`; `[CR][OA]`; `[FT: Stefani 2018 §1]` |
| 2018 | Laser-plasma turbulent dynamo amplification (Tzeferacos et al.). Nore et al. (2018) JFM: Rm_c → ≈ 70 at large Re in VKS simulations. | 2, 3 | `[CR][OA]`; `[site: specs/sources/dynamo.md:212-233]` |
| 2019 | Singer et al.: last reversal completed at ≈ 773 ka after a ≈ 22 kyr process. | 5 | Sci. Adv. 5, eaaw4621 `[CR][OA]` |
| 2022 | Machine-learning search for reversal precursors limited by data (Gwirtz et al.). | 4, 5 | GJI 231, 520–535 `[CR][OA]` |
| 2023 | Small-scale dynamo found down to Pm = 0.0031 (Warnecke et al.). | 1 | Nature Astron. 7, 662–668 `[CR][OA]` |
| 2025 | DRESDYN precession experiment "being set up" (Giesecke et al., arXiv v3, April 2025). | 2 | `[FT: arXiv:2410.14449v3, line "Currently, a new experiment is being set up at HZDR"]` |
| 2026 | ANR MilaDy starts (Jan.). Bousquet et al. (PRFluids, June): VKS reversals in simulations and the DQVU reduced model. Botez et al. (PRFluids, Aug.): boundary conditions and precession-dynamo onset. Guseva, Skene and Tobias (arXiv, March): DMD + SINDy dynamo-cycle equations. | 3, 4 | `[site: specs/sources/encadrants.md:28-33,227-240]`; `[AX]` |

---

## 3. Map of tracks and landmark works

Each track lists its question, the landmark works (full citations), what each showed, the state of the track in
2026, and the published contributions of the supervisors in that track (their own papers only).

### 3.1 Track 1: Theory

**Question.** Can a flow of conducting fluid sustain a magnetic field against ohmic decay, which flows can, how
fast, and at which scales?

**1a. Foundations: the idea, the obstacle, the first proofs**

1. Larmor, J. (1919). *How could a rotating body such as the Sun become a magnet?* Report of the British
   Association for the Advancement of Science, pp. 159–160. Idea of self-exciting fluid dynamos for sunspot
   magnetism `[FT: Rincon §1.3]`. Title and pages `[sec: search-engine excerpts of a Springer encyclopedia entry
   and of Blackett 1947; Wikisource transcription exists]`; the report itself was not opened: **title and pages
   [UNVERIFIED in the primary]**.
2. Cowling, T. G. (1933). *The magnetic field of sunspots.* MNRAS 94, 39–48, doi:10.1093/mnras/94.1.39. No
   axisymmetric field vanishing at infinity can be maintained by dynamo action `[site: specs/sources/dynamo.md:435-440]`;
   the full coupled kinematic proof was supplied by Kaiser & Tilgner (2014), SIAM J. Appl. Math. 74(2), 571–597
   `[site: specs/sources/dynamo.md:440]`.
3. Parker, E. N. (1955). *Hydromagnetic dynamo models.* ApJ 122, 293, doi:10.1086/146087 `[CR]`. Differential
   rotation plus small-scale cyclonic motions excite large-scale fields, including oscillatory "Parker waves"
   `[FT: Rincon §1.4]`.
4. Herzenberg, A. (1958). *Geomagnetic dynamos.* Phil. Trans. R. Soc. A 250, 543–583,
   doi:10.1098/rsta.1958.0007 `[CR]`. Rigorous proof that two eddies in a conducting sphere act as a steady dynamo
   `[OA]`. With Backus, G. (1958), *A class of self-sustaining dissipative spherical dynamos*, Ann. Phys. 4,
   372–447, doi:10.1016/0003-4916(58)90054-X `[CR]`: "the spell of Cowling's theorem was definitely broken"
   `[FT: Rincon §1.4]`.
5. Steenbeck, M., Krause, F., Rädler, K.-H. (1966). *Berechnung der mittleren Lorentz-Feldstärke …* Z. Naturforsch.
   A 21, 369–376, doi:10.1515/zna-1966-0401 `[CR]`. Mean-field electrodynamics: the α effect in flows lacking
   mirror symmetry `[site: en/prep/p3-mhd-dynamo/index.qmd:918-924]`; monograph: Krause, F., Rädler, K.-H. (1980),
   *Mean-Field Magnetohydrodynamics and Dynamo Theory*, Pergamon / Akademie-Verlag, De Gruyter record
   doi:10.1515/9783112729694 `[CR]`.

**1b. Kinematic dynamo flows (the templates of the experiments)**

1. Roberts, G. O. (1972). *Dynamo action of fluid motions with two-dimensional periodicity.* Phil. Trans. R. Soc. A
   271, 411–454, doi:10.1098/rsta.1972.0015. u = (cos y − cos z, sin z, sin y) is a dynamo for almost all
   resistivities; template of Karlsruhe `[site: specs/sources/dynamo.md:416-420]`. Earlier: Roberts (1970),
   *Spatially periodic dynamos*, Phil. Trans. R. Soc. A 266, 535–558, doi:10.1098/rsta.1970.0011 `[CR]`;
   Childress, S. (1970), *New solutions of the kinematic dynamo problem*, J. Math. Phys. 11, 3063–3076,
   doi:10.1063/1.1665095 `[CR][OA]`.
2. Ponomarenko, Yu. B. (1973). *Theory of the hydromagnetic generator.* J. Appl. Mech. Tech. Phys. 14, 775–778,
   doi:10.1007/BF00853190. Helical rigid-body motion in a conductor at rest; Rm_c = 17.7 (convective
   instability, radius as length scale; Gailitis and Freibergs 1976); template of Riga
   `[site: specs/sources/dynamo.md:424-431]`.
3. ABC flow: Arnol'd, V. I., Korkina, E. I. (1983), Vestnik Moskov. Univ. Ser. 1 Mat. Mekh. no. 3, 43–46;
   Galloway, D., Frisch, U. (1986), *Dynamo action in a family of flows with chaotic streamlines*, GAFD 36, 53–83,
   doi:10.1080/03091928608208797. Two dynamo windows 8.9 < Rm < 17.5 and Rm > 27 for A = B = C = 1
   `[site: specs/sources/dynamo.md:386-412]` (windows verified only through Archontis et al. 2003, see the site's
   §9). Chaotic streamlines: Dombre, T., Frisch, U., Greene, J. M., Hénon, M., Mehr, A., Soward, A. M. (1986), JFM
   167, 353–391, doi:10.1017/S0022112086002859 `[CR]`. Growth rate still ≈ 0.1 at Rm = 25 000 (Bouya & Dormy 2013)
   `[site: specs/sources/dynamo.md:397-404]`.
4. Taylor–Green: flow of Taylor, G. I., Green, A. E. (1937), *Mechanism of the production of small eddies from
   large ones*, Proc. R. Soc. A 158, 499–521, doi:10.1098/rspa.1937.0036 `[CR]`; dynamo shown by Nore, C.,
   Brachet, M. E., Politano, H., Pouquet, A. (1997), *Dynamo action in the Taylor–Green vortex near threshold*,
   Phys. Plasmas 4, 1–3, doi:10.1063/1.872578 `[CR]`: the critical Rm depends on the flow symmetries, and the
   magnetic boundary conditions select the fastest mode; motivated by a planned laboratory experiment `[OA]`.

**1c. Fast dynamos**

1. Vainshtein, S. I., Zel'dovich, Ya. B. (1972). *Origin of magnetic fields in astrophysics (turbulent "dynamo"
   mechanisms).* Sov. Phys. Usp. 15, 159–172, doi:10.1070/PU1972v015n02ABEH004960 `[CR]`. Fast dynamo concept and
   stretch–twist–fold picture, growth rate ln 2 per turnover in the ideal cartoon `[FT: Rincon §2.3.3]`.
2. Soward, A. M. (1987). *Fast dynamo action in a steady flow.* JFM 180, 267–295, doi:10.1017/S0022112087001800
   `[CR]`. Existence of fast dynamos in a steady 2D periodic flow with singular vorticity at X points `[OA]`.
3. Galloway, D. J., Proctor, M. R. E. (1992). *Numerical calculations of fast dynamos in smooth velocity fields with
   realistic diffusion.* Nature 356, 691–693, doi:10.1038/356691a0 `[CR]`. Time-periodic 2D–3C flow, thought fast
   `[FT: Rincon §2.3.3]`.
4. Childress, S., Gilbert, A. D. (1995). *Stretch, Twist, Fold: The Fast Dynamo.* Lecture Notes in Physics
   Monographs m37, Springer, doi:10.1007/978-3-540-44778-8 `[CR]`.
5. Requirement of Lagrangian chaos (Finn & Ott 1988) `[sec: Rincon §2.3.3]`.

**1d. Small-scale dynamo and the low-Pm problem**

1. Batchelor, G. K. (1950). *On the spontaneous magnetic field in a conducting liquid in turbulent motion.* Proc. R.
   Soc. A 201, 405–416, doi:10.1098/rspa.1950.0069 `[CR]`: argued for no dynamo at Pm < 1 `[sec: Rincon §3.3.2]`.
2. Kazantsev, A. P. (1968). *Enhancement of a magnetic field by a conducting fluid.* Sov. Phys. JETP 26(5), 1031
   (ZhETF 53, 1806, 1967) `[web: JETP archive listing via search; full text not read]`. Statistical model of
   small-scale dynamo action in non-helical random flows `[FT: Rincon §1.4]`; magnetic spectrum k^{3/2}
   (seen in the Taylor–Green runs of Ponty et al. 2005 `[site: specs/sources/dynamo.md:584]`).
3. Schekochihin, A. A., Haugen, N. E. L., Brandenburg, A., Cowley, S. C., Maron, J. L., McWilliams, J. C. (2005).
   *The onset of a small-scale turbulent dynamo at low magnetic Prandtl numbers.* ApJ 625, L115–L118,
   doi:10.1086/431214 `[CR]`. Rm_c grows with Re with no sign of a limit, up to Rm_c ≈ 500 at Re ≈ 3000 `[OA]`.
4. Ponty, Y., Mininni, P. D., Montgomery, D. C., Pinton, J.-F., Politano, H., Pouquet, A. (2005). *Numerical study
   of dynamo action at low magnetic Prandtl numbers.* PRL 94, 164502, doi:10.1103/PhysRevLett.94.164502.
   Taylor–Green forcing (zero net helicity): Rm_c = 30 at Pm = 1, 226 at Pm = 0.3, then a plateau Rm_c ≈ 150 in LES
   for 10⁻² ≤ Pm ≤ 10⁻¹ `[site: specs/sources/dynamo.md:573-595]`.
5. Iskakov, A. B., Schekochihin, A. A., Cowley, S. C., McWilliams, J. C., Proctor, M. R. E. (2007). *Numerical
   demonstration of fluctuation dynamo at low magnetic Prandtl numbers.* PRL 98, 208501,
   doi:10.1103/PhysRevLett.98.208501 `[CR]`. Dynamo exists for Rm ≫ 1, Pm ≪ 1; Rm_c ≲ 200 for Re ≳ 6000 against
   ≈ 60 for Pm ≥ 1 `[OA]`. Detailed report: Schekochihin et al. (2007), NJP 9, 300 `[CR][OA]`.
6. Warnecke, J., Korpi-Lagg, M. J., Gent, F. A., Rheinhardt, M. (2023). *Numerical evidence for a small-scale
   dynamo approaching solar magnetic Prandtl numbers.* Nature Astronomy 7, 662–668,
   doi:10.1038/s41550-023-01975-1 `[CR]`. Small-scale dynamo down to Pm = 0.0031, easier to excite below
   Pm ≈ 0.05 (bottleneck effect) `[OA]`.

**State in 2026.** Kinematic theory is mature; the turbulent, nonlinear and low-Pm regimes remain "uncertain"
(Tobias 2021 §10) `[FT: Tobias]`. Tobias lists four issues: turbulence at extreme Pm, large-scale organisation,
saturation, and rotation (§3.1–3.4) `[FT: Tobias]`.

**Supervisors' published contributions in this track.** C. Nore: Taylor–Green dynamo near threshold (Nore et al.
1997, above `[CR][OA]`). Y. Ponty: low-Pm Taylor–Green dynamos (Ponty et al. 2005; Ponty et al. 2007, NJP 9, 296,
fluctuations push the threshold onto the upper kinematic branch), subcritical Taylor–Green bifurcation (Ponty et
al. 2007, PRL 99, 224501), transition from large- to small-scale dynamo with a Roberts-type forcing (Ponty &
Plunian 2011, PRL 106, 154502), on-off intermittency near the ABC threshold (Alexakis & Ponty 2008, PRE 77,
056308), systematic route to subcritical branches by nonlinear optimisation (Mannix, Ponty & Marcotte 2022, PRL
129, 024502), intermittency in fast-dynamo regimes (Ponty, Politano & Pouquet 2025, JPP 91, E69)
`[site: specs/sources/encadrants.md:279-296]`. S. Cheng, D. Lucor: no dynamo-theory publication found
`[site: specs/sources/encadrants.md:103]`.

### 3.2 Track 2: Laboratory dynamos

**Question.** Can a dynamo be built, and what does a real, turbulent, low-Pm dynamo do near and above threshold?
The obstacle: Pm ≈ 10⁻⁵ for sodium, so Rm of a few tens means Re of millions and around a hundred kilowatts of
power `[site: en/prep/p3-mhd-dynamo/index.qmd:1145]`.

1. Lowes, F. J., Wilkinson, I. (1963). *Geomagnetic dynamo: a laboratory model.* Nature 198, 1158–1160,
   doi:10.1038/1981158a0; and (1968) *Geomagnetic dynamo: an improved laboratory model*, Nature 219, 717–718,
   doi:10.1038/219717a0 `[CR]`. Herzenberg-type "quasi-homogeneous" dynamos made of rotating soft-iron cylinders
   in blocks of the same material; hysteresis and rigid saturation, but step-by-step improvement produced "a sort
   of reversals" (Wilkinson 1984) `[FT: Stefani et al. 2018 §2.1]`. Note: Stefani et al. date the second paper
   1967 in the text; Crossref gives August 1968.
2. Riga (Ponomarenko-type helical flow): Gailitis, A., Lielausis, O., Dement'ev, S., Platacis, E., Cifersons, A.,
   Gerbeth, G., Gundrum, T., Stefani, F., Christen, M., Hänel, H., Will, G. (2000). *Detection of a flow induced
   magnetic field eigenmode in the Riga dynamo facility.* PRL 84, 4365–4368, doi:10.1103/PhysRevLett.84.4365.
   First self-excited eigenmode, 11 Nov. 1999, growth rate 0.0315 s⁻¹, 1.326 Hz; saturation reached July 2000
   (Gailitis et al. 2001, PRL 86, 3024) `[site: specs/sources/dynamo.md:51-74]`. Campaigns continued to 2016–2017
   `[FT: Stefani et al. 2018 §2.1]`.
3. Karlsruhe (Roberts–Busse two-scale flow): Stieglitz, R., Müller, U. (2001). *Experimental demonstration of a
   homogeneous two-scale dynamo.* Phys. Fluids 13, 561–564, doi:10.1063/1.1331315; first run December 1999;
   steady dipole-like field (Müller et al. 2008, C. R. Physique 9, 729–740) `[site: specs/sources/dynamo.md:85-107]`.
4. VKS (von Kármán sodium, Cadarache): Monchaux, R., et al. (2007). *Generation of a magnetic field by dynamo
   action in a turbulent flow of liquid sodium.* PRL 98, 044502, doi:10.1103/PhysRevLett.98.044502 (16 authors).
   First dynamo in a strongly turbulent flow; only with soft-iron impellers; Rm_c ≈ 31 (definition with K = 0.6)
   `[site: specs/sources/dynamo.md:111-136]`. Berhanu, M., et al. (2007), *Magnetic field reversals in an
   experimental turbulent dynamo*, EPL 77, 59001, doi:10.1209/0295-5075/77/59001: first laboratory reversals,
   ⟨T+⟩ = 120 s, ⟨T−⟩ = 50 s, reversal duration ≈ 5 s `[site: specs/sources/dynamo.md:138-153]`. Monchaux et al.
   (2009), Phys. Fluids 21, 035108: low-dimensional dynamics despite turbulence `[site: specs/sources/dynamo.md:155-166]`.
   Precursors: VKS1 induction measurements up to Rm ≈ 50 without dynamo (Bourgoin, M., et al. 2002, Phys. Fluids
   14, 3046–3058, doi:10.1063/1.1497376 `[CR][OA]`); impeller optimisation for VKS2 (Ravelet, F., Chiffaudel, A.,
   Daviaud, F., Léorat, J. 2005, Phys. Fluids 17, 117104, doi:10.1063/1.2130745 `[CR][OA]`). Threshold reached in
   2006 `[FT: Stefani et al. 2018 §2.1]`. Later regimes: Aumaître et al. (2008), C. R. Physique 9, 689–701,
   doi:10.1016/j.crhy.2008.07.002 `[CR][OA]`; Berhanu et al. (2010), EPJB 77, 459–468,
   doi:10.1140/epjb/e2010-00272-5 `[CR]`; Boisson et al. (2012); Miralles et al. (2013) `[site: specs/sources/dynamo.md:168-184]`.
5. Experiments without self-excitation that measured turbulent induction: Madison sphere (Spence, E. J., Nornberg,
   M. D., Jacobson, C. M., Kendrick, R. D., Forest, C. B. 2006, *Observation of a turbulence-induced large scale
   magnetic field*, PRL 96, 055002, doi:10.1103/PhysRevLett.96.055002 `[CR][OA]`: an induced dipole that no
   axisymmetric laminar flow can produce, i.e. a turbulent EMF); Perm braked torus (Frick, P., Noskov, V.,
   Denisov, S., Stepanov, R. 2010, *Direct measurement of effective magnetic diffusivity in turbulent flow of liquid
   sodium*, PRL 105, 184502, doi:10.1103/PhysRevLett.105.184502 `[CR][OA]`: Re ≈ 3×10⁶, Rm ≈ 30, effective
   diffusivity up to ≈ 50 % above laminar); Maryland 3 m sphere (Zimmerman, D. S., Triana, S. A., Nataf, H.-C.,
   Lathrop, D. P. 2014, JGR Solid Earth 119, 4538–4557, doi:10.1002/2013JB010733 `[CR]`, content not read).
   The MilaDy abstract counts "only three" sodium experiments that obtained a dynamo
   `[site: specs/sources/encadrants.md:56]`.
6. DRESDYN (HZDR, Dresden): Stefani, F., Eckert, S., Gerbeth, G., Giesecke, A., Gundrum, Th., Steglich, C., Weier, T., Wustmann, B.
   (2012). *DRESDYN – a new facility for MHD experiments with liquid sodium.* Magnetohydrodynamics 48(1), 103–114,
   doi:10.22364/mhd.48.1.13 `[CR][OA]`. Two flagship projects: a dynamo driven solely by precession, and a large
   Taylor–Couette experiment combining the magnetorotational and Tayler instabilities `[OA]`. Design: cylinder
   ≈ 2 m, rotation up to 10 Hz, precession up to 1 Hz, 8 t of sodium `[FT: Pizzi et al. 2023, arXiv:2301.08076]`
   (6 t in `[FT: Stefani et al. 2018 §3.1]`: discrepancy). Tayler instability first shown in a GaInSn column with
   currents up to 8 kA (Seilmayer, M., et al. 2012, PRL 108, 244501, doi:10.1103/PhysRevLett.108.244501 `[CR][OA]`).
   Status: building finalized 2017 `[FT: Stefani 2018]`; experiment "being set up" in April 2025
   `[FT: arXiv:2410.14449v3]`; **no report of a first sodium run found as of 2026-11-08 [UNVERIFIED status]**.
   Precursor: Gans (1971) sodium precession, field amplification by 3 `[sec: Stefani 2018 §2.1]`.
7. Plasma dynamos (outside liquid metals): Tzeferacos, P., et al. (2018), *Laboratory evidence of dynamo
   amplification of magnetic fields in a turbulent plasma*, Nat. Commun. 9, 591, doi:10.1038/s41467-018-02953-2
   `[CR][OA]` (laser-driven colliding plasmas, amplification to near equipartition); Bott, A. F. A., et al. (2021),
   PNAS 118, e2015729118 `[CR]`; Madison Plasma Dynamo Experiment (Cooper, C. M., et al. 2014, Phys. Plasmas 21,
   013505, doi:10.1063/1.4861609 `[CR][OA]`, design target Rm > 1000).

Reviews: Gailitis, A., Lielausis, O., Platacis, E., Gerbeth, G., Stefani, F. (2002), *Colloquium: Laboratory
experiments on hydromagnetic dynamos*, Rev. Mod. Phys. 74, 973–990, doi:10.1103/RevModPhys.74.973 `[CR][OA]`;
Stefani, F., Gailitis, A., Gerbeth, G. (2008), ZAMM 88, 930–954, doi:10.1002/zamm.200800102 `[CR]`; Pétrélis,
Mordant & Fauve (2007), GAFD 101, 289–323 `[site: specs/sources/dynamo.md:249-252]`; Lathrop, D. P., Forest, C. B.
(2011), *Magnetic dynamos in the lab*, Physics Today 64(7), 40–45, doi:10.1063/PT.3.1166 `[CR]`.

**State in 2026.** Three liquid-sodium dynamos; the only turbulent one (VKS) needs ferromagnetic impellers, and why
the field topology differs from the predictions "is still a matter of ongoing research" `[FT: Stefani 2018 §2.1]`;
Tobias even asks whether VKS "can be classed as a dynamo in the strictest sense" `[FT: Tobias §9]`. The first
homogeneous, impeller-free dynamo (DRESDYN precession) is still pending.

**Supervisors' contributions.** None of the four supervisors is an author of the experimental papers above.
Their contributions to this track are numerical models of the experiments (track 3): VKS impellers and
boundary conditions (Nore, Ponty) and the precession dynamo for DRESDYN (Nore, with Giesecke and Stefani: Stefani
et al. 2015, MHD 51, 275–284; Botez et al. 2026) `[site: specs/sources/encadrants.md:236-258]`.

### 3.3 Track 3: Numerical dynamos

**Question.** Can the full nonlinear MHD equations reproduce natural and laboratory dynamos, given that real
parameters are out of reach?

*3a. Planetary (geodynamo) simulations*

1. Glatzmaier, G. A., Roberts, P. H. (1995). *A three-dimensional self-consistent computer simulation of a
   geomagnetic field reversal.* Nature 377, 203–209, doi:10.1038/377203a0 `[CR]` (Crossref misspells the first
   author "Glatzmaiers"). Rotating anelastic convection, field resembling the Earth's, reversing fields; start of
   the "modern era" of geodynamo modelling `[FT: Tobias §8.3]`. Abstract (paywalled) known from search excerpts:
   several polarity excursions, then a successful reversal near the end of the run `[sec, UNVERIFIED wording]`.
   Same year: Kageyama, A., Sato, T. (1995), Phys. Plasmas 2, 1421–1431, doi:10.1063/1.871485 `[CR][OA]`.
2. Christensen, U. R., Aubert, J., Cardin, P., Dormy, E., Gibbons, S., Glatzmaier, G. A., Grote, E., Honkura, Y.,
   et al. (2001). *A numerical dynamo benchmark.* PEPI 128, 25–34, doi:10.1016/S0031-9201(01)00275-8 `[CR]`. One
   non-magnetic convection case and two dynamo cases (insulating or conducting inner core), E = 10⁻³
   `[sec: search excerpts of the abstract and of the CIG benchmark page; UNVERIFIED in the primary]`. Followed by
   anelastic benchmarks (Jones, C. A., et al. 2011, Icarus 216, 120–135, doi:10.1016/j.icarus.2011.08.014 `[CR]`)
   and performance benchmarks of 15 codes up to 16 384 cores (Matsui, H., et al. 2016, G-cubed 17, 1586–1607,
   doi:10.1002/2015GC006159 `[CR][OA]`).
3. Kutzner, C., Christensen, U. R. (2002). *From stable dipolar towards reversing numerical dynamos.* PEPI 131,
   29–45, doi:10.1016/S0031-9201(02)00016-X `[CR]`. Dipolar at low Rayleigh number, multipolar at high, reversals
   and excursions in between `[OA]`.
4. Schaeffer, N., Jault, D., Nataf, H.-C., Fournier, A. (2017). *Turbulent geodynamo simulations: a leap towards
   Earth's core.* GJI 211, 1–29, doi:10.1093/gji/ggx265 `[CR]`: Pm = 0.1, Rm > 500, E = 10⁻⁷ `[OA]`; and Aubert,
   J., Gastine, T., Fournier, A. (2017), JFM 813, 558–593, doi:10.1017/jfm.2016.789 `[CR][OA]` (path in parameter
   space toward the asymptotic MAC regime). Earth's core: E = O(10⁻¹⁵), Pm = O(10⁻⁶)
   `[site: en/prep/p3-mhd-dynamo/index.qmd:1353]`.

*3b. Turbulent and experimental-geometry simulations*

1. Meneguzzi, M., Frisch, U., Pouquet, A. (1981). *Helical and nonhelical turbulent dynamos.* PRL 47, 1060–1064,
   doi:10.1103/PhysRevLett.47.1060 `[CR]` `[FT: Rincon §1.4]`.
2. Taylor–Green as a von Kármán proxy: Nore et al. (1997) above; Ponty et al. (2005) `[site]`; Mininni, P. D.,
   Ponty, Y., Montgomery, D. C., Pinton, J.-F., Politano, H., Pouquet, A. (2005), *Dynamo regimes with a
   nonhelical forcing*, ApJ 626, 853–863, doi:10.1086/429911 `[CR][OA]`; Krstulovic, G., Thorner, G., Vest, J.-P.,
   Fauve, S., Brachet, M. (2011), *Axial dipolar dynamo action in the Taylor–Green vortex*, PRE 84, 066318,
   doi:10.1103/PhysRevE.84.066318 `[CR][OA]` (symmetries mimic realistic boundaries; a VKS-like axial dipole).
3. Role of the ferromagnetic impellers: Laguerre, R., Nore, C., Ribeiro, A., Léorat, J., Guermond, J.-L., Plunian, F.
   (2008), PRL 101, 104501 (α effect of the blades plus ferromagnetic conditions reach Rm_c ≈ 32); Giesecke, A.,
   Stefani, F., Gerbeth, G. (2010), PRL 104, 044503 (soft iron favours m = 0); Giesecke et al. (2012), NJP 14,
   053005 `[site: specs/sources/dynamo.md:188-196; specs/sources/encadrants.md:250-252]`.
4. SFEMaNS simulations of VKS: Nore, C., Castanon Quiroz, D., Cappanera, L., Guermond, J.-L. (2016), EPL 114, 65002
   (first nonlinear DNS with the impellers; threshold falls as impeller permeability rises) and (2018), JFM 854,
   164–195 (Rm_c → ≈ 70 at large Re, within the experimental 52–71; pseudo-vacuum vs vacuum conditions shift Rm_c
   by ≈ 40 %) `[site: specs/sources/dynamo.md:198-233]`. Code: Guermond et al. (2007, 2009, 2011), JCP
   `[site: specs/sources/dynamo.md:531-535]`.
5. LATU (pseudo-spectral with volume penalisation, H. Homann's code): Kreuzahler, S., Schulz, D., Homann, H.,
   Ponty, Y., Grauer, R. (2014), NJP 16, 103001; Kreuzahler, S., Ponty, Y., Plihon, N., Homann, H., Grauer, R.
   (2017), *Dynamo enhancement and mode selection triggered by high magnetic permeability*, PRL 119, 234501,
   doi:10.1103/PhysRevLett.119.234501 `[site: specs/sources/dynamo.md:235-245; en/prep/p3-mhd-dynamo/index.qmd:1360]`.
6. Reversals in simulations: Gissinger, C., Dormy, E., Fauve, S. (2010), EPL 90, 49001 (at Pm < 0.5 reversals
   involve the axial dipole and quadrupole) `[site: specs/sources/dynamo.md:291-304]`; Nore, C., Guermond, J.-L.,
   Laguerre, R., Léorat, J., Luddens, F. (2012), Phys. Fluids 24, 094106 (aperiodic reversals of the axial dipole
   in a short Taylor–Couette dynamo) `[site: specs/sources/encadrants.md:248]`; Bousquet, R., Ponty, Y., Botez, V.,
   Plihon, N., Nore, C. (2026), *Magnetic field reversals in numerical simulations of the von Kármán sodium
   experiment*, PRFluids 11, 063703, doi:10.1103/9tx2-1m13 (both solvers; Re = 1594, Rm = 531, asymmetry 0.058,
   μr = 16; five-stage mechanism) `[site: specs/sources/encadrants.md:227-235]`.
7. Precession: Nore, C., Léorat, J., Guermond, J.-L., Luddens, F. (2011), PRE 84, 016317; Cappanera et al. (2016),
   PRE 93, 043113; Giesecke, A., Vogt, T., Gundrum, T., Stefani, F. (2018), PRL 120, 024502; Botez, V., Giesecke, A.,
   Nore, C., Cappanera, L., Stefani, F. (2026), PRFluids 11, 083701, doi:10.1103/rx1h-5zxp (narrow Poincaré-number
   range; simplified vanishing-tangential-field conditions systematically underestimate Rm_c)
   `[site: specs/sources/encadrants.md:236-246,259]`; Giesecke, A., Wilbert, M., Šimkanin, J., Grauer, R.,
   Stefani, F. (2024–2025), arXiv:2410.14449 (kinematic vs self-consistent; onset minimum in the transitional
   regime; absolute Rm_c depends on the outer layers) `[AX][FT]`.

**State in 2026.** Geodynamo models reach E = 10⁻⁷ to 10⁻⁸, still far from 10⁻¹⁵; Tobias: simulations are "too
viscous and too slowly rotating" for planets and "too laminar and too diffusive" for stars `[FT: Tobias §10]`.
Simulations of the experiments reproduce thresholds and reversals but at Re ≈ 10³ instead of 10⁶–10⁷, and their
datasets are not public (Bousquet et al. 2026) `[site: en/rapport/index.qmd:161]`.

**Supervisors' contributions.** C. Nore: SFEMaNS foundations (with Guermond), VKS simulations (2008, 2012, 2015,
2016, 2018), precession dynamos (2011, 2016, 2026), Taylor–Couette dynamo (2012), local energy transfers (Creff et
al. 2024, Phys. Plasmas 31, 022306), POD of VKS (Botez, Bousquet & Nore 2025), VKS reversals (Bousquet et al. 2026)
`[site: specs/sources/encadrants.md:217-264]`. Y. Ponty: low-Pm Taylor–Green and ABC dynamos (2005–2011), LATU
simulations of VKS (Kreuzahler et al. 2014, 2017), Lagrangian statistics of the Taylor–Green dynamo (Homann et al.
2014), VKS reversals (Bousquet et al. 2026) `[site: specs/sources/encadrants.md:279-297]`. D. Lucor: co-author of
LES/POD analyses of turbulent von Kármán flows (Bousquet, Chaffard, Creff, Lucor, Nore 2024, Phys. Fluids 36,
105133; hydrodynamic, Rπ-breaking metastable state) `[site: specs/sources/encadrants.md:186]`. S. Cheng: none in
this track `[site: specs/sources/encadrants.md:103]`.

### 3.4 Track 4: Reduced models of reversals

**Question.** Why does a turbulent system, symmetric under B → −B, flip between two polarities, and can a few
equations capture it?

1. Disc dynamos: Bullard, E. (1955), *The stability of a homopolar dynamo*, Math. Proc. Camb. Phil. Soc. 51,
   744–760, doi:10.1017/S0305004100030814 `[CR]`; Rikitake, T. (1958), *Oscillations of a system of disk dynamos*,
   Math. Proc. Camb. Phil. Soc. 54, 89–105, doi:10.1017/S0305004100033223 `[CR]`: two coupled disc dynamos show
   reversals of current and field, unlike a single one `[OA]`. Nozières, P. (1978), PEPI 17, 55–74,
   doi:10.1016/0031-9201(78)90047-X `[CR]` (relaxation model; content not read; cited as a neighbour of the
   Gissinger model `[site: specs/sources/dynamo.md:324]`).
2. Stochastic mean-field models: Hoyng, P., Ossendrijver, M. A. J. H., Schmitt, D. (2001), *The geodynamo as a
   bistable oscillator*, GAFD 94, 263–314, doi:10.1080/03091920108203410 `[CR]`: a fluctuating α reproduces
   quadrupolar-looking reversals, aborted reversals, excursions and Poisson-distributed intervals `[OA]`. Stefani,
   F., Xu, M., Sorriso-Valvo, L., Gerbeth, G., Günther, U. (2007), GAFD 101, 227–248,
   doi:10.1080/03091920701523311 `[CR][AX]` (arXiv:physics/0701026 has a different title, *Reversals in nature
   and the nature of reversals*; Crossref title: *Oscillation or rotation: a comparison of two simple reversal
   models*: title discrepancy noted).
3. Symmetry-based normal form: Pétrélis, F., Fauve, S. (2008), J. Phys.: Condens. Matter 20, 494203: dipole and
   quadrupole A = D + iQ, phase equation θ̇ = μᵢ − ρ sin 2θ, saddle-node at μᵢ = ρ, noise-driven random reversals
   below it; Pétrélis, F., Fauve, S., Dormy, E., Valet, J.-P. (2009), PRL 102, 144503: application to the Earth,
   P[T] ∝ exp(−T/⟨T⟩) `[site: specs/sources/dynamo.md:260-287]`.
4. Deterministic chaos: Gissinger, C. (2012), *A new deterministic model for chaotic reversals*, EPJB 85, 137,
   doi:10.1140/epjb/e2012-20799-5: Q̇ = μQ − VD, Ḋ = −νD + VQ, V̇ = Γ − V + QD; crisis at μc ≈ 0.11928; Poisson
   waiting times at long times `[site: specs/sources/dynamo.md:308-367]`; earlier version in Gissinger, Dormy &
   Fauve (2010) `[site]`. A related minimal-model study links the regularity of reversal sequences to a "ghost
   limit cycle" (Breno Raphaldini, Everton S. Medeiros, David Ciro, Daniel Ribeiro Franco, Ricardo Ivan Ferreira Trindade 2020, arXiv:2006.15420,
   *Geomagnetic reversals at the edge of regularity*) `[AX][FT abstract]` (journal version not checked).
5. Data-driven reduced models: SINDy (Brunton, S. L., Proctor, J. L., Kutz, J. N. 2016, PNAS 113, 3932–3937,
   doi:10.1073/pnas.1517384113 `[CR]`) and its constrained Galerkin form with energy-preserving quadratic terms
   (Loiseau, J.-C., Brunton, S. L. 2018, *Constrained sparse Galerkin regression*, JFM 838, 42–67,
   doi:10.1017/jfm.2017.823 `[CR][OA]`). **DQVU** (Bousquet et al. 2026): POD of 2000 snapshots of VKS
   simulations, four axisymmetric modes (D, Q, V, U), Galerkin model whose coefficients are identified by
   constrained regression (PySINDy) under two constraints (quadratic energy conservation, third-moment
   constraint); reproduces the asymmetric bimodal distribution of V, which DQV does not
   `[site: specs/sources/encadrants.md:227-235; en/prep/p3-mhd-dynamo/index.qmd:1347]`. Elsewhere: DMD + SINDy
   recover dynamo-cycle equations for a 1D mean-field α–Ω model (Guseva, A., Skene, C., Tobias, S. M. 2026,
   arXiv:2603.29079, preprint) `[AX]`; reversals in 2D convection analysed with complex networks (Yang & Schmid
   2025, JFM 1011, A30) `[site: specs/sources/encadrants.md:90]`.
6. Machine learning for prediction: Gwirtz, K., Davis, T., Morzfeld, M., Constable, C., Fournier, A., Hulot, G.
   (2022). *Can machine learning reveal precursors of reversals of the geomagnetic axial dipole field?* GJI 231,
   520–535, doi:10.1093/gji/ggac195 `[CR]`. SVMs and LSTMs on models (from simple to 3D geodynamo) and on PADM2M
   and Sint-2000; rare-event imbalance needs a training tweak; the usable observational record (0–2 Ma) has only
   five reversals; predictability varies across models and records `[OA]`.

**State in 2026.** Low-dimensional models explain the qualitative features (bimodality, overshoot, excursions,
role of symmetry breaking) but are phenomenological; DQVU is the first VKS model derived from simulations and
identified under constraints, still deterministic and fitted on one parameter point (the regression is described
at a reference simulation `[site: specs/sources/encadrants.md:230-234]`; extension across parameters is not
reported there).

**Supervisors' contributions.** C. Nore and Y. Ponty: DQVU (Bousquet et al. 2026). C. Nore and D. Lucor: POD and
autoencoder representations of forced flows and VKS (Bousquet, Nore & Lucor 2025, CPC 315, 109728; Botez, Bousquet
& Nore 2025) `[site: specs/sources/encadrants.md:180-185,241]`. Y. Ponty: on-off intermittency (rare bursts) near
threshold (Alexakis & Ponty 2008) `[site: specs/sources/encadrants.md:285]`. S. Cheng: no reversal model; data
assimilation and latent reduced models in other fields `[site: specs/sources/encadrants.md:107-160]`.

### 3.5 Track 5: Statistics of reversals

**Question.** How often does the field flip, is the timing random, and what does the record allow us to infer?

1. Discovery and dating: Brunhes (1906) `[CR]`; Matuyama (1929) `[CR]`; Vine, F. J., Matthews, D. H. (1963),
   *Magnetic anomalies over oceanic ridges*, Nature 199, 947–949, doi:10.1038/199947a0 `[CR]`; Cox, A., Doell,
   R. R., Dalrymple, G. B. (1964), *Reversals of the Earth's magnetic field*, Science 144, 1537–1543,
   doi:10.1126/science.144.3626.1537 `[CR]`; evidence "not generally accepted as conclusive until the 1960's"
   `[FT: Constable 2003 §1]`.
2. Poisson-type modelling: Cox, A. (1968), *Lengths of geomagnetic polarity intervals*, JGR 73, 3247–3260,
   doi:10.1029/JB073i010p03247 `[CR]`: Bernoulli-trial model, probability p ≈ 0.05 per dipole cycle over the last
   10 Myr, at least 100 times smaller in the Permian `[OA]`. Since Cox (1968), reversals are treated as
   "uncorrelated, triggered events described by a Poisson process with a varying rate parameter"
   `[FT: Constable 2003 §4.1]`.
3. Time scales and varying rate: Cande, S. C., Kent, D. V. (1995), JGR 100, 6093–6095, doi:10.1029/94JB03098 `[CR]`
   (CK95); Constable, C. (2000), *On rates of occurrence of geomagnetic reversals*, PEPI 118, 181–193,
   doi:10.1016/S0031-9201(99)00139-9 `[CR]`: over 0–158 Ma the derivative of the rate changed sign at least once,
   with zero rate during the Cretaceous Normal Superchron (≈ 40 Myr, ending ≈ 83 Ma) `[FT: Constable 2003 §1, §4.1]`;
   Ogg, J. G. (2020), *Geomagnetic Polarity Time Scale*, in *Geologic Time Scale 2020*, pp. 159–192,
   doi:10.1016/B978-0-12-824360-2.00005-X `[CR]` (not read). Mean rate ≈ 5 per Myr over the last few Myr; CNS
   ≈ 118–83 Myr and Kiaman ≈ 312–262 Myr `[FT: Stefani et al. 2007 arXiv §1]` (Constable gives 302–252 Ma for
   the Permo-Carboniferous superchron: discrepancy).
4. Beyond Poisson: Carbone, V., Sorriso-Valvo, L., Vecchio, A., Lepreti, F., Veltri, P., Harabaglia, P., Guerra, I.
   (2006), *Clustering of polarity reversals of the geomagnetic field*, PRL 96, 128501,
   doi:10.1103/PhysRevLett.96.128501 `[CR]`: strong departure from Poisson statistics, temporal clustering, Lévy
   statistics, long-range correlations `[OA]`; Jonkers, A. R. T. (2003), PEPI 135, 253–266,
   doi:10.1016/S0031-9201(03)00036-0 `[CR]` (title: long-range dependence; not read); Sorriso-Valvo et al. (2007),
   PEPI 164, 197–207, doi:10.1016/j.pepi.2007.07.001 `[CR]` (not read).
5. Records of individual reversals: Valet, J.-P., Meynadier, L., Guyodo, Y. (2005), *Geomagnetic dipole strength
   and reversal rate over the past two million years*, Nature 435, 802–805, doi:10.1038/nature03674 `[CR]`
   (SINT-2000; abstract not read); Valet, J.-P., Fournier, A. (2016), *Deciphering records of geomagnetic
   reversals*, Rev. Geophys. 54, 410–446, doi:10.1002/2015RG000506 `[CR]`: questions remain on the dynamical
   processes; reversals are fast and weak-field recording is unreliable `[OA]`; Singer, B. S., Jicha, B. R.,
   Mochizuki, N., Coe, R. S. (2019), Sci. Adv. 5, eaaw4621 `[CR]`: final 180° flip at ≈ 773 ka after a process
   starting ≈ 795 ka, ≈ 22 kyr in all, mirrored by a geodynamo simulation `[OA]`.
6. Laboratory and model statistics: VKS ⟨T+⟩ = 120 s, ⟨T−⟩ = 50 s at F1 = 16 Hz, F2 = 22 Hz (Berhanu 2007)
   `[site: specs/sources/dynamo.md:147-153]`; Gissinger (2012): waiting times quantised at short times,
   Poissonian at long times, τ ∼ (μ − μc)^(−γ), γ ≃ 1/2 "difficult to conclude" `[site: specs/sources/dynamo.md:345-363]`;
   Pétrélis et al. (2009): Kramers-type ⟨T⟩ formula, ⟨T⟩ ≈ 170 kyr with fitted parameters
   `[site: specs/sources/dynamo.md:282-285]`; Hoyng et al. (2001): Poisson intervals in a stochastic model `[OA]`.

**State in 2026.** The polarity record is well dated for the last ≈ 160 Myr (Gwirtz et al. 2022 `[OA]`) but short
for statistics of what precedes a reversal; whether the process is Poisson with a slowly varying rate or
clustered with long memory remains debated (Constable vs Carbone et al.).

**Supervisors' contributions.** None in paleomagnetic statistics. In the laboratory and simulation sense, Nore and
Ponty's Bousquet et al. (2026) characterise reversal sequences and the bimodal distribution of the modes in VKS
simulations `[site: specs/sources/encadrants.md:227-235]`.

---

## 4. Open problems (as stated in sources read today or in the site)

1. **Low-Pm dynamos with mean flows and fluctuations.** The small-scale dynamo at Pm ≪ 1 now looks possible
   (Iskakov 2007; Warnecke 2023), but turbulent fluctuations raise thresholds of mean-flow dynamos (≈ 8× for
   Taylor–Green, Ponty et al. 2007 `[site: specs/sources/dynamo.md:605]`) and VKS needs magnetic impellers
   `[FT: Tobias §9]`. Tobias calls the theory of turbulent dynamos "uncertain" `[FT: Tobias §10]`.
2. **The parameter gap.** Earth's core E ≈ 10⁻¹⁵, Pm ≈ 10⁻⁶ vs E ≈ 10⁻⁷, Pm = 0.1 in the best runs
   `[site: en/prep/p3-mhd-dynamo/index.qmd:1353]`; simulations "too viscous and too slowly rotating"
   `[FT: Tobias §10]`.
3. **Mechanism and predictability of reversals.** No means yet of identifying when the field "has entered a
   transitional state destined to lead to a reversal" `[FT: Constable 2003, abstract]`; "questions remain regarding
   the dynamical processes" `[OA: Valet & Fournier 2016]`; ML precursor detection limited by five reversals in
   0–2 Ma `[OA: Gwirtz 2022]`.
4. **Reversal statistics.** Poisson with varying rate (Constable) vs clustering / long-range dependence (Carbone
   2006; Jonkers 2003); causes of rate changes and superchrons (core–mantle boundary, mantle plumes, or chaos
   alone) cannot be ruled in or out `[FT: Constable 2003 §4.1]`.
5. **The VKS puzzle.** Why soft-iron impellers are needed and why the observed axisymmetric dipole differs from
   kinematic predictions is "still a matter of ongoing research" `[FT: Stefani 2018 §2.1]`; boundary conditions
   shift numerical thresholds by tens of percent (Nore 2018: ≈ 40 %) `[site: specs/sources/dynamo.md:517]`.
6. **A homogeneous laboratory dynamo.** Precession dynamo not yet demonstrated; onset depends on outer layers and
   boundary conditions in simulations (Botez 2026; Giesecke 2025 `[AX]`); DRESDYN status unconfirmed.
7. **From simulations to reduced and statistical models.** Simulation data are expensive and private
   (Bousquet 2026); reduced models are fitted at single parameter points; no diffusion or flow-matching model trained
   on dynamo simulations was found (negative claim, cannot be proved) `[site: en/these/index.qmd:163;
   specs/sources/litterature.md:378,476]`.

---

## 5. Which tracks MilaDy and the thesis build on

| Track | What MilaDy / the thesis takes from it | Supervisors' published work in the track | Gap the thesis targets |
|---|---|---|---|
| 1 Theory | Kinematic eigenvalue σ(Rm) and thresholds (E3, ABC windows) `[site: en/these/index.qmd:97]`; anti-dynamo theorems explain why 2D fields must be forced (tier 1) `[site: en/these/index.qmd:894]`; low Pm motivates conditioning on Re, Rm, μr `[site: en/prep/p3-mhd-dynamo/index.qmd:1586]` | Nore 1997 (TG); Ponty 2005–2025 (low Pm, subcritical, on-off) | Generator that crosses a threshold; error bound near a jump of the distribution (Q3) `[site: en/these/index.qmd:126-131]` |
| 2 Laboratory | VKS (reversals, impellers) and DRESDYN (precession) are the two MilaDy objectives `[site: specs/sources/encadrants.md:29]` | none experimental; numerical models of both | Parametric exploration of DRESDYN with ROMs (tier 4) `[site: en/these/index.qmd:943]` |
| 3 Numerical | SFEMaNS and LATU data (tier 3); Taylor–Green and ABC periodic dynamos (tier 2) `[site: en/these/index.qmd:906-929]` | Nore (SFEMaNS, VKS, precession); Ponty (LATU, TG, ABC); Lucor (VK LES/POD) | Hard ∇·B = 0 / ∇·u = 0 in bounded cylinders with μr jumps and vacuum matching (Q1) `[site: en/these/index.qmd:111]` |
| 4 Reduced models | Gissinger model (E1, tier 0) and DQVU `[site: en/these/index.qmd:878-880]`; Q4: identify a DQVU-type model from generated snapshots `[site: en/these/index.qmd:135]` | Nore, Ponty (DQVU 2026); Nore, Lucor (POD/AE 2025) | Distributional (stationarity) constraints on a parametric generator; symmetry by equivariance `[site: en/rapport/index.qmd:118-125]` |
| 5 Statistics | Poisson-type waiting times as the benchmark of reversal statistics; Rice formula gives the mean crossing frequency from snapshots, but not the waiting-time distribution `[site: en/these/index.qmd:78-80,131]` | none paleomagnetic; Bousquet 2026 (simulated reversal statistics) | Reversal frequency without time integration (Q3) `[site: en/these/index.qmd:152]` |

In short: MilaDy is anchored in tracks 2 (VKS, DRESDYN), 3 (SFEMaNS, LATU) and 4 (DQVU), with Cheng and Lucor
bringing the data-driven side (latent models, data assimilation) that the dynamo tracks have only just started to
use (2022–2026: Gwirtz, Bousquet, Guseva). The thesis places a conditional generative model between track 3 (the
simulations) and tracks 4–5 (reduced dynamics and reversal statistics).

---

## 6. Verification log

- **Checked today in Crossref (about 80 DOI lookups, plus given names of the authors cited with initials):** all
  DOIs cited above outside the `[site]` marks. DOIs that differed from a first guess and were fixed by a Crossref
  search: Childress (1970) is 10.1063/1.1665095 (not …094); Nore et al. (1997) is
  10.1063/1.872578; Nozières (1978) is 10.1016/0031-9201(78)90047-X; Hoyng et al. (2001) is
  10.1080/03091920108203410; Berhanu et al. (2010) is 10.1140/epjb/e2010-00272-5; Stefani et al. (2019) GAFD is
  10.1080/03091929.2018.1501481; Jonkers (2003) is 10.1016/S0031-9201(03)00036-0; Taylor & Green (1937) is
  10.1098/rspa.1937.0036.
- **Abstracts read today (OpenAlex):** Herzenberg 1958, Rikitake 1958, Childress 1970, Soward 1987, Nore 1997,
  Kageyama 1995, Bourgoin 2002, Kutzner 2002, Boldyrev 2004, Schekochihin 2004/2005/2007, Iskakov 2007, Mininni
  2005, Ravelet 2005, Spence 2006/2008, Carbone 2006, Hoyng 2001, Cox 1968, Frick 2010, Krstulovic 2011, Seilmayer
  2012, Stefani 2012/2019, Gailitis 2002, Aumaître 2008, Matsui 2016, Schaeffer 2017, Aubert 2017, Loiseau 2018,
  Tzeferacos 2018, Cooper 2014, Singer 2019, Valet 2016, Dormy 2000, Gwirtz 2022, Warnecke 2023.
- **Full texts read today:** Rincon 2019 (arXiv), Tobias 2021 (arXiv), Stefani et al. 2018 (arXiv:1803.03421),
  Constable preprint (2001), Stefani et al. 2007 (arXiv:physics/0701026, introduction), Raphaldini et al. 2020
  (arXiv abstract page), Giesecke et al. 2025 (arXiv:2410.14449v3, introduction), Pizzi et al. 2023
  (arXiv:2301.08076, introduction).
- **Discrepancies noted:** Lowes–Wilkinson second paper 1967 (Stefani 2018 text) vs 1968 (Crossref); DRESDYN sodium
  mass 6 t (Stefani 2018) vs 8 t (Pizzi 2023); Kazantsev 1967 (Russian original, Rincon) vs 1968 (JETP English);
  Stefani et al. 2007 arXiv title vs journal title; Permo-Carboniferous / Kiaman superchron 312–262 Myr (Stefani
  2007) vs 302–252 Ma (Constable); last reversal ≈ 780 kyr (Stefani 2007, Constable) vs ≈ 773 ka (Singer 2019,
  newer dating); Riga first attempt 1986 vs 1987 `[site: specs/sources/dynamo.md:615]`.
- **UNVERIFIED (do not put on screen without a new check):** Larmor 1919 title and page numbers (secondary only);
  wording of the Glatzmaier–Roberts 1995 abstract (search excerpt only); case definitions of the Christensen 2001
  benchmark (search excerpt only); content of Nozières 1978, Jonkers 2003, Sorriso-Valvo 2007, Valet 2005, Ogg
  2020, Zimmerman 2014 (titles only); Steenbeck 1967 α-effect experiment and Gans 1971 (secondary only); authors of
  Frick et al. 2002 (Magnetohydrodynamics 38, 143–162; Crossref record has no authors); DRESDYN operating status in
  2026; journal version of Raphaldini et al. 2020.
