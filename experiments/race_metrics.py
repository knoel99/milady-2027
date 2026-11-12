"""Measurement commands of the race objectives (race/teams/claude/objectives.toml).

Each metric reads committed result files only, trains nothing, and prints on its last line a JSON
object ``{"value": <number>, "seeds": <n>}``. It exits with code 1 when the files it needs are
missing (the objective cannot be measured yet).

    python3 experiments/race_metrics.py --metric c1     # c1 … c7, t1, t2
    python3 experiments/race_metrics.py --all            # every metric, one line each (no exit code)

Files read
----------
- ``experiments/results/e4_mhd3d_s<k>.json`` (k = 0 … 4), written by ``experiments/e4_mhd3d.py``:
  ``evaluation[variant]["test"]`` is a list of rows, one per held-out parameter value;
- ``experiments/results/e4_selection.json``, written by ``experiments/e4_digest.py``: the variant
  that C1–C5, T1 and T2 measure. It is selected on the **validation** parameter values (lowest C1
  ratio, mean over the seeds), never on the held-out test values;
- ``research/hypotheses.json`` (C6) and the registry ``milady.train.constraints.REGISTRY`` with
  ``tests/test_constraints.py`` (C7).

Row keys (all computed on the n generated samples of one held-out value and one seed):
``ed_ratio`` (energy distance to the reference on standardized physical features, divided by the
noise floor: mean energy distance between two disjoint reference subsamples of the same size),
``div_rel_b_max`` (max over samples of ‖∇·B‖/‖∇B‖), ``balance_residual_total``
(E[injection − Dν − Dη] / E[Dν + Dη]), ``spec_err_b_l2`` (relative L2 error of the mean shell
spectrum of B), ``hel_m_err_rel`` (relative error of the mean magnetic helicity),
``null_count_err_rel`` (relative error of the mean number of magnetic null points),
``restart_drift_eb`` (relative change of the ensemble-mean magnetic energy after advancing the
generated snapshots with the solver), ``hc_sign_asym`` (|P(⟨u·B⟩ > 0) − ½|).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "experiments" / "results"
SEEDS = (0, 1, 2, 3, 4)
MIN_SEEDS = 5


class Unmeasurable(Exception):
    """The files needed by a metric are missing or incomplete."""


def _selected_variant() -> str:
    path = RESULTS / "e4_selection.json"
    if not path.exists():
        raise Unmeasurable(f"missing {path.relative_to(ROOT)} (run experiments/e4_digest.py)")
    return str(json.loads(path.read_text(encoding="utf-8"))["variant"])


def _test_rows(variant: str) -> dict[int, list[dict]]:
    """Held-out rows of ``variant`` per seed."""
    out = {}
    for s in SEEDS:
        path = RESULTS / f"e4_mhd3d_s{s}.json"
        if not path.exists():
            continue
        ev = json.loads(path.read_text(encoding="utf-8")).get("evaluation", {})
        rows = ev.get(variant, {}).get("test")
        if rows:
            out[s] = rows
    if len(out) < MIN_SEEDS:
        raise Unmeasurable(f"{len(out)} seed file(s) with variant {variant!r}, {MIN_SEEDS} needed")
    return out


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _seed_mean(key: str, absolute: bool = False, extra: str | None = None) -> tuple[float, int]:
    """Mean over the seeds of the mean over the held-out values of ``key`` (+ ``extra``)."""
    rows = _test_rows(_selected_variant())
    per_seed = []
    for rs in rows.values():
        vals = []
        for r in rs:
            if key not in r or (extra and extra not in r):
                raise Unmeasurable(f"key {key!r} missing in a result row")
            v = abs(r[key]) if absolute else r[key]
            if extra:
                v += abs(r[extra]) if absolute else r[extra]
            vals.append(float(v))
        per_seed.append(_mean(vals))
    return _mean(per_seed), len(per_seed)


def c1() -> tuple[float, int]:
    return _seed_mean("ed_ratio")


def c2() -> tuple[float, int]:
    rows = _test_rows(_selected_variant())
    vals = [float(r["div_rel_b_max"]) for rs in rows.values() for r in rs]
    return max(vals), len(rows)


def c3() -> tuple[float, int]:
    return _seed_mean("balance_residual_total", absolute=True)


def c4() -> tuple[float, int]:
    return _seed_mean("spec_err_b_l2", absolute=True, extra="hel_m_err_rel")


def c5() -> tuple[float, int]:
    return _seed_mean("null_count_err_rel", absolute=True)


def t1() -> tuple[float, int]:
    return _seed_mean("restart_drift_eb", absolute=True)


def t2() -> tuple[float, int]:
    return _seed_mean("hc_sign_asym", absolute=True)


def c6() -> tuple[float, int]:
    """Hypotheses comparing constraint mechanisms or model families, 5 seeds, encadrant verdict."""
    path = ROOT / "research" / "hypotheses.json"
    hyps = json.loads(path.read_text(encoding="utf-8")).get("hypotheses", [])
    n = 0
    for h in hyps:
        compares = str(h.get("comparison", "")).strip().lower() in ("constraint mechanisms", "model families")
        seeds = int(h.get("seeds", 0) or 0)
        verdict = re.match(r"\s*(CONFIRMED|REFUTED)\b", str(h.get("verdict", "")))
        if compares and seeds >= MIN_SEEDS and verdict:
            n += 1
    return float(n), MIN_SEEDS


def c7() -> tuple[float, int]:
    """Entries of ``milady.train.constraints.REGISTRY`` whose test ``test_<name>`` passes."""
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from milady.train.constraints import REGISTRY
    except ImportError:
        return 0.0, 0
    test_file = ROOT / "tests" / "test_constraints.py"
    if not test_file.exists():
        return 0.0, 0
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rA", "-p", "no:cacheprovider", str(test_file)],
                       cwd=ROOT, capture_output=True, text=True, timeout=540, check=False)
    passed = set(re.findall(r"^PASSED .*::test_(\w+)", r.stdout, re.MULTILINE))
    return float(sum(1 for name in REGISTRY if name in passed)), 0


METRICS = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5, "c6": c6, "c7": c7, "t1": t1, "t2": t2}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--metric", choices=sorted(METRICS))
    g.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        for name, fn in METRICS.items():
            try:
                value, seeds = fn()
                print(name, json.dumps({"value": value, "seeds": seeds}))
            except Unmeasurable as e:
                print(name, f"unmeasurable: {e}")
        return 0
    try:
        value, seeds = METRICS[a.metric]()
    except Unmeasurable as e:
        print(f"unmeasurable: {e}", file=sys.stderr)
        return 1
    print(json.dumps({"value": value, "seeds": seeds}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
