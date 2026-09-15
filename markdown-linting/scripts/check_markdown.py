#!/usr/bin/env python3
"""Heuristic static checker for the rules in ../SKILL.md.

Rule IDs mirror the numbering in ../references/rules-reference.md, which is
itself based on the standard markdownlint/mdl rule catalog (MD001-MD047).

Not a full CommonMark parser -- it uses line-based heuristics that cover the
common cases. Treat findings as strong hints, not ground truth; use judgment
on any borderline result. Two rules from the catalog are intentionally not
checked here: MD006 (top-level list indentation) and MD005 (sibling list
indentation) both require real list-nesting state to check reliably without
false positives; enforce them by eye instead.
"""

import argparse
import json
import re
import sys

BULLET_RE = re.compile(r"^(\s*)([-*+])(\s+)\S")
ORDERED_RE = re.compile(r"^(\s*)(\d+)([.)])(\s+)\S")
ATX_HEADING_RE = re.compile(r"^(#{1,6})(\s*)(.*)$")
CLOSED_ATX_TRAILING_RE = re.compile(r"^(.*\S)\s+#{1,6}\s*$")
FENCE_RE = re.compile(r"^(\s*)(```|~~~)(\S*)\s*$")
BARE_URL_RE = re.compile(r"(?<![(<\[])\bhttps?://\S+")
EMPTY_ALT_IMAGE_RE = re.compile(r"!\[\s*\]\([^)]*\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
REVERSED_LINK_RE = re.compile(r"\([^()\s][^()]*\)\[[^\[\]]*\]")
LINK_TEXT_SPACE_RE = re.compile(r"\[(?:\s+[^\[\]]*|[^\[\]]*\s+)\]\(")
BLOCKQUOTE_RE = re.compile(r"^ {0,3}>")
BLOCKQUOTE_MULTISPACE_RE = re.compile(r"^ {0,3}>( {2,})\S")
HR_RE = re.compile(r"^ {0,3}([-*_])(?:\s*\1){2,}\s*$")
DOLLAR_LINE_RE = re.compile(r"^\s*\$\s+\S")


def find_spaced_emphasis(line):
    """Find emphasis spans whose content touches the marker with whitespace
    (e.g. '** bold **'). Markers are symmetric (the same token opens and
    closes), so occurrences are paired sequentially -- 1st with 2nd, 3rd
    with 4th -- rather than matched with a single regex, which would wrongly
    pair the closing marker of one span with the opening marker of the next."""
    results = []

    def check_pairs(text, marker, source):
        positions = [m.start() for m in re.finditer(re.escape(marker), text)]
        for i in range(0, len(positions) - 1, 2):
            start = positions[i] + len(marker)
            end = positions[i + 1]
            content = text[start:end]
            if content and (content[0] in " \t" or content[-1] in " \t"):
                results.append(source[positions[i]:positions[i + 1] + len(marker)])

    check_pairs(line, "**", line)
    check_pairs(line, "__", line)
    # Mask double markers before scanning for single ones so a '**' pair
    # isn't miscounted as two separate '*' occurrences.
    check_pairs(re.sub(r"\*\*", "XX", line), "*", line)
    check_pairs(re.sub(r"__", "XX", line), "_", line)

    return results


def strip_inline_code(line):
    """Neutralize inline code spans so example syntax inside backticks
    (e.g. a doc that mentions `![](url)` as an anti-pattern) isn't
    mistaken for actual markdown to check. Replaced with same-length filler
    (not deleted) so a marker directly touching the span, as in
    `` **`code`text** ``, doesn't end up looking like it touches whitespace."""
    return INLINE_CODE_RE.sub(lambda m: "x" * len(m.group(0)), line)


def check_file(path):
    findings = []

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            raw = f.read()
    except OSError as e:
        return [{"line": 0, "rule": "read-error", "message": str(e)}]

    if raw == "":
        return findings

    lines = raw.split("\n")
    if raw.endswith("\n"):
        lines = lines[:-1]
        trailing_newline = True
    else:
        trailing_newline = False

    if not trailing_newline:
        findings.append({
            "line": len(lines),
            "rule": "MD047",
            "message": "File does not end with a newline.",
        })
    elif len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
        findings.append({
            "line": len(lines),
            "rule": "MD047",
            "message": "File ends with trailing blank line(s); should end with exactly one newline.",
        })

    in_fence = False
    fence_char = None
    fence_start_line = None
    fence_lang = None
    fence_body_lines = []
    heading_levels = []
    h1_count = 0
    bullet_markers_used = set()
    hr_styles = {}
    blank_run = 0
    front_matter_end = -1
    in_blockquote_block = False
    blank_after_blockquote = False

    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                front_matter_end = i
                break

    def flush_fence_dollar_check():
        if fence_lang in ("bash", "sh", "shell", "zsh", "console") and fence_body_lines:
            content_lines = [l for l in fence_body_lines if l.strip() != ""]
            if content_lines and all(DOLLAR_LINE_RE.match(l) for l in content_lines):
                findings.append({
                    "line": fence_start_line, "rule": "MD014",
                    "message": "Every line in the shell code block is prefixed with '$' and no output is shown; drop the '$' prefixes.",
                })

    for idx, line in enumerate(lines):
        lineno = idx + 1

        if idx <= front_matter_end:
            continue

        stripped = line.rstrip("\n")

        if "\t" in stripped:
            findings.append({
                "line": lineno, "rule": "MD010",
                "message": "Hard tab character found; use spaces.",
            })

        if stripped != stripped.rstrip():
            findings.append({
                "line": lineno, "rule": "MD009",
                "message": "Trailing whitespace found.",
            })

        if stripped.strip() == "":
            blank_run += 1
        else:
            if blank_run >= 2:
                findings.append({
                    "line": lineno - 1, "rule": "MD012",
                    "message": "Multiple consecutive blank lines.",
                })
            blank_run = 0

        fence_match = FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group(2)
            lang = fence_match.group(3)
            if not in_fence:
                in_fence = True
                fence_char = marker
                fence_start_line = lineno
                fence_lang = lang
                fence_body_lines = []
                if lang == "":
                    findings.append({
                        "line": lineno, "rule": "MD040",
                        "message": "Fenced code block opened without a language tag.",
                    })
            elif marker == fence_char:
                in_fence = False
                flush_fence_dollar_check()
                fence_char = None
                fence_lang = None
                fence_body_lines = []
            continue

        if in_fence:
            fence_body_lines.append(stripped)
            continue

        leading_spaces = len(line) - len(line.lstrip(" "))
        heading_source = None
        indented_heading = False
        if leading_spaces == 0:
            heading_source = stripped
        elif 1 <= leading_spaces <= 3:
            heading_source = stripped.lstrip(" ")
            indented_heading = heading_source.startswith("#")

        heading_match = ATX_HEADING_RE.match(heading_source) if heading_source else None
        if heading_match and heading_match.group(1):
            if indented_heading:
                findings.append({
                    "line": lineno, "rule": "MD023",
                    "message": "Heading is indented; headings must start at the beginning of the line.",
                })

            level = len(heading_match.group(1))
            spacing = heading_match.group(2)
            text = heading_match.group(3)

            closed_match = CLOSED_ATX_TRAILING_RE.match(text) if text else None
            if closed_match and set(text[len(closed_match.group(1)):].strip()) == {"#"}:
                findings.append({
                    "line": lineno, "rule": "MD003",
                    "message": "Closed ATX style heading ('## Heading ##'); this project uses open ATX only.",
                })
                text = closed_match.group(1)

            if text != "":
                if spacing == "":
                    findings.append({
                        "line": lineno, "rule": "MD018",
                        "message": "No space after '#' on ATX heading.",
                    })
                elif len(spacing) > 1:
                    findings.append({
                        "line": lineno, "rule": "MD019",
                        "message": "Multiple spaces after '#' on ATX heading.",
                    })

            if level == 1:
                h1_count += 1
                if h1_count > 1:
                    findings.append({
                        "line": lineno, "rule": "MD025",
                        "message": "Multiple H1 headings in one document.",
                    })

            if heading_levels and level > heading_levels[-1] + 1:
                findings.append({
                    "line": lineno, "rule": "MD001",
                    "message": f"Heading level jumps from H{heading_levels[-1]} to H{level}; do not skip levels.",
                })
            heading_levels.append(level)

            if text.rstrip().endswith((".", ",", ";", ":")):
                findings.append({
                    "line": lineno, "rule": "MD026",
                    "message": "Heading ends with trailing punctuation.",
                })

            prev = lines[idx - 1].strip() if idx > 0 and idx - 1 > front_matter_end else ""
            nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            if idx - 1 > front_matter_end and prev != "":
                findings.append({
                    "line": lineno, "rule": "MD022",
                    "message": "Missing blank line before heading.",
                })
            if idx + 1 < len(lines) and nxt != "":
                findings.append({
                    "line": lineno, "rule": "MD022",
                    "message": "Missing blank line after heading.",
                })
            in_blockquote_block = False
            blank_after_blockquote = False
            continue

        hr_match = HR_RE.match(stripped)
        if hr_match:
            char = hr_match.group(1)
            hr_styles.setdefault(char, lineno)
            in_blockquote_block = False
            blank_after_blockquote = False
            continue

        if BLOCKQUOTE_RE.match(stripped):
            if blank_after_blockquote:
                findings.append({
                    "line": lineno, "rule": "MD028",
                    "message": "Blank line splits what looks like one blockquote into two separate blocks.",
                })
            if BLOCKQUOTE_MULTISPACE_RE.match(stripped):
                findings.append({
                    "line": lineno, "rule": "MD027",
                    "message": "Multiple spaces after the blockquote '>' symbol.",
                })
            in_blockquote_block = True
            blank_after_blockquote = False
        elif stripped.strip() == "":
            if in_blockquote_block:
                blank_after_blockquote = True
        else:
            in_blockquote_block = False
            blank_after_blockquote = False

        bullet_match = BULLET_RE.match(stripped)
        if bullet_match:
            bullet_markers_used.add(bullet_match.group(2))

        code_free = strip_inline_code(stripped)

        for m in BARE_URL_RE.finditer(code_free):
            findings.append({
                "line": lineno, "rule": "MD034",
                "message": f"Bare URL found: {m.group(0)}",
            })

        for m in EMPTY_ALT_IMAGE_RE.finditer(code_free):
            findings.append({
                "line": lineno, "rule": "MD045",
                "message": "Image with empty alt text.",
            })

        for m in REVERSED_LINK_RE.finditer(code_free):
            findings.append({
                "line": lineno, "rule": "MD011",
                "message": f"Reversed link syntax found: {m.group(0)} (should be [text](url)).",
            })

        for m in LINK_TEXT_SPACE_RE.finditer(code_free):
            findings.append({
                "line": lineno, "rule": "MD039",
                "message": f"Spaces inside link text brackets: {m.group(0)}",
            })

        for snippet in find_spaced_emphasis(code_free):
            findings.append({
                "line": lineno, "rule": "MD037",
                "message": f"Spaces inside emphasis markers: {snippet}",
            })

    if in_fence:
        flush_fence_dollar_check()

    if len(bullet_markers_used) > 1:
        findings.append({
            "line": 0, "rule": "MD004",
            "message": f"Multiple bullet markers used in one document: {sorted(bullet_markers_used)}",
        })

    if len(hr_styles) > 1:
        findings.append({
            "line": 0, "rule": "MD035",
            "message": f"Multiple horizontal rule styles used, first seen at lines: {hr_styles}",
        })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Heuristic markdown best-practices checker (see references/rules-reference.md for rule IDs).",
    )
    parser.add_argument("files", nargs="+", help="Markdown file(s) to check")
    args = parser.parse_args()

    all_findings = {}
    any_findings = False
    for path in args.files:
        findings = check_file(path)
        all_findings[path] = findings
        if findings:
            any_findings = True

    print(json.dumps(all_findings, indent=2))
    sys.exit(1 if any_findings else 0)


if __name__ == "__main__":
    main()
