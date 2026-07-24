#!/usr/bin/env python3
"""Find stub/mock/placeholder/TODO patterns in a project.

purpose: Deterministic audit for accumulated code debt — short functions that may be stubs,
         placeholder return values, TODO/FIXME/XXX comments, future-tense narration in
         comments ("will return", "would handle"), and explicit mock/stub/placeholder words.
inputs: project directory (defaults to cwd)
outputs: JSON report or human summary; suspicious patterns by file/line

This is deterministic — same input produces same output. Latent judgment of "which findings
matter" lives elsewhere (e.g. a /simplify --placeholder-audit follow-up that filters the JSON).
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

STUB_BODY_PATTERNS = [
    "pass",
    "...",
    "return None",
    "return",
    "raise NotImplementedError",
]

PLACEHOLDER_WORDS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bXXX\b",
    r"\bHACK\b",
    r"\bmock\b",
    r"\bstub\b",
    r"\bplaceholder\b",
    r"\bdummy\b",
]

FUTURE_TENSE_COMMENT = re.compile(
    r"#.*\b(will|would|should be|to be|planned|coming soon|not yet)\b",
    re.IGNORECASE,
)

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
             ".mypy_cache", "dist", "build", ".next", ".cache", "vault", "media"}


def is_stub_function(node):
    """Heuristic: function body is suspiciously short or matches stub patterns."""
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None
    body = node.body
    # Strip docstring if present
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        body = body[1:]
    if not body:
        return "empty body after docstring"
    # Single-statement bodies are suspect
    if len(body) == 1:
        s = body[0]
        if isinstance(s, ast.Pass):
            return "body is `pass`"
        if isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis:
            return "body is `...`"
        if isinstance(s, ast.Return) and (s.value is None or
                                          (isinstance(s.value, ast.Constant) and s.value.value is None)):
            return "body is `return None`"
        if isinstance(s, ast.Raise):
            exc = s.exc
            if isinstance(exc, ast.Call) and getattr(exc.func, "id", "") == "NotImplementedError":
                return "body raises NotImplementedError"
            if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
                return "body raises NotImplementedError"
    # Short bodies (≤2 lines) get a soft flag
    if len(body) <= 2:
        return None  # too noisy to flag — only flag the explicit stub patterns above
    return None


def scan_python_file(path):
    """Return list of findings for a single Python file."""
    findings = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{"kind": "read_error", "msg": str(e)}]
    # AST-based stub detection
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            stub_reason = is_stub_function(node)
            if stub_reason:
                findings.append({
                    "kind": "stub_function",
                    "name": node.name,
                    "line": node.lineno,
                    "reason": stub_reason,
                })
    except SyntaxError as e:
        findings.append({"kind": "syntax_error", "line": e.lineno, "msg": e.msg})
    # Regex-based placeholder/future-tense detection
    for line_no, line in enumerate(src.splitlines(), 1):
        for pat in PLACEHOLDER_WORDS:
            if re.search(pat, line):
                findings.append({
                    "kind": "placeholder_word",
                    "line": line_no,
                    "word": re.search(pat, line).group(0),
                    "text": line.strip()[:120],
                })
                break  # one per line is enough
        if FUTURE_TENSE_COMMENT.search(line):
            findings.append({
                "kind": "future_tense_comment",
                "line": line_no,
                "text": line.strip()[:120],
            })
    return findings


def scan_non_python(path):
    """Regex-only scan for non-Python files (JS, TS, sh, md, etc.)."""
    findings = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for line_no, line in enumerate(src.splitlines(), 1):
        for pat in PLACEHOLDER_WORDS:
            if re.search(pat, line):
                findings.append({
                    "kind": "placeholder_word",
                    "line": line_no,
                    "word": re.search(pat, line).group(0),
                    "text": line.strip()[:120],
                })
                break
    return findings


def walk_project(root, include_non_py=False):
    """Yield (path, findings) for each file with findings."""
    for path in Path(root).rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix == ".py":
            findings = scan_python_file(path)
        elif include_non_py and path.suffix in {".js", ".ts", ".tsx", ".jsx", ".sh", ".md"}:
            findings = scan_non_python(path)
        else:
            continue
        if findings:
            yield path, findings


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", nargs="?", default=".", help="Project root (default: cwd)")
    parser.add_argument("--out", help="Write JSON to this path")
    parser.add_argument("--human", action="store_true", help="Print human-readable summary")
    parser.add_argument("--include-non-py", action="store_true",
                        help="Also scan .js/.ts/.sh/.md files (regex only)")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 1

    report = {"root": str(root), "files": [], "summary": {}}
    counts = {"stub_function": 0, "placeholder_word": 0,
              "future_tense_comment": 0, "syntax_error": 0}
    for path, findings in walk_project(root, args.include_non_py):
        rel = str(path.relative_to(root)).replace("\\", "/")
        report["files"].append({"path": rel, "findings": findings})
        for f in findings:
            kind = f.get("kind")
            counts[kind] = counts.get(kind, 0) + 1
    report["summary"] = counts

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report written to {args.out}", file=sys.stderr)

    if args.human or not args.out:
        print(f"Scanned: {root}")
        print(f"Files with findings: {len(report['files'])}")
        print(f"Counts: stubs={counts['stub_function']}, "
              f"placeholders={counts['placeholder_word']}, "
              f"future-tense={counts['future_tense_comment']}, "
              f"syntax-errors={counts['syntax_error']}")
        # Top 10 noisiest files
        if report["files"]:
            sorted_files = sorted(report["files"],
                                  key=lambda x: len(x["findings"]), reverse=True)[:10]
            print("\nTop files by finding count:")
            for f in sorted_files:
                print(f"  {len(f['findings']):>4}  {f['path']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
