# Dataset card: cursor kinematic ABC coefficients (H168)

## What this is

`dataset.npz` holds the packed Fourier coefficients used to train the H168 ResMLP. It is measured in this repository by `experiments/cursor_fm_train.py`. It is not a published observational dataset.

## Contents

- `coefficients`: float32 array, one row per snapshot, packed real and imaginary parts of the half-ball modes at kmax=4, six channels (velocity is not stored; the magnetic field of the kinematic run is)
- `rm`: the Reynolds number of each row
- `modes`: the integer wavevectors from `half_ball_modes(4)`

Training rows only. Held-out Rm=12 is not in this file. It is resimulated at score time.

## How it was built

For each seed in 0, 1, 2, 3, 4, and each Rm in 8, 10, 11, 13, 14, 16, and each time in 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, the script integrates the kinematic ABC dynamo at n=16 and packs the magnetic field. That is 5 × 6 × 8 = 240 rows. Normalization mean and standard deviation are computed per seed inside the trainer and stored in the matching checkpoint, not in this npz.

## Splits

There is no random split. The held-out parameter is Rm=12 for every seed. Seeds are the replicates, not a train/test cut of rows.

## Limits

n=16, kmax=4, laminar ABC forcing, one solver. Do not treat a row as a turbulent dynamo snapshot.

## Companion files

`metrics.json` is the score of the model trained on these rows. `MODEL_CARD.md` describes the checkpoints.

## License

Same as the repository that holds this file.
