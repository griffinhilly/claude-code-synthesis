# /prune — Context Bloat Pruning

*v1.0 — Audit and trim auto-loaded files to reduce unnecessary context consumption*

Audit CLAUDE.md and MEMORY.md files across projects for context bloat — duplication, stale detail, historical build records that should live in reference files. Proposes specific trims, then executes on approval.

## Instructions

### Step 0: Parse Arguments

Parse `$ARGUMENTS` for flags. **If `$ARGUMENTS` is `help`, print the table below and stop.**

| Flag | Syntax | Default | Purpose |
|------|--------|---------|---------|
| Help | `help` | — | Show this options table and stop |
| Scope | `project:path` | All projects | Limit to one project directory |
| Target | `target:claude/memory/all` | `all` | Which file types to audit |
| Threshold | `threshold:N` | 100 (MEMORY) / 200 (CLAUDE) | Line count trigger for detailed review |
| Dry run | `dryrun` | Off | Report only, no changes |
| Auto | `auto` | Off | Apply all proposed trims without confirmation |

### Step 1: Inventory

Scan all project directories for CLAUDE.md and MEMORY.md files. For each, collect:
- **Line count** (via `wc -l`)
- **Project status** (Active / Complete — check PLAN.md)
- **Whether it exceeds threshold** (MEMORY.md > 100 lines, CLAUDE.md > 200 lines, or custom threshold)

Present a summary table sorted by line count descending:

```
CONTEXT INVENTORY
| File | Lines | Status | Over? |
|------|-------|--------|-------|
```

If no files exceed thresholds, report "All files within limits" and stop.

### Step 2: Analyze Bloated Files

For each file over threshold, launch a parallel research agent to analyze it. The agent should:

1. **Read the target file** (CLAUDE.md or MEMORY.md)
2. **Read sibling COMP files** (PLAN.md, ORIENT.md) in the same directory
3. **Identify bloat categories:**
   - **Duplication**: Content that appears in both CLAUDE.md and PLAN.md, or CLAUDE.md and ORIENT.md
   - **Historical detail**: Phase-by-phase build records, resolved debugging notes, old error fixes
   - **Stale references**: Files/tables/scripts that no longer exist
   - **Reference-only content**: Detailed information rarely needed during active work that could move to a separate on-demand file
   - **Completed-project bloat**: Detailed operational docs for projects marked COMPLETE
4. **Propose specific actions** for each bloat section:
   - **DELETE**: Content duplicated elsewhere (cite where)
   - **MOVE**: Content moved to a new reference file (name the file)
   - **CONDENSE**: Multi-line detail replaced with a summary table or 1-2 line version
   - **KEEP**: Flagged for review but recommended to keep (explain why)
5. **Estimate savings**: Before/after line counts

### Step 3: Present Proposals

For each bloated file, present:

```
FILE: [path] ([lines] lines, project status: [status])

PROPOSED CHANGES:
1. [ACTION] lines [N-M]: [description]
   Rationale: [why this is bloat]
   Savings: [N lines]

2. [ACTION] lines [N-M]: [description]
   ...

ESTIMATED RESULT: [before] → [after] lines ([percent]% reduction)

NEW REFERENCE FILES (if any):
- [filename]: [what it will contain]
```

### Step 4: Confirmation Gate

If `auto` flag is set, proceed directly. Otherwise:

> "Apply these changes? Options:
> - `yes` — apply all proposed changes
> - `skip [file]` — skip a specific file
> - `keep [item#]` — keep a specific item that was proposed for deletion
> - `no` — abort"

### Step 5: Execute

For each approved change:
- **DELETE**: Remove the content from the file
- **MOVE**: Create the new reference file, remove content from original, add a pointer line
- **CONDENSE**: Replace verbose content with condensed version

After all changes, run `wc -l` on modified files and present before/after comparison.

## Thresholds Reference

These are guidelines, not hard rules. A 250-line CLAUDE.md for an active project with complex DB schema may be justified. A 150-line MEMORY.md for a completed project is almost certainly bloated.

| File | Soft Limit | Hard Limit | Notes |
|------|-----------|------------|-------|
| MEMORY.md | 50 | 100 | Dashboard format. Historical detail → reference files or delete. |
| CLAUDE.md (active) | 200 | 300 | Schema + conventions essential. Phase results → PLAN.md. |
| CLAUDE.md (complete) | 75 | 150 | Completed projects need less always-loaded context. |

## Project Directories

Scan these paths (update as projects change):

```
~/CLAUDE.md (global)
~/.claude/CLAUDE.md (global instructions)
~/.claude/projects/C--Users-griff/memory/MEMORY.md (auto-memory)
~/Projects/my-analytics/
~/Projects/griffin/Agencyism/
~/Projects/my-data-pipeline/
~/Projects/griffin/Polymarket/
~/Projects/griffin/NCP/
~/Projects/griffin/knowledge-architecture/
~/Projects/griffin/open-knowledge-graph/
~/Projects/griffin/Canons/
~/Projects/griffin/Discretion/
~/Projects/griffin/my-project/
~/Projects/griffin/my-database/
```

## Examples

```
/prune                              # Full audit across all projects
/prune project:~/my-analytics       # Audit one project only
/prune target:memory                # Only check MEMORY.md files
/prune dryrun                       # Report only, no changes
/prune threshold:50                 # Lower threshold to catch more files
/prune auto                         # Apply all changes without confirmation
```
