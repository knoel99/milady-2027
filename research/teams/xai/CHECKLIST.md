# NeurIPS paper checklist

Adapted to this computational study. Answers refer to `REPORT.md` and the code under `milady/`.

1. **Claims.** Yes. The abstract of the report states contributions and the limits (kinematic, small grids, no reversals).
2. **Limitations.** Yes. The Limits section states the missing physics (no Lorentz force, no turbulence, no reversals), the single-seed MHD 3D run, and the cloud refusal.
3. **Theory.** Not applicable. No theorem is claimed. The minimax statement cited from FunDiff is theirs, not ours.
4. **Reproducibility of experiments.** Yes. `reproduce.sh` reruns the studies. `DELIVERY.md` lists the exact commands that produced `results/`. Seeds, splits and step counts are in each `metrics.json`.
5. **Statistical significance.** Partial. Burgers is reported over 3 training seeds with a sample standard deviation (`results/seeds_summary.json`). MHD 2D extra seeds use a shorter schedule and are not pooled with the delivered run. MHD 3D is one seed. Error bars are not confidence intervals of a test-set bootstrap. With 4 test fields, small differences are not treated as findings.
6. **Compute.** One shared CPU (4 vCPU, 16 GB, no CUDA). Training times are in each `metrics.json` under `train_seconds` (a few seconds per model). No GPU was obtained: Scaleway quota exceeded on L4, P100, BASIC2-A16C and DEV1-L; Runpod community offers had empty data-centre lists. See `DECISIONS.md`.
7. **Code and data.** Yes, in this repository. Synthetic data generators are `milady/physics.py` and `milady/mhd3d.py`. Published weights and the synthetic sets are on the Hugging Face Hub; URLs in `DELIVERY.md`.
8. **Assets and licences.** The solvers and models are original code, MIT (`LICENSE`). Cited papers are used as references only; no figure, table or paragraph is copied. Checkpoints are our weights. The internship PDF in `subject/` is the mission input and is not redistributed as our work.
9. **New assets.** Yes. Model and dataset cards are in `hub/model/README.md` and `hub/dataset/README.md` (SPDX `license: mit`, `library_name: pytorch` on the model, `task_categories` on the dataset).
10. **Crowdsourcing / human subjects.** Not applicable.
11. **Use of AI.** The code, the runs and the report were produced by the race-xai harness on `grok-4.7` (xAI). No sub-agent wrote a numerical result. This is stated in the report.
12. **Ethics / broader impact.** The study generates synthetic kinematic fields. It has no path to a deployed system. Misuse as a surrogate for geodynamo prediction would be a misuse of a negative-to-modest result; the report says the samples are not a DNS surrogate.
