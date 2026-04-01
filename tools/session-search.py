"""
Session Search — search across Claude Code conversation transcripts.

Searches the JSONL session files stored by Claude Code under ~/.claude/projects/.
Each project directory contains session transcripts as .jsonl files with user and
assistant messages. This tool performs keyword search across all sessions, with
optional filtering by project name, recency, and message role.

Usage:
    python session-search.py "query"                     # keyword search all projects
    python session-search.py "query" --project myapp     # filter by project name
    python session-search.py "query" --days 7            # last 7 days only
    python session-search.py "query" --role user          # only user messages
    python session-search.py "query" --role assistant     # only assistant messages
    python session-search.py "query" --context 2          # lines of context around match
    python session-search.py "query" --max 20             # max results (default 10)
    python session-search.py --list-projects              # list all project dirs

Searches user and assistant message text in JSONL session files.
Skips subagent files, thinking blocks, and tool call internals.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def list_projects():
    """List all project directories."""
    if not PROJECTS_DIR.exists():
        print("No projects directory found.")
        return
    for d in sorted(PROJECTS_DIR.iterdir()):
        if d.is_dir():
            sessions = list(d.glob("*.jsonl"))
            print(f"  {d.name}  ({len(sessions)} sessions)")


def extract_text(message_obj):
    """Extract readable text from a message object."""
    content = message_obj.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_result":
                    # Skip tool results — too noisy
                    pass
                # Skip thinking blocks, tool_use, etc.
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


def parse_session(filepath, min_date=None):
    """Parse a JSONL session file into messages with metadata."""
    messages = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = obj.get("type")
                if msg_type not in ("user", "assistant"):
                    continue

                timestamp_str = obj.get("timestamp", "")
                if min_date and timestamp_str:
                    try:
                        ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        if ts < min_date:
                            continue
                    except (ValueError, TypeError):
                        pass

                message = obj.get("message", {})
                text = extract_text(message)
                if not text or len(text.strip()) < 5:
                    continue

                messages.append({
                    "role": msg_type,
                    "text": text,
                    "timestamp": timestamp_str,
                    "session_id": obj.get("sessionId", filepath.stem),
                })
    except (OSError, UnicodeDecodeError):
        pass
    return messages


def search_sessions(query, project_filter=None, days=None, role_filter=None,
                    max_results=10, context_lines=1):
    """Search across all session files."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []
    min_date = None
    if days:
        min_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Find project directories
    if not PROJECTS_DIR.exists():
        print("No projects directory found.", file=sys.stderr)
        return results

    project_dirs = []
    for d in PROJECTS_DIR.iterdir():
        if not d.is_dir():
            continue
        if project_filter:
            if project_filter.lower() not in d.name.lower():
                continue
        project_dirs.append(d)

    if not project_dirs:
        print(f"No projects matching '{project_filter}'", file=sys.stderr)
        return results

    total_files = 0
    for pdir in project_dirs:
        session_files = sorted(pdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        for sf in session_files:
            if "subagent" in sf.name:
                continue
            total_files += 1
            messages = parse_session(sf, min_date)
            for i, msg in enumerate(messages):
                if role_filter and msg["role"] != role_filter:
                    continue
                if pattern.search(msg["text"]):
                    # Get context lines
                    context_before = []
                    context_after = []
                    for j in range(max(0, i - context_lines), i):
                        context_before.append(messages[j])
                    for j in range(i + 1, min(len(messages), i + 1 + context_lines)):
                        context_after.append(messages[j])

                    results.append({
                        "project": pdir.name,
                        "session": sf.stem,
                        "match": msg,
                        "context_before": context_before,
                        "context_after": context_after,
                    })
                    if len(results) >= max_results:
                        return results

    if not results:
        print(f"No matches for '{query}' across {total_files} sessions.", file=sys.stderr)
    return results


def shorten_project_name(raw_name):
    """Shorten a Claude Code project directory name for display.

    Claude Code encodes project paths as directory names using '--' as the
    separator (e.g., 'C--Users--alice--Projects--myapp'). This function
    detects the user's home directory prefix and strips it, producing a
    shorter display name like 'Projects/myapp' or '~/myapp'.
    """
    # Build the home-directory prefix that Claude Code would use.
    # On Windows this looks like 'C--Users--username', on Unix '~--username'
    # or '/home/username' depending on resolution.
    home = Path.home()
    home_encoded = str(home).replace("\\", "/").replace("/", "--").replace(":", "")
    # e.g., "C--Users--alice"

    if raw_name.startswith(home_encoded + "-"):
        remainder = raw_name[len(home_encoded) + 1:]  # strip prefix + separator
        return remainder.replace("-", "/")
    elif raw_name.startswith(home_encoded):
        remainder = raw_name[len(home_encoded):]
        if remainder.startswith("-"):
            remainder = remainder[1:]
        return remainder.replace("-", "/") if remainder else "~"

    # Fallback: return as-is
    return raw_name


def highlight(text, query):
    """Highlight query matches in text."""
    pattern = re.compile(f"({re.escape(query)})", re.IGNORECASE)
    return pattern.sub(r">>> \1 <<<", text)


def format_results(results, query):
    """Format search results for display."""
    for i, r in enumerate(results, 1):
        match = r["match"]
        # Truncate text around match
        text = match["text"]
        match_pos = text.lower().find(query.lower())
        start = max(0, match_pos - 200)
        end = min(len(text), match_pos + len(query) + 200)
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        ts = match["timestamp"][:19] if match["timestamp"] else "?"
        project_short = shorten_project_name(r["project"])

        print(f"\n{'='*70}")
        print(f"[{i}] {project_short} | {ts} | {match['role']}")
        print(f"    Session: {r['session'][:12]}...")

        # Context before
        for ctx in r["context_before"]:
            ctx_snip = ctx["text"][:150].replace("\n", " ")
            print(f"    [{ctx['role']}] {ctx_snip}")

        # The match
        highlighted = highlight(snippet, query).replace("\n", "\n    ")
        print(f"  > {highlighted}")

        # Context after
        for ctx in r["context_after"]:
            ctx_snip = ctx["text"][:150].replace("\n", " ")
            print(f"    [{ctx['role']}] {ctx_snip}")


def main():
    parser = argparse.ArgumentParser(description="Search Claude Code session transcripts")
    parser.add_argument("query", nargs="?", help="Search query (keyword)")
    parser.add_argument("--project", "-p", help="Filter by project name (substring match)")
    parser.add_argument("--days", "-d", type=int, help="Only search last N days")
    parser.add_argument("--role", "-r", choices=["user", "assistant"], help="Filter by message role")
    parser.add_argument("--context", "-c", type=int, default=1, help="Context messages around match (default 1)")
    parser.add_argument("--max", "-m", type=int, default=10, help="Max results (default 10)")
    parser.add_argument("--list-projects", action="store_true", help="List all project directories")
    args = parser.parse_args()

    if args.list_projects:
        list_projects()
        return

    if not args.query:
        parser.print_help()
        return

    results = search_sessions(
        args.query,
        project_filter=args.project,
        days=args.days,
        role_filter=args.role,
        max_results=args.max,
        context_lines=args.context,
    )
    if results:
        format_results(results, args.query)
        print(f"\n--- {len(results)} results ---")


if __name__ == "__main__":
    main()
