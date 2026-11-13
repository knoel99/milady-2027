#!/usr/bin/env python3
"""Local relay between an OpenAI-chat harness and Gemini's OpenAI-compatible endpoint.

Gemini's endpoint (https://generativelanguage.googleapis.com/v1beta/openai) differs from the
OpenAI chat API in two ways that break harnesses such as Mistral Vibe, Qwen Code and Kimi Code:

1. streamed tool-call chunks carry no ``index`` (Vibe: "Tool call chunk missing index");
2. every tool call carries a ``thought_signature`` (``extra_content.google``) that must be sent
   back with the assistant message on the next request, otherwise the API answers 400; most
   harnesses drop that unknown field.

The relay adds the missing indexes and remembers each tool call's signature by its id, then puts it
back into the assistant messages of later requests. It uses the standard library only and honours
HTTPS_PROXY. Usage:

    python3 tools/gemini_compat_shim.py --port 8765 &
    # harness base URL: http://127.0.0.1:8765  (paths are forwarded under /v1beta/openai)
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import ssl
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "generativelanguage.googleapis.com"
PREFIX = "/v1beta/openai"
SIGNATURES: dict[str, dict] = {}
LOCK = threading.Lock()


def remember(tool_calls: list) -> None:
    for tc in tool_calls or []:
        extra = tc.get("extra_content")
        if tc.get("id") and extra:
            with LOCK:
                SIGNATURES[tc["id"]] = extra


def restore(body: dict) -> dict:
    """Put remembered thought signatures back into the assistant tool calls of a request."""
    for msg in body.get("messages", []):
        if msg.get("role") == "assistant":
            for tc in msg.get("tool_calls") or []:
                if "extra_content" not in tc:
                    with LOCK:
                        sig = SIGNATURES.get(tc.get("id"))
                    if sig:
                        tc["extra_content"] = sig
    return body


def fix_chunk(chunk: dict, state: dict) -> dict:
    """Add the index of each streamed tool call (one index per new tool-call id)."""
    for choice in chunk.get("choices", []):
        delta = choice.get("delta") or {}
        calls = delta.get("tool_calls") or []
        for pos, tc in enumerate(calls):
            if tc.get("index") is None and not tc.get("id"):
                tc["index"] = pos
            elif tc.get("index") is None:
                tid = tc.get("id")
                if tid and tid not in state["ids"]:
                    state["ids"][tid] = len(state["ids"])
                tc["index"] = state["ids"].get(tid, max(len(state["ids"]) - 1, 0))
        remember(calls)
        remember((choice.get("message") or {}).get("tool_calls"))
    return chunk


def upstream_connection() -> http.client.HTTPSConnection:
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE"))
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        p = urllib.parse.urlparse(proxy)
        conn = http.client.HTTPSConnection(p.hostname, p.port or 80, context=ctx, timeout=600)
        headers = {}
        if p.username:
            import base64
            cred = base64.b64encode(f"{urllib.parse.unquote(p.username)}:{urllib.parse.unquote(p.password or '')}".encode()).decode()
            headers["Proxy-Authorization"] = f"Basic {cred}"
        conn.set_tunnel(UPSTREAM, 443, headers=headers)
        return conn
    return http.client.HTTPSConnection(UPSTREAM, 443, context=ctx, timeout=600)


class Relay(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # quiet
        pass

    def _forward(self, method: str) -> None:
        path = self.path if self.path.startswith(PREFIX) else PREFIX + self.path
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method == "POST" else None
        stream = False
        if raw:
            try:
                body = restore(json.loads(raw))
                stream = bool(body.get("stream"))
                raw = json.dumps(body).encode()
            except ValueError:
                pass
        headers = {"Content-Type": "application/json",
                   "Authorization": self.headers.get("Authorization", "Bearer none")}
        conn = upstream_connection()
        conn.request(method, path, body=raw, headers=headers)
        resp = conn.getresponse()
        self.send_response(resp.status)
        self.send_header("Content-Type", resp.getheader("Content-Type", "application/json"))
        if stream and resp.status == 200:
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            state = {"ids": {}}
            for line in resp:
                text = line.decode()
                if text.startswith("data:") and text[5:].strip() not in ("", "[DONE]"):
                    try:
                        text = "data: " + json.dumps(fix_chunk(json.loads(text[5:]), state)) + "\n"
                    except ValueError:
                        pass
                data = text.encode()
                self.wfile.write(f"{len(data):x}\r\n".encode() + data + b"\r\n")
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")
        else:
            data = resp.read()
            try:
                obj = json.loads(data)
                fix_chunk(obj, {"ids": {}})
            except ValueError:
                pass
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        conn.close()

    def do_POST(self):
        self._forward("POST")

    def do_GET(self):
        self._forward("GET")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Relay).serve_forever()


if __name__ == "__main__":
    main()
