---
name: tradeoff
description: Compare 2+ options with a dedicated advocate for each, counter-advocates who challenge every position, and a referee who ranks what survives.
user-invocable: true
disable-model-invocation: true
argument-hint: [--agents X-Y-Z] [--lens <expert>] [options to compare]
---

# Tradeoff

Run `/dialectic-review --tradeoff $ARGUMENTS`

Read `~/.claude/skills/dialectic-review/SKILL.md` for argument parsing, then read `~/.claude/skills/dialectic-review/tradeoff-prompts.md` for the phase prompts. Follow the full three-phase process defined there. Any `/dialectic-review` flag is valid here — it passes straight through.
