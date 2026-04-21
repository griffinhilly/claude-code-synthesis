# Skills Reference

> **Note:** These are custom skills you build yourself as `.claude/commands/` files in your project. The `skills/` directory in this repo ships ready-to-use skill definitions. Start with 2-3 (e.g., `/plan-task`, `/wrapup`, `/implement`) and add more as your workflow matures.

## Workflow Skills

Skills in this table have corresponding directories in `skills/`.

| Skill | Purpose |
|-------|---------|
| `/plan-task <description>` | Structured planning before implementation. Defines objectives, success criteria, sub-task decomposition. No implementation until approved. |
| `/implement <plan>` | Execute a pre-defined plan. Follows the plan as written, no redesigning. |
| `/research <topic>` | Read-only investigation. Launches research agents, synthesizes findings. No changes made. |
| `/review [target]` | QA against success criteria. Finds issues but doesn't fix them. |
| `/ship [commit message hint]` | Pre-commit readiness check. Verifies tests, COMP freshness, uncommitted changes, then drafts commit message and stages specific files. |
| `/verify [target]` | Post-completion verification. Catches missing data, stale references, broken assumptions. Run after pipeline steps, implementations, or any multi-step work. |
| `/finalize [project]` | End-of-session COMP update. Records decisions, progress, state changes. |
| `/comp [directory]` | Create or update all 4 COMP files for a directory. |
| `/wrapup [flags]` | Session closer. Chains COMP updates + bloat check + session summary. Supports `noprune`, `prune` (full). |
| `/retro [scope]` | Periodic retrospective. Assesses what went well, what went poorly, patterns, and actionable suggestions. Scopes: `session` (default), `weekly`, `project <name>`. |
| `/dialectic-review [flags] [focus]` | Multi-agent dialectic with 4 modes: `review` (Critics -> Defenders -> Referees), `--ideate` (Generators -> Challengers -> Synthesizers), `--tradeoff` (Advocates -> Counter-Advocates -> Referee), `--premortem` (Pessimists -> Optimists -> Risk Assessors). Supports `--agents X-Y-Z`, `--lens <expert>`, `--test-first`, `--audit` (hostile auditor), `--no-audit`. |
| `/brainstorm <topic>` | Generate a wide field of ideas, then pressure-test them. Five generators diverge, challengers prune, synthesizers rank what survives. |
| `/premortem [plan]` | Assume the plan failed, then explain why. Pessimists diagnose failure, optimists rebut, a risk assessor weighs which failures are real. |
| `/red-team [target]` | Adversarial stress-test with hostile auditor. Critics attack, defender rebuts, referee judges, then a 4th agent attacks the synthesis itself. `--audit` on by default; pass `--no-audit` for plain review. |
| `/tradeoff [options]` | Compare 2+ options with dedicated advocates, counter-advocates who challenge every position, and a decisive referee. |
| `/bug-hunt [target]` | Three-agent adversarial bug finder. Hunter overclaims, Skeptic disproves, Referee arbitrates. Scoring incentives force each role to behave honestly. Supports `--lens <expert>`. |
| `/socrates <thesis>` | Socratic debate session to stress-test a philosophical framework or thesis. |
| `/debug [issue]` | Structured debugging with mandatory evidence gathering before any fix attempt. 4-phase protocol (Observe -> Hypothesize -> Reproduce -> Fix) with hard gates between phases. |
| `/learn <type> <lesson>` | Capture structured learnings (gotcha, pattern, decision, bug-fix) as JSONL per project. Cross-project searchable. |

## Planned Skills

These skills are referenced in the workflow but don't yet ship as `skills/` directories in this repo. Build them yourself or wait for a future release.

| Skill | Purpose |
|-------|---------|
| `/start [project] [-- task]` | Session kickoff. Loads COMP files, presents status dashboard, micro-plans the session. |
| `/prompt <brain dump>` | Converts informal/dictated requests into structured prompts, then executes. Supports `depth:light/standard/deep` and `hold` to skip execution. |
| `/prompt-only <brain dump>` | Same as `/prompt` but outputs the formatted prompt without executing. |
| `/prompt-refine <prompt>` | Audits an existing prompt against quality checklists and outputs an improved version. |
| `/review-plan [flags]` | Stress-tests a plan with expert critique, web research, and Red/Yellow/Green findings. Supports `quick`, `depth:deep`, `focus:dimension`, `role:"..."`. |
| `/prune [flags]` | Audit and trim auto-loaded files (CLAUDE.md, MEMORY.md) for context bloat. Supports `project:path`, `target:claude/memory`, `dryrun`, `auto`. |

## Recommended Workflow

1. `/start` -- Load context, review state, plan the session
2. `/prompt` -- Convert rough idea into structured instructions (or `/plan-task` for bigger efforts)
3. `/review-plan` -- Stress-test the plan before building (triggers dialectic for complex plans)
4. `/implement` -- Execute the plan (watch for dialectic triggers mid-session)
5. `/verify` -- Check that outputs are complete, consistent, and nothing was silently skipped
6. `/review` -- QA against success criteria
7. `/ship` -- Pre-commit readiness check, stage files, commit with approval
8. `/wrapup` -- Update COMP files + skill health + bloat check
9. `/prune` -- Periodically trim context bloat (monthly or when `/wrapup` flags it)
