# Implementation Rules

- Follow the plan as written. If you think the plan needs changes, say so and get approval first.
- Do NOT add features, refactor surrounding code, or make "improvements" beyond the plan.
- If you encounter an obstacle not covered by the plan, ask the user rather than guessing.
- Use the security safeguards: confirm DB mutations, don't push without approval.
- After implementation, run `/verify` on the output to catch silent failures before declaring done.
- Then suggest running `/finalize` to update COMP files.
