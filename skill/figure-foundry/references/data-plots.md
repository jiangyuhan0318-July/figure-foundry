# Numerical research figures

## Data and statistics

1. Read the actual table or arrays and identify identifiers, conditions, variables, units, missing values, and the independent experimental unit. Keep technical replicates or repeated observations linked to their parent unit.
2. Preserve the data at the precision needed to regenerate the marks. Record filtering, derived variables, normalization, and aggregation. Do not silently discard rows.
3. Choose a plot for the question: lines for ordered trends; paired points for matched units; points/intervals for group estimates; box/violin plus observations for distributions; scatter for relationships or trade-offs; heat maps for matrices. A bar chart is not the automatic default for every comparison.
4. Show raw independent observations where readable. Define every interval as SD, SE, CI, or another specified quantity and record how it was computed. Do not use training epochs, cells within the same specimen, or repeated measurements as independent replicates without a justified design.
5. Significance marks require an actual appropriate test and its comparison/unit definition. An error bar is not itself a significance test. Synthetic examples normally need descriptive summaries, not claims about real-world effectiveness.

For synthetic demonstrations, save a seeded generator and generated CSV/JSON, document the mechanism and independent simulated unit, and put a synthetic-data label on the final image and caption. The plotting entrypoint must read those saved data rather than quietly substituting new embedded values.

## Plot design

- Use consistent category order, colors, markers, and units across panels. Use the exact saved palette values as the category colors; dark neutral borders and distinct line/marker shapes improve the readability of pale fills.
- Keep axis ranges comparable when the comparison requires it. Bars normally start at zero. A narrowed range can be suitable for points or trends when the bounds are visible and do not hide material variation.
- Explain percentages versus percentage-point differences and every normalization denominator. Avoid dual axes unless the comparison needs them and the mapping is clear.
- Put legends in stable, non-overlapping positions; direct labels are useful when only a few series are present. Do not cover observations with a legend.
- Use readable text at the actual delivery width. A practical starting size is about 180 mm wide with 8–10 pt labels; it is a design assumption, not a universal publisher requirement.
- Use a scoped Matplotlib `rc_context`, not a global style mutation. Embed PDF fonts where supported and keep SVG text editable. Fonts must support the chosen labels.

## Build and verification

Start with an explicit panel arrangement and one color/marker registry. A concise usage note should name source files, independent unit, aggregation, interval definition, palette mapping, and intended size. A simple figure needs no multi-file schema framework.

The included `scripts/figure_style.py` can be imported from its installed location. It supplies `get_palette`, `style_settings`, and `export_figure`; it requires Matplotlib only when the plotting route is used. Use available plotting packages, and report a concrete missing dependency if the selected route cannot run.

Render a preview. Inspect both the complete image and any dense panel. Correct clipping, collisions, ambiguous marks, misleading ranges, or labels that are too small. Export again from the same source; do not resize the document after layout to repair the figure.

Verify the data-to-statistic path separately from appearance: observation counts, summary values, uncertainty definitions, and plotted coordinates/labels. Check exported canvas dimensions. Deliver the script, data, caption, preview/vector files, and the checks actually performed.
