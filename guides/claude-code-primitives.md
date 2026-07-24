# Claude Code Primitives — Reference Card

A reference guide to Claude Code's keybindings, slash commands, and session-management vocabulary. **Many of these are unused by default** — read this when looking for a lighter-weight move than the one currently being made.

> **Stack-fragility note:** slash-command names and keybindings change over Claude Code versions. This guide reflects the state of **CC at the last_verified date below**. When Anthropic ships changes (`/help` will show them first), update this file; don't try to maintain a parallel copy by guessing.
>
> **Last verified:** 2026-05-12

---

## Keyboard Shortcuts (in-session)

| Shortcut | Effect | When useful |
|---|---|---|
| **Ctrl+S** | Stash half-written prompt; type a quick question; stashed draft auto-restores on submit | When mid-thought you want to ask a clarifier without losing the prompt you were composing |
| **Ctrl+R** | Cross-message history search across all previously entered messages in this project | When you typed something useful 20 messages ago and want to find it without scrolling |
| **Ctrl+G** | Open current prompt (or plan) in `$EDITOR` for bigger edits | Long-form prompts where line-editing in the terminal is painful |
| **!** prefix | Run a bash command inline; command + output land in conversation context | When you want the model to see the result of `ls`, `git status`, etc. without you copy-pasting |
| **Esc** (double-tap) | `/rewind` — jump back to before the most recent agent attempt | When an approach failed and you want to try something else without keeping the failed attempt in context |

---

## Session-Management Slash Commands

These are the *built-in* slash commands (not your custom skills). Listed in approximate frequency-of-use order.

| Command | Effect | When useful |
|---|---|---|
| `/help` | List currently available commands + keybindings | Source of truth; consult this first if anything in this guide seems wrong |
| `/clear` | Clear conversation context entirely; keep CLAUDE.md and skills loaded | **#1 failure-mode mitigator.** Run between unrelated tasks (writing PRD → asking for status) to prevent context bleed |
| `/compact [steering instructions]` | Summarize conversation to free context. Steering instructions tell it what to keep ("focus on the auth refactor; drop the test debugging") | Run at ~60% context usage rather than waiting for auto-compaction at 90% — by 90% the model has already forgotten earlier instructions |
| `/rewind` (also: double-Esc) | Jump back to before the most recent attempt; drops failed approaches from context | When an approach failed. Prefer over typing "that didn't work, try X" — keeps the failed attempt out of context |
| `/resume` | Resume a prior conversation (when supported by harness) | When you bailed mid-task earlier |
| `/init` | Initialize a new CLAUDE.md for a directory | First-time project setup |
| `/memory` | Inspect / edit loaded memory files | Audit what context the model has |
| `/loop <interval> <prompt-or-skill>` | Run something on a recurring interval | Polling for status; recurring checks; babysitting tasks |
| `/schedule` | Cron-style scheduled remote agent (routines) | When you want a one-time run or recurring job that survives session end |
| `/btw` | Side-note to Claude that doesn't interrupt main flow (when supported) | "btw, this is for project X, not project Y" |
| `/channels` | Channel-based session organization (when supported) | Multi-Claude workflows |
| `/chrome` | Switch to / connect to Chrome browser session | Browser-automation tasks |
| `/rename` | Label which session is which when running multi-Claude | Disambiguating multiple parallel Claudes |
| `/help-shortcuts` (or similar) | Show keybindings | When this guide is stale |

---

## Session-Lifecycle Patterns

### The "context hygiene staircase" (mid-session)

When something is going off:

1. **First failed attempt** → `/rewind` (drop the bad attempt, re-prompt with what you learned). Don't type corrections in-thread.
2. **Task-type switch** (e.g., writing PRD → debugging code) → `/clear`. Context from the previous task will bleed into the new one.
3. **Context approaches 60%** → `/compact` with steering ("focus on X; drop Y"). Manual compaction with intent beats auto-compaction at 90%.
4. **Session is structurally off-track** → pause, ask Claude to *diagnose* what went wrong, and *update CLAUDE.md/COMP files* to close the gap. Don't just `/clear` and try again — that loses the lesson.

(The first three are CLAUDE.md doctrine; the fourth surfaces as a wrap-up question via the codify-before-repeating gate.)

### Stashing during composition

You're typing a long prompt. You realize you need to ask Claude a small clarifying question first. **Ctrl+S** stashes the prompt; type your question; the stash auto-restores when you submit the next prompt.

### Inline bash for "let me check"

`!ls projects/` runs `ls projects/` and puts the result in conversation. Same effect as you running it and pasting the output, but one keystroke shorter. Useful when you want the model to *see* current state without you copy-pasting.

---

## Anti-Patterns

**Don't:**
- Type "that didn't work, try X instead" — use `/rewind` and re-prompt with the lesson. Keeps the failed attempt out of context.
- Wait for auto-compaction at 90% — manual `/compact` at ~60% with steering instructions gives you control over what's kept.
- Switch tasks within a single conversation without `/clear` — context bleed is the #1 documented failure mode.
- Keep typing in a session that's clearly off-track — diagnose first, update doctrine, *then* `/clear` or `/rewind`.
- Memorize specific slash-command names as doctrine — names change. Doctrine should describe the *behavior* (rewind on failure; clear on task switch); slash names are footnotes.

---

## Maintenance Protocol

This guide should be refreshed whenever:
- `/help` output diverges from what's listed here
- Anthropic ships a new Claude Code release
- A new keybinding or slash command becomes part of your routine

To check freshness: run `/help` in any session and compare. If divergences exceed ~20% of entries, update `last_verified` and refresh the tables.

If/when Anthropic publishes canonical docs for these primitives, replace this guide with a one-line pointer to those docs and a "behaviors-not-names" abstraction section.
