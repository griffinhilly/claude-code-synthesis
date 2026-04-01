#!/bin/bash
# PreToolUse hook for Skill: log skill invocations for tracking
# Format: timestamp | skill_name | project | session_id | pwd

INPUT=$(cat)
SKILL_NAME=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('skill',''))" 2>/dev/null)

[ -z "$SKILL_NAME" ] && exit 0

SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
PROJECT=$(basename "$(pwd)")

LOG_FILE="$HOME/.claude/skill-usage.log"
echo "$(date -Iseconds) | $SKILL_NAME | $PROJECT | $SESSION_ID | $(pwd)" >> "$LOG_FILE"

exit 0
