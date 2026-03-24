# [Your Project Name] — Orientation

## What Is This?
<!-- One paragraph: what does this project do and why does it exist? -->
A data enrichment pipeline that takes raw data, enriches it with LLM-generated metadata (topic categories, content types, extracted claims), validates the LLM output, and provides semantic search over the results.

## How It Works
```
Raw Data (HAR/CSV/JSON/API)
    → pipeline.py (step-based orchestrator)
        → Step 1: Extract raw records into CSV
        → Step 2: Download associated media (if any)
        → Step 3: Enrich with additional metadata
        → Step 4: LLM categorization (batch agents) ← human gate
        → Step 5: Verify + merge categories
        → Step 6: Rebuild search index
    → search.py "your query" --top-k 10
```

## Common Operations

| Task | Command |
|------|---------|
| Full pipeline | `python pipeline.py` |
| Dry run | `python pipeline.py --dry-run` |
| Skip specific steps | `python pipeline.py --skip-enrich --skip-categories` |
| Verify + merge only | `python verify_and_merge.py` |
| Search | `python search.py "query" --top-k 10` |
| Rebuild search index | `python search.py --rebuild` |

## Key Files
- `shared/taxonomy.py` — **Start here.** Defines your categories and the LLM prompt.
- `shared/paths.py` — Where everything lives on disk.
- `pipeline.py` — The main orchestrator. Each step is a function you customize.

## Known Weirdness
<!-- Document encoding issues, API quirks, workarounds, etc. -->
- CSV files with BOM characters need `encoding='utf-8-sig'` when reading.
- LLMs will hallucinate category names not in your taxonomy. The fix maps in `taxonomy.py` handle this automatically.
