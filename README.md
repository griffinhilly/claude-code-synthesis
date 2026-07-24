# Claude Code Workflow

A complete, opinionated Claude Code workflow. 23 skills, 10 hooks, 29 guides, 7 tools, a routing table, and an operating model you can install in one command.

**This isn't a tutorial or a library.** It's a working configuration -- built over a year of daily use -- that you can copy into your own setup and adapt.

## What's New in v3

v2 (April 2026) shipped the full skill/hook/guide system. v3 ships three months of what daily use did to it -- including the parts that reversed:

- **Usage honesty.** The skill-usage log now has enough data to say what actually gets used (see [What Actually Gets Used](#what-actually-gets-used) below). The verdict reshaped this release: session-lifecycle ritual and dialectic review carry the workflow; many of the specialist one-shot skills mostly don't get invoked.
- **RESOLVER.md** -- a routing table mapping task descriptions to skill invocations and content types to filing destinations. The single biggest structural addition since v2: with 20+ skills, "what should I invoke" and "where does this fact go" became decisions worth making deterministic. Includes a formal ≥2-sightings promotion gate for candidate rules.
- **A reversed rule.** v2's Scope Discipline told Claude to push back on ambitious plans and suggest smaller increments. Real usage showed the agent's underscoping instinct is the bigger failure mode. The section now defaults to continuation -- and documents its own reversal, because a workflow repo that only ships rules that survived unchanged is lying by omission.
- **Mid-Session Hygiene** -- new CLAUDE.md section: `/rewind` over appended corrections, `/clear` at task-type boundaries, steered `/compact` at ~60% instead of riding into auto-compaction, and diagnose-before-abandoning for off-track sessions.
- **16 new guides** -- including hook self-testing, verify-before-deploy, data-before-code, subagent severity calibration, prose de-AI-ism, native HTML/CSS charts, and pre-publish critical response. Several encode rules promoted only after the same failure was sighted twice or more in real sessions.
- **4 new skills** -- `/distill` (extract rules from your corrections), `/sessions` (find/resume past sessions), `/check-resolvable` (audit orphaned config), `/autoresearch` (bounded autonomous optimization). Plus `--council` mode for `/dialectic-review` and a deterministic scope gate in `/plan-task`.
- **Hook bugfix release + test harness.** Two rounds of adversarial review (a solo pass in July, then a full multi-agent dialectic on the v3 diff itself) found the v2 hooks had silent no-op failure modes (bare `python` on python3-only systems), bypasses (chained commands, multi-target `rm -rf`, flag-order variants), and false positives (`git push origin my-feature-branch` matching a `-f` pattern, `git add .gitignore` matching `git add .`). All fixed, with a test harness (`hooks/test-hooks.sh`) covering all 10 hooks, and deploy.sh now verifies post-install that the hooks actually fire rather than failing open silently. The defect lists are honest history: nearly every bug would have been caught by the repo's own doctrine applied to itself — including the second round's finding that the first round's fixes landed in one file but not its siblings.

## Quick Start

**Tier 1: Just the operating model.**
```bash
cp CLAUDE.md ~/.claude/CLAUDE.md   # back up any existing ~/.claude/CLAUDE.md first
```
Edit the `Platform Notes` and `Interaction Style` sections to match your setup. This single file changes how Claude approaches every task. One caveat: this CLAUDE.md is written for the full install. On its own, its skill references (`/dialectic-review` etc.), its ~25 situational-guide pointers, and the RESOLVER.md routing mandate all point at files you won't have — the Decision Quality Gates have an explicit no-skills fallback, but the guide pointers will just be dead references Claude learns to skip. Tier 1 is a preview of the operating model, not a working subset; the working system is Tier 2.

**Tier 2: Full install (recommended).**
```bash
git clone https://github.com/griffinhilly/claude-code-synthesis /tmp/claude-workflow
bash /tmp/claude-workflow/deploy.sh
```
`deploy.sh` copies `CLAUDE.md`, `RESOLVER.md`, `skills/`, `commands/`, `hooks/`, `guides/`, and `tools/` into `~/.claude/`, backs up any of your files it would overwrite (to `~/.claude/.deploy-backup-<timestamp>/`), and — critically — registers the hooks in `~/.claude/settings.json`. Hooks only fire if registered there; copying the files alone does nothing. It asks before overwriting an existing CLAUDE.md, and if you already have a settings.json it prints the hook block for you to merge by hand.

Prefer manual installation? Copy the five directories the same way (`mkdir -p ~/.claude/skills && cp -r /tmp/claude-workflow/skills/* ~/.claude/skills/`, and likewise for `commands`, `hooks`, `guides`, `tools`), then register the hooks in `~/.claude/settings.json` using the template inside `deploy.sh`.

**Tier 3: Let Claude do it.**
Tell Claude Code: *"Clone https://github.com/griffinhilly/claude-code-synthesis and set up my config based on it."*

**New to all of this? Start with three.** After installing, use just `/plan-task`, `/dialectic-review`, and `/wrapup` for your first week, and add more as the workflow proves itself. (Our own usage log says those — plus the doctrine in CLAUDE.md — carry most of the value; see [What Actually Gets Used](#what-actually-gets-used).) The full set below is a menu, not a curriculum.

## What's In Here

### `CLAUDE.md` -- The Operating Model

The behavioral contract that governs every session. Defines leverage doctrine (human decides, Claude executes), plan-first protocol, scope discipline, agent principles, dialectic reviews, implementation behavior, mid-session hygiene, security safeguards, the COMP documentation system, and workflow evolution rules. See the [Key Ideas](#key-ideas-worth-highlighting) section below for highlights.

### `RESOLVER.md` -- The Routing Table

Task descriptions → skill invocations; content types → filing destinations. Consulted before invoking a skill on an ambiguous task or writing any cross-project memory. Also holds the when-to-make-a-new-skill checklist and the ≥2-sightings promotion gate that keeps single-occurrence "lessons" from accumulating as permanent doctrine.

### `skills/` -- 23 Slash Commands

Skills live in `skills/<name>/SKILL.md` directories (installed to `~/.claude/skills/`) and encode multi-step workflows as single invocations. They range from lightweight wrappers (brainstorm, premortem) to complex multi-agent protocols (dialectic-review, debug, bug-hunt).

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
| `/dialectic-review` | Multi-agent adversarial analysis. 5 modes: review, ideate, tradeoff, premortem, council (5 distinct advisor biases + anonymous peer review + chairman synthesis). Configurable agents, expert lenses, and optional hostile auditor (`--audit`). |
| `/bug-hunt` | Three-agent adversarial bug finder. Hunter overclaims, Skeptic disproves, Referee arbitrates. Scoring incentives force each role to behave honestly. |
| `/brainstorm` | Generate a wide field of ideas, then pressure-test them. Five generators diverge, challengers prune, synthesizers rank what survives. |
| `/premortem` | Assume the plan failed, then explain why. Pessimists diagnose failure, optimists rebut, a risk assessor weighs which failures are real. |
| `/red-team` | Adversarial stress-test with hostile auditor. Critics attack, defender rebuts, referee judges, then a 4th agent attacks the synthesis itself. `--audit` on by default. |
| `/tradeoff` | Compare 2+ options with dedicated advocates, counter-advocates who challenge every position, and a decisive referee. |
| `/socrates` | Socratic questioning to stress-test a philosophical framework or thesis. |
| `/distill` | Diff an agent draft against the user-corrected final, extract patterns from the corrections, propose candidate rules. The manual form of the self-improving-skill loop. |
| `/sessions` | List recent sessions with IDs, descriptions, and turn counts. For finding and resuming past or crashed sessions. |
| `/check-resolvable` | Audit `~/.claude/` for orphans — skills, guides, and tools that exist on disk but are unreachable from CLAUDE.md / RESOLVER.md. |
| `/autoresearch` | Bounded autonomous optimization loop: numeric eval + wall-clock budget + git-branch commits + keep-or-revert. Agent iterates on code; human iterates on the prompt. |

### `commands/` -- 7 Workflow Commands

Commands are user-invocable slash commands that handle session lifecycle and prompt formatting. Unlike skills (which are task-specific), commands are workflow infrastructure -- session start/end, commit preparation, plan review, context pruning.

| Command | What It Does |
|---------|-------------|
| `/start` | Session kickoff. Loads COMP files, presents status dashboard, micro-plans the session. |
| `/prompt` | Converts informal/dictated ideas into structured prompts, then executes. |
| `/prompt-only` | Same as `/prompt` but outputs the formatted prompt without executing. |
| `/prompt-refine` | Audits an existing prompt against quality checklists. |
| `/review-plan` | Stress-tests a plan with expert critique and Red/Yellow/Green findings. |
| `/prune` | Audit and trim auto-loaded files (CLAUDE.md, MEMORY.md) for context bloat. |
| `/overnight` | Set up overnight autonomous batch runs with retry and checkpoint logic. |

### `hooks/` -- 10 Event Hooks

| Hook | Trigger | What It Does |
|------|---------|-------------|
| `warn-destructive.sh` | PreToolUse (Bash) | Blocks `rm -rf`, `DROP TABLE`, `git push --force`, and similar destructive commands |
| `check-staged-secrets.sh` | PreToolUse (Bash) | Scans staged files for credentials before `git commit` |
| `block-secret-bash.sh` | PreToolUse (Bash) | Blocks `cat`, `head`, `tail` on known secret file patterns |
| `block-secret-reads.sh` | PreToolUse (Read) | Blocks the Read tool on `.env`, credential, and key files |
| `log-skill-usage.sh` | PreToolUse (Skill) | Tracks skill invocations with session IDs to a log file for usage analytics |
| `post-compact-reminder.sh` | PostCompact | Re-injects session context and Decision Quality Gates after compaction |
| `epistemic-guard.sh` | PostToolUse (Write/Edit) | Non-blocking notice to the model when written content contains unverified epistemic claims ("should work", "probably fine") |
| `log-unwrapped-session.sh` | SessionEnd | Flags sessions that end with a dirty git tree (any git repo outside `$HOME` itself), so the next session can reconcile unrecorded work |
| `warn-skill-md-too-long.sh` | PostToolUse (Write/Edit) | Non-blocking notice when a SKILL.md exceeds 150 lines — skills should stay lean, with depth in referenced files |
| `check-new-file-index.sh` | PostToolUse (Write) | Non-blocking reminder to update the relevant index when a new file is created |

Every hook is covered by `hooks/test-hooks.sh`, a harness that feeds each of the 10 hooks the same JSON the Claude Code harness would send and asserts the exact allow/block/notice exit code — including regression cases for every bypass and false positive found in review. Run it after any hook edit (see `guides/hook-self-test.md`). Note the delivery mechanics it encodes: on PreToolUse/PostToolUse, exit-0 output goes only to the debug log; a warning only reaches the model via PostToolUse exit 2 (non-blocking notice), which is how the three reminder hooks work. And know the failure mode: if no working `python3`/`python` is on PATH, the hooks fail OPEN — `deploy.sh` checks for this at install time.

### `tools/` -- 7 Utilities

| Tool | What It Does |
|------|-------------|
| `session-search.py` | Cross-session keyword search over conversation history. Supports `--project`, `--days`, `--role`, `--max` filters. |
| `skill-usage-report.py` | Skill usage analytics: invocation counts, trends, dead skill detection. Reads the log produced by `log-skill-usage.sh`. |
| `check-resolvable.py` | Deterministic reachability scan: finds skills, guides, and tools unreachable from CLAUDE.md / RESOLVER.md. Backs the `/check-resolvable` skill. |
| `skill-trigger-evals.py` | Eval harness for skill routing: checks that test-case task descriptions resolve to real skills (cases in `skill-trigger-evals.jsonl`). |
| `mock-finder.py` | Scans for stub/TODO/placeholder code debt an agent left behind. |
| `heartbeat.py` | Silent-by-default monitoring: parses a `~/.claude/HEARTBEAT.md` checklist you write (format documented in the script header), emits only anomalies. |
| `archive-transcripts.sh` | Idempotent daily archival of session transcripts before Claude Code's retention window prunes them. |

### `guides/` -- 29 On-Demand Reference Docs

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
| `event-driven-agents.md` | Bash pre-check gates, event-driven agent invocation, autonomous loop safety |
| `claude-code-primitives.md` | The session-management moves the workflow depends on: `/rewind`, `/clear`, steered `/compact`, `!` shell prefix |
| `hook-self-test.md` | Testing hook scripts before shipping them (feed JSON, assert exit codes) |
| `verify-before-deploy.md` | Verifying a batch of agent-generated content before the next workflow step |
| `data-before-code.md` | When generated-content skew means the upstream data set is the gap, not the code |
| `subagent-severity-judgments.md` | Calibrating subagent "ship-blocker" / "P0" severity claims before acting on them |
| `calibration-equivocation.md` | The "calibrate/tune/validate" equivocation trap in Bayesian / IRT / econometric plans |
| `pre-commit-rule-audit.md` | Auditing decision rules pre-committed on forthcoming data (bins, reversal conditions, defaults) |
| `pre-publish-critical-response.md` | Adversarial read before publishing for an external audience |
| `prose-de-aiism.md` | Removing LLM voice from user-facing prose, as a named final pass |
| `native-html-css-charts.md` | Professional-looking charts via HTML/CSS + headless Chrome instead of matplotlib |
| `chart-qa.md` | Matplotlib overlap/legibility QA before shipping a chart |
| `image-asset-audit.md` | Measuring assets and rendered geometry instead of eyeballing layout |
| `headless-chrome-qa.md` | Verifying web UI headlessly when a browser extension isn't available |
| `mcp-windows-debugging.md` | MCP servers on Windows that won't start or connect-but-sit-inert |
| `windows-paths.md` | Constructing file paths with usernames and system directories on Windows |
| `unavailable-source-fallback.md` | Archive-snapshot fallback (with mandatory validation) when a data host is down or throttling |
| `claude-code-features.md` | Superseded — a cautionary stub about why hand-mirroring a fast-moving product's feature list fails |

### `examples/data-pipeline/` -- Working Example

A complete data enrichment pipeline demonstrating these patterns in action: step-based pipeline runner with dry-run and skip flags, LLM batch categorization with taxonomy normalization, verify-and-merge cycles, and semantic search over enriched data.

## What Actually Gets Used

This repo ships a `log-skill-usage.sh` hook precisely so this question has an answer. Four months of logged invocations (165 entries, April–July 2026) from the config this repo is a snapshot of:

| Tier | Skills | Share |
|------|--------|-------|
| The ritual | `/wrapup` (~70), `/dialectic-review` (~46) | ~70% of all invocations |
| Regular | `/plan-task` (~10), `/prune`, `/comp` | ~10% |
| Occasional | `/research`, `/finalize`, `/retro`, `/schedule`, and Claude Code built-ins | ~20% |
| Rarely/never logged | `/bug-hunt`, `/red-team`, `/brainstorm`, `/premortem`, `/tradeoff`, `/socrates`, `/ship`, `/verify`, `/implement`, `/learn`, `/debug` | ~0% |

Honest readings of that last row:

1. **Session lifecycle + adversarial review are the workflow.** The two dominant skills are the ritual bookend (`/wrapup` compounds knowledge into COMP files every session) and the decision stress-tester. If you install only two skills, install those.
2. **Wrappers get absorbed.** `/premortem`, `/tradeoff`, `/red-team`, `/brainstorm` are thin wrappers around `/dialectic-review` modes — usage flows to the parent skill. That's the design working, not failing.
3. **Some zeros are real.** `/ship`, `/verify`, `/implement`, `/learn` genuinely get skipped: their behaviors partially migrated into CLAUDE.md doctrine (verify-before-done, operationalize-every-fix) that fires without explicit invocation. A skill whose content graduates into always-on doctrine is a success that looks like a failure in the log.
4. **Measurement has holes.** The hook only logs invocations routed through the Skill tool; auto-triggered skills and some earlier months aren't captured. Treat the log as strong signal, not census.

The meta-lesson we'd offer anyone building a big config: **instrument first, prune second.** We'd have guessed wrong about half of this table.

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

**The promotion gate.** A lesson observed once goes to `candidate-rules.md`, not to permanent doctrine. Only a second real sighting promotes it (bug-classes, security items, and explicit user requests skip the gate). This is the difference between a CLAUDE.md that compounds and one that silts up with rules that never fire. Several v3 rules carry their promotion history inline — "promoted after the second real incident of X" — as evidence they earned their place.

**Latent vs deterministic.** Every workflow step is either model judgment (synthesis, fuzzy classification) or code (counting, joining, thresholding). Putting deterministic work in latent space is the most common agent-design mistake. Wherever a spec names a number, that step should be code. RESOLVER.md itself is this principle applied to skill routing.

**Mid-session hygiene.** Context is a resource you manage mid-flight, not just at session boundaries: `/rewind` failed approaches out of context instead of appending corrections, `/clear` at task-type boundaries, steer `/compact` manually at ~60% rather than riding into auto-compaction at ~90%.

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

Not every session uses all 9 steps. A quick bug fix might be `/start`, `/debug`, `/ship`, `/wrapup`. A planning session might be `/start`, `/plan-task`, `/review-plan`, `/wrapup`. Use judgment — and note that [What Actually Gets Used](#what-actually-gets-used) shows our own sessions rarely invoke steps 4-7 explicitly anymore; their checks migrated into always-on CLAUDE.md doctrine. The 9 steps are the full ceremony; the lived workflow is closer to steps 1-2, doctrine doing 4-7 implicitly, then 8.

## Updating and Uninstalling

**Update:** pull the repo and re-run `deploy.sh`. It overwrites same-named shipped files (so customize under different filenames) and leaves everything else alone; it asks before touching your CLAUDE.md.

**Uninstall:** delete the installed files — the skills, commands, guides, hooks, and tools listed in the tables above — from `~/.claude/`, and remove the hook entries from `~/.claude/settings.json`.

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
- **@danpeguine** -- Their implementation of [@systematicls's method](https://x.com/danpeguine/status/2029268229030285589) using Hunter, Skeptic, and Referee agents was the direct inspiration for the dialectic review pattern and the `/bug-hunt` skill.
- **Kyle Mathews** ([@kylemathews](https://x.com/kylemathews)) -- His [Hegelian dialectic skill](https://github.com/KyleAMathews/hegelian-dialectic-skill) with its hostile auditor phase (Phase 6 validation) inspired the `--audit` flag in `/dialectic-review`.
- **Riley Ralmuto** ([@RileyRalmuto](https://x.com/RileyRalmuto)) -- Their [polyclaude plugin](https://github.com/Riley-Coyote/polyclaude) with 6 named perspectives (including Temporal and User Advocate) informed the recommended `--lens` values.
- **Danielle Fong** ([@DanielleFong](https://x.com/DanielleFong)) -- Her concept of an [epistemic claims hook](https://x.com/DanielleFong/status/2038061587752505711) that catches unverified assertions inspired `epistemic-guard.sh`.

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
- **@elvissun** -- Their [bash pre-check gate pattern](https://x.com/elvissun/status/2028671336219107687) (bash checks preconditions, only invokes the LLM when action is needed) achieving ~95% token reduction directly shaped `guides/event-driven-agents.md`.
- **@affaan-m** -- Their [everything-claude-code](https://github.com/affaan-m/everything-claude-code) repo (27 agents, 64 skills) contributed the loop-operator stall detection pattern documented in the event-driven agents guide.

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
