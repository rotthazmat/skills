import os
import shutil
import sys
from pathlib import Path


def _external_dir(name: str) -> Path:
    """Returns the OS-specific user cache dir for a named external binary download."""
    if sys.platform == "win32":
        return Path(os.environ["LOCALAPPDATA"]) / name
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / name
    return Path.home() / ".cache" / name


def remove(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
        print(f"Eliminado: {path}")
    else:
        print(f"No encontrado: {path}")


def main() -> None:
    remove(Path(__file__).parent / "venv")
    # Add one line per external binary download the project uses, e.g.:
    # remove(_external_dir("ms-playwright"))
    print("Listo.")


if __name__ == "__main__":
    main()
