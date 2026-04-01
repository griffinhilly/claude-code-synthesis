---
name: retro
description: Periodic retrospective — assess what Claude did well, what went poorly, and what to improve
user-invocable: true
disable-model-invocation: true
argument-hint: [weekly | session | project <name>]
---

# Retrospective

A structured review of how Claude has been performing, designed to surface patterns and turn them into feedback memories or CLAUDE.md improvements.

## Scope

Parse `$ARGUMENTS` for scope:

| Scope | What it reviews | Default |
|-------|----------------|---------|
| `session` | Just this conversation | default if no argument |
| `weekly` | All work in the past 7 days across projects |
| `project <name>` | Recent work in a specific project |

## Process

### Step 1: Gather Evidence

**Session scope:** Review the current conversation — what was attempted, what succeeded, what failed, what required correction.

**Weekly scope:** Read MEMORY.md and PLAN.md from each active project (check the Project Dashboard in auto-memory). Look for:
- Decisions recorded in MEMORY.md
- Feedback memories in `~/.claude/projects/<project-slug>/memory/`
- Recent git history (`git log --since="7 days ago" --oneline`) in active project directories

**Project scope:** Read the named project's COMP files + recent git history.

### Step 2: Assess (Present to User)

Organize findings into four categories:

**WORKED WELL** — Things Claude did that saved time, caught errors, or produced good results. Be specific: name the task, the approach, and why it worked.

**WENT POORLY** — Things that wasted time, required correction, or produced bad results. Be honest. Include:
- Times the user had to correct Claude
- Approaches that failed before succeeding
- Scope creep or overengineering incidents
- Wrong assumptions that went unchecked

**PATTERNS** — Recurring themes across multiple instances. These are the most valuable findings. Examples:
- "Claude keeps over-engineering database queries when simple ones would work"
- "Bug fixes are faster when reproduction tests are written first"
- "Planning phases run too long before the user redirects to execution"

**SUGGESTIONS** — Concrete changes to try. Each should be one of:
- A new feedback memory to save
- A CLAUDE.md rule to add or modify
- A skill to create or improve
- A workflow change to try next session

### Step 3: Act (With User Approval)

For each suggestion the user approves:
- Save feedback memories immediately
- Edit CLAUDE.md if warranted
- Note skill ideas in the relevant project's PLAN.md

Do NOT make changes without user approval. Present findings, wait for decisions.

### Output Format

```
RETRO — [scope] ([date range])

## Worked Well
1. [specific example]
2. [specific example]

## Went Poorly
1. [specific example with what happened and what should have happened]
2. [specific example]

## Patterns
- [recurring theme]
- [recurring theme]

## Suggestions
1. [concrete change] → [feedback memory / CLAUDE.md edit / skill idea]
2. [concrete change] → [feedback memory / CLAUDE.md edit / skill idea]
```
