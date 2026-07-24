# Windows Path Pitfalls

## Username

Windows usernames often display differently than expected (e.g., a shortened lowercase account name vs. a display name). Confirm which one Windows Bash actually uses — don't assume the full name. Paths follow whichever it is:
- `C:\Users\<username>\` (Windows-style)
- `/c/Users/<username>/` (Git Bash-style)

## Path Rules

- Use forward slashes in shell commands (Git Bash environment)
- Use `/dev/null` not `NUL`
- Verify paths exist before using them — don't assume directory structure
- Home directory shorthand `~` expands to `/c/Users/<username>` in Git Bash

## Common Paths

- Python: check with `command -v python3 || command -v python` — don't hardcode a version-specific path
- PostgreSQL: `/c/Program Files/PostgreSQL/<version>/`
- Claude config: `C:\Users\<username>\.claude\`
