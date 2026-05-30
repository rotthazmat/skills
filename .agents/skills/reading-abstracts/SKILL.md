---
name: reading-abstracts
description: Generate structured reading abstracts (full or short) from academic texts, and handle follow-up questions anchored strictly to the provided reading. Use when the user shares a reading and asks for a summary, resumen, abstract, or resumen corto — or asks follow-up questions about a previously summarized text.
user-invocable: true
argument-hint: "e.g. full / short / corto / follow-up"
---

Skill for producing two-format reading abstracts — full (resumen-lectura) and short (resumen-corto) — from any academic or essay reading provided by the user. All content is derived exclusively from the provided text. Follow-up questions are always answered in coherence with that reading. Applies research skill principles (concept mapping, dimensional analysis, hierarchical synthesis) to organize information analytically, not just sequentially.

## When to apply this skill

Apply immediately whenever the user:

- Provides an academic text and asks for a summary, resumen, abstract, or resumen corto
- Says "hazme un resumen de esta lectura", "resume esto", "abstract from this"
- Asks for a "versión corta" or "resumen corto" of a text already summarized
- Asks follow-up questions about content covered in a previous reading summary (e.g., "cuéntame más sobre X", "¿qué dice sobre Y?")
- Asks to complement, expand, or deepen a concept from a summarized reading

Do not activate for general topic research or questions that are clearly not anchored to a specific provided text.

---

## Workflow

### Step 1 — Ingest and map the reading

Before writing a single section, build an internal map of the text:

1. **Identify the central thesis**: what is the single core argument or finding the author is making?
2. **Map key concepts**: list every term that carries conceptual weight and how each relates to the thesis
3. **Identify argumentative sections**: what logical moves does the author make? (not just chapter titles — the actual argumentative steps)
4. **Detect tensions**: does the author resolve a paradox? challenge a prior framework? signal a limit of the argument?

This map determines section structure. Sections must reflect the argument's logic, not the reading's table of contents.

### Step 2 — Apply dimensional analysis (from research skill)

Classify the content of the reading by dimension — use only the ones that are present:

| Dimension | Question it answers |
|---|---|
| **Causal** | What explains or generates the phenomenon studied? |
| **Structural** | How is the system or society organized? |
| **Historical** | How did it evolve or transform over time? |
| **Interpretative** | How is the phenomenon understood, disputed, or re-framed? |
| **Ideological** | What function do ideas, norms, or symbols serve in the system? |

Use these dimensions to assign each section of the abstract to its analytical role. This prevents a flat, sequential summary.

### Step 3 — Generate output

Produce either the full or short format based on what the user requests. If unspecified, default to **full**.

### Step 3b — Completeness audit (short format only)

Before saving the short version, run this check against the internal map from Step 1:

1. **Argumentative points**: every main point in the map must appear in the short **body** — not just the glossary. Go one by one.
2. **Structural tensions**: any tension or conflict described in the full version (competing groups, paradoxes, institutional failures) must be present in the short body, even if compressed to one sentence.
3. **Concrete examples**: when the full version uses a historical example to illustrate an abstraction, at least one example must survive into the short version. Abstraction without example is harder to study.
4. **Load-bearing terms**: any term that actively drives an argument (not just gets defined) must appear in the body. Being in the glossary is not sufficient.

If any item fails: add it with the minimum words needed. Do not expand — compress.

---

## Full format — `resumen-lectura.md`

Use for: complete academic summaries, study reference, detailed analysis.

**Header:**
```
# Resumen: [Reading title]
**Autor:** [Author name]
**Fuente:** [Source — book, journal, chapter]
**Publicado originalmente en:** [Original publication info if available]

---
```

**Body structure:**
- Numbered sections (`## 1.`, `## 2.`, etc.) following argumentative logic, not chapter order
- Subsections (`### 2.1`, `### 2.2`) for topics with multiple components
- At least 2–3 direct quotes in blockquotes (`> "..."`) anchoring critical arguments — include attribution when available
- Bullet lists for enumerations, step-by-step processes, or comparative items
- Markdown tables for structured comparisons (tripartite systems, taxonomies, contrasts)
- Academic language preserved throughout — do not simplify terminology

**Mandatory closing section:**
```markdown
## Conceptos Clave

| Término | Significado en el texto |
|---|---|
| **[term]** | [definition as used in this text — not generic] |
```
Include every term that carries conceptual weight in the reading. Definitions must reflect how the term is used *in this text*, not its general meaning.

---

## Short format — `resumen-corto.md`

Use for: quick review, accessible version for non-specialist readers, study notes.

**Header (one line):**
```
# [Reading title] — Resumen Corto
**Autor:** [Author] | [Source short title]

---
```

**Body structure:**
- Fewer sections — keep only the argumentative pillars (3–5 sections max)
- **Compress expression, never cut ideas** — every main argumentative point from the full version must appear in the short body; what changes is how much space it gets, not whether it's there
- Bold every key term on **first mention** within its section
- Quotes that state the central thesis or a key conclusion are **mandatory** regardless of count — do not omit them to stay under a number. Quotes that are purely illustrative or decorative: cap at 1–2. Total typically 2–4.
- Explanatory language: substitute jargon with accessible equivalents the first time, then use the term
- Each section opens with a plain-language question that the section answers (e.g., `## ¿Cómo usó el Inca la reciprocidad?`)

**Mandatory closing section:**
```markdown
## Conceptos para recordar

| Término | Qué es |
|---|---|
| **[term]** | [plain-language definition] |
```
The short version's glossary should be *more complete* than the full version's — because the short format explains less inline, the glossary carries more of the definitional load. Include every term mentioned in the text, even briefly.

---

## Handling follow-up questions

When the user asks a follow-up question about a summarized reading:

1. **Anchor to the text**: answer only from the content of the reading that was provided. Do not import external knowledge.
2. **Quote when possible**: use a blockquote from the original text to ground the answer.
3. **Label any external context explicitly**: if the user explicitly asks to expand beyond the text, clearly mark external content with `> [Contexto externo — no proviene de la lectura]`.
4. **Maintain dimensional coherence**: if expanding on a structural point, stay in the structural dimension. Don't drift into historical tangents unless the text supports it.
5. **Apply research skill quick mode** for follow-ups: decompose the sub-topic → expand relevant dimension → synthesize in 2–4 paragraphs → verify consistency with the reading.

---

## Hierarchical synthesis rule

Neither format is a sequential paraphrase. Every section must:

- State what the author is arguing (not just what the section is "about")
- Show how that argument connects to the central thesis
- Identify at least one tension, paradox, or non-obvious implication if present

If a section of the reading is purely definitional (e.g., a glossary entry), integrate it into a substantive section rather than creating a standalone "definitions" section.

---

## Gotchas

- **Never add external context** — if the text mentions "Karl Polanyi", do not explain who Polanyi is from general knowledge unless asked. Only what the text says about him.
- **Short ≠ truncated full** — the short format is not the full format with sections deleted. It recasts the argument in accessible language with a different structural logic.
- **Glossary definitions must be text-specific** — "mitmaq" in this reading means X; in another reading it may mean something slightly different. Always anchor to the text.
- **Quotes must be exact** — blockquote content must be verbatim from the provided text. If you cannot reproduce the exact wording, paraphrase and mark it as `[paráfrasis]`.
- **Sections follow argument, not chapter order** — a reading with 8 chapters may produce 4 abstract sections if chapters 2–3 serve the same argumentative function.
- **Coherence constraint on follow-ups** — even if the user's question goes beyond the text, bring the answer back to what the text says. Signal the limit if needed: "La lectura no cubre este punto, pero dentro de lo que trata..."
- **Glossary ≠ body presence** — a term in the glossary does not substitute for its argumentative appearance in the body. If a concept actively drives an argument (e.g., a religious concept explaining why a political project failed), it needs at least one sentence in the body even if it's also defined in the glossary.
- **Structural tensions survive compression** — when the full version describes a tension between groups, institutions, or ideas, the short version must include it even in one sentence. Tensions explain why systems work or fail; omitting them leaves the argument incomplete.
- **Concrete examples anchor abstractions** — when the full version uses a specific example (a person, an event, a date) to illustrate an abstract concept, preserve the most vivid one in the short version. An abstraction without its example is harder to study and easier to forget.

---

## Anti-patterns to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| Summarizing section by section in the order they appear | Produces a flat inventory, not an analysis; misses the argumentative structure |
| Omitting quotes entirely | Removes the anchor to the actual text; the abstract becomes unverifiable |
| Adding background knowledge about authors or periods | Violates source fidelity; introduces content the user didn't ask to be synthesized |
| Making the short glossary smaller than the full glossary | The short format explains less inline — the glossary must compensate |
| Leaving a load-bearing concept only in the glossary | The glossary defines; the body argues. A concept that drives the reading's argument must appear in both. |
| Dropping a structural tension from the short version | Tensions explain causality; without them the short version describes a system but not why it worked or broke |
| Cutting all concrete examples to "save space" | Examples are not decoration — they are the proof of the abstraction. Keep at least one per key concept. |
| Answering follow-up questions from general knowledge | Breaks coherence with the provided reading; answers may contradict the text's framing |
| Creating a "Definiciones" or "Términos" section mid-abstract | Disrupts narrative flow; definitions belong in the glossary or inline on first mention |

---

## Resources

- **`evals/evals.json`** — test cases to verify this skill produces correct output.
