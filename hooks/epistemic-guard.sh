#!/bin/bash
# PostToolUse hook for Write/Edit: warn when written content contains unverified
# epistemic claims. Deterministic nudge for the "red flag language" behavioral rule.
# Registered under PostToolUse (not PreToolUse): exit 2 there is a non-blocking
# notice fed back to the model after the write succeeds — exit-0 output on either
# event goes only to the debug log and never reaches Claude.
#
# Configure in settings.json under "PostToolUse":
#   { "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/hooks/epistemic-guard.sh\"", "timeout": 3 }] }
#
# Inspired by @DanielleFong's epistemic claims hook concept.

INPUT=$(cat)

# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0

# Extract the content being written — check both Write (content) and Edit (new_string) fields
CONTENT=$(echo "$INPUT" | "$PY" -c "
import sys, json
data = json.load(sys.stdin).get('tool_input', {})
print(data.get('content', '') or data.get('new_string', ''))
" 2>/dev/null)

[ -z "$CONTENT" ] && exit 0

# Check for strong unverified-completion phrases. Deliberately narrow: broad
# hedges like "might be" or "appears to" are ordinary English and made this
# hook fire on nearly every prose write. This greps the whole payload, so
# occasional false positives in string literals are accepted noise.
HEDGES=$(echo "$CONTENT" | grep -inE \
    '(should work|probably fine|seems to handle|likely works|Done!|Perfect!)' \
    2>/dev/null | head -5)

if [ -n "$HEDGES" ]; then
    echo "WARN: The content just written contains unverified epistemic claims:" >&2
    echo "$HEDGES" >&2
    echo "" >&2
    echo "The write succeeded. Before repeating claims like these, run the actual check." >&2
    # PostToolUse exit 2 = non-blocking notice fed back to the model.
    exit 2
fi

exit 0
