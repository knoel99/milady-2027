# milady-2027

Preparation material, a prospective internship report and a PhD proposal for the M2 internship **"Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems"** (ANR project MilaDy, ANR-25-CE51-0077; CEREA/ENPC and LISN, 2027).

**Site**: <https://knoel99.github.io/milady-2027/>

> This is an independent project. It is neither produced nor endorsed by École nationale des ponts et chaussées, LISN, Observatoire de la Côte d'Azur, the ANR or the internship supervisors. The reference offer is the PDF published by the supervisors: <https://scheng2024.github.io/stage_milady_2027.pdf>. The internship report is **prospective**: it is written as if it concluded the internship, but its numerical results come only from the small-scale (CPU) experiments of this repository, described and reproducible in `experiments/`.

## Layout

```
site/                  published site (Quarto sources; rendered and deployed by .github/workflows/pages.yml)
  index.qmd            home: the offer, the MilaDy project, the path
  prep/p1-…/ … p8-…/   eight preparation modules, from L1 to M2 research level
  report/  thesis/     internship report and PhD proposal
  supervisors/ computing/ experiments/ interactive/
  assets/  figures/    stylesheet, page script, interactive widgets, schematic figures
experiments/           E1–E3 scripts, shared code (common.py), results/ (JSON, digest.md)
research/              hypothesis register and lab journal (empty until research starts)
src/milady/            Python package: MFF data format, catalogue, storage, 3D MHD solver, training, evaluation
tests/                 pytest suite for the package (make test)
infra/                 deployment: Docker, cloud VM, Slurm/Apptainer, campaign configs, SQL schema
docs/                  developer docs: specs/ (page contract, notation, theory brief, fact bases), ARCHITECTURE.md, review-2026-11.md
tools/                 site rendering and checks
```

## Reproduce the experiments

Python 3.11+ with NumPy, SciPy, Matplotlib and PyTorch (CPU is enough).

```bash
cd experiments
python3 e1_gissinger.py   # E1: invariant law of the Gissinger reversal model (≈ 2–3 h CPU, resumable)
python3 e2_data.py        # E2: forced 2D MHD snapshots (≈ 30 min)
python3 e2_mhd2d.py       # E2: five constraint variants + distributional constraints (≈ 1 h)
python3 e3_abc.py         # E3: kinematic ABC dynamo, growth rate versus Rm (≈ 23 min)
python3 figures.py        # plots
python3 digest.py > results/digest.md   # the only source of numbers quoted by the pages
```

Every script accepts `--quick` (a reduced run of a few minutes).

## Package and HPC infrastructure

`src/milady/` and `infra/` scale the experiments up for the thesis: MFF data format (HDF5, compatible with The Well), PostgreSQL/SQLite catalogue of simulations, models and evaluations, S3 storage, MLflow tracking, 3D MHD solver (PyTorch), constrained training and evaluation. Guide: [`infra/README.md`](infra/README.md); contract: [`docs/specs/infra.md`](docs/specs/infra.md).

```bash
make setup && make smoke RUN=local      # portable, no Docker (SQLite catalogue, files under data/)
sudo infra/deploy/bootstrap_vm.sh       # cloud VM: Docker, PostgreSQL, MinIO, MLflow, end-to-end test
python -m milady.sweep infra/configs/stage2_abc3d.yaml --scheduler slurm   # Slurm cluster
```

## Build the site

Requirements: [Quarto](https://quarto.org) 1.7.32, Python 3, Node.js (KaTeX check). `tools/setup-cloud.sh` installs them in a cloud session.

```bash
python3 tools/render.py --all     # Quarto render + pinned KaTeX tags (SRI)
python3 tools/check_gates.py      # sections, exercises, links, anchors
NODE_PATH=<node_modules with katex@0.19.0> node tools/check_katex.mjs $(find site -name index.html)
```

Rendered `index.html` files are not versioned. On every push to `main`, `.github/workflows/pages.yml` renders all pages, runs the checks and publishes `site/` (Settings → Pages → Source: GitHub Actions).

## Licence

Code and texts: Apache 2.0 (`LICENSE`). Quoted official texts (offer, ANR abstract) remain the property of their authors. KaTeX (MIT) is loaded from jsDelivr.
