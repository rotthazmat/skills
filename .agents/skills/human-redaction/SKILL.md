---
name: human-redaction
description: Rewrites or reviews text to eliminate AI writing patterns and produce authentic human-sounding prose. Use when asked for human-like redaction, humanize text, avoid AI detection, make writing sound natural, rewrite like a human, or similar requests. Prioritizes Spanish and English but works in any language.
user-invocable: true
argument-hint: "optional: paste text to humanize, or describe the writing task"
metadata:
  version: "1.1"
---

Simulate authentic human writing by diagnosing and eliminating AI patterns, then applying humanization techniques. The goal is prose that reads as written by a specific person with a voice — not a polished, neutral machine.

## When to apply this skill

Apply immediately and fully when:

- User says "humanize", "rewrite like a human", "make it sound natural", "avoid AI detection"
- User asks for "redacción humana", "que no parezca IA", "hazlo sonar natural"
- User submits a draft and asks to make it less robotic or more personal
- User is writing something where AI-generated content is unwanted (academic, professional, personal)
- User asks for help writing something that should sound like them specifically

---

## Modes

**Rewriting existing text** (most common): follow Steps 1–4 below.

**Writing from scratch in a human voice**: use the Step 1 checklist as a *negative space guide* — a list of things the output must not contain. Before writing, note 2–3 patterns to actively avoid given the genre and register. After a first draft, run Step 4 on what you produced. The same patterns apply; they just appear in your own output instead of someone else's.

---

## Workflow

Follow these four steps in order. Never skip diagnosis before rewriting.

### Step 1 — Diagnose

Scan the text (or the task brief) for AI patterns. Load `references/ai-patterns.md` for the full catalog. Key flags to check:

**Vocabulary red flags (universal):**
- Buzzwords: *delve, leverage, realm, robust, comprehensive, nuanced, multifaceted, foster, empower, unlock, elevate, navigate, transformative, cutting-edge, seamlessly, tapestry, vibrant, garner, underscore, pivotal, testament, intricate*
- Transition words used as sentence starters: *Furthermore, Moreover, Additionally, Notably, It's worth noting, In conclusion*
- Hedge clusters: *may, might, could potentially, in some cases, it is important to note*
- Forced drama: *"but here's the thing", "hot take:", "here's the kicker", "spoiler:"*
- "is/are" avoidance: *serves as, stands as, marks, represents, features, boasts* (instead of plain *is*)

**Spanish-specific red flags:**
- Openers: *"En el mundo actual", "Hoy en día", "En este sentido", "Cabe destacar que", "Es importante mencionar", "Es importante destacar que", "Es evidente que"*
- Closers: *"En conclusión", "A modo de resumen", "En definitiva", "En síntesis", "Vale la pena señalar que"*
- Hedges: *"cabe señalar", "resulta fundamental", "es preciso destacar", "se puede observar que", "podría decirse"*
- Filler connectors: *"Asimismo", "Ciertamente", "Sin duda", "En consecuencia", "Por lo tanto"* (when mechanical)
- Spanish buzzwords: *encomiable, sinérgico/a, transformador/a, invaluable, potenciar, facilitar, maximizar, subrayar, cautivar, explorar* (in "vamos a explorar...")

**Structural red flags:**
- Uniform paragraph lengths (all roughly the same size)
- Rule-of-three triplets everywhere ("X, Y, and Z" constructions repeated)
- Perfect intro → 3-point body → conclusion scaffold
- Negative parallelisms: *"It's not X, it's Y"* / *"No se trata de X, sino de Y"*
- Appended "-ing" clauses that add no substance: *"...demonstrating their commitment to quality"*
- Every paragraph ends with a transition to the next
- Bullet lists where prose would be natural
- Headers in casual writing (emails, essays, personal texts)
- Wordcount inflation: paragraphs that can be halved without losing meaning

**Tone and substance red flags:**
- Emotions described from the outside ("this situation can be challenging") instead of felt
- No personal opinion, only balanced neutral statements
- Excessive em dashes (—) used where a comma or period would work (English)
- Vague authority: *"experts argue", "studies show", "observers note"* / *"según expertos", "los analistas señalan"*
- Generic analogies: *"like a well-oiled machine"*, *"two sides of the same coin"*
- Significance overemphasis: *"pivotal moment", "marks a shift", "indelible mark"*
- Summarizes/reviews instead of analyzes or argues — all vocabulary, no substance
- Self-referential AI disclaimers ("as an AI...", "I don't have personal experience but...")

**Technical and structural precision flags:**
- Technical terms paraphrased or synonymized (e.g. "juvenile court" → "court system for youngins")
- Repeated three-item serial lists *within the same paragraph*, not just overall
- Multiple closing paragraphs that all say the same thing (padding to meet word count)
- Specific words: *"thought-provoking"*, *"lens"* (as in "through the lens of"), *"intricate interplay"*

Report findings before rewriting. Example:
> Found: 3 buzzwords (leverage, robust, nuanced), 2 mechanical transitions (Furthermore, Moreover), uniform paragraph length, no personal voice.

### Step 2 — Plan edits

Before touching the text, state which techniques you'll apply from `references/humanization-techniques.md`. Match the pattern to the technique number:

| Pattern found | Technique |
|---|---|
| Buzzwords / corporate jargon | #1 vary length + plain words |
| Mechanical transitions | Cut or use implicit flow (no technique number — just delete) |
| Uniform sentence/paragraph length | #1 vary sentence length |
| Contractions absent where appropriate | #2 contractions and spoken register |
| Generic / placeholder examples | #3 replace with specific detail |
| Hedge overload | #4 commit to opinions |
| Emotional flatness | #5 show don't tell |
| Formulaic opener or closer | #6 cut formulaic openers and closers |
| Rigid scaffold / announced structure | #7 break structural scaffolding |
| Punctuation monotony | #8 use punctuation naturally |
| "is/are" avoidance (*serves as, stands as*) | #11 flatten is/are avoidance |
| Negative parallelisms (*Not X, it's Y*) | #12 break negative parallelisms |
| Appended "-ing" clauses | #13 trim appended -ing clauses |
| Vague authority (*experts say, studies show*) | #14 replace vague authority attributions |
| Wordcount / conclusion inflation | #15 deflate wordcount + #18 end conclusion once |
| Summary/review instead of analysis | #16 argue don't summarize |
| Technical terms paraphrased | #17 preserve technical terms |
| Overreaching conclusions / contradictions | #19 stay accountable to sources |

### Step 3 — Rewrite

Apply edits. Preserve the original meaning and register (formal/informal), but alter the surface form enough to read as human. Do not:
- Simply swap buzzwords for synonyms that are equally generic
- Add fake personal anecdotes unless the user explicitly asks
- Over-correct into slang if the original is formal

Do:
- Vary sentence length deliberately (short punchy sentences break monotony)
- Use contractions when register allows (*don't*, *it's*, *I've* / *no*, *es*, *tengo*)
- Plant one or two specific concrete details (a number, a name, a sensory image)
- Let one sentence be structurally unusual — a fragment, a rhetorical question, a long winding clause
- In Spanish: use the personal voice, first-person verbs, and regionally natural phrasing

### Step 4 — Verify

After rewriting, do a final pass:
- Did you introduce any new buzzwords or clichés?
- Does the text still start with a broad/generic opener?
- Is the rhythm varied, or did you create a new monotonous pattern?
- Does the conclusion sound formulaic ("In conclusion, we have seen...")?
- Spanish: does it still use impersonal constructions where personal ones would be natural?

**Source consistency check (always run this):**
- Does every conclusion follow logically from evidence actually presented in the text?
- Does the text contradict itself between sections — a term defined one way early, used differently later?
- Are any sources cited for claims they don't actually support?
- Does the conclusion introduce claims that were never established in the body?

If any check fails, fix before delivering. For consistency failures: scale the conclusion down to match the evidence — don't patch by adding new unsupported claims.

**Deep coherence audit:** when the text is analytically complex (comparisons, causal claims, multi-section arguments), invoke the `analytical-synthesis` skill's Step 4 (cross-validation) before closing.

---

## Gotchas

- **Don't over-humanize** — removing all structure makes text hard to follow. The goal is natural, not chaotic.
- **Register matters** — a formal report humanized too aggressively becomes unprofessional. Match the output register to the context.
- **Contractions in Spanish** — Spanish doesn't contract the same way English does. Humanization in Spanish relies more on verb choice, word order, and personal voice than on contractions.
- **Em dash vs. dash** — in Spanish, em dashes are legitimate for dialogue/parenthetical; in English they're an AI red flag when overused.
- **Specificity beats authenticity tricks** — one concrete specific detail (a real number, a named place, a sensory observation) is worth ten stylistic tweaks.
- **Don't invent facts** — if the user's text makes a claim, humanize the *language* around it, not the *content*.
- **Stay accountable to sources** — human writers only draw conclusions their evidence supports. A conclusion that outreaches its evidence is a clear AI tell, even if the prose itself sounds natural. Scale conclusions down to match the evidence; never add new unsupported claims to justify an overreaching conclusion.
- **Check for internal contradictions** — re-read the full text after rewriting. AI doesn't catch its own contradictions between sections; you have to.

---

## Anti-patterns

| What to avoid | Why |
|---|---|
| Replacing "leverage" with "utilize" | Both are corporate jargon — go to plain verbs (*use*, *apply*) |
| Adding "I personally think..." everywhere | Forced, reads as a different kind of AI pattern |
| Breaking every long sentence into three short ones | Creates a new monotonous rhythm |
| Starting with "Look," or "Here's the thing:" | These have become their own AI clichés |
| Removing all hedging | Some contexts require epistemic humility; hedge only when necessary |
| Translating idioms literally between languages | Each language has its own natural informal markers |

---

## Resources

- **`references/ai-patterns.md`** — full catalog of AI writing patterns with Spanish and English examples. Load when diagnosing a text.
- **`references/humanization-techniques.md`** — humanization techniques with before/after examples in both languages. Load when planning Step 2 edits.
- **`evals/evals.json`** — test cases.
