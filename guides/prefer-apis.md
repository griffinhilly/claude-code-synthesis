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
2. Check if there's a Python package wrapping the API (e.g., `nba_api`, `tweepy`, `stripe`)
3. Check if the data is available as a static file (CSV, JSON, RSS)
4. Only use Playwright/Selenium as a **last resort** after confirming no API exists
