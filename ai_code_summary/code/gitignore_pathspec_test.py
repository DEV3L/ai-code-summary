from pathlib import Path

import pytest

from ai_code_summary.code.gitignore_pathspec import _find_gitignore_files, load_gitignore_patterns


@pytest.fixture
def tmp_gitignore_files(tmp_path: Path):
    # Create a temporary directory structure with .gitignore files
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / ".gitignore").write_text("*.pyc\n__pycache__/\n")
    (tmp_path / "dir2" / ".gitignore").write_text("*.log\n")
    return tmp_path


@pytest.fixture
def tmp_no_gitignore_files(tmp_path: Path):
    (tmp_path / "dir1").mkdir()
    return tmp_path


def test_find_gitignore_files(tmp_gitignore_files: Path):
    gitignore_files = _find_gitignore_files(tmp_gitignore_files, ["dir2"])
    assert len(gitignore_files) == 1
    assert (tmp_gitignore_files / "dir1" / ".gitignore") in gitignore_files
    assert (tmp_gitignore_files / "dir2" / ".gitignore") not in gitignore_files


def test_load_gitignore_patterns(tmp_gitignore_files: Path):
    pathspec = load_gitignore_patterns(tmp_gitignore_files, [])
    assert pathspec.match_file("test.pyc")
    assert pathspec.match_file("__pycache__/")
    assert pathspec.match_file("test.log")
    assert not pathspec.match_file("test.txt")


def test_load_gitignore_patterns_no_gitignore_files(tmp_no_gitignore_files: Path):
    pathspec = load_gitignore_patterns(tmp_no_gitignore_files, [])

    assert len(pathspec.patterns) == 0
