---
name: wrapup
description: End-of-session closer. Compiles session notes, gets fresh-context review, updates COMP files, checks skill health and execution gaps, runs bloat check.
user-invocable: true
disable-model-invocation: false
argument-hint: [noprune|prune|noreview|project:path]
---

# /wrapup — Session Closer

End a working session cleanly.

## Input
$ARGUMENTS

## Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `project:path` | Current directory | Which project to finalize |
| `noprune` | Off | Skip the bloat check |
| `prune` | Off | Run full `/prune` instead of dryrun |
| `noreview` | Off | Skip the session reviewer agent |

## Process

### Step 1: Compile Session Notes
Read @session-notes-template.md — fill in each field from the session.

### Step 2: Session Review (fresh context)
Unless `noreview` flag is set. Read @session-review-guide.md for how to dispatch and present the reviewer.

### Step 3: Update COMP Files
Read @comp-update-guide.md for what to update in each file.

### Step 4: Skill & Execution Health
Read @health-check-guide.md for the skill iteration check, execution reliability self-check, and cross-project transfer.

### Step 5: Bloat Check
Unless `noprune` flag is set, run the lightweight check described in @bloat-check-guide.md.

### Step 6: Session Summary
Read @summary-template.md for the output format.

## Examples
```
/wrapup                    # Full wrapup with session review
/wrapup project:~/my-app   # Finalize specific project
/wrapup noreview           # Skip the reviewer agent (quick sessions)
/wrapup prune              # Full prune analysis included
```
