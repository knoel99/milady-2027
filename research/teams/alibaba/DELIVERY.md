# DELIVERY.md — race-alibaba / MilaDy

Delivery at 2026-11-15, within the 00:31:53→02:01:53 UTC window. Everything claimed in the report is produced by
code in this repository and stored in this repository; the shared dataset is on the Hugging Face Hub.

## 1. Report

* `REPORT.md` — the research report (setup, validated generator, comparative study of physics-constrained
  generative strategies, analytic 2D benchmark, 1D reversal benchmark, findings, limits, related work).
  It contains the AI-contribution statement (§ "Who did what").
* `CHECKLIST.md` — NeurIPS-style paper checklist answers (reproducibility, significance, compute, licences, AI use).
* `COMPLIANCE.md` — traceability matrix S1…S13 against the subject, with status, evidence and justification.
* `DECISIONS.md` — strategy and every decision that changed it, timed (including the GPU-provisioning incident).
* `COSTS.md` — written by the framework at `deliver` from its ledgers (LLM + cloud).

## 2. Code (all of it produces the reported numbers)

| path | what |
|---|---|
| `code/milady/spectral.py` | pseudo-spectral operators: rfft/irfft wrappers, `div`, `curl`, `lap`, `grad`, exact Helmholtz `project`, Coulomb `vector_potential`, shell `energy_spectrum`, ABC flow (dim-generic 1D/2D/3D) |
| `code/milady/dynamo.py` | kinematic ABC dynamo integrator (RK4 + per-step projection, geometric-level snapshotting), growth-rate estimator, solenoidal random fields, 1D stochastic quenched mean-field α² dynamo |
| `code/milady/model.py` | conditional field network (residual conv, FiLM on flow time + control parameters), dim-generic |
| `code/milady/flow.py` | conditional flow matching with the four constraint routes (design / loss / sampling-projection / guidance), three priors (white, solenoidal, function-space coloured), sampler (Euler/Heun, step ablation), trainer |
| `code/milady/metrics.py` | relative divergence, energy spectra + slope, energy budget `P, D, γ_inst`, helicity + normalised helicity σ(k), polarity, KS, two-sample discriminative AUC |
| `code/exp_data.py` | validation suite (Table 1), independent γ(Rm) sweep, resolution study, dataset build |
| `code/exp_ds.py` | fast dataset build (used by `reproduce.sh`; the same generator as `exp_data.py`'s EXP1c section) |
| `code/exp_gen.py` | the three learning experiments: `--which 2` analytic 2D benchmark, `--which 3` main 3D comparative study, `--which 4` 1D reversal benchmark |
| `code/make_tables.py` | renders every table in `REPORT.md` from `results/*.json` |
| `push.sh` | the (unused after the pod failure) chunked uploader to the Runpod pod; kept for traceability |

## 3. Data and models

* **Dataset on the Hub:** `https://huggingface.co/datasets/knoel/milady-abc-dynamo-fields` (private, token user
  `knoel`) — 144 divergence-free 3D fields `X (N,3,16,16,16)` with parameters `C = [Rm, h]`, reference spectra,
  helicity spectra and measured growth rates. Card: `data/README.md`.
  Regenerate: `python3 code/exp_ds.py --n 16` → `data/dynamo_dataset.{pt,npz}`.
* **Also in the repository:** `data/dynamo_dataset.pt`, `data/dynamo_dataset.npz` (same bytes).
* **Models:** the study trains ~1e5-parameter conditional flow-matching networks per strategy for comparison;
  they are reproducible from the seeds in `code/exp_gen.py` and are not published separately (their value is in the
  comparison table, not as reusable weights). See `DECISIONS.md` 01:20 for the trade-off.
* **Results:** `results/*.json` (exp0 validation, exp1 growth + threshold, exp1b resolution, exp1c dataset
  descriptors, exp2 analytic benchmark, exp3 comparative study, exp4 reversals) and `results/TABLES.md`
  (the rendered tables) plus the run logs `results/*.log`.

## 4. Regenerate every reported result from a fresh checkout

```bash
bash reproduce.sh
# equivalent, step by step (only numpy + torch needed; CPU is enough):
python3 code/exp_data.py --n 16          # Table 1 validation (+ gamma sweep, resolution study)
python3 code/exp_ds.py --n 16            # data/dynamo_dataset.{pt,npz}, Tables 2 and 4
python3 code/exp_gen.py --which 3        # results/exp3_study.json  -> Table 5 (main study)
python3 code/exp_gen.py --which 2        # results/exp2_bench2d.json -> Table 6 (analytic benchmark)
python3 code/exp_gen.py --which 4        # results/exp4_reversals.json -> Table 7 (reversals)
python3 code/make_tables.py > results/TABLES.md
```
Wall clock: ~25 min on 4 CPU cores (the campaign ran under contention with another mission's jobs on the shared
host, so times vary); a GPU shortens it but is not required. Seeds are fixed, so `results/*.json` reproduce
bit-for-bit on the same torch build (float32 reductions can differ marginally across BLAS/thread counts).

## 5. Hardware / spend summary

LLM: harness only (`alibaba/qwen3.8-flash`), no paid sub-agents. Cloud: one Runpod RTX 4090 pod created and
deleted after its container crash-looped without executing any of our code; the campaign itself ran on the local
4 CPU cores. Exact figures are written to `COSTS.md` by the framework at delivery.
