#!/bin/bash
# PreToolUse hook for Bash: block commands that would display secret file contents in output
# Reads tool event JSON from stdin

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

[ -z "$COMMAND" ] && exit 0

# Normalize for matching
CMD_LOWER=$(echo "$COMMAND" | tr '[:upper:]' '[:lower:]' | sed 's|\\|/|g')

# Secret file patterns
SECRET_PATTERNS=".secrets/ secrets/ .env token slack_token api_key apikey pgpass credentials .pem .key .p12 .pfx"

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
