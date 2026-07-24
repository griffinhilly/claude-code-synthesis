#!/bin/bash
# PreToolUse hook for Read: block reading files that contain secrets/tokens/keys
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
FILE_PATH=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Normalize path separators
FILE_PATH=$(echo "$FILE_PATH" | sed 's|\\|/|g' | tr '[:upper:]' '[:lower:]')

# Allowlist: intentionally-public templates, and documentation ABOUT secrets
# (api_key_rotation_notes.md, user_credentials_flow.md) is not itself a secret.
case "$FILE_PATH" in
  *.env.example|*.env.sample|*.env.template|*.md) exit 0 ;;
esac

# Block reads of known secret locations and patterns
case "$FILE_PATH" in
  */.secrets/*|*/secrets/*|*.env|*.env.*|*credentials*|*secret*token*|*token*.txt|*.pem|*.key|*pgpass*|*.p12|*.pfx|*api_key*|*apikey*)
    echo "BLOCKED: Reading secret/credential file is not allowed — contents would be visible in chat." >&2
    echo "To use this secret, read it inside a script (e.g., Python open()) so the value never appears in tool output." >&2
    exit 2
    ;;
esac

exit 0
