---
name: skill-author
description: Create, improve, or audit Agent Skills. Use when asked to create, write, design, scaffold, upgrade, refactor, or review a skill in the .agents/skills/ directory.
---

Use this skill for both creating new skills and improving existing ones. Follow the appropriate path below.

---

## Creating a new skill

Follow these steps in order — don't skip ahead.

### Step 1 — Define scope

A skill must encapsulate one coherent unit of work. Ask:

- Can I describe what this skill does in one sentence?
- Does it compose cleanly with other skills, or does it overlap heavily?
- Is the scope narrow enough to activate precisely, and broad enough to be reusable across projects?

If no, split or merge before writing a single line.

### Step 2 — Choose a name

- Lowercase letters, numbers, and hyphens only — no spaces, no underscores
- Describes what the skill *does*: `git-conflict-resolve`, not `git`
- Max 64 characters; no leading/trailing/consecutive hyphens
- Must match the directory name exactly

### Step 3 — Write the description

The description is the only thing the model reads before deciding whether to activate. It determines trigger reliability.

**Formula:** `[What it does] + [Use when...]`

```
# Good — specific, includes trigger keywords
description: PHP code style, design patterns, and testing rules. Use when writing or reviewing PHP classes, services, or Pest/PHPUnit test files.

# Bad — too vague, no trigger context
description: Helps with PHP code.
```

Rules:
- Include the specific terms users will actually type (language names, tool names, operation names)
- The "Use when..." clause is not optional for code/review/workflow skills
- Max 1024 characters

### Step 4 — Write the SKILL.md body

Write only what the model *wouldn't* know without this skill:

- Project/team conventions that override defaults
- Non-obvious rules or gotchas
- The exact sequence of steps for a multi-step workflow
- Specific tools or libraries to use — pick a default, don't present a menu

**Do not write:** general explanations, generic advice, or exhaustive edge case coverage.

**Structure:** stepwise instructions → gotchas section → anti-patterns table. Keep under 500 lines — move detail to `references/`.

### Step 5 — Add supporting files (only what's needed)

| Folder | Use for | Load trigger |
|---|---|---|
| `references/` | Detailed docs, worked examples, scenario catalogs | On demand — agent loads when instructions say so |
| `assets/` | Output templates, code templates, static resources | On demand — agent uses when task requires it |
| `scripts/` | Reusable executable code the agent runs | Referenced by name in SKILL.md |
| `evals/` | Test cases in `evals.json` — always add these | Tooling and iteration |

Add a `## Resources` section at the end of SKILL.md with a load trigger for each file:

```markdown
## Resources

- **`references/scenarios.md`** — worked examples. Load when a scenario is unclear.
- **`assets/template.php`** — base class template. Use when creating a new class.
- **`scripts/validate.sh`** — runs validation. Referenced in Step 3 of the workflow.
- **`evals/evals.json`** — test cases.
```

### Step 6 — Write evals

Every skill must have `evals/evals.json`. Start with 2–3 cases. See `references/evals-guide.md` for the full format.

Minimum per eval case: a realistic prompt, a human-readable expected output, and 3–6 specific verifiable assertions.

### Step 7 — Final checklist

- [ ] Skill name matches the directory name
- [ ] Description has a "Use when..." clause with specific trigger keywords
- [ ] SKILL.md is under 500 lines
- [ ] No company names, project-specific file paths, or internal references
- [ ] Every supporting file listed in `## Resources` with a load trigger
- [ ] `evals/evals.json` exists with at least 2 test cases
- [ ] No `allowed-tools` field — not supported in VS Code's agent runtime

---

## Improving an existing skill

Use this path when asked to upgrade, refactor, audit, or improve a skill.

### Step 1 — Read the spec for updates

Before touching the skill, check if the spec has relevant updates:

```
Fetch: https://agentskills.io/llms.txt
```

Identify pages relevant to what you're improving (evals, scripts, descriptions, frontmatter). Fetch those pages.

### Step 2 — Audit the current skill

Read `SKILL.md` and all supporting files. Check against:

- [ ] Description has a "Use when..." trigger clause
- [ ] Body covers only non-obvious content — no generic advice
- [ ] SKILL.md is under 500 lines; excess detail belongs in `references/`
- [ ] `## Resources` section exists and lists all supporting files with load triggers
- [ ] `evals/evals.json` exists with realistic prompts and verifiable assertions
- [ ] No `allowed-tools` in frontmatter (VS Code incompatible)
- [ ] No company names, internal paths, or project-specific references
- [ ] Scripts (if any) have `--help`, no interactive prompts, structured stdout output

### Step 3 — Identify improvements

Categorize findings:

| Type | Examples |
|---|---|
| **Trigger reliability** | Vague description, missing "Use when...", no domain keywords |
| **Content quality** | Generic advice, missing gotchas, procedures not reusable |
| **Progressive disclosure** | SKILL.md over 500 lines, detail not moved to `references/` |
| **Missing evals** | No evals.json, weak assertions, no edge case coverage |
| **Spec compliance** | Unsupported frontmatter fields, missing `## Resources` |

### Step 4 — Apply changes

Make only the improvements identified in Step 3. Do not restructure content that works. Do not add features the skill doesn't need.

---

## Frontmatter reference

```yaml
---
name: skill-name                      # required — matches directory name
description: What it does. Use when… # required — trigger clause is non-optional
compatibility: Requires git           # optional — only if env has real requirements
license: MIT                          # optional
metadata:                             # optional — arbitrary key-value
  version: "1.0"
---
```

**VS Code-specific fields (optional):**
- `user-invocable: true` — allows explicit `/skill-name` activation by the user
- `argument-hint: "e.g. PR number"` — shown when the user types the slash command
- `disable-model-invocation: true` — prevents the model from auto-activating; user-only

## Resources

- **`assets/SKILL-template.md`** — ready-to-fill SKILL.md template for new skills.
- **`references/evals-guide.md`** — full evals.json format, assertion writing rules, and grading guidance.
- **`references/content-guide.md`** — detailed content writing principles: gotchas, output templates, checklists, and script design for agents.
- **`evals/evals.json`** — test cases to verify this skill produces well-formed skills.

**Spec:** https://agentskills.io/specification — fetch when verifying frontmatter or checking for updates.
