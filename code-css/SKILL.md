---
name: code-css
description: CSS and SCSS code style rules — property ordering, BEM naming, and constraint rules. Use when writing or reviewing CSS or SCSS files.
---

Apply the following rules to all CSS and SCSS code you write or review.

## Code Style

- **CSS properties must be in alphabetical order** — applies to every declaration block
- **No duplicate properties** within a block
- **No duplicate `$` variables** within a file (SCSS)
- **Max 1 ID selector** per rule
- **2-space indentation**

## Naming Conventions

- **BEM** for class names: `ComponentName-element`, `ComponentName--modifier`
- The component (block) class uses **PascalCase** — e.g. `.UserCard`, `.NavMenu`
- Elements use a single hyphen — e.g. `.UserCard-avatar`, `.NavMenu-item`
- Modifiers use double hyphens — e.g. `.UserCard--featured`, `.NavMenu-item--active`

## Resources

- **`references/bem-guide.md`** — BEM naming examples and common mistakes. Load when writing or reviewing class names.
- **`evals/evals.json`** — test cases to verify this skill produces correct reviews
