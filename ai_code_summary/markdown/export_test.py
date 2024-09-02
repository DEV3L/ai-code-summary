import shutil
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from ai_code_summary.markdown.export import _write_markdown, _write_markdown_file, create_markdown_from_code


@pytest.fixture
def setup_test_directory(tmp_path: Path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.py").write_text("print('Hello, World!')")
    (test_dir / "file2.py").write_text("def foo(): pass")
    yield test_dir
    shutil.rmtree(test_dir)


@pytest.fixture
def mock_file_contents():
    return [(Path("tmp/code/file1.py"), "def foo(): pass"), (Path("tmp/code/file2.py"), "def bar(): pass")]


@patch("ai_code_summary.markdown.export.clear_tmp_folder")
@patch("ai_code_summary.markdown.export.write_files_to_tmp_directory")
@patch("ai_code_summary.markdown.export.get_code_files")
@patch("ai_code_summary.markdown.export.read_file")
@patch("ai_code_summary.markdown.export._write_markdown")
def test_create_markdown_from_code(
    mock_write_markdown,
    mock_read_file,
    mock_get_code_files,
    mock_write_files_to_tmp_directory,
    mock_clear_tmp_folder,
    setup_test_directory,
):
    mock_get_code_files.return_value = [setup_test_directory / "file1.py", setup_test_directory / "file2.py"]
    mock_read_file.side_effect = lambda x: (x, x.read_text())

    create_markdown_from_code(str(setup_test_directory))

    mock_clear_tmp_folder.assert_called_once()
    mock_write_files_to_tmp_directory.assert_called_once()
    mock_get_code_files.assert_called_once()
    mock_read_file.assert_any_call(setup_test_directory / "file1.py")
    mock_read_file.assert_any_call(setup_test_directory / "file2.py")
    mock_write_markdown.assert_called_once()


def test_write_markdown(mock_file_contents):
    base_dir = Path("./tmp/code")
    base_dir_name = "test_project"
    output_markdown_file_name = Path("./tmp/test_project.md")

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("ai_code_summary.markdown.export.summarize_content", return_value="Summary of content"):
            _write_markdown(base_dir, base_dir_name, output_markdown_file_name, mock_file_contents)
            mocked_file.assert_called_with(output_markdown_file_name, "a")
            handle = mocked_file()
            handle.write.assert_any_call(f"# {base_dir_name}\n\n")


def test_write_markdown_file(mock_file_contents):
    base_dir = Path("./tmp/code")
    output_file_name = Path("./tmp/test_project.md")
    file_info = mock_file_contents[0]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("ai_code_summary.markdown.export.summarize_content", return_value="Summary of content"):
            _write_markdown_file(file_info, base_dir, output_file_name)
            mocked_file.assert_called_with(output_file_name, "a")
            handle = mocked_file()
            handle.write.assert_any_call(f"## {file_info[0].name}\n\n")
            handle.write.assert_any_call("### Summary\n\nSummary of content\n\n")
            handle.write.assert_any_call(f"```{file_info[0].suffix[1:]}\n")
            handle.write.assert_any_call(file_info[1])
            handle.write.assert_any_call("\n```\n")
