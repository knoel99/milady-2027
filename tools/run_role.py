#!/usr/bin/env python3
"""Run a role as a separate headless session of the team's own harness, with the role's model
and reasoning effort, so that it can use tools (read files, re-run scripts, browse).

The harness command, its environment and how the effort is passed come from the provider's
[harness] table in agents/providers.toml; the model from the role's tier and the provider's
[tier] table. Each run is appended to the same ledger as tools/call_model.py (kind "harness")
and its output saved under research/calls/.

    python3 tools/run_role.py --provider openai --role encadrant --task task.md
    python3 tools/run_role.py --provider claude --role physicien --task - --dry-run

Use tools/call_model.py instead when the role needs no tools: its model and effort are then
checked at the API level. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from call_model import API_NOTE, ROOT, load_providers, load_role, resolve

READ_ONLY_NOTE = "\n\nYou never modify files of the repository; write scratch files only under /tmp.\n"


def build_command(provider: str, tier: str, level: str, max_turns: int, prompt: str):
    """Harness command and environment for one headless run with the given tier and level."""
    cfg = load_providers()[provider]
    h = cfg.get("harness")
    if not h:
        sys.exit(f"{provider}: no [harness] table in providers.toml")
    model, provider_effort = resolve(cfg, tier, level, api=False)
    effort = {"level": level, "provider": provider_effort, "none": None}[h["effort_source"]]
    fill = {"prompt": prompt, "model": model, "effort": effort or "", "max_turns": str(max_turns)}
    cmd = [part.format(**fill) for part in h["command"]]
    if effort is None:  # drop a flag whose value would be empty
        cmd = [c for i, c in enumerate(cmd) if not (c == "" or (i + 1 < len(cmd) and cmd[i + 1] == ""))]
    env = dict(os.environ)
    for k, v in h.get("env", {}).items():
        env[k] = os.path.expandvars(v.format(**fill))
    return cmd, env, model, effort, h


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", default=os.environ.get("MILADY_PROVIDER"))
    ap.add_argument("--role", required=True)
    ap.add_argument("--task", default="-", help="file with the task, or - for stdin")
    ap.add_argument("--timeout", type=int, default=7200, help="seconds")
    ap.add_argument("--dry-run", action="store_true", help="print the command, run nothing, log nothing")
    args = ap.parse_args()
    if not args.provider:
        ap.error("--provider (or MILADY_PROVIDER) is required")

    meta, body = load_role(args.role)
    task = sys.stdin.read() if args.task == "-" else Path(args.task).read_text(encoding="utf-8")
    note = API_NOTE.split("## How you are called")[0]  # keep the role text, drop the no-tools note
    prompt = f"{body.strip()}{note}{READ_ONLY_NOTE if meta['read_only'] else ''}\n## Task\n\n{task}"
    cmd, env, model, effort, h = build_command(args.provider, meta["tier"], meta["reasoning"],
                                               meta["max_turns"], prompt)

    shown = [c if c != prompt else f"<prompt {len(prompt)} chars>" for c in cmd]
    if args.dry_run:
        print(json.dumps({"command": shown, "env": sorted(h.get("env", {})), "model": model,
                          "effort": effort, "effort_support": h.get("effort_support")}, indent=2))
        return 0

    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S%fZ")
    try:
        r = subprocess.run(cmd, check=False, env=env, cwd=ROOT, capture_output=True, text=True, timeout=args.timeout,
                           stdin=subprocess.DEVNULL)  # codex exec and others wait on an open stdin
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        partial = e.stdout or ""
        rc, out, err = "timeout", partial.decode(errors="replace") if isinstance(partial, bytes) else partial, "timeout"
    except FileNotFoundError:
        sys.exit(f"harness not installed: {cmd[0]} (install: {h['install']})")

    reported = None
    try:
        last = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
        reported = last.get("model") or list((last.get("modelUsage") or {}).keys()) or None
    except (json.JSONDecodeError, AttributeError, IndexError):
        pass
    path = ROOT / "research" / "calls" / f"{stamp}-{args.provider}-{args.role}-harness.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"## Task\n\n{task}\n\n## Output (rc={rc})\n\n{out}\n\n## Stderr\n\n{err[-4000:]}\n",
                    encoding="utf-8")
    entry = {
        "time": stamp, "kind": "harness", "harness": h["name"], "provider": args.provider,
        "role": args.role, "tier": meta["tier"], "level": meta["reasoning"], "model": model,
        "effort": effort, "effort_support": h.get("effort_support"), "status": rc,
        "reported_model": reported, "command": shown, "answer_file": str(path.relative_to(ROOT)),
        "task_sha256": hashlib.sha256(task.encode()).hexdigest()[:16],
    }
    ledger = Path(os.environ.get("MILADY_LEDGER", ROOT / "research" / "model-calls.jsonl"))
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[{args.provider} {h['name']} {model} effort={effort} rc={rc} output={entry['answer_file']}]",
          file=sys.stderr)
    print(out)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
