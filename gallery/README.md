# FigureFoundry example gallery

[Project home](../README.md) · [中文图型索引](GALLERY.md) · [Offline HTML viewer](index.html)

24 individual examples: 21 numerical plots and three editable schematics. All numerical inputs are seeded synthetic data (seed 261026); schematic relationships are fictional. Each PNG, SVG and PDF comes from the same plotting scene.

## 1. Comparisons and change

![Comparisons and change](gallery_01.png)

| ID | Figure type | Input or calculation | Exports |
|---|---|---|---|
| 01 | Grouped bar | Mean ± SD; n=8 per cell | [PNG](figures/01_grouped_bar.png) · [SVG](figures/01_grouped_bar.svg) · [PDF](figures/01_grouped_bar.pdf) |
| 02 | Trend + uncertainty | Mean ± SD across 8 trajectories | [PNG](figures/02_trend.png) · [SVG](figures/02_trend.svg) · [PDF](figures/02_trend.pdf) |
| 03 | Paired slope plot | 14 matched units; individual observations | [PNG](figures/03_paired.png) · [SVG](figures/03_paired.svg) · [PDF](figures/03_paired.pdf) |
| 04 | Forest / interval plot | 95% t intervals; 12 paired units per row | [PNG](figures/04_forest.png) · [SVG](figures/04_forest.svg) · [PDF](figures/04_forest.pdf) |
| 05 | Lollipop ranking | Assigned signal strengths; stems start at zero | [PNG](figures/05_lollipop.png) · [SVG](figures/05_lollipop.svg) · [PDF](figures/05_lollipop.pdf) |
| 06 | Waterfall | Signed changes reconcile with final total | [PNG](figures/06_waterfall.png) · [SVG](figures/06_waterfall.svg) · [PDF](figures/06_waterfall.pdf) |

## 2. Distributions and relationships

![Distributions and relationships](gallery_02.png)

| ID | Figure type | Input or calculation | Exports |
|---|---|---|---|
| 07 | Box + observations | Median / IQR; 60 observations per group | [PNG](figures/07_box.png) · [SVG](figures/07_box.svg) · [PDF](figures/07_box.pdf) |
| 08 | Violin distribution | Density + median / IQR; n=60 per group | [PNG](figures/08_violin.png) · [SVG](figures/08_violin.svg) · [PDF](figures/08_violin.pdf) |
| 09 | Histogram + KDE | Density normalization; Gaussian KDE | [PNG](figures/09_histogram.png) · [SVG](figures/09_histogram.svg) · [PDF](figures/09_histogram.pdf) |
| 10 | Ridgeline density | Five batches; 120 values per batch | [PNG](figures/10_ridge.png) · [SVG](figures/10_ridge.svg) · [PDF](figures/10_ridge.pdf) |
| 11 | Scatter + regression | OLS line; 95% interval for mean response | [PNG](figures/11_regression.png) · [SVG](figures/11_regression.svg) · [PDF](figures/11_regression.pdf) |
| 12 | Bubble plot | Marker area encodes assigned volume | [PNG](figures/12_bubble.png) · [SVG](figures/12_bubble.svg) · [PDF](figures/12_bubble.pdf) |

## 3. Scientific analysis

![Scientific analysis](gallery_03.png)

| ID | Figure type | Input or calculation | Exports |
|---|---|---|---|
| 13 | Correlation heat map | Pearson r from 100 simulated observations | [PNG](figures/13_heatmap.png) · [SVG](figures/13_heatmap.svg) · [PDF](figures/13_heatmap.pdf) |
| 14 | PCA embedding | SVD of standardized data; 135 observations | [PNG](figures/14_pca.png) · [SVG](figures/14_pca.svg) · [PDF](figures/14_pca.pdf) |
| 15 | ROC curves | 120 positives / 280 negatives; actual ranked AUC | [PNG](figures/15_roc.png) · [SVG](figures/15_roc.svg) · [PDF](figures/15_roc.pdf) |
| 16 | Precision–recall curves | AP from ranked predictions; baseline = prevalence | [PNG](figures/16_pr.png) · [SVG](figures/16_pr.svg) · [PDF](figures/16_pr.pdf) |
| 17 | Volcano plot | Welch tests + BH correction; n=12 per group | [PNG](figures/17_volcano.png) · [SVG](figures/17_volcano.svg) · [PDF](figures/17_volcano.pdf) |
| 18 | Kaplan–Meier curves | 60 per cohort; ticks indicate censoring | [PNG](figures/18_survival.png) · [SVG](figures/18_survival.svg) · [PDF](figures/18_survival.pdf) |

## 4. Composition and structure

![Composition and structure](gallery_04.png)

| ID | Figure type | Input or calculation | Exports |
|---|---|---|---|
| 19 | Stacked composition | Mean fractions; 10 samples per batch | [PNG](figures/19_stacked.png) · [SVG](figures/19_stacked.svg) · [PDF](figures/19_stacked.pdf) |
| 20 | Stacked area | Three positive shares normalized to 100% | [PNG](figures/20_area.png) · [SVG](figures/20_area.svg) · [PDF](figures/20_area.pdf) |
| 21 | Radar profile | All axes use assigned 0–100 benefit scores | [PNG](figures/21_radar.png) · [SVG](figures/21_radar.svg) · [PDF](figures/21_radar.pdf) |
| 22 | Relationship network | Toy undirected graph; width = assigned weight | [PNG](figures/22_network.png) · [SVG](figures/22_network.svg) · [PDF](figures/22_network.pdf) |
| 23 | Decision workflow | Toy logic; dashed line denotes retry | [PNG](figures/23_flowchart.png) · [SVG](figures/23_flowchart.svg) · [PDF](figures/23_flowchart.pdf) |
| 24 | Model architecture | Toy model; dashed paths are training-only | [PNG](figures/24_architecture.png) · [SVG](figures/24_architecture.svg) · [PDF](figures/24_architecture.pdf) |

## Reproduce and inspect

From the repository root, install the pinned requirements and run:

```bash
python gallery/generate_data.py
python gallery/render_gallery.py --skill-dir skill/figure-foundry
python gallery/build_index.py
python gallery/verify_gallery.py
```

Inputs: [JSON](synthetic_data.json). Source: [generator](generate_data.py), [renderer](render_gallery.py). Checks: [verification](verification.json), [verification script](verify_gallery.py).

Bars and trends show mean ± sample SD across eight simulated runs. Forest intervals use 12 paired differences per row and a 95% t interval. Regression shading is a 95% interval for the mean response. ROC/AP, PCA, Welch tests/BH correction and survival curves are calculated from the saved inputs. Stacked compositions total 100%. Radar axes use assigned 0–100 benefit scores.

Network edges are toy associations. The decision workflow uses a dashed retry path. Model architecture uses solid data flow and dashed training-only paths.

The Kaplan–Meier example uses untied event times. Native PPTX/draw.io/Origin output was not run. HTML asset links were checked; viewer interaction was not browser-tested.
