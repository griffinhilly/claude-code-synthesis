"""Centralized path definitions.

All file paths in one place. Import these everywhere instead of constructing
paths inline — it makes refactoring painless and prevents path mismatches.

Customize: Replace these with your actual file names and directory structure.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# --- Raw data ---
RAW_CSV = PROJECT_ROOT / "records.csv"
DATA_DIR = PROJECT_ROOT / "data"

# --- Enriched outputs ---
ENRICHED_CSV = PROJECT_ROOT / "records_enriched.csv"
CATEGORIZED_CSV = PROJECT_ROOT / "records_categorized.csv"
CATEGORIES_JSON = PROJECT_ROOT / "categories.json"

# --- Media (if your records have associated images/files) ---
MEDIA_DIR = PROJECT_ROOT / "media"

# --- Search index ---
SEARCH_INDEX = PROJECT_ROOT / "search_index.npz"
SEARCH_METADATA = PROJECT_ROOT / "search_metadata.json"

# --- Agent batch outputs ---
BATCH_DIR = PROJECT_ROOT / "category_batches"
