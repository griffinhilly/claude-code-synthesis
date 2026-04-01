# /overnight — Set Up Overnight Autonomous Runs

*v1.0 — Create job manifests and launch the overnight runner*

Help the user set up, check on, or resume overnight autonomous jobs.

## Input
$ARGUMENTS

## Instructions

### Parse Intent

Determine what the user wants:

| Intent | Trigger | Action |
|--------|---------|--------|
| **New job** | `/overnight <description>` | Build a manifest, then offer to launch |
| **Status** | `/overnight status [name]` | Run `python ~/.claude/scripts/overnight.py <manifest> --status` |
| **Resume** | `/overnight resume <name>` | Find the manifest and re-launch the orchestrator |
| **Help** | `/overnight help` | Show usage examples |

### Creating a New Job

1. **Determine the mode** from the description:
   - If the task involves a LIST of similar items → **batch mode**
   - If the task is a single long-running pipeline → **resume mode**

2. **Gather parameters** — ask only for what you can't infer:
   - `name`: derive from description (kebab-case, e.g., "generate-okg-topics")
   - `working_dir`: the relevant project directory
   - `items`: for batch mode, help enumerate the item list (read from files, directories, etc.)
   - `prompt_template`: draft this yourself based on the description — this is the key value-add

3. **Write the manifest** to `<project>/overnight-<name>.json`

4. **Offer to launch**:
   ```
   Manifest written to ~/project/overnight-<name>.json

   Preview:  python ~/.claude/scripts/overnight.py ~/project/overnight-<name>.json --dry-run
   Launch:   python ~/.claude/scripts/overnight.py ~/project/overnight-<name>.json

   Want me to do a dry run first?
   ```

### Prompt Template Best Practices

When drafting `prompt_template`, always include:
- What to do with each item (be specific)
- Where to find reference/template files
- How to check if work is already done (idempotency)
- What format the output should be in
- For resume mode: instruction to check `{checkpoint_file}` before starting

### Checking Status

Run the status command and present results in a dashboard:
```
OVERNIGHT JOB: <name>
Mode: batch | resume
Progress: 45/200 (22.5%)
Failed: 3
Last run: 2026-03-14 02:30 (exit 0)
Checkpoint: ~/project/overnight-checkpoint.json
Log: ~/.claude/logs/overnight_<name>_<timestamp>.log
```

### Resuming a Job

1. Find the manifest file in the project directory
2. Check the checkpoint to confirm there's remaining work
3. Re-launch the orchestrator

## Examples

```
/overnight generate remaining OKG topics for the expanded domains
/overnight status generate-okg-topics
/overnight resume generate-okg-topics
/overnight rebuild all analytics feature tables from scratch
/overnight help
```
