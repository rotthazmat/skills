---
name: skill-name
description: One sentence on what this skill does. Use when the user asks about X, Y, or Z.
# compatibility: Requires git        # uncomment if the skill needs specific tools
# license: MIT                       # uncomment to declare a license
# user-invocable: true               # uncomment to allow explicit /skill-name activation
# argument-hint: "e.g. module name"  # uncomment to show a hint when user types /skill-name
---

Brief one-paragraph summary of what this skill does and when it applies.

## When to apply this skill

Apply immediately and fully whenever the user:

- [Trigger scenario 1 — be specific, include the exact words a user would type]
- [Trigger scenario 2]
- [Trigger scenario 3]

Do not wait to be asked — enforce these conventions proactively on every matching task.

---

## [Main section — e.g. Workflow / Rules / Process]

[Core instructions. Write only what the model wouldn't know without this skill.
Steps for workflows, rules for style/conventions, gotchas for non-obvious behavior.]

### [Sub-section — universal]

[Guidance that applies to every project using this skill.]

### [Sub-section — project-specific — when X applies]

[Guidance that only applies when the project has a specific requirement. Label clearly so agents don't apply it everywhere.]

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
