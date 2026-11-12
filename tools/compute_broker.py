#!/usr/bin/env python3
"""Compute broker of the race: per-team CPU quota, shared cache of identical runs, and no cloud
credential on the teams' machines.

The broker runs on the user's coordinator machine, which alone holds the Scaleway key. A team
sends an archive of its code and one command; the broker computes a cache key from the code
that can change the result (experiments/, src/, infra/env/, pyproject.toml), the command, the
outputs and the machine type. If any team already ran exactly that, the cached outputs are
returned at no cost. Otherwise the broker checks the team's remaining vCPU-hours, starts a job
VM (infra/deploy/race-job.sh), collects its outputs, deletes the VM and charges the vCPU-hours
actually used.

Coordinator:
    python3 tools/compute_broker.py tokens --state DIR          # one secret per team (print once)
    SCW_SECRET_KEY=... python3 tools/compute_broker.py serve --state DIR --public-url http://IP:8080
Team machine (BROKER_URL, BROKER_TOKEN and MILADY_PROVIDER set by the launcher):
    python3 tools/compute_broker.py submit --hours 1.5 -- python3 experiments/e4.py --seed 3
    python3 tools/compute_broker.py status JOB
    python3 tools/compute_broker.py fetch JOB            # extracts the outputs into the checkout
    python3 tools/compute_broker.py quota

Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import secrets
import subprocess
import sys
import tarfile
import threading
import time
import tomllib
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "race" / "config.toml"
JOB_SCRIPT = ROOT / "infra" / "deploy" / "race-job.sh"
KEY_PATHS = ("experiments/", "src/", "infra/env/", "pyproject.toml")
ARCHIVE_PATHS = ["experiments", "src", "infra", "tools", "agents", "pyproject.toml"]
DEFAULT_OUTPUTS = ["experiments/results", "site/experiments/figures"]
NCPUS = {"POP2-HC-16C-32G": 16, "POP2-HC-8C-16G": 8, "POP2-4C-16G": 4, "POP2-2C-8G": 2}


def config() -> dict:
    return tomllib.loads(CONFIG.read_text(encoding="utf-8"))


def cache_key(archive: bytes, command: str, outputs: list[str], vm_type: str) -> str:
    """Hash of the files that can change the result, plus command, outputs and machine type."""
    h = hashlib.sha256()
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        members = sorted((m for m in tar.getmembers() if m.isfile() and m.name.startswith(KEY_PATHS)),
                         key=lambda m: m.name)
        for m in members:
            data = tar.extractfile(m).read()
            h.update(m.name.encode() + b"\0" + hashlib.sha256(data).digest())
    h.update(json.dumps([command, sorted(outputs), vm_type]).encode())
    return h.hexdigest()[:32]


class Scaleway:
    """The three cloud operations the broker needs, on top of infra/deploy/scaleway.py."""

    def __init__(self, zone: str):
        sys.path.insert(0, str(ROOT / "infra" / "deploy"))
        import scaleway

        self.s, self.zone = scaleway, zone

    def create(self, name: str, user_data: str, vm_type: str) -> str:
        s, z = self.s, self.zone
        body = {"name": name, "commercial_type": vm_type, "image": s.image_id(z, vm_type),
                "project": s.project_id(), "tags": [s.TAG, "race"], "dynamic_ip_required": True,
                "volumes": {"0": {"size": 40 * 10**9, "volume_type": "sbs_volume"}}}
        sid = s.call("POST", f"{s.inst(z)}/servers", body)["server"]["id"]
        s.call("PATCH", f"{s.inst(z)}/servers/{sid}/user_data/cloud-init", user_data, "text/plain")
        s.call("POST", f"{s.inst(z)}/servers/{sid}/action", {"action": "poweron"})
        return sid

    def ip(self, sid: str) -> str | None:
        srv = self.s.call("GET", f"{self.s.inst(self.zone)}/servers/{sid}")["server"]
        return (srv.get("public_ip") or {}).get("address")

    def get(self, url: str) -> bytes:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()

    def delete(self, sid: str) -> None:
        self.s.cmd_delete(argparse.Namespace(zone=self.zone, server=sid))


class Broker:
    def __init__(self, state: Path, public_url: str, cloud, cfg: dict | None = None):
        self.dir, self.public_url, self.cloud = state, public_url.rstrip("/"), cloud
        self.cfg = cfg or config()
        for sub in ("archives", "cache"):
            (state / sub).mkdir(parents=True, exist_ok=True)
        self.tokens = json.loads((state / "tokens.json").read_text())
        self.db_path = state / "jobs.json"
        self.db = json.loads(self.db_path.read_text()) if self.db_path.exists() else {"jobs": {}}
        self.lock = threading.Lock()

    def save(self) -> None:
        tmp = self.db_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.db, indent=1))
        tmp.replace(self.db_path)

    def team_of(self, token: str) -> str | None:
        return next((t for t, s in self.tokens.items() if secrets.compare_digest(s, token or "")), None)

    def used(self, team: str) -> tuple[float, float]:
        """vCPU-hours charged and vCPU-hours reserved by running jobs."""
        jobs = [j for j in self.db["jobs"].values() if j["team"] == team]
        charged = sum(j.get("charged", 0.0) for j in jobs)
        reserved = sum(j["ncpus"] * j["hours"] for j in jobs if j["state"] == "running")
        return charged, reserved

    def submit(self, team: str, req: dict) -> dict:
        b = self.cfg["budget"]
        vm_type = self.cfg["machines"]["job_vm"]
        hours = float(req.get("hours", 1))
        if not 0 < hours <= b["max_job_hours"]:
            return {"error": f"hours must be in (0, {b['max_job_hours']}]"}
        archive = base64.b64decode(req["archive"])
        command = req["command"]
        outputs = req.get("outputs") or DEFAULT_OUTPUTS
        key = cache_key(archive, command, outputs, vm_type)
        with self.lock:
            jid = f"{team}-{int(time.time())}-{secrets.token_hex(3)}"
            job = {"id": jid, "team": team, "key": key, "command": command, "outputs": outputs,
                   "vm_type": vm_type, "ncpus": NCPUS.get(vm_type, 16), "hours": hours,
                   "submitted": time.time()}
            if (self.dir / "cache" / f"{key}.tar.gz").exists():
                job.update(state="done", cached=True, charged=0.0)
            else:
                charged, reserved = self.used(team)
                need = job["ncpus"] * hours
                if charged + reserved + need > b["cpu_hours"]:
                    return {"error": f"quota: {charged:.1f} used + {reserved:.1f} reserved + {need:.1f} "
                                     f"requested > {b['cpu_hours']} vCPU-hours"}
                (self.dir / "archives" / f"{key}.tar").write_bytes(archive)
                token = secrets.token_hex(16)
                script = JOB_SCRIPT.read_text()
                for k, v in {"__TOKEN__": token,
                             "__ARCHIVE_URL__": f"{self.public_url}/archives/{key}?t={token}",
                             "__COMMAND__": base64.b64encode(command.encode()).decode(),
                             "__OUTPUTS__": " ".join(outputs),
                             "__MAX_MIN__": str(int(hours * 60) + 15)}.items():
                    script = script.replace(k, v)
                job.update(state="running", cached=False, token=token, started=time.time(),
                           server=self.cloud.create(f"race-{jid}", script, vm_type))
            self.db["jobs"][jid] = job
            self.save()
        return self.public(job)

    @staticmethod
    def public(job: dict) -> dict:
        return {k: v for k, v in job.items() if k not in ("token",)}

    def poll(self) -> None:
        """Collect finished jobs, delete their VMs and charge the vCPU-hours used."""
        for job in [j for j in self.db["jobs"].values() if j["state"] == "running"]:
            ip = self.cloud.ip(job["server"])
            status = ""
            if ip:
                try:
                    status = self.cloud.get(f"http://{ip}:8000/{job['token']}/status.txt").decode()
                except (urllib.error.URLError, OSError):
                    status = ""
            overdue = time.time() - job["started"] > (job["hours"] + 0.5) * 3600
            if "DONE" not in status and "FAILED" not in status and not overdue:
                continue
            ok = "DONE rc=0" in status
            if ip:
                try:
                    data = self.cloud.get(f"http://{ip}:8000/{job['token']}/results.tar.gz")
                    name = f"{job['key']}.tar.gz" if ok else f"{job['id']}-failed.tar.gz"
                    (self.dir / "cache" / name).write_bytes(data)
                except (urllib.error.URLError, OSError):
                    ok = False
            self.cloud.delete(job["server"])
            with self.lock:
                job["ended"] = time.time()
                job["charged"] = round(job["ncpus"] * (job["ended"] - job["started"]) / 3600, 3)
                job["state"] = "done" if ok else "failed"
                job["status_tail"] = status[-500:]
                self.save()

    def results(self, job: dict) -> bytes | None:
        name = f"{job['key']}.tar.gz" if job["state"] == "done" else f"{job['id']}-failed.tar.gz"
        path = self.dir / "cache" / name
        return path.read_bytes() if path.exists() else None


def make_handler(broker: Broker):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, code: int, obj=None, raw: bytes | None = None):
            data = raw if raw is not None else json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/octet-stream" if raw is not None else "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def team(self):
            return broker.team_of(self.headers.get("Authorization", "").removeprefix("Bearer "))

        def do_GET(self):
            path, _, query = self.path.partition("?")
            parts = path.strip("/").split("/")
            if parts[0] == "archives" and len(parts) == 2:  # fetched by a job VM with its own token
                job = next((j for j in broker.db["jobs"].values() if j["key"] == parts[1]
                            and query == f"t={j.get('token')}" and j["state"] == "running"), None)
                f = broker.dir / "archives" / f"{parts[1]}.tar"
                return self.reply(200, raw=f.read_bytes()) if job and f.exists() else self.reply(404, {})
            team = self.team()
            if not team:
                return self.reply(401, {"error": "bad token"})
            if parts == ["quota"]:
                charged, reserved = broker.used(team)
                return self.reply(200, {"team": team, "charged": round(charged, 2), "reserved": reserved,
                                        "quota": broker.cfg["budget"]["cpu_hours"]})
            if parts[0] == "jobs" and len(parts) >= 2:
                job = broker.db["jobs"].get(parts[1])
                if not job or job["team"] != team:
                    return self.reply(404, {"error": "no such job"})
                if len(parts) == 3 and parts[2] == "results":
                    data = broker.results(job)
                    return self.reply(200, raw=data) if data else self.reply(404, {"error": "no results yet"})
                return self.reply(200, broker.public(job))
            return self.reply(404, {})

        def do_POST(self):
            team = self.team()
            if not team:
                return self.reply(401, {"error": "bad token"})
            if self.path.rstrip("/") != "/jobs":
                return self.reply(404, {})
            req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            out = broker.submit(team, req)
            return self.reply(400 if "error" in out else 200, out)

        def log_message(self, *args):
            pass

    return Handler


def client(method: str, path: str, body: dict | None = None) -> tuple[int, bytes]:
    url = os.environ["BROKER_URL"].rstrip("/") + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {os.environ['BROKER_TOKEN']}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("tokens")
    s.add_argument("--state", type=Path, required=True)
    s = sub.add_parser("serve")
    s.add_argument("--state", type=Path, required=True)
    s.add_argument("--public-url", required=True, help="URL at which job VMs reach this broker")
    s.add_argument("--port", type=int, default=8080)
    s = sub.add_parser("submit")
    s.add_argument("--hours", type=float, required=True, help="wall-clock limit of the job")
    s.add_argument("--outputs", nargs="*", default=None, help=f"paths to collect (default {DEFAULT_OUTPUTS})")
    s.add_argument("command", nargs=argparse.REMAINDER)
    sub.add_parser("status").add_argument("job")
    sub.add_parser("fetch").add_argument("job")
    sub.add_parser("quota")
    a = ap.parse_args()

    if a.cmd == "tokens":
        a.state.mkdir(parents=True, exist_ok=True)
        path = a.state / "tokens.json"
        tokens = json.loads(path.read_text()) if path.exists() else {}
        for team in config()["teams"]:
            tokens.setdefault(team, secrets.token_hex(24))
        path.write_text(json.dumps(tokens, indent=1))
        path.chmod(0o600)
        print(f"{len(tokens)} tokens in {path}")
        return 0
    if a.cmd == "serve":
        broker = Broker(a.state, a.public_url, Scaleway(config()["machines"]["zone"]))

        def loop():
            while True:
                try:
                    broker.poll()
                except Exception as e:  # noqa: BLE001  keep serving; the error goes to the log
                    print(f"poll error: {e}", file=sys.stderr)
                time.sleep(60)

        threading.Thread(target=loop, daemon=True).start()
        print(f"broker on :{a.port}, state in {a.state}")
        ThreadingHTTPServer(("0.0.0.0", a.port), make_handler(broker)).serve_forever()
        return 0
    if a.cmd == "submit":
        command = " ".join(a.command[1:] if a.command[:1] == ["--"] else a.command)
        if not command:
            ap.error("give the command after --")
        archive = subprocess.run(["git", "archive", "--format=tar", "HEAD", *ARCHIVE_PATHS], cwd=ROOT,
                                 capture_output=True, check=True).stdout
        body = {"archive": base64.b64encode(archive).decode(), "command": command, "hours": a.hours}
        if a.outputs:
            body["outputs"] = a.outputs
        code, out = client("POST", "/jobs", body)
        print(out.decode())
        return 0 if code == 200 else 1
    if a.cmd == "status":
        code, out = client("GET", f"/jobs/{a.job}")
        print(out.decode())
        return 0 if code == 200 else 1
    if a.cmd == "fetch":
        code, out = client("GET", f"/jobs/{a.job}/results")
        if code != 200:
            print(out.decode())
            return 1
        with tarfile.open(fileobj=io.BytesIO(out)) as tar:
            tar.extractall(ROOT, filter="data")
        print(f"extracted {len(out)} bytes into {ROOT}")
        return 0
    code, out = client("GET", "/quota")
    print(out.decode())
    return 0 if code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
