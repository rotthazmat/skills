# Content Writing Guide

## The core rule

Add what the model *lacks*, omit what it *knows*. Ask of every sentence: "Would the model get this wrong without this instruction?" If the answer is no, cut it.

---

## Gotchas sections

The highest-value content in most skills is a list of gotchas — concrete corrections to mistakes the model will make without being told:

```markdown
## Gotchas

- **The `users` table uses soft deletes.** All queries must include
  `WHERE deleted_at IS NULL` or results will include deactivated records.
- **Array keys must be alphabetically sorted** — this applies to context arrays,
  config arrays, and view data — not just data models.
- **`Functions\when()` and `Functions\expect()` conflict when set for the same
  function in the same scope.** Set them individually per test.
```

Keep gotchas in `SKILL.md` — the model reads them before encountering the situation. Only move them to `references/` if you instruct the model exactly when to load that file and why.

---

## Output format templates

When output must follow a specific structure, provide a template rather than prose:

```markdown
## Commit message format

Use this template:

```
[type]: [short summary under 72 chars]

[optional body — one paragraph on the why]
```
```

Short templates belong in `SKILL.md`. Templates only needed in certain cases go in `assets/` — reference them from SKILL.md with a conditional load trigger.

---

## Procedures over declarations

Teach the model *how to approach* a class of tasks, not what to output for a specific instance:

```markdown
// Specific — only useful for this exact task
Join orders to customers on customer_id where region = 'EMEA'.

// Reusable — works for any analytical query
1. Read the schema to identify relevant tables
2. Join on the _id foreign key convention
3. Apply the user's filters as WHERE clauses
4. Aggregate numeric columns and format as a markdown table
```

---

## Checklists for multi-step workflows

Use checklists when steps have dependencies or validation gates:

```markdown
## Deployment checklist

- [ ] Run tests: `bash scripts/test.sh`
- [ ] Build: `bash scripts/build.sh`
- [ ] Verify output: `bash scripts/verify.sh`
- [ ] Wait for user approval before deploying
```

---

## Prescriptive vs. flexible instructions

Match specificity to fragility:

- **Flexible:** "Check for SQL injection — use parameterized queries" — the model knows what parameterized queries look like
- **Prescriptive:** "Run exactly this command: `bash scripts/migrate.py --verify --backup` — do not add flags" — fragile operation with a single correct invocation

---

## Progressive disclosure

Keep `SKILL.md` under 500 lines. Move detail to `references/` using conditional load triggers:

```markdown
// Good — tells the model exactly when to load
- **`references/scenarios.md`** — load when a conflict scenario is unclear.

// Bad — too vague, model may load it unnecessarily
- See `references/` for more details.
```

---

## Script design for agents

Scripts in `scripts/` must be agent-safe:

- **No interactive prompts** — agents can't respond to TTY input; the script will hang
- **`--help` output** — the primary way the model learns the interface; keep it concise
- **Structured output** — prefer JSON or CSV on stdout; diagnostics to stderr
- **Idempotency** — agents may retry; "create if not exists" is safer than "create and fail"
- **Clear error messages** — include what went wrong, what was expected, and what to try

```bash
# Good error
echo "Error: --format must be one of: json, csv, table. Received: 'xml'" >&2
exit 1

# Bad error  
echo "Error" >&2
exit 1
```

---

## Naming and confidentiality

- No company names, internal domain names, or project-specific file paths
- No references to private repositories, internal APIs, or proprietary tools
- Library names (Mockery, Pest, Brain\Monkey) are fine — they're public
- Framework conventions (WordPress hooks, Symfony DI) are fine if the skill targets that framework
