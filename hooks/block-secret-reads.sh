#!/bin/bash
# PreToolUse hook for Read: block reading files that contain secrets/tokens/keys
# Reads tool event JSON from stdin

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Normalize path separators
FILE_PATH=$(echo "$FILE_PATH" | sed 's|\\|/|g' | tr '[:upper:]' '[:lower:]')

# Block reads of known secret locations and patterns
case "$FILE_PATH" in
  */.secrets/*|*/secrets/*|*.env|*.env.*|*credentials*|*secret*token*|*token*.txt|*.pem|*.key|*pgpass*|*.p12|*.pfx|*api_key*|*apikey*)
    echo "BLOCKED: Reading secret/credential file is not allowed — contents would be visible in chat." >&2
    echo "To use this secret, read it inside a script (e.g., Python open()) so the value never appears in tool output." >&2
    exit 2
    ;;
esac

exit 0
