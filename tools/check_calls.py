#!/usr/bin/env python3
"""Verify that roles were called with the right model and the right reasoning effort.

    python3 tools/check_calls.py ledger [--provider P] [--since 20261112T000000Z]
        Check every ledger entry against agents/providers.toml: expected model and effort for
        the role, call accepted, model echoed by the API. Exit 1 on any mismatch.
    python3 tools/check_calls.py preflight --provider P [--dry-run]
        One minimal API call per (model, effort) pair the roles use: shows which settings the
        provider accepts, the model it echoes and the reasoning tokens. Costs a few cents.
    python3 tools/check_calls.py exam --provider P --since STAMP
        Autonomy test: after an agent was asked, without help, to call every role (see
        research/preflight-exam.md), check that the ledger holds, since STAMP, at least one
        accepted call per role with the expected model and effort.

The ledger is research/model-calls.jsonl, or $MILADY_LEDGER. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from call_model import ROLES, ROOT, call, load_providers, load_role, resolve


def ledger_path() -> Path:
    return Path(os.environ.get("MILADY_LEDGER", ROOT / "research" / "model-calls.jsonl"))


def read_ledger(provider: str | None, since: str | None) -> list[dict]:
    path = ledger_path()
    if not path.exists():
        return []
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [r for r in rows if (not provider or r["provider"] == provider) and (not since or r["time"] >= since)]


def expected(providers: dict, row: dict) -> tuple[str, object]:
    cfg = providers[row["provider"]]
    if row.get("kind") == "harness":
        model, peff = resolve(cfg, row["tier"], row["level"], api=False)
        src = cfg["harness"]["effort_source"]
        return model, {"level": row["level"], "provider": peff, "none": None}[src]
    return resolve(cfg, row["tier"], row["level"])


def verdict(providers: dict, row: dict) -> list[str]:
    problems = []
    if row.get("role"):
        meta, _ = load_role(row["role"])
        if (row["tier"], row["level"]) != (meta["tier"], meta["reasoning"]):
            problems.append(f"role {row['role']} is {meta['tier']}/{meta['reasoning']}, call used {row['tier']}/{row['level']}")
    model, effort = expected(providers, row)
    if row["model"] != model:
        problems.append(f"model {row['model']} != expected {model}")
    if row.get("effort") != effort:
        problems.append(f"effort {row.get('effort')} != expected {effort}")
    ok = row["status"] == 0 if row.get("kind") == "harness" else row["status"] == 200
    if not ok:
        problems.append(f"call failed (status {row['status']}): {(row.get('error') or '')[:120]}")
    echoed = row.get("response_model")
    if row.get("kind") != "harness" and ok and echoed and not (
            str(echoed).startswith(model) or model.startswith(str(echoed)) or model in str(echoed)):
        problems.append(f"API answered with model {echoed}, requested {model}")
    return problems


def cmd_ledger(args) -> int:
    providers, rows = load_providers(), read_ledger(args.provider, args.since)
    if not rows:
        print("ledger empty for this selection")
        return 1
    bad = 0
    for r in rows:
        p = verdict(providers, r)
        bad += bool(p)
        tag = "OK  " if not p else "FAIL"
        print(f"{tag} {r['time']} {r['provider']:9} {r.get('role') or r['tier']!s:13} {r.get('kind', 'api'):7} "
              f"model={r['model']} effort={r.get('effort')} reasoning_tokens={r.get('reasoning_tokens')}"
              + ("".join(f"\n       - {x}" for x in p)))
    print(f"{len(rows) - bad}/{len(rows)} calls conform")
    return 1 if bad else 0


def cmd_preflight(args) -> int:
    cfg = load_providers()[args.provider]
    pairs = {}
    for role in sorted(ROLES.glob("*.md")):
        meta, _ = load_role(role.stem)
        pairs.setdefault(resolve(cfg, meta["tier"], meta["reasoning"]), (meta["tier"], meta["reasoning"]))
    failed = 0
    for (model, effort), (tier, level) in pairs.items():
        if args.dry_run:
            print(f"would call {args.provider} model={model} effort={effort} ({tier}/{level})")
            continue
        e = call(args.provider, tier, level, "Answer in one word.", "Reply with the single word OK.",
                 role=None, max_tokens=4000, save=False)
        good = e["status"] == 200
        failed += not good
        print(f"{'OK  ' if good else 'FAIL'} model={model} effort={effort} status={e['status']} "
              f"echoed={e['response_model']} reasoning_tokens={e['reasoning_tokens']} "
              f"answer={e['text'][:20]!r}" + (f"\n       {(e['error'] or '')[:300]}" if not good else ""))
    return 1 if failed else 0


def cmd_exam(args) -> int:
    providers, rows = load_providers(), read_ledger(args.provider, args.since)
    roles = sorted(r.stem for r in ROLES.glob("*.md"))
    missing = []
    for role in roles:
        good = [r for r in rows if r.get("role") == role and not verdict(providers, r)]
        tried = [r for r in rows if r.get("role") == role]
        state = "PASS" if good else ("FAIL" if tried else "MISSING")
        if not good:
            missing.append(role)
        print(f"{state:7} {role:13} {len(good)} conforming call(s) out of {len(tried)}")
    print("exam passed" if not missing else f"exam failed: {', '.join(missing)}")
    return 1 if missing else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ledger")
    a.add_argument("--provider")
    a.add_argument("--since")
    b = sub.add_parser("preflight")
    b.add_argument("--provider", required=True)
    b.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("exam")
    c.add_argument("--provider", required=True)
    c.add_argument("--since", required=True)
    args = ap.parse_args()
    return {"ledger": cmd_ledger, "preflight": cmd_preflight, "exam": cmd_exam}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
