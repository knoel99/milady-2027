#!/usr/bin/env python3
"""Drive a Scaleway CPU instance through the HTTP API (standard library only).

The secret key goes in the `X-Auth-Token` header. In a Claude Code cloud session the network
proxy injects it, so the script sends a placeholder; elsewhere, export SCW_SECRET_KEY.
No SSH is needed: the VM receives a cloud-init script as user data and must publish its
results itself.

Usage:
  infra/deploy/scaleway.py check                         # key, project, zone, image, price
  infra/deploy/scaleway.py list
  infra/deploy/scaleway.py create NAME --user-data FILE [--type POP2-HC-16C-32G] [--disk 40]
  infra/deploy/scaleway.py status SERVER_ID
  infra/deploy/scaleway.py delete SERVER_ID              # terminate + delete leftover volumes
  infra/deploy/scaleway.py campaign NAME --args "--quick" [--type ...] [--ref COMMIT]
  infra/deploy/scaleway.py fetch IP TOKEN [FILE ...]     # status.txt, run_stage.log, results
  infra/deploy/scaleway.py cleanup [--dry-run]           # delete every milady-tagged resource

Environment: SCW_SECRET_KEY (optional, see above), SCW_DEFAULT_PROJECT_ID (otherwise the
first project of the key's organization), SCW_DEFAULT_ZONE (default fr-par-2; avoid fr-par-3,
which costs 50 % more).
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request

API = "https://api.scaleway.com"
PLACEHOLDER = "00000000-0000-0000-0000-000000000000"  # replaced by the proxy
ZONE = os.environ.get("SCW_DEFAULT_ZONE", "fr-par-2")
TAG = "milady"


def call(method: str, path: str, body=None, content_type: str = "application/json"):
    data = None
    if body is not None:
        data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("X-Auth-Token", os.environ.get("SCW_SECRET_KEY", PLACEHOLDER))
    if data is not None:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path}: HTTP {e.code} {e.read().decode(errors='replace')[:500]}")
    return json.loads(raw) if raw.strip() else {}


def inst(zone: str) -> str:
    return f"/instance/v1/zones/{zone}"


def project_id() -> str:
    pid = os.environ.get("SCW_DEFAULT_PROJECT_ID")
    if pid:
        return pid
    projects = call("GET", "/account/v3/projects?page_size=10").get("projects", [])
    if not projects:
        sys.exit("No project visible with this key: set SCW_DEFAULT_PROJECT_ID.")
    default = [p for p in projects if p.get("name") == "default"]
    return (default or projects)[0]["id"]


def image_id(zone: str, commercial_type: str, label: str = "ubuntu_noble") -> str:
    q = f"/marketplace/v2/local-images?image_label={label}&zone={zone}&type=instance_sbs"
    for img in call("GET", q).get("local_images", []):
        if commercial_type in img.get("compatible_commercial_types", []):
            return img["id"]
    sys.exit(f"No {label} image compatible with {commercial_type} in {zone}.")


def cmd_check(a):
    cat = call("GET", f"{inst(a.zone)}/products/servers?per_page=100")["servers"]
    if a.type not in cat:
        sys.exit(f"{a.type} is not offered in {a.zone}.")
    t = cat[a.type]
    print(f"type     : {a.type} in {a.zone}, {t['ncpus']} vCPU, {t['ram'] // 2**30} GiB")
    print(f"image    : ubuntu_noble -> {image_id(a.zone, a.type)}")
    print(f"project  : {project_id()}")
    servers = call("GET", f"{inst(a.zone)}/servers?per_page=50")["servers"]
    print(f"servers  : {len(servers)} in {a.zone} (the key is accepted)")


def cmd_list(a):
    for s in call("GET", f"{inst(a.zone)}/servers?per_page=50")["servers"]:
        ip = (s.get("public_ip") or {}).get("address", "-")
        print(s["id"], s["name"], s["commercial_type"], s["state"], ip, ",".join(s["tags"]))


def create_server(name: str, user_data: str, commercial_type: str, zone: str, disk_gb: int = 40,
                  tags: tuple[str, ...] = ()) -> str:
    """Create a server with a cloud-init user data script, power it on, return its id."""
    body = {
        "name": name,
        "commercial_type": commercial_type,
        "image": image_id(zone, commercial_type),
        "project": project_id(),
        "tags": [TAG, *tags],
        "dynamic_ip_required": True,
        "volumes": {"0": {"size": disk_gb * 10**9, "volume_type": "sbs_volume"}},
    }
    sid = call("POST", f"{inst(zone)}/servers", body)["server"]["id"]
    call("PATCH", f"{inst(zone)}/servers/{sid}/user_data/cloud-init", user_data, "text/plain")
    call("POST", f"{inst(zone)}/servers/{sid}/action", {"action": "poweron"})
    return sid


def cmd_create(a):
    with open(a.user_data) as f:
        user_data = f.read()
    sid = create_server(a.name, user_data, a.type, a.zone, a.disk)
    print(f"created  : {sid}")
    print("powering on; follow with: status", sid)


def cmd_status(a):
    s = call("GET", f"{inst(a.zone)}/servers/{a.server}")["server"]
    ip = (s.get("public_ip") or {}).get("address", "-")
    print(s["id"], s["name"], s["state"], s.get("state_detail", ""), ip)


def cmd_delete(a):
    path = f"{inst(a.zone)}/servers/{a.server}"
    s = call("GET", path)["server"]
    vols = [v["id"] for v in s.get("volumes", {}).values()]
    call("POST", f"{path}/action", {"action": "terminate"})
    for _ in range(60):  # wait until the server is gone
        req = urllib.request.Request(API + path, method="GET")
        req.add_header("X-Auth-Token", os.environ.get("SCW_SECRET_KEY", PLACEHOLDER))
        try:
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break
        time.sleep(5)
    for vid in vols:  # block volumes may survive terminate
        req = urllib.request.Request(f"{API}/block/v1alpha1/zones/{a.zone}/volumes/{vid}",
                                     method="DELETE")
        req.add_header("X-Auth-Token", os.environ.get("SCW_SECRET_KEY", PLACEHOLDER))
        try:
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print(f"volume {vid}: HTTP {e.code}, delete it in the console", file=sys.stderr)
    print(f"deleted  : {a.server}")


def http_get(url: str) -> bytes:
    """GET a plain-HTTP URL, through a CONNECT tunnel when HTTPS_PROXY is set (cloud sessions
    only allow outbound traffic through that proxy, which accepts CONNECT only)."""
    import http.client
    from urllib.parse import urlsplit
    u = urlsplit(url)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        p = urlsplit(proxy)
        conn = http.client.HTTPConnection(p.hostname, p.port, timeout=120)
        conn.set_tunnel(u.hostname, u.port or 80)
    else:
        conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=120)
    conn.request("GET", u.path)
    r = conn.getresponse()
    if r.status != 200:
        sys.exit(f"GET {u.path}: HTTP {r.status}")
    return r.read()


def cmd_campaign(a):
    here = os.path.dirname(os.path.abspath(__file__))
    ref = a.ref or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=here, text=True).strip()
    token = secrets.token_hex(16)
    with open(os.path.join(here, "scaleway-campaign.sh")) as f:
        script = f.read()
    for k, v in {"__TOKEN__": token, "__REPO__": a.repo, "__REF__": ref,
                 "__ARGS__": a.args, "__MAX_MIN__": str(a.max_min)}.items():
        script = script.replace(k, v)
    path = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"user-data-{token[:8]}.sh")
    with open(path, "w") as f:
        f.write(script)
    print(f"token    : {token}\nref      : {ref}")
    a.user_data = path
    cmd_create(a)


def cmd_fetch(a):
    base = f"http://{a.ip}:8000/{a.token}/"
    for name in a.files or ["status.txt"]:
        data = http_get(base + name)
        if name.endswith((".gz", ".npz")):
            out = os.path.basename(name)
            with open(out, "wb") as f:
                f.write(data)
            print(f"{name}: {len(data)} bytes -> {out}")
        else:
            sys.stdout.write(data.decode(errors="replace"))


def leftovers(zone: str):
    pid = project_id()
    servers = [s for s in call("GET", f"{inst(zone)}/servers?per_page=100&tags={TAG}&project={pid}")["servers"]]
    ips = [ip for ip in call("GET", f"{inst(zone)}/ips?per_page=100&project={pid}")["ips"]
           if TAG in ip.get("tags", []) or (ip.get("server") or {}).get("id") in
           {s["id"] for s in servers} or not ip.get("server")]
    vols = [v for v in call("GET", f"/block/v1alpha1/zones/{zone}/volumes?page_size=100&project_id={pid}")["volumes"]
            if not v.get("references")]
    return servers, ips, vols


def cmd_cleanup(a):
    servers, ips, vols = leftovers(a.zone)
    for s in servers:
        print("server", s["id"], s["name"], s["state"])
        if not a.dry_run:
            a.server = s["id"]
            cmd_delete(a)
    servers, ips, vols = leftovers(a.zone)
    for ip in ips:
        print("ip", ip["id"], ip["address"])
        if not a.dry_run and not ip.get("server"):
            call("DELETE", f"{inst(a.zone)}/ips/{ip['id']}")
    for v in vols:
        print("unattached volume", v["id"], v["name"], v["size"] // 10**9, "GB")
        if not a.dry_run:
            call("DELETE", f"/block/v1alpha1/zones/{a.zone}/volumes/{v['id']}")
    servers, ips, vols = leftovers(a.zone)
    print(f"remaining in {a.zone}: {len(servers)} milady servers, {len(ips)} IPs, "
          f"{len(vols)} unattached volumes")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--zone", default=ZONE)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--type", default="POP2-HC-16C-32G")
    sub.add_parser("list")
    c = sub.add_parser("create")
    c.add_argument("name")
    c.add_argument("--user-data", required=True)
    c.add_argument("--type", default="POP2-HC-16C-32G")
    c.add_argument("--disk", type=int, default=40, help="GB")
    for name in ("status", "delete"):
        sub.add_parser(name).add_argument("server")
    c = sub.add_parser("campaign")
    c.add_argument("name")
    c.add_argument("--args", default="--quick", help="run_stage.sh options")
    c.add_argument("--type", default="POP2-HC-8C-16G")
    c.add_argument("--disk", type=int, default=40, help="GB")
    c.add_argument("--ref", help="commit to run (default: local HEAD, must be pushed)")
    c.add_argument("--repo", default="https://github.com/knoel99/milady-2027.git")
    c.add_argument("--max-min", type=int, default=180, help="power off after N minutes")
    c = sub.add_parser("fetch")
    c.add_argument("ip")
    c.add_argument("token")
    c.add_argument("files", nargs="*")
    sub.add_parser("cleanup").add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    {"check": cmd_check, "list": cmd_list, "create": cmd_create, "status": cmd_status,
     "delete": cmd_delete, "campaign": cmd_campaign, "fetch": cmd_fetch,
     "cleanup": cmd_cleanup}[a.cmd](a)


if __name__ == "__main__":
    main()
