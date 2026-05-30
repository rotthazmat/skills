import sys
from pathlib import Path

from src.<module>.operations import <function>

# Only include INPUT_DIR / OUTPUT_DIR for projects that read/write files
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main() -> None:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    items = <get_items>(INPUT_DIR)
    if not items:
        print("No items found in input/")
        sys.exit(1)

    for i, item in enumerate(items, start=1):
        print(f"[{i}] {item.name}")

    <process>(items, OUTPUT_DIR / "output.<ext>")
    print(f"Done: output/<file> ({len(items)} item(s))")


if __name__ == "__main__":
    main()
