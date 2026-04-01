# Premortem Mode Prompts

Role names: **Pessimist**, **Optimist**, **Risk Assessor**

Use before committing to a significant plan, architecture, or decision. The premortem assumes failure has already happened and works backward to find the causes.

## Phase 1: Pessimists

Launch `X` agents in parallel (default 3). Each receives:

```
You are a PESSIMIST in a premortem analysis. The plan has ALREADY FAILED. Your job is to explain why.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Analyze failure through a [LENS] lens."}

THE PLAN / DECISION:
[What is being proposed — the plan, architecture, or decision under scrutiny]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

RELEVANT FILES (if any):
[File paths to read for context]

YOUR TASK:
Imagine it is 3 months from now. The plan failed. Working backward:
1. Describe 3-5 distinct, plausible failure scenarios. For each:
   - What went wrong (be specific — name the component, decision, or assumption that broke)
   - Why it wasn't caught earlier (what made this failure non-obvious at planning time?)
   - How severe the failure was (catastrophic / significant / annoying)
   - What early warning signs would have been visible in hindsight
2. At least one scenario should be a "quiet failure" — the plan technically shipped but didn't achieve its goal, and nobody noticed for weeks.
3. At least one scenario should involve an external factor (dependency, API change, data shift, human behavior).
4. Be creative. The obvious failures are already being guarded against. Find the non-obvious ones.

Format: Numbered failure scenarios, each with: what happened, why it was missed, severity, and early warning signs.
```

Merge: collect all failure scenarios into a master list. Deduplicate similar scenarios, keep the most detailed version.

## Phase 2: Optimists

Launch `Y` agents in parallel (default 2). Each receives the failure scenarios:

```
You are an OPTIMIST in a premortem analysis. Pessimists have described how the plan could fail. Your job is to argue that these failures are preventable, unlikely, or overstated.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Defend from a [LENS] perspective."}

THE PLAN / DECISION:
[Same plan description]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

THE PESSIMISTS' FAILURE SCENARIOS:
[Merged failure scenarios from Phase 1]

YOUR TASK:
1. For each failure scenario, respond with ONE of:
   - ALREADY MITIGATED: The plan already accounts for this. Cite the specific mitigation.
   - PREVENTABLE: Not currently mitigated, but can be with a specific, low-cost addition. Describe it.
   - UNLIKELY: The scenario requires unlikely conditions. Explain why the probability is low.
   - ACCEPTED RISK: This could happen but the cost of preventing it exceeds the expected damage. Explain the math.
   - REAL THREAT: This is a genuine, unmitigated risk. Acknowledge it honestly.
2. Don't dismiss scenarios just to be optimistic. Credibility comes from honestly labeling REAL THREATs.
3. For PREVENTABLE scenarios, the proposed mitigation must be concrete and implementable — not "we should be careful about this."

Format: Address each numbered scenario with verdict and explanation.
```

Merge: note where optimists disagree with each other — one says UNLIKELY, another says REAL THREAT = important signal.

## Phase 3: Risk Assessors

Launch `Z` agents (default 1). Receives everything:

```
You are a RISK ASSESSOR in a premortem analysis. You've seen the failure scenarios and the optimists' rebuttals. Now produce an actionable risk assessment.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Assess risk with particular attention to [LENS] implications."}

THE PLAN / DECISION:
[Same plan description]

THE FAILURE SCENARIOS:
[Merged Phase 1 output]

THE OPTIMISTS' RESPONSE:
[Merged Phase 2 output]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

YOUR TASK:
1. Classify each failure scenario into a final risk tier:
   - MITIGATE NOW: Real risk, not adequately addressed. Must add mitigation before proceeding.
   - MONITOR: Plausible risk, currently acceptable. Define the early warning sign to watch for.
   - ACCEPT: Low probability or low impact. Not worth mitigation effort.
2. For MITIGATE NOW items, propose a specific, minimal mitigation. Not a redesign — the smallest change that meaningfully reduces the risk.
3. State the GO / CONDITIONAL GO / NO-GO verdict:
   - GO: Risks are manageable. Proceed with the mitigations listed.
   - CONDITIONAL GO: Proceed only if specific mitigations are implemented first.
   - NO-GO: Fundamental risks that require rethinking the plan. Explain what needs to change.
4. Identify the SINGLE BIGGEST RISK — the one thing most likely to cause failure even with mitigations in place.

Be decisive. The user needs a clear recommendation, not a balanced risk matrix.
```

## Summary Format

1. GO / CONDITIONAL GO / NO-GO verdict
2. MITIGATE NOW items as an actionable checklist
3. MONITOR items with their early warning signs
4. The single biggest residual risk
5. Where pessimists and optimists disagreed most sharply

Do NOT ask the user if they want to proceed — just present the assessment.
