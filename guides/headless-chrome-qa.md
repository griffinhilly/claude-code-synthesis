# Headless-Chrome QA — verify web UI without the browser extension

Promoted after a second sighting across two separate UI-heavy projects. Rule of the house: for UI work,
verify through the layer the concern lives in — a clean build or unit sim is
NOT sufficient for interaction/layout claims.

## Decision table

| Need | Technique |
|---|---|
| Static render / above-the-fold look | `chrome --headless=new --screenshot=<png> --window-size=WxH --virtual-time-budget=5000 <url>` |
| Click/hover through the REAL event path | CDP driver (below) with `Input.dispatchMouseEvent`, or the temp-copy trick: append a script dispatching real DOM clicks + `window.onerror` banner, then `--virtual-time-budget` screenshot |
| Mobile layout / overflow claims | CDP driver with `Emulation.setDeviceMetricsOverride(mobile:true)` — **never** trust `--window-size=390` alone: desktop headless clamps to a minimum layout width and produces a fake uniform right-clip on every page (one project's dashboard QA hit this; real emulation showed zero overflow) |
| Layout measurements (scrollWidth, element rects, console errors) | CDP driver `Runtime.evaluate` |

## Reference implementation

A zero-dep Node (≥21) CDP driver script (e.g. `scripts/cdp-qa.mjs`): mobile emulation, full-page screenshots, scripted
click/hover/scroll actions, horizontal-overflow DIAG line, arbitrary eval.
Usage in its header. Start Chrome first:

```
chrome --headless=new --remote-debugging-port=9222 --user-data-dir=<throwaway> about:blank
```

Copy it into new projects rather than reinventing; it has no dependencies.

## Gotchas

- Screenshots can't capture native `<title>` tooltips — verify their text via
  `Runtime.evaluate` on the DOM instead.
- Chrome's `/json/new` endpoint needs `PUT` (not GET) on current releases.
- Don't restart the user's running Chrome to get the extension back — a
  separate headless instance never disturbs their session.
- Static-export Next sites: preview with `npx serve out` (clean-URL rewrite),
  not `python -m http.server`.
- `--screenshot` ignores a `#fragment` in the URL (it captures the top of the
  page). To capture a deeper section, screenshot a copy of the file with the
  sections above it hidden by CSS, or take a taller `--window-size`.
- Under `--dump-dom`, a test hook wrapped in `window.addEventListener('load', …)`
  may never fire; run the hook synchronously in a `<script>` appended before
  `</body>` and write results into a `<pre id="testout">`.
