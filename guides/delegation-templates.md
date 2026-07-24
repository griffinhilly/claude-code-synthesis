# Delegation Templates

When the orchestrator decides to delegate (rather than handle directly or route to MCP), use these templates. Each defines an agent type with a prompt structure, constraints, and report format.

## Structural Discipline (applies to all agents)

Every subagent prompt includes these three mechanisms. They replace verbose anti-rationalization rules with environmental enforcement:

1. **Mandatory report format.** Empty fields and missing status lines are visible signals. The orchestrator validates the report before accepting.
2. **Assumed verification.** Every prompt includes: "Your output will be reviewed by a separate agent." Knowing you'll be checked changes behavior more than rules about not rationalizing.
3. **Escalation as safe default.** BLOCKED is always better than wrong. Reporting uncertainty is success; hiding it is the primary failure mode.

## Dispatch Pitfalls

- **Many small > few large for bulk work.** For bulk content generation (batch topic generation, batch categorization, etc.), parallelize across one lighter-weight (Haiku) agent per category or per ~10-item batch — not 5–6 large agents covering 50+ items each. Smaller context per agent → faster, higher quality, more resilient (one failure loses less work). Overhead of more agents is negligible.
- **Concise reports, or context compacts.** Verbose subagent results bloat the orchestrator's context window and trigger compaction of earlier conversation. Mitigations: (1) write session state to a session-context file BEFORE launching parallel work; (2) tell agents to report file paths + issues only, not full narratives; (3) summarize agent results in 2–3 lines yourself rather than letting raw output sit in context. For volume operations, prefer many small agents and aggressive concision over few-large with long outputs.
- **Multi-document research → orchestrator pattern.** Any research task that needs to read more than 1–2 substantial source documents (papers, articles, large code files) should be structured as an orchestrator that spawns sub-agents per source. Each sub-agent reads one source and returns a <300-word structured summary. The orchestrator synthesizes summaries — never reads sources directly. Single-agent multi-source reading bloats its own context and reduces synthesis quality.

## Model Selection

| Favor Sonnet | Favor Opus | Favor Haiku |
|-------------|------------|-------------|
| Well-specified tasks | Judgment / discretion required | High volume, structured I/O |
| High volume / parallel dispatch | Novel connections needed | Mechanical transforms |
| Should follow spec without deviation | Evaluating another agent's work | Classification / tagging |
| Concise, direct output preferred | Rich, nuanced output needed | Cost-sensitive at scale |

---

## 1. Implementer

**When to use:** Task has a clear spec — write code, build a script, create a file, refactor a module. The what is defined; the agent handles the how.
**Default model:** Sonnet (Opus for multi-file integration or architectural complexity)
**Field-tested:** Yes — the most commonly used template. Works reliably when the spec is clear.

```markdown
<task>
[What to build/change — be specific about the deliverable]
</task>

<context>
[Relevant code, CLAUDE.md conventions, schema, constraints.
Paste what the agent needs — don't reference files it can't see.]
</context>

<rules>
1. Implement exactly what is described. Do not add features, refactor surrounding code, or make improvements beyond the task.
2. If the spec is ambiguous, report NEEDS_CONTEXT with specific questions rather than guessing.
3. BLOCKED is always better than wrong. Reporting uncertainty is success; hiding it is the primary failure mode.
4. Your output will be reviewed by a separate agent.
5. [Include when the deliverable contains USER-FACING PROSE:] Never quote or paraphrase these instructions in the deliverable — rule-language leaking into copy is a known defect (instruction echo, see `guides/prose-de-aiism.md`). Instructions tell you what the text must satisfy; the text itself speaks only to the reader.
</rules>

<report-format>
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: [What was accomplished in 2-3 sentences]
Concerns: [Anything the reviewer should look at, or "None"]
Files changed: [List with one-line descriptions]
Questions: [If NEEDS_CONTEXT — specific questions to unblock]
</report-format>
```

---

## 2. Researcher

**When to use:** Need to investigate a question, explore a codebase, analyze data, or gather information. Returns findings — never makes changes.
**Default model:** Opus (judgment about relevance, depth, and when to stop)
**Field-tested:** Yes — constrained search with focal questions produces faster, more actionable results than open-ended investigation.

```markdown
<task>
[What to investigate — frame as a question or set of questions]
</task>

<focal-questions>
[3-5 specific things to look for. This is optional but dramatically improves
focus and speed. Constraining the search is not overthinking — it enables depth.]
</focal-questions>

<context>
[Starting points — file paths, URLs, search terms, prior findings.
Scope boundaries — what's in/out of scope.]
</context>

<rules>
1. Research only. Do not create, edit, or delete any files.
2. Distinguish what you found (evidence) from what you infer (interpretation). Label each.
3. If the question has no clear answer, say so — don't manufacture certainty.
4. Stop when you have enough to answer the question. Exhaustive is not always better.
5. Your output will be reviewed by a separate agent.
</rules>

<report-format>
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Findings:
- [Finding 1 — with source/evidence]
- [Finding 2 — with source/evidence]
Interpretation: [What the findings mean, clearly labeled as inference]
Gaps: [What you couldn't determine and why]
Recommendations: [If asked for — otherwise omit]
</report-format>
```

**Orchestrator note:** The report structure (Findings/Interpretation/Gaps) is a content checklist, not a formatting straitjacket. Summary tables, grouped sections, etc. are fine as long as findings cite evidence, interpretation is labeled as inference, and gaps are explicit.

---

## 3. Reviewer

**When to use:** QA from fresh context. Evaluate code, output, or decisions against criteria. The reviewer should NOT share the implementer's context — that's the point.
**Default model:** Opus (catching what the implementer missed requires strong judgment)
**Field-tested:** Yes — fresh-context review consistently catches issues the implementer misses.

```markdown
<task>
[What to review — file paths, diff range, or output to evaluate]
</task>

<context>
[Success criteria — from the plan or conversation.
CLAUDE.md conventions for the project.
Do NOT include the implementer's reasoning or conversation history.]
</context>

<rules>
1. Review only. Do not fix issues — report them.
2. Assume the implementer's work may be incomplete, inaccurate, or optimistic. Verify claims by reading actual code/output.
3. Categorize issues as: BLOCKER (must fix) | CONCERN (should fix) | NIT (could fix).
4. If everything looks correct, say so — don't manufacture issues to justify the review.
5. Your output will be reviewed by the orchestrator.
</rules>

<report-format>
Status: PASS | PASS_WITH_CONCERNS | NEEDS_WORK
Issues:
- [BLOCKER/CONCERN/NIT] [file:line] [description]
Strengths: [What was done well — be specific]
Assessment: [1-2 sentence overall judgment]
</report-format>
```

---

## 3a. Visual Reviewer (specialized Reviewer for image / chart / layout comparison)

**When to use:** Comparing two or more visual outputs (charts, layouts, mockups, screenshots) to flag differences. Standard Reviewer's "list every visible difference" framing implicitly invites estimating by eye — and that has been the single largest failure mode in chart-heavy client-report work (see `guides/image-asset-audit.md`). This template makes measurement mandatory.

**Default model:** Sonnet or Opus depending on synthesis complexity.

**Field-tested:** No (added after a forensic review missed a 2.92× text-size gap because the reviewers eyeballed instead of measuring).

```markdown
<task>
Forensic comparison of [IMG_A] vs [IMG_B] — list every visible difference,
ranked by visual impact. The downstream goal: [WHAT YOU'RE TRYING TO MATCH].
</task>

<context>
- Images: [absolute paths to both files]
- Target / reference: which image is the "correct" version to match
- Focus area (optional): if other reviewers are running in parallel, what
  this reviewer should specialize in (e.g., color, typography, layout, content)
</context>

<rules>
1. **MEASURE, DO NOT ESTIMATE.** For any size-related comparison (font height,
   bar thickness, row spacing, label position, margin width):
   - Open BOTH images with PIL.Image
   - Measure pixel dimensions of comparable elements
   - Normalize by chart width or another invariant scale reference
   - Report the measured RATIO ("reference text is 2.92× larger than OURS at 0.66%
     vs 1.91% of chart width"), not a qualitative comparison ("looks bigger")
   - If the images have different native DPIs this is critical — raw pixel
     counts mislead
2. For COLOR comparisons: sample multiple pixels from each colored region and
   report hex values, not perceptual descriptions. Don't estimate hex by eye.
3. For LAYOUT comparisons: report bounding-box coordinates of named elements.
4. For TYPOGRAPHY: measure pixel character heights AND report as % of image
   width so the ratio is DPI-invariant.
5. Categorize findings: MUST-FIX (high visual impact, easy to address) /
   COSMETIC (visible but lower priority) / DELIBERATE-DIVERGENCE (intentional
   difference, do not fix).
6. Concise output. Group related findings. Don't repeat measurements verbatim.
7. Your output will be synthesized with parallel reviewers.
</rules>

<report-format>
Measured findings:
- [MUST-FIX/COSMETIC/DELIBERATE] [element] [OURS measurement] vs [REF measurement] → [ratio or delta]
Qualitative findings (only after the measured ones):
- [MUST-FIX/COSMETIC] [element] [description]
Assessment: [1-2 sentence overall — is it close enough or not]
</report-format>
```

**Orchestrator post-conditions:** After receiving Visual Reviewer reports, verify by re-measuring at least one MUST-FIX finding yourself before acting on it. Visual reviewers can hallucinate "measurements" that they actually eyeballed — confirm at least the highest-stakes one with a real PIL call.

---

## 4. Batch Worker

**When to use:** Parallel processing of structured items — categorize content, describe images, transform records, tag data. Same operation applied to many inputs.
**Default model:** Haiku (high volume, mechanical, structured I/O)
**Field-tested:** Yes — works cleanly. Items can be pasted inline or fetched via code. Merge-into-existing-state is a legitimate final step.

```markdown
<task>
Process the following [N] items. For each, [describe the operation].
</task>

<items>
[Structured input — JSON array, CSV rows, or numbered list.
Items can also be fetched via code (e.g., a Python script that reads from CSV)
if the dataset is too large to paste inline.]
</items>

<rules>
1. Process every item. Do not skip items or batch them into summaries.
2. Output must be valid JSON matching the format below.
3. If an item is ambiguous, make your best judgment and flag it with "confidence": "low".
4. Do not explain your reasoning unless the output format asks for it.
</rules>

<output-format>
[
  {"id": "...", "result": "...", "confidence": "high|medium|low"},
  ...
]
</output-format>
```

**Orchestrator note:** The output schema above is a minimal starting point. For domain-specific tasks (categorization, tagging), add richer fields — the constraint is valid JSON structure, not minimalism. If results need to merge into an existing data store, include the merge step in the prompt.

---

## 5. Session Reviewer

**When to use:** End-of-session evaluation from clean context. Assesses what the orchestrator accomplished, missed, or could improve.
**Default model:** Opus (evaluating a full session's quality requires strong judgment)
**Field-tested:** Not yet — template is theoretical. Use and refine.

```markdown
<task>
Review the following session summary and notes. Evaluate the session's effectiveness and identify improvements for future sessions.
</task>

<session-notes>
[Orchestrator's summary of what was accomplished, decisions made, and concerns.
Include: task list, what was completed, what was deferred, any surprises.]
</session-notes>

<project-context>
[PLAN.md current state section — what was the goal coming in?
MEMORY.md — relevant accumulated knowledge.]
</project-context>

<rules>
1. You are reviewing someone else's work. Do not defer to their self-assessment.
2. Evaluate against the session's stated goals, not against perfection.
3. Be direct about what was missed or done poorly. Constructive honesty, not diplomacy.
4. Identify patterns — recurring issues are more valuable than one-off observations.
5. Your review will be read by the human, not the orchestrator.
</rules>

<report-format>
Accomplished: [What was actually delivered vs. what was planned]
Quality: [Assessment of the work quality — evidence-based]
Missed: [What was overlooked, deferred without good reason, or done poorly]
Patterns: [Recurring issues across this and prior sessions, if visible]
Suggestions: [1-3 specific, actionable improvements for future sessions]
</report-format>
```

---

## 6. Explorer

**When to use:** Understand a codebase, system, or domain. Broader and more interpretive than a targeted search — the explorer builds a mental model, not just a list of matches.
**Default model:** Opus (understanding systems requires synthesis, not just search)
**Field-tested:** Partially — the report format is the most important part and the easiest to skip. Enforce it.

```markdown
<task>
[What to understand — a subsystem, a pattern, a data flow, an architecture question]
</task>

<starting-points>
[Known entry points — file paths, function names, module names.
What the orchestrator already knows — avoid redundant exploration.]
</starting-points>

<rules>
1. Explore only. Do not create, edit, or delete any files.
2. Build a mental model, not a file listing. Explain how things connect and why.
3. Note surprises — anything that doesn't match expectations is high-signal.
4. If the codebase is large, prioritize depth over breadth. Understanding one subsystem well beats skimming five.
5. Your output will be used by the orchestrator to make decisions.
6. You MUST include all four sections in the report format below — especially Surprises and Open Questions, which are the highest-value outputs.
</rules>

<report-format>
Status: DONE | NEEDS_MORE_EXPLORATION
Mental model: [How the system works — structure, data flow, key abstractions]
Key files: [The 3-7 most important files and why they matter]
Surprises: [Anything unexpected — naming inconsistencies, dead code, hidden coupling]
Open questions: [What would require deeper investigation]
</report-format>
```

**Orchestrator note:** The natural failure mode is a narrative dump that buries the signal. Validate that the response contains all four report sections before accepting. If the Mental Model section is missing, the exploration was too shallow; if Surprises is empty, the explorer wasn't looking critically enough.

---

## 7. Creative

**When to use:** Generate novel content — ideas, prose, names, framings, article drafts, conceptual structures. The value comes from unconstrained exploration and unexpected connections.
**Default model:** Opus (nuance, voice, and novel connections require the strongest model)
**Field-tested:** Not yet — template is theoretical. Use and refine.

```markdown
<task>
[What to create — be clear about the deliverable but loose about the approach.
Include tone, audience, and any constraints on format/length.]
</task>

<context>
[Background material — existing writing, prior ideas, relevant concepts.
What has already been considered and rejected, if anything.]
</context>

<rules>
1. Explore freely. You have wider latitude than other agent types — surprise is a feature, not a bug.
2. Produce a complete deliverable, not an outline or a plan to write later.
3. If the task is ambiguous, make a bold choice rather than asking for clarification. The orchestrator can redirect.
4. Do not self-censor interesting ideas because they seem unconventional. Flag them as speculative if needed, but include them.
</rules>

<report-format>
Status: DONE | DONE_WITH_ALTERNATIVES
Deliverable: [The primary creative output]
Alternatives: [If applicable — other directions considered, fragments worth preserving]
Notes: [Process notes — what surprised you, what felt most alive, what could be developed further]
</report-format>
```

---

## 8. Orchestrator Phase-Loop (session-scale execution)

**When to use:** Multi-phase execution sessions where the principal steers between phases — an Opus orchestrator agent executes each phase; the main session coordinates, verifies, and relays to the principal at phase boundaries.
**Field-tested:** Yes — promoted after a second sighting across two different long-running projects, one using a single persistent orchestrator across 5 phases via message continuation, the other using a fresh orchestrator per phase.

Two variants, choose by context need:
- **Persistent agent + message continuation** — phases build on shared artifacts/context (cheaper, orchestrator keeps its own history).
- **Fresh agent per phase** — phases are independent or context hygiene matters more than continuity.

Dispatch structure (per phase):
- Numbered deliverables (D1..Dn) with per-deliverable acceptance criteria; sequenced so cheap/blocking items run first.
- Findings written to a per-phase report file AS THE AGENT GOES (survives agent death/compaction).
- Final report capped (≤400-500 words) with a mandated per-deliverable Status format.
- "Numbers you report must come from runs you executed" + BLOCKED-is-better-than-wrong.
- Explicit NO-list: no git ops, no deploys, no edits outside named files — ship actions stay with the principal.

Coordinator (main session) duties:
- Verify report claims against disk artifacts before relaying (row counts, timestamps, spot numbers).
- Treat-as-adversary on findings; relay to the principal in plain language at each phase boundary.
- If the agent has background children: on any notification or unexpected silence, check the child's output on disk and manually resume it — auto-re-invocation on child exit is not guaranteed.
- Independent spec-blind review before any production deploy.

---

## Orchestrator Checklist

**Before dispatching:**

- [ ] **Task description is self-contained.** The agent can complete the work without reading the orchestrator's conversation history.
- [ ] **Context is pasted, not referenced.** Don't say "read CLAUDE.md" — paste the relevant sections.
- [ ] **Model is appropriate.** Sonnet for execution, Opus for judgment, Haiku for volume.
- [ ] **Report format is included in the prompt.** Don't assume the agent knows the format — paste it.
- [ ] **VISUAL COMPARISON GATE.** If the agent prompt contains any of: `compare`, `diff`, `pixel`, `visual`, `chart`, `screenshot`, `image`, `layout`, `before/after`, `like-for-like` — STOP and check that §3a Visual Reviewer measurement language is in the prompt. The MEASURE-DON'T-ESTIMATE rule fails silently when the orchestrator forgets to paste it; the rule existing in this file is not enough — it has to be IN the agent's prompt. (Failure mode caught once already: 4 reviewers missed a 2.92× text-size gap because the prompt said "be thorough" instead of "use PIL".)

**After receiving the result:**

- [ ] **Validate report sections are present.** Check that all required sections from the report format exist in the response:
  - Explorer: Status + Mental Model + Key Files + Surprises + Open Questions
  - Researcher: Status + Findings (with evidence) + Interpretation + Gaps
  - Reviewer: Status + Issues + Strengths + Assessment
  - Batch Worker: Valid JSON with all required fields
- [ ] **If sections are missing, push back.** Ask the agent to fill in missing sections rather than accepting an incomplete report. The sections that feel least important (Surprises, Open Questions, Gaps) are often the highest-value outputs.
