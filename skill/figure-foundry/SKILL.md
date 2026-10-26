---
name: figure-foundry
description: Create and refine scientific data plots, method diagrams, and mixed research figures with traceable data, editable source, saved palettes, and inspection of the actual rendered output. Use for 科研绘图、实验结果图、论文架构图、机制图 and multi-panel figures.
license: Apache-2.0
---

# FigureFoundry

Build a figure that answers one clear research question, preserves the source's meaning, and remains readable at its intended size. This is one integrated workflow; the upstream skills are not runtime dependencies.

## 1. Establish the figure brief once

Identify the audience, question, inputs, output format, approximate final width, and any accepted project style. Reuse information already supplied. State routine assumptions and continue; ask only when missing data or an ambiguous scientific relationship changes the figure's meaning.

Choose the relevant route:

| Content | Read | Authoring route |
|---|---|---|
| Numerical evidence: trends, comparisons, distributions, heat maps | [references/data-plots.md](references/data-plots.md) | Code that reads the source data, normally Matplotlib or an existing project renderer. |
| Relationships: architecture, mechanisms, workflows | [references/diagrams.md](references/diagrams.md) | Editable vector objects, normally SVG; use native PPTX when that is the requested working format. |
| Mixed figure | Both references, only applicable sections | Keep data panels source-derived; align schematic and numerical panels in one composition. |

Separate observed data, predictions, hypotheses, illustrations, and decoration. Do not infer missing measurements or add scientific modules for visual balance. When synthetic data are authorized, fix a seed and label the figure, caption, and data notes as synthetic.

## 2. Select visual references without blocking the task

Use an existing accepted figure, a user-selected example, or a small set of relevant visible previews. Inspect the actual image, not just its title. Borrow hierarchy, spacing, and encoding, while keeping the new figure's scientific content original and source-correct.

If the user has not requested a gallery-selection session, choose a suitable reference and explain the choice briefly. If no relevant reference is accessible, design directly from the visual question and disclose that no external preview was used. A large remote gallery, preference database, user voting round, and image-generation call are optional aids.

## 3. Use one style and encoding registry

Priority: explicit task instructions → accepted project style → saved personal palettes → a disclosed suitable default. Preserve category identities across panels.

[assets/palettes.json](assets/palettes.json) stores the exact three-color groups:

- `warm-orange` / 暖橙组
- `purple-blue-pink` / 紫蓝粉组
- `skin-blue` / 浅肤蓝组

Keep their hex values and order. Use pale colors as fills or pair them with dark strokes, readable labels, markers, hatches, or line styles; color alone must not carry identity. Neutral text and outlines are separate utility colors. Add colors only when the task requires them and record the extension.

Prefer a white canvas, restrained gridlines, aligned labels, meaningful grouping, and a clear visual anchor. Use available, language-compatible fonts. Retain an accepted dark or branded style when the user requests it. Do not load web fonts or change a saved style file merely to make a figure.

## 4. Plan one complete composition, then build it

Write a compact brief containing panel jobs, reading order, visual encodings, source files, and statistics or arrow meanings. For a simple figure this can be a few lines in the usage note; a many-panel figure may need a separate specification.

Allocate space by information and comparison needs. Equal panels are appropriate for matched comparisons; unequal panels can emphasize the main result. Remove redundant labels and decorative boxes, while preserving necessary scientific content. Avoid arbitrary node limits or a fixed number of panels.

Author at the final physical size. Keep one authoritative source: the plotting script, vector scene, or native editable document. Derive exports from that source. For numerical plots, [scripts/figure_style.py](scripts/figure_style.py) provides local style settings, saved-palette lookup, and consistent PNG/SVG/PDF export; use it when Matplotlib is the chosen renderer.

## 5. Inspect and revise the real output

First check the complete render and reading order; then inspect labels, uncertainty, source meaning, and local details at the intended size. Revise only demonstrated issues and export again after changes. Stop when the figure answers its question, the checks pass, and further decoration adds no value.

Check:

- Source values, exclusions, units, denominators, and transformations reconcile with visible marks.
- Independent units and interval definitions are correct; schematic arrows do not imply unsupported causation.
- Text, ticks, legend, arrows, and panel boundaries do not collide or clip; categories remain distinguishable without color alone.
- The saved PNG opens, the SVG/PDF has the intended canvas size, and an editable source is delivered.

A file-format or schema check does not replace visual inspection. If a route or output could not be tested, state that specific gap rather than marking it passed.

## 6. Deliver the smallest complete artifact set

Respect explicitly requested formats. Otherwise provide a PNG preview and vector export (SVG or PDF), with the script/vector source. For data figures include the portable data used, the caption, and a short usage/QA note with the selected route, palette, inspected reference, checks actually run, and remaining limitations. Keep unrelated user files and manuscripts unchanged.

For exact journal submission requirements, verify the named venue's current instructions; an ordinary illustrative example does not require a publisher-policy audit. Third-party source data and artwork keep their own licenses.

Read [references/sources-and-decisions.md](references/sources-and-decisions.md) for upstream attribution, the star-count snapshot, and the duplicate/conflict decisions. License texts and upstream notices are preserved under `LICENSES/` and `NOTICE`.
