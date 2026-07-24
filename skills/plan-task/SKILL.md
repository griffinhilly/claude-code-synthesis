---
name: plan-task
description: Plan a new task/project using structured decomposition before any implementation
user-invocable: true
disable-model-invocation: false
argument-hint: [--quiz-me] <task description>
---

# Plan Task

Structured planning mode. NO implementation until the plan is approved.

## Input

The task to plan is: `$ARGUMENTS`

Parse flags from `$ARGUMENTS`:
- `--quiz-me` — Run Step 1.5 (adversarial interrogation) before producing the plan. Use for new skills, new automations, fuzzy specs, or any task where the user's implicit knowledge is likely to have gaps.

If no arguments provided, ask the user what they want to plan.

If the task is genuinely trivial (< 2 minutes of work), say so and ask if the user wants to skip planning.

## Process

### Step 1: Clarify the Objective
State the objective in one clear sentence. If ambiguous, ask the user to clarify before proceeding.

### Step 1.5: Quiz Me (only if `--quiz-me` set)
Before decomposing or proposing a plan, *interrogate the user*. Generate 5-10 clarifying questions designed to surface hidden assumptions, edge cases, and priorities. The goal is to find every gap in the user's *implicit* knowledge before the plan locks them in.

Question shapes to draw from:
- **Edge cases:** "What happens if input X is empty / malformed / missing / duplicated?"
- **Priority order:** "If A and B conflict, which wins? Why?"
- **Failure mode:** "What does 'this didn't work' look like? What's the worst-case bad outcome?"
- **Boundary:** "Where does this responsibility end? What's explicitly out of scope?"
- **Reversibility:** "If this turns out to be wrong, what's the unwinding cost?"
- **Frequency:** "How often will this run? Once, weekly, every commit?"
- **Audience:** "Who reads/runs this output? What do they need from it?"
- **Counterexample:** "Show me an input where this design would fail."

Present the questions as a numbered list. Wait for the user's answers. Capture answers verbatim in the plan output as a "Stated assumptions" section — these become the parameter contract the rest of the plan is built on.

Per the doctrinal scaffolding: the quiz inverts the standard agent posture (agent surfaces assumptions for user to correct) into adversarial interrogation (agent interrogates user to surface *their* assumptions). Particularly load-bearing on complex frameworks where the user's own accumulated notes flag underspecification as a recurring failure mode.

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
Read @polishing-guide.md for the iterative refinement process, argue-the-opposite check, and multi-model synthesis option.

### Step 6.5: Scope Gate (MANDATORY — do not skip)
Read @scope-gate.md and execute it. This is a deterministic checkpoint that fires between polishing and presenting; it replaces the soft dialectic-checkpoint that used to live in `polishing-guide.md`. Its purpose is to force an explicit decision about dialectic-review when the plan's estimated scope crosses thresholds that correlate with "decisions worth stress-testing." If you read this far without running the gate, stop and run it now.

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
