# Review Output Format

Organize findings as:

## Pass
Criteria that are fully met. One line each.

## Issues
Problems found, each with:
- **Severity**: Critical / Major / Minor
- **Location**: file:line or specific section
- **Issue**: What's wrong
- **Evidence**: How you know (not just "it looks wrong" — cite the specific line, value, or test)
- **Suggested fix**: Specific recommendation (optional for Minor)

Order by severity descending.

## Suggestions
Optional improvements, clearly marked as optional. These are NOT issues — the work passes without them. Keep this section short. If you can't articulate why a suggestion matters, cut it.

## Summary
One-line verdict: "Passes with N issues (X critical, Y major, Z minor)" or "Does not pass — N critical issues must be addressed."
