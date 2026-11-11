#!/usr/bin/env python3
"""Site-wide checks for the MilaDy 2027 site (can be run from any directory).

- every index.qmd has its index.html, newer than the source;
- the pinned KaTeX tags (SRI) are present on pages that have formulas;
- the preparation modules have all the sections of the contract and >= 10 graded exercises;
- every image of a module's own folder is written by its figures_p*.py script (figure provenance);
- all relative links (href, src) of the published pages point to existing files;
- internal anchors (#id) exist in the target page;
- no index_files/ folder or .quarto file is published.
Output: "ok" and the number of pages, or the list of problems (exit code 1).
Usage: python3 tools/check_gates.py [page ...]   (no argument: the whole site; otherwise the given pages)
"""
import re
import sys
import html
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent / "site"  # root of the published site
KATEX_SRI = 'integrity="sha384-QFFtAGzvvj+bfgCGxXJlNZZR1nXEZgvG8tDLCCY1F19xl20WlfTYgguB4VcNdxYk"'
IMG_RE = re.compile(r'(?:\]\(|src=")([^)"\s]+\.(?:png|svg|jpg|gif))')
PREP_SECTIONS = ["{#objectives}", "{#prerequisites}", "{#plan}", "{#exercises}", "{#internship-link}", "{#further-reading}", "{#sources}"]


class Links:
    """Ids and links of a page (fast extraction with regular expressions)."""

    ID_RE = re.compile(r'\sid="([^"]+)"')
    REF_RE = re.compile(r'\s(?:href|src)="([^"]+)"')

    def __init__(self, text):
        # ignore the content of <script> tags and formulas (no useful links, and it is the bulkiest part)
        text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.S)
        self.ids = set(self.ID_RE.findall(text))
        self.refs = [html.unescape(r) for r in self.REF_RE.findall(text)]


def parse(path):
    return Links(path.read_text(encoding="utf-8"))


def main():
    problems = []
    only = [a.strip("/") for a in sys.argv[1:]]
    pages = sorted(q for q in ROOT.glob("**/index.qmd") if "figures" not in q.parts and "node_modules" not in q.parts)
    if only:  # restrict to the requested pages (relative paths, e.g. prep/p1-vector-calculus)
        pages = [q for q in pages if (q.parent.relative_to(ROOT).as_posix() or ".") in only]
    cache = {}
    for qmd in pages:
        rel = qmd.parent.relative_to(ROOT).as_posix() or "."
        html = qmd.with_name("index.html")
        if not html.is_file():
            problems.append(f"{rel}: index.html missing")
            continue
        if html.stat().st_mtime + 1 < qmd.stat().st_mtime:
            problems.append(f"{rel}: index.html older than index.qmd (re-run tools/render.py)")
        text = html.read_text(encoding="utf-8")
        if 'class="math' in text and KATEX_SRI not in text:
            problems.append(f"{rel}: KaTeX tags not pinned")
        src = qmd.read_text(encoding="utf-8")
        if rel.startswith("prep/") and rel != "prep":
            for sec in PREP_SECTIONS:
                if sec not in src:
                    problems.append(f"{rel}: section {sec} missing")
            ex = src.split("{#exercises}", 1)[-1].split("{#internship-link}", 1)[0]
            n_ex = len(re.findall(r"^\d+\.\s+\*\*★", ex, flags=re.M))
            if n_ex < 10:
                problems.append(f"{rel}: {n_ex} graded exercises (>= 10 expected)")
            scripts = "".join(f.read_text(encoding="utf-8") for f in qmd.parent.glob("figures_p*.py"))
            for img in sorted(set(IMG_RE.findall(src))):
                if not img.startswith("../") and Path(img).name not in scripts:
                    problems.append(f"{rel}: image {img} not written by a figures_p*.py script of the module")
        if (qmd.parent / "index_files").exists():
            problems.append(f"{rel}: index_files/ folder to delete")
        links = cache.setdefault(html, parse(html))
        for ref in links.refs:
            parts = urlsplit(ref)
            if parts.scheme or ref.startswith("//") or ref.startswith("mailto:"):
                continue
            target = html if not parts.path else (html.parent / parts.path).resolve()
            if parts.path and target.is_dir():
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{rel}: broken link {ref}")
                continue
            if parts.fragment and target.suffix == ".html":
                tl = cache.setdefault(target, parse(target))
                if parts.fragment not in tl.ids:
                    problems.append(f"{rel}: anchor missing {ref}")
    if (ROOT / ".quarto").exists():
        problems.append(".quarto/ present (do not publish)")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"ok {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
