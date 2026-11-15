# CHECKLIST.md — NeurIPS-style reproducibility checklist answers

## Reproducibility
- **Code**: full pipeline in `code/` (data generation, model, training, evaluation); `reproduce.sh`
  regenerates dataset, checkpoints, metrics and figures from a fresh checkout.
- **Data**: the dataset is synthetic, produced by `code/gen_data.py` (fixed seeds `SEED0=1234`);
  the generated dataset is also published on the Hugging Face Hub (see DELIVERY.md).
- **Splits**: train/test split is temporal (later snapshots of the same runs are held out);
  exact indices are deterministic in `gen_data.py:combine`.
- **Hyperparameters**: all constants at the top of `code/gen_data.py`, `code/train.py`,
  `code/evaluate.py` (grid 64×64, forcing k_f=4, F=1, α=0.1, dt=5e-3; training: 4000 steps,
  batch 128, AdamW lr 2e-4, EMA 0.999, λ_div=0.05; sampling: 40 Euler steps, 256 samples/Re).

## Statistical significance
- Metrics are computed on 256 generated fields per Reynolds number per variant and 64 held-out
  reference fields per Re; per-Re values are reported in `results/metrics.json`, means in
  REPORT.md. Error bars across samples (energy distributions) are given as mean/std and
  Wasserstein distances. Only one training seed per variant was run (1.5 h mission budget);
  this limitation is stated in REPORT.md, and per-sample spread is reported instead of
  seed-level error bars.

## Compute
- One NVIDIA RTX 2000 Ada (16 GB) Runpod pod, ~0.5 GPU-hour total (data generation is CPU,
  ~4 core-minutes per regime; training 3×4000 steps ≈ minutes each on GPU; evaluation on GPU).
  Exact spend is in `COSTS.md` (written by the framework at delivery).

## Licences of assets used
- All code and data were produced within this mission (MIT, see CITATION.cff).
- Software used: PyTorch (BSD-3-Clause), NumPy (BSD-3-Clause), Matplotlib (PSF-based).
- No external datasets or pretrained models were used.

## Use of AI
- The whole study (design, code, analysis, report) was carried out by an AI agent:
  Kimi Code CLI on the model kimi-k3 (Moonshot AI), which also wrote this file.
  Details in REPORT.md, section "AI usage".
