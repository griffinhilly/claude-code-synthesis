---
name: premortem
description: Dialectic premortem — assume failure, find the causes, assess real risks. Alias for /dialectic-review --premortem.
user-invocable: true
disable-model-invocation: true
argument-hint: [--agents X-Y-Z] [--lens <expert>] [plan or decision to stress-test]
---

# Premortem

Run `/dialectic-review --premortem $ARGUMENTS`

Read `~/.claude/skills/dialectic-review/SKILL.md` for argument parsing, then read `~/.claude/skills/dialectic-review/premortem-prompts.md` for the phase prompts. Follow the full three-phase process defined there.
