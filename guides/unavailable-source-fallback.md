# Unavailable-Source Fallback (Wayback / archive)

When a public data or document host is down, 403s, or IP-throttles, the **Wayback Machine snapshot of the same URL** is a viable rebuild source. Promoted to a guide after two independent sightings:
- **A financial-data project:** a macro-data API was unreachable all session; two time-series indicators were rebuilt from Wayback CSV snapshots.
- **A research-writing project:** a policy-report chapter (a key fiscal-multiplier source) was fetched from Wayback after the direct publisher URL 403'd.

## Procedure

1. Try the live URL first. On error (403/404/504/throttle), query the Wayback Machine for snapshots of that exact URL (`http://web.archive.org/web/*/<url>` or the availability API).
2. Pull the closest-dated snapshot to the vintage you need.
3. **Validation is mandatory — the fallback is not trusted until checked:**
   - **Time-series / tabular data:** if splicing an archived history with a recent partial pull, confirm the overlap seam agrees (byte- or value-identical on shared dates) AND spot-check ≥2 known historical values.
   - **A document (PDF, report):** confirm the archived copy matches the original where it's load-bearing (e.g., the specific figure/number you're quoting); record that the source is an archive copy, not the publisher's live file.
4. Record provenance: the archive URL, snapshot date, and the validation result. Never present an archived figure as if pulled from the live primary source.

## When this applies

Any project rebuilding an unavailable series or document from an archive/secondary source — economic-data, gated PDFs, dead blog data. If a host is merely slow, retry; if it's down or blocking, go to Wayback rather than fabricating or skipping.
