# FigureFoundry：24种图型画廊

[浏览版画廊](index.html) · [返回项目首页](../README.md)

固定随机种子261026。所有数值为合成数据，网络/流程/架构使用虚构关系。每张图均从保存的JSON读取输入；PNG、SVG、PDF来自同一绘图场景。

本次实际生成21种数据图与3种示意图，不声称穷尽所有专业图型。PPTX与原生draw.io编辑本次未验证。

## 1. 比较与变化

![比较与变化](gallery_01.png)

| 编号 | 图型 | 常见用途 | 文件 |
|---|---|---|---|
| 01 | 分组柱状图 | Mean ± SD; n=8 per cell | [PNG](figures/01_grouped_bar.png) · [SVG](figures/01_grouped_bar.svg) · [PDF](figures/01_grouped_bar.pdf) |
| 02 | 趋势与误差带 | Mean ± SD across 8 trajectories | [PNG](figures/02_trend.png) · [SVG](figures/02_trend.svg) · [PDF](figures/02_trend.pdf) |
| 03 | 配对斜率图 | 14 matched units; individual observations | [PNG](figures/03_paired.png) · [SVG](figures/03_paired.svg) · [PDF](figures/03_paired.pdf) |
| 04 | 森林与区间图 | 95% t intervals; 12 paired units per row | [PNG](figures/04_forest.png) · [SVG](figures/04_forest.svg) · [PDF](figures/04_forest.pdf) |
| 05 | 棒棒糖排序图 | Assigned signal strengths; stems start at zero | [PNG](figures/05_lollipop.png) · [SVG](figures/05_lollipop.svg) · [PDF](figures/05_lollipop.pdf) |
| 06 | 瀑布图 | Signed changes reconcile with final total | [PNG](figures/06_waterfall.png) · [SVG](figures/06_waterfall.svg) · [PDF](figures/06_waterfall.pdf) |

## 2. 分布与关系

![分布与关系](gallery_02.png)

| 编号 | 图型 | 常见用途 | 文件 |
|---|---|---|---|
| 07 | 箱线与观测点 | Median / IQR; 60 observations per group | [PNG](figures/07_box.png) · [SVG](figures/07_box.svg) · [PDF](figures/07_box.pdf) |
| 08 | 小提琴分布图 | Density + median / IQR; n=60 per group | [PNG](figures/08_violin.png) · [SVG](figures/08_violin.svg) · [PDF](figures/08_violin.pdf) |
| 09 | 直方与密度图 | Density normalization; Gaussian KDE | [PNG](figures/09_histogram.png) · [SVG](figures/09_histogram.svg) · [PDF](figures/09_histogram.pdf) |
| 10 | 山脊密度图 | Five batches; 120 values per batch | [PNG](figures/10_ridge.png) · [SVG](figures/10_ridge.svg) · [PDF](figures/10_ridge.pdf) |
| 11 | 回归散点图 | OLS line; 95% interval for mean response | [PNG](figures/11_regression.png) · [SVG](figures/11_regression.svg) · [PDF](figures/11_regression.pdf) |
| 12 | 气泡图 | Marker area encodes assigned volume | [PNG](figures/12_bubble.png) · [SVG](figures/12_bubble.svg) · [PDF](figures/12_bubble.pdf) |

## 3. 科研分析

![科研分析](gallery_03.png)

| 编号 | 图型 | 常见用途 | 文件 |
|---|---|---|---|
| 13 | 相关热图 | Pearson r from 100 simulated observations | [PNG](figures/13_heatmap.png) · [SVG](figures/13_heatmap.svg) · [PDF](figures/13_heatmap.pdf) |
| 14 | PCA降维图 | SVD of standardized data; 135 observations | [PNG](figures/14_pca.png) · [SVG](figures/14_pca.svg) · [PDF](figures/14_pca.pdf) |
| 15 | ROC曲线 | 120 positives / 280 negatives; actual ranked AUC | [PNG](figures/15_roc.png) · [SVG](figures/15_roc.svg) · [PDF](figures/15_roc.pdf) |
| 16 | PR曲线 | AP from ranked predictions; baseline = prevalence | [PNG](figures/16_pr.png) · [SVG](figures/16_pr.svg) · [PDF](figures/16_pr.pdf) |
| 17 | 火山图 | Welch tests + BH correction; n=12 per group | [PNG](figures/17_volcano.png) · [SVG](figures/17_volcano.svg) · [PDF](figures/17_volcano.pdf) |
| 18 | 生存曲线 | 60 per cohort; ticks indicate censoring | [PNG](figures/18_survival.png) · [SVG](figures/18_survival.svg) · [PDF](figures/18_survival.pdf) |

## 4. 组成与结构

![组成与结构](gallery_04.png)

| 编号 | 图型 | 常见用途 | 文件 |
|---|---|---|---|
| 19 | 堆叠组成柱状图 | Mean fractions; 10 samples per batch | [PNG](figures/19_stacked.png) · [SVG](figures/19_stacked.svg) · [PDF](figures/19_stacked.pdf) |
| 20 | 堆叠面积图 | Three positive shares normalized to 100% | [PNG](figures/20_area.png) · [SVG](figures/20_area.svg) · [PDF](figures/20_area.pdf) |
| 21 | 雷达图 | All axes use assigned 0–100 benefit scores | [PNG](figures/21_radar.png) · [SVG](figures/21_radar.svg) · [PDF](figures/21_radar.pdf) |
| 22 | 关系网络图 | Toy undirected graph; width = assigned weight | [PNG](figures/22_network.png) · [SVG](figures/22_network.svg) · [PDF](figures/22_network.pdf) |
| 23 | 判断流程图 | Toy logic; dashed line denotes retry | [PNG](figures/23_flowchart.png) · [SVG](figures/23_flowchart.svg) · [PDF](figures/23_flowchart.pdf) |
| 24 | 模型架构图 | Toy model; dashed paths are training-only | [PNG](figures/24_architecture.png) · [SVG](figures/24_architecture.svg) · [PDF](figures/24_architecture.pdf) |

## 数据、统计与复跑

- 分组柱状/趋势：各单元8次模拟运行，显示均值±样本SD。配对图：14个匹配单位。森林图：每行12个配对差值的95% t区间。
- 箱线/小提琴/直方：每组60个样本；山脊图每批120个样本；回归图90个观测，阴影为均值响应的95%区间。
- PCA实际采用标准化输入的SVD；ROC/PR来自120阳性、280阴性的预测分数；火山图实际进行Welch检验与BH校正。
- 生存曲线由每队列60个事件/删失记录计算；本例时间不重复，未展示置信区间；不作为临床分析工具。
- 堆叠组成与面积图均核对总和100%；雷达图全部坐标都是人为指定的0–100“越高越好”分数。
- 模型图的实线为数据流、虚线为训练专用路径；流程图的虚线为返回修改；网络图不表达真实生物或因果关系。

```bash
python gallery/generate_data.py
python gallery/render_gallery.py
python gallery/build_index.py
```

从项目根目录运行，默认使用已安装的`figure-foundry`。也可向绘图脚本传入`--skill-dir skill/figure-foundry`，使用项目内便携副本。

完整输入：[synthetic_data.json](synthetic_data.json)；源代码：[生成器](generate_data.py)、[绘图脚本](render_gallery.py)；过程：[gallery_checks.json](gallery_checks.json)。
