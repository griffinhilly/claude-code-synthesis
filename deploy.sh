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
    if [ -t 0 ]; then
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
    else
        # Non-interactive (piped/CI/agent-driven): never overwrite silently
        echo "Non-interactive run and $TARGET_DIR/CLAUDE.md exists — keeping existing. Copy manually to overwrite."
        SKIP_CLAUDE_MD=1
    fi
fi

# ── 2. Create target directory if needed ─────────────────────────────────────

mkdir -p "$TARGET_DIR"

# ── 3. Copy CLAUDE.md ────────────────────────────────────────────────────────

if [ "${SKIP_CLAUDE_MD:-0}" != "1" ]; then
    cp "$REPO_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "  Installed CLAUDE.md"
fi

# ── 3b. Copy RESOLVER.md (routing table) ─────────────────────────────────────

if [ -f "$TARGET_DIR/RESOLVER.md" ]; then
    echo "  Keeping existing RESOLVER.md (repo version at $REPO_DIR/RESOLVER.md if you want to merge)"
else
    cp "$REPO_DIR/RESOLVER.md" "$TARGET_DIR/RESOLVER.md"
    echo "  Installed RESOLVER.md"
fi

# ── 4. Merge directories (copy contents without deleting existing files) ─────

DIRS="skills commands hooks guides tools"

# Back up any files we're about to overwrite so a customized skill/hook/guide
# is never silently clobbered.
BACKUP_DIR="$TARGET_DIR/.deploy-backup-$(date +%Y%m%d-%H%M%S)"
BACKED_UP=0
for dir in $DIRS; do
    if [ -d "$REPO_DIR/$dir" ] && [ -d "$TARGET_DIR/$dir" ]; then
        while IFS= read -r f; do
            rel="${f#"$REPO_DIR/"}"
            if [ -f "$TARGET_DIR/$rel" ] && ! cmp -s "$f" "$TARGET_DIR/$rel"; then
                mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
                cp "$TARGET_DIR/$rel" "$BACKUP_DIR/$rel"
                BACKED_UP=$((BACKED_UP+1))
            fi
        done < <(find "$REPO_DIR/$dir" -type f)
    fi
done
if [ "$BACKED_UP" -gt 0 ]; then
    echo "  Backed up $BACKED_UP differing file(s) to $BACKUP_DIR before overwriting"
fi

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
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/epistemic-guard.sh\"",
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
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/warn-skill-md-too-long.sh\"",
            "timeout": 3
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/check-new-file-index.sh\"",
            "timeout": 3
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/log-unwrapped-session.sh\"",
            "timeout": 5
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
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/epistemic-guard.sh\"",
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
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/warn-skill-md-too-long.sh\"",
            "timeout": 3
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/check-new-file-index.sh\"",
            "timeout": 3
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/log-unwrapped-session.sh\"",
            "timeout": 5
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
echo "  - skills/    (23 skills: /plan-task, /dialectic-review, /wrapup, ...)"
echo "  - commands/  (7 workflow commands: /start, /prompt, /prune, ...)"
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
