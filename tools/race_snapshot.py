#!/usr/bin/env python3
"""The clean starting repository of a race team: the repository without the work of any team.

A team must not see the reports, results or branches of the other teams (race/BRIEF.md). Reading
them through the published site is closed by the race host; reading them in the repository is
closed here: each team starts from its own private repository, holding one commit (no history)
made of `main` minus every team's work, and its GitHub token can reach that repository only.

    python3 tools/race_snapshot.py list [--ref origin/main]          # the paths that would be removed
    python3 tools/race_snapshot.py build [--ref origin/main] --branch race-start
        # one orphan commit on a local branch, then: git push <team repository> race-start:main

Removed: site/teams/<team>/ and race/teams/<team>/ of every team; experiments/<team>_* and
experiments/results/<team>_* of every team; research/ except research/README.md (the register,
journal, reviews, calls, ledgers and logs of earlier teams). `check` refuses a tree that still holds
any of them. Standard library only.
"""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = {"research/README.md", "race/teams/README.md", "site/teams/index.qmd", "site/teams/_team-table.md"}


def team_names() -> list[str]:
    cfg = tomllib.loads((ROOT / "race" / "config.toml").read_text(encoding="utf-8"))
    return sorted(set(cfg.get("teams", {})) | {"cursor", "claude"})


def is_team_work(path: str, teams: list[str]) -> bool:
    if path in KEEP:
        return False
    if path.startswith("research/"):
        return True
    for t in teams:
        if path.startswith((f"site/teams/{t}/", f"race/teams/{t}/")):
            return True
        if fnmatch.fnmatch(path, f"experiments/{t}_*") or fnmatch.fnmatch(path, f"experiments/results/{t}_*"):
            return True
    return False


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def files(ref: str) -> list[str]:
    return [p for p in git("ls-tree", "-r", "--name-only", ref).splitlines() if p]


def check(paths: list[str], teams: list[str]) -> list[str]:
    """Paths of a tree that are team work (must be empty for a starting repository)."""
    return [p for p in paths if is_team_work(p, teams)]


def build(ref: str, branch: str) -> str:
    teams = team_names()
    removed = set(check(files(ref), teams))
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(d) / "index")}
        run = lambda *a, **k: subprocess.run(["git", "-C", str(ROOT), *a], check=True, capture_output=True,
                                             text=True, env=env, **k).stdout
        run("read-tree", ref)
        if removed:
            run("update-index", "--force-remove", "--stdin", input="\n".join(sorted(removed)) + "\n")
        left = check(run("ls-files").splitlines(), teams)
        if left:
            sys.exit("team work left in the snapshot: " + " ".join(left[:10]))
        tree = run("write-tree").strip()
    src = git("rev-parse", "--short", ref).strip()
    commit = subprocess.run(["git", "-C", str(ROOT), "commit-tree", tree, "-m",
                             f"Race starting point: {ref} ({src}) without the work of any team"],
                            check=True, capture_output=True, text=True).stdout.strip()
    git("branch", "-f", branch, commit)
    return commit


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("list", "build"):
        s = sub.add_parser(name)
        s.add_argument("--ref", default="origin/main")
        if name == "build":
            s.add_argument("--branch", default="race-start")
    a = ap.parse_args()
    if a.cmd == "list":
        out = check(files(a.ref), team_names())
        print("\n".join(out))
        print(f"{len(out)} path(s) of team work in {a.ref}", file=sys.stderr)
        return 0
    commit = build(a.ref, a.branch)
    print(f"{a.branch} = {commit} (one commit, no history); push it to each team repository as its main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
