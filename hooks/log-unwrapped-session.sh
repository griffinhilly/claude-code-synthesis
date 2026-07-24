#!/usr/bin/env bash
# SessionEnd hook: if the session's project directory has a dirty git tree when
# the session ends, append a line to ~/.claude/unwrapped-sessions.log so the
# next /start in that project surfaces possibly-unwrapped work.
# Built after the THIRD no-/wrapup sighting on the same project (one session left
# two sub-steps uncommitted + COMP stale; prior sightings were an interrupted
# dashboard scaffold and a separately interrupted diagnosis session).
# Log format: ISO-timestamp | project-dir | N dirty files
# /start reconciles and removes matching lines.

PY=$(command -v python3 || command -v python) || exit 0

input=$(cat)
cwd=$(printf '%s' "$input" | "$PY" -c "import sys,json;print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)
[ -z "$cwd" ] && exit 0
# Only care about real project dirs with git; home dir sessions are exempt
case "$cwd" in
  *Projects*) : ;;
  *) exit 0 ;;
esac
git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
dirty=$(git -C "$cwd" status --porcelain 2>/dev/null | grep -c .)
if [ "${dirty:-0}" -gt 0 ]; then
  printf '%s | %s | %s dirty files at session end\n' "$(date -Iseconds)" "$cwd" "$dirty" >> "$HOME/.claude/unwrapped-sessions.log"
fi
exit 0
