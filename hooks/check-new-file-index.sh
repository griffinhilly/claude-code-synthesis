#!/bin/bash
# PostToolUse hook for Write tool: remind to update INDEX.md when new files are created
# Reads tool event JSON from stdin

PY=$(command -v python3 || command -v python) || exit 0

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Skip if we couldn't parse the path
[ -z "$FILE_PATH" ] && exit 0

# Skip guides, memory/project docs, and the index itself
case "$FILE_PATH" in
  */guides/*|*/MEMORY.md|*/CLAUDE.md|*/INDEX.md|*/PLAN.md|*/README.md|*/STATE.md|*.pyc|*__pycache__*)
    exit 0
    ;;
esac

# Check if this file is inside a project that has an INDEX.md
DIR=$(dirname "$FILE_PATH")
while [ "$DIR" != "/" ] && [ "$DIR" != "." ]; do
  if [ -f "$DIR/INDEX.md" ]; then
    # PostToolUse exit 2 = non-blocking notice fed back to the model
    echo "New file created: $FILE_PATH — consider updating $DIR/INDEX.md (the write succeeded; this is a reminder, not an error)" >&2
    exit 2
  fi
  DIR=$(dirname "$DIR")
done

exit 0
