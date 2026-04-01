# Verify — Debug Protocol

Referenced by SKILL.md Step 4. Follow these phases in order when verification reports FAILED items.

## Phase 1 — OBSERVE (mandatory before any fix)

Write down the evidence: error messages, actual vs expected values, which pipeline stage shows wrong data. No hypotheses yet — just data. For multi-stage pipelines, walk the stages in order (see `~/.claude/guides/pipeline-diagnostic.md`) and stop at the first stage that shows incorrect output.

## Phase 2 — HYPOTHESIZE

Generate 3+ candidate causes ranked by likelihood. For each, state what evidence would confirm or rule it out. Prefer hypotheses that explain all observed symptoms over those that explain only one.

## Phase 3 — REPRODUCE

Try to reproduce via: (a) minimal script that triggers the bug, (b) specific input that produces wrong output, or (c) query that shows bad data. If you can't reproduce, escalate to the user — don't guess.

## Phase 4 — FIX

Fix only the confirmed root cause. Then: (a) write a test/check that would have caught it, (b) grep for sibling bugs (same pattern elsewhere), (c) update MEMORY.md with the gotcha if it's non-obvious.

## Gate Rule

No fix attempt before Phase 1 evidence is written down. Fixing without evidence is guessing.
