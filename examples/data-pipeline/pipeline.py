"""
Data enrichment pipeline — step-based orchestrator.

Usage:
    python pipeline.py                   # run full pipeline
    python pipeline.py --skip-enrich     # skip enrichment step
    python pipeline.py --skip-categories # skip categorization check
    python pipeline.py --dry-run         # show what would happen without doing it

Steps:
    1. Extract raw records into CSV
    2. Download associated media (if applicable)
    3. Enrich records (merge additional metadata)
    4. Identify uncategorized records (for LLM agent categorization)
    5. Verify + merge categories into final CSV
    6. Rebuild search index

The pipeline pauses at step 4 if records need categorization — this is the
"human gate" where you run batch Claude Code agents to categorize, then resume.
"""
import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared.paths import (
    PROJECT_ROOT, RAW_CSV, ENRICHED_CSV, CATEGORIZED_CSV,
    CATEGORIES_JSON, DATA_DIR,
)


def run_step(name, func, dry_run=False):
    """Run a pipeline step with status output."""
    print(f"\n{'='*60}")
    print(f"STEP: {name}")
    print(f"{'='*60}")
    if dry_run:
        print("  [DRY RUN — skipped]")
        return None
    return func()


# ---------------------------------------------------------------------------
# Pipeline steps — customize these for your domain
# ---------------------------------------------------------------------------

def step_extract():
    """Step 1: Extract raw records into CSV.

    Customize: Replace this with your data extraction logic.
    Examples:
      - Parse HAR files captured from a web app
      - Read a JSON export from an API
      - Process downloaded HTML pages
      - Import from a database dump
    """
    # EXAMPLE: scan data/ for JSON files and extract records
    json_files = sorted(DATA_DIR.glob("*.json"))
    if not json_files:
        print("  No data files found in data/")
        print("  Place your raw data files in the data/ directory")
        return 0

    all_records = {}
    for jf in json_files:
        count_before = len(all_records)
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)

        # --- YOUR EXTRACTION LOGIC HERE ---
        # Parse 'data' and populate all_records[record_id] = {...}
        # Example:
        #   for item in data.get("items", []):
        #       rid = item["id"]
        #       if rid not in all_records:
        #           all_records[rid] = {
        #               "item_id": rid,
        #               "title": item["title"],
        #               "text": item["text"],
        #               "author": item.get("author", ""),
        #               "created_at": item.get("date", ""),
        #           }

        new = len(all_records) - count_before
        print(f"  {jf.name}: +{new} new records")

    # Sort and write CSV
    sorted_records = sorted(all_records.values(), key=lambda r: r.get("created_at", ""), reverse=True)
    if sorted_records:
        fieldnames = list(sorted_records[0].keys())
        with open(RAW_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_records)

    print(f"\nExtracted {len(sorted_records)} records to {RAW_CSV.name}")
    return len(sorted_records)


def step_download_media():
    """Step 2: Download associated media.

    Customize: If your records reference images, PDFs, or other files,
    download them here. If not applicable, remove this step.
    """
    # EXAMPLE: run a separate download script
    # result = subprocess.run(
    #     [sys.executable, str(PROJECT_ROOT / "download_media.py")],
    #     capture_output=True, text=True, cwd=str(PROJECT_ROOT)
    # )
    # print(result.stdout)
    print("  [No media download configured — customize step_download_media()]")


def step_enrich():
    """Step 3: Enrich records with additional metadata.

    Customize: Merge in image descriptions, related records, external
    API data, or any other enrichment. This produces the enriched CSV
    that categorization will run against.
    """
    # EXAMPLE: copy raw CSV as enriched (no enrichment yet)
    if not RAW_CSV.exists():
        print("  ERROR: Raw CSV not found. Run extraction first.")
        return

    with open(RAW_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # --- YOUR ENRICHMENT LOGIC HERE ---
    # Example: merge in image descriptions, external metadata, etc.
    # enrichment_data = json.load(open("image_descriptions.json"))
    # for row in rows:
    #     rid = row["item_id"]
    #     if rid in enrichment_data:
    #         row["description"] = enrichment_data[rid]["description"]

    with open(ENRICHED_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Assembled {len(rows)} enriched records")


def step_find_uncategorized():
    """Step 4: Identify records needing LLM categorization.

    This is the "human gate" — if records need categorization, the pipeline
    pauses here. You then run batch Claude Code agents to categorize them,
    and resume the pipeline afterward.
    """
    if not CATEGORIES_JSON.exists():
        # First run — no categories yet
        existing = {}
    else:
        with open(CATEGORIES_JSON, encoding="utf-8") as f:
            existing = json.load(f)

    with open(ENRICHED_CSV, encoding="utf-8-sig") as f:
        all_ids = [row["item_id"] for row in csv.DictReader(f)]

    uncategorized = [rid for rid in all_ids if rid not in existing]
    print(f"Existing categories: {len(existing)}")
    print(f"Total records: {len(all_ids)}")
    print(f"Needing categorization: {len(uncategorized)}")

    if uncategorized:
        print(f"\n*** {len(uncategorized)} records need categorization ***")
        print("Run Claude Code agents to categorize these records, then resume:")
        print(f"  python verify_and_merge.py")
    else:
        print("\nAll records categorized!")

    return uncategorized


def step_verify_merge():
    """Step 5: Verify categories and merge into final CSV."""
    from verify_and_merge import run_verify_merge
    run_verify_merge()


def step_rebuild_search():
    """Step 6: Rebuild search index."""
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "search.py"), "test", "--rebuild", "--top-k", "1"],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    if "Saved" in result.stdout or "search_index" in result.stdout:
        print("Search index rebuilt successfully")
    else:
        print(result.stdout[-500:] if result.stdout else "")
        if result.returncode != 0:
            print(f"WARNING: {result.stderr[-500:]}")


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Data enrichment pipeline")
    parser.add_argument("--skip-enrich", action="store_true",
                        help="Skip enrichment step")
    parser.add_argument("--skip-categories", action="store_true",
                        help="Skip categorization check")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show plan without executing")
    args = parser.parse_args()

    print("DATA ENRICHMENT PIPELINE")
    print(f"Project: {PROJECT_ROOT}")

    # Step 1: Extract
    run_step("Extract raw records", step_extract, args.dry_run)

    # Step 2: Download media
    run_step("Download media", step_download_media, args.dry_run)

    # Step 3: Enrich
    if not args.skip_enrich:
        run_step("Enrich records", step_enrich, args.dry_run)
    else:
        print("\n[Skipping enrichment]")

    # Step 4: Check categorization coverage
    if not args.skip_categories:
        uncategorized = run_step("Check categorization coverage",
                                 step_find_uncategorized, args.dry_run)
        if uncategorized and not args.dry_run:
            print(f"\n*** PAUSING: {len(uncategorized)} records need agent categorization ***")
            print("After categorizing, run: python verify_and_merge.py")
            print("Then run: python pipeline.py --skip-enrich --skip-categories")
            return

    # Step 5: Verify + merge
    run_step("Verify and merge categories", step_verify_merge, args.dry_run)

    # Step 6: Rebuild search index
    run_step("Rebuild search index", step_rebuild_search, args.dry_run)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
