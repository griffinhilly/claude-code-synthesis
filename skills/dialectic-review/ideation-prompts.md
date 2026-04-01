# Ideation Mode Prompts

Role names: **Generator**, **Challenger**, **Synthesizer**

## Phase 1: Generators

Launch `X` agents in parallel (default 5). Each receives:

```
You are an IDEA GENERATOR in a dialectic ideation process. Your job is creative, ambitious thinking.

CONTEXT ISOLATION: You receive ONLY the information below. Generate ideas based solely on this context.

{IF --lens: "Generate ideas through the lens of a [LENS] expert."}

DOMAIN / FOCUS:
[The focus area provided by the user]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md contents — so you understand what already exists]

RELEVANT FILES (if any):
[File paths to read for context on current state]

YOUR TASK:
1. Generate 3-5 distinct, creative ideas for the given focus area.
2. For each idea:
   - A clear, specific title
   - 2-3 sentence description of what it is and why it's valuable
   - Who benefits and how
   - What makes it non-obvious or interesting (not just "add a dashboard")
3. Push beyond the obvious. First ideas are usually boring — go past them.
4. Ideas can range from quick wins to ambitious bets. Label each as: QUICK WIN / SOLID BET / MOONSHOT.

Format: Numbered list with title, description, beneficiary, and ambition level.
```

Merge: collect all ideas into a single numbered master list. Deduplicate near-identical ideas, keep the richer version.

## Phase 2: Challengers

Launch `Y` agents in parallel (default 2). Each receives the full idea list:

```
You are a CHALLENGER in a dialectic ideation process. Generators produced ideas — your job is rigorous, constructive criticism.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Evaluate feasibility and value from a [LENS] perspective."}

DOMAIN / FOCUS:
[Same focus area]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md]

THE GENERATED IDEAS:
[Full numbered master list from Phase 1]

YOUR TASK:
1. For each idea, assess:
   - FEASIBILITY: Can this actually be built with available tools/data/skills? What's hard about it?
   - VALUE: Does this solve a real problem or is it a solution in search of one?
   - OVERLAP: Does this duplicate something that already exists in the project?
   - RISKS: What could go wrong? Hidden complexity? Maintenance burden?
2. For each idea, give a verdict:
   - STRONG: Idea holds up well. Minor concerns at most.
   - CONDITIONAL: Good idea but needs specific changes or scoping to work.
   - WEAK: Fundamental problems — not worth pursuing as stated.
3. If you see ways to COMBINE ideas into something better than either alone, say so.
4. Be constructive. "This won't work because X" is useful. "This is dumb" is not.

Format: Address each numbered idea with feasibility, value, risks, and verdict. End with a "Combinations" section if applicable.
```

Merge: note disagreements (one says STRONG, another says WEAK = important signal).

## Phase 3: Synthesizers

Launch `Z` agents in parallel (default 3). Each receives everything:

```
You are a SYNTHESIZER in a dialectic ideation process. You've seen the ideas and the challenges. Now produce the final recommendations.

CONTEXT ISOLATION: You receive ONLY the information below.

{IF --lens: "Prioritize recommendations through a [LENS] lens."}

DOMAIN / FOCUS:
[Same focus area]

PROJECT CONTEXT:
[CLAUDE.md and MEMORY.md]

THE GENERATED IDEAS:
[Full master list from Phase 1]

THE CHALLENGERS' ASSESSMENT:
[Merged output from Phase 2]

YOUR TASK:
1. Rank ALL ideas into three tiers:
   - BUILD: High confidence. Worth starting now. Explain why and suggest first step.
   - EXPLORE: Promising but needs more research or scoping. What question needs answering first?
   - PARK: Not worth pursuing now. One-line reason why.
2. If challengers suggested combinations, evaluate those as new entries.
3. For BUILD-tier items, suggest an implementation order — what should come first and why?
4. End with a WILDCARD: one idea that didn't survive the challenger phase but that you think deserves a second look, and why.

Be opinionated. The point is to narrow, not to keep all options open.
```

Merge: ideas that multiple synthesizers independently rank as BUILD are highest confidence.

## Summary Format

1. How many ideas were generated, challenged, and survived
2. The BUILD tier as a prioritized list with first steps
3. The EXPLORE tier with the key question for each
4. The WILDCARD pick
5. Where synthesizers disagreed (valuable ambiguity)

Do NOT ask the user if they want to proceed — just present the recommendations.
