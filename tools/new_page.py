#!/usr/bin/env python3
"""Create the skeleton of a Quarto page.

Usage (paths relative to site/):
    python3 tools/new_page.py prep/p1-vector-calculus "Title" "Subtitle"
    python3 tools/new_page.py report "Internship report" "Subtitle"
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "site"  # root of the published site
sys.path.insert(0, str(Path(__file__).resolve().parent))
from page_header import header  # noqa: E402

if len(sys.argv) != 4:
    sys.exit(__doc__)
rel, title, subtitle = sys.argv[1].strip("/"), sys.argv[2], sys.argv[3]
depth = 0 if rel in ("", ".") else len(Path(rel).parts)
qmd = ROOT / rel / "index.qmd"
if qmd.exists():
    sys.exit(f"{qmd} already exists")
qmd.parent.mkdir(parents=True, exist_ok=True)
qmd.write_text(header(title, subtitle, "../" * depth) + "\n## Objectives {#objectives}\n\n", encoding="utf-8")
print(qmd)
