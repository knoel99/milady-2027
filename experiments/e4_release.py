"""E4 release - assemble the folder of a release: data in the MFF format, model files, catalogue, checksums, notes.

    python3 experiments/e4_release.py --mff DIR --npz DIR --run DIR --models DIR --out DIR [--url URL] [--repo-dir DIR]

Inputs (all written by ``experiments/e4_release_build.sh``, on CPU):

- ``--mff``: the 11 MFF files of the data (``python -m milady.data.convert e4``); ``--npz``: their source snapshots;
- ``--run``: the result files ``e4_mhd3d_s<seed>.json`` of the groups D and G trained and evaluated on these data, and the
  weights ``e4_model_W9_skip_sym_s<seed>.pt`` (``E4_SAVE_MODELS=1``);
- ``--models``: the parameter files of ``experiments/e4_release_models.py`` (latent space, G0, G1, maps of W16).

Output ``--out``, the assets of the release: the data files, the model files, a sample of the data, ``catalog.sqlite`` and
``catalog.json`` (``milady.catalog``: campaign, simulations, files, data set ``e4_mhd3d`` 1.0 with its splits; the models
released with their file, hyperparameters, commit, data set and evaluations; and, as records without files, the models of
the runs cited by the report with the evaluations of the committed result files), ``manifest.json``, ``SHA256SUMS`` and
``README.md``. ``--url`` is the address where the assets are published: it is written in the catalogue and in the notes.
``--repo-dir`` receives a copy of the small files (notes, manifest, checksums, catalogue export) to commit.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from sqlalchemy import text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

import e4_release_example as R  # noqa: E402
from milady import git_commit  # noqa: E402
from milady.catalog.api import Catalog  # noqa: E402
from milady.data import convert  # noqa: E402
from milady.data import format as mff  # noqa: E402

RES = ROOT / "experiments" / "results"
SAMPLE_ETA, SAMPLE_TRAJ, SAMPLE_T = "0.04899", 2, 25
METRICS = ("ed_ratio", "err_Eb_rel", "balance_residual_total", "balance_residual_magnetic", "prod_mean_over_d",
           "prod_fluct_over_d", "spec_err_b_l2", "hel_m_err_rel", "null_count_err_rel", "div_rel_b_max",
           "restart_drift_eb", "hc_sign_asym")
ARCH = {"G0": "Gaussian law, one mean and one 8 × 8 covariance per Fourier mode at each training η, interpolated linearly in the condition",
        "G1": "Gaussian law, mean and full sample covariance of the 5320 latent coordinates at each training η, interpolated linearly in the condition",
        "W9": "conditional flow matching on the potentials: ResMLP (width 512, depth 4) plus an explicit mode-wise affine term; Heun sampler, 50 steps",
        "W16": "samples of W9 sent through the linear map x → mean_G1 + (x − mean_W9) A that gives them the mean and covariance of G1"}
CONSTRAINT = {"G0": "vector potentials (zero divergence by design); law symmetric under B → −B",
              "G1": "vector potentials (zero divergence by design); law symmetric under B → −B",
              "W9": "vector potentials (zero divergence by design); velocity field equivariant under B → −B",
              "W16": "vector potentials; first two moments of the law imposed at sampling time"}
#: law → (variant in the committed result files of the report, run under results/replications)
CITED = {"G0": ("G0_gaussian_modes", "e4_nongauss"), "G1": ("G1_gaussian_full", "e4_recolour"),
         "W9": ("W9R_skip_sym", "e4_recolour"), "W16": ("W16_recoloured_full", "e4_recolour")}
#: law → variant in the result files of the release build
BUILT = {"G0": "G0_gaussian_modes", "G1": "G1_gaussian_full", "W9": "W9_skip_sym"}


def main_run_check(npz_dir: Path) -> dict:
    """Are the snapshots of ``npz_dir`` the realisation of the main run of the report?

    Compares the mean magnetic energy of each η over the kept window (time series of the solver) with the value recorded when
    the data of the main run were generated (``experiments/results/e4_data.json`` as committed: the build overwrites the file of
    its checkout, so the committed version is read from git). The solver is chaotic: two realisations differ in the second or
    third digit, the same one agrees to rounding."""
    try:
        blob = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:experiments/results/e4_data.json"], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        blob = (RES / "e4_data.json").read_text()
    ref = {round(r["eta"], 5): r["magnetic_energy"]["mean"] for r in json.loads(blob)["values"]}
    gaps = {}
    for path in sorted(npz_dir.glob("eta_*.npz")):
        with np.load(path) as d:
            eta = round(float(json.loads(str(d["config"]))["eta"]), 5)
            eb = float(d["diag_magnetic_energy"][np.asarray(d["diag_t"]) > 200 + 1e-9].mean())
        if eta in ref:
            gaps[f"{eta:.5f}"] = abs(eb / ref[eta] - 1)
    worst = max(gaps.values()) if len(gaps) == 11 else float("nan")
    return {"against": "experiments/results/e4_data.json (statistics of the data of the main run, generated on a GPU pod)",
            "max_relative_gap_of_E_B": worst, "same_realisation": bool(worst < 1e-9), "n_eta": len(gaps)}


def _within(gap: float) -> str:
    return "exactly" if gap == 0 else f"within {gap:.1e}"


def realisation_note(check: dict) -> str:
    """Provenance note written in the data files (``milady_note``)."""
    base = "Generated by experiments/e4_data.py with seed offset 0 in the build of the E4 release, on CPU. "
    if check["same_realisation"]:
        return base + ("This is the realisation of the data of the main run of the report: the mean magnetic energy of each η equals the value recorded for "
                       f"that run (experiments/results/e4_data.json) {_within(check['max_relative_gap_of_E_B'])}.")
    return base + ("The solver is chaotic and its float32 trajectories differ between processor types: this is another draw of the same law than the data "
                   f"of the main run of the report (largest relative gap of the mean magnetic energy: {check['max_relative_gap_of_E_B']:.1e}).")


def _place(src: Path, dst: Path) -> None:
    """Hard link when the two folders share a file system (the large files are not duplicated), copy otherwise."""
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def data_files(mff_dir: Path, out: Path, note: str) -> list[dict]:
    rows = []
    for src in sorted(mff_dir.glob("e4_eta*.h5"), reverse=True):
        path = out / src.name
        if not path.exists():
            _place(src, path)
        errs = mff.validate(path, full_scan=True)
        d = mff.read_mff(path, fields=[])
        g = mff.grid_info(path)
        with mff.open_mff(path) as f:
            n_traj = int(f.attrs["n_trajectories"])
        eb = np.asarray(d["diagnostics"]["magnetic_energy"])[:, np.asarray(d["diagnostics"]["time"]) > 200 + 1e-9].mean()
        rows.append({"file": path.name, "kind": "data", "format": "MFF 1.0 (HDF5, layout of The Well)", "size_bytes": path.stat().st_size,
                     "sha256": mff.sha256_file(path), "uuid": d["meta"]["uuid"], "eta": float(d["params"]["eta"]), "Rm": d["params"]["Rm"],
                     "split": d["meta"]["split"], "n_trajectories": n_traj, "n_t": g.get("n_t"), "t_start": g.get("t_start"),
                     "t_end": g.get("t_end"), "valid_full_scan": not errs, "problems": errs, "source_sha256": d["meta"]["source_sha256"],
                     "git_commit": d["meta"].get("git_commit"), "latent_roundtrip": d["meta"]["latent"]["roundtrip_max_abs_over_rms"],
                     "max_abs_divergence": d["meta"]["max_abs_divergence"], "E_B_mean": float(eb)})
    assert len(rows) == 11, f"{len(rows)} data files in {mff_dir}, expected 11"
    return rows


def model_files(run: Path, models: Path, out: Path) -> list[dict]:
    rows = []
    for src, kind, what in ([(models / R.SPACE, "latent space", "latent space of the models and its normalisation (state of FourierPotentialSpace)"),
                             (models / R.GAUSS.format(law="G0"), "G0", "parameters of the Gaussian law G0 (condition grid, mean and covariance per mode)"),
                             (models / R.GAUSS.format(law="G1"), "G1", "parameters of the Gaussian law G1 (condition grid, mean and factor A with AᵀA the covariance)")]
                            + [(run / R.WEIGHTS.format(seed=s), "W9", f"weights of the flow-matching model W9, seed {s}") for s in range(5)]
                            + [(models / R.MAP.format(seed=s), "W16", f"linear map of W16 at the held-out η for W9 of seed {s}") for s in range(5)]):
        if not src.exists():
            continue
        path = out / src.name
        if not path.exists():
            _place(src, path)
        rows.append({"file": path.name, "kind": kind, "format": "PyTorch (torch.save of a dictionary of tensors)", "content": what,
                     "size_bytes": path.stat().st_size, "sha256": mff.sha256_file(path)})
    return rows


def sample(npz_dir: Path, out: Path, note: str) -> dict:
    path = out / f"e4_sample_eta{SAMPLE_ETA}.h5"
    if not (path.exists() and not mff.validate(path)):
        convert.convert_e4_file(npz_dir / f"eta_{SAMPLE_ETA}.npz", path, split="test", max_members=SAMPLE_TRAJ, max_snapshots=SAMPLE_T,
                                extra_meta={"note": note + f" Sample: the first {SAMPLE_TRAJ} trajectories and {SAMPLE_T} snapshots."})
    return {"file": path.name, "kind": "data sample", "format": "MFF 1.0 (HDF5)", "size_bytes": path.stat().st_size, "sha256": mff.sha256_file(path),
            "content": f"η = {SAMPLE_ETA}, {SAMPLE_TRAJ} trajectories × {SAMPLE_T} snapshots"}


def _evals(cat: Catalog, mid: str, rows: list[dict], cfg: dict, seed: int, details: dict) -> int:
    n = 0
    for row in rows:
        for m in METRICS:
            if isinstance(row.get(m), int | float):
                cat.add_evaluation(mid, {"eta": row["eta"], "nu": cfg["nu"], "kf": cfg["kf"]}, m, row[m], int(row["n"]), seed, details=details)
                n += 1
    return n


def _w16(models: Path) -> dict | None:
    """Evaluations of W16 written per seed by e4_release_models.py, merged."""
    parts = [json.loads(p.read_text()) for p in sorted(models.glob("e4_release_w16_s*.json"))]
    if not parts:
        return None
    by_seed = {str(p["config"]["seed"]): p["config"]["n_recolour"] for p in parts}
    lo, hi = min(by_seed.values()), max(by_seed.values())
    return {"config": {**{k: v for k, v in parts[0]["config"].items() if k != "seed"}, "n_recolour": lo if lo == hi else f"{lo} to {hi}",
                       "n_recolour_by_seed": by_seed}, "evaluation": {str(p["config"]["seed"]): p["evaluation"] for p in parts}}


def catalogue(out: Path, run: Path, models: Path, files: list[dict], url: str) -> dict:
    db = out / "catalog.sqlite"
    db.unlink(missing_ok=True)
    cat = Catalog(f"sqlite:///{db}")
    members = []
    for f in files:
        ids = cat.ingest_mff((out / f["file"]).resolve().as_uri(), campaign="e4_mhd3d")
        members.append((ids["file_id"], f["split"]))
    cat.create_campaign("e4_mhd3d", config_yaml="source: experiments/e4_data.py\n",
                        description="E4: saturated 3D MHD dynamo, constant ABC forcing at kf = 2, ν = 0.05 (Re = 10), 11 magnetic "
                                    "diffusivities η from 0.08 to 0.03, 16³ grid, 24 trajectories × 100 snapshots per η.")
    ds_id = cat.register_dataset("e4_mhd3d", "1.0", members, description="E4: snapshots of a saturated 3D MHD dynamo on a 16³ grid (ABC forcing, "
                                 "Re = 10), conditioned on η: 6 training, 2 validation and 3 held-out test values.")
    commit, sha = os.environ.get("E4_MODEL_COMMIT") or git_commit(), {f["file"]: f["sha256"] for f in model_files(run, models, out)}
    out_models = []
    w16 = _w16(models)
    for seed in range(5):                                                    # the models of this release, with their files
        f = run / f"e4_mhd3d_s{seed}.json"
        if not f.exists():
            continue
        r = json.loads(f.read_text())
        for law in ("G0", "G1", "W9", "W16"):
            name = {"G0": R.GAUSS.format(law="G0"), "G1": R.GAUSS.format(law="G1"), "W9": R.WEIGHTS.format(seed=seed), "W16": R.MAP.format(seed=seed)}[law]
            if name not in sha:
                continue
            need = [R.SPACE, name] + ([R.WEIGHTS.format(seed=seed)] if law == "W16" else [])
            hyper = {"law": law, "seed": seed, "config": r["config"], "files": {n: sha.get(n) for n in need}, "dataset": "e4_mhd3d 1.0 (this release)",
                     "reload": f"python3 experiments/e4_release_example.py --dir e4_release --download --law {law} --seed {seed}",
                     "seed_meaning": "seed of the draws (one parameter file for the five)" if law in ("G0", "G1") else "seed of the training of W9"}
            if law == "W16":
                rows, hyper["n_recolour"] = (w16["evaluation"].get(str(seed), []), w16["config"]["n_recolour_by_seed"].get(str(seed))) if w16 else ([], None)
                hyper["evaluation"] = "512 samples per held-out η outside the estimate of the map; no restart in the solver"
            else:
                rows, hyper["times"] = r["evaluation"].get(BUILT[law], {}).get("test", []), r["times"].get(BUILT[law], {})
            mid = cat.register_model(f"e4/released/{law}/seed{seed}", ARCH[law], CONSTRAINT[law], hyper, dataset_id=ds_id,
                                     checkpoint_uri=f"{url}/{name}", git_commit=commit)
            n_eval = _evals(cat, mid, rows, r["config"], seed, {"run": "release build", "law": law})
            out_models.append({"id": mid, "name": f"e4/released/{law}/seed{seed}", "law": law, "seed": seed, "status": "released", "file": name,
                               "sha256": sha[name], "url": f"{url}/{name}", "git_commit": commit, "dataset": "e4_mhd3d 1.0", "evaluations": n_eval})
    for law, (variant, cited_run) in CITED.items():                          # the runs cited by the report: records without files
        for seed in range(5):
            f = RES / "replications" / cited_run / f"e4_mhd3d_s{seed}.json"
            if not f.exists():
                continue
            r = json.loads(f.read_text())
            hyper = {"law": law, "variant": variant, "seed": seed, "config": r["config"], "times": r["times"].get(variant, {}),
                     "result_file": str(f.relative_to(ROOT)),
                     "weights": "not kept: the GPU pod of the run was deleted with its files; the released models are the same code retrained on the released data",
                     "training_data": "E4 data as regenerated on the pod of the run (not stored): another draw of the law of the data set e4_mhd3d 1.0"}
            mid = cat.register_model(f"e4/cited/{law}/seed{seed}", ARCH[law], CONSTRAINT[law], hyper, dataset_id=None, checkpoint_uri=None, git_commit="")
            n_eval = _evals(cat, mid, r["evaluation"][variant]["test"], r["config"], seed, {"run": cited_run, "variant": variant})
            out_models.append({"id": mid, "name": f"e4/cited/{law}/seed{seed}", "law": law, "seed": seed, "status": "cited by the report, no file",
                               "result_file": hyper["result_file"], "evaluations": n_eval})
    summary: dict[str, dict] = {}
    for status in ("released", "cited"):
        for law in ARCH:
            per: dict[tuple[str, float], list[float]] = {}
            for m in (x for x in out_models if x["name"].startswith(f"e4/{status}/{law}/")):
                for row in cat.eval_summary(m["id"]):
                    per.setdefault((row["metric"], row["parameters"]["eta"]), []).append(row["mean"])
            summary[f"{status}/{law}"] = {f"{metric} @ eta={eta:g}": {"mean_over_seeds": float(np.mean(v)), "sd_over_seeds": float(np.std(v, ddof=1)) if len(v) > 1 else None,
                                                                    "seeds": len(v)} for (metric, eta), v in sorted(per.items())}
    sims = [{k: s.get(k) for k in ("id", "code", "parameters", "grid", "status", "git_commit")} for s in cat.query_simulations(campaign="e4_mhd3d")]
    ds = cat.dataset_files("e4_mhd3d", "1.0")
    cat.close()
    with Catalog(f"sqlite:///{db}").engine.begin() as conn:               # the files are published at `url`, not where they were built
        local = out.resolve().as_uri()
        conn.execute(text("UPDATE file SET uri = replace(uri, :a, :b)"), {"a": local, "b": url})
    export = {"dataset": {"name": "e4_mhd3d", "version": "1.0", "id": ds_id,
                          "files": [{"id": r["id"], "uri": r["uri"].replace(out.resolve().as_uri(), url), "sha256": r["sha256"], "size_bytes": r["size_bytes"],
                                     "split": r["split"], "simulation_id": r["simulation_id"]} for r in ds]},
              "simulations": sims, "models": out_models, "evaluation_summary": {k: v for k, v in summary.items() if v}}
    (out / "catalog.json").write_text(json.dumps(export, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return export


def _cell(ev: dict, key: str, metric: str) -> str:
    vals = [v["mean_over_seeds"] for k, v in ev.get(key, {}).items() if k.startswith(metric + " @")]
    return ", ".join(f"{x:.3g}" for x in vals) if vals else "not evaluated"


def readme(man: dict, export: dict, url: str) -> str:
    files, mods, ev = man["data_files"], man["model_files"], export["evaluation_summary"]
    total = sum(f["size_bytes"] for f in files)
    rows = "\n".join(f"| [`{f['file']}`]({url}/{f['file']}) | {f['eta']:.5f} | {f['Rm']:.2f} | {f['split']} | {f['size_bytes'] / 2**20:.1f} | `{f['sha256'][:16]}…` |" for f in files)
    mrows = "\n".join(f"| [`{f['file']}`]({url}/{f['file']}) | {f['content']} | {f['size_bytes'] / 2**20:.1f} | `{f['sha256'][:16]}…` |" for f in mods)
    metrics = (("energy distance over the noise floor", "ed_ratio"), ("relative error of the magnetic energy", "err_Eb_rel"),
               ("third-order part of the production over the dissipation", "prod_fluct_over_d"), ("residual of the energy balance", "balance_residual_total"),
               ("null-count error", "null_count_err_rel"), ("restart drift of the magnetic energy", "restart_drift_eb"))
    cmp_rows = "\n".join(f"| {law} | {name} | {_cell(ev, 'cited/' + law, m)} | {_cell(ev, 'released/' + law, m)} |" for law in ARCH for name, m in metrics)
    n_rec = man.get("n_recolour")
    chk = man["main_run_check"]
    if chk["same_realisation"]:
        which = ("These files were generated by this build from the committed script and seeds (`experiments/e4_data.py`), on the CPU of a hosted runner. "
                 "They are the realisation of the data of the main run of the report: the mean magnetic energy of each of the 11 files equals the value "
                 f"recorded when the data of that run were generated on a GPU pod (`experiments/results/e4_data.json`), {_within(chk['max_relative_gap_of_E_B'])}. "
                 "The solver is chaotic and some processor types give other trajectories from the same seeds; the second realisation on which most later "
                 "hypotheses were also run uses other seeds (`E4_DATA_SEED=100`) and is not part of this release.")
        trainings = ("They were trained on the same data as the cited runs of the main realisation, with the arithmetic of a CPU instead of a GPU: the Gaussian "
                     "laws, which are closed-form fits, reproduce the cited numbers, and the flow-matching model is another training of the same model.")
    else:
        which = ("The solver is chaotic and its float32 trajectories differ between processor types. These files were generated by this build from the "
                 "committed script and seeds (`experiments/e4_data.py`); they are another draw of the same law than the data of the main run of the report "
                 f"(largest relative gap of the mean magnetic energy: {chk['max_relative_gap_of_E_B']:.1e}).")
        trainings = "They are other trainings on another draw of the data than the cited runs."
    return f"""# E4 release 1.0: data in the MFF format, model files, catalogue

Generated by `experiments/e4_release.py` (do not edit; run the build again). Built by `experiments/e4_release_build.sh` on
{man['host']}: the snapshots, the reference statistics and the models at commit `{man['models_commit']}`, the data files in the MFF
format and this folder at commit `{man['git_commit']}`. Everything was computed on CPU; no file comes from a GPU run.

All files: {url} (checksums: [`SHA256SUMS`]({url}/SHA256SUMS); list with sizes: [`manifest.json`]({url}/manifest.json)).

## The data set `e4_mhd3d` 1.0

Saturated 3D MHD dynamo in a periodic box, constant ABC force at $k_f = 2$, ν = 0.05 (Re = 10), 16³ grid (every mode
$|m_i| \\le 5$ of the solver), 11 magnetic diffusivities η from 0.08 to 0.03 (Rm = 6.25 to 16.7): 6 training, 2 validation and
3 held-out test values. Each file holds {files[0]['n_trajectories']} trajectories × {files[0]['n_t']} snapshots (t = {files[0]['t_start']:g} to {files[0]['t_end']:g}, one every 2 time units, after
a transient of 200), the fields `velocity` and `magnetic_field` in float32, and the time series of the solver diagnostics
(energies, injection, dissipations, helicities; transient included). Format: MFF 1.0 (`docs/specs/data-format.md`), an HDF5
file with the layout of The Well. Every file passes `validate(..., full_scan=True)`: {sum(f['valid_full_scan'] for f in files)} of {len(files)}. Total: {total / 2**30:.2f} GiB.

| File | η | Rm | split | MiB | SHA-256 |
|---|---|---|---|---|---|
{rows}

The fields are band-limited: the potentials on which the models are trained are recovered from the stored fields by
`milady.data.convert.e4_latents(path)`, within {max(f['latent_roundtrip'] for f in files):.1e} of their root-mean-square value. Largest stored |∇·B|: {max(f['max_abs_divergence']['magnetic_field'] for f in files):.1e}.
A small sample for a first look: [`{man['sample']['file']}`]({url}/{man['sample']['file']}) ({man['sample']['content']}, {man['sample']['size_bytes'] / 2**20:.1f} MiB).

**Which realisation.** {which}

## The models

| File | Content | MiB | SHA-256 |
|---|---|---|---|
{mrows}

**What these models are.** The weights of the runs cited by the report were not kept: each GPU pod was deleted with its files at
the end of its job. The models here are the same code, seeds, widths and iterations **retrained by this build on the data of this
release, on CPU**, and evaluated by the same pipeline (`experiments/e4_mhd3d.py`, groups D and G) against the reference
statistics of these data. {trainings} Their numbers are in the
right column below, the numbers of the report in the left one. The map of W16 is estimated here on {n_rec} samples of W9 per
η (131 072 in the report, on a GPU), and W16 is evaluated on 512 samples outside that estimate, without the restart in the solver.

| Law | Metric at the held-out η = 0.0331, 0.0490, 0.0725 (mean over the five seeds) | cited by the report (GPU runs) | released (this build) |
|---|---|---|---|
{cmp_rows}

## The catalogue

[`catalog.sqlite`]({url}/catalog.sqlite) (`milady.catalog`, SQLite; [`catalog.json`]({url}/catalog.json) is a readable export): the campaign
`e4_mhd3d` with its 11 simulations and files, the data set `e4_mhd3d` 1.0 with its splits, and {len(export['models'])} model entries: the released
models (`e4/released/<law>/seed<k>`: file address, SHA-256, hyperparameters, commit, data set, evaluations) and, as records
without files, the models of the cited runs (`e4/cited/<law>/seed<k>`, with the evaluations of the committed result files).

```bash
PYTHONPATH=src python3 -m milady.catalog --url sqlite:///catalog.sqlite summary
```

## Reload a law and draw samples

From a checkout of the repository at the commit above (dependencies: `infra/env/requirements.txt`), `--download` fetches the
files that are needed and checks their SHA-256:

```bash
python3 experiments/e4_release_example.py --dir e4_release --download --law G1 --eta 0.04899 --n 256
```

```bash
python3 experiments/e4_release_example.py --dir e4_release --download --law W16 --seed 0 --eta 0.04899 --n 256 --out samples.h5
```

In Python:

```python
import sys; sys.path[:0] = ["src", "experiments"]
import e4_release_example as R
for name in (R.SPACE, R.GAUSS.format(law="G1"), R.WEIGHTS.format(seed=0)):
    R.fetch("e4_release", name)                       # download and check the SHA-256
space = R.load_space("e4_release")                    # latent space and its normalisation
g1 = R.load_gaussian("e4_release", "G1")              # Gaussian law with the full covariance
w9 = R.load_w9("e4_release", space, seed=0)           # flow-matching model
z = R.sample_w9(w9, space, eta=0.04899, n=64)         # normalised latents (64, 665, 8)
fields = R.to_fields(space, z)                        # "velocity", "magnetic_field": (64, 16, 16, 16, 3)
z1 = g1.sample(R.cn(0.04899), 64)                     # the same for the Gaussian law
```

Read a data file, and train on it (`milady.train`): `milady.data.read_mff(path)` returns the fields, coordinates, parameters and
diagnostics; `milady.data.convert.e4_latents(path)` the training latents; `experiments/e4_mhd3d.py` is the training script.

## Check a download

```bash
sha256sum -c SHA256SUMS
```

```bash
PYTHONPATH=src python3 -m milady.data.convert validate --full e4_eta*.h5
```
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print-note", action="store_true", help="print the provenance note of the data in --npz and exit")
    ap.add_argument("--npz", required=True)
    ap.add_argument("--mff")
    ap.add_argument("--run")
    ap.add_argument("--models")
    ap.add_argument("--out")
    ap.add_argument("--url", default=R.RELEASE_URL)
    ap.add_argument("--host", default="the CPU of a GitHub Actions runner")
    ap.add_argument("--build", default="data, reference statistics, models and parameter files in one job")
    ap.add_argument("--repo-dir", default=None)
    a = ap.parse_args()
    if a.print_note:
        print(realisation_note(main_run_check(Path(a.npz).resolve())))
        return
    mff_dir, npz_dir, run, models, out = (Path(x).resolve() for x in (a.mff, a.npz, a.run, a.models, a.out))
    out.mkdir(parents=True, exist_ok=True)
    check = main_run_check(npz_dir)
    note = realisation_note(check)
    w16 = _w16(models)
    man = {"release": "e4-data-v1.0", "url": a.url, "git_commit": git_commit(), "models_commit": os.environ.get("E4_MODEL_COMMIT") or git_commit(),
           "host": a.host, "build": a.build,
           "dataset": {"name": "e4_mhd3d", "version": "1.0", "format": "MFF 1.0"}, "main_run_check": check, "n_recolour": w16["config"]["n_recolour"] if w16 else None,
           "data_files": data_files(mff_dir, out, note), "model_files": model_files(run, models, out), "sample": sample(npz_dir, out, note)}
    export = catalogue(out, run, models, man["data_files"], a.url)
    man["catalog"] = {"simulations": len(export["simulations"]), "dataset_files": len(export["dataset"]["files"]), "models": len(export["models"]),
                      "released_models": sum(m["status"] == "released" for m in export["models"]), "evaluations": sum(m["evaluations"] for m in export["models"])}
    if w16:
        (out / "e4_release_w16.json").write_text(json.dumps(w16, indent=1) + "\n", encoding="utf-8")
    for s in range(5):                                                      # the evaluations of the released models, as written by the pipeline
        if (run / f"e4_mhd3d_s{s}.json").exists():
            shutil.copy2(run / f"e4_mhd3d_s{s}.json", out / f"e4_release_eval_s{s}.json")
    (out / "README.md").write_text(readme(man, export, a.url), encoding="utf-8")
    other = sorted(p for p in out.iterdir() if p.is_file() and p.name not in {f["file"] for f in man["data_files"] + man["model_files"]} | {"manifest.json", "SHA256SUMS", man["sample"]["file"]})
    man["other_files"] = [{"file": p.name, "size_bytes": p.stat().st_size, "sha256": mff.sha256_file(p)} for p in other]
    (out / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    every = man["data_files"] + man["model_files"] + [man["sample"]] + man["other_files"]
    (out / "SHA256SUMS").write_text("".join(f"{f['sha256']}  {f['file']}\n" for f in every) + f"{mff.sha256_file(out / 'manifest.json')}  manifest.json\n", encoding="utf-8")
    if a.repo_dir:
        repo = Path(a.repo_dir)
        repo.mkdir(parents=True, exist_ok=True)
        for n in ("README.md", "manifest.json", "SHA256SUMS", "catalog.json", "e4_release_w16.json"):
            if (out / n).exists():
                shutil.copy2(out / n, repo / n)
    print(json.dumps({"data_files": len(man["data_files"]), "all_valid": all(f["valid_full_scan"] for f in man["data_files"]),
                      "model_files": len(man["model_files"]), **man["catalog"], "total_GiB": round(sum(p.stat().st_size for p in out.iterdir() if p.is_file()) / 2**30, 2),
                      "largest_file_GiB": round(max(p.stat().st_size for p in out.iterdir() if p.is_file()) / 2**30, 2)}))


if __name__ == "__main__":
    main()
