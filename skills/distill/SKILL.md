---
name: distill
description: Diff an agent draft against the user-corrected final, extract patterns from the corrections, and propose candidate rules for skill files. Manual form of the self-improving-skill loop. Invoked at /ship or on demand.
user-invocable: true
disable-model-invocation: false
argument-hint: <draft-source> <final-source> [--target-skill <skill-name>]
---

# /distill — Extract Rules from Observed Corrections

When you and an agent collaborate on an artifact, the diff between the agent's draft and the version you actually shipped is a learning corpus. This skill takes that diff, classifies the patterns of correction, and proposes candidate rules for the relevant skill file.

**This is the manual half of the self-improving-skill loop.** The agent-watching-edits-automatically half (auto-watcher) is deferred pending Anthropic's native skill-learning features. The *doctrine* — that corrections are a learning corpus — is provider-neutral and ships now.

**Promotion gate applies.** Candidate rules go to `~/.claude/candidate-rules.md` on first sighting. Promotion to permanent skill doctrine happens on the second sighting per the rule promotion gate (see `~/.claude/skills/wrapup/health-check-guide.md`).

---

## Input

`$ARGUMENTS` should be one of:

1. **Two file paths**: `<draft-path> <final-path>` — explicit before/after files
2. **Git refs**: `<commit-or-branch>..<commit-or-branch>` <file-path> — use the diff between commits
3. **"last /ship"**: when invoked from `/ship` or right after a commit, automatically diff `HEAD~1..HEAD` for the staged files
4. **A description**: "Claude drafted X; I edited it to Y" — agent reconstructs the relevant artifacts and diffs them

Optional flag:
- `--target-skill <skill-name>` — propose rules for a specific skill (default: agent infers which skill produced the draft)

---

## Process

### Step 1: Establish the diff

Render the diff between draft and final in a structured way:
- Lines/blocks removed (what the agent *did* that the user un-did)
- Lines/blocks added (what the agent *missed* that the user filled in)
- Lines/blocks modified (what the agent *got partly right*)

If the diff is tiny (< 5 lines changed) or uniform (only whitespace/typos), report "no signal" and exit. Don't manufacture patterns from noise.

### Step 2: Classify correction patterns

For each non-trivial removal/addition/modification, classify it. Common pattern types:

- **Voice/tone:** Agent used X phrasing; user replaced with Y. (e.g. AI-tell phrases caught by the de-AI-ism pass — "load-bearing," "let me gently push back")
- **Specificity:** Agent abstracted; user got concrete. (e.g. "users" → a specific handle/name, "improve performance" → "reduce p95 latency below 200ms")
- **Hedging:** Agent qualified; user committed. (e.g. "this should work" → "this works")
- **Structure:** Agent used wrong format. (e.g. paragraph → numbered list; missing headers; wrong code-fence language)
- **Scope:** Agent did more than asked. (e.g. unsolicited refactor; defensive error handling for impossible cases)
- **Specificity-of-attribution:** Agent generic-attributed; user named the source. (e.g. "research suggests" → a named, dated citation)
- **Workflow-specific:** Agent missed a project convention. (e.g. forgot a known data-file encoding gotcha; used `cd <dir>` before git commands)

Pattern-count threshold: a pattern needs to appear **at least twice in this single diff** to be worth proposing as a rule. Once is noise; twice is signal.

### Step 3: Identify the target skill (if not specified)

Without `--target-skill`, infer:
- If the draft was a CLAUDE.md addition → propose rule for CLAUDE.md
- If the draft was a commit message → /ship
- If the draft was a code review comment → /review or /bug-hunt
- If the draft was prose for external publication → the pre-publish-critical-response guide
- If the draft was a plan → /plan-task
- If unclear, ask the user.

### Step 4: Propose candidate rules

For each pattern that fired ≥2 times in the diff, write a candidate rule entry. Format:

```
### YYYY-MM-DD — <short rule>
- **Pattern observed:** <how it showed up in the diff — give 2-3 concrete examples from the actual edits>
- **Proposed rule:** <one-sentence behavioral rule that would prevent the correction>
- **Proposed home:** <specific skill file / CLAUDE.md / guide>
- **First sighting context:** <which artifact, which project>
- **What would promote:** <what specific second sighting would justify codifying>
```

Append all candidates to `~/.claude/candidate-rules.md`.

### Step 5: Check for second-sighting matches

Before exiting, scan `~/.claude/candidate-rules.md` for prior entries whose **proposed rule** matches what was just observed. If a prior candidate matches, this is the **second sighting** — promote it now:

1. Read the prior candidate's "Proposed home"
2. Append the rule to that target file (with a "Promoted from candidate-rules.md after second sighting on YYYY-MM-DD" note)
3. Remove the original entry from candidate-rules.md
4. Report the promotion to the user

If no second sighting fires, exit with: "N candidate rules logged. Promotion happens when these patterns appear again."

---

## Output

Always print a concise summary to chat:

```
DISTILL SUMMARY
- Artifact: <what was diffed>
- Patterns detected: <N>
- Candidates logged: <N> (appended to candidate-rules.md)
- Promotions this run: <N> (matched second sightings)
- Top pattern: <one-line description of the most-fired pattern>
```

---

## When This Skill Triggers

- **Automatic at /ship** (intended): after a commit lands, /ship can call /distill on the agent's last draft vs. the committed version. (Currently /ship doesn't auto-call /distill — that's a future wiring.)
- **Manual after a session** where you noticeably edited Claude's output: invoke `/distill` with two file paths
- **From /wrapup** when reflecting on what got edited and what didn't
- **On demand** when you suspect a recurring correction pattern but haven't named it

**Don't use this skill when:**
- The diff is trivial (typos, whitespace, single-word swaps) — no learning signal
- The corrections were the user's own change of mind (not agent error) — wrong direction of learning
- The artifact was experimental / one-off — corrections won't generalize

---

## Latent / Deterministic Split (per CLAUDE.md rule)

| Step | Latent / Deterministic |
|---|---|
| Compute the diff | Deterministic (git diff or difflib) |
| Render the diff | Deterministic |
| Classify patterns | **Latent** (semantic judgment of what each edit represents) |
| Pattern-count threshold (≥2 per diff) | Deterministic (count) |
| Infer target skill | **Latent** (route based on content) |
| Propose candidate rules | **Latent** (write a behavioral rule that would prevent the pattern) |
| Check second-sighting matches | Deterministic (file scan, fuzzy match on proposed-rule text) |
| Append to candidate-rules.md | Deterministic |
| Promote on second sighting | Deterministic (file move) |

---

## Extensions (mode of thinking)

The core principle: **observed corrections are a learning corpus; corpora can be distilled into rules.** Today this fires manually on artifacts you choose. Extensions:

1. **Auto-watcher at /ship.** Once the doctrine is stable, /ship hooks into /distill on every commit — automatic distillation, manual promotion. This is the deferred half of the self-improving-skill loop.
2. **Cross-session corpus.** Today /distill operates on a single diff. A cross-session version would query the candidate-rules ledger for *similar pending rules* across diffs — clustering corrections from multiple artifacts to surface patterns invisible to any single one.
3. **Bidirectional distill.** Today we distill what Claude got wrong. The mirror image: when Claude's output *surprises the user positively*, what about the draft was non-obvious? That's also a learning signal — but for a capture-style skill, not for skill-rule promotion.
4. **Distill on rejected drafts.** Sometimes you `/rewind` an agent attempt. The pre-rewind state is a "definitively rejected" draft. Diff against your eventual replacement to surface what about the original framing was wrong.

---

## Sources

- A shared write-up on wiring agent skills into loops — diff-distill loop, 10-15 similar edits → classify → rule
- Garry Tan (/improve skill) — NPS feedback → diarize "OK" responses → propose rules → write back to matching skills. Reported 12% → 4% OK rate after one cycle
- Workflow dialectic review — the argument that the doctrine survives even if Anthropic ships native learning
