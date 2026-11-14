"""Assemble the second width scan of E4 (H21) from its three GPU jobs, split by seed.

    python3 e4_assemble_scan.py

Reads ``results/replications/e4_scan2a`` (seeds 0, 1), ``e4_scan2b`` (seeds 2, 3) and ``e4_scan2c`` (seed 4): each job
regenerated the reference data from the same seeds on its own pod. Writes ``results/replications/e4_scan2``: the
group files D and S of every seed (the clone of a job also holds the files of other runs, which are left out),
the reference, data and floor files of the first job, and ``assembly.json`` with the largest relative difference
of the reference statistics between the jobs (the data are deterministic on one CPU type and chaotic across types).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from e4_digest import R, merge

PARTS = {"e4_scan2a": (0, 1), "e4_scan2b": (2, 3), "e4_scan2c": (4,)}
KEYS = ("E_u", "E_B", "H_M", "null_count_mean", "ed_floor_512")


def main() -> None:
    root = R / "replications"
    out = root / "e4_scan2"
    out.mkdir(exist_ok=True)
    refs, info = {}, {"parts": {}, "reference_from": None}
    for name, seeds in PARTS.items():
        src = root / name
        if not (src / "e4_reference.json").exists():
            print(f"{name}: not there yet")
            continue
        refs[name] = json.loads((src / "e4_reference.json").read_text())["values"]
        copied = []
        for s in seeds:
            for f in sorted(src.glob(f"e4_mhd3d_s{s}_[DS].json")):         # the groups of this job; the clone holds others
                d = json.loads(f.read_text())
                if d["config"]["device"] != "cpu" and d["config"]["seed"] == s:
                    shutil.copy(f, out / f.name)
                    copied.append(f.name)
        info["parts"][name] = {"seeds": list(seeds), "files": copied,
                               "data_duration_s": json.loads((src / "e4_data.json").read_text()).get("duration_s")}
        if info["reference_from"] is None:
            for f in ("e4_reference.json", "e4_data.json", "e4_floor.json"):
                if (src / f).exists():
                    shutil.copy(src / f, out / f)
            info["reference_from"] = name
        for f in src.glob("e4_samples_s0_*.npz"):
            shutil.copy(f, out / f.name)
    first = next(iter(refs), None)
    for name, ref in refs.items():
        if name != first:
            info["parts"][name]["max_rel_diff_reference"] = max(
                abs(ref[e][k] - refs[first][e][k]) / max(abs(refs[first][e][k]), 1e-12) for e in ref for k in KEYS)
    for s in range(5):
        merged = out / f"e4_mhd3d_s{s}.json"
        merged.unlink(missing_ok=True)
        merge(s, "", out)
    (out / "assembly.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(json.dumps({k: {"seeds": v["seeds"], "files": len(v["files"]), "max_rel_diff_reference": v.get("max_rel_diff_reference")}
                      for k, v in info["parts"].items()}, indent=1))


if __name__ == "__main__":
    main()
