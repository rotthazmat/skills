---
name: code-js
description: JavaScript and TypeScript code style, naming conventions, and testing rules. Use when writing or reviewing JS, TS, or React/JSX files.
---

Apply the following rules to all JavaScript and TypeScript code you write or review.

## Code Style

- **2-space indentation**
- **Single quotes** for strings
- **Semicolons required**
- **`===` only** — never `==`
- **camelCase** for variable and function names
- **JSX props must be alphabetically sorted**
- **Cyclomatic complexity ≤ 8** per function
- **Always use curly braces** for control structures — no implicit single-line blocks
- **Unix linebreaks** (LF)

## TypeScript

- **Never use `any`** — always type every variable, parameter, and return value
- **Prefer `unknown` over `any`** when the type is truly unknown; narrow it before use

## Testing (Jest)

- Use `@testing-library/react` for component tests
- Use direct DOM manipulation for plain JS/TS interaction tests
- Coverage output: Cobertura format; exclude type-only files and test files from coverage

## Resources

- **`evals/evals.json`** — test cases to verify this skill produces correct reviews
