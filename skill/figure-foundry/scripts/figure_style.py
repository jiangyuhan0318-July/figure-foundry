"""Small Matplotlib helpers for FigureFoundry figures; no global style mutation."""
import json
from pathlib import Path


def get_palette(name="warm-orange"):
    source = Path(__file__).resolve().parents[1] / "assets" / "palettes.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    for key, value in data["palettes"].items():
        if name in (key, value["name_zh"]):
            return list(value["colors"])
    raise ValueError(f"Unknown palette: {name}")


def style_settings(font_family="DejaVu Sans"):
    return {
        "font.family": font_family,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "axes.labelcolor": "#26313D",
        "axes.edgecolor": "#AEB7BD",
        "axes.linewidth": 0.65,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.color": "#687681",
        "ytick.color": "#687681",
        "text.color": "#26313D",
        "grid.color": "#E8ECEF",
        "grid.linewidth": 0.6,
        "legend.fontsize": 8,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }


def export_figure(fig, stem, formats=("png", "svg", "pdf"), dpi=300):
    """Preserve the authored canvas; derive all requested exports from one scene."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    outputs = {}
    for suffix in formats:
        path = stem.with_suffix("." + suffix)
        fig.savefig(path, format=suffix, dpi=dpi, bbox_inches=None)
        outputs[suffix] = str(path)
    return outputs
