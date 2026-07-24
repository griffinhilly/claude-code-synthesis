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

START_TS=$(date -Iseconds)
BEFORE=$(find "$DST" -type f -name '*.jsonl' 2>/dev/null | wc -l)

# cp -rn: recursive, no-clobber. Once archived, a file is never overwritten,
# even if the source is later modified — each session is written once to its
# JSONL and then appended to, so the source file may grow; we want to capture
# the final state. -u flag makes it update-if-newer instead.
cp -run "$SRC"/. "$DST"/ 2>/dev/null || true
# -u pass: for files we already have, copy again only if source is newer.
# This keeps archive current for in-progress sessions.
cp -ru "$SRC"/. "$DST"/ 2>/dev/null || true

AFTER=$(find "$DST" -type f -name '*.jsonl' 2>/dev/null | wc -l)
ADDED=$((AFTER - BEFORE))

echo "[$START_TS] archive: before=$BEFORE after=$AFTER added=$ADDED" >> "$LOG"
echo "archive: before=$BEFORE after=$AFTER added=$ADDED"
