#!/bin/bash
# PreToolUse hook for Bash: block git commits that might include secrets
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
COMMAND=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check git commit commands.
# "git add ." must match only bare-dot staging: `git add .` at end of command
# or followed by a space — NOT `git add .gitignore` or `git add ./src`.
case "$COMMAND" in
  *"git commit"*|*"git add -A"*|*"git add --all"*|*"git add ."|*"git add . "*)
    ;;
  *)
    exit 0
    ;;
esac

# For git add -A or git add ., warn about broad staging
case "$COMMAND" in
  *"git add -A"*|*"git add --all"*|*"git add ."|*"git add . "*)
    echo "Broad staging detected (git add -A or git add .). Check for .env, credentials, or large binaries before committing." >&2
    exit 2
    ;;
esac

# For git commit, check if any staged files look like secrets.
# `git commit -a` / `-am` stages tracked modifications at commit time —
# scan unstaged tracked changes too in that case, since `git diff --cached`
# alone runs before that staging happens.
STAGED=$(git diff --cached --name-only 2>/dev/null)
case "$COMMAND" in
  *"git commit -a"*|*"git commit --all"*)
    STAGED="$STAGED"$'\n'"$(git diff --name-only 2>/dev/null)"
    ;;
esac
if [ -z "$STAGED" ]; then
  exit 0
fi

SUSPECT=""
while IFS= read -r file; do
  [ -z "$file" ] && continue
  # Exempt paths — CUSTOMIZE for your repo's known-safe content dirs.
  # (hooks/* stays exempt so hook scripts with "secret" in the filename don't trip the scan.
  #  .env.example/.env.sample/.env.template are intentionally-public templates.)
  case "$file" in
    hooks/*|*.env.example|*.env.sample|*.env.template) continue ;;
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
