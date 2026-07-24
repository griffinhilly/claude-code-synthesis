#!/bin/bash
# PostToolUse hook for Edit/Write: warn when a SKILL.md exceeds 150 lines.
# Progressive disclosure / skills-as-folders convention.
# Reads tool event JSON from stdin.

PY=$(command -v python3 || command -v python) || exit 0

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | "$PY" -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only fire on SKILL.md files under ~/.claude/skills/
case "$FILE_PATH" in
    */.claude/skills/*/SKILL.md)
        ;;
    *)
        exit 0
        ;;
esac

# Count lines in the post-edit state
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi
LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')

if [ "$LINE_COUNT" -gt 150 ]; then
    SKILL_NAME=$(echo "$FILE_PATH" | sed -E 's|.*\.claude/skills/([^/]+)/SKILL.md|\1|')
    cat >&2 <<EOF
WARNING: $SKILL_NAME/SKILL.md is now $LINE_COUNT lines (threshold: 150).

Consider refactoring into folder-with-leaf-files (progressive disclosure):
  - SKILL.md keeps numbered steps + @reference pointers only
  - rules.md, examples.md, templates.md, etc. become separate files loaded on demand

Single-file skills cause "attention competition" — fix one thing, break another. The
threshold is approximate; the principle is "rules + examples + templates in one file =
refactor candidate."

This is a warning, not a block — the write succeeded.
EOF
    # PostToolUse exit 2 = non-blocking notice fed back to the model
    # (exit 0 stdout goes only to the debug log and never reaches Claude).
    exit 2
fi

exit 0
