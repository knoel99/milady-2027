# NeurIPS-style checklist (short answers)

- **Claims match results / limits**: yes; 2-D, 32x32, one seed, 400 steps, stated in REPORT.md.
- **Reproducibility**: `reproduce.sh`; seeds fixed (data seed 123, train seed 0, sampling seed 1). CPU, float32; bitwise determinism not guaranteed on shared CPU threads.
- **Statistical significance**: NOT established. One training seed per method; no confidence intervals over seeds. Only a sampling-noise floor from real data (random subset of same size) is reported for calibration. Conclusions are therefore descriptive.
- **Compute**: ~4 CPU cores shared, ~15 min training (4 models in parallel) + ~10 min data generation. No GPU (cloud API unreachable). Cloud spend 0. LLM spend: see COSTS.md.
- **Licences of assets**: all code/data self-generated (MIT). Libraries: PyTorch (BSD-3), NumPy/SciPy (BSD-3), Matplotlib (PSF-based). No external datasets or pretrained models.
- **Use of AI**: the whole study (code, experiments, report) was produced autonomously by Claude Sonnet 5.5 (Claude Code harness). No sub-agents or other models were used.
- **Human subjects / data risk**: none.
