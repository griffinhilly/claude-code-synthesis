---
name: dialectic-review
description: Dialectic process for reviewing, brainstorming, comparing tradeoffs, or stress-testing plans. Configurable modes, agent counts, and expert lenses.
user-invocable: true
disable-model-invocation: false
argument-hint: [--mode review|ideate|tradeoff|premortem] [--agents X-Y-Z] [--lens <expert>] [--test-first] [--audit] [focus area]
---

# Dialectic Review

A multi-agent dialectic with four modes. The primitive is always the same: **structured opposition with impartial synthesis**. Modes set the role framing, default agent counts, and number of rounds.

## Modes

| Mode | Alias | Phase 1 | Phase 2 | Phase 3 | Default Agents | Rounds |
|------|-------|---------|---------|---------|---------------|--------|
| `review` | `/red-team` | Critics attack | Defenders rebut | Referees judge | 3-1-1 | 1 |
| `ideate` | `/brainstorm` | Generators create | Challengers prune | Synthesizers rank | 5-2-3 | 1 (future: multi-round) |
| `tradeoff` | `/tradeoff` | Advocates (1 per option) | Counter-advocates challenge | Referees rank | N-N-1 | 1 |
| `premortem` | `/premortem` | Pessimists explain failure | Optimists argue success | Risk assessors weigh | 3-2-1 | 1 |

Note: `/red-team` enables `--audit` by default (adds Phase 4 hostile auditor). Pass `--no-audit` to run plain review mode.

## Argument Parsing

Parse `$ARGUMENTS` for these flags (order-independent, all optional):

| Flag | Effect | Default |
|------|--------|---------|
| `--mode <mode>` | Set the mode | `review` |
| `--ideate` | Shorthand for `--mode ideate` | — |
| `--tradeoff` | Shorthand for `--mode tradeoff` | — |
| `--premortem` | Shorthand for `--mode premortem` | — |
| `--agents X-Y-Z` | Agent counts per phase | Mode-dependent (see table) |
| `--lens <expert>` | Expert perspective (e.g., `security`, `performance`, `UX`) | none (generalist) |
| `--test-first` | Phase 2 writes failing tests instead of prose (review mode only) | off |
| `--audit` | Add Phase 4: hostile auditor attacks the synthesis itself | off (but on by default when invoked via `/red-team`) |
| `--no-audit` | Disable the hostile auditor phase (use to opt out when invoked via `/red-team`) | — |

**Recommended `--lens` values**: `security`, `performance`, `UX`, `data-integrity`, `cost`, `temporal` (timeline/sequencing risks), `user-advocate` (end-user empathy), `scalability`

Everything not matching a flag is the **focus area**.

Examples:
```
/dialectic-review the migration plan                      # Review mode, 3-1-1
/dialectic-review --lens security fetch_articles.py       # Review with security lens
/dialectic-review --ideate features for the dashboard      # Ideation, 5-2-3
/dialectic-review --tradeoff "GMM vs K-Means for user clustering"
/dialectic-review --premortem "the overnight autonomous runner"
/dialectic-review --agents 5-3-2 --lens performance the BPM query
```

## Context Gathering

1. Identify the **subject**: code files, an argument, a plan, options to compare, or a domain for ideation.
2. If it involves code, list the relevant file paths.
3. If `--lens` is set, note the expert perspective — injected into every agent prompt.
4. Read the project's CLAUDE.md and MEMORY.md for project context.

## Context Isolation Rule

**CRITICAL**: Each agent receives ONLY:
- The subject description and relevant file paths
- Project CLAUDE.md and MEMORY.md (for project context)
- Output from prior phases (as specified per mode)
- The expert lens (if set)

Do NOT pass conversation history, your own opinions, or framing that could anchor the agents. Neutral handoffs only.

---

## Mode Dispatch

Based on the parsed mode, read the corresponding prompt file in this directory:

| Mode | Prompt file |
|------|------------|
| `review` | `review-prompts.md` |
| `ideate` | `ideation-prompts.md` |
| `tradeoff` | `tradeoff-prompts.md` |
| `premortem` | `premortem-prompts.md` |

Follow the three-phase process defined in that file. Each file defines the role names, prompt templates, merge strategy, and summary format.

## Shared Rules (all modes)

- Launch each phase's agents in parallel using the Agent tool.
- Use **Opus** for referees/synthesizers/risk-assessors (judgment-heavy). Use **Sonnet** for other roles.
- If multiple agents in the same phase, merge outputs — deduplicate overlapping points, keep the strongest version, note disagreements.
- After the final phase, present a concise summary. Do NOT ask the user if they want to proceed -- just present findings.
- If `--audit` is set, run the Hostile Auditor phase (see below) AFTER the normal summary.

## Phase 4: Hostile Auditor (when `--audit` is set)

After the three-phase process completes its synthesis, launch a single Opus agent that attacks the synthesis itself. This closes the gap where the review process never stress-tests its own conclusion.

```
You are a HOSTILE AUDITOR. You will receive a synthesis/conclusion produced by a multi-agent review process. Your job is to ATTACK IT.

CONTEXT ISOLATION: You receive ONLY the information below. You were not part of the prior process and owe it no deference.

THE SYNTHESIS TO ATTACK:
[Full output from Phase 3]

ORIGINAL SUBJECT:
[Subject description and file paths]

YOUR TASK:
1. What did the synthesis get WRONG? Where did it paper over disagreements with false compromise?
2. What did the entire process MISS? What questions were never asked? What assumptions went unchallenged?
3. Where is the synthesis WEAKEST? If you had to bet against one conclusion, which one and why?
4. What's the STRONGEST argument against the synthesis's main recommendation?

Be maximally adversarial. The synthesis has already been through three phases of review — easy criticisms were already caught. Your job is to find what survived.

Format:
- ERRORS: Things the synthesis got wrong
- BLIND SPOTS: Questions never asked
- WEAKEST POINT: Where to bet against
- COUNTER-ARGUMENT: The strongest case against the main recommendation
- VERDICT: Is this synthesis trustworthy enough to act on? (YES WITH CAVEATS / NO — REDO / YES)
```

Present the auditor's findings after the main summary, clearly labeled as "Hostile Audit." If the auditor's verdict is "NO -- REDO," flag this prominently.

### Sources

- [KyleAMathews/hegelian-dialectic-skill](https://github.com/KyleAMathews/hegelian-dialectic-skill) -- hostile auditor concept (Phase 6 validation)
- [Riley-Coyote/polyclaude](https://github.com/Riley-Coyote/polyclaude) -- temporal and user-advocate perspective lenses
