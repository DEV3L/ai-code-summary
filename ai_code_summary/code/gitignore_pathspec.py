from functools import reduce
from pathlib import Path
from typing import List

import pathspec
from loguru import logger


def _find_gitignore_files(directory: str) -> List[Path]:
    """
    Recursively find all .gitignore files in the given directory.

    This function is used to locate all .gitignore files within a given directory
    and its subdirectories. This is necessary because .gitignore files can be
    scattered throughout a project, and we need to aggregate all patterns from
    these files.
    """
    return list(Path(directory).rglob(".gitignore"))


def _read_patterns_from_file(file_path: Path) -> List[str]:
    """
    Read and return patterns from a .gitignore file.

    This function reads the contents of a .gitignore file and returns the patterns
    as a list of strings. These patterns are used to match files that should be ignored
    by git.
    """
    with open(file_path, "r") as f:
        return f.read().splitlines()


def load_gitignore_patterns(directory: str) -> pathspec.PathSpec:
    """
    Load and combine patterns from all .gitignore files in the directory.

    This function aggregates all ignore patterns from .gitignore files found in the
    specified directory and its subdirectories. It uses these patterns to create a
    pathspec.PathSpec object, which can be used to match files against the combined
    ignore patterns.

    Args:
        directory (str): The directory to search for .gitignore files.

    Returns:
        pathspec.PathSpec: A PathSpec object containing all combined ignore patterns.
    """
    gitignore_files = _find_gitignore_files(directory)

    if not gitignore_files:
        logger.info(f"No .gitignore files found in {directory}")
        return pathspec.PathSpec([])

    # Combine all patterns from the found .gitignore files
    all_patterns = reduce(
        lambda acc, gitignore_path: acc + _read_patterns_from_file(gitignore_path), gitignore_files, []
    )

    logger.info(f"Loaded .gitignore patterns from {len(gitignore_files)} files")
    return pathspec.PathSpec.from_lines("gitwildmatch", all_patterns)
