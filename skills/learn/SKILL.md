---
name: learn
description: Capture structured learnings (gotcha, pattern, decision, bug-fix) as JSONL per project. Cross-project searchable.
user-invocable: true
disable-model-invocation: false
argument-hint: [type] <description> | list | search <term>
---

# Structured Learning Capture

Capture reusable knowledge as structured JSONL entries in the current project directory. Each project gets its own `.claude-learnings.jsonl` file. Cross-project search supported.

## Input

Arguments: `$ARGUMENTS`

## Subcommand Routing

Parse the first word of `$ARGUMENTS`:

| First word | Action |
|------------|--------|
| `list` | Show all learnings for current project |
| `search` | Search ALL projects for matching learnings |
| `gotcha` | Capture with type=gotcha, rest is description |
| `pattern` | Capture with type=pattern, rest is description |
| `decision` | Capture with type=decision, rest is description |
| `bug-fix` | Capture with type=bug-fix, rest is description |
| anything else | Capture with type inferred from context (default: pattern) |

If no arguments at all, ask: "What did you learn? Describe it and I'll capture it."

## Type Definitions

Use these to classify learnings and to infer type when not specified:

| Type | When to use | Example |
|------|-------------|---------|
| `gotcha` | A trap or pitfall to avoid next time | "psycopg2 cursor.copy_expert needs binary mode for COPY" |
| `pattern` | A reusable approach or technique | "use pd.read_csv with encoding='utf-8-sig' for BOM files" |
| `decision` | A choice made with rationale worth preserving | "chose GMM over K-Means because clusters are non-spherical" |
| `bug-fix` | What broke and why, so it never recurs | "capacity_changes double-counted because JOIN lacked date filter" |

### Type Inference Rules (when no type specified)

- Contains "don't", "avoid", "careful", "trap", "gotcha", "watch out", "never" --> `gotcha`
- Contains "chose", "decided", "picked", "went with", "because", "over" --> `decision`
- Contains "broke", "fixed", "bug", "caused by", "root cause", "was wrong" --> `bug-fix`
- Default --> `pattern`

## Capture Process (for gotcha/pattern/decision/bug-fix)

### Step 1: Determine the File Path

The learning file lives in the **current project root** (the directory containing CLAUDE.md, or the current working directory if no CLAUDE.md is found):

```
<project-root>/.claude-learnings.jsonl
```

### Step 2: Compose the Entry

Build a JSON object with these fields:

```json
{"type": "gotcha|pattern|decision|bug-fix", "summary": "one-line summary", "detail": "full description with context", "date": "YYYY-MM-DD", "tags": ["tag1", "tag2"]}
```

Rules:
- `summary`: One sentence, max ~80 chars. This is the scannable headline.
- `detail`: The full description from the user, plus any relevant context (what project, what file, what triggered it). Include enough that someone reading this 6 months later understands it.
- `date`: Today's date in YYYY-MM-DD format.
- `tags`: 2-4 tags derived from the content. Use lowercase, hyphenated terms. Include the technology/tool involved (e.g., "pandas", "postgresql", "git") and the domain (e.g., "data-pipeline", "deployment", "testing").

### Step 3: Write the Entry

Append the JSON object as a single line to the `.claude-learnings.jsonl` file. One entry per line, no trailing comma, no array wrapper.

### Step 4: Confirm

Print the captured entry formatted for readability and state the file path it was written to.

## List Process

Read the `.claude-learnings.jsonl` file in the current project directory. Display all entries grouped by type, with newest first within each group. Format:

```
## Learnings for <project-name> (N total)

### Gotchas (N)
- [2025-03-15] one-line summary
  detail text here

### Patterns (N)
...
```

If no learnings file exists, say: "No learnings captured yet for this project. Use `/learn <description>` to start."

## Search Process

Arguments after `search`: the search term(s).

1. Glob for all `.claude-learnings.jsonl` files across all project directories (recursively).
2. Read each file and search for entries where `summary`, `detail`, or `tags` contain the search term (case-insensitive).
3. Display matching entries grouped by project, with the project path as a header.

Format:
```
## Search results for "<term>" (N matches across M projects)

### ~/Projects/my-web-app
- [pattern] [2025-03-15] one-line summary
  detail text

### ~/Projects/data-pipeline
- [gotcha] [2025-02-10] one-line summary
  detail text
```

If no matches, say: "No learnings found matching '<term>' across any project."

## Integration Notes

- This skill complements MEMORY.md. Use `/learn` for atomic, searchable facts. Use MEMORY.md for narrative context, status, and cross-cutting decisions.
- The `/debug` skill suggests `/learn gotcha` after fixing a bug. The `/retro` skill can bulk-capture learnings from session review.
- Learnings files are gitignored by convention (they're local workflow artifacts, not project code). Add `.claude-learnings.jsonl` to `.gitignore` if the project is version-controlled.
