# Pipeline Diagnostic

When debugging a data pipeline failure, walk stages in order. Stop at the FIRST stage that shows incorrect data. That's your investigation target.

## Generic Pipeline Stages

| # | Stage | What to check | How to check |
|---|-------|--------------|-------------|
| 1 | **SOURCE** | Is the raw data correct? | Read API response, CSV, or raw query. Compare to known-good values. |
| 2 | **INGEST** | Did all records load? | Row counts, null rates, schema validation. |
| 3 | **TRANSFORM** | Are calculations correct? | Spot-check 3 rows manually. Compare intermediate results to hand-calculated values. |
| 4 | **ENRICH** | Did lookups/joins succeed? | Check join rates, missing keys, null enrichment columns. |
| 5 | **AGGREGATE** | Are rollups correct? | Compare sum-of-parts to total. Check group-by dimensions. |
| 6 | **OUTPUT** | Does the final artifact match expectations? | Visual inspection, shape check, sample comparison. |

## Project-Specific Pipelines

Add your own project pipeline maps here as you document them. Example format:

### My Data Project
```
raw_api_data → cleaned_csv → enriched_with_lookups → aggregated_metrics → dashboard_input
```

The more specific you make this for your projects, the faster debugging goes.

## Diagnostic Questions

At each stage, answer:
1. **Input OK?** — Does this stage receive correct data from the previous stage?
2. **Logic OK?** — Does this stage's transformation produce correct output from correct input?
3. **Output OK?** — Does this stage's output match expectations?

If Input is OK but Output is wrong → the bug is in this stage's logic.
If Input is already wrong → move up one stage and repeat.
