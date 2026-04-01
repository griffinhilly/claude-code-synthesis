---
name: comp
description: Create or update all 4 COMP files (CLAUDE.md, ORIENT.md, MEMORY.md, PLAN.md) for a directory
user-invocable: true
disable-model-invocation: false
argument-hint: [directory path]
---

# COMP Update

Create or update all 4 COMP files for a project directory.

## Input

Directory to update: `$ARGUMENTS`

If no arguments, use the current working directory. If ambiguous, ask.

## The 4 Files

| File | Purpose | Audience | Change Frequency |
|------|---------|----------|-----------------|
| **C**LAUDE.md | Behavioral contract — how the AI should work here | Agent | Rare — only when conventions or architecture change |
| **O**RIENT.md | Orientation — what this project is, how to work in it | Human | When project shape changes |
| **M**EMORY.md | Accumulated knowledge — decisions, gotchas, cross-session context | Agent + Human | Most sessions |
| **P**LAN.md | Direction — roadmap, phases, progress, next steps (with `## Current State` at top) | Human + Agent | Most sessions |

## Process

### Step 1: Read Existing Files
Read all 4 COMP files if they exist. Also read the directory listing (ls).

### Step 2: Determine What Needs Updating
Based on the current session's work and the current state of the directory:
- Which files exist vs need creation?
- Which existing files are stale or incomplete?
- What new information needs recording?

### Step 3: Create or Update Each File

**PLAN.md** — If creating: project roadmap, current phase, next steps, and a `## Current State` section at the top with active work, blockers, and what to do next session. If updating: mark progress, adjust priorities, refresh the Current State section.

**MEMORY.md** — If creating: key decisions, known gotchas, cross-session context. If updating: add new decisions/gotchas. MEMORY is for durable knowledge that accumulates — don't put ephemeral session state here (that goes in PLAN.md's Current State section).

**ORIENT.md** — If creating: one-paragraph project description, current codebase shape (mental model, not file index), most common operations, known weirdness, key links. If updating: refresh to reflect new capabilities or structural changes. Written for the human — answer "what do I need to know to work on this after two weeks away?"

**CLAUDE.md** — If creating: project overview, key technical details, conventions, situational guides. If updating: add new conventions, update schema. Rare — don't add session-specific detail here.

### Step 4: Summary
Report what was created/updated.

## Rules
- Always READ existing files before editing — never overwrite blindly
- Keep each file focused on its purpose — don't duplicate across files
- CLAUDE.md is the behavioral contract (for the agent); ORIENT.md is orientation (for the human)
- MEMORY.md is durable cross-session knowledge; PLAN.md's Current State section is the session-scoped snapshot
- For sub-projects, reference the parent project's COMP files where relevant
