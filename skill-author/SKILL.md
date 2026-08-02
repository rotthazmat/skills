---
name: skill-author
description: Create, improve, update, polish, or audit Agent Skills — regardless of where they live. Use when asked to create, write, design, scaffold, build, upgrade, refactor, improve, polish, update, or review ANY skill file (SKILL.md, references/, assets/, evals/). This skill is MANDATORY for any work on skills — do not create or modify skill files without invoking it first.
user-invocable: true
argument-hint: "optional: skill name or area to focus on"
---

**This skill is mandatory for any work on Agent Skills — creating, improving, polishing, updating, auditing, or restructuring. Do not touch a skill file without following this process. No exceptions.**

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
| `assets/` | Starter templates, boilerplate code, static resources | On demand — agent uses when task requires it |
| `scripts/` | Reusable executable code the agent runs | Referenced by name in SKILL.md |
| `evals/` | Test cases in `evals.json` — always add these | Tooling and iteration |

**When to split `references/` into multiple files:** one file per distinct topic that would only be needed in some scenarios. Example: `testing.md`, `migration.md`, and `patterns.md` are all separate because a refactoring task needs migration + patterns but not testing, while a test-writing task needs testing but not migration. A single `references/all.md` bloats every context load.

**When to create files in `assets/`:** whenever the skill involves creating something from scratch that has a recurring shape — entry points, config files, test suites, class stubs. Name them descriptively (`entry-point.js`, `base-class.php`, `test-suite.ts`). A good asset is a file the agent would otherwise write from scratch every time and get slightly wrong each time.

**When to create files in `scripts/`:** when you notice the agent independently reinventing the same logic across runs — parsing a specific format, validating output, generating a report. Write a tested script once and bundle it. If an agent never needs to run code autonomously for this skill, skip `scripts/` entirely.

**Universal vs project-specific:** when a rule applies only to some projects (not all), label it explicitly. This prevents agents from applying optional rules everywhere:

```markdown
### Config file (project-specific — only when the tool needs persistent settings)
Use `assets/config-template.json` when the project stores user preferences...

### Error logging (universal — add to every project that runs unattended)
Wire `src/logger` when the project runs in batch mode or without a live terminal...
```

Add a `## Resources` section at the end of SKILL.md with a load trigger for each file:

```markdown
## Resources

- **`references/scenarios.md`** — worked examples. Load when a scenario is unclear.
- **`assets/base-class.php`** — base class template. Use when creating a new class.
- **`scripts/validate.sh`** — runs validation. Referenced in Step 3 of the workflow.
- **`evals/evals.json`** — test cases.
```

### Step 6 — Write evals

Every skill must have `evals/evals.json`. Start with 2–3 cases. See `references/evals-guide.md` for the full format.

Minimum per eval case: a realistic prompt, a human-readable expected output, and 3–6 specific verifiable assertions.

### Step 6b — Blind spot audit (do this before Step 7)

Before locking in the skill, ask: "What scenarios does this skill NOT cover?" Work through it systematically:

1. List every type of task this skill's users will do
2. For each task, ask: does SKILL.md give enough to handle it correctly?
3. If no — add it to SKILL.md, a `references/` file, or an `assets/` template
4. Mark each piece of guidance as **universal** (every project) or **project-specific** (conditional)

A skill with no blind spots is one where you can hand it to an agent with zero prior context and it will make no surprising decisions.

### Step 7 — Final checklist

- [ ] Skill name matches the directory name
- [ ] Description has a "Use when..." clause with specific trigger keywords
- [ ] SKILL.md body has a "When to apply this skill" section listing all trigger scenarios explicitly
- [ ] SKILL.md is under 500 lines
- [ ] No company names, project-specific file paths, or internal references
- [ ] Every supporting file listed in `## Resources` with a load trigger
- [ ] `evals/evals.json` exists with at least 2 test cases
- [ ] `allowed-tools` removed if targeting VS Code — not supported there (valid per spec for other runtimes)
- [ ] File references stay one level deep from SKILL.md — no deeply nested reference chains
- [ ] Universal vs project-specific guidance is labeled where applicable
- [ ] Blind spot audit completed (Step 6b)

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

- [ ] Description has a "Use when..." trigger clause with specific domain keywords
- [ ] Body has a "When to apply this skill" section listing all trigger scenarios explicitly
- [ ] Body covers only non-obvious content — no generic advice
- [ ] SKILL.md is under 500 lines; excess detail belongs in `references/`
- [ ] `## Resources` section exists and lists all supporting files with load triggers
- [ ] `evals/evals.json` exists with realistic prompts and verifiable assertions
- [ ] `allowed-tools` removed if targeting VS Code — not supported there (valid per spec for other runtimes)
- [ ] File references stay one level deep — no deeply nested chains
- [ ] No company names, internal paths, or project-specific references
- [ ] Scripts (if any) have `--help`, no interactive prompts, structured stdout output
- [ ] Universal vs project-specific guidance is labeled where applicable

### Step 2b — Blind spot audit

List every type of task the skill's users will do. For each, ask: does SKILL.md give enough to handle it without surprising decisions? Common blind spots to check:

- Scenarios that are universal (every project) vs project-specific (conditional) — are they labeled?
- Edge cases that aren't covered by any existing rule
- Missing `assets/` templates for recurring boilerplate the agent writes from scratch each time
- Missing `references/` files for scenarios that need detailed worked examples
- Rules that assume context the agent won't have (e.g., assumes a specific file exists, a framework is installed, etc.)

### Step 3 — Identify improvements

Categorize findings:

| Type | Examples |
|---|---|
| **Trigger reliability** | Vague description, missing "Use when...", no domain keywords, no "When to apply" section |
| **Content quality** | Generic advice, missing gotchas, procedures not reusable |
| **Blind spots** | Uncovered scenarios, missing universal/project-specific labels, missing assets templates |
| **Progressive disclosure** | SKILL.md over 500 lines, detail not moved to `references/`, references not split by topic |
| **Missing evals** | No evals.json, weak assertions, no edge case coverage |
| **Spec compliance** | Unsupported frontmatter fields, missing `## Resources` |

### Step 4 — Apply changes

Make only the improvements identified in Steps 2 and 2b. Do not restructure content that works. Do not add features the skill doesn't need.

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
