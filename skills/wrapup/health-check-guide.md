# Skill & Execution Health Check

## Skill Iteration Check
- Which skills fired this session (invoked by user or model)?
- For each: did the output quality match expectations?
- If a skill underperformed, note what went wrong and update its gotchas file (or create one).
- If a skill worked surprisingly well, note what made it work in the skill's examples or gotchas.

Check `~/.claude/skill-usage.log` if available for the session's skill invocations.

## Execution Reliability Self-Check
Review the CLAUDE.md behavioral instructions against what actually happened this session:
- Were there dialectic triggers that weren't suggested? (presented 2+ options, irreversible decisions, user uncertainty)
- Was `/verify` run after significant outputs, or was completion declared without verification?
- Was argue-the-opposite applied before significant commitments?
- Were red flag phrases used ("should work", "Done!") without fresh verification?

For each missed trigger: flag it in the session summary. Suggest whether:
- The instruction needs **stronger triggering** (promote from behavioral → composed in a skill step, or → deterministic via hook)
- The instruction **isn't earning its place** and should be revised or removed

## Skill Execution Health

Read `~/.claude/skill-usage.log` for the current session's skill invocations (entries are timestamped).

Check these pairing rules against the log:

1. **implement without verify**: If `/implement` was used this session but `/verify` does not appear after it, flag it. Implementation without verification is the #1 source of silent failures.
2. **Significant work without review**: If the session involved multi-file changes or non-trivial logic but `/review` was never invoked, flag it. Light sessions (single config edit, COMP updates) are exempt.
3. **Missing /start**: If `/start` was not the first skill invoked this session, note it. Skipping /start risks working on stale context or the wrong branch.
4. **Skill gap suggestions**: Based on what happened this session, suggest any skills that were skipped but probably should have run. Common gaps:
   - Heavy implementation with no `/review` or `/verify`
   - Session end approaching with no `/wrapup` (you are running it now, so this is fine)
   - Plan changes made during implementation without `/plan-task` to formalize them

Report which skills were used this session (from the log) and list any flags. If no flags, say so in one line.

## Cross-Project Transfer
- Did this session produce any learnings that apply to other projects?
- Any patterns, gotchas, or techniques that should be noted in another project's MEMORY.md?
- Any skills that should be updated based on cross-project experience?

If nothing notable on any of these, say so in one line and move on. Don't fabricate health issues.
