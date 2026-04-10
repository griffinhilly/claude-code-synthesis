# Event-Driven Agent Patterns

How to avoid burning tokens when nothing is happening. The core principle: **use zero-token bash checks as gates before invoking the LLM**.

## The Problem

A naive monitoring loop fires Claude on a schedule (every N minutes), loads full context, and checks if anything needs attention. Most of the time, nothing does — but the tokens are already spent.

Real-world example: 24M+ Opus tokens/day monitoring agents that weren't running. After switching to bash pre-checks: ~1.7M tokens/day. **14x reduction.**

## The Pattern: Bash Pre-Check Gate

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐
│ Cron/Timer   │────>│ Bash pre-check   │────>│ Claude (only if   │
│ (every N min)│     │ (0 tokens)       │     │ action needed)    │
└─────────────┘     └──────────────────┘     └───────────────────┘
                         │                         │
                    exit(0) if idle           Analyze, act, report
```

The bash script checks preconditions cheaply:
- `jq` to check task queues or config files
- `git status` / `git log` to check for new commits or PRs
- `curl` to check API endpoints or CI status
- `tmux list-sessions` to check running agents
- File existence/modification time checks

If the check finds nothing actionable, the script exits immediately — zero tokens spent. If it finds something, it invokes Claude with `--print` or via webhook.

## Example: PR Watch

```bash
#!/bin/bash
# pre-check-prs.sh — only invoke Claude if new PRs need review

PENDING=$(gh pr list --state open --json number,title --jq 'length')

if [ "$PENDING" -eq 0 ]; then
    exit 0  # Nothing to do — zero tokens
fi

# Something needs attention — invoke Claude
claude --print "Review the $PENDING open PRs. For each, check: tests passing, no security issues, follows conventions." \
    --allowedTools "Bash,Read,Grep,Glob"
```

## Example: Build Monitor

```bash
#!/bin/bash
# pre-check-ci.sh — only invoke Claude if CI is failing

STATUS=$(gh run list --limit 1 --json conclusion --jq '.[0].conclusion')

if [ "$STATUS" = "success" ]; then
    exit 0  # Green — zero tokens
fi

claude --print "CI is failing. Diagnose the most recent failure and propose a fix." \
    --allowedTools "Bash,Read,Grep,Glob"
```

## Integration with Overnight Runner

Use pre-check gates as the outer loop for overnight autonomous runs:

```bash
#!/bin/bash
# overnight-monitor.sh — runs via cron every 10 minutes

# Gate 1: Are there any active tasks?
[ ! -f ~/.claude/overnight-tasks.json ] && exit 0

ACTIVE=$(jq '[.[] | select(.status == "active")] | length' ~/.claude/overnight-tasks.json)
[ "$ACTIVE" -eq 0 ] && exit 0

# Gate 2: Is a Claude session already running?
pgrep -f "claude.*--print" > /dev/null && exit 0

# All gates passed — invoke Claude
claude --print "Check overnight-tasks.json and work on the next active task." \
    --allowedTools "Bash,Read,Grep,Glob,Edit,Write"
```

## Autonomous Loop Safety: Stall Detection

For agents running in autonomous loops, add stall detection to prevent infinite retries:

```bash
#!/bin/bash
# loop-with-stall-detection.sh

STALL_FILE="/tmp/claude-loop-state"
MAX_STALLS=3

# Check for stall: if the output hash hasn't changed in N iterations, stop
CURRENT_HASH=$(md5sum output.log 2>/dev/null | cut -d' ' -f1)
LAST_HASH=$(cat "$STALL_FILE" 2>/dev/null)

if [ "$CURRENT_HASH" = "$LAST_HASH" ]; then
    STALL_COUNT=$(cat "${STALL_FILE}.count" 2>/dev/null || echo 0)
    STALL_COUNT=$((STALL_COUNT + 1))
    echo "$STALL_COUNT" > "${STALL_FILE}.count"

    if [ "$STALL_COUNT" -ge "$MAX_STALLS" ]; then
        echo "STALL DETECTED: $MAX_STALLS iterations with no progress. Stopping."
        # Notify via webhook, Telegram, etc.
        exit 1
    fi
else
    echo 0 > "${STALL_FILE}.count"  # Reset stall counter
fi

echo "$CURRENT_HASH" > "$STALL_FILE"
```

Key principles for autonomous loops:
- **Stall detection**: Track output hashes between iterations. If nothing changes for N iterations, stop.
- **Max iterations**: Hard cap on loop count, independent of stall detection.
- **Distinguishable failures**: Retryable errors (network timeout) vs. non-retryable (bad config). Only retry the former.
- **Visible failure**: When a loop stops, it should notify — not silently exit.

## Sources

- [@elvissun (Mar 3, 2026)](https://x.com/elvissun/status/2028671336219107687) — bash pre-check gate pattern, 14x token reduction
- [@aakashgupta (Mar 22, 2026)](https://x.com/aakashgupta/status/2035805431516246363) — autonomous levels taxonomy
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — loop-operator agent with stall detection
