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
