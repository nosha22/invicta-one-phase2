#!/usr/bin/env bash
# Install the Invicta-One skill fleet into Claude Code's personal skills
# directory (~/.claude/skills/), available in every project. Run: ./install.sh
set -eu
DEST="${HOME}/.claude/skills"
SRC="$(cd "$(dirname "$0")" && pwd)/.claude/skills"
mkdir -p "$DEST"
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  mkdir -p "$DEST/$name"
  cp "$d/SKILL.md" "$DEST/$name/SKILL.md"
  echo "installed: $name -> $DEST/$name/SKILL.md"
done
echo "Done. Restart your Claude Code session - skills are scanned at startup."
