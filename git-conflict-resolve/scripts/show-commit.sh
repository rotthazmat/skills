#!/usr/bin/env bash
# Show what a commit changed, optionally scoped to one file.
# Usage: bash scripts/show-commit.sh <hash> [file-path]
set -euo pipefail

HASH="${1:-}"
FILE="${2:-}"

if [[ -z "$HASH" ]]; then
  echo "Error: commit hash required." >&2
  echo "Usage: bash scripts/show-commit.sh <hash> [file-path]" >&2
  exit 1
fi

if [[ -n "$FILE" ]]; then
  echo "=== Line count summary ==="
  git show "$HASH" --stat -- "$FILE"
  echo ""
  echo "=== Full diff ==="
  git show "$HASH" -- "$FILE"
else
  git show "$HASH"
fi
