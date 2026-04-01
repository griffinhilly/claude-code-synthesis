# Risk Identification Checklist

List anything that could go wrong. Use this checklist — don't just freeform.

## Technical Risks
- [ ] Data quality issues (missing fields, encoding, schema changes)
- [ ] Assumptions that might be wrong (check each explicitly)
- [ ] External dependencies (APIs, services, libraries that could break)
- [ ] Irreversible actions that need extra care (DB mutations, file deletions, git force-push)
- [ ] Performance bottlenecks (large data, slow queries, memory limits)

## Process Risks
- [ ] Scope creep potential (is the boundary clear?)
- [ ] Multi-session risk (if this takes >1 session, what state needs to persist?)
- [ ] Order-of-operations sensitivity (does step N depend on step M in non-obvious ways?)
- [ ] Verification gaps (how will we know each step succeeded before moving on?)

## Knowledge Risks
- [ ] Unfamiliar territory (should we research first?)
- [ ] Stale assumptions from MEMORY.md (verify anything time-sensitive)
- [ ] Missing context (do we need information we don't have?)

For each risk identified, propose a mitigation. If a risk can't be mitigated, flag it for the user.
