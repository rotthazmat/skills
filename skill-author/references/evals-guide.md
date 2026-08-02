# Evals Guide

## File location and format

Store test cases in `evals/evals.json` inside the skill directory:

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "...",
      "expected_output": "...",
      "files": ["evals/files/sample.php"],
      "assertions": [
        "...",
        "..."
      ]
    }
  ]
}
```

`files` is optional — include it only when the eval requires a sample file to act on.

---

## Writing prompts

- Write the prompt exactly as a real user would type it — casual phrasing, realistic context
- Vary phrasing across cases: formal, casual, abbreviated
- Include at least one edge case (boundary condition, ambiguous input, unusual request)
- Avoid "test the skill" — test real tasks like "review this file" or "help me resolve this conflict"

```json
// Good — realistic and specific
"prompt": "Review this PHP file for code style violations. List every issue you find."

// Bad — too abstract
"prompt": "Test if the code-php skill works."
```

---

## Writing expected_output

A human-readable description of what success looks like. Write it as a complete sentence describing what the agent's response must cover — not a transcript of exact wording.

```json
// Good — describes success without being brittle
"expected_output": "Lists all violations: Yoda comparison, == instead of ===, array() instead of [], unsorted array keys."

// Bad — exact wording (too brittle) or too vague
"expected_output": "Good output."
```

---

## Writing assertions

Assertions are verifiable statements about the output. Write 3–6 per eval. Each must be specific enough to PASS or FAIL unambiguously.

**Good assertions:**
- `"Reports the Yoda comparison: 'active' == $data['status']"` — names the exact issue
- `"Does not modify the file unless explicitly asked"` — behavioral constraint
- `"Uses 2-space indentation in the generated code"` — observable and specific

**Weak assertions:**
- `"The output is correct"` — too vague to grade
- `"Uses exactly the phrase 'SQL injection'"` — too brittle; correct output may use different wording

**Rules:**
- At least one assertion should check the skill's *most critical rule* — the thing that makes this skill valuable
- At least one assertion should check a behavioral constraint (what the agent must NOT do)
- Avoid asserting exact phrasing — assert the presence of a concept or finding

---

## Sample files

When an eval requires reviewing a file, store the sample in `evals/files/`:

```
evals/
├── evals.json
└── files/
    ├── bad-code.php
    └── insecure.php
```

Sample files should:
- Contain the minimum violations needed to test the skill's rules
- Be short (under 50 lines) — longer files make assertion grading ambiguous
- Not reference any real project, company name, or internal path

---

## How many evals to write

Start with 2–3. Expand after seeing real results. Aim for coverage of:

1. A realistic review/analysis task
2. A generation task (write code / write a commit message / etc.)
3. An edge case or boundary condition specific to this skill's most complex rule
