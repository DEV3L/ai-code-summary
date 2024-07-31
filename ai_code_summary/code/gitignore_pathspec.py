from functools import reduce
from pathlib import Path
from typing import List

import pathspec
from loguru import logger


def _find_gitignore_files(directory: str, exclude_dirs: List[str]) -> List[Path]:
    """
    Recursively find all .gitignore files in a directory, excluding specified directories.

    Args:
        directory (str): The root directory to search for .gitignore files.
        exclude_dirs (List[str]): Directories to exclude from the search.

    Returns:
        List[Path]: A list of paths to .gitignore files.
    """
    exclude_dirs = set(exclude_dirs or [])
    return [
        path
        for path in Path(directory).rglob(".gitignore")
        if not any(excluded in path.parts for excluded in exclude_dirs)
    ]


def _read_patterns_from_file(file_path: Path) -> List[str]:
    """
    Read patterns from a .gitignore file.

    Args:
        file_path (Path): The path to the .gitignore file.

    Returns:
        List[str]: A list of patterns from the .gitignore file.
    """
    with open(file_path, "r") as f:
        return f.read().splitlines()


def load_gitignore_patterns(directory: str, exclude_dirs: List[str]) -> pathspec.PathSpec:
    """
    Load .gitignore patterns from a directory, excluding specified directories.

    Args:
        directory (str): The root directory to search for .gitignore files.
        exclude_dirs (List[str] | None): Directories to exclude from the search. Defaults to _IGNORE_DIRS.

    Returns:
        pathspec.PathSpec: A PathSpec object containing all the loaded .gitignore patterns.
    """
    gitignore_files = _find_gitignore_files(directory, exclude_dirs)

    if not gitignore_files:
        logger.info(f"No .gitignore files found in {directory}")
        return pathspec.PathSpec([])

    # Combine all patterns from the found .gitignore files
    all_patterns = reduce(
        lambda acc, gitignore_path: acc + _read_patterns_from_file(gitignore_path), gitignore_files, []
    )

    logger.info(f"Loaded .gitignore patterns from {len(gitignore_files)} files")
    return pathspec.PathSpec.from_lines("gitwildmatch", all_patterns)
