#!/bin/bash
# PreToolUse hook for Bash: warn before destructive commands
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
COMMAND=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only check bash commands
[ -z "$COMMAND" ] && exit 0

# Replace quoted strings with a placeholder (NOT deletion: `rm -rf "/path"`
# must still present an argument to the rm analysis below) and drop heredoc
# bodies. Commit messages and echo arguments may DESCRIBE destructive
# commands without executing them — analyzing the substituted command closes
# the chained-command bypass (`git commit -m "x" && rm -rf ~/y`) without
# false-blocking `git add x && git commit -m "cleanup: rm -rf old docs"`.
STRIPPED=$(printf '%s' "$COMMAND" | sed -e "s/'[^']*'/QUOTEDARG/g" -e 's/"[^"]*"/QUOTEDARG/g')
STRIPPED=${STRIPPED%%<<*}

WARN=""

# Destructive file operations. Detect rm carrying recursive+force in any
# spelling (-rf, -fr, -r -f, --recursive --force), analyzing each chained
# segment separately. `rm` is matched at any token position (find -exec rm,
# xargs rm, sudo rm, env rm all count). Allowed only when EVERY target is a
# known safe cleanup dir given as a bare name or ./name — quoted targets
# became QUOTEDARG above and paths like /srv/app/build do NOT match, so
# `rm -rf node_modules ~/important` and `rm -rf "/home/u/x"` both warn.
SAFE_RM_TARGETS="node_modules .next dist __pycache__ .cache build .turbo coverage"
while IFS= read -r seg; do
  set -f
  # shellcheck disable=SC2086
  set -- $seg
  set +f
  # skip up to and including the first bare `rm` token, then classify the rest
  recursive=0; force=0; unsafe_target=""; past_rm=0
  for tok in "$@"; do
    if [ "$past_rm" = "0" ]; then
      [ "$tok" = "rm" ] && past_rm=1
      continue
    fi
    case "$tok" in
      --recursive) recursive=1 ;;
      --force) force=1 ;;
      --*) ;;
      -*)
        case "$tok" in *r*|*R*) recursive=1 ;; esac
        case "$tok" in *f*) force=1 ;; esac
        ;;
      *)
        safe=0
        for s in $SAFE_RM_TARGETS; do
          if [ "$tok" = "$s" ] || [ "$tok" = "./$s" ]; then safe=1; break; fi
        done
        [ "$safe" = "0" ] && unsafe_target="$tok"
        ;;
    esac
  done
  if [ "$past_rm" = "1" ] && [ "$recursive" = "1" ] && [ "$force" = "1" ] && [ -n "$unsafe_target" ]; then
    WARN="recursive force rm targeting: $unsafe_target"
  fi
done <<EOF
$(printf '%s' "$STRIPPED" | tr ';|&' '\n\n\n')
EOF

# Destructive SQL and git operations are checked against the ORIGINAL command,
# not the quote-substituted one: `psql -c "DROP TABLE users"` executes exactly
# what the quotes contain. The cost is a false positive when a commit message
# or echo merely mentions these phrases — a visible warning is cheap; a
# silently dropped table is not. TRUNCATE requires "truncate table" so flags
# like --truncate-long-lines don't trip it.
case "$COMMAND" in
  *"DROP TABLE"*|*"DROP DATABASE"*|*"drop table"*|*"drop database"*|*"TRUNCATE TABLE"*|*"truncate table"*)
    WARN="Destructive SQL operation detected (DROP/TRUNCATE)"
    ;;
esac

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
