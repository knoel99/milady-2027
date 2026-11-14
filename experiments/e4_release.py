"""E4 release - data in the MFF format, catalogue of the data set and of the cited models, checksums.

    python3 experiments/e4_release.py            # writes research/release/

What it does, from the root of the repository:

1. checks the MFF files of ``experiments/data_e4_mff`` (written by ``python -m milady.data.convert e4``; they are
   converted first if absent) with the full validation of the format, and records their size and SHA-256;
2. writes a small sample file (one held-out η, 2 trajectories × 25 snapshots) that fits in the repository;
3. builds a catalogue (``milady.catalog``, SQLite): the campaign ``e4_mhd3d``, its 11 simulations and files, the data
   set ``e4_mhd3d`` 1.0 with its splits, and the four laws cited by the report (G0, G1, W9, W16) for the five seeds,
   with their evaluations at the held-out η read from the committed result files;
4. writes ``manifest.json``, ``SHA256SUMS``, ``catalog.json`` (a readable export of the catalogue) and ``README.md``.

The large files stay where they are (git-ignored); the manifest gives their path and size. The weights of the trained
models of the cited runs were not kept (the GPU pods are deleted after each job): the catalogue records how to regenerate
them. When ``experiments/results/replications/e4_release_cpu`` holds the model W9 retrained on the released data set on the
CPU of the session (``e4_model_W9_skip_sym_s<seed>.pt`` with the result files of the same run), these weights are
registered as separate models, with their own evaluations, and listed in the manifest.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from milady import git_commit  # noqa: E402
from milady.catalog.api import Catalog  # noqa: E402
from milady.data import convert  # noqa: E402
from milady.data import format as mff  # noqa: E402

RES = ROOT / "experiments" / "results"
NOTE = ("Realisation generated in the container of the pilot session (Intel CPU) by experiments/e4_data.py with seed "
        "offset 0. The solver is chaotic and its float32 trajectories differ between processor types: this is another "
        "draw of the same law than the data regenerated on the GPU pods (AMD CPUs) for the results of the report.")
SAMPLE_ETA, SAMPLE_TRAJ, SAMPLE_T = "0.04899", 2, 25
METRICS = ("ed_ratio", "err_Eb_rel", "balance_residual_total", "balance_residual_magnetic", "prod_mean_over_d",
           "prod_fluct_over_d", "spec_err_b_l2", "hel_m_err_rel", "null_count_err_rel", "div_rel_b_max",
           "restart_drift_eb", "hc_sign_asym")
CPU_RUN = "e4_release_cpu"            # W9 retrained on the released data set, on CPU (weights kept)
JOB = "python3 tools/runpod_job.py run --hours 1.9 --outputs experiments/results/replications/{run} -- env E4_SAME_DATA=1 E4_SAVE_MODELS=1 bash experiments/e4_gpu_job.sh full '0 1 2 3 4' {run} {groups}"
#: law → (variant in the result files, run under results/replications, groups of the job, architecture, constraint, weights)
MODELS = {
    "G0": ("G0_gaussian_modes", "e4_nongauss", "D,E,G,N", "Gaussian law, one 8 × 8 covariance per Fourier mode, interpolated in η",
           "vector potentials (zero divergence by design); B → −B symmetry of the covariance",
           "closed form: milady.train.constraints.ModewiseGaussian(sign=…).fit(x_train, c_train), refitted from the data set in under 1 s"),
    "G1": ("G1_gaussian_full", "e4_recolour", "G,T,R", "Gaussian law, full 5320 × 5320 sample covariance per training η, interpolated in η",
           "vector potentials (zero divergence by design); B → −B symmetry of the covariance",
           "closed form: milady.train.constraints.FullGaussian(sign=…).fit(x_train, c_train), refitted from the data set in under 1 s"),
    "W9": ("W9R_skip_sym", "e4_recolour", "G,T,R", "conditional flow matching on the potentials: ResMLP (width 512, depth 4) plus an explicit mode-wise affine term",
           "vector potentials (zero divergence by design); velocity field equivariant under B → −B",
           "not kept (the pod of the job was deleted); retrained by the job below in about 1 min per seed on a GPU"),
    "W16": ("W16_recoloured_full", "e4_recolour", "G,T,R", "samples of W9 sent through the linear map that gives them the mean and covariance of G1 (estimated on 131 072 samples per η)",
            "vector potentials; first two moments of the law imposed at sampling time",
            "no weights of its own: W9 plus the map, recomputed at sampling time"),
}


def data_files(mff_dir: Path, npz_dir: Path) -> list[dict]:
    if not list(mff_dir.glob("e4_eta*.h5")):
        convert.convert_e4(npz_dir, mff_dir, extra_meta={"note": NOTE})
    ref = json.loads((RES / "e4_reference.json").read_text())["values"]
    rows = []
    for path in sorted(mff_dir.glob("e4_eta*.h5"), reverse=True):
        errs = mff.validate(path, full_scan=True)
        d = mff.read_mff(path, fields=[])
        eb = np.asarray(d["diagnostics"]["magnetic_energy"])[:, np.asarray(d["diagnostics"]["time"]) > 200 + 1e-9].mean()
        eta = float(d["params"]["eta"])
        pod = next((v["E_B"] for e, v in ref.items() if abs(float(e) - eta) < 1e-4), None)
        g = mff.grid_info(path)
        with mff.open_mff(path) as f:
            n_traj = int(f.attrs["n_trajectories"])
        rows.append({"file": path.name, "path": str(path.relative_to(ROOT)), "size_bytes": path.stat().st_size,
                     "sha256": mff.sha256_file(path), "uuid": d["meta"]["uuid"], "eta": eta, "Rm": d["params"]["Rm"],
                     "split": d["meta"]["split"], "n_trajectories": n_traj, "n_t": g.get("n_t"),
                     "t_start": g.get("t_start"), "t_end": g.get("t_end"), "valid_full_scan": not errs, "problems": errs,
                     "source": d["meta"]["source"], "source_sha256": d["meta"]["source_sha256"],
                     "git_commit": d["meta"].get("git_commit"), "latent_roundtrip": d["meta"]["latent"]["roundtrip_max_abs_over_rms"],
                     "max_abs_divergence": d["meta"]["max_abs_divergence"], "E_B_mean": float(eb),
                     "E_B_of_the_pod_realisation": pod, "E_B_gap_to_the_pod_realisation": None if pod is None else float(eb / pod - 1)})
    return rows


def sample(npz_dir: Path, out: Path) -> dict:
    path = out / f"e4_sample_eta{SAMPLE_ETA}.h5"
    if not (path.exists() and not mff.validate(path)):
        convert.convert_e4_file(npz_dir / f"eta_{SAMPLE_ETA}.npz", path, split="test", max_members=SAMPLE_TRAJ, max_snapshots=SAMPLE_T,
                                extra_meta={"note": NOTE + f" Sample: the first {SAMPLE_TRAJ} trajectories and {SAMPLE_T} snapshots."})
    return {"file": path.name, "path": str(path.relative_to(ROOT)), "size_bytes": path.stat().st_size, "sha256": mff.sha256_file(path),
            "valid_full_scan": not mff.validate(path, full_scan=True), "eta": float(SAMPLE_ETA), "n_trajectories": SAMPLE_TRAJ, "n_t": SAMPLE_T}


def catalogue(mff_dir: Path, npz_dir: Path, out: Path) -> dict:
    db = out / "catalog.sqlite"
    db.unlink(missing_ok=True)
    cat = Catalog(f"sqlite:///{db}")
    recs = convert.convert_e4(npz_dir, mff_dir, catalog=cat, verbose=False)
    assert all(r.get("reused") for r in recs), "the MFF files were rewritten: run the script again"
    ds = cat.dataset_files("e4_mhd3d", "1.0")
    models = []
    for law, (variant, run, groups, arch, constraint, weights) in MODELS.items():
        for seed in range(5):
            f = RES / "replications" / run / f"e4_mhd3d_s{seed}.json"
            r = json.loads(f.read_text())
            hyper = {"law": law, "variant": variant, "seed": seed, "config": r["config"], "times": r["times"].get(variant, {}),
                     "result_file": str(f.relative_to(ROOT)), "weights": weights,
                     "regenerate": JOB.format(run=run, groups=groups),
                     "training_data": "E4 data of the main run as regenerated on the pod of the job (not stored): another realisation "
                                      "of the law of the data set e4_mhd3d 1.0 (same script and seeds, other processor type)"}
            mid = cat.register_model(f"e4/{law}/seed{seed}", arch, constraint, hyper, dataset_id=None, checkpoint_uri=None, git_commit=git_commit())
            n_eval = 0
            for row in r["evaluation"][variant]["test"]:
                for m in METRICS:
                    if isinstance(row.get(m), int | float):
                        cat.add_evaluation(mid, {"eta": row["eta"], "nu": r["config"]["nu"], "kf": r["config"]["kf"]}, m, row[m], int(row["n"]), seed,
                                           details={"run": run, "variant": variant})
                        n_eval += 1
            models.append({"id": mid, "name": f"e4/{law}/seed{seed}", "law": law, "variant": variant, "run": run, "seed": seed,
                           "architecture": arch, "constraint_mechanism": constraint, "weights": weights,
                           "regenerate": hyper["regenerate"], "result_file": hyper["result_file"], "evaluations": n_eval})
    cpu = RES / "replications" / CPU_RUN
    ds_id = ds[0]["dataset_id"] if ds else None
    for seed in range(5):
        w, f = cpu / f"e4_model_W9_skip_sym_s{seed}.pt", cpu / f"e4_mhd3d_s{seed}_D.json"
        if not (w.exists() and f.exists()):
            continue
        r = json.loads(f.read_text())
        hyper = {"law": "W9-released", "variant": "W9_skip_sym", "seed": seed, "config": r["config"], "times": r["times"].get("W9_skip_sym", {}),
                 "result_file": str(f.relative_to(ROOT)), "weights_sha256": mff.sha256_file(w), "weights_size_bytes": w.stat().st_size,
                 "reload": f"python3 experiments/e4_release_example.py --weights {w.relative_to(ROOT)}",
                 "training_data": "data set e4_mhd3d 1.0 (the released files), trained on the CPU of the session container"}
        mid = cat.register_model(f"e4/W9-released/seed{seed}", MODELS["W9"][3], MODELS["W9"][4], hyper, dataset_id=ds_id,
                                 checkpoint_uri=w.resolve().as_uri(), git_commit=git_commit())
        n_eval = 0
        for row in r["evaluation"]["W9_skip_sym"]["test"]:
            for m in METRICS:
                if isinstance(row.get(m), int | float):
                    cat.add_evaluation(mid, {"eta": row["eta"], "nu": r["config"]["nu"], "kf": r["config"]["kf"]}, m, row[m], int(row["n"]), seed,
                                       details={"run": CPU_RUN, "variant": "W9_skip_sym"})
                    n_eval += 1
        models.append({"id": mid, "name": f"e4/W9-released/seed{seed}", "law": "W9-released", "variant": "W9_skip_sym", "run": CPU_RUN, "seed": seed,
                       "architecture": MODELS["W9"][3], "constraint_mechanism": MODELS["W9"][4],
                       "weights": str(w.relative_to(ROOT)), "weights_sha256": hyper["weights_sha256"], "weights_size_bytes": hyper["weights_size_bytes"],
                       "regenerate": f"E4_SAVE_MODELS=1 python3 experiments/e4_mhd3d.py --seed {seed} --group D --device cpu", "result_file": hyper["result_file"],
                       "evaluations": n_eval})
    summary: dict[str, dict] = {}
    for law in [*MODELS, "W9-released"]:                                                   # seed means per law, metric and held-out η
        per: dict[tuple[str, float], list[float]] = {}
        for m in (x for x in models if x["law"] == law):
            for row in cat.eval_summary(m["id"]):
                per.setdefault((row["metric"], row["parameters"]["eta"]), []).append(row["mean"])
        summary[law] = {f"{metric} @ eta={eta:g}": {"mean_over_seeds": float(np.mean(v)), "sd_over_seeds": float(np.std(v, ddof=1)), "seeds": len(v)}
                        for (metric, eta), v in sorted(per.items())}
    export = {"campaigns": cat.list_campaigns(),
              "dataset": {"name": "e4_mhd3d", "version": "1.0",
                          "files": [{k: r[k] for k in ("id", "uri", "sha256", "size_bytes", "split", "simulation_id") if k in r} for r in ds]},
              "simulations": [{k: s.get(k) for k in ("id", "code", "parameters", "grid", "status", "git_commit")}
                              for s in cat.query_simulations(campaign="e4_mhd3d")],
              "models": models, "evaluation_summary": {k: v for k, v in summary.items() if v}}
    (out / "catalog.json").write_text(json.dumps(export, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    cat.close()
    return export


def readme(man: dict) -> str:
    files, s = man["data_files"], man["sample"]
    total = sum(f["size_bytes"] for f in files)
    gaps = [abs(f["E_B_gap_to_the_pod_realisation"]) for f in files if f["E_B_gap_to_the_pod_realisation"] is not None]
    rows = "\n".join(f"| `{f['file']}` | {f['eta']:.5f} | {f['Rm']:.2f} | {f['split']} | {f['size_bytes'] / 2**20:.1f} | `{f['sha256'][:16]}…` |" for f in files)
    return f"""# E4 release 1.0: data in the MFF format, catalogue, cited models

Generated by `experiments/e4_release.py` (do not edit; run the script again). Commit of the conversion code: `{files[0]['git_commit']}`.

## What is here

| File | Content | In git |
|---|---|---|
| `manifest.json` | every file of the release with its path, size, SHA-256, identifier and checks | yes |
| `SHA256SUMS` | the same checksums in the format of `sha256sum -c` | yes |
| `{s['file']}` | sample of the data set: η = {s['eta']}, {s['n_trajectories']} trajectories × {s['n_t']} snapshots, {s['size_bytes'] / 2**20:.1f} MiB | yes |
| `catalog.sqlite`, `catalog.json` | catalogue (`milady.catalog`): campaign, 11 simulations and files, data set `e4_mhd3d` 1.0, 20 models with their evaluations; `catalog.json` is a readable export | yes |
| `experiments/data_e4_mff/e4_eta<η>.h5` | the data set: 11 files, {total / 2**30:.2f} GiB in all | no: in the container of the session |

## The data set `e4_mhd3d` 1.0

Saturated 3D MHD dynamo in a periodic box, constant ABC force at $k_f = 2$, ν = 0.05 (Re = 10), 16³ grid (every mode
$|m_i| \\le 5$ of the solver), 11 magnetic diffusivities η from 0.08 to 0.03 (Rm = 6.25 to 16.7): 6 training, 2 validation and
3 held-out test values. Each file holds {files[0]['n_trajectories']} trajectories × {files[0]['n_t']} snapshots (t = {files[0]['t_start']:g} to {files[0]['t_end']:g}, one every 2 time units, after
a transient of 200), the fields `velocity` and `magnetic_field` in float32, and the time series of the solver diagnostics
(energies, injection, dissipations, helicities; transient included). Format: MFF 1.0 (`docs/specs/data-format.md`),
readable as a data set of The Well. Every file passes `validate(..., full_scan=True)`: {sum(f['valid_full_scan'] for f in files)} of {len(files)}.

| File | η | Rm | split | MiB | SHA-256 |
|---|---|---|---|---|---|
{rows}

The fields are band-limited: the potentials on which the models are trained are recovered from the stored fields by
`milady.data.convert.e4_latents(path)`, within {max(f['latent_roundtrip'] for f in files):.1e} of their root-mean-square value. Largest stored |∇·B|: {max(f['max_abs_divergence']['magnetic_field'] for f in files):.1e}.

**Which realisation.** These files are the data generated in the container of the session. The results of the report were
computed on data regenerated on each GPU pod from the same script and seeds; the solver is chaotic and its float32
trajectories differ between processor types, so the two are different draws of the same law. The mean magnetic energy of these
files differs from that of the pod realisation (`experiments/results/e4_reference.json`) by at most {max(gaps) * 100:.1f} % over the 11 values of η.

## The cited models

Four laws × five seeds are in the catalogue, each with its evaluations at the three held-out η (source: the committed result
files named in `catalog.json`):

| Law | What it is | Weights |
|---|---|---|
""" + "\n".join(f"| {law} | {v[3]} | {v[5]} |" for law, v in MODELS.items()) + f"""

{weights_section(man)}
## Reload a law and draw samples

`experiments/e4_release_example.py` reads the data set, rebuilds the latent space from the training files, fits G0 and G1,
reloads W9 from a weight file, recolours it into W16, draws fields (u, B) on the 16³ grid at one η and prints their mean
energies against those of the data (about one minute on a CPU):

```bash
{reload_cmd(man)}
```

## Upload

The session cannot create a GitHub release. From a checkout that holds the files (this container), with the `gh` command
authenticated:

```bash
gh release create e4-data-v1.0 --repo knoel99/milady-2027 --target claude/modest-newton-zx8fqs --title "E4 data set 1.0 (MFF) and catalogue" --notes-file research/release/README.md experiments/data_e4_mff/e4_eta*.h5{' experiments/results/replications/' + CPU_RUN + '/e4_model_W9_skip_sym_s*.pt' if man.get('model_files') else ''} research/release/SHA256SUMS research/release/manifest.json research/release/catalog.json research/release/catalog.sqlite
```

To an object store instead, with the catalogue registered at the destination (`MILADY_DB_URL` set):

```bash
PYTHONPATH=src python3 -m milady.data.convert e4 experiments/data_e4 experiments/data_e4_mff --store s3://milady-data --catalog
```

Check after download:

```bash
sha256sum -c SHA256SUMS
```

```bash
PYTHONPATH=src python3 -m milady.data.convert validate --full e4_eta*.h5
```

The container is temporary: if it is reclaimed before the upload, the files are regenerated by `python3 experiments/e4_data.py
--jobs 4` (about 30 min of CPU) and `python -m milady.data.convert e4 experiments/data_e4 experiments/data_e4_mff` (2 min);
the checksums then differ (new identifiers and dates, and another draw on another processor type).
"""


def weights_section(man: dict) -> str:
    ws = man.get("model_files", [])
    job = f"```bash\n{JOB.format(run='e4_weights', groups='D')}\n```\n"
    if not ws:
        return ("The weights of W9 were not kept. One GPU job writes them (five seeds, about 30 min, under 1 USD at the prices of the pilot;\n"
                "not run, the pilot being closed to new jobs):\n\n" + job)
    rows = "\n".join(f"| `{w['path']}` | {w['seed']} | {w['size_bytes'] / 2**20:.1f} | `{w['sha256'][:16]}…` |" for w in ws)
    cmp_ = man.get("released_against_cited", {})
    lines = "\n".join(f"| {k} | {v['cited']} | {v['released']} |" for k, v in cmp_.items())
    return f"""**Weights.** The weights of the runs cited by the report were not kept (the GPU pods are deleted after each job). The files below are the
same model (W9: same code, seeds, iterations and width) **retrained on this data set on the CPU of the session**, with the evaluation
of the same pipeline against the reference statistics of this realisation (`experiments/results/replications/{CPU_RUN}/`). They are
another training on another draw of the data than the cited runs: their numbers are those of the table below, not those of the report.

| File (in the container, not in git) | seed | MiB | SHA-256 |
|---|---|---|---|
{rows}

| Held-out η, mean over the five seeds | W9 of the report (GPU pods) | W9 released (CPU, this data set) |
|---|---|---|
{lines}

The weights of the cited runs themselves can be written by one GPU job (five seeds, about 30 min, under 1 USD at the prices of the
pilot; not run, the pilot being closed to new jobs):

{job}"""


def reload_cmd(man: dict) -> str:
    ws = man.get("model_files", [])
    return "python3 experiments/e4_release_example.py --eta 0.04899 --n 256" + (f" --weights {ws[0]['path']}" if ws else "")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mff", default=str(ROOT / "experiments" / "data_e4_mff"))
    ap.add_argument("--npz", default=str(ROOT / "experiments" / "data_e4"))
    ap.add_argument("--out", default=str(ROOT / "research" / "release"))
    a = ap.parse_args()
    mff_dir, npz_dir, out = Path(a.mff), Path(a.npz), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    man = {"release": "e4-data-v1.0", "dataset": {"name": "e4_mhd3d", "version": "1.0", "format": "MFF 1.0"}, "note": NOTE,
           "data_files": data_files(mff_dir, npz_dir), "sample": sample(npz_dir, out)}
    export = catalogue(mff_dir, npz_dir, out)
    man["catalog"] = {"file": "catalog.sqlite", "export": "catalog.json", "simulations": len(export["simulations"]),
                      "dataset_files": len(export["dataset"]["files"]), "models": len(export["models"]),
                      "evaluations": sum(m["evaluations"] for m in export["models"])}
    man["models"] = [{k: m[k] for k in ("name", "variant", "run", "seed", "weights", "result_file")} for m in export["models"]]
    man["model_files"] = [{"file": Path(m["weights"]).name, "path": m["weights"], "seed": m["seed"], "size_bytes": m["weights_size_bytes"],
                           "sha256": m["weights_sha256"]} for m in export["models"] if m["law"] == "W9-released"]
    if man["model_files"]:
        ev = export["evaluation_summary"]

        def cell(law: str, metric: str) -> str:
            vals = [v["mean_over_seeds"] for k, v in ev[law].items() if k.startswith(metric + " @")]
            return ", ".join(f"{x:.3g}" for x in vals)

        man["released_against_cited"] = {name: {"cited": cell("W9", m), "released": cell("W9-released", m)} for name, m in (
            ("energy distance over the noise floor (η = 0.0331, 0.0490, 0.0725)", "ed_ratio"), ("relative error of the magnetic energy", "err_Eb_rel"),
            ("third-order part of the production over the dissipation", "prod_fluct_over_d"), ("residual of the energy balance", "balance_residual_total"),
            ("null-count error", "null_count_err_rel"), ("restart drift of the magnetic energy", "restart_drift_eb"))}
    (out / "README.md").write_text(readme(man), encoding="utf-8")
    small = [out / n for n in ("catalog.json", "catalog.sqlite", man["sample"]["file"])]
    man["release_files"] = [{"file": p.name, "size_bytes": p.stat().st_size, "sha256": mff.sha256_file(p)} for p in small]
    (out / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ([f"{f['sha256']}  {f['file']}" for f in man["data_files"]] + [f"{f['sha256']}  {f['file']}" for f in man["release_files"]]
             + [f"{f['sha256']}  {f['file']}" for f in man["model_files"]])
    (out / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"data_files": len(man["data_files"]), "all_valid": all(f["valid_full_scan"] for f in man["data_files"]),
                      "total_GiB": round(sum(f["size_bytes"] for f in man["data_files"]) / 2**30, 2), **man["catalog"],
                      "committed_MB": round(sum(p.stat().st_size for p in out.iterdir()) / 1e6, 2)}))


if __name__ == "__main__":
    main()
