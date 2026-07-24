#!/bin/bash
# Self-test harness for the hooks in this directory.
# Run after any hook edit: bash hooks/test-hooks.sh
# Each case feeds the hook the same JSON the Claude Code harness would send
# and asserts the exit code (0 = allow, 2 = block).
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python) || { echo "no python found"; exit 1; }
FAILS=0
t() { local desc="$1" hook="$2" json="$3" expect="$4"; out=$(echo "$json" | bash "$hook" 2>&1); rc=$?
  if [ "$rc" = "$expect" ]; then echo "PASS ($rc): $desc"; else echo "FAIL (got $rc want $expect): $desc | $out"; FAILS=$((FAILS+1)); fi; }
j() { "$PY" -c "import json,sys; print(json.dumps({'tool_input':{'command':sys.argv[1]}}))" "$1"; }
jr() { "$PY" -c "import json,sys; print(json.dumps({'tool_input':{'file_path':sys.argv[1]}}))" "$1"; }

t "plain git commit exempt" warn-destructive.sh "$(j 'git commit -m "fix rm -rf docs"')" 0
t "commit chained with rm -rf blocked" warn-destructive.sh "$(j 'git commit -m "x" && rm -rf ~/stuff')" 2
t "safe rm -rf allowed" warn-destructive.sh "$(j 'rm -rf node_modules')" 0
t "safe+unsafe rm -rf blocked" warn-destructive.sh "$(j 'rm -rf node_modules && rm -rf ~/important')" 2
t "push feature branch with -f in name allowed" warn-destructive.sh "$(j 'git push origin my-feature-branch')" 0
t "push --force blocked" warn-destructive.sh "$(j 'git push --force origin main')" 2
t "push -f blocked" warn-destructive.sh "$(j 'git push -f')" 2
t "truncate flag allowed" warn-destructive.sh "$(j 'somecmd --truncate-long-lines file')" 0
t "TRUNCATE TABLE blocked" warn-destructive.sh "$(j "psql -c 'TRUNCATE TABLE users'")" 2
t "branch long-form force delete blocked" warn-destructive.sh "$(j 'git branch --delete --force old')" 2

t "cat tokenizer config allowed" block-secret-bash.sh "$(j 'cat tokenizer_config.json')" 0
t "cat dotenv blocked" block-secret-bash.sh "$(j 'cat .env')" 2
t "cat dotenv example allowed" block-secret-bash.sh "$(j 'cat .env.example')" 0
t "cat pgpass blocked" block-secret-bash.sh "$(j 'cat /home/u/pgpass.conf')" 2

t "read dotenv blocked" block-secret-reads.sh "$(jr '/home/u/.env')" 2
t "read dotenv example allowed" block-secret-reads.sh "$(jr '/home/u/.env.example')" 0
t "read docs-about-keys md allowed" block-secret-reads.sh "$(jr '/docs/api_key_rotation_notes.md')" 0
t "read private key blocked" block-secret-reads.sh "$(jr '/home/u/id_rsa.key')" 2

HOME_BAK="$HOME"; export HOME="$(mktemp -d)"   # keep test entry out of the real skill-usage.log
t "skill log runs" log-skill-usage.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'skill':'hooktest'}}))")" 0
export HOME="$HOME_BAK"

t "epistemic guard warns not blocks" epistemic-guard.sh "$("$PY" -c "import json; print(json.dumps({'tool_input':{'content':'this should work fine'}}))")" 0

echo "---"
echo "$FAILS failures"
exit $((FAILS > 0))
