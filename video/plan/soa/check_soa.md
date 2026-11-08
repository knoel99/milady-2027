# Adversarial citation and attribution check — 2026-11-08

Files checked and corrected (kept consistent):
- `/home/user/milady-2027/video/ETAT-DE-L-ART.md` (FR)
- `/home/user/milady-2027/video/plan/state_of_the_art.md` (EN)

## Method

- Extracted every DOI (186 + 7 with parentheses) and arXiv id (61) from both files; resolved all of them today in
  Crossref (`api.crossref.org/works/<doi>`) and the arXiv API. Raw results: `chk/dois.json`, `chk/d2.json`,
  `chk/arx.json`. All DOIs resolve; no invented DOI or arXiv id found. Authors, years, titles, venues compared
  automatically (`tools/bibcmp.py`) and by hand.
- Abstracts re-read (Crossref, OpenAlex, arXiv, HAL) for every claim about a supervisor's paper and for the
  landmark claims; full text read for da Silva et al. 2025 (arXiv HTML), PIDM (Jensen gap), Tauberschmidt et al.
  (tilting), Mohan et al. (arXiv v2), Constable 2001 preprint, Tobias 2019/2021, Rincon 2019, Stefani et al. 2018.
- Venues checked on OpenReview (PBFM and Tauberschmidt: "ICLR 2026 Poster"; MPP, Poseidon NeurIPS 2024; DiffDA
  ICML 2024; Universal guidance ICLR 2024; Négiar ICLR 2023; Wang–Walters–Yu ICLR 2021), PMLR (Köhler et al.
  2020, pp. 5361-5370), JMLR index (Kovachki 24(89); Albergo 26(209); Lim 26(158)).
- Other web sources: HAL API (MilaDy deposit dates; Fournier 2010 abstract; wildfire 2022 abstract), the 2027
  internship offer PDF (text extracted with pypdf), C. Nore's LadHyX seminar abstract PDF ("since 2002" confirmed).

## Confirmed problems and fixes

| # | Problem (evidence) | Fix (both files unless noted) |
|---|---|---|
| 1 | "regress to the mean flow" attributed to the GenCFD *Nat. Commun.* abstract; it is only in the arXiv:2409.18359v2 abstract (different first author, Molinaro, and title "fast and accurate"); the published abstract says the MSE loss "fails to accurately characterize statistical features of chaotic dynamics" | quote reattributed to the preprint; published wording added; divergence listed in ETAT §5 |
| 2 | "Divergence dure en 3D : seulement PCDM, périodique" / "In 3D, the only exact divergence constraint we found lives in a periodic box": contradicted by the documents' own source da Silva et al. 2025 (full text: spherical harmonics satisfying Laplace's equation, ∇·B = 0, 3D sphere) | added da Silva as a 3D spherical case limited to a current-free potential field; SOA2.4 beats, pins, gate verdict, gap 2 updated; mark changed to `[TI]` |
| 3 | "Aucun n'est auteur d'une expérience de laboratoire" / "no laboratory experiment by any of the four": false for C. Nore (Nore, Moisy, Quartier 2005, *Phys. Fluids* 17, 064103, experimental von Kármán flow, PIV; co-author of Stefani et al. 2015 reporting water pre-experiments) | narrowed to "no laboratory *dynamo* experiment"; §2.6 table D2 row corrected; 2005 title added |
| 4 | Yang & Schmid 2025: first author is Rui Yang (Crossref), cited "Yang Y." | "Yang R., Schmid P. J." with title |
| 5 | "DQVU est le premier modèle de VKS dérivé de simulations…": no source says "first"; abstract says it "improves upon previous three-variable versions" | rewritten without "premier"; wording trap added in SOA §6 |
| 6 | "MilaDy's first paper" (SOA1.5, §4 diamond): unsourced ordinal | "first paper declaring MilaDy funding to appear" with dates (Crossref online 18 June 2026 vs Botez 14 Aug 2026; HAL deposits 24 June, 7 Oct, 13 Oct 2026) |
| 7 | Diamond rule "only Bousquet and Botez qualify": HAL lists a third item declaring ANR-25-CE51-0077 (Barré & Horii 2026) | rule restated: two dynamo papers; Barré & Horii off-topic, no pin (EN) |
| 8 | "Lowes et Wilkinson : premier modèle de dynamo de laboratoire" / "a first laboratory model": Stefani et al. 2018 §2.1 does not say "first" | "un modèle de dynamo « quasi homogène » de laboratoire" / "a laboratory model" |
| 9 | "Premier benchmark communautaire" (Christensen 2001): no source read says "first" | "premier" removed; listed as unverified |
| 10 | "La première dynamo homogène sans turbines (précession, DRESDYN) reste à obtenir": Karlsruhe was already a "homogeneous two-scale dynamo" (Stieglitz & Müller 2001) without impellers; Stefani et al. 2012 abstract: "homogeneous hydromagnetic dynamo driven solely by precession" | rewritten with the 2012 wording and the Karlsruhe precision (FR); wording trap (EN) |
| 11 | "La seule turbulente, VKS": Riga and Karlsruhe flows are turbulent too; Tobias §9 contrasts "constrained designs" with VKS's "less constrained flows" | "La seule à écoulement peu contraint", with Tobias quote (FR) |
| 12 | Glatzmaier & Roberts 1995: the "modern era" sentence of Tobias §8.3 cites their *PEPI* 91, 63-75 paper, not *Nature* 377 | PEPI paper added (doi:10.1016/0031-9201(95)03049-3, Crossref) and note in timeline, D3, SOA §7; "anélastique" flagged as Tobias's word |
| 13 | "≈ 8 fois … Ponty et al. 2007": site Dy:605 says the eightfold rise is *recalled* by the authors from earlier work | "rappelé par Ponty et al. 2007 d'après des travaux antérieurs" (FR); wording trap (EN) |
| 14 | Ponty et al. 2007 NJP: "seuil à deux branches selon le niveau de turbulence" misdescribes the abstract (two branches of the kinematic dynamo of the mean flow; dynamical threshold moves from low to high branch as Re grows) | rewritten from the abstract (FR) |
| 15 | D. Lucor "Chaos polynomial généralisé (fondateur)": overclaims; his 2002-2004 papers are co-authored applications with Xiu and Karniadakis | "premiers travaux d'application, co-signés avec D. Xiu et G. E. Karniadakis" (FR) |
| 16 | Scheinker 2026 described as "diffusion latente conditionnelle pour la MHD compressible": the preprint is a bidirectional latent diffusion model predicting its own rollout errors; compressible MHD is one of three test cases | description and §3.4 row corrected; title added (FR) |
| 17 | SOA §4 Lucor 2022 pin marked `[ABS]`: the relaxed-incompressibility sentence is in the preprint abstract (arXiv:2103.03565, different title); JCP abstract unavailable | source mark made explicit (EN; FR already said "résumé de la prépublication") |
| 18 | SOA §4 Nore 2018 "Rm ≈ 70" marked `[ABS]`: the abstract only says Rm_c "tends to a constant"; 70 is from the full text via site Dy | source note added (EN) |
| 19 | FunDiff called "référence principale de l'offre" (site paraphrase) | offer PDF re-read: first of two recommended readings, with Fukami & Taira 2023 (FR) |
| 20 | §2.6 table credits S. Cheng with "Koopman" work but §2.5 and §6.5 cited none | added Cheng X. et al. 2026, "Information shapes Koopman representation", ICLR 2026 (arXiv comment), arXiv:2510.13025, S. Cheng co-author (FR) |
| 21 | Kaiser & Tilgner 2014 cited without title or DOI | title and doi:10.1137/130928376 added (Crossref) (FR) |
| 22 | da Silva "∇·B = 0 par la représentation" marked `[RÉS]` (not in abstract) | full text read; mark `[TI : arXiv:2510.01441v1]` (FR) |
| 23 | Galletti "l'analogue le plus proche" given as a source statement | marked `[SYNTHÈSE]` (FR) |

## Checked and found correct (selection)

All 193 DOIs and 61 arXiv ids resolve to the cited authors, year, title and venue (allowing for documented
arXiv/journal title differences). PBFM quote "Our work is the first to recognize the trade-off…" verbatim (arXiv
v4) and ICLR 2026 (OpenReview). Tauberschmidt et al. ICLR 2026 and "tilts the generative distribution" (full
text). Supervisor claims confirmed against abstracts: Nore 1997 (symmetries, boundary conditions select mode),
Nore 2016 ("For the first time"), Laguerre 2008 (Rm_c ≈ 32, ferromagnetic BCs), Giesecke 2012 (μr^(-1/2)),
Nore 2012 ("exhibits aperiodic reversals"), Creff 2024, Bousquet 2024 (Rπ, Re > 10⁴), Botez–Bousquet–Nore 2025,
Bousquet–Nore–Lucor 2025 (Gaussian prior quote; equivariance), Bousquet 2026 (DQVU, two solvers), Botez 2026
(all abstract statements), Jackson 2014 (Nore is co-author), Stefani 2015 (Nore co-author); Ponty 2001, 2005,
2007 PRL (subcritical, hysteretic), Alexakis–Ponty 2008 (ABC), Baerenzung 2008 (EDQNM), Homann 2014, Mannix 2022,
Ponty–Politano–Pouquet 2025 (3.14 × 10⁵), Kreuzahler 2014/2017, Mininni 2005 quote; Lucor 2007 (Smagorinsky
constant), Cai 2024 (Galilean and rotational invariance, arXiv abstract), Lucor 2022 preprint quote; Cheng: CUTE
and PUB (arXiv abstract), GLA (error bound), wildfire 2022 ("around 1000 times faster", HAL abstract), VQ-VAE
2023, TorchDA (KF, EnKF, 3DVar, 4DVar), Zhuang 2025 (noisy vs noiseless), Yu 2026, Lin 2026 (VAE-Var), Xue 2026
(moment matching, global equivariance), PFNN quote, Bocquet–Finn–Cheng (IEnKF-G, weak-constraint 4D-Var).
Landmarks: Herzenberg, Backus ("first mathematical working examples", Rincon), Meneguzzi 1981 ("first published
numerical evidence", Rincon), Soward 1987, Schekochihin 2005, Iskakov 2007, Warnecke 2023, Cox 1968 (p ≈ 0.05,
Permian two orders smaller), Singer 2019 (773 / 795 ka), Gwirtz 2022 (five reversals; conclusion quote), Valet &
Fournier 2016 quote, Carbone 2006, Hoyng 2001, Kutzner 2002, Schaeffer 2017, Matsui 2016, Frick 2010, Bourgoin
2002, Cooper 2014, Fournier 2010 (3D dynamo and QG assimilation), Constable quotes, Tobias quotes, Stefani et al.
2007 arXiv/journal titles, Stefani et al. 2018 = GAFD 2019 (identical abstracts), Kacmaz, Rosofsky (Re ≤ 250),
FNO quote, GenCast 97.2 % of 1320, Kim 2021 (CycleGAN), Wu 2020 (covariance), Finzi quote, PIDM Jensen gap,
Köhler 2020, Mun 2026 (exponential tilting under moment constraints), Li X. 2026, Genuist 2025/2026, Guseva 2026,
Martin 2025, Illarionov 2026, Duarte 2025 (Orszag–Tang), offer 2027 phrases ("energy balance and divergence-free
conditions", "diffusion or flow matching"), SFEMaNS "since 2002" (seminar PDF).

## Non vérifié (also listed at the end of both files)

- Glatzmaier & Roberts 1995: "anelastic" (Tobias's word) and the *Nature* paper's content (neither read).
- Christensen et al. 2001: "first" status and case definitions (no abstract available).
- Lucor et al. 2022 JCP abstract (unavailable; claim rests on the preprint abstract).
- Nony et al. 2023 "POD et processus gaussiens" (title only; no abstract available).
- Kohl et al. 2026 (ACDM): "conditioned on Re and Mach" not stated in the abstract.
- Numbers from the site not re-read today: Kacmaz (128², Pm = 1), PCDM (64³, machine precision), Weak Generative
  Sampler (dimension 100), Nore et al. 2018 (Rm_c ≈ 70), Genuist et al. 2026 (six variants).
- "No physical constraint" for Galletti, TurbDiff, CoNFiLD, GenCast: inferred from silent abstracts.
- Botez et al. 2026 full text (PDF blocked); DRESDYN status in 2026.
- Pre-existing items of ETAT §5 / SOA §6 (Larmor 1919 pages, Nozières, Jonkers, Valet 2005, Ogg, Zimmerman
  content, Steenbeck 1967, Gans 1971, Jarolim loss terms, PBFM Darcy numbers, Maryland reservoir computing, the
  Botez–Bousquet–Nore JCP "in press" paper, postdoc's name) remain unverified; not re-checked.

Nothing outside `/home/user/milady-2027/video` and this scratchpad folder was modified; nothing committed.
