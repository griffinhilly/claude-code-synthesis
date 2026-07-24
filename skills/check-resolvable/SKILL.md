---
name: check-resolvable
description: Audit ~/.claude/ for orphans — skills, commands, guides, and tools that exist on disk but have no path from CLAUDE.md / RESOLVER.md / other reachable files. Run weekly or before any CLAUDE.md cleanup.
user-invocable: true
disable-model-invocation: false
argument-hint: [--list-reachable]
---

# /check-resolvable — Reachability Audit

A thin wrapper around `~/.claude/tools/check-resolvable.py`. The script does the deterministic scan; this skill interprets the result and recommends action.

**Per CLAUDE.md latent-vs-deterministic rule, the audit itself is deterministic** (regex over a fixed text corpus, no LLM judgment). The optional second pass — "which of these orphans actually matter" — is latent and lives in this skill, not the script.

## When to invoke

- Weekly cron via `/loop` or `/schedule`
- Before any CLAUDE.md cleanup or skill refactor
- After adding ≥3 new skills/guides/tools (signal that the routing surface has grown)
- After any workflow-config sync that may have moved files

## Process

### Step 1: Run the deterministic scan

```
python3 ~/.claude/tools/check-resolvable.py --human
```

Add `--list-reachable` to also see what's known-good. Add `--out report.json` to persist the full JSON.

### Step 2: Interpret orphans

For each orphan reported:

- **Genuine orphan** (dead capability) — the file exists but nothing references it; safe to retire or document for removal
- **False positive** (script's pattern missed a reference) — the file IS reachable but the script's regex didn't catch it; flag for adding the reference pattern to `check-resolvable.py`
- **Pending wire-up** (newly added, not yet wired) — the file was just created and hasn't been added to RESOLVER.md or CLAUDE.md yet; add the reference now

### Step 3: Resolve

- Genuine orphans: propose removal (don't delete without user approval per your safety doctrine)
- False positives: edit `check-resolvable.py` to add the missing pattern; re-run
- Pending wire-up: add the routing entry to RESOLVER.md or the trigger to CLAUDE.md; re-run

### Step 4: Report

Summarize:
- Total capabilities counted
- Number reachable vs. orphan, by kind
- Action taken for each orphan (retired / wired / pattern-fixed / left as-is)
- Any pattern-detection gaps in the script that should be fixed

## Limitations of the deterministic scan

The audit catches *file-level* reachability — whether the artifact is referenced. It does NOT catch:

- **Stale references** (a guide is referenced but its content is outdated) — different problem, addressed by quarterly CLAUDE.md health check
- **Logical reachability** (a skill is referenced but the conditions for invocation never fire) — addressed by trigger evals (`~/.claude/tools/skill-trigger-evals.py`)
- **Cross-project references** (project CLAUDE.md files reference user-scope skills) — partial: this scan only walks `~/.claude/`, not per-project COMP files

## Extensions (mode of thinking)

Reachability audits are an instance of the broader principle: **"trust the determinism."** Any time the workflow accumulates capability beyond what a human can mentally enumerate, automated reachability becomes the only way to keep the system honest. Extensions:

1. **Cross-project reachability** — extend the corpus to include every project's CLAUDE.md / MEMORY.md / PLAN.md / ORIENT.md. Catches cases where a project references a skill that no longer exists.
2. **Reverse direction** — instead of "are all capabilities reached?", ask "are all references valid?" (catches typos: CLAUDE.md says `/check-resolveable` but the skill is `/check-resolvable`).
3. **Health over time** — run the audit weekly and log results; surface the *trend* in orphan count. If orphans grow week-over-week despite no removals, something is decaying.
4. **Trigger eval coupling** — pair this with `skill-trigger-evals.py`. Reachability says "this skill is wired in"; trigger evals say "this skill actually fires on the right inputs." Both are needed for a healthy routing layer.

## Sources

- Garry Tan, *Resolvers: The Routing Table for Intelligence* — "First run found 6 unreachable skills. Fifteen percent of the system's capabilities were dark."
- Workflow dialectic review — the binding constraint that this audit must be a script, not an LLM-driven skill.
