# Skills Reference

> **Note:** These are custom skills you build yourself as `.claude/commands/` files in your project. They don't ship with this repo — this reference shows the skill architecture that works well in practice. Start with 2-3 (e.g., `/start`, `/wrapup`, `/prompt`) and add more as your workflow matures.

## Workflow Skills

| Skill | Purpose |
|-------|---------|
| `/plan-task <description>` | Structured planning before implementation. Defines objectives, success criteria, sub-task decomposition. No implementation until approved. |
| `/implement <plan>` | Execute a pre-defined plan. Follows the plan as written, no redesigning. |
| `/research <topic>` | Read-only investigation. Launches research agents, synthesizes findings. No changes made. |
| `/review [target]` | QA against success criteria. Finds issues but doesn't fix them. |
| `/finalize [project]` | End-of-session COMP update. Records decisions, progress, state changes. |
| `/comp [directory]` | Create or update all 4 COMP files for a directory. |
| `/dialectic-review [flags] [focus]` | Multi-agent dialectic with 4 modes: `review` (Critics + Defenders + Referees), `--ideate` (Generators + Challengers + Synthesizers), `--tradeoff` (Advocates + Counter-Advocates + Referee), `--premortem` (Pessimists + Optimists + Risk Assessors). Supports `--agents X-Y-Z`, `--lens <expert>`, `--test-first`. |
| `/retro [scope]` | Periodic retrospective. Assesses what went well, what went poorly, patterns, and actionable suggestions. Scopes: `session` (default), `weekly`, `project <name>`. |
| `/prompt <brain dump>` | Converts informal/dictated requests into structured prompts, then executes. Supports `depth:light/standard/deep` and `hold` to skip execution. |
| `/prompt-only <brain dump>` | Same as `/prompt` but outputs the formatted prompt without executing. |
| `/prompt-refine <prompt>` | Audits an existing prompt against quality checklists and outputs an improved version. |
| `/review-plan [flags]` | Stress-tests a plan with expert critique, web research, and Red/Yellow/Green findings. Supports `quick`, `depth:deep`, `focus:dimension`, `role:"..."`. |
| `/prune [flags]` | Audit and trim auto-loaded files (CLAUDE.md, MEMORY.md) for context bloat. Supports `project:path`, `target:claude/memory`, `dryrun`, `auto`. |
| `/start [project] [— task]` | Session kickoff. Loads COMP files, presents status dashboard, micro-plans the session. |
| `/wrapup [flags]` | Session closer. Chains COMP updates + bloat check + session summary. Supports `noprune`, `prune` (full). |

## Recommended Workflow

1. `/start` — Load context, review state, plan the session
2. `/prompt` — Convert rough idea into structured instructions (or `/plan-task` for bigger efforts)
3. `/review-plan` — Stress-test the plan before building
4. `/implement` — Execute the plan (watch for dialectic triggers mid-session)
5. `/review` — Verify the results
6. `/wrapup` — Update COMP files + bloat check
7. `/prune` — Periodically trim context bloat (monthly or when `/wrapup` flags it)
