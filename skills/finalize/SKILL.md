---
name: finalize
description: End-of-session COMP update — record decisions, progress, and state changes
user-invocable: true
disable-model-invocation: false
argument-hint: [project path or name]
---

# Session Finalization

Update the COMP files for the current project to capture this session's work.

## Determine Scope

If `$ARGUMENTS` specifies a project, use that directory. Otherwise, infer from the current working directory and conversation context. If unclear, ask.

## Process

### Step 1: Summarize the Session
Review the conversation to identify:
- What was accomplished
- What decisions were made (and why)
- What files were created, modified, or deleted
- What's left to do
- Any gotchas or surprises discovered

### Step 2: Update PLAN.md — Current State Section
Refresh the `## Current State` section at the top of PLAN.md:
- What's in flight right now (current step, active branches, open questions)
- Known broken things, blockers
- What to do next session
- Keep under 20 lines — this is a session-scoped snapshot, not a log

Also update the rest of PLAN.md:
- Mark completed items as done
- Add new items if scope changed
- Update "current phase" or "next steps" sections
- Note any blockers

### Step 3: Update MEMORY.md
Add or update entries for:
- Decisions made this session (what, why, what alternatives were considered)
- Technical gotchas discovered
- Any durable information that would help future sessions

Do NOT duplicate information already in CLAUDE.md. MEMORY.md is for accumulated knowledge, not permanent reference.

### Step 4: Update ORIENT.md (if needed)
Only if:
- New scripts or common operations were added
- Project shape changed (new directories, reorganization)
- Known weirdness changed

### Step 5: Update CLAUDE.md (if needed)
Only if:
- New conventions were established
- Schema changed
- Architecture changed in ways that affect agent behavior

### Step 6: Present Summary
Show the user a brief summary of what was updated:
- Files modified
- Key items recorded
- Next steps noted

## Rules
- Read each COMP file before editing it
- Don't duplicate information across COMP files
- Keep entries concise — future sessions need scannable notes, not essays
- If nothing meaningful happened this session, say so rather than adding noise
