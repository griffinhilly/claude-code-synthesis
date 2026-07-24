# Scope Gate (Mandatory)

A deterministic checkpoint that fires during `/plan-task` before the plan is presented. Forces an explicit decision — run a dialectic-review or skip with a recorded reason — when the plan's estimated scope correlates with "decisions worth stress-testing."

## Why this exists

The CLAUDE.md Decision Quality Gates include a post-implementation trigger ("after 5+ files or 200+ lines, ask about dialectic review"). That trigger failed to fire twice during a phase of an earlier project — it lives in always-loaded context but isn't wired to a discrete execution event. The orchestrator was in execution-mode flow across multiple cuts and the always-loaded instruction stayed dormant.

This gate IS the discrete event that failure surfaced as missing. It fires when the skill is actively re-executing its own steps, at a plan-boundary where the orchestrator is re-reading instructions in a context where they're actionable. If you're reading this file, you're inside `/plan-task`'s execution loop — do not skip this step.

## Trigger computation

From the decomposition table built in Step 4, compute:

- **File count** — distinct files the sub-tasks touch. If the table doesn't name files explicitly, err high (count plausible touches, not committed ones).
- **LoC estimate** — sum of rough line estimates per sub-task. If the table lacks explicit LoC estimates, use complexity as a proxy: `trivial=10`, `moderate=50`, `complex=150`.

Also assess qualitatively:

- **Irreversible actions** — deletions, migrations, credential rotations, external API calls with side effects, published/shared artifacts
- **Multi-session scope** — plan explicitly spans ≥ 1 session boundary
- **Architectural touch** — plan modifies a file or system the project's CLAUDE.md flags as load-bearing, or a design decision that later cuts will depend on

**The gate fires if ANY of these is true:**
- File count ≥ 5
- LoC estimate ≥ 200
- Any irreversible action is present
- Plan is multi-session
- Plan has an architectural touch

Write the computed values down in your response. Don't silently self-classify — the act of writing "file count: 3, LoC: 180, no irreversibility, single session, no architectural touch → gate does not fire" is the mechanism that ensures the gate was actually checked.

## The question

When the gate fires, ask the user ONE question, in-conversation, before proceeding:

> This plan crosses Decision Quality Gate thresholds:
> - [list exactly which triggers fired, with the computed values]
>
> Run a dialectic-review before I implement? Options:
> - **yes** — I'll run `/dialectic-review --premortem` on the plan (typical cost: ~5 agents, ~5–10 minutes)
> - **tradeoff** — I'll run `/dialectic-review --tradeoff` instead (use this if there are 2+ competing approaches worth comparing)
> - **skip: <reason>** — proceed without review; your reason gets written to PLAN.md as a paper trail

Then stop and wait for a response. Do not proceed to Step 7 until the user answers.

## Response handling

### yes
Invoke `/dialectic-review --premortem` on the plan. After it returns, integrate findings into the plan, then continue to Step 7 (Present the Plan).

### tradeoff
Invoke `/dialectic-review --tradeoff` with the competing approaches framed explicitly. Integrate findings, then continue to Step 7.

### skip: \<reason\>
The reason is mandatory and must be substantive. Bounce these and re-ask:
- `skip` alone (no reason)
- `skip: trivial`, `skip: small`, `skip: routine` (non-descriptive)
- `skip: user approved` (shifts decision without substance)

Valid reasons look like:
- `skip: mechanical refactor, no design decisions`
- `skip: already dialectic-reviewed in prior session — see MEMORY.md "Cut N dialectic"`
- `skip: low reversal cost, prefer to iterate`
- `skip: single-file change with well-understood pattern from prior cut`

Once a valid skip is received, append a one-line entry to the project's `PLAN.md` under a `## Gate Decisions` section (create the section if missing):

```
- [YYYY-MM-DD] /plan-task scope gate fired by [list triggers]. Skipped: "<the reason>"
```

If the project has no `PLAN.md` (new project, standalone script), state the skip reason inline in your response and note that no paper trail was written.

Then continue to Step 7.

## Why the paper trail matters

The project owner re-reads `PLAN.md` at session-start time. A skip reason visible in the next session creates mild social pressure against routine bypassing and makes the skip pattern auditable across sessions. Without this, "skip" collapses into muscle memory — which is exactly what a pre-push hook would have produced with a commit trailer.

The paper trail is not bureaucratic. It's the single mechanism that prevents this gate from degrading into ritual.

## What this gate does NOT do

- It does not enforce at `git push` time. Push-time enforcement was considered and rejected — see an earlier project's MEMORY.md for the full analysis, if you're maintaining one.
- It does not check completed diffs. This gate fires on the *plan*, before any code exists.
- It does not replace the argue-the-opposite step or the multi-model synthesis step in `polishing-guide.md`. Those are lighter checks for different purposes.
