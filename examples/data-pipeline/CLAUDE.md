# Data Pipeline — Claude Code Instructions

## Overview
Data enrichment pipeline: extract → enrich → categorize → merge → search.

## Pipeline
To run the full pipeline: `python pipeline.py`
To do a dry run: `python pipeline.py --dry-run`
To verify + merge after categorization: `python verify_and_merge.py`

Key scripts:
- `pipeline.py` — Full pipeline runner (extract → enrich → categorize → merge → search)
- `verify_and_merge.py` — Verify LLM categories + rebuild final CSV
- `search.py` — Semantic search CLI

## Architecture
- `shared/taxonomy.py` — Canonical category definitions + LLM prompt
- `shared/paths.py` — All file paths
- `shared/csv_merge.py` — Generic JSON→CSV merge utilities

## Taxonomy
Defined in `shared/taxonomy.py`. Update the valid tags, fix mappings, and prompt template there.

## Situational Guides
- When modifying or debugging a pipeline step → read `guides/pipeline-steps.md`
- When running batch LLM agents → read `guides/agent-orchestration.md`
