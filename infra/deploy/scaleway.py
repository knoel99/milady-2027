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

Environment: SCW_SECRET_KEY (optional, see above), SCW_DEFAULT_PROJECT_ID (otherwise the
first project of the key's organization), SCW_DEFAULT_ZONE (default fr-par-2; avoid fr-par-3,
which costs 50 % more).
"""
from __future__ import annotations

import argparse
import json
import os
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


def cmd_create(a):
    with open(a.user_data) as f:
        user_data = f.read()
    body = {
        "name": a.name,
        "commercial_type": a.type,
        "image": image_id(a.zone, a.type),
        "project": project_id(),
        "tags": [TAG],
        "dynamic_ip_required": True,
        "volumes": {"0": {"size": a.disk * 10**9, "volume_type": "sbs_volume"}},
    }
    s = call("POST", f"{inst(a.zone)}/servers", body)["server"]
    sid = s["id"]
    print(f"created  : {sid}")
    call("PATCH", f"{inst(a.zone)}/servers/{sid}/user_data/cloud-init", user_data, "text/plain")
    call("POST", f"{inst(a.zone)}/servers/{sid}/action", {"action": "poweron"})
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
    a = p.parse_args()
    {"check": cmd_check, "list": cmd_list, "create": cmd_create,
     "status": cmd_status, "delete": cmd_delete}[a.cmd](a)


if __name__ == "__main__":
    main()
