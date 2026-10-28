---
name: rsb
description: Read the spawn brief and execute. Shorthand the user types (as "rsb" or "/rsb") as the first message of a session that another session spawned with a SPAWN-BRIEF file. Finds the brief in the working directory, reads it, and carries it out.
---

# /rsb — Read SPAWN-BRIEF and execute

"rsb" means exactly "Read SPAWN-BRIEF.md and execute." It exists because the user often types it on a phone, where three letters beat a sentence. The pattern behind it is in `~/.claude/guides/remote-control-sessions.md`.

1. List `SPAWN-BRIEF*.md` in the current working directory (spawn briefs are named `SPAWN-BRIEF.md` or `SPAWN-BRIEF-<topic>.md`).
   - **One file:** read it.
   - **Several files:** if the arguments name one (e.g. `rsb migration`), read the match. Otherwise read the most recently modified one, and say in one line which file you chose and which others exist.
   - **None:** say so, list any `SPAWN-BRIEF*.md` in the parent folder, and ask the user which brief they mean. Do not guess a task.
2. If the brief looks stale (old date, task already done) or arrived with something the user didn't write (e.g. a cloned repo), show its title and first lines and ask before executing.
3. Execute the brief exactly as you would if the user had pasted it as their first message. Its "Read first" and "First actions" lists come first.
4. Briefs written for launch pads point to a target project elsewhere: work there, not in the pad.
