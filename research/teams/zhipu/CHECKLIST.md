# NeurIPS Paper Checklist — race-zhipu

Answers for the study in `report.md`. Each answer states where the evidence lives.

## 1. Claims

**Question**: Do the main claims made in the abstract and introduction accurately reflect the paper's
contributions and scope?
**Answer**: **Yes.** The claims are: (i) a controlled comparison of four constraint-injection points
(data/formulation, model design, training loss, sampling procedure) for conditional generative models of
parameter-dependent divergence-free fields; (ii) measured trade-offs between physical consistency,
distributional fidelity and sampling cost on two benchmarks. Scope (synthetic 3D stand-in for MHD, moderate
Re range, small models, one seed) is stated in §4 and §6. All §5 numbers come from `results/metrics.json`
produced by `code/sample_eval.py` in the committed run.

## 2. Limitations

**Question**: Does the paper discuss limitations and potential negative societal impacts of its work?
**Answer**: **Yes.** §6 states: synthetic 3D benchmark instead of MHD DNS; moderate Re with no inertial-range
claims; small U-Nets; single seed per configuration; guidance/projection evaluated only at sampling;
no claim of superiority over any published method. No negative societal impact is identified (the work is a
methodology benchmark for physical-field generation); this is stated in §6.

## 3. Theory, proofs and assumptions

**Question**: Does the paper present formal theorems, and are assumptions stated and proofs complete?
**Answer**: **N/A (No theorems).** The only formal statements are identities: exact divergence-free
properties of the data construction, of the Fourier projection, and of the curl-of-potential mapping
(verified numerically to round-off, §3.4–3.5 and `results/meta3d.json`); Parseval conventions are documented
in `code/common.py` and `code/gen_data_3d.py`.

## 4. Experimental result reproducibility

**Question**: Does the paper fully disclose all information needed to reproduce the main experimental results?
**Answer**: **Yes.** `DELIVERY.md` gives a `reproduce.sh`-equivalent single command (`bash code/run_all.sh`),
fixed seeds (data seed 0, model seed 0) in the code defaults, all hyperparameters in `report.md` §4 and in
`code/train_fm.py` argparse defaults, and the exact GPU model in §4. The datasets are generated
deterministically by the committed code (`code/gen_data_2d.py`, `code/gen_data_3d.py`); no external data.

## 5. Code and data

**Question**: Is source code and data available, and are the license terms stated?
**Answer**: **Yes.** All code is in `code/` (MIT license, `LICENSE` + `CITATION.cff`); generated data and
result artifacts (metrics.json, sample archives, figures, checkpoints) are in `results/` and published on
Hugging Face (see `DELIVERY.md`). The only third-party dependencies (torch, numpy, matplotlib) are
standard open-source packages, pinned in `code/requirements.txt`.

## 6. Experimental setting/details

**Question**: Does the paper specify the full experimental setup?
**Answer**: **Yes.** §4: grid sizes, solver (pseudo-spectral, fp32, 2/3 dealiasing, RK2, dt = 1e-4, T = 10,
snapshot cadence, transient), parameter values (ν ∈ {0.02, 0.01, 0.008, 0.006, 0.004}; θ = (k_p, h) ranges),
train/test splits, model sizes (1.0 M params 2D, ~1.9 M params 3D), training steps/batch/lr/optimizer,
50-step Euler ODE sampler, 64 fields per parameter point, and hardware (1× RTX 4090).

## 7. Error bars and statistical significance

**Question**: Does the paper report error bars or confidence intervals?
**Answer**: **Partially.** Metrics are means over 64 generated fields per parameter point (2D) and 200
reference fields (3D test sets); the MMD² and spectrum-error variability across the 5 (2D) / 4 (3D) parameter
points is visible per-point in `results/metrics.json` and the figures. We do not run multiple training seeds;
this is stated in §4/§6 as a limitation (single-seed study). No significance tests are claimed.

## 8. Compute resources

**Question**: For each experiment, can you state the compute used?
**Answer**: **Yes.** §4 and `DELIVERY.md`: one rented NVIDIA RTX 4090 (24 GB) on Runpod, ≈ 25 GPU-minutes for
the full pipeline (2 datasets + 4 trainings + sampling/evaluation). Cloud cost ≈ 0.7 USD; LLM cost for the
authoring agents ≈ 0.8 USD (`COSTS.md`).

## 9. Code of ethics / research integrity

**Question**: Does the research conform to the NeurIPS Code of Ethics?
**Answer**: **Yes.** No human subjects, no personal data, no unsafe applications. All compute was rented under
the mission's own accounts; no external resources were touched.

## 10. Broader impacts

**Question**: Does the paper discuss broader impacts?
**Answer**: **Yes (briefly).** §6: cheap, constraint-respecting generative surrogates can reduce the cost of
ensemble generation and parameter exploration for dynamo modelling; risk of misuse is not identified beyond
the general caveat that surrogate fields must not be mistaken for DNS data.

## 11. Licenses of assets

**Question**: Are the licenses of all assets referenced?
**Answer**: **Yes.** Code: MIT (this repo). Dependencies: BSD-3 (PyTorch, NumPy), Matplotlib (PSF-based
license). Subject references are cited publications (not code assets). The subject document
(`subject/stage_milady_2027.pdf`) is quoted only for compliance tracing.

## 12. New assets

**Question**: Are new assets introduced with documentation and licenses?
**Answer**: **Yes.** The repository introduces the benchmark code, generated datasets (with generation
metadata in `results/meta2d.json`, `results/meta3d.json`) and model checkpoints, each documented in
`DELIVERY.md` and on the Hugging Face cards (MIT license declared).

## 13. Experiment concurrency / crowdwork and human subjects

**Question**: Were crowdsourcing or human-subject experiments used?
**Answer**: **No.**

## 14. Use of AI in the research process

**Question**: Was AI used to produce this work, and is that use disclosed?
**Answer: **Yes.** The study was produced end-to-end by AI agents; the exact model contributions are listed in
`report.md` §Author contributions (harness agent on `glm-5.3-flash`/zhipu; drafting sub-agents on
`deepseek-v4-pro` and `glm-5.3-flash`), with per-agent costs in `COSTS.md`. All reported numbers were produced
by the committed machine-runnable pipeline, not generated by the LLMs.
