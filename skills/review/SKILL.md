---
name: review
description: Review completed work against success criteria and flag issues
user-invocable: true
disable-model-invocation: false
argument-hint: [what to review - file, feature, or recent work]
---

# Review

Evaluate completed work against its success criteria. Find problems before they compound.

## Input

What to review: `$ARGUMENTS`

If no arguments, review whatever was most recently implemented in the conversation.

## Process

### Step 1: Pre-check
- If `/verify` hasn't been run on the target, suggest running it first — /verify catches completeness issues, /review catches quality issues. Different concerns.
- Read relevant COMP files (CLAUDE.md for conventions, MEMORY.md for gotchas)
- Identify the success criteria (from /plan-task output, PLAN.md, or conversation)

### Step 2: Launch Review
Read @review-dimensions.md for what to check based on the type of work (code, data, writing).

Launch the review using a fresh-context subagent (use the `code-reviewer` agent persona for code). The reviewer should NOT share the implementer's assumptions.

### Step 3: Present Findings
Read @output-format.md for how to organize findings.

### Step 4: Escalation Check
- For significant reviews, consider suggesting `/dialectic-review` for adversarial depth
- If the review surfaces architectural concerns, suggest `/dialectic-review --premortem` before proceeding with fixes

## Rules
Read @rules.md for review rules and gotchas.
