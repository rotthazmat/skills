# SOLID + Separation of Concerns — Worked Examples

## Before: monolithic script (all violations)

```python
# main.py — does everything in one place
import os

def run():
    files = [f for f in os.listdir("input") if f.endswith(".csv")]
    files.sort()
    for filename in files:
        path = "input/" + filename
        with open(path) as f:
            data = f.read()
        rows = data.strip().split("\n")
        print(f"Processing {filename}: {len(rows)} rows")
        with open("output/summary.txt", "a") as out:
            out.write(f"{filename}: {len(rows)} rows\n")

run()
```

**Violations:**
- **S**: file discovery, processing, output writing, and printing are all one function
- **O**: adding a new format means editing `run()` directly
- **D**: no modules — nothing to depend on
- **Separation**: I/O paths hardcoded, printing inside processing logic, no layer separation

---

## After: correct structure

```python
# src/scanner/operations.py  — S: only discovers files
from pathlib import Path

SUPPORTED = {'.csv'}

def get_sorted_files(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(folder)
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    return sorted(
        (f for f in folder.iterdir() if f.suffix.lower() in SUPPORTED),
        key=lambda p: p.name.lower()
    )
```

```python
# src/processor/operations.py  — S: only processes content
from pathlib import Path

def count_rows(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())
```

```python
# src/reporter/operations.py  — S: only writes output
from pathlib import Path

def write_summary(output_path: Path, entries: list[tuple[str, int]]) -> None:
    lines = [f"{name}: {count} rows" for name, count in entries]
    output_path.write_text("\n".join(lines), encoding="utf-8")
```

```python
# index.py  — orchestrates only, no business logic
import sys
from pathlib import Path
from src.scanner.operations import get_sorted_files
from src.processor.operations import count_rows
from src.reporter.operations import write_summary

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def main() -> None:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    files = get_sorted_files(INPUT_DIR)
    if not files:
        print("No files found in input/")
        sys.exit(1)

    entries = []
    for i, f in enumerate(files, start=1):
        print(f"[{i}] {f.name}")
        entries.append((f.name, count_rows(f)))

    write_summary(OUTPUT_DIR / "summary.txt", entries)
    print(f"Done: output/summary.txt ({len(files)} file(s))")

if __name__ == "__main__":
    main()
```

---

## Principles satisfied — at a glance

| Principle | How it's applied |
|---|---|
| **S** | One module per job: scanner discovers, processor transforms, reporter writes |
| **O** | Add `.tsv` support by adding to `SUPPORTED` set — no logic changes |
| **L** | `get_sorted_files` works for any valid `Path` to a directory |
| **I** | Each function does one thing — `count_rows` doesn't also write anything |
| **D** | `index.py` imports modules; modules have zero knowledge of `index.py` |

## Separation of Concerns — layer ownership

| Layer | Owns | Must NOT own |
|---|---|---|
| `src/<module>/operations.py` | Pure logic, data transformation | Printing, hardcoded paths, I/O setup |
| `index.py` | I/O paths, directory setup, progress printing, orchestration | Any domain logic |
| `tests/` | Test assertions and fixtures | Calls to `index.py`, real filesystem access |

**Smell check:** if a module calls `print()`, hardcodes a path like `Path("input")`, or imports from `index.py` — it's violating separation of concerns.
