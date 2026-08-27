#!/usr/bin/env bash
#
# Symlinks this skills/ repo into ~/.claude/skills and ~/.agents/skills.
#
# Creates (or recreates) a "skills" symlink inside both ~/.claude and ~/.agents
# pointing at this repository. Missing ~/.claude or ~/.agents directories are
# created. An existing symlink is replaced; an existing real folder is left
# untouched and reported as an error.
#
# Compatible with bash and zsh.

set -eu

# On Windows Git Bash / MSYS, ask for real native symlinks instead of copies.
case "${MSYS:-}" in
  *winsymlinks*) : ;;
  *) export MSYS="winsymlinks:nativestrict${MSYS:+ $MSYS}" ;;
esac

# Resolve the directory this script lives in (bash or zsh).
if [ -n "${BASH_SOURCE:-}" ]; then
  self="${BASH_SOURCE[0]}"
elif [ -n "${ZSH_VERSION:-}" ]; then
  self="${(%):-%N}"
else
  self="$0"
fi
SOURCE_DIR="$(cd "$(dirname "$self")" && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

red()   { printf '%b%s%b\n' "$RED" "$1" "$NC" >&2; }
green() { printf '%b%s%b\n' "$GREEN" "$1" "$NC"; }
cyan()  { printf '%b%s%b\n' "$CYAN" "$1" "$NC"; }

exit_code=0

for name in .claude .agents; do
  base="$HOME/$name"

  if [ ! -d "$base" ]; then
    mkdir -p "$base"
    cyan "Created $base"
  fi

  link="$base/skills"

  if [ -L "$link" ]; then
    rm -f "$link"
    cyan "Removed existing symlink $link"
  elif [ -e "$link" ]; then
    red "There's already a skills/ folder inside $base"
    exit_code=1
    continue
  fi

  ln -s "$SOURCE_DIR" "$link"
  green "Linked $link -> $SOURCE_DIR"
done

exit "$exit_code"
