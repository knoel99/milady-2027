"""tools/check_deliverables.py on a synthetic team tree: an empty team fails, a complete one passes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import check_deliverables as cd


def build(tmp: Path) -> None:
    base = tmp / "site" / "teams" / "t"
    refs = []
    for i in range(cd.MIN_SCHEMATICS):
        f = base / "figures" / f"f{i}"
        (f / "figure" / "out").mkdir(parents=True)
        (f / "docs").mkdir()
        for name in ("figure/figure.js", "docs/brief.md", f"figure/out/f{i}.svg", f"figure/out/f{i}.pdf"):
            (f / name).write_text("x")
        refs.append(f"![](../figures/f{i}/figure/out/f{i}.svg)")
    (base / "diagrams").mkdir(parents=True)
    for i in range(cd.MIN_DIAGRAMS):
        (base / "diagrams" / f"d{i}.html").write_text("<html>")
        refs.append(f"[d](../diagrams/d{i}.html)")
    (base / "plots").mkdir()
    for i in range(cd.MIN_PLOTS):
        (base / "plots" / f"p{i}.svg").write_text("<svg/>")
    sections = "\n\n".join(f"## {a} {{#{a}}}\ntext" for a in cd.ANCHORS)
    sections = sections.replace("## comparative-study {#comparative-study}\ntext",
                                "## comparative-study {#comparative-study}\n| a | b |\n|---|---|\n| 1 | 2 |")
    (base / "report").mkdir()
    (base / "report" / "index.qmd").write_text(
        "---\ntitle: r\nformat:\n  html:\n    toc: false\n  pdf:\n    documentclass: report\n---\n\n"
        + sections + "\nmeasured, published, conjectured. See [explorer](../explorer/index.html), "
        "[PDF](index.pdf).\n" + "\n".join(refs))
    (base / "explorer" / "data").mkdir(parents=True)
    (base / "explorer" / "data" / "d.json").write_text("{}")
    (base / "explorer" / "index.qmd").write_text("```{ojs}\nviewof eta = Inputs.range([0, 1])\n```\n[report](../report/index.html)")
    (tmp / "experiments").mkdir()
    (tmp / "experiments" / "export_explorer.py").write_text("")


def test_empty_team_fails(tmp_path):
    assert not all(ok for ok, _ in cd.checks("t", False, tmp_path))


def test_complete_team_passes(tmp_path):
    build(tmp_path)
    failed = [w for ok, w in cd.checks("t", False, tmp_path) if not ok]
    assert failed == []
    built = [w for ok, w in cd.checks("t", True, tmp_path) if not ok]
    assert any("PDF" in w for w in built)               # not rendered yet


def minimal_pdf(path: Path, pages: int) -> None:
    """An uncompressed PDF with the given number of empty pages (no dependency)."""
    kids = " ".join(f"{3 + i} 0 R" for i in range(pages))
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>"]
    objs += ["<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>"] * pages
    body, offsets = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(body))
        body += f"{i} 0 obj {o} endobj\n".encode()
    xref = len(body)
    body += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    body += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    body += f"trailer << /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(body)


def test_pdf_page_count_and_minimum(tmp_path, monkeypatch):
    build(tmp_path)
    report = tmp_path / "site" / "teams" / "t" / "report"
    for name in ("index.html",):
        (report / name).write_text("<html>")
    (tmp_path / "site" / "teams" / "t" / "explorer" / "index.html").write_text("<html>")
    pdf = report / "index.pdf"

    def page_check(pages):
        minimal_pdf(pdf, pages)
        rows = [(ok, w) for ok, w in cd.checks("t", True, tmp_path) if w.startswith("PDF pages")]
        assert len(rows) == 1
        return rows[0]

    ok, what = page_check(cd.MIN_PDF_PAGES - 1)
    assert not ok and f"{cd.MIN_PDF_PAGES - 1} (at least {cd.MIN_PDF_PAGES}" in what
    ok, _ = page_check(cd.MIN_PDF_PAGES)
    assert ok
    assert [w for ok, w in cd.checks("t", True, tmp_path) if not ok] == []          # complete and long enough

    # every counter gives the same answer, and the last fallback works without pypdf or pdfinfo
    import builtins
    real_import = builtins.__import__
    monkeypatch.setattr(builtins, "__import__", lambda n, *a, **k: (_ for _ in ()).throw(ImportError(n))
                        if n == "pypdf" else real_import(n, *a, **k))
    monkeypatch.setattr(cd.shutil, "which", lambda name: None)
    assert cd.pdf_pages(pdf) == (cd.MIN_PDF_PAGES, "page objects")
    pdf.write_bytes(b"%PDF-1.4 not a real pdf")
    assert cd.pdf_pages(pdf)[0] is None                                              # reported, not raised
