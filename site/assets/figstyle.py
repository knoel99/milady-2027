"""Shared matplotlib style of the site's static figures.

Used by the figure scripts of the modules (``site/prep/p*/figures_p*.py``) and by
``experiments/figures.py``. Import it after putting this folder on ``sys.path``::

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "assets"))
    import figstyle as fs
    fs.use()

Palette: categorical colours in a fixed order (blue, orange, aqua, yellow, pink, green, violet, red);
the "ground truth" or reference is drawn in neutral ink. Font: Inter if installed, else DejaVu Sans.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
C1, C2, C3 = C[:3]
INK, INK2, LIGHT = "#0b0b0b", "#52514e", "#b9b8b2"
GRID = "#d9d8d4"          # module figures
GRID_LIGHT = "#e4e3df"    # result plots of experiments/figures.py
BLUES, DIVERGING = "Blues", "RdBu_r"
DPI = 150


def use(font_size: float = 10.5, **extra) -> None:
    """Apply the common rcParams (``extra`` overrides individual keys)."""
    plt.rcParams.update({
        "font.family": ["Inter", "DejaVu Sans"], "font.size": font_size,
        "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": font_size,
        "legend.frameon": False, "lines.linewidth": 2, "mathtext.fontset": "dejavusans",
        "figure.facecolor": "white", "savefig.facecolor": "white", "savefig.bbox": "tight",
        "figure.dpi": DPI, "savefig.dpi": DPI,
    })
    plt.rcParams.update(extra)


def save(fig, path: Path, svg: bool = False) -> None:
    """Write ``path`` (PNG), and the SVG twin if requested; print the path."""
    path = Path(path)
    fig.savefig(path)
    if svg:
        fig.savefig(path.with_suffix(".svg"))
    plt.close(fig)
    print("written", path)


def out_dir(script: str, argv: list[str]) -> Path:
    """Output folder: first command-line argument, else the folder of the script."""
    out = Path(argv[1]) if len(argv) > 1 else Path(script).resolve().parent
    out.mkdir(parents=True, exist_ok=True)
    return out
