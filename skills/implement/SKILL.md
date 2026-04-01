---
name: implement
description: Execute a pre-defined plan using implementation agents (no design changes)
user-invocable: true
disable-model-invocation: false
argument-hint: <plan reference or description>
---

# Implementation Agent

Execute a plan that has already been designed and approved. This is the "do" phase -- no redesigning.

## Input

Plan to implement: `$ARGUMENTS`

If no arguments, look for the most recently discussed plan in the conversation.

## Process

### Step 1: Locate the Plan
Find the plan to implement. Sources:
- Explicitly provided in arguments
- Most recent /plan-task output in conversation
- Project PLAN.md

If no plan exists, STOP and tell the user: "No plan found. Run /plan-task first, or describe what to implement."

### Step 2: Verify Prerequisites
Before starting:
- Read relevant COMP files (CLAUDE.md for conventions, MEMORY.md for gotchas)
- Confirm all dependencies are met
- Identify any sub-tasks that can run in parallel

### Step 2.5: Triage Complexity

Assess the plan's scope and choose execution strategy:
- **Trivial** (single file, well-understood): Execute directly, skip subagents. Don't waste tokens on delegation overhead.
- **Small** (few files, clear spec): Execute directly or single subagent.
- **Large** (multi-file, cross-cutting, research needed): Decompose into sequential subagent dispatches with verification between each.

### Step 3: Execute Sub-Tasks
Work through the plan's sub-tasks in order:
- For parallelizable tasks, use multiple Agent calls in a single message
- For each sub-task, verify completion before moving to the next dependent task
- If a sub-task fails or hits an unexpected issue, STOP and report to the user rather than improvising a workaround

After each subagent returns, validate the report. See `subagent-validation.md` for the full protocol.

### Step 4: Verify Success
Check the plan's success criteria:
- Run tests if applicable
- Generate visualizations if the plan called for them
- Spot-check outputs against expected values

Report results to the user.

See `rules.md` for implementation guardrails.

After implementation completes, `/verify` is mandatory -- not optional. The `/wrapup` health check will flag sessions where `/implement` ran without `/verify`.
