---
name: plan-task
description: Plan a new task/project using structured decomposition before any implementation
user-invocable: true
disable-model-invocation: false
argument-hint: <task description>
---

# Plan Task

Structured planning mode. NO implementation until the plan is approved.

## Input

The task to plan is: `$ARGUMENTS`

If no arguments provided, ask the user what they want to plan.

If the task is genuinely trivial (< 2 minutes of work), say so and ask if the user wants to skip planning.

## Process

### Step 1: Clarify the Objective
State the objective in one clear sentence. If ambiguous, ask the user to clarify before proceeding.

### Step 2: Define Success
List concrete success criteria. Use specific, measurable outcomes where possible.
- What does "done" look like?
- How will we verify success? (tests, visualizations, spot-checks)
- Are there examples of what good output looks like?

If the user hasn't provided success criteria, propose some and ask for confirmation.

### Step 3: Research (if needed)
If the task involves unfamiliar territory, launch an Explore agent to gather context:
- Read relevant COMP files (CLAUDE.md, PLAN.md, MEMORY.md) for the project
- Identify existing code, data, or patterns that inform the approach
- Note constraints, gotchas, or prior decisions from MEMORY.md

### Step 4: Decompose
Break the task into sub-tasks. Read @decomposition-guide.md for the sub-task template and table format.

### Step 5: Identify Risks
Read @risk-checklist.md for the risk identification framework.

### Step 6: Polish the Plan
Read @polishing-guide.md for the iterative refinement process, dialectic checkpoint, and multi-model synthesis option.

### Step 7: Present the Plan
Summarize the full plan in a clear format:
1. Objective
2. Success criteria
3. Sub-task table with sequencing
4. Risks and mitigations
5. Recommended execution order
6. Polish passes completed (and key changes from each)

Ask the user: "Does this plan look right? Adjust anything before I start?"

## Rules
Read @rules.md for planning rules and gotchas.
