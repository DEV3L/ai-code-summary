import os
import shutil
from pathlib import Path
from typing import List, Tuple

import pathspec
from loguru import logger

_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".html",
    ".css",
    ".cs",
    ".yml",
    ".toml",
    ".default",
    "Dockerfile",
}


def read_file(file_path: Path) -> Tuple[Path, str]:
    """
    Reads the content of a file, ignoring decoding errors to ensure the process doesn't fail.
    Logs the operation for traceability.

    Args:
        file_path (Path): The path to the file to be read.

    Returns:
        Tuple[Path, str]: The file path and its content.
    """
    try:
        with file_path.open("rb") as f:
            content = f.read().decode("utf-8", errors="ignore")
        logger.info(f"Read file {file_path}")
    except (OSError, UnicodeDecodeError) as e:
        logger.error(f"Error reading {file_path}: {e}")
        content = ""
    return file_path, content


def write_file(file_info: Tuple[Path, str], base_dir: Path, output_dir: Path) -> None:
    """
    Writes content to a file in the output directory, maintaining the relative path structure.
    Ensures the output directory structure mirrors the base directory structure.

    Args:
        file_info (Tuple[Path, str]): The file path and its content.
        base_dir (Path): The base directory to maintain relative paths.
        output_dir (Path): The directory where the file will be written.
    """
    file_path, content = file_info

    relative_path = file_path.relative_to(base_dir)
    output_file = output_dir / relative_path.name

    with output_file.open("w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Wrote file {output_file}")


def clear_tmp_folder(tmp_dir: Path) -> None:
    """
    Clears the contents of a temporary directory and recreates it.
    Ensures a clean state for temporary operations.

    Args:
        tmp_dir (Path): The temporary directory to be cleared and recreated.
    """
    if tmp_dir.exists() and tmp_dir.is_dir():
        shutil.rmtree(tmp_dir)
        logger.info(f"Cleared contents of {tmp_dir}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created directory {tmp_dir}")


def get_code_files(directory: str, spec: pathspec.PathSpec) -> List[Path]:
    base_dir = Path(directory)

    code_files = [
        Path(root) / file
        for root, _, files in os.walk(base_dir)
        for file in files
        if not spec.match_file((Path(root) / file).relative_to(base_dir)) and _is_code_file(Path(root) / file)
    ]
    
    logger.info(f"Found {len(code_files)} code files in {directory}")
    return code_files


def _is_code_file(file: Path) -> bool:
    return file.suffix in _CODE_EXTENSIONS or file.name == "Dockerfile"
