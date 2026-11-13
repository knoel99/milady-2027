# Model card: cursor ResMLP conditional flow (H168)

## What this is

Five checkpoints of `milady.train.fm3d.ResMLP`, one per seed. Width 256, depth 4, expansion 2, embedding 128, eight Fourier features, six channels, one condition. The sampling constraint is `project_solenoidal` after every Heun step. This is a measured checkpoint from this repository. It is not a published foundation model.

## Training

- Script: `experiments/cursor_fm_train.py`
- Command: `python3 experiments/cursor_fm_train.py --device cuda --steps 4000 --out-dir experiments/results/cursor_fm`
- Data: packed kinematic ABC coefficients, n=16, kmax=4, seeds 0-4
- Training Rm: 8, 10, 11, 13, 14, 16. Held-out Rm: 12
- Times: 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0
- Optimizer: Adam, learning rate 1e-3, 4000 steps, batch 32
- Each seed is normalized by its own coefficient mean and standard deviation. Those tensors are stored in the checkpoint.
- GPU: pod `1lzm2p635n6com`, RTX 4090, 0.1656 h, 0.1474 USD, commit `8064093778d74fda66c29ee5533160690d8b3a94`

## Measured scores

File `metrics.json`, seeds 0-4, all finite. Mean ± SE.

| Metric | Learned mean ± SE | Same-kmax midpoint mean |
| --- | --- | --- |
| energy-distance ratio (C1) | 0.769302 ± 0.202169 | 0.743129 |
| max relative divergence | 1.9865e-08 ± 7.71e-10 | see the midpoint file |
| C4, spectrum plus helicity | 0.309777 ± 0.0783 | not the H168 criterion |

H168 is supported. The pre-registered criterion was a learned mean C1 of at most 1.2. Seed 0 is 1.5077905808818028 and the mean is still under 1.2. The learned mean does not beat the midpoint. The learned C4 misses 0.1. That miss is not a registered hypothesis.

## Files

`weights_s0.pt` through `weights_s4.pt`. Each file holds `state`, `steps`, `kmax`, `seed`, `mean`, and `std`.

## Limits

n=16 and kmax=4. Not a resolved 3D dynamo generator. Not a substitute for the kmax=6 midpoint on C2 or C4. The forty-step flows near ratio 750 are a different, refuted protocol.

## License

Same as the repository that holds this file.
