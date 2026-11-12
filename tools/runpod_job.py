#!/usr/bin/env python3
"""Run one command of this repository on a RunPod GPU pod, collect its outputs, delete the pod.

The pod clones the public repository at a pushed commit, installs the pinned dependencies
(keeping the image's CUDA build of torch), runs the command under a time limit, packs the
outputs and serves them over HTTP under a random path; this tool polls through the RunPod
proxy, extracts the outputs into the checkout and deletes the pod in every case. Each job is
appended to research/compute-ledger.jsonl with GPU type, hourly price, duration and cost.

RunPod is reached through its MCP server (https://mcp.runpod.io/); in a Claude Code cloud
session of the milady-2027 environment the network proxy injects the API key, so no key is
read here. Standard library only.

    python3 tools/runpod_job.py run --hours 1.5 -- python -m milady.sim.mhd3d bench --n 64 --device cuda
    python3 tools/runpod_job.py run --gpu "NVIDIA H100 80GB HBM3" --hours 1 --outputs experiments/results -- CMD
    python3 tools/runpod_job.py prices        # hourly price and stock of the configured GPUs
    python3 tools/runpod_job.py spend         # GPU spend so far, from the ledger
    python3 tools/runpod_job.py cleanup       # delete this team's pods past their time limit (milady-<team>-job-*)
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import io
import json
import os
import re
import secrets
import subprocess
import sys
import tarfile
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "race" / "config.toml"
LEDGER = ROOT / "research" / "compute-ledger.jsonl"
MCP_URL = os.environ.get("RUNPOD_MCP_URL", "https://mcp.runpod.io/")
USER_AGENT = "milady-runpod-job/1"
# Live pods of every team that reserve the shared credit, including the legacy unscoped name.
_ACCOUNT_JOB = re.compile(r"^milady-(?:[A-Za-z0-9_-]+-)?job-")


def job_prefix() -> str:
    """Pod name prefix for this session: ``milady-<MILADY_TEAM>-job-``, default ``milady-cursor-job-``.

    ``cleanup`` deletes only this prefix. A shared ``milady-job-`` prefix let one session delete
    another team's running pods (pilot, 2026-11-12).
    """
    team = (os.environ.get("MILADY_TEAM") or "cursor").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", team):
        team = "cursor"
    return f"milady-{team}-job-"


def is_account_job(name: str) -> bool:
    """True for ``milady-<team>-job-*`` and the legacy ``milady-job-*`` pods. Used for the shared budget."""
    return _ACCOUNT_JOB.match(str(name)) is not None


BOOTSTRAP = r"""
set -u
OUT=/srv/www/$JOB_TOKEN; mkdir -p "$OUT"; : > /srv/www/index.html
status() { echo "$(date -u +%FT%TZ) $*" >> "$OUT/status.txt"; }
(cd /srv/www && nohup python3 -m http.server 8000 >/dev/null 2>&1 &)
status "boot $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1)"
exec >> "$OUT/setup.log" 2>&1
cd /workspace && git clone -q "$REPO" milady && cd milady && git checkout -q "$REF" || { status "FAILED clone"; sleep infinity; }
grep -vE '^(torch==|--extra-index-url|--index-url)' infra/env/requirements.txt > /tmp/req.txt
# The image ships Debian-installed packages (pyparsing...) that pip cannot uninstall: install the pins
# in a virtual environment that still sees the image's CUDA torch, or else on top of the system ones.
if python3 -m venv --system-site-packages /opt/milady-venv; then . /opt/milady-venv/bin/activate; fi
{ pip install -q -r /tmp/req.txt || pip install -q --ignore-installed -r /tmp/req.txt; } \
  && pip install -q --no-deps -e . || { status "FAILED pip"; sleep infinity; }
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())" >> "$OUT/setup.log"
status "job started"
echo "$CMD_B64" | base64 -d > /tmp/job.sh
T0=$(date +%s)
timeout "${MAX_MIN}m" bash /tmp/job.sh > "$OUT/job.log" 2>&1; rc=$?
status "job finished rc=$rc in $(( $(date +%s) - T0 )) s"
tar -czf "$OUT/results.tar.gz" --ignore-failed-read $OUTPUTS 2>>"$OUT/setup.log"
status "DONE rc=$rc"
sleep infinity
"""


def config() -> dict:
    return tomllib.loads(CONFIG.read_text(encoding="utf-8")).get("gpu", {})


class MCP:
    """Minimal client of the RunPod MCP server (JSON-RPC over HTTP)."""

    def __init__(self, url: str = MCP_URL):
        self.url, self.sid, self.n = url, None, 0
        self._post({"jsonrpc": "2.0", "id": 0, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "milady-runpod-job", "version": "1"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _post(self, body: dict) -> dict:
        headers = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json",
                   "Authorization": f"Bearer {os.environ.get('RUNPOD_API_KEY', 'proxy-injected')}"}
        if self.sid:
            headers["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            text = r.read().decode()
            self.sid = r.headers.get("Mcp-Session-Id") or self.sid
        data = re.findall(r"^data: (.*)$", text, re.MULTILINE)
        return json.loads(data[-1]) if data else (json.loads(text) if text.strip() else {})

    def call(self, tool: str, args: dict) -> dict | list:
        self.n += 1
        res = self._post({"jsonrpc": "2.0", "id": self.n, "method": "tools/call",
                          "params": {"name": tool, "arguments": args}})
        res = res.get("result", res)
        text = "".join(c.get("text", "") for c in res.get("content", []))
        if res.get("isError"):
            raise RuntimeError(f"{tool}: {text[:500]}")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"text": text}


def gpu_catalog(mcp: MCP, cloud: str = "SECURE") -> dict[str, dict]:
    data = mcp.call("list-gpu-types", {"include": ["AVAILABILITY"], "product": ["POD"], "cloud": cloud})
    items = next(iter(data.values())) if isinstance(data, dict) else data
    return {g["id"]: g for g in items}


def ledger_append(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def http_get(url: str) -> bytes | None:
    """GET through the RunPod HTTP proxy. The proxy (Cloudflare) answers 403, error 1010, to the default
    ``Python-urllib`` agent: without an explicit User-Agent the job status is never read (pilot, 2026-11-12)."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=60) as r:
            return r.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def pushed_commit(ref: str) -> str:
    sha = subprocess.check_output(["git", "rev-parse", ref], cwd=ROOT, text=True).strip()
    remote = subprocess.run(["git", "branch", "-r", "--contains", sha], cwd=ROOT, capture_output=True,
                            text=True, check=False).stdout.strip()
    if not remote:
        sys.exit(f"commit {sha[:12]} is not on any remote branch: push it first, the pod clones from GitHub")
    return sha


def run(args, mcp: MCP | None = None, sleep=time.sleep) -> int:
    cfg = config()
    hours = float(args.hours)
    if not 0 < hours <= cfg.get("max_job_hours", 2):
        sys.exit(f"--hours must be in (0, {cfg.get('max_job_hours', 2)}]")
    command = " ".join(args.command[1:] if args.command[:1] == ["--"] else args.command)
    if not command:
        sys.exit("give the command after --")
    budget = float(os.environ.get("MILADY_GPU_BUDGET_USD") or cfg.get("budget_usd") or 0)  # this team's share
    spent = spend()["usd"]
    share = cfg.get("approval_fraction", 0.8)
    if budget and share < 1 and spent >= share * budget and not args.over_budget_approved:
        sys.exit(f"GPU spend ${spent:.2f} is at or above {share:.0%} of the ${budget} budget: no new job without the "
                 "owner's approval (then pass --over-budget-approved)")
    sha = pushed_commit(args.ref)
    gpus = [g.strip() for g in (args.gpu or ",".join(cfg.get("fallback", []))).split(",") if g.strip()]
    outputs = args.outputs or cfg.get("outputs", ["experiments/results"])
    mcp = mcp or MCP()
    credit = cfg.get("credit_usd")  # the prepaid RunPod credit, shared by every team using the account
    account = account_spend(mcp) if credit else None
    if account is not None:
        print(f"RunPod account spend (all teams, billing may lag): ${account:.2f} of ${credit} credit",
              file=sys.stderr)
    jobs = running_jobs(mcp)  # other jobs of this tool in flight (any session): their worst case is reserved
    limit = int(cfg.get("max_parallel", 4))
    if len(jobs) >= limit:
        print(f"{len(jobs)} GPU jobs already running (limit [gpu].max_parallel = {limit}): wait for one to end",
              file=sys.stderr)
        return 1
    reserved = sum(j["reserved_usd"] for j in jobs)
    if jobs:
        print(f"{len(jobs)} job(s) in flight, ${reserved:.2f} reserved for their worst case", file=sys.stderr)
    token = secrets.token_hex(16)
    prefix = job_prefix()
    env = {"JOB_TOKEN": token, "REPO": cfg.get("repo", "https://github.com/knoel99/milady-2027.git"),
           "REF": sha, "CMD_B64": base64.b64encode(command.encode()).decode(),
           "OUTPUTS": " ".join(outputs), "MAX_MIN": str(int(hours * 60))}
    pod = gpu = None
    price = 0.0
    # Stock reads are unreliable both ways (LOW refuses, NONE sometimes accepts) and a refused create is free:
    # try every GPU of the list on each cloud in turn.
    for cloud in cfg.get("clouds", ["SECURE"]):
        catalog = gpu_catalog(mcp, cloud)
        for gid in gpus:
            g = catalog.get(gid)
            if not g:
                print(f"skip {gid} ({cloud}): not in the catalog", file=sys.stderr)
                continue
            listed = float(g["price"].get(cloud.lower()) or 0)
            if not g.get(cloud.lower(), True) or listed <= 0:  # the catalog shows placeholder prices off a cloud
                print(f"skip {gid} ({cloud}): not offered on this cloud", file=sys.stderr)
                continue
            worst = hours * listed
            if account is not None and account + reserved + worst > credit - cfg.get("credit_margin_usd", 5) \
                    and not args.over_budget_approved:
                print(f"skip {gid} ({cloud}): up to ${worst:.2f} would exhaust the shared RunPod credit "
                      f"(${account:.2f} of ${credit} billed)", file=sys.stderr)
                continue
            if budget and spent + reserved + worst > budget and not args.over_budget_approved:
                print(f"skip {gid} ({cloud}): up to ${worst:.2f} would exceed the ${budget} budget "
                      f"(${spent:.2f} spent, ${reserved:.2f} reserved by running jobs)", file=sys.stderr)
                continue
            body = {"name": f"{prefix}{token[:8]}", "cloud": cloud, "image": cfg.get("image"),
                    "gpu": {"id": gid, "count": 1, "minCudaVersion": cfg.get("min_cuda", "12.8")},
                    "disk": int(cfg.get("disk_gb", 40)), "ports": ["8000/http"], "env": env,
                    "entrypoint": ["/bin/bash", "-c"], "cmd": [BOOTSTRAP]}
            attempts = [dict(body, dataCenterIds=cfg["data_centers"]), body] if (
                cloud == "SECURE" and cfg.get("data_centers")) else [body]
            for attempt in attempts:
                try:
                    pod, gpu = mcp.call("create-pod", {"body": attempt}), g
                    break
                except RuntimeError as e:
                    where = "preferred data centers" if "dataCenterIds" in attempt else "any data center"
                    print(f"create-pod on {gid} ({cloud}, {where}) failed: {str(e)[:160]}", file=sys.stderr)
            if pod:
                cost = pod.get("cost") if isinstance(pod, dict) else None
                price = float(cost) if isinstance(cost, (int, float)) and cost > 0 else listed
                break
        if pod:
            break
    if not pod:
        print("no GPU could be rented: nothing billed", file=sys.stderr)
        return 1
    pid = pod.get("id") or (pod.get("pod") or {}).get("id") if isinstance(pod, dict) else None
    if not pid:  # unknown response shape: find the pod by its unique name, delete it, stop
        name = f"{prefix}{token[:8]}"
        found = mcp.call("list-pods", {})
        for p in (found.get("pods", []) if isinstance(found, dict) else found):
            if p.get("name") == name:
                mcp.call("delete-pod", {"id": p["id"]})
                print(f"deleted pod {p['id']}", file=sys.stderr)
        sys.exit(f"create-pod answered without a pod id ({str(pod)[:200]}); pod {name} looked up and deleted")
    t0 = time.time()
    print(f"pod {pid} on {gpu['id']} at ${price}/h; limit {hours} h; commit {sha[:12]}", file=sys.stderr)
    base = f"https://{pid}-8000.proxy.runpod.net/{token}/"
    rc, status = None, ""
    try:
        while True:
            sleep(30)
            raw = http_get(base + "status.txt")
            status = raw.decode(errors="replace") if raw else status
            m = re.search(r"DONE rc=(\d+)", status)
            if m:
                rc = int(m.group(1))
                break
            if "FAILED" in status:
                break
            if time.time() - t0 > (hours + 0.25) * 3600:
                status += "\nTIMEOUT: pod deleted by runpod_job.py"
                break
        data = http_get(base + "results.tar.gz")
        if data:
            with tarfile.open(fileobj=io.BytesIO(data)) as tar:
                tar.extractall(ROOT, filter="data")
        logs = http_get(base + "job.log") or b""
        setup = b""
        if rc != 0:  # the job did not run or failed: bring back the end of the set-up log (clone, pip)
            setup = b"\n--- setup (tail)\n" + (http_get(base + "setup.log") or b"")[-4000:]
        Path(args.log).parent.mkdir(parents=True, exist_ok=True)
        Path(args.log).write_bytes(logs + setup + b"\n--- status\n" + status.encode())
    finally:
        try:
            mcp.call("delete-pod", {"id": pid})
        except RuntimeError as e:
            print(f"DELETE FAILED for pod {pid}: {e}. Delete it by hand, it is still billing.", file=sys.stderr)
        hours_used = (time.time() - t0) / 3600
        ledger_append({"time": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "pod": pid,
                       "gpu": gpu["id"], "usd_per_hour": price, "hours": round(hours_used, 4),
                       "usd": round(hours_used * price, 4), "commit": sha, "command": command, "rc": rc,
                       "status_tail": status[-300:]})
    print(f"rc={rc}; {hours_used:.2f} h; ${hours_used * price:.2f}; log {args.log}", file=sys.stderr)
    print("The outputs are only in this checkout: commit and push them now, with research/compute-ledger.jsonl.",
          file=sys.stderr)
    return 0 if rc == 0 else 1


def running_jobs(mcp, now: float | None = None) -> list[dict]:
    """Live job pods of every team, with the dollars their time limit can still cost (plus the 15 min grace).

    The shared credit is one account, so a Claude pod (``milady-claude-job-*``) and a legacy
    ``milady-job-*`` pod count here. ``cleanup`` does not delete them.
    """
    now = now or time.time()
    found = mcp.call("list-pods", {})
    out = []
    for p in (found.get("pods", []) if isinstance(found, dict) else found or []):
        if not is_account_job(str(p.get("name", ""))):
            continue
        limit_h = int((p.get("env") or {}).get("MAX_MIN", 120)) / 60 + 0.25
        try:
            age_h = (now - dt.datetime.fromisoformat(p["createdAt"]).timestamp()) / 3600
        except (KeyError, ValueError):
            age_h = 0.0
        out.append({"id": p.get("id"), "name": p.get("name"), "age_h": age_h, "limit_h": limit_h,
                    "reserved_usd": float(p.get("cost") or 0) * max(0.0, limit_h - age_h)})
    return out


def account_spend(mcp) -> float | None:
    """Total billed on the RunPod account over the last 30 days, all teams; None if unreadable."""
    try:
        data = mcp.call("list-billing", {"lastN": 30, "bucketSize": "day"})
        return float(data["metadata"]["totals"]["totalAmount"])
    except (RuntimeError, KeyError, TypeError, ValueError):
        return None


def spend() -> dict:
    rows = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()] if LEDGER.exists() else []
    by_gpu: dict[str, dict] = {}
    for r in rows:
        g = by_gpu.setdefault(r["gpu"], {"jobs": 0, "hours": 0.0, "usd": 0.0})
        g["jobs"] += 1
        g["hours"] += r["hours"]
        g["usd"] += r["usd"]
    return {"jobs": len(rows), "hours": round(sum(r["hours"] for r in rows), 3),
            "usd": round(sum(r["usd"] for r in rows), 2), "by_gpu": by_gpu,
            "budget_usd": float(os.environ.get("MILADY_GPU_BUDGET_USD") or config().get("budget_usd") or 0)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--hours", required=True, help="wall-clock limit of the job")
    r.add_argument("--gpu", help="comma-separated catalog ids, tried in order (default: [gpu].fallback)")
    r.add_argument("--ref", default="HEAD", help="commit to run; must be pushed")
    r.add_argument("--outputs", nargs="*", help="paths to bring back (default: [gpu].outputs)")
    r.add_argument("--log", default=str(ROOT / "research" / "gpu-logs" / "last-job.log"))
    r.add_argument("--over-budget-approved", action="store_true", help="the owner approved spending past the budget")
    r.add_argument("command", nargs=argparse.REMAINDER)
    sub.add_parser("prices")
    sub.add_parser("spend")
    c = sub.add_parser("cleanup", help="delete pods of this tool past their time limit (orphans of a crashed run)")
    c.add_argument("--all", action="store_true", help="also delete pods whose job may still be running")
    a = ap.parse_args()
    if a.cmd == "run":
        return run(a)
    if a.cmd == "spend":
        s = spend()
        print(json.dumps(s, indent=1))
        if s["budget_usd"] and s["usd"] > 0.8 * s["budget_usd"]:
            print("WARNING: more than 80 % of the GPU budget spent", file=sys.stderr)
        return 0
    mcp = MCP()
    if a.cmd == "prices":
        for cloud in config().get("clouds", ["SECURE"]):
            cat = gpu_catalog(mcp, cloud)
            for gid in config().get("fallback", []):
                g = cat.get(gid, {})
                print(f"{cloud:<9} {gid:<48} ${g.get('price', {}).get(cloud.lower())}/h  stock {g.get('availability')}")
        return 0
    return cleanup(mcp, delete_running=a.all)


def cleanup(mcp, delete_running: bool = False) -> int:
    """Delete this team's pods past their time limit. Other teams and legacy ``milady-job-*`` stay."""
    own = job_prefix()
    jobs = running_jobs(mcp)
    mine = [j for j in jobs if str(j.get("name", "")).startswith(own)]
    # ``limit_h`` already includes 15 min. The extra 0.25 h is the same grace as before.
    gone = mine if delete_running else [j for j in mine if j["age_h"] > j["limit_h"] + 0.25]
    for j in gone:
        mcp.call("delete-pod", {"id": j["id"]})
        print(f"deleted {j['id']} {j['name']} (age {j['age_h']:.2f} h, limit {j['limit_h']:.2f} h)")
    print(f"{len(gone)} pod(s) deleted; {len(mine) - len(gone)} of this team's pods still within their time limit kept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
