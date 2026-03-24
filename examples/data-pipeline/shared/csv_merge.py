"""Generic utilities for merging JSON data into CSV files.

The core pattern: your LLM agents output JSON (keyed by record ID), and your
master dataset lives in a CSV. This module bridges the two — merging new columns
from JSON into CSV without losing existing data.

Handles:
  - Custom ID fields and column definitions
  - Field mapping functions (transform JSON structure → flat CSV columns)
  - Skip conditions (e.g., skip duplicates, skip archived records)
  - Encoding quirks (BOM characters from Excel, etc.)
"""
import csv
import json


def merge_json_into_csv(json_data, input_csv, output_csv, id_field="item_id",
                        new_columns=None, field_mapper=None, skip_condition=None,
                        input_encoding="utf-8-sig", output_encoding="utf-8-sig"):
    """
    Merge a JSON dict (keyed by ID) into a CSV, adding new columns.

    Args:
        json_data: dict keyed by ID with metadata dicts as values
        input_csv: path to input CSV
        output_csv: path to output CSV
        id_field: CSV column to match against JSON keys
        new_columns: list of column names to add (default: category columns)
        field_mapper: function(json_entry) -> dict of {col_name: value}
        skip_condition: function(row) -> bool, if True row gets empty values
        input_encoding: encoding for reading input CSV
        output_encoding: encoding for writing output CSV

    Returns:
        (total_rows, matched_rows, skipped_rows)
    """
    if new_columns is None:
        new_columns = ["topics", "content_type", "extracted_claims", "claim_confidence"]

    if field_mapper is None:
        def field_mapper(entry):
            return {
                "topics": ";".join(entry.get("topics", [])),
                "content_type": entry.get("content_type", ""),
                "extracted_claims": json.dumps(entry.get("extracted_claims", []), ensure_ascii=False),
                "claim_confidence": entry.get("claim_confidence", "none"),
            }

    empty_values = {col: "" for col in new_columns}
    if "extracted_claims" in new_columns:
        empty_values["extracted_claims"] = "[]"
    if "claim_confidence" in new_columns:
        empty_values["claim_confidence"] = "none"

    with open(input_csv, encoding=input_encoding) as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames) + new_columns
        rows = list(reader)

    matched = 0
    skipped = 0
    for row in rows:
        rid = row[id_field]
        if skip_condition and skip_condition(row):
            row.update(empty_values)
            skipped += 1
        elif rid in json_data:
            row.update(field_mapper(json_data[rid]))
            matched += 1
        else:
            row.update(empty_values)

    with open(output_csv, "w", encoding=output_encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), matched, skipped
