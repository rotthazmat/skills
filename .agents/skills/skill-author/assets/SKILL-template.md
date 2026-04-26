---
name: skill-name
description: One sentence on what this skill does. Use when the user asks about X, Y, or Z.
# compatibility: Requires git        # uncomment if the skill needs specific tools
# license: MIT                       # uncomment to declare a license
---

Brief one-paragraph summary of what this skill does and when it applies.

---

## [Main section — e.g. Workflow / Rules / Process]

[Core instructions. Write only what the model wouldn't know without this skill.
Steps for workflows, rules for style/conventions, gotchas for non-obvious behavior.]

---

## Gotchas

[Things the model will get wrong without being told. Each entry: what to do and why.]

- **[Non-obvious rule]** — [why it exists or what goes wrong without it]

---

## Anti-patterns to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| [Bad approach] | [Consequence] |

---

## Resources

- **`references/[file].md`** — [what it contains]. Load when [specific trigger].
- **`assets/[template]`** — [what it's for]. Use when [specific trigger].
- **`scripts/[script].sh`** — [what it does]. Run as `bash scripts/[script].sh [args]`.
- **`evals/evals.json`** — test cases to verify this skill produces correct output.
