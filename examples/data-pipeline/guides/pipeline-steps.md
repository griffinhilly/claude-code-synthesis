# Pipeline Steps Reference

## Pipeline Overview

```
Raw Data → Extract → Download Media → Enrich → Categorize → Verify+Merge → Search
                                                    ↑
                                              human gate
                                        (batch LLM agents)
```

## Step Details

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 1. Extract | `pipeline.py` (step_extract) | `data/*.json` | `records.csv` |
| 2. Media | `pipeline.py` (step_download_media) | URLs in CSV | `media/` |
| 3. Enrich | `pipeline.py` (step_enrich) | `records.csv` + metadata | `records_enriched.csv` |
| 4. Categorize | Claude Code agents | `records_enriched.csv` | `categories.json` |
| 5. Verify+Merge | `verify_and_merge.py` | `categories.json` + `records_enriched.csv` | `records_categorized.csv` |
| 6. Search | `search.py --rebuild` | `records_categorized.csv` | `search_index.npz` + `search_metadata.json` |

## The Human Gate (Step 4)

Step 4 is where the pipeline pauses for human intervention. The pipeline detects uncategorized records and tells you how many need processing. You then:

1. Prepare batches of records (typically 20-25 per batch)
2. Run Claude Code agents (Haiku recommended) with the prompt from `shared/taxonomy.py`
3. Collect JSON output into `categories.json`
4. Resume: `python verify_and_merge.py` then `python pipeline.py --skip-enrich --skip-categories`

See `agent-orchestration.md` for detailed agent batch patterns.

## Partial Re-runs

| Scenario | Command |
|----------|---------|
| Full pipeline | `python pipeline.py` |
| Skip enrichment (already done) | `python pipeline.py --skip-enrich` |
| Just verify + merge | `python verify_and_merge.py` |
| Just rebuild search | `python search.py --rebuild` |
| After categorization | `python pipeline.py --skip-enrich --skip-categories` |

## Adding a New Step

1. Write a `step_your_step()` function in `pipeline.py`
2. Add it to `main()` with `run_step("Your Step Name", step_your_step, args.dry_run)`
3. Optionally add a `--skip-your-step` flag
4. Update this guide
