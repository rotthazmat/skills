---
name: best-practices
description: General development best practices — code organization, error handling, and design conventions. Use when writing any code or reviewing scope, comments, and structure decisions.
---

Apply these rules to all code you write or review, regardless of language.

## Code Scope

- **No features beyond what the task requires** — don't design for hypothetical future requirements. Three similar lines is better than a premature abstraction.
- **No half-finished implementations** — either complete the feature or don't start it.
- **No error handling for scenarios that can't happen** — trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
- **No unnecessary feature flags or backwards-compatibility shims** — just change the code.
- **Prefer editing existing files** over creating new ones.

## Comments

- **Default to writing no comments** — only add one when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug, or behavior that would surprise a reader.
- **Never describe WHAT the code does** — well-named identifiers already do that.
- **No multi-paragraph docstrings or multi-line comment blocks** — one short line max.

## Code Organization

- Service classes: one main responsibility per class
- Tests collocated next to the code they test
- Views/templates adjacent to the class that renders them
- Max 400 lines per file, max 100 lines per function
- 2-space indentation (PHP, JS, SCSS)

## Input & Validation

- **Validate at the entry point, not deep in implementations** — input validation belongs in the route handler, controller, or plugin file, not inside the implementation class.
- **Pass only the variables a template actually uses** — don't flood templates with heavy global context objects. Extract only what's needed.

## Error Handling

- **Missing view/template files are deployment errors, not runtime errors** — don't wrap template compilation in try/catch. Let it throw.
- **Services return `null` on API failures** — the caller renders silently empty. Only show errors for invalid inputs, not for service outages.
- **HTTP service exceptions should wrap errors with context data** — include endpoint, params, and response body.
- **Log errors with structured context**; use a consistent logger across the project.
- **User-visible errors shown only to authenticated/admin users** — silent for visitors.

## Resources

- **`references/anti-patterns.md`** — before/after examples of common anti-patterns. Load when reviewing code for over-engineering, premature abstraction, or misplaced validation.
- **`evals/evals.json`** — test cases to verify this skill produces correct guidance.
