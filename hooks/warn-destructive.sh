#!/bin/bash
# PreToolUse hook for Bash: warn before destructive commands
# Reads tool event JSON from stdin

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check bash commands
[ -z "$COMMAND" ] && exit 0

# Skip checks for git commit commands — commit messages may contain
# destructive keywords as documentation without being destructive
case "$COMMAND" in
  "git commit"*) exit 0 ;;
esac

WARN=""

# Destructive file operations (allow rm -rf for known safe dirs)
case "$COMMAND" in
  *"rm -rf node_modules"*|*"rm -rf .next"*|*"rm -rf dist"*|*"rm -rf __pycache__"*|*"rm -rf .cache"*|*"rm -rf build"*|*"rm -rf .turbo"*|*"rm -rf coverage"*)
    # Known safe cleanup targets — allow
    ;;
  *"rm -rf "*)
    WARN="rm -rf detected"
    ;;
esac

# Destructive SQL operations
case "$COMMAND" in
  *DROP\ TABLE*|*DROP\ DATABASE*|*TRUNCATE*|*drop\ table*|*drop\ database*|*truncate*)
    WARN="Destructive SQL operation detected (DROP/TRUNCATE)"
    ;;
esac

# Destructive git operations
case "$COMMAND" in
  *"git reset --hard"*)
    WARN="git reset --hard — discards all uncommitted changes"
    ;;
  *"git push --force"*|*"git push -f"*|*"git push "*"-f"*)
    WARN="git push --force — can overwrite remote history"
    ;;
  *"git clean -f"*)
    WARN="git clean -f — permanently deletes untracked files"
    ;;
  *"git branch -D"*)
    WARN="git branch -D — force-deletes branch without merge check"
    ;;
  *"git checkout -- ."*|*"git restore ."*)
    WARN="Discards all uncommitted changes in working directory"
    ;;
esac

if [ -n "$WARN" ]; then
  echo "DESTRUCTIVE COMMAND WARNING: $WARN" >&2
  echo "Command: $COMMAND" >&2
  echo "Confirm this is intentional before proceeding." >&2
  exit 2
fi

exit 0
