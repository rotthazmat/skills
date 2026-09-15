---
name: markdown-linting
description: Markdown authoring best practices — heading structure, list and code-block formatting, links, tables, and whitespace hygiene. Use ALWAYS when creating or modifying any Markdown (.md/.markdown) file or markdown-formatted content, no exceptions — README, SKILL.md, docs, changelogs, PR descriptions, generated reports.
user-invocable: true
---

Apply these rules every single time you write or touch Markdown — this is not optional and not scoped to "important" files.

## When to apply this skill

Apply immediately and fully whenever you:

- Create a new `.md` or `.markdown` file from scratch
- Edit, patch, or append to an existing markdown file — even a one-line or one-word change
- Write a `SKILL.md`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, or any other docs file
- Generate markdown-formatted content that gets saved to a file (a report, a spec, a PR description written to disk)
- Review, audit, or lint existing markdown for quality
- Are asked to make a "quick" or "trivial" fix to a markdown file — small scope does not exempt the file from these rules; check the whole file, not just your diff

Do not skip this skill because the task seems unrelated to documentation, because the file is a draft, or because the change is tiny. If a `.md` file is touched, this skill applies. When the file already follows an established convention that conflicts with a default below (e.g. it consistently uses `*` bullets), match the existing convention instead of introducing a mixed style — consistency-with-existing-file beats the default preference.

---

## Headings

- **At most one H1 per document (MD025)**, and if present it must be the first heading. Multiple H1s make the document outline ambiguous.
- **A document does not need an H1 at all — this skill does not enforce MD002/MD041.** Many files (like this one) start directly with body text or an H2; don't force an H1 in.
- **Never skip a level going deeper (MD001)** (H2 straight to H4). Going shallower (H4 back to H2) is fine.
- **Blank line before and after every heading (MD022).**
- **Open ATX style only (MD003)** (`# Heading`) — never Setext (`===` / `---` underlines) and never closed ATX (`## Heading ##`).
- **Exactly one space after the `#` (MD018/MD019)** — not zero, not two-plus.
- **Headings start at column 0 (MD023)** — no leading indentation, even 1-2 spaces.
- No trailing punctuation in heading text (MD026).
- Don't use bold/italic text as a heading substitute (MD036) — use a real heading.

## Lists

- **One bullet marker per document (MD004).** Prefer `-`. Never mix `-`, `*`, and `+` in the same file.
- **Ordered lists (MD029):** either number sequentially (`1.`, `2.`, `3.`) or use `1.` for every item and let the renderer number them — pick one convention and hold it for the whole list.
- **Blank line before and after a list block (MD032)** when it sits between paragraphs or headings.
- **Nested items indent by the parent marker width + 1 space (MD007)** (2 spaces for `-`, `*`, `+`) — stay consistent within the document.
- **Exactly one space after the marker (MD030)** — `- Item`, not `-  Item` or `-Item`.
- No blank lines between sibling list items unless an item itself contains multiple paragraphs.
- Top-level list items start at column 0, not indented for no structural reason (MD006).

## Blockquotes

- **Exactly one space after `>` (MD027)** — `> Text`, not `>  Text`.
- **Don't split one logical quote into two blocks with just a blank line between them (MD028)** — parsers disagree on whether that's one blockquote or two. Either add real content between them, or keep a bare `>` on the blank line to signal it's still the same quote.

## Code blocks

- **Fenced code blocks (```) only (MD046)** — never indent-based code blocks.
- **Always declare a language on the opening fence (MD040)** (```` ```bash ````, ```` ```json ````, ```` ```text ```` if genuinely plain). An undeclared fence silently disables syntax highlighting.
- Blank line before and after every fenced block (MD031).
- **Don't prefix every line of a shown shell command with `$` unless you also show output (MD014)** — a block that's all `$ command` lines with no output is harder to copy-paste for no benefit.

## Links and images

- **No reversed link syntax (MD011)** — `(text)[url]` is backwards; it's always `[text](url)`.
- **No bare URLs in prose (MD034).** Wrap in `<https://example.com>` or give it link text: `[label](https://example.com)`.
- **No spaces inside link text brackets (MD039)** — `[a link](url)`, not `[ a link ](url)`.
- **Every image needs real alt text (MD045)** — `![](url)` with empty brackets is never acceptable; describe what the image shows.
- Use relative paths for links to files inside the same repo, not absolute filesystem paths or full URLs back to the same repo.
- If using reference-style links (`[text][ref]`), group all `[ref]: url` definitions at the bottom of the file, and remove any that are no longer referenced.

## Emphasis

- **No spaces inside emphasis markers (MD037)** — `**bold**`, not `** bold **`.
- **Bold:** `**text**`. **Italic:** `*text*`. Pick these and never switch to `__text__` / `_text_` mid-document.

## Horizontal rules

- **Pick one style and use it everywhere (MD035)** — this skill's default is `---`. Don't mix in `***` or `___` elsewhere in the same document.

## Tables

- Every row, including the header, has the same number of `|`-separated columns.
- The separator row uses `---` per column (`:--`, `:-:`, `--:` for alignment) and nothing else.

## Whitespace and file hygiene

- **No trailing whitespace** on any line — including the old "two spaces = line break" trick. Use an explicit `<br>` if a hard break is truly needed.
- **No hard tabs** — spaces only.
- **No more than one consecutive blank line.**
- **File ends with exactly one trailing newline** — no trailing blank lines, no missing final newline.

## Front matter (project-specific — only when the file uses YAML front matter, e.g. SKILL.md, static-site posts)

- Front matter is the very first thing in the file: opening `---` on line 1, valid YAML, closing `---`.
- Nothing — not even a blank line — precedes the opening `---`.
- If front matter declares a `title`, don't duplicate it as an H1 immediately below.

## Line wrapping (project-specific — only when the repo/tool declares a wrap column)

- Do not hard-wrap prose by default; most renderers reflow it. Only wrap to a fixed column when a linter config (e.g. `.markdownlint.json` with `MD013`) or the project's stated style demands it.

---

## Gotchas

- **This skill applies to its own kind.** Every `SKILL.md` you author or edit — including for other skills — is itself markdown; run these same checks on it.
- **This skill deliberately deviates from two common defaults: MD002 and MD041** (both would force every document to start with an H1). This repo's own `SKILL.md` files don't use one, and that's intentional — don't "fix" a missing H1 you encounter.
- **MD006 and MD005 are enforced by eye, not by the script** — reliably detecting sibling/top-level list indentation issues needs real list-nesting state that a line-based checker gets wrong too often. Use judgment on these two specifically.
- **A markdown snippet you paste inline in chat is not a standalone document** — the single-H1 rule and file-ending-newline rule apply to files you save, not to a fenced example shown for illustration.
- **Editing one paragraph still means checking the whole file** for things a diff-only view would miss: a stray extra blank line two sections down, a leftover tab, a second H1 introduced earlier by someone else.
- **`.markdownlint.json` in a repo overrides the defaults above** — if the project already has one, follow its configured rules instead of (or in addition to) these defaults.

## Anti-patterns to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| Mixing `-` and `*` bullets in the same list or file | Renders inconsistently across parsers and looks unintentional |
| Skipping heading levels (H2 straight to H4) | Breaks document outline and TOC/screen-reader navigation |
| Bare `https://example.com` dropped into prose | Not reliably auto-linked by every renderer; also visually noisy |
| Fenced code block with no language tag | Silently disables syntax highlighting |
| Trailing double-space for a line break | Invisible, easy to strip accidentally on the next edit |
| Multiple H1s in one document | Ambiguous title, breaks doc generators and TOC tools |
| `![](screenshot.png)` with empty alt text | Inaccessible to screen readers, meaningless in a link-only render |
| `(reversed link)[url]` | Parens/brackets swapped; renders as plain text plus a stray URL |
| `** bold with spaces **` or `[ spaced link ]` | Space touching the marker/bracket breaks emphasis or link parsing in most renderers |
| Two blockquotes separated by only a blank line | Ambiguous — some parsers merge them, others don't |
| Mixing `---` and `***` as horizontal rules in one document | Inconsistent visual style with no semantic difference |

## Resources

- **`references/rules-reference.md`** — full MD001-MD047 rule catalog (rationale, which are checked vs. by-eye, and this skill's explicit deviations from common defaults) plus edge cases (front matter, footnotes, HTML-in-markdown, definition lists). Load when a case above is ambiguous or you need the reasoning behind a rule.
- **`assets/document-template.md`** — a minimal correctly-formatted markdown document. Use as a starting skeleton when creating a new `.md` file from scratch.
- **`assets/markdownlint.json`** — project-specific — ready-to-use config for the `markdownlint-cli`/`markdownlint-cli2` tool. Use when the project wants automated CI enforcement of these rules.
- **`scripts/check_markdown.py`** — heuristic static checker for the rules above. Run as `python scripts/check_markdown.py <file.md> [file2.md ...]` after writing or editing any markdown file, before considering the task done. Exits non-zero and prints JSON findings if it detects a violation.
- **`evals/evals.json`** — test cases to verify this skill produces correct reviews and correctly-formatted generated output.
