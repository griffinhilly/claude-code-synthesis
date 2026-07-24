#!/usr/bin/env python3
"""
List Claude Code sessions with auto-generated descriptions.

Scans ~/.claude/projects/*/*.jsonl (top-level session files only; excludes
subagents/ and workflows/). Description = the session's own `aiTitle` record,
falling back to the first real user prompt.

Usage:
    python3 list_sessions.py [DAYS] [--project SUBSTR] [--md] [--all]

    DAYS            look-back window in days (default 7). Ignored with --all.
    --project STR   only sessions whose cwd contains STR (case-insensitive)
    --md            emit a GitHub-flavored markdown table (default: aligned text)
    --all           ignore the DAYS window; list every session on disk

Inputs:  ~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl
Outputs: stdout table (session id, last-active, cwd, turns, description)
"""
import json, glob, os, sys, time, datetime

def parse_args(argv):
    days, project, md, show_all = 7, None, False, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--project':
            i += 1; project = argv[i].lower()
        elif a == '--md':
            md = True
        elif a == '--all':
            show_all = True
        elif a.isdigit():
            days = int(a)
        i += 1
    return days, project, md, show_all

def first_user_text(msg):
    c = msg.get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        for blk in c:
            if isinstance(blk, dict) and blk.get('type') == 'text':
                return blk.get('text', '')
    return ''

def clean(s, n=None):
    s = ' '.join((s or '').split())
    return s[:n] if n else s

def scan(path):
    ai_title = first_prompt = cwd = start_ts = None
    turns = 0
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get('type')
            if t == 'ai-title' and not ai_title:
                ai_title = d.get('aiTitle')
            elif t == 'user' and not d.get('isMeta'):
                if cwd is None:
                    cwd = d.get('cwd')
                if start_ts is None and d.get('timestamp'):
                    start_ts = d['timestamp']
                txt = first_user_text(d.get('message', {}))
                if txt and not txt.startswith('<') and not txt.startswith('Caveat'):
                    turns += 1
                    if first_prompt is None:
                        first_prompt = txt
    return ai_title, first_prompt, cwd, turns

def main():
    days, project, md, show_all = parse_args(sys.argv[1:])
    root = os.path.expanduser('~/.claude/projects')
    cutoff = 0 if show_all else time.time() - days * 86400
    rows = []
    for path in glob.glob(os.path.join(root, '*', '*.jsonl')):
        mt = os.path.getmtime(path)
        if mt < cutoff:
            continue
        ai_title, first_prompt, cwd, turns = scan(path)
        if project and project not in (cwd or '').lower():
            continue
        rows.append({
            'sid': os.path.basename(path)[:-6],
            'last': datetime.datetime.fromtimestamp(mt),
            'cwd': cwd or '(unknown)',
            'turns': turns,
            'desc': clean(ai_title or first_prompt or '(no prompt)'),
        })
    rows.sort(key=lambda r: r['last'], reverse=True)

    scope = 'all time' if show_all else f'last {days} days'
    if project:
        scope += f", project~='{project}'"
    print(f"\n{len(rows)} sessions ({scope})\n")

    if md:
        print("| Last active | Turns | Session ID | cwd | Description |")
        print("|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['last']:%Y-%m-%d %H:%M} | {r['turns']} | `{r['sid']}` | {r['cwd']} | {clean(r['desc'],120)} |")
    else:
        print(f"{'LAST ACTIVE':<17}{'TURNS':>6}  {'SESSION ID':<38}DESCRIPTION")
        print('-' * 130)
        for r in rows:
            print(f"{r['last']:%Y-%m-%d %H:%M}  {r['turns']:>4}  {r['sid']:<38}{clean(r['desc'],78)}")
    print(f"\nResume a session:  claude --resume <SESSION ID>")

if __name__ == '__main__':
    main()
