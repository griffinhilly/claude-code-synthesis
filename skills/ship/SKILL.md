---
name: ship
description: Pre-commit readiness check. Verifies tests, COMP freshness, uncommitted changes, then drafts commit message and stages specific files.
user-invocable: true
disable-model-invocation: false
argument-hint: [commit message hint]
---

# /ship -- Pre-Commit Readiness Check

Verify everything is ready to commit, then stage and commit with user approval.

## Input

Commit message hint: `$ARGUMENTS`

If provided, use this to guide the commit message. If not, infer from the changes.

## Process

### Step 1: Gather State

Run these in parallel:

1. `git status` -- see all tracked/untracked changes
2. `git diff` -- unstaged changes
3. `git diff --cached` -- already-staged changes
4. `git log --oneline -5` -- recent commit style reference

### Step 2: Assess Readiness

Check each dimension:

**Tests:**
- Look for a test command in the project's CLAUDE.md (e.g., `npm test`, `pytest`, `cargo test`)
- If found, run it. Record PASS/FAIL.
- If no test command is defined, record NONE.

**COMP freshness:**
- For each COMP file (CLAUDE.md, ORIENT.md, MEMORY.md, PLAN.md) in the project root:
  - Check if it exists
  - Check `git log -1 --format="%ai" -- <file>` for last commit date
  - Compare against the current session's work -- if meaningful work was done but the relevant COMP file wasn't updated, flag it as STALE
  - CLAUDE.md and ORIENT.md rarely need updating -- only flag if architecture or project shape changed
  - MEMORY.md and PLAN.md should reflect the current session's decisions and progress

**Uncommitted work:**
- List all modified, added, and untracked files
- Categorize: which are related to the current work vs. unrelated leftovers
- Flag any files that look like they should be included but aren't staged

**Data pipeline check:**
- If the changes involve data pipeline scripts or outputs, suggest running `/verify` first
- This is advisory, not blocking

### Step 3: Present Readiness Dashboard

```
SHIP READINESS -- [project name]
Tests:        [PASS / FAIL / NONE]
COMP files:   [UP TO DATE / STALE -- list which]
Uncommitted:  [list of unstaged changes relevant to this work]
Verdict:      [READY / NOT READY -- reasons]
```

### Step 4a: If NOT READY

- List what needs to happen first, in priority order
- Offer to fix what can be fixed automatically:
  - Update stale COMP files (run through the `/finalize` logic)
  - Stage forgotten files
- Do NOT proceed to commit. Wait for user direction.

### Step 4b: If READY

1. **Draft commit message:**
   - 1-2 sentences focusing on "why" not "what"
   - Use the `$ARGUMENTS` hint if provided
   - Match the style of recent commits (from git log)
   - End with the Co-Authored-By trailer

2. **Stage specific files:**
   - List exactly which files will be staged
   - NEVER use `git add -A` or `git add .`
   - Only stage files related to the current work
   - Present the list for user review

3. **CHANGELOG check:**
   - If a CHANGELOG.md or CHANGELOG exists in the project, check if it was updated
   - If not, suggest an entry in user-facing voice ("You can now..." not "Refactored X")

4. **Present for approval:**
   ```
   STAGED FILES:
   - path/to/file1.py
   - path/to/file2.md

   COMMIT MESSAGE:
   <the drafted message>

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
   ```
   Wait for explicit user approval before running `git commit`.

5. **After user approves:**
   - Stage the listed files with individual `git add` commands
   - Commit using a HEREDOC for the message
   - Run `git status` to confirm clean state
   - Do NOT push. If user wants to push, they'll say so.

## Rules

- **Never push** to remote without explicit user approval
- **Never `git add -A` or `git add .`** -- the PreToolUse hook blocks this anyway
- **Stage only related files** -- unrelated changes get left for a separate commit
- **Commit message via HEREDOC** -- ensures correct formatting of multi-line messages
- **User approval is mandatory** -- never auto-commit, even if everything looks ready
- **Match project commit style** -- check recent git log for conventions (conventional commits, imperative mood, etc.)
