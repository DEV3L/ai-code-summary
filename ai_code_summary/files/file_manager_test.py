from pathlib import Path
from unittest.mock import patch

import pytest
from pathspec import PathSpec

from ai_code_summary.files.file_manager import clear_tmp_folder, get_code_files, read_file, write_file


@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path:
    return tmp_path / "tmp"


def test_read_file_success(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding="utf-8")

    file_path, content = read_file(test_file)

    assert file_path == test_file
    assert content == test_content


def test_read_file_nonexistent():
    test_file = Path("nonexistent.txt")

    file_path, content = read_file(test_file)

    assert file_path == test_file
    assert content == ""


def test_write_file(tmp_path: Path):
    # Create a temporary file and directories
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    test_file = base_dir / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content)

    # Test write_file function
    write_file((test_file, test_content), base_dir, output_dir)
    output_file = output_dir / "test.txt"
    assert output_file.exists()
    assert output_file.read_text() == test_content


def test_clear_tmp_folder(tmp_dir: Path):
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / "test.txt").write_text("Temporary file", encoding="utf-8")

    clear_tmp_folder(tmp_dir)

    assert tmp_dir.exists()
    assert tmp_dir.is_dir()
    assert not any(tmp_dir.iterdir())


def test_get_code_files(tmp_path: Path):
    # Create a mock PathSpec
    spec = PathSpec.from_lines("gitwildmatch", ["*.ignore"])

    # Create some test files
    (tmp_path / "test.py").write_text("print('Hello, world!')")
    (tmp_path / "test.ignore").write_text("This should be ignored")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "test.js").write_text("console.log('Hello, world!')")

    # Mock os.walk to control the directory structure
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (str(tmp_path), [], ["test.py", "test.ignore"]),
            (str(tmp_path / "subdir"), [], ["test.js"]),
        ]

        # Call the function
        result = get_code_files(str(tmp_path), spec)

    # Verify the result
    expected_files = {tmp_path / "test.py", tmp_path / "subdir" / "test.js"}
    assert set(result) == expected_files
