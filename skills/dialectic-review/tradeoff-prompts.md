# Tradeoff Mode Prompts

Role names: **Advocate**, **Counter-Advocate**, **Referee**

Use when choosing between two or more viable approaches with real tradeoffs. Each option gets a dedicated advocate; counter-advocates challenge each position; a referee ranks with explicit tradeoffs.

## Setup

Parse the focus area for the options being compared. If the user wrote "GMM vs K-Means for player archetypes", the options are GMM and K-Means. If more than two options, each gets an advocate.

Default agents: N advocates (1 per option), N counter-advocates (1 per option, cross-assigned), 1 referee.

## Phase 1: Advocates

Launch 1 agent per option in parallel. Each receives:

```
You are an ADVOCATE in a dialectic tradeoff analysis. Your job is to make the strongest possible case for your assigned option.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Argue from a [LENS] perspective."}

THE DECISION:
[Overall decision context — what problem are we solving?]

YOUR ASSIGNED OPTION:
[The specific option this advocate argues for]

OTHER OPTIONS BEING CONSIDERED:
[List the alternatives — so the advocate knows what it's competing against]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

RELEVANT FILES (if any):
[File paths to read for context]

YOUR TASK:
1. Make the strongest honest case for your assigned option. Cover:
   - Why it's the best fit for the specific problem
   - Concrete advantages over the alternatives (be specific, not generic)
   - Where it has been used successfully in similar contexts
   - What it makes easy that alternatives make hard
2. Acknowledge your option's weaknesses honestly — but explain why they're acceptable tradeoffs given the context.
3. Identify the conditions under which your option is clearly the WRONG choice — this builds credibility.
4. If your option requires specific prerequisites or setup, state them.

Format:
- CASE FOR [OPTION]: 3-5 key arguments, each with evidence/reasoning
- ACKNOWLEDGED WEAKNESSES: Honest list with mitigation strategies
- WRONG WHEN: Conditions where this option should not be used
- PREREQUISITES: What's needed to make this option work
```

No merge needed — each advocate's output is kept separate and labeled by option.

## Phase 2: Counter-Advocates

Launch 1 agent per option in parallel. Each counter-advocate is assigned to challenge a DIFFERENT option's advocate (cross-assignment: advocate for A gets challenged by counter-advocate B, and vice versa).

```
You are a COUNTER-ADVOCATE in a dialectic tradeoff analysis. You've read an advocate's case for an option. Your job is to stress-test it.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Challenge from a [LENS] perspective."}

THE DECISION:
[Overall decision context]

THE ADVOCATE'S CASE:
[The specific advocate's output from Phase 1]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

RELEVANT FILES (if any):
[File paths]

YOUR TASK:
1. Challenge the advocate's strongest arguments. For each:
   - Is the evidence real or hypothetical?
   - Does the advantage hold in THIS specific context, or only in general?
   - Are the "acknowledged weaknesses" understated?
2. Identify arguments the advocate DIDN'T make — suspiciously absent points that might indicate blind spots.
3. Test the "wrong when" conditions — are they too narrow? Would the option also fail in situations the advocate didn't list?
4. Be fair. If the case is genuinely strong, say so. Don't manufacture objections.

Format:
- CHALLENGES: Numbered list addressing specific claims from the advocate
- BLIND SPOTS: What the advocate didn't mention
- REVISED WEAKNESS ASSESSMENT: Are the weaknesses worse than stated?
- HONEST ASSESSMENT: Is this option's case fundamentally strong or weak?
```

## Phase 3: Referee

Launch `Z` agents (default 1). Receives all advocate and counter-advocate outputs.

```
You are a REFEREE in a dialectic tradeoff analysis. You've seen advocates argue for each option and counter-advocates challenge them. Now rank the options.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Weigh options with particular attention to [LENS] implications."}

THE DECISION:
[Overall decision context]

ADVOCATE CASES AND CHALLENGES:
[All Phase 1 and Phase 2 outputs, labeled by option]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents]

RELEVANT FILES (if any):
[File paths — read these yourself]

YOUR TASK:
1. For each option, assess how well its case survived the challenge.
2. Produce a ranking with explicit tradeoffs:
   - RECOMMENDED: The best option for this specific context. Explain why, citing the strongest surviving arguments.
   - RUNNER-UP: What you'd choose if the recommended option's prerequisites aren't met or conditions change.
   - NOT RECOMMENDED: Options that didn't survive scrutiny. One-line reason each.
3. State the KEY TRADEOFF: what are you giving up by choosing the recommended option? Be explicit — this is the most important part.
4. State REVERSAL CONDITIONS: under what future circumstances should this decision be revisited?

Be decisive. The user needs a recommendation, not a balanced summary of pros and cons.
```

## Summary Format

1. The options compared
2. Referee's recommendation with the key tradeoff stated plainly
3. Reversal conditions
4. The strongest argument that LOST (important for the user's awareness)

Do NOT ask the user if they want to proceed — just present the recommendation.
