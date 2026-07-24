#!/usr/bin/env python3
"""Reachability audit for ~/.claude/ workflow capabilities.

purpose: Walk CLAUDE.md / RESOLVER.md / skill files and find orphans — skills, commands,
         guides, and tools that exist on disk but have no path from any reachable root.
inputs: ~/.claude/CLAUDE.md, ~/.claude/RESOLVER.md, ~/.claude/skills/, ~/.claude/commands/,
        ~/.claude/guides/, ~/.claude/tools/, ~/.claude/SAFETY.md
outputs: JSON report to stdout (or to a path if --out provided). Optional human summary.

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
    """Inventory what exists on disk."""
    skills = sorted(p.name for p in (CLAUDE_DIR / "skills").iterdir() if p.is_dir())
    commands = sorted(p.stem for p in (CLAUDE_DIR / "commands").glob("*.md"))
    guides = sorted(p.stem for p in (CLAUDE_DIR / "guides").glob("*.md"))
    tools = sorted(p.name for p in (CLAUDE_DIR / "tools").iterdir()
                   if p.is_file() and p.suffix in {".py", ".sh"})
    return {"skills": skills, "commands": commands, "guides": guides, "tools": tools}


def gather_text():
    """Concatenate all roots + auto-loaded files for reference scanning."""
    roots = [CLAUDE_DIR / "CLAUDE.md",
             CLAUDE_DIR / "RESOLVER.md",
             CLAUDE_DIR / "SAFETY.md",
             CLAUDE_DIR / "HEARTBEAT.md",
             CLAUDE_DIR / "candidate-rules.md"]
    text = []
    for r in roots:
        if r.exists():
            text.append(f"=== {r.name} ===\n" + r.read_text(encoding="utf-8"))
    # Also include all SKILL.md content (skills reference other skills/guides)
    for p in (CLAUDE_DIR / "skills").rglob("*.md"):
        text.append(f"=== {p.relative_to(CLAUDE_DIR)} ===\n" + p.read_text(encoding="utf-8"))
    for p in (CLAUDE_DIR / "guides").glob("*.md"):
        text.append(f"=== guides/{p.name} ===\n" + p.read_text(encoding="utf-8"))
    return "\n\n".join(text)


def find_references(corpus, kind, name):
    """Return list of files that reference a given capability."""
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
    for pat in patterns:
        if re.search(pat, corpus):
            return True
    return False


def is_user_invocable(skill_name):
    """A skill is a root if it's user-invocable per its SKILL.md frontmatter."""
    skill_md = CLAUDE_DIR / "skills" / skill_name / "SKILL.md"
    if not skill_md.exists():
        return False
    head = skill_md.read_text(encoding="utf-8")[:600]
    # Frontmatter is YAML between --- markers. Look for user-invocable: true
    return bool(re.search(r"user-invocable:\s*true", head, re.I))


def audit():
    caps = list_capabilities()
    corpus = gather_text()

    orphans = {"skills": [], "commands": [], "guides": [], "tools": []}
    reachable = {"skills": [], "commands": [], "guides": [], "tools": []}

    for s in caps["skills"]:
        if is_user_invocable(s) or find_references(corpus, "skill", s):
            reachable["skills"].append(s)
        else:
            orphans["skills"].append(s)

    for c in caps["commands"]:
        if find_references(corpus, "command", c):
            reachable["commands"].append(c)
        else:
            orphans["commands"].append(c)

    for g in caps["guides"]:
        if find_references(corpus, "guide", g):
            reachable["guides"].append(g)
        else:
            orphans["guides"].append(g)

    for t in caps["tools"]:
        if find_references(corpus, "tool", t):
            reachable["tools"].append(t)
        else:
            orphans["tools"].append(t)

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
