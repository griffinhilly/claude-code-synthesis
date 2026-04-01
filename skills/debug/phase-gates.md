# Debug Phase Gates

## Gate Criteria

Each phase has a hard gate. You cannot proceed without meeting it.

| Phase | Gate | Evidence required |
|-------|------|------------------|
| 1 → 2 | Written evidence summary | Error message, reproduction status, first failing layer, data at failure point |
| 2 → 3 | 3+ ranked hypotheses | Each with confirmation/refutation criteria |
| 3 → 4 | Confirmed root cause | Specific hypothesis confirmed by reproduction |
| 4 → Done | Fix verified | Reproduction passes, existing tests pass, no regressions |

## What "Confirmed" Means

A root cause is confirmed when:
- You can reproduce the bug reliably with specific input
- Your hypothesis predicts the exact failure observed
- Changing the identified cause (and only that) fixes the reproduction

A root cause is NOT confirmed when:
- "It seems like it might be..."
- "This is the most likely explanation"
- "The fix seems to work" (without re-running the reproduction)

## Escalation Triggers

Return to a previous phase when:

| Signal | Action |
|--------|--------|
| Fix doesn't resolve the reproduction | Return to Phase 2 — your root cause was wrong |
| New symptoms appear after fix | Return to Phase 1 — gather evidence on the new symptoms |
| 3 fixes attempted, bug persists | STOP — escalate to user |
| Can't reproduce at all | Escalate to user — intermittent bugs need different tools |

## Pipeline-Specific Gates

For data pipeline bugs, Phase 1 has an additional requirement:

**Identify the first failing stage.** Walk the pipeline from SOURCE to OUTPUT using `~/.claude/guides/pipeline-diagnostic.md`. Check data at each stage boundary. The first stage where output doesn't match expectations is the investigation target.

Don't investigate downstream stages — they may be producing wrong output because they received wrong input, not because their logic is broken.
