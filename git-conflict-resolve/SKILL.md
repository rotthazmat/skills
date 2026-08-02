---
name: git-conflict-resolve
description: Step-by-step process for resolving git cherry-pick and rebase conflicts precisely and safely. Use whenever a cherry-pick or rebase produces a conflict.
compatibility: Requires git
---

Use this skill whenever resolving conflicts during a cherry-pick or rebase. Follow every step in order — do not skip or shortcut.

## Core Principle

**Never let conflict marker blocks drive resolution decisions.** The `<<<<<<< HEAD / ======= / >>>>>>>` presentation is misleading when commits interact. Always go to `git show <hash>` as the source of truth.

---

## Cherry-Pick Conflict Resolution Workflow

1. **Read exactly what the original commit changed:**
   ```
   git show <commit-hash> -- <file>
   ```
   Note every `+` line (added) and every `-` line (removed). This is the only authoritative source.

2. **Check the line-count summary:**
   ```
   git show <commit-hash> --stat
   ```
   Record the exact `-X +Y` count for the conflicted file. Your resolution must match it.

3. **Read the current HEAD version of the conflicted region** — use Read tool on the file to see the exact current state.

4. **Apply only those `+`/`-` lines onto HEAD's structure:**
   - Find where the code currently lives in HEAD (it may have moved from where the original commit expected it).
   - Apply the exact changes from the commit to wherever the code currently lives.
   - Do not move functions, restructure code, or introduce any additional changes.

5. **After staging, verify the diff-line count matches step 2:**
   ```
   git diff --staged -- <file>
   ```
   If the counts don't match, re-examine before proceeding.

6. **Stop and wait for explicit user approval** before running `git commit` or `git cherry-pick --continue`.

---

## Critical Rules

- **Never accept a full function from the incoming conflict side if the commit only changed lines inside it** — apply only the specific `+`/`-` lines to the function where it currently lives.
- **When the incoming conflict side contains a method that already exists elsewhere in HEAD**, discard the incoming side entirely — it's the move operation; don't duplicate.
- **Never drop code from the HEAD side without first confirming the commit explicitly removes it** — check `git show <hash> -- <file>` for a `-` line before discarding anything from HEAD.
- **When resolving conflicts, watch out for code that was moved** — if a method already exists at a different line, it was relocated, not removed. Do not add it as a duplicate.
- **Do not add back anything. Do only what the original commit does.** If HEAD removed surrounding code after the original commit was written, that removal stands.

---

## Rebase Conflict Resolution Workflow

1. Run `git show <commit-hash> -- <file>` to see exactly what the feature commit changed.
2. The correct resolution merges **both** changes — apply your commit's changes on top of what the base branch introduced.
3. Never blindly pick one side — always verify what each commit actually modified.

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it's wrong |
|---|---|
| Reading only the conflict markers | Misleading when commits interact — go to `git show` |
| Accepting the full incoming side | May include unrelated moves or extra context |
| Accepting the full HEAD side | May drop legitimate changes from the cherry-picked commit |
| Adding code back that HEAD removed | HEAD's removal stands regardless of the original commit |
| Duplicating a method that moved | The move is already in HEAD; the method exists, just elsewhere |
| Committing without checking diff count | Undetected extra or missing lines corrupt the history |

## Resources

- **`references/scenarios.md`** — worked examples of the five most common conflict patterns (moved method, renamed surrounding code, deleted method, rebase dual-edit, net-zero series). Load when a conflict scenario is unclear.
- **`scripts/show-commit.sh`** — helper that prints both the stat summary and the full diff for a commit. Run as `bash scripts/show-commit.sh <hash> <file>` instead of running `git show` twice.
- **`evals/evals.json`** — test cases to verify this skill enforces the correct resolution workflow.
