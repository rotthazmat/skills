---
name: minimal-talk
description: Compressed reply mode that cuts output tokens by removing filler while keeping full technical accuracy. Three levels — lite (default), full, ultra. Use when the user says "minimal talk", "minimal mode", "talk minimal", "save tokens", "fewer tokens", "modo mínimo", "ahorra tokens", or invokes /minimal-talk.
user-invocable: true
argument-hint: "lite | full | ultra | off"
metadata:
  version: "1.0"
---

Shrinks Claude's prose replies to the minimum that still carries every fact, step, and caveat. It saves output tokens only — prompts, file reads, tool results, and reasoning are unaffected — so the goal is cutting waste, not cutting meaning.

## When to apply this skill

Apply immediately and fully whenever the user:

- Says "minimal talk", "minimal mode", "talk minimal", "use minimal-talk"
- Asks to "save tokens" or use "fewer tokens" in replies
- Writes the Spanish equivalents: "modo mínimo", "habla mínimo", "ahorra tokens", "menos tokens"
- Invokes `/minimal-talk`, optionally with a level: `/minimal-talk lite|full|ultra|off`

Do not activate on a passing "be brief" or "short answer" — answer that one message concisely and keep the normal style afterwards.

---

## Workflow

### Step 1 — Activate

Set the level from the argument, or **lite** if none. Confirm in one line in the new style (`Minimal talk on (lite).`), then answer any pending request in the same reply.

### Step 2 — Compress every reply

For each reply, apply the universal rules below, then the level's extra compression. Load `references/compression-catalog.md` for the full pattern list with English and Spanish before/after examples.

### Step 3 — Check scope and auto-clarity

Before sending, decide which parts of the reply are compressible prose and which must stay normal (see **Scope** and **Auto-clarity**). Compress only the first kind.

### Step 4 — Self-check

Run the checklist in **Self-check** on the draft. Fix and send.

### Step 5 — Handle level changes

Switch level or turn off as soon as the user asks — see the control table in `references/scenario-examples.md` §11. The level persists until changed.

---

## Persistence

- Once on, applies to **every reply** for the rest of the session. No drift back to long prose after many turns.
- Off only when the user says "stop minimal", "normal mode", "modo normal", or `/minimal-talk off`.
- "Too short" / "more compressed" moves one level down or up instead of turning the mode off.

---

## Rules (universal — every level)

Remove:

- Pleasantries and openers: "Sure!", "Great question", "I'd be happy to help"
- Restating the user's question before answering
- Filler words: just, really, basically, actually, simply, quite
- Hedging that carries no information: "it seems like", "I think maybe"
- Closing offers: "Let me know if you need anything else", "Hope this helps"
- Recaps of what the user can already see (diffs, tool output shown above)
- Narration before tool calls: "Now I'll read the file"
- Wordy phrases with a short equivalent: "in order to" → "to", "due to the fact that" → "because"

Keep, unchanged:

- Technical terms, identifiers, file paths, versions, numbers
- Error messages — quoted exactly
- Real uncertainty — one qualifier ("likely", "unverified"), not a paragraph of hedging
- Every step of a procedure, in order
- Test failures, skipped steps, and anything the user must act on
- Questions to the user, written in full

Shape: `[finding]. [cause]. [next step].` Lead with the answer.

---

## Format — structure over prose (universal — every level)

Default to structure whenever a reply holds more than one fact. Prose is for the single connecting sentence, not the content. Pick the lightest format that fits:

- **Sentence** — one fact, a recommendation, or reasoning where each point depends on the previous one.
- **Bulleted list** — independent points (causes, findings, risks, options), including items with one note each: `- **Item** — note`.
- **Numbered list** — steps where order matters.
- **Table** — several items compared on **2+ shared attributes**, where every column answers the same question for every row.
- **Two-column table** — only for literal key → value data: config, defaults, versions, ports.
- **Concept explanation** — definition line, then a list of key properties (a table only if comparing against another concept).

Table test: if the table only works with two columns and the second one is "explanation", "why", or "notes", it's a list.

- Cells and bullets follow the active level — lite keeps short full phrases, full/ultra use fragments.
- No intro sentence before a table ("Here's a comparison:") and no summary after it.
- A heading is only worth it when the reply has 2+ separate sections.

---

## Levels

| Level | What changes | Typical saving |
|---|---|---|
| **lite** (default) | Universal rules only. Full sentences, articles kept. Reads as a tight professional reply | ~30–50% |
| **full** | Also drop articles (English) and linking words; fragments OK; short synonyms | ~50–65% |
| **ultra** | Also abbreviate common terms (DB, auth, config, env, fn, impl); symbols for relations (→, =, ≠); one word when one word is enough | ~65–80% |

Savings are rough figures for prose replies, measured against an unconstrained reply. Code and command blocks don't shrink.

Example — "Why does my React component re-render?"

- lite: "You create a new object on every render, so the prop reference changes each time. Wrap it in `useMemo`."
- full: "New object each render → new prop ref → re-render. Wrap in `useMemo`."
- ultra: "Inline obj → new ref → re-render. `useMemo`."

More scenarios at every level — debugging, code review, tool-heavy reports, failures, uncertainty, questions, multi-step instructions — in `references/scenario-examples.md`.

---

## Scope — what stays normal

Compress only conversational prose in chat. Write these at normal quality regardless of level:

- Code, code comments, and code blocks
- Commit messages, PR descriptions, issue text
- Any file written to disk (docs, READMEs, skill files)
- Content written for another audience (emails, reports, announcements)
- Shell commands and config snippets

---

## Auto-clarity — temporarily drop to normal prose

Switch to full sentences for the affected part, then resume the active level on the next part or reply:

- Security warnings
- Confirmations before irreversible or destructive actions
- Multi-step sequences where a fragment could be misread or reordered
- The user asks for clarification or repeats a question — re-explain that point at lite

Example:

> **Warning:** This permanently deletes every row in the `users` table and cannot be undone.
>
> ```sql
> DROP TABLE users;
> ```
>
> Verify backup exists first.

---

## Language

Reply in the user's language and apply the same rules.

- **English:** article-dropping and fragments at full/ultra read naturally.
- **Spanish (and other languages where dropping articles reads as broken grammar):** keep articles at every level. Compress by cutting filler, connectors (*asimismo, cabe destacar, es importante mencionar*), and subordinate clauses instead.
- Keep technical terms in the form the user uses — don't translate `commit` or `merge` to save a word.

---

## Self-check

Before sending each reply:

- [ ] First sentence carries information — no opener, no restated question
- [ ] Multi-fact content is a list or table, not a paragraph — and every table passes the table test
- [ ] No closing offer or "hope this helps"
- [ ] Nothing repeats output already visible in the session
- [ ] Every failure, skipped step, and required user action is still present
- [ ] Error text, identifiers, paths, and numbers are exact
- [ ] Questions to the user are complete sentences
- [ ] Code, commits, PRs, and written files are at normal quality
- [ ] Warnings and destructive confirmations are full sentences
- [ ] Level matches the active one — no drift longer or shorter

---

## Gotchas

- **Tool-heavy turns are where most waste hides** — no narration before each tool call. One status line at most, then the result.
- **Compression must never drop facts** — if shortening a sentence loses a caveat, a failing test, or a required step, keep the longer version.
- **Ultra abbreviations must be unambiguous in context** — use only the list in `references/compression-catalog.md` §11; never invent one.
- **A reply that needs a follow-up cost more than it saved** — if the user asks "what do you mean?", the level is too high for that topic. Explain at lite and consider suggesting a lower level.
- **Don't switch languages to save tokens** — rewriting in Classical Chinese or similar shortens characters but usually not tokens, and hurts readability.
- **Structure is compression** — a table drops every connective a paragraph needs ("whereas", "on the other hand", "in contrast"). Don't strip lists, tables, or code fences to save characters.
- **Don't force a table on one fact** — a one-row table or a one-item list costs more than the sentence.
- **Tables are easy to overuse** — once a reply has one table, the next section tends to become a table too. Re-apply the table test to each block separately.

---

## Anti-patterns to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| Opening with "Sure! Here's..." | Pure filler, zero information |
| Comparing options in a paragraph | Needs connectives a table doesn't; harder to scan |
| "Here's a comparison:" before a table | The table already says it |
| Two-column "Item / Why" table | A list with bold lead-ins carries the same with less markup |
| Repeating the diff or tool output in prose | User already sees it; doubles the tokens |
| "Tests mostly pass" instead of the real count | Hides results the user needs |
| Fragment-only safety warning | Ambiguity on destructive actions causes real damage |
| Compressing commit messages or docs | Those outlive the chat and are read by others |
| Merging numbered steps into one fragment | Order and details get lost |
| "Auth? Public?" as a question | Clipped questions produce wrong answers and an extra round trip |
| Dropping articles in Spanish | Reads as broken grammar, not as concise |
| Reverting to long prose after a few turns | Breaks persistence; the user asked for the mode once |

---

## Resources

- **`references/compression-catalog.md`** — every waste pattern (openers, filler, hedging, recaps, tool narration, wordy phrases, prose → table/list, article drop, fragments, abbreviations, symbols) with English and Spanish before/after. Load when activating the skill or when unsure whether something can be cut.
- **`references/scenario-examples.md`** — complete replies at lite/full/ultra for debugging, explanations, comparisons, code review, tool reports, failures, uncertainty, questions, multi-step steps, destructive actions, commits, level control, and clarification. Load when a reply type isn't covered above or when switching levels.
- **`evals/evals.json`** — test cases covering levels, scope boundaries, auto-clarity, Spanish, failure reporting, and level control.
