# Prefer APIs Over Browser Automation

When a task involves fetching data from a website, **always prefer direct API calls** over browser automation (Playwright, Selenium, Puppeteer).

## Why

Browser automation is fragile:
- Bot detection blocks automated browsers frequently
- Browser version mismatches cause silent failures
- Chrome profile locks prevent concurrent sessions
- Sessions are slow and resource-heavy compared to HTTP requests

## Checklist

1. Check if the site has a public API or data export
2. Check if there's a Python package wrapping the API (e.g., `tweepy`, `stripe`, `praw`)
3. Check if the data is available as a static file (CSV, JSON, RSS)
4. Only use Playwright/Selenium as a **last resort** after confirming no API exists

## Blocked or JavaScript-rendered pages: the data is usually already in the source

Promoted on the second sighting. Before reaching for a browser extension or Playwright, do these in order:

1. **Retry with a browser User-Agent.** Many hosts that return 403 or an empty shell to a default fetcher (applicant-tracking job boards like Ashby and Lever, many government and nonprofit sites) return full content to `curl -A "Mozilla/5.0 ... Chrome/128.0 Safari/537.36"` or `urllib` with the same header. Test this before assuming the host is down. Respect the site's terms and robots.txt.
2. **Look for a JSON endpoint behind the page.** Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>?questions=true` returns the posting plus the application form fields. WordPress: `/wp-json/wp/v2/...`.
3. **Grep the raw HTML for embedded bootstrap JSON.** Ashby pages carry the posting in a `"descriptionHtml":"..."` JSON string; JS apps carry their data in `<script>` blocks; some pages embed a whole entity-encoded HTML document in an attribute (decode with `html.unescape` twice, then parse). Wayback: `web.archive.org/web/<ts>id_/<url>` gives the unmodified original.
4. Only then drive a browser, and only for genuinely interactive state. A browser extension may be disconnected; always have a no-browser fallback.

Sightings: a 1,976-node knowledge map recovered from JSON embedded in an archived page after the browser extension was disconnected; a dozen pages plus a 500 KB embedded database recovered with curl, a browser User-Agent and JSON parsing after the default fetcher got 403s.
