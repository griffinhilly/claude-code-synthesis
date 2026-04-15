---
name: red-team
description: Adversarial stress-test of code, a plan, or an argument. Three critics attack, one defender rebuts, a referee judges, then a hostile auditor attacks the synthesis itself.
user-invocable: true
disable-model-invocation: true
argument-hint: [--no-audit] [--agents X-Y-Z] [--lens <expert>] [focus area]
---

# Red Team

Run the dialectic-review skill in `review` mode with the hostile auditor enabled by default. Read `~/.claude/skills/dialectic-review/SKILL.md` for argument parsing and `~/.claude/skills/dialectic-review/review-prompts.md` for the phase prompts. Any `/dialectic-review` flag is valid here — it passes straight through.

**Audit default:** Unless the user passed `--no-audit` in `$ARGUMENTS`, append `--audit` to the invocation. This is what differentiates `/red-team` from plain `/dialectic-review --mode review`: red-team always closes the loop by attacking its own synthesis.

Invocation:
- If `$ARGUMENTS` contains `--no-audit` — run `/dialectic-review $ARGUMENTS` (strip `--no-audit` before passing through; plain review mode, no auditor).
- Otherwise — run `/dialectic-review --audit $ARGUMENTS`.

Follow the full three-phase review process, then the Phase 4 Hostile Auditor defined in the dialectic-review SKILL.md.
