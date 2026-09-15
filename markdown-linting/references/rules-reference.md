# Markdown Rules Reference

This mirrors the standard markdownlint/mdl rule catalog (MD001-MD047). Each entry states what the rule catches, why it matters, and — where this skill picked a specific style among several valid ones, or deliberately deviates from the common default — what this skill enforces instead. `scripts/check_markdown.py` checks the ones marked **[checked]**; the rest are marked **[by eye]** because reliably detecting them needs real list/nesting state that a line-based heuristic gets wrong too often.

## Headings

- **MD001 — heading levels increment by one at a time. [checked]** H2 straight to H4 with no H3 breaks any tool that builds a table of contents from the heading tree, and confuses screen readers that navigate by level.
- **MD002 — first heading should be a top-level heading.** **This skill does not enforce MD002.** Many files (including this repo's own `SKILL.md` files) intentionally have no heading at all, or start below H1 — the document's title lives in front matter or the filename instead. Treat MD002 as off.
- **MD003 — consistent heading style. [checked]** This skill enforces **open ATX** (`# Heading`) only — never Setext (`Heading\n=======`) and never closed ATX (`## Heading ##`). ATX works at all six levels and survives reordering/editing without breaking.
- **MD018 — space required after `#` on ATX headings. [checked]** `#Heading` without a space is easy to type by accident and some parsers won't even recognize it as a heading.
- **MD019 — only one space after `#` on ATX headings. [checked]** `#  Heading` (two-plus spaces) is a typo, not a style choice.
- **MD020/MD021 — spacing inside closed ATX headings.** Not applicable here — closed ATX is disallowed entirely (see MD003), so there's no closing `#` to space correctly.
- **MD022 — blank line before and after every heading. [checked]** Some parsers (e.g. kramdown) won't recognize a heading glued directly to adjacent text and will render it as a plain paragraph.
- **MD023 — headings must start at column 0. [checked]** A heading indented 1-3 spaces is still valid CommonMark, but is almost always an accidental leftover indent from copy-pasting inside a list or blockquote.
- **MD024 — no duplicate headings** at the same level under the same parent. Breaks anchor links, since `#usage` can only point at one heading. Exception: repeated sibling headings across independent top-level sections (e.g. a `### Bug fixes` under every version in a changelog) are fine — this skill's `assets/markdownlint.json` sets `siblings_only: true` for that reason.
- **MD025 — at most one H1 per document. [checked]** If an H1 is used at all, treat it as the document title; a second one makes the title ambiguous.
- **MD026 — no trailing punctuation in heading text. [checked]** `## Installation:` → `## Installation`. A trailing `?` is fine for genuinely interrogative headings (FAQ entries).
- **MD036 — don't use bold/italic text as a heading substitute.** A single-line paragraph that's entirely `**Some Section**` should be a real heading — screen readers, TOC generators, and anchor links only recognize actual headings.
- **MD041 — first line of the file should be a top-level heading.** **Not enforced**, for the same reason as MD002: this repo's `SKILL.md` files (and many docs generally) legitimately start with body text or front matter instead.

## Lists

- **MD004 — consistent unordered-list marker. [checked]** This skill's default is `-`. Never mix `-`, `*`, and `+` in the same document — when editing a file that already committed to a different marker, match that file instead (see the Gotchas in `SKILL.md`).
- **MD005 — sibling list items must share the same indentation. [by eye]** A misaligned nested item (three spaces where its siblings use two) is usually a typo, but detecting "same level, different indent" reliably needs real list-nesting state.
- **MD006 — top-level lists should start at column 0. [by eye]** This is the softest rule in the catalog (the original wording is "consider..."), and flagging it via line-matching produces too many false positives on legitimately nested content. Apply it by eye: a top-level list item indented for no structural reason should be un-indented.
- **MD007 — nested list indentation. [by eye]** This skill's convention is 2 spaces per nesting level (matching the marker width of `-`, `*`, `+`, one space). Note the common alternative of 3 or 4 spaces (to match ordered-list or code-block width) is also valid — pick one and hold it project-wide via `assets/markdownlint.json`'s `MD007.indent`.
- **MD029 — ordered list numbering. [by eye]** Two valid conventions: sequential (`1.`, `2.`, `3.`) or all-`1.` (letting the renderer auto-number). Pick one per list; a list that goes `1.`, `1.`, `3.` is a mistake either way. This skill's default config uses `ordered` (sequential).
- **MD030 — exactly one space after a list marker.** `-  Item` (two spaces) or `-Item` (zero spaces) before the content is a typo.
- **MD032 — lists surrounded by blank lines.** A list glued directly to a preceding paragraph is ambiguous — some parsers merge the first list item into the paragraph text.

## Blockquotes

- **MD027 — exactly one space after the blockquote `>` symbol. [checked]** `>  Text` with extra spaces is usually accidental and shifts the rendered indentation.
- **MD028 — no blank line splitting one logical blockquote into two. [checked]** Some parsers treat two `>` blocks separated only by a blank line as a single blockquote, others treat them as separate ones — the ambiguity is the bug. Either put real text between them, or keep it one blockquote by adding a bare `>` on the blank line.

## Code

- **MD014 — don't prefix every line of a shown shell command with `$` unless you're also showing output. [checked]** A block of `$ command` lines with no output shown makes copy-paste harder and adds visual noise for no benefit. If you do show output, keep the `$` only on the command lines to distinguish them.
- **MD031 — fenced code blocks surrounded by blank lines.** Same rationale as headings/lists (MD022/MD032) — some parsers won't recognize a fence glued directly to adjacent text.
- **MD040 — fenced code blocks must declare a language. [checked]** Use `text` for genuinely unhighlighted content rather than leaving the tag empty — an empty tag reads as "forgot to add one," not "intentionally plain."
- **MD046 — fenced code blocks only, never indented (4-space) code blocks.** Fenced blocks are unambiguous about where they start and end, support language tags, and don't collide with nested-list indentation math.

## Links and images

- **MD011 — no reversed link syntax. [checked]** `(text)[url]` (parens and brackets swapped) renders as plain text with a stray bracketed URL next to it — always `[text](url)`.
- **MD034 — no bare URLs. [checked]** A bare `https://example.com` in prose relies on the renderer's autolink extension, which isn't part of core CommonMark and is inconsistently supported. Wrap it: `<https://example.com>` or give it label text. A URL inside a code span (`` `https://example.com` ``) is exempt — it's shown as literal text, not meant to link.
- **MD039 — no spaces inside link text brackets. [checked]** `[ a link ](url)` → `[a link](url)`.
- **MD045 — every image needs real alt text. [checked]** `![](url)` with empty brackets is never acceptable — alt text is the only content available to screen readers and text-only renderers.
- Reference-style links (`[text][ref]`) should have every `ref` defined exactly once, with unused definitions removed and all definitions grouped at the bottom of the file. (Corresponds to the newer markdownlint MD052/MD053 rules, not present in the classic MD001-047 set but worth following.)

## Emphasis

- **MD037 — no spaces inside emphasis markers. [checked]** `** bold **` or `* italic *` (space touching the marker) is usually meant as emphasis but fails to render as such in most parsers, since emphasis only applies when the marker isn't surrounded by whitespace.
- Pick **`**bold**`** and **`*italic*`** and use them consistently — never switch to `__bold__` / `_italic_` mid-document. (Corresponds to the newer markdownlint MD049/MD050 rules.)

## Horizontal rules

- **MD035 — consistent horizontal rule style. [checked]** `---`, `***`, and `___` are all valid thematic breaks, but a document should pick exactly one and use it everywhere. This skill's default is `---` (which doubles as this repo's section-separator convention already).

## Tables

- Every row, including the header, has the same number of `|`-separated columns. A short row silently drops trailing cells in most renderers instead of erroring. (Corresponds to the newer markdownlint MD055/MD056.)
- The separator row uses `---` per column (`:--`, `:-:`, `--:` for alignment) and nothing else.
- Surround tables with blank lines, same reasoning as MD022/MD031/MD032. (Corresponds to the newer markdownlint MD058.)

## Whitespace

- **MD009 — no trailing spaces. [checked]** Including the classic "two trailing spaces force a `<br>`" convention — it's invisible in most editors and routinely stripped by autoformatters, leaving a broken line break with no visible cause. Use an explicit `<br>` tag when a hard break is genuinely needed.
- **MD010 — no hard tabs. [checked]** Tabs render at different widths across editors/terminals and break alignment in tables and nested lists.
- **MD012 — no multiple consecutive blank lines. [checked]** One blank line is a paragraph break; two or more carries no additional meaning and is almost always an editing artifact.
- **MD013 — line length.** Off by default in this skill's config (`MD013: false`) — most renderers reflow prose regardless of source line length. Only turn it on when a project's own style guide specifies a wrap column.
- **MD047 — file ends with exactly one newline character. [checked]** No trailing blank lines, and the file must not be missing its final newline — many POSIX tools and diff formats treat a missing final newline as a defect.

## Other

- **MD033 — inline HTML.** Raw HTML is valid CommonMark and sometimes necessary (`<br>` for a hard break, `<details>` for a collapsible section). This skill allows it (`MD033: false` in the config) but prefers the markdown equivalent whenever one exists (`**bold**` not `<b>bold</b>`). When HTML is necessary, still surround block-level HTML with blank lines the same way you would a heading or list.

## Front matter

Front matter (YAML between `---` fences at the very top of the file) is common in this repo's `SKILL.md` files (`name:`, `description:`, etc.) and in static-site content (Jekyll/Hugo posts). Not part of the classic MD-numbered catalog, but load-bearing here:

- The opening `---` must be the literal first three bytes of the file — no blank line, no BOM-induced leading whitespace, nothing before it.
- Everything between the fences must be valid YAML; a syntax error there breaks tooling that parses the file (this repo's skill loader included).
- Don't restate front-matter fields as body content redundantly (e.g. an H1 that just repeats `title:`).

## HTML inside Markdown

See MD033 above. Keep it minimal and prefer markdown syntax where an equivalent exists.

## Footnotes and definition lists

These are extensions, not core CommonMark or part of the classic rule catalog — support varies by renderer (GitHub supports footnotes `[^1]`; definition lists are less universally supported). Before using either, confirm the target renderer supports the extension by checking existing usage elsewhere in the same repo/platform; if unsupported, fall back to a plain parenthetical note or a nested list.
