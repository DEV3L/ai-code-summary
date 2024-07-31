# AI Code Summary

This project automates the process of aggregating code files from a directory into a single markdown file, ready for use in an OpenAI Assistant or any RAG model. It intelligently skips files specified in the `.gitignore` and leverages ChatGPT to generate concise summaries for each code file, ensuring that the final markdown file is both comprehensive and easy to understand.

## Install through PyPI

```bash
pip install ai-code-summary
```

For more details, visit the [PyPI project page](https://pypi.org/project/ai-code-summary/).

## Setup

1. Clone the repository:

```bash
git clone https://github.com/DEV3L/ai-code-summary
cd ai-code-summary
```

2. Copy the env.local file to a new file named .env and replace `OPENAI_API_KEY` with your actual OpenAI API key:

```bash
cp env.default .env
```

3. Setup a virtual environment with dependencies and activate it:

```bash
brew install hatch
hatch env create
hatch shell
```

## Environment Variables

The following environment variables can be configured in the `.env` file:

- `OPENAI_MODEL`: The model to use
  - Default: `gpt-4o`
- `SUMMARY_PROMPT`: The prompt used to summarize code files
  - Default: `You are code summary expert. You summarize code in a short way that is easy to understand.`

## Testing

### End to End Test

```bash
hatch run e2e
```

### Unit Tests

```bash
hatch run test
```

### Coverage Gutters:

```bash
Command + Shift + P => Coverage Gutters: Watch
```

## Example

```
from ai_code_summary.markdown.export import create_markdown_from_code

if __name__ == "__main__":
    create_markdown_from_code(".")
```

Example output as a markdown file - [ai-code-summary.md](ai-code-summary.md)
