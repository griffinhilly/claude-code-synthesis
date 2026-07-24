# Pre-Commit Decision Rule — Structural Audit

When pre-committing a decision rule that will mechanically pick an action (downgrade / keep / hedge / whatever) based on a forthcoming empirical result, add one step before running the experiment: a 10-minute fresh-context agent call that audits the rule's *structure* for motivated-reasoning risk. Not the science. The rule.

**Why:** One research-writing session ran a pre-committed decision rule on an empirical null (≥15% → downgrade; 7–15% → intermediate hedge; ≤7% → light disclosure). The outcome was 14.0% with 95% CI [9.5%, 19.0%] — middle bin on point estimate, CI straddling the boundary between two verdict bins. The rule had a reversal condition saying "middle-bin with wide CI → default verdict, do NOT re-open the upstream debate." The rule defaulted to that verdict regardless of whether the CI extended into the downgrade bin or not. That default may have been the right call, but a session reviewer flagged it: "the rule as written makes the default verdict nearly unfalsifiable — any CI in the middle range defaults there regardless of direction." That's the failure mode this check prevents.

**How to apply:** Before the user approves a pre-committed rule, spawn one short subagent (a lighter model is fine, this is a structural check not a judgment call) with only:
- The rule as written
- A description of the expected experimental output format

Ask the subagent four specific questions:
1. For each verdict bin, describe an empirical outcome that would land there.
2. Is any verdict bin structurally easier to land on than the others (e.g., bigger width, catches ties, catches ambiguity)?
3. If the experiment produces a result near a boundary, what does the rule do? Is the tie-breaker stated, or does the rule default to one side without saying so?
4. If the user had the opposite prior from what they currently have, would this rule still look fair?

**When to skip:** Trivial rules (two bins, clean threshold, no edge cases) don't need it. The check earns its place when the rule has bins, reversal conditions, or any "if ambiguous, default to X" language — those are the structural shapes that hide motivated-reasoning risk.

## Companion check: lexical ambiguity audit

The structural audit above checks whether a rule can be gamed; this check hunts registered WORDS that admit two readings — each one costs a full decision cycle (or worse, a silent pick) when the data arrives. **Reinforcement:** a later research-writing project ratified its pre-registration through a structural checklist and still hit four lexical fights this class would have caught pre-data:

1. **Undefined operationalizations.** "Lagged income" — initial/period-start vs strict t−1. The two readings flipped a verdict (NULL vs FINDING). Test: for every registered variable, can two competent analysts build different columns from the words? If yes, pin it.
2. **Pre-named lists that may be partially unavailable.** "≤2-covariate spec (pre-named: X + Y)" — what happens when X's dataset is unacquired? The ambiguity licensed skipping a passing fallback rung. Test: for every pre-named input, state the rule under partial availability (available-subset vs not-constructible).
3. **Scale/estimand-silent inference clauses.** The inference stack (a "primary p-value" clause) was scale-silent while the verdict template named a hazard ratio; when the scales diverged, a "finding" appeared on the unregistered scale. Test: does every registered test name BOTH its machinery and the scale/quantity the verdict reads from?
4. **Disjunctive verdict templates.** A NULL template with "A or B" conditions fired half-true (one clause true, the other false) and needed a referee to rule SPLIT. Test: for each multi-clause template, describe an outcome satisfying only one clause — is the intended verdict stated?

Run this as part of the same fresh-context audit call (one agent, both checklists). For each hit, either fix the wording pre-ratification or add an explicit tie-break — never leave "we'll interpret it when we see the data."

**Integration with existing workflow:** Belongs as a sub-step of `/plan-task` scope gate when the plan includes a pre-committed decision rule on forthcoming data.

**Adjacent pattern:** a "plan persistence" doctrine — write down durable plan artifacts so future sessions don't lose the why. This guide is the specific case of that pattern where the plan artifact includes a decision rule — the rule needs its own structural audit, not just the plan's scope review.
