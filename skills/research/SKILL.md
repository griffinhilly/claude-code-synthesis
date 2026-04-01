---
name: research
description: Launch a research-only agent that investigates a topic and returns findings (no implementation)
user-invocable: true
disable-model-invocation: false
argument-hint: <research question or topic>
---

# Research Agent

Launch a research-only investigation. This agent gathers information but does NOT implement anything.

## Input

Research topic: `$ARGUMENTS`

If no arguments, ask the user what to research.

## Process

### Step 1: Scope the Research
Before launching agents, determine:
- What specifically needs to be answered?
- What sources are relevant? (codebase, web, specific files, databases)
- What does the user need to decide based on this research?

### Step 2: Launch Research Agent(s)
Use the Agent tool with `subagent_type=Explore` for codebase research, or `subagent_type=general-purpose` for broader research.

The agent prompt should:
1. State the research question clearly
2. List specific things to look for
3. Specify the output format (findings, options, recommendations)
4. Explicitly instruct: "Do NOT make any changes. Read-only research."

For broad topics, launch multiple agents in parallel targeting different aspects.

### Step 3: Synthesize
After agents return, synthesize findings into:
1. **Key Facts** — what we now know
2. **Options** — if the research was to inform a decision, list options with tradeoffs
3. **Recommendation** — if appropriate, suggest a path forward
4. **Unknowns** — what we still don't know

### Rules
- Research agents must NOT edit files, write code, or make changes
- Present findings neutrally — don't bias toward a conclusion
- If research reveals the task is more complex than expected, say so
- Record important findings in project MEMORY.md if they'll be needed later
