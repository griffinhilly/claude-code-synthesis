# How to Build a Searchable Twitter/X Bookmark Archive

This guide walks you through turning your Twitter/X bookmarks into a searchable, categorized personal knowledge base. This is the exact workflow used to build the data pipeline example in this repo — and to trace all the attributions in the README.

## Why Bother?

Your bookmarks are a curated signal of what you found valuable. But Twitter's built-in bookmark search is terrible — no full-text search, no filtering by topic, no semantic matching. After a few hundred bookmarks, you can't find anything.

This pipeline gives you:
- **Semantic search** — find bookmarks by meaning, not just keywords
- **Topic categorization** — every bookmark tagged with 1-3 topics from your custom taxonomy
- **Content type classification** — factual claims, advice, opinions, humor, etc.
- **Claim extraction** — specific claims pulled out and searchable
- **Image descriptions** — AI-generated descriptions of images in your bookmarks (searchable too)
- **Full offline archive** — everything stored locally, no API dependency after capture

## Step 0: Capture Your Bookmarks as HAR Files

Twitter doesn't offer a bookmark export API. The workaround: capture the network traffic as you scroll through your bookmarks.

1. Open Twitter/X in Chrome and go to your Bookmarks page
2. Open DevTools (F12) → Network tab
3. Check "Preserve log"
4. Scroll through ALL your bookmarks (the page lazy-loads as you scroll)
5. In the Network tab, right-click → "Save all as HAR with content"
6. Save as `data/Bookmarks_1.har`

**Tips:**
- Scroll slowly and wait for content to load. If you scroll too fast, some bookmarks won't be captured.
- For large collections (1000+), do it in chunks across multiple sessions. Save each as `Bookmarks_2.har`, `Bookmarks_3.har`, etc. The extraction script deduplicates by tweet ID.
- HAR files contain your auth cookies — treat them as sensitive. Don't commit them to git (already in `.gitignore`).

## Step 1: Extract Tweets from HAR Files

The HAR file contains raw Twitter API responses. You need a script to parse these and extract structured tweet data.

What to extract per tweet:
- `tweet_id`, `screen_name`, `display_name`
- `full_text` (the tweet body)
- `created_at`, `view_count`, `favorite_count`, `retweet_count`
- `media_urls` (image/video URLs)
- `quoted_text`, `quoted_user` (if it's a quote tweet)
- `in_reply_to_screen_name` (if it's a reply)
- `tweet_url`

The Twitter API responses are deeply nested JSON. The key path is roughly:
```
entry → content → itemContent → tweet_results → result → legacy
```

Output: `records.csv` with one row per bookmark.

## Step 2: Download Media

Loop through `media_urls` in your CSV and download images to `media/`. Name them `{tweet_id}_{index}.jpg` for easy cross-referencing.

**Important:** Twitter CDN requires a `User-Agent` header or returns 403.

## Step 3: AI Image Descriptions (Optional but Powerful)

Many bookmarked tweets have images with text, charts, or diagrams that aren't in the tweet text. Use Claude (Haiku is fast and cheap) to generate:
- A text description of the image
- OCR text extraction

This makes image content searchable — a huge unlock for bookmarks where the value is in an attached screenshot or infographic.

Batch 20 images per agent call for efficiency. See `examples/data-pipeline/guides/agent-orchestration.md` for the pattern.

## Step 4: LLM Categorization

Use the taxonomy + batch agent pattern from `shared/taxonomy.py` to categorize every bookmark. For a personal bookmark archive, a taxonomy like this works well:

```python
VALID_TOPICS = [
    "ai_technology", "economics_finance", "politics_governance",
    "philosophy_ethics", "psychology_cognition", "parenting_education",
    "health_medicine", "science_research", "culture_society",
    "media_journalism", "history", "career_productivity",
    "humor_shitposting", "personal_reflection"
]
```

Customize to match your interests. The whole point is that YOUR bookmarks reflect YOUR interests, so the taxonomy should too.

## Step 5: Verify, Merge, and Build Search Index

1. Run `verify_and_merge.py` to validate LLM output and merge categories into your CSV
2. Run `search.py --rebuild` to build the semantic search index
3. Search: `python search.py "your query" --top-k 10`

## Step 6: Ongoing Maintenance

When you accumulate more bookmarks:
1. Capture a new HAR file → `data/Bookmarks_N.har`
2. Run `python pipeline.py` — it auto-detects new HAR files
3. Pipeline pauses if new bookmarks need categorization
4. Run batch agents, then `python pipeline.py --skip-enrich --skip-categories`

## What You End Up With

After processing ~2,000 bookmarks:
- ~1,100 downloaded images with AI descriptions
- Every bookmark tagged with 1-3 topics + content type
- ~1,600 extracted claims from factual/advice tweets
- A semantic search index that finds bookmarks by meaning
- Total pipeline cost: ~$1-3 in Claude API credits (mostly Haiku for categorization + image descriptions)

The search is the real payoff. Instead of "I know I bookmarked something about X..." followed by 20 minutes of scrolling, you get instant semantic results with topic filters.

## Privacy Note

HAR files contain your Twitter session cookies and auth tokens. The `.gitignore` excludes them, but be aware:
- Don't share HAR files
- Don't commit them to public repos
- Session tokens in HAR files expire, so old files can't be used to impersonate you, but treat them as sensitive during their lifetime
