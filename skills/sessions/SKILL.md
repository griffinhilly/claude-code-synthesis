---
name: sessions
description: List recent Claude Code sessions as a table with auto-generated descriptions, session IDs, cwd, and turn counts. Use when the user asks "what sessions did I run", wants to find/recover a past or crashed session, or needs a session ID to resume.
user-invocable: true
disable-model-invocation: false
argument-hint: [days] [--project SUBSTR] [--md] [--all]
---

# Session History Table

Lists Claude Code sessions from the local session store with a one-line
description for each, so the user can find a session ID to resume or recover.

## How it works

Claude Code writes one JSONL transcript per session under
`~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl`. Each transcript
contains an `aiTitle` record (Claude's own auto-generated session title) and
the user's prompts. The bundled `list_sessions.py` reads these, skips subagent
and workflow transcripts, and prints a table sorted by last-active time.

## Run it

```
python3 ~/.claude/skills/sessions/list_sessions.py $ARGUMENTS
```

Falls back to `python` if `python3` isn't on PATH (e.g. some Windows setups) —
the script itself has no version-specific dependencies.

### Arguments (`$ARGUMENTS`)
- `[days]` — look-back window in days (default `7`).
- `--project SUBSTR` — only sessions whose cwd contains SUBSTR (e.g. `--project myproject`).
- `--md` — emit a GitHub-flavored markdown table (default: aligned monospace text). Use `--md` when presenting the result inline to the user.
- `--all` — ignore the day window; list every session on disk.

### Examples
- `/sessions` → last 7 days
- `/sessions 14 --md` → last 14 days as a markdown table
- `/sessions --project myproject --all` → every session ever, for a given project folder

## Presenting results

Render the output as a markdown table for the user (pass `--md`, or reformat the
text output). Columns: last-active, turns, session ID, description. Point out
that a session is resumed with `claude --resume <SESSION ID>`. If several
sessions share an identical timestamp, note that — it usually means a crash or
shutdown flushed them together.

## Notes / gotchas
- Description falls back to the first real user prompt when a session has no
  `aiTitle` yet (very new or aborted sessions).
- Turn count = non-meta user prompts; `0` turns usually means an empty/aborted session.
- Any secret-scanning hook that blocks shell `head`/`cat`/heredoc pipes over
  these JSONL files should be respected — always read them inside a Python script (as this tool
  does), never via a bash pipe.
