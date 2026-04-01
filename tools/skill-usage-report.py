"""
Skill Usage Report — analyze Claude Code skill invocation patterns.

Reads the skill usage log at ~/.claude/skill-usage.log (written by the /start
and other skill slash commands) and produces a summary report including:

- Invocation counts by skill and project
- Daily usage histogram (last 14 days)
- Session statistics (average skills per session)
- Skills health: installed but never invoked, invoked but not installed,
  and workflow order violations

The log format is pipe-delimited with either 3 or 5 fields:
  Old: timestamp | skill_name | pwd
  New: timestamp | skill_name | project | session_id | pwd

Usage:
    python skill-usage-report.py              # full report, all time
    python skill-usage-report.py --days 30    # last 30 days only
    python skill-usage-report.py --help       # show help
"""

import argparse
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path(os.path.expanduser("~"))
LOG_FILE = HOME / ".claude" / "skill-usage.log"
SKILLS_DIR = HOME / ".claude" / "skills"

# Recommended workflow order from skills-reference.md
RECOMMENDED_ORDER = [
    "start",
    "prompt",       # or plan-task
    "review-plan",
    "implement",
    "verify",
    "review",
    "ship",
    "wrapup",
    "prune",
]

# Skills listed in skills-reference.md (the canonical set)
REFERENCE_SKILLS = {
    "plan-task", "implement", "research", "review", "ship", "verify",
    "finalize", "comp", "dialectic-review", "retro", "prompt",
    "prompt-only", "prompt-refine", "review-plan", "prune", "start", "wrapup",
}


def parse_log_line(line):
    """Parse a log line. Handles both old and new formats.

    Old format: timestamp | skill_name | pwd
    New format: timestamp | skill_name | project | session_id | pwd
    """
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) == 5:
        return {
            "timestamp": parts[0],
            "skill": parts[1],
            "project": parts[2],
            "session_id": parts[3],
            "pwd": parts[4],
        }
    elif len(parts) == 3:
        # Old format -- derive project from pwd
        pwd = parts[2]
        project = os.path.basename(pwd) if pwd else "unknown"
        return {
            "timestamp": parts[0],
            "skill": parts[1],
            "project": project,
            "session_id": "unknown",
            "pwd": pwd,
        }
    return None


def parse_timestamp(ts_str):
    """Parse ISO timestamp, tolerant of timezone offset formats."""
    ts_str = ts_str.strip()
    # Handle timezone offsets like -05:00
    try:
        return datetime.fromisoformat(ts_str)
    except ValueError:
        pass
    # Fallback: strip timezone and parse naive
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts_str[:19], fmt)
        except ValueError:
            continue
    return None


def load_entries(days_filter=None):
    """Load and parse all log entries, optionally filtering by recency."""
    if not LOG_FILE.exists():
        return []

    entries = []
    cutoff = None
    if days_filter is not None:
        cutoff = datetime.now().astimezone() - timedelta(days=days_filter)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = parse_log_line(line)
            if entry is None:
                continue
            ts = parse_timestamp(entry["timestamp"])
            if ts is None:
                continue
            entry["dt"] = ts
            if cutoff is not None:
                # Compare naive if needed
                ts_compare = ts.replace(tzinfo=None) if ts.tzinfo else ts
                cutoff_compare = cutoff.replace(tzinfo=None) if cutoff.tzinfo else cutoff
                if ts_compare < cutoff_compare:
                    continue
            entries.append(entry)
    return entries


def get_installed_skills():
    """Get skill names from ~/.claude/skills/ directory."""
    if not SKILLS_DIR.exists():
        return set()
    return {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}


def check_workflow_order_violations(entries):
    """Check for skill invocations that violate recommended workflow order.

    Groups entries by session, then checks if skills within each session
    follow the recommended order.
    """
    # Build position map for ordered skills
    order_map = {skill: i for i, skill in enumerate(RECOMMENDED_ORDER)}
    # plan-task is an alternative to prompt at position 1
    order_map["plan-task"] = order_map["prompt"]

    violations = []
    sessions = defaultdict(list)
    for entry in entries:
        sessions[entry["session_id"]].append(entry)

    for session_id, session_entries in sessions.items():
        if session_id == "unknown":
            continue
        # Filter to only skills that are in the workflow order
        ordered = [(e["skill"], order_map[e["skill"]])
                    for e in session_entries if e["skill"] in order_map]
        # Check for out-of-order pairs
        for i in range(len(ordered) - 1):
            skill_a, pos_a = ordered[i]
            skill_b, pos_b = ordered[i + 1]
            if pos_b < pos_a:
                violations.append(
                    f"  Session {session_id[:12]}...: "
                    f"/{skill_b} invoked after /{skill_a} "
                    f"(expected {skill_b} before {skill_a})"
                )
    return violations


def print_report(entries, days_filter):
    header = "Skill Usage Report"
    if days_filter:
        header += f" (last {days_filter} days)"
    print(f"\n{'=' * 60}")
    print(f"  {header}")
    print(f"{'=' * 60}")

    if not entries:
        print("\n  No skill invocations found.\n")
        print_skills_health(entries)
        return

    # --- Total invocations by skill ---
    skill_counts = Counter(e["skill"] for e in entries)
    print(f"\n--- Invocations by Skill ({len(entries)} total) ---\n")
    for skill, count in skill_counts.most_common():
        bar = "#" * count
        print(f"  /{skill:<25s} {count:>4d}  {bar}")

    # --- Invocations by project ---
    project_counts = Counter(e["project"] for e in entries)
    print(f"\n--- Invocations by Project ---\n")
    for project, count in project_counts.most_common():
        print(f"  {project:<30s} {count:>4d}")

    # --- Invocations by day (last 14 days) ---
    print("\n--- Invocations by Day (last 14 days) ---\n")
    now = datetime.now()
    day_counts = Counter()
    for entry in entries:
        dt = entry["dt"]
        day_key = dt.replace(tzinfo=None).strftime("%Y-%m-%d")
        day_counts[day_key] += 1

    for i in range(13, -1, -1):
        day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        count = day_counts.get(day, 0)
        bar = "#" * count
        marker = " <-- today" if i == 0 else ""
        print(f"  {day}  {count:>3d}  {bar}{marker}")

    # --- Average skills per session ---
    sessions = defaultdict(set)
    for entry in entries:
        sessions[entry["session_id"]].add(entry["skill"])
    # Exclude "unknown" sessions from average (old format entries)
    known_sessions = {k: v for k, v in sessions.items() if k != "unknown"}
    if known_sessions:
        avg = sum(len(v) for v in known_sessions.values()) / len(known_sessions)
        print(f"\n--- Session Stats ---\n")
        print(f"  Known sessions:           {len(known_sessions)}")
        print(f"  Avg skills per session:   {avg:.1f}")
        print(f"  Unique skills used:       {len(skill_counts)}")
    else:
        unknown_count = len(sessions.get("unknown", set()))
        print(f"\n--- Session Stats ---\n")
        print(f"  Sessions with IDs:        0 (all entries pre-date session tracking)")
        print(f"  Unique skills used:       {len(skill_counts)}")

    # --- Skills Health ---
    print_skills_health(entries)


def print_skills_health(entries):
    installed = get_installed_skills()
    invoked = {e["skill"] for e in entries}

    print(f"\n--- Skills Health ---\n")

    # Dead skills: installed but never invoked
    dead = sorted(installed - invoked)
    if dead:
        print(f"  Never invoked ({len(dead)} skills):")
        for s in dead:
            in_ref = " (in reference)" if s in REFERENCE_SKILLS else " (not in reference)"
            print(f"    /{s}{in_ref}")
    else:
        print("  All installed skills have been invoked.")

    # Skills invoked but not installed
    invoked_not_installed = sorted(invoked - installed)
    if invoked_not_installed:
        print(f"\n  Invoked but no skill directory ({len(invoked_not_installed)}):")
        for s in invoked_not_installed:
            in_ref = " (in reference)" if s in REFERENCE_SKILLS else ""
            print(f"    /{s}{in_ref}")

    # Workflow order violations
    violations = check_workflow_order_violations(entries)
    if violations:
        print(f"\n  Workflow order violations ({len(violations)}):")
        for v in violations:
            print(v)
    else:
        print("\n  No workflow order violations detected.")

    # Summary line
    print(f"\n  Installed skills: {len(installed)}  |  "
          f"Referenced skills: {len(REFERENCE_SKILLS)}  |  "
          f"Invoked: {len(invoked)}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Skill usage analysis report")
    parser.add_argument("--days", type=int, default=None,
                        help="Filter to last N days (default: all time)")
    args = parser.parse_args()

    entries = load_entries(days_filter=args.days)
    print_report(entries, args.days)


if __name__ == "__main__":
    main()
