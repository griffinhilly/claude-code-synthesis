#!/bin/bash
# PreToolUse hook for Bash: warn before destructive commands
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
COMMAND=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check bash commands
[ -z "$COMMAND" ] && exit 0

# Strip quoted strings and heredoc bodies before analysis. Commit messages,
# echo arguments, and heredoc content may DESCRIBE destructive commands
# without executing them — analyzing the stripped command instead of
# special-casing `git commit` closes the chained-command bypass
# (`git commit -m "x" && rm -rf ~/y`) and stops false-blocking
# `git add x && git commit -m "cleanup: rm -rf old docs"` at the same time.
STRIPPED=$(printf '%s' "$COMMAND" | sed -e "s/'[^']*'//g" -e 's/"[^"]*"//g')
STRIPPED=${STRIPPED%%<<*}

WARN=""

# Destructive file operations. Detect any rm carrying recursive+force in any
# spelling (-rf, -fr, -r -f, --recursive --force), analyzing each chained
# segment separately, and allow it only when EVERY target is a known safe
# cleanup dir — so `rm -rf node_modules ~/important` (one command, two
# targets) still warns.
SAFE_RM_TARGETS="node_modules .next dist __pycache__ .cache build .turbo coverage"
while IFS= read -r seg; do
  set -f
  # shellcheck disable=SC2086
  set -- $seg
  set +f
  [ "${1:-}" = "sudo" ] && shift
  [ "${1:-}" = "rm" ] || continue
  shift
  recursive=0; force=0; unsafe_target=""
  for tok in "$@"; do
    case "$tok" in
      --recursive) recursive=1 ;;
      --force) force=1 ;;
      --*) ;;
      -*)
        case "$tok" in *r*|*R*) recursive=1 ;; esac
        case "$tok" in *f*) force=1 ;; esac
        ;;
      *)
        base="${tok##*/}"
        safe=0
        for s in $SAFE_RM_TARGETS; do
          [ "$base" = "$s" ] && safe=1 && break
        done
        [ "$safe" = "0" ] && unsafe_target="$tok"
        ;;
    esac
  done
  if [ "$recursive" = "1" ] && [ "$force" = "1" ] && [ -n "$unsafe_target" ]; then
    WARN="recursive force rm targeting: $unsafe_target"
  fi
done <<EOF
$(printf '%s' "$STRIPPED" | tr ';|&' '\n\n\n')
EOF

# Destructive SQL operations.
# TRUNCATE requires "truncate table" so flags like --truncate-long-lines don't trip it.
case "$STRIPPED" in
  *"DROP TABLE"*|*"DROP DATABASE"*|*"drop table"*|*"drop database"*|*"TRUNCATE TABLE"*|*"truncate table"*)
    WARN="Destructive SQL operation detected (DROP/TRUNCATE)"
    ;;
esac

# Destructive git operations.
# push force patterns require a leading space so branch names containing
# "-f" (e.g. my-feature-branch) don't false-positive.
case "$STRIPPED" in
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
