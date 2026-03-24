"""Canonical taxonomy definitions for LLM categorization.

This module is the single source of truth for your classification scheme.
Everything that touches categories should import from here — never hardcode
tag strings elsewhere.

Customize:
  1. Replace VALID_TOPICS with your domain's categories
  2. Replace VALID_CONTENT_TYPES with your classification types
  3. Populate TOPIC_FIXES as you discover LLM misnomers
  4. Update SYSTEM_PROMPT_TEMPLATE with your domain context
"""
import json

# --- Your domain categories (multi-label, 1-3 per record) ---
# Example: a product review dataset. Replace with your own.
VALID_TOPICS = [
    "electronics",
    "home_kitchen",
    "clothing_fashion",
    "health_wellness",
    "sports_outdoors",
    "books_media",
    "food_beverage",
    "automotive",
    "software_apps",
    "toys_games",
]

# --- Content type classification (single-label, exactly 1 per record) ---
VALID_CONTENT_TYPES = [
    "factual_claim",
    "opinion_argument",
    "advice_recommendation",
    "observation_insight",
    "humor_entertainment",
    "information_sharing",
]

# --- Fix mappings for common LLM hallucinations ---
# LLMs will invent tag names. Rather than re-running expensive batch jobs,
# map invalid tags to their closest valid equivalent (or None to drop them).
TOPIC_FIXES = {
    # Content types mistakenly used as topics — drop them
    "information_sharing": None,
    "observation_insight": None,
    # Common LLM misnomers → canonical form
    "tech": "electronics",
    "technology": "electronics",
    "kitchen": "home_kitchen",
    "fashion": "clothing_fashion",
    "health": "health_wellness",
    "fitness": "health_wellness",
    "sports": "sports_outdoors",
    "outdoor": "sports_outdoors",
    "books": "books_media",
    "food": "food_beverage",
    "auto": "automotive",
    "cars": "automotive",
    "apps": "software_apps",
    "games": "toys_games",
}

CONTENT_TYPE_FIXES = {
    "argument_opinion": "opinion_argument",
    "recommendation": "advice_recommendation",
}

# --- LLM prompt template ---
# This is sent to Claude (typically Haiku for cost efficiency) along with
# a batch of records. The prompt asks for structured JSON output keyed by
# record ID, making it easy to merge back into your CSV.
SYSTEM_PROMPT_TEMPLATE = """You are categorizing records. For each record, provide:

1. **topics**: 1-3 topic tags from this list (multi-label):
   {topics_json}

2. **content_type**: Exactly 1 from this list:
   {content_types_json}

3. **extracted_claims**: For records with content_type "factual_claim" or "advice_recommendation", extract specific claims as a JSON array of short strings. For other content types, use an empty array [].

4. **claim_confidence**: "high", "medium", or "low" if there are extracted claims, otherwise "none".

Rules:
- Every record gets 1-3 topics and exactly 1 content_type
- Use ONLY the exact tag strings listed above
- extracted_claims should be concise factual statements or actionable advice items
- Consider the full context of each record

Output ONLY a JSON object keyed by record_id. Example:
```json
{{
  "record_123": {{
    "topics": ["electronics", "software_apps"],
    "content_type": "advice_recommendation",
    "extracted_claims": ["USB-C charging is faster than Lightning"],
    "claim_confidence": "medium"
  }}
}}
```"""


def get_system_prompt():
    """Return the categorization system prompt with current taxonomy."""
    return SYSTEM_PROMPT_TEMPLATE.format(
        topics_json=json.dumps(VALID_TOPICS),
        content_types_json=json.dumps(VALID_CONTENT_TYPES),
    )
