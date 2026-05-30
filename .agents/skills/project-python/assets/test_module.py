import pytest
from pathlib import Path

from src.<module>.operations import <function>


class Test<FunctionName>:
    # --- Positive cases ---

    def test_happy_path(self, <fixture>) -> None:
        # arrange
        # act
        result = <function>(...)
        # assert
        assert result == <expected>

    def test_edge_case(self, <fixture>) -> None:
        pass

    # --- Negative cases (mandatory — never skip) ---

    def test_empty_input_returns_empty(self, input_dir: Path) -> None:
        assert <function>(input_dir) == []

    def test_missing_path_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            <function>(tmp_path / "nonexistent")

    def test_file_as_dir_raises_not_a_directory(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("x")
        with pytest.raises(NotADirectoryError):
            <function>(f)

    def test_invalid_data_raises_value_error(self, <fixture>) -> None:
        with pytest.raises(ValueError):
            <function>([])
