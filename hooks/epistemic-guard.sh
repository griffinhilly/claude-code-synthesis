#!/bin/bash
# PreToolUse hook for Write/Edit: warn when content contains unverified epistemic claims.
# Deterministic enforcement of the "red flag language" behavioral rule.
#
# Configure in settings.json:
#   { "matcher": "Write", "hooks": [{ "type": "command", "command": "bash hooks/epistemic-guard.sh", "timeout": 3 }] }
#   { "matcher": "Edit",  "hooks": [{ "type": "command", "command": "bash hooks/epistemic-guard.sh", "timeout": 3 }] }
#
# Inspired by @DanielleFong's epistemic claims hook concept.

INPUT=$(cat)

# Extract the content being written — check both Write (content) and Edit (new_string) fields
CONTENT=$(echo "$INPUT" | python -c "
import sys, json
data = json.load(sys.stdin).get('tool_input', {})
print(data.get('content', '') or data.get('new_string', ''))
" 2>/dev/null)

[ -z "$CONTENT" ] && exit 0

# Check for epistemic hedge phrases in comments and documentation
# Only flag content that looks like comments, docstrings, or documentation — not variable names or strings
HEDGES=$(echo "$CONTENT" | grep -inE \
    '(should work|probably fine|seems to handle|this works|I think this|I believe|might be|likely works|appears to|Done!|Perfect!)' \
    2>/dev/null | head -5)

if [ -n "$HEDGES" ]; then
    echo "WARN: Content contains unverified epistemic claims:" >&2
    echo "$HEDGES" >&2
    echo "" >&2
    echo "Before writing claims like these, verify them. Run the actual check." >&2
    # Exit 0 to warn but not block. Change to exit 2 to block the tool call.
    exit 0
fi

exit 0
