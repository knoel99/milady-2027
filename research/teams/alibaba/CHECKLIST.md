# CHECKLIST.md — NeurIPS paper-checklist answers for this study

**1. Claim alignment (abstract/intro).** Claims in `REPORT.md` are restricted to what was measured here.
Published values quoted for context (the ABC dynamo threshold Rm_c ≈ 20, the α²-dynamo threshold α0 > η,
Kolmogorov-like spectral slopes) are labelled as external references, not as our results.

**2. Limitations.** Stated in `REPORT.md` §8: kinematic (no Lorentz feedback) rather than saturated turbulent
MHD; a single box size (16³ for the learning study, resolution study at 12/16/24 in §3.3); snapshots taken at
fixed geometric energy levels and renormalised to unit rms, so *amplitude* is not generated (it is given by the
measured growth law) while shape statistics are; single training seed for the 9-strategy study; 6 IC seeds per
parameter group, so the reference distributions are estimated from ~24 fields per group; no closure test with an
external reduced-order or data-assimilation model.

**3. Theory assumptions.** The generator solves the kinematic induction equation with a prescribed steady ABC
flow (Beltrami, curl u = u, verified to 5.6e-7); fields are periodic, zero-mean and spectrally projected to be
solenoidal (verified to ~6e-7). The energy-balance identity P − D = dE/dt used by our metric is exact for the
discrete system (verified to 1.2e-7). The 2D benchmark's ground truth is analytic: u = ∇^⊥(I − λ²Δ)^{-1}ω with ω
white Gaussian ⇒ |û(k)|² ∝ k²/(1 + λ²k²)², which is stated and used as the reference spectrum.

**4. Experimental protocol / reproducibility.** Every number in the report comes from
`results/*.json` written by `code/exp_data.py` and `code/exp_gen.py`; `reproduce.sh` reruns the whole chain on a
fresh checkout (numpy + torch, CPU or GPU, no other dependency). Seeds are fixed
(`torch.Generator(...).manual_seed`) for data generation, training and sampling. Deterministic results do not
require a GPU; a GPU only shortens wall-clock time.

**5. Statistical significance.** Reported per-group statistics (mean and spread of spectra, helicity, γ_inst,
polarity fraction) over ensembles of 16-24 generated fields and 24 reference fields, plus a *two-sample
discriminative score* (AUC of a logistic classifier on physics features, real vs generated, chance = 0.5). No
p-values or multi-seed confidence intervals were computed for the 9-strategy comparison (single seed each): the
ranking is reported as descriptive, and §8 lists multi-seed error bars as required follow-up. This is an explicit
weakness, not a claim of significance.

**6. Experiments and compute.** 3 experiments (generator validation + dataset, 2D analytic benchmark, 3D
comparative study, 1D reversal benchmark). Model size ~90k-160k parameters; training 800-1400 flow-matching
steps per strategy. Wall clock: ~15 min of 4 CPU cores for the reported campaign (see `results/*.json` `wall_s`
fields and `COSTS.md`). A Runpod RTX 4090 pod was rented first and stayed in an image-start crash loop for
~20 min without ever executing our code; it was deleted (Runpod spend = pod lifetime only, see `COSTS.md`).

**7. Assets and licences.** Code written for this mission (numpy + torch only). Public data/assets used: none
besides the `subject/stage_milady_2027.pdf` advertisement. The published dataset is derived entirely from our own
simulations; its card states the licence (`CITATION.cff`, `data/README.md`). Software dependencies: PyTorch
(BSD-3-Clause), NumPy (BSD-3-Clause). Cited works are used as intellectual references only; no third-party model
weights or datasets were downloaded or redistributed.

**8. Use of AI assistance.** The entire mission (design, code, experiments, report) was executed by an autonomous
AI research team (Qwen Code harness on `qwen3.8-flash`), with model calls listed in `COSTS.md`. No human wrote
code in this repository during the mission. AI was used for: literature positioning, code generation, experiment
orchestration and writing; all quantitative statements come from the runs in `results/`.

**9. Positive/negative societal impact.** Energy-storage/geodynamo/astrophysics modelling; no direct harmful
pathway identified. The dataset is synthetic simulation output; no personal or sensitive data. Reduced-cost
generative surrogates could replace compute-heavy DNS, which is the intended benefit.
