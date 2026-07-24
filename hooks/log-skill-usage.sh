#!/bin/bash
# PreToolUse hook for Skill: log skill invocations for tracking
# Format: timestamp | skill_name | project | session_id | pwd

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
# Session id comes from the event JSON itself (the env var is not a documented
# hook variable and is usually unset, which logged "unknown" for every row)
PARSED=$(echo "$INPUT" | "$PY" -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('skill', ''))
print(d.get('session_id', '') or 'unknown')
" 2>/dev/null)
SKILL_NAME=$(echo "$PARSED" | sed -n 1p)
SESSION_ID=$(echo "$PARSED" | sed -n 2p)

[ -z "$SKILL_NAME" ] && exit 0
SESSION_ID="${SESSION_ID:-unknown}"
PROJECT=$(basename "$(pwd)")

LOG_FILE="$HOME/.claude/skill-usage.log"
# %Y-%m-%dT%H:%M:%S%z works on both GNU and BSD/macOS date (unlike -Iseconds)
echo "$(date +%Y-%m-%dT%H:%M:%S%z) | $SKILL_NAME | $PROJECT | $SESSION_ID | $(pwd)" >> "$LOG_FILE"

exit 0
