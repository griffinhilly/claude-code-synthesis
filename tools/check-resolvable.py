#!/usr/bin/env python3
"""Reachability audit for ~/.claude/ workflow capabilities.

purpose: BFS from the auto-loaded roots (CLAUDE.md, RESOLVER.md, SAFETY.md,
         candidate-rules.md, user-invocable skills) and find orphans — skills,
         commands, guides, and tools that exist on disk but have no reference
         path from any root. A capability referenced only by another orphan is
         still an orphan (this is a graph traversal, not a mention-scan).
inputs: ~/.claude/CLAUDE.md, ~/.claude/RESOLVER.md, ~/.claude/skills/,
        ~/.claude/commands/, ~/.claude/guides/, ~/.claude/tools/
outputs: JSON report to stdout (or to a path if --out provided). Optional human summary.
         Missing directories are treated as empty (partial/Tier-1 installs are fine).

Per CLAUDE.md latent-vs-deterministic rule, this is a *deterministic* audit. Same input
produces same output every run. No LLM judgment in the scan — only the optional second-pass
("which of these orphans actually matter") may be latent and is done outside this script.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"


def list_capabilities():
    """Inventory what exists on disk. Missing directories count as empty."""
    skills_dir = CLAUDE_DIR / "skills"
    commands_dir = CLAUDE_DIR / "commands"
    guides_dir = CLAUDE_DIR / "guides"
    tools_dir = CLAUDE_DIR / "tools"
    skills = sorted(p.name for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    commands = sorted(p.stem for p in commands_dir.glob("*.md")) if commands_dir.is_dir() else []
    guides = sorted(p.stem for p in guides_dir.glob("*.md")) if guides_dir.is_dir() else []
    tools = sorted(p.name for p in tools_dir.iterdir()
                   if p.is_file() and p.suffix in {".py", ".sh"}) if tools_dir.is_dir() else []
    return {"skills": skills, "commands": commands, "guides": guides, "tools": tools}


def capability_text(kind, name):
    """The text a capability contributes to the graph once it is reached."""
    try:
        if kind == "skill":
            d = CLAUDE_DIR / "skills" / name
            return "\n".join(p.read_text(encoding="utf-8", errors="replace")
                             for p in sorted(d.rglob("*.md")))
        if kind == "command":
            return (CLAUDE_DIR / "commands" / f"{name}.md").read_text(encoding="utf-8", errors="replace")
        if kind == "guide":
            return (CLAUDE_DIR / "guides" / f"{name}.md").read_text(encoding="utf-8", errors="replace")
        if kind == "tool":
            return (CLAUDE_DIR / "tools" / name).read_text(encoding="utf-8", errors="replace")
    except OSError:
        pass
    return ""


def root_text():
    """Text of the always-loaded roots."""
    roots = [CLAUDE_DIR / "CLAUDE.md",
             CLAUDE_DIR / "RESOLVER.md",
             CLAUDE_DIR / "SAFETY.md",
             CLAUDE_DIR / "candidate-rules.md"]
    return "\n\n".join(r.read_text(encoding="utf-8", errors="replace") for r in roots if r.exists())


def is_referenced(corpus, kind, name):
    """Does the corpus reference a given capability?"""
    patterns = []
    # NOTE: `/name` cannot use \b on the leading slash (both `/` and the space-before-it
    # are non-word chars, so there's no word boundary). Use (?<!\w) lookbehind instead.
    if kind == "skill":
        patterns += [
            rf"\bskills/{re.escape(name)}/",
            rf"(?<!\w)/{re.escape(name)}\b",
            rf"`{re.escape(name)}`",
            rf"`/{re.escape(name)}`",
        ]
    elif kind == "command":
        patterns += [
            rf"\bcommands/{re.escape(name)}\.md",
            rf"(?<!\w)/{re.escape(name)}\b",
            rf"`/{re.escape(name)}`",
        ]
    elif kind == "guide":
        patterns += [
            rf"\bguides/{re.escape(name)}\.md",
            rf"`{re.escape(name)}`",
        ]
    elif kind == "tool":
        patterns += [
            rf"\btools/{re.escape(name)}\b",
            rf"`{re.escape(name)}`",
        ]
    return any(re.search(pat, corpus) for pat in patterns)


def is_user_invocable(skill_name):
    """A skill is a root if it's user-invocable per its SKILL.md frontmatter."""
    skill_md = CLAUDE_DIR / "skills" / skill_name / "SKILL.md"
    if not skill_md.exists():
        return False
    head = skill_md.read_text(encoding="utf-8", errors="replace")[:600]
    # Frontmatter is YAML between --- markers. Look for user-invocable: true
    return bool(re.search(r"user-invocable:\s*true", head, re.I))


def audit():
    caps = list_capabilities()

    # BFS: start from root text + user-invocable skills; each newly-reached
    # capability contributes its own text; repeat to fixpoint.
    all_caps = [(kind, name) for kind in ("skills", "commands", "guides", "tools")
                for name in caps[kind]]
    kind_singular = {"skills": "skill", "commands": "command", "guides": "guide", "tools": "tool"}

    reached = set()
    corpus_parts = [root_text()]
    for s in caps["skills"]:
        if is_user_invocable(s):
            reached.add(("skills", s))
            corpus_parts.append(capability_text("skill", s))

    changed = True
    while changed:
        changed = False
        corpus = "\n\n".join(corpus_parts)
        for kind, name in all_caps:
            if (kind, name) in reached:
                continue
            if is_referenced(corpus, kind_singular[kind], name):
                reached.add((kind, name))
                corpus_parts.append(capability_text(kind_singular[kind], name))
                changed = True

    orphans = {k: [] for k in ("skills", "commands", "guides", "tools")}
    reachable = {k: [] for k in ("skills", "commands", "guides", "tools")}
    for kind, name in all_caps:
        (reachable if (kind, name) in reached else orphans)[kind].append(name)

    return {
        "total": {k: len(v) for k, v in caps.items()},
        "reachable": {k: len(v) for k, v in reachable.items()},
        "orphans": orphans,
        "reachable_lists": reachable,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", help="Write JSON to this path instead of stdout")
    parser.add_argument("--human", action="store_true", help="Print human-readable summary")
    parser.add_argument("--list-reachable", action="store_true",
                        help="In human mode, also list all reachable items")
    args = parser.parse_args()

    report = audit()

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report written to {args.out}", file=sys.stderr)

    if args.human or not args.out:
        lines = []
        for k in ["skills", "commands", "guides", "tools"]:
            total = report["total"][k]
            reach = report["reachable"][k]
            orph = total - reach
            lines.append(f"{k}: {total} total, {reach} reachable, {orph} orphans")
            if report["orphans"][k]:
                for name in report["orphans"][k]:
                    lines.append(f"  ORPHAN: {name}")
            if args.list_reachable and report["reachable_lists"][k]:
                for name in report["reachable_lists"][k]:
                    lines.append(f"  ok: {name}")
        print("\n".join(lines))

    if not args.out:
        print()
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
