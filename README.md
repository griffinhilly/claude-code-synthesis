# Claude Code Workflow

A complete, opinionated Claude Code workflow. 18 skills, 6 hooks, 11 guides, and an operating model you can install in one command.

**This isn't a tutorial or a library.** It's a working configuration -- built over months of daily use -- that you can copy into your own setup and adapt.

## What's New in v2

v1 shipped the operating model (`CLAUDE.md`) and a handful of guides. v2 ships the full working system:

- **18 skills** -- slash commands covering the entire session lifecycle, from planning through implementation to session close
- **6 hooks** -- PreToolUse and PostCompact hooks for security, observability, and context recovery
- **2 tools** -- Python utilities for cross-session search and skill usage analytics
- **3 new guides** -- pipeline diagnostics, learning from reference repos, and a deep comparison of Superpowers / gstack / Compound Engineering
- **Updated CLAUDE.md** -- 10+ new behavioral rules including structured debugging, subagent validation, confidence-scored planning, three-fix escalation, and knowledge compounding
- **Source analysis** -- `guides/reference-repo-comparison.md` maps exactly what this repo adopted from each major framework, what it skipped, and why

## Quick Start

**Tier 1: Just the operating model.**
```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```
Edit the `Platform Notes` and `Interaction Style` sections to match your setup. This single file changes how Claude approaches every task.

**Tier 2: Full install.**
```bash
git clone https://github.com/griffinhilly/claude-code-synthesis /tmp/claude-workflow

# Operating model
cp /tmp/claude-workflow/CLAUDE.md ~/.claude/CLAUDE.md

# Skills (copy to project or global commands)
cp -r /tmp/claude-workflow/skills/* ~/.claude/commands/

# Hooks
cp -r /tmp/claude-workflow/hooks/* ~/.claude/hooks/

# Guides
cp -r /tmp/claude-workflow/guides ~/.claude/guides

# Tools
cp -r /tmp/claude-workflow/tools ~/.claude/tools
```

**Tier 3: Let Claude do it.**
Tell Claude Code: *"Clone https://github.com/griffinhilly/claude-code-synthesis and set up my config based on it."*

## What's In Here

### `CLAUDE.md` -- The Operating Model

The behavioral contract that governs every session. Defines leverage doctrine (human decides, Claude executes), plan-first protocol, scope discipline, agent principles, dialectic reviews, implementation behavior, security safeguards, the COMP documentation system, and workflow evolution rules. See the [Key Ideas](#key-ideas-worth-highlighting) section below for highlights.

### `skills/` -- 18 Slash Commands

Skills are `.claude/commands/` files that encode multi-step workflows as single invocations. They range from lightweight wrappers (brainstorm, premortem) to complex multi-agent protocols (dialectic-review, debug).

| Skill | What It Does |
|-------|-------------|
| `/plan-task` | Structured planning with decomposition, risk checklists, and confidence scoring. No implementation until approved. |
| `/implement` | Execute a pre-defined plan. Delegates to subagents with mandatory validation. |
| `/research` | Read-only investigation. Launches research agents, synthesizes findings. No changes made. |
| `/review` | QA against success criteria. Finds issues but doesn't fix them. |
| `/verify` | Post-completion verification. Catches missing data, stale references, red flag language. |
| `/debug` | 4-phase structured debugging (Observe, Hypothesize, Reproduce, Fix) with hard gates between phases. |
| `/ship` | Pre-commit readiness check. Tests, COMP freshness, staged file review, commit message draft. |
| `/comp` | Create or update all 4 COMP files for a directory. |
| `/finalize` | Lightweight end-of-session COMP update. |
| `/wrapup` | Full session closer: COMP updates + skill health check + bloat audit + session summary. |
| `/retro` | Periodic retrospective. Scopes: session, weekly, or project. Turns patterns into rules. |
| `/learn` | Capture structured learnings (gotcha, pattern, decision, bug-fix) as JSONL. Cross-project searchable. |
| `/dialectic-review` | Multi-agent adversarial analysis. 4 modes: review, ideate, tradeoff, premortem. Configurable agents and expert lenses. |
| `/brainstorm` | Dialectic ideation. Wrapper for `/dialectic-review --ideate`. |
| `/premortem` | Assume failure, find the causes. Wrapper for `/dialectic-review --premortem`. |
| `/red-team` | Adversarial stress-testing of code, plans, or arguments. Wrapper for `/dialectic-review`. |
| `/tradeoff` | Compare options with dedicated advocates and a decisive referee. Wrapper for `/dialectic-review --tradeoff`. |
| `/socrates` | Socratic questioning to stress-test a philosophical framework or thesis. |

### `commands/` -- 8 Workflow Commands

Commands are user-invocable slash commands that handle session lifecycle and prompt formatting. Unlike skills (which are task-specific), commands are workflow infrastructure -- session start/end, commit preparation, plan review, context pruning.

| Command | What It Does |
|---------|-------------|
| `/start` | Session kickoff. Loads COMP files, presents status dashboard, micro-plans the session. |
| `/wrapup` | Session closer. COMP updates + bloat check + session summary. (Also in `skills/`.) |
| `/prompt` | Converts informal/dictated ideas into structured prompts, then executes. |
| `/prompt-only` | Same as `/prompt` but outputs the formatted prompt without executing. |
| `/prompt-refine` | Audits an existing prompt against quality checklists. |
| `/review-plan` | Stress-tests a plan with expert critique and Red/Yellow/Green findings. |
| `/prune` | Audit and trim auto-loaded files (CLAUDE.md, MEMORY.md) for context bloat. |
| `/overnight` | Set up overnight autonomous batch runs with retry and checkpoint logic. |

### `hooks/` -- 6 Event Hooks

| Hook | Trigger | What It Does |
|------|---------|-------------|
| `warn-destructive.sh` | PreToolUse (Bash) | Blocks `rm -rf`, `DROP TABLE`, `git push --force`, and similar destructive commands |
| `check-staged-secrets.sh` | PreToolUse (Bash) | Scans staged files for credentials before `git commit` |
| `block-secret-bash.sh` | PreToolUse (Bash) | Blocks `cat`, `head`, `tail` on known secret file patterns |
| `block-secret-reads.sh` | PreToolUse (Read) | Blocks the Read tool on `.env`, credential, and key files |
| `log-skill-usage.sh` | PreToolUse (Bash) | Tracks skill invocations to a log file for usage analytics |
| `post-compact-reminder.sh` | PostCompact | Re-injects session context after conversation compaction |

### `tools/` -- 2 Python Utilities

| Tool | What It Does |
|------|-------------|
| `session-search.py` | Cross-session keyword search over conversation history. Supports `--project`, `--days`, `--role`, `--max` filters. |
| `skill-usage-report.py` | Skill usage analytics: invocation counts, trends, dead skill detection. Reads the log produced by `log-skill-usage.sh`. |

### `guides/` -- 11 On-Demand Reference Docs

Guides load on-demand when triggered by specific situations. This keeps `CLAUDE.md` lean while making deep knowledge available when needed.

| Guide | When to Load It |
|-------|----------------|
| `skills-reference.md` | Need the full skills table or recommended workflow |
| `delegation-templates.md` | Delegating work to subagents -- 7 agent types with prompt templates |
| `reference-repo-comparison.md` | Comparing Superpowers, gstack, and Compound Engineering frameworks |
| `pipeline-diagnostic.md` | Debugging data pipelines stage by stage |
| `golden-exemplar.md` | Learning patterns from reference repos before building |
| `context-efficiency.md` | Sessions feel slow or token usage is high |
| `overnight-runner.md` | Running autonomous batch jobs overnight |
| `bookmark-archive.md` | Building a searchable bookmark archive from exported data |
| `shell-rules.md` | Shell command conventions (flag quoting, HEREDOCs) |
| `prefer-apis.md` | Fetching data from websites (API over scraping) |
| `postgres-batching.md` | Exploratory database queries needing repeated approval |

### `examples/data-pipeline/` -- Working Example

A complete data enrichment pipeline demonstrating these patterns in action: step-based pipeline runner with dry-run and skip flags, LLM batch categorization with taxonomy normalization, verify-and-merge cycles, and semantic search over enriched data.

## The COMP System

Every project maintains 4 files that keep Claude Code effective across sessions:

| File | Purpose | Audience | Updates |
|------|---------|----------|---------|
| **C**LAUDE.md | Behavioral contract -- how Claude should work here | Agent | Rare |
| **O**RIENT.md | Orientation -- what a human needs to know | Human | When project shape changes |
| **M**EMORY.md | Accumulated knowledge -- decisions, gotchas | Agent + Human | Most sessions |
| **P**LAN.md | Direction -- roadmap, progress, next steps | Human + Agent | Most sessions |

The key insight: separate *behavioral instructions* (CLAUDE.md) from *human orientation* (ORIENT.md) from *accumulated knowledge* (MEMORY.md) from *direction* (PLAN.md). Each file has a different audience, change frequency, and purpose.

## Key Ideas Worth Highlighting

**Orchestrator-first mindset.** The session agent shouldn't do everything itself. Before any task, assess: handle directly, delegate to a subagent, or route to MCP? This is the single biggest lever for productivity with Claude Code.

**Dialectic reviews.** For important decisions, don't ask Claude "what should I do?" Instead, spawn opposing agents -- one argues FOR, one argues AGAINST -- with a referee to synthesize. Four modes cover different needs: adversarial review, ideation, tradeoff comparison, and premortem.

**Structured debugging (4-phase).** Evidence before hypotheses. Hypotheses before reproduction. Reproduction before fix. Each phase has a hard gate requiring a written artifact. Prevents the "just try random fixes" loop that wastes unbounded time.

**Three-fix escalation.** If a fix has been attempted 3 times and the problem persists, STOP. Don't try a fourth. The approach or architecture is likely wrong. Escalate to the human.

**Subagent distrust.** Implementation subagents are assumed unreliable until verified. The `/implement` skill mandates post-execution validation by a fresh-context subagent that doesn't share the implementer's assumptions.

**Confidence-scored planning.** Plans identify where confidence is lowest and dispatch targeted research to weak sections before implementation begins. Adapted from Compound Engineering's `ce-plan`.

**Knowledge compounding.** The `/learn` skill captures structured learnings (gotchas, patterns, decisions, bug fixes) as searchable JSONL. Knowledge from one project informs the next. The `/retro` skill turns recurring patterns into permanent rules or new skills.

**Progressive disclosure.** Don't dump everything into CLAUDE.md. Keep it lean with trigger rules ("when X happens, read guide Y"). The guides load on-demand, keeping always-loaded context small and token costs low.

**Forcing specificity.** "Use version control" is not a useful lesson. "Commit data pipeline changes separately from visualization changes so rollbacks are clean" is. Every encoded rule and learning must reference concrete experience.

**Compaction-safe artifacts.** Claude Code conversations get compressed as they grow. Important outputs should be written to files immediately, not left in conversation history. The `post-compact-reminder.sh` hook re-injects session context after compaction events.

**Operationalize every fix.** When a bug is found and fixed, don't stop. Write tests that catch that bug *and* the whole class of similar bugs. Check for other instances. Update instructions if the bug reveals a workflow gap. Every bug is a learning opportunity.

**Evals before specs.** Define how you'll evaluate success *before* writing the spec. The progression -- evals, spec, plan, implement, verify -- produces better outcomes than plan, implement, "does this look right?"

**Human gates in pipelines.** Data enrichment workflows aren't fully automatable. Making the interruptible workflow explicit -- with named steps, skip flags, and resume points -- is better than pretending it's a straight-through pipeline.

**The virtuous circle.** Use your tools to improve your tools. Extract patterns from past sessions into skills or guides, apply them to new projects, refine based on results. The workflow improves itself through use.

## Recommended Workflow

The 9-step flow from `/start` to `/prune`, covering a complete session lifecycle:

1. **`/start`** -- Load context, review state, plan the session
2. **`/prompt`** or **`/plan-task`** -- Convert a rough idea into structured instructions (use `/plan-task` for bigger efforts)
3. **`/review-plan`** -- Stress-test the plan before building (triggers dialectic for complex plans)
4. **`/implement`** -- Execute the plan with subagent validation
5. **`/verify`** -- Check that outputs are complete, consistent, and nothing was silently skipped
6. **`/review`** -- QA against success criteria
7. **`/ship`** -- Pre-commit readiness check, stage files, commit
8. **`/wrapup`** -- Update COMP files, check skill health, audit context bloat
9. **`/prune`** -- Periodically trim context bloat (monthly or when `/wrapup` flags it)

Not every session uses all 9 steps. A quick bug fix might be `/start`, `/debug`, `/ship`, `/wrapup`. A planning session might be `/start`, `/plan-task`, `/review-plan`, `/wrapup`. Use judgment.

## Standing on the Shoulders of Giants

This workflow didn't emerge in a vacuum. Most ideas were shaped by things read, bookmarked, and experimented with. Here's where the concepts come from.

### Agent Architecture and Orchestration

- **Boris Cherny** ([@bcherny](https://x.com/bcherny)) -- Creator of Claude Code. His [tips thread](https://x.com/bcherny/status/2017742741636321619) on how the Claude Code team uses the tool differently than most people was foundational. His insight about separate context windows and test-time compute directly shaped the orchestrator-first and subagent delegation patterns.
- **@systematicls** -- Their [reply about context windows](https://x.com/systematicls/status/2031190025833181586) ("aggressively clear them when doing your work, and you can have your own code review agents by building a new context window") crystallized the fresh-eyes-for-review principle.
- **@doodlestein** -- Their observation that [the Unix tool approach](https://x.com/doodlestein/status/2000271365816131942) ("focused, composable functional units that can be used in isolation or as part of a larger pipeline") is the best model for AI agents directly influenced how the delegation templates are structured.
- **Simon Willison** ([@simonw](https://x.com/simonw)) -- His [Agentic Engineering Patterns](https://x.com/simonw/status/2025990408514523517) guide is the most rigorous public treatment of coding agent best practices. Many of the implementation behavior rules reflect patterns he documented.

### Source Frameworks: Superpowers, gstack, Compound Engineering

- **Jesse Vincent** ([@obra](https://x.com/obra)) -- [Superpowers](https://github.com/obra/superpowers): methodology-as-code with 14 skills and zero infrastructure. Key adoptions: 4-phase structured debugging (`systematic-debugging`), red flag language detection (`verification-before-completion`), TDD enforcement, three-fix escalation rule, and psychology-based agent persuasion using Cialdini's influence principles.
- **Garry Tan** ([@garrytan](https://x.com/garrytan)) -- [gstack](https://github.com/garrytan/gstack): virtual engineering team with 31 skills. Key adoptions: persistent browser daemon architecture (ref system over CSS selectors), `learn` skill for knowledge capture, cross-model review concept (generalized here to cross-role dialectic), and the plan-exit review pattern. The `careful`/`freeze`/`guard` hooks and office-hours forced specificity influenced our hook and guide design.
- **Every Inc / Nathan Baschez** -- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin): knowledge compounds over time. Key adoptions: `ce-compound` knowledge compounding (simplified to JSONL-based `/learn`), `ce-review` 18-reviewer confidence-gated system (simplified to single-reviewer with structured dimensions), `ce-plan` confidence scoring for plans, and the discoverability check (verifying that captured knowledge is actually findable by agents).

For the full mapping of what was adopted from each framework, what was skipped, and why, see `guides/reference-repo-comparison.md`.

### CLAUDE.md and Context Management

- **Todd Saunders** ([@toddsaunders](https://x.com/toddsaunders)) -- His insight about [rewriting CLAUDE.md from scratch](https://x.com/toddsaunders/status/2032436777630540182) every few weeks, and understanding that CLAUDE.md occupies a "high-dimensional vector space" of possible starting coordinates, shaped the quarterly CLAUDE.md health review.
- **@mstockton** -- Their [reply expanding on Todd's point](https://x.com/mstockton/status/2032451135479353790) about CLAUDE.md being the first file loaded into context helped crystallize the progressive disclosure pattern.
- **Pawel Huryn** ([@PawelHuryn](https://x.com/PawelHuryn)) -- His post about [tracking domain vs procedural knowledge](https://x.com/PawelHuryn/status/2033227605952889008) became the knowledge-type separation in the context efficiency guide.
- **@koylanai** -- Their [hook ideas table](https://x.com/koylanai/status/2031121107164467659) (18 practical hook ideas) is the best starting point for building your own Claude Code hooks.

### Structured Prompting and XML Tags

- **Anthropic's prompting documentation** -- The principle that Claude processes tagged content (XML) differently than prose comes directly from Anthropic's engineering practices.
- **@ihtesham2005** -- Their [thread on Anthropic's internal prompting docs](https://x.com/ihtesham2005/status/2032939863696388237) was the catalyst for the "prefer structured over prose" rule.
- **@Austen** -- Their post that ["the closer you can get to structured/executable formats, the better"](https://x.com/Austen/status/2033369724420026822) reinforced this as a hard rule.

### Test-First Bug Fixing, Operationalization, and Multi-Agent Review

- **@tangming2005** -- Their post about the ["single biggest improvement to my CLAUDE.md"](https://x.com/tangming2005/status/2031358195558658266) -- writing a reproduction test before fixing -- is almost verbatim the test-first bug fixing rule.
- **@doodlestein** -- Their ["Agent Coding Life Hack"](https://x.com/doodlestein/status/2036236834507047288) is the direct source of "operationalize every fix." Their broader work on the ["virtuous circle"](https://x.com/doodlestein/status/2035479010147242046) shaped the Workflow Evolution section.
- **@danpeguine** -- Their implementation of [@systematicls's method](https://x.com/danpeguine/status/2029268229030285589) using Hunter, Skeptic, and Referee agents was the direct inspiration for the dialectic review pattern.

### Plan-First and Scope Discipline

- **@doodlestein** -- Their posts about [the planning process](https://x.com/doodlestein/status/2014183464573047043) ("everyone gives short shrift to this part for some reason, and it's THE difference") shaped the plan-first protocol.
- **Garry Tan** ([@garrytan](https://x.com/garrytan)) -- His [/plan-exit-review skill](https://x.com/garrytan/status/2026778016463138882) directly inspired the review-plan skill.
- **Arvid Kahl** ([@arvidkahl](https://x.com/arvidkahl)) -- His advice to ["shift-tab into planning mode, and mention 'do deep research on best practices'"](https://x.com/arvidkahl/status/2031457304328229184) reinforced plan-first as a hard default.
- **Aakash Gupta** ([@aakashgupta](https://x.com/aakashgupta)) -- His observation about [building hundreds of working prototypes](https://x.com/aakashgupta/status/2029436537629491555) instead of writing PRDs shaped the "keep planning brief, start executing" style.

### Human-AI Leverage and Division of Labor

- **Ethan Mollick** ([@emollick](https://x.com/emollick)) -- His advice to ["collect your hard problems and good ideas now, they will get more valuable"](https://x.com/emollick/status/2026074883646517468) captures the leverage doctrine's human role perfectly.
- **Francois Chollet** ([@fchollet](https://x.com/fchollet)) -- His framing of [agentic coding as machine learning](https://x.com/fchollet/status/2024519439140737442) influenced how the orchestrator-first principle thinks about the human's role.

### Code Quality and Anti-Over-Engineering

- **Andrej Karpathy** ([@karpathy](https://x.com/karpathy)) -- His observation that ["agents bloat abstractions, have poor code aesthetics, are very prone to copy pasting"](https://x.com/karpathy/status/2035173492447224237) is exactly why the implementation behavior section emphasizes boring solutions.
- **@andrewmccalip** -- Their point about the ["specific disease in engineering"](https://x.com/andrewmccalip/status/2001517352324874358) where we "treat time as though it's free" reinforced naive-then-optimize.
- **@garybasin** -- His [complexity cleanup skill](https://x.com/garybasin/status/2036079728872890687) ("derive, don't store; make wrong states impossible") operationalizes the anti-over-engineering principle.

### Overnight Autonomous Runs

- **@witcheer** -- Their post about [running autoresearch overnight](https://x.com/witcheer/status/2030900817700565394) ("9PM to 6AM, 35 experiments, zero intervention") was the direct inspiration for the overnight runner.
- **@archiexzzz** -- Their [deep dive into autoresearch](https://x.com/archiexzzz/status/2033034161611817300) informed the batch mode vs resume mode distinction.
- **Anthropic's scheduled tasks** ([@trq212](https://x.com/trq212/status/2030019397335843288)) -- The official feature handles the simple case; the overnight runner handles usage limit retries, batch checkpointing, and multi-session resume.

### Evals-First, Agent Steering, and Skill Design

- **@synopsi** -- Their post about [evolving from plan-implement-review to evals-first](https://x.com/synopsi/status/2035971021510230401) is the source of the "evals before specs" principle.
- **Yishan Wong** ([@yishan](https://x.com/yishan)) -- His insight that ["saying 'remember to do X' is unreliable"](https://x.com/yishan/status/2035763780299510018) but presenting a possibly-wrong claim triggers corrective behavior shaped "corrective framing over reminders."
- **@doodlestein** -- Their work on the ["Agent Flywheel"](https://x.com/doodlestein/status/2036280197851320530) ("skills are a LOT more than just markdown files") is the foundational influence on treating skills as compressed expertise.

### After-Action Reviews and Premortem

- **Emmet Penney** ([@NukeBarbarian](https://x.com/NukeBarbarian)) -- His Ignatius skill, built on the Ignatian Pedagogical Paradigm, shaped the after-action review process and cumulative learning pattern.
- **Gary Klein** -- The premortem technique (imagine failure, work backwards) is from Klein's naturalistic decision-making research, popularized by Kahneman in *Thinking, Fast and Slow*.

### Community

- **OpenClaw** (via [@MillieMarconnni](https://x.com/MillieMarconnni/status/2030206607616053701)) -- The open-sourced Claude Code setup that won an Anthropic hackathon validated the idea that configurations are worth packaging and sharing.
- **@gvp324377** -- Their [division of AI users](https://x.com/gvp324377/status/2028994853707891083) into "people who use AI to tell them they are right" vs "people who use AI to tell them all the ways they could be wrong" is the philosophical foundation of the anti-sycophancy rule.

### Libraries

- [sentence-transformers](https://www.sbert.net/) by **Nils Reimers and Iryna Gurevych** -- the semantic search backbone in the data pipeline example.
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) -- the default embedding model. 22M params, 384-dim, runs on CPU.
- Pipeline runner pattern draws from [Luigi](https://github.com/spotify/luigi) (Spotify) and [Prefect](https://www.prefect.io/), simplified to a single file.

### Tools

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by **Anthropic** -- the AI coding assistant this workflow is built for.

## Build Your Own Bookmark Archive

The data pipeline example in this repo was originally built to archive and search bookmarks. The attributions section above? Every single source was found by running semantic search over archived bookmarks -- `python search.py "agent orchestration pattern" --top-k 5`.

If you want to do the same thing with your own bookmarks, see `guides/bookmark-archive.md` for the full walkthrough: HAR capture, extraction, media download, AI image descriptions, LLM categorization, semantic search. Total cost is roughly $1-3 in API credits for ~2,000 bookmarks.

Your bookmarks are a curated signal of what you found valuable. This pipeline turns that signal into a searchable knowledge base.

## License

MIT -- use however you want.
