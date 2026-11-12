# Data storage of the pilot

Decision of 2026-11-12 (team claude), asked by `race/PILOT.md` before producing more than about 1 GB.

## What is stored where

| Data | Size | Where | In git |
|---|---|---|---|
| E4 snapshots: 11 files `eta_<η>.npz`, 2400 snapshots each, every Galerkin mode of the 16³ solver as Craya–Herring potentials (665 modes × 8 reals, float32, compressed) | 507 MB | `experiments/data_e4/` in the session container | no (`.gitignore`) |
| E4 quick snapshots | 81 MB | `experiments/data_e4_quick/` | no |
| Model weights kept for later evaluations (W4s and W5 per seed) | about 50 MB each | `experiments/data_e4/model_*.pt` | no |
| Summaries, per-seed results, reference statistics, digest, logs of the GPU jobs, compute ledger | under 5 MB in all | `experiments/results/`, `research/` | yes |

No file above 50 MB is committed. Nothing is uploaded to an object store: the pilot has no storage budget
line, the RunPod credit is kept for GPU time, and a network volume could not be read from this session.

## How it is read back

- This session: `experiments/e4_data.py` (`load`, `data_dir`); the directory can be moved with `E4_DATA`.
- A RunPod pod: it regenerates the data from the committed script at the commit of the job
  (`python experiments/e4_data.py --jobs <cores>`: 30 min on the 4 cores of this container, measured;
  a pod has 12 to 32 vCPUs). Nothing is transferred to the pod.

## Regeneration

Every data set is a deterministic function of a committed script and its parameters:
`experiments/e4_data.py` (seeds `1000 + index of η`, float32, one thread per simulation). The
statistics of the regenerated data are checked against `experiments/results/e4_data.json` (committed).
Bit-for-bit identity across machines is not guaranteed (float32 FFT of a chaotic system); the laws are
the same, and the noise floors of the digest quantify the sampling variation.

## Cost and fate

Storage cost: none (container disk). If the container is reclaimed, the data are regenerated (30 min of
CPU) and the models retrained (about 1 h of one core per seed and group). After the pilot the container
copy disappears; the committed summaries and scripts remain. If a later experiment needs more than a few
GB (32³ or 64³ fields), the plan is the MFF/Zarr format of `docs/specs/data-format.md` with
`src/milady/storage.py` on an S3 bucket, which needs a storage budget from the owner.
