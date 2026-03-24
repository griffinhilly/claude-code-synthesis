# Overnight Autonomous Runner

> **Note:** This guide describes a pattern for building your own overnight orchestrator, not a script that ships with this repo. The architecture below is what works in practice — implement it as a Python script in your project.

An external Python orchestrator that wraps `claude -p` in a retry loop, surviving session boundaries and usage limits.

## Architecture

```bash
# You'd build a script like this and run it:
python overnight.py manifest.json

# Check progress:
python overnight.py manifest.json --status

# Preview without running:
python overnight.py manifest.json --dry-run
```

## Two Modes

### Batch Mode
For processing many similar items (topic generation, entity descriptions, file processing).

```json
{
  "name": "categorize-products",
  "mode": "batch",
  "working_dir": "~/my-project",
  "model": "sonnet",
  "batch_size": 5,
  "max_turns_per_batch": 50,
  "max_budget_usd": 10.0,
  "allowed_tools": "Bash,Read,Edit,Write,Glob,Grep",
  "retry_wait_minutes": 15,
  "max_retries": 10,
  "checkpoint_file": "overnight-checkpoint.json",
  "prompt_template": "Process these items:\n{items}\n\nWorking directory is already set. Read existing outputs for format reference. Skip any that already exist.",
  "items": ["item-1", "item-2", "item-3"]
}
```

**How it works**: The orchestrator takes `batch_size` items at a time, injects them into `prompt_template` via `{items}`, and runs `claude -p`. Completed items are tracked in the checkpoint file. On usage limits, it waits `retry_wait_minutes` and retries.

### Resume Mode
For long-running single tasks that may need multiple sessions (data pipelines, large refactors).

```json
{
  "name": "rebuild-features",
  "mode": "resume",
  "working_dir": "~/my-project",
  "model": "sonnet",
  "max_turns_per_session": 50,
  "max_sessions": 10,
  "max_budget_usd": 20.0,
  "allowed_tools": "Bash,Read,Edit,Write,Glob,Grep",
  "retry_wait_minutes": 15,
  "max_retries": 5,
  "checkpoint_file": "overnight-checkpoint.json",
  "prompt_template": "Continue the pipeline. Check {checkpoint_file} for what's been done. When fully complete, update the checkpoint with: {\"status\": \"complete\"}"
}
```

**How it works**: Runs the prompt repeatedly in fresh sessions. Each session reads the checkpoint to know where to pick up. When Claude writes `"status": "complete"` to the checkpoint, the orchestrator stops.

## Template Variables

Available in `prompt_template`:

| Variable | Batch Mode | Resume Mode | Description |
|----------|-----------|-------------|-------------|
| `{items}` | Yes | No | Newline-separated list of current batch items |
| `{items_list}` | Yes | No | JSON array of current batch items |
| `{checkpoint_file}` | Yes | Yes | Path to checkpoint JSON |
| `{batch_num}` | Yes | No | Current batch number |
| `{total_remaining}` | Yes | No | Items left to process |
| `{session_num}` | No | Yes | Current session number |
| `{max_sessions}` | No | Yes | Session limit |

## Checkpoint File

Auto-maintained by the orchestrator. Structure:

```json
{
  "completed": ["item1", "item2"],
  "failed": ["item3"],
  "started_at": "2026-03-14T22:00:00",
  "status": "in_progress",
  "runs": [
    {"batch_num": 1, "exit_code": 0, "timestamp": "...", "output_length": 1234}
  ]
}
```

Claude can also write to this file during execution to communicate progress back to the orchestrator. In resume mode, writing `"status": "complete"` signals the job is done.

## Tips

- **Prompt design matters**: The prompt should tell Claude to check what already exists before creating anything, to handle the case where a previous session partially completed a batch.
- **Use Sonnet for bulk work**: Faster, cheaper, and less likely to hit rate limits.
- **Start small**: Test with `--dry-run` first, then run a single batch manually before going overnight.
- **Budget guards**: Set `max_budget_usd` to prevent runaway costs.
- **Idempotent operations**: Design prompts so re-running a batch that partially completed is safe.
