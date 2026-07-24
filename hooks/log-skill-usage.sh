#!/bin/bash
# PreToolUse hook for Skill: log skill invocations for tracking
# Format: timestamp | skill_name | project | session_id | pwd

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
SKILL_NAME=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('skill',''))" 2>/dev/null)

[ -z "$SKILL_NAME" ] && exit 0

SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
PROJECT=$(basename "$(pwd)")

LOG_FILE="$HOME/.claude/skill-usage.log"
# %Y-%m-%dT%H:%M:%S%z works on both GNU and BSD/macOS date (unlike -Iseconds)
echo "$(date +%Y-%m-%dT%H:%M:%S%z) | $SKILL_NAME | $PROJECT | $SESSION_ID | $(pwd)" >> "$LOG_FILE"

exit 0
