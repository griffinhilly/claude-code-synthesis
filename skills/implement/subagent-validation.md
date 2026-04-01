# Subagent Validation Protocol

## Validate Subagent Reports

After each subagent returns, validate before accepting -- **do not trust the report:**
1. Are all report sections present per the delegation template?
2. Does the claimed output actually exist? (Read the files, run the query, check the data.)
3. If status is DONE, verify the success criteria independently -- a subagent claiming DONE without evidence is equivalent to NEEDS_REVIEW.

## Status Outcomes and Handling

- **DONE** -- Verify independently, then proceed
- **DONE_WITH_CONCERNS** -- Read concerns before proceeding. If about correctness/scope, address before moving on.
- **BLOCKED** -- Assess: context problem (provide more), task too large (split), or plan is wrong (escalate to user). Never force retry without changes.
- **NEEDS_CONTEXT** -- Provide missing info and re-dispatch

## System-Wide Check (for large tasks)

Before marking any large task as done, answer these 5 questions:
1. Do all affected files reflect the change?
2. Are COMP file references still accurate?
3. Would a fresh-context agent understand what happened?
4. Are there downstream dependencies that need updating?
5. Is there a way to verify the change works, and has it been run?
