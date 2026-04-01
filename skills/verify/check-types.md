# Verify — Check Type Checklists

Referenced by SKILL.md Step 2. Run the checks appropriate to the verification type identified in Step 1.

## Data Checks
- Row/record counts match expectations (compare before/after if applicable)
- No unexpected NaN/null rates in key columns
- All referenced data sources were actually consulted (not just assumed)
- Counts in documentation match actual counts in data

## Completeness Checks
- URLs in data — were articles/content actually fetched?
- References to other files — do those files exist?
- Pipeline steps — did every step run, or did some silently skip?
- Plan items — is every item addressed, not just the first few?

## Consistency Checks
- Counts in COMP files match actual data
- Terminology is consistent (no stale names/labels from before a rename)
- Date references are current (not from a previous session)

## Assumption Checks
- What was assumed true that wasn't verified?
- What data was accessed indirectly (through a summary) vs. directly (by reading the source)?
- Were quoted/linked sources actually read, or only the surface-level reference?
