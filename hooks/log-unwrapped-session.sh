#!/usr/bin/env bash
# SessionEnd hook: if the session's project directory has a dirty git tree when
# the session ends, append a line to ~/.claude/unwrapped-sessions.log so the
# next /start in that project surfaces possibly-unwrapped work.
# Built after repeated real incidents of sessions ending with work on disk but
# nothing committed and project docs stale.
# Log format: ISO-timestamp | project-dir | N dirty files
# /start reconciles and removes matching lines.

PY=$(command -v python3 || command -v python) || exit 0

input=$(cat)
cwd=$(printf '%s' "$input" | "$PY" -c "import sys,json;print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)
[ -z "$cwd" ] && exit 0
# Sessions launched from the home directory itself are exempt; any git repo
# elsewhere counts. (CUSTOMIZE: narrow to your projects root if this is noisy,
# e.g. case "$cwd" in */Projects/*|*/dev/*) : ;; *) exit 0 ;; esac)
cwd_norm=$(printf '%s' "$cwd" | sed 's|\|/|g')
home_norm=$(printf '%s' "$HOME" | sed 's|\|/|g')
[ "$cwd_norm" = "$home_norm" ] && exit 0
git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
dirty=$(git -C "$cwd" status --porcelain 2>/dev/null | grep -c .)
if [ "${dirty:-0}" -gt 0 ]; then
  printf '%s | %s | %s dirty files at session end\n' "$(date +%Y-%m-%dT%H:%M:%S%z)" "$cwd" "$dirty" >> "$HOME/.claude/unwrapped-sessions.log"
fi
exit 0
