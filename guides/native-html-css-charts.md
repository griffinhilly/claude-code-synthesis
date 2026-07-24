# Native HTML/CSS Charts — Design-Shop-Quality Graphics in Code

**One-line:** For report/publication-quality charts, render them as **native HTML/CSS (+ SVG)** through **headless Chrome**, not matplotlib. matplotlib plots data; it does not do page design. The professional polish a designer adds — typography, spacing, color discipline, layout, iconography — is all codeable, just not in matplotlib.

## When to reach for this (trigger)

- A chart/graphic is going in front of an external or senior audience (report, deck, working paper, client deliverable) and must look **professionally designed**, not "plotted."
- matplotlib output looks **amateurish, cramped, or illegible** — tiny text, default fonts, awkward spacing, oversized/wrong markers. (This is a recurring failure mode on client report work: matplotlib charts too small to read, off-brand, untrusted by reviewers.)
- You catch yourself post-processing matplotlib (scaling fonts, nudging layout) to fake polish — that's the signal you're using the wrong tool. **Stop and switch to HTML/CSS** rather than fighting matplotlib's ceiling.

**Do NOT** reach for this for quick internal/exploratory charts — matplotlib is faster and fine there. This is for *deliverables*.

## The two binding density rules

These are the most transferable rules from a large client-deck build — they drove every legibility round and apply to **any** chart/graphic for a real audience:

1. **Text as large as fits the page.** Each chart is one page; the binding constraint on label/element size is "as large as possible without overflow," not a fixed point size. Size the *densest* chart (the one with the most rows) until it just fills the page, and use that scale across the deck. A chart with small text and empty margin is a defect, not a neutral choice. (One deck locked at 19px row labels / ~31px rows on 1240px-wide pages, but the rule is the constraint, not the number.)
2. **Whitespace to the floor.** Inter-row margin = the **absolute minimum that still renders a distinguishable white gap, and no more**. Bars and dots nearly fill their rows; page padding is tight; aggregate gaps are hairlines. Every pixel of margin you don't need is a pixel stolen from legible content. Reduce margin first, *then* size text up into the reclaimed space.

These two compound: minimize margin → more room → larger text → more legible at the same page size. Do them together.

### Concrete starting anchor (the qualitative rule keeps getting under-applied)

"As large as fits" is true but keeps shipping as timid ~19–22px small-text-big-margin defects, because new chart code anchors on the wrong number and stops too early. Make it concrete — a pitch-graphics review once landed on: *"the fonts are not nearly as large as they can be… this is a recurring issue."*

- **Standalone / embedded charts need BIGGER text than a full-page deck.** A 32-page deck once locked 19px labels *because it's viewed at full page size*. A chart PNG dropped into a slide/pitch deck gets scaled **down**, so its text must be a large fraction of the canvas to survive. **Start ~28–32px row labels on a 1240px-wide page, not 19px.** The 19px is a deck number, not a floor.
- **Auxiliary text is not exempt — it's where "amateurish" lives.** Subtitle, legend, axis ticks, footer, and section/aggregate labels ("National," "Global") read illegible at 12–14px. Size them **17–24px**, and make section/aggregate headers *approach* the row-label size — not tiny grey afterthoughts floating in margin.
- **Order: whitespace to the floor FIRST, then size up.** Cut page padding, inter-row gaps, and section margins, *then* grow text into the reclaimed space. A big section-label margin with tiny text in it is the signature defect.
- **Mandatory verify (don't trust the thumbnail).** After rendering, crop the densest region at native (2×) resolution and confirm text fills its rows/cells with only hairline gaps and **no overflow/ellipsis**. Eyeballing the full downscaled image hides both under-sizing and clipping. (This is the `image-asset-audit` / measure-don't-estimate discipline applied to type.)

## Why matplotlib hits a ceiling (so you don't relearn it)

- Fonts are hardcoded points; making text legible after layout causes overlaps. Default DejaVu Sans reads "scientific," not "designed."
- No real grid/whitespace/alignment system; markers and spacing look generic.
- Brute-force fixes (post-render text scaling, `font_scale` multipliers) produce overlaps + oversized icons — exactly the "amateurish" look. The fix is the right tool, not a bigger hammer.

## Architecture (proven pattern from a client-deck build)

1. **One shared design-system module** = single source of truth. Holds: the CSS chrome (brand font stack, color tokens, typographic hierarchy, header/eyebrow/title/subtitle, legend, footer, aggregate-block, axis), reusable helpers (palettes, lookups), a `doc(eyebrow,title,tagline,subtitle,body,legend,footer,extra_css)` page scaffold, and a `render_png(html, path)` Chrome renderer. A fix here propagates to **every** chart.
2. **One generator per chart archetype** (stacked-bar, dot-plot, dumbbell, heatmap-table, bubble/SVG, scatter/SVG, …). Each computes data, emits body markup using the shared CSS classes, passes archetype-specific CSS via `extra_css=`, and returns `doc(...)`. Siblings (same archetype, different data) reuse one generator.
3. **Render → PNG → PDF.** Render each chart to a crisp full-page PNG (`device_scale_factor=2`), then assemble PNGs into the PDF (PIL `save_all`) — one chart per page, each page sized to its chart. Avoids print-CSS multi-page-sizing pain entirely.

Many charts are *easier* and cleaner in HTML/CSS than matplotlib: stacked/butterfly bars = flexbox divs; heatmaps = `<table>` with colored cells; dot plots/dumbbells = absolutely-positioned spans; bubble/scatter = inline `<svg>`.

## Lock the template before scaling

Build + iterate **1–2 exemplar charts to pixel-lock with the principal first** (the hardest/most-common archetypes), then propagate. The principal's design taste won't be captured first-try — expect several rounds on the exemplar (bar height, color, axis labels, legend placement, margins). Only after lock do you build the rest. This is the style-oracle discipline: get the canonical page right, then propagate.

## Parallelizing the build (workflow)

Once the shared system + exemplars are locked, the remaining charts parallelize cleanly: **one agent per archetype**, each importing the shared module and following the locked exemplars. Consistency is guaranteed *by construction* because all chrome/typography comes from the shared module — agents only emit body markup + archetype CSS. (One build used 7 agents to build 22 charts on a shared HTML design system, all consistent.) Use a **flat output schema** (see gotchas). Then do a human consistency pass — parallel-agent output is consistent in sample but verify at full scope (label collisions, drift).

## Gotchas (hard-won)

- **Self-host the font (or assert it loaded).** Pulling a web font from Google Fonts at render time means an offline/outage silently falls back to Arial — and a batch render→PDF has no error, so you ship a full off-brand deck. Self-host the woff2, or `await page.evaluate(() => document.fonts.ready)` + assert the brand font actually loaded before screenshot.
- **Match the reference where you diverge; don't impose your own "improvements."** When replicating a known design, the principal usually wants the reference's choices, not your variations. Surface deliberate divergences as explicit gates, not silent defaults. (Watch the "consistency quietly overriding fidelity" trap — when the goal is "faithful," fidelity/consistency conflicts are the principal's call.)
- **Legibility is the point, not faithful smallness.** Replicating a reference does NOT mean replicating its tiny text. Big, legible labels + minimal inter-row margin (bars/dots nearly fill rows, just enough white gap) is the professional look. "Faithful-to-the-style" ≠ "faithful-to-the-smallness."
- **PDF→image:** `Read` needs poppler/`pdftoppm` (often absent on Windows). Use PyMuPDF (`fitz`) to rasterize reference PDFs → PNG so you (and agents) can see them.
- **Reference implementation pattern:** a `pace_html.py`-style design system module + `scripts/*_charts/*.py` archetypes + an `assemble_deck.py` assembly script. Tooling: `playwright` (Chromium) is installed; `weasyprint`/`wkhtmltopdf` are not.

## Tooling

- `playwright` (sync API) drives headless Chromium for HTML→PNG. Chrome is also at the default Windows path for `--headless --print-to-pdf` if needed.
- Assembly: PIL `Image.save(pdf, save_all=True, append_images=[...])`.
