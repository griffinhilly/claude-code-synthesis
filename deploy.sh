#!/bin/bash
# deploy.sh — Install claude-code-synthesis workflow config into ~/.claude/
# Purpose: Copy skills, hooks, guides, tools, and CLAUDE.md from this repo
# Works on: macOS, Linux, Git Bash on Windows

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude"

echo "=== Claude Code Synthesis — Deploy ==="
echo ""
echo "Source:  $REPO_DIR"
echo "Target:  $TARGET_DIR"
echo ""

# ── 1. Check for existing CLAUDE.md ──────────────────────────────────────────

if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    echo "WARNING: $TARGET_DIR/CLAUDE.md already exists."
    echo ""
    read -rp "Overwrite it? [y/N] " answer
    case "$answer" in
        [yY]|[yY][eE][sS])
            echo "Overwriting CLAUDE.md..."
            ;;
        *)
            echo "Skipping CLAUDE.md (keeping existing)."
            SKIP_CLAUDE_MD=1
            ;;
    esac
fi

# ── 2. Create target directory if needed ─────────────────────────────────────

mkdir -p "$TARGET_DIR"

# ── 3. Copy CLAUDE.md ────────────────────────────────────────────────────────

if [ "${SKIP_CLAUDE_MD:-0}" != "1" ]; then
    cp "$REPO_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "  Installed CLAUDE.md"
fi

# ── 4. Merge directories (copy contents without deleting existing files) ─────

DIRS="skills commands hooks guides tools"

for dir in $DIRS; do
    if [ -d "$REPO_DIR/$dir" ]; then
        mkdir -p "$TARGET_DIR/$dir"
        cp -r "$REPO_DIR/$dir/." "$TARGET_DIR/$dir/"
        count=$(find "$REPO_DIR/$dir" -type f | wc -l | tr -d ' ')
        echo "  Merged $dir/ ($count files)"
    fi
done

# ── 5. Make hooks executable ─────────────────────────────────────────────────

if [ -d "$TARGET_DIR/hooks" ]; then
    chmod +x "$TARGET_DIR/hooks/"*.sh 2>/dev/null || true
    echo "  Made hooks executable"
fi

# ── 6. Handle settings.json (hook registration) ─────────────────────────────

SETTINGS_FILE="$TARGET_DIR/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    echo ""
    echo "MANUAL STEP REQUIRED: $SETTINGS_FILE already exists."
    echo ""
    echo "Add the following hooks to your settings.json if not already present:"
    echo ""
    cat <<'HOOKEOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/check-staged-secrets.sh\"",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/block-secret-bash.sh\"",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/warn-destructive.sh\"",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/block-secret-reads.sh\"",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/log-skill-usage.sh\"",
            "timeout": 3
          }
        ]
      }
    ],
    "PostCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/post-compact-reminder.sh\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
HOOKEOF
else
    cat > "$SETTINGS_FILE" <<'JSONEOF'
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/check-staged-secrets.sh\"",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/block-secret-bash.sh\"",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/warn-destructive.sh\"",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/block-secret-reads.sh\"",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/log-skill-usage.sh\"",
            "timeout": 3
          }
        ]
      }
    ],
    "PostCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/post-compact-reminder.sh\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
JSONEOF
    echo ""
    echo "  Created settings.json with hooks configured"
fi

# ── 7. Summary ───────────────────────────────────────────────────────────────

echo ""
echo "=== Deploy Complete ==="
echo ""
echo "Installed to $TARGET_DIR/:"
[ "${SKIP_CLAUDE_MD:-0}" != "1" ] && echo "  - CLAUDE.md (operating model + instructions)"
echo "  - skills/    (18 slash commands: /plan-task, /implement, /review, ...)"
echo "  - hooks/     (security hooks: secret blocking, destructive command warnings)"
echo "  - guides/    (situational guides: context-efficiency, delegation, ...)"
echo "  - tools/     (session-search, skill-usage-report)"
echo ""

echo "Next steps:"
echo "  1. Review CLAUDE.md and customize for your workflow"
echo "  2. Verify hooks are registered in $SETTINGS_FILE"
echo "  3. Run 'claude' and try: /plan-task, /implement, /review, /wrapup"
echo ""
echo "Docs: https://github.com/griffinhilly/claude-code-synthesis"
