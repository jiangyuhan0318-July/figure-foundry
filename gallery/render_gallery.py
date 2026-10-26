"""Render 24 source-driven synthetic examples with the installed FigureFoundry skill."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon
from matplotlib.path import Path as MplPath
from matplotlib.text import Text

INK, MUTED = "#26313D", "#687681"
MARKERS, LINES = ["o", "s", "D"], ["-", "--", "-."]


def clean(ax, grid=True):
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.set_axisbelow(True)
    if grid:
        ax.grid(axis="y", color="#E8ECEF", lw=.6)
    ax.tick_params(length=3, width=.6)


def grouped_bar(ax, d, c):
    values = np.array(d["grouped_bar"])
    x = np.arange(4)
    for i, label in enumerate(["Baseline", "Design A", "Design B"]):
        ax.bar(x+(i-1)*.24, values[:, i].mean(1), .22, yerr=values[:, i].std(1, ddof=1),
               color=c[i], edgecolor=INK, lw=.55, capsize=2, label=label,
               error_kw={"elinewidth": .7, "ecolor": INK}, hatch=["", "//", ".."][i])
    ax.set(xticks=x, xticklabels=["Set 1", "Set 2", "Set 3", "Set 4"], ylim=(0, 105), ylabel="Score (%)")
    ax.legend(ncol=3, fontsize=6.5, loc="upper left", columnspacing=.8, handlelength=1.1)


def trend(ax, d, c):
    values = np.array(d["trend"]["values"]); t = np.array(d["trend"]["time"])
    for i in range(3):
        mean, sd = values[i].mean(0), values[i].std(0, ddof=1)
        ax.fill_between(t, mean-sd, mean+sd, color=c[i], alpha=.25, lw=0)
        ax.plot(t, mean, color=c[i], marker=MARKERS[i], ls=LINES[i], markevery=5,
                ms=3, mec=INK, mew=.4, lw=1.7, label=f"Series {i+1}")
    ax.set(xlabel="Time (h)", ylabel="Response (a.u.)", ylim=(18, 52), xlim=(0, 24))
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.legend(ncol=3, fontsize=6.5, loc="upper left", columnspacing=.8)


def paired(ax, d, c):
    before, after = np.array(d["paired"]["before"]), np.array(d["paired"]["after"])
    jitter = np.linspace(-.055, .055, len(before))
    for a, b, j in zip(before, after, jitter):
        ax.plot([j, 1+j], [a, b], color="#B5BDC3", lw=.7, zorder=1)
    ax.scatter(jitter, before, s=23, fc=c[0], ec=INK, lw=.5, zorder=3)
    ax.scatter(1+jitter, after, s=23, marker="D", fc=c[2], ec=INK, lw=.5, zorder=3)
    ax.set(xticks=[0, 1], xticklabels=["Before", "After"], xlim=(-.35, 1.35), ylabel="Response (a.u.)")


def forest(ax, d, c):
    x = np.array(d["forest"]); mean = x.mean(1)
    ci = stats.t.ppf(.975, x.shape[1]-1)*x.std(1, ddof=1)/np.sqrt(x.shape[1])
    for i in range(6):
        ax.errorbar(mean[i], i, xerr=ci[i], fmt=MARKERS[i%3], color=INK,
                    mfc=c[i%3], mec=INK, ms=5.5, capsize=2, lw=1)
    ax.axvline(0, color=MUTED, lw=.8, ls="--")
    ax.set(yticks=range(6), yticklabels=[f"Contrast {i+1}" for i in range(6)],
           xlabel="Paired difference (a.u.)", ylim=(-.7, 5.7))
    ax.invert_yaxis()


def lollipop(ax, d, c):
    values = np.array(d["lollipop"]); y = np.arange(len(values))
    ax.hlines(y, 0, values, color="#C8C8C8", lw=1.8)
    colors = [c[0]]*len(values); colors[-1] = c[2]
    ax.scatter(values, y, s=40, c=colors, edgecolor=INK, lw=.6, zorder=3)
    ax.set(yticks=y, yticklabels=[f"Feature {i+1}" for i in y], xlabel="Signal strength (a.u.)", xlim=(0, 100))
    ax.grid(False); ax.grid(axis="x", color="#E8ECEF", lw=.6)


def waterfall(ax, d, c):
    start = d["waterfall"]["start"]; changes = d["waterfall"]["changes"]
    total = start
    ax.bar(0, start, width=.65, color=c[1], ec=INK, lw=.55)
    ax.text(0, start+3, str(start), ha="center", fontsize=7)
    for i, delta in enumerate(changes, 1):
        new = total+delta
        ax.plot([i-1+.325, i-.325], [total, total], c=MUTED, lw=.65)
        ax.bar(i, abs(delta), bottom=min(total, new), width=.65, color=c[2] if delta>0 else c[0], ec=INK, lw=.55)
        ax.text(i, max(total, new)+3, f"{delta:+}", ha="center", fontsize=7)
        total = new
    ax.bar(5, total, width=.65, color=c[1], ec=INK, lw=.55)
    ax.text(5, total+3, str(total), ha="center", fontsize=7)
    ax.set(xticks=range(6), xticklabels=["Start", "+A", "−B", "+C", "−D", "End"], ylim=(0, 150), ylabel="Cumulative units")


def box(ax, d, c):
    samples = [np.array(x) for x in d["distributions"]]
    b = ax.boxplot(samples, patch_artist=True, widths=.46, showfliers=False,
                   medianprops={"color": INK, "linewidth": 1.3},
                   boxprops={"linewidth": .7}, whiskerprops={"linewidth": .7}, capprops={"linewidth": .7})
    for i, (patch, x) in enumerate(zip(b["boxes"], samples)):
        patch.set_facecolor(c[i]); patch.set_edgecolor(INK)
        jitter = .12*np.sin(np.arange(len(x))*2.399)
        ax.scatter(i+1+jitter, x, s=9, fc=c[i], ec=INK, lw=.25, alpha=.65, zorder=3)
    ax.set(xticks=[1, 2, 3], xticklabels=["Group 1", "Group 2", "Group 3"], ylabel="Value (a.u.)")


def violin(ax, d, c):
    samples = [np.array(x) for x in d["distributions"]]
    p = ax.violinplot(samples, showextrema=False, widths=.8)
    for i, (body, x) in enumerate(zip(p["bodies"], samples)):
        body.set_facecolor(c[i]); body.set_edgecolor(INK); body.set_alpha(.8); body.set_linewidth(.65)
        q1, med, q3 = np.percentile(x, [25, 50, 75])
        ax.plot([i+1, i+1], [q1, q3], c=INK, lw=2.7)
        ax.scatter(i+1, med, s=15, color="white", ec=INK, lw=.4, zorder=3)
    ax.set(xticks=[1, 2, 3], xticklabels=["Group 1", "Group 2", "Group 3"], ylabel="Value (a.u.)")


def histogram(ax, d, c):
    samples = [np.array(x) for x in d["distributions"]]
    grid = np.linspace(4, 20, 240); bins = np.linspace(4, 20, 22)
    for i, x in enumerate(samples):
        ax.hist(x, bins=bins, density=True, color=c[i], alpha=.22, ec="white", lw=.3)
        ax.plot(grid, stats.gaussian_kde(x)(grid), color=c[i], lw=2, ls=LINES[i], label=f"Group {i+1}")
    ax.set(xlabel="Value (a.u.)", ylabel="Density", ylim=(0, .52))
    ax.legend(fontsize=6.5, loc="upper right")


def ridge(ax, d, c):
    grid = np.linspace(-3, 7, 220)
    for i, sample in enumerate(d["ridge"]):
        density = stats.gaussian_kde(sample)(grid)*1.45
        ax.fill_between(grid, i, i+density, color=c[i%3], alpha=.65, lw=0)
        ax.plot(grid, i+density, color=INK, lw=.65)
    ax.set(yticks=range(5), yticklabels=[f"Batch {i+1}" for i in range(5)], xlabel="Value (a.u.)", ylim=(-.15, 5))
    ax.grid(False)


def regression(ax, d, c):
    x, y = np.array(d["regression"]["x"]), np.array(d["regression"]["y"])
    fit = stats.linregress(x, y); xx = np.linspace(x.min(), x.max(), 150)
    yy = fit.intercept+fit.slope*xx
    residual = y-(fit.intercept+fit.slope*x)
    se = np.sqrt(np.sum(residual**2)/(len(x)-2))*np.sqrt(1/len(x)+(xx-x.mean())**2/np.sum((x-x.mean())**2))
    ci = stats.t.ppf(.975, len(x)-2)*se
    ax.fill_between(xx, yy-ci, yy+ci, color=c[0], alpha=.3, lw=0)
    ax.scatter(x, y, s=17, fc=c[1], ec=INK, lw=.35, alpha=.7)
    ax.plot(xx, yy, color=c[2], lw=1.8)
    ax.text(.03, .94, f"$R^2$ = {fit.rvalue**2:.2f}", transform=ax.transAxes, va="top", fontsize=8)
    ax.set(xlabel="Predictor (a.u.)", ylabel="Response (a.u.)", xlim=(0, 10))
    ax.set_xticks([0, 2, 4, 6, 8, 10])


def bubble(ax, d, c):
    b = d["bubble"]; groups = np.array(b["group"])
    for i in range(3):
        use = groups==i
        ax.scatter(np.array(b["x"])[use], np.array(b["y"])[use], s=np.array(b["size"])[use]*2.5,
                   fc=c[i], ec=INK, lw=.55, alpha=.8, marker=MARKERS[i], label=f"Class {i+1}")
    ax.set(xlabel="Resource (a.u.)", ylabel="Utility (a.u.)", ylim=(5, 105), xlim=(1, 13))
    ax.set_xticks([2, 4, 6, 8, 10, 12])
    ax.legend(ncol=3, loc="upper left", fontsize=6.5, columnspacing=.8, handletextpad=.4, markerscale=.6)


def heatmap(ax, d, c):
    matrix = np.corrcoef(np.array(d["correlation_inputs"]), rowvar=False)
    cmap = LinearSegmentedColormap.from_list("saved_skin_blue", c)
    edges = np.arange(7)-.5
    im = ax.pcolormesh(edges, edges, matrix, vmin=-1, vmax=1, cmap=cmap, rasterized=False)
    ax.set_ylim(5.5,-.5); ax.set_aspect("equal")
    for i in range(6):
        for j in range(6):
            ax.text(j, i, f"{matrix[i,j]:.2f}", ha="center", va="center", fontsize=6.5,
                    color="white" if matrix[i,j]>.65 else INK)
    ax.set(xticks=range(6), yticks=range(6), xticklabels=[f"F{i+1}" for i in range(6)], yticklabels=[f"F{i+1}" for i in range(6)])
    ax.grid(False)
    colorbar = ax.figure.colorbar(im, ax=ax, fraction=.046, pad=.04, label="Pearson r", ticks=[-1, 0, 1])
    colorbar.solids.set_rasterized(False)


def pca(ax, d, c):
    x = np.array(d["pca"]["x"]); group = np.array(d["pca"]["group"])
    x = (x-x.mean(0))/x.std(0, ddof=1)
    u, s, _ = np.linalg.svd(x, full_matrices=False); z = u[:, :2]*s[:2]; var = s*s/np.sum(s*s)
    for i in range(3):
        ax.scatter(z[group==i, 0], z[group==i, 1], s=17, fc=c[i], ec=INK, lw=.35, alpha=.8,
                   marker=MARKERS[i], label=f"Cluster {i+1}")
    ax.set(xlabel=f"PC1 ({var[0]*100:.1f}% variance)", ylabel=f"PC2 ({var[1]*100:.1f}% variance)")
    ax.legend(fontsize=6.5, loc="upper left")


def classification_curves(truth, scores):
    order = np.argsort(-np.asarray(scores)); hit = np.array(truth)[order]
    tp, fp = np.cumsum(hit), np.cumsum(1-hit)
    recall = tp/tp[-1]; precision = tp/np.arange(1, len(hit)+1)
    fpr = np.r_[0, fp/fp[-1]]; tpr = np.r_[0, recall]
    auc = float(np.sum(np.diff(fpr)*(tpr[:-1]+tpr[1:])/2))
    ap = float(np.sum(precision[hit==1])/tp[-1])
    return fpr, tpr, np.r_[0, recall], np.r_[1, precision], auc, ap


def roc(ax, d, c):
    truth = d["classification"]["truth"]
    for i, score in enumerate(d["classification"]["scores"]):
        fpr, tpr, _, _, auc, _ = classification_curves(truth, score)
        line,=ax.plot(fpr, tpr, c=c[i], lw=1.9, ls=LINES[i], label=f"Model {i+1}: {auc:.2f}")
        line.set_path_effects([patheffects.Stroke(linewidth=2.5,foreground="#9CA7AF",alpha=.55),patheffects.Normal()])
    ax.plot([0, 1], [0, 1], color=MUTED, lw=.7, ls=":")
    ax.set(xlim=(0, 1), ylim=(0, 1.03), xlabel="False-positive rate", ylabel="True-positive rate")
    ax.legend(loc="lower right", fontsize=6.5, title="ROC AUC", title_fontsize=7)


def precision_recall(ax, d, c):
    truth = d["classification"]["truth"]
    for i, score in enumerate(d["classification"]["scores"]):
        _, _, rec, prec, _, ap = classification_curves(truth, score)
        line,=ax.step(rec, prec, where="pre", c=c[i], lw=1.7, ls=LINES[i], label=f"Model {i+1}: {ap:.2f}")
        line.set_path_effects([patheffects.Stroke(linewidth=2.3,foreground="#9CA7AF",alpha=.55),patheffects.Normal()])
    ax.axhline(np.mean(truth), color=MUTED, lw=.7, ls=":")
    ax.set(xlim=(0, 1), ylim=(0, 1.03), xlabel="Recall", ylabel="Precision")
    ax.legend(loc="lower left", fontsize=6.5, title="Average precision", title_fontsize=7)


def bh_adjust(p):
    order = np.argsort(p); ranked = np.array(p)[order]*len(p)/np.arange(1, len(p)+1)
    adjusted = np.minimum.accumulate(ranked[::-1])[::-1]
    result = np.empty_like(adjusted); result[order] = np.minimum(adjusted, 1)
    return result


def volcano(ax, d, c):
    a, b = np.array(d["volcano"]["control"]), np.array(d["volcano"]["treated"])
    effect = b.mean(1)-a.mean(1); q = bh_adjust(stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue)
    y = -np.log10(q); masks = [(q<.05)&(effect < -1), ~((q<.05)&(np.abs(effect)>1)), (q<.05)&(effect>1)]
    for mask, color, label in zip(masks, c, ["Down", "Other", "Up"]):
        ax.scatter(effect[mask], y[mask], s=16, fc=color, ec=INK, lw=.3, alpha=.8, label=f"{label} ({mask.sum()})")
    ax.axhline(-np.log10(.05), color=MUTED, ls=":", lw=.7)
    for value in [-1, 1]:ax.axvline(value, color=MUTED, ls=":", lw=.7)
    ax.set(xlabel="Mean log2-expression difference", ylabel="−log10(BH q-value)")
    ax.legend(loc="upper center", ncol=3, fontsize=6.2, columnspacing=.5, handletextpad=.3)
    ax.set_ylim(-.2, y.max()*1.25)


def km_curve(time, event):
    order = np.argsort(time); t, e = np.array(time)[order], np.array(event)[order]
    probability = 1.0; xx, yy, cx, cy = [0.0], [1.0], [], []
    for i, (value, occurred) in enumerate(zip(t, e)):
        if occurred:probability *= (len(t)-i-1)/(len(t)-i)
        xx.append(value); yy.append(probability)
        if not occurred:cx.append(value); cy.append(probability)
    return np.array(xx), np.array(yy), cx, cy


def survival(ax, d, c):
    for i, group in enumerate(d["survival"]):
        t, y, cx, cy = km_curve(group["time"], group["event"])
        line,=ax.step(t, y, where="post", c=c[i], lw=1.8, ls=LINES[i], label=f"Cohort {i+1}")
        line.set_path_effects([patheffects.Stroke(linewidth=2.4,foreground="#9CA7AF",alpha=.55),patheffects.Normal()])
        ax.scatter(cx, cy, c=c[i], marker="|", s=20, linewidths=.9)
    ax.set(xlim=(0, 18), ylim=(0, 1.04), xlabel="Time (months)", ylabel="Survival probability")
    ax.legend(loc="upper right", fontsize=6.5)


def stacked(ax, d, c):
    value = np.array(d["composition"]).mean(1)*100; bottom = np.zeros(4)
    for i in range(3):
        ax.bar(range(4), value[:, i], bottom=bottom, color=c[i], ec=INK, lw=.45,
               hatch=["", "//", ".."][i], label=f"State {i+1}", width=.6)
        bottom += value[:, i]
    ax.set(xticks=range(4), xticklabels=["Batch 1", "Batch 2", "Batch 3", "Batch 4"], ylabel="Composition (%)", ylim=(0, 122))
    ax.legend(ncol=3, fontsize=6.5, loc="upper left", columnspacing=.7, handlelength=1)


def area(ax, d, c):
    t = np.array(d["area"]["time"]); f = np.array(d["area"]["fractions"])*100
    ax.stackplot(t, f, colors=c, edgecolor="white", lw=.8)
    bottom = 0
    for i in range(3):
        middle = bottom+f[i, -1]/2
        ax.text(24.4, middle, f"S{i+1}", fontsize=7, va="center", color=INK)
        bottom += f[i, -1]
    ax.set(xlim=(0, 26), ylim=(0, 100), xlabel="Time (h)", ylabel="Share (%)")
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.grid(False)


def radar(ax, d, c):
    names = d["radar"]["labels"]; theta = np.linspace(0, 2*np.pi, len(names), endpoint=False)
    closed = np.r_[theta, theta[0]]
    for i, row in enumerate(d["radar"]["scores"]):
        ax.plot(closed, np.r_[row, row[0]], c=c[i], ls=LINES[i], lw=1.7, marker=MARKERS[i], ms=3, mec=INK, mew=.4, label=f"Profile {i+1}")
        ax.fill(closed, np.r_[row, row[0]], color=c[i], alpha=.08)
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
    ax.set_xticks(theta); ax.set_xticklabels(names, fontsize=7.5)
    ax.set_ylim(0, 100); ax.set_yticks([25, 50, 75, 100]); ax.set_yticklabels(["25", "50", "75", "100"], fontsize=6)
    ax.spines["polar"].set_color("#CAD1D6"); ax.grid(color="#E1E7EB", lw=.6)
    ax.legend(loc="upper center", bbox_to_anchor=(.5,-.13), ncol=3, fontsize=6, columnspacing=.8)


def arrow(ax, points, dashed=False):
    path = MplPath(points, [MplPath.MOVETO]+[MplPath.LINETO]*(len(points)-1))
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=9,
                                color=MUTED, lw=1, ls="--" if dashed else "-", zorder=1))


def block(ax, xy, wh, label, color):
    ax.add_patch(FancyBboxPatch(xy, *wh, boxstyle="round,pad=0.008,rounding_size=0.02",
                              fc=color, ec="#63717C", lw=.8, zorder=3))
    ax.text(xy[0]+wh[0]/2, xy[1]+wh[1]/2, label, ha="center", va="center", fontsize=7.5, color=INK, zorder=4)


def network(ax, d, c):
    n = d["network"]; p = np.array(n["positions"])
    for a, b, weight in n["edges"]:
        ax.plot(p[[a,b], 0], p[[a,b], 1], color="#9CA9B2", lw=weight, zorder=1)
    for i, (x,y) in enumerate(p):
        ax.add_patch(Circle((x,y), .065, fc=c[i%3], ec=INK, lw=.8, zorder=3))
        ax.text(x,y,n["labels"][i],ha="center",va="center",fontsize=9,zorder=4)
    ax.set(xlim=(0,1),ylim=(0,1),aspect="equal"); ax.axis("off")


def flowchart(ax, d, c):
    n=d["flowchart"]["nodes"]
    arrow(ax,[(.23,.70),(.32,.70)]);arrow(ax,[(.50,.70),(.56,.70)])
    arrow(ax,[(.76,.70),(.80,.70)]);arrow(ax,[(.66,.57),(.66,.36)])
    arrow(ax,[(.55,.28),(.41,.28),(.41,.61)],True)
    block(ax,(.05,.61),(.18,.18),n[0],c[0]);block(ax,(.32,.61),(.18,.18),n[1],c[1])
    ax.add_patch(Polygon([[.66,.83],[.76,.70],[.66,.57],[.56,.70]],fc=c[2],ec="#63717C",lw=.8,zorder=3))
    ax.text(.66,.70,n[2],ha="center",va="center",fontsize=7.5,zorder=4)
    block(ax,(.80,.61),(.17,.18),"Plot +\nexport",c[1]);block(ax,(.55,.20),(.21,.16),n[4],c[0])
    ax.text(.78,.84,"Yes",ha="center",fontsize=7);ax.text(.69,.45,"No",fontsize=7)
    ax.text(.28,.30,"retry",fontsize=7,color=MUTED)
    ax.set(xlim=(0,1.02),ylim=(0,1));ax.axis("off")


def architecture(ax, d, c):
    nodes=d["architecture"]["nodes"]
    arrow(ax,[(.18,.53),(.23,.53),(.23,.76),(.28,.76)])
    arrow(ax,[(.23,.53),(.23,.37),(.28,.37)])
    arrow(ax,[(.45,.76),(.51,.76),(.51,.62),(.57,.62)])
    arrow(ax,[(.45,.37),(.51,.37),(.51,.50),(.57,.50)])
    arrow(ax,[(.73,.56),(.81,.56)]);arrow(ax,[(.90,.46),(.90,.24)],True)
    arrow(ax,[(.72,.15),(.81,.15)],True)
    block(ax,(.03,.44),(.15,.18),nodes[0],c[0]);block(ax,(.28,.67),(.17,.18),nodes[1],c[1])
    block(ax,(.28,.28),(.17,.18),nodes[2],c[2]);block(ax,(.57,.46),(.16,.20),nodes[3],c[0])
    block(ax,(.81,.46),(.18,.20),nodes[4],c[1]);block(ax,(.57,.08),(.15,.14),nodes[5],c[2]);block(ax,(.81,.08),(.18,.16),nodes[6],c[0])
    ax.set(xlim=(0,1.03),ylim=(0,1));ax.axis("off")


SPECS = [
    ("01_grouped_bar","Grouped bar","分组柱状图",0,"warm-orange","Mean ± SD; n=8 per cell",grouped_bar),
    ("02_trend","Trend + uncertainty","趋势与误差带",0,"warm-orange","Mean ± SD across 8 trajectories",trend),
    ("03_paired","Paired slope plot","配对斜率图",0,"warm-orange","14 matched units; individual observations",paired),
    ("04_forest","Forest / interval plot","森林与区间图",0,"warm-orange","95% t intervals; 12 paired units per row",forest),
    ("05_lollipop","Lollipop ranking","棒棒糖排序图",0,"warm-orange","Assigned signal strengths; stems start at zero",lollipop),
    ("06_waterfall","Waterfall","瀑布图",0,"warm-orange","Signed changes reconcile with final total",waterfall),
    ("07_box","Box + observations","箱线与观测点",1,"purple-blue-pink","Median / IQR; 60 observations per group",box),
    ("08_violin","Violin distribution","小提琴分布图",1,"purple-blue-pink","Density + median / IQR; n=60 per group",violin),
    ("09_histogram","Histogram + KDE","直方与密度图",1,"purple-blue-pink","Density normalization; Gaussian KDE",histogram),
    ("10_ridge","Ridgeline density","山脊密度图",1,"purple-blue-pink","Five batches; 120 values per batch",ridge),
    ("11_regression","Scatter + regression","回归散点图",1,"purple-blue-pink","OLS line; 95% interval for mean response",regression),
    ("12_bubble","Bubble plot","气泡图",1,"purple-blue-pink","Marker area encodes assigned volume",bubble),
    ("13_heatmap","Correlation heat map","相关热图",2,"skin-blue","Pearson r from 100 simulated observations",heatmap),
    ("14_pca","PCA embedding","PCA降维图",2,"skin-blue","SVD of standardized data; 135 observations",pca),
    ("15_roc","ROC curves","ROC曲线",2,"skin-blue","120 positives / 280 negatives; actual ranked AUC",roc),
    ("16_pr","Precision–recall curves","PR曲线",2,"skin-blue","AP from ranked predictions; baseline = prevalence",precision_recall),
    ("17_volcano","Volcano plot","火山图",2,"skin-blue","Welch tests + BH correction; n=12 per group",volcano),
    ("18_survival","Kaplan–Meier curves","生存曲线",2,"skin-blue","60 per cohort; ticks indicate censoring",survival),
    ("19_stacked","Stacked composition","堆叠组成柱状图",3,"purple-blue-pink","Mean fractions; 10 samples per batch",stacked),
    ("20_area","Stacked area","堆叠面积图",3,"purple-blue-pink","Three positive shares normalized to 100%",area),
    ("21_radar","Radar profile","雷达图",3,"purple-blue-pink","All axes use assigned 0–100 benefit scores",radar),
    ("22_network","Relationship network","关系网络图",3,"purple-blue-pink","Toy undirected graph; width = assigned weight",network),
    ("23_flowchart","Decision workflow","判断流程图",3,"purple-blue-pink","Toy logic; dashed line denotes retry",flowchart),
    ("24_architecture","Model architecture","模型架构图",3,"purple-blue-pink","Toy model; dashed paths are training-only",architecture),
]


def review_bounds(fig):
    fig.canvas.draw(); renderer=fig.canvas.get_renderer(); outside=[]
    for t in fig.findobj(Text):
        if t.get_visible() and t.get_text().strip():
            b=t.get_window_extent(renderer)
            if b.x0 < -1 or b.y0 < -1 or b.x1 > fig.bbox.width+1 or b.y1 > fig.bbox.height+1:outside.append(t.get_text())
    return outside


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--skill-dir",type=Path,default=Path.home()/".codex/skills/figure-foundry")
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location("figure_foundry_style",args.skill_dir/"scripts/figure_style.py")
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    root=Path(__file__).resolve().parent;out=root/"figures";out.mkdir(exist_ok=True)
    data=json.loads((root/"synthetic_data.json").read_text(encoding="utf-8"))
    records=[]
    with matplotlib.rc_context(helper.style_settings()):
        for slug,title,zh,group,palette,note,draw in SPECS:
            fig=plt.figure(figsize=(6.4,4.7))
            ax=fig.add_axes([.16,.18,.73,.59],projection="polar" if draw is radar else None)
            if draw not in [radar,network,flowchart,architecture]:clean(ax)
            draw(ax,data,helper.get_palette(palette))
            fig.text(.09,.94,f"{slug[:2]}  {title}",fontsize=14,fontweight="bold",va="top")
            fig.text(.09,.865,note,fontsize=8,color=MUTED)
            fig.text(.09,.055,"SYNTHETIC DATA / TOY SCHEMATIC  ·  FigureFoundry",fontsize=7.5,color=MUTED)
            files=helper.export_figure(fig,out/slug,dpi=300)
            records.append({"id":slug,"title":title,"title_zh":zh,"group":group+1,"palette":palette,
                            "note":note,"kind":"schematic" if draw in [network,flowchart,architecture] else "quantitative",
                            "text_outside_canvas":review_bounds(fig),"files":{k:Path(v).name for k,v in files.items()}})
            plt.close(fig)
        group_names=["Comparisons & change","Distributions & relationships","Scientific analysis","Composition & structure"]
        for group,name in enumerate(group_names):
            fig=plt.figure(figsize=(15,9.7));fig.subplots_adjust(left=.065,right=.95,bottom=.10,top=.83,wspace=.42,hspace=.72)
            fig.text(.055,.955,f"FigureFoundry  /  {group+1:02d}",fontsize=18,fontweight="bold",va="top")
            fig.text(.055,.905,name,fontsize=12,color=MUTED)
            fig.text(.95,.91,"SYNTHETIC EXAMPLES",ha="right",fontsize=10,color=MUTED)
            for pos,item in enumerate([s for s in SPECS if s[3]==group],1):
                slug,title,zh,_,palette,note,draw=item
                ax=fig.add_subplot(2,3,pos,projection="polar" if draw is radar else None)
                if draw not in [radar,network,flowchart,architecture]:clean(ax)
                draw(ax,data,helper.get_palette(palette))
                ax.set_title(f"{slug[:2]}  {title}",loc="left",fontsize=10,pad=26,fontweight="bold")
                if draw is not radar:
                    ax.text(0,1.025,note,transform=ax.transAxes,fontsize=6.8,color=MUTED,va="bottom")
            fig.text(.055,.035,"All numerical inputs are simulated. Schematics describe toy relationships, not real scientific claims.",fontsize=8,color=MUTED)
            files=helper.export_figure(fig,root/f"gallery_{group+1:02d}",dpi=180)
            records.append({"id":f"gallery_{group+1:02d}","title":name,"kind":"contact_sheet","text_outside_canvas":review_bounds(fig),"files":{k:Path(v).name for k,v in files.items()}})
            plt.close(fig)
    (root/"gallery_checks.json").write_text(json.dumps({"skill":"figure-foundry","synthetic":True,"seed":data["seed"],"records":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"individual_examples":24,"contact_sheets":4,"formats":["png","svg","pdf"],"outside_canvas":{x['id']:x['text_outside_canvas'] for x in records if x['text_outside_canvas']}},ensure_ascii=False,indent=2))


if __name__=="__main__":main()
