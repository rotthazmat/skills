# Migrating an Existing Project to These Conventions

## Rule: one module at a time

Never refactor everything at once. Extract one concern, verify it works, move to the next.

## Step-by-step

### 1 — Audit the current state

Read every Python file and classify each block of code:
- **Business logic** → belongs in `src/<module>/operations.py`
- **I/O paths / directory setup** → belongs in `index.py`
- **Progress printing** → belongs in `index.py`
- **Orchestration** → belongs in `index.py`

### 2 — Create the skeleton without moving code yet

```bash
mkdir -p src tests
touch src/__init__.py tests/__init__.py tests/conftest.py
```

### 3 — Extract one module at a time

1. Identify one concern (e.g. file scanning)
2. Create `src/<module>/__init__.py` and `src/<module>/operations.py`
3. Move only that concern's logic into `operations.py`
4. In the original file, replace the moved code with a call to the new function
5. Run existing tests (if any) — verify nothing broke before continuing

### 4 — Create index.py

Once all concerns are extracted into modules:
- Create `index.py` using `assets/index.py` as base
- Import from `src/` modules only
- Move all `Path` constants, `mkdir` calls, and `print` statements here
- Delete the original entry point if it's been fully replaced

### 5 — Create the test suite

- Create `tests/conftest.py` using `assets/conftest.py` as base
- Create `tests/test_<module>.py` for each extracted module using `assets/test_module.py`
- Cover positive and negative cases per module (see `references/testing.md`)

### 6 — Finish up

- Create `test.py` using the template in SKILL.md
- Update `.gitignore` to include `venv/`, `__pycache__/`, `input/`, `output/` as needed
- Update or create `CLAUDE.md` and `README.md`
- Update `requirements.txt` to match what's actually imported

## Common migration pitfalls

| Pitfall | Fix |
|---|---|
| Moving code that still has hidden dependencies on global state | Make all dependencies explicit function parameters before moving |
| Extracting a module that still prints or hardcodes paths | Strip prints and path constants before moving to `src/` |
| Writing tests for the old monolithic entry point | Test the extracted `src/` functions directly, not the old code |
| Trying to add tests before extraction is done | Extract first, test second — testing a monolith is harder |
