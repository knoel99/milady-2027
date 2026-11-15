# Delivery

- Report: [REPORT.md](REPORT.md). Traceability: [COMPLIANCE.md](COMPLIANCE.md); decisions: [DECISIONS.md](DECISIONS.md); research checklist: [CHECKLIST.md](CHECKLIST.md).
- Code: `code/heat.py`, `code/mhd.py`, `code/evaluate_heat.py`, `code/evaluate_mhd.py`, and `code/summarize.py`; operator and convergence tests: `code/test_physics.py`, `code/convergence.py`.
- Exact generated data, checkpoints and measured outputs: `artifacts/heat/`, `artifacts/mhd/`. `results/summary.md` summarizes corrected results; `results/*.log` capture training/evaluation, `results/environment.txt` records hardware.
- Dataset: [private Hugging Face dataset](https://huggingface.co/datasets/knoel/milady-20261115-race-openai-race-openai-milady-20261115-0031-7c9-data), commit `f8fbd96dc8304296e42a198cf4b8b36505a8d86a`, card `hub/dataset/README.md`, CC0-1.0.
- Models: [private Hugging Face models](https://huggingface.co/knoel/milady-20261115-race-openai-race-openai-milady-20261115-0031-7c9-models), commit `4a13d8dd1e88351f71459af2ee6c49003fe996d4`, card `hub/model/README.md`, MIT. Links require access to the mission's account.
- License and citation: `LICENSE` and `CITATION.cff`. Framework-recorded spending appears in `COSTS.md` after delivery.

## Reproduce

From a fresh checkout, on Python 3.11 and an NVIDIA CUDA GPU comparable to the 24 GB RTX 4090:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./reproduce.sh --evaluate     # use supplied training data and checkpoints; rerun checks and evaluation
./reproduce.sh --all          # regenerate data and retrain all 12 models, then evaluate
```

For matching the original binary environment install the PyTorch 2.4.1 CUDA 12.4 wheel; other devices/versions may differ. CPU runs are supported but substantially slower and device-specific RNG means results will not be bitwise identical. Outputs may vary with GPU kernels and numerical precision. The stored outputs are the original measured evidence. Commands overwrite generated outputs in `artifacts/` and `results/`; preserve a copy if comparing the exact original run.

Generate a small experimental MHD batch (the fields array has shape `[n,12,8,8,8]`, channels u₀,b₀,u₁,b₁ each with three Cartesian components):

```bash
python code/sample_mhd.py --checkpoint artifacts/mhd/baseline_11.pt --nu 0.06 --eta 0.10 --n 8 --constraint projected_budget --out samples.npz
```

The generator is for this benchmark, not a validated dynamo or assimilation model. See REPORT.md for the physics and limitations.
