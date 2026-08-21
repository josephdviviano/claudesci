#!/bin/bash
# Claude Code notification helper
# - Identifies which iTerm2 session raised the notification (via TTY)
# - On click, focuses the exact iTerm2 tab/window

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"

# Mode: focus a specific iTerm2 session by TTY (called on notification click)
if [ "$1" = "--focus" ]; then
    tty_path="$2"
    osascript <<APPLESCRIPT
tell application "iTerm2"
    repeat with w in windows
        tell w
            repeat with t in tabs of w
                repeat with s in sessions of t
                    if tty of s is "$tty_path" then
                        select t
                        set index of w to 1
                    end if
                end repeat
            end repeat
        end tell
    end repeat
    activate
end tell
APPLESCRIPT
    exit 0
fi

# Normal mode: called by Claude Code hook, reads JSON from stdin
input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd // empty')
project=$(basename "${cwd:-unknown}")
message="${1:-Claude needs your attention}"

# Find the TTY of our ancestor process (the Claude Code session's terminal)
tty_name=""
pid=$$
while [ "$pid" -gt 1 ]; do
    t=$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')
    if [ -n "$t" ] && [ "$t" != "??" ] && [ "$t" != "?" ]; then
        tty_name="$t"
        break
    fi
    pid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')
done

tty_path="/dev/${tty_name}"

# Send notification; clicking it will run this script in --focus mode
terminal-notifier \
    -title "Claude Code [$project]" \
    -message "$message" \
    -execute "$SCRIPT_PATH --focus $tty_path" \
    -sound default &
