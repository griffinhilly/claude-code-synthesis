# Dialectic / Multi-Lens Ideation — Adoption & Virality Frame

When running multi-agent ideation on product-design questions (`/dialectic-review`, `/plan-task` on a user-facing feature, or single-agent product brainstorming), the agents collectively under-weight adoption/virality concerns unless the prompt explicitly names them. They default to optimizing for model calibration, pedagogical rigor, or UX correctness — all good frames — but will collectively land on an onboarding experience that's too heavy for a curious first-time visitor.

**Why:** In one redesign of an interactive learning tool, a 4-lens dialectic (psychometrics / pedagogy / UX / skeptic) converged on a plan where a new visitor would take a 24-question adaptive assessment BEFORE seeing the product. None of the agents flagged "a stranger on the internet will not sit through 24 questions for an unknown tool." The user had to intervene mid-plan to reframe it as virality-vs-utility, which immediately demoted the assessment to an opt-in button.

Each lens has its own default success metric. Psychometrics optimizes information gain. Pedagogy optimizes mastery trajectory. UX optimizes cognitive load during use. Skeptic optimizes code size. **None of these default metrics include "will a stranger who just clicked a shared link stick around for 30 seconds?"** — and without explicit framing, that question gets dropped between the lenses.

**How to apply:** When running `/dialectic-review`, `/plan-task`, or any multi-agent ideation on a product-facing feature, inject one or more of these into the agent prompts:

1. **Name the adoption stage explicitly.** "This product is pre-product-market-fit. The goal is to get curious first-time visitors to stick around for 60 seconds, not to serve power users."

2. **Include a 'bounce-rate' lens as one of the agents**, or add it as an explicit criterion the referee must weigh. Something like: *"Agent 5: The Skeptical Visitor — you just clicked a link someone shared. What makes you bounce in the first 10 seconds?"*

3. **Test the emerging plan against a 'stranger from a shared link' persona** before committing. If the stranger has to commit >30 seconds of effort before seeing value, the plan needs a lighter entry ramp.

4. **Distinguish utility from virality in the framing.** The most useful feature and the most viral feature are usually different. Both matter, but they serve different stages of the funnel. Name which the plan is optimizing and where it's willing to trade off.

This applies to any product-design dialectic. The failure mode is easy to miss because the individual agent outputs all sound reasonable; the problem only surfaces when you imagine an uncommitted first-time user hitting the flow.
