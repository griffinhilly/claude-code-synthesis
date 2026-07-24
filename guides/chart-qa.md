# Chart QA Checklist & Pipeline

Two layers: the self-check to run as you build individual charts, and the batch vision-QA pipeline to run across a whole report package before shipping.

## Layer 1 — Inline checklist (every chart)

When generating matplotlib/visualization charts, verify these before shipping:

### Overlap & Collision
- Bars with negative values: enough xlim padding so they don't overlap y-axis labels or spines (explicit `ax.set_xlim(vmin - pad, vmax + pad)`, never rely on auto-scaling for mixed-sign data).
- Value labels: have room to render without colliding with axis lines, other labels, bars, or the chart title. For above-bar labels, add top-of-axis headroom via `ax.set_ylim(top=max + headroom)` or `ax.margins(y=0.2)`.
- Legends: don't overlap data area or axis labels. For horizontal bar charts, never use `loc="lower right"` — it clips the bottom bar. Place below the chart with clearance for BOTH x-axis label AND legend (`loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=...` combined with `fig.tight_layout(rect=[0, 0.15, 1, 1])`).
- Title↔label collisions: when data labels sit above bars and the title sits above the plot, either `set_title(..., pad=14)` or reserve ylim headroom of ~20–25% above max data value.
- Endpoint labels on line/scatter charts: if labels are `ha="center"` on the first/last data x-position, add x-axis padding — e.g., `ax.set_xlim(x_min - 0.35*x_range, x_max + 0.35*x_range)` — or they will clip.
- Scatter plot label overlaps: when a highlight label and a reference label can fall at the same coordinates, use a proximity filter — skip reference labels within ~0.45 z-score units of the highlight and ~0.25 of a prior reference.
- Two data series with near-identical values at the same x: use a rank-based vertical stagger (lowest below point, middle +0.12 above, top +0.28 above) to keep labels separated in data coordinates.

### Sizing & Layout
- `figsize` width matches the container the chart renders in (e.g., 1200px container needs figsize width ~10+, not 7).
- Height scales with number of items (`n_items * 0.4` minimum for horizontal bar charts).
- Small-multiples polar/radar grids: each subplot needs ≥3.5 inches per side, otherwise axis labels and polygons collide.
- `tight_layout()` called before `fig_to_base64()` or `savefig()`.
- `subplots_adjust` and `tight_layout(rect=...)` fight each other — use one, not both.

### Data-Driven Limits
- Compute xlim/ylim from actual data min/max + label padding — never rely on matplotlib auto-scaling for charts with mixed positive/negative values.
- Asymmetric limits: use `min(data_min - pad, -small)` and `max(data_max + pad, small)`, not symmetric `(-max_abs, +max_abs)`.

### Label Truncation
- Don't truncate category/tick labels with fixed-length slicing (`name[:16]`). Use the full name and let `bbox_inches="tight"` handle the margin. Truncated labels that collide (e.g. an ambiguous shortened category name covering several distinct groups) are a reader-confusing bug, not a cosmetic issue.

### Font & Spine Standards
- Tick labels ≥ 8pt, axis labels ≥ 10pt, titles ≥ 12pt, in-bar annotations ≥ 7pt.
- Remove top and right spines always.

---

## Layer 2 — Batch vision-QA pipeline

### Why this exists

A large client report package once ran the first version of this pipeline against 769 charts. Vision-QA found **71 layout defects across 66 charts (21 high-severity → 0 after fixes, 92% reduction)**. Most defects were cosmetic, but one was load-bearing: a shared bar-chart helper had a silent `xlim=0` lower bound that was clipping every negative-value bar — a correctness bug that had been shipping undetected because deterministic bbox-overlap checks couldn't see "data is missing from the chart." Without vision-QA, that bug stays in the report. The pipeline isn't overhead; it's a second net for the class of defects that look cosmetic but aren't.

For any multi-chart report, run this before declaring a deliverable done. Never assume a chart "looks fine" just because the generator succeeded.

### Pipeline

1. **Extract** — dump every embedded chart PNG from the HTML outputs to a flat directory.
2. **Resize** — downscale anything over 1600px on the long edge (Claude's many-image vision context limit is 2000px; leave headroom).
3. **Chunk** — split the PNG list into ~12 chunks of ~60 charts each.
4. **Fleet** — spawn one vision-critic subagent per chunk, parallel, each writing findings_chunk_N.json.
5. **Aggregate** — merge per-chunk findings, cluster by (generator script × issue type), severity-rank.
6. **Fix** — work the high-severity clusters first; each cluster usually traces to a single function.
7. **Regenerate + re-extract** affected deliverables.
8. **Re-verify** — targeted re-scan of previously-defective charts + random sample to catch regressions.
9. **Iterate** — 2-3 rounds is normal for a large package; don't expect one-shot perfection.

### 10-issue checklist (copy into subagent prompts verbatim)

```
- title_label_overlap — data label / value annotation / legend overlaps the chart title
- axis_label_clip — axis tick labels clipped/truncated at figure edge
- legend_data_collision — legend box overlaps bars, lines, points
- xlabel_legend_overlap — x-axis label and legend overlap each other
- annotation_outside_axes — value annotation falls outside plot area
- bar_extends_past_axis — bars with negative values extend past axis line into labels
- overlapping_data_labels — two or more data labels overlap each other
- title_cropped — title cut off at figure edge
- axis_tick_crowding — tick labels so dense they visibly overlap each other
- other_overlap — any other visible layout defect
```

Each finding returned as JSON: `{"file", "issue", "severity" (high/medium/low), "description"}`. Severity rubric: `high` = unreadable/shipping-blocker, `medium` = visible but usable, `low` = cosmetic.

### Reusable scripts (port to other projects as needed)

- `scripts/extract_charts_for_qa.py` — extracts embedded base64 PNGs → `output/qa_charts/{prefix}__{stem}__{idx:02d}.png` + manifest.json
- `scripts/aggregate_qa_findings.py` — merges findings_chunk_*.json, clusters by (script × issue), writes _findings_summary.md

Resize snippet:
```python
from PIL import Image
import os
for f in os.listdir("output/qa_charts"):
    if not f.endswith(".png"): continue
    p = f"output/qa_charts/{f}"
    im = Image.open(p)
    if max(im.size) > 1600:
        s = 1600 / max(im.size)
        im.resize((int(im.size[0]*s), int(im.size[1]*s)), Image.LANCZOS).save(p, optimize=True)
```

### When to run
- Before declaring any report package "done" for review.
- After any refactor of `viz.py` or a chart-heavy generator script.
- After a brand/style migration that changes palette or typography (visual regressions often break label placement).

### Don't bother running
- On a single ad-hoc chart — inline checklist above is sufficient.
- On charts that the generator doesn't emit as PNG (pure HTML tables, D3 SVGs).
