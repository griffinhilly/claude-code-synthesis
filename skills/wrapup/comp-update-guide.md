# COMP Update Guide

Update each file as needed. Skip files with no relevant changes. Incorporate any issues the reviewer flagged.

## PLAN.md
- Refresh the `## Current State` section at top (what's in flight, blockers, next session)
- Mark completed items
- Add new items discovered during work
- Update timeline if relevant

## MEMORY.md
- New gotchas discovered
- Decisions made (with rationale and alternatives considered)
- Remove resolved items
- Keep it dashboard-format (under 50 lines)

## ORIENT.md (if project shape changed)
- New common operations added
- Codebase structure changed
- Known weirdness changed

## CLAUDE.md (rare — only when conventions change)
- New conventions established
- Schema changes
- New technical constraints discovered

## Propagation Check
After updating counts or status in any COMP file, grep the other COMP files for stale references to the old values. A single session can leave stale data in 3-4 files.

## Discoverability Check
After writing to MEMORY.md or creating a new guide, verify the knowledge is findable:
1. Would a future `/start` session surface this?
2. Is there a trigger in CLAUDE.md's Situational Guides that would load this when relevant?
3. Could `session-search.py` find it with obvious search terms?

Knowledge that exists but can't be found is not knowledge.

Reference: Compound Engineering ce-compound uses a 5-dimension overlap scoring system and mandatory discoverability verification after writing solution docs.

## Overlap Check
Before adding a new MEMORY.md entry, scan existing entries for overlap. If the new learning overlaps with an existing one, merge and note the reinforcement — lessons rediscovered across multiple projects are stronger signals. If it contradicts, flag for user resolution rather than silently overwriting.
