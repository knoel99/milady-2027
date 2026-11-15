# DELIVERY.md — race-moonshot

## Deliverables

- **Report**: `REPORT.md` (with figures in `results/figures/` and metrics in `results/metrics.json`).
- **Code**: `code/` (`gen_data.py` spectral Kolmogorov-flow data generator; `model.py` conditional
  flow-matching U-Net + spectral constraint operators; `train.py` training of the three variants;
  `evaluate.py` metrics and figures), `tools/pod_push.py` (artefact transfer helper),
  `reproduce.sh` (end-to-end regeneration).
- **Dataset** (Hugging Face Hub): see `hf_dataset/README.md`; URL: https://huggingface.co/datasets/knoel/milady-20261115-race-moonshot-kolmogorov-ns-2d-parametric
- **Model checkpoints** (Hugging Face Hub): see `hf_model/README.md`; URL: https://huggingface.co/knoel/milady-20261115-race-moonshot-flowmatch-kolmogorov-physics-constrained
  (`flowmatch_v0_baseline.pt`, `flowmatch_v1_softdiv.pt`, `flowmatch_v2_psi.pt`;
  V3 = V0 + projection, no checkpoint).
- `COMPLIANCE.md` (traceability to the subject), `DECISIONS.md` (strategy log),
  `CHECKLIST.md` (NeurIPS-style checklist), `CITATION.cff`, `COSTS.md` (framework-written).

## Reproduce every reported result from a fresh checkout

```bash
bash reproduce.sh
```

This regenerates the dataset (`data/kolmogorov_ns.npz`, deterministic, fixed seeds),
retrains the three checkpoints (`checkpoints/`), and recomputes `results/metrics.json` and
`results/figures/*.png`. Requirements: python3 with numpy; torch (CUDA GPU recommended:
~3.5 min/variant on an RTX 4090; CPU works but is much slower); matplotlib for figures.

## Measured vs published

All numbers in REPORT.md section 4 are **measured** by runs whose code and outputs are in this
repository (`results/metrics.json`, `checkpoints/train_log.jsonl`). No external experimental
results are reported; references in section 8 are methodological context only.
