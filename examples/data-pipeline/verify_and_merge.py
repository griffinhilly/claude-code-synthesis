"""
Verify LLM-generated categories and merge into final CSV.

Usage:
    python verify_and_merge.py          # verify + merge

What it does:
    1. Load categories from JSON (output of LLM batch agents)
    2. Check coverage — which records are missing categories?
    3. Auto-fix invalid tags using the fix mappings in taxonomy.py
    4. Enforce constraints (1-3 topics, exactly 1 content type)
    5. Print distribution summary for spot-checking
    6. Merge validated categories into the final CSV
"""
import json
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared.taxonomy import VALID_TOPICS, VALID_CONTENT_TYPES, TOPIC_FIXES, CONTENT_TYPE_FIXES
from shared.paths import ENRICHED_CSV, CATEGORIZED_CSV, CATEGORIES_JSON
from shared.csv_merge import merge_json_into_csv


def verify_categories(categories_json, reference_csv, skip_condition=None):
    """Verify and fix categories in-place. Returns (categories, missing_ids)."""
    with open(categories_json, encoding="utf-8") as f:
        categories = json.load(f)
    print(f"Loaded {len(categories)} categorizations from {Path(categories_json).name}")

    with open(reference_csv, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if skip_condition:
        target_ids = {r["item_id"] for r in rows if not skip_condition(r)}
        total_label = "eligible records"
    else:
        target_ids = {r["item_id"] for r in rows}
        total_label = "records"
    print(f"Target {total_label}: {len(target_ids)}")

    # Coverage
    categorized = set(categories.keys()) & target_ids
    missing = target_ids - set(categories.keys())
    print(f"Coverage: {len(categorized)}/{len(target_ids)} "
          f"({100 * len(categorized) / len(target_ids):.1f}%)")
    if missing:
        print(f"  Missing: {len(missing)}")

    # Fix invalid tags
    valid_topics_set = set(VALID_TOPICS)
    valid_ct_set = set(VALID_CONTENT_TYPES)
    fixes = 0

    for entry in categories.values():
        # Fix topics
        fixed_topics = []
        for t in entry.get("topics", []):
            if t in valid_topics_set:
                fixed_topics.append(t)
            elif t in TOPIC_FIXES:
                replacement = TOPIC_FIXES[t]
                if replacement and replacement not in fixed_topics:
                    fixed_topics.append(replacement)
                fixes += 1
            else:
                fixes += 1

        if not fixed_topics:
            fixed_topics = [VALID_TOPICS[0]]  # fallback to first topic
            fixes += 1
        if len(fixed_topics) > 3:
            fixed_topics = fixed_topics[:3]
            fixes += 1
        entry["topics"] = fixed_topics

        # Fix content type
        ct = entry.get("content_type", "")
        if ct not in valid_ct_set:
            entry["content_type"] = CONTENT_TYPE_FIXES.get(ct, "observation_insight")
            fixes += 1

        # Ensure claims structure
        if not isinstance(entry.get("extracted_claims"), list):
            entry["extracted_claims"] = []
        if entry.get("claim_confidence") not in ("high", "medium", "low", "none"):
            entry["claim_confidence"] = "none" if not entry["extracted_claims"] else "medium"

    if fixes:
        print(f"Applied {fixes} fixes")

    # Distribution summary
    topic_counts = {}
    ct_counts = {}
    claim_count = 0
    for entry in categories.values():
        for t in entry["topics"]:
            topic_counts[t] = topic_counts.get(t, 0) + 1
        ct_counts[entry["content_type"]] = ct_counts.get(entry["content_type"], 0) + 1
        if entry.get("extracted_claims"):
            claim_count += 1

    print(f"\nTop topics: {', '.join(f'{t}:{c}' for t, c in sorted(topic_counts.items(), key=lambda x: -x[1])[:5])}...")
    print(f"Types: {', '.join(f'{t}:{c}' for t, c in sorted(ct_counts.items(), key=lambda x: -x[1]))}")
    print(f"Records with claims: {claim_count}")

    # Save fixed categories
    with open(categories_json, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)

    return categories, missing


def merge_categories(categories, input_csv, output_csv, skip_condition=None):
    """Merge verified categories into CSV."""
    total, matched, skipped = merge_json_into_csv(
        categories, str(input_csv), str(output_csv), skip_condition=skip_condition
    )
    print(f"\nMerged: {matched}/{total} matched"
          + (f", {skipped} skipped" if skipped else ""))
    print(f"Output: {Path(output_csv).name} ({total} rows)")


def run_verify_merge():
    """Main entry point — verify and merge categories."""
    print("=== VERIFY & MERGE ===")
    cats, missing = verify_categories(str(CATEGORIES_JSON), str(ENRICHED_CSV))
    merge_categories(cats, ENRICHED_CSV, CATEGORIZED_CSV)
    return missing


if __name__ == "__main__":
    run_verify_merge()
