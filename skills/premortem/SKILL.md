---
name: premortem
description: Assume the plan failed — then explain why. Three pessimists write failure narratives, two optimists rebut, a risk assessor weighs which failure modes are real.
user-invocable: true
disable-model-invocation: true
argument-hint: [--agents X-Y-Z] [--lens <expert>] [plan or decision to stress-test]
---

# Premortem

Run `/dialectic-review --premortem $ARGUMENTS`

Read `~/.claude/skills/dialectic-review/SKILL.md` for argument parsing, then read `~/.claude/skills/dialectic-review/premortem-prompts.md` for the phase prompts. Follow the full three-phase process defined there. Any `/dialectic-review` flag is valid here — it passes straight through.
