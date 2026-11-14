"""Write the tables of the report of team claude from the result files (no number is typed by hand).

    python3 e4_report_tables.py            # rewrite the blocks of site/teams/claude/report/index.qmd
    python3 e4_report_tables.py --print    # print the blocks instead

A block of the report is the text between ``<!-- e4:<name>:begin -->`` and ``<!-- e4:<name>:end -->``. Blocks:
``data`` (reference data per η), ``comparative`` (variant × metric on the held-out η, seed mean ± SE),
``hypotheses`` (register with the verdicts), ``long``, ``scan`` and ``mech`` (long trainings, width scan, Gaussian law with inter-mode covariance and mechanisms on W9), ``indep`` (replication
with other data seeds), ``objectives`` (targets of race/teams/claude/objectives.toml against the measured values),
``jobs`` (GPU ledger). Sources: ``experiments/results`` (main run), ``results/replications/e4_final_long``,
``e4_scan2`` (else ``e4_final_scan``), ``e4_mech``, ``e4_indep``, ``research/hypotheses.json``, ``research/compute-ledger.jsonl``.
"""
from __future__ import annotations

import argparse
import os
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from e4_digest import R, load, per_seed  # noqa: E402
from export_explorer import LABEL  # noqa: E402

REPORT = ROOT / "site" / "teams" / "claude" / "report" / "index.qmd"
COLS = [("ed_ratio", "ED / floor", False), ("div_rel_b_max", "div B", False), ("balance_residual_total", "energy residual", True),
        ("balance_residual_magnetic", "magnetic balance", True), ("spec_err_b_l2", "spectrum of B", False),
        ("hel_m_err_rel", "magnetic helicity", True), ("null_count_err_rel", "null points", True),
        ("restart_drift_eb", "restart drift $E_B$", True), ("restart_drift_eu", "restart drift $E_u$", True), ("hc_sign_asym", "polarity", True)]
NOTES = "@@notes@@"
WHERE = {"none": "none", "design": "design", "loss": "loss", "sampling": "sampling", "family": "family"}


def f(x: float, n: int = 3) -> str:
    if x is None or not np.isfinite(x):
        return "–"
    if x != 0 and (abs(x) < 1e-3 or abs(x) >= 1e4):
        m, e = f"{x:.1e}".split("e")
        return f"${m}\\times 10^{{{int(e)}}}$"
    return f"{x:.{n}g}"


def cell(x: np.ndarray) -> str:
    """Seed mean with its standard error in parentheses on the last digits: 217(14) = 217 ± 14, 0.456(3) = 0.456 ± 0.003.
    The error keeps two digits when its first digit is 1, one otherwise; means below 1e-3 are given as a power of ten."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return "–"
    m = float(x.mean())
    if abs(m) < 1e-12:
        return "$<10^{-12}$"
    if abs(m) < 1e-3:
        a, e = f"{m:.1e}".split("e")
        return f"${a}\\times 10^{{{int(e)}}}$"
    if len(x) < 2:
        return f(m)
    se = float(x.std(ddof=1) / np.sqrt(len(x)))
    if se <= 0 or se < 1e-6 * abs(m):
        return f(m)
    exp = int(np.floor(np.log10(se)))
    lead = int(se / 10 ** exp)
    digits = 2 if lead == 1 else 1                       # significant digits of the error
    dec = digits - 1 - exp                               # decimals to keep (may be negative)
    if dec <= 0:
        q = 10 ** (-dec)
        return f"{int(round(m / q) * q)}({int(round(se / q) * q)})"
    return f"{m:.{dec}f}({int(round(se * 10 ** dec))})"


def n_seeds(runs: dict, v: str) -> int:
    return int(np.isfinite(per_seed(runs, v, "ed_ratio")).sum())


def variants_table(runs: dict, names: list[str], extra_loss: bool = False) -> list[str]:
    head = ["Variant", "Acts through", "ED / floor, training $\\eta$"] + [c[1] for c in COLS] + (["FM loss"] if extra_loss else []) + ["Seeds"]
    out = ["| " + " | ".join(head) + " |", "|:" + "-" * 26 + "|:" + "-" * 8 + "|" + ("-" * 9 + ":|") * (len(head) - 3) + "----:|"]
    for v in names:
        if not n_seeds(runs, v):
            continue
        row = [tex(LABEL.get(v, (v, ""))[0]), WHERE[LABEL.get(v, (v, "design"))[1]], cell(per_seed(runs, v, "ed_ratio", "train"))]
        row += [cell(per_seed(runs, v, k, absolute=a)) for k, _, a in COLS]
        if extra_loss:
            row.append(cell(np.array([r["times"].get(v, {}).get("fm_loss_train_sample", np.nan) for r in runs.values()], dtype=float)))
        row.append(str(n_seeds(runs, v)))
        out.append("| " + " | ".join(row) + " |")
    return out


def block_data() -> list[str]:
    data = json.loads((R / "e4_data.json").read_text())
    ref = json.loads((R / "e4_reference.json").read_text())["values"]
    out = ["| $\\eta$ | Rm | Split | $E_u$ | $E_B$ | $H_M$ | $E_B(k{=}1)/E_B$ | Null points | $k_\\lambda$ | Energy residual | Floor of the energy distance |",
           "|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    name = {"train": "training", "val": "validation", "test": "held-out test"}
    for v in data["values"]:
        r = ref[f"{v['eta']:.5f}"]
        out.append(f"| {v['eta']:.4f} | {1 / (2 * v['eta']):.1f} | {name[v['split']]} | {f(r['E_u'])} | {f(r['E_B'])} | {f(r['H_M'])} | "
                   f"{f(r['EB_k1_fraction'])} | {f(r['null_count_mean'])} $\\pm$ {f(r['null_count_se'], 2)} | {f(r['k_lambda'])} | "
                   f"{f(r['balance_residual_total'], 2)} | {f(r['ed_floor_512'])} |")
    return out


TEX = {"½": "1/2", "η": "$\\eta$", "ν": "$\\nu$", "τ": "$\\tau$", "λ": "$\\lambda$", "π": "$\\pi$", "Σ": "$\\Sigma$",
       "⟨": "$\\langle$", "⟩": "$\\rangle$", "≥": "$\\ge$", "≤": "$\\le$", "≈": "$\\approx$", "∝": "$\\propto$",
       "→": "$\\to$", "−": "-", "×": "$\\times$", "±": "$\\pm$", "·": "$\\cdot$", "²": "$^2$", "³": "$^3$", "₁": "$_1$",
       "₀": "$_0$", "∇": "$\\nabla$", "‖": "$\\Vert$", "…": "...", "|": "\\|", "_": "\\_", "<": "$<$", ">": "$>$", "^": "\\^{}"}


def tex(s: str) -> str:
    """Text of the register for a table cell of both outputs: symbols that the PDF font lacks become maths."""
    return "".join(TEX.get(ch, ch) for ch in s)


def cut(s: str, n: int) -> str:
    """``s`` shortened to at most about ``n`` characters at the end of a sentence or clause, for a table cell."""
    if len(s) <= n:
        return tex(s)
    head = s[:n]
    stop = max(head.rfind(". "), head.rfind("; "), head.rfind(": "))
    return tex(head[: stop + 1] if stop > n // 2 else head[: head.rfind(" ")]) + " [...]"


def block_hypotheses() -> list[str]:
    reg = json.loads((ROOT / "research" / "hypotheses.json").read_text())["hypotheses"]
    out = ["| Id | Hypothesis (shortened) | Status | Verdict of the `encadrant` role (beginning) |",
           "|:---|:" + "-" * 44 + "|:" + "-" * 9 + "|:" + "-" * 40 + "|"]
    for h in reg:
        if not h["id"].startswith("H") or int(h["id"][1:]) < 4:
            continue
        st, vd = cut(h["statement"], 260), cut(h.get("verdict") or "not reviewed yet", 380)
        out.append(f"| {h['id']} | {st} | {h['status']} | {vd} |")
    return out


def block_objectives() -> list[str]:
    obj = tomllib.loads((ROOT / "race" / "teams" / "claude" / "objectives.toml").read_text())["objective"]
    out = ["| Objective | Target | Measured | Seeds | Met |", "|:---|---:|---:|---:|:---|"]
    sel = R / "e4_selection.json"
    for o in obj:
        r = subprocess.run(o["command"].split(), cwd=ROOT, capture_output=True, text=True)
        line = (r.stdout.strip().splitlines() or [""])[-1]
        try:
            val = json.loads(line)
            v, n = float(val["value"]), val.get("seeds")
            higher = o["id"].startswith(("C6", "C7"))
            met = "yes" if (v >= o["target"] if higher else v <= o["target"]) else "no"
            out.append(f"| {o['id']} | {'$\\ge$' if higher else '$\\le$'} {f(float(o['target']))} | {f(v)} | {n} | {met} |")
        except (json.JSONDecodeError, KeyError, ValueError):
            out.append(f"| {o['id']} | {f(float(o['target']))} | not measurable | – | no |")
    if sel.exists():
        s = json.loads(sel.read_text())
        out += [NOTES, f"Generator measured by C1–C5, T1 and T2: `{s.get('variant')}`, the learned variant of the main run with the lowest energy-distance ratio on the "
                    "validation $\\eta$ (file `experiments/results/e4_selection.json`)."]
    return out


def block_jobs() -> list[str]:
    led = [json.loads(x) for x in (ROOT / "research" / "compute-ledger.jsonl").read_text().splitlines() if x.strip()]
    rows = [r for r in led if r.get("event") != "start"]
    out = ["| End (UTC) | GPU | USD/h | Hours | USD | Exit | Commit | Command (shortened) |",
           "|:----------|:------------------|-----:|------:|-----:|:----|:-------|:" + "-" * 44 + "|"]
    for r in rows:
        cmd = (r.get("command") or "").replace("|", "/").replace("bash experiments/", "")
        cmd = cmd[:60] + (" ..." if len(cmd) > 60 else "")
        out.append(f"| {r['time'][5:16].replace('T', ' ')} | {(r.get('gpu') or '–').replace('NVIDIA ', '')} | {r.get('usd_per_hour', 0):.2f} | "
                   f"{r.get('hours', 0):.3f} | {r.get('usd', 0):.2f} | {'–' if r.get('rc') is None else r.get('rc')} | `{(r.get('commit') or '')[:7]}` | {tex(cmd)} |")
    out += [NOTES, f"Total: {len(rows)} ledger entries, {sum(r.get('hours', 0) for r in rows):.2f} GPU hours, "
                f"{sum(r.get('usd', 0) for r in rows):.2f} USD."]
    return out


def block_indep(main: dict) -> list[str]:
    other = load(False, R / "replications" / "e4_indep")
    if not other:
        return ["*(The replication with other data seeds is not available.)*"]
    cols = [("ed_ratio", "ED / floor", False), ("balance_residual_magnetic", "magnetic balance", True),
            ("null_count_err_rel", "null points", True), ("restart_drift_eb", "restart drift $E_B$", True)]
    out = ["| Variant | " + " | ".join(f"{lab}, main | {lab}, other" for _, lab, _ in cols) + " |",
           "|:" + "-" * 30 + "|" + ("-" * 9 + ":|") * (2 * len(cols))]
    for v in LABEL:
        if v.endswith("_half") or not n_seeds(main, v) or not n_seeds(other, v):
            continue
        out.append(f"| {tex(LABEL[v][0])} | " + " | ".join(
            f"{cell(per_seed(main, v, k, absolute=ab))} | {cell(per_seed(other, v, k, absolute=ab))}" for k, _, ab in cols) + " |")
    return out


def block_split() -> list[str]:
    """Production split and restart anchored on the reference energy (H25–H27), from the job e4_nongauss."""
    root = R / "replications" / "e4_nongauss"
    runs = load(False, root)
    if not runs or not (root / "e4_reference.json").exists():
        return ["*(not available)*"]
    ref = json.loads((root / "e4_reference.json").read_text())["values"]
    names = [v for v in ("G0_gaussian_modes", "G1_gaussian_full", "G3_gaussianised_G1", "W9N_skip_sym", "G2_gaussianised_W9", "W11_anchored_skip",
                         "W10_anchored") if n_seeds(runs, v)]
    etas = sorted({x["eta"] for r in runs.values() for x in r["evaluation"][names[0]]["test"]}, reverse=True)
    lab = {"W9N_skip_sym": "W9 mode-wise affine term", "G2_gaussianised_W9": "G2 Gaussian law fitted to W9 samples",
           "G3_gaussianised_G1": "G3 Gaussian law fitted to G1 samples (null control)"}
    head = ["Law"] + [f"mean-flow part, $\\eta$ = {e:.4f}" for e in etas] + [f"third-order part, $\\eta$ = {e:.4f}" for e in etas] + \
           ["$a_B(0)$", "overshoot of $E_B$", "$|a_B|$ at $\\tau = 16$"]
    out = ["| " + " | ".join(head) + " |", "|:" + "-" * 26 + "|" + ("-" * 9 + ":|") * (len(head) - 1)]

    def pm(m: float, se: float) -> str:
        return cell(np.array([m - se, m + se])) if se > 0 else f(m)       # two points with this mean and this SE (sd·√2/√2)

    rr = [ref[f"{e:.5f}"] for e in etas]
    row = ["reference (SE: jackknife over trajectories; 4 restart draws)"]
    row += [pm(r["prod_mean_over_d"], r.get("prod_mean_over_d_se_jack", 0.0)) for r in rr]
    row += [pm(r["prod_fluct_over_d"], r.get("prod_fluct_over_d_se_jack", 0.0)) for r in rr]
    if "restart_anchor_eb_mean" in rr[0]:
        a0 = np.array([r["restart_anchor_eb_mean"][0] for r in rr])
        ov = np.array([max(abs(v) for v in r["restart_anchor_eb_mean"][1:]) - abs(r["restart_anchor_eb_mean"][0]) for r in rr])
        en = np.array([abs(r["restart_anchor_eb_mean"][-1]) for r in rr])
        row += [f(float(a0.mean())), f(float(ov.mean())), f(float(en.mean()))]
    else:
        row += ["–", "–", "–"]
    out.append("| " + " | ".join(row) + " |")
    for v in names:
        row = [tex(lab.get(v, LABEL.get(v, (v, ""))[0]))]
        for key in ("prod_mean_over_d", "prod_fluct_over_d"):
            for e in etas:
                row.append(cell(np.array([x[key] for r in runs.values() for x in r["evaluation"][v]["test"] if x["eta"] == e])))
        a0 = np.array([np.mean([x["restart_anchor"]["eb"][0] for x in r["evaluation"][v]["test"]]) for r in runs.values()])
        row += [cell(a0), cell(per_seed(runs, v, "restart_overshoot_eb")), cell(per_seed(runs, v, "restart_anchor_end_eb"))]
        out.append("| " + " | ".join(row) + " |")
    return out


def block_later(run: str, names: list[str]) -> list[str]:
    """Table of a later job (H28: e4_anchor; H29-H31: e4_recolour): distance, the two parts of the production against the
    reference, second moments, balances, null points and the restart anchored on the reference energy."""
    root = R / "replications" / run
    runs = load(False, root)
    if not runs or not (root / "e4_reference.json").exists():
        return ["*(not available)*"]
    ref = json.loads((root / "e4_reference.json").read_text())["values"]
    names = [v for v in names if n_seeds(runs, v)]
    if not names:
        return ["*(not available)*"]
    etas = sorted({x["eta"] for r in runs.values() for x in r["evaluation"][names[0]]["test"]}, reverse=True)
    rv = lambda e, k: ref[f"{e:.5f}"][k]                                                 # noqa: E731
    head = ["Law", "ED / floor, validation $\\eta$", "ED / floor"] + [f"third-order part / reference, $\\eta$ = {e:.4f}" for e in etas] + \
           ["mean-flow part $-$ reference", "$E_B/E_{B,\\mathrm{ref}} - 1$", "magnetic balance", "energy residual", "spectrum of B", "null points",
            "$a_B(0)$", "excursion of $E_B$", "overshoot of $E_B$", "drift $E_B$, $\\tau = 4$", "FM loss", "Seeds"]
    out = ["| " + " | ".join(head) + " |", "|:" + "-" * 26 + "|" + ("-" * 9 + ":|") * (len(head) - 1)]

    def worst(v: str, fn) -> str:
        """Deviation of largest absolute value over the held-out η, on the seed means (as in the registered criteria)."""
        d = [float(np.mean([fn(x) for r in runs.values() for x in r["evaluation"][v]["test"] if x["eta"] == e])) for e in etas]
        return f(max(d, key=abs))

    def anchor(v: str, fn) -> np.ndarray:
        return np.array([np.mean([fn(x["restart_anchor"]["eb"]) for x in r["evaluation"][v]["test"] if "restart_anchor" in x] or [np.nan])
                         for r in runs.values()])

    for v in names:
        row = [tex(LABEL.get(v, (v, ""))[0]), cell(per_seed(runs, v, "ed_ratio", "val")), cell(per_seed(runs, v, "ed_ratio"))]
        row += [cell(np.array([x["prod_fluct_over_d"] / rv(e, "prod_fluct_over_d") for r in runs.values() for x in r["evaluation"][v]["test"]
                               if x["eta"] == e])) for e in etas]
        row += [worst(v, lambda x: x["prod_mean_over_d"] - rv(x["eta"], "prod_mean_over_d")), worst(v, lambda x: x["E_B"] / rv(x["eta"], "E_B") - 1)]
        row += [cell(per_seed(runs, v, k, absolute=True)) for k in ("balance_residual_magnetic", "balance_residual_total")]
        row += [cell(per_seed(runs, v, "spec_err_b_l2")), cell(per_seed(runs, v, "null_count_err_rel", absolute=True))]
        row += [cell(anchor(v, lambda a: a[0])), cell(anchor(v, lambda a: max(0.0, max(a[1:])))), cell(per_seed(runs, v, "restart_overshoot_eb")),
                cell(per_seed(runs, v, "restart_drift_eb", absolute=True))]
        row.append(cell(np.array([r["times"].get(v, {}).get("fm_loss_train_sample", np.nan) for r in runs.values()], dtype=float)))
        row.append(str(n_seeds(runs, v)))
        out.append("| " + " | ".join(row) + " |")
    cells = [[c.strip() for c in line.strip("|").split(" | ")] for line in out]
    k = head.index("FM loss")
    if all(c[k].strip() == "–" for c in cells[2:]):               # no loss recorded for these laws: drop the column
        out = ["| " + " | ".join(c[:k] + c[k + 1:]) + " |" for c in cells[:1] + cells[2:]]
        out.insert(1, "|:" + "-" * 26 + "|" + ("-" * 9 + ":|") * (len(head) - 2))
    return out


def blocks() -> dict[str, list[str]]:
    main = load(False)
    names = [v for v in LABEL if not v.endswith("_half") and not v.startswith("S_") and not v.endswith("_long")]
    long = load(False, R / "replications" / "e4_final_long")
    scan = load(False, R / "replications" / "e4_scan2") or load(False, R / "replications" / "e4_final_scan")
    mech = load(False, R / "replications" / "e4_mech")
    return {
        "data": block_data(),
        "comparative": variants_table(main, names),
        "hypotheses": block_hypotheses(),
        "long": variants_table(long, ["G0_gaussian_modes", "W9_skip_sym", "W9L_skip_long", "W10_anchored", "W11_anchored_skip",
                                      "W11L_anchored_skip_long"], extra_loss=True) if long else ["*(not available)*"],
        "scan": variants_table(scan, ["S_w512", "S_w2048", "S_w5632", "S_w512_long", "S_w2048_long", "W9_skip_sym", "G0_gaussian_modes"],
                               extra_loss=True) if scan else ["*(not available)*"],
        "mech": variants_table(mech, ["G0_gaussian_modes", "G1_gaussian_full", "W9_skip_sym", "W11_anchored_skip", "W12_skip_control",
                                      "W12_skip_stationarity", "W12_skip_control_half", "W13_skip_tilting"]) if mech else ["*(not available)*"],
        "indep": block_indep(main),
        "split": block_split(),
        "anchor": block_later("e4_anchor", ["G1_gaussian_full"] + [f"W14_full_anchor_it{k}" for k in (0, 250, 500, 1000, 2000, 4000)]),
        "recolour": block_later("e4_recolour", ["G1_gaussian_full", "G4_recoloured_gaussian", "W9R_skip_sym", "W9R_steps_check",
                                                "W15_recoloured_modes", "W16_recoloured_full"]),
        "objectives": block_objectives(),
        "jobs": block_jobs(),
        "release": block_release(),
        "releaseeval": block_releaseeval(),
    }


RELEASE = Path(os.environ.get("E4_RELEASE_DIR", ROOT / "research" / "release"))


def block_release() -> list[str]:
    """Files of the published release (research/release/manifest.json, written by the release build)."""
    path = RELEASE / "manifest.json"
    man = json.loads(path.read_text()) if path.exists() else {}
    if "url" not in man:
        return ["| File | Content | Format | Size |", "|:---|:---|:---|---:|", "| – | the release is not built yet | – | – |"]
    url, data, mods = man["url"], man["data_files"], man["model_files"]
    mib = lambda b: f"{b / 2**20:.1f} MiB" if b < 2**30 else f"{b / 2**30:.2f} GiB"                 # noqa: E731
    link = lambda f: f"[`{f}`]({url}/{f})"                                                           # noqa: E731
    rows = ["| File | Content | Format | Size |", "|:-----------------------|:------------------------------------------|:------------------|-------:|"]
    etas = "`e4_eta<η>.h5` for η = " + ", ".join(f"[{f['eta']:.5f}]({url}/{f['file']})" for f in data)
    rows.append(f"| {etas} | Reference data, one file per $\\eta$ ({data[0]['n_trajectories']} trajectories × {data[0]['n_t']} snapshots): "
                f"fields $u$ and $B$ on the $16^3$ grid, time series of the solver, provenance; splits train, val and test in the metadata | "
                f"MFF 1.0: HDF5 with the layout of The Well | {len(data)} files, {mib(sum(f['size_bytes'] for f in data))} in all |")
    rows.append(f"| {link(man['sample']['file'])} | Sample of the data: {man['sample']['content']} | MFF 1.0 | {mib(man['sample']['size_bytes'])} |")
    kinds = {"latent space": "Latent space of the models and its normalisation", "G0": "Parameters of the Gaussian law G0 (mean and covariance per Fourier mode at each training $\\eta$)",
             "G1": "Parameters of the Gaussian law G1 (mean and factor of the full covariance at each training $\\eta$)",
             "W9": "Weights of the flow-matching model W9, one file per seed", "W16": "Linear map of W16 at the three held-out $\\eta$, one file per seed of W9"}
    for kind, what in kinds.items():
        fs = [f for f in mods if f["kind"] == kind]
        if fs:
            size = mib(fs[0]["size_bytes"]) if len(fs) == 1 else f"{len(fs)} files, {mib(sum(f['size_bytes'] for f in fs))} in all"
            rows.append(f"| {', '.join(link(f['file']) for f in fs)} | {what} | PyTorch dictionary of tensors | {size} |")
    rows.append(f"| {link('catalog.sqlite')}, {link('catalog.json')} | Catalogue: data set `e4_mhd3d` 1.0 with its splits, {man['catalog']['released_models']} released models with "
                f"file, hyperparameters, commit, data set and evaluations, and the cited runs as records without files | SQLite (`milady.catalog`), JSON export | – |")
    rows.append(f"| {link('SHA256SUMS')}, {link('manifest.json')}, {link('README.md')} | Checksums, list of the files with sizes and identifiers, notes | text, JSON | – |")
    return rows


def block_releaseeval() -> list[str]:
    """Metrics of the released models against those of the cited runs (research/release/catalog.json)."""
    path = RELEASE / "catalog.json"
    ev = json.loads(path.read_text()).get("evaluation_summary", {}) if path.exists() else {}
    head = ["| Law | Metric | Runs cited by the report (GPU) | Released models (CPU build) |", "|:----|:--------------------------------------|:------------------------|:------------------------|"]
    if not any(k.startswith("released/") for k in ev):
        return head + ["| – | the release is not built yet | – | – |"]
    metrics = (("energy distance over the noise floor", "ed_ratio"), ("relative error of the magnetic energy", "err_Eb_rel"),
               ("third-order part of the production over the dissipation", "prod_fluct_over_d"), ("residual of the energy balance", "balance_residual_total"),
               ("null-count error", "null_count_err_rel"), ("restart drift of the magnetic energy", "restart_drift_eb"))

    def cell(key: str, metric: str) -> str:
        vals = [v["mean_over_seeds"] for k, v in ev.get(key, {}).items() if k.startswith(metric + " @")]
        return ", ".join(f"{x:.3g}" for x in vals) if vals else "not evaluated"

    man = json.loads((RELEASE / "manifest.json").read_text())
    notes = [f"The release was built from commit `{str(man['git_commit'])[:12]}` on {man['host']}. The map of W16 is estimated there on {man['n_recolour']} samples of W9 per "
             "held-out $\\eta$ (131 072 in the report, on a GPU), and W16 is evaluated on 512 samples outside that estimate, without the restart in the solver."]
    return head + [f"| {law} | {name} | {cell('cited/' + law, m)} | {cell('released/' + law, m)} |" for law in ("G0", "G1", "W9", "W16") for name, m in metrics] + [NOTES] + notes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    b = blocks()
    if a.print:
        for k, v in b.items():
            print(f"--- {k}\n" + "\n".join(v) + "\n")
        return
    text = REPORT.read_text(encoding="utf-8")
    for k, v in b.items():
        pat = re.compile(rf"(<!-- e4:{k}:begin -->\n).*?(<!-- e4:{k}:end -->)", re.DOTALL)
        if not pat.search(text):
            print(f"block {k}: no marker in the report")
            continue
        cap = re.search(r"\n(: [^\n]*\{#tbl-[a-z]+\})\s*\Z", pat.search(text).group(0).rsplit("<!--", 1)[0])
        tail = f"\n{cap.group(1)}\n\n" if cap else ""          # the caption of the table lives inside the block
        table = v[: v.index(NOTES)] if NOTES in v else v        # notes of a block come before its table and caption
        notes = v[v.index(NOTES) + 1:] if NOTES in v else []
        body = ("\n".join(notes) + "\n\n" if notes else "") + "\n".join(table) + "\n" + tail
        text = pat.sub(lambda m, body=body: m.group(1) + body + m.group(2), text)
        print(f"block {k}: {len(v)} lines")
    REPORT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
