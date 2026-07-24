#!/bin/bash
# Archive Claude Code transcripts to a separate location so retention
# policy can never delete them. Idempotent: copies new files, skips
# existing ones (no-clobber). Safe to run daily.
#
# Purpose:  Preserve session JSONL transcripts for provenance work on any
#           project where verbatim attribution or session recall matters.
# Input:    ~/.claude/projects/*/**/*.jsonl
# Output:   ~/.claude/archive/projects/... (mirrors source tree)
# Schedule: Run daily via Windows Task Scheduler or manual invocation.

set -euo pipefail

SRC="$HOME/.claude/projects"
DST="$HOME/.claude/archive/projects"
LOG="$HOME/.claude/archive/archive.log"

mkdir -p "$DST"
mkdir -p "$(dirname "$LOG")"

START_TS=$(date +%Y-%m-%dT%H:%M:%S%z)
BEFORE=$(find "$DST" -type f -name '*.jsonl' 2>/dev/null | wc -l)

# REQUIRES GNU cp (-u update-if-newer is not in BSD/macOS cp). Fail loudly
# rather than silently archiving nothing — a backup tool whose only failure
# signal is a zero counter is worse than no backup tool.
if ! cp --version 2>/dev/null | grep -q GNU; then
    echo "ERROR: GNU cp required (-u flag). On macOS: brew install coreutils, then use gcp or adjust this script." >&2
    exit 1
fi
# -u pass: copy new files; for files we already have, copy again only if the
# source is newer (sessions append to their JSONL, so grab the latest state).
cp -ru "$SRC"/. "$DST"/

AFTER=$(find "$DST" -type f -name '*.jsonl' 2>/dev/null | wc -l)
ADDED=$((AFTER - BEFORE))

echo "[$START_TS] archive: before=$BEFORE after=$AFTER added=$ADDED" >> "$LOG"
echo "archive: before=$BEFORE after=$AFTER added=$ADDED"
