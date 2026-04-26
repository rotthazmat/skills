---
name: git-workflow
description: Git workflow rules — branch safety, commit discipline, and cherry-pick verification. Use before any git commit, cherry-pick, or branch operation.
compatibility: Requires git
---

Apply these rules to all git operations.

## Branch Safety

- **Always run `git branch --show-current`** before any git operation involving the current branch — never assume which branch is active.

## Committing

- **Never commit without explicit user approval** — after staging files, stop and wait for confirmation before running `git commit`.
- **Never continue a cherry-pick without explicit user approval** — after resolving a conflict and staging the file, stop and wait for confirmation before running `git cherry-pick --continue`.

## Verification After Cherry-Pick

- **After cherry-picking multiple commits, verify the net diff** — run `git diff HEAD~N HEAD --stat` to confirm only the expected files changed.
- If a series of commits introduces and then reverts changes to a file, the net result should show no diff for that file.
- **When a series of commits moves a function and then moves it back, the net result must be no change to that function's location** — track cumulative state across all commits being cherry-picked.

## Resources

- **`scripts/check-branch.sh`** — run before any branch operation to print the current branch and catch detached HEAD state.
- **`evals/evals.json`** — test cases to verify this skill enforces correct workflow discipline.
