#!/usr/bin/env bash
# Print the current branch before a git operation.
set -euo pipefail

branch=$(git branch --show-current)

if [[ -z "$branch" ]]; then
  echo "ERROR: Not on any branch (detached HEAD state)." >&2
  exit 1
fi

echo "Current branch: $branch"
