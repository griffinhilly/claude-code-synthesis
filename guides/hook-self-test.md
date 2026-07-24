# Hook Self-Test Before Committing

Before any hook that pattern-matches command text ships, test it against itself:

```bash
echo '{"tool_input": {"command": "the_hook_command_itself"}}' | ./the_hook.sh
```

**Why:** Three false positives showed up in one session: a secret-scanning hook blocked its own filename (matched a `*secret*` glob against itself), a destructive-command hook matched "force-push" appearing inside a commit message (not an actual force-push), and a git-add hook matched ".gitignore" as "git add .". All caught during use, not during development.

**How to apply:** Add this as a post-creation check whenever writing or modifying a hook script. One-minute test that prevents session interruptions from a hook blocking commands it shouldn't.
