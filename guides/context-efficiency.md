# Context Efficiency Guide

*Loaded when: sessions feel slow, token usage seems high, or projects have large always-loaded context.*

## Input Token Ratio Monitoring

A healthy input-to-output ratio is roughly 10:1 to 30:1. If you notice ratios above 100:1, you're paying to re-read context, not to think. Symptoms:
- Sessions feel slow despite simple requests
- Compaction happening frequently
- Large COMP files being loaded every turn

### Fixes

1. **Move bulk context to semantic search.** If a project has hundreds of topics, entries, or records, don't load them into CLAUDE.md or MEMORY.md. Build a search index and query on demand. This can cut input tokens 40-60%.

2. **Progressive disclosure.** CLAUDE.md should contain triggers and pointers, not content. Situational guides get loaded only when relevant. This is already the pattern — enforce it.

3. **Aggressive context clearing.** When switching between unrelated tasks in the same session, use `/clear` or start a new session. Context bleed between unrelated tasks is the leading failure mode for long sessions.

## Domain vs Procedural Knowledge

Track two types of knowledge separately in project files:

- **Domain knowledge**: What things are — product context, data schemas, naming conventions, API shapes, business rules. Changes rarely.
- **Procedural knowledge**: How to do things — build commands, deployment steps, common error fixes, pipeline recipes. Changes when tools change.

In MEMORY.md, prefix entries with `[domain]` or `[procedural]` to make retrieval faster. In CLAUDE.md, keep domain knowledge in the main file (it's always relevant) and push procedural knowledge to guides (it's only relevant when doing that procedure).

## Context Window Hygiene

- **Separate contexts for adversarial review.** When reviewing your own work, spawn a fresh subagent with a clean context window. The reviewing agent shouldn't share the implementation agent's assumptions.
- **Plan tokens are cheap.** Spending 5 minutes in plan mode saves 50 minutes of implementation retries. Detailed plans survive compaction better than vibe-prompted features.
- **Compaction-safe artifacts.** When you produce something important (a schema, a decision, a list), write it to a file immediately. Don't rely on it surviving compaction in conversation history.
