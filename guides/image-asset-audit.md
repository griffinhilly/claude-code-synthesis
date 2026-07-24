# Image Asset & Layout Audit — Measure Before You Size

When wiring image/icon assets into a chart or layout, or sizing text to fit a
space, **inspect and measure the real artifact**. Do not treat assets as opaque,
and do not estimate dimensions by eye.

## Why this exists

A client report's engineering-readiness icon table saw ~15 rounds of
"make the icons bigger" feedback that chased the wrong fix (scaling display boxes)
because the source icon PNGs had wildly inconsistent baked-in transparent
padding — content fill ranged from ~58% to ~100% of canvas depending on the icon. At equal
display-box size they rendered at very different visual sizes. A 5-minute
`PIL.getbbox()` audit when the icons were first wired up would have caught it.
Separately, hand-estimating text widths (e.g. "TRANSMISSION ≈ X px") produced
over-conservative, repeatedly-wrong header sizing until measurement scripts
replaced the estimates.

## Rule 1 — Audit image assets before relying on them

For each asset in a set, measure up front:
- **Content bounding box vs canvas** — `PIL.Image.open(p).convert("RGBA").getbbox()`.
  Reveals baked-in transparent padding.
- **Fill ratio** (content w/h ÷ canvas w/h) and **aspect ratio**.
- Flag any asset whose fill ratio or aspect diverges from the set — it will
  render visually larger/smaller than its peers at an equal display box.

If the set is inconsistent, normalize *systematically* — trim each asset to its
content bbox, then size to a uniform metric (e.g. uniform height) — rather than
hand-tuning each one. A clean reference pattern: a `load_icon()` helper that trims,
paired with an `_icon_dims()` helper that height-normalizes, plus a small
documented per-icon scale table for residual visual-weight correction.

## Rule 2 — Measure layout, don't estimate it

Text fit, column widths, overlap clearance are **deterministic** — compute them:
- Browser-rendered layout: Playwright + `Element.getBoundingClientRect()` or
  `Range.getBoundingClientRect()` on the rendered HTML.
- Font metrics without a browser: `PIL.ImageFont.truetype(path, size).getbbox(text)`.
  Calibrate once against a known browser measurement — PIL runs a few percent
  wide vs Chromium.
- Then **maximize against the measured limit.** Don't undersize with a guessed
  "fear margin" — that produces work the user has to push back on round after round.

This is the latent-vs-deterministic doctrine (CLAUDE.md) applied to
layout: sizing geometry is deterministic; don't do it in latent space.

## Tell

If you are about to write a px value for an icon size, font size, or column
width based on a mental estimate — stop and measure instead.
