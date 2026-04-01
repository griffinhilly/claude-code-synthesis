---
name: debug
description: Structured debugging with mandatory evidence gathering before any fix attempt. 4-phase protocol (Observe → Hypothesize → Reproduce → Fix) with hard gates between phases.
user-invocable: true
disable-model-invocation: false
argument-hint: <bug description, error message, or "something is wrong with X">
---

# Structured Debugging

Systematic root-cause investigation. The goal is to find the actual cause before attempting any fix.

## Input

Bug to investigate: `$ARGUMENTS`

If no arguments, ask: "What's broken? Describe the symptom — what you expected vs what happened."

## The Rule

**No fix attempt before Phase 1 evidence is written down. Fixing without evidence is guessing.**

## Phase 1: OBSERVE — Gather Evidence

**Gate: Cannot proceed to Phase 2 without a written evidence summary.**

Do not hypothesize yet. Collect data:

1. **Read the error.** Full message, stack trace, exit code. Not a summary — the actual text.
2. **Reproduce.** Run the failing operation. Confirm it fails consistently. Note exact conditions.
3. **Inspect each layer.** For data pipelines, use `~/.claude/guides/pipeline-diagnostic.md` — walk stages in order, stop at the first stage showing incorrect data. For code bugs, trace the call path from entry point to failure.
4. **Check recent changes.** What changed since it last worked? `git log`, `git diff`, recent session-search results.
5. **Record the evidence:**

```
EVIDENCE SUMMARY — [bug description]
Error: [exact message]
Reproduced: [yes/no, conditions]
First failing layer: [stage name]
Data at failure point: [actual values]
Recent changes: [what changed]
```

### Red Flags (return to Phase 1)

If you catch yourself thinking any of these, you skipped Phase 1:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before inspecting data at the failure point

## Phase 2: HYPOTHESIZE — Candidate Causes

**Gate: Cannot proceed to Phase 3 without 3+ ranked hypotheses.**

Generate at least 3 candidate root causes:
- Rank by likelihood given the evidence
- For each, state what evidence would confirm or rule it out
- Prefer hypotheses that explain ALL observed symptoms over those explaining only one
- If the failure is at a layer boundary (data passes between stages), check both the producer and consumer

## Phase 3: REPRODUCE — Prove the Cause

**Gate: Cannot proceed to Phase 4 without a confirmed root cause.**

Test hypotheses one at a time, cheapest first:

| Bug type | Reproduction method |
|----------|-------------------|
| Data bug | Query that shows bad data at the identified stage |
| Logic bug | Minimal script or test that triggers the wrong behavior |
| Pipeline bug | Run the failing stage in isolation with known-good input |
| Integration bug | Trace the exact request/response at the boundary |

If hypothesis is confirmed → proceed to Phase 4.
If hypothesis is ruled out → test the next one.
If all hypotheses ruled out → return to Phase 1 with new evidence from the tests.

## Phase 4: FIX — Confirmed Root Cause Only

1. **Fix the confirmed cause.** Nothing else. No "while I'm here" changes.
2. **Write a test** that would have caught this bug.
3. **Check for siblings.** Grep for the same pattern elsewhere in the codebase. Are there other instances of the same mistake?
4. **Update MEMORY.md** if the gotcha is non-obvious or likely to recur.
5. **Verify the fix.** Run the reproduction from Phase 3. Does it pass now? Do other tests still pass?

## Three-Fix Escalation

If Phase 4 has been attempted 3 times and the bug persists, **STOP**. Don't try a fourth fix. The approach or architecture is wrong. Escalate to the user:

"This has survived 3 fix attempts. The root cause may be architectural, not local. Here's what I've tried and why each failed: [summary]. I recommend reconsidering [specific aspect]."

## After Fixing

Run `/verify` on the affected output to catch any secondary effects. Then suggest `/learn gotcha` to capture the lesson if it's reusable across projects.
