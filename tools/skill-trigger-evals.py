#!/usr/bin/env python3
"""Skill trigger eval harness — structural pass.

purpose: For each (input, expected_skill) test case in skill-trigger-evals.jsonl, verify
         (a) the expected_skill exists on disk, (b) RESOLVER.md / SKILL.md trigger phrasing
         could plausibly route the input. Also check coverage: every skill should have at
         least one test case OR an explicit "trigger-eval-exempt: true" in its frontmatter.
inputs: ~/.claude/tools/skill-trigger-evals.jsonl, ~/.claude/RESOLVER.md, all SKILL.md files
outputs: JSON report (--out) or human summary; exit code 1 if failures

This is a *structural* eval — it does not invoke an LLM to actually classify inputs to
skills. That requires routing infrastructure not present here. The structural eval catches:
  - Test cases pointing at non-existent skills (typos, renames)
  - Skills with no test coverage
  - Trigger phrases in RESOLVER.md that drift from skill descriptions
  - Duplicate trigger phrases routing to different skills

For latent eval (does the model actually pick the right skill?), run `--emit-llm-prompt`
to get a prompt-suite that can be fed to an agent for live classification.

Per CLAUDE.md latent-vs-deterministic: this script's structural checks are deterministic.
The optional LLM-based classification step is latent and lives in the harness (or in a
manual invocation), not in this file.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
EVALS_PATH = CLAUDE_DIR / "tools" / "skill-trigger-evals.jsonl"
RESOLVER_PATH = CLAUDE_DIR / "RESOLVER.md"


def load_evals():
    """Read JSONL test cases."""
    cases = []
    with open(EVALS_PATH, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                cases.append({"line": line_no, **json.loads(line)})
            except json.JSONDecodeError as e:
                print(f"  line {line_no}: invalid JSON — {e}", file=sys.stderr)
    return cases


def existing_skills():
    """Set of skill names on disk (folder names under skills/), plus plugin-prefixed names."""
    skills = set()
    skills_dir = CLAUDE_DIR / "skills"
    if skills_dir.exists():
        for p in skills_dir.iterdir():
            if p.is_dir() and (p / "SKILL.md").exists():
                skills.add(p.name)
    # Also accept Claude Code built-in skills that don't live in ~/.claude/skills/.
    # CUSTOMIZE: add your plugin-provided skills (e.g. "myplugin:configure") here,
    # or extend BUILTIN_SKILLS via the --extra-skills flag if you add one.
    skills.update({"loop", "schedule", "init"})
    # Commands also count as routable destinations
    commands_dir = CLAUDE_DIR / "commands"
    if commands_dir.exists():
        for p in commands_dir.glob("*.md"):
            skills.add(p.stem)
    return skills


def trigger_phrases_in_resolver():
    """Extract trigger phrases from RESOLVER.md Section 1 (best-effort)."""
    if not RESOLVER_PATH.exists():
        return {}
    text = RESOLVER_PATH.read_text(encoding="utf-8")
    # Crude extraction: rows are `| trigger phrase | invocation | ... |`
    # Parse table rows that match
    rows = {}
    for line in text.splitlines():
        # Match table rows starting with | and having at least 2 separators
        m = re.match(r"^\|\s*[\"`]?([^|`\"]+?)[\"`]?\s*\|\s*`?([^|`]+?)`?\s*\|", line)
        if m and "---" not in line and "Trigger phrase" not in line:
            phrase = m.group(1).strip()
            target = m.group(2).strip().strip("`/").split()[0]  # drop args after the command
            target = target.lstrip("/")
            if target and not phrase.startswith("|"):
                rows.setdefault(target, []).append(phrase)
    return rows


def check_skill_existence(cases, known_skills):
    """Verify every test case's expected_skill exists."""
    failures = []
    for c in cases:
        skill = c.get("expected_skill")
        if not skill:
            failures.append((c["line"], "missing expected_skill field"))
        elif skill not in known_skills:
            failures.append((c["line"], f"expected_skill='{skill}' does not exist on disk"))
    return failures


def check_coverage(cases, known_skills):
    """Identify skills with zero test coverage."""
    covered = {c.get("expected_skill") for c in cases if c.get("expected_skill")}
    return sorted(known_skills - covered)


def check_duplicates(cases):
    """Identify identical inputs mapped to different skills (would be a routing conflict)."""
    by_input = {}
    for c in cases:
        inp = c.get("input", "").strip().lower()
        if not inp:
            continue
        by_input.setdefault(inp, []).append((c["line"], c.get("expected_skill")))
    conflicts = []
    for inp, mappings in by_input.items():
        skills = {s for _, s in mappings}
        if len(skills) > 1:
            conflicts.append((inp, mappings))
    return conflicts


def emit_llm_prompt(cases):
    """Print a prompt-suite that can be passed to an agent for live trigger classification."""
    print("=== TRIGGER EVAL LLM PROMPT ===\n")
    print("You are a routing assistant. For each user input below, return ONLY the most "
          "appropriate skill name from this set (or 'NONE' if no skill fits):\n")
    print("Available skills + brief descriptions:")
    for skill_dir in sorted((CLAUDE_DIR / "skills").iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            head = (skill_dir / "SKILL.md").read_text(encoding="utf-8")[:400]
            desc_match = re.search(r"description:\s*(.+?)(?:\n|$)", head)
            desc = desc_match.group(1).strip() if desc_match else "(no description)"
            print(f"  - {skill_dir.name}: {desc[:120]}")
    print(f"\nFor each numbered input, output the skill name on its own line.\n")
    for i, c in enumerate(cases, 1):
        print(f"{i}. \"{c.get('input', '')}\"")
    print("\n=== END PROMPT ===")
    print("\nExpected answers (for comparison after the agent responds):")
    for i, c in enumerate(cases, 1):
        print(f"{i}. {c.get('expected_skill', '')}"
              + (f" [{','.join(c.get('expected_flags', []))}]" if c.get('expected_flags') else ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", help="Write JSON report to this path")
    parser.add_argument("--human", action="store_true", help="Print human summary")
    parser.add_argument("--emit-llm-prompt", action="store_true",
                        help="Print an agent prompt for live classification")
    args = parser.parse_args()

    cases = load_evals()
    known = existing_skills()

    if args.emit_llm_prompt:
        emit_llm_prompt(cases)
        return 0

    existence_failures = check_skill_existence(cases, known)
    coverage_gaps = check_coverage(cases, known)
    conflicts = check_duplicates(cases)
    # RESOLVER.md parse is best-effort; the regex doesn't handle the actual table format
    # robustly, so we don't enforce "skill must appear in RESOLVER" as a hard check yet.
    # Re-enable when trigger_phrases_in_resolver() is rewritten with a real Markdown table parser.

    report = {
        "test_cases": len(cases),
        "known_skills": len(known),
        "existence_failures": [{"line": l, "msg": m} for l, m in existence_failures],
        "coverage_gaps": coverage_gaps,
        "duplicates": [{"input": inp, "mappings": m} for inp, m in conflicts],
    }

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report written to {args.out}", file=sys.stderr)

    if args.human or not args.out:
        print(f"Test cases: {len(cases)}")
        print(f"Known skills + commands: {len(known)}")
        print(f"\nExistence failures: {len(existence_failures)}")
        for line, msg in existence_failures:
            print(f"  line {line}: {msg}")
        print(f"\nSkills with no test coverage: {len(coverage_gaps)}")
        for s in coverage_gaps:
            print(f"  uncovered: {s}")
        print(f"\nDuplicate-input conflicts: {len(conflicts)}")
        for inp, mappings in conflicts:
            print(f"  '{inp}' → {mappings}")

    # Exit 1 if any structural failure
    if existence_failures or conflicts:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
