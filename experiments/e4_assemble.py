"""Assemble a run of E4 from several GPU jobs split by seed.

    python3 e4_assemble.py --out e4_recolour --groups G,T,R --part e4_recolour_a:0,1,2 --part e4_recolour_b:3,4

Each job regenerated the reference data from the same seeds on its own pod. Writes ``results/replications/<out>``:
the files of the named groups for the seeds of each part (the clone of a job also holds the files of other runs,
which are left out: wrong group, wrong seed, CPU device, or another number of restart samples than the part's own
reference), the reference, data and floor files of the first part, the samples of seed 0, and ``assembly.json``
with the largest relative difference of the reference statistics between the parts (the data are deterministic on
one CPU type and chaotic across types). Generalises ``e4_assemble_scan.py`` (H21).
"""
from __future__ import annotations

import argparse
import json
import shutil

from e4_digest import R, merge

KEYS = ("E_u", "E_B", "H_M", "null_count_mean", "ed_floor_512")


def assemble(out_name: str, groups: list[str], parts: dict[str, tuple[int, ...]]) -> dict:
    root = R / "replications"
    out = root / out_name
    out.mkdir(exist_ok=True)
    refs, info = {}, {"parts": {}, "groups": groups, "reference_from": None}
    for name, seeds in parts.items():
        src = root / name
        if not (src / "e4_reference.json").exists():
            print(f"{name}: not there yet")
            continue
        refs[name] = json.loads((src / "e4_reference.json").read_text())["values"]
        copied = []
        for s in seeds:
            for g in groups:
                f = src / f"e4_mhd3d_s{s}_{g}.json"
                if not f.exists():
                    continue
                d = json.loads(f.read_text())
                if d["config"]["device"] != "cpu" and d["config"]["seed"] == s:
                    shutil.copy(f, out / f.name)
                    copied.append(f.name)
        data = src / "e4_data.json"
        info["parts"][name] = {"seeds": list(seeds), "files": copied,
                               "data_duration_s": json.loads(data.read_text()).get("duration_s") if data.exists() else None}
        if info["reference_from"] is None:
            for f in ("e4_reference.json", "e4_data.json", "e4_floor.json"):
                if (src / f).exists():
                    shutil.copy(src / f, out / f)
            info["reference_from"] = name
        for f in src.glob("e4_samples_s0_*.npz"):
            if 0 in seeds:
                shutil.copy(f, out / f.name)
    first = next(iter(refs), None)
    for name, ref in refs.items():
        if name != first:
            info["parts"][name]["max_rel_diff_reference"] = max(
                abs(ref[e][k] - refs[first][e][k]) / max(abs(refs[first][e][k]), 1e-12) for e in ref for k in KEYS if k in ref[e])
    for s in sorted({s for seeds in parts.values() for s in seeds}):
        (out / f"e4_mhd3d_s{s}.json").unlink(missing_ok=True)
        merge(s, "", out)
    (out / "assembly.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    return info


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="name of the assembled run under results/replications/")
    ap.add_argument("--groups", required=True, help="comma-separated groups of the jobs, e.g. G,T,R")
    ap.add_argument("--part", action="append", required=True, help="<directory>:<seeds>, e.g. e4_recolour_a:0,1,2 (repeat)")
    a = ap.parse_args()
    parts = {p.split(":")[0]: tuple(int(x) for x in p.split(":")[1].split(",")) for p in a.part}
    info = assemble(a.out, a.groups.split(","), parts)
    print(json.dumps({k: {"seeds": v["seeds"], "files": len(v["files"]), "max_rel_diff_reference": v.get("max_rel_diff_reference")}
                      for k, v in info["parts"].items()}, indent=1))


if __name__ == "__main__":
    main()
