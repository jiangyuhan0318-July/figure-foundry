"""Render the saved synthetic CSV using the installed FigureFoundry skill."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path,
                        default=Path.home() / ".codex/skills/figure-foundry")
    args = parser.parse_args()
    module_spec = importlib.util.spec_from_file_location(
        "figure_foundry_style", args.skill_dir / "scripts/figure_style.py")
    helper = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper)
    folder = Path(__file__).resolve().parent
    with (folder / "synthetic_data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    methods = ["Baseline", "Variant A", "Variant B"]
    runs = sorted({row["run_id"] for row in rows})
    epochs = np.array(sorted({int(row["epoch"]) for row in rows}))
    lookup = {(r["method"], r["run_id"], int(r["epoch"])): r for r in rows}
    if len(lookup) != len(rows) or len(rows) != 3 * 8 * 21:
        raise ValueError("Unexpected or duplicated data rows")
    if any(row["data_kind"] != "synthetic" for row in rows):
        raise ValueError("This example expects explicitly synthetic data")
    curves = {m: np.array([[float(lookup[m, r, int(e)]["score_pct"])
                           for e in epochs] for r in runs]) for m in methods}
    scores = {m: curves[m][:, -1] for m in methods}
    latencies = {m: np.array([float(lookup[m, r, int(epochs[-1])]["latency_ms"])
                             for r in runs]) for m in methods}
    colors = helper.get_palette("暖橙组")
    markers = ["o", "s", "D"]
    linestyles = ["--", "-.", "-"]
    summary = []
    for m in methods:
        summary.append({"method": m, "n_runs": len(runs),
                        "score_mean": float(scores[m].mean()),
                        "score_sd": float(scores[m].std(ddof=1)),
                        "latency_mean_ms": float(latencies[m].mean()),
                        "latency_sd_ms": float(latencies[m].std(ddof=1))})

    with matplotlib.rc_context(helper.style_settings()):
        fig = plt.figure(figsize=(180 / 25.4, 140 / 25.4))
        a = fig.add_axes([0.105, 0.580, 0.84, 0.250])
        b = fig.add_axes([0.105, 0.145, 0.355, 0.275])
        c = fig.add_axes([0.605, 0.145, 0.34, 0.275])
        fig.text(0.075, 0.957, "Illustrative model comparison", fontsize=14,
                 fontweight="bold", ha="left", va="top")
        fig.text(0.075, 0.910, "SYNTHETIC DATA  |  8 simulated runs per method  |  Warm-orange palette",
                 fontsize=8, color="#687681")
        for x, y, letter, title in [
            (0.075, 0.865, "A", "Learning progress"),
            (0.075, 0.475, "B", "Paired final scores"),
            (0.575, 0.475, "C", "Score–latency trade-off"),
        ]:
            fig.text(x, y, letter, fontsize=11, fontweight="bold")
            fig.text(x + 0.035, y, title, fontsize=10, fontweight="bold")
        for ax in [a, b, c]:
            for side in ["top", "right"]:
                ax.spines[side].set_visible(False)
            ax.grid(axis="y", zorder=0)
            ax.set_axisbelow(True)
            ax.tick_params(length=3, width=0.6)

        for index, method in enumerate(methods):
            mean = curves[method].mean(axis=0)
            sd = curves[method].std(axis=0, ddof=1)
            a.fill_between(epochs, mean - sd, mean + sd, color=colors[index], alpha=0.25, linewidth=0)
            line, = a.plot(epochs, mean, color=colors[index], lw=1.65,
                           linestyle=linestyles[index], marker=markers[index], markevery=4,
                           markersize=3.5, markeredgecolor="#45505A", markeredgewidth=0.55,
                           label=method, zorder=3 + index)
            line.set_path_effects([patheffects.Stroke(linewidth=2.25, foreground="#72787E"),
                                   patheffects.Normal()])
        a.set(xlim=(0, 102), ylim=(30, 100), xlabel="Training epoch", ylabel="Score (%)")
        a.set_xticks(np.arange(0, 101, 20))
        a.set_yticks([40, 60, 80, 100])
        a.legend(loc="lower right", ncol=3, columnspacing=1.8, handlelength=2.3)
        fig.text(0.945, 0.855, "Line: mean  ·  band: ±1 SD", ha="right", fontsize=7.4, color="#687681")

        offsets = np.linspace(-0.09, 0.09, len(runs))
        for j in range(len(runs)):
            b.plot(np.arange(3) + offsets[j], [scores[m][j] for m in methods],
                   color="#B4BDC3", lw=0.65, alpha=0.55, zorder=1)
        for index, method in enumerate(methods):
            b.scatter(index + offsets, scores[method], marker=markers[index], s=27,
                      facecolor=colors[index], edgecolor="#45505A", linewidth=0.55, zorder=3)
            b.errorbar(index, scores[method].mean(), yerr=scores[method].std(ddof=1),
                       fmt="_", markersize=15, color="#26313D", lw=1.1, capsize=3, zorder=4)
            c.scatter(latencies[method], scores[method], marker=markers[index], s=25,
                      facecolor=colors[index], edgecolor="#45505A", lw=0.55, alpha=0.8, zorder=3)
            c.errorbar(latencies[method].mean(), scores[method].mean(),
                       xerr=latencies[method].std(ddof=1), yerr=scores[method].std(ddof=1),
                       fmt=markers[index], markersize=6.0, markerfacecolor=colors[index],
                       markeredgecolor="#26313D", color="#26313D", lw=0.9, capsize=2.5, zorder=4)
        b.set(xticks=range(3), xticklabels=methods, xlim=(-0.4, 2.4),
              ylim=(85, 97), ylabel="Final score (%)")
        b.set_yticks([86, 90, 94])
        c.set(xlim=(7.0, 11.8), ylim=(85, 97), xlabel="Inference latency (ms)", ylabel="Final score (%)")
        c.set_xticks([7, 9, 11])
        c.set_yticks([86, 90, 94])
        fig.text(0.105, 0.442, "Thin links: matched run IDs; mean ±1 SD", fontsize=7.1, color="#687681")
        fig.text(0.605, 0.442, "Small marks: runs; large marks: mean ±1 SD", fontsize=7.1, color="#687681")
        fig.text(0.075, 0.048, "SIMULATED DATA — workflow demonstration, not experimental evidence.",
                 fontsize=7.5, color="#687681")

        outputs = helper.export_figure(fig, folder / "synthetic_comparison")
        renderer = fig.canvas.get_renderer()
        clipped = []
        for text in fig.findobj(matplotlib.text.Text):
            if text.get_visible() and text.get_text().strip():
                box = text.get_window_extent(renderer)
                if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width + 1 or box.y1 > fig.bbox.height + 1:
                    clipped.append(text.get_text())
        report = {"synthetic": True, "seed": 20261026, "input_rows": len(rows),
                  "excluded_rows": 0, "independent_unit": "simulated run ID",
                  "repeated_unit": "training checkpoint within a run", "n_runs_per_method": len(runs),
                  "uncertainty": "sample SD across runs, ddof=1", "palette": colors,
                  "width_mm": 180, "height_mm": 140, "png_dpi": 300,
                  "matplotlib_version": matplotlib.__version__, "summary": summary,
                  "text_outside_canvas": clipped, "outputs": {k: Path(v).name for k, v in outputs.items()}}
        (folder / "plot_checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
