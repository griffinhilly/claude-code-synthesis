#!/bin/bash
# Self-test harness for the hooks in this directory — all 10 hooks covered.
# Run after any hook edit: bash hooks/test-hooks.sh
# Each case feeds the hook the same JSON the Claude Code harness would send
# and asserts the exit code (0 = allow/silent, 2 = block or model-visible notice).
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python) || { echo "no python found"; exit 1; }
FAILS=0
t() { local desc="$1" hook="$2" json="$3" expect="$4"; out=$(echo "$json" | bash "$hook" 2>&1); rc=$?
  if [ "$rc" = "$expect" ]; then echo "PASS ($rc): $desc"; else echo "FAIL (got $rc want $expect): $desc | $out"; FAILS=$((FAILS+1)); fi; }
j() { "$PY" -c "import json,sys; print(json.dumps({'tool_input':{'command':sys.argv[1]}}))" "$1"; }
jf() { "$PY" -c "import json,sys; print(json.dumps({'tool_input':{'file_path':sys.argv[1]}}))" "$1"; }

echo "── warn-destructive ──"
t "plain git commit exempt" warn-destructive.sh "$(j 'git commit -m "fix rm -rf docs"')" 0
t "chained commit message exempt" warn-destructive.sh "$(j 'git add x && git commit -m "cleanup: rm -rf old docs"')" 0
t "commit chained with real rm -rf blocked" warn-destructive.sh "$(j 'git commit -m "x" && rm -rf ~/stuff')" 2
t "safe rm -rf allowed" warn-destructive.sh "$(j 'rm -rf node_modules')" 0
t "safe rm -rf with ./ prefix allowed" warn-destructive.sh "$(j 'rm -rf ./node_modules')" 0
t "multi-target rm -rf blocked (one command)" warn-destructive.sh "$(j 'rm -rf node_modules ~/important')" 2
t "chained safe+unsafe rm -rf blocked" warn-destructive.sh "$(j 'rm -rf node_modules && rm -rf ~/important')" 2
t "rm -fr flag order blocked" warn-destructive.sh "$(j 'rm -fr ~/stuff')" 2
t "rm -r -f split flags blocked" warn-destructive.sh "$(j 'rm -r -f ~/stuff')" 2
t "rm --recursive --force blocked" warn-destructive.sh "$(j 'rm --recursive --force ~/stuff')" 2
t "push feature branch with -f in name allowed" warn-destructive.sh "$(j 'git push origin my-feature-branch')" 0
t "push --force blocked" warn-destructive.sh "$(j 'git push --force origin main')" 2
t "push -f blocked" warn-destructive.sh "$(j 'git push -f')" 2
t "truncate flag allowed" warn-destructive.sh "$(j 'somecmd --truncate-long-lines file')" 0
t "TRUNCATE TABLE blocked" warn-destructive.sh "$(j 'run_sql TRUNCATE TABLE users')" 2
t "echo about DROP TABLE in quotes allowed" warn-destructive.sh "$(j 'echo "never run DROP TABLE manually"')" 0
t "branch long-form force delete blocked" warn-destructive.sh "$(j 'git branch --delete --force old')" 2

echo "── block-secret-bash ──"
t "cat tokenizer config allowed" block-secret-bash.sh "$(j 'cat tokenizer_config.json')" 0
t "cat dotenv blocked" block-secret-bash.sh "$(j 'cat .env')" 2
t "cat dotenv example allowed" block-secret-bash.sh "$(j 'cat .env.example')" 0
t "dotenv example chained with real dotenv blocked" block-secret-bash.sh "$(j 'cat .env.example && cat .env')" 2
t "grep on dotenv blocked" block-secret-bash.sh "$(j 'grep . .env')" 2
t "sed on pgpass blocked" block-secret-bash.sh "$(j 'sed -n 1p pgpass.conf')" 2
t "cat pgpass blocked" block-secret-bash.sh "$(j 'cat /home/u/pgpass.conf')" 2

echo "── block-secret-reads ──"
t "read dotenv blocked" block-secret-reads.sh "$(jf '/home/u/.env')" 2
t "read dotenv example allowed" block-secret-reads.sh "$(jf '/home/u/.env.example')" 0
t "read credentials.md blocked (no md carve-out)" block-secret-reads.sh "$(jf '/notes/credentials.md')" 2
t "read passwords file blocked" block-secret-reads.sh "$(jf '/home/u/passwords.txt')" 2
t "read ordinary README allowed" block-secret-reads.sh "$(jf '/project/README.md')" 0
t "read private key blocked" block-secret-reads.sh "$(jf '/home/u/id_rsa.key')" 2

echo "── check-staged-secrets ──"
t "git add -A blocked" check-staged-secrets.sh "$(j 'git add -A')" 2
t "git add . blocked" check-staged-secrets.sh "$(j 'git add .')" 2
t "git add . chained blocked" check-staged-secrets.sh "$(j 'git add . && git status')" 2
t "git add .gitignore allowed" check-staged-secrets.sh "$(j 'git add .gitignore')" 0
t "git add ./src allowed" check-staged-secrets.sh "$(j 'git add ./src/main.py')" 0
t "non-git command passes through" check-staged-secrets.sh "$(j 'ls -la')" 0

echo "── log-skill-usage ──"
LOG_HOME="$(mktemp -d)"; mkdir -p "$LOG_HOME/.claude"
HOME_BAK="$HOME"; export HOME="$LOG_HOME"
t "skill invocation logged" log-skill-usage.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'skill':'hooktest'},'session_id':'sess-123'}))")" 0
export HOME="$HOME_BAK"
if grep -q 'hooktest' "$LOG_HOME/.claude/skill-usage.log" 2>/dev/null; then
  echo "PASS (log): skill-usage.log received the entry"
else
  echo "FAIL (log): skill-usage.log missing or empty"; FAILS=$((FAILS+1))
fi
rm -rf "$LOG_HOME"

echo "── log-unwrapped-session ──"
t "home-dir session exempt" log-unwrapped-session.sh "$("$PY" -c "import json,os; print(json.dumps({'cwd': os.path.expanduser('~')}))")" 0
t "non-git cwd exits clean" log-unwrapped-session.sh "$("$PY" -c "import json,tempfile; print(json.dumps({'cwd': tempfile.gettempdir()}))")" 0

echo "── epistemic-guard (PostToolUse: 2 = notice, not block) ──"
t "hedge phrase triggers notice" epistemic-guard.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'content':'this should work fine'}}))")" 2
t "clean content silent" epistemic-guard.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'content':'verified by running the test suite; all 20 cases pass'}}))")" 0
t "ordinary hedge words no longer trip it" epistemic-guard.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'content':'the cause might be a race; it appears to involve the cache'}}))")" 0

echo "── warn-skill-md-too-long (PostToolUse: 2 = notice) ──"
SKILL_HOME="$(mktemp -d)"; mkdir -p "$SKILL_HOME/.claude/skills/big"
# Create fixtures with shell, not python: on Git Bash a Windows python can't
# resolve the POSIX-virtual mktemp path, and the fixture silently isn't created.
yes line | head -200 > "$SKILL_HOME/.claude/skills/big/SKILL.md"
t "oversized SKILL.md triggers notice" warn-skill-md-too-long.sh "$(jf "$SKILL_HOME/.claude/skills/big/SKILL.md")" 2
yes line | head -50 > "$SKILL_HOME/.claude/skills/big/SKILL.md"
t "small SKILL.md silent" warn-skill-md-too-long.sh "$(jf "$SKILL_HOME/.claude/skills/big/SKILL.md")" 0
t "non-skill file ignored" warn-skill-md-too-long.sh "$(jf '/project/notes.md')" 0
rm -rf "$SKILL_HOME"

echo "── check-new-file-index (PostToolUse: 2 = notice) ──"
IDX_DIR="$(mktemp -d)"; touch "$IDX_DIR/INDEX.md"
t "new file under INDEX.md dir triggers notice" check-new-file-index.sh "$(jf "$IDX_DIR/newfile.py")" 2
t "excluded file type silent" check-new-file-index.sh "$(jf "$IDX_DIR/README.md")" 0
rm -rf "$IDX_DIR"

echo "── post-compact-reminder ──"
t "runs clean on compact event" post-compact-reminder.sh "$("$PY" -c "import json; print(json.dumps({'trigger':'auto'}))")" 0

echo "---"
echo "$FAILS failures"
exit $((FAILS > 0))
