# Session Notes Template

**Step 0 — disk first, then your notes.** Before writing anything, run `git status` in the project and read the project's blocks in `~/claude-scratch/session-context.md`. Another session may have worked here since your last turn (in one real case, a second session had added six uncommitted files and a decisions file, and the wrapup's PLAN.md draft would have sent the next reader down a closed track). Your notes describe your session; the COMP files must describe the disk. Never commit another session's files.

Before updating any files, take stock of what happened this session. Write these notes down — they'll be passed to the reviewer and used to update COMP files.

Fill in each field:

1. **Goal** — What was the session supposed to accomplish? (from PLAN.md or conversation start)
2. **Accomplished** — What was actually delivered (be specific — files, features, decisions)
3. **Decisions made** — Non-default choices, architectural calls, tool selections (with rationale and alternatives considered)
4. **Files changed** — Created, modified, or deleted (group by project if multi-project session)
5. **Gotchas discovered** — Bugs, platform issues, data hazards, workflow friction
6. **Deferred** — What was planned but not done, and why
7. **Concerns** — Anything the orchestrator is uncertain about
