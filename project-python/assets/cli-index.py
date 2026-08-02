# Use this template instead of assets/index.py when the project needs
# command-line arguments (--input, --output, --verbose, custom flags, etc.)

import argparse
import sys
from pathlib import Path

from src.<module>.operations import <function>


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="<one-line project description>")
    parser.add_argument(
        "--input", type=Path, default=Path("input"),
        help="Input directory (default: input/)",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("output"),
        help="Output directory (default: output/)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.input.mkdir(exist_ok=True)
    args.output.mkdir(exist_ok=True)

    items = <get_items>(args.input)
    if not items:
        print(f"No items found in {args.input}/")
        sys.exit(1)

    for i, item in enumerate(items, start=1):
        print(f"[{i}] {item.name}")

    <process>(items, args.output / "output.<ext>")
    print(f"Done: {args.output}/<file> ({len(items)} item(s))")


if __name__ == "__main__":
    main()
