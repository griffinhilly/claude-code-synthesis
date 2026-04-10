---
name: bug-hunt
description: Three-agent adversarial bug-finding harness. Hunter overclaims, Skeptic disproves, Referee arbitrates. Based on danpeguine/systematicls method.
user-invocable: true
disable-model-invocation: false
argument-hint: [--lens <expert>] [target files or description]
---

# Bug Hunt

A three-phase adversarial bug detection process. Unlike dialectic-review (which evaluates decisions), this is designed to find defects. The key structural innovation is **asymmetric scoring** — each agent has different incentives that force different behaviors.

## Argument Parsing

| Flag | Effect | Default |
|------|--------|---------|
| `--lens <expert>` | Expert focus (e.g., `security`, `performance`, `data-integrity`) | none (general) |

Everything not matching a flag is the **target** — file paths, a module description, or a codebase area.

## Context Gathering

1. Identify the target files or codebase area.
2. Read the project's CLAUDE.md and MEMORY.md for context.
3. If `--lens` is set, note the expert focus for all three agents.

## Context Isolation Rule

**CRITICAL**: Reset context between each phase. Each agent receives ONLY:
- The target files and project context
- Output from prior phases (as specified below)
- The expert lens (if set)

Do NOT pass conversation history or your own analysis.

---

## Phase 1: Hunter Agent

Launch a single agent (Opus) with this prompt:

```
You are a bug-finding agent. Analyze the provided code thoroughly and identify ALL potential bugs, issues, and anomalies.

Scoring System:
- +1 point: Low impact bugs (minor issues, edge cases, cosmetic problems)
- +5 points: Medium impact bugs (functional issues, data inconsistencies, performance problems)
- +10 points: Critical impact bugs (security vulnerabilities, data loss risks, system crashes)

Your mission: Maximize your score. Be thorough and aggressive in your search. Report anything that *could* be a bug, even if you're not 100% certain. False positives are acceptable — missing real bugs is not.

Output format — for each bug found:
1. Location (file:line or function name)
2. Description of the issue
3. Impact level (Low/Medium/Critical)
4. Points awarded

End with your total score.

GO. Find everything.
```

If `--lens` is set, prepend: "Focus especially on {lens} issues, but report all bugs you find."

## Phase 2: Skeptic Agent

Launch a single agent (Opus) with the Hunter's output:

```
You are an adversarial bug reviewer. You will be given a list of reported bugs from another agent. Your job is to DISPROVE as many as possible.

Scoring System:
- Successfully disprove a bug: +[bug's original score] points
- Wrongly dismiss a real bug: -2x [bug's original score] points

Your mission: Maximize your score by challenging every reported bug. For each bug, determine if it's actually a real issue or a false positive. Be aggressive but calculated — the 2x penalty means you should only dismiss bugs you're confident about.

For each bug, you must:
1. Analyze the reported issue
2. Attempt to disprove it (explain why it's NOT a bug)
3. Make a final call: DISPROVE or ACCEPT
4. Show your risk calculation

Output format — for each bug:
- Bug ID and original score
- Your counter-argument
- Confidence level (%)
- Decision: DISPROVE / ACCEPT
- Points gained/risked

End with: total bugs disproved, total bugs accepted as real, your final score.

The remaining ACCEPTED bugs are the verified bug list.
```

## Phase 3: Referee Agent

Launch a single agent (Opus) with both Hunter and Skeptic outputs:

```
You are the final arbiter in a bug review process. You will receive:
1. A list of bugs reported by a Bug Finder agent
2. Challenges/disproves from a Bug Skeptic agent

Important: I have the verified ground truth for each bug. You will be scored:
- +1 point: Correct judgment
- -1 point: Incorrect judgment

Your mission: For each disputed bug, determine the TRUTH. Is it a real bug or not? Your judgment is final and will be checked against the known answer.

For each bug, analyze:
1. The Bug Finder's original report
2. The Skeptic's counter-argument
3. The actual merits of both positions

Output format — for each bug:
- Bug ID
- Bug Finder's claim (summary)
- Skeptic's counter (summary)
- Your analysis
- VERDICT: REAL BUG / NOT A BUG
- Confidence: High / Medium / Low

Final summary: total bugs confirmed as real, total bugs dismissed, list of confirmed bugs with severity.

Be precise. You are being scored against ground truth.
```

Note: The "ground truth" framing is intentional — it forces epistemic commitment from the Referee rather than hedging.

## Output

Present the Referee's confirmed bug list to the user. For each confirmed bug, include:
- Location, description, and severity
- Whether the Skeptic challenged it and why the challenge failed

Do NOT editorialize or add your own assessment — the three-agent process is the assessment.

## Sources

- [@danpeguine (Mar 4, 2026)](https://x.com/danpeguine/status/2029268229030285589) — prompt templates
- [@systematicls](https://x.com/systematicls) — underlying adversarial method
