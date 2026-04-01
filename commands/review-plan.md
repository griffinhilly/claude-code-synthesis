# /review-plan — Plan Review

*v1.1 — Stress-test a plan with structured expert critique, best-practice research, and optional fresh-context subagent review*

Stress-test a plan with structured expert critique, web research on best practices, and a revised version if needed. Use after developing a plan, or on any plan file. Catches blind spots, missing steps, and wishful thinking.

## Instructions

### Step 0: Pre-checks

Parse `$ARGUMENTS` for flags. **If `$ARGUMENTS` is `help`, print the table below and stop.**

| Flag | Syntax | Default | Purpose |
|------|--------|---------|---------|
| Help | `help` | — | Show this options table and stop |
| File path | `file:path` | Auto-detect | Explicit plan location |
| Expert role | `role:"..."` | Auto-detect | Override persona |
| Focus area | `focus:dimension` | All dimensions | Weight one dimension (e.g. `focus:feasibility`) |
| Depth | `depth:quick/standard/deep` | `standard` | Web research intensity |
| Quick | `quick` | Off | Shorthand for `depth:quick` |
| Dry run | `dryrun` | Off | Show role + research plan only |

### Step 1: Locate and Read the Plan

Three-tier priority:
1. **Explicit file** — `file:path/to/plan.md` argument
2. **Plan-mode file** — most recent file in `~/.claude/plans/`
3. **Conversation history** — scan the current session for the plan

If no plan found:
> "No plan found. Usage: `/review-plan` (after plan mode) or `/review-plan file:path/to/plan.md`"

### Step 2: Assign Expert Role

Infer the domain from plan content:

| Domain signals | Assigned role |
|---------------|---------------|
| skill, command, agent, MCP, Claude Code | AI engineering and skill design specialist |
| data, analysis, pipeline, ML, model, notebook | Data science and ML engineering specialist |
| philosophy, ethics, agency, article, writing | Academic writing and philosophical argument specialist |
| data science, statistics, machine learning | Data science and statistical modeling specialist |
| project management, tracker, workflow | Operations and project management specialist |
| Default (no strong signal) | Strategic planning and implementation specialist |

If `role:"..."` is provided, use that instead.

**Announce:** "**Reviewing as:** Meticulous [role]. (Override with `role:"your role"` if this doesn't fit.)"

### Step 3: Research Best Practices

Extract the plan's primary domain and approach. Build web search queries:
- Query A: "[approach] best practices [year]"
- Query B: "[domain] common pitfalls"
- Query C (deep only): "[specific methodology] implementation guide"

| Depth | Web searches |
|-------|-------------|
| `quick` | 0 — skip entirely |
| `standard` | 2 (queries A + B) |
| `deep` | 3-4 (all queries) |

Distill into 3-5 key principles relevant to this plan.

### Step 4: Structured Review

**Why fresh-context review matters:** If you wrote or helped develop the plan, you carry planner bias — you're more likely to rationalize gaps than catch them. A fresh-context reviewer sees the plan cold, the way a colleague or referee would.

**Fresh-context review (preferred):**
Launch a subagent to perform the critique. This avoids the bias of reviewing your own plan.

Use the Agent tool with a prompt containing:
- The full plan text
- The 6 review dimensions listed below
- The best practices distilled from Step 3
- Instructions to return findings in Red/Yellow/Green format (see classification below)

If the subagent returns results, incorporate them into the output in Step 5.

**Inline review (fallback):**
If subagent dispatch isn't available or fails, perform the review inline using the critic stance below.

**CRITIC STANCE:**
> You are now the critic, not the planner. Do not rationalize. Your job is to find what's missing, what will break, and what's wishful thinking.

Review against 6 dimensions:

**1. Pre-mortem** — "It's 3 months later and this plan failed. What were the top 3 causes?"

**2. Completeness** — What's missing that a domain expert would expect?

**3. Feasibility** — Are there steps that depend on unconfirmed resources or approvals?

**4. Best-practice alignment** — How does this compare to standards from Step 3?

**5. Sequencing** — Are there hidden blockers? Would reordering reduce risk?

**6. Specificity** — Could someone unfamiliar execute each step?

**Classify findings:**
- **Red** — Critical. Will likely cause failure if unaddressed.
- **Yellow** — Important. Creates risk but plan can proceed.
- **Green** — Minor. Nice-to-have improvement.

### Step 5: Generate Output

```
PLAN REVIEW — [Plan Title]

Reviewing as: Meticulous [role]
Plan source: [file / plan mode / conversation]
Depth: [quick / standard / deep]

BEST PRACTICES CONTEXT
[3-5 key principles from research]

STRENGTHS
1. [Label] — [Explanation]

WEAKNESSES & GAPS
[Red] [Label] — [Issue] → Fix: [Recommendation]
[Yellow] [Label] — [Issue] → Fix: [Recommendation]
[Green] [Label] — [Issue] → Fix: [Recommendation]

VERDICT
APPROVE — [Rationale]
  OR
REVISE — [Rationale]. See revised plan below.

REVISED PLAN (only if REVISE)
[Full revised plan with [CHANGED] and [NEW] markers]
```

### Step 6: Iteration Gate

Ask: "Apply these revisions? Or provide feedback to refine further."

## Examples

```
/review-plan
/review-plan file:~/my-project/PLAN.md
/review-plan quick
/review-plan depth:deep focus:feasibility
/review-plan role:"data science specialist" file:~/my-project/PLAN.md
```
