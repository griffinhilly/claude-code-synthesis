#!/bin/bash
# PreToolUse hook for Bash: block commands that would display secret file contents in output
# Reads tool event JSON from stdin

INPUT=$(cat)
# python3 first: stock macOS 12.3+ and many Linux distros ship no bare `python`
PY=$(command -v python3 || command -v python) || exit 0
COMMAND=$(echo "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

[ -z "$COMMAND" ] && exit 0

# Normalize for matching
CMD_LOWER=$(echo "$COMMAND" | tr '[:upper:]' '[:lower:]' | sed 's|\\|/|g')

# Intentionally-public template files are fine to display
case "$CMD_LOWER" in
  *".env.example"*|*".env.sample"*|*".env.template"*) exit 0 ;;
esac

# Secret file patterns — anchored enough that ordinary filenames don't trip them
# (bare "token" would block `cat tokenizer_config.json`; "_token"/"token."/"token=" don't).
SECRET_PATTERNS=".secrets/ secrets/ .env _token token. token= slack_token api_key apikey pgpass credentials .pem .key .p12 .pfx"

# Commands that display file contents to stdout
DISPLAY_CMDS="cat head tail less more type"

for pattern in $SECRET_PATTERNS; do
  case "$CMD_LOWER" in
    *"$pattern"*)
      # Check if a display command is used
      for cmd in $DISPLAY_CMDS; do
        case "$CMD_LOWER" in
          *"$cmd "*)
            echo "BLOCKED: Command would display secret/credential file contents in chat." >&2
            echo "To use secrets, read them inside a script (e.g., Python open()) so values stay internal." >&2
            exit 2
            ;;
        esac
      done
      # Also block echo/printf of variables loaded from secret files
      case "$CMD_LOWER" in
        *'echo '*'$'*|*'printf '*'$'*)
          echo "BLOCKED: Command may echo secret values to chat output." >&2
          exit 2
          ;;
      esac
      ;;
  esac
done

exit 0
