# /start — Session Kickoff

*v1.0 — Read project state, surface context, and micro-plan the session*

Begin a working session by loading context, summarizing current state, and planning what to work on.

## Input
$ARGUMENTS

## Instructions

### Step 0: Determine Session Mode

Parse `$ARGUMENTS` for a mode keyword: `quick`, `standard`, or `full`. Default is `standard` if not specified.

| Mode | Context Loading | Dashboard | Plan | When to Use |
|------|----------------|-----------|------|-------------|
| `quick` | PLAN.md (Current State) + MEMORY.md | Skip | Skip — just start working | Bug fixes, small edits, quick questions |
| `standard` | PLAN.md + MEMORY.md + CLAUDE.md | Brief (3-5 lines) | Micro-plan if task given | Default — most sessions |
| `full` | All 4 COMP files + auto-memory | Full dashboard | Detailed plan + scope check | New features, phase transitions, multi-session work |

### Step 1: Determine Scope

If `$ARGUMENTS` names a project or path, use that. Otherwise, use the current working directory.

If `$ARGUMENTS` includes a task description (e.g., `/start my-project — build the prediction model`), note the task for Step 4.

### Step 2: Load Context (scaled by mode)

**Quick mode:** Read PLAN.md's `## Current State` section (where are we?) and MEMORY.md (gotchas). Skip everything else — the user wants to get moving.

**Standard mode:** Read in parallel:
1. **PLAN.md** — roadmap + current state section at top
2. **MEMORY.md** — working notes, gotchas, recent decisions
3. **CLAUDE.md** — project instructions (scan for current phase/status)

**Full mode:** Read in parallel:
1. **CLAUDE.md** — project instructions
2. **ORIENT.md** — project orientation, codebase shape, common operations
3. **MEMORY.md** — working notes, gotchas, recent decisions
4. **PLAN.md** — roadmap + current state section at top
5. **Auto-memory** (`~/.claude/projects/C--Users-griff/memory/MEMORY.md`) — cross-project context

### Step 3: Present Status Dashboard

**Quick mode:** Skip entirely — go straight to Step 4.

**Standard mode:** Output a brief dashboard (3-5 lines):
```
SESSION START — [Project Name] (standard)
STATUS: [Current phase / active work]
GOTCHAS: [Active technical hazards relevant to today's work]
```

**Full mode:** Output a full dashboard:
```
SESSION START — [Project Name] (full)
STATUS: [Current phase / active work]
LAST SESSION: [Key outcomes from MEMORY.md]
PENDING: [Unfinished items, known issues, blocked tasks]
GOTCHAS: [Active technical hazards relevant to today's work]
```

### Step 4: Micro-Plan

**Quick mode:** If a task was provided, start working immediately. If not, ask: "What's the quick fix?"

**Standard mode:** If the user provided a task, propose a brief micro-plan (3 steps max). If not, suggest the next item from PLAN.md.

**Full mode:** If the user provided a task, propose a detailed plan with scope estimate. Apply scope discipline:
- If the task sounds like a multi-session effort, say so and propose a first-session subset.
- If there are prerequisites or blockers visible in the COMP files, flag them.
- If a reference repo might help, ask.

If no task was provided, ask:
> "What are we working on today? Here's what PLAN.md suggests as next: [next item from PLAN.md]"

### Step 5: Confirm and Begin

**Quick mode:** Skip — start immediately after Step 4.

**Standard/Full mode:** Wait for the user to confirm or adjust the plan before starting implementation.

## Examples

```
/start quick                              # Minimal context, just start
/start my-project — fix the data query   # Standard mode (default) with task
/start full Agencyism                     # Full context load for deep work
/start full my-project — design skill format   # Full mode with specific task
```
