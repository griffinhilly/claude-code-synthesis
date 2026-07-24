# Candidate Rules — Pending-Promotion Ledger

Rules observed ONCE land here, not in permanent doctrine. On a second real
sighting, promote to the target file and delete the entry (see RESOLVER.md
Section 4 — the ≥2-sightings promotion gate). Exceptions that skip the gate:
bug-classes, security/safety items, explicit user-requested codifications.

Entry format (one block per candidate):

```
## <short-rule-name>
- First sighting: YYYY-MM-DD — <one-line description of the incident>
- Proposed home: <CLAUDE.md section / guides/<name>.md / project CLAUDE.md>
- Promotes when: <what a second sighting looks like>
```

Installed to `~/.claude/candidate-rules.md`. This file starts empty on purpose —
its value is the discipline, not the contents.
