#!/usr/bin/env bash
# Install this setup into ~/.claude by symlink, so edits here take effect immediately.
# Idempotent. Existing real files are backed up, never overwritten.
#
#   ./install.sh           install into ~/.claude
#   ./install.sh --check   report what is linked, change nothing
#   CLAUDE_HOME=/path ./install.sh   install elsewhere

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${CLAUDE_HOME:-$HOME/.claude}"
STAMP="$(date +%Y%m%d-%H%M%S)"
MODE="${1:-install}"

check_one() {
    local src="$1" dst="$2"
    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
        echo "  ok       $dst"
    elif [ -e "$dst" ]; then
        echo "  DIFFERS  $dst"
    else
        echo "  missing  $dst"
    fi
}

link_one() {
    local src="$1" dst="$2"
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
        mv "$dst" "$dst.backup-$STAMP"
        echo "  backed up $dst -> $(basename "$dst").backup-$STAMP"
    fi
    ln -sfn "$src" "$dst"
    echo "  linked   $dst"
}

apply() {
    local action="$1"
    "$action" "$REPO/CLAUDE.md" "$TARGET/CLAUDE.md"
    "$action" "$REPO/CONVENTIONS.md" "$TARGET/CONVENTIONS.md"
    "$action" "$REPO/ENVIRONMENTS.md" "$TARGET/ENVIRONMENTS.md"
    # settings.json is written by the app itself. If it is ever replaced by a real
    # file instead of this symlink, --check reports it as DIFFERS.
    "$action" "$REPO/settings.json" "$TARGET/settings.json"
    "$action" "$REPO/notify.js" "$TARGET/notify.js"
    "$action" "$REPO/scripts/notify.sh" "$TARGET/scripts/notify.sh"
    local skill name
    for skill in "$REPO"/skills/x*/; do
        [ -d "$skill" ] || continue
        name="$(basename "$skill")"
        "$action" "${skill%/}" "$TARGET/skills/$name"
    done
}

if [ "$MODE" = "--check" ]; then
    echo "checking $TARGET against $REPO"
    apply check_one
    exit 0
fi

echo "installing $REPO into $TARGET"
mkdir -p "$TARGET/skills" "$TARGET/scripts"
apply link_one
echo "done. skills linked: $(find "$TARGET/skills" -maxdepth 1 -name 'x*' | wc -l | tr -d ' ')"
echo "Restart Claude Code for the skills to appear in the slash menu."
