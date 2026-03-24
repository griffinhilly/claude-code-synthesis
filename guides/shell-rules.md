# Shell Command Style Rules

Claude Code's security scanner flags commands that appear to contain "quoted characters
in flag names" (OBFUSCATED_FLAGS). To avoid these false-positive prompts, follow these
rules when generating bash commands:

## 1. Never wrap flags in quotes
Flags (arguments starting with `-`) must never be enclosed in quotes.

```bash
# WRONG - quoted flag triggers scanner
command '-n' 5 file.txt
command "-rf" directory

# RIGHT - flags are bare
command -n 5 file.txt
command -rf directory
```

## 2. Never place quotes immediately before a dash-flag
A quote character (`'`, `"`, or backtick) directly before a `-` triggers the scanner.

```bash
# WRONG - quote immediately before dash
echo "hello""-world"
value="test"  "-flag"

# RIGHT - separate with space, no quotes on flags
echo "hello" -n "world"
```

## 3. Avoid ANSI-C quoting ($'...') and locale quoting ($"...")
These patterns are flagged by the scanner as potentially hiding characters.

```bash
# WRONG - $'...' ANSI-C quoting triggers scanner
echo $'\t' file.txt
grep $'\n' file.txt

# RIGHT - use standard quoting or literal characters
printf '\t' file.txt
echo -e "\t" file.txt
```

## 4. Never use empty quotes before a dash
Empty quote pairs before a dash-flag are flagged.

```bash
# WRONG
command "" -flag
command '' -n

# RIGHT
command -flag
command -n
```

## 5. Git commit messages must not start with a dash
When the `-m` message begins with `-`, the scanner flags it as a potential obfuscated flag.

```bash
# WRONG - message starts with dash
git commit -m "-fix typo"
git commit -m '--update config'

# RIGHT - rephrase so message doesn't start with dash
git commit -m "Fix typo"
git commit -m "Update config"
```

## 6. Use HEREDOCs for git commit messages with special characters
For multi-line or complex commit messages, use the HEREDOC pattern with a **quoted
or escaped delimiter** to avoid all quoting issues:

```bash
git commit -m "$(cat <<'EOF'
Summary of changes here.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 7. For cut delimiter with quote characters, the scanner has an exception
`cut -d'"'` and `cut -d"'"` are explicitly allowed. No workaround needed.

## 8. Prefer simple quoting strategies
When a command needs quoted arguments alongside flags, put flags first (unquoted),
then quoted data arguments:

```bash
# GOOD - flags bare, data quoted
grep -r -n "search term" /path/to/dir
python -c "print('hello')"
head -4 "/path/with spaces/file.csv"

# AVOID - interleaving quotes and flags in confusing ways
grep "-r" "-n" "search term" /path/to/dir
```
