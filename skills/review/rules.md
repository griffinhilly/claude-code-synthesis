# Review Rules

## Hard Rules
- Review agents are read-only — they identify issues but don't fix them
- Be specific: "Line 47 has an off-by-one error" not "there might be bugs"
- Distinguish between must-fix issues and nice-to-have suggestions
- If success criteria weren't defined, note that as a process issue
- For trivial reviews, skip the subagent and review directly

## Gotchas
- Reviewing code you just wrote = confirmation bias. Always use a fresh-eyes subagent for non-trivial reviews.
- "No issues found" is almost always wrong for complex work. If you find zero issues, you're not looking hard enough — check your review dimensions.
- Data reviews that don't check actual values (just column names/types) miss the most dangerous errors.
- Don't nitpick formatting if a linter/formatter exists — focus on logic and correctness.
- The most valuable review finding is often not a bug but a missing test — "this code path has no verification."
- Red flag: if you find yourself writing "should work" or "looks correct" without citing specific evidence, you're not reviewing, you're rubber-stamping.
