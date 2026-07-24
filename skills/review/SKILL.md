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
Read `~/.claude/skills/review/review-dimensions.md` for what to check based on the type of work (code, data, writing).

Launch the review using a fresh-context subagent (use the `code-reviewer` agent persona for code). Apply the strengthened review discipline (per CLAUDE.md "Fresh eyes for review"):

1. **Spec-blind:** Do NOT include the original spec, plan, or coder context in the reviewer's prompt. Pass the diff (or the artifact) and have the reviewer reason backward. The reviewer's lack of spec-knowledge is a feature — it surfaces unstated assumptions the spec hid.
2. **Multiple uncorrelated passes:** Launch the reviewer 2-3 times in parallel with the same prompt. Union their findings. If the same model produces overlapping findings, that's signal; if they find different things, the union is the value.
3. **Treat-as-adversary:** Frame the reviewer's findings as questions about the work, not defects to auto-fix. Pass each finding through "is this actually wrong, or is it the reviewer pattern-matching without context?" Keep the credible ones; reject the rest with reasoning.

### Step 3: Present Findings
Read `~/.claude/skills/review/output-format.md` for how to organize findings.

### Step 4: Escalation Check
- For significant reviews, consider suggesting `/dialectic-review` for adversarial depth
- If the review surfaces architectural concerns, suggest `/dialectic-review --premortem` before proceeding with fixes

## Rules
Read `~/.claude/skills/review/rules.md` for review rules and gotchas.
