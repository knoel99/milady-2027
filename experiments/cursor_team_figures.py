"""Write the cursor team's schematic panels and data plots from result files."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
TEAM = ROOT / "site" / "teams" / "cursor"
RESULTS = ROOT / "experiments" / "results"


def _load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def _panel(path: Path, title: str, draw) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    draw(ax)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".svg"))
    fig.savefig(path.with_suffix(".pdf"))
    plt.close(fig)


def _schematic(name: str, title: str, brief: str, draw) -> None:
    base = TEAM / "figures" / name
    out = base / "figure" / "out" / name
    _panel(out, title, draw)
    (base / "figure").mkdir(parents=True, exist_ok=True)
    (base / "figure" / "figure.js").write_text(
        "export const figure = {\n"
        f"  name: {name!r},\n"
        "  width: 160,\n"
        "  height: 90,\n"
        f"  title: {title!r},\n"
        "};\n",
        encoding="utf-8",
    )
    (base / "docs").mkdir(parents=True, exist_ok=True)
    (base / "docs" / "brief.md").write_text(brief + "\n", encoding="utf-8")


def main() -> None:
    cmp_ = _load("cursor_constraint_cmp.json")
    ceiling = _load("cursor_constraint_ceiling.json")
    mid = _load("cursor_constraint_midpoint_kmax6.json")
    stat = _load("cursor_stationary.json")
    nulls = _load("cursor_nulls.json")
    seeds = [row["seed"] for row in cmp_["seeds"]]

    def div(ax):
        ax.plot(seeds, [row["projected"]["div_max"] for row in cmp_["seeds"]], "o-", label="sampling constraint")
        ax.plot(seeds, [row["free"]["div_max"] for row in cmp_["seeds"]], "s-", label="unconstrained")
        ax.set_yscale("log")
        ax.set_xlabel("seed")
        ax.set_ylabel("max relative divergence")
        ax.legend()

    def ratios(ax):
        ax.bar([s - 0.15 for s in seeds], [row["projected"]["c1"] for row in cmp_["seeds"]], width=0.3, label="projected")
        ax.bar([s + 0.15 for s in seeds], [row["free"]["c1"] for row in cmp_["seeds"]], width=0.3, label="free")
        ax.set_xlabel("seed")
        ax.set_ylabel("energy-distance ratio")
        ax.legend()

    def ceil(ax):
        for key in ("kmax4", "kmax6", "kmax7"):
            ax.plot([row["seed"] for row in ceiling["seeds"]], [row[key]["c1"] for row in ceiling["seeds"]], "o-", label=key)
        ax.set_yscale("log")
        ax.axhline(1.2, color="black", linewidth=0.8)
        ax.set_xlabel("seed")
        ax.set_ylabel("perfect-cutoff ratio")
        ax.legend()

    def midpoint(ax):
        ax.plot([row["seed"] for row in mid["seeds"]], [row["midpoint"]["c1"] for row in mid["seeds"]], "o-")
        ax.axhline(1.2, color="black", linewidth=0.8)
        ax.set_xlabel("seed")
        ax.set_ylabel("kmax=6 midpoint ratio")

    def balance(ax):
        ax.plot([row["seed"] for row in stat["seeds"]], [abs(row["second"]["total"]) for row in stat["seeds"]], "o-", label="total")
        ax.plot([row["seed"] for row in stat["seeds"]], [abs(row["second"]["magnetic"]) for row in stat["seeds"]], "s-", label="magnetic")
        ax.set_yscale("log")
        ax.axhline(0.05, color="black", linewidth=0.8)
        ax.set_xlabel("seed")
        ax.set_ylabel("absolute second-half residual")
        ax.legend()

    def null_counts(ax):
        ax.plot([row["seed"] for row in nulls["seeds"]], [row["n_full"] for row in nulls["seeds"]], "o-", label="full field")
        ax.plot([row["seed"] for row in nulls["seeds"]], [row["n_trunc"] for row in nulls["seeds"]], "s-", label="kmax=4")
        ax.set_xlabel("seed")
        ax.set_ylabel("trilinear null count")
        ax.legend()

    def c4(ax):
        ax.plot([row["seed"] for row in mid["seeds"]], [row["midpoint"]["c4"] for row in mid["seeds"]], "o-")
        ax.axhline(0.1, color="black", linewidth=0.8)
        ax.set_xlabel("seed")
        ax.set_ylabel("C4 of the kmax=6 midpoint")

    def errors(ax):
        ax.bar([row["seed"] for row in nulls["seeds"]], [row["relative_error"] for row in nulls["seeds"]])
        ax.axhline(0.1, color="black", linewidth=0.8)
        ax.set_xlabel("seed")
        ax.set_ylabel("relative null-count error")

    plots = {
        "divergence": ("Sampling constraint against the free baseline", div),
        "flow-ratios": ("Energy-distance ratios of the two flows", ratios),
        "ceiling": ("Perfect cutoff ratio against kmax", ceil),
        "midpoint": ("kmax=6 midpoint ratio by seed", midpoint),
        "balance": ("Dynamic second-half energy balance", balance),
        "nulls": ("Trilinear null counts, full field and truncation", null_counts),
        "spectra-helicity": ("Spectrum plus helicity error of the midpoint", c4),
        "null-error": ("Relative null-count error of the truncation", errors),
    }
    plot_dir = TEAM / "plots"
    for name, (title, draw) in plots.items():
        _panel(plot_dir / name, title, draw)

    briefs = {
        "dynamo-threshold": ("Kinematic ABC signs are seed dependent", "The panel marks the open n=128 seeds 0-4 bracket. Measured lambdas are in the race report."),
        "constraint-mechanisms": ("Two mechanisms on one glyph", "Sampling projection removes the longitudinal Fourier part. The free model does not."),
        "metrics-panel": ("What C1 to C5 measure", "Energy distance, divergence, balance, spectrum plus helicity, and the trilinear null count."),
        "protocol-panel": ("Held-out Rm and five seeds", "Training values stay off Rm=12. Every quoted comparison uses seeds 0-4."),
        "balance-panel": ("Total balance against the magnetic residual", "The total residual of the dynamic run is far under 0.05. The magnetic residual is not."),
        "null-panel": ("A truncation moves the null count", "Full and kmax=4 counts come from experiments/results/cursor_nulls.json."),
        "compute-path": ("Session, pod, result file", "GPU jobs are named milady-cursor-job-* and land in the compute ledger."),
        "pipeline-panel": ("Field, coefficients, comparison", "The quoted generator is a linear midpoint in Fourier coefficients, not a trained flow."),
    }
    drawers = [div, ratios, ceil, midpoint, balance, null_counts, errors, c4]
    for (name, (title, brief)), draw in zip(briefs.items(), drawers, strict=True):
        _schematic(name, title, f"{brief} Title: {title}.", draw)
    print("wrote", len(plots), "plots and", len(briefs), "schematics")


if __name__ == "__main__":
    main()
