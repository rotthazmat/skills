---
name: skill-toggle
description: Enable or disable a skill, or check its current state. Use when asked to disable, enable, turn off, turn on, or check if a skill is disabled.
---

A skill is disabled by prepending `Disabled. ` (capital D, period, space) to the `description` field in its `SKILL.md`. The model sees this prefix at catalog load time and skips auto-activation. To re-enable, remove that prefix.

---

## Disabling a skill

1. Read the target skill's `SKILL.md`.
2. Check the `description` field does **not** already start with `Disabled. ` — if it does, report that it's already disabled and stop.
3. Prepend `Disabled. ` to the existing description value. Do not change anything else.

**Before:**
```yaml
description: Every initial message will contain this greet.
```

**After:**
```yaml
description: Disabled. Every initial message will contain this greet.
```

## Enabling a skill

1. Read the target skill's `SKILL.md`.
2. Check whether the skill is disabled using the full detection logic below.
3. If not disabled by any method, report it's already enabled and stop.
4. If disabled via the `Disabled. ` prefix — remove it. Do not change anything else.
5. If disabled via description text (no prefix) — rewrite the description to remove any language that indicates the skill is disabled, leaving a clean description of what the skill does. Do not change anything else.

## Checking a skill's state

1. Read the target skill's `SKILL.md`.
2. Apply the full detection logic below and report the result.
3. Show the current description so the user can verify.

## Detecting disabled state

A skill is considered disabled if **either** condition is true:

1. **Prefix method** — `description` starts with exactly `Disabled. ` (capital D, period, space). This is the canonical form used by this skill.
2. **Implicit method** — `description` does not start with `Disabled. ` but its text still clearly states the skill is disabled (e.g. `"This skill is currently disabled."`, `"Disabled skill — does X"`, `"Not active. Does Y"`).

When disabling: always use the prefix method (condition 1) regardless of what the description currently says.
When enabling: condition 1 → strip the prefix. Condition 2 → ask the user for the correct enabled description before editing.
When checking: report which condition matched, or that the skill is enabled.

## Gotchas

- **Match exactly:** `Disabled. ` — capital D, period, single space. No other casing or punctuation.
- **Only touch the `description` field** — never modify the skill name, body, or any supporting file.
- **Idempotent:** disabling an already-disabled skill or enabling an already-enabled skill must be a no-op with a clear message, not a double-prefix or silent failure.
- **When re-disabling a skill that was enabled from an implicit state**, always use the `Disabled. ` prefix — never restore the old implicit wording.
- **Skill path:** skills live in `.agents/skills/<name>/SKILL.md`. Always resolve the path before editing.

## Resources

- **`evals/evals.json`** — test cases to verify correct toggle behavior.
