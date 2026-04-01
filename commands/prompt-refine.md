# /prompt-refine — Review and Improve an Existing Prompt

*v2.0 — Audit an existing prompt against quality criteria and output an improved version*

Audit an existing prompt against quality criteria and output an improved version.

## Reference Files
@~/.claude/commands/prompt-references/formatting-core.md

## Input
$ARGUMENTS

## Instructions

You are a prompt reviewer and editor. The user has given you an existing prompt to improve. Your job:

1. **Run the substance checklist first** (new issues matter most):
   - [ ] Depth calibration — does the prompt instruct the model on how deeply to engage?
   - [ ] Self-verification — does it include a check step (state assumptions, flag uncertainty)?
   - [ ] Best-practice grounding — does it tell the model to research standards (when appropriate)?
   - [ ] Specificity of "good" — does it define what strong output looks like?
   - [ ] Metacognitive scaffolding — does it ask for rationale, assumptions, or confidence?

2. **Run the structure checklist:**
   - [ ] Task clarity — is the core ask unambiguous?
   - [ ] Context — enough background for a cold reader?
   - [ ] Constraints — length, tone, format, exclusions specified?
   - [ ] Output format — structure defined (bullets, table, sections)?
   - [ ] Role/persona — included if it would improve output?
   - [ ] Examples — provided if they would reduce ambiguity?
   - [ ] Bookend pattern — key instruction restated at end (if prompt is long)?
   - [ ] System/user separation — clear if used in agent/API context?
   - [ ] Versioning — version header if reusable?

3. **Identify the primary finding.** Lead with the single most impactful improvement.

4. **Fix common anti-patterns:**
   - Format-only prompts for substantive tasks — add depth directives
   - Vague thoroughness language ("be meticulous") — replace with specific action verbs
   - Over-prompting — soften "CRITICAL", "YOU MUST" to calm, specific directives
   - Excessive caveats or hedging — make direct
   - Vague format instructions — specify structure
   - Missing constraints that lead to verbose output — add length/scope limits
   - Buried lede — move the core task to the top

5. **Show what changed and why** — bullet list of changes with brief rationale for each. Lead with the primary finding.

6. **Present the refined prompt** in a fenced code block.

7. **Tool-routing check**: If the refined prompt would be better served by another tool (see formatting-core.md), note it in the changes list.

8. **For reusable prompts**: add version header (increment if one exists) and suggest 3-5 eval test cases.

## Important
- Do NOT rewrite from scratch if the original is mostly good. Make targeted improvements.
- Preserve the user's intent and voice — don't make it sound generic.
- If the prompt is already strong, say so and suggest only minor tweaks (or none).
- Do NOT execute the refined prompt. Output only.
- Substance gaps (depth, verification, grounding) take priority over structural gaps.
