import os
import time
from pathlib import Path
from typing import List, Tuple

import pathspec
from loguru import logger
from openai import OpenAI

from ai_code_summary.code.gitignore_pathspec import load_gitignore_patterns
from ai_code_summary.files.file_manager import clear_tmp_folder, get_code_files, read_file, write_file

client = OpenAI()


def summarize_content(content: str) -> str:
    start_time = time.time()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are code summary expert. You summarize code in a short way that is easy to understand.",
            },
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )
    end_time = time.time()
    logger.debug(f"Summarized content in {end_time - start_time:.2f} seconds")
    return completion.choices[0].message.content


def write_markdown(base_dir, base_dir_name, output_markdown_file_name, file_contents):
    with open(output_markdown_file_name, "w") as f:
        f.write(f"# {base_dir_name}\n\n")
    [write_markdown_file(file_info, base_dir, output_markdown_file_name) for file_info in file_contents if file_info[1]]
    logger.info(f"Wrote markdown summary to {output_markdown_file_name}")


def write_markdown_file(file_info: Tuple[Path, str], base_dir: Path, output_file_name: Path) -> None:
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


def write_files_to_tmp_directory(directory: str, spec: List[str], base_dir: Path, output_temp_code_dir: Path) -> None:
    code_files = get_code_files(directory, spec)
    file_contents = [read_file(file_path) for file_path in code_files]
    [write_file(file_info, base_dir, output_temp_code_dir) for file_info in file_contents]


def create_markdown_from_code(directory: str) -> None:
    logger.info("Script started")

    base_dir = Path(directory)

    output_temp_dir = Path("./tmp")
    clear_tmp_folder(output_temp_dir)

    output_temp_code_dir = output_temp_dir / "code"
    output_temp_code_dir.mkdir(parents=True, exist_ok=True)

    spec = load_gitignore_patterns(directory)
    base_dir_name = base_dir.name if base_dir.name else os.path.basename(os.getcwd())
    output_markdown_file_name = output_temp_dir / f"{base_dir_name}.md"

    write_files_to_tmp_directory(directory, spec, base_dir, output_temp_code_dir)

    code_files = get_code_files(output_temp_code_dir, pathspec.PathSpec([]))
    file_contents = [read_file(file_path) for file_path in code_files]

    write_markdown(output_temp_code_dir, base_dir_name, output_markdown_file_name, file_contents)
    logger.info("Script finished")


if __name__ == "__main__":
    create_markdown_from_code(".")
