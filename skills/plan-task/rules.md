# Planning Rules

## Hard Rules
- Do NOT begin implementation during planning
- Do NOT skip steps — even if the task seems simple
- Use neutral framing — don't bias toward a specific solution before evaluating options
- Planning tokens are cheaper than implementation tokens — don't rush this phase
- The plan should trivially fit in a context window. If it's growing past 2000 lines, decompose into phases instead

## Gotchas
- Plans that skip success criteria produce unmeasurable outcomes — you won't know if you succeeded
- Plans that don't identify risks hit them during implementation when they're expensive to handle
- Sub-tasks without clear boundaries cause scope disputes during implementation
- "Research + Implement" as a single sub-task always produces worse results than separating them
- Skipping the dialectic checkpoint for complex plans is the #1 source of "we should have thought of that"
- The user tends toward ambitious scope — push back with smaller increments per the Scope Discipline guidelines
- If the plan requires information you don't have, flag it as a research dependency rather than guessing
- Multi-model synthesis is most valuable for architectural decisions and least valuable for routine work — calibrate your suggestion accordingly
