# Remote Control Sessions: Working From a Phone

Purpose: run real Claude Code sessions on your desktop and steer them from the Claude phone app. Execution stays local (your files, `~/.claude/` doctrine, MCP servers, credentials); the phone is a window onto the session. This guide covers the setup, the spawn-brief pattern that makes it work for real tasks, and the gotchas that cost the most time.

Scope note: Remote Control is a fast-moving feature. Everything here was verified on one Windows machine in late 2026. Re-check flags and behaviour against your CLI version (`claude remote-control --help`) before building on them.

## The shape

- **One standing bridge.** `claude remote-control` runs from a trusted, non-home folder (e.g. `~/Projects`). Each session you open from the phone is a full local CLI session in that folder. The bridge talks outbound to Anthropic's relay, so no VPN or open ports are needed. Phone disconnects are a non-event; if the desktop is offline for more than ~10 minutes, the session dies.
- **Keep it alive.** Start it hidden at logon (a Startup-folder script on Windows, a launch agent on macOS), plus a watchdog task every ~10 minutes that relaunches it if its PID is gone. Check the PID with a process-name check: PIDs get reused, and a reused PID looks "alive".
- **One session per task, not one session for everything.** The standing session acts as a dispatcher: it interprets the request, writes a brief, spawns a new session for the task, and hands off. Switching task types inside one session is a documented failure mode (see Mid-Session Hygiene in CLAUDE.md).

## The spawn-brief pattern (`/rsb`)

1. The dispatching session writes a self-contained brief to `SPAWN-BRIEF.md`: task, success criteria, constraints, absolute paths, "read first" files.
2. It starts a new bridge in the target folder (see launch pads below) with a session name.
3. The user opens the new session on the phone and types `rsb`. The `rsb` skill finds the brief and executes it.

Why a file instead of a pasted prompt: a complete first message plus a disk artifact both outrank follow-up turns. Mid-context turns get the weakest attention, and compaction eventually erases early turns. The brief survives both, and a restarted session can re-read it.

The brief's last rule tells the session to delete the brief at wrap-up, so a folder with a brief still in it means "task not yet picked up". A minimal brief:

```markdown
# SPAWN-BRIEF: <task> (<date>)
**Target project:** <absolute path>. You are in a launch pad; work there by absolute path.
## Task
<what the user asked, in their words, plus success criteria>
## Read first
1. <project>/CLAUDE.md (it does not auto-load from a pad)
2. <other files>
## First actions
1. <first concrete step>
## Rules
- <constraints: what not to touch, what needs approval>
- At wrap-up, delete this brief.
```

## Launch pads

Spawn into a fresh, empty, non-repo folder (e.g. `~/Projects/launch-pads/<session-name>/`) whose brief points at the real project by absolute path. Reasons, each learned the hard way:

- **One bridge per folder.** A second bridge in a folder that already has one fails to register.
- **Git-repo roots need their own trust acceptance.** Trust given to a parent folder covers plain subfolders but not repo roots. A bridge in an untrusted folder fails silently. Fix once by running `claude` interactively in the repo and accepting the trust dialog. Editing `~/.claude.json` by hand to fake trust does not work.
- **The home directory is never trusted for a standalone bridge** (it exits at once). An already-running interactive session can still expose itself with the in-session `/remote-control <name>` command from any folder.
- **"Registered" does not guarantee "visible".** A bridge spawned straight into a never-opened project folder registered but never appeared on the phone; fresh pads spawned the same minute all appeared. The phone lists sessions by folder name, so name the pad after the session.

The cost of pads: the real project sits outside the session's working directory, so every Read, Grep and Glob there asks for permission, and a subagent fan-out can bury the phone in prompts. Add the projects root to `permissions.additionalDirectories` in `~/.claude/settings.json`, and tell subagents to use the Read/Grep/Glob tools, not the shell.

## Lifecycle gotchas

- **Ending a session from the phone does not stop its bridge.** The bridge keeps listening, holds memory, and blocks a new spawn in that folder. Keep a pidfile per spawned bridge, and build a cleanup command that lists bridges as live (has a worker child process) or idle, stops idle ones **by PID, never by image name**, and archives finished pad folders (no bridge, no brief). Preview before stopping. A just-spawned session nobody has opened yet also looks idle, so don't run the cleanup right after spawning.
- **The watchdog protects only what it is told about.** Spawned bridges are unguarded unless you list them. Treat pad sessions as single-use; long unattended work belongs on a guarded bridge.
- **Restart recovery.** A reboot kills every bridge. `claude remote-control --session-id <id>`, run in the session's folder, reattaches a new bridge to the existing session, so the phone gets the same conversation back. Snapshot each live bridge's session ID periodically (it appears in the worker's command line), and reattach at logon. Guard the snapshot: if it runs before the restore finishes, it overwrites the list with the few survivors. On Windows with Fast Startup, "last boot time" survives a shutdown, so detect a new boot from the logon session's start time instead.
- **Auth loss looks like something else.** Changing the security settings on the account you log in with logged out every bridge at once; the logs blamed an "untrusted dir". Fix: `/login` in any CLI session, then let the watchdog respawn.
- **Background (`--bg`) sessions get retired when idle** (after hours normally, much sooner under low memory), and `--bg --resume` forks a new session ID. Don't use them for sessions meant to last. A hidden plain interactive `claude --resume <id> --remote-control <name>` holds up better, but no watchdog covers it.
- **Resume beats restart.** `claude --resume <SESSION-ID>` works from any directory and reattaches the full transcript, including images the user sent from the phone, which never reach disk any other way. Find IDs with `/sessions`.
- **Pinning a model.** `claude remote-control` has no `--model` flag. Set `ANTHROPIC_MODEL` in the environment of the process that starts the bridge; the bridge and its workers inherit it. Confirm with `/model` in the new session.
- **Shared memory across folders.** Auto-memory is stored per launch folder. If sessions start from several folders (home, `~/Projects`, pads), link their `memory/` directories to one (a junction on Windows, a symlink elsewhere) so every session sees the same memory.

## Scripts worth writing

These are short scripts on any OS. The reference versions were PowerShell and hardcoded to one machine, so they are described rather than shipped:

| Script | Job |
|---|---|
| spawn | Start a hidden bridge in a folder with a session name (optional model pin). Succeed only when the namespace's `bridge-pointer.json` is rewritten after launch; a live process is not proof of registration. Write a pidfile. |
| cleanup | List live/idle bridges from the pidfiles; stop idle or named ones by PID; archive finished pads; `-WhatIf` preview. |
| restore | Snapshot live session IDs; at logon, reattach each one and fresh-spawn idle pads that still hold a brief. Log every action. |
| watchdog | Every ~10 min: relaunch the standing bridge (and any listed standing pads) if dead; trigger the snapshot after the restore is done. |
