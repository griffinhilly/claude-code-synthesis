#!/bin/bash
# PreToolUse hook for Bash: warn before destructive commands
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
COMMAND=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check bash commands
[ -z "$COMMAND" ] && exit 0

# Skip checks for pure git commit commands — commit messages may contain
# destructive keywords as documentation without being destructive.
# Only skip when the command is a commit with nothing chained after it:
# `git commit -m "..." && rm -rf x` must still be checked.
case "$COMMAND" in
  "git commit"*)
    case "$COMMAND" in
      *"&&"*|*";"*|*"||"*) ;;   # chained — fall through to checks
      *) exit 0 ;;
    esac
    ;;
esac

WARN=""

# Destructive file operations (allow rm -rf for known safe dirs).
# Strip known-safe targets first, then check what remains — this way
# `rm -rf node_modules && rm -rf ~/important` still trips the warning.
RM_CHECK="$COMMAND"
for safe in node_modules .next dist __pycache__ .cache build .turbo coverage; do
  RM_CHECK="${RM_CHECK//rm -rf $safe/}"
done
case "$RM_CHECK" in
  *"rm -rf "*)
    WARN="rm -rf detected"
    ;;
esac

# Destructive SQL operations.
# TRUNCATE requires "truncate table" so flags like --truncate-long-lines don't trip it.
case "$COMMAND" in
  *"DROP TABLE"*|*"DROP DATABASE"*|*"drop table"*|*"drop database"*|*"TRUNCATE TABLE"*|*"truncate table"*)
    WARN="Destructive SQL operation detected (DROP/TRUNCATE)"
    ;;
esac

# Destructive git operations.
# push force patterns require a leading space so branch names containing
# "-f" (e.g. my-feature-branch) don't false-positive.
case "$COMMAND" in
  *"git reset --hard"*)
    WARN="git reset --hard — discards all uncommitted changes"
    ;;
  *"git push"*" --force"*|*"git push"*" -f "*|*"git push"*" -f")
    WARN="git push --force — can overwrite remote history"
    ;;
  *"git clean -f"*)
    WARN="git clean -f — permanently deletes untracked files"
    ;;
  *"git branch -D"*|*"git branch --delete --force"*)
    WARN="git branch force-delete — removes branch without merge check"
    ;;
  *"git checkout -- ."*|*"git restore ."*)
    WARN="Discards all uncommitted changes in working directory"
    ;;
esac

if [ -n "$WARN" ]; then
  echo "DESTRUCTIVE COMMAND WARNING: $WARN" >&2
  echo "Command: $COMMAND" >&2
  echo "This hook blocks the command. If it is genuinely intended, ask the user to run it themselves or to approve a narrower alternative — re-running the identical command will be blocked again." >&2
  exit 2
fi

exit 0
