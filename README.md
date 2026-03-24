# Claude Code Workflow

A complete, opinionated workflow for getting the most out of [Claude Code](https://docs.anthropic.com/en/docs/claude-code). This repo contains the operating model, agent delegation templates, situational guides, and project documentation system I use daily.

**This isn't a tutorial or a library.** It's a working configuration you can copy into your own setup and adapt.

## How to Use This

### Quick: Just grab the operating model
Copy `CLAUDE.md` to `~/.claude/CLAUDE.md` (your global Claude Code instructions). That's the single most impactful file — it changes how Claude approaches every task.

### Full: Adopt the whole workflow
```bash
git clone <this-repo> /tmp/claude-workflow

# Copy the operating model
cp /tmp/claude-workflow/CLAUDE.md ~/.claude/CLAUDE.md

# Copy the guides
cp -r /tmp/claude-workflow/guides ~/.claude/guides

# Edit CLAUDE.md to customize:
#   - Platform Notes section (your OS, Python path, etc.)
#   - Interaction Style section (your working preferences)
#   - Situational Guides paths (if you put guides elsewhere)
```

Or just point Claude at this repo: *"Download this repo and set up my Claude Code config based on it."*

## What's In Here

### `CLAUDE.md` — The Operating Model
The main event. This is a global `CLAUDE.md` that defines:

- **Leverage Doctrine** — Clear division of labor: human does ideation/decisions, Claude does research/execution
- **Plan-First Protocol** — Every task starts with planning. Define objectives, success criteria, and sub-tasks before writing code
- **Scope Discipline** — Push back on over-ambitious plans. Ship small, working things
- **Agent Principles** — When to handle directly vs. delegate to subagents vs. route to MCP. Separation of concerns between research and implementation agents
- **Dialectic Tension** — Use opposing agents (argue FOR vs AGAINST) for important decisions, with a referee to synthesize
- **Implementation Behavior** — Surface assumptions, stop when confused, push back on bad ideas, prefer boring solutions, test-first bug fixing, operationalize every fix
- **Workflow Evolution** — The system improves itself: operationalize learnings into instructions, build skills from recurring patterns, use corrective framing over reminders
- **Security Safeguards** — Explicit confirmation for database mutations, external communications, credential handling
- **The COMP System** — 4-file project documentation structure (see below)

### `guides/` — Situational Guides
Detailed reference docs that Claude loads on-demand (not always-loaded — that's the point). Keeps the main CLAUDE.md lean while having deep knowledge available when needed.

| Guide | When It's Loaded |
|-------|-----------------|
| `delegation-templates.md` | Delegating work to subagents — 7 agent types with prompt templates |
| `shell-rules.md` | Avoiding Claude Code's security scanner false positives |
| `context-efficiency.md` | Sessions feel slow or token usage is high |
| `prefer-apis.md` | Fetching data from websites (API > scraping) |
| `postgres-batching.md` | Exploratory database queries |
| `overnight-runner.md` | Running autonomous batch jobs overnight |
| `skills-reference.md` | Available slash commands and recommended workflow |
| `bookmark-archive.md` | How to build a searchable Twitter/X bookmark archive |

### `examples/data-pipeline/` — Working Example
A complete data enrichment pipeline showing these patterns in action:
- Step-based pipeline runner with dry-run, skip flags, and human gate points
- LLM batch categorization with taxonomy normalization and fix maps
- Verify-and-merge cycle for validating LLM output
- Semantic search over enriched data (sentence-transformers)
- COMP files for the project

## The COMP System

Every project maintains 4 files that keep Claude Code effective across sessions:

| File | Purpose | Audience | Updates |
|------|---------|----------|---------|
| **C**LAUDE.md | Behavioral contract — how Claude should work here | Agent | Rare |
| **O**RIENT.md | Orientation — what a human needs to know | Human | When project shape changes |
| **M**EMORY.md | Accumulated knowledge — decisions, gotchas | Agent + Human | Most sessions |
| **P**LAN.md | Direction — roadmap, progress, next steps | Human + Agent | Most sessions |

The key insight: separate *behavioral instructions* (CLAUDE.md) from *human orientation* (ORIENT.md) from *accumulated knowledge* (MEMORY.md) from *direction* (PLAN.md). Each file has a different audience, change frequency, and purpose.

## Key Ideas Worth Highlighting

**Orchestrator-first mindset.** The session agent shouldn't do everything itself. Before any task, it should assess: handle directly, delegate to a subagent, or route to MCP? This is the single biggest lever for productivity with Claude Code.

**Dialectic reviews.** For important decisions, don't ask Claude "what should I do?" Instead, spawn opposing agents — one argues FOR, one argues AGAINST — with a referee to synthesize. This produces dramatically better analysis than asking a single agent for pros and cons.

**Progressive disclosure.** Don't dump everything into CLAUDE.md. Keep it lean with trigger rules ("when X happens, read guide Y"). The guides load on-demand, keeping your always-loaded context small and your token costs low.

**Human gates in pipelines.** Data enrichment workflows aren't fully automatable. Some steps need human judgment (kick off agent runs, review quality, provide auth). Making the interruptible workflow explicit — with named steps, skip flags, and resume points — is better than pretending it's a straight-through pipeline.

**Compaction-safe artifacts.** Claude Code conversations get compressed as they grow. Important outputs (schemas, decisions, data) should be written to files immediately, not left in conversation history where they might get compacted away.

**Operationalize every fix.** When Claude finds and fixes a bug, don't stop there. Write tests that catch that bug *and* the whole class of similar bugs. Check if the same mistake exists elsewhere. If it reveals a gap in your instructions, update CLAUDE.md. Every bug is a learning opportunity — extract the lesson and encode it so it can't recur.

**The virtuous circle.** Use your tools to improve your tools. Study what worked in past sessions, extract the pattern into a skill or guide, apply it to new projects, refine based on results. The workflow improves itself through use — it's a flywheel, not a static configuration.

**Evals before specs.** Define how you'll evaluate success *before* writing the spec. This progression — evals → spec → plan → implement → verify — produces dramatically better outcomes than the more natural plan → implement → "does this look right?"

## Build Your Own Bookmark Archive

The data pipeline example in this repo was originally built to archive and search Twitter/X bookmarks. The attributions section below? Every single source was found by running semantic search over ~2,000 bookmarks — `python search.py "agent orchestration pattern" --top-k 5`.

If you want to do the same thing with your own bookmarks, see **`guides/bookmark-archive.md`** for the full walkthrough: HAR capture → extraction → media download → AI image descriptions → LLM categorization → semantic search. Total cost is ~$1-3 in API credits for ~2,000 bookmarks.

Your bookmarks are a curated signal of what you found valuable. This pipeline turns that signal into a searchable knowledge base.

## Acknowledgments & Influences

This workflow didn't emerge in a vacuum. Most of the ideas here were shaped by things I read, bookmarked, and experimented with. Here's where the concepts come from — roughly mapped to the people and posts that influenced each one.

### Agent Architecture & Orchestration

- **Boris Cherny** ([@bcherny](https://x.com/bcherny)) — Creator of Claude Code. His [tips thread](https://x.com/bcherny/status/2017742741636321619) on how the Claude Code team uses the tool differently than most people was foundational. His insight about separate context windows and test-time compute directly shaped the orchestrator-first and subagent delegation patterns.
- **@systematicls** — Their [reply about context windows](https://x.com/systematicls/status/2031190025833181586) ("aggressively clear them when doing your work, and you can have your own code review agents by building a new context window") crystallized the fresh-eyes-for-review principle.
- **@doodlestein** — Their observation that [the Unix tool approach](https://x.com/doodlestein/status/2000271365816131942) ("focused, composable functional units that can be used in isolation or as part of a larger pipeline") is the best model for AI agents directly influenced how the delegation templates are structured.
- **Simon Willison** ([@simonw](https://x.com/simonw)) — His [Agentic Engineering Patterns](https://x.com/simonw/status/2025990408514523517) guide is the most rigorous public treatment of coding agent best practices. Many of the implementation behavior rules reflect patterns he documented.

### CLAUDE.md & Context Management

- **Todd Saunders** ([@toddsaunders](https://x.com/toddsaunders)) — His insight about [rewriting CLAUDE.md from scratch](https://x.com/toddsaunders/status/2032436777630540182) every few weeks, and understanding that CLAUDE.md occupies a "high-dimensional vector space" of possible starting coordinates, shaped the CLAUDE.md health quarterly review practice.
- **@mstockton** — Their [reply expanding on Todd's point](https://x.com/mstockton/status/2032451135479353790) about CLAUDE.md being the first file loaded into context helped crystallize the progressive disclosure pattern (lean CLAUDE.md + on-demand guides).
- **Pawel Huryn** ([@PawelHuryn](https://x.com/PawelHuryn)) — His post about [tracking domain vs procedural knowledge](https://x.com/PawelHuryn/status/2033227605952889008) in CLAUDE.md became the knowledge-type separation in the context efficiency guide.
- **@koylanai** — Their [hook ideas table](https://x.com/koylanai/status/2031121107164467659) — 18 practical hook ideas from auto-formatting to quality gates — is the best starting point for building your own Claude Code hooks.

### Structured Prompting & XML Tags

- **Anthropic's prompting documentation** — The foundation. The principle that Claude processes tagged content (XML) differently than prose comes directly from Anthropic's internal engineering practices.
- **@ihtesham2005** — Their [thread on Anthropic's internal prompting docs](https://x.com/ihtesham2005/status/2032939863696388237) and XML tag usage was the specific catalyst for the "prefer structured over prose" rule.
- **@Austen** — Their post that ["the closer you can get to structured/executable formats, the better"](https://x.com/Austen/status/2033369724420026822) for things agents MUST follow reinforced this as a hard rule rather than a soft preference.

### Test-First Bug Fixing, Operationalization & Multi-Agent Review

- **@tangming2005** — Their viral post about the ["single biggest improvement to my CLAUDE.md"](https://x.com/tangming2005/status/2031358195558658266) — writing a test that reproduces the bug before trying to fix it, then having subagents attempt the fix — is almost verbatim the test-first bug fixing rule.
- **@doodlestein** — Their ["Agent Coding Life Hack"](https://x.com/doodlestein/status/2036236834507047288) post: "Whenever your agent finds and fixes a bug, don't let it just stop there. Ask it to also create comprehensive end-to-end integration tests that would have caught that bug and all similar types of bugs in the future." This is the direct source of the "operationalize every fix" principle. Their broader work on the ["virtuous circle"](https://x.com/doodlestein/status/2035479010147242046) — using skills to improve tooling and tooling to improve skills — shaped the Workflow Evolution section.
- **@danpeguine** — Their implementation of [@systematicls's method](https://x.com/danpeguine/status/2029268229030285589) using Hunter Agent, Skeptic Agent, and Referee Agent was the direct inspiration for the dialectic review pattern with opposing agents.

### Plan-First & Scope Discipline

- **@doodlestein** — Their posts about [the planning process](https://x.com/doodlestein/status/2014183464573047043) ("everyone gives short shrift to this part for some reason, and it's THE difference between getting incredible code and getting garbage") shaped the plan-first protocol.
- **Garry Tan** ([@garrytan](https://x.com/garrytan)) — His [/plan-exit-review skill](https://x.com/garrytan/status/2026778016463138882) for Claude Code, used when exiting plan mode to "shake out all issues, architecture and code smell issues," directly inspired the review-plan skill.
- **Arvid Kahl** ([@arvidkahl](https://x.com/arvidkahl)) — His advice to ["shift-tab into planning mode, and mention 'do deep research on best practices'"](https://x.com/arvidkahl/status/2031457304328229184) for any non-trivial feature reinforced plan-first as a hard default.
- **Aakash Gupta** ([@aakashgupta](https://x.com/aakashgupta)) — His observation about [Boris Cherny's team building hundreds of working prototypes](https://x.com/aakashgupta/status/2029436537629491555) instead of writing PRDs shaped the "keep planning brief, start executing" interaction style.

### Human-AI Leverage & Division of Labor

- **Ethan Mollick** ([@emollick](https://x.com/emollick)) — His advice to ["collect your hard problems and good ideas now, they will get more valuable"](https://x.com/emollick/status/2026074883646517468) captures the leverage doctrine's human role (ideation, discernment) perfectly. His broader body of work on human-AI collaboration is a constant reference.
- **Francois Chollet** ([@fchollet](https://x.com/fchollet)) — His framing of [agentic coding as machine learning](https://x.com/fchollet/status/2024519439140737442) ("the engineer sets up the optimization goal and constraints, then an optimizer searches for solutions") influenced how the orchestrator-first principle thinks about the human's role.

### Code Quality & Anti-Over-Engineering

- **Andrej Karpathy** ([@karpathy](https://x.com/karpathy)) — His observation that ["agents bloat abstractions, have poor code aesthetics, are very prone to copy pasting"](https://x.com/karpathy/status/2035173492447224237) is exactly why the implementation behavior section emphasizes boring solutions and minimal complexity. His broader influence on the "prefer the obvious solution" principle is hard to overstate.
- **@andrewmccalip** — Their agreement with [the "specific disease in engineering"](https://x.com/andrewmccalip/status/2001517352324874358) where we "treat the last sliver of efficiency like it's sacred, and treat time as though it's free" reinforced the naive-then-optimize approach.
- **@garybasin** — His [complexity cleanup skill](https://x.com/garybasin/status/2036079728872890687) — "derive, don't store; make wrong states impossible; enforce function contracts" — is a practical operationalization of the anti-over-engineering principle. Bonus: "this tends to delete more code than it adds."

### Overnight Autonomous Runs

- **@witcheer** — Their post about running [autoresearch overnight on a Mac Mini](https://x.com/witcheer/status/2030900817700565394) ("9PM to 6AM, 35 experiments, zero intervention, woke up to a telegram debrief") was the direct inspiration for the overnight runner pattern.
- **@archiexzzz** — Their [deep dive into Karpathy's autoresearch repo](https://x.com/archiexzzz/status/2033034161611817300) informed the batch mode vs resume mode distinction in the overnight runner.
- **Anthropic's scheduled tasks** ([@trq212](https://x.com/trq212/status/2030019397335843288)) — The official Claude Code scheduled tasks feature handles the simple case; the overnight runner handles the complex case (usage limit retries, batch checkpointing, multi-session resume).

### Hackathon & Community Influence

- **OpenClaw** (via [@MillieMarconnni](https://x.com/MillieMarconnni/status/2030206607616053701)) — The open-sourced Claude Code setup that won an Anthropic hackathon. Seeing a complete agents + skills + hooks + MCP setup shared publicly validated the idea that Claude Code configurations are worth packaging and sharing.
- **@gvp324377** — Their succinct [division of AI users](https://x.com/gvp324377/status/2028994853707891083) into "people who use AI to tell them they are right" vs "people who use AI to tell them all the ways they could be wrong" is the philosophical foundation of the anti-sycophancy rule.

### Evals-First & Agent Steering

- **@synopsi** — Their post about how their [workflow evolved](https://x.com/synopsi/status/2035971021510230401) from "plan → implement → review → fix" to "evals → prod spec → plan → implement" — spending 90% of time on evals — is the source of the "evals before specs" principle. "Stronger and clearer guardrails I give the coding agent, better it does."
- **Yishan Wong** ([@yishan](https://x.com/yishan)) — His insight that ["saying 'remember to do X' is unreliable"](https://x.com/yishan/status/2035763780299510018) but presenting a possibly-wrong claim triggers corrective behavior shaped the "corrective framing over reminders" technique in Workflow Evolution.

### Skills as Compressed Expertise

- **@doodlestein** — Their extensive work on the ["Agent Flywheel"](https://x.com/doodlestein/status/2036280197851320530) system — using skills to communicate complex instructions with economy of expression, and the self-referential loop of using tools to improve tools — is the foundational influence on the Workflow Evolution section. Their observation that "skills are a LOT more than just markdown files" captures why this repo treats skills as first-class workflow primitives.

### Premortem & Decision-Making

- **Gary Klein** — The premortem technique (imagine the project has failed, work backwards to identify why) is from Klein's research on naturalistic decision-making, popularized by Daniel Kahneman in *Thinking, Fast and Slow*. The dialectic `--premortem` mode adapts this for AI-assisted decisions.

### Libraries

- [sentence-transformers](https://www.sbert.net/) by **Nils Reimers & Iryna Gurevych** (UKP-TUDA) — the semantic search backbone in the data pipeline example. Their 2019 paper *"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"* made local semantic search practical.
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) — the default embedding model. 22M params, 384-dim, runs on CPU.
- Pipeline runner pattern draws from [Luigi](https://github.com/spotify/luigi) (Spotify) and [Prefect](https://www.prefect.io/), simplified to a single file.

### Tools

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by **Anthropic** — the AI coding assistant this workflow is built for.

## License

MIT — use however you want.
