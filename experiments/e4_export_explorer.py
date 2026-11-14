"""Export the data of a team's explorer page (race/DELIVERABLES.md §3) from the result files.

    python3 e4_export_explorer.py --team claude [--quick]

Reads, for team claude (experiment E4): the main run in ``experiments/results`` (``e4_data.json``,
``e4_reference.json``, ``e4_mhd3d_s<k>.json``, ``e4_samples_s0_*.npz``), the long trainings and the width scan
(``results/replications/e4_final_long``, ``e4_mech``, ``e4_scan2``, ``e4_final_scan``; only the variants not already read), the
hypothesis register ``research/teams/claude/hypotheses.json`` and the GPU ledger ``research/teams/claude/compute-ledger.jsonl``.

Writes ``site/teams/<team>/explorer/data/``: ``e4.json`` (reference and per-seed rows of every variant at every η),
``table.json`` (the comparative table: seed mean ± SE on the held-out η), ``hypotheses.json``, ``jobs.json`` and
``slices.json`` (a few generated and reference fields of seed 0 as 8-bit arrays). At most 25 MB in all.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from e4_digest import R, load, per_seed  # noqa: E402

SCALARS = ["ed_ratio", "div_rel_b_max", "balance_residual_total", "balance_residual_magnetic", "restart_drift_eu",
           "prod_mean_over_d", "prod_fluct_over_d", "restart_overshoot_eb", "restart_anchor_end_eb", "spec_err_b_l2", "spec_err_u_l2", "hel_m_err_rel",
           "null_count", "null_count_err_rel", "restart_drift_eb", "hc_sign_asym", "E_u", "E_B", "hel_m", "injection",
           "dissipation", "k_lambda"]
ARRAYS = ["spec_u", "spec_b", "H_shell"]
METRICS = [  # key, label, use the absolute value, objective of race/teams/claude/objectives.toml
    ("ed_ratio", "energy distance / noise floor", False, "C1"),
    ("div_rel_b_max", "relative divergence of B (largest of the ensemble)", False, "C2"),
    ("balance_residual_total", "|residual of the mean energy balance| / dissipation", True, "C3"),
    ("balance_residual_magnetic", "|residual of the mean magnetic energy balance|, production against Ohmic dissipation", True, "–"),
    ("spec_err_b_l2", "relative L2 error on the magnetic spectrum", False, "C4"),
    ("hel_m_err_rel", "relative error on the mean magnetic helicity", True, "C4"),
    ("null_count_err_rel", "relative error on the number of magnetic null points", True, "C5"),
    ("restart_drift_eb", "relative drift of the magnetic energy after a solver restart", True, "T1"),
    ("restart_drift_eu", "relative drift of the kinetic energy after a solver restart", True, "–"),
    ("hc_sign_asym", "polarity asymmetry of the cross helicity", True, "T2"),
    ("prod_fluct_over_d", "third-order part of the magnetic production / Ohmic dissipation (signed)", False, "–"),
    ("prod_mean_over_d", "mean-flow part of the magnetic production / Ohmic dissipation", False, "–"),
    ("restart_overshoot_eb", "restart anchored on the reference: overshoot of the magnetic energy", False, "–"),
    ("restart_anchor_end_eb", "restart anchored on the reference: |E_B/E_B,ref − 1| at τ = 16", False, "–"),
]
LABEL = {
    "W0_free": ("W0 free components", "none"), "W1_penalty": ("W1 divergence penalty", "loss"),
    "W2_final_projection": ("W2 final projection", "sampling"), "W3_projected_flow": ("W3 projected flow", "sampling"),
    "W4_potentials": ("W4 vector potentials", "design"), "W4s_potentials_sym": ("W4s potentials, B → −B equivariant", "design"),
    "W5_stationarity": ("W5 stationarity loss", "loss"), "W5_control": ("W5 control (same fine-tuning, no identity)", "loss"),
    "W5_stationarity_half": ("W5 stationarity loss, half ensemble", "loss"), "W5_control_half": ("W5 control, half ensemble", "loss"),
    "W6_diffusion": ("W6 diffusion (VP, v-prediction)", "family"), "W7_tilting": ("W7 exponential tilting", "sampling"),
    "W8_rescaling": ("W8 per-sample balance rescaling", "sampling"), "W4c_potentials_smooth": ("W4c potentials, smooth condition", "design"),
    "G0_gaussian_modes": ("G0 Gaussian per mode (no network)", "family"), "W9_skip_sym": ("W9 mode-wise affine term", "design"),
    "W10_anchored": ("W10 anchored on the Gaussian field", "design"), "W11_anchored_skip": ("W11 anchor + affine term", "design"),
    "W9L_skip_long": ("W9L affine term, 8× iterations", "design"), "W11L_anchored_skip_long": ("W11L anchor + affine, 8× iterations", "design"),
    "G1_gaussian_full": ("G1 Gaussian, full covariance (no network)", "family"),
    "G2_gaussianised_W9": ("G2 Gaussian law fitted to W9 samples (no network at sampling)", "family"),
    "G3_gaussianised_G1": ("G3 Gaussian law fitted to G1 samples (null control)", "family"),
    "W9N_skip_sym": ("W9 mode-wise affine term (base of G2, same job)", "design"),
    **{f"W14_full_anchor_it{k}": (f"W14 anchor on G1, iteration {k}" + (" (untrained: G1 integrated)" if k == 0 else ""), "design")
       for k in (0, 250, 500, 1000, 2000, 4000)},
    "G1T_gaussian_full": ("G1 Gaussian, full covariance (restarted at the training η too)", "family"),
    "W9R_skip_sym": ("W9 mode-wise affine term (base of the recolouring, same job)", "design"),
    "W9R_steps_check": ("W9, 200 Heun steps instead of 50 (same noise)", "design"),
    "W15_recoloured_modes": ("W15 W9 recoloured mode by mode onto the moments of the data", "sampling"),
    "W16_recoloured_full": ("W16 W9 recoloured onto the full covariance of the data", "sampling"),
    "G4_recoloured_gaussian": ("G4 Gaussian draws with the moments of W9, through the map of W16 (null control)", "family"),
    "W12_skip_stationarity": ("W12 affine term + stationarity loss", "loss"),
    "W12_skip_control": ("W12 control (same fine-tuning, no identity)", "loss"),
    "W13_skip_tilting": ("W13 affine term + exponential tilting", "sampling"),
    "W12_skip_stationarity_half": ("W12 stationarity loss, half ensemble", "loss"),
    "W12_skip_control_half": ("W12 control, half ensemble", "loss"),
    "S_w512": ("S width 512", "family"), "S_w2048": ("S width 2048", "family"), "S_w5632": ("S width 5632", "family"),
    "S_w512_long": ("S width 512, 8× iterations", "family"), "S_w2048_long": ("S width 2048, 8× iterations", "family"),
}
HYP = {  # hypotheses in which a variant is one side of the registered comparison
    "W0_free": ["H4", "H14"], "W1_penalty": ["H5"], "W2_final_projection": ["H6"], "W3_projected_flow": ["H6"],
    "W4_potentials": ["H4", "H9", "H10", "H15"], "W4s_potentials_sym": ["H9", "H12", "H17"], "W5_stationarity": ["H7", "H8"],
    "W5_control": ["H7"], "W6_diffusion": ["H10"], "W7_tilting": ["H8", "H12"], "W8_rescaling": [],
    "W4c_potentials_smooth": ["H15"], "G0_gaussian_modes": ["H16", "H18", "H19", "H20"], "W9_skip_sym": ["H17", "H18"],
    "W10_anchored": ["H19", "H20"], "W11_anchored_skip": ["H20"], "W9L_skip_long": ["H18"], "W11L_anchored_skip_long": ["H18", "H20"],
    "G1_gaussian_full": ["H22", "H26"], "G2_gaussianised_W9": ["H25", "H27"], "G3_gaussianised_G1": ["H27"], "W9N_skip_sym": ["H25", "H26", "H27"], "W12_skip_stationarity": ["H23"], "W12_skip_control": ["H23", "H24"], "W13_skip_tilting": ["H24"],
    "S_w512": ["H21"], "S_w2048": ["H21"], "S_w5632": ["H21"], "S_w512_long": ["H21"], "S_w2048_long": ["H21"],
}


def sig(x, n: int = 5):
    """Round to ``n`` significant digits (None for NaN), lists element-wise: the JSON stays small."""
    if isinstance(x, (list, tuple, np.ndarray)):
        return [sig(v, n) for v in x]
    if x is None or not np.isfinite(x):
        return None
    return float(f"{float(x):.{n}g}")


def mean_se(x: np.ndarray) -> tuple[float | None, float | None, int]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return None, None, 0
    return sig(x.mean()), sig(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else None, len(x)


def variant_block(name: str, runs: dict, source: str) -> dict:
    rows: dict = {}
    for seed, r in sorted(runs.items()):
        for split, lst in r["evaluation"].get(name, {}).items():
            for row in lst:
                e = rows.setdefault(f"{row['eta']:.5f}", {"split": split, "seeds": [], **{k: [] for k in SCALARS + ARRAYS}})
                e["seeds"].append(seed)
                for k in SCALARS:
                    e[k].append(sig(row.get(k)))
                for k in ARRAYS:
                    e[k].append(sig(row.get(k, []), 4))
    times = [r["times"].get(name, {}) for r in runs.values()]
    label, where = LABEL.get(name, (name, "design"))
    return {"id": name, "label": label, "where": where, "source": source, "hypotheses": HYP.get(name, []), "rows": rows,
            "training_time_s": mean_se(np.array([t.get("training_time_s", np.nan) for t in times]))[0],
            "fm_loss": mean_se(np.array([t.get("fm_loss_train_sample", np.nan) for t in times]))[0]}


def table_row(name: str, runs: dict, source: str, verdicts: dict) -> dict:
    out = {"id": name, "label": LABEL.get(name, (name, ""))[0], "where": LABEL.get(name, (name, "design"))[1], "source": source,
           "hypotheses": [{"id": h, "status": verdicts.get(h, "registered")} for h in HYP.get(name, [])]}
    for key, _, absolute, _ in METRICS:
        m, se, n = mean_se(per_seed(runs, name, key, absolute=absolute))
        out[key] = {"mean": m, "se": se, "n": n}
    m, se, n = mean_se(per_seed(runs, name, "ed_ratio", "train"))
    out["ed_ratio_train"] = {"mean": m, "se": se, "n": n}
    return out


def slices(quick: bool) -> dict | None:
    tag = "_quick" if quick else ""
    files = sorted(R.glob(f"e4_samples{tag}_s0_*.npz"), key=lambda p: -p.stat().st_size)
    for name in ("e4_final_long", "e4_mech", "e4_nongauss", "e4_anchor", "e4_recolour"):                        # fields of the variants the main run does not hold
        files += sorted((R / "replications" / name).glob(f"e4_samples{tag}_s0_*.npz"))
    fields: dict = {}
    eta = None
    for f in files:
        with np.load(f) as d:
            eta = float(d["eta"])
            for k in d.files:
                if k != "eta" and k not in fields and not k.endswith("_half"):
                    fields[k] = d[k].astype(np.float32)[:3]            # (3 snapshots, u|B, n, n, n, 3)
    if not fields:
        return None
    ref = fields.get("reference", next(iter(fields.values())))
    scale = [float(3.5 * ref[:, i].std()) for i in (0, 1)]              # one colour scale per field, from the reference
    out = {"eta": eta, "shape": list(ref.shape), "scale": sig(scale, 4), "order": "snapshot, field (0: u, 1: B), x, y, z, component",
           "encoding": "base64 of int8, value = q / 127 × scale[field]", "fields": {}}
    for k, a in fields.items():
        q = np.stack([np.clip(np.round(a[:, i] / scale[i] * 127), -127, 127) for i in (0, 1)], axis=1).astype(np.int8)
        out["fields"][k] = base64.b64encode(q.tobytes()).decode()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="claude")
    ap.add_argument("--quick", action="store_true", help="read the --quick result files (development only)")
    a = ap.parse_args()
    if a.team != "claude":
        raise SystemExit("only the results of team claude (experiment E4) are in this repository's branch")
    out = ROOT / "site" / "teams" / a.team / "explorer" / "data"
    out.mkdir(parents=True, exist_ok=True)
    tag = "_quick" if a.quick else ""
    data = json.loads((R / f"e4_data{tag}.json").read_text())
    ref = json.loads((R / f"e4_reference{tag}.json").read_text())
    register = json.loads((ROOT / "research" / "teams" / "claude" / "hypotheses.json").read_text())["hypotheses"]
    verdicts = {h["id"]: h["status"] for h in register}

    sets = [("experiments/results", load(a.quick))]
    if not a.quick:
        sets += [(f"experiments/results/replications/{n}", load(False, R / "replications" / n)) for n in ("e4_final_long", "e4_anchor", "e4_recolour", "e4_nongauss", "e4_mech", "e4_scan2", "e4_final_scan")]
    variants, table, seen = [], [], set()
    for source, runs in sets:
        if not runs:
            continue
        names = [n for n in LABEL if any(n in r["evaluation"] for r in runs.values()) and n not in seen]
        for n in names:
            seen.add(n)
            variants.append(variant_block(n, runs, source))
            if not n.endswith("_half"):
                table.append(table_row(n, runs, source, verdicts))
    cfg = next(iter(sets[0][1].values()))["config"] if sets[0][1] else {}
    e4 = {
        "quick": a.quick, "config": {k: cfg.get(k) for k in ("N", "nu", "kf", "iters", "batch", "width", "depth", "lr", "steps", "n_gen",
                                                            "n_gen_train", "modes", "dim_potentials", "n_train", "tau")},
        "etas": [{"eta": v["eta"], "rm": sig(1 / (2 * v["eta"]), 4), "split": v["split"]} for v in data["values"]],
        "shells": list(range(1, 10)),
        "metrics": [{"key": k, "label": lab, "abs": ab, "objective": obj} for k, lab, ab, obj in METRICS],
        "reference": {k: {"split": r["split"], "n": r["n"], "E_u": sig(r["E_u"]), "E_B": sig(r["E_B"]), "H_M": sig(r["H_M"]),
                          "null_count_mean": sig(r["null_count_mean"]), "null_count_se": sig(r["null_count_se"]),
                          "k_lambda": sig(r["k_lambda"]), "balance_residual_total": sig(r["balance_residual_total"]),
                          "ed_floor": sig(r["ed_floor_512"]), "hc_sign_asym": sig(r["hc_sign_asym"]),
                          "balance_residual_magnetic": sig(r.get("balance_residual_magnetic")), "restart_drift_eu": sig(r.get("restart_drift_eu")),
                          "restart_drift_eb": sig(r.get("restart_drift_eb")),
                          "spec_u": sig(r["spec_u"], 4), "spec_b": sig(r["spec_b"], 4), "H_shell": sig(r["H_shell"], 4)}
                      for k, r in ref["values"].items()},
        "variants": variants,
    }
    (out / "e4.json").write_text(json.dumps(e4, separators=(",", ":")), encoding="utf-8")
    (out / "table.json").write_text(json.dumps({"metrics": e4["metrics"], "rows": table}, indent=1), encoding="utf-8")
    keep = ("id", "statement", "refutation_criterion", "status", "verdict", "comparison", "seeds", "script", "commit")
    (out / "hypotheses.json").write_text(json.dumps([{k: h.get(k) for k in keep} for h in register], indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    led = [json.loads(x) for x in (ROOT / "research" / "teams" / "claude" / "compute-ledger.jsonl").read_text().splitlines() if x.strip()]
    jobs = [{"time": r["time"], "pod": r.get("pod"), "gpu": r.get("gpu"), "usd_per_hour": r.get("usd_per_hour"), "hours": r.get("hours"),
             "usd": r.get("usd"), "rc": r.get("rc"), "commit": (r.get("commit") or "")[:7], "command": (r.get("command") or "")[:160]}
            for r in led if r.get("event") != "start"]
    (out / "jobs.json").write_text(json.dumps(jobs, indent=1), encoding="utf-8")
    sl = slices(a.quick)
    if sl:
        (out / "slices.json").write_text(json.dumps(sl, separators=(",", ":")), encoding="utf-8")
    total = 0
    for f in sorted(out.iterdir()):
        total += f.stat().st_size
        print(f"{f.name:18s} {f.stat().st_size / 1e6:6.2f} MB")
    print(f"total {total / 1e6:.2f} MB (limit 25 MB, 10 MB per file); {len(variants)} variants")


if __name__ == "__main__":
    main()
