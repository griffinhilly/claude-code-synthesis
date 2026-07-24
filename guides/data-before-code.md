# Fix Data Gaps Before Adding Code Workarounds

When generated content shows uniformity, repetitive patterns, or distribution skew that suggests the upstream content set is the gap, surface it as a content/data issue before adding filters, fallback logic, or rotation rules in code.

**Why:** This was flagged when three successive code "fixes" were made for a quiz bias that was actually caused by one topic category being the only one with a particular question type available. The code changes masked the symptom without addressing the root cause, and the forced rotation ("demand the user see one question from each category") was a worse UX than the original problem.

**How to apply:** Observable patterns that should trigger this check, BEFORE writing code:
- Generated output is dominated by one source/category despite a query that should cover many
- Random selection keeps surfacing the same items
- "Fairness" or "rotation" requirements are surfacing as code-level patches
- Distribution skew that doesn't match the query intent

When you see one of these, ask: is this a *content/data gap*, not a *code logic problem*? If yes, surface the diagnosis ("only category X has items at stage Y") and propose expanding the content rather than jumping to code. Let the user decide the approach — code workarounds are a legitimate fallback, but they should be the chosen response, not the default response.

The original failure mode was self-reflective ("noticed I was tempted to add a workaround"). The reliable trigger is observable: skewed distributions, uniformity in generated outputs, fairness logic creeping into code.
