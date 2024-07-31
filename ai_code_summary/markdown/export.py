import os
from pathlib import Path
from typing import Tuple

import pathspec
from loguru import logger

from ai_code_summary.ai.summary import summarize_content
from ai_code_summary.code.gitignore_pathspec import load_gitignore_patterns
from ai_code_summary.files.file_manager import clear_tmp_folder, get_code_files, read_file, write_files_to_tmp_directory

_EXCLUDE_GITIGNORE_DIRS = [".venv", ".pytest_cache", ".ruff_cache"]


def create_markdown_from_code(directory: str, exclude_gitignore_dirs: list[str] = _EXCLUDE_GITIGNORE_DIRS) -> None:
    """
    Creates a markdown file summarizing the code in the given directory.

    Args:
        directory (str): The directory containing the code to summarize.

    Returns:
        None
    """
    logger.info("Script started")

    base_dir = Path(directory)

    output_temp_dir = Path("./tmp")
    clear_tmp_folder(output_temp_dir)

    output_temp_code_dir = output_temp_dir / "code"
    output_temp_code_dir.mkdir(parents=True, exist_ok=True)

    # Load gitignore patterns to exclude certain files
    spec = load_gitignore_patterns(directory, exclude_gitignore_dirs)
    base_dir_name = base_dir.name if base_dir.name else os.path.basename(os.getcwd())
    output_markdown_file_name = output_temp_dir / f"{base_dir_name}.md"

    write_files_to_tmp_directory(directory, spec, base_dir, output_temp_code_dir)

    code_files = get_code_files(output_temp_code_dir, pathspec.PathSpec([]))
    file_contents = [read_file(file_path) for file_path in code_files]

    _write_markdown(output_temp_code_dir, base_dir_name, output_markdown_file_name, file_contents)
    logger.info("Script finished")


def _write_markdown(base_dir: Path, base_dir_name: str, output_markdown_file_name: Path, file_contents: list) -> None:
    """
    Writes the markdown summary for the given code files.

    Args:
        base_dir (Path): The base directory of the code files.
        base_dir_name (str): The name of the base directory.
        output_markdown_file_name (Path): The path to the output markdown file.
        file_contents (list): A list of tuples containing file paths and their contents.

    Returns:
        None
    """
    with open(output_markdown_file_name, "w") as f:
        f.write(f"# {base_dir_name}\n\n")
    [
        _write_markdown_file(file_info, base_dir, output_markdown_file_name)
        for file_info in file_contents
        if file_info[1]  # Only process files with content
    ]
    logger.info(f"Wrote markdown summary to {output_markdown_file_name}")


def _write_markdown_file(file_info: Tuple[Path, str], base_dir: Path, output_file_name: Path) -> None:
    """
    Appends a markdown summary for a single file to the output markdown file.

    Args:
        file_info (Tuple[Path, str]): A tuple containing the file path and its content.
        base_dir (Path): The base directory of the code files.
        output_file_name (Path): The path to the output markdown file.

    Returns:
        None
    """
    file_path, content = file_info
    summary = summarize_content(content)
    relative_path = file_path.relative_to(base_dir)
    with open(output_file_name, "a") as f:
        f.write(f"## {relative_path.name}\n\n")
        f.write(f"### Summary\n\n{summary}\n\n")
        f.write(f"```{file_path.suffix[1:]}\n")
        f.write(content)
        f.write("\n```\n")
    logger.info(f"Appended summary for {file_path} to {output_file_name}")
