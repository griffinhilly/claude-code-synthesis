---
name: brainstorm
description: Generate a wide field of ideas, then pressure-test them. Five generators diverge, two challengers prune the weak ones, three synthesizers rank what survives.
user-invocable: true
disable-model-invocation: true
argument-hint: [--agents X-Y-Z] [--lens <expert>] [focus area]
---

# Brainstorm

Run `/dialectic-review --ideate $ARGUMENTS`

Read `~/.claude/skills/dialectic-review/SKILL.md` for argument parsing, then read `~/.claude/skills/dialectic-review/ideation-prompts.md` for the phase prompts. Follow the full three-phase process defined there. Any `/dialectic-review` flag is valid here — it passes straight through.
