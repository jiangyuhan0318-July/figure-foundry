# FigureFoundry

**From source data and method relationships to editable research figures.**

[English](README.md) · [简体中文](README.zh-CN.md) · [24-example gallery](gallery/README.md) · [Download the skill](figure-foundry-skill.zip)

FigureFoundry is a scientific-figure skill built through deliberate selection, rewriting, and recombination of practical ideas from [Diagram Design](https://github.com/cathrynlavery/diagram-design), [AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery), and [Open Research Skills](https://github.com/gxCaesar/open-research-skills). The project brings numerical plots and method diagrams into one workflow, with integrated routing, saved palettes, an export helper, and verification examples.

**Brief → source-aware design → editable construction → inspect the render → verify and deliver.**

## What makes it useful

The contribution is the way the workflow has been rebuilt around everyday research tasks:

| Design choice | What FigureFoundry does | Practical benefit |
|---|---|---|
| Two authoring routes | Routes measured values to data plotting, and relationships to editable schematics. | Statistical curves and workflow connectors each follow rules appropriate to their meaning. |
| One brief, one review loop | Reuses known preferences and combines repeated style, layout, and quality checks. | Ordinary tasks can proceed without repeated onboarding or a required gallery-voting session. |
| Outputs follow the task | Uses code-driven PNG/SVG/PDF for plots and editable vector scenes for diagrams; other formats follow the request. | The workflow fits both paper figures and further editing. |
| Three consistent palettes | Keeps exact saved colors, adding markers, line styles, hatches, and neutral outlines where needed. | Pale colors remain usable and categories have a second identification channel. |
| Traceable calculations | Reads saved inputs, defines the independent unit and uncertainty, and retains the generator and plotting source. | Readers can reproduce the example and inspect how values become marks. |
| Inspection of real exports | Opens the output, checks layout and calculations, corrects observed problems, and records what was tested. | Quality claims point to inspectable artifacts and checks. |
| Lightweight installation | The installed skill is ten files; upstream repositories and large reference galleries are optional. | Users can adopt the combined workflow without installing three separate skill systems. |

These are concrete workflow changes relative to the selected source instructions. The [decision record](skill/figure-foundry/references/sources-and-decisions.md) maps the original requirements to the new choices.

## A workflow example

This is the generated decision-flow example, rendered from saved toy relationships. Solid arrows carry the forward process; the dashed arrow returns invalid input for correction.

![Synthetic decision workflow](gallery/figures/23_flowchart.png)

[Editable SVG](gallery/figures/23_flowchart.svg) · [PDF](gallery/figures/23_flowchart.pdf) · [Toy model architecture](gallery/figures/24_architecture.png) · [Source code](gallery/render_gallery.py) · [Inputs](gallery/synthetic_data.json)

## 24 examples, with source and checks

All numerical examples use **seeded synthetic data**. Network, workflow, and architecture examples use toy relationships. Every individual figure is available as PNG, SVG, and PDF.

| Group | Examples |
|---|---|
| Comparisons and change | Grouped bars, trend bands, paired slopes, forest intervals, lollipop rankings, waterfall |
| Distributions and relationships | Box plots, violins, histograms/KDE, ridgelines, regression scatter, bubbles |
| Scientific analysis | Correlation heat map, PCA, ROC, precision–recall, volcano plot, Kaplan–Meier curves |
| Composition and structure | Stacked bars, stacked area, radar profiles, relationship network, decision workflow, model architecture |

[Browse the illustrated gallery](gallery/README.md) · [中文图型索引](gallery/GALLERY.md) · [Download figures, code, data, and skill](figure-foundry-gallery.zip)

The [offline HTML viewer](gallery/index.html) offers filtering, search, and enlarged images when opened locally. On GitHub, use the illustrated Markdown gallery above; download the repository to use the HTML viewer.

<details>
<summary>Preview all four six-figure boards</summary>

![Comparisons and change](gallery/gallery_01.png)

![Distributions and relationships](gallery/gallery_02.png)

![Scientific analysis](gallery/gallery_03.png)

![Composition and structure](gallery/gallery_04.png)

</details>

The original three-panel demonstration also includes [CSV data](demo/synthetic_data.csv), [generator](demo/generate_data.py), [plotting source](demo/plot_demo.py), [caption](demo/caption.zh-CN.md), and [statistics](demo/plot_checks.json).

![Synthetic three-panel research figure](demo/synthetic_comparison.png)

## Install and use

Copy the entire [skill/figure-foundry](skill/figure-foundry) folder into your skills directory. For Codex, the default local destination is `~/.codex/skills/figure-foundry/`. Keep its references, assets, helper, and license files together.

Invoke it with a concrete figure request:

```text
$figure-foundry Plot this CSV using the warm-orange palette.
Show independent observations, define the error bars,
inspect the rendered image, and deliver editable source plus SVG/PDF.
```

```text
$figure-foundry Draw this method as an editable SVG.
Preserve the input branches and distinguish training-only connections.
```

The skill supplies instructions and resources. These examples were executed with **Python, Matplotlib, NumPy, and SciPy**. Origin is optional; native PPTX and Origin execution have not been exercised in this repository.

## Reproduce the examples

Tested with Python 3.13 and the package versions in [requirements.txt](requirements.txt). Run these commands from the repository root:

```bash
python -m pip install -r requirements.txt
python demo/generate_data.py
python demo/plot_demo.py --skill-dir skill/figure-foundry
python gallery/generate_data.py
python gallery/render_gallery.py --skill-dir skill/figure-foundry
python gallery/build_index.py
python gallery/verify_gallery.py
```

The generators save the inputs first; the plotting scripts read those files. The original demo uses seed `20261026`, and the gallery uses `261026`.

## Verification you can inspect

- **24 individual examples and four contact sheets:** 84 PNG/SVG/PDF files opened and checked for the expected dimensions.
- **Vector output:** all gallery SVGs contain native text and vector geometry, including heat-map cells; no embedded raster images.
- **Numerical checks:** ROC AUC/AP and PCA agree with scikit-learn; BH correction agrees with SciPy. Composition totals, the waterfall total, and survival risk-set products were also checked.
- **Visual review:** four actual contact sheets inspected; observed label, legend, connector, and vector-export problems corrected.
- **Skill checks:** frontmatter validated; installed and portable skill files compared byte for byte.

See [gallery verification](gallery/verification.json), the [verification script](gallery/verify_gallery.py), [package checks](verification.json), and the [Chinese usage audit](使用说明与自检.md).

The examples demonstrate the recorded tasks. A comparative quality or speed benchmark against the source skills has not been run. Native PPTX/draw.io/Origin output remains untested. HTML asset links were checked; viewer interaction was not browser-tested because the in-app browser blocks local file URLs. The Kaplan–Meier helper is demonstrated on untied synthetic event times.

## Three saved palettes

| Palette | Exact colors, in order |
|---|---|
| Warm orange | `#C8C8C8` · `#F1D5B3` · `#F29440` |
| Purple / blue / pink | `#A3A4CA` · `#6A94BA` · `#ECA9AA` |
| Skin / blue | `#FFDBD1` · `#D6E2EE` · `#0183BB` |

Colors are stored in [palettes.json](skill/figure-foundry/assets/palettes.json). The helper uses a scoped style context and exports multiple formats from one figure scene.

## Acknowledgments and license

This project draws on the following selected source instructions:

- [Diagram Design](https://github.com/cathrynlavery/diagram-design): visual hierarchy, meaningful relationships, connector and layout checks; MIT.
- [AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery): inspecting actual visual references and preserving category/style preferences; MIT.
- [Open Research Skills — build-scientific-visualizations](https://github.com/gxCaesar/open-research-skills/tree/c79bac60f882b626e1754bff95101441e165e4ec/skills/build-scientific-visualizations): source data, independent units, complete compositions, editable output, and rendering checks; Apache-2.0.

The instructions were selected, rewritten, and reorganized into a new skill. Source commits, selection criteria, and conflict resolutions are recorded in the [decision log](skill/figure-foundry/references/sources-and-decisions.md) and [dated repository snapshot](audit/repository-snapshot.json).

New work and the synthesis are licensed under [Apache-2.0](LICENSE). Original MIT notices are retained in [LICENSES](LICENSES), with attribution in [NOTICE](NOTICE). The figures and datasets published in this project are synthetic examples; third-party reference artwork and datasets are not included.
