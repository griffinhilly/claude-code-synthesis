# Plan Polishing Guide

## Iterative Refinement
Review the plan 2-3 additional times, each pass asking:
- Are there blunders, logical flaws, errors of omission, or sloppy thinking?
- Could any sub-task be split, reordered, or parallelized better?
- Are success criteria actually measurable? Would you know if they failed?
- Is any sub-task underspecified — would an implementation agent need to make judgment calls?

For complex plans (5+ sub-tasks or multi-session scope), do 3 passes minimum. Each pass should surface at least one change or explicitly state convergence. Don't inflate — if the plan is solid after 2 passes, stop.

## Dialectic Checkpoint
If the plan involves irreversible actions, multi-session scope, or architectural decisions, STOP and suggest:

> "This plan is significant enough for a premortem. Want me to run `/dialectic-review --premortem` on it before we proceed?"

If the plan involves choosing between approaches that survived the polish passes, suggest `--tradeoff` instead.

Don't skip this step for complex plans — the cost of a dialectic is small relative to the cost of implementing the wrong plan.

## Multi-Model Synthesis (for significant plans)
For plans that are complex, high-stakes, or architectural (not bug fixes or small features), suggest:

> "This plan is substantial enough to benefit from multi-model synthesis. Want me to output a self-contained prompt you can paste into ChatGPT/Gemini for a competing plan? I'll then synthesize the best of both."

If the user agrees:
1. Output a self-contained prompt that includes: objective, constraints, context, and asks for a full decomposed plan
2. Wait for the user to paste back the competing plan(s)
3. Analyze with intellectual honesty — what did the other model do better?
4. Produce a "best of all worlds" revision that integrates the strongest ideas from each

If the user declines, proceed normally. Never block on this step.

## Forcing Specificity
For each success criterion, ask: **"Can you describe a specific, concrete scenario where you'd know this is met?"** If you can't make it concrete, it's not measurable — rewrite it until you can.

Examples of the transformation:
- Vague: "The API should be fast" --> Concrete: "GET /users/123 returns in under 200ms with a cold cache on the staging server"
- Vague: "Error handling should be robust" --> Concrete: "When the upstream payment API returns a 503, the system retries twice with exponential backoff, then returns a user-facing error with a support ticket link"
- Vague: "The UI should be intuitive" --> Concrete: "A new user can complete the signup flow in under 60 seconds without clicking 'help'"

If a success criterion resists concreteness, it may be a symptom of unclear requirements — flag it for the user rather than proceeding with ambiguity.

## Argue the Opposite
Before finalizing, spend 30 seconds arguing against the plan. What's the strongest case for a completely different approach? If the counter-argument is weak, proceed. If it's strong, surface it.
