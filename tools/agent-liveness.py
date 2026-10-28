#!/usr/bin/env python3
"""Subagent liveness check — distinguish RUNNING / COMPLETE / STALLED from disk.

purpose: Ground-truth check on background subagents before reporting their status to
         the principal. Reads subagents/agent-*.jsonl transcripts (the ONLY reliable
         liveness signal) and classifies each. The tasks/<id>.output path returned by
         the Agent tool is a decoy: it stays 0 bytes even for agents that finished.
inputs:  ~/.claude/projects/<project-slug>/<session-id>/subagents/agent-*.jsonl
outputs: stdout table, one row per agent; exit 1 if any agent is STALLED
last_run: 2026-09-08 (built after a research agent hung silently for 41 minutes)

Usage:
    python agent-liveness.py                      # newest session of newest project
    python agent-liveness.py --project myproj     # substring match on project slug
    python agent-liveness.py --all                # every session dir of that project
    python agent-liveness.py --stall-secs 600     # custom stall threshold

Verdict logic (why an agent stopped writing matters more than that it stopped):
    RUNNING  - wrote recently (idle < stall threshold)
    COMPLETE - last record is a final assistant message with text and no pending tool call
    STALLED  - last record is a tool result with no assistant turn after it, and idle
               past the threshold. This is the silent-hang shape: all tool results
               land, the model turn never comes, nothing times out, no notification
               fires. Relaunch rather than resume.
"""
import argparse
import json
import sys
import time
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def last_records(path, tail=400):
    """Parse the trailing records of a jsonl transcript, tolerating partial lines."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for line in lines[-tail:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue
    return out


def blocks(rec):
    content = (rec.get("message") or {}).get("content")
    return content if isinstance(content, list) else []


def classify(recs, idle, stall_secs):
    """Return (verdict, detail)."""
    # Bookkeeping records (summaries, system notes) say nothing about liveness
    recs = [r for r in recs if r.get("type") in ("user", "assistant")]
    if not recs:
        return "EMPTY", "no parseable records"

    last = recs[-1]
    kinds = [b.get("type") for b in blocks(last)]
    if last.get("type") == "assistant" and "tool_use" not in kinds:
        return "COMPLETE", "ended on a final assistant turn"
    if idle < stall_secs:
        return "RUNNING", "writing recently"

    if "tool_use" in kinds:
        names = [b.get("name") for b in blocks(last) if b.get("type") == "tool_use"]
        return "STALLED", (f"tool call issued, no result: {', '.join(filter(None, names))} "
                           f"(or a long tool call / pending permission prompt; check before relaunching)")
    if "tool_result" in kinds:
        return "STALLED", "tool result received, no assistant turn followed"

    return "STALLED", f"ended on a '{last.get('type')}' record with no reply"


def tool_calls(recs):
    return sum(
        1 for r in recs for b in blocks(r) if b.get("type") == "tool_use"
    )


def find_session_dirs(project_filter, want_all):
    if not PROJECTS.is_dir():
        return []
    slugs = [p for p in PROJECTS.iterdir() if p.is_dir()]
    if project_filter:
        needle = project_filter.lower()
        slugs = [p for p in slugs if needle in p.name.lower()]
    if not slugs:
        return []

    dirs = []
    for slug in slugs:
        sessions = [d for d in slug.iterdir() if d.is_dir() and (d / "subagents").is_dir()]
        if not sessions:
            continue
        sessions.sort(key=lambda d: (d / "subagents").stat().st_mtime, reverse=True)
        dirs.extend(sessions if want_all else sessions[:1])

    if not project_filter and not want_all and dirs:
        dirs.sort(key=lambda d: (d / "subagents").stat().st_mtime, reverse=True)
        dirs = dirs[:1]
    return dirs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", help="substring match on the project slug")
    ap.add_argument("--all", action="store_true", help="all session dirs, not just newest")
    ap.add_argument("--stall-secs", type=int, default=300,
                    help="idle seconds before a non-final transcript counts as stalled")
    args = ap.parse_args()

    session_dirs = find_session_dirs(args.project, args.all)
    if not session_dirs:
        print("No session directories with subagents found.")
        return 0

    now = time.time()
    rows = []
    for sd in session_dirs:
        for f in sorted((sd / "subagents").glob("agent-*.jsonl")):
            idle = now - f.stat().st_mtime
            recs = last_records(f)
            verdict, detail = classify(recs, idle, args.stall_secs)
            rows.append({
                "session": sd.name[:8],
                "agent": f.stem.replace("agent-", "")[:12],
                "kb": f.stat().st_size / 1024,
                "idle_min": idle / 60,
                "tools": tool_calls(recs),
                "verdict": verdict,
                "detail": detail,
            })

    if not rows:
        print("No subagent transcripts found.")
        return 0

    order = {"STALLED": 0, "RUNNING": 1, "EMPTY": 2, "COMPLETE": 3}
    rows.sort(key=lambda r: (order.get(r["verdict"], 9), -r["idle_min"]))

    print(f"{'SESSION':<10}{'AGENT':<14}{'VERDICT':<10}{'KB':>9}{'IDLE_MIN':>10}{'TOOLS':>7}  DETAIL")
    print("-" * 110)
    for r in rows:
        print(f"{r['session']:<10}{r['agent']:<14}{r['verdict']:<10}{r['kb']:>9.1f}"
              f"{r['idle_min']:>10.1f}{r['tools']:>7}  {r['detail']}")

    stalled = [r for r in rows if r["verdict"] == "STALLED"]
    if stalled:
        print()
        print(f"{len(stalled)} STALLED. Relaunch fresh (the prompt is line 1 of the "
              f"transcript); do not report these as 'still running'.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
