#!/usr/bin/env python3
"""Render Quarto pages, then restore the pinned KaTeX tags (SRI).

Quarto rewrites KaTeX's <script>/<link> tags and strips the integrity
attributes. This script renders each page, then puts back the two published tags.

Usage (from any directory):
    python3 tools/render.py report thesis prep/p1-vector-calculus
    python3 tools/render.py --all
Quarto 1.7.32 (pip install quarto-cli==1.7.32, or the official binary).
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "site"  # root of the published site
QUARTO = os.environ.get("QUARTO", "quarto")
BASE = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/"
JS_TAG = (
    '<script>window.backupDefine = window.define; window.define = undefined;</script>'
    f'<script src="{BASE}katex.min.js" integrity="sha384-QFFtAGzvvj+bfgCGxXJlNZZR1nXEZgvG8tDLCCY1F19xl20WlfTYgguB4VcNdxYk" crossorigin="anonymous"></script>'
)
CSS_TAG = (
    '<script>window.define = window.backupDefine; window.backupDefine = undefined;</script>'
    f'<link rel="stylesheet" href="{BASE}katex.min.css" integrity="sha384-3rdsX6e5mueWyoweR9NIVmtEsUkokpBT/0ALqKKIBMr9j4qhHkaIkAcGgsE6uVlp" crossorigin="anonymous">'
)
JS_RE = re.compile(r'<script defer="" src="https://cdn\.jsdelivr\.net/npm/katex@0\.19\.0/dist/katex\.min\.js(?:katex\.min\.js)?"></script>')
CSS_RE = re.compile(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/katex@0\.19\.0/dist/katex\.min\.js(?:katex\.min\.css)?">')


def pages():
    return sorted(p.parent.relative_to(ROOT).as_posix() for p in ROOT.glob("**/index.qmd")
                  if "figures" not in p.parts and "_freeze" not in p.parts)


def render(rel: str) -> bool:
    rel = "." if rel in ("", ".") else rel.strip("/")
    qmd = ROOT / rel / "index.qmd"
    subprocess.run([QUARTO, "render", str(qmd), "--quiet"], check=True)
    html_path = qmd.with_name("index.html")
    html = html_path.read_text(encoding="utf-8")
    html = JS_RE.sub(lambda _: JS_TAG, html)
    html = CSS_RE.sub(lambda _: CSS_TAG, html)
    html_path.write_text(html, encoding="utf-8")
    for junk in (qmd.parent / "index_files",):
        if junk.is_dir():
            import shutil
            shutil.rmtree(junk)
    ok = "katex" not in html or (JS_TAG in html and CSS_TAG in html)
    print(f"{rel}: rendered{'' if ok else ' (KaTeX tags NOT restored)'}")
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = pages()
    if not args:
        sys.exit(__doc__)
    bad = [a for a in args if not render(a)]
    sys.exit(1 if bad else 0)
