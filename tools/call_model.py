#!/usr/bin/env python3
"""Call a role, or a tier, on a provider's API with the right model and reasoning effort.

Provider-neutral: the model id comes from the role's `tier` and the provider's [tier] table,
the effort value from the role's `reasoning` and the provider's [reasoning] table, and the
request shape from the provider's [api] table, all in agents/providers.toml. Every call is
appended to the ledger (default research/model-calls.jsonl) and the answer is saved under
research/calls/, so that tools/check_calls.py can verify, after the fact, which model and
which effort were really used.

    python3 tools/call_model.py --provider openai --role encadrant --task task.md
    echo "question" | python3 tools/call_model.py --provider claude --role physicien
    python3 tools/call_model.py --provider google --tier standard --reasoning low --task -

The role is called through the API without tools: put in the task everything it needs
(the claim, the code, the outputs of the commands you ran). Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROVIDERS = ROOT / "agents" / "providers.toml"
ROLES = ROOT / "agents" / "roles"
TIERS = ("frontier", "standard", "light")
LEVELS = ("low", "medium", "high", "max")
API_NOTE = (
    "\n\n## How you are called\n\nYou are called through an API, without tools: you cannot read "
    "files, run code or browse. Work only from the material in the task. Mark every check that "
    "would need a file, a command or a source you were not given as UNCHECKED, and say what the "
    "caller must run or send.\n"
)


def load_providers() -> dict:
    return tomllib.loads(PROVIDERS.read_text(encoding="utf-8"))


def load_role(name: str) -> tuple[dict, str]:
    sys.path.insert(0, str(ROOT / "tools"))
    from sync_agents import parse_role

    return parse_role(ROLES / f"{name}.md")


def resolve(cfg: dict, tier: str, level: str, api: bool = True) -> tuple[str, object]:
    """Model id for a tier (nearest higher tier first, then lower) and effort value for a level
    (nearest higher level first, then lower). api=False ignores [api].models (harness names)."""
    table = (cfg.get("api", {}).get("models") if api else None) or cfg["tier"]
    order = list(TIERS[: TIERS.index(tier) + 1])[::-1] + list(TIERS[TIERS.index(tier) + 1 :])
    model = next((table[t] for t in order if t in table), None)
    if model is None:
        sys.exit(f"no model for tier {tier}")
    levels = cfg.get("reasoning", {})
    later = list(LEVELS[LEVELS.index(level) :])
    earlier = list(LEVELS[: LEVELS.index(level)])[::-1]
    effort = next((levels[x] for x in later + earlier if x in levels), None)
    return model, effort


def set_path(body: dict, dotted: str, value) -> None:
    keys = dotted.split(".")
    for k in keys[:-1]:
        body = body.setdefault(k, {})
    body[keys[-1]] = value


def merge(dst: dict, src: dict) -> dict:
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            merge(dst[k], v)
        else:
            dst[k] = v
    return dst


def build(api: dict, model: str, effort, system: str, task: str, max_tokens: int):
    style = api["style"]
    base = os.environ.get("MILADY_BASE_URL", api["base_url"]).rstrip("/")  # override: tests, logging proxy
    key = os.environ.get(api["key_env"], "")
    if style == "anthropic":
        url = f"{base}/messages"
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
        body = {"model": model, "max_tokens": max_tokens, "system": system,
                "messages": [{"role": "user", "content": task}]}
    elif style == "openai-responses":
        url = f"{base}/responses"
        headers = {"Authorization": f"Bearer {key}"}
        body = {"model": model, "instructions": system, "input": task, "max_output_tokens": max_tokens}
    elif style == "openai-chat":
        url = f"{base}/chat/completions"
        headers = {"Authorization": f"Bearer {key}"}
        body = {"model": model, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": task}]}
    elif style == "gemini":
        url = f"{base}/models/{model}:generateContent"
        headers = {"x-goog-api-key": key}
        body = {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": task}]}],
                "generationConfig": {"maxOutputTokens": max_tokens}}
    else:
        sys.exit(f"unknown api style {style!r}")
    merge(body, json.loads(json.dumps(api.get("extra", {}))))
    if effort is not None and api.get("effort_field"):
        set_path(body, api["effort_field"], effort)
    headers["Content-Type"] = "application/json"
    return url, headers, body


def parse(style: str, data: dict) -> dict:
    """Text, model echoed by the API, and token counts (None when the API does not report them)."""
    if style == "anthropic":
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        u = data.get("usage", {})
        return {"text": text, "model": data.get("model"), "input_tokens": u.get("input_tokens"),
                "output_tokens": u.get("output_tokens"), "reasoning_tokens": None}
    if style == "openai-responses":
        text = "".join(c.get("text", "") for o in data.get("output", []) for c in o.get("content", []) or []
                       if c.get("type") == "output_text")
        u = data.get("usage", {})
        return {"text": text, "model": data.get("model"), "input_tokens": u.get("input_tokens"),
                "output_tokens": u.get("output_tokens"),
                "reasoning_tokens": (u.get("output_tokens_details") or {}).get("reasoning_tokens")}
    if style == "openai-chat":
        msg = (data.get("choices") or [{}])[0].get("message", {})
        u = data.get("usage", {})
        return {"text": msg.get("content") or "", "model": data.get("model"),
                "input_tokens": u.get("prompt_tokens"), "output_tokens": u.get("completion_tokens"),
                "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens")}
    cand = (data.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []) if not p.get("thought"))
    u = data.get("usageMetadata", {})
    return {"text": text, "model": data.get("modelVersion"), "input_tokens": u.get("promptTokenCount"),
            "output_tokens": u.get("candidatesTokenCount"), "reasoning_tokens": u.get("thoughtsTokenCount")}


def call(provider: str, tier: str, level: str, system: str, task: str, *, role: str | None = None,
         max_tokens: int = 16000, timeout: int = 1800, ledger: Path | None = None, save: bool = True) -> dict:
    cfg = load_providers()[provider]
    api = cfg["api"]
    model, effort = resolve(cfg, tier, level)
    url, headers, body = build(api, model, effort, system, task, max_tokens)
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    t0 = time.time()
    status, data, error = None, {}, None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, data = r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        status, error = e.code, e.read().decode(errors="replace")[:2000]
    except (urllib.error.URLError, TimeoutError) as e:
        error = str(e)
    out = parse(api["style"], data) if data else {"text": "", "model": None, "input_tokens": None,
                                                    "output_tokens": None, "reasoning_tokens": None}
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S%fZ")
    entry = {
        "time": stamp, "provider": provider, "role": role, "tier": tier, "level": level,
        "model": model, "effort_field": api.get("effort_field"), "effort": effort,
        "status": status, "error": error, "response_model": out["model"],
        "input_tokens": out["input_tokens"], "output_tokens": out["output_tokens"],
        "reasoning_tokens": out["reasoning_tokens"], "seconds": round(time.time() - t0, 1),
        "task_sha256": hashlib.sha256(task.encode()).hexdigest()[:16],
    }
    if save and out["text"]:
        path = ROOT / "research" / "calls" / f"{stamp}-{provider}-{role or tier}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"<!-- {json.dumps(entry)} -->\n\n## Task\n\n{task}\n\n## Answer\n\n{out['text']}\n",
                        encoding="utf-8")
        entry["answer_file"] = str(path.relative_to(ROOT))
    ledger = ledger or Path(os.environ.get("MILADY_LEDGER", ROOT / "research" / "model-calls.jsonl"))
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    entry["text"] = out["text"]
    return entry


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", default=os.environ.get("MILADY_PROVIDER"), help="section of providers.toml")
    ap.add_argument("--role", help="agents/roles/<role>.md: gives tier, reasoning and system prompt")
    ap.add_argument("--tier", choices=TIERS, help="instead of --role (with --reasoning)")
    ap.add_argument("--reasoning", choices=LEVELS)
    ap.add_argument("--task", default="-", help="file with the task, or - for stdin")
    ap.add_argument("--max-tokens", type=int, default=16000)
    args = ap.parse_args()
    if not args.provider:
        ap.error("--provider (or MILADY_PROVIDER) is required")
    if args.role:
        meta, body = load_role(args.role)
        tier, level, system = meta["tier"], meta["reasoning"], body.strip() + API_NOTE
    elif args.tier and args.reasoning:
        tier, level, system = args.tier, args.reasoning, "You are a careful research assistant."
    else:
        ap.error("give --role, or --tier and --reasoning")
    task = sys.stdin.read() if args.task == "-" else Path(args.task).read_text(encoding="utf-8")
    e = call(args.provider, tier, level, system, task, role=args.role, max_tokens=args.max_tokens)
    print(f"[{e['provider']} {e['model']} effort={e['effort']} status={e['status']} "
          f"reasoning_tokens={e['reasoning_tokens']} answer={e.get('answer_file')}]", file=sys.stderr)
    if e["error"]:
        print(e["error"], file=sys.stderr)
        return 1
    print(e["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
