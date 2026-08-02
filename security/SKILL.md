---
name: security
description: Security rules for input sanitization, output escaping, and safe coding practices. Use when writing or reviewing any code that handles user input, database queries, external calls, or output rendering.
---

Apply these rules to all code you write or review.

## Core Rules

- **Always sanitize user-supplied values** before embedding them in commands, queries, or output strings — use parameterized queries, escaping functions, or the equivalent for your language/framework.
- **Never trust input** at system boundaries (user input, external APIs) — validate and sanitize there; trust internal code thereafter.
- **No `eval()`** — no dynamic code execution from user input.
- **Wrap external calls in try/catch**, return empty/null on failure, log the error — never expose stack traces to end users.
- **Never nest composable units that call each other** — circular delegation causes infinite recursion.
- **Sanitize output** — escape values before embedding them in HTML, attributes, URLs, or SQL. Use the appropriate escaping function for the context (HTML body, HTML attribute, URL, SQL).

## Resources

- **`references/examples.md`** — right/wrong code examples for every rule above. Load when reviewing code for security issues or when implementing safe patterns.
- **`evals/evals.json`** — test cases to verify this skill catches real vulnerabilities.
