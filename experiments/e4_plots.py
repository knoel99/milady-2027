"""Data plots of experiment E4 for the deliverables of team claude (SVG and PNG).

Reads only result files written by committed scripts: the main run in ``experiments/results``
(``e4_data.json``, ``e4_reference.json``, ``e4_floor.json``, ``e4_mhd3d_s<k>.json``), the runs of the long
trainings and of the width scan (``results/replications/e4_final_long``, ``e4_final_scan``), the convergence
check (``results/replications/e4_convergence``) and the GPU ledger ``research/compute-ledger.jsonl``.
A plot whose data are missing is skipped with a message.

    python3 e4_plots.py [--quick] [--out DIR]     # default DIR: site/teams/claude/plots

Every figure is written as ``<name>.svg`` and ``<name>.png``; ``plots.json`` lists them with the files they
come from (the report and the explorer quote these captions).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "site" / "assets"))
import figstyle as fs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from e4_digest import GENERATORS, R, load, per_seed  # noqa: E402

fs.use(font_size=9)
C, INK, INK2, LIGHT = fs.C, fs.INK, fs.INK2, fs.LIGHT
SPLIT_COL = {"train": "#009E73", "val": "#B39500", "test": "#8E3FA8"}
SPLIT_MARK = {"train": "o", "val": "s", "test": "D"}
LABEL = {
    "W0_free": "W0 free components", "W1_penalty": "W1 divergence penalty", "W2_final_projection": "W2 final projection",
    "W3_projected_flow": "W3 projected flow", "W4_potentials": "W4 potentials", "W4s_potentials_sym": "W4s potentials, B-sign equivariant",
    "W5_stationarity": "W5 stationarity loss", "W5_control": "W5 control", "W6_diffusion": "W6 diffusion",
    "W4c_potentials_smooth": "W4c smooth condition", "G0_gaussian_modes": "G0 Gaussian per mode (no network)",
    "W9_skip_sym": "W9 affine term", "W10_anchored": "W10 Gaussian anchor", "W11_anchored_skip": "W11 anchor + affine term",
    "W9L_skip_long": "W9L affine term, 8× iterations", "W11L_anchored_skip_long": "W11L anchor + affine, 8× iterations",
    "W7_tilting": "W7 tilting", "W8_rescaling": "W8 per-sample rescaling",
    "S_w512": "width 512", "S_w2048": "width 2048", "S_w5632": "width 5632", "S_w512_long": "width 512, 8× iterations",
    "S_w2048_long": "width 2048, 8× iterations",
}
WHERE = {"W0_free": "none", "W1_penalty": "loss", "W2_final_projection": "sampling", "W3_projected_flow": "sampling",
         "W4_potentials": "design", "W4s_potentials_sym": "design", "W5_stationarity": "loss", "W5_control": "design",
         "W6_diffusion": "family", "W4c_potentials_smooth": "design", "G0_gaussian_modes": "family",
         "W9_skip_sym": "design", "W10_anchored": "design", "W11_anchored_skip": "design",
         "W9L_skip_long": "design", "W11L_anchored_skip_long": "design"}
WHERE_COL = {"none": LIGHT, "design": C[0], "loss": C[1], "sampling": C[2], "family": C[6]}
MAIN = ["W0_free", "W1_penalty", "W2_final_projection", "W3_projected_flow", "W4_potentials", "W4s_potentials_sym",
        "W5_stationarity", "W6_diffusion", "W4c_potentials_smooth", "W9_skip_sym", "W10_anchored", "W11_anchored_skip",
        "G0_gaussian_modes"]
WRITTEN: list[dict] = []


def finish(fig, out: Path, name: str, caption: str, sources: list[str]) -> None:
    fig.savefig(out / f"{name}.svg")
    fig.savefig(out / f"{name}.png", dpi=200)
    plt.close(fig)
    WRITTEN.append({"name": name, "caption": caption, "sources": sources})
    print("written", out / f"{name}.svg")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


MIN_SEEDS = 5          # AGENTS.md rule 4: no mean ± SE quoted with fewer seeds


def mean_se(x: np.ndarray) -> tuple[float, float, int]:
    """Mean, standard error and number of the finite values of ``x`` (SE is NaN with fewer than two values)."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return np.nan, np.nan, 0
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else np.nan, len(x)


def seed_dots(ax, pos: float, x: np.ndarray, color: str, horizontal: bool = True) -> None:
    """One dot per seed at ``pos``; mean ± 2 SE in ink only with at least ``MIN_SEEDS`` seeds, otherwise the
    number of seeds is written next to the dots."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    m, se, n = mean_se(x)
    if not n:
        return
    p = np.full(n, pos)
    ax.scatter(*((x, p) if horizontal else (p, x)), s=14, color=color, alpha=0.6, zorder=2, linewidths=0)
    if n >= MIN_SEEDS:
        kw = dict(color=INK, capsize=2, zorder=3, lw=1)
        if horizontal:
            ax.errorbar(m, pos, xerr=2 * se, marker="|", ms=10, **kw)
        else:
            ax.errorbar(pos, m, yerr=2 * se, marker="_", ms=10, **kw)
    else:
        ax.annotate(f"n = {n}", (x.max(), pos) if horizontal else (pos, x.max()), xytext=(4, 0) if horizontal else (0, 4),
                    textcoords="offset points", fontsize=6.5, color=INK2, va="center" if horizontal else "bottom",
                    ha="left" if horizontal else "center")


def rows_of(runs: dict, variant: str, split: str) -> dict[float, list[dict]]:
    """Rows of ``variant`` grouped by η (one row per seed)."""
    out: dict[float, list[dict]] = {}
    for r in runs.values():
        for row in r["evaluation"].get(variant, {}).get(split, []):
            out.setdefault(row["eta"], []).append(row)
    return out


# ---------------------------------------------------------------------------------------------
def plot_data(out: Path, data: dict, ref: dict, tag: str) -> None:
    vals = data["values"]
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.9))
    for ax, key, lab in zip(axes, ("kinetic_energy", "magnetic_energy", "magnetic_helicity"),
                            (r"kinetic energy $E_u$", r"magnetic energy $E_B$", r"magnetic helicity $\langle A\cdot B\rangle$"),
                            strict=True):
        eta = np.array([v["eta"] for v in vals])
        m = np.array([v[key]["mean"] for v in vals])
        se = np.array([v[key]["sd_between_traj"] / np.sqrt(v["n_traj"]) for v in vals])
        ax.plot(eta, m, color=INK2, lw=1, zorder=1)
        for v, mi, si in zip(vals, m, se, strict=True):
            ax.errorbar(v["eta"], mi, yerr=2 * si, color=SPLIT_COL[v["split"]], marker=SPLIT_MARK[v["split"]], ms=5,
                        capsize=2, zorder=2)
        ax.set_xscale("log")
        ax.set_xlabel(r"magnetic diffusivity $\eta$")
        ax.set_title(lab)
        ax.set_xticks([0.03, 0.04, 0.05, 0.06, 0.08])
        ax.set_xticklabels(["0.03", "0.04", "0.05", "0.06", "0.08"])
    for s in ("train", "val", "test"):
        axes[0].plot([], [], color=SPLIT_COL[s], marker=SPLIT_MARK[s], ls="", label={"train": "training", "val": "validation", "test": "held-out test"}[s])
    axes[0].legend(fontsize=7.5)
    fig.tight_layout()
    finish(fig, out, "e4_data_trends", "Reference data of E4: kinetic energy, magnetic energy and magnetic helicity of the saturated "
           "dynamo against η (mean over 24 trajectories, bars: ± 2 standard errors), with the training, validation and held-out values.",
           [f"experiments/results/e4_data{tag}.json"])


def plot_helicity(out: Path, ref: dict, tag: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9))
    test = [(k, r) for k, r in sorted(ref["values"].items(), key=lambda t: -float(t[0])) if r["split"] == "test"]
    k = np.arange(1, 10)
    for i, (key, r) in enumerate(test):
        h = np.array(r["H_shell"])
        axes[0].plot(k[: len(h)], h, marker="o", ms=3.5, color=C[i], label=rf"$\eta$ = {float(key):.4f}")
        axes[1].plot(k[: len(h)], np.array(r["J_shell"]), marker="o", ms=3.5, color=C[i])
    for ax, lab in zip(axes, (r"magnetic helicity spectrum $H(k)$", r"current helicity spectrum $\langle j\cdot B\rangle(k)$"), strict=True):
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xlabel("shell k")
        ax.set_title(lab)
    axes[0].legend(fontsize=7.5)
    fig.tight_layout()
    finish(fig, out, "e4_helicity_spectrum", "Reference data: shell spectrum of the magnetic helicity and of the current helicity "
           "⟨j·B⟩ at the three held-out η. The mean of ⟨j·B⟩ is zero (stationarity identity): the negative shells k ≤ 2 cancel "
           "the positive shells k ≥ 3.", [f"experiments/results/e4_reference{tag}.json"])


def plot_ed(out: Path, runs: dict, tag: str) -> None:
    names = [v for v in MAIN if not np.all(np.isnan(per_seed(runs, v, "ed_ratio")))]
    fig, ax = plt.subplots(figsize=(7.4, 0.33 * len(names) + 1.2))
    for i, v in enumerate(names):
        xt = per_seed(runs, v, "ed_ratio", "train")
        seed_dots(ax, i, per_seed(runs, v, "ed_ratio"), WHERE_COL[WHERE.get(v, "design")])
        ax.scatter(np.nanmean(xt), i, s=26, facecolors="none", edgecolors=INK2, zorder=3)
    ax.axvline(1, color=INK2, lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels([LABEL.get(v, v) for v in names])
    ax.invert_yaxis()
    ax.set_xlabel("energy distance to the reference / noise floor (held-out η)")
    for w, lab in (("design", "model design"), ("loss", "training loss"), ("sampling", "sampling procedure"), ("family", "model family"),
                   ("none", "no constraint")):
        ax.scatter([], [], s=14, color=WHERE_COL[w], label=lab)
    ax.scatter([], [], s=26, facecolors="none", edgecolors=INK2, label="seed mean at the training η")
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    finish(fig, out, "e4_ed_ratio", "Energy distance to the reference divided by the noise floor on the held-out η, per variant: "
           "one dot per seed, bar: seed mean ± 2 standard errors (drawn with at least 5 seeds), open circle: seed mean at the training η. "
           "Dashed line: the floor.",
           [f"experiments/results/e4_mhd3d{tag}_s<k>.json"])


def plot_spectra(out: Path, runs: dict, ref: dict, tag: str) -> None:
    show = [v for v in ("W0_free", "W4s_potentials_sym", "W9_skip_sym", "W11_anchored_skip", "G0_gaussian_modes")
            if rows_of(runs, v, "test")]
    etas = sorted({e for v in show for e in rows_of(runs, v, "test")}, reverse=True)
    if not show or not etas or "spec_b" not in next(iter(rows_of(runs, show[0], "test").values()))[0]:
        print("skip e4_spectra: no shell spectra in the result rows")
        return
    eta = etas[len(etas) // 2]
    r = ref["values"][f"{eta:.5f}"]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.0))
    k = np.arange(1, 10)
    for ax, key, lab in zip(axes, ("spec_u", "spec_b", "H_shell"), (r"$E_u(k)$", r"$E_B(k)$", r"$H(k)$"), strict=True):
        ax.plot(k, r[key], color=INK, lw=2.4, label="reference", zorder=5)
        for i, v in enumerate(show):
            rows = rows_of(runs, v, "test")[eta]
            ax.plot(k, np.mean([x[key] for x in rows], axis=0), color=C[i], lw=1.4, marker="o", ms=2.5, label=LABEL[v])
        if key != "H_shell":
            ax.set_yscale("log")
        else:
            ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xlabel("shell k")
        ax.set_title(lab)
    axes[0].legend(fontsize=6.8)
    fig.suptitle(rf"held-out $\eta$ = {eta:.4f}, mean over the seeds", fontsize=9)
    fig.tight_layout()
    finish(fig, out, "e4_spectra", f"Shell spectra of the velocity and of the magnetic field and magnetic helicity spectrum at the "
           f"held-out η = {eta:.4f}: reference (black) and generated ensembles (mean over the seeds).",
           [f"experiments/results/e4_mhd3d{tag}_s<k>.json", f"experiments/results/e4_reference{tag}.json"])


def plot_tradeoff(out: Path, runs: dict, ref: dict, tag: str) -> None:
    names = [v for v in MAIN if not np.all(np.isnan(per_seed(runs, v, "ed_ratio")))]
    keys = [("balance_residual_total", "|energy balance residual|", True, True), ("null_count_err_rel", "relative error on the null count", True, False),
            ("restart_drift_eb", r"restart drift of $E_B$", True, True), ("hel_m_err_rel", "relative error on the magnetic helicity", True, True)]
    fig, axes = plt.subplots(1, 4, figsize=(12.5, 0.3 * len(names) + 1.3), sharey=True)
    t = [r for r in ref["values"].values() if r["split"] == "test"]
    floors = {"balance_residual_total": np.mean([abs(r["balance_residual_total"]) for r in t]),
              "restart_drift_eb": np.mean([r.get("restart_drift_eb", np.nan) for r in t])}
    for ax, (key, lab, absolute, log) in zip(axes, keys, strict=True):
        for i, v in enumerate(names):
            seed_dots(ax, i, per_seed(runs, v, key, absolute=absolute), WHERE_COL[WHERE.get(v, "design")])
        if key in floors and np.isfinite(floors[key]):
            ax.axvline(floors[key], color=INK, lw=0.9, ls="--")
        if log:
            ax.set_xscale("log")
        else:
            ax.set_xlim(left=0)
        ax.set_title(lab, fontsize=8.5)
    axes[0].set_yticks(range(len(names)))
    axes[0].set_yticklabels([LABEL.get(v, v) for v in names])
    axes[0].invert_yaxis()
    fig.tight_layout()
    finish(fig, out, "e4_physics_metrics", "Physical metrics on the held-out η, one dot per seed and seed mean ± 2 standard errors: residual of the mean "
           "energy balance, error on the number of magnetic null points, drift of the magnetic energy when the solver restarts from "
           "the generated snapshots, error on the mean magnetic helicity. Dashed lines: the same quantity on reference snapshots.",
           [f"experiments/results/e4_mhd3d{tag}_s<k>.json", f"experiments/results/e4_reference{tag}.json"])


def plot_per_eta(out: Path, runs: dict, data: dict, tag: str) -> None:
    show = [v for v in ("W4_potentials", "W4c_potentials_smooth", "W6_diffusion", "W9_skip_sym", "G0_gaussian_modes")
            if rows_of(runs, v, "test")]
    if not show:
        return
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    split = {v["eta"]: v["split"] for v in data["values"]}
    for i, v in enumerate(show):
        pts = {}
        for s in ("train", "val", "test"):
            for eta, rows in rows_of(runs, v, s).items():
                pts[eta] = np.mean([x["ed_ratio"] for x in rows])
        etas = sorted(pts, reverse=True)
        ax.plot(etas, [pts[e] for e in etas], color=C[i], lw=1.2, label=LABEL[v], zorder=1)
        for e in etas:
            ax.scatter(e, pts[e], color=C[i], marker=SPLIT_MARK[split[e]], s=22, zorder=2,
                       facecolors=C[i] if split[e] == "train" else "white")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([0.03, 0.04, 0.05, 0.06, 0.08])
    ax.set_xticklabels(["0.03", "0.04", "0.05", "0.06", "0.08"])
    ax.set_xlabel(r"magnetic diffusivity $\eta$")
    ax.set_ylabel("energy distance / floor")
    for sp, lab in (("train", "training η"), ("val", "validation η"), ("test", "held-out η")):
        ax.scatter([], [], color=INK2, marker=SPLIT_MARK[sp], s=22, facecolors=INK2 if sp == "train" else "white", label=lab)
    ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.tight_layout()
    finish(fig, out, "e4_per_eta", "Energy-distance ratio against η, seed mean: at the training values (filled circles) and between "
           "them (open squares: validation, open diamonds: held-out test). The gap between the two shows how each model interpolates in η.",
           [f"experiments/results/e4_mhd3d{tag}_s<k>.json"])


def plot_nulls(out: Path, runs: dict, ref: dict, tag: str) -> None:
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    xs, ys = [], []
    for v in GENERATORS:                       # the list of the digest's fit of H13
        px, py = [], []
        for r in runs.values():
            for row in r["evaluation"].get(v, {}).get("test", []):
                rr = ref["values"][f"{row['eta']:.5f}"]
                if "null_count" in row and row["null_count"] > 0:
                    px.append(np.log(row["k_lambda"] / rr["k_lambda"]))
                    py.append(np.log(row["null_count"] / rr["null_count_mean"]))
        if px:
            ax.scatter(px, py, s=9, color=WHERE_COL[WHERE.get(v, "design")], alpha=0.6)
            xs += px
            ys += py
    if len(xs) < 3:
        plt.close(fig)
        return
    slope, icpt = np.polyfit(xs, ys, 1)
    xx = np.linspace(min(xs), max(xs), 20)
    ax.plot(xx, slope * xx + icpt, color=INK, lw=1.2, label=f"least squares over {len(xs)} points: slope {slope:.2f}")
    ax.plot(xx, 3 * xx, color=INK2, lw=1, ls="--", label="slope 3 (Gaussian estimate)")
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.axvline(0, color=LIGHT, lw=0.8)
    ax.set_xlabel(r"$\ln\,(k_\lambda^{\rm gen} / k_\lambda^{\rm ref})$")
    ax.set_ylabel(r"$\ln\,(N^{\rm gen} / N^{\rm ref})$")
    ax.legend(fontsize=7.5)
    fig.tight_layout()
    finish(fig, out, "e4_nulls_klambda", "Number of magnetic null points against the magnetic Taylor wavenumber k_λ = (⟨|j|²⟩/⟨|B|²⟩)^½, "
           "generated over reference, one point per variant, held-out η and seed; the fit is the one of the digest (hypothesis H13).",
           [f"experiments/results/e4_mhd3d{tag}_s<k>.json", f"experiments/results/e4_reference{tag}.json"])


def plot_floors(out: Path, floors: dict, ref: dict) -> None:
    keys = sorted(floors, key=lambda k: -float(k))
    eta = np.array([float(k) for k in keys])
    a = np.array([floors[k]["traj_split_512"]["mean_first_10"] for k in keys])      # the 10 splits of the ratio's floor
    b = np.array([floors[k]["random_split_512"]["mean"] for k in keys])
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    lo = np.array([floors[k]["traj_split_512"]["min"] for k in keys])
    hi = np.array([floors[k]["traj_split_512"]["max"] for k in keys])
    ax.errorbar(eta, a, yerr=[a - lo, hi - a], color=C[0], marker="o", ms=4, capsize=2,
                label="two halves of the trajectories: mean of the 10 splits used for the ratio")
    ax.plot(eta, b, color=C[1], marker="s", ms=4, label="random split of the snapshots")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([0.03, 0.04, 0.05, 0.06, 0.08])
    ax.set_xticklabels(["0.03", "0.04", "0.05", "0.06", "0.08"])
    ax.set_xlabel(r"magnetic diffusivity $\eta$")
    ax.set_ylabel("energy distance between two\nreference subsamples (n = 512)")
    ax.legend(fontsize=7.5)
    fig.tight_layout()
    finish(fig, out, "e4_floors", "Noise floors of the energy distance on the reference data: between two subsamples from disjoint "
           "halves of the 24 trajectories (mean of the 10 splits that define the floor of the ratio; bars: smallest and largest of "
           "20 splits) and between two random subsamples.",
           ["experiments/results/e4_floor.json"])


def plot_convergence(out: Path) -> None:
    root = R / "replications" / "e4_convergence"
    base = read(R / "e4_data.json")
    files = [("16³ (E4 data)", None, C[0]), ("16³, same hardware", "e4_data_n16_same_hardware.json", C[3]),
             ("16³, half time step", "e4_data_cfl0.75.json", C[1]), ("24³", "e4_data_n24.json", C[2]), ("32³", "e4_data_n32.json", C[6])]
    if base is None or not (root / "e4_data_n24.json").exists():
        print("skip e4_convergence")
        return
    etas = [v["eta"] for v in read(root / "e4_data_n24.json")["values"] if v["split"] == "test" and v.get("shells")]
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 2.9))
    seen: set[str] = set()
    for j, (lab, fn, col) in enumerate(files):
        d = base if fn is None else read(root / fn)
        if d is None:
            continue
        for ax, key in zip(axes, ("kinetic_energy", "magnetic_energy", "magnetic_helicity"), strict=True):
            for i, eta in enumerate(etas):
                v = next((x for x in d["values"] if x["eta"] == eta and (fn is None or x.get("shells"))), None)
                if v is None:
                    continue
                se = v[key]["sd_between_traj"] / np.sqrt(v["n_traj"])
                ax.errorbar(i + 0.14 * (j - 2), v[key]["mean"], yerr=2 * se, color=col, marker="o", ms=4, capsize=2,
                            label=lab if (lab not in seen and key == "kinetic_energy") else None)
                seen.add(lab)
    for ax, lab in zip(axes, (r"$E_u$", r"$E_B$", r"$\langle A\cdot B\rangle$"), strict=True):
        ax.set_xticks(range(len(etas)))
        ax.set_xticklabels([f"{e:.4f}" for e in etas])
        ax.set_xlabel(r"held-out $\eta$")
        ax.set_title(lab)
    axes[0].legend(fontsize=6.8)
    fig.tight_layout()
    finish(fig, out, "e4_convergence", "Convergence of the reference data: energies and magnetic helicity at the three held-out η for "
           "the 16³ grid of E4, the same grid recomputed on the hardware of the check, half its time step, 24³ and 32³ (one η); bars: ± 2 standard errors over 24 trajectories.",
           ["experiments/results/e4_data.json", "experiments/results/replications/e4_convergence/*.json"])


def plot_scan(out: Path, tag: str) -> None:
    runs = load(bool(tag), R if tag else R / "replications" / "e4_final_scan")
    names = [v for v in ("S_w512", "S_w2048", "S_w5632", "S_w512_long", "S_w2048_long", "W9_skip_sym", "G0_gaussian_modes")
             if runs and not np.all(np.isnan(per_seed(runs, v, "ed_ratio")))]
    if not names or not names[0].startswith("S_"):
        print("skip e4_width_scan")
        return
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0))
    for i, v in enumerate(names):
        col = C[0] if v.startswith("S_") else (C[6] if v.startswith("G0") else C[2])
        seed_dots(axes[0], i, per_seed(runs, v, "ed_ratio"), col, horizontal=False)
        loss = [r["times"].get(v, {}).get("fm_loss_train_sample") for r in runs.values()]
        seed_dots(axes[1], i, np.array([x for x in loss if x is not None], dtype=float), col, horizontal=False)
    for ax in axes:
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([LABEL.get(v, v).replace(", ", "\n") for v in names], fontsize=6.5, rotation=20)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("energy distance / floor (held-out η)")
    axes[1].axhline(np.pi / 2, color=INK, lw=0.9, ls="--")
    axes[1].set_ylabel("flow-matching loss on a training sample")
    fig.tight_layout()
    finish(fig, out, "e4_width_scan", "Width scan (hypothesis H21): energy-distance ratio and flow-matching loss of the equivariant "
           "potentials model without affine term for three widths and two budgets, against the model with the explicit affine term "
           "and the Gaussian baseline. Dashed line: π/2, the loss of the exact field for independent unit Gaussian coordinates.",
           ["experiments/results/replications/e4_final_scan/e4_mhd3d_s<k>.json"])


def plot_long(out: Path, tag: str) -> None:
    runs = load(bool(tag), R if tag else R / "replications" / "e4_final_long")
    names = [v for v in ("G0_gaussian_modes", "W9_skip_sym", "W9L_skip_long", "W10_anchored", "W11_anchored_skip",
                         "W11L_anchored_skip_long") if runs and not np.all(np.isnan(per_seed(runs, v, "ed_ratio")))]
    if "W9L_skip_long" not in names:
        print("skip e4_long_trainings")
        return
    keys = [("ed_ratio", "energy distance / floor", False), ("balance_residual_total", "|energy residual|", True),
            ("null_count_err_rel", "error on the null count", True), ("restart_drift_eb", r"restart drift of $E_B$", True)]
    fig, axes = plt.subplots(1, 4, figsize=(12, 2.9))
    for ax, (key, lab, absolute) in zip(axes, keys, strict=True):
        for i, v in enumerate(names):
            seed_dots(ax, i, per_seed(runs, v, key, absolute=absolute),
                      C[6] if v.startswith("G0") else (C[1] if v.endswith("_long") else C[0]), horizontal=False)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([v.split("_")[0] for v in names], fontsize=7.5)
        ax.set_title(lab, fontsize=8.5)
        ax.set_yscale("log")
    fig.tight_layout()
    finish(fig, out, "e4_long_trainings", "Gaussian baseline (violet), flow matching with the explicit affine term or the Gaussian anchor "
           "at the base budget (blue) and with 8 times the iterations (orange), on the held-out η: one dot per seed, seed mean ± 2 standard errors.",
           ["experiments/results/replications/e4_final_long/e4_mhd3d_s<k>.json"])


def plot_costs(out: Path) -> None:
    led = HERE.parent / "research" / "compute-ledger.jsonl"
    if not led.exists():
        return
    rows = [json.loads(x) for x in led.read_text().splitlines() if x.strip()]
    rows = [r for r in rows if r.get("event") != "start"]
    usd = np.cumsum([r["usd"] for r in rows])
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    ax.step(range(1, len(rows) + 1), usd, where="post", color=C[0])
    for i, r in enumerate(rows):
        ok = r.get("rc") == 0
        ax.scatter(i + 1, usd[i], s=16, color=C[2] if ok else (C[7] if r["usd"] >= 0 else INK2), zorder=3)
    ax.scatter([], [], s=16, color=C[2], label="job finished (rc = 0)")
    ax.scatter([], [], s=16, color=C[7], label="job failed, interrupted or lost")
    ax.scatter([], [], s=16, color=INK2, label="ledger correction")
    ax.set_xticks(range(1, len(rows) + 1, 2))
    ax.set_xlabel("ledger entry (chronological)")
    ax.set_ylabel("cumulative GPU spend (USD)")
    ax.legend(fontsize=7.5)
    fig.tight_layout()
    finish(fig, out, "e4_gpu_costs", "Cumulative GPU spend of the pilot, one point per entry of the compute ledger: finished jobs, "
           "jobs that failed, were interrupted or were lost, and the corrections made after another session deleted running pods.",
           ["research/compute-ledger.jsonl"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true", help="read the --quick result files (development)")
    ap.add_argument("--out", type=Path, default=HERE.parent / "site" / "teams" / "claude" / "plots")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    tag = "_quick" if a.quick else ""
    data, ref, floors = read(R / f"e4_data{tag}.json"), read(R / f"e4_reference{tag}.json"), read(R / "e4_floor.json")
    runs = load(a.quick)
    if data and ref:
        plot_data(a.out, data, ref, tag)
        plot_helicity(a.out, ref, tag)
    if runs and ref and data:
        plot_ed(a.out, runs, tag)
        plot_spectra(a.out, runs, ref, tag)
        plot_tradeoff(a.out, runs, ref, tag)
        plot_per_eta(a.out, runs, data, tag)
        plot_nulls(a.out, runs, ref, tag)
    if floors and ref:
        plot_floors(a.out, floors["values"], ref)
    plot_convergence(a.out)
    plot_scan(a.out, tag)
    plot_long(a.out, tag)
    plot_costs(a.out)
    (a.out / "plots.json").write_text(json.dumps(WRITTEN, indent=1), encoding="utf-8")
    print(len(WRITTEN), "plots")


if __name__ == "__main__":
    main()
