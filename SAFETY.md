# SAFETY.md — Always-on Safeguards

**Purpose:** Safety-critical rules extracted from CLAUDE.md so they have a dedicated, hard-to-overwrite home. Re-read before any destructive operation, external communication, or credential access. The active hooks in `~/.claude/settings.json` are the deterministic enforcement layer; this file is the doctrine layer that backstops them and that the agent must internalize.

**Re-read mandate:** Before any of the following actions, re-read this file:
- Database mutations (INSERT/UPDATE/DELETE/DROP/ALTER) on any project DB
- External communications (git push, gh CLI write operations, Slack/Telegram/email sends, API calls to external services that change state)
- Reading or writing credential files (.env, pgpass, *.pem, *.key, anything with `token` / `secret` / `password` in name)
- Destructive shell commands (rm -rf, mass deletes, force-push, hard-reset to discard work)

---

## Database Mutations

- **INSERT** requires explicit human confirmation when the row count is >100, when affected tables include user/production data, or when triggered by a script the user hasn't reviewed.
- **UPDATE / DELETE** require explicit human confirmation *with a summary of what will be affected*: row count, affected columns, and a `SELECT` preview of representative rows.
- **DROP / TRUNCATE / ALTER** require explicit human confirmation *plus* a second confirmation showing the schema impact and a backup state check.
- **Backup state must be confirmed** before any destructive database operation. If no recent backup exists, refuse until one is made.

## External Communications

- **git push**: Only proceed on explicit human review of the diff. Never force-push to main/master. Force-push to other branches only on explicit user request.
- **gh CLI write operations** (`gh pr create`, `gh issue comment`, `gh pr merge`, label/milestone changes, repo settings): Only on explicit user approval. Show the exact command and target before executing.
- **Messages** (Slack, Telegram, email, Discord): Only on explicit user approval. Show the exact recipient and message body before sending.
- **PR comments**: Only on explicit user approval.
- **API calls to external services that change state** (Linear ticket updates, Notion writes, Stripe operations, etc.): Only on explicit user approval.
- **Third-party uploads** (diagram renderers, pastebins, gists, archive.ph submissions): Treat as external communications. Consider whether content could be sensitive before sending; once uploaded, it may be cached/indexed even if later deleted.

## Credentials

- **Never hardcode credentials** in any file Claude writes.
- **Reference from config files**: `pgpass` for PostgreSQL, `.env` for app-level secrets, `~/.aws/credentials` for AWS, etc.
- **Credential locations are documented** in one cross-project security note (e.g. a `security.md` in your auto-memory) and in each project's `CLAUDE.md` (project-specific).
- **Hook protection**: `~/.claude/hooks/block-secret-reads.sh` (and `block-secret-bash.sh` for shell reads) blocks reads of common credential file patterns. Don't try to bypass it. If a task genuinely needs a credential, tell the user, and use it inside a script that reads it without printing it, so the value never enters the conversation.

## Destructive Shell / Git Operations

- **rm -rf** requires explicit user approval for any path that isn't a project-local temp/build directory. Never run on user home, workspace roots, or git working trees.
- **git reset --hard**, **git clean -fd**, **git checkout .**, **git branch -D** on unmerged branches: explicit approval required.
- **--no-verify** on git commit, **--no-gpg-sign**: never unless user explicitly requests it. If a pre-commit hook fails, fix the underlying issue rather than bypassing.
- **Mass deletes** (find -delete, xargs rm, etc.): show what will be deleted before deleting.

## Hook-Backed Protections (do not bypass)

The active hooks in `~/.claude/settings.json` enforce a subset of the above deterministically:

- **PreToolUse → Bash**: Blocks `git add -A` / `git add .`, checks staged files for credentials before `git commit`, warns before destructive commands (rm -rf, DROP, git push --force, etc.)
- **PreToolUse → Read**: Blocks reads of secret/credential files

If a hook fires unexpectedly, **investigate the underlying request** — don't reword the command to evade the hook. The hook is the deterministic check; this file is the doctrine layer; both are intentional belt-and-suspenders.

## Principles That Survive Specific Rules

- **Reversibility scales caution.** The cost of pausing to confirm is low; the cost of an unwanted action is potentially high.
- **Scope-of-approval matters.** A user approving an action (e.g., `git push`) once does NOT mean approval in all future contexts. Authorization stands for the scope specified, not beyond.
- **Investigate before deleting.** Unexpected state (unfamiliar files, branches, lock files) may be the user's in-progress work. Investigate before overwriting.
- **Resolve, don't discard.** Prefer resolving merge conflicts over discarding changes. Prefer fixing failing hooks over bypassing them.

## When SAFETY.md and CLAUDE.md conflict

This file takes precedence. If a CLAUDE.md rule appears to authorize something this file forbids, surface the conflict and stop.

---

Installed to `~/.claude/SAFETY.md` by `deploy.sh` (an existing SAFETY.md is kept). Extracted from CLAUDE.md so the safety rules have a dedicated, hard-to-overwrite home.
