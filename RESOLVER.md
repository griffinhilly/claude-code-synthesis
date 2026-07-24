# RESOLVER.md — Routing Table

**Purpose:** Map (a) task descriptions → skill/command invocations and (b) content types → filing destinations. The single source of truth for "what should I invoke" and "where does this go." Read by the agent before any non-trivial task routing or memory write.

**Mandate** (from `CLAUDE.md`): Before writing any cross-project memory file or invoking a skill on an ambiguous task, consult this file. If the task type isn't in the table, propose adding it before proceeding.

**Maintenance:** Update this file when a new skill is added, when a memory-file convention changes, or when a routing decision is made repeatedly in sessions (signal that an entry is missing). Quarterly review removes orphan entries; the `/check-resolvable` skill audits reachability.

**Install note:** This file lives at `~/.claude/RESOLVER.md`. Rows referencing skills ship in this repo; rows marked "Claude Code built-in" (`/loop`, `/schedule`) reflect the product as of mid-2026 — verify against your Claude Code version, since built-in command names drift. Customize the trigger phrases to the things you actually say.

---

## Section 1 — Task → Skill/Command Routing

Entries grouped by intent. When the user says something matching the **Trigger phrase** (or close paraphrase), route to the **Invocation**.

### Session lifecycle

| Trigger phrase | Invocation | Notes |
|---|---|---|
| "start a session", "let's begin", `/start [project]` | `/start` | First skill of every session |
| "wrap up", "end session", "let's stop here" | `/wrapup` | Last skill of every session |
| "finalize", "close out the work" | `/finalize` | Lighter-weight than wrapup; for mid-session work-unit close |
| "let's plan this", "before we build", "design first" | `/plan-task <task>` | Structured decomposition before implementation |
| "review my plan", "stress-test the plan" | `/review-plan` | Plan-mode-specific review |
| "implement the plan", "build it" | `/implement` | Executes a `/plan-task` output |
| "review what I did", "check the work" | `/review` | Strengthened: spec-blind reviewer, ≥2 passes, adversary posture |
| "verify the output", "make sure it works" | `/verify` | Completeness check; pairs with /review (which is quality) |
| "ship it", "ready to commit" | `/ship` | Pre-commit readiness; verifies tests, doc freshness, drafts commit |
| "prune context", "clean up the session" | `/prune` | Mid-session bloat reduction |

### Decision-making & ideation

| Trigger phrase | Invocation | Notes |
|---|---|---|
| "let me think about this", weighing options, fork in design space | `/dialectic-review` (default review mode) | See Decision Quality Gates in CLAUDE.md |
| "compare these N options" | `/dialectic-review --tradeoff` | When 2+ viable approaches present |
| "what could go wrong with this plan" | `/dialectic-review --premortem` | Irreversible / multi-session scope |
| "stress-test this", "find what we missed" | `/dialectic-review` then `--audit` | Audit phase attacks the synthesis |
| "brainstorm", "give me alternatives", "ideation" | `/dialectic-review --ideate` OR `/brainstorm` | Diverse perspectives generation |
| "what does the strongest opposition look like" | `/red-team` OR `/dialectic-review --mode review` | Adversarial attack mode |
| "evaluate from 5 perspectives", "panel review" | `/dialectic-review --council` | 5 distinct advisor biases + anonymous peer review + chairman synthesis |
| "let's question this together", "Socratic dialogue" | `/socrates` | Guided questioning |

### Debugging & quality

| Trigger phrase | Invocation | Notes |
|---|---|---|
| "this is broken", "debug this", "what's wrong" | `/debug` | 4-phase: Observe → Hypothesize → Reproduce → Fix |
| "hunt for bugs", "find every defect" | `/bug-hunt` | Hunter/Skeptic/Referee triad |

### Research & learning capture

| Trigger phrase | Invocation | Notes |
|---|---|---|
| "research X", "go figure out Y" | `/research <topic>` | Read-only investigator agent |
| "capture this learning", "remember this for next time" | `/learn` | Apply rule promotion gate — see Section 4 below |
| "let me retrospect", "what worked / didn't" | `/retro` | Structured after-action review |
| "optimize this metric", "improve until budget runs out" | `/autoresearch` | Bounded autonomous optimization with rollback |
| "distill rules from edits", "what did I correct here" | `/distill <draft> <final>` | Diff agent draft vs. user-corrected final; propose rules to candidate-rules.md |

### Workflow maintenance

| Trigger phrase | Invocation | Notes |
|---|---|---|
| "update the COMP files", "refresh project docs" | `/comp` | Updates CLAUDE.md/ORIENT.md/MEMORY.md/PLAN.md |
| "audit reachability", "find orphan skills/guides" | `/check-resolvable` | Runs `~/.claude/tools/check-resolvable.py`; reports orphans |
| "what sessions did I run", "find that crashed session" | `/sessions` | Session table with IDs for resume/recovery |
| "search past sessions for X" | `python ~/.claude/tools/session-search.py "X"` | Keyword search over transcripts |
| "skill usage report", "which skills actually get used" | `python ~/.claude/tools/skill-usage-report.py` | Reads the log-skill-usage.sh log |
| "find stub/TODO/placeholder debt" | `python ~/.claude/tools/mock-finder.py <path>` | Deterministic code-debt scan |
| "archive session transcripts" | `bash ~/.claude/tools/archive-transcripts.sh` | Run daily (cron/scheduled task) |
| "silent health monitoring", "heartbeat check" | `python ~/.claude/tools/heartbeat.py` | Parses `~/.claude/HEARTBEAT.md`; emits anomalies only |
| "eval skill routing coverage" | `python ~/.claude/tools/skill-trigger-evals.py` | Cases in `tools/skill-trigger-evals.jsonl` |
| "schedule a recurring task" | `/schedule` | Claude Code built-in |
| "run X every N minutes" | `/loop <interval> <prompt>` | Claude Code built-in |
| "do X overnight" | `/overnight` | Autonomous unattended run |
| "make a new skill", "I want to codify this" | Update RESOLVER.md first, then write `~/.claude/skills/<name>/SKILL.md` | See Section 3 below |

---

## Section 2 — Content → Directory Routing

When you're about to write a learning, decision, fact, or rule, **find it on this table before writing**. If no row matches, add one.

### User-scope (cross-project) memory

Claude Code's auto-memory directory lives at `~/.claude/projects/<cwd-hash>/memory/` (the hash encodes the directory you usually launch from). `MEMORY.md` there is the always-loaded index.

| Content type | Destination | Example |
|---|---|---|
| Feedback memo (correction or confirmed approach) | auto-memory `feedback_<topic>.md` + entry in MEMORY.md | `feedback_writing_style.md` |
| User profile fact (role, preferences) | auto-memory `user_<topic>.md` + entry in MEMORY.md | `user_expertise.md` |
| Project-status entry | auto-memory MEMORY.md project dashboard | Status row update |
| Cross-project gotcha | auto-memory MEMORY.md gotchas section | One-line gotcha |
| Reference pointer (external system, dashboard) | auto-memory `reference_<topic>.md` + entry in MEMORY.md | `reference_agent_ecosystem.md` |
| Workflow doctrine (always-on behavioral rule) | `~/.claude/CLAUDE.md` | Implementation Behavior bullet |
| Situational guide (triggered rule, not always-on) | `~/.claude/guides/<name>.md` + index entry in CLAUDE.md Situational Guides | `econometrics.md` |
| Candidate rule (first sighting, pending promotion) | `~/.claude/candidate-rules.md` | Single-line entry with promotion criteria |
| Custom skill | `~/.claude/skills/<name>/SKILL.md` + entry in this file's Section 1 | `~/.claude/skills/autoresearch/SKILL.md` |

### Project-scope memory

| Content type | Destination | Example |
|---|---|---|
| Project conventions / behavioral contract | `<project>/CLAUDE.md` | Per-project AI doctrine |
| Human orientation doc | `<project>/ORIENT.md` | "What is this project, sit-down-after-2-weeks" |
| Accumulated decisions / gotchas | `<project>/MEMORY.md` | Cross-session knowledge |
| Direction / roadmap / current state | `<project>/PLAN.md` | Phases + `## Current State` section |
| Public-facing project description | `<project>/README.md` | Only when project goes public |

### Routing decision rules

- **Default to user-scope** when content applies across projects. Default to project-scope when content is project-specific.
- **Cross-project pattern observed twice → promote** from candidate-rules.md to user-scope memory.
- **Don't duplicate** between MEMORY.md and PLAN.md within a project. PLAN.md gets active/current state; MEMORY.md gets durable knowledge.
- **Triggered/situational rules belong in guides/**, not CLAUDE.md. CLAUDE.md is for always-on doctrine that applies to every session.

---

## Section 3 — When to Make a New Skill

Before creating `~/.claude/skills/<name>/SKILL.md`, work through this checklist:

1. **Is it recurring?** A skill is justified when an operation will run ≥3 times across your project portfolio. One-offs go in `~/.claude/tools/` as scripts or stay in conversation.
2. **Is it parameterized?** A skill should describe *process of judgment* and take parameters supplying *the world*. If it's domain-locked to one project, consider whether it belongs in that project's `CLAUDE.md` instead.
3. **Is it latent or deterministic?** Per CLAUDE.md's latent-vs-deterministic rule: if the work is counting/joining/optimizing/thresholding, it's a script (Python in `~/.claude/tools/`), not a skill.
4. **Does an existing skill have a `--<flag>` form that would carry it?** Modes beat new skills. `/dialectic-review --council` adds capability without adding resolver entries.
5. **Will a description-as-resolver-key work?** SKILL.md descriptions are matched against user intent. Write trigger phrases users actually say, not explanations.
6. **Add to Section 1 of this file** before writing the skill file. If you can't write a clear trigger-phrase row, the skill isn't ready.

---

## Section 4 — Promotion Gate (Convergent Signal)

When a session generates a candidate learning/rule/pattern, apply the **≥2 sightings** gate before promotion:

- **First sighting:** Append to `~/.claude/candidate-rules.md` with date, proposed home, and what-would-trigger-promotion.
- **Second sighting (matches an existing candidate):** Promote to target file; delete from candidate-rules.md; note "Promoted from candidate-rules.md after second sighting on YYYY-MM-DD" in the new home.
- **Exceptions (skip the gate):** Bug fixes revealing a class of bugs; security/safety items; explicit user-requested codifications.

This gate prevents single-occurrence rules from accumulating as permanent doctrine that doesn't fire. The deeper principle — *convergent signal across runs justifies investment* — generalizes beyond memory: don't generalize a bug fix from one occurrence, don't update doctrine from one reviewer's judgment, don't declare a data finding without replication, don't treat one positive response as product validation.

---

## Section 5 — Anti-Patterns

**Don't:**
- Write a memory file without an entry in MEMORY.md pointing to it (orphan files invisible to next session)
- Save the same rule in both CLAUDE.md and MEMORY.md (one source of truth)
- Build a new skill before adding its routing entry here (resolver decay starts here)
- Write project-specific facts to user-scope memory (clutters cross-project context)
- Bypass the candidate-rules.md gate for "obviously correct" rules (single-occurrence rules accumulate as permanent doctrine that doesn't fire)

**Do:**
- Update this file before changing the workflow (RESOLVER.md is the source of truth, not the consequence)
- Use Section 1 trigger phrases as the canonical names of skill descriptions (they're resolver keys for the model)
- Apply the promotion gate even when it feels obvious — convergent signal is what justifies permanent doctrine

---

## Cross-references

- `~/.claude/CLAUDE.md` — always-loaded behavioral doctrine
- `~/.claude/guides/skills-reference.md` — full skill catalog with descriptions
- `~/.claude/candidate-rules.md` — pending-promotion ledger
- Per-project COMP files (CLAUDE/ORIENT/MEMORY/PLAN)
