#!/bin/bash
# PostCompact hook: re-inject critical session context after compaction
# Outputs to stdout — text is added to Claude's context automatically

echo "=== POST-COMPACTION REMINDER ==="
echo ""
echo "Context was just compressed. Key things to re-establish:"
echo ""

# 1. Static reminders about compaction-safe behavior
echo "BEHAVIOR:"
echo "- Re-read any COMP files (CLAUDE.md, PLAN.md) relevant to current work"
echo "- Check task list (TaskList) to see where you left off"
echo "- Important outputs should already be in files — don't rely on conversation memory"
echo "- If mid-implementation, re-read the plan and any files you were editing"
echo ""

# 2. If a session context file exists, inject it
SESSION_CTX="$HOME/.claude/session-context.md"
if [ -f "$SESSION_CTX" ]; then
    echo "SESSION STATE (written before compaction):"
    cat "$SESSION_CTX"
    echo ""
fi

# 3. Show what project we're in
echo "WORKING DIRECTORY: $(pwd)"
echo "GIT BRANCH: $(git branch --show-current 2>/dev/null || echo 'not a git repo')"
echo ""
echo "=== END REMINDER ==="
