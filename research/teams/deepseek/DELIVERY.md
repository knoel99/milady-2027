# Delivery

Mission: `race-deepseek` — research pilot for the MilaDy internship subject
(`subject/stage_milady_2027.pdf`). Delivered 2026-11-15.

## 1. Where everything is

| deliverable | path | notes |
|---|---|---|
| Research report | `REPORT.md` | main deliverable, includes AI-contribution statement and limitations |
| NeurIPS checklist | `CHECKLIST.md` | reproducibility, significance, compute, licences, AI use |
| Compliance matrix | `COMPLIANCE.md` | one row per subject instruction (S1–S16) |
| Strategy / decision log | `DECISIONS.md` | chronological, with reasons and times |
| Citation metadata | `CITATION.cff` | repository citation |
| Code (package) | `code/*.py` | solver, data generation, model, training, evaluation, figures, checks |
| 2D MHD solver | `code/mhd_solver.py` | pseudo-spectral, split-step diffusion, 2/3 dealiasing |
| Generative model | `code/model.py` | conditional flow matching + spectral physics operators |
| Training | `code/train.py` | PCA latent, parameter conditioning, physics loss |
| Evaluation | `code/evaluate.py` | all reported metrics |
| Tables / sanity checks | `code/check_results.py` | generates `results/metrics_table.md` and significance tests |
| Figures | `code/make_figures.py` | `figures/fig1_fields.png`, `fig2_physics.png`, `fig3_burgers.png` |
| Reproduction entry point | `reproduce.sh` | one command, ~20–25 min on 4 CPU cores |
| Datasets | `data/mhd_{train,val,test,ood}.npz`, `data/burgers_{train,val,test}.npz`, `data/*_meta.json` | coefficients + diagnostics + spectra |
| Trained weights | `checkpoints_pca/*.pt` | 10 checkpoints (struct ×3 seeds, phys ×2, raw ×1, Burgers struct ×2, Burgers phys ×2) |
| Metrics (machine-readable) | `results/metrics.json`, `results/arrays.npz` | every number in the report |
| Significance / sanity | `results/sanity_checks.json` | Wilcoxon tests and guards |
| Metric tables | `results/metrics_table.md` | markdown tables |
| Figures | `figures/*.png` | 200 dpi |
| Costs | `COSTS.md` | written by the framework at delivery |

## 2. Hugging Face Hub

Publication was attempted twice through `hf_publish` (dataset `milady-pcfm-mhd-burgers-benchmark`,
model `milady-pcfm-mhd-models`) and failed in the tool with `InvalidURL: Invalid port: ':1]'`
(a proxy/URL parsing error in the Hub client, reproducible for both repositories, before any
upload). The complete cards and files are staged in `hf/dataset/` (CC-BY-4.0) and `hf/model/`
(MIT), so publication can be completed with one `hf_publish` call per folder when the Hub client is
reachable. No data is lost.

## 3. Reproduce from a fresh checkout

```bash
python3 -m pip install -r requirements.txt
bash reproduce.sh
```

`reproduce.sh` runs, in order:

```bash
python3 code/make_data.py --out data --only both                  # ~6 min, CPU
bash code/run_training.sh                                          # ~7 min, 3 workers
python3 code/evaluate.py --datadir data --ckptdir checkpoints_pca --out results --ng 24
python3 code/make_figures.py --results results --data data --ckptdir checkpoints_pca
python3 code/check_results.py --results results/metrics.json
```

All random seeds are explicit in `code/make_data.py`, `code/train.py` and `code/evaluate.py`
(training seed 0/1/2; data seeds 100000+, 200000+, 300000+, 400000+). CPU only; no cloud resource
and no external data download is needed.

## 4. What is measured (and where)

- Divergence, energy spectra, energies, `<A^2>`, Wasserstein topology proxies, energy-balance
  residual, PDE residual, diversity, parameter generalisation: `results/metrics.json`,
  `results/metrics_table.md`, `REPORT.md` §5.
- Significance tests (Wilcoxon over parameter pairs): `results/sanity_checks.json`.
- The reference floors (energy-balance and PDE residual of the held-out data, PCA truncation floor)
  are in the same files, so model numbers are always read against a floor.

## 5. Compute and budget

- CPU only: 4 vCPU, 15 GB RAM. No Scaleway or Runpod resource was created.
- Approximate wall time: data 6 min, training 7 min, evaluation 5 min, figures < 1 min.
- LLM spend is reported by the framework in `COSTS.md`; it is far below the 5 USD cap.

## 6. Known gaps (also in `REPORT.md` §6 and `COMPLIANCE.md`)

- 2D (not 3D) fields, 64² grid, moderate Re,Rm ≤ 50, 256 training fields per benchmark;
  the study is a reproducible pilot, not a finished MHD surrogate.
- Helicity is replaced by the 2D magnetic-potential invariant `<A^2>` because in-plane 2D magnetic
  helicity vanishes identically.
- The code is a standalone package, not merged into the private MilaDy toolbox.
