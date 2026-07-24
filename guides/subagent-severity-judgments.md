# Subagent Severity Judgments — Cross-Check Before Acting

Subagent severity ratings ("ship-blocker," "critical," "blocker," "P0," "must-fix") should be treated as hypotheses, not facts. Cross-check before prioritizing work based on them. This applies to any subagent type — Explore, Researcher, Reviewer, code-reviewer.

**Why:** In one claude-code-synthesis session, an Explore agent flagged 2 "ship-blockers." Both were wrong:
1. A wrapper-path reference "breaking on clone" — based on a false assumption that visitors use the repo directly without running the setup/deploy script. The absolute skill-path references were correct for the deploy model.
2. Inline phase prompts in a skill needing extraction for "architectural consistency" — cosmetic, not functional. Inline phases work fine.

The same agent's polish-tier findings were well-calibrated and actionable. The pattern: subagents inflate severity when they imagine a failure scenario without verifying the project's actual usage model.

**How to apply:** When any subagent returns top-severity findings, spend 60 seconds verifying the premise before treating it as urgent. Ask: does the failure scenario the agent imagined actually match how the project is used? Is the imagined caller real? Is the imagined data shape real?

For polish/nice-to-have findings, trust the subagent's judgment more — those are closer to its strength (pattern-matching across files). The miscalibration is concentrated at the top of the severity scale where the agent is making a stakes claim, not a pattern claim.

**Reinforcement (client deliverable review, later session):** the failure mode also hits *factual* claims, not just severity. A calibration agent confidently asserted a flagship chart was "left-anchored [FORM] — rebuild it" (it was actually a center butterfly chart) and that another chart was "a matrix" (it was actually a horizontal bar chart). Both were [HIGH]-confidence and both were wrong — caught by looking at the actual reference image for 30 seconds. **Verify high-confidence agent claims against the ground-truth artifact (the reference, the data, the real caller), not against the agent's own confidence.** Auto-applying that claim would have broken a correct, locked chart.
