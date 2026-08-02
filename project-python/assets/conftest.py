import pytest
from pathlib import Path


@pytest.fixture
def input_dir(tmp_path: Path) -> Path:
    d = tmp_path / "input"
    d.mkdir()
    return d


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    d = tmp_path / "output"
    d.mkdir()
    return d


@pytest.fixture
def make_<item>(input_dir: Path):
    """Factory — creates a <item> file in input_dir and returns its Path."""
    def _make(name: str, **kwargs) -> Path:
        path = input_dir / name
        # write content to path using kwargs
        return path
    return _make
