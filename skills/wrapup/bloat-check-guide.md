# Bloat Check Guide

## Lightweight Check (default)
- Count lines in the project's CLAUDE.md and MEMORY.md
- If MEMORY.md > 100 lines: flag it
- If CLAUDE.md > threshold (200 lines for active projects, 75 for complete): flag it
- Report: "MEMORY.md is [N] lines (limit: 100). Consider `/prune` if it keeps growing."

## Full Prune (when `prune` flag is set)
Run full `/prune` analysis on the project.

## Stale Dashboard Check
Run: `python ~/.claude/scripts/stale-dashboard.py`
- Checks all projects, not just the current one
- Flag any projects that haven't been touched in 14+ days — they may have drifted from reality

Note: stale-dashboard.py has a known issue with paths (pre-reorg paths). If it errors, skip and note the issue.

## Retro Suggestion
If the session completed a project phase or milestone, suggest:
> "You just finished [phase/milestone]. Worth running `/retro project [name]` to capture learnings while they're fresh?"

Don't suggest retro for routine sessions — only for phase transitions or significant completions.
