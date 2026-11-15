# Subject traceability

The source is the two-page `subject/stage_milady_2027.pdf`. The mission requests research, not an internship application. Rows follow the subject's order. “Partial” identifies a real limitation rather than an unverified success.

| ID | Subject instruction or outcome (location) | Status | Evidence and justification |
|---|---|---|---|
| S1 | Develop generative models respecting MHD physics, conditioned on system parameters (p.1, Context) | partial | `code/mhd.py`, `REPORT.md`; unforced periodic low-resolution MHD only, not realistic dynamo physics. |
| S2 | Start with simple PDE benchmarks, with potential turbulent dynamo applications (p.1, Context) | partial | Analytic heat benchmark and 3D MHD in `code/heat.py`, `code/mhd.py`; no turbulent dynamo dataset was available or claimed. |
| S3 | Design and evaluate parameter-dependent physical-field generators (p.1, Objective) | compliant | Conditional flow models and held-out interpolation tests in `REPORT.md` and `artifacts/*/results_corrected.json`. |
| S4 | Respect energy balance and divergence-free conditions (p.1, Objective) | partial | Soft loss plus Fourier projection and discrete budget correction; tested in `results/operator_checks.txt`; full MHD PDE and long-time energy evolution are not guaranteed. |
| S5 | Encode variations in control parameters (p.1, Objective) | partial | Inputs ν and η and matched interventions in corrected JSON; generator sensitivity is weaker than the simulator's in this experiment. |
| S6 | Enable robust 3D field generation usable for ROM or data assimilation (p.1, Objective) | partial | `code/sample_mhd.py` exports paired 3D fields; robustness and downstream ROM/assimilation performance were not established. |
| S7 | Implement and test conditional diffusion or flow-matching generators (p.1, Scientific work) | compliant | Two flow-matching architectures, multiple seeds, samples and saved checkpoints under `code/`, `artifacts/`. |
| S8 | Condition on controls and incorporate governing-PDE and boundary constraints through design, loss or sampling (p.1, Scientific work) | partial | Parameters, soft losses, projection, exact heat step and MHD budget correction are implemented; boundary conditions are periodic only, and corrections do not impose the full MHD PDE. |
| S9 | First validate on simple PDE benchmarks (p.1, Scientific work) | partial | Heat exact solutions, held-out interpolation and operator tests are in `REPORT.md`, `artifacts/heat/`; the heat and MHD runs were overlapped for time, so the complete heat study was not finished before MHD training began. |
| S10 | Evaluate generated MHD fields using energy spectra, helicity, divergence and topology preservation (p.1, Scientific work) | partial | Magnetic and kinetic spectra, magnetic/current helicity, divergence, energy and periodic excursion-set component count are measured; component count and helicity are proxies and do not establish field-line topology preservation. |
| S11 | Comparative study of physics-constrained strategies for parameter-dependent MHD (p.2, Expected outcomes) | partial | Baseline, soft, projection and budget strategies compared in `REPORT.md`; only one toy periodic regime, not broad dynamo regimes. |
| S12 | Concise technical report and reproducible code integrated into MilaDy toolbox (p.2, Expected outcomes) | partial | `REPORT.md`, `reproduce.sh` and modular `code/` delivered; no MilaDy toolbox repository or maintainer access was supplied, so actual integration and review could not be performed. |
| S13 | Possible dissemination to journals or conferences (p.2, Expected outcomes) | not applicable | An opportunity, not a required submission; no human-reviewed publication is claimed. |
| S14 | Possible fully funded PhD offer (p.2, Expected outcomes) | not applicable | Employment opportunity, not a research deliverable. |
| S15 | Candidate educational profile (p.2, Profile) | not applicable | This is a research mission, not a human internship application. |
| S16 | Candidate Python and ML framework skills (p.2, Profile) | not applicable | Candidate eligibility; the delivered implementation uses Python and PyTorch. |
| S17 | Candidate interest and prior knowledge (p.2, Profile) | not applicable | Candidate eligibility, not a research instruction. |
| S18 | Supervision and environment (p.2) | not applicable | Descriptive internship context; no supervisory interaction occurred. |
| S19 | Duration, location and compensation (p.2, Practical information) | not applicable | Internship terms, not work in this research mission. |
| S20 | Send single PDF application and reference contacts by email (p.2, Application) | not applicable | No application was requested; no contact details or application were fabricated or sent. |
| S21 | Read two recommended references before applying (p.2, References) | not applicable | No application; relevant methodological sources used in this study are cited in `REPORT.md`. |
| S22 | Other references (p.2) | not applicable | Background suggestions rather than mandatory reproductions; `REPORT.md` cites the relevant physics-informed diffusion paper and flow matching. |
