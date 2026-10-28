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

echo "DECISION QUALITY GATES (mandatory — check if any apply right now):"
echo "1. Tradeoff: Did you just present 2+ options? → Offer /dialectic-review --tradeoff"
echo "2. Premortem: Is the plan irreversible or multi-session? → Offer /dialectic-review --premortem"
echo "3. Post-implementation: Did you just finish /implement or change 5+ files? → Offer /dialectic-review"
echo "4. Ideation: Does the user need creative ideas? → Offer /dialectic-review --ideate"
echo "5. Uncertainty: Is the user or you uncertain about approach? → Suggest appropriate DR mode"
echo "Cost gate: Always get user approval before spawning dialectic agents."
echo ""

# 2. Inject the session scratchpad. It lives outside ~/.claude/ because every
#    write there prompts, whatever the allow rules say. The old path is still
#    read so setups that predate the move keep their state.
for SESSION_CTX in "$HOME/claude-scratch/session-context.md" "$HOME/.claude/session-context.md"; do
    if [ -f "$SESSION_CTX" ]; then
        # The file is shared across sessions and only grows; inject the tail
        echo "SESSION STATE (written before compaction; last 150 lines) — $SESSION_CTX:"
        tail -n 150 "$SESSION_CTX"
        echo ""
    fi
done

# 3. Show what project we're in
echo "WORKING DIRECTORY: $(pwd)"
echo "GIT BRANCH: $(git branch --show-current 2>/dev/null || echo 'not a git repo')"
echo ""
echo "=== END REMINDER ==="
