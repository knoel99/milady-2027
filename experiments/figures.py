"""Result plots (matplotlib).

Usage: python3 figures.py [e1] [e2] [e3] [--quick]
Outputs (in site/experiments/figures/): <name>.png and <name>.svg.
Reference categorical palette (fixed order); the "ground truth" reference is drawn in neutral ink.
"""
from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import FIGS, RESULTS  # noqa: E402

sys.path.insert(0, str(FIGS.parents[1] / "assets"))
from figstyle import C, INK, INK2, LIGHT  # noqa: E402  shared palette (site/assets/figstyle.py)
from figstyle import GRID_LIGHT as GRID  # noqa: E402
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 2,
    "savefig.facecolor": "white", "figure.facecolor": "white",
})

TXT = {
    "sim": "simulation (counting)", "rice_ref": "Rice, reference distribution", "rice_C": "Rice, generated distribution (C)",
    "rice_F": "Rice, generated distribution (F)", "gtrain": "training Γ", "rate": "zero crossings of D per unit time",
    "ref": "reference", "genC": "generated distribution (C)", "genF": "generated distribution (F)",
    "ed": "energy distance", "liou3": "Liouville residual (degree 3)", "asym": "|P(D>0) − 1/2|", "mc": " MC noise",
    "sig": "σ(dE/dt) / σ_ref", "one": " reference distribution",
    "density": "density", "projC": "C projected on dE/dt = 0", "genCshort": "C (generated)",
    "var": {"A_reference": "A baseline", "B_augmentation": "B augmentation", "C_equivariant": "C equivariant",
            "C_short": "C short budget", "F_stationarity_Cshort": "C short + stat. loss",
            "F0_control_Cshort": "C short + control", "F_stationarity_C": "C + stat. loss", "F0_control_C": "C + control",
            "D_tilting_C": "C + tilting", "E_projection_C": "C + per-sample proj."},
    "e2var": {"V0_free": "V0 free", "V1_penalty": "V1 penalty", "V2_final_projection": "V2 final projection",
              "V3_projected_flow": "V3 projected flow", "V4_potentials": "V4 potentials",
              "V5_potentials_stat": "V5 potentials + stat. loss", "V5_control": "V5 control",
              "reference_subsample": "data (subsample)"},
    "div": "relative divergence of u", "spec": "spectrum error (log₁₀, mean)",
    "bal": "|E[D] − ε_inj| / ε_inj", "k": "wavenumber k", "Eu": "E_u(k)", "Eb": "E_B(k)",
    "diss": "dissipation D(x) / ε_inj", "base": "V4 (generated)", "tilt": "V4 + tilting", "resc": "V4 + per-sample rescaling",
    "rm": "Rm = 1/η", "lam": "growth rate λ",
}


def finish(fig, name):
    fig.tight_layout()
    fig.savefig(FIGS / f"{name}.png", dpi=200)
    fig.savefig(FIGS / f"{name}.svg")
    plt.close(fig)
    print("written", FIGS / f"{name}.png")


def load(name):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
def e1(suffix=""):
    t = TXT
    r = load(f"e1_gissinger{suffix}.json")
    fine = r["fine_grid"]
    g = np.array([f["Gamma"] for f in fine])
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.3))
    ax[0].plot(g, [f["simulation_rate"] for f in fine], color=INK, lw=2.4, label=t["sim"])
    ax[0].plot(g, [f["rice_rate_ref"] for f in fine], color=INK2, ls="--", lw=1.4, label=t["rice_ref"])
    ax[0].plot(g, [f["rice_rate_model"] for f in fine], color=C[0], label=t["rice_C"])
    if "rice_rate_model_F" in fine[0]:
        ax[0].plot(g, [f["rice_rate_model_F"] for f in fine], color=C[1], label=t["rice_F"])
    tr = [f["Gamma"] for f in fine if f["in_training"]]
    ax[0].plot(tr, np.zeros(len(tr)), "|", color=INK2, ms=9, mew=1.5, label=t["gtrain"])
    ax[0].set_xlabel("Γ"); ax[0].set_ylabel(t["rate"])
    ax[0].legend(fontsize=7.5, loc="upper left")
    ax[1].plot(g, [f["bridge_ref"] for f in fine], color=INK, lw=2.4, label=t["ref"])
    ax[1].plot(g, [f["bridge_model"] for f in fine], color=C[0], label=t["genC"])
    if "bridge_model_F" in fine[0]:
        ax[1].plot(g, [f["bridge_model_F"] for f in fine], color=C[1], label=t["genF"])
    ax[1].set_xlabel("Γ"); ax[1].set_ylabel("P(|D| < 0.25)")
    ax[1].legend(fontsize=7.5, loc="upper left")
    finish(fig, f"e1_threshold{suffix}")

    res = r["summary"]
    keys = ["A_reference", "B_augmentation", "C_equivariant", "C_short", "F_stationarity_Cshort", "F0_control_Cshort",
            "F_stationarity_C", "F0_control_C", "D_tilting_C", "E_projection_C"]
    keys = [k for k in keys if k in res]
    from matplotlib.ticker import FuncFormatter, NullFormatter
    fig, ax = plt.subplots(1, 4, figsize=(12.4, 3.9), sharey=True)
    y = np.arange(len(keys))[::-1]
    sig_ref = res["reference"]["dEdt_std"]
    for j, (key, lab, floor_key) in enumerate((("energy", t["ed"], "energy"), ("liou_test_mean", t["liou3"], "liou_test_mean"),
                                               ("asym", t["asym"], "asym"), ("dEdt_std", t["sig"], "one"))):
        vals = [res[k]["test"][key] / (sig_ref if key == "dEdt_std" else 1.0) for k in keys]
        ax[j].barh(y, vals, color=C[0], height=0.62)
        if floor_key:
            if floor_key == "one":
                fl = 1.0
            elif floor_key == "asym":  # E|p̂ − 1/2| for an exactly symmetric law: √(2/π) · ½ / √n
                fl = np.sqrt(2 / np.pi) * 0.5 / np.sqrt(r["config"]["n_gen"])
            else:
                fl = res["mc_noise_floors"]["n_gen"][floor_key]
            ax[j].axvline(fl, color=INK2, ls="--", lw=1)
            ax[j].text(fl, len(keys) - 0.45, t[floor_key if floor_key == "one" else "mc"], color=INK2, fontsize=7, va="bottom")
        ax[j].set_xscale("log"); ax[j].set_xlabel(lab)
        ax[j].xaxis.set_minor_formatter(NullFormatter())
        if key in ("asym", "dEdt_std"):  # readable ticks (few decades)
            ticks = [0.003, 0.01, 0.03] if key == "asym" else [0.3, 1, 3, 10]
            ax[j].set_xticks(ticks)
            ax[j].xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        if key == "dEdt_std":  # per-sample projection cancels dE/dt: bar off scale, annotated
            ax[j].set_xlim(0.2, 30)
            for yy, v in zip(y, vals):
                if v < 0.2:
                    ax[j].text(0.22, yy, "≈ 0 (exact)", va="center", fontsize=7.5, color=INK2)
    ax[0].set_yticks(y); ax[0].set_yticklabels([t["var"][k] for k in keys])
    for a in ax:
        a._categ = True
    finish(fig, f"e1_variants{suffix}")

    d = np.load(RESULTS / f"e1_samples{suffix}.npz")
    from e1_gissinger import dEdt
    gam, gam2 = "0.85", "0.93"
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.3))
    bins = np.linspace(-1.5, 1.5, 80)
    for key, col, lab in (("ref", INK, t["ref"]), ("C_equivariant", C[0], t["genCshort"]), ("E_projection_C", C[1], t["projC"])):
        x = d[f"{key}|{gam2}"]
        ax[0].hist(dEdt(x, float(gam2)), bins=bins, density=True, histtype="step", color=col, lw=1.6, label=lab)
    ax[0].set_xlabel(f"dE/dt  (Γ = {gam2})"); ax[0].set_ylabel(t["density"]); ax[0].legend(fontsize=7)
    ax[0].set_yscale("log")
    for j, key in enumerate(("A_reference", "C_equivariant")):
        ref, x = d[f"ref|{gam}"], d[f"{key}|{gam}"]
        ax[j + 1].scatter(ref[:3000, 0], ref[:3000, 1], s=1, color=LIGHT, rasterized=True)
        ax[j + 1].scatter(x[:3000, 0], x[:3000, 1], s=1, color=C[0], rasterized=True)
        ax[j + 1].set_xlabel("Q"); ax[j + 1].set_ylabel("D")
        p = f"{(x[:, 1] > 0).mean():.2f}"
        ax[j + 1].set_title(f"{t['var'][key]}, Γ = {gam}: P(D>0) = {p}", fontsize=8.5)
    finish(fig, f"e1_symmetry_projection{suffix}")


# ---------------------------------------------------------------------------
def e2(suffix=""):
    t = TXT
    r = load(f"e2_mhd2d{suffix}.json")
    res = r["summary"]
    keys = [k for k in ("V0_free", "V1_penalty", "V2_final_projection", "V3_projected_flow", "V4_potentials",
                        "V5_potentials_stat", "V5_control", "reference_subsample") if k in res]
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.6), sharey=True)
    y = np.arange(len(keys))[::-1]
    for j, (key, lab) in enumerate((("div_rel_u", t["div"]), ("spectrum_error_log10", t["spec"]), ("balance_residual_energy", t["bal"]))):
        vals = np.array([max(res[k]["test"][key], 1e-17) for k in keys])
        cols = [INK2 if k == "reference_subsample" else C[0] for k in keys]
        ax[j].barh(y, vals, color=cols, height=0.62)
        ax[j].set_xscale("log"); ax[j].set_xlabel(lab, fontsize=8)
    ax[0].set_yticks(y); ax[0].set_yticklabels([t["e2var"][k] for k in keys])
    for a in ax:
        a._categ = True
    finish(fig, f"e2_mechanisms{suffix}")

    # mean spectra at one test η
    d = np.load(RESULTS / f"e2_samples{suffix}.npz")
    kx, ky = d["kx"], d["ky"]
    shell = np.rint(np.sqrt(kx ** 2 + ky ** 2)).astype(int)

    def spectra(c):
        su = [(0.5 * (np.abs(c[:, 0]) ** 2 + np.abs(c[:, 1]) ** 2) * (shell == s)).sum(-1).mean() for s in range(1, 14)]
        sb = [(0.5 * (np.abs(c[:, 2]) ** 2 + np.abs(c[:, 3]) ** 2) * (shell == s)).sum(-1).mean() for s in range(1, 14)]
        return np.array(su), np.array(sb)
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.3))
    ks = np.arange(1, 14)
    for name, col, lab in (("ref", INK, t["ref"]), ("V0_free", C[1], t["e2var"]["V0_free"]),
                           ("V4_potentials", C[0], t["e2var"]["V4_potentials"])):
        if name not in d:
            continue
        su, sb = spectra(d[name])
        ax[0].loglog(ks, su, color=col, label=lab, lw=2.2 if name == "ref" else 1.6)
        ax[1].loglog(ks, sb, color=col, label=lab, lw=2.2 if name == "ref" else 1.6)
    ax[0].set_xlabel(t["k"]); ax[0].set_ylabel(t["Eu"]); ax[1].set_xlabel(t["k"]); ax[1].set_ylabel(t["Eb"])
    ax[0].legend(fontsize=7.5)
    finish(fig, f"e2_spectra{suffix}")

    # "in law" part: means over the test η
    law = dict(res["in_law"])
    law["V5"] = res["V5_potentials_stat"]
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    modes = [("base", t["base"]), ("tilting", t["tilt"]), ("rescaling", t["resc"]), ("V5", t["e2var"]["V5_potentials_stat"])]
    y = np.arange(len(modes))[::-1]
    for j, (key, lab) in enumerate((("balance_residual_energy", t["bal"]), ("std_diss_rel", "σ(D) / σ_ref(D)"),
                                    ("energy_distance_features", t["ed"]))):
        vals = [law[m]["test"][key] for m, _ in modes]
        ax[j].barh(y, vals, color=[C[0], C[2], C[1], C[3]], height=0.6)
        for yy, v in zip(y, vals):
            txt = f"{v:.2g}"
            ax[j].text(v, yy, " " + txt, va="center", fontsize=7.5, color=INK2)
        ax[j].set_xlabel(lab, fontsize=8)
        if key == "std_diss_rel":
            ax[j].axvline(1, color=INK2, ls="--", lw=1)
    ax[0].set_yticks(y); ax[0].set_yticklabels([lab for _, lab in modes])
    for a in ax:
        a._categ = True
    finish(fig, f"e2_in_law{suffix}")


# ---------------------------------------------------------------------------
def e3(suffix=""):
    t = TXT
    r = load(f"e3_abc{suffix}.json")
    rm = np.array([x["Rm"] for x in r["rates"]])
    lam = np.array([x["lambda"] for x in r["rates"]])
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    ax.axhline(0, color=INK2, lw=1)
    ax.fill_between(rm, 0, np.where(lam > 0, lam, 0), color=C[0], alpha=0.15, lw=0)
    ax.plot(rm, lam, "-o", color=C[0], ms=4, label="N = 32")
    conv = r.get("convergence", [])
    if conv:
        ax.plot([c["Rm"] for c in conv], [c["lambda_N48"] for c in conv], "s", color=C[1], ms=6, label="N = 48")
    ax.set_ylim(max(lam.min(), -0.06), lam.max() * 1.6)
    for s in r.get("interpolated_thresholds", []):
        ax.axvline(s, color=INK2, ls=":", lw=1)
        lab = f" {s:.1f}"
        ax.text(s, ax.get_ylim()[1] * 0.9, lab, color=INK2, fontsize=7.5)
    ax.legend(fontsize=7.5, loc="lower right")
    ax.set_xlabel(t["rm"]); ax.set_ylabel(t["lam"])
    finish(fig, f"e3_abc{suffix}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or ["e1", "e2", "e3"]
    suffix = "_quick" if "--quick" in sys.argv else ""
    for a in args:
        try:
            globals()[a](suffix)
        except FileNotFoundError as e:
            print(f"{a}: results missing ({e.filename})")
