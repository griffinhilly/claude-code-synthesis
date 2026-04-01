# Claude Code Skill Frameworks: Comparison Guide

A deep comparison of the three most popular Claude Code skill frameworks, with recommendations for what to adopt based on your workflow.

These three repos represent fundamentally different philosophies for getting the most out of Claude Code. Each has strengths worth adopting, and none is universally best. This guide maps their patterns, traces what this repo adopted from each, and recommends which to reach for based on your workflow.

## Quick Comparison

| Dimension | gstack | Superpowers | Compound Engineering |
|-----------|--------|-------------|---------------------|
| **Author** | Garry Tan | Jesse Vincent (obra) | Every Inc |
| **Repo** | [garrytan/gstack](https://github.com/garrytan/gstack) | [obra/superpowers](https://github.com/obra/superpowers) | [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) |
| **Stars** | 57K+ | 57K+ | 12K+ |
| **Philosophy** | "Virtual engineering team" | "Methodology-as-code" | "Knowledge compounds" |
| **Skill count** | 31 | 14 | 41 |
| **Runtime** | Bun/Node.js | Shell (59%) + JavaScript (30%) | TypeScript (79%) + Python + Shell |
| **Primary strength** | Browser automation + parallel execution | Disciplined TDD + debugging methodology | Review sophistication + knowledge capture |
| **Complexity to adopt** | High (Bun, Chromium, Supabase) | Low (shell + JS, no infrastructure) | Medium (TypeScript, JSON task system) |
| **Browser automation** | Yes (persistent daemon with ref system) | No | Yes (agent-browser) |
| **Parallel execution** | Conductor (10-15 concurrent sprints) | Parallel agent dispatch (same session) | Swarm orchestration (persistent teams) |
| **Review system** | Cross-model (Claude + OpenAI) | Two-stage (spec compliance, then quality) | 18 reviewers, confidence-gated |
| **Knowledge persistence** | `learn` skill | Design docs in `docs/superpowers/specs/` | `docs/solutions/` with YAML + dedup + refresh |
| **Multi-platform support** | Codex, Factory Droid | Claude Code, Cursor, Codex, Gemini CLI, Copilot | 10+ platforms via Bun CLI converter |
| **Best for** | Full-stack product teams shipping fast | Solo developers wanting rigor | Teams building institutional knowledge |

---

## gstack

**Repo:** [github.com/garrytan/gstack](https://github.com/garrytan/gstack)

gstack models Claude Code as a virtual engineering team. Each skill represents a role (CEO, engineer, QA, security officer, DevOps), and the workflow mirrors how a well-staffed product team operates: product discovery, design exploration, parallel sprints, CI/CD, post-deploy monitoring.

### Strengths

**Persistent Browser Daemon.** Instead of cold-starting Chromium per command, gstack runs a long-lived Bun HTTP server talking to Chromium via CDP. State file (`.gstack/browse.json`) with PID/port/token. Random port selection (10000-60000) enables concurrent workspaces. Sub-second latency after first launch (100-200ms vs 3-5s cold start).

**The Ref System.** Elements addressed via refs (`@e1`, `@c1`) mapped to Playwright accessibility-tree Locators, not CSS selectors. This bypasses CSP restrictions, Shadow DOM, and framework hydration issues. Staleness detection via 5ms `count()` check. Materially better than coordinate-based or selector-based approaches.

**Conductor for Parallel Sprints.** `conductor.json` configures 10-15 concurrent agents, each on its own branch/workspace/Chromium instance. The structured workflow (think-plan-build-review-test-ship) is what makes parallelism work rather than chaos.

**Cross-Model Review.** The `review` + `codex` skills run Claude and OpenAI independently against the same code. Different models catch different failure modes. This is particularly valuable for reducing confirmation bias.

**SKILL.md Template Generation.** Templates (`.tmpl` files) are the source of truth. Code metadata is injected at build time. Skills are "prompt documents, not shell scripts" -- each code block executes independently, with natural language for conditionals. This prevents docs from drifting from behavior.

**"Boil the Lake" Philosophy.** When AI makes completeness nearly free, always choose the complete implementation. Rejects the "ship the shortcut" mindset when thoroughness costs nearly nothing in AI-assisted workflows.

### Best Patterns to Adopt

1. **Persistent browser daemon architecture** -- if you do any browser automation, the daemon + ref system is the state of the art. Worth the Bun dependency.
2. **Cross-model review** -- for high-stakes code, run through two models independently. The disagreements are the most informative part.
3. **Template-generated skill docs** -- eliminates drift between what a skill says and what it does. Scales well past 10+ skills.
4. **The three-layer knowledge hierarchy** -- before building anything unfamiliar: (1) search for existing patterns, (2) check current trends (scrutinize for hype), (3) reason from first principles.
5. **Three-tier E2E testing** -- Tier 1: free parse validation (<5s). Tier 2: real Claude E2E runs (~$3.85). Tier 3: LLM-as-judge scoring (~$0.15). Only Tier 1 runs on every test; Tiers 2-3 gated behind `EVALS=1`.

### When to Use

- You are building and shipping product (web apps, SaaS, full-stack)
- You need browser automation (testing, scraping, interaction)
- Your workload has many independent features that benefit from parallel execution
- You are comfortable with Bun/Node.js infrastructure
- Your team is large enough that role-based specialization pays off

---

## Superpowers

**Repo:** [github.com/obra/superpowers](https://github.com/obra/superpowers)

Superpowers is methodology-as-code. It has 14 skills and zero infrastructure requirements. Every skill encodes a rigorous engineering discipline -- TDD, systematic debugging, verification, code review -- and enforces it through hard gates and red flag language detection. If gstack gives you a team, Superpowers gives you the engineering culture that makes a team effective.

### Strengths

**Psychology-Based Agent Persuasion.** Superpowers applies Robert Cialdini's persuasion principles (from "Influence") to LLM behavior. Commitment/consistency, social proof, and authority framing are academically verified to change Claude's code quality. This is genuinely novel -- treating skill files as persuasive documents, not just instruction sets.

**Hard Gates with Red Flag Language Detection.** The `verification-before-completion` skill treats optimistic language ("should," "probably," "Great!," "Perfect!," "Done!") as red flags that trigger mandatory full verification. This directly counters LLM sycophancy at the skill level.

**Three-Fix Escalation Rule.** In `systematic-debugging`: if three fixes have failed, STOP. Don't try a fourth. The architecture itself is probably wrong. Escalate to discussion. This prevents the infinite fix-retry loop that plagues agentic coding.

**Two-Stage Review Pipeline.** `subagent-driven-development` mandates spec compliance review BEFORE code quality review. Never reverse the order. Spec compliance must be green before quality review even begins. This prevents polishing code that does not meet requirements.

**Model Selection by Task Complexity.** Explicit guidance: cheap/fast models for mechanical isolated tasks (1-2 files), standard models for integration work (multi-file), most capable models for architecture/design/review. Token-cost consciousness baked into the methodology.

**Design Doc as Hard Gate.** No implementation skill can be invoked until a design document is written and user-approved. The brainstorming process saves specs to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`.

**Subagent Context Discipline.** "Never make subagents read plan files -- provide full text instead." Each subagent gets precisely crafted context, not session history. File reading overhead eliminated.

### Best Patterns to Adopt

1. **Red flag language detection** -- add "should work," "probably fine," "Done!," "seems to" as triggers for mandatory re-verification in any verification skill.
2. **Three-fix escalation rule** -- hard-stop after 3 failed fix attempts. Architectural problems masquerading as local bugs waste unbounded time.
3. **One question per message in brainstorming** -- don't overwhelm the human. Single questions, preferably multiple choice over open-ended.
4. **Subagent context discipline** -- paste relevant content into subagent prompts. Don't reference files the subagent would need to find and read.
5. **Phase-gated debugging** -- evidence before hypotheses before reproduction before fix. Each gate requires a written artifact.
6. **Psychology-informed skill writing** -- frame skill instructions using commitment/consistency and authority framing, not just imperative commands.

### When to Use

- You are a solo developer or small team wanting engineering discipline
- You value correctness over speed
- Your workflow does not require browser automation or heavy infrastructure
- You want to adopt patterns incrementally (low barrier to entry)
- You are building something where bugs are expensive (data pipelines, financial, health)

---

## Compound Engineering

**Repo:** [github.com/EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)

Compound Engineering's core insight is that solved problems should make future problems easier. The `ce-compound` skill captures knowledge from every fix and feature into structured solution docs with YAML frontmatter, overlap detection, and automatic refresh triggers. It is the only framework that treats institutional memory as a first-class engineering concern.

### Strengths

**Knowledge Compounding (`ce-compound`).** Three parallel subagents (Context Analyzer, Solution Extractor, Related Docs Finder) capture each solved problem. Overlap scored across 5 dimensions with a decision tree: High overlap = update existing doc, Moderate = create new + flag for consolidation, Low = create new. Phase 2.5 checks whether existing docs need refresh.

**Confidence-Gated Review (`ce-review`).** 6 always-on reviewers + 10 conditional reviewers + 2 CE-specific reviewers. Findings below 60% confidence are suppressed -- except P0 (critical) findings, which survive at 50%+ ("critical-but-uncertain issues must surface"). Cross-reviewer agreement boosts confidence by 0.10. Duplicates merged by fingerprint (file + line bucket +/- 3 + normalized title).

**Four Mutation Routes.** Review findings classified into `safe_auto` (applied without asking), `gated_auto` (requires approval), `manual` (handed off as work item), `advisory` (report only). More nuanced than binary fix/don't-fix.

**Plan Confidence Deepening (`ce-plan`).** Plans score confidence gaps per section using checklist-first, risk-weighted scoring. Selects top 2-5 weak sections, dispatches 1-3 research agents per section (max 8 total), synthesizes findings back. Auto mode integrates directly; interactive mode lets user accept/reject each finding.

**Track-Aware Documentation.** Solutions classified by track (bug vs knowledge) with different output structures. Bug track: Problem, Symptoms, What Didn't Work, Solution, Why This Works, Prevention. Knowledge track: Context, Guidance, Why This Matters, When to Apply, Examples.

**Discoverability Check.** After writing a solution doc, `ce-compound` verifies that agent instruction files (AGENTS.md, CLAUDE.md) actually surface the knowledge store. Knowledge that agents cannot find is worthless.

**80/20 Time Allocation.** The methodology explicitly allocates 80% of time to planning and review, 20% to execution. Enforced by the workflow structure, not just advice.

**Multi-Platform CLI.** Converts plugins to 10+ formats: Codex, Factory Droid, Gemini CLI, GitHub Copilot, Cursor, Kiro, Windsurf, OpenClaw, Qwen Code. If you work across multiple AI coding tools, this is a significant advantage.

### Best Patterns to Adopt

1. **Structured knowledge capture with overlap detection** -- don't just write docs. Score overlap against existing docs and decide: update, create new, or consolidate.
2. **Confidence-gated review findings** -- suppress low-confidence noise while preserving high-severity/low-confidence signals. Cross-reviewer boosting rewards consensus.
3. **Four mutation routes** -- classify review findings by action type rather than just severity. Some fixes are safe to auto-apply; some need human judgment.
4. **Confidence-scored planning** -- score confidence per plan section and dispatch targeted research to weak areas before implementation.
5. **Discoverability checks** -- after writing knowledge docs, verify they are actually findable by agents. A doc that exists but is not referenced from agent instructions is invisible.
6. **Track-aware documentation templates** -- different structures for "what went wrong" vs "what we learned."

### When to Use

- Your team ships features across many sessions and needs accumulated knowledge
- You want review sophistication beyond pass/fail
- You work across multiple AI coding tools (Codex, Cursor, Gemini CLI, etc.)
- Your codebase has recurring patterns where past solutions inform future ones
- You are willing to invest in infrastructure (TypeScript, JSON task system)

---

## What This Repo Adopted

This repo (claude-code-synthesis) draws from all three frameworks but most heavily from Superpowers for methodology and Compound Engineering for knowledge capture. Here is the mapping from repo artifacts back to source frameworks.

### From Superpowers

| This Repo | Superpowers Pattern | Adaptation |
|-----------|-------------------|------------|
| **`/debug` skill** — 4-phase protocol (Observe, Hypothesize, Reproduce, Fix) with hard gates | `systematic-debugging` — 4-phase root cause investigation | Near-direct adoption. Added pipeline-specific diagnostic layer (`pipeline-diagnostic.md`) and integration with `/learn gotcha` for knowledge capture after fixes. |
| **`/verify` skill** — Red flag language detection ("should work," "Done!," "probably fine") | `verification-before-completion` — 5-gate proof requirement with red flag language | Adopted the language detection concept. Simplified from 5 gates to a checklist-based approach with type-specific checks (data, implementation, analysis, file output). |
| **Three-fix escalation rule** in `/debug` and `/verify` | `systematic-debugging` three-fix escalation | Direct adoption. Present in both `/debug` (Phase 4 escalation) and `/verify` (verification failure escalation). |
| **`/plan-task` skill** — design doc as hard gate, no implementation until approved | `brainstorming` + `writing-plans` — design doc required before implementation | Adopted the principle. Added structured decomposition tables, risk checklists, and iterative polishing passes. |
| **Model selection guidance** in `delegation-templates.md` | Model selection by task complexity | Formalized as a table: Sonnet for execution, Opus for judgment, Haiku for volume. Applied to all 7 delegation templates. |
| **Subagent context discipline** in `delegation-templates.md` | "Never make subagents read plan files" | Adopted as a structural rule: every delegation template includes pasted context, not file references. The orchestrator checklist enforces "context is pasted, not referenced." |
| **One question per message** reflected in interaction style | `brainstorming` single-question-per-interaction rule | Influenced the "keep planning brief, start executing" interaction style, though not formalized as a skill-level rule. |

### From Compound Engineering

| This Repo | Compound Engineering Pattern | Adaptation |
|-----------|----------------------------|------------|
| **`/learn` skill** — structured JSONL capture with types (gotcha, pattern, decision, bug-fix) | `ce-compound` — knowledge compounding with YAML frontmatter and overlap detection | Simplified version. Uses JSONL instead of YAML-frontmattered markdown. Supports cross-project search. Does not yet implement overlap detection or automatic refresh triggers. |
| **COMP system** (CLAUDE.md + ORIENT.md + MEMORY.md + PLAN.md) | Track-aware documentation + discoverability checks | Independent evolution toward a similar goal. The COMP system separates by audience and change frequency; CE separates by track (bug vs knowledge). The discoverability concept influenced the COMP system's emphasis on agent-first artifact design. |
| **`/review` skill** — fresh-context subagent with structured output | `ce-review` — 18 reviewers with confidence gating | Much simpler: single reviewer with dimension-based checklists. Does not implement confidence scoring, cross-reviewer boosting, or conditional reviewer activation. |
| **`/plan-task` confidence awareness** in polishing guide | `ce-plan` — confidence-scored planning with auto-deepening | Partial adoption. The polishing guide asks "where is confidence lowest?" but does not formalize numeric scoring or automated research dispatch to weak sections. |
| **`/wrapup` discoverability check** — bloat check + skill health | Discoverability check after writing solution docs | Adapted as skill health checking: are skills firing correctly? Is knowledge findable? Less formal than CE's automated verification. |
| **`/retro` skill** — cumulative learning with deduplication | Cumulative knowledge with overlap detection and refresh triggers | Adopted the principle of cumulative learning. The retro turns patterns into feedback memories, CLAUDE.md rules, or new skills. Does not implement automated deduplication or reinforcement counting. |

### From gstack

| This Repo | gstack Pattern | Adaptation |
|-----------|---------------|------------|
| **`/ship` skill** — pre-commit readiness check | `ship` — PR + CI pipeline | Simplified to pre-commit scope: test check, COMP freshness, staged file review, commit message drafting. Does not include PR creation or CI integration. |
| **`/dialectic-review` skill** — multi-agent opposing review | `review` + `codex` cross-model pattern | Generalized. Instead of cross-model review, uses cross-role review: Critics vs Defenders vs Referees. Extended to 4 modes (review, ideation, tradeoff, premortem). The core insight -- different perspectives catch different failures -- is the same. |
| **Plan-exit review** concept in `/review` escalation | `plan-ceo-review` + `plan-eng-review` | Adapted as the `/review` escalation check: significant reviews suggest `/dialectic-review` for adversarial depth. Not a separate skill, but an escalation path. |
| **`/retro` skill** — periodic retrospective | `retro` — weekly usage analytics | Adapted from analytics to methodology review. The gstack retro is quantitative (usage metrics); this repo's retro is qualitative (what worked, what failed, patterns, suggestions). |

### Original to This Repo

| Artifact | What It Does | Why It's Original |
|----------|-------------|-------------------|
| **`/dialectic-review` 4-mode framework** | Unified dialectic process with `review`, `ideate`, `tradeoff`, and `premortem` modes | None of the three frameworks have a single skill that supports all four dialectic modes with configurable agent counts and expert lenses. |
| **`/comp` skill** | Creates/updates all 4 COMP files for any directory | The 4-file COMP system (behavioral contract / human orientation / accumulated knowledge / roadmap) is a distinct documentation architecture. |
| **`/finalize` skill** | Lightweight end-of-session COMP update | Distinct from `/wrapup` (full session closer). Quick COMP refresh without the review, health check, and bloat audit. |
| **Delegation templates** (7 agent types) | Structured prompt templates with report formats and orchestrator checklist | None of the three frameworks publish reusable delegation templates at this granularity. The structural discipline rules (mandatory report format, assumed verification, escalation as safe default) are original. |
| **Progressive disclosure via situational guides** | Lean CLAUDE.md with trigger rules pointing to on-demand guides | All three frameworks load their full skill set. This repo's approach -- lean always-loaded context with guides loaded only when triggered -- is a distinct architectural choice for context efficiency. |
| **Security hooks** (block-secret-bash, block-secret-reads, check-staged-secrets, warn-destructive) | PreToolUse hooks that block credential exposure and warn on destructive commands | gstack has destructive command interception; this repo extends it to credential exposure in both Bash output and file reads, plus pre-commit secret scanning. |

---

## Recommendations by Workflow Type

### Solo developer, data-heavy (analytics, ML, pipelines)

**Start with:** Superpowers patterns adopted by this repo (already packaged here).

**Key skills:**
- `/debug` with its 4-phase protocol -- data pipeline bugs are the most common source of wasted time, and the "evidence before fix" discipline prevents the retry loop
- `/verify` after every pipeline step -- silent failures (unfetched data, stale counts, encoding issues) propagate across stages
- `/learn` for cross-project gotchas -- data tooling has idiosyncratic behaviors (BOM encoding, psycopg2 binary mode, pandas datetime parsing) that recur across projects
- Three-fix escalation rule -- when a data transform keeps failing, the schema or data model is usually wrong, not the code

**Skip:** gstack's browser daemon (no web UI to test), Compound Engineering's swarm orchestration (pipelines are sequential, not parallel), gstack's Conductor (features are not independent).

**Consider later:** Compound Engineering's track-aware documentation (bug track vs knowledge track) becomes valuable once you have 50+ learnings and need structure beyond flat JSONL.

### Product team shipping fast (SaaS, web apps, full-stack)

**Start with:** gstack for execution speed, Superpowers verification to catch quality issues.

**Key skills:**
- gstack's Conductor for parallel sprints -- 10-15 concurrent agents, each on its own branch, is transformative for teams with many independent features
- gstack's browser daemon + ref system -- sub-second browser automation for testing
- gstack's `review` + `codex` cross-model review -- different models catch different bugs
- Superpowers' red flag language detection -- add to your verification step to catch sycophantic completion claims
- Superpowers' two-stage review -- spec compliance before code quality

**Skip:** Compound Engineering's 80/20 planning/execution split (too slow for fast-shipping teams), elaborate knowledge compounding (diminishing returns if your product changes faster than your docs).

**Consider later:** Compound Engineering's confidence-gated review when your codebase stabilizes and review noise becomes a problem.

### Team building institutional knowledge (long-lived codebases, onboarding)

**Start with:** Compound Engineering for knowledge capture, Superpowers for methodology.

**Key skills:**
- Compound Engineering's `ce-compound` -- structured knowledge capture with overlap detection is the core value proposition for teams where people leave and join
- Compound Engineering's track-aware documentation -- bug track for "what went wrong," knowledge track for "how we do things here"
- Compound Engineering's discoverability check -- knowledge that agents cannot find is wasted effort
- Superpowers' design-doc-as-hard-gate -- prevents implementation of poorly specified features
- This repo's COMP system -- 4-file project documentation with clear audience and purpose separation

**Skip:** gstack's browser daemon (unless you need it), gstack's Conductor (parallel execution is secondary to knowledge quality for this use case).

**Consider later:** gstack's SKILL.md template generation when your skill count exceeds 15-20 and documentation drift becomes a real risk.

### Hybrid approach (recommended starting point)

If you are unsure which workflow type fits, adopt in this order:

1. **This repo's CLAUDE.md + COMP system** -- foundational operating model and documentation structure. Zero infrastructure required.
2. **Superpowers' methodology patterns** (already adopted here as `/debug`, `/verify`, three-fix escalation) -- engineering discipline that prevents the most common agentic coding failures.
3. **Compound Engineering's `/learn` pattern** (already adopted here) -- start capturing knowledge from day one. Overlap detection and refresh triggers can be added later.
4. **gstack's cross-model review** -- add when you have high-stakes code that justifies the cost of running two models.
5. **Compound Engineering's confidence-gated review** -- add when review noise becomes a problem and you need to suppress low-confidence findings.
6. **gstack's browser daemon** -- add when you need browser automation. Not before.

---

## Sources

- [gstack repo](https://github.com/garrytan/gstack)
- [Superpowers repo](https://github.com/obra/superpowers)
- [Compound Engineering repo](https://github.com/EveryInc/compound-engineering-plugin)
- [Superpowers blog post (Jesse Vincent)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Compound Engineering article (Every.to)](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents)
- [Compound Engineering definitive guide](https://every.to/source-code/compound-engineering-the-definitive-guide)
- [gstack fully explained (YouMind)](https://youmind.com/blog/gstack-garry-tan-claude-code-workflow-guide)
- [Superpowers deep dive (DeepToAI)](https://skills.deeptoai.com/en/docs/development/superpowers-deep-dive)
- [Superpowers TDD enforcement (YUV.AI)](https://yuv.ai/blog/superpowers)
- [Agentic patterns - Compounding Engineering](https://www.agentic-patterns.com/patterns/compounding-engineering-pattern/)
