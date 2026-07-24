#!/usr/bin/env python3
"""Heartbeat runner — parse HEARTBEAT.md, run each check, emit anomalies only.

purpose: Silent-by-default proactive monitoring across your projects. Parse the
         check definitions from ~/.claude/HEARTBEAT.md, execute each, collect non-silent
         output, and emit a summary. Exit 0 silently when nothing fires.
inputs: ~/.claude/HEARTBEAT.md
outputs: stdout summary when one or more checks fire; silent exit when all checks pass

Designed to be cron-runnable. Pair with /schedule (Anthropic-managed) or Windows Task
Scheduler. Output can be piped to a messaging integration via:
    python heartbeat.py | python <send-message-script>
(send-message-script not included — wire to your own messaging MCP setup separately)
"""
import re
import subprocess
import sys
from pathlib import Path

HEARTBEAT_PATH = Path.home() / ".claude" / "HEARTBEAT.md"


def parse_checks(path):
    """Extract checks from HEARTBEAT.md. Each check is a fenced block with [check] header."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    # Match fenced code blocks containing `[check] NAME\n...`
    pattern = re.compile(
        r"```\s*\n\[check\]\s*(.+?)\n"           # name
        r"project:\s*(.+?)\n"
        r"description:\s*(.+?)\n"
        r"command:\s*(.+?)\n"
        r"actionable_iff:\s*(.+?)\n"
        r"```",
        re.DOTALL,
    )
    checks = []
    for m in pattern.finditer(text):
        checks.append({
            "name": m.group(1).strip(),
            "project": m.group(2).strip(),
            "description": m.group(3).strip(),
            "command": m.group(4).strip(),
            "actionable_iff": m.group(5).strip(),
        })
    return checks


def run_check(check):
    """Execute a check's command. Returns (output, returncode)."""
    cmd = check["command"]
    if cmd.startswith("TBD") or "TBD" in cmd:
        return "", -1  # skip TBD checks
    try:
        # Expand ~ in commands
        cmd = cmd.replace("~", str(Path.home()))
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                timeout=10, encoding="utf-8", errors="replace")
        return (result.stdout or "").strip(), result.returncode
    except subprocess.TimeoutExpired:
        return f"(timeout after 10s)", 124
    except Exception as e:
        return f"(error: {e})", -1


def is_actionable(check, output, returncode):
    """Apply the actionable_iff condition to determine if this check fires."""
    cond = check["actionable_iff"].lower()
    if "tbd" in cond:
        return False
    # Common conditions:
    if "empty output" in cond:
        # actionable when output is empty (e.g. no recent log file found)
        return not output and returncode == 0
    if "stdout lists" in cond or "stdout contains" in cond:
        return bool(output)
    if "count >" in cond:
        # extract threshold
        m = re.search(r">\s*(\d+)", cond)
        threshold = int(m.group(1)) if m else 0
        try:
            n = int(output)
            return n > threshold
        except ValueError:
            return False
    if "increased" in cond or "grew" in cond:
        # snapshot comparison — needs state file; skip for now
        return False
    # Default: any non-empty stdout means actionable
    return bool(output)


def main():
    checks = parse_checks(HEARTBEAT_PATH)
    if not checks:
        # No checks defined — silent exit
        return 0

    fired = []
    skipped = 0
    for check in checks:
        output, rc = run_check(check)
        if rc == -1 and "TBD" in check["command"]:
            skipped += 1
            continue
        if is_actionable(check, output, rc):
            fired.append((check, output))

    if not fired:
        # Silent — this is the goal state
        return 0

    # Anomalies present — emit summary
    print(f"HEARTBEAT — {len(fired)} actionable check(s) fired"
          + (f" ({skipped} skipped as TBD)" if skipped else ""))
    print()
    for check, output in fired:
        print(f"  [{check['project']}] {check['name']}")
        print(f"    {check['description']}")
        if output:
            preview = (output[:200] + "...") if len(output) > 200 else output
            print(f"    Output: {preview}")
        print()
    return 1  # non-zero exit signals "something fired" for downstream piping


if __name__ == "__main__":
    sys.exit(main())
