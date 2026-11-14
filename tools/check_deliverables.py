#!/usr/bin/env python3
"""Check the deliverables of a team against race/DELIVERABLES.md of knoel99/frontier-one (report, figures, diagrams, explorer).

    python3 tools/check_deliverables.py --team claude            # sources: sections, figures, links, sizes
    python3 tools/check_deliverables.py --team claude --built    # also the rendered HTML and the PDF

Prints one line per check and exits 1 if one fails. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANCHORS = ["abstract", "introduction", "state-of-the-art", "methods", "experiments", "results",
           "comparative-study", "toolbox", "discussion", "conclusion", "references", "reproducibility"]
MIN_SCHEMATICS, MIN_DIAGRAMS, MIN_PLOTS = 8, 3, 8
MAX_DATA_MB, MAX_FILE_MB, MAX_PDF_MB = 25, 10, 20
MIN_PDF_PAGES = 30  # race/DELIVERABLES.md: "about 30 to 50 pages in PDF"
PLOT_EXT = {".svg", ".png"}


def pdf_pages(pdf: Path) -> tuple[int | None, str]:
    """Number of pages of a PDF and the method used: pypdf, else poppler's pdfinfo, else a count of the
    /Type /Page objects of an uncompressed file. (None, reason) when no method can tell."""
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf)).pages), "pypdf"
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001 - a broken file is reported, not raised
        return None, f"pypdf could not read it ({type(e).__name__})"
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=False).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.MULTILINE)
        if m:
            return int(m.group(1)), "pdfinfo"
    n = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf.read_bytes()))
    if n:
        return n, "page objects"
    return None, "no page counter (install pypdf or poppler-utils)"


def section(text: str, anchor: str) -> str:
    m = re.search(r"^(#+) [^\n]*\{#" + re.escape(anchor) + r"[ }]", text, re.MULTILINE)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(r"^#{1," + str(level) + r"} ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def checks(team: str, built: bool, root: Path = ROOT) -> list[tuple[bool, str]]:
    base = root / "site" / "teams" / team
    out: list[tuple[bool, str]] = []
    report = base / "report" / "index.qmd"
    explorer = base / "explorer" / "index.qmd"
    text = report.read_text(encoding="utf-8") if report.exists() else ""
    etext = explorer.read_text(encoding="utf-8") if explorer.exists() else ""
    out.append((bool(text), f"report source {report.relative_to(root)}"))
    header = text.split("\n---", 1)[0] if text.startswith("---") else ""
    out.append(("html:" in header and "pdf:" in header, "report declares format html and format pdf"))
    out.append((bool(re.search(r"documentclass:\s*(report|scrreprt)", header)),
                "PDF document class report or scrreprt"))
    for a in ANCHORS:
        out.append(("{#" + a in text, f"report section {{#{a}}}"))
    comp = section(text, "comparative-study")
    out.append((bool(re.search(r"^\|.*\|\s*$", comp, re.MULTILINE)), "comparative study holds a table"))
    for word in ("measured", "published", "conjectured"):
        out.append((word in text.lower(), f"report labels claims as {word}"))

    refs = text + etext
    figs = sorted(p.parents[2] for p in (base / "figures").glob("*/figure/out/*.svg")) if base.exists() else []
    figs = sorted(set(figs))
    ok_figs = [f for f in figs if list((f / "figure" / "out").glob("*.pdf")) and (f / "figure" / "figure.js").exists()
               and (f / "docs" / "brief.md").exists()]
    out.append((len(ok_figs) >= MIN_SCHEMATICS,
                f"schematic figures with source, brief, SVG and PDF: {len(ok_figs)} (at least {MIN_SCHEMATICS})"))
    unref = [f.name for f in ok_figs if f"figures/{f.name}/" not in refs]
    out.append((not unref, "every schematic is referenced" + (f" (not: {unref})" if unref else "")))
    diags = sorted((base / "diagrams").glob("*.html")) if (base / "diagrams").exists() else []
    out.append((len(diags) >= MIN_DIAGRAMS, f"Archify diagrams: {len(diags)} (at least {MIN_DIAGRAMS})"))
    undiag = [d.name for d in diags if d.name not in refs]
    out.append((not undiag, "every diagram is linked" + (f" (not: {undiag})" if undiag else "")))
    plots = [p for d in ("plots", "report", "explorer") for p in (base / d).rglob("*")
             if p.suffix in PLOT_EXT and "data" not in p.parts and p.is_file()] if base.exists() else []
    out.append((len(plots) >= MIN_PLOTS, f"data plots (SVG or PNG): {len(plots)} (at least {MIN_PLOTS})"))

    out.append((bool(etext), f"explorer source {explorer.relative_to(root)}"))
    out.append((bool(re.search(r"Inputs\.|<input|<select", etext)), "explorer has controls"))
    data = [p for p in (base / "explorer" / "data").rglob("*") if p.is_file()] if (base / "explorer" / "data").exists() else []
    total = sum(p.stat().st_size for p in data) / 1e6
    big = [p.name for p in data if p.stat().st_size > MAX_FILE_MB * 1e6]
    out.append((bool(data) and total <= MAX_DATA_MB and not big,
                f"explorer data: {len(data)} files, {total:.1f} MB (at most {MAX_DATA_MB} MB, {MAX_FILE_MB} MB per file)"))
    out.append(((root / "experiments" / "export_explorer.py").exists(), "export script experiments/export_explorer.py"))
    out.append(("report/" in etext and "explorer/" in text, "report and explorer link to each other"))

    if built:
        pdf = base / "report" / "index.pdf"
        out.append((pdf.exists() and pdf.stat().st_size <= MAX_PDF_MB * 1e6,
                    f"PDF {pdf.relative_to(root)} built (at most {MAX_PDF_MB} MB)"))
        pages, how = pdf_pages(pdf) if pdf.exists() else (None, "no PDF")
        out.append((pages is not None and pages >= MIN_PDF_PAGES,
                    f"PDF pages: {pages if pages is not None else '?'} (at least {MIN_PDF_PAGES}; {how})"))
        out.append(("index.pdf" in text, "the report links its PDF"))
        for page in (base / "report" / "index.html", base / "explorer" / "index.html"):
            out.append((page.exists(), f"rendered {page.relative_to(root)}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", required=True)
    ap.add_argument("--built", action="store_true", help="also check the rendered HTML and the PDF")
    a = ap.parse_args()
    res = checks(a.team, a.built)
    for ok, what in res:
        print(f"{'ok  ' if ok else 'FAIL'} {what}")
    bad = sum(not ok for ok, _ in res)
    print(f"{len(res) - bad}/{len(res)} checks pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
