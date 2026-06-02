---
name: project-python
description: "Apply to ALL Python projects without exception. Triggers on: creating a new Python project; refactoring, improving, or reorganizing existing Python code; applying best practices, SOLID, or KISS to Python; adding or restructuring tests; adding new modules or features to a Python project; reviewing Python project structure. Any request involving Python code — new or existing — must follow these conventions: src/ modules, venv/, pytest with conftest.py, index.py orchestrator, test.py runner, SOLID+KISS principles."
compatibility: Designed for Claude Code
user-invocable: true
argument-hint: "optional: module or area to focus on"
---

# Python Project Conventions

**This skill applies to every Python project task: creating, refactoring, improving, adding features, adding tests, applying best practices, or restructuring. No exceptions unless the user explicitly overrides.**

## When to apply this skill

Apply immediately and fully whenever the user:

- Creates a new Python project or script
- Asks to refactor, improve, clean up, or reorganize Python code
- Asks to apply best practices, SOLID, or KISS to Python code
- Adds a new module, feature, or functionality to a Python project
- Adds, restructures, or improves tests in a Python project
- Asks to follow the same structure/conventions as another Python project

Do not wait to be asked — enforce these conventions proactively on every Python task.

## Folder structure

```
project-name/
├── src/
│   ├── __init__.py
│   └── <module>/
│       ├── __init__.py
│       └── operations.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_<module>.py
├── venv/            (git-ignored)
├── index.py
├── test.py
├── requirements.txt
├── .gitignore
├── CLAUDE.md
└── README.md
```

### input/ and output/ directories

Only create these when the project takes user-provided files as input or generates file output:

- `input/` — user drops source files here before running. Git-ignored.
- `output/` — generated files are written here. Git-ignored.

When present, both are created at runtime by `index.py` via `mkdir(exist_ok=True)` so they never need to be committed.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Always use `venv/bin/pip` to install (Linux/Mac) or `venv\Scripts\pip` (Windows) — never the system Python. In code, always use `sys.executable -m pytest` instead of hardcoded paths.

## Running

Activate the venv once per session, then use `python` (not `python3`):

```bash
source venv/bin/activate
python index.py
python test.py
```

`source venv/bin/activate` prepends `venv/bin/` to `PATH`. That folder contains a `python` symlink pointing to the Python 3 interpreter used to create the venv — so `python`, `pip`, and `pytest` all resolve to the venv versions automatically. `python3` is only needed once, to create the venv itself.

## src/ modules

One subfolder per concern. Each has `__init__.py` (empty) and `operations.py` with the actual logic.

```
src/scanner/operations.py    — discover / list / sort input files
src/converter/operations.py  — transform data, produce output
src/processor/operations.py  — etc.
```

Keep modules flat. Don't nest unless complexity demands it. Never import from `index.py` inside a module.

**When `operations.py` grows:** if a single `operations.py` exceeds ~150 lines or handles more than one clearly separable sub-concern, split it into multiple focused files within the same module subfolder (e.g. `src/parser/reader.py`, `src/parser/validator.py`). The subfolder stays — only the single file splits.

### Logging module (universal — add to every project with persistent processing)

Add `src/logger/operations.py` when the project runs unattended, processes batches, or needs an audit trail. Use `assets/logger.py` as the template. Wire it in `index.py`:

```python
from src.logger.operations import get_logger
logger = get_logger("app", log_file=Path("logs/app.log"))
```

Add `logs/` to `.gitignore`. For simple one-shot scripts where a user watches the terminal, `print()` in `index.py` is sufficient.

## index.py

Thin orchestrator — wires modules, owns I/O paths, prints progress. No business logic here. Use `assets/index.py` as the starting template.

Rules:
- All `Path` constants (`INPUT_DIR`, `OUTPUT_DIR`) defined at the top
- `mkdir(exist_ok=True)` called at runtime, never committed to git
- Print `[{i}] {item.name}` for each item **before** the heavy processing call
- Guard against empty input with `sys.exit(1)`
- No domain logic — only calls into `src/` modules

### CLI arguments (project-specific — when the tool needs runtime parameters)

Use `assets/cli-index.py` instead of `assets/index.py` when the project requires command-line flags such as `--input`, `--output`, `--verbose`, or any custom options. The CLI template uses `argparse` and follows the same orchestration rules — it only adds argument parsing before the main logic.

### Multiple entry points (project-specific — when a project has several modes)

If a project has multiple independent operations (e.g. `import.py`, `export.py`, `report.py`), create one `index_<mode>.py` per mode rather than one monolithic entry point with subcommands. Each entry point remains a thin orchestrator.

## test.py

```python
import subprocess
import sys


def main() -> None:
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("pytest not found. Run: python -m venv venv && pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTests interrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

`sys.executable` apunta al Python que corre el script — sea del venv activado o no, en cualquier OS. Nunca uses rutas hardcodeadas como `venv/bin/pytest` (falla en Windows) ni bare `pytest` (puede resolver al Python del sistema).

## Tests

Use `assets/conftest.py` as the base for `tests/conftest.py` and `assets/test_module.py` as the base for each `tests/test_<module>.py`. Load `references/testing.md` for full worked examples and anti-patterns.

### Coverage goals

**Rule: maximum scenario coverage, minimum number of tests.**

Every test must cover a scenario not already covered by another. Never add a test just to increase count. If removing a test wouldn't reduce coverage, remove it.

Each function needs both **positive** and **negative** cases:

**Positive (passing) cases:**
| Scenario | Example |
|---|---|
| Happy/golden path | Valid input → expected output |
| Edge case | Case-insensitive extensions, mixed file types, Unicode names |
| Side effects | Output file exists, correct size, correct format |

**Negative (failing) cases — always required, never skip:**
| Scenario | Example |
|---|---|
| Empty input | Empty folder → `[]` or early exit |
| Missing resource | Non-existent path → `FileNotFoundError` |
| Wrong type | File used as directory → `NotADirectoryError` |
| Invalid data | Empty list → `ValueError` |
| Unsupported format | Wrong file type → excluded or raises |

One distinct scenario per test. A test that checks two unrelated things is two tests.

## .gitignore

```gitignore
venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.vscode/
.idea/
```

Add `/input/` and `/output/` when those directories are part of the project. Add `logs/` when the logging module is used.

## CLAUDE.md

Include: project overview, running instructions, testing instructions, setup, source layout tree, key design decisions.

## README.md

Include: what it does, quick start (setup + run), supported formats/inputs, how it works, testing, requirements.

## SOLID, Separation of Concerns, KISS, and Best Practices

These are mandatory on every Python project — not optional guidelines.

### SOLID

- **S — Single Responsibility**: one module = one job. Scanner scans. Converter converts. Processor processes. `index.py` only orchestrates.
- **O — Open/Closed**: extend behavior by adding to data structures (e.g. a `SUPPORTED_EXTENSIONS` set), not by modifying existing control flow.
- **L — Liskov Substitution**: functions must work correctly with any valid input of the expected type — don't add hidden assumptions about the caller.
- **I — Interface Segregation**: keep functions small and focused. A function that does two unrelated things is two functions.
- **D — Dependency Inversion**: `index.py` depends on modules; modules never import from `index.py`.

### Separation of Concerns

Each layer owns exactly one concern and nothing else:
- `src/<module>/operations.py` — pure logic, no I/O, no printing
- `index.py` — I/O paths, directory setup, progress output, orchestration
- `tests/` — test logic only, never calls `index.py` directly

A module that prints to the console or reads from disk paths it didn't receive as arguments is violating this.

### KISS

- No classes, inheritance, or design patterns unless complexity demands them.
- Three similar lines beats a premature abstraction.
- No error handling for scenarios that can't happen. Validate only at system boundaries (user input, external APIs).
- Don't design for hypothetical future requirements.

### Best Practices

- Default to no comments. Add one only when the WHY is non-obvious.
- Use `pathlib.Path` for all filesystem operations — never raw strings.
- Sort file lists case-insensitively and ascending (`key=lambda p: p.name.lower()`).
- Type-hint all function signatures.
- Never hardcode paths — receive them as parameters or define them as constants in `index.py`.

## Gotchas

- In `test.py`, always use `sys.executable -m pytest` — never `venv/bin/pytest` (breaks on Windows) nor bare `pytest` (may resolve to system Python).
- On Windows, terminal setup commands use `venv\Scripts\pip` instead of `venv/bin/pip`. In code, always use `sys.executable` to avoid OS-specific paths.
- When `input/` and `output/` are used, create them via `mkdir(exist_ok=True)` in `index.py` — never commit them.
- `python3` is used only once — to create the venv. Every subsequent command uses `python` inside the activated venv.
- Never pass raw string paths between modules — use `pathlib.Path` and receive paths as parameters.
- **PDF rendering:** For simple Markdown use WeasyPrint (~15 MB, no JS). For complex content with Mermaid diagrams or JavaScript use Playwright (~300 MB, requires `playwright install chromium` after `pip install playwright`). WeasyPrint requires GTK3 on Windows (not included by default) — prefer Playwright for cross-platform projects with complex rendering.
- **Projects with external binary downloads** (e.g. Playwright's Chromium): include `uninstall.py` using `assets/uninstall.py` as template. Borra `venv/` y la carpeta del binario en cualquier OS.

## Resources

- **`assets/index.py`** — starter template for `index.py`. Use when creating the entry point.
- **`assets/cli-index.py`** — argparse entry point template. Use instead of `assets/index.py` when the project needs CLI flags (`--input`, `--output`, `--verbose`, etc.).
- **`assets/conftest.py`** — starter template for `tests/conftest.py`. Use when creating or scaffolding the test suite.
- **`assets/test_module.py`** — starter template for `tests/test_<module>.py`. Use when creating a new test file.
- **`assets/logger.py`** — `get_logger()` template for `src/logger/operations.py`. Use when the project needs persistent file logging.
- **`references/testing.md`** — full conftest.py and test file examples, mocking patterns, anti-patterns table, and parametrize guidance. Load when writing or reviewing tests.
- **`references/solid-examples.md`** — before/after worked examples of SOLID and Separation of Concerns applied to Python modules. Load when refactoring or restructuring a project.
- **`references/migration.md`** — step-by-step guide for migrating an existing monolithic script to these conventions. Load when refactoring an existing project.
- **`assets/uninstall.py`** — cross-platform uninstall script template. Use when the project downloads external binaries (e.g. Playwright's Chromium). Borra `venv/` y el directorio del binario según el OS.
- **`evals/evals.json`** — test cases covering project creation, refactoring, and test authoring scenarios.
