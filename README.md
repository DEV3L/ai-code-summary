# AI Code Summary

![AI Code Summary Banner](ai-code-summary.png)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ai-code-summary)
![PyPI version](https://img.shields.io/pypi/v/ai-code-summary)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Build Status](https://img.shields.io/github/actions/workflow/status/DEV3L/ai-code-summary/continuous-integration.yml?branch=main)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

## Introduction

**AI Code Summary** is an **open-source** tool that automates the process of aggregating code files from a directory into a single markdown file. It intelligently skips files specified in the `.gitignore` and leverages OpenAI's GPT models to generate concise summaries for each code file. The final markdown file is both comprehensive and easy to understand, making it suitable for use in OpenAI Assistant or any Retrieval-Augmented Generation (RAG) model.

## Value Proposition

By automating code summarization and aggregation, **AI Code Summary** streamlines documentation efforts and enhances codebase comprehension. It saves developers time by reducing the manual effort required to create summaries, helps in onboarding new team members, and facilitates code reviews by providing clear overviews of the code structure and functionality.

## Key Features

- **Open Source**: Freely available and community-driven.
- **Automated Code Summarization**: Utilizes OpenAI's GPT models to generate concise summaries of code files.
- **Markdown Aggregation**: Combines code and summaries into a single, well-structured markdown file.
- **Gitignore Aware**: Skips files and directories specified in `.gitignore`.
- **Customizable Prompts**: Allows customization of the summary prompt used by the AI model.
- **Easy Integration**: Installable via PyPI and integrable into existing workflows.
- **Testing Suite**: Includes unit and end-to-end tests to ensure reliability.

## Technology Stack

- **Programming Language**: Python 3.11+
- **Frameworks and Libraries**:
  - **OpenAI API**: For generating code summaries.
  - **Pathspec**: For parsing `.gitignore` patterns.
  - **Loguru**: For logging.
  - **Python-dotenv**: For environment variable management.
  - **Hatch**: For environment management and packaging.
  - **Pytest**: For testing.
  - **Ruff**: For linting and code style enforcement.

## Installation Instructions

### Install via PyPI

**AI Code Summary** is published on PyPI and can be easily installed using `pip`:

```bash
pip install ai-code-summary
```

For more details, visit the [PyPI project page](https://pypi.org/project/ai-code-summary/).

### From Source

1. **Clone the repository**:

   ```bash
   git clone https://github.com/DEV3L/ai-code-summary.git
   cd ai-code-summary
   ```

2. **Set up environment variables**:

   Copy the `env.default` file to `.env` and replace placeholders with your actual OpenAI API key:

   ```bash
   cp env.default .env
   ```

   Edit `.env` to add your `OPENAI_API_KEY`:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Set up a virtual environment**:

   **Install Hatch** (if not already installed):

   ```bash
   pip install hatch
   ```

   **Create and activate the virtual environment**:

   ```bash
   hatch env create
   hatch shell
   ```

## Usage Guide

To generate a markdown summary of your code files:

1. **Ensure your OpenAI API key is set in the `.env` file**.
2. **Run the following script**:

   ```bash
   hatch run run_end_to_end.py
   ```

   This will generate a markdown file summarizing the code in the current directory.

### Example Output

An example output file is available at [ai-code-summary.md](ai-code-summary.md).

## Available Scripts

- **Run End-to-End Test**:

  ```bash
  hatch run e2e
  ```

- **Run Unit Tests**:

  ```bash
  hatch run test
  ```

- **Publish Package to PyPI**:

  ```bash
  hatch run publish
  ```

_Note: These scripts are defined in `pyproject.toml` under `[tool.hatch.envs.default.scripts]`._

## Testing Instructions

### End-to-End Test

Run the end-to-end test to ensure the tool works as expected:

```bash
hatch run e2e
```

### Unit Tests

To run unit tests:

```bash
hatch run test
```

Coverage reports are generated using `pytest-cov`.

### Coverage Gutters

To monitor code coverage in VSCode:

1. Install the **Coverage Gutters** extension.
2. Run:

   ```bash
   Command + Shift + P => Coverage Gutters: Watch
   ```

## Project Structure Overview

```
ai-code-summary/
├── ai_code_summary/
│   ├── ai/
│   │   └── summary.py
│   ├── code/
│   │   └── gitignore_pathspec.py
│   ├── files/
│   │   └── file_manager.py
│   ├── markdown/
│   │   └── export.py
│   └── env_variables.py
├── tests/
│   ├── ai/
│   │   └── summary_test.py
│   ├── code/
│   │   └── gitignore_pathspec_test.py
│   ├── files/
│   │   └── file_manager_test.py
│   └── markdown/
│       └── export_test.py
├── .env.default
├── pyproject.toml
├── README.md
├── run_end_to_end.py
├── LICENSE
```

- **ai_code_summary/**: Main package containing the code.
  - **ai/**: Functions related to AI summarization.
  - **code/**: Handles `.gitignore` parsing.
  - **files/**: Manages file operations.
  - **markdown/**: Generates markdown files.
  - **env_variables.py**: Manages environment variables.
- **tests/**: Contains unit tests for the code.
- **.env.default**: Template for environment variables.
- **pyproject.toml**: Project configuration and dependencies.
- **run_end_to_end.py**: Script to execute the end-to-end process.
- **LICENSE**: Project license information.

## Contributing Guidelines

We welcome contributions! Please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit them with clear messages.
4. **Run tests** to ensure nothing is broken:

   ```bash
   hatch run test
   ```

5. **Push to your fork** and submit a **pull request** to the `main` branch.

_Note: Please provide a `CONTRIBUTING.md` file with detailed contributing guidelines if available._

## License Information

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** - For providing the GPT models used in code summarization.
- **Community Contributors** - Thank you to all who have contributed through issues and pull requests.

## Additional Resources

- **PyPI Project Page**: [ai-code-summary](https://pypi.org/project/ai-code-summary/)
