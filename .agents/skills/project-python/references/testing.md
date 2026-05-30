# Testing Reference

## Complete conftest.py example

```python
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
def make_text_file(input_dir: Path):
    def _make(name: str, content: str = "hello") -> Path:
        path = input_dir / name
        path.write_text(content, encoding="utf-8")
        return path
    return _make


@pytest.fixture
def make_json_file(input_dir: Path):
    import json
    def _make(name: str, data: dict = None) -> Path:
        path = input_dir / name
        path.write_text(json.dumps(data or {}), encoding="utf-8")
        return path
    return _make
```

## Complete test file example

```python
from pathlib import Path
import pytest

from src.scanner.operations import get_sorted_files


class TestGetSortedFiles:
    # --- Positive cases ---

    def test_returns_files_sorted_ascending(self, make_text_file, input_dir):
        make_text_file("charlie.txt")
        make_text_file("alpha.txt")
        make_text_file("bravo.txt")

        result = get_sorted_files(input_dir)

        assert [p.name for p in result] == ["alpha.txt", "bravo.txt", "charlie.txt"]

    def test_sort_is_case_insensitive(self, input_dir):
        (input_dir / "B.txt").write_text("x")
        (input_dir / "a.txt").write_text("x")

        result = get_sorted_files(input_dir)

        assert result[0].name == "a.txt"

    def test_returns_only_matching_extension(self, make_text_file, input_dir):
        make_text_file("data.csv")
        (input_dir / "readme.txt").write_text("x")

        result = get_sorted_files(input_dir, extension=".csv")

        assert len(result) == 1 and result[0].name == "data.csv"

    # --- Negative cases ---

    def test_empty_folder_returns_empty_list(self, input_dir):
        assert get_sorted_files(input_dir) == []

    def test_missing_folder_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            get_sorted_files(tmp_path / "nonexistent")

    def test_file_path_raises_not_a_directory(self, tmp_path):
        f = tmp_path / "notadir.txt"
        f.write_text("x")
        with pytest.raises(NotADirectoryError):
            get_sorted_files(f)
```

## Mocking external dependencies

> **Project-specific** — only applies when a module calls something you can't control in tests: external APIs, network services, system time, or random values. Do NOT mock filesystem operations — use `tmp_path` fixtures instead.

```python
from unittest.mock import patch, MagicMock
import pytest

from src.fetcher.operations import fetch_data


class TestFetchData:
    def test_returns_parsed_response(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}

        with patch("src.fetcher.operations.requests.get", return_value=mock_response):
            result = fetch_data("https://api.example.com/data")

        assert result == {"status": "ok"}

    def test_raises_on_connection_error(self):
        with patch("src.fetcher.operations.requests.get", side_effect=ConnectionError):
            with pytest.raises(ConnectionError):
                fetch_data("https://api.example.com/data")
```

**Rules:**
- Patch at the call site, not the definition: `patch("src.fetcher.operations.requests.get")` not `patch("requests.get")`
- Always test both success AND failure paths when mocking
- If you're mocking more than 2 dependencies in one test, the function under test does too much — split it

## Anti-patterns

| Don't | Do instead |
|---|---|
| `assert len(result) > 0` | Assert exact count or contents |
| Multiple unrelated assertions in one test | One test = one scenario |
| `os.path` or string paths in fixtures | `pathlib.Path` + `tmp_path` |
| Shared mutable state between tests | Fresh fixtures per test (pytest default) |
| `import index` in a test file | Only import from `src/<module>/operations` |
| Fixtures that hit the real filesystem | Always scope to `tmp_path` |

## Parametrize vs separate methods

Use `@pytest.mark.parametrize` only when the test body is identical and only input/expected values differ:

```python
@pytest.mark.parametrize("name,expected", [
    ("A.PNG", True),
    ("b.jpg", True),
    ("doc.txt", False),
])
def test_is_supported_extension(name: str, expected: bool):
    assert is_supported(Path(name)) == expected
```

Use separate methods when the setup or assertion logic differs between cases.
