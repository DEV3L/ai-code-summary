# ai-code-summary

## pyproject.toml

### Summary

This is a Python project configuration file (`pyproject.toml`) for a project named "ai-code-summary." Here's a summary:

1. **Build System**: Uses `hatchling` as the build backend.
2. **Project Info**:
   - **Name**: ai-code-summary
   - **Description**: Automates the aggregation of code files into a markdown file, skipping files in `.gitignore` and using ChatGPT for summaries.
   - **Author**: Justin Beall
   - **License**: MIT License
   - **Python Requirement**: >=3.11
   - **Dependencies**: Includes `loguru`, `openai`, `pathspec`, `python-dotenv`, `twine`
   - **Keywords**: openai, code summary, AI, automation, python, API, artificial intelligence, data science
3. **Classifiers**: Specifies development status, intended audience, license, and compatible Python versions.
4. **URLs**: Provides a GitHub repository link.
5. **Versioning**: Manages versions using `hatch` with setup in `setup.cfg`.
6. **Build Targets**: Defines source distribution (sdist) and wheel targets.
7. **Virtual Environment**: Configures a default virtual environment with specific dependencies and scripts for testing, building, and publishing.
8. **Static Analysis**: Sets up `ruff` for code linting with configurations to ban relative imports.

This setup aims to streamline development and distribution, emphasizing automation and integration with AI tools.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "ai-code-summary"
dynamic = ["version"]
description = "This project automates the process of aggregating code files from a directory into a single markdown file, ready for use in an OpenAI Assistant or any RAG model. It intelligently skips files specified in the .gitignore and leverages ChatGPT to generate concise summaries for each code file, ensuring that the final markdown file is both comprehensive and easy to understand."
license = { file = "LICENSE" }
readme = "README.md"
authors = [{ name = "Justin Beall", email = "jus.beall@gmail.com" }]
requires-python = ">=3.11"
dependencies = ["loguru", "openai", "pathspec", "python-dotenv", "twine"]
keywords = [
    "openai",
    "code summary",
    "AI",
    "automation",
    "python",
    "API",
    "artificial intelligence",
    "data science",
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

[project.urls]
repository = "https://github.com/DEV3L/ai-code-summary"

[tool.hatch.version]
path = "setup.cfg"
pattern = "version = (?P<version>\\S+)"

[tool.hatch.build.targets.sdist]
include = ["/ai_code_summary"]
artifact = { name = "ai-code-summary" }

[tool.hatch.build.targets.wheel]
packages = ["ai_code_summary"]
artifact = { name = "ai-code-summary" }

[tool.hatch.envs.default]
type = "virtual"
path = ".venv"
dependencies = ["pyright", "pytest", "pytest-cov"]

[tool.hatch.envs.default.scripts]
e2e = "python run_end_to_end.py"
test = "pytest --cache-clear --cov --cov-report lcov --cov-report term"
publish = "rm -rf bin && rm -rf dist && hatch build && twine upload dist/*"

[tool.hatch.envs.hatch-static-analysis]
config-path = "ruff_defaults.toml"

[tool.ruff]
extend = "ruff_defaults.toml"

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "parents"

```

## continuous-integration.yml

### Summary

This GitHub Actions workflow named "Continuous Integration" triggers on any branch push. It runs a job called "Tests" on the latest Ubuntu version, performs a series of steps including checking out the code, setting up Python 3.x, installing dependencies using the Hatch tool, and executing unit tests.

```yml
name: Continuous Integration

on:
  push:
    branches: ["**"]

jobs:
  tests:
    name: "Tests"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          python -m pip install hatch
          hatch env create
      - name: Unit tests
        run: |
          hatch run test
```

## gitignore_pathspec_test.py

### Summary

The code is a set of tests for functions related to handling `.gitignore` files. It uses the `pytest` framework along with the `pathlib` library to create temporary directory structures.

Key points:

- Two fixtures create temporary directories: one with `.gitignore` files (`tmp_gitignore_files`), and one without (`tmp_no_gitignore_files`).
- Three tests:
  - `test_find_gitignore_files` ensures `_find_gitignore_files` correctly identifies `.gitignore` files in specified directories.
  - `test_load_gitignore_patterns` checks if `load_gitignore_patterns` correctly identifies files based on `.gitignore` patterns.
  - `test_load_gitignore_patterns_no_gitignore_files` verifies that `load_gitignore_patterns` returns no patterns when no `.gitignore` files exist.

```py
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

```

## export.py

### Summary

This code creates a markdown summary of code files in a specified directory, excluding certain directories defined by `.gitignore` patterns and some predefined folders. The key functions are:

1. **`create_markdown_from_code(directory: str, exclude_gitignore_dirs: list[str]) -> None`**:

   - Main function to create a markdown summary.
   - Clears temporary directories and creates necessary folders.
   - Loads `.gitignore` patterns to exclude files.
   - Writes code files to a temporary directory.
   - Reads and processes code files, and writes their summaries to a markdown file.

2. **`_write_markdown(base_dir: Path, base_dir_name: str, output_markdown_file_name: Path, file_contents: list) -> None`**:

   - Writes the markdown summary for all code files.
   - Calls `_write_markdown_file` for each file that has content.

3. **`_write_markdown_file(file_info: Tuple[Path, str], base_dir: Path, output_file_name: Path) -> None`**:
   - Appends a summary for a single code file to the markdown file.
   - Uses an external function `summarize_content` to generate the summary.

Supporting functions handle file managing tasks like clearing temporary folders, reading files, etc.

````py
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

````

## summary.py

### Summary

This code defines a module for summarizing text using the OpenAI API. It contains two main functions:

1. `_get_open_ai_client()`: Initializes and returns an OpenAI client using an API key.
2. `summarize_content(content: str)`: Summarizes given content by making an API call to OpenAI, logs the time taken for the API call, and returns the summarized content.

```py
import time

from loguru import logger
from openai import OpenAI

from ai_code_summary.env_variables import OPENAI_API_KEY, OPENAI_MODEL, SUMMARY_PROMPT


def _get_open_ai_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client using the provided API key.

    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return OpenAI(api_key=OPENAI_API_KEY)


def summarize_content(content: str) -> str:
    """
    Summarizes the given content using the OpenAI API.

    Args:
        content (str): The content to be summarized.

    Returns:
        str: The summarized content.
    """
    start_time = time.time()  # Record the start time to measure the duration of the API call
    completion = _get_open_ai_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )
    end_time = time.time()  # Record the end time to measure the duration of the API call
    logger.debug(f"Summarized content in {end_time - start_time:.2f} seconds")  # Log the duration of the API call
    return completion.choices[0].message.content  # Return the summarized content

```

## export_test.py

### Summary

This Python script uses `pytest` for testing and `unittest.mock` for mocking dependencies. It involves the functionality of exporting code summaries to Markdown files. Here's a brief summary:

1. **Setup for Testing:**

   - **Fixtures:**
     - `setup_test_directory`: Creates a temporary testing directory with two Python files.
     - `mock_file_contents`: Mock content for files used in tests.

2. **Tests:**
   - `test_create_markdown_from_code`: Mocks several functions (`clear_tmp_folder`, `write_files_to_tmp_directory`, `get_code_files`, `read_file`, `_write_markdown`) to test `create_markdown_from_code`, ensuring it reads files and writes markdown correctly.
   - `test_write_markdown`: Tests the `_write_markdown` function by checking if it writes to a markdown file correctly, using mocked file content.
   - `test_write_markdown_file`: Verifies `_write_markdown_file` to ensure it formats and writes file details to markdown correctly, mocking file operations and content summarization.

These tests validate that the functions handle file operations and correctly generate Markdown summaries from given code files.

````py
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

````

## env_variables.py

### Summary

The code loads environment variables from a `.env` file using the `dotenv` library. It then retrieves and sets default values for `OPENAI_API_KEY`, `OPENAI_MODEL`, and `SUMMARY_PROMPT`.

```py
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "${OPENAI_API_KEY}")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

SUMMARY_PROMPT = os.getenv(
    "SUMMARY_PROMPT", ("You are code summary expert. You summarize code in a short way that is easy to understand.")
)

```

## ruff_defaults.toml

### Summary

This configuration file sets coding standards:

- Maximum line length is 120 characters.
- Formats docstrings to include code and limits docstring code lines to 80 characters.
- Bans all relative imports.
- Identifies the "src" directory as first-party for import sorting.
- Specifies no parentheses for pytest fixtures and marks.

```toml
line-length = 120

[format]
docstring-code-format = true
docstring-code-line-length = 80

[lint.flake8-tidy-imports]
ban-relative-imports = "all"

[lint.isort]
known-first-party = ["src"]

[lint.flake8-pytest-style]
fixture-parentheses = false
mark-parentheses = false
```

## gitignore_pathspec.py

### Summary

This code provides functionality to locate and read `.gitignore` files within a given directory, excluding specified subdirectories, and then aggregates all patterns from these files into a `pathspec.PathSpec` object. The key components are:

1. **\_find_gitignore_files**: Recursively searches for `.gitignore` files in a given directory, excluding specified directories.
2. **\_read_patterns_from_file**: Reads and returns patterns from a specified `.gitignore` file.
3. **load_gitignore_patterns**: Combines functionalities of the two helper functions to load all `.gitignore` patterns from the directory and returns them as a `pathspec.PathSpec` object. Logs the process of loading the patterns.

```py
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

```

## summary_test.py

### Summary

This code defines a test function, `test_summarize_content`, that uses the `unittest.mock` library to mock the behavior of an OpenAI client. It verifies that the `summarize_content` function correctly generates a summary for a given piece of code.

1. `@patch("ai_code_summary.ai.summary.OpenAI")` mocks the OpenAI client.
2. Inside the test, a `MagicMock` client is created to simulate the OpenAI response.
3. The mock OpenAI client returns a pre-defined summary: "This is a summary."
4. The test checks that `summarize_content("def example_function(): pass")` returns this summary.
5. Finally, it confirms that the OpenAI client was called correctly with the expected parameters.

```py
from unittest.mock import MagicMock, patch

from ai_code_summary.ai.summary import summarize_content
from ai_code_summary.env_variables import OPENAI_MODEL, SUMMARY_PROMPT


@patch("ai_code_summary.ai.summary.OpenAI")
def test_summarize_content(mock_get_open_ai):
    mock_client = MagicMock()
    mock_get_open_ai.return_value = mock_client
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "This is a summary."
    mock_client.chat.completions.create.return_value = mock_completion

    content = "def example_function(): pass"

    result = summarize_content(content)

    assert result == "This is a summary."
    mock_get_open_ai.assert_called_once()
    mock_client.chat.completions.create.assert_called_once_with(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )

```

## file_manager.py

### Summary

This code provides utilities for handling code files in a specified directory. It can filter code files, read their contents, and write them to a temporary directory while preserving the directory structure. The main components are:

1. **File Reading (`read_file`)**: Reads the content of a given file.
2. **Temporary Directory Management (`clear_tmp_folder`)**: Clears and recreates a temporary directory.
3. **Code File Retrieval (`get_code_files`)**: Finds code files in a directory based on specific file extensions and a pathspec filter.
4. **File Type Check (`_is_code_file`)**: Checks if a file is a code file by its extension or name.
5. **Writing Files to Temp Directory (`write_files_to_tmp_directory`)**: Copies and writes code files to a temporary directory, preserving the original structure.
6. **File Writing (`_write_file`)**: Writes file content to an output directory.

Logging is used extensively for tracking operations and any errors that occur.

```py
import os
import shutil
from pathlib import Path
from typing import List, Tuple

import pathspec
from loguru import logger

# Set of recognized code file extensions
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

```

## file_manager_test.py

### Summary

The provided code conducts unit tests for file management functionalities from the `ai_code_summary.files.file_manager` module. Here's a brief summary:

1. **Setup Fixture**:

   - `tmp_dir`: Creates a temporary directory for the tests.

2. **Tests**:
   - `test_read_file_success`: Verifies successful reading of an existing file.
   - `test_read_file_nonexistent`: Ensures reading a nonexistent file returns an empty string.
   - `test_clear_tmp_folder`: Validates that the `clear_tmp_folder` function clears the given temporary directory.
   - `test_get_code_files`: Checks `get_code_files` to fetch code files excluding ignored patterns, using a mock for `os.walk` to simulate directory structure.
   - `test_write_files_to_tmp_directory`: Uses mock objects to test `write_files_to_tmp_directory`, ensuring correct file reading and writing behaviors.
   - `test_write_file`: Tests the `_write_file` function to ensure it writes a file from the base directory to an output directory correctly.

These tests validate critical file handling functions by creating temporary files, mocking behaviors, and asserting expected outcomes.

```py
from pathlib import Path
from unittest.mock import patch

import pytest
from pathspec import PathSpec

from ai_code_summary.files.file_manager import (
    _write_file,
    clear_tmp_folder,
    get_code_files,
    read_file,
    write_files_to_tmp_directory,
)


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

        result = get_code_files(str(tmp_path), spec)

    expected_files = {tmp_path / "test.py", tmp_path / "subdir" / "test.js"}
    assert set(result) == expected_files


@patch("ai_code_summary.files.file_manager.get_code_files")
@patch("ai_code_summary.files.file_manager.read_file")
@patch("ai_code_summary.files.file_manager._write_file")
def test_write_files_to_tmp_directory(mock_write_file, mock_read_file, mock_get_code_files):
    directory = "test_directory"
    spec = ["*.py"]
    base_dir = Path("base_dir")
    output_temp_code_dir = Path("output_temp_code_dir")

    mock_get_code_files.return_value = [Path("file1.py"), Path("file2.py")]
    mock_read_file.side_effect = [(Path("file1.py"), "content1"), (Path("file2.py"), "content2")]

    write_files_to_tmp_directory(directory, spec, base_dir, output_temp_code_dir)

    mock_get_code_files.assert_called_once_with(directory, spec)
    assert mock_read_file.call_count == 2
    assert mock_write_file.call_count == 2
    mock_write_file.assert_any_call((Path("file1.py"), "content1"), base_dir, output_temp_code_dir)
    mock_write_file.assert_any_call((Path("file2.py"), "content2"), base_dir, output_temp_code_dir)


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
    _write_file((test_file, test_content), base_dir, output_dir)
    output_file = output_dir / "test.txt"
    assert output_file.exists()
    assert output_file.read_text() == test_content

```

## .env.default

### Summary

This code snippet sets up environment variables for the OpenAI API key and model, and defines a project variable with a prompt for summarizing code in a simple and clear manner.

```default
# OpenAI
OPENAI_API_KEY=${OPENAI_API_KEY}
OPENAI_MODEL=${OPENAI_MODEL}

# Project
SUMMARY_PROMPT="You are code summary expert. You summarize code in a short way that is easy to understand."

```

## run_end_to_end.py

### Summary

The code imports the `create_markdown_from_code` function from the `ai_code_summary.markdown.export` module and then calls this function with the current directory (`"."`) as the argument if the script is run as the main module. This effectively generates a markdown summary of the code files in the current directory.

```py
from ai_code_summary.markdown.export import create_markdown_from_code

if __name__ == "__main__":
    create_markdown_from_code(".")

```
