#!/bin/bash
# PreToolUse hook for Bash: block git commits that might include secrets
# Reads tool event JSON from stdin

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check git commit commands
case "$COMMAND" in
  *"git commit"*|*"git add -A"*|*"git add ."*)
    ;;
  *)
    exit 0
    ;;
esac

# For git add -A or git add ., warn about broad staging
case "$COMMAND" in
  *"git add -A"*|*"git add ."*)
    echo "Broad staging detected (git add -A or git add .). Check for .env, credentials, or large binaries before committing." >&2
    exit 2
    ;;
esac

# For git commit, check if any staged files look like secrets
STAGED=$(git diff --cached --name-only 2>/dev/null)
if [ -z "$STAGED" ]; then
  exit 0
fi

SUSPECT=""
while IFS= read -r file; do
  # Skip known content directories (topic files, not secrets)
  case "$file" in
    domains/*|output/*|hooks/*) continue ;;
  esac
  case "$file" in
    *.env|*.env.*|*credentials*|*secret*|*.pem|*.key|*pgpass*|*.p12|*.pfx)
      SUSPECT="$SUSPECT  - $file"$'\n'
      ;;
  esac
done <<< "$STAGED"

if [ -n "$SUSPECT" ]; then
  echo "Potentially sensitive files staged for commit:" >&2
  echo "$SUSPECT" >&2
  echo "Remove them from staging or confirm this is intentional." >&2
  exit 2
fi

exit 0
