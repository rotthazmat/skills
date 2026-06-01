---
name: analytical-synthesis
description: Analytical framework for mapping, structuring, and synthesizing any information into hierarchical critical analysis — without requiring external sources. Use when analyzing, comparing, evaluating, or synthesizing information from any source; or when invoked by another skill (research, reading-abstracts, human-redaction) that needs structured thinking before producing output.
user-invocable: true
argument-hint: "e.g. topic to analyze / text to synthesize"
---

Standalone analytical framework that separates thinking work from data-gathering work. Applies concept mapping, dimensional analysis, hierarchical synthesis, and cross-validation on any information already in context — without external searching. Designed to be invoked by other skills (`research`, `reading-abstracts`, `human-redaction`) or activated directly when no source-gathering is needed.

## When to apply this skill

Apply immediately when:

- Asked to analyze, compare, evaluate, or synthesize information **already available in context** — no external search needed
- A task requires structured thinking before writing or deciding
- Another skill (`research`, `reading-abstracts`, `human-redaction`) explicitly invokes this skill
- The user asks "why", "how does this connect", "what does this mean", or "what's your take" about something already shared
- Information has been gathered from any source and needs to be organized into a position, not just summarized

Do not activate when the task requires gathering external information first — use `research` for that. Do not search for external sources at any point; if information is missing, signal the gap explicitly.

**When invoked by another skill:** apply only the steps that skill delegates. `research` delegates Steps 2–5. `reading-abstracts` delegates Step 2 only. `human-redaction` delegates Step 4 only. Do not run the full workflow unless activated standalone.

---

## Workflow

### Step 1 — Map the subject

Before analyzing, convert the subject into a system. Identify:

- **Central thesis or question**: the single core thing being analyzed
- **Key concepts**: every term or element that carries analytical weight
- **Actors or variables**: who or what drives the phenomenon
- **Relationships**: how elements connect, reinforce, or contradict each other
- **Relevant dimensions**: which analytical angles are present in this subject

This map determines structure. Without it, analysis is linear and flat.

### Step 2 — Apply dimensional analysis

Classify the information by dimension — use only the ones present in the subject. Load `references/dimensions.md` for the full guide with examples per dimension.

| Dimension | Question it answers |
|---|---|
| **Causal** | What explains or generates this? |
| **Structural** | How is it organized? |
| **Historical** | How did it evolve? |
| **Empirical** | What do the data say? |
| **Interpretive** | How is it understood or disputed? |
| **Ideological** | What function do ideas or values serve here? |

Dimensions are a tool, not a checklist. Force none; skip irrelevant ones.

### Step 3 — Hierarchical synthesis

Not a summary — an integration. Two layers:

**Layer 1 — Structured account:** what each dimension reveals, what patterns emerge, what tensions or contradictions exist between dimensions.

**Layer 2 — Explanatory model:** a position constructed from the evidence. Not "all sides have a point" — a specific explanation that resolves or explicitly names the tensions. This is the actual analytical output.

### Step 4 — Cross-validation

Before closing, verify:

- Is there an alternative explanation that accounts for the same evidence better?
- What data or facts would refute the model built in Step 3?
- Which dimensions remain uncovered? Are they relevant?
- Does the conclusion follow directly from the evidence, or does it overreach?

If the conclusion overreaches: scale it down. Never add new evidence at this stage to prop up an overreaching claim.

### Step 5 — Final model structure

Output the analysis in:

1. **Conceptual frame** — key definitions and how the question is bounded
2. **Dimensional findings** — what each relevant dimension reveals
3. **Tensions and debates** — competing explanations or contradictions
4. **Integrated position** — the explanatory model from Step 3

---

## Gotchas

- **Map before analyzing** — a flat list of facts is not a map. The map must show relationships, not just elements.
- **Synthesis ≠ summary** — if the output paraphrases the input, Step 3 hasn't happened. The model must commit to an explanation.
- **Dimensions are not sections** — don't create a section per dimension mechanically. Use them to assign analytical weight, then write sections that reflect the argument's logic.
- **Cross-validation is not optional** — skipping Step 4 produces confident-sounding claims that don't hold under scrutiny.
- **No external search** — this skill works only on information already in context. If data is missing, signal it explicitly rather than importing external knowledge.

---

## Anti-patterns

| Anti-pattern | Why it's wrong |
|---|---|
| Summarizing by dimension | Produces an inventory organized by label, not an integrated analysis |
| "All sides have valid points" as conclusion | Avoids the analytical work; the model must resolve or name the tension |
| Applying all 6 dimensions to every task | Forces artificial structure; irrelevant dimensions dilute the analysis |
| Skipping the map and going straight to dimensions | Analysis becomes linear; relationships between elements are missed |
| Adding new evidence in Step 4 to rescue an overreaching conclusion | Masks a weak argument; scale the conclusion instead |

---

## Resources

- **`references/dimensions.md`** — full dimensional analysis guide with examples per dimension. Load when the right dimensions for a task are unclear.
- **`evals/evals.json`** — test cases to verify this skill produces correct analytical output.
