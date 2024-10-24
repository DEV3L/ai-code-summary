import os
import shutil
from pathlib import Path
from typing import List, Tuple

import pathspec
from loguru import logger

# Set of recognized code file extensions
_CODE_EXTENSIONS = {
    ".c",
    ".cpp",
    ".cs",
    ".css",
    ".default",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".yml",
    "Dockerfile",
}


def read_file(file_path: Path) -> Tuple[Path, str]:
    """
    Reads the content of a file.

    Args:
        file_path (Path): The path to the file to be read.

    Returns:
        Tuple[Path, str]: A tuple containing the file path and its content as a string.
    """
    try:
        with file_path.open("rb") as f:
            content = f.read().decode("utf-8", errors="ignore")
        logger.info(f"Read file {file_path}")
    except (OSError, UnicodeDecodeError) as e:
        logger.error(f"Error reading {file_path}: {e}")
        content = ""
    return file_path, content


def clear_tmp_folder(tmp_dir: Path) -> None:
    """
    Clears the contents of a temporary directory and recreates it.

    Args:
        tmp_dir (Path): The path to the temporary directory.
    """
    if tmp_dir.exists() and tmp_dir.is_dir():
        shutil.rmtree(tmp_dir)
        logger.info(f"Cleared contents of {tmp_dir}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created directory {tmp_dir}")


def get_code_files(directory: str, spec: pathspec.PathSpec) -> List[Path]:
    """
    Retrieves a list of code files in a directory, excluding those that match the given pathspec.

    Args:
        directory (str): The directory to search for code files.
        spec (pathspec.PathSpec): The pathspec to filter out files.

    Returns:
        List[Path]: A list of paths to the code files.
    """
    base_dir = Path(directory)

    # Recursively collect all files in the directory
    all_files = [Path(root) / file for root, _, files in os.walk(base_dir) for file in files]

    # Filter files to include only code files
    code_files = [file for file in all_files if _is_code_file(file)]
    # Further filter files based on the pathspec
    filtered_files = [file for file in code_files if not spec.match_file(file.relative_to(base_dir))]

    logger.info(f"Found {len(filtered_files)} code files in {directory}")
    return filtered_files


def _is_code_file(file: Path) -> bool:
    """
    Checks if a file is a code file based on its extension or name.

    Args:
        file (Path): The file to check.

    Returns:
        bool: True if the file is a code file, False otherwise.
    """
    return file.suffix in _CODE_EXTENSIONS or file.name == "Dockerfile"


def write_files_to_tmp_directory(directory: str, spec: List[str], base_dir: Path, output_temp_code_dir: Path) -> None:
    """
    Writes code files from a directory to a temporary directory, maintaining the directory structure.

    Args:
        directory (str): The directory to search for code files.
        spec (List[str]): The pathspec to filter out files.
        base_dir (Path): The base directory to calculate relative paths.
        output_temp_code_dir (Path): The directory where the files will be written.
    """
    code_files = get_code_files(directory, spec)
    file_contents = [read_file(file_path) for file_path in code_files]
    [_write_file(file_info, base_dir, output_temp_code_dir) for file_info in file_contents]


def _write_file(file_info: Tuple[Path, str], base_dir: Path, output_dir: Path) -> None:
    """
    Writes content to a file in the specified output directory.

    Args:
        file_info (Tuple[Path, str]): A tuple containing the file path and its content.
        base_dir (Path): The base directory to calculate relative paths.
        output_dir (Path): The directory where the file will be written.
    """
    file_path, content = file_info

    # Calculate the relative path to maintain directory structure
    relative_path = file_path.relative_to(base_dir)
    output_file = output_dir / relative_path.name

    with output_file.open("w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Wrote file {output_file}")
