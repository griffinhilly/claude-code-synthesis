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

## Rule Promotion Gate

**Principle: convergent signal across runs justifies investment. A single sighting is a candidate; a second sighting is a rule.**

For every candidate rule, learning, or pattern this session would promote into permanent doctrine (CLAUDE.md, MEMORY.md, project memory files, feedback-style memos), apply the **≥2 sightings** gate:

1. **Is this the first sighting?** Don't promote yet. Append to `~/.claude/candidate-rules.md` as a pending entry with: date, one-sentence rule, source session/project, what would-trigger-promotion (what specific second sighting would justify codifying it).
2. **Has a candidate-rule been observed before?** Check `~/.claude/candidate-rules.md` for prior entries that match. If a pending candidate matches what happened this session, that's the second sighting — promote it now (move to its target file, delete from candidate-rules.md).
3. **Genuine exceptions (skip the gate):** Bug fixes that revealed a class of bugs (already covered by "operationalize every fix"); explicit user requests to codify; security/safety items.

Why this gate exists: single-occurrence rules accumulate as permanent doctrine that doesn't fire and creates resolver decay. Two independent observations is the threshold where promotion is justified. See CLAUDE.md doctrine ("Cumulative best practices with deduplication") for the broader principle this operationalizes.

This gate applies recursively — it's why the rule itself was promoted (this is the second time the pattern has surfaced in workflow design).

## Codify-Before-Repeating Check

Per CLAUDE.md "Codify before repeating": review what happened this session for **recurring task shapes that should become skills or skill modes**. Ask explicitly:

- Did you do any multi-step task this session that has the shape of something likely to recur?
- Did you write the same kind of code, prompt, or workflow more than once in slightly different forms?
- Were there manual fixes or workarounds that will be re-needed next time?

If yes, propose codification (new skill, new skill flag, new guide, or CLAUDE.md bullet) before ending the session. Use the promotion gate above — first occurrence goes to candidate-rules.md, second occurrence promotes.
