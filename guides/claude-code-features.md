# Underutilized Claude Code Features

A reference of powerful but underused native features. Sourced from Boris Cherny (head of Claude Code) and community practitioners.

## Multi-Repo and Context

- **`--add-dir <path>`** — Grant Claude access to multiple repos simultaneously. Essential for cross-repo refactors or when your code depends on a sibling library.
- **`--bare`** — Launch with explicit system prompts, MCP configs, and settings. Skips auto-discovery and can speed up SDK startup by up to 10x. Critical for programmatic/SDK usage where startup latency matters.
- **`.claude/agents/`** — Define named custom agents with their own system prompts and tool sets via `--agent <name>`.

## Session Management

- **`/branch` / `--fork-session`** — Fork the current session into parallel development paths. Use `claude --resume <session-id> --fork-session` to branch from any point. Useful when exploring two approaches simultaneously.
- **`/btw`** — Ask a side question without interrupting the agent's current work. The agent continues its task after answering.
- **`/compact`** — Proactively compress context. Tip: invoke at ~60% context usage rather than waiting for auto-compaction at ~90%, when the model is already losing instruction fidelity.
- **`/teleport`** — Move a cloud session to your local machine. Paired with `/remote-control` to control a local session from phone or web.

## Parallel Execution

- **`-w` (git worktrees)** — Launch Claude in an isolated git worktree for parallel repo work without branch conflicts.
- **`/batch`** — Fan out across dozens or hundreds of worktree agents. Designed for large-scale migrations, bulk file transformations, or any task that's embarrassingly parallel.

## Automation

- **`/loop` and `/schedule`** — Automate recurring tasks (PR management, code review, status checks) for up to a week. `/loop` runs at intervals; `/schedule` uses cron expressions.
- **Hooks** — `PreToolUse`, `PostToolUse`, `Stop`, `PostCompact` — turn the CLI into a programmable agentic framework. See `hooks/` directory for examples.

## Input

- **`/voice`** — Voice input via spacebar hold. Useful for dictating complex instructions or when typing is impractical.

## Sources

- [Boris Cherny's 15 hidden features thread (Mar 30, 2026)](https://x.com/bcherny/status/2038454336355999749)
- [Community discussion of autonomous levels](https://x.com/aakashgupta/status/2035805431516246363)
