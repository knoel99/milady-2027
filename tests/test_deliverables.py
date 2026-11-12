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
