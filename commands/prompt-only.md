# /prompt-only — Format Without Executing

*v2.0 — Format informal requests into structured prompts, output only (do not execute)*

Format an informal request into a structured prompt. Show the result but do NOT execute it.

## Reference Files
@~/.claude/commands/prompt-references/formatting-core.md

## Input
$ARGUMENTS

## Instructions

Follow the same steps as `/prompt` (parse intent, calibrate depth, format, inject depth directives), but:

1. **Do NOT execute the prompt.** Output only.
2. Present the formatted prompt in a fenced code block.
3. After the code block, add: `**Best run in:** [tool] — [reason]` based on tool-routing check in formatting-core.md.
4. If the task is best run in Claude Code, say so.
