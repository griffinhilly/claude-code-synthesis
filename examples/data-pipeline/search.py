"""
Semantic search over enriched records.

Embeds all records using sentence-transformers, caches the index to disk,
and returns cosine-similarity ranked results for natural language queries.

Usage:
    python search.py "your search query"
    python search.py "query" --topic electronics --top-k 5
    python search.py "query" --content-type factual_claim
    python search.py --rebuild

Model: all-MiniLM-L6-v2 (22M params, 384-dim, CPU-only)
  Paper: "Sentence-BERT" by Nils Reimers & Iryna Gurevych (2019)
  https://www.sbert.net/

Customize:
  - build_document(): define which fields get embedded
  - metadata construction: define which fields appear in search results
  - argparse filters: add domain-specific filters
"""
import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).parent

INPUT_CSV = str(_PROJECT_ROOT / "records_categorized.csv")
INDEX_FILE = str(_PROJECT_ROOT / "search_index.npz")
META_FILE = str(_PROJECT_ROOT / "search_metadata.json")

MODEL_NAME = "all-MiniLM-L6-v2"


def build_document(row):
    """Build a combined text document for a single record.

    Customize: Include all fields that should be semantically searchable.
    More text = richer embeddings, but keep it under ~512 tokens per record
    (the model's max sequence length).
    """
    parts = []

    # Primary text content
    if row.get("title"):
        parts.append(row["title"])
    if row.get("text"):
        parts.append(row["text"])

    # Additional context fields — add your own
    # if row.get("image_descriptions"):
    #     parts.append(f"[Image]: {row['image_descriptions']}")
    # if row.get("author"):
    #     parts.append(f"[Author]: {row['author']}")

    # Categories as readable text (helps with topic-based queries)
    topics = row.get("topics", "")
    if topics:
        readable = ", ".join(t.replace("_", " ") for t in topics.split(";"))
        parts.append(f"[Topics]: {readable}")

    # Extracted claims
    claims_json = row.get("extracted_claims", "[]")
    try:
        claims = json.loads(claims_json)
        if claims:
            parts.append(f"[Claims]: {'; '.join(claims)}")
    except (json.JSONDecodeError, TypeError):
        pass

    return "\n".join(parts)


def build_search_index():
    """Load CSV, embed all records, save index to disk."""
    from sentence_transformers import SentenceTransformer

    print(f"Loading model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Reading {INPUT_CSV}...")
    with open(INPUT_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"  {len(rows)} records loaded")

    documents = []
    metadata = []
    for row in rows:
        doc = build_document(row)
        documents.append(doc)

        # Customize: which fields to include in search result display
        metadata.append({
            "item_id": row.get("item_id", ""),
            "title": row.get("title", "")[:200],
            "text": row.get("text", "")[:300],
            "author": row.get("author", ""),
            "created_at": row.get("created_at", ""),
            "topics": row.get("topics", ""),
            "content_type": row.get("content_type", ""),
            "extracted_claims": row.get("extracted_claims", "[]"),
            "claim_confidence": row.get("claim_confidence", "none"),
        })

    print(f"Encoding {len(documents)} documents...")
    t0 = time.time()
    embeddings = model.encode(documents, show_progress_bar=True,
                              normalize_embeddings=True)
    elapsed = time.time() - t0
    print(f"  Encoded in {elapsed:.1f}s ({embeddings.shape})")

    np.savez_compressed(INDEX_FILE, embeddings=embeddings)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False)

    print(f"  Saved index to {INDEX_FILE} ({os.path.getsize(INDEX_FILE) / 1024:.0f} KB)")
    print(f"  Saved metadata to {META_FILE} ({os.path.getsize(META_FILE) / 1024:.0f} KB)")
    return embeddings, metadata


def load_index():
    """Load cached index from disk."""
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        return None, None
    data = np.load(INDEX_FILE)
    embeddings = data["embeddings"]
    with open(META_FILE, encoding="utf-8") as f:
        metadata = json.load(f)
    return embeddings, metadata


def search(query, embeddings, metadata, model, top_k=10,
           topic_filter=None, content_type_filter=None, author_filter=None):
    """Search records by semantic similarity with optional filters."""
    query_emb = model.encode([query], normalize_embeddings=True)

    # Cosine similarity (normalized embeddings → dot product = cosine)
    scores = (embeddings @ query_emb.T).flatten()

    # Apply filters — set score to -1 for filtered-out records
    for i, meta in enumerate(metadata):
        if topic_filter:
            record_topics = meta.get("topics", "").split(";")
            if topic_filter not in record_topics:
                scores[i] = -1
                continue
        if content_type_filter:
            if meta.get("content_type") != content_type_filter:
                scores[i] = -1
                continue
        if author_filter:
            if meta.get("author", "").lower() != author_filter.lower():
                scores[i] = -1
                continue

    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            break
        results.append((scores[idx], metadata[idx]))
    return results


def format_result(rank, score, meta):
    """Format a single search result for display."""
    date_str = meta.get("created_at", "")[:10] if meta.get("created_at") else "N/A"
    topics = meta.get("topics", "")
    topics_str = ", ".join(t.replace("_", " ") for t in topics.split(";")) if topics else "N/A"
    ct = meta.get("content_type", "").replace("_", " ") if meta.get("content_type") else "N/A"

    text = meta.get("text", "") or meta.get("title", "")
    if len(text) > 200:
        text = text[:200] + "..."

    claims_str = ""
    try:
        claims = json.loads(meta.get("extracted_claims", "[]"))
        if claims:
            claims_str = f"\n    Claims: {'; '.join(claims[:3])}"
            if len(claims) > 3:
                claims_str += f" (+{len(claims) - 3} more)"
    except (json.JSONDecodeError, TypeError):
        pass

    lines = [
        f"[{rank}] Score: {score:.3f} | {meta.get('author', 'unknown')} | {date_str}",
        f"    Topics: {topics_str} | Type: {ct}",
        f"    \"{text}\"",
    ]
    if claims_str:
        lines.append(claims_str)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Semantic search over enriched records")
    parser.add_argument("query", nargs="?", default=None,
                        help="Natural language search query")
    parser.add_argument("--top-k", type=int, default=10,
                        help="Number of results (default: 10)")
    parser.add_argument("--topic", type=str, default=None,
                        help="Filter by topic tag")
    parser.add_argument("--content-type", type=str, default=None,
                        help="Filter by content type")
    parser.add_argument("--author", type=str, default=None,
                        help="Filter by author")
    parser.add_argument("--rebuild", action="store_true",
                        help="Rebuild the search index from CSV")
    args = parser.parse_args()

    if not args.query and not args.rebuild:
        parser.print_help()
        sys.exit(1)

    embeddings, metadata = None, None
    if not args.rebuild:
        embeddings, metadata = load_index()

    if embeddings is None:
        if not args.rebuild:
            print("No cached index found. Building for the first time...\n")
        embeddings, metadata = build_search_index()
        print()

    if not args.query:
        print("Index rebuilt. Ready for queries.")
        return

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)

    results = search(
        args.query, embeddings, metadata, model,
        top_k=args.top_k,
        topic_filter=args.topic,
        content_type_filter=args.content_type,
        author_filter=args.author,
    )

    if not results:
        print("No results found.")
        return

    filter_parts = []
    if args.topic:
        filter_parts.append(f"topic={args.topic}")
    if args.content_type:
        filter_parts.append(f"type={args.content_type}")
    if args.author:
        filter_parts.append(f"author={args.author}")
    filter_str = f" [{', '.join(filter_parts)}]" if filter_parts else ""

    print(f"Search: \"{args.query}\"{filter_str}")
    print(f"Results: {len(results)} of {len(metadata)} records\n")

    for i, (score, meta) in enumerate(results, 1):
        print(format_result(i, score, meta))
        print()


if __name__ == "__main__":
    main()
