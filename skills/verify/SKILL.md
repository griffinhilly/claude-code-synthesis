---
name: verify
description: Verify outputs after pipeline steps, implementations, or any multi-step work. Catches missing data, stale references, broken assumptions. Use after completing significant work, before declaring done.
user-invocable: true
disable-model-invocation: false
argument-hint: [target — what to verify]
---

# Verify

Run after any significant output to catch what was missed. The goal is to prevent the class of error where work appears complete but isn't — unfetched data, stale counts, broken assumptions, missing files.

## Input

Target to verify: `$ARGUMENTS`

If no arguments, verify the most recent significant output or pipeline step.

## Process

### Step 1: Identify What to Verify

Determine the verification type from context:

| Type | Trigger | What to Check |
|------|---------|--------------|
| **Data pipeline** | After running a pipeline (refresh, ETL, etc.) | Row counts, coverage rates, missing fields, stale references |
| **Implementation** | After implementing from a plan | All plan items addressed, tests pass, no regressions |
| **Analysis** | After producing analysis/reports | Claims supported by data, no unfetched sources, numbers consistent |
| **File output** | After generating files | Files exist, non-empty, correct format, no orphan references |

### Step 2: Run Checks

Read the relevant files and run checks appropriate to the type. See @check-types.md for the four composable check categories (data, completeness, consistency, assumption). A single verification usually draws from multiple categories — e.g., a data pipeline verification runs data + completeness + consistency.

### Step 3: Report

Format findings as:

```
VERIFICATION — [target]

PASSED:
- [check]: [result]

FAILED:
- [check]: [what's wrong] → [suggested fix]

WARNINGS:
- [check]: [not broken but suspicious]

COVERAGE: [X/Y checks passed]
```

If everything passes, say so concisely. Don't pad the report.

### Step 4: When Verification Fails — Debug Protocol

If Step 3 reports FAILED items, do not jump to fixing. See @debug-protocol.md for the full 4-phase protocol.

## Red Flag Language (from Superpowers)
If you catch yourself or a subagent using any of these phrases, STOP and re-verify:
- "Done!", "should work", "probably fine", "seems to", "I believe this handles"
- "Great!", "Perfect!" (sycophantic completion signals)
These indicate a completion claim without fresh evidence. Run the actual checks.

## Three-Fix Escalation Rule (from Superpowers)
If a verification failure has been "fixed" 3 times and still fails, STOP. Don't try a fourth fix. The architecture is probably wrong. Escalate to the user: "This has failed 3 fixes. The approach itself may need rethinking."

## Gotchas
- The most dangerous failures are silent ones — things that LOOK complete but aren't. Prioritize checking those.
- Don't just verify what was done. Verify what SHOULD have been done but might have been skipped.
- When verifying data pipelines, always check the enrichment chain: raw → enriched → categorized → indexed. A break at any stage propagates silently.
- Stale counts in COMP files are the most common consistency failure after batch operations.
- After writing to MEMORY.md or project docs, verify the information is actually findable by future agent sessions (discoverability check).
